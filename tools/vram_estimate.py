#!/usr/bin/env python3
"""How much GPU memory will Qwen3-8B Cooking Assistant need on your machine? A planning estimate, no GPU needed.

    python tools/vram_estimate.py                     # table for common setups
    python tools/vram_estimate.py --vram 6            # what fits on a 6 GB card
    python tools/vram_estimate.py --quant Q4_K_M --ctx 8192 --kv q8_0

Memory = model weights on the GPU + the KV cache (grows with context) + a compute buffer. The weights and cache
figures come from the model's shape; the buffer was measured with llama.cpp (see SMALL-GPU.md). Leave some headroom:
your desktop and browser use the GPU too.
"""
import argparse

# Qwen3-8B: 36 layers, 8 key/value heads of 128 dims (grouped-query attention)
LAYERS, KV_HEADS, HEAD_DIM = 36, 8, 128
GIB = 1024 ** 3

# file sizes of the published GGUFs (bytes)
QUANTS = {
    "Q4_K_M": 5_027_784_000,
    "Q6_K": 6_725_899_584,
    "Q8_0": 8_709_518_336,
    "BF16": 16_388_043_776,
}
# bytes per cached value: f16 = 2; q8_0 = 34 bytes per 32 values; q4_0 = 18 bytes per 32 values
KV_BYTES = {"f16": 2.0, "q8_0": 34 / 32, "q4_0": 18 / 32}
# llama.cpp keeps the token-embedding table (151,936 x 4,096) in system RAM, and with partial offload the output
# layer too. Bits per weight of those two tensors in each file:
EMBED_PARAMS = 151_936 * 4_096
EMBED_BITS = {"Q4_K_M": 4.5, "Q6_K": 6.5625, "Q8_0": 8.5, "BF16": 16.0}
OUTPUT_BITS = {"Q4_K_M": 6.5625, "Q6_K": 6.5625, "Q8_0": 8.5, "BF16": 16.0}
# compute buffer + CUDA context, fitted to llama.cpp measurements on an RTX PRO 4000 (SMALL-GPU.md): every
# one of 21 measured setups within 0.03 GiB; partial offload needs larger buffers for the CPU/GPU split
COMPUTE_BUFFER_GIB = 0.35
COMPUTE_BUFFER_PARTIAL_GIB = 0.76


def kv_cache_bytes(ctx, kv="f16"):
    """K and V for every layer, every KV head, every token of context."""
    return 2 * LAYERS * KV_HEADS * HEAD_DIM * ctx * KV_BYTES[kv]


def estimate(quant="Q4_K_M", ctx=8192, kv="f16", gpu_layers=LAYERS):
    """GiB of GPU memory with `gpu_layers` of the 36 layers on the GPU (the rest run on the CPU)."""
    n = max(0, min(gpu_layers, LAYERS))
    embed = EMBED_PARAMS * EMBED_BITS[quant] / 8
    output = EMBED_PARAMS * OUTPUT_BITS[quant] / 8
    layers = QUANTS[quant] - embed - output              # the 36 repeating blocks
    cache = kv_cache_bytes(ctx, kv)
    if n == LAYERS:
        return (layers + output + cache) / GIB + COMPUTE_BUFFER_GIB
    return (layers + cache) * n / LAYERS / GIB + COMPUTE_BUFFER_PARTIAL_GIB


def best_fit(vram_gib, headroom_gib=0.5):
    """The largest setup that fits, trying better quality first, then longer context."""
    budget = vram_gib - headroom_gib
    for quant in ("Q8_0", "Q6_K", "Q4_K_M"):
        for ctx in (16384, 8192, 4096):
            for kv in ("f16", "q8_0"):
                if estimate(quant, ctx, kv) <= budget:
                    return {"quant": quant, "ctx": ctx, "kv": kv, "gpu_layers": LAYERS, "gib": estimate(quant, ctx, kv)}
    for layers in range(LAYERS - 1, 0, -1):          # partial offload: some layers on the CPU
        if estimate("Q4_K_M", 4096, "q8_0", layers) <= budget:
            return {"quant": "Q4_K_M", "ctx": 4096, "kv": "q8_0", "gpu_layers": layers,
                    "gib": estimate("Q4_K_M", 4096, "q8_0", layers)}
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vram", type=float, help="your GPU's memory in GB: print the best setup that fits")
    ap.add_argument("--quant", choices=QUANTS)
    ap.add_argument("--ctx", type=int, default=8192)
    ap.add_argument("--kv", choices=KV_BYTES, default="f16")
    ap.add_argument("--gpu-layers", type=int, default=LAYERS)
    a = ap.parse_args()
    if a.vram:
        b = best_fit(a.vram)
        if not b:
            print(f"{a.vram:g} GB is too small for GPU offload; run on the CPU (-ngl 0) with Q4_K_M.")
            return
        flags = f"-ngl {b['gpu_layers'] if b['gpu_layers'] < LAYERS else 99} -c {b['ctx']}"
        flags += f" -fa on -ctk {b['kv']} -ctv {b['kv']}" if b["kv"] != "f16" else ""
        print(f"{a.vram:g} GB: {b['quant']}, context {b['ctx']}, KV cache {b['kv']}, "
              f"{b['gpu_layers']}/{LAYERS} layers on the GPU, ~{b['gib']:.1f} GiB\n  llama-server flags: {flags}")
        return
    if a.quant:
        print(f"~{estimate(a.quant, a.ctx, a.kv, a.gpu_layers):.1f} GiB")
        return
    print(f"{'quant':8} {'ctx':>6} {'KV f16':>8} {'KV q8_0':>8}   (GiB, all {LAYERS} layers on the GPU)")
    for q in ("Q4_K_M", "Q6_K", "Q8_0"):
        for ctx in (4096, 8192, 16384):
            print(f"{q:8} {ctx:>6} {estimate(q, ctx, 'f16'):>8.1f} {estimate(q, ctx, 'q8_0'):>8.1f}")


if __name__ == "__main__":
    main()

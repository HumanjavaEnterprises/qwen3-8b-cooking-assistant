# Serving with llama-server

Two tested command lines for [llama.cpp](https://github.com/ggml-org/llama.cpp)'s `llama-server`, one per GPU size.
The numbers below were measured with llama.cpp commit
[`08c252e2`](https://github.com/ggml-org/llama.cpp/commit/08c252e221759e0f69e80f0450b295c92d2344e1) (CUDA build) on one
NVIDIA RTX PRO 4000 Blackwell SFF (70 W), Q4_K_M, one user, thinking off. Flag names can change between llama.cpp
releases; check `llama-server --help` if one is rejected.

| Script | GPU memory | Context | Answer (tokens/s) | Notes |
|---|---|---|---|---|
| [`6gb.sh`](6gb.sh) | 5.84 GiB | 8,192 | 65.1 | default KV cache; fits a 6 GB card with nothing else on it. If the card also drives a display, add `-ctk q8_0 -ctv q8_0` (lossy, 5.3 GiB) or use `-c 4096` |
| [`8gb-draft.sh`](8gb-draft.sh) | 7.13 GiB | 8,192 | 68.7 | adds the Qwen3-0.6B draft model; prompts read about 20% slower |

Neither script turns thinking off by itself: put `"chat_template_kwargs": {"enable_thinking": false}` in each request (as
[`../examples/ask.sh`](../examples/ask.sh) does), or add `--reasoning-budget 0` to the command line.

## `-np 1`

One slot for one user. With the default (several slots sharing one cache), the cache of a finished long request
stays in place and later short answers decode slower for the rest of the session: 40.9 instead of 66.2 tokens/s after
a 32k-token prompt in one test. To serve four chats at once, use `-np 4` instead (same memory, about 180 tokens/s
in total for short chats).

## The draft model (8 GB cards)

`8gb-draft.sh` uses speculative decoding: the small upstream
[Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) (Apache-2.0, by the Qwen team; not part of this release)
guesses one token ahead and the cooking model checks it. The cooking model's output is kept; in greedy tests 4 of 10
answers differed, each where the top two words were close (probability gap 0.02 to 0.17). It reads prompts about 20% slower because the draft reads
them too.

Convert Qwen3-0.6B to a Q4_K_M GGUF yourself, as for the measured setup. (Qwen also publishes a Q8_0 GGUF,
[Qwen/Qwen3-0.6B-GGUF](https://huggingface.co/Qwen/Qwen3-0.6B-GGUF). A Q8_0 draft also works: about 0.2 GiB more,
and slower in one test.)

```bash
hf download Qwen/Qwen3-0.6B --local-dir Qwen3-0.6B
python llama.cpp/convert_hf_to_gguf.py Qwen3-0.6B --outtype f16 --outfile qwen3-0.6b-f16.gguf
llama-quantize qwen3-0.6b-f16.gguf qwen3-0.6b-Q4_K_M.gguf Q4_K_M
```

In one test run the Q8_0 draft was slower than the Q4_K_M one (68.2 vs 70.8 tokens/s in the same session).

## 32k context on 8 GB (lossy)

With the default cache, 32k needs about 9.3 GiB. Storing the KV cache in 8 bits fits 8 GiB (7.20 GiB, 63.2
tokens/s, one run). This is **lossy**: the cache is quantised, and its answer quality was not evaluated.

```bash
llama-server -m qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf --jinja -c 32768 -np 1 -ctk q8_0 -ctv q8_0 --port 8080
```

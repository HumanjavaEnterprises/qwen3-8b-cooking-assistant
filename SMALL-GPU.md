# Running Qwen3-8B Cooking Assistant on a small GPU

Step by step, from "I have a gaming laptop" to asking the model about a recipe. Every number here was measured
with llama.cpp. Your speeds will differ, but the memory figures carry over to any NVIDIA card.

## 1. Check what you have

- **NVIDIA:** run `nvidia-smi` and read the memory total, e.g. `8188MiB` is an 8 GB card.
- **Apple Silicon (M1–M4):** the GPU shares system memory. 16 GB of RAM runs Q4_K_M or Q6_K comfortably.
- **AMD or Intel GPU:** use a llama.cpp Vulkan build (or LM Studio, which bundles one). The memory figures are the same.
- **No GPU:** it runs on the CPU, slowly. Use Q4_K_M with 16 GB of RAM.

Your desktop, browser and other apps use some GPU memory too. Leave about 0.5 GB free. (Memory figures in this
guide are GiB, the unit `nvidia-smi` reports in MiB: an "8 GB" card shows about 8,000 MiB.)

## 2. Pick a file and settings

| Your GPU memory | File | Context | KV cache | Layers on GPU | Uses (measured) |
|---|---|---|---|---|---|
| 4 GB | Q4_K_M | 4,096 | q8_0 | 23 of 36 (`-ngl 23`) | ~3.5 GB |
| 6 GB | Q4_K_M | 8,192 | q8_0 | all (`-ngl 99`) | 5.3 GB (5.8 GB with the default f16 cache) |
| 8 GB | Q6_K | 8,192 | q8_0 | all | 6.8 GB |
| 10–12 GB | Q8_0 | 8,192 | f16 | all | 9.0 GB |
| 16 GB+ | Q8_0 | 16,384 | f16 | all | 10.1 GB |

Not sure? `python tools/vram_estimate.py --vram 6` prints the best fit and the exact flags for your card.

What the settings mean:
- **File (quantisation).** Smaller files hold the weights in fewer bits. On our checks, Q4_K_M, Q6_K and Q8_0 all
  match full precision within noise (see [EVALS.md](EVALS.md)). Use the biggest that fits.
- **Context** is how much text the model sees at once: system prompt + recipe + question + answer. A long recipe is
  about 1,000 tokens, so 4,096 is plenty for one recipe; 8,192 leaves room for a conversation.
- **KV cache** is the model's working memory for that context. `q8_0` halves it. It is lossy: answer quality with it was not evaluated. It needs
  flash attention (`-fa on`).
- **Layers on GPU.** The model has 36 layers. If they don't all fit, put some on the GPU and the rest run on the CPU.
  Slower, but it works.

### Measured: memory and speed

llama.cpp (build `ca8daad`, CUDA) on an NVIDIA RTX PRO 4000 (24 GB), one request, thinking off. "Memory" is what the
llama-server process used on the GPU.

| File | Context | KV cache | Memory | Prompt (tokens/s) | Answer (tokens/s) |
|---|---|---|---|---|---|
| Q4_K_M | 4,096 | f16 | 5.3 GB | 1,658 | 73 |
| Q4_K_M | 4,096 | q8_0 | 5.0 GB | 1,718 | 70 |
| Q4_K_M | 8,192 | f16 | 5.8 GB | 1,681 | 73 |
| Q4_K_M | 8,192 | q8_0 | 5.3 GB | 1,713 | 70 |
| Q4_K_M | 16,384 | q8_0 | 5.9 GB | 1,671 | 70 |
| Q6_K | 8,192 | f16 | 7.3 GB | 1,697 | 58 |
| Q6_K | 8,192 | q8_0 | 6.8 GB | 1,650 | 56 |
| Q6_K | 16,384 | q8_0 | 7.4 GB | 1,639 | 55 |
| Q8_0 | 8,192 | f16 | 9.0 GB | 1,948 | 46 |
| Q8_0 | 8,192 | q8_0 | 8.5 GB | 1,828 | 45 |
| Q8_0 | 16,384 | f16 | 10.1 GB | 1,947 | 46 |

Partial offload (Q4_K_M, context 4,096, q8_0 cache). The CPU here is a workstation Xeon; a laptop CPU is slower.

| Layers on GPU | Memory | Prompt (tokens/s) | Answer (tokens/s) |
|---|---|---|---|
| 24 of 36 | 3.5 GB | 417 | 37 |
| 16 of 36 | 2.6 GB | 303 | 30 |
| 8 of 36 | 1.7 GB | 225 | 25 |

For reading speed, 15 tokens/s is already faster than most people read.

### Measured again: speed on one card (2026-11-19)

Q4_K_M, 8,192-token context, default f16 KV cache, one user, thinking off, short chats, on one NVIDIA RTX PRO 4000
Blackwell SFF (24 GB, 70 W). [llama.cpp](https://github.com/ggml-org/llama.cpp) commit `08c252e2`; Ollama 0.40.16.
Command lines: [serving/](serving/). Method: the
[inference-optimisation skill](https://github.com/sybil-solutions/inference-optimisation-skill).

| Setup | GPU memory | Answer (tokens/s) | Prompt, ~1k / ~8k tokens (tokens/s) | First token | Start-up |
|---|---|---|---|---|---|
| Ollama | 5.96 GiB | 65.6 | 2,566 / 2,360 | 28.5 ms | 10.8 s |
| llama-server `-c 8192 -np 1` ([serving/6gb.sh](serving/6gb.sh)) | 5.84 GiB | 65.1 | 2,556 / 2,317 | 20.3 ms | 3.1 s |
| + Qwen3-0.6B draft model, 8 GB cards ([serving/8gb-draft.sh](serving/8gb-draft.sh)) | 7.13 GiB | 68.7 | 2,059 / 1,887 | 26.3 ms | 4.1 s |
| **Lossy:** 32,768 context, q8_0 KV cache, `-np 1` | 7.20 GiB | 63.2 (one run) | 31k tokens: 1,635 | 22.3 ms | 2.1 s |

- Ollama and llama-server answer at the same speed. llama-server starts faster and shows the first token sooner.
  Ollama's first start on a new install compiles GPU kernels (here 45 s to start plus 39 s for the first answer).
- The draft model makes answers about 4% to 9% faster (+3.8% to +9.3% over five paired runs; +5.6% in the final
  one) and reads prompts about 20% slower. It does not fit next to the
  8k setup on a 6 GB card.
- 32k with the default cache needs about 9.3 GiB. The 32k row stores the cache in 8 bits: lossy, and its answer
  quality was not evaluated.
- These rows come from a separate session with a newer llama.cpp. This card's speed moves with its temperature
  (64 to 71 tokens/s for one setup over a night), so compare rows within one table.

**Correction (2026-11-19):** the model card said Q4_K_M uses "5.3 GB at 8k context". That is the q8_0-cache figure
(the 6 GB row of step 2). With the default cache it uses 5.84 GiB (llama-server) / 5.96 GiB (Ollama). A 6 GB card
that also drives a display may not hold that fully: use a 4,096 context (about 5.3 GiB), the q8_0 cache (lossy,
5.3 GiB at 8k), or let Ollama put a few layers on the CPU.

**Other hardware (calculated, not measured).** Answer speed is limited by memory bandwidth: each token reads about
4.76 GB (Q4_K_M weights plus a short chat's KV cache). Ceiling = bandwidth ÷ 4.76 GB; estimate = 0.75 × ceiling, the
share reached on the card above.

| Hardware | Bandwidth (GB/s) | Ceiling (tokens/s) | Estimate (tokens/s) |
|---|---|---|---|
| RTX 3050 6GB | 168 | 35 | 26 |
| RTX 3060 12GB | 360 | 76 | 57 |
| RTX 4060 8GB | 272 | 57 | 43 |
| RTX 4060 Ti 8GB | 288 | 61 | 45 |
| RTX 5060 8GB | 448 | 94 | 71 |
| MacBook Air (M4) | 120 | 25 | 19 |
| MacBook Pro (M4 Pro) | 273 | 57 | 43 |

Desktop cards with a bigger power budget may do better than 0.75; laptop GPUs may do worse. Apple numbers use the
same fraction; llama.cpp's Metal backend was not measured.

## 3. Install a runtime

Pick one.

**Ollama** (easiest). Install from [ollama.com](https://ollama.com), then:

```bash
ollama run vveerrgg/qwen3-8b-cooking-assistant          # Q4_K_M, 6 GB cards
ollama run vveerrgg/qwen3-8b-cooking-assistant:q6_k     # 8 GB cards
ollama run vveerrgg/qwen3-8b-cooking-assistant:q8_0     # 10 GB and up
```

Or straight from Hugging Face: `ollama run hf.co/HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant-GGUF:Q4_K_M`.

Ollama picks how many layers fit by itself. The model repo carries the chat template, the trained system prompt and
the sampling settings, so this one line is all you need. (Tested with Ollama 0.12.6 and 0.40.16. Without that template
Ollama guesses a raw format and the model rambles: if you build it from the GGUF file yourself, use
[examples/Modelfile](examples/Modelfile), step 4.)

**Thinking in Ollama (note, 2026-11-19).** Some newer Ollama versions (seen on 0.40.16) use the chat template inside
the GGUF file instead of the one shipped with the model, and that template turns thinking on: answers start with a
paragraph of reasoning and run 3 to 5 times longer. The fix is one line, `PARSER passthrough`, in
[examples/Modelfile](examples/Modelfile) and in the library tags updated 2026-11-19 (`latest`, `q4_k_m`, `q6_k`,
`q8_0`; the pinned `v1` tags stay as first published): pull again or rebuild. With a pinned tag, an older pull or
the `hf.co/` path, turn thinking off per request: `"think": false` (Ollama API),
`"reasoning_effort": "none"` (OpenAI-compatible `/v1`), `ollama run ... --think=false`, or `/set nothink` in a chat.

**LM Studio** (point and click). Search for `HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant-GGUF` in the model browser,
download the file from step 2, set **GPU offload** and **context length** from the table, turn thinking off, and
paste the system prompt from step 5.

**llama.cpp** (most control; the commands below). Download a prebuilt release for your platform from
[github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases) (CUDA for NVIDIA, Vulkan for
AMD / Intel, macOS for Apple Silicon), or `brew install llama.cpp` on a Mac.

## 4. Download the file

```bash
pip install -U huggingface_hub
hf download HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant-GGUF qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf --local-dir .
```

Check it against `SHA256SUMS` in the model repo if you like: `sha256sum qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf`.

For Ollama with the trained system prompt:

```bash
cp examples/Modelfile .      # edit FROM if you picked another file
ollama create cooking -f Modelfile
ollama run cooking
```

The Modelfile sets the chat template (thinking off), the trained system prompt, the context length and the stop
tokens.

## 5. Start the server (llama.cpp)

6 GB card, everything on the GPU:

```bash
llama-server -m qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf \
  -ngl 99 -c 8192 -fa on -ctk q8_0 -ctv q8_0 \
  --reasoning-budget 0 --port 8080
```

4 GB card, part on the GPU:

```bash
llama-server -m qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf \
  -ngl 23 -c 4096 -fa on -ctk q8_0 -ctv q8_0 \
  --reasoning-budget 0 --port 8080
```

| Flag | What it does |
|---|---|
| `-ngl N` | layers on the GPU (`99` = all 36) |
| `-c N` | context length in tokens |
| `-fa on` | flash attention: less memory, and needed for the q8_0 cache |
| `-ctk q8_0 -ctv q8_0` | store the KV cache in 8 bits (about half the memory) |
| `--reasoning-budget 0` | thinking off. The model was trained to answer directly; thinking only adds delay |

Open `http://127.0.0.1:8080` for a chat page, or use the API.

**The system prompt.** The model was trained with this one and works best with it:

```
You are a cooking assistant. You answer questions about dishes, ingredients, techniques and food safety. When you are not sure, you say so.
```

## 6. Try it

```bash
examples/ask.sh
```

Expected: `You would need 900 ml of milk.` (it reads the recipe in the prompt and triples 300 ml).

Now ask without the recipe:

```bash
examples/ask.sh "" "If I triple my pancake recipe, how much milk do I need?"
```

It should ask you for the original amount instead of inventing one. That is the behaviour this model was built for.
From Python: [examples/chat.py](examples/chat.py) (works with llama-server, Ollama, LM Studio or vLLM).

## 7. Using it well

- **Give it the recipe.** Put the recipe text in the same message as the question. It answers from that text; it
  was not trained to recall recipes from memory.
- **Let your app do the maths.** Scaling and unit conversion are best calculated by code; the model is good at
  reading the recipe and explaining.
- **Not a food-safety authority.** It repeats standard guidance but can be wrong. Check official sources for
  temperatures and storage.

## Troubleshooting

| Problem | Fix |
|---|---|
| `out of memory` / `failed to allocate` | Lower `-c`, add `-ctk q8_0 -ctv q8_0 -fa on`, use a smaller file, or lower `-ngl` |
| Very slow answers | Some layers are on the CPU. Raise `-ngl` as far as memory allows, or use a smaller file so all layers fit |
| Answers start with `<think>` or "Okay, the user wants…" | Thinking is on. Add `--reasoning-budget 0` (llama.cpp) or send `"chat_template_kwargs": {"enable_thinking": false}`; in Ollama, pull the tags again or rebuild with [examples/Modelfile](examples/Modelfile), or send `"think": false` (step 3) |
| Ollama answer never ends, or asks itself questions | Ollama is using a raw template. Pull from `hf.co/...` (step 3) or build with [examples/Modelfile](examples/Modelfile) |
| It invents quantities | It has no recipe to read. Paste the recipe into the message |
| Strange characters or loops | Use the trained system prompt; keep temperature around 0.7 |
| Memory still too tight | Close the browser (it uses GPU memory), or run on the CPU with `-ngl 0` |

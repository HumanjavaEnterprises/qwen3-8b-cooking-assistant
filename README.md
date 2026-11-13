# Qwen3-8B Cooking Assistant

A multilingual cooking assistant you can run on your own machine, down to a 4 GB GPU. Fine-tuned from Qwen3-8B on
public-domain and openly licensed cookbooks.

It answers from the recipe you give it, asks for the recipe when an answer depends on one it cannot see, and gives
full answers to general cooking questions. On questions it could not answer without a recipe, base Qwen3-8B invented
recipe details 25.8% of the time; this model does it 2.7% of the time. Given the recipe, it reads it correctly 94.8% of
the time (base: 83.1%). Four open-weights judges, see [EVALS.md](EVALS.md).

*Unofficial fine-tune of Qwen3-8B by Humanjava Enterprises; not made or endorsed by Alibaba Cloud or the Qwen team.*

| | |
|---|---|
| **Run it on a small GPU** | [SMALL-GPU.md](SMALL-GPU.md): pick a file for your card, install, start, test, troubleshoot |
| **GGUF** (llama.cpp, Ollama, LM Studio) | [HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant-GGUF](https://huggingface.co/HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant-GGUF) |
| **Full precision** (Transformers, vLLM) | [HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant](https://huggingface.co/HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant) |
| **Evaluation set** (every question, answer and judge verdict behind the numbers) | [HumanjavaEnterprises/cooking-assistant-eval](https://huggingface.co/datasets/HumanjavaEnterprises/cooking-assistant-eval) |
| **Results** | [EVALS.md](EVALS.md) |
| **Help refine it** | [Label five answers](https://label-test.humanjava.com/?s=cook4&k=cook-9ac741a1e387&src=github-guide): blind, no account, a few minutes |

## Quick start

With [Ollama](https://ollama.com):

```bash
ollama run vveerrgg/qwen3-8b-cooking-assistant
```

With llama.cpp on a 6 GB GPU:

```bash
pip install -U huggingface_hub
hf download HumanjavaEnterprises/Qwen3-8B-Cooking-Assistant-GGUF qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf --local-dir .
llama-server -m qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf -ngl 99 -c 8192 -fa on -ctk q8_0 -ctv q8_0 --reasoning-budget 0 --port 8080
examples/ask.sh          # -> "You would need 900 ml of milk."
```

Other card sizes: `python tools/vram_estimate.py --vram 4` (or 8, 12, ...) prints the setup that fits and the flags.

## Which file?

| GPU memory | File | Measured memory use |
|---|---|---|
| 4 GB | `Q4_K_M`, 23 of 36 layers on the GPU | ~3.5 GB |
| 6 GB | `Q4_K_M`, context 8,192 | 5.3 GB |
| 8 GB | `Q6_K`, context 8,192 | 6.8 GB |
| 10 GB and up | `Q8_0` | 9.0 GB |

All three match full precision within noise on our checks. Details and speeds: [SMALL-GPU.md](SMALL-GPU.md).

## How to use it

Thinking off, and this system prompt (the one it was trained with):

```
You are a cooking assistant. You answer questions about dishes, ingredients, techniques and food safety. When you are not sure, you say so.
```

Put the recipe in the same message as the question. Without a recipe it asks for one instead of guessing. The design
idea: **the fine-tune for behaviour, your app for facts** (look up the recipe and pass it in) **and code for
numbers** (scaling, unit conversion).

## In this repo

| Path | What |
|---|---|
| [SMALL-GPU.md](SMALL-GPU.md) | the full process for a small-GPU machine, with measured memory and speed |
| [EVALS.md](EVALS.md) | how the model was checked, and the results |
| [examples/](examples/) | `ask.sh` (curl), `chat.py` (Python, any OpenAI-compatible server), an Ollama `Modelfile` |
| [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) | report a wrong answer, a bug or a security issue |
| [tools/vram_estimate.py](tools/vram_estimate.py) | memory planner, fitted to measurements (within 0.03 GiB on 21 setups); `python -m pytest tests` |

## Licence and credits

Code and docs in this repo: MIT. Model weights: Apache-2.0, same as the base model. Evaluation set text: CC BY-SA 4.0
(per-row attribution in the dataset).

Base model: [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) by the Qwen team (Apache-2.0). Runtime used for every
number here: [llama.cpp](https://github.com/ggml-org/llama.cpp) (MIT). Cookbook sources: Wikibooks Cookbook
contributors (CC BY-SA 4.0), Project Gutenberg and Internet Archive public-domain books, NHLBI (US government).

Built by [Humanjava Enterprises](https://humanjava.com).

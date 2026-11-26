# Olmo-3-7B Cooking Assistant (v2)

The Cooking Assistant on Ai2's fully open **OLMo 3 7B**, with an auditable lineage: every model that wrote, judged or
labelled anything in its training and evaluation is an open-weights model from a US lab (gpt-oss-120b by OpenAI,
Granite 4.2 by IBM, OLMo by Ai2), and the base model's training data is public. Added to the family on 2026-11-26 as
part of v2 (the family's v1 was the Qwen3-8B and GLM-4-9B builds).

*Unofficial fine-tune of OLMo 3 7B by Humanjava Enterprises; not made or endorsed by Ai2.*

| | |
|---|---|
| **GGUF** (llama.cpp, Ollama, LM Studio) | [HumanjavaEnterprises/Olmo-3-7B-Cooking-Assistant-GGUF](https://huggingface.co/HumanjavaEnterprises/Olmo-3-7B-Cooking-Assistant-GGUF) |
| **Full precision + LoRA adapter** (Transformers, vLLM) | [HumanjavaEnterprises/Olmo-3-7B-Cooking-Assistant](https://huggingface.co/HumanjavaEnterprises/Olmo-3-7B-Cooking-Assistant) |
| **Evaluation set** (config `olmo-3-7b-v2`) | [HumanjavaEnterprises/cooking-assistant-eval](https://huggingface.co/datasets/HumanjavaEnterprises/cooking-assistant-eval) |
| **Results** | [EVALS.md](EVALS.md) |

## Quick start

```bash
# Ollama, straight from Hugging Face (template, system prompt and settings ship in the HF repo)
ollama run hf.co/HumanjavaEnterprises/Olmo-3-7B-Cooking-Assistant-GGUF:Q4_K_M

# llama.cpp on a 6 GB GPU
hf download HumanjavaEnterprises/Olmo-3-7B-Cooking-Assistant-GGUF olmo-3-7b-cooking-assistant-v2-Q4_K_M.gguf --local-dir .
llama-server -m olmo-3-7b-cooking-assistant-v2-Q4_K_M.gguf --jinja -ngl 99 -c 8192 --port 8080
examples/ask.sh          # -> "You would need 900 ml of milk."
```

| GPU memory | File |
|---|---|
| 6 GB | `Q4_K_M` (4.5 GB) |
| 8 GB | `Q6_K` (6.0 GB) |
| 10 GB and up | `Q8_0` (7.8 GB) |

## When to pick this one

Pick it for **English** use when you want the lineage above, or strong recipe scaling (arithmetic 33/40 on our
probe vs 25/40 for the Qwen build; odd egg counts 12/13). Pick the [Qwen3-8B build](../README.md) for other
languages and general cooking questions: the OLMo base is English-only, and this model is clearly behind there (see
[EVALS.md](EVALS.md)). It is also under-cautious about heat when doubling chilli-heavy dishes.

## How to use it

No thinking mode. This system prompt (the one it was trained with):

```
You are a cooking assistant. You answer questions about dishes, ingredients, techniques and food safety. When you are not sure, you say so.
```

Put the recipe in the same message as the question. Without a recipe it usually asks for one.

## Licence and credits

Code and docs: MIT (repo `LICENSE`). Model weights: Apache-2.0, same as the base model. Base model:
[OLMo 3 7B](https://huggingface.co/allenai/Olmo-3-1025-7B) by Ai2 (Apache-2.0; Ai2's Responsible Use Guidelines).
Writer gpt-oss-120b (OpenAI), judge Granite 4.2 30B (IBM), fact check OLMo 3.1 32B Instruct (Ai2), all Apache-2.0.
Cookbook sources: Wikibooks Cookbook contributors (CC BY-SA 4.0), Project Gutenberg and Internet Archive
public-domain books, NHLBI (US government). Runtime: llama.cpp (MIT).

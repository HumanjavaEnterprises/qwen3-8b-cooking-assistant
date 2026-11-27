# EuroLLM-9B Cooking Assistant (v2)

The Cooking Assistant on **EuroLLM-9B-Instruct**, with an auditable lineage: every model that wrote, labelled,
filtered or voted on anything in its training and evaluation is an open-weights model from a European lab (EuroLLM by
the UTTER consortium, Apertus by the Swiss AI Initiative, Mistral-Small and Magistral-Small by Mistral AI), and an
independent panel from outside that chain cross-checks the numbers. Added to the family on 2026-11-26 as part of v2
(the family's v1 was the Qwen3-8B and GLM-4-9B builds).

> **Human review: pending.** No person has reviewed the training labels yet. A 100-item review is planned (50 accepted training answers and 50 preference pairs, read blind by people); its results will be added to this card.

*Unofficial fine-tune of EuroLLM-9B-Instruct by Humanjava Enterprises; not made or endorsed by the EuroLLM project or
the UTTER consortium.*

| | |
|---|---|
| **GGUF** (llama.cpp, Ollama, LM Studio) | [HumanjavaEnterprises/EuroLLM-9B-Cooking-Assistant-GGUF](https://huggingface.co/HumanjavaEnterprises/EuroLLM-9B-Cooking-Assistant-GGUF) |
| **Full precision** (Transformers, vLLM) | [HumanjavaEnterprises/EuroLLM-9B-Cooking-Assistant](https://huggingface.co/HumanjavaEnterprises/EuroLLM-9B-Cooking-Assistant) |
| **Ollama** | [Ollama](https://ollama.com/vveerrgg/eurollm-9b-cooking-assistant): `ollama run vveerrgg/eurollm-9b-cooking-assistant:q6_k` |
| **Evaluation set** (config `eurollm-9b-v2`) | [HumanjavaEnterprises/cooking-assistant-eval](https://huggingface.co/datasets/HumanjavaEnterprises/cooking-assistant-eval) |
| **Results** | [EVALS.md](EVALS.md) |

## Quick start

```bash
# Ollama, straight from Hugging Face (template, system prompt and settings ship in the HF repo)
ollama run hf.co/HumanjavaEnterprises/EuroLLM-9B-Cooking-Assistant-GGUF:Q4_K_M

# llama.cpp on an 8 GB GPU
hf download HumanjavaEnterprises/EuroLLM-9B-Cooking-Assistant-GGUF eurollm-9b-cooking-assistant-v2-Q4_K_M.gguf --local-dir .
llama-server -m eurollm-9b-cooking-assistant-v2-Q4_K_M.gguf --jinja -ngl 99 -c 8192 --port 8080
examples/ask.sh          # -> "Use 900 ml of milk (300 ml x 3)."
```

| GPU memory | File |
|---|---|
| 8 GB | `Q4_K_M` (5.6 GB) |
| 10 GB | `Q6_K` (7.5 GB) |
| 12 GB and up | `Q8_0` (9.7 GB) |

## When to pick this one

Pick it when you want the European lineage above, recipe scaling with the cautions that go with it (arithmetic 38/40
on our probe, tied with the Qwen build; "season to taste" 15/19 and pan-size / time 33/37, where the Qwen build gets
3/19 and 1/37), or answers in the European languages EuroLLM was trained on. Pick the [Qwen3-8B build](../README.md)
for general cooking questions: this model is **below its own base model** there (54.9% vs 64.6%), and it still
invents details on 11.4% of questions that need a recipe it was not shown. See [EVALS.md](EVALS.md).

## How to use it

No thinking mode. This system prompt (the one it was trained with):

```
You are a cooking assistant. You answer questions about dishes, ingredients, techniques and food safety. When you are not sure, you say so.
```

With no system prompt, the embedded template adds a version that also names the model ("You are the Cooking
Assistant by Humanjava Enterprises, fine-tuned from EuroLLM-9B. ..."); the Ollama files use that one. Put the recipe in the
same message as the question. Without a recipe it usually asks for it, or answers with a clearly hypothetical amount.

## Licence and credits

Code and docs: MIT (repo `LICENSE`). Model weights: Apache-2.0, same as the base model. Base model:
[EuroLLM-9B-Instruct-2512](https://huggingface.co/utter-project/EuroLLM-9B-Instruct-2512) by the UTTER consortium
(Apache-2.0). Writer and labeller EuroLLM-22B-Instruct-2512 (UTTER); filters Apertus-v1.5-70B (Swiss AI Initiative,
Apache-2.0 + Apertus Acceptable Use Policy; used to judge, not redistributed) and Mistral-Small-3.2-24B (Mistral AI);
evaluation judges Apertus-v1.5-70B, Mistral-Small-3.2-24B, Magistral-Small-2509, with ALIA-40B (BSC) reported but not
voting; all Apache-2.0. Cookbook sources: Wikibooks Cookbook contributors (CC BY-SA 4.0), Project Gutenberg and Internet
Archive public-domain books, NHLBI (US government). Runtime: llama.cpp (MIT).

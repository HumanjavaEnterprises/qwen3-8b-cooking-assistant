# Olmo-3-7B Cooking Assistant v2: evaluation

Every number below comes from the published evaluation set,
[HumanjavaEnterprises/cooking-assistant-eval](https://huggingface.co/datasets/HumanjavaEnterprises/cooking-assistant-eval)
config `olmo-3-7b-v2` (all 682 questions, all answers, every judge verdict), except the scaling probe.

## Panel

Three open-weights judges from US labs, run locally, blind to which model wrote each answer: gpt-oss-120b (OpenAI),
Granite 4.2 30B (IBM), OLMo 3.1 32B Instruct (Ai2). A verdict counts when 2 of 3 agree. A code check removes
"invents" verdicts on answers whose every detail was already in the question. The Qwen3-8B Cooking Assistant v1
column was re-scored by this same panel (answers generated again from its published weights), so its numbers here
differ from its own card, which used a different panel.

## 682-question set (21 languages; 164 English)

| | OLMo 3 7B base | **v2** | Qwen3-8B Cooking Assistant v1 |
|---|---|---|---|
| Invents, no recipe (all / English) | 49.3% / 52.2% | **21.1% / 4.4%** | 6.8% / 2.9% |
| Correct, recipe shown (all / English) | 52.0% / 70.4% | **80.3% / 91.5%** | 92.0% / 91.7% |
| General questions (all 82 / English 20) | 17.1% / 55% | **22.0% / 65%** | 48.8% / 65% |

"Recipe shown" includes the 10 recall questions. The base is the pretrained OLMo 3 7B with our chat template (no
instruction tuning).

## Recipe scaling probe (40 held-out items)

| | v2 | Qwen3-8B Cooking Assistant v1 |
|---|---|---|
| Arithmetic right | 33/40 | 25/40 |
| Odd egg counts | 12/13 | 3/13 |
| ⅓-cup lines | 8/8 | 2/8 |
| Wrong unit equivalents (answers) | 2 | 1 |
| Heat caution when doubling chilli/spice | 4/15 | 0/15 |

Noise: the same weights after a bf16 merge round-trip moved probe columns by up to 3 (spice 4 → 7/15), so read
differences of about ±3 there as noise.

## Quantised files

All three files were scored on the same 682 questions against the full-precision model, by the same three judges in the same run (2 of 3). Invents with no recipe: Q4_K_M 19.5% (full precision 20.6%), Q6_K 19.9% (20.2%), Q8_0 21.1% (22.1%). Correct with the recipe shown: 79.9% (79.9%), 79.5% (79.9%), 80.1% (79.8%). General questions: 19.5% (25.6%), 25.6% (25.6%), 23.2% (22.0%). No difference is significant (McNemar p ≥ 0.27). The full-precision answers are the same text in every comparison; only the judging was re-run (the Granite judge samples), which alone moves their scores by up to 1.9 points.

## Memorisation

Cookbook training documents (Wikibooks Cookbook, CC BY-SA) were probed with 12,000 prefixes of 32 to 128 tokens at several offsets, as raw text and as chat prompts, with greedy decoding. The model never continues a document verbatim (no 50-token match; longest overlap 16 characters, vs 84 for the OLMo 3 7B base), and its overlap with the true text is far below the base's (ROUGE-L 0.022 vs 0.138).

## Limits

Under-cautious on heat when doubling chilli and spice (≤ 7/15 on the probe); English-only base, so weaker in other
languages; behind the Qwen build on general questions overall; probe noise of about ±3.

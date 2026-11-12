# How Qwen3-8B Cooking v8 was checked

Everything is on a fixed held-out set of 682 questions in 26 languages that were never used in training: 300 with the
recipe shown, 300 that need a recipe the model is not shown, and 82 general cooking questions. Each answer from base
Qwen3-8B and from this model (both with thinking off) was judged blind. The full write-up, with confidence intervals
and caveats, is on the [model card](https://huggingface.co/HumanjavaEnterprises/Qwen3-8B-Cooking-v8).

## Does it invent recipe details?

Four open-weights judges from four model families scored every answer on its own: DeepSeek-V4-Flash (MIT),
Qwen3.8-27B (Apache-2.0), GLM-4.7-Flash (MIT) and gpt-oss-120b (Apache-2.0). Share of no-recipe questions where the
answer invents recipe details:

| counted as "invents" when | Qwen3-8B | this model |
|---|---|---|
| at least 3 of 4 judges agree | 25.8% [21.1, 31.0] | **2.7%** [1.4, 5.2] |
| all four agree | 19.1% | 1.0% |
| any one judge says so | 49.2% | 18.3% |

And when the recipe **is** shown (290 questions, 3 of 4 judges agree): Qwen3-8B reads it correctly 83.1%
[78.4, 87.0] of the time, this model **94.8%** [91.6, 96.8] (McNemar p < 1e-6).

3 of 4: 72 questions where only the base invents, 3 where only this model does (McNemar p < 1e-17). Caveats: the
judges are models, and model judges tend to share mistakes, so four agreeing is less than four independent checks.
Qwen3.8-27B also labelled part of this model's training data.

**We are still refining the numbers with people.** Label Test is our blind labelling tool: you see five answers, one at
a time, and decide whether each made recipe details up, asked for the recipe, or gave honest general help. No
account; we keep only a name or initials and your labels. [Label five answers](https://label-test.humanjava.com/?s=cook4&k=cook-9ac741a1e387).

## Do the small files lose quality?

Same questions, same four judges, each quantised file against full precision:

| | Q4_K_M | Q6_K | Q8_0 |
|---|---|---|---|
| Invents with no recipe, 3 of 4 judges (full precision) | 4.7% (3.3%) | 3.0% (3.3%) | 3.3% (2.7%) |
| Correct when the recipe is shown (full precision) | 95.5% (94.1%) | 95.5% (94.1%) | 95.2% (94.8%) |
| Difference significant? (McNemar, inventing) | no, p = 0.34 | no, p = 1.0 | no, p = 0.69 |

On Q4_K_M, two judges on their own see slightly more invented details (p = 0.02 and 0.04); pick Q6_K or Q8_0 if that
matters to you.

## Does it copy its training text?

1,000 CC BY-SA training documents probed 12,000 ways (prefixes of 32 to 128 tokens, raw and chat prompts, greedy
decoding): no verbatim continuation (no 50-token match; longest overlap 67 characters vs the base model's 52), and no
more overlap with the true text than base Qwen3-8B (ROUGE-L 0.169 vs 0.177).

## General ability

lm-evaluation-harness 0.4.13, thinking off:

| | IFEval | GSM8K | TruthfulQA mc2 | MMLU-Pro | MGSM (8 lang) | Belebele (21 lang) |
|---|---|---|---|---|---|---|
| Qwen3-8B | 0.817 | 0.807 | 0.532 | 0.611 | 0.341 | 0.846 |
| this model | 0.800 | 0.866 | 0.542 | 0.591 | 0.401 | 0.863 |

MMLU-Pro is 2.0 points down, the largest loss. MMLU-Pro used 100 questions per subject (about ±1.3 points of noise).

# EuroLLM-9B Cooking Assistant v2: evaluation

Every number below comes from the published evaluation set,
[HumanjavaEnterprises/cooking-assistant-eval](https://huggingface.co/datasets/HumanjavaEnterprises/cooking-assistant-eval)
config `eurollm-9b-v2` (all 682 questions, both models' answers, every judge verdict), except the scaling probe.

## Panels

- **European voting panel:** Apertus-v1.5-70B (Swiss AI Initiative), Mistral-Small-3.2-24B and Magistral-Small-2509
  (Mistral AI), run locally, blind to which model wrote each answer; a verdict counts when 2 of 3 agree. ALIA-40B (BSC)
  is reported but does not vote (it was far more lenient on invented details when vetted).
- **Independent cross-check ("run A"):** DeepSeek-V4-Flash, gpt-oss-120b, Seed-OSS-36B, from outside the European
  chain. Apertus and Mistral-Small also filtered this model's synthetic training data, so this panel is the
  independent check.

A code check removes "invents" verdicts on answers whose every detail was already in the question.

## 682-question set (21 languages; 72 English no-recipe, 68 English recipe-shown)

| | EuroLLM-9B-Instruct (base) | **v2** |
|---|---|---|
| Invents, no recipe (European vote / run A) | 43.7% / 49.5% | **11.4% / 14.3%** |
| Correct, recipe shown (European vote / run A) | 80.3% / 73.4% | **83.8% / 83.8%** |
| General questions, 82 (European vote / run A) | **64.6% / 56.1%** | 54.9% / 46.3% |
| Invents / correct, English (European vote) | 30.6% / 85.3% | **5.6%** / 82.4% |
| ALIA-40B, non-voting (invents / general) | 20.7% / 73.2% | 6.0% / 68.3% |

"Recipe shown" excludes the 10 recall questions. **General answers are below the base on both panels**: the base is
the instruction-tuned EuroLLM-9B itself, and the preference stage that cut invented details cost about 5 points there.

## Recipe scaling probe (40 held-out items)

| | base | v2 | Qwen3-8B Cooking Assistant v1 |
|---|---|---|---|
| Arithmetic right (our rule) | 27/40 | **38/40** | 38/40 |
| Arithmetic right (the Olmo build's stricter rule) | 7/40 | **16/40** | 16/40 |
| Wrong unit conversions (answers / count) | 4 / 12 | 3 / 6 | 5 / 7 |
| Odd egg counts | 7/10 | 5/10 | 3/10 |
| "Season to taste" caution | 7/19 | 15/19 | 3/19 |
| Pan size / time caution | 11/37 | 33/37 | 1/37 |

The stricter rule only reads US volume units, so 22 of the 40 items cannot be checked by it and count as fails.
Noise: read differences of about ±3 on this probe as noise.

## Quantised files

All three files were scored on the same 682 questions against the full-precision model, by the European voting judges in the same run (2 of 3). Invents with no recipe: Q4_K_M 8.1% (full precision 11.8%), Q6_K 9.1% (11.8%), Q8_0 10.7% (11.4%). Correct with the recipe shown: 80.0% (84.1%), 81.4% (83.8%), 81.0% (83.8%). General questions: 50.0% (54.9%), 51.2% (56.1%), 53.7% (54.9%). No difference is significant (McNemar p ≥ 0.11), but every file reads a shown recipe 2 to 4 points less often than full precision, most at Q4_K_M; pick Q6_K or Q8_0 if you have the memory. The full-precision answers are the same text in every comparison; only the judging was re-run (Magistral samples).

## Memorisation

Cookbook training documents (Wikibooks Cookbook, CC BY-SA) were probed with 12,000 prefixes of 32 to 128 tokens at several offsets, as raw text and as chat prompts, with greedy decoding. The model reproduces training text no more than EuroLLM-9B-Instruct itself: one 50-token verbatim continuation for each (the same count), no overlap of 200 characters or more, longest overlap 63 characters for both, and overlap with the true text slightly below the base's (ROUGE-L 0.152 vs 0.157).

## Human review

Pending. No person has reviewed the training labels yet. A 100-item review is planned (50 accepted training answers and 50 preference pairs, read blind by people); its results will be added to this card.

## Limits

General answers below the base model; invented details on 11.4% / 14.3% of no-recipe questions; Bengali and Vietnamese
repetition loops (several eval languages are outside EuroLLM's 35); probe noise of about ±3.

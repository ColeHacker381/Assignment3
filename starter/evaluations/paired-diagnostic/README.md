# Paired challenge diagnostic

This self-authored set probes whether changing one choice to “None of the above” changes the model's answer. The standard and challenge versions use the same ten stems and original option order. In D01–D04, D09 and D10 the correct substantive option was replaced, so None is correct. In D05–D08 a distractor was replaced. None appears in all four positions. Six of ten correct None answers intentionally oversample that case relative to the assignment's approximate one-quarter rate.

The correct original choices are 7, 12, opposite direction, 1, 1/2, 4, 5, σ₂u₂, final evaluation after model selection, and j > i, respectively. The keys record the corresponding option numbers. The diagnostic mixes elementary arithmetic and course concepts and is not an official exam sample. It was written after the other practice sets and prompt experiments were examined.

One local run per condition used the pinned runtime, model and assignment generation settings. The standard run used the standard baseline prompt. The challenge runs used the current derive-first prompt and an experimental prompt with short course checks. The latter was written for the concepts represented here, so its targeted-set result is especially vulnerable to overlap. Results and per-question predictions are in `results.json`.

| Prompt and batch | Correct | Correct None | False None | Qwen prompt tokens |
| --- | ---: | ---: | ---: | ---: |
| Standard baseline, paired standard | 8/10 | — | — | 25 |
| Current challenge, paired challenge | 7/10 | 4/6 | 1/4 | 74 |
| Course checks, paired challenge | 9/10 | 5/6 | 0/4 | 155 |
| Course checks, released challenge | 2/10 | 1/3 | 3/7 | 155 |
| Course checks, earlier supplemental challenge | 4/10 | 0/3 | 1/7 | 155 |

The current prompt previously scored 7/10 released and 6/10 on the earlier supplemental challenge batch. The course-check candidate selected option 1 for every released question. Its targeted-set improvement did not carry over to those batches, so it remains an experiment. On the paired set, the current prompt got D02, D03, D04 and D09 right when None replaced the original correct choice, while it missed D01 and D10. The standard and challenge prompts and batches differ, and the model gives no reasoning under this profile. These observations cannot identify its internal cause of error. Batch composition and repeated experimentation also limit generalization.

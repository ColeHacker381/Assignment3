# Compact course-reference challenge experiment

The candidate retains the current derive-first instructions and adds a short set of course checks. The checks were selected after seeing the practice sets and overlap directly with their questions. Each batch was run once with the pinned model, runtime and generation settings. Detailed predictions are in `results.json`.

| Prompt | Qwen tokens | Released | Supplemental | Paired | Correct None cases | False None selections |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Current | 74 | 7/10 | 6/10 | 7/10 | 4/12 | 2/18 |
| Compact reference | 191 | 7/10 | 6/10 | 8/10 | 4/12 | 1/18 |

The candidate gave the same answers as the current prompt on the released and supplemental batches. Its paired-set gain came from D07, where a substantive answer was correct and the added reference gives the receptive-field rule directly. It selected None correctly in 4/6 paired cases and 0/6 across the other two batches, matching the current prompt. False None selections were one on supplemental for both prompts, plus one on paired for the current prompt.

The batches are small, have been used repeatedly in development, and are not representative hidden data. The paired batch deliberately has six correct None answers. The direct overlap between reference and diagnostic makes the one-point gain particularly weak evidence of general improvement. The current challenge prompt is retained pending broader evaluation.

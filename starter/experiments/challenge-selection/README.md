# Challenge prompt comparisons

Both drafts use the assignment's pinned model, runtime and generation settings. The supplemental batch is self-authored after viewing the released examples and is not a blinded holdout. Each result is one deterministic local run. The baseline measurements come from the earlier practice runs.

| Prompt | Qwen tokens | Released challenge | Supplemental challenge | Correct None cases, released + supplemental |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 39 | 6/10 | 6/10 | 0/6 |
| Derive first | 74 | 7/10 | 6/10 | 0/6 |
| Contrast example | 128 | 7/10 | 6/10 | 0/6 |

`results.json` records predictions for the two new candidates. The earlier baseline predictions are in `../../evaluations/course-review/results.json` for the supplemental set and the baseline brief for the released score. The released baseline predictions were Q01=2, Q02=4, Q03=1, Q04=2, Q05=2, Q06=4, Q07=3, Q08=2, Q09=3, Q10=3. In both batches, correct None cases were Q02, Q06 and Q09, and C02, C04 and C07 respectively.

The derive-first prompt is the provisional challenge candidate because it matches the example-based candidate's scores with fewer tokens. Its one-point improvement on the released set is weak evidence and is not an estimate of hidden performance. Neither candidate improved correct None selections in these tests. Further evaluation is needed.

# None-of-the-above example experiment

These candidates add arithmetic examples to illustrate when a missing answer makes None correct and when a substantive choice remains correct. `balanced.txt` includes None in two different positions. `strict-match.txt` emphasizes exact matching. Both were run once per challenge batch using the pinned local model, runtime and assignment generation settings.

| Prompt | Qwen tokens | Released | Supplemental | Correct None answers | Incorrect None selections |
| --- | ---: | ---: | ---: | ---: | ---: |
| Current derive-first | 74 | 7/10 | 6/10 | 0/6 | 1/14 |
| Balanced examples | 214 | 7/10 | 6/10 | 0/6 | 0/14 |
| Strict match | 155 | 6/10 | 6/10 | 0/6 | 0/14 |

Counts aggregate the three correct None cases and seven substantive-answer cases in each batch. The current derive-first prompt's false None selection occurred on supplemental question C06. Predictions for the new runs appear in `results.json` and earlier derive-first predictions are in `../challenge-selection/results.json`.

These development sets are small and have been used repeatedly for prompt selection. The supplemental set is self-authored after viewing the released material. The results do not establish the reason the model misses None cases, nor predict hidden-set accuracy. The current challenge prompt is retained because neither new prompt improved the observed None cases or total score across the batches.

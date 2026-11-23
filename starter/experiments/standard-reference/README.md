# Standard prompt course-reference comparison

The candidate appends the compact checks from the challenge prompt to the existing standard baseline instructions. Each batch was run once with the pinned local model, runtime and assignment profile. Per-question candidate predictions are in `results.json`. Baseline results and predictions are recorded in the earlier practice and evaluation artifacts.

| Standard prompt | Qwen tokens | Released | Course review | Paired | Broader topics |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 25 | 7/10 | 9/10 | 8/10 | 10/10 |
| Compact reference | 144 | 8/10 | 9/10 | 9/10 | 10/10 |

The candidate corrected the released attention-mask question. On course review it corrected the receptive-field question and missed the convexity question that the baseline answered correctly. Its paired gain was the receptive-field question. The added reference explicitly covers both attention masking and receptive-field width.

The candidate is selected provisionally because its score matched or exceeded the baseline on these batches. The reference was selected after the practice questions were observed. The diagnostic sets were self-authored after earlier testing, and the paired set overlaps directly with the reference. The results do not establish hidden-exam performance.

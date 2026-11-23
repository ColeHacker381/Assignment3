# Approach

The standard prompt asks the model to select the best option and return the required JSON. The challenge prompt asks it to determine the answer, compare the substantive choices, and select None of the above when the answer is absent. It adds compact checks for linear algebra, PCA, convexity, attention, convolution, sampling and backpropagation. The standard and challenge prompts measure 25 and 191 Qwen tokens, respectively.

I used the course's dynamic materials through November 11, the instructor's released standard and challenge batches and keys, and self-authored course-based diagnostic questions. The course inventory and diagnostic materials are included in the development workspace. The local runs used the supplied pinned Qwen3.5-4B Q4_K_M model, runtime and generation profile. Each score below is a single run on a ten-question batch. Outputs satisfied the runner's JSON validation.

| Prompt | Released | Course-review diagnostic | Paired diagnostic | Broader-topic diagnostic |
| --- | ---: | ---: | ---: | ---: |
| Standard | 7/10 | 9/10 | 8/10 | 10/10 |
| Challenge, compact reference | 7/10 | 6/10 | 8/10 | 8/10 |

The paired challenge set intentionally contains six correct None answers, while the other challenge sets each contain three. On the broader-topic set the challenge prompt got one of three correct None cases and had no false None selections. An earlier 74-token challenge prompt scored 7/10 on that same set, with one correct None and one false None selection. The compact reference matched or exceeded that prompt on the four development batches and is the provisional choice. Its paired-set gain was on a question directly covered by its reference.

These are measured development results, not hidden-set scores or estimates of final grades. The released batches share underlying questions. The diagnostic sets were written after reviewing course and practice materials, and prompt choices were made after earlier tests. They are small and not blinded or representative of all course coverage. The compact checks were selected after seeing prior development questions, which increases the risk of overfitting. Per-question results and earlier prompt comparisons are preserved in the workspace.

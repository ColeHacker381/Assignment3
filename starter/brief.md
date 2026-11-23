# Approach

The current standard and challenge prompts are short baselines that ask for the best answer and a JSON mapping. The challenge baseline explicitly permits “None of the above.” Neither baseline contains course material. These are provisional candidates pending further evaluation.

## Development and evidence

The course inventory in `../course-materials.md` covers the dynamic materials through November 11 and informed a separate pair of experimental prompts. Those prompts combine a concise reference on PCA, prediction, optimization, neural networks, sequences, generative models and AI-assisted development with setting-specific answer instructions. They are saved under `experiments/course-reference-v1/` for reproducibility.

The supplied runner used the pinned Qwen3.5-4B Q4_K_M model and llama.cpp runtime with the assignment settings. On the released ten-question batch per setting, the standard baseline scored 7/10 with 25 prompt tokens and the challenge baseline scored 6/10 with 39 prompt tokens. The course-reference experiment scored 6/10 with 662 prompt tokens on standard and 2/10 with 679 prompt tokens on challenge. All four runs returned valid answer mappings. The challenge experiment selected option 1 for all ten questions. On this limited evidence the current files retain the baseline prompts, while the experiment remains available for further study.

These measurements use the released examples only. The two batches share underlying questions, and repeated testing on them can overfit them. Scores do not establish hidden-set performance. This brief is preliminary and needs further development and broader evaluation before submission.

## Supplemental evaluation

A self-authored ten-question course-review set and its challenge variant are recorded in `evaluations/course-review/`. The questions were written after reviewing the released examples and course material, and are not a blinded or representative hidden-exam sample. The standard baseline scored 9/10 on this set. The challenge baseline scored 6/10 and missed all three questions where None was correct. A revised 46-token challenge prompt also scored 6/10 on this set and 6/10 on the released challenge batch, with no improvement in the three supplemental None cases. The current prompts remain unchanged pending stronger evidence.

## Challenge prompt comparison

Two additional challenge drafts were tested on the released and supplemental batches using the pinned local settings. A derive-first prompt scored 7/10 and 6/10 respectively, compared with 6/10 and 6/10 for the earlier challenge baseline. A prompt with a simple None-of-the-above example also scored 7/10 and 6/10. Both new drafts answered zero of the six questions whose correct answer was None correctly. The 74-token derive-first draft is the provisional challenge prompt because it matched the example-based draft with fewer tokens. This choice rests on two small development batches and should not be interpreted as a measured hidden-set improvement. Prompt texts and per-question results are in `experiments/challenge-selection/`.

## None-of-the-above examples

Two further challenge candidates included short examples illustrating both correct None selections and correct substantive selections. Across the released and supplemental challenge batches, neither chose None on any question. The balanced-example candidate scored 7/10 and 6/10, tying the current challenge prompt. The strict-match candidate scored 6/10 and 6/10. The current prompt had zero correct None answers and one false None selection across the same 20 questions. The example candidates had zero correct and zero false None selections. The results and prompt texts are in `experiments/none-examples/`; the 74-token challenge prompt remains the provisional choice. Repeated testing on these small sets limits what the comparison can establish.

## Paired challenge diagnostic

A self-authored paired set tested ten standard questions and challenge versions with six correct None answers across all four option positions. This intentionally oversamples None relative to the assignment and is not representative of hidden scoring. The standard baseline scored 8/10. The current challenge prompt scored 7/10, correctly selecting None in 4/6 applicable cases and selecting it incorrectly once in the other four. An experimental 155-token course-check prompt scored 9/10 on this targeted set, with 5/6 correct None cases and no false None selections, but scored 2/10 on released challenge questions and 4/10 on the earlier supplemental batch, both below the current prompt's 7/10 and 6/10. It selected option 1 for every released question. The current prompt remains the provisional choice. Paired questions, keys and predictions are recorded in `evaluations/paired-diagnostic/`. The diagnostic was self-authored after prior practice review and does not reveal the model's internal reasoning.

## Compact course-reference experiment

A 191-token challenge candidate retained the current selection instructions and added compact course checks chosen after reviewing the practice questions. It scored 7/10 released, 6/10 supplemental, and 8/10 on the paired diagnostic, compared with 7/10, 6/10, and 7/10 for the 74-token current prompt. Both got 4/12 correct None cases across these three development batches. The candidate's paired gain was on a substantive-answer question directly covered by its added reference. The current prompt remains provisional because these repeatedly used, nonrepresentative batches provide limited evidence of broader improvement. Candidate text and predictions are in `experiments/compact-reference/`.

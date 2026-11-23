# Approach

The current standard and challenge prompts are short baselines that ask for the best answer and a JSON mapping. The challenge baseline explicitly permits “None of the above.” Neither baseline contains course material. These are provisional candidates pending further evaluation.

## Development and evidence

The course inventory in `../course-materials.md` covers the dynamic materials through November 11 and informed a separate pair of experimental prompts. Those prompts combine a concise reference on PCA, prediction, optimization, neural networks, sequences, generative models and AI-assisted development with setting-specific answer instructions. They are saved under `experiments/course-reference-v1/` for reproducibility.

The supplied runner used the pinned Qwen3.5-4B Q4_K_M model and llama.cpp runtime with the assignment settings. On the released ten-question batch per setting, the standard baseline scored 7/10 with 25 prompt tokens and the challenge baseline scored 6/10 with 39 prompt tokens. The course-reference experiment scored 6/10 with 662 prompt tokens on standard and 2/10 with 679 prompt tokens on challenge. All four runs returned valid answer mappings. The challenge experiment selected option 1 for all ten questions. On this limited evidence the current files retain the baseline prompts, while the experiment remains available for further study.

These measurements use the released examples only. The two batches share underlying questions, and repeated testing on them can overfit them. Scores do not establish hidden-set performance. This brief is preliminary and needs further development and broader evaluation before submission.

## Supplemental evaluation

A self-authored ten-question course-review set and its challenge variant are recorded in `evaluations/course-review/`. The questions were written after reviewing the released examples and course material, and are not a blinded or representative hidden-exam sample. The standard baseline scored 9/10 on this set. The challenge baseline scored 6/10 and missed all three questions where None was correct. A revised 46-token challenge prompt also scored 6/10 on this set and 6/10 on the released challenge batch, with no improvement in the three supplemental None cases. The current prompts remain unchanged pending stronger evidence.

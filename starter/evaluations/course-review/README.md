# Course review evaluation

These ten questions were written for this project from the course topics listed in `../../../course-materials.md`. They are a small supplemental diagnostic set, not official course questions or a representative sample of the hidden exam. Several concepts also appear in the released examples and the experimental course-reference prompt. The set was authored after seeing those materials and is not a blinded holdout.

`standard.json` contains four substantive choices for each question. `challenge.json` replaces one choice per question with “None of the above.” The answer keys record the correct option number. For C02, C04, and C07 the replaced choice was correct, so None is correct. For the other questions a distractor was replaced.

The key follows these calculations and concepts:

- C01. The singular-vector identity gives Av = 5u.
- C02. Orthogonal reconstruction error is 80 − 53 = 27.
- C03. Fit preprocessing on training data, then apply it to test data.
- C04. Convexity gives 0.25 × 2 + 0.75 × 14 = 11.
- C05. Gradient descent subtracts the learning-rate-scaled gradient.
- C06. The activation is 4, so the chain rule gives (4 − 1) × 2 = 6.
- C07. Two stride-1 kernels of width 3 have receptive-field width 5.
- C08. Causal attention allows the current position and preceding positions.
- C09. Top-2 renormalization gives 0.5 / (0.5 + 0.3) = 0.625.
- C10. The VAE KL term regularizes the latent distribution toward its prior.

`challenge-v2.txt` is a short revised challenge prompt. Compare it and the baseline using the starter's `assignment3_runtime.run_batch` with the pinned model and settings. It is a diagnostic candidate, not a submitted prompt.

## Measurements

One run per prompt and batch used the pinned model, server and assignment generation settings. `results.json` records each answer and comparison. Both challenge prompts selected a substantive distractor on all three supplemental questions where None was correct.

| Prompt | Batch | Correct | Prompt tokens |
| --- | --- | ---: | ---: |
| Standard baseline | Supplemental standard | 9/10 | 25 |
| Challenge baseline | Supplemental challenge | 6/10 | 39 |
| Challenge v2 | Supplemental challenge | 6/10 | 46 |
| Challenge v2 | Released challenge | 6/10 | 46 |

The previously recorded challenge baseline scored 6/10 on the released challenge batch. The v2 prompt avoided the course-reference experiment's all-option-1 response on the released batch, but its overall score did not improve. The results do not establish the cause of the earlier behavior. We retain the existing submission prompts because this small set does not establish an improvement.

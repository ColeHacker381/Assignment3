# Broader course-topic evaluation

This self-authored batch covers linear algebra, evaluation, logistic regression, backpropagation, residual connections, U-Net, autoregressive modeling, attention, VAEs and Gaussian denoising. It was written after the prompts and earlier results were inspected. It is a fresh diagnostic batch, not a blinded or representative hidden exam. Questions were checked against the course inventory in `../../../course-materials.md`.

The standard answers are B01 2 (two nonzero singular values), B02 3 (final evaluation), B03 3 (sigmoid(0)=0.5), B04 1 (s−y), B05 2 (residual addition), B06 1 (encoder spatial detail), B07 2 (prefix), B08 3 (attention weights multiply values), B09 2 (differentiable latent sampling) and B10 3 (subtract predicted noise). The challenge version replaces one option per question. B03, B05 and B08 replace the correct option, making None correct in three of ten cases. The other seven replace distractors.

All runs used the pinned local model, runtime and assignment settings. `results.json` contains per-question outputs.

| Prompt | Qwen tokens | Batch | Correct | Correct None | False None |
| --- | ---: | --- | ---: | ---: | ---: |
| Current standard | 25 | Standard | 10/10 | — | — |
| Derive-first challenge | 74 | Challenge | 7/10 | 1/3 | 1/7 |
| Compact-reference challenge | 191 | Challenge | 8/10 | 1/3 | 0/7 |

The compact-reference prompt and derive-first prompt gave the same answers except B08 and B10. Both missed B08, while the compact-reference prompt correctly answered B10, where the derive-first prompt incorrectly selected None. On earlier development batches, the compact-reference prompt matched derive-first on released and supplemental sets and scored one point higher on a paired diagnostic question directly covered by its reference. The compact prompt is selected provisionally based on these local results. The small, self-authored sets and previous prompt tuning limit generalization, and no hidden score was measured.

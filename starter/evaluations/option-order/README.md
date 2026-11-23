# Challenge option-order check

This check rotates each answer option in the post-selection challenge batch forward by one position, with option 4 moving to option 1. Question stems, option text and answer correctness remain the same. The answer key was remapped with the options. This is a second presentation of the same questions, not an independent evaluation set.

The selected challenge prompt ran once on the rearranged batch using the pinned local model, runtime and assignment settings. It scored 8/10, compared with 9/10 on the original ordering, and correctly selected None on two of the three applicable questions rather than all three. It made one false None selection in each run, on P10. Per-question predictions for the rearranged run are in `results.json`; the original predictions are in `../postselection/results.json`.

After accounting for the rotation, nine chosen answers had the same content as before. On P06, the original run correctly selected None, while the reordered run selected a substantive distractor. P10 was incorrect in both orders. This single permutation of a small, self-authored set shows sensitivity on one question and does not estimate how often it occurs on unseen exams.

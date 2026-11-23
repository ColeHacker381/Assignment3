# Approach

These initial baselines use short general instructions to select the best answer and return JSON. The challenge prompt explicitly allows “None of the above.” Neither prompt includes course reference material. The next development step can use the course inventory to design and compare more informative prompts.

## Released practice results

The supplied local runner used the pinned Qwen3.5-4B Q4_K_M model and llama.cpp runtime with the assignment settings. On one released ten-question batch per setting, the standard baseline scored 7/10 with 25 prompt tokens, and the challenge baseline scored 6/10 with 39 prompt tokens. Both produced valid answer mappings. The standard errors were Q04, Q06, and Q09. The challenge errors were Q02, Q06, Q07, and Q09.

These are measured results on the released examples only, not estimates of hidden-set performance. The two practice batches share underlying questions, so their scores are not independent estimates. This brief and the prompts are preliminary and need further development before submission.

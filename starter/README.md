# Assignment 3 starter

Edit `standard.txt`, `challenge.txt`, and `brief.md`. The two prompt files are
limited to 1,500 tokens each under the pinned Qwen tokenizer. Keep your work in
Git if useful: `.git`, `.gitignore`, worktree files, and ordinary tool caches are
allowed in this workspace and are not included in the submission ZIP.

## Run the released practice questions locally

The optional helper downloads about 2.74 GB of model weights into a cache
outside this folder. It verifies the model and inference runtime against
`runtime-manifest.json`; it never selects a substitute model or engine.

1. Use Python 3.9 or newer.
2. Run `python3 setup_local.py` once. On Linux x86-64/ARM64, including WSL2, it
   downloads the pinned binary. On macOS it needs Xcode Command Line Tools and
   CMake and builds the pinned source with CPU-only settings.
3. Run `python3 run_practice.py` after editing your prompts.
4. Inspect `practice-results/standard.json` and
   `practice-results/challenge.json` for requests, responses, token counts,
   timings, and comparisons with the released keys.

Native Windows is not supported; use Ubuntu under WSL2. macOS Apple Silicon is
the currently tested local route. Linux, WSL2, Intel macOS, and different CPU
configurations may work but are not yet qualified. A fixed seed does not promise
identical answers across hardware. Gradescope's pinned Linux run is authoritative.
If setup does not work on your computer, use the Gradescope practice autograder.

The helper uses four CPU generation threads, four prompt-processing threads, no
GPU layers, no repacking, one slot, a 4,096-token context, temperature 0, seed
314159, thinking disabled, and at most 512 output tokens. It starts the model
once and runs one fresh request for each released ten-question batch.

The model uses the standard shared Hugging Face cache at
`~/.cache/huggingface/hub` (or `$HF_HOME/hub`). Set `ASSIGNMENT3_CACHE` to move
the smaller runtime/build cache. Rerunning setup reuses verified artifacts.

## Submit

Run `python3 package_submission.py`. It creates
`assignment-3-submission.zip` containing exactly:

- `standard.txt`
- `challenge.txt`
- `brief.md`

The packager ignores workspace extras but validates that the three declared
members are regular UTF-8 files. Upload that ZIP, or those three files, as
directed on Gradescope. Do not add question files or model outputs to your
submission.

The released practice output and correctness comparison are diagnostic only.
They carry no credit and are not your final grade. Private final questions are
not present in this starter or the practice autograder and will not run until
after submissions close.

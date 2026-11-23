"""Validate a workspace and create an Assignment 3 ZIP containing only declared files."""
from __future__ import annotations

import argparse
from pathlib import Path
import stat
import zipfile

REQUIRED = ("standard.txt", "challenge.txt", "brief.md")


def validate(workspace):
    errors = []
    for name in REQUIRED:
        path = workspace / name
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            errors.append(f"missing {name}")
            continue
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            errors.append(f"{name} must be a regular file, not a link or directory")
            continue
        try:
            path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{name} is not valid UTF-8")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("assignment-3-submission.zip"))
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    if output in {workspace / name for name in REQUIRED}:
        parser.exit(2, "Output ZIP must not overwrite a declared submission file.\n")
    errors = validate(workspace)
    if errors:
        parser.exit(2, "Cannot package submission:\n- " + "\n- ".join(errors) + "\n")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in REQUIRED:
            archive.write(workspace / name, name)
    with zipfile.ZipFile(output) as archive:
        if archive.namelist() != list(REQUIRED):
            raise RuntimeError("Internal packaging error")
    print(f"Wrote {output} with only: {', '.join(REQUIRED)}")
    print("Workspace metadata such as .git, .gitignore, and tool caches was left in place and excluded.")


if __name__ == "__main__":
    main()

"""Run both released practice batches with the pinned Assignment 3 profile."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from assignment3_runtime import LlamaClient, compare, load_key, load_questions, read_prompt, run_batch, ProtocolError

HERE = Path(__file__).resolve().parent


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def start_server(config, port):
    runtime = json.loads(config.read_text(encoding="utf-8"))
    server = Path(runtime["server"])
    model = Path(runtime["model"])
    manifest = json.loads(Path(runtime["manifest"]).read_text(encoding="utf-8"))
    if not server.is_file() or not model.is_file():
        raise RuntimeError("Runtime configuration points to a missing server or model; rerun setup_local.py")
    if file_sha(model) != manifest["model"]["sha256"]:
        raise RuntimeError("Pinned model SHA256 mismatch; rerun setup_local.py")
    environment = {key: value for key, value in os.environ.items() if not key.startswith("LLAMA_ARG_")}
    if sys.platform.startswith("linux"):
        environment["LD_LIBRARY_PATH"] = str(server.parent) + ":" + environment.get("LD_LIBRARY_PATH", "")
    version = subprocess.run([str(server), "--version"], capture_output=True, text=True, check=True, env=environment)
    version_text = version.stdout + version.stderr
    if manifest["runtime"]["tag"].removeprefix("b") not in version_text or manifest["runtime"]["commit"][:9] not in version_text:
        raise RuntimeError("llama-server is not the pinned build from runtime-manifest.json")
    command = [
        str(server), "-m", str(model), "-c", "4096", "-b", "256", "-np", "1",
        "-t", "4", "-tb", "4", "-ngl", "0", "--no-repack", "--host", "127.0.0.1",
        "--port", str(port), "--jinja", "--reasoning", "off", "--reasoning-budget", "0",
        "--no-context-shift", "--cache-ram", "0", "--no-webui",
    ]
    # Inherit stderr so diagnostics remain available without risking a full,
    # unread pipe blocking the long-running server.
    return subprocess.Popen(command, env=environment, stdout=subprocess.DEVNULL, stderr=None, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(".assignment3/runtime.json"))
    parser.add_argument("--port", type=int, default=8947)
    parser.add_argument("--output-dir", type=Path, default=Path("practice-results"))
    parser.add_argument("--server-already-running", action="store_true")
    args = parser.parse_args()
    server = None
    client = LlamaClient(args.port)
    try:
        if not args.server_already_running:
            server = start_server(args.config.resolve(), args.port)
            client.wait_until_ready()
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for setting in ("standard", "challenge"):
            prompt = read_prompt(Path(f"{setting}.txt"))
            questions, ids = load_questions(HERE / f"example-{setting}.json")
            key = load_key(HERE / f"answers-{setting}.json", ids)
            record = run_batch(client, prompt, questions, ids)
            rows, correct = compare(record["answers"], key, ids)
            record["comparison"] = rows
            record["practice_correct"] = correct
            record["practice_total"] = len(ids)
            output = args.output_dir / f"{setting}.json"
            output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"{setting}: {correct}/{len(ids)} on released practice only; {record['prompt_tokens']} prompt tokens")
            print(json.dumps(record["answers"], ensure_ascii=False, sort_keys=True))
        print("Practice only — these results are not your final grade.")
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError, ProtocolError) as exc:
        parser.exit(2, f"Practice run failed: {exc}\n")
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    main()

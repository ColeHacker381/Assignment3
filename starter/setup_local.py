"""Install the exact public Assignment 3 model and llama.cpp runtime into caches."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import tarfile
import tempfile
import urllib.request

HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url, destination, expected_sha, expected_bytes=None):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and sha256(destination) == expected_sha:
        return
    partial = destination.with_suffix(destination.suffix + ".partial")
    partial.unlink(missing_ok=True)
    print(f"Downloading {url}\n  -> {destination}", flush=True)
    with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as output:
        shutil.copyfileobj(response, output, length=4 * 1024 * 1024)
    if expected_bytes is not None and partial.stat().st_size != expected_bytes:
        partial.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded size mismatch for {destination.name}")
    actual = sha256(partial)
    if actual != expected_sha:
        partial.unlink(missing_ok=True)
        raise RuntimeError(f"SHA256 mismatch for {destination.name}: {actual}")
    partial.replace(destination)


def safe_extract(archive, destination):
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    links = []
    with tarfile.open(archive) as bundle:
        for member in bundle.getmembers():
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"Unsafe archive member: {member.name}")
            if member.islnk() or member.isdev():
                raise RuntimeError(f"Unsupported archive member: {member.name}")
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                source = bundle.extractfile(member)
                if source is None:
                    raise RuntimeError(f"Could not read archive member: {member.name}")
                with source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
                target.chmod(member.mode & 0o777)
            elif member.issym():
                links.append((target, member.linkname))
            else:
                raise RuntimeError(f"Unsupported archive member: {member.name}")
    for target, linkname in links:
        resolved_link = (target.parent / linkname).resolve()
        if resolved_link != root and root not in resolved_link.parents:
            raise RuntimeError(f"Unsafe archive link: {target.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(linkname)


def find_server(root):
    matches = [path for path in root.rglob("llama-server") if path.is_file()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one llama-server under {root}; found {len(matches)}")
    matches[0].chmod(matches[0].stat().st_mode | stat.S_IXUSR)
    return matches[0]


def linux_runtime(spec, cache):
    architecture = platform.machine().lower()
    key = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(architecture)
    if key is None:
        raise RuntimeError(f"Unsupported Linux CPU architecture: {architecture}")
    asset = spec["runtime"]["assets"][key]
    root = cache / "llama.cpp" / spec["runtime"]["commit"] / f"linux-{key}"
    try:
        return find_server(root)
    except RuntimeError:
        pass
    archive = cache / "downloads" / Path(asset["url"]).name
    download(asset["url"], archive, asset["sha256"])
    safe_extract(archive, root)
    return find_server(root)


def mac_runtime(spec, cache, jobs):
    for command in ("cmake", "c++"):
        if shutil.which(command) is None:
            raise RuntimeError(f"macOS setup requires {command}; install Xcode Command Line Tools and CMake")
    source_spec = spec["runtime"]["source"]
    root = cache / "llama.cpp" / spec["runtime"]["commit"] / "macos-source"
    build = root / "build"
    candidates = list(build.rglob("llama-server")) if build.exists() else []
    if len(candidates) == 1:
        return candidates[0]
    archive = cache / "downloads" / f"llama.cpp-{spec['runtime']['commit']}.tar.gz"
    download(source_spec["url"], archive, source_spec["sha256"])
    with tempfile.TemporaryDirectory(prefix="assignment3-llama-") as temporary:
        unpack = Path(temporary)
        safe_extract(archive, unpack)
        source_dirs = [path for path in unpack.iterdir() if path.is_dir()]
        if len(source_dirs) != 1:
            raise RuntimeError("Unexpected llama.cpp source archive layout")
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(source_dirs[0], root)
    subprocess.run([
        "cmake", "-S", str(root), "-B", str(build), "-DCMAKE_BUILD_TYPE=Release",
        "-DGGML_NATIVE=OFF", "-DGGML_METAL=OFF", "-DGGML_CUDA=OFF", "-DLLAMA_BUILD_TESTS=OFF",
    ], check=True)
    subprocess.run(["cmake", "--build", str(build), "--config", "Release", "--target", "llama-server", "-j", str(jobs)], check=True)
    return find_server(build)


def install(manifest, cache, config, jobs=4, model_cache=None):
    spec = json.loads(manifest.read_text(encoding="utf-8"))
    system = platform.system()
    if system == "Windows":
        raise RuntimeError("Native Windows is not supported. Run this setup inside WSL2 (Ubuntu).")
    if system == "Linux":
        server = linux_runtime(spec, cache)
    elif system == "Darwin":
        server = mac_runtime(spec, cache, jobs)
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")
    model_cache = model_cache or (Path.home() / ".cache" / "huggingface" / "hub")
    model = model_cache / f"models--{spec['model']['repo'].replace('/', '--')}" / "snapshots" / spec["model"]["revision"] / spec["model"]["file"]
    model_url = f"https://huggingface.co/{spec['model']['repo']}/resolve/{spec['model']['revision']}/{spec['model']['file']}"
    download(model_url, model, spec["model"]["sha256"], spec["model"]["bytes"])
    environment = os.environ.copy()
    if system == "Linux":
        environment["LD_LIBRARY_PATH"] = str(server.parent) + ":" + environment.get("LD_LIBRARY_PATH", "")
    version = subprocess.run([str(server), "--version"], capture_output=True, text=True, check=True, env=environment)
    version_text = version.stdout + version.stderr
    if spec["runtime"]["tag"].removeprefix("b") not in version_text or spec["runtime"]["commit"][:9] not in version_text:
        raise RuntimeError("Installed llama-server does not report the pinned build and commit")
    if sha256(model) != spec["model"]["sha256"]:
        raise RuntimeError("Installed model failed its final SHA256 verification")
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(json.dumps({"server": str(server), "model": str(model), "manifest": str(manifest.resolve())}, indent=2) + "\n", encoding="utf-8")
    print(f"Verified pinned runtime and model. Wrote {config}")
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    local_manifest = HERE / "runtime-manifest.json"
    source_manifest = HERE / "example-package" / "runtime-manifest.json"
    parser.add_argument("--manifest", type=Path, default=local_manifest if local_manifest.is_file() else source_manifest)
    default_cache = Path(os.environ.get("ASSIGNMENT3_CACHE", Path.home() / ".cache" / "assignment3-qwen35"))
    parser.add_argument("--cache", type=Path, default=default_cache)
    default_hf = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    parser.add_argument("--model-cache", type=Path, default=default_hf)
    parser.add_argument("--config", type=Path, default=Path(".assignment3/runtime.json"))
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    try:
        install(
            args.manifest.resolve(), args.cache.expanduser().resolve(), args.config.resolve(),
            max(1, args.jobs), args.model_cache.expanduser().resolve(),
        )
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"Setup failed: {exc}\nSee README.md for manual setup and supported platforms.\n")


if __name__ == "__main__":
    main()

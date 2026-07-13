#!/usr/bin/env python3
"""Build a release zip from tracked files only."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def run(cmd: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def require_clean_git_tree(root: Path) -> list[str]:
    result = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], root)
    if result.returncode != 0:
        return [f"git status failed: {result.stderr.strip() or result.stdout.strip()}"]
    if result.stdout.strip():
        return ["release tree is dirty or has untracked files; commit/stash/remove them before packaging", result.stdout.rstrip()]
    return []


def tracked_files(root: Path) -> tuple[list[Path], list[str]]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return [], [f"git ls-files failed: {result.stderr.decode(errors='replace').strip()}"]
    paths = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        rel = Path(raw.decode("utf-8"))
        path = root / rel
        if path.is_file():
            paths.append(rel)
    return sorted(paths), []


def validate_package(root: Path) -> list[str]:
    validator = root / "validate-agent-harness-reliability.py"
    result = run([sys.executable, str(validator), str(root)], root)
    if result.returncode != 0:
        return ["validation failed before packaging", result.stdout.rstrip(), result.stderr.rstrip()]
    return []


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(root: Path, version: str) -> tuple[Path, Path, list[str]]:
    errors = require_clean_git_tree(root)
    if errors:
        return Path(), Path(), errors
    errors = validate_package(root)
    if errors:
        return Path(), Path(), errors
    files, errors = tracked_files(root)
    if errors:
        return Path(), Path(), errors
    if not files:
        return Path(), Path(), ["no tracked files found; refusing to build empty archive"]

    output_dir = root / "downloads"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"beginners-guide-to-agent-harness-reliability-{version}.zip"
    checksum = output.with_suffix(output.suffix + ".sha256")
    for path in [output, checksum]:
        if path.exists():
            path.unlink()

    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for rel in files:
            archive.write(root / rel, rel)

    checksum.write_text(f"{sha256_file(output)}  {output.name}\n", encoding="utf-8")
    return output, checksum, []


def main() -> int:
    parser = argparse.ArgumentParser(description="Build release zip from tracked files only.")
    parser.add_argument("--version", required=True, help="Release version, such as v0.1.2.")
    parser.add_argument("--root", default=".", help="Package root.")
    args = parser.parse_args()

    output, checksum, errors = build(Path(args.root).resolve(), args.version)
    if errors:
        print("Release package build failed:")
        for error in errors:
            if error:
                print(error)
        return 1
    print(output)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a release zip without requiring external zip tools."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


EXCLUDED_PARTS = {".git", "__pycache__", "downloads"}


def should_include(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return not any(part in EXCLUDED_PARTS for part in rel.parts)


def build(root: Path, version: str) -> Path:
    output_dir = root / "downloads"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"beginners-guide-to-agent-harness-reliability-{version}.zip"
    if output.exists():
        output.unlink()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file() and should_include(path, root):
                archive.write(path, path.relative_to(root))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build release zip.")
    parser.add_argument("--version", default="v0.1.1", help="Release version, such as v0.1.1.")
    parser.add_argument("--root", default=".", help="Package root.")
    args = parser.parse_args()
    output = build(Path(args.root).resolve(), args.version)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

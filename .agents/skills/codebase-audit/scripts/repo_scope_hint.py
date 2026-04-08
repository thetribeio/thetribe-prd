#!/usr/bin/env python3
"""
Quick repository size hints for scoping Phases 1–2 (no extra dependencies).

Run from the repository root (or pass the path). Prefers `git ls-files` when inside a git work tree;
otherwise walks the tree skipping common vendor/build directories.

Interpret counts using references/large-repository-strategy.md in this skill.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    "out",
    "target",
    "vendor",
    "__pycache__",
    ".venv",
    "venv",
    "coverage",
    ".turbo",
    ".parcel-cache",
}


def git_ls_files_count(root: Path) -> int | None:
    if not (root / ".git").exists():
        return None
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    return len(lines)


def walk_file_count(root: Path) -> int:
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_DIR_NAMES and not d.startswith(".")
        ]
        n += len(filenames)
    return n


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0]).resolve() if args else Path.cwd()

    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    git_count = git_ls_files_count(root)
    if git_count is not None:
        print(f"method=git_ls_files")
        print(f"tracked_paths={git_count}")
    else:
        print(f"method=directory_walk")
        print(f"files_count_excluding_common_vendor_dirs={walk_file_count(root)}")
    print("Map this count to a review strategy in references/large-repository-strategy.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

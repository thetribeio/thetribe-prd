#!/usr/bin/env python3
"""
Verify dependencies for optional Phase 4 (PDF) of the codebase-audit skill.

Usage:
  python check_audit_env.py              # warn if reportlab missing, exit 0
  python check_audit_env.py --require-pdf  # exit 1 if reportlab missing (fail fast before a long audit)
"""

from __future__ import annotations

import argparse
import sys


def reportlab_available() -> bool:
    try:
        import reportlab  # noqa: F401

        return True
    except ImportError:
        return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Check PDF export prerequisites for codebase-audit.")
    p.add_argument(
        "--require-pdf",
        action="store_true",
        help="Exit with code 1 if reportlab is not installed (use before starting Phases 1–3 when PDF is required).",
    )
    args = p.parse_args(argv)

    if reportlab_available():
        print("reportlab: OK (PDF export ready)")
        return 0

    msg = (
        "reportlab is not installed. Phase 4 (PDF) will fail.\n"
        "Install with: pip install reportlab\n"
        "Or skip PDF and deliver markdown only."
    )
    if args.require_pdf:
        print(msg, file=sys.stderr)
        return 1

    print(msg, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

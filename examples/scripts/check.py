#!/usr/bin/env python3
"""
EXAMPLE ONLY — not used in the TDWI lab workshop.

Starter template for a deterministic pre-push / CI check script.
The lab uses Recipe 2 (pytest via AGENTS.md) instead.

When adopting (Recipe 1):
  1. Copy this file to scripts/check.py at your repo root.
  2. Grow it incrementally, cheapest checks first:
     - ruff check .  /  ruff format --check .
     - smoke imports (e.g. import generate_sales_report)
     - pytest (below)
     - integration or deploy smoke tests
  3. Reference in AGENTS.md: "Run python scripts/check.py before pushing."

Try this example from repo root (optional, post-lab):
    python examples/scripts/check.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# examples/scripts/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str]) -> int:
    print(f"+ {' '.join(command)}", flush=True)
    return subprocess.run(command, check=False, cwd=REPO_ROOT).returncode


def main() -> int:
    # Example extension points (uncomment as you adopt):
    # if (code := run(["ruff", "check", "."])) != 0:
    #     return code
    # if (code := run(["ruff", "format", "--check", "."])) != 0:
    #     return code

    return run([sys.executable, "-m", "pytest", "test_sales_report.py"])


if __name__ == "__main__":
    sys.exit(main())

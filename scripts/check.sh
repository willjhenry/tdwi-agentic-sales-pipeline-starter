#!/usr/bin/env bash
# TDWI lab — deterministic checks before push/PR (Recipe 1 starter).
# Run from repo root: bash scripts/check.sh

set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> pip dry-run (catch dependency conflicts before install)"
python -m pip install --dry-run -r requirements.txt

# --- Extension points (uncomment as you grow this script) ---
# echo "==> ruff"
# ruff check .
# ruff format --check .

echo "==> pytest"
python -m pytest test_sales_report.py

echo "All checks passed."
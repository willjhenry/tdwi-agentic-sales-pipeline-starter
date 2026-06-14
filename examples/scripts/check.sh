#!/usr/bin/env bash
# EXAMPLE ONLY — not shipped on upstream main (Part 3 lab creates a simpler scripts/check.sh).
#
# Unix wrapper for the check script (Mac, Linux, Cloud Agent VM, Git Bash on Windows).
#
# When adopting (Recipe 1):
#   1. Copy this file and check.py to scripts/ at your repo root.
#   2. Update the exec line below to: exec python scripts/check.py
#   3. chmod +x scripts/check.sh
#
# Try this example from repo root (optional, post-lab):
#   bash examples/scripts/check.sh

set -euo pipefail
cd "$(dirname "$0")/../.."
exec python examples/scripts/check.py

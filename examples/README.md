# Examples (not used in the lab)

Everything under `examples/` is **starter / vanilla reference material** for ideas you might adopt **after** the workshop. The hands-on lab does **not** implement these files.

| Path | Recipe | When adopting |
|------|--------|----------------|
| [`scripts/check.py`](scripts/check.py), [`scripts/check.sh`](scripts/check.sh) | 1 | Copy to `scripts/` at repo root; extend with linters, smoke tests |
| [`cursor/commands/commit-code.md`](cursor/commands/commit-code.md) | 3 | Copy to `.cursor/commands/` |
| [`github/workflows/ci.yml`](github/workflows/ci.yml) | 4 | Copy to `.github/workflows/`; point at your `scripts/check.py` |
| [`automations/pr-review-instructions.md`](automations/pr-review-instructions.md) | 5 | Paste into Cursor Automations |

See [WORKFLOW_RECIPES.md](../WORKFLOW_RECIPES.md) for the full framework.

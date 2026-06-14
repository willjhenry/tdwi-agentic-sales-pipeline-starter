# Examples (post-lab reference)

Everything under `examples/` is **starter / vanilla reference material** for ideas you might adopt **after** the workshop. The hands-on lab does **not** ship these files on upstream `main`.

**Exception:** Part 3 Step 8 has students create their own minimal `scripts/check.sh` (pip dry-run + pytest). The files here are a **fuller** Recipe 1 template to grow into after the lab.

| Path | Recipe | When adopting |
|------|--------|----------------|
| [`scripts/check.py`](scripts/check.py), [`scripts/check.sh`](scripts/check.sh) | 1 | Post-lab: copy to `scripts/` and extend (or grow your lab `check.sh`) |
| [`cursor/commands/commit-code.md`](cursor/commands/commit-code.md) | 3 | Copy to `.cursor/commands/` |
| [`github/workflows/ci.yml`](github/workflows/ci.yml) | 4 | Copy to `.github/workflows/`; point at your `scripts/check.py` |
| [`automations/pr-review-instructions.md`](automations/pr-review-instructions.md) | 5 | Paste into Cursor Automations |

See [WORKFLOW_RECIPES.md](../WORKFLOW_RECIPES.md) for the full framework.

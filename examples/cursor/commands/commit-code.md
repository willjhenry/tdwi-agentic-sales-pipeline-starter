# commit-code

**EXAMPLE ONLY — not used in the lab.** Copy to `.cursor/commands/commit-code.md` to enable `/commit-code` in Cursor (Recipe 3).

Optional arguments: `--quick` or `--no-review` (skip the expensive sub-agent review step).

---

Review the current git diff. Then run deterministic checks before suggesting a commit:

1. Run your check script from the repo root (after adopting Recipe 1, typically `python scripts/check.py`; to try the example as-is: `python examples/scripts/check.py`).
2. If checks fail, stop and summarize failures—do not suggest a commit.
3. Unless the user passed `--quick` or `--no-review`, launch a **fresh sub-agent** (or separate review pass) to review only the diff. The reviewer must not be the same context that wrote the changes. Focus on scope, correctness risks, and test coverage—not re-running the full implementation.
   - **Note:** Sub-agent review is **slow and costly** (extra model calls). Use it as the last automated gate before a human commit/merge, or skip with `--quick` while your team is still adopting the workflow.
4. If review or checks surface issues, summarize them for the user.
5. If all gates are green, draft a concise commit message from the diff and ask the user whether to commit.

Do not commit unless the user explicitly confirms.

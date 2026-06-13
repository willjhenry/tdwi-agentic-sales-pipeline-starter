# PR review automation instructions (example)

**EXAMPLE ONLY — Part 3 uses similar text hands-on; this file is a copy-paste reference.**

In production, prefer your AI provider's built-in PR review features when available (e.g. Cursor **Bugbot**, **Approval Agents**). Custom Automations teach the same **agent-as-reviewer** pattern in a portable way—see Recipe 5 in [WORKFLOW_RECIPES.md](../../WORKFLOW_RECIPES.md).

**Trigger:** GitHub → **Pull request opened** only (when a draft is marked **Ready for review**). Do **not** use **Draft opened**—see loop prevention below.

**Output:** PR comments; optionally a **draft** fix PR when blocking errors are found.

Agent review on a PR is **expensive** (model cost + latency). Run it **after** cheap deterministic CI/tests are green (Recipes 1 and 4), not instead of them.

## Loop prevention

| Setup | Risk |
|-------|------|
| Trigger on **draft opened** + agent fixes issues | High—automation re-fires on every new draft |
| Trigger on ready + fix **all** suggestions | High—there are always more suggestions |
| **Recommended:** ready only + fix **blocking errors** + open **draft** fix PR | Low—human marks ready again if another pass is wanted |

Prompts are not deterministic; this is a tested pattern, not a guarantee.

```text
Review this pull request.

Focus on:
- Summary of what changed and whether the approach fits the existing codebase
- Correctness, edge cases, and error handling in the diff
- Whether tests were added or updated; note if the PR does not mention test results
- New or changed dependencies (e.g. requirements.txt): necessity and version pinning
- Scope: flag unrelated refactors or drive-by changes
- Security or data-handling concerns if relevant

Post a concise review as PR comments: summary, strengths, blocking errors, suggested improvements. Do not merge or approve. If you find blocking errors, implement the fixes and open a draft PR using this PR's branch (the branch under review) as the base—not the default branch. The fix PR must be a draft. Include a link to the fix PR in your review summary comment.
```

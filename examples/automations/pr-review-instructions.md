# PR review automation instructions (example)

**EXAMPLE ONLY — Part 3 uses similar text hands-on; this file is a copy-paste reference.**

In production, prefer your AI provider's built-in PR review features when available (e.g. Cursor **Bugbot**, **Approval Agents**). Product helpers like **`/babysit`** can assist with PR follow-up—review and experiment as you build your workflow. Custom Automations teach the **agent-as-reviewer** pattern in a portable way—see Recipe 5 in [WORKFLOW_RECIPES.md](../../WORKFLOW_RECIPES.md).

**Trigger:** GitHub → **Pull request opened** only (when a draft is marked **Ready for review**). Do **not** use **Draft opened**.

**Output (lab):** PR comments only. Fixes are handled by a **separate implementer agent** on the same branch (Part 3 Step 6b)—not by the automation opening new PRs.

Agent review on a PR is **expensive** (model cost + latency). Run it **after** cheap deterministic CI/tests are green (Recipes 1 and 4), not instead of them.

## Loop prevention

| Setup | Risk |
|-------|------|
| Trigger on **draft opened** | High—automation re-fires on every new draft |
| Automation opens fix PRs | High—wrong base branch, merge-order issues, re-fire on ready-to-merge |
| **Lab / recommended:** ready only + **comments only** | Low—human or Step 6b agent fixes on same branch |

## Lab prompt (comments only)

```text
Review this pull request.

Focus on:
- Summary of what changed and whether the approach fits the existing codebase
- Correctness, edge cases, and error handling in the diff
- Whether tests were added or updated; note if the PR does not mention test results
- New or changed dependencies (e.g. requirements.txt): necessity and version pinning
- Scope: flag unrelated refactors or drive-by changes
- Security or data-handling concerns if relevant

Post a concise review as PR comments: summary, strengths, blocking errors, suggested improvements. Do not merge or approve. Do not open new pull requests or push code—comments only.
```

## Advanced (not used in lab): automation opens fix PRs

Some teams ask the automation to implement blocking fixes and open a **draft** PR. This is **fragile** (agents often pick the wrong base branch; merge order gets complicated). Prefer **Bugbot + babysit** or **comments + separate implementer agent** instead. If you experiment, instruct the agent to use the **reviewed branch as base—not `main`**—and expect to verify base branch manually on GitHub.

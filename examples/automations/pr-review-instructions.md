# PR review automation instructions (example)

**EXAMPLE ONLY — Part 3 uses similar text hands-on; this file is a copy-paste reference.**

Use in Cursor **Automations** → **Comment on pull request** (Recipe 5 in [WORKFLOW_RECIPES.md](../../WORKFLOW_RECIPES.md)).

Trigger: GitHub → **Pull request opened** (includes when a draft is marked **Ready for review**).

Agent review on a PR is **expensive** (model cost + latency). Run it **after** cheap deterministic CI/tests are green (Recipes 1 and 4), not instead of them.

```text
Review this pull request for the TDWI sales pipeline lab.

Focus on:
- Whether cleaning logic is reused from generate_sales_report.load_and_clean_data() (not duplicated)
- Whether requirements.txt pins any new dependencies (e.g. streamlit)
- Whether existing tests in test_sales_report.py would still pass; note if the PR does not mention test results
- Filter/UI edge cases if a Streamlit app was added
- Scope: flag unrelated refactors

Post a concise review as PR comments: summary, strengths, 1–3 suggestions. Do not merge or approve.
```

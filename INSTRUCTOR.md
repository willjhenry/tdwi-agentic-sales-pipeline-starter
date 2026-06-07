# TDWI Lab 3 — Instructor Notes

Teaching guide for this workshop. Students use [README.md](README.md) and the Part 1–3 notebooks; this file is for you.

## Lab map (student-facing summary)

See the **Lab map** table in [README.md](README.md).

## Suggested timeboxes

| Segment | Time | Notes |
|---------|------|--------|
| **Setup** (README) | 30–45 min | Fork, clone, `.venv`, first push; PAT auth is the usual snag |
| **Part 1** | 45–60 min | First Cloud env build can take several minutes; secrets must target **student forks** |
| **Part 2** | 60–75 min | Cloud Agent run is mostly async; human review + merge while agent works for fast groups |
| **Part 3** | 20–30 min | Automation setup + second agent run + mark PR ready |
| **Debrief** (all parts) | 10–15 min each | Use debrief questions at the end of each notebook |

Total: roughly **3–4 hours** with breaks, or split across sessions.

## Before class

- [ ] Confirm students have Cursor accounts on a plan with **Cloud Agents** (and **Automations** for Part 3).
- [ ] Confirm GitHub is connected; everyone works on **their fork**, not only `willjhenry/tdwi-agentic-sales-pipeline-starter`.
- [ ] Upstream `main` stays the **clean starter** (broken pipeline, minimal `AGENTS.md`). Optional: maintain `main-working-example` for your dry runs.
- [ ] You have run Parts 1–3 once on a fork (see gotchas below).

## Teaching notes by part

### Setup (README)

- Fork is required so Cloud Agents and Automations run against the student’s repo.
- Windows: `python` vs `py` for venv; Mac: `python3`.

### Part 1 — Cloud environment

- `.cursor/environment.json` is already in the starter repo; students verify detection in the dashboard (“Repo file observed”).
- Secrets: `REPORT_EXPORT_KEY` (runtime), `TEST_ENV_VAR` (env var); scope to **This repo** / their fork.
- Agent smoke-test prompt is in the notebook.

### Part 2 — Fix pipeline with Cloud Agent

- Students run **pytest first**, then `generate_sales_report.py` (secret / `output/` errors are expected on broken `main`).
- **`AGENTS.md`**: students add the **testing workflow rule** in class (text is in the notebook); they must **commit and push** before starting the agent.
- Starter `AGENTS.md` intentionally does **not** spell out the fix—tests + student prompt define done.
- Cloud Agent opens a **draft PR** by default.
- **Optional demo in agent VM:** Terminal → pytest + script; Desktop → open `report.png` (keyring password `test`; Chrome default-browser prompt may hang first open—retry).
- After `git fetch`, students run `git branch -a` to confirm `remotes/origin/<branch>`.
- **Ready for review** is required on GitHub before merge.
- Locally after merge: `export REPORT_EXPORT_KEY=demo-123` (or any value) before running the script.

### Part 3 — Automations + Streamlit

- Automations trigger: **Pull request opened** (includes draft → **Ready for review**; not **Draft opened**).
- Output: **Comment on pull request**; automation must be on the **same fork** where PRs open.
- Part 3 agent adds `revenue_explorer.py` + `streamlit` in `requirements.txt`.
- If Automations is unavailable on some accounts, demo on your fork and use **Bugbot** for compare/contrast in debrief.

## Common issues

| Issue | What to tell students |
|-------|------------------------|
| Agent can’t see `AGENTS.md` changes | Push to fork before starting the agent |
| Can’t merge draft PR | Click **Ready for review** first |
| `git checkout` branch not found | `git fetch origin` then `git branch -a` |
| Script fails after merge locally | Set `REPORT_EXPORT_KEY` in the terminal |
| Automation didn’t run | Trigger is **opened** (ready), not draft created; check fork + automation repo match |

## Debrief prompts (in notebooks)

Each part notebook ends with student debrief questions. Part 3 includes **Automations vs Bugbot vs CI**—keep that discussion even if Automations was demo-only.

## Repo hygiene

- `.gitignore` ignores `*.png` and `output/` so generated artifacts aren’t committed.
- Do not commit workshop solutions to upstream `main` if it is the shared starter.

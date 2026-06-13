# Agent workflow framework & example recipes

Post-lab reference for building reliable **human + agent** development workflows. The hands-on lab (Parts 1–3) uses **Recipe 2** (`AGENTS.md` + pytest) only.

Everything under [`examples/`](examples/) is **starter / vanilla reference material**—ideas to adopt after the workshop, **not** implemented in the lab. See [`examples/README.md`](examples/README.md).

## Core framework

**Treat agents like engineers with tools—not like the entire pipeline.**

| Principle | What it means |
|-----------|----------------|
| **Agents run scripts; they don't replace them** | Put linters, tests, and checks in deterministic scripts or CI. The agent's job is to run them and react to output. |
| **Agents are probabilistic; gates are deterministic** | Don't ask an agent "is this correct?" when `pytest` or `ruff` can answer definitively. |
| **ReAct loop** | **Act** (run check) → **Observe** (stdout, exit code) → **Reason** (what to fix) → repeat until green. |
| **Escalating cost** | Cheap linters → tests → **fresh-context final review (expensive)** → **human merge**. Run the cheapest gate that can fail first. |
| **Separate implementer from final reviewer** | Just as a colleague with fresh eyes catches what you missed, an agent benefits when **another agent with fresh context** reviews the finished diff—not the same run that wrote the code. Humans and agents both review and iterate **while** building (editing, running tests, fixing); this principle is about the **final** critique before merge: sub-agent, PR Automation, Bugbot, Approval Agents, or human PR review. Fresh-context review costs extra time and model usage; use it last among automated gates, or skip with `--quick` while adopting. |
| **Humans keep merge authority** | Automate the inner loop; a person still approves the PR. |

### Intentional gates—not the only way

The recipes below are **one adoption path**, not a mandatory stack. Teams pick surfaces that match their maturity: pytest in `AGENTS.md` only, or check scripts, or CI, or PR Automations—or combinations. The **core idea** the lab is teaching:

1. **Implementation agent** does the work (Cloud Agent, local agent, etc.).
2. **Deterministic gates** (linters, tests, CI) catch objective failures cheaply.
3. **Fresh-context final review** critiques the diff before merge—another agent (or reviewer), not the one that wrote the code. Incremental self-review while implementing is expected; this step is the deliberate **final** pass.

That third step is the main payoff of Recipe 5 and the `/commit-code` sub-agent step in Recipe 3. Research and practice show that a **reflection** or **critique** pass—stepping back from the implementation trace—often improves quality. You are wiring that into the workflow on purpose.

**How this relates to ReAct:** The implementation loop is classic ReAct against **tools**: **Act** (edit code, run pytest) → **Observe** (failures, exit codes) → **Reason** (what to fix) → repeat. Fresh-context review is a **second loop**: the reviewer **observes** the finished diff (and optionally test/CI status) and **reasons** about correctness, scope, and risks—without carrying the implementation agent's chain-of-thought. It is not a substitute for pytest; it catches different things (design fit, subtle logic, scope creep). Use both.

You can place the reflection step locally (slash command sub-agent), on the PR (Automation), or both. The lab uses PR Automations because it is event-driven and easy to demo after human **Ready for review**.

### Target inner loop

```text
Agent implements
  → cheap CI (linters, formatters)
  → tests (pytest, smoke)
  → fresh-context final review (optional, expensive)
→ human review → merge
```

Automate the parenthesized steps gradually via scripts, `AGENTS.md`, rules, slash commands, hooks, GitHub Actions, and PR automations. Teams rarely jump to full automation on day one—and that's fine.

### Where you wire it

| Surface | Good for |
|---------|----------|
| **Local** | `scripts/check.py` (you create from example), `AGENTS.md`, `.cursor/rules/`, `/commit-code`, pre-commit hooks |
| **Cloud Agent** | Same `AGENTS.md` + same check script in the Dockerfile-managed VM |
| **GitHub** | Actions workflow on PR; Automations on **PR opened** or **CI completed**; Cloud Agents responding to CI/review events |

Implementation details depend on your stack and AI tool (Cursor, Copilot, Claude Code, etc.). The **pattern** is portable.

---

## Example recipes (simple → advanced)

> **Lab vs examples:** Only **Recipe 2** and **Recipe 5** (Part 3) are practiced in the workshop. Recipes 1, 3, 4, and 6 are illustrated by files in `examples/`—copy and extend them on your own fork after the lab.

### Recipe 1 — Deterministic check script *(example only)*

**One entry point** for humans and agents. Same command on Mac, Linux, Windows (PowerShell), and Cloud Agent Linux.

When you adopt, copy [`examples/scripts/check.py`](examples/scripts/check.py) to `scripts/check.py` and grow it (ruff, smoke imports, etc.). The example includes commented extension points.

Try the example from repo root (optional, post-lab):

```bash
python examples/scripts/check.py
```

On Mac/Linux or Git Bash: `bash examples/scripts/check.sh`

- **Lab:** Students use `python -m pytest test_sales_report.py` via `AGENTS.md` (Recipe 2)—not this script.

**`AGENTS.md` snippet (after you adopt):**

```markdown
Before pushing, run `python scripts/check.py` and fix all failures. Re-run until exit code 0.
```

---

### Recipe 2 — `AGENTS.md` workflow rules *(lab default)*

Encode "run tests before push" in repo-level agent instructions. Students add this in **Part 2**.

- **In lab:** [`AGENTS.md`](AGENTS.md) + the testing paragraph in [`LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb`](LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb)
- **ReAct:** Cloud Agent runs pytest, reads failures, fixes code, repeats.

This is the minimum viable deterministic gate—no extra tooling required.

---

### Recipe 3 — `/commit-code` slash command *(example only)*

A Cursor **slash command** that orchestrates: diff → run check script → (optional) sub-agent review → suggest commit message → ask user to confirm.

- **Example:** [`examples/cursor/commands/commit-code.md`](examples/cursor/commands/commit-code.md)  
  Copy to `.cursor/commands/commit-code.md` to enable `/commit-code`.

**Why start here:** Easy to try, easy to adjust. Commands can take arguments (e.g. `--quick` to skip **expensive** sub-agent review). Good for teams adopting AI workflows incrementally.

**Inner loop automated:** check script + optional review. **Human** still confirms the commit.

---

### Recipe 4 — GitHub Actions CI *(example only)*

Run the **same** check script on every push/PR so GitHub is the source of truth for "green."

- **Example:** [`examples/github/workflows/ci.yml`](examples/github/workflows/ci.yml)  
  Copy to `.github/workflows/ci.yml` on your fork; point at `scripts/check.py` after adopting Recipe 1.

**Pair with Recipe 2:** Agent runs checks locally before push; CI catches anything that slipped through.

**Part 3 connection:** Debrief asks about a **CI completed** trigger so Automations run only after green checks—not instead of CI.

---

### Recipe 5 — PR review (+ fix) Automation *(lab: Part 3)*

Event-driven **agent review** on GitHub after a human marks a draft PR **Ready for review**. Optionally fixes **blocking errors** in a **new draft PR**—so the automation does not immediately re-fire.

- **In lab:** Part 3 hands-on
- **Example instructions:** [`examples/automations/pr-review-instructions.md`](examples/automations/pr-review-instructions.md)

**Trigger:** **Pull request opened** only—not **Draft opened**. Implementation PRs and fix PRs stay drafts until a human marks them ready.

**Loop prevention:** Fix **blocking errors** only (not every suggestion). Opening fix PRs as **drafts** plus ready-only triggers avoids most recursion; asking the agent to fix all suggestions on draft-opened triggers can loop indefinitely.

**Position in the stack:** After deterministic CI/tests. Agent review is **expensive**—don't use it as a substitute for linters or pytest. Compare with **Bugbot** (product default) vs your custom checklist (Automations).

**What this recipe is really teaching:** **Separate implementer from final reviewer**—implementation agent and review agent are separate runs. That reflection step is intentional; see [Intentional gates—not the only way](#intentional-gatesnot-the-only-way) in the core framework. Draft vs ready triggers and blocking-only fixes are **engineering choices** to make automation safe, not requirements for every team.

**Provider-native review vs custom Automations:** The pattern—**agent as reviewer**, triggered on PR events—is universal. Vendors are productizing it. On Cursor, for example, **Bugbot** and **Approval Agents** are dedicated review features; **Automations** let you roll your own checklist and fix behavior. Other AI coding tools offer similar built-ins.

| Approach | When to use |
|----------|-------------|
| **Provider feature** (e.g. Bugbot, Approval Agents) | Default for production—better integration, maintained by the vendor, less prompt engineering |
| **Custom Automation** (this recipe) | Teach the portable pattern; encode **your** team's checklist; combine review + fix exactly how you want |

**Recommendation:** Explore your provider's dedicated review features first. For Cursor teams, Bugbot is an excellent production choice. The lab uses a **custom Automation on purpose** so you learn the general workflow—not because custom is always better, and not to imply Bugbot is the only or uniquely special option. After the workshop, try both and pick what fits your team.

---

### Recipe 6 — End-to-end ticket → draft PR *(aspirational example)*

A fully wired flow teams work toward—not a required lab exercise.

```text
Jira ticket (context)
  → launch Cloud Agent with ticket + AGENTS.md + rules + MCP tools
  → agent implements on branch
  → runs check script (linters + tests) in a loop until green
  → fresh sub-agent reviews diff (expensive; last automated gate)
  → opens draft PR for human review
  → (optional) GitHub CI + PR Automation on ready
  → human merges
```

**Ingredients:**

| Piece | Role |
|-------|------|
| **Jira (or Linear, etc.)** | Ticket title, acceptance criteria, links—agent context |
| **MCP / docs** | Live access to APIs, schemas, runbooks |
| **`AGENTS.md` + rules** | Repo conventions, check commands, definition of done |
| **Check script** (from example) | Cheap deterministic gates |
| **Sub-agent review** | Expensive gate before PR—budget time and model cost |
| **Draft PR + human** | Final accountability |

**Caveats:** Product support for "auto-fix on CI failure" and ticket triggers varies by tool. Start with Recipes 1–3 locally, add 4–5 on GitHub, then integrate issue trackers and MCP as the team matures.

---

## Adoption path (suggested)

1. **Recipe 2** — `AGENTS.md` + pytest (**lab**)
2. **Recipe 1** — copy `examples/scripts/check.py` → `scripts/check.py`
3. **Recipe 3** — `/commit-code` for local commits (use `--quick` until sub-agent review is worth the cost)
4. **Recipe 4** — GitHub Actions running the same script
5. **Recipe 5** — PR Automation after ready + green CI (**lab Part 3**)
6. **Recipe 6** — Ticket integration + MCP + full inner-loop automation

Take small steps. Adjust prompts and gates based on what fails in practice.

---

## Related lab material

| Part | What you practiced |
|------|-------------------|
| **Part 1** | Reproducible Cloud environment (same checks can run in the agent VM when you adopt them) |
| **Part 2** | Recipe 2 + human local verify before merge |
| **Part 3** | Recipe 5 + Automations vs Bugbot vs CI discussion |

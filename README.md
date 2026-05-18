# TDWI Agentic Sales Data Pipeline – Lab 3 Starter Repo

**Course:** Agentic Code Generation: From Prompting to Production-Ready Autonomous Agents  
**Lab 3:** From Broken Script → Self-Testing Production PR (60–75 minutes)

**Welcome!**  
This is a deliberately buggy but realistic data pipeline for the hands-on lab.  
Your Cloud Agent will clean messy sales data, run real tests **in the cloud**, generate a report chart, and open a PR — all while you close your laptop.

### Files in this repo
- `data/messy_sales_data.csv` – 100 rows of intentionally messy e-commerce data  
- `src/generate_sales_report.py` – buggy script the agent must fix  
- `tests/test_sales_report.py` – failing tests the agent must make pass  
- `requirements.txt` – pandas, matplotlib, pytest  
- `Dockerfile` – production-ready config (full Python image + ubuntu user)  
- `.cursor/environment.json` – tells Cursor to use the Dockerfile

### Lab Instructions (real 2026 production flow)

**Step 1: Clone and open the repo in Cursor**
```bash
git clone https://github.com/willjhenry/tdwi-agentic-sales-pipeline-starter.git
cd tdwi-agentic-sales-pipeline-starter
code .
```

**Step 2: Create your Cloud Agent Development Environment (Dockerfile-managed)**  
1. Open **Agents Window** (Cmd/Ctrl + Shift + P → “Agents: Open Agents Window”).  
2. Go to the **Environment** tab → **Create new Development Environment**.  
3. Name it: `Sales Pipeline Env`.  
4. Choose **Agent-driven setup**.  
   → Cursor will automatically read `.cursor/environment.json` and use the committed `Dockerfile`.

**Step 3: Manually attach the build secret (important production step)**  
1. After the environment shows “Ready”, stay in the **Environment** tab.  
2. In the **Secrets** section, click **Attach secret**.  
3. Select (or create in My Secrets dashboard) the secret named `REPORT_EXPORT_KEY`.  
4. Enter any fake value (e.g. `demo-123`).  
5. Set the toggle to **“This repo”** (least-privilege best practice).  

**Step 4: Give the agent its mission**  
Paste this exact prompt into Composer or the Agent chat:

> “You are a senior data engineer. Fix the buggy sales data pipeline.  
> 1. Clean messy_sales_data.csv (remove duplicates, fix dates, calculate correct revenue).  
> 2. Add summary metrics (total revenue, top 5 customers, avg order value).  
> 3. Generate a matplotlib chart and save it as report.png in the root.  
> 4. Use the REPORT_EXPORT_KEY secret to ‘encrypt’ the final CSV export (mock function).  
> 5. Make all tests in tests/test_sales_report.py pass.  
> 6. Run the full test suite with pytest.  
> Only open a PR when everything is green. Include the chart and a one-paragraph business summary in the PR description.”

**Step 5: Watch the agent work (20–30 min)**  
- The agent will use the Cloud Dev Environment you defined.  
- It will edit code, run `pytest` **in the cloud**, iterate until tests pass, and open a PR.  
- You can close your laptop — the agent keeps going.

**Step 6: Debrief & Best-Practice Takeaways (15 min – group discussion)**  
Answer these on your handout:  
1. How was the test-running experience different from basic Cloud Agents?  
2. What did the per-secret “This repo” / “All repos” toggle actually control?  
3. Why do we manage the environment with a committed `Dockerfile` + `.cursor/environment.json`?  
4. Which Module 4 safety rules did we just apply? (Dockerfile as code, manual secret attachment, build vs runtime secrets)

---

**Production Note for Managers**  
Dockerfile-managed environments give you version-controlled consistency (exactly what enterprise teams use). Secrets are attached manually, which is the expected pattern when you want full control. For real production pipelines, prefer external secret managers + MCP for runtime credentials.

Enjoy the lab!  
— Your TDWI Instructor
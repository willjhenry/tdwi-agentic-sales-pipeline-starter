# TDWI Agentic Sales Data Pipeline – Lab 3 Starter Repo

**Course:** Agentic Code Generation: From Prompting to Production-Ready Autonomous Agents  

**Lab 3:** From Broken Script → Self-Testing Production PR (60–75 min)

**Welcome!**  

This is a deliberately buggy but realistic data pipeline for the hands-on lab.  

Your Cloud Agent will clean messy sales data, run tests in the cloud, generate a report chart, and open a PR — all while you close your laptop.

### Files in this repo

- `data/messy_sales_data.csv` – 100 rows of intentionally messy e-commerce data  

- `src/generate_sales_report.py` – buggy script the agent must fix  

- `tests/test_sales_report.py` – failing tests the agent must make pass  

- `requirements.txt` – pandas, matplotlib, pytest  

- `Dockerfile` – already configured for secure build secrets  

### Lab Instructions (copy these into your Cursor Agent chat)

**Step 1:** Clone and open the repo in Cursor  

```bash

git clone [https://github.com/willjhenry/tdwi-agentic-sales-pipeline-starter.git](https://github.com/willjhenry/tdwi-agentic-sales-pipeline-starter.git)

cd tdwi-agentic-sales-pipeline-starter

code .
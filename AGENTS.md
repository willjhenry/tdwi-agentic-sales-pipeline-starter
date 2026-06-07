# AGENTS.md

## Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

Lab work is to implement data cleaning in `load_and_clean_data()` in `generate_sales_report.py` until `test_sales_report.py` passes (dedupe orders, fix dates, correct revenue). Do not reorganize the repo or change import paths unless the user asks.

### Human-only lab docs

These files are for **humans** during the workshop. They exist in the repo but are **not** your runbook:

- **`README.md`** — one-time setup (GitHub, fork, clone, local `.venv`, test push). **Do not** follow or repeat these steps.
- **`LAB3-Part-1-Cloud-Agent-Environment-Setup.ipynb`** — Part 1 UI walkthrough (Cloud Agent environment, secrets). **Do not** follow notebook steps.
- **`LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb`** — Part 2 UI walkthrough (local tests, Cloud Agent fix, PR review). **Do not** follow notebook steps.
- **`LAB3-Part-3-Automations.ipynb`** — Part 3 Automations setup and Streamlit Cloud Agent prompt. **Do not** follow notebook steps.

Use **this file (`AGENTS.md`)**, the user's prompt, and the Python source/tests as your source of truth. Do not modify the lab notebook unless the user explicitly asks.

### Repo layout

Starter files live at the repo root:

- `generate_sales_report.py` 
- `test_sales_report.py` — pytest tests

Data files live in the `data` directory:

- `data/messy_sales_data.csv` — messy e-commerce input data

## Core Workflow Rules

### Running the pipeline

```bash
python generate_sales_report.py
```

### Running tests

```bash
python -m pytest test_sales_report.py
```


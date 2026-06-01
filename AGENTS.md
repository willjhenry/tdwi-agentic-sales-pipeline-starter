# AGENTS.md

You are a senior data engineer and python developer.

## Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

Lab work is to implement data cleaning in `load_and_clean_data()` in `generate_sales_report.py` until `test_sales_report.py` passes (dedupe orders, fix dates, correct revenue). Do not reorganize the repo or change import paths unless the user asks.

### Human-only lab docs

These files are for **humans** during the workshop. They exist in the repo but are **not** your runbook:

- **`README.md`** — one-time setup (GitHub, fork, clone, local `.venv`, test push). **Do not** follow or repeat these steps.
- **`LAB3-Cloud-Agent-Environment-Setup.ipynb`** — in-lab UI walkthrough (Cloud Agent environment, secrets, prompts). **Do not** follow notebook steps (fork, clone, Environment tab flows, secret attachment, etc.). Humans perform those while you work on code.

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

Always run `python -m pytest test_sales_report.py` before pushing changes. Ensure all tests pass before pushing. After fixing code, re-run the tests to verify the fixes. If a test fails, diagnose the issue, fix it, and re-run the tests to verify. Iterate until all tests pass and you have met the user's requirements.


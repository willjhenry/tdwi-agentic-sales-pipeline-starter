# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

Lab work is to implement data cleaning in `load_and_clean_data()` in `generate_sales_report.py` until `test_sales_report.py` passes (dedupe orders, fix dates, correct revenue). Do not reorganize the repo or change import paths unless the user asks.

### Human-only lab docs

These files are for **humans** during the workshop. They exist in the repo but are **not** your runbook:

- **`README.md`** — one-time setup (GitHub, fork, clone, local `.venv`, test push). **Do not** follow or repeat these steps.
- **`LAB3-Cloud-Agent-Environment-Setup.ipynb`** — in-lab UI walkthrough (Cloud Agent environment, secrets, prompts). **Do not** follow notebook steps (fork, clone, Environment tab flows, secret attachment, etc.). Humans perform those while you work on code.

Use **this file (`AGENTS.md`)**, the user's prompt, and the Python source/tests as your source of truth. Do not modify the lab notebook unless the user explicitly asks.

### Dependencies

Install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

In Cloud Agent environments, all dependencies are pre-installed via the root `Dockerfile`.

### Repo layout

Starter files live at the repo root:

- `generate_sales_report.py` 
- `test_sales_report.py` — pytest tests

Data files live in the `data` directory:

- `data/messy_sales_data.csv` — messy e-commerce input data

### Running the pipeline

```bash
python generate_sales_report.py
```

### Running tests

```bash
python -m pytest test_sales_report.py
```

Always run `python -m pytest test_sales_report.py` before pushing changes. Ensure all tests pass before pushing.

### Linting

No linter is configured in this repo. If you add one (e.g. `ruff`, `flake8`), install it separately.

### Docker (optional)

Cloud environment config is in `.cursor/environment.json`: the **build** step uses the root `Dockerfile`, and the **install** hook runs `pip install -r requirements.txt` when the environment starts (so dependencies may be installed both at image build and again on startup). Build secrets are not required for the image build; `REPORT_EXPORT_KEY` is only used at runtime in the script.

```bash
docker build -f Dockerfile -t sales-pipeline .
```

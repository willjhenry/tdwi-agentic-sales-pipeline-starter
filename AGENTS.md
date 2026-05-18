# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

### Dependencies

Install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

In Cloud Agent environments, pandas, matplotlib, and pytest are pre-installed via `.cursor/Dockerfile`.

### Repo layout

Starter files live at the repo root:

- `generate_sales_report.py` — main pipeline script (intentionally buggy)
- `test_sales_report.py` — pytest tests
- `messy_sales_data.csv` — messy e-commerce input data

Note: the script and tests reference paths like `data/messy_sales_data.csv` and `src.generate_sales_report`; fixing those mismatches is part of the lab exercise.

### Running the pipeline

```bash
python generate_sales_report.py
```

### Running tests

```bash
python -m pytest test_sales_report.py
```

### Linting

No linter is configured in this repo. If you add one (e.g. `ruff`, `flake8`), install it separately.

### Docker (optional)

The Cloud Agent Dockerfile lives at `.cursor/Dockerfile` (see `.cursor/environment.json`). Build secrets are not required for the image build; `REPORT_EXPORT_KEY` is only used at runtime in the script.

```bash
docker build -f .cursor/Dockerfile -t sales-pipeline .
```

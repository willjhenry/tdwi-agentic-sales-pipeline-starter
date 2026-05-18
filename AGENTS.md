# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

### Key Gotchas

- **Install dependencies** with `pip install -r requirements.txt` or `pip install --user -r requirements.txt`. The file pins `pandas==3.0.3`, `matplotlib==3.10.9`, and `pytest==9.0.3`.
- **Expected layout** (files live in subdirectories, not the repo root):
  - `src/generate_sales_report.py` — main pipeline script
  - `tests/test_sales_report.py` — pytest tests
  - `data/messy_sales_data.csv` — input data (25 rows)
- **pip `--user` installs to `~/.local/bin`** — ensure `PATH` includes `$HOME/.local/bin` for `pytest` CLI access.
- **`create_chart()` has a known bug** — `df.groupby("date")["revenue"].sum().plot(kind="bar")` raises `ValueError: Must supply freq for datetime value` due to a pandas/matplotlib compatibility issue. The rest of the pipeline (load, clean, metrics, export) works correctly.

### Running the pipeline

```bash
python src/generate_sales_report.py
```

### Running tests

```bash
python -m pytest tests/
```

### Linting

No linter is configured in this repo. If you add one (e.g. `ruff`, `flake8`), install it separately.

### Docker (optional)

The Dockerfile builds a containerized version. It requires a build secret:
```bash
docker build --secret id=REPORT_EXPORT_KEY,env=REPORT_EXPORT_KEY -t sales-pipeline .
```

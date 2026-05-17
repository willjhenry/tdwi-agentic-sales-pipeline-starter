# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

### Key Gotchas

- **Install dependencies** with `pip install -r requirements.txt`. The file pins `pandas==3.0.3`, `matplotlib==3.10.9`, and `pytest==9.0.3`.
- **Source files may not exist** until the lab exercise creates them. The expected layout is:
  - `src/generate_sales_report.py` — main pipeline script
  - `tests/test_sales_report.py` — pytest tests
  - `data/messy_sales_data.csv` — input data (100 rows)
- **pip installs to `~/.local/bin`** — ensure `PATH` includes `$HOME/.local/bin` for `pytest` CLI access.

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

# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python data pipeline starter repo for the TDWI "Agentic Code Generation" lab. It cleans messy e-commerce sales data, runs tests, and generates a sales report chart.

### Key Gotchas

- **`requirements.txt` has an intentionally invalid pytest version** (`pytest==0.0.3`). This is part of the lab exercise. Do NOT run `pip install -r requirements.txt` directly — it will fail. Instead, install pandas and matplotlib at pinned versions, and install pytest without a version pin:
  ```
  pip install --user pandas==3.0.3 matplotlib==3.10.9 pytest
  ```
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

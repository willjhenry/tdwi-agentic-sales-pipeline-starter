import pandas as pd
import pytest

from generate_sales_report import filter_sales_data, compute_kpis
from revenue_explorer import parse_customer_id, parse_date_range


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "product": ["Widget", "Gadget", "Widget"],
            "customer_id": [1, 2, 1],
            "revenue": [10.0, 20.0, 30.0],
        }
    )


def test_filter_sales_data_empty_products_returns_no_rows(sample_df):
    filtered = filter_sales_data(sample_df, products=[])
    assert filtered.empty


def test_compute_kpis_empty_dataframe():
    empty = pd.DataFrame(columns=["revenue"])
    assert compute_kpis(empty) == (0.0, 0, 0.0)


def test_parse_customer_id_rejects_non_numeric_input():
    customer_id, error = parse_customer_id("abc")
    assert customer_id is None
    assert error is not None


def test_parse_date_range_falls_back_for_incomplete_selection():
    min_date = pd.Timestamp("2024-01-01").date()
    max_date = pd.Timestamp("2024-12-31").date()
    assert parse_date_range((), min_date, max_date) == (min_date, max_date)

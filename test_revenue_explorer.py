import pandas as pd
import pytest

from generate_sales_report import compute_kpis, filter_sales_data, load_and_clean_data
from revenue_explorer import parse_customer_id, parse_date_range


@pytest.fixture
def cleaned_df():
    return load_and_clean_data()


def test_filter_empty_products_returns_no_rows(cleaned_df):
    filtered = filter_sales_data(cleaned_df, products=[])
    assert len(filtered) == 0


def test_compute_kpis_empty_dataframe():
    empty_df = pd.DataFrame(columns=["revenue"])
    assert compute_kpis(empty_df) == (0.0, 0, 0.0)


def test_parse_customer_id_accepts_blank_input():
    assert parse_customer_id("") == (None, None)
    assert parse_customer_id("   ") == (None, None)


def test_parse_customer_id_accepts_valid_integer():
    assert parse_customer_id("42") == (42, None)


def test_parse_customer_id_rejects_non_numeric_input():
    customer_id, error = parse_customer_id("abc")
    assert customer_id is None
    assert error is not None


def test_parse_date_range_single_date():
    single_date = pd.Timestamp("2024-01-15").date()
    start, end = parse_date_range(single_date, single_date, single_date)
    assert start == single_date
    assert end == single_date


def test_parse_date_range_normalizes_inverted_range():
    early = pd.Timestamp("2024-01-01").date()
    late = pd.Timestamp("2024-01-31").date()
    start, end = parse_date_range((late, early), early, late)
    assert start == early
    assert end == late

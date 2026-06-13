import pandas as pd
import pytest
from datetime import date

from generate_sales_report import load_and_clean_data
from revenue_explorer import apply_filters, normalize_date_range, parse_date_range


@pytest.fixture
def cleaned_df():
    return load_and_clean_data()


def test_apply_filters_empty_products_returns_no_rows(cleaned_df):
    start = cleaned_df["date"].min().date()
    end = cleaned_df["date"].max().date()
    filtered = apply_filters(cleaned_df, start, end, [], None)
    assert filtered.empty


def test_apply_filters_unknown_customer_returns_no_rows(cleaned_df):
    start = cleaned_df["date"].min().date()
    end = cleaned_df["date"].max().date()
    products = sorted(cleaned_df["product"].unique())
    filtered = apply_filters(cleaned_df, start, end, products, 99999)
    assert filtered.empty


def test_apply_filters_single_day_range(cleaned_df):
    day = cleaned_df["date"].min().date()
    products = sorted(cleaned_df["product"].unique())
    filtered = apply_filters(cleaned_df, day, day, products, None)
    expected = cleaned_df[cleaned_df["date"].dt.date == day]
    pd.testing.assert_frame_equal(
        filtered.reset_index(drop=True),
        expected.reset_index(drop=True),
    )


def test_normalize_date_range_swaps_inverted_dates():
    start = date(2024, 3, 15)
    end = date(2024, 1, 1)
    assert normalize_date_range(start, end) == (end, start)


def test_parse_date_range_handles_partial_selection():
    min_date = date(2024, 1, 1)
    max_date = date(2024, 3, 15)
    assert parse_date_range((date(2024, 2, 1),), min_date, max_date) == (
        date(2024, 2, 1),
        date(2024, 2, 1),
    )
    assert parse_date_range((), min_date, max_date) == (min_date, max_date)


def test_apply_filters_inverted_dates_match_ordered_range(cleaned_df):
    start = cleaned_df["date"].max().date()
    end = cleaned_df["date"].min().date()
    products = sorted(cleaned_df["product"].unique())
    filtered = apply_filters(cleaned_df, start, end, products, None)
    expected = apply_filters(cleaned_df, end, start, products, None)
    pd.testing.assert_frame_equal(
        filtered.reset_index(drop=True),
        expected.reset_index(drop=True),
    )

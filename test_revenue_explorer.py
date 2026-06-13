import pandas as pd
import pytest

from generate_sales_report import load_and_clean_data
from revenue_explorer import apply_filters


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

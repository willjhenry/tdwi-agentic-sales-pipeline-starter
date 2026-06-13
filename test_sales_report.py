import matplotlib

matplotlib.use("Agg")

import pytest
import pandas as pd
from generate_sales_report import (
    create_chart,
    load_and_clean_data,
    generate_metrics,
)


@pytest.fixture
def cleaned_df():
    df = load_and_clean_data()
    return df


def test_total_revenue_is_positive(cleaned_df):
    total = cleaned_df["revenue"].sum()
    assert total > 0, "Total revenue should be positive"


def test_no_duplicate_orders(cleaned_df):
    assert len(cleaned_df) == len(cleaned_df.drop_duplicates()), (
        "Duplicates were not removed"
    )


def test_top_customers_have_5_entries(cleaned_df):
    top = cleaned_df.groupby("customer_id")["revenue"].sum().nlargest(5)
    assert len(top) == 5, "Should return top 5 customers"


def test_revenue_calculation_is_correct(cleaned_df):
    expected = cleaned_df["price"] * cleaned_df["quantity"]
    assert (cleaned_df["revenue"] == expected).all(), "Revenue must be price * quantity"


def test_date_column_is_datetime(cleaned_df):
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["date"]), (
        "Date column must be datetime"
    )


def test_create_chart_with_datetime_dates(cleaned_df, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    create_chart(cleaned_df)
    assert (tmp_path / "report.png").exists()

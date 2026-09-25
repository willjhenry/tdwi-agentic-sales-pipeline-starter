import pandas as pd
import pytest

from generate_sales_report import (
    daily_revenue,
    filter_sales,
    load_and_clean_data,
    summarize_sales,
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


def test_filter_limits_products_dates_and_customer(cleaned_df):
    start = cleaned_df["date"].min()
    end = start + pd.Timedelta(days=2)
    product = cleaned_df["product"].iloc[0]
    customer_id = cleaned_df["customer_id"].iloc[0]

    filtered = filter_sales(cleaned_df, start, end, [product], customer_id)

    assert not filtered.empty
    assert (filtered["product"] == product).all()
    assert (filtered["customer_id"].astype(str) == str(customer_id)).all()
    assert filtered["date"].between(start, end).all()


def test_optional_customer_filter_keeps_every_customer(cleaned_df):
    filtered = filter_sales(
        cleaned_df,
        cleaned_df["date"].min(),
        cleaned_df["date"].max(),
        cleaned_df["product"].unique(),
    )
    assert len(filtered) == len(cleaned_df)


def test_summary_matches_filtered_rows(cleaned_df):
    total_revenue, order_count, average_order_value = summarize_sales(cleaned_df)
    assert order_count == len(cleaned_df)
    assert total_revenue == pytest.approx(cleaned_df["revenue"].sum())
    assert average_order_value == pytest.approx(total_revenue / order_count)


def test_empty_summary_is_zero():
    total_revenue, order_count, average_order_value = summarize_sales(
        pd.DataFrame(columns=["revenue"])
    )
    assert (total_revenue, order_count, average_order_value) == (0.0, 0, 0.0)


def test_daily_revenue_sums_to_total(cleaned_df):
    trend = daily_revenue(cleaned_df)
    assert trend.sum() == pytest.approx(cleaned_df["revenue"].sum())
    assert trend.index.is_monotonic_increasing

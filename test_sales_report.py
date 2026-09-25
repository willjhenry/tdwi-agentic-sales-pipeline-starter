from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from generate_sales_report import (
    create_chart,
    daily_revenue,
    filter_sales,
    load_and_clean_data,
    sales_kpis,
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


def test_filter_by_product_customer_and_dates(cleaned_df):
    filtered = filter_sales(
        cleaned_df,
        start="2025-01-15",
        end="2025-01-20",
        products=["Widget A"],
        customer_id=101,
    )
    assert not filtered.empty
    assert set(filtered["product"]) == {"Widget A"}
    assert set(filtered["customer_id"]) == {101}
    assert filtered["date"].min() >= pd.Timestamp("2025-01-15")
    assert filtered["date"].max() <= pd.Timestamp("2025-01-20")


def test_customer_filter_is_optional(cleaned_df):
    filtered = filter_sales(
        cleaned_df,
        start=cleaned_df["date"].min(),
        end=cleaned_df["date"].max(),
        products=sorted(cleaned_df["product"].unique()),
    )
    assert len(filtered) == len(cleaned_df)


def test_empty_product_selection_has_zero_kpis(cleaned_df):
    filtered = filter_sales(
        cleaned_df,
        start=cleaned_df["date"].min(),
        end=cleaned_df["date"].max(),
        products=[],
    )
    total, count, avg = sales_kpis(filtered)
    assert filtered.empty
    assert total == 0
    assert count == 0
    assert avg == 0


def test_revenue_explorer_shows_filtered_kpis():
    app = AppTest.from_file(
        str(Path(__file__).resolve().parent / "revenue_explorer.py"),
        default_timeout=30,
    )
    app.run()
    assert not app.exception
    assert [metric.label for metric in app.metric] == [
        "Total revenue",
        "Order count",
        "Average order value",
    ]
    assert app.metric[0].value == "$1,459.48"
    assert app.metric[1].value == "25"

    app.sidebar.selectbox[0].set_value("101").run()
    app.sidebar.multiselect[0].set_value(["Widget C"]).run()
    assert app.metric[1].value == "0"
    assert app.info[0].value == "No orders match the current filters."


def test_create_chart_writes_report(cleaned_df, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    create_chart(cleaned_df)
    assert (tmp_path / "report.png").is_file()


def test_kpis_and_daily_revenue_use_filtered_rows(cleaned_df):
    filtered = filter_sales(
        cleaned_df,
        start="2025-01-15",
        end="2025-02-02",
        products=["Widget C"],
    )
    total, count, avg = sales_kpis(filtered)
    assert count == len(filtered)
    assert total == pytest.approx(filtered["revenue"].sum())
    assert avg == pytest.approx(filtered["revenue"].mean())
    assert daily_revenue(filtered).sum() == pytest.approx(total)

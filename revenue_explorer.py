# streamlit run revenue_explorer.py

import streamlit as st

from generate_sales_report import (
    compute_kpis,
    daily_revenue,
    filter_sales_data,
    load_and_clean_data,
)


@st.cache_data
def load_data():
    return load_and_clean_data()


def _parse_date_range(date_range):
    if isinstance(date_range, tuple) and len(date_range) == 2:
        return date_range
    return date_range, date_range


def main():
    st.set_page_config(page_title="Revenue Explorer", layout="wide")
    st.title("Revenue Explorer")

    df = load_data()
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    all_products = sorted(df["product"].unique())

    with st.sidebar:
        st.header("Filters")
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        products = st.multiselect("Products", options=all_products, default=all_products)
        customer_options = ["All customers", *sorted(df["customer_id"].unique())]
        customer_choice = st.selectbox("Customer ID", options=customer_options)

    start_date, end_date = _parse_date_range(date_range)
    customer_filter = None if customer_choice == "All customers" else customer_choice
    filtered = filter_sales_data(
        df,
        start_date=start_date,
        end_date=end_date,
        products=products,
        customer_id=customer_filter,
    )

    total_revenue, order_count, avg_order_value = compute_kpis(filtered)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Order Count", f"{order_count:,}")
    col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

    st.subheader("Daily Revenue Trend")
    trend = daily_revenue(filtered)
    if trend.empty:
        st.info("No revenue data for the selected filters.")
    else:
        st.line_chart(trend.rename("revenue"))


if __name__ == "__main__":
    main()

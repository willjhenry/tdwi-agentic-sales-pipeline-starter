# streamlit run revenue_explorer.py

import streamlit as st

from generate_sales_report import (
    compute_kpis,
    daily_revenue_series,
    filter_sales_data,
    load_and_clean_data,
)


@st.cache_data
def get_sales_data():
    return load_and_clean_data()


def parse_date_range(date_range, min_date, max_date):
    if isinstance(date_range, tuple) and len(date_range) == 2:
        return date_range
    if hasattr(date_range, "year"):
        return date_range, date_range
    return min_date, max_date


def parse_customer_id(customer_id_input):
    customer_id_input = customer_id_input.strip()
    if not customer_id_input:
        return None
    return int(customer_id_input)


def render_sidebar(df):
    st.sidebar.header("Filters")

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    all_products = sorted(df["product"].unique())
    selected_products = st.sidebar.multiselect(
        "Product",
        options=all_products,
        default=all_products,
    )

    customer_id_input = st.sidebar.text_input("Customer ID (optional)", value="")

    start_date, end_date = parse_date_range(date_range, min_date, max_date)
    customer_id = parse_customer_id(customer_id_input)

    return filter_sales_data(
        df,
        start_date=start_date,
        end_date=end_date,
        products=selected_products,
        customer_id=customer_id,
    )


def render_kpis(df):
    total_revenue, order_count, avg_order_value = compute_kpis(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Order Count", f"{order_count:,}")
    col3.metric("Average Order Value", f"${avg_order_value:,.2f}")


def render_daily_revenue_chart(df):
    st.subheader("Daily Revenue Trend")

    if df.empty:
        st.info("No data matches the selected filters.")
        return

    chart_data = daily_revenue_series(df).reset_index()
    chart_data.columns = ["date", "revenue"]
    chart_data["date"] = chart_data["date"].astype(str)
    st.line_chart(chart_data, x="date", y="revenue")


def main():
    st.set_page_config(page_title="Revenue Explorer", layout="wide")
    st.title("Revenue Explorer")

    df = get_sales_data()
    filtered_df = render_sidebar(df)

    render_kpis(filtered_df)
    render_daily_revenue_chart(filtered_df)


if __name__ == "__main__":
    main()

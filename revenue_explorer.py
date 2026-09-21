import streamlit as st

from generate_sales_report import (
    daily_revenue,
    filter_sales,
    load_and_clean_data,
    sales_kpis,
)

st.set_page_config(page_title="Revenue Explorer", layout="wide")


@st.cache_data
def load_data():
    return load_and_clean_data()


def _date_bounds(date_range, min_date, max_date):
    if isinstance(date_range, (tuple, list)):
        if len(date_range) == 2:
            return date_range
        if len(date_range) == 1:
            return date_range[0], date_range[0]
        return min_date, max_date
    return date_range, date_range


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
    products = sorted(df["product"].unique())
    selected_products = st.sidebar.multiselect(
        "Product",
        options=products,
        default=products,
    )
    customer_ids = sorted(df["customer_id"].unique())
    customer_labels = ["All"] + [str(customer_id) for customer_id in customer_ids]
    customer_choice = st.sidebar.selectbox("Customer ID", customer_labels)
    customer_id = None if customer_choice == "All" else int(customer_choice)
    start, end = _date_bounds(date_range, min_date, max_date)
    return filter_sales(df, start, end, selected_products, customer_id)


def render_kpis(df):
    total_revenue, order_count, avg_order_value = sales_kpis(df)
    total_col, count_col, avg_col = st.columns(3)
    total_col.metric("Total revenue", f"${total_revenue:,.2f}")
    count_col.metric("Order count", f"{order_count:,}")
    avg_col.metric("Average order value", f"${avg_order_value:,.2f}")


def render_trend(df):
    st.subheader("Daily revenue trend")
    trend = daily_revenue(df)
    if trend.empty:
        st.info("No orders match the current filters.")
        return
    chart = trend.rename("revenue").reset_index()
    st.line_chart(chart, x="date", y="revenue")


def main():
    st.title("Revenue Explorer")
    filtered = render_sidebar(load_data())
    render_kpis(filtered)
    render_trend(filtered)


main()

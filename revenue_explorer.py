import streamlit as st

from generate_sales_report import (
    daily_revenue,
    filter_sales,
    load_and_clean_data,
    summarize_sales,
)


st.set_page_config(page_title="Revenue Explorer", layout="wide")
st.title("Revenue Explorer")

sales = load_and_clean_data()
if sales.empty:
    st.info("No orders match the current filters.")
    st.stop()

min_date = sales["date"].min().date()
max_date = sales["date"].max().date()
product_options = sorted(sales["product"].unique())
customer_options = ["All", *[str(customer_id) for customer_id in sorted(sales["customer_id"].unique())]]

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    selected_products = st.multiselect(
        "Product",
        options=product_options,
        default=product_options,
    )
    customer_choice = st.selectbox("Customer ID", options=customer_options)

if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = date_range

customer_id = None if customer_choice == "All" else customer_choice
filtered = filter_sales(sales, start_date, end_date, selected_products, customer_id)
total_revenue, order_count, average_order_value = summarize_sales(filtered)

revenue_col, orders_col, average_col = st.columns(3)
revenue_col.metric("Total revenue", f"${total_revenue:,.2f}")
orders_col.metric("Order count", f"{order_count:,}")
average_col.metric("Average order value", f"${average_order_value:,.2f}")

st.subheader("Daily revenue")
trend = daily_revenue(filtered)
if trend.empty:
    st.info("No orders match the current filters.")
else:
    st.line_chart(trend)

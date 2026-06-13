# streamlit run revenue_explorer.py

import streamlit as st
import pandas as pd

from generate_sales_report import load_and_clean_data


@st.cache_data
def get_data():
    return load_and_clean_data()


def filter_data(df, start_date, end_date, products, customer_id):
    filtered = df[
        (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
    ]

    if products:
        filtered = filtered[filtered["product"].isin(products)]

    if customer_id is not None:
        filtered = filtered[filtered["customer_id"] == customer_id]

    return filtered


st.set_page_config(page_title="Revenue Explorer", layout="wide")
st.title("Revenue Explorer")

df = get_data()
min_date = df["date"].min().date()
max_date = df["date"].max().date()
all_products = sorted(df["product"].unique())

with st.sidebar:
    st.header("Filters")
    start_date, end_date = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    selected_products = st.multiselect(
        "Products",
        options=all_products,
        default=all_products,
    )
    customer_input = st.text_input(
        "Customer ID (optional)",
        placeholder="Leave blank for all customers",
    )

if isinstance(start_date, tuple):
    start_date, end_date = start_date
else:
    end_date = start_date

customer_id = None
if customer_input.strip():
    try:
        customer_id = int(customer_input.strip())
    except ValueError:
        st.error("Customer ID must be a whole number.")
        st.stop()

filtered = filter_data(df, start_date, end_date, selected_products, customer_id)

total_revenue = filtered["revenue"].sum()
order_count = len(filtered)
avg_order_value = filtered["revenue"].mean() if order_count else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Order Count", f"{order_count:,}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

st.subheader("Daily Revenue Trend")
if order_count:
    daily_revenue = (
        filtered.groupby(filtered["date"].dt.date)["revenue"]
        .sum()
        .reset_index(name="revenue")
    )
    daily_revenue.columns = ["date", "revenue"]
    daily_revenue = daily_revenue.set_index("date")
    st.line_chart(daily_revenue)
else:
    st.info("No orders match the selected filters.")

# streamlit run revenue_explorer.py

import streamlit as st
import pandas as pd

from generate_sales_report import load_and_clean_data

st.set_page_config(page_title="Revenue Explorer", layout="wide")

st.title("Revenue Explorer")


@st.cache_data
def get_data():
    return load_and_clean_data()


df = get_data()

with st.sidebar:
    st.header("Filters")

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    products = sorted(df["product"].unique())
    selected_products = st.multiselect("Products", options=products, default=products)

    customer_filter = st.text_input("Customer ID (optional)", value="")

filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["date"].dt.date >= start_date)
        & (filtered["date"].dt.date <= end_date)
    ]
elif date_range:
    filtered = filtered[filtered["date"].dt.date == date_range]

if selected_products:
    filtered = filtered[filtered["product"].isin(selected_products)]

if customer_filter.strip():
    try:
        customer_id = int(customer_filter.strip())
        filtered = filtered[filtered["customer_id"] == customer_id]
    except ValueError:
        st.sidebar.warning("Enter a valid numeric customer ID.")

total_revenue = filtered["revenue"].sum()
order_count = len(filtered)
avg_order_value = filtered["revenue"].mean() if order_count else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Order Count", f"{order_count:,}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

st.subheader("Daily Revenue Trend")
daily_revenue = (
    filtered.groupby(filtered["date"].dt.date)["revenue"]
    .sum()
    .sort_index()
)
st.line_chart(daily_revenue)

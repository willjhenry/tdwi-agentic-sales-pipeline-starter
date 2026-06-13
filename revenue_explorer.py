# streamlit run revenue_explorer.py

import streamlit as st
import pandas as pd

from generate_sales_report import load_and_clean_data


@st.cache_data
def get_data():
    return load_and_clean_data()


df = get_data()

st.set_page_config(page_title="Revenue Explorer", layout="wide")
st.title("Revenue Explorer")

st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

products = st.sidebar.multiselect(
    "Product",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique()),
)

customer_id_input = st.sidebar.text_input("Customer ID (optional)")

filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["date"].dt.date >= start_date)
        & (filtered["date"].dt.date <= end_date)
    ]
elif date_range:
    filtered = filtered[filtered["date"].dt.date == date_range]

if products:
    filtered = filtered[filtered["product"].isin(products)]

if customer_id_input.strip():
    try:
        customer_id = int(customer_id_input.strip())
        filtered = filtered[filtered["customer_id"] == customer_id]
    except ValueError:
        st.sidebar.warning("Customer ID must be a whole number.")

total_revenue = filtered["revenue"].sum()
order_count = len(filtered)
avg_order_value = total_revenue / order_count if order_count > 0 else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Order Count", f"{order_count:,}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

st.subheader("Daily Revenue Trend")

if order_count > 0:
    daily_revenue = (
        filtered.groupby(filtered["date"].dt.date)["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"date": "Date", "revenue": "Revenue"})
        .set_index("Date")
    )
    st.line_chart(daily_revenue)
else:
    st.info("No data matches the selected filters.")

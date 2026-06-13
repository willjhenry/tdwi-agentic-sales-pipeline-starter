# streamlit run revenue_explorer.py

import streamlit as st

from generate_sales_report import load_and_clean_data

st.set_page_config(page_title="Revenue Explorer", layout="wide")
st.title("Revenue Explorer")

df = load_and_clean_data()

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
    selected_products = st.multiselect(
        "Products",
        options=products,
        default=products,
    )

    customer_options = ["All"] + sorted(df["customer_id"].unique().astype(str).tolist())
    selected_customer = st.selectbox("Customer ID", options=customer_options)

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
else:
    filtered = filtered.iloc[0:0]

if selected_customer != "All":
    filtered = filtered[filtered["customer_id"].astype(str) == selected_customer]

total_revenue = filtered["revenue"].sum()
order_count = len(filtered)
avg_order_value = filtered["revenue"].mean() if order_count > 0 else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Order Count", f"{order_count:,}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

st.subheader("Daily Revenue Trend")

if order_count > 0:
    daily_revenue = filtered.groupby(filtered["date"].dt.date)["revenue"].sum()
    st.bar_chart(daily_revenue)
else:
    st.info("No data matches the selected filters.")

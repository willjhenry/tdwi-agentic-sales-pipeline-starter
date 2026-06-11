# streamlit run revenue_explorer.py
import streamlit as st
import pandas as pd

from generate_sales_report import load_and_clean_data


@st.cache_data
def get_data():
    return load_and_clean_data()


def apply_filters(df, start_date, end_date, products, customer_id):
    mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
    if products:
        mask &= df["product"].isin(products)
    if customer_id is not None:
        mask &= df["customer_id"] == customer_id
    return df[mask]


def main():
    st.title("Revenue Explorer")

    df = get_data()
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    with st.sidebar:
        st.header("Filters")
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        products = st.multiselect(
            "Product",
            options=sorted(df["product"].unique()),
            default=sorted(df["product"].unique()),
        )
        customer_input = st.text_input("Customer ID (optional)", value="")
        customer_id = None
        if customer_input.strip():
            try:
                customer_id = int(customer_input.strip())
            except ValueError:
                st.warning("Customer ID must be a number.")

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    filtered = apply_filters(df, start_date, end_date, products, customer_id)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${filtered['revenue'].sum():,.2f}")
    col2.metric("Order Count", f"{len(filtered):,}")
    avg_order = filtered["revenue"].mean() if len(filtered) > 0 else 0.0
    col3.metric("Average Order Value", f"${avg_order:,.2f}")

    st.subheader("Daily Revenue Trend")
    if filtered.empty:
        st.info("No data matches the selected filters.")
    else:
        daily = (
            filtered.groupby(filtered["date"].dt.date)["revenue"]
            .sum()
            .reset_index()
            .rename(columns={"date": "Date", "revenue": "Revenue"})
        )
        daily = daily.set_index("Date")
        st.line_chart(daily)


if __name__ == "__main__":
    main()

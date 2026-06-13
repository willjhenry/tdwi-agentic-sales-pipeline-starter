# streamlit run revenue_explorer.py
import streamlit as st

from generate_sales_report import daily_revenue, load_and_clean_data


@st.cache_data
def get_data():
    return load_and_clean_data()


def normalize_date_range(start_date, end_date):
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    return start_date, end_date


def parse_date_range(date_range, min_date, max_date):
    if isinstance(date_range, (tuple, list)):
        if len(date_range) == 2:
            return normalize_date_range(date_range[0], date_range[1])
        if len(date_range) == 1:
            return date_range[0], date_range[0]
        return min_date, max_date
    if date_range is None:
        return min_date, max_date
    return date_range, date_range


def parse_customer_id(customer_input):
    text = customer_input.strip()
    if not text:
        return None, True
    try:
        return int(text), True
    except ValueError:
        return None, False


def apply_filters(df, start_date, end_date, products, customer_id):
    start_date, end_date = normalize_date_range(start_date, end_date)
    mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
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
        if not products:
            st.warning("Select at least one product.")
        customer_input = st.text_input("Customer ID (optional)", value="")
        customer_id, customer_id_valid = parse_customer_id(customer_input)
        if not customer_id_valid:
            st.warning("Customer ID must be a number.")

    start_date, end_date = parse_date_range(date_range, min_date, max_date)

    if customer_id_valid:
        filtered = apply_filters(df, start_date, end_date, products, customer_id)
    else:
        filtered = df.iloc[0:0]

    col1, col2, col3 = st.columns(3)
    if not customer_id_valid:
        col1.metric("Total Revenue", "—")
        col2.metric("Order Count", "—")
        col3.metric("Average Order Value", "—")
        st.error("Enter a numeric Customer ID or clear the field to see results.")
    elif not products:
        col1.metric("Total Revenue", "—")
        col2.metric("Order Count", "—")
        col3.metric("Average Order Value", "—")
    else:
        col1.metric("Total Revenue", f"${filtered['revenue'].sum():,.2f}")
        col2.metric("Order Count", f"{len(filtered):,}")
        avg_order = filtered["revenue"].mean() if len(filtered) > 0 else 0.0
        col3.metric("Average Order Value", f"${avg_order:,.2f}")

    st.subheader("Daily Revenue Trend")
    if not customer_id_valid:
        pass
    elif not products:
        st.info("Select at least one product to see results.")
    elif filtered.empty:
        st.info("No data matches the selected filters.")
    else:
        daily = (
            daily_revenue(filtered)
            .reset_index()
            .rename(columns={"date": "Date", "revenue": "Revenue"})
        )
        daily = daily.set_index("Date")
        st.line_chart(daily)


if __name__ == "__main__":
    main()

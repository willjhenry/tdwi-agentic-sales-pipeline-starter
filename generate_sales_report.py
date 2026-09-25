import pandas as pd
import matplotlib.pyplot as plt
import os


def load_and_clean_data():
    df = pd.read_csv("data/messy_sales_data.csv")
    df["date"] = pd.to_datetime(df["date"], format="mixed")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["date", "quantity", "price"])
    df = df.drop_duplicates()
    df["revenue"] = df["price"] * df["quantity"]
    return df


def filter_sales(df, start_date, end_date, products, customer_id=None):
    """Return rows on the selected calendar days, for the selected products, and optionally one customer.

    The end date is the whole day, so a timestamp later that day stays included.
    """
    start = pd.Timestamp(start_date).normalize()
    end = pd.Timestamp(end_date).normalize()
    order_day = df["date"].dt.normalize()
    filtered = df.loc[order_day.between(start, end, inclusive="both")]
    filtered = filtered.loc[filtered["product"].isin(products)]
    if customer_id is not None and str(customer_id).strip() != "":
        customer_key = str(customer_id).strip()
        filtered = filtered.loc[filtered["customer_id"].astype(str) == customer_key]
    return filtered


def summarize_sales(df):
    """Total revenue, order count, and average order value for the given rows."""
    order_count = int(len(df))
    if order_count == 0:
        return 0.0, 0, 0.0
    total_revenue = float(df["revenue"].sum())
    average_order_value = float(df["revenue"].mean())
    return total_revenue, order_count, average_order_value


def daily_revenue(df):
    """Revenue summed by order date, sorted chronologically."""
    if df.empty:
        return pd.Series(dtype="float64", name="revenue")
    return df.groupby("date")["revenue"].sum().sort_index().rename("revenue")


def generate_metrics(df):
    total_revenue, _, avg_order_value = summarize_sales(df)
    top_customers = df.groupby("customer_id")["revenue"].sum().nlargest(5)
    return total_revenue, top_customers, avg_order_value


def create_chart(df):
    daily = daily_revenue(df)
    if not daily.empty:
        daily.index = daily.index.strftime("%Y-%m-%d")
    plt.figure(figsize=(10, 6))
    daily.plot(kind="bar")
    plt.title("Daily Revenue Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig("report.png")
    plt.close()


def mock_encrypt_export(df, secret_key):
    # Uses the secret (REPORT_EXPORT_KEY)
    os.makedirs("output", exist_ok=True)
    encrypted_file = "output/encrypted_sales_report.csv"
    df.to_csv(encrypted_file, index=False)
    if secret_key:
        print(f"Exported encrypted report using secret: {secret_key[:4]}...")
    else:
        print("Exported sales report CSV")


def main():
    df = load_and_clean_data()
    total, top, avg = generate_metrics(df)
    create_chart(df)

    secret_key = os.getenv("REPORT_EXPORT_KEY")
    mock_encrypt_export(df, secret_key)

    print("Report generated!")
    print(f"Total Revenue: ${total:,.2f}")
    print(f"Avg Order Value: ${avg:,.2f}")
    print(f"Top Customers:\n{top}")


if __name__ == "__main__":
    main()

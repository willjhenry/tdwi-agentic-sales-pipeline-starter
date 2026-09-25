import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "messy_sales_data.csv"


def load_and_clean_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df = df.drop_duplicates().reset_index(drop=True)
    df["date"] = pd.to_datetime(df["date"], format="mixed").dt.normalize()
    df["quantity"] = pd.to_numeric(df["quantity"])
    df["price"] = pd.to_numeric(df["price"])
    df["revenue"] = df["price"] * df["quantity"]
    return df


def filter_sales(df, start, end, products, customer_id=None):
    start_ts, end_ts = sorted((pd.Timestamp(start), pd.Timestamp(end)))
    filtered = df.loc[df["date"].between(start_ts, end_ts)]
    if products is not None:
        filtered = filtered.loc[filtered["product"].isin(products)]
    if customer_id is not None:
        filtered = filtered.loc[filtered["customer_id"] == int(customer_id)]
    return filtered


def sales_kpis(df):
    total_revenue = df["revenue"].sum()
    order_count = len(df)
    avg_order_value = df["revenue"].mean()
    if pd.isna(avg_order_value):
        avg_order_value = 0.0
    return total_revenue, order_count, avg_order_value


def daily_revenue(df):
    return df.groupby("date")["revenue"].sum().sort_index()


def generate_metrics(df):
    total_revenue, _, avg_order_value = sales_kpis(df)
    top_customers = df.groupby("customer_id")["revenue"].sum().nlargest(5)
    return total_revenue, top_customers, avg_order_value


def create_chart(df):
    trend = daily_revenue(df)
    labels = trend.index.strftime("%Y-%m-%d")
    plt.figure(figsize=(10, 6))
    plt.bar(labels, trend.to_numpy())
    plt.title("Daily Revenue Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("report.png")
    plt.close()


def mock_encrypt_export(df, secret_key):
    # Uses the secret (REPORT_EXPORT_KEY)
    encrypted_file = "output/encrypted_sales_report.csv"
    df.to_csv(encrypted_file, index=False)
    print(f"Exported encrypted report using secret: {secret_key[:4]}...")


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

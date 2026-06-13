import pandas as pd
import matplotlib.pyplot as plt
import os


def load_and_clean_data():
    df = pd.read_csv("data/messy_sales_data.csv")

    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"], format="mixed")
    df["revenue"] = df["price"] * df["quantity"]

    return df


def generate_metrics(df):
    total_revenue = df["revenue"].sum()
    top_customers = df.groupby("customer_id")["revenue"].sum().nlargest(5)
    avg_order_value = df["revenue"].mean()
    return total_revenue, top_customers, avg_order_value


def daily_revenue(df):
    return df.groupby(df["date"].dt.date)["revenue"].sum()


def create_chart(df):
    plt.figure(figsize=(10, 6))
    daily_revenue(df).plot(kind="bar")
    plt.title("Daily Revenue Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig("report.png")
    plt.close()


def mock_encrypt_export(df, secret_key):
    # Uses the secret (REPORT_EXPORT_KEY)
    encrypted_file = "output/encrypted_sales_report.csv"
    os.makedirs(os.path.dirname(encrypted_file), exist_ok=True)
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

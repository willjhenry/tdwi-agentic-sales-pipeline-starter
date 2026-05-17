"""
Generate Sales Report — TDWI Agentic Code Generation Lab 3
Reads messy e-commerce sales data, cleans it, and produces a summary report chart.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "messy_sales_data.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load raw CSV data."""
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean messy sales data:
    - Drop rows with missing product names
    - Fill missing categories with 'Unknown'
    - Fill missing customer regions with 'Unknown'
    - Convert unit_price to numeric (coerce errors)
    - Parse order_date with mixed formats
    - Remove rows with non-positive quantity or unit_price
    """
    df = df.copy()

    df = df.dropna(subset=["product"])
    df["product"] = df["product"].str.strip()

    df["category"] = df["category"].fillna("Unknown")
    df["customer_region"] = df["customer_region"].fillna("Unknown")

    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["unit_price"])

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=False)

    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] > 0]

    df["total_sales"] = df["quantity"] * df["unit_price"]

    return df.reset_index(drop=True)


def generate_report(df: pd.DataFrame, output_dir: str = OUTPUT_DIR) -> str:
    """Generate a bar chart of total sales by product and save to output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    sales_by_product = df.groupby("product")["total_sales"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sales_by_product.plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title("Total Sales by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Sales ($)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    chart_path = os.path.join(output_dir, "sales_report.png")
    fig.savefig(chart_path, dpi=100)
    plt.close(fig)

    print(f"Sales report chart saved to: {chart_path}")
    return chart_path


def main():
    print("Loading data...")
    raw_df = load_data()
    print(f"  Loaded {len(raw_df)} rows")

    print("Cleaning data...")
    clean_df = clean_data(raw_df)
    print(f"  {len(clean_df)} rows after cleaning")

    print("Generating report...")
    chart_path = generate_report(clean_df)
    print("Done!")

    summary = clean_df.groupby("product")["total_sales"].sum().sort_values(ascending=False)
    print("\n--- Sales Summary ---")
    for product, total in summary.items():
        print(f"  {product}: ${total:,.2f}")
    print(f"\n  Grand Total: ${summary.sum():,.2f}")


if __name__ == "__main__":
    main()

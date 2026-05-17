"""Tests for the sales report pipeline."""

import os
import pandas as pd
import pytest

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.generate_sales_report import load_data, clean_data, generate_report


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "messy_sales_data.csv")


class TestLoadData:
    def test_load_returns_dataframe(self):
        df = load_data(DATA_PATH)
        assert isinstance(df, pd.DataFrame)

    def test_load_has_expected_columns(self):
        df = load_data(DATA_PATH)
        expected = {"order_id", "product", "category", "quantity", "unit_price", "order_date", "customer_region"}
        assert expected == set(df.columns)

    def test_load_has_100_rows(self):
        df = load_data(DATA_PATH)
        assert len(df) == 100


class TestCleanData:
    @pytest.fixture
    def raw_df(self):
        return load_data(DATA_PATH)

    @pytest.fixture
    def clean_df(self, raw_df):
        return clean_data(raw_df)

    def test_no_missing_products(self, clean_df):
        assert clean_df["product"].notna().all()

    def test_no_missing_categories(self, clean_df):
        assert clean_df["category"].notna().all()

    def test_no_negative_quantities(self, clean_df):
        assert (clean_df["quantity"] > 0).all()

    def test_no_negative_prices(self, clean_df):
        assert (clean_df["unit_price"] > 0).all()

    def test_total_sales_column_exists(self, clean_df):
        assert "total_sales" in clean_df.columns

    def test_total_sales_positive(self, clean_df):
        assert (clean_df["total_sales"] > 0).all()

    def test_dates_parsed(self, clean_df):
        assert pd.api.types.is_datetime64_any_dtype(clean_df["order_date"])

    def test_fewer_rows_after_cleaning(self, raw_df, clean_df):
        assert len(clean_df) < len(raw_df)


class TestGenerateReport:
    def test_chart_file_created(self, tmp_path):
        raw_df = load_data(DATA_PATH)
        clean_df = clean_data(raw_df)
        chart_path = generate_report(clean_df, output_dir=str(tmp_path))
        assert os.path.exists(chart_path)
        assert chart_path.endswith(".png")

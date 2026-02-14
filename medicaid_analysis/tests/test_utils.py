"""Tests for the utils package — config, formatting, I/O, and DB helpers."""

import pytest
from pathlib import Path


class TestConfig:
    """Verify configuration constants and paths."""

    def test_base_dir_exists(self):
        from utils import BASE_DIR
        assert BASE_DIR.exists()
        assert BASE_DIR.is_dir()

    def test_data_dir_exists(self):
        from utils import DATA_DIR
        assert DATA_DIR.exists()

    def test_output_dirs_configurable(self):
        from utils import OUTPUT_DIR, PLOTS_DIR
        assert isinstance(OUTPUT_DIR, Path)
        assert isinstance(PLOTS_DIR, Path)

    def test_csv_paths_defined(self):
        from utils import FULL_CSV, SAMPLE_CSV
        assert FULL_CSV.name == "medicaid-provider-spending.csv"
        assert SAMPLE_CSV.name == "sample.csv"


class TestFormatting:
    """Verify formatting functions produce valid output."""

    def test_usd_fmt_positive(self):
        from utils import usd_fmt
        result = usd_fmt(1234567.89, None)
        assert "$" in result
        assert "1" in result

    def test_usd_fmt_zero(self):
        from utils import usd_fmt
        result = usd_fmt(0, None)
        assert "$" in result

    def test_usd_fmt_negative(self):
        from utils import usd_fmt
        result = usd_fmt(-500, None)
        assert "$" in result or "-" in result

    def test_num_fmt(self):
        from utils import num_fmt
        result = num_fmt(1000000, None)
        assert "M" in result or "1" in result

    def test_pct_fmt(self):
        from utils import pct_fmt
        result = pct_fmt(0.5, None)
        assert "%" in result or "50" in result


class TestDatabase:
    """Verify DuckDB connection and query functions."""

    def test_connect_returns_connection(self):
        from utils import connect
        con = connect()
        assert con is not None
        result = con.execute("SELECT 1 AS test").fetchone()
        assert result[0] == 1
        con.close()

    def test_query_returns_dataframe(self):
        from utils import connect, query
        con = connect()
        df = query(con, "SELECT 42 AS value, 'hello' AS text")
        assert len(df) == 1
        assert df.iloc[0]["value"] == 42
        assert df.iloc[0]["text"] == "hello"
        con.close()

    def test_query_with_csv(self):
        """Test querying a real CSV file (uses sample data)."""
        from utils import connect, query, SAMPLE_CSV
        if not SAMPLE_CSV.exists():
            pytest.skip("Sample CSV not available")
        con = connect()
        df = query(con, f"SELECT COUNT(*) AS n FROM '{SAMPLE_CSV}' LIMIT 1")
        assert len(df) == 1
        assert df.iloc[0]["n"] > 0
        con.close()


class TestIO:
    """Verify I/O helper functions."""

    def test_banner_runs(self, capsys):
        from utils import banner
        banner(1, "Test Section")
        # banner uses logging, not print

    def test_savefig_creates_file(self, tmp_path):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from utils import savefig, PLOTS_DIR

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        PLOTS_DIR.mkdir(parents=True, exist_ok=True)
        savefig(fig, "test_savefig_output.png")
        path = PLOTS_DIR / "test_savefig_output.png"
        assert path.exists()
        path.unlink()  # cleanup
        plt.close(fig)

    def test_save_csv_creates_file(self, tmp_path):
        import pandas as pd
        from utils import save_csv, OUTPUT_DIR

        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        save_csv(df, "test_save_csv_output.csv")
        path = OUTPUT_DIR / "test_save_csv_output.csv"
        assert path.exists()
        loaded = pd.read_csv(path)
        assert len(loaded) == 2
        path.unlink()  # cleanup

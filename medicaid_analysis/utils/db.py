"""
Medicaid Analysis — DuckDB Database Helpers
"""

import duckdb
import pandas as pd


def connect() -> duckdb.DuckDBPyConnection:
    """Create an in-memory DuckDB connection."""
    return duckdb.connect(database=":memory:")


def query(con, sql: str) -> pd.DataFrame:
    """Execute SQL against a DuckDB connection and return a pandas DataFrame."""
    return con.execute(sql).fetchdf()

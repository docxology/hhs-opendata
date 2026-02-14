"""Integration tests that run actual analysis sections on real sample data."""

import pytest
import pandas as pd
from pathlib import Path
from utils import connect, SAMPLE_CSV, OUTPUT_DIR, PLOTS_DIR


@pytest.fixture(scope="module")
def data_csv():
    """Provide path to sample CSV or skip if unavailable."""
    if not SAMPLE_CSV.exists():
        pytest.skip("Sample CSV not available — run create_sample.py first")
    return str(SAMPLE_CSV)


@pytest.fixture(scope="module")
def con():
    """Provide a DuckDB connection."""
    c = connect()
    yield c
    c.close()


@pytest.fixture(autouse=True)
def ensure_dirs():
    """Ensure output directories exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    (PLOTS_DIR / "fraud").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "fraud").mkdir(parents=True, exist_ok=True)


class TestEDASections:
    """Test EDA sections run and produce output."""

    def test_s01_eda(self, con, data_csv):
        from eda import s01_eda
        result = s01_eda(con, data_csv)
        assert result is not None

    def test_s02_monthly_trends(self, con, data_csv):
        from eda import s02_monthly_trends
        s02_monthly_trends(con, data_csv)
        assert (PLOTS_DIR / "02_yearly_spending.png").exists()

    def test_s03_top_procedures(self, con, data_csv):
        from eda import s03_top_procedures
        s03_top_procedures(con, data_csv)
        assert (OUTPUT_DIR / "03_top_procedures.csv").exists()

    def test_s04_top_providers(self, con, data_csv):
        from eda import s04_top_providers
        s04_top_providers(con, data_csv)
        assert (OUTPUT_DIR / "04_top_providers.csv").exists()

    def test_s05_cost_efficiency(self, con, data_csv):
        from eda import s05_cost_efficiency
        cost_df = s05_cost_efficiency(con, data_csv)
        assert isinstance(cost_df, pd.DataFrame)
        assert len(cost_df) > 0
        assert "cost_per_claim" in cost_df.columns


class TestStatsSections:
    """Test stats sections."""

    @pytest.fixture(scope="class")
    def cost_df(self, con, data_csv):
        from eda import s05_cost_efficiency
        return s05_cost_efficiency(con, data_csv)

    def test_s06_anomaly_detection(self, con, data_csv, cost_df):
        from stats import s06_anomaly_detection
        s06_anomaly_detection(con, data_csv, cost_df)
        assert (OUTPUT_DIR / "06a_anomalies_zscore.csv").exists()

    def test_s08_concentration(self, con, data_csv):
        from stats import s08_concentration
        s08_concentration(con, data_csv)
        assert (OUTPUT_DIR / "08_concentration_metrics.csv").exists()

    def test_s15_power_law(self, con, data_csv):
        from stats import s15_power_law
        s15_power_law(con, data_csv)
        assert (PLOTS_DIR / "15_power_law.png").exists()

    def test_s18_spending_deciles(self, con, data_csv):
        from stats import s18_spending_deciles
        s18_spending_deciles(con, data_csv)
        assert (OUTPUT_DIR / "18_spending_deciles.csv").exists()

    def test_s31_benfords_law(self, con, data_csv):
        from stats import s31_benfords_law
        s31_benfords_law(con, data_csv)
        assert (PLOTS_DIR / "31_benfords_law.png").exists()


class TestFraudSections:
    """Test fraud detection sections."""

    def test_s33_upcoding_detection(self, con, data_csv):
        from fraud import s33_upcoding_detection
        result = s33_upcoding_detection(con, data_csv)
        assert isinstance(result, pd.DataFrame)
        assert (OUTPUT_DIR / "fraud" / "33_upcoding_flagged.csv").exists()

    def test_s34_billing_velocity(self, con, data_csv):
        from fraud import s34_billing_velocity_anomalies
        result = s34_billing_velocity_anomalies(con, data_csv)
        assert isinstance(result, pd.DataFrame)
        assert (OUTPUT_DIR / "fraud" / "34_velocity_anomalies.csv").exists()

    def test_s35_phantom_billing(self, con, data_csv):
        from fraud import s35_phantom_billing
        result = s35_phantom_billing(con, data_csv)
        assert isinstance(result, pd.DataFrame)
        assert (OUTPUT_DIR / "fraud" / "35_phantom_records.csv").exists()

    def test_s36_provider_clustering(self, con, data_csv):
        from fraud import s36_provider_clustering
        result = s36_provider_clustering(con, data_csv)
        assert isinstance(result, pd.DataFrame)

    def test_s37_cost_outliers(self, con, data_csv):
        from fraud import s37_cost_outliers_by_procedure
        result = s37_cost_outliers_by_procedure(con, data_csv)
        assert isinstance(result, pd.DataFrame)

    def test_s39_temporal_anomalies(self, con, data_csv):
        from fraud import s39_temporal_anomalies
        result = s39_temporal_anomalies(con, data_csv)
        assert isinstance(result, pd.DataFrame)

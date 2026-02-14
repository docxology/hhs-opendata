"""Tests for all 8 subpackage imports and function signatures."""

import pytest
import inspect


# All 40 section functions with their expected parameters
SECTION_REGISTRY = {
    # eda
    "eda.s01_eda": ["con", "csv"],
    "eda.s02_monthly_trends": ["con", "csv"],
    "eda.s03_top_procedures": ["con", "csv"],
    "eda.s04_top_providers": ["con", "csv"],
    "eda.s05_cost_efficiency": ["con", "csv"],
    "eda.s12_high_value_claims": ["con", "csv"],
    # stats
    "stats.s06_anomaly_detection": ["con", "csv", "cost_df"],
    "stats.s08_concentration": ["con", "csv"],
    "stats.s09_correlations": ["con", "csv", "cost_df"],
    "stats.s15_power_law": ["con", "csv"],
    "stats.s17_statistical_tests": ["con", "csv", "cost_df"],
    "stats.s18_spending_deciles": ["con", "csv"],
    "stats.s31_benfords_law": ["con", "csv"],
    # providers
    "providers.s07_billing_vs_servicing": ["con", "csv"],
    "providers.s10_procedure_diversity": ["con", "csv"],
    "providers.s13_provider_growth": ["con", "csv"],
    "providers.s16_provider_network": ["con", "csv"],
    "providers.s24_provider_tenure": ["con", "csv"],
    "providers.s27_provider_specialization": ["con", "csv"],
    "providers.s29_market_share_dynamics": ["con", "csv"],
    # procedures
    "procedures.s14_hcpcs_categories": ["con", "csv"],
    "procedures.s23_procedure_cooccurrence": ["con", "csv"],
    "procedures.s26_claims_size_distribution": ["con", "csv"],
    "procedures.s30_hcpcs_lifecycle": ["con", "csv"],
    # temporal
    "temporal.s11_temporal_patterns": ["con", "csv"],
    "temporal.s19_beneficiary_intensity": ["con", "csv"],
    "temporal.s21_rolling_cumulative": ["con", "csv"],
    "temporal.s22_yoy_comparison": ["con", "csv"],
    "temporal.s25_spending_velocity": ["con", "csv"],
    # visualization
    "visualization.s20_distribution_deep_dive": ["con", "csv", "cost_df"],
    "visualization.s28_outlier_profiles": ["con", "csv", "cost_df"],
    "visualization.s32_executive_summary": ["con", "csv", "eda", "yoy_totals"],
    # fraud
    "fraud.s33_upcoding_detection": ["con", "csv"],
    "fraud.s34_billing_velocity_anomalies": ["con", "csv"],
    "fraud.s35_phantom_billing": ["con", "csv"],
    "fraud.s36_provider_clustering": ["con", "csv"],
    "fraud.s37_cost_outliers_by_procedure": ["con", "csv"],
    "fraud.s38_billing_servicing_anomalies": ["con", "csv"],
    "fraud.s39_temporal_anomalies": ["con", "csv"],
    "fraud.s40_composite_fraud_score": ["con", "csv", "upcoding_df", "velocity_df",
                                         "phantom_df", "cost_outlier_df",
                                         "relationship_df", "temporal_df"],
}


class TestImports:
    """Verify all packages import without errors."""

    @pytest.mark.parametrize("pkg", ["utils", "eda", "stats", "providers",
                                      "procedures", "temporal", "visualization", "fraud"])
    def test_package_imports(self, pkg):
        mod = __import__(pkg)
        assert mod is not None

    def test_main_imports(self):
        import main
        assert hasattr(main, "main")
        assert hasattr(main, "parse_args")
        assert hasattr(main, "run_section")


class TestFunctionSignatures:
    """Verify every section function has the expected parameter signature."""

    @pytest.mark.parametrize("func_path,expected_params", list(SECTION_REGISTRY.items()),
                             ids=list(SECTION_REGISTRY.keys()))
    def test_function_signature(self, func_path, expected_params):
        pkg, func_name = func_path.split(".")
        mod = __import__(pkg)
        func = getattr(mod, func_name)
        assert callable(func), f"{func_path} is not callable"
        sig = inspect.signature(func)
        actual_params = list(sig.parameters.keys())
        assert actual_params == expected_params, (
            f"{func_path}: expected {expected_params}, got {actual_params}"
        )


class TestPackageExports:
    """Verify __init__.py re-exports match expected function counts."""

    EXPECTED_EXPORTS = {
        "eda": 6,
        "stats": 7,
        "providers": 7,
        "procedures": 4,
        "temporal": 5,
        "visualization": 3,
        "fraud": 8,
    }

    @pytest.mark.parametrize("pkg,expected_count", list(EXPECTED_EXPORTS.items()))
    def test_export_count(self, pkg, expected_count):
        mod = __import__(pkg)
        section_funcs = [name for name in dir(mod)
                         if name.startswith("s") and name[1:3].isdigit()]
        assert len(section_funcs) >= expected_count, (
            f"{pkg}: expected ≥{expected_count} section functions, found {len(section_funcs)}: {section_funcs}"
        )

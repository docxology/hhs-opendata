#!/usr/bin/env python3
"""
Medicaid Provider Spending — Modular Analysis Pipeline
======================================================
Orchestrates all 40 analysis sections across 8 subpackages:
  utils, eda, statistics, providers, procedures, temporal, visualization, fraud.

Usage:
    uv run main.py                        # Run all 40 sections
    uv run main.py --sections 1 2 5       # Run specific sections
    uv run main.py --skip-fraud           # Skip fraud sections (33-40)
    uv run main.py --sample               # Use sample dataset
"""

import sys
import time
import argparse
import pandas as pd
from pathlib import Path

from utils import (
    log, connect, query, FULL_CSV, SAMPLE_CSV, OUTPUT_DIR, PLOTS_DIR,
    FULL_ROW_COUNT, FULL_TOTAL_PAID, FULL_TOTAL_CLAIMS,
    FULL_BILLING_NPIS, FULL_SERVICING_NPIS, FULL_HCPCS_CODES,
)

# ── EDA ────────────────────────────────────────────────────────────────────
from eda import (
    s01_eda, s02_monthly_trends, s03_top_procedures, s04_top_providers,
    s05_cost_efficiency, s12_high_value_claims,
)

# ── Statistics ─────────────────────────────────────────────────────────────
from stats import (
    s06_anomaly_detection, s08_concentration, s09_correlations,
    s15_power_law, s17_statistical_tests, s18_spending_deciles,
    s31_benfords_law,
)

# ── Providers ──────────────────────────────────────────────────────────────
from providers import (
    s07_billing_vs_servicing, s10_procedure_diversity, s13_provider_growth,
    s16_provider_network, s24_provider_tenure,
    s27_provider_specialization, s29_market_share_dynamics,
)

# ── Procedures ─────────────────────────────────────────────────────────────
from procedures import (
    s14_hcpcs_categories, s23_procedure_cooccurrence,
    s26_claims_size_distribution, s30_hcpcs_lifecycle,
)

# ── Temporal ───────────────────────────────────────────────────────────────
from temporal import (
    s11_temporal_patterns, s19_beneficiary_intensity,
    s21_rolling_cumulative, s22_yoy_comparison, s25_spending_velocity,
)

# ── Visualization ──────────────────────────────────────────────────────────
from visualization import (
    s20_distribution_deep_dive, s28_outlier_profiles, s32_executive_summary,
)

# ── Fraud Detection ───────────────────────────────────────────────────────
from fraud import (
    s33_upcoding_detection, s34_billing_velocity_anomalies,
    s35_phantom_billing, s36_provider_clustering,
    s37_cost_outliers_by_procedure, s38_billing_servicing_anomalies,
    s39_temporal_anomalies, s40_composite_fraud_score,
)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Medicaid Provider Spending Analysis Pipeline")
    parser.add_argument("--sections", nargs="*", type=int,
                        help="Specific section numbers to run (default: all)")
    parser.add_argument("--skip-fraud", action="store_true",
                        help="Skip fraud detection sections (33-40)")
    parser.add_argument("--sample", action="store_true",
                        help="Use sample dataset instead of full dataset")
    parser.add_argument("--csv", type=str, default=None,
                        help="Path to a specific CSV file to analyse")
    return parser.parse_args()


def should_run(section_num: int, args) -> bool:
    """Decide whether to run a given section based on CLI args."""
    if args.skip_fraud and section_num >= 33:
        return False
    if args.sections is not None:
        return section_num in args.sections
    return True


def run_section(section_num: int, func, *args, **kwargs):
    """Run an analysis section with timing and error handling."""
    t0 = time.time()
    try:
        result = func(*args, **kwargs)
        log.info("  ✓ Section %d completed in %.1fs", section_num, time.time() - t0)
        return result
    except Exception as e:
        log.error("  ✗ Section %d FAILED: %s", section_num, e, exc_info=True)
        return None


def main():
    """Main pipeline orchestrator."""
    args = parse_args()
    t_start = time.time()

    if args.csv:
        csv = args.csv
    elif args.sample:
        csv = str(SAMPLE_CSV)
    else:
        csv = str(FULL_CSV)
    csv_path = Path(csv)
    if not csv_path.exists():
        log.error("Dataset not found: %s", csv)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    (PLOTS_DIR / "fraud").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "fraud").mkdir(parents=True, exist_ok=True)

    log.info("=" * 72)
    log.info("MEDICAID PROVIDER SPENDING — MODULAR ANALYSIS PIPELINE")
    log.info("=" * 72)
    log.info("Dataset: %s", csv_path.name)
    log.info("Output:  %s", OUTPUT_DIR)
    log.info("Plots:   %s", PLOTS_DIR)
    log.info("")

    con = connect()

    # ── Shared state (results passed between sections) ────────────────────
    eda_result = None
    cost_df = None
    yoy_totals = None

    # ── S01–S05: EDA & Core Analysis ─────────────────────────────────────
    if should_run(1, args):
        eda_result = run_section(1, s01_eda, con, csv)
    if should_run(2, args):
        run_section(2, s02_monthly_trends, con, csv)
    if should_run(3, args):
        run_section(3, s03_top_procedures, con, csv)
    if should_run(4, args):
        run_section(4, s04_top_providers, con, csv)
    if should_run(5, args):
        cost_df = run_section(5, s05_cost_efficiency, con, csv)

    # ── S06–S10: Statistical & Provider Analysis ─────────────────────────
    if should_run(6, args):
        if cost_df is not None:
            run_section(6, s06_anomaly_detection, con, csv, cost_df)
        else:
            log.warning("  Skipping S06: requires S05 cost_df (run S05 first)")
    if should_run(7, args):
        run_section(7, s07_billing_vs_servicing, con, csv)
    if should_run(8, args):
        run_section(8, s08_concentration, con, csv)
    if should_run(9, args):
        if cost_df is not None:
            run_section(9, s09_correlations, con, csv, cost_df)
        else:
            log.warning("  Skipping S09: requires S05 cost_df (run S05 first)")
    if should_run(10, args):
        run_section(10, s10_procedure_diversity, con, csv)

    # ── S11–S15: Temporal & Deep Analysis ────────────────────────────────
    if should_run(11, args):
        run_section(11, s11_temporal_patterns, con, csv)
    if should_run(12, args):
        run_section(12, s12_high_value_claims, con, csv)
    if should_run(13, args):
        run_section(13, s13_provider_growth, con, csv)
    if should_run(14, args):
        run_section(14, s14_hcpcs_categories, con, csv)
    if should_run(15, args):
        run_section(15, s15_power_law, con, csv)

    # ── S16–S20: Network & Distributions ─────────────────────────────────
    if should_run(16, args):
        run_section(16, s16_provider_network, con, csv)
    if should_run(17, args):
        if cost_df is not None:
            run_section(17, s17_statistical_tests, con, csv, cost_df)
        else:
            log.warning("  Skipping S17: requires S05 cost_df (run S05 first)")
    if should_run(18, args):
        run_section(18, s18_spending_deciles, con, csv)
    if should_run(19, args):
        run_section(19, s19_beneficiary_intensity, con, csv)
    if should_run(20, args):
        if cost_df is not None:
            run_section(20, s20_distribution_deep_dive, con, csv, cost_df)
        else:
            log.warning("  Skipping S20: requires S05 cost_df (run S05 first)")

    # ── S21–S25: Rolling & Growth ────────────────────────────────────────
    if should_run(21, args):
        run_section(21, s21_rolling_cumulative, con, csv)
    if should_run(22, args):
        yoy_totals = run_section(22, s22_yoy_comparison, con, csv)
    if should_run(23, args):
        run_section(23, s23_procedure_cooccurrence, con, csv)
    if should_run(24, args):
        run_section(24, s24_provider_tenure, con, csv)
    if should_run(25, args):
        run_section(25, s25_spending_velocity, con, csv)

    # ── S26–S32: Size, Specialization & Summaries ────────────────────────
    if should_run(26, args):
        run_section(26, s26_claims_size_distribution, con, csv)
    if should_run(27, args):
        run_section(27, s27_provider_specialization, con, csv)
    if should_run(28, args):
        if cost_df is not None:
            run_section(28, s28_outlier_profiles, con, csv, cost_df)
        else:
            log.warning("  Skipping S28: requires S05 cost_df (run S05 first)")
    if should_run(29, args):
        run_section(29, s29_market_share_dynamics, con, csv)
    if should_run(30, args):
        run_section(30, s30_hcpcs_lifecycle, con, csv)
    if should_run(31, args):
        run_section(31, s31_benfords_law, con, csv)
    if should_run(32, args):
        if eda_result is not None:
            run_section(32, s32_executive_summary, con, csv, eda_result, yoy_totals)
        else:
            log.warning("  Skipping S32: requires S01 eda_result (run S01 first)")

    # ── S33–S40: Fraud Detection ─────────────────────────────────────────
    upcoding_df = velocity_df = phantom_df = None
    cost_outlier_df = relationship_df = temporal_fraud_df = None

    if should_run(33, args):
        upcoding_df = run_section(33, s33_upcoding_detection, con, csv)
    if should_run(34, args):
        velocity_df = run_section(34, s34_billing_velocity_anomalies, con, csv)
    if should_run(35, args):
        phantom_df = run_section(35, s35_phantom_billing, con, csv)
    if should_run(36, args):
        run_section(36, s36_provider_clustering, con, csv)
    if should_run(37, args):
        cost_outlier_df = run_section(37, s37_cost_outliers_by_procedure, con, csv)
    if should_run(38, args):
        relationship_df = run_section(38, s38_billing_servicing_anomalies, con, csv)
    if should_run(39, args):
        temporal_fraud_df = run_section(39, s39_temporal_anomalies, con, csv)
    if should_run(40, args):
        # Composite requires all prior fraud DataFrames
        empty = pd.DataFrame(columns=["BILLING_PROVIDER_NPI_NUM"])
        run_section(40, s40_composite_fraud_score, con, csv,
                   upcoding_df if upcoding_df is not None else empty,
                   velocity_df if velocity_df is not None else empty,
                   phantom_df if phantom_df is not None else empty,
                   cost_outlier_df if cost_outlier_df is not None else empty,
                   relationship_df if relationship_df is not None else empty,
                   temporal_fraud_df if temporal_fraud_df is not None else empty)

    # ── Summary ──────────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    log.info("")
    log.info("=" * 72)
    log.info("PIPELINE COMPLETE — %.1f minutes (%.0f seconds)", elapsed / 60, elapsed)
    log.info("=" * 72)

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

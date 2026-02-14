"""Visualization — Outlier Profiles (Section 28)."""

import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s28_outlier_profiles(con, csv: str, cost_df: pd.DataFrame):
    """Multi-dimensional outlier profiling — extreme records across multiple axes."""
    banner(28, "Outlier Deep-Dive Profiling")

    provider_stats = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
               SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene,
               COUNT(DISTINCT HCPCS_CODE) AS num_codes,
               COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months,
               AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS avg_cost_per_claim,
               MAX(TOTAL_PAID) AS max_single_record
        FROM '{csv}' WHERE TOTAL_CLAIMS > 0 GROUP BY BILLING_PROVIDER_NPI_NUM
    """)

    outlier_flags = pd.DataFrame()
    outlier_flags["BILLING_PROVIDER_NPI_NUM"] = provider_stats["BILLING_PROVIDER_NPI_NUM"]
    for col in ["total_paid", "total_claims", "total_bene", "avg_cost_per_claim", "max_single_record"]:
        threshold = provider_stats[col].quantile(0.995)
        outlier_flags[f"outlier_{col}"] = provider_stats[col] > threshold
    outlier_flags["outlier_count"] = outlier_flags.iloc[:, 1:].sum(axis=1)
    multi_outliers = outlier_flags[outlier_flags["outlier_count"] >= 2].merge(provider_stats)
    multi_outliers = multi_outliers.sort_values("outlier_count", ascending=False)
    multi_outliers.to_csv(OUTPUT_DIR / "28_multi_dim_outliers.csv", index=False)
    log.info("  Multi-dimensional outliers (≥2 axes): %d", len(multi_outliers))
    log.info("  Max outlier dimensions: %d", multi_outliers["outlier_count"].max() if len(multi_outliers) > 0 else 0)

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    ax = axes[0]
    dim_counts = outlier_flags["outlier_count"].value_counts().sort_index()
    ax.bar(dim_counts.index.astype(str), dim_counts.values, color="#ea4335", edgecolor="white")
    ax.set_title("Outlier Dimension Count Distribution", fontsize=13, fontweight="bold")
    ax.set_xlabel("# Outlier Dimensions"); ax.set_ylabel("Provider Count")

    # Downsample for scatter plots to avoid matplotlib cell block overflow
    MAX_SCATTER = 10_000
    plot_df = multi_outliers
    if len(plot_df) > MAX_SCATTER:
        log.info("  Downsampling scatter from %d to %d points", len(plot_df), MAX_SCATTER)
        plot_df = plot_df.head(MAX_SCATTER)  # already sorted by outlier_count desc

    ax = axes[1]
    if len(plot_df) > 0:
        ax.scatter(plot_df["total_claims"], plot_df["total_paid"],
                   c=plot_df["outlier_count"], cmap="Reds", s=20, alpha=0.6, rasterized=True)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title("Multi-Dim Outliers: Claims vs Paid", fontsize=13, fontweight="bold")
        ax.set_xlabel("Total Claims"); ax.set_ylabel("Total Paid"); usd(ax)
    ax = axes[2]
    if len(plot_df) > 0:
        ax.scatter(plot_df["avg_cost_per_claim"], plot_df["total_paid"],
                   c=plot_df["outlier_count"], cmap="Reds", s=20, alpha=0.6, rasterized=True)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title("Multi-Dim Outliers: Cost/Claim vs Paid", fontsize=13, fontweight="bold")
        ax.set_xlabel("Avg Cost per Claim (USD)"); ax.set_ylabel("Total Paid"); usd(ax)
    fig.suptitle("Multi-Dimensional Outlier Profiling", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "28_outlier_profiles.png")
    return multi_outliers

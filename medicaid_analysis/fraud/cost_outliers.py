"""Fraud Detection — Cost Outliers by Procedure (Section 37)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, save_csv, usd, OUTPUT_DIR


def s37_cost_outliers_by_procedure(con, csv: str):
    """Find providers charging far more than peers for the same procedure."""
    banner(37, "Cost Outliers by Procedure (Within-HCPCS)")

    outliers = query(con, f"""
        WITH code_stats AS (
            SELECT HCPCS_CODE,
                   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS median_cpc,
                   PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS q1_cpc,
                   PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS q3_cpc,
                   COUNT(*) AS n
            FROM '{csv}' WHERE TOTAL_CLAIMS > 0 GROUP BY HCPCS_CODE HAVING n >= 30
        )
        SELECT r.BILLING_PROVIDER_NPI_NUM, r.HCPCS_CODE,
               r.TOTAL_PAID / NULLIF(r.TOTAL_CLAIMS, 0) AS provider_cpc,
               cs.median_cpc, cs.q1_cpc, cs.q3_cpc, (cs.q3_cpc - cs.q1_cpc) AS iqr,
               r.TOTAL_PAID, r.TOTAL_CLAIMS
        FROM '{csv}' r JOIN code_stats cs ON r.HCPCS_CODE = cs.HCPCS_CODE WHERE r.TOTAL_CLAIMS > 0
    """)
    outliers["upper_fence"] = outliers["q3_cpc"] + 3 * outliers["iqr"]
    outliers["excess_ratio"] = outliers["provider_cpc"] / outliers["median_cpc"].clip(lower=0.01)
    outliers["flag_cost_outlier"] = (outliers["provider_cpc"] > outliers["upper_fence"]) & (outliers["excess_ratio"] > 3)
    flagged = outliers[outliers["flag_cost_outlier"]].sort_values("excess_ratio", ascending=False)
    provider_agg = flagged.groupby("BILLING_PROVIDER_NPI_NUM").agg(
        flagged_codes=("HCPCS_CODE", "count"), max_excess_ratio=("excess_ratio", "max"),
        total_excess_paid=("TOTAL_PAID", "sum"),
    ).reset_index().sort_values("total_excess_paid", ascending=False)
    save_csv(flagged.head(2000), "37_cost_outlier_records.csv", "fraud")
    save_csv(provider_agg, "37_cost_outlier_providers.csv", "fraud")
    log.info("  Cost outlier records: %d (%d providers)", len(flagged), len(provider_agg))

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Within-HCPCS Cost Outliers", fontsize=15, fontweight="bold", y=1.02)
    ax = axes[0]
    ax.hist(outliers["excess_ratio"].clip(0, 20), bins=100, color="#ea4335", edgecolor="white", alpha=0.85, log=True)
    ax.axvline(3, color="black", linestyle="--", label="3x median threshold"); ax.set_title("Excess Ratio Distribution", fontweight="bold"); ax.legend()
    ax = axes[1]
    if len(provider_agg) > 0:
        top20 = provider_agg.head(20).iloc[::-1]
        ax.barh(range(len(top20)), top20["total_excess_paid"], color="#e8710a", edgecolor="white")
        ax.set_yticks(range(len(top20))); ax.set_yticklabels(top20["BILLING_PROVIDER_NPI_NUM"].astype(str).str[:10], fontsize=7)
        ax.set_title("Top 20 Cost-Outlier Providers", fontweight="bold"); usd(ax, "x")
    ax = axes[2]
    if len(flagged) > 0:
        sample = flagged.head(2000)
        ax.scatter(sample["excess_ratio"], sample["TOTAL_PAID"], alpha=0.2, s=8, color="#9334e6")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title("Excess Ratio vs Total Paid", fontweight="bold"); usd(ax)
    fig.tight_layout(); savefig(fig, "37_cost_outliers.png", "fraud")
    return provider_agg

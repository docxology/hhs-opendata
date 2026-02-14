"""EDA — Cost Efficiency Metrics (Section 5)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s05_cost_efficiency(con, csv: str):
    """Cost per claim and cost per beneficiary distributions and outliers."""
    banner(5, "Cost Efficiency Metrics")

    df = query(con, f"""
        SELECT
            BILLING_PROVIDER_NPI_NUM,
            HCPCS_CODE,
            TOTAL_PAID,
            TOTAL_CLAIMS,
            TOTAL_UNIQUE_BENEFICIARIES,
            TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)               AS cost_per_claim,
            TOTAL_PAID / NULLIF(TOTAL_UNIQUE_BENEFICIARIES, 0) AS cost_per_beneficiary
        FROM '{csv}'
        WHERE TOTAL_CLAIMS > 0 AND TOTAL_UNIQUE_BENEFICIARIES > 0
    """)

    for metric in ["cost_per_claim", "cost_per_beneficiary"]:
        s = df[metric].describe()
        log.info("  %s — mean: $%.2f, median: $%.2f, std: $%.2f",
                 metric, s["mean"], s["50%"], s["std"])

    pcts = df[["cost_per_claim", "cost_per_beneficiary"]].describe(
        percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
    )
    pcts.to_csv(OUTPUT_DIR / "05_cost_efficiency_percentiles.csv")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Cost Efficiency Distributions", fontsize=16, fontweight="bold", y=1.01)

    for i, (metric, color, label) in enumerate([
        ("cost_per_claim",       "#1a73e8", "Cost per Claim"),
        ("cost_per_beneficiary", "#e8710a", "Cost per Beneficiary"),
    ]):
        vals = df[metric].dropna()
        p99 = vals.quantile(0.99)

        ax = axes[i, 0]
        ax.hist(vals.clip(upper=p99), bins=100, color=color, alpha=0.8, edgecolor="white")
        ax.set_title(f"{label} Distribution (≤99th pctl)", fontsize=12, fontweight="bold")
        ax.set_xlabel("USD"); ax.set_ylabel("Frequency"); usd(ax, axis="x")

        ax = axes[i, 1]
        log_vals = np.log10(vals[vals > 0])
        ax.hist(log_vals, bins=100, color=color, alpha=0.8, edgecolor="white")
        ax.set_title(f"{label} (log₁₀ scale)", fontsize=12, fontweight="bold")
        ax.set_xlabel("log₁₀(USD)"); ax.set_ylabel("Frequency")

    fig.tight_layout()
    savefig(fig, "05_cost_distributions.png")
    return df

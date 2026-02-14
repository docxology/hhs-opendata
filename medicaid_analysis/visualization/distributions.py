"""Visualization — Distribution Deep-Dive (Section 20)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import log, banner, query, savefig, OUTPUT_DIR


def s20_distribution_deep_dive(con, csv: str, cost_df: pd.DataFrame):
    """Box plots and violin plots for key metrics by top procedure codes."""
    banner(20, "Distribution Deep-Dive (Box & Violin)")

    top_codes = query(con, f"""
        SELECT HCPCS_CODE, COUNT(*) AS n FROM '{csv}'
        GROUP BY HCPCS_CODE ORDER BY n DESC LIMIT 10
    """)["HCPCS_CODE"].tolist()

    subset = cost_df[cost_df["HCPCS_CODE"].isin(top_codes)].copy()
    subset["log_paid"] = np.log10(subset["TOTAL_PAID"].clip(lower=1))
    subset["log_cpc"] = np.log10(subset["cost_per_claim"].clip(lower=0.01))

    fig, axes = plt.subplots(2, 1, figsize=(16, 14))
    ax = axes[0]
    order = subset.groupby("HCPCS_CODE")["TOTAL_PAID"].median().sort_values(ascending=False).index
    sns.boxplot(data=subset, x="HCPCS_CODE", y="log_paid", order=order,
                ax=ax, palette="viridis", fliersize=1, linewidth=0.8)
    ax.set_title("log10(Total Paid) by Top 10 Procedure Codes", fontsize=14, fontweight="bold")
    ax.set_xlabel("HCPCS Code"); ax.set_ylabel("log10(Total Paid)"); ax.tick_params(axis="x", rotation=45)
    ax = axes[1]
    sns.violinplot(data=subset, x="HCPCS_CODE", y="log_cpc", order=order,
                   ax=ax, palette="magma", inner="quartile", linewidth=0.8, cut=0)
    ax.set_title("log10(Cost per Claim) by Top 10 Procedure Codes", fontsize=14, fontweight="bold")
    ax.set_xlabel("HCPCS Code"); ax.set_ylabel("log10(Cost per Claim)"); ax.tick_params(axis="x", rotation=45)
    fig.suptitle("Spending Distributions by Procedure", fontsize=16, fontweight="bold", y=1.01)
    fig.tight_layout(); savefig(fig, "20_box_violin.png")

    pctl_list = []
    for code in top_codes:
        vals = subset[subset["HCPCS_CODE"] == code]["TOTAL_PAID"]
        desc = vals.describe(percentiles=[0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
        desc["HCPCS_CODE"] = code
        pctl_list.append(desc)
    pctl_df = pd.DataFrame(pctl_list)
    pctl_df.to_csv(OUTPUT_DIR / "20_procedure_percentiles.csv", index=False)
    return subset

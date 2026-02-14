"""Providers — Market Share Dynamics (Section 29)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s29_market_share_dynamics(con, csv: str):
    """How top providers' market shares change over time."""
    banner(29, "Market Share Dynamics")

    top10 = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM ORDER BY total_paid DESC LIMIT 10
    """)["BILLING_PROVIDER_NPI_NUM"].tolist()

    monthly_total = query(con, f"""
        SELECT CLAIM_FROM_MONTH, SUM(TOTAL_PAID) AS market_total
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH
    """)
    monthly_top = query(con, f"""
        SELECT CLAIM_FROM_MONTH, BILLING_PROVIDER_NPI_NUM, SUM(TOTAL_PAID) AS provider_paid
        FROM '{csv}' WHERE BILLING_PROVIDER_NPI_NUM IN ({','.join(f"'{n}'" for n in top10)})
        GROUP BY CLAIM_FROM_MONTH, BILLING_PROVIDER_NPI_NUM ORDER BY CLAIM_FROM_MONTH
    """)
    pivot = monthly_top.pivot_table(index="CLAIM_FROM_MONTH", columns="BILLING_PROVIDER_NPI_NUM",
                                    values="provider_paid", fill_value=0)
    pivot = pivot.merge(monthly_total, on="CLAIM_FROM_MONTH")
    for col in top10:
        if col in pivot.columns:
            pivot[f"share_{col}"] = pivot[col] / pivot["market_total"] * 100
    pivot["CLAIM_FROM_MONTH"] = pd.to_datetime(pivot["CLAIM_FROM_MONTH"])
    pivot = pivot.sort_values("CLAIM_FROM_MONTH")
    top10_cols = [c for c in top10 if c in pivot.columns]
    pivot["top10_combined"] = pivot[top10_cols].sum(axis=1) / pivot["market_total"] * 100
    pivot.to_csv(OUTPUT_DIR / "29_market_share_dynamics.csv", index=False)
    log.info("  Avg top-10 combined share: %.1f%%", pivot["top10_combined"].mean())

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    ax = axes[0]
    ax.plot(pivot["CLAIM_FROM_MONTH"], pivot["top10_combined"], color="#ea4335", linewidth=2.5)
    ax.fill_between(pivot["CLAIM_FROM_MONTH"], pivot["top10_combined"], alpha=0.15, color="#ea4335")
    ax.set_title("Top-10 Providers Combined Market Share", fontsize=14, fontweight="bold")
    ax.set_ylabel("% of Total Spending"); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax = axes[1]
    share_cols = [f"share_{c}" for c in top10_cols[:5] if f"share_{c}" in pivot.columns]
    if share_cols:
        pivot[share_cols].set_index(pivot["CLAIM_FROM_MONTH"]).plot.area(
            ax=ax, alpha=0.65, linewidth=0.5, color=plt.cm.tab10(np.linspace(0, 0.5, len(share_cols))))
        ax.set_title("Top-5 Provider Market Shares Over Time", fontsize=14, fontweight="bold")
        ax.set_ylabel("% Market Share"); ax.legend(fontsize=7, loc="upper left")
    fig.suptitle("Market Share Dynamics", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "29_market_share.png")
    return pivot

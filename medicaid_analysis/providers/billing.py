"""Providers — Billing vs Servicing (Section 7)."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s07_billing_vs_servicing(con, csv: str):
    """Analysis of billing provider vs servicing provider patterns."""
    banner(7, "Billing vs Servicing Provider Analysis")

    billing = query(con, f"""
        SELECT
            CASE WHEN BILLING_PROVIDER_NPI_NUM = SERVICING_PROVIDER_NPI_NUM
                 THEN 'Same' ELSE 'Third-Party' END AS billing_type,
            COUNT(*) AS row_count, SUM(TOTAL_PAID) AS total_paid,
            SUM(TOTAL_CLAIMS) AS total_claims,
            SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene,
            AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS avg_cost_per_claim
        FROM '{csv}' WHERE TOTAL_CLAIMS > 0 GROUP BY billing_type
    """)
    billing.to_csv(OUTPUT_DIR / "07_billing_vs_servicing.csv", index=False)
    log.info("  Breakdown:\n%s", billing.to_string(index=False))

    billing_monthly = query(con, f"""
        SELECT CLAIM_FROM_MONTH,
            CASE WHEN BILLING_PROVIDER_NPI_NUM = SERVICING_PROVIDER_NPI_NUM
                 THEN 'Same' ELSE 'Third-Party' END AS billing_type,
            SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH, billing_type ORDER BY CLAIM_FROM_MONTH
    """)
    billing_monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(billing_monthly["CLAIM_FROM_MONTH"])
    billing_monthly.to_csv(OUTPUT_DIR / "07_billing_monthly_by_type.csv", index=False)

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    colors = ["#1a73e8", "#e8710a"]
    ax = axes[0]
    ax.pie(billing["row_count"], labels=billing["billing_type"],
           autopct="%1.1f%%", colors=colors, startangle=90, textprops={"fontsize": 11})
    ax.set_title("Rows by Billing Type", fontsize=13, fontweight="bold")
    ax = axes[1]
    ax.pie(billing["total_paid"], labels=billing["billing_type"],
           autopct="%1.1f%%", colors=colors, startangle=90, textprops={"fontsize": 11})
    ax.set_title("Spending by Billing Type", fontsize=13, fontweight="bold")
    ax = axes[2]
    for bt, color in zip(["Same", "Third-Party"], colors):
        d = billing_monthly[billing_monthly["billing_type"] == bt]
        ax.plot(d["CLAIM_FROM_MONTH"], d["total_paid"], label=bt, color=color, linewidth=2)
    ax.set_title("Monthly Trend by Billing Type", fontsize=13, fontweight="bold")
    ax.set_ylabel("Total Paid (USD)"); usd(ax); ax.legend(fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.suptitle("Billing vs Servicing Provider", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "07_billing_analysis.png")
    return billing

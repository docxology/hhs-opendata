"""EDA — Monthly & Yearly Spending Trends (Section 2)."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import seaborn as sns
from utils import log, banner, query, savefig, usd, usd_fmt, num_fmt, OUTPUT_DIR


def s02_monthly_trends(con, csv: str):
    """Monthly and yearly spending trend analysis with multiple metrics."""
    banner(2, "Monthly & Yearly Spending Trends")

    monthly = query(con, f"""
        SELECT
            CLAIM_FROM_MONTH,
            SUM(TOTAL_PAID)                              AS total_paid,
            SUM(TOTAL_CLAIMS)                            AS total_claims,
            SUM(TOTAL_UNIQUE_BENEFICIARIES)              AS total_bene,
            COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM)     AS active_providers,
            COUNT(DISTINCT HCPCS_CODE)                   AS active_codes,
            AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0))    AS avg_cost_per_claim,
            AVG(TOTAL_PAID / NULLIF(TOTAL_UNIQUE_BENEFICIARIES, 0)) AS avg_cost_per_bene
        FROM '{csv}'
        WHERE TOTAL_CLAIMS > 0 AND TOTAL_UNIQUE_BENEFICIARIES > 0
        GROUP BY CLAIM_FROM_MONTH
        ORDER BY CLAIM_FROM_MONTH
    """)
    monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly["CLAIM_FROM_MONTH"])
    monthly.to_csv(OUTPUT_DIR / "02_monthly_trends.csv", index=False)
    log.info("  Months in data: %d", len(monthly))

    yearly = query(con, f"""
        SELECT
            EXTRACT(YEAR FROM CAST(CLAIM_FROM_MONTH || '-01' AS DATE)) AS year,
            SUM(TOTAL_PAID)    AS total_paid,
            SUM(TOTAL_CLAIMS)  AS total_claims,
            COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS providers,
            COUNT(DISTINCT HCPCS_CODE) AS codes
        FROM '{csv}'
        GROUP BY year ORDER BY year
    """)
    yearly.to_csv(OUTPUT_DIR / "02_yearly_summary.csv", index=False)

    # ── Plot: 4-panel monthly dashboard ──
    sns.set_theme(style="whitegrid", font_scale=1.05)
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("Medicaid Provider Spending — Monthly Dashboard", fontsize=17, fontweight="bold", y=1.01)

    ax = axes[0, 0]
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["total_paid"], alpha=0.3, color="#1a73e8")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["total_paid"], color="#1a73e8", linewidth=2)
    ax.set_title("Total Paid per Month"); ax.set_ylabel("USD"); usd(ax)

    ax = axes[0, 1]
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["total_claims"], alpha=0.3, color="#e8710a")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["total_claims"], color="#e8710a", linewidth=2)
    ax.set_title("Total Claims per Month"); ax.set_ylabel("Claims")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))

    ax = axes[1, 0]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["active_providers"], color="#34a853", linewidth=2, marker="o", markersize=3)
    ax.set_title("Active Billing Providers per Month"); ax.set_ylabel("Count")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))

    ax = axes[1, 1]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["avg_cost_per_claim"], color="#9334e6", linewidth=2)
    ax.set_title("Avg Cost per Claim (Monthly)"); ax.set_ylabel("USD"); usd(ax)

    for a in axes.flat:
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        a.xaxis.set_major_locator(mdates.YearLocator())

    fig.tight_layout()
    savefig(fig, "01_monthly_dashboard.png")

    # ── Plot: yearly bar chart ──
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(yearly["year"].astype(int).astype(str), yearly["total_paid"],
                  color="#1a73e8", edgecolor="white", linewidth=0.8)
    ax.set_title("Medicaid Spending by Year", fontsize=15, fontweight="bold")
    ax.set_xlabel("Year"); ax.set_ylabel("Total Paid (USD)"); usd(ax)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h, usd_fmt(h),
                ha="center", va="bottom", fontsize=10, fontweight="bold")
    fig.tight_layout()
    savefig(fig, "02_yearly_spending.png")

    return monthly, yearly

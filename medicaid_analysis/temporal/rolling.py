"""Temporal — Rolling & Cumulative Metrics (Section 21)."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, usd, num_fmt, OUTPUT_DIR


def s21_rolling_cumulative(con, csv: str):
    """Rolling averages and cumulative spending curves."""
    banner(21, "Rolling & Cumulative Metrics")

    monthly = query(con, f"""
        SELECT CLAIM_FROM_MONTH, SUM(TOTAL_PAID) AS total_paid,
               SUM(TOTAL_CLAIMS) AS total_claims,
               COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS providers
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH ORDER BY CLAIM_FROM_MONTH
    """)
    monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly["CLAIM_FROM_MONTH"])
    monthly = monthly.sort_values("CLAIM_FROM_MONTH")
    monthly["paid_3m_avg"] = monthly["total_paid"].rolling(3, center=True).mean()
    monthly["paid_6m_avg"] = monthly["total_paid"].rolling(6, center=True).mean()
    monthly["paid_12m_avg"] = monthly["total_paid"].rolling(12, center=True).mean()
    monthly["cumulative_paid"] = monthly["total_paid"].cumsum()
    monthly["paid_std_6m"] = monthly["total_paid"].rolling(6, center=True).std()
    monthly["cv_6m"] = monthly["paid_std_6m"] / monthly["paid_6m_avg"]
    monthly.to_csv(OUTPUT_DIR / "21_rolling_cumulative.csv", index=False)
    log.info("  Total cumulative spending: $%s", f"{monthly['cumulative_paid'].iloc[-1]:,.0f}")

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("Rolling Averages & Cumulative Metrics", fontsize=16, fontweight="bold", y=1.01)
    ax = axes[0, 0]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["total_paid"], alpha=0.3, color="#aaa", label="Monthly")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["paid_3m_avg"], color="#1a73e8", linewidth=2, label="3-mo avg")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["paid_6m_avg"], color="#e8710a", linewidth=2, label="6-mo avg")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["paid_12m_avg"], color="#34a853", linewidth=2.5, label="12-mo avg")
    ax.set_title("Spending with Rolling Averages", fontsize=13, fontweight="bold"); ax.set_ylabel("Total Paid (USD)"); usd(ax); ax.legend(fontsize=9)
    ax = axes[0, 1]
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["cumulative_paid"], alpha=0.3, color="#1a73e8")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["cumulative_paid"], color="#1a73e8", linewidth=2)
    ax.set_title("Cumulative Spending", fontsize=13, fontweight="bold"); ax.set_ylabel("Cumulative Paid (USD)"); usd(ax)
    ax = axes[1, 0]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["cv_6m"], color="#9334e6", linewidth=2)
    ax.set_title("6-Month Rolling Volatility (CV)", fontsize=13, fontweight="bold"); ax.set_ylabel("Coefficient of Variation")
    ax = axes[1, 1]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["providers"], color="#34a853", linewidth=2, marker="o", markersize=3)
    ax.set_title("Active Providers per Month", fontsize=13, fontweight="bold"); ax.set_ylabel("Provider Count")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))
    for a in axes.flat:
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout(); savefig(fig, "21_rolling_cumulative.png")
    return monthly

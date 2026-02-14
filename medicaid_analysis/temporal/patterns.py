"""Temporal — Temporal Patterns & Seasonality (Section 11)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, usd, num_fmt, OUTPUT_DIR


def s11_temporal_patterns(con, csv: str):
    """Day-of-week, month, and seasonal spending patterns."""
    banner(11, "Temporal Patterns & Seasonality")

    monthly = query(con, f"""
        SELECT CLAIM_FROM_MONTH, SUM(TOTAL_PAID) AS total_paid,
               SUM(TOTAL_CLAIMS) AS total_claims,
               COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS providers
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH ORDER BY CLAIM_FROM_MONTH
    """)
    monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly["CLAIM_FROM_MONTH"])
    monthly["month_num"] = monthly["CLAIM_FROM_MONTH"].dt.month
    monthly["year"] = monthly["CLAIM_FROM_MONTH"].dt.year
    monthly["quarter"] = monthly["CLAIM_FROM_MONTH"].dt.quarter

    seasonal = monthly.groupby("month_num").agg(
        avg_paid=("total_paid", "mean"), std_paid=("total_paid", "std"),
        avg_claims=("total_claims", "mean"),
    ).reset_index()
    seasonal["month_name"] = pd.to_datetime(seasonal["month_num"], format="%m").dt.strftime("%b")
    seasonal["seasonal_index"] = seasonal["avg_paid"] / seasonal["avg_paid"].mean() * 100
    seasonal.to_csv(OUTPUT_DIR / "11_seasonal_patterns.csv", index=False)
    log.info("  Strongest month: %s (index=%.1f)",
             seasonal.loc[seasonal["seasonal_index"].idxmax(), "month_name"],
             seasonal["seasonal_index"].max())
    log.info("  Weakest month: %s (index=%.1f)",
             seasonal.loc[seasonal["seasonal_index"].idxmin(), "month_name"],
             seasonal["seasonal_index"].min())

    qtr = monthly.groupby("quarter").agg(avg_paid=("total_paid", "mean")).reset_index()
    qtr["quarter_name"] = "Q" + qtr["quarter"].astype(str)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Temporal Patterns & Seasonality", fontsize=16, fontweight="bold", y=1.01)
    ax = axes[0, 0]
    ax.bar(seasonal["month_name"], seasonal["seasonal_index"], color="#1a73e8", edgecolor="white")
    ax.axhline(100, color="red", linestyle="--", linewidth=1, label="Average=100")
    ax.set_title("Monthly Seasonal Index", fontsize=13, fontweight="bold"); ax.set_ylabel("Seasonal Index"); ax.legend()
    ax = axes[0, 1]
    ax.bar(qtr["quarter_name"], qtr["avg_paid"], color="#e8710a", edgecolor="white")
    ax.set_title("Quarterly Average Spending", fontsize=13, fontweight="bold"); ax.set_ylabel("Avg Total Paid (USD)"); usd(ax)
    ax = axes[1, 0]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["total_paid"], color="#aaa", alpha=0.5, label="Raw")
    rolling = monthly.set_index("CLAIM_FROM_MONTH")["total_paid"].rolling(3, center=True).mean()
    ax.plot(rolling.index, rolling.values, color="#1a73e8", linewidth=2.5, label="3-mo avg")
    ax.set_title("Spending Trend with Seasonal Smoothing", fontsize=13, fontweight="bold"); usd(ax)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y")); ax.legend()
    ax = axes[1, 1]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["providers"], color="#34a853", linewidth=2, marker="o", markersize=3)
    ax.set_title("Active Providers per Month", fontsize=13, fontweight="bold"); ax.set_ylabel("Provider Count")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout(); savefig(fig, "11_temporal_patterns.png")
    return monthly, seasonal

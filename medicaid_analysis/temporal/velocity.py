"""Temporal — Spending Velocity & Acceleration (Section 25)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, usd, num_fmt, OUTPUT_DIR


def s25_spending_velocity(con, csv: str):
    """Spending acceleration — month-over-month velocity and acceleration."""
    banner(25, "Spending Velocity & Acceleration")

    monthly = query(con, f"""
        SELECT CLAIM_FROM_MONTH, SUM(TOTAL_PAID) AS total_paid,
               SUM(TOTAL_CLAIMS) AS total_claims,
               COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS providers
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH ORDER BY CLAIM_FROM_MONTH
    """)
    monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly["CLAIM_FROM_MONTH"])
    monthly["velocity_paid"] = monthly["total_paid"].diff()
    monthly["velocity_claims"] = monthly["total_claims"].diff()
    monthly["accel_paid"] = monthly["velocity_paid"].diff()
    monthly["accel_claims"] = monthly["velocity_claims"].diff()
    monthly["velocity_pct"] = monthly["total_paid"].pct_change() * 100
    monthly["accel_pct"] = monthly["velocity_pct"].diff()
    monthly.to_csv(OUTPUT_DIR / "25_spending_velocity.csv", index=False)
    log.info("  Avg monthly velocity: $%s", f"{monthly['velocity_paid'].mean():,.0f}")
    log.info("  Max acceleration: $%s", f"{monthly['accel_paid'].max():,.0f}")

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("Spending Velocity & Acceleration", fontsize=16, fontweight="bold", y=1.01)
    ax = axes[0, 0]
    ax.bar(monthly["CLAIM_FROM_MONTH"], monthly["velocity_paid"],
           color=np.where(monthly["velocity_paid"] >= 0, "#34a853", "#ea4335"), width=25)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("Monthly Spending Velocity (Δ$)", fontsize=13, fontweight="bold"); ax.set_ylabel("Monthly Change (USD)"); usd(ax)
    ax = axes[0, 1]
    ax.bar(monthly["CLAIM_FROM_MONTH"], monthly["accel_paid"],
           color=np.where(monthly["accel_paid"] >= 0, "#1a73e8", "#9334e6"), width=25)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("Spending Acceleration (ΔΔ$)", fontsize=13, fontweight="bold"); ax.set_ylabel("Acceleration (USD)"); usd(ax)
    ax = axes[1, 0]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["velocity_pct"], color="#e8710a", linewidth=2)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["velocity_pct"],
                    where=monthly["velocity_pct"] >= 0, alpha=0.2, color="#34a853")
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["velocity_pct"],
                    where=monthly["velocity_pct"] < 0, alpha=0.2, color="#ea4335")
    ax.set_title("Monthly Growth Rate (%)", fontsize=13, fontweight="bold"); ax.set_ylabel("% Change")
    ax = axes[1, 1]
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["velocity_claims"], color="#1a73e8", linewidth=2, label="Claims")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("Claims Volume Velocity", fontsize=13, fontweight="bold"); ax.set_ylabel("Monthly Δ Claims")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))
    for a in axes.flat:
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout(); savefig(fig, "25_spending_velocity.png")
    return monthly

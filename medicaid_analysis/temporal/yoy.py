"""Temporal — Year-over-Year Comparison (Section 22)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, usd, num_fmt, OUTPUT_DIR


def s22_yoy_comparison(con, csv: str):
    """Year-over-year comparison of spending, claims, and providers."""
    banner(22, "Year-over-Year Cohort Comparison")

    yearly_monthly = query(con, f"""
        SELECT EXTRACT(YEAR FROM CAST(CLAIM_FROM_MONTH || '-01' AS DATE)) AS year,
               EXTRACT(MONTH FROM CAST(CLAIM_FROM_MONTH || '-01' AS DATE)) AS month_num,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
               COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS providers
        FROM '{csv}' GROUP BY year, month_num ORDER BY year, month_num
    """)
    yearly_monthly["month_name"] = pd.to_datetime(yearly_monthly["month_num"].astype(int), format="%m").dt.strftime("%b")
    yearly_monthly.to_csv(OUTPUT_DIR / "22_yoy_monthly.csv", index=False)

    yearly_totals = yearly_monthly.groupby("year").agg(
        total_paid=("total_paid", "sum"), total_claims=("total_claims", "sum"),
    ).reset_index()
    yearly_totals["paid_yoy_change"] = yearly_totals["total_paid"].pct_change() * 100
    yearly_totals["claims_yoy_change"] = yearly_totals["total_claims"].pct_change() * 100
    yearly_totals.to_csv(OUTPUT_DIR / "22_yoy_totals.csv", index=False)
    log.info("  YoY paid changes:  %s",
             ", ".join([f"{y:.0f}: {c:+.1f}%" for y, c in
                        zip(yearly_totals["year"], yearly_totals["paid_yoy_change"].fillna(0))]))

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("Year-over-Year Comparison", fontsize=16, fontweight="bold", y=1.01)
    years = sorted(yearly_monthly["year"].unique())
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(years)))

    ax = axes[0, 0]
    for yr, color in zip(years, colors):
        d = yearly_monthly[yearly_monthly["year"] == yr]
        ax.plot(d["month_num"], d["total_paid"], "o-", color=color, linewidth=2, markersize=4, label=str(int(yr)))
    ax.set_title("Monthly Spending by Year", fontsize=13, fontweight="bold"); ax.set_xlabel("Month"); ax.set_ylabel("Total Paid (USD)"); usd(ax)
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(["J","F","M","A","M","J","J","A","S","O","N","D"]); ax.legend(fontsize=8, ncol=2)

    ax = axes[0, 1]
    yt = yearly_totals.dropna(subset=["paid_yoy_change"])
    colors_bar = ["#34a853" if v >= 0 else "#ea4335" for v in yt["paid_yoy_change"]]
    ax.bar(yt["year"].astype(int).astype(str), yt["paid_yoy_change"], color=colors_bar, edgecolor="white")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("YoY Spending Growth %", fontsize=13, fontweight="bold"); ax.set_xlabel("Year"); ax.set_ylabel("% Change")
    for i, row in yt.iterrows():
        ax.text(i - yearly_totals.index[0], row["paid_yoy_change"],
                f"{row['paid_yoy_change']:+.1f}%", ha="center",
                va="bottom" if row["paid_yoy_change"] >= 0 else "top", fontsize=9, fontweight="bold")

    ax = axes[1, 0]
    pivot_yr = yearly_monthly.pivot_table(index="month_num", columns="year", values="total_paid")
    pivot_yr.plot.area(ax=ax, alpha=0.6, linewidth=1, stacked=True,
                       color=plt.cm.viridis(np.linspace(0.1, 0.9, len(years))))
    ax.set_title("Stacked Monthly Spending by Year", fontsize=13, fontweight="bold"); ax.set_xlabel("Month"); ax.set_ylabel("Total Paid (USD)"); usd(ax)
    ax.legend(fontsize=8, title="Year")

    ax = axes[1, 1]
    for yr, color in zip(years, plt.cm.plasma(np.linspace(0.1, 0.9, len(years)))):
        d = yearly_monthly[yearly_monthly["year"] == yr]
        ax.plot(d["month_num"], d["total_claims"], "o-", color=color, linewidth=2, markersize=4, label=str(int(yr)))
    ax.set_title("Monthly Claims by Year", fontsize=13, fontweight="bold"); ax.set_xlabel("Month"); ax.set_ylabel("Total Claims")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(["J","F","M","A","M","J","J","A","S","O","N","D"]); ax.legend(fontsize=8, ncol=2)
    fig.tight_layout(); savefig(fig, "22_yoy_comparison.png")
    return yearly_totals

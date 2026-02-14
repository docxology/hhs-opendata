"""Visualization — Executive Summary Dashboard (Section 32)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, usd, usd_fmt, num_fmt, OUTPUT_DIR


def s32_executive_summary(con, csv: str, eda: dict, yoy_totals: pd.DataFrame):
    """Executive summary dashboard — key KPIs and sparklines."""
    banner(32, "Executive Summary Dashboard")

    row_count = eda["row_count"]
    total_paid = eda["total_paid"]
    billing_npis = eda["billing_npis"]
    hcpcs_codes = eda["hcpcs_codes"]

    kpis = {
        "Total Records": f"{row_count:,}",
        "Total Paid": usd_fmt(total_paid),
        "Billing Providers": f"{billing_npis:,}",
        "HCPCS Codes": f"{hcpcs_codes:,}",
        "Avg Cost/Claim": f"${eda.get('avg_paid', 0):,.2f}",
        "Median Cost/Claim": f"${eda.get('median_paid', 0):,.2f}",
    }

    monthly = query(con, f"""
        SELECT CLAIM_FROM_MONTH, SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH ORDER BY CLAIM_FROM_MONTH
    """)
    monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly["CLAIM_FROM_MONTH"])

    fig = plt.figure(figsize=(20, 16))
    fig.suptitle("Medicaid Provider Spending — Executive Summary",
                 fontsize=20, fontweight="bold", y=0.98, color="#1a1a2e")
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3, top=0.92, bottom=0.05)

    ax_kpi = fig.add_subplot(gs[0, :]); ax_kpi.axis("off")
    kpi_items = list(kpis.items())
    for i, (label, value) in enumerate(kpi_items):
        x_pos = (i + 0.5) / len(kpi_items)
        ax_kpi.text(x_pos, 0.7, value, transform=ax_kpi.transAxes, fontsize=22, fontweight="bold", ha="center", va="center", color="#1a1a2e")
        ax_kpi.text(x_pos, 0.2, label, transform=ax_kpi.transAxes, fontsize=11, ha="center", va="center", color="#666")

    ax = fig.add_subplot(gs[1, 0])
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["total_paid"], alpha=0.3, color="#1a73e8")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["total_paid"], color="#1a73e8", linewidth=2)
    ax.set_title("Monthly Spending Trend", fontsize=13, fontweight="bold"); usd(ax); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax = fig.add_subplot(gs[1, 1])
    ax.fill_between(monthly["CLAIM_FROM_MONTH"], monthly["total_claims"], alpha=0.3, color="#e8710a")
    ax.plot(monthly["CLAIM_FROM_MONTH"], monthly["total_claims"], color="#e8710a", linewidth=2)
    ax.set_title("Monthly Claims Trend", fontsize=13, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax = fig.add_subplot(gs[1, 2])
    if yoy_totals is not None and "paid_yoy_change" in yoy_totals.columns:
        yt = yoy_totals.dropna(subset=["paid_yoy_change"])
        colors_bar = ["#34a853" if v >= 0 else "#ea4335" for v in yt["paid_yoy_change"]]
        ax.bar(yt["year"].astype(int).astype(str), yt["paid_yoy_change"], color=colors_bar, edgecolor="white")
        ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("YoY Growth %", fontsize=13, fontweight="bold"); ax.set_ylabel("% Change")

    ax = fig.add_subplot(gs[2, 0])
    paid_vals = query(con, f"SELECT TOTAL_PAID FROM '{csv}' WHERE TOTAL_PAID > 0 USING SAMPLE 50000")
    ax.hist(np.log10(paid_vals["TOTAL_PAID"]), bins=60, color="#9334e6", edgecolor="white", alpha=0.85)
    ax.set_title("Spending Distribution (log₁₀)", fontsize=13, fontweight="bold"); ax.set_xlabel("log₁₀(Paid)"); ax.set_ylabel("Frequency")

    ax = fig.add_subplot(gs[2, 1])
    top5_procs = query(con, f"""
        SELECT HCPCS_CODE, SUM(TOTAL_PAID) AS total_paid FROM '{csv}'
        GROUP BY HCPCS_CODE ORDER BY total_paid DESC LIMIT 5
    """)
    ax.barh(top5_procs["HCPCS_CODE"].iloc[::-1], top5_procs["total_paid"].iloc[::-1], color="#1a73e8", edgecolor="white")
    ax.set_title("Top 5 Procedures", fontsize=13, fontweight="bold"); usd(ax, axis="x")

    ax = fig.add_subplot(gs[2, 2])
    prov_spend = query(con, f"""
        SELECT SUM(TOTAL_PAID) AS total_paid FROM '{csv}'
        GROUP BY BILLING_PROVIDER_NPI_NUM ORDER BY total_paid
    """)["total_paid"].values
    cum_pct = np.cumsum(prov_spend) / prov_spend.sum()
    x_pct = np.arange(1, len(prov_spend) + 1) / len(prov_spend)
    ax.plot(x_pct, cum_pct, color="#e8710a", linewidth=2)
    ax.plot([0, 1], [0, 1], "--", color="#aaa")
    ax.fill_between(x_pct, cum_pct, x_pct, alpha=0.1, color="#e8710a")
    ax.set_title("Provider Lorenz Curve", fontsize=13, fontweight="bold")
    ax.set_xlabel("Cumulative % Providers"); ax.set_ylabel("Cumulative % Spending")

    savefig(fig, "32_executive_summary.png")
    log.info("  Dashboard saved with 6 KPIs + 6 charts")
    return kpis

"""Procedures — HCPCS Lifecycle (Section 30)."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s30_hcpcs_lifecycle(con, csv: str):
    """HCPCS code lifecycle — new codes appearing, codes disappearing over time."""
    banner(30, "HCPCS Code Lifecycle")

    code_lifecycle = query(con, f"""
        SELECT HCPCS_CODE, MIN(CLAIM_FROM_MONTH) AS first_seen, MAX(CLAIM_FROM_MONTH) AS last_seen,
               COUNT(DISTINCT CLAIM_FROM_MONTH) AS months_active,
               SUM(TOTAL_PAID) AS total_paid,
               COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS provider_count
        FROM '{csv}' GROUP BY HCPCS_CODE
    """)
    code_lifecycle["first_dt"] = pd.to_datetime(code_lifecycle["first_seen"])
    code_lifecycle["last_dt"] = pd.to_datetime(code_lifecycle["last_seen"])
    code_lifecycle["first_quarter"] = code_lifecycle["first_dt"].dt.to_period("Q").astype(str)
    code_lifecycle["last_quarter"] = code_lifecycle["last_dt"].dt.to_period("Q").astype(str)
    entering = code_lifecycle.groupby("first_quarter").size().reset_index(name="new_codes")
    code_lifecycle.to_csv(OUTPUT_DIR / "30_hcpcs_lifecycle.csv", index=False)

    monthly_active = query(con, f"""
        SELECT CLAIM_FROM_MONTH, COUNT(DISTINCT HCPCS_CODE) AS active_codes
        FROM '{csv}' GROUP BY CLAIM_FROM_MONTH ORDER BY CLAIM_FROM_MONTH
    """)
    monthly_active["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly_active["CLAIM_FROM_MONTH"])
    log.info("  Total unique HCPCS codes: %d", len(code_lifecycle))
    log.info("  Codes active all 84 months: %d", (code_lifecycle["months_active"] == 84).sum())
    log.info("  Codes active <6 months: %d", (code_lifecycle["months_active"] < 6).sum())

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("HCPCS Code Lifecycle", fontsize=16, fontweight="bold", y=1.01)
    ax = axes[0, 0]
    ax.plot(monthly_active["CLAIM_FROM_MONTH"], monthly_active["active_codes"],
            color="#1a73e8", linewidth=2, marker="o", markersize=3)
    ax.set_title("Active HCPCS Codes per Month", fontsize=13, fontweight="bold")
    ax.set_ylabel("Code Count"); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax = axes[0, 1]
    ax.hist(code_lifecycle["months_active"], bins=42, color="#e8710a", edgecolor="white", alpha=0.85)
    ax.set_title("Code Longevity Distribution", fontsize=13, fontweight="bold"); ax.set_xlabel("Months Active"); ax.set_ylabel("Code Count")
    ax = axes[1, 0]
    if len(entering) > 0:
        ax.bar(range(len(entering)), entering["new_codes"], color="#34a853", edgecolor="white")
        ax.set_xticks(range(len(entering))); ax.set_xticklabels(entering["first_quarter"], rotation=45, fontsize=7)
        ax.set_title("New HCPCS Codes per Quarter", fontsize=13, fontweight="bold"); ax.set_ylabel("New Codes")
    ax = axes[1, 1]
    sample = code_lifecycle.sample(n=min(5000, len(code_lifecycle)), random_state=42)
    ax.scatter(sample["months_active"], sample["total_paid"], alpha=0.4, s=10, color="#9334e6"); ax.set_yscale("log")
    ax.set_title("Code Longevity vs Total Spending", fontsize=13, fontweight="bold")
    ax.set_xlabel("Months Active"); ax.set_ylabel("Total Paid (USD, log)"); usd(ax)
    fig.tight_layout(); savefig(fig, "30_hcpcs_lifecycle.png")
    return code_lifecycle

"""Providers — Specialization HHI (Section 27)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s27_provider_specialization(con, csv: str):
    """Provider specialization via HHI (Herfindahl–Hirschman Index)."""
    banner(27, "Provider Specialization Index (HHI)")

    hhi = query(con, f"""
        WITH provider_code AS (
            SELECT BILLING_PROVIDER_NPI_NUM, HCPCS_CODE, SUM(TOTAL_PAID) AS code_paid
            FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM, HCPCS_CODE
        ), provider_total AS (
            SELECT BILLING_PROVIDER_NPI_NUM, SUM(code_paid) AS total_paid, COUNT(DISTINCT HCPCS_CODE) AS num_codes
            FROM provider_code GROUP BY BILLING_PROVIDER_NPI_NUM
        ), provider_shares AS (
            SELECT pc.BILLING_PROVIDER_NPI_NUM, pc.HCPCS_CODE,
                   (pc.code_paid / pt.total_paid) AS share, pt.total_paid, pt.num_codes
            FROM provider_code pc JOIN provider_total pt ON pc.BILLING_PROVIDER_NPI_NUM = pt.BILLING_PROVIDER_NPI_NUM
            WHERE pt.total_paid > 0
        )
        SELECT BILLING_PROVIDER_NPI_NUM, SUM(share * share) AS hhi,
               MAX(total_paid) AS total_paid, MAX(num_codes) AS num_codes
        FROM provider_shares GROUP BY BILLING_PROVIDER_NPI_NUM
    """)
    hhi["specialization"] = pd.cut(hhi["hhi"], bins=[0, 0.15, 0.25, 0.5, 1.01],
                                   labels=["Diversified", "Moderate", "Concentrated", "Specialist"])
    hhi.to_csv(OUTPUT_DIR / "27_provider_hhi.csv", index=False)
    spec_summary = hhi.groupby("specialization", observed=True).agg(
        count=("BILLING_PROVIDER_NPI_NUM", "count"), avg_paid=("total_paid", "mean"), total_paid=("total_paid", "sum"),
    ).reset_index()
    spec_summary["pct"] = spec_summary["count"] / spec_summary["count"].sum() * 100
    spec_summary.to_csv(OUTPUT_DIR / "27_specialization_summary.csv", index=False)
    log.info("  Mean HHI: %.4f", hhi["hhi"].mean())
    log.info("  Specialists (HHI>0.5): %.1f%%", (hhi["hhi"] > 0.5).mean() * 100)

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    ax = axes[0]
    ax.hist(hhi["hhi"], bins=50, color="#9334e6", edgecolor="white", alpha=0.85)
    ax.axvline(0.25, color="red", linestyle="--", label="HHI=0.25 (concentrated)")
    ax.set_title("Provider HHI Distribution", fontsize=13, fontweight="bold"); ax.set_xlabel("HHI"); ax.set_ylabel("Provider Count"); ax.legend()
    ax = axes[1]; colors_spec = ["#34a853", "#1a73e8", "#e8710a", "#ea4335"]
    ax.bar(spec_summary["specialization"].astype(str), spec_summary["pct"], color=colors_spec, edgecolor="white")
    ax.set_title("Provider Specialization Breakdown", fontsize=13, fontweight="bold"); ax.set_ylabel("% of Providers")
    for i, v in enumerate(spec_summary["pct"]):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9, fontweight="bold")
    ax = axes[2]; sample = hhi.sample(n=min(50_000, len(hhi)), random_state=42)
    ax.scatter(sample["hhi"], sample["total_paid"], alpha=0.15, s=3, color="#1a73e8"); ax.set_yscale("log")
    ax.set_title("HHI vs Total Paid", fontsize=13, fontweight="bold"); ax.set_xlabel("HHI (Specialization)"); ax.set_ylabel("Total Paid (USD, log)"); usd(ax)
    fig.suptitle("Provider Specialization (HHI)", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "27_specialization.png")
    return hhi

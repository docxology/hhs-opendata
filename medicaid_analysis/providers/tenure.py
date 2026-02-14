"""Providers — Tenure & Longevity (Section 24)."""

import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s24_provider_tenure(con, csv: str):
    """Provider tenure and longevity — new vs established providers."""
    banner(24, "Provider Tenure & Longevity")

    tenure = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM,
               MIN(CLAIM_FROM_MONTH) AS first_month, MAX(CLAIM_FROM_MONTH) AS last_month,
               COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
               COUNT(DISTINCT HCPCS_CODE) AS procedure_count
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM
    """)
    tenure["first_dt"] = pd.to_datetime(tenure["first_month"])
    tenure["last_dt"] = pd.to_datetime(tenure["last_month"])
    tenure["tenure_months"] = ((tenure["last_dt"] - tenure["first_dt"]).dt.days / 30.44).round().astype(int)
    tenure["activity_rate"] = tenure["active_months"] / tenure["tenure_months"].clip(lower=1)
    tenure["avg_monthly_paid"] = tenure["total_paid"] / tenure["active_months"].clip(lower=1)
    tenure["cohort"] = pd.cut(tenure["tenure_months"], bins=[0, 6, 12, 24, 48, 200],
                              labels=["<6mo", "6-12mo", "1-2yr", "2-4yr", "4yr+"])

    cohort_summary = tenure.groupby("cohort", observed=True).agg(
        provider_count=("BILLING_PROVIDER_NPI_NUM", "count"), total_paid=("total_paid", "sum"),
        avg_paid=("total_paid", "mean"), avg_active_months=("active_months", "mean"),
    ).reset_index()
    cohort_summary["pct_providers"] = cohort_summary["provider_count"] / cohort_summary["provider_count"].sum() * 100
    cohort_summary["pct_spending"] = cohort_summary["total_paid"] / cohort_summary["total_paid"].sum() * 100

    tenure[["BILLING_PROVIDER_NPI_NUM", "tenure_months", "active_months", "activity_rate",
            "total_paid", "avg_monthly_paid", "cohort"]].to_csv(OUTPUT_DIR / "24_provider_tenure.csv", index=False)
    cohort_summary.to_csv(OUTPUT_DIR / "24_cohort_summary.csv", index=False)
    log.info("  Avg tenure: %.1f months", tenure["tenure_months"].mean())
    log.info("  Avg activity rate: %.2f", tenure["activity_rate"].mean())

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Provider Tenure & Longevity", fontsize=16, fontweight="bold", y=1.01)
    ax = axes[0, 0]
    ax.hist(tenure["tenure_months"].clip(upper=84), bins=42, color="#1a73e8", edgecolor="white", alpha=0.85)
    ax.set_title("Provider Tenure Distribution (months)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tenure (months)"); ax.set_ylabel("Provider Count")
    ax = axes[0, 1]; cs = cohort_summary; x = range(len(cs)); w = 0.35
    ax.bar([i - w/2 for i in x], cs["pct_providers"], w, label="% of Providers", color="#1a73e8")
    ax.bar([i + w/2 for i in x], cs["pct_spending"], w, label="% of Spending", color="#e8710a")
    ax.set_xticks(x); ax.set_xticklabels(cs["cohort"])
    ax.set_title("Providers vs Spending by Tenure Cohort", fontsize=13, fontweight="bold"); ax.set_ylabel("%"); ax.legend()
    ax = axes[1, 0]; sample = tenure.sample(n=min(50_000, len(tenure)), random_state=42)
    ax.scatter(sample["tenure_months"], sample["total_paid"], alpha=0.15, s=3, color="#9334e6"); ax.set_yscale("log")
    ax.set_title("Tenure vs Total Paid", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tenure (months)"); ax.set_ylabel("Total Paid (USD, log)"); usd(ax)
    ax = axes[1, 1]
    ax.hist(tenure["activity_rate"].clip(upper=1), bins=50, color="#34a853", edgecolor="white", alpha=0.85)
    ax.set_title("Provider Activity Rate (active/tenure months)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Activity Rate"); ax.set_ylabel("Provider Count")
    fig.tight_layout(); savefig(fig, "24_provider_tenure.png")
    return tenure

"""Fraud Detection — Temporal Billing Anomalies (Section 39)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats
from utils import log, banner, query, savefig, save_csv, usd, OUTPUT_DIR


def s39_temporal_anomalies(con, csv: str):
    """Detect suspicious temporal patterns — ramping, end-of-year spikes, etc."""
    banner(39, "Temporal Billing Anomalies")

    monthly = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, CLAIM_FROM_MONTH,
               SUM(TOTAL_PAID) AS monthly_paid, SUM(TOTAL_CLAIMS) AS monthly_claims,
               COUNT(DISTINCT HCPCS_CODE) AS monthly_codes
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM, CLAIM_FROM_MONTH
    """)
    monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(monthly["CLAIM_FROM_MONTH"])
    monthly["month_num"] = monthly["CLAIM_FROM_MONTH"].dt.month

    provider_entropy = monthly.groupby("BILLING_PROVIDER_NPI_NUM").apply(
        lambda g: scipy_stats.entropy(g["monthly_paid"].values / g["monthly_paid"].sum())
            if g["monthly_paid"].sum() > 0 and len(g) > 1 else 0
    ).reset_index(name="temporal_entropy")
    # Replace -inf/nan entropy with 0 (single-value or degenerate distributions)
    provider_entropy["temporal_entropy"] = provider_entropy["temporal_entropy"].replace(
        [np.inf, -np.inf], np.nan).fillna(0)

    provider_stats = monthly.groupby("BILLING_PROVIDER_NPI_NUM").agg(
        total_paid=("monthly_paid", "sum"), active_months=("CLAIM_FROM_MONTH", "nunique"),
        max_monthly=("monthly_paid", "max"),
        cv=("monthly_paid", lambda x: x.std() / x.mean() if x.mean() > 0 else 0),
    ).reset_index()
    provider_stats = provider_stats.merge(provider_entropy, on="BILLING_PROVIDER_NPI_NUM")
    provider_stats["max_concentration"] = provider_stats["max_monthly"] / provider_stats["total_paid"].clip(lower=1)
    entropy_p5 = provider_stats.loc[provider_stats["active_months"] >= 6, "temporal_entropy"].quantile(0.05)
    provider_stats["flag_concentrated_time"] = (
        (provider_stats["temporal_entropy"] < entropy_p5) & (provider_stats["active_months"] >= 6) & (provider_stats["total_paid"] > 5000))
    provider_stats["flag_high_cv"] = (provider_stats["cv"] > 2) & (provider_stats["active_months"] >= 6)
    provider_stats["flag_any_temporal"] = provider_stats["flag_concentrated_time"] | provider_stats["flag_high_cv"]
    flagged = provider_stats[provider_stats["flag_any_temporal"]].sort_values("total_paid", ascending=False)
    save_csv(provider_stats, "39_temporal_profiles.csv", "fraud")
    save_csv(flagged, "39_temporal_flagged.csv", "fraud")
    log.info("  Temporally concentrated: %d", provider_stats["flag_concentrated_time"].sum())
    log.info("  High CV: %d", provider_stats["flag_high_cv"].sum())

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Temporal Billing Anomalies", fontsize=15, fontweight="bold", y=1.02)
    ax = axes[0]; valid = provider_stats[(provider_stats["active_months"] >= 6) & np.isfinite(provider_stats["temporal_entropy"])]
    ax.hist(valid["temporal_entropy"], bins=50, color="#1a73e8", edgecolor="white", alpha=0.85)
    ax.axvline(entropy_p5, color="red", linestyle="--", label=f"P5 = {entropy_p5:.2f}"); ax.set_title("Temporal Entropy (≥6mo providers)", fontweight="bold"); ax.legend()
    ax = axes[1]
    ax.hist(valid["cv"].clip(0, 5), bins=50, color="#e8710a", edgecolor="white", alpha=0.85)
    ax.axvline(2, color="red", linestyle="--", label="CV=2 threshold"); ax.set_title("Coefficient of Variation", fontweight="bold"); ax.legend()
    ax = axes[2]
    ax.scatter(provider_stats["temporal_entropy"], provider_stats["total_paid"], alpha=0.1, s=3, color="#34a853")
    if len(flagged) > 0:
        ax.scatter(flagged["temporal_entropy"], flagged["total_paid"], alpha=0.5, s=10, color="#ea4335", label="Flagged")
    ax.set_yscale("log"); ax.set_title("Entropy vs Total Paid", fontweight="bold"); usd(ax); ax.legend()
    fig.tight_layout(); savefig(fig, "39_temporal_anomalies.png", "fraud")
    return flagged

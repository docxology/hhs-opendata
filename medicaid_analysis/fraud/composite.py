"""Fraud Detection — Composite Fraud Risk Score (Section 40)."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, save_csv, usd, usd_fmt, num_fmt, OUTPUT_DIR


def s40_composite_fraud_score(con, csv: str, upcoding_df, velocity_df, phantom_df,
                               cost_outlier_df, relationship_df, temporal_df):
    """Combine all fraud signals into a single composite risk score per provider."""
    banner(40, "Composite Fraud Risk Scoring")

    all_providers = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM
    """)
    scores = all_providers[["BILLING_PROVIDER_NPI_NUM", "total_paid", "total_claims"]].copy()
    scores["risk_upcoding"] = scores["BILLING_PROVIDER_NPI_NUM"].isin(
        upcoding_df["BILLING_PROVIDER_NPI_NUM"] if len(upcoding_df) > 0 else []).astype(int)
    scores["risk_velocity"] = scores["BILLING_PROVIDER_NPI_NUM"].isin(
        velocity_df["BILLING_PROVIDER_NPI_NUM"] if len(velocity_df) > 0 else []).astype(int)
    scores["risk_phantom"] = scores["BILLING_PROVIDER_NPI_NUM"].isin(
        phantom_df["BILLING_PROVIDER_NPI_NUM"] if len(phantom_df) > 0 else []).astype(int)
    scores["risk_cost_outlier"] = scores["BILLING_PROVIDER_NPI_NUM"].isin(
        cost_outlier_df["BILLING_PROVIDER_NPI_NUM"] if len(cost_outlier_df) > 0 else []).astype(int)
    scores["risk_relationship"] = scores["BILLING_PROVIDER_NPI_NUM"].isin(
        relationship_df["BILLING_PROVIDER_NPI_NUM"] if len(relationship_df) > 0 else []).astype(int)
    scores["risk_temporal"] = scores["BILLING_PROVIDER_NPI_NUM"].isin(
        temporal_df["BILLING_PROVIDER_NPI_NUM"] if len(temporal_df) > 0 else []).astype(int)

    risk_cols = [c for c in scores.columns if c.startswith("risk_")]
    scores["fraud_score"] = scores[risk_cols].sum(axis=1)
    scores["risk_tier"] = pd.cut(scores["fraud_score"], bins=[-1, 0, 1, 2, 6],
                                  labels=["Clean", "Low", "Medium", "High"])
    tier_summary = scores.groupby("risk_tier", observed=True).agg(
        providers=("BILLING_PROVIDER_NPI_NUM", "count"), total_paid=("total_paid", "sum"),
    ).reset_index()
    tier_summary["pct_providers"] = tier_summary["providers"] / tier_summary["providers"].sum() * 100
    tier_summary["pct_spending"] = tier_summary["total_paid"] / tier_summary["total_paid"].sum() * 100
    high_risk = scores[scores["fraud_score"] >= 2].sort_values("fraud_score", ascending=False)

    save_csv(scores, "40_fraud_risk_scores.csv", "fraud")
    save_csv(tier_summary, "40_risk_tier_summary.csv", "fraud")
    save_csv(high_risk.head(500), "40_high_risk_providers.csv", "fraud")

    log.info("  Risk distribution:")
    for _, row in tier_summary.iterrows():
        log.info("    %s: %d providers (%.1f%%), $%s (%.1f%%)",
                 row["risk_tier"], row["providers"], row["pct_providers"],
                 usd_fmt(row["total_paid"]), row["pct_spending"])

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Composite Fraud Risk Scoring", fontsize=16, fontweight="bold", y=1.01)
    tier_colors = {"Clean": "#34a853", "Low": "#fbbc04", "Medium": "#e8710a", "High": "#ea4335"}
    ax = axes[0, 0]
    bars = ax.bar(tier_summary["risk_tier"].astype(str), tier_summary["pct_providers"],
                  color=[tier_colors.get(t, "#999") for t in tier_summary["risk_tier"]], edgecolor="white")
    ax.set_title("Providers by Risk Tier", fontsize=13, fontweight="bold"); ax.set_ylabel("% of Providers")
    for bar, v in zip(bars, tier_summary["pct_providers"]):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.3, f"{v:.1f}%", ha="center", fontsize=9, fontweight="bold")
    ax = axes[0, 1]
    bars = ax.bar(tier_summary["risk_tier"].astype(str), tier_summary["pct_spending"],
                  color=[tier_colors.get(t, "#999") for t in tier_summary["risk_tier"]], edgecolor="white")
    ax.set_title("Spending by Risk Tier", fontsize=13, fontweight="bold"); ax.set_ylabel("% of Spending")
    for bar, v in zip(bars, tier_summary["pct_spending"]):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.3, f"{v:.1f}%", ha="center", fontsize=9, fontweight="bold")
    ax = axes[1, 0]
    score_dist = scores["fraud_score"].value_counts().sort_index()
    ax.bar(score_dist.index.astype(str), score_dist.values, color="#1a73e8", edgecolor="white")
    ax.set_title("Fraud Score Distribution", fontsize=13, fontweight="bold"); ax.set_xlabel("# Fraud Signals"); ax.set_ylabel("Provider Count")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))
    ax = axes[1, 1]
    if len(high_risk) > 0:
        top_hr = high_risk.head(50); heatmap_data = top_hr[risk_cols].values
        ax.imshow(heatmap_data, cmap="Reds", aspect="auto", interpolation="nearest")
        ax.set_yticks(range(len(top_hr))); ax.set_yticklabels(top_hr["BILLING_PROVIDER_NPI_NUM"].astype(str).str[:10], fontsize=6)
        ax.set_xticks(range(len(risk_cols))); ax.set_xticklabels([c.replace("risk_", "") for c in risk_cols], fontsize=8, rotation=45)
        ax.set_title("Top-50 High-Risk Signal Heatmap", fontsize=13, fontweight="bold")
    fig.tight_layout(); savefig(fig, "40_fraud_risk_scores.png", "fraud")
    return scores

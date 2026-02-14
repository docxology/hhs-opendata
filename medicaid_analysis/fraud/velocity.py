"""Fraud Detection — Billing Velocity Anomalies (Section 34)."""

import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, save_csv, usd, OUTPUT_DIR


def s34_billing_velocity_anomalies(con, csv: str):
    """Detect providers with suspicious sudden spikes in billing volume."""
    banner(34, "Billing Velocity Anomalies")

    provider_monthly = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, CLAIM_FROM_MONTH,
               SUM(TOTAL_PAID) AS monthly_paid, SUM(TOTAL_CLAIMS) AS monthly_claims
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM, CLAIM_FROM_MONTH
    """)
    provider_monthly["CLAIM_FROM_MONTH"] = pd.to_datetime(provider_monthly["CLAIM_FROM_MONTH"])
    provider_monthly = provider_monthly.sort_values(["BILLING_PROVIDER_NPI_NUM", "CLAIM_FROM_MONTH"])

    # Filter to providers with ≥4 active months (required for rolling window)
    month_counts = provider_monthly.groupby("BILLING_PROVIDER_NPI_NUM").size()
    eligible_npis = month_counts[month_counts >= 4].index
    log.info("  Providers with ≥4 months: %d / %d", len(eligible_npis), len(month_counts))
    eligible = provider_monthly[provider_monthly["BILLING_PROVIDER_NPI_NUM"].isin(eligible_npis)].copy()

    if eligible.empty:
        log.info("  No eligible providers — skipping spike detection")
        provider_flags = pd.DataFrame(columns=["BILLING_PROVIDER_NPI_NUM", "spike_count",
                                                "max_spike_ratio", "max_spike_paid", "total_paid"])
        save_csv(provider_flags, "34_velocity_anomalies.csv", "fraud")
        fig, axes = plt.subplots(1, 3, figsize=(20, 7))
        fig.suptitle("Billing Velocity Anomalies — No Data", fontsize=15, fontweight="bold")
        fig.tight_layout(); savefig(fig, "34_velocity_anomalies.png", "fraud")
        return provider_flags

    # Compute rolling stats per provider using vectorized groupby + transform
    eligible = eligible.sort_values(["BILLING_PROVIDER_NPI_NUM", "CLAIM_FROM_MONTH"])
    eligible["rolling_mean"] = eligible.groupby("BILLING_PROVIDER_NPI_NUM")["monthly_paid"] \
        .transform(lambda x: x.rolling(3, min_periods=2).mean().shift(1))
    eligible["rolling_std"] = eligible.groupby("BILLING_PROVIDER_NPI_NUM")["monthly_paid"] \
        .transform(lambda x: x.rolling(3, min_periods=2).std().shift(1))
    eligible["spike_ratio"] = eligible["monthly_paid"] / eligible["rolling_mean"].clip(lower=1)
    eligible["z_spike"] = (eligible["monthly_paid"] - eligible["rolling_mean"]) / eligible["rolling_std"].clip(lower=1)

    spikes = eligible.dropna(subset=["spike_ratio"])
    spikes["flag_spike"] = (spikes["spike_ratio"] > 5) | (spikes["z_spike"] > 4)
    flagged_events = spikes[spikes["flag_spike"]]

    if flagged_events.empty:
        log.info("  No spike events detected")
        provider_flags = pd.DataFrame(columns=["BILLING_PROVIDER_NPI_NUM", "spike_count",
                                                "max_spike_ratio", "max_spike_paid", "total_paid"])
    else:
        provider_flags = flagged_events.groupby("BILLING_PROVIDER_NPI_NUM").agg(
            spike_count=("flag_spike", "sum"), max_spike_ratio=("spike_ratio", "max"),
            max_spike_paid=("monthly_paid", "max"), total_paid=("monthly_paid", "sum"),
        ).reset_index().sort_values("max_spike_ratio", ascending=False)

    save_csv(provider_flags, "34_velocity_anomalies.csv", "fraud")
    save_csv(flagged_events.head(500), "34_spike_events.csv", "fraud")
    log.info("  Spike events: %d across %d providers", len(flagged_events), len(provider_flags))

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Billing Velocity Anomalies — Sudden Spikes", fontsize=15, fontweight="bold", y=1.02)
    ax = axes[0]
    ax.hist(spikes["spike_ratio"].clip(0, 20), bins=100, color="#9334e6", edgecolor="white", alpha=0.85, log=True)
    ax.axvline(5, color="red", linestyle="--", label="5x threshold"); ax.set_title("Spike Ratio Distribution", fontweight="bold"); ax.set_xlabel("Ratio to 3-mo avg"); ax.legend()
    ax = axes[1]
    if len(provider_flags) > 0:
        ax.hist(provider_flags["spike_count"].clip(0, 20), bins=20, color="#1a73e8", edgecolor="white")
        ax.set_title("Spikes per Provider", fontweight="bold"); ax.set_xlabel("# Spike Events")
    ax = axes[2]
    if len(provider_flags) > 0:
        sample = provider_flags.head(200)
        ax.scatter(sample["spike_count"], sample["max_spike_paid"], alpha=0.5, s=20, color="#ea4335")
        ax.set_yscale("log"); ax.set_title("Spike Count vs Max Spike $", fontweight="bold"); usd(ax)
    fig.tight_layout(); savefig(fig, "34_velocity_anomalies.png", "fraud")
    return provider_flags

"""Fraud Detection — Phantom / Ghost Billing (Section 35)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, save_csv, usd, OUTPUT_DIR


def s35_phantom_billing(con, csv: str):
    """Detect impossible billing volumes — claims/beneficiary ratios far above norms."""
    banner(35, "Phantom / Ghost Billing Detection")

    phantom = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, HCPCS_CODE,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
               SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene,
               COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months
        FROM '{csv}' WHERE TOTAL_CLAIMS > 0 AND TOTAL_UNIQUE_BENEFICIARIES > 0
        GROUP BY BILLING_PROVIDER_NPI_NUM, HCPCS_CODE
    """)
    phantom["claims_per_bene"] = phantom["total_claims"] / phantom["total_bene"]
    phantom["paid_per_bene"] = phantom["total_paid"] / phantom["total_bene"]
    phantom["claims_per_month"] = phantom["total_claims"] / phantom["active_months"].clip(lower=1)

    peer_stats = phantom.groupby("HCPCS_CODE").agg(
        peer_median_cpb=("claims_per_bene", "median"),
        peer_p95_cpb=("claims_per_bene", lambda x: x.quantile(0.95)),
        peer_p99_cpb=("claims_per_bene", lambda x: x.quantile(0.99)),
    ).reset_index()
    phantom = phantom.merge(peer_stats, on="HCPCS_CODE")
    phantom["ratio_to_p95"] = phantom["claims_per_bene"] / phantom["peer_p95_cpb"].clip(lower=0.1)
    phantom["flag_phantom"] = (phantom["ratio_to_p95"] > 3) | (phantom["claims_per_bene"] > 50)
    flagged = phantom[phantom["flag_phantom"]].sort_values("claims_per_bene", ascending=False)
    provider_phantom = flagged.groupby("BILLING_PROVIDER_NPI_NUM").agg(
        flagged_codes=("HCPCS_CODE", "count"), max_claims_per_bene=("claims_per_bene", "max"),
        total_paid=("total_paid", "sum"),
    ).reset_index().sort_values("max_claims_per_bene", ascending=False)
    save_csv(flagged.head(2000), "35_phantom_records.csv", "fraud")
    save_csv(provider_phantom, "35_phantom_providers.csv", "fraud")
    log.info("  Phantom-flagged records: %d (%d providers)", len(flagged), len(provider_phantom))

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Phantom / Ghost Billing — Impossible Volumes", fontsize=15, fontweight="bold", y=1.02)
    ax = axes[0]
    ax.hist(phantom["claims_per_bene"].clip(0, 30), bins=80, color="#ea4335", edgecolor="white", alpha=0.85, log=True)
    ax.axvline(50, color="black", linestyle="--", label="Absolute threshold (50)"); ax.set_title("Claims/Beneficiary Distribution", fontweight="bold"); ax.legend()
    ax = axes[1]
    ax.hist(phantom["ratio_to_p95"].clip(0, 10), bins=60, color="#e8710a", edgecolor="white", alpha=0.85, log=True)
    ax.axvline(3, color="red", linestyle="--", label="3x P95 threshold"); ax.set_title("Ratio to Peer P95", fontweight="bold"); ax.legend()
    ax = axes[2]
    if len(flagged) > 0:
        sample = flagged.head(1000)
        ax.scatter(sample["claims_per_bene"], sample["total_paid"], alpha=0.3, s=10, color="#9334e6")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title("Flagged: Claims/Bene vs Paid", fontweight="bold"); usd(ax)
    fig.tight_layout(); savefig(fig, "35_phantom_billing.png", "fraud")
    return provider_phantom

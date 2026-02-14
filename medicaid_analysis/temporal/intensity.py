"""Temporal — Beneficiary Intensity (Section 19)."""

import numpy as np
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s19_beneficiary_intensity(con, csv: str):
    """Claims per beneficiary analysis — utilization intensity."""
    banner(19, "Beneficiary Intensity (Claims/Beneficiary)")

    intensity = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, HCPCS_CODE, TOTAL_CLAIMS, TOTAL_UNIQUE_BENEFICIARIES, TOTAL_PAID,
               TOTAL_CLAIMS * 1.0 / NULLIF(TOTAL_UNIQUE_BENEFICIARIES, 0) AS claims_per_bene,
               TOTAL_PAID / NULLIF(TOTAL_UNIQUE_BENEFICIARIES, 0) AS paid_per_bene
        FROM '{csv}' WHERE TOTAL_UNIQUE_BENEFICIARIES > 5 AND TOTAL_CLAIMS > 0
    """)
    log.info("  Mean claims/beneficiary: %.2f", intensity["claims_per_bene"].mean())
    log.info("  Median claims/beneficiary: %.2f", intensity["claims_per_bene"].median())
    log.info("  P99 claims/beneficiary: %.2f", intensity["claims_per_bene"].quantile(0.99))

    proc_intensity = intensity.groupby("HCPCS_CODE").agg(
        avg_claims_per_bene=("claims_per_bene", "mean"), median_claims_per_bene=("claims_per_bene", "median"),
        avg_paid_per_bene=("paid_per_bene", "mean"), total_records=("BILLING_PROVIDER_NPI_NUM", "count"),
    ).reset_index().sort_values("avg_claims_per_bene", ascending=False)
    proc_intensity.head(50).to_csv(OUTPUT_DIR / "19_beneficiary_intensity.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Beneficiary Utilization Intensity", fontsize=16, fontweight="bold", y=1.01)
    ax = axes[0, 0]
    cpb = intensity["claims_per_bene"].clip(upper=intensity["claims_per_bene"].quantile(0.99))
    ax.hist(cpb, bins=100, color="#1a73e8", edgecolor="white", alpha=0.85)
    ax.set_title("Claims per Beneficiary Distribution", fontsize=13, fontweight="bold"); ax.set_xlabel("Claims / Beneficiary"); ax.set_ylabel("Frequency")
    ax = axes[0, 1]
    log_cpb = np.log10(intensity["claims_per_bene"][intensity["claims_per_bene"] > 0])
    ax.hist(log_cpb, bins=80, color="#e8710a", edgecolor="white", alpha=0.85)
    ax.set_title("Claims per Beneficiary (log10)", fontsize=13, fontweight="bold"); ax.set_xlabel("log10(Claims/Bene)"); ax.set_ylabel("Frequency")
    ax = axes[1, 0]
    sample = intensity.sample(n=min(50_000, len(intensity)), random_state=42)
    ax.scatter(sample["claims_per_bene"], sample["paid_per_bene"], alpha=0.15, s=3, color="#9334e6")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_title("Claims/Bene vs Paid/Bene", fontsize=13, fontweight="bold"); ax.set_xlabel("Claims per Beneficiary"); ax.set_ylabel("Paid per Beneficiary (USD)"); usd(ax)
    ax = axes[1, 1]
    top_int = proc_intensity[proc_intensity["total_records"] >= 20].head(15).iloc[::-1]
    ax.barh(top_int["HCPCS_CODE"], top_int["avg_claims_per_bene"], color="#34a853", edgecolor="white")
    ax.set_title("Top 15 Procedures by Avg Claims/Beneficiary", fontsize=13, fontweight="bold"); ax.set_xlabel("Avg Claims per Beneficiary")
    fig.tight_layout(); savefig(fig, "19_beneficiary_intensity.png")
    return proc_intensity

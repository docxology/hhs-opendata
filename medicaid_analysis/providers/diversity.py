"""Providers — Procedure Diversity (Section 10)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s10_procedure_diversity(con, csv: str):
    """How many procedures each provider bills and vice versa."""
    banner(10, "Procedure Diversity per Provider")

    div = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM,
               COUNT(DISTINCT HCPCS_CODE) AS num_procedures,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM
    """)
    div.to_csv(OUTPUT_DIR / "10_procedure_diversity.csv", index=False)
    log.info("  Avg procedures per provider: %.1f", div["num_procedures"].mean())
    log.info("  Median procedures per provider: %.0f", div["num_procedures"].median())

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    ax = axes[0]
    ax.hist(div["num_procedures"].clip(upper=50), bins=50, color="#1a73e8", edgecolor="white", alpha=0.85)
    ax.set_title("Procedures per Provider (clipped at 50)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Number of Distinct HCPCS Codes"); ax.set_ylabel("Provider Count")
    ax = axes[1]
    sample = div.sample(n=min(50_000, len(div)), random_state=42)
    ax.scatter(sample["num_procedures"], sample["total_paid"], alpha=0.2, s=3, color="#e8710a")
    ax.set_title("Procedure Diversity vs Total Paid", fontsize=13, fontweight="bold")
    ax.set_xlabel("Number of Procedures"); ax.set_ylabel("Total Paid (USD)")
    ax.set_yscale("log"); usd(ax)
    fig.tight_layout(); savefig(fig, "10_procedure_diversity.png")
    return div

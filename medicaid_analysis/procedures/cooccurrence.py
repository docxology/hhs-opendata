"""Procedures — Co-occurrence Analysis (Section 23)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, OUTPUT_DIR


def s23_procedure_cooccurrence(con, csv: str):
    """Which procedures are commonly billed together by the same provider."""
    banner(23, "Procedure Co-occurrence Analysis")

    pairs = query(con, f"""
        WITH provider_procs AS (
            SELECT BILLING_PROVIDER_NPI_NUM, HCPCS_CODE, SUM(TOTAL_PAID) AS total_paid
            FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM, HCPCS_CODE
        )
        SELECT a.HCPCS_CODE AS code_a, b.HCPCS_CODE AS code_b,
               COUNT(DISTINCT a.BILLING_PROVIDER_NPI_NUM) AS shared_providers,
               SUM(a.total_paid + b.total_paid) AS combined_paid
        FROM provider_procs a
        JOIN provider_procs b ON a.BILLING_PROVIDER_NPI_NUM = b.BILLING_PROVIDER_NPI_NUM AND a.HCPCS_CODE < b.HCPCS_CODE
        GROUP BY a.HCPCS_CODE, b.HCPCS_CODE HAVING shared_providers >= 50
        ORDER BY shared_providers DESC LIMIT 50
    """)
    pairs.to_csv(OUTPUT_DIR / "23_procedure_cooccurrence.csv", index=False)
    log.info("  Top pair: %s + %s (%d shared providers)",
             pairs.iloc[0]["code_a"], pairs.iloc[0]["code_b"],
             pairs.iloc[0]["shared_providers"] if len(pairs) > 0 else 0)

    fig, ax = plt.subplots(figsize=(14, 8))
    top = pairs.head(20).iloc[::-1]
    top["pair"] = top["code_a"] + " + " + top["code_b"]
    ax.barh(top["pair"], top["shared_providers"], color="#1a73e8", edgecolor="white")
    ax.set_title("Top 20 Procedure Co-occurrence Pairs (by Shared Providers)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Shared Providers")
    fig.tight_layout(); savefig(fig, "23_cooccurrence.png")
    return pairs

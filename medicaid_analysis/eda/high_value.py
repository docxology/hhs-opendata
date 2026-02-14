"""EDA — High-Value Claims (Section 12)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, OUTPUT_DIR


def s12_high_value_claims(con, csv: str):
    """Analysis of highest-value individual claim records."""
    banner(12, "Highest-Value Records")

    top_records = query(con, f"""
        SELECT *,
            TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0) AS cost_per_claim,
            TOTAL_PAID / NULLIF(TOTAL_UNIQUE_BENEFICIARIES, 0) AS cost_per_bene
        FROM '{csv}'
        ORDER BY TOTAL_PAID DESC
        LIMIT 100
    """)
    top_records.to_csv(OUTPUT_DIR / "12_highest_value_records.csv", index=False)
    log.info("  Top record: NPI %s, HCPCS %s, $%s (%s claims)",
             top_records.iloc[0]["BILLING_PROVIDER_NPI_NUM"],
             top_records.iloc[0]["HCPCS_CODE"],
             f"{top_records.iloc[0]['TOTAL_PAID']:,.2f}",
             f"{top_records.iloc[0]['TOTAL_CLAIMS']:,}")

    fig, ax = plt.subplots(figsize=(12, 6))
    counts = top_records["HCPCS_CODE"].value_counts().head(15)
    ax.barh(counts.index[::-1], counts.values[::-1], color="#9334e6", edgecolor="white")
    ax.set_title("HCPCS Codes in Top 100 Highest-Paid Records", fontsize=14, fontweight="bold")
    ax.set_xlabel("Count in Top 100")
    fig.tight_layout()
    savefig(fig, "12_high_value_hcpcs.png")
    return top_records

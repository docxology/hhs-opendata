"""EDA — Top Procedures & Top Providers (Sections 3 & 4)."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, usd, num_fmt, OUTPUT_DIR


def s03_top_procedures(con, csv: str):
    """Top HCPCS procedures by total spending, claims, and beneficiaries."""
    banner(3, "Top Procedures by Spending")

    top = query(con, f"""
        SELECT
            HCPCS_CODE,
            SUM(TOTAL_PAID)                         AS total_paid,
            SUM(TOTAL_CLAIMS)                       AS total_claims,
            SUM(TOTAL_UNIQUE_BENEFICIARIES)         AS total_bene,
            COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS provider_count,
            AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS avg_cost_per_claim
        FROM '{csv}'
        WHERE TOTAL_CLAIMS > 0
        GROUP BY HCPCS_CODE
        ORDER BY total_paid DESC
        LIMIT 50
    """)
    top.to_csv(OUTPUT_DIR / "03_top_procedures.csv", index=False)
    log.info("  #1 procedure: %s  ($%s)", top.iloc[0]["HCPCS_CODE"], f"{top.iloc[0]['total_paid']:,.0f}")

    fig, axes = plt.subplots(1, 2, figsize=(18, 9))
    ax = axes[0]
    d = top.head(20).iloc[::-1]
    ax.barh(d["HCPCS_CODE"], d["total_paid"], color="#1a73e8", edgecolor="white")
    ax.set_title("Top 20 Procedures by Total Paid", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Paid (USD)"); usd(ax, axis="x")

    ax = axes[1]
    by_claims = top.sort_values("total_claims", ascending=False).head(20).iloc[::-1]
    ax.barh(by_claims["HCPCS_CODE"], by_claims["total_claims"], color="#e8710a", edgecolor="white")
    ax.set_title("Top 20 Procedures by Claim Volume", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Claims"); ax.xaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))

    fig.tight_layout()
    savefig(fig, "03_top_procedures.png")
    return top


def s04_top_providers(con, csv: str):
    """Top billing providers ranked by spending and claim volume."""
    banner(4, "Top Billing Providers")

    top = query(con, f"""
        SELECT
            BILLING_PROVIDER_NPI_NUM,
            SUM(TOTAL_PAID)                         AS total_paid,
            SUM(TOTAL_CLAIMS)                       AS total_claims,
            SUM(TOTAL_UNIQUE_BENEFICIARIES)         AS total_bene,
            COUNT(DISTINCT HCPCS_CODE)              AS procedure_count,
            MIN(CLAIM_FROM_MONTH)                   AS first_month,
            MAX(CLAIM_FROM_MONTH)                   AS last_month
        FROM '{csv}'
        GROUP BY BILLING_PROVIDER_NPI_NUM
        ORDER BY total_paid DESC
        LIMIT 100
    """)
    top.to_csv(OUTPUT_DIR / "04_top_providers.csv", index=False)
    log.info("  #1 provider: NPI %s  ($%s)", top.iloc[0]["BILLING_PROVIDER_NPI_NUM"],
             f"{top.iloc[0]['total_paid']:,.0f}")

    fig, ax = plt.subplots(figsize=(12, 10))
    d = top.head(25).iloc[::-1]
    d["label"] = d["BILLING_PROVIDER_NPI_NUM"].astype(str)
    ax.barh(d["label"], d["total_paid"], color="#9334e6", edgecolor="white")
    ax.set_title("Top 25 Billing Providers by Total Paid", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Paid (USD)"); usd(ax, axis="x")
    ax.set_ylabel("Billing Provider NPI")
    fig.tight_layout()
    savefig(fig, "04_top_providers.png")
    return top

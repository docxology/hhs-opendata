"""Procedures — HCPCS Categories (Section 14)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s14_hcpcs_categories(con, csv: str):
    """HCPCS code category analysis using code prefix grouping."""
    banner(14, "HCPCS Category Analysis")

    cats = query(con, f"""
        SELECT
            CASE
                WHEN HCPCS_CODE LIKE '99%' THEN 'E&M (99xxx)'
                WHEN HCPCS_CODE LIKE 'T%'  THEN 'State Codes (T)'
                WHEN HCPCS_CODE LIKE 'S%'  THEN 'Commercial (S)'
                WHEN HCPCS_CODE LIKE 'J%'  THEN 'Drugs (J)'
                WHEN HCPCS_CODE LIKE 'H%'  THEN 'Behavioral Health (H)'
                WHEN HCPCS_CODE LIKE 'G%'  THEN 'Temporary Procedures (G)'
                WHEN HCPCS_CODE LIKE 'A%'  THEN 'Transport/Supplies (A)'
                WHEN HCPCS_CODE LIKE 'D%'  THEN 'Dental (D)'
                WHEN HCPCS_CODE LIKE 'E%'  THEN 'DME (E)'
                WHEN HCPCS_CODE LIKE 'L%'  THEN 'Orthotics/Prosthetics (L)'
                WHEN HCPCS_CODE LIKE 'V%'  THEN 'Vision/Hearing (V)'
                WHEN HCPCS_CODE BETWEEN '00100' AND '01999' THEN 'Anesthesia'
                WHEN HCPCS_CODE BETWEEN '10004' AND '69990' THEN 'Surgery'
                WHEN HCPCS_CODE BETWEEN '70010' AND '79999' THEN 'Radiology'
                WHEN HCPCS_CODE BETWEEN '80047' AND '89398' THEN 'Pathology/Lab'
                WHEN HCPCS_CODE BETWEEN '90281' AND '99199' THEN 'Medicine'
                ELSE 'Other'
            END AS category,
            COUNT(DISTINCT HCPCS_CODE) AS code_count,
            SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
            SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene,
            COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS provider_count
        FROM '{csv}' GROUP BY category ORDER BY total_paid DESC
    """)
    cats.to_csv(OUTPUT_DIR / "14_hcpcs_categories.csv", index=False)
    log.info("  Categories found: %d", len(cats))

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    ax = axes[0]
    d = cats.sort_values("total_paid", ascending=True)
    colors = plt.cm.tab20(np.linspace(0, 1, len(d)))
    ax.barh(d["category"], d["total_paid"], color=colors, edgecolor="white")
    ax.set_title("Spending by HCPCS Category", fontsize=14, fontweight="bold"); ax.set_xlabel("Total Paid (USD)"); usd(ax, axis="x")
    ax = axes[1]
    top_cats = cats.head(8)
    other = pd.DataFrame({"category": ["Other Categories"], "total_paid": [cats.iloc[8:]["total_paid"].sum()]})
    pie_data = pd.concat([top_cats[["category", "total_paid"]], other], ignore_index=True)
    ax.pie(pie_data["total_paid"], labels=pie_data["category"], autopct="%1.1f%%", startangle=90,
           textprops={"fontsize": 9}, colors=plt.cm.Set3(np.linspace(0, 1, len(pie_data))))
    ax.set_title("Spending Share by Category", fontsize=14, fontweight="bold")
    fig.tight_layout(); savefig(fig, "14_hcpcs_categories.png")

    fig, ax = plt.subplots(figsize=(12, 7))
    cats["avg_cost_per_claim"] = cats["total_paid"] / cats["total_claims"].replace(0, np.nan)
    d = cats.dropna(subset=["avg_cost_per_claim"]).sort_values("avg_cost_per_claim", ascending=True)
    ax.barh(d["category"], d["avg_cost_per_claim"], color="#9334e6", edgecolor="white")
    ax.set_title("Average Cost per Claim by HCPCS Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Avg Cost per Claim (USD)"); usd(ax, axis="x")
    fig.tight_layout(); savefig(fig, "14_category_cost_per_claim.png")
    return cats

"""Fraud Detection — Billing-Servicing Relationship Anomalies (Section 38)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, save_csv, usd, OUTPUT_DIR


def s38_billing_servicing_anomalies(con, csv: str):
    """Detect suspicious billing-servicing relationships (kickback signals)."""
    banner(38, "Billing-Servicing Relationship Anomalies")

    relationships = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, SERVICING_PROVIDER_NPI_NUM,
               COUNT(DISTINCT HCPCS_CODE) AS shared_codes, COUNT(DISTINCT CLAIM_FROM_MONTH) AS shared_months,
               SUM(TOTAL_PAID) AS relationship_paid, SUM(TOTAL_CLAIMS) AS relationship_claims
        FROM '{csv}' WHERE BILLING_PROVIDER_NPI_NUM != SERVICING_PROVIDER_NPI_NUM
        GROUP BY BILLING_PROVIDER_NPI_NUM, SERVICING_PROVIDER_NPI_NUM
    """)
    billing_totals = relationships.groupby("BILLING_PROVIDER_NPI_NUM")["relationship_paid"].sum().reset_index()
    billing_totals.columns = ["BILLING_PROVIDER_NPI_NUM", "billing_total"]
    relationships = relationships.merge(billing_totals, on="BILLING_PROVIDER_NPI_NUM")
    relationships["concentration_pct"] = relationships["relationship_paid"] / relationships["billing_total"].clip(lower=1) * 100
    relationships["flag_concentrated"] = (relationships["concentration_pct"] > 90) & (relationships["relationship_paid"] > 10000)
    code_p95 = relationships["shared_codes"].quantile(0.95)
    relationships["flag_broad"] = relationships["shared_codes"] > code_p95
    relationships["flag_any"] = relationships["flag_concentrated"] | relationships["flag_broad"]
    flagged = relationships[relationships["flag_any"]].sort_values("relationship_paid", ascending=False)
    save_csv(flagged.head(2000), "38_billing_servicing_anomalies.csv", "fraud")
    log.info("  Concentrated relationships (>90%%): %d", relationships["flag_concentrated"].sum())
    log.info("  Unusually broad (>%d codes): %d", int(code_p95), relationships["flag_broad"].sum())

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Billing-Servicing Relationship Anomalies", fontsize=15, fontweight="bold", y=1.02)
    ax = axes[0]
    ax.hist(relationships["concentration_pct"].clip(0, 100), bins=50, color="#1a73e8", edgecolor="white", alpha=0.85)
    ax.axvline(90, color="red", linestyle="--", label=">90% concentration"); ax.set_title("Billing Concentration %", fontweight="bold"); ax.legend()
    ax = axes[1]
    ax.hist(relationships["shared_codes"].clip(0, 50), bins=50, color="#e8710a", edgecolor="white", alpha=0.85, log=True)
    ax.axvline(code_p95, color="red", linestyle="--", label=f"P95 ({code_p95:.0f})"); ax.set_title("Shared Codes per Pair", fontweight="bold"); ax.legend()
    ax = axes[2]
    if len(flagged) > 0:
        sample = flagged.head(500)
        ax.scatter(sample["concentration_pct"], sample["relationship_paid"], alpha=0.4, s=15,
                   c=sample["flag_concentrated"].astype(int), cmap="RdYlGn_r")
        ax.set_yscale("log"); ax.set_title("Flagged Relationships", fontweight="bold"); usd(ax)
    fig.tight_layout(); savefig(fig, "38_billing_servicing.png", "fraud")
    return flagged

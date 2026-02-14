"""Providers — Network Analysis (Section 16)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, OUTPUT_DIR


def s16_provider_network(con, csv: str):
    """Billing ↔ servicing provider relationship analysis."""
    banner(16, "Provider Network (Billing ↔ Servicing)")

    billing_to_serv = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, COUNT(DISTINCT SERVICING_PROVIDER_NPI_NUM) AS num_servicing,
               SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' WHERE BILLING_PROVIDER_NPI_NUM != SERVICING_PROVIDER_NPI_NUM
        GROUP BY BILLING_PROVIDER_NPI_NUM HAVING num_servicing > 1 ORDER BY num_servicing DESC
    """)
    serv_to_billing = query(con, f"""
        SELECT SERVICING_PROVIDER_NPI_NUM, COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS num_billing,
               SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' WHERE BILLING_PROVIDER_NPI_NUM != SERVICING_PROVIDER_NPI_NUM
        GROUP BY SERVICING_PROVIDER_NPI_NUM HAVING num_billing > 1 ORDER BY num_billing DESC
    """)
    billing_to_serv.to_csv(OUTPUT_DIR / "16_billing_to_servicing.csv", index=False)
    serv_to_billing.to_csv(OUTPUT_DIR / "16_servicing_to_billing.csv", index=False)
    log.info("  Billing providers with multiple servicing: %d", len(billing_to_serv))
    log.info("  Max servicing per billing: %d", billing_to_serv["num_servicing"].max() if len(billing_to_serv) > 0 else 0)
    log.info("  Servicing providers with multiple billing: %d", len(serv_to_billing))

    top_orgs = billing_to_serv.head(30)
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    ax = axes[0]
    ax.hist(billing_to_serv["num_servicing"].clip(upper=50), bins=50, color="#1a73e8", edgecolor="white", alpha=0.85)
    ax.set_title("Servicing Providers per Billing Entity", fontsize=13, fontweight="bold"); ax.set_xlabel("# Servicing Providers"); ax.set_ylabel("Count")
    ax = axes[1]
    ax.hist(serv_to_billing["num_billing"].clip(upper=20), bins=20, color="#e8710a", edgecolor="white", alpha=0.85)
    ax.set_title("Billing Entities per Servicing Provider", fontsize=13, fontweight="bold"); ax.set_xlabel("# Billing Entities"); ax.set_ylabel("Count")
    ax = axes[2]
    if len(top_orgs) > 0:
        d = top_orgs.head(20).iloc[::-1]
        ax.barh(d["BILLING_PROVIDER_NPI_NUM"].astype(str), d["num_servicing"], color="#34a853", edgecolor="white")
        ax.set_title("Top Billing Orgs by Network Size", fontsize=13, fontweight="bold"); ax.set_xlabel("# Servicing Providers")
    fig.suptitle("Provider Network Analysis", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "16_provider_network.png")
    return billing_to_serv

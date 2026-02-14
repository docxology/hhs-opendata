"""Fraud Detection — Upcoding Detection (Section 33)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, save_csv, usd, OUTPUT_DIR


def s33_upcoding_detection(con, csv: str):
    """Detect providers billing systematically higher-cost codes than peers."""
    banner(33, "Upcoding Detection")

    upcoding = query(con, f"""
        WITH code_stats AS (
            SELECT HCPCS_CODE,
                   AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS peer_avg_cpc,
                   STDDEV(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS peer_std_cpc,
                   COUNT(*) AS n_providers
            FROM '{csv}' WHERE TOTAL_CLAIMS > 0
            GROUP BY HCPCS_CODE HAVING n_providers >= 20
        ),
        provider_deviation AS (
            SELECT r.BILLING_PROVIDER_NPI_NUM, r.HCPCS_CODE,
                   r.TOTAL_PAID / NULLIF(r.TOTAL_CLAIMS, 0) AS provider_cpc,
                   cs.peer_avg_cpc, cs.peer_std_cpc,
                   CASE WHEN cs.peer_std_cpc > 0
                        THEN (r.TOTAL_PAID / NULLIF(r.TOTAL_CLAIMS, 0) - cs.peer_avg_cpc) / cs.peer_std_cpc
                        ELSE 0 END AS z_score,
                   r.TOTAL_PAID, r.TOTAL_CLAIMS
            FROM '{csv}' r JOIN code_stats cs ON r.HCPCS_CODE = cs.HCPCS_CODE
            WHERE r.TOTAL_CLAIMS > 0
        )
        SELECT BILLING_PROVIDER_NPI_NUM,
               COUNT(*) AS n_codes, AVG(z_score) AS avg_z_score, MAX(z_score) AS max_z_score,
               SUM(CASE WHEN z_score > 2 THEN 1 ELSE 0 END) AS high_z_count,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims
        FROM provider_deviation GROUP BY BILLING_PROVIDER_NPI_NUM HAVING n_codes >= 3
    """)
    upcoding["upcode_ratio"] = upcoding["high_z_count"] / upcoding["n_codes"]
    upcoding["flag_upcoding"] = (upcoding["avg_z_score"] > 1.5) | (upcoding["upcode_ratio"] > 0.5)
    flagged = upcoding[upcoding["flag_upcoding"]].sort_values("avg_z_score", ascending=False)
    save_csv(upcoding, "33_upcoding_all.csv", "fraud")
    save_csv(flagged, "33_upcoding_flagged.csv", "fraud")
    log.info("  Flagged upcoding providers: %d / %d (%.1f%%)",
             len(flagged), len(upcoding), len(flagged)/max(len(upcoding),1)*100)

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Upcoding Detection — Billing Higher Than Peers", fontsize=15, fontweight="bold", y=1.02)
    ax = axes[0]
    ax.hist(upcoding["avg_z_score"].clip(-3, 5), bins=60, color="#ea4335", edgecolor="white", alpha=0.85)
    ax.axvline(1.5, color="black", linestyle="--", label="Flag threshold (z=1.5)"); ax.set_title("Avg Z-Score Distribution", fontweight="bold"); ax.set_xlabel("Avg Z-Score"); ax.legend()
    ax = axes[1]
    ax.hist(upcoding["upcode_ratio"].clip(0, 1), bins=50, color="#e8710a", edgecolor="white", alpha=0.85)
    ax.axvline(0.5, color="black", linestyle="--", label="Flag threshold (50%)"); ax.set_title("Upcode Ratio (codes >2σ / total)", fontweight="bold"); ax.legend()
    ax = axes[2]
    if len(flagged) > 0:
        sample = flagged.head(500)
        ax.scatter(sample["avg_z_score"], sample["total_paid"], alpha=0.4, s=15, color="#ea4335")
        ax.set_yscale("log"); ax.set_title("Flagged: Z-Score vs Spending", fontweight="bold"); ax.set_xlabel("Avg Z-Score"); usd(ax)
    fig.tight_layout(); savefig(fig, "33_upcoding.png", "fraud")
    return flagged

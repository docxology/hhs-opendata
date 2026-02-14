"""Statistics — Anomaly Detection (Section 6)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s06_anomaly_detection(con, csv: str, cost_df: pd.DataFrame):
    """Statistical anomaly detection using z-scores and Isolation Forest."""
    banner(6, "Anomaly Detection")

    log.info("  6a. Z-score outliers (z > 3 within each HCPCS code)...")
    anomalies_z = query(con, f"""
        WITH per_row AS (
            SELECT *, TOTAL_PAID / NULLIF(TOTAL_UNIQUE_BENEFICIARIES, 0) AS cpb
            FROM '{csv}' WHERE TOTAL_UNIQUE_BENEFICIARIES > 10
        ),
        stats AS (
            SELECT HCPCS_CODE, AVG(cpb) AS avg_cpb, STDDEV(cpb) AS std_cpb, COUNT(*) AS n
            FROM per_row GROUP BY HCPCS_CODE HAVING std_cpb > 0 AND n >= 20
        )
        SELECT r.BILLING_PROVIDER_NPI_NUM, r.HCPCS_CODE, r.CLAIM_FROM_MONTH,
               r.TOTAL_PAID, r.TOTAL_CLAIMS, r.TOTAL_UNIQUE_BENEFICIARIES,
               r.cpb AS cost_per_bene, s.avg_cpb, s.std_cpb,
               (r.cpb - s.avg_cpb) / s.std_cpb AS z_score
        FROM per_row r JOIN stats s ON r.HCPCS_CODE = s.HCPCS_CODE
        WHERE (r.cpb - s.avg_cpb) / s.std_cpb > 3
        ORDER BY z_score DESC LIMIT 500
    """)
    anomalies_z.to_csv(OUTPUT_DIR / "06a_anomalies_zscore.csv", index=False)
    log.info("    Z-score anomalies: %d", len(anomalies_z))

    log.info("  6b. Isolation Forest on provider-level aggregates...")
    provider_agg = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
               SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene,
               COUNT(DISTINCT HCPCS_CODE) AS procedure_count,
               COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months,
               AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS avg_cost_per_claim
        FROM '{csv}' WHERE TOTAL_CLAIMS > 0
        GROUP BY BILLING_PROVIDER_NPI_NUM HAVING total_paid > 1000
    """)

    features = ["total_paid", "total_claims", "total_bene", "procedure_count",
                "active_months", "avg_cost_per_claim"]
    X = provider_agg[features].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    provider_agg["anomaly_score"] = iso.fit_predict(X_scaled)
    provider_agg["anomaly_label"] = provider_agg["anomaly_score"].map({1: "normal", -1: "anomaly"})

    anomalies_if = provider_agg[provider_agg["anomaly_label"] == "anomaly"].sort_values("total_paid", ascending=False)
    anomalies_if.to_csv(OUTPUT_DIR / "06b_anomalies_isolation_forest.csv", index=False)
    log.info("    Isolation Forest anomalies: %d / %d providers (%.1f%%)",
             len(anomalies_if), len(provider_agg), 100 * len(anomalies_if) / len(provider_agg))

    fig, ax = plt.subplots(figsize=(12, 8))
    normal = provider_agg[provider_agg["anomaly_label"] == "normal"]
    anom = provider_agg[provider_agg["anomaly_label"] == "anomaly"]
    ax.scatter(normal["total_claims"], normal["total_paid"], alpha=0.3, s=5, color="#aaa", label="Normal")
    ax.scatter(anom["total_claims"], anom["total_paid"], alpha=0.7, s=15, color="#e8710a", label="Anomaly")
    ax.set_title("Provider Anomaly Detection (Isolation Forest)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Claims"); ax.set_ylabel("Total Paid (USD)")
    ax.set_xscale("log"); ax.set_yscale("log"); usd(ax); ax.legend(fontsize=11)
    fig.tight_layout(); savefig(fig, "06_anomaly_scatter.png")

    if len(anomalies_z) > 0:
        anom_by = anomalies_z.groupby("HCPCS_CODE").size().reset_index(name="count") \
                    .sort_values("count", ascending=False).head(15)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=anom_by.iloc[::-1], y="HCPCS_CODE", x="count", ax=ax, palette="Reds_r")
        ax.set_title("HCPCS Codes with Most Z-score Anomalies", fontsize=13, fontweight="bold")
        ax.set_xlabel("Count of Anomalous Provider Entries")
        fig.tight_layout(); savefig(fig, "06_zscore_by_procedure.png")

    return anomalies_z, anomalies_if

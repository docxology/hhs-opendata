"""Fraud Detection — Provider Clustering (Section 36)."""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from utils import log, banner, query, savefig, save_csv, OUTPUT_DIR


def s36_provider_clustering(con, csv: str):
    """Cluster providers by behavioral features to identify unusual profiles."""
    banner(36, "Provider Clustering (Unsupervised Profiling)")

    profiles = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM,
               SUM(TOTAL_PAID) AS total_paid, SUM(TOTAL_CLAIMS) AS total_claims,
               SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene,
               COUNT(DISTINCT HCPCS_CODE) AS n_codes, COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months,
               AVG(TOTAL_PAID / NULLIF(TOTAL_CLAIMS, 0)) AS avg_cpc,
               COUNT(DISTINCT SERVICING_PROVIDER_NPI_NUM) AS n_servicing
        FROM '{csv}' WHERE TOTAL_CLAIMS > 0 GROUP BY BILLING_PROVIDER_NPI_NUM HAVING total_paid > 1000
    """)
    features = ["total_paid", "total_claims", "total_bene", "n_codes", "active_months", "avg_cpc", "n_servicing"]
    X = profiles[features].fillna(0)
    X_log = np.log1p(X)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)
    n_clusters = 6
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
    profiles["cluster"] = kmeans.fit_predict(X_scaled)
    cluster_sizes = profiles["cluster"].value_counts()
    cluster_stats = profiles.groupby("cluster").agg(
        count=("BILLING_PROVIDER_NPI_NUM", "count"), avg_paid=("total_paid", "mean"),
        avg_claims=("total_claims", "mean"), avg_cpc=("avg_cpc", "mean"), avg_codes=("n_codes", "mean"),
    ).reset_index()
    cluster_stats["pct"] = cluster_stats["count"] / cluster_stats["count"].sum() * 100
    save_csv(profiles, "36_provider_clusters.csv", "fraud")
    save_csv(cluster_stats, "36_cluster_stats.csv", "fraud")
    log.info("  Clusters: %s", ", ".join(f"C{c}: {n} providers" for c, n in cluster_sizes.sort_index().items()))

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Provider Clustering — Behavioral Profiles", fontsize=15, fontweight="bold", y=1.02)
    colors = plt.cm.Set1(np.linspace(0, 0.8, n_clusters))
    ax = axes[0]
    for c in range(n_clusters):
        mask = profiles["cluster"] == c
        ax.scatter(np.log10(profiles.loc[mask, "total_paid"].clip(lower=1)),
                   np.log10(profiles.loc[mask, "total_claims"].clip(lower=1)), alpha=0.15, s=5, color=colors[c], label=f"C{c}")
    ax.set_title("Clusters: Paid vs Claims (log₁₀)", fontweight="bold"); ax.set_xlabel("log₁₀(Total Paid)"); ax.set_ylabel("log₁₀(Total Claims)"); ax.legend(fontsize=7)
    ax = axes[1]
    ax.bar(cluster_stats["cluster"].astype(str), cluster_stats["pct"], color=colors, edgecolor="white")
    ax.set_title("Cluster Size Distribution", fontweight="bold"); ax.set_ylabel("% of Providers")
    ax = axes[2]
    for c in range(n_clusters):
        mask = profiles["cluster"] == c
        ax.scatter(np.log10(profiles.loc[mask, "avg_cpc"].clip(lower=0.01)), profiles.loc[mask, "n_codes"],
                   alpha=0.15, s=5, color=colors[c], label=f"C{c}")
    ax.set_title("Clusters: Avg CPC vs # Codes", fontweight="bold"); ax.set_xlabel("log₁₀(Avg Cost/Claim)"); ax.set_ylabel("# HCPCS Codes"); ax.legend(fontsize=7)
    fig.tight_layout(); savefig(fig, "36_provider_clusters.png", "fraud")
    return profiles

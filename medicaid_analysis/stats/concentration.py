"""Statistics — Market Concentration & Spending Deciles (Sections 8 & 18)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def s08_concentration(con, csv: str):
    """Provider and procedure market concentration (Lorenz / Gini / HHI)."""
    banner(8, "Market Concentration Analysis")

    prov_spend = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM ORDER BY total_paid
    """)
    prov_vals = prov_spend["total_paid"].values
    prov_cum = np.cumsum(prov_vals) / prov_vals.sum()
    prov_pct = np.arange(1, len(prov_vals) + 1) / len(prov_vals)

    n = len(prov_vals)
    gini = (2 * np.sum((np.arange(1, n+1)) * np.sort(prov_vals)) / (n * np.sum(prov_vals))) - (n + 1) / n
    log.info("  Provider Gini coefficient: %.4f", gini)

    total = prov_vals.sum()
    top10_share = prov_vals[-10:].sum() / total * 100
    top100_share = prov_vals[-100:].sum() / total * 100
    log.info("  Top 10 providers:  %.1f%% of all spending", top10_share)
    log.info("  Top 100 providers: %.1f%% of all spending", top100_share)

    proc_spend = query(con, f"""
        SELECT HCPCS_CODE, SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' GROUP BY HCPCS_CODE ORDER BY total_paid
    """)
    proc_vals = proc_spend["total_paid"].values
    proc_cum = np.cumsum(proc_vals) / proc_vals.sum()
    proc_pct = np.arange(1, len(proc_vals) + 1) / len(proc_vals)
    proc_gini = (2 * np.sum((np.arange(1, len(proc_vals)+1)) * np.sort(proc_vals)) /
                 (len(proc_vals) * np.sum(proc_vals))) - (len(proc_vals) + 1) / len(proc_vals)
    log.info("  Procedure Gini coefficient: %.4f", proc_gini)

    conc = pd.DataFrame({
        "metric": ["provider_gini", "procedure_gini", "top10_provider_share", "top100_provider_share"],
        "value": [gini, proc_gini, top10_share, top100_share],
    })
    conc.to_csv(OUTPUT_DIR / "08_concentration_metrics.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Spending Concentration (Lorenz Curves)", fontsize=15, fontweight="bold", y=1.02)
    for ax, pct, cum, label, g in [
        (axes[0], prov_pct, prov_cum, "Provider", gini),
        (axes[1], proc_pct, proc_cum, "Procedure (HCPCS)", proc_gini),
    ]:
        ax.plot(pct, cum, color="#1a73e8", linewidth=2, label="Lorenz curve")
        ax.plot([0, 1], [0, 1], "--", color="#aaa", label="Perfect equality")
        ax.fill_between(pct, cum, pct, alpha=0.15, color="#1a73e8")
        ax.set_title(f"{label} Concentration (Gini={g:.3f})", fontsize=13, fontweight="bold")
        ax.set_xlabel(f"Cumulative % of {label}s"); ax.set_ylabel("Cumulative % of Spending"); ax.legend()
    fig.tight_layout(); savefig(fig, "08_lorenz_curves.png")
    return conc


def s18_spending_deciles(con, csv: str):
    """Spending inequality via provider decile analysis."""
    banner(18, "Spending Decile & Inequality Analysis")

    prov = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, SUM(TOTAL_PAID) AS total_paid,
               SUM(TOTAL_CLAIMS) AS total_claims
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM HAVING total_paid > 0
    """)

    prov["decile"] = pd.qcut(prov["total_paid"], 10, labels=[f"D{i}" for i in range(1, 11)])
    decile_summary = prov.groupby("decile", observed=True).agg(
        provider_count=("BILLING_PROVIDER_NPI_NUM", "count"),
        total_paid=("total_paid", "sum"), avg_paid=("total_paid", "mean"),
        median_paid=("total_paid", "median"), min_paid=("total_paid", "min"),
        max_paid=("total_paid", "max"), total_claims=("total_claims", "sum"),
    ).reset_index()
    decile_summary["pct_of_total"] = decile_summary["total_paid"] / decile_summary["total_paid"].sum() * 100
    decile_summary.to_csv(OUTPUT_DIR / "18_spending_deciles.csv", index=False)
    log.info("  Top decile (D10): %.1f%% of total spending", decile_summary.iloc[-1]["pct_of_total"])
    log.info("  Bottom decile (D1): %.1f%% of total spending", decile_summary.iloc[0]["pct_of_total"])

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    ax = axes[0]
    ax.bar(decile_summary["decile"].astype(str), decile_summary["pct_of_total"],
           color=plt.cm.RdYlGn_r(np.linspace(0, 1, 10)), edgecolor="white")
    ax.set_title("% of Total Spending by Provider Decile", fontsize=13, fontweight="bold")
    ax.set_xlabel("Decile"); ax.set_ylabel("% of Total Spending")
    for i, row in decile_summary.iterrows():
        ax.text(i, row["pct_of_total"] + 0.3, f"{row['pct_of_total']:.1f}%", ha="center", fontsize=8, fontweight="bold")

    ax = axes[1]
    ax.bar(decile_summary["decile"].astype(str), decile_summary["avg_paid"], color="#1a73e8", edgecolor="white")
    ax.set_title("Average Provider Spending by Decile", fontsize=13, fontweight="bold")
    ax.set_xlabel("Decile"); ax.set_ylabel("Avg Paid (USD)"); usd(ax)

    ax = axes[2]
    ratio = decile_summary.iloc[-1]["avg_paid"] / decile_summary.iloc[0]["avg_paid"]
    labels = [f"D{i}" for i in range(1, 11)]
    ax.semilogy(labels, decile_summary["avg_paid"], "o-", color="#9334e6", linewidth=2, markersize=8)
    ax.set_title(f"Decile Avg Spending (log, D10/D1 = {ratio:,.0f}x)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Decile"); ax.set_ylabel("Avg Paid (USD, log)"); usd(ax)

    fig.suptitle("Provider Spending Inequality", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "18_spending_deciles.png")
    return decile_summary

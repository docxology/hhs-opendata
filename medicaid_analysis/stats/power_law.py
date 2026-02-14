"""Statistics — Power-Law / Pareto Analysis (Section 15)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, OUTPUT_DIR


def s15_power_law(con, csv: str):
    """Power-law / Pareto distribution analysis of spending."""
    banner(15, "Power-Law & Pareto Analysis")

    prov = query(con, f"""
        SELECT BILLING_PROVIDER_NPI_NUM, SUM(TOTAL_PAID) AS total_paid
        FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM
        HAVING total_paid > 0 ORDER BY total_paid DESC
    """)
    vals = prov["total_paid"].values
    n = len(vals)
    ranks = np.arange(1, n + 1)

    cum = np.cumsum(vals) / vals.sum() * 100
    p20_share = cum[int(n * 0.2) - 1] if n > 5 else 0
    log.info("  Top 1%% of providers: %.1f%% of spending", cum[int(n * 0.01)] if n > 100 else 0)
    log.info("  Top 5%% of providers: %.1f%% of spending", cum[int(n * 0.05)] if n > 20 else 0)
    log.info("  Top 20%% of providers: %.1f%% of spending", p20_share)

    log_rank = np.log10(ranks[:int(n * 0.9)])
    log_vals = np.log10(vals[:int(n * 0.9)])
    slope, intercept = np.polyfit(log_rank, log_vals, 1)
    log.info("  Power-law exponent (slope): %.3f", slope)

    pareto_stats = pd.DataFrame({
        "metric": ["top_1pct_share", "top_5pct_share", "top_20pct_share", "power_law_exponent"],
        "value": [cum[int(n * 0.01)] if n > 100 else 0,
                  cum[int(n * 0.05)] if n > 20 else 0, p20_share, slope],
    })
    pareto_stats.to_csv(OUTPUT_DIR / "15_pareto_stats.csv", index=False)

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle("Power-Law & Pareto Analysis (Provider Spending)", fontsize=15, fontweight="bold", y=1.02)

    ax = axes[0]
    ax.scatter(ranks, vals, s=1, alpha=0.4, color="#1a73e8")
    fit_line = 10 ** (slope * np.log10(ranks) + intercept)
    ax.plot(ranks, fit_line, color="#ea4335", linewidth=2, linestyle="--", label=f"Power law (α={slope:.2f})")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_title("Rank-Size Distribution", fontsize=13, fontweight="bold")
    ax.set_xlabel("Rank"); ax.set_ylabel("Total Paid (USD)"); ax.legend()

    ax = axes[1]
    ax.plot(np.arange(1, n + 1) / n * 100, cum, color="#1a73e8", linewidth=2)
    ax.axhline(80, color="#aaa", linestyle="--", alpha=0.7)
    ax.axvline(20, color="#aaa", linestyle="--", alpha=0.7)
    ax.set_title("Cumulative Spending Share", fontsize=13, fontweight="bold")
    ax.set_xlabel("% of Providers (ranked)"); ax.set_ylabel("% of Total Spending")

    ax = axes[2]
    sorted_vals = np.sort(vals)[::-1]
    ccdf = np.arange(1, n + 1) / n
    ax.scatter(sorted_vals, ccdf, s=1, alpha=0.3, color="#e8710a")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_title("CCDF (Complementary CDF)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Spending Threshold (USD)"); ax.set_ylabel("P(X > x)")

    fig.tight_layout(); savefig(fig, "15_power_law.png")
    return pareto_stats

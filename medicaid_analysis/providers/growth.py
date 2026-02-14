"""Providers — Growth Trajectories (Section 13)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, OUTPUT_DIR


def s13_provider_growth(con, csv: str):
    """Provider spending growth trajectories — fastest-growing and declining."""
    banner(13, "Provider Growth & Trajectory Analysis")

    growth = query(con, f"""
        WITH halves AS (
            SELECT BILLING_PROVIDER_NPI_NUM,
                SUM(CASE WHEN CLAIM_FROM_MONTH < '2021-07' THEN TOTAL_PAID ELSE 0 END) AS early_paid,
                SUM(CASE WHEN CLAIM_FROM_MONTH >= '2021-07' THEN TOTAL_PAID ELSE 0 END) AS late_paid,
                SUM(TOTAL_PAID) AS total_paid,
                COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months
            FROM '{csv}' GROUP BY BILLING_PROVIDER_NPI_NUM
            HAVING early_paid > 10000 AND late_paid > 10000 AND active_months >= 12
        )
        SELECT *, (late_paid - early_paid) / NULLIF(early_paid, 0) * 100 AS growth_pct,
                  late_paid - early_paid AS growth_abs
        FROM halves ORDER BY growth_pct DESC
    """)
    growth.to_csv(OUTPUT_DIR / "13_provider_growth.csv", index=False)
    log.info("  Providers with growth data: %d", len(growth))
    log.info("  Median growth: %.1f%%", growth["growth_pct"].median())

    top_growers = growth.head(20)
    top_decliners = growth.tail(20).iloc[::-1]

    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    ax = axes[0]
    clipped = growth["growth_pct"].clip(-200, 500)
    ax.hist(clipped, bins=80, color="#1a73e8", alpha=0.8, edgecolor="white")
    ax.axvline(0, color="red", linestyle="--", linewidth=1.5)
    ax.axvline(growth["growth_pct"].median(), color="#34a853", linestyle="--", linewidth=1.5,
               label=f"Median: {growth['growth_pct'].median():.0f}%")
    ax.set_title("Provider Growth Distribution (Early vs Late Half)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Growth %"); ax.set_ylabel("Provider Count"); ax.legend()

    ax = axes[1]
    ax.barh(range(len(top_growers)), top_growers["growth_pct"].values, color="#34a853", edgecolor="white")
    ax.set_yticks(range(len(top_growers)))
    ax.set_yticklabels(top_growers["BILLING_PROVIDER_NPI_NUM"].astype(str), fontsize=7)
    ax.set_title("Top 20 Fastest-Growing Providers", fontsize=13, fontweight="bold"); ax.set_xlabel("Growth %")

    ax = axes[2]
    ax.barh(range(len(top_decliners)), top_decliners["growth_pct"].values, color="#ea4335", edgecolor="white")
    ax.set_yticks(range(len(top_decliners)))
    ax.set_yticklabels(top_decliners["BILLING_PROVIDER_NPI_NUM"].astype(str), fontsize=7)
    ax.set_title("Top 20 Fastest-Declining Providers", fontsize=13, fontweight="bold"); ax.set_xlabel("Growth %")

    fig.tight_layout(); savefig(fig, "13_provider_growth.png")
    return growth

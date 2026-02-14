"""Procedures — Claims Size Distribution (Section 26)."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import log, banner, query, savefig, num_fmt, OUTPUT_DIR


def s26_claims_size_distribution(con, csv: str):
    """Claims size stratification — micro, small, medium, large, mega."""
    banner(26, "Claims Size Distribution")

    buckets = query(con, f"""
        SELECT
            CASE
                WHEN TOTAL_PAID < 100        THEN '1. Micro (<$100)'
                WHEN TOTAL_PAID < 1000       THEN '2. Small ($100-$1K)'
                WHEN TOTAL_PAID < 10000      THEN '3. Medium ($1K-$10K)'
                WHEN TOTAL_PAID < 100000     THEN '4. Large ($10K-$100K)'
                WHEN TOTAL_PAID < 1000000    THEN '5. Very Large ($100K-$1M)'
                ELSE '6. Mega (>$1M)'
            END AS size_bucket,
            COUNT(*) AS record_count, SUM(TOTAL_PAID) AS total_paid, AVG(TOTAL_PAID) AS avg_paid,
            SUM(TOTAL_CLAIMS) AS total_claims, SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_bene
        FROM '{csv}' GROUP BY size_bucket ORDER BY size_bucket
    """)
    buckets["pct_records"] = buckets["record_count"] / buckets["record_count"].sum() * 100
    buckets["pct_spending"] = buckets["total_paid"] / buckets["total_paid"].sum() * 100
    buckets.to_csv(OUTPUT_DIR / "26_claims_size_buckets.csv", index=False)
    log.info("  Buckets:\n%s", buckets[["size_bucket", "pct_records", "pct_spending"]].to_string(index=False))

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    labels = [b.split(". ")[1] for b in buckets["size_bucket"]]
    ax = axes[0]
    ax.bar(labels, buckets["pct_records"], color="#1a73e8", edgecolor="white")
    ax.set_title("% of Records by Size", fontsize=13, fontweight="bold"); ax.set_ylabel("%"); ax.tick_params(axis="x", rotation=30)
    for i, v in enumerate(buckets["pct_records"]):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=8, fontweight="bold")
    ax = axes[1]
    ax.bar(labels, buckets["pct_spending"], color="#e8710a", edgecolor="white")
    ax.set_title("% of Spending by Size", fontsize=13, fontweight="bold"); ax.set_ylabel("%"); ax.tick_params(axis="x", rotation=30)
    for i, v in enumerate(buckets["pct_spending"]):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=8, fontweight="bold")
    ax = axes[2]
    ax.bar(labels, buckets["record_count"], color="#34a853", edgecolor="white")
    ax.set_title("Record Count by Size", fontsize=13, fontweight="bold"); ax.set_ylabel("Records"); ax.tick_params(axis="x", rotation=30)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(num_fmt))
    fig.suptitle("Claims Size Distribution", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "26_claims_size.png")
    return buckets

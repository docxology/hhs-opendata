"""EDA — Exploratory Data Analysis Summary (Section 1)."""

import time
import json
import pandas as pd
from utils import log, banner, query, OUTPUT_DIR


def s01_eda(con, csv: str) -> dict:
    """Exploratory Data Analysis — shape, types, cardinal counts, and numeric summaries."""
    banner(1, "Exploratory Data Analysis")
    t0 = time.time()

    row_count = con.execute(f"SELECT COUNT(*) FROM '{csv}'").fetchone()[0]
    log.info("Rows: %s (%.1fs scan)", f"{row_count:,}", time.time() - t0)

    date_range = con.execute(
        f"SELECT MIN(CLAIM_FROM_MONTH) AS mn, MAX(CLAIM_FROM_MONTH) AS mx FROM '{csv}'"
    ).fetchone()
    log.info("Date range: %s → %s", date_range[0], date_range[1])

    uniques = query(con, f"""
        SELECT
            COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM)   AS billing_npis,
            COUNT(DISTINCT SERVICING_PROVIDER_NPI_NUM) AS servicing_npis,
            COUNT(DISTINCT HCPCS_CODE)                 AS hcpcs_codes
        FROM '{csv}'
    """)
    for col in uniques.columns:
        log.info("  %s: %s", col, f"{uniques.iloc[0][col]:,}")

    nums = query(con, f"""
        SELECT
            SUM(TOTAL_PAID)                            AS total_paid,
            AVG(TOTAL_PAID)                            AS avg_paid,
            MEDIAN(TOTAL_PAID)                         AS median_paid,
            MAX(TOTAL_PAID)                            AS max_paid,
            MIN(TOTAL_PAID)                            AS min_paid,
            STDDEV(TOTAL_PAID)                         AS std_paid,
            SUM(TOTAL_CLAIMS)                          AS total_claims,
            AVG(TOTAL_CLAIMS)                          AS avg_claims,
            SUM(TOTAL_UNIQUE_BENEFICIARIES)            AS total_bene,
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY TOTAL_PAID) AS p25_paid,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY TOTAL_PAID) AS p75_paid,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY TOTAL_PAID) AS p95_paid,
            PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY TOTAL_PAID) AS p99_paid
        FROM '{csv}'
    """)
    log.info("  Total paid:  $%s", f"{nums.iloc[0]['total_paid']:,.2f}")
    log.info("  Mean paid:   $%s", f"{nums.iloc[0]['avg_paid']:,.2f}")
    log.info("  Median paid: $%s", f"{nums.iloc[0]['median_paid']:,.2f}")
    log.info("  Std paid:    $%s", f"{nums.iloc[0]['std_paid']:,.2f}")
    log.info("  P25/P75/P95/P99: $%.0f / $%.0f / $%.0f / $%.0f",
             nums.iloc[0]['p25_paid'], nums.iloc[0]['p75_paid'],
             nums.iloc[0]['p95_paid'], nums.iloc[0]['p99_paid'])

    summary = {
        "row_count": int(row_count),
        "date_min": str(date_range[0]),
        "date_max": str(date_range[1]),
        **{k: float(v) for k, v in nums.iloc[0].items()},
        **{k: int(v) for k, v in uniques.iloc[0].items()},
    }
    nums.to_csv(OUTPUT_DIR / "01_numeric_summary.csv", index=False)
    with open(OUTPUT_DIR / "01_eda_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    pd.DataFrame([summary]).T.to_csv(OUTPUT_DIR / "01_summary_statistics.csv")
    return summary


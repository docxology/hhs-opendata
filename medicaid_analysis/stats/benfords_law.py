"""Statistics — Benford's Law Analysis (Section 31)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats
from utils import log, banner, query, savefig, OUTPUT_DIR


def s31_benfords_law(con, csv: str):
    """Benford's Law analysis — first-digit distribution as fraud signal."""
    banner(31, "Benford's Law Analysis")

    first_digits = query(con, f"""
        SELECT
            CAST(SUBSTR(CAST(CAST(ABS(FLOOR(TOTAL_PAID)) AS BIGINT) AS VARCHAR), 1, 1) AS INTEGER) AS first_digit,
            COUNT(*) AS observed_count
        FROM '{csv}'
        WHERE TOTAL_PAID >= 10
        GROUP BY first_digit
        HAVING first_digit BETWEEN 1 AND 9
        ORDER BY first_digit
    """)

    total = first_digits["observed_count"].sum()
    first_digits["observed_pct"] = first_digits["observed_count"] / total * 100
    first_digits["benford_pct"] = [np.log10(1 + 1/d) * 100 for d in first_digits["first_digit"]]
    first_digits["deviation"] = first_digits["observed_pct"] - first_digits["benford_pct"]
    first_digits["deviation_abs"] = first_digits["deviation"].abs()

    expected = np.array([np.log10(1 + 1/d) for d in range(1, 10)]) * total
    observed = first_digits["observed_count"].values
    chi2 = np.sum((observed - expected) ** 2 / expected)
    p_value = 1 - scipy_stats.chi2.cdf(chi2, df=8)
    mad = first_digits["deviation_abs"].mean()

    benford_stats = pd.DataFrame({
        "metric": ["chi_squared", "p_value", "mean_abs_deviation", "conformity"],
        "value": [chi2, p_value, mad, "Close" if mad < 1.5 else ("Marginal" if mad < 3.0 else "Non-conforming")],
    })
    first_digits.to_csv(OUTPUT_DIR / "31_benfords_law.csv", index=False)
    benford_stats.to_csv(OUTPUT_DIR / "31_benford_stats.csv", index=False)
    log.info("  Chi-squared: %.2f (p=%.4f)", chi2, p_value)
    log.info("  MAD: %.4f (%s)", mad, benford_stats.iloc[3]["value"])

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle("Benford's Law Analysis (First-Digit Distribution)", fontsize=15, fontweight="bold", y=1.02)
    digits = first_digits["first_digit"].values.astype(str)

    ax = axes[0]
    width = 0.35; x = np.arange(len(digits))
    ax.bar(x - width/2, first_digits["observed_pct"], width, label="Observed", color="#1a73e8", edgecolor="white")
    ax.bar(x + width/2, first_digits["benford_pct"], width, label="Benford Expected", color="#e8710a", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(digits)
    ax.set_title("Observed vs Expected", fontsize=13, fontweight="bold")
    ax.set_xlabel("First Digit"); ax.set_ylabel("% of Records"); ax.legend()

    ax = axes[1]
    colors_dev = ["#34a853" if d < 1.0 else ("#e8710a" if d < 2.0 else "#ea4335") for d in first_digits["deviation_abs"]]
    ax.bar(digits, first_digits["deviation"], color=colors_dev, edgecolor="white")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("Deviation from Benford's Law", fontsize=13, fontweight="bold")
    ax.set_xlabel("First Digit"); ax.set_ylabel("Deviation (pp)")

    ax = axes[2]
    ax.plot(first_digits["observed_pct"], first_digits["benford_pct"], "o", color="#9334e6", markersize=10)
    for _, row in first_digits.iterrows():
        ax.annotate(str(int(row["first_digit"])), (row["observed_pct"], row["benford_pct"]),
                    textcoords="offset points", xytext=(7, 0), fontsize=10)
    lims = [0, max(first_digits["observed_pct"].max(), first_digits["benford_pct"].max()) + 2]
    ax.plot(lims, lims, "--", color="#aaa")
    ax.set_title(f"Q-Q: Observed vs Benford (MAD={mad:.2f})", fontsize=13, fontweight="bold")
    ax.set_xlabel("Observed %"); ax.set_ylabel("Benford Expected %")

    fig.tight_layout(); savefig(fig, "31_benfords_law.png")
    return first_digits

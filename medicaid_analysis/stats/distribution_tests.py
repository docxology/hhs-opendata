"""Statistics — Distribution Tests (Section 17)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats
from utils import log, banner, savefig, OUTPUT_DIR


def s17_statistical_tests(con, csv: str, cost_df: pd.DataFrame):
    """Statistical distribution tests — skewness, kurtosis, normality."""
    banner(17, "Statistical Distribution Tests")

    metrics = {
        "TOTAL_PAID": cost_df["TOTAL_PAID"],
        "TOTAL_CLAIMS": cost_df["TOTAL_CLAIMS"],
        "cost_per_claim": cost_df["cost_per_claim"],
        "cost_per_beneficiary": cost_df["cost_per_beneficiary"],
    }

    results = []
    for name, vals in metrics.items():
        v = vals.dropna()
        n = len(v)
        skew = float(v.skew())
        kurt = float(v.kurtosis())
        sample = v.sample(n=min(50_000, n), random_state=42).values
        try:
            _, p_normal = scipy_stats.normaltest(sample)
        except Exception:
            p_normal = 0.0
        log_v = np.log1p(v[v > 0])
        log_skew = float(log_v.skew())
        results.append({
            "metric": name, "n": n, "skewness": skew, "kurtosis": kurt,
            "p_normal": p_normal, "is_normal": p_normal > 0.05, "log_skewness": log_skew,
        })
        log.info("  %s: skew=%.2f, kurt=%.2f, p_normal=%.2e, log_skew=%.2f",
                 name, skew, kurt, p_normal, log_skew)

    stats_df = pd.DataFrame(results)
    stats_df.to_csv(OUTPUT_DIR / "17_statistical_tests.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("Log-Transformed Q-Q Plots", fontsize=15, fontweight="bold", y=1.01)
    for ax, (name, vals) in zip(axes.flat, metrics.items()):
        v = vals.dropna()
        log_v = np.log1p(v[v > 0]).sample(n=min(10_000, len(v)), random_state=42)
        scipy_stats.probplot(log_v, dist="norm", plot=ax)
        ax.set_title(f"QQ: log({name})", fontsize=12, fontweight="bold")
        ax.get_lines()[0].set(markersize=2, alpha=0.4)
    fig.tight_layout(); savefig(fig, "17_qq_plots.png")
    return stats_df

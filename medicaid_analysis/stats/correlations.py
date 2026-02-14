"""Statistics — Correlation Analysis (Section 9)."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import log, banner, savefig, OUTPUT_DIR


def s09_correlations(con, csv: str, cost_df: pd.DataFrame):
    """Correlation analysis between numeric variables."""
    banner(9, "Correlation Analysis")

    cols = ["TOTAL_PAID", "TOTAL_CLAIMS", "TOTAL_UNIQUE_BENEFICIARIES",
            "cost_per_claim", "cost_per_beneficiary"]
    corr_data = cost_df[cols].dropna()

    corr_pearson = corr_data.corr(method="pearson")
    corr_pearson.to_csv(OUTPUT_DIR / "09_correlation_pearson.csv")
    corr_spearman = corr_data.corr(method="spearman")
    corr_spearman.to_csv(OUTPUT_DIR / "09_correlation_spearman.csv")

    log.info("  Pearson(TOTAL_PAID, TOTAL_CLAIMS): %.4f", corr_pearson.loc["TOTAL_PAID", "TOTAL_CLAIMS"])
    log.info("  Spearman(TOTAL_PAID, TOTAL_CLAIMS): %.4f", corr_spearman.loc["TOTAL_PAID", "TOTAL_CLAIMS"])

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    short = {"TOTAL_PAID": "Paid", "TOTAL_CLAIMS": "Claims",
             "TOTAL_UNIQUE_BENEFICIARIES": "Bene", "cost_per_claim": "$/Claim",
             "cost_per_beneficiary": "$/Bene"}
    for ax, corr, title in [
        (axes[0], corr_pearson, "Pearson Correlation"),
        (axes[1], corr_spearman, "Spearman Correlation"),
    ]:
        corr_r = corr.rename(index=short, columns=short)
        sns.heatmap(corr_r, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                    square=True, ax=ax, vmin=-1, vmax=1, cbar_kws={"shrink": 0.8}, linewidths=0.5)
        ax.set_title(title, fontsize=13, fontweight="bold")
    fig.suptitle("Correlation Between Spending Metrics", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout(); savefig(fig, "09_correlations.png")

    sample_n = min(50_000, len(corr_data))
    sample_df = corr_data.sample(n=sample_n, random_state=42).rename(columns=short)
    fig = sns.pairplot(sample_df, diag_kind="kde", plot_kws={"alpha": 0.15, "s": 3}, corner=True, height=2.2)
    fig.figure.suptitle("Pairwise Relationships (sampled)", fontsize=14, fontweight="bold", y=1.02)
    savefig(fig.figure, "09_pairplot.png")

    return corr_pearson, corr_spearman

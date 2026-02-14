"""
Medicaid Analysis — I/O Helpers (save figures, CSVs, logging banners)
"""

import pandas as pd
import matplotlib.pyplot as plt
from .config import log, PLOTS_DIR, OUTPUT_DIR


def savefig(fig, name: str, subdir: str = None):
    """Save a matplotlib figure to the plots directory (or a subdirectory)."""
    target = PLOTS_DIR / subdir if subdir else PLOTS_DIR
    target.mkdir(parents=True, exist_ok=True)
    path = target / name
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.info("  → %s", path.name)


def save_csv(df: pd.DataFrame, name: str, subdir: str = None):
    """Save a DataFrame to CSV in the output directory."""
    target = OUTPUT_DIR / subdir if subdir else OUTPUT_DIR
    target.mkdir(parents=True, exist_ok=True)
    path = target / name
    df.to_csv(path, index=False)
    log.info("  → %s", path.name)
    return path


def banner(n, title: str):
    """Print a section banner to the log."""
    log.info("═══ %s. %s ═══", str(n), title)

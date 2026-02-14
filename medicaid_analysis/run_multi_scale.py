#!/usr/bin/env python3
"""
Multi-Scale Analysis Runner
============================
Runs the full analysis pipeline at 1%, 10%, 50%, and 100% data scales,
outputting into percentage-based subfolders under `output/`.

Usage:
    uv run run_multi_scale.py                     # Run all 4 scales
    uv run run_multi_scale.py --scales 1 10       # Run only 1% and 10%
    uv run run_multi_scale.py --skip-fraud        # Pass --skip-fraud to each run
"""

import argparse
import os
import subprocess
import sys
import time
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
OUTPUT_ROOT = BASE_DIR / "output"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("multi_scale")

# ── Scale definitions ──────────────────────────────────────────────────────
SCALES = {
    1:   {"csv": DATA_DIR / "sample.csv",                  "label": "1pct"},
    10:  {"csv": DATA_DIR / "sample_10pct.csv",            "label": "10pct"},
    50:  {"csv": DATA_DIR / "sample_50pct.csv",            "label": "50pct"},
    100: {"csv": DATA_DIR / "medicaid-provider-spending.csv", "label": "100pct"},
}


def ensure_sample(pct: int):
    """Create the sample CSV if it does not exist."""
    info = SCALES[pct]
    csv_path = info["csv"]
    if csv_path.exists():
        size_mb = csv_path.stat().st_size / (1024 * 1024)
        log.info("  Sample %d%% already exists: %s (%.0f MB)", pct, csv_path.name, size_mb)
        return True

    if pct == 100:
        log.error("  Full dataset not found: %s", csv_path)
        return False

    # Generate via create_sample.py
    log.info("  Creating %d%% sample...", pct)
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "create_sample.py"), "--pct", str(pct)],
        cwd=str(BASE_DIR),
    )
    if result.returncode != 0:
        log.error("  Failed to create %d%% sample", pct)
        return False

    if not csv_path.exists():
        log.error("  Sample file not created at expected path: %s", csv_path)
        return False
    size_mb = csv_path.stat().st_size / (1024 * 1024)
    log.info("  ✓ Created %s (%.0f MB)", csv_path.name, size_mb)
    return True


def run_pipeline(pct: int, extra_args: list[str] | None = None):
    """Run the full pipeline for a given scale."""
    info = SCALES[pct]
    csv_path = info["csv"]
    label = info["label"]

    output_dir = OUTPUT_ROOT / label
    plots_dir = BASE_DIR / "plots" / label

    log.info("─" * 72)
    log.info("SCALE: %d%%  →  output/%s", pct, label)
    log.info("─" * 72)

    env = os.environ.copy()
    env["MEDICAID_OUTPUT_DIR"] = str(output_dir)
    env["MEDICAID_PLOTS_DIR"] = str(plots_dir)

    cmd = [sys.executable, str(BASE_DIR / "main.py"), "--csv", str(csv_path)]
    if extra_args:
        cmd.extend(extra_args)

    t0 = time.time()
    result = subprocess.run(cmd, cwd=str(BASE_DIR), env=env)
    elapsed = time.time() - t0

    status = "✓ PASSED" if result.returncode == 0 else "✗ FAILED"
    log.info("  %s  %d%% completed in %.1f minutes", status, pct, elapsed / 60)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run analysis at multiple data scales")
    parser.add_argument("--scales", nargs="*", type=int, default=[1, 10, 50, 100],
                        help="Percentage scales to run (default: 1 10 50 100)")
    parser.add_argument("--skip-fraud", action="store_true",
                        help="Pass --skip-fraud to each pipeline run")
    args = parser.parse_args()

    log.info("=" * 72)
    log.info("MULTI-SCALE ANALYSIS RUNNER")
    log.info("Scales: %s", ", ".join(f"{s}%%" for s in args.scales))
    log.info("=" * 72)

    t_start = time.time()
    results = {}

    for pct in args.scales:
        if pct not in SCALES:
            log.error("Unknown scale: %d%%  (valid: %s)", pct, list(SCALES.keys()))
            results[pct] = False
            continue

        if not ensure_sample(pct):
            results[pct] = False
            continue

        extra = ["--skip-fraud"] if args.skip_fraud else None
        results[pct] = run_pipeline(pct, extra)

    # ── Summary ──────────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    log.info("")
    log.info("=" * 72)
    log.info("MULTI-SCALE SUMMARY — %.1f minutes total", elapsed / 60)
    log.info("=" * 72)
    for pct, ok in results.items():
        status = "✓ PASSED" if ok else "✗ FAILED"
        log.info("  %3d%%  %s  →  output/%s/", pct, status, SCALES[pct]["label"])
    log.info("=" * 72)

    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

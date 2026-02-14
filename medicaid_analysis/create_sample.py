"""
Create stratified samples at configurable percentages of the full dataset.

Usage:
    uv run create_sample.py                    # Default 1% sample
    uv run create_sample.py --pct 1 10         # Create 1% and 10% samples
    uv run create_sample.py --pct 0.1 1 10     # Create 0.1%, 1%, and 10%
"""

import argparse
import duckdb
import logging
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FULL_CSV = DATA_DIR / "medicaid-provider-spending.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("sampler")


def create_sample(con, full_csv: Path, pct: float, output_path: Path):
    """Create a Bernoulli sample at the given percentage."""
    log.info("Creating %.1f%% sample → %s", pct, output_path.name)
    t0 = time.time()
    con.execute(f"""
        COPY (
            SELECT * FROM '{full_csv}'
            USING SAMPLE {pct} PERCENT (bernoulli)
        ) TO '{output_path}' (HEADER, DELIMITER ',');
    """)
    count = con.execute(f"SELECT COUNT(*) FROM '{output_path}'").fetchone()[0]
    elapsed = time.time() - t0
    size_mb = output_path.stat().st_size / (1024 * 1024)
    log.info("  ✓ %s rows, %.0f MB, %.1fs", f"{count:,}", size_mb, elapsed)
    return count


def main():
    parser = argparse.ArgumentParser(description="Create data samples at specified percentages")
    parser.add_argument("--pct", nargs="+", type=float, default=[1.0],
                        help="Sample percentages to create (default: 1)")
    args = parser.parse_args()

    if not FULL_CSV.exists():
        log.error("Full dataset not found: %s", FULL_CSV)
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()

    for pct in args.pct:
        if pct == 1.0:
            output = DATA_DIR / "sample.csv"
        else:
            label = f"{pct:.1f}".replace(".", "_") if pct != int(pct) else str(int(pct))
            output = DATA_DIR / f"sample_{label}pct.csv"
        create_sample(con, FULL_CSV, pct, output)

    con.close()
    log.info("Done.")


if __name__ == "__main__":
    main()

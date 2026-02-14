"""
Medicaid Analysis — Configuration & Constants
"""

import logging
import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR.parent / "data"
FULL_CSV   = DATA_DIR / "medicaid-provider-spending.csv"
SAMPLE_CSV = DATA_DIR / "sample.csv"
OUTPUT_DIR = Path(os.environ["MEDICAID_OUTPUT_DIR"]) if "MEDICAID_OUTPUT_DIR" in os.environ else BASE_DIR / "output"
PLOTS_DIR  = Path(os.environ["MEDICAID_PLOTS_DIR"]) if "MEDICAID_PLOTS_DIR" in os.environ else BASE_DIR / "plots"

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("medicaid")

# ── Known full-dataset statistics (for reference / scaling) ────────────────
FULL_ROW_COUNT      = 227_083_361
FULL_TOTAL_PAID     = 1_093_562_833_510.64
FULL_TOTAL_CLAIMS   = 18_825_564_012
FULL_BILLING_NPIS   = 617_503
FULL_SERVICING_NPIS = 1_627_362
FULL_HCPCS_CODES    = 10_881

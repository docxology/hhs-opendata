"""Stage the pinned aggregate tables and figure for manuscript reproduction."""

import csv
import hashlib
import io
import json
from decimal import Decimal
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = "317c24bbdd823a89a85853982919b3735bcaaefd"
SOURCES = {
    "yearly": (
        "medicaid_analysis/output/100pct/02_yearly_summary.csv",
        "0d05eaa68de6e64cb46f6edd9e2e6190310b67aae3da997e18b6cbdea64d2414",
    ),
    "eda": (
        "medicaid_analysis/output/100pct/01_eda_summary.json",
        "dd101adcc3bded74ce61140479639f2b5175aba1963e3011c9fa6fd448aca7e9",
    ),
    "plot": (
        "medicaid_analysis/plots/100pct/02_yearly_spending.png",
        "a9440376ed59d14101f3c7e4229540d1b4bb2716fc04eaa4a7ddfd71fce42fb0",
    ),
}


def read_artifact(path: str, expected_digest: str) -> bytes:
    """Read a public Git blob and verify its recorded digest."""
    payload = subprocess.check_output(["git", "show", f"{SNAPSHOT}:{path}"], cwd=ROOT)
    if hashlib.sha256(payload).hexdigest() != expected_digest:
        raise ValueError(f"Archive checksum mismatch for {path}")
    return payload


def main() -> None:
    blobs = {name: read_artifact(*source) for name, source in SOURCES.items()}
    yearly = list(csv.DictReader(io.StringIO(blobs["yearly"].decode("utf-8"))))
    eda = json.loads(blobs["eda"], parse_float=Decimal)

    paid_sum = sum(Decimal(row["total_paid"]) for row in yearly)
    if abs(paid_sum - eda["total_paid"]) > Decimal("2"):
        raise ValueError("Archived annual and overall paid totals differ by more than two dollars.")
    if sum(Decimal(row["total_claims"]) for row in yearly) != eda["total_claims"]:
        raise ValueError("Archived annual claim totals do not match the overall total.")

    billions = Decimal("1000000000")
    trillions = Decimal("1000000000000")
    evidence = {
        "source_revision": SNAPSHOT,
        "inputs": {name: {"path": path, "sha256": digest} for name, (path, digest) in SOURCES.items()},
        "rows": eda["row_count"],
        "date_min": eda["date_min"],
        "date_max": eda["date_max"],
        "total_claims": int(eda["total_claims"]),
        "total_paid_trillions": float((eda["total_paid"] / trillions).quantize(Decimal("0.001"))),
        "annual_paid_billions": [
            {
                "year": int(row["year"]),
                "paid_billions": float((Decimal(row["total_paid"]) / billions).quantize(Decimal("0.001"))),
            }
            for row in yearly
        ],
    }
    figure = {
        "figures": [{
            "label": "fig:archived-yearly-spending",
            "filename": "archived-yearly-spending.png",
            "caption": "Archived annual Medicaid payments by calendar year.",
            "alt_text": "Annual Medicaid payments rise across the series through 2023 and are lower in 2024.",
            "source": SOURCES["plot"][0],
        }],
    }

    figures = ROOT / "output" / "figures"
    data = ROOT / "output" / "data"
    figures.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    (figures / "archived-yearly-spending.png").write_bytes(blobs["plot"])
    (figures / "figure_registry.json").write_text(json.dumps(figure, indent=2) + "\n", encoding="utf-8")
    (data / "archive-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Verified and staged three pinned aggregate artifacts.")


if __name__ == "__main__":
    main()

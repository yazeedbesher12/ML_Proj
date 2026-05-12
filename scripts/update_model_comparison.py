from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SPECS = [
    ("DTC", "Without DR", "dtc_without_dr_metrics.csv"),
    ("DTC", "With DR", "dtc_with_dr_metrics.csv"),
    ("SVM", "Without DR", "svm_without_dr_metrics.csv"),
    ("SVM", "With DR", "svm_with_dr_metrics.csv"),
]

OUT_FIELDS = ["Model", "Dimensionality Reduction", "Accuracy", "Precision", "Recall", "F1-score"]
rows = []

for model, dr, filename in SPECS:
    path = RESULTS_DIR / filename
    if not path.exists():
        continue

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        first = next(reader, None)

    if not first:
        continue

    rows.append(
        {
            "Model": model,
            "Dimensionality Reduction": dr,
            "Accuracy": first.get("Accuracy", ""),
            "Precision": first.get("Precision", ""),
            "Recall": first.get("Recall", ""),
            "F1-score": first.get("F1-score", ""),
        }
    )

out_path = RESULTS_DIR / "model_comparison_results.csv"
with out_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=OUT_FIELDS, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {out_path}")
print(f"Rows written: {len(rows)}")

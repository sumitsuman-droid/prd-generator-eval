import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generator import evaluate_prd
from tabulate import tabulate

SAMPLE_DIR = Path(__file__).parent / "sample_prds"
RESULTS_FILE = Path(__file__).parent / "calibration_results.json"
DIMS = ["specificity", "measurability", "testability", "user_centricity", "completeness"]


def load_prds():
    files = sorted(SAMPLE_DIR.glob("*.json"))
    return [(f.name, json.loads(f.read_text(encoding="utf-8"))) for f in files]


def run():
    prds = load_prds()
    total = len(prds)
    rows = []
    raw_results = []

    for i, (filename, prd) in enumerate(prds, 1):
        expected = "strong" if filename.startswith("strong") else "weak"
        try:
            result = evaluate_prd(prd)
            overall = result["overall_score"]
            dim_scores = {d: result["scores"][d]["score"] for d in DIMS}
            print(f"[{i:2d}/{total}] {filename:<22} → {overall}")
            rows.append({
                "filename": filename,
                "expected": expected,
                "overall": overall,
                **dim_scores,
            })
            raw_results.append({"filename": filename, "expected": expected, "eval": result})
        except Exception as exc:
            print(f"[{i:2d}/{total}] {filename:<22} → ERROR: {exc}")
            rows.append({
                "filename": filename, "expected": expected,
                "overall": None, **{d: None for d in DIMS},
            })
            raw_results.append({"filename": filename, "expected": expected, "error": str(exc)})

    # ── table ────────────────────────────────────────────────────────────────
    print("\n")
    table_rows = [
        [r["filename"], r["expected"], r["overall"],
         r["specificity"], r["measurability"], r["testability"],
         r["user_centricity"], r["completeness"]]
        for r in rows
    ]
    headers = ["filename", "expected", "overall",
               "specific.", "measur.", "testab.", "user_c.", "complet."]
    print(tabulate(table_rows, headers=headers, floatfmt=".1f", tablefmt="simple"))

    # ── separation stats ─────────────────────────────────────────────────────
    def mean(vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals), 2) if vals else None

    strong = [r for r in rows if r["expected"] == "strong"]
    weak   = [r for r in rows if r["expected"] == "weak"]

    mean_strong = mean([r["overall"] for r in strong])
    mean_weak   = mean([r["overall"] for r in weak])
    separation  = round(mean_strong - mean_weak, 2) if (mean_strong and mean_weak) else None

    print(f"\nMean overall  — strong ({len(strong)}): {mean_strong}  |  weak ({len(weak)}): {mean_weak}")
    print(f"Separation (strong − weak): {separation}")

    dim_seps = {}
    for d in DIMS:
        ms = mean([r[d] for r in strong])
        mw = mean([r[d] for r in weak])
        sep = round(ms - mw, 2) if (ms and mw) else None
        dim_seps[d] = sep
        print(f"  {d:<18} strong={ms}  weak={mw}  Δ={sep}")

    best_dim  = max(dim_seps, key=lambda d: dim_seps[d] or 0)
    worst_dim = min(dim_seps, key=lambda d: dim_seps[d] or 99)
    print(f"\nBest-separating dimension : {best_dim} (Δ={dim_seps[best_dim]})")
    print(f"Worst-separating dimension: {worst_dim} (Δ={dim_seps[worst_dim]})")

    if separation is not None and separation >= 2.0:
        print(f"\nVERDICT: PASS  (separation={separation})")
    else:
        print(f"\nVERDICT: FAIL  (separation={separation} < 2.0) — "
              f"weakest dimension: {worst_dim} (Δ={dim_seps[worst_dim]})")

    # ── persist results ───────────────────────────────────────────────────────
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mean_strong": mean_strong, "mean_weak": mean_weak,
        "separation": separation, "dim_separations": dim_seps,
        "verdict": "PASS" if (separation or 0) >= 2.0 else "FAIL",
        "results": raw_results,
    }
    RESULTS_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nFull results saved → {RESULTS_FILE}")


if __name__ == "__main__":
    run()

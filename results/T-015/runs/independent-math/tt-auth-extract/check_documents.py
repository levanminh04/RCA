"""Check numeric and provenance anchors in the worked example against artifacts."""
import ast
import json
from pathlib import Path

root = Path("results/T-015")
base = root / "runs/independent-math/tt-auth-extract"
data = json.loads((base / "output-exact-prior/example-extract.json").read_text(encoding="utf-8"))
control = json.loads((root / "runs/tt-local/auth/two-normal-summary.json").read_text(encoding="utf-8"))
example = (root / "vi-du-tinh-tay.md").read_text(encoding="utf-8")
profile = (root / "ho-so-microrank.md").read_text(encoding="utf-8")
checks = {}
vnint = lambda value: f"{value:,}".replace(",", ".")
for name, label in (("normal", "Bình thường"), ("anomaly", "Bất thường")):
    g = data["groups"][name]
    row = f"| {label} | {g['operation_count']} | {g['edge_count']} | {vnint(g['trace_count'])} | {vnint(g['span_occurrence_count'])} | {g['kind_count']} |"
    checks[name + "_graph_row"] = row in example
checks["station_score"] = f"{float(data['top11'][0]['score']):.14f}".replace(".", ",") in example
root_eval = data["after_prediction_root_inspection"]
checks["auth_score"] = f"{float(root_eval['root_operations'][0]['score']):.14f}".replace(".", ",") in example
checks["auth_rank"] = f"hạng {root_eval['full_service_rank']}" in example
checks["4383_all_points"] = vnint(data["arithmetic"]["n_comparisons"]) in example and data["arithmetic"]["all_passed"]
checks["19_input_checks"] = len(data["independent_inputs_check"]["checks"]) == 19 and all(data["independent_inputs_check"]["checks"].values())
checks["normal_control_flag_count"] = vnint(control["counts"]["abnormal_spans"]) in example
checks["normal_control_current_spans"] = vnint(control["counts"]["spans_after"]) in example
checks["normal_control_false_alarm_explicit"] = "false alarm" in example and "false alarm" in profile
checks["25_not_claimed_converged"] = "Không có bằng chứng hội tụ" in example and "Không được gọi là đã hội tụ" in profile
checks["null_semantic_gap_disclosed"] = "<NA>" in example and "<NA>" in profile
checks["old_snapshot_placeholder_removed"] = "chờ snapshot chạy hợp lệ" not in profile
for file in (
    root / "scripts/independent_math.py",
    base / "extract_example.py",
    root / "runs/independent-math/trace-vector-probe/capture_trace_vector.py",
):
    ast.parse(file.read_text(encoding="utf-8"))
    checks[file.name + "_syntax"] = True
summary = {"checks": checks, "all_passed": all(checks.values()),
           "scope": "Numeric rows, scores, checks and limits compared to saved artifacts; not a new method run"}
(base / "document-check.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=True))
raise SystemExit(0 if summary["all_passed"] else 1)

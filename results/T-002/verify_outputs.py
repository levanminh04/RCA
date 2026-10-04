"""Cheap checks of saved T-002 results, without opening any raw telemetry."""
from __future__ import annotations
import ast
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
LOCAL = HERE / "local-inspection" / "run-002"
PUBLIC = HERE / "public-metadata" / "run-002"


def main():
    base = HERE / "verification"
    base.mkdir(exist_ok=True)
    run = base / f"run-{len(list(base.glob('run-*'))) + 1:03d}"
    run.mkdir()
    report = {"started_utc": datetime.now(timezone.utc).isoformat(), "checks": [], "status": "running"}
    def check(name, condition, detail):
        report["checks"].append({"name": name, "pass": bool(condition), "detail": detail})
        assert condition, name
    try:
        cases = json.loads((LOCAL / "cases.json").read_text(encoding="utf-8"))
        manifest = json.loads((LOCAL / "manifest.json").read_text(encoding="utf-8"))
        summary = json.loads((LOCAL / "summary.json").read_text(encoding="utf-8"))
        check("full_run_complete", manifest["status"] == "complete" and len(cases) == 35, "35 cases; completed manifest")
        check("allowed_inputs_only", all(i["path"].startswith("data/rcaeval/") and "locked" not in i["path"] for i in manifest["inputs"]), "saved input paths only; no locked path opened")
        check("input_file_count", len(manifest["inputs"]) == 100, "100 parquet files from allowed 35 cases")
        hashes_match = hashlib.sha256((HERE / "inspect_local.py").read_bytes()).hexdigest() == manifest["script_sha256"]
        check("inspection_script_provenance", hashes_match, "current script matches full-run hash")
        trace_cases = [c for c in cases if "trace" in c]
        check("parent_accounting", all(t["n_spans"] == t["root_or_empty_parent_count"] + t["parent_reference_count"] and t["parent_reference_count"] == t["parent_resolved_count"] + t["parent_unresolved_count"] for t in [c["trace"] for c in trace_cases]), "sum roots/references/resolved/unresolved per case")
        check("unique_trace_span_keys", all(c["trace"]["duplicate_key_rows"] == c["trace"]["conflicting_service_keys"] == 0 for c in trace_cases), "no duplicate or ambiguous key in inspected traces")
        check("timestamp_field_relation", all(c["trace"]["start_field_relation"]["startTime_div_1000_minus_startTimeMillis_min"] == c["trace"]["start_field_relation"]["max"] == 0 for c in trace_cases), "startTime//1000 matches startTimeMillis")
        check("normal_full_graph_equality", all(c["trace"]["graphs"]["pre_injection"]["nodes"] == c["trace"]["graphs"]["full"]["nodes"] and c["trace"]["graphs"]["pre_injection"]["edges"] == c["trace"]["graphs"]["full"]["edges"] for c in trace_cases), "exact node and edge sets per case, not just counts")
        targets = [c for c in cases if c["dataset"] in ("re2tt", "re2ob", "re3tt", "re3ob")]
        check("injection_within_target_windows", all(c["metric_time_min"] < c["inject_time"] <= c["metric_time_max"] for c in targets), "32 target cases; auxiliary RE1 intentionally excluded")
        check("normal_point_accounting", all(c["normal_rows"] + c["post_rows"] == c["n_metric_rows"] and c["metric_duplicate_times"] == 0 and c["metric_step_seconds"] == [1.0] for c in targets), "normal/post rows and regular 1s samples")
        for ds, s in summary.items():
            ts = [c["trace"] for c in cases if c["dataset"] == ds and "trace" in c]
            check(f"aggregate_{ds}", s["n_spans"] == sum(t["n_spans"] for t in ts) and s["parent_reference_count"] == sum(t["parent_reference_count"] for t in ts), "aggregate derived from per-case saved counts")
        public = json.loads((PUBLIC / "count-summary.json").read_text(encoding="utf-8"))
        check("public_counts", [(p["n_cases"], p["n_root_services"], p["n_faults"]) for p in public] == [(90,5,6),(90,5,6),(30,2,4),(30,4,5)], "public counts 90/5/6,90/5/6,30/2/4,30/4/5")
        bands = pd.read_csv(LOCAL / "symptom-channel-bands.csv")
        rates = pd.read_csv(LOCAL / "symptom-entity-rates.csv")
        check("finite_bands", np.isfinite(bands.absolute_deviation_band).all() and (bands.absolute_deviation_band >= 0).all(), "no negative/NaN/infinite bands; no epsilon or divide-by-scale")
        check("rate_denominators", np.allclose(rates.control_exceed_rate, rates.control_exceed_rows / rates.control_valid_rows, equal_nan=True) and np.allclose(rates.post_exceed_rate, rates.post_exceed_rows / rates.post_valid_rows, equal_nan=True), "rates recomputed from saved counts/denominators; zero valid rows give undefined rate")
        probe_cases = pd.read_csv(LOCAL / "probe-case-summary.csv")
        check("probe_shapes", len(probe_cases) == 192 and set(probe_cases.q) == {0.95,0.99,0.995} and len(probe_cases.case.unique()) == 32, "32 cases x3 quantiles x2 groups; no binary propagation labels")
        other = rates.loc[~rates.is_root & rates.business_name_heuristic]
        recomputed = other.groupby(["case", "q", "signal_group"])[["control_exceed_rate", "post_exceed_rate"]].mean()
        for row in probe_cases.itertuples():
            expected = recomputed.loc[(row.case, row.q, row.signal_group)]
            assert np.isclose(expected.control_exceed_rate, row.control_mean_service_rate)
            assert np.isclose(expected.post_exceed_rate, row.post_mean_service_rate)
        check("probe_aggregates", True, "all per-case probe values recomputed from service rows")
        tree = ast.parse((HERE / "inspect_local.py").read_text(encoding="utf-8"))
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "metric_excursions")
        check("signal_function_interface", [a.arg for a in fn.args.args] == ["frame", "boundary"], "no root/fault/path/graph parameter; injection boundary explicitly known-window")
        for filename in ("mau-the-dataset.md", "the-rcaeval.md", "public-sources.md"):
            content = (HERE / filename).read_text(encoding="utf-8")
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", content)
            check(f"links_{filename}", all((HERE / link.split("#",1)[0]).exists() for link in links if not re.match(r"[a-z]+://",link) and link.split("#",1)[0]), "local artifact links exist")
        card = (HERE / "the-rcaeval.md").read_text(encoding="utf-8")
        check("four_complete_cards", len(re.findall(r"^## RE[23]-(?:TT|OB)$", card, re.M)) == 4 and all(len(re.findall(rf"^### {i}\. ", card, re.M)) == 4 for i in range(1,11)), "each of four cards includes all 10 template sections")
        artifacts = []
        for path in sorted(HERE.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.is_relative_to(base) or (path.name.startswith("verification") and path.suffix == ".log"):
                continue
            raw = path.read_bytes()
            artifacts.append({"path": str(path.relative_to(REPO)).replace("\\", "/"), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        report["artifacts"] = artifacts
        report["spec_sha256"] = hashlib.sha256((REPO / "tasks/T-002-the-dataset-rcaeval/SPEC.md").read_bytes()).hexdigest()
        report["status"] = "passed"
    except Exception:
        report["status"] = "failed"
        report["error"] = traceback.format_exc()
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (run / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"PASS {len(report['checks'])} saved-output checks; {len(report['artifacts'])} result artifacts: {run}")


if __name__ == "__main__":
    main()

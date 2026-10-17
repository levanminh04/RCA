"""Kiểm literal của hợp đồng messaging; mỗi lần chạy ghi thư mục mới, giữ cả lỗi."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def ordered(rows):
    return sorted(rows, key=canonical)


def projection_key(edge):
    # Định dạng giao diện được ghi trong design; không gọi helper khóa của bộ dựng.
    key = [edge[k] for k in ["source", "target", "type", "evidence_source", "destination"]]
    if "messaging" in edge:
        key.append(canonical(edge["messaging"]))
    return key


def project_counts(operation):
    """Oracle riêng cho phép chiếu count/witness, không gọi project của bộ dựng."""
    owners = dict(operation["belongs_to"])
    out = {}
    for row in operation["edges"]:
        source = owners.get(row["source"], row["source"])
        target = owners.get(row["target"], row["target"])
        if source == target or row["type"] == "span-parent":
            continue
        item = dict(row, source=source, target=target)
        descriptor = {k: v for k, v in item.items() if k not in ("event_count", "witness")}
        key = canonical(descriptor)
        if key not in out:
            out[key] = dict(descriptor, event_count=0, witness=[])
        out[key]["event_count"] += item["event_count"]
        out[key]["witness"] = sorted(
            {tuple(w) for w in out[key]["witness"]} | {tuple(w) for w in item["witness"]}
        )[:2]
    return ordered(list(out.values()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="Tên thư mục mới bên trong sua-n1-001")
    parser.add_argument("--builder-path", type=Path, help="Bản builder lịch sử để kiểm phản chứng")
    args = parser.parse_args()
    out = (BASE / args.output).resolve()
    if out.parent != BASE or out == BASE:
        raise ValueError("output_must_be_one_new_directory_under_fixture_base")
    out.mkdir(exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    result = {"started_utc": started, "fixtures": [], "fatal_error": None}
    try:
        import pandas as pd

        path = (args.builder_path or ROOT / "src/do_thi/builder.py").resolve()
        spec = importlib.util.spec_from_file_location("t035_messaging_builder_under_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        build, project = module.build, module.project
        inputs = json.loads((BASE / "fixture_inputs.json").read_text("utf-8"))
        expected = json.loads((BASE / "fixture_expected.json").read_text("utf-8"))
        result["sources"] = [
            {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in [path, BASE / "fixture_inputs.json", BASE / "fixture_expected.json", Path(__file__)]
        ]
        result["python"] = sys.version
        result["pandas"] = pd.__version__
        for case in inputs:
            record = {"name": case["name"], "checks": [], "exception": None}
            result["fixtures"].append(record)
            want = expected[case["name"]]

            def compare(name, actual, target):
                ok = canonical(actual) == canonical(target)
                row = {"check": name, "pass": ok}
                if not ok:
                    row.update(actual=actual, expected=target)
                record["checks"].append(row)

            try:
                entity, operation = build(
                    pd.DataFrame(case["spans"]), case["interval_ns"], {}, case["universe"]
                )
                record.update(entity=entity, operation=operation)
                compare("entity_nodes", sorted(n["id"] for n in entity["nodes"]), want["entity_nodes"])
                compare("operation_nodes", sorted(n["id"] for n in operation["nodes"]), want["operation_nodes"])
                compare("entity_edges_exact", ordered(entity["edges"]), ordered(want["entity_edges"]))
                compare("operation_edges_exact", ordered(operation["edges"]), ordered(want["operation_edges"]))
                for level, graph in [("entity", entity), ("operation", operation)]:
                    compare(level + "_unresolved", graph["stats"]["unresolved_messages"], want["unresolved_messages"])
                    compare(level + "_diagnostics", graph.get("messaging_diagnostics"), want["messaging_diagnostics"])
                    addresses = sorted({tuple(e["queue_metric_address"]) for e in graph["edges"] if e.get("queue_metric_address") is not None})
                    compare(level + "_metric_addresses", addresses, want["queue_metric_addresses"])
                nodes, edges = project(operation)
                compare("project_api_nodes", sorted(nodes), want["entity_nodes"])
                compare("project_api_keys", ordered([list(k) for k in edges]), ordered([projection_key(e) for e in want["entity_edges"]]))
                compare("independent_projection_counts_witness", project_counts(operation), ordered(want["entity_edges"]))
            except Exception as exc:
                record["exception"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
            record["pass"] = record["exception"] is None and bool(record["checks"]) and all(c["pass"] for c in record["checks"])
    except Exception as exc:
        result["fatal_error"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    result["passed"] = sum(c["pass"] for c in result["fixtures"])
    result["failed"] = len(result["fixtures"]) - result["passed"]
    result["pass"] = result["fatal_error"] is None and bool(result["fixtures"]) and result["failed"] == 0
    with (out / "result.json").open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
    print(json.dumps({k: result[k] for k in ["passed", "failed", "pass", "fatal_error"]}, ensure_ascii=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

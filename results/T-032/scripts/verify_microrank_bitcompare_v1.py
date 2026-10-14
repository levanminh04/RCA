"""T-032: lượt so bit độc lập cho 52 ca MicroRank laptop (không dùng code của wrapper hay driver).

Chỉ đọc. Với mỗi ca trong plan-52: bản đóng băng (kiểm hash theo plan) so với bản ghi native và observed,
mọi trường trừ run_id và cost; float so theo biểu diễn hex. Ghi một file kết quả mới.
Dùng: py -3 -B verify_microrank_bitcompare_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
COHORT = REPO / "results/T-032/runs/microrank-laptop-cohort-001"
DIAGNOSTIC = REPO / "results/T-032/runs/microrank-laptop-diagnostic-001"
EXCLUDED = ("run_id", "cost")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def differences(a, b, path=""):
    if type(a) is not type(b):
        return [path + ": kiểu khác"]
    if isinstance(a, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            if path == "" and key in EXCLUDED:
                continue
            if key not in a or key not in b:
                out.append(path + "/" + key + ": thiếu một bên")
            else:
                out += differences(a[key], b[key], path + "/" + key)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path + ": độ dài khác"]
        out = []
        for index, (x, y) in enumerate(zip(a, b)):
            out += differences(x, y, path + "/" + str(index))
        return out
    if isinstance(a, float):
        return [] if a.hex() == b.hex() else [path + ": float khác"]
    return [] if a == b else [path + ": giá trị khác"]


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    rows = []
    for row in read(COHORT / "plan-52.json")["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        item = {"dataset": dataset, "opaque_id": opaque_id, "source_status": row["source_status"]}
        if (dataset, opaque_id) == ("RE2-TT", "dev-3defe3d34b"):
            frozen_path = read(COHORT / "retrospective-dev-3defe3d34b/audit/check.json")["source"]["path"]
            run = DIAGNOSTIC
        else:
            run = COHORT / "cases" / dataset / opaque_id
            binding = run / "source-binding.json"
            frozen_path = read(binding)["entry"]["path"] if binding.is_file() else None
        native, observed = run / "native/ban-ghi-0.json", run / "observed/ban-ghi-0.json"
        if frozen_path is None or not native.is_file() or not observed.is_file():
            rows.append({**item, "result": "not_run"})
            continue
        frozen_file = REPO / frozen_path
        frozen, n, o = read(frozen_file), read(native), read(observed)
        d_fn, d_no, d_fo = differences(frozen, n), differences(n, o), differences(frozen, o)
        item.update(frozen_path=frozen_path, frozen_hash_ok=sha(frozen_file) == row["source_sha256"],
                    frozen_status=frozen["status"], native_status=n["status"], observed_status=o["status"],
                    frozen_vs_native=len(d_fn), native_vs_observed=len(d_no), frozen_vs_observed=len(d_fo),
                    first_differences=(d_fn + d_no + d_fo)[:5],
                    score_pairs=len(frozen.get("ranking") or []), entities=len(frozen.get("entity_ranking") or []))
        item["result"] = "exact" if item["frozen_hash_ok"] and not (d_fn or d_no or d_fo) else "DIFFERENT"
        rows.append(item)
    summary = {"n": len(rows), "exact": sum(r["result"] == "exact" for r in rows),
               "different": [r["dataset"] + "/" + r["opaque_id"] for r in rows if r["result"] == "DIFFERENT"],
               "not_run": [r["dataset"] + "/" + r["opaque_id"] for r in rows if r["result"] == "not_run"],
               "exact_by_source_status": {s: sum(r["result"] == "exact" and r["source_status"] == s for r in rows) for s in ("OK", "ERROR")},
               "status_reproduced": sum(r.get("frozen_status") == r.get("native_status") == r.get("observed_status") for r in rows if r["result"] != "not_run")}
    (out / "result.json").write_text(json.dumps({"schema": "T032-microrank-independent-bit-compare-v1", "excluded_fields": list(EXCLUDED),
                                                 "plan_sha256": sha(COHORT / "plan-52.json"), "summary": summary, "rows": rows,
                                                 "methods_executed": False}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()

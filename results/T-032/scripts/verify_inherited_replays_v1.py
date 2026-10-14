"""T-032: người làm mới tự so từng bit các bản ghi phát lại BARO và SimpleRCA do phiên 1-8 tạo.

Chỉ đọc. Không gọi phương pháp. Với mỗi bản ghi phát lại trên EC2, tìm bản đóng băng theo chỉ mục
T-024/T-026 (đã kiểm hash theo chỉ mục), so mọi trường trừ run_id và cost. Ghi một file kết quả mới.
Dùng: python verify_inherited_replays_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
EXCLUDED = ("run_id", "cost")
SOURCES = {
    "baro": ["runs/baro-re2-first-001", "runs/baro-re2-batch-001/cases", "runs/baro-nezha-first-001", "runs/baro-nezha-batch-001"],
    "simplerca": ["runs/simplerca-re2-first-001", "runs/simplerca-nezha-first-001", "runs/simplerca-batch-001"],
}


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


def frozen_index():
    """(dataset, method, opaque_id) -> (đường dẫn, sha256) cho cấu hình chính của BARO và SimpleRCA."""
    index = {}
    for record in read(REPO / "results/T-024/ban-ghi-dua-vao-cham.json")["records"]:
        if (record["method"], record.get("variant")) in (("baro", "native"), ("simplerca", "native")):
            index[("RE2-TT", record["method"], record["opaque_id"])] = (record["path"], record["sha256"])
    unique = read(REPO / "results/T-026/ban-ghi-dua-vao-cham.json")["unique_records"]
    for record in (unique.values() if isinstance(unique, dict) else unique):
        if record.get("method") in ("baro", "simplerca") and record.get("source_view") == "main":
            index[("Nezha-OB", record["method"], record["opaque_id"])] = (record["path"], record["sha256"])
    return index


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    index = frozen_index()
    rows, seen = [], set()
    for method, roots in SOURCES.items():
        for root in roots:
            for replay_path in sorted((BASE / root).rglob("ban-ghi-0.json")):
                replay = read(replay_path)
                matches = []
                for dataset in ("RE2-TT", "Nezha-OB"):
                    key = (dataset, method, replay["opaque_id"])
                    if key not in index:
                        continue
                    frozen_path, expected = index[key]
                    frozen_file = REPO / frozen_path
                    hash_ok = sha(frozen_file) == expected
                    diff = differences(read(frozen_file), replay)
                    matches.append({"dataset": dataset, "frozen_path": frozen_path, "frozen_hash_ok": hash_ok,
                                    "difference_count": len(diff), "first_differences": diff[:5]})
                exact = [m for m in matches if m["frozen_hash_ok"] and m["difference_count"] == 0]
                row = {"method": method, "opaque_id": replay["opaque_id"], "replay_path": str(replay_path.relative_to(BASE)),
                       "replay_sha256": sha(replay_path), "status": replay.get("status"), "candidates": matches,
                       "exact_dataset": exact[0]["dataset"] if len(exact) == 1 else None}
                rows.append(row)
                if row["exact_dataset"]:
                    seen.add((row["exact_dataset"], method, replay["opaque_id"]))
    missing = sorted(key for key in index if key not in seen)
    summary = {method: {"frozen_main_records": sum(k[1] == method for k in index),
                        "replay_records_found": sum(r["method"] == method for r in rows),
                        "exact": sum(r["method"] == method and r["exact_dataset"] is not None for r in rows),
                        "not_exact": [r["replay_path"] for r in rows if r["method"] == method and r["exact_dataset"] is None]}
               for method in SOURCES}
    result = {"schema": "T032-inherited-replay-bit-compare-v1", "excluded_fields": list(EXCLUDED),
              "summary": summary, "frozen_without_exact_replay": [list(k) for k in missing], "rows": rows,
              "methods_executed": False}
    (out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "frozen_without_exact_replay": len(missing)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

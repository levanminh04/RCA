"""T-032 phép B-1 (thiet-ke-phep-doi-001.md mục 6): BARO không lọc cột hằng.

Chạy trên EC2. Mỗi ca chạy hai nhánh, mỗi nhánh một tiến trình riêng:
  sham: đúng đường native của lượt phát lại; bản ghi phải khớp bản đóng băng từng bit, nếu không thì B-1 của ca đó vô hiệu;
  b1:   chỉ thay `RCAEval.io.time_series.drop_constant` bằng hàm đồng nhất trong tiến trình đó; mọi thứ khác là code native
        (worker, adapter, preprocess, phép giao, RobustScaler, max). Không sửa file mã nguồn nào.
Dựng job và bản ghi bằng đúng các hàm của replay_baro.py đã dùng cho 52 lượt phát lại khớp.
Mọi thực thể được tính trước; nhãn root nối sau ở lệnh `collect`.

Dùng:
  python contrast_baro_b1_v1.py one <sham|b1> <RE2-TT|Nezha-OB> <opaque_id> <thư mục mới>
  python contrast_baro_b1_v1.py all <thư mục lượt mới>
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
PYTHON = Path("/home/ubuntu/rca/T-025/envs/main/bin/python")
LABELS = BASE / "repo/results/T-028/runs/phan-hoi-review-001/ca-sai.json"
MAX_CHILD_S = 600


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=1, allow_nan=False)
        stream.write("\n")


def one(branch, dataset, opaque_id, directory):
    import replay_baro as rb
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    audit = []
    entry, frozen, index26, _code_hashes = rb.source_for(dataset, opaque_id, audit)
    from p3 import ban_ghi, runner, selector, worker
    if dataset == "RE2-TT":
        allow = selector.nap_allowlist(rb.safe_source("results/T-022/allowlist-dev.json"))
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
        if wanted != frozen["input_sha256"]:
            raise rb.ReplayError("selected allowlist hashes differ from frozen inputs")
        files = selector.chon_ca(allow, opaque_id, rb.RE2_RAW_REPO, kiem_hash=True)
        job = {"kind": "ranker", "method": "baro", "t": frozen["window"]["t"], "model": None,
               "files": {name: {"path": path, "sha256": wanted[name]} for name, path in files.items()}}
        invoke = worker.main
    else:
        from p3 import nezha, nezha_worker
        from p3.adapters.nezha import VARIANTS, VERSIONS
        allow_relative = "results/T-026/allowlist-dev.json"
        allow_path = rb.verify(allow_relative, index26["source_hashes"][allow_relative], rb.I26 + "#/source_hashes", audit)
        allow = nezha.nap_allowlist(allow_path)
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items()}
        if wanted != frozen["input_sha256"] or entry["trace_guard_s"] != 0:
            raise rb.ReplayError("Nezha input hashes/main guard differ from source")
        script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
        constants = rb.literal_constants(rb.verify(script, index26["source_hashes"][script], rb.I26 + "#/source_hashes", audit))
        job = {"allowlist_path": str(allow_path), "opaque_id": opaque_id, "repo_root": str(rb.REPO),
               "view": "main", "method": "baro", "trace_guard_s": 0}
        invoke = nezha_worker.main
    rb.dump(directory / "job.json", job)
    patched = False
    if branch == "b1":
        import importlib
        time_series = importlib.import_module("RCAEval.io.time_series")
        baro_module = importlib.import_module("RCAEval.e2e.baro")  # RCAEval.e2e.__init__ che tên module bằng hàm
        if baro_module.preprocess is not time_series.preprocess:
            raise rb.ReplayError("baro() không dùng preprocess của io.time_series; phép đổi không áp được")
        time_series.drop_constant = lambda df: df  # bước duy nhất bị đổi
        patched = True
    started = time.perf_counter()
    with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout, \
            (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            invoke(str(directory / "job.json"), str(directory / "ket-qua.json"))
    cost = rb.measured_cost(started, 0)
    output = rb.read(directory / "ket-qua.json")
    if output.get("hashseed") != "0":
        raise rb.ReplayError("worker reported wrong hashseed")
    if dataset == "RE2-TT":
        base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None,
                "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "baro", "a")
        if len(records) != 1:
            raise rb.ReplayError("BARO reconstruction did not return one record")
    else:
        if len(output["ket_qua_nhieu"]) != 1:
            raise rb.ReplayError("BARO worker did not return one result")
        result = output["ket_qua_nhieu"][0]
        record = ban_ghi.tao("baro", VERSIONS["baro"], VARIANTS["baro"], "a", result, output["window"],
                             constants["CONFIG"], constants["WHY"], seed=None, hashseed=0,
                             run_id=directory.name, opaque_id=opaque_id)
        record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
        record["input_sha256"] = output["input_sha256"]
        if entry["reused_pilot"]:
            record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
        else:
            record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
        ban_ghi.kiem(record)
        rb.dump(directory / "ban-ghi-0.json", record)
    replay = rb.read(directory / "ban-ghi-0.json")
    differences = rb.compare_records(frozen, replay)
    rb.dump(directory / "check.json", {"branch": branch, "drop_constant_replaced_by_identity": patched,
            "dataset": dataset, "opaque_id": opaque_id, "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
            "frozen_status": frozen["status"], "branch_status": replay["status"],
            "difference_count_vs_frozen": len(differences), "exact_vs_frozen": not differences,
            "wall_s": cost.get("wall_s"), "note": "sham phải khớp tuyệt đối; b1 được phép khác"})
    return 0


def ranks(record):
    groups = {}
    for row in record["entity_ranking"]:
        groups.setdefault(row["tie_group"], []).append(row["entity"])
    out, offset = {}, 0
    for group in sorted(groups):
        for entity in groups[group]:
            out[entity] = (offset + 1, offset + len(groups[group]))
        offset += len(groups[group])
    return out


def margin(a, b):
    return None if abs(a) + abs(b) == 0 else (a - b) / (abs(a) + abs(b))


def collect(out):
    """Nối nhãn sau khi mọi nhánh đã chạy xong."""
    labels = {}
    for row in read(LABELS)["main_rows"]:
        if row["method"] == "baro":
            flags = {k: (((row.get("mechanisms") or {}).get(k) or {}).get("assignment") or {}).get("multi") for k in ("1", "5")}
            labels[(row["dataset"], row["opaque_id"])] = {"root": row["root"], "fault": row["fault"], "cell": row["cell"],
                "t028": {"status": row["status"], "rank_min": row["rank_min"], "rank_max": row["rank_max"], "multi_flags": flags}}
    cases = []
    for (dataset, opaque_id), label in sorted(labels.items()):
        base = {"dataset": dataset, "opaque_id": opaque_id, **label}
        directory = out / "cases" / dataset / opaque_id
        state = {branch: (read(directory / branch / "check.json") if (directory / branch / "check.json").is_file() else None)
                 for branch in ("sham", "b1")}
        if state["sham"] is None or not state["sham"]["exact_vs_frozen"]:
            cases.append({**base, "status": "INVALID", "reason": "sham không khớp bản đóng băng hoặc chưa chạy"})
            continue
        if state["b1"] is None:
            cases.append({**base, "status": "B1_FAILED", "reason": "nhánh b1 không cho bản ghi; xem failure.json"})
            continue
        native, changed = read(directory / "sham/ban-ghi-0.json"), read(directory / "b1/ban-ghi-0.json")
        item = {**base, "status": "OK", "sham_exact": True, "b1_status": changed["status"],
                "columns_scored": {"native": len(native["ranking"]), "b1": len(changed["ranking"])}}
        native_columns = {row["item"] for row in native["ranking"]}
        added = [row for row in changed["ranking"] if row["item"] not in native_columns]
        item["columns_added_by_b1"] = len(added)
        root = label["root"]
        item["root_columns_added_by_b1"] = [{"column": row["item"], "key": row["key"]} for row in added if row["entity"] == root]
        views = {}
        for name, record in (("native", native), ("b1", changed)):
            rank = ranks(record)
            score = {row["entity"]: row["key"][0] for row in record["entity_ranking"]}
            best = {}
            for row in record["ranking"]:
                best.setdefault(row["entity"], row["item"])
            if root not in rank:
                views[name] = {"root_ranked": False, "n_entities": len(rank)}
                continue
            above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
            views[name] = {"root_ranked": True, "n_entities": len(rank), "root_rank_min": rank[root][0], "root_rank_max": rank[root][1],
                           "root_score": score[root], "root_best_column": best[root],
                           "above_root": [{"entity": e, "score": score[e], "best_column": best[e],
                                           "best_column_added_by_b1": best[e] not in native_columns,
                                           "margin_vs_root": margin(score[e], score[root])} for e in above]}
        item["native"], item["b1"] = views["native"], views["b1"]
        if views["native"]["root_ranked"]:
            item["self_check_native_rank_equals_t028"] = (label["t028"]["status"] == "OK" and
                [views["native"]["root_rank_min"], views["native"]["root_rank_max"]] == [label["t028"]["rank_min"], label["t028"]["rank_max"]])
        if views["native"]["root_ranked"] and views["b1"]["root_ranked"]:
            before, after = views["native"]["root_rank_min"], views["b1"]["root_rank_min"]
            item["b1_effect_on_root"] = "tăng hạng" if after < before else "giảm hạng" if after > before else "không đổi"
            item["root_best_column_added_by_b1"] = views["b1"]["root_best_column"] not in native_columns
        cases.append(item)
    valid = [c for c in cases if c["status"] == "OK" and "b1_effect_on_root" in c]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        return {"n": len(rows),
                "b1_effect_on_root": {k: count(lambda c, k=k: c["b1_effect_on_root"] == k) for k in ("tăng hạng", "không đổi", "giảm hạng")},
                "hit1": {"native": count(lambda c: c["native"]["root_rank_max"] == 1), "b1": count(lambda c: c["b1"]["root_rank_max"] == 1)},
                "hit5": {"native": count(lambda c: c["native"]["root_rank_max"] <= 5), "b1": count(lambda c: c["b1"]["root_rank_max"] <= 5)},
                "cases_root_has_added_column": count(lambda c: c["root_columns_added_by_b1"]),
                "cases_root_best_column_is_added": count(lambda c: c["root_best_column_added_by_b1"]),
                "native_wrong_at_1": {"n": count(lambda c: c["native"]["root_rank_max"] > 1),
                                      "becomes_hit1": count(lambda c: c["native"]["root_rank_max"] > 1 and c["b1"]["root_rank_max"] == 1)},
                "native_hit_at_1": {"n": count(lambda c: c["native"]["root_rank_max"] == 1),
                                    "loses_hit1": count(lambda c: c["native"]["root_rank_max"] == 1 and c["b1"]["root_rank_max"] > 1)}}

    summary = {"n_cases": len(cases), "status_counts": {s: sum(c["status"] == s for c in cases) for s in ("OK", "INVALID", "B1_FAILED")},
               "self_check_native_rank_equals_t028": sum(bool(c.get("self_check_native_rank_equals_t028")) for c in cases),
               "all": tally(valid), "by_dataset": {d: tally([c for c in valid if c["dataset"] == d]) for d in ("RE2-TT", "Nezha-OB")},
               "note": "n là số ca có sham khớp từng bit và root được xếp ở cả hai nhánh. Hit tính bi quan theo hòa. "
                       "B-1 là phép đổi chẩn đoán trên dev, không phải phương pháp mới và không thay số P3."}
    write(out / "summary.json", {"schema": "T032-BARO-B1-v1", "design": "results/T-032/thiet-ke-phep-doi-001.md#6",
                                 "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def run_all(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    todo = sorted({(row["dataset"], row["opaque_id"]) for row in read(LABELS)["main_rows"] if row["method"] == "baro"})
    for dataset, opaque_id in todo:
        for branch in ("sham", "b1"):
            directory = out / "cases" / dataset / opaque_id / branch
            command = [str(PYTHON), "-B", "-X", "utf8", str(Path(__file__).resolve()), "one", branch, dataset, opaque_id, str(directory)]
            started = time.perf_counter()
            try:
                done = subprocess.run(command, cwd=BASE, env=os.environ.copy(), stdin=subprocess.DEVNULL,
                                      capture_output=True, text=True, timeout=MAX_CHILD_S)
                code, tail = done.returncode, (done.stderr or "")[-2000:]
            except subprocess.TimeoutExpired:
                code, tail = -1, "timeout 600 s"
            event = {"at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "dataset": dataset, "opaque_id": opaque_id,
                     "branch": branch, "exit_code": code, "wall_s": time.perf_counter() - started}
            if code != 0:  # giữ lượt hỏng; ca vẫn nằm trong mẫu số với trạng thái tương ứng
                event["stderr_tail"] = tail
                if directory.is_dir() and not (directory / "failure.json").exists():
                    write(directory / "failure.json", event)
            with (out / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            print(dataset, opaque_id, branch, code, round(event["wall_s"], 1), flush=True)
    collect(out)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "one":
        try:
            return one(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        except Exception:
            traceback.print_exc()
            return 1
    if len(sys.argv) == 3 and sys.argv[1] == "all":
        run_all(sys.argv[2])
        return 0
    if len(sys.argv) == 3 and sys.argv[1] == "collect":
        collect(Path(sys.argv[2]))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())

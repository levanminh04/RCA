"""T-032 phép B-2 (BARO, thang độ lệch chuẩn) và S-1 (SimpleRCA, đếm theo cột): thiet-ke-phep-doi-002.md.

Chạy trên EC2. Mỗi nhánh của mỗi ca một tiến trình riêng. Không sửa file mã nguồn nào; chỉ thay đối tượng trong tiến trình:
  baro b2      : `RobustScaler` -> `StandardScaler` của scikit-learn ở baro() và ở phần tính lại khóa của adapter;
  simplerca s1 : `Config()` mặc định -> `Config(metric_aggregation='channels')`;
  simplerca sham: đường native, phải khớp bản đóng băng từng bit.
Sham của BARO dùng lại lượt baro-b1-001 (đã khớp 52/52). Job và bản ghi dựng bằng đúng các hàm của các bộ phát lại đã khớp.
Mọi thực thể được tính trước; nhãn root nối sau ở bước collect.

Dùng:
  python contrast_scale_v1.py one <baro|simplerca> <nhánh> <RE2-TT|Nezha-OB> <opaque_id> <thư mục mới>
  python contrast_scale_v1.py all <baro|simplerca> <thư mục lượt mới>
"""
from __future__ import annotations

import contextlib
import importlib
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
BARO_SHAM = BASE / "runs/baro-b1-001/cases"
BRANCHES = {"baro": ("b2",), "simplerca": ("sham", "s1")}
CHANGED = {"baro": "b2", "simplerca": "s1"}
MAX_CHILD_S = 600


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=1, allow_nan=False)
        stream.write("\n")


def one(method, branch, dataset, opaque_id, directory):
    replay = importlib.import_module("replay_baro" if method == "baro" else "replay_simplerca_v4")
    shared = importlib.import_module("replay_microrank")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    audit = []
    entry, frozen, index26, _code_hashes = replay.source_for(dataset, opaque_id, audit)
    if frozen["status"] == "UNSUPPORTED":
        raise RuntimeError("nguồn UNSUPPORTED: không có đường chạy")
    from p3 import ban_ghi, runner, selector, worker
    if dataset == "RE2-TT":
        allow = selector.nap_allowlist(shared.safe_source("results/T-022/allowlist-dev.json"))
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
        if wanted != frozen["input_sha256"]:
            raise RuntimeError("hash đầu vào theo allowlist khác bản đóng băng")
        files = selector.chon_ca(allow, opaque_id, shared.RE2_RAW_REPO, kiem_hash=True)
        job = {"kind": "ranker", "method": method, "t": frozen["window"]["t"], "model": None,
               "files": {name: {"path": path, "sha256": wanted[name]} for name, path in files.items()}}
        invoke = worker.main
    else:
        from p3 import nezha, nezha_worker
        from p3.adapters.nezha import VARIANTS, VERSIONS
        allow_relative = "results/T-026/allowlist-dev.json"
        allow_path = shared.verify(allow_relative, index26["source_hashes"][allow_relative], shared.I26 + "#/source_hashes", audit)
        allow = nezha.nap_allowlist(allow_path)
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items()}
        if wanted != frozen["input_sha256"] or entry["trace_guard_s"] != 0:
            raise RuntimeError("hash đầu vào/guard của Nezha khác nguồn")
        script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
        constants = shared.literal_constants(shared.verify(script, index26["source_hashes"][script], shared.I26 + "#/source_hashes", audit))
        job = {"allowlist_path": str(allow_path), "opaque_id": opaque_id, "repo_root": str(shared.REPO),
               "view": "main", "method": method, "trace_guard_s": 0}
        invoke = nezha_worker.main
    shared.dump(directory / "job.json", job)
    change = None
    if (method, branch) == ("baro", "b2"):
        preprocessing = importlib.import_module("sklearn.preprocessing")
        baro_module = importlib.import_module("RCAEval.e2e.baro")
        if baro_module.RobustScaler is not preprocessing.RobustScaler:
            raise RuntimeError("baro() không dùng RobustScaler của sklearn.preprocessing")
        standard = preprocessing.StandardScaler
        baro_module.RobustScaler = standard        # lời gọi trong baro()
        preprocessing.RobustScaler = standard      # lời gọi `from sklearn.preprocessing import RobustScaler` trong adapter
        change = "RobustScaler -> StandardScaler"
    elif (method, branch) == ("simplerca", "s1"):
        package = importlib.import_module("simplerca")
        core = importlib.import_module("simplerca.core")
        if package.Config is not core.Config or core.Config().metric_aggregation != "events":
            raise RuntimeError("Config mặc định của simplerca khác dự kiến")
        package.Config = lambda: core.Config(metric_aggregation="channels")  # adapter gọi `from simplerca import Config` lúc chạy
        change = "Config(metric_aggregation='events') -> 'channels'"
    elif branch != "sham":
        raise RuntimeError("nhánh lạ")
    started = time.perf_counter()
    with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout, \
            (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            invoke(str(directory / "job.json"), str(directory / "ket-qua.json"))
    cost = shared.measured_cost(started, 0)
    output = shared.read(directory / "ket-qua.json")
    if output.get("hashseed") != "0":
        raise RuntimeError("worker báo hashseed khác 0")
    if dataset == "RE2-TT":
        base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None,
                "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, method, "a")
        if len(records) != 1:
            raise RuntimeError("không dựng lại được đúng một bản ghi")
    else:
        if len(output["ket_qua_nhieu"]) != 1:
            raise RuntimeError("worker không trả đúng một kết quả")
        record = ban_ghi.tao(method, VERSIONS[method], VARIANTS[method], "a", output["ket_qua_nhieu"][0], output["window"],
                             constants["CONFIG"], constants["WHY"], seed=None, hashseed=0, run_id=directory.name, opaque_id=opaque_id)
        record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
        record["input_sha256"] = output["input_sha256"]
        if entry["reused_pilot"]:
            record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
        else:
            record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
        ban_ghi.kiem(record)
        shared.dump(directory / "ban-ghi-0.json", record)
    result = shared.read(directory / "ban-ghi-0.json")
    differences = shared.compare_records(frozen, result)
    shared.dump(directory / "check.json", {"method": method, "branch": branch, "change": change, "dataset": dataset, "opaque_id": opaque_id,
                "frozen_path": entry["path"], "frozen_sha256": entry["sha256"], "frozen_status": frozen["status"],
                "branch_status": result["status"], "difference_count_vs_frozen": len(differences),
                "exact_vs_frozen": not differences, "wall_s": cost.get("wall_s")})
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
    return out, len(groups)


def collect(method, out):
    changed_branch = CHANGED[method]
    label_method = method
    labels = {}
    for row in read(LABELS)["main_rows"]:
        if row["method"] == label_method:
            labels[(row["dataset"], row["opaque_id"])] = {"root": row["root"], "fault": row["fault"], "cell": row["cell"],
                "t028": {"status": row["status"], "rank_min": row["rank_min"], "rank_max": row["rank_max"]}}
    cases = []
    for (dataset, opaque_id), label in sorted(labels.items()):
        base = {"dataset": dataset, "opaque_id": opaque_id, **label}
        directory = out / "cases" / dataset / opaque_id
        sham_dir = (BARO_SHAM / dataset / opaque_id / "sham") if method == "baro" else directory / "sham"
        sham_check = read(sham_dir / "check.json") if (sham_dir / "check.json").is_file() else None
        if sham_check is None or not sham_check["exact_vs_frozen"]:
            cases.append({**base, "status": "INVALID", "reason": "sham không khớp bản đóng băng hoặc chưa chạy"})
            continue
        if not (directory / changed_branch / "check.json").is_file():
            cases.append({**base, "status": "BRANCH_FAILED", "reason": "nhánh đổi không cho bản ghi; xem failure.json"})
            continue
        native, changed = read(sham_dir / "ban-ghi-0.json"), read(directory / changed_branch / "ban-ghi-0.json")
        item = {**base, "status": "OK", "native_status": native["status"], "branch_status": changed["status"]}
        if native["status"] != "OK" or changed["status"] != "OK":
            item["status"] = "N/A"
            cases.append(item)
            continue
        root = label["root"]
        views = {}
        for name, record in (("native", native), ("changed", changed)):
            rank, n_groups = ranks(record)
            score = {row["entity"]: row["key"][0] for row in record["entity_ranking"]}
            best = {}
            for row in record["ranking"]:
                best.setdefault(row["entity"], row["item"])
            if root not in rank:
                views[name] = {"root_ranked": False, "n_entities": len(rank)}
                continue
            above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
            views[name] = {"root_ranked": True, "n_entities": len(rank), "n_tie_groups": n_groups,
                           "root_rank_min": rank[root][0], "root_rank_max": rank[root][1], "root_score": score[root],
                           "root_best_item": best[root], "above_root": [{"entity": e, "score": score[e], "best_item": best[e]} for e in above]}
        item["native"], item["changed"] = views["native"], views["changed"]
        if views["native"]["root_ranked"]:
            item["self_check_native_rank_equals_t028"] = (label["t028"]["status"] == "OK" and
                [views["native"]["root_rank_min"], views["native"]["root_rank_max"]] == [label["t028"]["rank_min"], label["t028"]["rank_max"]])
        if views["native"]["root_ranked"] and views["changed"]["root_ranked"]:
            before, after = views["native"]["root_rank_min"], views["changed"]["root_rank_min"]
            item["effect_on_root"] = "tăng hạng" if after < before else "giảm hạng" if after > before else "không đổi"
            native_above = {a["entity"] for a in views["native"]["above_root"]}
            changed_above = {a["entity"] for a in views["changed"]["above_root"]}
            item["pairs_above_root_native"] = len(native_above)
            item["pairs_no_longer_above"] = len(native_above - changed_above)
            item["pairs_newly_above"] = len(changed_above - native_above)
        cases.append(item)
    valid = [c for c in cases if c["status"] == "OK" and "effect_on_root" in c]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        return {"n": len(rows),
                "effect_on_root": {k: count(lambda c, k=k: c["effect_on_root"] == k) for k in ("tăng hạng", "không đổi", "giảm hạng")},
                "hit1": {"native": count(lambda c: c["native"]["root_rank_max"] == 1), "changed": count(lambda c: c["changed"]["root_rank_max"] == 1)},
                "hit5": {"native": count(lambda c: c["native"]["root_rank_max"] <= 5), "changed": count(lambda c: c["changed"]["root_rank_max"] <= 5)},
                "hit1_optimistic_on_ties": {"native": count(lambda c: c["native"]["root_rank_min"] == 1),
                                            "changed": count(lambda c: c["changed"]["root_rank_min"] == 1)},
                "tie_groups_total": {"native": sum(c["native"]["n_tie_groups"] for c in rows), "changed": sum(c["changed"]["n_tie_groups"] for c in rows)},
                "entities_total": sum(c["native"]["n_entities"] for c in rows),
                "native_wrong_at_1": {"n": count(lambda c: c["native"]["root_rank_max"] > 1),
                                      "becomes_hit1": count(lambda c: c["native"]["root_rank_max"] > 1 and c["changed"]["root_rank_max"] == 1)},
                "native_hit_at_1": {"n": count(lambda c: c["native"]["root_rank_max"] == 1),
                                    "loses_hit1": count(lambda c: c["native"]["root_rank_max"] == 1 and c["changed"]["root_rank_max"] > 1)},
                "pairs_above_root_native": sum(c["pairs_above_root_native"] for c in rows),
                "pairs_no_longer_above": sum(c["pairs_no_longer_above"] for c in rows),
                "pairs_newly_above": sum(c["pairs_newly_above"] for c in rows)}

    summary = {"method": method, "changed_branch": changed_branch, "n_cases": len(cases),
               "status_counts": {s: sum(c["status"] == s for c in cases) for s in ("OK", "N/A", "INVALID", "BRANCH_FAILED")},
               "self_check_native_rank_equals_t028": sum(bool(c.get("self_check_native_rank_equals_t028")) for c in cases),
               "all": tally(valid), "by_dataset": {d: tally([c for c in valid if c["dataset"] == d]) for d in ("RE2-TT", "Nezha-OB")},
               "note": "n là số ca có sham khớp từng bit và root được xếp ở cả hai nhánh. Hit tính bi quan theo hòa, trừ dòng ghi rõ lạc quan. "
                       "Phép đổi chẩn đoán trên dev, thiết kế sau khi xem bảng mô tả; không phải phương pháp mới và không thay số P3."}
    write(out / "summary.json", {"schema": "T032-contrast-scale-v1", "design": "results/T-032/thiet-ke-phep-doi-002.md",
                                 "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def run_all(method, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    todo = sorted({(row["dataset"], row["opaque_id"]) for row in read(LABELS)["main_rows"] if row["method"] == method})
    for dataset, opaque_id in todo:
        for branch in BRANCHES[method]:
            directory = out / "cases" / dataset / opaque_id / branch
            command = [str(PYTHON), "-B", "-X", "utf8", str(Path(__file__).resolve()), "one", method, branch, dataset, opaque_id, str(directory)]
            started = time.perf_counter()
            try:
                done = subprocess.run(command, cwd=BASE, env=os.environ.copy(), stdin=subprocess.DEVNULL,
                                      capture_output=True, text=True, timeout=MAX_CHILD_S)
                code, tail = done.returncode, (done.stderr or "")[-2000:]
            except subprocess.TimeoutExpired:
                code, tail = -1, "timeout 600 s"
            event = {"at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "dataset": dataset, "opaque_id": opaque_id,
                     "branch": branch, "exit_code": code, "wall_s": time.perf_counter() - started}
            if code != 0:
                event["stderr_tail"] = tail
                if directory.is_dir() and not (directory / "failure.json").exists():
                    write(directory / "failure.json", event)
            with (out / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            print(dataset, opaque_id, branch, code, round(event["wall_s"], 1), flush=True)
    collect(method, out)


def main():
    if len(sys.argv) == 7 and sys.argv[1] == "one":
        try:
            return one(*sys.argv[2:7])
        except Exception:
            traceback.print_exc()
            return 1
    if len(sys.argv) == 4 and sys.argv[1] == "all":
        run_all(sys.argv[2], sys.argv[3])
        return 0
    if len(sys.argv) == 4 and sys.argv[1] == "collect":
        collect(sys.argv[2], Path(sys.argv[3]))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())

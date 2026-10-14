"""T-032 phép K-2 (thiet-ke-phep-doi-001.md mục 8): CIRCA OLS chấm với đồ thị không cạnh. Chỉ RE2-TT.

Chạy trên EC2. Mỗi ca hai nhánh, mỗi nhánh một tiến trình riêng:
  sham: đúng đường native (worker -> adapter -> score_graph); hai bản ghi `ols+rht_da` và `ols+rht` phải khớp
        bản đóng băng từng bit. Bản đóng băng CIRCA sinh trên laptop, nên sham cũng là phép thử xem EC2 có tái lập
        được CIRCA từng bit hay không. Sham lệch thì K-2 của ca đó vô hiệu và phải báo.
  k2:   chỉ bọc `p3.adapters.circa.do_thi` để bỏ mọi cạnh của đồ thị trả về (giữ nguyên tập nút); mọi thứ khác native.
Không sửa file mã nguồn nào, không dùng tolerance. Nhãn root nối sau ở bước collect.

Dùng:
  python contrast_circa_k2_v1.py one <sham|k2> <opaque_id> <thư mục mới>
  python contrast_circa_k2_v1.py all <thư mục lượt mới>
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
PYTHON = Path("/home/ubuntu/rca/T-025/envs/main/bin/python")
INDEX = REPO / "results/T-024/ban-ghi-dua-vao-cham.json"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
VARIANTS = ("ols+rht_da", "ols+rht")  # thứ tự bản ghi 0, 1 của runner
MAX_CHILD_S = 600
HUGE = 1e10  # mốc báo riêng theo Q-82/WHY-36


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=1)
        stream.write("\n")


def frozen_pair(opaque_id):
    entries = {e["variant"]: e for e in read(INDEX)["records"]
               if e["method"] == "circa" and e["opaque_id"] == opaque_id and e.get("variant") in VARIANTS and e["seed"] is None}
    if set(entries) != set(VARIANTS):
        raise RuntimeError("không đủ cặp bản đóng băng OLS")
    out = []
    for variant in VARIANTS:
        path = REPO / entries[variant]["path"]
        if sha(path) != entries[variant]["sha256"]:
            raise RuntimeError("bản đóng băng khác hash chỉ mục: " + variant)
        out.append((entries[variant], read(path)))
    return out


def one(branch, opaque_id, directory):
    import replay_microrank as shared
    from p3 import runner, selector, worker
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    pair = frozen_pair(opaque_id)
    frozen = [record for _entry, record in pair]
    allow = selector.nap_allowlist(shared.safe_source("results/T-022/allowlist-dev.json"))
    wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
    if wanted != frozen[0]["input_sha256"]:
        raise RuntimeError("hash đầu vào theo allowlist khác bản đóng băng")
    files = selector.chon_ca(allow, opaque_id, shared.RE2_RAW_REPO, kiem_hash=True)
    job = {"kind": "ranker", "method": "circa", "t": frozen[0]["window"]["t"], "model": "ols",
           "files": {name: {"path": value, "sha256": wanted[name]} for name, value in files.items()}}
    shared.dump(directory / "job.json", job)
    removed = None
    if branch == "k2":
        import p3.adapters.circa as adapter
        original = adapter.do_thi
        removed = {}

        def without_edges(columns, spans, t, circa_src=adapter.CIRCA_SRC):
            graph, report = original(columns, spans, t, circa_src)
            graph = graph.copy()
            removed["nodes"], removed["edges_removed"] = graph.number_of_nodes(), graph.number_of_edges()
            graph.remove_edges_from(list(graph.edges))
            return graph, report

        adapter.do_thi = without_edges  # bước duy nhất bị đổi
    started = time.perf_counter()
    with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout, \
            (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            worker.main(str(directory / "job.json"), str(directory / "ket-qua.json"))
    cost = shared.measured_cost(started, 0)
    output = shared.read(directory / "ket-qua.json")
    if output.get("hashseed") != "0":
        raise RuntimeError("worker báo hashseed khác 0")
    base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None, "hashseed": 0,
            "detector": None, "detector_columns": None, "config_id": frozen[0]["config_id"]}
    records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "circa", "a", model="ols")
    if len(records) != 2:
        raise RuntimeError("không dựng lại được đủ hai biến thể")
    replay = [shared.read(directory / ("ban-ghi-" + str(i) + ".json")) for i in range(2)]
    if [r["variant"] for r in replay] != list(VARIANTS):
        raise RuntimeError("thứ tự biến thể của bản ghi khác dự kiến")
    differences = [shared.compare_records(frozen[i], replay[i]) for i in range(2)]
    shared.dump(directory / "check.json", {"branch": branch, "opaque_id": opaque_id, "edges_removed": removed,
                "frozen_paths": [entry["path"] for entry, _record in pair], "frozen_statuses": [r["status"] for r in frozen],
                "branch_statuses": [r["status"] for r in replay],
                "difference_count_vs_frozen": {VARIANTS[i]: len(differences[i]) for i in range(2)},
                "first_differences": {VARIANTS[i]: differences[i][:5] for i in range(2)},
                "exact_vs_frozen": not (differences[0] or differences[1]), "wall_s": cost.get("wall_s"),
                "note": "sham phải khớp tuyệt đối cả hai biến thể; k2 được phép khác"})
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


def collect(out):
    labels = {}
    for row in read(LABELS)["main_rows"]:
        if row["dataset"] == "RE2-TT":
            labels.setdefault(row["opaque_id"], {"root": row["root"], "fault": row["fault"], "cell": row["cell"]})
    cases = []
    for opaque_id, label in sorted(labels.items()):
        directory = out / "cases" / opaque_id
        base = {"opaque_id": opaque_id, **label}
        state = {b: (read(directory / b / "check.json") if (directory / b / "check.json").is_file() else None) for b in ("sham", "k2")}
        if state["sham"] is None:
            cases.append({**base, "status": "SHAM_FAILED", "reason": "nhánh sham không cho bản ghi; xem failure.json"})
            continue
        if not state["sham"]["exact_vs_frozen"]:
            cases.append({**base, "status": "SHAM_NOT_EXACT", "difference_count_vs_frozen": state["sham"]["difference_count_vs_frozen"],
                          "first_differences": state["sham"]["first_differences"]})
            continue
        if state["k2"] is None:
            cases.append({**base, "status": "K2_FAILED", "reason": "nhánh k2 không cho bản ghi; xem failure.json"})
            continue
        item = {**base, "status": "OK", "edges_removed": state["k2"]["edges_removed"]}
        native_rht = read(directory / "sham/ban-ghi-1.json")
        native_da = read(directory / "sham/ban-ghi-0.json")
        k2_rht = read(directory / "k2/ban-ghi-1.json")
        k2_da = read(directory / "k2/ban-ghi-0.json")
        # Đồ thị không cạnh: DA không có hậu duệ để cộng. Ghi lại hai bảng k2 có cùng thứ tự thực thể hay không.
        item["k2_da_entity_order_equals_k2_rht"] = [r["entity"] for r in k2_da["entity_ranking"]] == [r["entity"] for r in k2_rht["entity_ranking"]]
        native_nodes, k2_nodes = native_rht["diagnostics"]["nodes"], k2_rht["diagnostics"]["nodes"]
        shared_nodes = sorted(set(native_nodes) & set(k2_nodes))
        with_parents = [n for n in shared_nodes if native_nodes[n]["regression_route"] == "linear_regression"]
        changed = [n for n in shared_nodes if float(native_nodes[n]["rht_score"]).hex() != float(k2_nodes[n]["rht_score"]).hex()]
        item["nodes"] = {"n": len(shared_nodes), "native_route_linear_regression": len(with_parents),
                         "score_changed_without_edges": len(changed),
                         "changed_but_no_regression_natively": len(set(changed) - set(with_parents)),
                         "regression_natively_but_unchanged": len(set(with_parents) - set(changed)),
                         "regression_lowers_score": sum(native_nodes[n]["rht_score"] < k2_nodes[n]["rht_score"] for n in with_parents),
                         "regression_raises_score": sum(native_nodes[n]["rht_score"] > k2_nodes[n]["rht_score"] for n in with_parents),
                         "huge_native": sum(abs(native_nodes[n]["rht_score"]) > HUGE for n in shared_nodes),
                         "huge_k2": sum(abs(k2_nodes[n]["rht_score"]) > HUGE for n in shared_nodes)}
        root = label["root"]
        views = {}
        for name, record in (("native_rht", native_rht), ("native_da", native_da), ("k2_rht", k2_rht)):
            rank = ranks(record)
            if root not in rank:
                views[name] = {"root_ranked": False}
                continue
            best = {}
            for row in record["ranking"]:
                best.setdefault(row["entity"], row["item"])
            above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
            views[name] = {"root_ranked": True, "root_rank_min": rank[root][0], "root_rank_max": rank[root][1],
                           "root_best_node": best[root], "n_above": len(above), "above_root": above[:15]}
        item["views"] = views
        if all(v["root_ranked"] for v in views.values()):
            a, b = views["native_rht"]["root_rank_min"], views["k2_rht"]["root_rank_min"]
            # So native (có hồi quy theo cha) với không cạnh: hạng nhỏ hơn là tốt hơn.
            item["regression_on_parents_effect_on_root"] = "tăng hạng" if a < b else "giảm hạng" if a > b else "không đổi"
            root_node = views["native_rht"]["root_best_node"]
            item["root_best_node_native"] = {"node": root_node, "route": native_nodes[root_node]["regression_route"],
                                             "parents": native_nodes[root_node]["parents"],
                                             "rht_native": native_nodes[root_node]["rht_score"],
                                             "rht_without_edges": k2_nodes.get(root_node, {}).get("rht_score")}
        cases.append(item)
    ok = [c for c in cases if c["status"] == "OK" and "regression_on_parents_effect_on_root" in c]

    def count(predicate):
        return sum(1 for c in ok if predicate(c))

    summary = {"n_cases": len(cases), "status_counts": {s: sum(c["status"] == s for c in cases)
                                                         for s in ("OK", "SHAM_NOT_EXACT", "SHAM_FAILED", "K2_FAILED")},
               "n_interpretable": len(ok),
               "regression_on_parents_effect_on_root": {k: count(lambda c, k=k: c["regression_on_parents_effect_on_root"] == k)
                                                        for k in ("tăng hạng", "không đổi", "giảm hạng")},
               "hit1": {name: count(lambda c, name=name: c["views"][name]["root_rank_max"] == 1) for name in ("k2_rht", "native_rht", "native_da")},
               "hit5": {name: count(lambda c, name=name: c["views"][name]["root_rank_max"] <= 5) for name in ("k2_rht", "native_rht", "native_da")},
               "k2_da_entity_order_equals_k2_rht": count(lambda c: c["k2_da_entity_order_equals_k2_rht"]),
               "nodes_total": {key: sum(c["nodes"][key] for c in ok) for key in (ok[0]["nodes"] if ok else {})},
               "note": "n_interpretable là số ca có sham khớp từng bit cả hai biến thể và root được xếp ở mọi bảng. Hit tính bi quan theo hòa. "
                       "K-2 là phép đổi chẩn đoán trên dev, không phải phương pháp mới và không thay số P3."}
    write(out / "summary.json", {"schema": "T032-CIRCA-K2-v1", "design": "results/T-032/thiet-ke-phep-doi-001.md#8",
                                 "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def run_all(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    todo = sorted({row["opaque_id"] for row in read(LABELS)["main_rows"] if row["dataset"] == "RE2-TT"})
    for opaque_id in todo:
        for branch in ("sham", "k2"):
            directory = out / "cases" / opaque_id / branch
            command = [str(PYTHON), "-B", "-X", "utf8", str(Path(__file__).resolve()), "one", branch, opaque_id, str(directory)]
            started = time.perf_counter()
            try:
                done = subprocess.run(command, cwd=BASE, env=os.environ.copy(), stdin=subprocess.DEVNULL,
                                      capture_output=True, text=True, timeout=MAX_CHILD_S)
                code, tail = done.returncode, (done.stderr or "")[-2000:]
            except subprocess.TimeoutExpired:
                code, tail = -1, "timeout 600 s"
            event = {"at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "opaque_id": opaque_id, "branch": branch,
                     "exit_code": code, "wall_s": time.perf_counter() - started}
            if code != 0:
                event["stderr_tail"] = tail
                if directory.is_dir() and not (directory / "failure.json").exists():
                    write(directory / "failure.json", event)
            with (out / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            print(opaque_id, branch, code, round(event["wall_s"], 1), flush=True)
    collect(out)


def main():
    if len(sys.argv) == 5 and sys.argv[1] == "one":
        try:
            return one(sys.argv[2], sys.argv[3], sys.argv[4])
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

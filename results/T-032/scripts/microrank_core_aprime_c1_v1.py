"""T-032 MicroRank: bảng lõi own/context, phép M-A′ (SPEC) và M-C1 (thiet-ke-phep-doi-001.md mục 4).

Chạy trên EC2 trên bản sao trung gian J0 của các ca laptop đã khớp tuyệt đối. Không gọi detector, graph hay PageRank.
Chỉ gọi hàm native `calculate_spectrum_without_delay_list` của src/microrank/official.py với từ điển đầu vào:
  w_native: trọng số và số đếm của J0. Sham: điểm và thứ tự phải trùng bản ghi native từng bit.
  w_unit  : (A′) trọng số = 1 cho đúng các operation có trong từ điển trọng số của từng nhóm; số đếm giữ nguyên.
  c1      : số đếm nhóm A của operation = số trace thuộc A mà chính operation có span mang cờ; trọng số native.
Mọi operation/service được tính trước; nhãn root nối sau cùng.
Dùng: python microrank_core_aprime_c1_v1.py <thư mục J0> <thư mục lượt mới>
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
sys.path.insert(0, str(BASE / "scripts"))
sys.path.insert(0, str(REPO / "src"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def spectrum(official, weights_a, weights_n, counts_a, counts_n, size_a, size_n):
    names, scores = official.calculate_spectrum_without_delay_list(
        anomaly_result=weights_a, normal_result=weights_n, anomaly_list_len=size_a, normal_list_len=size_n,
        top_max=max(len(set(weights_a) | set(weights_n)), 5), normal_num_list=counts_n, anomaly_num_list=counts_a,
        spectrum_method="dstar2")
    return list(names), [float(x) for x in scores]


def fixtures(official):
    """Kiểm tay công thức DStar2 native theo mục A′ của SPEC: đủ hai nhóm, thiếu một nhóm, hòa, mẫu số 0."""
    out = {}
    names, scores = spectrum(official, {"x": 0.5}, {"x": 0.25}, {"x": 4}, {"x": 8}, 10, 20)
    out["both_groups"] = scores == [(0.5 * 4) ** 2 / (0.25 * 8 + 0.5 * 6)]            # ef=2, nf=3, ep=2 -> 0.8
    names, scores = spectrum(official, {"x": 0.5}, {}, {"x": 4}, {}, 10, 20)
    out["anomaly_only"] = scores == [(0.5 * 4) ** 2 / (0.0000001 + 0.5 * 6)]
    names, scores = spectrum(official, {}, {"y": 0.25}, {}, {"y": 8}, 10, 20)
    out["normal_only"] = scores == [0.0000001 * 0.0000001 / ((1 + 0.25) * 8 + 0.0000001)]
    names, scores = spectrum(official, {"x": 0.5, "y": 0.5}, {"x": 0.25, "y": 0.25}, {"x": 4, "y": 4}, {"x": 8, "y": 8}, 10, 20)
    out["tie_keeps_insertion_order"] = names == ["x", "y"] and scores[0] == scores[1]
    try:
        spectrum(official, {"x": 0.5}, {"x": 0.25}, {"x": 10}, {"x": 0}, 10, 20)       # nf = 0 và ep = 0
        out["zero_denominator_raises_as_native"] = False
    except ZeroDivisionError:
        out["zero_denominator_raises_as_native"] = True
    return {"pass": all(out.values()), "checks": out}


def entity_view(names, scores, service_of):
    best = {}
    for op, score in zip(names, scores):
        service = service_of[op]
        if service not in best or score > best[service]["score"]:
            best[service] = {"score": score, "operation": op}
    for row in best.values():
        row["rank_min"] = 1 + sum(other["score"] > row["score"] for other in best.values())
        row["rank_max"] = sum(other["score"] >= row["score"] for other in best.values())
    return best


def margin(a, b):
    return None if abs(a) + abs(b) == 0 else (a - b) / (abs(a) + abs(b))


def one_case(directory, label, official, table_columns):
    result = read(directory / "native-result.json")
    if result.get("status") != "ok":
        return {"status": "N/A", "reason": "trạng thái native " + str(result.get("status")) + ": thiếu nhóm trace"}
    call = read(directory / "001-microrank.json")
    after = pd.DataFrame(table_columns(directory, call["tables"]["after"]))
    anomaly, normal = result["groups"]["anomaly"]["official"], result["groups"]["normal"]["official"]
    size_a, size_n = result["counts"]["anomaly"], result["counts"]["normal"]
    service_of = result["operation_services"]
    # --- J0 và sham ---
    names, scores = spectrum(official, anomaly["weights"], normal["weights"], anomaly["tracecounts"], normal["tracecounts"], size_a, size_n)
    saved = result["scores"]
    sham = (names == result["full_ranks"] and len(scores) == len(saved)
            and all(float(saved[op]).hex() == score.hex() for op, score in zip(names, scores)))
    # --- đếm riêng, tính lại từ bảng after của J0 ---
    after["traceID"] = after["traceID"].astype(str)
    abnormal_traces = set(after.loc[after["abnormal"], "traceID"])
    partition_ok = len(abnormal_traces) == size_a and after["traceID"].nunique() == size_a + size_n
    in_a = after[after["traceID"].isin(abnormal_traces)]
    coverage_a = in_a.groupby("operation")["traceID"].nunique().to_dict()
    coverage_n = after[~after["traceID"].isin(abnormal_traces)].groupby("operation")["traceID"].nunique().to_dict()
    own_a = after[after["abnormal"]].groupby("operation")["traceID"].nunique().to_dict()
    counts_ok = (all(coverage_a.get(op, 0) == count for op, count in anomaly["tracecounts"].items())
                 and all(coverage_n.get(op, 0) == count for op, count in normal["tracecounts"].items()))
    # --- A′: trọng số đơn vị ---
    unit_names, unit_scores = spectrum(official, {op: 1.0 for op in anomaly["weights"]}, {op: 1.0 for op in normal["weights"]},
                                       anomaly["tracecounts"], normal["tracecounts"], size_a, size_n)
    # --- C1: đếm riêng thay đếm phủ ở nhóm A ---
    c1_names, c1_scores = spectrum(official, anomaly["weights"], normal["weights"],
                                   {op: int(own_a.get(op, 0)) for op in anomaly["tracecounts"]}, normal["tracecounts"], size_a, size_n)
    views = {"w_native": entity_view(names, scores, service_of), "w_unit": entity_view(unit_names, unit_scores, service_of),
             "c1": entity_view(c1_names, c1_scores, service_of)}
    by_branch = {"w_native": dict(zip(names, scores)), "w_unit": dict(zip(unit_names, unit_scores)), "c1": dict(zip(c1_names, c1_scores))}
    operations = {}
    for op in names:
        cells = result["spectrum"][op]
        operations[op] = {"service": service_of[op], "cov_A": anomaly["tracecounts"].get(op), "cov_N": normal["tracecounts"].get(op),
                          "own_A": int(own_a.get(op, 0)),
                          "context_only_A": None if op not in anomaly["tracecounts"] else anomaly["tracecounts"][op] - int(own_a.get(op, 0)),
                          "w_A": anomaly["weights"].get(op), "w_N": normal["weights"].get(op),
                          "branch_missing_group": "none" if op in anomaly["weights"] and op in normal["weights"] else
                                                  "normal_missing" if op in anomaly["weights"] else "anomaly_missing",
                          "cells_native": cells, "score": {branch: by_branch[branch][op] for branch in by_branch}}
    # Quan hệ gọi mức service từ cặp cha-con khác service trong bảng after, không dùng nhãn.
    key = after["traceID"] + "|" + after["spanID"].astype(str)
    service_by_key = pd.Series(after["serviceName"].to_numpy(), index=key.to_numpy())
    service_by_key = service_by_key[~service_by_key.index.duplicated(keep=False)]
    parent_service = (after["traceID"] + "|" + after["parentSpanID"].astype(str)).map(service_by_key)
    cross = pd.DataFrame({"caller": parent_service.to_numpy(), "callee": after["serviceName"].to_numpy()}).dropna()
    edges = sorted({(str(a), str(b)) for a, b in zip(cross["caller"], cross["callee"]) if a != b})
    # --- từ đây mới nối nhãn ---
    root = label["root"]
    callers_of_root = sorted({a for a, b in edges if b == root})
    callees_of_root = sorted({b for a, b in edges if a == root})
    item = {"status": "OK", "root": root, "fault": label["fault"], "cell": label["cell"], "t028": label["t028"],
            "sham_w_native_bit_exact": bool(sham), "partition_counts_match": bool(partition_ok), "coverage_counts_match": bool(counts_ok),
            "counts": {"A": size_a, "N": size_n, "abnormal_spans": int(after["abnormal"].sum()), "operations": len(names),
                       "share_A": size_a / (size_a + size_n),
                       "A_traces_without_root_service": int(len(abnormal_traces - set(in_a.loc[in_a["serviceName"] == root, "traceID"]))),
                       "A_traces_root_service_own_abnormal": int(in_a.loc[(in_a["serviceName"] == root) & in_a["abnormal"], "traceID"].nunique())},
            "callers_of_root": callers_of_root, "callees_of_root": callees_of_root, "branches": {}, "operations": operations}
    for branch, view in views.items():
        if root not in view:
            item["branches"][branch] = {"root_ranked": False, "n_entities": len(view)}
            continue
        root_row = view[root]
        above = sorted((e for e, r in view.items() if r["rank_max"] < root_row["rank_min"]), key=lambda e: view[e]["rank_min"])
        item["branches"][branch] = {"root_ranked": True, "n_entities": len(view), "root": root_row, "above_root": [
            {"entity": e, "relation": "caller_of_root" if e in callers_of_root else "callee_of_root" if e in callees_of_root else "other",
             **view[e], "max_operation_own_A": operations[view[e]["operation"]]["own_A"],
             "max_operation_context_only_A": operations[view[e]["operation"]]["context_only_A"],
             "margin_vs_root": margin(view[e]["score"], root_row["score"])} for e in above],
            "callers_above": [e for e in above if e in callers_of_root]}
    native = item["branches"]["w_native"]
    if native["root_ranked"]:
        t028 = label["t028"]
        item["self_check_native_rank_equals_t028"] = (t028["status"] == "OK" and
            [native["root"]["rank_min"], native["root"]["rank_max"]] == [t028["rank_min"], t028["rank_max"]])
        for branch in ("w_unit", "c1"):
            other = item["branches"][branch]
            if not other["root_ranked"]:
                continue
            before, after_rank = native["root"]["rank_min"], other["root"]["rank_min"]
            item[branch + "_effect_on_root"] = "tăng hạng" if after_rank < before else "giảm hạng" if after_rank > before else "không đổi"
            pairs = {}
            for row in native["above_root"]:
                e = row["entity"]
                new = views[branch].get(e)
                new_margin = None if new is None else margin(new["score"], other["root"]["score"])
                pairs[e] = {"relation": row["relation"], "margin_native": row["margin_vs_root"], "margin_branch": new_margin,
                            "delta": None if new_margin is None or row["margin_vs_root"] is None else row["margin_vs_root"] - new_margin,
                            "still_above": new is not None and new["rank_max"] < other["root"]["rank_min"],
                            "max_operation_changed": new is not None and new["operation"] != row["operation"]}
            item[branch + "_pairs_above_root_native"] = pairs
    return item


def main():
    source, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    from microrank import official
    from replay_microrank import table_columns
    fixture = fixtures(official)
    (out / "spectrum-fixtures.json").write_text(json.dumps(fixture, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not fixture["pass"]:
        print(json.dumps(fixture, ensure_ascii=False))
        return 1
    labels = {}
    for row in read(LABELS)["main_rows"]:
        if row["method"] == "microrank_full":
            flags = {k: (((row.get("mechanisms") or {}).get(k) or {}).get("assignment") or {}).get("multi") for k in ("1", "5")}
            labels[(row["dataset"], row["opaque_id"])] = {"root": row["root"], "fault": row["fault"], "cell": row["cell"],
                "t028": {"status": row["status"], "rank_min": row["rank_min"], "rank_max": row["rank_max"], "multi_flags": flags}}
    transfer = read(source / "manifest.json")
    cases = []
    for entry in transfer["cases"]:
        dataset, opaque_id = entry["dataset"], entry["opaque_id"]
        base = {"dataset": dataset, "opaque_id": opaque_id, "source_status": entry["source_status"]}
        if entry["source_status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "nguồn " + entry["source_status"] + ": phương pháp không trả điểm"})
            continue
        directory = source / dataset / opaque_id
        if any(sha(directory / name) != digest for name, digest in entry["files"].items()):
            cases.append({**base, "status": "INVALID", "reason": "file J0 trên EC2 khác hash đã chép"})
            continue
        try:
            item = one_case(directory, labels[(dataset, opaque_id)], official, table_columns)
        except Exception as error:  # giữ ca lỗi trong mẫu số
            item = {"status": "TOOL_ERROR", "error": type(error).__name__ + ": " + str(error)}
        item = {**base, **item}
        (out / "cases").mkdir(exist_ok=True)
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps(item, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        cases.append({k: v for k, v in item.items() if k != "operations"})
        print(dataset, opaque_id, item.get("status"), item.get("sham_w_native_bit_exact"), item.get("w_unit_effect_on_root"), item.get("c1_effect_on_root"), flush=True)

    def tally(rows, branch):
        key = branch + "_effect_on_root"
        rows = [c for c in rows if c.get("status") == "OK" and c.get("sham_w_native_bit_exact") and key in c]
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        native = lambda c: c["branches"]["w_native"]
        other = lambda c: c["branches"][branch]
        return {"n": len(rows),
                "effect_on_root": {k: count(lambda c, k=k: c[key] == k) for k in ("tăng hạng", "không đổi", "giảm hạng")},
                "hit1": {"native": count(lambda c: native(c)["root"]["rank_max"] == 1), branch: count(lambda c: other(c)["root"]["rank_max"] == 1)},
                "hit5": {"native": count(lambda c: native(c)["root"]["rank_max"] <= 5), branch: count(lambda c: other(c)["root"]["rank_max"] <= 5)},
                "cases_with_caller_above_root": {"native": count(lambda c: native(c)["callers_above"]), branch: count(lambda c: other(c)["callers_above"])},
                "native_wrong_at_1": {"n": count(lambda c: native(c)["root"]["rank_max"] > 1),
                                      "becomes_hit1": count(lambda c: native(c)["root"]["rank_max"] > 1 and other(c)["root"]["rank_max"] == 1)},
                "native_hit_at_1": {"n": count(lambda c: native(c)["root"]["rank_max"] == 1),
                                    "loses_hit1": count(lambda c: native(c)["root"]["rank_max"] == 1 and other(c)["root"]["rank_max"] > 1)},
                "entity_pairs_above_root_native": {
                    "n": sum(len(c[branch + "_pairs_above_root_native"]) for c in rows),
                    "no_longer_above": sum(not p["still_above"] for c in rows for p in c[branch + "_pairs_above_root_native"].values()),
                    "callers_n": sum(p["relation"] == "caller_of_root" for c in rows for p in c[branch + "_pairs_above_root_native"].values()),
                    "callers_no_longer_above": sum(p["relation"] == "caller_of_root" and not p["still_above"]
                                                   for c in rows for p in c[branch + "_pairs_above_root_native"].values())}}

    summary = {"n_cases": len(cases), "status_counts": {s: sum(c.get("status") == s for c in cases) for s in ("OK", "N/A", "INVALID", "TOOL_ERROR")},
               "sham_w_native_bit_exact": sum(bool(c.get("sham_w_native_bit_exact")) for c in cases),
               "partition_counts_match": sum(bool(c.get("partition_counts_match")) for c in cases),
               "coverage_counts_match": sum(bool(c.get("coverage_counts_match")) for c in cases),
               "self_check_native_rank_equals_t028": sum(bool(c.get("self_check_native_rank_equals_t028")) for c in cases),
               "w_unit": {"all": tally(cases, "w_unit"), **{d: tally([c for c in cases if c["dataset"] == d], "w_unit") for d in ("RE2-TT", "Nezha-OB")}},
               "c1": {"all": tally(cases, "c1"), **{d: tally([c for c in cases if c["dataset"] == d], "c1") for d in ("RE2-TT", "Nezha-OB")}},
               "note": "n là số ca OK có sham khớp từng bit và root được xếp ở cả hai nhánh. Hit tính bi quan theo hòa. "
                       "Hai nhánh là phép đổi chẩn đoán trên dev, không phải phương pháp mới và không thay số P3."}
    (out / "summary.json").write_text(json.dumps({"schema": "T032-microrank-core-aprime-c1-v1",
        "design": ["tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md#A′", "results/T-032/thiet-ke-phep-doi-001.md#4"],
        "spectrum_fixtures": fixture, "j0_manifest_sha256": sha(source / "manifest.json"), "summary": summary, "cases": cases},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

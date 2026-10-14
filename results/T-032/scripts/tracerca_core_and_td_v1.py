"""T-032 TraceRCA: bảng lõi a/n/H/ji cho mọi operation và phép T-D (thiet-ke-phep-doi-001.md mục 5).

Chạy trên EC2, chỉ đọc capture của các ca đã phát lại khớp tuyệt đối. Không gọi phương pháp, không ghi đè lõi.
Với mỗi ca OK:
  1. dựng lại phép tính native từ `adapter-input.parquet` bằng đúng các biểu thức của RCAEval e2e/tracerca.py;
     sham: ji dựng lại phải trùng ji native từng bit, nếu không thì ca đó không được diễn giải;
  2. kiểm đẳng thức ji = 2a/(n+H) bằng số;
  3. T-D: thay duration bằng u = duration trừ độ dài hợp các khoảng span con trực tiếp (cắt vào khoảng của cha)
     ở cả thống kê nền và cờ sau mốc; span thuộc trước/sau mốc vẫn theo thời điểm kết thúc gốc;
  4. tính cho mọi thực thể trước, nối nhãn root sau cùng.
Dùng: python tracerca_core_and_td_v1.py <thư mục lượt mới> [dataset:opaque_id để chạy thử một ca]
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
COHORT = BASE / "runs/tracerca-cohort-simple-001"
PLAN = BASE / "sources/tracerca-plan-52.json"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
REUSED = {"re2-ok": BASE / "runs/tracerca-path-pilots-002/re2-ok",
          "nezha-ok": BASE / "runs/tracerca-path-pilots-002/nezha-ok"}
sys.path.insert(0, str(BASE / "scripts"))


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def uncovered(frame):
    """u = duration - độ dài hợp các khoảng con trực tiếp đã cắt vào khoảng của cha.

    frame: traceID, spanID, parentSpanID, startTime, duration (số nguyên micro giây).
    Con được tìm trong cùng trace theo parentSpanID == spanID. Trả (u, covered, n_children, parent_resolved).
    Không gọi u là thời gian tự xử lý; nó chỉ là phần của span không được span con quan sát được phủ.
    """
    start = frame["startTime"].to_numpy(dtype="int64")
    duration = frame["duration"].to_numpy(dtype="int64")
    end = start + duration
    key = frame["traceID"].astype(str) + "|" + frame["spanID"].astype(str)
    position = pd.Series(np.arange(len(frame)), index=key.to_numpy())
    duplicated = position.index.duplicated(keep=False)
    position = position[~duplicated]  # định danh trùng không dùng làm cha
    parent_key = frame["traceID"].astype(str) + "|" + frame["parentSpanID"].astype(str)
    parent_position = parent_key.map(position).to_numpy(dtype="float64")
    resolved = ~np.isnan(parent_position)
    child_index = np.flatnonzero(resolved)
    parent_index = parent_position[resolved].astype("int64")
    clipped_start = np.clip(start[child_index], start[parent_index], end[parent_index])
    clipped_end = np.clip(end[child_index], start[parent_index], end[parent_index])
    order = np.lexsort((clipped_end, clipped_start, parent_index))
    parent_sorted, s, e = parent_index[order], clipped_start[order], clipped_end[order]
    covered = np.zeros(len(frame), dtype="int64")
    children = np.zeros(len(frame), dtype="int64")
    if len(parent_sorted):
        table = pd.DataFrame({"p": parent_sorted, "s": s, "e": e})
        previous_max = table.groupby("p", sort=False)["e"].cummax().groupby(table["p"], sort=False).shift(1)
        low = np.where(previous_max.isna().to_numpy(), s, np.maximum(s, previous_max.fillna(0).to_numpy(dtype="int64")))
        contribution = np.maximum(0, e - low)
        np.add.at(covered, parent_sorted, contribution)
        np.add.at(children, parent_sorted, 1)
    return duration - covered, covered, children, resolved


def interval_fixtures():
    """Các trường hợp tự dựng theo SPEC: lồng nhau, song song chồng lấn, con vượt cha, thiếu cha, chạm biên."""
    rows = [  # trace, span, parent, start, duration
        ("t1", "p", "root", 0, 100), ("t1", "c1", "p", 10, 20), ("t1", "c2", "p", 40, 10),          # lồng, rời nhau: phủ 30
        ("t2", "p", "root", 0, 100), ("t2", "c1", "p", 10, 40), ("t2", "c2", "p", 30, 40),          # song song chồng: hợp [10,70] = 60
        ("t3", "p", "root", 0, 100), ("t3", "c1", "p", 80, 50),                                     # con vượt cha: cắt còn 20
        ("t4", "c1", "missing", 0, 30),                                                             # thiếu cha
        ("t5", "p", "root", 0, 100), ("t5", "c1", "p", 0, 100), ("t5", "g", "c1", 20, 10),          # con phủ hết; cháu không tính cho ông
        ("t6", "p", "root", 50, 0), ("t6", "c1", "p", 50, 0),                                       # thời lượng 0
        ("t7", "p", "root", 0, 100), ("t7", "c1", "p", -20, 30),                                    # con bắt đầu trước cha: cắt còn 10
    ]
    frame = pd.DataFrame(rows, columns=["traceID", "spanID", "parentSpanID", "startTime", "duration"])
    u, covered, children, resolved = uncovered(frame)
    got = {(r[0], r[1]): (int(u[i]), int(covered[i]), int(children[i]), bool(resolved[i])) for i, r in enumerate(rows)}
    expected = {("t1", "p"): (70, 30, 2, False), ("t2", "p"): (40, 60, 2, False), ("t3", "p"): (80, 20, 1, False),
                ("t4", "c1"): (30, 0, 0, False), ("t5", "p"): (0, 100, 1, False), ("t5", "c1"): (90, 10, 1, True),
                ("t6", "p"): (0, 0, 1, False), ("t7", "p"): (90, 10, 1, False)}
    bad = {str(k): {"got": got[k], "expected": v} for k, v in expected.items() if got[k] != v}
    return {"pass": not bad, "checked": len(expected), "mismatches": bad}


def native_formula(span_df, inject_time, quantity):
    """Bản sao các biểu thức của RCAEval e2e/tracerca.py; `quantity` là cột dùng cho SLO và cờ."""
    normal_df = span_df[span_df["startTime"] + span_df["duration"] < inject_time]
    anomal_df = span_df[span_df["startTime"] + span_df["duration"] >= inject_time].copy()
    slo = {}
    for op in normal_df["operation"].dropna().unique():
        mean = round(normal_df[normal_df["operation"] == op][quantity].mean() / 1_000, 2)
        std = round(normal_df[normal_df["operation"] == op][quantity].std() / 1_000, 2)
        slo[op] = {"mean": mean, "std": std}
    anomal_df["mean"] = anomal_df["operation"].apply(lambda op: slo[op]["mean"])
    anomal_df["std"] = anomal_df["operation"].apply(lambda op: slo[op]["std"])
    anomal_df["abnormal"] = anomal_df[quantity] / 1_000 >= anomal_df["mean"] + 3 * anomal_df["std"]
    operations = list(anomal_df.operation.unique())
    total_abnormal = anomal_df["abnormal"].sum()
    out = {}
    for op in operations:
        a = anomal_df[anomal_df["operation"] == op]["abnormal"].sum()
        n = anomal_df[anomal_df["operation"] == op]["operation"].count()
        support = a / total_abnormal
        confidence = a / n
        ji = 2 * support * confidence / (support + confidence)
        out[op] = {"a": int(a), "n": int(n), "ji": float(ji), "mean_ms": slo[op]["mean"], "std_ms": slo[op]["std"]}
    return out, int(total_abnormal), len(normal_df), len(anomal_df)


def same_float(x, y):
    if isinstance(x, float) and isinstance(y, float) and math.isnan(x) and math.isnan(y):
        return True
    return float(x).hex() == float(y).hex()


def decode_ji(locals_ji):
    return {op: (float("nan") if isinstance(v, dict) else float(v)) for op, v in locals_ji.items()}


def entity_ranking(scores, service_of):
    """service -> điểm = ji hữu hạn cao nhất; hạng theo nhóm hòa (điểm bằng nhau từng bit)."""
    best = {}
    for op, row in scores.items():
        if math.isfinite(row["ji"]):
            service = service_of[op]
            if service not in best or row["ji"] > best[service]["score"]:
                best[service] = {"score": row["ji"], "operation": op, "a": row["a"], "n": row["n"]}
    for service, row in best.items():
        row["rank_min"] = 1 + sum(other["score"] > row["score"] for other in best.values())
        row["rank_max"] = sum(other["score"] >= row["score"] for other in best.values())
    return best


def margin(a, b):
    return None if abs(a) + abs(b) == 0 else (a - b) / (abs(a) + abs(b))


def one_case(directory, row, table_columns):
    capture = directory / "capture"
    adapter = read(capture / "calls/001-adapter.json")
    meta = adapter["entry"]["input"]
    columns = table_columns(capture, meta)
    spans = pd.DataFrame(columns)
    t_us = int(adapter["entry"]["t_seconds"]) * 1_000_000
    spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
    spans["operation"] = spans["serviceName"] + "_" + spans["methodName"]
    native_ji = decode_ji(adapter["locals"]["ji"])
    rebuilt, H, n_normal, n_after = native_formula(spans, t_us, "duration")
    sham_ok = set(rebuilt) == set(native_ji) and all(same_float(rebuilt[op]["ji"], native_ji[op]) for op in rebuilt)
    identity_ok = all(not r["a"] or abs(r["ji"] - 2 * r["a"] / (r["n"] + H)) <= 1e-12 * max(1.0, abs(r["ji"]))
                      for r in rebuilt.values())
    integer = spans[["traceID", "spanID", "parentSpanID", "startTime", "duration"]].copy()
    u, covered, children, resolved = uncovered(integer)
    spans["u"] = pd.array(u, dtype="Int64")
    changed, H_u, _n0, _n1 = native_formula(spans, t_us, "u")
    service_of = dict(zip(spans["operation"], spans["serviceName"]))
    after_mask = (spans["startTime"] + spans["duration"] >= t_us).to_numpy(dtype=bool)
    # Quan hệ gọi mức service từ cặp cha-con khác service, không dùng nhãn.
    key = spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)
    service_by_key = pd.Series(spans["serviceName"].to_numpy(), index=key.to_numpy())
    service_by_key = service_by_key[~service_by_key.index.duplicated(keep=False)]
    parent_service = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(service_by_key)
    cross = pd.DataFrame({"caller": parent_service.to_numpy(), "callee": spans["serviceName"].to_numpy()}).dropna()
    cross = cross[cross["caller"] != cross["callee"]]
    edges = sorted({(str(a), str(b)) for a, b in zip(cross["caller"], cross["callee"])})
    native_rank = entity_ranking(rebuilt, service_of)
    changed_rank = entity_ranking(changed, service_of)
    operations = {op: {"service": service_of[op], **rebuilt[op], "a_u": changed[op]["a"], "ji_u": changed[op]["ji"],
                       "mean_u_ms": changed[op]["mean_ms"], "std_u_ms": changed[op]["std_ms"]} for op in rebuilt}
    # Từ đây mới nối nhãn.
    root = row["root"]
    callers_of_root = sorted({a for a, b in edges if b == root})
    callees_of_root = sorted({b for a, b in edges if a == root})

    def view(rank):
        if root not in rank:
            return {"root_ranked": False, "n_entities": len(rank)}
        root_row = rank[root]
        above = sorted((e for e, r in rank.items() if r["rank_max"] < root_row["rank_min"]), key=lambda e: rank[e]["rank_min"])
        return {"root_ranked": True, "n_entities": len(rank), "root": root_row,
                "above_root": [{"entity": e, "relation": "caller_of_root" if e in callers_of_root else
                                "callee_of_root" if e in callees_of_root else "other", **rank[e],
                                "margin_vs_root": margin(rank[e]["score"], root_row["score"])} for e in above],
                "callers_above": [e for e in above if e in callers_of_root]}

    native_view, changed_view = view(native_rank), view(changed_rank)
    result = {
        "dataset": row["dataset"], "opaque_id": row["opaque_id"], "status": "OK", "root": root, "fault": row["fault"],
        "cell": row["cell"], "t028": row["t028"], "sham_ji_bit_exact": bool(sham_ok), "identity_2a_over_n_plus_H": bool(identity_ok),
        "counts": {"spans": int(len(spans)), "spans_before": int(n_normal), "spans_after": int(n_after),
                   "H_native": H, "H_u": H_u, "operations_after": len(rebuilt),
                   "spans_parent_resolved": int(resolved.sum()), "spans_with_children": int((children > 0).sum()),
                   "after_spans_with_children": int(((children > 0) & after_mask).sum()),
                   "covered_share_of_total_duration": float(covered.sum() / max(1, int(spans["duration"].sum())))},
        "callers_of_root": callers_of_root, "callees_of_root": callees_of_root, "service_edges": len(edges),
        "native": native_view, "t_d": changed_view, "operations": operations,
    }
    if native_view["root_ranked"]:
        t028 = row["t028"]
        result["self_check_native_rank_equals_t028"] = (t028["status"] == "OK"
            and [native_view["root"]["rank_min"], native_view["root"]["rank_max"]] == [t028["rank_min"], t028["rank_max"]])
    if native_view["root_ranked"] and changed_view["root_ranked"]:
        before, after = native_view["root"]["rank_min"], changed_view["root"]["rank_min"]
        result["td_effect_on_root"] = "tăng hạng" if after < before else "giảm hạng" if after > before else "không đổi"
        result["callers_no_longer_above"] = sorted(set(native_view["callers_above"]) - set(changed_view["callers_above"]))
        result["callers_newly_above"] = sorted(set(changed_view["callers_above"]) - set(native_view["callers_above"]))
        pairs = {}
        for item in native_view["above_root"]:
            e = item["entity"]
            new = changed_rank.get(e)
            new_margin = None if new is None else margin(new["score"], changed_view["root"]["score"])
            pairs[e] = {"relation": item["relation"], "margin_native": item["margin_vs_root"], "margin_t_d": new_margin,
                        "delta": None if new_margin is None or item["margin_vs_root"] is None else item["margin_vs_root"] - new_margin,
                        "still_above": new is not None and new["rank_max"] < changed_view["root"]["rank_min"]}
        result["pairs_above_root_native"] = pairs
    return result


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    fixtures = interval_fixtures()
    (out / "interval-fixtures.json").write_text(json.dumps(fixtures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not fixtures["pass"]:
        print(json.dumps(fixtures, ensure_ascii=False))
        return 1
    from replay_tracerca_v3 import table_columns
    labels = {}
    for item in read(LABELS)["main_rows"]:
        if item["method"] == "tracerca":
            flags = {k: (((item.get("mechanisms") or {}).get(k) or {}).get("assignment") or {}).get("multi") for k in ("1", "5")}
            labels[(item["dataset"], item["opaque_id"])] = {"root": item["root"], "fault": item["fault"], "cell": item["cell"],
                "t028": {"status": item["status"], "rank_min": item["rank_min"], "rank_max": item["rank_max"], "multi_flags": flags}}
    cases = []
    only = sys.argv[2] if len(sys.argv) > 2 else None  # "dataset:opaque_id" để chạy thử một ca
    for plan_row in read(PLAN)["rows"]:
        dataset, opaque_id = plan_row["dataset"], plan_row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        label = labels.get((dataset, opaque_id))
        reused = plan_row.get("replay_phase_already_valid")
        directory = REUSED.get(reused, COHORT / "cases" / dataset / opaque_id)
        base = {"dataset": dataset, "opaque_id": opaque_id, "source_status": plan_row["source_status"]}
        if plan_row["source_status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "nguồn " + plan_row["source_status"] + ": phương pháp không trả điểm"})
            continue
        check = directory / "check.json"
        if not check.is_file() or read(check).get("status") != "PASS":
            cases.append({**base, "status": "N/A", "reason": "chưa có lượt phát lại khớp tuyệt đối"})
            continue
        if label is None:
            cases.append({**base, "status": "N/A", "reason": "không có dòng nhãn trong T-028"})
            continue
        try:
            item = one_case(directory, {"dataset": dataset, "opaque_id": opaque_id, **label}, table_columns)
        except Exception as error:  # giữ ca lỗi trong mẫu số, không bỏ
            item = {**base, "status": "TOOL_ERROR", "error": type(error).__name__ + ": " + str(error)}
        item["check_sha256"] = sha(check)
        (out / "cases").mkdir(exist_ok=True)
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps(item, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        slim = {k: v for k, v in item.items() if k != "operations"}
        cases.append(slim)
        print(dataset, opaque_id, item.get("status"), item.get("sham_ji_bit_exact"), item.get("td_effect_on_root"), flush=True)
    valid = [c for c in cases if c.get("status") == "OK" and c.get("sham_ji_bit_exact") and "td_effect_on_root" in c]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        return {"n": len(rows),
                "td_effect_on_root": {k: count(lambda c, k=k: c["td_effect_on_root"] == k) for k in ("tăng hạng", "không đổi", "giảm hạng")},
                "hit1": {"native": count(lambda c: c["native"]["root"]["rank_max"] == 1), "t_d": count(lambda c: c["t_d"]["root"]["rank_max"] == 1)},
                "hit5": {"native": count(lambda c: c["native"]["root"]["rank_max"] <= 5), "t_d": count(lambda c: c["t_d"]["root"]["rank_max"] <= 5)},
                "cases_with_caller_above_root": {"native": count(lambda c: c["native"]["callers_above"]), "t_d": count(lambda c: c["t_d"]["callers_above"])},
                "cases_caller_leaves_above_root": count(lambda c: c["callers_no_longer_above"]),
                "cases_caller_enters_above_root": count(lambda c: c["callers_newly_above"]),
                "native_wrong_at_1": {"n": count(lambda c: c["native"]["root"]["rank_max"] > 1),
                                      "becomes_hit1": count(lambda c: c["native"]["root"]["rank_max"] > 1 and c["t_d"]["root"]["rank_max"] == 1)},
                "native_hit_at_1": {"n": count(lambda c: c["native"]["root"]["rank_max"] == 1),
                                    "loses_hit1": count(lambda c: c["native"]["root"]["rank_max"] == 1 and c["t_d"]["root"]["rank_max"] > 1)}}

    summary = {"n_plan": len(cases),
               "status_counts": {s: sum(c.get("status") == s for c in cases) for s in ("OK", "N/A", "TOOL_ERROR")},
               "sham_bit_exact": sum(bool(c.get("sham_ji_bit_exact")) for c in cases),
               "identity_holds": sum(bool(c.get("identity_2a_over_n_plus_H")) for c in cases),
               "self_check_native_rank_equals_t028": sum(bool(c.get("self_check_native_rank_equals_t028")) for c in cases),
               "root_unranked": {"native": sum(c.get("status") == "OK" and not c["native"]["root_ranked"] for c in cases),
                                 "t_d": sum(c.get("status") == "OK" and not c["t_d"]["root_ranked"] for c in cases)},
               "all": tally(valid),
               "by_dataset": {d: tally([c for c in valid if c["dataset"] == d]) for d in ("RE2-TT", "Nezha-OB")},
               "note": "Mẫu số n là số ca OK có sham khớp từng bit và root được xếp ở cả hai nhánh. Hit tính bi quan theo hòa. "
                       "T-D là phép đổi chẩn đoán trên dev, không phải phương pháp mới và không thay số P3."}
    result = {"schema": "T032-tracerca-core-td-v1", "design": "results/T-032/thiet-ke-phep-doi-001.md#5",
              "interval_fixtures": fixtures, "summary": summary, "cases": cases, "methods_executed": False}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

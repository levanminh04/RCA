"""T-032 bản 013 mục 4: bảng nối theo cây span cho nhánh ghép của MicroRank (mo15c1, mo1p50c1). Chạy trên EC2, chỉ đọc.

Không gọi phương pháp. Thứ hạng và thao tác cao nhất lấy từ bản ghi của lượt laptop runs/microrank-kt3-001 (file rút gọn, kiểm hash).
Hai tập trace của nhánh ghép được dựng lại từ bảng span đã lưu bằng đúng đoạn mã của hàm móc trong laptop_contrast_v7.py
(hàm partition dưới đây chép nguyên phần tính; hai luật gọi nguyên hàm của src/microrank/detectors.py).
Tự kiểm theo ca và luật: các số của tập trace dựng lại phải trùng số lưu ở check.json của lượt laptop; lệch thì ca đó không dùng.
Mọi thao tác và dịch vụ được tính trước; nhãn root nối sau cùng.
Dùng: python microrank_merged_link_v1.py <thư mục lượt mới> <file kt3-rankings.json> [dataset:opaque_id]
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402
import chain_position_v1 as cp  # noqa: E402
import chain_spanpass_v1 as csp  # noqa: E402 — subtree, depth_of và 13 trường hợp tự dựng
from fake_marker_v1 import flags_microrank  # noqa: E402

COLS = ['traceID', 'spanID', 'parentSpanID', 'serviceName', 'methodName', 'operationName', 'startTime', 'duration']
ONE_SECOND_US = 1_000_000
MIN_CALLS = 20
RULE_OF = {"mo15c1": "mo15", "mo1p50c1": "mo1p50"}
CHECK_KEYS = ("traces_after", "traces_after_with_root", "baseline_traces", "baseline_traces_used", "slo_operations", "new_traces", "new_abnormal",
              "new_normal", "new_abnormal_also_native_abnormal", "native_traces", "native_abnormal", "new_abnormal_traces_by_service")
UP = ("goi_truc_tiep", "phia_tren_gian_tiep", "hai_chieu")
MIN_F = 5


def partition(df, t_us, all_traces, abnormal, branch):
    """Chép nguyên phần tính của hàm hook trong laptop_contrast_v7.py (patch_microrank_partition), nhánh mo15 / mo1p50."""
    from microrank import detectors
    call = {"rows": int(len(df)), "native_traces": len(all_traces), "native_abnormal": len(abnormal)}
    tid = df.traceID.astype(str).to_numpy()
    par = df.parentSpanID
    declared = (par.isna() | par.astype("string").fillna("").isin(["", "root"])).to_numpy(dtype=bool)
    ident = (df.traceID.astype(str) + "|" + df.spanID.astype(str)).to_numpy()
    position = pd.Series(np.arange(len(df)), index=ident)
    position = position[~position.index.duplicated(keep=False)]
    parent = (df.traceID.astype(str) + "|" + par.astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent) & ~declared
    p = np.where(has_parent, parent, 0).astype("int64")
    orphan = ~declared & ~has_parent
    duration = df.duration.to_numpy(dtype="int64")
    after_span = (df.startTime.to_numpy(dtype="int64") + duration) >= t_us
    child_sum = np.zeros(len(df), dtype="int64")
    np.add.at(child_sum, p[has_parent], duration[has_parent])
    handling = duration - child_sum
    tcode, tuniq = pd.factorize(tid)
    frame = pd.DataFrame({"t": tcode, "after": after_span, "declared": declared, "orphan": orphan, "dur": duration, "handling": handling})
    g = frame.groupby("t", sort=True).agg(n=("after", "size"), n_after=("after", "sum"), roots=("declared", "sum"), orphans=("orphan", "sum"))
    roots = frame[frame["declared"]].groupby("t", sort=True).agg(root_dur=("dur", "sum"), root_handling_max=("handling", "max"))
    g = g.join(roots)
    if not np.array_equal(g.index.to_numpy(), np.arange(len(tuniq))):
        raise RuntimeError("chỉ số trace không liên tục")
    is_after = (g["n_after"] > 0).to_numpy()
    has_root = (g["roots"] >= 1).to_numpy()
    base_ok = (~is_after) & has_root & (g["orphans"] == 0).to_numpy() & ~(g["root_handling_max"] > ONE_SECOND_US).to_numpy()
    op = df.operation.to_numpy()
    mask = base_ok[tcode]
    slo = {}
    for name, values in pd.Series(handling[mask]).groupby(op[mask], sort=True):
        x = values.to_numpy(dtype="float64")
        slo[name] = [round(float(np.mean(x)) / 1000.0, 4), round(float(np.std(x)) / 1000.0, 4)]
    keep = is_after & has_root
    if set(tuniq[is_after]) != set(all_traces):
        raise RuntimeError("tập trace sau mốc tính lại khác tập của hàm native")
    sel = keep[tcode]
    counts = pd.DataFrame({"t": tcode[sel], "o": op[sel]}).groupby(["t", "o"], sort=True).size()
    root_dur = g["root_dur"].to_numpy()
    operation_counts = {}
    for (t, o), c in counts.items():
        operation_counts.setdefault(tuniq[t], {"duration": float(root_dur[t])})[o] = int(c)
    call.update({"traces_after": int(is_after.sum()), "traces_after_with_root": int(keep.sum()),
                 "baseline_traces": int((~is_after).sum()), "baseline_traces_used": int(base_ok.sum()), "slo_operations": len(slo)})
    if branch == "mo15":
        new_abnormal = set(detectors.original_system_alarm(operation_counts, slo)["abnormal_trace_ids"])
    else:
        new_abnormal = set(detectors.original_trace_partition(operation_counts, slo)[0])
    new_all = set(operation_counts)
    svc = df.serviceName.astype(str).to_numpy()

    def by_service(trace_set):
        code_in = np.isin(tuniq, list(trace_set)) if trace_set else np.zeros(len(tuniq), dtype=bool)
        m = code_in[tcode] & after_span
        if not m.any():
            return {}
        return {k: int(v) for k, v in pd.DataFrame({"t": tcode[m], "s": svc[m]}).drop_duplicates().groupby("s").size().items()}

    call.update({"new_traces": len(new_all), "new_abnormal": len(new_abnormal), "new_normal": len(new_all - new_abnormal),
                 "new_abnormal_also_native_abnormal": len(new_abnormal & abnormal),
                 "native_abnormal_traces_by_service": by_service(abnormal), "new_abnormal_traces_by_service": by_service(new_abnormal)})
    return new_all, new_abnormal, call


def direct_fixture():
    """A(0) gọi B(1) gọi C(2): span A.client có con trực tiếp thuộc B, không có con trực tiếp thuộc C."""
    svc = np.array([0, 0, 1, 1, 2])
    parent = np.array([-1, 0, 1, 2, 3])
    has_parent = parent >= 0
    p = np.where(has_parent, parent, 0)
    bit = np.uint64(1) << svc.astype("uint64")
    cross = has_parent & (svc[p] != svc)
    direct = np.zeros(5, dtype="uint64")
    np.bitwise_or.at(direct, p[cross], bit[cross])
    has = lambda i, x: bool((int(direct[i]) >> x) & 1)   # noqa: E731
    checks = {"span 1 (A phía gọi) có con trực tiếp thuộc B": has(1, 1), "span 1 không có con trực tiếp thuộc C": not has(1, 2),
              "span 3 (B phía gọi) có con trực tiếp thuộc C": has(3, 2), "span 0 (A, con cùng dịch vụ) không có lời gọi trực tiếp": int(direct[0]) == 0}
    checks = {k: bool(v) for k, v in checks.items()}
    return {"pass": all(checks.values()), "checks": checks}


def prepare(spans, t_us):
    """Bảng span theo đúng thứ tự và cột mà hàm microrank dùng; cây span và các mặt nạ như chain_spanpass_v1.one_case."""
    df = spans[COLS].copy()
    df["methodName"] = df.methodName.fillna(df.operationName)
    df["operation"] = df.serviceName + "_" + df.methodName
    df = df.sort_values(["traceID", "startTime", "spanID"], kind="mergesort").reset_index(drop=True)
    start = df["startTime"].to_numpy(dtype="int64")
    duration = df["duration"].to_numpy(dtype="int64")
    end = start + duration
    after = end >= t_us
    service = df["serviceName"].astype(str).to_numpy()
    operation = df["operation"].to_numpy()
    services = sorted(set(service))
    if len(services) > 63:
        raise RuntimeError("hơn 63 dịch vụ")
    sid = pd.Series(np.arange(len(services)), index=services)
    own_bit = np.uint64(1) << sid.loc[service].to_numpy().astype("uint64")
    ident = (df["traceID"].astype(str) + "|" + df["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(df)), index=ident)
    position = position[~position.index.duplicated(keep=False)]
    parent = (df["traceID"].astype(str) + "|" + df["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent)
    p = np.where(has_parent, parent, 0).astype("int64")
    cross = has_parent & (service[p] != service)
    flag, ok = flags_microrank(duration, operation, ~after, after)
    stats = pd.DataFrame({"o": operation[~after], "d": duration[~after]}).groupby("o", sort=True)["d"].mean()
    mean_us = pd.Series(operation).map(stats.map(lambda v: round(float(v) / 1_000, 2) * 1000.0)).to_numpy(dtype="float64")
    span_excess = duration - mean_us
    c_index, p_index = np.flatnonzero(cross), p[cross]
    calls = pd.DataFrame({"caller": service[p_index], "callee": service[c_index], "d_p": duration[p_index], "p": p_index, "after": end[p_index] >= t_us})
    slow_to = np.zeros(len(df), dtype="uint64")
    exc_to = np.zeros((len(df), len(services)), dtype="float64")
    measurable, edges = set(), set()
    for (a, b), g in calls.groupby(["caller", "callee"], sort=True):
        edges.add((a, b))
        bf, af = g[~g["after"]], g[g["after"]]
        if len(bf) >= MIN_CALLS and len(af) >= MIN_CALLS:
            threshold = float(np.percentile(bf["d_p"].to_numpy(), 95))
            median_before = float(np.median(bf["d_p"].to_numpy()))
            slow = af[af["d_p"] > threshold]
            x = int(sid[b])
            rows = slow["p"].to_numpy()
            slow_to[rows] |= np.uint64(1) << np.uint64(x)
            np.maximum.at(exc_to[:, x], rows, slow["d_p"].to_numpy(dtype="float64") - median_before)
            measurable.add(b)
    svc_below, slow_sub, flag_below, exc_sub, maxdepth = csp.subtree(has_parent, p, own_bit, slow_to, flag, exc_to)
    direct = np.zeros(len(df), dtype="uint64")
    np.bitwise_or.at(direct, p[cross], own_bit[cross])
    return {"df": df, "after": after, "service": service, "operation": operation, "services": services, "sid": sid, "own_bit": own_bit,
            "has_parent": has_parent, "flag": flag, "ok": ok, "span_excess": span_excess, "svc_below": svc_below, "slow_sub": slow_sub,
            "flag_below": flag_below, "exc_sub": exc_sub, "direct": direct, "measurable": measurable, "edges": edges, "trace": df["traceID"].astype(str).to_numpy(),
            "max_depth": maxdepth}


def bit_of(mask, x):
    return ((mask >> np.uint64(x)) & np.uint64(1)).astype(bool)


def shares(P, idx, x):
    """Các tỷ lệ của tập span idx đối với dịch vụ có chỉ số x."""
    n = len(idx)
    if n == 0:
        return {"n": 0}
    slow, fb = bit_of(P["slow_sub"][idx], x), bit_of(P["flag_below"][idx], x)
    with np.errstate(invalid="ignore", divide="ignore"):
        ratio = np.where(P["span_excess"][idx] > 0, P["exc_sub"][idx, x] / P["span_excess"][idx], np.nan)
    return {"n": n, "direct": float(bit_of(P["direct"][idx], x).mean()), "below": float(bit_of(P["svc_below"][idx], x).mean()),
            "slow": float(slow.mean()), "flag_below": float(fb.mean()), "linked": float((slow | fb).mean()),
            "r50": float((slow & (ratio >= 0.5)).mean())}


def link_entity(P, new_abnormal, entity, operation, root):
    in_new = np.isin(P["trace"], list(new_abnormal)) if new_abnormal else np.zeros(len(P["trace"]), dtype=bool)
    is_op = P["operation"] == operation
    F = np.flatnonzero(P["after"] & P["flag"] & is_op & in_new)
    NF = np.flatnonzero(P["after"] & P["ok"] & ~P["flag"] & is_op)
    Fall = np.flatnonzero(P["after"] & P["flag"] & is_op)
    res = {"entity": entity, "operation": operation, "F": int(len(F)), "flagged_spans_all_traces": int(len(Fall)), "nonflagged_spans_after": int(len(NF)),
           "F_without_parent_share": float((~P["has_parent"][F]).mean()) if len(F) else None,
           "own_count_traces": int(len(set(P["trace"][F].tolist())))}
    if root in P["sid"].index:
        x = int(P["sid"][root])
        res["root"] = {"on_F": shares(P, F, x), "on_nonflagged": shares(P, NF, x), "edge_measurable": root in P["measurable"]}
        # mức trace
        own_traces = set(P["trace"][F].tolist())
        after_idx = np.flatnonzero(P["after"])
        tr = pd.DataFrame({"t": P["trace"][after_idx], "is_root": P["service"][after_idx] == root, "root_flag": (P["service"][after_idx] == root) & P["flag"][after_idx]})
        tr = tr[tr["t"].isin(own_traces)].groupby("t").agg(has_root=("is_root", "max"), root_flag=("root_flag", "max"))
        res["trace_level"] = {"own_traces": len(own_traces), "has_root": int(tr["has_root"].sum()) if len(tr) else 0,
                              "root_flagged": int(tr["root_flag"].sum()) if len(tr) else 0}
    else:
        res["root"] = None
    g = cp.Graph(P["services"], list(P["edges"]))
    others = {}
    for y in P["services"]:
        if y in (root, entity):
            continue
        if root in P["sid"].index and g.position(y, root)["class"] in UP:
            continue
        s = shares(P, F, int(P["sid"][y]))
        if s["n"]:
            others[y] = {"linked": s["linked"], "slow": s["slow"], "flag_below": s["flag_below"], "below": s["below"]}
    best = max(others, key=lambda y: others[y]["linked"], default=None)
    res["best_other"] = None if best is None else {"service": best, **others[best]}
    res["best_other_flag_below"] = max((v["flag_below"] for v in others.values()), default=None)
    if root != entity and root in P["sid"].index:
        res.update({k: v for k, v in g.position(entity, root).items()})
    return res


def classify(link):
    r = link.get("root")
    if not r or link["F"] < MIN_F:
        return "ít span (F < 5)" if r else "root không có span"
    key = "linked" if r["edge_measurable"] else "flag_below"
    value = r["on_F"][key]
    other = (link["best_other"] or {}).get("linked", 0.0) if key == "linked" else (link.get("best_other_flag_below") or 0.0)
    tag = "" if r["edge_measurable"] else " (cạnh tới root không đủ lời gọi; chỉ dùng flag_below)"
    if value >= 0.5 and value > other:
        return "gắn với root" + tag
    if value < 0.2:
        return "không gắn" + tag
    return "không rõ" + tag


def main():
    out, rankings_path = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    only = sys.argv[3] if len(sys.argv) > 3 else None
    fx, fx2 = csp.fixtures(), direct_fixture()
    if not (fx["pass"] and fx2["pass"]):
        raise SystemExit("trường hợp tự dựng không đạt")
    from replay_tracerca_v3 import table_columns
    rankings = {(c["dataset"], c["opaque_id"]): c for c in td.read(rankings_path)["cases"]}
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "microrank_full"}
    cases = []
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        key = (dataset, opaque_id)
        label, rk = labels[key], rankings[key]
        base = {"dataset": dataset, "opaque_id": opaque_id, "root": label["root"], "fault": label["fault"], "cell": label["cell"]}
        if row["source_status"] != "OK" or not all(rk["branches"].get(b, {}).get("status") == "OK" for b in RULE_OF):
            cases.append({**base, "status": "N/A", "reason": "nguồn TraceRCA " + row["source_status"] + "; trạng thái nhánh ghép: " +
                          ", ".join(b + "=" + str(rk["branches"].get(b, {}).get("status")) for b in RULE_OF)})
            continue
        began = time.time()
        directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
        adapter = td.read(directory / "capture/calls/001-adapter.json")
        spans = pd.DataFrame(table_columns(directory / "capture", adapter["entry"]["input"]))
        t_us = int(adapter["entry"]["t_seconds"]) * 1_000_000
        item = {**base, "status": "OK", "branches": {}}
        try:
            P = prepare(spans, t_us)
            df, after = P["df"], P["after"]
            all_traces = set(P["trace"][after].tolist())
            native_abnormal = set(P["trace"][after & P["flag"]].tolist())
            for branch, rule in RULE_OF.items():
                b = rk["branches"][branch]
                new_all, new_abnormal, call = partition(df, t_us, all_traces, native_abnormal, rule)
                ref = b["partition_call"]
                check = {k: call.get(k) == ref.get(k) for k in CHECK_KEYS}
                cc = [c for c in b["count_calls"] if c.get("is_anomaly")]
                in_new = np.isin(P["trace"], list(new_abnormal)) if new_abnormal else np.zeros(len(df), dtype=bool)
                flagged = after & P["flag"] & in_new
                own = pd.DataFrame({"o": P["operation"][flagged], "t": P["trace"][flagged]}).drop_duplicates().groupby("o").size()
                if len(cc) == 1 and cc[0].get("mode") == "đếm riêng":
                    check["group_traces_with_flagged_span"] = int(len(set(P["trace"][flagged].tolist()))) == cc[0]["group_traces_with_flagged_span"]
                    check["sum_own"] = int(own.sum()) == cc[0]["sum_own"]
                bi = {"self_check": check, "self_check_pass": all(check.values()), "new_traces": call["new_traces"], "new_abnormal": call["new_abnormal"],
                      "abnormal_traces_without_flagged_span": call["new_abnormal"] - int(len(set(P["trace"][flagged].tolist())))}
                item["branches"][branch] = bi
                if not bi["self_check_pass"]:
                    continue
                # thứ hạng của nhánh (từ laptop); chưa dùng nhãn tới đây
                groups, order = {}, []
                for entity, tie in b["entity_ranking"]:
                    if tie not in groups:
                        order.append(tie)
                    groups.setdefault(tie, []).append(entity)
                rank, offset = {}, 0
                for tie in order:
                    for entity in groups[tie]:
                        rank[entity] = (offset + 1, offset + len(groups[tie]))
                    offset += len(groups[tie])
                item_of = {}
                for op, entity, _key in b["ranking"]:
                    item_of.setdefault(entity, op)
                # --- từ đây nối nhãn ---
                root = label["root"]
                bi.update({"root_ranked": root in rank, "n_entities": len(rank)})
                if root not in rank:
                    continue
                bi.update({"root_rank_min": rank[root][0], "root_rank_max": rank[root][1], "root_operation": item_of.get(root),
                           "root_own_count_traces": int(own.get(item_of.get(root), 0))})
                bi["root_wrong"] = rank[root][1] > 1
                tops = sorted(e for e in rank if rank[e][0] == 1 and e != root)
                bi["top_entities"] = tops
                if bi["root_wrong"]:
                    bi["links"] = []
                    for e in tops:
                        link = link_entity(P, new_abnormal, e, item_of[e], root)
                        link["reading"] = classify(link)
                        bi["links"].append(link)
        except Exception as error:  # giữ lượt hỏng
            item.update(status="TOOL_ERROR", error=type(error).__name__ + ": " + str(error)[:300])
        item["wall_s"] = round(time.time() - began, 1)
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps(item, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        cases.append(item)
        print(dataset, opaque_id, item["status"], {b: (v["self_check_pass"], v.get("root_rank_max"), [(l["entity"], l["F"], l["reading"]) for l in v.get("links", [])])
                                                   for b, v in item.get("branches", {}).items()}, item["wall_s"], flush=True)

    summary = {"n_cases": len(cases), "status": dict(Counter(c["status"] for c in cases)), "self_check": {}, "by_dataset": {}}
    for branch in RULE_OF:
        rows = [c for c in cases if c["status"] == "OK" and branch in c["branches"]]
        summary["self_check"][branch] = {"cases": len(rows), "pass": sum(c["branches"][branch]["self_check_pass"] for c in rows),
                                         "fail": [c["opaque_id"] for c in rows if not c["branches"][branch]["self_check_pass"]]}
    for dataset in ("RE2-TT", "Nezha-OB"):
        summary["by_dataset"][dataset] = {}
        for branch in RULE_OF:
            rows = [c for c in cases if c["dataset"] == dataset and c["status"] == "OK" and c["branches"].get(branch, {}).get("self_check_pass")
                    and c["branches"][branch].get("root_ranked")]
            wrong = [c for c in rows if c["branches"][branch]["root_wrong"]]
            links = [(c, l) for c in wrong for l in c["branches"][branch]["links"]]
            block = {"cases_usable": len(rows), "root_rank1": len(rows) - len(wrong), "root_not_rank1": len(wrong),
                     "top_entity": dict(Counter(l["entity"] for _c, l in links)), "reading_all": dict(Counter(l["reading"] for _c, l in links)),
                     "by_top_entity": {}}
            for e in sorted({l["entity"] for _c, l in links}):
                es = [(c, l) for c, l in links if l["entity"] == e]
                with_root = [l for _c, l in es if l.get("root") and l["F"] >= MIN_F]
                block["by_top_entity"][e] = {
                    "cases": len(es), "reading": dict(Counter(l["reading"] for _c, l in es)), "operations": dict(Counter(l["operation"] for _c, l in es)),
                    "class_vs_root": dict(Counter(str(l.get("class")) for _c, l in es)),
                    "median_on_F": {k: float(np.median([l["root"]["on_F"][k] for l in with_root])) if with_root else None for k in ("direct", "below", "slow", "flag_below", "linked", "r50")},
                    "median_on_nonflagged": {k: float(np.median([l["root"]["on_nonflagged"][k] for l in with_root if l["root"]["on_nonflagged"]["n"]])) if with_root else None
                                             for k in ("direct", "below", "slow", "flag_below", "linked")},
                    "median_best_other_linked": float(np.median([(l["best_other"] or {}).get("linked", 0.0) for l in with_root])) if with_root else None,
                    "case_list": [{"opaque_id": c["opaque_id"], "cell": c["cell"], "root_rank": [c["branches"][branch]["root_rank_min"], c["branches"][branch]["root_rank_max"]],
                                   "operation": l["operation"], "F": l["F"], "reading": l["reading"],
                                   "on_F": (l["root"] or {}).get("on_F"), "edge_measurable": (l["root"] or {}).get("edge_measurable"),
                                   "best_other": l["best_other"], "trace_level": l.get("trace_level")} for c, l in es]}
            summary["by_dataset"][dataset][branch] = block
    # dự đoán khai trước: các ca Nezha-OB còn sai có frontend đứng đầu
    pred = {}
    for branch in RULE_OF:
        b = summary["by_dataset"]["Nezha-OB"][branch]["by_top_entity"].get("frontend", {"cases": 0, "reading": {}})
        n = b["cases"]
        attached = sum(v for k, v in b["reading"].items() if k.startswith("gắn với root"))
        pred[branch] = {"cases_frontend_top": n, "attached": attached, "not_attached": sum(v for k, v in b["reading"].items() if k.startswith("không gắn")),
                        "unclear_or_few": n - attached - sum(v for k, v in b["reading"].items() if k.startswith("không gắn")),
                        "reading": None if not n else "cùng cơ chế H4, H7" if attached >= 2 * n / 3 else "cơ chế khác, chưa giải thích" if attached <= n / 3 else "không phân xử rõ"}
    summary["prediction_nezha_frontend"] = pred
    result = {"schema": "T032-microrank-merged-link-v1", "design": "results/T-032/thiet-ke-phep-doi-013.md mục 4",
              "fixtures": {"subtree": fx, "direct": fx2}, "min_calls": MIN_CALLS, "min_F": MIN_F,
              "sources": {"rankings_sha256": td.sha(rankings_path), "plan_sha256": td.sha(td.PLAN), "labels_sha256": td.sha(td.LABELS)},
              "note": "Mô tả trên dev cho một nhánh chẩn đoán; không là nhãn lan; các cột chồng lấn, không cộng thành tỷ lệ nguyên nhân.",
              "methods_executed": [], "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("status", "self_check", "prediction_nezha_frontend")}, ensure_ascii=False, indent=1), flush=True)
    for dataset, blocks in summary["by_dataset"].items():
        for branch, b in blocks.items():
            print(dataset, branch, {k: b[k] for k in ("cases_usable", "root_rank1", "root_not_rank1", "top_entity", "reading_all")}, flush=True)
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())

"""T-032 bản 008 mục 2: một lượt đọc bảng span cho 52 ca, CHƯA dùng nhãn. Chạy trên EC2, chỉ đọc.

Mỗi ca lưu: đồ thị gọi giữa dịch vụ; lời gọi chậm theo cạnh (như bảng C2); với mỗi thao tác O và dịch vụ X, số span mang cờ
của O có X / lời gọi chậm tới X / span mang cờ của X nằm dưới trong cây span; và bảng theo trace cho MicroRank.
Không gọi phương pháp, không chấm Hit. Nhãn root và thứ hạng nối ở script khác.
Dùng: python chain_spanpass_v1.py <thư mục lượt mới> [dataset:opaque_id để chạy thử một ca]
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402
import root_signal_location_v1 as rsl  # noqa: E402 — dùng nguyên hàm baseline_flags đã khớp H_native 48/48

MIN_CALLS = 20


def depth_of(has_parent, p):
    depth = np.zeros(len(p), dtype="int32")
    for _ in range(500):
        new = np.where(has_parent, depth[p] + 1, 0).astype("int32")
        if np.array_equal(new, depth):
            return depth
        depth = new
    raise RuntimeError("cây span không hội tụ sau 500 vòng (có vòng cha–con?)")


def subtree(has_parent, p, own_bit, slow_to, flag, exc_to):
    """Truyền từ con lên cha, mỗi span đúng một lần theo độ sâu giảm dần.

    Trả: svc_below (bit dịch vụ của mọi span nằm dưới, không gồm chính nó), slow_sub (bit X có lời gọi chậm tới X ở chính span
    hoặc dưới nó), flag_below (bit dịch vụ có span mang cờ nằm dưới), exc_sub (tổng phần vượt của lời gọi chậm tới X ở đó).
    """
    depth = depth_of(has_parent, p)
    svc_below = np.zeros(len(p), dtype="uint64")
    slow_sub = slow_to.copy()
    flag_below = np.zeros(len(p), dtype="uint64")
    exc_sub = exc_to.copy()
    order = np.argsort(-depth, kind="stable")
    bounds = np.flatnonzero(np.diff(depth[order])) + 1
    for idx in np.split(order, bounds):
        if depth[idx[0]] == 0:
            continue
        pr = p[idx]
        np.bitwise_or.at(svc_below, pr, svc_below[idx] | own_bit[idx])
        np.bitwise_or.at(slow_sub, pr, slow_sub[idx])
        np.bitwise_or.at(flag_below, pr, flag_below[idx] | np.where(flag[idx], own_bit[idx], np.uint64(0)))
        np.add.at(exc_sub, pr, exc_sub[idx])
    return svc_below, slow_sub, flag_below, exc_sub, int(depth.max())


def fixtures():
    """Trường hợp tự dựng: A gọi B gọi C (chậm ở B→C), A còn một nhánh song song tới D; một span E mất cha; span 6 tự mang lời gọi chậm."""
    #  i: 0=A(root) 1=A.client→B 2=B.server 3=B.client→C 4=C.server 5=A.client→D 6=D.server 7=E(mất cha) 8=A.client2→C 9=C.server
    svc = np.array([0, 0, 1, 1, 2, 0, 3, 4, 0, 2])
    parent = np.array([-1, 0, 1, 2, 3, 0, 5, -1, 0, 8])
    has_parent = parent >= 0
    p = np.where(has_parent, parent, 0)
    bit = (np.uint64(1) << svc.astype("uint64"))
    slow_to = np.zeros(10, dtype="uint64")
    exc_to = np.zeros((10, 5))
    slow_to[3] = np.uint64(1) << np.uint64(2); exc_to[3, 2] = 100.0   # B→C chậm, phần vượt 100
    slow_to[8] = np.uint64(1) << np.uint64(2); exc_to[8, 2] = 7.0     # A→C chậm, span 8 tự mang
    flag = np.array([True, True, True, False, True, False, False, True, True, False])
    below, slow_sub, flag_below, exc_sub, maxdepth = subtree(has_parent, p, bit, slow_to, flag, exc_to)
    def has(mask, i, x):
        return bool((int(mask[i]) >> x) & 1)
    checks = {
        "sâu nhất bằng 4": maxdepth == 4,
        "A gốc thấy B, C, D nằm dưới, không thấy E": [has(below, 0, x) for x in range(5)] == [True, True, True, True, False],
        "span B.server thấy C nằm dưới, không thấy D": has(below, 2, 2) and not has(below, 2, 3),
        "lời gọi chậm tới C truyền lên A gốc qua hai đường": has(slow_sub, 0, 2) and exc_sub[0, 2] == 107.0,
        "span 1 (A gọi B) bao lời gọi chậm tới C với phần vượt 100": has(slow_sub, 1, 2) and exc_sub[1, 2] == 100.0,
        "span 8 tự mang lời gọi chậm": has(slow_sub, 8, 2) and exc_sub[8, 2] == 7.0,
        "nhánh D không bao lời gọi chậm tới C": not has(slow_sub, 5, 2) and not has(slow_sub, 6, 2),
        "span mất cha E không truyền cho ai": not has(below, 0, 4) and int(below[7]) == 0,
        "span mang cờ của C nằm dưới span 1, không tính chính span": has(flag_below, 1, 2) and not has(flag_below, 4, 2),
        "span mang cờ của B nằm dưới A gốc": has(flag_below, 0, 1),
        "span phía gọi mang cờ của A (span 1, 8) nằm dưới A gốc nên A gốc có bit A": has(flag_below, 0, 0),
        "span 1 không có span mang cờ của A nằm dưới": not has(flag_below, 1, 0),
        "span 9 không có cờ nên C dưới span 8 không có cờ": not has(flag_below, 8, 2),
    }
    checks = {k: bool(v) for k, v in checks.items()}
    return {"pass": all(checks.values()), "checks": checks}


def one_case(spans, t_us):
    spans = spans.reset_index(drop=True)
    spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
    spans["operation"] = spans["serviceName"].astype(str) + "_" + spans["methodName"].astype(str)
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    end = start + duration
    after = end >= t_us
    before = ~after
    service = spans["serviceName"].astype(str).to_numpy()
    operation = spans["operation"].to_numpy()
    services = sorted(set(service))
    if len(services) > 63:
        raise RuntimeError("hơn 63 dịch vụ, không dùng được mặt nạ 64 bit")
    sid = pd.Series(np.arange(len(services)), index=services)
    svc_id = sid.loc[service].to_numpy().astype("uint64")
    own_bit = np.uint64(1) << svc_id
    # cha theo vị trí dòng; định danh lặp không dùng làm cha (như bảng A, C, C2)
    ident = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(spans)), index=ident)
    position = position[~position.index.duplicated(keep=False)]
    parent = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent)
    p = np.where(has_parent, parent, 0).astype("int64")
    cross = has_parent & (service[p] != service)
    # cờ theo luật TraceRCA (hàm đã khớp H_native) và theo đúng biểu thức của MicroRank-RCAEval sửa đầu vào
    flag, flag_ok = rsl.baseline_flags(spans["duration"], operation, before, after)
    flag = np.asarray(flag, dtype=bool)
    flag_ok = np.asarray(flag_ok, dtype=bool)
    frame = pd.DataFrame({"operation": operation, "duration": spans["duration"]})
    stats = frame[before].groupby("operation", sort=True)["duration"].agg(["mean", "std", "count"])
    mr_mean = (stats["mean"] / 1000).round(2)
    mr_std = (stats["std"] / 1000).round(2)
    m = frame["operation"].map(mr_mean).to_numpy(dtype="float64")
    s = frame["operation"].map(mr_std).to_numpy(dtype="float64")
    with np.errstate(invalid="ignore"):
        flag_mr = after & ((duration / 1000) >= m + 3 * s)
    mean_ms = frame["operation"].map(stats["mean"].map(lambda v: round(float(v) / 1_000, 2) if pd.notna(v) else float("nan"))).to_numpy(dtype="float64")
    span_excess = duration - mean_ms * 1000.0   # µs; NaN khi thao tác không có nền
    # lời gọi và cạnh
    c_index, p_index = np.flatnonzero(cross), p[cross]
    calls = pd.DataFrame({"caller": service[p_index], "callee": service[c_index], "d_p": duration[p_index], "p": p_index,
                          "after": end[p_index] >= t_us})
    edges = {}
    slow_to = np.zeros(len(spans), dtype="uint64")
    exc_to = np.zeros((len(spans), len(services)), dtype="float64")
    for (a, b), g in calls.groupby(["caller", "callee"], sort=True):
        bf, af = g[~g["after"]], g[g["after"]]
        item = {"caller": a, "callee": b, "n_before": int(len(bf)), "n_after": int(len(af))}
        if len(bf) >= MIN_CALLS and len(af) >= MIN_CALLS:
            threshold = float(np.percentile(bf["d_p"].to_numpy(), 95))
            median_before = float(np.median(bf["d_p"].to_numpy()))
            slow = af[af["d_p"] > threshold]
            item.update(threshold_p95_d_p_us=threshold, median_d_p_before_us=median_before, n_slow_after=int(len(slow)),
                        slow_share_after=float(len(slow) / len(af)))
            x = int(sid[b])
            rows = slow["p"].to_numpy()
            slow_to[rows] |= np.uint64(1) << np.uint64(x)
            np.maximum.at(exc_to[:, x], rows, slow["d_p"].to_numpy(dtype="float64") - median_before)
        edges[a + "→" + b] = item
    svc_below, slow_sub, flag_below, exc_sub, maxdepth = subtree(has_parent, p, own_bit, slow_to, flag, exc_to)

    def bit_of(mask, x):
        return ((mask >> np.uint64(x)) & np.uint64(1)).astype(bool)

    # bảng theo thao tác O và dịch vụ X
    F = np.flatnonzero(flag)
    NF = np.flatnonzero(after & flag_ok & ~flag)
    op_table = {}
    for o, n in pd.Series(operation[after & flag_ok]).value_counts().items():
        op_table[o] = {"service": None, "n": int(n), "a": 0, "x": {}}
    for o, a in pd.Series(operation[F]).value_counts().items():
        op_table[o]["a"] = int(a)
    for o, sv in pd.DataFrame({"o": operation, "s": service}).drop_duplicates().itertuples(index=False):
        if o in op_table:
            op_table[o]["service"] = sv
    for x, name in enumerate(services):
        fb, fs, ff = bit_of(svc_below[F], x), bit_of(slow_sub[F], x), bit_of(flag_below[F], x)
        nb, ns = bit_of(svc_below[NF], x), bit_of(slow_sub[NF], x)
        if not (fb.any() or nb.any()):
            continue
        with np.errstate(invalid="ignore", divide="ignore"):
            ratio = np.where(span_excess[F] > 0, exc_sub[F, x] / span_excess[F], np.nan)
        df = pd.DataFrame({"o": operation[F], "below": fb, "slow": fs, "flag_below": ff, "r50": fs & (ratio >= 0.5), "r80": fs & (ratio >= 0.8)})
        agg = df.groupby("o", sort=False).sum()
        med = pd.DataFrame({"o": operation[F][fs], "r": ratio[fs]}).groupby("o", sort=False)["r"].median()
        nagg = pd.DataFrame({"o": operation[NF], "below": nb, "slow": ns}).groupby("o", sort=False).sum()
        for o in set(agg.index[(agg["below"] > 0)]) | set(nagg.index[nagg["below"] > 0]):
            row = {"a_below": 0, "a_slow": 0, "a_flag_below": 0, "a_r50": 0, "a_r80": 0, "nf_below": 0, "nf_slow": 0, "ratio_median": None}
            if o in agg.index:
                row.update(a_below=int(agg.at[o, "below"]), a_slow=int(agg.at[o, "slow"]), a_flag_below=int(agg.at[o, "flag_below"]),
                           a_r50=int(agg.at[o, "r50"]), a_r80=int(agg.at[o, "r80"]))
            if o in med.index and pd.notna(med[o]):
                row["ratio_median"] = float(med[o])
            if o in nagg.index:
                row.update(nf_below=int(nagg.at[o, "below"]), nf_slow=int(nagg.at[o, "slow"]))
            op_table[o]["x"][name] = row
    # bảng theo trace cho MicroRank (chỉ span sau mốc; cờ theo biểu thức MicroRank)
    A = np.flatnonzero(after)
    tcode, tuniq = pd.factorize(spans["traceID"].astype(str).to_numpy()[A])
    nt = len(tuniq)
    t_svc = np.zeros(nt, dtype="uint64"); np.bitwise_or.at(t_svc, tcode, own_bit[A])
    fa = flag_mr[A]
    t_abn = np.zeros(nt, dtype=bool); t_abn[tcode[fa]] = True
    t_own = np.zeros(nt, dtype="uint64"); np.bitwise_or.at(t_own, tcode[fa], own_bit[A][fa])
    t_wait = np.zeros(nt, dtype="uint64"); np.bitwise_or.at(t_wait, tcode[fa], slow_sub[A][fa])
    pairs = pd.DataFrame({"t": tcode, "o": operation[A], "f": fa}).groupby(["t", "o"], sort=False)["f"].max().reset_index()
    pt = pairs["t"].to_numpy()
    pairs["abn"] = t_abn[pt]
    trace_table = {}
    base = pairs.groupby("o", sort=False).agg(A=("abn", "sum"), T=("abn", "size"), own_A=("f", "sum"))
    for o, row in base.iterrows():
        trace_table[o] = {"A": int(row["A"]), "N": int(row["T"] - row["A"]), "own_A": int(row["own_A"]), "x": {}}
    abn_pairs = pairs[pairs["abn"]]
    nor_pairs = pairs[~pairs["abn"]]
    at, ntt = abn_pairs["t"].to_numpy(), nor_pairs["t"].to_numpy()
    for x, name in enumerate(services):
        has, own, wait = bit_of(t_svc[at], x), bit_of(t_own[at], x), bit_of(t_wait[at], x)
        agg = pd.DataFrame({"o": abn_pairs["o"].to_numpy(), "has": has, "own": own, "wait": wait, "linked": own | wait}).groupby("o", sort=False).sum()
        nagg = pd.DataFrame({"o": nor_pairs["o"].to_numpy(), "has": bit_of(t_svc[ntt], x)}).groupby("o", sort=False).sum()
        for o in set(agg.index[agg["has"] > 0]) | set(nagg.index[nagg["has"] > 0]):
            row = {"A_has": 0, "A_own_flag": 0, "A_wait_flag": 0, "A_linked": 0, "N_has": 0}
            if o in agg.index:
                row.update(A_has=int(agg.at[o, "has"]), A_own_flag=int(agg.at[o, "own"]), A_wait_flag=int(agg.at[o, "wait"]), A_linked=int(agg.at[o, "linked"]))
            if o in nagg.index:
                row["N_has"] = int(nagg.at[o, "has"])
            trace_table[o]["x"][name] = row
    counts = {"spans": int(len(spans)), "spans_after": int(after.sum()), "parent_resolved": int(has_parent.sum()), "max_depth": maxdepth,
              "flags_tracerca_rule": int(flag.sum()), "flags_microrank_rule": int(flag_mr.sum()), "flags_differ": int((flag != flag_mr).sum()),
              "traces_after": int(nt), "traces_A": int(t_abn.sum()), "traces_N": int(nt - t_abn.sum()),
              "edges": len(edges), "edges_with_min_calls": sum("threshold_p95_d_p_us" in e for e in edges.values()),
              "slow_calls_after": int(sum(e.get("n_slow_after", 0) for e in edges.values())),
              "after_spans_without_baseline": int((after & ~flag_ok).sum())}
    return {"services": services, "counts": counts, "edges": edges, "operations": op_table, "trace_operations": trace_table}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    only = sys.argv[2] if len(sys.argv) > 2 else None
    fx = fixtures()
    (out / "fixtures.json").write_text(json.dumps(fx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not fx["pass"]:
        raise SystemExit("trường hợp tự dựng không đạt: " + json.dumps(fx, ensure_ascii=False))
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    td_cases = {(c["dataset"], c["opaque_id"]): c for c in td.read(BASE / "runs/tracerca-core-td-001/summary.json")["cases"]}
    mr_cases = {(c["dataset"], c["opaque_id"]): c for c in td.read(BASE / "runs/microrank-core-aprime-c1-002/summary.json")["cases"]}
    rows = []
    progress = (out / "progress.jsonl").open("a", encoding="utf-8")
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        began = time.time()
        if row["source_status"] == "OK":
            directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
            adapter = td.read(directory / "capture/calls/001-adapter.json")
            spans = pd.DataFrame(table_columns(directory / "capture", adapter["entry"]["input"]))
            t = int(adapter["entry"]["t_seconds"])
            source = "bảng span adapter TraceRCA đã lưu"
        else:
            entry = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == opaque_id][0]
            t = int(td.read(BASE / "repo" / entry["path"])["window"]["t"])
            files = selector.chon_ca(allow, opaque_id, Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
            spans = cua_so.cat_span(pd.read_parquet(files["traces.parquet"]), t)
            source = "parquet gốc qua cua_so.cat_span"
        item = {"dataset": dataset, "opaque_id": opaque_id, "t_seconds": t, "span_source": source, "source_status": row["source_status"]}
        try:
            item.update(one_case(spans, t * 1_000_000))
        except Exception as error:  # giữ lượt hỏng
            item.update(status="TOOL_ERROR", error=type(error).__name__ + ": " + str(error)[:300])
            print(dataset, opaque_id, "TOOL_ERROR", error, flush=True)
            rows.append({k: item[k] for k in ("dataset", "opaque_id", "status", "error")})
            continue
        key = (dataset, opaque_id)
        check = {}
        tdc = td_cases.get(key, {})
        if tdc.get("status") == "OK":
            check["flags_equal_H_native"] = item["counts"]["flags_tracerca_rule"] == tdc["counts"]["H_native"]
        mrc = mr_cases.get(key, {})
        if mrc.get("status") == "OK":
            c = mrc["counts"]
            check["microrank_A_N_abnormal_spans_equal"] = [item["counts"]["traces_A"], item["counts"]["traces_N"], item["counts"]["flags_microrank_rule"]] == \
                [c["A"], c["N"], c["abnormal_spans"]]
        slow_ref = td.read(BASE / "runs/call-slow-001/cases" / (dataset + "-" + opaque_id + ".json"))["edges"]
        mine = {k: v for k, v in item["edges"].items() if "slow_share_after" in v}
        check["slow_edges_equal_call_slow_001"] = set(mine) == set(slow_ref) and all(
            mine[k]["n_slow_after"] == slow_ref[k]["n_slow_after"] and mine[k]["threshold_p95_d_p_us"] == slow_ref[k]["threshold_p95_d_p_us"] for k in mine)
        item["self_check"] = check
        item["status"] = "OK" if all(check.values()) else "CHECK_FAIL"
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps(item, ensure_ascii=False) + "\n", encoding="utf-8")
        line = {"dataset": dataset, "opaque_id": opaque_id, "status": item["status"], "self_check": check, "counts": item["counts"],
                "wall_s": round(time.time() - began, 1)}
        rows.append(line)
        progress.write(json.dumps(line, ensure_ascii=False) + "\n"); progress.flush()
        print(dataset, opaque_id, item["status"], check, line["wall_s"], flush=True)
    summary = {"schema": "T032-chain-spanpass-v1", "design": "results/T-032/thiet-ke-vi-tri-chuoi-goi-008.md mục 2", "fixtures": fx,
               "cases": rows, "n_cases": len(rows), "n_ok": sum(r.get("status") == "OK" for r in rows),
               "flags_differ_total": sum(r.get("counts", {}).get("flags_differ", 0) for r in rows),
               "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("XONG", summary["n_cases"], summary["n_ok"], flush=True)


if __name__ == "__main__":
    main()

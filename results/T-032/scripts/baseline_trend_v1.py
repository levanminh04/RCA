"""T-032 bảng B (thiet-ke-bang-mo-ta-004.md mục 3): xu hướng nền của cột thắng ở BARO và SimpleRCA, chỉ RE2-TT.

Chạy trên EC2. Không gọi phương pháp nào: chỉ gọi các hàm tiền xử lý mà adapter gọi (cua_so.cat_ca, baro.chuan_bi,
RCAEval preprocess, simplerca.adapter.prepare) để lấy đúng chuỗi mỗi phương pháp nhận, rồi tính các đại lượng mô tả.
Tự kiểm theo ca:
  - z cực đại theo cột tính lại bằng RobustScaler phải trùng khóa trong bản ghi BARO đóng băng từng bit;
  - phiếu metric theo dịch vụ tính lại phải trùng root_parts và above_root của runs/simplerca-decomposition-002/summary.json.
Mọi cột được tính trước; nhãn root nối sau cùng.
Dùng: python baseline_trend_v1.py <thư mục lượt mới> [opaque_id để chạy thử một ca]
"""
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
RAW = Path("/home/ubuntu/rca/T-031/repo")
I24 = REPO / "results/T-024/ban-ghi-dua-vao-cham.json"
ALLOW = REPO / "results/T-022/allowlist-dev.json"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
SIMPLE = BASE / "runs/simplerca-decomposition-002/summary.json"
HALF = 300


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def kind(column):
    return column.rsplit("_", 1)[-1]


def trend(time_n, n, time_a, a):
    """Các đại lượng của mục 3; n, a là mảng float hữu hạn cùng độ dài với time_n, time_a."""
    out = {"n_N": int(len(n)), "n_A": int(len(a))}
    if len(n) < 10 or len(a) < 10:
        out["status"] = "quá ít mẫu"
        return out
    x = time_n - time_n.mean()
    sxx = float((x * x).sum())
    slope = float((x * (n - n.mean())).sum() / sxx) if sxx > 0 else 0.0
    fitted = n.mean() + slope * x
    ss_res, ss_tot = float(((n - fitted) ** 2).sum()), float(((n - n.mean()) ** 2).sum())
    med_n, med_a = float(np.median(n)), float(np.median(a))
    shift = med_a - med_n
    step = float(np.median(a[:60]) - np.median(n[-60:]))
    drift = slope * (float(time_a.mean()) - float(time_n.mean()))
    mean, std = float(n.mean()), float(n.std(ddof=0))
    q25, q75 = np.percentile(n, [25, 75])
    diffs = np.diff(n)
    out.update({"status": "ok", "slope_N": slope, "drift_N": drift, "shift": shift, "step_60": step,
                "drift_ratio": None if shift == 0 else drift / shift, "r2_N": None if ss_tot == 0 else 1 - ss_res / ss_tot,
                "monotone_N": float((diffs >= 0).mean()) if len(diffs) else None, "median_N": med_n, "median_A": med_a,
                "std_N": std, "iqr_N": float(q75 - q25), "votes": int((a > mean + 3 * std).sum()),
                "rel_shift": None if med_n == 0 else shift / abs(med_n)})
    ratio, r2 = out["drift_ratio"], out["r2_N"]
    if ratio is not None and r2 is not None and 0.5 <= ratio <= 1.5 and r2 >= 0.5:
        out["group"] = "trôi nền"
    elif ratio is not None and abs(ratio) < 0.5 and shift != 0 and abs(step) >= 0.5 * abs(shift):
        out["group"] = "bậc tại mốc"
    elif shift == 0:
        out["group"] = "không dịch"
    else:
        out["group"] = "khác"
    return out


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


def one_case(opaque_id, frozen, allow):
    from p3 import cua_so, selector
    from p3.adapters import baro as baro_adapter
    from p3.ban_ghi import thuc_the_metric
    from RCAEval.io.time_series import preprocess
    from simplerca.adapter import prepare
    from sklearn.preprocessing import RobustScaler
    t = frozen["baro"]["window"]["t"]
    files = selector.chon_ca(allow, opaque_id, RAW, kiem_hash=True, tep=["metrics.parquet"])
    metrics = pd.read_parquet(files["metrics.parquet"])
    win, _info = cua_so.cat_ca(metrics, None, None, t)
    # ----- chuỗi như BARO nhận -----
    data = baro_adapter.chuan_bi(win["metric"])
    part_n, part_a = data[data["time"] < t], data[data["time"] >= t]
    n_df = preprocess(data=part_n, dataset="re2-tt", dk_select_useful=False)
    a_df = preprocess(data=part_a, dataset="re2-tt", dk_select_useful=False)
    time_n, time_a = part_n["time"].to_numpy(dtype=float), part_a["time"].to_numpy(dtype=float)
    columns = [c for c in n_df.columns if c in a_df.columns]
    frozen_keys = {row["item"]: row["key"][0] for row in frozen["baro"]["ranking"]}
    baro_table, z_exact = {}, set(columns) == set(frozen_keys)
    for c in columns:
        n, a = n_df[c].to_numpy(), a_df[c].to_numpy()
        scaler = RobustScaler().fit(n.reshape(-1, 1))
        z = scaler.transform(a.reshape(-1, 1))[:, 0]
        z_max = float(max(z))
        if c not in frozen_keys or z_max.hex() != float(frozen_keys[c]).hex():
            z_exact = False
        item = trend(time_n, n.astype(float), time_a, a.astype(float))
        item.update({"entity": thuc_the_metric(c), "kind": kind(c), "z_max": z_max, "argmax_z": int(np.argmax(z))})
        baro_table[c] = item
    # ----- chuỗi như SimpleRCA nhận -----
    prepared = prepare(win["metric"], None, None, t)
    nm, am = prepared.normal_metrics, prepared.incident_metrics
    tn, ta = nm["time"].to_numpy(dtype=float), am["time"].to_numpy(dtype=float)
    simple_table, votes_by_service = {}, Counter()
    for c, service in prepared.metric_services.items():
        n_raw, a_raw = np.asarray(nm[c].tolist(), dtype=float), np.asarray(am[c].tolist(), dtype=float)
        fn, fa = np.isfinite(n_raw), np.isfinite(a_raw)
        n, a = n_raw[fn], a_raw[fa]
        item = {"service": service, "entity": thuc_the_metric(service), "kind": kind(c), "n_N": int(len(n)), "n_A": int(len(a))}
        if len(n) >= 2 and len(a):  # đúng điều kiện và công thức của simplerca.core.diagnose
            mean, std = float(n.mean()), float(n.std(ddof=0))
            item["votes_native_formula"] = int(np.sum(a > mean + 3.0 * std))
            votes_by_service[service] += item["votes_native_formula"]
        else:
            item["votes_native_formula"] = 0
        item.update({k: v for k, v in trend(tn[fn], n, ta[fa], a).items() if k not in ("n_N", "n_A")})
        simple_table[c] = item
    return {"t": t, "baro_columns": baro_table, "baro_z_bit_exact": bool(z_exact), "simple_columns": simple_table,
            "simple_votes_by_service": dict(votes_by_service)}


def best_column(table, entity, score_key):
    rows = [(v[score_key], c) for c, v in table.items() if v["entity"] == entity and v.get(score_key) is not None]
    if not rows:
        return None
    top = max(x[0] for x in rows)
    return sorted(c for s, c in rows if s == top)[0]


def quantiles(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    pick = lambda q: values[min(len(values) - 1, int(q * len(values)))]
    return {"n": len(values), "min": values[0], "q25": pick(0.25), "median": statistics.median(values), "q75": pick(0.75), "max": values[-1]}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    only = sys.argv[2] if len(sys.argv) > 2 else None
    from p3 import selector
    allow = selector.nap_allowlist(ALLOW)
    index = read(I24)["records"]
    labels = {r["opaque_id"]: r for r in read(LABELS)["main_rows"] if r["dataset"] == "RE2-TT" and r["method"] == "baro"}
    simple_ref = {c["opaque_id"]: c for c in read(SIMPLE)["cases"] if c["dataset"] == "RE2-TT"}
    cases, pooled = [], {"baro": [], "simple": []}
    winners = {"baro": [], "simple": []}
    for opaque_id in sorted(labels):
        if only and only != opaque_id:
            continue
        frozen = {}
        for method in ("baro", "simplerca"):
            entry = [e for e in index if e["method"] == method and e["opaque_id"] == opaque_id and e["variant"] == "native"]
            if len(entry) != 1 or sha(REPO / entry[0]["path"]) != entry[0]["sha256"]:
                raise SystemExit("bản đóng băng thiếu hoặc khác hash: " + method + " " + opaque_id)
            frozen[method] = read(REPO / entry[0]["path"])
        label = labels[opaque_id]
        base = {"opaque_id": opaque_id, "root": label["root"], "fault": label["fault"], "cell": label["cell"]}
        if frozen["baro"]["status"] != "OK" or frozen["simplerca"]["status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "bản đóng băng không OK"})
            continue
        computed = one_case(opaque_id, frozen, allow)  # chưa dùng nhãn
        (out / "cases" / (opaque_id + ".json")).write_text(json.dumps({**base, **computed}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        # --- nối nhãn ---
        root = label["root"]
        ref = simple_ref.get(opaque_id)
        vote_check = None
        if ref and ref.get("status") == "OK" and ref.get("root_ranked"):
            expected = {ref["root_parts"]["item"]: ref["root_parts"]["metric"]}
            expected.update({a["item"]: a["metric"] for a in ref.get("above_root", [])})
            vote_check = all(computed["simple_votes_by_service"].get(s, 0) == v for s, v in expected.items())
        item = {**base, "status": "OK", "baro_z_bit_exact": computed["baro_z_bit_exact"], "simple_votes_match_decomposition": vote_check}
        usable = computed["baro_z_bit_exact"] and vote_check is True
        item["usable"] = bool(usable)
        for name, table, record, score in (("baro", computed["baro_columns"], frozen["baro"], "z_max"),
                                           ("simple", computed["simple_columns"], frozen["simplerca"], "votes_native_formula")):
            rank = ranks(record)
            if root not in rank:
                item[name] = {"root_ranked": False}
                continue
            above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
            block = {"root_ranked": True, "root_rank_min": rank[root][0], "root_rank_max": rank[root][1], "n_above": len(above), "rows": []}
            for entity, role in [(root, "root")] + [(e, "above_root") for e in above]:
                column = best_column(table, entity, score)
                if column is None:
                    block["rows"].append({"entity": entity, "role": role, "column": None})
                    continue
                c = table[column]
                row = {"entity": entity, "role": role, "column": column, "kind": c["kind"], "group": c.get("group"),
                       "drift_ratio": c.get("drift_ratio"), "r2_N": c.get("r2_N"), "monotone_N": c.get("monotone_N"),
                       "shift": c.get("shift"), "step_60": c.get("step_60"), "rel_shift": c.get("rel_shift"),
                       "votes": c.get("votes_native_formula", c.get("votes")), "z_max": c.get("z_max")}
                block["rows"].append(row)
                if usable:
                    winners[name].append({**row, "opaque_id": opaque_id, "case_wrong_at_1": rank[root][1] > 1})
            item[name] = block
        if usable:
            for name, table in (("baro", computed["baro_columns"]), ("simple", computed["simple_columns"])):
                for column, c in table.items():
                    if c.get("status") == "ok":
                        pooled[name].append({"opaque_id": opaque_id, "kind": c["kind"], "group": c["group"], "votes": c.get("votes_native_formula", c.get("votes")),
                                             "drift_ratio": c["drift_ratio"], "r2_N": c["r2_N"], "is_root_entity": c["entity"] == root})
        cases.append(item)
        print(opaque_id, item["baro_z_bit_exact"], item["simple_votes_match_decomposition"], flush=True)

    def winner_block(rows):
        table = {}
        for role in ("root", "above_root"):
            for wrong in (True, False):
                sub = [r for r in rows if r["role"] == role and r["case_wrong_at_1"] == wrong]
                key = role + ("|ca sai hạng 1" if wrong else "|ca đúng hạng 1")
                table[key] = {"n": len(sub), "by_kind": dict(Counter(r["kind"] for r in sub)),
                              "by_group": dict(Counter(str(r["group"]) for r in sub)),
                              "by_kind_group": dict(Counter(r["kind"] + "|" + str(r["group"]) for r in sub)),
                              "drift_ratio": quantiles([r["drift_ratio"] for r in sub]), "r2_N": quantiles([r["r2_N"] for r in sub]),
                              "votes": quantiles([r["votes"] for r in sub])}
        return table

    def pooled_block(rows):
        table = {}
        for k in sorted({r["kind"] for r in rows}):
            sub = [r for r in rows if r["kind"] == k]
            table[k] = {"n_columns": len(sub), "by_group": dict(Counter(r["group"] for r in sub)),
                        "votes_ge_250": sum((r["votes"] or 0) >= 250 for r in sub),
                        "votes_ge_250_root_entity": sum((r["votes"] or 0) >= 250 and r["is_root_entity"] for r in sub),
                        "n_root_entity": sum(r["is_root_entity"] for r in sub),
                        "drift_group_root_entity": sum(r["group"] == "trôi nền" and r["is_root_entity"] for r in sub),
                        "r2_N": quantiles([r["r2_N"] for r in sub]), "drift_ratio": quantiles([r["drift_ratio"] for r in sub])}
        return table

    ok = [c for c in cases if c["status"] == "OK"]
    summary = {"n_cases": len(cases), "status_ok": len(ok), "baro_z_bit_exact": sum(c["baro_z_bit_exact"] for c in ok),
               "simple_votes_match_decomposition": sum(c["simple_votes_match_decomposition"] is True for c in ok),
               "usable": sum(c["usable"] for c in ok),
               "winning_columns": {"baro": winner_block(winners["baro"]), "simple": winner_block(winners["simple"])},
               "all_columns_no_label": {"baro_view": pooled_block(pooled["baro"]), "simple_view": pooled_block(pooled["simple"])},
               "note": "Bảng mô tả trên dev RE2-TT. Mốc chia nhóm đặt trước ở thiet-ke-bang-mo-ta-004.md mục 3; phân vị thô báo kèm. "
                       "Cột 'votes' ở khung BARO là số mẫu A vượt mean+3std của N trên chuỗi BARO nhận; ở khung SimpleRCA là phiếu native."}
    result = {"schema": "T032-baseline-trend-v1", "design": "results/T-032/thiet-ke-bang-mo-ta-004.md#3", "methods_executed": False,
              "sources": {"index24_sha256": sha(I24), "labels_sha256": sha(LABELS), "simplerca_decomposition_sha256": sha(SIMPLE)},
              "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("n_cases", "status_ok", "baro_z_bit_exact", "simple_votes_match_decomposition", "usable")}))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())

"""T-034 K2: dựng `bang-baseline.json` từ các file chấm đã khóa và tính lại độc lập các số tổng (V2). Chỉ đọc nguồn.

Không chạy phương pháp nào. Bảng chính lấy nguyên số của T-024, T-025, T-026; nhánh chẩn đoán báo riêng.
V2: tính lại từ **bản ghi từng lượt** (thứ hạng theo thực thể kèm nhóm hòa, hoặc khối của TORAI) và file nhãn,
bằng một bộ chấm viết riêng ở đây (không nhập `src/p3/danh_gia.py`), rồi so với số tổng trong JSON chấm.
Phát hiện: tính lại từ báo động thô (`bao-dong.json`) theo quy tắc cửa sổ 60 giây của WHY-35.

Dùng: python k2_bang_baseline.py <thư mục lượt mới>
"""
import hashlib
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOL = 1e-12
MAIN = ["baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"]
NAMES = {"baro": "BARO", "simplerca": "SimpleRCA (M4)", "microrank_full": "MicroRank (bản RCAEval sửa đầu vào, xếp đầy đủ)",
         "tracerca": "TraceRCA (bản RCAEval, lọc hữu hạn)", "circa_ols_da": "CIRCA (đồ thị kiến trúc, OLS+RHT+DA)", "torai_B": "TORAI (bản sửa, nguồn B)"}
METRICS = ["hit@1", "hit@3", "hit@5", "avg@5", "mrr", "ndcg@5", "retrieval@5", "rerank@1(K=5)", "retrieval@10", "rerank@1(K=10)"]


def read(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------------------------------------------------
# Bộ chấm độc lập: phân phối hạng của root khi thứ tự trong nhóm hòa ngẫu nhiên đều (WHY-28)
# ---------------------------------------------------------------------------------------------------------------------
def ordered_groups(record):
    """Trả danh sách nhóm hòa theo thứ tự hạng. TORAI: nối khối theo thứ tự; các khối cùng khóa phải không tồn tại (đã kiểm ở T-024)."""
    if record.get("blocks"):
        keys = [tuple(b["key"]) for b in record["blocks"]]
        if len(set(keys)) != len(keys):
            raise ValueError("TORAI có khối cùng khóa: bộ chấm độc lập này không xử lý, phải dùng hoán vị khối")
        return [list(g) for b in record["blocks"] for g in b["groups"]]
    groups = defaultdict(list)
    order = []
    for e in record["entity_ranking"]:
        if e["tie_group"] not in groups:
            order.append(e["tie_group"])
        groups[e["tie_group"]].append(e["entity"])
    assert order == sorted(order), "nhóm hòa không theo thứ tự hạng"
    return [groups[g] for g in order]


def score_record(record, root):
    zero = {"hit@%d" % k: 0.0 for k in range(1, 11)}
    zero.update(rr=0.0, **{"ndcg@5": 0.0, "avg@5": 0.0}, rank_min=None, rank_max=None)
    if record["status"] != "OK":
        return zero
    before = 0
    for g in ordered_groups(record):
        if root in g:
            s = len(g)
            ranks = range(before + 1, before + s + 1)
            out = {"hit@%d" % k: min(max(k - before, 0), s) / s for k in range(1, 11)}
            out["rr"] = sum(1.0 / r for r in ranks) / s
            out["ndcg@5"] = sum(1.0 / math.log2(r + 1) for r in ranks if r <= 5) / s
            out["avg@5"] = sum(out["hit@%d" % k] for k in range(1, 6)) / 5
            out["rank_min"], out["rank_max"] = before + 1, before + s
            return out
        before += len(g)
    return zero


def summarize(per_case):
    n = len(per_case)
    out = {"n": n}
    for k in (1, 3, 5, 10):
        out["hit@%d" % k] = sum(c["hit@%d" % k] for c in per_case) / n
    out["avg@5"] = sum(c["avg@5"] for c in per_case) / n
    out["mrr"] = sum(c["rr"] for c in per_case) / n
    out["ndcg@5"] = sum(c["ndcg@5"] for c in per_case) / n
    out["retrieval@5"], out["retrieval@10"] = out["hit@5"], out["hit@10"]
    for K in (5, 10):
        den = sum(c["hit@%d" % K] for c in per_case)
        out["rerank@1(K=%d)" % K] = (sum(c["hit@1"] for c in per_case) / den) if den > 0 else None
    return out


def compare(a, b, keys, where, problems):
    worst = 0.0
    for k in keys:
        x, y = a.get(k), b.get(k)
        if x is None or y is None:
            if x != y:
                problems.append({"where": where, "key": k, "source": y, "recomputed": x})
            continue
        d = abs(x - y)
        worst = max(worst, d)
        if d > TOL:
            problems.append({"where": where, "key": k, "source": y, "recomputed": x, "abs_diff": d})
    return worst


def ranking_block(dataset, cohort_name, case_ids, methods, labels, getter, problems, source_file):
    """getter(method) -> (summary_main, rcaeval_mean, per_case_source, record_paths_by_case, bootstrap, pointer_prefix)."""
    block = {}
    for m in methods:
        info = getter(m)
        if info is None:
            continue
        summary, rcaeval, per_case_src, paths, boot, pointer = info
        mine = []
        statuses = Counter()
        by_cell = defaultdict(lambda: {"n": 0, "hit@1": 0.0, "hit@5": 0.0, "status": Counter(), "cases": []})
        for cid in case_ids:
            root = labels[cid]["root"]
            seeds = []
            st = Counter()
            for p in paths[cid]:
                rec = read(p)
                assert rec["opaque_id"] == cid
                seeds.append(score_record(rec, root))
                st[rec["status"]] += 1
            agg = {k: sum(s[k] for s in seeds) / len(seeds) for k in seeds[0] if k not in ("rank_min", "rank_max")}
            case_status = st.most_common(1)[0][0] if len(st) == 1 else "MIXED"
            statuses[case_status] += 1
            mine.append(agg)
            src = per_case_src[cid]
            compare(agg, src, ["hit@1", "hit@3", "hit@5", "hit@10", "rr", "ndcg@5", "avg@5"], f"{dataset}/{cohort_name}/{m}/{cid}", problems)
            if src.get("status") not in (None, case_status):
                problems.append({"where": f"{dataset}/{cohort_name}/{m}/{cid}", "key": "status", "source": src.get("status"), "recomputed": case_status})
            cell = by_cell[labels[cid]["cell"]]
            cell["n"] += 1
            cell["hit@1"] += agg["hit@1"]
            cell["hit@5"] += agg["hit@5"]
            cell["status"][case_status] += 1
            cell["cases"].append({"opaque_id": cid, "hit@1": agg["hit@1"], "hit@5": agg["hit@5"], "status": case_status})
        recomputed = summarize(mine)
        worst = compare(recomputed, summary, METRICS, f"{dataset}/{cohort_name}/{m}/summary", problems)
        src_status = {k: v for k, v in summary["trang_thai"].items() if v}
        if dict(statuses) != src_status:
            problems.append({"where": f"{dataset}/{cohort_name}/{m}", "key": "trang_thai", "source": src_status, "recomputed": dict(statuses)})
        entry = {"name": NAMES.get(m, m), "n": summary["n"], "status": src_status,
                 **{k: summary[k] for k in METRICS},
                 "bounds_optimistic_hit@1": summary["can_lac_quan"]["hit@1"], "bounds_pessimistic_hit@1": summary["can_bi_quan"]["hit@1"],
                 "hit@1_cases_expected": summary["hit@1"] * summary["n"], "hit@5_cases_expected": summary["hit@5"] * summary["n"],
                 "rcaeval": None if rcaeval is None else {k: rcaeval[k] for k in ("AC@1", "AC@3", "AC@5", "Avg@5")},
                 "bootstrap95": None if boot is None else {k: boot[k] for k in ("hit@1", "hit@5", "rr", "ndcg@5") if k in boot},
                 "by_cell": {c: {"n": v["n"], "hit@1_sum": v["hit@1"], "hit@5_sum": v["hit@5"], "status": dict(v["status"]), "cases": v["cases"]} for c, v in sorted(by_cell.items())},
                 "source": source_file, "pointer": pointer, "v2_max_abs_diff_summary": worst, "v2_records_read": sum(len(paths[c]) for c in case_ids)}
        block[m] = entry
    return block


def detection_from_alarms(alarms_file, labels, problems, source):
    """Tính lại theo WHY-35: cửa sổ 60 giây từ đầu file; chỉ chấm cửa sổ mà mọi điểm đã được đánh giá; bỏ cửa sổ cuối thiếu điểm."""
    raw = read(alarms_file)["bo_phat_hien"]
    out = {}
    T, W = 1441, 60
    # t0 của từng ca lấy từ bản ghi BOCPD (có cả timestamp lẫn chỉ số); N-Sigma chỉ lưu timestamp nên dùng chung t0 này
    t0_by_case = {cid: c["alarms"][0] - c["chi_so"][0] for cid, c in raw["bocpd"].items() if c["alarms"]}
    assert len(t0_by_case) == len(raw["bocpd"]) == 30
    for det, cases in raw.items():
        src = source["bo_phat_hien"][det]
        tp = fp = fn = tn = dropped = 0
        false_alarms = normal_seconds = detected = first_correct = 0
        delays = []
        per_case = {}
        for cid, c in cases.items():
            assert c["status"] == "OK", "bộ chấm lại này chỉ xử lý ca OK"
            t0 = t0_by_case[cid]
            idx = sorted(a - t0 for a in c["alarms"])
            if c.get("chi_so") is not None:
                assert idx == sorted(c["chi_so"]), "chỉ số suy từ timestamp khác chỉ số đã lưu"
            assert all(0 <= i < T for i in idx)
            inject = labels[cid]["inject_time"]
            p = inject - t0
            assert p == 720, f"mốc không ở chỉ số 720: {cid} {p}"
            start = c["bat_dau_danh_gia"]
            ctp = cfp = cfn = ctn = cdrop = 0
            for w0 in range(0, T, W):
                w1 = w0 + W
                if w1 > T or w0 < start:
                    cdrop += 1
                    continue
                positive = any(w0 <= i < w1 for i in idx)
                anomalous = w0 >= p
                assert not (w0 < p < w1), "cửa sổ cắt ngang mốc"
                if anomalous and positive:
                    ctp += 1
                elif anomalous:
                    cfn += 1
                elif positive:
                    cfp += 1
                else:
                    ctn += 1
            before = [i for i in idx if start <= i < p]
            after = [i for i in idx if i >= p]
            cnormal = p - start
            d = (after[0] - p) if after else None
            t_hat_correct = bool(idx) and idx[0] >= p
            per_case[cid] = {"tp": ctp, "fp": cfp, "fn": cfn, "tn": ctn, "dropped": cdrop, "false_alarms": len(before), "normal_seconds": cnormal,
                             "delay_s": d, "detected": bool(after), "first_alarm_correct": t_hat_correct, "first_alarm_index": idx[0] if idx else None}
            s = src["ca"][cid]
            for a, b in (("tp", "tp"), ("fp", "fp"), ("fn", "fn"), ("tn", "tn"), ("dropped", "bo")):
                if per_case[cid][a] != s["cua_so"][b]:
                    problems.append({"where": f"detection/{det}/{cid}", "key": a, "source": s["cua_so"][b], "recomputed": per_case[cid][a]})
            for a, b in (("false_alarms", "bao_dong_sai"), ("normal_seconds", "giay_binh_thuong_danh_gia"), ("delay_s", "do_tre_s"), ("detected", "phat_hien_ca"),
                         ("first_alarm_correct", "t_hat_dung")):
                if per_case[cid][a] != s[b]:
                    problems.append({"where": f"detection/{det}/{cid}", "key": a, "source": s[b], "recomputed": per_case[cid][a]})
            tp, fp, fn, tn, dropped = tp + ctp, fp + cfp, fn + cfn, tn + ctn, dropped + cdrop
            false_alarms += len(before)
            normal_seconds += cnormal
            detected += bool(after)
            first_correct += t_hat_correct
            if d is not None:
                delays.append(d)
        delays.sort()
        n = len(delays)
        median = (delays[n // 2] if n % 2 else (delays[n // 2 - 1] + delays[n // 2]) / 2) if n else None
        mine = {"precision": tp / (tp + fp) if tp + fp else None, "recall": tp / (tp + fn) if tp + fn else None,
                "bao_dong_sai_moi_gio": false_alarms / normal_seconds * 3600}
        mine["f1"] = 2 * mine["precision"] * mine["recall"] / (mine["precision"] + mine["recall"]) if mine["precision"] and mine["recall"] else None
        cond = src["tong_hop"]["co_dieu_kien_tren_ca_OK"]
        worst = compare(mine, cond, ["precision", "recall", "f1", "bao_dong_sai_moi_gio"], f"detection/{det}/summary", problems)
        for key, mine_v, src_v in (("tp", tp, cond["cua_so"]["tp"]), ("fp", fp, cond["cua_so"]["fp"]), ("fn", fn, cond["cua_so"]["fn"]), ("tn", tn, cond["cua_so"]["tn"]),
                                   ("false_alarms", false_alarms, cond["bao_dong_sai"]), ("normal_seconds", normal_seconds, cond["giay_binh_thuong_danh_gia"]),
                                   ("detected", detected, src["tong_hop"]["theo_ca_tren_30"]["phat_hien"]),
                                   ("first_alarm_correct", first_correct, src["tong_hop"]["theo_ca_tren_30"]["bao_dong_dau_dung"]),
                                   ("delay_median", median, cond["do_tre_s"]["trung_vi"]), ("delay_min", delays[0] if n else None, cond["do_tre_s"]["min"]),
                                   ("delay_max", delays[-1] if n else None, cond["do_tre_s"]["max"])):
            if mine_v != src_v:
                problems.append({"where": f"detection/{det}/summary", "key": key, "source": src_v, "recomputed": mine_v})
        out[det] = {"n_cases": src["tong_hop"]["so_ca"], "status": {k: v for k, v in src["tong_hop"]["trang_thai"].items() if v},
                    "windows": {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "dropped": dropped},
                    "precision": cond["precision"], "recall": cond["recall"], "f1": cond["f1"],
                    "false_alarms": cond["bao_dong_sai"], "normal_seconds_evaluated": cond["giay_binh_thuong_danh_gia"],
                    "false_alarms_per_normal_hour": cond["bao_dong_sai_moi_gio"],
                    "delay_from_injection_s": {k: cond["do_tre_s"][k] for k in ("n", "trung_vi", "tb", "min", "max")},
                    "cases_detected": src["tong_hop"]["theo_ca_tren_30"]["phat_hien"], "cases_first_alarm_at_or_after_injection": src["tong_hop"]["theo_ca_tren_30"]["bao_dong_dau_dung"],
                    "delays_equal_zero": sum(1 for d in delays if d == 0),
                    "source": "results/T-025/phat-hien.json", "pointer": f"/bo_phat_hien/{det}/tong_hop", "raw_alarms": alarms_file,
                    "v2_max_abs_diff_summary": worst, "v2_per_case": per_case}
    return out


def main():
    run = Path(sys.argv[1])
    run.mkdir(parents=True, exist_ok=False)
    began = time.perf_counter()
    problems = []
    out = {"schema": "T034-bang-baseline-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "note": "Số bảng chính lấy nguyên từ các file chấm đã khóa của T-024, T-025, T-026; không chạy lại phương pháp. Nhánh chẩn đoán báo riêng, không phải baseline.",
           "sources": {}}
    for rel in ("results/T-024/cham-a.json", "results/T-025/phat-hien.json", "results/T-025/cham-b.json", "results/T-025/bao-dong.json", "results/T-026/cham-a.json",
                "results/T-022/nhan-dev.json", "results/T-026/nhan-dev.json", "results/T-029/a-so-b.json",
                "results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/fast-summary-001.json",
                "results/T-032/runs/bo-sung-toan-dien-20261012-001/author-tracerca/full008-instrumented/summary.json",
                "results/T-032/runs/microrank-partition-001/collect-001/summary.json"):
        out["sources"][rel] = sha(rel)

    # ---------------- xếp hạng chế độ (a), RE2-TT ----------------
    a24 = read("results/T-024/cham-a.json")
    lab24 = {c["opaque_id"]: c for c in read("results/T-022/nhan-dev.json")["cases"]}
    out["ranking_mode_a"] = {}
    for cohort in ("dev30", "dev19"):
        ids = a24["cohorts"][cohort]["case_ids"]

        def getter(m, cohort=cohort):
            mm = a24["methods"][m]
            s = mm["summaries"][cohort]
            return (s["main"], s["rcaeval"]["mean"], mm["per_case"], {c: mm["per_case"][c]["source_paths"] for c in ids},
                    a24["bootstrap"][cohort]["phuong_phap"].get(m), f"/methods/{m}/summaries/{cohort}/main")

        out["ranking_mode_a"]["RE2-TT_" + cohort] = {"n_cases": len(ids), "n_cells": a24["cohorts"][cohort]["n_cells"],
                                                     "cohort_note": a24["cohorts"][cohort].get("selection_note"),
                                                     "methods": ranking_block("RE2-TT", cohort, ids, MAIN, lab24, getter, problems, "results/T-024/cham-a.json")}
    # ---------------- xếp hạng chế độ (a), Nezha-OB ----------------
    a26 = read("results/T-026/cham-a.json")
    lab26 = {c["opaque_id"]: c for c in read("results/T-026/nhan-dev.json")["cases"]}
    main26 = a26["tables"]["main"]
    ids26 = main26["case_ids"]

    def getter26(m):
        mm = main26["methods"][m]
        paths = defaultdict(list)
        for r in mm["source_records"]:
            paths[r["opaque_id"]].append(r["path"])
        s = mm["summary"]
        boot = main26["bootstrap"].get("phuong_phap", {}).get(m) if isinstance(main26.get("bootstrap"), dict) else None
        return s["main"], (s.get("rcaeval") or {}).get("mean"), mm["per_case"], paths, boot, f"/tables/main/methods/{m}/summary/main"

    out["ranking_mode_a"]["Nezha-OB_main"] = {"n_cases": len(ids26), "n_cells": main26["n_cells"],
                                              "methods": ranking_block("Nezha-OB", "main", ids26, MAIN, lab26, getter26, problems, "results/T-026/cham-a.json")}

    # ---------------- phát hiện ----------------
    ph = read("results/T-025/phat-hien.json")
    out["detection_mode_b"] = detection_from_alarms("results/T-025/bao-dong.json", lab24, problems, ph)
    out["detection_label_note"] = ("Nhãn proxy của giao thức (WHY-35): bất thường = [mốc tiêm, cuối file]. Không xác nhận độc lập khoảng khỏe, onset hay lúc hết lỗi. "
                                   "Số báo động sai mỗi giờ là trên giờ bình thường theo nhãn proxy; độ trễ tính từ mốc tiêm.")
    d33 = read("results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/fast-summary-001.json")
    out["detection_endpoint_sensitivity_D"] = {"bocpd_cases_with_any_cp_within_D_seconds_after_injection": d33["bocpd_post_any_byD"], "n_cases": 30,
                                               "source": "results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/fast-summary-001.json", "pointer": "/bocpd_post_any_byD",
                                               "note": "Độ nhạy theo điểm cuối D; D không phải thời điểm hết lỗi vật lý; không chấm lại P3."}

    # ---------------- chế độ (b): RCA tại báo động đầu ----------------
    cb = read("results/T-025/cham-b.json")
    out["mode_b_rca_at_first_alarm"] = {}
    for det, rankers in cb["theo_bo_phat_hien"].items():
        for ranker, block in rankers.items():
            th = block["tong_hop"]
            ca = block["ca"]
            n = len(ca)
            joint = {k: sum((c[k] if c["t_hat_dung"] else 0.0) for c in ca.values()) / n for k in ("hit@1", "hit@3", "hit@5")}
            compare(joint, th["thanh_cong_chung_tren_30"], ["hit@1", "hit@3", "hit@5"], f"mode_b/{det}/{ranker}/joint", problems)
            correct = sum(bool(c["t_hat_dung"]) for c in ca.values())
            if correct != th["so_ca_t_hat_dung"]:
                problems.append({"where": f"mode_b/{det}/{ranker}", "key": "so_ca_t_hat_dung", "source": th["so_ca_t_hat_dung"], "recomputed": correct})
            # báo động đầu đúng phải khớp bảng phát hiện
            det_ok = out["detection_mode_b"][det]["cases_first_alarm_at_or_after_injection"]
            if correct != det_ok:
                problems.append({"where": f"mode_b/{det}/{ranker}", "key": "t_hat_dung vs detection", "source": det_ok, "recomputed": correct})
            out["mode_b_rca_at_first_alarm"][f"{ranker}[{det}]"] = {
                "n": n, "cases_first_alarm_correct": th["so_ca_t_hat_dung"], "cases_first_alarm_wrong": th["so_ca_t_hat_sai"],
                "joint_success": th["thanh_cong_chung_tren_30"], "rca_at_first_alarm_all_cases": {k: th["tren_ca_co_luot_rca"][k] for k in ("n", "hit@1", "hit@3", "hit@5")},
                "rca_when_first_alarm_correct": None if th["tren_ca_t_hat_dung"] is None else {k: th["tren_ca_t_hat_dung"][k] for k in ("n", "hit@1", "hit@3", "hit@5")},
                "source": "results/T-025/cham-b.json", "pointer": f"/theo_bo_phat_hien/{det}/{ranker}/tong_hop"}

    # ---------------- bảng G của T-029: RCA theo điểm chạy ----------------
    g = read("results/T-029/a-so-b.json")
    out["table_G_run_point"] = {"definition": g["interpretation"], "points": {"a": "mốc tiêm (chế độ a)", "t_hat_plus": "báo động đầu tiên sau mốc (chọn nhờ nhãn mốc, I3)", "t_hat": "báo động đầu"}, "rows": {}}
    for det, rankers in g["by_detector"].items():
        for ranker, block in rankers.items():
            pts = {p: {"hit@1": 0.0, "hit@5": 0.0} for p in ("a", "t_hat_plus", "t_hat")}
            for c in block["per_case"]:
                for p in pts:
                    for k in ("hit@1", "hit@5"):
                        pts[p][k] += c["points"][p][k] / len(block["per_case"])
            for p in pts:
                compare(pts[p], block["all30"]["points"][p], ["hit@1", "hit@5"], f"table_G/{det}/{ranker}/{p}", problems)
            out["table_G_run_point"]["rows"][f"{ranker}[{det}]"] = {"n": block["all30"]["n"], "points": block["all30"]["points"], "signed_deltas": block["all30"]["signed_deltas"],
                                                                    "by_event_group": {k: {"n": v["n"], "points": v["points"]} for k, v in block["by_event_group"].items()},
                                                                    "source": "results/T-029/a-so-b.json", "pointer": f"/by_detector/{det}/{ranker}/all30"}

    # ---------------- nhánh chẩn đoán, báo riêng ----------------
    f8 = read("results/T-032/runs/bo-sung-toan-dien-20261012-001/author-tracerca/full008-instrumented/summary.json")
    diag = {}
    for row in f8["rows"]:
        key = (row["dataset"], row["latency_unit"], row["feature_selection_threshold"])
        d = diag.setdefault(key, {"n": 0, "status": Counter(), "hit1_pessimistic": 0, "hit1_expected": 0.0, "hit1_optimistic": 0, "ties_with_root_at_top": 0, "root_default_minus1": 0})
        d["n"] += 1
        d["status"][row["status"]] += 1
        if row["status"] == "OK" and row.get("root_rank_min") is not None:
            lo, hi = row["root_rank_min"], row["root_rank_max"]
            d["hit1_pessimistic"] += int(hi == 1)
            d["hit1_optimistic"] += int(lo == 1)
            d["hit1_expected"] += (1.0 / (hi - lo + 1)) if lo == 1 else 0.0
            d["ties_with_root_at_top"] += int(lo == 1 and hi > 1)
            if row.get("scores", {}).get(row["root"]) == -1.0:
                d["root_default_minus1"] += 1
    out["diagnostic_branches_not_baseline"] = {
        "tracerca_author_code_latency_only": {
            "label": "Chẩn đoán trên dev, chưa là baseline. Mã tác giả TraceRCA (commit b9087c72), nhánh chỉ độ trễ mà đầu vào hỗ trợ; không phải tái lập bài hay cấu hình mặc định.",
            "input_contract": f8["default_pipeline_status"], "missing_evidence_rule": "NO_EVIDENCE và root vắng tính 0 trong mẫu số toàn cohort",
            "tie_rule": "hạng bi quan = cuối nhóm hòa; kỳ vọng = xác suất root vào hạng 1 khi hoán vị đều trong nhóm; dịch vụ không có tập một dịch vụ được giữ nhận điểm mặc định −1",
            "rows": [{"dataset": k[0], "latency_unit": k[1], "feature_selection_threshold": k[2], **{kk: (dict(vv) if isinstance(vv, Counter) else vv) for kk, vv in v.items()}}
                     for k, v in sorted(diag.items())],
            "source": "results/T-032/runs/bo-sung-toan-dien-20261012-001/author-tracerca/full008-instrumented/summary.json", "pointer": "/rows"}}
    # đối chiếu với ledger đính chính (đơn vị ms)
    led = read("results/T-032/runs/bo-sung-toan-dien-20261012-001/closure-ledger-review-001.json")["baseline_comparison"]["supported_author"]
    for L in led:
        mine = diag[(L["dataset"], L["latency_unit"], float(L["feature_selection_threshold"]))]
        for a, b in (("hit1_pessimistic", "Hit1_pessimistic"), ("hit1_expected", "Hit1_expected"), ("n", "N_all_cases")):
            if abs(mine[a] - L[b]) > TOL:
                problems.append({"where": f"author/{L['dataset']}/{L['feature_selection_threshold']}", "key": a, "source": L[b], "recomputed": mine[a]})
        if dict(mine["status"]) != L["statuses"]:
            problems.append({"where": f"author/{L['dataset']}/{L['feature_selection_threshold']}", "key": "statuses", "source": L["statuses"], "recomputed": dict(mine["status"])})
    mr = read("results/T-032/runs/microrank-partition-001/collect-001/summary.json")
    out["diagnostic_branches_not_baseline"]["microrank_paper_split"] = {
        "label": "Chẩn đoán trên dev, chưa là baseline. " + mr["name"], "summary": {ds: mr["summary"][ds] for ds in ("RE2-TT", "Nezha-OB") if ds in mr["summary"]},
        "self_check": mr["summary"]["self_check"], "source": "results/T-032/runs/microrank-partition-001/collect-001/summary.json", "pointer": "/summary"}

    out["v2"] = {"status": "PASS" if not problems else "FAIL", "tolerance_abs": TOL, "problems": problems[:200], "n_problems": len(problems),
                 "elapsed_s": round(time.perf_counter() - began, 3),
                 "what": "Số tổng xếp hạng tính lại từ bản ghi từng lượt + file nhãn bằng bộ chấm viết riêng; phát hiện tính lại từ báo động thô; chế độ (b) và bảng G tính lại từ bảng theo ca; nhánh tác giả tính lại từ 208 hàng Full008 và so ledger."}
    text = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    (run / "bang-baseline.json").write_text(text, encoding="utf-8")
    print("V2", out["v2"]["status"], "problems", len(problems), "elapsed", out["v2"]["elapsed_s"])
    for p in problems[:25]:
        print("  ", json.dumps(p, ensure_ascii=False)[:300])


if __name__ == "__main__":
    main()

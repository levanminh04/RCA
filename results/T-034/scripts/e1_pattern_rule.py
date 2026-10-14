"""T-034 E1: tác động riêng của quy tắc pattern trong bản TraceRCA cài theo lời văn (phép T-O của T-032).

Thiết kế: results/T-034/thiet-ke-hai-phep-kiem.md, phần E1 (viết trước khi chạy). Chạy trên EC2 T-032, chỉ đọc nguồn T-032.
Mã nguồn `tracerca_original_ranking_v1` được nhập nguyên trạng; `one_case` gốc dựng lời gọi, cờ, bảng kiểu trace.
Yếu tố duy nhất bị đổi: trong tập `top` đã giữ, chỉ tập một dịch vụ được đóng góp điểm (nhánh B). Nhánh A giữ như nguồn.
Nhãn root chỉ dùng sau khi mọi điểm đã tính.

Dùng: python e1_pattern_rule.py <thư mục lượt mới> <ledger đính chính> [--only dataset:opaque_id]
"""
import hashlib
import json
import os
import platform
import resource
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
import tracerca_original_ranking_v1 as src  # noqa: E402  (nguồn, chỉ đọc)

td, cp = src.td, src.cp

PINS = {
    "scripts/tracerca_original_ranking_v1.py": "9cc409f21da4cbb8be6e9a799eead2904c6fe69db6933156b27ed20a3c3ee080",
    "scripts/tracerca_core_and_td_v1.py": "ee60f9197600426ca35fe3dc50214aac14c981d7f1d623afbd84f7dafcf2e003",
    "scripts/chain_position_v1.py": "f30debb080e86a488112115eabb00540b4407a473e285ef72e295b13e9dc8c31",
    "scripts/replay_tracerca_v3.py": "3127b73285cbce3cf7ba68483a7ca5d651007e097b5d913ac7544dc76ef064ee",
    "runs/tracerca-original-ranking-001/cases.json": "2203c6efae523d934f176eb9bea8e1c495efce752987a56ce286c4f7325d20ac",
    "runs/tracerca-original-ranking-001/summary.json": "1d36448e30c490df648bf17c52c061de2e3416991d495408acdb4510f5ed0612",
    "runs/slow-call-flag-link-001/cases.json": "7b3663a286facbd4b3061d29ff6a0304da62311c00e59920fd2f10536f47fde8",
}
LEDGER_SHA = "03606df024ae3a89ac8702d765948c1095e689d7d99e02e277f5041f180b81d6"
BRANCH_ORDER = list(src.BRANCHES)          # to_p, to_c, to_p3: thứ tự gọi score_services trong one_case
PRIMARY, SECOND, AUX = "to_p", "to_p3", "to_c"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def frac(v):
    return [v.numerator, v.denominator]


def names(mask, services):
    return [services[i] for i in range(len(services)) if (mask >> i) & 1]


# ---------------------------------------------------------------------------------------------------------------------
# Bản instrument: dựng lại `sets` và `top` đúng như score_services gốc, rồi lưu đóng góp của từng (tập, dịch vụ).
# ---------------------------------------------------------------------------------------------------------------------
def instrumented(patterns, n_services):
    rows = list(patterns.items())
    mask = np.array([k[0] for k, _ in rows], dtype="int64")
    in_m = np.array([k[1] for k, _ in rows], dtype="int64")
    out_m = np.array([k[2] for k, _ in rows], dtype="int64")
    abn = np.array([k[3] for k, _ in rows], dtype=bool)
    cnt = np.array([c for _, c in rows], dtype="int64")
    Y = int(cnt[abn].sum())
    if Y == 0:
        return {"status": "NO_ABNORMAL_TRACE"}
    need = src.MIN_SUPPORT * Y
    sets = []
    amask, acnt = mask[abn], cnt[abn]

    def grow(current, start):
        for s in range(start, n_services):
            cand = current | (1 << s)
            xy = int(acnt[(amask & cand) == cand].sum())
            if xy >= need:
                x = int(cnt[(mask & cand) == cand].sum())
                sets.append((Fraction(xy, x + Y - xy), cand, xy, x))
                grow(cand, s + 1)

    grow(0, 0)
    if not sets:
        return {"status": "NO_FREQUENT_SET"}
    frequent_masks = {z[1] for z in sets}
    sets.sort(key=lambda z: (-z[0], z[1]))
    cut = sets[min(src.TOP_K, len(sets)) - 1][0]
    top = [z for z in sets if z[0] >= cut]
    top_masks = {z[1] for z in top}
    contributions = []                       # theo đúng thứ tự `top`
    for order, (ji, cand, xy, x) in enumerate(top):
        inside = (mask & cand) == cand
        members = []
        for s in range(n_services):
            if not (cand >> s) & 1:
                continue
            bit = 1 << s
            n_in = int(cnt[inside & ((in_m & bit) != 0)].sum())
            n_out = int(cnt[inside & ((out_m & bit) != 0)].sum())
            members.append({"s": s, "n_in": n_in, "n_out": n_out, "value": ji * abs(n_in - n_out)})
        contributions.append({"order": order, "mask": cand, "size": bin(cand).count("1"), "ji": ji, "xy": xy, "x": x, "members": members})

    def best_under(rule):
        scores, best = {}, {}
        for c in contributions:
            if rule == "singleton" and c["size"] != 1:
                continue
            for m in c["members"]:
                s = m["s"]
                if s not in scores or m["value"] > scores[s]:   # cùng phép so nghiêm ngặt và cùng thứ tự như nguồn
                    scores[s] = m["value"]
                    best[s] = {"order": c["order"], "mask": c["mask"], "set_size": c["size"], "ji": c["ji"], "n_in": m["n_in"], "n_out": m["n_out"],
                               "in_set_score": abs(m["n_in"] - m["n_out"])}
        return scores, best

    scores_a, best_a = best_under("all")
    scores_b, best_b = best_under("singleton")
    at_max = {}
    for s, value in scores_a.items():
        sizes = [c["size"] for c in contributions for m in c["members"] if m["s"] == s and m["value"] == value]
        at_max[s] = {"patterns_at_max": len(sizes), "singleton_at_max": 1 in sizes, "sizes_at_max": sorted(Counter(sizes).items())}
    return {"status": "OK", "Y": Y, "traces": int(cnt.sum()), "distinct_patterns": len(rows), "frequent_sets": len(sets), "top_sets": len(top),
            "top_ji_max": top[0][0], "top_ji_min": top[-1][0], "frequent_masks": frequent_masks, "top_masks": top_masks,
            "contributions": contributions, "scores_all": scores_a, "best_all": best_a, "scores_singleton": scores_b, "best_singleton": best_b,
            "at_max": at_max}


# ---------------------------------------------------------------------------------------------------------------------
# Bản tính lại độc lập: chỉ dùng tập hợp Python trên bảng kiểu trace; khai phá kiểu Apriori; không mặt nạ bit, không NumPy.
# ---------------------------------------------------------------------------------------------------------------------
def independent(patterns, n_services):
    types = []
    for (mask, in_mask, out_mask, abnormal), count in patterns.items():
        types.append((frozenset(i for i in range(n_services) if (mask >> i) & 1),
                      frozenset(i for i in range(n_services) if (in_mask >> i) & 1),
                      frozenset(i for i in range(n_services) if (out_mask >> i) & 1), bool(abnormal), int(count)))
    total_abnormal = sum(c for _s, _i, _o, a, c in types if a)
    if total_abnormal == 0:
        return {"status": "NO_ABNORMAL_TRACE"}

    def support(candidate):
        return sum(c for s, _i, _o, a, c in types if a and candidate <= s)

    level = [frozenset([i]) for i in range(n_services) if 10 * support(frozenset([i])) >= total_abnormal]
    frequent = list(level)
    while level:
        known = set(level)
        nxt = set()
        for a in level:
            for i in range(n_services):
                if i in a:
                    continue
                cand = a | {i}
                if cand in nxt:
                    continue
                if all(frozenset(sub) in known for sub in combinations(sorted(cand), len(cand) - 1)) and 10 * support(cand) >= total_abnormal:
                    nxt.add(cand)
        level = list(nxt)
        frequent.extend(level)
    if not frequent:
        return {"status": "NO_FREQUENT_SET"}

    def jaccard(candidate):
        xy = support(candidate)
        x = sum(c for s, _i, _o, _a, c in types if candidate <= s)
        return Fraction(xy, x + total_abnormal - xy)

    ji = {f: jaccard(f) for f in frequent}
    ordered = sorted(ji.values(), reverse=True)
    cut = ordered[min(100, len(ordered)) - 1]
    top = [f for f in frequent if ji[f] >= cut]
    score_all, score_single = {}, {}
    for f in top:
        for s in f:
            n_in = sum(c for sv, i, _o, _a, c in types if f <= sv and s in i)
            n_out = sum(c for sv, _i, o, _a, c in types if f <= sv and s in o)
            value = ji[f] * abs(n_in - n_out)
            if s not in score_all or value > score_all[s]:
                score_all[s] = value
            if len(f) == 1:
                score_single[s] = value
    return {"status": "OK", "frequent": set(frequent), "top": set(top), "scores_all": score_all, "scores_singleton": score_single}


def mask_of(fset):
    out = 0
    for i in fset:
        out |= 1 << i
    return out


# ---------------------------------------------------------------------------------------------------------------------
def fixtures():
    """Ví dụ Hình 2 của bài (cùng bảng kiểu trace với fixture gốc) với giá trị tính tay cho cả hai nhánh, và ba trường hợp gốc."""
    A, B, C, D, E, F = (1 << i for i in range(6))
    p = Counter()
    p[(A | B | D | E, B | D | E, A | B, True)] += 1
    p[(A | B | C | D, B | C | D, A | B, True)] += 1
    p[(A | B | C | E, B | C | E, A | B, True)] += 1
    p[(A | F, 0, 0, False)] += 1
    p[(E | A, 0, 0, False)] += 1
    r = instrumented(p, 6)
    ind = independent(p, 6)
    source_scores, source_info = src.score_services(p, 6)
    hand_all = {0: Fraction(3), 1: Fraction(0), 2: Fraction(4, 3), 3: Fraction(4, 3), 4: Fraction(4, 3)}
    hand_single = {0: Fraction(9, 5), 1: Fraction(0), 2: Fraction(4, 3), 3: Fraction(4, 3), 4: Fraction(1)}
    leaf = Counter({(A | B, B, A, True): 4, (A | C, 0, 0, False): 6})
    rl = instrumented(leaf, 3)
    mid = Counter({(A | B | C, B | C, A | B, True): 5, (A | D, 0, 0, False): 5})
    rm = instrumented(mid, 4)
    none = instrumented(Counter({(A | B, 0, 0, False): 7}), 2)
    checks = {
        "fixture gốc của nguồn đạt": bool(src.fixtures()["pass"]),
        "Hình 2, nhánh all trùng giá trị tính tay": r["scores_all"] == hand_all,
        "Hình 2, nhánh singleton trùng giá trị tính tay": r["scores_singleton"] == hand_single,
        "Hình 2, F không có tập ở cả hai nhánh": 5 not in r["scores_all"] and 5 not in r["scores_singleton"],
        "Hình 2, nhánh all trùng hàm gốc": r["scores_all"] == source_scores,
        "Hình 2, bản độc lập trùng cả hai nhánh": ind["scores_all"] == hand_all and ind["scores_singleton"] == hand_single,
        "Hình 2, pattern quyết định của A ở nhánh all là {A,B}": names(r["best_all"][0]["mask"], list("ABCDEF")) == ["A", "B"],
        "Hình 2, E đổi từ 4/3 xuống 1 khi chỉ chấm singleton": r["scores_all"][4] == Fraction(4, 3) and r["scores_singleton"][4] == Fraction(1),
        "lá chuỗi: hai nhánh cho A và B cùng điểm": rl["scores_all"][0] == rl["scores_all"][1] and rl["scores_singleton"][0] == Fraction(4, 10) * 4 and rl["scores_singleton"][1] == Fraction(4),
        "giữa chuỗi: B có điểm 0 ở cả hai nhánh": rm["scores_all"][1] == 0 and rm["scores_singleton"][1] == 0,
        "không có trace bất thường": none["status"] == "NO_ABNORMAL_TRACE",
        "singleton không vượt all ở mọi dịch vụ": all(r["scores_singleton"][s] <= r["scores_all"][s] for s in r["scores_singleton"]),
    }
    return {"pass": all(checks.values()), "checks": checks,
            "hand_values": {"all": {k: frac(v) for k, v in hand_all.items()}, "singleton": {k: frac(v) for k, v in hand_single.items()}}}


def relation(rank, root, other):
    return "root trên" if rank[root][1] < rank[other][0] else "root dưới" if rank[other][1] < rank[root][0] else "hòa"


def source_view(computed, item, root, labels_row):
    """Chép đúng phần dựng `view` của main() gốc để so với cases.json cũ."""
    root_callers = computed["callers_by_service"].get(root, [])
    for name, b in computed["branches"].items():
        view = {k: v for k, v in b.items() if k not in ("scores", "best")}
        if b.get("status") == "OK":
            scores = {s: Fraction(*b["scores"][s]) if s in b["scores"] else Fraction(0) for s in computed["services"]}
            rank = src.rank_of(scores)
            view["n_entities"] = len(rank)
            view["positive_scores"] = sum(v > 0 for v in scores.values())
            if root in rank:
                view.update(root_in_spans=True, root_score_positive=scores[root] > 0, root_rank_min=rank[root][0], root_rank_max=rank[root][1],
                            above=sorted(e for e in rank if e != root and rank[e][1] < rank[root][0]), root_best=b["best"].get(root))
            else:
                view["root_in_spans"] = False
            view["top"] = sorted(e for e in rank if rank[e][0] == 1)
            view["top_best"] = {e: b["best"].get(e) for e in view["top"][:3]}
            if root in rank:
                view["root_vs_direct_callers"] = {c: relation(rank, root, c) for c in root_callers if c in rank}
                view["root_vs_waiting_callers_library"] = {c: relation(rank, root, c) for c in item["waiting_callers_library"] if c in rank}
        item["branches"][name] = view
    return item


def diff(a, b, path=""):
    if type(a) is not type(b):
        return [{"path": path, "old": repr(a)[:120], "new": repr(b)[:120], "kind": "type"}]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append({"path": path + "/" + k, "kind": "missing", "in_old": k in a, "in_new": k in b})
            else:
                out += diff(a[k], b[k], path + "/" + k)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [{"path": path, "kind": "length", "old": len(a), "new": len(b)}]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, path + "/" + str(i))
        return out
    return [] if a == b else [{"path": path, "kind": "value", "old": a, "new": b}]


def main():
    out = Path(sys.argv[1])
    ledger_path = Path(sys.argv[2])
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    began_all = time.time()
    pins = {k: sha(BASE / k) for k in PINS}
    pins_ok = pins == PINS and sha(ledger_path) == LEDGER_SHA
    environment = {"python": sys.version, "numpy": np.__version__, "pandas": pd.__version__, "platform": platform.platform(),
                   "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"), "PYTHONPATH": os.environ.get("PYTHONPATH"), "argv": sys.argv,
                   "source_module_file": src.__file__, "self_sha256": sha(__file__), "pins": pins, "pins_expected": PINS, "pins_ok": pins_ok,
                   "ledger_sha256": sha(ledger_path), "utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (out / "environment.json").write_text(json.dumps(environment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not pins_ok:
        raise SystemExit("mã băm nguồn không khớp bản ghim; dừng")
    fx = fixtures()
    (out / "fixtures.json").write_text(json.dumps(fx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not fx["pass"]:
        raise SystemExit("fixture không đạt: " + json.dumps(fx["checks"], ensure_ascii=False))

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    declared = ledger["h6_pair_audit"]["pairs"]
    wanted = []
    for p in declared:
        key = (p["dataset"], p["opaque_id"])
        if key not in wanted:
            wanted.append(key)
    old_cases = {(c["dataset"], c["opaque_id"]): c for c in td.read(BASE / "runs/tracerca-original-ranking-001/cases.json")["cases"]}

    # --- nạp nguồn đúng như main() gốc ---
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    labels = {(r["dataset"], r["opaque_id"]): r for r in cp.read(cp.LABELS)["main_rows"] if r["method"] == "tracerca"}
    waiting = {}
    for c in cp.read(BASE / "runs/slow-call-flag-link-001/cases.json"):
        if c["method"] == "tracerca" and c.get("root_ranked") and c.get("root_edge_measurable"):
            got = [e["entity"] for e in c["entities"] if e["above_root"] and e["class"] in ("goi_truc_tiep", "phia_tren_gian_tiep", "hai_chieu")
                   and "span" in e and (e["span"]["share_r50"] or 0) >= 0.5]
            if got:
                waiting[(c["dataset"], c["opaque_id"])] = got

    progress = (out / "progress.jsonl").open("a", encoding="utf-8")
    summary_cases, pair_rows = [], []
    original_score = src.score_services
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if (dataset, opaque_id) not in wanted or (only and only != dataset + ":" + opaque_id):
            continue
        began = time.time()
        if row["source_status"] == "OK":
            directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
            adapter = td.read(directory / "capture/calls/001-adapter.json")
            spans = pd.DataFrame(table_columns(directory / "capture", adapter["entry"]["input"]))
            t = int(adapter["entry"]["t_seconds"])
            source_kind = "capture"
        else:
            entry = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == opaque_id][0]
            t = int(td.read(BASE / "repo" / entry["path"])["window"]["t"])
            files = selector.chon_ca(allow, opaque_id, Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
            spans = cua_so.cat_span(pd.read_parquet(files["traces.parquet"]), t)
            source_kind = "parquet"
        captured = []

        def recorder(patterns, n_services, _captured=captured):
            _captured.append((Counter(patterns), n_services))     # bản sao: nhánh đổi nhận đúng bảng mà hàm gốc nhận
            return original_score(patterns, n_services)

        src.score_services = recorder
        try:
            computed = src.one_case(spans, t * 1_000_000)          # mã nguồn, chưa dùng nhãn
        finally:
            src.score_services = original_score
        t_source = time.time() - began
        services = computed["services"]
        label = labels[(dataset, opaque_id)]
        root = label["root"]
        item = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": label["fault"], "cell": label["cell"], "library_status": label["status"],
                "library_rank": [label.get("rank_min"), label.get("rank_max")], "invocations": computed["invocations"], "branches": {}}
        item["root_callers"] = computed["callers_by_service"].get(root, [])
        item["waiting_callers_library"] = waiting.get((dataset, opaque_id), [])
        new_item = json.loads(json.dumps(source_view(computed, item, root, label), ensure_ascii=False))
        old_item = {k: v for k, v in old_cases[(dataset, opaque_id)].items() if k != "wall_s"}
        sham_diff = diff(old_item, new_item)

        useful = [n for n in BRANCH_ORDER if computed["branches"][n].get("status") != "NO_USEFUL_FEATURE"]
        assert len(useful) == len(captured), "số lần gọi score_services không khớp số nhánh có đặc trưng"
        case_out = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": label["fault"], "t_seconds": t, "source_kind": source_kind,
                    "span_rows": int(len(spans)), "services": services, "sham": {"equal": not sham_diff, "differences": sham_diff[:50], "n_differences": len(sham_diff)},
                    "branches": {}}
        for name in BRANCH_ORDER:
            status = computed["branches"][name].get("status")
            if name not in useful:
                case_out["branches"][name] = {"status": status}
                continue
            patterns, n_services = captured[useful.index(name)]
            b = computed["branches"][name]
            if status != "OK":
                case_out["branches"][name] = {"status": status}
                continue
            ins = instrumented(patterns, n_services)
            ind = independent(patterns, n_services)
            source_scores = {services.index(s): Fraction(*v) for s, v in b["scores"].items()}
            source_best = {services.index(s): v for s, v in b["best"].items()}
            inst_best_view = {s: {"set_size": v["set_size"], "ji": float(v["ji"]), "n_in": v["n_in"], "n_out": v["n_out"], "in_set_score": v["in_set_score"]}
                              for s, v in ins["best_all"].items()}
            checks = {
                "A_scores_equal_source": ins["scores_all"] == source_scores,
                "A_best_equal_source": inst_best_view == source_best,
                "frequent_sets_equal_source": ins["frequent_sets"] == b["frequent_sets"],
                "top_sets_equal_source": ins["top_sets"] == b["top_sets"],
                "top_ji_equal_source": float(ins["top_ji_max"]) == b["top_ji_max"] and float(ins["top_ji_min"]) == b["top_ji_min"],
                "trace_counts_equal_source": ins["traces"] == b["traces"] and ins["Y"] == b["abnormal_traces"] and ins["distinct_patterns"] == b["distinct_patterns"],
                "independent_frequent_equal": {mask_of(f) for f in ind["frequent"]} == ins["frequent_masks"],
                "independent_top_equal": {mask_of(f) for f in ind["top"]} == ins["top_masks"],
                "independent_A_scores_equal": ind["scores_all"] == ins["scores_all"],
                "independent_B_scores_equal": ind["scores_singleton"] == ins["scores_singleton"],
                "B_not_above_A": all(ins["scores_singleton"][s] <= ins["scores_all"][s] for s in ins["scores_singleton"]),
                "B_services_subset_of_A": set(ins["scores_singleton"]) <= set(ins["scores_all"]),
            }
            full_a = {s: ins["scores_all"].get(i, Fraction(0)) for i, s in enumerate(services)}
            full_b = {s: ins["scores_singleton"].get(i, Fraction(0)) for i, s in enumerate(services)}
            rank_a, rank_b = src.rank_of(full_a), src.rank_of(full_b)
            per_service = {}
            for i, s in enumerate(services):
                single_mask = 1 << i
                in_a, in_b = i in ins["scores_all"], i in ins["scores_singleton"]
                ba = ins["best_all"].get(i)
                per_service[s] = {
                    "score_all": frac(full_a[s]), "score_singleton": frac(full_b[s]),
                    "evidence_all": "scored" if in_a else "no_pattern",
                    "evidence_singleton": "scored" if in_b else ("lost" if in_a else "no_pattern"),
                    "singleton_frequent": single_mask in ins["frequent_masks"], "singleton_in_top": single_mask in ins["top_masks"],
                    "rank_all": list(rank_a[s]), "rank_singleton": list(rank_b[s]),
                    "deciding_all": None if ba is None else {"members": names(ba["mask"], services), "set_size": ba["set_size"], "ji": frac(ba["ji"]),
                                                              "n_in": ba["n_in"], "n_out": ba["n_out"], "top_order": ba["order"], **{k: v for k, v in ins["at_max"][i].items()}},
                    "deciding_singleton": None if not in_b else {"ji": frac(ins["best_singleton"][i]["ji"]), "n_in": ins["best_singleton"][i]["n_in"],
                                                                 "n_out": ins["best_singleton"][i]["n_out"], "top_order": ins["best_singleton"][i]["order"]},
                }
            top_sets = [{"order": c["order"], "members": names(c["mask"], services), "size": c["size"], "ji": frac(c["ji"]), "xy": c["xy"], "x": c["x"],
                         "per_member": [{"service": services[m["s"]], "n_in": m["n_in"], "n_out": m["n_out"], "value": frac(m["value"])} for m in c["members"]]}
                        for c in ins["contributions"]]
            trace_types = [{"services": names(k[0], services), "in": names(k[1], services), "out": names(k[2], services), "abnormal": bool(k[3]), "count": int(c)}
                           for k, c in patterns.items()]
            in_spans = root in rank_a
            branch_out = {"status": "OK", "feature": b["feature"], "threshold_sigma": b["threshold_sigma"], "traces": ins["traces"], "abnormal_traces": ins["Y"],
                          "distinct_trace_types": ins["distinct_patterns"], "frequent_sets": ins["frequent_sets"], "top_sets": ins["top_sets"],
                          "top_size_histogram": sorted(Counter(c["size"] for c in ins["contributions"]).items()),
                          "top_ji_max": frac(ins["top_ji_max"]), "top_ji_min": frac(ins["top_ji_min"]), "checks": checks, "checks_pass": all(checks.values()),
                          "n_services": len(services), "coverage_all": sum(v["evidence_all"] == "scored" for v in per_service.values()),
                          "coverage_singleton": sum(v["evidence_singleton"] == "scored" for v in per_service.values()),
                          "lost_evidence": sorted(s for s, v in per_service.items() if v["evidence_singleton"] == "lost"),
                          "root_in_spans": in_spans,
                          "top_all": sorted(e for e in rank_a if rank_a[e][0] == 1), "top_singleton": sorted(e for e in rank_b if rank_b[e][0] == 1),
                          "root_rank_all": list(rank_a[root]) if in_spans else None, "root_rank_singleton": list(rank_b[root]) if in_spans else None,
                          "services_changed_score": sorted(s for s in services if full_a[s] != full_b[s]),
                          "services_changed_rank": sorted(s for s in services if rank_a[s] != rank_b[s]),
                          "per_service": per_service, "top_sets_detail": top_sets, "trace_types": trace_types}
            case_out["branches"][name] = branch_out
        # --- các cặp đã khai ---
        for p in declared:
            if (p["dataset"], p["opaque_id"]) != (dataset, opaque_id):
                continue
            assert p["root"] == root, "root của ledger khác nhãn"
            for name in BRANCH_ORDER:
                bo = case_out["branches"][name]
                rowp = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "caller": p["caller"], "branch": name, "status": bo["status"],
                        "old_relation_ledger_to_p": p["old_relation"], "old_status_ledger": p["old_status"]}
                if bo["status"] == "OK" and bo["root_in_spans"] and p["caller"] in bo["per_service"]:
                    r, c = bo["per_service"][root], bo["per_service"][p["caller"]]
                    ra = {root: tuple(r["rank_all"]), p["caller"]: tuple(c["rank_all"])}
                    rb = {root: tuple(r["rank_singleton"]), p["caller"]: tuple(c["rank_singleton"])}
                    rowp.update(relation_all=relation(ra, root, p["caller"]), relation_singleton=relation(rb, root, p["caller"]),
                                root_score_all=r["score_all"], caller_score_all=c["score_all"], root_score_singleton=r["score_singleton"],
                                caller_score_singleton=c["score_singleton"], root_evidence_all=r["evidence_all"], caller_evidence_all=c["evidence_all"],
                                root_evidence_singleton=r["evidence_singleton"], caller_evidence_singleton=c["evidence_singleton"],
                                root_rank_all=r["rank_all"], root_rank_singleton=r["rank_singleton"], caller_rank_all=c["rank_all"],
                                caller_rank_singleton=c["rank_singleton"],
                                caller_deciding_all=c["deciding_all"], root_deciding_all=r["deciding_all"],
                                caller_deciding_singleton=c["deciding_singleton"], root_deciding_singleton=r["deciding_singleton"])
                pair_rows.append(rowp)
        wall = time.time() - began
        case_out["cost"] = {"wall_s": round(wall, 3), "source_one_case_s": round(t_source, 3), "ru_maxrss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        text = json.dumps(case_out, ensure_ascii=False, indent=1) + "\n"
        path = out / "cases" / (dataset + "--" + opaque_id + ".json")
        path.write_text(text, encoding="utf-8")
        brief = {"dataset": dataset, "opaque_id": opaque_id, "sham_equal": case_out["sham"]["equal"], "n_sham_differences": case_out["sham"]["n_differences"],
                 "branches": {n: (v["status"], v.get("checks_pass"), v.get("root_rank_all"), v.get("root_rank_singleton"), v.get("coverage_all"), v.get("coverage_singleton"))
                              for n, v in case_out["branches"].items()}, "wall_s": round(wall, 3),
                 "ru_maxrss_kb": case_out["cost"]["ru_maxrss_kb"], "bytes": len(text.encode("utf-8")), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        progress.write(json.dumps(brief, ensure_ascii=False) + "\n")
        progress.flush()
        print(json.dumps(brief, ensure_ascii=False), flush=True)
        summary_cases.append(brief)
    progress.close()
    all_sham = all(c["sham_equal"] for c in summary_cases)
    all_checks = all(v[1] is not False for c in summary_cases for v in c["branches"].values())
    summary = {"schema": "T034-E1-pattern-rule-v1", "design": "results/T-034/thiet-ke-hai-phep-kiem.md, E1", "fixtures_pass": fx["pass"],
               "declared_pairs": len(declared), "declared_cases": len(wanted), "cases_done": len(summary_cases), "sham_all_equal": all_sham,
               "instrument_checks_all_pass": all_checks, "interpretable": bool(fx["pass"] and all_sham and all_checks and len(summary_cases) == len(wanted)),
               "cases": summary_cases, "pairs": pair_rows, "wall_s_total": round(time.time() - began_all, 3),
               "ru_maxrss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "utc_end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("XONG", len(summary_cases), "sham_all_equal", all_sham, "checks", all_checks, "interpretable", summary["interpretable"], flush=True)


if __name__ == "__main__":
    main()

"""T-032 bản 012 mục 3 (KT-15): bước DA của CIRCA cộng gì, cho nút nào. Chạy trên laptop, chỉ đọc.

Đọc trung gian đã lưu của nhánh quan sát (runs/circa-laptop-k2-001/cases/RE2-TT/*/obs/score-graph.json.gz). Không chạy phương pháp.
Nhãn root nối ở cuối, chỉ để in riêng các thực thể đứng trên root.
Dùng: py -3 -B -X utf8 scripts/circa_da_addition_v1.py <thư mục tổng hợp mới>
"""
import gzip
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
BASE = REPO / "results/T-032"
RUN = BASE / "runs/circa-laptop-k2-001"
COLLECT = RUN / "collect-001/summary.json"
THRESHOLD = 3.0


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def service_of(node):
    return node.rsplit("_", 1)[0]


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else None


def reach(start, nxt, score):
    """Theo mã CIRCA: lấy điểm các nút kề; nút kề dưới ngưỡng thì chuyển tiếp các nút kề của nó."""
    out, stack, seen = {}, list(nxt.get(start, ())), set()
    while stack:
        c = stack.pop()
        if c in seen or c not in score:
            continue
        seen.add(c)
        out[c] = score[c]
        if score[c] < THRESHOLD:
            stack.extend(nxt.get(c, ()))
    return out


def descendants(start, nxt):
    seen, stack = set(), list(nxt.get(start, ()))
    while stack:
        c = stack.pop()
        if c not in seen:
            seen.add(c)
            stack.extend(nxt.get(c, ()))
    return seen


def one(path, meta):
    d = json.load(gzip.open(path, "rt", encoding="utf-8"))
    own = {n: v["rht_score"] for n, v in d["nodes"].items()}
    da = d["da"]
    succ, pred = defaultdict(list), defaultdict(list)
    for u, v in d["graph"]["edges"]:
        succ[u].append(v)
        pred[v].append(u)
    added_nodes = {n: v for n, v in da.items() if v.get("child_score") is not None}
    ident = sum(abs(v["score"] - (own[n] + v["child_score"])) <= 1e-6 * max(1.0, abs(v["score"])) for n, v in added_nodes.items())
    unchanged = sum(abs(v["score"] - own[n]) <= 1e-9 * max(1.0, abs(own[n])) for n, v in da.items() if v.get("child_score") is None)
    # hướng "con" của CIRCA: thử cả hai chiều cạnh, chọn chiều mà max của tập với tới bằng child_score ở nhiều nút hơn
    match = {}
    for name, nxt in (("theo_chieu_canh", succ), ("nguoc_chieu_canh", pred)):
        ok = 0
        for n, v in added_nodes.items():
            r = reach(n, nxt, own)
            if r and abs(max(r.values()) - v["child_score"]) <= 1e-6 * max(1.0, abs(v["child_score"])):
                ok += 1
        match[name] = ok
    direction = max(match, key=match.get)
    nxt = succ if direction == "theo_chieu_canh" else pred
    rows = []
    for n, v in added_nodes.items():
        r = reach(n, nxt, own)
        source = max(r, key=r.get) if r else None
        rows.append({"node": n, "service": service_of(n), "own": own[n], "added": v["child_score"], "n_children": len(nxt.get(n, ())),
                     "n_descendants": len(descendants(n, nxt)), "source": source,
                     "source_matches": bool(source) and abs(r[source] - v["child_score"]) <= 1e-6 * max(1.0, abs(v["child_score"]))})
    values = Counter(round(r["added"], 6) for r in rows)
    top_value, top_n = values.most_common(1)[0] if values else (None, 0)
    top_sources = Counter(r["source"] for r in rows if round(r["added"], 6) == top_value)
    eligible = [n for n in da if own[n] >= THRESHOLD]
    rho = spearman([r["n_descendants"] for r in rows], [r["added"] for r in rows])
    by_service_added = defaultdict(float)
    for r in rows:
        by_service_added[r["service"]] = max(by_service_added[r["service"]], r["added"])
    root = meta["root"]
    above_da = [x if isinstance(x, str) else x.get("entity") for x in meta["views"]["native_da"].get("above_root") or []]
    above_rht = {x if isinstance(x, str) else x.get("entity") for x in meta["views"]["native_rht"].get("above_root") or []}
    best = {}
    for n, v in da.items():
        s = service_of(n)
        if s not in best or v["score"] > best[s]["da_score"]:
            best[s] = {"node": n, "da_score": v["score"], "own": own[n], "added": v.get("child_score")}
    src_of = {r["node"]: r["source"] for r in rows}
    above_detail = [{"entity": e, "newly_above_after_DA": e not in above_rht, **best.get(e, {}), "source": src_of.get(best.get(e, {}).get("node"))} for e in above_da]
    return {"opaque_id": meta["opaque_id"], "cell": meta["cell"], "root": root, "has_huge_node": meta["has_huge_node"],
            "root_rank": {"RHT": meta["views"]["native_rht"]["root_rank_min"], "DA": meta["views"]["native_da"]["root_rank_min"]},
            "nodes": len(da), "nodes_score_ge_threshold": len(eligible), "nodes_with_added": len(rows),
            "identity_da_equals_own_plus_child": ident, "nodes_without_added_unchanged": unchanged, "nodes_without_added": len(da) - len(rows),
            "child_direction": direction, "child_direction_match": match, "source_matches": sum(r["source_matches"] for r in rows),
            "distinct_added_values": len(values), "top_added_value": top_value, "nodes_receiving_top_value": top_n,
            "share_receiving_top_value": top_n / len(rows) if rows else None, "top_value_sources": dict(top_sources),
            "top_value_over_root_best_own": (top_value / best[root]["own"]) if rows and root in best and best[root]["own"] else None,
            "spearman_descendants_vs_added": rho,
            "added_by_n_descendants": {str(k): {"n": len(v), "median_added": statistics.median(v)} for k, v in sorted(
                (lambda g: g)({k: [r["added"] for r in rows if r["n_descendants"] == k] for k in sorted({r["n_descendants"] for r in rows})}).items())},
            "root_best": best.get(root), "root_n_descendants": max((len(descendants(n, nxt)) for n in da if service_of(n) == root), default=None),
            "above_root_after_DA": above_detail,
            "above_newly_after_DA_receiving_top_value": sum(1 for a in above_detail if a["newly_above_after_DA"] and a.get("added") is not None
                                                             and round(a["added"], 6) == top_value),
            "above_newly_after_DA": sum(1 for a in above_detail if a["newly_above_after_DA"]),
            "source_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    collect = read(COLLECT)
    cases = []
    for meta in collect["cases"]:
        path = RUN / "cases/RE2-TT" / meta["opaque_id"] / "obs/score-graph.json.gz"
        cases.append(one(path, meta))
    nh = [c for c in cases if not c["has_huge_node"]]
    hh = [c for c in cases if c["has_huge_node"]]

    def block(rows):
        with_added = [c for c in rows if c["nodes_with_added"]]
        rhos = [c["spearman_descendants_vs_added"] for c in with_added if c["spearman_descendants_vs_added"] is not None]
        return {"cases": len(rows), "cases_with_added_nodes": len(with_added),
                "cases_majority_receive_one_value": sum(c["share_receiving_top_value"] > 0.5 for c in with_added),
                "share_receiving_top_value": {"min": min((c["share_receiving_top_value"] for c in with_added), default=None),
                                              "median": statistics.median([c["share_receiving_top_value"] for c in with_added]) if with_added else None,
                                              "max": max((c["share_receiving_top_value"] for c in with_added), default=None)},
                "spearman": {"n": len(rhos), "min": min(rhos, default=None), "median": statistics.median(rhos) if rhos else None, "max": max(rhos, default=None),
                             "positive": sum(r > 0 for r in rhos), "negative": sum(r < 0 for r in rhos)},
                "top_value_source_services": dict(Counter(service_of(s) for c in with_added for s in c["top_value_sources"] if s).most_common(8)),
                "nodes_with_added_total": sum(c["nodes_with_added"] for c in rows),
                "identity_ok_total": sum(c["identity_da_equals_own_plus_child"] for c in rows),
                "source_matches_total": sum(c["source_matches"] for c in rows),
                "child_direction": dict(Counter(c["child_direction"] for c in with_added))}
    summary = {"all": block(cases), "khong_co_nut_cuc_lon": block(nh), "co_nut_cuc_lon": block(hh),
               "self_check": {"identity_da_equals_own_plus_child": [sum(c["identity_da_equals_own_plus_child"] for c in cases), sum(c["nodes_with_added"] for c in cases)],
                              "nodes_without_added_unchanged": [sum(c["nodes_without_added_unchanged"] for c in cases), sum(c["nodes_without_added"] for c in cases)]},
               "da_lowers_root_without_huge": [{"opaque_id": c["opaque_id"], "cell": c["cell"], "root_rank": c["root_rank"], "root_best": c["root_best"],
                                                "root_n_descendants": c["root_n_descendants"], "top_added_value": c["top_added_value"],
                                                "top_value_sources": c["top_value_sources"], "share_receiving_top_value": c["share_receiving_top_value"],
                                                "above_newly_after_DA": c["above_newly_after_DA"],
                                                "above_newly_after_DA_receiving_top_value": c["above_newly_after_DA_receiving_top_value"]}
                                               for c in nh if c["root_rank"]["DA"] > c["root_rank"]["RHT"]],
               "da_raises_root_without_huge": [{"opaque_id": c["opaque_id"], "cell": c["cell"], "root_rank": c["root_rank"], "root_best": c["root_best"],
                                                "root_n_descendants": c["root_n_descendants"], "top_added_value": c["top_added_value"],
                                                "top_value_sources": c["top_value_sources"]} for c in nh if c["root_rank"]["DA"] < c["root_rank"]["RHT"]]}
    result = {"schema": "T032-circa-da-addition-v1", "design": "results/T-032/thiet-ke-phep-doi-012.md mục 3", "threshold": THRESHOLD,
              "sources": {"collect": str(COLLECT.relative_to(REPO).as_posix()), "collect_sha256": hashlib.sha256(COLLECT.read_bytes()).hexdigest()},
              "summary": summary, "cases": cases, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary["self_check"], ensure_ascii=False))
    for k in ("khong_co_nut_cuc_lon", "co_nut_cuc_lon"):
        print(k, json.dumps(summary[k], ensure_ascii=False))
    for x in summary["da_lowers_root_without_huge"]:
        print("DA hại:", json.dumps(x, ensure_ascii=False))
    for x in summary["da_raises_root_without_huge"]:
        print("DA giúp:", json.dumps(x, ensure_ascii=False))


if __name__ == "__main__":
    main()

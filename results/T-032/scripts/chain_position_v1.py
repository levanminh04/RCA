"""T-032 bản 008 mục 3 (việc 1): thực thể đứng trên root nằm đâu so với chuỗi gọi, kèm tỷ lệ nền. Chạy trên EC2, chỉ đọc.

Nguồn thứ hạng: 372 bản ghi đóng băng mà ca-sai.json của T-028 trỏ tới; đồ thị gọi theo ca từ lượt chain-spanpass.
Không gọi phương pháp, không chấm Hit mới. Tự kiểm: hạng root tính lại phải trùng hạng T-028 ở mọi bản ghi OK.
Dùng: python chain_position_v1.py <thư mục lượt spanpass> <thư mục lượt mới>
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
INDEX = REPO / "results/T-024/ban-ghi-dua-vao-cham.json"
CALLER_ROOT = BASE / "runs/caller-root-phien9-001/caller-root.json"
CLASSES = ("goi_truc_tiep", "phia_tren_gian_tiep", "hai_chieu", "duoc_goi_truc_tiep", "phia_duoi_gian_tiep", "chung_phia_tren", "roi", "khong_co_span")
GROUPS = {"phia_tren": ("goi_truc_tiep", "phia_tren_gian_tiep"), "hai_chieu": ("hai_chieu",),
          "phia_duoi": ("duoc_goi_truc_tiep", "phia_duoi_gian_tiep"), "khong_lien_he": ("chung_phia_tren", "roi"), "khong_co_span": ("khong_co_span",)}
DRAWS, SEED = 20000, 20261011


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ranks_of(record, method):
    """(rank_min, rank_max) theo giao thức P3. TORAI: khối rồi nhóm trong khối. Phương pháp khác: nhóm hòa theo tie_group."""
    out, offset = {}, 0
    if method.startswith("torai"):
        for block in record["blocks"]:
            for group in block["groups"]:
                for entity in group:
                    out[entity] = (offset + 1, offset + len(group))
                offset += len(group)
        return out
    groups = defaultdict(list)
    order = []
    for row in record["entity_ranking"]:
        if row["tie_group"] not in groups:
            order.append(row["tie_group"])
        groups[row["tie_group"]].append(row["entity"])
    for g in order:
        for entity in groups[g]:
            out[entity] = (offset + 1, offset + len(groups[g]))
        offset += len(groups[g])
    return out


class Graph:
    def __init__(self, services, edges):
        self.nodes = set(services)
        self.out = defaultdict(set)
        for a, b in edges:
            self.out[a].add(b)
        self.edges = set(edges)
        self._reach = {}

    def reach(self, a):
        """{nút: khoảng cách ngắn nhất} với đường đi từ a, độ dài từ 1."""
        if a not in self._reach:
            dist, frontier, d = {}, [a], 0
            while frontier:
                d += 1
                nxt = []
                for u in frontier:
                    for v in self.out[u]:
                        if v not in dist:
                            dist[v] = d
                            nxt.append(v)
                frontier = nxt
            self._reach[a] = dist
        return self._reach[a]

    def position(self, e, r):
        if e not in self.nodes:
            return {"class": "khong_co_span"}
        if r not in self.nodes:
            return {"class": "root_khong_co_span"}
        up, down = self.reach(e).get(r), self.reach(r).get(e)
        info = {"dist_up": up, "dist_down": down}
        if up and down:
            info["class"] = "hai_chieu"
        elif up == 1:
            info["class"] = "goi_truc_tiep"
        elif up:
            info["class"] = "phia_tren_gian_tiep"
        elif down == 1:
            info["class"] = "duoc_goi_truc_tiep"
        elif down:
            info["class"] = "phia_duoi_gian_tiep"
        elif any(e in self.reach(a) and r in self.reach(a) for a in self.nodes):
            info["class"] = "chung_phia_tren"
        else:
            info["class"] = "roi"
        return info


def fixtures():
    g = Graph(["a", "b", "c", "d", "e", "f", "g", "h"], [("a", "b"), ("b", "c"), ("c", "d"), ("a", "e"), ("f", "g"), ("c", "b")])
    want = {("a", "c"): "phia_tren_gian_tiep", ("b", "c"): "hai_chieu", ("d", "c"): "duoc_goi_truc_tiep", ("e", "c"): "chung_phia_tren",
            ("f", "c"): "roi", ("h", "c"): "roi", ("x", "c"): "khong_co_span", ("a", "b"): "goi_truc_tiep", ("d", "b"): "phia_duoi_gian_tiep",
            ("a", "d"): "phia_tren_gian_tiep", ("g", "f"): "duoc_goi_truc_tiep", ("e", "a"): "duoc_goi_truc_tiep"}
    got = {k: g.position(*k)["class"] for k in want}
    rec = {"entity_ranking": [{"entity": "p", "tie_group": 0}, {"entity": "q", "tie_group": 1}, {"entity": "r", "tie_group": 1}, {"entity": "s", "tie_group": 2}]}
    rk = ranks_of(rec, "baro")
    tor = ranks_of({"blocks": [{"groups": [["p"], ["q", "r"]]}, {"groups": [["s"]]}]}, "torai_B")
    ok_rank = rk == {"p": (1, 1), "q": (2, 3), "r": (2, 3), "s": (4, 4)} and tor == rk
    return {"pass": got == want and ok_rank, "position": {a + ">" + b: v for (a, b), v in got.items()}, "rank_ok": ok_rank}


def unit_rows(spanpass):
    labels = read(LABELS)["main_rows"]
    graphs = {}

    def graph_of(dataset, opaque_id, baseline_only=False):
        key = (dataset, opaque_id, baseline_only)
        if key not in graphs:
            case = read(spanpass / "cases" / (dataset + "-" + opaque_id + ".json"))
            edges = [(e["caller"], e["callee"]) for e in case["edges"].values() if (e["n_before"] > 0 or not baseline_only)]
            graphs[key] = Graph(case["services"], edges)
        return graphs[key]

    def build(dataset, method, opaque_id, row, record, seed, reference_rank):
        base = {"dataset": dataset, "method": method, "seed": seed, "opaque_id": opaque_id, "root": row["root"], "fault": row["fault"], "cell": row["cell"]}
        if record.get("status") != "OK":
            return {**base, "status": record.get("status")}
        rank = ranks_of(record, method)
        root = row["root"]
        if root not in rank:
            return {**base, "status": "OK", "root_ranked": False, "n_candidates": len(rank)}
        g, g0 = graph_of(dataset, opaque_id), graph_of(dataset, opaque_id, True)
        cand = [e for e in rank if e != root]
        pos = {e: g.position(e, root) for e in cand}
        pos0 = {e: g0.position(e, root)["class"] for e in cand}
        above = sorted((e for e in cand if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
        top = sorted(rank, key=lambda e: rank[e][0])[0] if rank[root][1] > 1 else None
        top1 = [e for e in cand if rank[e][0] == 1] if rank[root][0] > 1 else []
        return {**base, "status": "OK", "root_ranked": True, "root_rank": list(rank[root]),
                "self_check_rank_equals_reference": (list(rank[root]) == list(reference_rank)) if reference_rank is not None else None,
                "n_candidates": len(cand), "candidates_by_class": dict(Counter(pos[e]["class"] for e in cand)),
                "n_above": len(above), "above_by_class": dict(Counter(pos[e]["class"] for e in above)),
                "above": [{"entity": e, "rank_min": rank[e][0], **pos[e], "class_baseline_graph": pos0[e]} for e in above],
                "top1_when_root_not_first": [{"entity": e, **pos[e]} for e in top1], "top_entity": top,
                "graph": {"nodes": len(g.nodes), "edges": len(g.edges), "edges_baseline_only": len(g0.edges)}}

    units = []
    for row in labels:
        dataset, method, opaque_id = row["dataset"], row["method"], row["opaque_id"]
        for ref in row["source"]["records"]:
            seed = None if ref.get("seed") in (None, "None") else str(ref["seed"])
            if row["status"] not in ("OK",) and ref.get("status") != "OK":
                units.append({"dataset": dataset, "method": method, "seed": seed, "opaque_id": opaque_id, "root": row["root"], "fault": row["fault"],
                              "cell": row["cell"], "status": ref.get("status") or row["status"]})
                continue
            record = read(REPO / ref["path"])
            metrics = (row.get("seed_metrics") or {}).get(seed if seed is not None else "single")
            if metrics is None and seed is None:  # dòng Nezha-OB của T-028 không có seed_metrics; hạng nằm ở cấp dòng
                metrics = {"rank_min": row.get("rank_min"), "rank_max": row.get("rank_max")}
            reference = (metrics["rank_min"], metrics["rank_max"]) if metrics and metrics.get("rank_min") is not None else None
            units.append(build(dataset, method, opaque_id, row, record, seed, reference))
    # góc nhìn phụ: CIRCA không có DA
    without_da = {r["opaque_id"]: r.get("root_rank_without_da") for r in read(CALLER_ROOT)["methods"]["circa"]}
    circa_rows = {r["opaque_id"]: r for r in labels if r["dataset"] == "RE2-TT" and r["method"] == "circa_ols_da"}
    for ref in read(INDEX)["records"]:
        if ref["method"] == "circa" and ref["variant"] == "ols+rht":
            row = circa_rows[ref["opaque_id"]]
            units.append(build("RE2-TT", "circa_ols_rht_khong_DA", ref["opaque_id"], row, read(REPO / ref["path"]), None, without_da.get(ref["opaque_id"])))
    return units


def tally(units, rng):
    ok = [u for u in units if u.get("status") == "OK" and u.get("root_ranked")]
    out = {"units": len(units), "status": dict(Counter(u.get("status") for u in units)), "units_ok_root_ranked": len(ok),
           "units_root_rank1": sum(u["root_rank"][1] == 1 for u in ok), "units_with_above": sum(u["n_above"] > 0 for u in ok),
           "pairs_above": sum(u["n_above"] for u in ok), "above_by_class": {c: 0 for c in CLASSES}, "candidates_by_class": {c: 0 for c in CLASSES},
           "expected_above_by_class": {c: 0.0 for c in CLASSES}}
    for u in ok:
        for c, n in u["above_by_class"].items():
            out["above_by_class"][c] = out["above_by_class"].get(c, 0) + n
        for c, n in u["candidates_by_class"].items():
            out["candidates_by_class"][c] = out["candidates_by_class"].get(c, 0) + n
            out["expected_above_by_class"][c] = out["expected_above_by_class"].get(c, 0.0) + u["n_above"] * n / u["n_candidates"]
    groups = dict(GROUPS)
    groups["phia_tren_ke_ca_hai_chieu"] = GROUPS["phia_tren"] + GROUPS["hai_chieu"]
    out["groups"] = {}
    for name, classes in groups.items():
        observed = sum(out["above_by_class"].get(c, 0) for c in classes)
        expected = sum(out["expected_above_by_class"].get(c, 0.0) for c in classes)
        total = np.zeros(DRAWS, dtype="int64")
        for u in ok:
            if u["n_above"] == 0:
                continue
            good = sum(u["candidates_by_class"].get(c, 0) for c in classes)
            if good:
                total += rng.hypergeometric(good, u["n_candidates"] - good, u["n_above"], size=DRAWS)
        out["groups"][name] = {"observed": observed, "expected": expected, "ratio": (observed / expected) if expected > 0 else None,
                               "candidates": sum(out["candidates_by_class"].get(c, 0) for c in classes),
                               "random_draw_share_ge_observed": float((total >= observed).mean()),
                               "random_draw_share_le_observed": float((total <= observed).mean())}
    wrong = [u for u in ok if u["root_rank"][0] > 1]
    out["top1_when_root_rank_min_gt_1"] = {"units": len(wrong),
                                           "by_class": dict(Counter(t["class"] for u in wrong for t in u["top1_when_root_not_first"])),
                                           "entities": dict(Counter(t["entity"] for u in wrong for t in u["top1_when_root_not_first"]).most_common(8))}
    out["pairs_class_changes_with_baseline_only_graph"] = sum(a["class"] != a["class_baseline_graph"] for u in ok for a in u["above"])
    out["self_check_rank_equals_reference"] = {"true": sum(u["self_check_rank_equals_reference"] is True for u in ok),
                                               "false": sum(u["self_check_rank_equals_reference"] is False for u in ok),
                                               "no_reference": sum(u["self_check_rank_equals_reference"] is None for u in ok)}
    return out


def main():
    spanpass, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    fx = fixtures()
    if not fx["pass"]:
        raise SystemExit("trường hợp tự dựng không đạt: " + json.dumps(fx, ensure_ascii=False))
    units = unit_rows(spanpass)
    rng = np.random.default_rng(SEED)
    summary = {}
    keys = sorted({(u["dataset"], u["method"], u["seed"]) for u in units}, key=lambda k: (k[0], k[1], str(k[2])))
    for dataset, method, seed in keys:
        rows = [u for u in units if (u["dataset"], u["method"], u["seed"]) == (dataset, method, seed)]
        name = method if seed is None else method + "|seed=" + seed
        block = tally(rows, rng)
        block["by_fault"] = {f: {"units_with_above": sum(u.get("n_above", 0) > 0 for u in g), "pairs_above": sum(u.get("n_above", 0) for u in g),
                                 "above_by_class": dict(sum((Counter(u.get("above_by_class", {})) for u in g), Counter()))}
                             for f, g in ((f, [u for u in rows if u["fault"] == f]) for f in sorted({u["fault"] for u in rows}))}
        block["by_root"] = {r: {"units": len(g), "units_with_above": sum(u.get("n_above", 0) > 0 for u in g), "pairs_above": sum(u.get("n_above", 0) for u in g),
                                "above_by_class": dict(sum((Counter(u.get("above_by_class", {})) for u in g), Counter())),
                                "candidates_by_class_first_unit": next((u["candidates_by_class"] for u in g if "candidates_by_class" in u), None)}
                            for r, g in ((r, [u for u in rows if u["root"] == r]) for r in sorted({u["root"] for u in rows}))}
        summary.setdefault(dataset, {})[name] = block
    result = {"schema": "T032-chain-position-v1", "design": "results/T-032/thiet-ke-vi-tri-chuoi-goi-008.md mục 3", "fixtures": fx,
              "sources": {"labels": {"path": str(LABELS.relative_to(REPO)), "sha256": sha(LABELS)},
                          "spanpass_summary": {"path": str(spanpass / "summary.json"), "sha256": sha(spanpass / "summary.json")},
                          "index": {"path": str(INDEX.relative_to(REPO)), "sha256": sha(INDEX)}},
              "draws": DRAWS, "rng_seed": SEED, "classes": CLASSES, "groups": {k: list(v) for k, v in GROUPS.items()},
              "note": "Mô tả vị trí trên dev. Tỷ lệ rút ngẫu nhiên chỉ là mốc tham chiếu, không phải kiểm định. Không là nhãn lan.",
              "summary": summary, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "units.json").write_text(json.dumps(units, ensure_ascii=False) + "\n", encoding="utf-8")
    for dataset, block in summary.items():
        for name, b in block.items():
            g = b["groups"]
            print(dataset, name, "ok", b["units_ok_root_ranked"], "pairs", b["pairs_above"], "selfcheck", b["self_check_rank_equals_reference"],
                  "| tren", g["phia_tren"]["observed"], round(g["phia_tren"]["expected"], 1), "| 2chieu", g["hai_chieu"]["observed"], round(g["hai_chieu"]["expected"], 1),
                  "| duoi", g["phia_duoi"]["observed"], round(g["phia_duoi"]["expected"], 1), "| klh", g["khong_lien_he"]["observed"], round(g["khong_lien_he"]["expected"], 1),
                  "| kospan", g["khong_co_span"]["observed"], round(g["khong_co_span"]["expected"], 1), flush=True)


if __name__ == "__main__":
    main()

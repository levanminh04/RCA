"""T-032 bản 011 mục 2 (phép T-R, ngoài gói, Minh duyệt 11/10/2026): đổi công thức điểm của TraceRCA bản thư viện sang tỷ lệ.

Chạy trên EC2, chỉ đọc. Số a (span mang cờ), n (span sau mốc), H (tổng cờ) của từng thao tác lấy từ lượt chain-spanpass
(tổng cờ đã khớp H_native 48/48). Nhánh sham tính 2a/(n+H) bằng phân số chính xác; hạng mọi dịch vụ phải trùng bản ghi đóng băng.
Bước duy nhất bị đổi ở các nhánh khác: điểm của thao tác. Không gọi phương pháp. Nhãn root chỉ dùng để đọc hạng ở cuối.
Dùng: python tracerca_score_contrast_v1.py <lượt spanpass> <thư mục lượt mới>
"""
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import chain_position_v1 as cp  # noqa: E402

MIN_N = 20
BRANCHES = ("tr1", "tr1m", "ts")


def rank_of(scores):
    """{thực thể: điểm} → {thực thể: (hạng tốt nhất, hạng xấu nhất)}, giảm dần, hòa khi điểm bằng nhau chính xác."""
    out, offset = {}, 0
    for value in sorted(set(scores.values()), reverse=True):
        group = [e for e, s in scores.items() if s == value]
        for e in group:
            out[e] = (offset + 1, offset + len(group))
        offset += len(group)
    return out


def service_scores(ops, score, min_n=0):
    out = {}
    for v in ops.values():
        if v["n"] < min_n:
            continue
        s = score(v)
        if v["service"] not in out or s > out[v["service"]]:
            out[v["service"]] = s
    return out


def fixtures():
    ops = {"x1": {"service": "x", "a": 2, "n": 4}, "x2": {"service": "x", "a": 1, "n": 100}, "y1": {"service": "y", "a": 10, "n": 200}, "z1": {"service": "z", "a": 1, "n": 2}}
    H = 14
    sham = rank_of(service_scores(ops, lambda v: Fraction(2 * v["a"], v["n"] + H)))
    tr1 = rank_of(service_scores(ops, lambda v: Fraction(v["a"], v["n"])))
    tr1m = rank_of(service_scores(ops, lambda v: Fraction(v["a"], v["n"]), 20))
    ts = rank_of(service_scores(ops, lambda v: v["a"]))
    checks = {"sham: x 4/18 đứng trên z 2/16 đứng trên y 20/214": sham == {"x": (1, 1), "z": (2, 2), "y": (3, 3)},
              "tr1: x và z hòa ở 1/2, y sau": tr1 == {"x": (1, 2), "z": (1, 2), "y": (3, 3)},
              "tr1m: chỉ còn thao tác n>=20; y 0,05 trên x 0,01; z không được xếp": tr1m == {"y": (1, 1), "x": (2, 2)},
              "ts: y 10 trên x 2 trên z 1": ts == {"y": (1, 1), "x": (2, 2), "z": (3, 3)}}
    return {"pass": all(checks.values()), "checks": checks}


def main():
    spanpass, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    fx = fixtures()
    if not fx["pass"]:
        raise SystemExit("trường hợp tự dựng không đạt: " + json.dumps(fx, ensure_ascii=False))
    cases = []
    for row in cp.read(cp.LABELS)["main_rows"]:
        if row["method"] != "tracerca":
            continue
        dataset, opaque_id, root = row["dataset"], row["opaque_id"], row["root"]
        item = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": row["fault"], "cell": row["cell"], "status": row["status"]}
        if row["status"] != "OK":
            cases.append(item)
            continue
        frozen = cp.ranks_of(cp.read(cp.REPO / row["source"]["records"][0]["path"]), "tracerca")
        sp = cp.read(spanpass / "cases" / (dataset + "-" + opaque_id + ".json"))
        H = sp["counts"]["flags_tracerca_rule"]
        ops = {o: v for o, v in sp["operations"].items() if v["a"] > 0}
        views = {"sham": rank_of(service_scores(ops, lambda v: Fraction(2 * v["a"], v["n"] + H))),
                 "tr1": rank_of(service_scores(ops, lambda v: Fraction(v["a"], v["n"]))),
                 "tr1m": rank_of(service_scores(ops, lambda v: Fraction(v["a"], v["n"]), MIN_N)),
                 "ts": rank_of(service_scores(ops, lambda v: v["a"]))}
        item["H"] = H
        item["sham_ranks_equal_frozen"] = views["sham"] == {e: tuple(r) for e, r in frozen.items()}
        if not item["sham_ranks_equal_frozen"]:
            item["sham_difference"] = {"only_frozen": sorted(set(frozen) - set(views["sham"])), "only_sham": sorted(set(views["sham"]) - set(frozen)),
                                       "rank_differs": sorted(e for e in set(frozen) & set(views["sham"]) if tuple(frozen[e]) != views["sham"][e])[:10]}
        item["root_ranked_frozen"] = root in frozen
        item["views"] = {}
        for name, rank in views.items():
            v = {"n_entities": len(rank), "root_ranked": root in rank}
            if root in rank:
                v.update(root_rank_min=rank[root][0], root_rank_max=rank[root][1], above=sorted(e for e in rank if e != root and rank[e][1] < rank[root][0]))
            v["top"] = sorted(e for e in rank if rank[e][0] == 1)
            item["views"][name] = v
        cases.append(item)

    def block(rows, b):
        ok = [c for c in rows if c["status"] == "OK"]
        base = [c for c in ok if c["views"]["sham"]["root_ranked"]]
        ev = [c for c in base if c["views"][b]["root_ranked"]]
        res = {"cases": len(rows), "status": dict(Counter(c["status"] for c in rows)), "root_ranked_native": len(base), "root_ranked_branch": len(ev),
               "root_unranked_under_branch": [c["opaque_id"] for c in base if not c["views"][b]["root_ranked"]]}
        eff = Counter("tăng hạng" if c["views"][b]["root_rank_min"] < c["views"]["sham"]["root_rank_min"] else
                      "giảm hạng" if c["views"][b]["root_rank_min"] > c["views"]["sham"]["root_rank_min"] else "không đổi" for c in ev)
        res["root_effect"] = {k: eff.get(k, 0) for k in ("tăng hạng", "không đổi", "giảm hạng")}
        res["hit1"] = {"native": sum(c["views"]["sham"]["root_rank_max"] == 1 for c in base), b: sum(c["views"][b]["root_rank_max"] == 1 for c in ev)}
        res["hit5"] = {"native": sum(c["views"]["sham"]["root_rank_max"] <= 5 for c in base), b: sum(c["views"][b]["root_rank_max"] <= 5 for c in ev)}
        wrong = [c for c in ev if c["views"]["sham"]["root_rank_max"] > 1]
        right = [c for c in ev if c["views"]["sham"]["root_rank_max"] == 1]
        res["native_wrong"] = {"n": len(wrong), "become_rank1": sum(c["views"][b]["root_rank_max"] == 1 for c in wrong),
                               "ids_become_rank1": [c["opaque_id"] for c in wrong if c["views"][b]["root_rank_max"] == 1]}
        res["native_right"] = {"n": len(right), "lose_rank1": sum(c["views"][b]["root_rank_max"] > 1 for c in right),
                               "ids_lose_rank1": [c["opaque_id"] for c in right if c["views"][b]["root_rank_max"] > 1]}
        pairs = [(c, e) for c in ev for e in c["views"]["sham"]["above"]]
        res["pairs_above_root_native"] = {"n": len(pairs), "still_above": sum(e in c["views"][b]["above"] for c, e in pairs),
                                          "gone": sum(e not in c["views"][b]["above"] for c, e in pairs),
                                          "new_pairs": sum(e not in c["views"]["sham"]["above"] for c in ev for e in c["views"][b]["above"])}
        res["top_entity_same_as_native"] = sum(c["views"][b]["top"] == c["views"]["sham"]["top"] for c in ok)
        res["by_fault"] = {f: {"n": len(g), "hit1_native": sum(c["views"]["sham"]["root_rank_max"] == 1 for c in g), "hit1_branch": sum(c["views"][b]["root_rank_max"] == 1 for c in g)}
                           for f, g in ((f, [c for c in ev if c["fault"] == f]) for f in sorted({c["fault"] for c in ev}))}
        return res

    ok_all = [c for c in cases if c["status"] == "OK"]
    summary = {"self_check": {"cases_ok": len(ok_all), "sham_ranks_equal_frozen": sum(c["sham_ranks_equal_frozen"] for c in ok_all),
                              "not_equal": [c["opaque_id"] for c in ok_all if not c["sham_ranks_equal_frozen"]]}}
    for dataset in ("RE2-TT", "Nezha-OB"):
        summary[dataset] = {b: block([c for c in cases if c["dataset"] == dataset], b) for b in BRANCHES}
    result = {"schema": "T032-tracerca-score-contrast-v1", "design": "results/T-032/thiet-ke-phep-doi-011.md mục 2", "min_n": MIN_N, "fixtures": fx,
              "sources": {"spanpass_summary_sha256": cp.sha(spanpass / "summary.json"), "labels_sha256": cp.sha(cp.LABELS)},
              "summary": summary, "cases": cases, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary["self_check"], ensure_ascii=False))
    for dataset in ("RE2-TT", "Nezha-OB"):
        for b in BRANCHES:
            r = summary[dataset][b]
            print(dataset, b, "ranked", r["root_ranked_native"], "→", r["root_ranked_branch"], r["root_effect"], "hit1", r["hit1"], "hit5", r["hit5"],
                  "| wrong→1", r["native_wrong"]["become_rank1"], "/", r["native_wrong"]["n"], "right lost", r["native_right"]["lose_rank1"], "/", r["native_right"]["n"],
                  "| pairs", r["pairs_above_root_native"], "| top same", r["top_entity_same_as_native"], flush=True)


if __name__ == "__main__":
    main()

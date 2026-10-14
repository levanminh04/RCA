"""T-032 bản 010 mục 2 (việc 3): cột metric thắng của từng thực thể ở BARO và SimpleRCA so với vị trí trên chuỗi gọi và lưu lượng.

Chạy trên EC2, chỉ đọc và ghép các bảng đã có; không gọi phương pháp; không định nghĩa nhãn lan.
Dùng: python metric_chain_v1.py <lượt spanpass> <lượt service-traffic> <thư mục lượt mới>
"""
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import chain_position_v1 as cp  # noqa: E402

TREND = BASE / "runs/baseline-trend-001/cases"
DERIVED = BASE / "runs/derived-tables-001/derived.json"
GROUP_OF = {"goi_truc_tiep": "phia_tren", "phia_tren_gian_tiep": "phia_tren", "hai_chieu": "hai_chieu", "duoc_goi_truc_tiep": "phia_duoi",
            "phia_duoi_gian_tiep": "phia_duoi", "chung_phia_tren": "khong_lien_he", "roi": "khong_lien_he", "khong_co_span": "khong_co_span"}
ON_CHAIN = ("phia_tren", "hai_chieu", "phia_duoi")
BAND = (0.8, 1.25)


def table(rows, a, b):
    out = defaultdict(Counter)
    for r in rows:
        out[str(r.get(a))][str(r.get(b))] += 1
    return {k: dict(v) for k, v in sorted(out.items())}


def q(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def main():
    spanpass, traffic_dir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=False)
    labels = cp.read(cp.LABELS)["main_rows"]
    derived = cp.read(DERIVED)
    traffic = {(c["dataset"], c["opaque_id"]): c["services"] for c in cp.read(traffic_dir / "summary.json")["cases"]}
    kind_ref = {"baro": {(p["dataset"], p["opaque_id"], p["entity"]): p["entity_best"]["kind"] for p in derived["baro"]["pairs"]},
                "simplerca": {(p["dataset"], p["opaque_id"], p["entity"]): p["entity_top_column_kind"] for p in derived["simplerca"]["pairs"]}}
    rows, checks = [], Counter()
    for row in labels:
        method, dataset, opaque_id, root = row["method"], row["dataset"], row["opaque_id"], row["root"]
        if method not in ("baro", "simplerca") or row["status"] != "OK":
            continue
        record = cp.read(cp.REPO / row["source"]["records"][0]["path"])
        rank = cp.ranks_of(record, method)
        if root not in rank:
            continue
        sp = cp.read(spanpass / "cases" / (dataset + "-" + opaque_id + ".json"))
        g = cp.Graph(sp["services"], [(e["caller"], e["callee"]) for e in sp["edges"].values()])
        tr = traffic[(dataset, opaque_id)]
        ratios = {s: (v["spans_after"] / v["spans_before"]) for s, v in tr.items() if v["spans_before"] > 0}
        med = statistics.median(ratios.values()) if ratios else None
        winners = {}
        if dataset == "RE2-TT":
            trend = cp.read(TREND / (opaque_id + ".json"))
            columns = trend["baro_columns"] if method == "baro" else trend["simple_columns"]
            key = "z_max" if method == "baro" else "votes"
            for name in sorted(columns):
                c = columns[name]
                if c.get("status") != "ok" or c.get(key) is None:
                    continue
                best = winners.get(c["entity"])
                if best is None or c[key] > best[key]:
                    winners[c["entity"]] = {"column": name, "kind": c["kind"], "group": c["group"], key: c[key], "drift_ratio": c.get("drift_ratio")}
        for e in rank:
            if e == root:
                continue
            pos = g.position(e, root)
            above = rank[e][1] < rank[root][0]
            item = {"dataset": dataset, "method": method, "opaque_id": opaque_id, "fault": row["fault"], "root": root, "entity": e, "above_root": above,
                    "class": pos["class"], "position": GROUP_OF.get(pos["class"], pos["class"]), "root_rank_min": rank[root][0]}
            w = winners.get(e)
            if w:
                item.update(win_kind=w["kind"], win_group=w["group"], win_column=w["column"])
                if method == "simplerca" and w["votes"] == 0:
                    item.update(win_kind="không phiếu", win_group="không phiếu")
            if above and (dataset, opaque_id, e) in kind_ref[method]:
                ref = kind_ref[method][(dataset, opaque_id, e)]
                if dataset == "RE2-TT":
                    checks["above_kind_equals_derived" if item.get("win_kind") == ref else "above_kind_differs_from_derived"] += 1
                else:
                    item["win_kind"] = ref
            if e in ratios and med:
                item["traffic_ratio"] = ratios[e]
                item["traffic_ratio_normalized"] = ratios[e] / med
                item["traffic_changed"] = not (BAND[0] <= ratios[e] / med <= BAND[1])
            rows.append(item)
    summary = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        for method in ("baro", "simplerca"):
            rs = [r for r in rows if r["dataset"] == dataset and r["method"] == method]
            ab = [r for r in rs if r["above_root"]]
            block = {"entities": len(rs), "pairs_above": len(ab), "cases_with_above": len({r["opaque_id"] for r in ab}),
                     "above_position_by_kind": table(ab, "position", "win_kind"),
                     "above_traffic_changed_by_position": table([r for r in ab if "traffic_changed" in r], "position", "traffic_changed"),
                     "all_traffic_changed_by_position": table([r for r in rs if "traffic_changed" in r], "position", "traffic_changed"),
                     "above_traffic_ratio_normalized": {p: q([r.get("traffic_ratio_normalized") for r in ab if r["position"] == p]) for p in sorted({r["position"] for r in ab})}}
            if dataset == "RE2-TT":
                block["above_position_by_trend_group"] = table(ab, "position", "win_group")
                block["above_kind_by_trend_group"] = table(ab, "win_kind", "win_group")
                block["all_entities_position_by_trend_group"] = table([r for r in rs if "win_group" in r], "position", "win_group")
                step = [r for r in rs if r.get("win_group") == "bậc tại mốc"]
                block["step_at_t"] = {
                    "all_entities": len(step), "above_root": sum(r["above_root"] for r in step),
                    "all_on_chain": sum(r["position"] in ON_CHAIN for r in step), "all_unrelated": sum(r["position"] == "khong_lien_he" for r in step),
                    "all_no_span": sum(r["position"] == "khong_co_span" for r in step),
                    "above_on_chain": sum(r["above_root"] and r["position"] in ON_CHAIN for r in step),
                    "above_unrelated": sum(r["above_root"] and r["position"] == "khong_lien_he" for r in step),
                    "above_no_span": sum(r["above_root"] and r["position"] == "khong_co_span" for r in step),
                    "share_step_among_on_chain_entities": (sum(r["position"] in ON_CHAIN for r in step) /
                                                           max(1, sum(r["position"] in ON_CHAIN and "win_group" in r for r in rs))),
                    "share_step_among_unrelated_entities": (sum(r["position"] == "khong_lien_he" for r in step) /
                                                            max(1, sum(r["position"] == "khong_lien_he" and "win_group" in r for r in rs))),
                    "share_step_among_no_span_entities": (sum(r["position"] == "khong_co_span" for r in step) /
                                                          max(1, sum(r["position"] == "khong_co_span" and "win_group" in r for r in rs))),
                    "traffic_changed_among_step_with_span": dict(Counter(str(r.get("traffic_changed")) for r in step if r["position"] != "khong_co_span")),
                    "by_fault_above": dict(Counter(r["fault"] for r in step if r["above_root"]))}
            summary.setdefault(dataset, {})[method] = block
    result = {"schema": "T032-metric-chain-v1", "design": "results/T-032/thiet-ke-kenh-metric-010.md mục 2", "band": list(BAND), "on_chain": list(ON_CHAIN),
              "self_check": dict(checks), "note": "Mô tả trên dev; không là nhãn lan; các cột có thể chồng lấn.", "summary": summary, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "rows.json").write_text(json.dumps(rows, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"self_check": dict(checks)}, ensure_ascii=False))
    for dataset, b in summary.items():
        for method, r in b.items():
            print("==", dataset, method, "pairs", r["pairs_above"], "cases", r["cases_with_above"])
            print("   pos x kind", json.dumps(r["above_position_by_kind"], ensure_ascii=False))
            print("   above traffic changed", json.dumps(r["above_traffic_changed_by_position"], ensure_ascii=False), "| all", json.dumps(r["all_traffic_changed_by_position"], ensure_ascii=False))
            if "step_at_t" in r:
                print("   pos x trend", json.dumps(r["above_position_by_trend_group"], ensure_ascii=False))
                print("   kind x trend", json.dumps(r["above_kind_by_trend_group"], ensure_ascii=False))
                print("   step", json.dumps(r["step_at_t"], ensure_ascii=False))


if __name__ == "__main__":
    main()

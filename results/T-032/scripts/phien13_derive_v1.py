"""T-032 phiên 13: các đại lượng dẫn xuất từ bốn file kết quả mới, tính SAU khi đã xem kết quả (không phải mốc khai trước).

Chỉ đọc: runs/fake-marker-001/summary.json, runs/microrank-merged-link-001/summary.json, runs/tracerca-dropnew-001/summary.json,
runs/microrank-kt3-001/collect-001/summary.json. Không tính gì từ dữ liệu thô. Mỗi mục ghi nguồn và cách tính.
Dùng: python phien13_derive_v1.py <results/T-032> <file kết quả mới>
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8-sig"))


def q(v):
    v = sorted(x for x in v if x is not None)
    return {"n": len(v), "min": v[0], "median": statistics.median(v), "max": v[-1]} if v else {"n": 0}


def main():
    base, out = Path(sys.argv[1]), Path(sys.argv[2])
    res = {"schema": "T032-phien13-derived-v1", "note": "Đại lượng tính sau khi xem kết quả; dùng để mô tả, không phải mốc khai trước."}
    # --- KT-1: so cùng loại trace (không có root với không có root; có root với có root) ---
    fm = read(base / "runs/fake-marker-001/summary.json")
    ok = [c for c in fm["cases"] if c["status"] == "OK"]
    rows = []
    for c in ok:
        f, r = c["configs"]["fake150"], c["configs"]["real150"]
        rows.append({"opaque_id": c["opaque_id"], "cell": c["cell"], "fake_all": f["abnormal_share"], "real_all": r["abnormal_share"],
                     "fake_noroot": f["share_without_root"], "real_noroot": r["share_without_root"], "fake_withroot": f["share_with_root"], "real_withroot": r["share_with_root"],
                     "traces_noroot_real": r["traces_without_root"], "traces_withroot_real": r["traces_with_root"],
                     "abn_noroot_real": r["abnormal_without_root"], "abn_real": r["abnormal_traces"],
                     "pred_fake": f["predicted_share_independent_own_rates"], "span_flag_fake": f["span_flag_share"], "span_flag_real": r["span_flag_share"]})
    ratio_all = [x["fake_all"] / x["real_all"] for x in rows if x["real_all"]]
    ratio_no = [x["fake_noroot"] / x["real_noroot"] for x in rows if x["real_noroot"] and x["fake_noroot"] is not None]
    ratio_with = [x["fake_withroot"] / x["real_withroot"] for x in rows if x["real_withroot"] and x["fake_withroot"] is not None]
    res["kt1"] = {
        "source": "runs/fake-marker-001/summary.json → /cases/*/configs/{fake150,real150}", "n_cases": len(rows),
        "fake_all": q([x["fake_all"] for x in rows]), "real_all": q([x["real_all"] for x in rows]), "fake_over_real_all_by_case": q(ratio_all),
        "fake_noroot": q([x["fake_noroot"] for x in rows]), "real_noroot": q([x["real_noroot"] for x in rows]), "fake_over_real_noroot_by_case": q(ratio_no),
        "cases_fake_noroot_ge_0.8_real_noroot": sum(v >= 0.8 for v in ratio_no), "cases_fake_noroot_le_0.5_real_noroot": sum(v <= 0.5 for v in ratio_no),
        "fake_withroot": q([x["fake_withroot"] for x in rows]), "real_withroot": q([x["real_withroot"] for x in rows]), "fake_over_real_withroot_by_case": q(ratio_with),
        "share_of_real_abnormal_traces_without_root": q([x["abn_noroot_real"] / x["abn_real"] for x in rows if x["abn_real"]]),
        "predicted_over_actual_fake_by_case": q([x["pred_fake"] / x["fake_all"] for x in rows if x["fake_all"]]),
        "span_flag_fake": q([x["span_flag_fake"] for x in rows]), "span_flag_real": q([x["span_flag_real"] for x in rows]),
        "cases_fake_all_ge_0.20": sum(x["fake_all"] >= 0.20 for x in rows),
        "by_root": {root: {"n": len(g), "fake_noroot_median": statistics.median(x["fake_noroot"] for x in g), "real_noroot_median": statistics.median(x["real_noroot"] for x in g)}
                    for root, g in ((root, [x for x in rows if x["cell"].split("|")[0] == root]) for root in sorted({x["cell"].split("|")[0] for x in rows}))},
        "rows": rows}
    # --- KT-2 ---
    k = fm["summary"]["kt2"]
    up = ("goi_truc_tiep", "phia_tren_gian_tiep")
    unrel = ("roi", "chung_phia_tren")
    busy = [b for c in ok for b in c["busy_operations"]]

    def blk(rows_):
        return {"n": len(rows_), "fake_median": statistics.median(b["fake_share"] for b in rows_), "real_median": statistics.median(b["real_share"] for b in rows_),
                "fake_ge_2pct": sum(b["fake_share"] >= 0.02 for b in rows_), "real_ge_2x_fake": sum(b["real_share"] >= 2 * b["fake_share"] and b["real_share"] > 0 for b in rows_),
                "fake_max": max(b["fake_share"] for b in rows_)}
    pairs = [p for c in ok for p in c["unrelated_above_root_tracerca"]]
    res["kt2"] = {"source": "runs/fake-marker-001/summary.json → /cases/*/busy_operations, /cases/*/unrelated_above_root_tracerca",
                  "all": blk(busy), "upstream_of_root": blk([b for b in busy if b["class"] in up]), "unrelated": blk([b for b in busy if b["class"] in unrel]),
                  "downstream_or_both": blk([b for b in busy if b["class"] not in up + unrel]),
                  "summary_marks": {"mark_a": k.get("mark_a"), "mark_b": k.get("mark_b")},
                  "pairs": {"n": len(pairs), "real150_ge_2x_fake150": sum(p["real150"]["share"] >= 2 * p["fake150"]["share"] for p in pairs),
                            "fake150_ge_2pct": sum(p["fake150"]["share"] >= 0.02 for p in pairs),
                            "list": [{"entity": p["entity"], "fake150": [p["fake150"]["a"], p["fake150"]["n"]], "real150": [p["real150"]["a"], p["real150"]["n"]]} for p in pairs]}}
    # --- bảng nối cho nhánh ghép ---
    ml = read(base / "runs/microrank-merged-link-001/summary.json")
    link = {"source": "runs/microrank-merged-link-001/summary.json → /cases/*/branches/*/links", "by_dataset": {}}
    for ds in ("RE2-TT", "Nezha-OB"):
        link["by_dataset"][ds] = {}
        for br in ("mo15c1", "mo1p50c1"):
            cs = [c for c in ml["cases"] if c["dataset"] == ds and c["status"] == "OK" and c["branches"][br].get("root_wrong")]
            links = [(c, l) for c in cs for l in c["branches"][br]["links"]]
            short = Counter("gắn với root" if l["reading"].startswith("gắn") else "không gắn" if l["reading"].startswith("không gắn") else
                            "ít span" if l["reading"].startswith("ít span") else "không rõ" for _c, l in links)
            notatt = [l for _c, l in links if l["reading"].startswith("không gắn")]
            att = [l for _c, l in links if l["reading"].startswith("gắn")]
            link["by_dataset"][ds][br] = {
                "wrong_cases": len(cs), "top_entity_links": len(links), "reading": dict(short), "top_entities": dict(Counter(l["entity"] for _c, l in links)),
                "not_attached_with_zero_root_traces": sum((l.get("trace_level") or {}).get("has_root") == 0 for l in notatt),
                "attached_direct_ge_0.5": sum(l["root"]["on_F"]["direct"] >= 0.5 for l in att),
                "attached_class": dict(Counter(str(l.get("class")) for l in att)),
                "attached_cases": [c["opaque_id"] for c, l in links if l["reading"].startswith("gắn")],
                "not_attached_cases": [c["opaque_id"] for c, l in links if l["reading"].startswith("không gắn")]}
    res["merged_link"] = link
    # --- KT-8: hai phương pháp cạnh nhau ---
    td = read(base / "runs/tracerca-dropnew-001/summary.json")["summary"]
    kt3 = read(base / "runs/microrank-kt3-001/collect-001/summary.json")
    mr = {c["opaque_id"]: c["branches"]["dropnew"] for c in kt3["cases"] if c["t028"]["status"] != "OK"}
    res["kt8"] = {"source": "runs/tracerca-dropnew-001/summary.json → /summary; runs/microrank-kt3-001/collect-001/summary.json → /cases/*/branches/dropnew",
                  "tracerca_self_check": td["self_check"],
                  "cases": [{"opaque_id": c["opaque_id"], "cell": c["cell"], "spans_dropped": c["drop"]["spans_dropped"], "traces_touched": c["drop"]["traces_touched"],
                             "tracerca_root_rank": [c["root_rank_min"], c["root_rank_max"]], "tracerca_top": c["top"], "tracerca_n_entities": c["n_entities"],
                             "microrank_root_rank": [mr[c["opaque_id"]].get("root_rank_min"), mr[c["opaque_id"]].get("root_rank_max")],
                             "microrank_top": mr[c["opaque_id"]].get("top")} for c in td["error_source_cases"]],
                  "tracerca_hit1": td["error_source_hit1"], "tracerca_hit5": td["error_source_hit5"]}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
        f.write("\n")
    show = {"kt1": {k: v for k, v in res["kt1"].items() if k != "rows"}, "kt2": res["kt2"], "merged_link": res["merged_link"], "kt8": res["kt8"]}
    print(json.dumps(show, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()

"""T-034 E1: tổng hợp lượt e1 thành bảng theo cặp, theo ca và các đại lượng mô tả từ trung gian đã lưu. Chỉ đọc.

Không tính lại phương pháp. Mọi số lấy từ results/T-034/runs/<lượt>/out/ (đã kiểm mã băm hai đầu) và ledger đính chính.
Dùng: python e1_tong_hop.py <thư mục lượt, ví dụ results/T-034/runs/e1-001> <file ra .json>
"""
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEDGER = "results/T-032/runs/bo-sung-toan-dien-20261012-001/closure-ledger-review-001.json"
BRANCHES = ["to_p", "to_p3", "to_c"]
ROLE = {"to_p": "nhánh chính (cờ 1 lần độ lệch chuẩn, thời lượng span phía gọi)", "to_p3": "nhánh thứ hai (cờ 3 lần độ lệch chuẩn)",
        "to_c": "báo phụ (thời lượng span phía được gọi, 1 lần độ lệch chuẩn)"}


def fr(v):
    return None if v is None else float(Fraction(v[0], v[1]))


def classify(p):
    if p["status"] != "OK" or "relation_all" not in p:
        return "khong_co_quan_he"
    a, b = p["relation_all"], p["relation_singleton"]
    r_ev = (p["root_evidence_all"], p["root_evidence_singleton"])
    c_ev = (p["caller_evidence_all"], p["caller_evidence_singleton"])
    lost = "lost" in (r_ev[1], c_ev[1])
    if a == b:
        if r_ev == ("no_pattern", "no_pattern") and c_ev == ("no_pattern", "no_pattern"):
            return "khong_doi_ca_hai_khong_co_tap"
        if r_ev == ("no_pattern", "no_pattern"):
            return "khong_doi_root_khong_co_tap"
        return "khong_doi_ca_hai_con_bang_chung"
    if lost:
        return "doi_do_mat_bang_chung"
    return "doi_ca_hai_con_bang_chung"


def main():
    run = ROOT / sys.argv[1]
    out_path = ROOT / sys.argv[2]
    s = json.loads((run / "out/summary.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / LEDGER).read_text(encoding="utf-8"))
    author = {}
    for p in ledger["h6_pair_audit"]["pairs"]:
        author[(p["opaque_id"], p["caller"])] = {str(a["feature_selection_threshold"]): {"relation": a["relation"], "status": a["status"], "root_score": a.get("root_score"),
                                                                                         "caller_score": a.get("caller_score"), "root_fallback": a.get("root_fallback"),
                                                                                         "caller_fallback": a.get("caller_fallback")} for a in p["author"]}
    cases = {}
    for c in s["cases"]:
        cases[c["opaque_id"]] = json.loads((run / "out/cases" / f"{c['dataset']}--{c['opaque_id']}.json").read_text(encoding="utf-8"))
    pairs = []
    for p in s["pairs"]:
        row = {"dataset": p["dataset"], "opaque_id": p["opaque_id"], "root": p["root"], "caller": p["caller"], "branch": p["branch"], "status": p["status"],
               "old_relation_ledger_to_p": p["old_relation_ledger_to_p"], "class": classify(p),
               "author_thr1": author[(p["opaque_id"], p["caller"])].get("1"), "author_thr3": author[(p["opaque_id"], p["caller"])].get("3")}
        if "relation_all" in p:
            b = cases[p["opaque_id"]]["branches"][p["branch"]]
            tt = b["trace_types"]
            root, cal = p["root"], p["caller"]
            y = b["abnormal_traces"]
            ca, cs, rs, ra = p["caller_deciding_all"], p["caller_deciding_singleton"], p["root_deciding_singleton"], p["root_deciding_all"]
            row.update(
                relation_all=p["relation_all"], relation_singleton=p["relation_singleton"],
                root_score_all=fr(p["root_score_all"]), root_score_singleton=fr(p["root_score_singleton"]),
                caller_score_all=fr(p["caller_score_all"]), caller_score_singleton=fr(p["caller_score_singleton"]),
                root_score_all_fraction=p["root_score_all"], root_score_singleton_fraction=p["root_score_singleton"],
                caller_score_all_fraction=p["caller_score_all"], caller_score_singleton_fraction=p["caller_score_singleton"],
                root_evidence_all=p["root_evidence_all"], root_evidence_singleton=p["root_evidence_singleton"],
                caller_evidence_all=p["caller_evidence_all"], caller_evidence_singleton=p["caller_evidence_singleton"],
                root_rank_all=p["root_rank_all"], root_rank_singleton=p["root_rank_singleton"],
                caller_rank_all=p["caller_rank_all"], caller_rank_singleton=p["caller_rank_singleton"],
                caller_score_changed=p["caller_score_all"] != p["caller_score_singleton"], root_score_changed=p["root_score_all"] != p["root_score_singleton"],
                caller_deciding_all_members=None if ca is None else ca["members"], caller_deciding_all_size=None if ca is None else ca["set_size"],
                caller_deciding_all_ji=None if ca is None else fr(ca["ji"]), caller_deciding_all_n_out=None if ca is None else ca["n_out"],
                caller_singleton_ji=None if cs is None else fr(cs["ji"]), caller_singleton_n_in=None if cs is None else cs["n_in"],
                caller_singleton_n_out=None if cs is None else cs["n_out"],
                root_deciding_all_size=None if ra is None else ra["set_size"],
                root_singleton_ji=None if rs is None else fr(rs["ji"]), root_singleton_n_in=None if rs is None else rs["n_in"],
                root_singleton_n_out=None if rs is None else rs["n_out"],
                root_singleton_frequent=b["per_service"][root]["singleton_frequent"], root_singleton_in_top=b["per_service"][root]["singleton_in_top"],
                caller_singleton_frequent=b["per_service"][cal]["singleton_frequent"], caller_singleton_in_top=b["per_service"][cal]["singleton_in_top"],
                traces=b["traces"], abnormal_traces=y,
                traces_with_root=sum(t["count"] for t in tt if root in t["services"]),
                abnormal_traces_with_root=sum(t["count"] for t in tt if t["abnormal"] and root in t["services"]),
                traces_root_incoming_flag=sum(t["count"] for t in tt if root in t["in"]),
                traces_caller_outgoing_flag=sum(t["count"] for t in tt if cal in t["out"]),
                traces_caller_outgoing_flag_without_root_incoming_flag=sum(t["count"] for t in tt if cal in t["out"] and root not in t["in"]))
            row["caller_outgoing_flag_share_of_abnormal"] = row["traces_caller_outgoing_flag"] / y if y else None
        pairs.append(row)

    def tally(rows):
        return dict(Counter(r["class"] for r in rows))

    agg = {}
    for br in BRANCHES:
        for ds in ("RE2-TT", "Nezha-OB"):
            rows = [r for r in pairs if r["branch"] == br and r["dataset"] == ds]
            ok = [r for r in rows if "relation_all" in r]
            below = [r for r in ok if r["relation_all"] == "root dưới"]
            agg[f"{br}|{ds}"] = {
                "pairs_declared": len(rows), "pairs_with_relation": len(ok), "status": dict(Counter(r["status"] for r in rows)),
                "relation_all": dict(Counter(r["relation_all"] for r in ok)), "relation_singleton": dict(Counter(r["relation_singleton"] for r in ok)),
                "class_all_pairs": tally(ok),
                "phenomenon_pairs_root_below_in_all": len(below), "class_phenomenon_pairs": tally(below),
                "phenomenon_flipped_to_root_above_both_evidence": sum(r["relation_singleton"] == "root trên" and r["class"] == "doi_ca_hai_con_bang_chung" for r in below),
                "phenomenon_unchanged": sum(r["relation_singleton"] == "root dưới" for r in below),
                "phenomenon_caller_score_changed": sum(r["caller_score_changed"] for r in below),
                "phenomenon_caller_deciding_multi_service": sum((r["caller_deciding_all_size"] or 0) > 1 for r in below),
                "phenomenon_root_without_any_pattern": sum(r["root_evidence_all"] == "no_pattern" for r in below),
                "author_thr1_relation": dict(Counter((r["author_thr1"] or {}).get("relation") for r in rows)),
                "author_thr3_relation": dict(Counter((r["author_thr3"] or {}).get("relation") for r in rows))}
    by_case = []
    for cid, c in cases.items():
        for br in BRANCHES:
            b = c["branches"][br]
            row = {"dataset": c["dataset"], "opaque_id": cid, "root": c["root"], "fault": c["fault"], "branch": br, "status": b["status"]}
            if b["status"] == "OK":
                row.update(traces=b["traces"], abnormal_traces=b["abnormal_traces"], frequent_sets=b["frequent_sets"], top_sets=b["top_sets"],
                           top_size_histogram=b["top_size_histogram"], coverage_all=b["coverage_all"], coverage_singleton=b["coverage_singleton"],
                           n_services=b["n_services"], lost_evidence=b["lost_evidence"], root_rank_all=b["root_rank_all"], root_rank_singleton=b["root_rank_singleton"],
                           top_all=b["top_all"], top_singleton=b["top_singleton"], services_changed_score=b["services_changed_score"],
                           services_changed_rank=b["services_changed_rank"], checks_pass=b["checks_pass"],
                           root_singleton_frequent=b["per_service"][c["root"]]["singleton_frequent"], root_singleton_in_top=b["per_service"][c["root"]]["singleton_in_top"],
                           root_evidence_all=b["per_service"][c["root"]]["evidence_all"], root_evidence_singleton=b["per_service"][c["root"]]["evidence_singleton"])
            by_case.append(row)
    cases_ok = [r for r in by_case if r["status"] == "OK"]
    out = {"schema": "T034-E1-tong-hop-v1", "run": sys.argv[1], "design": "results/T-034/thiet-ke-hai-phep-kiem.md, phần E1",
           "validity": {"fixtures_pass": s["fixtures_pass"], "sham_all_equal": s["sham_all_equal"], "sham_cases_equal": sum(c["sham_equal"] for c in s["cases"]),
                        "sham_differences_total": sum(c["n_sham_differences"] for c in s["cases"]), "cases_done": s["cases_done"], "declared_cases": s["declared_cases"],
                        "declared_pairs": s["declared_pairs"], "instrument_checks_all_pass": s["instrument_checks_all_pass"], "interpretable": s["interpretable"],
                        "branch_results_ok": len(cases_ok), "branch_results_checks_pass": sum(bool(r["checks_pass"]) for r in cases_ok),
                        "branch_results_non_ok": dict(Counter(r["status"] for r in by_case if r["status"] != "OK")),
                        "wall_s_total": s["wall_s_total"], "ru_maxrss_kb": s["ru_maxrss_kb"]},
           "branch_roles": ROLE, "pairs": pairs, "aggregate": agg, "by_case": by_case,
           "notes": {"unit": "cặp (root, caller) đã khai; các cặp chung một ca không độc lập",
                     "class": {"doi_ca_hai_con_bang_chung": "quan hệ đổi, cả root và caller còn tập một dịch vụ được chấm",
                               "khong_doi_ca_hai_con_bang_chung": "quan hệ không đổi, cả hai còn tập được chấm ở nhánh B",
                               "khong_doi_root_khong_co_tap": "quan hệ không đổi; root không có tập nào trong top ở cả hai nhánh nên quy tắc pattern không chạm tới root",
                               "khong_doi_ca_hai_khong_co_tap": "cả hai không có tập nào trong top ở cả hai nhánh; hòa ở đáy",
                               "doi_do_mat_bang_chung": "quan hệ đổi vì một bên mất mọi tập được chấm ở nhánh B",
                               "khong_co_quan_he": "nhánh không có đặc trưng hữu ích hoặc không xếp được"}}}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["validity"], ensure_ascii=False))
    for k, v in agg.items():
        print(k, json.dumps(v, ensure_ascii=False))


if __name__ == "__main__":
    main()

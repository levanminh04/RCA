"""T-034: gom kết quả E1 và E2 thành `hai-phep-kiem.json` và chạy các phép kiểm V6, V7. Chỉ đọc đầu ra của các lượt đã đưa về laptop.

Dùng: python hai_phep_kiem_build.py <lượt E1> <lượt E2 dùng để kết luận> <lượt E2 đối chiếu> <file ra>
ví dụ: python hai_phep_kiem_build.py results/T-034/runs/e1-001 results/T-034/runs/e2-002 results/T-034/runs/e2-001 results/T-034/hai-phep-kiem.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
LABELS = ["dev-3ae0a6c15a--PF", "dev-3ae0a6c15a--FF", "dev-ba831dbeb8--PF", "dev-ba831dbeb8--FF"]
PROXY = 720


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def e2_chain(run, label):
    s = read(run / "out" / f"{label}--summary.json")
    c = s["comparison_native_vs_log"]
    z = np.load(run / "out" / f"{label}--compact.npz")
    out = {"label": label, "case": label.split("--")[0], "branch": label.split("--")[1], "T": s["T"], "d": s["d"], "schema": s["schema"],
           "npz_sha256": s["npz_sha256"], "sham": {k: v for k, v in s["sham"].items() if k not in ("cp_indices", "cp_indices_stored", "note_pdf")},
           "sham_cp_indices": s["sham"]["cp_indices"], "density_check": s["density_check"], "stored_pdf_exact_zero_values": s["stored_pdf_exact_zero_values"],
           "extended_reference": s.get("extended_reference"), "lineage_cross_check": s["lineage_cross_check"],
           "timing": {"sham_s": s["sham"]["wall_s"], "log_s": s["log_wall_s"], "extended_s": (s.get("extended_reference") or {}).get("wall_s"), "total_s": s["wall_s_total"],
                      "rss_peak_observed_bytes": s["rss_peak_observed_bytes"], "compact_npz_bytes": s["compact_npz_bytes"]},
           "comparison": {k: v for k, v in c.items() if k != "m_difference_detail"}, "m_difference_detail": c["m_difference_detail"]}
    cn, cl = c["cp_native"], c["cp_log"]
    post_n, post_l = [i for i in cn if i >= PROXY], [i for i in cl if i >= PROXY]
    win = lambda idx: sorted({i // 60 for i in idx})
    differing = sorted(set(c["cp_only_native"]) | set(c["cp_only_log"]))
    mdiff = [d["index"] for d in c["m_difference_detail"]]
    out["reading"] = {
        "cp_count_native": len(cn), "cp_count_log": len(cl), "cp_only_native": c["cp_only_native"], "cp_only_log": c["cp_only_log"],
        "first_alarm_native": cn[0] if cn else None, "first_alarm_log": cl[0] if cl else None, "first_alarm_unchanged": (cn[:1] == cl[:1]),
        "first_alarm_before_proxy_native": bool(cn and cn[0] < PROXY), "first_alarm_before_proxy_log": bool(cl and cl[0] < PROXY),
        "cp_before_proxy_equal": [i for i in cn if i < PROXY] == [i for i in cl if i < PROXY],
        "first_cp_from_proxy_native": post_n[0] if post_n else None, "first_cp_from_proxy_log": post_l[0] if post_l else None,
        "delay_from_proxy_native_s": (post_n[0] - PROXY) if post_n else None, "delay_from_proxy_log_s": (post_l[0] - PROXY) if post_l else None,
        "windows60_positive_native": win(cn), "windows60_positive_log": win(cl), "windows60_changed": sorted(set(win(cn)) ^ set(win(cl))),
        "differing_cp_indices": differing, "differing_cp_offsets_from_proxy_s": [i - PROXY for i in differing],
        "differing_cp_all_within_seconds_after_proxy": (max(differing) - PROXY + 1) if differing and min(differing) >= PROXY else None,
        "m_difference_indices": mdiff, "m_difference_first": mdiff[0] if mdiff else None, "m_difference_last": mdiff[-1] if mdiff else None,
        "m_differences_contiguous": bool(mdiff) and mdiff == list(range(mdiff[0], mdiff[-1] + 1)),
        "m_native_at_first_difference": int(z["m_native"][mdiff[0]]) if mdiff else None, "m_log_at_first_difference": int(z["m_log"][mdiff[0]]) if mdiff else None,
        "log_map_lineage_start_index_at_first_difference": (mdiff[0] - int(z["m_log"][mdiff[0]]) + 1) if mdiff else None,
        "native_map_lineage_start_index_at_first_difference": (mdiff[0] - int(z["m_native"][mdiff[0]]) + 1) if mdiff else None}
    return out, z


def main():
    e1_run, e2_run, e2_ref, out_path = (ROOT / a for a in sys.argv[1:5])
    e1 = read(e1_run / "tong-hop.json")
    pairs = e1["pairs"]
    nz_front = [p for p in pairs if p["branch"] == "to_p" and p["dataset"] == "Nezha-OB" and p["caller"] == "frontend" and "relation_all" in p]
    re2_first = {}
    for p in pairs:
        if p["branch"] == "to_p" and p["dataset"] == "RE2-TT" and "relation_all" in p:
            re2_first.setdefault(p["opaque_id"], p)
    shares = [p["caller_outgoing_flag_share_of_abnormal"] for p in nz_front]
    e1["derived"] = {
        "to_p_nezha_frontend_pairs": len(nz_front),
        "to_p_nezha_frontend_outgoing_flag_share_min": min(shares), "to_p_nezha_frontend_outgoing_flag_share_max": max(shares),
        "to_p_nezha_frontend_outgoing_without_root_incoming_min": min(p["traces_caller_outgoing_flag_without_root_incoming_flag"] for p in nz_front),
        "to_p_nezha_frontend_outgoing_without_root_incoming_max": max(p["traces_caller_outgoing_flag_without_root_incoming_flag"] for p in nz_front),
        "to_p_nezha_frontend_score_drop_relative_max": max((p["caller_score_all"] - p["caller_score_singleton"]) / p["caller_score_all"] for p in nz_front),
        "to_p_re2_cases": len(re2_first), "to_p_re2_root_singleton_frequent": sum(p["root_singleton_frequent"] for p in re2_first.values()),
        "to_p_re2_root_singleton_in_top": sum(p["root_singleton_in_top"] for p in re2_first.values()),
        "to_p_re2_root_support_min": min(p["abnormal_traces_with_root"] / p["abnormal_traces"] for p in re2_first.values()),
        "to_p_re2_root_support_max": max(p["abnormal_traces_with_root"] / p["abnormal_traces"] for p in re2_first.values()),
        "to_p3_nezha_flip_by_lost_evidence": e1["aggregate"]["to_p3|Nezha-OB"]["class_all_pairs"].get("doi_do_mat_bang_chung", 0),
        "to_p3_singleton_relation_matches_author_thr1_pairs": sum(1 for p in pairs if p["branch"] == "to_p3" and p["dataset"] == "Nezha-OB" and "relation_singleton" in p
                                                                  and {"root trên": "above", "root dưới": "below", "hòa": "tie"}[p["relation_singleton"]] == (p["author_thr1"] or {}).get("relation")),
        "to_p3_nezha_pairs_with_relation": sum(1 for p in pairs if p["branch"] == "to_p3" and p["dataset"] == "Nezha-OB" and "relation_singleton" in p),
        "note": "Đại lượng mô tả tính từ bảng kiểu trace đã lưu của E1; không phải can thiệp."}
    v6 = {"fixtures": e1["validity"]["fixtures_pass"], "sham_11_of_11": e1["validity"]["sham_cases_equal"] == e1["validity"]["declared_cases"] == 11,
          "sham_zero_differences": e1["validity"]["sham_differences_total"] == 0, "instrument_checks": e1["validity"]["instrument_checks_all_pass"],
          "all_declared_pairs_present": len({(p["opaque_id"], p["caller"]) for p in pairs}) == e1["validity"]["declared_pairs"] == 13,
          "every_pair_has_result_or_status_in_3_branches": all(sum(1 for p in pairs if (p["opaque_id"], p["caller"]) == k) == 3 for k in {(p["opaque_id"], p["caller"]) for p in pairs}),
          "singleton_never_above_all": all(p["caller_score_singleton"] <= p["caller_score_all"] and p["root_score_singleton"] <= p["root_score_all"] for p in pairs if "relation_all" in p),
          "to_p_all_relation_equals_ledger_old_relation": all(p["relation_all"] == p["old_relation_ledger_to_p"] for p in pairs if p["branch"] == "to_p" and "relation_all" in p)}
    v6["status"] = "PASS" if all(v6.values()) else "FAIL"
    e1["v6"] = v6

    # ------------------------------------------------------------------------------------------------ E2
    chains, compact = {}, {}
    for label in LABELS:
        chains[label], compact[label] = e2_chain(e2_run, label)
    ref_chains, ref_compact = {}, {}
    for label in LABELS:
        ref_chains[label], ref_compact[label] = e2_chain(e2_ref, label)
    cross = {label: {"m_log_equal": bool(np.array_equal(compact[label]["m_log"], ref_compact[label]["m_log"])),
                     "m_native_equal": bool(np.array_equal(compact[label]["m_native"], ref_compact[label]["m_native"])),
                     "cp_log_equal": bool(np.array_equal(compact[label]["cp_log"], ref_compact[label]["cp_log"])),
                     "reference_run_sham_pass": ref_chains[label]["sham"]["pass"],
                     "reference_run_sham_R_relative_error_max": ref_chains[label]["sham"]["R_relative_error_max_normal_zone"]} for label in LABELS}
    fx = read(e2_run / "fixtures-ec2" / "fixtures.json")
    det_dir = e2_run / "determinism"
    determinism = {p.stem: {k: v for k, v in read(p).items() if k not in ("environment", "threadpools")} | {"threads_env": read(p)["environment"]["threads_env"]}
                   for p in sorted(det_dir.glob("*.json"))} if det_dir.is_dir() else {}
    diff = [c for c in chains.values() if not (c["comparison"]["m_equal_all"] and c["comparison"]["cp_equal"])]
    summary = {"chains": len(chains), "chains_sham_pass_declared": sum(c["sham"]["pass"] for c in chains.values()),
               "chains_sham_bit_exact": sum(c["sham"]["R_bit_equal_stored"] for c in chains.values()),
               "chains_extended_pass": sum(bool((c["extended_reference"] or {}).get("pass")) for c in chains.values()),
               "chains_m_cp_equal": sum(c["comparison"]["m_equal_all"] and c["comparison"]["cp_equal"] for c in chains.values()),
               "chains_m_cp_differ": len(diff),
               "chains_first_alarm_unchanged": sum(c["reading"]["first_alarm_unchanged"] for c in chains.values()),
               "chains_cp_before_proxy_equal": sum(c["reading"]["cp_before_proxy_equal"] for c in chains.values()),
               "native_exact_zero_states_min": min(c["comparison"]["native_exact_zero_states"] for c in chains.values()),
               "native_exact_zero_states_max": max(c["comparison"]["native_exact_zero_states"] for c in chains.values()),
               "clean_error_before_affected_mass_max": max(c["comparison"].get("posterior_log_abs_error_max_clean_before_affected_mass", 0.0) for c in chains.values()),
               "extended_max_abs_log_difference_max": max((c["extended_reference"] or {}).get("max_abs_log_difference_vs_log_domain", 0.0) for c in chains.values()),
               "lineage_cross_check_max_abs_difference": max(abs(r["difference"]) for c in chains.values() for r in c["lineage_cross_check"] if "difference" in r),
               "cross_run_m_log_equal": sum(v["m_log_equal"] for v in cross.values()), "cross_run_cp_log_equal": sum(v["cp_log_equal"] for v in cross.values()),
               "machine_seconds_total": round(sum(c["timing"]["total_s"] for c in chains.values()), 1)}
    if diff:
        d = diff[0]
        r, c = d["reading"], d["comparison"]
        w = [x for x in c.get("divergence_windows_tv_gt_1e-6", [])]
        summary["diff"] = {"case": d["case"], "label": d["label"], "m_differences": c["m_differences"], "m_first": r["m_difference_first"], "m_last": r["m_difference_last"],
                           "m_contiguous": r["m_differences_contiguous"], "cp_only_native": len(c["cp_only_native"]), "cp_only_log": len(c["cp_only_log"]),
                           "cp_only_native_indices": c["cp_only_native"], "cp_only_log_indices": c["cp_only_log"],
                           "cp_count_native": r["cp_count_native"], "cp_count_log": r["cp_count_log"],
                           "delay_native_s": r["delay_from_proxy_native_s"], "delay_log_s": r["delay_from_proxy_log_s"],
                           "window_s": r["differing_cp_all_within_seconds_after_proxy"], "windows60_changed": len(r["windows60_changed"]),
                           "first_alarm_native": r["first_alarm_native"], "first_alarm_unchanged": r["first_alarm_unchanged"],
                           "log_map_lineage_start": r["log_map_lineage_start_index_at_first_difference"], "native_map_lineage_start": r["native_map_lineage_start_index_at_first_difference"],
                           "classes": c["m_difference_classes"], "divergence_windows": w, "divergence_columns": c.get("columns_tv_gt_1e-6"),
                           "affected_mass_max": float(np.exp(c["affected_mass_log_max"])) if c.get("affected_mass_log_max") is not None else None,
                           "total_variation_max": c["total_variation_max"], "other_chains_with_difference": len(diff) - 1}
    v7 = {"fixtures_F1_F2_F3_F4": bool(fx["pass"] and fx["F1"]["pass"] and fx["F2"]["pass"] and fx["F3"]["pass"] and fx["F4"]["pass"] is True),
          "four_declared_chains_present": sorted(chains) == sorted(LABELS),
          "sham_declared_criterion_all": summary["chains_sham_pass_declared"] == 4,
          "sham_m_cp_exact_all": all(c["sham"]["m_equal_stored"] and c["sham"]["cp_flags_equal_stored"] for c in chains.values()),
          "log_domain_finite_all": all(c["comparison"]["log_domain_nonfinite_reachable"] == 0 and c["comparison"]["log_domain_nan"] == 0 for c in chains.values()),
          "log_normalization_all": all(c["comparison"]["log_normalization_abs_max"] <= 1e-12 for c in chains.values()),
          "clean_states_before_affected_mass_within_1e-9": summary["clean_error_before_affected_mass_max"] <= 1e-9,
          "extended_reference_all": summary["chains_extended_pass"] == 4,
          "no_unexplained_m_difference": all(c["comparison"]["m_difference_classes"]["other"] == 0 for c in chains.values()),
          "frozen_normalizer_cross_check_within_1e-6": summary["lineage_cross_check_max_abs_difference"] <= 1e-6,
          "density_matches_stored": all(c["density_check"]["logpdf_abs_error_max_vs_stored"] <= 1e-9 for c in chains.values())}
    v7["status"] = "PASS" if all(v7.values()) else "FAIL"
    out = {"schema": "T034-hai-phep-kiem-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "design": "results/T-034/thiet-ke-hai-phep-kiem.md",
           "E1": dict(e1, run=sys.argv[1]),
           "E2": {"run_used": sys.argv[2], "run_reference_one_thread": sys.argv[3], "chains": chains, "reference_run_chains": {k: {"sham": v["sham"], "comparison": v["comparison"], "reading": v["reading"]} for k, v in ref_chains.items()},
                  "cross_run": cross, "fixtures_ec2": {k: {kk: vv for kk, vv in fx[k].items() if kk in ("checks", "pass", "status", "T", "d")} for k in ("F1", "F2", "F3", "F4")},
                  "fixtures_pass": fx["pass"], "determinism": determinism, "summary": summary, "v7": v7}}
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("V6", v6["status"], {k: v for k, v in v6.items() if v is not True and k != "status"})
    print("V7", v7["status"], {k: v for k, v in v7.items() if v is not True and k != "status"})
    print(json.dumps(summary, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()

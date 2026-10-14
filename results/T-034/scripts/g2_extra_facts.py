"""T-034: số lấy từ hai file do T-034 dựng (`bang-baseline.json`, `hai-phep-kiem.json`) cho bản đồ và gói G2.

`bang-baseline.json` chép nguyên số của T-024/T-025/T-026/T-029 kèm con trỏ nguồn và đã qua V2 (tính lại từ bản ghi).
`hai-phep-kiem.json` gom đầu ra của các lượt E1/E2 và đã qua V6/V7.
"""
BL = "results/T-034/bang-baseline.json"
HK = "results/T-034/hai-phep-kiem.json"
MAIN = ["baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"]


def register(F):
    A = F.add
    # ---- bảng baseline: xếp hạng chế độ (a)
    for coh, tag in (("RE2-TT_dev30", "re2"), ("RE2-TT_dev19", "re19"), ("Nezha-OB_main", "nz")):
        A(f"bl.{tag}.n", BL, f"/ranking_mode_a/{coh}/n_cases")
        A(f"bl.{tag}.cells", BL, f"/ranking_mode_a/{coh}/n_cells")
        for m in MAIN:
            base = f"/ranking_mode_a/{coh}/methods/{m}"
            for key, short in (("hit@1", "h1"), ("hit@3", "h3"), ("hit@5", "h5"), ("mrr", "mrr"), ("ndcg@5", "ndcg"), ("avg@5", "avg"), ("retrieval@5", "ret5"), ("retrieval@10", "ret10"),
                               ("rerank@1(K=5)", "rr5"), ("hit@1_cases_expected", "h1n"), ("hit@5_cases_expected", "h5n")):
                A(f"bl.{tag}.{m}.{short}", BL, f"{base}/{key}")
            A(f"bl.{tag}.{m}.lo", BL, f"{base}/bootstrap95/hit@1/lo")
            A(f"bl.{tag}.{m}.hi", BL, f"{base}/bootstrap95/hit@1/hi")
            for st in ("OK", "ERROR", "UNSUPPORTED"):
                try:
                    A(f"bl.{tag}.{m}.st.{st}", BL, f"{base}/status/{st}")
                except KeyError:
                    pass
            if tag != "nz":
                A(f"bl.{tag}.{m}.ac1", BL, f"{base}/rcaeval/AC@1")
                A(f"bl.{tag}.{m}.avg5r", BL, f"{base}/rcaeval/Avg@5")
    # ---- phát hiện
    for det in ("bocpd", "nsigma", "nsigma_doi_chung"):
        base = f"/detection_mode_b/{det}"
        A(f"bl.det.{det}.n", BL, base + "/n_cases")
        A(f"bl.det.{det}.p", BL, base + "/precision")
        A(f"bl.det.{det}.r", BL, base + "/recall")
        A(f"bl.det.{det}.f1", BL, base + "/f1")
        A(f"bl.det.{det}.fa", BL, base + "/false_alarms_per_normal_hour")
        A(f"bl.det.{det}.fan", BL, base + "/false_alarms")
        A(f"bl.det.{det}.sec", BL, base + "/normal_seconds_evaluated")
        A(f"bl.det.{det}.delay", BL, base + "/delay_from_injection_s/trung_vi")
        A(f"bl.det.{det}.dmin", BL, base + "/delay_from_injection_s/min")
        A(f"bl.det.{det}.dmax", BL, base + "/delay_from_injection_s/max")
        A(f"bl.det.{det}.zero", BL, base + "/delays_equal_zero")
        A(f"bl.det.{det}.det", BL, base + "/cases_detected")
        A(f"bl.det.{det}.first_ok", BL, base + "/cases_first_alarm_at_or_after_injection")
    # ---- chế độ (b) và bảng G
    for ranker, short in (("baro:native", "baro"), ("circa:ols+rht_da", "circa"), ("torai_B", "torai")):
        for det in ("bocpd", "nsigma"):
            base = f"/mode_b_rca_at_first_alarm/{ranker}[{det}]"
            A(f"bl.b.{short}_{det}.joint1", BL, base + "/joint_success/hit@1")
            A(f"bl.b.{short}_{det}.joint5", BL, base + "/joint_success/hit@5")
            A(f"bl.b.{short}_{det}.all1", BL, base + "/rca_at_first_alarm_all_cases/hit@1")
            A(f"bl.b.{short}_{det}.ok", BL, base + "/cases_first_alarm_correct")
    for ranker, short in (("baro", "baro"), ("circa_ols_da", "circa"), ("torai_B", "torai")):
        for det in ("bocpd", "nsigma"):
            base = f"/table_G_run_point/rows/{ranker}[{det}]/points"
            A(f"bl.g.{short}_{det}.a", BL, base + "/a/hit@1")
            A(f"bl.g.{short}_{det}.tplus", BL, base + "/t_hat_plus/hit@1")
            A(f"bl.g.{short}_{det}.that", BL, base + "/t_hat/hit@1")
    # ---- nhánh chẩn đoán
    rows = "/diagnostic_branches_not_baseline/tracerca_author_code_latency_only/rows"
    for i, tag in enumerate(("nz.ms1", "nz.ms3", "nz.us1", "nz.us3", "re2.ms1", "re2.ms3", "re2.us1", "re2.us3")):
        for k, short in (("n", "n"), ("hit1_pessimistic", "pes"), ("hit1_expected", "exp"), ("hit1_optimistic", "opt")):
            A(f"bl.author.{tag}.{short}", BL, f"{rows}/{i}/{k}")
        A(f"bl.author.{tag}.ok", BL, f"{rows}/{i}/status/OK")
        A(f"bl.author.{tag}.noev", BL, f"{rows}/{i}/status/NO_EVIDENCE")
    mr = "/diagnostic_branches_not_baseline/microrank_paper_split/summary"
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        for br in ("mo15", "mo1p50"):
            A(f"bl.mrsplit.{tag}.{br}.hit1", BL, f"{mr}/{ds}/{br}/hit1/{br}")
            A(f"bl.mrsplit.{tag}.{br}.eval", BL, f"{mr}/{ds}/{br}/evaluable")
            A(f"bl.mrsplit.{tag}.{br}.cases", BL, f"{mr}/{ds}/{br}/cases")
    A("bl.v2.problems", BL, "/v2/n_problems")
    A("bl.v2.status", BL, "/v2/status")
    # ---- E1
    v = "/E1/validity"
    for k, short in (("declared_cases", "cases"), ("declared_pairs", "pairs"), ("sham_cases_equal", "sham"), ("sham_differences_total", "shamdiff"),
                     ("branch_results_ok", "branches_ok"), ("branch_results_checks_pass", "checks"), ("wall_s_total", "wall")):
        A(f"e1.{short}", HK, f"{v}/{k}")
    A("e1.nouse", HK, f"{v}/branch_results_non_ok/NO_USEFUL_FEATURE")
    for br, tag in (("to_p", "top"), ("to_p3", "top3"), ("to_c", "toc")):
        for ds, dtag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
            base = f"/E1/aggregate/{br}|{ds}"
            for k, short in (("pairs_with_relation", "rel"), ("phenomenon_pairs_root_below_in_all", "phen"), ("phenomenon_flipped_to_root_above_both_evidence", "flip"),
                             ("phenomenon_unchanged", "unch"), ("phenomenon_caller_score_changed", "scorechg"), ("phenomenon_caller_deciding_multi_service", "multi"),
                             ("phenomenon_root_without_any_pattern", "rootnone")):
                A(f"e1.{tag}.{dtag}.{short}", HK, f"{base}/{k}")
    d = "/E1/derived"
    for k, short in (("to_p_nezha_frontend_pairs", "front.pairs"), ("to_p_nezha_frontend_outgoing_flag_share_min", "front.share_min"),
                     ("to_p_nezha_frontend_outgoing_flag_share_max", "front.share_max"), ("to_p_nezha_frontend_outgoing_without_root_incoming_min", "front.noroot_min"),
                     ("to_p_nezha_frontend_outgoing_without_root_incoming_max", "front.noroot_max"), ("to_p_nezha_frontend_score_drop_relative_max", "front.drop_max"),
                     ("to_p_re2_cases", "re2.cases"), ("to_p_re2_root_singleton_frequent", "re2.freq"), ("to_p_re2_root_singleton_in_top", "re2.intop"),
                     ("to_p_re2_root_support_min", "re2.sup_min"), ("to_p_re2_root_support_max", "re2.sup_max"), ("to_p3_nezha_flip_by_lost_evidence", "top3.lost"),
                     ("to_p3_singleton_relation_matches_author_thr1_pairs", "top3.match"), ("to_p3_nezha_pairs_with_relation", "top3.rel")):
        A(f"e1.{short}", HK, f"{d}/{k}")
    # ---- E2
    s = "/E2/summary"
    for k, short in (("chains", "chains"), ("chains_sham_pass_declared", "sham_pass"), ("chains_sham_bit_exact", "sham_bit"), ("chains_extended_pass", "ext_pass"),
                     ("chains_m_cp_equal", "chains_equal"), ("chains_m_cp_differ", "chains_differ"), ("chains_first_alarm_unchanged", "first_same"),
                     ("chains_cp_before_proxy_equal", "pre_same"), ("native_exact_zero_states_min", "zero_min"), ("native_exact_zero_states_max", "zero_max"),
                     ("clean_error_before_affected_mass_max", "clean_err"), ("extended_max_abs_log_difference_max", "ext_err"),
                     ("lineage_cross_check_max_abs_difference", "lineage_err"), ("cross_run_m_log_equal", "cross_m"), ("cross_run_cp_log_equal", "cross_cp"),
                     ("machine_seconds_total", "machine_s")):
        A(f"e2.{short}", HK, f"{s}/{k}")
    for k, short in (("case", "case"), ("m_differences", "m"), ("m_first", "m_first"), ("m_last", "m_last"), ("cp_only_native", "cp_only_native"), ("cp_only_log", "cp_only_log"),
                     ("cp_count_native", "cp_n"), ("cp_count_log", "cp_l"), ("delay_native_s", "delay_n"), ("delay_log_s", "delay_l"), ("window_s", "window_s"),
                     ("windows60_changed", "win_changed"), ("first_alarm_native", "first"), ("log_map_lineage_start", "lin_log"), ("native_map_lineage_start", "lin_nat"),
                     ("divergence_columns", "div_cols"), ("affected_mass_max", "mass"), ("total_variation_max", "tv")):
        A(f"e2.diff.{short}", HK, f"{s}/diff/{k}")
    A("e2.diff.cls.direct", HK, f"{s}/diff/classes/underflow")
    A("e2.diff.cls.down", HK, f"{s}/diff/classes/underflow_downstream")
    A("e2.diff.cls.other", HK, f"{s}/diff/classes/other")
    for i in range(3):
        A(f"e2.diff.cp_log.{i}", HK, f"{s}/diff/cp_only_log_indices/{i}")
    A("e2.diff.cp_nat.0", HK, f"{s}/diff/cp_only_native_indices/0")
    for label, tag in (("dev-3ae0a6c15a--PF", "3ae.pf"), ("dev-3ae0a6c15a--FF", "3ae.ff"), ("dev-ba831dbeb8--PF", "ba8.pf"), ("dev-ba831dbeb8--FF", "ba8.ff")):
        base = f"/E2/chains/{label}"
        A(f"e2.{tag}.T", HK, base + "/T")
        A(f"e2.{tag}.d", HK, base + "/d")
        A(f"e2.{tag}.zeros", HK, base + "/comparison/native_exact_zero_states")
        A(f"e2.{tag}.sub", HK, base + "/comparison/native_subnormal_states")
        A(f"e2.{tag}.reach", HK, base + "/comparison/reachable_states")
        A(f"e2.{tag}.mdiff", HK, base + "/comparison/m_differences")
        A(f"e2.{tag}.cpn", HK, base + "/reading/cp_count_native")
        A(f"e2.{tag}.cpl", HK, base + "/reading/cp_count_log")
        A(f"e2.{tag}.tv", HK, base + "/comparison/total_variation_max")
        A(f"e2.{tag}.dirty", HK, base + "/comparison/states_error_gt_1e-9_lineage_was_subnormal")
        A(f"e2.{tag}.dirtyerr", HK, base + "/comparison/posterior_log_abs_error_max_lineage_was_subnormal")
        A(f"e2.{tag}.total_s", HK, base + "/timing/total_s")
        A(f"e2.{tag}.ext", HK, base + "/extended_reference/max_abs_log_difference_vs_log_domain")
        A(f"e2.{tag}.ref_sham", HK, f"/E2/cross_run/{label}/reference_run_sham_R_relative_error_max")
    A("e2.v7", HK, "/E2/v7/status")
    A("e1.v6", HK, "/E1/v6/status")
    A("e2.fx.pass", HK, "/E2/fixtures_pass")
    A("e2.det.unset.rows", HK, "/E2/determinism/3ae-PF--threads-unset/pdf_rows_bit_equal_stored")
    A("e2.det.unset.total", HK, "/E2/determinism/3ae-PF--threads-unset/pdf_rows")
    A("e2.det.unset.rbit", HK, "/E2/determinism/ba83-PF--threads-unset/R_bit_equal_stored")
    A("e2.det.one.rows", HK, "/E2/determinism/ba83-PF--threads-1/pdf_rows_bit_equal_stored")
    A("e2.det.one.frac", HK, "/E2/determinism/ba83-PF--threads-1/R_bit_equal_fraction")
    A("e2.det.one.rel", HK, "/E2/determinism/ba83-PF--threads-1/pdf_relative_difference_max")
    A("e2.det.one.rbit", HK, "/E2/determinism/ba83-PF--threads-1/R_bit_equal_stored")
    for label, tag in (("dev-3ae0a6c15a--PF", "3ae.pf"), ("dev-3ae0a6c15a--FF", "3ae.ff"), ("dev-ba831dbeb8--PF", "ba8.pf"), ("dev-ba831dbeb8--FF", "ba8.ff")):
        base = f"/E2/chains/{label}"
        A(f"e2.{tag}.shambit", HK, base + "/sham/R_bit_equal_stored")
        A(f"e2.{tag}.rss", HK, base + "/timing/rss_peak_observed_bytes")
        A(f"e2.{tag}.npz", HK, base + "/timing/compact_npz_bytes")
        A(f"e2.{tag}.first", HK, base + "/reading/first_alarm_native")
        A(f"e2.{tag}.prefirst", HK, base + "/reading/first_alarm_before_proxy_native")
        A(f"e2.{tag}.dirtymass", HK, base + "/comparison/max_log_mass_of_states_error_gt_1e-9")
        A(f"e2.{tag}.lost", HK, base + "/comparison/lost_mass_log_max")
        A(f"e2.{tag}.ref_m", HK, f"/E2/cross_run/{label}/m_log_equal")
    A("e2.diff.first_mass_col", HK, "/E2/chains/dev-3ae0a6c15a--FF/comparison/first_column_affected_mass_gt_1e-12")
    A("e2.diff.mass_cols", HK, "/E2/chains/dev-3ae0a6c15a--FF/comparison/columns_affected_mass_gt_1e-12")
    A("e2.diff.win_first", HK, "/E2/chains/dev-3ae0a6c15a--FF/comparison/divergence_windows_tv_gt_1e-6/0/first_column")
    A("e2.diff.win_last", HK, "/E2/chains/dev-3ae0a6c15a--FF/comparison/divergence_windows_tv_gt_1e-6/0/last_column")
    A("e2.diff.pre_n", HK, "/E2/chains/dev-3ae0a6c15a--FF/comparison/n_cp_before_720_native")
    A("e2.diff.pre_l", HK, "/E2/chains/dev-3ae0a6c15a--FF/comparison/n_cp_before_720_log")
    A("e2.diff.native_at_logmap", HK, "/E2/chains/dev-3ae0a6c15a--FF/m_difference_detail/0/native_R_at_log_map")
    A("e1.rss", HK, "/E1/validity/ru_maxrss_kb")
    A("e1.top.nz.unch_both", HK, "/E1/aggregate/to_p|Nezha-OB/class_phenomenon_pairs/khong_doi_ca_hai_con_bang_chung")

"""T-032 phiên 11: so các con số của ket-qua-phien-11.md với file kết quả, theo con trỏ JSON. Chạy trên laptop, chỉ đọc.

Mỗi dòng: (mục, mô tả, giá trị viết trong báo cáo, file, con trỏ, cách làm tròn). Con trỏ là danh sách khóa; nhiều con trỏ thì cộng.
Cách làm tròn: None = so nguyên giá trị; số nguyên n = làm tròn n chữ số; "pct1" = nhân 100 rồi làm tròn 1 chữ số.
Dùng: py -3 -B -X utf8 scripts/self_check_phien11_v1.py <file kết quả mới>
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = "runs/chain-position-002/summary.json"
C = "runs/chain-position-cond-001/summary.json"
S = "runs/chain-spanpass-001/summary.json"
L = "runs/slow-call-flag-link-001/summary.json"
R = "runs/tracerca-ratio-vs-count-001/summary.json"
M = "runs/metric-chain-001/summary.json"
F = "runs/root-signal-by-fault-001/summary.json"
N = "runs/trace-root-census-001/summary.json"
CLAIMS = []


def add(section, what, value, file, pointer, rounding=None):
    CLAIMS.append({"section": section, "what": what, "reported": value, "file": file, "pointer": pointer, "rounding": rounding})


def pos(dataset, method, with_above, pairs, obs, exp, ratio, pct, top1, cond=None):
    base = ["summary", dataset, method]
    add("1", f"{dataset} {method} ca có thực thể đứng trên root", with_above, P, base + ["units_with_above"])
    add("1", f"{dataset} {method} số cặp", pairs, P, base + ["pairs_above"])
    g = base + ["groups", "phia_tren"]
    add("1", f"{dataset} {method} phía trên quan sát", obs, P, g + ["observed"])
    add("1", f"{dataset} {method} phía trên kỳ vọng", exp, P, g + ["expected"], 1)
    add("1", f"{dataset} {method} tỷ số", ratio, P, g + ["ratio"], 2)
    add("1", f"{dataset} {method} rút ngẫu nhiên %", pct, P, g + ["random_draw_share_ge_observed"], "pct1")
    add("1", f"{dataset} {method} đổi lớp với đồ thị nền", 0, P, base + ["pairs_class_changes_with_baseline_only_graph"])
    add("1", f"{dataset} {method} thực thể đứng đầu nằm phía trên", top1, C, base + ["cases", "top1_is_upstream"])
    if cond:
        gc = base + ["groups", "phia_tren"]
        add("1", f"{dataset} {method} kỳ vọng (có span)", cond[0], C, gc + ["expected"], 1)
        add("1", f"{dataset} {method} tỷ số (có span)", cond[1], C, gc + ["ratio"], 2)
        add("1", f"{dataset} {method} rút ngẫu nhiên % (có span)", cond[2], C, gc + ["random_draw_share_ge_observed"], "pct1")


pos("RE2-TT", "baro", 9, 103, 8, 3.1, 2.58, 0.2, 1, (4.9, 1.62, 3.8))
pos("RE2-TT", "simplerca", 5, 20, 6, 0.8, 7.58, 0.0, 4, (1.9, 3.21, 0.1))
pos("RE2-TT", "microrank_full", 24, 132, 4, 18.5, 0.22, 100.0, 0)
pos("RE2-TT", "tracerca", 5, 15, 4, 1.9, 2.10, 7.7, 3)
pos("RE2-TT", "circa_ols_da", 14, 110, 25, 3.5, 7.19, 0.0, 9, (9.0, 2.79, 0.0))
pos("RE2-TT", "circa_ols_rht_khong_DA", 18, 86, 22, 3.1, 7.09, 0.0, 13, (7.2, 3.04, 0.0))
pos("RE2-TT", "torai_B|seed=0", 4, 7, 2, 0.3, 6.09, 3.2, 1, (0.8, 2.36, 18.1))
pos("Nezha-OB", "baro", 14, 59, 7, 6.9, 1.02, 58.4, 2)
pos("Nezha-OB", "simplerca", 15, 44, 9, 4.7, 1.93, 0.8, 7)
pos("Nezha-OB", "microrank_full", 22, 120, 20, 19.2, 1.04, 45.8, 0)
pos("Nezha-OB", "tracerca", 18, 75, 20, 12.6, 1.58, 0.0, 12)
add("1", "spanpass số ca OK", 52, S, ["n_ok"])
add("1", "spanpass cờ hai cách khác nhau", 0, S, ["flags_differ_total"])
add("1", "BARO RE2 không có span", 44, P, ["summary", "RE2-TT", "baro", "above_by_class", "khong_co_span"])
add("1", "BARO RE2 không liên hệ", 38, P, ["summary", "RE2-TT", "baro", "groups", "khong_lien_he", "observed"])
add("1", "BARO RE2 đứng đầu lớp rời", 7, P, ["summary", "RE2-TT", "baro", "top1_when_root_rank_min_gt_1", "by_class", "roi"])
add("1", "MicroRank RE2 phía dưới quan sát", 35, P, ["summary", "RE2-TT", "microrank_full", "groups", "phia_duoi", "observed"])
add("1", "MicroRank RE2 phía dưới kỳ vọng", 14.1, P, ["summary", "RE2-TT", "microrank_full", "groups", "phia_duoi", "expected"], 1)
add("1", "MicroRank RE2 phía dưới tỷ số", 2.49, P, ["summary", "RE2-TT", "microrank_full", "groups", "phia_duoi", "ratio"], 2)
add("1", "MicroRank RE2 không liên hệ quan sát", 87, P, ["summary", "RE2-TT", "microrank_full", "groups", "khong_lien_he", "observed"])
add("1", "MicroRank RE2 không liên hệ kỳ vọng", 97.1, P, ["summary", "RE2-TT", "microrank_full", "groups", "khong_lien_he", "expected"], 1)
add("1", "MicroRank RE2 đứng đầu ts-station-service", 21, P, ["summary", "RE2-TT", "microrank_full", "top1_when_root_rank_min_gt_1", "entities", "ts-station-service"])
add("1", "MicroRank RE2 đứng đầu ts-route-service", 3, P, ["summary", "RE2-TT", "microrank_full", "top1_when_root_rank_min_gt_1", "entities", "ts-route-service"])
add("1", "MicroRank Nezha đứng đầu currencyservice", 13, P, ["summary", "Nezha-OB", "microrank_full", "top1_when_root_rank_min_gt_1", "entities", "currencyservice"])
add("1", "MicroRank Nezha đứng đầu cartservice", 5, P, ["summary", "Nezha-OB", "microrank_full", "top1_when_root_rank_min_gt_1", "entities", "cartservice"])
add("1", "MicroRank Nezha đứng đầu productcatalogservice", 4, P, ["summary", "Nezha-OB", "microrank_full", "top1_when_root_rank_min_gt_1", "entities", "productcatalogservice"])
add("1", "TraceRCA Nezha đứng đầu frontend", 11, P, ["summary", "Nezha-OB", "tracerca", "top1_when_root_rank_min_gt_1", "entities", "frontend"])
add("1", "CIRCA DA phía dưới", 0, P, ["summary", "RE2-TT", "circa_ols_da", "groups", "phia_duoi", "observed"])
add("1", "CIRCA DA đứng đầu travel2 + travel", 9, P, [["summary", "RE2-TT", "circa_ols_da", "top1_when_root_rank_min_gt_1", "entities", "ts-travel2-service"],
                                                         ["summary", "RE2-TT", "circa_ols_da", "top1_when_root_rank_min_gt_1", "entities", "ts-travel-service"]])
for m, v in (("baro", 5), ("circa_ols_da", 4), ("microrank_full", 4), ("torai_B|seed=0", 2)):
    add("1", f"RE2 {m} ca sai root không có phía trên", v, C, ["summary", "RE2-TT", m, "cases", "root_has_no_upstream_candidates"])
for m in ("baro", "simplerca", "microrank_full", "tracerca"):
    add("1", f"Nezha {m} ca sai root không có phía trên", 2, C, ["summary", "Nezha-OB", m, "cases", "root_has_no_upstream_candidates"])
add("1", "BARO RE2 ca có thực thể phía trên", 3, C, ["summary", "RE2-TT", "baro", "cases", "with_any_upstream_above"])
for name, a, b in (("MicroRank phía trên mọi cặp", ("RE2-TT", "microrank_full"), ("Nezha-OB", "microrank_full")), ("TraceRCA", ("RE2-TT", "tracerca"), ("Nezha-OB", "tracerca")),
                   ("SimpleRCA", ("RE2-TT", "simplerca"), ("Nezha-OB", "simplerca")), ("BARO", ("RE2-TT", "baro"), ("Nezha-OB", "baro"))):
    want = {"MicroRank phía trên mọi cặp": (24, 30), "TraceRCA": (24, 25), "SimpleRCA": (15, 16), "BARO": (15, 18)}[name]
    add("1", name + " phía trên cộng hai dataset", want[0], P, [["summary", *a, "groups", "phia_tren", "observed"], ["summary", *b, "groups", "phia_tren", "observed"]])
    add("1", name + " kể cả hai chiều", want[1], P, [["summary", *a, "groups", "phia_tren_ke_ca_hai_chieu", "observed"], ["summary", *b, "groups", "phia_tren_ke_ca_hai_chieu", "observed"]])


def grp(dataset, method, group, n, ge50, median):
    base = ["summary", dataset, method, "groups", group]
    add("2", f"{dataset} {method} {group} n", n, L, base + ["n"])
    add("2", f"{dataset} {method} {group} đạt 50%", ge50, L, base + ["main", "ge_0.5"])
    if median is not None:
        add("2", f"{dataset} {method} {group} trung vị", median, L, base + ["main_quantiles", "median"], 2)


grp("RE2-TT", "tracerca", "above_upstream_measurable", 4, 4, 0.85)
grp("Nezha-OB", "tracerca", "above_upstream_measurable", 15, 9, 0.88)
grp("RE2-TT", "tracerca", "above_not_upstream_measurable", 3, 0, 0.0)
grp("Nezha-OB", "tracerca", "above_not_upstream_measurable", 36, 0, 0.0)
grp("RE2-TT", "tracerca", "not_above_upstream_measurable_wrong_cases", 21, 11, 0.57)
grp("Nezha-OB", "tracerca", "not_above_upstream_measurable_wrong_cases", 4, 4, 1.0)
grp("RE2-TT", "tracerca", "not_above_upstream_measurable_root_rank1_cases", 96, 83, 0.96)
grp("Nezha-OB", "tracerca", "not_above_upstream_measurable_root_rank1_cases", 3, 2, 0.93)
grp("RE2-TT", "microrank", "above_upstream_measurable", 10, 0, 0.17)
grp("Nezha-OB", "microrank", "above_upstream_measurable", 16, 4, 0.21)
grp("RE2-TT", "microrank", "above_not_upstream_measurable", 66, 18, 0.29)
grp("Nezha-OB", "microrank", "above_not_upstream_measurable", 71, 16, 0.13)
grp("RE2-TT", "microrank", "not_above_upstream_measurable_wrong_cases", 112, 103, 0.99)
grp("Nezha-OB", "microrank", "not_above_upstream_measurable_wrong_cases", 9, 7, 0.95)
for d, m, v in (("RE2-TT", "tracerca", 17), ("Nezha-OB", "tracerca", 15), ("Nezha-OB", "microrank", 16), ("RE2-TT", "microrank", 17)):
    add("2", f"{d} {m} ca xét được", v, L, ["summary", d, m, "cases_root_edge_measurable"])
add("2", "TraceRCA RE2 span không cờ trung vị %", 1.5, L, ["summary", "RE2-TT", "tracerca", "groups", "above_upstream_measurable", "share_slow_nonflag_quantiles", "median"], "pct1")
add("2", "TraceRCA RE2 span không cờ lớn nhất %", 5.1, L, ["summary", "RE2-TT", "tracerca", "groups", "above_upstream_measurable", "share_slow_nonflag_quantiles", "max"], "pct1")
add("2", "TraceRCA Nezha span không cờ lớn nhất %", 10.8, L, ["summary", "Nezha-OB", "tracerca", "groups", "above_upstream_measurable", "share_slow_nonflag_quantiles", "max"], "pct1")
for d, vals in (("RE2-TT", (5, 4, 4, 3, 3)), ("Nezha-OB", (19, 13, 16, 8, 5))):
    for key, v in zip(("wrong_cases", "wrong_cases_measurable", "wrong_cases_with_above_upstream", "wrong_cases_with_above_upstream_mostly_waiting",
                       "wrong_cases_all_above_mostly_waiting"), vals):
        add("2", f"TraceRCA {d} {key}", v, L, ["summary", d, "tracerca", key])
for f, w, k in (("cpu_contention", 5, 4), ("network_delay", 5, 3), ("cpu_consumed", 2, 1), ("exception", 3, 0), ("return", 4, 0)):
    add("2", f"TraceRCA Nezha {f} ca sai", w, L, ["summary", "Nezha-OB", "tracerca", "wrong_cases_by_fault", f, "wrong_cases"])
    add("2", f"TraceRCA Nezha {f} chủ yếu chờ", k, L, ["summary", "Nezha-OB", "tracerca", "wrong_cases_by_fault", f, "with_above_upstream_mostly_waiting"])
add("2", "MicroRank RE2 ca sai chủ yếu gắn root", 0, L, ["summary", "RE2-TT", "microrank", "wrong_cases_with_above_upstream_mostly_waiting"])
add("2", "MicroRank Nezha ca sai chủ yếu gắn root", 4, L, ["summary", "Nezha-OB", "microrank", "wrong_cases_with_above_upstream_mostly_waiting"])
add("2", "MicroRank RE2 ca sai", 24, L, ["summary", "RE2-TT", "microrank", "wrong_cases"])
add("2", "MicroRank Nezha ca sai", 22, L, ["summary", "Nezha-OB", "microrank", "wrong_cases"])
add("2", "MicroRank RE2 gọi trực tiếp: span chậm đạt 50%", 3, L, ["summary", "RE2-TT", "microrank", "groups", "above_direct_caller_measurable", "span_share_slow", "ge_0.5"])
add("2", "MicroRank RE2 gọi trực tiếp n", 5, L, ["summary", "RE2-TT", "microrank", "groups", "above_direct_caller_measurable", "n"])
add("2", "MicroRank RE2 gọi trực tiếp nhỏ nhất %", 24.3, L, ["summary", "RE2-TT", "microrank", "groups", "above_direct_caller_measurable", "main_quantiles", "min"], "pct1")
add("2", "MicroRank RE2 gọi trực tiếp lớn nhất %", 37.6, L, ["summary", "RE2-TT", "microrank", "groups", "above_direct_caller_measurable", "main_quantiles", "max"], "pct1")
for d, v in (("RE2-TT", (15, 12, 15, 12, 3, 5)), ("Nezha-OB", (75, 39, 75, 39, 5, 18))):
    for key, x in zip(("pairs", "ratio_lower_than_root", "ji_larger_than_root", "ratio_lower_and_a_larger", "cases_where_root_has_top_ratio_among_above_and_root", "cases_with_above"), v):
        add("2", f"TraceRCA tỷ lệ và số tuyệt đối {d} {key}", x, R, ["summary", d, key])

MB, MS = ["summary", "RE2-TT", "baro"], ["summary", "RE2-TT", "simplerca"]
for position, vals in (("phia_tren", {"bậc tại mốc": 3, "khác": 5}), ("hai_chieu", {"khác": 3}), ("phia_duoi", {"bậc tại mốc": 2, "trôi nền": 1, "khác": 5, "không dịch": 2}),
                       ("khong_lien_he", {"bậc tại mốc": 3, "trôi nền": 6, "khác": 27, "không dịch": 2}), ("khong_co_span", {"bậc tại mốc": 6, "trôi nền": 12, "khác": 26})):
    for k, v in vals.items():
        add("3", f"BARO RE2 {position} {k}", v, M, MB + ["above_position_by_trend_group", position, k])
for position, vals in (("phia_tren", {"bậc tại mốc": 3, "khác": 3}), ("hai_chieu", {"khác": 1}), ("khong_lien_he", {"bậc tại mốc": 1, "trôi nền": 1, "khác": 4}),
                       ("khong_co_span", {"bậc tại mốc": 2, "trôi nền": 5})):
    for k, v in vals.items():
        add("3", f"SimpleRCA RE2 {position} {k}", v, M, MS + ["above_position_by_trend_group", position, k])
add("3", "tự kiểm loại cột thắng", 123, M, ["self_check", "above_kind_equals_derived"])
for base, vals in ((MB, (19.5, 11.2, 9.3)), (MS, (22.4, 11.9, 5.7))):
    for key, v in zip(("share_step_among_on_chain_entities", "share_step_among_unrelated_entities", "share_step_among_no_span_entities"), vals):
        add("3", f"{base[2]} {key} %", v, M, base + ["step_at_t", key], "pct1")
for key, v in (("all_on_chain", 41), ("all_unrelated", 59), ("all_no_span", 118), ("above_root", 14), ("above_on_chain", 5)):
    add("3", f"BARO bậc tại mốc {key}", v, M, MB + ["step_at_t", key])
add("3", "BARO bậc tại mốc lưu lượng đổi", 19, M, MB + ["step_at_t", "traffic_changed_among_step_with_span", "True"])
add("3", "BARO bậc tại mốc lưu lượng không đổi", 81, M, MB + ["step_at_t", "traffic_changed_among_step_with_span", "False"])
for f, v in (("loss", 9), ("delay", 3), ("cpu", 2)):
    add("3", f"BARO bậc tại mốc lỗi {f}", v, M, MB + ["step_at_t", "by_fault_above", f])
NB = ["summary", "Nezha-OB", "baro"]
for position, t, fl in (("phia_duoi", 14, 14), ("khong_lien_he", 6, 18), ("phia_tren", 1, 6)):
    add("3", f"BARO Nezha {position} lưu lượng đổi", t, M, NB + ["above_traffic_changed_by_position", position, "True"])
    add("3", f"BARO Nezha {position} lưu lượng không đổi", fl, M, NB + ["above_traffic_changed_by_position", position, "False"])
for position, t, fl in (("phia_duoi", 23, 29), ("khong_lien_he", 20, 96), ("phia_tren", 4, 26)):
    add("3", f"Nezha mọi thực thể {position} lưu lượng đổi", t, M, NB + ["all_traffic_changed_by_position", position, "True"])
    add("3", f"Nezha mọi thực thể {position} lưu lượng không đổi", fl, M, NB + ["all_traffic_changed_by_position", position, "False"])

for key, vals in (("RE2-TT|cpu", (6, 6, 4, 6, 6, 6, 0, 0)), ("RE2-TT|delay", (6, 5, 2, 3, 5, 5, 0, 0)), ("RE2-TT|disk", (6, 6, 6, 6, 4, 6, 0, 0)),
                  ("RE2-TT|loss", (6, 5, 3, 2, 2, 5, 0, 0)), ("RE2-TT|mem", (3, 2, 1, 2, 2, 2, 0, 0)), ("RE2-TT|socket", (3, 2, 2, 2, 2, 2, 0, 0)),
                  ("Nezha-OB|cpu_consumed", (4, 4, 2, 0, 2, 3, 0, 1)), ("Nezha-OB|cpu_contention", (5, 5, 5, 5, 0, 5, 3, 0)),
                  ("Nezha-OB|exception", (3, 3, 1, 1, 0, 2, 0, 0)), ("Nezha-OB|network_delay", (6, 6, 0, 1, 0, 6, 4, 0)), ("Nezha-OB|return", (4, 4, 0, 0, 0, 1, 0, 3))):
    for field, v in zip(("cases", "cases_with_span_table", "baro_rank1", "simplerca_rank1", "tracerca_rank1", "root_first_at_any_trace_position",
                         "root_first_only_at_caller_side", "no_signal_any_channel"), vals):
        add("7", f"{key} {field}", v, F, ["by_dataset_fault", key, field])
for key, med, mn in (("RE2-TT|cpu", 1331.5, 1290), ("RE2-TT|delay", 838, 509), ("RE2-TT|disk", 1401.0, 1160), ("RE2-TT|loss", 664, 240), ("RE2-TT|mem", 1580.5, 1446),
                     ("RE2-TT|socket", 1472.0, 1441), ("Nezha-OB|cpu_consumed", 11.0, 2), ("Nezha-OB|cpu_contention", 34, 27), ("Nezha-OB|exception", 10, 9),
                     ("Nezha-OB|network_delay", 4.0, 0), ("Nezha-OB|return", 1.5, 0)):
    add("7", f"{key} phiếu trung vị", med, F, ["by_dataset_fault", key, "root_metric_votes_median"])
    add("7", f"{key} phiếu nhỏ nhất", mn, F, ["by_dataset_fault", key, "root_metric_votes_min"])

for d, vals in (("RE2-TT", (30, 29, 39724, 261, 39463, 0, 38727, 38727, 5)), ("Nezha-OB", (22, 22, 19080, 0, 19022, 58, 19022, 19022, 0))):
    for field, v in zip(("cases", "cases_gate_pass", "after_traces", "after_traces_roots_0", "after_traces_roots_1", "after_traces_roots_2_plus", "one_root_complete",
                         "one_root_complete_identity_holds", "cases_with_needed_operation_without_slo"), vals):
        add("4", f"bước đếm {d} {field}", v, N, ["summary", d, field])

TA, TB = "runs/torai-severity-table-a-001/summary.json", "runs/torai-severity-table-003/summary.json"
LA, LB = "runs/torai-log-source-a-001/summary.json", "runs/torai-log-source-001/summary.json"
PA, PB = "runs/torai-log-placebo-a-001/summary.json", "runs/torai-log-placebo-001/summary.json"
for tag, f, vals in (("A", TA, (21, 9, 21, 0, 22, 23, 4, 10)), ("B", TB, (26, 4, 26, 0, 7, 23, 2, 22))):
    z = ["summary", "seed0"]
    for ptr, v in zip((["hit1"], ["wrong_at_1"], ["root_severity_rank_is_1_among_hit1"], ["root_severity_rank_is_1_among_wrong"], ["pairs_above_root"],
                       ["root_source_rank_is_1", "metric"], ["root_source_rank_is_1", "log"], ["root_source_rank_is_1", "trace_lat"]), vals):
        add("6", f"TORAI {tag} {'/'.join(ptr)}", v, f, z + ptr)
for src, v in (("trace_lat", 13), ("log", 5), ("metric", 4)):
    add("6", f"TORAI A nguồn nghiêng nhiều nhất {src}", v, TA, ["summary", "seed0", "pairs_above_root_largest_source_difference", src])
add("6", "TORAI B nguồn nghiêng nhiều nhất log", 7, TB, ["summary", "seed0", "pairs_above_root_largest_source_difference", "log"])
add("6", "TORAI A hạng trùng TORAI B (không phải tự kiểm)", 66, TA, ["summary", "self_check_rank_equals_t028"])
add("6", "TORAI A trung gian giống nhau ba seed", 30, TA, ["summary", "cases_three_seeds_same_pre_rcd_intermediates"])
for key in ("y_train_equals_row_mean", "cluster_score_rebuilt", "blocks_equal_clusters_in_rank_order"):
    add("6", f"TORAI A kiểm {key}", 90, TA, ["summary", "checks", key])
for tag, f, vals in (("A", LA, (30, 30, 7, 7, 2, 0.0, 19.6, 0.0, 86.6)), ("B", LB, (29, 29, 14, 20, 7, 27.3, 56.6, 54.6, 89.9))):
    top = "ts-preserve-other-service" if tag == "A" else "ts-order-other-service"
    for ptr, v, r in ((["cases_with_log_columns"], vals[0], None), (["rebuild_ok"], vals[1], None), (["top_service_by_log", top], vals[2], None),
                      (["top_service_top_column_std_N_zero"], vals[3], None), (["wrong_cases", "pairs_where_entity_top_log_column_has_std_N_zero"], vals[4], None),
                      (["share_of_scored_columns_with_std_N_zero", "median"], vals[5], "pct1"), (["share_of_scored_columns_with_std_N_zero", "max"], vals[6], "pct1"),
                      (["log_mass_on_std_N_zero_columns", "median"], vals[7], "pct1"), (["log_mass_on_std_N_zero_columns", "max"], vals[8], "pct1")):
        add("6", f"TORAI log {tag} {'/'.join(ptr)}", v, f, ["summary"] + ptr, r)
add("6", "phép thử giả A trùng dịch vụ đứng đầu", 2, PA, ["summary", "placebo_top_service_equals_main_top_service"])
add("6", "phép thử giả B trùng dịch vụ đứng đầu", 12, PB, ["summary", "placebo_top_service_equals_main_top_service"])
add("6", "trace_err A số ca tổng mọi ô bằng 0", 20, PA, ["summary", "trace_err", "cases_sum_all_cells_zero"])
add("6", "trace_err A số ca mọi cột không đổi", 30, PA, ["summary", "trace_err", "cases_all_columns_constant"])
add("4", "bước đếm RE2 tỷ lệ một span đầu nhỏ nhất %", 83.5, N, ["summary", "RE2-TT", "share_exactly_one_root", "min"], "pct1")
add("4", "bước đếm RE2 tỷ lệ một span đầu trung vị %", 99.9, N, ["summary", "RE2-TT", "share_exactly_one_root", "median"], "pct1")
add("4", "bước đếm Nezha tỷ lệ nhỏ nhất %", 97.6, N, ["summary", "Nezha-OB", "share_exactly_one_root", "min"], "pct1")
add("4", "bước đếm Nezha tỷ lệ trung vị %", 99.8, N, ["summary", "Nezha-OB", "share_exactly_one_root", "median"], "pct1")
for d, vals in (("RE2-TT", (997, 35, 39256, 227470, 9514577, 5340, 41886, 40699, 254, 759, 174)), ("Nezha-OB", (58, 61, 18761, 278798, 1421887, 90779, 13504, 13462, 0, 42, 0))):
    for field, v in zip(("after_traces_with_orphan", "after_traces_straddling_t", "one_root_traces_root_encloses_all", "spans_sum_rule_differs_from_union_rule", "spans",
                         "spans_negative_handling", "baseline_traces", "baseline_used", "baseline_dropped_no_root", "baseline_dropped_orphan", "baseline_dropped_gt_1s"), vals):
        add("4", f"bước đếm {d} {field}", v, N, ["summary", d, field])
for d, lo, hi in (("RE2-TT", 388, 1566), ("Nezha-OB", 348, 861)):
    add("4", f"bước đếm {d} trace nền dùng được nhỏ nhất", lo, N, ["summary", d, "baseline_used_per_case", "min"])
    add("4", f"bước đếm {d} trace nền dùng được lớn nhất", hi, N, ["summary", d, "baseline_used_per_case", "max"])

MP = "runs/microrank-partition-001/collect-001/summary.json"
add("4", "nhánh giữ nguyên khớp", 52, MP, ["summary", "self_check", "sham_exact"])
add("4", "nhánh giữ nguyên hạng trùng T-028", 52, MP, ["summary", "self_check", "sham_rank_equals_t028"])
for d, n, vals in (("RE2-TT", 25, {"mo15": (10.0, 55, 139, 70.3, 19, 3, 3, 14, 23, 13, 110, 17), "mo1p50": (12.3, 54, 163, 62.7, 20, 2, 3, 15, 23, 12, 111, 13)}),
                   ("Nezha-OB", 22, {"mo15": (1.5, 2, 12.0, 52.0, 15, 3, 4, 7, 14, 53, 67, 13), "mo1p50": (2.6, 1, 21.0, 53.4, 13, 5, 4, 7, 14, 55, 65, 12)})):
    for b, v in vals.items():
        base = ["summary", d, b]
        add("4", f"{d} {b} số ca tính được", n, MP, base + ["evaluable"])
        add("4", f"{d} {b} tỷ lệ trace bất thường %", v[0], MP, base + ["abnormal_share", b, "median"], "pct1")
        add("4", f"{d} {b} số trace bất thường nhỏ nhất", v[1], MP, base + ["new_abnormal_count", "min"])
        add("4", f"{d} {b} số trace bất thường trung vị", v[2], MP, base + ["new_abnormal_count", "median"])
        add("4", f"{d} {b} tỷ lệ có root %", v[3], MP, base + ["abnormal_share_with_root_service", b, "median"], "pct1")
        add("4", f"{d} {b} root tăng", v[4], MP, base + ["root_effect", "tăng hạng"])
        add("4", f"{d} {b} root không đổi", v[5], MP, base + ["root_effect", "không đổi"])
        add("4", f"{d} {b} root giảm", v[6], MP, base + ["root_effect", "giảm hạng"])
        add("4", f"{d} {b} Hit@1", v[7], MP, base + ["hit1", b])
        add("4", f"{d} {b} Hit@5", v[8], MP, base + ["hit5", b])
        add("4", f"{d} {b} cặp còn", v[9], MP, base + ["pairs_above_root_native", "still_above"])
        add("4", f"{d} {b} cặp mất", v[10], MP, base + ["pairs_above_root_native", "gone"])
        add("4", f"{d} {b} cặp mới", v[11], MP, base + ["pairs_above_root_native", "new_pairs"])
for d, h1, h5, share, root, pairs in (("RE2-TT", 2, 13, 50.1, 51.7, 123), ("Nezha-OB", 0, 8, 33.0, 29.1, 120)):
    add("4", f"{d} gốc Hit@1", h1, MP, ["summary", d, "mo15", "hit1", "native"])
    add("4", f"{d} gốc Hit@5", h5, MP, ["summary", d, "mo15", "hit5", "native"])
    add("4", f"{d} gốc tỷ lệ trace bất thường %", share, MP, ["summary", d, "mo15", "abnormal_share", "native", "median"], "pct1")
    add("4", f"{d} gốc tỷ lệ có root %", root, MP, ["summary", d, "mo15", "abnormal_share_with_root_service", "native", "median"], "pct1")
    add("4", f"{d} gốc số cặp", pairs, MP, ["summary", d, "mo15", "pairs_above_root_native", "n"])
for b, h1, gone in (("mo15", 21, 177), ("mo1p50", 22, 176)):
    add("4", f"gộp {b} Hit@1", h1, MP, ["summary", "all", b, "hit1", b])
    add("4", f"gộp {b} cặp mất", gone, MP, ["summary", "all", b, "pairs_above_root_native", "gone"])
add("4", "gộp số cặp", 243, MP, ["summary", "all", "mo15", "pairs_above_root_native", "n"])
add("4", "gộp số ca tính được", 47, MP, ["summary", "all", "mo15", "evaluable"])
for e, v in (("ts-station-service", 20), ("ts-route-service", 3)):
    add("4", f"RE2 gốc đứng đầu {e}", v, MP, ["summary", "RE2-TT", "mo15", "top_entity_when_root_not_first", "native", e])
for e, v in (("ts-auth-service", 7), ("ts-admin-travel-service", 2)):
    add("4", f"RE2 mo15 đứng đầu {e}", v, MP, ["summary", "RE2-TT", "mo15", "top_entity_when_root_not_first", "mo15", e])
for e, v in (("cartservice", 7), ("frontend", 2), ("adservice", 2), ("recommendationservice", 1)):
    add("4", f"Nezha mo15 đứng đầu {e}", v, MP, ["summary", "Nezha-OB", "mo15", "top_entity_when_root_not_first", "mo15", e])
for f, a, n in (("cpu", 3, 6), ("delay", 3, 4), ("disk", 3, 6), ("loss", 2, 5), ("mem", 2, 2), ("socket", 1, 2)):
    add("4", f"RE2 mo15 lỗi {f} Hit@1", a, MP, ["summary", "RE2-TT", "mo15", "by_fault", f, "hit1_branch"])
    add("4", f"RE2 mo15 lỗi {f} số ca", n, MP, ["summary", "RE2-TT", "mo15", "by_fault", f, "evaluable"])
for f, a, c, n in (("cpu_consumed", 2, 3, 4), ("cpu_contention", 1, 1, 5), ("exception", 1, 1, 3), ("network_delay", 1, 2, 6), ("return", 2, 0, 4)):
    add("4", f"Nezha mo15 lỗi {f} Hit@1", a, MP, ["summary", "Nezha-OB", "mo15", "by_fault", f, "hit1_branch"])
    add("4", f"Nezha mo1p50 lỗi {f} Hit@1", c, MP, ["summary", "Nezha-OB", "mo1p50", "by_fault", f, "hit1_branch"])
    add("4", f"Nezha lỗi {f} số ca", n, MP, ["summary", "Nezha-OB", "mo15", "by_fault", f, "evaluable"])

LR = "runs/torai-log-remaining-001/summary.json"
for ptr, v in ((["rebuild_equals_saved"], 29), (["top_service_kept_columns", "ts-order-other-service"], 9), (["top_service_all_columns", "ts-order-other-service"], 14),
               (["top_service_kept_columns", "ts-order-service"], 4), (["top_service_kept_columns", "ts-seat-service"], 4),
               (["top3_membership_kept", "ts-order-other-service"], 16), (["top3_membership_kept", "ts-seat-service"], 15), (["top3_membership_kept", "ts-order-service"], 12),
               (["top_service_kept_is_root"], 1), (["top_column_of_top_service", "n"], 29), (["top_column_of_top_service", "baseline_nonzero_bins_le_3"], 17),
               (["top_column_of_top_service", "baseline_nonzero_bins_median"], 1), (["top_column_of_top_service", "direction", "tăng"], 23),
               (["top_columns_order_other_and_seat", "n"], 31), (["top_columns_order_other_and_seat", "baseline_nonzero_bins_le_3"], 22),
               (["top_columns_order_other_and_seat", "direction", "tăng"], 29)):
    add("6", "cột log còn lại " + "/".join(ptr), v, LR, ["summary"] + ptr)

SC = "runs/tracerca-score-contrast-001/summary.json"
add("8", "nhánh giữ nguyên hạng trùng bản đóng băng", 48, SC, ["summary", "self_check", "sham_ranks_equal_frozen"])
for d, n, vals in (("RE2-TT", 26, {"tr1": (13, 16, 4, 11, 11, 3, 5, 11, 21, 4, 11, 71, 10), "tr1m": (14, 17, 4, 11, 11, 3, 5, 10, 21, 4, 11, 61, 11), "ts": (14, 21, 0, 16, 10, 0, 5, 7, 21, 14, 1, 22, 17)}),
                   ("Nezha-OB", 21, {"tr1": (6, 16, 10, 4, 7, 6, 19, 2, 2, 32, 43, 12, 8), "tr1m": (7, 17, 11, 4, 6, 6, 19, 1, 2, 29, 46, 11, 9), "ts": (2, 12, 3, 10, 8, 0, 19, 0, 2, 68, 7, 13, 15)})):
    for b, v in vals.items():
        base = ["summary", d, b]
        add("8", f"{d} {b} số ca root được xếp", n, SC, base + ["root_ranked_native"])
        for ptr, x in zip((["hit1", b], ["hit5", b], ["root_effect", "tăng hạng"], ["root_effect", "không đổi"], ["root_effect", "giảm hạng"], ["native_wrong", "become_rank1"],
                           ["native_wrong", "n"], ["native_right", "lose_rank1"], ["native_right", "n"], ["pairs_above_root_native", "still_above"],
                           ["pairs_above_root_native", "gone"], ["pairs_above_root_native", "new_pairs"], ["top_entity_same_as_native"]), v):
            add("8", f"{d} {b} {'/'.join(ptr)}", x, SC, base + ptr)
for d, h1, h5 in (("RE2-TT", 21, 25), ("Nezha-OB", 2, 11)):
    add("8", f"{d} gốc Hit@1", h1, SC, ["summary", d, "tr1", "hit1", "native"])
    add("8", f"{d} gốc Hit@5", h5, SC, ["summary", d, "tr1", "hit5", "native"])

TO = "runs/tracerca-original-ranking-001/summary.json"
for d, b, vals in (("RE2-TT", "to_p", (22, 8, 14, 12, 12, 40, 22, 6, 0, 1, 3, 10.7, 18.3, 18, 13, 9)), ("RE2-TT", "to_p3", (22, 8, 15, 12, 14, 41, 21, 6, 0, 1, 3, 1.7, 11.7, 18, 13, 9)),
                   ("Nezha-OB", "to_p", (11, 11, 7, 0, 7, 3, 4, 7, 0, 1, 7, 7.3, 9.2, 10, 1, 0)), ("Nezha-OB", "to_p3", (11, 11, 11, 2, 11, 8, 1, 5, 2, 1, 5, 2.4, 3.9, 10, 1, 2))):
    base = ["summary", d, b]
    items = [(["status", "OK"], vals[0], None), (["status", "NO_USEFUL_FEATURE"], vals[1], None), (["root_score_positive"], vals[2], None), (["hit1"], vals[3], None), (["hit5"], vals[4], None),
             (["direct_caller_pairs", "root trên"], vals[5], None), (["direct_caller_pairs", "hòa"], vals[6], None), (["direct_caller_pairs", "root dưới"], vals[7], None),
             (["waiting_caller_pairs_library", "hòa"], vals[9], None), (["waiting_caller_pairs_library", "root dưới"], vals[10], None),
             (["abnormal_share_before_same_rule_median"], vals[11], "pct1"), (["abnormal_share_after_median"], vals[12], "pct1"),
             (["library_comparison", "cases_both_ranked"], vals[13], None), (["library_comparison", "hit1_library"], vals[14], None), (["library_comparison", "hit1_branch"], vals[15], None)]
    if vals[8]:
        items.append((["waiting_caller_pairs_library", "root trên"], vals[8], None))
    for ptr, x, r in items:
        add("9", f"{d} {b} {'/'.join(ptr)}", x, TO, base + ptr, r)
add("9", "RE2 to_p đứng đầu ts-route-service", 8, TO, ["summary", "RE2-TT", "to_p", "top_entities", "ts-route-service"])
add("9", "RE2 to_p3 đứng đầu ts-route-service", 11, TO, ["summary", "RE2-TT", "to_p3", "top_entities", "ts-route-service"])
add("9", "Nezha to_p đứng đầu frontend", 11, TO, ["summary", "Nezha-OB", "to_p", "top_entities", "frontend"])
add("9", "Nezha to_p3 đứng đầu frontend", 9, TO, ["summary", "Nezha-OB", "to_p3", "top_entities", "frontend"])
add("9", "RE2 to_c xếp được", 22, TO, ["summary", "RE2-TT", "to_c", "ranked_cases"])
add("9", "RE2 to_c Hit@1", 12, TO, ["summary", "RE2-TT", "to_c", "hit1"])
add("9", "Nezha to_c xếp được", 9, TO, ["summary", "Nezha-OB", "to_c", "ranked_cases"])
add("9", "Nezha to_c Hit@1", 1, TO, ["summary", "Nezha-OB", "to_c", "hit1"])


def resolve(data, pointer):
    for key in pointer:
        data = data[key] if not isinstance(data, list) else data[int(key)]
    return data


def main():
    cache, rows, bad = {}, [], 0
    for c in CLAIMS:
        data = cache.setdefault(c["file"], json.loads((ROOT / c["file"]).read_text(encoding="utf-8")))
        pointers = c["pointer"] if isinstance(c["pointer"][0], list) else [c["pointer"]]
        try:
            value = sum(resolve(data, p) for p in pointers) if len(pointers) > 1 else resolve(data, pointers[0])
        except (KeyError, IndexError, TypeError) as error:
            value, c["error"] = None, type(error).__name__ + ": " + str(error)
        shown = value
        if value is not None and c["rounding"] == "pct1":
            shown = round(value * 100, 1)
        elif value is not None and isinstance(c["rounding"], int):
            shown = round(value, c["rounding"])
        ok = shown is not None and abs(float(shown) - float(c["reported"])) < 1e-9
        bad += not ok
        rows.append({**c, "file_value": value, "compared": shown, "match": ok})
    out = Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"schema": "T032-self-check-phien11-v1", "claims": len(rows), "mismatch": bad, "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        if not r["match"]:
            print("LỆCH", r["section"], r["what"], "báo cáo", r["reported"], "file", r["compared"], r.get("error", ""))
    print("claims", len(rows), "mismatch", bad)


if __name__ == "__main__":
    main()

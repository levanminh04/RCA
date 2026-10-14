"""T-032 phiên 10: tự soát số trong ket-qua-phien-10.md với file kết quả (Q-131 mục 14). Chạy trên laptop, chỉ đọc.

Mỗi dòng: (mục trong ket-qua-phien-10.md, điều được viết, file, con trỏ hoặc cách tính, giá trị viết trong báo cáo). Script đọc file,
lấy giá trị thật và so. Số thực được so sau khi làm tròn đúng số chữ số đã viết. Không sửa file nào ngoài file kết quả của chính nó.
Dùng: python self_check_phien10_v1.py <file kết quả mới>
"""
import json
import sys
from pathlib import Path

BASE = Path("D:/RCA-flashticket/results/T-032")
CACHE = {}


def load(rel):
    if rel not in CACHE:
        CACHE[rel] = json.loads((BASE / rel).read_text(encoding="utf-8-sig"))
    return CACHE[rel]


def get(rel, pointer):
    value = load(rel)
    for part in [p for p in pointer.split("/") if p]:
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


K2 = "runs/circa-laptop-k2-001/collect-001/summary.json"
REG = "runs/circa-laptop-k2-001/collect-002/regression-decomposition.json"
MD = "runs/microrank-md-001/collect-001/summary.json"
A = "runs/root-signal-location-001/summary.json"
P3 = "runs/root-signal-placebo-003/summary.json"
B = "runs/baseline-trend-001/summary.json"
TS = "runs/torai-severity-table-003/summary.json"
TL = "runs/torai-log-source-001/summary.json"
TP = "runs/torai-log-placebo-001/summary.json"
FP = "runs/source-fingerprint-001/fingerprint.json"
SEM = "runs/trace-semantics-002/semantics.json"
CI = "runs/call-interval-001/summary.json"
CS = "runs/call-slow-001/summary.json"

K2E = "runs/circa-laptop-k2-edges-001/collect-001/summary.json"
TC = "runs/torai-log-contrast-001/summary.json"
S1 = "runs/torai-log-contrast-seeds-001/summary.json"
S2 = "runs/torai-log-contrast-seeds-002/summary.json"

CLAIMS_78 = [
    ("7", "k2x còn 11 ca có nút cực lớn", K2E, "/summary/all/cases_with_huge_node/k2x", 11),
    ("7", "k2s còn 11 ca có nút cực lớn", K2E, "/summary/all/cases_with_huge_node/k2s", 11),
    ("7", "không cạnh 0 ca", K2E, "/summary/all/cases_with_huge_node/k2", 0),
    ("7", "native 3.285 nút cao hơn không cạnh", K2E, "/summary/all/score_above_no_edges/native", 3285),
    ("7", "k2x 2.920", K2E, "/summary/all/score_above_no_edges/k2x", 2920),
    ("7", "k2s 687", K2E, "/summary/all/score_above_no_edges/k2s", 687),
    ("7", "nút còn cha k2x 3.968", K2E, "/summary/all/regressed_nodes_still_with_parents/k2x", 3968),
    ("7", "nút còn cha k2s 986", K2E, "/summary/all/regressed_nodes_still_with_parents/k2s", 986),
    ("7", "Hit@1 native 12", K2E, "/summary/all/hit1/native", 12),
    ("7", "Hit@1 k2x 13", K2E, "/summary/all/hit1/k2x", 13),
    ("7", "Hit@1 k2s 12", K2E, "/summary/all/hit1/k2s", 12),
    ("7", "Hit@1 k2 21", K2E, "/summary/all/hit1/k2", 21),
    ("7", "Hit@5 26/24/25/24", K2E, "/summary/all/hit5/k2s", 25),
    ("7", "19 ca: Hit@1 k2x 13", K2E, "/summary/cases_without_huge_node/hit1/k2x", 13),
    ("7", "19 ca: Hit@5 native 17", K2E, "/summary/cases_without_huge_node/hit5/native", 17),
    ("7", "19 ca: Hit@5 k2s 16", K2E, "/summary/cases_without_huge_node/hit5/k2s", 16),
    ("7", "11 ca: Hit@1 k2x 0", K2E, "/summary/cases_with_huge_node/hit1/k2x", 0),
    ("7", "k2x tăng 7", K2E, "/summary/all/effect_vs_native/k2x/tăng hạng", 7),
    ("7", "k2x giảm 4", K2E, "/summary/all/effect_vs_native/k2x/giảm hạng", 4),
    ("7", "k2s tăng 3", K2E, "/summary/all/effect_vs_native/k2s/tăng hạng", 3),
    ("7", "k2s giảm 8", K2E, "/summary/all/effect_vs_native/k2s/giảm hạng", 8),
    ("7", "caller còn 10 dưới k2x", K2E, "/summary/all/pairs_above_root_native/k2x/caller_of_root|còn trên root", 10),
    ("7", "caller còn 14 dưới k2s", K2E, "/summary/all/pairs_above_root_native/k2s/caller_of_root|còn trên root", 14),
    ("7", "5 cặp caller mất thuộc nhóm có nút cực lớn", K2E, "/summary/cases_with_huge_node/pairs_above_root_native/k2x/caller_of_root|không còn trên root", 5),
    ("7", "cạnh bị bỏ k2x 3.709", K2E, "/summary/all/edges_removed/k2x", 3709),
    ("7", "cạnh bị bỏ k2s 7.220", K2E, "/summary/all/edges_removed/k2s", 7220),
    ("8", "sham trùng lượt gốc 30", TC, "/summary/sham_equals_native", 30),
    ("8", "hạng sham trùng T-028 30", TC, "/summary/self_check_sham_rank_equals_t028", 30),
    ("8", "Hit@1 native 26", TC, "/summary/sham/hit1", 26),
    ("8", "Hit@1 tl2 26", TC, "/summary/tl2/hit1", 26),
    ("8", "Hit@1 tl1 29 (seed 0)", TC, "/summary/tl1/hit1", 29),
    ("8", "Hit@5 tl2 29", TC, "/summary/tl2/hit5", 29),
    ("8", "tl2: 1 ca sai thành đúng", TC, "/summary/tl2/native_wrong/becomes_hit1", 1),
    ("8", "tl2: 1 ca đúng mất hạng 1", TC, "/summary/tl2/native_hit1/loses_hit1", 1),
    ("8", "tl1: 3 ca sai thành đúng (seed 0)", TC, "/summary/tl1/native_wrong/becomes_hit1", 3),
    ("8", "tl1: 0 ca đúng mất hạng 1", TC, "/summary/tl1/native_hit1/loses_hit1", 0),
    ("8", "số cột log 382", TC, "/summary/tl2/log_columns_in_median", 382),
    ("8", "còn 263 cột dưới tl2", TC, "/summary/tl2/log_columns_out_median", 263),
    ("8", "kiểm seed lượt 1: 11 cặp", S1, "/summary/pairs_checked", 11),
    ("8", "lượt 1: 10 cặp giống", S1, "/summary/root_rank_same_across_seeds", 10),
    ("8", "kiểm seed lượt 2: 10 cặp", S2, "/summary/pairs_checked", 10),
    ("8", "lượt 2: 10 cặp giống", S2, "/summary/root_rank_same_across_seeds", 10),
]

CLAIMS = [
    # mục 1
    ("1.1", "sham khớp 30/30", K2, "/summary/sham_exact", 30),
    ("1.1", "nhánh quan sát khớp 30/30", K2, "/summary/obs_exact", 30),
    ("1.1", "điểm RHT trung gian trùng bản ghi 30/30", K2, "/summary/obs/snapshot_rht_equals_record", 30),
    ("1.1", "hạng root có DA trùng T-028 30/30", K2, "/summary/self_check_da_rank_equals_t028", 30),
    ("1.1", "DA: tăng 5", K2, "/summary/da_effect_on_root/tăng hạng", 5),
    ("1.1", "DA: không đổi 15", K2, "/summary/da_effect_on_root/không đổi", 15),
    ("1.1", "DA: giảm 10", K2, "/summary/da_effect_on_root/giảm hạng", 10),
    ("1.2", "11 ca có nút cực lớn", K2, "/summary/obs/cases_with_huge_node", 11),
    ("1.2", "luôn nút ts-admin-travel-service_latency (11)", K2, "/summary/obs/huge_node_names/ts-admin-travel-service_latency", 11),
    ("1.2", "y train 2 giá trị ở 11 nút", K2, "/summary/obs/huge_node_train_y_n_unique/2", 11),
    ("1.2", "không cạnh: 0 nút cực lớn", K2, "/summary/obs/huge_nodes_still_huge_without_edges", 0),
    ("1.2", "huge_k2 = 0", K2, "/summary/k2_all/node_counts_total/huge_k2", 0),
    ("1.3", "41 nút nhận qua child_score", K2, "/summary/obs/da_huge_by_source_total/nhận qua child_score", 41),
    ("1.3", "11 nút tự có", K2, "/summary/obs/da_huge_by_source_total/tự có", 11),
    ("1.3", "root có nút DA cực lớn ở 3 ca", K2, "/summary/obs/cases_root_has_da_huge_node", 3),
    ("1.3", "7/10 ca giảm có thực thể trên root mang khóa cực lớn", K2, "/summary/da_changed_cases_by_huge/giảm hạng/entity_above_root_under_da_is_huge", 7),
    ("1.3", "cạnh cùng dịch vụ 7.220", K2, "/summary/obs/edge_direction_vs_calls_total/cùng dịch vụ", 7220),
    ("1.3", "cạnh từ dịch vụ được gọi sang dịch vụ gọi 1.642", K2, "/summary/obs/edge_direction_vs_calls_total/từ dịch vụ được gọi sang dịch vụ gọi", 1642),
    ("1.3", "cạnh chiều ngược 1.344", K2, "/summary/obs/edge_direction_vs_calls_total/từ dịch vụ gọi sang dịch vụ được gọi", 1344),
    ("1.4", "30 ca: tăng 12", K2, "/summary/k2_all/removing_edges_effect_on_root/tăng hạng", 12),
    ("1.4", "30 ca: không đổi 14", K2, "/summary/k2_all/removing_edges_effect_on_root/không đổi", 14),
    ("1.4", "30 ca: giảm 4", K2, "/summary/k2_all/removing_edges_effect_on_root/giảm hạng", 4),
    ("1.4", "Hit@1 có cạnh 12", K2, "/summary/k2_all/hit1/native_rht", 12),
    ("1.4", "Hit@1 không cạnh 21", K2, "/summary/k2_all/hit1/k2_rht", 21),
    ("1.4", "Hit@5 26 → 24", K2, "/summary/k2_all/hit5/native_rht", 26),
    ("1.4", "Hit@5 không cạnh 24", K2, "/summary/k2_all/hit5/k2_rht", 24),
    ("1.4", "11 ca: tăng 10", K2, "/summary/k2_cases_with_huge_node/removing_edges_effect_on_root/tăng hạng", 10),
    ("1.4", "11 ca: Hit@1 0 → 9", K2, "/summary/k2_cases_with_huge_node/hit1/k2_rht", 9),
    ("1.4", "19 ca: 2/13/4", K2, "/summary/k2_cases_without_huge_node/removing_edges_effect_on_root/không đổi", 13),
    ("1.4", "19 ca: Hit@1 12 → 12", K2, "/summary/k2_cases_without_huge_node/hit1/k2_rht", 12),
    ("1.4", "19 ca: Hit@5 17", K2, "/summary/k2_cases_without_huge_node/hit5/native_rht", 17),
    ("1.4", "19 ca: Hit@5 không cạnh 15", K2, "/summary/k2_cases_without_huge_node/hit5/k2_rht", 15),
    ("1.4", "4.526 nút có hồi quy", K2, "/summary/k2_all/node_counts_total/native_route_linear_regression", 4526),
    ("1.4", "3.285 nút điểm native cao hơn", K2, "/summary/k2_all/node_counts_total/regression_raises_score", 3285),
    ("1.4", "1.161 nút thấp hơn", K2, "/summary/k2_all/node_counts_total/regression_lowers_score", 1161),
    ("1.4", "80 nút bằng nhau", K2, "/summary/k2_all/node_counts_total/regression_natively_but_unchanged", 80),
    ("1.4", "cặp caller còn 7", K2, "/summary/k2_all/pairs_above_root_native_rht_under_k2/caller_of_root|còn trên root", 7),
    ("1.4", "cặp caller mất 8", K2, "/summary/k2_all/pairs_above_root_native_rht_under_k2/caller_of_root|không còn trên root", 8),
    ("1.4", "cặp khác còn 54, mất 17", K2, "/summary/k2_all/pairs_above_root_native_rht_under_k2/other|không còn trên root", 17),
    ("1.4", "4.407 nút phân rã được", REG, "/summary/all_nodes/n", 4407),
    ("1.4", "f_num >= 1 ở 2.588 nút", REG, "/summary/all_nodes/f_num_ge_1", 2588),
    ("1.4", "trung vị f_den 0,93", REG, "/summary/all_nodes/median_f_den", ("round", 2, 0.93)),
    ("1.4", "tỷ số 1,05 với 1 cha", REG, "/summary/by_n_parents/1/median_ratio_native_over_without", ("round", 2, 1.05)),
    ("1.4", "tỷ số 8,43 với >= 8 cha", REG, "/summary/by_n_parents/8/median_ratio_native_over_without", ("round", 2, 8.43)),
    # mục 2
    ("2", "sham M-D khớp 52/52", MD, "/summary/sham_exact", 52),
    ("2", "48 OK + 4 ERROR", MD, "/summary/sham_exact_by_source_status/ERROR", 4),
    ("2", "hạng native trùng T-028 48", MD, "/summary/self_check_native_rank_equals_t028", 48),
    ("2", "root tăng 3", MD, "/summary/all/md_effect_on_root/tăng hạng", 3),
    ("2", "không đổi 35", MD, "/summary/all/md_effect_on_root/không đổi", 35),
    ("2", "giảm 10", MD, "/summary/all/md_effect_on_root/giảm hạng", 10),
    ("2", "Hit@1 2 → 4", MD, "/summary/all/hit1/md", 4),
    ("2", "Hit@5 21 → 20", MD, "/summary/all/hit5/md", 20),
    ("2", "cặp caller còn 19", MD, "/summary/all/pairs_above_root_native_under_md/caller_of_root|còn trên root", 19),
    ("2", "cặp mới 17", MD, "/summary/all/pairs_newly_above_root_under_md", 17),
    ("2", "số span mang cờ còn 0,74", MD, "/summary/all/abnormal_spans_ratio_md_over_native/median", ("round", 2, 0.74)),
    # mục 3
    ("3", "tự kiểm own_d 48/48", A, "/summary/self_check/own_d_total_equals_H_native", 48),
    ("3", "tự kiểm own_u 48/48", A, "/summary/self_check/own_u_total_equals_H_u", 48),
    ("3", "RE2 own_d đứng đầu 8", A, "/summary/by_dataset/RE2-TT/positions/own_d/root_first", 8),
    ("3", "RE2 own_u đứng đầu 26", A, "/summary/by_dataset/RE2-TT/positions/own_u/root_first", 26),
    ("3", "RE2 in_d 18/20", A, "/summary/by_dataset/RE2-TT/positions/in_d/root_first", 18),
    ("3", "RE2 in_u 19/20", A, "/summary/by_dataset/RE2-TT/positions/in_u/root_first", 19),
    ("3", "RE2 in_d_edge 18/20", A, "/summary/by_dataset/RE2-TT/positions/in_d_edge/root_first", 18),
    ("3", "Nezha own_d 9", A, "/summary/by_dataset/Nezha-OB/positions/own_d/root_first", 9),
    ("3", "Nezha own_u 10", A, "/summary/by_dataset/Nezha-OB/positions/own_u/root_first", 10),
    ("3", "Nezha in_d 11", A, "/summary/by_dataset/Nezha-OB/positions/in_d/root_first", 11),
    ("3", "Nezha in_u 13", A, "/summary/by_dataset/Nezha-OB/positions/in_u/root_first", 13),
    ("3", "thử giả RE2 own_d 1", P3, "/summary/by_dataset/RE2-TT/positions/own_d/root_first", 1),
    ("3", "thử giả RE2 own_u 0", P3, "/summary/by_dataset/RE2-TT/positions/own_u/root_first", 0),
    ("3", "thử giả RE2 in_d 2", P3, "/summary/by_dataset/RE2-TT/positions/in_d/root_first", 2),
    ("3", "thử giả Nezha own_d 4", P3, "/summary/by_dataset/Nezha-OB/positions/own_d/root_first", 4),
    ("3", "thử giả Nezha in_u 4", P3, "/summary/by_dataset/Nezha-OB/positions/in_u/root_first", 4),
    ("3", "RE2 chỉ phía gọi 18", A, "/summary/by_dataset/RE2-TT/cross/incoming_first_only", 18),
    ("3", "Nezha không vị trí nào 5", A, "/summary/by_dataset/Nezha-OB/cross/neither", 5),
    ("3", "network_delay in_u 5/6", A, "/summary/by_dataset_fault/Nezha-OB|network_delay/positions/in_u/root_first", 5),
    ("3", "network_delay own_d 1/6", A, "/summary/by_dataset_fault/Nezha-OB|network_delay/positions/own_d/root_first", 1),
    ("3", "return: 3/4 không vị trí nào", A, "/summary/by_dataset_fault/Nezha-OB|return/cross/neither", 3),
    # mục 4
    ("4", "z khớp 30/30", B, "/summary/baro_z_bit_exact", 30),
    ("4", "phiếu khớp 30/30", B, "/summary/simple_votes_match_decomposition", 30),
    ("4", "1.966 cột mem", B, "/summary/all_columns_no_label/baro_view/mem/n_columns", 1966),
    ("4", "574 cột trôi nền", B, "/summary/all_columns_no_label/baro_view/mem/by_group/trôi nền", 574),
    ("4", "trung vị drift_ratio 0,94", B, "/summary/all_columns_no_label/baro_view/mem/drift_ratio/median", ("round", 2, 0.94)),
    ("4", "226 cột mem >= 250 phiếu", B, "/summary/all_columns_no_label/baro_view/mem/votes_ge_250", 226),
    ("4", "BARO 103 cột thắng trên root", B, "/summary/winning_columns/baro/above_root|ca sai hạng 1/n", 103),
    ("4", "BARO mem trôi nền 19", B, "/summary/winning_columns/baro/above_root|ca sai hạng 1/by_kind_group/mem|trôi nền", 19),
    ("4", "BARO trung vị 0,61", B, "/summary/winning_columns/baro/above_root|ca sai hạng 1/drift_ratio/median", ("round", 2, 0.61)),
    ("4", "SimpleRCA mem trôi nền 6", B, "/summary/winning_columns/simple/above_root|ca sai hạng 1/by_kind_group/mem|trôi nền", 6),
    ("4", "SimpleRCA trung vị 0,24", B, "/summary/winning_columns/simple/above_root|ca sai hạng 1/drift_ratio/median", ("round", 2, 0.24)),
    # mục 5
    ("5", "severity = trung bình hàng 90", TS, "/summary/checks/y_train_equals_row_mean", 90),
    ("5", "hạng root trùng T-028 90", TS, "/summary/self_check_rank_equals_t028", 90),
    ("5", "ba seed cùng trung gian 30", TS, "/summary/cases_three_seeds_same_pre_rcd_intermediates", 30),
    ("5", "Hit@1 26", TS, "/summary/seed0/hit1", 26),
    ("5", "root severity cao nhất ở 26 ca đúng", TS, "/summary/seed0/root_severity_rank_is_1_among_hit1", 26),
    ("5", "0 ca sai có severity cao nhất", TS, "/summary/seed0/root_severity_rank_is_1_among_wrong", 0),
    ("5", "7 cặp", TS, "/summary/seed0/pairs_above_root", 7),
    ("5", "2 cặp cùng cụm", TS, "/summary/seed0/pairs_above_root_same_cluster", 2),
    ("5", "log là nguồn chênh lớn nhất 7/7", TS, "/summary/seed0/pairs_above_root_largest_source_difference/log", 7),
    ("5", "trace_err rỗng 30", TS, "/summary/seed0/root_source_value_is_zero/trace_err", 30),
    ("5", "root đứng đầu metric 23", TS, "/summary/seed0/root_source_rank_is_1/metric", 23),
    ("5", "trace_lat 22", TS, "/summary/seed0/root_source_rank_is_1/trace_lat", 22),
    ("5", "log 2", TS, "/summary/seed0/root_source_rank_is_1/log", 2),
    ("5", "cụm root một dịch vụ 27", TS, "/summary/seed0/root_cluster_size/1", 27),
    ("5", "rebuild log 29", TL, "/summary/rebuild_ok", 29),
    ("5", "order-other đứng đầu log 14", TL, "/summary/top_service_by_log/ts-order-other-service", 14),
    ("5", "root đứng đầu log 2", TL, "/summary/top_service_is_root", 2),
    ("5", "cột cao nhất nền không đổi 20/29", TL, "/summary/top_service_top_column_std_N_zero", 20),
    ("5", "55% điểm log", TL, "/summary/log_mass_on_std_N_zero_columns/median", ("round", 2, 0.55)),
    ("5", "27% số cột", TL, "/summary/share_of_scored_columns_all_zero_N/median", ("round", 2, 0.27)),
    ("5", "7/7 cặp cột nền không đổi", TL, "/summary/wrong_cases/pairs_where_entity_top_log_column_has_std_N_zero", 7),
    ("5", "thử giả: order-other 20/29", TP, "/summary/placebo_top_service_by_log/ts-order-other-service", 20),
    ("5", "thử giả 39%", TP, "/summary/placebo_log_mass_on_std_zero_columns/median", ("round", 2, 0.39)),
    ("5", "trace_err tổng mọi ô bằng 0 ở 30 ca", TP, "/summary/trace_err/cases_sum_all_cells_zero", 30),
    # mục 6
    ("6.1", "55 tên span Nezha", FP, "/online_boutique/span_names", 55),
    ("6.1", "19 chuỗi nguyên văn không có ở kho gốc", FP, "/online_boutique/literal_in_service_but_not_in_upstream", 19),
    ("6.1", "31 rpc", FP, "/online_boutique/by_class/rpc trong demo.proto (span do thư viện gRPC tạo)", 31),
    ("6.1", "58 route v0.2.0", FP, "/train_ticket/tags/v0.2.0/routes_found", 58),
    ("6.1", "0 route ở 0.0.1", FP, "/train_ticket/tags/0.0.1/routes_found", 0),
    ("6.1", "54 route ở v1.0.0", FP, "/train_ticket/tags/v1.0.0/routes_found", 54),
    ("6.2", "63 loại lời gọi đồng bộ ở mọi tag", SEM, "/source_scan/train_ticket/call_kinds_synchronous_in_every_candidate", 63),
    ("6.2", "18 loại lời gọi OB đồng bộ", SEM, "/source_scan/online_boutique/call_kinds_synchronous", 18),
    ("6.2", "left_parallel không có trong dữ liệu", SEM, "/source_scan/facts/re2_left_parallel_route_observed", False),
    ("6.4", "RE2 21 ca có cạnh", CS, "/summary/RE2-TT/cases_with_edge_to_root", 21),
    ("6.4", "RE2 19 ca >= 50%", CS, "/summary/RE2-TT/cases_max_to_root_slow_share_after_ge_0_5", 19),
    ("6.4", "RE2 20 ca >= 20%", CS, "/summary/RE2-TT/cases_max_to_root_slow_share_after_ge_0_2", 20),
    ("6.4", "Nezha 16 ca có cạnh", CS, "/summary/Nezha-OB/cases_with_edge_to_root", 16),
    ("6.4", "Nezha 10 ca >= 50%", CS, "/summary/Nezha-OB/cases_max_to_root_slow_share_after_ge_0_5", 10),
    ("6.4", "Nezha 12 ca >= 20%", CS, "/summary/Nezha-OB/cases_max_to_root_slow_share_after_ge_0_2", 12),
    ("6.4", "delay 97% trong span root", CS, "/summary/RE2-TT/by_fault/delay/slow_calls_inside_root_span_share", ("round", 2, 0.97)),
    ("6.4", "socket 42%", CS, "/summary/RE2-TT/by_fault/socket/slow_calls_inside_root_span_share", ("round", 2, 0.42)),
    ("6.4", "mem 56%", CS, "/summary/RE2-TT/by_fault/mem/slow_calls_inside_root_span_share", ("round", 2, 0.56)),
    ("6.4", "network_delay 0,5%", CS, "/summary/Nezha-OB/by_fault/network_delay/slow_calls_inside_root_span_share", ("round", 3, 0.005)),
    ("6.4", "cpu_contention 48% (bản đầu viết 49%, lượt 001 bắt được, đã sửa trong báo cáo)", CS, "/summary/Nezha-OB/by_fault/cpu_contention/slow_calls_inside_root_span_share", ("round", 2, 0.48)),
    ("6.4", "cpu_consumed 91%", CS, "/summary/Nezha-OB/by_fault/cpu_consumed/slow_calls_inside_root_span_share", ("round", 2, 0.91)),
    ("6.4", "disk 79%", CS, "/summary/RE2-TT/by_fault/disk/slow_calls_inside_root_span_share", ("round", 2, 0.79)),
    ("6.4", "loss 76%", CS, "/summary/RE2-TT/by_fault/loss/slow_calls_inside_root_span_share", ("round", 2, 0.76)),
    ("6.4", "cpu 74%", CS, "/summary/RE2-TT/by_fault/cpu/slow_calls_inside_root_span_share", ("round", 2, 0.74)),
    ("6.5", "RE2 đo được có điều kiện 21", SEM, "/summary/RE2-TT/by_level/đo được (có điều kiện)", 21),
    ("6.5", "RE2 không đo được 9", SEM, "/summary/RE2-TT/by_level/không đo được", 9),
    ("6.5", "Nezha đo được có điều kiện 16", SEM, "/summary/Nezha-OB/by_level/đo được (có điều kiện)", 16),
    ("6.5", "Nezha không đo được 6", SEM, "/summary/Nezha-OB/by_level/không đo được", 6),
    ("6.5", "auth 6 ca", SEM, "/summary/RE2-TT/not_measurable_roots/ts-auth-service", 6),
]


def main():
    out = Path(sys.argv[1])
    rows, bad = [], 0
    for section, text, rel, pointer, expected in CLAIMS + CLAIMS_78:
        try:
            actual = get(rel, pointer)
            if isinstance(expected, tuple):
                ok = round(actual, expected[1]) == expected[2]
                shown = expected[2]
            else:
                ok = actual == expected
                shown = expected
            error = None
        except Exception as exc:  # con trỏ sai cũng là lỗi của báo cáo
            actual, ok, shown, error = None, False, expected if not isinstance(expected, tuple) else expected[2], type(exc).__name__ + ": " + str(exc)[:120]
        bad += not ok
        rows.append({"section": section, "claim": text, "file": rel, "pointer": pointer, "written": shown, "actual": actual, "match": ok, "error": error})
    # con số tính từ từng ca, không có sẵn trong summary
    ci = load(CI)
    import statistics
    for dataset, key, written, digits in (("RE2-TT", "nested_share", 0.851, 3), ("RE2-TT", "post_negative_share", 0.148, 3), ("RE2-TT", "gap_negative_share", 0.0025, 4),
                                          ("Nezha-OB", "nested_share", 0.997, 3), ("Nezha-OB", "gap_negative_share", 0.0, 3)):
        values = [c["all_calls"]["before"][key] for c in ci["cases"] if c["dataset"] == dataset and c["status"] == "OK"]
        actual = statistics.median(values)
        ok = round(actual, digits) == written
        bad += not ok
        rows.append({"section": "6.3", "claim": dataset + " trung vị " + key + " ở nền", "file": CI, "pointer": "/cases/*/all_calls/before/" + key + " (trung vị)",
                     "written": written, "actual": actual, "match": ok, "error": None})
    result = {"schema": "T032-self-check-phien10-v1", "n_claims": len(rows), "n_mismatch": bad, "rows": rows}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=1)
        stream.write("\n")
    print("claims", len(rows), "mismatch", bad)
    for r in rows:
        if not r["match"]:
            print("LỆCH", r["section"], r["claim"], "| viết:", r["written"], "| thật:", r["actual"], "|", r["error"] or "")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

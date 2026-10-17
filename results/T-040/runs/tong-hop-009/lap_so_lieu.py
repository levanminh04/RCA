"""Lập results/T-040/so-lieu.json: mỗi số trong báo cáo .md ↔ đoạn chữ ↔ con trỏ JSON.

Giá trị được đọc từ tệp kết quả tại thời điểm lập; kiem_tra.py K4 đọc lại và so.
Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-009/lap_so_lieu.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
TH = "results/T-040/tong-hop.json"
DV = "results/T-040/dau-vao.json"
T35 = "results/T-035/do-phu-theo-nhan.json"
B = "bao-cao-p5b.md"
P6 = "ban-giao-p6.md"
P9 = "yeu-cau-quan-sat-p9.md"


def m(sys_, k):
    return TH + "#/he_thong/%s/mo_hinh_tinh/so_dem/%s" % (sys_, k)


def fam(sys_, f, view, k, sub=None):
    p = TH + "#/he_thong/%s/doi_chieu/ho_graph/%s/views/%s/%s" % (sys_, f, view, k)
    return p + ("/" + sub if sub else "")


def kc(sys_, k):
    return TH + "#/he_thong/%s/mo_hinh_tinh/kieu_canh_kenh/%s" % (sys_, k)


def ma(sys_, k):
    return TH + "#/he_thong/%s/mo_hinh_tinh/dia_chi_messaging/%s" % (sys_, k)


ROW_INV = "| Thực thể trong inventory | 32 | 110 | 23 |"
ROW_REC = "| Bản ghi quan hệ | 115 | 513 | 82 |"
ROW_EE = "| Cạnh mức thực thể | 72 | 170 | 22 |"
ROW_OP = "| Thao tác | 65 | 993 | 68 |"
ROW_RN = "| Thao tác chưa có tên runtime | 65 | 993 | 47 |"
ROW_OE = "| Cạnh mức thao tác | 55 | 343 | 71 |"
ROW_PJ = "| Cạnh chiếu từ thao tác | 17 | 122 | 18 |"
ROW_EO = "| Cạnh chỉ ở mức thực thể | 55 | 48 | 4 |"
ROW_BD = "| Binding tài nguyên | 14 | 50 | 2 |"
ROW_SG = "| Địa chỉ tín hiệu (dùng chung) | 153 (23) | 139 (139) | 53 (14) |"

E = []


def add(file, snippet, pointer=None, **kw):
    E.append(dict(file=file, snippet=snippet, pointer=pointer, **kw))


# ---- bao-cao-p5b.md
add(B, "đã băm theo 9 manifest", DV + "#/manifest", op="len")
add(B, "8 manifest khớp toàn bộ", DV + "#/manifest_khop_toan_bo")
add(B, "11.009 tệp của T-038", DV + "#/manifest/6/files")
add(B, "2.277 tệp của run sửa R1", DV + "#/manifest/7/files")
add(B, "5.667 tệp của T-035", DV + "#/manifest/1/files")
add(B, "lệch đúng ba tệp mã chung", DV + "#/manifest/2/mismatch", op="len", word=True, expect=3)
for sys_, i in [("FT", 0), ("TT", 1), ("OB", 2)]:
    add(B, ROW_INV, m(sys_, "inventory"))
    add(B, ROW_REC, m(sys_, "relation_records"))
    add(B, ROW_EE, m(sys_, "entity_edges"))
    add(B, ROW_OP, m(sys_, "operations"))
    add(B, ROW_RN, m(sys_, "operations_runtime_name_null"))
    add(B, ROW_OE, m(sys_, "operation_edges"))
    add(B, ROW_PJ, m(sys_, "projection_edges"))
    add(B, ROW_EO, m(sys_, "entity_only_edges"))
    add(B, ROW_BD, m(sys_, "resource_bindings"))
    add(B, ROW_SG, m(sys_, "signals"))
    add(B, ROW_SG, m(sys_, "signals_shared"))
add(B, "11 cạnh gọi HTTP", kc("FT", "gọi-đồng-bộ|http"))
add(B, "12 cạnh dữ liệu", kc("FT", "dữ-liệu|data"))
add(B, "31 cạnh thông điệp (9 phát", op="sum_of", pointers=[kc("FT", "thông-điệp|publish"), kc("FT", "thông-điệp|consume"), kc("FT", "thông-điệp|logical-message")])
add(B, "(9 phát, 11 nhận, 11 logic)", kc("FT", "thông-điệp|publish"))
add(B, "(9 phát, 11 nhận, 11 logic)", kc("FT", "thông-điệp|consume"))
add(B, "(9 phát, 11 nhận, 11 logic)", kc("FT", "thông-điệp|logical-message"))
add(B, "17 cạnh triển khai", kc("FT", "triển-khai|deployment"))
add(B, "1 cạnh SMTP", kc("FT", "gọi-chưa-phân-kiểu|smtp"))
add(B, "(14 RPC, 4 HTTP) và 4 cạnh dữ liệu", kc("OB", "gọi-đồng-bộ|rpc"))
add(B, "(14 RPC, 4 HTTP) và 4 cạnh dữ liệu", kc("OB", "gọi-đồng-bộ|http"))
add(B, "(14 RPC, 4 HTTP) và 4 cạnh dữ liệu", kc("OB", "dữ-liệu|data"))
add(B, "Cả 31 cạnh thông điệp của FlashTicket thiếu `broker_scope`", op="sum_of",
    pointers=[ma("FT", "publish|missing:broker_scope"), ma("FT", "consume|missing:broker_scope,queue"),
              ma("FT", "logical-message|missing:broker_scope,queue")])
add(B, "22 cạnh nhận/logic thiếu cả queue", op="sum_of",
    pointers=[ma("FT", "consume|missing:broker_scope,queue"), ma("FT", "logical-message|missing:broker_scope,queue")])
add(B, "FlashTicket có 130 địa chỉ gắn thao tác", m("FT", "signals_with_operation"))
add(B, "Online Boutique có 22 (", m("OB", "signals_with_operation"))
add(B, "0 lỗi trên 1.069 graph TT và 132 graph OB", TH + "#/he_thong/TT/doi_chieu/so_graph")
add(B, "0 lỗi trên 1.069 graph TT và 132 graph OB", TH + "#/he_thong/OB/doi_chieu/so_graph")
add(B, "0 lỗi trên 1.069 graph TT và 132 graph OB", TH + "#/he_thong/TT/doi_chieu/loi_tinh_lai", op="len")
add(B, "0 lỗi trên 1.069 graph TT và 132 graph OB", TH + "#/he_thong/OB/doi_chieu/loi_tinh_lai", op="len")
add(B, "mọi 13 khóa trace đủ điều kiện đều có trong 22 khóa tĩnh", fam("OB", "entity:full", "endpoints", "T", "max"))
add(B, "mọi 13 khóa trace đủ điều kiện đều có trong 22 khóa tĩnh", fam("OB", "entity:full", "endpoints", "S", "max"))
for f in ["entity:A", "entity:N", "entity:full"]:
    add(B, "Không có cạnh chỉ có ở trace ở bất kỳ graph nào.", fam("OB", f, "endpoints", "TO", "max"), word=True, expect=0)
add(B, "Cửa sổ A có graph chỉ còn 11 khóa trace", fam("OB", "entity:A", "endpoints", "T", "min"))
add(B, "N và toàn miền luôn 13", fam("OB", "entity:N", "endpoints", "T", "min"))
add(B, "N và toàn miền luôn 13", fam("OB", "entity:full", "endpoints", "T", "min"))
add(B, "9 khóa tĩnh vắng ở mọi graph thực thể", fam("OB", "entity:full", "endpoints", "static_only_in_every_graph"))
add(B, "6 cặp có đích không xuất hiện trong trace", TH + "#/lan_theo/OB_static_only_every_full_graph/classification/target_not_observed")
add(B, "2 cặp có nguồn không xuất hiện", TH + "#/lan_theo/OB_static_only_every_full_graph/classification/source_not_observed")
add(B, "1 cặp cả hai đầu đều quan sát được", TH + "#/lan_theo/OB_static_only_every_full_graph/classification/both_observed_no_edge")
add(B, "10 khóa trace đủ điều kiện, đều có trong 71 khóa tĩnh", fam("OB", "operation:full", "endpoints", "T", "max"))
add(B, "10 khóa trace đủ điều kiện, đều có trong 71 khóa tĩnh", fam("OB", "operation:full", "endpoints", "S", "max"))
add(B, "32 cặp vì nguồn chưa xác minh", fam("OB", "operation:full", "endpoints", "trace_exclusion_pairs_by_reason", "unverified_mapping:source"))
add(B, "17 cặp vì đích chưa xác minh", fam("OB", "operation:full", "endpoints", "trace_exclusion_pairs_by_reason", "unverified_mapping:target"))
add(B, "4 cặp vì đích chưa ánh xạ", fam("OB", "operation:full", "endpoints", "trace_exclusion_pairs_by_reason", "unmapped:target"))
for f in ["entity:A", "entity:N", "entity:full", "operation:A", "operation:N", "operation:full"]:
    add(B, "T rỗng ở 22 graph mỗi họ, tức toàn bộ 132 graph", fam("OB", f, "typed", "graphs_T_empty"))
add(B, "T có từ 16 đến 49 khóa", fam("TT", "entity:full", "endpoints", "T", "min"))
add(B, "T có từ 16 đến 49 khóa", fam("TT", "entity:full", "endpoints", "T", "max"))
add(B, "hợp qua 30 ca là 49 khóa", fam("TT", "entity:full", "endpoints", "union_T"))
add(B, "hợp qua 30 ca là 49 khóa", TH + "#/he_thong/TT/doi_chieu/ho_graph/entity:full/graphs")
add(B, "Đầu mút của mọi khóa T thuộc 24 service", TH + "#/he_thong/TT/doi_chieu/dau_mut_khoa_T/entity", op="len")
add(B, "19 trong 739 ảnh chụp 60 giây có T rỗng", fam("TT", "entity:s60", "endpoints", "graphs_T_empty"))
add(B, "19 trong 739 ảnh chụp 60 giây có T rỗng", TH + "#/he_thong/TT/doi_chieu/ho_graph/entity:s60/graphs")
add(B, "Hai tên trace không có ánh xạ", TH + "#/he_thong/TT/doi_chieu/nut_trace_chua_anh_xa_muc_thuc_the/unmapped", op="len", word=True, expect=2)
add(B, "T rỗng ở cả 979 graph thực thể và 90 graph thao tác", op="sum_of",
    pointers=[fam("TT", f, "typed", "graphs_T_empty") for f in ["entity:A", "entity:N", "entity:full", "entity:s300", "entity:s60"]])
add(B, "T rỗng ở cả 979 graph thực thể và 90 graph thao tác", op="sum_of",
    pointers=[fam("TT", f, "typed", "graphs_T_empty") for f in ["operation:A", "operation:N", "operation:full"]])
for f in ["operation:A", "operation:N", "operation:full"]:
    add(B, "T rỗng ở 30 graph mỗi họ", fam("TT", f, "endpoints", "graphs_T_empty"))
add(B, "Train Ticket có 132 cạnh gọi HTTP, 30 cạnh dữ liệu, 6 cạnh thông điệp (4 phát, 2 nhận), 1 cạnh SMTP và 1 cạnh HTTP chưa phân kiểu", kc("TT", "gọi-đồng-bộ|http"))
add(B, "Train Ticket có 132 cạnh gọi HTTP, 30 cạnh dữ liệu, 6 cạnh thông điệp (4 phát, 2 nhận), 1 cạnh SMTP và 1 cạnh HTTP chưa phân kiểu", kc("TT", "dữ-liệu|data"))
add(B, "6 cạnh thông điệp (4 phát, 2 nhận)", op="sum_of", pointers=[kc("TT", "thông-điệp|publish"), kc("TT", "thông-điệp|consume")])
add(B, "6 cạnh thông điệp (4 phát, 2 nhận)", kc("TT", "thông-điệp|publish"))
add(B, "6 cạnh thông điệp (4 phát, 2 nhận)", kc("TT", "thông-điệp|consume"))
add(B, "1 cạnh SMTP và 1 cạnh HTTP chưa phân kiểu", kc("TT", "gọi-chưa-phân-kiểu|smtp"))
add(B, "1 cạnh SMTP và 1 cạnh HTTP chưa phân kiểu", kc("TT", "gọi-chưa-phân-kiểu|http"))
add(B, "S có 164 khóa endpoints và 162 khóa typed ở mọi graph", fam("TT", "entity:full", "endpoints", "S", "min"))
add(B, "S có 164 khóa endpoints và 162 khóa typed ở mọi graph", fam("TT", "entity:s60", "endpoints", "S", "max"))
add(B, "S có 164 khóa endpoints và 162 khóa typed ở mọi graph", fam("TT", "entity:full", "typed", "S", "min"))
add(B, "Phần riêng tĩnh toàn ca từ 120 đến 149 khóa", fam("TT", "entity:full", "endpoints", "SO", "min"))
add(B, "Phần riêng tĩnh toàn ca từ 120 đến 149 khóa", fam("TT", "entity:full", "endpoints", "SO", "max"))
add(B, "120 khóa tĩnh vắng ở mọi graph thực thể", fam("TT", "entity:s60", "endpoints", "static_only_in_every_graph"))
O5 = "results/T-040/runs/tong-hop-005/tong-hop.json"
add(B, "S tăng từ 160 lên 164 khóa endpoints, từ 159 lên 162 khóa typed", O5 + "#/he_thong/TT/doi_chieu/ho_graph/entity:full/views/endpoints/S/min")
add(B, "S tăng từ 160 lên 164 khóa endpoints, từ 159 lên 162 khóa typed", fam("TT", "entity:full", "endpoints", "S", "min"))
add(B, "S tăng từ 160 lên 164 khóa endpoints, từ 159 lên 162 khóa typed", O5 + "#/he_thong/TT/doi_chieu/ho_graph/entity:full/views/typed/S/min")
add(B, "S tăng từ 160 lên 164 khóa endpoints, từ 159 lên 162 khóa typed", fam("TT", "entity:full", "typed", "S", "min"))
add(B, "thêm 4 bản ghi quan hệ và 4 cạnh thực thể", op="minus", pointers=[m("TT", "relation_records"), O5 + "#/he_thong/TT/mo_hinh_tinh/so_dem/relation_records"])
add(B, "thêm 4 bản ghi quan hệ và 4 cạnh thực thể", op="minus", pointers=[m("TT", "entity_edges"), O5 + "#/he_thong/TT/mo_hinh_tinh/so_dem/entity_edges"])
add(B, "(cạnh chiếu vẫn 122)", m("TT", "projection_edges"))
add(B, "Giao mức thực thể toàn ca từ 15 đến 44 khóa", fam("TT", "entity:full", "endpoints", "I", "min"))
add(B, "Giao mức thực thể toàn ca từ 15 đến 44 khóa", fam("TT", "entity:full", "endpoints", "I", "max"))
add(B, "44 khóa; 5 cặp chỉ có ở trace", fam("TT", "entity:full", "endpoints", "union_trace_only"))
add(B, "không thuộc 24 service của T", TH + "#/he_thong/TT/doi_chieu/dau_mut_khoa_T/entity", op="len")
add(B, "Ở cả 5 cặp, span phía gọi", TH + "#/lan_theo/TT_trace_only_vs_intersection/trace_only/summary/caller_method_only")
add(B, "44 cặp khớp đối chứng có cùng dạng này", TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/caller_method_only")
add(B, "Nhưng 25 trong 44 cặp khớp cũng vậy", op="minus",
    pointers=[TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/pairs",
              TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/callee_has_any_static_caller"])
add(B, "chỉ 19 cặp có bên gọi tĩnh", TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/callee_has_any_static_caller")
add(B, "handler phía nhận của 5 cặp không có bên gọi tĩnh nào", TH + "#/lan_theo/TT_trace_only_vs_intersection/trace_only/summary/pairs")
add(B, "handler phía nhận của 5 cặp không có bên gọi tĩnh nào", TH + "#/lan_theo/TT_trace_only_vs_intersection/trace_only/summary/callee_has_any_static_caller", word=True, expect=0)
add(B, "Trên 22 graph toàn miền (mỗi ca một graph), currency chỉ có bên gọi là frontend", TH + "#/he_thong/OB/doi_chieu/ho_graph/entity:full/graphs")
add(B, "Trên 22 graph toàn miền (mỗi ca một graph), currency chỉ có bên gọi là frontend", TH + "#/lan_theo/OB_static_only_every_full_graph/rows/2/target_called_by_in_trace", op="len", word=True, expect=1)
add(B, "checkout có span phía gọi cho 7 lời gọi RPC đi ra khác", TH + "#/lan_theo/OB_static_only_every_full_graph/rows/2/source_other_cross_entity_calls_in_trace", op="len")

add(B, "Ở cả 25 cặp khớp đó, mô hình tĩnh có cạnh từ thao tác phía gọi", TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/no_static_caller_but_op_to_component_edge")
add(B, "Ở 5 cặp chỉ có ở trace, mô hình tĩnh không có cạnh nào", TH + "#/lan_theo/TT_trace_only_vs_intersection/trace_only/summary/no_static_caller_and_no_static_op_edge")

# ---- Phiên 5: static-only TT (N2) và ma trận hai đầu OB (N3)
TS = TH + "#/lan_theo/TT_static_only_every_full_graph"
add(B, "13 khóa có cả hai đầu quan sát được, 23 chỉ nguồn, 54 chỉ đích, 30 không đầu nào", TS + "/endpoint_matrix/src_obs|tgt_obs")
add(B, "13 khóa có cả hai đầu quan sát được, 23 chỉ nguồn, 54 chỉ đích, 30 không đầu nào", TS + "/endpoint_matrix/src_obs|tgt_not")
add(B, "13 khóa có cả hai đầu quan sát được, 23 chỉ nguồn, 54 chỉ đích, 30 không đầu nào", TS + "/endpoint_matrix/src_not|tgt_obs")
add(B, "13 khóa có cả hai đầu quan sát được, 23 chỉ nguồn, 54 chỉ đích, 30 không đầu nào", TS + "/endpoint_matrix/src_not|tgt_not")
add(B, "(hợp qua 30 graph toàn ca)", TH + "#/he_thong/TT/doi_chieu/ho_graph/entity:full/graphs")
add(B, "Ở cả 13 cặp, hai đầu cùng có mặt ở 24 hoặc 30 trong 30 ca", TS + "/both_observed_pairs")
add(B, "Ở cả 13 cặp, hai đầu cùng có mặt ở 24 hoặc 30 trong 30 ca", TS + "/rows/0/cases_both_endpoints_full")
add(B, "Ở cả 13 cặp, hai đầu cùng có mặt ở 24 hoặc 30 trong 30 ca", TS + "/rows/1/cases_both_endpoints_full")
add(B, "Ở cả 13 cặp, hai đầu cùng có mặt ở 24 hoặc 30 trong 30 ca", TH + "#/he_thong/TT/doi_chieu/ho_graph/entity:full/graphs")
add(B, "hai đầu cùng có mặt ở 27–32 graph mức thực thể", TS + "/rows/6/entity_graphs_both_present_per_case/0")
add(B, "hai đầu cùng có mặt ở 27–32 graph mức thực thể", TS + "/rows/0/entity_graphs_both_present_per_case/1")
add(B, "Có 11 cặp mà thao tác nguồn tĩnh chỉ là candidate", TS + "/both_observed_source_op_unverified_candidate")
add(B, "trong đó 3 cặp có cả hai đầu không xuất hiện", TH + "#/lan_theo/OB_static_only_every_full_graph/endpoint_matrix/src_not|tgt_not")
add(B, "Mười ba khóa tĩnh Train Ticket", TS + "/both_observed_pairs", word=True, expect=13)

# ---- ban-giao-p6.md
add(P6, "| 32 thực thể: service", m("FT", "inventory"))
add(P6, "| 153 địa chỉ theo B16; 130 gắn thao tác; 23 dùng chung |", m("FT", "signals"))
add(P6, "| 153 địa chỉ theo B16; 130 gắn thao tác; 23 dùng chung |", m("FT", "signals_with_operation"))
add(P6, "| 153 địa chỉ theo B16; 130 gắn thao tác; 23 dùng chung |", m("FT", "signals_shared"))
add(P6, "| 23 thực thể gồm DB, cache, external |", m("OB", "inventory"))
add(P6, "| 53 khai báo địa chỉ |", m("OB", "signals"))
add(P6, "| 110 thực thể |", m("TT", "inventory"))
add(P6, "Trên OB, mọi 4 cạnh dữ liệu tĩnh đều vắng ở trace", kc("OB", "dữ-liệu|data"))
add(P6, "tên runtime trống ở 65/65 thao tác FT", m("FT", "operations_runtime_name_null"))
add(P6, "tên runtime trống ở 65/65 thao tác FT", m("FT", "operations"))
add(P6, "993/993 thao tác TT", m("TT", "operations_runtime_name_null"))
add(P6, "993/993 thao tác TT", m("TT", "operations"))
add(P6, "47/68 ở OB", m("OB", "operations_runtime_name_null"))
add(P6, "47/68 ở OB", m("OB", "operations"))
add(P6, "Root không được gọi (8 ca), cạnh thưa (7 ca)", T35 + "#/totals/no_incoming")
add(P6, "Root không được gọi (8 ca), cạnh thưa (7 ca)", T35 + "#/totals/too_sparse")
add(P6, "graph tĩnh OB (22 cạnh, gồm DB)", m("OB", "entity_edges"))
add(P6, "Graph tĩnh thêm 9 cạnh không bao giờ quan sát được trong dev", fam("OB", "entity:full", "endpoints", "static_only_in_every_graph"))
add(P6, "6 trong số đó có đích không phải nút trace", TH + "#/lan_theo/OB_static_only_every_full_graph/classification/target_not_observed")
add(P6, "5 cặp chỉ có ở trace. Ngược lại, 120 khóa tĩnh vắng", fam("TT", "entity:full", "endpoints", "union_trace_only"))
add(P6, "5 cặp chỉ có ở trace. Ngược lại, 120 khóa tĩnh vắng", fam("TT", "entity:full", "endpoints", "static_only_in_every_graph"))
add(P6, "Trên OB chỉ 10 cạnh thao tác đủ điều kiện", fam("OB", "operation:full", "endpoints", "T", "max"))
add(P6, "Trong 120 khóa, 13 có cả hai đầu quan sát được", TS + "/static_only_every_full_graph")
add(P6, "Trong 120 khóa, 13 có cả hai đầu quan sát được", TS + "/both_observed_pairs")
add(P6, "qua `ts-ticketinfo-service` (4)", TS + "/both_observed_with_same_graph_path_via_unmapped")

# ---- yeu-cau-quan-sat-p9.md
XR = TH + "#/lan_theo/TT_trace_only_vs_intersection/operation_cross_owner_trace_exclusions"
add(P9, "Cả 1.640 lần loại cạnh trace thao tác khác owner", XR + "/total_over_30_full_graphs")
add(P9, "Cả 1.640 lần loại cạnh trace thao tác khác owner", op="sum_of", pointers=[XR + "/method_only_caller_by_reason/ambiguous_mapping:source", XR + "/method_only_caller_by_reason/unverified_mapping:source", XR + "/method_only_caller_by_reason/unmapped:source"])
add(P9, "1.286 mơ hồ, 300 chưa xác minh, 54 chưa ánh xạ", XR + "/method_only_caller_by_reason/ambiguous_mapping:source")
add(P9, "1.286 mơ hồ, 300 chưa xác minh, 54 chưa ánh xạ", XR + "/method_only_caller_by_reason/unverified_mapping:source")
add(P9, "1.286 mơ hồ, 300 chưa xác minh, 54 chưa ánh xạ", XR + "/method_only_caller_by_reason/unmapped:source")
add(P9, "(cộng qua 30 graph toàn ca", TH + "#/he_thong/TT/doi_chieu/ho_graph/operation:full/graphs")
add(P9, "44/44 cặp khớp mức thực thể cũng có span phía gọi dạng này", TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/caller_method_only")
add(P9, "44/44 cặp khớp mức thực thể cũng có span phía gọi dạng này", TH + "#/lan_theo/TT_trace_only_vs_intersection/intersection_control/summary/pairs")
add(P9, "FT: 65/65 thao tác chưa có tên runtime", m("FT", "operations_runtime_name_null"))
add(P9, "FT: 65/65 thao tác chưa có tên runtime", m("FT", "operations"))
add(P9, "OB: cả 4 cạnh dữ liệu tĩnh vắng ở mọi graph", kc("OB", "dữ-liệu|data"))
add(P9, "đối chiếu 11 cạnh HTTP của mô hình T-037", kc("FT", "gọi-đồng-bộ|http"))
add(P9, "12 cạnh dữ liệu và 14 binding của T-037", kc("FT", "dữ-liệu|data"))
add(P9, "12 cạnh dữ liệu và 14 binding của T-037", m("FT", "resource_bindings"))
add(P9, "FT: cả 31 cạnh thông điệp thiếu broker_scope", op="sum_of",
    pointers=[ma("FT", "publish|missing:broker_scope"), ma("FT", "consume|missing:broker_scope,queue"),
              ma("FT", "logical-message|missing:broker_scope,queue")])
add(P9, "22 cạnh nhận/logic thiếu queue", op="sum_of",
    pointers=[ma("FT", "consume|missing:broker_scope,queue"), ma("FT", "logical-message|missing:broker_scope,queue")])
add(P9, "17 cạnh triển khai của FT là thiết kế", kc("FT", "triển-khai|deployment"))


def resolve(obj, ptr):
    cur = obj
    for part in [x for x in ptr.lstrip("/").split("/")] if ptr not in ("", "/") else []:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


cache = {}


def val(ptr):
    f, p = ptr.split("#", 1)
    if f not in cache:
        cache[f] = json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
    return resolve(cache[f], p)


out = []
for i, e in enumerate(E):
    op = e.get("op")
    if op == "sum_of":
        v = sum(val(x) for x in e["pointers"])
    elif op == "minus":
        v = val(e["pointers"][0]) - val(e["pointers"][1])
    elif op == "len":
        v = len(val(e["pointer"]))
    else:
        v = val(e["pointer"])
    if "expect" in e and v != e["expect"]:
        raise SystemExit("expect mismatch %s: %r != %r" % (e["snippet"], v, e["expect"]))
    rec = {"id": "S%03d" % (i + 1), "file": e["file"], "snippet": e["snippet"], "value": v}
    if e.get("pointer"):
        rec["pointer"] = e["pointer"]
    if e.get("pointers"):
        rec["pointers"] = e["pointers"]
    if op:
        rec["op"] = op
    if e.get("word"):
        rec["word"] = True
    out.append(rec)
reg = {"schema": "T040-so-lieu-v1", "run": json.load(open(os.path.join(ROOT, TH.split("#")[0]), encoding="utf-8"))["run"],
       "y_nghia": "Mỗi mục: đoạn chữ trong báo cáo, con trỏ JSON tới tệp kết quả, phép (len/sum_of/minus) nếu có, và giá trị đọc được khi lập. kiem_tra.py K4 đọc lại và so.",
       "entries": out}
with open(os.path.join(ROOT, "results/T-040/so-lieu.json"), "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(reg, ensure_ascii=False, indent=1) + "\n")
print(len(out))

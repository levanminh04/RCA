# Đề xuất hoàn tất nguồn hậu xử lý bridge MicroRank — chờ Minh duyệt

## Chỗ lỗi, bằng chứng và hậu quả

Bridge-002 đã thực hiện đúng phạm vi: thêm helper `source` nguyên AST; 11/11 fixture đạt. Lượt audit ca RE2 đã lưu `microrank-re2-posthoc-001` vẫn FAIL và đã dừng theo lời duyệt. Comparator record đạt, native–observed exact; bridge chưa đạt tự kiểm bản T-028 đóng băng. Không có lượt phương pháp mới/cohort/A′ dùng kết quả này.

Verdict `t028-check.json → /differences` có đúng một khác biệt: `/frozen_self_check/evidence/graph_role`, nguồn có trường nhưng bản dựng lại thiếu. Nguyên nhân: bridge chỉ chạy `analysis_rows`, chưa chạy phép gắn chú thích ở bước cuối của nguồn T-028. Trong snapshot `results/T-028/runs/phan-hoi-review-001/scripts-final/tong_hop_bao_cao.py`, dòng 312 gắn `graph_role` theo tên phương pháp. Đây là chú thích về vai trò đồ thị phân tích; không được bỏ khỏi phép so hay coi đó là đồ thị native MicroRank.

Snapshot này có hash trong manifest cuối T-028. Phép gắn nguyên bản là:

```python
r['evidence']['graph_role'] = 'analysis_context_not_input_to_BARO_TORAI' if r['method'] in ('baro', 'torai_B') else 'analysis_graph_not_claimed_native_method_graph'
```

## Thay đổi đề nghị và ảnh hưởng

Chỉ tạo bốn bản mới trong `results/T-032/scripts/`, giữ mọi bản/lượt cũ:

1. `check_microrank_t028_v3.py`: giữ bridge v2; đọc snapshot hậu xử lý với hash từ manifest cuối T-028. Xác định duy nhất phép gắn `graph_role` nguyên AST trong đúng hàm nguồn, kiểm cấu trúc đích/điều kiện và dùng nguyên phép gắn ấy cho cả hàng frozen dựng lại và observed dựng lại trước so. Không chạy phần import, main, IO hay tổng hợp còn lại. Không chép mù giá trị từ hàng đã lưu. Thêm fixture cho annotation nguyên nguồn và phát hiện bỏ/sửa role; tự kiểm riêng đủ52 hàng nguồn frozen để phát hiện thiếu bước trước ca mới. Tự kiểm frozen không cấp verdict native/observed/eligibility cho52 ca chưa phát lại. Giữ self-check và so mọi trường cũ.
2. `replay_microrank_approved_v3.py`, `audit_microrank_posthoc_v3.py`, `batch_microrank_approved_v3.py`: chỉ đổi filename/pin bridge/wrapper v3 tương ứng; không đổi native/observer/comparator, tiêu chí số hay invariant.

Chuyển đúng snapshot T-028 còn thiếu nếu cần theo quyền chuyển nguồn đã duyệt; kiểm hash hai đầu, inventory/LOG. Không sửa T-028, SPEC, Q-94/Q-95, WHY-42 hay bản đóng băng. Khác biệt này là lỗi chưa tái hiện đủ pipeline của bộ kiểm, không là bằng chứng MicroRank đổi cờ/hạng hoặc cơ chế RCA sai.

## Kiểm và chi phí

Trước chạy: soát toàn bộ khác biệt giữa pipeline dựng lại và đầu ra cuối T-028, không chỉ dòng vừa lỗi; soát AST/source-binding và full diff/pin chain. Sau đó một fixture mới và một audit ca RE2 đã lưu; ngân sách gộp tối đa 120 giây máy, 15 MiB mới, guard nền/fail-stop. Lỗi thì dừng và trình, không tiếp ca MicroRank mới/cohort/A′ trong lượt sửa. Ngưỡng MicroRank và mọi invariant giữ đúng Q-94/WHY-42.

## Dòng quyết định xin phép nối

Đọc lại DECISIONS ngay trước nối đúng một dòng Q-96, giữ mọi dòng cũ:

| Q-96 | 10/10/2026 | Minh duyệt đúng de-xuat-microrank-bridge-003.md: bridge v3 tái hiện nguyên AST bước hậu xử lý graph_role của nguồn T-028, giữ toàn bộ self-check/trường so, chỉ đổi pin/filename downstream; giữ mọi bản/lượt cũ và ngưỡng/invariant/SPEC/WHY-42; một fixture + một audit ca RE2 đã lưu tối đa 120 giây/15 MiB, lỗi dừng/trình, chưa chạy ca MicroRank mới/cohort/A′ trong lượt sửa. | lời duyệt Minh trong chat; results/T-032/de-xuat-microrank-bridge-003.md |

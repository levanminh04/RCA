# Đề xuất sửa bộ kiểm MicroRank — chờ Minh duyệt

## Chỗ lỗi, bằng chứng và hậu quả

`check_microrank_t028.py` nạp nguyên các định nghĩa AST được chọn từ bản code T-028 có hash trong manifest. Danh sách `ANALYSIS_FUNCTIONS` thiếu `source`, trong khi `analysis_rows` gọi hàm này tại dòng 239 và 255 của `results/T-028/runs/phan-hoi-review-001/scripts-final/thuc_hien_buoc3_6.py`. Hàm `source` ở dòng 59 chỉ trả `{'path': str(path), 'json_pointer': pointer}`; không đọc tệp, không chạy phương pháp, không đổi điểm/cờ.

Lượt `microrank-t028-fixture-003` đã đủ nguồn (closure 113 tệp: 30 RE2 và 22 Nezha, hash hai đầu PASS), nhưng dừng `NameError: name 'source' is not defined` trước khi có verdict fixture. Supervisor/worker 141345/141348; elapsed 6,418 giây; exit 1. Hai lượt trước dừng vì thiếu tệp nguồn, đã giữ toàn bộ. Chưa có lượt phương pháp mới hay A′ dùng bộ kiểm này. Chưa được coi bridge/cờ M đã đạt.

## Thay đổi đề nghị và phạm vi ảnh hưởng

Chỉ tạo phiên bản mới trong `results/T-032/scripts/`, giữ mọi bản cũ và lượt lỗi:

1. `check_microrank_t028_v2.py`: giữ nguyên bản hiện tại; thêm đúng định nghĩa `source` từ snapshot T-028 đã kiểm hash vào danh sách AST nạp. Thêm kiểm fixture cho giá trị path/pointer của hàm nguồn. Không thực thi top-level runner/import/write của snapshot. Soát toàn bộ dependency global của các hàm AST đã chọn trước lần chạy tiếp.
2. `replay_microrank_approved_v2.py`: giữ native/observer/comparator/invariant/guard; chỉ trỏ bridge v2 và khóa hash mới.
3. `audit_microrank_posthoc_v2.py`: giữ việc audit ca RE2 cũ, không chạy phương pháp; chỉ trỏ bridge v2 và khóa hash mới.
4. `batch_microrank_approved_v2.py`: controller chuẩn bị/chạy cohort chỉ trỏ wrapper/bridge v2 cùng hash mới. Chưa chạy cohort trong lượt sửa này.

Ghi inventory/hash hai đầu, kết quả và checkpoint vào `results/T-032/runs/` và LOG T-032. Không sửa SPEC, Q-94, WHY-42, kết quả T-028 hay code dùng chung. Không đổi ngưỡng 16 ULP/tương đối, tie/order/Hit/cờ M, không cấp ngoại lệ cho CIRCA/phương pháp khác.

## Kiểm và chi phí

Sau Minh duyệt: AST/soát diff bản mới, kiểm hash nguồn và script hai đầu, chạy một fixture bridge mới rồi audit ca RE2 đã lưu. Dự toán tối đa 2 phút máy, 15 MiB mới; chạy trong guard nền, dừng ngay nếu bất kỳ kiểm nào không đạt. Không tự thử thêm vòng sửa khi lỗi. Không chạy MicroRank Nezha/cohort/A′ trước khi hai kiểm đạt và ngân sách/điều kiện các bước ấy được kiểm riêng.

Việc phát lại trên laptop vẫn là phương án thay thế đã trình trong đề xuất MicroRank-001; sửa thiếu helper của bộ kiểm không thay được phép kiểm cờ M, kể cả trên laptop. Vì bridge đã dừng ba lượt, trình Minh theo AGENTS §5a.1 trước lần tiếp; đây là sửa bộ kiểm, không thay cách tính hay tiêu chí khoa học đã duyệt.

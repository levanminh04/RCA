# TORAI A — tạm hoãn vô thời hạn (08/11/2026)

**Quyết định của Minh:** "bỏ torai A, ghi trong tài liệu là tạm hoãn vô thời hạn trừ khi sau này cần đến, ghi đầy đủ lỗi tìm được để sau này còn xem lại nếu cần".

## Trạng thái

- TORAI A là bảng phụ ngoài A4. A4, bảng chính và mọi kết luận RQ3b/RQ3d không phụ thuộc A.
- Đã có: 6/180 slot VERIFIED trên 3 ca (`cda8dfc162` 3 seed, `2a0c838e6b` 2 seed, `edaa68b4cf` 1 seed), trong `results/T-054/runs/main-013-v2/queue/`. Slot `cda8dfc162` seed 1 có khoảng mất quan sát 342 s do laptop ngủ (LOG T-054).
- Thiếu: 174 slot BLOCKED (1 slot lỗi kiểm danh tính, 173 `A_QUEUE_HALTED_BEFORE_DISPATCH`); 2 ca thiếu bộ ba seed. Bảng A trong `reports/main-013-v2/tables.json#/missing`.
- Không sửa file đã ghim nào; không dựng plan/protocol mới.

## Lỗi đã tìm được

**Hiện tượng.** Slot `torai_A test-2a0c838e6b seed 2` (job `585e37aa…`, attempt-001) BLOCKED ở bước giám sát stage prepare với thông báo "PID pha không phải worker con của launcher" (`results/T-054/scripts/dieu_phoi.py:212–235`, hàm `bind_actual_process`). Prep đã ghi đủ `prepared.json`; pha cuối kết thúc 17:43:01,76 UTC, chỉ ~0,5 s sau khi bắt đầu. Theo policy A đã khóa, hàng chờ A dừng.

**Cơ chế.** Trên Windows, worker chạy qua launcher venv (`D:/RCA-ext/envs/T-014-main/Scripts/python.exe`), launcher mở Python gốc làm worker. Monitor lấy PID worker từ `phases.jsonl` rồi kiểm ba điều kiện: launcher nằm trong danh sách cha; token có trong cmdline; worker tạo sau launcher. Trong psutil 6.1.1, `Process.parent()` gọi `Process(ppid)`; nếu launcher vừa thoát thì `NoSuchProcess` bị nuốt và `parent()` trả `None`, nên `parents()` rỗng → điều kiện 1 trượt → Blocked. Nhánh `except NoSuchProcess` sẵn có trong hàm không bắt được trường hợp này vì không có ngoại lệ nào được ném ra. Đây là tranh chấp thời điểm khi worker và launcher cùng kết thúc, không phải tiến trình lạ.

**Bằng chứng tái hiện** (gọi đúng hàm đã ghim, không sửa file; worker giả không đọc dữ liệu):

| Script | Worker giả | Lượt | BLOCKED |
|---|---|---|---|
| `chan_doan.py` | ngủ 0,05 s giữa 3 lần ghi pha | 60 | 0 |
| `chan_doan.py` | thoát ngay | 150 | 8 (`chan-doan-lan2-150.json`) |
| `chan_doan.py` (chạy lại) | thoát ngay | 150 | 15 (`chan-doan.json`) |
| `chan_doan_2.py`, `chan_doan_3.py` (bản sao rút gọn / bọc psutil) | thoát ngay | 200 mỗi script | 0 |

Ở mọi lượt BLOCKED, truy vấn lại ngay sau đó cho `NoSuchProcess` (worker đã thoát). Hai bản sao rút gọn không tái hiện → cửa sổ tranh chấp rất hẹp; chưa ghi được giá trị ba điều kiện ngay trong lần trượt (chưa kiểm trực tiếp điều kiện nào trượt; suy từ code psutil).

**Hệ quả với kết quả đã có.** Lỗi chỉ xảy ra ở bước giám sát, trước khi slot được nhận. Các slot đã VERIFIED (cả A lẫn non-A) đã qua kiểm danh tính bình thường; không có dấu hiệu kết quả sai. Slot càng ngắn càng dễ gặp lỗi.

## Nếu sau này cần chạy lại A

1. **Bản sửa đề xuất (chưa cài, chưa kiểm):** khi phép kiểm trượt, chỉ coi là tranh chấp nếu worker hoặc launcher (đúng PID và `create_time`) đã kết thúc → xử lý như nhánh `NoSuchProcess` sẵn có (giữ identity launcher). Cả hai còn sống mà vẫn trượt → vẫn Blocked. Fixture cần có: tái hiện lỗi (≥150 lượt worker thoát ngay, 0 BLOCKED sau sửa); PID không phải con của launcher vẫn bị chặn; token sai vẫn bị chặn.
2. **Không sửa tại chỗ** `dieu_phoi.py`: file này được ghim trong `chuan-bi-main-013-v2/manifest.json`, plan/protocol main013-v2, plan RE3 (`re3-ban-cuoi-001/meta/`) và plan chấm T-055.
3. **Đường phát:** supervisor không thử lại slot BLOCKED (`dieu_phoi.py:495`); `p7.py` buộc thư mục = `plan['directory']`; `nguon.py:381–415` buộc plan khớp placement đủ partition, code_pins = hợp đồng, protocol LOCKED_G3. Vì vậy cần bộ v3 riêng (protocol/hợp đồng/placement/plan/grant, như `build_v2.py`), code_pins = pin v2 + mã sửa + entry supervisor; entry phải cài bản sửa trong chính tiến trình `_supervise` (`p7.py:65` khởi chạy tiến trình mới) và ghi module thực nạp. Đây là hồ sơ khóa mới, cần Minh duyệt riêng.
4. **Chấm:** `cham.evaluate` đòi đủ A4; bảng A cần đường chấm riêng ghép 6 slot v2 (kiểm theo hợp đồng v2) với slot v3 (kiểm theo v3), không trộn plan.
5. **Dự toán (chưa đo):** dựng v3 + fixture 2–3 giờ; chạy 174 slot tuần tự trong nhóm `RE2-TT|torai_A` (`dieu_phoi.py:68, 687`) khoảng 1–3 giờ (slot đã đo 19–61 s); laptop cắm sạc, tắt ngủ; trình mục lỗi 10/50/99% (luật 21) trước khi phát.

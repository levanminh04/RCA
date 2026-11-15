# L8b — tiếp L8 sau khi T-064 sửa hash cấu hình (14/11/2026 16:58Z)

Điều phối T-064 đã xử lý điểm chặn trong `results/T-065/kiem/005-gc-cuoi/BAO-CAO.md` (kiểm lại, không tin brief):

- Nguyên nhân: điều phối ghi `cau_hinh_sha256` của V082 bằng hash byte file (sổ `results/T-064/so-bien-the.jsonl` dòng 180), lệch quy ước `src/m1_ft/chay.py::sha_cau_hinh` mà sổ và đầu ra dùng. Sổ có dòng `dinh_chinh` 16:57:20Z. Không đổi file cấu hình, không đổi đầu ra, không chạy lại M1.
- `results/T-064/ban-xuat/chi-muc-ban.json` dựng lại (SHA-256 file = `7e4278d6fbf1ae124da865780642304e459869d3d239787615fefed66fb12b0b`): `cau_hinh_sha256` theo `sha_cau_hinh`, thêm `cau_hinh_file_sha256` (hash byte file); bộ dựng `ban-xuat/dung_chi_muc.py` kiểm mọi đầu ra của V082 và V071 trùng `cau_hinh_sha256` và `ma_nguon_sha256` (56/56). Bản lỗi giữ ở `chi-muc-ban-2-loi-hash.json`.
- `results/T-064/cau-hinh-de-xuat.json` sửa tương tự (trường `quy_uoc_hash`); bản lỗi giữ ở `cau-hinh-de-xuat-loi-hash.json`.
- Ghi tại `tasks/T-064-m1-flashticket/LOG.md` (mục 16:56Z).

Việc: tiếp đúng nhiệm vụ trong brief L8 (`results/T-065/codex/L8-brief.md`) từ checkpoint của bạn — kiểm lại chỉ mục mới, rồi bộ xuất, dashboard mới, API và các phép kiểm đã nêu. Phạm vi ghi, checkpoint, báo xong như brief L8; giữ hồ sơ chặn L8 làm lịch sử.

# Đề xuất sửa tài liệu chung từ T-021

Chưa sửa file nào dưới đây. Mỗi mục chờ Minh duyệt riêng (Luật 0).

## E1. `docs/DECISIONS.md` — ghi các quyết định ngày 05/10 trong T-021 (K8)

- **Đoạn cũ:** không có.
- **Đoạn mới (đề xuất Q-61):** "05/10 | T-021: (1) tiêu chí 8 của MRP §4 (đủ dữ liệu bình thường) xét ở lớp gói, như tiêu chí 5, 6, 7, 9; giữ điều kiện 'bộ không có trace chỉ dùng có chủ đích' của tiêu chí 3. (2) Vị trí root ở G1 dùng bậc đã lưu trong results/, không đọc dữ liệu đo mới, ghi lệch so với Q-60(b). (3) Quy tắc nhóm: không có trong trace; bậc 0; nguồn; lá; hub (tổng bậc từ phân vị 75 của đồ thị); giữa; độ nhạy phân vị 90. (4) Bộ chỉ lưu bậc của root (Eadro, Nezha): gộp 'giữa hoặc hub', hub OPEN. Lời Minh: 'đồng ý sửa giúp tôi các lỗi trên'; '(a) Bậc đã lưu, ghi lệch'; 'Quy tắc bậc + độ nhạy'; 'đồng ý sửa SPEC theo đề xuất, S8 chọn (i)'. | SPEC/LOG T-021"
- **Lý do:** AGENTS mục 4: quyết định trong chat phải nằm trong DECISIONS.
- **Ảnh hưởng:** chỉ ghi nhận; không đổi kết quả.

## E2. `docs/WHY.md` — WHY-04 (sau khi Minh trả lời câu hỏi 1, 2, 4 của `goi-g1.md`)

- **Đoạn cũ:** WHY-04 chỉ nói chia theo ô và giữ ngoài.
- **Đoạn mới:** thêm (a) đơn vị chia cho bộ có nhiều lần tiêm trong một file (theo lựa chọn câu 1), kèm số cặp ca liền kề (`results/T-021/runs/chia-003/bao-cao-chia.json`); (b) tỷ lệ 1/3 dev và lý do; (c) phân tầng theo loại lỗi; (d) bộ giữ ngoài phải toàn TX0.
- **Ảnh hưởng:** cách chia của mọi bộ chia ở P3, P7.

## E3. Ghi chú cho sổ tiếp xúc của T-020

- `results/T-020/trung-gian/exposure_ledger/public-census.csv` ghi RE1-OB là 124 TX0 + 1 TX1. File gốc cho thấy T-006 đã chạy `main.py` trên 125 ca của bản Zenodo RE1-OB (`results/T-006/runs/kiem-chay-fse-baro-main-re1-ob.tar.gz`). Đề xuất: không sửa T-020 (đã đóng phạm vi), chỉ dẫn `results/T-021/tiep-xuc.csv` làm sổ tiếp xúc hiện hành cho G1.

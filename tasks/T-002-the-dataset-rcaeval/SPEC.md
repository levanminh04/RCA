# T-002 — Thẻ dataset cho họ RCAEval

- **Trạng thái:** đã duyệt (02/10/2026)
- **Người làm:** Codex
- **Người phản biện:** Claude
- **Thuộc gói MRP:** P2 — **Cổng:** G1

## Mục tiêu

Viết thẻ dataset cho RE2-TT, RE2-OB, RE3-TT, RE3-OB theo mẫu thẻ ở MRP P2. Phục vụ G1 (chọn dataset) và các tiêu chí phân xử ở MRP §4.

## Đầu vào

- `data/rcaeval/`: 30 ca dev RE2-TT và 5 ca mẫu (RE1-OB, RE2-OB, RE2-SS, RE3-SS, RE3-TT). Xem `data/README.md`.
- README và bài báo RCAEval.
- `docs/knowledge/K2-du-lieu.md`, `docs/knowledge/K3-dataset-ung-vien.md`.
- `docs/MRP.md` §4 (tiêu chí, chống thiên vị RCAEval Q-31, định nghĩa "nhìn" với dataset giữ ngoài) và P2.

## Đầu ra

- `results/T-002/mau-the-dataset.md`: mẫu thẻ dùng chung cho mọi dataset.
- `results/T-002/the-rcaeval.md`: thẻ cho RE2-TT, RE2-OB, RE3-TT, RE3-OB.
- Script đọc schema, đặt trong `results/T-002/`.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-002/`
- `.venv/` (git đã bỏ qua)
- `requirements.txt` ở gốc repo

## Các bước

1. Dựng `.venv` bằng `py -3 -m venv .venv`, cài pandas và pyarrow; ghi phiên bản vào `requirements.txt` — kiểm bằng: import được, đọc được một file parquet.
2. Đọc schema thật của các ca mẫu: các trường trace, tỷ lệ span cha resolve được, log có trace_id không — kiểm bằng: in schema và số đếm, lưu vào `results/T-002/`.
3. Đếm số service gốc, loại lỗi và vị trí của service gốc trong đồ thị (tiêu chí 5, 6). Nguồn đếm: tên thư mục ca trên Hugging Face, xem qua danh sách file, không tải dữ liệu — kiểm bằng: bảng đếm kèm nguồn.
4. Ước lượng thô tiêu chí 7 (triệu chứng lan) trên dữ liệu đã có, thử vài ngưỡng lấy từ dữ liệu bình thường, theo MRP P2. Không gắn nhãn "lan" cho từng ca — kiểm bằng: báo kết quả theo từng ngưỡng.
5. Điền thẻ; ô nào chưa kiểm được ghi "chưa kiểm" và lý do.

## Tiêu chí xong

- Mỗi thẻ điền đủ các mục của mẫu; ô chưa kiểm có lý do.
- Mọi con số có đường dẫn tới file kết quả hoặc nguồn.
- Mỗi nhận định dựa trên kết quả có nêu nguyên nhân khả thi khác (Q-33).

## Không làm

- Không mở `data/locked/` (AGENTS luật cứng 1).
- Không chọn dataset (việc của G1).
- Không so RCAEval hơn hay kém dataset khác (Q-31). Thẻ RCAEval làm trước chỉ vì dữ liệu đã có; mọi ứng viên sẽ so trên cùng một bảng khi đủ thẻ.
- Không chạy phương pháp RCA nào.

## Chi phí ước lượng

Cài gói Python dưới 1 GB. Không tải dữ liệu lớn. Không cần báo trước theo luật cứng 8.

## Rủi ro và điều chưa chắc

- Chỉ có 1 ca mẫu cho RE2-OB và RE3-TT, 0 ca cho RE3-OB: schema của các bộ này chỉ kiểm được trên mẫu đó, hoặc ghi "chưa kiểm".
- Ước lượng tiêu chí 7 phụ thuộc ngưỡng; chỉ dùng để biết dataset có ca lan hay không, không làm căn cứ kết luận.

# Đính chính khi chạy trên dữ liệu thật — T-045

Ghi theo SPEC T-045 bước 1 ("Lỗi thì ghi đính chính, dừng phần phụ thuộc") và lời Minh trong prompt mở phiên 31/10/2026 ("Lỗi code thì ghi đính chính trong results/T-045/ và dừng phần phụ thuộc. KHÔNG sửa src khi Minh chưa duyệt"). Code: `src/m1` ở commit nghiệm thu T-044 `69ef90b6`. **Chưa sửa `src/`. Mọi mục chờ Minh duyệt.**

Phép chẩn đoán dùng một bản sao `src/` trong thư mục scratchpad của phiên (ngoài repo) có vá ĐC1, ĐC2, chỉ để biết lỗi có dừng ở đó không và để đo thời gian. Bản ghi của bản vá đó không là kết quả T-045 và không được dùng.

## ĐC1. Adapter RE2-TT dừng ở mọi ca vì `parentSpanID` rỗng là `pd.NA` — CHẶN mọi phần RE2-TT

- **Quan sát.** Lượt `runs/b1-r0-thu-001` (bước 1, ca RE2-TT đầu `dev-03d4910932`) dừng trong `adapter.ca_re2tt` với `TypeError: boolean value of NA is ambiguous` (`runs/b1-r0-thu-001.stdout.txt`). Runner không ghi được bản ghi ERROR, vì lỗi xảy ra trước `chuoi.chay`.
- **Nguyên nhân (đã xác định).** `traces.parquet` của RE2-TT mang metadata pandas với `numpy_type = "string"`, nên `pq.read_table(...).to_pandas()` (pyarrow 18.1.0, pandas 2.2.3) trả cột `parentSpanID` kiểu `string` của pandas; giá trị rỗng là `pd.NA`. `adapter._rong(x)` (`src/m1/adapter.py:73–74`) xét `x is None`, NaN số thực, rồi `x == ''`; với `pd.NA`, `x == ''` trả `pd.NA` và `or` gọi `bool(pd.NA)` nên ném lỗi.
- **Phạm vi.** Đếm trên 30/30 ca RE2-TT dev: cột `parentSpanID` có `pd.NA` ở cả 30 ca (ca đầu: 6.515 dòng trên toàn file); các cột span khác không có NA. Nezha-OB không bị (lượt `runs/b1-r0-thu-002-nezha` chạy OK).
- **Vì sao test T-044 không bắt.** `test_adapter.py` sinh parquet tổng hợp với cột kiểu object, giá trị rỗng là `None`.
- **Đối chiếu code khác trong repo.** KS-16 đọc cùng cột bằng `tr['parentSpanID'].fillna('')` (`results/T-043/ks16/ks16_pha1_v11.py:405`).
- **Sửa đề xuất (tối thiểu).** `src/m1/adapter.py`, hàm `_rong`: thêm `x is pd.NA` (trả True) trước phép so `x == ''`. Ý nghĩa giữ nguyên: parent rỗng là span gốc (PII-20).
- **Phép kiểm đề xuất.** Thêm vào `results/T-044/tests/test_adapter.py` (hoặc test mới trong `results/T-045/`) một ca parquet có metadata pandas `string` và `parentSpanID` null: span đó thành span gốc, `parentSpanID = ''`. Chạy lại toàn bộ test T-044 (SPEC T-045 "Phạm vi ghi"). Đối chiếu D1 (span gốc, span mồ côi) với KS-16 trên 30 ca.
- **Phần dừng.** Mọi lượt RE2-TT: T1 RE2-TT, 30 mốc giả, D1 RE2-TT, D3 RE2-TT, D5 RE2-TT, D17.

## ĐC2. Adapter RE2-TT đổi `message` rỗng thành chuỗi `'<NA>'` — KHÔNG CHẶN R0; ảnh hưởng E3

- **Quan sát.** `logs.parquet` của RE2-TT có cột `message` kiểu `string` của pandas. 15/29 ca có log mang `message` rỗng (ví dụ `dev-12a1a88069`: 42/272.821 dòng trên toàn file). `adapter.ca_re2tt` dùng `lg['message'].astype(str)` (`src/m1/adapter.py:108`); pandas đổi `pd.NA` thành chuỗi `'<NA>'`.
- **Hệ quả.** Số dòng không đổi. Với quy tắc từ khóa của SimpleRCA, `'<NA>'` và `''` đều là dòng không lỗi, nên kênh log lỗi cơ bản (R0, E3 tắt) không đổi. Khi E3 bật, `'<NA>'` thành một token và có thể thành một mẫu Drain riêng; với `''` thì là chuỗi rỗng. Chưa đo số mẫu bị ảnh hưởng (chặn bởi ĐC1).
- **Đối chiếu.** Adapter SimpleRCA của repo dùng `al['message'].fillna('').astype(str)` (`src/simplerca/adapter.py:84`); từ khóa RE2-TT của M1 lấy từ SimpleRCA (CĐ5).
- **Sửa đề xuất.** `src/m1/adapter.py:108`: `lg['message'].fillna('').astype(str)`.
- **Phép kiểm đề xuất.** Ca parquet có `message` null: dòng vẫn được giữ, `message = ''`.

## ĐC3. Chuỗi tính đường găng E1-CP cho mọi span ở mọi cấu hình — không sai kết quả; làm thời gian RE2-TT tăng khoảng 5 lần

- **Quan sát.** Trên bản sao có vá ĐC1, ĐC2 (ngoài repo), R0 trên `dev-03d4910932` mất 132,6 giây; cấu hình K đầy đủ mất 120,4 giây. Nezha-OB: R0 2,8 giây một ca. Profile một lần chạy R0 RE2-TT (cProfile, 142,6 giây): `span.chuan_bi` 121,5 giây, trong đó `span.duong_gang` 109,6 giây tự thân (322.096 lần gọi, một lần cho mỗi span).
- **Nguyên nhân.** `span.chuan_bi` luôn tính `s['u_CP'] = doc_quyen_CP(...)` (`src/m1/span.py:138`). `u_CP` chỉ được đọc khi `E1 == 'CP'` (`span.py:156`); ma trận dev không chạy E1-CP (`ma-tran-thu.json#/ket_cuc_khai_truoc_T0/khong_du_ca/E1-CP`). `duong_gang` dựng danh sách `khac` cho mỗi ứng viên ở mỗi bước, nên tốn bậc ba theo số con của cha.
- **Sửa đề xuất.** `span.chuan_bi(rows, t, tau, mien=None, tinh_CP=True)`: khi `tinh_CP` là False thì `u_CP = None`; `chuoi._chay` gọi với `tinh_CP=(E1 == 'CP')`. Mặc định True giữ nguyên hành vi cho test gọi thẳng `chuan_bi`.
- **Vì sao không đổi kết quả.** Với E1 ∈ {tắt, U}, không chỗ nào đọc `u_CP` (tìm `u_CP` trong `src/`: chỉ `span.py:138` và `span.py:156`). Phép kiểm: 374 test T-044; `results/T-044/scripts/tat_dinh.py` so 104 bản ghi trước/sau sửa (phải giống hệt từng byte); trên dữ liệu thật, so bản ghi R0 của vài ca trước/sau.
- **Nếu không sửa.** RE2-TT khoảng 130 giây mỗi (cấu hình, ca). Khối K pha 1 (16 cấu hình × 30 ca + 30 mốc giả) khoảng 35 giờ máy; T1 RE2-TT (3 seed + xáo + mốc giả) khoảng 5,4 giờ.
- **D4 không phụ thuộc sửa này:** D4 gọi `span.chuan_bi` hoặc `doc_quyen_CP` trực tiếp trên Nezha-OB.

## Trạng thái (ghi thêm ở phiên 2, 01/11/2026; phần trên giữ nguyên làm lịch sử)

- Đoạn đầu tệp ("Chưa sửa `src/`. Mọi mục chờ Minh duyệt") đúng ở thời điểm ghi, nay đã cũ.
- ĐC1, ĐC2, ĐC3 đã được Minh duyệt trong chat ngày 31/10/2026, nguyên lời: "duyệt đc 1 2 3" (LOG T-045 mục "Tiếp chặng 1 — sửa ĐC1–ĐC3"). Dòng DECISIONS Q-216 đang chờ ghi.
- Đã sửa, mỗi sửa một commit: ĐC1 `ec10087a`, ĐC2 `eb14262a`, ĐC3 `bbef69dd`. Test riêng ở `results/T-045/tests/`; 374/374 test T-044 qua sau mỗi sửa; `results/T-044/scripts/tat_dinh.py` sau ĐC3 cho bản ghi giống hệt `results/T-044/runs/tat-dinh-012` (`runs/sua-dc-001/`).
- Mục "Sửa đề xuất" và "Phép kiểm đề xuất" ở trên giữ làm lịch sử.

## D1. Các lệch khi đối chiếu số trung gian với KS-16 — không phải lỗi cài đặt (ghi ở phiên 2 tiếp, 01/11/2026)

SPEC T-045 bước 2 (D1) ghi "Lệch thì ghi đính chính". Phiên 1 chỉ giải thích các lệch ở LOG và `doi-chieu-ks16*.json`. Mục này ghi chúng qua đính chính (điểm tự tìm N4; REVIEW-2 U5). Không đổi số, không sửa `src/`.

- **Nezha-OB, trường quan sát (T^chắc, T^max, trạng thái ô của trace và log).** Lệch so với `results/T-043/ks16/dem-khong-nhan.json` (KS-16 v1, không tách khe giữa file phút). M1 cài luật F phương án (a) của Q-207 (khe là OPEN). Đối chiếu thêm `results/T-043/ks16/runs/pha1-002/dem-khong-nhan.json` (v1.1): khớp ở 22/22 ca, sai khác ≤ 2 µs do adapter đưa span về µs nguyên (`doi-chieu-ks16-nezha.json#/tong_hop/so_ca_dat_luat_F_a_Q207`, `#/tong_hop/so_ca_lech_v11_ngoai_2us`). Phân loại: khác định nghĩa giữa hai bản KS-16; M1 đúng Q-207.
- **RE2-TT, đầu H của trace phía N ở 7 ca (lệch 3–12 ms).** KS-16 lấy span có `end` trong cửa sổ; M1 lấy span thuộc miền (start ≥ t − 300). Chênh T dưới 0,004% (`doi-chieu-ks16-re2.json#/tong_hop`; LOG phiên 1 mục 22:50). Phân loại: khác định nghĩa bản ghi trong cửa sổ.
- **RE2-TT, ca `dev-3defe3d34b` không có tệp log.** M1 ghi 0 dòng, KS-16 để trống. Phân loại: dữ liệu thiếu, cả hai cách xử lý nhất quán.
- Mọi số đếm còn lại của D1 (span, bỏ lặp, mồ côi, gốc, bọc, vượt biên, thao tác E1 tắt và bật, cạnh E2, metric, log) khớp KS-16 ở 52/52 ca.

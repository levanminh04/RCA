# T-046 — Cổng kiểm định, `verdict` và thang điểm của M1 (báo cáo tới điểm dừng D-2)

- **Người làm:** Claude (phiên mới, độc lập với phiên soạn SPEC). **Người phản biện:** Codex. **Ngày:** 01/11/2026.
- **SPEC:** `tasks/T-046-cong-verdict-thang-diem/SPEC.md`. Gồm bản 2 (Minh duyệt), các sửa S1–S10 khi người làm rà SPEC (mục "Đặc tả bổ sung khi rà", A1–A7), bản 3 (B1–B6) và bản 4 (C1–C3). Bản 3 và bản 4 viết theo lời Minh giao quyền quyết ở hai điểm dừng (LOG phiên 1 (tiếp), (tiếp 2)).
- **Trạng thái:** đã xong bước 0–8; đang dừng ở D-2, chờ Minh duyệt WHY. Chưa cài vào `src`, chưa chạy bước 9–10, chưa commit.
- **Ràng buộc đã giữ:**
  - Không đọc root, loại lỗi, ô; không tính MRR. Chỉ dùng mốc tiêm (chế độ (a)) để biết cửa sổ nào có lỗi.
  - Mọi lần nhìn số dev ghi ở `so-lan-nhin.jsonl`.
  - Cặp cổng được khóa lúc 15:49, kèm hash ở LOG, trước khi xem C-e.
- **Mọi số trong báo cáo là số dev.** Dev dùng để chọn và kiểm lại; không có phần kiểm độc lập. C-e chồng lấn dữ liệu với A/A.

## 1. Tóm tắt

**Quan sát (có số, có con trỏ):**
1. **Cổng hiện hành G0 qua giả nhiều ở cửa sổ không lỗi.** Đo trên A/A (nửa đầu N so với nửa sau, theo A1):
   - RE2-TT: metric 0,300; thao tác 0,070; op_excl 0,115.
   - Nezha-OB: 0,08–0,10.
   - Nguồn: `chan-doan-cong.json#/qua_cong_aa/<ô>/G0/ty_le`.
2. **Không ứng viên cổng nào đạt mức (a) ≤ 2α = 0,02 ở mọi ô.**
   - Ô khó nhất là metric RE2-TT: G1 0,126; G3 0,072; G4 0,272; GE không tìm được ngưỡng.
   - Đơn vị đếm (log): nhị thức hiện hành D0 qua giả 0,066, D1 0,039 (mẫu log thường RE2-TT).
   - Nguồn: `chan-doan-cong-ban3.json#/qua_cong_aa`, `#/don_vi_dem`, `#/nguong`.
3. **Cơ chế ở metric RE2-TT** (dữ liệu N trước mốc tiêm, không nhãn; `cau-truc-metric-re2.json`):
   - 82% số giây có giá trị y hệt giây trước. Theo kênh: cpu 74%, mem 96%, socket 97%.
   - Trôi khi hệ khỏe: mem chênh 1,48 độ lệch chuẩn giữa hai nửa N. Latency gần bước ngẫu nhiên ở thang 60 giây (VR60 khoảng 0,75).
   - Bỏ các giây lặp giá trị, G0 giảm từ 0,30 xuống 0,18; cpu vẫn 0,10–0,21; mem hướng lên 0,57 (`bo-giu-metric-re2.json`).
4. **Chọn theo minimax (bản 4): G3 cho đơn vị phân vị, D1 cho đơn vị đếm.**
   - Minimax ở đây nghĩa là chọn cổng có tỷ lệ qua giả ở ô tệ nhất thấp nhất (`danh-gia-ban4-luot2.json#/minimax`).
   - Không quy tắc `verdict` nào đạt cả (b) lẫn (c1):

     | Quy tắc | (b): CAUSE_FOUND ở A/A RE2-TT | (c1): CAUSE_FOUND ở cửa sổ thật |
     |---|---|---|
     | V0, V3, V1 | 30/30 | — |
     | V4 (q* = 0,085) | 6/30 | RE2-TT 0,73; Nezha-OB 0,18 |

     Nguồn: `#/to_hop`.
   - Khóa riêng cặp cổng (G3, D1) lúc 15:49 (`ung-vien.json`, sha256 ở LOG). Để `verdict` là chưa chọn được.
5. **Sau khóa, trên C-e (300 + 300 giây, đúng cỡ thật; chỉ báo cáo):**
   - Tỷ lệ qua giả của G3: metric 0,026–0,027; op_full 0,029 (`kiem-sau-khoa.json#/a_phay`).
   - Với K-đủ: op_excl lên 0,023, xuống **0,171**; cạnh 0,006; mẫu log thường (D1) 0,027 (`#/K_du/ce|RE2-TT|qua_cong_theo_o`).
   - Số đơn vị có cờ ở cửa sổ thật lớn hơn C-e ở 29/30 cặp cùng ca. Trung vị 59,5 so với 19; theo tỷ lệ 0,124 so với 0,040 (`#/c2`).
   - CAUSE_FOUND ở C-e: V0 30/30, V4:0,085 0/30 (`#/b_phay|*`).
6. **Thang điểm:** tỷ lệ kênh phân vị có cờ đạt rA = 1 là RE2-TT 0,034, Nezha-OB 0,269 (metric 5 điểm 43/125). Vì vậy (S) mở. Theo luật khai trước, T4c làm số cửa sổ có khối đầu nhiều thực thể ở Nezha-OB giảm từ 1 xuống 0, RE2-TT giữ 0 (`thang-diem.json#/hoa_khoa_tang1`).

**Suy luận (chưa phân xử hết):**
- **C1 — vì sao cổng qua giả:**
  - Ở metric RE2-TT, tự tương quan dừng kiểu AR(1) **không** phải nguyên nhân chính. Làm trắng AR(1) hiệu chuẩn được AR(1) tổng hợp tới φ = 0,9, nhưng trên dev vẫn để 27% qua giả.
  - Ba thành phần có bằng chứng: chuỗi giữ giá trị; động học bền của chuỗi gốc; trôi khi hệ khỏe (mem, latency).
  - Giải thích khác chưa loại: giữ giá trị có thể do cách RCAEval đưa metric về lưới 1 giây. Chưa đối chiếu nguồn gốc dữ liệu.
- **A/A 150 giây đánh giá G3 kém hơn ở cỡ thật** (A/A 0,072 so với C-e 0,027 ở metric). Cửa sổ ngắn buộc khối ngắn hoặc rơi về G0, đúng rủi ro R7 đã khai khi rà SPEC.
- **Thao tác trace:** khối thời gian (G1, G3) gom được phụ thuộc giữa các span gần nhau. op_excl RE2-TT lệch mạnh về hướng xuống (A/A 0,092, C-e 0,171): self-time giảm theo thời gian khi hệ khỏe, nguyên nhân chưa biết.
- **`verdict`:** ở cùng cỡ cửa sổ, tỷ lệ đơn vị có cờ tách được cửa sổ có lỗi khỏi C-e ở 29/30 cặp. Nhưng không có dữ liệu cùng cỡ để chọn ngưỡng mà không dùng C-e. A/A 150 giây không cùng cỡ, nên mọi quy tắc chọn trên A/A đều lệch.

**Chưa phân xử / OPEN:**
- Nguyên nhân hướng xuống của op_excl RE2-TT.
- Phần qua giả còn lại của đơn vị đếm ở thang dài hơn 10 giây.
- Hiệu chuẩn metric Nezha-OB (5 điểm).
- `verdict` cho bản P7.
- Hiệu chuẩn cổng từng đơn vị bằng lịch sử bình thường dài (FlashTicket).

## 2. Đầu vào, kiểm hash, môi trường

- Hash T-045 PASS 6.085/6.085 (gồm `src/m1` ở `bbef69dd`); dữ liệu dev PASS (RE2-TT 30 ca, Nezha-OB 22 ca) (`runs/b0-kiem-001`).
- Test T-044 374/374, T-045 16/16 (`runs/b0-test-001`). Test T-046 30/30 (`tests/`).
- Môi trường: `source results/T-045/scripts/moi_truong.sh` (Python 3.12.10, numpy 1.26.4, scipy 1.14.1).
- Không sửa `src`. Ứng viên cài trong `scripts/cong.py`, `scripts/t046.py`.
- Chuỗi M1 chạy có móc ghi mẫu, mốc thời gian và thay cache cổng. Bản ghi có móc trùng từng byte bản ghi T-045:
  - cửa sổ thật: 52/52 ca;
  - C-e: 30/30 ca.
- Chạy lại chuỗi với cổng khóa (p phát lại; cờ đếm thay qua móc) khớp tập cờ và verdict khi tính lại bên ngoài (kiểm trên một ca, ba bộ cổng).

## 3. Rà SPEC (trước bước 0)

Mười hai điểm R1–R12, sửa S1–S10 (LOG mục "Rà và sửa SPEC"). Các điểm chính:
- A/A Nezha-OB chia ở t − 150 không có phép hợp lệ nào. Hệ quả: (b) gộp 52 cửa sổ đạt được khi đầu ra mất tác dụng.
- G3 × V1 suy biến, vì p nhỏ nhất 1/2.001 lớn hơn ngưỡng Holm.
- Thứ tự tổ hợp cổng × `verdict` chưa định.
- G1, G3 chưa đặc tả đủ.
- (a) chỉ đo trên đơn vị của R0.
- (S) chưa rõ gộp hay tách dataset.

Đã sửa theo hướng chặt hơn, không nới tiêu chí nào.

## 4. Bước 2 — dữ liệu tổng hợp

- `runs/b2-tong-hop-001` (A7 đạt):
  - Tái lập SPEC T-043: G0 ra 0,011; 0,073; 0,288; 0,386.
  - Ở φ = 0, G1 và G3 hiệu chuẩn.
  - Ở φ = 0,9: G1 0,05–0,07, G3 0,04–0,06. Ở φ = 0,98: 0,09–0,18. Luật chọn b theo ρ < 0,2 cho khối quá ngắn.
- `runs/b2b-tong-hop-001` (B4 đạt):
  - G4 ở φ = 0,9 (cỡ 300) còn 0,015–0,026.
  - G4 không xử lý được xu hướng: 0,63.
  - D1: Poisson 0,002–0,008; Poisson gộp cụm từ 0,13–0,15 (D0) xuống 0,003–0,024.
- Độ nhạy với bước nhảy 0,5σ (cỡ 300): G0 0,98; G1 0,93; G4 0,87; G3 0,61.

## 5. Bước 3–5 — A/A, luật chọn

Tỷ lệ qua cổng ở A/A, mức (a) = 0,02:

| Ô | G0 | G1 | G3 | G4 |
|---|---|---|---|---|
| RE2-TT metric | 0,300 | 0,126 | 0,072 | 0,272 |
| RE2-TT op_full | 0,070 | 0,026 | 0,020 | 0,020 |
| RE2-TT op_excl | 0,115 | 0,053 | 0,053 | 0,053 |
| RE2-TT canh | 0,020 | 0,013 | 0,005 | 0,005 |
| Nezha-OB op_full | 0,078 | 0,012 | 0,007 | 0,007 |
| Nezha-OB op_excl | 0,096 | 0,016 | 0,013 | 0,013 |
| Nezha-OB canh | 0,079 | 0 | 0 | 0 |

Nguồn: `chan-doan-cong-ban3.json#/qua_cong_aa`.

- Đơn vị đếm (`#/don_vi_dem`):
  - mẫu log thường: D0 0,066 → D1 0,039 (RE2-TT); D0 0,052 → D1 0,022 (Nezha-OB);
  - log_loi và mau_loi RE2-TT chỉ có 30 phép mỗi ô, không đo được, ghi OPEN.
- Lịch sử luật chọn:
  - Bản 2: D-1 kích hoạt (đơn vị đếm vượt mức; không cổng nào đạt).
  - Bản 3: thêm G4, GE, D1, DE; vẫn không bộ nào đạt.
  - Bản 4: chọn theo minimax; `verdict` không đạt.
  - Chi tiết: LOG.

## 6. Khóa và kiểm sau khóa

- Khóa (G3, D1) lúc 15:49, `ung-vien.json` sha256 `2023c643…`; `verdict` null.
- C-e: `runs/b6-sau-khoa-001/ce`.
- K-đủ: `runs/b6-sau-khoa-001/kdu`, gồm A/A, thật và C-e.
- R0 thật: `runs/b6-sau-khoa-001/r0`.
- Số ở mục 1, ý 5–6.
- C-e không dùng để chọn lại. Nó là phép kiểm lại có chồng lấn dữ liệu với A/A.

## 7. Đề xuất ở D-2

Đề xuất WHY-67 (cổng), WHY-68 (`verdict`), WHY-69 (thang điểm) và kế hoạch cài đặt nằm ở LOG, mục "D-2". Tóm tắt:
- (G3, D1) làm chế độ mới. Chế độ cũ (G0, D0, V0, E4) giữ làm mặc định trong mã.
- `verdict` không khóa cho bản P7. T-047 tính vế mốc giả bằng V4:0,085 kèm V0; việc này lệch (c1), Minh quyết.
- Thang điểm S1 theo luật khai trước; tác dụng đo được rất nhỏ; đây là đổi D24, Minh quyết.

## 8. Tiêu chí xong (SPEC)

| # | Tiêu chí | Trạng thái |
|---|---|---|
| 1 | Test T-044, T-045 qua ở đầu phiên và sau mỗi commit `src` | Đầu phiên đạt; chưa có commit `src` |
| 2 | C1 theo loại đơn vị và nguồn; metric Nezha-OB OPEN | Đạt. Metric RE2-TT phân xử phần lớn; trace và đếm thu hẹp; metric Nezha-OB OPEN |
| 3 | Khóa trước C-e có hash; kiểm sau khóa đã báo; hoặc xung đột trình Minh | Đạt một phần: khóa cổng có hash; `verdict` không chọn được, đã trình qua hai lượt quyết |
| 4 | Thang điểm quyết theo (S) | (S) mở; đề xuất S1; đổi D24 chờ Minh |
| 5 | WHY duyệt trước khi cài; chế độ cũ không đổi hành vi | Chờ D-2 |
| 6 | Bước 10 tái lập số | Chưa làm (sau D-2) |
| 7 | Không đọc root, không tính MRR, mọi lần nhìn số đã ghi | Đạt; hai dòng đầu của sổ nhìn số chỉ có giờ trong khoảng |

## 9. Lượt chạy (giữ cả lượt thử và lượt dừng)

- `b0-kiem-001`, `b0-test-001`
- `b1-thu-C-001`, `b1-kiem-001`
- `b2-tong-hop-001`, `b2b-tong-hop-001`
- `b3-thu-001`, `b3-aa-001`, `b3b-thu-001`, `b3b-aa-001`
- `b5r-tinh-001`
- `b6-sau-khoa-001`: có một lượt r0 dừng lúc 16:04 trước khi có ca nào; dòng tham số còn trong `tham-so.json`.

Chẩn đoán không nằm trong `runs/`: `chan-doan-cong*.json`, `cau-truc-metric-re2.json`, `bo-giu-metric-re2.json`.

## 10. Lệnh dựng lại

```
source results/T-045/scripts/moi_truong.sh
cd results/T-046/tests && $PY -B -m pytest -q -p no:cacheprovider
cd results/T-046/scripts
$PY -B b1_kiem_du_lieu.py --ra ../runs/<lượt>
$PY -B b2_tong_hop.py --ra ../runs/<lượt>;  $PY -B b2b_tong_hop.py --ra ../runs/<lượt>
PYTHONHASHSEED=0 $PY -B b3_chay.py --luot ../runs/<lượt> --so 4 [--cong G0,G4]
$PY -B b3_tong_hop.py --luot ../runs/b3-aa-001 --ra ../chan-doan-cong.json
$PY -B b3b_tong_hop.py --cu ../runs/b3-aa-001 --moi ../runs/b3b-aa-001 --ra ../chan-doan-cong-ban3.json
$PY -B b3_bo_sung.py …; $PY -B b3c_cau_truc_metric.py …; $PY -B b3d_bo_giu.py …
$PY -B b5c_danh_gia.py --cu ../runs/b3-aa-001 --moi ../runs/b3b-aa-001 --chan-doan ../chan-doan-cong-ban3.json --ra-danh-gia <tệp> --ra-khoa <tệp> [--g3-tinh ../runs/b5r-tinh-001/ca]
PYTHONHASHSEED=0 $PY -B b5r_tinh_G3.py --cu ../runs/b3-aa-001 --moi ../runs/b3b-aa-001 --luot ../runs/<lượt>
$PY -B b5d_khoa_cong.py --danh-gia ../danh-gia-ban4-luot2.json --chan-doan ../chan-doan-cong-ban3.json --ra <tệp>
PYTHONHASHSEED=0 $PY -B b6_sau_khoa.py --ung-vien ../ung-vien.json --sha256 <hash LOG> --phan ce|r0|kdu --luot ../runs/<lượt>
$PY -B b6_tong_hop.py --ung-vien ../ung-vien.json --cu ../runs/b3-aa-001 --moi ../runs/b3b-aa-001 --luot ../runs/b6-sau-khoa-001 --ra-kiem ../kiem-sau-khoa.json --ra-thang ../thang-diem.json
$PY -B tao_manifest.py [--kiem]
```

Lệnh đầy đủ của từng lượt nằm trong `tham-so.json` của lượt, docstring từng script và LOG.

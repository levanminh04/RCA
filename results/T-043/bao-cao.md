# Báo cáo T-043 — M1: thiết kế chuỗi chẩn đoán RCA và giao thức thử trên dev

- **Trạng thái:** đã nghiệm thu trong phạm vi thiết kế (Q-209, 29/10/2026), sau ba lượt Codex kiểm kết quả và các lượt sửa phiên 9–10 (`dinh-chinh-phien9.md`, `dinh-chinh-phien10.md`). Không xác nhận hiệu quả hay cơ chế của thành phần nào; không đóng G3.
- **Quyền:** Q-206 (duyệt thực hiện có điều kiện, 28/10/2026). Phiên 7 làm bước 0–5 và một phần bước 6; phiên 8 kiểm nhận xét F_s của Codex, đính chính, hoàn tất bước 6–7.
- **Người làm:** Claude. **Người phản biện:** Codex.
- **Cách đọc:**
  - Mọi số có đường dẫn tới file kết quả trong `results/T-043/`; con trỏ JSON ghi sau dấu `#`.
  - "Chưa kiểm" là giả thuyết, không là căn cứ.
  - "GIÚP", "HẠI" là tên kết cục của luật C, không là khẳng định thành phần có ích.

## 0. Tóm tắt

**Task đạt gì.**
- Đủ đầu ra theo SPEC: đặc tả v1, hợp đồng, thẻ đọc sáu bài, 82 fixture có đáp án, KS-16 trên 52/52 ca, ma trận thử đóng băng trước mọi code thành phần, WHY đề xuất, bảng chuyển giao, báo cáo này, manifest.
- Đủ căn cứ để mở ba task cài đặt (D1). Chưa đủ để chọn thành phần, khóa G3 hay khẳng định lợi ích của đồ thị (MRP §3).

**Câu hỏi nghiên cứu trả lời tới đâu.**
- Chưa trả lời RQ3b, RQ3c, RQ3d hay câu hỏi lợi ích nào. T-043 là task thiết kế.
- T-043 trả lời được các câu về **khả năng phân xử của dev**, những câu mà SPEC giao cho KS-16:
  - **E1-CP không đạt điều kiện chạy K-b theo Q2 (ngưỡng 5%):** cha có con chồng lấn trên 1 ms là 0/494.815 ở RE2-TT và 444/277.534 (0,16%) ở Nezha-OB; khác biệt E1-CP so với E1-U trên các trace Nezha-OB này chưa được kiểm; chồng lấn chưa chứng minh là song song thật (`dinh-chinh-phien10.md` Đ21);
  - **E3 chỉ có 4 ô kích hoạt** (lỗi return và exception ở Nezha-OB), nên là thành phần ít ca;
  - **trace và log Nezha-OB chỉ phủ 41–97 giây ở N và 84–140 giây ở A**, do điều kiện xuất dữ liệu của dataset;
  - **nối log–span khả thi ở Nezha-OB** (99,90% dòng khớp đúng một span), **không khả thi ở RE2-TT** (không có ID).
  - Các thành phần khác có từ 8 tới 21 ô kích hoạt.

**Nhận xét F_s của Codex** (mục 5): đúng một phần.
- Người làm tìm thêm một lỗi ở code v1: khe giữa hai file phút bị gộp vào khoảng ghi F.
- v1 và v1.1 chênh T ở 12/22 ca Nezha-OB, tối đa 1,01%; 4/1.420 quyết định cổng của đơn vị đếm đại diện Nezha-OB đổi. RE2-TT không đổi. Số ô kích hoạt không đổi.
- Minh chọn luật F phương án (a) (Q-207): khe giữa file là OPEN; v1 và v1.1 là hai đầu của phép quét độ nhạy (`dinh-chinh-phien9.md` Đ9). Bản chốt v1 giữ nguyên.

**Chưa phân xử.**
- Hiệu quả của mọi thành phần; A0; giả định mẫu độc lập ở cổng E4; bảng lớp lan (đặc biệt "tần suất tăng"); nghĩa vật lý của cạnh (O03).

**Đã quyết** (mục 11; Q-209): mọi mục từng chờ Minh của T-043. Không còn mục chờ quyết trong phạm vi thiết kế.

## 1. Đầu ra và tiêu chí xong

| Tiêu chí (SPEC) | Trạng thái | Bằng chứng |
|---|---|---|
| 1. Mọi thành phần và đối chứng ở phần C đủ 10 trường; mỗi kết cục có ngưỡng số | Đạt, với hai ngoại lệ đã ghi | `dac-ta-phuong-phap-v1.md` §0 (danh sách 10 trường do người làm dựng, vì SPEC không liệt kê), §7–8. Ngưỡng: luật C (δ = 0,01; δ_d = 1/n_d; 6 ô; mốc giả 0,10; M + M′ ≥ 3), Q2 (5%), luật khối (0,01). Ngoại lệ: E8 chỉ FlashTicket, mười trường giao `bang-chuyen-giao.json#/dong/9` (dòng có `ma` = E8) và SPEC P10; "dung sai đồng hồ" không có bước riêng ở B4 (mục 11) |
| 2. KS-16 xong 52/52 ca; hash khớp; số ô kích hoạt từng ứng viên; trạng thái quan sát từng nguồn, từng cửa sổ | Đạt | `ks16/dem-khong-nhan.json#/so_ca_xong` = 52, `#/ca_loi` = []; `ks16/dem-sau-ghep-nhan.json#/o_kich_hoat`; trạng thái ô theo nguồn ở `#/cases/*/quan_sat`. Luật F v1.1: lượt `ks16/runs/pha1-002`, `pha2-002` (mục 5) |
| 3. Ma trận đóng băng trước mọi code thành phần; số cấu hình hữu hạn; vai trò từng phép so | Đạt; hai câu chữ sai (Đ3, Đ7) | `ma-tran-thu.json` sha256 ghi ở LOG phiên 7 trước bước 6; chưa có code thành phần nào. Số ô T0 khai trong `#/ket_cuc_khai_truoc_T0` khớp cả `pha2-001` và `pha2-002` |
| 4. Fixture đủ 82 ca kèm đáp án | Đạt | `fixture-dac-ta.json` (82 mục; mục 1 gồm 7 ca S1–S7); `fixture/ket-qua-kiem.json#/A_khop` = 109, `#/B_khop` = 109, `#/so_phep_kiem` = 109 |
| 5. Bảng bao phủ DT18/cô/MRP, phần chưa bao phủ, nơi nhận, quyết định phụ thuộc | Đạt | Mục 6 |
| 6. Không có câu "đã chọn" hay "giúp"; mọi dự đoán ghi "chưa kiểm" | Đạt | Rà bằng grep "đã chọn", "giúp", "được chọn" trên các file `.md`, `.json` của `results/T-043` (trừ thư mục lượt chạy). Chỉ còn câu phủ định ("không là bằng chứng … giúp") và câu mô tả thủ tục: tín hiệu của chuỗi cuối được chọn khi có đồ thị (D23); baseline dùng cho cờ M5 |

## 2. KS-16 (T0): số chính

- **Lượt chạy:**
  - luật F v1: `ks16/runs/pha1-001` (không nhãn; 288,3 s; RSS đỉnh 1,40 GB, `progress.jsonl`) và `ks16/runs/pha2-001` (ghép nhãn sau barrier). Bản chốt `ks16/dem-khong-nhan.json`, `ks16/dem-sau-ghep-nhan.json` là bản v1;
  - luật F v1.1: `ks16/runs/pha1-002` (556,4 s) và `ks16/runs/pha2-002`.
- **Phạm vi khác nhau giữa hai bản:** luật F chỉ đổi thời lượng và trạng thái ô của trace, log Nezha-OB ở 12 ca có khe giữa file. Các số ở mục 2.1, 2.2, 2.4–2.7 giống hệt ở hai bản (`runs/so-v1-v11-004/ket-qua.json#/so_sanh`). Mục 2.3 ghi số của cả hai bản. Con trỏ `#/...` dưới đây trỏ vào bản chốt v1 khi không ghi khác.

### 2.1 Cấu trúc trace (`ks16/dem-khong-nhan.json#/tong_hop/<dataset>`)

| | RE2-TT (30 ca) | Nezha-OB (22 ca) |
|---|---:|---:|
| Span trong miền chế độ (a) | 9.514.577 | 1.416.087 (sau bỏ 5.800 bản lặp y hệt) |
| Span mồ côi | 78.702 | 32.584 (span vào có parent không resolve) |
| Con khác chủ (lời gọi) | 1.651.558 | 338.829 |
| Span bọc chặt (= lỏng) | 1.643.384 | 338.829 |
| Cha có ≥ 2 con | 494.815 | 277.534 |
| Cha có cặp con chồng lấn > 1 ms | 0 | 444 (0,16%) |
| Con vượt biên cha > 1 ms | 6.272 | 5.808 |
| Độ sâu dịch vụ lớn nhất | 4 | 2 |

### 2.2 Hỗ trợ đơn vị và chế độ cổng (`#/tong_hop/<dataset>/op_E1_tat`, `op_E1_bat`, `canh_E2`, `metric`, `tan_suat_E3b`)

| | RE2-TT | Nezha-OB |
|---|---|---|
| Thao tác đủ hỗ trợ, E1 tắt | 3.244/4.080 (1.162 chính xác, 2.082 xấp xỉ) | 990/1.210 (236, 754) |
| Thao tác đủ hỗ trợ, E1 bật | 2.665/4.080 (1.047, 1.618) | 670/1.210 (152, 518) |
| Cạnh E2 đủ hỗ trợ | 979/1.440 (352, 627) | 251/286 (54, 197) |
| Kênh metric đủ hỗ trợ | 10.808/10.872 (đều xấp xỉ, 300 + 300 điểm) | 3.579/3.630 (đều chính xác, 5 + 5 điểm) |
| NEW_OP, STOPPED | 4, 0 | 0, 22 |

- Bốn NEW_OP của RE2-TT là `ts-order-other-service` / `getMore ts.orders` ở 4 ca.
- 22 STOPPED của Nezha-OB là 11 thao tác luồng checkout trong 2 ca (Đ4).

### 2.3 Trạng thái quan sát (cả hai bản luật F)

- **RE2-TT** (giống nhau ở v1 và v1.1):
  - trace, log, metric phủ ít nhất [t−719, t+719] ở mọi ca có file: đầu F trong [t−720, t−719], cuối F trong [t+719, t+722] (`#/cases/*/quan_sat/*/F_rel_t`). Một ca (dev-3defe3d34b) không có file log;
  - không có ô OPEN nguyên ô. Phần OPEN chỉ ở mép cửa sổ: trace 30/30 ca (≤ 0,90 s ở N, ≤ 1,40 s ở A); log 3/30 ca (≤ 1,0 s).
- **Nezha-OB:**

| | v1 (`ks16/dem-khong-nhan.json`) | v1.1 (`ks16/runs/pha1-002/dem-khong-nhan.json`) |
|---|---|---|
| T^chắc của trace, N (`#/tong_hop/Nezha-OB/quan_sat/trace/T/N`) | 41,4–96,9 s | 41,4–96,9 s |
| T^chắc của trace, A (`.../T/A`) | 84,2–140,4 s | 84,2–140,1 s |
| Ô N: A0 / biên / thiếu thu (`.../trace/o/N`) | 150 / 22 / 488 | 145 / 27 / 488 |
| Ô A: A0 / biên / thiếu thu (`.../trace/o/A`) | 228 / 22 / 410 | 216 / 34 / 410 |
| Phần OPEN của trace, log | không có | không có |

- Log Nezha-OB cho cùng số ô. Đầu mút khoảng T^chắc của log lệch trace dưới 0,07 s.
- Ô ngoài ba file phút là XÁC NHẬN THIẾU THU ở cả hai bản. v1.1 chuyển thêm 5 ô N và 12 ô A từ A0 sang ô biên, vì các ô đó chứa khe giữa hai file.
- **Hệ quả:** câu "tối đa khoảng 150 giây" ở SPEC B1.5 sai so với dữ liệu (R7-1). Dự đoán của SPEC "E3b trên Nezha-OB OBS_DEPENDENT" mất căn cứ. Cả hai đúng với hai bản luật.

### 2.4 Nối log–span (`#/cases/*/log_span_join`)

- Nezha-OB: 1.539.335 dòng log trong miền, đều có TraceID và SpanID. 1.537.834 dòng khớp đúng một span của miền (99,90%); 1.501 dòng không khớp; 0 dòng lệch thời gian quá 1 s.
- RE2-TT: không có cột ID; 0 thông điệp chứa chuỗi hex 32 ký tự.
- Đề xuất chưa dùng nối log–span trong bản P7, là lựa chọn ưu tiên phạm vi; câu hỏi lợi ích của nối giữ OPEN, Nezha-OB dev phân xử được (WHY-M1-07; `dinh-chinh-phien10.md` Đ18).

### 2.5 Mốc giả RE2-TT (`#/cases/*/moc_gia`, `quan_sat_moc_gia`)

- Cả 30 ca có dữ liệu cho miền [t−600, t): F của trace bắt đầu trong [t−720, t−719] ở mọi ca. Ví dụ dev-03d4910932: N′ có 157.409 span, A′ có 163.726 span.

### 2.6 Ô kích hoạt, kiểu quan sát, hình dạng xếp hạng (`ks16/dem-sau-ghep-nhan.json`)

| Thành phần | RE2-TT (10 ô) | Nezha-OB (13 ô) | Tổng | Ít ca (< 6) |
|---|---:|---:|---:|---|
| E1 | 8 | 11 | 19 | không |
| E1-CP | 0 | 11 | 11 | theo Q2: KHÔNG ĐỦ CA (tỷ lệ chồng lấn < 5% ở cả hai dataset) |
| E2 | 2 | 6 | 8 | không |
| E2-VC | 8 | 9 | 17 | không |
| E3 | 0 | 4 | 4 | **có** |
| E3b | 7 | 5 | 12 | không |
| E5 | 8 | 12 | 20 | không |
| E6b | 8 | 13 | 21 | không |
| E9 | 4 | 6 | 10 | không |
| T12 | 10 | 3 | 13 | không |

- Định nghĩa: `dinh-nghia-pha2.json`, băm vào LOG phiên 7 trước pha 2.
- Số của E1 (8/11) và E2 (2/6) trùng số xem trước của SPEC, vì dùng cùng định nghĩa.
- Kiểu quan sát root (`#/kieu_quan_sat_root`): RE2-TT O1 24, O2 6; Nezha-OB O1 20, O2 2; không có O3 hay O4. O1–O4 do người làm định nghĩa (R7-2).
- **Hình dạng xếp hạng baseline** (`#/hinh_dang_xep_hang_baseline`): MRR đọc lại từ bản ghi P3 khớp bảng G2 ở 12/12 cặp phương pháp × dataset (sai số < 1e−9). Số ca có cờ M5 cơ sở:
  - RE2-TT: BARO 3, SimpleRCA 5, MicroRank 5, TraceRCA 4, CIRCA 10, TORAI B 1;
  - Nezha-OB: BARO 7, SimpleRCA 9, MicroRank 20, TraceRCA 16; CIRCA và TORAI B là 0 vì UNSUPPORTED.

### 2.7 Đối chiếu

| Đối chiếu | Kết quả |
|---|---|
| T-035 K3 | RE2-TT 22.834.238 span toàn bảng; 22.639.789 có cha; 22.437.039 resolve. Nezha-OB 1.421.887 dòng adapter. Đều khớp đúng |
| T-042 | 1.539.335 dòng log Nezha-OB khớp `histogram-001/full-summary.json#/counts/rows` |
| T-032 `call-interval-001` | RE2-TT khớp đúng 26/26 ca. Nezha-OB khớp 3/22 ca; 19 ca lệch 0,3–3% vì T-032 bỏ mọi bản của khóa span lặp (`call_interval_table_v1.py:57`), còn T-043 giữ một bản (SPEC B1.2). Áp quy ước T-032 trong bộ nhớ ra đúng số T-032 ở ba ca kiểm (LOG phiên 7) |
| Nhãn T-022, T-026 với nhãn trong `call-interval-001` | 52/52 khớp |
| Bản ghi baseline P3 | 0 bản ghi lệch hash so với index đóng băng |
| Hash nguồn (bước 0) | Lượt `runs/hash-nguon-001` FAIL (script đọc sai khóa ghim allowlist T-022, chưa tách file dùng/không dùng; giữ lại). Lượt `runs/hash-nguon-002`, `-003` PASS mọi file T-043 dùng. Năm file không dùng bị lệch hash so với manifest cũ: `results/T-026/cham-a.md`, `tasks/T-026-nezha-ob-che-do-a/LOG.md`, `docs/STATE.md`, `results/T-024/cham-a.md`, `results/T-024/scripts/report.py` (`runs/hash-nguon-003/ket-qua.json#/nhom/*/lech_o_file_khong_dung`). Không dùng chúng để lấy số; lệch hash tự nó không chứng minh sửa trái phép |

## 3. Fixture (bước 3)

- 82 mục, đáp án literal tính tay (`fixture-dac-ta.json`).
- Kiểm bằng hai cách độc lập (`fixture/kiem_fixture.py`):
  - lượt `fixture/runs/kiem-001.json`: 108/109 khớp. Mục 47 lệch vì script chưa xuất hai trường, không phải đáp án sai;
  - lượt `kiem-002.json`: 109/109 khớp ở cả A và B, phủ 82/82 mục.
- Cổng chính xác B1.8 so với oracle phân số: 6/6 khớp, sai số ≤ 1e−12 (1/252; 2/481; C(34,14)/C(40,20); 1; C(90,40)/C(100,50); 7.136/7.391.536.347.803.839).
- **Phạm vi thật của "hai cách khớp":**
  - mục 1 (S1–S7) và 8, 57, 58, 71, 80 kiểm ở **mức kênh**: logic tầng, E2-VC, E5, xếp hạng, RR;
  - phép tính span → kênh của S1–S7 là suy luận tay ghi ở `trace_mau_S`; phép tính span của E1, E2 được kiểm riêng ở mục 2–5, 44, 72;
  - các khối 46–50 nhận kết cục cặp làm đầu vào; chỉ mục 45 tính từ kênh tới luật C và luật khối;
  - vài trường định nghĩa chỉ chép literal, không tính (`khong_co` của 55, `giu_luot_chinh` của 61, `nguyen_nhan` của 29 khi nhãn ổn định);
  - chưa có fixture cho khe giữa hai file (luật F v1.1). Fixture 21 dùng một file liên tục.
- **Kết quả đáng chú ý:** đáp án S1–S7 tính lại theo B1.3 khác bảng B5 bản 1.
  - Cột C-a0: F, A có hai kênh nên đứng trước R.
  - S2, S2b cột +E1: E1 bật bỏ span bọc khỏi mẫu thao tác; E2 tắt, nên không còn kênh nào có cờ, sáu thực thể hòa.
  - Hệ quả thiết kế đã nằm trong D21: E1 bật mà E2 tắt thì làm mất tín hiệu trễ mạng.

## 4. Ma trận thử (bước 5)

- `ma-tran-thu.json`, đóng băng trước bước 6 và trước mọi code thành phần.
- **R0** không dùng quan hệ.
- **Khối K:** 16 cấu hình E1-U × E2-C × E3 × E5; luật chọn khối; E3 là thành phần ít ca.
- **K-b:** chỉ E2-VC, tối đa 2 cấu hình (E1-CP khai trước KHÔNG ĐỦ CA).
- **Các bước sau:** T6 (E3b), T9 (E6b), T11 (E9), T12 (cạnh tĩnh) quyết định theo luật C; KB đảo trạng thái 4 thành phần.
- **T13 chỉ báo cáo:** C-a0, C-a1, C-d1, C-d2, C-d3, C-c, C-g, C-e. C-h là ứng viên, chưa vào T13 (`dinh-chinh-phien10.md` Đ16).
- **Ngân sách:** K + K-b + KB = 22 × 52 = 1.144 lượt chấm, dưới trần 1.300 của SPEC.
- **Đính chính:**
  - câu về ba thế giới sai một phần (Đ3);
  - `#/ngan_sach/thoi_gian` trỏ "bao-cao.md mục 6", nhưng dự toán nằm ở mục 9 của báo cáo này (Đ7). Ma trận đóng băng trước khi báo cáo có bố cục cuối, nên không sửa ma trận.

## 5. Nhận xét F_s của Codex, đính chính phiên 8, tính lại

Chi tiết ở `dinh-chinh-phien8.md`. Tóm tắt:
- **Nhận xét đúng một phần.**
  - Phần lớn khoảng ngoài file ở Nezha-OB có căn cứ phía thu/xuất: điều kiện xuất dữ liệu ở T-008 §8, cộng metric cho thấy hệ đang chạy (740/740 điểm workload trước F_s dương).
  - Văn bản v1 không nêu căn cứ đó. Mép ngoài lấy theo bản ghi đầu và cuối là giả định chưa kiểm, không có cận sai số (câu "≤ 3,6 ms" của phiên 8 đã rút; `dinh-chinh-phien9.md` Đ9).
- **Phát hiện thêm:**
  - code v1 gộp khe giữa các file phút vào F: 30 khe ở 12/22 ca, dài 0,055–1,212 s (`runs/bien-F-001/ket-qua.json`). Luật v1.1 tách khe ra ngoài F;
  - văn bản đặc tả v1, trường `khe_file_toi_da_s` của hợp đồng và code v1 không cùng một nghĩa. Số v1 khớp cách đọc "nối khe ≤ 10 s", số v1.1 khớp cách đọc nghĩa đen "hợp các khoảng của từng file" (Đ1);
  - hai lỗi chữ khác trong file đã đóng băng: câu trỏ mục của ma trận (Đ7), số làm tròn ở đặc tả v1 §2.2 điểm 9 (Đ8).
- **Đề xuất thêm:** khoảng ghi đi vào phương pháp qua `params.coverage`; không dùng ở chế độ (b) trên Nezha-OB, vì file phút mang thông tin phút tiêm.
- **Tính lại** (`dinh-chinh-phien8.md` Đ5; `runs/so-v1-v11-004/ket-qua.json`):
  - RE2-TT: không đổi giá trị nào;
  - Nezha-OB: 12/22 ca đổi; T^chắc giảm ở 13 cặp (ca, phía), nhiều nhất 1,212 s (1,01%) (`#/T_Nezha_OB_giam_tuong_doi_lon_nhat`);
  - ô kích hoạt, O1–O4, hình dạng xếp hạng giống hệt từng ca (`#/pha2_kich_hoat_giong_nhau_moi_ca`); số ô T0 của ma trận không đổi;
  - đơn vị đếm đại diện ở mức KS-16 đổi quyết định cổng: RE2-TT 0/5.388; Nezha-OB 4/1.420 (`#/don_vi_dem_doi_quyet_dinh`). Điểm sau cổng đổi ở 140 đơn vị Nezha-OB, lệch tối đa 0,105 khi cổng đổi kết quả (`#/don_vi_dem_doi_diem_the_gioi_P`). Đây chưa phải điểm M1.
- **Quan sát thêm (chưa kiểm):** quyết định cổng của đơn vị đếm có n lớn đổi khi T đổi dưới 1,1%. Task cài đặt cần dùng đúng luật F mà Minh duyệt.
- **Sau phản biện kết quả (phiên 9; Q-207):**
  - Chênh giữa v1 và v1.1 là độ nhạy, không là sai số so với sự thật. Khe giữa hai file không xác định được là đã thu hay chưa thu.
  - Minh chọn luật F phương án (a): khe dương giữa hai file là OPEN (T^chắc không tính khe, T^max tính khe); mép ngoài là giả định chưa kiểm, không có cận (`dinh-chinh-phien9.md` Đ9).
  - Theo (a), đơn vị đếm đại diện phụ thuộc quan sát: RE2-TT 5 (có sẵn do phần OPEN ở đầu, cuối cửa sổ; 0 phát sinh thêm), Nezha-OB 4 (đều do khe; đúng bốn đơn vị lật giữa v1 và v1.1) (`runs/khe-open-002/ket-qua.json#/tong_hop`). Thế giới P trùng số v1.1; ô kích hoạt và số T0 không đổi. Lượt `runs/khe-open-001` hỏng ở bước kiểm hash, giữ lại.
  - Ba thế giới chỉ quét phần bất định đã đưa vào T, không bao bất định ở mép ngoài.

## 6. Bảng bao phủ nguồn

| Nguồn | Yêu cầu | T-043 bao phủ | Chưa bao phủ, nơi nhận |
|---|---|---|---|
| DT18-NV2 | Log, trace, metric ánh xạ lên đồ thị phụ thuộc | Đặc tả v1 §5 (danh mục kênh theo nút và cạnh), §7 (E1 cha–con, E2 cạnh, E5 cạnh có hướng); hợp đồng kênh | Cạnh dữ liệu, thông điệp, triển khai (E8): FlashTicket |
| DT18-NV2 | Xác định vùng ảnh hưởng | E7, hai cách dựng, gọi đúng là "vùng nghi ngờ"; T10 mô tả | P/R/F1 vùng chỉ đo được trên FlashTicket (P10) |
| DT18-NV2 | Phát hiện dấu hiệu bất thường | Mức thành phần: E4, E5 (đồ thị tham gia điểm bất thường) | Mức hệ thống (RQ3a): SPEC phát hiện riêng (D3) |
| DT18-NV2 | Xếp hạng nguyên nhân gốc | E6a, E6b; khối K, T9; MRR độ đo chính (WHY-06) | Đánh giá ở P7 |
| DT18-NV3 | Thực nghiệm dữ liệu công khai trước, áp dụng hệ bán vé sau | Ba chặng, hai bản P7/FlashTicket, phép so D14 (`bang-chuyen-giao.json`) | Thực hiện ở P7, P10 |
| Cô, bước 2 | Graph-based anomaly detection; ví dụ PageRank, subgraph, GNN | E5 (đồ thị tham gia chấm); E6b (PageRank cá nhân hóa); E7 (đồ thị con bất thường → vùng) | GNN hoãn (mục 7). E7 chưa là "subgraph anomaly detection" theo nghĩa hẹp (MRP §2.3) |
| Cô, bước 4 | So với RCA cơ sở; P, R, F1, MRR, NDCG | T13 chỉ báo cáo trên dev; MRR chính, NDCG@5 báo kèm | Kết luận so sánh ở P7 (E-04); P/R/F1 thuộc phát hiện (D3) và vùng (P10) |
| MRP RQ3b | MRR, NDCG, Hit@k | Ma trận, luật chọn | P7 |
| MRP RQ3c | Vùng ảnh hưởng | T10 mô tả | P10 |
| MRP RQ3d | Bỏ quan hệ; quy tắc đơn giản trên cùng đồ thị | C-a0, C-a1, C-d1, C-d2, C-d3 (T13); C-h là ứng viên, chưa vào bản P7 (Đ16); phạm vi theo B3 (D23) | Không có đồ thị ngẫu nhiên (M-25); lợi ích do cấu trúc thật không trả lời được |
| MRP RQ5 | Áp dụng trên FlashTicket | Hợp đồng và kế hoạch phép so (B1.9, D14) | P10 |
| MRP P6 tầng 1–4 | Ánh xạ, chấm có đồ thị, vùng, xếp hạng | E1–E4; E5; E7; E6 | Hiệu quả: ba task cài đặt |
| MRP §6.7 | Phép thử giả | C-e (RE2-TT); tỷ lệ `CAUSE_FOUND` tuyệt đối | Nezha-OB không có mốc giả (D6) |
| MRP P8, P9 | Gói bằng chứng; yêu cầu quan sát | Mục 10; `hop-dong.json#/goi_bang_chung` | P8, P9 |

**Quyết định phụ thuộc phần chưa bao phủ:**
- chọn thành phần: ba task cài đặt;
- khóa G3: sau task (3) và A4;
- RCA chế độ (b) (D16): sau SPEC phát hiện, trước khi khóa bản FlashTicket.

## 7. Ba cách ứng viên của MRP P6 tầng 2

| Cách | Trạng thái | Lý do |
|---|---|---|
| Quy tắc phân rã theo cây lời gọi | Đưa vào ma trận thử làm ứng viên chính: E1 (trừ con), E2 (khoảng ngoài span), E5 (giải thích loại trừ) | Nối với G2-H03, G2-H06, G2-H17 và UV-1, UV-2 (mức ĐC); đồ thị tham gia điểm bất thường (MRP §2.3). Điều kiện thất bại đã khai: bất đồng bộ, thiếu span con, lỗi không làm chậm. Trên dev, E1-CP không đạt điều kiện chạy K-b theo Q2; khác biệt trên 444 cha chồng lấn ở Nezha-OB chưa được kiểm (Đ21) |
| Hồi quy có điều kiện kiểu CIRCA | Không đưa vào chuỗi M1 bản P7; CIRCA vẫn là baseline P3 | Bằng chứng dev bất lợi: G2-H12 (phần dư gần 0 cho điểm cực lớn, bước DA cộng sang tổ tiên), G2-H13 (hồi quy theo nút cha làm điểm cao hơn bản không cạnh ở 3.285/4.526 nút; nhạy với cửa sổ). UV-8 ghi: muốn thử lại cần cách xử lý giá trị không hợp lệ và chuẩn phần dư, và bản có cạnh phải hơn bản bỏ cạnh (hiện 12 so với 12 trên 19 ca) (`results/T-034/goi-g2.md` mục 5) |
| GNN dự báo hành vi bình thường kiểu GDN | Hoãn | WHY-10 chưa đạt đủ ba tiêu chí: chưa có hiện tượng phụ thuộc ngữ cảnh mà chấm theo phần tử bỏ sót; thiếu dữ liệu học không lộ nhãn; ràng buộc CPU laptop. PLAN-P6 C15 chưa kích hoạt. Đây là thiếu căn cứ hiện tại, không là bằng chứng GNN thất bại |

## 8. Đồ thị tham gia phép tính ở đâu

| Thành phần | Nút, cạnh | Phép tính dùng quan hệ | Thông tin mất hoặc giả định |
|---|---|---|---|
| E1 | Cha–con trong trace | Hợp khoảng con; bỏ span bọc | Mất song song (CP chỉ là biến thể); "chưa được con phủ" chưa phải thời gian CPU |
| E2 | Cạnh dịch vụ qua span bọc | Mẫu g theo cạnh; phủ đỉnh | g gộp đường truyền, hàng đợi, xử lý phía gọi |
| E5 | Cạnh N ∪ A có hướng (+ cạnh tĩnh khi T12) | Loại kênh kế thừa theo lớp | Nhị phân hóa: cờ yếu ở bên được gọi xóa bằng chứng mạnh (fixture 57) |
| E6b | Đồ thị con F_raw | PageRank cá nhân hóa | Nút sâu hút khối lượng: ví dụ A(0,8) → R(0,6) cho π(R) ≈ 0,833 |
| E7 | Đồ thị con F_raw | Đường đi, liên thông | Root không cạnh hoặc không tín hiệu nằm ngoài vùng |
| E9 | Cạnh của E5 | Thứ tự khởi phát | Độ phân giải thô |
| C-d1, C-d3 | Cùng đồ thị | Độ sâu; đường đi | — |

- **C-a0 không dùng quan hệ** ở bốn chặng: đặc trưng, điểm, tập ứng viên, xếp hạng. Phần không tách được: lựa chọn tín hiệu E3, E3b của chuỗi cuối được chọn khi có đồ thị (D23).
- **C-a1** còn giữ cha–con (E1).
- **C-h** (ứng viên, chưa vào bản P7): không dùng quan hệ; công thức chưa khóa (Đ16).

## 9. Dự toán cho ba task cài đặt (ước lượng, chưa đo trên M1)

**Căn cứ đo được:**
- KS-16 pha 1 đọc và dựng cấu trúc 52 ca trong 288 s (lượt `pha1-001`, RSS đỉnh 1,40 GB) và 556 s (lượt `pha1-002`).
- Số đơn vị phải qua cổng (mục 2.2). Mỗi họ đơn vị chỉ cần một lần nhờ cache theo nội dung (B1.3):
  - cổng chính xác: RE2-TT 1.162 + 1.047 + 352; Nezha-OB 236 + 152 + 54, cộng 3.579 kênh metric 5 + 5 điểm;
  - cổng xấp xỉ: khoảng 16.600 đơn vị.
- Thời gian cổng đo trong phiên 8, khi máy đang chạy việc khác: chính xác 0,001 s (n = 20), 0,063 s (n = 60), 0,56 s (n = 100); xấp xỉ 0,0015 s (n = 600).

| Task (D1) | Phần việc | Ước lượng máy | Ghi chú |
|---|---|---|---|
| (1) T1, T4, T4b, khối K | Trích đặc trưng (khoảng 5–10 phút một lượt); cổng một lượt cho mọi họ đơn vị (cận trên khoảng 25 phút nếu mọi cổng chính xác có n = 100; thực tế nhỏ hơn); 16 cấu hình xếp hạng trên cache; T1 ba hash seed phải tính lại để kiểm bất biến | 1,5–3 giờ tổng; chia thành các lượt dưới 1 giờ (ví dụ mỗi hash seed một lượt) | Lượt dài hơn 1 giờ phải báo Minh trước (luật cứng 8). Ba thế giới chỉ nhân đơn vị đếm ở RE2-TT |
| (2) K-b, T6, T9, T10, T11, T12, KB | Khoảng 10 cấu hình trên đặc trưng đã cache | 0,5–1 giờ | — |
| (3) T13, hồ sơ G3 | Khoảng 10–15 cấu hình; C-c từ bản ghi P3 (giây); C-g nhẹ; bootstrap 10.000 mẫu theo ô (giây) | 0,5–1 giờ | Cộng thời gian soạn hồ sơ G3 |

Chi phí đợt phát triển FlashTicket vẫn OPEN (SPEC).

## 10. Giao diện cho P8 và P9

- **P8** (`hop-dong.json#/goi_bang_chung`):
  - gói gồm thứ hạng kèm khóa và tầng; đồ thị con bất thường; vùng R_r và vùng hợp; `inherited_by`; ba kênh lệch nhất mỗi thực thể; tối đa 3 dòng log tiêu biểu mỗi thực thể theo mẫu; `coverage`; `worlds`; `verdict`;
  - LLM không đổi thứ hạng; được trả lời "không đủ bằng chứng".
- **P9:**
  - định dạng nội bộ chung (WHY-08);
  - `params.coverage` dựng từ manifest lượt chạy và chỉ số collector (B16 mục 8; Đ2), để có trạng thái XÁC NHẬN CÓ QUAN SÁT và giảm phụ thuộc A0;
  - yêu cầu R-01 (kiểu span), R-03 (DB), R-04 (thông điệp), R-05 (host), R-06 (log nối span), R-07 (manifest), R-08 (lấy mẫu, drop), R-09 (ranh giới trace), R-10 (nối nguồn tĩnh) như `bang-chuyen-giao.json` ghi theo từng thành phần.

## 11. Còn mở, giới hạn, việc chờ Minh

**Đã quyết (Q-209, 29/10/2026; trước đó Q-207, Q-208):**
1. Đính chính phiên 8: Đ1 đóng, không dùng (thay bởi Q-207, `dinh-chinh-phien9.md` Đ9); Đ2 theo schema của `dinh-chinh-phien10.md` Đ19, giữ giới hạn chế độ (b) trên Nezha-OB; Đ3 theo Đ9; Đ4 theo Đ13; Đ5: task cài đặt (1) báo kèm số đơn vị đếm có quyết định cổng đổi khi T lệch ±1%, không dùng để chọn cấu hình; Đ6 giữ làm lịch sử; Đ7, Đ8 duyệt.
2. Đính chính phiên 9 (Đ9–Đ14, Q-207) và phiên 10 (Đ15–Đ18, Q-208; Đ19–Đ22, Q-209) đã ghi. Fixture bổ sung 8/8 khớp (`fixture/runs/kiem-bo-sung-002.json#/tong`); đây là kiểm đáp án đặc tả, không là kiểm cài đặt M1.
3. WHY-M1-01 đến 11 chép vào `docs/WHY.md` thành WHY-55 đến WHY-65.
4. C-h là ứng viên (Đ16). Dung sai đồng hồ τ = 1 ms cố định, chưa hiệu chỉnh cho dataset. C-d2 ở T13, chỉ báo cáo. "10 trường" theo đặc tả v1 §0.
5. Sửa chữ SPEC: dòng 82, 84, 127, 489 (Q-209 mục 5).
6. Nối log–span hoãn sang chặng 2, khóa trước chặng 3; câu hỏi lợi ích giữ OPEN (Đ18, Đ22).
7. Dừng phản biện; T-043 nghiệm thu trong phạm vi thiết kế. Lỗi đặc tả lộ ra khi cài đặt được ghi đính chính trong task cài đặt, chờ Minh duyệt; không mở lại T-043.

**Còn mở (không chặn T-043):**
- A0;
- giả định mẫu độc lập ở cổng (tự tương quan; T1 đo tỷ lệ qua cổng ở mốc giả);
- bảng lớp lan, đặc biệt "tần suất tăng": retry hay tải vào (thẻ MicroHECL);
- O03;
- độ phủ severity khác giữa N và A (N9);
- 1.501 dòng log Nezha-OB không khớp span (chưa phân loại nguyên nhân);
- lợi ích của nối log–span (Đ18, phân xử được trên Nezha-OB dev); đã quyết hoãn (Q-209); dự toán Đ22 chưa kiểm;
- hợp đồng Đ19 (thời gian, `r_ns`, cạnh tĩnh) chưa qua phản biện độc lập; đáp án H1–H6 chưa thành fixture chạy được;
- đường E4 → E5: cờ yếu ở bên được gọi có thể xóa bằng chứng mạnh ở bên gọi (fixture 57);
- giả định lớp mẫu Drain học từ N còn đúng ở A (Đ15);
- hiệu quả mọi thành phần;
- RQ3, RQ5, G3.

**Giới hạn của chính T-043:**
- O1–O4, ô kích hoạt, luật trạng thái quan sát và danh mục kênh là định nghĩa của người làm, chưa qua phản biện.
- Đáp án S1–S7 phụ thuộc trace mẫu tự dựng.
- Dự toán chưa đo trên M1.

## 12. Tác dụng phụ ngoài repo; phạm vi ghi

- **Ngoài repo:**
  - WebFetch tự lưu 5 PDF (CRISP, MicroHECL, TraceDiag, PRISM, DiagMLP) vào thư mục `tool-results` của phiên Claude (phiên 7);
  - lệnh chạy nền tạo file đầu ra tạm của Claude Code trong thư mục Temp của phiên (stdout của lượt chạy đã chuyển vào `results/T-043/`);
  - **vi phạm Luật 0 (phiên 8):** người làm tạo hai file nháp ngoài repo, ngoài quyền Q-206, trong scratchpad của phiên Claude: `log-phien8-phan1.md` (mục LOG) và `prompt-codex-T043-phien8.txt` (prompt), ở `C:\Users\84583\AppData\Local\Temp\claude\D--RCA-flashticket\ee010168-adc9-4542-af59-590e921ca79a\scratchpad\`. Đây là lặp lại loại vi phạm đã ghi ở Q-203. Nội dung hai file nằm trong LOG phiên 8. Minh duyệt xóa (Q-207); xóa ở phiên 9.
- **Quyền dữ liệu:** không đọc `data/locked/`, 34 ca test Nezha-OB hay RE3-OB. Nhãn dev chỉ đọc ở pha 2, sau khi số đếm không nhãn đã băm. Không tạo `__pycache__` (Python chạy với `-B`).
- **Ghi trong repo:** `results/T-043/` (mới); nối LOG T-043 (phiên 7, 8, 9); dòng T-043 trong STATE; Q-206, Q-207 trong DECISIONS. Không sửa SPEC, AGENTS, MRP, WHY chính thức, KE-HOACH, `src/`, kết quả task cũ. Không commit. Kiểm phạm vi ở LOG phiên 8 và 9.
- **Đính chính câu phạm vi của phiên 8:** LOG phiên 8 mục 3 ghi "Phạm vi ghi: chỉ các file trong quyền Q-206". Câu đó sai, vì có hai file nháp nêu trên.

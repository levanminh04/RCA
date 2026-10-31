# T-045 — Chạy T1, T4, T4b và khối K của M1 trên 52 ca dev

- **Trạng thái:** đã duyệt (29/10/2026, lời Minh trong chat: "duyệt toàn bộ các đề xuất, ngoài trừ 9 10 hoãn"), gồm bảng mặc định cho các điểm "Minh quyết" và phép độ bền. Bản này đã sửa theo lượt rà SPEC của Codex trong chat ngày 29/10/2026 (điểm 1: đặc tả phép độ bền). Triển khai sau khi T-044 được nghiệm thu.
- **Người làm:** Claude, chạy local trên máy của Minh. **Người phản biện:** Codex. Đổi ngày 31/10/2026 theo lời Minh: "045 sẽ là claude làm" (Q-215); trước đó Codex làm, Claude phản biện.
- **Thuộc gói MRP:** P6 (M1). **Cổng:** chuẩn bị G3.
- **Phụ thuộc:** T-044 đã nghiệm thu; code `src/m1`, `src/m1_danh_gia` lấy đúng commit được ghi khi nghiệm thu T-044.
- **Nguồn chia task:** D1 của SPEC T-043 (Q-199); Minh chốt tách task (1) thành T-044 và T-045 trong chat ngày 29/10/2026.

## Mục tiêu

**Câu hỏi nguồn:** như T-044 (DT18-NV2; cô bước 2 và 4; MRP P6 tầng 1–4; MRP P7 đoạn kiểm hành vi trên dev trước G3).

**Loại task:** chạy thử trên dev theo ma trận đã đóng băng (`results/T-043/ma-tran-thu.json`) và áp luật chọn đã khai trước (SPEC T-043 B4, Phụ lục C).

**Đạt task này** cho:
- kiểm cài đặt trên dữ liệu thật (T1);
- độ nhạy tham số E4 (T4) và mô tả nhánh z (T4b), chỉ báo cáo;
- cấu hình thắng của khối K, hoặc xung đột được trình Minh, theo luật chọn khối bước 1–8 và 10.

Task **không** cho bằng chứng hiệu quả trên dữ liệu chưa dùng để thiết kế (SPEC T-043 B4: MRR dev của cấu hình được chọn lạc quan). Task không trả lời RQ3d (thuộc T13) và không chạm G3.

**Phần nguồn chưa bao phủ và nơi nhận:** K-b, T6, T9, T10, T11, T12, KB (task (2)); T13, A4, hồ sơ G3 (task (3)); chế độ (b) (task sau SPEC phát hiện).

## Câu hỏi, bằng chứng và quyết định

Mọi dự đoán là **chưa kiểm**. Câu Q1, Q3, Q5, Q6, Q8 theo bảng câu hỏi của SPEC T-043.

| # | Câu hỏi | Giải thích khác | Phép kiểm | Hỗ trợ / bác bỏ khi | Còn thiếu |
|---|---|---|---|---|---|
| T1 | Code chạy đúng trên dữ liệu thật không? | Lỗi đọc dữ liệu, dạng dữ liệu fixture không phủ, phụ thuộc thứ tự hàng, hash seed | Bước 1–2 | Bất biến đạt; QT5 không có giá trị vô lý | Sai thì sửa cài đặt qua đính chính |
| Q5 | Điểm E4 có hữu hạn, đúng miền; nhánh z khác ra sao? | Bão hòa, trôi nền | T4b vế (1), (2) | Vế (1) sai thì sửa cài đặt; vế (2) chỉ mô tả | E4 cố định (D24) |
| Q1, Q3, Q6, Q8 | E1-U, E2-C, E3, E5 bật/tắt trong bối cảnh khối | Một ca đổi hạng đã vượt ngưỡng; nhiễu do 52 ca | Khối K, luật C cho từng cặp, luật chọn khối | Theo luật C và luật chọn khối | Kết cục ở bối cảnh chuỗi cuối kiểm ở KB (task (2)) |
| S | Lựa chọn của khối K bền tới đâu khi đổi mẫu ca? | Lựa chọn do vài ô quyết định | Phép độ bền (bước 7), chỉ báo cáo | — | Không dùng để chọn |

## Đầu vào

**Quyền dữ liệu:**
- RE2-TT: 30 ca dev trong `data/rcaeval/`, chọn qua `src/p3/selector.py`.
- Nezha-OB: 22 ca dev theo `results/T-026/allowlist-dev.json`, đọc qua `src/p3/nezha.py`.
- Mốc giả C-e: chỉ RE2-TT, t′ = t − 300 (đặc tả v1 §8).
- Nhãn chỉ đọc ở pha 2, bởi `src/m1_danh_gia`, sau khi bản ghi pha 1 đã băm.
- Không đọc `data/locked/`, 34 ca test Nezha-OB, RE3-OB.

**Nguồn kiểm hash trước khi dùng:** `results/T-043/manifest.json` (lệnh `py -3 -B results/T-043/scripts/tao_manifest.py --kiem`); manifest của T-044; dữ liệu theo `data/README.md`; nguồn ở bảng "Nguồn phải kiểm hash" của SPEC T-043 mà bước chạy dùng tới (bản ghi P3 cho C-c, C-g không thuộc task này). Cho D2: bản ghi baseline P3 đã đóng băng (`results/T-024/ban-ghi-dua-vao-cham.json`, `results/T-026/ban-ghi-dua-vao-cham.json`, kiểm sha256 từng bản ghi như `results/T-043/ks16/ks16_pha2_v11.py`), nhãn dev (`results/T-022/nhan-dev.json`, `results/T-026/nhan-dev.json`), chỉ đọc ở pha 2.

**Môi trường:** `results/T-044/requirements-m1.txt` (ghim ở T-044), dựng thành một venv local. Ghi đường dẫn venv và phiên bản thực tế vào LOG.

**Quyết định áp dụng:** SPEC T-043 Phụ lục C và D (D2a–D2f, D12, D17, D22, D24); Q-207, Q-208, Q-209 (Đ5: báo số đơn vị đếm có quyết định cổng đổi khi T lệch ±1%, không dùng để chọn).

## Đầu ra (`results/T-045/`)

1. `runs/<lượt>/`: bản ghi pha 1 theo `hop-dong.json`, hash; kết quả pha 2; `progress.jsonl` (thời gian, RAM theo bước); stdout. Giữ mọi lượt, kể cả lượt hỏng.
2. `t1.json`: bất biến thứ tự hàng, hash seed 0/1/2; phân bố điểm; QT5; tỷ lệ qua cổng ở mốc giả RE2-TT theo loại đơn vị và nguồn; tỷ lệ `CAUSE_FOUND` tuyệt đối ở mốc giả; Đ5.
3. `t4.json`, `t4b.json`: độ nhạy (9 cấu hình) và nhánh z; chỉ báo cáo.
4. `khoi-k.json`: 16 cấu hình × 52 ca; RR theo ca và ô; MRR theo dataset và gộp; ca đúng bị hỏng, ca được sửa; cờ M5; mốc giả theo `verdict`; dấu vết E5; luật C cho từng cặp ở ba thế giới; vết từng bước của luật chọn khối; cấu hình thắng hoặc xung đột; C-d1, C-d3 chỉ báo cáo.
5. `do-ben.json`: phép độ bền.
6. `so-lan-nhin.jsonl`: mỗi lần người làm xem số dev (thời điểm, file, con trỏ JSON, lý do) theo `ma-tran-thu.json#/ghi_lai_moi_lan_nhin_so`.
7. `dinh-chinh-cai-dat.md` (nếu có).
8. `bao-cao.md`, `manifest.json`.
9. Phép kiểm và mô tả bổ sung (Minh duyệt trong chat ngày 29/10/2026 cùng các đề xuất của người làm T-044; xem LOG T-044, giai đoạn 2): `doi-chieu-ks16.json` (D1), `tai-lap-baseline.json` (D2), `e3-khong-nhan.json` (D3), `e1-cp.json` (D4), `nhom-vong.json` (D5).

## Phạm vi ghi

- `results/T-045/`;
- `tasks/T-045-chay-khoi-k-dev/LOG.md`;
- dòng T-045 trong `docs/STATE.md`;
- `src/m1/`, `src/m1_danh_gia/` **chỉ** để sửa lỗi theo đính chính đã được Minh duyệt; mỗi sửa có commit riêng, chạy lại toàn bộ test của T-044.

Không ghi `results/T-043/`, `results/T-044/`, `src/p3`, DECISIONS, WHY, MRP, KE-HOACH, task cũ.

## Các bước

0. **Mở phiên.** Đọc AGENTS, STATE, SPEC này, báo cáo T-044. Kiểm hash T-043, T-044, dữ liệu dev. Chạy lại toàn bộ test T-044 trên môi trường local (phải qua). Ghi dòng mở phiên.
1. **Chạy thử.** R0 trên 1 ca RE2-TT và 1 ca Nezha-OB. Soi trung gian theo QT5 (điểm lớn hơn 1e6, toàn hòa, ngưỡng cực lớn, một nhóm kênh chiếm gần hết); ghi thời gian, RAM, dự báo thời gian lượt đầy đủ. Lỗi thì ghi đính chính, dừng phần phụ thuộc.
2. **T1.** R0 với điểm E4 trên 52 ca × 3 hash seed, cộng 30 cặp mốc giả. Kiểm bất biến theo thứ tự hàng (xáo hàng, so đầu ra) và hash seed. Báo các đại lượng ở đầu ra 2, gồm Đ5.
   - **D1 (không nhãn):** đối chiếu số trung gian của M1 với `results/T-043/ks16/dem-khong-nhan.json#/cases/*` từng ca: span sau bỏ lặp, span mồ côi, span gốc, span bọc, số đơn vị đủ hỗ trợ, F, H, T. Lệch thì ghi đính chính, dừng phần phụ thuộc.
   - **D4 (không nhãn, chỉ mô tả):** với E1 = CP và E1 = U, mô tả u_CP − u_U trên các cha có chồng lấn hơn 1 ms ở Nezha-OB (444 cha theo `ks16/dem-khong-nhan.json#/cases/*/trace/parents_with_overlap`). Không đổi ma trận; K-b vẫn không chạy E1-CP.
2b. **Đo không nhãn trước D17** (pha 1, không đọc nhãn, chỉ mô tả):
   - **D3, E3:** cho từng cách khớp `params.tham_so_E3.khop` ∈ {(a) khớp hoàn toàn, (b) khớp theo ngưỡng, (c) khớp theo ngưỡng trong mẫu cùng lớp}: số mẫu theo thực thể; tỷ lệ dòng A vào "mẫu mới"; số thực thể có cờ "mẫu mới" ở mốc giả RE2-TT; số dòng A là dòng lỗi (severity ở Nezha-OB, từ khóa ở RE2-TT) bị gán vào mẫu lớp thường, ở cả hai dataset; năm mẫu đầu của hai ca mỗi dataset; tùy chọn số đo ở ngưỡng của Nezha (OB 0,9; TT 0,8).
   - **D5, nhóm vòng E5:** số kênh có trạng thái kế thừa khác nhau giữa cách đọc (C′) và cách đọc chẩn đoán (A), ở 16 cấu hình khối K và ở mốc giả. Chỉ để biết cách đọc ảnh hưởng tới đâu; không dùng để chọn.
3. **Điểm dừng D17 (bắt buộc).** Trình Minh tỷ lệ `CAUSE_FOUND` tuyệt đối ở mốc giả của R0, để Minh quyết có đặt mức tuyệt đối không. Ghi rõ mức (nếu có) được đặt sau khi xem dev T1. Trình cùng kết quả D3 để Minh chốt cách khớp của E3 (mặc định (a)), và kết quả D5. Ghi rõ lựa chọn được đặt sau khi xem số dev không nhãn. Chờ Minh trước bước 4.
4. **T4, T4b.** Chỉ báo cáo. T4b dẫn kết quả T4c của T4, không chạy lại.
5. **Khối K, pha 1.** 16 cấu hình × 52 ca, cộng mốc giả RE2-TT cho mỗi cấu hình. Ghi bản ghi, băm hash, ghi hash vào LOG trước pha 2. Ca ERROR giữ nguyên, tính là trượt ở pha 2.
6. **Khối K, pha 2.** Trước luật C, **D2**: dùng `src/m1_danh_gia` tính lại MRR và số ca có cờ M5 của sáu baseline từ bản ghi P3 đã đóng băng (G_N lấy từ `call_rows` của KS-16), rồi so với `results/T-034/bang-baseline.json#/ranking_mode_a` và `results/T-043/ks16/dem-sau-ghep-nhan.json#/hinh_dang_xep_hang_baseline`. Lệch thì dừng phần phụ thuộc, ghi đính chính. Sau đó: bộ đánh giá ghép nhãn; luật C cho mọi cặp ở thế giới P, S_lo, S_hi; luật chọn khối bước 1–8 và 10; C-d1, C-d3 chỉ báo cáo. Áp các mặc định khai trước ở mục dưới.
7. **Phép độ bền (chỉ báo cáo).** Không chạy lại phương pháp; dùng lại kết quả pha 2 của khối K.
   - **Đơn vị lấy mẫu:** ô, định nghĩa như `results/T-043/dinh-nghia-pha2.json#/rr_theo_o`. Lấy mẫu có hoàn lại **trong từng dataset**, giữ số ô của mỗi dataset. Một ô được chọn k lần thì mọi ca của ô đó tính k lần.
   - **Lấy ghép cặp:** một mẫu ô dùng chung cho mọi cấu hình của khối K và cho cả ba thế giới P, S_lo, S_hi.
   - **Đầu vào lấy mẫu là toàn bộ đầu vào của luật chọn**, không chỉ RR: RR theo ca và ô; số ô tăng/giảm P, M, P′, M′ (đếm theo bội số); cờ M5 theo ca (điều kiện riêng E5); điều kiện UV-6 của E3; `verdict` của các cặp mốc giả RE2-TT thuộc các ca trong mẫu (mẫu số C-e tính lại trên mẫu).
   - **Giữ cố định từ T0:** tập ô kích hoạt E_X của từng thành phần và phân loại "ít ca" (E3). Ô của E_X xuất hiện k lần trong mẫu thì đếm k lần ở P, M.
   - **Ngưỡng giữ nguyên như luật C:** δ = 0,01; δ_d = 1/n_d với n_d là số ca gốc của dataset (30, 22); mốc giả 0,10; M + M′ ≥ 3.
   - **Mặc định ở bảng dưới áp tự động**, không dừng. Mẫu rơi vào ba tình huống dừng (bước 7 không còn cấu hình; bước 8 cấu hình thắng không có E1, E2, E5) được đếm thành loại riêng, không gán cấu hình.
   - **Số lần và seed:** 1.000 mẫu, seed cố định ghi trong LOG trước khi chạy.
   - **Báo:** tần suất mỗi cấu hình thắng; tần suất từng thành phần được bật; tần suất từng loại không chọn được; tần suất cờ TRÁI CHIỀU và "phụ thuộc quan sát" ở cấu hình thắng.
   - **Diễn giải:** chỉ nói lựa chọn trên dev thay đổi bao nhiêu khi đổi mẫu ô. Không dùng để đổi lựa chọn, không là bằng chứng hiệu quả.
8. **Báo cáo.** Tách quan sát, suy luận, câu hỏi mở. Mọi số có con trỏ JSON. Không viết "thành phần X giúp"; chỉ ghi kết cục theo luật C (GIÚP, HẠI, KHÔNG TÁC DỤNG, KHÔNG ĐỦ CA, TRÁI CHIỀU) kèm phạm vi dev. Tạo manifest. Ghi mục kết thúc phiên vào LOG, cập nhật STATE, soạn prompt phản biện cho Claude.

**Mặc định khai trước cho các điểm "Minh quyết"** (duyệt cùng SPEC; Minh vẫn đổi được, đổi phải ghi lý do):

| Tình huống (SPEC T-043 B4, Phụ lục C) | Mặc định | Dừng chờ Minh? |
|---|---|---|
| D17 sau T1 | — | **Có** |
| D17: cách khớp của E3 (theo D3) | (a) khớp hoàn toàn | **Có** (cùng D17) |
| Bước 6: cờ TRÁI CHIỀU theo dataset nằm ở cấu hình thắng hoặc cấu hình có MRR cao hơn | Giữ cấu hình thắng theo bước 7; gắn cờ; báo MRR từng dataset | Không |
| Bước 7: không còn cấu hình nào (xung đột) | — | **Có** |
| Bước 8: cấu hình thắng không có E1, E2 hay E5 (mâu thuẫn MRP P6 tầng 2) | — | **Có** |
| Bước 8: kết cục đảo trạng thái mâu thuẫn với lựa chọn | Giữ cấu hình thắng; ghi xung đột kèm cặp liên quan | Không |
| Bước 8: cặp phụ thuộc quan sát của thành phần không ít ca (`kiem_cau_hinh_thang` ghi `phu_thuoc_quan_sat`; T-044 C7, G5) | Giữ cấu hình thắng; ghi "phụ thuộc quan sát" | Không |
| Bước 10: S_lo hoặc S_hi cho cấu hình thắng khác P | Giữ lựa chọn tại P; ghi "phụ thuộc quan sát" | Không |
| Luật C bước 7 (TRÁI CHIỀU theo ô) ở một cặp trong khối | Không là căn cứ loại (luật khối chỉ loại theo HẠI); ghi cờ | Không |

## Kiểm đúng đắn

- T1 là phép kiểm cài đặt không cần nhãn: bất biến, QT5, mốc giả.
- Pha 1 băm trước pha 2: chứng minh bản ghi phương pháp không đổi sau khi thấy nhãn.
- So ca đúng và ca sai có điều kiện tương ứng khi báo cờ M5 và dấu vết E5 (luật cứng 15); không gọi đó là xác nhận cơ chế.
- So số baseline đã công bố trong repo (TORAI B, SimpleRCA M4 ở `results/T-034/bang-baseline.json`) chỉ để định vị, không dùng để chọn (QT4).
- Không kiểm được trong task: hiệu quả trên dữ liệu chưa dùng để thiết kế; tương tác nhiều thành phần ở chuỗi cuối (KB, task (2)).

## Tiêu chí xong

1. Test T-044 qua trên môi trường local ở đầu phiên.
2. T1: bất biến đạt; không còn giá trị vô lý theo QT5, hoặc đã được sửa qua đính chính và chạy lại.
3. D17 đã được Minh quyết và ghi trong LOG trước T4b.
4. Khối K đủ 16 × 52 lượt chấm (ERROR được đếm, không bỏ ca); hash pha 1 ghi trước pha 2.
5. Luật chọn khối áp đủ bước 1–8 và 10, có vết từng bước; kết quả là một cấu hình thắng kèm cờ, hoặc một xung đột đã trình Minh.
6. Phép độ bền và Đ5 có trong kết quả; D1–D5 có trong kết quả; D1, D2 khớp hoặc lệch đã được xử lý qua đính chính.
7. Mọi lần nhìn số dev được ghi.
8. Báo cáo tách: kết cục theo luật C; điều đã quan sát; điều chưa phân xử; quyết định cho task (2).

## Không làm

- K-b, T6, T9, T10, T11, T12, KB, T13; hồ sơ G3 và A4 (task (2), (3)).
- Chế độ (b), D13.
- Đổi tham số, luật chọn hay ma trận sau khi thấy số dev; muốn đổi phải trình Minh như thay đổi thiết kế (`ma-tran-thu.json#/trang_thai`).
- Đọc dữ liệu khóa; chạy trên cloud (dữ liệu dev không nằm trong git và không đưa lên cloud).

## Chi phí ước lượng

- Máy: khoảng 1,5–3 giờ tổng (báo cáo T-043 §9, chưa đo trên M1), chia thành các lượt dưới 1 giờ. Bước 1 đo lại; nếu dự báo một lượt vượt 1 giờ thì dừng, báo Minh (luật cứng 8).
- RAM: KS-16 pha 1 đỉnh 1,40 GB (báo cáo T-043 §9); M1 chưa đo.
- Không tải dữ liệu mới.

## Rủi ro và điều chưa chắc

- 52 ca: một ca đổi hạng đã làm MRR đổi khoảng 0,01, bằng ngưỡng δ; kết cục luật C có thể do nhiễu. Phép độ bền giúp thấy mức mong manh, không sửa được vấn đề này.
- E3 đã khai trước là thành phần ít ca (4 ô); theo D2a nó được giữ bật ở bước 5 của luật khối nếu không bị loại vì hại.
- Code có thể lộ lỗi trên dạng dữ liệu fixture không phủ; xử lý bằng đính chính, mỗi lần chờ Minh.
- Thời gian chạy thực tế chưa đo.

## Prompt bàn giao

Prompt soát SPEC cho agent đối phương được trình trong chat ngày 29/10/2026, vì chưa có quyền ghi LOG. Khi SPEC được duyệt, người làm ghi prompt vào LOG.

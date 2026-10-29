# T-044 — Cài chuỗi M1 và kiểm đặc tả, chưa chạm dữ liệu dev

- **Trạng thái:** đã duyệt (29/10/2026, lời Minh trong chat: "duyệt toàn bộ các đề xuất, ngoài trừ 9 10 hoãn"), gồm ngoại lệ fixture D13 và cho phép kéo dài nhiều phiên. Bản này đã sửa theo lượt rà SPEC của Codex trong chat ngày 29/10/2026 (điểm 2: runner áp đính chính có hiệu lực).
- **Người làm:** Claude, chạy trong phiên cloud trên branch riêng (đề xuất; Minh chọn). **Người phản biện:** Codex.
- **Thuộc gói MRP:** P6 (M1). **Cổng:** chuẩn bị G3.
- **Nguồn chia task:** D1 của SPEC T-043 (Q-199) chia task cài đặt (1); Minh chốt tách task (1) thành hai task con trong chat ngày 29/10/2026: T-044 (cài và kiểm đặc tả) và T-045 (chạy T1, T4, T4b, khối K trên dev).

## Mục tiêu

**Câu hỏi nguồn:**
- DT18-NV2: ánh xạ log, trace, metric lên đồ thị phụ thuộc để xác định vùng ảnh hưởng, phát hiện dấu hiệu bất thường và xếp hạng nguyên nhân (`docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2).
- Cô: bước 2 và bước 4 (`docs/reference/sources/advisor-2026-09-23.md` §1).
- MRP P6 tầng 1–4, cấu trúc tổng; MRP P7 đoạn "Trước G3, phương pháp và các đối chứng đã khai báo phải được cài và kiểm đầu vào, trung gian, hành vi trên dev".
- Q-209 mục 9: "tiêu chí đầu tiên là mọi đáp án đặc tả thành phép kiểm chạy được trước khi chạy dữ liệu dev".

**Loại task:** cài đặt. Task viết code của chuỗi M1, các đối chứng và bộ đánh giá đúng như đặc tả T-043, rồi kiểm bằng đáp án đặc tả. Task không đọc dữ liệu dev, không chạy thành phần trên ca thật.

**Đạt task này** cho đủ căn cứ để mở T-045: code làm đúng đặc tả trên các ca giả có đáp án. Task không trả lời câu hỏi hiệu quả nào (RQ3b, RQ3c, RQ3d) và không kiểm hành vi trên dữ liệu thật; phần đó thuộc T-045 và các task sau.

**Phần nguồn chưa bao phủ và nơi nhận:**
- Hành vi trên dữ liệu thật (giá trị trung gian, thời gian, RAM): T-045 bước 0 và T1.
- Chế độ (b), biến thể nền lùi D13: task sau SPEC phát hiện (D3, D16 của SPEC T-043). Quyết định (i)/(ii) về chế độ (b) ở P7 còn chờ Minh.
- Chạy K-b, T6–T12, KB, T13 và hồ sơ G3 (gồm A4): task (2) và (3) theo D1.

## Câu hỏi, bằng chứng và quyết định

| # | Câu hỏi | Lựa chọn cần phân xử; giải thích khác | Phép kiểm | Hỗ trợ / bác bỏ khi | Còn thiếu |
|---|---|---|---|---|---|
| A1 | Code có làm đúng đặc tả không? | Code sai; hoặc đáp án đặc tả sai; hoặc đặc tả mơ hồ, nhiều cách hiểu | Test gọi code `src/m1` và so với đáp án trong file JSON (bước 3–5) | Mọi phép kiểm trong phạm vi qua mà không sửa đáp án ngoài thủ tục đính chính | Hành vi trên ca thật: T-045 |
| A2 | Test có thật sự bắt được lỗi không, hay qua vì kiểm lỏng? | Test rỗng, sai số quá rộng, so code với chính nó | Phép thử đột biến: cố ý làm hỏng một số hàm, test phải đỏ (bước 7) | Mọi đột biến bị bắt | — |
| A3 | Nhãn có lọt vào phương pháp không? (luật cứng 6) | Import nhầm bộ đánh giá; trường cấm trong bản ghi | Kiểm tĩnh import; bộ kiểm trường cấm duyệt đệ quy (fixture 74) | Package phương pháp không import bộ đánh giá hay đường dẫn nhãn; fixture 74 qua | — |
| A4 | Kết quả có tất định không? | Phụ thuộc thứ tự hàng, hash seed của Python, thứ tự duyệt tập | Chạy toàn bộ fixture với thứ tự hàng xáo trộn và `PYTHONHASHSEED` 0, 1, 2 | Đầu ra giống hệt | Trên dữ liệu thật: T-045 T1 |
| A5 | Đặc tả có chỗ sai hoặc mơ hồ lộ ra khi cài không? | — | Ghi mọi chỗ phải tự diễn giải | Không còn đính chính chưa được Minh quyết | Theo Q-209 mục 8 |

## Đầu vào

**Quyền dữ liệu:** không đọc bất kỳ file nào trong `data/`; không tải dữ liệu; không đọc bản ghi P3 có nhãn. Task chỉ dùng ca giả trong fixture.

**Nguồn từ T-043 (đã commit; kiểm hash trước khi dùng):**
- `results/T-043/dac-ta-phuong-phap-v1.md` (đặc tả v1), `hop-dong.json`, `ma-tran-thu.json` (đóng băng), `dinh-nghia-pha2.json`, `bang-chuyen-giao.json`.
- `results/T-043/fixture-dac-ta.json` (82 fixture; 109 phép kiểm theo `fixture/ket-qua-kiem.json#/so_phep_kiem`), `results/T-043/fixture/fixture-bo-sung.json` (B1–B8).
- Đính chính có hiệu lực: `dinh-chinh-phien8.md` (theo Q-209 mục 2), `dinh-chinh-phien9.md` (Q-207), `dinh-chinh-phien10.md` (Đ15–Đ22, Q-208, Q-209). Đáp án U1–U6 (Đ15) và H1–H6 (Đ19) nằm dạng bảng viết tay trong `dinh-chinh-phien10.md`.
- SPEC T-043 Phụ lục B (B1–B6), Phụ lục C, Phụ lục D.
- Lệnh kiểm hash: `python -B results/T-043/scripts/tao_manifest.py --kiem` (trên Windows dùng `py -3 -B`). Phải PASS trước bước 1.

**Code dùng lại, chỉ đọc:** `src/p3/cua_so.py`, `src/p3/danh_gia.py`, `src/p3/ban_ghi.py` (chỉ lấy danh sách `CAM`; không dùng `ban_ghi.kiem`, vì không duyệt list/tuple, SPEC T-043 dòng 157), danh sách khóa cấm của `src/p3/nezha.py`, `src/p3/selector.py`, `src/do_thi/builder.py`. Không sửa `src/p3`.

**Môi trường (ghim, duyệt cùng SPEC này):**
- Python 3.12.
- Theo bộ `py312-pin` (WHY-15) đã dùng ở T-043: numpy 1.26.4, pandas 2.2.3, scipy 1.14.1, networkx 2.5, pytest 8.3.4.
- `drain3` 0.9.11 (đặc tả v1 §7.3).
- pyarrow: ghim một phiên bản tương thích pandas 2.2.3 và ghi vào file yêu cầu; chỉ cần cho T-045 (đọc parquet).
- Người làm ghi `results/T-044/requirements-m1.txt` với đúng các phiên bản trên. Không sửa `requirements.txt` ở gốc. Cần thêm gói ngoài danh sách thì dừng, đề xuất.
- PageRank, SCC và các phép đồ thị: ưu tiên tự viết theo công thức đặc tả; nếu dùng networkx thì ghi hàm và phiên bản vào báo cáo.

## Đầu ra

1. `src/m1/`: package phương pháp. Gợi ý cấu trúc, người làm được đổi nếu ghi lý do:
   - hợp đồng vào/ra và bộ kiểm trường cấm đệ quy;
   - cửa sổ, trạng thái quan sát, ba thế giới (B1.1, B1.3b; đặc tả §2);
   - tiền xử lý span (B1.2; đặc tả §3);
   - E4: thống kê chung, cổng chính xác/xấp xỉ, cache theo nội dung, nhánh z (B1.3, B1.8; đặc tả §4);
   - danh mục kênh, severity, lớp tín hiệu (đặc tả §5);
   - thành phần E1-U, E2-C, E2-VC, E3 (kể cả nhánh tắt phương án A, D2d), E3b, E5, E6a, E6b, E7 (hai cách dựng, D19, D20), E9, cạnh tĩnh T12 (D8);
   - `verdict`, xếp hạng, khóa hòa;
   - đối chứng C-a0, C-a1, C-d1, C-d2, C-d3, C-c, C-g, C-e (đặc tả §8);
   - runner đọc `ma-tran-thu.json`, sinh mã cấu hình, ghi bản ghi theo `hop-dong.json` kèm hash.
2. `src/m1_danh_gia/` (package riêng): bộ đánh giá — RR theo ô, P/M, MRR theo dataset và gộp, luật C, luật chọn khối, điều kiện riêng E5, vế mốc giả, phụ thuộc quan sát, WORLD_DEPENDENT. Chỉ package này được đọc nhãn. Package phương pháp không import nó.
3. `results/T-044/fixture/dap-an-u-h.json`: đáp án U1–U6, H1–H6 chép từ `dinh-chinh-phien10.md`, mỗi mục ghi dòng nguồn.
4. `results/T-044/tests/`: test pytest đọc đáp án từ JSON (82 fixture, B1–B8, U1–U6, H1–H6) và gọi code `src/m1`, `src/m1_danh_gia`.
5. `results/T-044/runs/<lượt>/`: kết quả test (stdout, bảng qua/trượt theo fixture và phép kiểm), phép tất định, phép đột biến, thời gian.
6. `results/T-044/dinh-chinh-cai-dat.md` (nếu có): mọi chỗ đặc tả sai hoặc mơ hồ, kèm đáp án đề xuất, chờ Minh duyệt.
7. `results/T-044/bao-cao.md`, `results/T-044/manifest.json`.

## Phạm vi ghi

- `src/m1/`, `src/m1_danh_gia/` (mới);
- `results/T-044/`;
- `tasks/T-044-cai-dat-m1/LOG.md`;
- dòng T-044 trong `docs/STATE.md`.

Không ghi `src/p3`, `results/T-043/`, `requirements.txt` ở gốc, DECISIONS, WHY, MRP, KE-HOACH, task cũ. Chạy trên cloud: chỉ commit lên branch của phiên; không merge vào `master`, không push lên `master`.

## Các bước

0. **Mở phiên.** Đọc AGENTS, STATE, SPEC này, SPEC T-043 Phụ lục B–D, đặc tả v1, ba file đính chính. Chạy lệnh kiểm hash T-043 (PASS). Đếm 82 fixture, 8 fixture B. Ghi dòng mở phiên vào LOG.
1. **Môi trường.** Tạo `requirements-m1.txt`, cài, ghi phiên bản thực tế vào LOG. Kiểm: `python -c` in phiên bản từng gói khớp file.
2. **Chép đáp án U và H.** Chép U1–U6 (Đ15) và H1–H6 (Đ19) sang `dap-an-u-h.json`, kèm số dòng nguồn. Không tự sửa đáp án. Kiểm: người phản biện đối chiếu từng dòng.
3. **Khung test.** Viết test cho mọi fixture trong phạm vi trước khi viết thành phần; chạy để thấy đỏ. Sai số: theo fixture (cổng so với oracle phân số: ≤ 1e−12); thứ hạng và trạng thái: khớp tuyệt đối.
4. **Cài theo thứ tự phụ thuộc,** mỗi khối xong thì chạy test của khối đó và ghi một dòng LOG:
   1. hợp đồng, bộ kiểm trường cấm (fixture 74);
   2. cửa sổ, trạng thái quan sát, đếm, ba thế giới (21–24, 28–30, 82; H1–H6);
   3. tiền xử lý span (6, 7, 44, 72);
   4. E4, cổng, cache, nhánh z (25–27, 41, 75, 76, 81; B1–B8 phần liên quan);
   5. kênh, severity, lớp (77–79; U1–U6);
   6. E1-U (2–5); E2-C, E2-VC (9–13);
   7. E3 và nhánh tắt (55, 73); E3b;
   8. E5 (8, 57, 58, 71, 80); E6a, E6b (14–16, 69); E7 (70); E9; cạnh tĩnh (58);
   9. `verdict` (31, 42); chuỗi S1–S7 (1);
   10. đối chứng: C-d3 (17–20), C-g (33, 68), C-e (32, 43, 56), C-a0, C-a1, C-d1, C-d2, C-c;
   11. bộ đánh giá: luật C (34–40, 51–54, 60), luật chọn khối (45–47, 49, 50), bối cảnh (48).
   Số fixture ở trên lấy theo tên trong `fixture-dac-ta.json`; người làm đối chiếu lại và ghi bảng ánh xạ fixture → module vào báo cáo.
5. **Runner.** Đọc `ma-tran-thu.json` (giữ nguyên file đóng băng), áp các đính chính có hiệu lực (ví dụ Đ16 ở `dinh-chinh-phien10.md`: bỏ C-h khỏi T13, còn 7 đối chứng), rồi sinh đúng danh sách cấu hình của T1, T4, T4b, K, K-b, T6, T9, T10, T11, T12, KB, T13. Ghi bảng đính chính đã áp vào báo cáo. Hai pha: pha 1 chạy phương pháp, ghi bản ghi, băm hash, không đọc nhãn; pha 2 bộ đánh giá đọc bản ghi đã băm và nhãn. Kiểm trên ca giả của fixture: đếm cấu hình khớp `ma-tran-thu.json#/ngan_sach`; hash pha 1 không đổi khi chạy lại.
6. **Tất định.** Chạy toàn bộ test với thứ tự hàng xáo trộn (3 seed xáo) và `PYTHONHASHSEED` 0, 1, 2. Kiểm: đầu ra giống hệt.
7. **Đột biến.** Làm hỏng có chủ đích ít nhất 6 chỗ (ví dụ: đảo hướng lớp lan, bỏ cắt con ở E1, đổi khóa hòa, bỏ duyệt list trong bộ kiểm trường cấm, đổi δ trong luật C, đọc nhãn trong pha 1). Mỗi đột biến chạy trên bản sao tạm, không commit. Kiểm: test đỏ ở mọi đột biến.
8. **Đính chính.** Khi code và đáp án lệch nhau: dừng phần phụ thuộc; ghi vào `dinh-chinh-cai-dat.md` chỗ lệch, cách hiểu, đáp án đề xuất; chờ Minh duyệt (Q-209 mục 8). Không sửa đáp án, không nới sai số để test qua. Phần không phụ thuộc được làm tiếp.
9. **Báo cáo.** Bảng qua/trượt theo fixture; ánh xạ fixture → module; kết quả tất định, đột biến; danh sách tự diễn giải; điều chưa kiểm. Tạo manifest. Ghi mục kết thúc phiên vào LOG; cập nhật dòng STATE thành "chờ phản biện"; soạn prompt phản biện cho Codex.

## Kiểm đúng đắn

- Test so với đáp án ghi sẵn, không so với code kiểm của T-043 (`kiem_fixture.py`), để tránh hai bản cài chung một cách hiểu sai.
- Phép đột biến chứng minh test có sức bắt lỗi.
- Phép tất định trên ca giả. Tất định trên dữ liệu thật để T-045 T1.
- Không kiểm được trong task: giá trị trung gian, thời gian và RAM trên ca thật; hành vi khi dữ liệu thật có dạng mà fixture không phủ. Kết luận "code đúng" chỉ trong phạm vi fixture.

## Tiêu chí xong

1. `python -B results/T-043/scripts/tao_manifest.py --kiem` PASS ở đầu phiên.
2. Mọi phép kiểm của 82 fixture qua trên code `src/m1`/`src/m1_danh_gia`, **trừ** các phép thuộc fixture D13 (59, 61–67) đã nêu ở "Không làm"; B1–B8, U1–U6, H1–H6 qua. Số phép kiểm qua/tổng ghi bằng con trỏ JSON trong file kết quả test.
3. Test đọc đáp án từ JSON; không fixture nào bị sửa đáp án ngoài đính chính đã được Minh duyệt.
4. Kiểm tĩnh: không module nào trong `src/m1` import `src/m1_danh_gia` hoặc đọc đường dẫn nhãn; fixture 74 qua.
5. Tất định: đầu ra giống hệt qua 3 seed xáo hàng × 3 hash seed.
6. Mọi đột biến ở bước 7 bị bắt.
7. Runner sinh đúng danh sách và số cấu hình theo `ma-tran-thu.json` sau khi áp các đính chính có hiệu lực; hai pha tách được, hash pha 1 ổn định.
8. Không còn đính chính chưa được Minh quyết; nếu còn thì task dừng ở trạng thái "chờ Minh", không gọi là xong.
9. Báo cáo tách: đã kiểm, chưa kiểm, tự diễn giải.

## Không làm

- **Fixture D13 (59, 61–67)** và biến thể nền lùi: thuộc task sau SPEC phát hiện (`ma-tran-thu.json#/khong_lam_trong_ma_tran`). Đây là ngoại lệ so với câu chữ "mọi đáp án đặc tả" của Q-209 mục 9; cần Minh duyệt ngoại lệ này cùng SPEC. Lý do: đầu vào (định nghĩa luật Grafana, lịch sử trạng thái) chưa có và hợp đồng có thể đổi theo SPEC phát hiện. Hệ quả: khi làm chế độ (b) phải cài và kiểm D13 trước khi chạy.
- E1-CP (khai trước KHÔNG ĐỦ CA, chặng 2), E8, C-f (FlashTicket), C-h (ứng viên, Đ16), nối log–span (Q-209 mục 6), nhánh không quan hệ chọn riêng (D23), đồ thị ngẫu nhiên (M-25).
- Chế độ (b): không chạy. Hợp đồng cửa sổ nhận mốc t theo B1.1, không gắn chặt với mốc tiêm, để chế độ (b) không phải sửa code lõi.
- Đọc dữ liệu dev, bản ghi P3 có nhãn, `data/locked/`.
- Sửa `src/p3`, sửa hướng dẫn môi trường ở AGENTS §12 (đề xuất riêng sau task).

## Chi phí ước lượng

- Máy: không đáng kể (test trên ca giả).
- Token: lớn; đây là phần viết code chính của M1. Có thể vượt một phiên. Nếu vượt: ghi checkpoint vào LOG theo mục 5a, tiếp tục trên cùng branch ở phiên sau; mỗi phiên mở và kết thúc theo mục 6–7. Việc cho phép task kéo dài nhiều phiên cần Minh duyệt cùng SPEC.
- Không có thao tác thuộc luật cứng 8.

## Rủi ro và điều chưa chắc

- Đặc tả dài, có nhiều đính chính chồng lên nhau; người làm có thể đọc nhầm bản hiệu lực. Giảm bằng bảng ánh xạ fixture → mục đặc tả → đính chính.
- networkx 2.5 trên Python 3.12: đã chạy được ở môi trường T-043 (chưa kiểm trên máy cloud).
- Chép đáp án U/H có thể sai; người phản biện đối chiếu từng dòng.
- Fixture không phủ hết dạng dữ liệu thật; T-045 bước 0 có thể lộ lỗi mới, khi đó ghi đính chính trong T-045.
- Người làm (Claude) cũng là người viết đặc tả T-043, nên có thể mang cùng cách hiểu sai vào code. Giảm bằng: test so với đáp án viết sẵn; Codex phản biện đọc đặc tả độc lập.

## Prompt bàn giao

Prompt soát SPEC cho Codex được trình trong chat ngày 29/10/2026, vì chưa có quyền ghi LOG. Khi SPEC được duyệt, người làm ghi prompt vào LOG.

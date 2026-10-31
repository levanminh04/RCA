# T-044 — Cài chuỗi M1 và kiểm đặc tả (báo cáo)

- **Người làm:** Claude, phiên cloud rồi máy local Windows (từ 30/10/2026), branch `claude/sweet-hawking-dy078d`. **Người phản biện:** Codex (lượt 1 trong chat 29/10/2026: 3 CHẶN, 1 KHÔNG CHẶN; lượt 2: 7 CHẶN, 1 KHÔNG CHẶN, rồi kiểm phản hồi; lượt 3 ngày 30/10/2026: 2 CHẶN, 3 KHÔNG CHẶN, 1 nguy cơ có điều kiện; lượt 4 cùng ngày: 2 CHẶN, 6 KHÔNG CHẶN). Lượt 5 ngày 31/10/2026 do một phiên Claude soát theo yêu cầu của Minh (Claude là người làm nên lượt này không thay phản biện chính thức): 4 điểm CHẶN bắt đầu T-045, 9 điểm KHÔNG CHẶN, 28 đột biến đổi hành vi sống sót; đã sửa theo duyệt của Minh. Phiên Claude mới kiểm lại (31/10/2026): S33 chưa đạt, cách ghi khóa lệch bộ đánh giá, bốn nguy cơ cho T-045, 9 đột biến sống sót; đã sửa theo duyệt của Minh ("Duyệt cả gói", mục C8), chờ kiểm lại.
- **Ngày:** 29–31/10/2026. **SPEC:** `tasks/T-044-cai-dat-m1/SPEC.md` (đã duyệt; sửa theo các mục Minh duyệt ngày 29/10/2026, LOG giai đoạn 2).
- **Quyền dữ liệu:** không đọc `data/`, không tải dữ liệu, không đọc bản ghi P3 có nhãn. Mọi phép kiểm dùng ca giả.

## 1. Tóm tắt

**Task đạt gì (trong phạm vi fixture):**
- Code `src/m1/` (phương pháp, đối chứng, runner, adapter) và `src/m1_danh_gia/` (bộ đánh giá) theo đặc tả v1, ba bản đính chính T-043 và Phần I của `dinh-chinh-cai-dat.md`.
- 366/366 phép kiểm qua (`bang-phep-kiem.json#/tong`). Trong đó 97/97 phép của T-043 trong phạm vi (`#/T043/qua_trong_pham_vi`); 12 phép của fixture D13 loại theo ngoại lệ đã duyệt (`#/T043/loai_tru_D13`); B1–B8, U1–U6, H1–H6 và 145 mục đáp án tự lập qua (`#/theo_nhom`, `#/dap_an_tu_lap`).
- Không sửa đáp án đặc tả nào; không có đáp án đặc tả nào lệch với code. Đáp án tự lập WD1–WD3 đổi ở lượt 3 theo định nghĩa cặp mới của S13 (`dinh-chinh-cai-dat.md` mục C4); TS2 ghi đủ map bội số ở lượt 4 (S25, đáp án không đổi); T4C1 ca 2 do người làm tính tay sai lúc đầu (quên r_u = 2e308), đã sửa thành ln 2 trước khi chạy lượt cuối.
- Tất định: 104 bản ghi và 366 phép kiểm giống hệt qua 4 thứ tự hàng × PYTHONHASHSEED 0, 1, 2 (`runs/tat-dinh-011/tong-hop.json#/ket_luan`); hash seed ghi trong đầu ra và khớp (`#/ban_ghi/hash_seed_khop`).
- Đột biến: 128/128 bị bắt, trong đó 126/126 đột biến đổi hành vi (D07, D08 chỉ bị phép quét tĩnh bắt) (`runs/dot-bien-012/tong-hop.json#/so_bi_bat`, `#/so_bi_bat_hanh_vi`); 93 đột biến chỉ bị đúng một phép bắt (`#/so_bi_bat_dung_mot_phep`), sau khi lượt đầu lộ 2 lỗ hổng test và đã vá (`runs/dot-bien-001/tong-hop.json#/song_sot`). D22–D27 thêm sau phản biện lượt 1; D28–D35 sau lượt 2; D36–D41 sau lượt 3; D42–D44 sau khi Minh quyết E1-CP và bước 5; D45–D58 sau lượt 4; D59–D110 sau lượt 5; D111–D128 sau kiểm lại lượt 5 (D80 đổi thành đột biến ngược).
- Sau phản biện lượt 1: đã sửa ba lỗi CHẶN (bội số ô trong luật C, M5, UV-6, mốc giả; trạng thái quan sát của nguồn metric; cặp giải thích WORLD_DEPENDENT), thu hẹp lập luận E3 trong đề xuất WHY, và cho manifest kiểm được trên checkout CRLF (giả lập trên Linux, `runs/manifest-crlf-001`; chưa chạy trên Windows thật) (`dinh-chinh-cai-dat.md` Phần II mục C2).
- Sau phản biện lượt 2: đã sửa MRR chính xác tới hết luật chọn, ô bội số 0, bước 8 với cặp phụ thuộc quan sát, kiểm khai báo bắt buộc, thống kê severity và cặp Drain trong bản ghi, giải thích WORLD_DEPENDENT khi hòa hoặc vắng, trạng thái nguồn metric rỗng (mục C3). Chưa sửa, chờ Minh: quy tắc E1-CP; cách đọc cặp phụ thuộc quan sát ở bước 5 (mục D).
- Sau phản biện lượt 3: định danh kênh theo đơn vị (S12; lỗi làm đổi thứ hạng khi hai kênh khác đơn vị cùng tên), giải thích WORLD_DEPENDENT theo kênh đổi và phần khóa (S13), freeze dùng được trên máy khác (S15), báo kèm UV-6 theo Hit@1 kỳ vọng (S16) (mục C4). Chưa sửa: E7 ở C-a0/C-a1 (S14, cách sửa lệch hợp đồng, trình lại); `chon` khi thiếu cặp (S17, chờ Minh).
- Minh quyết hai OPEN ngày 30/10/2026 (mục C5): quy tắc E1-CP của M1 (τ = 1 ms, xét cả con đã chọn, biên mở, phá hòa PII-04; ca phản ví dụ 2600; lệch code CRISP ghi là giới hạn) (S18); bước 5 đọc cặp phụ thuộc quan sát là KHÔNG ĐỦ CA, giữ bật thành phần ít ca kể cả khi P cho HẠI (S19).
- Sau phản biện lượt 4 (mục C6): điểm và khóa xếp hạng so chính xác, hai điểm bằng nhau theo công thức không còn bị tách hòa vì số thực (S20); giá trị không hữu hạn không còn làm dừng pha 1 (S21); kiểm `bat_tat` (S22); lưu π gốc E6b (S23); kiểm số mốc metric (S24); map bội số phải đủ (S25); pha 2 kiểm bản ghi trùng, thiếu (S26); S14 (C-a0/C-a1 không dựng vùng) và S17 (thiếu cặp là lỗi).
- Sau phản biện lượt 5 (mục C7): luật chọn khối đòi đủ 2^n cấu hình, it_ca, do_thi hợp lệ (G1); luật C, bội số, UV-6 chỉ nhận số chính xác (G2); E_X phải thuộc tập ô của ca, mã ca không trùng (G3); pha 2 kiểm nhãn thành phần của cặp khối K (G4); bước 8 ghi riêng cặp phụ thuộc quan sát của thành phần không ít ca (G5, Q1); mã nội dung gồm `doi_chung` (G6); trùng mã đơn vị là ERROR (S27); verdict chỉ đếm phép chấm trong U (S28, Q2); ngưỡng E4 không tràn (S29); NEW_OP/STOPPED chỉ ở hướng được chấm (S30, Q5); kiểm khóa `nhanh_z`, `tham_so_E4`, `params_ca` (S31); E1-CP bỏ con bắt đầu trong khoảng của nút đang xét (S32, Q3); báo kèm kết cục khi chưa áp mốc giả (S33). Ca biên cho 28 đột biến đổi hành vi còn sống của lượt 5; sửa ba test tự so với chính nó. Trên bộ ca tất định, 104 bản ghi giống bản trước sửa ở mọi trường (`runs/tat-dinh-010/so-truong-truoc-luot5.json`).
- Sau kiểm lại lượt 5 (mục C8): `khong_moc_gia` giữ điều kiện riêng E5/E3 (S34); gộp hòa theo khóa ghi ra, như bộ đánh giá đọc (S35; RR không đổi); luật chọn khối theo thế giới (S36); MRR theo bội số và lấy mẫu ô (S37); cache cổng theo ca (S38); giá trị `tham_so_E4` (S39); ca cho 9 đột biến sống sót của phiên kiểm lại (S40); ghi rõ hai cách dựng G_N (S41); pha 2 lưu đủ độ đo của `src/p3/danh_gia` (S42). Trên bộ ca tất định, 104 bản ghi chỉ khác bản trước lượt 5 ở trường mới `diagnostics.gop_khoa_ghi_ra` (`runs/tat-dinh-011/so-truong-truoc-luot5.json`).
- Runner sinh đúng số cấu hình theo `ma-tran-thu.json` sau Đ16; hai pha tách được; hash pha 1 ổn định.

**Câu hỏi của SPEC trả lời tới đâu:**
- A1 (code đúng đặc tả?): đúng trên mọi ca giả có đáp án; kết luận chỉ trong phạm vi fixture.
- A2 (test có sức bắt lỗi?): 58/58 đột biến bị bắt. Ba lượt phản biện vẫn tìm được lỗi mà bộ test và đột biến lúc đó không bắt (lượt 1: ba lỗi với 235 phép, 21 đột biến; lượt 2: tám điểm với 246 phép, 27 đột biến; lượt 3: hai lỗi CHẶN, một làm đổi thứ hạng, với 254 phép, 35 đột biến; lượt 4: hai lỗi CHẶN, sai số làm tròn đổi hòa và giá trị vô hạn dừng pha 1, với 266 phép, 44 đột biến; lượt 5: bốn điểm CHẶN bắt đầu T-045 ở giao diện bộ đánh giá và 28 đột biến đổi hành vi sống sót, với 289 phép, 58 đột biến): phép kiểm và đột biến chỉ mạnh tới đâu đáp án và câu hỏi đặt ra tới đó. Chỗ không có fixture thì đột biến tương ứng không thể bị bắt (biên p = α, mục 9).
- A3 (nhãn có lọt?): kiểm tĩnh qua; fixture 74 qua; chặn rò ở mức giá trị (CĐ12) có test và đột biến D06–D08.
- A4 (tất định?): PASS trên ca giả. Trên dữ liệu thật: T-045 T1.
- A5 (đặc tả có chỗ sai hay mơ hồ?): không chỗ sai; 20 chỗ đặc tả không nói, người làm đã chọn cách hiểu (`dinh-chinh-cai-dat.md` Phần II, mục A); Minh duyệt giữ cả 20 ngày 29/10/2026.

**Không trả lời:** hiệu quả của M1 (RQ3b, RQ3c, RQ3d); hành vi, thời gian, RAM trên dữ liệu thật (T-045).

**Trạng thái:** Phần II mục A đã được Minh duyệt (29/10/2026); đã sửa sau phản biện lượt 1–4 (mục C2–C4, C6), lượt 5 (mục C7) và kiểm lại lượt 5 (mục C8); E1-CP và bước 5 đã quyết và sửa (mục C5); chờ kiểm lại gói C8.

## 2. Đầu vào, môi trường, kiểm hash

- Kiểm hash T-043: PASS 69/69 file, 10/10 hash đóng băng, ở đầu giai đoạn 2 (`runs/kiem-hash-t043-001/stdout.txt`), cuối giai đoạn 2 (`runs/kiem-hash-t043-002/stdout.txt`) và sau gói sửa (`runs/kiem-hash-t043-003/stdout.txt`), qua `scripts/kiem_hash_t043.py` vì bản clone thiếu thư mục rỗng `runs/khe-open-001`. Chạy trực tiếp `tao_manifest.py --kiem` FAIL chỉ vì `luot_thieu` (`runs/kiem-hash-t043-001/truc-tiep.txt`).
- Môi trường: Python 3.12.3 trên cloud tới lượt 2; từ lượt 3, Python 3.12.10 trên Windows (`D:/RCA-ext/envs/py312-pin`, cộng `PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages`; thư mục này nạp drain3 và cả numpy, scipy, pandas cùng phiên bản ghim 1.26.4, 1.14.1, 2.2.3, đã kiểm `__version__` và đường dẫn; networkx 2.5 lấy từ py312-pin; không thêm `T-014-main` vì thư mục đó có networkx 2.8.8 và che bản 2.5). `requirements-m1.txt`: numpy 1.26.4, pandas 2.2.3, scipy 1.14.1, networkx 2.5, pytest 8.3.4, drain3 0.9.11, pyarrow 18.1.0; gói gián tiếp ở `freeze-m1.txt`.
- Nguồn gốc pyarrow trên cloud (S15): bản cài từ wheel `pyarrow-18.1.0-cp312-cp312-manylinux_2_28_x86_64.whl`, sha256 `c52f81aa6f6575058d8e2c782bf79d4f9fdc89887f16825ec3a66607a5dd8e30`, tải vào thư mục scratchpad của phiên cloud. `freeze-m1.txt` nay ghi `pyarrow==18.1.0` để dựng được trên máy khác. Chưa chạy lại lệnh dựng môi trường sau sửa (cần mạng).
- Hàm thư viện dùng ngoài phần tự viết:
  - networkx 2.5: `is_directed_acyclic_graph`, `all_simple_paths`, chỉ trong C-d3 (như mã PetShop; networkx 2.5 cũng trả bộ sinh rỗng khi nguồn trùng đích, như 2.8.8 của PetShop). PageRank, SCC (Tarjan), phủ đỉnh nhỏ nhất tự viết.
  - scipy 1.14.1: `mannwhitneyu(method='asymptotic', use_continuity=True)` cho cổng xấp xỉ khi n_N + n_A > 100; cổng chính xác là DP chép từ B1.8.
  - drain3 0.9.11: `Drain` (học mẫu, `fast_match`, cây tiền tố).
- Cảnh báo duy nhất khi chạy test: DeprecationWarning của `networkx/release.py` lúc import trên Python 3.12; không ảnh hưởng tính toán.

## 3. Kết quả phép kiểm

Nguồn: `runs/test-xanh-010/ket-qua.json` (từng phép), tổng hợp ở `bang-phep-kiem.json` (`scripts/tao_bang_phep_kiem.py`). Các lượt trước: `runs/test-xanh-001` (235/235), `runs/test-xanh-002` (246/246), `runs/test-xanh-003` (254/254), `runs/test-xanh-004` (263/263), `runs/test-xanh-005` (266/266), `runs/test-xanh-006` (289/289, trước bản cuối), `runs/test-xanh-007` (289/289), `runs/test-xanh-008` (342/342, lượt 5 trước bản cuối), `runs/test-xanh-009` (342/342, lượt 5).

| Nhóm | Số phép | Qua | Con trỏ |
|---|---|---|---|
| Fixture T-043 trong phạm vi (82 fixture trừ D13) | 97 | 97 | `bang-phep-kiem.json#/theo_nhom/T043` |
| Fixture bổ sung B1–B8 | 8 | 8 | `#/theo_nhom/B` |
| U1–U6 (Đ15), H1–H6 (Đ19) | 12 | 12 | `#/theo_nhom/U`, `#/theo_nhom/H` |
| H1–H3 chạy qua chuỗi (trạng thái quan sát của nguồn metric) | 3 | 3 | `#/theo_nhom/H_qua_chuoi` |
| Đáp án tự lập, thành phần (125 mục) | 190 | 190 | `#/theo_nhom/tu_lap_thanh_phan` |
| Đáp án tự lập, đối chứng (15 mục) | 15 | 15 | `#/theo_nhom/tu_lap_doi_chung` |
| Đáp án từ văn bản đặc tả (5 mục) | 5 | 5 | `#/theo_nhom/tu_lap_van_ban` |
| Phép bổ sung của người làm (đầu-cuối từ span, runner, adapter, kiểm tĩnh, cache…) | 36 | 36 | `#/theo_nhom/bo_sung_nguoi_lam` |
| **Tổng** | **366** | **366** | `#/tong` |

- Đáp án tự lập ở `fixture/dap-an-thanh-phan.json`, `dap-an-doi-chung.json`, `dap-an-van-ban.json` mang dấu "đáp án của người làm T-044, chưa qua phản biện". Codex cần kiểm từng mục (Q-212).
- `fixture/dap-an-u-h.json`: U1–U6, H1–H6 chép từ `results/T-043/dinh-chinh-phien10.md` dòng 42–47 và 144–149; cột `van_ban` tách nguyên văn, cột `may_doc` chép tay; chờ người phản biện đối chiếu.
- Sai số: theo CĐ16 (phân số ≤ 1e−12; số đã làm tròn trong fixture: nửa đơn vị chữ số cuối; thứ hạng, trạng thái, tập: khớp tuyệt đối). Test không so với `kiem_fixture.py`.

## 4. Ánh xạ fixture → test → module

| Khối SPEC bước 4 | Fixture | Test | Module |
|---|---|---|---|
| 1. Hợp đồng, trường cấm | 74 | `test_k01_hop_dong.py` | `m1.hop_dong` |
| 2. Cửa sổ, quan sát, ba thế giới | 21–24, 28–30, 82; H1–H6 | `test_k02_quan_sat.py` | `m1.quan_sat`, `m1.e4`, `m1.xep_hang`, `m1_danh_gia.the_gioi`, `m1.chuoi` (H4–H6) |
| 3. Tiền xử lý span | 6, 7, 44, 72 | `test_k03_span.py` | `m1.span` |
| 4. E4, cổng, cache, nhánh z | 25–27, 41, 75, 76, 81; B1–B8 phần liên quan | `test_k04_e4.py`, `test_k02_quan_sat.py` (B1, B8) | `m1.e4` |
| 5. Kênh, severity, lớp | 77–79; U1–U6 | `test_k05_kenh.py` | `m1.kenh`, `m1.e3` |
| 6. E1-U, E1-CP; E2-C, E2-VC | 2–5; 9–13 | `test_k06_e1_e2.py` | `m1.span`, `m1.e2` |
| 7. E3, nhánh tắt; E3b | 55, 73 | `test_k07_e3.py` | `m1.e3`, `m1.kenh` |
| 8. E5, E6a, E6b, E7, E9, cạnh tĩnh | 8, 57, 58, 71, 80 (phía phương pháp); 14–16, 69; 70; B2–B5 | `test_k08_e5_e6_e7_e9.py` | `m1.e5`, `m1.e9`, `m1.xep_hang`, `m1.e7`, `m1_danh_gia.e7` |
| 9. `verdict`; chuỗi S1–S7 | 31, 42; 1 | `test_k09_chuoi.py` | `m1.chuoi`, `m1.xep_hang`, `m1.e7` |
| 10. Đối chứng | 17–20, B7; 33, 68; 32, 43, 56; B6 | `test_k10_doi_chung.py` | `m1.doi_chung`, `m1_danh_gia.moc_gia`, `m1.chuoi` |
| 11. Bộ đánh giá | 34–40, 51–54, 60; 45–47, 49, 50; 48; 80 (phía bộ đánh giá); TS1–TS5, WD1 | `test_k11_danh_gia.py` | `m1_danh_gia.luat_c`, `chon_khoi`, `boi_canh`, `m5`, `uv6`, `dau_vet`, `rr`, `pha2` |
| Runner, hai pha | RUN1 | `test_runner.py` | `m1.runner`, `m1_danh_gia.pha2` |
| Adapter | dữ liệu tổng hợp | `test_adapter.py` | `m1.adapter` |
| Kiểm tĩnh | — | `test_tinh.py` | toàn `src/m1` |

Đối chiếu: 74 fixture trong phạm vi đều có phép kiểm, không thiếu fixture nào (`bang-phep-kiem.json#/T043/thieu` rỗng). Phân khối khớp danh sách của SPEC bước 4; fixture 80 có hai phần ở khối 8 và khối 11.

## 5. Code

- `src/m1/`: `kieu.py` (kênh), `hop_dong.py`, `quan_sat.py`, `span.py`, `e4.py`, `kenh.py`, `e2.py`, `e3.py`, `e5.py`, `e7.py`, `e9.py`, `xep_hang.py`, `chuoi.py` (API 7 tham số `chay(spans, metrics, logs, inventory, aliases, t, params)`), `doi_chung.py`, `runner.py`, `adapter.py`.
- `src/m1_danh_gia/`: `rr.py`, `the_gioi.py`, `e7.py`, `moc_gia.py`, `luat_c.py`, `chon_khoi.py`, `boi_canh.py`, `m5.py`, `uv6.py`, `dau_vet.py`, `pha2.py`.
- Bản ghi theo schema của `ban_ghi.tao` (để `src/p3/danh_gia` đọc được) cộng các trường của `hop-dong.json#/ra/truong_them`; `extra` thêm thứ hạng P, đối chứng C-d1, C-d2, C-d3, T4c, kênh có cờ kèm F_I (gộp và theo từng thế giới), G_N và chi tiết đơn vị; `coverage` có trạng thái quan sát của trace, log và từng nguồn metric (`dinh-chinh-cai-dat.md` Phần II mục B).
- Không sửa `src/p3`. `src/m1` chỉ đọc `p3.ban_ghi.CAM`, `p3.nezha.FORBIDDEN_LABEL_KEYS`, và gọi `p3.selector`, `p3.nezha` trong adapter.

## 6. Runner và hai pha

- `runner.ap_dinh_chinh` áp Đ16 (bỏ C-h khỏi T13) lên bản sao trong bộ nhớ của `ma-tran-thu.json`; file đóng băng giữ nguyên. Đ3, Đ7 chỉ đổi chữ, ghi riêng, không áp.

| Đính chính | Nguồn | Chỗ áp | Đổi gì |
|---|---|---|---|
| Đ16 | `results/T-043/dinh-chinh-phien10.md` dòng 70 | `#/buoc/<T13>/so_sanh`, `so_cau_hinh` | bỏ C-h; "+ 8 đối chứng" thành "+ 7 đối chứng" |

- Số cấu hình (RUN1): T1 1, T4 9, T4b 1, K 16, K-b 2, T6 1, T9 1, T10 0, T11 1, T12 1, KB 4, T13 13. K + K-b + KB = 22 cấu hình × 52 ca = 1.144 lượt chấm ≤ 1.300 (`ma-tran-thu.json#/ngan_sach/K_Kb_KB`). Mỗi cấu hình có mã nội dung, nên cấu hình trùng giữa các bước (ví dụ R0 ở T1, T4, K) chạy một lần là đủ.
- Pha 1 (`runner.pha1`): không đọc nhãn; chặn mã mờ, case_dir, tên thư mục ca và đường dẫn tệp xuất hiện trong `params`, `aliases`, `inventory` (CĐ12); ghi `ban-ghi.jsonl` (JSON chuẩn hóa, không NaN) và sha256. Hai lần chạy cho cùng hash (`test_runner.py::test_hai_pha_hash_on_dinh`).
- Pha 2 (`m1_danh_gia.pha2.cham`): kiểm hash rồi mới ghép nhãn; hash sai thì từ chối. Ca WORLD_DEPENDENT có `nguyen_nhan_WD` (cặp đổi thứ tự với root theo từng thế giới). `ket_cuc_cap` và `dem_moc_gia` nhận bội số ô (SPEC T-045 dòng 88–89).
- Adapter: kiểm trên dữ liệu tổng hợp RE2-TT (parquet) và Nezha-OB (CSV phút) đúng schema của `src/p3`, sinh trong thư mục tạm; tệp sai hash bị từ chối.

## 7. Tất định

- Cách làm: `tests/conftest.py` xáo mọi danh sách đầu vào mà thứ tự không mang nghĩa, ở mọi tầng gọi (`M1_XAO`); `scripts/tat_dinh.py` băm 104 bản ghi (trace S1–S7 và ca metric, 13 cấu hình gồm E1-CP, E3, E6b, E9, T12, nhánh z, cách đọc A).
- Lượt đầu (`runs/tat-dinh-000-truoc-sua/`): 6 phép trượt khi xáo, do `e2.gan_canh` và `e5.phan_loai` giữ thứ tự đầu vào trong đầu ra. Đã chuẩn hóa thứ tự.
- Lượt `runs/tat-dinh-002/tong-hop.json` (trước gói sửa): 0 sha256 lệch; 235 phép.
- Lượt cuối `runs/tat-dinh-003/tong-hop.json`: 0 sha256 lệch trong 12 biến thể; 246 phép qua và giống hệt ở cả 12 biến thể. Cả 104 bản ghi khác lượt 002 vì gói sửa thêm trường (`coverage` của nguồn metric, `extra.kenh_co_the_gioi`). Bỏ hai trường này thì 104 bản ghi giống hệt bản trước gói sửa (`runs/tat-dinh-003/tong-hop.json#/so_voi_truoc_sua`).
- Lượt cuối `runs/tat-dinh-004/tong-hop.json` (sau gói sửa lượt 2): 0 sha256 lệch; 254 phép giống hệt ở 12 biến thể. Bỏ các trường mới (`coverage` của nguồn metric, `extra.kenh_co_the_gioi`, `extra.thong_ke_log`) thì 104 bản ghi giống hệt bản ở 9206eaa6 (`#/so_voi_truoc_sua`).
- Lượt `runs/tat-dinh-005/tong-hop.json` (sau gói sửa lượt 3, Windows local): 0 sha256 lệch; 263 phép giống hệt ở 12 biến thể. Bỏ các trường mã mới (`ma` của `extra.kenh_co`; `ma`, `don_vi`, `giai_thich_ma` của `inherited_by`) và so `kenh_co`, `inherited_by` theo nội dung thì 104 bản ghi giống bản ở 253dbe46 (`#/so_voi_truoc_sua`). So theo thứ tự thì `S3|E3`, `S3|E6b` lệch, chỉ do hai danh sách sắp theo mã kênh mà mã nay có đơn vị (người làm kiểm: giống hệt sau khi sắp theo nội dung); đầu ra của lần so đó bị ghi đè.
- Lượt cuối `runs/tat-dinh-006/tong-hop.json` (sau sửa E1-CP và bước 5): 0 sha256 lệch; 266 phép giống hệt ở 12 biến thể; 104 bản ghi giống bản ở 253dbe46 sau khi bỏ trường mới. Bộ ca tất định không có cha nào mà quy tắc E1-CP mới đổi kết quả, nên sửa S18 không đổi bản ghi nào ở đây; hành vi mới chỉ được kiểm bằng CP2.
- Lượt cuối `runs/tat-dinh-008/tong-hop.json` (sau gói sửa lượt 4): 0 sha256 lệch; 289 phép giống hệt ở 12 biến thể. So với 253dbe46 sau khi bỏ trường mới: 16 bản ghi lệch, và `so-truong-253dbe46.json` (`scripts/so_truong_ban_ghi.py`) cho thấy mọi chỗ lệch chỉ ở m của T4c, chữ số cuối, do đổi sang log1p của x chính xác (S21). Khóa xếp hạng, thứ tự, kênh, verdict không đổi trên bộ ca này.
- Lượt cuối `runs/tat-dinh-010/tong-hop.json` (sau gói sửa lượt 5): 0 sha256 lệch; 342 phép giống hệt ở 12 biến thể; hash seed ghi trong đầu ra khớp 0, 1, 2. So với cây trước sửa (bản chụp cây làm việc lúc bắt đầu lượt 5, chưa commit; `CAY_CU`), so đủ mọi trường (`so_truong_ban_ghi.py --day-du`): 0/104 bản ghi lệch (`so-truong-truoc-luot5.json`); vậy gói sửa không đổi bản ghi nào của bộ ca này, chỉ đổi kết quả ở các ca phản ví dụ. Phụ thuộc hash seed ở mức thành phần kiểm thêm bằng TD2 (đường E5 qua 8 seed) và TD3 (đầu ra luật chọn khối, luật C qua 4 seed và hai thứ tự khóa). Lượt `runs/tat-dinh-009` (lần 1 của lượt 5) cho cùng kết quả.
- Lượt cuối `runs/tat-dinh-011/tong-hop.json` (sau gói sửa C8): 0 sha256 lệch; 366 phép giống hệt ở 12 biến thể; hash seed khớp. So đủ mọi trường với cây trước lượt 5: 104 bản ghi khác đúng một đường dẫn, trường mới `/diagnostics/gop_khoa_ghi_ra` (`so-truong-truoc-luot5.json#/duong_dan_lech`); bộ ca này không có hai khóa chính xác khác nhau mà ghi ra cùng số thực.

## 8. Đột biến

Nguồn: `runs/dot-bien-012/tong-hop.json`. Mỗi đột biến thay đúng một chuỗi trong bản sao tạm của `src/`; lượt đối chứng không đột biến xanh 366/366. Số phép trượt dưới đây theo lượt 012 (Windows local). D80 đổi thành đột biến ngược theo S35 (gộp theo khóa chính xác); D111–D119 bỏ từng sửa của C8; D120–D128 là 9 đột biến sống sót của phiên kiểm lại lượt 5 (tên gốc trong mô tả). Lượt 011 (lượt 5): 110/110. D09 đổi chỗ theo dòng mới của S32 (cùng ý). D59–D78 bỏ từng chặn của gói sửa lượt 5; D79–D110 là các đột biến đổi hành vi sống sót mà phiên phản biện lượt 5 tìm ra (tên gốc trong mô tả). Lượt `runs/dot-bien-010` (lần 1 của lượt 5): 108/110, D103 và D107 sống sót vì ca E4B chỉ giả lập p của đơn vị đếm và ca E9X chỉ gọi `e9.phu_quyet` trực tiếp; đã thêm hai phép vào E4B, E9X. Lượt 012: 93/128 đột biến chỉ bị đúng một phép bắt: sức bắt lỗi theo từng điểm, chưa phủ đều các biên. D03, D13 đổi chỗ theo dòng mới của lượt 4 (cùng ý). D30 đổi chỗ theo hàm dùng chung của bước 5 và bước 8 (S19). D26, D27 đổi chỗ đột biến theo code mới của lượt 2; D11 đổi chỗ theo dòng E7 mới của lượt 3 (cùng ý).

| Mã | Đột biến | Tệp | Phép trượt |
|---|---|---|---|
| D01 | E5: đảo quy tắc lan ngược và lan xuôi | `m1/e5.py` | 29 |
| D02 | E1-U: bỏ cắt con về cha | `m1/span.py` | 2 |
| D03 | Khóa K: đổi chỗ số kênh và tổng điểm | `m1/xep_hang.py` | 12 |
| D04 | Bộ kiểm trường cấm không duyệt list, tuple | `m1/hop_dong.py` | 3 |
| D05 | Luật C: δ = 0,02 | `m1_danh_gia/luat_c.py` | 5 |
| D06 | Pha 1 đưa mã mờ vào params | `m1/runner.py` | 6 |
| D07 | `src/m1` import bộ đánh giá | `m1/chuoi.py` | 1 |
| D08 | Pha 1 trỏ tới file nhãn | `m1/runner.py` | 1 |
| D09 | E1-CP bỏ dung sai τ | `m1/span.py` | 3 |
| D10 | E5: cách đọc nhóm vòng mặc định A | `m1/e5.py` | 3 |
| D11 | E7 cách 1: "mọi kênh" thành "một kênh" | `m1/e7.py` | 4 |
| D12 | E9: bỏ τ, lấy cả biên 2 ô | `m1/e9.py` | 1 |
| D13 | Đơn vị đếm: λ dùng T đảo | `m1/e4.py` | 7 |
| D14 | E6b: hệ số tắt dần 0,80 | `m1/xep_hang.py` | 2 |
| D15 | E4: n = 100 sang cổng xấp xỉ | `m1/e4.py` | 1 |
| D16 | Đổi S_lo và S_hi | `m1/quan_sat.py` | 1 |
| D17 | E3 cách khớp (a) dùng ngưỡng | `m1/e3.py` | 2 |
| D18 | Bỏ tầng kế thừa | `m1/xep_hang.py` | 8 |
| D19 | E5 bỏ thứ tự chuẩn (chạy với `M1_XAO=1`) | `m1/e5.py` | 2 |
| D20 | Cột metric không khai nguồn vẫn được chấm | `m1/chuoi.py` | 1 |
| D21 | Chuỗi thiếu `tham_so_E5` dùng cách đọc A | `m1/chuoi.py` | 1 |
| D22 | Luật C: P, M đếm mỗi ô một lần dù ô lấy k lần | `m1_danh_gia/luat_c.py` | 3 |
| D23 | Cờ M5 nhánh tắt bỏ bội số | `m1_danh_gia/pha2.py` | 1 |
| D24 | UV-6 bỏ bội số | `m1_danh_gia/uv6.py` | 4 |
| D25 | Mẫu số mốc giả không theo bội số | `m1_danh_gia/pha2.py` | 1 |
| D26 | Chuỗi không xuất trạng thái quan sát của nguồn metric | `m1/chuoi.py` | 4 |
| D27 | WORLD_DEPENDENT lấy mọi thực thể đứng trước root | `m1_danh_gia/the_gioi.py` | 4 |
| D28 | Pha 2: MRR đổi sang số thực | `m1_danh_gia/pha2.py` | 1 |
| D29 | RR_o: ô bội số 0 vẫn chia | `m1_danh_gia/rr.py` | 2 |
| D30 | Bước 8: đọc kết cục tại P của cặp phụ thuộc quan sát | `m1_danh_gia/chon_khoi.py` | 3 |
| D31 | T12: thiếu khóa con của `canh_tinh` không ra UNSUPPORTED | `m1/chuoi.py` | 1 |
| D32 | Bản ghi bỏ thống kê severity và cặp Drain | `m1/chuoi.py` | 1 |
| D33 | WORLD_DEPENDENT coi hòa là đứng sau | `m1_danh_gia/the_gioi.py` | 2 |
| D34 | WORLD_DEPENDENT chỉ xét thực thể có ở cả hai thế giới | `m1_danh_gia/the_gioi.py` | 1 |
| D35 | Không xuất trạng thái nguồn metric khi không có hàng | `m1/chuoi.py` | 1 |
| D36 | Mã kênh bỏ đơn vị (mã cũ thực thể\ | `m1/kieu.py` | 10 |
| D37 | E5 không báo lỗi khi hai kênh trùng mã | `m1/e5.py` | 2 |
| D38 | E7 tra giải thích theo tên kênh | `m1/e7.py` | 2 |
| D39 | WORLD_DEPENDENT: cặp luôn lấy kênh mạnh nhất | `m1_danh_gia/the_gioi.py` | 1 |
| D40 | WORLD_DEPENDENT: không ghi phần khóa phân định | `m1_danh_gia/the_gioi.py` | 1 |
| D41 | UV-6 báo kèm bỏ bội số | `m1_danh_gia/uv6.py` | 1 |
| D42 | E1-CP: kiểm vùng chồng lấn chỉ với con còn lại | `m1/span.py` | 1 |
| D43 | E1-CP: biên đóng | `m1/span.py` | 1 |
| D44 | Bước 5: đọc kết cục tại P của cặp phụ thuộc quan sát | `m1_danh_gia/chon_khoi.py` | 2 |
| D45 | E4 phân vị: tỷ lệ vượt của A bằng số thực | `m1/e4.py` | 1 |
| D46 | E4 đếm: λ bằng số thực | `m1/e4.py` | 4 |
| D47 | Khóa: Σs cộng bằng số thực | `m1/xep_hang.py` | 1 |
| D48 | Nhánh z giữ cờ và điểm không hữu hạn | `m1/chuoi.py` | 1 |
| D49 | T4c: log trên số thực | `m1/e4.py` | 1 |
| D50 | Không chặn bản ghi có giá trị không hữu hạn | `m1/chuoi.py` | 1 |
| D51 | Không kiểm giá trị của `bat_tat` | `m1/chuoi.py` | 1 |
| D52 | Bỏ π gốc của E6b | `m1/chuoi.py` | 1 |
| D53 | Không kiểm số mốc của nguồn metric | `m1/chuoi.py` | 1 |
| D54 | Ca thiếu trong map bội số tự lấy 1 | `m1_danh_gia/rr.py` | 2 |
| D55 | Pha 2 không kiểm đủ tích cấu hình × ca | `m1_danh_gia/pha2.py` | 1 |
| D56 | Pha 2 không kiểm số dòng thật | `m1_danh_gia/pha2.py` | 1 |
| D57 | C-a0, C-a1 vẫn dựng vùng E7 | `m1/chuoi.py` | 2 |
| D58 | Luật chọn khối không kiểm đủ cặp | `m1_danh_gia/chon_khoi.py` | 1 |
| D59 | Luật chọn khối: không kiểm đủ 2^n cấu hình (G1) | `m1_danh_gia/chon_khoi.py` | 1 |
| D60 | Luật chọn khối: không kiểm it_ca, do_thi (G1) | `m1_danh_gia/chon_khoi.py` | 3 |
| D61 | Bước 8: thiếu cặp thì bỏ qua (G1) | `m1_danh_gia/chon_khoi.py` | 1 |
| D62 | Luật C: nhận số thực (G2) | `m1_danh_gia/luat_c.py` | 1 |
| D63 | Bội số: nhận chuỗi, số không nguyên (G2) | `m1_danh_gia/rr.py` | 1 |
| D64 | UV-6: nhận Hit@1 số thực (G2) | `m1_danh_gia/uv6.py` | 1 |
| D65 | Luật C: không kiểm E_X thuộc tập ô (G3) | `m1_danh_gia/luat_c.py` | 3 |
| D66 | Luật C: không kiểm mã ca trùng (G3) | `m1_danh_gia/luat_c.py` | 1 |
| D67 | Pha 2: không kiểm nhãn thành phần của cặp (G4) | `m1_danh_gia/pha2.py` | 3 |
| D68 | Bước 8: thành phần không ít ca đọc như ít ca (G5, Q1) | `m1_danh_gia/chon_khoi.py` | 1 |
| D69 | Mã nội dung không gồm doi_chung (G6) | `m1/runner.py` | 1 |
| D70 | Chuỗi: không kiểm trùng mã đơn vị (S27) | `m1/chuoi.py` | 1 |
| D71 | Verdict đếm cả phép chấm ngoài U (S28, Q2) | `m1/chuoi.py` | 1 |
| D72 | E4: ngưỡng trên có thể tràn (S29) | `m1/e4.py` | 1 |
| D73 | STOPPED cả ở hướng không chấm (S30, Q5) | `m1/e4.py` | 1 |
| D74 | Chuỗi: không kiểm kiểu nhanh_z (S31) | `m1/chuoi.py` | 1 |
| D75 | Chuỗi: không kiểm khóa tham_so_E4 (S31) | `m1/chuoi.py` | 1 |
| D76 | Runner: params_ca được mang doi_chung (S31) | `m1/runner.py` | 1 |
| D77 | E1-CP: nhận con bắt đầu trong khoảng của nút đang xét (S32, Q3) | `m1/span.py` | 6 |
| D78 | Pha 2: không báo kèm kết cục khi chưa áp mốc giả (S33) | `m1_danh_gia/pha2.py` | 3 |
| D79 | E6b: không dùng K_I, K_raw phá hòa π (N01) | `m1/xep_hang.py` | 1 |
| D80 | Gộp hòa theo khóa chính xác thay khóa ghi ra (ngược K07; S35) | `m1/xep_hang.py` | 1 |
| D81 | E6b: không làm tròn π 12 chữ số (N02) | `m1/xep_hang.py` | 1 |
| D82 | E1-CP: happensBefore không chặt (N22) | `m1/span.py` | 1 |
| D83 | E1-CP: hòa LFC chọn con bắt đầu sớm (N24) | `m1/span.py` | 1 |
| D84 | Luật C: GIÚP khi ΔMRR = δ (N30) | `m1_danh_gia/luat_c.py` | 1 |
| D85 | Luật C: | `m1_danh_gia/luat_c.py` | 1 |
| D86 | Luật C: GIÚP khi P = M (N33) | `m1_danh_gia/luat_c.py` | 1 |
| D87 | Luật C: TRÁI CHIỀU tại biên (N34) | `m1_danh_gia/luat_c.py` | 2 |
| D88 | Luật C: P, M đếm cả ô ngoài E_X (N36) | `m1_danh_gia/luat_c.py` | 1 |
| D89 | Luật C: KHÔNG ĐỦ CA trước HẠI gộp (N37) | `m1_danh_gia/luat_c.py` | 2 |
| D90 | Mốc giả: HẠI khi tăng đúng 0,1 (N39) | `m1_danh_gia/moc_gia.py` | 1 |
| D91 | Mốc giả: biên không phân xử được (N40) | `m1_danh_gia/moc_gia.py` | 1 |
| D92 | Chọn khối: hòa số thành phần chọn MRR thấp (N42) | `m1_danh_gia/chon_khoi.py` | 1 |
| D93 | Chọn khối: thứ tự theo tên (N43) | `m1_danh_gia/chon_khoi.py` | 1 |
| D94 | Bước 5: không cần c thêm x thuộc tập cố định (N44) | `m1_danh_gia/chon_khoi.py` | 1 |
| D95 | Bước 8: tắt với KHÔNG TÁC DỤNG là xung đột (N47) | `m1_danh_gia/chon_khoi.py` | 1 |
| D96 | Chọn khối: cờ TRÁI CHIỀU gắn cho a (N48) | `m1_danh_gia/chon_khoi.py` | 1 |
| D97 | Lượt một: bỏ loại vì (R0, c) HẠI (N49) | `m1_danh_gia/chon_khoi.py` | 1 |
| D98 | Bước 5: áp cho mọi thành phần (K03) | `m1_danh_gia/chon_khoi.py` | 1 |
| D99 | Pha 2: không kiểm bản ghi trùng (N51) | `m1_danh_gia/pha2.py` | 1 |
| D100 | Pha 2: không kiểm số ca với metadata (N52) | `m1_danh_gia/pha2.py` | 1 |
| D101 | E4: khóa cache không có hướng (N14) | `m1/e4.py` | 1 |
| D102 | NEW_OP: biên count_min (N12) | `m1/e4.py` | 1 |
| D103 | PII-01 đơn vị phân vị: p ≤ α (N07) | `m1/e4.py` | 1 |
| D104 | PII-01 đơn vị đếm: p ≤ α (N08) | `m1/e4.py` | 1 |
| D105 | UV-6: ca được sửa cần Hit@1 tắt = 0 (N55) | `m1_danh_gia/uv6.py` | 1 |
| D106 | E5: lan xuôi chỉ do bên gọi lớp lan ngược/không lan (N19) | `m1/e5.py` | 1 |
| D107 | E9: chỉ xét bên giải thích đầu (N18) | `m1/e5.py` | 1 |
| D108 | MRR: tổng bội số 0 trả 0 (K01) | `m1_danh_gia/rr.py` | 1 |
| D109 | E5: đường phụ thuộc hash seed (K09) | `m1/e5.py` | 1 |
| D110 | E3: log trùng mốc theo thứ tự vào (K17) | `m1/e3.py` | 1 |
| D111 | khong_moc_gia bỏ điều kiện riêng E5, E3 (S34; lỗi của lượt 5) | `m1_danh_gia/pha2.py` | 1 |
| D112 | Không đếm lần gộp khóa ghi ra (S35) | `m1/xep_hang.py` | 1 |
| D113 | Luật chọn khối ở S_lo, S_hi vẫn đọc kết cục tại P (S36) | `m1_danh_gia/chon_khoi.py` | 1 |
| D114 | MRR gộp của cấu hình bỏ bội số (S37) | `m1_danh_gia/pha2.py` | 1 |
| D115 | Lấy mẫu ô gộp hai dataset (S37) | `m1_danh_gia/rr.py` | 1 |
| D116 | Lấy mẫu ô theo thứ tự đầu vào (S37) | `m1_danh_gia/rr.py` | 1 |
| D117 | Pha 1 không làm mới cache theo ca (S38) | `m1/runner.py` | 1 |
| D118 | Chuỗi: không kiểm khoảng giá trị tham_so_E4 (S39) | `m1/chuoi.py` | 1 |
| D119 | Pha 2 không lưu đủ độ đo (S42) | `m1_danh_gia/pha2.py` | 1 |
| D120 | Mốc giả giữ cặp có bản ghi lỗi trong mẫu số (X02; PII-13) | `m1_danh_gia/pha2.py` | 1 |
| D121 | T4c: phần K_I của m không theo F_I (X04) | `m1/chuoi.py` | 1 |
| D122 | M5 ở S_lo, S_hi dùng khối của P (X05) | `m1_danh_gia/pha2.py` | 1 |
| D123 | E2-VC lấy cạnh điểm thấp nhất (X08) | `m1/chuoi.py` | 1 |
| D124 | WORLD_DEPENDENT theo hạng kỳ vọng (X10) | `m1_danh_gia/the_gioi.py` | 1 |
| D125 | Đích C-d3 lấy span phía N (X13) | `m1/chuoi.py` | 1 |
| D126 | G_N nhận cạnh có span cha thuộc A (X14) | `m1/chuoi.py` | 1 |
| D127 | Ô E9 5 giây (X16) | `m1/chuoi.py` | 1 |
| D128 | E9: cạnh E2 chỉ xét một chiều (X26) | `m1/e5.py` | 1 |

- Gồm đủ sáu ví dụ của SPEC bước 7 (D01, D02, D03, D04, D05; rò nhãn D06–D08).
- Lượt `runs/dot-bien-001` (20 đột biến) có 2 đột biến sống sót: D02 vì fixture 4, 5 chỉ gọi `cat_con` trực tiếp, không đi qua `chuan_bi`; D10 vì test nhóm vòng luôn truyền cách đọc. Đã thêm test, không thêm đáp án.

## 9. Tự diễn giải, giới hạn, phần chưa kiểm

- Tự diễn giải đã duyệt: Phần I của `dinh-chinh-cai-dat.md` (CĐ1–CĐ16).
- Tự diễn giải lộ ra khi cài: Phần II mục A (PII-01…PII-20), Minh duyệt giữ cả 20 ngày 29/10/2026. Quy ước biểu diễn: mục B. Sửa trong phiên: mục C. Sửa sau phản biện lượt 1: mục C2. Sửa sau lượt 2: mục C3. Sửa sau lượt 3: mục C4. Hai OPEN Minh quyết: mục C5. Sửa sau lượt 4: mục C6. Sửa sau lượt 5: mục C7. Sửa sau kiểm lại lượt 5: mục C8.
- Chưa kiểm (Phần II mục D):
  - biên p = α không có fixture; lượt 5 thêm phép giả lập p = α cho cả đơn vị phân vị và đơn vị đếm (E4B; D103, D104 bị bắt) (PII-01);
  - khoảng tin cậy bootstrap theo ô chưa nằm trong `luat_c` (báo kèm; T-045 dùng `p3.danh_gia.bootstrap`);
  - adapter chưa chạy trên dữ liệu dev; C-g, C-c chưa nối bản ghi P3 thật; cạnh tĩnh T12 chưa đọc mô hình T-038, T-039;
  - thời gian, RAM, giá trị trung gian trên ca thật (T-045 bước 0, T1);
  - quy tắc E1-CP: đã quyết (S18); lệch code CRISP chính thức (ngưỡng 1% thời lượng cha, biên đóng; 3000 ở ca phản ví dụ) là giới hạn chưa kiểm, vì chưa xác minh bản code bài báo dùng; xét lại khi dùng E1-CP ở FlashTicket;
  - bước 5: đã quyết (S19); hệ quả là thành phần ít ca có thể được giữ bật dù P cho HẠI, phải báo khi xảy ra trên dev;
  - S14 đã sửa: C-a0/C-a1 không dựng vùng; "không quan hệ" của C-a0 vẫn chỉ đúng cho thứ hạng (bản ghi còn `inherited_by` đề xuất, nhóm vòng, C-d1/C-d3 dựng từ cạnh, chỉ báo);
  - m của T4c là log1p của x chính xác: x bằng nhau cho m bằng nhau; hai x khác nhau vẫn có thể làm tròn ra cùng số thực (N2, mục C6); C-g giữ số thực;
  - C-e theo verdict tại P; ứng viên E5 giữ phần dư và tối ưu C-d3 chưa kiểm (mục C6);
  - dữ liệu dev có ca hai kênh trùng tên không: chưa biết (không đọc dữ liệu); sau S12 không còn trùng mã;
  - lượt 5: cặp giải thích WORLD_DEPENDENT có thể ghi kênh đổi không phân định phần khóa (Q6, ghi giới hạn); trùng tên cạnh E2-VC khi tên chứa `->` chỉ kiểm bằng đọc code; phép độ bền 1.000 mẫu và bước 10 luật chọn khối do T-045 tự viết, với các điều kiện ở mục D của đính chính; lượt 5b thêm `chon(..., the_gioi)`, `pha2.mrr_cau_hinh`, `rr.lay_mau_o` làm phần nền;
  - lượt 5b: hai khóa chính xác khác nhau mà ghi ra cùng số thực nay là hòa (S35), đếm ở `diagnostics.gop_khoa_ghi_ra`; tần suất trên dev chưa biết; dòng mặc định cho SPEC T-045 (bước 8, cặp phụ thuộc quan sát của thành phần không ít ca) chưa áp, vì SPEC T-045 ngoài phạm vi ghi.
- Kết luận "code đúng" chỉ trong phạm vi fixture. Đáp án tự lập chưa qua phản biện; nếu một đáp án tự lập sai thì code đang khớp cùng cách hiểu sai đó.

## 10. Các lượt chạy (giữ cả lượt hỏng)

| Lượt | Kết quả |
|---|---|
| `runs/kiem-hash-t043-001` | trực tiếp FAIL (chỉ `luot_thieu`); qua script PASS |
| `runs/test-do-001` | khung test trên package rỗng: 206/208 đỏ (bước 3) |
| `runs/tat-dinh-000-truoc-sua` | xáo hàng trước khi sửa E2, E5: 6 trượt |
| `runs/tat-dinh-001` | PASS (226 phép) |
| `runs/dot-bien-001` | 18/20 bị bắt; D02, D10 sống sót |
| `runs/dot-bien-002` | 21/21 bị bắt |
| `runs/test-xanh-001` | 235/235 qua |
| `runs/tat-dinh-002` | PASS (235 phép, 104 bản ghi) |
| `runs/kiem-hash-t043-002` | PASS |
| `runs/test-xanh-002` | sau gói sửa: 246/246 qua |
| `runs/tat-dinh-003` | sau gói sửa: PASS (246 phép, 104 bản ghi) |
| `runs/dot-bien-003` | sau gói sửa: 27/27 bị bắt |
| `runs/test-xanh-003` | sau gói sửa lượt 2: 254/254 qua |
| `runs/tat-dinh-004` | sau gói sửa lượt 2: PASS (254 phép, 104 bản ghi) |
| `runs/dot-bien-004` | sau gói sửa lượt 2: 35/35 bị bắt |
| `runs/kiem-hash-t043-004` | sau gói sửa lượt 2: PASS |
| `runs/test-xanh-004` | sau gói sửa lượt 3 (Windows local): 263/263 qua |
| `runs/tat-dinh-005` | sau gói sửa lượt 3: PASS (263 phép, 104 bản ghi) |
| `runs/dot-bien-005` | lượt hỏng: lần 1 dừng ở D11 (chuỗi cũ không còn), đầu ra bị xóa nhầm; lần 2 hỏng ở D01 do cp1252 (`GHI-CHU.txt`) |
| `runs/dot-bien-006` | sau gói sửa lượt 3: 41/41 bị bắt |
| `runs/kiem-hash-t043-005` | sau gói sửa lượt 3: PASS |
| `runs/test-xanh-005` | sau sửa E1-CP, bước 5: 266/266 qua |
| `runs/tat-dinh-006` | sau sửa E1-CP, bước 5: PASS (266 phép, 104 bản ghi; 0 bản ghi lệch so với 253dbe46 sau khi bỏ trường mới) |
| `runs/dot-bien-007` | sau sửa E1-CP, bước 5: 44/44 bị bắt |
| `runs/kiem-hash-t043-006` | sau sửa E1-CP, bước 5: PASS |
| `runs/test-xanh-006`, `tat-dinh-007`, `dot-bien-008`, `kiem-hash-t043-007` | lượt 4, trước bản cuối: 289/289; tất định PASS; 58/58; PASS. Sau lượt này người làm đổi log của T4c sang log1p và giữ khóa C-d2 dạng số thực, nên chạy lại |
| `runs/test-xanh-007` | sau gói sửa lượt 4: 289/289 qua |
| `runs/tat-dinh-008` | sau gói sửa lượt 4: PASS (289 phép, 104 bản ghi); so với 253dbe46: 16 bản ghi lệch, chỉ ở m của T4c, chữ số cuối (`so-truong-253dbe46.json`) |
| `runs/dot-bien-009` | sau gói sửa lượt 4: 58/58 bị bắt |
| `runs/kiem-hash-t043-008` | sau gói sửa lượt 4: PASS |
| `runs/test-xanh-008`, `tat-dinh-009`, `dot-bien-010`, `kiem-hash-t043-009` | lượt 5, lần 1: 342/342; tất định PASS, 0/104 bản ghi lệch mọi trường so với trước sửa; 108/110 (D103, D107 sống sót); PASS |
| `runs/test-xanh-009` | sau gói sửa lượt 5: 342/342 qua |
| `runs/tat-dinh-010` | sau gói sửa lượt 5: PASS (342 phép, 104 bản ghi); so đủ mọi trường với cây trước sửa: 0 lệch (`so-truong-truoc-luot5.json`) |
| `runs/dot-bien-011` | sau gói sửa lượt 5: 110/110 bị bắt (108/108 hành vi) |
| `runs/kiem-hash-t043-010` | sau gói sửa lượt 5: PASS |
| `runs/test-xanh-010` | sau gói sửa C8: 366/366 qua |
| `runs/tat-dinh-011` | sau gói sửa C8: PASS (366 phép, 104 bản ghi); so với cây trước lượt 5: chỉ khác trường mới `diagnostics.gop_khoa_ghi_ra` |
| `runs/dot-bien-012` | sau gói sửa C8: 128/128 bị bắt (126/126 hành vi) |
| `runs/kiem-hash-t043-011` | sau gói sửa C8: PASS |
| `runs/kiem-hash-t043-003` | sau gói sửa: PASS |
| `runs/manifest-crlf-001` | manifest trên checkout CRLF giả lập: thiếu `.gitattributes` FAIL (lượt hỏng); có `.gitattributes` PASS, 29 file `src/` khớp `git_blob` |

Lượt chạy thử đầu tiên của `scripts/tat_dinh.py` dừng vì ca metric thiếu lớp `latency-90` trong hồ sơ của bộ sinh S; đầu ra lỗi bị ghi đè, chỉ còn ghi ở LOG.

## 11. Lệnh dựng lại

```
cd results/T-044/tests && python -B -m pytest -q -p no:cacheprovider
python -B results/T-044/scripts/tat_dinh.py
python -B results/T-044/scripts/dot_bien.py <thư mục ra>
python -B results/T-044/scripts/kiem_hash_t043.py
python -B results/T-044/scripts/tao_bang_phep_kiem.py <ket-qua.json>
python -B results/T-044/scripts/tao_manifest.py --kiem
```
Trên máy cloud dùng `$HOME/m1env/bin/python`; trên Windows dùng `py -3`, hoặc môi trường ghim ở mục 2. Lượt 3 chạy cả gói bằng `bash results/T-044/scripts/chay_kiem_windows.sh` (Git Bash), rồi `python -B results/T-044/scripts/tong_hop_tat_dinh.py results/T-044/runs/tat-dinh-005`. Lượt 5: `TX_LUOT=test-xanh-009 TD_LUOT=tat-dinh-010 DB_LUOT=dot-bien-011 KH_LUOT=kiem-hash-t043-010 GOC_CU=truoc-luot5 SO_DAY_DU=1 CAY_CU=<bản chụp cây trước sửa> bash results/T-044/scripts/chay_kiem_windows.sh`, rồi `tong_hop_tat_dinh.py results/T-044/runs/tat-dinh-010 truoc-luot5`. Lượt 5b: cùng lệnh với `TX_LUOT=test-xanh-010 TD_LUOT=tat-dinh-011 DB_LUOT=dot-bien-012 KH_LUOT=kiem-hash-t043-011`. Bản chụp cây trước sửa nằm ngoài repo (thư mục tạm của phiên), không dựng lại được trên máy khác; kết quả so đã ghi trong `runs/tat-dinh-009`, `tat-dinh-010`.

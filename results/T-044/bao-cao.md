# T-044 — Cài chuỗi M1 và kiểm đặc tả (báo cáo)

- **Người làm:** Claude, phiên cloud, branch `claude/sweet-hawking-dy078d`. **Người phản biện:** Codex (lượt 1 trong chat 29/10/2026: 3 CHẶN, 1 KHÔNG CHẶN; lượt 2: 7 CHẶN, 1 KHÔNG CHẶN, rồi kiểm phản hồi; đã sửa phần không còn bất đồng, chờ kiểm lại).
- **Ngày:** 29/10/2026. **SPEC:** `tasks/T-044-cai-dat-m1/SPEC.md` (đã duyệt; sửa theo các mục Minh duyệt ngày 29/10/2026, LOG giai đoạn 2).
- **Quyền dữ liệu:** không đọc `data/`, không tải dữ liệu, không đọc bản ghi P3 có nhãn. Mọi phép kiểm dùng ca giả.

## 1. Tóm tắt

**Task đạt gì (trong phạm vi fixture):**
- Code `src/m1/` (phương pháp, đối chứng, runner, adapter) và `src/m1_danh_gia/` (bộ đánh giá) theo đặc tả v1, ba bản đính chính T-043 và Phần I của `dinh-chinh-cai-dat.md`.
- 254/254 phép kiểm qua (`bang-phep-kiem.json#/tong`). Trong đó 97/97 phép của T-043 trong phạm vi (`#/T043/qua_trong_pham_vi`); 12 phép của fixture D13 loại theo ngoại lệ đã duyệt (`#/T043/loai_tru_D13`); B1–B8, U1–U6, H1–H6 và 86 mục đáp án tự lập qua (`#/theo_nhom`).
- Không sửa đáp án nào; không có đáp án đặc tả nào lệch với code.
- Tất định: 104 bản ghi và 254 phép kiểm giống hệt qua 4 thứ tự hàng × PYTHONHASHSEED 0, 1, 2 (`runs/tat-dinh-004/tong-hop.json#/ket_luan`).
- Đột biến: 35/35 bị bắt (`runs/dot-bien-004/tong-hop.json#/so_bi_bat`), sau khi lượt đầu lộ 2 lỗ hổng test và đã vá (`runs/dot-bien-001/tong-hop.json#/song_sot`). D22–D27 thêm sau phản biện lượt 1; D28–D35 sau lượt 2.
- Sau phản biện lượt 1: đã sửa ba lỗi CHẶN (bội số ô trong luật C, M5, UV-6, mốc giả; trạng thái quan sát của nguồn metric; cặp giải thích WORLD_DEPENDENT), thu hẹp lập luận E3 trong đề xuất WHY, và cho manifest kiểm được trên checkout CRLF (giả lập trên Linux, `runs/manifest-crlf-001`; chưa chạy trên Windows thật) (`dinh-chinh-cai-dat.md` Phần II mục C2).
- Sau phản biện lượt 2: đã sửa MRR chính xác tới hết luật chọn, ô bội số 0, bước 8 với cặp phụ thuộc quan sát, kiểm khai báo bắt buộc, thống kê severity và cặp Drain trong bản ghi, giải thích WORLD_DEPENDENT khi hòa hoặc vắng, trạng thái nguồn metric rỗng (mục C3). Chưa sửa, chờ Minh: quy tắc E1-CP; cách đọc cặp phụ thuộc quan sát ở bước 5 (mục D).
- Runner sinh đúng số cấu hình theo `ma-tran-thu.json` sau Đ16; hai pha tách được; hash pha 1 ổn định.

**Câu hỏi của SPEC trả lời tới đâu:**
- A1 (code đúng đặc tả?): đúng trên mọi ca giả có đáp án; kết luận chỉ trong phạm vi fixture.
- A2 (test có sức bắt lỗi?): 35/35 đột biến bị bắt. Hai lượt phản biện vẫn tìm được lỗi mà bộ test và đột biến lúc đó không bắt (lượt 1: ba lỗi với 235 phép, 21 đột biến; lượt 2: tám điểm với 246 phép, 27 đột biến): phép kiểm và đột biến chỉ mạnh tới đâu đáp án và câu hỏi đặt ra tới đó. Chỗ không có fixture thì đột biến tương ứng không thể bị bắt (biên p = α, mục 9).
- A3 (nhãn có lọt?): kiểm tĩnh qua; fixture 74 qua; chặn rò ở mức giá trị (CĐ12) có test và đột biến D06–D08.
- A4 (tất định?): PASS trên ca giả. Trên dữ liệu thật: T-045 T1.
- A5 (đặc tả có chỗ sai hay mơ hồ?): không chỗ sai; 20 chỗ đặc tả không nói, người làm đã chọn cách hiểu (`dinh-chinh-cai-dat.md` Phần II, mục A); Minh duyệt giữ cả 20 ngày 29/10/2026.

**Không trả lời:** hiệu quả của M1 (RQ3b, RQ3c, RQ3d); hành vi, thời gian, RAM trên dữ liệu thật (T-045).

**Trạng thái:** Phần II mục A đã được Minh duyệt (29/10/2026); đã sửa sau phản biện lượt 1 và lượt 2 (trừ hai mục chờ Minh); chờ phản biện kiểm lại.

## 2. Đầu vào, môi trường, kiểm hash

- Kiểm hash T-043: PASS 69/69 file, 10/10 hash đóng băng, ở đầu giai đoạn 2 (`runs/kiem-hash-t043-001/stdout.txt`), cuối giai đoạn 2 (`runs/kiem-hash-t043-002/stdout.txt`) và sau gói sửa (`runs/kiem-hash-t043-003/stdout.txt`), qua `scripts/kiem_hash_t043.py` vì bản clone thiếu thư mục rỗng `runs/khe-open-001`. Chạy trực tiếp `tao_manifest.py --kiem` FAIL chỉ vì `luot_thieu` (`runs/kiem-hash-t043-001/truc-tiep.txt`).
- Môi trường: Python 3.12.3 (T-043 dùng 3.12.10 trên Windows); `requirements-m1.txt`: numpy 1.26.4, pandas 2.2.3, scipy 1.14.1, networkx 2.5, pytest 8.3.4, drain3 0.9.11, pyarrow 18.1.0; gói gián tiếp ở `freeze-m1.txt`.
- Hàm thư viện dùng ngoài phần tự viết:
  - networkx 2.5: `is_directed_acyclic_graph`, `all_simple_paths`, chỉ trong C-d3 (như mã PetShop; networkx 2.5 cũng trả bộ sinh rỗng khi nguồn trùng đích, như 2.8.8 của PetShop). PageRank, SCC (Tarjan), phủ đỉnh nhỏ nhất tự viết.
  - scipy 1.14.1: `mannwhitneyu(method='asymptotic', use_continuity=True)` cho cổng xấp xỉ khi n_N + n_A > 100; cổng chính xác là DP chép từ B1.8.
  - drain3 0.9.11: `Drain` (học mẫu, `fast_match`, cây tiền tố).
- Cảnh báo duy nhất khi chạy test: DeprecationWarning của `networkx/release.py` lúc import trên Python 3.12; không ảnh hưởng tính toán.

## 3. Kết quả phép kiểm

Nguồn: `runs/test-xanh-003/ket-qua.json` (từng phép), tổng hợp ở `bang-phep-kiem.json` (`scripts/tao_bang_phep_kiem.py`). Các lượt trước: `runs/test-xanh-001` (235/235), `runs/test-xanh-002` (246/246).

| Nhóm | Số phép | Qua | Con trỏ |
|---|---|---|---|
| Fixture T-043 trong phạm vi (82 fixture trừ D13) | 97 | 97 | `bang-phep-kiem.json#/theo_nhom/T043` |
| Fixture bổ sung B1–B8 | 8 | 8 | `#/theo_nhom/B` |
| U1–U6 (Đ15), H1–H6 (Đ19) | 12 | 12 | `#/theo_nhom/U`, `#/theo_nhom/H` |
| H1–H3 chạy qua chuỗi (trạng thái quan sát của nguồn metric) | 3 | 3 | `#/theo_nhom/H_qua_chuoi` |
| Đáp án tự lập, thành phần (66 mục) | 80 | 80 | `#/theo_nhom/tu_lap_thanh_phan` |
| Đáp án tự lập, đối chứng (15 mục) | 15 | 15 | `#/theo_nhom/tu_lap_doi_chung` |
| Đáp án từ văn bản đặc tả (5 mục) | 5 | 5 | `#/theo_nhom/tu_lap_van_ban` |
| Phép bổ sung của người làm (đầu-cuối từ span, runner, adapter, kiểm tĩnh, cache…) | 34 | 34 | `#/theo_nhom/bo_sung_nguoi_lam` |
| **Tổng** | **254** | **254** | `#/tong` |

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

## 8. Đột biến

Nguồn: `runs/dot-bien-004/tong-hop.json`. Mỗi đột biến thay đúng một chuỗi trong bản sao tạm của `src/`; lượt đối chứng không đột biến xanh 254/254. Số phép trượt dưới đây theo lượt 004. D26, D27 đổi chỗ đột biến theo code mới của lượt 2 (cùng ý).

| Mã | Đột biến | Tệp | Phép trượt |
|---|---|---|---|
| D01 | E5: đảo quy tắc lan ngược và lan xuôi | `m1/e5.py` | 19 |
| D02 | E1-U: bỏ cắt con về cha | `m1/span.py` | 2 |
| D03 | Khóa K: đổi chỗ số kênh và tổng điểm | `m1/xep_hang.py` | 6 |
| D04 | Bộ kiểm trường cấm không duyệt list, tuple | `m1/hop_dong.py` | 3 |
| D05 | Luật C: δ = 0,02 | `m1_danh_gia/luat_c.py` | 4 |
| D06 | Pha 1 đưa mã mờ vào params | `m1/runner.py` | 4 |
| D07 | `src/m1` import bộ đánh giá | `m1/chuoi.py` | 1 |
| D08 | Pha 1 trỏ tới file nhãn | `m1/runner.py` | 1 |
| D09 | E1-CP bỏ dung sai τ | `m1/span.py` | 2 |
| D10 | E5: cách đọc nhóm vòng mặc định A | `m1/e5.py` | 2 |
| D11 | E7 cách 1: "mọi kênh" thành "một kênh" | `m1/e7.py` | 1 |
| D12 | E9: bỏ τ, lấy cả biên 2 ô | `m1/e9.py` | 1 |
| D13 | Đơn vị đếm: λ dùng T đảo | `m1/e4.py` | 3 |
| D14 | E6b: hệ số tắt dần 0,80 | `m1/xep_hang.py` | 2 |
| D15 | E4: n = 100 sang cổng xấp xỉ | `m1/e4.py` | 1 |
| D16 | Đổi S_lo và S_hi | `m1/quan_sat.py` | 1 |
| D17 | E3 cách khớp (a) dùng ngưỡng | `m1/e3.py` | 2 |
| D18 | Bỏ tầng kế thừa | `m1/xep_hang.py` | 8 |
| D19 | E5 bỏ thứ tự chuẩn (chạy với `M1_XAO=1`) | `m1/e5.py` | 1 |
| D20 | Cột metric không khai nguồn vẫn được chấm | `m1/chuoi.py` | 1 |
| D21 | Chuỗi thiếu `tham_so_E5` dùng cách đọc A | `m1/chuoi.py` | 1 |
| D22 | Luật C: P, M đếm mỗi ô một lần dù ô lấy k lần | `m1_danh_gia/luat_c.py` | 3 |
| D23 | Cờ M5 nhánh tắt bỏ bội số | `m1_danh_gia/pha2.py` | 1 |
| D24 | UV-6 bỏ bội số | `m1_danh_gia/uv6.py` | 2 |
| D25 | Mẫu số mốc giả không theo bội số | `m1_danh_gia/pha2.py` | 1 |
| D26 | Chuỗi không xuất trạng thái quan sát của nguồn metric | `m1/chuoi.py` | 4 |
| D27 | WORLD_DEPENDENT lấy mọi thực thể đứng trước root | `m1_danh_gia/the_gioi.py` | 3 |
| D28 | Pha 2: MRR đổi sang số thực | `m1_danh_gia/pha2.py` | 1 |
| D29 | RR_o: ô bội số 0 vẫn chia | `m1_danh_gia/rr.py` | 1 |
| D30 | Bước 8: đọc kết cục tại P của cặp phụ thuộc quan sát | `m1_danh_gia/chon_khoi.py` | 1 |
| D31 | T12: thiếu khóa con của `canh_tinh` không ra UNSUPPORTED | `m1/chuoi.py` | 1 |
| D32 | Bản ghi bỏ thống kê severity và cặp Drain | `m1/chuoi.py` | 1 |
| D33 | WORLD_DEPENDENT coi hòa là đứng sau | `m1_danh_gia/the_gioi.py` | 1 |
| D34 | WORLD_DEPENDENT chỉ xét thực thể có ở cả hai thế giới | `m1_danh_gia/the_gioi.py` | 1 |
| D35 | Không xuất trạng thái nguồn metric khi không có hàng | `m1/chuoi.py` | 1 |

- Gồm đủ sáu ví dụ của SPEC bước 7 (D01, D02, D03, D04, D05; rò nhãn D06–D08).
- Lượt `runs/dot-bien-001` (20 đột biến) có 2 đột biến sống sót: D02 vì fixture 4, 5 chỉ gọi `cat_con` trực tiếp, không đi qua `chuan_bi`; D10 vì test nhóm vòng luôn truyền cách đọc. Đã thêm test, không thêm đáp án.

## 9. Tự diễn giải, giới hạn, phần chưa kiểm

- Tự diễn giải đã duyệt: Phần I của `dinh-chinh-cai-dat.md` (CĐ1–CĐ16).
- Tự diễn giải lộ ra khi cài: Phần II mục A (PII-01…PII-20), Minh duyệt giữ cả 20 ngày 29/10/2026. Quy ước biểu diễn: mục B. Sửa trong phiên: mục C. Sửa sau phản biện lượt 1: mục C2. Sửa sau lượt 2: mục C3.
- Chưa kiểm (Phần II mục D):
  - biên p = α không có fixture; đột biến ≤ thay < sẽ không bị bắt (PII-01);
  - khoảng tin cậy bootstrap theo ô chưa nằm trong `luat_c` (báo kèm; T-045 dùng `p3.danh_gia.bootstrap`);
  - adapter chưa chạy trên dữ liệu dev; C-g, C-c chưa nối bản ghi P3 thật; cạnh tĩnh T12 chưa đọc mô hình T-038, T-039;
  - thời gian, RAM, giá trị trung gian trên ca thật (T-045 bước 0, T1);
  - quy tắc E1-CP (ngưỡng, biên, sibling, phá hòa) chưa thống nhất giữa CĐ1, bài CRISP và code CRISP; code hiện cho 2000 ở ca phản ví dụ, chờ Minh quyết (OPEN; ảnh hưởng D4 của T-045);
  - bước 5 luật chọn khối đọc cặp phụ thuộc quan sát theo kết cục tại P; có nên đọc là KHÔNG ĐỦ CA không, chờ Minh quyết (OPEN; đổi được cấu hình thắng).
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
Trên máy cloud dùng `$HOME/m1env/bin/python`; trên Windows dùng `py -3`.

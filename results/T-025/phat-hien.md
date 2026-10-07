# T-025 — Phát hiện ở chế độ (b) trên 30 ca dev RE2-TT

Ngày 07/10/2026. Người làm: Claude. Giao thức: `results/T-022/giao-thuc-v2.md` §7.1–7.4. SPEC: `tasks/T-025-che-do-b/SPEC.md`.

**Đây là phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố** (§7.1, Q-74 Q11). Mỗi bộ phát hiện nhận cả bản ghi 1.441 điểm một lần. BOCPD bỏ cột hằng và min–max trên cả bản ghi trước khi tìm điểm đổi, nên mọi vị trí BOCPD báo là **vị trí điểm đổi hồi cứu**, không phải thời điểm cảnh báo, và không gắn với t̂+300 (§4, §7.2). Mốc tiêm ở chỉ số 720 ở cả 30 ca (`cham/phan-tich-b.json` → `chi_so_moc_cac_gia_tri` = [720]; như §5.1), nên mọi ca có đúng 720 s nền; số ở đây chỉ nói cho cấu hình đó (§7.1).

Nguồn số: `phat-hien.json` (bản chép của `cham/phat-hien.json`, đầu ra `scripts/danh_gia_b.py`), `cham/phan-tich-b.json` (`scripts/phan_tich_b.py`), `cham-thu-gia/phat-hien.json` (phép thử dời mốc). Danh sách bản ghi chốt lúc 09:10:10 ngày 07/10: `ban-ghi-dua-vao-cham.json`.

## 1. Trạng thái

| Bộ phát hiện | Cột | OK | ERROR | TIMEOUT | Nguồn |
|---|---|---|---|---|---|
| BOCPD | tập Q-67 (25–48 cột thô; d = 22–39 sau bỏ cột hằng) | 30 | 0 | 0 | `phat-hien.json` → `bo_phat_hien.bocpd.tong_hop.trang_thai`; d: `cham/phan-tich-b.json` → `chi_phi.bocpd.d` |
| N-Sigma tập chính | tập BOCPD | 30 | 0 | 0 | `…nsigma.tong_hop.trang_thai` |
| N-Sigma đối chứng | mọi cột trừ `time` (340–375 cột) | 30 | 0 | 0 | `…nsigma_doi_chung.tong_hop.trang_thai`; số cột: `runs/nsigma-doi-chung-m2-001/luot/*/ban-ghi-0.json` → `input_shape.cot` |

Posterior BOCPD hữu hạn ở 30/30 ca (§7.2, V2-S1): không ca nào `ERROR`. Vì mọi ca `OK`, các số "có điều kiện trên ca OK" dưới đây là trên đủ 30 ca (sửa U1 của SPEC không phát sinh khác biệt).

## 2. Kết quả chính

Phát hiện theo ca, báo động đầu đúng: trên 30 ca. Các cột còn lại: trên 30 ca OK.

| Chỉ số | BOCPD | N-Sigma chính | N-Sigma đối chứng | Nguồn (`phat-hien.json` → `bo_phat_hien.<bộ>.tong_hop.`) |
|---|---|---|---|---|
| Ca được phát hiện (≥ 1 báo động sau mốc) | 30/30 | 30/30 | 30/30 | `theo_ca_tren_30.phat_hien` |
| Ca có báo động đầu đúng (t̂ ≥ t_tiêm) | **3/30** | **0/30** | **0/30** | `theo_ca_tren_30.bao_dong_dau_dung` |
| Báo động thô mỗi ca, trung vị (min–max) | 13,5 (5–31) | 557,5 (111–775) | 1.332,5 (1.238–1.341) | `co_dieu_kien_tren_ca_OK.so_bao_dong_moi_ca` |
| Báo động sai mỗi giờ bình thường | 23,9 (143 / 21.570 s) | 1.167,7 (6.033 / 18.600 s) | 3.563,0 (18.409 / 18.600 s) | `co_dieu_kien_tren_ca_OK.bao_dong_sai_moi_gio`, `bao_dong_sai`, `giay_binh_thuong_danh_gia` |
| Cửa sổ 60 s: TP / FP / FN / TN | 172 / 88 / 188 / 242 | 300 / 234 / 60 / 66 | 360 / 300 / 0 / 0 | `co_dieu_kien_tren_ca_OK.cua_so` |
| Precision / recall / F1 theo cửa sổ | 0,662 / 0,478 / 0,555 | 0,562 / 0,833 / 0,671 | 0,545 / 1,000 / 0,706 | `…precision`, `recall`, `f1` |
| Tỉ lệ dương giả theo cửa sổ | 0,267 | 0,780 | 1,000 | `…fpr` |
| Độ trễ (N-Sigma) / độ lệch vị trí điểm đổi hồi cứu (BOCPD), trung vị (min–max), s | 34 (2–317) | 9 (0–54) | 0 (0–0) | `…do_tre_s` |
| Thông báo sau thời gian trơ 300 s: trước mốc / sau mốc (tổng 30 ca) | 38 / 50 | 69 / 66 | 90 / 60 | `…thong_bao_truoc_tiem`, `thong_bao_sau_tiem` |
| Thông báo sai mỗi giờ bình thường | 6,34 | 13,35 | 17,42 | `…thong_bao_sai_moi_gio` |

Mẫu số báo động sai đúng §7.4: BOCPD 719 s/ca (21.570 = 30 × 719), N-Sigma 620 s/ca (18.600 = 30 × 620). Cửa sổ bị bỏ vì có điểm chưa đánh giá hoặc là cửa sổ cuối 1 điểm: BOCPD 2/ca, N-Sigma 3/ca (`…cua_so.bo` = 60, 90). Không cửa sổ nào cắt ngang mốc (`cat_ngang_moc` = 0), vì mốc ở giây 720 trùng biên cửa sổ.

## 3. Đọc kết quả

**Phát hiện theo ca 30/30 không có nghĩa là bộ phát hiện tốt.** Ba bộ báo dày tới mức gần như chắc chắn có báo động sau mốc. N-Sigma đối chứng báo ở 18.409/18.600 giây bình thường được đánh giá (99 %). Phép thử dời mốc 300 s về trước trong evaluator (`danh_gia_b.py … doi_moc=-300`, bản ghi không đổi) vẫn cho 30/30 ở cả ba bộ (`cham-thu-gia/phat-hien.json` → `bo_phat_hien.<bộ>.tong_hop.theo_ca_tren_30.phat_hien`). Chỉ số phân biệt được là báo động đầu đúng và báo động sai mỗi giờ.

**N-Sigma (k = 3, `startsfrom` = 100) báo ngay khi bắt đầu đánh giá.** Báo động đầu của N-Sigma tập chính ở giây 100–490 tính từ đầu file, của N-Sigma đối chứng luôn ở giây 100 (`cham/phan-tich-b.json` → `theo_ca.<oid>.nsigma.t_hat_giay_tu_dau_file`). Vì vậy t̂ của N-Sigma luôn trước mốc (t̂ − t_tiêm từ −620 đến −230 s), và không ca nào có lượt RCA ở báo động đầu đúng. Đã kiểm một phần (sửa sau phản biện, N1; `scripts/soi_nsigma_t_hat.py` → `cham/soi-nsigma-t-hat.json`, chỉ đọc dữ liệu, không nhãn): tại t̂, không ca nào có cột báo với dưới 20 điểm quá khứ (0/30 ở cả hai tập), nên cột bắt đầu bằng NaN không giải thích t̂. Cột báo có std quá khứ bằng 0 có ở 2/30 (chính) và 3/30 (đối chứng) ca, nhưng không ca nào chỉ do loại cột này. Số cột báo tại t̂: trung vị 1 (1–3) ở tập chính, 8 (3–21) ở đối chứng. Giả thuyết còn lại: báo động gộp OR qua d cột, nên tỉ lệ báo sai mỗi giây tăng theo d; cộng thêm đuôi dài của chuỗi độ trễ. Ví dụ, nếu các cột độc lập và có phân phối chuẩn, mỗi cột báo sai 0,27 % số giây, thì 30 cột cho ≈ 8 %/giây, 350 cột cho ≈ 61 %/giây. Phần do đuôi dài, phần do số cột: chưa kiểm. Không chỉnh ngưỡng hay `startsfrom` (SPEC "Không làm"; Q-66).

**BOCPD báo thưa hơn nhiều, nhưng báo động đầu cũng thường trước mốc.** t̂ của BOCPD ở giây 102–761; 3 ca t̂ sau mốc (+28, +32, +41 s), 9 ca t̂ trong 300 s trước mốc, 18 ca sớm hơn nữa (`cham/phan-tich-b.json` → `theo_ca.<oid>.bocpd.t_hat_tru_t_tiem`). Phép thử dời mốc −300 s cho 12/30 ca báo động đầu "đúng" (`cham-thu-gia/phat-hien.json` → `bocpd.tong_hop.theo_ca_tren_30.bao_dong_dau_dung`), khớp 3 + 9. Do min–max toàn chuỗi, điểm đổi trước mốc vẫn có thể chịu ảnh hưởng của phần sau mốc (look-ahead khai báo ở §7.2); chưa tách được trong task.

**Theo loại lỗi và root, báo động đầu đúng của BOCPD:** cpu 2/6, loss 1/6, các loại khác 0; auth 1/6, order 1/6, train 1/6, route 0/6, travel 0/6 (`phat-hien.json` → `bo_phat_hien.bocpd.theo_loai_loi`, `theo_root`). Ba ca là một điểm ở mỗi ô, không nêu mẫu hình (LESSONS QT15). Bảng theo ô: `…theo_o`.

## 4. Kiểm đúng đắn đã chạy

| Kiểm | Kết quả | Nguồn |
|---|---|---|
| Bộ phát hiện không nhận mốc (§11.8): khóa `job.json` | 90/90 job chỉ có `kind, method, files, tap_cot` | `runs/kiem-b-002/kiem-b.json` → `job_*` |
| §11.8 trên đầu ra thật: dời mốc −300 s ở evaluator | báo động đầu và t̂ giống hệt ở 90/90 ca-bộ; báo động lấy từ bản ghi không đổi | so `cham/` với `cham-thu-gia/` (LOG phiên 2) |
| N-Sigma tập chính so pilot T-031 (3 ca, cùng hash `src/p3`) | báo động, lượt RCA, cột giống hệt ở 3/3 ca | `runs/kiem-b-002/kiem-b.json` → `nsigma_vs_pilot_T031` |
| BOCPD laptop so EC2 (ca `dev-20acb4402d`, tiền tố T = 150) | R lệch tuyệt đối ≤ 2,2e-16; `maxes`, m, điểm đổi giống hệt | `runs/bocpd-r-tien-to-laptop-001/so-sanh.json` |
| BOCPD: posterior hữu hạn; sentinel chỉ ở `maxes` gốc | 30/30 hữu hạn; số điểm đổi gốc = số điểm đổi tính lại + 1 ở 30/30 ca | `runs/kiem-b-002/kiem-b.json` → `bocpd`; `bao-dong.json` → `diagnostics` |
| Mốc tiêm nằm trên lưới `times` của bản ghi | đạt 90/90 (evaluator dừng nếu không) | `scripts/danh_gia_b.py` → `kiem_moc_tren_luoi` |
| Tính lại độc lập (không dùng `src/p3/danh_gia.py`) mọi số theo ca: cửa sổ, báo động sai, giây bình thường, độ trễ, phát hiện, t̂, thông báo; tổng phát hiện, báo động sai mỗi giờ | 0 không khớp / 2.317 phép so (gồm cả phần RCA) | `cham/tinh-tay.json` |
| Chạy khô evaluator với nhãn giả trước khi chốt (2 bộ nhãn) | chạy hết, tính lại độc lập khớp 0 lệch; bộ kiểm bắt được 2 lỗi cấy vào | `work/chay-kho/` (LOG phiên 2, 09:08–09:10) |

## 5. Giới hạn

- Hồi cứu, 720 s nền cố định mỗi ca, 30 ca dev; không nói gì về test (§7.1, §14).
- Nhãn proxy giả định lỗi kéo dài tới cuối file (§7.4); chưa kiểm.
- BOCPD: min–max và bỏ cột hằng trên cả bản ghi (look-ahead); tên số là "độ lệch vị trí điểm đổi hồi cứu".
- Audit cột (§10): hợp cột qua 30 ca là 53 (tập BOCPD) và 382 (mọi cột); cột vắng từng ca ở `phat-hien.json` → `bo_phat_hien.<bộ>.audit_cot`. Tương quan với nhãn để P4 kiểm.
- Chi phí là của EC2, xem `chi-phi.md`.

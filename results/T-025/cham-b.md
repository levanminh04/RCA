# T-025 — RCA tại báo động đầu t̂ (chế độ b) trên 30 ca dev RE2-TT

Ngày 07/10/2026. Người làm: Claude. Giao thức: `results/T-022/giao-thuc-v2.md` §7.5, §8. SPEC: `tasks/T-025-che-do-b/SPEC.md`.

Tên trong bảng theo §7.5: "tích hợp P3: `<ranker>[<bộ phát hiện>]`". Ranker: BARO (RobustScorer), CIRCA kiến trúc OLS+RHT+DA (kèm RHT-only cùng lượt; mô hình khóa ở Q-80), TORAI bản sửa nguồn B (seed 0, 1, 2; trung bình theo ca). Bộ phát hiện: BOCPD và N-Sigma tập chính. N-Sigma đối chứng chỉ chấm phát hiện (Q-74 Q12). **Nhánh dùng BOCPD là hồi cứu:** chính t̂ chỉ có sau cuối bản ghi (§4), nên không gắn kết quả với thời điểm t̂+300.

Nguồn số: `cham-b.json` (bản chép của `cham/cham-b.json`, đầu ra `scripts/danh_gia_b.py`), `cham/phan-tich-b.json` (`scripts/phan_tich_b.py`), `cham/tinh-tay.json`. Danh sách bản ghi chốt lúc 09:10:10 ngày 07/10 (`ban-ghi-dua-vao-cham.json`, 360 bản ghi RCA). Đường dẫn khóa JSON dưới đây viết tắt: `[d][k]` = `cham-b.json` → `theo_bo_phat_hien.<d>.<k>.tong_hop`.

## 1. Lượt RCA và trạng thái

- Cả 30 ca có báo động ở cả hai bộ, nên mỗi bộ có 30 lượt RCA cho mỗi ranker (TORAI: 90 lượt). Mọi bản ghi RCA `OK` (180/180 mỗi bộ); BARO và TORAI `key_check = pass`; 0 lỗi runner (`runs/kiem-b-002/kiem-b.json` → `rca_nsigma`, `rca_bocpd`).
- Báo động đầu đúng (t̂ ≥ t_tiêm): BOCPD 3/30, N-Sigma 0/30 (`[d][k].so_ca_t_hat_dung`). Ca còn lại là `BAO_DONG_DAU_SAI`, tính trượt ở thành công chung (`[d][k].trang_thai_thanh_cong_chung`).
- Cửa sổ quanh t̂ cắt ở biên file (§7.5): đoạn N dữ liệu thô dưới 300 s ở 15/30 lượt BOCPD và 29/30 lượt N-Sigma; dưới 120 s ở 3 và 26 lượt (`runs/rca-*-001/luot/baro-*/ban-ghi-0.json` → `window.seconds_N`). Đoạn A luôn đủ 300 s. Mỗi ranker xử lý phần thiếu khác nhau (sửa sau phản biện, REVIEW R1, R2):
  - BARO: chỉ dùng các dòng có trong N.
  - CIRCA: dữ liệu quan sát không phủ đủ khoảng train [t̂−120, t̂−10] ở 3 (BOCPD) và 26 (N-Sigma) lượt. Loader RCAEval vẫn tạo đủ 111 điểm train: nó thêm biên đầu, nội suy rồi điền ngược, nên phần trước đầu file là giá trị đầu tiên lặp lại (`RCAEval/classes/data.py:92–104, 175, 225`). Train không ngắn đi; một phần là giá trị điền.
  - TORAI B: lưới cố định 40 bin 15 s từ t̂−300 (`src/p3/torai_b.py:113`); bin không có sự kiện được điền 0 (`:73, :78, :106`), kể cả bin trước đầu file. Ở 15/30 ca BOCPD (14 ca có 1–13 bin N hoàn toàn trước span đầu, 1 ca phủ một phần) và 29/30 ca N-Sigma (9–13 bin), N của trace và log có số 0 không quan sát được; số 0 này vào bước chuẩn hóa và điểm bất thường. Bản tác giả không thêm hàng (`RCAEval/main.py:381–393`). Không ca nào trong số đó có t̂ sau giây 420 (`cham/soi-bin-torai.json`). Không chạy lại; số TORAI có điều kiện được tách ở mục 3 và 5.

## 2. Thành công chung trên 30 ca (§7.5)

Báo động đầu đúng **và** root ở hạng ≤ k theo quy tắc hòa §8.4. Nguồn: `[d][k].thanh_cong_chung_tren_30`, MRR: `[d][k].thanh_cong_chung_bang_chinh.mrr`; khoảng bootstrap 95 % theo cặp ô (10 ô, B = 10.000, seed 20261005): `cham-b.json` → `bootstrap_thanh_cong_chung.phuong_phap`.

| Tích hợp P3 | Hit@1 | Hit@3 | Hit@5 | MRR | Bootstrap Hit@1 |
|---|---|---|---|---|---|
| BARO[BOCPD] | 0,067 | 0,067 | 0,100 | 0,073 | [0; 0,167] |
| CIRCA OLS+RHT+DA[BOCPD] | 0 | 0,033 | 0,033 | 0,025 | [0; 0] |
| CIRCA OLS+RHT-only[BOCPD] | 0 | 0 | 0 | 0,009 | [0; 0] |
| TORAI B[BOCPD] | 0 | 0 | 0,067 | 0,021 | [0; 0] |
| BARO, CIRCA (cả hai), TORAI [N-Sigma] | 0 | 0 | 0 | 0 | [0; 0] |

Cận lạc quan và bi quan do hòa bằng giá trị chính ở mọi dòng (`[d][k].thanh_cong_chung_bang_chinh.can_lac_quan`, `can_bi_quan`). Hit@1 = 0,067 của BARO[BOCPD] là 2 ca trên 30.

**Ba ca BOCPD báo đúng** (`cham/phan-tich-b.json` → `theo_ca.<oid>.bocpd`):

| Ca | Root, loại lỗi | t̂ − t_tiêm | Hạng root: BARO / TORAI B (3 seed) / CIRCA RHT+DA |
|---|---|---|---|
| `dev-3defe3d34b` | ts-auth-service, cpu | +28 s | 1 / 4, 4, 4 / 9 |
| `dev-98bc73c499` | ts-train-service, cpu | +41 s | 1 / 8, 8, 8 / 8 |
| `dev-f36d0647d5` | ts-order-service, loss | +32 s | 5 / 4, 4, 4 / 2 |

Ba ca là quá ít để so ranker với nhau; mọi khoảng bootstrap chứa 0. Kết luận chính của chế độ (b) trên dev: **thành công chung trước hết bị chặn bởi bộ phát hiện**. Báo động đầu đúng chỉ 3/30 (BOCPD) và 0/30 (N-Sigma), nên Hit@k chung tối đa là 0,1 và 0 (xem `phat-hien.md` §3). Trên 3 ca báo đúng, ranker vẫn làm mất thêm: Hit@5 của BARO 3/3, CIRCA RHT+DA 1/3, TORAI B 2/3 (bảng trên). 3 ca không đủ để đánh giá ranker. Ba ca này đều có t̂ sau giây 720, nên không chịu phần điền ở biên file (mục 1).

## 3. Thứ hạng tại t̂, không cần báo động đúng (có điều kiện, báo riêng)

Độ đo §8 trên 30 ca có lượt RCA, gộp t̂ đúng và sai. Nguồn: `[d][k].tren_ca_co_luot_rca`; t̂ đúng: `[d][k].tren_ca_t_hat_dung`; báo động sai: `[d][k].tai_bao_dong_sai_bao_rieng`.

| Ranker | BOCPD: Hit@1 / Hit@5 / MRR | N-Sigma: Hit@1 / Hit@5 / MRR |
|---|---|---|
| BARO | 0,267 / 0,400 / 0,325 | 0,033 / 0,067 / 0,082 |
| CIRCA RHT+DA | 0,133 / 0,467 / 0,267 | 0,033 / 0,133 / 0,106 |
| CIRCA RHT-only | 0,067 / 0,300 / 0,208 | 0,033 / 0,033 / 0,070 |
| TORAI B | 0,233 / 0,367 / 0,336 | 0,033 / 0,200 / 0,146 |

Mức ngẫu nhiên Hit@1 trên tập quan sát O (|O| = 68 ở mọi bản ghi): 0,015 (`[d][k].ngau_nhien_O_tb_hit@1_tren_ca_co_luot`, §8.7).

Hàng TORAI B ở bảng trên gộp ca đủ nền với ca có N bù 0 (mục 1). Tách ra (`cham/tach-torai-bu0.json`, phân tích đặt ra sau khi thấy số, theo REVIEW R1):

| TORAI B, trên ca có lượt RCA | Đủ nền: n, Hit@1 / Hit@5 / MRR | N có bù 0: n, Hit@1 / Hit@5 / MRR |
|---|---|---|
| [BOCPD] | 15, 0,467 / 0,733 / 0,580 | 15, 0 / 0 / 0,092 |
| [N-Sigma] | 1, 1 / 1 / 1 | 29, 0 / 0,172 / 0,116 |

Hai nhóm khác nhau cả về vị trí t̂ (nhóm bù 0 có t̂ trước giây 300, nên A không chứa mốc), nên chênh lệch này không đo tác động của việc bù 0.

**Tại báo động sai, tách theo việc cửa sổ A có chứa mốc không.** Đây là phân tích đặt ra **sau khi thấy số** (LOG phiên 2, 09:10), không khai trước; n nhỏ; không dùng để kết luận. Ranker xem A = [t̂, t̂+300). Khi t̂ trong 300 s trước mốc, A chứa phần đầu của sự cố. Tách 27 lượt báo động sai của BOCPD (`cham/phan-tich-b.json` → `bao_dong_sai_theo_A.bocpd`):

| Ranker [BOCPD], báo động sai | A chứa mốc (n = 9): Hit@1 / Hit@5 / MRR | A không chứa mốc (n = 18): Hit@1 / Hit@5 / MRR |
|---|---|---|
| BARO | 0,667 / 0,889 / 0,747 | 0 / 0,056 / 0,047 |
| CIRCA RHT+DA | 0,222 / 1,000 / 0,454 | 0,111 / 0,222 / 0,178 |
| CIRCA RHT-only | 0,111 / 0,778 / 0,410 | 0,056 / 0,111 / 0,127 |
| TORAI B | 0,778 / 1,000 / 0,861 | 0 / 0 / 0,094 |

Với N-Sigma, chỉ 1 ca A chứa mốc (`bao_dong_sai_theo_A.nsigma`). Khi A chứa mốc, BARO và TORAI B đứng đầu ở 6/9 và 7/9 ca. Khi A không chứa mốc, ranker chỉ thấy dữ liệu trước sự cố: BARO và TORAI B có Hit@1 = 0, nhưng CIRCA RHT+DA có 2/18 và RHT-only 1/18, cao hơn mức ngẫu nhiên 1/68 ≈ 0,015. Nguyên nhân chưa xác định (trúng tình cờ, schema, hay ca cùng ô phụ thuộc nhau); không suy ra CIRCA hơn ngẫu nhiên. Ở nhóm này, 15/18 ca TORAI có N bù 0 (`cham/tach-torai-bu0.json`). Theo §7.5 các ca này vẫn là trượt trong thành công chung; số ở bảng này chỉ để phân tích. Dời mốc −300 s ở evaluator đưa đúng 9 ca này vào nhóm "đúng" (`cham-thu-gia/cham-b.json`, BARO[BOCPD] Hit@1 0,267), khớp.

**Bảng RCAEval riêng (§8.6)** trên bản ghi tại t̂, 30 ca, cùng thứ hạng: `[d][k].rcaeval_tren_ca_co_luot_rca` (TORAI theo từng seed; ba seed cho cùng số ở cả hai bộ). Không dùng bảng này để kết luận khi có hòa.

## 4. CIRCA và luật 1e10 (§6.5, Q-82, WHY-36)

Luật tách không dùng nhãn, chốt trước khi chấm, áp trên bản ghi tại t̂: ca có ít nhất một nút điểm RHT > 1e10. Tại t̂, tên nhóm chỉ có nghĩa là vượt ngưỡng; nguyên nhân lỗi làm tròn mới xác nhận ở 11 ca dev chế độ (a).

| | Ca vượt | Nhóm không vượt: thành công chung Hit@5 (RHT+DA / RHT-only) | Nhóm không vượt, trên ca có lượt: Hit@1 / Hit@5 (RHT+DA) |
|---|---|---|---|
| BOCPD | 8 (`dev-03d4910932`, `dev-16870e660c`, `dev-3ae0a6c15a`, `dev-4e68956051`, `dev-a5cabe5fa7`, `dev-a915aa2424`, `dev-b8bd0abf60`, `dev-de89e2f9e9`) | 0,045 / 0 (n = 22) | 0,136 / 0,273 |
| N-Sigma | 1 (`dev-8017c6dc70`) | 0 / 0 (n = 29) | 0,034 / 0,138 |

Nguồn: `[d][circa:ols+rht_da].nhom_khong_vuot_1e10`, `[d][circa:ols+rht].nhom_khong_vuot_1e10`. Bảng ở mục 2–3 là trên mọi ca có lượt RCA. Route hồi quy (tổng nút qua 30 lượt RHT+DA): BOCPD 4.536 hồi quy tuyến tính, 4.118 không cha hiệu lực; N-Sigma 4.511 và 4.105; không nút `value_error_fallback` (`[d][circa:ols+rht_da].regression_routes_tong`).

## 5. Chẩn đoán phương pháp (không cần nhãn)

- TORAI B: tỉ lệ cụm rơi nhánh dự phòng trung bình 0,89 (BOCPD) và 0,93 (N-Sigma); 53/90 và 66/90 lượt có mọi cụm rơi dự phòng; 22/30 ca ba seed cho cùng thứ tự (`cham/phan-tich-b.json` → `torai`). Tách theo nền (REVIEW R1, `cham/tach-torai-bu0.json` → `du_phong`): BOCPD, đủ nền 0,82 (16/45 lượt toàn dự phòng), N bù 0 0,96 (37/45); N-Sigma, đủ nền 0,80 (0/3), N bù 0 0,93 (66/87). Nghĩa là thứ hạng TORAI ở đây phần lớn là thứ tự dự phòng, không phải thứ tự của bước nhân quả RCD (LESSONS SL36). Không đổi gì.
- BARO: thứ hạng trùng thứ tự cột ở 0/30 lượt mỗi bộ; `key_check` đạt 30/30 (`cham/phan-tich-b.json` → `baro`).
- Không có cặp khối TORAI cùng điểm và không có hòa trong khối ở 180/180 bản ghi TORAI (LOG phiên 2, 09:10).

## 6. Kiểm đúng đắn

| Kiểm | Kết quả | Nguồn |
|---|---|---|
| t của mọi lượt RCA = t̂ của bộ phát hiện | 360/360 | `runs/kiem-b-002/kiem-b.json` → `lech_t_hat`; `danh_gia_b.py` dừng nếu lệch |
| Tính lại độc lập từng ca: E[Hit@1/3/5], E[RR] cho 4 biến thể × 2 bộ × 30 ca (TORAI liệt kê hoán vị khối), t̂ đúng/sai, thành công chung trên 30, danh sách ca vượt 1e10 | 0 không khớp / 2.317 phép so (gồm phần phát hiện) | `cham/tinh-tay.json` |
| Chạy khô với nhãn giả trước khi chốt | 2 bộ nhãn giả, 0 lệch; bộ kiểm bắt 2 lỗi cấy | `work/chay-kho/` |
| Thứ hạng tại t̂ = t so với bản ghi chế độ (a) (EC2 so laptop) | **không có ca**: chỉ số t̂ khác 720 ở 30/30 ca cả hai bộ (`cham/phan-tich-b.json` → `theo_ca.<oid>.<bộ>.t_hat_tru_t_tiem` ≠ 0). Chưa so trực tiếp thứ hạng EC2 với laptop ở cùng cửa sổ cho BARO/CIRCA/TORAI. Đã có: môi trường hai EC2 giống hệt nhau và cùng phiên bản gói với laptop (`runs/ec2-may{1,2}/runs/freeze-main-rca.txt`); mã khớp SHA-256 (LOG phiên 1, 22:25–22:32) | — |
| Tự kiểm biên (t̂ ở dòng 1, 100, 1.440 của một ca) | 15/15 lượt chạy, 0 lỗi runner; N = 1 s: BARO `NO_EVIDENCE`, CIRCA và TORAI `OK` | `runs/kiem-bien-m2-001/tom-tat.json` |

## 7. Giới hạn

- 30 ca dev; 3 ca báo đúng. Không kết luận về đồ thị (P4) hay về so sánh ranker.
- Nhánh BOCPD là hồi cứu (§4, §7.2).
- Đoạn N dữ liệu thô ngắn ở hầu hết lượt N-Sigma (t̂ gần chỉ số 100). CIRCA vẫn có 111 điểm train, một phần là giá trị điền ngược, ở 26/30 lượt N-Sigma và 3/30 lượt BOCPD (code tác giả, giữ theo §5.4).
- TORAI B điền 0 vào bin N trước đầu file ở 29/30 ca N-Sigma và 15/30 ca BOCPD (`src/p3/torai_b.py`). Giao thức chưa nói trường hợp này (§5.5 cấm kéo dài cửa sổ để bù; §6.6 viết cho chế độ (a)). Số TORAI có điều kiện ở các ca này không phải là TORAI trên nền đã cắt. Không ảnh hưởng thành công chung.
- TORAI chủ yếu chạy nhánh dự phòng.
- Chưa kiểm thứ hạng EC2 so với laptop ở cùng cửa sổ (mục 6).

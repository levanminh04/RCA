# Bàn giao phiên C — T-064: dời mốc ±30 s, H8-adapter, H8-log

Ghi 14/11/2026 ~07:30Z; bổ sung ca RECREATE-PAY 10:57Z. Người làm: Claude (phiên C). Brief: `tasks/T-062-dem-chang-1-4/PHIEN-C-BRIEF.md`. Nhật ký từng bước: `NHAT-KY.md`; checkpoint: `CHECKPOINT.md`; trạng thái: `TRANG-THAI.json` (`lo_exp_obs: xong`).

**Mọi kết quả dưới đây "chờ WHY"**: điều phối chép `de-xuat-WHY.md` (ba mục a, b, c) vào `docs/WHY.md` trước khi dùng trong `ho-so-chon.md`.

## 1. Mã đã đổi (`src/m1_ft/`, không chạm `src/m1`, `src/p3`)

| File | Thay đổi | sha256 |
|---|---|---|
| `chay_ca.py` | `--doi-t`, `--dung-lai-dau-vao`, `--cau-hinh-p7`, `--bo-sung-t-goc`, `--dem-dau-vao`; nhánh H8-adapter (biến đổi gói trước adapter); `log_phu` | `79cf3669…` |
| `doi_moc.py` (mới) | dựng lại 7 tham số từ gói ca với t' (đường của `run-m1.py` ghim) | `04c20c0f…` |
| `chay.py` | `_duong_ong_metric`: áp H8-adapter trước biến đổi khác; `bundles_bo_sung` có thể vắng | `22406828…` |
| `bo_sung.py` | thêm `log_phu` | `8f7f72cf…` |
| `thanh_phan/h8_adapter.py` (mới) | H8-adapter | `6a8ac65c…` |
| `thanh_phan/h8_log.py` (mới) | H8-log-kq, H8-log-chuoi | `80ef12e1…` |
| `tests/test_h8.py` (mới) | test H8 (đạt trên laptop) | `fa1cb44c…` |

- Mã nguồn chung (`ft.sha_ma_nguon()`): lô dời mốc chạy `05273b2e…` (`goc-10`); lô H8 và cây hiện tại `b0f79a4d…` (`goc-11`).
- **Đường mặc định giữ nguyên:** `chay_ca.py` cũ và mới trên cùng cây cho đầu ra trùng byte và `summary.json` trùng (V041, a5539fba). Kiểm lại sau mỗi lần sửa.
- **Đính chính chưa áp vào mã:** docstring `h8_adapter.py` nói "điểm bị bỏ luôn là bản lặp… `mat_mau == 0`" là sai (xem §4b). Sửa ở lần đóng gói kế tiếp; chưa sửa để giữ `ma_nguon_sha256` đã ghi trong đầu ra.

## 2. Sổ biến thể (`results/T-064/so-bien-the.jsonl`, chỉ thêm)

| Mã | Cha | Vai trò | Ghi trước chấm | Sau chấm |
|---|---|---|---|---|
| V052–V057 | P7, V032, V041 × d ∈ {−30, +30} | `do_nhay_moc` (không dùng chọn) | 05:19:19Z | 06:39:09Z |
| V058-KC-P7-dunglai-d0 | P7 | `kiem_cai_dat_doi_moc` | 05:19:19Z | 06:39:09Z |
| V059-TG-P7-t-300 | P7 | `thu_gia_doi_moc` | 05:19:19Z | 06:39:09Z |
| V060-H8a, V061-V032+H8a | P7, V032 | `h8_phien_c` | 05:39:46Z | 07:24:00Z |
| V062-H8lk, V063-V032+H8lk | P7, V032 | `h8_phien_c` | 05:39:46Z | 07:24:00Z |
| V064-H8lc, V065-V032+H8lc | P7, V032 | `h8_phien_c` | 05:39:46Z | 07:24:00Z |

Tổng phiên C: **14 bản** (V052–V065; ca RECREATE-PAY chạy lại V058, V032, V060, V061, không thêm mã), gồm 8 bản kiểm độ nhạy/kiểm cài đặt và 6 bản H8. Khai trong sổ: thiết kế sau khi đã xem lượt 1–3. H8-log thiết kế sau khi đếm log theo ca × service; người làm biết mã ca ↔ ô.

## 3. Dời mốc ±30 s (SPEC bước 6, §7) — chi tiết `doi-moc/PHAN-TICH.md`, `doi-moc/bang-o.md`

- **Kiểm đúng đắn.**
  - 176/176 cặp `status OK`, hai lần trùng SHA.
  - V058 (dựng lại, d = 0): `method-input.json` trùng byte ở 22/22 ca và đầu ra trùng byte P7 ở 22/22 ca (`cham/kiem-lo-doi-moc.json`).
  - Gói metric bổ sung xuất lại quanh t': 0 lệch ở 252.125 điểm chung (`doi-moc/kiem-bo-sung-doi-t.json`).
  - Thử giả d = −300: AC@1 của P7 5 → 1 (dev bản 2), 5 → 1,06 (T-062), nên phép kiểm có sức phân biệt.
- **Tập 13 ca** (AC@1 / AC@3 / tổng hạng cắt / K):

| Bản | d = 0 | −30 | +30 |
|---|---|---|---|
| P7 | 5 / 7 / 15 / 4 | 5 / 8 / 12 / 5 | 5 / 7 / 16 / 5 |
| V032 | 6 / 8 / 10 / 4 | 6 / 8 / 10 / 5 | 5 / 8 / 13 / 5 |
| V041 | 6 / 8 / 11 / 3 | 6 / 7 / 12,5 / 3 | 4 / 7 / 16 / 3 (cạnh 2/3) |

- **9 ca T-062:** ở +30, AC@1 của P7 và V032 5 → 3, của V041 5 → 4; ở −30 không đổi, trừ K của V041 1 → 2.
- **Ô nhạy:**
  - HTTP5-EVENT e9c9679b (1 → 2 ở ±30, mọi bản);
  - HTTP5-EVENT-FLASH 98ea5ba4 (2 → 1 ở −30, 2 → 3 ở +30);
  - PAUSE-PAYMENT (V032, V041: 1 → 3 ở +30);
  - BINH-THUONG 83073ed1 (`NO_INTRINSIC_ANOMALY` → `CAUSE_FOUND`);
  - T-062: HTTP5-EVENT a89954d1, NET-GW-BOOK f728fce2 (ở +30).
- **Ô bền** (không đổi ở cả 6 phép dời): CPU-BOOK-1, NET-GW-BOOK dev, FLASH-HEALTHY, SLOW-BOOK, CPU-BOOK T-062.
- **Cơ chế đã xác nhận trên trung gian:**
  - **C1:** ở +30, N chứa 30 s lỗi (10% > 1 − q_hi = 5%), nên ngưỡng E4 nhảy vào phân bố lỗi. Ví dụ f728fce2 cạnh E2 api-gateway→booking: `h` 1.952 → 316.532 µs, `r_len_A` 1 → 0, mất cờ.
  - **C2:** H5b mất điều kiện (i) vì liveness payment hụt từ t+15 s.
  - **C3:** `nhanh_z` chia cho IQR_N của chuỗi workload phẳng: 0,04 → 0,025, z 69,25 → 110,6 (tính lại khớp đầu ra).
  - Ca "tốt lên" ở +30 (4af494a5) cũng do C1 tác động lên đối thủ của đáp án.
- **Chưa kiểm:** lý do định vị cạnh REDIS-BOOK của V041 đổi sang `phia_dich` ở +30; CPU-BOOK-2 của V041; p/ngưỡng từng đơn vị lật ở 83073ed1; 98ea5ba4 ở −30.
- **Suy luận:** M1 (mọi bản) nhạy với mốc muộn 30 s; cơ chế chính là cách E4 chọn N/A theo mốc, không riêng thành phần nào. Trên tập 13 ca, V032 không kém P7 ở cả ba mốc; V041 kém P7 về AC@1 ở +30. Lợi thế của V032 ở PAUSE-PAYMENT mất ở +30.
- **Hệ quả cho FlashTicket:** mốc t phải đặt không muộn hơn lúc khởi phát lỗi. Với RCA trực tuyến lấy t từ cảnh báo (G3), đây là yêu cầu thiết kế, **chưa kiểm**.

## 4. H8-adapter (2b)

- **a. Dữ liệu** (`h8-adapter/dem-chuoi-trung.json`): trên 37 gói ca của `exp-obs`, chỉ `thuong01` làm adapter ghim ném lỗi. thuong01 là ca chạy thử 11/11 giữa lượt triển khai, cpu/mem có 2–3 `container_id` ở 7 service; nguồn gốc đã ghi ở `results/T-062/chay/thu-ong-M1.md`. 22 ca của hai tập: 0 metric logic có > 1 định danh. Lần theo mốc mẫu gốc: các chuỗi không chồng lấn (ví dụ api-gateway [−609, −509] s và [−499, 591] s); phần "chồng lấn" trên lưới chỉ là lookback của PromQL.
- **b. Cài và kiểm.**
  - Nối theo thời gian khi chỉ khác nhãn runtime và không chồng lấn mốc gốc (WHY-(b)).
  - Test `tests/test_h8.py`: tách giả một chuỗi thật theo ngữ nghĩa lookback → adapter ghim ném lỗi; nối lại → rows/owners/indices/clocks/coverage/aliases trùng bản gốc; chồng lấn và khác nhãn ngoài runtime thì không nối.
  - thuong01 trên `exp-obs`: P7 dựng lại (V058) ném `Multiple runtime series…`; V060 chạy được, 14 nhóm nối, 0 nhóm không nối, `diem_lap_bo` 318, `mat_mau` 12.
  - Đã lần 12 mẫu đó: mỗi mẫu là mẫu gốc cuối của container cũ, cùng bước lưới 15 s với mẫu đầu container mới, nên một chuỗi liên tục cũng không trả. **Không mất thông tin**; nhưng docstring sai (§1).
  - thuong01 chỉ có 10 dòng log (KP-19), nên `nguon_khong_phu_tron: ['log']`.
- **c. Chấm:** V060 = P7, V061 = V032 (ngoài `extra.m1_ft`) ở 22/22 ca → **KHONG_TAC_DUNG theo chữ §4, nhưng đúng nghĩa là "chưa thử được hiệu quả xếp hạng"**: không ca nào có tình huống. Đây là thành phần đáp ứng nhu cầu kỹ thuật (P7 ERROR cả ca), không phải xử lý một hạn chế phương pháp (luật 18).
- **d. Ca thật RECREATE-PAY** (phiên B thu, mã `ebd5ef38`; sổ `chay_them` 10:50:19Z trước khi chạy, `sau_cham` 10:55:02Z; TD-64-13). **Chưa vào tập chọn**: hậu kiểm theo điều kiện khai trước trượt httpcheck; "Sửa sau 2" chờ Minh.

| Bản | Kết quả trên ebd5ef38 |
|---|---|
| P7 (V058, dựng lại) | ERROR adapter `Multiple runtime series…` (như runner ghim của phiên B) |
| V032 (dựng lại) | ERROR adapter |
| V060 = P7 + H8-adapter | OK, trùng SHA, **payment-service hạng 1** (p1 = 1) |
| V061 = V032 + H8-adapter | OK, trùng SHA, payment-service hạng 1 |

  - **Cơ chế:** H8-adapter nối cpu/mem của payment (cũ [−607, +3] s, mới [+13, 593] s theo mốc gốc; 0 nhóm không nối). Payment lên hạng 1 nhờ span payment chậm từ khoảng t+50 s (JVM mới) và kênh `mem` xuống (khởi phát t+10 s). Kênh `mem` chỉ có nhờ chuỗi đã nối.
  - **Hạn chế dữ liệu phát hiện ở V061 (luật 17), ảnh hưởng H5/H5b, không riêng H8:** H5b coi payment "chết im" tới hết cửa sổ. Nhưng mẫu thô `httpcheck_error` chỉ hụt ở t+3…t+43 (bằng chứng của phiên B, `results/T-063/thu3/dieu-kien-xac-nhan-3.md` "Sửa sau 2"). `query_range` giữ giá trị 1 tới khoảng t+343 vì chuỗi đẩy qua OTLP không có dấu stale (lookback 5 phút). Thời gian hụt thật khoảng 50 s, dưới ngưỡng 60 s của H5b. Vậy H5b kích hoạt do lookback. Kết luận đúng ở ca này không nhờ H5b, vì V060 cũng xếp payment hạng 1. Cần xét: bộ xuất bổ sung (`results/T-063/dong-goi/xuat_bo_sung.py`) có nên đọc mẫu thô cho kênh liveness không, và WHY-86 có cần ghi điều kiện thất bại này không.
  - **Kết luận về H8-adapter:** đáp ứng nhu cầu kỹ thuật (P7 ERROR cả ca → bản có H8-adapter cho đáp án đúng ở hạng 1) trên **một ca, một lần thu, chưa vào tập chọn**. Trên 22 ca của hai tập: trùng bản cha. Không đổi kết luận §4 trên tập chọn; việc đưa vào bản đề xuất thuộc điều phối và Minh, sau khi Minh quyết ca này.

## 5. H8-log (2c)

- **a. Dữ liệu** (`h8-log/dem-log-nghiep-vu.json`):
  - Có ở cả 22 ca. Dev bản 2: api-gateway, booking, payment, ticket ghi `outcome` ở 100% bản ghi JSON; event-service chỉ có log ở 2 ca (FAILED); user-service không có ở ca nào. T-062: api-gateway, payment, ticket.
  - Giá trị đúng tập B16.
  - Bảng chéo 22 ca (`h8-log/cheo-severity-outcome-22ca.json`): ERROR trùng FAILED ở 10.424/10.424 dòng. Khác biệt duy nhất: 4.490 dòng UNKNOWN (payment INFO ở 9 ca T-062; 5 dòng ở 46aab4be).
- **b. Thiết kế** (WHY-(c)): nút = thực thể ghi log, không cạnh mới.
  - **H8-log-kq:** phân loại lại dòng lỗi của `log_loi` theo outcome.
  - **H8-log-chuoi:** `log-kq-loi` (lớp lỗi) và `log-kq-ok` (lớp lưu lượng), ô 15 s.
  - Phương án thêm đơn vị log mới bị loại vì cổng D1 của P7 tính mốc N trong `chuoi._chay`.
- **c. Chấm** (`cham/h8.json`; §4 như `cham/giu_bo.py::xet`):

| Bản | Phép | Tập 13 ca | Kết luận §4 | T-062 so P7 |
|---|---|---|---|---|
| V062 H8lk | 1 | = P7 (5 / 7 / 15 / 4) | KHONG_TAC_DUNG | không hồi quy |
| V063 V032+H8lk | 2 | = V032 | KHONG_TAC_DUNG | không hồi quy |
| V064 H8lc | 1 | 5 / 7 / **13** / 4 (P7 15) | **GIU (l1)** | không hồi quy |
| V065 V032+H8lc | 2 | = V032 (6 / 8 / 10 / 4) | KHONG_TAC_DUNG | không hồi quy |

- **d. Cơ chế.**
  - **H8lk:** đầu vào đổi đúng 10 ca dự báo, không đại lượng chấm nào đổi (một ca FLASH T-062 đổi thứ tự nhưng K vẫn 1). Trên FlashTicket hiện tại, severity ERROR đã trùng outcome FAILED, nên kênh gần như trùng `log_loi`.
  - **H8lc:** ở PAUSE-PAYMENT, `log-kq-ok` xuống của payment có cờ (s = 7,2), nên payment từ ngoài thứ hạng lên **hạng 4**. P7 không có kênh nào của payment vì thành phần tạm dừng im lặng. Payment không lên đầu vì SUCCESS giảm theo cả luồng mua (api-gateway s = 12,7; booking 8,2).
  - **Đầu vào thật:** kênh cho 4–5 thực thể/ca dev, 3–4/ca T-062. Đơn vị có cờ: 21 ở 4 ca dev (2 HTTP5-EVENT, PAUSE, FLASH), 4 ở 2 ca T-062 (HTTP5-EVENT, FLASH). 0 cờ ở ca BINH-THUONG.
  - Ở FLASH, `log-kq-ok` gắn cờ "lên" theo tải (điều kiện thất bại đã ghi). K không đổi vì các ca này đã `CAUSE_FOUND`.
- **e. Giới hạn của "GIU (l1)" của H8lc:**
  - Lợi đến từ **một ô** (PAUSE-PAYMENT, một lần thu). Đó là ô người làm đã thấy khi đếm log (đã khai trong sổ).
  - Phép 2 không tác dụng vì V032 đã giải ô này bằng H5b.
  - Theo §5 (4) "ít thành phần hơn", thêm H8lc vào V032 không có căn cứ trên tập này. Quyết định đưa vào hồ sơ thuộc điều phối.

## 6. Đề xuất WHY

`de-xuat-WHY.md`: (a) dời mốc bằng dựng lại đầu vào và xuất lại gói bổ sung; (b) nguyên lý gộp chuỗi H8-adapter, kèm đính chính `mat_mau`; (c) kênh log B16.

## 7. Phần chờ dữ liệu của phiên B

Ô RECREATE-PAY đã thu và đã chạy (§4d). Còn chờ Minh nhận "Sửa sau 2" để ca vào tập chọn. Nếu Minh nhận: chấm lại tập (13 + RECREATE-PAY) bằng `cham_phien_c.py` với tập chọn mới; đầu ra đã có ở `bien-the/V060-H8a/ra-recreate/`, `bien-the/V061-V032+H8a/ra-recreate/`. P7 và V032 trên ca này là ERROR, tính là trượt theo tiêu chí §2.

## 8. Việc cần Minh hoặc điều phối quyết

1. Chép WHY-(a)(b)(c) trước khi dùng kết quả.
2. Có đưa H8-log-chuoi vào hồ sơ chọn không, khi nó chỉ giữ theo phép 1, ở một ô đã xem trước.
3. Có chạy thêm d ∈ {−60, −15, +15} để tìm ngưỡng lật ở các ô HTTP5-EVENT không (ước khoảng 1 giờ máy, chờ `exp-obs` rảnh sau đợt thu).
4. Có thiết kế biến thể bền với mốc muộn không (thay đổi phương pháp, cần sổ và WHY).
5. Sửa docstring `h8_adapter.py` ở lần đóng gói kế tiếp.
6. Minh nhận "Sửa sau 2" cho RECREATE-PAY không (do phiên B trình; quyết định này quyết luôn việc ca vào tập chọn của H8-adapter).
7. Hạn chế lookback của kênh liveness H5/H5b (§4d): sửa bộ xuất hay ghi điều kiện thất bại vào WHY-86 — thuộc điều phối.

## 9. Lệnh cuối và trạng thái máy

- **Lệnh cuối:** `chay_recreate.sh` trên exp-obs (TD-64-13), rồi ghi sổ `sau_cham` của ca RECREATE-PAY.
- **Máy:** `exp-obs` không còn tiến trình của phiên C (kiểm 07:21:52Z). Thư mục giữ lại (TD-64-11, TD-64-12): `goc-10`, `goc-11`, `out/pc-doi-moc`, `out/pc-doi-moc-dem` (bộ đệm đầu vào, khoảng 2 GB), `out/pc-bo-sung-dt`, `out/pc-h8`, `~/phien-c`. Đầu ra đã chép về repo:
  - dev2: `results/T-064/cham/dau-ra-dev2/V05[2-9]-*`, `V06[0-5]-*`;
  - T-062: `results/T-064/bien-the/<mã>/ra-doi-moc|ra-h8/`;
  - thuong01: `bien-the/V060-H8a/ra-kc/`.
- **Chưa commit** (brief §7).

# T-074 — Thiết kế W6, bản 4

- **Soạn:** Claude, phiên `danh-gia-w6`, 23/11/2026. Không dùng máy, không SSH, không subagent, không commit.
- **Cách đọc:** bản 4 = `thiet-ke-w6-2.md` + `thiet-ke-w6-3.md` + các mục dưới. Chỗ khác nhau theo bản mới hơn. Bảng §0 chỉ mục nào hiện hiệu lực ở bản nào. Bản 1–3 giữ nguyên (`SHA256SUMS`, `-2`, `-3`).
- **Nguồn sửa:** tự soát bản 3 (N1–N4, LOG phiên 4, ghi **trước** khi đọc phản biện); Codex CX-15 (`results/T-070/codex/CX-15-tin-cuoi.md`, điểm 1–6) và CX-15b (`CX-15b-tin-cuoi.md`, điểm 1–6 và N1–N5); tổng hợp `results/T-070/hop-nhat-cx13-16.md` §3; phạm vi RQ3d (CX-06, CX-08); dữ liệu mới W4 (`results/T-072/bang-bao-dong-gia.md`, `troi-p95-e2-e4.md`) và E5 (`results/T-073/e5-ket-qua.md`).
- **Đi kèm:** `du-toan-4.json` (tự đủ, thay `du-toan.json` và `du-toan-3.json`), `cau-hoi-minh-4.md` (danh sách quyết định **duy nhất**), `e6-spec-nhap.md` (nháp SPEC bổ sung E6).
- **Trạng thái:** đề xuất. Quyết định đã có của Minh: D2, R9 (LOG T-070 lượt 3, 6; `docs/DECISIONS.md` mục "Điều phối giai đoạn 2: quyết định R1, R5, R7, R9").

---

## 0. Mục hiệu lực

| Chủ đề | Hiệu lực ở | Ghi chú |
|---|---|---|
| Khóa bản | bản 2 §1 | digest lấy ở E6 (`e6-spec-nhap.md` bước 7) |
| Chế độ (a)/(b), D13 | bản 2 §2 + **bản 4 §6** | D13 khả thi tới g ≤ 300 s |
| D14, nhóm che | bản 2 §3 + bản 3 §E | — |
| Đối chứng quan hệ | bản 2 §3.4 + **bản 4 §12** (phạm vi RQ3d) | — |
| Ma trận ô | bản 2 §4 + bản 2 §4.3 (D2) | — |
| Lặp, mức tải, thứ tự, khối | bản 2 §5.1–5.2 + bản 3 §F (khối) + **bản 4 §8** | — |
| Kiểm soát DB | bản 2 §5.3 + bản 3 §F, §G | — |
| E6 | **`e6-spec-nhap.md`** (thay bản 2 §5.4) | — |
| Hạn bán, sức chứa | **`e6-spec-nhap.md`**, `du-toan-4.json` | — |
| R-07 | bản 2 §6 + bản 3 §H + **bản 4 §9** | — |
| Baseline | bản 2 §7, §7.1 + bản 3 §C + **bản 4 §5, §10, §11** | — |
| Runner | bản 2 §8.1–8.3 + **bản 4 §6** | — |
| Gói hợp lệ, bù ca | bản 3 §B.1–B.2 + **bản 4 §2** | — |
| Độ đo phát hiện | bản 3 §A, §B.3 + **bản 4 §3, §4, §7** | — |
| Độ đo xếp hạng, vùng | bản 2 §9.2–9.3 + **bản 4 §7** | — |
| Bảng diễn giải | **bản 4 §7** (thay bản 2 §9.4) | — |
| Điểm yếu một mẫu max | bản 2 §10 mục 1–3, 5 (mục 4 bỏ ở bản 3 §G) | — |
| Dự toán | **`du-toan-4.json`** | `du-toan.json`, `du-toan-3.json` hết hiệu lực |
| WHY đề xuất | `de-xuat-why-2.md` + bản 3 §D + **bản 4 §13** | — |

---

## 1. Dữ liệu mới từ W4 và E5 dùng cho W6

**W4 (T-072):** trên 383 phút khỏe ×1 của E4 (∩ phút Grafana đánh giá), 0 sự cố; đạt R5 theo phép so đã khai; khoảng tin cậy Poisson 95% [0; 3,47]/6 giờ (`bang-bao-dong-gia.md`). Bảy luật **chưa kiểm dương** trên dữ liệu thật (p95 booking/event/ticket, lỗi booking/ticket, mất dò, mất gateway). p95 payment và ticket ở E4 tới 0,84 ngưỡng; T-072 xếp "dao động đuôi do ~72 request/5 phút" là giải thích ứng viên chính, "trôi do DB" không được dữ liệu cả lượt hỗ trợ (`troi-p95-e2-e4.md` §3). Hệ quả cho W7:
- W7 là lần kiểm dương đầu tiên của nhiều luật. Không đổi ngưỡng trong W7 (sửa sau thì báo riêng).
- Báo động giả ở W7 báo **theo luật**, để thấy riêng payment và ticket.
- ×3 làm số request mỗi cửa sổ tăng; tác động lên đuôi p95 của payment/ticket **chưa biết** (nhiều request hơn làm p95 ổn định hơn, nhưng tải cao có thể làm request chậm nhiều hơn).

**E5 (T-073):** một lượt `PAUSE-PAYMENT` ×1, chế độ (b): t̂ = mốc gây lỗi theo nhật ký điều khiển + 60 s (luật liveness); stage bắt đầu t̂ + 753 s; xử lý ~104 s; dashboard hiện ca ≈ 14,8 phút sau t̂; `phu.du_cua_so = false` vì 6 metric của Payment thiếu (lỗ 365 s) — có thể do chính lỗi pause, chưa phân xử (`e5-ket-qua.md` §1–§3). Hệ quả cho W7:
- Khớp quy tắc bản 3 §B.1: ca như vậy **giữ**, cờ `thieu_chua_phan_loai` cho tới khi có bằng chứng nối với can thiệp.
- Một lượt, một ô dev, ×1: **không** dùng làm số độ chính xác hay độ trễ của W7.

---

## 2. Bù ca và Ticket (CX-15 điểm 1; CX-15b điểm 1: đúng một phần)

**Sự thật đã kiểm (`407b4f5`):**
- `runner4.py` ghi `fault-start-failed` cho **mọi** ngoại lệ của `inj('start', …)` (dòng 268–270); khi đó `fault_ok = False` và runner bỏ lệnh `stop` thường. Ngoại lệ có thể xảy ra **sau** khi máy đích đã tác động (ví dụ mất phản hồi SSH).
- `inj3.py` có hẹn giờ tự gỡ cho kiểu `toxic` và `pause` (tiến trình tách phiên gọi `stop(cell)` ở hạn + 5 s, dòng 142–155). Chỗ hở: hẹn giờ không chạy được hoặc gỡ lỗi.
- `trang_thai_sach()` chỉ kiểm pause của **Payment** (`PAY`, dòng 284–285); ô mới TICKET-PAUSE sẽ không được kiểm sạch.

**Quy tắc bản 4 (thay bản 3 §B.2 dòng `fault-start-failed`):**

| Tình huống | Bằng chứng cần | Xử lý |
|---|---|---|
| Xác nhận **chưa tiêm** | đầu dò hoặc nhật ký phía đích cho thấy không có tác động (không toxic, không pause, không lease, không luồng đốt, container không đổi `StartedAt`) | ca không vào mẫu số lỗi; **bù 1 lần** bằng lịch con |
| Mất phản hồi, chưa rõ đã tiêm chưa | `fault-start-failed` mà không có bằng chứng dòng trên | **giữ** ca, nhóm "can thiệp chưa xác nhận"; **không bù**; trước chu kỳ kế: kiểm sạch đúng container/proxy/lease của ô đó; không sạch → gỡ, kiểm lại; vẫn không sạch → dừng lượt (luật 21: lỗi nguồn chung) |
| Đã tiêm, đầu dò không xác nhận | như bản 3 | giữ, nhóm riêng, không bù |

**Yêu cầu cho gói code W7:** `trang_thai_sach()` và `verify()` của bộ tiêm phải kiểm **mọi** container có thể bị pause (thêm Ticket), mọi proxy mới (hạng B), mọi cgroup có luồng đốt (Event nếu có CPU-EVENT). Mặt trái của quy tắc: có thể để một ô thiếu một lần lặp; bù tự động thì có nguy cơ đếm hai lần một can thiệp đã diễn ra.

---

## 3. Mẫu số ×3 (CX-15 điểm 2; CX-15b điểm 2: đúng một phần)

**Sự thật:** `results/T-071/phan_loai_phut.py` (dòng 189: `muc = 'x3' if (l.get('buoc_tai') and a >= l['S'] + l['buoc_tai']) else 'x1'`) chỉ đặt mức `x3` khi lượt có `buoc_tai` và đã qua mốc tăng bậc; hệ số khởi đầu của lượt không được xét. W7 chạy ×3 **từ đầu chu kỳ**, không có bậc → nếu dùng nguyên code, phút ×3 rơi vào nhánh ×1 và có thể nhận `khoe_x1`. Sai cả tử số lẫn mẫu số.

**Quy tắc bản 4 (thay bản 3 §B.3):**
- Mức tải của mỗi phút lấy từ **lịch thực chạy** (hệ số khởi đầu và bậc tải của lượt trong sổ/`tai-out`), không từ nhãn của bộ phân loại.
- Phút ×1: dùng `khoe_x1` của bộ phân loại T-071 như cũ.
- Phút ×3: không dùng nhãn khỏe của bộ phân loại. **Điều kiện nhận phút ×3** (khai trước): đúng mức tải theo lịch; không có bằng chứng hỏng đường thu độc lập (bản 3 §B.1 dòng 1); Grafana đánh giá phút đó (§4); hành trình k6 không có lỗi hạ tầng tải (k6 chạy, không `dropped_iterations` do máy tải). Không đòi chỉ tiêu khỏe phụ thuộc tốc độ.
- **Điều kiện nhận phần N của ca ×3 vào mẫu số xếp hạng** (thay bản 2 §8.4 điều kiện 3 cho ×3): như trên, cộng không 429 do quota trong N (I2). Tiêu chí K1–K5/B1–B2 nào của T-071 không phụ thuộc tốc độ thì áp được cho ×3 — **CHƯA-KIỂM** từng tiêu chí; gói code W7 lập bảng trước khi khóa.
- **Báo cáo:**
  - ×1: báo động giả mỗi giờ khỏe ×1 (phút `khoe_x1` ∩ Grafana đánh giá).
  - ×3: "sự cố trên giờ quan sát ×3 đủ điều kiện" (phút ×3 đủ điều kiện ∩ Grafana đánh giá). Câu "báo động giả mỗi giờ khỏe ×3" OPEN (Q-W6-10 cũ, nay câu 10 ở `cau-hoi-minh-4.md`).
  - Precision báo **riêng theo mức tải**; FP chỉ đếm sự cố có t̂ trong phút đủ điều kiện của mức đó. Sự cố ở phút không đủ điều kiện: không vào tử, không vào mẫu; báo số lượng.
- Phương án khác: định nghĩa `khoe_x3` (cần căn cứ riêng cho từng chỉ tiêu theo tốc độ).

---

## 4. Phút Grafana không đánh giá (CX-15b N2)

Mọi mẫu số thời gian (giờ khỏe ×1, giờ quan sát ×3, đoạn âm) = **giao** của phút đủ điều kiện tải với phút Grafana thực sự đánh giá luật, theo đúng quy tắc T-072 đã dùng cho R5 (`results/T-072/quy-tac-gom.json`, mục loại phút không đánh giá; áp ở E4: `bang-bao-dong-gia.md` "Mẫu số"). Báo riêng thời lượng bị loại vì Grafana không đánh giá.

---

## 5. Adapter baseline (CX-15 điểm 3; CX-15b điểm 3: đúng)

Thay bản 3 §C.3 và bổ sung §C.1.

**Biên N/A.** Bản 3 dựng lưới 15 s neo theo epoch rồi chia N/A theo thời gian hàng. Phản ví dụ (CX-15): 14/17 mốc t của lượt chính T-069 không chia hết 15; ở `03573b63` (t = 1795085304) mẫu tại t rơi vào hàng 1795085295 < t, tức vào N. Quy tắc bản 4:
1. Chia mẫu **theo thời gian native** thành N = `[t−300, t)` và A = `[t, t+300)` (nửa mở; t̂ thay t ở chế độ (b)).
2. Trong mỗi nửa, dựng lưới bước 15 s **neo tại t** (hàng `t−300+15k` cho N, `t+15k` cho A); mỗi mẫu vào ô `[mốc, mốc+15)` chứa nó; nhiều mẫu một ô → mẫu native muộn nhất; ghi số ô trùng.
3. Sau đó mới áp quy ước P3 của BARO (bản 2 §7.1: bỏ `_latency-50`, đổi `_latency-90`, ffill rồi 0). Quy ước P3 điền trên **cả** cửa sổ đã cắt (`src/p3/cua_so.py::tien_xu_ly_main` chạy sau khi cắt), nên ô trống đầu A có thể nhận giá trị cuối của N — giữ đúng như P3, ghi số ô được điền theo nửa. Thứ tự: cắt native `[t−300, t+300)` → lưới neo t → điền → BARO tự tách N/A theo cột `time` (lưới neo t bảo đảm không hàng nào chứa mẫu của nửa kia).

**SimpleRCA — ánh xạ trường, đơn vị, tên chuẩn trước khi cộng điểm:**

| Nguồn | Ra từ `m1.adapter_flashticket` | SimpleRCA `prepare` đòi | Đổi |
|---|---|---|---|
| metric | bảng thưa, mốc ns | `time` epoch giây | lưới như trên, `time` = giây |
| trace | `owner`, `start_us`, `duration_us` (`normalize_spans`) | `serviceName`, `startTime`, `duration` | đổi tên; đơn vị theo hợp đồng `prepare` (gói code kiểm trên dev; **CHƯA-KIỂM**) |
| log | `entity`, `timestamp` (ns), `message` (`normalize_logs`) | `container_name`, `timestamp` (giây), `message` | đổi tên; ns → giây |

- **Tên chuẩn:** hợp nhất **hai** bảng alias — tiền tố metric (`normalize_metrics`, dòng 126–134) và alias kiến trúc `ALIASES` (ví dụ `discovery-server → config-discovery`); M1 hợp nhất hai bảng ở `adapter_flashticket.py:292` (`aliases = dict(ALIASES, **metric_aliases)`) — rồi đổi mọi tên về tên chuẩn inventory **trước** khi SimpleRCA cộng phiếu các nguồn. Lý do: nếu cộng trước rồi mới đổi tên ở đầu ra, phiếu của cùng một dịch vụ đã bị chia ra hai thực thể; đổi tên sau không gộp lại được (CX-15 điểm 3). `simplerca.adapter.prepare` đã nhận tham số `aliases`.
- Ánh xạ ngược ở biên trả kết quả (bản 3 §C.1) vẫn giữ cho BARO (BARO chỉ có metric; tên cột theo tiền tố).
- Phép kiểm động trên 17 gói T-069 thuộc gói code W7 (chỉ tính toán).

---

## 6. Thời gian chụp gói (b) và D13 (CX-15 điểm 4; CX-15b điểm 4: đúng)

Bộ xuất của T-073 đã khóa: gói thu `[t̂−600, t̂+600)`, `flush_F` = 150 s, bắt đầu chụp ở t̂ + 750 s (`results/T-073/khai-truoc-e5.json` `#/N/thanh_phan_giay`; E5 thực: t̂ + 753 s). Ba mốc **tách riêng**, với cảnh báo muộn nhất còn ghép được (G1 = 370 s ⇒ t̂ ≤ S+1570):

| Mốc | Công thức | Cảnh báo muộn nhất | Vượt biên chu kỳ S+1800 |
|---|---|---|---|
| Hết dữ liệu lõi (A) | t̂ + 300 | S+1870 | 70 s |
| Hết gói thu | t̂ + 600 | S+2170 | 370 s |
| Bắt đầu chụp | t̂ + 750 | S+2320 | 520 s |

- **Chụp bất đồng bộ (ĐX):** bộ điều phối (b) của T-073 chạy như dịch vụ riêng, độc lập runner (E5: chạy liên tục, pid riêng). Runner W7 **không chờ** bộ chụp; chu kỳ kế bắt đầu như lịch. Chi phí thời gian chờ: 0.
- Hệ quả phải ghi: gói (b) của cảnh báo muộn chứa phần đầu chu kỳ sau (khoảng nghỉ giữa hai lượt tải và đoạn khởi động). Chỉ **A** (lõi) quyết định chất lượng RCA; phần gói ngoài A chỉ ảnh hưởng D13 và hiển thị.
- **Khoảng nghỉ giữa hai lượt tải:** chu kỳ đo 31,40 phút, tải 30 phút → khoảng ~84 s không tải sau S+1800 (suy từ thời lượng; **CHƯA-KIỂM** trực tiếp). A của cảnh báo muộn nhất có tới 70 s **không tải**. Cờ `A_vuot_bien_chu_ky` (bản 3 §A) ghi số giây A rơi vào khoảng không tải.
- **Phương án khác (câu 9 `cau-hoi-minh-4.md`):** kéo dài mỗi lượt tải thêm 90 s để A luôn dưới tải. Chi phí +90 s × số chu kỳ (57 chu kỳ: +85,5 phút; `du-toan-4.json`); đổi thời lượng tải so với dev và W4.
- **D13 (sửa bản 2 §2):** gói (b) lùi được tới t̂ − 600, nên biến thể nền lùi D13 khả thi với g ≤ 300 s mà không thu thêm; g > 300 s thì UNSUPPORTED.
- **×3:** `flush_F` = 150 s đủ dưới tải ×1 (E3, `khai-truoc-e5.json`: stage lại ở t̂+1199 s trùng sha256). Dưới ×3 **chưa đo** → pilot trước W7.

---

## 7. Diễn giải RQ5 và độ đo (CX-15 điểm 5; CX-15b điểm 5: đúng; tự soát N1, N4)

**Thay bảng §9.4 của bản 2.** Bảng cũ cho phép một kết quả hòa mọi ca thỏa cả cột "hỗ trợ" lẫn "không phân xử"; và "chuyển thẳng" so với dev (khác ô, khác DB, khác thời điểm) không phân xử được. Phản ví dụ đã lưu: ở `03573b63`, H8s1 bỏ 12 cờ nhưng hạng đáp án vẫn 3 (`results/T-069/dinh-chinh-1.md` §4, `phan-tich/bien-the/hang.txt`) — hòa hạng không có nghĩa thành phần không kích hoạt.

**Bảng bản 4 (mô tả, không có cột "hỗ trợ/bác bỏ" theo ngưỡng):**

| Câu | Báo gì | Không suy ra |
|---|---|---|
| RQ5 "chuyển thẳng" | Mức tuyệt đối của P7 trên ô đánh giá (AC@1/3, MRR, NDCG@5, K) theo ô, mức tải, chế độ. Số P7 trên ô dev (T-069) đặt cạnh làm **mô tả** | "giữ được/tụt" so với dev (không có khoảng dev khai trước) |
| RQ5 "sau thích nghi" | V082 so P7 **theo ca**: ba nhóm tách riêng — (i) cải thiện hạng, (ii) giữ hạng, (iii) tụt hạng; thắng/hòa/thua theo ô | "thành phần không tác dụng" từ nhóm (ii) |
| Thành phần có kích hoạt không | Từ trung gian mỗi ca: cờ đổi (`#/extra/kenh_co`), khóa đổi, chú thích (`chet_im`, nối chuỗi H8a, sàn H8s1) | — |
| Thông tin nào mang thay đổi | V082 so V082-che từng nhóm, theo ca, kèm trung gian (bản 3 §E) | "còn dẫn xuất" từ khác biệt với P7 |
| So baseline | V082, P7, SimpleRCA, BARO theo ca và theo ô; mô tả | cơ chế (bản 3 §G) |
| Lợi của dùng quan hệ trong xếp hạng | §12 | vùng ảnh hưởng, vai trò đồ thị trong báo động, topology thật |
| Giá của tự phát hiện | (b) so (a) cùng phương pháp; theo nhóm giây N nhiễm lỗi (dưới) | — |

**N nhiễm lỗi ở chế độ (b) (tự soát N1; D3 của T-043):** ở (b), N = `[t̂−300, t̂)`; với ca lỗi t̂ ≥ t nên N luôn chứa `min(t̂ − t, 300)` giây của đoạn lỗi (E5: 60 s). Mỗi ca (b) ghi `giay_N_nhiem = min(t̂ − t, 300)`; báo xếp hạng (b) theo ba nhóm 0–60 / 60–180 / ≥ 180 s. Với G1, cảnh báo muộn (t̂ ≥ t+300) có N nằm trọn trong đoạn lỗi.

**Đoạn N ngắn (tự soát N2):** bộ phân loại T-071 thiết kế cho lượt 30–60 phút; áp cho đoạn N 8 phút sau khởi động chưa kiểm. Pilot: chạy bộ phân loại trên đoạn 10 phút đầu của lượt E4 đã lưu, đếm phút bị xếp `bien` hay khác — chỉ tính toán.

---

## 8. Dự toán (CX-15 điểm 6; CX-15b điểm 6, N4)

`du-toan-4.json` (sinh bằng `du_toan_4.py`) **tự đủ**: không kế thừa mục nào của `du-toan.json` hay `du-toan-3.json`; danh sách mục cũ hết hiệu lực ghi đích danh trong `#/het_hieu_luc` (gồm `du-toan.json#/loi_giua_chung/loi_khoi_phuc_K2` 6–9 chu kỳ, `#/viec_them/E6_tuy_chon_phan_xu_T069`, `#/viec_them/K2_khoi_phuc_moi_khoi`, `#/viec_them/E6_do_khoi_phuc`; `du-toan-3.json#/loi_K2_moi_khoi/ghi_chu` "11–20").
- Kích thước khối và phạm vi mất khi khôi phục hỏng lấy từ **dòng phương án đã chọn** (9–20 chu kỳ tùy dòng).
- **Sức chứa:** K0 so nhu cầu cả đợt với vé còn; K2 khôi phục tồn kho về cùng mốc trước mỗi khối nên so **nhu cầu khối lớn nhất** (= cả đợt ÷ 3; phương án lớn nhất 25.488 vé) — chỉ dùng cột K2 sau khi E6 xác nhận khôi phục tồn kho nhất quán (CX-15b N4).
- Chi phí chờ gói (b) tách khỏi giờ thu cơ sở: 0 khi chụp bất đồng bộ; +90 s/chu kỳ nếu chọn kéo dài tải (§6).
- E6: theo `e6-spec-nhap.md` (bỏ một giờ "phân xử T-069" đã rút ở bản 3 §G).

---

## 9. Mốc của độ trễ (CX-15b N1)

Runner đặt `t = S + 600` **trước** khi gọi bộ tiêm (`runner4.py:260`); ở RECREATE-PAY của T-069, bộ tiêm ghi xong lúc t + 6,675 s (`results/T-069/thu/t069-chinh/so.jsonl`). Trường `t` là **mốc tiêm theo lịch**, không phải giây tác động bắt đầu. Bản 4:
- Số chính: **"độ trễ từ mốc tiêm theo lịch"** = t̂ − t.
- Ghi riêng mỗi ca: giờ bộ tiêm báo xong (`fault-start` trong sổ) và độ lệch so với t; báo phụ "độ trễ từ lúc bộ tiêm xác nhận".
- Ghép cửa sổ (bản 3 §A) vẫn theo t (khai trước, không đổi).

---

## 10. BARO trên ca khỏe (CX-15b N3)

Bản 2 §7 mục 4 đòi "hai cửa sổ đều bình thường không 'tìm ra' nguyên nhân". BARO **luôn** trả thứ hạng khi còn cột sau tiền xử lý (N = A = `[1,2,3]` vẫn cho `OK`; `e2e/baro.py:45`; adapter `src/p3/adapters/baro.py:44`). Tiêu chí đó không áp được cho BARO. Bản 4:
- BARO là phương pháp **chỉ xếp hạng**; K (kết luận ca khỏe) của BARO ghi `UNSUPPORTED`, không tính 0 hay 1.
- Phép kiểm không nhãn của BARO: cột vào/ra từng bước (bản 2 §7.1 bước 8); điểm và thứ hạng dựng lại khớp thứ tự chính thức (`key_check` của adapter); thứ hạng không trùng thứ tự cột; chạy lại ra cùng kết quả.
- Không thêm ngưỡng từ chối cho BARO: đó là biến thể mới, không còn là baseline của tác giả.
- SimpleRCA có `abstain` khi toàn 0 → K áp được.

---

## 11. Căn cứ chọn baseline (CX-15b N5)

- **Bỏ** số công bố 0,80 (top-1 SimpleRCA trên RE2-TT, bài FSE 2026) làm căn cứ cho độ mạnh của M4. WHY-17 ghi M4 là bản cài độc lập theo mô tả bài, chưa tái lập đúng chương trình tác giả; số của bài không nói về bản cài này, cũng không nói về FlashTicket.
- **Đề xuất (câu 7):** M4 (SimpleRCA, quy ước T-017) + BARO RobustScorer (RCAEval `259ea41`). Lý do: đúng §8.3; một baseline đơn giản đa nguồn (metric, trace, log, không dùng đồ thị) và một baseline metric đã công bố; cả hai đã có adapter P3 và đã chạy trong P3/P7 trên dữ liệu công khai, chi phí adapter FlashTicket thấp.
- **Mặt trái:** không có baseline dựa trên trace hoặc đồ thị độc lập (MicroRank, TraceRCA). Vì vậy W7 không đối chiếu được V082 với một phương pháp cùng họ dùng trace/quan hệ trên FlashTicket; câu "V082 so với phương pháp đồ thị đã có" chỉ trả lời được trên dữ liệu công khai (P7).
- Phương án khác: thêm MicroRank hoặc TraceRCA (adapter FlashTicket chưa ước lượng; không tốn giờ máy thu vì chạy trên gói đã niêm).

---

## 12. Phạm vi RQ3d (CX-06, CX-08; thay bản 2 §3.4 phần diễn giải)

- `DC-bo-quan-he` tắt E1, E2, E5 trên **cùng đầu vào** (span, log, metric, định danh thực thể, đặc trưng đã dựng giữ nguyên; `src/m1_ft/thanh_phan/dc_bo_quan_he.py`). V082 so `DC-bo-quan-he` trả lời: **các bước dùng quan hệ có tác dụng gì trong xếp hạng**.
- C-d1 dùng cạnh gọi giữa các nút có cờ; C-d2 chỉ xếp theo khởi phát và khóa nút, **không** dùng cạnh; C-d3 dùng đường đi có hướng và có thể trả `NO_TARGET` hoặc `UNSUPPORTED_CYCLIC` (`src/m1/doi_chung.py`). Báo số ca mỗi trạng thái của C-d3; C-d2 không tính là "quy tắc đơn giản trên cùng đồ thị".
- **Không trả lời:** độ đúng vùng ảnh hưởng; vai trò của đồ thị trong phát cảnh báo (M-20 hoãn); ưu thế của topology thật (không có đối chứng đồ thị ngẫu nhiên, M-25).

---

## 13. WHY đề xuất chịu ảnh hưởng (thay phần tương ứng)

- **W6-G (bản 4):** bù chỉ khi xác nhận chưa tiêm; mất phản hồi → giữ, kiểm sạch đúng container trước chu kỳ kế; bộ tiêm kiểm sạch mọi container/proxy/cgroup của ô đánh giá.
- **W6-I (bản 4):** mức tải phút từ lịch thực chạy; ×3 có điều kiện nhận riêng, báo "sự cố trên giờ quan sát ×3"; mẫu số thời gian ∩ phút Grafana đánh giá; Precision riêng mức tải; độ trễ từ mốc tiêm theo lịch; `giay_N_nhiem` cho (b).
- **W6-K (bản 4):** cắt native nửa mở rồi lưới neo tại t/t̂; SimpleRCA đổi trường, đơn vị, hợp nhất hai bảng alias trước khi cộng phiếu; BARO chỉ xếp hạng, K = UNSUPPORTED; bỏ 0,80 làm căn cứ M4.
- **W6-F (bản 4):** chụp (b) bất đồng bộ, ba mốc tách; D13 khả thi g ≤ 300 s.
- **W6-M (bản 4):** phạm vi RQ3d như §12.
- **Bảng diễn giải (mới, W6-N):** bản 4 §7 thay bản 2 §9.4; mô tả theo ca và ô, tách cải thiện/giữ/tụt và kích hoạt thành phần; không suy theo ngưỡng chưa khai.

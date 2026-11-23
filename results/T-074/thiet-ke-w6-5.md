# T-074 — Thiết kế W6, bản 5 (phần khóa W7)

- **Soạn:** Claude, phiên `danh-gia-w6`, 23/11/2026. Không máy, không subagent, không commit.
- **Cách đọc:** bản 5 = bản 4 (`thiet-ke-w6-4.md`, cùng bản 2–3 theo bảng §0 của bản 4) + các mục thay dưới. Bản 1–4 giữ nguyên (`SHA256SUMS` … `-4`).
- **Tách phần:** việc **cần cho E6** (máy) nằm ở `e6-spec-nhap-2.md`. File này chỉ gồm phần **khóa W7**, **không chặn E6**.
- **Nguồn sửa:** tự soát S4, S5 (LOG phiên 5); Codex CX-29 #3–#7, mục E5, và CX-29b (ba điểm mới). Bảng đáp từng điểm ở LOG phiên 5.
- **Trạng thái:** đề xuất. Quyết định cần Minh: `cau-hoi-minh-5.md` (phần B).

## 0. Mục hiệu lực thay đổi so với bản 4

| Chủ đề | Hiệu lực ở |
|---|---|
| E6 | `e6-spec-nhap-2.md` (thay `e6-spec-nhap.md`) |
| N nhiễm lỗi chế độ (b) | §1 (thay bản 4 §7 đoạn "N nhiễm lỗi") |
| D13 | §2 (thay bản 4 §6 dòng D13) |
| Đường thu T1(a), T1b, pilot ×3 | §3 (thay bản 4 §6 "Chụp bất đồng bộ" và bổ sung bản 2 §8.2) |
| Adapter SimpleRCA, nghiệm thu BARO | §4 (thay bản 4 §5 bảng SimpleRCA, §10 mục 2) |
| Bù ca | §5 (thay bản 4 §2 dòng "Xác nhận chưa tiêm") |
| CPU-EVENT | §6 |
| Dự toán khi kéo dài tải | §7 (bổ sung `du-toan-4.json#/cho_goi_b`) |
| Dữ liệu E5 | §8 (thay bản 4 §1 đoạn E5) |
| Giới hạn RQ5/DT18 | §9 |
| WHY | §10 |

---

## 1. N nhiễm lỗi ở chế độ (b) (tự soát S4; CX-29 #3: đúng)

Bản 4 dùng `min(t̂ − t, 300)`: sai khi t̂ > t + 600 (ví dụ t̂ = t+900 → N = `[t+600, t+900)`, giao với khoảng tiêm theo lịch 0 s, công thức cho 300 s).

**Bản 5:**
- `giay_N_nhiem_lich = max(0, min(t̂, t+600) − max(t̂−300, t))` — giao của N = `[t̂−300, t̂)` với khoảng tiêm **theo lịch** `[t, t+600)`.
- `giay_N_nhiem_xn = max(0, min(t̂, t_stop) − max(t̂−300, t_start))` — với khoảng **theo mốc bộ tiêm xác nhận** (`t_start` = giờ `fault-start` ghi xong; `t_stop` = giờ `fault-stop` hoặc tự gỡ). Thiếu một mốc → ghi `null`, không suy.
- Tính **sau khi** đầu ra đã băm (bộ chấm; đọc sổ).
- Nhóm báo cáo không chồng biên: `0`, `(0, 60]`, `(60, 180]`, `(180, 300]`.
- Dư âm sau gỡ (tín hiệu còn lệch sau `t_stop`) không tính vào giao; nếu muốn xét cần bằng chứng tín hiệu riêng — ghi OPEN.
- **Tách hai loại N:** N dùng để **xét ca hợp lệ** là nền trước tiêm `[S+120, t)` (§8.4 bản 2 điều kiện 3; bản 4 §3 cho ×3). N quanh t̂ dùng cho **phương pháp**. Không loại ca (b) vì suy giảm sau tiêm — đó là thứ phép so (a)/(b) phải đo.

## 2. D13 (tự soát S5; CX-29 #4: đúng)

D13 (T-043 SPEC dòng 329, 344) neo nền lùi tại `t_p` (lần đầu luật rời Normal, thường là Pending): `N′ = [t_p − g − 300, t_p − g)`.

| Nguồn | Khoảng có | Điều kiện hỗ trợ D13 |
|---|---|---|
| Gói cơ sở (W5: `[t̂−600, t̂+600)`) | trace, log, metric M1 | `g + (t̂ − t_p) ≤ 300` |
| Gói bổ sung (W5: `xuat_bo_sung --t t̂`, ±300 quanh t̂; `xuat_bo_sung.py:103`; E5 `prometheus-bo-sung.json#/cua_so`) | kênh liveness H5 | cần `t_p − g − 300 ≥ t̂ − 300`, tức `g ≤ t_p − t̂ ≤ 0` → **không bao giờ** với g > 0 |

- `t_p` lấy từ lịch sử trạng thái Grafana (`grafana.db`, chỉ đọc, như T-072 E4); `startsAt` của webhook là t̂, **không** phải `t_p`. Thiếu lịch sử Pending → `UNSUPPORTED`.
- P7, SimpleRCA, BARO: `SUPPORTED` khi điều kiện gói cơ sở đạt và có `t_p`; baseline dùng **cùng** N′.
- V082 và bản che có H5: `UNSUPPORTED` cho D13 (nới gói bổ sung rồi đưa vào H5 là đổi hành vi bản khóa — H5 đọc cả mẫu biên phải, `h4_h5.py:119`).
- D13 vẫn là **dòng độ nhạy tùy chọn**; không chặn D14 chính.

## 3. Đường thu W7 (CX-29 #5: đúng một phần; CX-29b mới #1)

**T1(a) — mọi chu kỳ đã phát tải đều được chụp gói.** `runner4.py:275–278` bỏ hàng đợi khi `fault_ok = False` (`m1-skipped`), nên ca "chưa xác nhận" mất gói. Runner W7: kích hoạt chụp **theo chu kỳ đã phát tải**, không theo `fault_ok`; ghi trạng thái tiêm (xác nhận / chưa xác nhận / xác nhận chưa tiêm) **riêng** trong sổ.

**T1b — niêm cả hai gói trước mọi phương pháp.** Tuyến E5 (`81a9273`, `orchestrator.py`) chạy `stage → P7 → bổ sung → V082 → kiểm → G1`; lỗi P7 chưa phân loại xảy ra **trước** bước bổ sung làm mất gói bổ sung. Bản 5: bộ chụp W7 (dùng bộ gom và bộ xuất của W5) chạy `stage` + `xuat_bo_sung` → **niêm** (manifest, sha256) → rồi mới đến bất kỳ phương pháp nào (P7, V082, G1 thuộc tuyến riêng sau đó). Gói code W7 sửa thứ tự này; T-074 chỉ khai yêu cầu.

**Chi phí chờ:** runner **không chờ** nối tiếp bộ chụp → 0 giờ cho phần chờ nối tiếp. Độ trễ hàng chờ của bộ chụp khi nhiều sự cố gần nhau và việc capture giữ đủ ở ×3 (`flush_F`) **chưa đo** → pilot. Mốc `t̂ + 750` (S+2320 với cảnh báo muộn nhất) là lúc **sớm nhất** có thể bắt đầu chụp, không phải lúc chụp thực.

**Pilot ×3:** `runner4.py::chay_d2` gọi `start_load(...)` không truyền `mult` → mặc định ×1. Gói code W7 thêm tham số mức tải cho pilot và kiểm **hệ số thực chạy** từ đầu ra k6 (tốc độ yêu cầu) trước khi nhận pilot.

## 4. Adapter baseline (CX-29 #6: đúng)

**SimpleRCA:**
1. Ánh xạ tên về tên chuẩn inventory (hợp nhất `ALIASES` và alias tiền tố metric, như M1 `adapter_flashticket.py:292`) **trước** `prepare`, và truyền `aliases` vào `prepare`.
2. Sau `diagnose`, **giữ nguyên** tên thực thể chuẩn ở cả `items` và `observed_entities`. **Không** gọi `thuc_the_metric` lên tên thực thể như wrapper P3 hiện làm (`src/p3/adapters/simplerca.py`: `thuc_the_metric(s)` → `booking_db` thành `booking`). Wrapper FlashTicket là bản mới, không tái dùng nguyên đoạn cuối của wrapper P3.
3. Đơn vị (đã xác định tĩnh): `startTime` là µs epoch (`src/simplerca/adapter.py:61–65` chia 1e6 và kiểm); `normalize_spans` trả `start_us`, `duration_us` → giữ µs. `duration` dùng tỉ số P95 sự cố/nền nên không phụ thuộc đơn vị. Log `timestamp` ns → giây.
4. Đối chiếu tên qua cả `items` lẫn tập quan sát trước khi chấm.

**BARO — tiêu chí nghiệm thu:** điểm và thứ hạng dựng lại khớp kết quả chính thức, gồm quy tắc hòa (sắp giảm dần theo điểm, ổn định khi hòa; `e2e/baro.py`); chạy lại cùng kết quả; danh sách cột từng bước (bản 2 §7.1 bước 8). `rank_equals_column_order` **chỉ là chẩn đoán**, không là tiêu chí trượt (một cột, điểm hòa, hoặc cột vốn theo thứ tự điểm đều trùng hợp lệ).

## 5. Bù ca (CX-29 #7: đúng)

| Bằng chứng | Xử lý |
|---|---|
| **Phía đích xác nhận chưa tác động, theo loại can thiệp và thời điểm** — ví dụ: bộ tiêm báo lỗi ở bước **trước** lệnh tác động (Toxiproxy trả lỗi khi tạo toxic; `docker pause` rc ≠ 0 và `State.Paused=false` đọc ngay sau lệnh; lease hook không được ghi; tiến trình đốt không khởi chạy) | bù 1 lần bằng lịch con |
| Chỉ có đầu dò sạch **sau** hạn tự gỡ | **không bù**; giữ ca ở nhóm "chưa xác nhận"; đầu dò sạch chỉ dùng để **quyết định chạy chu kỳ kế** |
| Mất phản hồi, không rõ | như dòng trên |

Gói code W7: bộ tiêm ghi rõ **giai đoạn** lỗi (trước/sau lệnh tác động) trong đầu ra `start`, để có bằng chứng dòng 1. `StartedAt` không dùng để phân biệt (pause không đổi `StartedAt`).

## 6. CPU-EVENT (CX-29b mới #2: đúng)

Ở `407b4f5`, kiểu `cpu` của `inj3.py` đốt bằng `docker exec -d BOOK …` (dòng 115–117); kiểm sạch đếm luồng đốt trong `BOOK` (dòng 286). Thêm quota Event và mục ô mới **không đủ**: tải vẫn đặt lên Booking, nhãn ô sai. Gói code W7 phải tham số hóa container cho cả **đốt, gỡ, đầu dò throttle, kiểm sạch**. Chưa có đường đó → CPU-EVENT giữ trạng thái **ứng viên**, không vào ma trận chạy. Câu B1 `cau-hoi-minh-5.md`.

## 7. Nhu cầu vé khi kéo dài tải +90 s (CX-29b mới #3: đúng)

`du_toan_4.py` cộng 90 s vào giờ nhưng giữ nguyên số đơn: sai. Tính lại theo thời lượng và mức tải cuối mỗi lượt (×1: 0,36 đơn/s; ×3: 1,08 đơn/s; flash: 600 s ×1 + 1.290 s ×3), lệnh python ghi ở LOG phiên 5:

| Phương án | K3 | Đơn bảo thủ (tải 1.800 s, `du-toan-4.json`) | Đơn bảo thủ (tải 1.890 s) |
|---|---|---|---|
| A | dùng lại | 35.640 | 37.487 |
| A | thêm 3 mốc | 37.584 | 39.528 |
| A + CPU-EVENT | dùng lại | 43.416 | 45.652 |
| A + CPU-EVENT | thêm 3 mốc | 45.360 | **47.693** (vượt 46.402) |
| A + B | dùng lại | 66.744 | 70.146 |
| A + B | thêm 3 mốc | 68.688 | 72.187 |
| A + B + CPU-EVENT | dùng lại | 74.520 | 78.311 |
| A + B + CPU-EVENT | thêm 3 mốc | 76.464 | 80.352 |

Khi chốt sức chứa ở E6, dùng tồn kho đọc thật (`e6-spec-nhap-2.md` §4). Đề xuất vẫn là **không** kéo dài tải (câu B2).

## 8. Dữ liệu E5 — đính chính bản 4 §1 (CX-29 mục E5, CX-29b N4–N7)

- t̂ − `fault-start` = **55,767 s** (`results/T-073/dap-cx21/dinh-chinh-e5-1.md`), không "60 s".
- Mốc hiện ca Minh nhận (Q2): cận trên **898,8 s** sau t̂, không "14,8 phút (API)".
- Thiếu phủ Payment: CPU/mem lỗ **364,999 s**, bốn kênh HTTP lỗ **315 s** (`results/T-073/e5/su-co/bbc0a6d44f.json#/du_lieu_loi/phu/nguon`), không một số 365 s cho sáu kênh.
- Tập ứng viên: P7 có 16 thực thể (thiếu `payment-service`); V082 có 17 (Payment ở `tie_group` 6). Diễn giải luôn ghi rõ bản phương pháp.
- H5 không nâng Payment ở ca này vì N đã có 3 mẫu `live-down` = 1 (t̂ − 45, −30, −15 s) — điều kiện nền H5 loại Payment trước khi xét A. **W7 ghi trạng thái điều kiện nền H5 mỗi ca** khi so (a)/(b) và bản che. Nguyên nhân Booking hạng đầu vẫn OPEN.
- W7 dẫn hash đầu ra từ hiện vật của chính lượt W7 (Q6 đã xử lý chú thích demo).

## 9. Giới hạn RQ5 và DT18 của phạm vi đề xuất

Nếu Minh chọn A + CPU-EVENT (hoặc A): bằng chứng "vị trí mới" chỉ cho các ô đó. **Không** có ô cạnh mạng/dữ liệu/cache ở vị trí mới, lỗi phụ thuộc (DB, Redis đích), bù trừ Saga, hoặc tải tăng ngay trong một ca lỗi. Hồ sơ G6 phải ghi rõ giới hạn này (DT18-NV3 "phân tích các trường hợp … còn hạn chế").

## 10. WHY đề xuất chịu ảnh hưởng

- **W6-I (bản 5):** hai độ dài giao N (lịch / xác nhận), nhóm không chồng biên, tính sau băm; N xét ca là nền trước tiêm.
- **W6-F (bản 5):** chụp mọi chu kỳ đã phát tải; niêm gói cơ sở và bổ sung trước mọi phương pháp; pilot ×3 có kiểm hệ số thực; D13 theo điều kiện §2.
- **W6-K (bản 5):** wrapper SimpleRCA mới giữ tên chuẩn sau `diagnose`; BARO nghiệm thu bằng dựng lại điểm/thứ hạng/hòa.
- **W6-G (bản 5):** bù chỉ khi phía đích xác nhận chưa tác động theo loại và thời điểm.
- **W6-B (bản 5):** CPU-EVENT là ứng viên cho tới khi bộ tiêm tham số hóa container.

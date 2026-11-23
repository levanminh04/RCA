# Hợp nhất phản biện Codex vòng A/B (CX-13…CX-16b) — điều phối T-070

Lập 22/11/2026 ~19:15Z (phiên điều phối, Claude). Theo yêu cầu của Minh 22/11: hai phiên Codex phản biện lần lượt, độc lập; Claude tham gia sau để thống nhất. Tài liệu này **không** là phản hồi của người làm các task: T-066, T-068, T-074 vẫn cần lượt "người làm đáp phản biện" (Minh chuyển prompt), T-073 cần sửa trước E5. Điều phối chỉ kiểm chọn lọc trên file (cột "Điều phối kiểm").

Nguồn: `results/T-070/codex/CX-1{3,4,5,6}-tin-cuoi.md` (phiên 1) và `CX-1{3,4,5,6}b-tin-cuoi.md` (phiên 2).

**Đính chính đầu vào:** `CX-15.jsonl` và `CX-15-tin-cuoi.md` bản trước là chữ loạn (UTF-8 bị đọc thành cp437 khi chuyển từ UTF-16 do `Start-Job`). Đã khôi phục từ `CX-15.utf16-goc.jsonl` (UTF-16 → cp437 → UTF-8; 92 dòng JSON hợp lệ, có `turn.completed`); bản loạn giữ ở `CX-15.mojibake.jsonl`, `CX-15-tin-cuoi.mojibake.md`. CX-15b đã đọc bản loạn nhưng đối chiếu được đủ sáu điểm của phiên 1.

## 1. T-066 (W1, repo lab, dựng lại máy) — CX-13, CX-13b

| Điểm | Phiên 1 | Phiên 2 | Điều phối kiểm | Trạng thái |
|---|---|---|---|---|
| R1 manifest, R2 STOP/PyYAML, R4 thứ tự phát lại, R5 `XONG` | Đúng, đã xử lý / không chặn | Đúng | — | Thống nhất; không còn việc |
| R3a sáu đầu ra `gia*` đã xóa | CHẶN kết luận "không còn căn cứ nhận diện" | Đúng | — | Người làm sửa câu kết luận thành ba mức bằng chứng |
| R3b xóa 2.6/2.7 sau T-067 | CHẶN | Đúng | — | **Minh quyết**: giữ 2.6 tới khi quyết CLI `fixture.py`; 2.7 xét từng script; đồng bộ dòng STATE |
| README "hành vi lệnh không đổi" | Không chặn | Đúng một phần | — | Lỗi nhỏ, cần commit lab nếu sửa |
| Tempo "chỉ có tăng" | Không chặn | Đúng | — | Lỗi nhỏ, đính chính câu |
| **Mới: liên kết Grafana `live-down`** | — | CHẶN dùng liên kết làm bằng chứng; không chặn hồi quy W1 | **Đúng.** `xuat_bo_sung.py` (ab1c52c) trả `query=MO_TA_R9` (câu mô tả); `l8b-xuat.py` dùng nguyên `q['query']` làm biểu thức Prometheus của liên kết | Người làm; sửa G1 cần commit lab mới (file đã ghim T-067). **Ảnh hưởng E5:** liên kết metric `live-down` trên trang ca mới sẽ hỏng → ghi là giới hạn đã biết khi kiểm dashboard ở E5, không tính là lỗi tuyến mới |

Hai phiên đồng ý chấp nhận kết quả kỹ thuật W1, giữ mở R3a, R3b, `live-down`.

## 2. T-068 (dọn, dựng lại Grafana) — CX-14, CX-14b

| Điểm | Phiên 1 | Phiên 2 | Điều phối kiểm | Trạng thái |
|---|---|---|---|---|
| F1 "trang DB có bằng chứng cờ M1" | CHẶN | Đúng; tái lập dãy 30/15/14/11/3 là đếm theo `co_m1[].ten`, còn panel lọc theo `thuc_the` → 0/84 | — | Người làm đính chính báo cáo; giữ link theo quyết định Minh |
| F2 lý do bỏ `dv=__khong_co__` (WHY-101) | CHẶN | Đúng | — | Đính chính WHY-101 (cần Minh duyệt ghi WHY) |
| F3 đề xuất xóa bản hoàn tác | CHẶN | Đúng | — | **Minh quyết**: giữ bản hoàn tác |
| F4 ba cam kết kỹ thuật; F5 STATE | Không chặn | Đúng | — | Lỗi nhỏ |
| **Mới N1: mốc "trước khi xóa"** | — | CHẶN xác nhận thứ tự kiểm rồi xóa | **Đúng.** `truoc/grafana-truoc.json` ghi `utc_chup "02:3xZ"` còn `thay-doi-may.md` ghi xóa 02:22–02:28 | Người làm: đối chiếu dấu thời gian API gốc nếu còn, nếu không ghi giới hạn |
| Mới N2 dựng riêng P7; N3 RabbitMQ | — | Không chặn | — | Lỗi nhỏ, ghi giới hạn |

## 3. T-074 (W6 bản 3) — CX-15, CX-15b

Hai phiên thống nhất: bản 3 sửa đúng D14, bỏ hai suy luận cơ chế, dự toán 8/8 phương án đúng (46.402 vé theo mô hình). Chưa khóa W7 được.

| Điểm | Phiên 1 | Phiên 2 | Trạng thái |
|---|---|---|---|
| 1 `fault-start-failed` và Ticket | CHẶN | Đúng một phần (bộ tiêm có hẹn giờ `stop`; hở khi hẹn giờ/gỡ hỏng, `verify` chỉ kiểm Payment) | Người làm |
| 2 tải ×3 | CHẶN | Đúng một phần | Người làm |
| 3 adapter baseline (lưới 15 s, SimpleRCA alias/đơn vị) | CHẶN | Đúng | Người làm |
| 4 thời gian chụp gói (b) | CHẶN | Đúng | Người làm |
| 5 diễn giải RQ5 | CHẶN | Đúng | Người làm |
| 6 hiệu lực JSON dự toán | CHẶN ngân sách khi lỗi | Đúng | Lỗi nhỏ |
| Mới N1 mốc tiêm R-07 (lệch 6,675 s) | — | CHẶN diễn giải độ trễ sát biên | Lỗi nhỏ |
| Mới N2 phút Grafana không đánh giá | — | CHẶN tỷ lệ báo động W6 | Lỗi nhỏ; **khớp quy tắc T-072 dùng cho R5 ở E4** |
| Mới N3 BARO trên ca khỏe | — | CHẶN nghiệm thu BARO theo tiêu chí hiện tại | Người làm |
| Mới N4 sức chứa K2 theo khối | — | CHẶN dùng bảng chốt sức chứa K2 | Người làm |
| Mới N5 căn cứ baseline mạnh (0,80 của bài báo) | — | CHẶN lấy 0,80 làm bằng chứng về M4 | **Minh quyết** (Q-W6-07) |

Còn giao chưa làm: phạm vi RQ3d (CX-06). Không chặn W4/W5/E5.

## 4. T-073 (hướng dẫn chạy E5) — CX-16 (sửa), CX-16b (kiểm)

CX-16 chỉ sửa `results/T-073/trien-khai-e5.md` (bản cũ `trien-khai-e5.truoc-cx16.md`); N = 25 phút, tiêu chí, ô không đổi; hai file khóa khớp hash.

| Điểm CX-11/12 | CX-16b |
|---|---|
| 1 K8 sau S4-8; 2 I7 mỗi lần đổi checkout; 3 tách `inj3` S4-1a; 4 mốc cuối E4 trước Test; 6 ô `PAUSE-PAYMENT` | ĐẠT |
| 5 dashboard | CHƯA ĐẠT khi triển khai: S4-7 dùng "provider tạm" cho `90-archive/` nhưng chưa chỉ commit nào chứa provider đó (máy chủ chỉ dùng cấu hình từ commit) |
| Còn lại S4-6 | Giả định một lần bấm Test gửi tới cả hai integration; giao diện Grafana có thể thử từng integration → ghi rõ thử từng webhook, dùng tin phía T-073 cho K8 |

**Chặn phát E5** tới khi T-073 sửa S4-6, S4-7 (người làm T-073 quyết cách bật dashboard lưu trữ: thêm provider vào commit E5 hay commit riêng, và hoàn tác). Điều phối giao T-073 khi usage cho phép; Minh vẫn phải duyệt commit E5.

## 5. Việc tiếp theo theo người quyết

- **Minh:** R3b (T-066 xóa 2.6/2.7), F3 (T-068 giữ bản hoàn tác), N5/Q-W6-07 (T-074), duyệt commit E5 sau khi T-073 sửa; chọn chuyển prompt "người làm đáp phản biện" cho T-066 (`CX-13-tin-cuoi.md` dòng 67–135), T-068 (`CX-14-tin-cuoi.md` dòng 73…), T-074 (theo CX-15b) — kèm bảng phiên 2.
- **Người làm (Claude):** các dòng "Người làm"/"Lỗi nhỏ" ở trên, trong lượt đáp phản biện của từng task.

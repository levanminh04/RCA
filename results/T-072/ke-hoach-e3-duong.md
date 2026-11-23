# T-072 — Bằng chứng dương theo từng luật và kế hoạch tín hiệu dương E3 (đề xuất, điều phối duyệt trước E3)

Trạng thái 20/11 13:40Z. "Dương thật" = biểu thức luật (đúng chuỗi PromQL trong `bieu-thuc.json`) có điểm vượt ngưỡng thử trên dữ liệu đã ghi của một lỗi thật, chấm bằng `cham_offline.py`. Ngưỡng thử `kiem-code/nguong-thu.json` chỉ để kiểm code. Giờ lỗi lấy từ sổ T-069 chỉ để đối chiếu, không vào phương pháp.

| Luật | Thử giả (`tu-kiem`) | Dương thật đã có | Nguồn |
|---|---|---|---|
| t072-p95-booking | có | **chưa** | — |
| t072-p95-event | có | **chưa** (HTTP5-EVENT trả lỗi nhanh) | — |
| t072-p95-payment | có | có: PAUSE-PAYMENT, p95 tới 10 s | `kiem-code/cham-thu-pause.json` |
| t072-p95-ticket | có | **chưa** | — |
| t072-loi-booking | có | **chưa**: chưa từng có 5xx ở route `booking` từ lần khởi động gateway hiện tại (không có chuỗi 5xx, khảo sát 20/11) | — |
| t072-loi-event | có | có: HTTP5-EVENT `30ae6ac0`, 89 điểm, tỷ lệ tới 0,50; t̂ = lúc tiêm + 101 s, hết lúc gỡ + 271 s | `kiem-code/cham-thu-http5-event.json` |
| t072-loi-payment | có | có: PAUSE-PAYMENT, 50 điểm, tỷ lệ tới 1 | `kiem-code/cham-thu-pause.json` |
| t072-loi-ticket | có | **chưa**: như `booking` | — |
| t072-live | có | có: PAUSE-PAYMENT, t̂ = lúc tiêm + 30 s | `kiem-code/cham-thu-pause.json` |
| t072-mat-do | có | **chưa** (chưa có lần mất dò) | — |
| t072-mat-gw | có | **chưa** | — |

Năm luật p95/lỗi chưa có dương thật khác các luật đã có dương thật **chỉ ở giá trị nhãn `http_route`** (cùng hàm sinh trong `sinh_bieu_thuc.py`). Đó là căn cứ cấu trúc, không thay cho dương thật. `loi-booking`, `loi-ticket` còn chịu giới hạn "lần lỗi đầu của một tổ hợp (route, mã) mới": phần tăng trước mẫu đầu không thấy (`bieu-thuc.json#/khong_phu`).

## Đề xuất cho E3 (khung S2: exp-app nghỉ, không tải)

Vì không có tải ở S2, luật p95/lỗi thật không thể có điểm (chặn < 30 request). E3 vì vậy kiểm **đường ống Grafana**, không kiểm dương từng biểu thức:

1. Nạp 11 luật thật. Qua API trạng thái luật của Grafana: mỗi luật được đánh giá, `health` không lỗi; p95/lỗi ở Normal (NoData → OK); `t072-live` có 8 instance Normal; hai luật mất quan sát Normal. Ghi giờ hiệu lực.
2. Một luật thử tạm `t072-thu-e3` (thư mục riêng, `t072_loai = thu`, uid khác mọi luật thật), biểu thức `vector(1)`, ngưỡng > 0,5, `for` 20 s, cùng `notification_settings`. Bật trong ≈ 2 phút rồi gỡ. Kiểm: Pending → Alerting trong lịch sử trạng thái; webhook firing tới bộ nhận nhẹ; so `startsAt` với giờ chuyển Alerting trong lịch sử trạng thái (I1 `da_doi_chieu_E3`); gỡ → webhook resolved, so `endsAt`. Ngoài khoảng chấm; gỡ và ghi giờ trước khi mở S3.
3. So trạng thái luật thật với `cham_offline.py` trên chuỗi xuất cùng khung (chỉ có trạng thái Normal ở S2).

**Còn chưa kiểm dương sau E3** (ghi vào `e3.md`): `p95-booking`, `p95-event`, `p95-ticket`, `loi-booking`, `loi-ticket`, `mat-do`, `mat-gw`. Lần dương đầu có thể đến từ các ca tiêm của E5 (T-073) hoặc W6/W7. Muốn dương trước E4 thì cần tải và tiêm lỗi có kiểm soát ở S2, nghĩa là đổi khung S2 (exp-app đang nghỉ): đó là quyết định của điều phối và Minh, không làm khi chưa duyệt.

# Yêu cầu ô thật cho H8-adapter (phiên C → phiên B, T-063 thu bù)

Ghi 14/11/2026 ~05:50Z. Người ghi: phiên C (Claude, người làm T-064 phần H8). Phiên B **tự quyết** có thu kèm hay không, theo hồ sơ và lịch đợt thu của mình. File này không phải lệnh.

## Vì sao cần

- H8-adapter (`src/m1_ft/thanh_phan/h8_adapter.py`) xử lý trường hợp container bị tạo lại trong cửa sổ [t−600, t+600]. Khi đó adapter ghim của P7 ném `Multiple runtime series map to one logical metric` và **cả ca ERROR** (M1 không cho kết quả).
- Đếm trên 37 gói ca hiện có (`results/T-064/phien-c/h8-adapter/dem-chuoi-trung.json`): chỉ `thuong01` gặp tình huống này. Đó là ca chạy thử 11/11, container được tạo lại lúc triển khai, không có lỗi tiêm và thiếu log ứng dụng của container mới (KP-19). 22 ca của tập chọn và tập không hồi quy đều không có tình huống này.
- Vì vậy hiện chỉ kiểm được **cài đặt**: trên thuong01 P7 lỗi còn H8-adapter chạy được; ca tách giả trong test cho lại đúng đầu ra adapter. Muốn biết H8-adapter có cho **xếp hạng đúng** khi một thành phần bị tạo lại giữa sự cố hay không, cần ít nhất một ca thật có lỗi và có tạo lại container trong cửa sổ.

## Ô đề xuất

| Mục | Đề xuất |
|---|---|
| Tên ô (dev, mới) | `RECREATE-PAY` |
| Họ lỗi | container được tạo lại (triển khai lại / thay container) trong lúc chạy tải. Họ này không có trong `results/T-059/danh-muc-loi.json`. |
| Vị trí | `payment-service`. Đây là vị trí dev đã có (PAUSE-PAYMENT, họ khác). Không trùng gốc của ô đánh giá T-059: payment chỉ là bên gọi của NET-PAY-BOOK và VNPAY-REFUND-LAT (cạnh, họ khác). Phương án dự phòng: `user-service` (không là gốc ô nào của T-059), **chỉ khi** tải mua vé có gọi tới nó; phiên B kiểm. Tránh booking, event, ticket vì là gốc của nhiều ô đánh giá. |
| Cách tạo lại | Trên `exp-app`: `docker compose … up -d --force-recreate --no-deps payment-service`, đúng một lần, tại t (mốc phiên B ghi như ô khác). `container_id` mới; container cũ dừng. Không dùng `docker restart` vì nó giữ nguyên `container_id`, nên không tạo tình huống này. |
| Thời điểm | Tạo lại tại t, để cả container cũ (N) và mới (A) nằm trong [t−600, t+600]. Tải mua vé chạy suốt chu kỳ như các ô khác. |
| Tập chấp nhận (khai trước, phía chấm) | `payment-service`. |
| Đầu dò độc lập (ngoài dữ liệu RCA) | `docker inspect` trước/sau (Id, StartedAt); liveness `httpcheck` của payment; lỗi/timeout phía k6 trên route thanh toán. |
| Xác nhận khi | `container_id` của payment đổi đúng một lần trong [t, t+60]; liveness payment hụt trong lúc JVM khởi động rồi phục hồi. |
| Cần kiểm thêm | (1) Sau khi tạo lại, Collector filelog có thu log của container mới không (KP-19 từng mất log khi đường dẫn ghim theo ID container). Thiếu log thì ghi đúng thiếu gì. (2) `container_name` có đổi không (H8-adapter chấp nhận `container_id`, `container_name`, `service_instance_id` khác nhau). |

## Phiên C dùng ô này thế nào

- Chạy P7, V060 (P7 + H8-adapter), V032, V061 (V032 + H8-adapter) trên ca. Kỳ vọng tối thiểu: P7 ERROR, bản có H8-adapter chạy được. Phân xử thật: hạng của `payment-service`.
- Kết quả là **một ca, một lần thu**: chỉ cho bằng chứng có điều kiện, không đo được dao động.
- Nếu phiên B không thu, H8-adapter được ghi "đã cài, kiểm cài đặt; hiệu quả xếp hạng chưa thử được trên ca thật có lỗi", kèm phần thiếu là ô này.

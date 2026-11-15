# Xuất metric bổ sung của T-062 và sự cố Prometheus khởi động lại (12/11/2026 ~19:15Z = 13/11 02:15 giờ VN)

**Vì sao xuất.** Prometheus `exp-obs` chỉ lưu 2 ngày (`storage.tsdb.retention.time=2d`, đọc từ `/api/v1/status/flags`). Gói ca T-062 chỉ có 7 truy vấn metric. Mẫu của lượt E1 (bắt đầu ~19:06Z 11/11) sẽ bắt đầu bị xóa từ ~19:00Z 13/11. Minh duyệt tổng thể gói 13/11; Codex đề nghị tách việc này làm sớm.

**Đã làm.**
- `xuat.py` (chạy trên `exp-obs` qua `ssh … 'python3 -' < xuat.py`, chỉ đọc Prometheus, không ghi file trên máy): mẫu thô `<metric>[34200s] @ 1794450600` cho mọi tên metric trừ tiền tố `prometheus_`, `go_`, `promhttp_`. Cửa sổ 11/11 17:00:00Z → 12/11 02:30:00Z (D2 + E1).
- Kết quả `prometheus-tho-1794416400-1794450600.jsonl.gz` (56,6 MB): 217 tên metric, 10.496 chuỗi, 16.025.774 mẫu, mẫu đầu 1794416400.704, mẫu cuối 1794450599.953; 0 metric rỗng; **4 metric lỗi**: `traces_span_metrics_duration_seconds_bucket`, `…_count`, `…_sum`, `up`.

**Sự cố.** Truy vấn một phát 9,5 giờ của `traces_span_metrics_duration_seconds_bucket` làm kết nối bị đóng; ba truy vấn kế tiếp bị từ chối kết nối. `docker inspect flash-ticket-obs-prometheus`: `RestartCount=1`, `OOMKilled=false`, `StartedAt=2026-11-12T19:16:38Z`. Log: lỗi ghi lúc 19:16:33Z, "Server is ready" lúc 19:16:42Z, WAL phát lại xong. Tức Prometheus **tự khởi động lại một lần, gián đoạn khoảng 10 giây**. Nguyên nhân chính xác (hết bộ nhớ tiến trình hay giới hạn container) **chưa xác định**: `OOMKilled=false` nhưng thời điểm trùng truy vấn nặng; phân xử bằng `docker logs` trước 19:16:33Z và `dmesg` (chưa đọc).

**Ảnh hưởng.** Không có lượt thí nghiệm nào đang chạy. Có thể mất mẫu ghi vào trong ~10 giây đó (chưa đếm). Dữ liệu T-062 trước đó không bị ảnh hưởng (WAL phát lại). Loki, Tempo, Grafana không khởi động lại.

**Khắc phục.** `xuat-phan-con-thieu.py` xuất 4 metric lỗi theo **khúc 10 phút**, nghỉ 0,3 s giữa các khúc → `prometheus-tho-phan-con-thieu.jsonl.gz`; `prometheus-sau-xuat.txt` ghi `RestartCount` sau lượt này (phải vẫn là 1). Kiểm kết quả: `xuat-phan-con-thieu.rc.txt`.

**Bài học cho các lượt sau.** Truy vấn Prometheus trên `exp-obs` phải cắt khúc thời gian với metric nhiều chuỗi; bộ đóng gói mở rộng của T-063 xuất ngay sau mỗi chu kỳ (cửa sổ ngắn). Tăng retention trước đợt thu.

# T-072 — Đối chiếu bộ chấm offline với Grafana trên E3, theo từng UID

23/11/2026 (lượt 10, làm tiếp sau khi bị dừng nhầm 22/11 ~16:43Z). Bổ sung phép kiểm còn thiếu theo SPEC ("so trạng thái luật Grafana với bộ chấm offline"), Codex CX-12 nêu là CHẶN kết luận "bộ chấm offline khớp Grafana".

## Đầu vào (không dùng máy, không truy vấn Prometheus)

| File | Vai trò | sha256 (16 đầu) |
|---|---|---|
| `results/T-071/e3/xuat-tin-hieu.json` | chuỗi luật của lượt E3 do T-071 xuất (định dạng T072-xuat-1, 24 chuỗi, 0 khúc lỗi, lưới 05:15:26–06:00:26Z, bước 10 s) | trong `results/T-071/e3/SHA256SUMS` (5/5 OK) |
| `results/T-072/e3/b9-lich-su.json` | lịch sử trạng thái Grafana (bảng `annotation`, đọc chỉ đọc 22/11 06:03Z) | `124622904e526a7d` |
| `bieu-thuc.json`, `nguong.json` | luật, ngưỡng thật | `1a4aee67…`, `c8f44854…` |
| `cham_offline.py` | bộ chấm (chạy đúng code, nạp bằng `exec` bỏ dòng `main()` cuối) | trong `SHA256SUMS-e3-offline` |
| `e3_doi_chieu_offline.py` → `e3-doi-chieu-offline.json` | script đối chiếu và kết quả | trong `SHA256SUMS-e3-offline` |

Luật thử được dựng lại offline bằng bản sao 4 luật p95 với ngưỡng 0,005 s, đọc cùng chuỗi `tin-hieu/t072-p95-<route>` (đúng như `sinh_luat_thu_e3.py`: cùng PromQL, chặn ≥ 30 request, `for` 60 s, NoData → OK).

## Kết quả theo từng UID

| UID | Khoảng cháy offline / Grafana | Pending offline → Grafana | Alerting offline → Grafana | Hết offline → Grafana | Lệch (s) |
|---|---|---|---|---|---|
| t072-thu-p95-booking | 1 / 1 | 05:25:46 → 05:25:50 | 05:26:46 → 05:26:50 | 06:00:16 → 06:00:20 (NoData) | −4 / −4 / −4 |
| t072-thu-p95-event | 1 / 1 | 05:25:46 → 05:25:50 | 05:26:46 → 05:26:50 | 06:00:16 → 06:00:20 (NoData) | −4 / −4 / −4 |
| t072-thu-p95-payment | 1 / 1 | 05:27:36 → 05:27:40 | 05:28:36 → 05:28:40 | 05:58:26 → 05:58:30 (NoData) | −4 / −4 / −4 |
| t072-thu-p95-ticket | 1 / 1 | 05:27:36 → 05:27:40 | 05:28:36 → 05:28:40 | 05:58:26 → 05:58:30 (NoData) | −4 / −4 / −4 |
| 11 luật thật (`t072-p95-*`, `t072-loi-*`, `t072-live`, `t072-mat-do`, `t072-mat-gw`) | 0 / 0 mỗi luật | — | — | — | — |

Không khoảng offline nào bị cắt bởi lỗ dữ liệu (`cat = False`).

## Vì sao lệch đúng −4 s

- Lưới xuất của T-071 nằm ở pha …6 s (điểm 05:25:46, 05:25:56, …); Grafana đánh giá ở tick …0 s (05:25:40, 05:25:50, …). Mọi chuyển trạng thái offline rơi vào một điểm …6, Grafana thấy nó ở tick kế tiếp …0, tức muộn hơn 4 s. Với pha này lệch chỉ có thể là −4 s (chuyển trạng thái giữa …40 và …46) hoặc +6 s (giữa …46 và …50). Cả 12 phép so đều là −4 s, nghĩa là cả 12 thời điểm chuyển nằm trong (…40, …46].
- `for` 60 s: Alerting = Pending + 60 s ở cả hai phía, nên lệch Alerting bằng lệch Pending.
- Kết thúc: điểm offline đầu tiên thiếu chuỗi (chặn < 30 request) tương ứng NoData → Normal của Grafana (lý do ghi trong lịch sử: `Normal (NoData)`); cũng lệch −4 s.
- Không thấy dấu hiệu Grafana nhận mẫu trễ khác offline (độ trễ nạp mẫu lúc đánh giá): nếu có, Grafana sẽ chuyển muộn thêm ít nhất một tick (lệch ≤ −14 s); không xảy ra ở 12 phép so.

## Kết luận đúng mức bằng chứng

1. **Khớp dương (offline = Grafana, sai khác chỉ do pha lưới):** 4 luật thử, tức cơ chế luật p95 (chặn ≥ 30 request, ngưỡng, `for` 60 s, NoData → Normal) trên 4 route. Mọi chuyển trạng thái lệch đúng −4 s, nằm trong biên một nhịp đánh giá (10 s).
2. **Chỉ khớp âm (0 = 0):** 11 luật thật trong ~45 phút (05:15:26–06:00:26Z, gồm 30 phút tải ×1). Đây là đồng thuận "không cảnh báo", **không** chứng minh offline và Grafana khớp khi luật thật cháy.
3. **Chưa có so sánh dương offline ↔ Grafana** cho luật lỗi 5xx, liveness và mất quan sát. Ngoài ra, theo `ke-hoach-e3-duong.md`, **7 luật chưa kiểm dương** trên dữ liệu thật: `t072-p95-booking`, `t072-p95-event`, `t072-p95-ticket`, `t072-loi-booking`, `t072-loi-ticket`, `t072-mat-do`, `t072-mat-gw`. Các luật `t072-p95-payment`, `t072-loi-event`, `t072-loi-payment`, `t072-live` có dương thật trên dữ liệu T-069, nhưng chỉ ở bộ chấm offline, chưa so với Grafana.
4. Hệ quả cho chấm E4: với luật p95, sự cố đếm từ Grafana và từ offline phải trùng; khác biệt ≤ 10 s về t̂. Với luật khác, nếu E4 có cảnh báo thì phải so lại từng sự cố, không suy từ phép này.

## Quan sát phụ (không dùng để sửa ngưỡng)

p95 lớn nhất của chuỗi E3 (lượt ×1, khỏe): booking 0,0931 s (ngưỡng 0,098), event 0,0452 (0,097), payment 0,1450 (0,184), ticket 0,0650 (0,112). Giá trị booking 0,0931 là điểm đầu lượt (05:25:46, chặn vừa đạt 30 request), cách ngưỡng ≈ 5%; nó không cháy vì không giữ 60 s. Ghi để đọc kết quả E4, không đổi ngưỡng (ngưỡng khóa từ E2).

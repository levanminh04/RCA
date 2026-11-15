# Thử đường ống M1 trên dữ liệu T-062 (khám phá, không phải ca RCA)

- 19:52Z, mã `thuong01`, t = 2026-11-11T19:02:40Z (giữa lượt chạy thử 5 phút của Codex). Gói tạo trên exp-obs (`/opt/flash-ticket-rca/cases/thuong01`, giữ nguyên): raw-traces 60,8 MB, raw-logs 105 KB.
- `run-m1.py` dừng ở adapter: `Multiple runtime series map to one logical metric without a declared aggregation`.
- Nguyên nhân đã xác minh trên `prometheus.json` của gói: kênh `cpu`, `mem` (metric gốc theo container) có 2–3 `container_id` cho mỗi service vì trong cửa sổ t±600 s có các lần recreate (triển khai lượt 1 18:50–18:54Z, đổi topology D1 ~18:58Z). Adapter P7 (khóa) không gộp nhiều container; T-058 cũng sẽ dừng như vậy nếu có recreate trong cửa sổ.
- Hệ quả cho E1: chu kỳ E1 không recreate container (ô CPU-BOOK dùng `docker exec` trong container sẵn có) nên không gặp. Một container tự khởi động lại (OOM, crash) trong t±600 s sẽ làm M1 của ca đó dừng → ghi `M1 LỖI`, chỉ chặn ca đó (hồ sơ `HO-SO-LUOT-E1.md`). Không chỉnh adapter (luật cứng 4).

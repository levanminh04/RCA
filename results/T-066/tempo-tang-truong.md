# T-066 — Tốc độ tăng dung lượng Tempo (bước 10)

**Trạng thái: dừng sớm theo quyết định của Minh** (17/11/2026, trong chat: "dừng đo, giữ 14 ngày"). Đo 12:10:07Z–14:55:08Z (12 mốc), dừng bằng file `DUNG` lúc 15:09Z. Số liệu: `results/T-066/tempo-do-dung.tsv` (chép nguyên `/srv/rca-lab/runs/tempo-do-t066/tempo-24h.tsv`).

## Cách đo

- Script `results/T-066/tempo_do.sh` (sha256 `e14519a0…`), chạy nền trên exp-obs bằng user ubuntu (`setsid nohup`), mỗi 15 phút ghi một dòng vào `/srv/rca-lab/runs/tempo-do-t066/tempo-24h.tsv`: byte volume `flash-ticket-obs-pinned_tempo-data` (`du -sb`), byte `blocks/`, byte `wal/`, tổng span gateway nhận (`otelcol_receiver_accepted_spans_total`) và xuất tới Tempo (`otelcol_exporter_sent_spans_total{exporter=~".*tempo.*"}`). Chỉ đọc.
- Tempo giữ mặc định 14 ngày (`compactor.compaction.block_retention` không đặt trong `observability/tempo/tempo.yaml`). Khi dữ liệu cũ hơn 14 ngày bị xóa, dung lượng có thể giảm trong lúc đo; khối đầu tiên (10/11 ~20:00Z) chưa tới 14 ngày trong cửa sổ đo, nên trong 24 giờ này chỉ có tăng.
- Mốc đầu: 6.142.589.639 byte (khoảng 7 ngày dữ liệu từ 10/11).

## Mức tải trong lúc đo (ghi khoảng có tải)

| Khoảng (UTC) | Tải | Nguồn |
|---|---|---|
| 17/11 12:15:04 – ~12:45 | k6 hành trình mua vé ×1, tag `t3-7ffb2305` (tuyến một ca T-066 bước 9, có tiêm PAUSE-PAYMENT 10 phút) | `/srv/rca-lab/runs/e2e-001/` |
| còn lại | lưu lượng nền của hệ thống thử (không k6) | — |

T-067 chưa chạy trong lúc đo.

## Kết quả

- **Quyết định:** giữ mặc định 14 ngày (Minh, 17/11/2026). Không sửa `tempo.yaml`.
- Quan sát: dung lượng volume dao động răng cưa 6,02–6,46 GB; giảm mạnh ở các mốc 13:10Z và 14:10Z (Tempo nén khối theo chu kỳ). Từ 12:10Z tới 14:55Z thực tăng khoảng +0,05 GB. 2 giờ 45 phút quá ngắn để tách tốc độ tăng khỏi dao động do nén; không đưa ra con số GB/giờ.
- Span gateway nhận (bộ đếm đặt lại khi tạo lại container 12:07:48Z): nền khoảng 115–116 nghìn span/15 phút (13:10Z–14:55Z); khoảng có tải 12:25Z–12:40Z là 204 nghìn, tức khoảng 1,8 lần nền.
- Ước lượng thô (suy luận, chưa kiểm bằng đo dài): volume 6,1 GB chứa khoảng 7 ngày (từ 10/11), tức khoảng 0,9 GB/ngày ở mức tải của T-058…T-065. Ở 14 ngày thì khoảng 12–13 GB, so với đĩa exp-obs đang dùng 27/135 GB. Ước lượng sai nếu tải các đợt sau dày hơn nhiều so với 10–17/11.

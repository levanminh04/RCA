# T-068 — Thay đổi trên exp-obs và Grafana

| Giờ (UTC, 18/11) | Thay đổi | Trước → sau | Hoàn tác |
|---|---|---|---|
| 02:15 | Tạo thư mục thử `/srv/rca-lab/runs/t068-thu/` (cây lab chưa commit, 2 bản sao `du-lieu` ~190 MB mỗi bản) | — | **Ngoài mục "Phạm vi ghi" của SPEC (phản biện R3; Minh ghi nhận 18/11).** Giữ làm bằng chứng (luật cứng 10); xóa khi Minh duyệt: `sudo rm -rf /srv/rca-lab/runs/t068-thu` |
| 02:21:14 | `/opt/rca-lab`: `git checkout 5495877` (trước `ab1c52c`) | ab1c52c → 5495877 | `git checkout ab1c52c` |
| 02:21 | Ghi `rca-results/t065-l11-001/service-graph/` (85 đồ thị + 85 status) | không có → có | Xóa thư mục |
| 02:21 | Đổi nhãn ca 7ffb2305: `V082-V066+H8a/7ffb2305.json` `8b51fe1f…` → `1133d125…`; `V082-V066+H8a/chi-muc.json` `472ba9a5…` → `519b870c…`; bản sao `.bak-t066` cùng thư mục | dev3 → t066 | Giữ `.bak-t066`. Nếu hash hai file vẫn là `1133d125…`/`519b870c…`: chép `.bak-t066` đè lại. Nếu chỉ mục đã có ca mới (hash khác): **không** chép đè, chạy `relabel_case.py --ca 7ffb2305 --nguon dev3` (tự tạo `.bak-dev3`, chỉ đổi hai trường). Sau đó luôn chạy `service_graph.py --ban V082-V066+H8a --ca 7ffb2305` vì `nguon_file_sha256` của đồ thị theo file ca |
| 02:21:45 | Restart `flash-ticket-obs-grafana` (healthy 02:21:54) | provider `rca-g2` → 4 provider | checkout `ab1c52c` + restart |
| 02:22–02:26 | Xóa 9 folder Grafana rỗng (`counts` toàn 0): fg4kl9juknzlsc, bg4kl9k2ccmbkb, eg4kl9k7c5b7ke, fg4kl9jrdsnpca, fg4kl9kbpgwzke, eg4kl9jj9mj9cb, dg4mpei1ofdvka, cg4mpeifouvpce, ag4mpei6bql1cc | — | Tạo lại khi nạp lại provider cũ |
| 02:26:26 | Xóa dashboard `t061-infinity`; xóa datasource `loki-1` (uid dg49lda2pxj40e, url rỗng, 0 tham chiếu) | — | Nhập lại `manual-export/t061-infinity.json`; tạo lại datasource rỗng |
| 02:28:01 | Xóa dashboard `t058-flashticket` (sau khi trang hệ thống đạt) | — | Nhập lại `manual-export/t058-flashticket.json` |
| 02:31:19 | `/opt/rca-lab`: `git checkout 82e813a`; sinh lại 85 đồ thị (service-graph-2) | 5495877 → 82e813a | `git checkout <revision cần phục hồi>` **rồi** `sudo python3 -B campaigns/g1/service_graph.py --tat-ca` bằng chính revision đó: JSON đồ thị nằm trong volume dữ liệu, checkout mã không đổi được chúng |
| 04:26:36 | `/opt/rca-lab`: `git checkout 8dccb34` (sửa R1, R2, R5 theo phản biện, Minh duyệt 18/11); sinh lại 85 đồ thị (service-graph-3); dashboard sự cố tự nạp lại (provider quét 30 s) | 82e813a → 8dccb34 | như dòng trên: checkout revision cần phục hồi rồi `service_graph.py --tat-ca` |

Hash cây `du-lieu` trước/sau: `truoc/du-lieu.sha256`, `sau-du-lieu.sha256`, `sau-du-lieu-2.sha256`, `sau-du-lieu-3.sha256` (ba bản sau trùng nhau).

# T-068 — Thay đổi trên exp-obs và Grafana

| Giờ (UTC, 18/11) | Thay đổi | Trước → sau | Hoàn tác |
|---|---|---|---|
| 02:15 | Tạo thư mục thử `/srv/rca-lab/runs/t068-thu/` (cây lab chưa commit, 2 bản sao `du-lieu` ~190 MB mỗi bản) | — | **Ngoài mục "Phạm vi ghi" của SPEC (phản biện R3; Minh ghi nhận 18/11).** Giữ làm bằng chứng (luật cứng 10); xóa khi Minh duyệt: `sudo rm -rf /srv/rca-lab/runs/t068-thu` |
| 02:21:14 | `/opt/rca-lab`: `git checkout 5495877` (trước `ab1c52c`) | ab1c52c → 5495877 | `git checkout ab1c52c` |
| 02:21 | Ghi `rca-results/t065-l11-001/service-graph/` (85 đồ thị + 85 status) | không có → có | Xóa thư mục |
| 02:21 | Đổi nhãn ca 7ffb2305: `V082-V066+H8a/7ffb2305.json` `8b51fe1f…` → `1133d125…`; `V082-V066+H8a/chi-muc.json` `472ba9a5…` → `519b870c…`; bản sao `.bak-t066` cùng thư mục | dev3 → t066 | Chỉ hoàn tác nhãn khi không có runner ghi chỉ mục; sau đó kiểm lại danh sách ca. Giữ `.bak-t066`. Nếu hash hai file vẫn là `1133d125…`/`519b870c…`: chép `.bak-t066` đè lại. Nếu chỉ mục đã có ca mới (hash khác): **không** chép đè, chạy `relabel_case.py --ca 7ffb2305 --nguon dev3` (tự tạo `.bak-dev3`, chỉ đổi hai trường). Sau đó luôn chạy `service_graph.py --ban V082-V066+H8a --ca 7ffb2305` vì `nguon_file_sha256` của đồ thị theo file ca (đính chính 19/11: từ `service-graph-4` lệnh cần thêm `--goi /srv/rca-lab/m1/cases/7ffb2305`; xem mục Phiên 3) |
| 02:21:45 | Restart `flash-ticket-obs-grafana` (healthy 02:21:54) | provider `rca-g2` → 4 provider | checkout `ab1c52c` + restart |
| 02:22–02:26 | Xóa 9 folder Grafana rỗng (`counts` toàn 0): fg4kl9juknzlsc, bg4kl9k2ccmbkb, eg4kl9k7c5b7ke, fg4kl9jrdsnpca, fg4kl9kbpgwzke, eg4kl9jj9mj9cb, dg4mpei1ofdvka, cg4mpeifouvpce, ag4mpei6bql1cc | — | Tạo lại khi nạp lại provider cũ |
| 02:26:26 | Xóa dashboard `t061-infinity`; xóa datasource `loki-1` (uid dg49lda2pxj40e, url rỗng, 0 tham chiếu) | — | Nhập lại `manual-export/t061-infinity.json`; tạo lại datasource rỗng |
| 02:28:01 | Xóa dashboard `t058-flashticket` (sau khi trang hệ thống đạt) | — | Nhập lại `manual-export/t058-flashticket.json` |
| 02:31:19 | `/opt/rca-lab`: `git checkout 82e813a`; sinh lại 85 đồ thị (service-graph-2) | 5495877 → 82e813a | `git checkout <revision cần phục hồi>` **rồi** `sudo python3 -B campaigns/g1/service_graph.py --tat-ca` bằng chính revision đó: JSON đồ thị nằm trong volume dữ liệu, checkout mã không đổi được chúng |
| 04:26:36 | `/opt/rca-lab`: `git checkout 8dccb34` (sửa R1, R2, R5 theo phản biện, Minh duyệt 18/11); sinh lại 85 đồ thị (service-graph-3); dashboard sự cố tự nạp lại (provider quét 30 s) | 82e813a → 8dccb34 | như dòng trên: checkout revision cần phục hồi rồi `service_graph.py --tat-ca` |

Hash cây `du-lieu` trước/sau: `truoc/du-lieu.sha256`, `sau-du-lieu.sha256`, `sau-du-lieu-2.sha256`, `sau-du-lieu-3.sha256` (ba bản sau trùng nhau).

## Phiên 2 — phương án A (18/11)

| Giờ (UTC, 18/11) | Thay đổi | Trước → sau | Hoàn tác |
|---|---|---|---|
| 09:43 | Tạo thư mục tạm `/srv/rca-lab/runs/t068-a/` (trong phạm vi ghi của mục Bổ sung SPEC): `ra_soat.py`, `dem_doc_lap.py`, kết quả rà soát/kiểm, `truoc-may.part`, `sau-may.part`, `sg4.tar`, `sg4/`, `thu/` (bản sao 1 file ca + đồ thị thử), `nguon-trace-may.json` | — | Giữ làm bằng chứng (luật cứng 10); xóa khi Minh duyệt: `sudo rm -rf /srv/rca-lab/runs/t068-a` (mất luôn bản sao lưu dòng dưới) |
| 09:56 | Sao lưu `rca-results/t065-l11-001/service-graph/` (service-graph-3, 170 file) → `/srv/rca-lab/runs/t068-a/service-graph-3-bak/`; danh sách hash `t068-a/service-graph-3.sha256`; bản sao trùng nguồn | — | — |
| 09:56:28 | `/opt/rca-lab`: `git fetch` + `git checkout 9f4eb5c` (detached; giữa `8dccb34` và `9f4eb5c` có thêm các commit T-067 chỉ ở `app-host/`, `tests/`, không dùng trên exp-obs) | 8dccb34 → 9f4eb5c | `git checkout 8dccb34` |
| 09:56:52 | Sinh đồ thị V082/7ffb2305 trên máy (service-graph-4, 5,9 s) | v3 → v4 | xem dòng 09:59 |
| 09:59:49 | Chép 168 file đồ thị v4 (84 cặp, sinh trên laptop) vào `service-graph/`; hash khớp 168/168 | v3 → v4 | Chép lại từ bản sao lưu: `sudo cp -r /srv/rca-lab/runs/t068-a/service-graph-3-bak/. /srv/rca-lab/rca-results/t065-l11-001/service-graph/` rồi kiểm `sha256sum -c` theo `t068-a/service-graph-3.sha256` (chạy trong thư mục `service-graph/`); kèm checkout `8dccb34` để dashboard đọc đúng trường. Không dùng `service_graph.py --tat-ca` trên máy để hoàn tác (thiếu gói trace của 28 ca, lệnh dừng) — đính chính 19/11: câu này sai. Ở revision `8dccb34` (service-graph-3), `--tat-ca` không cần trace và hoàn tác được bằng checkout `8dccb34` + `sudo python3 -B campaigns/g1/service_graph.py --tat-ca`; đường chép bản sao lưu vẫn đúng. Số gói chỉ có trên laptop là 26, không phải 28. Xem mục Phiên 3 |
| 10:01:12 | `/opt/rca-lab`: checkout `69973fa` (thứ tự cột bảng) | 9f4eb5c → 69973fa | checkout revision cần phục hồi |
| 10:03:54 | `/opt/rca-lab`: checkout `6a0def7` (bố cục chú giải/bảng); dashboard sự cố tự nạp lại (provider quét 30 s), không restart Grafana | 69973fa → 6a0def7 | như trên |

Hash cây `du-lieu` và 200 file bảo vệ trước/sau phiên 2: `a-truoc.sha256` = `a-sau.sha256` (trùng byte).

## Phiên 3 — sửa theo phản biện, service-graph-5 (18/11 23:52 – 19/11 02:48 UTC)

| Giờ (UTC) | Thay đổi | Trước → sau | Hoàn tác |
|---|---|---|---|
| 18/11 23:53 | Tạo `/srv/rca-lab/trace-goi/` (`sudo mkdir`, chủ `ubuntu`); chép 26 gói trace (17 `.tgz`, 9 thư mục ca T-062), `SHA256SUMS` 71 file = `results/T-068/trace-goi.sha256`; `sha256sum -c` khớp 71/71 | — | Không cần cho đồ thị; xóa khi Minh duyệt: `sudo rm -rf /srv/rca-lab/trace-goi` |
| 19/11 02:45 | Mốc trước: `results/T-068/p3-truoc.sha256` (trùng byte `a-sau.sha256`); sao lưu `service-graph/` v4 (170 file) → `/srv/rca-lab/runs/t068-a/service-graph-4-bak/`, danh sách `t068-a/service-graph-4.sha256`, bản sao khớp | — | — |
| 02:46 | `/opt/rca-lab`: `git fetch` + `git checkout --detach ee91432` | 6a0def7 → ee91432 | `git checkout 6a0def7` |
| 02:46:55 | Sinh `V082-V066+H8a/7ffb2305` trên máy (`--goi /srv/rca-lab/m1/cases/7ffb2305`); trùng sha256 bản thử `t068-a/sg5-thu`; bộ kiểm trên máy (`t068-a/dem_doc_lap_5.py`, cùng sha256 bản laptop) 1/1 đạt | v4 → v5 | xem dòng dưới |
| 02:48:08 | Chép 168 file v5 (84 cặp, sinh trên laptop) vào `service-graph/`; tar `sg5.tar` sha256 hai đầu trùng, 168/168 khớp `sg5-laptop.sha256` sau giải nén và sau khi chép; 170/170 file là `service-graph-5` | v4 → v5 | Chép lại bản sao lưu: `sudo cp -r /srv/rca-lab/runs/t068-a/service-graph-4-bak/. /srv/rca-lab/rca-results/t065-l11-001/service-graph/` rồi `sha256sum -c` theo `t068-a/service-graph-4.sha256` (chạy trong `service-graph/`); kèm `git checkout 6a0def7` |

Thư mục tạm thêm trong `t068-a/`: `sg5-thu/`, `thu5/` (thử nhánh lỗi `sau_v082` trên bản sao file ca), `sg5.tar`, `sg5/`, `sg5-laptop.sha256`, `p3-truoc-may.part`, `p3-sau-may.part`, `dem-doc-lap-may-7ffb2305-v5.json`. Mốc sau `results/T-068/p3-sau.sha256` trùng byte mốc trước; không file nào dưới `/srv/rca-lab/m1` mới hơn đầu phiên.

**Lệnh sinh lại theo revision** (thay các hướng dẫn cũ ở trên khi khác):
- `service-graph-2`, `-3` (≤ `8dccb34`): `sudo python3 -B campaigns/g1/service_graph.py --tat-ca` (đọc file ca, không cần trace).
- `service-graph-4`, `-5` (`9f4eb5c` trở đi): một ca `sudo python3 -B campaigns/g1/service_graph.py --ban <bản> --ca <ca> --goi <gói>` (ca mới: `/srv/rca-lab/m1/cases/<ca>`); mọi ca `--tat-ca --nguon-trace <json>`. Gói ca lịch sử trên máy: `/srv/rca-lab/trace-goi/` (26 ca; `.tgz` cần `--sha-ngoai` theo `SHA256SUMS`) và `/srv/rca-lab/m1/cases/` (`46aab4be`, `ebd5ef38`). Chưa thử `--tat-ca` trên máy với các gói này.
- Hoàn tác về một revision trước: checkout revision đó rồi chạy lệnh của chính revision đó, hoặc chép bản sao lưu tương ứng (`t068-a/service-graph-3-bak`, `-4-bak`).

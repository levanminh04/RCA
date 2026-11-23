# T-073 — Gói triển khai E5 (S4): đích cảnh báo, nguồn dashboard, thứ tự, hoàn tác

Bản 1, 22/11/2026, phiên `rca-w5`. **Chưa commit, chưa triển khai.** Điều phối cho Codex soát rồi trình Minh duyệt commit.

## 1. Diff

Worktree `D:/Project/rca-lab-wt/T-073-e5`, nhánh `t073-e5`, gốc **`ecdeed2`** (commit G đang chạy trên exp-obs, nhánh tích hợp `t070-e3`). Toàn văn: `results/T-073/e5.diff`.

| File | Thay đổi | Mục |
|---|---|---|
| `observability/grafana/provisioning/alerting/t073-e5.yaml` | **mới**: thêm integration webhook `t073-webhook-e5` → `http://t073-webhook:8080/t073/canh-bao` vào contact point **`t072-bo-nhan-nhe`** | (a) |
| `observability/grafana/provisioning/alerting/t073-e5-go.yaml.mau` | **mới**: `deleteContactPoints` uid `t073-webhook-e5` (hoàn tác; Grafana không nạp đuôi `.mau`) | (a) |
| `observability/grafana/build_dashboards.py` | biến `RCA_G1_BO` (mặc định `t065-l11-001`); khác mặc định thì đổi mọi URL `public/rca/t065-l11-001` và tên bộ trong ghi chú; dừng nếu còn sót | (b) |
| `observability/grafana/dashboards/{00-start-here,20-incidents,30-replay}/*.json` | sinh lại với `RCA_G1_BO=t073-e5-001`: 43 dòng, chỉ khác tên bộ (1 + 28 + 13 URL, 1 ghi chú) | (b) |
| `campaigns/online/g1_b.py` | cờ `--chi-khoi-tao` (dựng bộ `--ra` theo `--khoi-tao`, không ghi ca) | (b) |

Không đổi: `t072-luat.yaml` (11 luật, file do script T-072 sinh), `compose.yaml`, `compose.t073-webhook.yaml`, lõi M1, các file khác của `campaigns/online/`.

## 2. (a) Đích cảnh báo: thêm integration vào contact point sẵn có

11 luật thật (`t072-luat.yaml`) đều định tuyến từng luật `notification_settings.receiver: t072-bo-nhan-nhe` (kiểm: 11/11). Contact point đó có một integration `t072-webhook` → `http://t072-bo-nhan:9172/t072`.

| Cách | Đổi luật? | Bằng chứng T-072 | Chọn |
|---|---|---|---|
| **Thêm integration thứ hai vào `t072-bo-nhan-nhe` bằng file riêng** | Không: truy vấn, ngưỡng, `for`, nhãn, `notification_settings` giữ nguyên | Giữ (Grafana gửi tới mọi integration của contact point) | **Có** |
| Contact point mới + đổi `receiver` của 11 luật | Có: đổi định nghĩa luật (phiên bản luật mới), dù không đổi biểu thức | Phải liệt kê lại cả hai đích | Không |
| Sửa `t072-luat.yaml` bằng tay | Không | Giữ | Không: file "sinh bởi `sinh_luat_grafana.py`, không sửa tay" |

**Chưa kiểm:** Grafana 13.3 nạp hai file provisioning cùng `name` contact point thành **một** contact point có hai integration (provisioning theo `uid` từng receiver, nhóm theo `name`). Kiểm ở S4-6. Không đạt (chỉ thấy một integration, hoặc log Grafana báo lỗi provisioning) → hoàn tác §5 bước 3, và phương án dự phòng: T-072 sinh lại `t072-luat.yaml` bằng `sinh_luat_grafana.py` với hai receiver trong cùng contact point (việc của T-072, cần điều phối/Minh).

Hệ quả: bộ nhận T-073 nhận cả hai luật lớp `quan-sat` (`t072-mat-do`, `t072-mat-gw`) và tin Test của Grafana; bộ gom xếp lớp quan sát, không chạy RCA (`incidents.py`, T072-i1-1 (a)).

## 3. (b) Nguồn dashboard: bộ `rca-results/t073-e5-001`

- Dashboard đọc qua mount chỉ đọc `rca-results` → `/usr/share/grafana/public/rca`. Commit này đổi ba dashboard sang `public/rca/t073-e5-001`.
- Bộ `t073-e5-001` dựng **trước** khi đổi checkout bằng bản chép `du-lieu/` và `service-graph/` của `t065-l11-001` (giống `g1_b.py --khoi-tao chep:`), nên ca cũ vẫn xem và phát lại được; ca E5 do `g1_b.py` thêm vào chỉ mục (chỉ thêm, không sửa mục cũ). `t065-l11-001` không bị ghi.
- Dashboard nạp bằng provider file (`updateIntervalSeconds: 30`): đổi checkout là đổi hiển thị trong ≤ 30 s, không cần restart cho phần này.
- Kiểm trên laptop: sinh lại mặc định → 4 dashboard trùng byte bản `ecdeed2`; sinh với `t073-e5-001` → 0 chuỗi `t065-l11-001` còn lại, 43 dòng đổi chỉ khác tên bộ; tên bộ sai dạng bị từ chối. `--chi-khoi-tao` (hàm `khoi_tao`, chép) thử trên thư mục giả: chép `du-lieu/`, `service-graph/`, bỏ thư mục khác; chạy lần hai → `da_co`.

## 4. Thứ tự ở S4 (I7: chỉ khi không có job; mỗi bước ghi giờ vào `results/T-073/e5/`)

Điều kiện mở: E4 xong; điều phối mở S4 cho T-073; Minh duyệt commit E5 và commit đã push; `khai-truoc-e5.json` (`5883c4e2…`) và `khoa-boc-e5.json` (`27b0a61d…`) đã khóa; Minh đã cấp hạt và ô đã bốc; K1–K10 (`bang-o-e5.md`) kiểm trong S4-1.

1. **S4-1** Kiểm chỉ đọc: không job (`pgrep -af "runner4|tai_linux|chuoi_tai|orchestrator|do-0"`), không STOP; `/opt/rca-lab` = `ecdeed2` sạch; container `flash-ticket-obs-*`, `flash-ticket-t072-bo-nhan` Up; K1–K10.
2. **S4-2** Dựng bộ: `sudo install -d -o root -g root -m 0755 /srv/rca-lab/rca-results/t073-e5-001 && sudo cp -a /srv/rca-lab/rca-results/t065-l11-001/du-lieu /srv/rca-lab/rca-results/t065-l11-001/service-graph /srv/rca-lab/rca-results/t073-e5-001/`; ghi số file và sha256 danh sách chỉ mục hai bên.
3. **S4-3** Bộ nhận T-073: `install -d -m 0700 /srv/rca-lab/runs/t073-e5-01/spool`; file env `/srv/rca-lab/runs/t073-e5-01/webhook.env` = cùng `T073_WEBHOOK_IMAGE` và `T072_RA_DIR` như `/srv/rca-lab/runs/t072-e3-01-cfg/webhook.env` (để không tạo lại `t072-bo-nhan`), thêm `T073_SPOOL_DIR=/srv/rca-lab/runs/t073-e5-01/spool`; `cd /opt/rca-lab/observability && docker compose -p t073-webhook --env-file /srv/rca-lab/runs/t073-e5-01/webhook.env -f compose.t073-webhook.yaml up -d t073-webhook`; kiểm `healthy`, `t072-bo-nhan` giữ nguyên thời gian Up.
4. **S4-4** Đổi checkout `/opt/rca-lab` `ecdeed2` → commit E5 (I7; ghi trước/sau vào `LICH-MAY.md`); cây sạch.
5. **S4-5** Restart Grafana như T-072 E3 bước 4 (`results/T-072/e3.md`, `e3/b4-restart.txt`); chờ health ok; lưu log Grafana sau restart.
6. **S4-6** Kiểm (a): trang Alerting → Contact points: `t072-bo-nhan-nhe` có **hai** integration (`t072-webhook`, `t073-webhook-e5`); 11 luật giữ uid, biểu thức, ngưỡng (đối chiếu `t072-luat.yaml`); log không có lỗi provisioning. Nút Test của contact point → có dòng mới ở **cả** `/srv/rca-lab/runs/t072-e3-01/webhook.jsonl` và spool T-073. Không đạt → §5 bước 3 và phương án dự phòng §2; không đi tiếp.
7. **S4-7** Kiểm (b): dashboard "RCA — sự cố" liệt kê đủ ca cũ từ `t073-e5-001` (số ca = chỉ mục `t065-l11-001`); mở một ca cũ và trang phát lại của nó; ảnh chụp.
8. **S4-8** Phát bộ điều phối: `RCA_ONLINE_OUT=/srv/rca-lab/runs/t073-e5-01 setsid -f nohup python3 -B /opt/rca-lab/campaigns/online/orchestrator.py chay --ra /srv/rca-lab/rca-results/t073-e5-001 --spool /srv/rca-lab/runs/t073-e5-01/spool > /srv/rca-lab/runs/t073-e5-01/orchestrator.out 2>&1 < /dev/null`; tin Test ở S4-6 phải được gom thành sự cố **quan sát** (không chạy RCA).
9. **S4-9** Lượt E5 theo `khai-truoc-e5.json` và ô đã bốc (tải, tiêm, ba mốc giờ, lúc dashboard hiện ca). Ngoài phạm vi file này.

## 5. Hoàn tác (đảo thứ tự; giữ mọi dữ liệu)

1. Dừng bộ điều phối: `touch /srv/rca-lab/runs/t073-e5-01/STOP`, chờ bước đang chạy xong, rồi dừng tiến trình.
2. Dashboard: commit hoàn tác sinh lại `build_dashboards.py` không đặt `RCA_G1_BO` (hoặc trả checkout về `ecdeed2`) → dashboard về `t065-l11-001` trong ≤ 30 s. Bộ `t073-e5-001` giữ nguyên.
3. Đích cảnh báo: trong commit hoàn tác, xóa `t073-e5.yaml`, đổi `t073-e5-go.yaml.mau` → `t073-e5-go.yaml`; đổi checkout (I7); restart Grafana; kiểm `t072-bo-nhan-nhe` còn một integration. Chỉ xóa file `t073-e5.yaml` thì **không** gỡ integration đã nạp (provisioning không tự xóa), nên phải có bước `deleteContactPoints`.
4. Bộ nhận T-073: `docker compose -p t073-webhook --env-file /srv/rca-lab/runs/t073-e5-01/webhook.env -f compose.t073-webhook.yaml rm -s -f t073-webhook`; spool giữ trên host.
5. `/opt/rca-lab` về commit được chỉ định; ghi `LICH-MAY.md`.

## 6. Còn mở

- Gộp nhánh: `t073-e5` đặt trên `ecdeed2`; nếu điều phối muốn commit nằm trên `t070-e3` thì cherry-pick nguyên commit (không xung đột: chỉ thêm file và đổi các file chỉ T-073 chạm).
- (a) chưa kiểm trên Grafana thật (S4-6).
- Lúc dashboard hiện ca mới: đo ở E5 (đích cuối của N).

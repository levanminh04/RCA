# Kế hoạch dọn repo lab và ba máy thực nghiệm

Bản 2, ngày 24/11/2026. Người làm: Claude (phiên T-070). Người phản biện: Codex.

File này là kế hoạch duy nhất cho việc dọn. Bản 1 được giữ nguyên ở `KE-HOACH-DON.ban-1.md` để đối chiếu.

**Trạng thái:** chưa dời và chưa sửa gì, cả trên máy lẫn trong repo lab. Mỗi bước ở §9 chỉ bắt đầu khi Minh ra lệnh riêng cho bước đó.

## Lịch sử bản

| Bản | Ngày | Nội dung |
|---|---|---|
| 1 | 24/11 | Bản đầu. Codex phản biện lượt 1 (`tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md`, R1–R10) |
| 2 | 24/11 | Minh duyệt sửa ("Duyệt, viết bản 2"), gồm giữ nguyên UID. Sửa theo R1–R10 và N1–N4 (bảng phản hồi trong `REVIEW.md`). §15 đối chiếu từng điểm với chỗ sửa |

## Mục lục

1. Mong muốn của Minh
2. Quyết định đã có và đang chờ
3. Mục tiêu và tiêu chí xong
4. Bất biến: không làm lệch phương pháp và dữ liệu
5. Khung đích
6. Bảng dời: repo lab
7. Bảng dời: ba máy, tên trong Grafana
8. Chỗ phải sửa đường dẫn
9. Các bước, hoàn tác, gặp lỗi giữa chừng
10. Kiểm sau khi dời
11. Việc nhẹ làm kèm
12. Ngoài phạm vi dọn: việc sau
13. Rủi ro và điểm chưa kiểm
14. Nguồn dữ kiện
15. Đối chiếu sửa theo phản biện lượt 1

Ký hiệu máy:
- **obs**: exp-obs, máy quan sát. Chạy Grafana, Prometheus, Loki, Tempo, Collector gateway, và là nơi chạy RCA.
- **app**: exp-app, máy chạy bản FlashTicket thử nghiệm.
- **tải**: máy tải AWS, chạy k6.

---

## 1. Mong muốn của Minh

Trích từ chat ngày 24/11/2026. Nguồn: lịch sử phiên T-070, và các dòng LOG T-070 lúc 09:25Z, 10:20Z, 11:40Z, 13:20Z, 14:45Z.

| # | Mong muốn | Lời Minh (trích ngắn) | Kế hoạch đáp ở |
|---|---|---|---|
| Y1 | Repo lab sạch, cô đọng, đọc hiểu được code. Không có thư mục rỗng, không đặt file lung tung | "cần 1 repo thật clean, cô đọng để đọc hiểu code" | §5, §6 |
| Y2 | Tách vai hai repo: lab là nơi sạch để đọc code, repo RCA là nơi chạy thực nghiệm và lưu hồ sơ | "1 bên để làm nơi clean, đọc hiểu code, 1 nơi là để chạy thực nghiệm" | §5 |
| Y3 | Không đặt tên theo mã task (T-0xx, t063, t064…) trong lab và trên máy. Người ngoài và giảng viên phải đọc hiểu | "toàn thư mục T-0xx thì giảng viên đọc sẽ không hiểu" | §5–7; phần còn lại ở §7.5 |
| Y4 | Chốt khung trước, sửa đường dẫn sau. Sửa đường dẫn không được đụng code phương pháp | "chốt các khung trước đi, sửa path tính sau… không động đến code phương pháp" | §4, §8 |
| Y5 | Dọn kỹ, không bất cẩn: dời file hay sửa linh tinh đều có thể làm hỏng | "đừng đề xuất 1 cách bất cẩn… đề xuất kĩ giúp tôi" | §4, §9, §10 |
| Y6 | Giữ những gì thực sự cần cho đồ án. Phần ít giá trị hoặc ít khả năng dùng lại thì để trên server, không kéo về laptop, ghi rõ chỗ để sau còn tìm | "giữ trên server… đừng lôi về laptop, note rõ để sau có chỗ tìm" | §7, §2 (A1) |
| Y7 | Xem lại luật "lưu mọi bước tính toán" và việc lập manifest tràn lan | "về luật agent mà lưu lại mọi bước tính toán thì xem lại" | §2 (A1, A2) |
| Y8 | Chỉ giữ một bản mã phương pháp. V082 là bản chạy chính | "chốt 1 bản thôi không được à? … V082 LÀ CHẠY chính" | §5, §6 (`rca/method.lock`) |
| Y9 | Được đọc trên máy bằng sudo, nhưng không sửa lung tung | "đừng sửa lung tung, phần nào cần đọc thì hãy đọc" | §9 (bước 0 chỉ đọc) |
| Y10 | Không nêu việc nhẹ như việc chính. Việc làm lại được thì ghi là việc nhẹ | "đừng nhắc bất kì 1 việc nhẹ nào mà như thế nào quan trọng" | §11 |
| Y11 | Phần log, telemetry, giám sát và observability của FlashTicket do Minh toàn quyền quyết, miễn không ảnh hưởng hệ thống | "tôi toàn quyền quyết định… miễn là không ảnh hưởng đến hệ thống" | §12 |
| Y12 | Muốn dùng bản FlashTicket mới nhất cho thống nhất | "tôi muốn merge mới nhất để cho thống nhất" | §12 |
| Y13 | Dọn trước W7. E6 dừng hẳn, hạn bán tính sau. W7 hoãn | "dừng toàn bộ… sự kiện hết hạn thì tính sau"; "w7 tạm hoãn" | §2 |
| Y14 | Dừng điều phối, làm trong một phiên. Codex chỉ phản biện khi Minh tự gửi, và không dùng subagent | "dừng điều phối nữa… làm ở phiên này thôi"; "dặn codex không dùng subagent" | §9 |
| Y15 | Không đoán, không chữa cháy. Có bằng chứng thì nói, chưa kiểm thì ghi chưa kiểm | "đừng cố giải thích theo kiểu chữa cháy lấp liếm"; "không bịa hay đoán ý" | toàn văn; §13 |
| Y16 | Ghi kế hoạch đủ vào một file để không mất ngữ cảnh | (yêu cầu ngày 24/11) | file này |

## 2. Quyết định đã có và đang chờ

**Đã có.** Minh nói trong chat ngày 24/11. Các dòng này chưa vào `docs/DECISIONS.md`; chữ ghi vào đó chờ Minh duyệt (mục D1 bên dưới).

- E6 dừng hẳn. Hạn bán của sự kiện tải (02/12/2026 22:16Z) tính sau.
- W7 tạm hoãn.
- Dọn làm trước W7. Câu này thay quyết định ngày 23/11 "dọn repo sau W7".
- Minh toàn quyền quyết phần log, telemetry và observability.
- Kiểm kê chỉ đọc đã duyệt và đã xong (`results/T-070/kiem-ke/`).
- Khung thư mục ở §5: Minh duyệt ("Duyệt khung").
- Bản 2 theo các đề xuất sửa sau phản biện lượt 1, gồm giữ nguyên UID dashboard và luật cảnh báo: Minh duyệt ("Duyệt, viết bản 2").
- Q5 ngày 23/11 vẫn hiệu lực: giữ mục 2.6 (`/opt/rca-tai` trên máy tải).

**Đang chờ Minh:**

| Mã | Việc | Đề xuất |
|---|---|---|
| K1–K7 | Những chỗ khung chưa có | §5.4. Codex lượt 1 không phản đối K1–K6 về bố trí; K7 thêm ở bản 2 |
| Q2 | Tên bộ kết quả dashboard đang hiện | `dev` (§7.1) |
| Q3 | Chạy hồi quy V082 trên 2 ca sau khi dời | §10. Mất vài phút, không phát tải |
| Q4 | Lượt mua vé 10 phút để kiểm tín hiệu sau khi dời | §10. Có phát tải |
| A1 | Sửa luật 10 trong `AGENTS.md` | "**Giữ mọi lượt chạy**, kể cả lượt hỏng, nhưng chọn nơi giữ theo giá trị: (a) đầu ra làm bằng chứng cho kết luận trong quyển hoặc cần cho bước sau → repo hoặc laptop; (b) phần còn lại (đầu ra thô, nhật ký trung gian, lượt hỏng đã có kết luận) → giữ trên máy ở `/srv/flashticket-rca/archive/`, không kéo về laptop, ghi một dòng vào `docs/ARCHIVE-INDEX.md` (máy, đường dẫn, nội dung, dung lượng, ngày). Không xóa (b) khi Minh chưa duyệt." |
| A2 | Thêm vào luật 4 của `AGENTS.md` | "Manifest chỉ lập cho dữ liệu nằm ngoài git và được dùng làm bằng chứng; file trong git dùng commit làm vân tay." |
| D1 | Ghi khối DECISIONS chiều 24/11 | Chữ đã trình trong chat |
| G1 | Commit `results/T-070/kiem-ke/`, `results/T-070/don/`, `REVIEW.md`; push `74b2515` | Cần Minh duyệt |

## 3. Mục tiêu và tiêu chí xong

**Mục tiêu.** Sau khi dọn, một người chưa biết dự án (ví dụ giảng viên) làm được ba việc:
1. Đọc repo lab và hiểu hệ thống thực nghiệm gồm những phần nào, mỗi phần nằm ở đâu, mà không phải đọc tên mã task trong cây thư mục.
2. Đăng nhập một máy bất kỳ và đoán đúng thư mục nào chứa gì.
3. Lần từ một kết quả trong quyển về đúng mã phương pháp đã chạy (commit repo RCA và hash bản chụp), và về đúng dữ liệu đầu vào (đường trên máy, hoặc chỗ lưu trữ ghi trong chỉ mục).

Trong lúc đạt mục tiêu này, kết quả của phương pháp không được đổi (§4).

**Tiêu chí xong:**
1. Repo lab `main` khớp khung §5. Tên file và thư mục không mang mã task, trừ các ngoại lệ ở §7.5.
2. Ba máy cùng checkout một commit lab, tại `/opt/flashticket-rca`.
3. Mọi bất biến §4 đạt. Lệnh và kết quả ghi trong LOG T-070.
4. Mọi phép kiểm §10 đạt, hoặc ghi rõ phần chưa kiểm kèm lý do.
5. Có `archive/2026-11/README.md` trên mỗi máy và `docs/ARCHIVE-INDEX.md` trong repo RCA, liệt kê đủ những gì đã chuyển vào lưu trữ.
6. Không xóa dữ liệu nào ngoài danh sách việc nhẹ §11, và danh sách đó phải được Minh duyệt riêng.

## 4. Bất biến: không làm lệch phương pháp và dữ liệu

Bước 0 (§9) chụp số đo "trước". §10 đo lại "sau". Lệch ở đâu thì dừng phần phụ thuộc và báo Minh.

**Không lưu giá trị bí mật.** Mọi so sánh cấu hình làm ngay trên máy. Lưu về repo chỉ gồm: tên project, image, mount (nguồn, đích, loại, rw/ro), đường env file, tên biến, và hash của từng giá trị biến tính trên máy (cách `hieu_luc.py::mask`). Không lưu đầu ra của `docker compose config` và `docker inspect` khi đã giải biến.

| # | Bất biến | Cách chứng minh |
|---|---|---|
| B1 | Mã phương pháp trong repo RCA (`src/m1`, `src/m1_ft`, `src/p3`) không đổi trong suốt đợt dọn | `git diff` và `git status` trên ba thư mục đều rỗng, so với commit lúc bắt đầu |
| B2 | Bản chụp mã trên obs không đổi byte | 149 file trùng sha256 với `kiem-ke/m1-ban-chup.tsv`. Tính lại `sha_ma_nguon` ra đúng `b0f79a4d…`. Thư mục được `mv`, không chép lại từ git (RR1) |
| B3 | Tham số và cấu hình khóa không đổi | sha256 của `m1-source-pins.json`, `m1-p7-config.json`, `flashticket-inventory-source.json`. Cấu hình V082 trong bản chụp phải có byte hash `01a64b60…` (`results/T-066/hoi-quy-v082.json#/ghim/cau_hinh`) |
| B4 | Môi trường Python của V082 không đổi khi dựng lại venv | `pip freeze --all` của venv mới **trùng từng dòng** với venv cũ (chụp ở bước 0), kể cả dòng `pip`. Phiên bản Python trùng (`3.12.3`). Mọi gói khai trong `requirements-m1.txt` có đúng phiên bản đã ghim |
| B5 | Phía lab chỉ đổi chuỗi đường dẫn, tên module và tên file, trừ đúng các hunk logic đã khai ở §6 (L1, L2). Áp cho `run_m1`, `stage_m1`, `stage_b`, `xuat_bo_sung`, `sau_v082`, `g1_b`, `g1_export`, `service_graph`, `runner`, `orchestrator`, `incidents`, `inject` | `git diff -M` so với tag `truoc-don-2026-11`, đọc từng hunk. Hunk nào ngoài danh sách thì tách ra và trình riêng |
| B6 | Cách ly nhãn giữ nguyên | (a) Sổ tiêm lỗi vẫn `ledger:ledger 700`. (b) `rca/cases` và `rca/outputs` giữ quyền cũ. (c) `runs/` mới và `archive/2026-11/runs/` đều `ubuntu:ubuntu 700`. (d) `sudo -u rca test -r` trả 1 trên một nhật ký có tên ô ở cả vùng lưu trữ lẫn vùng đang dùng, và trên sổ tiêm. (e) Danh sách cấm trong `run_m1.py` trỏ đúng đường sổ mới |
| B7 | Thu thập telemetry không đổi (đây là đầu vào của phương pháp) | Nội dung `agent-docker-host.yaml` và `gateway.yaml` trùng bản đang chạy; đã kiểm `git diff 407b4f5 main -- observability/collector` rỗng. Tên biến và hash giá trị biến của container agent và gateway trùng trước và sau, trừ biến chứa đường dẫn |
| B8 | FlashTicket thử nghiệm chạy đúng cấu hình cũ | Image vẫn `ft-local/*:arm64-t067-36a3725d`. Từng container giữ cùng tập tên biến và hash giá trị, trừ biến đường dẫn. Mount (đích, loại, rw/ro) trùng; nguồn chỉ khác phần đường đã đổi. Riêng mount MongoDB: xem §7.2 |
| B9 | Dữ liệu quan sát và DB không mất | Tên compose project và volume giữ nguyên (§5.3). Sau dời, Prometheus, Loki và Tempo vẫn truy vấn được một khoảng cố định trước ngày dời, cùng số chuỗi hoặc số dòng như ở bước 0. DB FlashTicket còn đơn cũ (đếm bằng truy vấn đọc) |
| B10 | Dữ liệu hiển thị không đổi | sha256 toàn cây `rca/results/dev` trùng cây `rca-results/t065-l11-001` trước dời. UID dashboard giữ nguyên, nên các link `detail__url` trong dữ liệu đồ thị vẫn đúng |
| B11 | Luật cảnh báo chỉ đổi tên folder và tên nhóm hiển thị | `rules.yaml` so với `t072-luat.yaml`: chỉ khác hai dòng `folder:` và `name:` của nhóm. UID, `title`, nhãn (gồm `t072_uid`), receiver và contact point giữ nguyên |
| B12 | Dashboard chỉ đổi tên file và đường dữ liệu | Thay `t065-l11-001` → `dev` trong JSON cũ, so với JSON mới: phải trùng. UID và link chéo giữ nguyên |
| B13 | Phương pháp cho cùng kết quả trên cùng đầu vào | Hồi quy V082 trên 2 ca theo lệnh ở §10. `method-output-1.json` và `-2.json` của mỗi ca trùng byte với chuẩn T-066/T-064: `46aab4be` → `573df32d…`, `ebd5ef38` → `563f449d…` (`results/T-066/hoi-quy-v082.json#/ca`) |
| B14 | Không mở dữ liệu khóa | Không đụng `data/locked/` của repo RCA |

## 5. Khung đích

Khung này Minh đã duyệt ngày 24/11. Những chỗ khung chưa có nằm ở §5.4.

### 5.1 Repo lab `flashticket-rca-lab`: nơi đọc hiểu code

```
flashticket-rca-lab/
├─ README.md          sơ đồ hệ thống, cách chạy, link sang mã phương pháp
├─ docs/              kiến trúc, hướng dẫn chạy, ten-cu-moi.md (bảng tra tên cũ → mới)
├─ inventory/         địa chỉ máy, biến cấu hình
├─ test-environment/  cách dựng FlashTicket thử nghiệm trên app (không chứa code FlashTicket)
├─ observability/     collector, prometheus, loki, tempo, grafana, alert-receiver
├─ load/              kịch bản k6, mức tải, bộ điều khiển tải
├─ faults/            tiêm lỗi, toxiproxy, VNPay giả và đường hầm
├─ rca/
│  ├─ online/         nhận cảnh báo → gom sự cố → chụp dữ liệu → chạy V082 → kết quả cho Grafana
│  ├─ batch/          chạy hàng loạt theo lịch, bước sau V082
│  ├─ lib/            (K1) mã dùng chung cho online và batch
│  └─ method.lock     trỏ tới mã phương pháp: commit repo RCA, hash bản chụp
└─ tests/
```

- Repo lab **không chứa mã phương pháp** (Y8). Mã chỉ nằm ở repo RCA (`src/m1`, `src/m1_ft`, `src/p3`), vì 1.037 script trong `results/` đang dùng tới nó.
- V082 là một cấu hình của M1, nên chạy V082 chính là chạy mã M1.
- Trên máy hiện chỉ có một bản chụp (`b0f79a4d…`), và `rca/method.lock` ghi đúng bản đó.
- Lịch chạy và hồ sơ từng lượt thuộc repo RCA. Khi chạy, lịch đã duyệt được chép vào thư mục lượt trên obs (§7.1).

### 5.2 Repo RCA `RCA-flashticket`: nơi chạy thực nghiệm và lưu hồ sơ

- Giữ đánh số T-0xx. Đây là nhật ký nghiên cứu, và hồ sơ cũ dẫn chiếu theo số này.
- Giảng viên đọc repo qua `docs/READING-GUIDE.md`.
- Thêm `docs/ARCHIVE-INDEX.md`: chỉ mục những gì nằm ở `archive/` trên máy. File này đi cùng A1.

### 5.3 Trên máy

```
/opt/flashticket-rca/           checkout repo lab (cùng commit trên cả ba máy)
/etc/flashticket-rca/           bí mật, file env của phía RCA
/srv/flashticket-rca/
├─ rca/                         gốc M1 (RCA_M1_ROOT): pins, config, cases/, outputs/, v082/, bo-sung/, *-hoi-quy/
│  ├─ method/<hash>/            bản chụp mã V082 đang chạy
│  ├─ results/<bộ>/             kết quả cho Grafana (bind vào public/rca)
│  └─ venv/                     (K5) venv dựng lại
├─ runs/<ngày>-<mục-đích>/      nhật ký từng lượt; runs/STOP là cờ dừng của runner và orchestrator
├─ ledger/                      sổ tiêm lỗi (user ledger, 700)
├─ collector/                   vùng ghi vòng của Collector (gateway trên obs, agent trên app)
├─ load/                        (K4, obs) trạng thái bộ điều khiển tải; load/STOP là cờ dừng tải
├─ alerts/                      (K7, obs) env và đầu ra của bộ nhận cảnh báo
├─ faults/                      (K3, app) control/audit của hook, trạng thái inject, VNPay giả
└─ archive/2026-11/             mọi thứ cũ, giữ tên t0xx, có README.md chỉ mục

/opt/flashticket/               (app) FlashTicket thử nghiệm
├─ src/  build/<commit>/  compose/  env/
└─ infra/  secrets/  otel/      (K2)
```

**Không đổi tên compose project.** Volume Docker gắn với tên project (`flash-ticket-obs-pinned_*`, `flash-ticket-infra_*`). Đổi tên project thì Docker tạo volume mới, rỗng. Vì vậy các file compose khai `name:` bằng đúng tên cũ: `flash-ticket-obs-pinned`, `flash-ticket-infra`, `flash-ticket-<service>`, `flash-ticket-collector`, `flash-ticket-keycloak`, `t073-webhook`.

**Quyền của thư mục mới cấp một** (thư mục dời bằng `mv` thì giữ quyền cũ):

| Thư mục | Chủ, quyền |
|---|---|
| `/srv/flashticket-rca/` | root:root 755 |
| `rca/` | root:rca 755. Các con giữ quyền cũ |
| `runs/`, `load/`, `alerts/` | ubuntu:ubuntu 700 |
| `archive/2026-11/` | root:root 755 |
| `archive/2026-11/runs/` | ubuntu:ubuntu 700 |
| `archive/2026-11/m1/` | root:rca 750 |
| `faults/` (app) | root:root 755; `faults/<svc>` giữ uid 10001 750 |
| `/etc/flashticket-rca/` | root:root 755; file con giữ quyền cũ |
| `/opt/flashticket/` | root:root 755 |

### 5.4 Chỗ khung chưa có: cần Minh duyệt

| # | Thứ chưa có chỗ | Đề xuất | Lý do | Phương án khác |
|---|---|---|---|---|
| K1 | Mã dùng chung cho online và batch: `run_m1`, `stage_m1`, `ledger_append`, `safe_export`, `xuat_bo_sung`, `service_graph`, `g1_export`, `inventory` | `rca/lib/` | `orchestrator.py` (online) và runner (batch) cùng gọi các file này | Để trong `batch/` và cho online gọi chéo: khó đọc |
| K2 | Hạ tầng DB, bí mật mã QR vé, javaagent của Keycloak trên app | `/opt/flashticket/{infra,secrets,otel}` | Đều là đồ của FlashTicket | Gộp vào `compose/` |
| K3 | Trạng thái tiêm lỗi trên app | `/srv/flashticket-rca/faults/` | Dữ liệu RCA sinh ra khi chạy, sống qua nhiều lượt | Đặt trong `runs/` |
| K4 | Trạng thái bộ điều khiển tải trên obs | `/srv/flashticket-rca/load/` | Trạng thái dài hạn của một dịch vụ | Đặt trong `runs/` |
| K5 | Venv V082 | `/srv/flashticket-rca/rca/venv/`, dựng lại | Đi cùng bản chụp | Giữ đường cũ: trái Y3 |
| K6 | File bỏ khỏi lab mà repo RCA chưa có | Chép vào `results/T-070/don/tu-lab/`, kèm commit nguồn | Thuộc phạm vi ghi của T-070 | Chép vào thư mục kết quả của task đã đóng |
| K7 | Env và đầu ra của bộ nhận cảnh báo (đang ở `runs/t072-e3-01*`) | `/srv/flashticket-rca/alerts/` | Bộ nhận chạy liên tục, không thuộc một lượt | Đặt trong `runs/` |

## 6. Bảng dời: repo lab

Ký hiệu:
- **giữ**: giữ nguyên chỗ.
- **bỏ**: bỏ khỏi `main`. Bản vẫn còn trong tag `truoc-don-2026-11`, và bảng ghi chỗ bản sao ở repo RCA nếu có.

Đặt tên file theo chức năng; chỉ đổi tên những file mang mã task hoặc số lượt. Đối chiếu bản sao bằng git blob id.

**Hai hunk logic được khai trước.** Đây là thay đổi ngoài đường dẫn, cần Minh duyệt cùng bản 2 (B5):
- **L1.** Trong `g1_b.py`, điều kiện "chỉ ghi vào bộ tên `t073-*`" đổi thành "chỉ ghi vào bộ tên `online-*`". Vẫn cấm ghi vào bộ `dev` (hằng `CAM_GHI` trỏ `rca/results/dev`). Mục đích giữ nguyên: bảo vệ bộ chính (I9).
- **L2.** Trong `sau_v082.py`, `nap_bo_xuat` nạp `rca/lib/g1_export.py` thay cho `campaigns/g1/l8b-xuat.py`. Tên module nạp đổi theo. Cặp chuỗi mẫu `SRC_GOC` và `BS_GOC` **giữ nguyên byte**: đó là chuỗi trong nguồn `dev3_template` mà hàm đếm và thay lúc nạp, không phải đường được truy cập.

| Cũ | Mới | Ghi chú |
|---|---|---|
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes` | giữ | Sửa đường dẫn. `AGENTS.md` của lab là file luật nên phải duyệt chữ |
| `docs/architecture.md`, `docs/sources-2026-11.md` | giữ | `sources-2026-11.md` là tài liệu lịch sử, không sửa đường. Thêm `docs/ten-cu-moi.md` |
| `inventory/*` | giữ | Sửa đường trong `oracle-exp.env` |
| `app-host/README.md` | `test-environment/README.md` | Sửa tag image đã cũ |
| `app-host/overrides/*.yml` (7 file) | `test-environment/overrides/` | |
| `app-host/infra/docker-compose.rca-log.yml` | `test-environment/infra/` | |
| `app-host/scripts/{build.sh, deploy.sh, hieu_luc.py}` | `test-environment/scripts/` | `hieu_luc.py`: sửa hằng đường dẫn. `deploy.sh`: đích hoàn tác chuyển sang bộ Compose hiệu lực T-067 đã lưu (§7.2) |
| `app-host/scripts/{build,prepare,rollback}-t062.*` | bỏ | Có ở RCA `results/T-062/ha-tang/scripts/` |
| `app-host/scripts/deploy-t062.sh` | bỏ | Chép vào `tu-lab/` |
| `app-host/services/*.yml` (9 file) | bỏ | Bản `compose-t062` cũ. Chép vào `tu-lab/` |
| `campaigns/` (gói Python) | `rca/` | Sửa 4 chỗ `from campaigns.lib import inventory` |
| `campaigns/{README.md, requirements-m1.txt, __init__.py}` | `rca/` | |
| `campaigns/lib/inventory.py` | `rca/lib/` | |
| `campaigns/online/*` (8 file) | `rca/online/` | `g1_b.py`: L1 |
| `campaigns/runner/{run_m1, stage_m1, ledger_append, safe_export, xuat_bo_sung}.py` | `rca/lib/` | Danh sách cấm của `run_m1.py` chứa chuỗi `'/srv/rca-lab/ledger'`. **Bắt buộc** đổi thành đường sổ mới (B6) |
| `campaigns/runner/sau_v082.py` | `rca/batch/sau_v082.py` | L2. Mặc định `--ra` đổi thành `rca/results/dev`. Không xóa `SRC_GOC`/`BS_GOC` |
| `campaigns/g1/l8b-xuat.py` | `rca/lib/g1_export.py` | **Giữ**: đang được nạp khi chạy (R2). Không sửa thân file. Hàm `stop()` của file bị `sau_v082` thay lúc nạp, nên đường `~/rca-dieu-phoi/STOP` bên trong không có tác dụng; giữ nguyên |
| `campaigns/runner/runner4.py` | `rca/batch/runner.py` | Bỏ số "4" trong tên |
| `campaigns/g1/service_graph.py` | `rca/lib/` | Hằng `DASH = '/d/t065-l8b-rca'` **giữ nguyên** (UID giữ) |
| `campaigns/g1/relabel_case.py` | bỏ | Việc một lần của T-068. Chép vào `tu-lab/` |
| `campaigns/runner/pool_prom.py` | bỏ | Có ở RCA `results/T-063/thu3/scripts/` |
| `campaigns/schedules/{lich-2, lich-3, lich-thu-ngan, lich-thu3-ngan}.json` | bỏ | Có ở RCA `results/T-063/` |
| `campaigns/schedules/{lich-t069, -chinh, -lap, -thu, e2e-t066}.json` | bỏ | Chép vào `tu-lab/` |
| — | `rca/method.lock` (mới) | Commit repo RCA, `sha_ma_nguon` `b0f79a4d…`, danh sách file kèm sha256, ghi chú quy ước byte CRLF (RR1) |
| `load/controller/*`, `load/fixtures/*`, `load/profiles/purchase-journey.json`, `load/scenarios/purchase-journey.js` | giữ | Sửa đường dẫn. `fixture.py` vẫn trỏ `/opt/rca-tai`, vì thư mục đó giữ nguyên theo Q5 |
| `load/scenarios/legacy/*.js` (2 file) | bỏ | Có ở RCA `results/T-062/` |
| `load/profiles/legacy/workload-t062.json` | bỏ | Chép vào `tu-lab/` |
| `faults/README.md`, `faults/mocks/vnpay/*`, `faults/toxiproxy/proxies.json` | giữ | |
| `faults/injectors/docker/inj3.py` | `faults/injectors/docker/inject.py` | Đường trạng thái `/home/ubuntu/t063/inj` đổi theo §7.2 |
| `observability/compose.yaml`, `collector/*`, `loki/`, `prometheus/`, `tempo/` | giữ | `compose.yaml` khai `name: flash-ticket-obs-pinned`. File cấu hình collector không đổi nội dung (B7) |
| `observability/compose.t073-webhook.yaml` | `observability/alert-receiver/compose.yaml` | Giữ `name: t073-webhook` và tên container. Bind nguồn `./t072-bo-nhan` → `.`; `../campaigns/online` → `../../rca/online` |
| `observability/t072-bo-nhan/bo_nhan.py` | `observability/alert-receiver/bo_nhan.py` | Không sửa nội dung |
| `observability/grafana/{README.md, build_dashboards.py}`, `provisioning/datasources/*`, `provisioning/dashboards/providers.yaml` | giữ | Sửa đường dữ liệu. `build_dashboards.py` đọc nguồn quá khứ bằng `git show ab1c52c:<đường cũ>`; giữ nguyên các đường đó |
| `dashboards/00-start-here/t065-l5-muc-luc.json` | `dashboards/00-start-here/start.json` | UID giữ (§7.5) |
| `dashboards/10-system/flashticket-he-thong.json` | giữ | |
| `dashboards/20-incidents/t065-l8b-rca.json` | `dashboards/20-incidents/rca-incidents.json` | UID giữ |
| `dashboards/30-replay/t065-l8b-phat-lai.json` | `dashboards/30-replay/rca-replay.json` | UID giữ |
| `dashboards/90-archive/*` (6 file, không được nạp) | bỏ | 4 file có ở RCA `results/T-065/grafana*`; 2 file G2 chép vào `tu-lab/` |
| `provisioning/alerting/t072-luat.yaml` | `provisioning/alerting/rules.yaml` | Chỉ đổi `folder:` và `name:` của nhóm (B11). Ghi đầu file: "đổi tên từ đầu ra của `results/T-072/sinh_luat_grafana.py`; script đó sinh ra `t072-luat.yaml` bản cũ" |
| `provisioning/alerting/{t072-thu-e3-go.yaml, t073-e5-go.yaml}` | bỏ | Trước khi bỏ: đọc Grafana (API) để chắc 4 luật thử và contact point `t073-webhook-e5` không còn. Còn thì giữ file. Chép vào `tu-lab/` |
| `provisioning/alerting/t072-hoan-tac-n.yaml.mau` | bỏ | Chép vào `tu-lab/` |
| `provisioning/README.md`, `rca-service/README.md` | bỏ | Thư mục chỉ có README ghi "chưa làm" |
| `tests/signals/*` | giữ | |

## 7. Bảng dời: ba máy, tên trong Grafana

Mọi dời trên máy dùng `mv` trong cùng một filesystem: obs và app là `/dev/sda1`, máy tải là `/dev/root`. `mv` đổi tên tại chỗ, giữ chủ, quyền và byte. Không chép lại từ git.

### 7.1 obs

| Cũ | Mới | Ai dùng / việc phải làm |
|---|---|---|
| `/opt/rca-lab` (@`1bb40ca`) | `/opt/flashticket-rca` | Working dir của compose quan sát và bộ nhận cảnh báo |
| `/etc/rca-lab/{grafana.env, controller/, credential-hash-catalog.json}` | `/etc/flashticket-rca/` | Biến `RCA_LAB_SECRETS`, `RCA_LAB_CONTROLLER_KEYS` |
| `/srv/rca-lab/collector-gateway` (5 GB, ghi vòng) | `/srv/flashticket-rca/collector/` | Bind vào gateway. `stage_m1` và `stage_b` đọc qua `RCA_CAPTURE` |
| `/srv/rca-lab/m1` (19 GB) | `/srv/flashticket-rca/rca/` | Gốc M1, gồm 30 ca (có ca của lượt T-069). Đổi quyền `rca/` thành 755; các con giữ quyền cũ (B6) |
| `m1/t073-dev` (5,5 GB), `m1/t069-phan-tich` | `archive/2026-11/m1/` (root:rca 750) | Dữ liệu dev của E5 và phân tích T-069 |
| `/srv/rca-lab/m1-snapshots/b0f79a4d…` | `/srv/flashticket-rca/rca/method/b0f79a4d…` | `RCA_M1_CODE` (4 file viết cứng) |
| `/srv/rca-lab/venv-m1` | `/srv/flashticket-rca/rca/venv/` | Dựng lại (B4). Venv cũ giữ ở archive tới khi B4 và B13 đạt |
| `/srv/rca-lab/rca-results/t065-l11-001` | `/srv/flashticket-rca/rca/results/dev/` | Q2. Bộ dữ liệu của 3 dashboard đang hiện. URL Infinity `public/rca/t065-l11-001/` → `public/rca/dev/` |
| `rca-results/{t065-l3, l4, l8, l8b-001, t073-dev-001, t073-e5-001, *.json, chi-muc, mau, phat-lai}` | `archive/2026-11/rca-results/` | Không dashboard đang nạp nào đọc |
| Bind Grafana `/srv/rca-lab/rca-results → public/rca` | `/srv/flashticket-rca/rca/results → public/rca` | `compose.yaml` |
| `/srv/rca-lab/ledger` | `/srv/flashticket-rca/ledger/` | `ledger_append.py` và danh sách cấm của `run_m1.py`. Không có luật sudoers riêng |
| `/var/lib/flash-ticket-ledger` | giữ | Thư mục nhà của user hệ thống `ledger` |
| `/srv/rca-lab/runs/*` (39 mục, trừ hai mục dưới) | `archive/2026-11/runs/` (ubuntu 700) | Có tên ô trong nhật ký (B6) |
| `/srv/rca-lab/runs/t072-e3-01/webhook.jsonl` | `archive/2026-11/runs/t072-e3-01/` | Đầu ra cũ của bộ nhận. Bộ nhận mới ghi vào `alerts/bo-nhan/` (K7) |
| `/srv/rca-lab/runs/t072-e3-01-cfg/webhook.env` | `/srv/flashticket-rca/alerts/receiver.env` | Sửa giá trị `T072_RA_DIR` thành `/srv/flashticket-rca/alerts/bo-nhan`. Bản cũ giữ trong archive để hoàn tác |
| `runs/STOP` (cờ của runner, orchestrator, `chuoi_tai`) | `/srv/flashticket-rca/runs/STOP` | ubuntu tạo và xóa. Trước khi dời: kiểm cờ không có mặt |
| `load-controller/STOP` (cờ của `tai_linux`, `chuoi_tai`) | `/srv/flashticket-rca/load/STOP` | Như trên. Không gộp hai cờ, vì gộp là đổi hợp đồng I8 |
| `/srv/rca-lab/load-controller/{tai-linux-events.jsonl, tai-linux.lock}` | `/srv/flashticket-rca/load/` | K4; biến `RCA_LAB_LOAD_STATE` |
| `/srv/rca-lab/load-controller/tai-out/` (47 tag, 3,5 GB) | `archive/2026-11/load-tai-out/` | Bản k6 thô. Repo RCA đã có bản tóm tắt theo phút |
| `/srv/rca-lab/trace-goi` (2 GB) | `archive/2026-11/trace-goi/` | `service_graph.py --goi` cho ca lịch sử |
| `/srv/rca-lab/rca-results-chep-2026-11-17.sha256`, `/home/ubuntu/t063` | `archive/2026-11/` | |
| Lịch chạy cho runner (`--lich`) | `/srv/flashticket-rca/runs/<ngày>-<mục-đích>/lich.json` | Chép từ repo RCA trước lượt. Runner băm đúng file này |
| Volume `flash-ticket-obs-pinned_*` | giữ | §5.3 |

### 7.2 app

| Cũ | Mới | Ai dùng / việc phải làm |
|---|---|---|
| `/opt/rca-lab` (@`407b4f5`) | `/opt/flashticket-rca` (cùng commit với obs) | Collector agent. Runner gọi `inject.py` qua SSH |
| `/etc/rca-lab/{collector.env, payment-ngrok-gia.env}` | `/etc/flashticket-rca/` | `agent-compose.yaml`, override của payment |
| `/srv/rca-lab/collector-agent` | `/srv/flashticket-rca/collector/` | Bind vào agent |
| `/srv/rca-lab/backups/t067-20261118` | `archive/2026-11/backups/` | |
| `/opt/flash-ticket-src` | `/opt/flashticket/src` | Có `.git/worktrees`: chạy `git worktree repair` sau khi dời |
| `/opt/flash-ticket-build/t067-36a3725d` | `/opt/flashticket/build/36a3725d` | Nơi dựng image đang chạy |
| `/opt/flash-ticket-build/t067-36a3725d-logs` | `archive/2026-11/build/` | |
| 13 checkout còn lại ở `/opt/flash-ticket-build/` | xóa (§11) | |
| `/opt/flash-ticket-build/t067-compose/` (cả thư mục, gồm `hieu-luc/`) | `archive/2026-11/compose-t067/` | **Đích hoàn tác** cho bước 3. Giữ tới khi Minh xác nhận không cần hoàn tác nữa |
| — | `/opt/flashticket/compose/*.yml` | Dựng lại bằng `hieu_luc.py` với đường mới; so theo B8 |
| `/opt/flash-ticket-app/compose-exp/keycloak.yml` | `/opt/flashticket/compose/keycloak.yml` | |
| `/opt/flash-ticket-app/env-t062/*.env` (7 service, đang dùng) | `/opt/flashticket/env/` | |
| `/opt/flash-ticket-app/env/{keycloak.env, client-secrets.json, test-users.json, l1-buyers.json}` | `/opt/flashticket/env/` | `auth.py` đọc `test-users` và `l1-buyers`. Không trùng tên với 7 file trên |
| `/opt/flash-ticket-app/env/*-service.env`, `*.truoc-thu-*`, `env-t062/*.bak-*` | `archive/2026-11/env/` | Bản cũ, không compose nào dùng |
| `/opt/flash-ticket-infra/` | `/opt/flashticket/infra/` | K2. Project `flash-ticket-infra` giữ tên (volume DB) |
| Mount MongoDB `../../docs/architecture/data/mongodb/schema.cjs` | Tự phân giải thành `/opt/flashticket/docs/architecture/data/mongodb/schema.cjs` | Đường tương đối tính từ `infra/deploy`. Nguồn hiện tại `/opt/docs/…/schema.cjs` là **thư mục rỗng** do Docker tự tạo (`stat`: directory), nên file schema chưa từng được gắn. Sau dời Docker lại tự tạo thư mục rỗng ở đường mới, hành vi như cũ. Không sửa lỗi có sẵn này trong đợt dọn. `/opt/docs` cũ chuyển vào archive. Kiểm: loại mount và đích trùng trước dời |
| `/opt/flash-ticket-app/secrets/ticket-qr` | `/opt/flashticket/secrets/ticket-qr` | K2; bind vào ticket-service |
| `/opt/flash-ticket-app/otel` | `/opt/flashticket/otel` | K2; bind vào Keycloak |
| `/opt/flash-ticket-app/rca-faults/<svc>/{control,audit}` | `/srv/flashticket-rca/faults/<svc>/` | K3; bind vào booking và event (uid 10001, 750) |
| `/home/ubuntu/t063/inj` | `/srv/flashticket-rca/faults/inject-state/` | K3; `inject.py`. **Sửa nội dung** file `compose-dir` từ `/opt/flash-ticket-build/t067-compose/hieu-luc` thành `/opt/flashticket/compose` |
| `/home/ubuntu/t063/thu3` | `archive/2026-11/home/t063/thu3` | Lịch sử (log build, patch, kết quả thử) |
| `/opt/flash-ticket-app/l1-vnpay` | `/srv/flashticket-rca/faults/vnpay/` (cả thư mục: mã chạy, trạng thái, khóa đường hầm) | Giữ cơ chế chạy hiện tại (R6). Sửa đường `/opt/flash-ticket-app/l1-vnpay` trong `kiem-mock.py` và `tunnel-remote.py`. Dừng hai tiến trình rồi khởi động lại từ chỗ mới bằng chính hai helper này |
| `/opt/flash-ticket-app/rca-toxiproxy/proxies.json` | `/srv/flashticket-rca/faults/toxiproxy/proxies.json` | Tạo lại container `rca-toxiproxy` bằng đúng lệnh `docker run` cũ (đọc ở bước 0, trừ giá trị bí mật), chỉ đổi đường bind |
| `/opt/flash-ticket-app/{collector, compose, compose-t062, state, l1-fixtures}` | `archive/2026-11/flash-ticket-app/` | Không container nào dùng |
| `/home/ubuntu/{t058, t062, t071, *.py, *-t062.*}` | `archive/2026-11/home/` | Gồm `t071/db-moc` |
| Image `ft-local/*:arm64-t067-36a3725d` | giữ | Đang chạy và là đích hoàn tác |
| Volume `flash-ticket-infra_*` | giữ | §5.3 |

### 7.3 tải

| Cũ | Mới | Ghi chú |
|---|---|---|
| `/opt/rca-lab` (@`5a39028`) | `/opt/flashticket-rca` (cùng commit) | |
| `/etc/rca-lab/load-secret` | `/etc/flashticket-rca/load-secret` | `tai_linux.py`, `kiem-token-con-han.py` |
| `/srv/rca-lab/load-runs/` (47 tag) | `archive/2026-11/load-runs/` | Lượt mới ghi vào `/srv/flashticket-rca/runs/<ngày>-<mục-đích>/` |
| `/opt/rca-tai` | **giữ nguyên, không dời, không xóa** | Q5 (DECISIONS 23/11): giữ mục 2.6. `load/fixtures/fixture.py` còn đọc `secret/` và `k6/` ở đây. Kho `D:/RCA-archive` chỉ có `out/` |
| `/home/ubuntu/{x86-check, uvenv, arm-check*.tgz, rec-x86linux.json, dump_rec.py}` | `archive/2026-11/home/` | Chưa rõ hồ sơ nào dẫn tới, nên lưu chứ không xóa |
| Container `rca-tai-*` đã dừng (ít nhất 30) | xóa (§11) | |

### 7.4 Bộ nhận cảnh báo

**Đã quyết (bản 2):** giữ bộ nhận nhẹ chạy liên tục.
- Giữ project `t073-webhook`, container `flash-ticket-t072-bo-nhan`, alias mạng `t072-bo-nhan`, contact point `t072-bo-nhan-nhe` / `t072-webhook`. Nhờ vậy đường gửi của 11 luật không đổi.
- Chỉ đổi:
  - chỗ của file compose và mã (`observability/alert-receiver/`);
  - env file (`/srv/flashticket-rca/alerts/receiver.env`);
  - thư mục ghi (`/srv/flashticket-rca/alerts/bo-nhan/`, ubuntu 700; container chạy uid 1001 = ubuntu).
- **Kiểm sau dời:** container healthy, gửi thử từ Grafana tới contact point (nút "Test"), có một dòng mới trong `webhook.jsonl`.
- **Hoàn tác:** `down` project bằng env file mới, rồi `up` bằng env file cũ trong archive.

### 7.5 Tên trong Grafana, và phần mã task còn lại

**UID giữ nguyên** (Minh duyệt 24/11), vì hai lý do:
- `service_graph.py` đã ghi link `/d/t065-l8b-rca` vào trường `detail__url` của dữ liệu đồ thị đang hiện. Codex đếm được 109/218 file.
- `incidents.py:84-87` lấy mã luật từ nhãn `t072_uid`. Với cảnh báo kiểu NoData hoặc DatasourceError, nó lấy từ `rulename`, tức `title` của luật.

| Loại | Giữ | Đổi |
|---|---|---|
| Dashboard | UID `t065-l5-muc-luc`, `flashticket-he-thong`, `t065-l8b-rca`, `t065-l8b-phat-lai`; folder uid `rca-*` | Tên file (§6). Tên hiển thị đã không mang mã task |
| Luật cảnh báo | UID `t072-*`, `title` `t072-*` (dùng làm `rulename`), nhãn `t072_uid`, `t072_loai` | Folder "T-072 W4 cảnh báo" → "Cảnh báo FlashTicket"; nhóm `t072-w4` → `canh-bao` (RR2) |
| Contact point | `t072-bo-nhan-nhe`, `t072-webhook` | — |

**Phần còn mang mã task sau khi dọn**, ghi cả vào `docs/ten-cu-moi.md` để người đọc hiểu:
- UID dashboard (thấy trong URL);
- UID, tên và nhãn luật cảnh báo;
- contact point; project và container bộ nhận (`t073-webhook`, `t072-bo-nhan`);
- tag image `arm64-t067-36a3725d`; nhãn container `t062=topology` của toxiproxy (container được tạo lại không gắn nhãn này);
- thư mục `results/T-*` bên trong bản chụp mã;
- các đường lịch sử trong `build_dashboards.py` và `docs/sources-2026-11.md`;
- tên trong `archive/`.

Đổi những tên này là đổi dữ liệu bằng chứng, hoặc đổi hợp đồng gom sự cố, nên không làm trong đợt dọn.

## 8. Chỗ phải sửa đường dẫn

Đếm trên lab `main` = `4b6c4b2`:

| Chuỗi | Lệnh | Số file |
|---|---|---|
| Đường máy cũ | `git grep -l -E '/opt/rca-lab\|/srv/rca-lab\|/etc/rca-lab' main` | 32. Codex đếm 34 bằng lệnh khác; chưa phân xử, không ảnh hưởng cách làm vì bước 1 dùng phép `git grep` sau khi sửa |
| `t065-l11-001` | `git grep -c t065-l11-001 main` | 10 (hai dashboard có 28 và 13 chỗ) |
| `from campaigns.lib import inventory` | `git grep -n 'from campaigns' main` | 4 |
| `/opt/flash-ticket-app`, `/opt/flash-ticket-build`, `/opt/flash-ticket-src`, `/home/ubuntu/t063` | cột `duong_dan_may_viet_cung` của `kiem-ke/lab-file.tsv` | theo bảng |

**Quy tắc sửa:**
- Chỉ thay chuỗi đường dẫn, tên module và tên file, cộng L1 và L2 (B5).
- Mỗi chỗ đọc lại trong ngữ cảnh, không thay hàng loạt mù. Riêng hai dashboard được thay hàng loạt, vì B12 kiểm toàn bộ.
- **Không sửa:**
  - bản chụp mã;
  - `SRC_GOC`/`BS_GOC`;
  - `git show ab1c52c:<đường cũ>` trong `build_dashboards.py`;
  - `docs/sources-2026-11.md`;
  - đường bên trong `g1_export.py`.
- **Sau khi sửa:** `git grep` các chuỗi cũ trên `main` mới chỉ còn ở các chỗ "không sửa" trên và ở `docs/ten-cu-moi.md`. Liệt kê kết quả vào LOG.

**Không sửa** đường dẫn trong hồ sơ cũ của repo RCA (597 script đã track). Người đọc tra bằng `docs/ten-cu-moi.md` (lab) và `docs/ARCHIVE-INDEX.md` (RCA).

## 9. Các bước, hoàn tác, gặp lỗi giữa chừng

Mỗi bước cần Minh ra lệnh bắt đầu riêng. Không bước nào dài hơn 1 giờ. Không phát tải, trừ Q4.

**Luật chung khi thao tác trên máy:**
- Trước mỗi bước, ghi vào LOG danh sách lệnh dời (cũ → mới) và lệnh ngược tương ứng.
- Sau mỗi lệnh `mv`, ghi một dòng LOG.
- **Nếu đứt SSH:** không chạy lại nguyên bước. Đọc trạng thái từng dòng trong danh sách (nguồn còn hay đích đã có, project nào đang chạy), rồi làm tiếp từ dòng chưa xong.

**Bước 0. Chụp hiện trạng (chỉ đọc, ba máy).** Ghi vào `results/T-070/don/truoc/`. Không lưu giá trị bí mật (§4).
- sha256 của bản chụp M1, pins, config, cấu hình V082.
- `pip freeze --all` và `python --version` của venv cũ.
- sha256 toàn cây `t065-l11-001`.
- Với mọi container: tên, image, project, file compose, env file, mount (nguồn, đích, loại, rw/ro), tên biến và hash giá trị từng biến.
- Lệnh `docker run` của `rca-toxiproxy`: các cờ, không ghi giá trị bí mật.
- Nội dung `/home/ubuntu/t063/inj/compose-dir` (chỉ là một đường dẫn).
- Danh sách luật (uid, title, folder, nhóm), dashboard (uid, folder) và contact point, đọc qua API Grafana.
- Một truy vấn mẫu Prometheus, Loki và Tempo trên một khoảng cố định trước ngày dời (đếm chuỗi hoặc dòng). Đếm đơn hàng trong DB bằng truy vấn đọc.
- Quyền và chủ của các thư mục sẽ dời. Phép `sudo -u rca test -r` (B6).
- `grep` các đường cũ trong `/opt`, `/etc`, `/home` của ba máy, để tìm script hoặc cấu hình nằm ngoài kiểm kê (RR4).
- Kiểm cờ STOP: không có mặt.

**Bước 1. Laptop, chưa đụng máy.**
1. Gắn tag `truoc-don-2026-11` lên lab `main` và push tag.
2. Tạo nhánh dọn:
   - `git mv` theo §6;
   - sửa đường theo §8;
   - thêm L1, L2, `method.lock`, `ten-cu-moi.md`;
   - khai `name:` trong các file compose.
3. Kiểm offline:
   - `python -m py_compile` mọi file `.py`;
   - `docker compose config --quiet` cho từng file compose, với env giả không chứa bí mật;
   - nạp thử `sau_v082.nap_bo_xuat` với thư mục giả, để chắc L2 nạp được `g1_export.py` và đếm đúng một chỗ cho mỗi chuỗi mẫu;
   - đọc diff theo B5; kiểm B11, B12;
   - `git grep` chuỗi cũ theo §8.
   `kiem-hop-dong.py` **không** dùng làm phép kiểm: hai test của nó đã lỗi từ trước khi dọn (§12).
4. Chép các file K6 vào `results/T-070/don/tu-lab/`.
5. Minh duyệt diff, rồi merge vào `main`.

Hoàn tác: chưa merge thì bỏ nhánh; đã merge thì revert.

**Bước 2. obs.** Không có lượt chạy nào. Dữ liệu agent gửi sang trong vài phút gateway dừng có thể mất.
1. `docker compose down` project `t073-webhook` (bộ nhận), dùng env cũ. Down project này trước, vì nó dùng chung mạng với bộ quan sát.
2. `docker compose down` bộ quan sát. Không dùng `-v`.
3. Tạo các thư mục mới theo bảng quyền §5.3. `mv` theo §7.1. Checkout commit mới vào `/opt/flashticket-rca`.
4. Dựng venv mới; kiểm B4.
5. `up` bộ quan sát (project `flash-ticket-obs-pinned`). Kiểm `docker volume ls`: không có volume mới (RR3).
6. `up` bộ nhận bằng `alerts/receiver.env`.
7. Kiểm B2, B3, B6, B9 (phần obs), B10, B11, B12, và bộ nhận theo §7.4.

Hoàn tác:
- `down` cả hai project.
- `mv` ngược theo danh sách đã ghi; checkout `1bb40ca`.
- `up` bộ quan sát; `up` bộ nhận bằng env cũ.
- Nếu Grafana đã nạp folder hoặc nhóm mới: commit cũ khai lại folder và nhóm cũ, Grafana chuyển luật về. Folder mới, nay rỗng, xóa qua API.
- Volume không bị đụng.

**Bước 3. app.** FlashTicket thử nghiệm ngừng; ước lượng 10–15 phút, chưa đo.
1. Dừng theo thứ tự ngược: VNPay giả và đường hầm → agent → 7 service → Keycloak → toxiproxy → hạ tầng `flash-ticket-infra`. `docker compose down` không dùng `-v`.
2. Tạo thư mục mới theo §5.3. `mv` theo §7.2. `git worktree repair`. Sửa nội dung `compose-dir`. Checkout commit mới vào `/opt/flashticket-rca`.
3. Dựng lại cấu hình hiệu lực bằng `hieu_luc.py`; kiểm B8 trên máy.
4. Bật theo thứ tự:
   1. hạ tầng;
   2. **toxiproxy** (event và booking nối DB, Redis, RabbitMQ qua toxiproxy; `proxies.json` khai 4 cổng nghe: 15433, 16379, 15673, 18082);
   3. Keycloak, discovery, các service (`deploy.sh` chờ health và đăng ký Eureka từng service);
   4. agent;
   5. VNPay giả và đường hầm, bằng `kiem-mock.py` và `tunnel-remote.py`.
5. Kiểm B7, B8, B9 (DB), mount MongoDB (§7.2), cổng 19091 trên máy tải.

Hoàn tác: dừng như mục 1 → `mv` ngược → checkout `407b4f5` → `up` bằng bộ Compose T-067 trong `archive/2026-11/compose-t067/` → trả lại nội dung `compose-dir` cũ. Image và volume không bị đụng.

**Bước 4. tải.** `mv` theo §7.3, rồi checkout. Không có dịch vụ thường trực trên máy này.

**Bước 5. Kiểm sau dời:** §10.

**Gặp lỗi giữa chừng:**
- Lỗi ở bước nào thì dừng ở bước đó, không đi tiếp.
- Lỗi của chính việc dời (thiếu file, sai đường): sửa đường, hoặc `mv` ngược phần đó. Không làm lại phần đã đạt.
- Lỗi chạm tới B1–B4, B6 hoặc B13 (phương pháp hoặc cách ly nhãn): dừng toàn bộ, hoàn tác máy đó, báo Minh. Đây là lỗi tính đúng, không vá tại chỗ.
- Lỗi hạ tầng (mất SSH, máy treo): không ghi thành kết quả. Làm tiếp theo luật đứt SSH ở trên.

## 10. Kiểm sau khi dời

Tiêu chí của từng phép kiểm được khai ở đây, trước khi chạy.

| Kiểm | Đạt khi |
|---|---|
| B1–B12 | Như cột "Cách chứng minh" ở §4 |
| B13 / Q3: hồi quy V082 | Chạy bằng user `rca`, venv mới, bản chụp ở chỗ mới, đích là thư mục mới `rca/hoi-quy-sau-don/` (rca 750, chưa tồn tại). `v082-hoi-quy/` giữ chỉ đọc. Lệnh từng ca theo `results/T-066/hoi-quy-v082.json#/ghim/lenh`, thay đường mới:<br>`sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -B <method>/src/m1_ft/chay_ca.py --id <ca> --cau-hinh <method>/results/T-064/bien-the/V082-V066+H8a/cau-hinh.json --ban V082-V066+H8a --ra <rca>/hoi-quy-sau-don --goc <rca> --bo-sung <rca>/bo-sung-hoi-quy/{id}/prometheus-bo-sung.json`<br>Ca `46aab4be`: không thêm cờ (dùng `outputs/46aab4be/method-input.json`). Ca `ebd5ef38`: thêm `--dung-lai-dau-vao`, vì `outputs/ebd5ef38/method-input.json` không có trên máy, giống T-066 (`dung_lai_dau_vao: true`). Đạt khi cả hai lần chạy của mỗi ca trùng byte với chuẩn: `573df32d…`, `563f449d…` |
| Grafana | 4 dashboard có dữ liệu. Bấm một nút thường và một nút chú thích trong dữ liệu đồ thị: tới đúng dashboard. 11 luật ở folder "Cảnh báo FlashTicket", UID như cũ. Datasource kiểm đạt |
| Bộ nhận cảnh báo | Theo §7.4 |
| Tín hiệu / Q4 | Đúng tiêu chí đã khai từ trước, `tests/signals/tieu-chi.json#/buoc_7`: một lượt mua vé 10 phút mức x1 cộng một GET `/api/v1/me`, rồi chạy `tests/signals/run_remote.sh`. Đạt theo các điều kiện trong file đó. Phần nào script trả `chua_kiem` thì ghi chưa kiểm. Phép này kiểm telemetry, không kiểm bước chụp dữ liệu và G1 (RR7) |
| Tên | `find` trên ba máy: không còn đường `rca-lab`, `flash-ticket-app`, `flash-ticket-build`, `flash-ticket-src`, `flash-ticket-infra` hay tên t0xx, ngoài các ngoại lệ §7.5 và `/opt/rca-tai` (Q5) |
| Lưu trữ | `archive/2026-11/README.md` mỗi máy khớp `du` thực tế. `docs/ARCHIVE-INDEX.md` có đủ dòng |

## 11. Việc nhẹ làm kèm

Việc làm lại được, không cần bàn. Mọi lệnh xóa vẫn trình Minh trước khi chạy.

- Xóa image và build cache không dùng trên app. Giữ image đang chạy và image mà bộ Compose T-067 trong archive cần.
- Xóa 13 checkout build cũ.
- Xóa các container k6 đã dừng trên máy tải.

## 12. Ngoài phạm vi dọn: việc sau

| Việc | Hiện trạng đã kiểm | Đề xuất |
|---|---|---|
| Cho VNPay giả và đường hầm chạy dưới Compose | `tai_linux.py:189-210` tự khôi phục bằng tiến trình chạy trần qua hai helper | Lượt riêng. Sửa hai helper để chỉ một nơi khởi chạy |
| Hai test lỗi trong `kiem-hop-dong.py` | `ctl.start(args, {})` rồi đọc `manifest['labCommit']`; test hash nguồn chờ kiểm hash cũ, trong khi `verify_sources()` kiểm git | Sửa đầu vào và kỳ vọng của test theo hợp đồng commit hiện hành. Không sửa bộ tải để chiều test cũ |
| Bật agent OTel trên FlashTicket thật (K8s, máy 84) | Image có agent, mặc định tắt; K8s chưa có nơi nhận | Bật khi máy 84 nối được với obs (Y11) |
| Nối máy 84 vào obs | Gateway chỉ nghe IP nội bộ `10.0.0.215`; iptables của obs chỉ nhận `10.0.0.0/24` và SSH | Sửa 4 chỗ: cho gateway nghe IP công khai, mở iptables cho IP máy 84, mở Security List Oracle (Minh làm trên giao diện), thêm xác thực. Luật và dashboard lọc theo `deployment.environment` |
| Merge PR #17 vào main của nhóm | 13 file xung đột. Hook tiêm lỗi chỉ ở `src/rca-test/` | Trước khi merge, đọc từng dòng 39 file nghiệp vụ được chèn lệnh ghi log |
| Dùng FlashTicket bản mới nhất trên app (Y12) | App chạy bản ghim `36a3725` | Đổi bản là đổi hệ thống được đo, nên kết quả trước và sau không so trực tiếp. Làm thành bước riêng sau đợt dọn, có kiểm tín hiệu lại |
| Lỗi mount `schema.cjs` của MongoDB | Nguồn là thư mục rỗng do Docker tự tạo | Báo nhóm hệ thống hoặc sửa khi nâng bản FlashTicket |
| Đổi UID / tên luật sang tên không mã task | Bị chặn bởi dữ liệu đồ thị và hợp đồng gom sự cố (§7.5) | Chỉ làm nếu Minh muốn, kèm bộ hiển thị dẫn xuất và sửa `incidents.py` |
| `/opt/rca-tai` (Q5) | Còn được `fixture.py` dùng | Minh quyết khi bỏ hoặc thay CLI `fixture.py` |
| Hạn bán sự kiện tải | Hết 02/12/2026 22:16Z | Minh quyết sau |
| W7 | Hoãn | Mở lại sau khi dọn xong |
| `docs/READING-GUIDE.md` của repo RCA | Có nhắc đường lab cũ | Sửa đường sau khi lab merge (cần duyệt) |

## 13. Rủi ro và điểm chưa kiểm

| # | Điểm | Trạng thái | Nếu sai thì sao | Cách phân xử |
|---|---|---|---|---|
| RR1 | Hash bản chụp `b0f79a4d…` tính trên byte CRLF; 26/149 file khác blob git | Đã kiểm | Dựng lại bản chụp từ git ra hash khác | Đợt này chỉ `mv`. `method.lock` ghi quy ước byte. Cách dựng bản chụp mới là việc sau |
| RR2 | Đổi `folder:` và `name:` nhóm trong provisioning có chuyển luật (giữ UID) mà không tạo bản trùng không | Chưa kiểm | Luật trùng, hoặc lỗi nạp provisioning | Bước 2 đọc API: đúng 11 luật, UID như cũ. Lỗi thì giữ tên nhóm cũ, chỉ đổi folder; vẫn lỗi thì hoàn tác |
| RR3 | `name:` trong compose có giữ đúng project và volume khi working dir đổi không | Chưa kiểm trên máy | Volume mới rỗng; dữ liệu trông như mất nhưng vẫn còn trong volume cũ | Bước 1: `docker compose config` xem tên project. Bước 2: `docker volume ls` trước khi đi tiếp |
| RR4 | Script hoặc cấu hình ngoài kiểm kê còn trỏ đường cũ | Kiểm kê không thấy cron hay unit tự tạo | Lỗi khi chạy sau | `grep` ở bước 0 |
| RR5 | Đường hầm VNPay phụ thuộc khóa và cổng 19091 trên máy tải | Đã kiểm cổng đang nghe | Luồng thanh toán của k6 lỗi | Kiểm ở bước 3.5 và Q4 |
| RR6 | Hồ sơ nào dẫn tới `x86-check` và các file khác trên máy tải | Chưa kiểm | Không ảnh hưởng: chỉ lưu, không xóa | — |
| RR7 | B13 phủ lõi V082, không phủ bước chụp dữ liệu (`stage_m1`, `stage_b`) và xuất G1 | Đã biết | Lỗi đường dẫn ở bước chụp hoặc xuất không lộ qua hồi quy | B5 (đọc diff), phép nạp thử L2 ở bước 1. Đề xuất thêm (chưa duyệt, không bắt buộc cho tiêu chí xong): phát lại một ca cũ từ `m1/t073-dev/sim-capture/` (nay trong archive) theo `check_old_case.py` vào đích `online-*` mới, so gói, đầu vào, đầu ra V082 và G1 với bản cũ. Dữ liệu cố định, không phát tải |
| RR8 | Thời gian app ngừng | Ước lượng, chưa đo | Kéo dài hơn dự kiến | Không có lượt chạy nào phụ thuộc trong lúc dọn |
| RR9 | Đếm 32 hay 34 file chứa đường máy cũ | Chưa phân xử | Không ảnh hưởng: tiêu chí là `git grep` sau khi sửa | — |

## 14. Nguồn dữ kiện

- **Kiểm kê chỉ đọc** `results/T-070/kiem-ke/`: README, 14 bảng TSV, `tho/`, SHA256SUMS 49/49. Codex tính lại và cũng ra 49/49.
- **Đọc thêm có sudo, chỉ đọc**, ngày 24/11 (LOG T-070 lúc 12:05Z, 13:20Z, 15:40Z):
  - kích thước và quyền `/srv/rca-lab/*` và `m1/*`;
  - compose project và volume;
  - `/etc/sudoers.d`;
  - `v082-hoi-quy`;
  - quyền `runs/` và phép `test -r` bằng user `rca`;
  - nội dung `compose-dir`;
  - mount MongoDB;
  - filesystem máy tải;
  - `outputs/ebd5ef38`.
- **Code lab** `main@4b6c4b2`: `sau_v082.py:28-46`, `g1_b.py:78,97`, `service_graph.py:47`, `incidents.py:84-91`, `tai_linux.py:189-210,263`, `chuoi_tai.py:63-65`, `kiem-hop-dong.py:35,85`, `compose.t073-webhook.yaml`.
- **Code RCA**: `src/m1_ft/chay_ca.py:28-55,124`.
- **Hồ sơ**: `results/T-066/{thay-doi-may.md, hoi-quy-v082.json, danh-sach-xoa.md}`; `docs/DECISIONS.md` (Q5 ngày 23/11).
- **Phản biện**: `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md` (Codex, lượt 1) và bảng phản hồi ở cuối file đó.

## 15. Đối chiếu sửa theo phản biện lượt 1

| Điểm | Sửa ở đâu trong bản 2 |
|---|---|
| R1 bí mật ở bước 0 | §4 (đoạn "Không lưu giá trị bí mật"), §9 bước 0 |
| R2 bộ xuất G1 | §6 (L1, L2, dòng `g1_export.py`), §9 bước 1.3 (phép nạp thử) |
| R3 link trong dữ liệu đồ thị | §7.5 (giữ UID), B10, B12, §10 Grafana (bấm nút) |
| R4 quyền khi dời nhật ký | §5.3 (bảng quyền), B6, §7.1 |
| R5 thứ tự bật app, `compose-dir`, MongoDB, hoàn tác T-067, đứt SSH | §9 bước 3, §7.2, §9 (luật đứt SSH) |
| R6 VNPay và đường hầm | §7.2 (giữ cơ chế hiện tại), §12 |
| R7 các phép kiểm | B4, B13, §10 (lệnh từng ca, Q4 dùng đúng 10 phút), §9 bước 1.3 (bỏ `kiem-hop-dong.py`), §12 |
| R8 UID luật, bộ nhận, hoàn tác | §7.4, §7.5, B11, §9 bước 2 |
| R9 `/opt/rca-tai`, `t063/thu3` | §7.3, §7.2, §2 |
| R10 tiêu chí tên, hai cờ STOP, đếm, filesystem, lịch | §7.5, §10 Tên, §7.1 (STOP, lịch), §8, §7 (filesystem), RR9 |
| N1 thư mục ra của hồi quy | §10 B13 |
| N2 quyền thư mục mới | §5.3 |
| N3 tag image, nhãn container | §7.5 |
| N4 `rules.yaml` không sinh lại được | §6 |

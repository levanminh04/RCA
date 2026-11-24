# Kế hoạch dọn repo lab và ba máy thực nghiệm

Bản 1, 24/11/2026. Người soạn: Claude (phiên T-070). Người phản biện: Codex.

Đây là file kế hoạch duy nhất cho việc dọn. File này thay bản nháp `BANG-DOI.md` cùng thư mục; toàn bộ nội dung bản nháp đã gộp vào mục 6–7.

**Trạng thái:** chưa dời, chưa sửa gì trên máy hay trong repo lab. Minh đã duyệt khung thư mục (mục 5). Các phần khác của kế hoạch chưa được duyệt: các chỗ khung chưa có (K1–K6), các quyết định Q1–Q3, và lệnh bắt đầu từng bước.

## Mục lục

1. Mong muốn của Minh
2. Quyết định đã có và đang chờ
3. Mục tiêu và tiêu chí xong
4. Bất biến: không được làm lệch phương pháp và dữ liệu
5. Khung đích
6. Bảng dời: repo lab
7. Bảng dời: ba máy, UID Grafana
8. Chỗ phải sửa đường dẫn
9. Các bước thực hiện, hoàn tác, gặp lỗi giữa chừng
10. Kiểm sau khi dời
11. Việc nhẹ làm kèm
12. Ngoài phạm vi dọn: việc sau
13. Rủi ro và điểm chưa kiểm
14. Nguồn dữ kiện

Ký hiệu máy:
- **obs**: exp-obs, máy quan sát (Grafana, Prometheus, Loki, Tempo, Collector gateway, nơi chạy RCA).
- **app**: exp-app, máy chạy bản FlashTicket thử nghiệm.
- **tải**: máy tải AWS, chạy k6.

---

## 1. Mong muốn của Minh

Trích từ chat ngày 24/11/2026 (nguồn: lịch sử phiên T-070; dòng LOG T-070 lúc 09:25Z, 10:20Z, 11:40Z, 13:20Z).

| # | Mong muốn | Lời Minh (trích ngắn) | Kế hoạch đáp ở |
|---|---|---|---|
| Y1 | Repo lab sạch, cô đọng, đọc hiểu được code. Không để thư mục rỗng hay đặt file lung tung | "cần 1 repo thật clean, cô đọng để đọc hiểu code" | §5, §6 |
| Y2 | Tách vai hai repo: lab là nơi sạch để đọc code; repo RCA là nơi chạy thực nghiệm và lưu hồ sơ | "1 bên để làm nơi clean, đọc hiểu code, 1 nơi là để chạy thực nghiệm" | §5 |
| Y3 | Không đặt tên theo mã task (T-0xx, t063, t064…) trong lab và trên máy. Người ngoài và giảng viên phải đọc hiểu | "toàn thư mục T-0xx thì giảng viên đọc sẽ không hiểu" | §5–7 |
| Y4 | Chốt khung trước, sửa đường dẫn sau. Sửa đường dẫn không được động tới code phương pháp | "chốt các khung trước đi, sửa path tính sau… không động đến code phương pháp" | §4, §8 |
| Y5 | Dọn kỹ, không bất cẩn: dời file hay sửa linh tinh thì cũng hỏng | "đừng đề xuất 1 cách bất cẩn… đề xuất kĩ giúp tôi" | §4, §9, §10 |
| Y6 | Giữ cái thực sự cần cho đồ án cuối cùng. Phần ít giá trị hoặc ít khả năng dùng lại thì giữ trên server, không kéo về laptop, ghi rõ chỗ để sau tìm được | "giữ trên server… đừng lôi về laptop, note rõ để sau có chỗ tìm" | §7, §12 (luật 10) |
| Y7 | Xem lại luật "lưu mọi bước tính toán" và việc lập manifest tràn lan | "về luật agent mà lưu lại mọi bước tính toán thì xem lại" | §2 (A1, A2) |
| Y8 | Chỉ giữ một bản mã phương pháp. V082 là bản chạy chính | "chốt 1 bản thôi không được à? … V082 LÀ CHẠY chính" | §5, §6 (`rca/method.lock`) |
| Y9 | Được đọc trên máy bằng sudo, nhưng không sửa lung tung. Phần nào cần đọc thì đọc | "đừng sửa lung tung, phần nào cần đọc thì hãy đọc" | §9 (bước 0 chỉ đọc) |
| Y10 | Đừng nêu việc nhẹ như việc chính. Việc làm lại được thì ghi là việc nhẹ | "đừng nhắc bất kì 1 việc nhẹ nào mà như thế nào quan trọng" | §11 |
| Y11 | Log, telemetry, giám sát, observability của FlashTicket do Minh toàn quyền quyết, miễn không ảnh hưởng hệ thống | "tôi toàn quyền quyết định… miễn là không ảnh hưởng đến hệ thống" | §12 |
| Y12 | Muốn dùng bản FlashTicket mới nhất cho thống nhất, không thử mãi trên bản cũ | "tôi muốn merge mới nhất để cho thống nhất" | §12 |
| Y13 | Dọn trước W7; E6 dừng hẳn, hạn bán tính sau; W7 hoãn | "dừng toàn bộ… sự kiện hết hạn thì tính sau"; "w7 tạm hoãn" | §2 |
| Y14 | Dừng điều phối, làm trong một phiên. Codex chỉ phản biện khi Minh tự gửi; Codex không dùng subagent | "dừng điều phối nữa… làm ở phiên này thôi"; "dặn codex không dùng subagent" | §9 |
| Y15 | Không đoán, không chữa cháy. Có bằng chứng thì nói, chưa kiểm thì ghi chưa kiểm | "đừng cố giải thích theo kiểu chữa cháy lấp liếm"; "không bịa hay đoán ý" | toàn văn; §13 |
| Y16 | Kế hoạch ghi đủ vào một file để không mất ngữ cảnh | (yêu cầu lượt này) | file này |

## 2. Quyết định đã có và đang chờ

**Đã có** (Minh nói trong chat ngày 24/11). Những dòng này chưa được ghi vào `docs/DECISIONS.md`: khối DECISIONS chiều 24/11 đang chờ Minh duyệt chữ.

- E6 dừng hẳn; hạn bán của sự kiện tải (02/12/2026 22:16Z) tính sau.
- W7 tạm hoãn.
- Dọn làm trước W7. Câu này thay quyết định ngày 23/11 "dọn repo sau W7".
- Minh toàn quyền quyết phần log, telemetry, observability.
- Kiểm kê chỉ đọc: Minh đã duyệt và việc kiểm kê đã xong (`results/T-070/kiem-ke/`).
- Khung thư mục ở mục 5: duyệt ("Duyệt khung").

**Đang chờ Minh** (đề xuất kèm lý do ở chỗ được dẫn):

| Mã | Việc | Đề xuất |
|---|---|---|
| K1–K6 | Những chỗ khung chưa có | §5.4 |
| Q1 | Bộ nhận cảnh báo `t072-bo-nhan` đang chạy | §7.4 |
| Q2 | Tên bộ kết quả dashboard đang hiện | `dev` (§7.1) |
| Q3 | Hồi quy V082 sau dời: chạy lại 2 ca hồi quy | §10. Mất vài phút, không phát tải |
| A1 | Sửa luật 10 (`AGENTS.md`) | "**Giữ mọi lượt chạy**, kể cả lượt hỏng, nhưng chọn nơi giữ theo giá trị: (a) đầu ra làm bằng chứng cho kết luận trong quyển hoặc cần cho bước sau → repo hoặc laptop; (b) phần còn lại (đầu ra thô, nhật ký trung gian, lượt hỏng đã có kết luận) → giữ trên máy ở `/srv/flashticket-rca/archive/`, không kéo về laptop, ghi một dòng vào `docs/ARCHIVE-INDEX.md` (máy, đường dẫn, nội dung, dung lượng, ngày). Không xóa (b) khi Minh chưa duyệt." |
| A2 | Thêm vào luật 4 (`AGENTS.md`) | "Manifest chỉ lập cho dữ liệu nằm ngoài git và được dùng làm bằng chứng; file trong git dùng commit làm vân tay." |
| D1 | Ghi khối DECISIONS chiều 24/11 | Chữ đã trình trong chat |
| G1 | Commit `results/T-070/kiem-ke/` và thư mục này; push `74b2515` | Cần Minh duyệt |

## 3. Mục tiêu và tiêu chí xong

**Mục tiêu.** Sau khi dọn, một người chưa biết dự án (ví dụ giảng viên) có thể:
1. Đọc repo lab, hiểu hệ thống thực nghiệm gồm những phần nào và mỗi phần nằm ở đâu, mà không gặp tên mã task.
2. Đăng nhập một máy bất kỳ và đoán đúng thư mục nào chứa gì.
3. Lần từ một kết quả trong quyển về đúng mã phương pháp đã chạy (commit repo RCA và hash bản chụp) và đúng dữ liệu đầu vào (đường trên máy, hoặc chỗ lưu trữ ghi trong chỉ mục).

Đồng thời, kết quả của phương pháp phải không đổi (§4).

**Tiêu chí xong:**
1. Repo lab `main` khớp khung §5. Không tên file hay thư mục nào mang mã task; ngoại lệ duy nhất là bảng tra tên cũ trong `docs/ten-cu-moi.md`.
2. Ba máy cùng checkout một commit lab, ở `/opt/flashticket-rca`.
3. Mọi bất biến §4 đạt, có lệnh và kết quả ghi trong LOG T-070.
4. Mọi phép kiểm §10 đạt.
5. `archive/2026-11/README.md` trên mỗi máy và `docs/ARCHIVE-INDEX.md` của repo RCA liệt kê đủ những gì đã chuyển vào lưu trữ.
6. Không xóa dữ liệu nào ngoài danh sách việc nhẹ §11 đã được Minh duyệt riêng.

## 4. Bất biến: không được làm lệch phương pháp và dữ liệu

Đây là phần trả lời trực tiếp mong muốn Y4 và Y5. Mỗi bất biến có cách chứng minh. Bước 0 (§9) chụp số đo "trước"; §10 đo lại "sau". Lệch ở đâu thì dừng phần phụ thuộc và báo Minh.

| # | Bất biến | Cách chứng minh |
|---|---|---|
| B1 | Mã phương pháp trong repo RCA (`src/m1`, `src/m1_ft`, `src/p3`) không đổi trong suốt đợt dọn | `git diff` và `git status` trên ba thư mục này rỗng, so với commit lúc bắt đầu |
| B2 | Bản chụp mã trên obs không đổi byte | 149 file trùng sha256 với `kiem-ke/m1-ban-chup.tsv`; tính lại `sha_ma_nguon` ra đúng `b0f79a4d…`. Thư mục được `mv` (cùng ổ), không chép lại từ git (rủi ro CRLF, §13) |
| B3 | Tham số và cấu hình khóa không đổi | sha256 của `m1-source-pins.json`, `m1-p7-config.json`, `flashticket-inventory-source.json`, cấu hình V082 trong bản chụp (runner kiểm hash này trước khi chạy) |
| B4 | Thư viện của V082 không đổi khi dựng lại venv | `pip freeze --all` của venv mới trùng của venv cũ (chụp ở bước 0), và trùng `requirements-m1.txt` |
| B5 | Phía lab chỉ đổi chuỗi đường dẫn và import. Áp cho `run_m1`, `stage_m1`, `stage_b`, `xuat_bo_sung`, `sau_v082`, `g1_b`, `service_graph`, `runner`, `orchestrator`, `incidents`, `inject` | `git diff -M` từ tag `truoc-don-2026-11`, đọc từng hunk: chỉ đường dẫn, tên module, hằng thư mục. Hunk nào khác thì tách ra, trình riêng |
| B6 | Cách ly nhãn giữ nguyên | Sổ tiêm lỗi vẫn `ledger:ledger 700`; `rca/cases` và `rca/outputs` giữ `root:rca` / `rca:rca 750`. Danh sách cấm trong `run_m1.py` trỏ đúng đường sổ mới. Không đường đọc mới nào từ M1 tới sổ |
| B7 | Thu thập telemetry không đổi (đây là đầu vào của phương pháp) | Nội dung `agent-docker-host.yaml` và `gateway.yaml` trùng bản đang chạy. Đã kiểm: `git diff 407b4f5 main -- observability/collector` rỗng. Biến môi trường của container agent và gateway trước và sau chỉ khác giá trị đường dẫn |
| B8 | FlashTicket thử nghiệm chạy đúng cấu hình cũ | Image vẫn `ft-local/*:arm64-t067-36a3725d`. Cấu hình hiệu lực dựng lại (`docker compose config`) chỉ khác cũ ở đường bind và env_file. Nội dung env file trùng sha256 (so tại chỗ, không in giá trị) |
| B9 | Dữ liệu quan sát và DB không mất | Tên compose project và volume giữ nguyên (§5.3). Sau dời, Prometheus, Loki và Tempo truy vấn được một khoảng trước ngày dời; DB FlashTicket còn đơn hàng cũ |
| B10 | Dữ liệu hiển thị không đổi | sha256 toàn cây `rca/results/dev` trùng cây `rca-results/t065-l11-001` trước dời |
| B11 | Luật cảnh báo chỉ đổi định danh | Bỏ `uid`, `title`, nhóm, folder và receiver ở cả hai bản; phần còn lại (biểu thức, ngưỡng, `for`, nhãn, `noDataState`, `execErrState`) trùng nhau |
| B12 | Dashboard chỉ đổi định danh và URL | Thay chuỗi UID cũ → mới và `t065-l11-001` → `dev` trong bản cũ, rồi so: phải trùng bản mới |
| B13 | Phương pháp cho cùng kết quả trên cùng đầu vào | Hồi quy V082 trên 2 ca `46aab4be`, `ebd5ef38` (giống T-066, `results/T-066/hoi-quy-v082.json`) bằng venv mới và bản chụp ở chỗ mới: `method-output-1.json` và `-2.json` trùng byte với `v082-hoi-quy/` |
| B14 | Không mở dữ liệu khóa | Không đụng `data/locked/` của repo RCA |

## 5. Khung đích

Khung này Minh đã duyệt ngày 24/11. Các chỗ khung chưa có (K1–K6) ở §5.4.

### 5.1 Repo lab `flashticket-rca-lab`: nơi đọc hiểu code

```
flashticket-rca-lab/
├─ README.md          sơ đồ hệ thống, cách chạy, link sang mã phương pháp
├─ docs/              kiến trúc, hướng dẫn chạy, ten-cu-moi.md (bảng tra tên cũ → mới)
├─ inventory/         địa chỉ máy, biến cấu hình
├─ test-environment/  cách dựng FlashTicket thử nghiệm trên app (không chứa code FlashTicket)
├─ observability/     collector, prometheus, loki, tempo, grafana (dashboard, luật cảnh báo)
├─ load/              kịch bản k6, mức tải, bộ điều khiển tải
├─ faults/            tiêm lỗi, toxiproxy, VNPay giả và đường hầm
├─ rca/
│  ├─ online/         nhận cảnh báo → gom sự cố → chụp dữ liệu → chạy V082 → kết quả cho Grafana
│  ├─ batch/          chạy hàng loạt theo lịch, sau-V082
│  ├─ lib/            (K1) mã dùng chung cho online và batch
│  └─ method.lock     trỏ tới mã phương pháp: commit repo RCA, hash bản chụp
└─ tests/
```

- Repo lab **không chứa mã phương pháp** (Y8). Mã chỉ nằm ở repo RCA (`src/m1`, `src/m1_ft`, `src/p3`), vì 1.037 script trong `results/` đang dùng tới nó.
- V082 là một cấu hình của M1, nên chạy V082 là chạy mã M1. Hiện chỉ có một bản chụp trên máy (`b0f79a4d…`); `rca/method.lock` ghi đúng bản đó.
- Lịch chạy và hồ sơ của từng lượt thuộc repo RCA, không ở lab.

### 5.2 Repo RCA `RCA-flashticket`: nơi chạy thực nghiệm và lưu hồ sơ

- Giữ đánh số T-0xx: đây là nhật ký nghiên cứu, và hồ sơ cũ dẫn chiếu theo số này.
- Giảng viên đọc qua `docs/READING-GUIDE.md`.
- Thêm `docs/ARCHIVE-INDEX.md`, chỉ mục những gì nằm ở `archive/` trên máy (đi cùng A1).

### 5.3 Trên máy

```
/opt/flashticket-rca/           checkout repo lab (cùng commit trên cả ba máy)
/etc/flashticket-rca/           bí mật, file env của phía RCA
/srv/flashticket-rca/
├─ rca/                         gốc M1 (RCA_M1_ROOT): pins, config, cases/, outputs/, v082/, bo-sung/, *-hoi-quy/
│  ├─ method/<hash>/            bản chụp mã V082 đang chạy
│  ├─ results/<bộ>/             kết quả cho Grafana (bind vào public/rca)
│  └─ venv/                     (K5) venv dựng lại
├─ runs/<ngày>-<mục-đích>/      nhật ký từng lượt chạy; runs/STOP là cờ dừng
├─ ledger/                      sổ tiêm lỗi (user ledger, 700)
├─ collector/                   vùng ghi vòng của Collector (gateway trên obs, agent trên app)
├─ load/                        (K4, obs) trạng thái bộ điều khiển tải
├─ faults/                      (K3, app) control/audit hook, trạng thái inject, VNPay giả
└─ archive/2026-11/             mọi thứ cũ, giữ tên t0xx, có README.md chỉ mục

/opt/flashticket/               (app) FlashTicket thử nghiệm
├─ src/  build/<commit>/  compose/  env/
└─ infra/  secrets/  otel/      (K2)
```

**Không đổi tên compose project.** Volume Docker gắn theo tên project (`flash-ticket-obs-pinned_*`, `flash-ticket-infra_*`). Đổi tên project thì Docker tạo volume rỗng mới. Vì vậy các file compose khai `name:` đúng tên cũ. Tên project không phải đường dẫn, người đọc không thấy trong cây thư mục; chỗ duy nhất phải giải thích là `docs/ten-cu-moi.md`.

### 5.4 Chỗ khung chưa có: cần Minh duyệt

| # | Thứ chưa có chỗ | Đề xuất | Lý do | Phương án khác |
|---|---|---|---|---|
| K1 | Mã dùng chung cho online và batch (`run_m1`, `stage_m1`, `ledger_append`, `safe_export`, `xuat_bo_sung`, `service_graph`, `inventory`) | `rca/lib/` | `orchestrator.py` (online) và runner (batch) cùng gọi các file này | Để trong `batch/` và cho online gọi chéo: khó đọc |
| K2 | Hạ tầng DB, bí mật mã QR vé, javaagent của Keycloak trên app | `/opt/flashticket/{infra,secrets,otel}` | Đều là đồ của FlashTicket; gộp vào `compose/` hay `env/` thì lẫn loại | Gộp vào `compose/` |
| K3 | Trạng thái tiêm lỗi trên app | `/srv/flashticket-rca/faults/` | Dữ liệu RCA sinh ra khi chạy | Đặt trong `runs/`: nhưng nó sống qua nhiều lượt |
| K4 | Trạng thái bộ điều khiển tải trên obs | `/srv/flashticket-rca/load/` | Trạng thái dài hạn của một dịch vụ | Đặt trong `runs/` |
| K5 | Venv V082 | `/srv/flashticket-rca/rca/venv/`, dựng lại | Đi cùng bản chụp | Giữ đường cũ: trái Y3 |
| K6 | File bỏ khỏi lab mà repo RCA chưa có | Chép vào `results/T-070/don/tu-lab/`, kèm commit nguồn | Thuộc phạm vi ghi T-070; không phải sửa task đã đóng | Chép vào `results/T-062/`, `T-066/`, `T-069/`… |

## 6. Bảng dời: repo lab

Ký hiệu:
- **giữ**: giữ nguyên chỗ.
- **bỏ**: bỏ khỏi `main`; bản vẫn còn trong tag `truoc-don-2026-11`, và bảng ghi chỗ bản sao ở repo RCA.

Đặt tên file theo chức năng; chỉ đổi tên file mang mã task hoặc số lượt. Đối chiếu bản sao làm bằng git blob id (`git ls-files -s` của repo RCA so với `git rev-parse main:<file>` của lab).

| Cũ | Mới | Ghi chú |
|---|---|---|
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes` | giữ | Sửa đường dẫn. `AGENTS.md` của lab là file luật: phải duyệt chữ |
| `docs/architecture.md`, `docs/sources-2026-11.md` | giữ | Thêm `docs/ten-cu-moi.md` |
| `inventory/*` | giữ | Sửa đường trong `oracle-exp.env` |
| `app-host/README.md` | `test-environment/README.md` | Sửa tag image cũ ghi trong README |
| `app-host/overrides/*.yml` (7 file) | `test-environment/overrides/` | |
| `app-host/infra/docker-compose.rca-log.yml` | `test-environment/infra/` | |
| `app-host/scripts/{build.sh,deploy.sh,hieu_luc.py}` | `test-environment/scripts/` | `hieu_luc.py`: sửa hằng đường dẫn. `deploy.sh`: đích hoàn tác chuyển sang bản cấu hình hiệu lực trước đó |
| `app-host/scripts/{build,prepare,rollback}-t062.*` | bỏ | Có ở RCA `results/T-062/ha-tang/scripts/` |
| `app-host/scripts/deploy-t062.sh` | bỏ | Chép vào `tu-lab/` (K6) |
| `app-host/services/*.yml` (9 file) | bỏ | Bản `compose-t062` cũ, không service nào chạy từ đây. Chép vào `tu-lab/` |
| `campaigns/` (gói Python) | `rca/` | Sửa 4 chỗ `from campaigns.lib import inventory` |
| `campaigns/{README.md, requirements-m1.txt, __init__.py}` | `rca/` | |
| `campaigns/lib/inventory.py` | `rca/lib/` | K1 |
| `campaigns/online/*` (8 file) | `rca/online/` | |
| `campaigns/runner/{run_m1,stage_m1,ledger_append,safe_export,xuat_bo_sung}.py` | `rca/lib/` | K1. Danh sách cấm của `run_m1.py` chứa chuỗi `'/srv/rca-lab/ledger'`: **bắt buộc** đổi theo đường sổ mới (B6) |
| `campaigns/runner/sau_v082.py` | `rca/batch/sau_v082.py` | Bỏ các đường đã chết (`/opt/flash-ticket-rca/cases`, `/opt/rca-m1ft/bo-sung-dev3`, `~/rca-dieu-phoi/STOP`) |
| `campaigns/runner/runner4.py` | `rca/batch/runner.py` | Bỏ số "4" trong tên |
| `campaigns/g1/service_graph.py` | `rca/lib/` | K1 |
| `campaigns/g1/l8b-xuat.py` | bỏ | Có ở RCA `results/T-065/codex/` |
| `campaigns/g1/relabel_case.py` | bỏ | Việc một lần của T-068; chép vào `tu-lab/` |
| `campaigns/runner/pool_prom.py` | bỏ | Có ở RCA `results/T-063/thu3/scripts/` |
| `campaigns/schedules/{lich-2, lich-3, lich-thu-ngan, lich-thu3-ngan}.json` | bỏ | Có ở RCA `results/T-063/` |
| `campaigns/schedules/{lich-t069, -chinh, -lap, -thu, e2e-t066}.json` | bỏ | Chép vào `tu-lab/`. Lịch mới đặt ở repo RCA, trong task tương ứng |
| — | `rca/method.lock` (mới) | Commit repo RCA, `sha_ma_nguon` `b0f79a4d…`, danh sách file kèm sha256, ghi chú CRLF (§13) |
| `load/controller/*`, `load/fixtures/*`, `load/profiles/purchase-journey.json`, `load/scenarios/purchase-journey.js` | giữ | Sửa đường dẫn |
| `load/scenarios/legacy/*.js` (2 file) | bỏ | Có ở RCA `results/T-062/` |
| `load/profiles/legacy/workload-t062.json` | bỏ | Chép vào `tu-lab/` |
| `faults/README.md`, `faults/mocks/vnpay/*`, `faults/toxiproxy/proxies.json` | giữ | Thêm `tunnel-supervisor.py` và compose cho toxiproxy (việc nhẹ §11) |
| `faults/injectors/docker/inj3.py` | `faults/injectors/docker/inject.py` | Bỏ số bản "3". Đường trạng thái `/home/ubuntu/t063/inj` chuyển sang K3 |
| `observability/compose.yaml`, `collector/*`, `loki/`, `prometheus/`, `tempo/` | giữ | `compose.yaml` khai `name: flash-ticket-obs-pinned`. File cấu hình collector không đổi nội dung (B7) |
| `observability/compose.t073-webhook.yaml`, `observability/t072-bo-nhan/` | bỏ | Theo Q1. Chép vào `tu-lab/` |
| `observability/grafana/{README.md, build_dashboards.py}`, `provisioning/datasources/*`, `provisioning/dashboards/providers.yaml` | giữ | Sửa đường dẫn và UID |
| `dashboards/00-start-here/t065-l5-muc-luc.json` | `dashboards/00-start-here/start.json` | UID ở §7.5 |
| `dashboards/10-system/flashticket-he-thong.json` | giữ | |
| `dashboards/20-incidents/t065-l8b-rca.json` | `dashboards/20-incidents/rca-incidents.json` | |
| `dashboards/30-replay/t065-l8b-phat-lai.json` | `dashboards/30-replay/rca-replay.json` | |
| `dashboards/90-archive/*` (6 file, không được nạp) | bỏ | 4 file có ở RCA `results/T-065/grafana*`; 2 file G2 chép vào `tu-lab/` |
| `provisioning/alerting/t072-luat.yaml` | `provisioning/alerting/rules.yaml` | Đầu file ghi "sinh bởi `results/T-072/sinh_luat_grafana.py`". Đổi UID bằng phép thay chuỗi có ghi lại lệnh; kiểm theo B11 |
| `provisioning/alerting/{t072-thu-e3-go.yaml, t073-e5-go.yaml}` | bỏ | Lệnh xóa chạy mỗi lần Grafana khởi động. Trước khi bỏ, kiểm trong Grafana rằng luật thử và contact point `t073-webhook-e5` không còn. Chép vào `tu-lab/` |
| `provisioning/alerting/t072-hoan-tac-n.yaml.mau` | bỏ | Chép vào `tu-lab/` |
| — | `provisioning/alerting/go-uid-cu.yaml` (dùng một lần) | Xóa 11 luật UID cũ, vì Grafana không tự xóa luật khi file provisioning không còn khai luật đó. Bỏ file sau khi kiểm |
| `provisioning/README.md`, `rca-service/README.md` | bỏ | Thư mục chỉ có README ghi "chưa làm" |
| `tests/signals/*` | giữ | |

## 7. Bảng dời: ba máy, UID Grafana

Mọi dời trên máy dùng `mv` trên cùng ổ (`/opt`, `/srv`, `/etc` đều ở `/dev/sda1` trên cả ba máy). `mv` giữ chủ, quyền và byte. Không chép lại từ git.

### 7.1 obs

| Cũ | Mới | Ai dùng / việc phải làm |
|---|---|---|
| `/opt/rca-lab` (@`1bb40ca`) | `/opt/flashticket-rca` | Working dir của compose quan sát |
| `/etc/rca-lab/{grafana.env, controller/, credential-hash-catalog.json}` | `/etc/flashticket-rca/` | Biến `RCA_LAB_SECRETS`, `RCA_LAB_CONTROLLER_KEYS` |
| `/srv/rca-lab/collector-gateway` (5 GB, ghi vòng) | `/srv/flashticket-rca/collector/` | Bind vào gateway; `stage_m1`, `stage_b` đọc (`RCA_CAPTURE`) |
| `/srv/rca-lab/m1` (19 GB) | `/srv/flashticket-rca/rca/` | Gốc M1. Gồm 30 ca, trong đó có ca của lượt T-069, là bằng chứng nên giữ. `rca/` mở 755; các thư mục con giữ quyền cũ, nên mức cách ly không đổi (B6) |
| `m1/t073-dev` (5,5 GB), `m1/t069-phan-tich` | `archive/2026-11/m1/` | Dữ liệu dev của E5 và phân tích T-069; lượt sau không dùng |
| `/srv/rca-lab/m1-snapshots/b0f79a4d…` | `/srv/flashticket-rca/rca/method/b0f79a4d…` | `RCA_M1_CODE` (4 file viết cứng) |
| `/srv/rca-lab/venv-m1` | `/srv/flashticket-rca/rca/venv/` | Dựng lại (B4); venv cũ chuyển vào archive |
| `/srv/rca-lab/rca-results/t065-l11-001` | `/srv/flashticket-rca/rca/results/dev/` | Q2. Bộ dữ liệu 3 dashboard đang hiện. URL Infinity `public/rca/t065-l11-001/` đổi thành `public/rca/dev/` |
| `rca-results/{t065-l3, l4, l8, l8b-001, t073-dev-001, t073-e5-001, *.json, chi-muc, mau, phat-lai}` | `archive/2026-11/rca-results/` | Không dashboard đang nạp nào đọc |
| Bind Grafana `/srv/rca-lab/rca-results → public/rca` | `/srv/flashticket-rca/rca/results → public/rca` | `compose.yaml` |
| `/srv/rca-lab/ledger` | `/srv/flashticket-rca/ledger/` | `ledger_append.py`; danh sách cấm của `run_m1.py`. Không có luật sudoers riêng (đã đọc `/etc/sudoers.d`) |
| `/var/lib/flash-ticket-ledger` | giữ | Thư mục nhà của user hệ thống `ledger` |
| `/srv/rca-lab/runs/*` (39 mục) | `archive/2026-11/runs/` | `t072-e3-01` và `-cfg` gắn vào container `t072-bo-nhan` (Q1) |
| `/srv/rca-lab/runs/STOP` | `/srv/flashticket-rca/runs/STOP` | runner, `orchestrator.py`, `chuoi_tai.py` |
| `/srv/rca-lab/load-controller/{tai-linux-events.jsonl, tai-linux.lock}` | `/srv/flashticket-rca/load/` | K4; `RCA_LAB_LOAD_STATE` |
| `/srv/rca-lab/load-controller/tai-out/` (47 tag, 3,5 GB) | `archive/2026-11/load-tai-out/` | Bản k6 thô; repo RCA đã có bản tóm tắt theo phút |
| `/srv/rca-lab/trace-goi` (2 GB) | `archive/2026-11/trace-goi/` | `service_graph.py --goi` cho ca lịch sử |
| `/srv/rca-lab/rca-results-chep-2026-11-17.sha256`, `/home/ubuntu/t063` | `archive/2026-11/` | |
| Volume `flash-ticket-obs-pinned_*` | giữ | §5.3 |

### 7.2 app

| Cũ | Mới | Ai dùng / việc phải làm |
|---|---|---|
| `/opt/rca-lab` (@`407b4f5`) | `/opt/flashticket-rca` (cùng commit với obs) | Collector agent; runner gọi `inject.py` qua SSH |
| `/etc/rca-lab/{collector.env, payment-ngrok-gia.env}` | `/etc/flashticket-rca/` | `agent-compose.yaml`, override payment |
| `/srv/rca-lab/collector-agent` | `/srv/flashticket-rca/collector/` | Bind vào agent |
| `/srv/rca-lab/backups/t067-20261118` | `archive/2026-11/backups/` | |
| `/opt/flash-ticket-src` | `/opt/flashticket/src` | Có `.git/worktrees`: chạy `git worktree repair` sau khi dời |
| `/opt/flash-ticket-build/t067-36a3725d` | `/opt/flashticket/build/36a3725d` | Nơi dựng image đang chạy |
| `/opt/flash-ticket-build/t067-36a3725d-logs` | `archive/2026-11/build/` | |
| 13 checkout còn lại ở `/opt/flash-ticket-build/` | xóa (§11) | |
| `/opt/flash-ticket-build/t067-compose/hieu-luc/*.yml` | `/opt/flashticket/compose/` | Dựng lại bằng `hieu_luc.py`; so theo B8 |
| `/opt/flash-ticket-app/compose-exp/keycloak.yml` | `/opt/flashticket/compose/keycloak.yml` | |
| `/opt/flash-ticket-app/env-t062/*.env` (7 service, đang dùng) | `/opt/flashticket/env/` | |
| `/opt/flash-ticket-app/env/{keycloak.env, client-secrets.json, test-users.json, l1-buyers.json}` | `/opt/flashticket/env/` | `auth.py` đọc `test-users`, `l1-buyers`. Không trùng tên với 7 file ở trên |
| `/opt/flash-ticket-app/env/*-service.env`, `*.truoc-thu-*`, `env-t062/*.bak-*` | `archive/2026-11/env/` | Bản cũ, không compose nào dùng |
| `/opt/flash-ticket-infra/` | `/opt/flashticket/infra/` | K2; project `flash-ticket-infra` giữ tên (volume DB) |
| `/opt/docs/architecture/data/mongodb/schema.cjs` | `/opt/flashticket/infra/docs/architecture/data/mongodb/` | Bind vào user-db |
| `/opt/flash-ticket-app/secrets/ticket-qr` | `/opt/flashticket/secrets/ticket-qr` | K2; bind vào ticket-service |
| `/opt/flash-ticket-app/otel` | `/opt/flashticket/otel` | K2; bind vào Keycloak |
| `/opt/flash-ticket-app/rca-faults/<svc>/{control,audit}` | `/srv/flashticket-rca/faults/<svc>/` | K3; bind vào booking, event (uid 10001, 750) |
| `/home/ubuntu/t063/inj` | `/srv/flashticket-rca/faults/inject-state/` | K3; `inject.py` |
| `/opt/flash-ticket-app/l1-vnpay` | Mã chạy từ `/opt/flashticket-rca/faults/mocks/vnpay`; trạng thái → `/srv/flashticket-rca/faults/vnpay/`; khóa đường hầm → `/etc/flashticket-rca/tunnel/` | Việc nhẹ §11 |
| `/opt/flash-ticket-app/rca-toxiproxy/proxies.json` | Bind từ `/opt/flashticket-rca/faults/toxiproxy/proxies.json` (cùng hash) | Việc nhẹ §11. Kết nối DB của event đi qua toxiproxy |
| `/opt/flash-ticket-app/{collector, compose, compose-t062, state, l1-fixtures}` | `archive/2026-11/flash-ticket-app/` | Không container nào dùng |
| `/home/ubuntu/{t058, t062, t071, *.py, *-t062.*}` | `archive/2026-11/home/` | Gồm `t071/db-moc` |
| Volume `flash-ticket-infra_*` | giữ | §5.3 |

### 7.3 tải

| Cũ | Mới | Ghi chú |
|---|---|---|
| `/opt/rca-lab` (@`5a39028`) | `/opt/flashticket-rca` (cùng commit) | |
| `/etc/rca-lab/load-secret` | `/etc/flashticket-rca/load-secret` | `tai_linux.py`, `kiem-token-con-han.py` |
| `/srv/rca-lab/load-runs/` (47 tag) | `archive/2026-11/load-runs/` | Lượt mới ghi vào `/srv/flashticket-rca/runs/<ngày>-<mục-đích>/` |
| `/opt/rca-tai` | xóa (§11) | Đã có ở `D:/RCA-archive/load-generator` |
| `/home/ubuntu/{x86-check, uvenv, arm-check*.tgz, rec-x86linux.json, dump_rec.py}` | `archive/2026-11/home/` | Chưa rõ hồ sơ nào dẫn tới, nên lưu chứ không xóa |
| Container `rca-tai-*` đã dừng (ít nhất 30) | xóa (§11) | |

### 7.4 Q1: bộ nhận cảnh báo

Hiện trạng: container `t072-bo-nhan` (bộ nhận thử của E3) vẫn chạy. Contact point `t072-webhook` gửi 11 luật vào nó, và nó ghi `runs/t072-e3-01/webhook.jsonl`.

**Đề xuất:**
- Dừng container, chuyển dữ liệu của nó vào archive.
- 11 luật vẫn tính và hiện trạng thái trên Grafana, nhưng không gửi đi đâu.
- Khi bật lại RCA trực tuyến, chạy `rca/online/webhook_receiver.py` dưới tên `rca-webhook`; contact point mới trỏ vào đó.

**Mặt trái:** trong khoảng không có bộ nhận, cảnh báo không được ghi ra file (Grafana vẫn giữ lịch sử trạng thái).

**Phương án khác:** giữ một bộ nhận nhẹ chạy liên tục.

### 7.5 UID Grafana: cũ → mới

| Loại | Cũ | Mới |
|---|---|---|
| dashboard | `t065-l5-muc-luc` | `ft-start` |
| dashboard | `flashticket-he-thong` | giữ |
| dashboard | `t065-l8b-rca` | `ft-rca-incidents` |
| dashboard | `t065-l8b-phat-lai` | `ft-rca-replay` |
| luật | `t072-p95-{booking,event,payment,ticket}` | `ft-p95-{…}` |
| luật | `t072-loi-{booking,event,payment,ticket}` | `ft-5xx-{…}` |
| luật | `t072-live` | `ft-live` |
| luật | `t072-mat-do` | `ft-mat-dau-do` |
| luật | `t072-mat-gw` | `ft-mat-gateway` |
| nhóm / folder | `t072-w4` / "T-072 W4 cảnh báo" | `ft-canh-bao` / "Cảnh báo FlashTicket" |
| contact point | `t072-webhook` | Theo Q1 |

- Hồ sơ cũ của repo RCA (382 file) giữ UID cũ, không sửa; người đọc tra `docs/ten-cu-moi.md`.
- `incidents.py` gom sự cố theo nhãn `__alert_rule_uid__`/`alertname`, không viết cứng UID.
- Folder thư mục dashboard đang có uid `rca-*`, không mang mã task: giữ.

## 8. Chỗ phải sửa đường dẫn

Đếm bằng `git grep` trên lab `main` (`4b6c4b2`):

| Chuỗi | Số file |
|---|---|
| `/opt/rca-lab`, `/srv/rca-lab`, `/etc/rca-lab` | 32 |
| `t065-l11-001` | 10 (riêng hai dashboard: 28 và 13 chỗ) |
| UID dashboard cũ | 9 |
| `from campaigns.lib import inventory` | 4 |
| Đường đã chết (rủi ro R15 của kiểm kê) | `sau_v082.py`, docstring runner, `load/controller/README.md` |
| `/opt/flash-ticket-app`, `/opt/flash-ticket-build`, `/opt/flash-ticket-src`, `/home/ubuntu/t063` | Liệt kê ở cột "duong_dan_may_viet_cung" của `kiem-ke/lab-file.tsv` |

Quy tắc sửa:
- Chỉ thay chuỗi đường dẫn, tên module và tên file (B5).
- Mỗi chỗ đọc lại trong ngữ cảnh, không thay hàng loạt mù. Riêng hai dashboard và `rules.yaml` được thay hàng loạt, vì B11 và B12 kiểm toàn bộ.
- Sau khi sửa, `git grep` các chuỗi cũ trên `main` mới phải rỗng, trừ `docs/ten-cu-moi.md` và `docs/sources-2026-11.md` (tài liệu lịch sử).

**Không sửa** đường dẫn trong hồ sơ cũ của repo RCA. Có 597 script đã track nhắc đường máy cũ; đó là ghi chép của việc đã làm. Người đọc tra bằng `docs/ten-cu-moi.md` (lab) và `docs/ARCHIVE-INDEX.md` (RCA).

## 9. Các bước thực hiện, hoàn tác, gặp lỗi giữa chừng

Mỗi bước cần Minh cho lệnh bắt đầu riêng. Không có lượt chạy nào dài hơn 1 giờ. Không phát tải, trừ một lượt mua vé ngắn ở bước 5 nếu Minh duyệt.

**Bước 0. Chụp hiện trạng (chỉ đọc, ba máy).** Ghi vào `results/T-070/don/truoc/`:
- sha256 của bản chụp M1, pins, config, cấu hình V082;
- `pip freeze --all` của venv cũ;
- sha256 cây `t065-l11-001`;
- sha256 các env file của 7 service và Keycloak (chỉ hash, không in giá trị);
- `docker compose config` của mọi project đang chạy;
- `docker inspect` (mounts, env file, labels) của mọi container;
- danh sách luật, dashboard và contact point trong Grafana (qua API đọc);
- một truy vấn mẫu Prometheus, Loki và Tempo cho một khoảng cố định trước ngày dời (đếm chuỗi hoặc dòng).

**Bước 1. Laptop, chưa đụng máy.**
1. Gắn tag `truoc-don-2026-11` lên lab `main`, push tag.
2. Tạo nhánh dọn; `git mv` theo §6; sửa đường dẫn theo §8; thêm `method.lock`, `ten-cu-moi.md`, `go-uid-cu.yaml`, compose có `name:`.
3. Kiểm offline:
   - `python -m py_compile` mọi file `.py`;
   - `docker compose config` cho từng file compose (với env giả);
   - `kiem-hop-dong.py`;
   - B5 (đọc diff), B11, B12;
   - `git grep` chuỗi cũ.
4. Chép các file K6 vào `results/T-070/don/tu-lab/`.
5. Minh duyệt diff, rồi merge vào `main`.

Hoàn tác: chưa merge thì bỏ nhánh; đã merge thì revert.

**Bước 2. obs** (không có lượt chạy nào; dữ liệu agent gửi sang trong vài phút gateway dừng có thể mất).
1. Dừng `t072-bo-nhan` (Q1).
2. `docker compose down` bộ quan sát. Không dùng `-v`.
3. `mv` theo §7.1. Checkout commit mới vào `/opt/flashticket-rca`.
4. Dựng venv mới; kiểm B4.
5. `docker compose up -d` (project `flash-ticket-obs-pinned`).
6. Kiểm B2, B3, B9 (phần obs), B10, B11, B12; xóa luật UID cũ; bỏ `go-uid-cu.yaml` sau khi kiểm.

Hoàn tác: `compose down`, `mv` ngược theo bảng (ghi sẵn lệnh ngược vào LOG trước khi làm), checkout `1bb40ca`, `compose up`. Volume không bị đụng.

**Bước 3. app** (FlashTicket thử nghiệm ngừng; ước lượng 10–15 phút, chưa đo).
1. `docker compose down` (không `-v`) 7 service, Keycloak, agent; hạ tầng `flash-ticket-infra` dừng sau cùng.
2. Dừng VNPay giả, đường hầm, toxiproxy.
3. `mv` theo §7.2; `git worktree repair`.
4. Dựng lại cấu hình hiệu lực bằng `hieu_luc.py`; kiểm B8.
5. `up` theo thứ tự: hạ tầng → Keycloak → discovery → các service → agent → toxiproxy → VNPay giả, đường hầm.
6. Kiểm B7, B8, B9 (DB).

Hoàn tác: như bước 2, dùng compose cũ còn trong archive.

**Bước 4. tải.** `mv` theo §7.3, checkout. Không có dịch vụ nào chạy thường trực trên máy này.

**Bước 5. Kiểm sau dời:** §10.

**Gặp lỗi giữa chừng:**
- Lỗi ở bước nào thì dừng bước đó, không đi tiếp.
- Lỗi của chính việc dời (thiếu file, sai đường): sửa đường hoặc `mv` ngược phần đó. Không cần làm lại phần đã đạt.
- Lỗi chạm tới B1–B4, B6 hoặc B13 (phương pháp hoặc cách ly nhãn): dừng toàn bộ, hoàn tác máy đó, báo Minh. Đây là lỗi tính đúng, không vá tại chỗ.
- Lỗi hạ tầng (mất SSH, máy treo): không ghi thành kết quả; làm lại bước từ đầu sau khi máy ổn.
- Mọi bước ghi một dòng vào LOG T-070: lệnh, giờ, kết quả, hash.

## 10. Kiểm sau khi dời

| Kiểm | Đạt khi |
|---|---|
| B1–B12 | Như cột "cách chứng minh" ở §4 |
| B13, hồi quy V082 (Q3) | 2 ca `46aab4be`, `ebd5ef38` với bổ sung `bo-sung-hoi-quy`, chạy bằng `chay_ca.py` của bản chụp theo đúng lệnh trong runner (cấu hình V082 kiểm hash). `method-output-1.json` và `-2.json` trùng byte với `rca/v082-hoi-quy/` |
| Grafana | 4 dashboard hiện có dữ liệu; 11 luật UID mới ở folder "Cảnh báo FlashTicket"; không còn luật UID cũ; datasource kiểm đạt |
| Chuỗi tín hiệu | `tests/signals/run_remote.sh` sau một lượt mua vé ngắn (khoảng 5 phút; cần Minh duyệt vì phát tải) đạt theo `tests/signals/tieu-chi.json` |
| Tên | `find` trên ba máy không còn đường `rca-lab`, `flash-ticket-app`, `flash-ticket-build`, `t0xx` ngoài `archive/` và volume Docker |
| Lưu trữ | `archive/2026-11/README.md` mỗi máy khớp `du` thực tế; `docs/ARCHIVE-INDEX.md` có đủ dòng |

## 11. Việc nhẹ làm kèm

Đây là việc làm lại được, không cần bàn. Mọi lệnh xóa vẫn trình Minh trước khi chạy.

- Cho VNPay giả và đường hầm chạy dưới compose.
- Tạo lại toxiproxy bằng compose.
- Xóa image và build cache cũ trên app (khoảng 12 GB).
- Xóa 13 checkout build cũ.
- Xóa `/opt/rca-tai` trên máy tải.
- Xóa các container k6 đã dừng.

## 12. Ngoài phạm vi dọn: việc sau

Ghi lại để không mất ngữ cảnh. Không làm trong đợt dọn.

| Việc | Hiện trạng đã kiểm | Đề xuất |
|---|---|---|
| Bật agent OTel trên FlashTicket thật (K8s, máy 84) | Image có agent, mặc định tắt (`OTEL_AGENT_ENABLED=false`); K8s chưa có nơi nhận | Bật khi máy 84 nối được với obs: hai biến môi trường trong cấu hình K8s (Y11) |
| Nối máy 84 vào obs | Gateway chỉ nghe IP nội bộ `10.0.0.215`; iptables obs chỉ nhận `10.0.0.0/24` và SSH | Sửa 4 chỗ: cho nghe IP công khai, mở iptables cho IP máy 84, mở Security List Oracle (Minh làm trên giao diện), thêm xác thực. Luật và dashboard lọc theo `deployment.environment` |
| Merge PR #17 vào main của nhóm | 13 file xung đột; hook tiêm lỗi chỉ ở `src/rca-test/` (profile `-P rca-test`), không xung đột; 3 file Java xung đột do code ghi log | Trước khi merge, đọc từng dòng 39 file nghiệp vụ được chèn lệnh ghi log |
| Dùng FlashTicket bản mới nhất trên app (Y12) | App đang chạy bản ghim `36a3725` (main `640dbaf` + PR) | Đổi bản đổi luôn hệ thống được đo: kết quả trước và sau không so trực tiếp được. Làm sau đợt dọn, như một bước riêng có kiểm tín hiệu lại |
| Hạn bán sự kiện tải | Hết 02/12/2026 22:16Z | Minh quyết sau (E6 dừng) |
| W7 | Hoãn | Mở lại sau khi dọn xong |
| A1, A2, D1, G1 | §2 | Chờ Minh duyệt chữ |
| `docs/READING-GUIDE.md` của repo RCA | Có nhắc đường lab cũ | Sửa đường sau khi lab merge (cần duyệt) |

## 13. Rủi ro và điểm chưa kiểm

| # | Điểm | Trạng thái | Nếu sai thì sao | Cách phân xử |
|---|---|---|---|---|
| RR1 | Hash bản chụp `b0f79a4d…` tính trên byte CRLF của cây làm việc Windows; 26/149 file khác blob git | Đã kiểm (kiểm kê §4) | Dựng lại bản chụp từ git sẽ ra hash khác, không khớp chỉ mục cũ | Đợt này chỉ `mv`, không dựng lại. `method.lock` ghi rõ quy ước byte. Cách dựng bản chụp mới là việc sau |
| RR2 | Grafana có tự xóa dashboard khi file provisioning đổi tên không | Chưa kiểm | Dashboard UID cũ còn lại song song | Kiểm ở bước 2; còn thì xóa qua API |
| RR3 | `name:` trong compose có làm Docker nhận đúng project và volume cũ không, khi working dir đã đổi | Chưa kiểm trên máy | Volume mới rỗng, dữ liệu trông như mất (dữ liệu vẫn còn trong volume cũ) | Bước 1 chạy `docker compose config` xem tên project. Bước 2 kiểm `docker volume ls` và dữ liệu trước khi đi tiếp. Hoàn tác không mất dữ liệu |
| RR4 | Script hay cron ngoài danh sách kiểm kê còn trỏ đường cũ | Kiểm kê không thấy cron hay unit tự tạo | Lỗi khi chạy sau này | `grep` toàn `/opt`, `/etc`, `/home` ba máy ở bước 0 |
| RR5 | Đường hầm VNPay phụ thuộc khóa và cổng 19091 trên máy tải | Đã kiểm cổng đang nghe | Luồng thanh toán của k6 lỗi | Kiểm ở bước 5 (lượt mua vé ngắn) |
| RR6 | Hồ sơ nào dẫn tới `x86-check` và các file khác trên máy tải | Chưa kiểm | Không ảnh hưởng: chỉ lưu, không xóa | — |
| RR7 | B13 chỉ phủ `run_m1`/`chay_ca`, không phủ bước chụp dữ liệu (`stage_m1`, `stage_b`) | Đã biết | Lỗi đường dẫn ở bước chụp không lộ qua hồi quy | B5 (đọc diff, chỉ đường dẫn) + lượt mua vé ngắn ở bước 5. Phép chụp lại cùng một cửa sổ không lặp được hoàn toàn, vì vùng ghi vòng thay đổi liên tục |
| RR8 | Thời gian app ngừng | Ước lượng, chưa đo | Kéo dài hơn dự kiến | Không có lượt chạy nào phụ thuộc trong lúc dọn |

## 14. Nguồn dữ kiện

- **Kiểm kê chỉ đọc** `results/T-070/kiem-ke/` (README, 14 bảng TSV, `tho/`, SHA256SUMS 49/49):
  - `lab-file.tsv`: file lab, đường dẫn viết cứng, nơi được dẫn;
  - `duong-dan-ai-dung.tsv`: đường dẫn trên máy và ai dùng;
  - `lab-dashboard.tsv`, `lab-luat-canh-bao.tsv`;
  - `m1-ban-chup.tsv`;
  - rủi ro R1–R17.
- **Đọc thêm có sudo, chỉ đọc**, 24/11 (LOG T-070 các dòng 12:05Z, 13:20Z): kích thước và quyền `/srv/rca-lab/*` và `m1/*`; compose project và volume; `/etc/sudoers.d`; cấu trúc `v082-hoi-quy`; máy tải (thư mục, container, image).
- **Đối chiếu git blob** lab ↔ RCA cho các file "bỏ" (§6).
- **`git diff 407b4f5 main -- observability/collector inventory app-host faults`**: rỗng.
- **`results/T-066/thay-doi-may.md`, `results/T-066/hoi-quy-v082.json`**: cách tạo bộ hồi quy V082.

# Phản biện T-070 — kế hoạch dọn repo lab và ba máy

- **Người phản biện** Codex. **Người làm** Claude. **Ngày** 24/11/2026.
- **Công đoạn** Soát SPEC, bản kế hoạch 1 trước W7. Đây là việc vận hành, ngoài G0–G4. Minh cho ghi bản lượt đầu tại `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md`.
- **Bản đã đọc** RCA `74b2515d8`, lab `main@4b6c4b2`, kế hoạch và kiểm kê chưa commit. Số dòng dưới đây tính trên `results/T-070/don/KE-HOACH-DON.md` bản 1. Đường dẫn mã lab tính từ gốc repo lab.
- **Tự soát độc lập** Đã đọc AGENTS của hai repo, STATE, SPEC, LOG ngày 24/11 từ 10:20Z, HOP-DONG I7–I12, kế hoạch, bảng TSV, lệnh và đầu ra thô của kiểm kê. Đối chiếu T-066 (`thay-doi-may.md`, `hoi-quy-v082.json`, đính chính, phép cách ly), manifest T-064, mã nguồn tại revision nêu trên và trạng thái thực trên ba máy bằng SSH chỉ đọc. Nguồn mục tiêu gồm DT18-NV2/NV3, hướng dẫn cô ngày 23/09, MRP P9/P10, WHY-08/98/100/101, DECISIONS 16 và 23–24/11, LESSONS SL23, SL37 và QT18. Không có bản phản biện hay phản hồi trước cho kế hoạch này.

## Kết luận chung

**Giữ khung thư mục Minh đã duyệt. Chưa nên duyệt bản 1 để dời máy hoặc xóa dữ liệu.** Có hai phản ví dụ ngay trên đường V082 → giao diện. Một module đang được nạp bị xếp vào danh sách bỏ. Dữ liệu đồ thị đang hiển thị chứa liên kết sẽ hỏng khi đổi UID dù cây dữ liệu vẫn khớp hash.

Ba máy vẫn ở các revision đã kiểm kê. Những điểm dưới đây chặn đúng bước ghi ở từng mục. Đây là đánh giá khả năng thực hiện kế hoạch. Nghiệm thu T-070 còn phụ thuộc W4/W5, W8 và diễn tập W9a theo SPEC §“Tiêu chí xong”. Dọn máy chỉ bảo toàn khả năng chạy, truy nguồn và trình diễn theo P9/P10. Lượt này không đánh giá lại chất lượng xếp hạng hay mở W7.

## Các điểm

### R1. Bước chụp hiện trạng có đường đưa bí mật thật vào repo RCA — CHẶN bước 0 như đang viết

Dòng 365–372 yêu cầu ghi `docker compose config` của mọi project vào `don/truoc/`. Compose giải tham chiếu `env_file` khi dựng cấu hình. Lab `observability/compose.yaml` nạp `grafana.env`. Trên obs, truy vấn chỉ **tên** biến trong `docker inspect` trả về `GF_SECURITY_ADMIN_PASSWORD`. Trên app có `EVENT_DB_PASSWORD`. Không đọc hay lưu giá trị. B8 nói chỉ ghi hash env, nhưng ràng buộc ấy chưa áp lên bản cấu hình đã giải biến. G1 còn đề xuất commit cả thư mục dọn. Đây là đường lộ trong thiết kế, chưa có bằng chứng bí mật đã được ghi.

**Sửa tối thiểu.** So cấu hình hiệu lực trên chính máy. Chỉ lưu tên project, image, mount, đường env, tên biến và kết quả so/hash cần cho B7/B8. Với inspect, chọn rõ trường. `app-host/scripts/hieu_luc.py::mask` đã có cách so giá trị env bằng hash. Các bản đã giải biến không cần rời máy.

### R2. Danh sách bỏ làm đứt đường xuất G1 của cả hai chế độ — CHẶN bước 1

Dòng 211, 214 gọi các literal trong `sau_v082.py` là đường chết và bỏ `campaigns/g1/l8b-xuat.py`. Trong `sau_v082.py:33–46`, `nap_bo_xuat` nạp chính file đó bằng `exec_module`, lấy nguồn `dev3_template`, đòi mỗi literal xuất hiện đúng một lần rồi mới thay đường dữ liệu. Nhánh xử lý ca **mới** cũng gọi hàm này. `campaigns/online/g1_b.py` nạp lại `sau_v082` và gọi cùng hàm. Bản sao trong tag hoặc repo RCA không nằm ở nơi tiến trình trên obs nạp. `py_compile` riêng từng file vẫn có thể đạt trong lúc ca mới không xuất được đồ thị.

Đường ghi còn có điều kiện riêng. `g1_b.py:78` từ chối bộ chính và mọi tên bộ không bắt đầu bằng `t073-`. Chỉ sửa đường dẫn hoặc bỏ hẳn điều kiện đó lần lượt làm tuyến trực tuyến dừng hoặc mất bảo vệ bộ chính của I9.

**Sửa tối thiểu.** Giữ bộ xuất dưới tên chức năng trong lab, cập nhật hai nơi nạp và cặp literal tương ứng. Khai một đích online riêng được phép, tiếp tục cấm ghi vào bộ `dev`. `check_old_case.py` và `campaigns/online/README.md` đã có đường phát lại từ capture, Prometheus và gói bổ sung lưu sẵn. Trên obs còn `m1/t073-dev/sim-capture/`. Khi Minh duyệt, dùng một ca cũ vào đích mới để so gói, đầu vào P7, đầu ra V082 và G1. Đây là phép thử trên dữ liệu cố định cho RR7, tách được lỗi đường dẫn khỏi tín hiệu sống đã quay vòng. Không cần thu thêm một đợt.

### R3. Đổi UID dashboard làm hỏng liên kết nằm trong dữ liệu đã xuất — CHẶN đổi UID ở bước 2

B10 đòi bộ `dev` trùng byte bộ cũ. B12 chỉ so JSON cấu hình dashboard. `campaigns/g1/service_graph.py:47,191` ghi URL `/d/t065-l8b-rca` vào trường `detail__url` của nút. Panel dùng chính giá trị đó khi bấm (`build_dashboards.py:103–108`). Tôi đếm trên obs bằng `files = list((bo_cu/'service-graph').rglob('*.json'))` và `sum(b'/d/t065-l8b-rca' in f.read_bytes() for f in files)`. Kết quả **109/218 file JSON** chứa UID cũ. Ví dụ `service-graph/V071-V041+H8a/00eaea92.json`. Khi gỡ dashboard UID cũ theo RR2, mở trang mới vẫn có dữ liệu nhưng bấm vào nút sẽ tới dashboard đã gỡ. Đây là chức năng Minh đã chọn giữ trong WHY-101.

**Sửa tối thiểu.** Ưu tiên giữ UID đích đang được các nút dùng. Vẫn đổi được tên file, tên hiển thị và đường `public/rca/dev`. Nếu Minh muốn đổi cả UID, giữ nguyên bộ bằng chứng, đổi đúng URL trong một bản hiển thị dẫn xuất và sửa B10 để so phần ngoài URL. Trong cả hai cách, bấm lại một nút thường và một nút chú thích trên bộ đã dời. Không cần dựng lại kết quả M1.

### R4. Di chuyển nội dung từng lượt có thể bỏ mất quyền bảo vệ của thư mục cha — CHẶN B6 trước bước 2

Dòng 258–263 giữ mode sổ riêng và dời `runs/*` vào archive. T-066 còn chứng minh user `rca` không liệt kê được `runs`, vì nhật ký có tên ô. Kiểm `stat` trên obs cho `runs` = `ubuntu:ubuntu 700`, `runs/t069-chinh.out` = `664`, `runs/t073-e5-01` = `755`, file `webhook.env` trong đó = `664`. Hiện `sudo -n -u rca test -r /srv/rca-lab/runs/t069-chinh.out` trả 1. Dời con giữ mode của con. Nếu cha archive mới cho đi qua, quyền đọc phát sinh ngay cả khi sổ chính vẫn 700. Chưa thấy nhãn lọt vào đầu vào phương pháp.

**Sửa tối thiểu.** Giữ nguyên thư mục cha 700 khi lưu lịch sử, tạo `runs` mới cùng chủ/quyền. Xử lý cờ STOP đang có trước khi dời. Lặp lại phép `test -r` bằng user `rca` trên một nhật ký ở cả vùng cũ đã lưu và vùng đang dùng, cùng phép từ chối sổ đã có ở T-066. Chỉ mục archive có thể đọc riêng, không cần mở quyền trên hiện vật.

### R5. Thứ tự bật app và hai đường dẫn ngoài Git không khớp trạng thái đang chạy — CHẶN bước 3

- **Event và Booking cần proxy trước khi lên.** Bước 3.5 đặt toxiproxy sau các service. Trên app, kiểm biến hiệu lực chỉ theo tên biến và số cổng cho `EVENT_DB_URL` → 15433, `REDIS_PORT` → 16379, `RABBITMQ_PORT` → 15673. Cả ba cổng được khai trong `faults/toxiproxy/proxies.json`. `app-host/scripts/deploy.sh` chờ health/đăng ký Eureka từng service, rồi dừng ở service không đạt. Bật proxy sau bước chờ có thể làm việc triển khai dừng trước khi có cơ hội bật proxy.
- **Bộ tiêm đọc một đường dẫn lưu trong file.** Trên app, `cat /home/ubuntu/t063/inj/compose-dir` trả `/opt/flash-ticket-build/t067-compose/hieu-luc`. `inj3.py::compose_dir` đọc nội dung này khi runner gọi qua SSH. Dòng 290 chỉ chuyển thư mục chứa file. Cấu hình app có thể lên bình thường trong khi lượt tái tạo Payment tiếp theo gọi nhầm chỗ.
- **Nguồn bind MongoDB phân giải sang chỗ khác.** Compose thực dùng `deploy/mongodb/compose.yaml:19`, đường `../../docs/architecture/data/mongodb/schema.cjs` tính từ thư mục của file Compose gốc đầu tiên, tức `infra/deploy`. Sau dời nó thành `/opt/flashticket/docs/…`, còn dòng 286 đặt nguồn ở `/opt/flashticket/infra/docs/…`. `docker inspect` xác nhận mount hiện tại, và `stat` tại nguồn hiện trả **directory**, dù tên kết thúc bằng `.cjs`. Đây là sai khác mount có thể bị kiểm “DB còn đơn cũ” bỏ sót. Không suy ra DB hiện mất dữ liệu hay script khởi tạo từng chạy.

**Sửa tối thiểu.** Bật hạ tầng và proxy trước các service phụ thuộc. Ghi cặp đường cũ/mới cho cả **nội dung** `compose-dir` và nguồn bind MongoDB. So nguồn, đích và loại mount với trước dời. Giữ nguyên bộ Compose hiệu lực T-067 trước khi sinh file mới và giữ các image nó cần cho đến khi hết nhu cầu hoàn tác. Bản `compose-t062` lưu trữ thuộc cấu hình khác. Nếu SSH đứt sau một lệnh dời, đọc trạng thái nguồn/đích và project hiện có rồi tiếp từ dòng thiếu. Lặp nguyên bước như dòng 417 có thể áp lệnh lần hai lên cây đã dời một phần.

### R6. Chuyển VNPay và đường hầm sang Compose đổi người quản lý tiến trình — CHẶN phần này của §11 và lần phát tải sau dời

`load/controller/tai_linux.py:189–210` luôn gọi `kiem-mock.py` với `RECOVER=True` và `tunnel-remote.py` với `ACTION='start'` khi chuẩn bị tải. Hai helper đọc PID trên máy chủ và tự khởi chạy tiến trình nếu không thấy PID đúng. Nếu Compose đã sở hữu tiến trình, lần kiểm trước tải vẫn có thể tự bật thêm bản chạy trần, tranh cổng hoặc báo sai rằng dịch vụ chết. Kiểm cổng 19091 ngay sau khi bật chưa đi qua nhánh này.

**Sửa tối thiểu.** Trong đợt đổi tên, giữ một cơ chế quản lý đang chạy và sửa đường mã, trạng thái, env, khóa tương ứng. Để việc chuyển sang Compose sang lượt riêng là ít thay đổi nhất. Nếu Minh chọn làm cùng, thay hành vi khôi phục của chính hai helper để chỉ một nơi được khởi chạy dịch vụ. Giữ kiểm sức khỏe từ phía máy tải. Chi phí của hoãn là vẫn dùng cơ chế khôi phục hiện tại trong đợt dọn.


### R7. Các phép kiểm trước và sau dời chưa cho được kết luận mà §10 yêu cầu — CHẶN việc dùng chúng để nghiệm thu

| Phép kiểm | Phản ví dụ trên bản hiện hành | Sửa nhỏ nhất trước khi dùng |
|---|---|---|
| B4, môi trường Python | So tập dòng gói của `campaigns/requirements-m1.txt` với `results/T-066/hoi-quy-v082.json#/ghim/pip_freeze` cho đúng một phần tử chỉ có ở freeze, `pip==24.0`. Ngay venv chuẩn cũng trượt phép “trùng cả hai”. | So freeze mới với freeze cũ, kể cả pip. Kiểm các pin trong requirements theo danh sách gói được khai, ghi cả phiên bản Python. |
| B13/Q3, hai ca chuẩn | Trên obs, `test -f m1/outputs/<ca>/method-input.json` đạt với `46aab4be` và thiếu với `ebd5ef38`. `src/m1_ft/chay_ca.py:55` đọc file này ở chế độ mặc định. T-066 `#/ca/1/dung_lai_dau_vao` là `true`. Lệnh cũ `#/ghim/lenh` còn dùng đích `v082-hoi-quy` hiện đã có, trong khi `chay_ca.py:124` dùng `exist_ok=False`. | Khai lệnh từng ca, `--dung-lai-dau-vao` cho ca thứ hai, `--bo-sung` theo từng mã và thư mục ra mới. Giữ hai đầu ra chuẩn chỉ đọc. So cả hai lần với hash T-066/T-064. Phép này chứng minh lõi trên hai ca. R2 xử lý đường xuất của lab. |
| `kiem-hop-dong.py`, bước 1.3 | Chạy riêng hai ca cô lập từ `Contract` trên obs với `python3 -B`, SSH/tải trong ca khởi chạy đã được giả lập. `test_normal_pool_and_multiplier` lỗi `KeyError: 'labCommit'` vì test truyền `{}`. `test_source_hash_mismatch_fails_before_ssh` trượt vì test chờ kiểm hash nguồn cũ, còn `verify_sources()` kiểm Git. Hai file lab này trùng Git blob giữa obs và main. | Điều chỉnh đầu vào và kỳ vọng của bộ thử theo hợp đồng commit hiện hành, hoặc ghi chính xác phần chưa có kiểm hợp lệ. Không sửa bộ tải để thỏa kỳ vọng cũ. Nếu đổi thư mục, bộ kiểm cây sạch cũng phải theo đúng `rca/` thay cho `campaigns/`. |
| Tín hiệu mua vé, bước 5 | `tests/signals/tieu-chi.json#/buoc_7/cua_so` khai 10 phút ×1 và GET `/api/v1/me`. Kế hoạch ghi khoảng 5 phút. `check_purchase_journey.py:151–156` trả `chua_kiem` cho số vé nếu thiếu kết quả DB của đơn. Script xét telemetry, không gọi stage hay G1. | Nếu xin dùng tiêu chí cũ, ghi đúng lượt 10 phút, GET và truy vấn đơn COMPLETED đã chọn. Nếu chỉ cần lượt ngắn, khai trước những tín hiệu sẽ xác nhận, phần còn lại ghi chưa được kiểm. Chọn một cách trước khi xem kết quả. |

Các lỗi trong bảng thuộc đường kiểm và cách gọi. Không có cơ sở từ chúng để kết luận V082 đã đổi hạng hoặc FlashTicket đang lỗi.

### R8. B11 bỏ qua hai phần quyết định một cảnh báo tới đâu và mang mã nào — CHẶN đổi UID luật, dừng bộ nhận và hoàn tác obs

Dòng 113, 310–319, 338 và bước 2 chỉ so nội dung luật sau khi bỏ receiver, đếm UID mới, rồi gỡ UID cũ. Đối chiếu toàn bộ `t072-luat.yaml` được **11/11** luật có `labels.t072_uid == uid`. `incidents.py::ma_luat` ưu tiên **`t072_uid`** trước `__alert_rule_uid__` và `alertname`. Nếu thay chuỗi toàn file để đổi UID, B11 sẽ trượt vì nhãn đổi. Nếu giữ nguyên nhãn để qua B11, bộ gom sự cố vẫn xuất UID cũ. Bộ nhận hiện đang chạy, cùng mạng với Grafana. Các luật gửi tới tên contact point `t072-bo-nhan-nhe` có integration `t072-webhook`. Dừng container không tự đổi đích gửi.

Ngoài ra, hoàn tác ở dòng 397 chỉ dựng bộ quan sát từ commit cũ. `docker ps --format '{{.Names}} {{.Label "com.docker.compose.project"}}'` trên obs cho bộ nhận thuộc project **`t073-webhook`** riêng. Hoàn tác còn có thể để lại luật UID mới trong DB Grafana bên cạnh luật cũ. Chính bước 2 đã thừa nhận bỏ file provisioning không đủ để xóa luật. Xóa file dùng một lần ngay trên một máy cũng sẽ làm checkout khác commit đích nếu không có một commit tiếp theo.

**Sửa tối thiểu.** Ưu tiên giữ UID luật và mã I1, đổi tên hiển thị nếu cần. Giữ một bộ nhận nhẹ trong lúc chưa có đích thay thế, theo quyết định hiện hành. Mặt trái là vẫn phải giữ một dịch vụ nhỏ. Nếu Minh muốn ngừng giao nhận hoặc đổi UID, ghi rõ UID vật lý ↔ mã I1, cấu hình định tuyến hiệu lực và cách lui lại. Hoàn tác phải khôi phục đúng tập luật/đích nhận trước dời và project bộ nhận với env của nó. Việc gỡ cấu hình dùng một lần cần theo đúng commit lab trên cả ba máy.

### R9. Xếp cả `/opt/rca-tai` vào danh sách xóa trái quyết định đang hiệu lực — CHẶN riêng việc xóa

`docs/DECISIONS.md` ngày 23/11, **Q5** ghi giữ T-066 mục **2.6**. `results/T-066/danh-sach-xoa.md` xác định 2.6 chính là `/opt/rca-tai` trên máy tải. Dòng 304, 439 của bản 1 dựa vào “đã có ở `D:/RCA-archive/load-generator`”. Kiểm tại chỗ cho thấy kho này chỉ có `load-runs/out`. Manifest `D:/RCA-archive/hash-lists/load-generator-out.sha256` có 0 dòng ngoài `out/`. Máy tải còn `bo-sung-1/`, `k6/`, `k6-e1/`, `fixture.py`, `secret/`. T-066 có đối chiếu riêng cho secret khi chuyển trước đây. Việc đó không chứng minh cả cây đã có bản ở laptop.

**Sửa tối thiểu.** Bỏ thao tác xóa 2.6 khỏi lượt này, ghi đường tra cứu trên máy. Không cần kéo thêm dữ liệu về laptop. Nếu sau này Minh muốn thay Q5, trình đúng phần định xóa và đối chiếu phần đó với bản giữ. Với app cũng cần tách phần lịch sử khỏi phần có thể xóa. Ví dụ `/home/ubuntu/t063/thu3` còn log build, patch và kết quả thử ngoài nhánh `inj` được dời. Không xóa cây cha hoặc quét image làm mất đường quay về T-067 chỉ để đạt tiêu chí tên.

### R10. Phép quét tên xung đột với bản chụp đã khóa và bỏ sót cờ dừng thứ hai — CHẶN tiêu chí tên và việc phát tải theo đường mới

Dòng 428 đòi không còn tên task ngoài archive/volume, trong khi B2 bắt buộc giữ nguyên cấu trúc snapshot. Trên obs, `find <snapshot> -type f -path '*/results/T-*' | wc -l` trả **91**. Runner mở cấu hình V082 theo tên tương đối dưới `results/T-064/`. Bộ sinh dashboard cũng dùng `git show ab1c52c:<đường cũ>` để đọc nguồn quá khứ. Sửa những chuỗi đó theo quy tắc “grep phải rỗng” có thể làm đứt tham chiếu dù tệp đang chạy đã được dời đúng.

Ở chiều ngược lại, một cái tên còn vắng trong bảng đích lại điều khiển hành vi thật. I8 và `chuoi_tai.py:63–65` dùng **cả** STOP của `runs` và STOP của bộ tải. `tai_linux.py:86,137` tự kiểm `STATE/STOP`. Dòng 261–262 chỉ kê `runs/STOP`, file sự kiện và file khóa. Lúc kiểm, `ls -A /srv/rca-lab/load-controller` cho `tai-linux-events.jsonl`, `tai-linux.lock`, `tai-out`. Cờ không hiện diện lúc này, nhưng người vận hành vẫn cần biết đường nào có hiệu lực ở lượt kế tiếp.

**Sửa tối thiểu.** Áp quy tắc tên cho giao diện và đường vận hành mới. Nếu dời lịch ra khỏi lab, nêu chỗ đặt bản lịch được duyệt trên obs: `runner4.py:238–240` mở `--lich` bằng đường cục bộ và băm file đó trước khi chạy. Cho phép tên trong snapshot bất biến và đường tra lịch sử tại revision cũ. Ghi hai đường STOP đích, nơi từng chương trình đọc và quyền tạo/xóa. Nếu Minh muốn hợp nhất hai cờ thì đó là thay đổi hợp đồng I8, cần nêu riêng. Kiểm nguồn cho §8 bằng `git grep -El '/(opt|srv|etc)/rca-lab' 4b6c4b2 --` trả **34 file**, còn bảng ghi 32. Đếm ở đúng revision và nói rõ bộ lọc. `findmnt -T /srv/rca-lab` trên máy tải trả `/dev/nvme0n1p1`; các đường nguồn/đích ở cùng filesystem vẫn có thể dời tại chỗ.

## Đối chiếu các lượt trước

Đây là lượt đầu dành cho kế hoạch dọn. Các đính chính của T-066 được dùng để xác định đúng hiện vật và phạm vi phép hồi quy. Không có finding hoặc phản hồi trước của T-070 về kế hoạch này cần chấm lại.

## Tuân thủ quy trình

- **Đã quyết.** Claude làm, Codex phản biện. Minh duyệt kiểm kê, đọc máy bằng sudo và khung §5. LOG 10:20Z–14:45Z và yêu cầu lượt này xác nhận E6 dừng, W7 hoãn, dọn trước W7. DECISIONS 23/11 còn ghi lịch cũ. Kế hoạch đã khai D1 chờ duyệt chữ. Q5 về giữ 2.6 là quyết định riêng.
- **Quyền ghi.** `don/` và `kiem-ke/` nằm trong vùng kết quả T-070. Lượt này chỉ có quyền tạo bản phản biện. SPEC gốc loại sửa runner/bộ tải và chạy máy; quyền đọc 24/11 không cấp các bước triển khai. Sửa code lab, luật hai repo, G1 (commit/push), A1/A2 và việc xóa cần đúng phê duyệt tương ứng. Không có bằng chứng trong lượt này về một lần dời máy hoặc sửa lõi trái phép. Người phản biện không ghi LOG/STATE.
- **Nguồn và vân tay.** Kế hoạch hiện chưa track. Không thấy kế hoạch hay REVIEW trong SHA256SUMS kiểm kê hoặc manifest/plan đã rà của T-066/T-070. Các sửa tối thiểu ở trên là đề xuất cho **bản kế hoạch**. Khi thực hiện, đổi/lược file lab làm đổi tree/commit lab, kể cả khi đầu ra tính toán giữ nguyên. Giữ tag và revision gốc cho hồ sơ cũ. Đổi byte cấu hình, file nguồn trong snapshot hay hai bộ chuẩn sẽ ảnh hưởng pin/manifest đã dẫn, nên dùng lại bản chuẩn nguyên vẹn. Đổi link theo phương án dẫn xuất của R3 chỉ đổi hash bản hiển thị mới.

## Điều đã kiểm và thấy đúng

- Tính lại SHA-256 cho từng dòng `results/T-070/kiem-ke/SHA256SUMS` đạt **49/49**. So cặp đường tương đối + SHA-256 của `find . -type f -exec sha256sum {} +` trong snapshot trên obs với `m1-ban-chup.tsv`, rồi băm các file tương ứng trong cây RCA, đạt **149/149** ở mỗi phép. Phương án dời cùng filesystem giữ được nguồn chuẩn và tránh dựng sai byte CRLF.
- Tính lại hash `results/T-064/manifest-3.json` khớp đính chính T-066 §1. Hai file chuẩn tại `hoi-quy-v082.json#/ca/{0,1}/chuan/file` khớp từng mục trong manifest. Trên obs, `find m1/v082-hoi-quy -name 'method-output-*.json' -exec sha256sum {} +` cho hai bản của mỗi ca khớp chuẩn tương ứng. Đây là kiểm hiện vật có sẵn. Phép hồi quy sau dời còn chờ Q3.
- `git diff 407b4f5 4b6c4b2 -- observability/collector inventory app-host faults` rỗng. So `1bb40ca..4b6c4b2` chỉ khác README. Kết quả hợp với việc giữ nguyên nội dung Collector. Giữ tên project/volume, dữ liệu dev chuẩn và bản FlashTicket ghim là có căn cứ. Không cần một vòng chọn lại cơ chế. WHY-98 đã ghi căn cứ chọn V082 và các phương án từng so. WHY-100/101 chi phối cách truy từ đồ thị về đúng ca.
- Đường nhập lõi hiện đọc gói ca theo danh sách file/hash, chuyển span, metric, log, inventory, alias, mốc thời gian và tham số, kiểm trường/giá trị cấm ở `run_m1.py`, rồi chạy `chay_ca.py` với cấu hình ghim. G1 đọc xếp hạng và dựng dữ liệu hiển thị phía sau. Không phát hiện kế hoạch chọn thuật toán theo nhãn hoặc thay phép chấm. R2–R4 liên quan khả năng chạy/hiển thị và cách ly sau dời. Không có đối chứng “không đồ thị” hay kết quả khoa học mới phải nghiệm thu trong lượt này.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm.** Soát kế hoạch bản 1, truy từ bảng dời tới code, quyền thư mục, nguồn bind, hiện vật trên máy và quyết định đã ghi.
2. **File thay đổi.** Chỉ `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md`. Không chạy tải, tiêm lỗi, mở dữ liệu khóa, thay dịch vụ hoặc commit.
3. **Kiểm.** Gói kiểm kê, snapshot và chuẩn hai ca khớp. Đã tái hiện hai lỗi của bộ kiểm hợp đồng bằng phép thử cô lập và đếm file đồ thị trên máy. Chưa có bản triển khai sau dời để nghiệm thu. Không ghi lỗi công cụ hay đường dẫn thành lỗi khoa học.
4. **Minh quyết.** Đề xuất **tiếp tục một lượt Claude đáp phản biện trong phạm vi kế hoạch**. Giữ khung đã duyệt. Ưu tiên giữ bộ xuất G1, UID đang được dữ liệu tham chiếu, một bộ nhận đang hoạt động và đường hoàn tác. Dùng `dev` cho tên bộ hiển thị (Q2) nếu giữ được link như R3. Xin giữ Q3 với lệnh đúng cho mỗi ca. Cách này giữ lại vài định danh lịch sử và một dịch vụ nhỏ, đổi lại tránh phải sửa kết quả cũ hay phát lại tải. Phương án đổi đồng loạt cần tách bản hiển thị, đích online và cơ chế khôi phục như các mục trên.

K1–K6 có thể giữ ở mức phương án bố trí, với bộ xuất còn hoạt động ở K1, bind đúng ở K2, giữ phân quyền và đường điều khiển ở K3–K5. K6 chỉ dành cho hiện vật lịch sử, nguồn đã có trong tag không cần chép thêm nếu Minh chỉ cần tra cứu. Đề xuất giải quyết D1 bằng chữ Minh duyệt để hồ sơ sau khớp lịch mới. Để riêng A1/A2 và G1. Thay luật toàn repo hoặc push lúc này rộng hơn phần cần để sửa kế hoạch. Giữ Q5 tránh một lần xóa không đảo ngược. Thời gian ngừng máy thật vẫn là ước lượng vì chưa triển khai; trình Minh cửa sổ vận hành sau khi chốt phụ thuộc ở R5/R6. Không cần đo trước bằng một lần dừng máy thử.

Phần chờ bằng chứng là **sau dời**. Claude có thể phân xử các bất đồng thiết kế bằng mã, các hiện vật ở máy và các lệnh chỉ đọc nêu trên ngay trong lượt đáp. Khi Minh duyệt triển khai mới phát lại ca dev vào đích riêng và đo các tín hiệu đã khai. Việc tiếp tục phản biện không tự cho phép dọn, phát tải, đóng task hoặc mở W7.

## Prompt bàn giao cho người làm

Minh có thể chuyển nguyên khối dưới đây cho Claude. Phạm vi mặc định của lời bàn giao là trả lời trong chat.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-070, tasks/T-070-dieu-phoi-giai-doan-2/. Kế hoạch dọn repo lab và ba máy, results/T-070/don/KE-HOACH-DON.md (bản 1, 24/11/2026).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giai đoạn 2, kế hoạch vận hành trước W7, ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-070.
- Tài liệu gốc: results/T-070/don/KE-HOACH-DON.md, results/T-070/kiem-ke/ (README, TSV, tho/, SHA256SUMS), tasks/T-070-dieu-phoi-giai-doan-2/{SPEC.md,LOG.md,HOP-DONG.md}, AGENTS.md, results/T-066/thay-doi-may.md và results/T-066/hoi-quy-v082.json. Repo RCA ở 74b2515d8, kế hoạch và kiểm kê chưa commit.
- Phản biện và phản hồi trước: tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md (lượt đầu, sau khi tự soát mới đọc). Phản biện các đề xuất mà bản lượt này trình Minh, cùng phương án khác nếu có..
- Code và kết quả liên quan: lab D:/Project/flashticket-rca-lab, main 4b6c4b2, obs 1bb40ca, app 407b4f5, tải 5a39028. Mã RCA trong src/m1, src/m1_ft, src/p3. Nếu cần đối chiếu máy, dùng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs|tai với script qua stdin, chỉ lệnh đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền mới. Làm trong phiên này, không dùng subagent.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN bước 0 | `docker compose config` giải biến từ `env_file` vào `environment`, nên bản lưu sẽ chứa giá trị bí mật. Bước 0 trong kế hoạch ghi bản này vào `don/truoc/`. Sửa: so cấu hình hiệu lực ngay trên máy; chỉ lưu tên project, image, mount (nguồn, đích, loại), đường env, tên biến và hash giá trị (cách `hieu_luc.py::mask`). | |
| R2 | Đúng; CHẶN bước 1 | Đã đọc `sau_v082.py:28-46`: `nap_bo_xuat` nạp `campaigns/g1/l8b-xuat.py` bằng `exec_module`, đếm đúng một chỗ `SRC_GOC`/`BS_GOC` rồi thay. `g1_b.py:97` gọi lại hàm này; `g1_b.py:78` chỉ cho ghi vào bộ có tên `t073-*`. Kế hoạch bản 1 gọi hai literal là đường chết và bỏ `l8b-xuat.py`: sai. Hai literal là chuỗi mẫu trong nguồn `dev3_template`, phải giữ nguyên cặp. Sửa: giữ bộ xuất dưới tên chức năng (`rca/lib/g1_export.py`), cập nhật hai nơi nạp. Điều kiện `t073-` đổi thành tiền tố đích trực tuyến mới (ví dụ `online-`), vẫn cấm `dev`. Đây là hunk logic, không chỉ đường dẫn: tách khỏi B5, trình riêng. | |
| R3 | Đúng; CHẶN đổi UID dashboard | `service_graph.py:47` đặt `DASH = '/d/t065-l8b-rca'` và ghi vào `detail__url` (dòng 297, 333, 406). Codex đếm 109/218 file JSON trong bộ đang hiện; tôi chưa đếm lại, nhưng đường code khớp. Đề xuất: giữ UID dashboard, chỉ đổi tên file, tên hiển thị và đường `public/rca/dev`. Mặt trái: URL trên trình duyệt vẫn có `t065-l8b-rca`. Phương án đổi UID cần bộ hiển thị dẫn xuất và sửa B10. | |
| R4 | Đúng; CHẶN B6 trước bước 2 | `stat` trên obs: `runs` ubuntu:ubuntu 700, `runs/t069-chinh.out` 664, `runs/t073-e5-01` 755; `sudo -u rca test -r runs/t069-chinh.out` trả 1. Dời con vào một cha mới mở quyền sẽ làm lộ nhật ký có tên ô. Trùng ý N2 tự tìm. Sửa: `archive/2026-11/runs` và `runs/` mới đều ubuntu 700. Lặp `test -r` bằng user `rca` ở vùng cũ đã lưu và vùng mới, cùng phép từ chối đọc sổ. | |
| R5 | Đúng; CHẶN bước 3 | (a) Thứ tự: event và booking nối DB, Redis, RabbitMQ qua toxiproxy, nên phải bật toxiproxy trước service. Bản 1 đặt sau: sai. (b) `/home/ubuntu/t063/inj/compose-dir` chứa `/opt/flash-ticket-build/t067-compose/hieu-luc` (đã đọc): phải đổi nội dung file, không chỉ dời thư mục. (c) `deploy/mongodb/compose.yaml:19` bind `../../docs/architecture/data/mongodb/schema.cjs`; nguồn hiện là **thư mục** rỗng do Docker tự tạo (`stat`: directory). Sau dời nó phân giải thành `/opt/flashticket/docs/…`, không phải chỗ bản 1 ghi. Sửa: ghi đúng đường mới, so nguồn, đích, loại mount trước và sau. Đồng ý giữ bộ Compose hiệu lực T-067 và image tới khi hết nhu cầu hoàn tác, và cách tiếp tục khi đứt SSH. | |
| R6 | Đúng; CHẶN phần VNPay/đường hầm của §11 | `tai_linux.py:189-210`: `preflight` luôn gọi `kiem-mock.py` (`RECOVER=True`) và `tunnel-remote.py` (`ACTION=start`). Hai helper tự khởi chạy tiến trình trần nếu không thấy PID. Chuyển sang Compose mà không sửa helper thì có hai nơi khởi chạy. Đề xuất: đợt dọn giữ cơ chế hiện tại, chỉ đổi đường dẫn; chuyển sang Compose để lượt riêng. | |
| R7 | Đúng; CHẶN dùng các phép kiểm để nghiệm thu | B4: requirements không ghim `pip`; so freeze mới với freeze cũ (kể cả pip) và ghi phiên bản Python. B13: `results/T-066/hoi-quy-v082.json` cho ca `ebd5ef38` `dung_lai_dau_vao: true`; trên obs không có `outputs/ebd5ef38/method-input.json` (đã kiểm); `chay_ca.py:36,54-55` cần `--dung-lai-dau-vao` để dựng lại từ gói ca. Đích cũ đã tồn tại nên phải ra thư mục mới (trùng N1). `kiem-hop-dong.py`: đọc code thấy `ctl.start(args, {})` rồi `tai_linux.py:263` đọc `manifest['labCommit']`, và `verify_sources()` (dòng 121-133) kiểm git thay cho hash nguồn. Hai test lỗi sẵn từ trước, không do dọn; bỏ khỏi phép kiểm hoặc ghi rõ. Tín hiệu: `tieu-chi.json` khai lượt 10 phút cộng GET `/api/v1/me`; bản 1 ghi 5 phút là sai. Chọn trước: dùng đúng tiêu chí 10 phút (cần Minh duyệt phát tải). | |
| R8 | Đúng; CHẶN đổi UID luật và dừng bộ nhận | `incidents.py:84-85` ưu tiên nhãn `t072_uid`; `t072-luat.yaml` có 11 dòng `t072_uid`. Đổi UID mà giữ nhãn thì bộ gom vẫn xuất mã cũ; đổi cả nhãn thì B11 trượt. Bộ nhận thuộc project riêng `t073-webhook`; hoàn tác bản 1 không tính tới. Đề xuất: giữ UID luật, nhãn và contact point; chỉ đổi tên folder và nhóm hiển thị (cần kiểm đổi nhóm không đổi UID). Giữ bộ nhận nhẹ chạy, chỉ dời env và thư mục ra; hoàn tác gồm cả project này. | |
| R9 | Đúng; CHẶN việc xóa `/opt/rca-tai` | DECISIONS (dòng 778): "Q5: T-066 giữ mục 2.6". `results/T-066/danh-sach-xoa.md:32,50`: 2.6 là `/opt/rca-tai`, giữ vì `load/fixtures/fixture.py` còn đọc `/opt/rca-tai/secret` và `/opt/rca-tai/k6`. Bản 1 dựa vào "đã có ở D:/RCA-archive" là sai một phần (kho chỉ có `out/`). Sửa: không xóa, không dời `/opt/rca-tai` trong đợt này. Không xóa `/home/ubuntu/t063` nguyên cây: `thu3` là lịch sử, chuyển vào archive. | |
| R10 | Đúng một phần; CHẶN tiêu chí tên và đường STOP | Đúng: bản chụp có thư mục `results/T-*` (bất biến B2) và runner mở cấu hình V082 theo đường tương đối dưới `results/T-064/`; tiêu chí "không tên t0xx" phải miễn bản chụp và tài liệu lịch sử. Đúng: `chuoi_tai.py:63-65` dùng hai cờ STOP (`runs/STOP` và `load-controller/STOP`); bản 1 chỉ ghi một. Đúng: máy tải là `/dev/root` (`df`), bản 1 ghi "/dev/sda1 cả ba máy" là sai chữ; `/opt`, `/srv`, `/etc` vẫn cùng một filesystem nên `mv` vẫn đổi tên tại chỗ. Chưa tái hiện được con số 34 file: `git grep -l -E '/opt/rca-lab\|/srv/rca-lab\|/etc/rca-lab' main` (main = 4b6c4b2) cho 32. Đồng ý ghi lệnh đếm cùng con số. Lịch: runner băm file `--lich` cục bộ, nên lịch được duyệt đặt trong thư mục lượt trên obs, chép từ repo RCA. | |
| N1 | Tự tìm; KHÔNG CHẶN | Hồi quy V082 trong bản 1 không ghi thư mục ra; lệnh runner ghi vào `--ra {M1_ROOT}/v082`. Gộp vào sửa R7. | |
| N2 | Tự tìm; KHÔNG CHẶN | Thư mục mới cấp một không ghi chủ và quyền. Gộp vào sửa R4. | |
| N3 | Tự tìm; KHÔNG CHẶN | Tag image `arm64-t067-36a3725d` và nhãn container `t062=topology` mang mã task. Ghi là phần còn lại, hoặc gắn tag mới cùng digest. | |
| N4 | Tự tìm; KHÔNG CHẶN | Nếu đổi gì trong `t072-luat.yaml` thì script sinh ở T-072 không tái tạo được file. Theo đề xuất R8 (giữ UID) thì chỉ đổi tên folder và nhóm: ghi chú đầu file. | |

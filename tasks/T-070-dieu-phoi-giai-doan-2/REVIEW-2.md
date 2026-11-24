# Phản biện T-070 — kiểm lại kế hoạch dọn bản 2

- **Người phản biện** Codex. **Người làm** Claude. **Ngày** 24/11/2026.
- **Công đoạn** Kiểm lại phản hồi và sửa, lượt 2. Việc vận hành trước W7, ngoài G0–G4. Minh cho ghi riêng `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-2.md`.
- **Bản đã đọc** RCA `74b2515d8`, lab `main@4b6c4b2`. Các số dòng của kế hoạch dưới đây thuộc `results/T-070/don/KE-HOACH-DON.md` bản 2. Đường mã lab tính từ repo `D:/Project/flashticket-rca-lab`.
- **Tự soát độc lập** Đọc AGENTS của hai repo, STATE, SPEC, hai bản kế hoạch, bảng kiểm kê, mã và hiện vật gốc trước khi mở bảng phản hồi R1–R10/N1–N4, §15 và kết luận trong LOG. Nguồn đối chiếu gồm HOP-DONG I7–I12, hồ sơ máy/hồi quy/danh sách xóa T-066, manifest T-064, DT18-NV2/NV3, hướng dẫn của cô ngày 23/09, MRP P9/P10, WHY-08/98/100/101, DECISIONS ngày 16 và 23–24/11, LESSONS SL23/SL37/QT18. Sau đó đối chiếu `REVIEW.md` và LOG ngày 24/11 từ 10:20Z đến mục duyệt viết bản 2.

## Kết luận chung

**Giữ khung và các quyết định đã sửa, gồm giữ UID Grafana, bộ xuất G1, bộ nhận nhẹ và `/opt/rca-tai`.** Không còn phản đối việc chụp hiện trạng theo bước 0 đã giới hạn trường xuất, khi Minh cho bắt đầu. Cần sửa vài dòng trước đúng bước chịu ảnh hưởng, đặc biệt là nguồn bind của Keycloak, lệnh hoàn tác app, quyền ghi hồi quy và danh sách xóa container.

Bản 2 là kế hoạch vận hành. Nó bảo toàn đầu vào và đường hiển thị cho P9/P10 tới mức được kiểm. Chưa có phép so trước/sau dời. Việc nghiệm thu T-070 còn theo SPEC §“Tiêu chí xong”, trong đó có W4/W5, W8 và W9a. Lượt này không cho căn cứ mới về chất lượng RCA, không mở W7.

## Các điểm

### PB1. Phép kiểm offline từ chối một file phủ hợp lệ — CHẶN dùng bước 1.3 để duyệt merge

Dòng 437 yêu cầu chạy `docker compose config --quiet` cho từng file. `app-host/overrides/event-service.yml` chỉ bổ sung env, mount, giới hạn bộ nhớ và cách ghi log. Image nằm ở file cơ sở. Trên app, tôi đã dùng biến giả và gọi `docker compose -p test-r2 -f app-host/overrides/event-service.yml config --no-env-resolution --quiet`. Mã trả về 1, với thông báo `service "event-service" has neither an image nor a build context specified`. Lệnh chỉ đọc cấu hình.

**Sửa nhỏ nhất.** Với file phủ, kiểm cặp file theo đúng thứ tự mà `app-host/scripts/hieu_luc.py` dùng: `deploy/app/<svc>.yml` của revision ghim, sau đó là file phủ tương ứng. Với một project gồm nhiều file hạ tầng, kiểm đúng tập file của project. File Compose độc lập vẫn kiểm riêng. Không cần thêm bộ thử.

### PB2. Dời file Keycloak giữ lại ba nguồn bind cũ, còn lệnh hoàn tác app trỏ hai nơi — CHẶN bước 3

**Chiều đi.** Dòng 319 chỉ dời `compose-exp/keycloak.yml`. Đọc file thật trên app, dòng 14–16 còn ba nguồn tuyệt đối dưới `/opt/flash-ticket-app/otel` và `/opt/flash-ticket-infra/keycloak/keycloak/{themes/flash-ticket,import}`. `docker inspect flash-ticket-keycloak-keycloak-1` xác nhận cả ba đang gắn. Khi các cây nguồn chuyển chỗ, một lần `up` bằng file chưa sửa có thể gắn thư mục rỗng, làm thiếu Java agent, theme hoặc dữ liệu import. Dòng `env_file: ../env/keycloak.env` tự phân giải đúng ở cây mới. `hieu_luc.py` chỉ sinh file cho bảy service Spring, không sinh file cho Keycloak.

**Chiều lui.** Dòng 317 dời **cả** `t067-compose/` vào archive. Dòng 475 yêu cầu `mv` ngược rồi `up` từ archive. Nếu đã dời ngược dòng 317 thì ở archive không còn bộ đó. Nếu vẫn giữ ở archive thì file của service nằm dưới **`hieu-luc/`**, còn `deploy.sh` đòi `$DIR/<service>.yml`. Các file hiệu lực cũ vẫn dẫn đến env, secrets và fault-control ở đường cũ. Lệnh `up` bảy service cũng không tự bật lại hạ tầng, proxy, Keycloak, Collector và hai tiến trình đã dừng ở bước 3.1.

**Sửa nhỏ nhất.** Ghi ba thay thế nguồn bind vào đúng file Keycloak và giữ lại nội dung cũ để lui. Chọn một đường hoàn tác: trả bộ T-067 về `/opt/flash-ticket-build/t067-compose/hieu-luc`, trả nguồn bind/env và `compose-dir` về chỗ cũ, rồi bật lại các thành phần theo thứ tự phụ thuộc đã nêu ở §9.3. Đối chiếu B8 ngay trên máy. Ngoài env/mount, giữ được các trường hiệu lực ảnh hưởng phép đo như giới hạn bộ nhớ, chế độ mạng và nhãn ghi log. Inspect Event hiện cho `Memory=1073741824`, `NetworkMode=host` và hai nhãn Compose trong cấu hình log. Có thể dùng lại `diff(mask(cũ), mask(mới))` của `hieu_luc.py` cho các service, chỉ lưu kết quả so đã che giá trị.

### PB3. Hai đường dẫn phải sẵn sàng trước khi gọi bộ nhận và phép hồi quy — CHẶN lệnh tương ứng ở bước 2 và Q3

| Chỗ | Đường thực thi và hậu quả | Sửa nhỏ nhất |
|---|---|---|
| Bộ nhận, dòng 295, 453, 459 | File Compose có cả `t072-bo-nhan` và `t073-webhook`. Hai nguồn bind dùng `create_host_path: false`. Env cũ đặt `T073_SPOOL_DIR` ở `runs/t073-khong-dung-o-e3/spool`; `test -d` trên obs trả 1. Đây là giá trị dự phòng hợp lệ khi chỉ bật bộ nhận nhẹ. Lệnh `up` cả project có thể gọi thêm dịch vụ E5 và trượt ở bind không tồn tại. Kế hoạch có nêu mục đích “up bộ nhận”, nhưng thiếu tên service ở chính bước thao tác. | Ghi rõ `up -d t072-bo-nhan` ở cả chiều đi và chiều lui. Giữ đủ các biến Compose bắt buộc khi nội suy; tạo trước `alerts/bo-nhan/` cho uid chạy container. Không cần bật dịch vụ E5 hay tạo spool giả của E5. |
| Hồi quy, dòng 194, 494 | Kế hoạch ghi cha `rca/` là `root:rca 755`, còn đích `hoi-quy-sau-don/` “chưa tồn tại”. User `rca` không có quyền tạo con trong cha 755. `chay_ca.py:124` gọi `mkdir(parents=True, exist_ok=False)` ở `<ra>/<id>`. Nếu hiểu “chưa tồn tại” cho chính thư mục `--ra`, cả hai ca sẽ dừng trước khi ghi đầu ra. | Bên vận hành tạo trước **thư mục cha** `--ra` mới với `rca:rca 750`; chỉ hai thư mục **con mã ca** phải chưa tồn tại. Mỗi lượt thử lại có đích khác. Giữ nguyên hai chuẩn và cờ dựng lại đầu vào của ca thứ hai. |

Cùng ở bước 2.3, chỉ tạo **thư mục cha** trước khi đổi tên cả cây `m1` thành `rca`. Nếu tạo sẵn đích `rca/` rồi gọi `mv m1 rca/`, kết quả là `rca/m1/`; pins và cases nằm sâu hơn một cấp. Sau khi đổi tên đúng, đặt mode 755 cho gốc rồi mới tạo các con mới ở §5.3. Đây là điều kiện chạy, chưa có lần dời hay hồi quy sau dời thất bại.

### PB4. Danh sách xóa container bao gồm một lượt hỏng còn log ở Docker — CHẶN xóa hàng loạt ở §11

Tôi liệt kê container `rca-tai-*` trên máy tải, lọc `State.Status == exited`, lấy nguồn mount có đích `/out`. Chỉ kiểm metadata của `LogPath` và sự tồn tại của `<nguồn>/container.log`, không đọc nội dung log. Kết quả: **106** container đã thoát. **102** có file `container.log` cạnh đầu ra. **Một** có mount nhưng thiếu file này. **Ba** không có mount `/out`.

Phản ví dụ là `rca-tai-d2-2e071903` (exit 107). Docker còn log 290 byte. Thư mục nguồn `/opt/rca-tai/out/d2-2e071903` và bản tương ứng trong `D:/RCA-archive/load-generator/load-runs/out/` đều có file đầu vào và giờ bắt đầu, thiếu `container.log`. Giữ 2.6 theo Q5 không tự giữ log do Docker quản lý. Ba `verify-00{1,2,3}` là lệnh k6 inspect đã được ghi trong `results/T-062/tai/thay-doi-may-tai.md`; không gộp chúng thành ba lượt tải hỏng. Có file cạnh 102 lượt cũng chưa chứng minh các bản log đều trùng byte.

**Sửa nhỏ nhất.** Giữ nguyên bốn container ngoại lệ, hoặc trước khi xin xóa thì bảo toàn log và trạng thái cần giữ ngay trên máy. Một bản tương đương có thể đã được lưu ở chỗ khác. Muốn dùng làm căn cứ xóa, chỉ cần chỉ ra bản đó và đối chiếu đúng hiện vật. Không cần kéo tập tải về laptop hoặc chạy lại k6. Dữ liệu hiện có chưa bị xóa.

### PB5. Kiểm cây Git sạch còn lọc tên thư mục sắp bỏ — CHẶN xác nhận revision cho lượt tải sau dời

Dòng 239 đổi `campaigns/` thành `rca/`. Dòng 441 bỏ bộ test cũ khỏi nghiệm thu là hợp lý, nhưng hai chỗ chạy thật vẫn cần đổi bộ lọc. `load/controller/tai_linux.py:128` và `load/controller/chuoi_tai.py:174` đều gọi `git status --porcelain -- load campaigns inventory`. Một chỉnh sửa chưa commit chỉ ở `rca/` sau dời sẽ nằm ngoài kết quả của cả hai. Lượt tải khi đó có thể ghi HEAD trong hồ sơ trong khi mã chạy khác HEAD. Quét ba tiền tố đường máy ở §8 không bắt được literal `'campaigns'` này.

**Sửa nhỏ nhất.** Ghi rõ đổi pathspec (danh sách đường Git kiểm) ở **cả hai** chương trình thành `load rca inventory`, cùng thông báo tương ứng. Đây là phép đổi đường theo B5, không cần khôi phục bộ test hash cũ.

### PB6. Phạm vi kết luận sau dời phải theo đúng đầu ra đã kiểm — CHẶN riêng tuyên bố Q4 đạt đủ hoặc đường online nguyên vẹn

- **Q4.** Dòng 497 đã khôi phục 10 phút ×1 và GET `/api/v1/me`. Tiêu chí gốc `tests/signals/tieu-chi.json#/buoc_7/luong_chinh` còn yêu cầu đối chiếu vé của một đơn COMPLETED. `check_purchase_journey.py:151–156` cho `mot_ve.ket_qua = chua_kiem` nếu không truyền kết quả DB của **chính đơn đó**. Số đơn trước/sau ở B9 không phân xử điều kiện này. Nếu Minh duyệt Q4 đầy đủ, dùng `--don` và `--don-db-json` như giao diện sẵn có. Nếu chỉ duyệt kiểm tín hiệu hẹp, ghi rõ điều kiện một vé còn mở, không ghi Q4 đạt đủ.
- **RR7.** Kiểm nạp L2, link của bộ cũ và hồi quy lõi có giá trị riêng. Chúng không chạy `stage_b → run_m1 → V082 → g1_b` trên một ca mới sau dời. Bản 2 đã nói rõ giới hạn ở dòng 536, nên việc chưa phát lại **không chặn dời** nếu Minh chấp nhận giới hạn đó. Nếu cần xác nhận tuyến online, dùng ngay một capture dev lưu sẵn vào đích `online-*` mới, không phát tải. Khi đọc `check_old_case.py so`, phải xem từng kết quả: hàm `so` ghi so hash gói bổ sung và G1 riêng, không cộng chúng vào `trung_tat_ca`; nếu G1 thiếu còn `continue`. Với đồ thị dịch vụ, xem cả trạng thái do `sau_v082.py::do_thi_dich_vu` trả vì hàm có nhánh ghi lỗi rồi trả trạng thái. Không cần mở test hay đòi làm lại W5.

## Đối chiếu các lượt trước

Đánh giá dưới đây phân biệt chẩn đoán của Claude với mức xử lý thực tế trong bản 2. Các mã PB1–PB6 dưới đây chỉ các điểm của bản phản biện này.

| Điểm | Đánh giá phản hồi | Bằng chứng và phần còn lại |
|---|---|---|
| R1 | Đúng | Bản 2 dòng 111, 415–424 chuyển so sánh về trên máy và giới hạn trường xuất. Không còn đề xuất lưu cấu hình đã giải biến. Khi dò đường ở bước 0 chỉ cần ghi tên file/đường cần dời. |
| R2 | Đúng | Dòng 224–245 giữ module và hai literal, đổi tiền tố vùng ghi, tiếp tục bảo vệ bộ chính. Gọi `nap_bo_xuat` trên mã gốc với ba đường giả, nạp hàm thành công mà không ghi file. Đây là bằng chứng cho cơ chế nạp. Giới hạn xác nhận toàn tuyến ở PB6. |
| R3 | Đúng | Đếm lại bằng `rglob('*.json')` trong bộ `t065-l11-001/service-graph` trên obs: 109/218 file có `/d/t065-l8b-rca`. Giữ UID và đổi đường dữ liệu đáp đúng phản ví dụ, B12 còn có phép bấm thật sau dời. |
| R4 | Đúng | Đã định owner/mode 700 cho hai thư mục nhật ký. Chú ý phép `test -r`: trên obs user `rca` trả 1 cho cả `t069-chinh.out` thực sự tồn tại và một tên không tồn tại. Khi nghiệm thu, chọn file mà chủ đã xác nhận có thật hoặc kiểm quyền đi qua cha mới bằng `test -x` khi nó còn rỗng. |
| R5 | Đúng về chẩn đoán, sửa một phần | Thứ tự proxy, nội dung `compose-dir`, chỗ phân giải mount MongoDB và cách tiếp sau đứt SSH đã sửa. Nguồn `schema.cjs` hiện là thư mục rỗng; hiện trạng không xác định được ai tạo nó hoặc chứng minh nó chưa từng là file trong quá khứ. Chốt theo loại và nội dung tại thời điểm dời. Phần app còn PB2. |
| R6 | Đúng | Giữ một nơi quản lý tiến trình. Mã máy của tunnel supervisor lấy gốc từ `__file__`; mock lấy env và state từ thư mục chứa script. Việc chuyển Compose đã hoãn đúng. |
| R7 | Đúng về chẩn đoán, sửa một phần | B4 so hai freeze và Python; B13 tách cờ từng ca; hai test lỗi cũ không còn dùng để phán hồi quy. Còn điều kiện thư mục của B13 (PB3), cách chạy Compose (PB1), nguồn DB cho Q4 (PB6) và hai bộ lọc thật (PB5). |
| R8 | Đúng | Giữ UID, title, nhãn và đích nhận. Quy tắc `ma_luat` ưu tiên `t072_uid`, có nhánh `rulename` cho cảnh báo nguồn. Project bộ nhận đã xuất hiện trong cả hai chiều. Còn việc gọi đúng service ở PB3. Việc Grafana chuyển folder/nhóm là RR2 đã khai: kiểm UID/nhóm thực tế sau nạp, nếu không đạt thì lui. |
| R9 | Đúng | Q5 và mục 2.6 T-066 khớp với việc giữ cả cây `/opt/rca-tai`; trên máy còn cả `k6/` và thư mục secret. `t063/thu3` có đích lưu. Docker giữ log ở nơi khác, nên phần xóa container còn PB4. |
| R10 | Phản hồi đúng một phần | Hai STOP, lịch cục bộ, ngoại lệ snapshot và filesystem đã được xử lý. `findmnt -T` cho cùng `/dev/nvme0n1p1` ở `/opt/rca-tai`, `/srv`, `/etc` trên máy tải. Riêng số 32 bị bác trên revision đã nêu. Hai lệnh đếm bên dưới đều cho 34. |
| N1 | Đúng một phần | Bản 2 tách đích chuẩn và đích mới, nhưng phải chuẩn bị cha ghi được như PB3. |
| N2 | Đúng | Bảng quyền mới giải quyết nguy cơ đã nêu cho lịch sử `runs`. Theo dõi điều kiện phép thử ở dòng R4. |
| N3 | Đúng | Dòng 375 giữ tag image. Dòng 331 nói tái tạo toxiproxy chỉ đổi đường bind, còn 375 nói bỏ nhãn `t062=topology`. Đề xuất giữ cả nhãn hiện có trong đợt này cho đúng phạm vi. Đây là chênh lệch nhỏ, không phải finding về RCA. |
| N4 | Đúng | Dòng 267 giữ liên hệ với bộ sinh lịch sử. Khi kiểm B11, so cấu trúc YAML để phần chú thích nguồn không làm trượt phép so. |

Hai biểu thức dưới đây trả cùng **34 file** khi đếm số dòng ở checkout lab trên laptop. Dùng toán tử alternation `|` thực của regex, không chép dấu thoát cột của bảng Markdown vào câu lệnh. Không cần giữ RR9 ở trạng thái chưa phân xử cho phép đếm này.

```powershell
(git grep -l -E '/opt/rca-lab|/srv/rca-lab|/etc/rca-lab' 4b6c4b2 -- | Measure-Object).Count
(git grep -l -E '/(opt|srv|etc)/rca-lab' 4b6c4b2 -- | Measure-Object).Count
```

## Tuân thủ quy trình

LOG ghi N1–N4 lúc 15:05Z rồi mới đọc kết luận lượt 1 và đáp lúc 15:40Z. Mục 16:20Z ghi Minh duyệt **viết bản 2**. Bản 1 lưu nguyên byte, SHA-256 khớp mốc đã đọc ở lượt 1. K1–K7 về bố trí, Q2–Q4 và lệnh triển khai vẫn chờ theo kế hoạch/LOG. Sửa kế hoạch được duyệt không tự cấp quyền chạy máy, sửa code, xóa hoặc push. Không thấy một thay đổi phương pháp, việc ghép nhãn hay quyết định khoa học mới cần ghi WHY cho lượt này.

Các chỉnh sửa tối thiểu đề nghị đều cho kế hoạch trước. Không thấy bản kế hoạch hay REVIEW-2 được ghim trong các manifest/plan đã rà của T-066/T-070. Nếu triển khai, sửa bộ lọc Git hay Compose làm đổi commit lab. Giữ nguyên commit cũ, manifest T-064, hai chuẩn T-066, snapshot và dữ liệu ca gốc. Cột “Minh quyết” ở bản cũ thuộc Minh; không sửa bản lượt trước, LOG hoặc STATE.

## Điều đã kiểm và thấy đúng

- Tính lại **49/49** dòng trong `kiem-ke/SHA256SUMS`. So SHA-256 cây RCA với từng đường trong `m1-ban-chup.tsv` đạt **149/149**. So `manifest-3.json` với hash ở đính chính T-066 §1, rồi đối chiếu hai file trong `hoi-quy-v082.json#/ca/{0,1}/chuan`, đều khớp. `find m1/v082-hoi-quy -name 'method-output-*.json' -exec sha256sum {} +` trên obs cho bốn file khớp hai chuẩn tương ứng.
- Đối chiếu hai bản, Git báo 341 dòng thêm và 247 dòng bỏ. Kiểm trực tiếp revision lab trên obs/app/tải lần lượt là `1bb40ca`, `407b4f5`, `5a39028`. Các phép SSH chỉ đọc. Không dời, gỡ, chạy tải, tiêm lỗi hay mở dữ liệu khóa.
- Không phát hiện bản 2 dùng nhãn để chọn đầu vào, tập ứng viên hoặc cách xếp hạng. B5 thu hẹp sửa phía lab, B6 bảo vệ vùng nhật ký. Bộ xuất G1 đọc kết quả phương pháp để hiển thị. Việc giữ UID bảo toàn liên kết hiện có. Không có đối chứng “không đồ thị” hoặc phép đánh giá mới cần kết luận trong lượt này.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm.** So bản 2 với bản gốc, kiểm từng phản hồi R1–R10 và N1–N4, lần theo nguồn bind, user thực thi, nơi lưu log và các điều kiện chấp nhận.
2. **File thay đổi.** Chỉ tạo `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-2.md`.
3. **Kiểm.** Đã tái hiện lỗi kiểm file phủ đứng riêng, xác nhận ba bind Keycloak, quyền ở obs, nguồn log k6 và con số 34. Các kiểm tích hợp sau dời chưa chạy.
4. **Minh quyết.** Đề xuất **tiếp tục một lượt Claude đáp tập trung vào các bước trên**. Giữ nguyên các phần đã thống nhất. Cho từng bước đi tiếp sau khi sửa đúng điều kiện của bước đó và có lệnh riêng của Minh. Giữ bốn container ngoại lệ là phương án ít công nhất; nếu cần giải phóng chúng, bảo toàn đúng log/trạng thái trên máy trước. Với RR7, nếu mục đích là tuyên bố hệ thống online dùng được sau dời, chọn phát lại một ca dev sẵn có. Nếu Minh chỉ cần nghiệm thu bố trí và lõi, ghi giới hạn minh bạch rồi để việc xác nhận tuyến online đến lúc cần dùng. Đường thực thi có thể phân xử bằng mã, cấu hình và hiện vật sẵn có, không cần thêm cổng hay chiến dịch tải.

## Prompt bàn giao cho người làm

Minh có thể chuyển nguyên khối dưới đây cho Claude.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-070, tasks/T-070-dieu-phoi-giai-doan-2/. Kế hoạch dọn repo lab và ba máy, results/T-070/don/KE-HOACH-DON.md, bản 2 ngày 24/11/2026.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giai đoạn 2, kế hoạch vận hành trước W7, ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-070.
- Tài liệu gốc: results/T-070/don/KE-HOACH-DON.md và KE-HOACH-DON.ban-1.md, results/T-070/kiem-ke/, AGENTS.md, SPEC, LOG và HOP-DONG của T-070, cùng hồ sơ T-066 được dẫn trong kế hoạch. RCA HEAD 74b2515d8.
- Phản biện và phản hồi trước: tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md, mục đáp lượt 1 trong LOG.md, rồi REVIEW-2.md. Sau khi tự soát, phản biện các đề xuất đang trình Minh trong bản lượt 2.
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab, main 4b6c4b2, obs 1bb40ca, app 407b4f5, tải 5a39028. Mã RCA ở src/m1, src/m1_ft, src/p3. Chỉ cần đọc máy thì dùng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs|tai, script qua stdin, chỉ lệnh đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat trừ khi Minh cấp quyền ghi cụ thể cho lượt đáp. Làm trong phiên này, không dùng subagent, không sửa máy.

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
| PB1 | Đúng; CHẶN bước 1.3 | `git show 4b6c4b2:app-host/overrides/event-service.yml` không có `image:`; file phủ đứng riêng không hợp lệ với `compose config`. Sửa trong bản 3: kiểm cặp file theo thứ tự `hieu_luc.py` (file nhóm của revision ghim + file phủ); project nhiều file kiểm đúng tập file; file độc lập kiểm riêng. | |
| PB2 | Đúng; CHẶN bước 3 | Bản lab `app-host/services/keycloak.yml:14-16` có ba bind tuyệt đối; tôi chưa đọc bản đang chạy, Codex đã `inspect`. Hoàn tác bản 2 mâu thuẫn (mv ngược và up từ archive; `deploy.sh` cần `$DIR/<service>.yml` còn file nằm dưới `hieu-luc/`). Sửa trong bản 3: ghi ba thay thế bind của Keycloak, giữ bản cũ để lui; chọn một đường hoàn tác: trả bộ T-067 về chỗ cũ, trả bind/env/`compose-dir`, bật lại đủ thành phần theo thứ tự phụ thuộc; B8 so thêm giới hạn bộ nhớ, `NetworkMode`, nhãn log bằng `diff(mask(cũ), mask(mới))`. | |
| PB3 | Đúng; CHẶN bước 2 và Q3 | Bộ nhận: env cũ có `T073_SPOOL_DIR` trỏ thư mục không tồn tại; phải gọi `up -d t072-bo-nhan`. Hồi quy: `rca/` 755 root:rca thì user `rca` không tạo được `--ra`; `chay_ca.py:124` chỉ tạo `<ra>/<id>`. `mv m1 rca/` khi đích đã có sẽ ra `rca/m1/`. Sửa trong bản 3: gọi đúng service ở cả chiều đi và lui; tạo trước `alerts/bo-nhan/`; tạo trước thư mục `--ra` (rca:rca 750), chỉ hai thư mục mã ca chưa tồn tại; `mv /srv/rca-lab/m1 /srv/flashticket-rca/rca` khi `rca` chưa tồn tại, rồi mới chmod và tạo con. | |
| PB4 | Đúng; CHẶN xóa hàng loạt | Kiểm trên máy tải: 106 container `rca-tai-*` đã thoát; `rca-tai-d2-2e071903` thoát mã 107, Docker còn file log; `/opt/rca-tai/out/d2-2e071903` không có `container.log`. Sửa trong bản 3: giữ bốn container ngoại lệ (`d2-2e071903`, `verify-001..003`); chỉ đề xuất xóa 102 container có `container.log` cạnh đầu ra, và trước khi xin xóa sẽ so byte log Docker với `container.log` trên máy. | |
| PB5 | Đúng; CHẶN xác nhận revision cho lượt tải sau dời | `tai_linux.py:128`, `chuoi_tai.py:174` gọi `git status --porcelain -- load campaigns inventory`. Sửa trong bản 3: đổi pathspec ở cả hai thành `load rca inventory` (đổi đường theo B5). | |
| PB6 | Đúng; CHẶN tuyên bố Q4 đạt đủ và tuyến online nguyên vẹn | `check_purchase_journey.py:151-156`: không có `--don-db` thì `mot_ve` là `chua_kiem`. Sửa trong bản 3: Q4 đầy đủ dùng `--don` và `--don-db-json` của một đơn COMPLETED. RR7: đề xuất phát lại một ca dev lưu sẵn vào đích `online-*` (không phát tải), đọc từng mục kết quả của `check_old_case.py so` và trạng thái `do_thi_dich_vu`. Mặt trái: thêm một lượt chạy trên obs (vài phút). Phương án khác: ghi giới hạn, chỉ nghiệm thu bố trí và lõi. | |
| R10 (đếm) | Phản hồi trước của tôi sai | Chạy lại với `MSYS_NO_PATHCONV=1`: cả hai lệnh cho 34 file tại `4b6c4b2`. Con số 32 do Git Bash tự đổi chuỗi bắt đầu bằng `/` trong đối số. Bỏ RR9. | |
| Ghi chú lượt 2 | Đồng ý | R4: `test -r` trả 1 cả với file không tồn tại; chọn file đã xác nhận có bằng chủ, hoặc kiểm `test -x` trên cha. N3: giữ nhãn `t062=topology` khi tạo lại toxiproxy. R5: `schema.cjs` chỉ ghi "hiện là thư mục rỗng", không kết luận nguồn gốc. N4: B11 so theo cấu trúc YAML. | |
| S3 (tự tìm) | KHÔNG CHẶN | Dựng lại venv cần obs tải gói từ PyPI; chưa kiểm obs có mạng ra ngoài. Thêm vào bước 0: thử `pip download --no-deps` một gói nhỏ vào thư mục tạm. Không có mạng thì dừng trước bước 2, trình cách khác. | |
| S4 (tự tìm) | KHÔNG CHẶN | L1 đổi tiền tố đích `online-*`; `orchestrator.py` đang tự đặt đích `rca-results/t073-<lượt>` → phải đổi cùng L1. | |

# Phản biện T-070, lượt 6

**Codex phản biện, Claude làm. 28/11/2026.** Kiểm phản hồi và bản sửa REVIEW-5. Đây là lượt vận hành giai đoạn 2, ngoài G0–G4. Revision RCA khi đọc là `75e239c2a`. Trong lab, `git diff c1da15f da9c843` chỉ đổi `chuoi_tai.py` và `g1_b.py`. `git show 94bb11e` đổi đường webhook trong Compose, README và bộ nhận của T-076. Hai file T-070 tại HEAD có cùng nội dung với `da9c843`.

**Tự soát độc lập.** Trước khi đọc các bảng phản hồi, tôi lần từ `tai_linux.start/get` tới nhật ký, bước chấm và nhận tải, từ `g1_b.khoi_tao` tới hai chỉ mục và dashboard. Đã đối chiếu nguồn Q4 với tiêu chí, bản tin gốc và thử hai đường lỗi trong bộ nhớ. Sau đó mới đọc REVIEW đến REVIEW-5 theo thứ tự, các bảng của Claude, mục duyệt và tự kiểm ngày 28/11 trong LOG, rồi đối chiếu với runbook T-076 bản 3.

**Nguồn.** AGENTS của hai repo, STATE, SPEC, LOG, TRANG-THAI, LICH-MAY, HOP-DONG T-070, kế hoạch dọn bản 3.1, các hiện vật trong `results/T-070/don/`, tiêu chí lab `tests/signals/tieu-chi.json#/buoc_7`, biểu thức luật Grafana, DT18-NV1–NV3, hướng dẫn cô 23/09, MRP P9/P10 và RQ5, WHY-103/111, DECISIONS 20–24/11, LESSONS QT18. Các kết luận dưới đây chỉ dùng dữ liệu được phép.

## Kết luận chung

**Giữ Q4 đạt tiêu chí tín hiệu. Đề xuất tiếp tục phản biện hai đường vận hành.** Sau khi `start` thất bại trước bước tạo container, bộ chuỗi vẫn có thể chấm và nhận một lượt cũ. G1 có thể báo `da_co` với bản chép thiếu ca. Hai lỗi đã tái hiện trong bộ nhớ. Chưa có bằng chứng hai lỗi đã làm sai một lượt thật. Bước 9 T-076 gọi trực tiếp `tai_linux.py`. Với lần đầu của bước 10, runbook có đối chứng toàn cây trước khi chuyển dashboard.

## Các điểm

### R1. Bộ chuỗi nhận lượt cũ ngay trong lần phát bị từ chối — CHẶN phát lịch qua `chuoi_tai`

Trong lab `da9c843`, `tai_linux.py:149,242–251` kiểm máy tải có container đang chạy **trước** khi kiểm tag đã dùng. Nếu chính container cũ cùng tag đang chạy, lỗi trả về là `A rca-tai- container is running`. Lần phát này chưa tới `docker run`. Tuy nhiên `chuoi_tai.py:267–301` gọi `get(tag)` trước khi phân loại lỗi trước phát. Nếu container cũ vừa kết thúc và có `StartedAt` trong dung sai 120 giây, code ghi `phat_co_container`. `cho_xong` tiếp tục theo tên và thời gian. Khi tiếp nhận nhật ký, dòng 404 còn coi `phat_co_container` là đủ để qua chốt mới.

**Phản ví dụ.** Cho hai đồng hồ khớp, container cũ bắt đầu sớm 10 giây, kết thúc sau ý định phát 1 giây. Với chính chuỗi lỗi của `assert_idle`, `Chuoi.chay_luot` trả `xong`. Thứ tự gọi là `start → get → get → kiem → nhan`. Đổi lỗi thành timeout của `start` cũng cho cùng kết quả. Phép thử bên dưới tái hiện nhánh thứ nhất. Khi chỉ có `sap_phat`, bản mới dừng đúng. Khi `phat_loi` ghi rõ `Tag already used`, bản mới cũng dừng đúng. Hai đối chứng này giải thích vì sao các ca kiểm của Claude đạt và vẫn bỏ lọt đường phát trực tiếp.

**Phần đã duyệt còn thiếu.** LOG ngày 28/11, đề xuất 2, ghi “có `phat` thì đối chiếu `containerId`”. `start` trả ID và `phat` lưu trong `ket_qua`. `get` chỉ trả `.State` của container hiện mang tên đó. Bản sửa bỏ đối chiếu ID. Lý do của Claude đúng về dữ liệu mà `get` hiện trả. Nó chỉ chứng minh đã phát thành công tại thời điểm `start`. Khi tiến trình tiếp nhận, cùng tên và giờ hợp lệ chưa phân biệt được container đã lưu với container thay thế. Có `phat_co_container` thậm chí chưa chứng minh lần phát thành công. LOG công khai phần bỏ này. Duyệt commit sau đó có căn cứ riêng, còn hồ sơ đã đọc chưa ghi Minh thay tiêu chí nhận dạng. Theo Luật 0 §2.5, cần trình chính phần khác với đề xuất đã duyệt.

**Đề xuất Minh.** Với lỗi chắc chắn trước phát, giữ đúng trạng thái lỗi chung/cục bộ theo nguyên nhân. Với kết quả phát mơ hồ hoặc nhật ký chỉ có `phat_co_container`, dừng ở `chua_xac_minh` trước chấm, nhận hoặc dừng container theo tên. Với `phat`, đề xuất cho `tai_linux.get` trả thêm ID của cùng lần inspect, giữ trường `state` cho bên gọi cũ, rồi so đúng ID lưu trong nhật ký. ID vắng hoặc lệch thì giữ lượt để xác minh thủ công. Sửa này cần duyệt thêm `tai_linux.py`. Phương án hẹp hơn là dừng tự tiếp nhận khi thiếu bằng chứng nhận dạng, đổi lại cần người xử lý một lượt thật bị gián đoạn. Siết dung sai giờ vẫn nhận nhầm được. T-076 bước 9 dùng bộ tải trực tiếp nên R1 không chặn bước đó.

### R2. Chỉ mục xuất hiện trước khi chép xong dữ liệu ca — CHẶN dùng `da_co` để xác nhận bộ G1 hoàn chỉnh

`rca/online/g1_b.py:85–106` đổi đúng thứ tự hai cây. Nguồn thiếu một thành phần bắt buộc bị từ chối. Khi chép `du-lieu/`, `shutil.copytree` duyệt mục con theo `os.scandir`. Nó có thể ghi `chi-muc-ban.json` trước các thư mục ca. Lần sau, nếu có chỉ mục và thư mục `service-graph/`, hàm trả ngay `da_co`, không đọc phần dữ liệu ca còn thiếu. `kiem_dich` kiểm chủ sở hữu và liên kết, nên một cây sạch nhưng thiếu tệp vẫn qua.

**Bằng chứng.** Chạy `python3 -B` trên obs chỉ đọc. `os.listdir('/srv/flashticket-rca/rca/results/dev/du-lieu')` trả theo thứ tự `trang-thai, chi-muc-ban.json, V082-V066+H8a, p7, V071-V041+H8a`. Thứ tự có thể thay đổi. Chỉ riêng thứ tự vừa quan sát đã cho phép lỗi. Trong bộ nhớ, thay thao tác chép bằng hàm ghi nhận từng mục rồi ngắt sau khi tạo chỉ mục chung, trước chỉ mục bản. Lần gọi kế tiếp trả `da_co` dù `du-lieu/<bản>/chi-muc.json` còn thiếu. Ngắt **trước** chỉ mục thì bản mới từ chối đúng. Chép đủ hai cây thì trả `chep` và lần sau `da_co` như dự kiến. Với `rong`, ngắt giữa hai lệnh `write_text` ở dòng 105–106 cũng cho `da_co` với chỉ mục bản chưa có. Trên obs chưa có `online-demo-001` khi kiểm. Không suy ra bộ `dev` hoặc ca Q6 đã hỏng.

**Ảnh hưởng tới T-076.** Runbook bản 3 §4.A.2 đòi lần đầu trả `chep` và đối chiếu đường dẫn + SHA-256 của hai cây với nguồn trước khi chuyển. Nếu so đủ thì phát hiện được tệp thiếu cho **lần chép đầu**. Tuy nhiên, runbook còn yêu cầu cùng hash nguồn ở **mọi lần**. Sau khi ghi một ca mới, `g1_b.py:177–183` chủ động nối mã ca vào hai chỉ mục đã sao từ `dev`. Lần dùng lại sẽ trượt phép so byte kể cả khi toàn bộ ca cũ còn nguyên. Đây là mâu thuẫn giữa phép kiểm của runbook và thay đổi hợp lệ của G1. Nó chặn việc dùng nguyên phép so ấy cho lần tiếp sau, chưa phải sự cố demo đã xảy ra.

**Đề xuất Minh.** Với hàm khởi tạo, chép vào đích tạm cùng hệ tệp và chỉ công bố bộ mới bằng đổi tên sau khi hai cây đã hoàn tất. Áp dụng cùng nguyên tắc cho hai chỉ mục của `rong`, giữ đích dở để đối chiếu. Đích tạo trước bản sửa cần so với nguồn trước khi dùng lại nếu thiếu bằng chứng đã chép trọn. Với T-076, có thể chọn đường ít chờ cho lần đầu là giữ đích mới, một người ghi, đòi `chep` và thực hiện phép so đủ đã có ở §4.A.2. Lần tiếp theo, giữ phép so byte cho tệp ca cũ, còn ở hai chỉ mục so nội dung cũ được bảo toàn và đối chiếu các mục nối thêm với ca demo đã ghi. Đổi lại cần xử lý riêng hai chỉ mục. Tạo bộ riêng cho từng lần cũng được, nhưng tốn thêm một bản chép và mất lịch sử tích lũy trên cùng dashboard. Trình phần runbook ở T-076. Bất kỳ lần bật, đẩy hoặc triển khai nào vẫn cần quyết định riêng của Minh.

### R3. Dòng bàn giao T-070 vẫn yêu cầu duyệt commit đã thực hiện — KHÔNG CHẶN Q4 hoặc kiểm bản sửa local

`docs/STATE.md`, dòng T-070, ghi R1/R2 “chưa commit” và “Chờ Minh duyệt commit lab”. LOG T-070 mục cuối ngày 28/11 ghi Minh đã duyệt, lab commit local `da9c843`. `git log -3` trong lab cho `94bb11e → da9c843 → c1da15f`. Ref `origin/main` lưu tại máy ở `c1da15f`. SSH chỉ đọc obs trả `c1da15f`. Minh xác nhận app và tải cùng ở bản này. `TRANG-THAI.json#/cap_nhat_utc` là ảnh ngày 26/11, còn `#/buoc_tiep_dieu_phoi` chỉ prompt cũ. Sai khác là trạng thái tiếp nhận sau commit. Đính chính trước đó về việc đã đẩy gói RCA `672391b` là đúng.

**Đề xuất Minh.** Ở lượt cập nhật hồ sơ có quyền, cho Claude sửa dòng T-070 và bước tiếp/phiên bản local của TRANG-THAI, giữ riêng revision từng máy và prompt hiện hành. Lợi ích là người nhận không xin lại commit hoặc kéo nhầm cả thay đổi T-076. Có thể chỉ dùng LOG lúc này, nhưng người mở phiên theo STATE sẽ gặp lại chỉ dẫn cũ. Việc này không đòi commit, push hay cập nhật máy trong lượt phản biện.

### R4. Báo cáo Q4 lấy giờ bắt đầu triển khai làm giờ gateway đã lên — KHÔNG CHẶN Q4

Mục 1 của `q4/README.md` ghi “Gateway lên lại lúc 16:38:32Z”. Trong `sau-buoc-3/deploy.tsv` dòng 13–14, 16:38:32Z là `START`, 16:39:13Z mới là `END health=yes eureka=yes running`. Lệnh thực thi nằm ở `sau-buoc-3/lenh-4-bat.sh`. Tại lab `85ace52:test-environment/scripts/deploy.sh` dòng 19–50, script ghi `START` trước lệnh Compose, rồi kiểm HTTP và Eureka trước khi ghi `END`. Vì vậy kết quả Prometheus rỗng lúc 16:38:40Z chưa phân biệt được gateway còn đang lên với gateway đã sẵn sàng nhưng chưa có mẫu. Kết quả rỗng lúc 16:39:50Z **sau** mốc xác nhận vẫn hỗ trợ phần quan sát của báo cáo.

**Đề xuất Minh.** Đổi câu trên thành “Bắt đầu triển khai gateway 16:38:32Z. Đến 16:39:13Z, script đã xác nhận health và Eureka”. Phân biệt cả thời điểm truy vấn 03:21:45Z với mẫu tuổi 9,667 giây mà nó thấy. Chỉ sửa `q4/README.md` và dòng hash của nó trong `q4/SHA256SUMS` nếu được duyệt. Mặt trái là hồ sơ chỉ khoanh được khoảng gateway lên. Tìm chính xác giây đầu sẵn sàng cần kết quả đầu dò có thời điểm, không cần cho Q4. Hai giờ `endsAt` đã đính chính ở REVIEW-5 R3 vẫn đúng.

## Đối chiếu các lượt trước

**REVIEW-5 và phản hồi ngày 28/11.**

| Điểm | Kết luận về phản hồi và sửa | Bằng chứng quyết định |
|---|---|---|
| R1 | Chẩn đoán **đúng**, thực hiện **đúng một phần** | So hai revision bằng cùng nhật ký. Với chỉ `sap_phat` tại −121/−60/0/+60 giây, bản mới trả `chua_xac_minh` trước `get` cho cả bốn. Hai dạng từ chối tag đều dừng. Với `phat`, −60 giây nhận và −121 giây dừng như LOG. Phản ví dụ R1 ở trên còn đi tới chấm. |
| R2 | Chẩn đoán **đúng**, sửa **đúng một phần** | So cùng sáu trạng thái nguồn/đích. Bản mới từ chối nguồn vắng, thiếu cây đồ thị, thiếu chỉ mục nguồn và hai dạng đích dở chỉ có một thành phần. Nguồn đủ trên đích mới đi theo thứ tự đồ thị rồi dữ liệu. Trạng thái dở bên trong cây cuối chưa được phân biệt. |
| R3 | **Đúng, đã sửa** | Từ `webhook.jsonl` trên obs, giải JSON `than`, lọc `alerts[].status=resolved` theo `labels.t072_uid`. Gateway có `endsAt=03:21:40Z`, nhận `03:21:47.790169Z` ngày 25/11. Đầu dò có `endsAt=16:39:40Z`, nhận `16:39:44.590111Z` ngày 24/11. Trừ `q4/k6-state.json#/StartedAt` được 14,75 và 22,54 giây cho gateway. |
| R4 | **Đúng, đã sửa** | WHY-103 và lab `rules.yaml` dùng histogram gateway theo route, cửa sổ 5 phút, điều kiện `increase(count[5m]) >= 30`. `q4/k6-summary.json#/metrics/http_req_duration{expected_response:true}/p(95)` là 535,55 ms toàn lượt phía tải. Hai nguồn trả lời hai câu hỏi khác nhau. |
| R5 | **Đúng** về gói RCA cũ. Hồ sơ phát sinh R3 lượt này | `git branch -r --contains 672391b` có cả hai ref RCA đã ghi. Lỗi mới xuất hiện khi lab được commit sau lần cập nhật dòng STATE. |

**Các lượt 1–4.** Các kết luận sau áp dụng tại revision và phạm vi ban đầu. Phép đối chiếu dùng kế hoạch bản 3.1 §15, mã lab và hiện vật đã kiểm hash.

| Lượt, điểm | Đánh giá và căn cứ |
|---|---|
| 1 R1 | **Đúng.** Script `truoc/buoc0.py` và `sau-buoc-3/sau_app.py` xuất trường chọn lọc và băm giá trị env. |
| 1 R2, R3 | **Đúng** về bộ xuất và UID. Q6 `so-ca-cu.json#/g1` có ba mục giữ nội dung ngoài khối bổ sung. So từ điển `#/dev_sha256` trong `truoc/obs.json` và `sau-buoc-2/obs.json` bằng nhau trên 3.676 khóa. |
| 1 R4, N2 | **Đúng.** `sau-buoc-2/obs.json#/cach_ly` xác nhận tệp tồn tại, user RCA bị từ chối ở cả cha runs và ledger. |
| 1 R5, R6 | **Đúng** về thứ tự phụ thuộc, mount và việc giữ helper. `sau-buoc-3/app.json#/compose_dir` là `/opt/flashticket/compose` và `#/schema_cjs` là directory. Loại mount chưa cho biết ai đã tạo. `tai_linux.preflight` vẫn dùng hai helper. |
| 1 R7, N1 | **Đúng** sau bổ sung đích ghi. `q3-hoi-quy.out` có hai cặp hash đích/chuẩn theo đường cụ thể, dù lệnh glob trước đó lỗi. Bản freeze trước và sau đều có 18 dòng gói, bản Python ghi trong `lenh-3-checkout-venv.out`. |
| 1 R8, N4 | **Đúng.** Giữ UID luật, nguồn bộ sinh và project bộ nhận. Q4 ghi cả firing và resolved của đúng bộ nhận nhẹ. |
| 1 R9 | **Đúng** theo DECISIONS 23/11 Q5 ở thời điểm lập kế hoạch. §7.3 và danh sách xóa sau đó tách vùng giữ khỏi từng mục được duyệt xóa. |
| 1 R10, N3 | R10 **đúng một phần** ở phản hồi ban đầu, số 32 **sai**. `git grep -l -E '/(opt\|srv\|etc)/rca-lab' 4b6c4b2 --` với ba nhánh regex cho 34 file. Hai cờ ở `chuoi_tai.STOP_FILES`. N3 **đúng**, kế hoạch §7.5 giữ dấu vết tên lịch sử. |
| 2 PB1, PB2, S1, S2 | **Đúng.** Bản 3 §9 ghép file phủ với file nền. §7.2 và bước 3 giải quyết ba bind Keycloak, chọn một chiều hoàn tác. Chỉ đánh giá đường triển khai từ hồ sơ đã lưu. |
| 2 PB3, PB4 | **Đúng.** `lenh-4-bat.sh` gọi riêng `t072-bo-nhan`. `q3-hoi-quy.sh` chuẩn bị nơi ghi. `sau-don/k6-so-log.out` ghi `trung=102 khac=0 ngoai_le=4`. |
| 2 PB5, PB6 | **Đúng.** Hai bộ điều khiển lọc `load, rca, inventory`. Q4 có DB cho đơn thật ở `q4/don-db.out` và `kiem-tin-hieu.json#/luong_chinh/mot_ve`. Q6 riêng có `service-graph-60186b05.status.json#/trang_thai=ok`. |
| 2 S3, S4 | S3 **đúng** về phụ thuộc tải gói khi dựng venv. S4 **đúng một phần**, `orchestrator.py:243` bắt buộc người gọi truyền `--ra`. `OUT` giữ hồ sơ lượt. Phản hồi sửa số ở R10 **đúng**. |
| 3 R1, R2 | **Đúng** về tag archive và chặn đường ngoài gốc. `tag_da_dung` đọc archive trước phát. `kiem_dich, kiem_nguon_chep, quet_cay` kiểm cây. Sửa **một phần** cho đường sử dụng xuyên suốt, xem R1/R2 lượt này. |
| 3 R3, R4, R5 | **Đúng** trong phạm vi từng điểm. `inject.py` đối chiếu `compose-dir` với nhãn Payment. `build.sh:17` tách log theo revision, nhãn và giây UTC cho build nối tiếp. README trỏ được tới bộ điều phối sau khi đổi thư mục. |
| 3 R6, R7 | R6 **đúng một phần**. Nhật ký dừng và `deploy.tsv` cho trình tự, webhook cho số bản tin, nhưng gateway và Collector cùng dừng. R7 **đúng** về nhu cầu cập nhật checkpoint, trạng thái mới tại R3. |
| 4 R1, R2 | **Đúng** cho lỗi gốc, sửa **một phần** về nhận dạng. So `c1da15f` với `da9c843` phân biệt nhánh tag rõ với nhánh mất phản hồi. Phần quét cây/đối số G1 đã có trong `c1da15f`. Cây qua kiểm quyền vẫn có thể chép thiếu. |
| 4 R3, R4 | **Đúng.** Bảy truy vấn tuổi mẫu ở đúng giờ trong `q4/README.md` cho 9,479 / 119,479 / 129,479 giây, ba kết quả rỗng, rồi 9,667 giây. STATE hiện ghi đúng R1–R5 lượt 3 chặn từng đường dùng. |

## Điều đã kiểm và tuân thủ quy trình

- **Toàn vẹn.** Dưới `results/T-070/don`, đọc từng dòng `<sha256> *<đường>` của từng `SHA256SUMS` rồi chạy `Get-FileHash -LiteralPath` tương đối với thư mục manifest. Số mục khớp là q4 12, sau-buoc-2 10, sau-buoc-3 15, sau-buoc-4-5 13, sau-don 16, truoc 5, tu-lab 23. Tổng 94/94. Diff RCA `7bd38ee44` chỉ thay dòng README trong manifest Q4. Đệ quy đếm trường `ket_qua` trong `q4/kiem-tin-hieu.json` cho 38 `dat` trên 38 trường. `q4/k6-summary.json#/metrics/{journey_started,journey_finished,http_reqs}/count` lần lượt là 720, 720, 3.317. `q4/canh-bao-nhan.out` có 5 bản tin trước và 9 trong lượt.
- **Diễn giải Q4.** Truy vấn tức thời trên Prometheus obs với chính biểu thức p95 của `rules.yaml` và `sum by(http_route)(increase(http_server_request_duration_seconds_count{service_name="api-gateway",http_route=~"booking|event|payment|ticket"}[5m]))`. Tại 25/11 03:26:20Z và 03:31:20Z, p95 theo thứ tự booking/event/payment/ticket là 0,214/0,100/0,442/0,158 và 0,060/0,048/0,066/0,125 giây. Số request ước tính ở hai cửa sổ lần lượt khoảng 683/695/68/65 và 688/720/72/70. Tất cả p95 đều giảm giữa hai mốc, nhưng riêng ticket còn trên ngưỡng 0,112 s ở mốc sau. Trạng thái luật còn phụ thuộc `for: 60s`. Hai cửa sổ không tách được hiệu ứng JVM khỏi thành phần hành trình hay độ trễ hạ nguồn. Muốn chọn thời gian làm ấm vì JVM cần tín hiệu JVM cùng thời điểm hoặc một cặp tải lạnh/ấm tương đương. Đọc số đã lưu mất vài giây. Cặp chạy mới cần quyền và thời gian tải riêng, chưa cần để nhận Q4. Đề xuất giữ giả thuyết mở và dùng trạng thái luật thực tế trước tiêm như runbook.
- **Phạm vi và mục tiêu nguồn.** Có SPEC của T-071 đến T-075, LICH-MAY có lịch bàn giao và TRANG-THAI ghi không còn khung mở. Tiêu chí 2 của SPEC T-070 chưa đủ cho nghiệm thu toàn task. W8 bị hoãn theo quyết định Minh, W9a chưa có bằng chứng hai lượt diễn tập đạt. Tiêu chí 3 còn lệch checkpoint ở R3. Các mục chờ quyết định đã có ở LOG/kế hoạch. Đợt dọn phục vụ quan sát và hiển thị của DT18. Diff không đổi cách chọn tín hiệu, mốc cảnh báo, đặc trưng, cạnh, tập ứng viên hay thứ hạng. G1 đọc `method-output-1.json` đã tính và kiểm cửa sổ với `su_co.t_hat` trước khi bổ sung trường hiển thị. Không thấy đường đưa tag tải hay nhãn tiêm vào xếp hạng qua hai file sửa. Chưa có phép so có/bỏ cạnh hoặc đối chứng xếp hạng trong Q4, vì vậy kết quả này không trả lời RQ5 hay xác nhận lợi ích đồ thị. WHY-103 giải thích được chọn route gateway và hạn chế gộp API. Các bản sửa vận hành không chọn thêm cơ chế khoa học trước thực nghiệm. Dung sai 120 giây là lựa chọn cài đặt, không đủ làm bằng chứng định danh.
- **Quyền và vân tay.** LOG ghi quyền điền bảng/LOG trước, quyền sửa bốn mục sau, rồi quyền commit riêng. Claude đã ghi rõ việc thấy tóm tắt trước khi tự soát. Diff T-070 trong RCA khớp các file được nêu và nghĩa vụ LOG. Hai file của `da9c843` đúng danh sách lab. Phần lệch nội dung đã duyệt nằm ở R1. `94bb11e` thuộc T-076. T-071 `khai-truoc-e2.json` và `khai-truoc-e4.json` ghim bộ chuỗi lịch sử theo revision/byte. `Chuoi.chay` kiểm commit mở kho. Sửa bộ tải hoặc G1 cần revision lab mới cho lượt mới. Giữ kho và bản khai E2/E4 tại revision gốc. D3 của runbook ghim `94bb11e` hoặc commit Minh chỉ định, cặp DEMO/HOAN-TAC phụ thuộc gốc đó. Đường Q4 và bản chụp phương pháp độc lập với thay đổi đề nghị. A1/A2/D1 vẫn là các đề xuất ở §2 kế hoạch dọn. Đề xuất giữ trạng thái chờ đã ghi cho ba mục ấy, vì việc sửa luật hoặc ghi quyết định không giải quyết hai lỗi cài đặt.
- **Phạm vi máy.** Chỉ đọc obs, kiểm revision, thứ tự thư mục, webhook và một số mốc Prometheus. Phiên này không truy cập app/máy tải. Không chạy tải, M1, tiêm lỗi, dịch vụ, mở tập khóa hay dùng subagent.

### Tái hiện hai phản ví dụ bằng bộ nhớ

Chạy đoạn dưới bằng `python -B` từ repo lab ở `94bb11e`. Các thao tác liên quan tới tải, nhật ký và đích G1 đều có dữ liệu giả. Kết quả quan sát là `xong ['start', 'get', 'get', 'kiem', 'nhan']` và `da_co False`.

```python
import runpy
from pathlib import Path
from unittest.mock import patch

C = runpy.run_path('load/controller/chuoi_tai.py')['Chuoi']
c = object.__new__(C)
c.su_kien = []
def ghi(loai, **v):
    c.su_kien.append(dict(loai=loai, utc='2026-11-25T03:21:25+00:00', **v))
c.ghi = ghi
c.trang_thai = lambda **v: None
c.co_stop = lambda **v: None
calls = []
def tl(cmd, *args, **kw):
    calls.append(cmd)
    if cmd == 'start':
        return dict(ok=False, error='A rca-tai- container is running; nothing stopped or replaced')
    assert cmd == 'get'
    return dict(ok=True, result={'tag':'demo', 'state':{'Running':False, 'ExitCode':0,
                'StartedAt':'2026-11-25T03:21:15Z', 'FinishedAt':'2026-11-25T03:21:26Z'}})
c.tl = tl
c.kiem = lambda tag: calls.append('kiem') or 'dat'
c.nhan = lambda tag: calls.append('nhan') or True
print(c.chay_luot(dict(tag='demo', seconds=600, thu_tu=1)), calls)

init = runpy.run_path('rca/online/g1_b.py')['khoi_tao']
dst = Path('dst')
idx = dst/'du-lieu'/'chi-muc-ban.json'
graph = dst/'service-graph'
missing = dst/'du-lieu'/'V082'/'chi-muc.json'
# Các đường đã xuất hiện trên đích ngay trước khi lần chép đầu bị ngắt.
present = {idx, graph, idx.parent}
with patch.object(Path, 'exists', lambda p: p in present), \
     patch.object(Path, 'is_dir', lambda p: p == graph), \
     patch('shutil.copytree', side_effect=AssertionError('unexpected copy')):
    print(init(dst, '', 'chep:dev', 'V082'), missing.exists())
```

## Báo cáo lượt và đề xuất tiếp tục

1. Đã kiểm độc lập bản sửa, phản hồi R1–R5 và đối chiếu năm lượt trước.
2. Chỉ tạo `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-6.md`. Giữ lịch sử và trạng thái các máy.
3. Manifest, số Q4, bản tin gốc, các nhánh đã sửa và hai phản ví dụ cho kết quả như trên.
4. **Đề xuất Minh tiếp tục phản biện R1 và R2, nhận đính chính REVIEW-5 R3/R4, sửa mốc triển khai ở R4 lượt này và cho cập nhật checkpoint ở lượt có quyền.** Nếu ưu tiên demo lần đầu, đề xuất cho T-076 trình đường có phép so toàn cây đã nêu, giữ chặn riêng lịch tự tiếp nhận và việc dùng `da_co` làm bằng chứng. Cách này giảm chờ sửa bộ tải, đổi lại phải đối chiếu cây thật và vẫn cần Minh duyệt runbook, revision, triển khai. Chưa đề nghị nghiệm thu toàn T-070. Việc cần ghi chính thức sau khi Minh quyết là cách xác minh container và điều kiện dùng lại bộ G1.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-070, tasks/T-070-dieu-phoi-giai-doan-2/.
- Công đoạn: người làm đáp phản biện REVIEW-6.
- Gói/cổng: giai đoạn 2, vận hành ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-070.
- Tài liệu gốc: SPEC.md, LOG.md, TRANG-THAI.json và LICH-MAY.md trong thư mục task, docs/STATE.md, results/T-070/don/KE-HOACH-DON.md, results/T-070/don/q4/ và results/T-076/exp-app/runbook-online.md.
- Phản biện và phản hồi trước: trong thư mục task, lần lượt REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md, REVIEW-6.md và bảng phản hồi tương ứng nếu đã có.
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab, git diff c1da15f da9c843 và git show 94bb11e, results/T-070/don/ và các SHA256SUMS, phép thử bộ nhớ trong LOG và REVIEW-6, python -B từ gốc repo lab.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat cho đến khi Minh cho phép ghi rõ file và phần tương ứng.

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

| Điểm | Ý kiến người làm và mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN phát lịch qua `chuoi_tai` | Chạy lại đoạn tái hiện của Codex trên lab `94bb11e`: `xong ['start', 'get', 'get', 'kiem', 'nhan']`. Nhánh `phat()` khi `start` lỗi mà `get` thấy container cùng tên chỉ so giờ (`LECH_DONG_HO_S`), nên nhận container cũ. **Lỗi quy trình của người làm:** đề xuất 2 Minh duyệt (LOG dòng 526) có "đối chiếu `containerId`"; bản sửa `da9c843` bỏ phần này mà không trình lại (Luật 0 §2.5). Sửa (Minh duyệt cách A 28/11): `tai_linux` thêm `inspect()` trả ID và State trong cùng một lần inspect, lệnh `get` trả thêm `containerId` (giữ `state`); `chuoi_tai.cua_lan_nay` đòi ID trùng `containerId` của bản ghi `phat` cuối; `start` lỗi mà có container → `chua_xac_minh`; nhật ký chỉ có `phat_co_container` → `chua_xac_minh`. | |
| R2 | Đúng; CHẶN dùng `da_co` làm bằng chứng bản chép đủ | Tái hiện của Codex cho `da_co False` trên `94bb11e`. Sửa: `g1_b.khoi_tao` dựng trong `<ra>/.khoi-tao-tam` (cùng hệ tệp), đổi tên `service-graph` rồi `du-lieu`; nhánh `rong` ghi hai chỉ mục trong thư mục tạm rồi đổi tên một lần; còn `.khoi-tao-tam` hoặc có cây nhưng thiếu chỉ mục → dừng. Mâu thuẫn runbook T-076 A2 (so byte hai chỉ mục mọi lần) cũng đúng: sửa A2 tách kiểm lần đầu với kiểm khi dùng lại. Đoạn tái hiện của Codex giả lập trạng thái "có chỉ mục mà thiếu ca"; với bản sửa trạng thái đó không còn sinh ra do ngắt (chỉ mục chỉ xuất hiện qua đổi tên sau khi cây đủ), nên phép thử bản sửa dùng ngắt thật trên thư mục tạm. | |
| R3 | Đúng; KHÔNG CHẶN | Dòng T-070 trong STATE vẫn ghi "chưa commit", "Chờ Minh duyệt commit lab"; `TRANG-THAI.json#/cap_nhat_utc` 26/11. Sửa dòng STATE, `cap_nhat_utc`, `buoc_tiep_dieu_phoi`, thêm `phien_ban/repo_lab_local`. | |
| R4 | Đúng; KHÔNG CHẶN | `sau-buoc-3/deploy.tsv` dòng 13 `START` 16:38:32Z, dòng 14 `END health=yes eureka=yes` 16:39:13Z. Sửa câu ở `q4/README.md` mục 1, thêm dòng đính chính, cập nhật dòng README trong `q4/SHA256SUMS` (12/12 khớp). | |

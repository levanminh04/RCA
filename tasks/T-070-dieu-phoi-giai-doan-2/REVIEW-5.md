# Phản biện T-070, lượt 5

**Người phản biện** Codex. **Người làm** Claude. **Ngày** 28/11/2026. Minh cho ghi riêng bản này. Công đoạn kiểm lại phản hồi và sửa cho đợt dọn vận hành, thuộc P9/P10, ngoài G0–G4.

## Kết luận chung

**Giữ kết quả Q4. Giữ chặn việc phát lịch tự tiếp nhận bằng `chuoi_tai`.** Khi mất phản hồi phát tải, bộ chuỗi còn có thể chấm nhầm lượt trước. Với G1, bản sửa xử lý đúng những đường dẫn bất thường nêu ở lượt 4 trên cây đứng yên. Còn một lỗi độc lập ở chế độ chép bộ cũ: chương trình có thể báo đã khởi tạo dù chưa chép được dữ liệu.

Đối với T-076, bước 9 chạy thẳng `tai_linux.py` nên lỗi bộ chuỗi không chặn bước này. Với bước 10, đề xuất Minh cho dùng đích riêng, một tiến trình ghi, và chỉ chuyển dashboard khi bộ dữ liệu dự kiến đã có thật. Nếu cần giữ ca cũ thì kiểm cả chỉ mục và đồ thị của ca cũ theo runbook. Minh vẫn quyết việc bật trực tuyến và duyệt runbook riêng.

## Nguồn và tự soát độc lập

Đọc luật của hai repo, SPEC T-070, kế hoạch dọn bản 3.1 §3–4, §6–10, hợp đồng, STATE, TRANG-THAI. Đối chiếu diff lab `3ac0d07..c1da15f`, đối chiếu tên, các hunk vận hành và bộ xuất trên toàn đợt từ `truoc-don-2026-11`. Đọc mã gọi thật của bộ chuỗi, bộ tải, bộ điều phối G1, hàm khởi tạo và điểm ghi kết quả. Kiểm hiện vật gốc ở `results/T-070/don/` và quyền thư mục trên obs trước khi đọc kết luận cũ. Sau đó đọc bốn bản phản biện, bảng phản hồi, LOG 26/11 và đối chiếu lại trên máy.

Nguồn mục tiêu là DT18-NV1–NV3, hướng dẫn cô ngày 23/09 và MRP P9/P10. Hạ tầng giữ tín hiệu và hiển thị phục vụ nghiên cứu. Ngưỡng 120 giây là lựa chọn cài đặt của bộ tải. DT18 và cô không đặt ngưỡng đó. Đối chiếu WHY-08, WHY-100, WHY-108–111, DECISIONS 20–24/11 và LESSONS về kiểm trung gian, phạm vi suy luận, đáp phản biện. Lượt sửa không chọn thuật toán, đặt lại tiêu chí Q4 hay đưa nhãn mới vào lõi. Diff toàn đợt giữ nguyên byte của `incidents.py`, `g1_export.py` và `xuat_bo_sung.py` khi đổi đường dẫn. Ở đường online, mã ca sinh độc lập, mốc cửa sổ lấy từ cảnh báo, `g1_b.py` đối chiếu mốc đó với đầu ra lõi trước khi hiển thị.

## Các điểm

### R1. Bộ chuỗi có thể chấm lượt cũ khi tiếp nhận sau gián đoạn — CHẶN lịch dùng bộ chuỗi

Ở lab `load/controller/chuoi_tai.py:144,274,297,329,392`, nhật ký có `sap_phat` nhưng thiếu `tag_da_dung` được tiếp nhận ở bước chờ. Ngay cả khi nhật ký đã ghi `phat_loi` với lý do từ chối tag, quyết định dừng chỉ có hiệu lực sau **lần ghi kế tiếp**. Ở nhánh mất phản hồi, thời gian bắt đầu cũng chỉ có một cận dưới. Một container bắt đầu trước mốc phát 60 giây có thể là lượt trước ngay cả khi hai đồng hồ khớp hoàn toàn.

**Bằng chứng.** Trên obs ở commit đang xét, gọi `Chuoi.chay_luot` bằng `python3 -B`, với nhật ký, `get`, kiểm telemetry và nhận đầu ra thay trong bộ nhớ. Container giả đã thoát mã 0. Thời gian dưới đây là `StartedAt − sap_phat`. Ba số cuối là số lần gọi `get / kiem / nhan`. Không chạy k6.

| Nhật ký hiện có | Chênh giờ | Kết quả thật của bộ chuỗi | Số lần gọi |
|---|---:|---|---|
| Chỉ có `sap_phat` | −121 s | `chua_xac_minh` | 1 / 0 / 0 |
| Chỉ có `sap_phat` | −60 s | `xong` | 1 / 1 / 1 |
| Chỉ có `sap_phat` | 0 s và +60 s, hai ca riêng | `xong` ở từng ca | 1 / 1 / 1 mỗi ca |
| Có thêm `phat_loi` ghi rõ `Tag already used` | −60 s | `xong` | 1 / 1 / 1 |
| Có cả `tag_da_dung` | −60 s | `tag_da_dung` | 0 / 0 / 0 |

Bản sửa đã loại đúng tag bị từ chối ở đường bình thường và ca cũ cách xa. Phép thử của Claude chấp nhận lệch 60 giây cho **đúng** container. Dữ kiện về giờ y hệt cũng có thể thuộc **sai** container. Trường hợp đã có `phat_loi` còn có bằng chứng rõ rằng lần phát này bị từ chối. Đây là lỗi phân loại đã tái hiện trong bộ nhớ. Chưa thấy lượt thật nào bị chấm sai.

**Sửa tối thiểu đề nghị.** Khôi phục quyết định từ chối từ chính bản ghi đã bền vững. Khi còn duy nhất ý định phát, hoặc mất phản hồi trước khi biết lệnh có tạo container hay không, trả `chua_xac_minh` trước bước chấm/nhận nếu không có bằng chứng nhận dạng. `tai_linux.start` đã trả `containerId` khi thành công. Có thể đối chiếu ID ở nhánh đã lưu thành công nếu cần tự tiếp nhận. Với lượt mất phản hồi, dừng cho người vận hành xác minh là thay đổi nhỏ hơn thêm mã lần phát lên hai máy. Mặt trái là một lượt thật có thể phải nhận thủ công. Thu hẹp 120 giây vẫn để hai giải thích cùng đúng. Kiểm bản sửa bằng các ca bộ nhớ trên, mất vài giây.

### R2. Khởi tạo G1 có thể báo đã chép khi nguồn vắng hoặc đích mới chép dở — CHẶN dùng trạng thái khởi tạo để chuyển dashboard sang bộ sao

Ở lab `rca/online/g1_b.py:29,64,82,124`, kiểm đường nguồn cho phép đường con chưa tồn tại. Hàm chép chỉ gọi `copytree` với từng thư mục có thật, sau đó trả `chep`. Chế độ `--chi-khoi-tao` in kết quả đó và kết thúc thành công. Khi chạy lại, chỉ cần đích có `du-lieu/chi-muc-ban.json` là trả `da_co`. Nếu lần trước đã chép chỉ mục nhưng chưa xong `service-graph`, nhánh này cũng bỏ qua phần còn thiếu.

**Bằng chứng.** Gọi trực tiếp `khoi_tao` trên obs với hai tên con đã xác nhận chưa tồn tại dưới gốc kết quả, kiểu `chep:`. Chặn các hàm tạo thư mục, ghi file và chép trong bộ nhớ. Kết quả là `chep`, số lần gọi `copytree` bằng **0**. Trường hợp chép dở kết luận từ thứ tự hai lần chép và điều kiện `da_co`. Không gây gián đoạn hay sửa đích thật. Đối chứng dương: cả `kiem_nguon_chep(dev)` và `kiem_dich(online-dev-001)` qua trên cây thật. Ca Q6 cũ dùng được và không có bằng chứng bộ thật hiện tại mất dữ liệu.

**Hậu quả và sửa tối thiểu.** Nếu dựa vào kết quả CLI để chuyển nguồn, ca cũ có thể biến mất khỏi giao diện hoặc còn chỉ mục nhưng thiếu đồ thị. Đề xuất kiểm nguồn và thành phần bắt buộc trước khi chép, chỉ công nhận đích chép đã hoàn tất sau khi các thành phần cần dùng đã có. Khi đích dở, dừng và giữ lại để xử lý. Nếu chỉ cần bật một lần với nguồn `dev` đã biết, phương án nhẹ là kiểm chỉ mục và mở ca/đồ thị cũ trên đích dự kiến trước khi chuyển. Nếu Minh chọn bộ rỗng, yêu cầu giữ ca cũ trên bộ mới không áp dụng. Không cần phát lại M1 cho phép kiểm này.

**Giới hạn cách ly.** Cây hiện hữu đã qua phép quét chủ sở hữu và liên kết. `namei -l` và `stat` cho thư mục cha `rca/results` là `ubuntu:ubuntu 775`, tài khoản phương pháp `rca` không có quyền ghi tại đó. Phép quét xác nhận ảnh chụp tại thời điểm kiểm. Khóa của bộ điều phối đặt theo thư mục lượt `OUT`. Nếu hai lượt cùng dùng một đích, khóa đó không loại trừ ghi đồng thời. Với một lượt, một đích riêng và không đổi bố trí khi ghi, chưa có bằng chứng cần thay quyền toàn cây hay thêm cơ chế khóa mới. Không dùng kết luận này làm cam kết cách ly với tác nhân đồng thời có quyền sửa thư mục cha.

### R3. Hồ sơ Q4 nhầm giờ hết cảnh báo với giờ nhận thông báo — KHÔNG CHẶN Q4

`results/T-070/don/q4/README.md` mục 1 ghi luật gateway tự hết lúc 03:21:47Z, 22 giây sau khi k6 bắt đầu. Script `canh-bao-nhan.sh` in `nhan_webhook_utc` và `startsAt`. Nó không xuất `endsAt`. Đọc đúng ba trường từ bản tin đã lưu trên obs, lọc trạng thái `resolved` theo `labels.t072_uid`:

| Luật | Grafana ghi `alerts[].endsAt` (UTC) | Bộ nhận ghi `nhan_webhook_utc` (UTC) |
|---|---|---|
| `t072-mat-gw` | 25/11 03:21:40 | 25/11 03:21:47.790169 |
| `t072-mat-do` | 24/11 16:39:40 | 24/11 16:39:44.590111 |

Nguồn là `/srv/flashticket-rca/alerts/bo-nhan/webhook.jsonl`, JSON trong trường `than`. Q4 bắt đầu lúc 03:21:25.254416657Z theo `q4/k6-state.json#/StartedAt`. Khoảng tới hết cảnh báo gateway xấp xỉ **14,75 giây**, tới bộ nhận xấp xỉ **22,54 giây**. Đính chính hai cặp mốc và cập nhật đúng dòng README trong `q4/SHA256SUMS` nếu Minh duyệt. Đây là sai khác có ảnh hưởng khi trích độ trễ phát hiện/khôi phục. Nó không đổi kết quả giao nhận hay ngưỡng tín hiệu.

### R4. p95 của k6 không đủ để quy cảnh báo cho JVM làm ấm — KHÔNG CHẶN Q4

Ở `q4/README.md` mục 2, giả thuyết JVM đã được ghi là chưa kiểm. Điểm còn sai là chỉ dẫn “phân xử được bằng” p95 từng phút ở `k6-summary.json` hoặc `raw.json` so với lượt đã ấm. File summary chỉ có p95 toàn lượt (ví dụ `#/metrics/http_req_duration{expected_response:true}/p(95)`). Kể cả tính từng phút từ mẫu thô phía máy tải, bốn luật đo histogram **ở gateway, theo từng route, trên cửa sổ trượt 5 phút**, có điều kiện đủ 30 request. Nguồn là `observability/grafana/provisioning/alerting/rules.yaml`, các biểu thức bắt đầu ở dòng 31, 86, 141, 196. Phân bố hành trình đầu lượt và thay đổi thời gian xử lý hạ nguồn đều có thể giải thích chênh lệch.

Đề xuất giữ JVM là giả thuyết. Nếu cần định thời gian chờ cho demo, đọc lại chính biểu thức luật và số request theo route trong hai cửa sổ có tải tương đương, ưu tiên dữ liệu đã lưu (vài truy vấn ngắn). Thế đủ để xem cảnh báo đã hạ cho lần quan sát. Muốn quy riêng cho JVM còn cần tín hiệu JVM hoặc đối chiếu lạnh/ấm tương đương về tải và trạng thái phụ thuộc. Q4 không cần kết luận nhân quả này. T-076 C6 đã yêu cầu kiểm trạng thái luật và sự cố đang mở trước khi tiêm.

### R5. STATE còn treo việc đẩy hồ sơ RCA đã hoàn tất — KHÔNG CHẶN vận hành

Dòng T-070 ở `docs/STATE.md` đã sửa đúng mức chặn của hai lượt. Phần “chờ … commit/push repo RCA” gây hiểu nhầm về chính gói sửa này. LOG 26/11 15:10Z ghi Minh đã duyệt và đã đẩy. `git show --stat 672391b` có hồ sơ sửa và `git branch -r --contains 672391b` trả cả `origin/master` lẫn nhánh làm việc trong refs lưu tại máy. Đề xuất ở lần cập nhật dòng T-070 đã được duyệt kế tiếp, ghi rõ gói sửa đã đẩy, nếu còn file mới thì gọi tên đợt mới. Không cần đẩy lại. Bản ghi JSON đã được Minh duyệt cập nhật riêng lúc 14:45Z, đúng commit và đúng prompt.

## Đối chiếu các lượt trước

Đánh giá dưới đây áp vào thời điểm của từng kết luận. Một lỗi được sửa ở lượt sau vẫn là chẩn đoán đúng cho phiên bản cũ.

| Lượt và điểm | Đánh giá phản hồi và bằng chứng đối chiếu |
|---|---|
| 1 R1 | **Đúng.** Script chụp so cấu hình trên máy. JSON trước/sau dùng trường đã chọn và hash. Bản sửa ba file không đụng bộ chụp. |
| 1 R2 | **Đúng.** Diff đổi tên giữ nguyên byte của bộ xuất G1. Loader còn ở `sau_v082`, Q6 có ba kết quả G1 đã so theo khóa. |
| 1 R3 | **Đúng.** UID dashboard được giữ. `truoc/obs.json#/dev_sha256` và `sau-buoc-2/obs.json#/dev_sha256` bằng nhau trên 3.676 file. |
| 1 R4, N2 | **Đúng.** `sau-buoc-2/obs.json#/cach_ly` có kiểm tệp thật trước phép từ chối, kiểm đi qua hai thư mục lượt và sổ tiêm bằng user phương pháp. |
| 1 R5 | **Đúng về dời và thứ tự bật.** Lệnh bước 3, `deploy.tsv`, `app.json#/compose_dir` và `#/schema_cjs` xác nhận proxy, cấu hình hiệu lực và loại bind Mongo. Nguồn gốc lịch sử của thư mục Mongo rỗng không suy ra từ loại hiện thời. |
| 1 R6 | **Đúng.** Helper tiếp tục quản lý đường hầm/mock. Q4 chạy qua preflight ở đường mới. Không có thay đổi helper trong commit sửa. |
| 1 R7, N1 | **Đúng sau bổ sung.** So bản Python/freeze cũ với `lenh-3-checkout-venv.out`. Q3 có hai ca với hai đầu ra từng ca và chuẩn tương ứng. Trong `q3-hoi-quy.out`, glob đầu báo lỗi, các đường cụ thể bên dưới có đủ hash ghép cặp. |
| 1 R8, N4 | **Đúng.** Luật còn nhãn UID, đích nhận và chú thích nguồn. Bản tin gốc cho thấy đúng UID tới receiver. Không suy giờ hết cảnh báo từ giờ giao nhận. |
| 1 R9 | **Đúng về việc giữ theo quyết định ở thời điểm đó.** Kế hoạch §7 và hiện vật bước 4/X1 tách cây tải khỏi danh sách xóa tùy tiện. Việc xóa các mục sau đó có danh sách và quyết định riêng. |
| 1 R10, N3 | **R10 đúng một phần ở phản hồi ban đầu.** Đếm `git grep -l -E '/opt/rca-lab\|/srv/rca-lab\|/etc/rca-lab' 4b6c4b2` bằng regex với ba nhánh OR được 34 file. Hai cờ STOP đã có đường hiện hành trong checkpoint, bản chụp phương pháp thuộc ngoại lệ tên. **N3 đúng**, kế hoạch giữ tag image và nhãn topology. |
| 2 PB1 | **Đúng.** File phủ được ghép cùng file nền qua bước tạo cấu hình hiệu lực. Kết quả cấu hình và triển khai lưu ở `sau-buoc-3/`. |
| 2 PB2 | **Đúng về chiều triển khai.** Lệnh dời và cấu hình sau dời xử lý các bind Keycloak, proxy và thư mục Compose. LOG ghi Minh đã kết thúc việc giữ đường lui cũ. Chưa chạy lại rollback. |
| 2 PB3 | **Đúng.** `lenh-4-bat.sh` gọi service nhận nhẹ, `q3-hoi-quy.sh` chuẩn bị thư mục cha. Đầu ra của cả hai bước có trong bộ đã kiểm hash. |
| 2 PB4 | **Đúng.** `sau-don/k6-so-log.out` kết thúc bằng 102 trùng, 0 khác, 4 ngoại lệ. `docker ps -a --format '{{.Names}}'` trên máy tải còn đủ bốn tên ngoại lệ. |
| 2 PB5 | **Đúng.** Hai bộ điều khiển kiểm nhóm đường `load rca inventory`. Ba checkout có diff rỗng cho file được Git theo dõi. |
| 2 PB6 | **Đúng.** Q4 có kết quả DB của đúng đơn và `#/luong_chinh/mot_ve/ket_qua=dat`. Q6 tách riêng ca dev và có trạng thái đồ thị. Hai phép kiểm khác mục tiêu, khác đường chạy. |
| 2 S3, S4 | **S3 đúng**, bản freeze đã dựng được. **S4 đúng một phần**, đích G1 là đối số bắt buộc `--ra` người gọi truyền. Giá trị mặc định của `OUT` là thư mục nhật ký. |
| 3 R1 | **Đúng ở bộ tải, sửa một phần ở bộ chuỗi.** `tai_linux.tag_da_dung` xét cây hiện hành, archive và container trước bước đăng nhập. R1 của lượt này còn ở nhánh tiếp nhận. |
| 3 R2 | **Đúng về đường chuẩn và phép quét.** Nguồn, đích có giới hạn gốc, đường nguồn đã chuẩn hóa và được truyền nguyên đối số. Tính đầy đủ của bản chép là R2 lượt này. |
| 3 R3 | **Đúng.** `inject.py` kiểm `compose-dir` và nhãn cấu hình trước khi tái tạo Payment. Bản sửa mới không đổi injector. Không tiêm lại để kiểm. |
| 3 R4 | **Đúng với build nối tiếp.** `build.sh:17` đặt log theo revision, nhãn và giây UTC. Chưa có căn cứ dùng cho build cùng nhãn đồng thời. |
| 3 R5 | **Đúng.** README quay về gốc repo và chỉ tới file điều phối có thật. Bản sửa xử lý lỗi đường dẫn đã nêu. |
| 3 R6 | **Đúng một phần.** Lịch dừng và số thông báo đúng, quy riêng nguyên nhân cho gateway đã được rút. Mốc hết và mốc nhận vẫn khác như R3. |
| 3 R7 | **Đúng về checkpoint sau khi cập nhật.** Dòng STATE còn một việc đã xong như R5. |
| 4 R1 | **Đúng một phần.** Nhánh có bản ghi từ chối cuối cùng đã dừng bền vững. Hai trạng thái tiếp nhận chưa đủ bằng chứng nhận dạng, xem bảng R1. |
| 4 R2 | **Đúng về lỗi ban đầu và bản sửa trên cây tĩnh.** Hai bộ thật qua kiểm, số đếm ở dưới. Đây không phải bằng chứng `chep:` tạo ra bộ dùng được, cũng không phải phép chạy webhook → G1. |
| 4 R3 | **Đúng về cơ chế tuổi mẫu.** Bảy truy vấn độc lập khớp. Hai thành phần dừng cùng đợt nên không tách nguyên nhân. Bản đính chính còn nhầm trường thời gian ở R3. |
| 4 R4 | **Đúng về mức chặn và revision.** STATE phân loại đúng, JSON đã được phép cập nhật sau lượt sửa. R5 phát sinh khi commit đã đẩy sau đó. |

## Kiểm chứng, phạm vi và quyết định

- **Tính toàn vẹn.** Tính SHA-256 trên byte của từng mục trong bảy `SHA256SUMS` dưới `results/T-070/don/*/`. Số mục đúng theo thứ tự `q4, sau-buoc-2, sau-buoc-3, sau-buoc-4-5, sau-don, truoc, tu-lab` là **12, 10, 15, 13, 16, 5, 23**. Tổng 94/94. Hai ánh xạ `#/snapshot_sha256` trước/sau bằng nhau trên 149 file. Q6 ở `sau-buoc-4-5/q6/so-ca-cu.json` có `#/trung_tat_ca=true`, hai đầu ra V082 khớp, ba mục G1 khớp ngoài khối thêm, file trạng thái đồ thị ghi `ok`. Đây là ca dev ở revision cũ.
- **Tải và tín hiệu.** Q4 gọi trực tiếp bộ tải. `k6-summary.json#/metrics/journey_started/count` và `journey_finished/count` cùng 720. `http_reqs/count=3317`, `http_req_failed/value=0`. Duyệt đệ quy các trường chuỗi tên `ket_qua` trong `kiem-tin-hieu.json` được 38 giá trị `dat`. Số lượng, vé và phát hành cùng bằng 1 ở `#/luong_chinh/db`, khớp `don-db.out`. Tất cả 14 dòng `canh-bao-nhan.out` chia thành 5 trước và 9 trong Q4 theo giờ nhận. Đếm thông báo không ước lượng tỷ lệ báo động giả.
- **Cơ chế mất mẫu.** Truy vấn tức thời trên Prometheus của obs bằng biểu thức `time() - max(timestamp(http_server_request_duration_seconds_count{service_name="api-gateway",http_route=~"booking|event|payment|ticket"}))`. Ngày 24/11 ở 16:29:40, 16:31:50, 16:32:00, 16:38:40, 16:39:50 UTC lần lượt ra 9,479 s, 119,479 s, 129,479 s, rỗng, rỗng. Ngày 25/11 ở 03:21:20, 03:21:45 UTC ra rỗng và 9,667 s. Quy tắc dùng ngưỡng 60 s, giữ 60 s, đánh giá mỗi 10 s và cho phép báo khi không dữ liệu. Các điểm rỗng không đếm request suốt đêm. Nếu cần tách thiếu lưu lượng khỏi mất đường đo thì đối chiếu log truy cập theo route và tình trạng Collector ở cùng cửa sổ. Không có nhu cầu đó để công nhận Q4.
- **Ba máy.** Đọc qua wrapper SSH Minh chỉ định. `git rev-parse --short HEAD` ra `c1da15f` tại `/opt/flashticket-rca` trên app, obs, tải. `git diff --quiet HEAD` thành công trên cả ba. `docker ps` trên obs có bộ nhận nhẹ, không có bộ nhận online. Đếm bằng `lstat` trên gốc và các mục con của `dev` (4.025 mục), `online-dev-001` (62 mục) cho 0 mục khác chủ root, 0 symlink, 0 file thường có nhiều hard link ở mỗi bộ. Không khởi động dịch vụ. Không dùng kết quả giả lập làm kết quả chạy thật.
- **Quyền và tiêu chí.** SPEC gốc giao điều phối và hạn chế chạy máy. Kế hoạch dọn cùng các lượt duyệt riêng sau đó cho phép các thao tác cụ thể. LOG 26/11 ghi duyệt bốn sửa, tiếp đó duyệt JSON riêng rồi duyệt commit/push. Diff lab đúng ba file. Việc ghi bảng của Claude, LOG, đính chính Q4 và dòng STATE có căn cứ. LOG nói rõ giới hạn tự soát khi Minh đã gửi kèm tóm tắt. Đếm 15/15 và 22/22 là số Claude ghi trong LOG; lượt này kiểm độc lập các nhánh quyết định ở trên, không nhận đã tái lập nguyên hai bộ đó. SPEC T-070 còn tiêu chí W8/W9a và bàn giao. Điều phối đã dừng theo Minh, W9a chưa có hai lượt diễn tập đạt. Đợt dọn cung cấp bằng chứng về bảo toàn đầu vào, lõi và hiển thị, chưa đo chất lượng xếp hạng hay lợi ích của cạnh đồ thị.
- **Ảnh hưởng nếu sửa.** Hai script lab dùng revision Git làm vân tay. Bộ chuỗi so commit với commit mở kho, nên nếu đổi mã phải giữ kho và revision lịch sử, không tiếp nhận kho cũ dưới commit mới như cùng một lượt. `rca/method.lock` ghim bản chụp phương pháp. Sửa bộ chuỗi hay khởi tạo G1 không đòi tái tính kết quả khoa học cũ. Nếu đổi revision dùng cho runbook T-076 thì phải trình lại phần ghim bị ảnh hưởng. README Q4 có mục trong chính `q4/SHA256SUMS`. Đề xuất sửa số giờ kèm dòng hash đó, giữ nguyên dữ liệu máy và đầu ra gốc. Bản review mới là tài liệu duy nhất được phép ghi.

## Báo cáo lượt và đề xuất

1. Đã kiểm lại phản hồi và bản sửa bằng code, hiện vật đã kiểm hash, phép thử bộ nhớ và dữ liệu máy chỉ đọc.
2. Chỉ tạo `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-5.md`. Không commit, không sửa LOG/STATE, không mở dữ liệu khóa, không phát tải và không gửi prompt.
3. Ba checkout đúng revision. Q4 đạt các tiêu chí tín hiệu đã khai. R1 và R2 có phản ví dụ độc lập. Dữ liệu webhook phân xử được mốc kết thúc ở R3.
4. **Đề xuất tiếp tục phản biện hẹp R1 và tính đầy đủ của bản chép ở R2.** Minh có thể chọn dừng ở giới hạn đã nêu nếu chưa cần dùng hai đường đó. Để dùng ngay đích riêng, phương án ít việc nhất là giữ bộ chuỗi tự tiếp nhận ở trạng thái dừng và yêu cầu runbook kiểm chính bộ hiển thị định chuyển sang. Để dùng tự động nhiều lượt, đề xuất sửa R1 và R2 theo phạm vi trên. R3–R5 có thể đính chính cùng lần cập nhật tài liệu kế tiếp. Đề xuất giữ A1/A2/D1 cho quyết định riêng đã trình ở §2 kế hoạch dọn, vì sửa luật lưu trữ hoặc ghi quyết định không phân xử lỗi vận hành này. Không có đề nghị chạy lại Q4, Q6 hay mở W7.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-070, tasks/T-070-dieu-phoi-giai-doan-2/.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giai đoạn 2, vận hành, ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-070.
- Tài liệu gốc: tasks/T-070-dieu-phoi-giai-doan-2/SPEC.md, LOG.md, TRANG-THAI.json, docs/STATE.md, results/T-070/don/KE-HOACH-DON.md và q4/ trong cùng thư mục; repo lab D:/Project/flashticket-rca-lab, git diff 3ac0d07 c1da15f và git diff -M truoc-don-2026-11 c1da15f.
- Phản biện và phản hồi trước: tasks/T-070-dieu-phoi-giai-doan-2/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md theo thứ tự.
- Code và kết quả liên quan: repo lab tại c1da15f, results/T-070/don/ và các SHA256SUMS của từng nhóm; đọc hồ sơ và kết quả theo AGENTS.md.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cấp quyền cụ thể riêng cho lượt đáp.

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
| R1 | Đúng; CHẶN lịch dùng `chuoi_tai` tự tiếp nhận; không chặn T-076 bước 9 | Đọc `load/controller/chuoi_tai.py` @`c1da15f`: `buoc_tag` (143–157) chỉ ra `tag_da_dung` khi có bản ghi `tag_da_dung`; nhật ký có `phat_loi` "Tag already used" mà chết trước dòng 277 vẫn ra `can_cho`. Tiếp nhận ở `can_cho` dùng `cho_xong`/`cua_lan_nay` (300–311) với dung sai `LECH_DONG_HO_S=120`, nên nhận container bắt đầu sớm tới 120 s. Điều kiện xảy ra: dùng lại tag cũ và tiến trình chết giữa `sap_phat` và bản ghi kết quả start. Không tự chạy lại phép thử bộ nhớ của reviewer; logic mã khớp bảng R1. Sửa: `phat_loi` "Tag already used" → `tag_da_dung`; chỉ có `sap_phat` mà không có `phat` → `chua_xac_minh` trước chấm/nhận; có `phat` thì đối chiếu `containerId` đã lưu. Mặt trái: lượt thật mất phản hồi phải nhận thủ công. | |
| R2 | Đúng; CHẶN dùng kết quả `--chi-khoi-tao` để chuyển dashboard (ảnh hưởng T-076 bước 10) | `rca/online/g1_b.py` `khoi_tao` (82–91 theo tệp): `kiem_nguon_chep` → `quet_cay` trả về khi nguồn không tồn tại; vòng chép bỏ qua thư mục con vắng rồi vẫn trả `chep`; `da_co` chỉ dựa vào `du-lieu/chi-muc-ban.json`, mà `du-lieu` được chép trước `service-graph`. Sửa: đòi nguồn có `du-lieu/chi-muc-ban.json` và `service-graph/` trước khi chép; chép `service-graph` trước, `du-lieu` sau cùng (chỉ mục là dấu hoàn tất); đích có một phần thì dừng. Runbook bước 10 vẫn kiểm mở ca/đồ thị cũ trên đích trước khi chuyển. | |
| R3 | Đúng; KHÔNG CHẶN Q4 | Đọc lại `/srv/flashticket-rca/alerts/bo-nhan/webhook.jsonl` trên obs (chỉ đọc, 28/11): `t072-mat-gw` resolved `endsAt` 2026-11-25T03:21:40Z, nhận 03:21:47.790169Z; `t072-mat-do` `endsAt` 16:39:40Z, nhận 16:39:44.590111Z. `q4/README.md` dòng 29, 33 ghi 03:21:47Z là giờ hết. Sửa hai dòng (hết 03:21:40Z, ~14,75 s sau StartedAt; nhận 03:21:47,79Z) và dòng README trong `q4/SHA256SUMS`. | |
| R4 | Đúng; KHÔNG CHẶN Q4 | `q4/README.md` dòng 41 nói phân xử bằng p95 từng phút trong `k6-summary.json`/`raw.json`; summary chỉ có p95 toàn lượt, còn luật đo histogram gateway theo route trên cửa sổ 5 phút. Sửa câu "Phân xử được bằng": đọc lại biểu thức luật và số request theo route ở hai cửa sổ tải tương đương; quy riêng cho JVM cần tín hiệu JVM hoặc đối chứng lạnh/ấm. Giữ JVM là giả thuyết chưa kiểm. | |
| R5 | Đúng; KHÔNG CHẶN | Dòng T-070 ở `docs/STATE.md` còn "Chờ: Codex kiểm lại (`prompt-codex-6.md`) … commit/push repo RCA". Đã xong: `672391b` (26/11), `b04af7b` (27/11) trên master; REVIEW-5 có ngày 28/11. Sửa dòng STATE khi Minh duyệt. | |

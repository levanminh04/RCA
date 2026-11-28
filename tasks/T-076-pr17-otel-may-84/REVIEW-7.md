# Phản biện T-076 — runbook demo bản 2 và mở rộng máy 84

- **Người phản biện** Codex. **Người làm** Claude. **Ngày** 28/11/2026.
- **Công đoạn** Soát kết quả, P9/P10, ngoài G0–G4. Lượt chính thức đầu tiên cho hai đầu ra. Minh dành REVIEW-7 cho lượt này. REVIEW-6 và lượt kiểm bản sửa PR có phạm vi riêng.
- **Đầu ra đã đọc** `results/T-076/exp-app/runbook-online.md` (gọi tắt là runbook) và `results/T-076/mo-rong-may-84.md` (mở rộng), theo cây RCA `d31ad6943`. Hai file trong cây làm việc khớp HEAD. Code lab đọc bằng `git show/grep` ở `94bb11e`, FlashTicket ở `f40b849` như Minh giao. Chỉ so chênh về sau để định vị tuổi của số liệu. STATE và mục cuối LOG đã ghi PR lên `cd21f17`.
- **Tự soát độc lập** Đọc AGENTS, STATE, SPEC 6, hai đầu ra, DT18, hướng dẫn của cô, MRP P9/P10, B16 §3/§6, WHY-109/110/111, DECISIONS giai đoạn 2 và LESSONS QT8/12/15–19. Kiểm manifest, đọc khai trước E5, tuyến thực thi và hồ sơ đã lưu trước khi mở kết luận các bản REVIEW và mục F1–F8 trong LOG. Bằng chứng quyết định gồm mã đọc spool/ghi G1, mốc E5, biểu thức luật, code tải, bộ tiêm, sổ ghi, file provisioning, dashboard, manifest workload và script CD. Không dùng chat của phiên Claude làm nguồn đo.

## Kết luận chung

**Đề xuất chưa duyệt runbook bản 2 để phát bước 10.** Có thể giữ một bộ dashboard ổn định và hai bản cấu hình bật/gỡ để Minh dùng lại. Cần sửa cách tách lượt, xác nhận tải và tín hiệu trước tiêm, xác định mốc chấm và mô tả đường quay lại. Đây là lỗi của hướng dẫn và điều kiện suy luận. Chưa có lượt demo T-076 nào để kết luận trượt.

**Tiêu chí 5 đạt một phần.** Hồ sơ mở rộng có bảng việc, số RAM và các điều kiện còn mở. Chỗ nói chỉ cần Collector lọc phần còn lại mâu thuẫn với điều kiện B16 ngay trong tài liệu. Bảng cũng chưa chỉ đúng file phải sửa khi chuyển môi trường, đường tin cậy TLS và căn cứ để quyết dung lượng. Các điểm này chặn dùng hồ sơ làm hướng dẫn bật máy 84, riêng chúng không chặn phần demo trên Oracle.

## Các điểm

### R1. B9 có thể cho tiêm khi nền chưa đủ điều kiện C6 — CHẶN bước B10

**Ở đâu.** Runbook 63–82, 95, 114–116. D7 mới xác định tên container. B8 lấy giờ bắt đầu. B9 dùng trạng thái luật và danh sách sự cố, B14 mới đọc trạng thái kết thúc của k6.

**Bằng chứng.** Lab `load/controller/tai_linux.py` trả `get → result.state` kể cả khi container đã thoát. `observability/grafana/provisioning/alerting/rules.yaml` có 11 UID luật, 9 dòng `noDataState: OK`. Luật p95 còn yêu cầu số request đủ trong cửa sổ. Một route không có tải vẫn có thể hiện bình thường. Hai luật mất mẫu kiểm tín hiệu tổng hợp, không chứng minh hành trình Payment đang chạy. E5 đã có phép kiểm K6 ngay trước tiêm trong `e5/e5_luot.sh`. File `e5/luot/k6-sau-tai.txt`, hai phản hồi `/data/result/0/value/1`, lần lượt là 139,322 request tăng ước tính trên route Payment và tuổi mẫu đầu dò 7,292 s. Đây là ví dụ một lượt hợp lệ. E5 còn kiểm sạch trước chu kỳ.

**Độ mới của trạng thái.** `rca/online/orchestrator.py:216–228` đọc spool rồi gọi xử lý từng ca đồng bộ. Khi đang xử lý ca nền, thông báo mới có thể đã đến spool nhưng chưa vào `su-co/*.json`. B9 in cùng một danh sách rỗng khi thực sự không có ca hệ thống và khi glob nhầm thư mục. A7 chỉ xác nhận bộ đọc ở thời điểm tin Test. Vì thế điều kiện 300 s đúng cho các khoảng đã đọc, chưa đủ chứng minh đây là toàn bộ các khoảng cần xét. Trạng thái `dang_chay` cũng có thể làm ca mới phải xếp hàng trước hạn N.

**Sửa tối thiểu.** Ngay tại B9 dùng `get` của đúng tag, kiểm tải còn chạy và lấy lại hai tín hiệu K6 của E5 trên bản demo. Kiểm tình trạng can thiệp tồn dư trước chu kỳ bằng cách đã duyệt, lưu ý `inject.py verify` có thể gỡ pause đã quá hạn. Đối chiếu con trỏ `spool-da-doc.json` với phần dòng hoàn chỉnh đã tới và nhận diện được tin Test trong đúng OUT. Nếu còn tồn đọng thì đợi trong hạn nền. Dùng trạng thái luật cùng `t_het` trong file sự cố sau đó. Lưu `ExitCode/OOMKilled` và bằng chứng hành trình của lượt khi nhận tải. Mất tải, mất dữ liệu hoặc bộ đọc ngừng cần được ghi đúng là lỗi điều kiện chạy. Chưa đủ căn cứ chấm “bỏ sót”.

**Sai số trong ví dụ Q4.** `q4/canh-bao-nhan.sh` chỉ in giờ nhận, UID, trạng thái và `startsAt`. Dòng 14 của `canh-bao-nhan.out` là giờ **nhận** 03:29:28Z. Trừ `k6-state.json#/StartedAt` được 482,746 s. Không có `endsAt` trong file đó. `incidents.py::_ket_thuc` lấy phần nguyên của chính `endsAt`. Nên giữ 483 s làm minh họa giờ nhận, bỏ khẳng định giây 783 là biên ghép đo được. Tính biên từ `endsAt` của lượt mới không tốn thêm lần chạy. Chỉ cần bản tin gốc Q4 nếu muốn công bố con số lịch sử chính xác. Bốn luật p95 đã báo thật, nguyên nhân JVM làm ấm vẫn là giả thuyết.

### R2. B10–B13 chưa khóa rõ mốc tiêm thành công và mốc mở ca — CHẶN chấm đạt, bỏ sót hoặc quá N

**Bằng chứng.** B10 gọi bản ghi `mark` trước thao tác là “mốc”, rồi B13 dùng “mốc tiêm”. Trong E5, bảng đính chính `results/T-073/dap-cx21/dinh-chinh-e5-1.md` §1 và bản chấm sổ của T-070 lúc 02:40Z phân biệt `mark` 02:17:31,841Z với `fault-start.inj.t` 02:17:34,233Z. File sự cố `e5/su-co/bbc0a6d44f.json#/t_hat` cho 02:18:30Z. Độ trễ đã chấm là 55,767 s. Một cảnh báo ở giữa hai mốc sẽ đổi kết luận nếu lấy nhầm mốc. `ledger_append.py` bổ sung số thứ tự và hash dòng trước, không tự gán giờ hay chứng minh lệnh thành công. `inject.py::start` in trường `t` sau khi thao tác và lập hẹn giờ. Hẹn gỡ tự động dùng `seconds + 5` (dòng 149), còn `verify` có thể tự gỡ can thiệp đã quá hạn. “Sạch sau verify” tự nó chưa đo được thời lượng pause thực.

**Hậu quả và sửa.** Ghi rõ người chấm sau lượt lấy `inj.t` của bản ghi `fault-start` đúng tag/ô và có kết quả thành công, dùng UTC cùng gốc với cảnh báo, giữ phần lẻ khi so biên. `mark`, giờ nhận webhook và giờ gỡ/verify dùng để giải thích độ trễ. Lệnh tiêm lỗi sau khi đã pause một phần, ghi sổ hỏng hoặc không xác nhận được tải thì giữ bằng chứng, khôi phục đúng can thiệp và báo “lỗi thao tác/chưa chấm được”. Đừng để §5 tự chuyển trường hợp đó thành “bỏ sót”. Giữ cửa sổ danh nghĩa 600 s đã khai, ghi thời gian thực riêng. Không đưa sổ vào đầu vào RCA.

B12 hiện yêu cầu giờ thấy mã trong **danh sách** rồi mới mở trang. SPEC C6 yêu cầu mở được **đúng ca có đồ thị con và hạng** trong 25 phút. Nếu thấy danh sách lúc 24:59 nhưng mở được lúc 25:05, giờ danh sách chưa chứng minh C6. Ghi cả hai giờ, đối chiếu mã sự cố → `ma_ca_m1` → `che_do_b.su_co`, ảnh panel của ca và hai cờ của đúng lượt. Khi bộ xử lý có lỗi, theo `khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang/loi_xu_ly` phân biệt lỗi P7 đã nhận diện với lỗi khác. Khi N hết mà hàng đợi chưa xử lý, giữ trạng thái “quá N” và giờ xuất hiện muộn nếu có. Đây không phải phép kiểm chất lượng xếp hạng.

### R3. Lượt sau dùng lại cả trạng thái điều khiển hoặc bị chặn vì G1 có thêm ca — CHẶN diễn tập lại và tiếp nhận

**Ở đâu.** §2, §3 dòng 48, A2/A3/A6/A7, C1/C5, nhánh giữ cấu hình và §5. Đổi tag tải chưa đổi `runs/<ngày>-online-demo` trong cùng ngày. C1 để lại `OUT/STOP`. `orchestrator.py:93,216–228,262` kiểm STOP, lấy lock theo OUT, đọc lại offset spool. `incidents.BoGom.__init__` nạp ca cũ. `webhook_receiver.seq_bat_dau` tiếp số thứ tự từ spool cũ. Hệ quả cụ thể là A7 vẫn có thể thấy dấu vết Test nhưng STOP của lượt trước ngăn xử lý ca mới. Với nhánh giữ cấu hình, bộ nhận còn ghi khi bộ điều phối dừng.

Ở cấp hiển thị, `g1_b.py` trả `da_co` cho bộ đã tồn tại và cuối hàm chính thêm ID vào cả `chi-muc.json` lẫn `chi-muc-ban.json`. Sau một ca thành công, nếu dev đứng yên thì bộ demo có thêm một ca. A6 đòi số ca bằng dev sẽ loại chính trạng thái hợp lệ đó. A2 còn khẳng định mọi đích chép dở sẽ bị từ chối. `khoi_tao:85–101` chỉ đòi có chỉ mục và thư mục đồ thị ở nhánh đã có. Trong lần chép đầu, `copytree(du-lieu)` có thể tạo chỉ mục trước khi chép xong các file ca khác. Có chỉ mục và mở được một ca cũ chưa chứng minh bản chép đủ.

**Sửa tối thiểu, thuận tiện cho Minh.** Giữ tên bộ **hiển thị** cố định để dùng lại hai commit. Cho **mỗi lần phát** một ID mới dùng chung cho OUT, spool, env, tag và bản ghi sổ. Lượt bị ngắt giữ nguyên. Gắn bộ nhận đúng spool mới khi mở lại. Đo trước tập ID hiện có của bộ demo theo bản phương pháp, kiểm các ID cũ còn và mã mới thuộc đúng lượt. Chỉ yêu cầu bản chép khởi tạo bằng dev lần đầu. Nếu phục hồi lần chép dở, so danh sách đường dẫn/hash của phần phải chép với dev trước khi dùng `da_co`, giữ bản dở khi lệch. Các lượt sau khỏi chép lại dữ liệu đã kiểm. Một tiến trình ghi cho bộ demo vẫn cần vì khóa theo OUT. Nếu Minh muốn từng G1 biệt lập thì tên bộ riêng cũng hợp lệ, đổi lại phải chuyển nguồn dashboard theo lượt.

**Khi cần phát lại mà Grafana hoặc obs hỏng.** §5 nói “phát lại offline ca E5” nhưng chưa nêu thứ Minh thực sự mở được. Sau dọn, bộ E5 đầy đủ ở archive của obs, ngoài mount Grafana hiện tại (`docs/ARCHIVE-INDEX.md`, dòng exp-obs `rca-results/`; manifest `don/sau-don/SHA256SUMS` khớp 16/16). Với bản ca E5 đã chép về laptop, `Test-Path` cho file `du-lieu/V082-V066+H8a/phat-lai/7577dd5b.json` là true, cho cả `du-lieu/chi-muc-ban.json` và chỉ mục của bản V082 là false. Không được hứa chỉ mở dashboard dev là thấy E5. Để quay sang minh họa ngay, ghi rõ hai ảnh `e5/s49-anh-ca-moi-trong-danh-sach.jpg`, `e5/s49-anh-mo-ca-7577dd5b.jpg` và file ca đã kiểm hash; gọi đúng là xem lại bằng chứng đã lưu. Nếu Minh cần thao tác Grafana tương tác khi tuyến sống hỏng, người làm phải chỉ rõ nguồn đã phục vụ và đường mở được theo quyền. Hai ảnh không chứng minh một buổi phát lại tương tác hay một lần demo mới.

### R4. Dự toán đang trộn thời điểm thấy ca với thời điểm hoàn tất — CHẶN duyệt thời lượng

Theo §2, §3, B9, B12, C và giả định của chính bản nháp, tính bằng giây: `900 chuẩn bị + giây tiêm + trễ phát hiện + 1500 chờ N + 600 hoàn tác`. Với tiêm ở giây 600 và độ trễ ví dụ 56 s, được **50 phút 56 giây tới hạn N, 60 phút 56 giây gồm hoàn tác**. Với tiêm ở giây 900 và t̂ sát cuối cửa sổ, tương ứng gần **65 và 75 phút**. Ngay cả tiêm ở giây 600, t̂ sát cuối cửa sổ cũng cho gần 70 phút gồm hoàn tác. Đây là dự toán theo giả định, chưa gồm phần nhận đầu ra còn kéo dài hay chờ ca đang xử lý. Profile `load/profiles/purchase-journey.json#/gracefulStop` cho phép thêm 90 s. 2.100 s vẫn là thời lượng tải danh nghĩa hợp lý cho cửa sổ lấy dữ liệu.

**Sửa tối thiểu.** Trình Minh một khung thời gian thống nhất, gồm chuẩn bị, tải, quan sát tới N, nhận và phục hồi. Đề xuất cho phép dự trù khoảng 75 phút cộng phần chờ thực tế nêu rõ, một lần tiêm. Nếu một giờ là giới hạn cứng thì tách việc chuẩn bị/hoàn tác được Minh duyệt riêng hoặc dời lượt. Không rút ngắn N hay tiêm khi nền chưa sạch để vừa giờ. §5 đã có nhánh xử lý theo pha. Bổ sung ngay trong bảng đó: lỗi đầu lượt chỉ làm lại A chưa đạt (~15 phút), lỗi giữa lượt trước tiêm giữ dữ liệu (~một lượt mới nếu cần), lỗi cuối lượt dùng lại ca/spool/ảnh để phân biệt chậm UI với lỗi xử lý, dự trù phần hoàn tác (~10 phút). Chỉ trình lặp khi khớp điều kiện hạ tầng đã khai trước. Chi phí thực của ca đang xử lý chưa đo trên bản mới.

### R5. Hai cách đổi Grafana chưa có hai đường quay lại tương ứng — CHẶN chọn nhánh API và phê duyệt toàn bộ §3

**Bằng chứng.** Runbook 42–55, A4/A5 và C2–C6. Nhánh API nói “giữ nguyên các bước khác”, trong khi A4 vẫn checkout DEMO chứa integration theo file, C2 checkout HOAN-TAC có chỉ thị xóa cùng UID. Như vậy hai nơi cùng quản lý một đích, hoặc phải dùng commit không tồn tại của nhánh đã bỏ. Cả A5 và việc so SHA của file T-072 trong một khoảng có thể có cảnh báo thật chỉ kiểm được tin Test trong cấu hình đang hoạt động. Một hash thay đổi vì tin thật không chứng minh Test gửi nhầm. Test dương của T-073 cũng không chứng minh gỡ/đổi ngược thành công hoặc T-072 vẫn nhận tin.

SPEC phần ghi bước 10 còn yêu cầu trạng thái contact point trước/sau và bản sao dashboard hiện hành. “Cây git sạch” chỉ nói về file. Nó không xác định trạng thái integration của Grafana hay đích dashboard đang phục vụ trước khi tiếp quản. Ví dụ E5 có riêng phép đọc lại sau gỡ trong `e5/hoan-tac/s5-4-kiem-sau-restart.txt`. Hai digest Grafana ở `ecdeed2` và `94bb11e` trùng trong `observability/compose.yaml`. Điều đó hỗ trợ tái sử dụng cách làm, chưa xác nhận trạng thái trên obs hiện tại.

**Sửa tối thiểu.** Chỉ phát một nhánh hoàn chỉnh đã chọn. Ưu tiên file, có SHA nguồn ban đầu và hai diff thuận/nghịch chỉ thay các file đã duyệt. Lưu bằng chứng trước/sau trên các trường vận hành và bản dashboard mà SPEC yêu cầu, tránh lưu thông tin xác thực. Nếu trước A khác trạng thái dev/T-072 dự kiến, trình Minh trước khi thay. Phân biệt “trở về cấu hình dev” với “đã trở về đúng checkout ban đầu”. Sau khi chỉ thị gỡ có hiệu lực mới cân nhắc trở về nhánh gốc ở đúng revision đã kiểm. API chỉ thành phương án dùng được khi có bước thêm/gỡ UID và đổi nguồn dashboard tương ứng, không nạp file quản lý cùng integration. Tận dụng nút Test của từng integration như E5 và đối chiếu các dòng mới đúng loại/giờ thay vì suy từ hash toàn file khi có tin thật. Lỗi trước A4 chỉ đảo các bước đã làm.

### R6. Danh sách mở rộng thiếu đường tin cậy và các file hiện hữu phải sửa — CHẶN dùng tiêu chí 5 làm kế hoạch chuyển máy

**Ở đâu.** Mở rộng 16–25, 55–66. Hai dòng sửa công tắc/RAM ghi hết vào `deployment.yaml`. `git ls-tree f40b849:deploy/k8s/discovery-server` chỉ có ConfigMap, hai Service và **StatefulSet**. Khi chọn bật Discovery, phải đổi công tắc/nguồn lực ở StatefulSet. Bộ kiểm tín hiệu dùng chung `tests/signals/check_purchase_journey.py:107–119,179–181` hiện truy vấn Tempo theo service/route mà thiếu môi trường. Chỉ thêm datasource hay dashboard mới chưa làm Q4 đọc riêng `exp` khi hai nguồn cùng ghi Tempo. `datasources.yaml` hiện gắn `serviceMap` với `prometheus`; datasource chạy thật cần gắn đúng nguồn production. `_deploy-service.yml` và `deploy-k8s-service.sh:9–10,271` còn kiểm kiểu build/đích registry/digest và Eureka. Chỉ thêm tên Collector không đủ cho image upstream dựng sẵn.

**Chuyển máy.** `git ls-tree -r 94bb11e -- observability/tls` rỗng. `git status --short -- observability/tls` tại laptop trả `?? observability/tls/`; thấy tên script và CA công khai ở cây làm việc. Do đó clone revision này chưa mang theo CA. Việc chứng chỉ đã tạo trên obs là ghi nhận lịch sử, chưa chứng minh Collector mới biết CA nào xác thực đúng tên máy nhận. Đề xuất dùng lại CA công khai có nguồn xác minh, khai mount/trust và đối chiếu tên kết nối với SAN, trỏ exporter đúng Secret token. Khóa riêng chỉ ở nơi cấp/nhận có thẩm quyền. Ghi đường phân phối CA công khai hoặc đường bàn giao được nhóm chọn. Không cần cấp lại chứng chỉ chỉ vì đổi checkout.

**Sửa tối thiểu.** Ghi đúng các file thêm/sửa và điều kiện tương ứng. Đề xuất giữ kho metric production tách, sửa các truy vấn **thực sự dùng** khi Tempo chung bắt đầu có dữ liệu 84, xác nhận bản ghi exp/production không được tính lẫn. Chọn image Collector đúng digest với đường CD nhóm chấp nhận, hoặc nêu việc sửa guard giới hạn đúng service và nguồn image được duyệt. Hệ quả là có một số sửa file đang tồn tại ngoài dashboard mới. Những mục này phục vụ giai đoạn sau, không cần triển khai bây giờ.

### R7. Hai câu đưa ra hai điều kiện khác nhau về lọc ở nguồn — CHẶN kết luận đủ điều kiện bật 84

Mở rộng §4 để Minh quyết biên B16; §5 dòng 66 kết luận “chỉ cần Collector lọc phần còn lại”. B16 §6 yêu cầu whitelist trước khi ghi/xuất và mô tả filter Collector là dự phòng. File thô `kiem-cuc-bo/ban-6/bat-ghi-de/phan-tich.txt` có sentinel email/điện thoại trong trace, các tên đã che thành REDACTED, số exemplar bằng 0. `agent-docker-host.yaml` hiện sửa query ở ngữ cảnh span. Điều đó chưa xử lý mọi trường/event, log local hoặc nơi ghi trước Collector. §4 có nêu sentinel, span event và hai cách hiểu. Vì vậy lỗi nằm ở kết luận chắc chắn ở §5, chưa có chứng cứ dữ liệu thật đã rời máy 84.

**Sửa tối thiểu.** Giữ kết quả cục bộ và điều kiện §4, thay kết luận §5 bằng các nhánh. Đề xuất mặc định theo B16 hiện hành: giữ agent tắt cho tới khi đường ở nguồn đáp ứng chuẩn; Collector tiếp tục lọc dự phòng. Nếu nhóm chấp nhận biên trong cụm cho một phạm vi trace cụ thể, ghi rõ thẩm quyền, nơi đầu tiên dữ liệu được ghi/xuất và giới hạn, rồi đối chiếu sentinel ở các điểm B16 nêu. Chưa có số chi phí chỉnh instrumentation; thử một service trong môi trường thử khi được phép đủ để loại phương án không đạt cho service đó. Quyết định ảnh hưởng đường bật production, chưa ảnh hưởng Q6 demo.

### R8. Tỷ lệ limits và guard reader chưa quyết định bắt buộc thêm RAM hay một lịch CD duy nhất — KHÔNG CHẶN soạn hồ sơ, chặn hai kết luận cụ thể

Mở rộng §3 tách đúng phép cộng **chỉ cho Booking**. `tom-tat.tsv` tại `agent/bo-nho-{tat,bat}-768`, `ban-6/{tat-secret-true,tat-khong-secret,bat-ghi-de}`, `sua-review-5/tat-secret-true` cho 381,3 → 499,0; 416,8/386,1 → 491,7; 415,9 MiB khi tắt. Chênh làm tròn +118 và +75…106 MiB khớp. Số máy 84 đối chiếu được với LOG T-076 dòng 336–337, một lần đọc khi nhóm triển khai. Chưa có chuỗi đo ổn định theo node dưới tải tại pin tới; không thể xác nhận động bằng lượt này.

Tổng limits 115% cùng mức dùng 83% cho thấy nguy cơ áp lực RAM. Nó không tự buộc dời pod hay mua RAM khi đổi một limit. Kubernetes xét **requests** so với phần có thể phân bổ khi xếp pod. Tệp Deployment Payment tại pin, chẳng hạn, có request 512Mi và limit 768Mi. Nếu request giữ nguyên và tải mới còn đủ chỗ thì có thể giữ bố trí; nếu đỉnh thực hoặc rolling update gây áp lực thì có thể cần dời/tăng tài nguyên. So hai revision được nêu trong hồ sơ, `git diff f40b849 cd21f17 -- deploy/k8s/{booking-service,payment-service}/hpa.yaml` cho min/max từ 2/2 về 1/1. Đây là cấu hình nguồn, không phải quan sát số pod trên máy. [Kubernetes, quản lý tài nguyên Pod và container](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

Dòng 59 gộp “mọi lần ... đổi image/cấu hình”. Đúng khi đưa **digest mới** vào reader cần writer baseline tương thích. Ở `deploy-k8s-service.sh@f40b849`, Booking `writer_revision` so image, vị trí, HPA/PDB…; Event `event_writer_revision` còn so env/ConfigMap; Ticket/Payment so manifest đã chuẩn hóa. Cùng digest chưa bảo đảm đạt ở cả bốn, cũng không đủ căn cứ kết luận mọi đổi cấu hình đều buộc lịch writer-only ở cả bốn. Đề xuất khai trạng thái/digest và thay đổi thật của service bật; dùng writer-only khi guard yêu cầu. Đo lại tải và chỗ cho rollout trước khi nhóm quyết RAM. Tránh thay toàn cụm vì số của laptop.

**Quay lại khi bật 84 ở giai đoạn sau.** Công tắc cứng của mỗi workload phải đổi lại qua một revision/CD hợp lệ. Trang §2 nên ghi đích tắt đã biết cho từng service, giữ cấu hình nhận đến khi xác nhận service đã tắt, rồi mới gỡ đường nhận nếu cần. Kiểm revision và `writer-baseline` tại thời điểm chuyển. Dùng lại quy tắc hoàn tác C4/Q10 phù hợp với bản triển khai thực tế; không mặc định digest trước đây còn là `previous`. Việc này chỉ bổ sung đường quay lại vào hồ sơ, không đòi đổi layout repo hoặc thử trên 84 trong T-076.

### R9. Năm dòng §3 chưa bao hết các nơi bước 10 sẽ ghi — CHẶN xác nhận phạm vi phát lượt

SPEC mục Phạm vi ghi phân riêng obs bước 9 và obs bước 10. Bước 9 ghi rõ nhật ký/trạng thái bộ tải, làm mới token, phục hồi mock/đường hầm và nhận kết quả. Bước 10 ghi rõ spool, cấu hình Grafana và G1. B8/B14 lại dùng `tai_linux.start/receive` trên obs. `start` gọi `preflight(..., force=True)`, ghi nhật ký, làm mới pool trên máy tải và có nhánh khôi phục trên app. B10 ghi sổ trên obs. Khi chạy ca, `stage_b.py:133–177` tạo `rca/cases/<id>`, `run_m1.py` ghi `rca/outputs/<id>`, `orchestrator.py` ghi `runs/<lượt>`, `rca/bo-sung/<id>`, `rca/v082` rồi mới tới G1. Đây là hệ quả vận hành có thật của C6. SPEC đã duyệt mục tiêu demo và lượt k6, nhưng bảng “duyệt cả năm chỗ” không nói rõ hiệu lực đối với các ghi này. Trong §3, mẫu `t076-demo*.yaml` cũng không bao tên `t076-demo-go.yaml.mau` được đề xuất ở dòng 52.

**Sửa tối thiểu.** Trong đúng đề xuất để Minh duyệt trước bước 10, liệt kê các đường/loại ghi ở trên, các file Git thêm/sửa/đổi tên theo từng commit, máy nào chuyển bản nào và ghi nào sẽ giữ sau hoàn tác. Xác nhận tính cả các thao tác có điều kiện của controller. Phân biệt dữ liệu runtime ở `/srv` với mã ghim ở `/opt`. Không cần mở rộng quyền sửa lõi RCA, luật, dữ liệu cũ hay cấp quyền triển khai lên 84. Hoạt động đã diễn ra chỉ là soạn nháp. LOG ngày 28/11 ghi Minh đã duyệt riêng sửa ba file về URL ở lab và sau đó duyệt commit; đây không phải vi phạm ghi vượt quyền của người làm.

## Năm lựa chọn ở §3 trình Minh

| Điểm lệch | Đề xuất của Codex | Mặt trái, điều kiện và cách phân xử còn lại |
|---|---|---|
| Đích cảnh báo | **File provisioning + restart cho cả bật và gỡ**, dùng UID demo riêng cùng contact point. E5 có bằng chứng thêm, từng integration nhận Test, rồi gỡ về một UID. Dễ mang sang checkout mới và dễ phục hồi. | Gián đoạn Grafana và đánh giá lại luật. Chọn lúc chưa tải, đối chiếu trạng thái trước/sau theo R5. API sửa trực tiếp đỡ restart nhưng chưa có bằng chứng thêm/gỡ UID trong contact point nguồn file trên cấu hình này. Reload là ứng viên nếu muốn giảm gián đoạn: mã Grafana v13.3.0 đã có endpoint và kiểm quyền reload theo phạm vi alert rules. Tài liệu admin nêu Basic Auth. Có phiên đăng nhập UI hoặc Test thành công chưa xác nhận quyền gọi này. Dùng restart nếu chưa xác nhận được đường reload, không giao mật khẩu cho agent. Chi phí phân xử nằm ở A4/A5 và C trên lượt được phép. [Mã Grafana v13.3.0](https://github.com/grafana/grafana/blob/v13.3.0/pkg/api/api.go#L509-L512) · [Grafana Admin API](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/api-legacy/admin/#reload-provisioning-configurations) |
| Nguồn dashboard | **Sinh sẵn trên laptop** từ D3, kiểm diff chỉ đổi nguồn, giữ UID và dùng lại cặp commit. Dùng tên G1 ổn định với OUT riêng theo R3. | `build_dashboards.py::main` ghi bốn JSON. Ở pin này ba file có tên bộ cần thay: `00-start-here/start.json`, `20-incidents/rca-incidents.json`, `30-replay/rca-replay.json`. Trang hệ thống được sinh lại cùng nội dung nếu đầu vào tương đương. Git Bash dùng cú pháp env của docstring; PowerShell cần đặt biến môi trường theo cú pháp PowerShell. Chạy script trên obs tiết kiệm bước chuyển commit nhưng làm đổi file được Git theo dõi suốt lượt. Kiểm file sinh mặc định và diff thực trước khi chốt SHA. |
| Gốc lab | **Ghim chính xác D3 = `94bb11e`** nếu kết luận của T-070 bao phủ phần dùng và Minh chấp thuận đưa revision đó lên máy. Trỏ SHA bật/gỡ về cùng gốc. Khi chuyển sang gốc lab mới, áp lại riêng diff cấu hình và so với dev của gốc mới. | `da9c843` thêm sửa G1/bộ chuỗi; `94bb11e` đổi đường nhận thật. “Sau da9c843” không nhận diện duy nhất một bản. Cặp commit cũ có thể kéo lùi code tải/RCA khi đổi cả checkout. Ghi vai trò obs/app/tải và ngoại lệ checkout cấu hình của obs so với quy ước cùng commit trong lab/AGENTS §3. Chỉ cần xét các đường thay đổi. T-070 R1 về `chuoi_tai` không tự chặn lệnh tải trực tiếp. D2 là bằng chứng người phản biện và kết luận của Minh về tuyến dùng, không cần buộc tên một file tương lai nếu cùng việc đã được xác nhận ở nguồn chính thức. |
| Phạm vi file | **Duyệt diff tối thiểu** của hai file provisioning khi bật, biến đổi file gỡ khi hoàn tác, và ba dashboard có diff nếu kết quả sinh đúng. Ghi tên file đầy đủ và quyền ghi runtime theo R9. | Script viết lại bốn file tại laptop; file nào trùng byte thì không cần đưa vào diff. Không sửa bộ sinh, `rules.yaml` hay `providers.yaml` chỉ để đổi tên bộ. Trước khi có các SHA cụ thể là duyệt phương án chuẩn bị; duyệt chính các diff/SHA để phát là quyết định khác đã có ở D4. |
| Thời lượng | **Giữ 2.100 s tải và N = 25 phút, xin khung thời gian gồm cả phục hồi** theo R4. Đừng dùng E5 làm lời hứa phát hiện sau 56 s trên bản mới. | Có thể vượt một giờ dù tiêm ở giây 600. Phương án giữ trần một giờ phải nói rõ phần chuẩn bị và phục hồi nào được Minh duyệt ngoài lượt. Nếu không bố trí được, dời lượt hoặc diễn lại ca đã lưu và ghi rõ là phát lại. |

## Đối chiếu các lượt trước

Mức dưới đây đánh giá nhận xét và phản hồi **tại revision và công đoạn của nó**. Hồ sơ bàn giao PR ở revision mới thuộc lượt riêng. Không chuyển lỗi lịch sử đã được xử lý thành finding mới cho hai file.

| Nguồn và điểm | Đánh giá độc lập và hệ quả còn liên quan |
|---|---|
| REVIEW R1 | **Đúng.** Stage đọc capture và Prometheus thực nghiệm. Tách đường thu/metric giải quyết đường chính; bộ kiểm đọc Tempo chung vẫn cần R6. |
| R2 | **Đúng ở bản cũ.** Danh mục mẫu Secret và cách dựng Secret của CD giới hạn nguồn biến. SPEC 6 chuyển TLS/token sang Collector tương lai. Có ConfigMap đích OTLP không tự cấp CA. |
| R3 | **Đúng.** `agent-docker-host.yaml` có transform ở span, chuyển thẳng bỏ lớp này. Lời đáp bổ sung Collector hợp lý cho lớp sau nhận, khép yêu cầu nguồn mới **đúng một phần** (R7). |
| R4 | **Đúng.** SPEC bản 1 C5 đòi p95; SPEC 6 C4/Q7/Q8 đổi sang nền RAM, chức năng GET, Ready/OOM và quy tắc phục hồi. Việc Minh duyệt phạm vi mới không tạo số p95 hay bằng chứng quay lại. |
| R5 | **Đúng.** `_maven-verify.yml` dùng `b16-services.txt`; có bảy service, Discovery có trong danh sách, Assistant không có. Tám entrypoint có agent không có nghĩa tám hợp đồng log B16 đã được kiểm. |
| R6 | **Đúng.** `_deploy-service.yml:120` giữ hai kiến trúc. Entry point lấy `SERVICE_VERSION` cho định danh. Không cần bỏ đường build ARM cho demo. |
| R7 | **Đúng về bản và phạm vi cũ.** Lịch sử lab xác nhận `c1da15f → da9c843 → 94bb11e`. Quyền đặc biệt cho URL ghi rõ trong LOG. Phạm vi bước 10 mới còn R9. |
| REVIEW-2 N1 | **Đúng.** CD mang con trỏ revision qua mỗi lần phát. Trạng thái active trước merge không phải đích vô điều kiện sau các lần phát kế tiếp. |
| N2 | **Đúng.** Các truy vấn thật của bộ kiểm ở R6 vẫn cho phép cùng service khác môi trường. Phần B hiện chỉ có nguồn exp theo thiết kế; rủi ro phát sinh khi nối production. |
| N3 | **Đúng.** Sentinel còn trong payload trước processor. Lượt bật Booking chứng minh lọc theo tên và tắt exemplar trên ca thử; không chứng minh whitelist trên toàn chuỗi. |
| N4 | **Đúng.** Datasource Tempo hiện trỏ serviceMap sang Prometheus thực nghiệm. Cần nạp và dùng đúng datasource khi bật 84; không cần triển khai ở task này. |
| REVIEW-3 R1 | **Đúng.** Tại pin PR, công tắc nằm trực tiếp trong workload; bản 6 đã bỏ phụ thuộc vào giá trị Secret cũ khi tắt. Kết quả trên pod thật thuộc bước 7. |
| R2 | **Đúng.** C4 đã khai nền, giờ theo dõi, hành động và phạm vi các GET. Chưa có phép đo production trong hai file. |
| R3 | **Đúng.** Q4, E5 và code xác nhận các lần ghi obs. SPEC 6 đã mở phần vận hành; nhánh mới ở bước 10 cần minh định tiếp theo R9. |
| R4 | **Đúng.** Bộ gom có thể nhận vào ca cũ đã hết cảnh báo trong 300 s. Người làm đã sửa B9; tình trạng hàng đợi và tải còn R1. |
| R5 | **Đúng.** C5/Q5 ghi riêng bản demo, chọn bản W7 để khi mở lại. C6 không chọn phương pháp/benchmark. |
| R6 | **Đúng.** Hai trường exception có thể cùng mang nội dung. §2/§4 đã giữ cả hai; còn mâu thuẫn §5 ở R7. |
| R7 | **Đúng.** SPEC 6 bước 8 ghi bản dựng, tag cũ, cấu hình hiệu lực, mock/ngrok và giới hạn dữ liệu DB. Đây là việc trước demo. |
| REVIEW-4 R1 | **Đúng.** Script cần revision phù hợp ngoài digest, còn `writer-baseline` tùy service. Quyền thao tác khẩn cấp vẫn của Minh. |
| R2 | **Đúng.** E5 §5 dùng đường/checkout cũ. Runbook dùng đường mới, nhưng nhánh API và phân bổ ghi bước 10 còn R5/R9. |
| R3 | **Đúng.** Khai trước E5 phân biệt cửa sổ, hai cờ, đúng ca trên giao diện và độ phủ. Bản 2 đưa chúng vào B13. Cách thực sự xác nhận mốc còn R1/R2. |
| R4 | **Đúng.** Workload có công tắc tắt nhưng code filter/listener/log của PR vẫn chạy. C4 đã thu hẹp câu kết luận. |
| REVIEW-5 R1 | **Đúng.** Diff `2a275b5..f40b849` đổi fixture `BookingPersistenceIT`; log integration cục bộ có 157 ca lớp đó, toàn Failsafe 173 ca, đều 0 failure/error. Không suy ra tín hiệu demo đạt. |
| R2 | **Đúng một phần nếu hiểu là mọi cấu hình.** Guard giữ digest và so manifest khi có reader. Trường hợp writer-only sang writer-only và các khác biệt theo service cần xét như R8. Trạng thái thật trước merge cần nhóm xác nhận. |
| R3 | **Đúng với vấn đề nối mã.** `OrderController` ở pin đã trả header orderId. Khẳng định chỉ sửa header là đủ nối mã tạm với orderId **đúng một phần**; B16 §3 còn cần log liên kết. Đây thuộc luồng PR. |
| R4 | **Đúng.** Đã đối chiếu nhánh ghi callback UNKNOWN trong diff `BusinessTelemetry.java`; đây là ngữ nghĩa log, không tự chứng minh trạng thái giao dịch trên máy. |
| R5 | **Đúng một phần về mức đã sửa.** `PaymentMessageListener` ở pin phân biệt hợp đồng sai, lỗi IO lệnh broker và ngoại lệ giao dịch; ngoại lệ runtime của kênh vẫn có thể vào nhánh RETRY. Không dùng nhãn retry làm chứng cứ broker đã giao lại. |
| R6 | **Đúng.** Đối chiếu StatefulSet Discovery và ConfigMap production tại pin. Trường giá trị trên pod còn thuộc bước 7. |
| R7 và N1 của người làm | **R7 đúng một phần, N1 đúng.** Customizer Event loại trùng span cha và ưu tiên khóa agent; bảy ConfigMap ở pin đã bỏ khóa MDC tùy chỉnh. Thứ tự/ID span Event đang xử lý khi agent thật bật cần ghép log với span cùng Event ở lượt tín hiệu được phép; một log riêng chưa phân xử được. |
| R8 | **Đúng về lỗi quy nguyên nhân và số lần thử ban đầu.** `TicketOutboxPublisher` đã tính `max(0,attempt-1)`. Nhánh ghi RETRY còn có thể xảy ra khi dời lịch không tác động dòng nào; sửa nguyên nhân báo broker chưa đủ khẳng định dời lịch xong. |
| R9a, R9b và N2 | **R9a đúng:** CI verify không build image bằng CD, lượt local dùng đường đóng gói ghi trong README kiểm cục bộ. **R9b đúng:** hồ sơ `sua-review-5/log/ticket-replica-*` có lượt hỏng, lượt chạy trên bản sao fixture và đối chứng main; không suy bản nguyên đạt. **N2 đúng về việc đính chính:** LOG mục 14:30Z đã hiệu chỉnh hai giờ; không dùng hai giờ xấp xỉ này để dự toán bước 10. |
| T-070 REVIEW-5 R1–R5 | **R1 đúng** cho tiếp nhận bằng `chuoi_tai`, không nằm trên B8 trực tiếp. **R2 đúng, khép một phần**: `khoi_tao` đã bắt nguồn thiếu/chừng dở điển hình; trường hợp chỉ mục tồn tại trước khi toàn bộ cây chép xong còn R3. **R3 đúng**, file xuất Q4 bỏ `endsAt`. **R4 đúng**, summary k6 toàn lượt không xác định nguyên nhân p95 của cửa sổ route. **R5 đúng ở thời điểm nhận xét**, lịch sử commit RCA có `672391b`; mục theo dõi không cấp quyền chạy. Không thay kết luận chính thức của T-070. |

**Lượt bổ sung 28/11.** Chỉ có tóm tắt F1–F8 trong LOG chứ không có toàn văn phiên kia trong repo. Đã đối chiếu từng mệnh đề được lưu với file/code.

| Điểm | Kết luận về nhận xét và bản 2 |
|---|---|
| F1 | **Đúng** về đọc hồ sơ sự cố và khoảng ghép. **Đúng một phần** về bằng chứng Q4 và mức đủ của B9. Nguồn t_hết và khoảng tồn đọng spool xem R1. |
| F2 | **Đúng.** STOP chặn bắt đầu xử lý ca mới; vòng lặp còn đọc spool, ca đang xử lý có thể tiếp tục các bước. C1 đợi ca đang chạy rồi dừng đúng tiến trình là phù hợp. Không dùng STOP trước khi giữ bằng chứng ca còn `cho` nếu đang chấm quá N. |
| F3 | **Đúng.** `orchestrator.py:54,93` có STOP toàn cục; D6 đã thêm. STOP theo OUT của lần trước vẫn là phản ví dụ ở R3. |
| F4 | **Đúng, đã xử lý một phần.** Sổ đặt obs, ghi bằng user ledger và lưu kết quả của app. Cần xác định rõ trường thời gian chấm và nhánh tiêm thất bại như R2. |
| F5 | **Đúng.** A5/A6/B12 cần Grafana; D9 đã nêu đường hầm và phiên của Minh. Kiểm login/Test khác quyền admin reload. |
| F6 | **Đúng về cửa sổ.** 900 + 600 + 600 = 2.100 s. **Đúng một phần** về tổng chi phí 51–65 phút, vì còn C và nhận dữ liệu (R4). |
| F7 | **Đúng.** Tên container trong compose bằng tên restart tại A4/C2; bằng chứng restart E5 có thật. Chưa xác nhận restart tại checkout mới hay nạp lại không restart. |
| F8 | **Đúng về hai chỗ thiếu** là gốc lab và file Grafana. Nói đủ năm điểm cho toàn bộ quyền/đường chuyển trạng thái mới **đúng một phần** (R5/R9). |
| Ba sửa ở hồ sơ 84 | **Đúng** khi tách phép cộng RAM cho Booking, ghi thời điểm đang rollout và nhận diện Discovery thiếu các biến OTEL. Còn file StatefulSet, đường đưa CA sang máy mới và kết luận về giới hạn RAM (R6/R8). |

## Tuân thủ quy trình và mức bằng chứng

- SPEC 6 và LOG ghi Minh duyệt bản 6 ngày 27/11, sau đó duyệt viết hai đầu ra, sửa hai bản nháp và đường dẫn bộ nhận ngày 28/11. Quyền đó khác duyệt chạy. D1, kết luận T-070 và phê duyệt runbook vẫn là phụ thuộc. Không thấy bằng chứng người làm đã phát bước 10 hay ghi ngoài phần đã duyệt để tạo **hai đầu ra này**. Câu chữ ghi quyết định T-076 cho DECISIONS còn chờ Minh theo STATE. Không nâng năm ứng viên ở §3 thành quyết định đã ghi.
- Đối chiếu tiêu chí xong: (1)–(2) thuộc tuyến PR, merge và theo dõi trên 84, chưa được hai tài liệu chứng minh. (3) cần bản ghim demo thực và kiểm bước 9. (4) chưa có `exp-app/demo.md`, runbook là nháp. (5) đã có hồ sơ việc thêm/sửa và RAM, còn R6–R8. Các phụ thuộc triển khai hợp lệ của giai đoạn sau tự chúng không phải lỗi. Chênh lệch nằm ở chỗ tài liệu hiện hướng dẫn sai hoặc mạnh hơn bằng chứng.
- DT18-NV2/NV3 và hướng dẫn của cô đòi áp dụng nghiên cứu trên hệ bán vé, minh họa đồ thị/chẩn đoán, còn RQ5/P10 cần đánh giá qua điều kiện tải/lỗi. T-076 C6 chỉ đề nghị kiểm đường tích hợp trên một ca. Tải nhiều mức, độ đúng vùng/nguyên nhân và phần giải thích LLM của P10 vẫn thuộc các gói tương ứng. Không cần thêm đối chứng vào T-076; không suy lợi ích của cạnh, độ nhạy hoặc độ chính xác từ ca này.
- WHY-109 giải thích 300 s bằng cửa sổ rate và nửa cửa sổ RCA. Đó là quy ước nhóm đã chọn; không chứng minh ca ghép đúng cơ chế vật lý. WHY-111 ghi lý do sau E5 và ghi đúng ngày khóa ngưỡng trước E5. Cờ phủ tách khỏi đạt chức năng. WHY không làm 300 s hay 25 phút trở thành độ trễ đo được của bản mới. Chưa thấy lựa chọn phương pháp mới bị dùng trong hai đầu ra mà thiếu WHY. Các cách triển khai §3 là đề xuất vận hành. Bằng chứng E5 thuận cho provisioning; chưa kiểm API là giới hạn bằng chứng, không đủ để bác bỏ API.
- Xét phạm vi ghim trước khi đề nghị sửa: `git grep` theo tên hai tài liệu trong manifest/SHA256/plan JSON **được Git theo dõi** không thấy dòng khớp. SPEC và LOG tham chiếu runbook theo đường dẫn. Đổi nội dung đổi blob của tài liệu ở revision sau. Không sửa khai trước E5, Q4, dữ liệu, mã phương pháp hoặc manifest để “khớp” bản nháp mới. Mọi đổi file Grafana sau này sinh revision lab mới; ghi SHA gốc và diff riêng. Không có commit DEMO/HOAN-TAC trong phạm vi kiểm của lượt này.

## Điều đã kiểm và thấy đúng

- **Toàn vẹn.** Dùng PowerShell, với từng dòng trong `results/T-073/e5/SHA256SUMS`, `e5/ca-7577dd5b.SHA256SUMS`, `results/T-070/don/q4/SHA256SUMS`, đối chiếu `Get-FileHash -LiteralPath <file>` theo đúng gốc lần lượt T-073, thư mục ca, thư mục q4. Kết quả **52/52, 58/58, 12/12**, không thiếu, không lệch. `Get-FileHash` trên khai trước và kế hoạch triển khai E5 khớp hai giá trị đầy đủ tại LOG T-073 dòng 154, 209. Các mốc bổ sung sau thời điểm lập manifest E5 như `hoan-tac/s5-4-kiem-sau-restart.txt` là file theo dõi bằng Git; đối chiếu với HEAD. Không tính chúng vào 52 mục.
- **Đường dữ liệu và nhãn.** Webhook ghi giờ nhận + payload; bộ gom hiểu firing/resolved, thiếu nhãn/lỗi nguồn đi lớp quan sát. Stage nhận `startsAt` đã quy giây, sinh mã mờ và `request.json`, lập gói từ capture/Prometheus. P7 và phần bổ sung đưa dữ liệu vào V082 ghim. G1 kiểm cửa sổ nano giây, lấy `entity_ranking`, nhóm đồng hạng và kênh cờ từ đầu ra đã tính qua `sau_v082.dung_mot_ca`; đồ thị dịch vụ còn dùng trace gốc để hiển thị. Trên ca E5, V082 `method-output-1.json#/extra/canh` có cạnh gateway–Booking; `#/window/{N,A}` gặp nhau ở 1795400310000000000 ns. `e5/su-co/bbc0a6d44f.json#/ma_ca_m1` là `7577dd5b`, `#/ket_qua/trung_sha` đúng và `#/ket_qua/nhom_hang_1/0` là Booking trong lượt pause Payment. Đây là phản ví dụ cụ thể cho suy luận “hàm băm trùng và có đồ thị thì tìm đúng nguyên nhân”. Cờ `trung_sha` kiểm tính lặp, còn nhãn ô và sổ dùng cho điều khiển/chấm sau. Không thấy đường đưa chúng vào khâu chọn ứng viên hoặc xếp hạng trên tuyến đã rà. Không có nhánh không đồ thị hay thay thuật toán trong hai đầu ra để so.
- **Kiểm rẻ, chỉ đọc.** Đếm trực tiếp manifest workload và ConfigMap ở pin PR: 7 Deployment + 1 StatefulSet có công tắc, 7 ConfigMap có 29 tên query mỗi file; Secret mẫu không có diff so với main gốc. Đếm UID luật, nguồn dashboard, so phép tính thời gian, truy ngược `endsAt`, kiểm bộ gom/lock/đích bằng mã, đọc các JSON/TSV và README từng lượt kiểm cục bộ. Không dựng lại dashboard lên cây lab vì bộ sinh ghi bốn file. Python của venv tại laptop không khởi động được trong phiên này; các phép đọc, hash và số học đã thực hiện bằng PowerShell/Git. Chưa có bằng chứng runtime mới trên máy thật.

## Báo cáo lượt và đề xuất tiếp tục

1. Đã soát hai đầu ra gốc, kiểm đường thực thi, phân xử lại phản hồi lịch sử và năm lựa chọn §3.
2. File duy nhất tạo trong lượt là `tasks/T-076-pr17-otel-may-84/REVIEW-7.md`. Giữ các bản cũ. Không commit.
3. Kiểm toàn vẹn và đối chiếu revision đạt như trên. Phát hiện các mâu thuẫn có thể thay đổi kết quả chấm hoặc làm mất khả năng tái sử dụng trong R1–R5/R9; R6–R8 ảnh hưởng hồ sơ mở rộng.
4. **Đề xuất tiếp tục một lượt người làm đáp phản biện**, chỉ sửa sau khi Minh duyệt đề xuất cụ thể. Ưu tiên bản sửa runbook ở các chỗ điều khiển/chấm/hoàn tác, giữ bộ hiển thị và giữ cặp cấu hình dùng lại. Đối với 84, sửa hồ sơ trước, để nguồn lọc, số RAM dưới tải, giá egress và lịch writer theo service cho giai đoạn được phép. Với chi phí egress, cần lượng byte nén/đơn vị thời gian của đúng cấu hình và biểu giá/định mức khi triển khai; hiện chưa có tải đo nên không có cơ sở dự toán tiền. Với MDC Event, tận dụng log/span của Event ở bước kiểm tín hiệu hợp lệ nếu có, không chạy thêm trong lượt này. Nếu các điều kiện máy thật chưa tới, có thể dừng sau khi thống nhất giới hạn và đường kiểm trong các bước đã duyệt. Minh quyết việc sửa tài liệu, thời lượng và phạm vi triển khai. Lượt này chưa cấp quyền chạy.

## Prompt bàn giao cho người làm

Minh có thể sao chép khối dưới sang Claude. Không có khối cổng cho P9/P10 của lượt này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md bản 6, results/T-076/exp-app/runbook-online.md bản 2 và results/T-076/mo-rong-may-84.md.
- Công đoạn: người làm đáp phản biện, gồm đánh giá các đề xuất trong REVIEW-7.md.
- Gói/cổng: P9/P10, tích hợp ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude là người làm, Codex là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md, SPEC.md và LOG.md của T-076, hai đầu ra trên, docs/architecture/B16-observability-baseline.md của FlashTicket.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md tới REVIEW-5.md cùng bảng phản hồi, LOG T-076 mục phản biện bổ sung ngày 28/11, REVIEW-6.md của tuyến PR và REVIEW-7.md của hai đầu ra.
- Code và kết quả liên quan: results/T-073/{khai-truoc-e5.json,trien-khai-e5.md,e5/}, results/T-070/don/q4/, tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-5.md, results/T-076/kiem-cuc-bo/, repo lab D:/Project/flashticket-rca-lab @94bb11e và FlashTicket D:/Project/flash-ticket-platform @f40b849, chỉ đọc trên laptop, không vào máy 84, exp-app hay obs, không dùng subagent.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat theo quyền hiện có cho lượt đáp, trừ khi Minh cấp rõ quyền ghi riêng cho lượt đó.

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

Người làm chỉ điền bảng theo phạm vi Minh duyệt. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN B10 | B9 bản 2 không kiểm tải còn chạy (`get` của đúng tag), không kiểm tín hiệu tải trước tiêm như E5 (`e5_luot.sh`), không kiểm spool đã đọc hết. `rules.yaml` 9 dòng `noDataState: OK`, nên route không tải vẫn bình thường. `orchestrator.py:216–228` đọc spool rồi xử lý ca đồng bộ, file sự cố có thể chậm hơn spool. Ví dụ Q4: `q4/canh-bao-nhan.out` dòng 14 là giờ **nhận** 03:29:28 (`startsAt` 03:24:40), không có `endsAt`; "giây 483 / 783" là sai nguồn. Sửa ở runbook bản 3 (B9, ví dụ Q4). | |
| R2 | Đúng; CHẶN chấm | B10/B13 bản 2 gọi `mark` là mốc tiêm. E5 chấm bằng `fault-start.inj.t` (`dinh-chinh-e5-1.md` §1). Lệnh tiêm hỏng/thiếu sổ chưa có nhánh riêng, §5 có thể chấm nhầm "bỏ sót". B12 ghi giờ thấy trong danh sách, chưa ghi giờ mở được ca có đồ thị và hạng (C6). Sửa ở B10, B12, B13 và §5. | |
| R3 | Đúng; CHẶN diễn tập lại | OUT theo ngày, nên lượt hai cùng ngày dùng lại `STOP`, `spool-da-doc.json`, sự cố cũ. `g1_b.py:177–183` thêm ca mới vào chỉ mục, nên A6 "số ca = dev" sai từ lượt hai. `g1_b.py:87` trả `da_co` chỉ vì có `chi-muc-ban.json`; nếu lần chép đầu dở ở giữa `copytree(du-lieu)` thì lần sau không phát hiện. Sửa: ID riêng mỗi lần phát cho OUT/spool/env/tag/sổ; giữ tên bộ hiển thị; A6 kiểm tập ca cũ còn đủ; A2 so danh sách file + hash với nguồn. | |
| R4 | Đúng; CHẶN thời lượng | Bản 2 tính theo độ trễ ví dụ 56 s. Biên xấu: tiêm giây 900, t̂ sát cuối cửa sổ 600 s, chờ N 25 phút, hoàn tác 10 phút ≈ 75 phút. Sửa §2 và §3: khung ~75 phút cộng phần chờ ca đang xử lý; trình Minh. | |
| R5 | Đúng; CHẶN nhánh API | Nhánh API bản 2 "giữ nguyên các bước khác" nhưng A4/C2 vẫn checkout DEMO/HOAN-TAC có file integration: hai nơi cùng quản lý một đích. Sửa: chỉ giữ nhánh file; ghi trạng thái contact point/dashboard trước và sau; nhánh API, reload để ngoài runbook, chưa kiểm. | |
| R6 | Đúng; CHẶN dùng hồ sơ 84 làm kế hoạch | Discovery là `statefulset.yaml` (`git ls-tree f40b849:deploy/k8s/discovery-server`). `tests/signals/check_purchase_journey.py` truy vấn Tempo không lọc môi trường (file có sẵn phải sửa). `git ls-tree -r 94bb11e -- observability/tls` rỗng: CA không theo clone lab. Sửa bảng §2 của `mo-rong-may-84.md`. | |
| R7 | Đúng; CHẶN kết luận bật 84 | §5 "chỉ cần Collector lọc phần còn lại" trái điều kiện §4 và B16 §6 (lọc trước khi ghi/xuất). Sửa §5 thành các nhánh; mặc định giữ agent tắt tới khi lọc ở nguồn đạt B16. | |
| R8 | Đúng; KHÔNG CHẶN | Kubernetes xếp pod theo requests; limits 115 % là nguy cơ, không buộc thêm RAM. Câu "mọi lần bật agent … đều cần lịch writer-only" nói quá: guard so khác nhau theo service. Sửa §3, §4 và thêm đường quay lại khi bật agent. | |
| R9 | Đúng; CHẶN phạm vi phát lượt | Bản 2 chưa liệt kê ghi của `tai_linux start` (preflight, pool máy tải), `stage_b`/`run_m1`/bổ sung/V082 khi chạy ca, sổ trên obs. Mẫu `t076-demo*.yaml` không khớp `t076-demo-go.yaml.mau`. Sửa: bảng nơi ghi theo máy và commit trong §3. | |

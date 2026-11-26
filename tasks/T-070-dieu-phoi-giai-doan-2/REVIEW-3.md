# Phản biện T-070 — kết quả dọn repo lab và ba máy

- **Người phản biện** Codex. **Người làm** Claude. **Ngày** 26/11/2026.
- **Công đoạn** Soát kết quả, lượt 3. Việc vận hành trước W7, ngoài G0–G4. Minh cho ghi riêng `REVIEW-3.md`.
- **Bản đã đọc** Lab `85ace52` so với `truoc-don-2026-11` (`4b6c4b2`). RCA `ee16127` và phiên bản làm việc hiện tại của kế hoạch/LOG/STATE. Đường mã lab dưới đây tính từ gốc repo lab.
- **Tự soát độc lập** Đọc hai AGENTS, SPEC, kế hoạch bản 3.1, hợp đồng, diff, hiện vật trước/sau, chỉ mục archive và bằng chứng trên ba máy trước khi mở hai file phản biện cũ. Đối chiếu DT18-NV2/NV3, phần 2 hướng dẫn cô, MRP P9/P10 và RQ5, WHY-08/98–101/110–111, DECISIONS 16–24/11, LESSONS và mục cuối LOG. Sau đó kiểm riêng từng phản hồi cũ.

## Kết luận chung

**Giữ cấu trúc mới và các kết quả đã xác nhận. Chưa dùng nguyên trạng để phát lịch mới dựa vào cam kết tag không tái dùng, bật lại tuyến trực tuyến theo README, hoặc dùng nhánh dự phòng RECREATE-PAY.** Ba máy cùng chạy commit đích. Bản chụp mã và hai ca hồi quy V082 khớp. Một ca phát lại trực tuyến khớp trong điều kiện đầu vào cố định. Q4 đạt các tiêu chí tín hiệu đã chấm.

Đợt dọn đạt phần bảo toàn hiện vật, hiển thị và đường mua vé đã kiểm của P9/P10. Việc nghiệm thu toàn T-070 vẫn theo SPEC mục Tiêu chí xong. Điều phối đã dừng theo lệnh Minh, W7 hoãn và W9a chưa diễn tập. Q3/Q4/Q6 chưa phân xử RQ5, độ nhạy cảnh báo, độ chính xác xếp hạng trên ô mới hay tác dụng của quan hệ đồ thị. Đồ thị hiển thị của WHY-100 đọc trace gốc, rồi ghép màu/hạng từ kết quả lõi. Phép kiểm B10/B12 xác nhận bảo toàn hiển thị.

## Các điểm

### R1. Bộ tải đã quên tag chuyển vào archive — CHẶN dùng nguyên guard cho lịch tải mới

- **Ở đâu** `load/controller/tai_linux.py:225–251`, `load/controller/chuoi_tai.py:454–471`, bước 4 và X1.
- **Sai gì** Trước dọn, phép kiểm từ chối tag tồn tại dưới `load-runs/` trước khi chuẩn bị token. Sau dọn, phép kiểm chỉ xem `runs/`. Chạy khô của bộ chuỗi suy “tag chưa dùng” từ lỗi `get`, tức thiếu container hoặc lỗi đọc có thể được gắn cùng nhãn.
- **Bằng chứng** Trên máy tải, dùng `find` liệt kê tên thư mục con tại `archive/2026-11/load-runs` và `runs`, lấy tên container từ `sudo -n docker ps -a --format '{{.Names}}'`, rồi `comm -23` giữa danh sách archive và hợp của hai danh sách đang dùng. Kết quả **47** tag archive không có thư mục hoặc container cùng tên đang dùng. Q4 dùng tag mới, nên Q4 đạt và trường hợp này có thể cùng đúng. Không gọi `start` để tái dùng tag.
- **Bước và quyết định chịu ảnh hưởng** Mất một chốt bảo toàn danh tính lượt chạy. Nếu một tag trong số này được chọn lại, hồ sơ cũ và mới cùng tên. `get` và `receive` sẽ gắn với hiện vật mới trong khi chỉ mục archive vẫn trỏ tag cũ. Chặn phát lịch dựa vào lời cam kết “tag không tái dùng”; chưa thấy tag nào thực sự bị tái dùng.
- **Đề xuất sửa** Cho kiểm tra trước phát và chạy khô dùng chung quy tắc nhận dạng tag đã dùng ở kho mới, archive đợt dọn và container còn giữ. Tách lỗi đọc máy khỏi kết quả “chưa dùng”. Chi phí xác nhận là vài phút với kết quả giả lập và danh sách metadata đã có. Cách chỉ dùng prefix mới là biện pháp tạm khi Minh cần một lượt riêng; nó vẫn để CLI cũ chấp nhận nhầm và chưa giải quyết lần tiếp nhận sau.

### R2. Điều kiện giới hạn thư mục ghi trực tuyến chưa đúng hợp đồng — CHẶN xác nhận đã cách ly vùng ghi G1

- **Ở đâu** L1, I9, `rca/online/g1_b.py:37–51,75–97`, `rca/online/orchestrator.py:151–154,238–256`.
- **Sai gì** Tiến trình ghi chạy bằng root. Điều kiện hiện tại so đúng một đường `dev` và kiểm tiền tố ở tên cuối. Nó chưa xác nhận đích chuẩn hóa nằm ngay dưới `rca/results/`, cũng chưa áp cùng quy tắc cho các thư mục con dùng khi ghi hoặc cây chép vào. Kiểu khởi tạo chép giữ liên kết tượng trưng. Bộ điều phối bắt đầu xử lý trước khi G1 kiểm đích.
- **Bằng chứng** Đọc điều kiện L1 và đối chiếu với hai phép kiểm riêng ở dòng 78–79. Sau đó `khoi_tao`, hàm xuất và phần viết chỉ mục dùng lại đường từ đối số. Ca Q6 dùng đích hợp lệ, do đó xác nhận đường bình thường. Root sở hữu `dev` (755) và phép so cây hiện có 3.676 file cho thấy chưa có dấu hiệu ghi nhầm trong lần triển khai. Mẫu kiểm tiền tố đã có ở bản cũ, lần này điều kiện ấy được tái sử dụng dưới đường mới.
- **Bước và quyết định chịu ảnh hưởng** Chặn tuyên bố phiên trực tuyến được giới hạn vùng ghi như README/I9, trước khi bật lại dịch vụ hoặc nhận một đích cấu hình mới. Đây là thiếu sót xác thực đường dẫn ở luồng vận hành đặc quyền. Bằng chứng hiện có không xác định bất kỳ ai từ mạng có quyền đặt `--ra`, và không cho biết đã xảy ra ghi ngoài vùng.
- **Đề xuất sửa** Kiểm đích đã chuẩn hóa là một bộ `online-*` ngay dưới gốc được phép, rồi dùng chính đích đã kiểm cho mọi thao tác. Từ chối liên kết tượng trưng ở đường sẽ ghi, giới hạn nguồn chép vào bộ đã được duyệt. Kiểm sớm ở đầu tuyến, giữ chốt ở điểm ghi root. Có thể xác nhận điều kiện bằng kiểm đơn vị trên mô hình đường dẫn và ca dev Q6 đã có; chưa cần tải. Chỉ ghi thông lệ đặt tên trong README rẻ hơn, nhưng không cưỡng chế được phạm vi ghi.

### R3. Nhánh dự phòng tái tạo Payment trỏ tới bộ Compose thiếu env — CHẶN dùng nhánh này cho ô RECREATE-PAY

- **Ở đâu** `faults/injectors/docker/inject.py:20–22,64–69,126–143`, `sau-buoc-3/lenh-2-doi.sh`.
- **Sai gì** Khi thiếu cấu hình hiệu lực, mã mới chuyển sang Compose T-062 trong archive. File này tham chiếu `../env-t062/payment-service.env`. Lệnh dời đã chuyển env hiệu lực sang `/opt/flashticket/env/`. Archive là tư liệu lịch sử, không còn đủ nguồn để bật Payment bằng nhánh đó.
- **Bằng chứng** `git show 4b6c4b2:app-host/services/payment-service.yml` xác nhận tham chiếu env. SSH chỉ đọc thấy file Compose lưu trữ hiện diện, `test -s` báo env tương ứng trong archive thiếu, còn env dưới cây mới hiện diện. `compose-dir` và nhãn `com.docker.compose.project.config_files` của Payment đang chạy cùng trỏ cấu hình mới. Kiểm tĩnh, không gọi tạo lại.
- **Bước và quyết định chịu ảnh hưởng** Nhánh thường đang có tiền điều kiện đúng. Nếu file trạng thái mất/rỗng và không có biến chỉ đích, nhánh dự phòng đã duyệt sẽ thất bại; nếu ai dựng lại cây archive thiếu đúng một phần, nguy cơ dùng sai cấu hình tăng. Không suy ra ca hồi quy `ebd5ef38` đã kiểm tiêm lại. Ca đó dùng gói cũ.
- **Đề xuất sửa** Từ chối làm tiếp nếu không xác nhận được nguyên bộ Compose đang chạy, báo rõ nguồn cần khôi phục. Có thể đối chiếu đường đã chọn với nhãn Compose của container trước thao tác. Cách phục dựng nhánh T-062 phải quản thêm một bộ env/bind cũ, trái mục đích dọn và tốn hơn. Kiểm bằng đối chiếu file/nhãn và nhánh điều kiện giả lập trước khi phát ô; chỉ thử tái tạo thật khi Minh duyệt lượt cần nó.

### R4. Nhật ký build theo SHA ngắn ghi đè giữa các nhãn — CHẶN dùng thư mục dùng chung làm bằng chứng build mới

- **Ở đâu** `test-environment/scripts/build.sh:9–26,28–44,47–80`.
- **Sai gì** Worktree và thư mục log được gom theo cùng tám ký tự đầu của revision. Gom worktree có thể hữu ích. Tên image vẫn chứa nhãn, còn file log từng bước, `build-manifest.json` và marker `*.done` không chứa nhãn/lượt. Build cùng revision với nhãn khác sẽ ghi đè manifest và log, nối tiến độ vào cùng TSV. Marker cũ có thể còn khi lần sau gián đoạn. Mã cũ đã có giới hạn khác: `verify_one` luôn trả 0 và marker chỉ nói script đi đến cuối, còn kết quả Maven/Docker ở log/manifest.
- **Bằng chứng** So hai bản `build.sh` bằng `git diff -M`: trước dọn đường log chứa cả `LABEL` và SHA, bản mới bỏ `LABEL`; dòng 48 ghi mới manifest, dòng 31/53 mở log theo tên cố định, dòng 80 ghi marker. T-070 tái dùng image/worktree cũ, không có bằng chứng đã ghi đè log sau dọn.
- **Đề xuất sửa** Giữ worktree theo revision nếu dùng nối tiếp. Đặt log/manifest theo lần chạy khi cùng revision có nhiều nhãn hoặc phải chạy lại; mỗi marker đứng cùng chứng cứ của đúng lần. Giữ rc riêng trong kết quả và dựa vào chúng để xác nhận build đạt. Cách chỉ khôi phục nhãn vào đường log xử lý hai nhãn nhưng còn ghi đè khi chạy lại cùng nhãn. So lệnh và hai định danh đầu ra giả lập là đủ để xác nhận trùng tên đã hết; không cần build chỉ để so tên.

### R5. Hướng dẫn bật trực tuyến sai thư mục làm việc — CHẶN chạy đúng nguyên khối lệnh trong README

- **Ở đâu** `rca/online/README.md:20–31`, đối chiếu `sau-buoc-4-5/q6/q6-chay.sh`.
- **Sai gì và bằng chứng** README chuyển vào `/opt/flashticket-rca/observability/alert-receiver` để bật bộ nhận, rồi gọi Python bằng đường tương đối `rca/online/orchestrator.py`. Git tree không có đường đó dưới thư mục bộ nhận. Lệnh Q6 đã chạy dùng `cd /opt/flashticket-rca`; vì vậy Q6 không vấp lỗi này. Khi làm theo README, có thể bật bộ nhận mà bộ xử lý chưa chạy.
- **Đề xuất sửa** Dùng đường tuyệt đối trong lệnh điều phối hoặc trở về gốc repo ngay trước lệnh. So các đường lệnh với cây commit. Cách này giữ nguyên cơ chế nhận cảnh báo và không đòi chạy lại Q6.

### R6. Báo cáo Q4 gán nguyên nhân cho thời điểm cảnh báo sớm hơn lúc Gateway được tạo — KHÔNG CHẶN Q4 đạt tín hiệu

- **Ở đâu** `q4/README.md` mục “Hai điều thấy ở cảnh báo”, `q4/canh-bao-nhan.out` dòng 2–6, `sau-buoc-3/deploy.tsv`, `rules.yaml` luật `t072-mat-gw`.
- **Sai gì và bằng chứng** `startsAt` báo `16:32:00Z`. `docker inspect ... --format '{{.State.StartedAt}}'` trên app cho Gateway hiện hành khởi động **16:38:32Z**, phù hợp với `deploy.tsv`. Trạng thái đã bắt đầu trước khoảng 6,5 phút, nên Gateway mới không thể là nguyên nhân làm cảnh báo bắt đầu. Cảnh báo hết lúc 03:21:47Z, 22 giây sau khi Q4 bắt đầu. File có **14** dòng giao nhận, trong đó **5** dòng trước thời điểm Q4 bắt đầu. Các dòng này chứng minh đường gửi sau dọn, với cả `firing` và `resolved`.
- **Ảnh hưởng và cách phân xử** Có thể mất chuỗi trong thời gian app dừng, rồi trạng thái kéo dài khi route thiếu request sau lúc khởi động. Chưa phân biệt được với khoảng trống do agent hoặc nhịp đánh giá quanh lúc bảo trì. So timestamp mẫu gốc Prometheus của bốn route và lịch sử luật trong đúng khoảng 16:29–16:40Z nếu cần định nguyên nhân của W4/W7. Chi phí ước vài phút truy vấn hẹp nếu kho còn lưu; nếu hết lưu chỉ giữ giải thích cạnh tranh. JVM lạnh cho bốn cảnh báo p95 vẫn là ứng viên. Không dùng các dòng bảo trì để suy tỷ lệ báo động giả.
- **Đề xuất sửa** Đính chính trình tự và phạm vi 14 dòng. Giữ kết quả Q4 về telemetry và giao nhận. Một lượt tải mới không thể xác định nguyên nhân của mốc lịch sử này.

### R7. Checkpoint và trạng thái chưa theo kịp phần việc đã xong — KHÔNG CHẶN dùng kết quả Q3/Q4/Q6

- **Ở đâu** `docs/STATE.md:13,41–44`, `TRANG-THAI.json:7,285`, kế hoạch §2, mục cuối LOG ngày 25–26/11.
- **Sai gì và bằng chứng** STATE vẫn ghi Q4 và commit/push chờ. Q4 có bản lưu hợp lệ, và Git local HEAD ở `ee16127` chứa Q4/chỉ mục archive. LOG đã ghi kết quả chạy, duyệt và đẩy. Checkpoint vẫn đưa bước tiếp về danh sách 23/11. I8/I9 trong HOP-DONG là đường cũ; kế hoạch §7.1 mới chỉ ra chương trình nào đọc từng STOP. Chênh này ảnh hưởng lần tiếp nhận thực tế và tiêu chí 3 của SPEC, có thể dẫn đến phát lại hoặc làm theo đường cũ.
- **Đề xuất sửa** Sau khi Minh duyệt chữ, ghi quyết định dọn trước W7 và trạng thái Q4 vào nơi có thẩm quyền, sau đó đồng bộ dòng T-070 và checkpoint với trạng thái dừng/lịch đã hoãn. Dẫn nơi có đường STOP hiện hành. Giữ kế hoạch và HOP-DONG gốc như hồ sơ lịch sử nếu thêm ghi chú tiếp nhận đủ rõ. Lựa chọn chỉ dựa vào LOG giữ được lịch sử nhưng không đáp mục đích checkpoint. A1/A2 và chữ D1 vẫn cần quyết riêng.

## Đối chiếu các lượt trước

| Điểm | Đánh giá | Bằng chứng sau triển khai |
|---|---|---|
| R1 lượt 1 | Đúng, đã xử lý ở phần đã kiểm | `truoc/buoc0.py` và `sau-buoc-3/sau_app.py` lấy trường chọn lọc và băm giá trị env. Hai bộ JSON kiểm là hiện vật đã qua manifest. Không rà hay hiển thị giá trị env. |
| R2 lượt 1 | Đúng về đường nạp; đúng một phần về giới hạn ghi | Blob `g1_export.py` giống bản cũ, cặp literal giữ, Q6 đủ ba JSON G1 và trạng thái đồ thị `ok`. R2 của lượt này ghi phần chốt vùng ghi còn thiếu. |
| R3 lượt 1 | Đúng | Đếm lại dưới `dev/service-graph` bằng `rglob('*.json')`: 109/218 file chứa UID cũ. Ba dashboard đổi file giữ UID và chỉ thay tên bộ, dashboard hệ thống tạo lại trùng. GET chỉ mục dev trên máy là 200. Chưa bấm giao diện trong lượt này. |
| R4 lượt 1 và N2 | Đúng | Cả `runs` hiện hành và archive đều ubuntu 700; cả hai vùng ledger đều ledger 700. SSH kiểm `sudo -n -u rca test -x` trên bốn cha trả 1. Phép sau bước 2 có kiểm hiện vật tồn tại. |
| R5 lượt 1 | Đúng về chiều đi | Lệnh bước 3 bật proxy trước app; `compose-dir` mới khớp nhãn Payment. `schema.cjs` vẫn là thư mục rỗng như chụp trước. Hoàn tác T-067 đã được Minh cho kết thúc theo LOG, phần nhánh tự động T-062 là R3 của lượt này. |
| R6 lượt 1 | Đúng | Helper vẫn quản tiến trình trần. Health đường hầm từ máy tải trả 200 và Q4 đã qua preflight. Chưa thử nhánh tự khôi phục khi tiến trình chết; đưa vào lượt sửa cơ chế nếu Minh thực hiện việc đó. |
| R7 lượt 1 và N1 | Đúng | So `truoc/obs.json#/venv_pip_freeze` với `sau-buoc-2/lenh-3-checkout-venv.out` khớp 18/18 dòng theo thứ tự và Python 3.12.3. Q3 dùng đúng đích mới/cờ từng ca. Hai lỗi của test hợp đồng cũ đã được khai và không dùng làm tiêu chí. |
| R8 lượt 1 | Đúng | So cấu trúc YAML cho 11/11 luật trùng sau khi đặt cùng tên nhóm/folder. Bộ nhận nhẹ chạy, nhận cả hai trạng thái. Q4 xác nhận T-072; bộ nhận trực tuyến T-073 hiện không chạy. |
| R9 lượt 1 | Đúng | SSH thấy `/opt/rca-tai` còn tại chỗ. Các mục app cũ tương ứng có README archive và bản chép. |
| R10 lượt 1 | Đúng; phản hồi lúc đầu về số lượng sai và đã đính chính | `git grep -l -E '/(opt\|srv\|etc)/rca-lab' 4b6c4b2 --` trong PowerShell trả 34. Hai cờ có bảng theo chương trình ở kế hoạch §7.1. Bản chụp còn cấu trúc mã task theo pin. Checkpoint cần sửa theo R7 của lượt này. |
| N3, N4 lượt 1 | Đúng | Lệnh mới giữ nhãn `t062=topology`; artefact ghi tên ảnh cùng nhãn cũ. Đầu `rules.yaml` ghi nguồn lịch sử; khác biệt cấu trúc chỉ nằm ở tên nhóm/folder. |
| PB1 lượt 2 | Đúng | File phủ Event vẫn không khai image. `hieu_luc.py` nạp file gốc cùng file phủ, kết quả lệnh tại `sau-buoc-3/lenh-3-hieu-luc.out` có 7 cấu hình. |
| PB2 lượt 2 | Đúng về chiều đi và điểm mâu thuẫn cũ | Lệnh dời thực tế sửa ba bind Keycloak; chỉ còn đường mới trong snapshot sau. Bản 3 chọn một đường lui khi còn quyền hoàn tác. Lượt này không diễn lại hoàn tác, đã được Minh cho dừng giữ đường lui theo LOG 23:40Z. |
| PB3 lượt 2 | Đúng | `lenh-4-bat.sh` chỉ bật `t072-bo-nhan`; live healthy. `q3-hoi-quy.sh` chuẩn bị cha ghi được trước khi user rca tạo thư mục ca. Snapshot nằm ngay dưới cây đích. |
| PB4 lượt 2 | Đúng | Hồ sơ `sau-don/k6-so-log.out` và X1, kèm Docker metadata: đã xóa 102 theo duyệt và còn đủ bốn ngoại lệ. Lượt này đối chiếu bằng chứng đã lưu vì Docker log của container đã xóa không còn đối tượng để so lại. |
| PB5 lượt 2 | Đúng | Cả hai pathspec hiện là `load rca inventory`. Tree trên ba máy sạch ở HEAD đã kiểm. R1 lượt này nằm ở danh tính tag, ngoài phép kiểm pathspec. |
| PB6 lượt 2 | Đúng | Q4 dùng chính đơn COMPLETED ở `kiem-tin-hieu.json#/luong_chinh`, đủ `mot_ve`. Q6 đối chiếu đủ từng mục thay vì chỉ `trung_tat_ca`; phạm vi bọc dữ liệu như dưới đây. |
| S3 và S4 lượt 2 | Đúng trong phạm vi triển khai | Dựng venv thành công theo log lệnh. `orchestrator` nhận đích qua `--ra` của người vận hành, mặc định bên trong là thư mục nhật ký, không tự chọn đích G1 như phản hồi mô tả. Giá trị đích mới ở lệnh Q6 hợp lệ. |

## Tuân thủ quy trình và phạm vi kết luận

- SPEC gốc của T-070 là điều phối, ghi “không chạy máy” và hạn chế ghi ngoài repo. Đợt dọn có duyệt bổ sung theo từng bước trong LOG 18:05Z, 19:00Z, 19:20Z, 19:40Z, 21:00Z, 22:05Z, 23:40Z và sau nửa đêm. Quyền sửa riêng AGENTS lab và các hunk ngoài B5 được ghi trước commit cuối. Quyền chạy Q4, xóa X1–X8, ghi chỉ mục và commit được cấp riêng. Chưa thấy bằng chứng thay đổi ngoài quyền đó trong phạm vi rà. Số **101** trong LOG là cây trước khi thêm AGENTS lab. Diff commit cuối là **102** mục, gồm 38 rename, 41 delete, 18 modify, 5 add, theo `git diff -M --name-status 4b6c4b2 85ace52`.
- Q4 dùng tiêu chí `tests/signals/tieu-chi.json#/buoc_7` có sẵn ở cả hai revision lab. Q3 dùng ca và chuẩn ghi trước. Q6 dùng capture, chuỗi Prometheus và gói bổ sung cố định, chạy chế độ `mot` từ mốc thủ công. Bằng chứng này chưa xác nhận nhận → gom → chờ flush → chụp live → xuất G1 cùng trong một ca ở commit mới. Q4 xác nhận bộ nhận nhẹ và tín hiệu sống, hai bằng chứng không nối thành một lần chạy W5. Nếu cần nghiệm thu tuyến sống ở revision mới, dùng đúng phép W5/W9a đã có khi Minh cho chạy; dự kiến tốn một lượt và cửa sổ chờ `t̂ + 600 + F`. Không cần chạy thêm để giải quyết các lỗi tĩnh R1–R5.
- Trong RCA batch, runner giữ tên ô và mốc tiêm ở sổ để chấm. `stage_m1.py` nhận mã mờ và thời điểm cắt gói; ở online, `incidents.py` lấy `startsAt`, còn `stage_b.py` nhận mã mờ và mốc đó, không dùng sổ. Trace/log lọc theo ns qua cửa sổ nửa mở, metric lấy theo bước 15 s. Adapter chuẩn hóa span, alias, log, metric rồi `run_m1.py` đưa bộ trường đầu vào xác định cho lõi và có kiểm trường/giá trị cấm. V082 chạy theo cấu hình ghim; H8a dựng lại đầu vào khi tuyến P7 gặp nhiều chuỗi runtime trong một metric logic, theo WHY-98/99 và `src/m1_ft/chay_ca.py`. `check_core_input.py` đối chiếu đầu vào lõi/cửa sổ. `sau_v082.py` sử dụng xếp hạng trong kết quả, `service_graph.py` dựng cạnh quan sát từ trace cho giao diện. Không thấy thay đổi mã chọn đặc trưng, tập ứng viên hay xếp hạng trong đợt này. Không mở dữ liệu khóa. Không suy rằng kiểm chuỗi nguồn hiện có giải quyết RQ3d hay RQ5.
- Rà riêng các hunk đặc quyền. `run_m1.py` đổi mặc định và chuỗi đường sổ cấm; pin và đầu vào thực dùng khớp trên ca Q6. `ledger_append.py` đổi gốc, cơ chế khóa ghi nối giữ nguyên; live kiểm quyền thư mục; chưa phát bộ batch mới để tạo sổ. `safe_export.py` có đích audit root 700 và catalog root 600 ở đường mới; `case` chỉ quét tập JSON/JSONL được chọn với catalog và dạng JWT, đúng phạm vi đã ghi trong code. Các chế độ `catalog`, `app-config`, `obs-config` vẫn dùng nguồn cũ theo ngoại lệ đã khai. Muốn dùng lại sau thay thông tin xác thực thì cần xác nhận đường nguồn và cập nhật catalog theo quyền được cấp. Nhánh `sau_v082.py --kiem-lai` còn hai nguồn cũ đã vắng trên obs, tình trạng đường lịch sử được khai; Q6 dùng nhánh kiểm khác. Không dùng hai nhóm lệnh lịch sử này làm bằng chứng vận hành hiện tại.
- Compose chính, Collector agent và bộ nhận không bổ sung cổng public trong diff. Mount đường dữ liệu, project và UID giữ theo phạm vi đã duyệt. Socket Docker của agent là cấu hình có từ trước. Kết luận an toàn ở đây giới hạn theo diff, cấu hình/metadata kiểm được và chốt ghi nêu ở R2. Không kiểm xâm nhập, không mở dữ liệu nhạy cảm để thử.
- Lý do giữ UID, cấu hình phương pháp, cửa sổ, ngưỡng và lớp hiển thị có thể lần theo kế hoạch và WHY. WHY-98 ghi rõ đã xem kết quả dev trước khi đề xuất V082, WHY-100 tách cạnh quan sát khỏi xếp hạng. Chưa thấy phương án nghiên cứu mới được quyết trước bằng chứng trong commit dọn. Phần chữ ghi quyết định thay thứ tự dọn trước W7 đang chờ như R7. Sai lệch mốc ở R6 là ví dụ cần sửa trước khi dùng hiện tượng cảnh báo để diễn giải nghiên cứu.
- Những đề xuất đổi mã ở R1–R5 ảnh hưởng commit lab và các lượt ghim revision. Không sửa trực tiếp file kết quả đã có manifest hay lock cũ. Với bản sửa đã duyệt, ghi commit mới ở hồ sơ lượt chạy mới. Nháp W7 mục khóa yêu cầu commit lab. Không dùng hash cũ để mô tả luồng mới. Sửa tài liệu Q4 cần giữ tệp dưới manifest làm hiện vật gốc hoặc cập nhật manifest theo đúng quyền Minh duyệt. Sửa trạng thái đi sau chữ quyết định.

## Điều đã kiểm và thấy đúng

- **Toàn vẹn.** Tính SHA256 trên byte của **143 mục** trong 8 manifest thuộc `don/` và `kiem-ke/`: tất cả khớp. So **22** bản chép `tu-lab/` với blob tag: tất cả khớp. README archive ba máy và bản lưu giống nội dung sau khi bỏ newline cuối; bản máy có thêm một byte xuống dòng cuối. Đây là so nội dung, không đánh đồng với SHA256 bản cục bộ.
- **Mã đã khóa.** SSH obs tính lại từ `rca/method.lock`: **149/149** file và **2/2** file P7 khớp. Đối chiếu blob RCA `25550d2a5` cho 123 trùng byte, 26 khớp sau đổi LF sang CRLF như khai trong lock. `git diff --quiet 74b2515 ee16127 -- src/m1 src/m1_ft src/p3` trả 0. Hai bộ `obs.json` khớp toàn bộ cây dev **3.676/3.676**, cùng bốn số mẫu kho trên cửa sổ đã khai. Q3 khớp hai đầu ra mỗi ca theo `q3-hoi-quy.out` và chuẩn T-066. Không chạy lại phương pháp.
- **Ứng dụng và kho.** HEAD ba máy là `85ace52`, cây sạch tại lúc đọc. Trên app còn 14 container đợt dọn đang chạy. Hai snapshot có 14 tên chung và một toxiproxy cũ đã dừng trong snapshot trung gian, rồi xóa theo X3. Số đơn theo trạng thái trong hai `app.json#/db_don` giống nhau; 11 hash env sau nằm trong tập trước dời. Bind quan trọng có log đối chiếu và đường đang dùng. Kiểm HTTP nhẹ trên obs: Prometheus/Tempo/Grafana 200. Loki lúc đầu báo chờ readiness, truy vấn số log API thành công và lần đọc sau readiness 200. Tunnel trên máy tải 200.
- **Grafana và bộ parser.** `git diff -M --check` đạt. Đọc cú pháp từ blob: 40 Python, 21 YAML, 10 JSON và 3 shell (`bash -n`). Dùng đầu ghi trong bộ nhớ cho đúng builder: chế độ `dev` tái tạo 4/4 blob triển khai, chế độ `online-*` đổi đúng ba dashboard phụ thuộc nguồn và giữ hệ thống. Tên bộ cũ được builder chấp nhận để dựng bộ lịch sử; archive phải được cấp ở đường phục vụ tương ứng nếu dùng lại. Không xuất file khi chạy builder kiểm.
- **Q4.** `k6-summary.json#/metrics`: 720 bắt đầu, 720 kết thúc, 3.317 request, tỷ lệ HTTP fail 0, p95 request mong đợi 535,55 ms. Số hành trình khác số đơn COMPLETED. `don-db.out` và `kiem-tin-hieu.json#/luong_chinh/db` cùng một đơn hoàn tất, một vé, một phát vé; P1–P6 và các trường kiểm trạng thái đều đạt. Mẫu chỉ là lượt ×1 mười phút.
- **Q6.** `q6/so-ca-cu.json` khớp 5/5 file gói, đầu vào P7, hai đầu ra V082, gói bổ sung và ba JSON G1 sau khi bỏ các trường mô tả đã khai. `q6/service-graph-60186b05.status.json` xác nhận đồ thị thành công. `q6/q6-chay.sh` xác minh đây là chế độ thủ công với ba nguồn dev cố định. Cấp đầu ra này đủ kiểm đổi đường nạp/xuất cho ca đã phát lại.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm.** Soát commit cuối, kế hoạch, các bằng chứng triển khai và kiểm chỉ đọc trên ba máy. Đối chiếu từng phản biện cũ sau tự soát.
2. **File thay đổi.** Chỉ `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-3.md`. Các hoạt động kiểm không phát tải, không tiêm, không sửa máy hay mở dữ liệu khóa. Không commit.
3. **Kiểm đã chạy.** Git, SHA256, parse cú pháp, tạo dashboard trong bộ nhớ, đối chiếu số trước/sau, metadata và HTTP GET chỉ đọc. Các kết quả và giới hạn nằm ở mục trên.
4. **Minh quyết.** Đề xuất **tiếp tục một lượt Claude đáp phản biện**. Giữ các kết quả đã kiểm. Ưu tiên R1 trước lần phát tải có lịch dùng lại; R2 và R5 trước bật trực tuyến; R3 trước dùng ô tái tạo Payment theo nhánh dự phòng; R4 trước build lại cùng revision; R6/R7 cho hồ sơ. Các phương án hẹp hơn và mặt trái ở từng mục. Các phép kiểm tĩnh sửa đường không đòi tải hay hồi quy diện rộng. Bất đồng trước về 32/34 đã phân xử. Hiện chưa có phản hồi mới của Claude. Cần Minh quyết riêng phạm vi sửa, chữ ghi sổ và nhu cầu chạy tích hợp mới. Đề xuất này không mở lại W7.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-070, tasks/T-070-dieu-phoi-giai-doan-2/. Kết quả đợt dọn repo lab và ba máy, kế hoạch bản 3.1.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giai đoạn 2, việc vận hành trước W7, ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-070.
- Tài liệu gốc: results/T-070/don/KE-HOACH-DON.md và các thư mục truoc, sau-buoc-2, sau-buoc-3, sau-buoc-4-5, q4, sau-don, tu-lab cùng SHA256SUMS, docs/ARCHIVE-INDEX.md, tasks/T-070-dieu-phoi-giai-doan-2/{SPEC,LOG,HOP-DONG}.md, TRANG-THAI.json và AGENTS.md của hai repo. Diff repo lab: git diff -M truoc-don-2026-11 85ace52.
- Phản biện và phản hồi trước: tasks/T-070-dieu-phoi-giai-doan-2/{REVIEW,REVIEW-2,REVIEW-3}.md. Kiểm cả các đề xuất và phương án khác được trình Minh trong bản lượt này.
- Code và kết quả liên quan: Lab D:/Project/flashticket-rca-lab tại 85ace52, tag trước dọn tại 4b6c4b2. Repo RCA tại ee16127, mã src/m1, src/m1_ft, src/p3. Nếu quyền chỉ đọc ba máy còn hiệu lực, dùng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs|tai với script qua stdin và sudo chỉ cho lệnh đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi riêng cho lượt đáp. Làm trong phiên này, không dùng subagent.

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
| R1 | Đúng; CHẶN phát lịch tải mới | `tai_linux.py` chỉ kiểm `test ! -e /srv/flashticket-rca/runs/<tag>` trên máy tải. `chuoi_tai.py:468` chỉ xem `load/tai-out/<tag>`. 47 tag cũ nằm ở `archive/2026-11/load-runs` và `load-tai-out`; container cũ đã xóa ở X1, nên không còn gì chặn việc dùng lại tag. Lỗi do đợt dọn sinh ra: trước dọn, tag cũ nằm ngay trong thư mục được kiểm. Sửa: kiểm thêm hai thư mục archive và tên container; lỗi đọc máy thì dừng, không coi là "chưa dùng". | |
| R2 | Đúng; CHẶN bật lại RCA trực tuyến | `g1_b.py:78` chỉ so `resolve(ra) == CAM_GHI` và tên cuối bắt đầu bằng `online-`. Vì vậy `/tmp/online-x` hay bất kỳ `…/online-*` nào cũng qua, mà tiến trình chạy bằng root. `khoi_tao` kiểu `chep:` chép từ nguồn tùy ý, giữ liên kết tượng trưng. Mẫu kiểm này có từ bản cũ (`t073-*`); L1 giữ nguyên mẫu, không làm chặt hơn. Sửa: đích chuẩn hóa phải là con trực tiếp của `/srv/flashticket-rca/rca/results`, tên `online-*`, không phải liên kết tượng trưng; nguồn `chep:` phải nằm dưới `rca/results`; kiểm sớm ở `orchestrator.py`. | |
| R3 | Đúng; CHẶN dùng nhánh dự phòng RECREATE-PAY | `inject.py:21` đặt `COMPOSE_CU` vào archive `compose-t062`; file đó dùng `../env-t062/<svc>.env`, mà 7 env đã chuyển sang `/opt/flashticket/env`. Nhánh dự phòng do tôi đặt ở bước 1 (để "giữ hành vi cũ") nhưng không chạy được. Sửa: bỏ nhánh dự phòng. Thiếu `compose-dir` thì dừng, báo rõ cần khôi phục gì. Có thể thêm đối chiếu với nhãn `config_files` của container trước khi tái tạo. | |
| R4 | Đúng; CHẶN dùng thư mục log làm bằng chứng build mới | Do thay đổi L ở bước 1: `build.sh:16` bỏ nhãn khỏi tên thư mục log. Hai nhãn cùng revision ghi đè `build-manifest.json` (dòng 48), log từng bước và `*.done` (dòng 80). Sửa: giữ worktree theo `<sha8>`, nhưng thư mục log theo lần chạy: `<sha8>-<nhãn>-<UTC>-logs`. | |
| R5 | Đúng; CHẶN chạy nguyên khối lệnh trong README | `rca/online/README.md:23` `cd …/observability/alert-receiver` rồi dòng 30 gọi `rca/online/orchestrator.py` theo đường tương đối. Lỗi do tôi viết ở bước 1. Sửa: dùng đường tuyệt đối `/opt/flashticket-rca/rca/online/orchestrator.py`. | |
| R6 | Đúng; KHÔNG CHẶN | `sau-buoc-3/lenh-1-dung.out`: gateway bị dừng 16:29:48–16:31:18Z; `deploy.tsv`: gateway lên lại lúc 16:38:32Z; `startsAt` là 16:32:00Z. Vậy cảnh báo bắt đầu cháy vì gateway bị dừng (không có mẫu mới), rồi kéo dài vì sau khi lên lại chưa có request vào 4 route. `q4/README.md` gán nhầm thời điểm bắt đầu cho lúc khởi động lại. 14 dòng: 5 dòng trước Q4 (lúc bảo trì), 9 dòng trong Q4. Sửa: đính chính trình tự và phạm vi 14 dòng trong `q4/README.md`. | |
| R7 | Đúng; KHÔNG CHẶN | Dòng T-070 trong STATE viết trước Q4 nên còn ghi "chờ Q4" và "commit/push". `TRANG-THAI.json` vẫn ở lịch 23/11. Sửa: cập nhật dòng T-070 (Q4 xong, đã push `ee16127`, còn A1/A2/D1) và `TRANG-THAI.json` (bước tiếp, đường STOP hiện hành ở kế hoạch §7.1). HOP-DONG giữ làm hồ sơ lịch sử, thêm ghi chú trỏ tới đường mới. | |

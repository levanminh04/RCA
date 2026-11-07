# Vận hành — ứng viên checkpoint013

Đọc [báo cáo013](runs/chuan-bi-main-013/bao-cao.md), [nội dung duyệt cuối](runs/chuan-bi-main-013/de-nghi-duyet-main.md) và manifest. Gói011/006 là lịch sử. Chuẩn bị013 đã được duyệt, G3/test/main/chấm chưa được cấp; mọi lệnh phát/nhận/chấm dưới đây chỉ dùng sau lời duyệt cuối đúng gói.

Từ `D:/RCA-flashticket`, kiểm manifest chỉ đọc:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/verify_manifest.py
```

Phân lô: EC2_1=16.176.181.251/key4,448job+2support,1worker; EC2_2=13.236.44.106/key3,450job,1worker; local742job,2worker tối đa. Mỗi EC230TT, toànOB/CIRCA/MicroRank/A ở laptop. Khóa SSH chỉ đọc từ `D:/RCA-ext/keys/`, không chép vào repo. Giữ strict host key/instance ID; không bật/tắt máy. Code=`checkpoint013/work`, data=`checkpoint013/data-root`, output=`work/results/T-054/runs/main-013/queue`. Python main trên EC2 phụ thuộc interpreter ở012: giữ012.

Sau Minh duyệt, người thực hiện (Claude từ 07/11/2026, theo `grants/minh-main.txt`) lưu nguyên văn lời duyệt ở `013/grants/minh-main.txt`, dựng grant thật `013/grants/main-grant.json` từ mẫu và ghi các quyền riêng theo đề nghị. Ghim protocol/source-bundle/manifest và nguồn quyết định; A giữ pin riêng. Nối DECISIONS/WHY/LOG và dòng STATE đúng quyền cuối; không sửa đầu ra chuẩn bị đã ghim. Minh không cần tự điền JSON. Dùng hash thật của file grant, không dùng chuỗi ví dụ dưới đây làm giá trị.

```powershell
$grant013 = 'results/T-054/runs/chuan-bi-main-013/grants/main-grant.json'
$grant013Sha = (Get-FileHash -LiteralPath $grant013 -Algorithm SHA256).Hash.ToLowerInvariant()
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/main.py --grant $grant013 --sha256 $grant013Sha
```

Entry kiểm toàn vẹn gói/tài nguyên/identity, tạo metadata LOCKED và attestation đầy đủ cohort, kiểm plan/union, stage đúng code và grant, kiểm môi trường cùng106file upstream/bản vá local, kiểm nguồn/chuyển đúng phân lô, materialize hardlink local rồi phát CLI ba máy. Truyền qua stdin với kê byte/hash, đích mờ; không đóng gói bản đồ thật/nhãn. Giữ biên nhận và đầu ra; bước lỗi không tự bỏ qua. Không tự gọi lại helper create-only khi đã có output dở: đọc receipt/queue trước, giữ lỗi và trình đúng sửa cần thiết.

Theo dõi `p7.py status --plan <activated-host-plan> --sha256 <pin-thật>` trên đúng host/root. Lệnh status chỉ đọc. Lần trả launcher_pid không chứng minh supervisor còn sống: kiểm status.controller và tiến độ/monitor. Mất SSH không nghĩa worker chết. DRAIN bằng `p7.py drain` với cùng plan/pin; giữ active đóng. Resume bằng `p7.py resume --plan ... --sha256 ... --authority ... --authority-sha256 ...` trên đúng runtime/host/root, một luồng số học như khi phát; đối chiếu PID/token trước, không retry hỏng hoặc phát bản sao.

Monitor poll0,1giây, maxgap<5giây, method600giây/C-d3=60giây; không trần cộng dồn, không tựretry. Theo dõi RAM/đĩa và nhóm ERROR/BLOCKED; thiếu nguồn, clock, mất monitor hoặc không tiến triển thì dừng/báo. Chưa chạy không gán TIMEOUT. TORAI A preflight nguồn theo grant, chỉ phát sau mọi non-A của laptop VERIFIED; thiếu quyền/sai pinA giữ BLOCKED, lỗi lạ dừngA và ghi phần chưa phát. Không bình quân A thiếu seed. Không sửa thiết kế sau dùng test; giữ kết quả đầu và khai riêng mọi bản sửa theo C-15 B.

Sau cả ba queue dừng và có đủ snapshot, nhận và chấm từ laptop (thư mục nhận mới):

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/receive_main.py --grant $grant013 --sha256 $grant013Sha --destination D:/RCA-flashticket/results/T-054/runs/chuan-bi-main-013/received-main-001
```

Helper giữ archive và bản nhận, xác minh receipt/seal, union đủ từng slot rồi mới đọc nhãn evaluator. A4 còn thiếu/chặn thì chưa tạo bảng; thiếuA ngoài A4 được khai trong bảng thiếu, không bình quân seed sống. Báo cáo ở `results/T-054/reports/main-013/`, D4 trong a4.json#/OB_group_description. Nếu bước nhận/kiểm/chấm lỗi thì giữ output, chọn tên lượt mới khi được phép sửa; không ghi đè report.

D3: main giữ AC sleep0, DC giữ hiện hành; chỉ khôi phục AC2700giây sau nhận/kiểm/chấm thành công. receive_main làm và ghi receipt. Nếu bị chặn trước đó, giữ máy thức, báo Minh; không tự khôi phục giữa lượt cần laptop. Không tạo ScheduledTask hoặc tựresume sau reboot. RE3 không thuộc grant main TT/OB. Commit/push chỉ sau Minh duyệt riêng danh sách đã rà, không dùng packet cũ có mapping thật hoặc archive/raw data.


Sau đáp review: xem review-response.md và manifest mới. Cả hai EC2 một worker, không dùng worker2 của bản trước sửa. WAIT_RESOURCE khi không có active có thể làm supervisor thoát; agent kiểm RAM/PID/token rồi resume cùng plan trong quyền main đã cấp, không tự đóng ứng dụng Minh hoặc retry slot hỏng. Dự toán toàn chuỗi có giả định; quyền cuối phải chỉ đúng bản metadata đã được kiểm lại.

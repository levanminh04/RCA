# L1 — đã hoàn thành phần bổ sung, chờ điều phối tiếp nhận

Codex là người làm T-062 phụ lục 2; Claude điều phối và phản biện. Đã thực hiện ba việc của `results/T-062/codex/L1-tiep-1-brief.md` và lời nhắn tiếp nhận 02:32Z. Không thêm quyết định nghiên cứu. Chỉ ghi trong tai-2/, codex/L1-* và nối ha-tang/thay-doi.md; không commit/push hoặc sửa tasks/docs/src, C1 cũ, repo FlashTicket.

Đọc trước: `BAN-GIAO-3-sau-bao-tri.md`, `bo-sung-1/bao-cao-bo-sung-1.md`, `bo-sung-1/buoc-tai.md`, `PROMPT-CLAUDE-bo-sung-1.md`. Manifest hiện hành: `bo-sung-1/manifest-bo-sung-1.json`. Manifest/source cũ được giữ lịch sử; không dùng pin cũ để kiểm source mới.

## Quyền và máy

D2 `d2b-2a7f481a` của Claude tự kết thúc 02:53:27Z, exit 0. L1 chỉ quan sát, không dừng/sửa container đó. Đã chờ máy tải trống mới cài tunnel và phát tải. Marker bảo trì xong 23:41:18Z đã có. App vẫn revision 6b21ed55. Trong lượt bổ sung, L1 chỉ đổi phần mock/tunnel được giao; không recreate container, đổi VNPAY, Collector, Toxiproxy, iptables hoặc bộ tiêm. Không đọc sổ tiêm, ô đánh giá, dữ liệu khóa; không chạy M1.

Mock PID 4038368, ở `/opt/flash-ticket-app/l1-vnpay/`. Kiểm cuối 03:14:29Z: mock sống, health từ AWS 200, pool 20 phiên còn hạn, quyền 0600. Không có k6 đang chạy. Cấu hình và state giữ nguyên qua phép thử restart; 3.027 dòng audit cũ giữ nguyên tiền tố.

Tunnel hiện hành: exp-app → AWS `127.0.0.1:19091` → mock exp-app `127.0.0.1:19090`. Supervisor PID 4037005; xem PID thực trong `tunnel-state.json`. Nó có session riêng trên app, parent 1 sau khi launcher đã kết thúc; SSH tự nối lại sau phép thử ngắt child. Không phụ thuộc tiến trình Codex/laptop. Khóa mới chỉ forward cổng loopback, private key chỉ ở app; kiểm lệnh từ xa bị từ chối. AWS nhận dòng public key hạn chế bằng append-only; không đọc `.ssh` hoặc khóa cũ, không mở firewall. Tunnel Windows của Claude giữ nguyên vì sandbox không xác minh được executable/start time của các PID đó.

`Test-L1Duong` kiểm/sửa đường trước mỗi chu kỳ. Hàm từ chối đổi token/tunnel khi còn workload hoặc bảo trì chưa xong. Start tự preflight và đăng nhập trước cửa sổ; VU refresh ở tuổi 200 s. Start tiếp theo sẽ cấp pool mới.

## Đầu ra đã kiểm

- `l1maint20261113a`, 300 s: 361 hành trình, 39/72 mua trọn, 33 lỗi tạo payment (19 × 504, 14 × 503), 0 dropped/401 k6. Cả 1.429 request k6 khớp gateway; 22 GET 401 ngoài workload được tách riêng. Đây là lượt lỗi thật, giữ đầy đủ.
- `l1step20261113a`, 240 s, bậc 120 s, ×3: 577 hành trình (145 chuẩn, 432 tăng), 117 mua trọn, 0 lỗi/dropped/401 k6. Cả 2.491 request khớp gateway; 25 request ngoài workload tách riêng. Nhịp gửi hai đoạn 120 s: 5,1333 → 15,475 request/s. Đỉnh hành trình đồng thời ở bậc tăng là 10, dưới giới hạn 20 VU mỗi scenario. Bảng 30 s và phần đuôi ở `bo-sung-1/buoc-tai.md/.json`. K6 dự phòng tổng tối đa 40 VU khi hai nhóm chồng trong gracefulStop; 40 phiên thuộc cùng 20 người mua.
- `l1maint20261113b`, 300 s: 361 hành trình, 72/72 mua trọn, 0 lỗi/dropped/401 k6, 20 refresh thành công. Cả 1.554 request khớp gateway; 30 GET 401 ngoài workload tách riêng. Chỉ chạy thêm pilot này sau khi lượt bậc sạch lỗi, khai lý do/chi phí trước ở `ke-hoach-kiem-lai-pilot.json`.

Các lượt giữ trên AWS và `out/<tag>/`, exit 0, không OOM. JSON/CSV/summary/console khớp; 36 mục hash đầu ra gốc khớp. 17 script PowerShell và 31 Python qua cú pháp; đã đọc diff 5 nguồn chính (276 dòng) cùng helper mới. Bằng chứng: `bo-sung-1/kiem-dau-ra-cuoi.json`, `kiem-cu-phap-cuoi.json`, `diff-nguon.txt`. Không chạy lại pilot/hai lượt 10 phút cũ còn hợp lệ.

Đơn sau bảo trì `f6dd8088-0f15-46a9-b666-3a6adc097b6d`: PENDING_PAYMENT → ISSUING → COMPLETED, 1 vé VALID, IPN 00, return 302. Mười trace liên quan có 6 PRODUCER + 6 CONSUMER. Dữ liệu: `bo-sung-1/giao-dich-sau-bao-tri.json`, các file log/Tempo và `kiem-span-sau-bao-tri.json`. Không tự phát traceparent.

## Điều còn mở

Nguyên nhân 33 lỗi 503/504 ở pilot a chưa phân xử. Trace 504 mẫu có gateway client tới 127.0.0.1:8083 kéo 25 s rồi cancelled trong snapshot truy vấn; 503 mẫu có ServiceUnavailableException, không có client downstream. Không gọi 503 là breaker mở chỉ từ status. Kiểm đọc sau đó: Eureka UP, cổng 8083 nghe, health trả 401 nhanh, container restart 0.

Cần điều phối đối chiếu discovery/connection/listener/worker/telemetry và thao tác trên máy đúng cửa sổ. L1 không tự đọc sổ tiêm hoặc sửa nghiệp vụ. Bằng chứng trong `CAN-DOI-PHIEU-PILOT.md`, `loi-pilot-chan-doan.jsonl`, `trace-loi-payment.jsonl`, `payment-discovery-trong-pilot.jsonl`. Pilot b sạch lỗi không xóa pilot a hoặc chứng minh cơ chế lỗi đã hết. R-04/R-09 toàn gói và chốt cấu hình thu chính vẫn thuộc T-063/Claude. Không bảo đảm qua reboot hoặc mọi mức lỗi từ phép thử khỏe này.

## Tiếp nhận

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Test-L1Duong
Start-Tai -Scenario hanh-trinh -Seconds 1800 -BuocTai 600 -Multiplier 3 -Tag <ma-moi> -May tai
Get-Tai -Tag <ma-moi> -May tai
Receive-Tai -Scenario hanh-trinh -Tag <ma-moi> -May tai
Stop-Tai -Tag <ma-moi> -May tai
```

Không có BuocTai thì Multiplier giữ nghĩa cũ. Rate trong nhánh hành trình là hành trình/10 s. Mốc bậc phải còn hạn refresh seed của scenario chờ; Start kiểm trước khi chạy. Không gọi hai Start đồng thời.

Bước tiếp: Claude đọc bàn giao 3 và prompt kiểm độc lập; kiểm manifest bổ sung, tiếp nhận đường tải vào runner; đối chiếu cửa sổ lỗi trong T-063. Không tự chạy lại đầu ra hợp lệ. Hoàn tác tunnel theo báo cáo, giữ state/audit/log; quản trị viên có thể thu hồi riêng key mới, không đụng key cũ.

Lệnh công việc cuối: kiểm ba bộ JSON/CSV/36 hash; Test-L1Duong và docker ps xác nhận máy trống, health 200, token còn hạn; sinh bàn giao 3, bảng 30 s và báo cáo. Lệnh đóng gói cuối: quét token/private key trên file mới/đổi, băm và kiểm manifest bổ sung. Không còn tiến trình thu cần chờ; chỉ mock/tunnel giữ sống cho chiến dịch.
## 2026-11-13T05:19Z - Linux transfer in progress
Read current checkpoint and approved appendix. New tai_linux.py and transport-only trien-khai-linux.ps1 deployed to exp-obs ~/rca-dieu-phoi; 10 pinned source files verified against repo and previous manifests. test-duong passed at 05:17:56Z: health200, mock alive, tunnel parent1, pool20 BUYER 0600 access287s refresh1787s. Detached kiem-linux.py now runs Linux 150s then 180s/step90/x3, get/receive/hash checks. No old PowerShell source changed; no app configuration changed. Read ~/rca-dieu-phoi/linux-check/result.json or error.json; keep both runs. Next: review negative checks, fetch results, compare saved PS and write BAN-GIAO-4-linux.md.

## 2026-11-13T05:25:16.2147485Z - Linux: xong lượt chuẩn, đang kiểm bậc

Đã nhận lượt l1linux20261113a: 180 hành trình hoàn tất, 36 đơn COMPLETED, 0 lỗi/401/dropped. 12 hash khớp; JSON/CSV/summary/log nhất quán; receive lặp giữ nguyên hash. Lượt l1linux20261113b (180s, bậc90 x3) bắt đầu 05:24:06Z. Driver độc lập PID94119 trên exp-obs, chỉ chờ get và nhận sau khi xong. Chín kiểm hợp đồng offline đạt, gồm từ chối hash sai, hạn seed và STOP. Thêm STOP trước mỗi SSH trong lúc lượt a chạy; giữ nguồn/pin v1 tại linux/, không đổi start/k6/cấu hình. Lượt b dùng nguồn cuối. Các nguồn PowerShell cũ vẫn khớp manifest. Kế hoạch so PS đúng thời lượng ở linux/ke-hoach-doi-chieu.json; chỉ phát sau khi Linux xong và máy tải trống. Không có lỗi hạ tầng cần làm lại.
## 2026-11-13T05:36:41.2315920Z - Linux xong kiểm tải; đang nhận lượt đối chiếu cuối

Hai lượt Linux l1linux20261113a/b hoàn tất, driver exp-obs PID94119 đã ghi linux/check/result.json (ok=true), dữ liệu đã chép thêm về out/<tag>/ trong repo. Lượt a: 180 hành trình, 36 mua, 773 gateway; lượt b: 433 hành trình, 88 mua, 1.869 gateway. Cả hai 0 lỗi/401/dropped, 24 hash khớp, gateway thiếu/lệch 0. Bản mã cuối thêm STOP trước SSH và xuất manifest qua .partial rồi rename sau khi tính đủ; giữ v1/v2 và pin, không đổi logic start/preflight/token/k6. Mười kiểm offline đạt. Giữ mọi log và lệnh từ chối trong linux/check/commands.jsonl.

PS đối chiếu l1ps20261113a đã xong: 181 hành trình, 36 mua, 779 gateway, 0 lỗi/401/dropped, 12 hash khớp. Khác 1 lượt xem tại t=150,001 s; Linux lượt xem cuối t=149,167 s; chênh thêm 3 lần poll. Lượt PS b đang kết thúc/nhận; tiến trình tool session39368 còn chạy, không dừng container. Chờ linux/ps-reference.jsonl có 2 dòng rồi chạy linux/thu-ket-qua-linux.ps1 để receive PS qua bản Linux, kiểm 4 bộ, đối chiếu flags Docker và thu nguồn triển khai. Sau đó viết BAN-GIAO-4-linux.md, báo cáo/manifest và kết thúc. Không sửa nguồn PS cũ, ứng dụng hoặc firewall.
## 2026-11-13T05:39:26.6861869Z - Kiểm ghép lệnh bị lỗi, đã sửa trước bàn giao

Lần đầu linux/thu-ket-qua-linux.ps1 dừng tại scp buoc-tai.json thiếu. Phía exp-obs chỉ có ps-a-receive.json; các lệnh sau receive chưa chạy. Cơ chế đã tái hiện bằng chương trình con cat: run() bản v3 kế thừa stdin, lấy phần stdin còn lại của caller. Sửa run() dùng DEVNULL khi không truyền input; vẫn dùng PIPE khi truyền mã/pool. Kiểm hồi quy giữ stdin caller đạt; 11 kiểm offline đạt. Không phát lại tải: cả bốn lượt chạy trong driver có DEVNULL hoặc PowerShell launcher, các container và raw/12 hash từng lượt đã hoàn tất hợp lệ; lỗi chỉ ở chuỗi kiểm/nhận sau đo. Đang chạy lại riêng bước thu/đối chiếu (tool session mới), giữ nguồn/pin v3 và dữ liệu cũ. Bằng chứng linux/check/stdin-regression.json sau khi nhận về.
## 2026-11-13T05:45:24.6601113Z - L1 XONG: chuyển bộ điều khiển sang exp-obs

Bàn giao hiện hành: BAN-GIAO-4-linux.md; linux/huong-dan-linux.md; codex/L1-linux-ket-qua.md; PROMPT-CLAUDE-linux.md. Source pin: linux-source-manifest.json; gói kiểm: linux/manifest-linux.json. Repo chỉ đổi các đầu ra đã được giao; không sửa tasks/docs/src, nguồn PowerShell cũ hoặc repo FlashTicket, không commit/push.

Bốn lượt Linux/PS cùng thời lượng đã xong và giữ ở out/<tag>/, trên máy tải và exp-obs tai-out/<tag>/. 180/181 hành trình ở 150s; 433/434 ở 180s bậc90x3. Mua36/36 và88/88; 0 lỗi/401/dropped k6, exit0, không OOM. 48 hash gốc khớp; gateway tất cả khớp, ngoài workload tách riêng. Config Docker và byte k6/cấu hình từng cặp bằng nhau. Chênh do lượt xem cuối tại biên ở PS và số poll được ghi cụ thể; không tự đặt ngưỡng chấp nhận. 11 kiểm offline và kiểm CLI ghép đạt. Lỗi stdin đã tái hiện/sửa, chỉ chạy lại bước nhận, giữ lịch sử nguồn/pin và collect-attempt-1.txt.

Không có lệnh tải nền còn cần chờ. Driver Linux94119 và các tool thu đã kết thúc; bốn container giữ ở trạng thái exited. Mock4038368 và supervisor4037005 tiếp tục phục vụ, kiểm cuối parent1/health200. Test-duong05:40:47Z cấp pool20 BUYER0600, token phải được kiểm/cấp mới khi chạy sau. EXP-APP-XONG cũ giữ nguyên; không đổi config app trong lượt Linux. Các tunnel/khóa hiện có giữ tại chỗ, không mở firewall. Lỗi pilot503/504 cũ chưa được giải thích lại, xem bàn giao3.

Bước tiếp: Claude kiểm hồ sơ và ghép tai_linux.py vào bộ điều phối trên exp-obs. Chạy `python3 ~/rca-dieu-phoi/tai_linux.py test-duong` trước chu kỳ; start/get/receive/stop theo hướng dẫn. Không phát lại bốn lượt đã hợp lệ. Không tự chạy M1/đợt thu. Lệnh cuối đóng gói: kiểm nguồn triển khai và hash, quét JWT/private-key/password JSON trên file mới/đổi, tạo manifest-linux.json. Kết quả scan và danh sách file nằm trong linux/.
## 2026-11-13T05:46:33.1354766Z - Trạng thái máy cập nhật

## Cập nhật ranh giới bàn giao

Sau khi cả bốn lượt L1 kết thúc và bước nhận/đối chiếu đạt, kiểm đóng gói lúc 05:44Z thấy container khác `rca-tai-t2-865c8e93` đang chạy. Start bản cuối từ chối vì máy bận; get lượt L1 cũ và stop với tag không tồn tại vẫn trả đúng một JSON, caller tiếp tục. Không dừng, sửa hoặc nhận dữ liệu của container mới. `linux/check/composed-cli.json` ghi đúng `idleCheckPassed=false`; máy không trống ở thời điểm kết thúc, bốn container L1 đều exited. L1 không còn phép đo nào chờ phát. Chủ lượt tải mới do điều phối xác nhận.
Lưu ý: câu không có lệnh tải cần chờ ở mốc trước chỉ nói bốn lượt L1; hiện máy có tải khác, không được chạy test-duong hoặc start cho tới khi trống.

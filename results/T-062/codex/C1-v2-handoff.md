C1 XONG MỘT PHẦN

Phiên C1 v2, kết thúc 2026-11-11 18:43Z. Đây là bàn giao phần việc đã làm, không nghiệm thu C1 hoặc T-062. Phiên v3 đang thực hiện cùng phạm vi; phiên này đã dừng ghi file dùng chung và thao tác thay đổi máy sau khi phát hiện ghi đồng thời.

## Đã làm và đã kiểm

- Đọc AGENTS, STATE, SPEC, LOG cuối và nguồn trực tiếp về mục tiêu MRP, DT18/cô, LESSONS, kế hoạch giai đoạn 2. Phạm vi ghi riêng C1 không cho sửa tasks/docs, nên không ghi LOG/STATE chung.
- AWS: cài Docker 29.9.3 từ apt chính thức và bật Docker/chrony; kéo k6 1.4.2, digest trong cấu hình. Image amd64 110775510 byte. Bằng chứng `tai/cai-dat-tai.txt` và lệnh `tai/cai-dat-tai.sh`. Không cài lại khi tiếp nhận.
- obs: chỉ tạo `/opt/rca-tai/`, các file thuộc phạm vi đó và container `rca-tai-version-01`, `rca-tai-validate-01`. k6 1.4.2 arm64 104820053 byte, cùng digest đa kiến trúc. Không sửa stack quan sát, iptables hoặc `/opt/flash-ticket-obs/`. Container kiểm đã dừng được giữ nguyên.
- Chrony: AWS last offset +0.000000239 giây, obs -0.000065233 giây, cả hai NTPSynchronized=yes. Nguồn `tai/cai-dat-tai.txt`, `tai/obs-thong-tin.txt`, mốc khoảng 18:36Z. Trên obs chỉ đọc đồng hồ.
- PKCE qua Python in-memory trên app thành công; token pipe trực tiếp qua SSH vào secret obs. Metadata TTL access 300 giây, refresh 1800 giây ở `tai/auth-metadata.json`. Không in mật khẩu/token vào repo, console hoặc command argument.
- API fixture đọc lại trực tiếp: một event; ba order buyer trả 200, state CANCELLED; ba route order/payment 200; ba route order/tickets 500. Nguồn `tai/fixture-doc-02.json#/checks`, 18:40:55Z. Không tạo đơn, vì đã tìm thấy đơn có sẵn. Không suy nguyên nhân của 500.
- Đầu AWS: 8081 HTTP 000/curl exit 7; 8080 HTTP 302/exit 0 (`tai/ket-noi-dau.txt`, 18:36:27Z). Cuối AWS: 8081 `/` HTTP 401/exit 0; 8080 `/` HTTP 302/exit 0 (`tai/ket-noi-cuoi-v2.txt`, 18:43:05Z). HTTP 401 chứng minh nối được, không chứng minh API healthy.
- Parse PowerShell bản Start/Stop/Receive lúc 18:40 không báo lỗi cú pháp. Bản trên đĩa sau đó được phiên khác thay đổi nên kết quả này không xác nhận bản hiện tại.
- `k6 inspect` trên obs: exit 107 ở environment guard; chưa kiểm thành công. Lệnh/container được giữ trong `tai/thay-doi-may-tai.md`. Không coi là đã kiểm k6 workload.

## File phiên này đã tạo hoặc ghi

Trong `results/T-062/tai/`: `c1.ps1`, `cai-dat-tai.sh`, `cai-dat-tai.txt`, `kiem-ket-noi.sh`, `ket-noi-dau.txt`, `ket-noi-cuoi-v2.txt`, `ket-noi.md`, `may-tai.md`, `CHECKPOINT.md`, `obs-tao-thu-muc.txt`, `obs-thong-tin.txt`, `obs-k6-version.txt`, `auth-metadata.json`, `doc-fixture.py`, `fixture-doc.json`, `fixture-doc-02.json`, `fixture.md`, `chay-tai.ps1`, `k6/workload-t062.js`, `k6/cau-hinh.json`, `k6/fixtures.json`, và nối `thay-doi-may-tai.md`.

Trong `results/T-062/codex/`: `C1-progress.md`, báo cáo này và prompt soát kèm theo. Các file dùng chung có thể đã được phiên v3 thay đổi; không ghi đè để khôi phục bản v2. Không commit/push, không thay đổi docs/tasks/src, không đọc data/locked hoặc sổ/nhật ký tiêm lỗi. STOP và A2-XONG đều chưa tồn tại ở lần kiểm cuối trước bàn giao.

## Vì sao dừng và phần còn thiếu

FACT: `workload-t062.js`, `cau-hinh.json`, `chay-tai.ps1` và helper C1 bị một phiên khác sửa trong khi v2 đang làm. Đường dẫn k6 đã đổi từ `/work/k6` sang `/scripts`, máy mặc định đổi sang tai. CHECKPOINT chung 18:40:14Z chỉ định C1-brief-v3 và C1-v3.log. Brief v3 trên đĩa nói phiên v2 đã dừng và giao AWS làm nguồn tải chính; thực tế v2 vẫn chạy đến lúc phát hiện xung đột. Không biết cơ chế khiến hai phiên cùng tồn tại; không giết tiến trình nào.

Khuyến nghị: giữ đúng một người ghi C1, tiếp tục ở phiên v3 đã được CHECKPOINT chỉ định. Giữ lại đầu ra cài đặt/đồng hồ đã có; đọc lại code/config hiện hành trước khi chạy, vì bản v2 và v3 không đồng nhất. Báo cáo `may-tai.md`, `ket-noi.md`, `fixture.md`, CHECKPOINT riêng và C1-progress là ảnh chụp v2, cần được người tiếp nhận đối chiếu với v3 trước khi dùng làm trạng thái hiện hành.

Chưa chạy 5 phút vì A2-XONG chưa có. Chưa có raw/summary hoặc tỷ lệ/p95/refesh/401 của tải để báo. Cần kiểm nền tickets sau A2; nếu vẫn lỗi, người điều phối xử lý hoặc quyết giới hạn, không tự đổi mixture hoặc sửa ứng dụng. Không có đủ bằng chứng kết luận C1 ổn định.

C1 chỉ là hạ tầng/read-mix trong T-062. Chưa hoàn thành chặng 2 nguồn: còn yêu cầu giao dịch đặt vé trong tải, hai lượt có lưu lượng gateway tương đương; chưa trả lời RQ5 hoặc đánh giá phương pháp. Không tự mở rộng lượt chạy.

## Lệnh E1 dự kiến

Chưa xác nhận chạy được với bản hiện hành. Phiên v3 cần kiểm xong rồi bàn giao:

```powershell
. ./results/T-062/tai/chay-tai.ps1
Start-Tai -May tai -Seconds 1800 -Rate 5 -Tag <ma-mo>
Stop-Tai -May tai
Receive-Tai -May tai -Tag <ma-mo>
```

Đầu ra dự kiến: `/opt/rca-tai/out/<ma-mo>/` trên máy chọn và `results/T-062/tai/out/<ma-mo>/` khi nhận. Không thực hiện các lệnh trên trong phiên v2. Bước tiếp: đọc brief v3 và code/config hiện tại, xác nhận một phiên ghi duy nhất, chờ A2-XONG rồi kiểm fixture và chạy thử theo brief. Lệnh thực thi cuối phiên: SSH AWS chạy `kiem-ket-noi.sh`, kết quả trong `ket-noi-cuoi-v2.txt`; sau đó chỉ đọc nguồn và ghi bàn giao.

Quyết định nghiên cứu mới: không có. Chưa khẳng định cơ chế của tickets 500. Không đề xuất commit trong lúc hai phiên đang thay đổi cùng đầu ra; người làm tiếp sẽ trình gói commit sau kiểm cuối.

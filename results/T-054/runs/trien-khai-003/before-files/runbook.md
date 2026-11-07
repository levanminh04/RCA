# Vận hành công cụ T-054 tại checkpoint

Trạng thái: công cụ và dữ liệu giả đã kiểm; chưa phát pilot thật, G3 hoặc test. Quyền mới của Minh cho triển khai nằm ở `authorization.json` và LOG phiên 2. Quyền test/SSH/materialize/commit không được suy từ quyền triển khai.

## Đã có thể kiểm lại

Python chính: `D:/RCA-ext/envs/T-014-main/Scripts/python.exe`. Chạy `-B` để không tạo cache ngoài phạm vi task. `p7.py preflight` chỉ kiểm code/môi trường/tài nguyên, không mở dataset.

`runs/trien-khai-001/operator-fixture.json` giữ ref/pin chính xác của plan giả đã diễn tập. Dùng ref này cho status/drain/resume/verify. Đây là queue giả đã hoàn tất; không phải queue dev/test.

```powershell
$fixture = Get-Content -LiteralPath 'D:/RCA-flashticket/results/T-054/runs/trien-khai-001/operator-fixture.json' -Raw | ConvertFrom-Json
& 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe' -B 'D:/RCA-flashticket/results/T-054/scripts/p7.py' status --plan $fixture.plan.path --sha256 $fixture.plan.sha256
```

Đổi `status` thành `drain`, `resume` hoặc `verify` trên cùng plan giả để diễn tập. `status` chỉ đọc. `drain` ghi yêu cầu ngừng phát mới; worker hiện tại đóng lượt. `resume` khởi supervisor ẩn, giữ plan/output root bất biến, kiểm identity/output trước nhận lại. Không dùng heartbeat cũ làm bằng chứng process chết. Reboot nhận tiếp thủ công; không có Scheduled Task. Worker/supervisor ghi stdout/stderr/events/phases/monitor và giữ attempt dở/lỗi.

`report` giả chỉ đóng snapshot phi khoa học. `report` thật đòi grant, đủ slot A4, mọi nguồn nhãn độc lập và plan chấm. Không có đường bỏ gate bằng báo một bảng khác trước. `protocol.json` đang CANDIDATE; không đổi trạng thái bằng tay để phát test.

## Bước tiếp nhận chính xác

1. Đọc LOG phiên 2, báo cáo `reports/tu-soat-001/bao-cao.md`, `pilot-plan.json`, `source-manifest.json` và manifest phiên. Kiểm pin trước dùng; giữ các lượt hỏng.
2. Nhận các quyết định/nguồn quyền riêng còn thiếu. Tách quyền code khỏi pilot, SSH/sync, map riêng, G3 và test. Không dùng một OPEN pha sau để trì hoãn phần code/fixture độc lập.
3. Ghim plan dev tối thiểu từ danh sách candidate/native refs: member/source/window/config/env/seed/timeout/partition/budget. Nguồn độc lập đối chiếu runtime, trước truyền tín hiệu phi nhãn vào API. Giữ guard v3 cho test. Không materialize private test trong bước chuẩn bị code.
4. Trước pilot thật, kiểm lại TORAI prep/method environment và provenance CSV, C-d3 sau main seal, đường phân loại lỗi theo chính sách Minh chọn. Cache prep chưa bật/tuyên bố parity. Lỗi/config/phase chưa rõ giữ BLOCKED.
5. Chỉ SSH/sync sau quyền đúng bước. Kiểm identity/host key và vùng lịch sử bằng tên/hash; không đọc raw OB trên EC2. Chỉ chuyển allowlist TT dev cụ thể; test/dẫn xuất test giữ local theo phương án cơ sở. Không tự bật/tắt máy hoặc sửa ACL.
6. Pilot đủ nhánh, parity nguồn và đo cold/warm/RSS cả cây/throughput/receive/score trước chốt worker và ETA. Khi chưa đủ ngân sách/máy/grant, ghi đúng WAIT. Không giảm ca/seed/vế để vừa giờ.

## Giới hạn của checkpoint

Source code cuối checkpoint được đóng gói đúng byte ở `runs/freeze-cong-cu-003/`; snapshot môi trường local là kiểm kê, không thay môi trường đã chạy đủ bundle. Test sources, nhãn riêng và RE3 chưa materialize. Chưa có plan thật đã duyệt để người dùng phát P7 bằng một lệnh. Công cụ timeout mặc định giữ BLOCKED khi chưa có chính sách/phân loại; không tự retry lỗi phương pháp hoặc chuyển lượt chưa chạy thành trượt.

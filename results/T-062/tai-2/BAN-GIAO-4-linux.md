# Bàn giao 4 — điều khiển tải trên exp-obs

Codex làm theo lời nhắn điều phối 13/11/2026 05:15Z. Đã triển khai `tai_linux.py` trong `~/rca-dieu-phoi/`, Python 3.12.3, thư viện chuẩn. Nguồn PowerShell tải cũ giữ nguyên. Không commit/push, sửa nghiệp vụ, đổi container ứng dụng hoặc mở firewall.

Năm lệnh `test-duong/start/get/stop/receive` trả một dòng JSON; lỗi trả exit khác 0. Start kiểm máy tải trống, cấp mới pool qua PKCE trên exp-app, kiểm hạn seed cho bậc tải, rồi dùng cùng image/script/cấu hình k6. Receive chép vào `~/rca-dieu-phoi/tai-out/<tag>/`, kiểm SHA-256 hai đầu và giữ nguyên bản xuất đầu khi nhận lại. Manifest chỉ hoàn tất sau khi tính đủ hash; bản dở dùng `.partial`.

## Kiểm thực tế

| Lượt | Giây / bậc | Hành trình xong | Mua COMPLETED + vé | Request gateway khớp | Lỗi hành trình / 401 / dropped |
|---|---|---:|---:|---:|---|
| `l1linux20261113a` | 150 / không | 180 | 36 | 773 | 0 / 0 / 0 |
| `l1ps20261113a` | 150 / không | 181 | 36 | 779 | 0 / 0 / 0 |
| `l1linux20261113b` | 180 / 90s ×3 | 433 | 88 | 1.869 | 0 / 0 / 0 |
| `l1ps20261113b` | 180 / 90s ×3 | 434 | 88 | 1.880 | 0 / 0 / 0 |

Nguồn số: [comparison.json](linux/check/comparison.json), `/runs/<tag>/totals`, `/purchaseCompleted`, `/gatewayMatched`; bảng theo route ở [comparison-routes.csv](linux/check/comparison-routes.csv). Cả bốn lượt exit 0, không OOM, thiếu/lệch gateway 0; JSON/CSV/summary/log nhất quán. Mỗi lượt 12 hash gốc khớp. Hai lượt Linux còn được nhận lặp và kiểm manifest không đổi. Bản sao giữ trên máy tải, exp-obs và `out/<tag>/` trong repo.

Gateway còn có lần lượt 16/15/19/19 request 401 ngoài k6, giữ riêng tại `/gatewayOutside` và log gốc. Số 401 bằng 0 trong bảng là bộ đếm `gateway_401` của workload k6.

Chênh Linux trừ PowerShell: −1 hành trình ở mỗi cặp, −6 và −11 request gateway. Log PowerShell có thêm một lượt xem tại 150,001s và 180,001s; Linux ghi lần bắt đầu cuối tại 149,167s và 179,723s. Mỗi lượt xem thêm tạo ba GET; phần chênh còn lại là 3 và 8 lần poll đơn. Đây là số đo thực, không nhận là lưu lượng trùng tuyệt đối và không đặt ngưỡng chấp nhận. Linux lượt b có 5 refresh thành công, PS b có 0; cả hai giữ ngưỡng tuổi token 200s, không có refresh thất bại hoặc 401. Metadata hạn seed và thời điểm refresh giữ trong từng bộ đầu ra.

Hai scenario bậc Linux có 109 + 324 lượt; PowerShell có 109 + 325. Đỉnh hành trình đang chạy là 5 ở bậc chuẩn và 9 ở bậc tăng, dưới 20 VU/scenario trong mẫu này. Không suy thành bảo đảm cho mọi điều kiện. Bảng 30 giây và phần đuôi nằm ở `out/<tag>/buoc-tai.json` và `buoc-tai-30s.csv`.

[docker-launches.json](linux/check/docker-launches.json) xác nhận từng cặp bằng nhau về image/imageId, command, sáu biến tải, user, network và mount sau khi thay tag bằng ký hiệu chung. Hash hai file k6 của cả bốn lượt khớp nguồn repo; pin ở [linux-source-manifest.json](linux-source-manifest.json).

`test-duong` cuối đạt lúc 05:40:47Z: health 200, mock PID 4038368 không phải khởi động lại, supervisor PID 4037005 có parent 1, pool 20 BUYER quyền 0600, hạn access tối thiểu 286s và refresh 1786s tại thời điểm kiểm. Đây không phải cam kết token còn hạn tại lúc người khác đọc báo cáo; Start luôn cấp pool mới. Bằng chứng [preflight-final.json](linux/check/preflight-final.json).

11 kiểm hợp đồng đạt, gồm hạn seed sát biên, pool 20/40, tham số Docker, từ chối receive đang chạy/hash sai, bảo vệ output bí mật, STOP, manifest dở và giữ stdin caller. Kiểm CLI tích hợp giữ tại [commands.jsonl](linux/check/commands.jsonl); mã lỗi 1 cho tag sai, bậc sai, máy đang bận, nhận khi đang chạy và tái sử dụng tag. Lệnh stop với tag không tồn tại không chạm workload khác.

## Lỗi đã sửa trong bước nhận

Lần thu đối chiếu đầu chỉ chạy tới receive PS a; bước sau không chạy, rồi scp báo thiếu bảng bậc. Nguyên nhân đã tái hiện: SSH con kế thừa stdin và lấy phần script caller chưa thực thi. `run()` nay đặt stdin `DEVNULL` khi không truyền input; mã hoặc pool vẫn truyền bằng pipe. [stdin-regression.json](linux/check/stdin-regression.json) giữ kết quả trước/sau; [collect-attempt-1.txt](linux/collect-attempt-1.txt) giữ lỗi. Đã chạy lại riêng bước nhận/đối chiếu bằng nguồn cuối và đạt. Không phát lại tải hợp lệ: driver tải vốn có stdin DEVNULL; logic start/preflight/token và k6 giữ nguyên, có đối chiếu AST ở `comparison.json`. Giữ nguồn/pin các bản v1–v3 trong `linux/` và trên exp-obs.

## Dùng từ bộ điều phối

```sh
cd ~/rca-dieu-phoi
python3 tai_linux.py test-duong
python3 tai_linux.py start --tag ma-moi --seconds 1800 --buoc-tai 600 --multiplier 3
python3 tai_linux.py get --tag ma-moi
python3 tai_linux.py receive --tag ma-moi
python3 tai_linux.py stop --tag ma-moi
```

Chờ `result.state.Running=false`; kiểm thêm `ExitCode` và số lỗi workload. Bỏ `--buoc-tai` giữ nghĩa multiplier cho cả lượt. Hướng dẫn đầy đủ, STOP và marker bảo trì tại [huong-dan-linux.md](linux/huong-dan-linux.md). STOP của bộ chạy mới nằm trên exp-obs; Python không thể đọc tín hiệu mới trên laptop khi mất mạng.

Chỉ ghi trên exp-obs trong `~/rca-dieu-phoi/`; không chép khóa hay ghi token tại đó. Nhật ký máy: [thay-doi-may.md](thay-doi-may.md), [tai-linux-events.jsonl](linux/tai-linux-events.jsonl), các file deploy/pin trong `linux/`. `EXP-APP-XONG` cũ còn nguyên; lượt này chỉ kiểm mock/tunnel hiện có và cấp pool, không đổi cấu hình app. Lỗi 503/504 của pilot cũ vẫn theo hồ sơ bàn giao 3, không được kết luận đã giải quyết từ việc chuyển bộ điều khiển.

Đã hoàn thành phần chuyển lệnh và phép đối chiếu được giao. Claude tiếp nhận bộ điều khiển vào runner trên exp-obs và đánh giá các chênh lệch đã báo. Không tự chạy đợt thu M1. Hồ sơ kiểm độc lập: [PROMPT-CLAUDE-linux.md](PROMPT-CLAUDE-linux.md).

## Cập nhật ranh giới bàn giao

Sau khi cả bốn lượt L1 kết thúc và bước nhận/đối chiếu đạt, kiểm đóng gói lúc 05:44Z thấy container khác `rca-tai-t2-865c8e93` đang chạy. Start bản cuối từ chối vì máy bận; get lượt L1 cũ và stop với tag không tồn tại vẫn trả đúng một JSON, caller tiếp tục. Không dừng, sửa hoặc nhận dữ liệu của container mới. `linux/check/composed-cli.json` ghi đúng `idleCheckPassed=false`; máy không trống ở thời điểm kết thúc, bốn container L1 đều exited. L1 không còn phép đo nào chờ phát. Chủ lượt tải mới do điều phối xác nhận.
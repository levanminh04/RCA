# T-033 — Checkpoint phiên 4

Chốt 2026-10-11T01:56:42.793817+07:00. Codex người làm, Claude phản biện. Phiên dừng do ngữ cảnh nén theo AGENTS §5a.2 và lời Minh. **Chưa khởi chặng tính mới, task chưa hoàn tất.**

## Bằng chứng và trạng thái mới

- `checkpoint.json`: hai lời duyệt nguyên văn, việc đã/chưa làm. Lời duyệt tổng 12 giờ xử lý và xóa đúng archive đã có hiệu lực; chưa sửa guard/ledger hoặc xóa archive. Chưa có quyền ghi hai dòng vào DECISIONS.
- `integrity-verification.json`: tự kiểm laptop PASS 825/825 file, byte và SHA khớp inventory; không thiếu/thừa. Metadata lịch sử bất biến trong handoff-manifest khớp. External-documents lịch sử không được coi là pin của docs hiện tại đang có sửa được duyệt của phiên khác.
- `remote-status.json`: SSH chỉ đọc lúc 2026-10-10T18:52:19.999080+00:00; không worker/tmux T-033. EC2 T-033 du 2791021314	/home/ubuntu/rca/T-033; archive 1395097600 byte còn nguyên. Không EC2 writes, không khởi worker, không xóa. Dung lượng trước/sau xóa chưa có vì chưa xóa.
- `script-reading-evidence.json`: ba script parse AST đạt; dict status lặp trong channel_context.py được người làm kiểm. `script-reading-notes.md` phân biệt chứng cứ người làm với báo cáo trợ lý chưa kiểm EC2. Ba script không đổi trong phiên.
- `scope-verification.json`: kiểm LOG chỉ nối, SPEC giữ hash lịch sử, chỉ dòng T-033 STATE đổi, script nghiên cứu không đổi. `manifest.json` khóa file checkpoint.

## Mức đạt và phần thiếu

Checkpoint-handoff-001 giữ nguyên bộ lõi/bổ sung và toàn bộ lượt lỗi; locator có core/FF/factorial/fixed. Hash bản nhận đạt không thay kiểm số/intermediates mới, không xác nhận cơ chế. `output-presence.json` lịch sử vẫn mô tả đầu ra cấp gốc; phiên 4 không tạo đầu ra nghiên cứu mới.

Chưa: ledger tổng mọi lượt hỏng/kiểm; sửa guard; xóa archive; tự đọc đủ ba script và sửa lỗi metadata kênh; fixture/pilot/rest độ trễ/kênh; khóa nhóm/đối chứng sau phân rã; đọc tay; tổng hợp. RQ2/P4/P6/G2 vẫn OPEN. Không có bằng chứng mới phân xử cơ chế/tín hiệu/onset.

Trần 4 GiB hiện chỉ tính đầu ra EC2 theo lời Minh. Không dùng combined storage trong README cũ làm trần hiện tại. Không dùng subtotal wall có status trong snapshot để mặc nhiên cấp giờ còn lại; phải dựng ledger đủ trước run mới.

## Bước tiếp chính xác

Minh mở phiên Codex mới với `prompt-next-session.md`; đó là prompt nối việc, không phải phản biện Claude. Đọc bản gốc và các notes trước hành động. Việc tiếp ngay vẫn là chuẩn bị/kiểm script và chặng tính EC2; **chưa chuyển sang đọc tay + tổng hợp**. Khi chặng tính đạt mới soạn prompt đó. Prompt Claude chính thức chỉ khi task hoàn tất.

Lệnh đọc trước ở laptop:

```powershell
Get-Content -LiteralPath results/T-033/scripts/nsigma_delay.py -Encoding UTF8
Get-Content -LiteralPath results/T-033/scripts/bocpd_delay.py -Encoding UTF8
Get-Content -LiteralPath results/T-033/scripts/channel_context.py -Encoding UTF8
```

Lệnh EC2 chỉ đọc trước sửa/chạy, rồi kiểm hash theo inventory/source/manifest và môi trường pin:

```powershell
ssh -i D:/RCA-ext/keys/keys.pem -o UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes ubuntu@3.107.246.249 'tail -n 20 ~/rca/T-033/trang-thai.txt'
```

Không gọi CLI delay hiện tại để chạy toàn lô: cần tự xác nhận/hoàn thiện pilot/rest, provenance/lifecycle và guard trong phạm vi đã duyệt, giữ bản cũ và hash hai đầu. Lệnh tính pilot chính xác chỉ ghi sau sửa/kiểm script đạt, không đoán CLI chưa có. Python EC2 pin `/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8`; native `/home/ubuntu/rca/T-025/src/baro`; adapter `/home/ubuntu/rca/T-025/repo/src/p3/`. Dữ liệu chỉ allowlist trong inputs/source.json đã hash.

## EC2 và Minh cần làm

Không có lượt chạy nền hiện tại; Minh có thể tắt laptop sau chốt. EC2 vẫn cần cho phần tính còn lại; giữ bật để phiên mới tiếp, agent không bật/tắt EC2. Chưa thông báo worker “đã ổn định” vì chưa có pilot mới. Khi kiểm pilot phiên sau phải báo CẦN GIỮ LAPTOP MỞ theo yêu cầu Minh.

Hai lời duyệt đã ghi nguyên văn LOG. Đề xuất nối nguyên văn thành hai dòng mới trong docs/DECISIONS.md, ngày 10/10/2026, nguồn lời Minh trong phiên 4; mã lấy từ file sau khi đọc lại lúc có quyền ghi. Phạm vi chỉ lưu quyết định, không thêm quyền/SPEC. Chờ Minh duyệt ghi sổ theo Luật 0; không chờ duyệt lại các việc đã được phép.

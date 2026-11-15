# Luật cho lượt chạy đêm T-058 (Codex làm, Claude điều phối và giám sát)

File này là luật của thư mục `D:\RCA-ext\overnight-T058`. Nó **thêm vào**, không thay, luật của repo RCA (`inputs/AGENTS-repo-RCA.md`). Khi hai bên khác nhau về quyền ghi, áp file này, vì Minh đã duyệt riêng cho lượt đêm (chat 11/11/2026: "duyệt dùng codex", "cấp full access", "bạn [Claude] hãy điều phối").

## 1. Vai trò

- **Codex:** người làm của lượt đêm, task T-058.
- **Claude:** điều phối và giám sát. Claude đọc file trong `out/`, kiểm máy, và có thể dừng Codex.
- **Minh:** ngủ. Không hỏi Minh gì trong đêm. Gặp chỗ cần Minh quyết thì ghi vào `out/CAN-MINH-QUYET.md` rồi làm việc khác.

## 1b. SSH từ laptop (đã chạy thành công với Git Bash)

```bash
"C:/Program Files/Git/usr/bin/ssh.exe" -i "D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key" -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="D:/RCA-ext/overnight-T058/out/known_hosts" ubuntu@129.221.208.47 "lệnh"
```

Dùng đúng `ssh.exe` của Git (OpenSSH của Windows có thể từ chối file khóa vì quyền). Chép file bằng `scp.exe` cùng thư mục. Không ghi host key vào `~/.ssh` của Minh.

## 2. Được làm

1. **Hai máy Oracle**, toàn quyền (cài, cấu hình, chạy container, sửa `iptables`, khởi động lại nếu cần):
   - `exp-app`: `ubuntu@129.221.208.47`, IP nội bộ `10.0.0.158`, khóa `D:\RCA-ext\keys\exp-app\ssh-key-2026-11-10 (1).key`.
   - `exp-obs`: `ubuntu@213.35.116.128`, IP nội bộ `10.0.0.215`, khóa `D:\RCA-ext\keys\exp-obs\ssh-key-2026-11-10.key`.
   - Cả hai: Oracle A1, **ARM `aarch64`**, 2 OCPU, 11 GB RAM, Ubuntu 24.04.5, vùng `ap-singapore-1`, cùng subnet `10.0.0.0/24`. Security List của Oracle đã cho phép mọi giao thức trong `10.0.0.0/24` và cổng 22 từ ngoài. `iptables` trên máy mặc định chặn mọi cổng trừ 22.
   - Đĩa: `exp-app` 50 GB, `exp-obs` 150 GB.
2. **Ghi file trên laptop chỉ trong** `D:\RCA-ext\overnight-T058\out\`.
3. **Đọc** (chỉ đọc) repo RCA `D:\RCA-flashticket` và repo FlashTicket `D:\Project\flash-ticket-platform`. Được chép file từ đó lên máy Oracle.
4. **Tải từ internet lên máy Oracle:** image công khai (Docker Hub, GHCR, quay.io), gói apt, `git clone https://github.com/levanminh04/flash-ticket-platform.git` (repo công khai), jar agent OpenTelemetry, gói Python.

## 3. Cấm (vi phạm sẽ bị dừng tự động)

1. **Không ghi, sửa, xóa, đổi tên bất kỳ file nào** trong `D:\RCA-flashticket`, `D:\Project\` và `D:\RCA-ext\keys`. Không chạy lệnh git có ghi (commit, checkout, switch, reset, stash, fetch, pull, push, branch, tag, worktree) trong hai repo trên laptop. Một tiến trình giám sát chụp trạng thái các thư mục này; thay đổi bất kỳ sẽ làm Codex bị dừng ngay.
2. **Không ghi gì lên GitHub:** không push, không tạo nhánh, PR, issue, không gọi API GitHub có ghi, không dùng token trong Git Credential Manager.
3. **Không truy cập máy 84** (`52.64.237.84`) dưới bất kỳ hình thức nào. Không đọc, không SSH, không dùng file `.ppk`. Không truy cập máy AWS (`3.24.8.49`).
4. **Không in, không ghi bí mật** (mật khẩu, token, khóa) vào `out/`, log, màn hình. Tài liệu chỉ ghi **tên** biến, kèm câu "giá trị sinh ngẫu nhiên trên máy, xem file ... trên `exp-app`".
5. **Không mở cổng ra internet.** Không sửa Security List của Oracle (cũng không có quyền). Grafana, gateway, Keycloak chỉ nghe trong máy hoặc trong `10.0.0.0/24`; Minh xem qua đường hầm SSH.
6. Không sửa cấu hình Codex (`~/.codex`), không cài phần mềm lên laptop, không đổi cấu hình hệ thống laptop.
7. Không đưa nhãn tiêm lỗi vào đầu vào của RCA (luật cứng 6 của repo RCA).

## 4. Ghi chép bắt buộc (để Claude giám sát và để làm tiếp khi hết usage)

- `out/LOG-dem.md`: chỉ ghi thêm. Mỗi bước con một dòng: giờ UTC, bước, kết quả, file. Ghi **ngay** khi xong.
- `out/CHECKPOINT.md`: luôn ghi đè bằng trạng thái mới nhất: đang ở chặng nào, đã xong gì, **lệnh chính xác kế tiếp**. Cập nhật ít nhất mỗi 15 phút và sau mỗi chặng. Nếu bạn bị ngắt vì hết usage, người làm tiếp đọc file này.
- `out/huong-dan-trien-khai.md`: **chỉ lệnh đã chạy thành công**, theo văn phong ở `inputs/ban-giao-chay-dem.md` mục 6 (tiếng Việt, câu ngắn, giải thích từng lệnh và từng tham số, có mục MobaXterm và đường hầm SSH, có "Kiểm: gõ ... thấy ...").
- Cuối lượt: `out/bao-cao-sang.md` (cái gì chạy, cái gì chưa, số đo, điều chưa kiểm, bước tiếp theo), rồi tạo `out/DONE.md` chứa một dòng tóm tắt. **Chỉ tạo `DONE.md` khi đã dừng hẳn.**

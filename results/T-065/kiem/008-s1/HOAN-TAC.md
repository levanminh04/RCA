# Hoàn tác S1 trên exp-obs

Lệnh dưới **chưa chạy**. Nó chỉ hoàn tác ba file của L10. Bằng chứng và nguồn phát hành local được giữ.

```powershell
& ([ScriptBlock]::Create((Get-Content -Raw -Encoding UTF8 results/T-065/kiem/008-s1/s1-ssh.ps1))) -Action rollback -OutputName hoan-tac-001.jsonl
```

Chạy từ D:/RCA-flashticket, khi Minh yêu cầu hoàn tác. Bộ gọi kiểm STOP local/home; script máy kiểm STOP remote, pin sau của mục lục, hai L4 ở đích mới, hai L8b và hai vị trí cũ phải vắng trước khi ghi. Nếu trạng thái đã khác thì dừng, không ép ghi. Lượt mới phải dùng OutputName chưa tồn tại.

Thao tác: chuyển đúng hai L4 về `RCA FlashTicket/1 · Kết quả hiện hành/` bằng tạo đích không ghi đè; khôi phục nguyên byte mục lục trước sửa đã ghim trong s1-may.py và đối chiếu `ban-truoc/t065-l5-muc-luc.json`. Giữ nguyên UID/byte hai L4. Không đổi provider/datasource/compose; không xóa folder rỗng. Grafana đã tự nạp trong lượt triển khai; sau hoàn tác kiểm API bằng lệnh dưới (chế độ before chỉ đọc).

```powershell
& ([ScriptBlock]::Create((Get-Content -Raw -Encoding UTF8 results/T-065/kiem/008-s1/s1-ssh.ps1))) -Action before -OutputName kiem-hoan-tac-001.json
```

Pin trước/sau: [hash-truoc-sau.json](hash-truoc-sau.json). Nguồn byte trước sửa: `ban-truoc/t065-l5-muc-luc.json`, `ban-truoc/t065-l4-rca.json`, `ban-truoc/t065-l4-phat-lai.json`. Không phục hồi manifest cũ lên hiện hành vì sẽ che lịch sử L10; mọi lần hoàn tác cần một mục LOG và manifest kế tiếp trong quyền được cấp.

# Hoàn tác S2 L12 — chưa chạy

Chỉ thực hiện khi Minh yêu cầu. Kiểm STOP local và remote. Dùng nguyên s2-may.py của L12 qua stdin SSH, mode rollback; không tải script hoặc tạo backup trên máy:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()
if ((Test-Path -LiteralPath 'D:/RCA-overnight/STOP') -or (Test-Path -LiteralPath "$HOME/rca-dieu-phoi/STOP")) { throw 'STOP local' }
Get-Content -Raw -Encoding UTF8 'D:/RCA-flashticket/results/T-065/kiem/012-s2-s4-u2/s2-may.py' | & 'C:/Program Files/Git/usr/bin/ssh.exe' -i 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key' -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts ubuntu@213.35.116.128 'sudo -n python3 -B - rollback'
if ($LASTEXITCODE -ne 0) { throw 'Rollback stopped; preserve output and inspect pins' }
```

Script GET cả hai UID, đòi pin live bằng pin sau L12, kiểm byte backup nhúng bằng pin trước, rồi phục hồi đúng hai file hiện hành. Không sửa dữ liệu hoặc file máy khác; không restart. Pin lệch hoặc GET chưa khớp thì dừng, không ghi đè thay đổi về sau. Nếu hết ba quan sát nạp, dừng ghi và chẩn đoán chỉ đọc; không coi assertion cuối là chưa ghi file.

Pin trước/sau và đường dẫn ở noi-dung-va-diff.json#/S2/dashboards; byte cũ độc lập ở ban-truoc/t065-l8b-rca.json và t065-l8b-phat-lai.json. Manifest trước nguyên byte ở ../../codex/manifest-L12-truoc.json.

Các tài liệu được nối không bị rollback máy tự động. Nếu Minh muốn hoàn tác phần local, phải đối chiếu đúng pin sau của từng file trong manifest L12 trước khi phục hồi từ ban-truoc/; không làm mất mục nối về sau. Giữ mọi transcript, ảnh, dữ liệu và LOG append-only.

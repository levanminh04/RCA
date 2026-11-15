# Hoàn tác L11b — chỉ thực hiện khi Minh yêu cầu

Trên exp-obs: `sudo python3 -B /opt/flash-ticket-obs/rca-ket-qua/t065-l11-001/codex/l11-may.py rollback`. Kiểm STOP trước; script GET ba UID, yêu cầu hash live bằng pin sau ở hash-du-kien.json, kiểm byte backup bằng pin trước rồi phục hồi đúng ba file bằng thay nguyên tử. Lệch pin thì dừng. Dữ liệu thư mục mới và mọi lịch sử vẫn giữ; không xóa. Sau hoàn tác chờ provisioning tự nạp, GET lại ba UID và đối chiếu hash/panel với byte trước. Không đổi compose/provider/datasource hoặc restart tự động.

Lệnh chưa được chạy. Nếu mất dữ liệu máy, byte trước nguyên vẹn ở ../ban-truoc/t065-l8b-rca.json, t065-l8b-phat-lai.json, t065-l5-muc-luc.json; kiểm hash rồi trình Minh thao tác phục hồi.

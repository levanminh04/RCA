# Bố trí đã thực hiện theo Q-47

EC2 mới 3.26.62.217/key2 dành cho DeepTraLog và LEMMA IT mẫu tại /home/ubuntu/rca-t003/{data,scripts,results}/. Nezha và Eadro ở laptop. Không dùng IP 3.104.124.160 của T-007. Báo cáo preflight cũ ec2-preflight-2026-10-03.json mô tả instance cũ, giữ lịch sử và không dùng làm năng lực máy mới.

Máy mới được kiểm SSH/df/free trước tải: root còn38.226.227.200byte, RAM8.153.149.440byte, không swap; bằng chứng trong LOG parent mục kiểm instance mới. Key2 đã sửa ACL theo quyền Minh, không ghi nội dung key. Host fingerprint của preflight chưa được đối chiếu qua AWS độc lập. Không cài môi trường RCA/training.

Các ZIP/CSV nguồn được giữ, kiểm bằng streaming; kết quả/script/hash chép về repo. [Dung lượng thực](dung-luong-tai-va-giai-nen.md) phân biệt logical expansion và dung lượng đĩa. Không tự dọn sau khảo sát, không mở Bank/locked. Chưa Stop/terminate EC2; Minh quyết thao tác dọn/Stop sau khi xem kết quả. Chi phí tiền thực cần AWS billing, chưa đo trong task.

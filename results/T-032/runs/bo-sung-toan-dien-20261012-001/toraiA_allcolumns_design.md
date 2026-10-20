# KT7 — Bổ sung mọi cột đóng góp, trước kết quả

Max-column probe không đại diện tổng điểm trace của dịch vụ. Bổ sung mọi cột còn lại trong `trace_lat_ranks`: dựng lại max absolute z theo mean/population std của N, chuẩn hóa trên toàn nguồn, cộng đúng các cột của service. Đối chiếu vector trace của root và chênh lệch trace/severity của mọi cặp đứng trên root trong nguồn A, seed0, toàn 30 dev. Không dùng phép so A với B để gọi sham đúng.

Nối mọi operation-column với cây span raw đầy đủ và đúng start-bin 15 giây của A. Lưu support, descendants và share từng cột; cột không nối được giữ N/A. Tổng share của cột có descendant-root chỉ là phần điểm từ operation có quan hệ quan sát, không phải phần điểm do chờ root. Bảng CSV đếm cờ nhưng không lưu danh tính span bật cờ; nếu chưa dựng lại chính xác encoder/threshold tác giả thì không gán mọi span cùng operation là flagged. Không suy nguyên nhân vật lý từ association.

Phần khai bổ sung nhằm trả lời service sum trong KT7, không thay bảng hoặc chạy lại TORAI/GMM/RCD. Kết quả trước còn nguyên. Ước 3–5 phút một core EC2, đọc dữ liệu dev tại chỗ, không chuyển dữ liệu lớn.

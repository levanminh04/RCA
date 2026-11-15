# Tiếp UI T-065 sau L8b

Đọc AGENTS.md, SPEC T-065 và mục cuối LOG/CHECKPOINT. Codex tiếp vai trò người làm; Claude phản biện. Quyền ghi giữ như brief L8/L8b: results/T-065 và nối LOG, không sửa nguồn T-064/docs/STATE/SPEC/REVIEW. Không tự đóng task hoặc mở test.

L8b đã kiểm dữ liệu/API và triển khai hai UID t065-l8b-rca/t065-l8b-phat-lai. Chưa bấm/ảnh Chrome trên hai UID mới. Đọc kiem/006-gc-cuoi/BAO-CAO.md và tom-tat.json; kiểm hash đúng phần sẽ dùng, giữ hồ sơ/lỗi và các lượt cũ. Không chạy lại M1/raw/API đã đạt khi nguồn/target không đổi.

1. Kiểm STOP local/remote, listener 13000 và tunnel do phiên trước để lại; không dừng tunnel khác. Nếu cần tunnel mới, dùng cách SSH đã được giao trong L7/L8, chỉ loopback 13000 tới exp-obs 10.0.0.215:3000. Không in khóa/mật khẩu; nếu cần login thì Minh thao tác theo quyền đã cấp.
2. Dùng URL ISO của chín tổ hợp trong kiem/006-gc-cuoi/mau-UI-con-lai.json. Mở tab riêng. Đổi bản cùng ca và kiểm giữ đúng mã ca/cửa sổ; đọc metadata/hạng/cờ/trạng thái cạnh. P7/ebd5ef38 phải hiện lỗi chạy và đường dẫn lỗi, không có hạng; V082 hiện không có đầu ra cạnh; V071 có bảng cạnh nguồn. Kiểm ô service là chuỗi service bình thường, ca lỗi có lựa chọn giải thích.
3. Theo luồng thực: ca → service → thao tác/graph → chi tiết → Tempo/Loki/Prometheus, tối thiểu ba ca mẫu. Đọc cửa sổ/query tại đích, giữ request/response/ảnh. Phát lại T-062 giữ tách đáp án; dev chỉ hiện giới hạn đáp án chưa cấp. Ghi rõ snapshot khác dữ liệu sống và không suy nguyên nhân query rỗng. Giữ các ảnh đang dựng/lỗi.
4. Dùng lại dữ liệu/API để đối chiếu, chỉ thu phần UI còn thiếu. Nếu phát hiện lỗi vượt phạm vi hoặc nguồn hash lệch, dừng phần phụ thuộc và ghi checkpoint. Chốt manifest, LOG và prompt chuẩn cho Claude sau lượt.

Chi phí chưa kiểm: khoảng 15–30 phút nếu Chrome/tunnel sẵn; đồ thị hoặc kết nối chậm có thể kéo dài. Có checkpoint theo từng tổ hợp; không lặp phần đã có bằng chứng hợp lệ.

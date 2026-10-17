# T-032 — Thiết kế phép đổi tất định, bản 006: nguồn log của TORAI B (chỉ RE2-TT)

Viết ngày 11/10/2026 (khoảng 00:55Z), trước khi chạy hai nhánh dưới đây. Người viết: Claude. Căn cứ: Q-131 mục 3 (các phép đổi thuật toán: ghi thiết kế chính xác vào file trước khi chạy, rồi triển khai) và kế hoạch mục 5 ("nếu cần phép đổi thì viết thiết kế trước"). Quy tắc chung ở mục 3 của bản 001 áp dụng y nguyên.

## 1. Điều tôi đã thấy trước khi viết

Toàn bộ `ket-qua-phien-10.md` mục 5: root mất hạng ở bước severity trong cả 4 ca TORAI B sai; nguồn log là nguồn nghiêng về thực thể kia nhiều nhất ở 7/7 cặp; riêng chênh log đủ đảo dấu chênh severity ở 4/7 cặp (2 ca), không đủ ở 3/7 cặp (2 ca); cột log có nền không đổi mang trung vị 55% điểm nguồn log; phép thử giả cho thấy hiện tượng có cả khi không có lỗi. Vì vậy hai nhánh này kiểm một ứng viên rút ra từ dev, không phải giả thuyết đặt trước.

## 2. Vì sao cần phép đổi

Phân rã cộng của severity cho biết chênh lệch nằm ở nguồn nào, nhưng bỏ hoặc sửa nguồn log sẽ làm đổi cả vectơ đưa vào bước phân cụm, nên hạng sau khi đổi không suy ra được từ phân rã. Muốn nói "bước chấm cột log có nền không đổi làm root mất hạng" thì phải đổi đúng bước đó và xem hạng.

## 3. Hai nhánh

Đầu vào của bước TORAI là bốn bảng mà lượt sham của `runs/torai-core-obs-001` đã tạo (lượt đó khớp bản đóng băng từng bit). Chỉ bảng `logts.csv` bị đổi, và chỉ bằng cách bỏ cột; giá trị các cột giữ lại không bị ghi lại dưới dạng số (chép nguyên chuỗi ký tự), ba bảng còn lại chép nguyên byte.

| Nhánh | Bước duy nhất bị đổi | Giữ |
|---|---|---|
| `tl2` | Bỏ các cột log không đổi ở 20 bin trước mốc (độ lệch chuẩn nền bằng 0). Đây là các cột mà bước chấm cho z bằng số đếm thô | Mọi cột log khác; metric, trace_lat, trace_err; chuẩn hóa, cộng theo dịch vụ, phân cụm, RCD, seed |
| `tl1` | Bỏ mọi cột log (nguồn log rỗng, như một hệ không có log) | Như trên |

Bước TORAI chạy bằng đúng worker native (`python -m p3.worker` trong môi trường py38), không qua lớp quan sát.

**Sham:** nhánh `sham` chép nguyên bốn bảng sang thư mục mới rồi chạy cùng đường; `ket_qua` phải trùng `ket_qua` của lượt sham gốc (`torai-core-obs-001`) từng bit. Lệch thì dừng.

**Phạm vi:** 30 ca, seed 0. Lý do chỉ một seed: trung gian trước RCD giống nhau giữa ba seed ở 30/30 ca và hạng root giống nhau giữa ba seed ở 30/30 ca trong lượt gốc; ba seed sẽ mất khoảng 70 phút máy. Giới hạn này ghi kèm kết quả.

## 4. Đại lượng (khai trước)

Với mỗi ca và mỗi nhánh: trạng thái; hạng root (rank_min, rank_max, tính theo nhóm trong khối như giao thức P3); tập thực thể đứng trên root; số cụm. Tổng hợp: Hit@1 và Hit@5 bi quan theo hòa; số ca root tăng, giữ, giảm hạng so với native; số ca đúng ở native bị mất hạng 1; số cột log bị bỏ.

## 5. Dự đoán đối lập

- **H-nền-hằng:** root mất hạng vì cột log có nền không đổi. Khi đó dưới `tl2` root lên hạng 1 ở ít nhất 2 ca (hai ca mà phân rã cho thấy riêng chênh log đủ đảo dấu), và không ca đúng nào mất hạng 1 vì lý do log.
- **H-khác:** dưới `tl2` hạng root ở 4 ca sai không đổi. Khi đó phần log còn lại, hoặc metric và trace_lat, hoặc bước phân cụm mới là nơi quyết định.
- `tl1` so với `tl2`: nếu `tl1` cho kết quả tốt hơn hoặc bằng `tl2` ở mọi ca thì nguồn log, như được dựng ở nguồn B, không giúp định vị root ở ca dev nào; nếu `tl1` làm mất hạng 1 ở ca mà native đúng thì nguồn log có đóng góp ở ca đó.
- Phải báo kèm số ca đúng bị hỏng đi ở từng nhánh.

## 6. Giới hạn

Đổi nguồn log làm đổi phân cụm, nên kết quả là tác động tổng của việc bỏ cột, không tách riêng bước severity với bước phân cụm. Bảng log là bảng của nguồn B do ta dựng (WHY-29); kết quả không nói gì về bảng log của tác giả. Không phải phương pháp mới, không thay số P3, không dùng để chọn cấu hình.

## 7. Nơi chạy và chi phí

EC2, tuần tự, 90 lượt con (30 ca × 3 nhánh), mỗi lượt khoảng 16 giây theo số đo của lượt quan sát: khoảng 25 phút.

## 8. Bổ sung: kiểm seed 1 và 2 (thêm lúc 01:12Z ngày 11/10, sau khi thấy kết quả seed 0, trước khi chạy)

**Điều đã thấy:** kết quả seed 0 của `runs/torai-log-contrast-001`. Ở ca `dev-a5cabe5fa7` dưới `tl1`, root và `ts-order-other-service` rơi vào cùng một cụm hai dịch vụ đứng đầu, và thứ tự trong cụm do nhánh RCD xếp; bước RCD dùng seed. Vì vậy kết luận "3/4 ca sai thành đúng dưới `tl1`" có thể phụ thuộc seed ở ca này.

**Phép kiểm:** với mọi cặp (ca, nhánh `tl2` hoặc `tl1`) mà ở seed 0 có ít nhất một khối do nhánh RCD xếp (chọn theo đầu ra, không dùng nhãn; 11 cặp), chạy lại bước TORAI trên đúng các bảng đã tạo với seed 1 và seed 2. Đại lượng: hạng root ở ba seed có giống nhau không. Script `scripts/torai_log_contrast_seeds_v1.py`. Khoảng 5 phút máy EC2.

**Cách đọc:** hạng root giống nhau ở ba seed thì kết luận seed 0 giữ cho cặp đó; khác thì báo từng seed và không gộp.

**Bổ sung lần hai (01:20Z, sau khi thấy lượt `torai-log-contrast-seeds-001`, trước khi chạy lượt 002).** Lượt 001 chọn cặp theo "có khối do nhánh RCD xếp ở seed 0" nên bỏ sót các cặp mà root nằm trong một cụm nhiều dịch vụ được xếp bằng nhánh dự phòng ở seed 0: ở seed khác RCD có thể trả đủ và đổi thứ tự trong cụm. Lượt 002 chạy seed 1 và 2 cho các cặp đó (9 cặp; việc chọn dùng nhãn root, chỉ để quyết chạy thêm seed nào). Script `scripts/torai_log_contrast_seeds_v2.py`. Với các cặp root nằm trong cụm một dịch vụ, hạng root không phụ thuộc seed vì seed chỉ đổi thứ tự bên trong cụm nhiều dịch vụ.

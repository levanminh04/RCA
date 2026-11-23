# Đề xuất gom việc — bản 5 (sau Codex CX-23b)

23/11/2026, điều phối T-070. Bản 5 = bản 4 (`de-xuat-quyet-2026-11-23-ban4.md`) + các sửa tối thiểu CX-23b (`results/T-070/codex/CX-23b-tin-cuoi.md`) áp nguyên ý. Điều phối không bất đồng điểm nào.

Ghi chú kỹ thuật: lần chạy CX-23b bị chuỗi tự động báo nhầm "hết usage" (bộ dò khớp chữ trong nội dung file Codex đọc); jsonl có `turn.completed`, kết quả hợp lệ; giữ `HET-USAGE.7-bao-nham-CX-23b.txt`. Các chuỗi sau chỉ coi là dừng khi thiếu `turn.completed`.

## Sửa so với bản 4

| # | Sửa | Nguồn |
|---|---|---|
| 5.1 | **Khôi phục B3:** Claude T-073 đáp CX-21/21b **ngay** phần có trên laptop (hai nhóm metric Payment, hai trang L4, mốc `fault-stop` là giờ lệnh, mốc 898,8/886,8 s, hash lưu trữ đến 02:05Z), soạn chữ WHY hai ngưỡng phủ (trình Minh duyệt chữ trước khi ghi), cập nhật LOG và dòng STATE T-073. Phần biên H5 và kiểm đầu vào V082 chờ file ca chép ở Q1. Hai lượt Codex kiểm phần đáp | CX-23b hàng 1 |
| 5.2 | **CX-24 thu hẹp:** Codex viết bản mới hai script + ca giả trong `results/T-072/v2/`, ghi đầu ra cùng hash của code thực chạy; ca giả bắt buộc: chuỗi `8,7,8` **không** đạt điều kiện duy trì `<8`; có/không giao khoảng hệ thống–quan sát; route thiếu → mã thoát ≠ 0 kèm tên route. Claude T-072 giữ `quy_ve()`, Pending, ca `t0+60`, **kiểm phần Codex viết trước khi tích hợp**; CX-24b chỉ là kiểm kỹ thuật. Nếu quy tắc đầu khoảng mới làm đổi phép chấm đã khóa → trình Minh. K1 giao T-072 (tác giả script ghi log trên exp-obs); T-071 giữ B2 | CX-23b hàng 2 |
| 5.3 | Đồng bộ `buoc_tiep` của T-071, T-072, T-073, T-074 trong `TRANG-THAI.json` đúng chủ việc và điều kiện chờ | CX-23b hàng 3 |
| 5.4 | Chỉ dẫn hash cho **cả Q6 (W8) và W9a**: không dùng chú thích "Hash do chỉ mục T-064 cấp" trên ca `t073-b`; hash đầu ra V082 của ca dẫn `#/du_lieu_loi/v082/output_sha256` trong bản ghi sự cố; trường hash đầu vào dùng lại là `null`. Giữ xử lý `live-down` trong kịch bản W9a | CX-23b hàng 4 |
| 5.5 | Thu hẹp mục xin duyệt: **Q8** chỉ xin duyệt thiết kế W6 bản 4 và phát E6/S5 (soạn đã có quyền, T-074 đang làm). **Q11** chỉ xin phần ngoài R2(b) hoặc hunk còn tranh chấp (R2(b) đã duyệt, điều kiện CX-05 đạt, push theo luật 11). **Q5** chỉ xin quyết định giữ/xử lý hiện vật; T-066/T-068 đáp phản biện và cập nhật dòng STATE của mình là quyền người làm. **Q10** chỉ ghi câu chữ Minh thực sự duyệt. Khuôn W8 trình trong chat được ngay; mở phiên T-075 vẫn chờ Minh | CX-23b hàng 5 |
| 5.6 | Nháp Q8: câu mở đầu đổi thành "độ trễ trung vị … cao hơn ở đợt đo thứ hai, khi bảng cũng lớn hơn" | CX-23b hàng 6 — đã sửa |

## Danh sách trình Minh sau sửa (thay bảng §2 bản 4)

Q1 (A1 chép file ca rồi hoàn tác, xóa thư mục rỗng theo UID), Q2 (nhận R5 và chức năng E5), Q3 (tên G1 `0.5 + che_do_b b-1`, duyệt chữ đính chính khi CX-26 soạn xong), Q4 (nghiệm thu T-069 với ngoại lệ CPU-BOOK-1), Q5 (giữ 2.6, chưa xóa 2.7; giữ nội dung bản hoàn tác T-068 và hiện vật ca `7ffb2305`), Q6 (W8 mức demo, kèm 5.4), Q7 (nhà cung cấp/model/danh sách trường; trước mắt chỉ khuôn ngoại tuyến), Q8 (duyệt thiết kế W6 bản 4 + phát E6, khi T-074 trình), Q9 (E7 trước E6 nếu W5, W8 sẵn và S4 đã trả), Q10 (ghi DECISIONS đúng chữ duyệt), Q11 (phần ngoài R2(b), nếu có). Nội dung chi tiết từng mục như bản 4 §2.

## Chạy ngay (trong quyền)

Codex lần lượt: CX-28 (liệt kê file R2(b), chỉ đọc) → CX-26/26b (chữ đính chính G1) → CX-25/25b (đính chính cơ học W4) → CX-24/24b (theo 5.2). Claude: T-073 phần B3 có sẵn (5.1); T-074 W6 bản 4 + nháp E6 (đang chạy); T-072 phần khó sau CX-24b; điều phối soạn SPEC W9a và khuôn W8 trong chat.

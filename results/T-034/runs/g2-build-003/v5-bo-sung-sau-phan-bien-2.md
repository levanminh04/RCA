# T-034 V5 — Bổ sung lần hai sau phản biện (lượt dựng `g2-build-003`)

Ngày 13/10/2026. Nối tiếp `runs/g2-build-002/v5-bo-sung-sau-phan-bien.md`; các bản trước giữ nguyên. Nguồn: lượt soát độc lập của Codex (trong chat), lượt đáp của Claude, lời Minh “duyệt sửa”.

## Đã sửa

| Điểm | Sửa | Ở đâu |
|---|---|---|
| R1: “bằng chứng nghiêng về lan không chiếm đa số” | Bỏ. Viết: chưa có căn cứ nói lan gây phần lớn ca sai, cũng chưa có căn cứ nói nó là thiểu số; tìm thấy cơ chế chấm khác ở BARO, CIRCA không loại vai trò của lan. Thêm số ca sai được sửa khi đổi thang của BARO | `goi-g2.md` mục 0, 4.2, câu 8 mục 7 |
| R2: UV-7 thành ràng buộc, UV-8 “phải kèm UV-7” | UV-7 tách hai phần: xử lý giá trị không hợp lệ là yêu cầu kỹ thuật; cách gộp điểm là ứng viên cần so. Ghi đủ ba biến thể và việc phép bỏ cạnh không cô lập bước cộng. UV-8 bỏ điều kiện bắt buộc | `goi-g2.md` mục 5 |
| R3: kết luận B-1 quá rộng | “Đã loại việc lọc cột hằng như nguyên nhân làm root mất hạng dưới quy tắc chấm hiện tại; bước lọc có bỏ cột của root” kèm số | Dòng G2-H09 |

Không số nào đã phát hành bị đổi; văn bản dùng thêm năm số có con trỏ nguồn. `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json` không đổi. V3 đạt; V4 đạt trên lượt này.

## Thấy khi soát lại, chưa sửa vì ngoài phạm vi đã duyệt

Dòng G2-H12, trường “Hiện tượng”, viết “DA chép điểm đó cho các nút cha”. Theo mã (`rht.py`, bước DA) thì bước này cộng điểm gộp của nút con vào nút có điểm vượt ngưỡng; chữ “chép” không chính xác. Cùng dòng, câu “chuỗi bằng chứng đủ từ đầu vào tới hạng” dựa trên phép bỏ cạnh, là phép không cô lập riêng bước DA. Trình Minh quyết.

## Ghi nhận

Ba lượt phản biện liên tiếp đều bắt được câu mạnh hơn bằng chứng do tôi viết. Tự kiểm của người viết không đủ cho loại lỗi này ở gói này.

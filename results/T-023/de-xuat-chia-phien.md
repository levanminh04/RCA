# T-023 — Đề xuất chia phiên Eadro-TT

Ngày 05/10/2026. **USER_CONFIRMED: Minh đã duyệt danh sách và quyền kiểm đúng 5 phiên/145 member, kèm B1.** Nguyên lời duyệt ở LOG phiên 2 và allowlist-phien.json; bản proposed trước duyệt giữ tại runs/approval-001/allowlist-before.json. Tài liệu này lưu phương án đã trình trước raw. Duyệt quyền kiểm không là kết luận dữ liệu dùng được trong thực nghiệm.

## Phương án trình Minh

Giữ đơn vị toàn phiên theo Q-63. Dùng lại seed 20261004 của T-021; sắp tăng SHA-256 của chuỗi `20261004|Eadro-TT|<session>` rồi lấy 3/9 phiên làm dev. Khóa chỉ chứa seed, dataset và mã phiên trung tính. Không dùng root, loại lỗi, vị trí đồ thị, độ phủ trace hoặc triệu chứng để chọn; không đổi seed sau kiểm số đo. Tỷ lệ 1/3 dev giữ đề xuất tỷ lệ ở `results/T-021/goi-g1.md` mục 4, chưa có bằng chứng đây là tỷ lệ tối ưu cho chia phiên. Hash/thứ tự đầy đủ chỉ nằm trong `runs/metadata-001/split-order.json`.

| Mã phiên giữ đúng như metadata | Phân bổ được duyệt | Sự kiện / root |
|---|---|---|
| TT.2022-04-18T150729D2022-04-18T165511 | dev, cho kiểm toàn phiên | 9 / 3 |
| TT.2022-04-18T165807D2022-04-18T184548 | dev, cho kiểm toàn phiên | 9 / 3 |
| TT.2022-04-18T184759D2022-04-18T203539 | dev, cho kiểm toàn phiên | 9 / 3 |
| TT.2022-04-17T212101D2022-04-17T230842 | test, không mở | 9 / 3 |
| TT.2022-04-18T102520D2022-04-18T121301 | test, không mở | 9 / 3 |
| TT.2022-04-18T121515D2022-04-18T140256 | test, không mở | 9 / 3 |
| TT.2022-04-18T203805D2022-04-18T222547 | test, không mở | 9 / 3 |
| TT.2022-04-18T222801D2022-04-19T001541 | test, không mở | 9 / 3 |
| TT.2022-04-19T001753D2022-04-19T020534 | test, không mở | 9 / 3 |
| TT.2022-04-21T105158D2022-04-21T130705 | reference — cho kiểm, tính đại diện cần bằng chứng | 0, faults=[] |
| TT.2022-04-21T153246D2022-04-21T174753 | control — cho kiểm, tính độc lập cần bằng chứng | 0, faults=[] |
| TT.2022-04-20T134450D2022-04-20T155957 | OPEN, loại khỏi danh sách đọc | không có nhãn riêng |

Reference/control được đề xuất theo thứ tự tên phiên trong hai nhãn rỗng, trước khi đọc số đo mới; không chọn theo accuracy hay độ sạch sau quan sát. Cho kiểm toàn hai phiên để đánh giá warm-up (giai đoạn khởi động), drift (trôi mức), tải và coverage (độ phủ). Quyền kiểm không đồng nghĩa đã chốt dùng toàn phiên để học ngưỡng P3. Nếu reference không phù hợp, trình Minh; không tự đổi vai trò hoặc đưa phiên thiếu nhãn vào nền.

Danh sách chính xác member, origin, byte và hash nguồn nằm trong **`allowlist-phien.json`**; hiện `status=approved`, đúng 5 approved_sessions/145 member. Mỗi record trace/log còn phải qua B1 trước đọc nội dung; quyền member không cho đọc nội dung có thể thuộc test/unlabelled. Bảng CSV là bản đề xuất metadata lịch sử, cột NOT_APPROVED phản ánh lúc tạo, không là nguồn quyền hiện tại. `runs/metadata-001/events.csv` giữ từng sự kiện, mốc gốc và giới hạn cửa sổ. Không dùng CSV chia ô T-021 cấp quyền raw.

## Phạm vi đọc đề nghị và chi phí

Đề nghị Minh cho kiểm metric/trace/log của đúng 5 phiên ở bảng: 3 dev và 2 no-fault. Có 145 member cuối, tổng logical payload 367.776.611 byte (~0,368 GB): 87 member outer của dev, 58 member trong hai TAR.XZ normal riêng. Đây là byte giải nén logic, không phải RAM hoặc đĩa sẽ ghi. Không giải nén toàn bộ ra đĩa. Nguồn: `runs/metadata-001/summary.json`, `member-map.csv`.

Không cần mở `TT-all.txz`: metadata đã xác minh 261 member telemetry nested fault trùng byte/hash outer. `TT-no-fault.txz` chứa phiên không nhãn và bị loại. Selector sau duyệt chỉ mở outer member dev và hai container normal cụ thể. Traversal container normal phải từ chối member lạ; không gọi `testzip()` trên toàn ZIP vì nó đọc cả test.

Ước lượng streaming/joins giữ 10–30 phút máy, RAM 0,5–2 GB, đĩa 0,1–0,5 GB theo SPEC: **chưa kiểm**. Giả định xử lý một phiên mỗi lần, chỉ lưu bảng kiểm gọn; có thể sai nếu trace lặp/conflict cần lưu nhiều hoặc join vượt RAM. Không tải thêm, không EC2. Đo thời gian từng bước; không chạy parsing nặng cùng pilot cost T-022. Nếu dự kiến một lượt vượt 1 giờ hoặc không vừa một phiên, báo Minh trước.

## Những giới hạn phải chấp nhận khi duyệt

- **FACT metadata:** 81 sự kiện, 27 root × 3 loại lỗi, 9 phiên fault. Mỗi root chỉ trong một phiên. Phương án có 27 sự kiện/9 root dev và 54 sự kiện/18 root test; root hai phía không trùng. Tập ứng viên của phương pháp vẫn lấy từ service quan sát/schema, không từ danh sách root. Phương án không kiểm khả năng lặp cùng root giữa dev/test.
- Ba phiên dev do seed chọn đều liên tiếp ngày 18/04. Đây không phải phép cân bằng ngày/tải/vị trí; tương quan giữa phiên và số đơn vị chia ít làm giới hạn suy rộng. Không đổi seed để đạt đồ thị hoặc triệu chứng thuận lợi. Chưa kết luận phủ mọi vị trí root.
- Trace và triệu chứng Eadro đã từng được khảo sát ở T-009/T-021. Test phiên mới không được gọi hoàn toàn chưa nhìn; chia phiên ngăn đọc mới chồng phía, không xóa mức tiếp xúc lịch sử.
- Mốc trước tiêm không chồng lần trước theo nhãn native chỉ có 2,687–124,484 s trên 81 sự kiện, đều dưới 300 s. Hai phiên faults=[] còn phải kiểm; nhãn rỗng không chứng minh sạch hay cùng tải. Nguồn số: `runs/metadata-001/events.csv` và `summary.json`.
- Tên phiên chỉ là định danh. Chưa được dùng thời gian trong tên để sửa epoch, suy múi giờ hay dịch trace/log. Clock và export lịch sử còn OPEN; kế hoạch kiểm ở `ke-hoach-kiem.md`.

## Sau lời duyệt

Quyền kiểm đã được Minh duyệt trước telemetry mới. B1 và giả thuyết cố định khai báo tại ke-hoach-kiem.md §8; kết quả thực kiểm ở kiem-eadro.md/bang-dieu-kien.csv. Phạm vi dùng cho T-027 vẫn phải trình Minh chọn; không tự chuyển nhánh hay ghi DECISIONS/WHY.

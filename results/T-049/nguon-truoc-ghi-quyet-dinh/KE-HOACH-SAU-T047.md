# Kế hoạch sau T-047

**Trạng thái:** kế hoạch đã chốt hướng. Không phải SPEC; mỗi task vẫn cần SPEC riêng được duyệt. Không mở G3 hoặc test.

**Chuỗi phụ thuộc chính:** T-048 → K-b → T6 → T9 → T11/T12 → KB → T13 trên cấu hình cuối. Không chạy chính thức hai task trên một nền còn có thể đổi.

**Phân công:** Codex làm T-048 đến T-051, Claude phản biện. T-052: Minh chưa chọn; đề xuất Claude làm, Codex phản biện.

## T-048 — thang điểm và tham số E4 trong cổng mới

**B0. Kiểm nguồn và máy chạy**
- Kiểm hash theo manifest; tái lập R0 với E4+S1, phải khớp T-047.
- Chạy thử để đo thời gian trên chính máy sẽ chạy: laptop, và EC2 hiện tại theo `data/README.md` (cấu hình máy chưa xác nhận).
- So khớp các trường đầu ra (thứ hạng, tầng, khóa, cờ) của cùng một cấu hình giữa hai máy. Nếu lệch, mọi cặp trong một phép so phải tính trên cùng một máy.
- Chỉ chép ca dev lên máy chạy; không đưa dữ liệu khóa ra khỏi `data/locked/`.
- Cache α là ứng viên tối ưu, chỉ dùng khi:
  - giữ nguyên mọi yếu tố ảnh hưởng tới p;
  - đã kiểm đầu ra tương đương với lượt chạy riêng.
  - Không trừ phần tiết kiệm vào dự toán trước khi đo.

**B1. T4: lưới ε × α (3 × 3) trên R0**
- Báo MRR, Hit@k, M5, N1, V0.
- Mặc định giữ ε, α hiện hành (SPEC T-043:761). Điều kiện để trình Minh đổi phải khai trước trong SPEC.
- **Chốt ε, α trước khi chuyển sang chọn thành phần.**

**B2. T4b vế (1):** kiểm công thức z trong cổng mới.

**B3. Phép so chính:** E4+S1 so với z+S1, ở R0 và ở E1+E2. Báo kèm z+S0.

**B4. Cơ chế**
- Khai trước các trung gian cần lưu cho từng ca và từng kênh: loại kênh (phân vị hay đếm), e của E4, z, m của T4c, bão hòa (rA = 1), khóa xếp hạng.
- Phân xử bốn giải thích: (i) E4 bão hòa, mất thông tin độ lớn; (ii) z lấn át kênh đếm; (iii) do cổng; (iv) ngẫu nhiên.
- Thiếu bằng chứng để phân xử thì trình phần cần bổ sung. Không suy nguyên nhân chỉ từ việc MRR tăng.

**B5. Luật quyết**
- Gọi luật C với `buoc='luat_C'`; E_X là cả 23 ô; không áp UV-6.
- Vế mốc giả ghi "không phân xử được do cấu tạo phép thử": z không đổi cờ hay số tầng 1.
- Tách ba phần: kết cục quan sát được, hành động theo luật, điều Minh quyết.

| Kết cục của z | Ở R0 | Ở E1+E2 |
|---|---|---|
| GIÚP | z vào đối chứng QT7 | Dừng, trình Minh đổi D24 → chạy lại khối K |
| HẠI riêng / HẠI gộp | Giữ E4 | Giữ E4 |
| TRÁI CHIỀU | Minh quyết; mặc định giữ E4, gắn cờ | Minh quyết; mặc định giữ E4, gắn cờ |
| KHÔNG TÁC DỤNG | Giữ E4, báo | Giữ E4, báo |
| KHÔNG ĐỦ CA (phụ thuộc quan sát) | Giữ E4, ghi "chưa phân xử" | Giữ E4, ghi "chưa phân xử", trình Minh |

**Chi phí:** Codex dự báo 4,5–6 giờ trên laptop, chưa đo. Trần do Minh đặt.

## T-049 — K-b và T6

- **Chuẩn bị công cụ:**
  - helper gọi đúng `khoi_K` hoặc `luat_C` theo từng bước;
  - sửa F1;
  - khai luật mặc định cho cờ trái chiều, tôn trọng mặc định riêng của từng thành phần;
  - E_X lấy từ T0, không định nghĩa lại sau khi nhìn số;
  - test hồi quy.
- **K-b (E2-VC):** báo theo từng ca ba trạng thái: định danh thật, không có đỉnh định danh, rơi về E2-C do vượt giới hạn (`src/m1/e2.py:35`). Nếu phần lớn ca rơi về dự phòng, không được gọi kết quả là "VC không giúp".
- **T6 (E3b):** lần theo chuỗi kênh tần suất → cờ và điểm → thứ hạng; đối chiếu ca được sửa với ca bị làm hỏng. Báo riêng số ô kích hoạt theo định nghĩa đã khai và số ca cơ chế thực sự tác động.

## T-050 — T9 và T10

- **T9:** phép chính E6a+S1 so với E6b; báo kèm E6a+S0 so với E6b (S1 chỉ áp khi dùng E6a, `src/m1/chuoi.py:566`).
  - Cơ chế: nút tham gia, cạnh có tác dụng, khối lượng điểm ban đầu, điểm sau lan truyền, nhánh dự phòng.
  - C-g, C-c chỉ báo cáo.
- **T10:** chỉ mô tả "vùng nghi ngờ" (`docs/MRP.md:271`): root có nằm trong vùng không, vùng rộng bao nhiêu. Đây là bản trung gian, sẽ cập nhật ở T-052.

## T-051 — T11, T12, KB

- **T11 ở nhánh chính:** E9 không tác dụng khi E5 tắt là đúng thiết kế (`src/m1/e5.py:174`). Ghi "không áp dụng".
- **Nhánh E5 bật (chỉ báo cáo; thêm vào ma trận đã đóng băng nên cần Minh duyệt):**
  - chạy E5, có và không có E9, có và không có cạnh tĩnh;
  - báo theo từng thực thể ba trạng thái của E9 (`khong_du_khoi_phat`, `da_xet_khong_phu_quyet`, `da_xet_phu_quyet`; `src/m1/e9.py:27`), và phủ quyết có đổi thứ hạng không.
- **T12:** báo riêng ảnh hưởng lên thứ hạng, lên vùng E7 và lên các đối chứng.
- Mỗi cặp so ghi rõ E5, E9 và cạnh tĩnh được giữ cố định ở trạng thái nào.
- **KB:** kết cục khác lúc chọn thì trình Minh, không tự đổi.
- **Hành động cho E5:**

| Kết cục | Hành động | Câu hỏi còn mở |
|---|---|---|
| GIÚP | Trình Minh đưa vào nền; nếu đồng ý thì kiểm lại các bước phụ thuộc | — |
| HẠI riêng / HẠI gộp | Bỏ khỏi bản P7 | Giả thuyết chưa kiểm: thiếu quan sát chiều mạng làm luật kế thừa áp sai. Phải nêu dữ liệu FlashTicket nào phân xử được và điều kiện bác bỏ; không mặc định collector sửa được giả định của phương pháp |
| TRÁI CHIỀU | Minh quyết; mặc định không bật | Như trên |
| KHÔNG TÁC DỤNG | Đề xuất bỏ, trừ khi E5 là phần cuối cùng còn đáp ứng DT18 | — |
| E5+E9 tốt hơn | Chỉ báo cáo; không tự cấp quyền đưa vào nền | Minh quyết có mở lượt chọn mới |

## T-052 — T13 và hồ sơ G3

- **Bỏ lần lượt từng thành phần đang bật** theo danh sách ở `src/m1/runner.py:149`; dùng lại kết quả KB nếu cùng nền.
- **Đối chứng:** C-a0, C-a1, C-d1–3, C-c, C-g, C-e, và z cho QT7.
  - C-a0, C-a1 là phép bỏ thành phần khỏi chuỗi đã chọn, không phải phương pháp không đồ thị được tối ưu độc lập (D23).
- **Bảng baseline:** cùng giao thức, cùng tập ca, cùng cách tính hòa và lỗi, cùng mẫu số. Cách đọc Q-62 do Minh quyết.
- **Vùng:** mô tả lại trên cấu hình cuối.
- **Hồ sơ G3** theo A4 và B6 (SPEC T-043).
- **Chặn G3, cần Minh quyết:** điều kiện `verdict`, chế độ (b), RE3-OB.
- Kết quả dev chỉ dùng để chọn và mô tả. Hoàn thành task không tự mở test.

## Chạy lại có điều kiện

| Nền thay đổi | Phải chạy lại hoặc kiểm lại | Còn dùng được |
|---|---|---|
| Đổi thang điểm | Khối K và mọi bước sau | T1, T4, phân tích cơ chế |
| Đổi ε, α | Từ T1 (nếu cờ đổi) và khối K trở đi | Phân tích ở cổng |
| Thêm E5 sau KB | T6, T9, T12, KB trên nền mới | K-b, nếu E2-VC không tương tác với E5 (**chưa kiểm**) |
| Chọn E6b ở T9 | Phạm vi T12; T10 trung gian | K-b, T6 |

Mỗi lần chạy lại là một task mới.

## Làm song song

| Khi đang làm | Việc làm song song được |
|---|---|
| T-048 chạy máy | Chuẩn bị công cụ cho T-049; soạn SPEC các task sau với nền để trống |
| T-048 đến T-051 chạy | Bảng baseline, C-c, khung T13, phần hồ sơ G3 độc lập (T-052) |
| Bất kỳ lúc nào | Quyết `verdict`, chế độ (b), RE3-OB |

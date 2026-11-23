# T-075 — Các điểm cần Minh quyết (Q7 còn mở)

Ngày 23/11/2026. Đây là đề xuất của người làm (Claude), **chưa kiểm** với model thật. Lượt này không gọi API, không gửi dữ liệu ra ngoài.

## 1. Danh sách trường gửi đi

**Đề xuất:** dùng đúng các khối `gui_di` ở `khuon-dau-vao.md` §3, và loại các trường ở §4.

- **Lý do:** đủ để giải thích dẫn bằng chứng ở mức demo. Không có nhãn, đường dẫn, trace ID, log thô hay giờ tuyệt đối.
- **Mặt trái:** vẫn gửi tên service, tên thao tác (có câu SQL, tên bảng, schema) và tên luật cảnh báo của FlashTicket.
- **Phương án nhẹ hơn:**
  - (a) bỏ `thao_tac_co_co`: mất chi tiết ở mức thao tác;
  - (b) thay tên service và thao tác bằng bí danh, rồi đổi lại ở máy: thêm một bước ánh xạ, có thể sai, và giải thích khó đọc hơn nếu đổi lại không trọn.

**Cần Minh:** duyệt danh sách, hoặc chọn (a)/(b).

## 2. Nhà cung cấp và model

| Phương án | Ưu | Mặt trái |
|---|---|---|
| A. Claude API (Anthropic), model `claude-opus-5-5` (mặc định hiện hành) hoặc `claude-sonnet-5-5` (rẻ hơn) | Có structured outputs ép đúng lược đồ JSON. Gọi trực tiếp, ít hạ tầng | Dữ liệu ra một nhà cung cấp ngoài (R3). Cần khóa API do Minh cấp. Chính sách lưu dữ liệu theo tài khoản, cần Minh xem |
| B. Claude qua Amazon Bedrock, trong tài khoản AWS đang có máy tải | Dữ liệu nằm trong tài khoản AWS của nhóm. Hóa đơn chung chỗ | Phải bật quyền model ở Bedrock và cấp IAM. Khả dụng theo vùng cần kiểm. Thêm thao tác trên tài khoản AWS (cần Minh duyệt) |
| C. Model mở chạy tại chỗ (laptop hoặc EC2) | Không gửi dữ liệu ra ngoài | Laptop không có GPU, chậm. Model nhỏ khó giữ đúng lược đồ và trích dẫn. Phải dựng thêm dịch vụ |
| D. Không gọi LLM khi demo; dùng câu giải thích sinh bằng khuôn cố định từ gói | Không rủi ro dữ liệu. Tất định | Không đạt W8 "LLM tối thiểu" nếu cô yêu cầu đúng là LLM |

**Đề xuất:** A với `claude-opus-5-5`, nhiệt độ mặc định, structured outputs, khoảng chục lần gọi trên ca W5 và các ca thử.

- **Lý do:** đi nhanh nhất tới "chạy trong demo", và lược đồ được ép từ phía API.
- **Khi Minh muốn dữ liệu ở lại tài khoản của nhóm:** chọn B.

Giá chưa tra lại cho lượt này. Ước lượng SPEC là "vài chục lần gọi", không đáng kể với mỗi phương án A hoặc B. Cần kiểm giá thật trước khi chạy.

**Cần Minh:** chọn phương án và model. Cấp khóa: Minh tự nhập vào biến môi trường; agent không nhập khóa.

## 3. Xử lý khi đầu ra LLM trượt bộ kiểm (chưa có trong SPEC)

**Đề xuất:** gọi lại một lần, kèm danh sách lỗi của bộ kiểm. Nếu vẫn trượt, trang ca hiện "Không đủ bằng chứng để giải thích tự động" cùng lỗi kiểm, không hiện câu chưa kiểm.

- **Lý do:** demo không bao giờ hiện câu bịa.
- **Mặt trái:** có thể không có giải thích ở đúng lúc demo. Mỗi lần gọi lại tốn thêm một lượt.

**Cần Minh:** duyệt cách xử lý, hoặc chọn không gọi lại.

## 4. File G1 của ca E5 `7577dd5b`

Gói E5 hiện dựng từ file sự cố. Nguồn này không có bằng chứng theo kênh, nên mọi đầu ra đúng ở ca E5 đều là `KHONG_DU_BANG_CHUNG`. Muốn có giải thích đầy đủ trên ca W5, cần file G1 của ca, gồm cả khối `che_do_b`. Q1 đã giao T-073 chép file này về laptop. Khi có file, chạy:

```
py -3 -I -X utf8 goi_bang_chung.py <đường dẫn file G1 của ca> g1 e5-g1
```

Sau đó viết lại đầu ra mẫu cho ca E5 (việc chưa làm, thuộc bước sau).

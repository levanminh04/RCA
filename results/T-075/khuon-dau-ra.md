# T-075 — Khuôn đầu ra W8 (`T075-ra-1`) và bộ kiểm

Ngày 23/11/2026. Bản 1. Bộ kiểm: `kiem_w8.py`. Prompt mẫu: `prompt-mau.md`.

## 1. Khuôn

```json
{
 "khuon": "T075-ra-1",
 "trang_thai": "GIAI_THICH | KHONG_DU_BANG_CHUNG",
 "xep_hang_nhac_lai": [["<thực thể nhóm hạng 1>"], ["<nhóm hạng 2>"]],
 "khang_dinh": [{"id": "k1", "loai": "quan_sat | suy_luan", "cau": "...",
                 "trich_dan": [{"con_tro": "/bang_chung/0", "gia_tri": "<tùy chọn>"}]}],
 "goi_y_xu_ly": [{"id": "g1", "loai": "kiem_tra | thu_them_du_lieu | giam_thieu", "cau": "...",
                  "can_cu": [{"con_tro": "/bang_chung/0"}]}],
 "thieu_bang_chung": [{"cau": "...", "trich_dan": [{"con_tro": "/thieu_trong_goi/0"}]}]
}
```

- `con_tro` là con trỏ JSON (RFC 6901) vào `gui_di` của gói. Không trỏ ra ngoài gói.
- `quan_sat` là điều đọc thẳng từ gói. `suy_luan` là điều nối các quan sát (ví dụ đọc quy tắc kế thừa). Tách hai loại theo luật cứng 14.
- `xep_hang_nhac_lai` chép lại ít nhất nhóm hạng 1, đúng thứ tự của lõi.
- `KHONG_DU_BANG_CHUNG`: chỉ có khẳng định `quan_sat`, không có gợi ý `giam_thieu`, và phải nêu phần thiếu.
- Được trả `KHONG_DU_BANG_CHUNG` cả khi gói đủ (thận trọng). Bộ kiểm cho qua, nhưng mục "thiếu" phải đúng sự thật (K4b).

## 2. Bộ kiểm (không gọi LLM)

| Mã | Kiểm gì | Lỗi bắt được |
|---|---|---|
| K1 | Khóa, enum; mỗi mục có ≥ 1 trích dẫn | Câu không dẫn nguồn |
| K2 | Con trỏ phân giải được; `gia_tri` khớp gói | Trích dẫn bịa, sai số |
| K3 | Tên thực thể trong câu có trong giá trị hoặc con trỏ được trích | Gán bất thường cho service khác |
| K3b | Số trong câu khớp số trong giá trị trích (theo số chữ số đã viết) | Bịa số |
| K4 | Gói không đủ (quy tắc tất định) thì đầu ra phải `KHONG_DU_BANG_CHUNG`, không `suy_luan`, không `giam_thieu`, có mục thiếu. `GIAI_THICH` phải trích `/bang_chung` hoặc `/ke_thua` | Bịa nguyên nhân khi thiếu tín hiệu |
| K4b | Mục thiếu trích nguyên khối `/bang_chung` hoặc `/ke_thua` thì khối đó phải rỗng | Nói "không có bằng chứng" khi gói có |
| K5 | Gói thiếu phủ cửa sổ thì phải trích `/do_phu` | Giấu việc dữ liệu thiếu |
| K6 | `xep_hang_nhac_lai` là tiền tố của nhóm hạng trong gói; câu "X hạng k" khớp gói | Đổi thứ hạng RCA |
| K7 | Không có mẫu chữ cấm (sổ tiêm, đường dẫn, tên lượt, dạng tên ô) | Rò nhãn vào câu |
| K8 | Gói sạch khóa/chữ cấm (chạy ở `chay_thu.py`) | Rò nhãn vào đầu vào |
| K9 | Hash file nguồn và bảng hạng nguồn trước = sau; bảng hạng trong gói = nguồn (`chay_thu.py`) | Lớp giải thích làm đổi thứ hạng RCA |

## 3. Giới hạn của bộ kiểm

- K3, K3b, K6 so chữ, không hiểu nghĩa câu. Câu có thực thể và số đúng vẫn có thể suy luận sai, ví dụ đảo chiều nhân quả. Chất lượng suy luận vẫn cần người đọc; SPEC để câu này OPEN.
- K6 phần câu chỉ kiểm câu nhắc đúng một thực thể cùng "hạng k". Câu nhắc nhiều thực thể không được kiểm hạng.
- K3 chỉ nhận ra tên có trong gói. Tên ngoài gói (ví dụ một service không có trong ca) không bị bắt. Phần này nên thêm danh mục service của hệ thống khi có LLM thật.
- K7 là danh sách mẫu, không đầy đủ. Mẫu dạng tên ô (`[A-Z]{2,}-[A-Z]{2,}`) có thể báo nhầm chữ viết hoa có gạch nối.
- Bộ kiểm chỉ quyết đạt/trượt. Chưa có cách xử lý khi LLM thật trượt (thử lại, hay hiện "không đủ bằng chứng" mặc định). Đề xuất ở `de-xuat-minh.md` §3.

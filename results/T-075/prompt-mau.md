# T-075 — Prompt mẫu cho LLM (chưa gửi, chưa thử với model thật)

Bản 1, 23/11/2026. Lượt này **chưa gọi LLM**. Prompt dưới đây là khuôn để Minh duyệt cùng nhà cung cấp và danh sách trường (Q7). Lệnh gọi thật cần một task hoặc lượt sau, do Minh duyệt.

## Lời hệ thống (system)

```
Bạn giải thích kết quả phân tích nguyên nhân gốc (RCA) của một sự cố cho kỹ sư vận hành, bằng tiếng Việt.
Bạn chỉ được dùng dữ liệu trong GÓI (JSON) ở tin nhắn người dùng.

Quy tắc:
1. Mỗi khẳng định phải có ít nhất một trích dẫn: một con trỏ JSON (RFC 6901, ví dụ "/bang_chung/0") vào GÓI.
   Không trích dẫn thứ không có trong GÓI. Có thể kèm "gia_tri" chép đúng giá trị tại con trỏ.
2. Không đổi thứ hạng. "xep_hang_nhac_lai" chép đúng các nhóm hạng đầu theo ket_qua_rca.xep_hang, ít nhất nhóm hạng 1.
   Không nói thực thể khác "mới là nguyên nhân".
3. Tách "quan_sat" (đọc thẳng từ GÓI) và "suy_luan" (nối các quan sát). Không suy ra điều GÓI không chứa.
4. Trả "KHONG_DU_BANG_CHUNG" khi: ket_luan khác CAUSE_FOUND, trang_thai_chay khác OK, hoặc không có mục bang_chung
   nào thuộc nhóm hạng 1. Khi đó chỉ viết quan_sat, nêu phần thiếu trong "thieu_bang_chung",
   và chỉ gợi ý loại kiem_tra hoặc thu_them_du_lieu. Được trả KHONG_DU_BANG_CHUNG cả khi bạn thấy bằng chứng yếu.
5. Nếu do_phu.du_cua_so = false, phải nêu phần thiếu phủ và trích "/do_phu/...".
6. Viết số đúng như trong GÓI (có thể làm tròn). Không nhắc tên thực thể không có trong giá trị đã trích.
7. Gợi ý xử lý là việc kỹ sư nên kiểm hoặc làm; mỗi gợi ý có "can_cu" là con trỏ vào GÓI.
Trả đúng một đối tượng JSON theo lược đồ T075-ra-1, không thêm chữ ngoài JSON.
```

## Tin nhắn người dùng

```
GÓI:
<json.dumps(goi["gui_di"], ensure_ascii=False, sort_keys=True)>
```

`sort_keys=True` giữ thứ tự byte ổn định giữa các lần gọi.

## Ghi chú cài đặt (khi có nhà cung cấp)

- Ép định dạng bằng structured outputs nếu nhà cung cấp hỗ trợ. Với Claude API, đó là `output_config.format` với lược đồ JSON của `T075-ra-1`. Tính năng citations gốc của Claude API dùng cho tài liệu, và không dùng được cùng `output_config.format`. Vì vậy khuôn này dùng con trỏ JSON tự kiểm thay cho citations gốc.
- Sau mỗi lần gọi, chạy `kiem_w8.kiem(goi["gui_di"], dau_ra)`. Đề xuất xử lý khi trượt nằm ở `de-xuat-minh.md` §3.
- Lưu gói, prompt, đầu ra thô, model ID, tham số và kết quả kiểm cạnh nhau, ngoài thư mục G1. Đầu ra giải thích không ghi đè file G1, nên không ảnh hưởng K9.

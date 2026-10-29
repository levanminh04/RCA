# Thẻ đọc sáu bài (T-043, bước 1)

Mỗi thẻ ghi: cơ chế, đầu vào, phần ta có và thiếu, điều kiện thất bại, chỗ đổi trong B2 của SPEC. Trang và dòng mã dẫn theo bản đã đọc. Thẻ diễn giải bằng lời; không chép nguyên văn.

| Thẻ | Bài | Phục vụ | Bản đã đọc |
|---|---|---|---|
| [petshop.md](petshop.md) | PetShop (CLeaR 2024), mã baseline Traversal | C-d3 | GitHub `amazon-science/petshop-root-cause-analysis`, commit `2e96f937c4c044b8b4aad03217592cd52e66db5d` |
| [crisp.md](crisp.md) | CRISP (USENIX ATC 2022) | E1-CP, cách cắt span con của E1-U | PDF USENIX, tr. 659–661 |
| [tracediag.md](tracediag.md) | TraceDiag (ESEC/FSE 2023, industry) | E1, E5, E7 | arXiv 2310.18740 |
| [prism.md](prism.md) | PRISM, "Graph-Free Root Cause Analysis" | C-h | arXiv 2601.21359v1 |
| [diagmlp.md](diagmlp.md) | DiagMLP | C-a0, C-a1 | arXiv 2501.02766 |
| [microhecl.md](microhecl.md) | MicroHECL (ICSE-SEIP 2021) | B1.4, E2, E5, E7 | arXiv 2103.01782v1 |

**Cách đọc.**
- Mã PetShop đọc bằng WebFetch tới file raw trên GitHub. Công cụ không trả mã nguyên văn, nên tôi hỏi theo cấu trúc: dòng của từng hàm và từng bước xử lý.
- Năm PDF lấy bằng WebFetch. Công cụ tự lưu PDF vào thư mục `tool-results` của phiên Claude, ngoài repo (ghi ở LOG phiên 7). Văn bản trích bằng `pypdf` 5.1.0 (môi trường `D:/RCA-ext/envs/T-016-cong-cu`), chạy trong bộ nhớ.
- Hành vi `networkx.all_simple_paths` khi nguồn trùng đích kiểm trên NetworkX 2.8.8 đã cài ở `D:/RCA-ext/envs/T-014-main` (`simple_paths.py:242–243`; gọi thử trả danh sách rỗng). Đây cũng là bản PetShop ghim.

**Các bài khác của KS-14** giao về nơi dùng theo SPEC B6:
- OTel messaging semconv → hạ tầng và E8.
- Urbano, FDA → A4.
- CNSS, GRLIA, DiLink → nhánh G/H.
- TraceContrast, MicroDig, OpenRCA 2.0 → tham khảo.

T-043 không đọc các bài này.

**Phát hiện khi đọc, ảnh hưởng tới văn bản SPEC (không đổi thiết kế):**
1. SPEC dẫn `requirements.txt` của PetShop. Ở commit đã ghim, file nằm ở `code/requirements.txt` và ghim `networkx==2.8.8`; nội dung khớp điều SPEC ghi.
2. SPEC dẫn "MicroHECL §IV.C" cho B1.4, E2, E5, E7. Trong bài, §IV.C là chiến lược tỉa bằng tương quan. Hướng lan theo loại bất thường (Bảng I) và quy trình chuỗi lan nằm ở §IV.A; phát hiện theo cạnh ở §IV.B; xếp hạng bằng tương quan ở §III. Thẻ đọc cả §III–IV.
3. Bảng I của MicroHECL xếp lưu lượng (QPS) lan **từ trên xuống**, tức cơ chế "tải vào". B1.4 xếp "tần suất tăng" vào lớp lan ngược, tức cơ chế "retry". SPEC đã khai hai cơ chế này là chưa phân xử (B1.4, ghi chú). Thẻ chỉ ghi thêm nguồn cho phía "tải vào".
4. Luật happensBefore của CRISP khớp câu chữ B2 (E1-CP). Bài còn quy định cắt con ở cả hai đầu và bỏ hẳn cây con nằm ngoài cha; đặc tả v1 ghi rõ phần này.

# V5 bổ sung sau lượt phản biện thứ ba (13/10/2026)

Phép đọc, không phải phép máy. Ghi các nhận định đã đổi ở lượt dựng `g2-build-004` và căn cứ của từng chỗ. Bản trước: `results/T-034/runs/phat-hanh-003/`.

## Điều V5 các lượt trước đã bỏ sót

- Mục 4.1 viết ở CIRCA dịch vụ gọi đứng trên root "không phải do chờ". Câu này loại hẳn một giải thích mà không có phép nào cô lập.
- Mục 4.2 và câu 8 mục 7 viết lan "được xác lập là cơ chế gây sai" cho lỗi trễ mạng, trong khi G2-H06 ghi chưa phân xử vì sao từng phương pháp xếp sai.
- Trong lượt đáp phản biện, người làm còn đọc nhãn `other` của bảng CIRCA thành "không gọi root". Nhãn này chỉ loại quan hệ trực tiếp; người phản biện chỉ ra đường gọi gián tiếp ở cả tám ca. Câu sai đó chỉ nằm trong chat, chưa vào file.

## Nhận định đã đổi và căn cứ

| Chỗ | Nhận định mới | Đầu vào → xử lý → trung gian → đầu ra | Giải thích khác còn lại |
|---|---|---|---|
| G2-H12; mục 4.1; mục 0; câu 6 | Hồi quy theo nút cha tạo điểm cực lớn; root đã không hạng 1 trước DA ở mọi ca của nhóm; DA nhận đúng các điểm đó và đổi hạng root. Đóng góp của chờ: chưa phân xử | `results/T-032/runs/circa-laptop-k2-001/collect-001/summary.json`: `/summary/k2_cases_with_huge_node/hit1` (trước DA, sau DA, bỏ cạnh) và `/summary/da_effect_on_root`; `src/circa_kien_truc/scoring.py` truyền bản sao điểm RHT vào DA | Bỏ cạnh đổi cả hồi quy lẫn DA. Nút cực lớn gọi root gián tiếp (trường `/extra/call_edges` của bản ghi từng ca), nên chờ chưa bị loại |
| Mục 4.2; câu 8 | TraceRCA bản thư viện: chuỗi chờ → cờ → điểm đã xác lập, bỏ phần chờ chỉ đổi ít ca. Trễ mạng: mới xác lập nơi có dấu hiệu | Số ca có dịch vụ gọi trên root trước và sau phép T-D (đã có trong sổ số liệu) | Số ca có dịch vụ gọi trên root khác số ca root hạng 1 |
| Mục 0 câu 3; câu 13, 14; UV-3 | Ứng viên chia ba loại: dùng cạnh đồ thị dịch vụ, dùng quan hệ cha–con trong trace, yêu cầu kỹ thuật. Hai tỷ lệ "không nằm phía trên root" chỉ nói về quan hệ gọi | MRP P7 coi quan hệ cha–con trong trace là cấu trúc khi làm đối chứng | Cạnh cùng máy, thông điệp, dữ liệu chưa được xét |
| UV-1, UV-2 | Ghi rõ điều kiện của MRP P6: hạn chế xác nhận ở bản thư viện của TraceRCA và ở phép đo vị trí; chưa xác nhận nó gây bao nhiêu ca sai | G2-H03, G2-H06 | Bài gốc TraceRCA có bước xử lý mà bản thư viện bỏ |
| UV-10; mục 6.2 | Đã khảo sát: trace hai dataset không đủ thông tin dựng cạnh thông điệp và cạnh dữ liệu. Không suy rằng quan hệ ấy không tồn tại | `results/T-002/the-rcaeval.md`; `results/T-008/the-dataset.md` | Nguồn tĩnh hoặc FlashTicket |
| Mục 0; câu 9 | Cơ chế đếm theo mẫu thuộc SimpleRCA bản M4 theo quy ước T-017 | `results/T-017/ho-so-simplerca.md` | Bài không khóa đơn vị phiếu |
| G2-H06, H17, H22 | Mức dòng nâng theo quy ước "mức cao nhất" của WHY-51 (CT, ĐC, CT); trường "Vì sao" ghi mức đó thuộc phần nào | Trường `muc_nguon_con` của từng dòng | Câu "vì sao" chính của ba dòng vẫn chưa phân xử |
| G2-H25, G2-H26; Phụ lục C | Thêm bảng theo ô lấy thẳng từ JSON của T-029 | `results/T-029/a-so-b.json`; `results/T-029/nhan-proxy-va-schema.json` | Mỗi ô ba ca; bảng mô tả |
| Mục 7 | Thêm câu 16 (vì sao chọn các phương pháp); câu 15 ghi là kế hoạch | Quyết định Q-37, Q-38; gói G1 mục 2 | — |

## Điều không đổi

Số của bảng baseline, `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json`. Các câu còn mở: lan có đáng kể; bước gây chênh giữa hai pipeline TraceRCA; onset và nền sạch; underflow ngoài hai ca; lợi ích đồ thị.

## Giới hạn của phép đọc này

- Chưa đọc lại toàn bộ Phụ lục A và B.
- Chưa đối chiếu lại từng dòng G2-H23, G2-H24 xem có bảng theo ô nào dùng được.
- Dòng B16 ở mục 6.2 dựa trên tìm từ khóa trong tài liệu chuẩn quan sát, không phải đọc toàn văn.

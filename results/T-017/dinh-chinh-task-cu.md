# Vấn đề task cũ — để reviewer kiểm

**Trạng thái 04/10/2026:** Minh duyệt theo Q-55; D1–D3 đã sửa trong results/T-001/danh-sach-phuong-phap.md, gồm ô cửa sổ và L4 của D1. Các đoạn dưới giữ audit và đề xuất trước sửa. Không đổi kết quả T017; chưa định lượng ảnh hưởng của nhánh tiền xử lý lên accuracy.

Ở thời điểm audit, không sửa task cũ. Đã soi phần liên quan SimpleRCA/Type/schema/reproduction của T000–T012, gồm SPEC/LOG/REVIEW và đầu ra cần tái dùng. Không tuyên bố kiểm lại mọi phép đo của mọi task. T003 R1–R4 đã có sửa và reviewer xác nhận; không ghi lỗi lịch sử đó như lỗi đang tồn tại.

## D1 — T001: mô tả nhánh orig nhầm đường chạy mặc định

- **Ở đâu:** `results/T-001/danh-sach-phuong-phap.md:106` (dòng SimpleRCA §3a), `:138` (L4).
- **Sai gì:** gán 6sigma/weight100/50/20 và DataAdapter đọc nhãn cho nhánh orig mà không phân biệt lớp SimpleRCA riêng với CLI mặc định. Các dòng code được dẫn có thật, nhưng CLI orig không gọi lớp đó.
- **Bằng chứng:** snapshot orig `main.py:5–11` import SimpleRCA nhưng registry['simplerca'] là NezhaRCA; `run.py:24` import NezhaRCA; `src/simplerca/nezha_rca.py:434–441` gọi NezhaDataAdapter, `nezha_adapter.py:26–58` đọc sáu parquet. SHA Git blob mọi snapshot được kiểm trong `sources/git-blob-verification.json`; đường đầy đủ/revision trong `sources/download-manifest.json`. Lớp riêng `src/simplerca/main.py:452–459` vẫn gọi DataAdapter; L4 tồn tại ở đường này, không phủ nhận.
- **Ảnh hưởng:** hồ sơ code và đường nhãn orig; M4 vẫn hợp lý vì cả hai đường code đều khác §3.1.2. Chưa biết tác giả dùng CLI hay lớp riêng/revision khác sinh bảng2; không suy từ registry hiện tại rằng lớp riêng chưa từng được chạy.
- **Đã triển khai:** snapshot đúng revision, kiểm blob, AST syntax (chỉ chứng minh parse không lỗi), sơ đồ gọi và luật từng modality trong `doi-chieu-code.md`. Không chạy code không license hoặc chép vào bản cài. Đây là sửa bằng chứng/lập luận, không có số task cũ cần chạy lại.
- **Đề xuất cũ → mới:** thay phần “(1) nhánh mặc định orig: ngưỡng metric6σ... trọng số100/50/20” bằng “(1) CLI orig đăng ký NezhaRCA: metric CPU/mem max>1,19P95 normal và>80; trace P90 tuyệt đối>100ms; các danh sách top5 cộng phiếu theo hạng5-i, metric weight1,2. Lớp SimpleRCA riêng không được CLI đăng ký vẫn có metric6σ và weight100/50/20; đó là đường code khác.” Thay L4 bằng “DataAdapter của lớp SimpleRCA riêng, không phải adapter CLI orig: đọc fault_type nhưng hàm không dùng; fault_start/end chia cửa sổ.”

## D2 — T001: luật Type bị khái quát thành chỉ đếm log

- **Ở đâu:** `results/T-001/danh-sach-phuong-phap.md:188`, hàng nhận định Type trong §7.
- **Sai gì:** câu “bài tự nói luật chỉ đếm dòng lỗi” gán một hạn chế riêng RE3-OB cho toàn bộ luật.
- **Bằng chứng:** PDF FSE §3.2.3 trang8 xét metric liên quan lỗi **hoặc** error counts log; trang9 chỉ nhận xét RE3-OB dùng error entries. arXivv2 giữ cùng nội dung. Text/hash/ảnh trong nguồn T017, bảng3 đối chiếu độc lập.
- **Ảnh hưởng:** G1 có thể hiểu sai tín hiệu đầu vào luật và nghĩa tỷ lệ0,86. Không làm đổi nguyên số công bố hoặc quyết định M4.
- **Đã triển khai:** `type-i-ii.md`, `ty-le-type-cong-bo.csv`, script đối chiếu PDF, mô tả nhãn và OPEN đủ. Không phân loại Type trên dataset mới.
- **Đề xuất cũ → mới:** “Tỷ lệ Type do luật riêng của tác giả, xét metric liên quan lỗi hoặc số log lỗi so với ngưỡng. Riêng nhận xét RE3-OB, tác giả nói chỉ đếm error entries; không khái quát điều này sang mọi dataset. Tỷ lệ này không do SimpleRCA. Điểm bản cài lại còn phụ thuộc lựa chọn nhóm và chế độ biết trước thời điểm.”

## D3 — T001: mô tả khác biệt RE3-SS còn thiếu nhánh tiền xử lý

- **Ở đâu:** `results/T-001/danh-sach-phuong-phap.md:106`, mô tả rcaeval_re3_ss chỉ nêu cờ dk_select_useful.
- **Thiếu gì:** ngoài cờ, điều kiện nhánh dataset ở time_series thay đổi; cùng tên RE3-SS đi vào chuỗi tiền xử lý khác. Không coi việc “không liệt kê hết” là lỗi quyết định M4, nhưng cần hồ sơ đủ để reviewer đánh giá code khác bài.
- **Bằng chứng:** `rcaeval/src/simplerca/time_series.py:101` dùng endswith('ss'); `rcaeval_re3_ss/.../time_series.py:101` dùng endswith('sock-shop'); đoạn103–110 drop_constant/convertmem/drop_extra/drop_near_constant/select_useful. Filter chọn CPU/mem std>1, lat50 std×1000>10 tại67–86. Diff hai snapshot được kiểm, không chạy toàn RE3-SS vì ngoài data allowlist của T017.
- **Ảnh hưởng:** khác biệt số nếu ai dùng code branch làm phép tái lập RE3-SS; không đổi kết luận M4.
- **Đã triển khai:** đối chiếu code trong hồ sơ nguồn và manifest. Không sửa file cũ, không chạy dữ liệu mới.
- **Đề xuất cũ → mới:** thêm sau câu bật dk_select_useful “Ngoài cờ, time_series.py đổi kiểm hậu tố ss thành sock-shop, làm tên rcaeval_re3_ss đi qua chuỗi lọc khác. Đây là cấu hình dataset riêng, không được mô tả trong bài.”

## Các điểm đã kiểm nhưng không gọi là lỗi mới

- T005 chưa cài SimpleRCA; không có số SimpleRCA ở T005–T007 để dùng lại. T002 duration vật lý OPEN; ratio P95 không cần đổi đơn vị. Chú thích micro giây ở T005 không đủ làm chứng cứ đơn vị, nên T017 không dùng nó.
- Mâu thuẫn Eadro-SN I&II0,96 là trong PDF, đã giữ nguyên và ghi ở type-i-ii.md; không sửa số của task cũ.
- Không thấy lỗi mới có bằng chứng trong phần còn lại liên quan T017. Phần không liên quan của T000–T012 không được tái thực nghiệm.

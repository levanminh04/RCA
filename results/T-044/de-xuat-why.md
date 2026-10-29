# Đề xuất mục WHY từ T-044 (chưa ghi vào `docs/WHY.md`)

- **Trạng thái:** bản nháp của người làm T-044 (Claude), 29/10/2026. `docs/WHY.md` nằm ngoài phạm vi ghi của T-044; Minh duyệt thì mới ghi, theo Luật 0.
- **Nguồn lập luận:** `tasks/T-044-cai-dat-m1/LOG.md` phiên 1 (mục R4, R5 của "Tự rà SPEC", "Lượt 2", "Lượt 2, phần bổ sung"); Minh duyệt các khuyến nghị ngày 29/10/2026; nội dung đã ghi ở `results/T-044/dinh-chinh-cai-dat.md` CĐ3, CĐ4.
- Lựa chọn đã được duyệt để cài. Phần ghi "chưa kiểm" chưa được dữ liệu dev xác nhận; T-045 đo bằng phép không nhãn D3, D5.

## Đề xuất 1. Đường xử lý log của E3

**Chọn gì.**
- Chuỗi vào Drain. Nezha-OB: lấy chuỗi `log` của JSON ngoài; nếu `log` giải mã được thành object có `message` kiểu chuỗi thì dùng `message`, không thì dùng `log`; JSON ngoài không giải mã được thì dùng nguyên chuỗi. RE2-TT: cột `message` nguyên văn. Adapter làm việc này, không phải lõi.
- Một Drain chung học trên mọi dòng N của thế giới đang tính, mọi thực thể, theo thứ tự (mốc ns, thực thể, nội dung) (Đ15 điểm 5). Đơn vị là cặp (thực thể, mẫu).
- Khớp dòng A chỉ trên mẫu đã biết của chính thực thể. Ba cách khớp: (a) khớp hoàn toàn, mặc định; (b) khớp theo ngưỡng; (c) khớp theo ngưỡng trong mẫu cùng lớp. Không học thêm từ A.
- Che token theo thứ tự UUID → IP (kèm cổng) → HEX → NUM, ranh giới không dính chữ hoặc số; tắt phần che sẵn của drain3. **Bỏ che "chuỗi trong ngoặc"** của đặc tả v1 dòng 227 (đổi thiết kế đã duyệt).

**Vì sao.**
- Chuỗi vào Drain: quy tắc cho cùng kết quả với `log_parsing.py` của Nezha (dòng 94–127, commit `d8140101fdb4`) mà không gọi tên dịch vụ (WHY-08).
- Một Drain chung: Đ15 điểm 5 ghi "Drain học chung cho mọi thực thể".
- Mặc định (a): đây là hàm suy luận của chính drain3 0.9.11 ("Match shall be perfect (sim_th=1.0)", `drain3/template_miner.py` dòng 149–166). Khớp hoàn toàn hỏng theo kiểu lộ ra được (tín hiệu giả hiện ở vế mốc giả và UV-6); khớp theo ngưỡng 0,4 hỏng im lặng (dòng lỗi mới bị gộp vào mẫu thường, mất bằng chứng log lỗi vì kênh log lỗi cơ bản bị thay khi E3 bật).
- Bỏ che ngoặc: TrainTicket v1.0.0 ghi log dạng `[method][…][…][…]` (`results/T-038/sources/train-ticket-v1.0.0/`, ví dụ `RouteServiceImpl.java` dòng 84). Che nội dung trong ngoặc biến cả dòng thành một token, gộp mọi thông điệp cùng số nhóm ngoặc, gộp cả dòng lỗi với dòng thường. Nezha không che ngoặc.
- Thứ tự học chuẩn: Drain phụ thuộc thứ tự dòng; phép tất định (A4) cần một thứ tự cố định.

**Đã xét.** Truyền nguyên cột `Log` như adapter P3 (`src/p3/adapters/nezha.py` dòng 94); chỉ lấy chuỗi `log` như converter của T-042; mỗi thực thể một Drain riêng; khớp theo ngưỡng làm mặc định; giữ che ngoặc; dùng mẫu che riêng của Nezha cho Online Boutique (gắn với câu log cụ thể, trái WHY-08).

**Bằng chứng.** Đọc code và cấu hình nguồn như trên; fixture tự lập MASK1–7, NEZ1–4, KHOP1–2, U1–U6 qua (`results/T-044/runs/`). Chưa có số trên dev.

**Chưa kiểm.** RE2-TT có chạy đúng bản TrainTicket v1.0.0 hay không (T-002 không ghi phiên bản). Cách khớp nào cho kênh có nghĩa hơn trên dev: T-045 đo ba cách bằng phép không nhãn D3 trước khối K; Minh chốt ở điểm dừng D17. Giả định lớp học từ N còn đúng ở A (Đ15).

**Kết luận phụ thuộc.** Kênh log khi E3 bật ở 8/16 cấu hình khối K; UV-6; kết cục của E3 theo luật C.

## Đề xuất 2. Nhóm vòng của E5 theo cách đọc C′ (co vòng)

**Chọn gì.** Với SCC S (cỡ ≥ 2) của đồ thị con gồm nút có kênh F_raw = 1 (D19), coi S như một nút:
- kênh lan ngược của e ∈ S là kế thừa khi có thành viên m ≠ e có kênh F_raw lớp không lan, hoặc có b ∉ S được một thành viên của S gọi và b có kênh F_raw thuộc lớp giải thích được của luật chung;
- kênh lan xuôi của e ∈ S là kế thừa khi có thành viên m ≠ e có kênh không lan, hoặc có a ∉ S gọi một thành viên của S và a có kênh F_raw bất kỳ.
Cách đọc A (kề cạnh) được cài như tùy chọn chẩn đoán (`params.tham_so_E5.doc_nhom_vong = "ke_canh"`), chỉ để T-045 đếm mức ảnh hưởng (D5), không dùng để chọn.

**Vì sao.** Luật chung đã bắc cầu theo F_raw: chuỗi travel → seat → config với config chậm thì travel được giải thích qua seat. RE2-TT có vòng 3 nút ở 24/30 ca dev (LOG T-044 phiên 1). Nếu có vòng seat ↔ travel, cách đọc A chặn mất chuỗi đó vì seat chỉ có kênh lan ngược, nên travel thành nghi phạm giả chỉ vì có vòng. C′ giữ chuỗi tới nguyên nhân ngoài vòng mà không cho hai triệu chứng trong vòng giải thích lẫn nhau. Câu SCC của đặc tả dùng chữ "thành viên", không kèm điều kiện kề cạnh; trong SCC mọi thành viên tới được nhau.

**Đã xét.** (A) giữ kề cạnh; (B) như A nhưng bên gọi ngoài S không giải thích kênh lan xuôi (đọc chữ "chỉ" theo nghĩa đen); (C′).

**Bằng chứng.** Fixture 8 đúng ở cả ba cách nên không phân xử được; đáp án tự lập SCC1–SCC4 (vòng 3 nút như RE2-TT) phân biệt C′ và A, qua ở cả hai cách đọc (`results/T-044/fixture/dap-an-thanh-phan.json`).

**Mặt trái (điều kiện thất bại).** Một cờ không lan yếu ở một thành viên xa vẫn xóa được bằng chứng mạnh của root nằm trong vòng; cùng loại với fixture 57 nhưng tầm rộng hơn.

**Chưa kiểm.** Số ca dev có ít nhất hai nút của vòng mang cờ F_raw (luật chỉ áp khi đó) chưa biết vì M1 chưa chạy; T-045 D5 đếm số kênh có trạng thái kế thừa khác nhau giữa A và C′.

**Kết luận phụ thuộc.** Kết quả E5 ở RE2-TT (8/16 cấu hình khối K có E5); điều kiện riêng M5.

## Đề xuất 3. Ngưỡng Drain sim_th = 0,4, độ sâu 4

**Chọn gì.** Giữ sim_th = 0,4 và độ sâu 4 của đặc tả v1 dòng 228; tham số drain3 còn lại theo mặc định 0.9.11 (max_children 100, max_clusters không giới hạn, extra_delimiters rỗng, parametrize_numeric_tokens True).

**Vì sao.** Căn cứ có trong repo: `results/T-016/dung-logts-tracets.md` dòng 60 (log Online Boutique dùng cho bài TORAI): mặc định của drain3 (ngưỡng 0,4) cho 95 mẫu so với 73 của tác giả, còn ngưỡng cao hơn tách tới 1.398 mẫu (bảng ở dòng 44–53 của cùng file; drain3 0.9.11). Với cách khớp mặc định (a), sim_th chỉ ảnh hưởng lúc học mẫu từ N.

**Đã xét.** Ngưỡng của Nezha: 0,9 (OB) và 0,8 (TT); Nezha học trên toàn bộ dữ liệu, khác cách học trên N của M1.

**Chưa kiểm.** Độ nhạy theo ngưỡng trên dev: T-045 D3 báo thêm số đo ở ngưỡng của Nezha; chỉ đổi khi Minh quyết.

**Kết luận phụ thuộc.** Tập mẫu và kênh log khi E3 bật.

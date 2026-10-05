# Đề xuất tài liệu chung — nháp, chưa duyệt

Không ghi WHY, DECISIONS, LESSONS, K1, MRP hay task cũ. File này giữ nội dung nguồn và đối chiếu việc đã áp; không phục hồi nháp bị Minh loại. Khi G1 chọn, mỗi lựa chọn quan trọng cần WHY trước dùng trong kết quả. Mọi phương án trong gói hiện **chờ WHY**.

## Kiểm từng đề xuất cũ

[CSV 90 mục đầy đủ, nguyên văn cũ→mới và lý do](trung-gian/root/application-audit-final.csv) bảo toàn văn bản nguồn, thêm trạng thái thực, câu đích và file:dòng. [Báo cáo đối chiếu](trung-gian/exposure_ledger/application-audit-reviewed.md) phân biệt mục bao trùm và con. Không coi 90 section là 90 thay đổi độc lập. Dùng cột `review_status` và `review_evidence` để biết kết luận kiểm hiện hành; các cột đầu giữ bản inventory ban đầu để truy vết.

Trạng thái: 4 mục áp nguyên văn, 23 mục áp biến thể, 50 mục chưa áp, 13 mục không áp. “pending” là chưa áp nguồn, không tự có nghĩa task chưa xong. Các mục pending cần Minh quyết việc sửa tài liệu đích; các mục notapply không đưa vào hàng đợi duyệt lại.

| Nguồn/mục | Trạng thái thực | Đích/bằng chứng |
|---|---|---|
| results/T-013/de-xuat-tai-lieu-chung.md:5 ## 1. DECISIONS — ghi quyền thực hiện task | pending | docs/DECISIONS.md:65 |
| results/T-013/de-xuat-tai-lieu-chung.md:12 ## 2. WHY — cách kiểm cơ chế T-013 (đề xuất, chưa quyết G1) | pending | docs/WHY.md:195 |
| results/T-013/de-xuat-tai-lieu-chung.md:22 ## 3. K1 — phân biệt bài với code và đơn vị độ đo | pending | docs/knowledge/K1-phuong-phap-rca.md:189; docs/knowledge/K1-phuong-phap-rca.md:191 |
| results/T-013/de-xuat-tai-lieu-chung.md:32 ## 4. Task cũ — sửa diễn giải tối thiểu | pending | docs/knowledge/K1-phuong-phap-rca.md:189; results/T-006/kiem-dung-dan.md:132; results/T-007/kiem-dung-dan.md:227; results/T-006/kiem-dung-dan.md:287; results/T-001/danh-sach-phuong-phap.md:276 |
| results/T-013/de-xuat-tai-lieu-chung.md:38 ## 5. G1 — các lựa chọn vẫn OPEN | pending | docs/DECISIONS.md:62; docs/MRP.md:159 |
| results/T-013/de-xuat-tai-lieu-chung.md:45 ## 6. WHY — phân bổ tác động biên DELAY khi sửa R1 (nháp, chờ Minh) | pending | docs/WHY.md:195; results/T-013/cua-so-va-che-do-b.md:18; tasks/T-013-ho-so-baro/LOG.md:573; tasks/T-013-ho-so-baro/LOG.md:582 |
| results/T-013/de-xuat-tai-lieu-chung.md:54 ## 7. DECISIONS — quyền sửa sau phản biện (nháp) | pending | docs/DECISIONS.md:65; tasks/T-013-ho-so-baro/LOG.md:573 |
| results/T-014/de-xuat-tai-lieu-chung.md:5 ## 1. docs/DECISIONS.md — ghi ủy quyền | pending | docs/DECISIONS.md:65 |
| results/T-014/de-xuat-tai-lieu-chung.md:15 ## 2. docs/WHY.md — scorer CIRCA tham chiếu | pending | docs/WHY.md:195; results/T-001/danh-sach-phuong-phap.md:108 |
| results/T-014/de-xuat-tai-lieu-chung.md:33 ## 3. docs/WHY.md — mapping và coverage CIRCA kiến trúc | pending | docs/WHY.md:195 |
| results/T-014/de-xuat-tai-lieu-chung.md:55 ## 4. docs/STATE.md — phần prose cũ | pending | docs/STATE.md:36 |
| results/T-014/de-xuat-tai-lieu-chung.md:63 ## 5. Tài liệu khoa học chung sau review | pending | docs/knowledge/K1-phuong-phap-rca.md:206; results/T-001/danh-sach-phuong-phap.md:60; results/T-006/kiem-dung-dan.md:216 |
| results/T-014/de-xuat-tai-lieu-chung.md:67 ## 6. docs/knowledge/K1-phuong-phap-rca.md — tách paper và implementation | pending | docs/knowledge/K1-phuong-phap-rca.md:206; docs/knowledge/K1-phuong-phap-rca.md:210 |
| results/T-014/de-xuat-tai-lieu-chung.md:93 ## 7. docs/DECISIONS.md — máy EC2 thay thế do Minh cung cấp (ghi nhận trước lượt chạy tiếp) | pending | docs/DECISIONS.md:65 |
| results/T-014/de-xuat-tai-lieu-chung.md:105 ## 8. docs/DECISIONS.md — yêu cầu tiếp tục T-014 và phân biệt cách tính ngân sách | pending | docs/DECISIONS.md:65 |
| results/T-014/de-xuat-tai-lieu-chung.md:115 ## 9. K1 §C.6 — giới hạn của PC stable và phép kiểm đổi cột | pending | docs/knowledge/K1-phuong-phap-rca.md:206; docs/knowledge/K1-phuong-phap-rca.md:210 |
| results/T-015/de-xuat-tai-lieu-chung.md:5 ## 1. docs/DECISIONS.md — thêm các xác nhận trong phiên | pending | docs/DECISIONS.md:65 |
| results/T-015/de-xuat-tai-lieu-chung.md:17 ## 2. docs/WHY.md — nháp lựa chọn biến thể MicroRank, đề xuất G1 | pending | docs/WHY.md:195 |
| results/T-015/de-xuat-tai-lieu-chung.md:23 ### Vì sao đề xuất MicroRank-RCAEval sửa đầu vào cho giao thức span hiện có — Đề xuất (G1) | pending | docs/WHY.md:195 |
| results/T-015/de-xuat-tai-lieu-chung.md:32 ## 3. docs/WHY.md — nháp sửa sắp xếp TraceRCA RCAEval, đề xuất G1 | pending | docs/WHY.md:195 |
| results/T-015/de-xuat-tai-lieu-chung.md:38 ### Vì sao lọc giá trị không hữu hạn trước khi sắp TraceRCA RCAEval — Đề xuất (G1) | pending | docs/WHY.md:195 |
| results/T-015/de-xuat-tai-lieu-chung.md:46 ## 4. K1, MRP, WHY-02 — làm rõ quan hệ tham gia detector gốc | pending | docs/knowledge/K1-phuong-phap-rca.md:178; docs/knowledge/K1-phuong-phap-rca.md:303; docs/MRP.md:54; docs/WHY.md:23 |
| results/T-015/de-xuat-tai-lieu-chung.md:56 ## 5. T-001 — ngưỡng TraceRCA gốc | pending | results/T-001/danh-sach-phuong-phap.md:88 |
| results/T-015/de-xuat-tai-lieu-chung.md:66 ## 6. STATE — việc dọn EC2 đã làm | pending | docs/STATE.md:19 |
| results/T-015/de-xuat-tai-lieu-chung.md:77 ## 7. DECISIONS — EC2 thứ hai theo Minh | pending | docs/DECISIONS.md:65 |
| results/T-015/de-xuat-tai-lieu-chung.md:81 ## 8. WHY — bản sao span và guard conflict | pending | docs/WHY.md:195 |
| results/T-015/de-xuat-tai-lieu-chung.md:86 ## 9. Cụ thể hóa nguyên văn đoạn cũ cho đề xuất §4 | pending | docs/MRP.md:54; docs/WHY.md:23; docs/knowledge/K1-phuong-phap-rca.md:178 |
| results/T-015/de-xuat-tai-lieu-chung.md:111 ## 10. docs/DECISIONS.md — Minh duyệt sửa sau REVIEW T-015 | pending | docs/DECISIONS.md:65 |
| results/T-015/de-xuat-tai-lieu-chung.md:120 ## 11. docs/DECISIONS.md — Minh chốt T-015 sau sửa phản biện | pending | docs/DECISIONS.md:65; docs/STATE.md:27 |
| results/T-016/de-xuat-tai-lieu-chung.md:7 ## W1 — `docs/WHY.md`: thêm mục bản TORAI dùng cho P3 | variant | docs/WHY.md:178; docs/WHY.md:180; docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:14 ## WHY-18. Bản TORAI dùng cho P3: bản sửa hai chỗ trong `src/torai/` — Đề xuất (G1) (T-016) | variant | docs/WHY.md:178; docs/WHY.md:180; docs/WHY.md:181; docs/WHY.md:186; docs/WHY.md:187; docs/WHY.md:188; docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:30 ## W2 — `docs/WHY.md`: seed và số lần chạy cho phương pháp có ngẫu nhiên | variant | docs/WHY.md:190; docs/WHY.md:192; docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:36 ## WHY-19. Đặt seed theo ca và số lần chạy cho TORAI, RCD — Đề xuất (G1) (T-016) | variant | docs/WHY.md:190; docs/WHY.md:192; docs/WHY.md:193; docs/WHY.md:194; docs/WHY.md:195; docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:44 ## L1 — `docs/LESSONS.md`: khớp số công bố không chứng minh phương pháp chạy đúng | variant | docs/LESSONS.md:39; docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:56 ## L2 — rút lại (sửa theo tự soát N3, REVIEW T-016) | notapply | results/T-016/de-xuat-tai-lieu-chung.md:56 |
| results/T-016/de-xuat-tai-lieu-chung.md:60 ## K1 — `docs/knowledge/K1-phuong-phap-rca.md` mục C.8 (TORAI) và C.5 (RCD) | variant | docs/knowledge/K1-phuong-phap-rca.md:198; docs/knowledge/K1-phuong-phap-rca.md:224; docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:70 ## D1 — `docs/DECISIONS.md`: ghi ủy quyền tự duyệt SPEC | variant | docs/DECISIONS.md:65 |
| results/T-016/de-xuat-tai-lieu-chung.md:76 ## R1 — rút lại (sửa theo tự soát N3, REVIEW T-016) | notapply | results/T-016/de-xuat-tai-lieu-chung.md:76 |
| results/T-016/de-xuat-tai-lieu-chung.md:80 ## Không đề xuất | notapply | docs/STATE.md:29 |
| results/T-017/de-xuat-tai-lieu-chung.md:7 ## 1. docs/DECISIONS.md — thêm sau dòng cuối | variant | docs/DECISIONS.md:63 |
| results/T-017/de-xuat-tai-lieu-chung.md:13 ## 2. docs/WHY.md — đề xuất thêm mục “Các quy ước M4 SimpleRCA của T-017” | variant | docs/WHY.md:145; docs/WHY.md:147; docs/WHY.md:149; docs/WHY.md:151; docs/WHY.md:153; docs/WHY.md:155; docs/WHY.md:157; docs/WHY.md:159; docs/WHY.md:161; docs/WHY.md:163; docs/WHY.md:165; docs/WHY.md:167; docs/DECISIONS.md:63 |
| results/T-017/de-xuat-tai-lieu-chung.md:37 ## 3. docs/LESSONS.md — đề xuất bổ sung sự cố adapter T017 | variant | docs/LESSONS.md:37; docs/DECISIONS.md:63 |
| results/T-017/de-xuat-tai-lieu-chung.md:43 ## 4. Chưa đề xuất chọn dataset, split, detector hoặc đồ thị | notapply | results/T-017/de-xuat-tai-lieu-chung.md:43 |
| results/T-018/de-xuat-tai-lieu-chung.md:5 ## E1. `docs/WHY.md` — thêm mục: cách chạy GDN ở chế độ b | variant | docs/WHY.md:169; docs/WHY.md:171; docs/WHY.md:174; docs/DECISIONS.md:64 |
| results/T-018/de-xuat-tai-lieu-chung.md:11 ## WHY-17. Lý do của phép chẩn đoán GDN ở T-018 (bộ cột cố định, điền cột thiếu, chuẩn hóa và ngưỡng từ tập kiểm định) — Đề xuất (G1); không phải cấu hình P3 | variant | docs/WHY.md:169; docs/WHY.md:171; docs/WHY.md:172; docs/WHY.md:173; docs/WHY.md:174; docs/WHY.md:175; docs/WHY.md:176; docs/DECISIONS.md:64 |
| results/T-018/de-xuat-tai-lieu-chung.md:25 ## E2. `docs/WHY.md` — thêm mục: báo Retrieval@K và Rerank@1 ở P3 | pending | docs/DECISIONS.md:64; docs/WHY.md:169 |
| results/T-018/de-xuat-tai-lieu-chung.md:31 ## WHY-18. Vì sao báo Retrieval@K và Rerank@1 (K tính theo service) cùng MRR, Hit@k — Đề xuất (G1, dùng ở P3) | pending | docs/DECISIONS.md:64; docs/WHY.md:169; docs/WHY.md:195 |
| results/T-018/de-xuat-tai-lieu-chung.md:43 ## E3. `docs/MRP.md` — P2, ý "Kiểm rò nhãn": thêm đường rò qua bộ cột | applied verbatim | docs/MRP.md:151; docs/DECISIONS.md:64 |
| results/T-018/de-xuat-tai-lieu-chung.md:50 ## E4. `docs/knowledge/K1-phuong-phap-rca.md` — §C.11 GDN | applied verbatim | docs/knowledge/K1-phuong-phap-rca.md:250; docs/DECISIONS.md:64 |
| results/T-018/de-xuat-tai-lieu-chung.md:57 ## E5. `docs/LESSONS.md` — thêm một sai lầm | variant | docs/LESSONS.md:38; docs/DECISIONS.md:64 |
| results/T-018/de-xuat-tai-lieu-chung.md:69 ## E6. `docs/MRP.md` — P1, dòng 143 (không bắt buộc) | notapply | docs/DECISIONS.md:64; docs/MRP.md:143 |
| results/T-019/de-xuat-tai-lieu-chung.md:5 ## docs/DECISIONS.md — ghi ủy quyền, mã để Minh/phiên được duyệt điền | pending | docs/DECISIONS.md:65 |
| results/T-019/de-xuat-tai-lieu-chung.md:9 ## data/README.md — sửa câu khái quát sai và thêm mục dựng T-019 | pending | data/README.md:21; data/README.md:25; data/README.md:79 |
| results/T-019/de-xuat-tai-lieu-chung.md:23 ## Hồ sơ G1/P2 — bổ sung kết quả, không quyết chọn/chia | pending | docs/MRP.md:152; results/T-019/de-xuat-tai-lieu-chung.md:23 |
| results/T-019/de-xuat-tai-lieu-chung.md:29 ## Task cũ | pending | results/T-003/the-dataset-ngoai-rcaeval.md:19; results/T-002/public-sources.md:61 |
| results/T-019/de-xuat-tai-lieu-chung.md:33 ## WHY/LESSONS/AGENTS/MRP | notapply | results/T-019/de-xuat-tai-lieu-chung.md:33 |

## Các chỗ hiện hành cần làm rõ

- `docs/DECISIONS.md:65` Q-57 ghi đã áp WHY-19/20, nhưng `docs/WHY.md:178,190` heading còn “Đề xuất (G1, dùng ở P3)”. Nội dung đã áp không có nghĩa cấu hình P3 đã duyệt. Nháp sửa tối thiểu heading: “Lý do triển khai/kiểm cơ chế T-016 đã ghi nhận theo Q-57; cấu hình P3 còn chờ G1”. Không tự sửa và không suy header để rút quyết định Minh.
- `docs/MRP.md:119` nhãn test chỉ chấm, `:160` chế độ (a) biết thời điểm. D4 cần ghi rõ mốc ngoài nào có thể cấp khi chấm test và tách nó khỏi nhãn root/tune. Cũ→mới đề xuất sau Minh chọn D4: giữ root gold/test outcome chỉ evaluator; thêm “mode (a) nhận mốc sự cố theo ngân sách đã duyệt; mode (b) không nhận mốc tiêm; không dùng nhãn test fit/tune”. Đây là nháp làm rõ, chưa là quyền đọc test.
- `docs/STATE.md:36` prose “Task đang mở” cònT001/T002. Chỉ dòngT020được sửa trong task này. Đề xuất cũ→mới: nội dung trạng thái hiện hành lấy từ các dòng task trong bảng; cập nhật prose theo taskthực đang mở sau Minh duyệt. Không tự chọntaskđể ghi vào đây.
- Q-37/Q-38 đã thu gọn danh sách; MRP P1 ước lượng8–12 là mục tiêu ban đầu, không yêu cầu mở lại lựa chọn Minh. Nháp sửa MRP nếu Minh muốn: “Danh sách hiện hành theo Q-37/Q-38; các họ không có đại diện được nêu cùng giới hạn RQ”. Không thêm phương pháp để đạt count.

## Nháp DECISIONS cho T-020 — nguyên lời ủy quyền

Đích `docs/DECISIONS.md`, thêm mã kế tiếp **sau Minh duyệt nội dung ghi** (không tự cấp mã):

| Mã nháp | Ngày | Lời đã nhận / trạng thái |
|---|---|---|
| chưa cấp | 04/10/2026 | Minh: “Minh ủy quyền tự duyệt SPEC theo prompt G1 ngày 04/10/2026”. |
| chưa cấp | 04/10/2026 | Minh: “không giới hạn số subagent, chỉ giới hạn dùng model gpt 6.1 sol ultra”. Chỉ T-020, theo prompt. |

Đây là lời ủy quyền task đã có. Phạm vi nằm trong prompt T-020: lập gói đề xuất, không quyết dataset/split G1 hoặc ghi tài liệu chung. Bản ghi shared-doc vẫn là nháp. Không ghép suy luận của agent vào cùng lời USER_CONFIRMED của Minh.

## Nháp DECISIONS và WHY cho từng lựa chọn G1

**Nháp, chưa duyệt.** Chỉ điền phương án Minh thực sự chọn. Không biến khuyến nghị của Codex thành USER_CONFIRMED. Khi ghi phải kiểm mã kế tiếp, nguồn và phiên bản. Căn cứ, phản đối mạnh nhất và bằng chứng làm đổi lựa chọn nằm ở [sáu thẻ](g1-goi-quyet-dinh.md).

### D1 — Danh sách và biến thể baseline

DECISIONS: “Minh chọn D1-__; giữ danh sách Q-37/Q-38, biến thể theo bảng 07; báo tái lập tác giả riêng với so sánh theo protocol chung.”

WHY: **Chọn:** __. **Vì sao:** __, dựa hồ sơ T-013–T-018 và kiểm sâu. **Đối lập:** code ghim làm bảng chính; bản sửa báo riêng; hoặc bản gốc đầy đủ. **Bằng chứng:** [07](07-danh-sach-phuong-phap-va-doc-nhanh.md), [kiểm sâu](trung-gian/method_evidence/deep-source-audit.md), [09](09-kiem-cheo-so-lieu.md). **Hệ quả:** bản sửa không đồng nhất tái lập toàn bài; báo schema và tập ứng viên thiếu. RQ1/RQ3a/b/d phụ thuộc biến thể, không quy toàn bộ chênh lệch cho đồ thị. **Kiểm ở P3:** normal, fixture, parity và candidates trên dev được duyệt; không chọn theo score. **Làm đổi:** pipeline gốc có schema đủ và kiểm không nhãn chứng minh hợp lệ.

### D2 — Dataset và vai trò

DECISIONS: “Minh chọn gói __ trong 06, vai trò theo CSV __; bộ giữ ngoài __ hoặc chưa có bộ đạt; giấy phép/provenance/schema __ còn OPEN, cần đầu vào __.”

WHY: **Chọn:** __. **Vì sao:** __ theo cùng chín tiêu chí cho 40 phần. **Đối lập:** A đa tín hiệu; B kiến trúc thiếu trace; C test chỉ TX0. Không dùng công adapter hoặc “đã có sẵn” làm điểm phân xử. **Bằng chứng:** [V2](01-bang-tieu-chi-hop-nhat.csv), [ba split](06-phuong-an-dataset-va-chia.md). **Hệ quả:** chưa chứng minh C9 đủ ba trục; public data chưa có nhãn vùng ảnh hưởng độc lập hoặc protocol blind hợp lệ. **Kiểm:** schema/census/provenance phải đủ cho vai trò; chỉ mở test/giữ ngoài sau G3 và Minh cho phép. **Làm đổi:** nguồn bất biến, quyền dùng, normal và nhãn chứng minh bộ ngoài phù hợp.

### D3 — Tiếp xúc và chia theo ô

DECISIONS: “Minh chọn D3-__; TX1 có vai trò __ và giới hạn __; duyệt seed 20261004, quy tắc __ và CSV __; RE2-TT 30/60 giữ __.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** TX1 test có công bố; test chỉ TX0; TX1 chỉ tái lập. **Bằng chứng:** [sổ tiếp xúc](02-so-ca-da-nhin.csv), [assert chia](runs/split-assertions.json). **Hệ quả:** TX2 kéo toàn ô sang dev; alias cần chứng cứ. TX1 không hoàn toàn ngoài thiết kế, không khôi phục TX0 bằng đổi tên. Ít ô test làm khoảng tin cậy chỉ thăm dò. **Kiểm:** identity/ô/census, không TX2 test, không đưa lookup nhãn vào features. **Làm đổi:** phát hiện output/alias TX2 gián tiếp, hoặc Minh chọn định nghĩa test nghiêm hơn.

### D4 — Ngân sách nhãn và hai chế độ

DECISIONS: “Minh chọn ngân sách __; fit normal __, tune chỉ dev, root gold và test outcome chỉ evaluator; mốc ngoài chế độ a __, chế độ b không nhận mốc tiêm; normal giữ ngoài __.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** normal từng hệ; zero-shot không normal hệ ngoài; known và blind báo riêng. **Bằng chứng:** [V6](05-nhan-va-cua-so.md). **Hệ quả:** học scale/threshold vẫn dùng thông tin normal/regime; cắt trước tiêm chưa chứng minh healthy. Test labels không fit/tune; mốc ngoài chế độ a được Minh làm rõ __ trước P7. **Kiểm ở P3:** runner, bộ cột, filename, crop và chuẩn hóa nhìn tương lai; phân biệt injection/onset/end. **Làm đổi:** không có normal sạch hoặc evaluator onset hợp lệ.

### D5 — Quy tắc cửa sổ

DECISIONS: “Minh chọn W-__; primary __ khóa từ normal trước score, sensitivity __; ghi rõ coverage thiếu; cấu hình tác giả báo riêng.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** W-time cố định; W-feasible dựa coverage/fit normal. **Bằng chứng:** [yêu cầu từng phương pháp](yeu-cau-dau-vao-hop-nhat.csv), [V6](05-nhan-va-cua-so.md). **Hệ quả:** số điểm tối thiểu để chạy không bảo đảm calibration; không clip âm thầm hoặc chọn window vì phương pháp thắng. **Kiểm ở P3:** normal-only coverage/fit/calibration rồi khóa trước score; báo sensitivity cho các phương pháp đủ điều kiện. **Làm đổi:** normal control chứng minh thiếu coverage/calibration hoặc cơ chế cần history khác.

### D6 — Retrieval@K và Rerank@1

DECISIONS: “Minh chọn __; K theo service __; báo Rerank có điều kiện cùng độ đo cuối, mẫu số 0 là NA; candidate universe/mapping/ties __.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** thêm Retrieval/Rerank; chỉ báo độ đo cuối. **Bằng chứng:** đề xuất E2 T-018, evaluator ghim và [D6](g1-goi-quyet-dinh.md). **Hệ quả:** prefix ranking không tự là module truy hồi độc lập; mapping không dùng gold; multiple-root cần evaluator riêng. **Kiểm:** lưu candidates trước cutoff, mapping độc lập nhãn; test labels chỉ score, không tune K. **Làm đổi:** không định nghĩa được candidate universe hoặc mapping hợp lệ.

## Phần chờ Minh ngoài thẻ

Nguồn bất biến và cơ chế đọc tiêu đề cho ứng viên giữ ngoài; điều khoản phái sinh/license còn OPEN. V7 đã cấp quyền first-line theo điều kiện, Bank chưa có artifact/cơ chế đáp ứng. Chi phí CIRCA lịch sử gồm worker và queue đã vượt Q-40; nháp T-014 còn chờ cách xử lý riêng, không thêm cổng G1 hoặc đổi nghĩa ba giờ. Các sửa nguồn chung ở mục pending phải duyệt đúng file/đoạn trước ghi. Không khôi phục T-018 E6/D3 đã loại.

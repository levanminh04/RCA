# Phản biện T-029

- **Người phản biện:** Codex — **Ngày:** 08/10/2026 — **Commit/diff đã đọc:** working tree so với commit gốc Minh cung cấp, bằng `git diff 6c93e6dc31f0c991b4ac6d1cfd44fcc0e989c84c`.
- **Đã đọc:** `AGENTS.md`; `docs/STATE.md`; SPEC T-029; mẫu REVIEW và `docs/review-prompt.md`; hai nguồn DT18/cô; các phần liên quan của MRP, PLAN-P3-G2, DECISIONS, WHY và LESSONS; giao thức V2 §4, §7, §8, §10; nhãn dev và universe T-022; `results/T-024/cham-a.json`; báo động, số chấm phát hiện, phân tích chi phí, soi N-Sigma và báo cáo phát hiện/RCA T-025; `results/T-025/scripts/rca_b.py`; hồ sơ BOCPD/N-Sigma và manifest T-013; `src/p3/adapters/phat_hien.py`. Đã đọc code BARO chính thức ở revision được manifest T-013 chỉ định, gồm `anomaly_detection.py`, recurrence trong `_bocpd.py` và luật điểm đổi trong `utility.py`. Đã đối chiếu [bài BARO, bản v1](https://arxiv.org/html/2405.09330v1), §2.3, §4.5 và §4.8.
- **Trạng thái đầu vào:** SPEC đang trình duyệt. `LOG.md` và `results/T-029/` chưa tồn tại. Đây là phản biện thiết kế, không phải nghiệm thu kết quả thực hiện.

## Kết luận chung

Có hai điểm CHẶN trong thiết kế: B2 áp phép so tiền tố vào thời điểm đã bị cắt bỏ; V7 dùng điều kiện không báo động để đối chứng các cờ vốn chứa điều kiện báo động. Có hai điểm KHÔNG CHẶN về phạm vi suy luận của N3 và I3. Chưa có lỗi kết quả thực nghiệm T-029 để báo; việc chưa có đầu ra không phải vi phạm tiêu chí xong ở trạng thái trình duyệt.

## Các điểm

### R1. B2 tự gắn look-ahead cho ba ca có báo động đầu sau mốc — CHẶN

- **Ở đâu:** `tasks/T-029-p4-han-che-phat-hien/SPEC.md`, dòng 66–77; bước 2b và bước 5; WHY-39 dự thảo, dòng 254.
- **Sai gì:** B2 không giới hạn thời điểm đủ điều kiện so sánh. I1 chỉ nhận chỉ số 0–719, nhưng B2 vẫn tìm điểm đổi quanh t̂ của cả các ca S có t̂ sau 720. Không có điểm I1 ở đó vì dữ liệu đã bị cắt, không phải vì đã loại ảnh hưởng của tiền xử lý dùng tương lai. Bản đồ C2 sẽ nhận cờ cơ chế sai; B3 còn bị chuyển thành N/A theo cờ B2 đó.
- **Bằng chứng:** đọc `results/T-025/bao-dong.json` → `bo_phat_hien.bocpd.<ca>.chi_so` cho ba báo động đầu: `dev-3defe3d34b` = 748, `dev-98bc73c499` = 761, `dev-f36d0647d5` = 752. Khớp `results/T-025/cham-b.md:36–38`. Ngay dung sai lớn nhất ±10 s cũng nằm hoàn toàn ngoài I1. Đây là hệ quả tất định của thiết kế, chưa chạy I1. Đã xét giới hạn ở SPEC:192 rằng B3 chỉ nói về báo sai trong nền; giới hạn đó chưa được đưa vào điều kiện B2. Recurrence native và `src/p3/adapters/phat_hien.py:30–39` xác nhận lập luận chỉ dùng dữ liệu tới i là đúng trên miền thời gian chung, nhưng không cứu phép so ngoài miền đó.
- **Đề xuất sửa:** chỉ chấm B2/B3 ở miền thời gian cùng được bản đầy đủ và tiền tố đánh giá. Quy định cách xử lý biên của vùng dung sai; thời điểm ngoài miền so ghi N/A, không ghi True. Đồng bộ điều kiện trong bước 5 và WHY-39. Giữ ảnh hưởng sau mốc OPEN; không cần chạy thêm BOCPD đầy đủ với hazard mới.

### R2. V7 phân biệt bằng chính định nghĩa cờ — CHẶN

- **Ở đâu:** SPEC dòng 57–67, 118, 166, 185, 198; WHY-39 dự thảo, dòng 254. Bước chịu ảnh hưởng: gán cờ, V7 và mức bằng chứng C2.
- **Sai gì:** V7 yêu cầu tính cùng cờ tại điểm không có báo động rồi dùng chênh tỉ lệ để quyết cờ có phân biệt được không. Với các cờ chứa điều kiện báo động, kết quả đối chứng đã bị quyết định trước. Điều này có thể tạo bằng chứng phân biệt giả hoặc loại một dấu hiệu chỉ vì điều kiện đúng rỗng.
- **Bằng chứng:** theo native `anomaly_detection.py:24–34` và adapter `phat_hien.py:74–80`, báo động gộp là OR của cờ từng cột. Tại điểm i không báo, mọi Z[i,j] = 0. N2 và N4 cần “có cột báo tại t̂”, nên khi thế t̂ = i chúng luôn False, bất kể cơ chế có ích hay không. N3 có điều kiện “không cột nào báo tại t̂ đạt N2”, nên điều kiện này đúng rỗng tại mọi điểm không báo trước mốc. B2 cũng cần bản đầy đủ có điểm đổi tại điểm đang xét. Nếu giữ nguyên cờ ở t̂ thay vì thế i, phép so lại không còn là tính cùng cờ tại điểm đối chứng. Đã xét SPEC:118 và :235 gọi cờ là liên hệ, không phải nhân quả; finding này không cáo buộc suy nhân quả. Vấn đề là WHY-39:254 vẫn khẳng định V7 ngăn cờ phổ biến thành lời giải thích, trong khi V7 ở các cờ này không cung cấp kiểm chứng độc lập.
- **Đề xuất sửa:** ghi V7 là N/A đối với N2/N3/N4/B2 dưới định nghĩa hiện tại; giữ các cờ đó là mô tả có điều kiện trên báo động. V7 chỉ áp cho đặc trưng/cờ có thể tính mà không cần điều kiện đang báo động. Bỏ khẳng định kiểm chứng độ phân biệt cho các cờ cấu trúc đó trong WHY-39 và đồng bộ tiêu chí V7. Không đề xuất thêm phép kiểm.

### R3. N3 và ba tỉ lệ chưa xác định được cơ chế được gọi tên — KHÔNG CHẶN

- **Ở đâu:** SPEC dòng 54–58; bảng C2 và `n-sigma-cot.json` dự kiến.
- **Sai gì:** E và không có cột báo dày tại t̂ chưa chứng minh báo động do cộng dồn nhiều cột. Hai tỉ lệ r_obs/r_ind không đo được mức tương quan giữa các cột. Chênh r_ind/r_nom cũng không xác định riêng phần do phân phối lệch chuẩn. Nếu dùng các diễn giải này làm hạn chế HP-n, lời giải thích sẽ mạnh hơn phép đo.
- **Bằng chứng:** phản ví dụ đại số, không chạy thực nghiệm: trên 620 điểm Nv, chỉ cột 1 báo một lần trước mốc, mọi cột khác không báo. Khi đó p1 = 1/620 < 10·p0; N3 vẫn True nhưng r_obs = r_ind = p1, không có khuếch đại do OR nhiều cột. Với ba cột có tám trạng thái `000, 001, 001, 011, 100, 110, 110, 111`, mỗi p_j = 1/2 và r_obs = r_ind = 7/8; tương quan cặp 1–2 là 0,5, cặp 1–3 là −0,5. Vì vậy cùng tỉ lệ gộp với mô hình độc lập không xác định được tương quan. Code native dùng mean/std ước lượng từ prefix, không dùng tham số thật đã biết; lịch sử hữu hạn, nền không dừng hoặc điền thiếu cũng có thể làm p_j khác p0. Đã xét quy định “cờ là liên hệ”; quy định đó không bổ sung thông tin còn thiếu cho các suy luận cụ thể trên.
- **Đề xuất sửa:** gọi N3 đúng theo điều kiện đo: “E không có cột báo dày tại t̂”. Giữ ba tỉ lệ như thống kê mô tả: độ lệch báo gộp so với mô hình độc lập và độ lệch tỉ lệ từng cột so với p0. Không coi chúng là phép tách định lượng tương quan, đuôi lệch chuẩn hay nguyên nhân cộng dồn nhiều cột.

### R4. I3 không bảo đảm là trần chất lượng RCA — KHÔNG CHẶN

- **Ở đâu:** SPEC dòng 77 và phần C4/G; WHY-39 dự thảo, dòng 254.
- **Sai gì:** t̂⁺ là báo động đầu sau mốc, không phải điểm chạy tối ưu của RCA. I3 vì thế không cung cấp cận trên chất lượng khi chọn sự kiện nhờ mốc. Dùng số này như “trần” có thể đánh giá sai phần hiệu quả còn có thể đạt được hoặc mặc định các chênh lệch đều là phần mất.
- **Bằng chứng:** định nghĩa I3 chỉ chọn min báo động ≥720, không tối đa hóa Hit. Đếm từ báo động T-025 và nhãn dev: t̂⁺ của BOCPD lệch 2–317 s; N-Sigma chính lệch 0–54 s. Ranker đổi cửa sổ và nền theo điểm chạy (`giao-thuc-v2.md:255`); không có tính đơn điệu của Hit theo độ trễ. [BARO §4.8.1](https://arxiv.org/html/2405.09330v1#S4.SS8.SSS1) cũng phân tích ảnh hưởng của việc đổi điểm chạy tới nền và thứ hạng. Đã xét SPEC:73 và :208 tách I3 khỏi số P3: điều đó đúng, nhưng không tạo bảo đảm cận trên. Bảng ghép cặp ba điểm chạy vẫn hợp lệ như phân rã mô tả; finding này không yêu cầu bỏ I3.
- **Đề xuất sửa:** gọi I3 là “RCA tại báo động đầu sau mốc, chọn nhờ nhãn mốc”. Báo các chênh ghép cặp có dấu; không dùng I3 làm cận trên chất lượng RCA hoặc bằng chứng đã phân xử sự kiện thật ngoài quy ước nhãn proxy.

## Điều đã kiểm và thấy đúng

- **Độ khớp đề tài:** C1–C6 phục vụ P4/RQ2 và NV3. DT18/cô không duyệt các ngưỡng N1/N2/B4 hay hazard; SPEC đã ghi đó là đề xuất chưa kiểm. Q-30, Q-61 và Q-69 hỗ trợ phạm vi phát hiện trên RE2-TT dev; không phải lý do đòi T-029 chạy phát hiện trên Nezha. SPEC không chốt thành phần P6 trước kết quả P4.
- **Số hiện có:** đọc JSON lưu, không chạy lại detector. Khớp BOCPD 3/30 báo động đầu đúng, hai tập N-Sigma 0/30. Mẫu có 30 ca, 10 ô, 6 ca mỗi root; cpu/disk/delay/loss có 6 ca mỗi loại, mem/socket có 3. Cả 90 cặp hiện có báo động sau mốc.
- **V4 khả thi:** BOCPD không có t̂⁺ =720, nhưng N-Sigma chính có 11/30 ca như vậy. Do đó yêu cầu tìm một ca cho V4 có đầu vào hợp lệ; không báo lỗi chỉ vì BOCPD không có ca trễ 0.
- **Nhãn và đồ thị:** native N-Sigma/BOCPD không nhận root hoặc mốc tiêm. SPEC dùng mốc trong I1–I3 và dùng root trong phân tích P1/chấm E; đã khai là phép phân tích, không thay baseline. Mốc chung 720 vẫn là thông tin nhãn thời gian, không trở thành đầu vào triển khai hợp lệ chỉ vì chung cho mọi ca. Hai detector không dùng đồ thị phụ thuộc; covariance đa biến không tự là đồ thị service. Bảng E thêm ánh xạ cột→service và thứ tự thời gian; không phải đối chứng đã loại thông tin cấu trúc, cũng không được SPEC dùng để kết luận giá trị đồ thị hay lan nhân quả.
- **WHY và lựa chọn:** WHY-39 đang là nháp trong SPEC; việc chưa nối vào WHY trước khi Minh duyệt không phải thiếu lý do đã dùng trong kết quả. Ngoài các suy luận ở R1–R4, chưa thấy phương án đối lập giả làm sai lựa chọn. R1–R3 là các điểm cần xử lý để tránh lặp lỗi suy cơ chế mạnh hơn bằng chứng của LESSONS; không cáo buộc task đã có kết quả sai.
- **Phạm vi ghi và tiêu chí xong:** T-029 chưa thực hiện, chưa thể nghiệm thu V1–V8 hoặc đầu ra. Diff tracked có thay đổi DECISIONS/STATE/WHY về T-026/T-028; SPEC T-029 là untracked nên không xuất hiện trong diff này và đã được đọc trực tiếp. Không có căn cứ quy các thay đổi có sẵn đó thành ghi ngoài phạm vi của T-029.
- **Lệnh/kiểm đã dùng:** `git status --short`, `git diff` theo commit gốc, tìm/đọc file; `git rev-parse`, `git status`, `git show` ở checkout BARO đúng revision; Python `-B -X utf8` chỉ đọc JSON, đếm các giá trị và đối chiếu số đã lưu. Không chạy detector/ranker, không mở telemetry hay dữ liệu khóa, không tải dataset, không dùng EC2. Chỉ ghi file REVIEW này; không sửa quyết định, LOG, STATE hoặc SPEC; không commit.
- **Còn mở:** thời điểm lỗi thật, nền sạch, thời lượng lỗi và khái quát ngoài RE2-TT dev chưa được task này kiểm. Không biến các OPEN đó thành finding. Minh quyết sửa/duyệt SPEC và nội dung WHY-39; reviewer không tự sửa chúng.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng | `results/T-025/bao-dong.json` → `bo_phat_hien.bocpd.<ca>.chi_so[0]` = 748, 752, 761 ở ba ca S; I1 chỉ có chỉ số 0–719. Định nghĩa B2 cũ không giới hạn miền nên gắn cờ tất định. Ca E muộn nhất t̂ = 684; 684 + 10 < 719, nên quy tắc biên không chạm dữ liệu dev. Gộp thêm: I1 chỉ loại dữ liệu sau mốc, min–max trên [0, 720) vẫn dùng dữ liệu sau t̂, nên đổi tên B2. Mặt trái: ca S không có phép kiểm look-ahead, giữ OPEN. Đã sửa SPEC B2, B3 | Duyệt sửa (08/10) |
| R2 | Đúng một phần, phạm vi rộng hơn | Đúng với N2, N3, N4, B2. Thiếu N1 (tỉ lệ theo khoảng là thuộc tính cả ca; t̂ là báo động đầu nên tự sớm) và B3 (điều kiện điểm đổi của I1). V7 chỉ có nghĩa với B1, B4. Mặt trái: cờ N-Sigma không còn đối chứng; báo cáo đặt nguyên nhân ở lý do cột báo (N1, N4, N5), không ở chính N2. Đã sửa SPEC dòng mức bằng chứng, bước 5, bảng V7 và WHY-39 | Duyệt sửa (08/10) |
| R3 | Đúng | Tính tay lại phản ví dụ: p_j = 1/2, r_obs = r_ind = 7/8, tương quan cặp 0,5 / −0,5 / 0. Chênh r_ind/r_nom có thể do lệch chuẩn, nền không dừng, lịch sử hữu hạn hoặc ffill. Nếu r_ind ≈ r_nom thì riêng số cột d ở tỉ lệ danh nghĩa đã đủ giải thích, nên chiều so này vẫn có ích như mô tả. Mặt trái: giả thuyết "phần do số cột, phần do đuôi dài" của T-025 vẫn chưa kiểm. Đã đổi tên N3 và câu diễn giải | Duyệt sửa (08/10) |
| R4 | Đúng | Không có bảo đảm đơn điệu. Ví dụ: `dev-03d4910932`, BOCPD t̂ = 684 (E-gần), BARO Hit@1 = 1 tại t̂ (`results/T-025/cham/phan-tich-b.json` → `theo_ca.dev-03d4910932.bocpd.hang_root`), nên chênh có thể âm. Đã kiểm V4 khả thi: N-Sigma chính 11/30 ca có độ trễ 0. Đã đổi tên I3 và "phần mất" thành "chênh lệch có dấu" ở C4, G và WHY-39 | Duyệt sửa (08/10) |

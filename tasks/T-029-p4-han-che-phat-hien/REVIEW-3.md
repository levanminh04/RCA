# Phản biện T-029 — lượt 3

- **Người phản biện:** Codex — **Ngày:** 08/10/2026 — **Commit/diff đã đọc:** working tree so với commit gốc Minh cung cấp, bằng `git diff 6c93e6dc31f0c991b4ac6d1cfd44fcc0e989c84c`. Thư mục T-029 chưa được track, đã đọc trực tiếp.
- **Đã đọc:** `AGENTS.md`; `docs/STATE.md`; toàn bộ SPEC T-029; `REVIEW.md` cùng bảng phản hồi; `REVIEW-2.md` cùng bảng phản hồi hiện còn trống; mẫu REVIEW; hai nguồn DT18/cô; các phần liên quan của MRP, DECISIONS, WHY, LESSONS và giao thức V2; báo động, số chấm phát hiện, nhãn dev và phân tích chi phí đã lưu. Các nguồn phương pháp, runner và cách chấm đã đối chiếu ở lượt trước được dùng lại; không chạy lại bước đã có bằng chứng hợp lệ.
- **Đối chiếu nguồn gốc lượt này:** checkout BARO sạch và đúng revision trong manifest T-013. Đọc lại native `anomaly_detection.py`, recurrence/hazard trong `_bocpd.py`, tiền xử lý và cách chấm trong `reproducibility.py`; đọc adapter `src/p3/adapters/phat_hien.py`. Đối chiếu [BARO v1 §4.5](https://arxiv.org/html/2405.09330v1#S4.SS5) và [RCAEval v2 §3.3–§3.4](https://arxiv.org/html/2412.17015v2#S3.SS3); không dùng số bài làm mốc trực tiếp cho giao thức chấm khác của T-025.
- **Trạng thái đầu vào:** SPEC còn trình duyệt, nội dung trùng snapshot đã kiểm ở lượt 2. `LOG.md` và `results/T-029/` chưa tồn tại. Không thấy phản hồi của người làm đối với hai điểm lượt 2 trong file được giao đọc. Đây là trạng thái quan sát, không suy rằng Minh đã bác hoặc duyệt các điểm đó.

## Kết luận chung

Không tìm thấy lỗi đáng kể mới. Hai điểm của lượt 2 vẫn còn trong SPEC: một điểm CHẶN về miền tính B4/V7 và một điểm KHÔNG CHẶN về diễn giải định vị N-Sigma. Sửa R1–R4 lượt 1 vẫn xử lý đúng các lỗi đã nêu; chưa có đầu ra T-029 để nghiệm thu.

## Các điểm

### R1. Miền tính B4/V7 vẫn chưa được quy định — CHẶN

- **Ở đâu:** SPEC dòng 42, 68, 166, 185, 198; bước 5, V7 và mức bằng chứng C2. Đây là REVIEW-2 R1 còn nguyên, không phải finding mới.
- **Sai gì:** B4 cần MAD của `[s0, i−w)` và hai cửa sổ quanh i. V7 vẫn yêu cầu tính cùng cờ tại mọi chỉ số không báo trong Nv. Với s0 = 1, các điểm đầu Nv có đoạn MAD rỗng. Chưa khóa việc ghi N/A, bỏ điểm hay quy False; mỗi cách cho mẫu số và tỉ lệ khác nhau. Hậu quả là kết luận “không phân biệt” phụ thuộc xử lý biên chưa được định nghĩa. Đây là lỗi thiết kế, chưa cáo buộc script T-029 đã tính sai.
- **Bằng chứng:** đếm lại chỉ đọc từ `results/T-025/bao-dong.json` → `bo_phat_hien.bocpd.<ca>.chi_so`. Báo động đầu nhỏ nhất là 102. Với w = 30, i = 1..31 không báo ở cả 30 ca, và `i−w ≤ s0`; tổng **930 điểm đối chứng có đoạn MAD rỗng**. Độ nhạy w = 15/60 cho 480/1.830 điểm như vậy. Ngoài ra, với w = 30 có 858 điểm không báo mà hậu cửa sổ chứa dữ liệu Av; ví dụ i = 719 dùng `[719,749)`. Việc dùng hậu cửa sổ ở phân tích hồi cứu không tự là rò nhãn vào detector, nhưng không còn là cửa sổ hoàn toàn trong nền. Đã xét SPEC dòng 68 xử lý MAD = 0, dòng 118 giới hạn V7 còn B1/B4, dòng 193 giữ nền sạch OPEN: các đoạn này không xử lý MAD của tập rỗng. Bằng chứng đếm khớp REVIEW-2; không chạy detector hay tính cờ mới.
- **Đề xuất sửa:** quy định miền tính B4/V7 theo từng w; ngoài miền ghi N/A và mẫu số chỉ gồm điểm hợp lệ. Nếu dùng phép so để giải thích đổi trước mốc, giới hạn cả hai cửa sổ trước mốc và khai các báo động không đủ điều kiện. Đồng bộ tiêu chí V7. Chỉ sửa phép kiểm đã có; không thêm thực nghiệm.

### R2. Loại N2 vẫn chưa bảo đảm loại báo động kéo dài qua mốc — KHÔNG CHẶN

- **Ở đâu:** SPEC dòng 81–83, bảng E và C3. Đây là REVIEW-2 R2 còn nguyên, không phải finding mới.
- **Sai gì:** bảng định vị đo báo động đầu sau mốc của mỗi dịch vụ. Độ nhạy bỏ cột báo dày trong Nv không bảo đảm thời điểm đó là khởi đầu báo động mới. Diễn giải như thời điểm thành phần bắt đầu bất thường có thể làm sai ý nghĩa bảng C3.
- **Bằng chứng:** phản ví dụ đại số: cột báo tại 719 và 720 có p_j trong Nv = 1/620 ≈ 0,00161. Ngưỡng N2 nhỏ nhất là 5·p0 = 0,0135; cột được giữ ở cả ba mức N2. Bảng E vẫn gọi 720 là “khởi phát”, dù báo động đã bắt đầu trước mốc. Native `anomaly_detection.nsigma` xét từng điểm riêng, không có luật tách episode ở đầu ra này. Đã xét dòng 85 cấm suy nhân quả/lan: giới hạn đó đúng nhưng không đổi ý nghĩa đại lượng thời gian. Chưa khẳng định dữ liệu dev có một cột cụ thể khớp phản ví dụ.
- **Đề xuất sửa:** gọi đại lượng là “báo động đầu sau mốc của dịch vụ”; mô tả bỏ N2 là độ nhạy loại cột báo dày. Bỏ bảo đảm loại mọi báo động kéo dài qua mốc. Giữ bảng như mô tả, không thêm luật onset hoặc phép chạy mới.

## Điều đã kiểm và thấy đúng

- **Phản biện trước:** bảng phản hồi lượt 1 có đánh giá và lời duyệt sửa R1–R4. SPEC hiện đã giới hạn miền B2/B3, ghi V7 N/A cho các cờ chứa điều kiện báo động, thu hẹp diễn giải N3 và bỏ cận trên của I3. Không báo lại các lỗi đã sửa. Bảng phản hồi lượt 2 còn trống; SPEC dòng 68, 81–83 và 166 vẫn giữ nội dung liên quan tới hai finding trên.
- **Số từ kết quả:** đọc JSON, đếm lại từ báo động thô và nhãn dev. BOCPD S = 3, E = 27; cả hai tập N-Sigma S = 0, E = 30. Khớp `phat-hien.json`; 90/90 cặp có báo động sau mốc. Mẫu có 30 ca, 10 ô, 6 ca mỗi root; cpu/disk/delay/loss có 6 ca mỗi loại, mem/socket có 3. Mốc tương đối là 720 ở cả 30 ca. N-Sigma chính có 11 ca t̂⁺ = 720, nên V4 có ca hợp lệ. Các số chi phí nguồn khớp: BOCPD 8.418,6 s; N-Sigma chính 164,2 s; đối chứng 1.041,8 s. Chi phí laptop trong SPEC vẫn là ngoại suy chưa kiểm.
- **Nhãn và thông tin đồ thị:** native detector không nhận root/mốc; adapter chọn cột theo schema, tính cờ rồi gộp báo động. N-Sigma dùng quá khứ; BOCPD tiền xử lý toàn bản ghi nên hồi cứu, như giao thức đã khai. Mốc 720 dùng trong I1–I3/E là nhãn thời gian cho phân tích, không trở thành đầu vào detector hợp lệ vì chung giữa các ca. Root nối sau để chấm/phân tích. Bảng E thêm mapping cột→dịch vụ; CIRCA còn dùng graph dựng từ trace trong cửa sổ. “Không dùng đồ thị” ở detector không có nghĩa toàn pipeline đã loại mọi thông tin cấu trúc. SPEC không dùng các phép này để kết luận giá trị đồ thị.
- **WHY, LESSONS và đề tài:** C1–C6 thuộc phân tích hạn chế P4 mà DT18/cô yêu cầu. Ngưỡng, hazard và định vị cụ thể là đề xuất, không phải yêu cầu của cô. Q-30 yêu cầu phần phát hiện riêng; Q-61/Q-69 giới hạn phạm vi dataset. WHY-39 vẫn là nháp, nối sau duyệt; chưa có kết quả dùng lựa chọn thiếu WHY. Các cơ chế P6 trong MRP còn là ứng viên chốt sau P4. Chưa thấy thêm phương án đối lập giả hoặc cam kết cơ chế trước bằng chứng. Hai finding hiện tại liên quan tính hợp lệ của phép đo và mức suy luận, không phải lỗi văn phong.
- **Tiêu chí xong/phạm vi:** chưa thể nghiệm thu V1–V8, bảng 90 dòng hay C1–C6 vì chưa triển khai. Thiếu LOG/đầu ra ở trạng thái trình duyệt không phải finding. Diff tracked gồm thay đổi có sẵn của DECISIONS/STATE/WHY về T-026/T-028; không có căn cứ quy chúng thành ghi ngoài phạm vi T-029. Không thay đổi quyết định nào trong lượt này.
- **Lệnh và giới hạn kiểm:** đọc/tìm file; `git diff` theo commit gốc; `git status`, `git rev-parse`, `git show` tại checkout BARO; Python `-B -X utf8` chỉ đọc JSON và đếm các giá trị nêu trên. Không chạy thực nghiệm, detector/ranker, không mở telemetry hay dữ liệu khóa, không tải dataset, không dùng EC2 hoặc subagent. Sau khi ghi, kiểm toàn bộ nội dung REVIEW-3, hash ba file T-029 có sẵn, diff tracked và trạng thái file: chỉ thêm `REVIEW-3.md`. Không commit.
- **Còn mở:** thời điểm lỗi thật, thời lượng lỗi, nền sạch và khái quát ngoài RE2-TT dev. Không biến các OPEN thành lỗi. Minh quyết xử lý hai finding và duyệt SPEC/WHY-39; reviewer không tự sửa chúng hoặc yêu cầu thêm vòng phản biện.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng; trùng REVIEW-2 R1 | Đếm lại: 480/930/1.830 điểm có đoạn MAD rỗng ở w = 15/30/60, khớp. Xử lý như REVIEW-2 R1 (xem bảng phản hồi ở đó); SPEC đã sửa sau lượt này | Duyệt sửa (08/10) |
| R2 | Đúng; trùng REVIEW-2 R2 | Xử lý như REVIEW-2 R2; SPEC đã sửa sau lượt này | Duyệt sửa (08/10) |

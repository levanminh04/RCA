# Phản biện T-022 (gói tài liệu trước triển khai: PLAN-P3-G2, SPEC T-022, SPEC T-023)

- **Người phản biện:** Claude — **Ngày:** 05/10/2026 — **Commit/diff đã đọc:** HEAD `3b1e0dd`; ba đầu vào đều chưa theo dõi (untracked), nên `git diff HEAD` rỗng; đọc trực tiếp file.
- **Ghi chú vai trò:** PLAN §9–10 dự kiến một phiên Codex soát gói này. Minh dán prompt cho Claude. Claude là người làm dự kiến của T-022 và người phản biện dự kiến của T-023. Bản nháp do Codex soạn, nên lượt này là phản biện khác agent với người soạn. Minh cân nhắc điều này khi dùng kết quả.
- **Đã đọc:** AGENTS.md; docs/STATE.md; docs/PLAN-P3-G2.md; tasks/T-022-giao-thuc-p3/SPEC.md; tasks/T-023-kiem-eadro/SPEC.md (T-022 chưa có LOG.md); docs/MRP.md §1–7; docs/DECISIONS.md Q-40, Q-54, Q-60–Q-70; docs/WHY.md (WHY-04–07, 15–21); docs/LESSONS.md; docs/review-prompt.md; DT18 và advisor-2026-09-23; results/T-005/do-kha-thi.md; results/T-013/ho-so-bocpd.md, cua-so-va-che-do-b.md, trung-gian/chi-phi-va-sentinel.json; results/T-021/goi-g1.md, chia-theo-o/A-phan-tang.csv, runs/kiem-phien-001/ket-qua.json; results/T-002/local-inspection/run-002/case-summary.csv; results/T-009/runs/run-001/labels.json, normal_intervals.json; các file nguồn của bảng chi phí và dung lượng ở PLAN §3, §6.

## Kết luận chung

Không có lỗi CHẶN. Gói bám đúng DECISIONS Q-61–Q-70, giữ chuỗi của cô (P3 rồi P4), không mở test. Số liệu tôi kiểm đều khớp file nguồn. Có ba điểm KHÔNG CHẶN cần sửa trước khi duyệt SPEC T-022. Điểm nặng nhất là R1: mốc chi phí BOCPD dùng cửa sổ cắt theo mốc tiêm, trong khi chế độ (b) không được dùng cửa sổ đó.

## Các điểm

### R1. Mốc chi phí BOCPD dùng cửa sổ chọn theo mốc tiêm, không áp được cho chế độ (b) — KHÔNG CHẶN

- **Ở đâu:** PLAN §3 dòng 76 ("BOCPD cũ 24 phút/ca chiếu 30 ca là khoảng 12 giờ"); PLAN §3 bảng, dòng T-025 ("detector dự trù 0,5–3 giờ"); PLAN §4 dòng "Cùng đêm hoặc đêm kế tiếp"; SPEC T-022 bước 4 và Tiêu chí xong ("Có số chi phí theo cấu hình Q-67").
- **Sai gì:**
  - Con số 24 phút/ca đo trên cửa sổ 600 điểm, cắt 300 + 300 quanh mốc tiêm. Đó là cách cắt của `reproduce_bocpd`.
  - Chế độ (b) là chế độ duy nhất cần BOCPD làm bộ phát hiện. Theo AGENTS luật cứng 6, SPEC T-022 mục chế độ (b) và bảng §2 của T-013, ở chế độ này detector không được nhận cửa sổ chọn theo mốc tiêm. Với RE2-TT, đầu vào hợp lệ gần nhất là cả bản ghi, T = 1441.
  - Vậy mốc 12 giờ là của một cấu hình mà chế độ (b) không được chạy. Theo chính phép ngoại suy của T-013, con số đúng nằm khoảng 5,8 lần cao hơn.
  - Q-67 nói "tập cột theo cấu hình tác giả (`reproduce_bocpd`)". SPEC không nói rõ chỉ lấy tập cột, không lấy cách cắt cửa sổ. Pilot bước 4 có thể đo nhầm ở T = 600 và ra số chi phí sai cho T-025.
  - Khoảng "0,5–3 giờ" của T-025 không có nguồn. Mọi số đo BOCPD hiện có (T-005) đều cao hơn khoảng này một bậc.
- **Bằng chứng:**
  - `results/T-005/do-kha-thi.md:49`: "BOCPD, cửa sổ 600 điểm (cùng cách cắt 300 + 300 như `reproduce_bocpd`…)" mất 1440 s. Dòng 48: cả ca 1441 điểm "không xong trong 1 giờ". Dòng 75: ước lượng cả ca ≈ 140 phút.
  - `results/T-013/ho-so-bocpd.md:66`: `reproduce_bocpd` "cắt 300 điểm trước +300 điểm sau mốc tiêm". `cua-so-va-che-do-b.md` §2: "Detector không nhận tên `inject_time` vẫn nhận window do nhãn chọn".
  - `results/T-013/trung-gian/chi-phi-va-sentinel.json`: 30 ca, T = 600 → 5.409.000 lần tính predictive; T = 1441 → 31.168.830 lần (tỉ lệ 5,76). `hours_30_equal_cases` = 12,0 giờ ứng với T = 600. Ngoại suy cho T = 1441 với cấu hình cũ: 12,0 × 5,76 ≈ 69 giờ cho 30 ca, tức khoảng 2,3 giờ/ca. Ngoại suy này **chưa kiểm**: giả định cùng d, cùng máy, cùng tải.
  - Tôi đã chạy lệnh đọc `case-summary.csv`: cả 30 ca dev RE2-TT có `n_metric_rows` = 1441 và `normal_rows` = 720.
  - Phản bác có thể có: Q-67 giảm cột sẽ giảm chi phí, và T-013 ghi runtime xấp xỉ O(T²d³), nên giảm d có thể rất hiệu quả. Nhưng số cột sau giảm chưa đo. Hệ số T² do bỏ cắt theo mốc tiêm thì vẫn còn nguyên. PLAN đã ghi mốc 12 giờ "không phải lịch được duyệt". Lỗi nằm ở chỗ chọn mốc so sánh, không ở chỗ PLAN tự nhận là lịch.
- **Hậu quả:** Dự báo lịch T-025 và việc xếp "cùng đêm" sau T-024 dựa trên số thấp hơn nhiều so với cấu hình hợp lệ. Có khả năng thật là BOCPD chế độ (b) trên 30 dev vượt trần Q-40 (3 giờ). Nếu vậy, Minh cần biết ngay khi duyệt SPEC, không phải sau pilot.
- **Đề xuất sửa:**
  - SPEC T-022 bước 4: ghi rõ pilot BOCPD cho chế độ (b) chạy trên đầu vào không chọn theo mốc tiêm (với RE2-TT là cả 1441 dòng). Ghi rõ Q-67 chỉ được hiểu là chọn tập cột.
  - PLAN §3: thay mốc 12 giờ bằng ngoại suy T = 1441 (khoảng 69 giờ cho cấu hình cũ, chưa kiểm). Bỏ khoảng "0,5–3 giờ", hoặc ghi rõ là không có nguồn.

### R2. Các quyết định G1 đã chốt nhưng chưa có mục WHY, và SPEC T-022 không giao việc viết nháp — KHÔNG CHẶN

- **Ở đâu:** SPEC T-022, Đầu ra 2 ("de-xuat-why.md — từng CANDIDATE"), bước 4 ("cấu hình liên quan đã được Minh duyệt và ghi vào docs/WHY.md") và Tiêu chí xong; PLAN §7 T-022 ("Áp dụng cửa sổ Q-64").
- **Sai gì:**
  - Q-64 (cửa sổ), Q-66 (mốc tiêm là thông tin biết trước ở chế độ (a), ngân sách nhãn root bằng 0), Q-67 (tập cột BOCPD) và Q-65 đều là DECIDED, nhưng WHY chưa có mục nào cho chúng.
  - SPEC T-022 chỉ giao nháp WHY cho các mục CANDIDATE. Các mục DECIDED không thuộc phạm vi đó, nên không ai được giao viết.
  - Theo luật cứng 3, các lựa chọn này phải có mục WHY trước khi dùng trong kết quả. Bước 4 của chính SPEC cũng chặn pilot cho tới khi WHY được ghi. Kết quả là pilot có thể bị chặn vì một việc không ai được giao. Nếu không, số P3 sẽ dùng cửa sổ chưa có WHY.
  - WHY-19 vẫn ghi "Cửa sổ P3 chưa chốt (Q-54)". Câu này đã cũ so với Q-64.
- **Bằng chứng:** Lệnh `grep -n "Q-64\|Q-66\|Q-67\|Q-65" docs/WHY.md` không trả về dòng nào. Chỉ có dòng 187 ghi "Cửa sổ P3 chưa chốt (Q-54)". Các nguồn khác cũng nói phải viết WHY cho các quyết định này:
  - `results/T-021/goi-g1.md:69`: "các chỗ đổi giao thức (cửa sổ, nguồn dữ liệu bình thường của Eadro) ghi WHY riêng khi chốt".
  - `goi-g1.md:189`, câu 4: "Đề xuất: (a), ghi vào WHY".
  - STATE: "Chưa có WHY cho cửa sổ (Q-64)… phải ghi trước khi dùng trong kết quả".
  - T-023 có giao nháp WHY cho chia phiên và nguồn bình thường Eadro, nên phần Eadro đã được phủ.
- **Đề xuất sửa:** Thêm vào Đầu ra 2 của SPEC T-022 các nháp WHY cho Q-64, Q-66, Q-67 (và Q-65 nếu Minh coi là lựa chọn quan trọng), kèm một đề xuất đính chính câu cửa sổ trong WHY-19. Ghi WHY chung vẫn cần Minh duyệt riêng như SPEC đã nói.

### R3. SPEC T-022 có điểm chờ Minh duyệt giữa task, nên theo cấu trúc không xong được trong một phiên — KHÔNG CHẶN

- **Ở đâu:** SPEC T-022, các bước 2 → 3 → 4, Tiêu chí xong, Chi phí ước lượng ("3–6 giờ công agent"); PLAN §3 ("Mục tiêu mỗi task một phiên").
- **Sai gì:**
  - Bước 3 chỉ bắt đầu khi hợp đồng đã chốt. Bước 4 cần Minh duyệt và WHY đã ghi. Tiêu chí xong cần cả hai.
  - Vậy task chắc chắn phải dừng giữa chừng để chờ Minh quyết khoảng chín nhóm lựa chọn ("Nội dung phải khóa ở bước 2"), rồi chờ ghi WHY. Đây không phải một rủi ro có thể tránh.
  - AGENTS §5a.3 yêu cầu gom câu hỏi cho Minh ở đầu phiên. §5a.4 yêu cầu đề xuất tách task ngay khi viết SPEC. SPEC lại hoãn quyết định tách sang bước 0.
  - Ngoài điểm chờ duyệt, khối việc cũng lớn: src/p3 (reader, selector, adapter, evaluator, runner), khoảng 10 độ đo kèm bootstrap, fixture, pilot 3 ca cho nhiều phương pháp, rồi phép chiếu.
  - Phản bác có thể có: SPEC đã dự liệu việc này ("Nếu đang chờ quyết định thiết yếu, chỉ báo phần đã hoàn tất… không báo task xong"). Vậy không có rủi ro báo xong sai. Còn lại là SPEC lệch với quy tắc tách task, và dòng phụ thuộc "T-022 hoàn tất" của T-024/T-025 trong PLAN thành mơ hồ.
- **Hậu quả:** Lịch PLAN §4 ("Đêm chuẩn bị") tính T-022 như một khối, trong khi thực tế có một khoảng chờ duyệt ở giữa. Phần code độc lập, như reader/selector và evaluator với fixture biết đáp án, bị xếp sau bước 2 dù chỉ phụ thuộc một phần (luật cứng 12, LESSONS SL32).
- **Đề xuất sửa:** Tách ngay khi duyệt SPEC thành hai task. Task 1: allowlist, bảng dùng lại bằng chứng, các lựa chọn giao thức và nháp WHY, kết thúc ở bước Minh quyết. Task 2: code chung, fixture, pilot, phép chiếu. Ghi rõ phần reader/selector và chấm ranking nào không phụ thuộc lựa chọn còn mở, để làm song song với task 1.

## Điều đã kiểm và thấy đúng

- **Khớp quyết định:**
  - Thứ tự dataset theo bậc khớp Q-61: T-026 sau T-024/T-025, T-027 sau T-023/T-026.
  - TORAI ở tầng 1 khớp Q-62; Nezha chỉ dùng xếp hạng biết trước cửa sổ khớp Q-61/Q-64.
  - Không chạy EC2 khớp Q-67; mốc G2 khớp Q-70.
  - Không có câu nào đổi cổng hoặc mở test/RE3-OB.
- **Prompt phản biện ở PLAN §10:** chép nguyên văn "Prompt chung" của docs/review-prompt.md, chỉ điền thông tin trung tính (Q-44, SL31). G2 không có khối trọng tâm riêng, đúng như PLAN ghi.
- **Allowlist và dung lượng:**
  - `case-summary.csv` có 35 dòng, trong đó 30 dòng `re2tt`. Đúng 30 ca này là dev RE2-TT của `A-phan-tang.csv` (so tập: True).
  - Tổng byte của 30 ca là 656.358.942 (metric + trace + log), khớp PLAN §6.
  - Lưu ý: vai trò dev lấy từ T-021, không lấy từ T-002. SPEC đã ghi "đối chiếu chia T-021".
- **Số trong PLAN §3, §5, §6 khớp nguồn:**
  - T-005: MicroRank 106/242 s, RSS 1202/2342 MB; N-Sigma phát hiện 59 s.
  - T-015 ledger: 14,653 s, chạy trên `/home/ubuntu`, tức EC2.
  - T-016: TORAI sửa 30 dev, tổng 66 s.
  - T-014: 4,063 s. T-009: 168,156 s cho hai archive.
  - Nezha 2.677.369.464 byte; ZIP TT 48.923.113 byte; logical TT 1.477.635.868 / 880.924.139 byte.
  - RAM 2.872.100 KiB ≈ 2,74 GiB; D 47.820.439.552 byte ≈ 44,54 GiB.
  - Tổng công agent 20–37 giờ, hoặc 18–33 giờ nếu bỏ T-027: cộng lại đúng.
- **Dữ kiện Eadro trong T-023 và PLAN §7 (kiểm trên `labels.json`):**
  - TT có 81 sự kiện, 9 phiên fault, 27 root, mỗi loại lỗi 27 sự kiện. Không root nào nằm ở hơn một phiên.
  - Cả 9 phiên đều trộn dev/test theo bảng ô T-021: mỗi phiên có từ 1 đến 6 ca dev.
  - Có 2 phiên TT không nhãn lỗi, mỗi phiên khoảng 8.107 s.
  - Từ `kiem-phien-001`: khoảng nghỉ giữa hai lần tiêm là 114–124 s; lần tiêm đầu cách đầu phiên 2,7–4,2 s. Vậy không sự kiện nào có đủ 300 s trước mốc mà không chồng lần tiêm trước. Q-64 đã chọn lấy dữ liệu bình thường từ phiên no-fault, và T-023 bước 5 kiểm nguồn này. Vì vậy đây không phải lỗi của gói.
- **Rò nhãn trong thiết kế:**
  - Mốc tiêm chỉ vào adapter chế độ (a). Nhãn và locator chỉ có ở runner/evaluator. Có phép kiểm "đổi locator giữ payload".
  - SLI không chọn theo root. T-022 nêu rủi ro bộ cột tương quan root (T-018) và rủi ro missingness. T-023 khóa allowlist phiên trước khi đọc telemetry.
  - Cả 30 ca dev RE2-TT có mốc tiêm đúng ở dòng 720/1441. SPEC đã nêu giới hạn "recording cắt quanh lỗi", không gọi snapshot là stream liên tục.
- **Giữ lượt hỏng, ghi tiến độ, báo trước lượt trên 1 giờ và không chạy song song khi đo:** có trong cả hai SPEC (LESSONS SL25, SL27, SL30).

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng | Pilot BOCPD chế độ (b) phải chạy trên đầu vào không chọn theo mốc tiêm (RE2-TT: cả 1.441 điểm); Q-67 chỉ chọn tập cột. Đã đưa vào `results/T-022/lua-chon-can-duyet.md` mục 10. Lưu ý: 69 giờ là ngoại suy cho bộ 76 cột của T-005; bộ cột Q-67 có 25–48 cột thô mỗi ca (`results/T-022/cot-bocpd-dev.csv`), nên chi phí thật **chưa kiểm**, đo ở pilot. | Q-72: BOCPD chạy qua đêm trên EC2 ở T-025, tối đa 20 giờ |
| R2 | Đúng | Nháp WHY cho Q-64, Q-65, Q-66, Q-67/Q-72 và ghi chú WHY-19 ở `results/T-022/de-xuat-why.md` mục A, B. Chưa ghi `docs/WHY.md`. Phản biện giao thức (phần dưới) đề nghị sửa lập luận A1–A4 trước khi ghi. | Q-74 Q15: sửa nháp WHY, trình duyệt một lần; văn bản WHY-22–35 duyệt và ghi `docs/WHY.md` ngày 06/10 (Q-76) |
| R3 | Đúng | Đã xảy ra: phiên 1 dừng ở bước 2 để chờ Minh. Trình thành câu Q1 (đề xuất tách, task mới T-030 làm bước 3–5). | Q-74 Q1: tách; T-022 dừng ở giao thức, T-030 làm code, fixture, pilot |

Ghi chú: R1–R3 do Claude viết, và Claude cũng là người làm T-022. Phản hồi trên vì vậy không độc lập. Điền ngày 05/10/2026 theo lời Minh: "duyệt sửa sổ sách và chép phản biện vào REVIEW.md và tạo prompt cho phiên của t022 làm việc tiếp".

---

# Phản biện giao thức T-022 (đầu ra bước 0–2 của phiên 1)

- **Đối tượng:** `results/T-022/lua-chon-can-duyet.md`, `giao-thuc.md`, `de-xuat-why.md` và các file đi kèm trong `results/T-022/` (phiên 1, 05/10/2026).
- **Nguồn:** Minh dán bản phản biện này vào chat của một phiên Claude ngày 05/10/2026. Bản dán không ghi tên agent viết.
- **Chép:** nguyên văn, ngày 05/10/2026, theo lời Minh: "duyệt sửa sổ sách và chép phản biện vào REVIEW.md và tạo prompt cho phiên của t022 làm việc tiếp". Không sửa nội dung; liên kết giữ như bản dán.

**Tôi không đề nghị duyệt nguyên gói hiện tại.** Phần kiểm dữ liệu và tổ chức bằng chứng có cơ sở tốt, nhưng giao thức còn vài mâu thuẫn ảnh hưởng trực tiếp đến cửa sổ thông tin, hành vi phương pháp và cách chấm.

Tôi đã đọc nguồn tại `D:/RCA-flashticket`, đối chiếu mã phương pháp và kiểm độc lập: **30 ca dev, 89/89 file khớp fingerprint, universe 68 thực thể khớp metadata**. Tôi không sửa file, không chạy benchmark và không mở tập khóa. Các đề xuất dưới đây là **CANDIDATE**, chưa thay quyết định của bạn.

Tôi đánh giá theo bốn tiêu chí: cùng điều kiện so sánh; đầu vào thực sự có sẵn tại thời điểm tuyên bố; giữ đúng phiên bản phương pháp đã chọn; và độ đo phải trả lời đúng câu hỏi nghiên cứu. Việc một cấu hình đã chạy được hoặc khớp điểm công bố chưa đủ để thỏa các tiêu chí này.

**Các điểm phản biện đáng kể**

1. **CHẶN bảng so sánh chung: TORAI chưa tuân cửa sổ Q-64.**

   Tôi tính trực tiếp từ `logts.csv` của ca `auth_cpu_1`:

   | Phần | Cửa sổ tuyên bố | Khoảng dữ liệu các bin thực sự đại diện |
   |---|---|---|
   | N | `[t−300, t)` | `[t−295, t+5)` |
   | A | `[t, t+300)` | `[t+5, t+305)` |

   Như vậy N chứa **5 giây sau tiêm**, còn A dùng thêm **5 giây ngoài cửa sổ**. Đây là khác biệt đầu vào thật. Ngoài ra, hồ sơ T-016 ghi ngưỡng tạo `tracets_lat` được tính trên toàn file; cắt các hàng sau đó không loại ảnh hưởng của dữ liệu ngoài cửa sổ.

   **Đề xuất:** đầu vào cùng nguồn/cửa sổ làm nhánh so sánh chính; CSV tác giả làm nhánh tham chiếu riêng. Không dùng lý do “đúng dữ liệu tác giả” để tuyên bố cả hai đã nhận cùng thông tin. [Nguồn đặc tả TORAI](/D:/RCA-flashticket/results/T-016/dung-logts-tracets.md:19).

2. **CHẶN triển khai MicroRank: nháp mô tả khác bản đã chọn.**

   Nháp nói operation không có nền bình thường sẽ không bị gắn cờ. Nhưng bản sửa đang được chọn **trả lỗi** khi operation mới xuất hiện hoặc độ lệch chuẩn nền không xác định do thiếu span.

   Đây không phải lựa chọn diễn giải: hai hành vi khác nhau và có thể đổi cả số ca chạy được.

   **Đề xuất:** giữ hợp đồng lỗi của bản sửa; ghi nguyên nhân và số operation thiếu nền. Muốn thêm cách xử lý khác phải được nhận diện là thay đổi phương pháp. [Mã MicroRank](/D:/RCA-flashticket/src/microrank/__init__.py:54).

3. **CHẶN triển khai TraceRCA: lọc đầu ra hiện tại chưa sửa được lỗi đã xác định.**

   Hàm tác giả tính điểm, sắp xếp rồi chỉ trả `ranks`. Adapter gọi hàm đó và lọc danh sách trả về sẽ không lấy lại được điểm trước sắp xếp để xử lý thứ tự và hòa.

   **Đề xuất:** lấy các thống kê/điểm trước bước sắp xếp, hoặc cài cầu nối trung thành với công thức trong phạm vi adapter. Đối chiếu trung gian đã có của T-015; không chỉ lọc tên trong danh sách cuối. [Mã TraceRCA](/D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py:79).

4. **CHẶN bộ chấm: hai quy tắc hòa làm các độ đo tự mâu thuẫn.**

   Nháp dùng kỳ vọng hòa cho Hit, nhưng phá hòa theo tên cho AC/Retrieval, rồi khẳng định chúng tương đương.

   Phản ví dụ: hai thực thể đồng điểm, root đứng trước theo tên. Khi đó **Hit@1 kỳ vọng = 0,5**, còn **AC@1 theo tên = 1**.

   CIRCA còn có khóa xếp hạng nhiều thành phần của DA. Không được coi hai đầu ra là hòa chỉ vì scalar score bằng nhau nếu khóa khoa học của phương pháp vẫn phân biệt chúng.

   **Đề xuất:** bảng chính dùng cùng quy tắc hòa cho mọi độ đo; giữ bảng tương thích RCAEval riêng để thực hiện Q-65. Hòa phải xét khóa xếp hạng thực của từng phương pháp. [Nháp cách chấm](/D:/RCA-flashticket/results/T-022/lua-chon-can-duyet.md:139), [khóa DA](/D:/RCA-flashticket/src/circa_kien_truc/scoring.py:66).

5. **CHẶN diễn giải chế độ (b): chưa tách vị trí điểm đổi, thời điểm kết quả có sẵn và thành công chẩn đoán.**

   BOCPD dùng chuẩn hóa toàn recording. Vì vậy vị trí điểm đổi ở giữa file không chứng minh hệ thống đã cảnh báo được ngay lúc đó. Mã còn gán `maxes[t]` từ posterior của bước trước; bỏ sentinel riêng chưa giải quyết đầy đủ hợp đồng timestamp.

   Đồng thời, RCA tại báo động sai trước tiêm vẫn có thể xếp trúng root của sự cố xảy ra sau đó — do ngẫu nhiên, schema hoặc cửa sổ A chồng vào sự cố. Điều này không đủ để tính là **phát hiện đúng rồi chẩn đoán đúng**.

   **Đề xuất:** BOCPD báo “độ lệch vị trí điểm đổi hồi cứu”; thành công chung phải yêu cầu báo động được ghép đúng sự kiện. Giữ thứ hạng tại báo động đầu để phân tích riêng. [BOCPD](/D:/RCA-ext/src/baro/baro/_bocpd.py:201), [quy tắc báo động đầu](/D:/RCA-flashticket/results/T-022/lua-chon-can-duyet.md:178).

6. **Cần sửa lập luận về schema và CIRCA; chưa có căn cứ để gọi chúng an toàn hoặc ổn định.**

   “Chạy riêng từng ca nên không học quy luật cột vắng” không loại được ảnh hưởng schema. Số cột có thể đổi số alert của SimpleRCA, số chiều BOCPD hoặc quan hệ forwarding của CIRCA, dù không có mô hình học xuyên ca.

   Với CIRCA, bằng chứng T-014 đã cho thấy hash seed khác làm đổi cạnh ở **24/30 ca có call/meta graph chu trình**, dù metric graph cuối đều là DAG. Đó là bằng chứng về độ nhạy của builder, chưa phải bằng chứng thứ hạng P3 chắc chắn đổi.

   **Đề xuất:** giữ tín hiệu `_error` hợp lệ; thêm đối chứng schema cố định. CIRCA phải khóa cả cách dựng graph và kiểm độ nhạy cấu trúc, thay vì chỉ kiểm DA trên một DAG đã có. [Schema](/D:/RCA-flashticket/results/T-018/dinh-chinh-task-cu.md:7), [CIRCA](/D:/RCA-flashticket/results/T-014/ho-so-circa-kien-truc.md:148).

**Đề xuất của tôi cho đủ 16 câu đang chờ**

| Câu | Đề xuất độc lập |
|---|---|
| **Q1 — Tách task** | **Tách.** T-022 kết thúc ở giao thức, allowlist, bằng chứng và nháp WHY; T-030 làm adapter, evaluator, fixture, pilot và chiếu chi phí. Việc triển khai phụ thuộc giao thức đã chốt. Khi tách phải cập nhật rõ phạm vi và phụ thuộc; không tự coi T-022 đã đạt tiêu chí xong cũ. |
| **Q2 — Cửa sổ (a)** | **Chọn timestamp, nửa mở.** Giữ cách chia nội bộ đã được xác minh của từng phương pháp, nhưng xử lý rõ bản ghi vượt biên: span phải đã kết thúc trong giới hạn thông tin; bin tổng hợp phải nằm đúng khoảng hoặc được dựng lại. CIRCA cần chốt điểm cuối: `current=t+300` hiện đòi điểm mà cửa sổ nửa mở không cung cấp, có thể dẫn đến điền thay điểm quan sát. |
| **Q3 — Nguồn TORAI** | **Ưu tiên B cho bảng so sánh chung; A làm tham chiếu tác giả.** B dùng telemetry cùng nguồn, bin đúng cửa sổ và ngưỡng latency học từ N. Đặt tên rõ là TORAI bản sửa với tiền xử lý của nhóm. B **chưa được kiểm trên đủ TT**, nên chưa bật mặc định. Không khớp artifact tác giả không tự chứng minh B sai phương pháp; nguyên nhân còn gồm clock và cấu hình Drain chưa biết. |
| **Q4 — Universe 68** | **Đồng ý**, gồm DB và dashboard. Không gộp DB khi chưa có nguồn sở hữu; không điền hạng cho thực thể thiếu bằng chứng. Báo riêng inventory, tập được quan sát, tập được chấm và tập được trả về. Mức ngẫu nhiên phải phản ánh đúng tập ứng viên thực tế, kể cả vị trí bị đầu ra ngoài U chiếm. |
| **Q5 — Cột metric** | **Giữ cột quan sát và `_error` cho cấu hình native**, không tự bỏ tín hiệu có ý nghĩa. Nhưng bỏ lập luận rằng chạy từng ca bảo đảm không có thông tin schema. Chạy đối chứng L* cố định từ dev để đánh giá độ nhạy; không chọn phiên bản theo accuracy. Schema toàn recording ở (b) phải được khai báo là thông tin hồi cứu. |
| **Q6 — CIRCA** | **RHT+DA làm chính; tôi ưu tiên kiểm cấu hình SVR(sigmoid) của thực nghiệm bài trước khi chốt mô hình.** Tuyến tính đã kiểm là cấu hình tham chiếu tốt, nhưng “đã kiểm” không chứng minh nó là baseline mạnh nhất. Nếu ngân sách chỉ cho tuyến tính, dùng tên đầy đủ “CIRCA kiến trúc, OLS+RHT+DA, cấu hình P3”; giới hạn kết luận tương ứng. Giữ metric cô lập, graph từ N, khóa builder và xử lý SCC. |
| **Q7 — MicroRank** | **Full ranking chính, top-11 tham chiếu.** Bản hiện có đã cung cấp cả hai. Operation thiếu nền hoặc std không xác định phải giữ ERROR theo code đã chọn. Ánh xạ bằng `serviceName`; giữ điểm và nhóm hòa. |
| **Q8 — TraceRCA** | **Support 0 không xếp; không span bất thường → NO_EVIDENCE.** Lọc hữu hạn trước sort. Phân biệt zero-support thật với thiếu baseline/std không xác định. Cài đường lấy điểm trước sort như phản biện số 3. |
| **Q9 — Ca lỗi** | **Giữ trong mẫu số, tính 0** đối với NO_EVIDENCE, lỗi phương pháp và timeout trong cohort đã cam kết. Lỗi dữ liệu hỏng/hash sai/runner đọc sai cần xử lý trước bảng khoa học, không dùng để kết luận thuật toán kém. Báo bảng trạng thái; số trên ca chạy được chỉ là phân tích có điều kiện. |
| **Q10 — Hòa/bootstrap** | **Chọn kỳ vọng hòa + cận; bootstrap theo ô, B=10.000.** Dùng cùng các ô resample khi tính chênh lệch giữa hai phương pháp. Trung bình seed theo ca trước bootstrap. Bảng chính thống nhất hòa; bảng gọi hàm RCAEval giữ riêng. Retrieval bằng 0 thì Rerank là N/A. CI chỉ phản ánh tập ô này, không đại diện mọi topology. |
| **Q11 — Chuỗi detector (b)** | **Chọn full recording 1.441 điểm, một lần, giữ bản tác giả dưới tên hồi cứu; bỏ sentinel.** Chốt ánh xạ index/timestamp trước dùng số. Lưu thời điểm thông tin cần thiết có sẵn. Không diễn giải BOCPD toàn-file như cảnh báo trực tuyến; không tự cắt đoạn để vừa ngân sách. |
| **Q12 — Cột N-Sigma** | **Cùng tập BOCPD cho phép so detector có kiểm soát.** Ghi rõ đây là N-Sigma giới hạn latency/error. N-Sigma toàn metric là đối chứng bổ sung có giá trị nếu vừa ngân sách; không suy kết quả nhánh giới hạn thành kết luận về N-Sigma nói chung. Giữ công thức riêng của từng detector, không ép toàn bộ tiền xử lý giống nhau. |
| **Q13 — Episode/chấm phát hiện** | **Không duyệt nguyên gói.** P/R/F1 theo cửa sổ dùng raw alarms. Cooldown 300 s dùng để đo thông báo/lượt RCA, không xóa phát hiện thật khỏi bảng detector. Mỗi ca tối đa một sự kiện injection được phát hiện; báo động lặp là thông báo lặp. Chọn 60 s như quy ước nhóm; chốt xử lý cửa sổ cuối chỉ một điểm và warm-up. FA/giờ dùng thời gian thực sự được đánh giá. |
| **Q14 — Ranker (b)** | **Giữ phạm vi BARO, CIRCA, TORAI**, với điều kiện đầu vào từng pipeline hợp lệ. TORAI chưa đủ điều kiện dùng nhánh cùng cửa sổ nếu còn lấy đặc trưng toàn-file. Giữ chính sách báo động đầu như cấu hình tham chiếu; bảng thành công chung cần matching sự kiện. Không tự suy trường trace thiếu để thêm MicroRank/TraceRCA vào (b). |
| **Q15 — Ghi WHY** | **Chưa ghi nguyên bản nháp.** A1–A4 ghi nhận quyết định đã có, nhưng sửa các lập luận sai về schema, hòa và thời gian. C1–C12 phải theo lựa chọn cuối của bạn. Bổ sung rõ cấu hình SimpleRCA và lựa chọn mô hình CIRCA. Ghi chú lịch sử WHY-19 hợp lý, nhưng không được dùng “cùng độ dài” để khẳng định cùng cửa sổ thông tin. |
| **Q16 — Chỗ ghi review** | **Ưu tiên thêm phần phản biện giao thức vào REVIEW.md hiện có**, giữ nguyên phần trước triển khai. Nếu tách T-030 thì kết quả code/pilot có REVIEW.md của T-030. `REVIEW-ket-qua.md` riêng chưa khớp quy tắc hiện hành rằng reviewer chỉ ghi REVIEW.md; muốn dùng cần bạn duyệt ngoại lệ rõ. |

Với Q13, tôi **không yêu cầu đợi xác minh thời lượng lỗi vật lý mới được tính mọi P/R/F1**. README RCAEval có quy ước trước injection là normal, sau injection là faulty. Có thể dùng `[t_inject, cuối file]` làm **nhãn proxy của benchmark**; onset và recovery thực vẫn OPEN. Nguồn phù hợp là [README dataset đã lưu](/D:/RCA-flashticket/results/T-002/public-metadata/run-002/sources/hf-README.md:97), không phải suy từ thời kỳ tiêm của corpus BARO khác.

Với Q14, prior work hỗ trợ việc nối detector với ranker, nhưng cần viết đúng mức bằng chứng: BARO đã ghép RobustScorer/CIRCA với các detector, song CIRCA trong bài dùng **PC**; TORAI nhận mốc từ detector ngoài, chưa chứng minh chính hai cặp tích hợp đề xuất đã được tác giả kiểm. Các cặp kiến trúc CIRCA/TORAI ở đây cần mang tên tích hợp P3. [Bài BARO, §4.4–4.6](https://arxiv.org/html/2405.09330v1), [bài TORAI, §2.2](https://arxiv.org/html/2604.13522v1).

**Các lựa chọn còn mở chưa được hỏi riêng**

- **SimpleRCA:** chốt rõ M4 theo quy ước T-017: metric events, 3σ, trace P95 tỷ lệ 3, log keyword với ngưỡng 0 và all-zero abstain. Đây là quy ước triển khai của nhóm ở những chỗ bài không khóa chi tiết. Giữ đối chứng events/channels để biết kết luận có phụ thuộc đơn vị alert không. [WHY-17](/D:/RCA-flashticket/docs/WHY.md:145).
- **Seed:** TORAI `{0,1,2}` đặt lại theo ca là hợp lý. MicroRank khóa hash seed và kiểm seed khác. CIRCA cũng phải khóa seed/order của builder; “scorer tất định” không làm graph tự tất định.
- **Pilot:** chọn theo kích thước đầu vào **sau xử lý**, không chỉ số cột thô hoặc byte toàn file. Trace cần xét span và operation trong cửa sổ; TORAI cần xét số chuỗi/biến vào bước nhân quả; CIRCA cần xét kích thước graph và parent sets. Chiếu tổng chi phí từ phân bố 30 ca, không lấy thời gian ca trung vị nhân 30 rồi coi là đủ.
- **STATE/SPEC:** câu “chưa mở phiên” và trạng thái đầu SPEC đã cũ so với Q-71/LOG. Đây là việc đồng bộ trạng thái, không phải quyết định khoa học mới. Không đánh dấu T-022 hoàn thành khi code/pilot vẫn thuộc tiêu chí xong hiện hành.

Những phần vẫn **chưa kiểm** là TORAI với đầu vào B trên TT, CIRCA SVR và graph ở cửa sổ N mới, tác động thực của các sửa giao thức lên thứ hạng, cùng chi phí BOCPD cấu hình mới. Người làm cung cấp bằng chứng triển khai/pilot; bạn quyết cấu hình và phạm vi. Phiên này chưa thêm hoặc thay quyết định nào, và không thay đổi file nào.

## Phản hồi của người làm cho phản biện giao thức (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| 1 (TORAI) | Đúng | Lưới 15 s của tác giả ở ca `re2tt_ts-auth-service_cpu_1` bắt đầu ở đầu file metric − 10 s (LOG phiên 1, 20:25). Bin là `[t0+15k, t0+15k+15)` (`results/T-016/dung-logts-tracets.md:23`). Bin chứa mốc bắt đầu ở t−10, nhãn thời gian < t, nên vào N theo `time < inject_time` (`D:/RCA-ext/src/RCAEval/main.py:382–383`). Vậy N phủ [t−295, t+5), A phủ [t+5, t+305). Ngưỡng `tracets_lat` tính trên toàn file (`dung-logts-tracets.md:26, 37`). Phạm vi: mới kiểm độ lệch ở 1/30 ca; 29 ca còn lại chưa kiểm. Nháp `lua-chon-can-duyet.md:30` có nêu lệch, nhưng không nói N chứa 5 s sau tiêm. | Q-74 Q3: chạy A và B; B làm dòng chính nếu qua phép kiểm không dùng nhãn khai báo trước; không qua thì A chính, ghi lệch 5 s và ngưỡng toàn file |
| 2 (MicroRank) | Đúng | `src/microrank/__init__.py:54–55`: operation sau mốc không có nền → `ValueError("No normal baseline for: …")`. `:56`: std nền NaN (< 2 span) → `ValueError`. Nháp `lua-chon-can-duyet.md:106` ("không bị cờ") sai. Thêm một chỗ lệch phản biện chưa nêu: nháp `:107` ghi "không có trace bình thường → ERROR", nhưng code trả về bình thường với status `no_normal_traces` và danh sách rỗng (`__init__.py:68–70`); `missing_window` cũng trả về bình thường (`:51`). | Q-74 Q7: giữ cách báo lỗi của code; đếm số ca lỗi ở ±300 s trước pilot, nhiều thì trình Minh |
| 3 (TraceRCA) | Đúng | `D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py:79–82` tính `ji_dict` cục bộ; `:86` sắp cả NaN; `:88–98` bỏ NaN sau sắp và chỉ trả `ranks`. Lọc danh sách trả về (nháp `giao-thuc.md:76`, "lọc trong src/p3") không khôi phục được thứ tự đúng. Cách sửa không cần đổi code tác giả: đọc `ji_dict` lúc hàm trả về bằng `sys.setprofile`, như `src/circa_kien_truc/scoring.py:60–65` đã làm với `DAScorer`; đối chiếu với phép tính độc lập của T-015 (`results/T-015/tracerca-rcaeval.md:93`). Thêm: operation mới sau mốc gây `KeyError` ở `tracerca.py:59` (`results/T-015/tracerca-rcaeval.md:99`). | Q-74 Q8: lấy điểm trước khi sắp; support 0 không xếp |
| 4 (quy tắc hòa) | Đúng | Nháp dùng kỳ vọng hòa cho Hit/RR/DCG (`lua-chon-can-duyet.md:139`), phá hòa theo tên cho hàm RCAEval (`:140`), rồi khẳng định trùng nghĩa (`:142`). Phản ví dụ đứng vững: hai thực thể cùng điểm, root đứng trước theo tên → Hit@1 kỳ vọng 0,5, AC@1 theo tên 1. CIRCA DA sắp theo `key` nhiều thành phần (`RCAEval/graph_heads/rht.py:285`; `src/circa_kien_truc/scoring.py:68`), nên điểm bằng nhau chưa chắc là hòa. Thêm: BARO RCAEval chỉ trả tên, điểm nằm trong biến cục bộ bị ghi đè (`RCAEval/e2e/baro.py:52–55`); TORAI chỉ trả thứ tự, khóa thật là điểm cụm rồi thứ tự trong cụm (`src/torai/torai_sua.py:286–362`). Mỗi phương pháp cần một cách lấy khóa riêng. | Q-74 Q10: một quy tắc hòa cho mọi độ đo theo khóa xếp hạng thật; bảng RCAEval riêng |
| 5 (BOCPD, chế độ b) | Đúng | `D:/RCA-ext/src/baro/baro/_bocpd.py:225`: `maxes[t] = R[:, t].argmax()`; cột `t` của R chỉ chứa dữ liệu tới `data[t−1]` (`:212–220` ghi cột `t+1` sau khi thấy `x_t`). `maxes[T]` không được gán, giữ 0 (`:196`), nên `find_cps` (`baro/utility.py:208–214`) sinh điểm đổi ở chỉ số T. Min–max toàn chuỗi (`baro/reproducibility.py:147–152`) dùng dữ liệu tương lai, nên vị trí điểm đổi không phải thời điểm cảnh báo được. Phản ví dụ cho cách gộp episode của nháp (`lua-chon-can-duyet.md:174, 176`): báo động sai ở t−100 mở một episode trơ tới t+200 và che mọi báo động đúng trong khoảng đó; ca bị tính trượt. | Q-74 Q11: cả bản ghi 1.441 điểm, gọi "hồi cứu", bỏ sentinel, sửa lệch chỉ số `maxes`; Q13: chấm bằng báo động thô; Q14: thành công chung đòi báo động ghép đúng sự kiện |
| 6 (schema, CIRCA) | Đúng | Nháp `lua-chon-can-duyet.md:76` và `de-xuat-why.md:90` ("chạy riêng từng ca nên không học được quy luật cột vắng") chỉ loại đường học xuyên ca. Số cột vẫn đổi số alert SimpleRCA (WHY-17: score tăng theo số cột), số chiều BOCPD, tập ứng viên BARO và đồ thị metric CIRCA. Sự có mặt cột tương quan root (`results/T-018/dinh-chinh-task-cu.md`, D1). CIRCA: hash seed 1 đổi cạnh ở 24 ca có call/meta graph chu trình (`results/T-014/ho-so-circa-kien-truc.md:148, 150`). Đây là bằng chứng builder nhạy, chưa phải bằng chứng thứ hạng đổi. | Q-74 Q5: dùng cột có trong file, giữ `_error`, không chạy L\*, kiểm ảnh hưởng schema ở P4; Q6: khóa hash seed khi dựng đồ thị và kiểm độ nhạy |
| Q1 | Đúng (trùng nháp) | Nháp cũng đề xuất tách (`lua-chon-can-duyet.md:18`). | Q-74 Q1: tách; T-030 làm code, fixture, pilot |
| Q2 | Đúng | (a) Span: nháp lọc theo `startTime` trong [t−300, t+300) (`lua-chon-can-duyet.md:30`), nên span bắt đầu trước t+300 mà kết thúc sau đó vẫn vào A, dù lúc t+300 chưa có. (b) CIRCA: `CaseData.load_data` nạp khoảng đóng [t−120, current] (`RCAEval/classes/data.py:89`), thêm NaN ở hai biên rồi `interpolate`/`bfill` (`:91–104`); `current = t+300` (`src/circa_kien_truc/scoring.py:38`; `RCAEval/graph_heads/rht.py:365`). Cửa sổ nửa mở không có điểm t+300, nên điểm test cuối là giá trị điền. `score_graph` nhận tham số `current`, nên sửa được mà không đổi code. (c) Thêm: `main.py:308–309` `ffill`/điền 0 trên toàn file **trước** khi cắt, nên ô trống đầu cửa sổ có thể nhận giá trị từ trước t−300. | Q-74 Q2: timestamp, nửa mở; span phải kết thúc trước t+300; CIRCA dùng điểm quan sát thật cuối cùng, không nội suy |
| Q3 | Đúng một phần | Đúng: A không nhận cùng cửa sổ thông tin (điểm 1). Chưa đủ: phản biện để B làm chính mà chưa nêu điều kiện khóa trước. B chưa kiểm trên TT; đặc tả `tracets` chỉ kiểm trên OB (`dung-logts-tracets.md:28–33`); tên cột `tracets` của TT có dạng `ts-seat-service_POST-seatservice-seats-left-tickets` (header `D:/RCA-ext/work/T-016/data/torai-TT/ts-auth-service_cpu/1/tracets_err.csv`), khác quy tắc OB ở `dung-logts-tracets.md:24`. | Q-74 Q3 theo đề xuất Claude: chạy A và B; B chính nếu qua phép kiểm khai báo trước, không qua thì A chính; không đổi sau khi thấy số |
| Q4 | Đúng | Nháp dùng U cho cả coverage và mức ngẫu nhiên (`lua-chon-can-duyet.md:60`). Mức ngẫu nhiên đúng phải tính trên tập ứng viên thật của phương pháp; RCAEval cũng tính `n_candidates` sau tiền xử lý (`main.py:322–329`). | Q-74 Q4: U = 68; báo riêng inventory, tập quan sát, tập chấm, tập trả về |
| Q5 | Đúng một phần | Đúng: bỏ lập luận "chạy từng ca nên an toàn" (điểm 6). Không đồng ý chạy L\*: L\* bỏ 23/25 cột `_error` (nháp `lua-chon-can-duyet.md:75`, nguồn T-018 D1), nên chênh giữa bản dùng cột trong file và L\* trộn hiệu ứng schema với việc mất tín hiệu lỗi; không tách được hai phần. | Q-74 Q5 theo đề xuất Claude: không chạy L\*; kiểm ảnh hưởng schema ở P4 |
| Q6 | Đúng một phần | Đúng: "đã kiểm" không chứng minh OLS là bản mạnh nhất; cấu hình thực nghiệm của bài là `ANMRegressor(regressor=SVR(kernel="sigmoid"))` (`D:/RCA-ext/work/T-014/CIRCA/circa/experiment/comparison/models.py:583–586`). Không đồng ý kiểm SVR bằng accuracy dev: Q-66 cấm chọn cấu hình bằng nhãn root. T-014 đã thấy số SVR trên 25 ca MEM fse-OB (`results/T-014/ho-so-circa-pc.md:141`); số đó không được dùng làm căn cứ chọn. | Q-74 Q6 theo đề xuất Claude: RHT+DA; khóa mô hình trước khi chạy (SVR nếu kiểm được không dùng nhãn, không thì OLS kèm tên đầy đủ); khóa hash seed và kiểm độ nhạy |
| Q7 | Đúng | Như điểm 2. Bản đầy đủ có sẵn trong đầu ra: `full_ranks`, `service_ranks_full`, `scores` (`src/microrank/__init__.py:94–103`). | Q-74 Q7 |
| Q8 | Đúng | Như điểm 3. Support 0 cho `ji` = 0/0 = NaN (`tracerca.py:82`; `results/T-015/tracerca-rcaeval.md:44`), nên "không xếp" trùng ý định "ignore ji nan" của tác giả (`tracerca.py:90`). | Q-74 Q8 |
| Q9 | Đúng | Nháp đã giữ ca lỗi ở mẫu số (`lua-chon-can-duyet.md:129`); phản biện thêm việc tách lỗi dữ liệu/runner khỏi lỗi phương pháp. Hợp lý: `main.py:552–553` bỏ ca có khóa `error`, nên lỗi runner không sửa sẽ thành "phương pháp kém" hoặc biến mất khỏi mẫu. | Q-74 Q9 |
| Q10 | Đúng | Như điểm 4. Thêm: `Evaluator` mặc định `max_k=5` (`RCAEval/benchmark/evaluation.py:9`); Retrieval@10 cần `max_k=10`, không thì trả `None` (`:162–166`). Rerank của RCAEval là tỉ số của hai tỉ lệ gộp, không tính theo ca (`:203–210`). Bootstrap theo cặp ô: đúng, vì hai phương pháp được so trên cùng mẫu lấy lại. | Q-74 Q10 |
| Q11 | Đúng | Như điểm 5. Sửa lệch chỉ số làm được ngoài code tác giả: `online_changepoint_detection` trả cả R (`_bocpd.py:227`), nên tính lại `argmax R[:, t+1]` với `t = 0..T−1`; không có phần tử thứ T, nên không còn sentinel. | Q-74 Q11 |
| Q12 | Đúng | Trùng nháp ở phần chính (`lua-chon-can-duyet.md:173`); phản biện thêm đối chứng mọi cột. | Q-74 Q12: cùng tập cột BOCPD; thêm mọi cột làm đối chứng |
| Q13 | Đúng | Như phản ví dụ ở điểm 5. Nguồn nhãn proxy: README RCAEval ("inject_time.txt splits each case into a normal period (before) and a faulty period (after)", `results/T-002/public-metadata/run-002/sources/hf-README.md:97`), hợp hơn nguồn nháp (bài BARO, corpus khác). | Q-74 Q13 |
| Q14 | Đúng | Bài BARO ghép bộ phát hiện với CIRCA bản PC; RCAEval CIRCA dùng PC (`results/T-014/ho-so-circa-pc.md:100`). TORAI nhận `t̂_A` từ bộ phát hiện ngoài (`results/T-016/ho-so-torai.md:25`), nhưng không có bằng chứng tác giả đã kiểm cặp cụ thể. Phần trích bài TORAI §2.2 của phản biện: chưa đọc lại trong phiên này. | Q-74 Q14 |
| Q15 | Đúng | A1 ("trùng `--length 10`") nói cùng độ dài, không chứng minh cùng cửa sổ thông tin (Q2 mục c, điểm 1); A2 viện dẫn "phá hòa theo tên" (`de-xuat-why.md:27`); A4 viện dẫn "không thành đường học nhãn" (`:45`). Đã sửa ở `results/T-022/de-xuat-why-v2.md`. | Q-74 Q15 |
| Q16 | Đúng | AGENTS §9: người phản biện chỉ ghi `REVIEW.md`. Nháp đề xuất `REVIEW-ket-qua.md` (`lua-chon-can-duyet.md:219`), trái luật đó. | Q-74 Q16: ghi tiếp REVIEW.md hiện có; T-030 có REVIEW.md riêng |
| Lựa chọn mở: SimpleRCA | Đúng | Nháp chỉ ghi "quy ước T-017 (WHY-17)" (`cau-hinh/p3-re2tt-de-xuat.json`), không chốt; WHY-17 tự ghi "chưa chốt P3". Thêm: adapter T-017 chia span theo `startTime` và không đòi span kết thúc trước t+300 (`src/simplerca/adapter.py:63–69`), nên số `run-dev-005` của T-017 không dùng lại nguyên trạng ở P3. | Q-74 "Thêm": SimpleRCA theo T-017/WHY-17 |
| Lựa chọn mở: seed | Đúng | Nháp mục 12 không nói seed của builder CIRCA. Scorer tất định (SLI chọn theo tên, `src/circa_kien_truc/scoring.py:39`), nhưng builder nhạy với hash seed (điểm 6). | Q-74 Q6: khóa hash seed khi dựng đồ thị và kiểm độ nhạy |
| Lựa chọn mở: pilot | Đúng | Nháp chọn ca theo số cột thô hoặc số span toàn file (`lua-chon-can-duyet.md:195`), không theo kích thước sau tiền xử lý. | Q-74 "Thêm": chọn ca pilot theo kích thước sau xử lý |
| STATE/SPEC cũ | Đúng một phần | Dòng "Trạng thái" đầu SPEC (`tasks/T-022-giao-thuc-p3/SPEC.md:3`) còn ghi "chưa duyệt", dù LOG ghi Minh duyệt ngày 05/10 (Q-71). SPEC đã khóa; sửa dòng này cần Minh duyệt riêng. STATE đã đồng bộ ở phiên 2. | Chưa có quyết định |

Ghi chú: điền ngày 05/10/2026, phiên 3 của người làm (Claude). Cột "Minh quyết" chép theo DECISIONS Q-74. Bằng chứng kiểm lại trong phiên 3 trên file thật; RCAEval `259ea41`, BARO `e35f4ec` và `src/` chưa đổi so với phiên 2.


---

# Phản biện T-022 — giao thức P3 bản 2

- **Người phản biện:** Codex — **Ngày:** 06/10/2026 — **Commit/diff đã đọc:** `git diff 3b1e0dd`, cùng các file chưa commit đọc trực tiếp. Đây là phần bổ sung; hai phần trước và bảng phản hồi của người làm giữ nguyên.
- **Đã đọc:** `AGENTS.md`; mẫu `tasks/_MAU/REVIEW.md`; SPEC, toàn LOG và REVIEW của T-022; mọi file trong `results/T-022/` (hai bản giao thức, lựa chọn, hai nháp WHY, hai bộ quy tắc/cấu hình, allowlist, nhãn, CSV, mappings, scripts và runs); `docs/STATE.md`, `DECISIONS.md`, `WHY.md`, `LESSONS.md`, `MRP.md`, `PLAN-P3-G2.md`; hai nguồn DT18/hướng dẫn cô. Đối chiếu hồ sơ T-013–T-018, nguồn metadata/chia T-002/T-021 và bằng chứng T-017. Đọc code `src/microrank`, `src/simplerca`, `src/torai`, `src/circa_kien_truc`; code RCAEval `259ea41`, BARO `e35f4ec`, CIRCA `0215e18` tại các đường dẫn được giao, và CSV torai-TT của ca dev auth_cpu_1.

## Kết luận chung

Có **hai điểm CHẶN** ở phép kiểm đầu vào TORAI và quy tắc hòa của TORAI; có **hai điểm KHÔNG CHẶN** ở hợp đồng thời điểm thông tin và diễn giải Retrieval/Rerank. Đây là lỗi lập luận hoặc mâu thuẫn thiết kế trong văn bản đề xuất, **không phải bằng chứng đã có một lượt benchmark P3 sai**. Cần sửa hai điểm chặn trước khi dùng các phần giao thức tương ứng ở T-030; không cần làm trước công việc P4.

## Các điểm

### V2-R1. K-B1 khớp tổng service nhưng không kiểm đúng đặc trưng TORAI sử dụng — CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:186–189`; `de-xuat-why-v2.md:92,95` (WHY-29); `cau-hinh/p3-re2tt-v2.json:11`.
- **Bước chịu ảnh hưởng / sai gì:** dựng `tracets` → điểm mức nghiêm trọng → GMM → lựa chọn nguồn B làm dòng chính. K-B1 gộp cột operation về tổng (service, bin), rồi coi ≥95% ô tổng trùng là bằng chứng “B có dựng đúng đặc tả trên TT”. Nhưng TORAI chuẩn hóa, lấy max |z| **từng cột operation**, chuẩn hóa điểm toàn nguồn, rồi mới cộng về service. Phép gộp để kiểm đã xóa chính thông tin mà phương pháp còn dùng.
- **Bằng chứng:** `src/torai/torai_sua.py:130–134,193–203,232–235` thực hiện bỏ cột hằng, StandardScaler từng cột, max |z|, chuẩn hóa và cộng điểm service. Phản ví dụ số học: bản X có hai operation của service s, mỗi cột N = [0,2,0,2], A = [4,4,4,4]. Bản Y dồn vào operation thứ nhất, N = [0,4,0,4], A = [8,8,8,8], operation thứ hai toàn 0. Tổng (service, bin) hai bản trùng **100%**, nhưng X có hai điểm z = 3, Y bỏ cột hằng và chỉ còn một điểm z = 3. Nếu một service khác có một cột điểm 3, điểm trace của s sau chuẩn hóa/cộng là **2/3 ở X, 1/2 ở Y**. K-B1 vẫn đạt dù đầu vào mức nghiêm trọng khác. S9 được viện dẫn thật sự ghép theo tên `service_operation` và tính cả cột không ghép được (`tasks/T-016-ho-so-torai/SPEC.md:95`); v2 đã đổi đơn vị của tiêu chí đó.
- **Đoạn đã xét có thể phản bác:** D4 vẫn chờ xác nhận; WHY-29 cũng nói B khác tác giả và log B chưa khớp. Điều này giữ đúng trạng thái đề xuất, nhưng không làm phép kiểm tổng service xác minh được cột trace. K-B2 chỉ kiểm tổng log; K-B3 chỉ kiểm không lỗi. Cả ba không loại phản ví dụ trên.
- **Hậu quả:** quy tắc chọn trước khi thấy số có thể cho B đạt vì dựng sai hoặc gộp thiếu operation, rồi quy thay đổi điểm/cụm/thứ hạng cho các thay đổi đầu vào có chủ đích. Đây là khuyết tật của phép kiểm đề xuất, chưa khẳng định dữ liệu B thực tế đã bị dựng sai. Nó lặp kiểu suy “kiểm đúng” từ đại lượng không kiểm đầu vào thật của thành phần (LESSONS SL36).
- **Đề xuất sửa:** sửa **chính K-B1** để đối chiếu cột operation bằng ánh xạ tường minh, tính cả cột không ghép; giữ ngưỡng nếu Minh vẫn chọn ngưỡng đó. Nếu chưa xác định được ánh xạ TT, giữ phần này OPEN và gọi phép tổng service–bin đúng là kiểm tổng đếm, không dùng nó để xác nhận dựng đúng đặc trưng TORAI. Không đổi quyết định Q-74 chạy cả A/B.

### V2-R2. Hòa điểm cụm không cho phép hoán vị đều mọi service trong cụm — CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:190,262–273`; `de-xuat-why-v2.md:79` (WHY-28).
- **Bước chịu ảnh hưởng / sai gì:** đầu ra TORAI → khóa xếp hạng → kỳ vọng các độ đo. Mục 6.6 vừa đề xuất khóa (điểm cụm, thứ tự RCD hoặc y_train), vừa quy định “Hai cụm cùng điểm thì mọi service của hai cụm tính là một nhóm hòa”. Mục 8.4 lại chỉ coi khóa bằng nhau là hòa và hoán vị ngẫu nhiên đều từng service. Ba quy định này không tương đương.
- **Bằng chứng:** `src/torai/torai_sua.py:287–300,305–358` sắp cụm theo điểm rồi nối **trọn từng khối cụm**; bên trong giữ thứ tự RCD, hoặc thứ tự y_train khi rơi nhánh dự phòng. Giả sử hai cụm ngang điểm có thứ tự nội bộ A > B và C > D. Đổi thứ tự hai khối cho AB|CD hoặc CD|AB, vẫn giữ thứ tự nội bộ. Với root A, kỳ vọng RR là (1 + 1/3)/2 = **2/3**. Coi cả bốn service hòa đều cho RR = (1 + 1/2 + 1/3 + 1/4)/4 = **25/48**; Hit@1 cũng đổi từ **1/2 thành 1/4**. Nếu thay vào sắp phẳng theo (điểm cụm, thứ tự nội bộ), có thể ra A,C,B,D, không còn danh sách nối khối của code.
- **Đoạn đã xét có thể phản bác:** yêu cầu “thứ tự dựng lại phải trùng ranks chính thức” không xác định phân phối hòa cho evaluator. Giới hạn “hòa bên trong RCD chưa kiểm” là việc khác: phản ví dụ giữ nguyên thứ tự RCD và chỉ xét hòa **giữa cụm**. Chưa có bằng chứng hai cụm ngang điểm đã xuất hiện trong 30 ca dev; finding không khẳng định số benchmark hiện có sai.
- **Hậu quả:** T-030 phải tự chọn một trong các quy định trái nhau; nếu dùng nhóm hòa phẳng thì làm mất bằng chứng thứ tự nội bộ và tính sai kỳ vọng Hit/MRR/NDCG so với chính sách xếp hạng đã mô tả.
- **Đề xuất sửa:** thống nhất mục 6.6, 8.4 và WHY-28 theo xếp hạng hai cấp: cụm là khối, thứ tự nội bộ giữ theo nhánh thật; khi hòa điểm cụm, kỳ vọng chỉ trên các hoán vị khối hợp lệ, cộng hòa nội bộ nếu xác định được. Không đồng nhất mọi service chỉ vì điểm cụm bằng nhau; không gán tuple phẳng thành khóa toàn cục của code.

### V2-R3. Bảng thời điểm có kết quả chưa ghi ngoại lệ của đầu vào hồi cứu — KHÔNG CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:82–84,92,101,178,202`; `de-xuat-why-v2.md:23–24,95,145`; `cau-hinh/p3-re2tt-v2.json:5`.
- **Bước chịu ảnh hưởng / sai gì:** hợp đồng thông tin đầu vào và diễn giải thời điểm RCA ở (a)/(b). Bảng chung nói ranker chỉ nhận [t−300,t+300), kết quả có lúc t+300 hoặc t̂+300; WHY-22 giải thích “chỉ dữ liệu đã có lúc đó được vào”. TORAI A vẫn có thể làm dòng chính nhưng dùng bin vượt biên và ngưỡng toàn file. Pipeline BOCPD cần preprocessing toàn bản ghi trước khi xác định t̂.
- **Bằng chứng:** đọc lại CSV auth_cpu_1 bằng Python cho N phủ **[t−295,t+5)**, A phủ **[t+5,t+305)**; tổng log tác giả **223.924**. Metric cả 30 ca thật sự có 1.441 điểm từ t−720 đến t+720. `RCAEval/main.py:381–394` cắt 20 dòng mỗi phía; v2:178 và WHY-29:95 giữ ngưỡng `tracets_lat` toàn file. BARO `e35f4ec`, `baro/reproducibility.py:147–154` dùng min–max toàn chuỗi; v2:202 giữ bước đó. Do vậy không thể áp thời điểm t+300/t̂+300 như giới hạn khả dụng chung cho các nhánh này.
- **Đoạn đã xét có thể phản bác:** v2:206,369–371 và WHY-34:145 đã khai báo hồi cứu/look-ahead, đúng với Q-74. Đây không phải cáo buộc giấu rò nhãn hoặc yêu cầu đổi BOCPD. Tuy nhiên, các giới hạn đó chưa sửa dòng khẳng định thời điểm khả dụng trong hợp đồng chung.
- **Hậu quả:** báo cáo có thể gắn thời điểm kết quả sớm hơn lúc đủ đầu vào, hoặc gọi nguồn A là cùng giới hạn thông tin với các baseline khác. Chưa có lượt P3 dùng timestamp này.
- **Đề xuất sửa:** ghi ngoại lệ ngay trong bảng §4, §5.1, WHY-22 và trường cấu hình liên quan: nhánh dùng TORAI A hoặc BOCPD chỉ có kết quả khi bản ghi/đặc trưng toàn file đã sẵn có, cộng thời gian chạy; t̂ BOCPD là vị trí hồi cứu. Giữ quyết định Q-74 và cách gọi kết quả hồi cứu.

### V2-R4. Retrieval/Rerank từ thứ hạng cuối không tự xác định bước cơ chế bị hỏng — KHÔNG CHẶN

- **Ở đâu:** `results/T-022/de-xuat-why-v2.md:33,37` (WHY-23).
- **Bước chịu ảnh hưởng / sai gì:** số xếp hạng P3 → diễn giải hạn chế P4. Nháp nói phép tách “cho P4 biết tìm cơ chế ở bước nào”, với kết luận phụ thuộc là “lỗi truy hồi hay lỗi xếp lại”. Nhưng K=5/10 ở đây là cắt **thứ hạng cuối**, không phải một tập ứng viên độc lập trước bước xếp hạng.
- **Bằng chứng:** code RCAEval `259ea41`, `RCAEval/benchmark/evaluation.py:162–184` định nghĩa Retrieval@K bằng accuracy@K; `:203–210` lấy tỉ số accuracy/retrieval. Phản ví dụ: root đã có trong tập quan sát, đã được phương pháp chấm và trả về, nhưng đứng hạng 6. Với K=5, Retrieval=0 dù root không bị loại ở đầu vào hay bước tạo ứng viên. Chỉ lỗi điểm/thứ tự cũng tạo được kết quả gọi là “không truy hồi”.
- **Đoạn đã xét có thể phản bác:** WHY-23:36 đã nhận hai độ đo là cách trình bày của cùng thứ hạng, không phải bằng chứng độc lập. Công thức và việc báo theo Q-65 đều hợp lệ; bài DecompRCA cũng có định nghĩa top-K ngầm này. Nhưng đoạn giới hạn chưa rút lại suy luận định vị **cơ chế/bước**.
- **Hậu quả:** P4 có thể gán lỗi xếp hạng cho bước tạo ứng viên chỉ từ nhãn metric. Đây là kết luận mạnh hơn bằng chứng, không phải lỗi công thức.
- **Đề xuất sửa:** giới hạn lý do và kết luận phụ thuộc thành phân biệt root ngoài top-K với root trong top-K nhưng ngoài top-1 của danh sách cuối. Muốn quy về bước cơ chế thì dùng các tập và bằng chứng trung gian giao thức đã yêu cầu lưu; không thêm phép kiểm hay yêu cầu làm P4 ngay.

## Điều đã kiểm và thấy đúng

- **Số liệu/đầu vào:** đọc và parse toàn bộ JSON/CSV/runs của T-022. Tính độc lập từ allowlist, nhãn và schema: **30 ca**, **10 ô × 3**, **68 thực thể** = 41 service + 26 DB + dashboard; mọi root dev thuộc U; tập cột BOCPD **25–48/ca**. Băm lại **89/89 file** (30 metric, 30 trace, 29 log), không sai hash/byte; tổng **656.358.942 byte** khớp `kiem-allowlist.json`. Đọc cột time thật của 30 parquet: mỗi ca **1.441 điểm, nhịp 1 s, mốc ở giây 720**, cuối file ở t+720. Không dùng vị trí giữa file để dựng mốc.
- **Lệnh kiểm:** `git status --short`, `git diff 3b1e0dd`; kiểm revision/trạng thái các checkout RCAEval/BARO/CIRCA. Các tính lại metadata/hash/CSV chạy từ stdin bằng `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -`, với `PYTHONDONTWRITEBYTECODE=1` và PYTHONPATH được giao khi đọc parquet. Không chạy lại các script tạo đầu ra vì chúng ghi file; không chạy phương pháp, benchmark, thực nghiệm mới hoặc mở dữ liệu khóa. Các phản ví dụ V2-R1/R2/R4 là tính tay từ code.
- **Tiêu chí xong:** SPEC nguyên bản vẫn gồm code/fixture/pilot; **Q-74 Q1 đã quyết tách chúng sang T-030**. Phần giao thức/allowlist/bảng bằng chứng/nháp WHY đã có; LOG không nhận đã làm code/pilot hay task xong. WHY-22–35 và D1–D12 vẫn là văn bản chờ duyệt, chưa đủ quyền dùng cho số P3. Không báo việc chưa có đầu ra của T-030 hoặc phân tích schema ở P4 thành lỗi T-022.
- **Phạm vi ghi:** diff tracked chỉ có DECISIONS và STATE; file T-022 đang untracked nên phải đọc trực tiếp. LOG phiên 2 và Q-71/Q-73/Q-74 ghi quyền riêng cho sổ sách/REVIEW/plan. Không thấy bằng chứng một sửa ngoài phạm vi **không được duyệt** trong tập đã đối chiếu; diff này không đủ để quy các file của T-023 cho người làm T-022. Phiên phản biện này chỉ nối thêm REVIEW.
- **Nhãn và đồ thị:** scripts hiện có dùng nhãn để lập allowlist/nhãn phía runner–evaluator; chưa có runner P3 nên chưa chứng minh được cách ly lúc thực thi. Các lõi đã đọc không cần root/fault/case để tính. Luồng CIRCA là trace N → đồ thị gọi/meta → cha hồi quy → z/RHT → DA → metric/service; **RHT-only vẫn dùng đồ thị qua cha hồi quy**. MicroRank dùng quan hệ cha–con và trace–operation trước PageRank/spectrum. TORAI dùng trace để tính Severity/GMM; RCD bên trong nhận metric/log, không nhận call graph. SimpleRCA không dùng parentSpanID, nhưng giữ danh tính service, schema và thống kê trace. So các baseline khác nhau chưa tách riêng hiệu quả của đồ thị; v2 chưa tuyên bố đã làm được. WHY-07/MRP P7 đã giới hạn đúng nhánh “không đồ thị” nếu còn giữ self-time/hồi quy theo cha.
- **DT18/cô và quyết định:** DT18 yêu cầu đồ thị, dữ liệu quan sát, vùng ảnh hưởng/bất thường/xếp hạng và thử dữ liệu công khai trước hệ vé; không quy định TORAI, SVR, bốn tầng hay ngưỡng này. Danh sách ví dụ của cô không biến thành ba thuật toán bắt buộc. Q-64–67/Q-74 là quyết định Minh; D1–D12 là đề xuất. WHY-02/MRP giữ cơ chế tự sinh/kế thừa và khung bốn tầng là ứng viên sau P4; không thấy v2 cam kết chúng từ T-022. Theo lời Minh được ghi cuối LOG/STATE, không áp dụng Q-75 đã bị bác.
- **Bài học/sửa cũ:** đã sửa các lỗi đã được phản biện về MicroRank thiếu nền, lấy điểm TraceRCA trước sort, schema, hòa giữa bảng chính/bảng RCAEval, sentinel/chỉ số BOCPD và chấm báo động thô. Không báo lại chúng. Các lựa chọn khoa học cần thiết đã có mục nháp WHY; việc chưa ghi vào nguồn chung được công khai, chưa dùng cho số P3. Không thêm quyết định hay đổi trạng thái quyết định trong phiên này.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| V2-R1 | Đúng; phạm vi rộng hơn (xem N1); đồng ý CHẶN | `src/torai/torai_sua.py:176–183, 193–200` (z từng cột, max \|z\|), `:188` và dòng tương ứng của `tracets_lat` (chia tổng cả nguồn), `:206–216, 234–235` (`fine2coarse_addup` cộng theo service). Phản ví dụ của reviewer tính lại đúng: X cho s điểm 6/9 = 2/3, Y cho 3/6 = 1/2, dù tổng (service, bin) trùng 100 %. S9 của T-016 ghép theo tên cột và tính cột không ghép là sai (`tasks/T-016-ho-so-torai/SPEC.md:95`); v2 đổi đơn vị nên câu "cho biết B có dựng đúng đặc tả trên TT" (`de-xuat-why-v2.md:95`) mạnh hơn phép kiểm. Lý do v2 gộp về service là "tên cột TT chưa dò được" (`giao-thuc-v2.md:382`). Phiên này dò lại, chỉ đọc, ca dev `re2tt_ts-auth-service_cpu_1`: luật "operation chuẩn hóa (bỏ `/api/v1/`, bỏ `{}`, `_`→`-`, dấu cách và `/`→`-`); span chỉ có tên phương thức HTTP (`GET`, `POST`…) gán cho service của span con" cho đúng 157/157 tên cột của `tracets_err.csv` tác giả, 0 thừa, 0 thiếu. Vậy K-B1 mức cột làm được. **Chưa kiểm:** 29 ca còn lại, giá trị ô. Sửa tối thiểu: K-B1 so theo tên cột với luật trên, tính cột không ghép là sai, giữ ngưỡng 95 % như S9; nếu luật không đúng ở ca khác thì giữ OPEN như reviewer đề xuất. || Duyệt sửa theo đề xuất (06/10; LOG phiên 4 tiếp; Q-76) |
| V2-R2 | Đúng; đồng ý CHẶN cho phần TORAI của §6.6, §8.4, WHY-28 | `torai_sua.py:296` sắp cụm theo điểm, ổn định trên thứ tự `set(y_pred)` (chỉ số cụm GMM, không mang thông tin); `:300–360` nối trọn từng khối cụm. Phản ví dụ đúng: theo khối, E[RR] của A = 2/3, E[Hit@1] = 1/2; theo câu §6.6 "mọi service hai cụm là một nhóm hòa": 25/48 và 1/4. Thêm cách thứ ba: quy tắc chung §8.4 trên khóa tuple (điểm cụm, thứ tự trong cụm) cho nhóm hòa {A, C} ở hạng 1–2: E[RR] = 3/4. Ba quy định, ba kết quả. Sắp phẳng theo tuple ra A, C, B, D, khác `ranks` chính thức, nên phép kiểm "thứ tự dựng lại phải trùng" của §6.6 sẽ báo hỏng đúng ở ca có hòa. Tần suất hai cụm cùng điểm trên 30 ca dev: **chưa kiểm** (điểm cụm là trung bình số thực, có thể hiếm). Sửa tối thiểu: như reviewer: xếp hạng hai cấp, kỳ vọng trên các hoán vị khối của các cụm cùng điểm, giữ thứ tự trong khối, cộng hòa trong khối (nhánh dự phòng: `y_train` bằng nhau). Bỏ câu "mọi service của hai cụm tính là một nhóm hòa". || Duyệt sửa theo đề xuất (06/10; LOG phiên 4 tiếp; Q-76) |
| V2-R3 | Đúng; KHÔNG CHẶN | `giao-thuc-v2.md:84` ghi kết quả có lúc t+300 / t̂+300 cho mọi ranker, nhưng TORAI A dùng bin tới t+305 và ngưỡng `tracets_lat` toàn file (`:178`); BOCPD min–max và bỏ cột hằng trên cả bản ghi (`:202`), nên chính t̂ chỉ có sau cuối file (t+720). §14 và WHY-34 đã khai hồi cứu, nhưng bảng §4, §5.1 và câu "chỉ dữ liệu đã có lúc đó được vào" ở WHY-22 (`de-xuat-why-v2.md:24`) chưa ghi ngoại lệ. Thêm: tập cột N-Sigma chính chọn theo schema cả bản ghi (§10 đã khai), nên dòng chế độ (b) của §4 cũng cần ghi điều này. Ảnh hưởng của schema lên thời điểm báo động N-Sigma: chưa kiểm. Sửa: như reviewer. || Duyệt sửa theo đề xuất (06/10; LOG phiên 4 tiếp; Q-76) |
| V2-R4 | Đúng; KHÔNG CHẶN | Code: `RCAEval/benchmark/evaluation.py:162–184, 203–210`. Chính bài DecompRCA, với phương pháp chỉ trả thứ hạng, lấy C = K phần tử đầu, nên Retrieval@K = top@K (`results/T-018/decomprca.md:16`). "Lỗi truy hồi" khi đó là quy ước định nghĩa, không định vị bước. WHY-23 ("cho P4 biết tìm cơ chế ở bước nào", "lỗi truy hồi hay lỗi xếp lại", `de-xuat-why-v2.md:33, 37`) mạnh hơn bằng chứng. Sửa: đổi hai câu đó thành "root ngoài K đầu hay trong K đầu nhưng không đứng đầu của danh sách cuối"; quy về bước dùng bốn tập của WHY-26 (root ngoài tập quan sát; trong tập quan sát nhưng không được trả về; được trả về nhưng hạng > K). || Duyệt sửa theo đề xuất (06/10; LOG phiên 4 tiếp; Q-76) |
| N1 | Người làm tự tìm — CHẶN (cùng phạm vi V2-R1) | Đặc tả nguồn B (`giao-thuc-v2.md:181–182`) chỉ dẫn quy tắc OB (`dung-logts-tracets.md:22–25`) mà không nêu tên cột và cách gán service cho trace TT. Quy tắc OB áp nguyên cho TT sẽ đặt span `GET` của `ts-seat-service` vào cột `ts-seat-service_GET`; file tác giả gán cột kiểu này cho service của span con (luật ở dòng V2-R1, 157/157 tên khớp ở 1 ca). Gán service khác đổi điểm trace theo service, rồi đổi GMM. Sửa: ghi luật tên cột TT vào §6.6 nguồn B, kèm trạng thái "chưa kiểm ở 29 ca", và dùng cùng luật cho K-B1. || Duyệt sửa theo đề xuất (06/10; LOG phiên 4 tiếp; Q-76) |
| N2 | Người làm tự tìm — KHÔNG CHẶN | Lý do chọn cả bản ghi ở WHY-34 (`de-xuat-why-v2.md:142`) và §7.1 (`giao-thuc-v2.md:197`): "mọi lịch chia đoạn theo vị trí đều gắn với mốc". Cả bản ghi cũng gắn với mốc như vậy: mốc luôn ở giây 720, nên nền trước lỗi luôn đúng 720 s. Câu này không phân biệt hai phương án. Quyết định Q-74 Q11 không đổi; chỉ sửa lập luận: chọn cả bản ghi vì Q-74 Q11, không phải chọn độ dài và bước đoạn, và SPEC cấm chia đoạn để vừa chi phí; thêm giới hạn "nền 720 s cố định ở mọi ca; số phát hiện chỉ nói cho cấu hình này". Ghi chú: Q-75 (Minh đã bác) có nhắc câu này; điểm này nêu từ tự soát, Minh quyết. || Duyệt sửa theo đề xuất (06/10; LOG phiên 4 tiếp; Q-76) |

Ghi chú: điền ngày 06/10/2026, phiên 4 của người làm (Claude). Người làm đã đọc REVIEW.md trước khi tự soát, nên N1, N2 không phải tự soát độc lập hoàn toàn (LOG phiên 4). Lệnh kiểm tên cột chạy từ stdin, chỉ đọc, không ghi file; lệnh và kết quả ghi ở LOG phiên 4.


---

# Phản biện tiếp T-022 — bản V2 sau sửa ngày 06/10/2026

- **Người phản biện:** Codex — **Ngày:** 06/10/2026.
- **Phạm vi:** yêu cầu Minh phản biện tiếp sau review và phản hồi của người làm. Đối chiếu bản V2 đã sửa ở LOG phiên 4 (tiếp); giữ nguyên các phần review và bảng phản hồi trước. Chỉ ghi thêm phần này vào `tasks/T-022-giao-thuc-p3/REVIEW.md`.
- **Nguồn hiệu lực:** AGENTS.md; `docs/STATE.md`; `docs/review-prompt.md`; SPEC và LOG T-022; DECISIONS Q-64–Q-74. Q-74 Q1 đã chuyển code, fixture và pilot sang T-030. Các chi tiết D1–D12 và việc ghi WHY vẫn chờ Minh; không coi việc chưa có đầu ra T-030 là lỗi T-022.
- **Đã đọc/đối chiếu:** các phần REVIEW và phản hồi cũ; `results/T-022/{giao-thuc-v2.md,de-xuat-why-v2.md,cau-hinh/p3-re2tt-v2.json,quy-tac-cot-v2.json}`; JSON/CSV đầu ra T-022; MRP P3/P4 và §6–7, LESSONS, các mục WHY liên quan; DT18 và hướng dẫn cô; code `src/{torai,microrank,circa_kien_truc}/`, TraceRCA RCAEval; hồ sơ/bằng chứng T-013, T-016, T-018. Diff nguồn chung so với `3b1e0dd` đã đọc. File T-022 còn untracked nên đọc trực tiếp; diff tracked không chứa các bản sửa này.

## Kết luận chung

V2-R1, V2-R2, V2-R4, N1 và N2 đã được xử lý trong văn bản hiện tại. V2-R3 đã sửa ngoại lệ TORAI A và BOCPD, nhưng còn thiếu điều kiện về thời điểm có schema của N-Sigma.

Còn một điểm **CHẶN chốt hợp đồng xử lý lỗi BOCPD trước khi chấm khoa học**, và hai điểm **KHÔNG CHẶN** về cận Rerank và thời điểm kết quả N-Sigma. Đây là lỗi/thiếu sót của đặc tả; chưa có bằng chứng một lượt P3 trên TT đã tạo số sai. Các sửa dưới là đề xuất, Minh quyết; phiên này không sửa giao thức, code hoặc nguồn quyết định.

## Các điểm

### V2-S1. Posterior BOCPD không hữu hạn vẫn bị đổi thành chỉ số hữu hạn — CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:218` (§7.2), `:263–271` (§8.3), `:336` (§11.7); `results/T-022/de-xuat-why-v2.md:147` (WHY-34); cấu hình `che_do_b.bocpd`.
- **Bước chịu ảnh hưởng / sai gì:** đầu ra xác suất của BOCPD → `argmax` → điểm đổi → chấm phát hiện/RCA. Đặc tả yêu cầu lấy `m[i] = argmax R[:, i+1]` mà chưa loại posterior không hữu hạn. `argmax` có thể trả một số nguyên dù cột R không còn là phân phối xác suất. Hợp đồng ERROR hiện chỉ nêu ngoại lệ; lỗi số học này không nhất thiết ném ngoại lệ.
- **Bằng chứng:** BARO `e35f4ec`, `baro/_bocpd.py:220` chia cột R cho tổng mass; `:227` trả R. Trường hợp tổng mass bằng 0 đã được T-013 ghi ở `results/T-013/kiem-tra.json:2241–2252`, check `N3-positive-mass-condition`: `zero_mass = 0`, `zero_mass_posterior = [NaN, NaN]`. Hồ sơ `results/T-013/ho-so-bocpd.md` §2, §6 đã nêu underflow (mật độ nhỏ đến mức máy lưu thành 0). Đọc lại đúng posterior từ file kết quả, `isfinite(...).all()` là False nhưng NumPy `argmax` vẫn trả **0**. Nếu mode hợp lệ trước đó lớn hơn 1, bước đổi thành 0 còn thỏa luật nhảy mode và bị gọi là điểm đổi; nếu không, lỗi có thể bị gọi là không báo động.
- **Đoạn đã xét có thể phản bác:** §11.4 có fixture điểm không hữu hạn, nhưng đó là bộ chấm thứ hạng. §11.7 của detector chỉ nêu chỉ số, sentinel, timestamp và warm-up. Quy tắc `ERROR` ở §8.3/D12 không phủ hàm trả bình thường với posterior NaN. Tiền xử lý min–max có thể giảm nguy cơ; fixture T-013 không chứng minh wrapper P3 đã gặp lỗi trên 30 ca TT. Finding chỉ xác định đường lỗi đã biết chưa được hợp đồng xử lý.
- **Hậu quả:** lỗi xác suất có thể được ghi thành báo động/không báo động hợp lệ, làm sai phát hiện và thời điểm RCA. Bỏ sentinel và sửa chỉ số không giải quyết đường này.
- **Đề xuất sửa tối thiểu:** thêm ngay trước `argmax` quy định posterior dùng để quyết định phải hữu hạn và chuẩn hóa hợp lệ; không đạt thì adapter ghi `ERROR` của phương pháp, giữ lượt hỏng và ca trong mẫu số theo Q-74 Q9. Ghi cùng quy tắc vào WHY-34 và cấu hình liên quan. Không điền 0 vào R, không thay recurrence hoặc prior của BOCPD. Đây là xử lý lỗi đầu ra đã biết, không đề xuất thêm cổng hay thực nghiệm.

### V2-S2. Cận theo hạng nhỏ nhất/lớn nhất không phải cận lạc quan/bi quan của Rerank — KHÔNG CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:287–293` (§8.4–8.5); `results/T-022/de-xuat-why-v2.md:86` (WHY-28).
- **Bước chịu ảnh hưởng / sai gì:** phân phối hòa → cận độ đo gộp. Quy tắc lấy hạng nhỏ nhất làm cận lạc quan, hạng lớn nhất làm cận bi quan đúng với Hit/RR/DCG. WHY-28 áp cận cho mọi độ đo, gồm Rerank, nhưng Rerank là tỉ số có mẫu số Retrieval thay đổi theo hạng; nó không đơn điệu theo hạng root.
- **Bằng chứng:** hai ca, K = 5. Ca 1 root cố định ở hạng 1. Ca 2 root hòa hạng 5–6. Giá trị chính theo §8.5 là `1 / (1 + 1/2) = 2/3`. Đặt root ca 2 ở hạng nhỏ nhất 5 cho Rerank `1/2`; đặt ở hạng lớn nhất 6 cho Rerank `1`. Như vậy cận được gọi là lạc quan thấp hơn cận được gọi là bi quan. Phép tính đã kiểm độc lập bằng phân số chính xác, không dùng dữ liệu hay chạy phương pháp.
- **Đoạn đã xét có thể phản bác:** công thức giá trị chính `ΣE[Hit@1] / ΣE[Hit@K]` vẫn đúng với quy ước tỉ số gộp đã chốt. Bootstrap tính lại tỉ số từng mẫu và xử lý Retrieval = 0 cũng không phải lỗi này. Finding chỉ áp cho cách dựng/đặt tên hai cận do hòa.
- **Hậu quả:** báo cáo có thể gắn sai ý nghĩa hoặc dựng sai cận của Rerank; không làm sai các công thức giá trị chính và các độ đo đơn điệu khác.
- **Đề xuất sửa tối thiểu:** giới hạn cận hạng nhỏ nhất/lớn nhất cho các độ đo đơn điệu. Với Rerank, bỏ yêu cầu báo hai cận này, hoặc định nghĩa cận của tỉ số riêng trên các thứ tự hợp lệ. Cách bỏ cận Rerank không cần chạy thêm; giữ nguyên giá trị chính và bootstrap.

### V2-S3. Thời điểm kết quả N-Sigma còn thiếu điều kiện về schema — KHÔNG CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:88,91` (§4), `:325` (§10); `results/T-022/de-xuat-why-v2.md:31` (WHY-22, lý do về thời điểm thông tin). Cùng phạm vi còn sót của V2-R3 và phản hồi người làm về tập cột N-Sigma.
- **Bước chịu ảnh hưởng / sai gì:** nguồn schema → chọn cột detector → thời điểm đủ đầu vào để có kết quả RCA. §4 và §10 khai tập cột BOCPD/N-Sigma chọn theo schema cả bản ghi, là thông tin hồi cứu. Dòng kết quả §4 vẫn ghi `t̂+300` với N-Sigma; ngoại lệ chỉ nêu BOCPD và TORAI A. Đặc tả chưa chỉ ra nguồn schema đã có trước mốc đó.
- **Bằng chứng:** §4: tập cột “chọn theo tên cột có trong file của cả bản ghi”; §10: “tập cột BOCPD/N-Sigma ... dùng cả bản ghi: thông tin hồi cứu”. Bản ghi có 1.441 điểm; với một báo động sớm, `t̂+300` có thể trước cuối bản ghi. Tính nhân quả của mean/std không tự chứng minh schema được xác định trước lúc đó. Code BARO `anomaly_detection.py:7–35` đúng là chỉ dùng các điểm trước i cho mean/std; không cáo buộc code này dùng thống kê tương lai.
- **Đoạn đã xét có thể phản bác:** §7.1 và §14 gọi toàn phép đánh giá là hồi cứu; §10 cũng công khai giới hạn schema. Vì vậy đây không phải rò nhãn bị che giấu. Tuy nhiên, các đoạn đó chưa sửa lời khẳng định thời điểm khả dụng cụ thể trong bảng §4.
- **Hậu quả:** báo cáo có thể nhầm mốc kết thúc cửa sổ RCA với lúc pipeline đã có đủ mọi đầu vào. Chưa khẳng định báo động N-Sigma thực tế đã thay đổi vì schema.
- **Đề xuất sửa tối thiểu:** ghi rõ `t̂+300` chỉ là mốc kết thúc cửa sổ; thời điểm đủ đầu vào còn phụ thuộc nguồn schema. Với schema cả bản ghi như hiện tại, giữ diễn giải hồi cứu và không cam kết kết quả sẵn có ở `t̂+300`. Chỉ dùng cam kết đó khi nguồn schema có sẵn trước mốc được xác định. Đồng bộ phần lý do WHY-22; không yêu cầu đổi N-Sigma hay chạy thêm phương pháp.

## Điều đã kiểm và thấy đúng

- **V2-R1/N1:** K-B1 đã đối chiếu theo tên cột operation, tính cột không ghép là sai. WHY-29 giới hạn phép kiểm vào phần trace dựng theo quy ước tác giả; không coi nó là kiểm log hoặc lưới/ngưỡng riêng của B. Luật tên cột ở 29 ca và giá trị ô vẫn OPEN của T-030, không báo thành lỗi mới.
- **V2-R2:** TORAI đã giữ khối cụm và thứ tự nội bộ. Tính độc lập bằng phân số: công thức xác suất tập con §8.4 trùng duyệt mọi hoán vị với cỡ khối (2,2), (1,3,2), (1,2,3,1); tổng xác suất bằng 1. Ví dụ AB/CD cho E[RR] = 2/3. Hòa nội bộ RCD vẫn được khai là chưa kiểm.
- **V2-R4/N2:** WHY-23 không còn dùng Retrieval/Rerank riêng để định vị cơ chế. Lý do chọn cả bản ghi không còn dựa vào lập luận mọi lịch chia đoạn gắn mốc; giới hạn nền 720 s đã nêu. Không mở lại Q-74.
- **BOCPD/N-Sigma:** sửa chỉ số posterior loại phần tử sentinel; mean/std N-Sigma dùng quá khứ, bắt đầu từ chỉ số 100. Chấm báo động thô và thời gian trơ RCA đã tách riêng. Mẫu số nền theo đặc tả là 620/719 s mỗi ca.
- **Artifact hiện có:** parse nghiêm ngặt 13 JSON của T-022 đạt; allowlist/nhãn đều 30 ca; universe 68 thực thể; CSV BOCPD 30 dòng, 25–48 cột thô/ca. Audit allowlist hiện có ghi `tat_ca_dat = true`; lượt này không băm lại 89 telemetry hay tái chạy phương pháp để lặp bước đã có đầu ra hợp lệ.
- **Code tham chiếu:** kiểm revision các checkout RCAEval, BARO và CIRCA đúng revision được giao. Đã đọc đường lấy điểm/khóa và hợp đồng lỗi liên quan; không sửa runtime hoặc lõi.

## Phép kiểm và giới hạn của phiên

Các lệnh chỉ đọc: `git status --short`, `git diff 3b1e0dd -- docs/DECISIONS.md docs/STATE.md`, `git diff --check`, đọc source bằng PowerShell/rg; Python stdin với `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -` để parse JSON/CSV, đọc fixture posterior có sẵn, tính phản ví dụ Rerank và đối chiếu công thức hòa khối. Không chạy các script tạo đầu ra, benchmark, phương pháp hay thực nghiệm mới; không mở `data/locked/` hoặc repo RCA lưu trữ.

Chỉ nối thêm phần này vào REVIEW. Các phần cũ và bảng phản hồi của Claude giữ nguyên. Đã kiểm sau ghi: phần trước điểm nối khớp nguyên trạng. So snapshot nội dung toàn repo phát hiện thay đổi ngoài REVIEW trong thời gian phiên; các file T-023 có cập nhật đồng thời (bảng điều kiện và script tổng hợp). Vì vậy không khẳng định mọi file ngoài REVIEW giữ nguyên. Các thao tác ghi của phiên phản biện này chỉ nhắm REVIEW; không sửa hoặc hoàn tác thay đổi của T-023. Không commit/push, không thay quyết định hay trạng thái task.

**Cần Minh quyết:** sửa V2-S1–S3 theo đề xuất nào. Việc duyệt WHY-22–35, chi tiết D1–D12, SPEC T-030 và sổ sách còn OPEN như LOG đã ghi; phản biện này không tự đóng các việc đó.

## Phản hồi của người làm cho phần phản biện tiếp (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| V2-S1 | Đúng; đồng ý CHẶN (hợp đồng lỗi, chưa có số sai) | BARO `e35f4ec` `baro/_bocpd.py:220` chia cột R cho tổng; tổng = 0 (mọi `predprobs` tràn dưới về 0) hoặc tổng = ∞ (tràn trên) cho cả cột NaN, và mọi cột sau cũng NaN vì `:211` nhân với cột trước. `MultivariateT.pdf` (`:86–108`) trả mật độ, không phải log, nên tràn số là đường có thật khi d tới 48. NumPy `argmax` trên cột toàn NaN trả 0: sau một chỗ hỏng, `m` thành 0 mãi; nếu `m` trước đó > 1 thì `find_cps` sinh đúng một "điểm đổi" giả, rồi im. `results/T-013/kiem-tra.json` check `N3-positive-mass-condition` cho `zero_mass_posterior = [NaN, NaN]`. §8.3 chỉ định nghĩa `ERROR` là ném ngoại lệ, nên đường này lọt. Bổ sung: điều kiện "mọi phần tử R[:, 1..T] hữu hạn" là đủ, không cần ngưỡng sai số: cột chia cho tổng hữu hạn dương thì hữu hạn và tổng 1; tổng 0 hoặc ∞ thì cả cột NaN. Cùng điều kiện áp cho bản ghi `maxes` gốc (chỉ để đối chiếu). Tần suất trên 30 ca dev: **chưa kiểm** (phải chạy BOCPD; thuộc pilot T-030). Sửa tối thiểu: như reviewer; ghi vào §7.2, §8.3 (thêm "đầu ra vi phạm điều kiện hợp lệ đã khai trước" vào `ERROR`), §11.7 (fixture R có cột NaN → `ERROR`), §15 D12, WHY-34, `cau-hinh` `che_do_b.bocpd`. Không điền 0, không cắt chuỗi tại chỗ hỏng. || Duyệt sửa theo đề xuất (06/10; LOG phiên 5 tiếp 2; Q-76) |
| V2-S2 | Đúng; KHÔNG CHẶN | Tính lại phản ví dụ: ca 1 root hạng 1; ca 2 root hòa hạng 5–6, K = 5. Giá trị chính ΣE[Hit@1]/ΣE[Hit@5] = 1/1,5 = 2/3; root ca 2 ở hạng 5 → 1/2; ở hạng 6 → 1/1 = 1. Cận "lạc quan" thấp hơn cận "bi quan". Nguyên nhân: Rerank là tỉ số gộp, mẫu số đổi theo hạng, không đơn điệu. Các độ đo khác của bảng chính (Hit@k, MRR, NDCG@5, Avg@5, Retrieval@K) đơn điệu giảm theo hạng root, nên cận theo hạng nhỏ nhất/lớn nhất đúng cho chúng. Chỗ sai: `giao-thuc-v2.md:287` ("mọi độ đo ... kèm cận"), `:288` (cận TORAI), WHY-28 (`de-xuat-why-v2.md:86`, "Mọi độ đo ... kèm cận lạc quan và bi quan" có Rerank@1). Sửa tối thiểu: giới hạn cận cho độ đo đơn điệu; Rerank chỉ báo giá trị chính và bootstrap, không báo cận do hòa. || Duyệt sửa theo đề xuất (06/10; LOG phiên 5 tiếp 2; Q-76) |
| V2-S3 | Đúng một phần; KHÔNG CHẶN. Văn bản mâu thuẫn là đúng; hướng sửa của reviewer (bỏ cam kết t̂+300 cho N-Sigma) là sai | Mâu thuẫn có thật: §10 (`giao-thuc-v2.md:325`) gọi tập cột BOCPD/N-Sigma theo cả bản ghi là "thông tin hồi cứu", còn §4 ghi kết quả N-Sigma có lúc t̂+300. Nhưng với N-Sigma, danh sách cột lấy từ cả bản ghi **không đổi báo động tới mọi thời điểm τ**: BARO `anomaly_detection.py:24–34` xét từng cột riêng; báo động ở i chỉ dùng `iloc[:i]` và `iloc[i]` của cột đó; tiền xử lý D9 (`inf → NaN`, `ffill`) là nhân quả, không bỏ cột hằng, không min–max. Cột chưa có dữ liệu trước τ cho `mean`/`std` NaN và phép so `> k·std` sai, nên không báo trước τ. Vậy báo động tới τ giống hệt khi chỉ dùng các cột đã xuất hiện tới τ, và t̂+300 đúng cho N-Sigma (cả tập chính và đối chứng mọi cột). Trường hợp này có thật trên dữ liệu: đếm chỉ đọc 30 ca dev, tập cột BOCPD có 1.108 cột-ca; 53 cột bắt đầu bằng NaN (dài 2–1.414 điểm, trung vị 695), 17 cột toàn NaN (lệnh ở LOG phiên 5 tiếp). Ở BOCPD thì khác: bỏ cột hằng và min–max dùng cả chuỗi, nên hồi cứu là đúng (đã ghi ngoại lệ). Lập luận chỉ đúng khi T-030 cài N-Sigma đúng D9, không thêm bước dùng thống kê cả chuỗi. Sửa tối thiểu: tách câu §10 — BOCPD hồi cứu; N-Sigma lấy danh sách cột theo cả bản ghi nhưng không đổi báo động tới τ (kèm lý do trên); sửa dòng "Bộ phát hiện" §4 tương ứng; thêm lý do vào WHY-34 "Vì sao". Giữ t̂+300 cho N-Sigma. || Duyệt sửa theo đề xuất, gồm hướng của người làm: giữ t̂+300 cho N-Sigma (06/10; LOG phiên 5 tiếp 2; Q-76) |

Ghi chú: điền ngày 06/10/2026 lúc 03:3x, người làm Claude (LOG mục "Phiên 5 (tiếp)"). Người làm đã đọc phần phản biện tiếp trước khi tự soát. Không tìm thêm điểm mới ngoài ba điểm trên. Mọi lệnh chỉ đọc; không chạy phương pháp, không mở `data/locked/`.


---

# Kiểm lại T-022 sau sửa V2-S1–S3 — 06/10/2026

- **Người phản biện:** Codex. Vai trò theo SPEC: Claude làm, Codex phản biện.
- **Phạm vi:** yêu cầu Minh phản biện tiếp sau review, phản hồi và sửa đổi. Đối chiếu bản V2 hiện tại với LOG «Phiên 5 (tiếp 2)». Chỉ nối phần này vào REVIEW; giữ nguyên các phần cũ và bảng phản hồi của người làm.
- **Nguồn đã đối chiếu:** AGENTS.md; STATE; workflow tại `docs/review-prompt.md` và mẫu REVIEW; SPEC, LOG, REVIEW T-022; `giao-thuc-v2.md`, `de-xuat-why-v2.md`, hai cấu hình/quy tắc V2, allowlist, nhãn, mappings, CSV, scripts và audit đã có. Đối chiếu DECISIONS Q-61–Q-74, MRP P3/P4 và §6–7, WHY liên quan, LESSONS, PLAN-P3-G2, DT18 và hướng dẫn cô. Đọc nguồn BARO/RCAEval liên quan đến BOCPD, N-Sigma, RHT và hồ sơ/code CIRCA, TORAI. Checkout RCAEval/BARO/CIRCA đúng các revision được giao trong LOG. Diff tracked so với `3b1e0dd` đã đọc; T-022 còn untracked nên kiểm trực tiếp file.

## Kết luận chung

Các điểm V2-S1–S3 đã được xử lý trong phạm vi đặc tả. Với V2-S3, chấp nhận hướng sửa của người làm: giữ mốc t̂+300 cho pipeline N-Sigma theo D9 và các ngoại lệ đã khai; không giữ đề xuất cũ bỏ cam kết này chỉ vì danh sách cột lấy từ cả bản ghi.

Có **một điểm KHÔNG CHẶN** còn thiếu rõ ràng trong điều kiện chọn mô hình CIRCA: K-SVR2 chưa phân biệt SVR chạy thành công với lỗi bị code bắt rồi chuyển sang z-score. Chưa có bằng chứng đường này đã xảy ra trên TT hoặc đã tạo số P3 sai. Cần làm rõ điều kiện này trước khi dùng K-SVR để khóa mô hình ở T-030. Không có điểm CHẶN mới trong phần đã kiểm; kết luận này không thay việc Minh duyệt WHY, D1–D12 hoặc SPEC T-030.

## Các điểm

### V2-T1. K-SVR2 chưa phân biệt SVR thành công với nhánh dự phòng z-score — KHÔNG CHẶN

- **Ở đâu:** `results/T-022/giao-thuc-v2.md:179–185` (§6.5, nhất là K-SVR2 ở dòng 181); `results/T-022/de-xuat-why-v2.md:114–115` (WHY-30); `results/T-022/cau-hinh/p3-re2tt-v2.json:10` dẫn quy tắc K-SVR1–4.
- **Bước chịu ảnh hưởng / sai gì:** kiểm SVR không dùng nhãn → khóa mô hình CIRCA → tên cấu hình và diễn giải số P3. K-SVR2 yêu cầu «30/30 ca chạy không lỗi, mọi z hữu hạn; ghi số nút không có cha». Nếu «không lỗi» chỉ được kiểm ở đầu ra hàm/tiến trình, điều kiện này vẫn có thể đạt dù hồi quy SVR của nút có cha đã thất bại. Đặc tả chưa yêu cầu phân biệt lỗi hồi quy bị bắt bên trong với nhánh z-score hợp lệ của nút không cha.
- **Bằng chứng:** RCAEval `259ea41`, `D:/RCA-ext/src/RCAEval/RCAEval/graph_heads/rht.py:118–124`: nút không có đầu vào cha dùng z-score trực tiếp; khi `self._score(...)` ném `ValueError`, code ghi warning (cảnh báo) rồi **trả z-score trực tiếp**, không truyền ngoại lệ lên caller. `:144–147` cho thấy đường `ANMRegressor._score` gồm fit, predict và tính residual (phần dư). Với đầu vào y cho z-score hữu hạn, lỗi ở đường hồi quy vẫn cho kết quả trả về hữu hạn; tính lặp lại và thời gian chạy cũng không tự phân biệt hai đường. T-014 đã nêu đúng vấn đề ở `results/T-014/ho-so-circa-pc.md:50,103` và `ho-so-circa-kien-truc.md:70`. Bản giao thức cũ `results/T-022/giao-thuc.md:77` yêu cầu ghi cảnh báo ValueError RHT; bản V2 không đưa ý nghĩa của cảnh báo đó vào điều kiện đạt K-SVR2.
- **Đoạn đã xét có thể phản bác:** «chạy không lỗi» có thể được người cài hiểu là tính cả ValueError đã được ghi cảnh báo. Nếu hiểu và thực hiện như vậy, đường này không đạt K-SVR2. Finding vì vậy là thiếu rõ ràng của hợp đồng, không cáo buộc T-030 đã cài sai. K-SVR1 xác nhận lớp và tham số, nhưng lớp được cấu hình là SVR không chứng minh từng hồi quy đã chạy SVR. Ghi số nút không cha chỉ bao phủ nhánh hợp lệ, không bao phủ lỗi của nút có cha. Diagnostics mẫu §13 có `fallback_clusters` cho TORAI; chưa xác định trạng thái fit của RHT.
- **Hậu quả:** người cài có thể khóa và gọi cấu hình là SVR chỉ từ đầu ra hữu hạn, trong khi một phần điểm đã dùng y trực tiếp thay cho residual của SVR. Khi đó diễn giải P4 về hồi quy theo cha hoặc về mô hình SVR sẽ mạnh hơn bằng chứng. Số nút/ca bị ảnh hưởng trên TT **chưa kiểm**: chưa chạy đường SVR P3; việc đó thuộc T-030.
- **Đề xuất sửa tối thiểu:** làm rõ **chính K-SVR2 hiện có**: ở các nút có đầu vào cha hiệu lực, ghi trạng thái hồi quy và số/nội dung ValueError bị RHT bắt; đường lỗi chuyển sang z-score không được tính là SVR chạy thành công để đạt K-SVR2. Nút không có cha hiệu lực vẫn dùng z-score hợp lệ theo code tác giả. Nếu K-SVR không đạt, xử lý theo quy tắc chọn mô hình đã trình ở D5/Q-74 Q6. Đồng bộ câu K-SVR2 trong WHY-30 và cấu hình dẫn nó. Không sửa lõi RHT, không đặt ngưỡng mới, không thêm cổng hay thực nghiệm.

## Điều đã kiểm và thấy đúng

- **V2-S1:** §7.2 đã kiểm R[:, 1..T] hữu hạn trước `argmax`; không đạt thì ERROR, giữ ca trong mẫu số, không chấm điểm đổi hoặc chạy RCA. §8.3, §11.7, D12, WHY-28/34 và cấu hình BOCPD đã phản ánh đường lỗi posterior được nêu ở review trước. Không khẳng định đã đo tần suất lỗi trên TT.
- **V2-S2:** §8.4 và WHY-28 đã giới hạn cận theo hạng cho các độ đo đơn điệu. Rerank chỉ có giá trị chính và bootstrap. Phản ví dụ hai ca vẫn cho 2/3, 1/2, 1; không lặp điểm này thành lỗi tồn đọng.
- **V2-S3:** `baro/anomaly_detection.py:24–34` xét từng cột riêng; ở i chỉ dùng giá trị trước i và tại i. D9 chỉ đổi inf thành NaN rồi ffill theo quá khứ. Cột chưa có dữ liệu tới τ không sinh báo động trước τ; thêm tên cột đó vào schema không đổi tập báo động tới τ. Vì vậy hướng giữ t̂+300 của người làm có cơ sở với N-Sigma theo D9. Ngoại lệ BOCPD và TORAI A vẫn được khai trong §4/WHY-22; không suy kết luận này thành tính trực tuyến của toàn phép đánh giá.
- **Sửa V2-R1/R2/R4 và N1/N2:** K-B1 đã so theo tên cột và tính cột không ghép là sai; TORAI giữ khối cụm và thứ tự nội bộ; WHY-23 không còn định vị bước cơ chế chỉ bằng Retrieval/Rerank; lý do chọn cả bản ghi không còn dựa vào lập luận cũ về vị trí mốc. Phép tính thuần của công thức hòa khối khớp duyệt mọi hoán vị ở 9 trường hợp root/khối thuộc các cỡ (2,2), (1,3,2), (1,2,3,1).
- **Artifact:** 13 JSON parse nghiêm ngặt đạt, không khóa trùng hoặc hằng NaN/Infinity; 4 script parse cú pháp đạt. Allowlist/nhãn cùng 30 mã, 10 ô; mọi root thuộc universe 68. Universe tính lại từ schema metadata khớp; CSV BOCPD có đúng 30 ca, 25–48 cột thô/ca. Audit hash có sẵn ghi 89/89 file khớp T-017 và không có file thiếu đối chiếu. Không băm lại telemetry hoặc tái chạy script tạo đầu ra để lặp bước đã có artifact hợp lệ.
- **Phạm vi:** Q-74 Q1 đã chuyển code, fixture và pilot sang T-030. Việc chưa chạy SVR, TORAI B, chưa đo BOCPD hoặc chưa ghi WHY hiệu lực không tự là kết quả sai của T-022. Các giới hạn đó vẫn phải giữ OPEN; chưa dùng chúng như bằng chứng đã kiểm.

## Phép kiểm, phạm vi ghi và việc còn OPEN

Lệnh chỉ đọc: đọc file/nguồn bằng PowerShell và rg; `git status --short`, `git diff 3b1e0dd -- docs/DECISIONS.md docs/STATE.md`, `git diff --check`; kiểm revision checkout. Python stdin với `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -` dùng để parse JSON/CSV/script, đối chiếu metadata/audit đã có và tính thuần. Không gọi các phương pháp, chạy benchmark/thực nghiệm mới, mở telemetry, dữ liệu khóa hoặc repo RCA lưu trữ.

Phiên này chỉ nối thêm REVIEW.md. Không sửa LOG, STATE, SPEC, giao thức, code, WHY hoặc DECISIONS; không commit/push và không thêm/thay quyết định của Minh. Các bảng phản hồi trước giữ nguyên. Điểm V2-T1 là đề xuất để Minh quyết.

Những việc chờ đã ghi ở STATE/LOG vẫn còn: văn bản WHY-22–35 và D1–D12, SPEC T-030, ghi sổ hai lời duyệt sửa, cùng mâu thuẫn sổ sách Q-75. Không dùng kết luận phản biện này để tự đóng task hoặc giải quyết các việc đó.

## Phản hồi của người làm cho phần kiểm lại (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| V2-T1 | Đúng; KHÔNG CHẶN; phạm vi rộng hơn reviewer nêu | RCAEval `259ea41` `graph_heads/rht.py:118–124`: nút không cha → `_zscore`; `ValueError` trong `_score` → `warning` rồi `_zscore`, không ném lên caller. `:133–147`: `ANMRegressor._score` gồm fit, predict, phần dư, `_zscore`. Có `ValueError` riêng của SVR mà OLS không có: sklearn 1.6.0 `svm/_base.py:275` ("The dual coefficients or intercepts are not finite… input data may contain large values"). Khi đó z trả về vẫn hữu hạn, nên K-SVR2 ("không lỗi, mọi z hữu hạn", `giao-thuc-v2.md:181`) vẫn đạt. **Rộng hơn:** cùng đường bắt lỗi áp cho OLS (`ANMRegressor` mặc định `LinearRegression()`, `rht.py:135`), nên tên "OLS+RHT+DA" cũng có thể mạnh hơn bằng chứng; bản ghi §13 không có trường route hồi quy của CIRCA. T-014 đã phân ba route mức nút: `no_effective_parents`, `linear_regression`, `value_error_fallback` kèm thông điệp (`src/circa_kien_truc/scoring.py:44–57`; `results/T-014/runs/regression-route-summary.json`: 0 nút `value_error_fallback` ở các lượt ví dụ, không phải 30 ca). Sửa tối thiểu: như reviewer (nút có cha hiệu lực mà rơi `value_error_fallback` dưới SVR thì K-SVR2 không đạt), thêm: ghi route và thông điệp từng nút cho mô hình được khóa, cả OLS, vào `diagnostics` §13; báo số nút `value_error_fallback` cạnh bảng CIRCA. Mặt trái của sửa: `ValueError` do kiểm đầu vào (NaN/inf) xảy ra như nhau với OLS; khi đó chuyển sang OLS không bỏ được nhánh dự phòng; số nút rơi được báo là giới hạn của cấu hình OLS, không thêm cổng. Tần suất trên 30 ca TT: **chưa kiểm** (phải chạy CIRCA; thuộc T-030). || Duyệt sửa theo đề xuất (06/10; LOG phiên 6 tiếp; Q-76) |
| N3 | Người làm tự tìm — KHÔNG CHẶN | `giao-thuc-v2.md:274` (§8.3) định nghĩa `TIMEOUT` là "vượt giới hạn thời gian đã khai". Giao thức, cấu hình và WHY-28 không khai giới hạn nào, không nói khai ở đâu. Cũng không nói ca chưa chạy khi hết ngân sách tổng (Q-40: 3 giờ/phương pháp/dataset; Q-72: BOCPD 20 giờ) tính thế nào. Q-74 Q9 và §8.3 đã chốt `TIMEOUT` ở mẫu số, tính trượt. Nhưng Q-67 có tiền lệ khác: CIRCA-PC trên TT báo "không chạy đủ trong ngân sách", không báo số. Hai cách cho bảng khác hẳn. Để T-024/T-025 tự chọn giới hạn sau khi thấy thời gian chạy là chọn sau khi nhìn kết quả. Sửa tối thiểu (§8.3, WHY-28): giới hạn mỗi lượt khai trong SPEC của task chạy (T-030 pilot, T-024, T-025) trước khi chạy. Với ngân sách tổng: nếu phép chiếu pilot vượt ngân sách thì quyết trước khi chạy theo kiểu Q-67; nếu đã cam kết chạy đủ cohort mà hết ngân sách giữa chừng thì ca chưa chạy là `TIMEOUT` (Q-74 Q9). Minh chọn. || Duyệt sửa theo đề xuất (06/10; LOG phiên 6 tiếp; Q-76) |

Ghi chú: điền ngày 06/10/2026 lúc 03:57–04:0x, phiên 6 của người làm (Claude; LOG "Phiên 6"). Người làm đã đọc phần kiểm lại trước khi tự soát, nên N3 không phải tự soát độc lập. Lệnh chỉ đọc; không chạy phương pháp, không mở `data/locked/`.

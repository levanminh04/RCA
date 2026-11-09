# LOG T-056

## 08/11/2026 — Claude, Windows điều khiển EC2, người làm

Mở phiên. Nguồn quyền `results/T-056/minh-duyet.txt`.

### Kết thúc — 08/11/2026

1. **Đã làm.** 2.1–2.5 theo SPEC. Số đếm theo mã mờ trên hai EC2 (`signals_ec2.py`, `redis_diskio_ec2.py`). Ghép nhãn và phân tích trên laptop (`phan_tich.py` → `ket-qua.json`). Báo cáo: `results/T-056/bao-cao.md`. Không chạy phương pháp.
2. **File.** `tasks/T-056-phan-tich-bo-sung/`, `results/T-056/**`, dòng T-056 trong STATE. Trên EC2: `/home/ubuntu/rca-p7/T-056/signals_ec2.py`.
3. **Kiểm.**
   - z tính lại khớp s của M1 ở 2634/2634 (TT) và 273/273 (RE3) kênh metric.
   - Điểm BARO của `redis_diskio` bằng max(A) ở 30/30 ca.
   - `phan_tich.py` chạy hai lần cho cùng sha256.
   - Lượt chạy đầu `signals_ec2.py` lỗi ghi JSON (`numpy.bool_`); đã sửa ép kiểu rồi chạy lại.
4. **Cần Minh quyết / mở.**
   - Kết quả T-056 đính chính diễn giải ở hai báo cáo trước:
     - RE3 §4 "cơ chế 1" cần tách z từ max(A) với IQR = 0;
     - RE3 §6 đề xuất "kênh status span" phải sửa thành "gán lỗi theo cạnh, cần trace đủ";
     - log bị chặn không phải nguyên nhân duy nhất.
   - Chưa sửa hai báo cáo đó; chờ Minh duyệt sửa hoặc để G4 ghi đính chính.
   - OB 2.3 chỉ có dấu hiệu thay thế.
   - Chưa commit.

**Bước tiếp.** Minh chọn: sửa đính chính trong báo cáo RE3/P7(a), hay ghi vào G4. Chuyển prompt dưới cho Codex.

### Prompt phản biện cho Codex — Minh chọn chuyển, không tự gửi

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-056, tasks/T-056-phan-tich-bo-sung/ (SPEC.md, LOG.md); báo cáo results/T-056/bao-cao.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P7 phân tích bổ sung sau khi xem (TT, Nezha-OB, RE3-OB); chuẩn bị G4.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (SPEC T-056).
- Tài liệu gốc: tasks/T-056-phan-tich-bo-sung/SPEC.md; tasks/T-056-phan-tich-bo-sung/LOG.md; results/T-056/minh-duyet.txt; results/T-056/{bao-cao.md, ket-qua.json, manifest-001.json}; results/T-055/reports/re3/bao-cao-re3.md và results/T-054/reports/p7a-013-v2/bao-cao.md (các báo cáo được đính chính diễn giải); git diff từ commit 601be1a1 trên branch claude/sweet-hawking-dy078d.
- Phản biện và phản hồi trước: không có cho T-056.
- Code và kết quả liên quan: results/T-056/scripts/{build_requests.py, signals_ec2.py, redis_diskio_ec2.py, phan_tich.py}; results/T-056/runs/{yeu-cau-001, ec2-001}/; kết quả đã chấm results/T-054/reports/{main-013-v2, re3-ban-cuoi-001}/; trung gian M1 trong bản nhận T-054/T-055; code src/m1/e4.py, src/m1/xep_hang.py. Lệnh: py -3 -B results/T-056/scripts/phan_tich.py <đường-dẫn-ra-ngoài-repo.json>. Quyền đọc dữ liệu: kết quả, trung gian và parquet TT/OB/RE3 đã mở theo grant T-054/T-055; không chạy phương pháp.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cho phép ghi đúng một bản phản biện mới trong tasks/T-056-phan-tich-bo-sung/ theo tasks/_MAU/REVIEW.md.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

### Phần 2 — 08/11/2026 (Minh: "Ghi vào T-056")

- **Câu hỏi của Minh:** còn pattern nào khác không; vì sao SimpleRCA cao nhất; có phải do dữ liệu đơn giản; phân loại mức I/II/III.
- **Làm:**
  - `rules_ec2.py` tính lại trên EC2 (TT 60, RE3 30), theo mã mờ, không nhãn, bốn quy tắc đơn giản theo service. Kết quả ở `runs/ec2-002/`.
  - `phan_tich_002.py` ghép nhãn trên laptop → `ket-qua-002.json`. Báo cáo: mục "Phần 2" của `results/T-056/bao-cao.md`.
  - Bản tính đầu chạy trong scratchpad, cho cùng số; đã chép script và đầu ra vào repo.
  - Manifest mới: `manifest-002.json`; giữ `manifest-001.json`.
- **Kết quả chính:**
  - R1 (đếm mẫu vượt 3σ) tái lập M4: hạng 1 trùng 60/60 (TT) và 30/30 (RE3), MRR bằng nhau.
  - TT/RE3 "đơn giản" theo nghĩa root lệch bền nhất (48/60, 28/30).
  - R1 đúng ở 6/7 ca M1 sai; M1 hơn R1 ở 12 ca lỗi mạng TT.
  - Độ khó theo dữ liệu: TT I 48 / II 12 / III 0; RE3 I 28 / II 1 / III 1.
- **Chưa:** R1 trên OB thô; lần từng ca của 12 ca TT; chưa commit. Codex phản biện gộp cả hai phần (prompt cũ của T-056 vẫn dùng được; tài liệu gốc thêm `ket-qua-002.json` và `manifest-002.json`).

## 08/11/2026 — Claude, Windows, người làm — Đáp phản biện

Mở phiên. Nguồn quyền ghi: Minh cho phép ghi gói bốn file Codex đề xuất (`dinh-chinh-001.md`, `manifest-003.json`, LOG, dòng STATE) nếu Claude không còn mâu thuẫn với Codex; yêu cầu rà thêm phần khác, kiểm chính xác.

### Điểm tự tìm trước khi đọc kết luận phản biện (lượt chat đầu)
- N1 CHẶN: "M1 thắng nhờ E1/E2" (báo cáo dòng 139–141, 160) chưa đối chiếu C-a0.
- N2 KHÔNG CHẶN: "M4 = R1", "phiếu trace/log không đổi hạng 1" mạnh hơn phép đếm (chỉ so đúng/sai root).
- N3 KHÔNG CHẶN: "I/O không bất thường" chưa có căn cứ.
- N4 KHÔNG CHẶN: mô tả cơ chế TORAI dòng 68 sai; chưa đọc code khi viết.
- N5 KHÔNG CHẶN: "M1 0,875 trên OB nhờ E1/E2" chưa đối chiếu.

### Kết luận từng điểm phản biện
| Điểm | Kết luận | Bằng chứng riêng của Claude |
|---|---|---|
| R1 | Đúng | C-a0 RR = 1 ở 12/12 ca (K2 `#/tom_tat/RE2-TT/ca_lech_M1_R1`); cấu hình `src/m1/chuoi.py:37` |
| R1 lượt 2: E3b | Đúng | `results/T-054/protocol.json`: M1 và C-a0 đều E3 = false, E3b = false |
| R1 lượt 2: OB | Đúng | B: M1 so bo-E1 8/25/1, bo-E2 7/25/2, C-a0 11/20/3 |
| R1 lượt 2: 3 ca auth | Đúng | Bản ghi M1 (2 bản/ca) có 55 cạnh, 0 cạnh chứa ts-auth-service |
| R1 lượt 2: không ghi đè báo cáo | Đúng | `results/T-056/` chưa track trong git; ghi đè làm mất byte manifest-001/002 ghim |
| R2 | Đúng | RR root R1 = M4 ở 60/60, 30/30; script dòng 81 chỉ so đúng/sai. Số 16/7 chưa kiểm độc lập |
| R3 | Đúng | Không có số nào xác nhận I/O bình thường |
| TORAI | Đúng phần code | `torai_sua.py`: chuẩn hóa, fillna(0), mean, GMM. Số 90/30/27/23 chưa kiểm độc lập |

Không có mâu thuẫn với Codex. Phần lượt 1 Claude nói "tần suất" là phần chung: sai, đã rút (D1a).

### Rà thêm (Codex chưa kiểm)
- D6: TORAI B trên OB là `UNSUPPORTED` 34/34, K `#/2_5_vi_tri_N` ghi MRR 0.
- D7: "một thống kê đơn lẻ là đủ, không cần đồ thị" nói quá; thu về 48/60, 28/30.
- D8: "phân loại theo dữ liệu đúng hơn" không có tiêu chí.
- D9: lý do nhóm vị trí N ("không cần cạnh") là ứng viên chưa kiểm; RE3 M1 = C-a0 = 0,925.
- D10: "root span lỗi tăng 0/30" thực là 0/18; 12 ca giá trị rỗng do root vắng trace.
- Các số 2.1–2.5 còn lại khớp K.

### Kết thúc
1. **Đã làm.** Kiểm ba điểm sửa của Codex và ý ba ca auth; rà phần còn lại của báo cáo; ghi đính chính.
2. **File.** Tạo `results/T-056/dinh-chinh-001.md`, `results/T-056/manifest-003.json` (24 file; byte cũ không đổi so với 002; trỏ manifest-002). Nối LOG này. Sửa dòng T-056 trong `docs/STATE.md`. Không sửa `bao-cao.md`, K, K2.
3. **Kiểm.** manifest-002 khớp 21/21 trước khi ghi; các lệnh đếm ở bảng trên chạy trực tiếp trên file.
4. **Mở / cần Minh.** Phần chung tạo lợi thế trước R1; phân rã E1/E2/E5 trên OB; R1 trên OB; bất thường thực của redis_diskio; hai phân tích ứng viên của Codex chưa duyệt. Dừng phản biện R1–R3 không là nghiệm thu T-056. D6–D10 chờ Codex kiểm. Chưa commit.

**Bước tiếp.** Minh chuyển prompt dưới cho Codex kiểm D1–D10 (đặc biệt D6–D10), hoặc nghiệm thu. Lệnh cuối: tạo manifest-003 bằng Python một dòng (sha256 mọi file trong `results/T-056` trừ chính nó).

### Prompt cho Codex kiểm lại — Minh chọn chuyển, không tự gửi

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-056; tasks/T-056-phan-tich-bo-sung/.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: phân tích sau P7(a) và RE3, chuẩn bị G4.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện.
- Tài liệu gốc: tasks/T-056-phan-tich-bo-sung/{SPEC.md,LOG.md}; results/T-056/{bao-cao.md,dinh-chinh-001.md,ket-qua.json,ket-qua-002.json,manifest-001.json,manifest-002.json,manifest-003.json,minh-duyet.txt}; phần T-056 trong docs/STATE.md. Đọc trực tiếp cây làm việc chưa commit.
- Phản biện và phản hồi trước: theo thứ tự: phản biện Codex (chat), phản hồi Claude (chat), kiểm lại Codex (chat), phản hồi và gói sửa Claude ghi ở mục LOG ngày 08/11/2026 "Đáp phản biện". Chưa có REVIEW.md của T-056.
- Code và kết quả liên quan: results/T-056/{scripts/,runs/}; results/T-054/reports/{main-013-v2,p7a-013-v2,re3-ban-cuoi-001}/; results/T-054/protocol.json; results/T-055/reports/re3/ cùng các manifest hiện hành; src/m1/, src/p3/, src/simplerca/, src/torai/. Python D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -X utf8 -B. Đọc kết quả, trung gian, nhãn đã chấm và CSV chuẩn bị đã lưu theo quyền T-054/T-055; không chạy phương pháp mới trên test hoặc chọn, đổi thiết kế từ test.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền sửa file, LOG, STATE hoặc tạo bản phản biện.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```


## 09/11/2026 — Claude, Windows, người làm (khép task)

- Minh: “T56 chạy xong chưa ? rồi thì khép 3 task lại, trình kế hoạch tiếp theo”. T-056 đã chạy và đáp phản biện xong; Codex chưa kiểm lại lượt cuối. Minh nghiệm thu T-054, T-055, T-056 ngày 09/11/2026. Các câu hỏi khoa học OPEN giữ nguyên; nghiệm thu không xác nhận cơ chế hay hiệu quả.

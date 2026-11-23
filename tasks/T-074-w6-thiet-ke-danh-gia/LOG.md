# Nhật ký T-074

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 0 — 20/11/2026 — Claude (phiên điều phối T-070) — laptop Minh — vai trò: điều phối, khởi tạo task

- Tạo SPEC theo kế hoạch bản 5 (`tasks/T-070-dieu-phoi-giai-doan-2/SPEC.md`) và quyền Minh cho phiên điều phối (chat 20/11/2026, nguyên văn ở SPEC T-070): "… nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình". Phần "chờ Minh" trong SPEC chưa được duyệt.
- Hợp đồng giữa phiên: `tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md`; lịch máy: `LICH-MAY.md`. Phiên làm việc báo về điều phối khi kết thúc mỗi lượt (I15).
- Prompt Codex soát SPEC: ở LOG T-070 (gom cho T-070–T-075), Minh chuyển.

---

## Phiên 1 — 20/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm

- Mở phiên theo AGENTS §6; đọc AGENTS, STATE, SPEC T-074, HOP-DONG và SPEC T-070. Lượt này: SPEC bước 1–3 (thiết kế, không máy).
- 13:01Z — Bước 1 xong (chỉ đọc): MRP §2–§3, P7, P9, P10, §6–§7; DT18; hướng dẫn cô; LESSONS; KE-HOACH-GIAI-DOAN-2 §8; thong-nhat §1; lich-su/04; T-069 dinh-chinh-1, bang-theo-o-2; T-059 danh-muc-loi (quy tắc nhãn, ô đánh giá); T-063 o-dev-bo-sung; T-064 ho-so-chon, cau-hinh-de-xuat, hop-dong-dau-ra; T-043 SPEC B1.9, D3, D13, D14; WHY-17; DECISIONS (T-059, Q-201); SPEC T-071/T-072/T-073; results/T-071 e0, e1/suc-chua.json. Repo lab 407b4f5 (chỉ đọc): runner4.py, safe_export.py, stage_m1.py, inj3.py, toxiproxy/proxies.json, purchase-journey.js, collector agent (httpcheck). FlashTicket 36a3725 (chỉ đọc): RcaFaults/RcaFaultsWebConfig của Booking, Event. Không dùng máy, không SSH.
- 13:05Z — Bước 2: ghi `results/T-074/thiet-ke-w6.md` (14 mục theo §8.3 W6; mỗi lựa chọn có trạng thái ĐX/CHỜ-MINH/CHỜ-W4/CHỜ-W5/ĐÃ-KIỂM/CHƯA-KIỂM). Số thời lượng chu kỳ tính lại: 31,40 phút/chu kỳ trên 17 chu kỳ `t069-chinh`; V082 49,9 giây/ca (hai lần chạy, 16 ca) — lệnh python đọc `results/T-069/thu/t069-chinh/chay/nhat-ky-3.jsonl`.
- 13:05Z — Bước 3a: `results/T-074/du-toan.json` sinh bằng `results/T-074/du_toan.py` (`py -3 -I results/T-074/du_toan.py results/T-074/du-toan.json`). Kết quả: A 27 chu kỳ/14,1 giờ; A+CPU-EVENT 33/17,3; A+B 51/26,7; A+B+CPU-EVENT 57/29,8; sức chứa còn lại sau W4+W5 tối đa 47.698 vé → A+B vượt theo giả định bảo thủ.
- 13:08Z — Bước 3b: `de-xuat-why.md` (13 mục W6-A…W6-M), `cau-hoi-minh.md` (Q-W6-01…08, mỗi câu có đề xuất, mặt trái, phương án khác). Tự kiểm: soát lại bằng code các khẳng định về nhóm che (V082 chỉ `H5-liveness` khai `can_bo_sung`; `src/m1_ft/chay_ca.py:96`, `thanh_phan/h4_h5.py:93`) → sửa dòng "G-span-attr" thành "không thuộc V082"; sửa số đơn ở §5.3, §5.5, §11 cho khớp `du-toan.json`; hạ "3 ô chắc chắn" xuống "3 ô có sẵn cơ chế tiêm, chưa xác nhận"; ghi rõ 0,80 của SimpleRCA là số công bố. `du-toan.json` đọc lại bằng `json.load` đạt. Manifest `results/T-074/SHA256SUMS` (5 file).

### Kết thúc phiên 1 — 13:08Z

**1. Đã làm gì.** SPEC bước 1–3: đọc nguồn trực tiếp; soạn hồ sơ thiết kế W6 theo từng mục §8.3 W6; dự toán (sinh bằng script) có mục lỗi 10/50/99%; đề xuất WHY; câu hỏi Minh. Bước 4 (báo điều phối, prompt Codex): prompt ở cuối mục này; báo điều phối bằng báo cáo cuối lượt.

**2. File đã thay đổi.** `results/T-074/` (mới): `thiet-ke-w6.md`, `de-xuat-why.md`, `du-toan.json`, `du_toan.py`, `cau-hoi-minh.md`, `SHA256SUMS`. `tasks/T-074-w6-thiet-ke-danh-gia/LOG.md` (nối). Dòng T-074 trong `docs/STATE.md` (Edit). Không ghi WHY/DECISIONS/MRP, không sửa code, không dùng máy, không commit.

**3. Kiểm đã chạy.** Thời lượng chu kỳ 31,40 phút (17 chu kỳ `t069-chinh`) và thời gian V082 tính lại từ `nhat-ky-3.jsonl`; số dự toán sinh bằng `du_toan.py`; `du-toan.json` hợp lệ JSON; các dẫn dòng code (`RcaFaults.java`, `RcaFaultsWebConfig.java`, `inj3.py`, `proxies.json`, `purchase-journey.js`, `agent-docker-host.yaml`, `safe_export.py`, `runner4.py`, `chay_ca.py`, `h4_h5.py`) đọc trực tiếp. Không có phép kiểm động nào (không máy).

**4. Chưa chắc / cần quyết.**
- Task đạt: hồ sơ đủ mục §8.3 W6, mỗi lựa chọn có trạng thái; dự toán có số; câu hỏi gom một lần. Chưa phản biện.
- Câu hỏi nguồn: chưa trả lời RQ5/RQ3 trên FlashTicket (việc của W7). Hồ sơ chỉ ra kết luận sẽ hẹp: trên bản ghim chỉ 3 ô đánh giá có sẵn cơ chế tiêm (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE), CPU-EVENT có điều kiện quota; 4 ô cần proxy mới (đổi topology); 3 ô cần đổi image/tải; DB-BOOK-DOWN OPEN. Chưa ô nào được đầu dò xác nhận.
- Chờ W4: chọn chính sách DB (K0/K2/K3), tiêu chí khỏe, quy tắc gom, G. Chờ W5: bộ xuất theo t̂, độ trễ (b), D13. Chờ E6: khôi phục có nhất quán với Redis/RabbitMQ không.
- Thiếu bằng chứng: thời hạn vòng ghi Collector (quyết định chụp gói trong đợt là bắt buộc); k6 có ghi từng request không (R-07 tùy chọn, nhãn vùng); thời gian RCA batch, khôi phục DB, chụp gói trong đợt.
- **Gấp cho điều phối:** Q-W6-08 — hạn bán 02/12 22:16Z và sức chứa (A+B+CPU-EVENT cần tới 74.520 vé bảo thủ, còn 47.698 sau W4+W5 tối đa). I13 chỉ cho sửa DB ở E1 (đang mở) hoặc E6.
- Khối cổng G6 không có trong `docs/review-prompt.md`; prompt dùng khối G3 và ghi rõ điều này.

**I15.** Tài nguyên đang giữ: không. Job server: không. Việc cần điều phối quyết: Q-W6-08 (gấp, liên quan E1); Q-W6-02/03 nếu muốn proxy hoặc quota Event có mặt từ W4 E4; trình `cau-hoi-minh.md` cho Minh; chuyển prompt dưới cho Codex.

**Bước tiếp theo chính xác.** Minh trả lời `results/T-074/cau-hoi-minh.md`; Codex soát theo prompt dưới. Sau đó người làm đáp phản biện, cập nhật hồ sơ (bản 2). Phần CHỜ-W4/CHỜ-W5 cập nhật khi T-071/T-072/T-073 có kết quả. E6 cần SPEC bổ sung trước khung S5. Gói code W7 (runner thu-niêm, `safe_export case-input`, ô đánh giá trong `inj3.py`, adapter baseline, cấu hình bản che) cần SPEC riêng.

**Lệnh cuối đã chạy.** `sha256sum` năm file `results/T-074/` → `SHA256SUMS`.

### Prompt cho Codex — soát kết quả T-074 (phiên 1)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — W6 khóa bản và thiết kế đánh giá, `tasks/T-074-w6-thiet-ke-danh-gia/`.
- Công đoạn: soát kết quả (đầu ra thiết kế của SPEC bước 1–3).
- Gói/cổng: P9, P10 — chuẩn bị G6. `docs/review-prompt.md` chưa có khối cổng G6; khối dưới là khối G3 (khóa thiết kế trước khi dùng dữ liệu đánh giá).
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: `tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md`, `LOG.md`; `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8; `tasks/T-070-dieu-phoi-giai-doan-2/SPEC.md`, `HOP-DONG.md`; `docs/techstack/ban-giao-dieu-phoi-2026-11-20/thong-nhat.md`; các đầu vào ở mục "Đầu vào" của SPEC T-074. Các file chưa commit (không có git diff gốc).
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: `results/T-074/` (`thiet-ke-w6.md`, `de-xuat-why.md`, `du-toan.json`, `du_toan.py`, `cau-hoi-minh.md`; manifest `results/T-074/SHA256SUMS`; tái tạo: `py -3 -I results/T-074/du_toan.py results/T-074/du-toan.json`). Repo lab `D:/Project/flashticket-rca-lab` `407b4f5` (chỉ đọc); FlashTicket `D:/Project/flash-ticket-platform` `36a3725` (chỉ đọc).
- Phạm vi ghi được Minh cho phép trong lượt này: [Minh điền: chỉ trả lời trong chat, hoặc `tasks/T-074-w6-thiet-ke-danh-gia/REVIEW.md`].

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

---

## Phiên 2 — 21/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm

- Mở phiên theo tin của điều phối T-070 (20/11): Minh duyệt D2 ("Duyệt cả năm", LOG T-070 lượt 6) và R9 (LOG T-070 lượt 3) — đã đối chiếu nguyên văn trong LOG T-070. Việc: sửa theo CX-06 (`results/T-070/codex/CX-06-tin-cuoi.md`) điểm 7, 8, 9, chỉ trong `results/T-074/`, ghi bản mới, không đổi bản cũ. Không dùng máy.
- Kiểm bản 1 theo `results/T-074/SHA256SUMS`: 5/5 OK (trước và sau khi sửa).
- Điểm 9: đọc code tác giả `D:/RCA-ext/src/RCAEval` (HEAD `259ea41`, `git status` sạch): `e2e/baro.py:23–51`, `io/time_series.py:4–5, 12–20, 45–54, 99–115`; local `src/p3/cua_so.py:72–94`, `src/p3/adapters/baro.py`, `src/p3/ban_ghi.py:7–9`. Danh sách cột trước xử lý: đọc `#/coverage` của `results/T-069/dau-ra/dev3/d0/P7/03573b63/method-output-1.json` (sha256 khớp `results/T-069/SHA256SUMS`): 61 cặp (thực thể, kênh), 17 thực thể, kênh cpu 12, mem 12, error 8, latency-50 8, latency-90 8, workload 8, db-size 5.
- 02:44Z — Ghi bản 2: `thiet-ke-w6-2.md` (sửa §4.3 theo D2; §5.3 theo điểm 7: K0 + K3 là đề xuất, K2 ứng viên khi E6 chứng minh khôi phục nhất quán, trôi E2→E4 chỉ mô tả; §5.5 theo R9; §7 + §7.1 mới theo điểm 9; §8.4–§8.5 và §9.1 theo điểm 8), `de-xuat-why-2.md` (W6-A, W6-G, W6-I, W6-K), `cau-hoi-minh-2.md` (Q-W6-01, 02, 03, 08). Manifest `SHA256SUMS-2` (3 file). `du-toan.json` không đổi.

### Kết thúc phiên 2 — 02:44Z

**1. Đã làm gì.** Sửa ba điểm CX-06 và áp D2, R9 vào bản 2 của hồ sơ thiết kế; giữ nguyên bản 1.

**2. File đã thay đổi.** Mới: `results/T-074/thiet-ke-w6-2.md`, `de-xuat-why-2.md`, `cau-hoi-minh-2.md`, `SHA256SUMS-2`. Nối: LOG này. Dòng T-074 trong `docs/STATE.md` (Edit). Bản 1 không đổi.

**3. Kiểm đã chạy.** `sha256sum -c SHA256SUMS` 5/5 OK; hash file T-069 đã đọc khớp manifest; đếm kênh/thực thể bằng python trên `#/coverage`; mọi dẫn dòng BARO đọc trực tiếp ở `259ea41`. Không chạy BARO (chưa có adapter FlashTicket).

**4. Chưa chắc / cần quyết.**
- Danh sách cột **sau** `drop_constant` và giao hai nửa phụ thuộc dữ liệu từng ca: chưa có (cần adapter W7 chạy trên 17 gói T-069, chỉ tính toán). Dự đoán có thể bác bỏ: cột `error` và `db-size` hằng ở N bị bỏ.
- G, biên K và tiêu chí khỏe vẫn CHỜ-W4. K2 chờ E6.
- Ghi nhận ngoài ba điểm được giao: CX-06 dòng 44 nêu phạm vi RQ3d (`DC-bo-quan-he` chỉ đo tác dụng bước dùng quan hệ trong **xếp hạng**; C-d1 dùng quan hệ caller–callee; C-d2 chỉ dùng thứ tự khởi phát). Bản 2 chưa sửa W6-M/§3.4 theo ý này; cần điều phối giao nếu muốn.
- Câu hỏi Minh còn mở: Q-W6-01…07 và phần số lượng Q-W6-08 (`cau-hoi-minh-2.md`).

**I15.** Tài nguyên giữ: không. Job server: không. Việc cần điều phối: trình `cau-hoi-minh-2.md`; chuyển prompt dưới cho Codex nếu muốn kiểm lại; quyết có giao sửa phạm vi RQ3d (W6-M) không.

**Bước tiếp theo chính xác.** Đọc `results/T-074/thiet-ke-w6-2.md` §5.3, §7.1, §8.4, §9.1. Chờ Minh trả lời; chờ T-072 chốt luật (G, K) và E6.

**Lệnh cuối đã chạy.** `sha256sum thiet-ke-w6-2.md de-xuat-why-2.md cau-hoi-minh-2.md > SHA256SUMS-2`.

### Prompt cho Codex — kiểm lại sửa T-074 (phiên 2)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — W6 khóa bản và thiết kế đánh giá, `tasks/T-074-w6-thiet-ke-danh-gia/`.
- Công đoạn: kiểm lại phản hồi và sửa (bản 2 theo CX-06 điểm 7, 8, 9).
- Gói/cổng: P9, P10 — chuẩn bị G6. `docs/review-prompt.md` chưa có khối cổng G6; khối dưới là khối G3.
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: `tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md`, `LOG.md` (phiên 1, phiên 2); `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8; `tasks/T-070-dieu-phoi-giai-doan-2/LOG.md` (lượt 3, lượt 6); các đầu vào ở mục "Đầu vào" của SPEC T-074. Chưa commit (không có git diff gốc).
- Phản biện và phản hồi trước: `results/T-070/codex/CX-06-tin-cuoi.md` (job Codex của điều phối, không phải lượt phản biện chính thức của T-074).
- Code và kết quả liên quan: `results/T-074/`: bản 1 (`thiet-ke-w6.md`, `de-xuat-why.md`, `cau-hoi-minh.md`, `du-toan.json`, `du_toan.py`; manifest `SHA256SUMS`) và bản 2 (`thiet-ke-w6-2.md`, `de-xuat-why-2.md`, `cau-hoi-minh-2.md`; manifest `SHA256SUMS-2`). RCAEval `D:/RCA-ext/src/RCAEval` revision `259ea41`; `src/p3/`; `results/T-069/dau-ra/` (manifest `results/T-069/SHA256SUMS`). Repo lab `407b4f5`, FlashTicket `36a3725` (chỉ đọc).
- Phạm vi ghi được Minh cho phép trong lượt này: [Minh điền: chỉ trả lời trong chat, hoặc `tasks/T-074-w6-thiet-ke-danh-gia/REVIEW.md`].

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

---

## Phiên 3 — 21–22/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm

- Mở phiên theo giao việc của điều phối T-070: sửa W6 bản 3 theo Codex CX-08 (`results/T-070/codex/CX-08-tin-cuoi.md`) điểm 1, 2, 3; chỉ trong `results/T-074/`, giữ bản 1 và 2. Phiên bị cắt một lần do hết hạn mức (chưa ghi file nào của bản 3 lúc đó); tiếp sau khi điều phối báo usage đặt lại. E4 đang chạy: không dùng máy, không truy vấn Prometheus.
- Đọc: CX-08; `results/T-072/bieu-thuc.json` (eval 10 s, cửa sổ rate 300 s, `for` 60 s); `results/T-071/khai-truoc-e2.json#/phan_loai_phut` (chỉ nhãn `khoe_x1`); `src/m1/adapter_flashticket.py:126–134` (alias), `:154` (lỗi nhiều chuỗi); `src/simplerca/adapter.py::prepare` (đòi epoch giây, nhận `aliases`).
- 10:22Z — Ghi `results/T-074/thiet-ke-w6-3.md` (dạng bổ sung bản 2: §A G = 370/120, §B giữ ca/thay lượt/giờ khỏe theo mức tải, §C BARO ánh xạ ngược, nhiều chuỗi, lưới thời gian, đính chính IQR = 0; §D WHY chịu ảnh hưởng; §E điểm CX-08 chưa giao) và `cau-hoi-minh-3.md` (Q-W6-09…11). Manifest `SHA256SUMS-3` (2 file). Kiểm `SHA256SUMS` 5/5, `SHA256SUMS-2` 3/3 OK.

### Kết thúc phiên 3 — 10:22Z

1. **Đã làm:** sửa ba điểm CX-08 được giao vào bản 3; ba câu hỏi mới cho Minh.
2. **File:** mới `results/T-074/thiet-ke-w6-3.md`, `cau-hoi-minh-3.md`, `SHA256SUMS-3`; nối LOG; dòng T-074 STATE (Edit). Bản 1, 2 không đổi.
3. **Kiểm:** hai manifest cũ khớp; dẫn dòng code đọc trực tiếp; số luật đọc từ `bieu-thuc.json`. Không chạy gì.
4. **Chưa chắc / cần quyết:** Q-W6-09 (G), Q-W6-10 (×3), Q-W6-11 (nhiều chuỗi). CX-08 điểm 4 (G-live thiếu kênh `live-ms`, **CHẶN khóa D14**), 5, 6, 7 và phạm vi RQ3d chưa được giao sửa. Thời gian xả trước khi chụp gói (b) vượt biên chưa đo.

**I15.** Tài nguyên: không. Job server: không. Cần điều phối: trình Q-W6-09…11; giao hay không CX-08 điểm 4–7.

**Bước tiếp:** đọc `results/T-074/thiet-ke-w6-3.md`; chờ Minh và điều phối.

**Lệnh cuối:** `sha256sum thiet-ke-w6-3.md cau-hoi-minh-3.md > SHA256SUMS-3`.

### Phiên 3 (tiếp) — bổ sung CX-08 điểm 4–7, 22/11/2026

- Giao việc thứ hai của điều phối T-070 (giao sót điểm 4–7). Bổ sung vào bản 3 (bản 3 chưa ai phản biện). sha256 bản 3 **trước** bổ sung: `thiet-ke-w6-3.md` `b1d69be0…adfe5`, `cau-hoi-minh-3.md` `86c05535…37ed` (đã ghi trong `SHA256SUMS-3` cũ, nay thay).
- Đọc: CX-08 điểm 4–7; `src/m1_ft/thanh_phan/h4_h5.py::kenh_moi`, `bien_doi_bundle` (hai kênh `live-down`, `live-ms`); `src/m1_ft/chay_ca.py:108–109` (đọc `--bo-sung` bắt buộc); LOG T-070 dòng 222 (D1); `results/T-069/thu/t069-chinh/tai-create-order.json` (`0bec9eca` 1.944, `785bfd0c` 1.765, `124242f0` 1.512); `results/T-071/e1/moc-db.json#/kho_ticket_type` (sức chứa 100.000).
- 10:25Z — Thêm §E (G-live hai kênh; cách che giữ gói đúng schema/mốc, `result` rỗng; bỏ quy tắc §9.4), §F (46.402 vé theo mô hình; khối = 1 lần mỗi cặp + 3 đối chứng, 3 khối, K2 3 lần; K0 dùng lại 3 đối chứng ×1; mốc K2 là dump E6 sau sửa), §G (so BARO–V082 và ô mốc chỉ mô tả; bỏ hai chu kỳ E6; câu WHY W6-A), §H (k6 `raw.json` đã có theo request), §I (RQ3d chưa giao). Mới `du-toan-3.json` + `du_toan_3.py` (`py -3 -I results/T-074/du_toan_3.py results/T-074/du-toan-3.json`). `cau-hoi-minh-3.md`: Q-W6-12 mới; Q-W6-06 việc 3 rút lại; Q-W6-08 số vé mới. `SHA256SUMS-3` ghi lại 4 file. `SHA256SUMS`, `SHA256SUMS-2` 8/8 OK.

**Báo cáo.** (1) Bổ sung bốn điểm CX-08 còn lại. (2) File: `thiet-ke-w6-3.md`, `cau-hoi-minh-3.md` (bổ sung), mới `du-toan-3.json`, `du_toan_3.py`, `SHA256SUMS-3` (ghi lại); LOG; dòng STATE. (3) Kiểm: hash bản 1, 2 khớp; JSON hợp lệ; số sinh bằng script. (4) Chưa chắc: gói bổ sung có kênh `result` rỗng có làm `chay_ca.py`/H5 lỗi không (CHƯA-KIỂM, kiểm trên dev); đơn ×3 cho ô lỗi chỉ có một mẫu (1.765); A+B vượt 46.402 theo giả định bảo thủ. Cần Minh: Q-W6-01…12. RQ3d chưa giao.

**I15.** Tài nguyên: không. Job server: không. Cần điều phối: trình `cau-hoi-minh-3.md`; giao hay không phần RQ3d; prompt Codex kiểm lại (nếu cần) — dùng prompt phiên 2 với tài liệu bản 3.

**Lệnh cuối:** `sha256sum thiet-ke-w6-3.md cau-hoi-minh-3.md du-toan-3.json du_toan_3.py > SHA256SUMS-3`.

---

## Phiên 4 — 23/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm

- Mở theo giao việc điều phối T-070 (23/11): W6 bản 4 + nháp SPEC bổ sung E6 + một danh sách quyết định. Không máy, không subagent, không commit.
- 03:50Z — Kiểm manifest: `SHA256SUMS` 5/5, `-2` 3/3, `-3` 4/4 OK.
- 03:50Z — **Tự soát bản 3 trước khi đọc CX-15/CX-15b** (điểm tự tìm):
  - N1 (CHẶN diễn giải (b)): với G1 = 370 s, sự cố ghép muộn có t̂ tới t+970 → cửa sổ N của RCA `[t̂−300, t̂)` nằm trong đoạn lỗi; D3 (T-043) đòi ghi giới hạn "N nhiễm lỗi khi báo trễ". Bản 3 chưa có cờ/bảng cho việc này.
  - N2 (KHÔNG CHẶN): §B.3 áp bộ phân loại phút T-071 (thiết kế cho lượt ≥ 30–60 phút) cho đoạn N chỉ 8 phút sau khởi động; tính hợp lệ của quy tắc biên trên đoạn ngắn chưa kiểm.
  - N3 (KHÔNG CHẶN, căn cứ yếu): bản 2 §7 vẫn dùng số công bố 0,80 của SimpleRCA trên RE2-TT làm căn cứ "baseline mạnh" trên FlashTicket; số trên dataset khác không chứng minh độ mạnh trên FlashTicket.
  - N4 (CHẶN diễn giải RQ5): §9.4 dòng "chuyển thẳng" so P7 trên ô đánh giá với P7 trên ô dev T-069 — khác ô, khác trạng thái DB, khác thời điểm; so này không phân xử "chuyển thẳng". Nên báo mức tuyệt đối trên ô mới, so dev chỉ mô tả.
- 03:53Z — Đọc CX-15 (điểm 1–6), CX-15b (bảng 11 điểm), `hop-nhat-cx13-16.md` §3, W4 (`bang-bao-dong-gia.md`, `troi-p95-e2-e4.md`), E5 (`e5-ket-qua.md`), DECISIONS R9 (dòng 753), `results/T-071/e1/moc-db.json`, `sau.jsonl`. Kiểm code: `runner4.py:258–270`, `inj3.py:135–155, 279–290`, `phan_loai_phut.py:186–189`, `adapter_flashticket.py:288–292`, `quy-tac-gom.json#/gian_doan_grafana`. Ghi `results/T-074/thiet-ke-w6-4.md` (§0 bảng hiệu lực; §1 W4/E5; §2–§12 theo CX-15/15b, N1–N4 tự soát, RQ3d; §13 WHY).
- 03:55Z — Ghi `du-toan-4.json` (tự đủ; `py -3 -I results/T-074/du_toan_4.py results/T-074/du-toan-4.json`), `e6-spec-nhap.md`, `cau-hoi-minh-4.md` (12 câu, thay danh sách cũ); `SHA256SUMS-4` (5 file). Lượt bị cắt do hạn mức sau bước này.
- 05:20Z — Tiếp từ checkpoint (tin điều phối 05:2xZ): `SHA256SUMS-4` 5/5 OK; bản 1–3 12/12 OK. Tự đọc lại: §2–§11 phủ đủ 11 điểm CX-15/15b, §12 RQ3d; `cau-hoi-minh-4.md` 12 câu, mỗi câu có đề xuất, lý do, mặt trái, phương án khác; `e6-spec-nhap.md` có phạm vi DB, giá trị đích R9, khôi phục, kiểm nhất quán, quyền máy S5, lỗi 10/50/99%, chi phí. Không thiếu phần nào → không sửa file đã băm.

### Kết thúc phiên 4 — 05:20Z

**1. Đã làm.** Tự soát bản 3 (N1–N4) trước khi đọc phản biện; W6 bản 4 (`thiet-ke-w6-4.md`, bổ sung bản 2–3, có bảng mục hiệu lực) xử lý CX-15 điểm 1–6, CX-15b N1–N5, RQ3d, N1–N4 tự soát, và đưa dữ liệu W4/E5; dự toán tự đủ `du-toan-4.json`; danh sách quyết định duy nhất `cau-hoi-minh-4.md`; nháp SPEC bổ sung E6 `e6-spec-nhap.md`.

**2. File.** Mới trong `results/T-074/`: `thiet-ke-w6-4.md`, `cau-hoi-minh-4.md`, `e6-spec-nhap.md`, `du-toan-4.json`, `du_toan_4.py`, `SHA256SUMS-4`. LOG này; dòng T-074 STATE. Bản 1–3 không đổi. Không ghi `tasks/` ngoài LOG.

**3. Kiểm.** Manifest bản 1–4 khớp (17/17). Số dự toán sinh bằng script (8 phương án; 46.402 vé; khối lớn nhất K2 25.488 vé, khớp CX-15b N4). Dẫn dòng code đọc trực tiếp: `runner4.py:258–270`, `inj3.py:135–155, 279–290`, `phan_loai_phut.py:189`, `adapter_flashticket.py:126–134, 288–292`, `quy-tac-gom.json#/gian_doan_grafana`. Không chạy phương pháp, không máy.

**4. Chưa chắc / cần quyết.**
- Task: bản 4 là thiết kế đề xuất; W7 chưa khóa. RQ5, RQ3 trên FlashTicket chưa trả lời.
- CHƯA-KIỂM: danh sách đầy đủ bản sao ngày/sức chứa (E6 bước 1); khoảng nghỉ ~84 s giữa hai lượt tải; `flush_F` ở ×3; tiêu chí T-071 nào không phụ thuộc tốc độ (cho ×3); đơn vị trace của SimpleRCA `prepare`; gói bổ sung có kênh rỗng có chạy được (D14 G-live); bộ phân loại trên đoạn N 8 phút.
- Cần Minh: 12 câu `cau-hoi-minh-4.md` (gồm duyệt nháp E6, câu 12). Câu 2 và 3 quyết có SPEC E6b (proxy/quota) hay không.

**I15.** Tài nguyên: không. Job server: không. Cần điều phối: trình `cau-hoi-minh-4.md` và `e6-spec-nhap.md` cho Minh một lần; ghi khung S5 vào `LICH-MAY.md` khi duyệt; chuyển prompt dưới cho Codex nếu cần phản biện bản 4.

**Bước tiếp.** Chờ Minh trả lời 12 câu; khi duyệt E6, chép nháp thành SPEC bổ sung, mở S5.

**Lệnh cuối.** `sha256sum -c SHA256SUMS-4` (5/5 OK).

### Prompt cho Codex — kiểm lại bản 4 và nháp E6 (phiên 4)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — W6 khóa bản và thiết kế đánh giá, `tasks/T-074-w6-thiet-ke-danh-gia/`.
- Công đoạn: kiểm lại phản hồi và sửa (bản 4 theo CX-15, CX-15b, RQ3d; nháp SPEC bổ sung E6).
- Gói/cổng: P9, P10 — chuẩn bị G6. `docs/review-prompt.md` chưa có khối cổng G6; khối dưới là khối G3.
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: `tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md`, `LOG.md` (phiên 1–4); `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8; `tasks/T-070-dieu-phoi-giai-doan-2/LOG.md`; `docs/DECISIONS.md` (R9); các đầu vào ở mục "Đầu vào" của SPEC T-074. Chưa commit.
- Phản biện và phản hồi trước: `results/T-070/codex/CX-06-tin-cuoi.md`, `CX-08-tin-cuoi.md`, `CX-15-tin-cuoi.md`, `CX-15b-tin-cuoi.md`; `results/T-070/hop-nhat-cx13-16.md` §3.
- Code và kết quả liên quan: `results/T-074/` bản 1–4 (manifest `SHA256SUMS`, `-2`, `-3`, `-4`); `du_toan_4.py` (`py -3 -I results/T-074/du_toan_4.py <file ra>`); `results/T-072/bang-bao-dong-gia.md`, `troi-p95-e2-e4.md`; `results/T-073/e5-ket-qua.md`, `khai-truoc-e5.json`; `results/T-071/e1/`; `src/p3/`, `src/simplerca/`, `src/m1/`, `src/m1_ft/`; RCAEval `259ea41`; repo lab `407b4f5`; FlashTicket `36a3725` (chỉ đọc).
- Phạm vi ghi được Minh cho phép trong lượt này: [Minh/điều phối điền: chỉ trả lời trong chat, hoặc file phản biện được phép].

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

---

## Phiên 5 — 23/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm (đáp phản biện CX-29, CX-29b)

- Mở theo giao việc điều phối T-070: đáp phản biện W6 bản 4 + nháp E6; sửa phần đúng thành bản 5. Không máy, không subagent, không commit.
- 05:51Z — Manifest: `SHA256SUMS` 5/5, `-2` 3/3, `-3` 4/4, `-4` 5/5 OK.
- 05:51Z — **Tự soát bản 4 và nháp E6, trước khi mở CX-29/CX-29b:**
  - S1 (CHẶN E6): bước 6(c) chạy một chu kỳ BINH-THUONG "bằng runner" — `runner4.py::m1_worker` xếp stage, P7, V082 và `sau_v082.py` (ghi chỉ mục G1 `t065-l11-001`) cho mọi chu kỳ; dùng runner là tạo ca RCA và ghi vùng demo, trái mục "Không thu ca RCA".
  - S2 (CHẶN E6): bước 5 "chạy 1 lượt tải ×1 ngắn" cần máy tải AWS và `tai_linux` trên exp-obs, nhưng mục quyền máy chỉ nêu máy tải cho 6(c).
  - S3 (CHẶN E6): Redis trả `NOAUTH` với lệnh đọc khóa (`results/T-071/e1/moc-db.json#/bo_sung_luot_2/redis`); MongoDB `user-db` cũng cần xác thực. Nháp E6 ghi "Redis keyspace (chỉ đọc)" và "xóa nhóm khóa giữ chỗ" như thể làm được: không làm được nếu không có quyền đọc thông tin xác thực (AGENTS §12 cấm đọc `.env`).
  - S4 (CHẶN W7, công thức sai): bản 4 §7 `giay_N_nhiem = min(t̂ − t, 300)` sai khi t̂ > t + 600 (lỗi đã gỡ): phần giao đúng là `max(0, min(t̂, t+600) − max(t̂−300, t))`. Ví dụ t̂ = t+970 → 0 s, không phải 300 s. Câu "cảnh báo muộn có N nằm trọn trong đoạn lỗi" sai với t̂ > t+600.
  - S5 (CHẶN W7, D13): bản 4 §6 nói D13 khả thi với g ≤ 300 s. D13 (T-043) neo nền lùi tại `t_p` (lúc rời Normal), `N′ = [t_p − g − 300, t_p − g)`; gói (b) bắt đầu ở t̂ − 600. Điều kiện đúng: `t̂ − t_p + g ≤ 300`; với `for` = 60 s thì t̂ − t_p ≥ 60 → g ≤ 240 s (chưa tính độ trễ đánh giá).
  - S6 (CHẶN mốc W7): bước 4 dump "từng DB" khi service đang chạy (worker hết hạn đơn, consumer) — không tĩnh như E1 (E1 dump lúc không tải, không job); các dump không đồng thời có thể lệch nhau giữa DB.
- 05:52Z — Đọc CX-29 (điểm 1–7, mục E5, đối chiếu), CX-29b (bảng + 3 điểm mới), DECISIONS Q1–Q11 (23/11, dòng 770–790). Kiểm code: `inj3.py:115–117` (kiểu `cpu` đốt cố định trong `BOOK`), `src/p3/adapters/simplerca.py:14–22` và cuối hàm (gọi `thuc_the_metric` lại trên tên thực thể), `src/simplerca/adapter.py:61–65` (`startTime` µs, chia 1e6), `runner4.py:272–278` (nhánh `m1-skipped` khi `fault_ok = False`).
- **Đáp từng điểm** (người làm; Minh quyết sửa):

| Điểm | Kết luận | Bằng chứng riêng / ghi chú | Trùng tự soát |
|---|---|---|---|
| CX-29 #1 quyền E6, 6(c) | **Đúng** | `runner4.py:276` đưa mọi chu kỳ không lỗi khởi động vào hàng M1; bước 5 cần máy tải; bước 7 đọc ba máy | S1, S2 |
| CX-29 #2 mốc, hoàn tác, Redis | **Đúng** | `moc-db.json#/bo_sung_luot_2/redis` NOAUTH; 99% "về mốc W7 đã kiểm" không phải đường phục hồi; 50% restore dump trước sửa làm mất sửa ngày/sức chứa | S3, S6 |
| CX-29 #3 N nhiễm lỗi | **Đúng** | t̂ = t+900 → giao 0 s, bản 4 cho 300 s; nhóm 60/180 trùng biên | S4 |
| CX-29 #4 D13 | **Đúng** | điều kiện `g + (t̂ − t_p) ≤ 300`; thêm (mới với tôi): gói bổ sung chỉ ±300 quanh t̂ (`xuat_bo_sung.py:103`) → bản có H5 không dựng được N′ | S5 (một phần) |
| CX-29 #5 niêm đầu vào | **Đúng một phần** (như CX-29b) | bản 2 §8.2 đã yêu cầu niêm độc lập; chỗ hở thật: tuyến E5 xuất bổ sung sau P7, `chay_d2` không truyền `mult` | không |
| CX-29 #6 baseline | **Đúng** | wrapper P3 gọi `thuc_the_metric` trên tên thực thể sau `diagnose` → `booking_db` thành `booking`; tiêu chí "hạng ≠ thứ tự cột" bác cả kết quả đúng; đơn vị `startTime` đã xác định (µs) | không |
| CX-29 #7 bù ca | **Đúng** | probe sạch sau hạn tự gỡ tương thích cả "chưa tiêm" và "đã tiêm rồi gỡ" | không |
| E5 N4 tập ứng viên | **Đúng** | bản 4 không khẳng định ngược; ghi rõ bản phương pháp khi diễn giải | — |
| E5 N5 H5 | **Đúng** | báo điều kiện nền H5 khi so (a)/(b) và bản che | — |
| E5 N6 hash | **Đúng**, không chặn | W7 dẫn hash từ hiện vật W7 | — |
| E5 N7 mốc giờ, phủ | **Đúng** | bản 4 §1 sai: "t̂ = mốc + 60 s" (đúng: 55,767 s từ `fault-start`), "14,8 phút" (mốc Q2 nhận: cận trên 898,8 s), "lỗ 365 s cho 6 metric" (đúng: CPU/mem 364,999 s, HTTP 315 s) | không |
| Mới: gói ca chưa xác nhận (`m1-skipped`) | **Đúng** | T1(a) phải chụp mọi chu kỳ đã phát tải, ghi trạng thái tiêm riêng | không |
| Mới: đích CPU-EVENT | **Đúng** | `inj3.py:117` `docker exec -d BOOK …`; probe/dừng cũng theo BOOK | không |
| Mới: +90 s đổi nhu cầu vé | **Đúng** | `du_toan_4.py` giữ số đơn khi cộng 90 s | không |

- Bất đồng còn lại: không có. Sửa vào bản 5; phần E6 tách sang `e6-spec-nhap-2.md`.
- 05:55Z — Ghi bản 5: `e6-spec-nhap-2.md` (phần E6: nhánh K0; quyền từng máy; phạm vi DB và giới hạn Redis/MongoDB; trạng thái yên kiểm trước và sau dump; bỏ bước 5–6(c); khóa bản sau thay đổi cuối; lỗi 10/50/99% với UPDATE ngược theo `truoc.jsonl`; nhánh K2 tách §9), `thiet-ke-w6-5.md` (phần khóa W7: N nhiễm lỗi hai công thức giao, D13 theo `t_p` và hai gói, T1(a) chụp mọi chu kỳ đã phát tải, T1b niêm hai gói trước P7, pilot ×3, wrapper SimpleRCA mới, nghiệm thu BARO, bù ca theo bằng chứng phía đích, CPU-EVENT ứng viên, nhu cầu vé khi +90 s, đính chính E5), `cau-hoi-minh-5.md` (phần A 4 câu cho E6, phần B 7 câu khóa W7). `SHA256SUMS-5` (3 file). Bản 1–4: 17/17 OK.
- Đổi đề xuất so bản 4: phạm vi ô đề xuất từ A + CPU-EVENT xuống **A** (CPU-EVENT thành ứng viên vì `inj3.py:117` đốt cố định trong Booking); E6 chỉ nhánh K0.

### Kết thúc phiên 5 — 05:55Z

**1. Đã làm.** Tự soát bản 4 + nháp E6 (S1–S6) trước khi đọc phản biện; đáp từng điểm CX-29/CX-29b (14 điểm: 12 đúng, 1 đúng một phần, 1 đúng không chặn; không có điểm sai); sửa thành bản 5, tách phần E6 với phần khóa W7.

**2. File.** Mới trong `results/T-074/`: `thiet-ke-w6-5.md`, `e6-spec-nhap-2.md`, `cau-hoi-minh-5.md`, `SHA256SUMS-5`. LOG này; dòng T-074 STATE. Bản 1–4 không đổi.

**3. Kiểm.** Manifest bản 1–4 17/17. Đọc code xác nhận các điểm mới (`inj3.py:115–117`, `src/p3/adapters/simplerca.py`, `src/simplerca/adapter.py:61–65`, `runner4.py:272–278`). Nhu cầu vé +90 s tính bằng python (lệnh ở dòng trên của LOG); khớp CX-29b (47.693). Không máy.

**4. Chưa chắc / cần quyết.**
- Phần A (chặn E6): A1 K0/K2, A2 quyền máy, A3 giá trị đích, A4 giới hạn Redis/MongoDB.
- Phần B (khóa W7, không chặn E6): B1–B7.
- CHƯA-KIỂM: danh sách đủ bản sao ngày/sức chứa; service có giữ cấu hình trong bộ nhớ; phản hồi GET có trường ngày bán; độ trễ hàng chờ bộ chụp và `flush_F` ở ×3; gói bổ sung rỗng kênh với H5.
- Không còn bất đồng có bằng chứng với CX-29/29b.

**I15.** Tài nguyên: không. Job server: không. Cần điều phối: trình `cau-hoi-minh-5.md` phần A (để phát E6) và phần B; nếu phát E6, ghi S5 theo bảng quyền `e6-spec-nhap-2.md` §2; chuyển prompt dưới cho Codex nếu cần kiểm lại.

**Bước tiếp.** Chờ Minh trả lời phần A; khi duyệt, chép `e6-spec-nhap-2.md` thành SPEC bổ sung và mở S5.

**Lệnh cuối.** `sha256sum thiet-ke-w6-5.md e6-spec-nhap-2.md cau-hoi-minh-5.md > SHA256SUMS-5`.

### Prompt cho Codex — kiểm lại bản 5 (phiên 5)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — W6 khóa bản và thiết kế đánh giá, `tasks/T-074-w6-thiet-ke-danh-gia/`.
- Công đoạn: kiểm lại phản hồi và sửa (bản 5: thiết kế phần khóa W7, nháp SPEC E6 bản 2, danh sách quyết định bản 5).
- Gói/cổng: P9, P10 — chuẩn bị G6. `docs/review-prompt.md` chưa có khối cổng G6; khối dưới là khối G3.
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: `tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md`, `LOG.md` (phiên 1–5; bảng đáp từng điểm ở phiên 5); `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8; `docs/DECISIONS.md` (R9; Q1–Q11 ngày 23/11); các đầu vào ở mục "Đầu vào" của SPEC T-074. Chưa commit.
- Phản biện và phản hồi trước: `results/T-070/codex/CX-06-tin-cuoi.md`, `CX-08-tin-cuoi.md`, `CX-15-tin-cuoi.md`, `CX-15b-tin-cuoi.md`, `CX-29-tin-cuoi.md`, `CX-29b-tin-cuoi.md`; `results/T-070/hop-nhat-cx13-16.md` §3.
- Code và kết quả liên quan: `results/T-074/` bản 1–5 (manifest `SHA256SUMS`, `-2` … `-5`); `results/T-071/e1/`, `results/T-072/`, `results/T-073/e5/`, `dap-cx21/`; `src/p3/`, `src/simplerca/`, `src/m1/`, `src/m1_ft/`; RCAEval `259ea41`; repo lab `407b4f5` và `81a9273`; FlashTicket `36a3725` (chỉ đọc).
- Phạm vi ghi được Minh cho phép trong lượt này: [Minh/điều phối điền: chỉ trả lời trong chat, hoặc file phản biện được phép].

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

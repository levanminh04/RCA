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

---

## Phiên 6 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm (đáp CX-32/32b, nháp E6 bản 3)

- 17:42Z — Mở theo giao việc điều phối T-070 (24/11; Minh duyệt phương án C: E6 là khung máy đầu tiên). Lượt 12:1xZ ngày 23/11 dừng trước khi ghi file; làm lại. Quyết định đã có (Minh, `results/T-070/cho-duyet-2026-11-23-chieu.md` mục 13–24): A1 K0, A2, A3, A4, B1 phương án A, B2 G = 370 s không kéo dài tải, B3–B7. Không máy, không subagent, không commit.
- 17:43Z — Đọc CX-32 (§1 điểm 1–4, §2 bảng), CX-32b (bảng + M1, M2), `results/T-073/dap-cx21/dinh-chinh-e5-3.md` §2; kiểm `inj3.py:21` (nạp module tạo `/home/ubuntu/t063/inj`), `:120, 188, 311` (deadline pause, `verify` gỡ pause quá hạn).
- **Đáp CX-32/CX-32b** (người làm; phần E6 sửa ở `e6-spec-nhap-3.md`, phần W7 ghi vào `con-mo-w6.md`, chưa sửa thiết kế):

| Điểm | Kết luận | Xử lý |
|---|---|---|
| CX-32 #1 quyền bước 0; `verify` có ghi; bộ điều phối W5 có thể tạo ca | **Đúng** (`inj3.py:21` mkdir khi nạp; `:311` gỡ pause quá hạn, xóa deadline) | E6 bản 3 §2, §5 bước 0: bảng đọc đủ từng máy; exp-app dùng lệnh đọc thuần, không gọi `inj3.py`; bộ điều phối W5 còn chạy → dừng ở bước 0 |
| CX-32 #2 A3 phụ thuộc B1/B2 | **Đúng**; nay Minh đã chốt B1 = A, B2 không kéo dài tải → ngân sách 35.640 | §4: đích = max(sức chứa hiện tại, `purchased` + 1,5 × 35.640) làm tròn lên nghìn |
| CX-32 #3 GET xác nhận | **Đúng** (Event công khai không trả `saleEndsAt`; Booking qua cache) | §5 bước 3: đạt/trượt chỉ bằng SQL đọc lại đúng cột, đúng kiểu; GET Event chỉ đối chiếu trường nó trả; bỏ GET Booking; sửa Event bằng SQL (đường API đòi `DRAFT`) |
| CX-32 #4 hoàn tác 50/99% | **Đúng** (worker Payment chạy định kỳ khi không tải) | §7: bỏ `pg_restore` khỏi K0; đảo theo khóa chỉ cột còn mang giá trị E6; gặp giá trị thứ ba → giữ máy ở điều phối; lỗi muộn ở bước 7 chỉ làm lại hiện vật |
| CX-32 D13 miền hỗ trợ | **Đúng**, không chặn E6 | `con-mo-w6.md` W-1 |
| CX-32 BARO tiêu chí điểm | **Đúng**, không chặn E6 | `con-mo-w6.md` W-2 |
| CX-32 K0 và độ trôi | **Đúng**, không chặn K0 | `con-mo-w6.md` W-3 |
| CX-32b M1 khóa nhầm ID container | **Đúng** | §5 bước 7: `.Image` → `docker image inspect` |
| CX-32b M2 SimpleRCA D13 dùng một `boundary` | **Đúng**, không chặn E6 | `con-mo-w6.md` W-4 |
| CX-32b dự toán `#/viec_them/E6` cũ | **Đúng** | E6 bản 3 §8 thay mục đó |

- Không bất đồng.
- 17:44Z — Ghi `results/T-074/e6-spec-nhap-3.md` (quyền đọc đủ ba máy, bước 0 đọc thuần không gọi `inj3.py`, dừng nếu W5 còn chạy; ngân sách 35.640, giữ sức chứa nếu cao hơn; đạt/trượt bằng SQL đọc lại, bỏ GET Booking; hoàn tác theo dòng, bỏ `pg_restore`; khóa bản qua `.Image`) và `con-mo-w6.md` (W-1…W-6, gồm hai giới hạn H5 của T-073). `SHA256SUMS-6` (2 file); bản 1–5 20/20 OK.

### Kết thúc phiên 6 — 17:44Z

**1. Đã làm.** Đáp CX-32/CX-32b (10 điểm, đều đúng; không bất đồng); viết nháp E6 bản 3 (chỉ phần E6, nhánh K0); ghi câu hỏi mở W6 (W-1…W-6, gồm hai giới hạn H5 của T-073) dạng đề xuất.
**2. File.** Mới: `results/T-074/e6-spec-nhap-3.md`, `con-mo-w6.md`, `SHA256SUMS-6`. LOG; dòng STATE. Bản 1–5 không đổi.
**3. Kiểm.** Manifest bản 1–5 20/20 OK. Đọc code `inj3.py:21, 120, 188, 311`. Không máy.
**4. Chưa chắc / cần quyết.** Minh duyệt nháp E6 bản 3 (quyền ba máy §2; dừng ở bước 1 để duyệt danh sách dòng và SQL). CHƯA-KIỂM: danh sách đủ bản sao ngày/sức chứa; cache Booking sau SQL. W-1…W-6 chờ khi khóa W7.
**I15.** Tài nguyên: không. Job server: không. Cần điều phối: trình `e6-spec-nhap-3.md`; ghi S5 theo §2; chuyển prompt dưới cho Codex nếu cần.
**Bước tiếp.** Khi Minh duyệt: chép nháp thành SPEC bổ sung, mở S5, làm bước 0.
**Lệnh cuối.** `sha256sum e6-spec-nhap-3.md con-mo-w6.md > SHA256SUMS-6`.

### Prompt cho Codex — kiểm lại nháp E6 bản 3 (phiên 6)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — W6, nháp SPEC bổ sung E6 bản 3 (`results/T-074/e6-spec-nhap-3.md`) và `con-mo-w6.md`.
- Công đoạn: kiểm lại phản hồi và sửa (theo CX-32, CX-32b).
- Gói/cổng: P9, P10 — chuẩn bị G6. `docs/review-prompt.md` chưa có khối cổng G6; khối dưới là khối G3.
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: `tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md`, `LOG.md` (phiên 5–6; bảng đáp ở phiên 6); `results/T-070/cho-duyet-2026-11-23-chieu.md` mục 13–24; `docs/DECISIONS.md` (R9, Q8–Q9); `tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md`. Chưa commit.
- Phản biện và phản hồi trước: `results/T-070/codex/CX-29-tin-cuoi.md`, `CX-29b-tin-cuoi.md`, `CX-32-tin-cuoi.md`, `CX-32b-tin-cuoi.md`.
- Code và kết quả liên quan: `results/T-074/` (manifest `SHA256SUMS` … `-6`); `results/T-071/e0-trang-thai.md`, `e1/`; `results/T-073/dap-cx21/dinh-chinh-e5-3.md`; repo lab `1bb40ca` (`faults/injectors/docker/inj3.py`, `campaigns/online/`); FlashTicket `36a3725` (chỉ đọc).
- Phạm vi ghi được Minh cho phép trong lượt này: [Minh/điều phối điền].

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

## Phiên 7 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm, chủ khung S5 (pha chỉ đọc)

- 18:02Z — Mở theo giao việc điều phối T-070 (24/11 ~01:0x): đáp CX-37/37b, nháp E6 bản 4 tách pha đọc/ghi, chạy **pha đọc** (bước 0–1), lập giá trị đích và SQL thuận/nghịch, **dừng trước mọi lệnh ghi**. Không subagent, không commit.
- Ghi nhận quy trình (CX-37 "Quy trình", đúng): phiên 6 không ghi tự soát trước khi đọc phản biện. Lượt này cũng đã mở CX-37 trước khi tự soát; không có danh sách tự soát độc lập cho nháp 3 — ghi đúng như vậy.
- 18:02Z — **Đáp CX-37/CX-37b:**

| Điểm | Kết luận | Xử lý ở nháp 4 |
|---|---|---|
| CHẶN 1 GET Event qua gateway (route `/api/v1/events/**` qua `RequestRateLimiter` dùng Redis) | **Đúng** (không tự kiểm lại code gateway; dựa CX-37b dẫn `application.yaml:94` và trace T-067) | bỏ mọi GET qua gateway; xác nhận chỉ bằng SQL đọc lại |
| CHẶN 2 sức chứa: A3 là `purchased + 53.460` làm tròn lên nghìn, không `max` | **Đúng** (nháp 3 thêm `max` theo lời giao điều phối, khác văn bản A3 Minh duyệt) | áp đúng A3; nếu đích < sức chứa hiện tại thì ghi rõ là **giảm** sức chứa và trình Minh ở điểm dừng bước 1 |
| CHẶN 3 cặp SQL thuận/nghịch theo khóa/cột/đường dẫn JSON/kiểu | **Đúng** | pha đọc lập `results/T-074/e6/sql-thuan.sql`, `sql-nghich.sql`, `kiem-sau-ghi.sql`; so giá trị đã khóa với giá trị bước 1; đảo JSON từng trường |
| 10/50/99% | **Đúng** | §7 nháp 4 |
| Bước 0: HEAD cả hai máy; t072-bo-nhan được phép, t073-webhook thì không; `docker ps -a`; dịch vụ kỳ vọng E0; lỗi đọc → "chưa kiểm được" | **Đúng** | §5 bước 0 |
| Payout `tbl_event_payouts.event_ends_at` | **Đúng** | bước 1 đếm; có dòng → trình lại phạm vi |
| Dump: ghi đích danh tập DB (E1 có cả `keycloak_db`) | **Đúng** | bước 4 dump 4 DB nghiệp vụ, ghi rõ không dump `keycloak_db` (không ghi gì vào đó) |
| Chi phí 75–155 phút | **Đúng** | §8 sửa |
| Pilot W7 không phân biệt hai hạn bán | **Đúng** | kết luận E6 dừng ở mức đọc lại PostgreSQL |
| CX-37b: `docker ps` bỏ sót dịch vụ đã dừng | **Đúng** | bước 0 đối chiếu danh sách container kỳ vọng E0 bằng `docker ps -a` + `inspect` |
- 18:03Z — Nháp 4 ghi (`results/T-074/e6-spec-nhap-4.md`). Chạy **bước 0 (chỉ đọc)**: script `b0-app.sh`, `b0-obs.sh` (nội dung chép vào `results/T-074/e6/` cùng đầu ra); exp-app qua khóa `D:/RCA-ext/keys/exp-app`, exp-obs qua `D:/RCA-ext/keys/exp-obs`, máy tải qua khóa bộ điều khiển trên exp-obs (`sudo ssh`, không đọc nội dung khóa). Không ghi file nào trên máy.
- 18:03–18:04Z (giờ máy) — **Bước 0 đạt** (`results/T-074/e6/b0-app.out`, `b0-obs.out`): exp-app HEAD `407b4f5` sạch; 14 container kỳ vọng (theo E0 T-071) đều chạy, không Paused; không tiến trình job; `/home/ubuntu/t063/inj` có, không deadline/pid; 4 proxy không toxic; lease Booking/Event `off`, đã hết hạn; không cron/timer; 30 hàng đợi đều 0/0; chrony đồng bộ. exp-obs HEAD `1bb40ca` sạch; không STOP; không tiến trình job; container chạy: obs ×5 + `flash-ticket-t072-bo-nhan` (thuộc project Compose `t073-webhook`, được phép); không có container `flash-ticket-t073-webhook`, không `orchestrator.py`. Máy tải: không `rca-tai-*` đang chạy (106 đã Exited, giữ), dòng khớp "k6" duy nhất là chính lệnh dò; k6 image `grafana/k6:1.4.2`.
- 18:04Z — **Bước 1** (`b1-app.out`, `b1b-app.out`, chỉ SELECT): bản sao ngày/sức chứa = `event_schema.tbl_events` (5 cột ngày), `event_schema.tbl_ticket_types.configured_quantity`, `booking_schema.tbl_event_sales_snapshots` (`sale_ends_at` + JSON `saleEndsAt`, `eventStartsAt`, `eventEndsAt` kiểu number; `ticketTypes[ticketTypeId=ffb36fc7…].configuredQuantity` kiểu string), `booking_schema.tbl_ticket_type_inventory.configured_capacity`, `ticket_schema.tbl_event_access_snapshots` (2 cột), `payment_schema.tbl_event_finance_snapshots.event_ends_at`. Payout 0; sector/promotion 0. Ràng buộc: `checkin_* = starts/ends`, `sale_ends_at <= ends_at`, `purchased <= configured_capacity`. Không trigger cập nhật. Tồn kho: `configured_capacity` 100.000, `held` 0, `purchased` **41.705** → A3: 41.705 + 53.460 = 95.165 → **96.000 (giảm 4.000)**. Cột trạng thái đơn là `lifecycle_state` (dùng ở bước 2 pha ghi). JSON lịch sử theo đơn (`frozen_purchase_snapshot`, `selection_snapshot`, `purchase_snapshot`, `display_snapshot`) ngoài phạm vi.
- 18:06Z — Soạn `results/T-074/e6/sql-thuan.sh` (mỗi DB một giao dịch; khóa dòng; so mọi giá trị với bước 1 kể cả kiểu JSON và `purchased`/`held`; in TRUOC/SAU; UPDATE có điều kiện giá trị cũ; ROW_COUNT = 1; 5 cột ngày Event cùng một UPDATE; JSON sửa theo đường dẫn, `configuredQuantity` chọn theo `ticketTypeId`, giữ kiểu chuỗi; payout phải 0), `sql-nghich.sh` (đảo từng trường còn mang giá trị đích; giá trị thứ ba → RAISE), `kiem-sau-ghi.sh` (chỉ SELECT; trạng thái CU/DICH/KHAC từng trường + kiểu + `pg_stat_activity`). **Chạy thử `kiem-sau-ghi.sh` (chỉ SELECT) lúc 18:06:53Z: 17/17 trường = CU, kiểu JSON đúng** (`kiem-truoc-ghi.out`) — xác nhận cú pháp và phép so của bộ kiểm; `sql-thuan.sh`/`sql-nghich.sh` **chưa chạy** (có ghi). Thấy phiên `booking_db` active (truy vấn đơn của worker) khi không tải — khớp CX-32 #4.
- `gia-tri-dich.json`, `danh-sach-dong.json`; `results/T-074/e6/SHA256SUMS` (14 file); `SHA256SUMS-7` (nháp 4).
- **Không có thay đổi trạng thái máy nào**: không tạo thư mục, không ghi file trên ba máy (mọi lệnh qua stdin, đầu ra về laptop). **DỪNG trước pha ghi.**

### Kết thúc phiên 7 — 18:08Z (giờ máy)

**1. Đã làm.** Đáp CX-37/37b (10 điểm, đều đúng); nháp E6 bản 4 tách pha đọc/ghi; chạy pha đọc (bước 0 đạt ba máy; bước 1 đọc đủ bản sao); lập giá trị đích, danh sách dòng, SQL thuận/nghịch, bộ kiểm sau ghi.
**2. File.** Repo: `results/T-074/e6-spec-nhap-4.md`, `SHA256SUMS-7`; `results/T-074/e6/` (script, đầu ra đọc, JSON, SQL, `SHA256SUMS`); LOG; dòng STATE. Máy: không đổi gì.
**3. Kiểm.** Bước 0 theo tiêu chí nháp 4; bước 1 SELECT; `kiem-sau-ghi.sh` 17/17 CU.
**4. Cần quyết.** (a) **Sức chứa theo A3 = 96.000 < 100.000 hiện tại (giảm 4.000)** — Minh xác nhận giảm hay giữ 100.000. (b) Không đổi `row_version`/`updated_at` khi sửa (tối thiểu) — người phản biện xét rủi ro ghi đè từ thực thể cũ trong bộ nhớ service (CHƯA-KIỂM). (c) Hai phiên Codex kiểm bộ SQL trước khi giao pha ghi. Thời gian pha ghi chưa đo (40–105 phút ước).
**I15.** Tài nguyên: khung S5 pha đọc — đã xong, **trả lại điều phối**; không job nào đang chạy. Cần điều phối: trình (a); chuyển bộ SQL cho Codex; giao pha ghi khi không còn CHẶN.
**Bước tiếp.** Khi giao pha ghi: bước 2 (yên + dump) → `sql-thuan.sh` → `kiem-sau-ghi.sh` → bước 4 → bước 7.
**Lệnh cuối.** `sha256sum e6-spec-nhap-4.md > SHA256SUMS-7`.

---

## Phiên 8 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm (bộ SQL E6 v2, không máy)

- 23:07Z — Mở theo giao việc điều phối T-070 (24/11 06:0x giờ máy): đáp CX-39/39b; bộ SQL/kiểm mới ở `results/T-074/e6/v2/` (giữ bản cũ nguyên hash), hai biến thể sức chứa A (96.000) và B (giữ 100.000, không ghi sức chứa); phép thử giả lập trên laptop; dừng trước mọi lệnh ghi. Không máy, không subagent, không commit.
- Laptop không có PostgreSQL (`which psql postgres pg_ctl` không thấy): phép thử giả lập chỉ kiểm **luồng shell** (mã thoát, dừng ở lỗi đầu, log riêng từng lượt, nhánh mất kết nối, đếm trường). Logic SQL (NULL, kiểu JSONB) chỉ kiểm được trên PostgreSQL — đề xuất phép thử SQL chỉ đọc bằng hằng JSONB, chạy khi có quyền đọc exp-app.
- **Đáp CX-39/CX-39b:** #1 SQL thuận chấp nhận khóa JSON mất — **đúng**; #2 nghịch chạy tiếp, `tee` ghi đè — **đúng**; #3 nghịch nhận nhầm dòng/kiểu — **đúng**; #4 mất kết nối lúc COMMIT, `SAU` in trước COMMIT, đọc không khóa — **đúng**; #5 bộ kiểm trả 0 khi `psql` lỗi, 15 chứ không 17 trường, so văn bản — **đúng** (LOG phiên 7 ghi "17/17" là sai: 15 trường + 2 dòng phụ); #6 bước 1 chưa chứng minh DB yên (đếm đơn lỗi, thiếu outbox) — **đúng**; mới: bước 0 trên exp-obs/máy tải lọc thiếu tiến trình — **đúng** (kết quả bước 0 cũ không dùng để phát ghi; làm lại khi nhận S5); 106 container máy tải chưa chứng minh đều Exited — **đúng**; LOG phiên 7 thiếu prompt — **đúng**. Không bất đồng.
- 23:14Z — Ghi `results/T-074/e6/v2/`: `tao_sql.py` → `sql/A`, `sql/B` (thuận, nghịch, kiểm, kiểm-khóa cho 4 DB; `truong.txt` 15 trường, `phu.txt`); `chay.sh` (dừng ở lỗi đầu, lượt riêng, mã thoát 0/2/3/4/5/6/7/8); `b0-v2.sh` (lọc tiến trình đầy đủ ba máy, trạng thái container máy tải); `b1c-yen.sh` (đơn theo `lifecycle_state`, outbox, hàng đợi; chỉ SELECT); `thu/fake_psql.sh`, `thu/chay_thu.sh` — **26/26 phép thử giả lập đạt** (`thu/chay_thu.out`); phép đột biến (không dừng sau lỗi SQL) → 2 phép trượt, bộ thử phát hiện được; `thu/thu-sql-chi-doc.sql` (11 phép logic SQL chỉ đọc, chưa chạy: laptop không có PostgreSQL). Nháp `e6-spec-nhap-5.md`. Manifest `e6/v2/SHA256SUMS` (44 file), `SHA256SUMS-8`; bản cũ `e6/SHA256SUMS` 14/14 OK.

### Kết thúc phiên 8 — 23:14Z

**1. Đã làm.** Đáp CX-39/39b (đều đúng); bộ thực thi E6 v2 hai biến thể A/B; phép thử giả lập luồng shell; nháp E6 bản 5. Không máy.
**2. File.** Mới: `results/T-074/e6/v2/` (44 file), `e6-spec-nhap-5.md`, `SHA256SUMS-8`; LOG; dòng STATE. Bản cũ giữ nguyên.
**3. Kiểm.** `bash results/T-074/e6/v2/thu/chay_thu.sh` 26/26; đột biến bắt được; manifest cũ khớp.
**4. Chưa chắc / cần quyết.** Minh chọn biến thể A (96.000) hay B (giữ 100.000, ngoại lệ A3; CX-39b đề nghị B). Logic SQL chưa chạy trên PostgreSQL: đề xuất chạy `thu-sql-chi-doc.sql` (chỉ đọc) đầu pha ghi; nếu một phép J01–J11 khác mong đợi thì dừng, sửa SQL. Bước 0 và `b1c-yen.sh` phải chạy lại khi nhận S5.
**I15.** Tài nguyên: không. Job server: không. Cần điều phối: Minh chọn A/B; Codex kiểm v2; giao pha ghi.
**Bước tiếp.** Khi giao pha ghi: `b0-v2.sh` (ba máy) → `thu-sql-chi-doc.sql` → `chay.sh kiem <bt> CU` → `b1c-yen.sh` + dump → `chay.sh thuan <bt>` → `chay.sh kiem <bt> DICH` → mốc, khóa bản.
**Lệnh cuối.** `sha256sum e6-spec-nhap-5.md e6/v2/SHA256SUMS > SHA256SUMS-8`.

### Prompt cho Codex — kiểm lại bộ thực thi E6 v2 (phiên 8)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — E6 bộ thực thi v2 (`results/T-074/e6/v2/`) và nháp SPEC bổ sung E6 bản 5 (`results/T-074/e6-spec-nhap-5.md`).
- Công đoạn: kiểm lại phản hồi và sửa (theo CX-39, CX-39b).
- Gói/cổng: P9, P10 — chuẩn bị G6. `docs/review-prompt.md` chưa có khối cổng G6; khối dưới là khối G3.
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: `tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md`, `LOG.md` (phiên 7–8); `results/T-074/e6-spec-nhap-4.md`; `results/T-070/cho-duyet-2026-11-23-chieu.md` mục 13–24; `tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md`. Chưa commit.
- Phản biện và phản hồi trước: `results/T-070/codex/CX-37-tin-cuoi.md`, `CX-37b-tin-cuoi.md`, `CX-39-tin-cuoi.md`, `CX-39b-tin-cuoi.md`.
- Code và kết quả liên quan: `results/T-074/e6/` (pha đọc, manifest `SHA256SUMS`) và `e6/v2/` (manifest `e6/v2/SHA256SUMS`; sinh SQL: `py -3 -I tao_sql.py`; phép thử giả lập: `bash thu/chay_thu.sh`); `results/T-074/SHA256SUMS-8`; FlashTicket `36a3725` (chỉ đọc). Không dùng máy.
- Phạm vi ghi được Minh cho phép trong lượt này: [Minh/điều phối điền].

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

- 01:29Z — Điều phối báo (24/11 sáng): Minh duyệt **biến thể B** (giữ sức chứa 100.000; E6 chỉ sửa ngày bán/diễn/check-in; DECISIONS khối 24/11). Hai giới hạn H5 của T-073 (`con-mo-w6.md` W-5, W-6) nay là câu hỏi mở chính thức của W6. Pha ghi chưa giao, chờ CX-41/41b. Không tạo nháp mới lúc này để không đổi đích phản biện CX-41; đường chạy B đã có sẵn: `chay.sh <che_do> B …` với `v2/sql/B/`. Không máy, không sửa file khác.

## Phiên 9 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm (nháp SPEC W7, không máy)

- Yêu cầu điều phối (24/11 sáng): trong lúc chờ Codex kiểm E6 v2 (CX-41/41b), soạn nháp SPEC W7 ở `results/T-074/w7-spec-nhap.md` theo `tasks/_MAU/SPEC.md`; chỉ nháp, tạo task cần Minh duyệt. Không máy, không subagent, không commit.
- Căn cứ đã đọc: W6 bản 5 (+ §0 bản 4), `con-mo-w6.md` (W-5, W-6 là câu hỏi mở chính thức), `du-toan-4.json#/phuong_an/0` (27 chu kỳ, 14,1 giờ, 9 chu kỳ/khối, 3 khối, 35.640 đơn bảo thủ), `#/phut_moi_chu_ky/gia_tri` 31,4; DECISIONS khối 23–24/11 (phương án C; sức chứa 100.000; bộ chấm W4 v2d); kế hoạch giai đoạn 2 §8.3–8.4; LESSONS; HEAD lab trên máy từ `e6/b0-app.out` (`407b4f5`), `e6/b0-obs.out` (`1bb40ca`).
- Ngữ cảnh phiên bị nén một lần giữa chừng; sau nén đọc lại AGENTS, STATE, LESSONS, kế hoạch §8, DECISIONS 23–24/11 và soát lại nháp. Sửa trong nháp (chưa bàn giao nên sửa tại chỗ): thêm phụ thuộc thật giữa pha (SL32: 0a → pha 2, 0b → pha 1, pha 1 ∥ pha 2, pha 2 sau E6 pha ghi); quét suy biến phía đầu vào trên gói pilot (luật 21c; không chạy phương pháp); kiểm đóng gói thử sau đêm 1 (đề xuất luật 12); bảng lỗi 10/50/99% theo chu kỳ trong đêm + mốc sau đêm 1 + pha 5–7; Hit@k và mẫu số (b) theo §8.3; ghi thời gian batch RCA **chưa đo**; thứ tự cắt khi trễ §8.4.
- Đầu ra: `results/T-074/w7-spec-nhap.md`; manifest `results/T-074/SHA256SUMS-9`. Không đổi file cũ, không chạm máy.
- Nội dung chính: 8 pha có cổng (0 code; 1 dev + quét suy biến trên 17 gói T-069; 2 pilot xác nhận can thiệp; 3 khóa; 4 thu 3 khối × 9 chu kỳ, 1 khối/đêm ≈ 4,7 giờ, diễn tập W9a ban ngày; 5 đóng đợt băm trước RCA; 6 RCA batch; 7 chấm sau băm). 7 mục cần Minh quyết (tách W7a/W7b; 1 khối/đêm; (b) "chỉ chụp"; điều kiện bàn giao exp-app; seed; WHY W6 trước thu; ô không xác nhận → loại), mỗi mục có đề xuất, lý do, mặt trái.
- Chưa kiểm: thời gian batch RCA mỗi ca; logic adapter/che/bộ chụp "chỉ chụp" (chưa có code); cường độ 3 ô mới trên bản ghim (pilot).

### Kết thúc phiên 9 — 01:38Z

1. Đã làm: soạn và soát nháp SPEC W7.
2. File: `results/T-074/w7-spec-nhap.md`, `results/T-074/SHA256SUMS-9`, LOG này, dòng T-074 trong STATE.
3. Kiểm: đối chiếu số với `du-toan-4.json`, HEAD với `e6/b0-*.out`, mục với mẫu SPEC; không chạy phép thử (nháp văn bản).
4. Chưa chắc/cần quyết: 7 mục trong nháp; E6 vẫn chờ CX-41/41b và giao pha ghi.
- Bước tiếp: điều phối cho Codex soát nháp (prompt dưới), trình Minh; khi Minh duyệt tạo task W7 thì chép SPEC sang `tasks/T-0xx-…/SPEC.md`. Lệnh cuối: `sha256sum w7-spec-nhap.md > SHA256SUMS-9`.

### Prompt cho Codex — soát nháp SPEC W7 (phiên 9)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: nháp SPEC W7 (đợt đánh giá FlashTicket), chưa có mã task: results/T-074/w7-spec-nhap.md (sha256 ở results/T-074/SHA256SUMS-9); do người làm T-074 soạn theo yêu cầu của điều phối T-070.
- Công đoạn: soát SPEC.
- Gói/cổng: P10 (W7, nhánh đánh giá kế hoạch giai đoạn 2 §8.3); chuẩn bị G6; đề xuất tạo task mới, chưa duyệt.
- Người làm và người phản biện chính thức: dự kiến người làm Claude, người phản biện Codex.
- Tài liệu gốc: results/T-074/w7-spec-nhap.md; tasks/_MAU/SPEC.md; results/T-074/thiet-ke-w6-5.md và thiet-ke-w6-4.md §0 (bảng hiệu lực), thiet-ke-w6-2.md, -3.md, -4.md; results/T-074/con-mo-w6.md; results/T-074/du-toan-4.json; results/T-074/e6-spec-nhap-5.md và results/T-074/e6/v2/; docs/DECISIONS.md (khối 23–24/11 cuối file); docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.3–8.4; AGENTS.md luật 8, 19, 20, 21; tasks/T-074-w6-thiet-ke-danh-gia/LOG.md phiên 9.
- Phản biện và phản hồi trước: không có cho nháp này (phản biện các bản W6 và E6: results/T-070/codex/ CX-06 … CX-39b; LOG T-074 phiên 1–8).
- Code và kết quả liên quan: results/T-074/SHA256SUMS-9; results/T-069/ (17 gói dev, manifest); results/T-072/v2/cham_offline_v2d.py; repo lab D:/Project/flashticket-rca-lab (HEAD trên máy đọc ở results/T-074/e6/b0-app.out, b0-obs.out).
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi điều phối/Minh cấp file phản biện riêng.

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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 10 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm (E6 v3 theo "Duyệt kết hợp", không máy)

- **Yêu cầu điều phối (24/11 ~04:00Z):** Minh trả lời "Duyệt kết hợp" cho E6: (1) giữ SQL thuận v2 B (không sửa `v2/sql/B/thuan-*.sql`; buộc phải sửa thì dừng, báo); (2) Codex sửa ngay lỗi nhỏ hai bên đồng thuận, một phiên Codex khác kiểm; (3) bỏ SQL nghịch và phân loại 50% "toàn CU/toàn DICH/lẫn", thay bằng khôi phục từ dump chụp ngay trước khi ghi, có thử khôi phục vào DB nháp trước; (4) chạy có người theo dõi, mỗi lần một DB. Chia việc: Codex CX-45 chỉ ghi `v3/b1c-yen.sh`, `v3/b0.sh`, `v3/thu-codex/`; phiên này ghi phần còn lại của `results/T-074/e6/v3/` và `e6-spec-nhap-6.md`, giữ nguyên v2/ và manifest cũ. Việc a–g (bộ chạy chiều thuận có dump + thử khôi phục; phân loại mọi rc ≠ 0 là chưa rõ, so cả nhóm trường với đầu và đích B; thủ tục khôi phục; sửa bộ kiểm theo CX-41/41b; phép thử; nháp 6; đề xuất chạy thuận trên DB nháp ghi "chờ Minh duyệt"). Không SSH, không chạm máy.
- **Tin điều phối thứ hai (~04:10Z):** Minh trả lời "Duyệt chạy thử" cho mục g: sau thử khôi phục vào DB nháp, chạy SQL thuận B (nguyên file v2) trên DB nháp, rồi kiểm DICH trên DB nháp, rồi mới ghi DB thật; lỗi → dừng DB đó, không ghi DB thật, báo điều phối. Bỏ chữ "chờ Minh duyệt" trong nháp 6. Đã làm: bước này thành bắt buộc trong `chuan-bi`; `ghi` từ chối chuẩn-bị thiếu dấu `thuan-nhap-dat`; nháp 6 §2 bước 1.7 và §8 ghi căn cứ. Phép đột biến lượt đầu (D1–D3 đã cho TRUOT như mong đợi) dừng giữa chừng để chạy lại toàn bộ trên bản cuối.
- **Quy trình:** lượt này khởi đầu từ yêu cầu đã chứa kết luận CX-41/41b, nên không có lượt tự soát độc lập trước khi đọc phản biện. Tôi đọc `CX-41-tin-cuoi.md`, `CX-41b-tin-cuoi.md`, `CX-45-brief.md`, SQL B v2, `chay.sh` v2, mẫu E1 (`results/T-071/e1/sua_ngay.sh`, `moc-db.json`, `moc/so-dong.txt`), danh sách container ở `e6/b0-app.out`.
- **Đối chiếu CX-41/41b (phần thuộc Claude):** kiểm yên `b1c` và bước 0 → phần Codex CX-45. Phân loại 50% sai với đích B (Event 5 DICH + 1 CU, Booking 4 DICH + 2 CU) — **đúng**; v3 so cả nhóm trường với đầu (toàn CU) và đích (cột 2 `truong.txt`). rc 3 sau COMMIT bị gọi "đã rollback" — **đúng** (16/16 file thuận/nghịch in `DA_COMMIT` sau `COMMIT`); v3: mọi rc ≠ 0 hoặc thiếu dấu → xác định. Bộ kiểm báo đạt sai (`purchased` 41706, `eventXstarts_at`, tên lạ) — **đúng**; v3 so tên theo nghĩa đen bằng awk, mỗi tên đúng một lần, không tên lạ, `purchased`/`held` so mốc kiểm yên. Thiếu `truong.txt` → đạt — **đúng**; v3 dừng mã 2. Tên DB lặp — **đúng**; v3 từ chối. `test -e` + `mkdir -p` hở — **đúng**; v3 `mkdir` nguyên tử cho thư mục lượt và khóa toàn cục. Nghịch đảo nhầm phiên bản — không còn áp dụng (bỏ nghịch). Cam kết "so mọi giá trị đã khóa" rộng hơn SQL (inventory không so `source_config_version`, `row_version`) — **đúng**, không sửa vì SQL thuận B giữ nguyên theo duyệt; nháp 6 không cam kết rộng hơn SQL.
- **Đầu ra:**
  - `results/T-074/e6/v3/chay.sh`: chế độ `chuan-bi` (đĩa, `kiem-khoa` đầu, chữ ký DML, `pg_dump -Fc` + sha256, thử khôi phục vào DB nháp, băm nội dung từng bảng + sequence hai bên phải trùng, xóa DB nháp), `ghi` (chuẩn-bị dùng một lần, còn hạn 30 phút; rc 0 + `DA_COMMIT` + kiểm DICH → 20; còn lại → xác định), `xac-dinh` (chờ phiên theo `application_name`, đọc dưới khóa, 20/21/22), `khoi-phuc` (dừng dịch vụ, đổi tên DB hiện tại thành `_hong_`, tạo lại, `pg_restore`, băm = dump, kiểm đầu, khởi động dịch vụ; lỗi restore → trả tên cũ), `kiem`. SQL lấy nguyên văn `v2/sql/B`, kiểm sha256 với `v2/SHA256SUMS`. Chuẩn-bị chạy thử thuận + kiểm DICH trên DB nháp (bắt buộc, Minh duyệt 24/11).
  - `results/T-074/e6/v3/thu/`: `fake_docker.sh`, `fake_df.sh`, `chay_thu.sh`, `chay_thu.out` (64/64 đạt), `dot-bien.out` (6 phép đột biến đều làm bộ thử trượt (D1 6, D2 1, D3 1, D4 3, D5 1, D6 1); `v2/SHA256SUMS` kiểm lại khớp (v2 không đổi)).
  - `results/T-074/e6-spec-nhap-6.md`: thủ tục từng DB có người theo dõi, xác định kết cục, khôi phục, luật 21, thời gian S5 (≈ 65–120 phút, CHƯA-KIỂM); mục cần Minh quyết còn: cách khôi phục thay cả DB (§8.2).
  - Manifest phần Claude: `results/T-074/SHA256SUMS-10`. `v3/SHA256SUMS` gộp phần Codex chưa lập: CX-45 bị cắt do hết usage 04:08Z, chưa có `thu-codex/SHA256SUMS`; điều phối báo chờ lượt CX-45r rồi mới gộp.
- **Tự kiểm:** `bash -n` 4 script. Bộ thử bắt một lỗi thật của bản đầu: `danh_gia` chia file theo `FNR==1`, file PHU rỗng (Ticket) làm đầu ra kiểm bị đọc như PHU → mã 7 sai; đã sửa (chia theo `FILENAME`), chạy lại đạt. Fake DML tăng sau khi báo làm T45 không phân biệt; sửa fake (tăng trước khi báo).
- **Chưa kiểm:** mọi lệnh trên PostgreSQL thật (`\gexec` băm, `pg_dump`/`pg_restore` vào DB nháp, CREATE/ALTER/DROP DATABASE, `pg_stat_user_tables` có thể trễ vài giây — chốt phụ; chốt chính là băm), `docker stop/start` dịch vụ, thời gian `pg_restore` trên exp-app.
- **Không làm:** không sửa `v2/` hay file Codex; không SSH; không commit; không subagent. Thử phép đột biến lần đầu bị chặn bởi kiểm an toàn (`rm -rf` biến tạm) — đã chạy lại trong thư mục scratchpad, không xóa gì.

### Kết thúc phiên 10 — 05:06Z

1. Đã làm: bộ chạy E6 v3 phần Claude, phép thử giả lập, nháp 6.
2. File: `results/T-074/e6/v3/chay.sh`, `results/T-074/e6/v3/thu/*`, `results/T-074/e6-spec-nhap-6.md`, `results/T-074/SHA256SUMS-10`, LOG này, dòng T-074 trong STATE.
3. Kiểm: 64/64 đạt phép thử giả lập; 6 phép đột biến đều làm bộ thử trượt (D1 6, D2 1, D3 1, D4 3, D5 1, D6 1); `v2/SHA256SUMS` kiểm lại khớp (v2 không đổi).
4. Cần quyết/chưa chắc: Minh quyết cách khôi phục thay cả DB với dịch vụ dừng (nháp 6 §8.2); mọi lệnh trên PostgreSQL thật chưa chạy (bước 1.7 sẽ là lần đầu, trên bản sao).
- Bước tiếp: khi điều phối báo CX-45r xong, lập `results/T-074/e6/v3/SHA256SUMS` gộp phần Codex (không sửa nội dung); Codex kiểm v3 (2 phiên, prompt dưới cho phần Claude); điều phối giao pha ghi. Lệnh cuối: `sha256sum … > results/T-074/SHA256SUMS-10`.

### Prompt cho Codex — kiểm bộ thực thi E6 v3 phần Claude và nháp 6 (phiên 10)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 E6, bộ thực thi v3: results/T-074/e6/v3/chay.sh, results/T-074/e6/v3/thu/ (phần Claude) và nháp results/T-074/e6-spec-nhap-6.md; phần Codex CX-45 (v3/b0.sh, v3/b1c-yen.sh, v3/thu-codex/) do phiên CX-45b kiểm riêng.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P9/P10, chuẩn bị G6 (E6 nền cho W7); khối cổng hiện có dùng theo bàn giao T-074 là G3.
- Người làm và người phản biện chính thức: Claude là người làm T-074, Codex là người phản biện.
- Tài liệu gốc: tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md, LOG.md (phiên 10); docs/DECISIONS.md khối 24/11; tin điều phối 24/11 ~04:00Z ("Duyệt kết hợp") chép ở LOG phiên 10; results/T-074/e6-spec-nhap-4.md, -5.md, -6.md; results/T-074/SHA256SUMS-10.
- Phản biện và phản hồi trước: results/T-070/codex/CX-39-tin-cuoi.md, CX-39b-tin-cuoi.md, CX-41-tin-cuoi.md, CX-41b-tin-cuoi.md; LOG T-074 phiên 8 và phiên 10.
- Code và kết quả liên quan: results/T-074/e6/v2/ và v2/SHA256SUMS (SQL B giữ nguyên); results/T-074/e6/v3/ (manifest v3/SHA256SUMS khi gộp phần Codex, phần Claude ở results/T-074/SHA256SUMS-10); results/T-071/e1/ (mẫu dump E1). Thử trên laptop: Git Bash, `bash results/T-074/e6/v3/thu/chay_thu.sh` (docker giả, không kết nối máy).
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; không SSH, không kết nối DB, không dùng subagent.

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

## Phiên 11 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm, đáp phản biện nháp SPEC W7 (CX-43, CX-43b)

- Yêu cầu điều phối (~04:45Z): sau E6 v3, đáp phản biện nháp W7 theo AGENTS §5 bước 7; nháp W7 bản 2 là file mới; không DECISIONS/WHY; không máy.
- **Ghi chú độc lập:** tin điều phối đã tóm tắt trước một phần kết luận phản biện (CX-43b xác nhận R1–R8; N1 = cách gom sự cố T-072 và W5 khác nhau khi cảnh báo đến sai thứ tự; N2 = vị trí chạy bù so với ô mốc K0; Codex đề nghị tách W7a/W7b, một khối/đêm, chỉ chụp, R3 phạm vi ghi trên máy, bù ở cuối đợt). Tôi chưa mở hai file `CX-43-tin-cuoi.md`, `CX-43b-tin-cuoi.md`. Điểm dưới tự soát trên `results/T-074/w7-spec-nhap.md` (sha256 ở `SHA256SUMS-9`), ghi lúc 05:07Z; điểm trùng với tóm tắt trên ghi rõ.

### Tự soát nháp W7 (trước khi mở CX-43/43b)

- **S1 (CHẶN tạo task) Phạm vi ghi trên máy thiếu thao tác đổi trạng thái:** nháp chỉ liệt kê thư mục ghi (`/srv/rca-lab/runs/t0xx-*`…), không liệt kê: triển khai commit lab W7 lên `/opt/rca-lab` hai máy; tiêm lỗi (`docker pause` Ticket, `pool.hold` Booking, `http.delay` Event qua hook/lease); phát tải k6 ở máy tải; đổi chế độ bộ chụp (b) giữa diễn tập và đêm W7; tạo đơn (đổi DB). SPEC duyệt không cấp được các quyền này. Trùng hướng với "R3 phạm vi ghi trên máy" trong tóm tắt điều phối.
- **S2 (CHẶN khóa) Ngân sách vé chưa tính pilot, bù và diễn tập:** 58.295 vé còn (E6 B) − 35.640 đơn bảo thủ của 27 chu kỳ (`du-toan-4.json#/phuong_an/0/K0_don_ca_dot_bao_thu`) = 22.655 cho pilot (6 chu kỳ, ~1.320 đơn/chu kỳ bảo thủ = 35.640/27 ≈ 7.920), mọi chu kỳ bù và diễn tập W9a (chưa ước). Chưa có quy tắc dừng khi vé còn không đủ cho đêm kế. Cần: đếm `purchased` đầu mỗi đêm, ngưỡng dừng, và trần số chu kỳ bù.
- **S3 (KHÔNG CHẶN) Không có trần tổng số lần bù:** bảng lỗi cho "bù 1 lần" mỗi slot nhưng không giới hạn tổng; nhiều slot hỏng có thể kéo thêm đêm. Cần trần (ví dụ quá N bù/đợt → dừng, trình Minh).
- **S4 (CHẶN tiêu chí xong) "Đợt thu đủ hoặc có lý do" không kiểm được:** không nêu số lần lặp hợp lệ tối thiểu mỗi ô × mức tải để vẫn báo kết quả ô đó, hay khi nào ô bị coi là thiếu.
- **S5 (KHÔNG CHẶN) Bù ở "cuối khối cùng đêm" làm lệch vị trí trong khối so với lịch trộn và so với ô mốc K0 đầu khối** (DB trôi theo thời gian K0). Trùng với N2 trong tóm tắt điều phối (tôi đọc tóm tắt trước khi tự soát nên không tính là tự tìm độc lập).
- **S6 (KHÔNG CHẶN) Đầu dò xác nhận can thiệp ở pilot chưa nêu cho từng ô** (đặc biệt TICKET-PAUSE và SLOW-EVENT): "đầu dò độc lập, điều kiện xác nhận khai trước (T-059)" chưa chỉ file/tiêu chí của T-059 cho 3 ô này.
- **S7 (KHÔNG CHẶN) Mẫu số phát hiện ×1 trong W7 nhỏ:** FP/giờ khỏe ×1 trong đợt chỉ lấy từ phút `khoe_x1` của 3 chu kỳ BINH-THUONG ×1 (+ đoạn K/N/H khỏe của chu kỳ lỗi nếu bộ chấm tính); nháp không nói số giờ dự kiến hay quan hệ với kết quả R5 ở E4 (383 phút). Cần nêu rõ số này chỉ mô tả, R5 vẫn lấy từ E4.
- **S8 (KHÔNG CHẶN) Cách gom sự cố dùng trong chấm W7 chưa chỉ rõ:** nháp nói "bộ chấm W4 v2d" nhưng chế độ (b) đi qua bộ điều phối W5; nếu hai bên gom khác nhau, số sự cố/độ trễ khác nhau. Trùng N1 trong tóm tắt điều phối (không tính là tự tìm độc lập).
- **S9 (KHÔNG CHẶN) Chi phí pha 6 chưa đo:** đã ghi "chưa đo"; giữ.
- Kiểm đầu vào: `results/T-064/cau-hinh-de-xuat.json` có thật (`ls`).

Tiếp theo: mở `results/T-070/codex/CX-43-tin-cuoi.md`, `CX-43b-tin-cuoi.md`; đối chiếu từng điểm.

### Đối chiếu CX-43 (R1–R8) và CX-43b (N1, N2) — kiểm trên file/code thật

| Điểm | Kết luận | Bằng chứng tôi kiểm | Sửa trong `w7-spec-nhap-2.md` |
|---|---|---|---|
| R1 đầu dò, D2 | **ĐÚNG** | `inj3.probe()` (lab `4b6c4b2`, dòng 201–240): toxics, audit hook booking/event, cgroup Booking, `payment_state`, RTT, `rabbit_booking`; không có pool Booking, queue Ticket, độ trễ đúng request Event. `chay_d2` (runner4 dòng 306–330): nền 120 s, ô 150 s, không gọi bộ chụp | pha 0a mục 1 (đầu dò từng ô theo T-059), mục 4 (nhịp bắt đầu hành trình + `dropped_iterations`); pha 2 chia 2a D2 / 2b chu kỳ đủ |
| R2 đường nhận (b) | **ĐÚNG** | `git diff --name-status 81a9273 1bb40ca -- observability`: xóa `t073-e5.yaml`; `bo_nhan.py` ghi `webhook.jsonl`; `incidents.py:119` đọc `canh-bao-*.jsonl`, dùng `seq` | pha 0b mục 7; pilot 2b tín hiệu dương; nhóm "giao nhận hỏng" |
| R3 phạm vi ghi | **ĐÚNG** | runner4 dòng 21–40, 71–75: sổ `ledger/` qua `sudo -u ledger`; `d2b-` ở `chay_d2`; `main` laptop `4b6c4b2` | bảng Phạm vi ghi theo máy/tài khoản; revision gốc/từng máy; Q4 |
| R4 đuôi cuối đêm | **ĐÚNG** | `thiet-ke-w6-4.md` §6: chụp ở t̂ + 750 s, t̂ ≤ S+1570 ⇒ S+2320, 520 s sau hết tải; `b0-v2.sh` cấm `orchestrator` | pha 4: thứ tự đầu đêm, đóng khoảng nhận, chờ gói niêm, bàn giao theo máy, quy tắc phiên bản |
| R5 lưới khuyết, CLI v2d | **ĐÚNG** | `cham_offline_v2d.py:497–504` từ chối `--ra` ngoài `v2/ra/`; DECISIONS 24/11 mục 2 | pha 0b mục 8 (import logic, ghi vùng W7, bảng "chưa phân xử", ba nhóm ca) |
| R6 tiêu chí trùng byte | **ĐÚNG** | `bang-theo-o-2.json`: `#/hang/*/moi/P7/status` = 16 OK, 1 ERROR; `#/hang/16/moi/P7/sha256 = null` (RECREATE-PAY) | pha 1 hồi quy: byte nơi có hash; ca lỗi so bước/loại; BARO dựng lại điểm, so thứ tự và hòa |
| R7 quan hệ; H5 | **ĐÚNG** cả hai | đọc `dc_bo_quan_he.py`, `chuoi.py` theo dẫn chiếu; dòng 21 bản 1 viết H5 như thuộc tính (b) — sai mức khái quát | Mục tiêu: "tác dụng gộp"; bảng câu hỏi: H5 theo thực thể, từng ca, (a) và (b) |
| R8 dự toán, vé | **ĐÚNG** | `nhat-ky-3.jsonl` lọc `msg == "V082 xong"`: 16 bản ghi, ví dụ `giay [22.89, 22.25]`; 58.295 là tồn pha đọc | Chi phí: V082 ≈ 25 s/lần, phần khác đo pha 1; ngân sách vé có pilot/bù/diễn tập |
| N1 hai cách gom | **ĐÚNG** | `incidents.py:193–200`: cảnh báo cầu nối chỉ thêm vào sự cố có `t_hat` nhỏ nhất, không gộp hai sự cố đã mở; T-072 sắp theo giờ bắt đầu | pha 0b mục 8: nguồn sự cố từng bảng, gói sớm nhất là chính, bảng ghép một–nhiều; Q9 |
| N2 bù trước ô mốc | **ĐÚNG** | bản 1 dòng 99–104 (bù cuối khối/đầu đêm sau) vs ô mốc đầu khối; W6 bản 2 dòng 339 "lịch con cuối đợt" | bù cuối đợt; Q5 |

**Tự soát S1–S9 ↔ phản biện:** S1 ⊂ R3; S2 ⊂ R8 (và chính S2 của tôi tính sai pilot "6 × 1.320 = 7.920": 1.320 là trung bình cả đợt, pilot D2 không phải chu kỳ 30 phút; bản 2 tính lại ≈ 1.470 từ nhịp 648 và 1.944 đơn/1.800 s, `du-toan-4.json` dòng 16–24); S3 (trần bù) — không có trong CX-43, thêm vào bản 2; S4 (tiêu chí xong ≥ 2/3 lặp hợp lệ mỗi ô × mức tải) — không có trong CX-43, thêm; S5 = N2; S6 ⊂ R1; S7 ⊂ R5 (FP ×1 trong đợt chỉ mô tả); S8 = N1; S9 ⊂ R8. Codex không nêu S3, S4; tôi không thấy điểm nào của Codex sai.

**Bất đồng còn lại:** không. Điểm cần Minh quyết: `w7-spec-nhap-2.md` mục "Cần Minh quyết" Q1–Q10 (mỗi mục có đề xuất, lý do, mặt trái). Đề xuất của tôi trùng hướng Codex ở Q1 (tách), Q2 (một khối/đêm), Q3 (chỉ chụp), Q4 (phạm vi ghi), Q5 (bù cuối đợt), Q8 (loại ô chỉ khi đầu dò đúng đích); thêm Q9 (nguồn sự cố), Q10 (trần bù, ngưỡng vé).

**Đầu ra:** `results/T-074/w7-spec-nhap-2.md` (bản 1 giữ nguyên), manifest `results/T-074/SHA256SUMS-11`. Không ghi DECISIONS/WHY, không chạm máy, không commit.

**Chưa kiểm:** tên chỉ số Hikari Booking và queue Ticket trên `36a3725`; đường nhận (b) W7; thời gian đuôi; nhu cầu vé của diễn tập W9a.

### Kết thúc phiên 11 — 05:11Z

1. Đã làm: tự soát nháp W7 (ghi trước khi mở phản biện), kiểm từng điểm CX-43/43b trên code/dữ liệu, nháp W7 bản 2.
2. File: `results/T-074/w7-spec-nhap-2.md`, `results/T-074/SHA256SUMS-11`, LOG này, dòng T-074 trong STATE.
3. Kiểm: đếm P7 status T-069 (16 OK/1 ERROR), V082 xong (16 bản ghi), diff alerting E5→H, đọc `inj3.probe`, `chay_d2`, `incidents.py`, guard v2d; số đơn từ `du-toan-4.json`.
4. Cần quyết: Q1–Q10 trong bản 2. E6: chờ CX-45r rồi gộp `v3/SHA256SUMS`; Codex kiểm v3.
- Bước tiếp: Codex kiểm lại bản 2 (prompt dưới); Minh quyết Q1–Q10. Lệnh cuối: `sha256sum w7-spec-nhap-2.md > SHA256SUMS-11`.

### Prompt cho Codex — kiểm lại phản hồi CX-43/43b và nháp W7 bản 2 (phiên 11)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: nháp SPEC W7 bản 2 results/T-074/w7-spec-nhap-2.md (sha256 ở results/T-074/SHA256SUMS-11); bản 1 results/T-074/w7-spec-nhap.md (SHA256SUMS-9).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10 (W7), chuẩn bị G6; đề xuất tạo task mới, chưa duyệt; khối cổng hiện có dùng là G3.
- Người làm và người phản biện chính thức: dự kiến người làm Claude, người phản biện Codex.
- Tài liệu gốc: results/T-074/w7-spec-nhap.md, w7-spec-nhap-2.md; tasks/_MAU/SPEC.md; results/T-074/thiet-ke-w6-2.md … -5.md, con-mo-w6.md, du-toan-4.json, e6-spec-nhap-6.md; docs/DECISIONS.md khối 23–24/11; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.3–8.4; tasks/T-074-w6-thiet-ke-danh-gia/LOG.md phiên 9 và 11.
- Phản biện và phản hồi trước: results/T-070/codex/CX-43-tin-cuoi.md, CX-43b-tin-cuoi.md; phản hồi người làm ở LOG T-074 phiên 11.
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab (laptop main 4b6c4b2; exp-obs 1bb40ca, exp-app 407b4f5 theo results/T-074/e6/b0-*.out); results/T-069/ (bang-theo-o-2.json, thu/t069-chinh/chay/nhat-ky-3.jsonl); results/T-072/v2/cham_offline_v2d.py, quy-tac-gom.json; results/T-059/danh-muc-loi.md.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; không SSH, không dùng subagent.

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

## Phiên 12 — 24/11/2026 — Claude (Opus 5.5, phiên `danh-gia-w6`) — laptop Minh — vai trò: người làm, đáp phản biện E6 v3 (CX-45b, CX-46, CX-46b)

- Yêu cầu điều phối: tự soát v3 rồi kiểm từng điểm CX-45b, CX-46, CX-46b; sửa điểm đúng thuộc phần Claude trong phạm vi "Duyệt kết hợp" + "Duyệt chạy thử" (24/11) vào `results/T-074/e6/v4/` và nháp E6 bản 7; giữ v3, nháp 6, manifest cũ, SQL B; không sửa file Codex; điểm 5 CX-46 trình Minh. Không SSH/DB, không commit, không subagent.
- **Ghi chú độc lập:** tin giao việc đã nêu tên một số điểm phản biện (câu "DB thật chưa đổi kể từ dump"; tên BAO lạ; T51 chưa thử nhánh kiểm DICH thất bại; cờ khôi phục `khong` vẫn ghi; đường xử lý lỗi trước khi phát SQL; lệnh gọi trong nháp; đối chiếu purchased trước Event; hai lỗi b0.sh). Tôi chưa mở bốn file kết luận. Điểm dưới tự soát trên `v3/chay.sh`, `v3/thu/`, `e6-spec-nhap-6.md` lúc 07:04Z; điểm trùng tên với tin giao việc đánh dấu (TG).

### Tự soát v3 (trước khi mở CX-45b/46/46b)

- **A1 (CHẶN khôi phục)** `khoi-phuc`: sau `IFS='|' read … < dbinfo.txt` của chuẩn-bị, `doc_dbinfo "$D"` ghi đè OWNER/ENC/COLL/CTYPE bằng giá trị DB hiện tại; DB mới được tạo theo trạng thái hiện tại chứ không theo chuẩn-bị, và không có phép so hai bộ.
- **A2 (CHẶN khôi phục)** `tra_ve` không kiểm kết quả: DROP/ALTER lỗi vẫn log "đã trả về"; không xác nhận `<db>_db` tồn tại và `_hong_` không còn. Thêm: nếu CREATE thất bại vì `<db>_db` đã tồn tại (người khác tạo), `DROP DATABASE IF EXISTS` trong `tra_ve` sẽ xóa DB đó.
- **A3 (CHẶN khôi phục)** `khoi-phuc` không đòi chuẩn-bị đã được một lượt `ghi` dùng (`DA_DUNG`) và lượt ghi đó có kết luận KHÁC; có thể khôi phục từ một dump cũ hơn, xóa thay đổi hợp lệ sau đó.
- **A4 (KHÔNG CHẶN)** `xoa_nhap` trả 1 ở các nhánh lỗi chuẩn-bị bị bỏ qua; KET_QUA không nói DB nháp còn. Cần ghi rõ để người trực xóa tay.
- **A5 (TG, KHÔNG CHẶN)** `danh_gia` nhận mọi dòng `BAO|…` lạ mà không báo.
- **A6 (TG)** băm thật = nháp chỉ chứng minh nội dung bảng (`relkind='r'`) và sequence tại thời điểm băm khớp dump; không phủ đối tượng khác (view, hàm, quyền) và không phủ khoảng từ lúc băm tới lúc ghi; chữ ký DML là chốt phụ có độ trễ. Câu "DB thật chưa đổi kể từ dump" trong nháp 6 mạnh hơn bằng chứng.
- **A7 (TG, KHÔNG CHẶN bộ chạy, CHẶN bằng chứng)** T51 dùng `mot_phan` nên trượt ở bước thuận trên nháp (rc 3), không chạm nhánh kiểm DICH thất bại.
- **A8 (TG)** chuẩn-bị vẫn DAT khi `khoi-phuc-tu-dong = khong`; `ghi` không chặn, nên có thể ghi khi đường hoàn tác đã duyệt không dùng được.
- **A9 (TG)** nháp 6 §2 bước 0 viết `bash chay.sh kiem CU event booking ticket payment` không có `MOC_PURCHASED`/`MOC_HELD` → bộ chạy trả 2 ngay. Lệnh trong nháp sai.
- **A10 (KHÔNG CHẶN)** `ghi` tạo `DA_DUNG` trước các kiểm DML/kiểm đầu; trượt ở đó thì chuẩn-bị bị tiêu, phải chuẩn-bị lại (bảo thủ, chỉ tốn thời gian; nháp không nói).
- **A11 (KHÔNG CHẶN)** fake `pg_restore` lỗi vẫn ghi một phần rồi trả mã; bộ chạy không kiểm DB nháp còn sót sau lỗi — trùng A4.

Tiếp theo: mở `results/T-070/codex/CX-45r-tin-cuoi.md`, `CX-45b-tin-cuoi.md`, `CX-46-tin-cuoi.md`, `CX-46b-tin-cuoi.md`.

### Kết thúc phiên 12 — dừng theo lệnh Minh (24/11, ~10:10Z, qua T-070)

1. **Đã làm:** tự soát v3 (A1–A11, ghi ở trên trước khi mở phản biện); đọc và kiểm CX-45b, CX-46, CX-46b trên code v3: mọi điểm đều đúng, không có bất đồng (chưa ghi bảng đáp từng điểm). Viết bộ chạy E6 v4, bộ thử giả lập và nháp E6 bản 7. **Dừng theo lệnh Minh: dừng toàn bộ E6, W7 hoãn.** Lượt chạy nền cuối (bộ thử + đột biến) bị dừng giữa chừng theo lệnh.
2. **File tạo trong phiên 12, CHƯA XONG, CHƯA TẠO MANIFEST, CHƯA QUA PHẢN BIỆN, KHÔNG DÙNG:**
   - `results/T-074/e6/v4/chay.sh`;
   - `results/T-074/e6/v4/thu/` (`fake_docker.sh`, `fake_df.sh`, `fake_ps.sh`, `chay_thu.sh`, `chay_thu.out`, `dot-bien.out`);
   - `results/T-074/e6-spec-nhap-7.md`.
   v3, nháp 6, SQL B (`v2/sql/B/`), file Codex và mọi manifest cũ không đổi. Không xóa, không đổi tên file nào.
3. **Kiểm đã chạy (giả lập, laptop):** `chay_thu.out` lượt cuối 86/86 đạt (gồm T08 thêm sau lượt đột biến đầu: mốc khớp DB giả nhưng lệch hằng số SQL B → `mo-luot` mã 3). `dot-bien.out` là lượt chạy lại bị dừng: D1–D7 mỗi đột biến làm ít nhất một phép thử trượt; D8 chưa có kết quả trong lượt này (lượt trước đó D8 bị bắt, D4 thì không — lý do thêm T08). Nháp 7 §7 đã sửa theo T08. **Chưa kiểm:** mọi lệnh trên PostgreSQL thật, `docker stop/start`, `ps` trên exp-app. Không SSH, không chạm DB hay máy nào, không gửi gì sang Codex.
4. **Còn mở / cần Minh:** CX-46 #5 (mã 22 có thay cả DB không) — đề xuất ở nháp 7 §6.1, chưa trình chính thức. Hai lỗi hiển thị `v3/b0.sh` (dòng 116, bộ lọc awk dòng 121–122) đã đồng ý là đúng; chưa giao Codex sửa.

**Bước tiếp theo nếu Minh mở lại E6:**
1. Đọc lệnh mở lại của Minh và lịch hạn bán; đối chiếu phạm vi đã duyệt 24/11 ("Duyệt kết hợp", "Duyệt chạy thử").
2. Chạy lại `bash results/T-074/e6/v4/thu/chay_thu.sh > results/T-074/e6/v4/thu/chay_thu.out` và lại cả 8 đột biến (kịch bản đột biến ở scratchpad phiên này có thể đã mất: mẫu là chép `v4/chay.sh`, thay một chuỗi, chạy `SCRIPT=<bản đột biến> bash chay_thu.sh`); ghi `dot-bien.out` đủ D1–D8.
3. Ghi bảng đáp từng điểm CX-45b/46/46b vào LOG; tạo `results/T-074/e6/v4/SHA256SUMS` và `results/T-074/SHA256SUMS-12`.
4. Trình Minh CX-46 #5; điều phối giao Codex sửa hai lỗi `b0.sh`; soạn hai prompt kiểm lại v4 cho Codex theo `docs/review-prompt.md`.
- Lệnh cuối đã chạy: lượt nền `bash chay_thu.sh …; bash dot4.sh` (scratchpad), bị dừng bằng TaskStop theo lệnh Minh.

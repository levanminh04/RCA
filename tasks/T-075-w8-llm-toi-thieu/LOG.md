# Nhật ký T-075

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 0 — 20/11/2026 — Claude (phiên điều phối T-070) — laptop Minh — vai trò: điều phối, khởi tạo task

- Tạo SPEC theo kế hoạch bản 5 (`tasks/T-070-dieu-phoi-giai-doan-2/SPEC.md`) và quyền Minh cho phiên điều phối (chat 20/11/2026, nguyên văn ở SPEC T-070): "… nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình". Phần "chờ Minh" trong SPEC chưa được duyệt.
- Hợp đồng giữa phiên: `tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md`; lịch máy: `LICH-MAY.md`. Phiên làm việc báo về điều phối khi kết thúc mỗi lượt (I15).
- Prompt Codex soát SPEC: ở LOG T-070 (gom cho T-070–T-075), Minh chuyển.

---

## Phiên 1 — 23/11/2026 — Claude (phiên `llm-w8`, khởi từ điều phối T-070) — laptop Minh — vai trò: người làm

- Minh duyệt Q6, Q7 ngày 23/11/2026 (DECISIONS, khối "Điều phối giai đoạn 2: gói E5/P/H và Q1–Q11"). Phạm vi lượt này: bước 2–3 SPEC ở chế độ ngoại tuyến, không gọi API LLM thật; không gửi dữ liệu ra ngoài (R3); nhà cung cấp, model, danh sách trường gửi đi Minh chọn sau. Không SSH, không commit, không subagent (Minh yêu cầu qua điều phối).
- Code đặt trong `results/T-075/` (chưa dùng worktree lab ở lượt này, theo giao việc của điều phối).
- Bước con 1 (đọc đầu vào): ca E5 trên laptop chỉ có file sự cố `results/T-073/e5/su-co/bbc0a6d44f.json` (kết luận V082, nhóm hạng 1, cảnh báo, độ phủ, số mẫu theo thực thể). File G1 của ca `7577dd5b` chưa có trên laptop (Q1 giao T-073 chép về). Ca G1 0.5 cũ có ở `results/T-065/may-l11/du-lieu/V082-V066+H8a/` (28 ca dev2, chế độ a). Chọn `1e5a3dc5` (CAUSE_FOUND, có kế thừa) và `729604d2` (NO_INTRINSIC_ANOMALY) vì nhỏ và phủ hai nhánh; không đọc nhãn của chúng.
- Bước con 2 (khuôn đầu vào): `results/T-075/goi_bang_chung.py`, `khuon-dau-vao.md`. Gói tách `gui_di` / `kiem_toan`; mỗi mục mang con trỏ nguồn; thời gian tương đối; loại nhãn, đường dẫn, mã ca, URL, trace ID, `ban.ghi_chu_hash`. Hash V082 của ca `t073-b` dẫn `#/du_lieu_loi/v082/output_sha256` (file sự cố) hoặc `#/che_do_b/du_lieu_loi/v082/output_sha256` (file G1), chỉ ở `kiem_toan`.
- Bước con 3 (khuôn đầu ra, prompt): `khuon-dau-ra.md`, `prompt-mau.md`. Trạng thái GIAI_THICH / KHONG_DU_BANG_CHUNG; khẳng định quan_sat/suy_luan kèm con trỏ JSON; gợi ý xử lý kèm căn cứ.
- Bước con 4 (bộ kiểm): `kiem_w8.py` (K1–K7), `chay_thu.py` (K8 gói sạch, K9 thứ hạng trước/sau, đối chứng chéo). Lượt chạy đầu 18/18 khớp mong đợi; đối chứng chéo lọt 2/30 cặp (đầu ra "không có bằng chứng" qua trên gói có bằng chứng) → thêm K4b; chạy lại: 18/18, 0/30 lọt, K8, K9 đạt. Chi tiết `ket-qua-thu.md`, số ở `ket-qua-thu.json`.
- Bước con 5: `de-xuat-minh.md` (danh sách trường, nhà cung cấp/model, xử lý khi trượt, file G1 ca E5), `README.md`, `SHA256SUMS` (34 file, `sha256sum -c` đạt).

### Kết thúc phiên 1 — 23/11/2026

1. **Đã làm:** bước 2–3 SPEC ở chế độ ngoại tuyến: khuôn đầu vào, khuôn đầu ra, prompt mẫu, bộ kiểm trích dẫn / không đủ bằng chứng / giữ thứ hạng; chạy thử trên ca E5 (từ file sự cố), 2 ca G1 cũ và 3 ca giả. Không gọi LLM, không gửi dữ liệu ra ngoài, không SSH, không commit, không subagent.
2. **File đã thay đổi:** tạo `results/T-075/` (README.md, khuon-dau-vao.md, khuon-dau-ra.md, prompt-mau.md, de-xuat-minh.md, ket-qua-thu.md, ket-qua-thu.json, goi_bang_chung.py, kiem_w8.py, chay_thu.py, ca-thu/*, SHA256SUMS); nối LOG này; dòng T-075 trong `docs/STATE.md`.
3. **Kiểm đã chạy:** `py -3 -I -B -X utf8 chay_thu.py` → `#/tong` = 18 khớp, 0 không khớp, K8 và K9 đạt; `#/doi_chung_cheo/dat_ngoai_y_muon` = []; `kiem_w8.py` CLI trên `ca-thu/e5` (đầu ra đúng → đạt, exit 0; sai-doi-hang → K4/K5/K6, exit 1); `sha256sum -c SHA256SUMS` đạt.
4. **Chưa chắc / cần Minh quyết:**
   - Task đạt: khuôn và bộ kiểm ngoại tuyến; ba thuộc tính của SPEC đạt trên ca thử **với đầu ra viết tay**. Chưa đạt "Tiêu chí xong" (chạy trong demo trên ca W5): chưa có LLM, chưa có file G1 ca E5.
   - Câu hỏi nguồn (giải thích chỉ dựa trên gói) mới trả lời ở mức "bộ kiểm bắt được các lỗi đã định". Chất lượng giải thích của model thật: chưa biết, thiếu lượt gọi thật. Bộ kiểm so chữ, không bắt suy luận sai nhưng đúng chữ.
   - Đầu ra mẫu ca E5 do người làm viết khi đã biết ô của lượt E5; không dùng làm bằng chứng chất lượng.
   - Nhánh `g1` + khối `che_do_b` chưa chạy trên file thật (hai ca cũ là chế độ a); tên khóa trong `che_do_b` có thể khác file sự cố.
   - Minh quyết (đề xuất ở `de-xuat-minh.md`): (1) danh sách trường gửi đi; (2) nhà cung cấp/model: đề xuất Claude API `claude-opus-5-5` + structured outputs, hoặc Bedrock nếu muốn dữ liệu ở lại tài khoản AWS; (3) xử lý khi đầu ra trượt bộ kiểm (gọi lại một lần, trượt nữa thì hiện "không đủ bằng chứng"); (4) chờ file G1 ca E5 từ T-073.

**Bước tiếp theo chính xác:** khi T-073 chép file G1 ca `7577dd5b` về laptop: `py -3 -I -X utf8 results/T-075/goi_bang_chung.py <file G1> g1 e5-g1`, soát khóa `che_do_b`, viết đầu ra mẫu, thêm ca vào `chay_thu.py`. Khi Minh chọn nhà cung cấp và danh sách trường: viết bước gọi LLM theo `prompt-mau.md`, chạy ≤ vài chục lần, lưu đầu ra thô và kết quả `kiem_w8`. Đọc trước: `results/T-075/de-xuat-minh.md`, `ket-qua-thu.md`.

**Lệnh cuối cùng đã chạy:** `py -3 -I -B -X utf8 chay_thu.py`, rồi `sha256sum -c SHA256SUMS` (trong `results/T-075/`).

### Prompt phản biện cho Codex (Minh chuyển)

Nguyên văn "Prompt chung" + khối "Soát kết quả" của `docs/review-prompt.md` (sinh bằng script từ file đó); không có khối trọng tâm cổng G6 nên không kèm khối cổng.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-075, tasks/T-075-w8-llm-toi-thieu/ (SPEC.md, LOG.md).
- Công đoạn: soát kết quả.
- Gói/cổng: W8 (docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2); MRP P8, P10; chuẩn bị G6. docs/review-prompt.md không có khối trọng tâm cổng G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-075-w8-llm-toi-thieu/SPEC.md; docs/DECISIONS.md khối "Điều phối giai đoạn 2: gói E5/P/H và Q1–Q11 (T-070, 23/11/2026)" mục Q1, Q6, Q7; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2; results/T-073/e5-ket-qua.md; results/T-073/g1-0.3.md; results/T-065/dinh-dang/0.5/ca.schema.json. Chưa có commit cho task (thư mục task và results/T-075/ chưa được theo dõi trong git).
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: results/T-075/ (README.md, khuon-dau-vao.md, khuon-dau-ra.md, prompt-mau.md, de-xuat-minh.md, ket-qua-thu.md, ket-qua-thu.json, goi_bang_chung.py, kiem_w8.py, chay_thu.py, ca-thu/), manifest results/T-075/SHA256SUMS. Nguồn đầu vào: results/T-073/e5/su-co/bbc0a6d44f.json; results/T-065/may-l11/du-lieu/V082-V066+H8a/1e5a3dc5.json và 729604d2.json. Lệnh (Python 3.12, thư viện chuẩn), trong results/T-075/: `py -3 -I -B -X utf8 chay_thu.py`; kiểm một đầu ra: `py -3 -I -B -X utf8 kiem_w8.py <goi.json> <dau-ra.json>`. chay_thu.py ghi lại ca-thu/*/goi.json, ca-thu/*/dau-ra-sinh-*.json và ket-qua-thu.json.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tasks/T-075-w8-llm-toi-thieu/REVIEW.md>.

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
```

---

## Phiên 2 — 23/11/2026 — Claude (phiên `llm-w8`) — laptop Minh — vai trò: người làm, đáp phản biện

- Giao việc từ điều phối T-070 (tin 10:0xZ 23/11): đáp CX-30, CX-30b; sửa phần đúng bằng file mới, giữ nguyên hash lượt 1; dùng G1 đầy đủ của ca E5 (`results/T-073/e5/ca-7577dd5b/`). Vẫn ngoại tuyến: không gọi LLM, không gửi ra ngoài, không subagent, không commit.
- Hash lượt 1: `sha256sum -c results/T-075/SHA256SUMS` đạt trước khi sửa.
- **Tự soát trước khi mở CX-30/CX-30b** (điểm tự tìm):
  - N1 (CHẶN kết luận "gói E5 đúng nguồn"): `goi_bang_chung.py:166` lấy `trang_thai_chay` của gói E5 từ `#/du_lieu_loi/p7_status`. Đây là trạng thái bước P7, không phải V082, nên gói trộn hai bản trong cùng khối `ket_qua_rca`.
  - N2 (CHẶN "bộ kiểm chặn đầu ra sai"): `kiem_w8.kiem` không kiểm kiểu. Khi `khang_dinh` là chuỗi, hàm sập `AttributeError` thay vì trả trượt. Khóa lạ ở gốc (`them`) vẫn đạt. Câu `"a"` có trích dẫn hợp lệ vẫn đạt. Lệnh thử ghi ở phiên này, kết quả `CRASH` và `[]`.
  - N3 (KHÔNG CHẶN): mẫu E5 `g1` viết "sau t̂ không còn … metric bắt buộc". Căn cứ `/do_phu/thieu_bat_buoc` chỉ nói thiếu phủ trong [t−300, t+300), không nói thời điểm. Câu mạnh hơn căn cứ, nhưng bộ kiểm so chữ không bắt được.
  - N4 (KHÔNG CHẶN): K3 chỉ nhận ra tên có trong gói. Đã khai ở `khuon-dau-ra.md` §3.
- Mở `results/T-070/codex/CX-30-tin-cuoi.md` và `CX-30b-tin-cuoi.md` sau khi ghi các điểm tự soát ở trên. N1 tự soát nằm trong R2. N2 tự soát nằm trong R3. N3 tự soát là một phần của R1.
- Hash G1 ca E5: `sha256sum -c ../ca-7577dd5b.SHA256SUMS` (chạy trong `results/T-073/e5/ca-7577dd5b/`) đạt.
- Sửa bằng file mới; bản 1 giữ nguyên (`sha256sum -c SHA256SUMS` vẫn đạt). Các file mới: `goi_bang_chung_2.py`, `kiem_w8_2.py`, `viet_mau_2.py`, `chay_thu_2.py`, `ca-thu-2/`, `ket-qua-thu-2.json`, `ban-2.md` (thay đổi, quy tắc ứng viên, kết quả, đề xuất sửa), `SHA256SUMS-2` (42 file mới).
- Kết quả: `py -3 -I -B -X utf8 chay_thu_2.py` cho `#/tong` = 28 đầu ra (8 viết tay, 20 sinh), 28 khớp mong đợi; K8, K9 đạt; `#/doi_chung_cheo` có 49 cặp, 0 lọt; `#/tong/dat` = true.

### Đáp phản biện CX-30 (R1–R6) và CX-30b (N1–N3)

| Điểm | Kết luận | Bằng chứng riêng | Sửa (bản 2) |
|---|---|---|---|
| R1 mẫu E5 thiếu căn cứ | **Đúng** | Mẫu `ca-thu/e5/dau-ra-dung.json` `#/goi_y_xu_ly/0` không trích log. Danh sách thiếu phủ không cho biết thời điểm mất mẫu. `#/khang_dinh/1` chỉ trích `50`, `60`. Trùng điểm tự soát N3 | `viet_mau_2.py` (e5-su-co): dẫn riêng span, log của Payment cùng quy ước khóa vắng và phạm vi P7; viết "sáu nguồn metric cơ sở"; dẫn cả đối tượng cảnh báo. Chưa đối chiếu `prometheus-bo-sung.json` (20 mẫu liveness) trong lượt này; mẫu chỉ nói về đầu vào P7 cơ sở |
| R2 lẫn P7/V082 | **Đúng** | `goi_bang_chung.py:166` lấy `p7_status`. `so_mau_vao_loi` là đầu vào P7, gồm cả hàng ngoài cửa sổ. Trùng điểm tự soát N1 | `goi_bang_chung_2.py`: `trang_thai_chay` = null ở nhánh sự cố; đổi tên `so_mau_dau_vao_p7_co_so` kèm `pham_vi`; tách hàng ngoài cửa sổ; thêm `pham_vi` cho `do_phu`; thêm giới hạn D3 từ `che_do_b.gioi_han` |
| R3 đạt mà trái khuôn | **Đúng** | Tái hiện cả ba phản ví dụ thành `sinh-sai-r3a/r3b/r3c`; bản 1 sập ở trường hợp `null`. Trùng điểm tự soát N2 | `kiem_w8_2.py`: thêm K0; K4 áp theo trạng thái đầu ra; trả `hop_khuon` riêng. Bản 2 bắt K4/K4/sai khuôn. Đề xuất đổi thông báo và rút câu "không bao giờ hiện câu bịa" (`ban-2.md` §4) |
| R4 trùng tên không giải thích hạng | **Đúng** | `gia-4` (e5-g1 bỏ hai mục F_I = 1 của Booking): bản 1 cho rằng gói đủ | Quy tắc mới: mọi thực thể nhóm hạng 1 cần mục F_I = 1; `GIAI_THICH` phải trích một mục như vậy; gói sắp F_I = 1 trước khi cắt. `gia-4` → không đủ, giải thích bị K4 bắt. Quy tắc là **ứng viên**, chưa có WHY. Nhánh H5 sẽ bị coi là không đủ (`ban-2.md` §2) |
| R5 K8 và chữ tự do | **Đúng** (nguy cơ, chưa rò thật) | `goi_bang_chung.py:136` chép `summary` | Bỏ `tom_tat` khỏi gói |
| R6 kết quả chéo và mô tả | **Đúng** | `chay_thu.py` không tính cặp lọt vào `tong.dat`. STATE ghi "18 đầu ra viết tay", thực tế 7 viết tay + 11 sinh | `chay_thu_2.py` tính cặp lọt vào `dat`; kết quả ghi riêng `ket-qua-thu-2.json`; đếm `viet_tay`/`sinh`; sửa dòng STATE |
| CX-30 mục 2: phạm vi Q7 | **Đúng một phần** | Q7 ghi "ca giả"; SPEC ghi "ca có sẵn", "ca W5". Không dữ liệu nào ra ngoài | Trình Minh xác nhận (`ban-2.md` §4) |
| CX-30b N1 K5 cho giấu thiếu phủ | **Đúng** | Tái hiện `gia-3/sinh-sai-n1-giau-thieu-phu`; bản 1 cho đạt | K5 đòi một mục thiếu trích `/do_phu/du_cua_so` hoặc `thieu_bat_buoc` |
| CX-30b N2 `false` = `0` | **Đúng** | Tái hiện `e5-su-co/sinh-sai-n2-bool-so` | So kiểu JSON chặt |
| CX-30b N3 K4b bác câu đúng | **Đúng** | Tái hiện `cu-1/sinh-dung-n3-boi-canh` | K4b chỉ kiểm con trỏ khai trong `vang`; câu bối cảnh đạt |

### Kết thúc phiên 2 — 23/11/2026

1. **Đã làm:** tự soát lượt 1; đáp từng điểm CX-30, CX-30b (bảng trên); sửa bằng file mới, dùng G1 đầy đủ của E5; chạy thử bản 2. Không gọi LLM, không gửi ra ngoài, không SSH, không subagent, không commit.
2. **File:** mới trong `results/T-075/` (danh sách ở trên, manifest `SHA256SUMS-2`); nối LOG này; dòng T-075 trong `docs/STATE.md`. File bản 1 không đổi.
3. **Kiểm:** `sha256sum -c SHA256SUMS` đạt; `sha256sum -c SHA256SUMS-2` đạt; G1 E5 khớp manifest T-073; `chay_thu_2.py` có `#/tong/dat` = true (28/28, 0/49 lọt, K8, K9).
4. **Còn mở / cần Minh:**
   - Tiêu chí xong của SPEC (chạy LLM trong demo W5) chưa đạt: chưa có lời gọi LLM.
   - Quy tắc "đủ bằng chứng" bản 2 là ứng viên, chưa có WHY. Nhánh H5 chưa có ca thử. Gói chưa có trường H5.
   - Bộ kiểm vẫn so chữ; câu sai nghĩa nhưng đúng chữ vẫn qua.
   - Mẫu E5 viết bởi người đã biết ô; không phải bằng chứng chất lượng.
   - Minh quyết: danh sách trường (đã bỏ `tom_tat`); nhà cung cấp/model (giữ đề xuất ở `de-xuat-minh.md` §2); cách xử lý khi trượt (`ban-2.md` §4); phạm vi nguồn thật cho Q7.

**Bước tiếp theo:** chờ Codex kiểm lại bản 2 và Minh quyết các điểm trên. Khi có nhà cung cấp: viết bước gọi LLM dùng `goi_bang_chung_2` và `kiem_w8_2`, sửa `prompt-mau.md` thành bản 2 (khuôn `T075-ra-2`, khóa `vang`, thông báo khi sai khuôn).

**Lệnh cuối:** `sha256sum -c SHA256SUMS-2` (trong `results/T-075/`).

### Prompt kiểm lại cho Codex (Minh chuyển)

Nguyên văn "Prompt chung" + khối "Kiểm lại phản hồi và sửa" của `docs/review-prompt.md` (sinh bằng script từ file đó); không có khối trọng tâm cổng G6.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-075, tasks/T-075-w8-llm-toi-thieu/ (SPEC.md, LOG.md).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: W8 (docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2); MRP P8, P10; chuẩn bị G6. docs/review-prompt.md không có khối trọng tâm cổng G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-075-w8-llm-toi-thieu/SPEC.md; docs/DECISIONS.md khối "Điều phối giai đoạn 2: gói E5/P/H và Q1–Q11 (T-070, 23/11/2026)" mục Q1, Q6, Q7; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2. Chưa có commit cho task.
- Phản biện và phản hồi trước: results/T-070/codex/CX-30-tin-cuoi.md; results/T-070/codex/CX-30b-tin-cuoi.md; phản hồi của người làm ở tasks/T-075-w8-llm-toi-thieu/LOG.md, mục "Phiên 2".
- Code và kết quả liên quan: bản 1 trong results/T-075/ (manifest results/T-075/SHA256SUMS); bản 2 gồm results/T-075/ban-2.md, goi_bang_chung_2.py, kiem_w8_2.py, viet_mau_2.py, chay_thu_2.py, ca-thu-2/, ket-qua-thu-2.json (manifest results/T-075/SHA256SUMS-2). Nguồn: results/T-073/e5/su-co/bbc0a6d44f.json; results/T-073/e5/ca-7577dd5b/ (manifest results/T-073/e5/ca-7577dd5b.SHA256SUMS); results/T-065/may-l11/du-lieu/V082-V066+H8a/1e5a3dc5.json và 729604d2.json. Lệnh (Python 3.12, thư viện chuẩn), trong results/T-075/: `py -3 -I -B -X utf8 viet_mau_2.py` rồi `py -3 -I -B -X utf8 chay_thu_2.py` (ghi lại ca-thu-2/ và ket-qua-thu-2.json); kiểm một đầu ra: `py -3 -I -B -X utf8 kiem_w8_2.py <goi.json> <dau-ra.json>`.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tasks/T-075-w8-llm-toi-thieu/REVIEW-<n>.md>.

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
```

---

# Nhật ký T-057

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục.

---

## Phiên 1 — 09/11/2026 — Claude — Windows (laptop) — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, MRP, DT18, hướng dẫn của cô, LESSONS, DECISIONS (mục 08–09/11), review-prompt, mẫu SPEC. Chưa có đầu ra phiên trước (task mới).

**Công đoạn và mục tiêu nguồn:** trình SPEC. Nguồn: MRP §7 (sáu câu G4), §8 (khung báo cáo cho cô), §3 (RQ3), DT18-NV2/NV3, hướng dẫn của cô. Minh giao (chat 09/11/2026): Claude làm, Codex phản biện; soạn SPEC sau khi tự rà toàn bộ kết quả P3–P7, RE3, T-055, T-056.

**Diễn biến:**
- Đọc báo cáo và đính chính T-054 (001–004), T-055 (001), T-056 (001); gói G2 (`results/T-034/goi-g2.md`); thiết kế M1 (`results/T-043/bao-cao.md`); hồ sơ G3; protocol khóa (`results/T-054/runs/chuan-bi-main-013-v2/activated-001/protocol.json#/hypotheses`, `#/interpretation`).
- Phép đếm chỉ đọc (để chốt quan sát ở Phụ lục A của SPEC):
  - MRR dev theo vế: `results/T-052/ket-qua-dev.json#/worlds/P/<bộ>/summary/<vế>/metrics/rr`.
  - Tập nút trong `extra/canh` của `result.json` M1 (đường dẫn ở `PT#/trung_gian_theo_ca/*/M1/result`): TT 26 service, OB 10 service.
  - Tầng của root và Σ thực thể tầng 1 trong `PT#/trung_gian_theo_ca/*/M1`: TT root tầng 1 60/60, Σ tầng 1 = 1342; OB root tầng 2 1/34, Σ tầng 1 = 125; root có kênh bị giải thích TT 28/60, OB 10/34.
  - `avg@5` có trong `results/T-054/reports/main-013-v2/tables.json#/rows/*/metrics`.
  - 22 file `results/T-054/runs/sua-cd3-ob-001/nhan/ec2_{1,2}/ra/dev-*.json` có `ban_ghi_cu/extra/don_vi_phan_vi` và `kenh_co`.
- Trình SPEC trong chat. Tạo `SPEC.md`, `LOG.md`, dòng T-057 trong STATE sau khi Minh duyệt.

**Quyết định của Minh trong phiên:**
- “Duyệt, tạo file” (09/11/2026), trả lời câu “Duyệt SPEC T-057 để tạo file, hay gửi Codex soát trước?”. Minh duyệt SPEC ngày 09/11/2026. Chưa ghi DECISIONS.

**Kết thúc phiên:**
1. Đã làm gì: rà kết quả, soạn và trình SPEC; tạo file sau khi Minh duyệt.
2. File đã thay đổi: `tasks/T-057-ho-so-g4/SPEC.md`, `tasks/T-057-ho-so-g4/LOG.md` (tạo mới); dòng T-057 trong `docs/STATE.md`.
3. Kiểm tra đã chạy và kết quả: các phép đếm chỉ đọc ở mục Diễn biến. Chưa kiểm hash manifest (bước B0).
4. Điều chưa chắc hoặc cần Minh quyết (kèm đề xuất của Claude):
   - **Quyền H11** (đọc lại metric thô OB test trên laptop, dưới 3 giờ, mô tả). Đề xuất: cấp. Mặt trái: thêm tiếp xúc test đã mở toàn bộ. Phương án khác: giữ OPEN, bản đồ độ khó thiếu OB.
   - **Định dạng báo cáo cho cô.** Đề xuất: `.md` trong repo làm nguồn, xuất `.docx` ở bước cuối, khoảng 12–15 trang. Mặt trái: giữ hai bản khớp nhau. Phương án khác: chỉ docx, khó soát số bằng máy. Cần Minh xác nhận đường dẫn báo cáo gửi cô 21/10 (`docs/KE-HOACH-GIAI-DOAN-TOI.md:855` trỏ `C:\Users\84583\Downloads\Định hướng chức năng AI cho đồ án tốt nghiệp.docx`).
   - **Câu xin cô định hướng.** Đề xuất: (a) đồ thị tham gia quyết định báo động (M-20); (b) đánh giá RQ3a chỉ trên FlashTicket; (c) dữ liệu công khai "đơn giản": thêm dataset khó hay dồn lực FlashTicket; (d) GNN có bắt buộc (WHY-10).
   - **Sửa STATE ngoài dòng T-057.** "P8 (LLM, dự kiến T-058)" → "P8 hoãn; T-058 = bộ đọc FlashTicket". Đề xuất: duyệt.
   - **Sửa MRP** (chưa duyệt, đề xuất trong chat 09/11): E-MRP-1 (§8 mục 5: P8 hoãn, thêm điều kiện giúp/không giúp và giới hạn độc lập); E-MRP-2 (§5 P8: hoãn sau RCA bản đầu FlashTicket, G5 dời); E-MRP-3 (§3 RQ3a: P7 chỉ chế độ (a), RQ3a mức hệ thống đánh giá ở P10). Đề xuất: duyệt cả ba; giữ ngỏ chạy chế độ (b) nếu cô yêu cầu.
   - **Tách H14, H15.** Đề xuất: H14 sang task chuẩn bị thiết kế FlashTicket (chỉ khi H8 thiếu dữ liệu); H15 sang T-058.
   - **Codex soát SPEC.** Minh duyệt trước khi Codex soát. Prompt ở dưới; Minh quyết gửi hay bỏ qua.
5. Bước tiếp theo chính xác: B0 — chạy `py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents` (lệch đã biết duy nhất: `docs/LESSONS.md`), kiểm sha256 theo `results/T-054/reports/p7a-013-v2/manifest-006.json`, `results/T-055/manifest-002.json`, `results/T-056/manifest-003.json`; rồi B1–B6.
6. Lệnh cuối cùng đã chạy: kiểm trường `don_vi_phan_vi`/`kenh_co` trong `results/T-054/runs/sua-cd3-ob-001/nhan/ec2_1/ra/dev-14701a3bbb.json` (Python chỉ đọc).

---

## Prompt bàn giao của lượt này cho agent đối phương (soát SPEC)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-057 — Hồ sơ G4 và báo cáo tiến độ cho cô; tasks/T-057-ho-so-g4/SPEC.md (Minh duyệt 09/11/2026, trước khi soát) và tasks/T-057-ho-so-g4/LOG.md phiên 1 (các điểm chờ Minh quyết và đề xuất sửa MRP E-MRP-1…3).
- Công đoạn: soát SPEC.
- Gói/cổng: P7 (tổng hợp, phân tích), cổng G4.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện.
- Tài liệu gốc: docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/STATE.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/KE-HOACH-GIAI-DOAN-TOI.md (Phụ lục P1); tasks/_MAU/SPEC.md. Thay đổi chưa commit so với commit b91232eb: docs/DECISIONS.md, docs/LESSONS.md, docs/STATE.md, tasks/T-054-khoa-g3-chay-p7-a/LOG.md; results/T-055/, results/T-056/, tasks/T-055-re3-ban-cuoi/, tasks/T-056-phan-tich-bo-sung/, tasks/T-057-ho-so-g4/ chưa được theo dõi trong git.
- Phản biện và phản hồi trước: không có cho T-057.
- Code và kết quả liên quan: results/T-034/goi-g2.md, results/T-034/ban-do-g2.json; results/T-040/bao-cao-p5b.md, results/T-040/ban-giao-p6.md; results/T-043/bao-cao.md; results/T-052/ket-qua-dev.json, results/T-052/ho-so-g3-004.md; results/T-054/reports/main-013-v2/a4.json, results/T-054/reports/main-013-v2/tables.json; results/T-054/reports/p7a-013-v2/ (bao-cao.md, dinh-chinh-001.md … dinh-chinh-004.md, phan-tich-nhom.json, phan_tich.py, manifest-006.json); results/T-054/runs/chuan-bi-main-013-v2/activated-001/protocol.json; results/T-054/runs/sua-cd3-ob-001/; results/T-055/reports/re3/ (bao-cao-re3.md, dinh-chinh-001.md, phan-tich-re3.json), results/T-055/manifest-002.json; results/T-056/ (bao-cao.md, dinh-chinh-001.md, ket-qua.json, ket-qua-002.json, manifest-003.json); tasks/T-054-khoa-g3-chay-p7-a/, tasks/T-055-re3-ban-cuoi/, tasks/T-056-phan-tich-bo-sung/. Kiểm manifest: py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents (xem DECISIONS mục "LESSONS không ghim trong manifest, 08/11/2026").
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phiên 2 — 09/11/2026 — Claude — Windows (laptop) — vai trò: người làm

- Mở phiên. Minh dán prompt có câu "Codex là người làm, Claude phản biện". Claude dừng, hỏi lại. Minh trả lời (chat 09/11/2026): "prompt ghi nhầm, claude là người làm chính, codex phản biện". Vai giữ như SPEC dòng 4–5; không sửa SPEC.
- Trình tự theo prompt của Minh: (1) đánh giá độc lập trước khi đọc SPEC; (2) đối chiếu SPEC; (3) kết luận chặn/không chặn; (4) triển khai.
- Khai tiếp xúc trước bước 1: lúc kiểm vai, Claude đã đọc SPEC dòng 4–5 (hai dòng vai) và phần cuối LOG (khối prompt mẫu). Chưa đọc phần nội dung SPEC.

### Phiên Claude — đánh giá độc lập (bước 1, chưa đọc SPEC)

Nguồn đã đọc: MRP §0–§3, §6–§8 (và P6/P7); DT18; hướng dẫn của cô (`docs/reference/sources/advisor-2026-09-23.md`); T-054 `bao-cao.md` + đính chính 001–004; T-055 `bao-cao-re3.md` + đính chính 001; T-056 `bao-cao.md` + đính chính 001; T-034 `goi-g2.md` §0–§1; T-043 `bao-cao.md` §0, §8–§11; T-052 `ket-qua-dev.json`; T-040 `bao-cao-p5b.md` §6–§7; T-021 `goi-g1.md` §3.4.

Viết tắt: A = `results/T-054/reports/main-013-v2/a4.json`; T = `results/T-054/reports/main-013-v2/tables.json`; PT = `results/T-054/reports/p7a-013-v2/phan-tich-nhom.json`; R = `results/T-055/reports/re3/phan-tich-re3.json`; K/K2 = `results/T-056/ket-qua.json` / `ket-qua-002.json`; D = `results/T-052/ket-qua-dev.json`.

**A. G4 cần chứng minh gì** (MRP §7 bảng cổng: "Kết quả và phân tích; báo cáo tiến độ cho cô"; sáu câu cổng; §3 "Hoàn thành nghĩa là gì"; §6 mục 3):

- G4-1. Bảng kết quả P7(a) của ba bộ (TT, OB, RE3-OB), theo vế, có CI theo ô, thắng/hòa/thua theo ca, tách theo loại lỗi và vị trí root. Đã có ở T-054 §4–§6 và T-055 §2; G4 phải gom và dẫn đúng bản sau đính chính.
- G4-2. Câu trả lời RQ3b, RQ3d (và trạng thái RQ3a, RQ3c) kèm điều kiện đúng/không đúng và cơ chế ("Đồ thị không giúp ở X, vì Y" là câu hợp lệ, MRP §3).
- G4-3. Sáu câu cổng, từng câu có bằng chứng.
- G4-4. Khai C-15 B/Q-247: phần nào là kết quả đầu của bản khóa, phần nào là sửa/phân tích sau khi xem test (adapter OB D1; C-d3 OB Đ12; T-056; đính chính).
- G4-5. Báo cáo cho cô theo đúng 7 phần MRP §8, mỗi phần mở bằng câu "trả lời nhận xét nào". Phần 5 (P8 LLM) chưa có; phần 6 (FlashTicket) chỉ là hướng.
- G4-6. Khai rõ phần thiếu: RQ3a P/R/F1 (Q-245), nhãn vùng RQ3c, P8, FlashTicket, cạnh thông điệp/dữ liệu (DT18-NV2).

**B. Kết luận yếu hoặc dễ bị cô/hội đồng chất vấn**

- Y1. **Thông điệp tổng: M1 không hơn rõ baseline mạnh ở bộ nào.** TT: ΔMRR M1−TORAI B = 317/7200, CI [−0,033; 0,149] (`A#/TT/P/delta`, `A#/TT/P/E04/lo_12`, `hi_12`). OB: ΔHit@5 = 3/34, không đạt (`A#/OB/P/delta`, `A#/OB/P/pass_formula`). RE3: M1−M4 = −0,050, CI [−0,133; 0,033], 1/25/4 (`R#/so_cap/M1-simplerca|rr`). Câu hỏi đầu tiên của cô sẽ là "phương pháp đồ thị có tốt hơn không"; G4 phải trả lời thẳng câu này, không chỉ "đạt E-04".
- Y2. **Lợi ích của quan hệ chỉ có điều kiện và không đến từ đồ thị dịch vụ.** TT: M1 = C-a0, 2/56/2 (`PT#/so_cap/RE2-TT|M1-C-a0|RR`). RE3: M1 = C-a0, 1/28/1 (`R#/so_cap/M1-C-a0|rr`). OB: +0,164, 11/20/3 (`PT#/so_cap/Nezha-OB|M1-C-a0|RR`), nhưng phần E1 giảm còn +0,079 khi bỏ 4 ca D1 (`results/T-054/reports/p7a-013-v2/dinh-chinh-001.md` Đ2). Phần hơn đến từ E1/E2 (quan hệ cha–con của span), không từ bước xếp hạng: M1 − C-d2 OB = −0,0025 (`PT#/so_cap/Nezha-OB|M1-C-d2|RR`). Hội đồng sẽ hỏi "đồ thị phụ thuộc dịch vụ góp gì".
- Y3. **Nghĩa hẹp của "graph-based anomaly detection" (MRP §2.3) có bằng chứng yếu.** Thành phần đồ thị tham gia điểm bất thường là E5 (tách tự sinh/kế thừa). Trên test, E5 đổi RR root 1/60 TT, 0/34 OB (`results/T-054/reports/p7a-013-v2/dinh-chinh-002.md` Đ6); trên RE3, E5 làm root mất 2 hạng ở `test-428cf2c868` (`results/T-055/reports/re3/dinh-chinh-001.md` Đ2). E6b (PageRank) tắt trong M1; GNN không làm. Ba ví dụ thuật toán của cô phải có câu trả lời "làm/không làm, vì sao".
- Y4. **Tác dụng thành phần trên dev không lặp lại trên test** — chưa báo cáo nào đặt cạnh nhau. Lệnh (chạy trong phiên này): đọc `D#/worlds/P/<bộ>/summary/<vế>/MRR/phan_so` và `D#/worlds/P/<bộ>/pairs_M1_minus/<vế>/counts`.
  - TT dev: C-a0 59/60 ≈ 0,983 > M1 167/180 ≈ 0,928; M1−C-a0 1/25/4. Test TT: M1 = C-a0.
  - OB dev: bo-E1 = M1 (48/55); test OB: E1 +0,130 (`PT#/so_cap/Nezha-OB|M1-bo-E1|RR`).
  - OB dev: bo-E5 ≈ 0,806 < M1 ≈ 0,873 (4 thắng/0 thua); test OB: E5 không đổi RR ở 34/34.
  - OB dev: C-d2 ≈ 0,899 > M1 ≈ 0,873 (3/17/2).
  - Hệ quả: câu "thành phần X giúp" không ổn định giữa dev và test. G4 cần câu "vì sao vẫn chọn cấu hình M1 trên dev khi C-a0 hơn ở TT dev" (dẫn luật chọn khối K, QT4), và không trình tác dụng thành phần trên test như đã được dev tiên đoán.
- Y5. **Sức phân xử thấp.** TT 6/20 ô khác 0 (`A#/TT/P/counts`); OB 3 ô hữu hiệu, p nhỏ nhất 1/8 (`A#/OB/P/cell_sign_at_zero/p_exact`); RE3 10 ô; Hit@5 chạm trần ở cả ba (`PT#/bang_theo_ve_P/Nezha-OB|M1/Hit5_Q`; T-055 §2); power câu (1) ≈ 0,19 (WHY-06, theo T-054 `bao-cao.md` §3.1). "CI chứa 0" phải đọc là "chưa phân biệt", không là "bằng nhau".
- Y6. **Độ mạnh baseline có lỗ.** TraceRCA/MicroRank là bản RCAEval khác bài gốc (T-034 G2-H01, G2-H03); CIRCA và TORAI B không hỗ trợ OB, nên OB chỉ so được M4, có giới hạn tái lập Q-192; TORAI A 6/180 slot (`dinh-chinh-004.md` Đ14). SimpleRCA mạnh nhất RE3 (QT7).
- Y7. **Nhiều phân tích sau khi xem test.** T-056, đính chính 001–004, C-d3 OB. Các "bài học thiết kế" (khóa theo độ bền, xử lý IQR = 0, kênh lỗi theo cạnh; `results/T-056/bao-cao.md` mục "Bài học thiết kế") sinh từ test, phải mang nhãn C-15 B và "chưa kiểm".
- Y8. **"Dữ liệu đơn giản".** Root lệch bền nhất 48/60 TT, 28/30 RE3 (`K2#/tom_tat/<bộ>/root_events_hon_moi_service_khac`); R1 tái lập khối đầu và RR root của M4 (`results/T-056/dinh-chinh-001.md` D3). Hội đồng có thể hỏi bộ dữ liệu có đòi hỏi đồ thị không. OB chưa tính R1 (thiếu thô trên EC2; đọc lại thô test cần quyền).
- Y9. **Cơ chế max-z kênh hẹp** lặp ở ba bộ (TT/OB 6/10 ca sai, T-054 `bao-cao.md` §7.5; RE3 2 ca, T-055 `dinh-chinh-001.md` Đ1b) nhưng cũng giúp root ở ca đúng (30/57 TT, 5/27 OB). Không được trình là nguyên nhân riêng của ca sai.
- Y10. **RQ3a không có.** Cô liệt kê Precision/Recall/F1. Q-245 hoãn chế độ (b). C-e cho thấy M1 trả CAUSE_FOUND ở 58/58 ca tại t−300 (`PT#/ce_tom_tat`). G4 phải khai M1 chưa có lớp phát hiện mức thành phần đã hiệu chuẩn.

**C. Mẫu hình, nhóm ca, trung gian đã lưu nhưng chưa khai thác**

- U1. `avg@5` và `hit@k` có sẵn ở `T#/rows/*/metrics` nhưng báo cáo không báo AC@k/Avg@5 để so với số công bố RCAEval (MRP P7, độ đo). Rẻ, chỉ đọc file.
- U2. Bảng dev↔test theo vế và theo thành phần (Y4). Rẻ, đọc D, A/T/PT, R.
- U3. Vùng E7 của các vế bỏ quan hệ (C-a0, bo-E5) chưa so với M1; mới có T12-on (T-054 `bao-cao.md` §8). Cần kiểm `T#/regions` có vế nào.
- U4. Ca sai của M1 ở ba bộ (TT 3, OB 7, RE3 4) nằm rải ở sáu file; chưa có một bảng chung theo cơ chế (kênh hẹp, IQR = 0, E5, root nguồn, E2 gán theo hướng).
- U5. Nhóm root là nút nguồn: OB frontend 6 ca, M1 0,708 so với M4 0,958 (T-054 `bao-cao.md` §6); C-d3 không thể đúng khi root trùng đích (`dinh-chinh-004.md` Đ13); RE3 nhóm lá M1 0,875 so với M4 0,986 (`K#/2_5_vi_tri_N`). Chưa gộp thành điều kiện "M1 yếu khi …".
- U6. TORAI B: trung gian TT auth loss chưa lần (T-054 `bao-cao.md` §11).
- U7. C-e TT: 16,4 thực thể tầng 1 mỗi ca ở t−300 (`PT#/ce_tom_tat`) chưa dùng cho câu về phát hiện/hiệu chuẩn.
- U8. R1 trên OB: không làm được nếu không đọc lại thô test OB (cần quyền).

**D. Phép so sánh còn thiếu**

- S1. Số baseline so với số công bố RCAEval (AC@k, Avg@5), để trả lời "baseline đủ mạnh" (QT7).
- S2. Dev ↔ test (Y4).
- S3. Bảng theo nhóm loại lỗi đặt cạnh nhau ở ba bộ (tài nguyên, mạng, mã nguồn), chỉ mô tả, không gộp thống kê (WHY-06).
- S4. R1 như "quy tắc đơn giản" thứ ba (sau C-d1, C-d2): chỉ mô tả sau xem test.
- S5. Đồ thị ngẫu nhiên: không làm theo M-25/WHY-07; G4 phải khai giới hạn này cho RQ3d.
- S6. Cạnh thông điệp/dữ liệu (DT18-NV2): trace dataset chỉ có cạnh gọi (T-040 §7); G4 phải nói phần này chỉ kiểm được ở FlashTicket.

### Đối chiếu đánh giá độc lập với SPEC (bước 2)

Đã đọc: SPEC (cả Phụ lục A), LOG phiên 1, `docs/review-prompt.md` (đủ 194 dòng, mục 1–20 và khối G4).

**Kiểm số và con trỏ của SPEC** (lệnh chỉ đọc, chạy trong phiên này):

| Chỗ trong SPEC | Kiểm | Kết quả |
|---|---|---|
| H3, số dev | Đọc `DEV#/worlds/P/<bộ>/summary/<vế>/MRR/phan_so` | Khớp: TT M1 167/180 ≈ 0,928, C-a0 59/60 ≈ 0,983; OB M1 48/55 ≈ 0,873, bo-E2 ≈ 0,721, bo-E1 = 48/55, bo-E5 ≈ 0,806, C-d2 ≈ 0,899 |
| H3, con trỏ | `summary/<vế>/metrics/rr` | **Sai con trỏ**: nút này không có. Đúng là `summary/<vế>/MRR/phan_so`. Không đổi số |
| H4 | `PT#/E5_tac_dung_M1` | Khớp: TT 273 thực thể tầng 2 ở 59/60 ca; OB 21 ở 14/34; 14.905 và 1.418 dòng giải thích |
| H2 | `results/T-043/bao-cao.md` §7 | Khớp: E1/E2/E5 nối G2-H03, H06, H17 và UV-1, UV-2 |
| H6 | `results/T-040/bao-cao-p5b.md:46`, `results/T-040/ban-giao-p6.md:19` | Khớp nội dung (kiểu cạnh; cạnh dữ liệu/thông điệp chỉ ở mô hình tĩnh) |
| H10 | Nguồn "SimpleRCA công bố top-1 0,80" | Số có ở `docs/LESSONS.md:10` (ST9, ST10), không ở MRP. SPEC ghi "(MRP chưa đối chiếu bản in)": **dẫn sai nơi**. Không đổi kết luận |
| Đầu vào | Mọi đường dẫn trong mục Đầu vào | Tồn tại. "manifest của T-052 và T-034" không ghi tên file; B0 sẽ ghi rõ file đã dùng |
| U3 khả thi | `tables.json#/regions` | Chỉ có vế M1 và T12-on (TT 60+60, OB 34+34). `result.json` của C-a0 không lưu vùng (khóa `extra` không có trường vùng) |

**Từng ý của bước 1 so với SPEC:**

| Ý bước 1 | SPEC | Mức | Ghi chú |
|---|---|---|---|
| G4-1 bảng kết quả ba bộ | Có, ngầm (ho-so-g4, báo cáo cho cô mục 5) | KHÔNG CHẶN | Sẽ đặt bảng chính ba bộ trong `ho-so-g4.md`; nằm trong đầu ra đã duyệt |
| G4-2…G4-6 | Có (Câu hỏi, Tiêu chí xong 1–6, Không làm) | — | — |
| Y1 thông điệp tổng | Có (dòng RQ3b) | — | — |
| Y2 lợi ích quan hệ có điều kiện | Có (RQ3d a, b; tiêu chí 3) | — | — |
| Y3 nghĩa hẹp, ba ví dụ của cô | Có một phần: H4 đo E5; không có dòng riêng cho PageRank/subgraph/GNN | KHÔNG CHẶN | Thông tin đã có (T-043 §7, WHY-10, C-g/E6b, E7). Đưa vào `ho-so-g4.md` và báo cáo cho cô mục 4, trong đầu ra đã duyệt; không cần phân tích mới |
| Y4 dev↔test | Có (H3) | — | — |
| Y5 sức phân xử | Có (H5) | — | — |
| Y6 lỗ baseline | Có (H10, H13, Q3 trong ho-so) | — | — |
| Y7 phân tích sau xem test | Có (C-15 B trong ho-so; Kiểm đúng đắn) | — | — |
| Y8 dữ liệu đơn giản | Có (RQ3d b, H5, H11) | — | — |
| Y9 max-z | Có (H8, tiêu chí 3) | — | — |
| Y10 RQ3a | Có (H7) | — | — |
| U1, S1 AC@k/Avg@5 | Có (H10) | — | — |
| U2, S2 | Có (H3) | — | — |
| U3 vùng của vế bỏ quan hệ | Không có | KHÔNG CHẶN | Đề xuất cho Minh ở dưới (Đ-1) |
| U4, S3 bảng ca sai/điều kiện ba bộ | Có (H9) | — | — |
| U5 root nút nguồn | Có một phần (H9) | — | Đưa vào H9 như một nhóm điều kiện |
| U6 TORAI B auth loss | Có (H16, giữ OPEN) | — | — |
| U7 C-e | Có (H7) | — | — |
| U8 R1 OB | Có (H11, chờ quyền) | — | — |
| S4 R1 làm quy tắc đơn giản | Có ngầm (H5, H9) | — | Ghi rõ "mô tả sau xem test" |
| S5 đồ thị ngẫu nhiên | Không có | KHÔNG CHẶN | Là giới hạn đã quyết (M-25, WHY-07), không là phân tích mới. Ghi vào ho-so phần giới hạn RQ3d |
| S6 cạnh thông điệp/dữ liệu | Có (H6) | — | — |

**Từng mục của SPEC:**

| Mục SPEC | Đánh giá | Mức | Bằng chứng; hậu quả; sửa tối thiểu |
|---|---|---|---|
| Mục tiêu, nguồn | Cần, đủ | — | Đủ MRP §3, §4, §7, §8, DT18, cô |
| Bảng câu hỏi | Cần | — | Mỗi dòng có giải thích khác và phần thiếu |
| H1–H10 (nhóm A) | Cần | — | Đều trả lời một câu G4 hoặc nguồn; chỉ đọc đầu ra đã lưu |
| H3 con trỏ | Sai con trỏ | KHÔNG CHẶN | Sửa `metrics/rr` → `MRR/phan_so`. Không đổi số hay kết luận |
| H10 dẫn nguồn | Dẫn sai nơi | KHÔNG CHẶN | Sửa "(MRP chưa đối chiếu bản in)" → "(`docs/LESSONS.md:10`, ST9–ST10; chưa đối chiếu bản in)" |
| H11 | Cần quyền | — | Đúng: chờ Minh, có đề xuất ở LOG phiên 1 |
| Nhóm C, D | Có lý do, hệ quả | — | Đạt mục 19 review-prompt |
| Phạm vi ghi | Đúng | — | Không chạm MRP/WHY/DECISIONS/LESSONS/src |
| Quyền dữ liệu | Đúng | — | Không đọc `data/locked`, không đọc thô test ngoài H11 |
| C-15 B | Đúng | — | "Trên test, không thử khóa xếp hạng…" |
| Tiêu chí xong 1–7 | Cần, đo được | — | Tiêu chí 3 khai trước cách đọc E2 (dev↔test cùng chiều) trước khi làm H3: đạt mục 16 |
| Chi phí, luật 19/21 | Hợp lý | — | Chỉ đọc; không lượt nào trên 1 giờ |
| Đầu vào "manifest T-052, T-034" | Chưa đủ cụ thể | KHÔNG CHẶN | B0 ghi tên file đã dùng vào LOG; không sửa SPEC |

**Rà theo mục 1–20 của `docs/review-prompt.md`** (chỉ ghi mục có điểm): mục 14 — câu "E5 không đổi" trong ho-so phải ghi rõ đại lượng (RR root/khối đầu, theo T-054 Đ6); mục 16 — tiêu chí 3 đã khai trước H3; mục 19 — các OPEN trong SPEC (H12, H13, H16, H17, H11) đã có lý do, giải thích khác, chi phí; mục 20 — các điểm chờ Minh ở LOG phiên 1 có đề xuất. Không thấy điểm chặn ở mục 1–13, 15, 17, 18.

**Đề xuất không chặn, trình Minh (không đưa vào SPEC):**

- Đ-1. **Vùng nghi ngờ của vế bỏ quan hệ (U3).** Tính lại vùng E7 cho C-a0 và bo-E5 từ `kenh_co` và `canh` đã lưu, so với M1 (tỷ lệ chứa root, cỡ vùng). Trả lời: quan hệ có đổi vùng nghi ngờ không (RQ3c mức mô tả, RQ3d cho vùng). Chi phí 1–2 giờ, chỉ đọc. Rủi ro C-15 B: mô tả, không đổi thiết kế. Mặt trái: phải tái lập đúng hàm E7 ngoài lõi (gọi `src/m1` chỉ đọc); kiểm bằng cách tính lại vùng M1 khớp `tables.json#/regions`. Đề xuất của Claude: làm nếu còn thời gian sau B9; không làm thì ghi OPEN với giải thích.

### Kết luận bước 3

**Không có điểm chặn — bắt đầu triển khai.**

Sửa nhỏ SPEC (được phép theo prompt của Minh: con trỏ/dẫn nguồn sai không đổi kết luận):

1. Phụ lục A, H3: "`DEV#/worlds/P/<bộ>/summary/<vế>/metrics/rr`" → "`DEV#/worlds/P/<bộ>/summary/<vế>/MRR/phan_so`". Lý do: con trỏ cũ không tồn tại.
2. Phụ lục A, H10: "(MRP chưa đối chiếu bản in)" → "(`docs/LESSONS.md:10`, ST9–ST10; chưa đối chiếu bản in)". Lý do: số nằm ở LESSONS, không ở MRP.

Không đổi phạm vi ghi, quyền dữ liệu, tiêu chí xong hay hướng khai thác. Đ-1 chờ Minh.

### Triển khai (bước 4)

- **B0 (09/11/2026).** `py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents` → `PASS false`, 515 mục, lệch duy nhất `docs/LESSONS.md` (lệch đã biết, DECISIONS mục "LESSONS không ghim trong manifest, 08/11/2026"). Script `results/T-057/scripts/b0_kiem_hash.py` → `results/T-057/b0-kiem-hash.json`: 16 manifest (T-034 manifest-cuoi-007; 7 manifest T-052; 6 manifest báo cáo T-054; T-055 manifest-002; T-056 manifest-003), bỏ tài liệu sống; 1062/1065 file khớp pin mới nhất. Ba file lệch: `src/m1/adapter.py`, `src/m1/chuoi.py` (pin ở `results/T-052/manifest.json`), `src/p3/nezha.py` (pin ở `results/T-052/manifest-dap-phan-bien-001.json`). Cả ba khớp `results/T-054/runs/chuan-bi-main-013-v2/code-pins.json` (pin của lượt test). Đây là bản cũ của T-052 bị thay bởi commit `601be1a1` (thêm RE3, metric Nezha source-native, tách C-d3). Không ảnh hưởng đầu ra T-057 (không chạy code). Ảnh hưởng H3: dev T-052 tính bằng code trước thay đổi; xem B3.
- **B3 (H3).** `results/T-057/scripts/h3_dev_test.py` → `results/T-057/dev-test.json`.
  - Kiểm cấu hình OB: RR root của M1 dev OB trong `results/T-052/ket-qua-dev.json` trùng RR tính lại từ `blocks` của 22 bản ghi M1 dev chạy bằng code khớp pin main013-v2 (`results/T-054/runs/sua-cd3-ob-001/nhan/ec2_*/ra/dev-*.json#/ban_ghi_cu`): **22/22** (`dev-test.json#/kiem_cau_hinh_OB`).
  - TT: không có bản ghi dev TT chạy bằng code khóa. `git diff dc01bc0d 601be1a1 -- src/m1/chuoi.py` chỉ thêm nhánh tùy chọn (`chi_so_hang_metric` cho metric source-native, `tach_cd3`); không đổi đường TT khi hai tham số vắng. Kết luận: dev TT so được ở mức "code thay đổi không chạm đường TT theo diff", chưa kiểm bằng chạy lại.
  - Chiều M1 − vế, dev so với test (`dev-test.json#/so_sanh_M1_tru_ve`): OB cùng chiều ở C-a0, C-a1, bo-E2, C-d1, C-d2; ngược chiều ở bo-E1 (dev 0, test +0,130) và bo-E5 (dev +0,067, test 0). TT ngược chiều ở C-a0 (dev −0,056, test 0), C-a1, bo-E2, bo-E5; cùng chiều ở bo-E1, C-d1, C-d2, C-g. Baseline cùng chiều cả hai bộ.
  - Lưu ý đọc: vế CIRCA, TORAI B trên OB là UNSUPPORTED (MRR ghi 0); không phải phép so.
- **B2 (H6).** `results/T-057/scripts/h6_do_thi.py` → `results/T-057/do-thi-dt18.json`. M1: TT 26 nút có cạnh, 55 cạnh hợp, 68 thực thể xếp hạng, mỗi ca 42–50 thực thể không có cạnh (gồm 26 thực thể tên DB/cache); OB 10 nút, 13 cạnh, mọi thực thể có cạnh; RE3 7 nút, 9 cạnh, 12 thực thể, 5 không cạnh. T12-on thêm nút tĩnh DB/broker (TT 84 nút, 181 cạnh; OB 19 nút, 22 cạnh); tên nút tĩnh DB (ví dụ `database-default:ts-auth-service:ts-auth-mysql`) khác tên thực thể DB đang xếp hạng (ví dụ `ts-auth-mongo`). `extra/canh` không có trường kiểu cạnh.
- **B4 (H4).** `results/T-057/scripts/h4_e5.py` → `results/T-057/e5-thanh-phan.json`. Tổng tầng 2 khớp `PT#/E5_tac_dung_M1` (TT 273, OB 21; ca có tầng 2 TT 59/60, OB 14/34). RE3: tầng 1 = 104, tầng 2 = 40 ở 21/30 ca. Root bị hạ xuống tầng 2: TT 0/60, OB 1/34 (`test-88dc4b2c47`), RE3 0/30. Ca RR root đổi khi bỏ E5: TT 1 (`test-e9dc7064cc`, M1 1,0 so với 0,5), OB 0, RE3 1 (`test-428cf2c868`, M1 0,25 so với 0,5). Root có kênh bị E5 giải thích (lệnh chỉ đọc trong phiên: đếm `PT#/trung_gian_theo_ca/*/M1/n_root_inherited` > 0 và `R#/trung_gian_M1_family/*/M1/root_inherited` khác rỗng): TT 28/60, OB 10/34, RE3 14/30. Sửa so với SPEC H4 ("root bị hạ … RE3 1/30"): ở `428c` root vẫn tầng 1; E5 làm mất F_I hai kênh mạnh nhất của root, không hạ tầng.
- **B5 (H8).** `results/T-057/scripts/h8_maxz_dev.py` → `results/T-057/maxz-dev.json`. Dev OB (22 ca, code khóa): 5 ca sai; 2/5 do đối thủ thắng bằng kênh hẹp (`dev-3b92690644`: op recommendationservice s 16,7 rộng 0,040, root mem s 12,8 rộng 0,8; `dev-63c30faf34`: cạnh frontend→adservice s 1289,9 rộng 0,054, root cạnh rộng 0,925 s 620,3). Ca đúng: root thắng bằng kênh hẹp 3/17; đối thủ hạng 2 có kênh mạnh nhất hẹp 5/17. Bản theo hướng và bản chỉ "len" như T-054 cho cùng số. Dev TT: KHÔNG ĐỦ DỮ LIỆU (không có độ rộng kênh trong bản ghi dev). Nguồn trước G3: `results/T-053/bao-cao.md:250` đã ghi "cực trị A và ca hại" là giả thuyết chưa xác nhận.
- **B9 (H10).** `results/T-057/scripts/h10_so_cong_bo.py` → `results/T-057/so-cong-bo.json`. Hit@1/3/5 (= AC@k), Avg@5, NDCG@5, MRR theo vế, world P, ba bộ. Tính lại khớp `PT#/bang_theo_ve_P` (TT 18 vế, OB 17 vế: 0 lệch) và `R#/bang_theo_ve_P` (RE3: 0 lệch trừ CIRCA; dòng `circa` trong `so-cong-bo.json#/bang/RE3-OB` gộp hai biến thể RHT+DA và RHT của file CIRCA bổ sung, (0,917 + 0,878)/2 ≈ 0,897; **không dùng dòng này**, dùng `R#/bang_theo_ve_P/circa`). Avg@5 M1: TT 0,990, OB 0,924, RE3 0,960. SimpleRCA trên đủ 90 ca RE2-TT (30 dev + 60 test): Hit@1 0,811; số công bố 0,80 (`docs/LESSONS.md:10`, chưa đối chiếu bản in, chưa biết cửa sổ/tập ca của bài). Đọc: cùng cỡ; chưa gọi là tái lập. Dòng TORAI B/CIRCA OB là UNSUPPORTED (0), không là điểm.
- **B6 (H5, H7).** `results/T-057/scripts/h5_h7_phan_xu.py` → `results/T-057/kha-nang-phan-xu.json`. Ô khác 0 của các phép so MRR (TT 20 ô, OB 20 ô, RE3 10 ô): ví dụ TT M1−TORAI B 6, M1−C-a0 3; OB M1−M4 14, M1−C-a0 12, M1−C-d2 3; RE3 M1−M4 4, M1−C-a0 2. Hit@5 của M1 = 1 ở 60/60, 34/34, 30/30 ca (trần). R1: root lệch bền nhất 48/60 TT, 28/30 RE3; OB chưa tính (H11). H7: C-e 58/58 CAUSE_FOUND, trung bình 16,4 thực thể tầng 1/ca, RR root tương lai 0,130 so với mức ngẫu nhiên 0,071.
- **B1 (H1).** `results/T-057/cau-hien-hanh.json` (28 mục, viết tay từ sáu file đính chính) và `results/T-057/cau-hien-hanh.md` (sinh bằng `py -3 -B results/T-057/scripts/b1_md.py`). Mỗi mục trỏ câu gốc, đính chính thay nó, câu hiện hành và trạng thái kiểm chéo. Codex chưa kiểm 9 mục (`#/dem/codex_chua_kiem`). Số trong các câu sẽ soát bằng máy ở B12.

**Kết thúc phiên 2 (checkpoint theo mốc SPEC "09–10/11: B0–B6, checkpoint LOG"):**

1. Đã làm gì: bước 1 (đánh giá độc lập), bước 2 (đối chiếu SPEC, kiểm số và con trỏ), bước 3 (không có điểm chặn), bước 4 tới B0, B1, B2, B3, B4, B5, B6, B9.
2. File đã thay đổi:
   - `tasks/T-057-ho-so-g4/SPEC.md`: hai sửa con trỏ/dẫn nguồn ở Phụ lục A (H3, H10), ghi ở mục "Kết luận bước 3".
   - `tasks/T-057-ho-so-g4/LOG.md`: mục phiên 2.
   - Mới trong `results/T-057/`: `b0-kiem-hash.json`, `dev-test.json`, `do-thi-dt18.json`, `e5-thanh-phan.json`, `maxz-dev.json`, `so-cong-bo.json`, `kha-nang-phan-xu.json`, `cau-hien-hanh.{json,md}`; `scripts/` gồm `b0_kiem_hash.py`, `h3_dev_test.py`, `h6_do_thi.py`, `h4_e5.py`, `h8_maxz_dev.py`, `h10_so_cong_bo.py`, `h5_h7_phan_xu.py`, `b1_md.py`.
   - Dòng T-057 trong `docs/STATE.md`.
3. Kiểm đã chạy: verify_manifest (lệch duy nhất LESSONS, đã biết); b0 1062/1065 khớp, 3 file src lệch pin cũ T-052 nhưng khớp code-pins main013-v2; H3 dev OB trùng code khóa 22/22; H4 khớp PT (273, 21); H10 tính lại khớp PT/R (0 lệch, trừ dòng CIRCA RE3 gộp hai biến thể — không dùng). Mọi script ghi file mới bằng chế độ "x" (không ghi đè).
4. Chưa chắc / cần Minh quyết (kèm đề xuất):
   - **Đ-1 (vùng của vế bỏ quan hệ).** Đề xuất: làm sau B9 nếu Minh duyệt; 1–2 giờ, chỉ đọc. Mặt trái: tái lập hàm E7 ngoài lõi, phải kiểm khớp vùng M1 trước. Phương án khác: ghi OPEN.
   - **H14 (chạy lại M1 dev TT đủ trung gian).** H8 cho thấy dev TT thiếu dữ liệu độ rộng. Đề xuất: không làm trong T-057; tách sang task chuẩn bị thiết kế FlashTicket như SPEC. G4-Q6 trả lời "OB dev: có (2/5 ca sai); TT dev: không đủ dữ liệu".
   - **H11** và các điểm chờ ở LOG phiên 1 (định dạng báo cáo, câu xin cô, E-MRP-1…3, sửa STATE ngoài dòng T-057) vẫn chờ.
   - Dev TT so được với test chỉ ở mức "diff không chạm đường TT"; chưa kiểm bằng chạy lại.
   - Prompt phản biện kết quả cho Codex chưa soạn: chưa có `ho-so-g4.md` để soát. Soạn ở B12.
5. Bước tiếp theo chính xác:
   - B7 (H2): đọc `results/T-034/ban-do-g2.json` và `results/T-034/goi-g2.md` §3; lập ma trận dòng G2 → thành phần M1 (E1/E2/E5, UV-1/UV-2) → kết quả theo ca từ `PT#/so_cap`, `R#/so_cap`, `results/T-057/dev-test.json`; ghi `results/T-057/truy-vet-han-che.json`.
   - B8 (H9): gộp ca sai M1 ở ba bộ (TT 3, OB 7, RE3 4) từ `PT#/doi_chieu_sai_dung`, `R#/trung_gian_M1_family`, `results/T-056/ket-qua-002.json`; nhóm điều kiện (kênh hẹp, IQR = 0, E5, root nút nguồn, loại lỗi); ghi `results/T-057/ban-do-dieu-kien.json`.
   - B10 `ho-so-g4.md`, B11 `bao-cao-tien-do-co.md`, B12 `soat-so.json`, `manifest.json`, prompt "Soát kết quả" + khối G4 cho Codex.
6. Lệnh cuối cùng đã chạy: `py -3 -B results/T-057/scripts/b1_md.py`.

## Phiên 2 (tiếp) — 09/11/2026 — Claude — Windows (laptop) — người làm

**Quyết định của Minh trong phiên:** "Duyệt Đ-1, làm tiếp" (chat 09/11/2026), trả lời câu "Duyệt Đ-1 (tính vùng nghi ngờ cho C-a0, bo-E5) trước khi tôi làm tiếp B7?". Phạm vi: Đ-1 như mô tả ở mục Kết luận bước 3; ghi trong `results/T-057/`. Chưa ghi DECISIONS.

- **Đ-1.** `results/T-057/scripts/d1_vung_ve.py` → `results/T-057/vung-ve-bo-quan-he.json`. Vế có E7 trong bản ghi (M1, bo-E1, bo-E2, bo-E5, T12-on) đọc `record.region`; C-a0, C-a1 (không có E7 theo `src/m1/chuoi.py:96`) dựng lại bằng `src/m1/e7.vung` trên `kenh_co`, `canh`, `inherited_by` của chính vế đó. Kiểm tái dựng trên 248 bản ghi M1/bo-E5 có E7: 248/248 khớp `region` đã lưu; M1, T12-on so `tables.json#/regions`: 0 lệch. Tóm tắt cách 1 (tỷ lệ chứa root kỳ vọng / cỡ kỳ vọng): TT M1 0,950/3,90, C-a0 0,950/5,03; OB M1 0,824/1,38, C-a0 0,735/2,29, bo-E2 0,706/1,47, bo-E1 0,765/2,21; RE3 M1 0,900/1,60, C-a0 0,900/1,73. Lưu ý đọc: vùng dựng quanh T = nhóm đầu của khối đầu, nên tỷ lệ chứa root đi theo độ đúng hạng 1; không là bằng chứng độc lập với xếp hạng.
- **B7 (H2).** `results/T-057/scripts/h2_truy_vet.py` → `results/T-057/truy-vet-han-che.json`. Ma trận 7 dòng G2 M1 nhắm hoặc liên quan (H03, H06, H17, H07, H09, H12, H16); 19 dòng còn lại ghi lý do không thuộc M1 (`#/khong_thuoc_M1`). Đo bằng máy ("sai" = root không đứng riêng khối đầu; "phía trên" theo `extra/canh` của chính vế): OB C-a0 sai 15, đối thủ là bên gọi trực tiếp của root 8; OB M1 sai 7, bên gọi trực tiếp 0. TT: C-a0 1/3, M1 0/3. RE3: C-a0 2/4 (1 trực tiếp, 1 gián tiếp), M1 1/4. Root trong tập trả về: 60/60, 34/34, 30/30. Lỗi return OB (3 ca): M1 0,75, C-a0 0,778, M4 0,712 — G2-H07 không có thành phần riêng trong M1.
- **B8 (H9).** `results/T-057/scripts/h9_ban_do.py` → `results/T-057/ban-do-dieu-kien.json` (lượt đầu dừng ở lỗi kiểu dữ liệu trước khi ghi file; sửa một dòng đọc `R#/tach/fault`, chạy lại). Ca sai M1: TT 3, OB 7, RE3 4. Nhãn cơ chế chép từ báo cáo/đính chính (không gán mới): kênh hẹp của đối thủ 8/14; cả hai kênh hẹp hoặc cả hai rộng 2; E5 2 (`88dc`, `428c`); root nút nguồn 2; IQR = 0 1; root chỉ có log 1 (một ca có thể nhiều nhãn). C-a0 đúng ở 3/14 ca M1 sai (TT `5e8f`, `7a22`; OB `3218`). R1 đặt root hạng 1 ở 6/7 ca M1 sai có R1 (TT+RE3). Đối thủ là bên gọi trực tiếp root: 1/14 (`cde8`). Bảng MRR theo loại lỗi và vị trí N chép ở `#/nhom`.
- **B10.** `results/T-057/ho-so-g4.md`: tóm tắt; sổ C-15 B; bảng chính ba bộ; trạng thái RQ3a–d; sáu câu G4 (câu 2 có số ô hữu hiệu từng phép so); ba nhận định chính kèm bảng giải thích khác (E2 OB: "mô tả, nhất quán"; TT/RE3: không phân xử được (a) dữ liệu đơn giản với (b) thành phần kém; max-z: đã hiện trên dev OB 2/5, dev TT không đủ dữ liệu); ma trận H2; đồ thị so DT18 và ba ví dụ của cô; Đ-1; dev↔test; RQ3a; bản đồ điều kiện; giới hạn độc lập; 9 câu mở theo review-prompt mục 19; ứng viên P10 "chưa kiểm"; 5 điểm chờ Minh kèm đề xuất (mục 20). Thêm một số tính trong phiên: MRR dev gộp 52 ca (M1 0,904; C-a0 0,847; C-d2 0,909) bằng lệnh Python chỉ đọc `DEV#/worlds/P/<bộ>/summary/<vế>/MRR/phan_so`, trọng số 30/22.
- **B11.** `results/T-057/bao-cao-tien-do-co.md`: 7 phần theo MRP §8, mỗi phần mở bằng "Phần này trả lời nhận xét…"; phần 1–3 tóm tắt (chi tiết ở báo cáo 21/10); có lý do không dùng Sock Shop, LEMMA-RCA (theo `results/T-021/goi-g1.md` §3.4) và Eadro (Q-83); khai P8 hoãn, RQ3a chưa có, phần sửa sau khi xem test; 4 câu xin cô định hướng. Chưa xuất `.docx` (chờ Minh chọn định dạng).
- **B12.** `results/T-057/scripts/b12_soat_so.py` → `results/T-057/soat-so.json`: 140 số trong hai tài liệu đối chiếu file nguồn bằng con trỏ, **0 lệch**. Lượt thử ở scratchpad lộ 5 lỗi con trỏ của chính script (A4 lưu phân số; C-d2 RE3 nằm ở R, không ở `so-cong-bo.json`; RE3 viết giá trị tuyệt đối trong báo cáo cho cô), đã sửa script trước lượt chính. Giới hạn: soát sự có mặt của chuỗi số, không chứng minh số nằm đúng câu. Các số đếm viết tay (8 → 0, 2/124, 14 ca, 1 → 0, 2 → 1, 658/658) đối chiếu tay với `truy-vet-han-che.json#/dem`, `e5-thanh-phan.json`, T-054 §1. `results/T-057/manifest.json` (`scripts/manifest.py`): 28 file, gồm SPEC; ghi trước khi kiểm bản nhận RE3, nên thay bằng `results/T-057/manifest-002.json` (thêm `b0-re3-nhan.json`, `b0-re3-nhan-002.json` và hai script).
- **Tự kiểm.**
  - Không đọc `data/locked/`, không đọc lại dữ liệu thô test, không chạy phương pháp. Bản nhận RE3 ngoài repo (`D:/RCA-ext/T-055/...`): kiểm theo `results/T-055/runs/cham-001/main-receipt.json`. Lượt 001 (`scripts/b0_re3_nhan.py` → `b0-re3-nhan.json`) báo 420/420 slot lệch: lỗi của phép kiểm (so `job.json` theo byte, trong khi `job_sha256` là vân tay JSON chuẩn hóa, `results/T-054/scripts/bien_nhan.py:74-75`). Giữ file lượt 001, không dùng. Lượt 002 (`scripts/b0_re3_nhan_002.py` → `b0-re3-nhan-002.json`): hai archive, snapshot, aggregate-plan khớp; 420/420 slot khớp (verified.json theo snapshot, result.json, vân tay job). Số dùng từ bản nhận khớp R ở phần trùng: vùng M1 RE3 0,900/1,60 khớp `K#/2_5_vung`.
  - Câu "E5 không đổi" trong hồ sơ ghi rõ đại lượng (RR root).
  - Tiêu chí 3 (E2 OB) đọc đúng mức đã khai trước khi làm H3.
- Tiêu chí xong 1–6: đạt theo tự kiểm, chờ phản biện. Tiêu chí 7 (Codex phản biện, bảng phản hồi) chưa.

**Kết thúc phiên 2 (tiếp):**

1. Đã làm gì: Đ-1, B7, B8, B10, B11, B12 (soát số, manifest).
2. File đã thay đổi: `tasks/T-057-ho-so-g4/LOG.md` (mục này); dòng T-057 trong `docs/STATE.md`; mới trong `results/T-057/`: `vung-ve-bo-quan-he.json`, `truy-vet-han-che.json`, `ban-do-dieu-kien.json`, `ho-so-g4.md`, `bao-cao-tien-do-co.md`, `soat-so.json`, `manifest.json`, `manifest-002.json`, `b0-re3-nhan.json` (lượt lỗi phép kiểm, giữ), `b0-re3-nhan-002.json`; scripts `d1_vung_ve.py`, `h2_truy_vet.py`, `h9_ban_do.py`, `b12_soat_so.py`, `manifest.py`, `b0_re3_nhan.py`, `b0_re3_nhan_002.py`.
3. Kiểm đã chạy: Đ-1 tái dựng 248/248, 0 lệch với `tables.json#/regions`; soát số 140/0 lệch; H2 "phía trên root" đếm trên `extra/canh` của chính vế.
4. Chưa chắc / cần Minh quyết (đề xuất ở `ho-so-g4.md` §14):
   - Duyệt G4 sau phản biện. Đề xuất: duyệt với kết luận "không hơn rõ baseline; quan hệ giúp có điều kiện (OB, E1/E2)".
   - H11: đề xuất cấp. H14: đề xuất tách sang task chuẩn bị thiết kế FlashTicket.
   - Câu xin cô (4 câu ở báo cáo §7) và định dạng `.docx`.
   - E-MRP-1…3 và sửa STATE ngoài dòng T-057 (từ phiên 1) vẫn chờ.
5. Bước tiếp theo chính xác: Minh chuyển prompt dưới cho Codex (soát kết quả, G4). Sau phản biện: người làm tự soát lại `ho-so-g4.md` trước khi đọc kết luận phản biện, rồi điền bảng phản hồi.
6. Lệnh cuối cùng đã chạy: `py -3 -B results/T-057/scripts/manifest.py results/T-057/manifest-002.json`.

---

## Prompt bàn giao cho agent đối phương (soát kết quả, G4)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-057 — Hồ sơ G4 và báo cáo tiến độ cho cô; tasks/T-057-ho-so-g4/SPEC.md, tasks/T-057-ho-so-g4/LOG.md (phiên 1, phiên 2 và phiên 2 tiếp).
- Công đoạn: soát kết quả.
- Gói/cổng: P7 (tổng hợp, phân tích), cổng G4.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện.
- Tài liệu gốc: docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/STATE.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/review-prompt.md. Commit gốc b91232eb; thay đổi chưa commit: docs/DECISIONS.md, docs/LESSONS.md, docs/STATE.md, tasks/T-054-khoa-g3-chay-p7-a/LOG.md; chưa theo dõi trong git: results/T-055/, results/T-056/, results/T-057/, tasks/T-055-re3-ban-cuoi/, tasks/T-056-phan-tich-bo-sung/, tasks/T-057-ho-so-g4/.
- Phản biện và phản hồi trước: không có cho T-057.
- Code và kết quả liên quan: results/T-057/ (ho-so-g4.md, bao-cao-tien-do-co.md, cau-hien-hanh.json, cau-hien-hanh.md, b0-kiem-hash.json, dev-test.json, do-thi-dt18.json, e5-thanh-phan.json, maxz-dev.json, kha-nang-phan-xu.json, so-cong-bo.json, vung-ve-bo-quan-he.json, truy-vet-han-che.json, ban-do-dieu-kien.json, soat-so.json, b0-re3-nhan-002.json, scripts/, manifest-002.json); nguồn đầu vào: results/T-054/reports/main-013-v2/{a4,tables}.json, results/T-054/reports/p7a-013-v2/ (bao-cao.md, dinh-chinh-001.md … dinh-chinh-004.md, phan-tich-nhom.json), results/T-054/runs/sua-cd3-ob-001/nhan/, results/T-055/reports/re3/ (bao-cao-re3.md, dinh-chinh-001.md, phan-tich-re3.json), results/T-054/reports/re3-ban-cuoi-001/, results/T-054/reports/re3-ban-cuoi-001-circa/, results/T-056/ (bao-cao.md, dinh-chinh-001.md, ket-qua.json, ket-qua-002.json), results/T-052/ket-qua-dev.json, results/T-034/goi-g2.md, results/T-043/bao-cao.md, results/T-040/ban-giao-p6.md, results/T-021/goi-g1.md; bản nhận RE3 ngoài repo D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/. Mọi script T-057 chạy từ gốc repo bằng py -3 -B, lệnh ghi trong docstring và trường "lenh" của từng file kết quả; script ghi file mới bằng chế độ "x". Kiểm manifest: py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents; sha256 đầu ra T-057 ở results/T-057/manifest-002.json.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cho phép ghi tasks/T-057-ho-so-g4/REVIEW.md theo tasks/_MAU/REVIEW.md.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```


## Phiên 3 — 09/11/2026 — Claude — Windows (laptop) — người làm (đáp phản biện G4 lượt 1, ghi gói sửa)

**Quyết định của Minh trong phiên** (chat 09/11/2026, dán kèm lượt kiểm phản hồi của Codex): "nếu không có mâu thuẫn nào với codex hoặc phản đối nào thì cho phép ghi luôn, nếu có mâu thuẫn thì soạn trình claude phản biện, rà soát các phần khác xem còn lỗ hổng nào không, tuyệt đối không coi là đã đúng mà cần kiểm chính xác". Claude không phản đối điểm nào của Codex, nên ghi gói sửa mục C (phản hồi lượt 1) cùng hai bổ sung của Codex. Chưa ghi DECISIONS.

**Phản biện G4 lượt 1 (Codex, chat, tóm tắt; nguyên văn do Minh giữ trong chat).** R1 CHẶN: câu "quan hệ không còn chỗ thêm thông tin" (TT 2/56/2, RE3 1/28/1). R2 CHẶN: bỏ sót native T-053 cho dev TT (30/30 ca có độ rộng kênh; 3/4 ca sai thỏa điều kiện H8). R3 CHẶN: dòng G2-H17 dùng "đối thủ đứng đầu" thay cờ M5 gốc (OB 10 → 0, RE3 3 → 2); nhóm "8 ca" gồm 7 network_delay + 1 cpu_contention. R4 CHẶN: mô tả E7 trong báo cáo cho cô là cách 2, số là cách 1. Lượt kiểm phản hồi (Codex): đồng ý R1–R4, N1, N2 (dòng CIRCA RE3 n = 60, gộp hai biến thể); thêm: (a) soát số bản mới phải dùng script mới trỏ đúng tài liệu `-002`, kiểm theo dòng; (b) khai file kiểm ở scratchpad.

**Phản hồi của người làm** (kiểm trên file, lệnh chỉ đọc; script `C:/Users/84583/AppData/Local/Temp/claude/5310c26210b3e696/287ea605-ee38-4d82-b9f4-cc60c10b348f/scratchpad/kiem_r2_r3.py`):

| Điểm | Kết luận | Bằng chứng riêng |
|---|---|---|
| R1 | Đúng | `PT#/so_cap/RE2-TT|M1-C-a0|RR` 2/56/2; `R#/so_cap/M1-C-a0|rr` 1/28/1; 4 ca TT có cơ chế ở T-054 §7.2 (E1 giúp 327a, E5 giúp e9dc; E1 hại 7a22, 5e8f) |
| R2 | Đúng | Seal `results/T-053/runs/k-dong-pha1-001/seal.json#/that` khớp hash; 30/30 ca TT `K-E1+E2+E5` có `don_vi_phan_vi`; RR khớp T-052 30/30; 4 sai, 3 thỏa điều kiện H8; 10/26 ca đúng root thắng bằng kênh hẹp |
| R3 | Đúng | `co_M5` trên 248 bản ghi: TT 1 → 0, OB 10 → 0, RE3 3 → 2; 8 ca = 7 network_delay + `f92f` cpu_contention |
| R4 | Đúng | `src/m1/e7.py:41` (cách 2 = liên thông); số báo là cách 1 |
| N1 (tự tìm) | KHÔNG CHẶN | Hồ sơ §1 thiếu con trỏ kiểm bản nhận RE3 |
| N2 (tự tìm) | KHÔNG CHẶN | `so-cong-bo.json#/bang/RE3-OB/circa` gộp hai biến thể |
| Codex (a) | Đúng | `b12_soat_so.py` ghi cứng tài liệu cũ |
| Codex (b) | Đúng | Tạo `kiem_r2_r3.py` ở scratchpad trong lượt "chỉ trả lời trong chat" là ghi file ngoài phạm vi (Luật 0 mục 1, áp cả ngoài repo). Khai ở đây; giữ file làm bằng chứng. |

**Rà soát thêm theo yêu cầu Minh (kiểm trên file, trước khi sửa):**

- **N3 — CHẶN câu trả lời G4-Q6.** Hồ sơ §4 câu 6 ghi "cấu hình được chọn theo MRR dev gộp hai bộ". Sai: gói E1+E2+E5 do bộ chọn khối K của T-053 trả theo luật khai trước (`results/T-053/bao-cao.md:11`, `:143`, `:147`); Minh chốt nền và chấp nhận cờ TRÁI CHIỀU của E2 (Q-237, Q-239, Q-242). Bootstrap: gói thắng chỉ thắng 249/1000 mẫu, "không có bằng chứng lựa chọn ổn định duy nhất trên dev" (`results/T-053/bao-cao.md:162`). Số MRR dev gộp (M1 0,904, C-a0 0,847, C-d2 0,909) đúng nhưng chỉ là mô tả.
- **N4 — CHẶN câu cơ chế trong báo cáo cho cô §5.2 và hồ sơ §10.** "E2 không gán được bằng chứng cho nút không có bên gọi" đưa ra như nguyên nhân M1 yếu ở root frontend. Ở T-054, câu này nằm trong mục "Câu hỏi mở" (`results/T-054/reports/p7a-013-v2/bao-cao.md:306`). Sự kiện theo code đúng (E2-C gán cho bên nhận; frontend không có bên gọi trong `canh`, `dinh-chinh-004.md` Đ13), nhưng việc nó gây MRR thấp chưa kiểm.
- **N5 — KHÔNG CHẶN.** Báo cáo cho cô §5.2: "lỗi hiện ở bên gọi, không ở chính root". Sai với log: root có log lỗi tăng ở 18/30 ca RE3 (`K#/2_2_log_loi_RE3/tom_tat/root_has_logerr_increase`); chỉ đứng đầu theo log lỗi 4/30. Status span: 0/18 ca có trace của root (C26).
- **N6 — KHÔNG CHẶN.** Hồ sơ §0: "cơ chế đủ chuỗi … cho E1 ở lỗi CPU". Quá mức: E1 OB chỉ có quan sát trung gian ở 2 ca (T-054 §7.4), phần E1 giảm còn +0,079 khi bỏ ca D1 (C02).
- **N7 — KHÔNG CHẶN.** Hồ sơ §8 "cùng chiều … mọi baseline trên cả hai bộ": trên OB, CIRCA và TORAI B không hỗ trợ. Sửa thành "mọi baseline chạy được".
- **N8 — KHÔNG CHẶN.** Báo cáo cho cô §5.4 liệt kê ba chỗ sửa sau khi xem test, thiếu: quy tắc v1 → v2 (sửa sau khi mở test, trước khi xem điểm; 740/740 slot trùng) và lệch số worker RE3 chưa khai. Hồ sơ §1 có đủ.
- **N9 — KHÔNG CHẶN.** Báo cáo cho cô §5.3 "cỡ vùng 1,4–3,9 dịch vụ": thực thể gồm cả DB/cache (TT). Sửa "thực thể".

**Gói sửa ghi trong lượt này** (bản đã ghim giữ nguyên):
1. `results/T-057/scripts/h8b_maxz_dev_tt.py` → `results/T-057/maxz-dev-002.json` (R2).
2. `results/T-057/scripts/h2b_m5.py` → `results/T-057/truy-vet-han-che-002.json` (R3: giữ phép đếm "đối thủ đứng đầu", thêm M5 gốc, tách trực tiếp/gián tiếp, theo loại lỗi).
3. `results/T-057/dinh-chinh-001.md` cho `ho-so-g4.md` (R1, R2, R3, N1, N2, N3, N4, N6, N7).
4. `results/T-057/bao-cao-tien-do-co-002.md` (R1, R3, R4, N4, N5, N8, N9; R2 phần dev).
5. `results/T-057/scripts/b12b_soat_so.py` → `results/T-057/soat-so-002.json`, kiểm theo dòng có nhãn neo.
6. `results/T-057/manifest-003.json`; LOG; dòng T-057 STATE.

**Thực hiện gói sửa (phiên 3):**

- `h8b_maxz_dev_tt.py` → `results/T-057/maxz-dev-002.json`: hash seal T-053 khớp; 30/30 ca TT có độ rộng kênh; RR khớp T-052 30/30; 4 ca sai, 3 thỏa điều kiện H8 (`dev-14372e1209`, `dev-20acb4402d`, `dev-a915aa2424`); 10/26 ca đúng root thắng bằng kênh hẹp. Khớp số Codex.
- `h2b_m5.py` → `results/T-057/truy-vet-han-che-002.json`: 248 bản ghi. M5 gốc: TT C-a0 1 (`e9dc`, cpu) → M1 0; OB C-a0 10 (network_delay 8, cpu_consumed 1, cpu_contention 1; cả 10 có bên gọi trực tiếp) → M1 0; RE3 C-a0 3 (2 trực tiếp, 1 chỉ gián tiếp) → M1 2 (`428c`, `cde8`). Đại lượng A theo loại lỗi: OB C-a0 7 network_delay + 1 cpu_contention.
- `results/T-057/dinh-chinh-001.md`: Đ1–Đ10 cho `ho-so-g4.md` (R1, R2, R3, N1–N4, N6, N7). `ho-so-g4.md` giữ nguyên.
- `results/T-057/bao-cao-tien-do-co-002.md`: chép từ bản cũ rồi thay đúng 11 đoạn (mỗi đoạn kiểm xuất hiện đúng 1 lần trước khi thay): ngày/trạng thái; E7 mô tả cách 1 (R4); tiêu đề và câu M5/nhóm 8 ca (R3); "Không thấy lợi ích ròng" kèm T/H/T (R1); câu "chưa phân biệt được" thay câu "không còn chỗ" (R1); nút nguồn "chưa kiểm" (N4); lỗi mã nguồn theo log 18/30, 4/30 và status 0/18 (N5); max-z thêm dev 3/4, 2/5 (R2); "thực thể" (N9); danh sách sửa sau khi mở test thêm v1→v2 và lệch worker (N8). Bản cũ giữ nguyên.
- `b12b_soat_so.py` → `results/T-057/soat-so-002.json`: soát theo dòng neo, 88 mục, **0 lệch**. Trước lượt chính, thử đột biến trong bộ nhớ: bản đầu chỉ bắt 5/7 đột biến (số nguyên nhỏ trùng chữ số khác trên dòng: "0/18", mã ca); sửa thành khớp số tách biệt + mẫu câu cho số đếm nhỏ; bản sửa bắt 7/7. Lượt thử đầu của bản sửa lộ 1 mẫu câu viết sai (`dc_A_OB_nd`), đã sửa mẫu. Tệp thử ở scratchpad, không ghi trong repo.
- `results/T-057/manifest-003.json`: 40 file; mọi file đã ghim ở `manifest-002.json` không đổi hash.

**Kết thúc phiên 3:**

1. Đã làm gì: kiểm lại R1–R4 và hai bổ sung của Codex; rà thêm hồ sơ và báo cáo, tìm N3–N9; ghi gói sửa.
2. File đã thay đổi: `tasks/T-057-ho-so-g4/LOG.md`; dòng T-057 trong `docs/STATE.md`; mới trong `results/T-057/`: `maxz-dev-002.json`, `truy-vet-han-che-002.json`, `dinh-chinh-001.md`, `bao-cao-tien-do-co-002.md`, `soat-so-002.json`, `manifest-003.json`; scripts `h8b_maxz_dev_tt.py`, `h2b_m5.py`, `b12b_soat_so.py`. Ngoài repo (scratchpad, khai theo Luật 0): `kiem_r2_r3.py` (phiên trước, lượt chỉ trả lời chat), tệp thử soát số.
3. Kiểm đã chạy: như mục "Thực hiện gói sửa"; số mới khớp các số Codex tự kiểm (3/4, 10/26, M5 10 → 0, 3 → 2, n = 60 của dòng CIRCA).
4. Chưa chắc / cần Minh quyết:
   - Soát số kiểm số đúng dòng, không kiểm ý nghĩa câu; phần ý nghĩa cần Codex kiểm lại.
   - N3 đổi câu trả lời G4-Q6: lựa chọn M1 trên dev không ổn định (249/1000 mẫu). Đề xuất: giữ như một giới hạn khai trong G4, không mở lại T-053.
   - Đề xuất cho Minh: gửi Codex kiểm phần sửa (prompt dưới); nếu không còn phản đối, Minh quyết G4. H14 bỏ; H11 giữ OPEN; câu xin cô và `.docx` sau khi chốt nội dung.
5. Bước tiếp theo chính xác: Minh chuyển prompt dưới cho Codex.
6. Lệnh cuối cùng đã chạy: `py -3 -B results/T-057/scripts/manifest.py results/T-057/manifest-003.json`.

---

## Prompt bàn giao cho agent đối phương (kiểm lại phản hồi và sửa, G4)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-057 — Hồ sơ G4 và báo cáo tiến độ cho cô; tasks/T-057-ho-so-g4/SPEC.md, tasks/T-057-ho-so-g4/LOG.md (phiên 3).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P7, cổng G4.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện.
- Tài liệu gốc: docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/STATE.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/review-prompt.md. Commit gốc b91232eb; đọc git diff và trạng thái hiện tại.
- Phản biện và phản hồi trước: phản biện G4 lượt 1 của Codex, phản hồi của Claude, lượt kiểm phản hồi của Codex (chat 09/11/2026, Minh giữ nguyên văn); tóm tắt và bảng phản hồi ở LOG phiên 3.
- Code và kết quả liên quan: results/T-057/ (bản đã ghim trước: ho-so-g4.md, bao-cao-tien-do-co.md, soat-so.json, manifest.json, manifest-002.json; bản mới: dinh-chinh-001.md, bao-cao-tien-do-co-002.md, maxz-dev-002.json, truy-vet-han-che-002.json, soat-so-002.json, manifest-003.json; scripts/h8b_maxz_dev_tt.py, scripts/h2b_m5.py, scripts/b12b_soat_so.py); results/T-053/runs/k-dong-pha1-001/seal.json; results/T-053/bao-cao.md; results/T-052/ket-qua-dev.json; src/m1/e7.py; src/m1_danh_gia/m5.py; nguồn T-054, T-055, T-056 dẫn trong SPEC; bản nhận RE3 D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/. Script chạy từ gốc repo bằng py -3 -B; lệnh ghi trong docstring và trường "lenh" của file kết quả.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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


## Phiên 3 (tiếp) — 09/11/2026 — Claude — người làm — Minh duyệt G4

- Codex kiểm bản sửa (chat 09/11/2026, Minh chuyển): R1–R4, N1–N9 và hai bổ sung đã xử lý; không có lỗi đáng kể mới; manifest-003 khớp 40/40, manifest-002 khớp 32/32; tính lại ba script mới cho JSON trùng bản lưu; đề xuất dừng phản biện. Claude đồng ý, không còn bất đồng.
- **Quyết định của Minh trong phiên:** "duyệt" (chat 09/11/2026), trả lời câu "Minh có duyệt G4 với các giới hạn này không?". Phạm vi: G4 trong phạm vi P7(a) với kết luận "M1 không hơn rõ baseline mạnh ở bộ nào; dùng quan hệ chỉ giúp có điều kiện (Nezha-OB, nhờ E1/E2)", theo `results/T-057/ho-so-g4.md` cùng `results/T-057/dinh-chinh-001.md`. Giữ OPEN: RQ3a, nhãn vùng, tương tác E1/E2/E5, nguồn vật lý kênh cực trị, H11. H14 bỏ. Dừng phản biện. Chưa ghi DECISIONS (chờ Minh duyệt dòng ghi).
- Duyệt G4 không đóng T-057: còn chốt câu xin cô, xuất `.docx` từ `bao-cao-tien-do-co-002.md`, và Minh nghiệm thu task.
- Bước tiếp theo: Minh duyệt dòng DECISIONS và nội dung commit (đề xuất trong chat); chốt câu xin cô và định dạng gửi.

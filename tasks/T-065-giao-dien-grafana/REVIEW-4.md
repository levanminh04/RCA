# Phản biện T-065 — lượt 4 (kiểm lại sửa S1: L10 và ảnh Minh chụp)

- **Người phản biện:** Claude (Opus 5.5) — **Ngày:** 15/11/2026 — **Commit/diff đã đọc:** nhánh `claude/sweet-hawking-dy078d` trên `c3d27f8a`. Đầu ra T-065 chưa commit, ghim bởi `results/T-065/manifest.json` (`utc` 2026-11-15T03:47:52.521Z, `status` `s1_trien_khai_api_dat_anh_chua_lam_L10`).
- **Công đoạn/cổng và bản lượt:** kiểm lại phản hồi và sửa; chiến dịch M1-FlashTicket, nhánh giao diện sau G4. Quyền ghi đúng file này do phiên điều phối chuyển, theo lời Minh "triển khai phần còn lại giúp tôi" (15/11/2026). Giữ REVIEW, REVIEW-2, REVIEW-3.
- **Đã đọc:** `results/T-065/prompt-ban-giao.md`; LOG mục L9–L10; `kiem/008-s1/` (BAO-CAO, HOAN-TAC, hash-truoc-sau, doi-chieu, kiem-cuoi, `ban-truoc/`); `grafana-l10/t065-l5-muc-luc.json`; `kiem/009-s1-anh-minh/` (4 ảnh, SHA256SUMS, GHI-CHU); bảng phản hồi cuối `REVIEW-3.md`; `results/T-064/ban-xuat/chi-muc-ban.json` (bản 3) và `chi-muc-ban-2.json`; WHY-99.
- **Tự soát độc lập:** chỉ đọc file đã lưu và xem 4 ảnh. Không gửi truy vấn tới `exp-obs`, không động Chrome.

## Kết luận chung

**S1 đạt.**
- Mục lục mới chỉ đổi nội dung panel văn bản. Nó trỏ hai UID `t065-l8b-*` là hiện hành và ghi V082 là đề xuất cuối, V071 là bản thay thế.
- Hai dashboard L4 nằm trong `9 · Lưu trữ/L4 · Bộ bản tạm · 14-11`, giữ nguyên byte và UID.
- Ảnh Minh chụp khớp file nguồn và biên nhận API.
- Không còn điểm CHẶN. Có ba điểm KHÔNG CHẶN. Hai trong số đó liên quan tới lượt xuất lại slot ebd5ef38 theo chỉ mục T-064 bản 3, việc này nằm ngoài S1.

## Các điểm

### T1. Mục lục trỏ "Nguồn bản và ca" tới chỉ mục bản 3, trong khi dashboard dựng từ bản 2 — KHÔNG CHẶN

- **Ở đâu:** `grafana-l10/t065-l5-muc-luc.json` dòng cuối của panel: "Nguồn bản và ca: results/T-064/ban-xuat/chi-muc-ban.json"; ảnh `01-muc-luc.png`.
- **Sai gì:** khi L10 viết câu này, file đó vẫn là bản 2. Nay T-064 đã lên bản 3: file cùng tên đã là bản 3, còn bản 2 chuyển sang `chi-muc-ban-2.json`. `nguon-l8b/chi-muc-ban.json` (nguồn dựng L8b) có SHA `7e4278d6…`, bằng `chi-muc-ban-2.json`. Trang ca L8b vẫn ghi đúng "Trang này dùng chỉ mục bản 2" (ảnh 02, 03).
- **Hậu quả:** người lần nguồn từ Mục lục sẽ mở bản 3 và thấy hai slot ebd5ef38 khác với dashboard.
- **Đề xuất sửa:** sửa câu nguồn trong lượt xuất lại ebd5ef38. Ghi đúng bản chỉ mục đang hiển thị: hoặc trỏ `chi-muc-ban-2.json` nếu chưa xuất lại, hoặc bản 3 sau khi xuất lại.

### T2. Lượt xuất lại ebd5ef38: "hạng và cờ không đổi" chỉ đúng với thứ tự hạng — KHÔNG CHẶN (thông tin cho lượt sau)

- **Ở đâu:** thông tin điều phối chuyển kèm lượt này; chỉ mục T-064 bản 3 (`sua`: "slot ebd5ef38 V082/V071 theo R9 (WHY-99)").
- **Quan sát (lệnh Python chỉ đọc, so đầu ra bản 2 với bản 3 của slot ebd5ef38):**
  - Thứ tự `entity_ranking` và `tie_group` trùng nhau ở cả V082 và V071.
  - `extra/kenh_co`: 65 → 64 ở cả hai bản. Kênh mất là `payment-service|metric|payment-service_live-down|live-down|len`.
  - Khóa điểm của payment-service đổi từ `[3.0, 0.0, …]` (nhánh H5b "chết im") sang `[2, 4511.15…, …]`.
  - Đúng như WHY-99 dự kiến: chết im mất ở ebd5ef38.
  - Dữ liệu L8b hiện hiển thị 65 cờ (`may-l8b/du-lieu/V082-V066+H8a/ebd5ef38.json#/co_m1`).
- **Hậu quả:** nếu lượt xuất lại chỉ kiểm thứ tự hạng, bảng cờ và lời diễn giải H5b của ca này có thể lệch nguồn mà không ai thấy.
- **Đề xuất:** lượt xuất lại đối chiếu đủ thứ tự hạng, khóa, bảng cờ (64) và mọi chữ trên dashboard có nhắc H5b hay chết im của ca này. Hai hash cấp bản không đổi (bản 3 chỉ đổi `dau_ra` và `sha256` của hai slot). Đây là việc của T-064 và điều phối, không thuộc S1.

### T3. Chưa có bằng chứng bấm hai liên kết từ Mục lục — KHÔNG CHẶN

- **Ở đâu:** `kiem/008-s1/kiem-cuoi.json#/ui_click_from_toc` = false; ảnh 02, 03 có URL đầy đủ tham số (`from`/`to` ISO, `var-…`), tức là mở trực tiếp, không bấm từ Mục lục.
- **Xét:** liên kết là markdown tĩnh `/d/t065-l8b-rca` và `/d/t065-l8b-phat-lai`. API xác nhận cả hai đích tồn tại và trả 200 (`doi-chieu.json#/checks/toc_has_both_l8b_links`, `all_five_uid_get_200`). Ảnh 02, 03 cho thấy hai UID ấy hiển thị đúng. Rủi ro rất thấp.
- **Đề xuất:** chấp nhận giới hạn, ghi một dòng trong báo cáo. Không cần lượt riêng.

## Kiểm sửa S1

- **Nguồn:** so cấu trúc `kiem/008-s1/ban-truoc/t065-l5-muc-luc.json` với `grafana-l10/t065-l5-muc-luc.json`: chỉ khác `/panels/0/options/content`. SHA bản mới `c5170208…` bằng `hash-truoc-sau.json#/targets/t065-l5-muc-luc.json/after/sha256`. Bản trước trùng byte với `grafana-l5/t065-l5-muc-luc.json`.
- **Nội dung:**
  - "28 ca × 3 bản (9 T-062 + 13 dev2 + 6 dev3)" khớp chỉ mục (3 × 28).
  - "19 ca dev chỉ hiện giới hạn" = 13 + 6.
  - V082 "đề xuất cuối Minh chọn ngày 14/11/2026" khớp DECISIONS.
  - Có câu "không thay nghiệm thu T-064/T-065".
  - Không có đáp án.
- **Hai L4:** byte `ban-truoc/t065-l4-*.json` trùng `grafana-l4/t065-l4-*.json`. Hash trước bằng hash sau, đường dẫn mới nằm trong `9 · Lưu trữ/L4 · Bộ bản tạm · 14-11/` (`hash-truoc-sau.json#/targets`).
- **Máy:** `kiem-cuoi.json#/checks`: only_three_authorized_dashboard_changes, no_restart, api_folder_hierarchy, only_l8b_in_current, both_l4_in_archive đều đúng.
- **Ảnh Minh chụp:** `sha256sum -c SHA256SUMS` đạt cả 4 ảnh. Tôi xem trực tiếp từng ảnh.
  - Ảnh 01: breadcrumb `0 · Bắt đầu tại đây › Mục lục RCA`; chữ trên ảnh khớp `panels[0].options.content` của nguồn L10.
  - Ảnh 02: `t065-l8b-rca` trong `1 · Kết quả hiện hành`, bản V082 `de_xuat`, ca 86dea661, hash cấu hình `451a8437…`, hash file `01a64b60…`, hash mã nguồn `b0f79a4d…`, hash đầu ra `fef04529…`. Các hash khớp đầu ra tôi kiểm ở lượt 3.
  - Ảnh 04: cây folder đúng, L4 nằm trong Lưu trữ.
  - Giới hạn: giờ chụp chỉ suy từ giờ file tới máy (GHI-CHU tự nêu).
- **Hoàn tác:** `HOAN-TAC.md` có lệnh kèm guard pin, chưa chạy. Lệnh hoàn tác Mục lục về byte trước và chuyển hai L4 về chỗ cũ, không ghi đè. Đủ.

## Đối chiếu các lượt trước

- **S1 (REVIEW-3) — đã xử lý.** Đồng ý đóng; Minh quyết.
- **S2 — phản hồi L9 "đúng một phần" hợp lý.** L9 chỉ ra rằng H1c không bật không đồng nghĩa với tắt E1/E2/E5. Đề xuất sửa description panel 5 là đủ. Chưa được duyệt, chưa sửa.
- **S3 — phản hồi L9 "đúng một phần" đúng.** Tôi viết "cả ba thời điểm" là chưa chính xác: snapshot L4 panel 35 dùng query có thêm regex error/exception/warn, không cùng query với L5 và L8c. L9 bổ sung phép đếm raw: 7.400 logRecords trong cửa sổ, payment-service 885, booking-service 0. Như vậy dữ liệu đã ghi nhận không có log booking. Chưa phân biệt được ứng dụng không phát log với log bị rơi trước khi ghi. Nguyên nhân vẫn OPEN; đồng ý.
- **S4 — đúng, chưa duyệt.** Giữ nguyên.
- **N1 (L9) — đồng ý.** Cùng phạm vi S1, đã xử lý cùng S1.
- **N2 (L9) — đúng, tôi đính chính.** Trong REVIEW-3, "726/726 liên kết bằng chứng" sai đơn vị. Đúng là 726 thao tác (295 + 303 + 128), với 1.479 phần tử `lien_ket` (601 + 609 + 269), giữa V071 và V082 trùng hoàn toàn. Kết luận dùng lại bằng chứng Explore của V071 cho V082 không đổi.
- **Một câu trong REVIEW-3 nay đã cũ:** "`nguon-l8b/chi-muc-ban.json` trùng SHA với `results/T-064/ban-xuat/chi-muc-ban.json`" đúng tại 15/11 trước bản 3. Nay phải đọc là trùng `chi-muc-ban-2.json` (xem T1).

## Tuân thủ quy trình

- L10 sửa đúng gói S1 đã được Minh duyệt ("Duyệt cả ba", DECISIONS mục R9/R10/S1, theo LOG L10). S2, S3, S4 không bị đụng (`kiem-cuoi.json#/checks/protected_sources_and_S2_S3_S4_untouched`).
- Người làm thêm đúng một dòng "S1 (sửa)" vào bảng phản hồi REVIEW-3. Tôi đã so: phần nhận xét và prompt của phản biện trước bảng trùng bản gốc.
- Manifest: 9.197/9.197 file khớp SHA; LOG khớp `#/task_log`.
- `kiem/009-s1-anh-minh/` do phiên Claude điều phối ghi sau manifest, nên chưa được ghim, chỉ có SHA256SUMS riêng. Không phải lỗi. Manifest lượt sau nên ghim thư mục này.
- Codex không lấy được ảnh (browser host không khả dụng; render trả HTTP 500) và ghi đúng là chưa làm, không tự nhận đạt. Ảnh do Minh chụp bù và được ghi rõ nguồn.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm gì:** kiểm lượt sửa S1 (L10), ảnh Minh chụp, phản hồi L9 cho S2–S4 và N1, N2. Đối chiếu chỉ mục T-064 bản 3 với bản 2.
2. **File đã thay đổi:** chỉ tạo `tasks/T-065-giao-dien-grafana/REVIEW-4.md`.
3. **Kiểm đã chạy:** lệnh Python chỉ đọc (manifest, so cấu trúc JSON, so chỉ mục, so đầu ra ebd5ef38); `sha256sum -c` cho ảnh; xem 4 ảnh.
4. **Bất đồng, câu hỏi mở, quyết định:**
   - Không còn bất đồng với người làm.
   - Chờ Minh quyết: S2, S3, S4 (gói đính chính chưa duyệt) và R4.
   - Lượt xuất lại ebd5ef38 theo bản 3 cần kiểm cả bảng cờ và khóa (T2), kèm sửa câu nguồn (T1).
   - OPEN: Loki booking 00eaea92, 10 quan sát (iii) lịch sử.
   - G-c phụ thuộc nghiệm thu T-064.
   - T-065 là giao diện minh họa DT18; không đóng RQ5/P10.

**Đề xuất: dừng phản biện phần S1.** Không còn phản đối nào ảnh hưởng tính đúng của đầu ra hiện có. Lượt xuất lại ebd5ef38 là đầu ra mới, nên cần một lượt kiểm ngắn riêng khi có (T1, T2). Minh quyết sửa S2–S4 và nghiệm thu.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, lượt L10 (sửa S1); tasks/T-065-giao-dien-grafana/SPEC.md; bản phản biện tasks/T-065-giao-dien-grafana/REVIEW-4.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md (mục L9–L10); docs/DECISIONS.md; results/T-064/ban-xuat/chi-muc-ban.json (bản 3) và chi-muc-ban-2.json; docs/WHY.md WHY-99.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md, REVIEW-3.md (gồm bảng phản hồi L9 và dòng S1 sửa), REVIEW-4.md; các mục L6–L10 trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/, grafana-l10/, grafana-l8b/, may-l8b/, kiem/008-s1/ (BAO-CAO.md, hash-truoc-sau.json, doi-chieu.json, kiem-cuoi.json, HOAN-TAC.md, s1-ssh.ps1, s1-may.py), kiem/009-s1-anh-minh/ (anh/, SHA256SUMS, GHI-CHU.md), XONG.md, CHECKPOINT.md, thay-doi-may.md, manifest.json, codex/manifest-L10-truoc.json.
- Phạm vi ghi được Minh cho phép trong lượt này: chưa có quyền ghi riêng cho lượt này; chỉ trả lời trong chat cho tới khi Minh hoặc điều phối theo quyền chiến dịch cấp quyền chính xác (ví dụ bảng "Phản hồi của người làm" trong REVIEW-4.md và mục LOG mới).

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| T1 | | | |
| T2 | | | |
| T3 | | | |

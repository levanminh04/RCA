# Phản biện T-065 — lượt 3 (kiểm lại phản hồi và sửa: L6, L7, L8, L8b, L8c)

- **Người phản biện:** Claude (Opus 5.5) — **Ngày:** 15/11/2026 — **Commit/diff đã đọc:** nhánh `claude/sweet-hawking-dy078d` trên `c3d27f8a`. Đầu ra T-065 chưa commit, ghim bởi `results/T-065/manifest.json` (`utc` 2026-11-14T22:53:09Z, `status` `dat_g_c_chrome_mau_L8c`).
- **Công đoạn/cổng và bản lượt:** kiểm lại phản hồi và sửa; chiến dịch M1-FlashTicket, nhánh giao diện sau G4. Quyền ghi đúng file này do phiên điều phối cấp ngày 15/11/2026, theo DECISIONS "Bổ sung quyền điều phối chiến dịch nhiều ngày, 13/11/2026" (tổ chức kiểm/phản biện theo phân vai). Giữ `REVIEW.md`, `REVIEW-2.md`.
- **Đã đọc:** `results/T-065/prompt-ban-giao.md`; SPEC; LOG mục L6–L8c; `codex/L8-brief.md`, `L8b-brief.md`; `kiem/004-r1-ui06/doi-chieu-dich.json`; `kiem/006-gc-cuoi/may-sau.json`, `BAO-CAO.md`; `kiem/007-gc-chrome/BAO-CAO.md`, `doi-chieu.json`, `observations.jsonl`; `XONG.md`; `README-L8b.md`; `grafana-l8b/*.json`; `grafana-l5/t065-l5-muc-luc.json`; `may-l8b/du-lieu/`; `results/T-064/ban-xuat/chi-muc-ban.json`, `cau-hinh-de-xuat.json`, `ho-so-chon.md` (§15 và đoạn V082 không có đầu ra cạnh); `docs/DECISIONS.md` mục V082; `docs/WHY.md` WHY-98 vùng V066/V082. Bảng phản hồi L6 trong `REVIEW-2.md` chỉ đọc sau phần tự soát.
- **Tự soát độc lập:** chỉ đọc file đã lưu. Không gửi truy vấn tới `exp-obs`, không động máy hay Chrome. Các lệnh Python chỉ đọc kèm kết quả ở mục "Điều đã kiểm và thấy đúng".

## Kết luận chung

Dữ liệu và API của G-c trên bản cuối V082 khớp nguồn: 83 slot có đầu ra, 0 lệch, và 1 slot lỗi chạy hiện đúng. R1 của lượt 2 đã đủ bằng chứng bấm thật (12/12 luồng). Còn **một điểm CHẶN**: trang Mục lục (điểm bắt đầu) và folder "1 · Kết quả hiện hành" vẫn mô tả bộ bản tạm. Mục lục không nhắc V082, không trỏ tới hai dashboard bản cuối. Lỗi này không do người làm: brief L8 chỉ cho tạo file dashboard mới. Ngoài ra có ba điểm KHÔNG CHẶN.

## Các điểm

### S1. Mục lục và folder "hiện hành" lỗi thời sau khi có bản cuối V082 — CHẶN

- **Ở đâu:**
  - `results/T-065/grafana-l5/t065-l5-muc-luc.json`, panel văn bản; dashboard UID `t065-l5-muc-luc` trên `exp-obs`.
  - Folder `RCA FlashTicket/1 · Kết quả hiện hành`.
- **Sai gì:**
  - Mục lục vẫn ghi: "P7 đã khóa. V032-H5b là đề xuất tạm. V041… là bản thay thế…". Nó liệt kê `t065-l4-rca` và `t065-l4-phat-lai` là **hiện hành**.
  - Mục lục không có dòng nào cho `t065-l8b-rca` hay `t065-l8b-phat-lai`, cũng không nhắc V082 hay V071.
  - Hai dashboard bản cuối được đặt chung folder "1 · Kết quả hiện hành" với hai dashboard L4 (bản tạm).
- **Bằng chứng:**
  - Đọc nội dung panel của `t065-l5-muc-luc.json`.
  - `kiem/006-gc-cuoi/may-sau.json#/old_files_changed` là `[]`: 3.019 file máy có trước không đổi, nên Mục lục trên máy giống file local.
  - `#/new_dashboards` cho thấy đường dẫn hai file mới nằm dưới `…/1 · Kết quả hiện hành/`.
  - Brief L8 (`codex/L8-brief.md` dòng 20 và 24) chỉ cho "thêm bản mới" và "chỉ file dashboard **mới**". Vì vậy người làm không có quyền sửa Mục lục.
- **Xét phản bác:** trang ca của `t065-l8b-rca` hiện đúng bản, trạng thái, hai hash cấu hình, hash mã nguồn và cửa sổ (18/18 trang, `kiem/007-gc-chrome/doi-chieu.json#/matched_pages`). Người đã vào đúng dashboard sẽ biết mình đang xem bản nào. Nhưng Mục lục được dựng ở L5 chính là điểm vào. Câu hỏi G-c "Người xem có biết đang xem bản M1 nào?" bị trả lời sai ngay từ điểm vào: người xem (ví dụ cô) sẽ được dẫn tới bản tạm, và đọc thấy V032 là đề xuất.
- **Bước và quyết định chịu ảnh hưởng:** lỗi đã xảy ra, do phạm vi brief chứ không do cách làm. Chặn đề nghị nghiệm thu G-c và chặn việc dùng giao diện để trình diễn kết quả cuối. Không ảnh hưởng số liệu.
- **Đề xuất sửa:**
  - Cần quyền mới (điều phối hoặc Minh cấp).
  - Sửa nội dung Mục lục: thêm hai UID `t065-l8b-*` là hiện hành, ghi V082 "đề xuất cuối (Minh chọn 14/11/2026)" và V071 "thay thế có đầu ra cạnh". Chuyển `t065-l4-*` thành "lưu trữ — bộ bản tạm L4".
  - Chuyển hai file `t065-l4-*.json` sang một thư mục con trong "9 · Lưu trữ". Giữ UID và byte JSON, ghi hash trước/sau và cách hoàn tác như lần sắp folder ở L5.
  - Kiểm bằng API folders và một ảnh Mục lục. Không cần chạy lại dữ liệu, API hay Chrome của L8b/L8c.

### S2. Ô "không có đầu ra cạnh" của V082 dễ bị đọc thành "V082 không dùng quan hệ" — KHÔNG CHẶN

- **Ở đâu:** `grafana-l8b/t065-l8b-rca.json` panel 5 "Trạng thái đầu ra cạnh" và panel 6; dữ liệu `may-l8b/du-lieu/V082-V066+H8a/*.json#/trang_thai_canh` = "không có đầu ra cạnh".
- **Sai gì:** dashboard ghi đúng là V082 không xuất xếp hạng cạnh. Nhưng không có câu nào nói quan hệ vẫn được dùng bên trong phương pháp. `results/T-064/ho-so-chon.md` ghi: "V082 không có đầu ra cạnh; vai trò tính toán của quan hệ trong V082 là E1/E2/E5 của lõi P7". Tên bản `V082-V066+H8a` chứa "V066" (V041 bỏ H1c). Ở đây đồ thị thao tác panel 23 chỉ là quan hệ span quan sát được. Người xem có thể hiểu rằng bản cuối không dùng đồ thị. AGENTS luật 18 yêu cầu vai trò tính toán của đồ thị phải rõ.
- **Bằng chứng:** tìm trong JSON dashboard L8b: 0 lần "không dùng quan hệ", "bỏ quan hệ"; lần duy nhất có "E1" là câu về span bọc ở bảng thao tác, không nói vai trò quan hệ khi xếp hạng; panel 23 chỉ ghi "Không suy nhân quả từ quan hệ này".
- **Hậu quả:** dễ hiểu sai khi trình diễn; không sai số liệu.
- **Đề xuất sửa:** thêm một câu vào panel 5 hoặc vào lời diễn giải ở dữ liệu xuất, kèm con trỏ hồ sơ T-064: V082 không xuất bảng cạnh; quan hệ dùng bên trong qua E1/E2/E5; đồ thị thao tác chỉ để truy vết. Có thể gộp vào lượt sửa S1.

### S3. Loki rỗng của 00eaea92/booking-service: dữ liệu đã lưu đủ loại một giải thích — KHÔNG CHẶN

- **Ở đâu:** `kiem/007-gc-chrome/BAO-CAO.md` ("Loki của `00eaea92` trả 0 dòng… Cần đối chiếu log đã lưu với nhãn và cấu hình retention…"); `XONG.md`.
- **Sai gì:** báo cáo để OPEN và đề xuất kiểm retention. Dữ liệu đã lưu cho thấy:
  - truy vấn `{service_name="booking-service"}` của ca này rỗng ở cả ba thời điểm: snapshot L4 01:37:31Z ngày 14/11 (`kiem/002/api-snapshot.json`, khóa `00eaea92/booking-service`, panel 35, `so_dong` 0), 6 lượt bấm L5 (`kiem/003-trinh-duyet/kiem-lien-ket-that.json`, `co_du_lieu` false) và L8c;
  - trong **cùng cửa sổ** `[1794442999000, 1794443598999]`, `{service_name="payment-service"}` có dữ liệu ở cả 6 lượt L5.
  - Vậy retention của cả khung giờ khó giải thích được. Còn lại hai khả năng: booking-service không phát log trong cửa sổ, hoặc nhãn/luồng của booking-service khác.
- **Bước và quyết định chịu ảnh hưởng:** chỉ ảnh hưởng mức giải thích của phần OPEN.
- **Đề xuất sửa:** ghi dữ kiện trên vào báo cáo. Nếu muốn phân xử, đếm dòng log booking-service trong cửa sổ từ gói raw đã băm của ca 00eaea92 (T-062, không thuộc `data/locked/`). Phép này chỉ đọc, tốn vài phút, không cần máy. Trước đó vẫn giữ OPEN.

### S4. Các đính chính tài liệu theo R2, R3, N1 chưa được áp dụng — KHÔNG CHẶN (trạng thái)

- **Ở đâu:** `kiem/003-trinh-duyet/BAO-CAO.md`, `BAN-GIAO-L5.md`; impact map L6 trong LOG.
- **Sai gì:** không có lỗi của người làm. L6 đề xuất các đính chính và đúng là chờ duyệt. SHA hai file hiện tại (`5e196236…`, `c5ec446f…`) bằng giá trị trong `codex/manifest-L7-truoc.json`. Vậy chúng chưa đổi từ L5 sang L8c. `BAN-GIAO-L5.md` vẫn ghi G-b "Dùng lại luồng mẫu đã đạt" mà không trỏ tới R1/L7.
- **Đề xuất:** Minh hoặc điều phối quyết có áp dụng gói đính chính L6 không. Đề xuất của phản biện: áp dụng phần nối thêm (không sửa câu cũ) cho R1/L7, R2, R3 và N1 trong hai file trên, gộp vào lượt sửa S1. Lý do: rẻ, và giữ được truy vết. Mặt trái: đổi hash hai file đã ghim, nên cần manifest lượt mới. Phương án khác: chỉ dựa vào LOG và REVIEW; khi đó người đọc báo cáo L5 riêng lẻ sẽ thấy bản lỗi thời.

## G-c: đánh giá trên bản cuối

- **Đạt, đã kiểm lại độc lập:**
  - Chỉ mục nguồn: `nguon-l8b/chi-muc-ban.json` trùng SHA với `results/T-064/ban-xuat/chi-muc-ban.json` (`7e4278d6…`); 3 bản × 28 ca.
  - 83/83 slot có đầu ra khớp SHA; xếp hạng (thực thể, `tie_group`) khớp nguồn; `sha256_output` và `cau_hinh_sha256` khớp chỉ mục. V082 hiện "không có đầu ra cạnh" ở 28/28 trang.
  - P7/ebd5ef38 (`dau_ra` null, có `loi_chay`) hiện "không có đầu ra phương pháp — lỗi chạy", 0 dòng hạng, kèm lời giải thích cửa sổ.
  - Quy ước hash: `cau_hinh_sha256` của V082 (`451a8437…`) bằng `extra/m1_ft/cau_hinh_sha256` trong đầu ra. `cau_hinh_file_sha256` (`01a64b60…`) bằng SHA byte của `results/T-064/bien-the/V082-V066+H8a/cau-hinh.json`.
  - Không có khóa đáp án nào trong dữ liệu trang chính của 84 slot.
- **Chrome L8c:** 18/18 trang, 9/9 bảng, 9/9 Inspector HTTP 200 (8 có dữ liệu). Lưu ý: cả 9 đích Explore đều bấm trên V071. Kết quả vẫn áp được cho V082 vì 726/726 liên kết bằng chứng của ba ca mẫu giống hệt giữa V071 và V082 (đối chiếu `thao_tac[].lien_ket` trong `may-l8b/du-lieu`). Liên kết 4/22/23 của `t065-l8b-rca` trùng mẫu UI06 đã kiểm ở R1, chỉ khác UID. Báo cáo nên nói rõ điểm này, nhưng không cần bấm lại.
- **Phụ thuộc còn mở:** DECISIONS mục V082 ghi rõ đây chưa phải nghiệm thu T-064; độ nhạy dời mốc và phản biện cuối của T-064 còn chờ. Nếu T-064 đổi đầu ra, chỉ mục hoặc hash của V082, cần xuất lại và đối chiếu phần chịu ảnh hưởng.

## Đối chiếu các lượt trước

- **R1 (REVIEW-2, CHẶN) — đã xử lý.** `kiem/004-r1-ui06/doi-chieu-dich.json`: `passed` 12/12. Có 3 ca × 3 bản (1ad3afeb/P7, 46aab4be/V032, 2e2a5541/V041), mỗi ca gồm panel 4, 22, 23 của trang chính và panel 4 của phát lại. Mỗi luồng có URL đích ISO đúng cửa sổ và Inspector panel sống HTTP 200 (ví dụ lần 1: `from_ms` 1794431776000, `to_ms` 1794432375999, step 15s). Lần 19 thiếu Inspector ở checkpoint, đã bổ sung ở L7 tiếp nhận. Đồng ý đóng R1; Minh quyết.
- **R2 — phản hồi L6 đúng.** L6 thêm được dữ kiện: cả 67 DOM có URL số ở ca khác chỉ là trang "Loading", nên không làm đối chứng được. Tôi đồng ý giữ loại (iii)/OPEN và coi URL số là ứng viên. Đính chính tài liệu chưa áp dụng (S4).
- **R3 — phản hồi L6 đúng.** Phép đếm L6 (18 khóa trùng; 568 = 381 + 187) khớp phép đếm của tôi ở lượt 2. Chưa áp dụng (S4).
- **R4 — phản hồi L6 "đúng một phần" là đúng.** Lượt 2 tôi chỉ đối chiếu mục 14/11. Mục 13/11 giao Claude "toàn quyền điều phối và triển khai" trong chiến dịch, nên câu "vượt văn bản quyền" mạnh hơn bằng chứng. Tôi rút mức xuống: quyền xóa folder rỗng có thể đọc theo hai cách; Minh phân xử. Vẫn đề xuất xác nhận, không hoàn tác.
- **N1 (người làm tự tìm) — đúng, KHÔNG CHẶN.** Chỉ là lịch sử, ở 3/66 trang e8661e0a. Bằng chứng sau UI06 cho thấy cả ba bản đúng cửa sổ. Không quy được cơ chế khi thiếu request đúng giờ cũ.
- **Phản hồi L6 đã điền đúng bảng của REVIEW-2.** Phần nhận xét và prompt của phản biện giữ nguyên: đã so phần trước bảng phản hồi với bản gốc, trùng hoàn toàn.

## Tuân thủ quy trình

- Máy: L8b chỉ thêm thư mục `t065-l8b-001` và hai file provisioning mới. 3.019 file có trước giữ hash. Không restart (`may-sau.json#/restart_by_agent` false; compose/provider/datasource không đổi). Khớp phạm vi brief L8 và SPEC.
- L8 dừng đúng lúc khi gặp mâu thuẫn quy ước hash, rồi chờ nguồn được sửa, không tự chọn. Đây là cách làm đúng luật cứng 4 và AGENTS mục 3.13.
- Lỗi công cụ (ENOSPC, tunnel mất, chụp ảnh quá thời gian, DOM ngoài khung nhìn) được giữ lại và tách khỏi kết quả.

## Điều đã kiểm và thấy đúng

- Manifest: 9.175/9.175 file khớp SHA và số byte (Python, đọc `#/files`); LOG khớp `#/task_log`.
- Bảng phản hồi REVIEW-2: phần trước bảng trùng bản tôi ghi ở lượt 2.
- Các phép kiểm G-c và R1 nêu ở hai mục trên.
- Biến `t_tu`/`t_den` và thời gian mặc định của `t065-l8b-rca` dùng ISO (`$fromMillis`). Liên kết panel 4/22/23 trùng UI06, chỉ khác UID.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm gì:** kiểm lại phản hồi L6 và các lượt sửa/kiểm L7, L8, L8b, L8c trên file đã lưu. Đối chiếu độc lập dữ liệu G-c bản cuối với nguồn T-064.
2. **File đã thay đổi:** chỉ tạo `tasks/T-065-giao-dien-grafana/REVIEW-3.md`.
3. **Kiểm đã chạy:** các lệnh Python chỉ đọc trên `results/T-065/` và `results/T-064/`. Không truy vấn `exp-obs`, không động Chrome.
4. **Bất đồng, câu hỏi mở, quyết định:**
   - S1 (CHẶN): cần quyền sửa Mục lục và chuyển hai dashboard L4 sang lưu trữ.
   - S2–S4: sửa nhỏ hoặc chấp nhận giới hạn.
   - R4: Minh phân xử phạm vi quyền.
   - Loki 00eaea92 và 10 quan sát (iii) lịch sử vẫn OPEN.
   - G-c phụ thuộc T-064 chưa nghiệm thu.
   - T-065 là giao diện minh họa DT18; không xác nhận lợi ích RCA hay đóng RQ5/P10.

**Đề xuất:** tiếp tục một lượt ngắn chỉ cho S1 (gộp S2, S4 nếu được cấp quyền), rồi dừng phản biện. Lý do: S1 là điểm duy nhất chặn nghiệm thu; sửa rẻ và không cần kiểm lại dữ liệu. Sau khi S1 đạt, tôi không còn phản đối nào ảnh hưởng tính đúng. Minh quyết nghiệm thu.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, các lượt L6, L7, L8, L8b, L8c; tasks/T-065-giao-dien-grafana/SPEC.md; bản phản biện tasks/T-065-giao-dien-grafana/REVIEW-3.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-065/codex/L8-brief.md, L8b-brief.md, L8b-app-brief.md; results/T-064/hop-dong-dau-ra.md, ban-xuat/chi-muc-ban.json, cau-hinh-de-xuat.json, ho-so-chon.md; docs/DECISIONS.md.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md (gồm bảng phản hồi L6), REVIEW-3.md; results/T-065/codex/L6-dap-review2.json; các mục L6–L8c trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/, grafana-l8b/, may-l8b/, nguon-l8b/, kiem/003-trinh-duyet/, kiem/004-r1-ui06/, kiem/006-gc-cuoi/, kiem/007-gc-chrome/, codex/l8b-*.py, codex/l8b-local.ps1, README-L8b.md, XONG.md, manifest.json; lệnh kiểm checksum & ./results/T-065/codex/l8b-local.ps1 -Action verify.
- Phạm vi ghi được Minh cho phép trong lượt này: chưa có quyền ghi riêng cho lượt này; chỉ trả lời trong chat cho tới khi Minh hoặc điều phối theo quyền chiến dịch cấp quyền chính xác (ví dụ bảng "Phản hồi của người làm" trong REVIEW-3.md và mục LOG mới).

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
| S1 | Đúng — CHẶN nghiệm thu G-c và trình diễn bản cuối qua điểm bắt đầu. | Đọc lại mục lục ghim tại grafana-l5/t065-l5-muc-luc.json; nội dung không có hai UID L8b, V082/V071 hoặc 28 ca. may-l8b/kiem/may-truoc.json ghim mục lục và hai L4; may-sau.json ghi 0 file cũ đổi và đặt hai L8b cùng folder hiện hành. Hai dashboard L8b riêng khớp nguồn, nên lỗi thuộc đường vào/lưu trữ, không thuộc số xuất. N1 tự soát L9 trùng vấn đề này. L8 chỉ cho thêm mới; không tự sửa. Đề xuất mục lục mới trỏ L8b, V082 đề xuất cuối Minh chọn và V071 thay thế; chuyển đúng hai L4 sang lưu trữ giữ UID/byte. File, hash dự kiến, hoàn tác và chi phí ở LOG L9. | |
| S2 | Đúng một phần — KHÔNG CHẶN. | Nhãn “không có đầu ra cạnh” đúng ở 28/28 slot V082; chưa có bằng chứng người xem thực sự hiểu sai. Thiếu lời giải thích có thể gây nhầm khi demo. Hash cây mã src/m1 + src/m1_ft khớp bản V082; chuoi.py dùng E1 ở mau_thao_tac, E2 ở mau_canh/gan_canh, E5 ở phan_loai; H1c không bật không đồng nghĩa tắt E1/E2/E5. Đề xuất chỉ thêm description panel 5 của JSON RCA, dẫn hồ sơ chọn §15 và nói graph thao tác là truy vết; không sửa 28 bản xuất hoặc phương pháp. Nguồn sửa lưu riêng grafana-l10, giữ JSON L8b lịch sử; chi tiết/hash ở LOG. | |
| S3 | Đúng một phần — KHÔNG CHẶN. | Tự đếm L5: 6 query booking thuần rỗng, 6 query payment có dữ liệu cùng window. Nhưng snapshot L4 panel 35 có thêm regex error/exception/warn, nên không phải cùng query ở cả ba mốc. L9 đã kiểm raw-logs.jsonl theo manifest ca 00eaea92: 14.280 logRecords, 7.400 trong cửa sổ, payment 885, booking 0 theo resource service.name. Điều này thu hẹp vắng dữ liệu ghi nhận; không chứng minh ứng dụng không phát log và không loại mọi khả năng retention/nhãn/định tuyến theo stream. Chưa có stdout/Collector/Loki đúng thời điểm để tách các giải thích. Đề xuất nối đính chính vào báo cáo L8c; giữ nguyên nguyên nhân OPEN, không sửa kho quan sát. Lệnh/count, giới hạn, hash dự kiến và chi phí ở LOG L9. | |
| S4 | Đúng — KHÔNG CHẶN; gói đính chính chưa được duyệt thực hiện. | Hash BAO-CAO L5 và BAN-GIAO-L5 khớp manifest L7-truoc và manifest hiện hành; không được tự áp dụng góp ý. Đếm lại R2 khớp 36 URL số của e8661e0a, 67/1.665 lượt số của 21 ca khác; R3 khớp 586 bản ghi, 568 khóa, 381 false positive, 187 panel (177 i, 10 iii). R1/L7 có 12/12 luồng với Inspector HTTP 200; phản hồi N1 lịch sử vẫn có giới hạn cơ chế. Đề xuất nối cùng đính chính vào hai tài liệu, giữ câu/file thô và lưu manifest trước khi ghim lượt mới. Không sửa trong L9. | |
| N1 (L9) | Tự soát trước review — CHẶN, cùng phạm vi S1; không tính thành lỗi thứ hai. | Nguồn độc lập trước khi đọc kết luận: folder-plan.json#/dashboard/panels/0/options/content, may-truoc.json#/files và may-sau.json#/old_files_changed. Kết luận chỉ cho mốc hồ sơ L8b/L8c; chưa GET live ở L9. Đề xuất và quyền chờ như S1. N1 của L6 là lỗi thời gian lịch sử khác, không gộp với N1 này. | |
| N2 (L9) | Tự kiểm sau đọc review — KHÔNG CHẶN; sai đơn vị đếm trong nhận định G-c của REVIEW-3. | 726 là số thao tác, không phải số phần tử lien_ket: 295 + 303 + 128 thao tác ở 86dea661/ebd5ef38/00eaea92. Số liên kết tương ứng 601 + 609 + 269 = 1.479; đối chiếu đầy đủ id và mảng lien_ket giữa V082/V071 đều trùng. Chín lần Explore L8c đều ở V071 đúng như reviewer nêu. Kết luận dùng lại bằng chứng vẫn đứng; đề nghị reviewer dùng đúng đại lượng trong lượt sau. Người làm không sửa nhận xét của reviewer. | |
| S1 (sửa) | Đã triển khai và kiểm API theo gói L9; ảnh chưa làm, chưa đề nghị xác nhận hoàn tất S1. | Nguồn mục lục mới grafana-l10 chỉ đổi panels[0].options.content; hash live trước/sau đúng pin. Hai L4 giữ UID/byte ở Lưu trữ, hai L8b còn Hiện hành; GET nội dung/folders/search khớp. Bằng chứng và hoàn tác: results/T-065/kiem/008-s1/BAO-CAO.md, hash-truoc-sau.json, doi-chieu.json, HOAN-TAC.md. Browser access host không khả dụng; API render HTTP 500, còn ảnh và bấm từ Mục lục để Minh chạy app. S2/S3/S4 chưa duyệt và chưa sửa. | |

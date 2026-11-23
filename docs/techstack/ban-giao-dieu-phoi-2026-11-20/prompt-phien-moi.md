# Prompt mở phiên Claude điều phối mới — rà soát rồi triển khai

Soạn theo duyệt của Minh (chat 20/11/2026, nguyên văn ở cuối `lich-su/01-minh-tin-nhan.md`): "soạn prompt chi tiết cho phiên claude mới yêu cầu triển khai task , trước khi triển khai cần phiên tự rà soát lại toàn bộ plan một lượt nếu phát hiện có điểm xung đột hoặc rủi ro dẫm chân nhau giữa các phiên thì cần sửa ngay, nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình".

**Cách dùng:** Minh chọn model và effort cho phiên điều phối (Opus 5.5 high hoặc xhigh), mở phiên mới tại `D:\RCA-flashticket` **trên laptop này** (gói và T-069 chưa commit), dán **một** khối dưới đây.

```text
Bạn là phiên Claude ĐIỀU PHỐI mới của Minh cho giai đoạn 2 RCA FlashTicket (W4, W5, W6, W8, đường tới W9a), thư mục D:\RCA-flashticket. Bạn không có lịch sử chat cũ; mọi ngữ cảnh nằm trong repo. Đọc AGENTS.md trước và tuân theo nó (Luật 0, luật cứng, mục 5–9). Gói bàn giao: docs/techstack/ban-giao-dieu-phoi-2026-11-20/.

== QUYỀN MINH ĐÃ CHO (nguyên văn, chat 20/11/2026) ==
"trước khi triển khai cần phiên tự rà soát lại toàn bộ plan một lượt nếu phát hiện có điểm xung đột hoặc rủi ro dẫm chân nhau giữa các phiên thì cần sửa ngay, nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình"
Mong muốn đầy đủ của Minh: mong-muon-minh.md (tất cả mục "Trực tiếp" là lời Minh, không cần hỏi lại).

== GIAI ĐOẠN 0 — KIỂM TRẠNG THÁI (chỉ đọc, chỉ local) ==
1. git status (gói bàn giao, T-069, DECISIONS/WHY/STATE đều có thay đổi chưa commit — đọc cây làm việc, không chỉ commit).
2. Kiểm manifest: chạy `sha256sum -c SHA256SUMS` và `sha256sum -c SHA256SUMS-2` từ TRONG results/T-069/; `sha256sum -c SHA256SUMS` từ trong thư mục gói bàn giao.
3. Trạng thái máy và lịch: chỉ dùng bằng chứng đã ghi (README §2), ghi rõ thời điểm của bằng chứng và phần chưa xác minh hiện tại. Không SSH ở giai đoạn này. Kiểm lịch trong ứng dụng Claude bằng công cụ liệt kê lịch (chỉ đọc).
4. Không coi phiên Claude cũ hay phiên fork là chủ việc nào. Không có job server nào được ghi là đang chạy; nếu phát hiện dấu hiệu khác, đó là lỗi chặn (giữ nguyên job, trình Minh).

== GIAI ĐOẠN 1 — TỰ RÀ SOÁT TOÀN BỘ PLAN MỘT LƯỢT ==
Bước 1A (độc lập, chưa đọc phản biện): đọc README.md, mong-muon-minh.md, tasks/T-069-v082-ban-ghim/SPEC.md + mục cuối LOG.md, results/T-069/dinh-chinh-1.md, docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8, và mục "## 2. Kế hoạch điều phối bản 4" trong lich-su/08-claude-ke-hoach-ban-4.md. Kiểm đường thực thi thật trong code: repo lab D:/Project/flashticket-rca-lab commit 407b4f5 (load/controller/tai_linux.py, load/scenarios/purchase-journey.js, campaigns/runner/runner4.py, xuat_bo_sung.py, stage_m1.py), FlashTicket D:/Project/flash-ticket-platform revision 36a3725d. Ghi danh sách điểm tự tìm (đặc biệt: xung đột, rủi ro dẫm chân giữa các phiên về file, máy, khung giờ, Prometheus/Grafana, checkout repo lab; phụ thuộc; việc song song được; việc phải tuần tự).
Bước 1B: đọc thong-nhat.md (kế hoạch hiệu lực = bản 4 + sửa ở §1; ba điểm còn chặn ở §2 kèm ba phương án tải A/B/C), rồi phản biện Codex lich-su/05, 07, 09, 12 và các lượt Claude 02–04, 06, 10, 11, 13. Đối chiếu với danh sách 1A bằng bằng chứng riêng; Codex và Claude cũ đều có thể sai. Ghi rõ điểm nào 1A tự tìm, điểm nào chỉ thấy sau khi đọc phản biện.

== GIAI ĐOẠN 2 — PHÂN LOẠI VÀ XỬ LÝ ==
LỖI CHẶN (dừng, trình Minh, không triển khai phần bị ảnh hưởng; vẫn làm phần độc lập không bị ảnh hưởng):
- làm một phép đo hoặc kết quả sai hay không diễn giải được (tính đúng ưu tiên cao nhất);
- hai phiên/tiến trình phải ghi cùng file, dùng cùng máy/dịch vụ trong cùng khung giờ mà phiên điều phối không thể xếp tuần tự trong quyền của mình;
- plan trái AGENTS.md, DECISIONS, SPEC đã duyệt, hoặc cần một quyết định thuộc mục "DÀNH CHO MINH" trước khi BẤT KỲ việc nào chạy được;
- trạng thái repo/máy khác README theo cách ảnh hưởng an toàn (hash lệch, job không rõ chủ).
LỖI NHỎ (sửa ngay, ghi lại, rồi triển khai): câu chữ, thứ tự, phân chia file/thư mục/khung giờ, hợp đồng giữa phiên, ngân sách thời gian, thiếu bước kiểm — miễn không đổi nội dung khoa học (tiêu chí, ngưỡng, phép đo, dữ liệu dùng) và không đụng mục DÀNH CHO MINH.
Ghi mọi sửa (đoạn cũ → mới, lý do) vào LOG của task điều phối (dưới đây).

== GIAI ĐOẠN 3 — TRIỂN KHAI (khi không còn lỗi chặn ở phần đó) ==
1. Kiểm danh mục tasks/ rồi tạo task điều phối T-070 (mã dự kiến; nếu đã bị dùng thì lấy mã kế tiếp): tasks/T-070-dieu-phoi-giai-doan-2/ gồm SPEC.md (kế hoạch bản 5 = bản 4 + sửa §1 thong-nhat + sửa của bạn, kèm danh sách thay đổi so với bản 4), LOG.md, TRANG-THAI.json (mỗi việc: mã slot/tag, phiên chủ và mã phiên, lệnh đã phát, revision, máy, nơi đầu ra, hash, lần kiểm cuối, bước tiếp), LICH-MAY.md (chủ theo khung giờ cho exp-app, máy tải AWS, Grafana, phần exp-obs chịu tải), HOP-DONG.md (I1–I6 và mọi hợp đồng mới). Thêm dòng T-070 vào docs/STATE.md (chỉ dòng của bạn).
2. Tạo các task làm việc theo plan (dự kiến T-071 W4a nền, T-072 W4b luật, T-073 W5, T-074 W6, T-075 W8; kiểm lại mã), mỗi task có SPEC đủ mục theo tasks/_MAU (gồm Phạm vi ghi, Người làm, Người phản biện = Codex, Tiêu chí xong, mục luật 21 nếu có lượt > 1 giờ) và LOG. SPEC không được vượt kế hoạch bản 5 và không tự quyết mục DÀNH CHO MINH.
3. Mở các phiên Claude làm việc (công cụ start_session), mỗi phiên một task, brief đủ để tự làm từ repo; mức model theo mong-muon-minh.md (Medium/High theo độ khó, ghi lý do; T-074 W6 mức High). Phiên điều phối giữ quyết định tích hợp, bất đồng, thiết kế khoa học và lịch máy. Một máy/dịch vụ chỉ một chủ theo khung giờ trong LICH-MAY.md; code đang viết ở nhánh hoặc checkout riêng, /opt/rca-lab chỉ checkout commit đã duyệt và phải sạch.
4. Codex qua terminal cho việc phụ có đầu vào/đầu ra/tiêu chí rõ (đối chiếu hash, rà đường code, kiểm diff): `$brief | codex exec -C D:/RCA-flashticket -m gpt-6.2-astra -c 'model_reasoning_effort="high"' -s read-only --json -`, chạy nền, ghi mã việc và thread ID vào TRANG-THAI.json. Hết usage → báo Minh đổi account ngay; mất mạng, lỗi lệnh, hết quota là ba tình trạng khác nhau. Lượt Codex hỗ trợ không thay lượt phản biện chính thức (AGENTS §9): với mỗi SPEC, soạn prompt Codex soát SPEC theo docs/review-prompt.md để Minh chuyển.
5. Thức và tiếp nhận: ưu tiên thức theo sự kiện (phiên con báo về khi xong lượt; lệnh nền theo dõi từng job server, thoát khi job kết thúc; job Codex nền). Mỗi lần thức xét việc độc lập đủ điều kiện để phát. Lịch dò dự phòng: soạn cấu hình đề xuất (chu kỳ, nội dung, hai nhánh: chủ còn chạy → báo đúng mã việc; chủ đã dừng → phiên tiếp nhận kiểm chủ cũ và lệnh nền, nhận quyền đúng một lần, tiếp từ checkpoint) — CẤU HÌNH CỤ THỂ CHỜ MINH (mục R6). Lịch M1 cũ không bật lại.
6. Khi gián đoạn: trước khi phát lại bất cứ gì, kiểm tag/container/log/manifest trên server và nhận lại đầu ra; không gọi lại nguyên lịch runner (sinh mã ca mới); chưa rõ trạng thái thì giữ job và làm việc độc lập. Phân biệt lỗi cục bộ (một lượt) với lỗi nguồn chung (nhiều lượt). Không đặt "không làm lại 100%" lên trên tính đúng.
7. T-069: bạn là phiên giữ T-069. Được nối dòng đính chính hash vào LOG T-069 theo thong-nhat.md §1.1 (sửa nhỏ đã thống nhất). Lượt Codex kiểm lại kết quả T-069 dùng prompt ở cuối LOG T-069 (Minh chuyển); nghiệm thu, commit là của Minh.

== DÀNH CHO MINH (không tự quyết; gom hỏi MỘT lần trong báo cáo đầu; trong lúc chờ vẫn làm việc độc lập) ==
R1 Q1: dùng V082 cho demo / nghiệm thu W3 (ngoại lệ CPU-BOOK-1).
R2 Nghiệm thu, đóng task; commit/push repo RCA; ghi docs/DECISIONS.md, WHY, MRP, LESSONS, AGENTS (khối đề xuất DECISIONS ở mong-muon-minh.md §4).
R3 Gửi bất kỳ nội dung nào ra ngoài (bản nháp báo nhóm FlashTicket chỉ soạn).
R4 Sửa code lõi M1/V082, bộ tải, runner chung ngoài SPEC; mở dữ liệu khóa hay test.
R5 Ngưỡng báo động giả chấp nhận (ứng viên ≤ 1 sự cố / 6 giờ khỏe ×1).
R6 Cấu hình cụ thể của lịch dò dự phòng.
R7 Phương án tải cho E2/E4 (A/B/C ở thong-nhat.md §2) và duyệt lượt chạy dài > 1 giờ theo luật cứng 8 và luật 21 (E2, E4): trình chi phí, ngân sách lượt, mục lỗi 10/50/99%. E1 (đồng bộ ngày Ticket/Payment theo giá trị đích, dump trước, kiểm đúng dòng, đọc lại; rồi chụp mốc DB) thuộc quyền triển khai nếu không có lỗi chặn.
R8 Đổi model phiên điều phối; tăng mức model phiên làm việc (báo kèm ví dụ).
Nếu bạn thấy quyền triển khai chưa đủ rõ cho một việc cụ thể, xếp nó vào lần hỏi gom thay vì đoán; không vì thế dừng phần khác.

== BÁO CÁO ĐẦU CHO MINH (sau giai đoạn 1–2, trước hoặc song song phần triển khai đã được phép) ==
Theo AGENTS §7: đã làm gì; file đã thay đổi; kiểm đã chạy và kết quả; điều chưa chắc. Thêm: danh sách điểm 1A/1B và cách xử lý (sửa nhỏ / lỗi chặn); kế hoạch bản 5 tóm tắt; bảng phân công phiên (người giữ, model/mức và lý do, đầu vào, đầu ra, nơi ghi, tài nguyên, điều kiện bắt đầu, cách bàn giao, việc làm ngay); lịch máy; các phiên đã mở; một lần hỏi gom R1–R8 kèm đề xuất, mặt trái, phương án khác. Sau mỗi lượt, soạn prompt Codex theo docs/review-prompt.md (đặt trong LOG T-070).
```

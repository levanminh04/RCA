# T-070 — Điều phối giai đoạn 2 (W4, W5, W6, W8 → W9a), kế hoạch bản 5

- **Trạng thái:** đã duyệt triển khai 20/11/2026 theo quyền Minh cho (nguyên văn ở dưới), **trừ** các mục ghi "chờ Minh (R…)".
- **Người làm:** Claude (phiên điều phối, Opus 5.5, mức do Minh chọn).
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6.

Quyền Minh cho (chat 20/11/2026, `docs/techstack/ban-giao-dieu-phoi-2026-11-20/lich-su/01-minh-tin-nhan.md`, tin cuối): "trước khi triển khai cần phiên tự rà soát lại toàn bộ plan một lượt nếu phát hiện có điểm xung đột hoặc rủi ro dẫm chân nhau giữa các phiên thì cần sửa ngay, nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình".

## Mục tiêu

Đưa nhánh demo của [kế hoạch giai đoạn 2 §8.2](../../docs/techstack/KE-HOACH-GIAI-DOAN-2.md) (W4 luật cảnh báo, W5 RCA trực tuyến chế độ (b), W8 LLM tối thiểu, W9a diễn tập) và thiết kế W6 tới chỗ chạy được, bằng nhiều phiên Claude song song không dẫm chân nhau (Minh, chat 20/11 03:10Z; tin gửi Codex 03:33:57Z). Nguồn sản phẩm: DT18 "giao diện minh họa kết quả phân tích"; MRP P10, Q-28 (báo sự cố → đồ thị con → nguyên nhân → LLM giải thích; phần phát hiện demo ngang phần RCA).

Task này là **điều phối và thiết kế tích hợp**: phân công, hợp đồng giữa phiên, lịch máy, tiếp nhận sau gián đoạn. Nó không tự trả lời câu hỏi khoa học của W4–W6; các câu đó nằm ở SPEC T-071–T-075. Tính đúng ưu tiên cao nhất (Minh 20/11 03:10Z).

## Kế hoạch bản 5

Bản 5 = mục "2. Kế hoạch điều phối bản 4" (`docs/techstack/ban-giao-dieu-phoi-2026-11-20/lich-su/08-claude-ke-hoach-ban-4.md`) + sửa ở `thong-nhat.md` §1 + các sửa C1–C10 dưới đây. Khi lệch nhau: file này > `thong-nhat.md` §1 > bản 4.

### Phân công

| Phiên | Task | Model/mức | Tài nguyên (theo `LICH-MAY.md`) | Bắt đầu |
|---|---|---|---|---|
| Điều phối | T-070 | Opus 5.5, Minh chọn | Không chạy máy; giữ lịch máy, hợp đồng, quyết định tích hợp | Ngay |
| *(T-069)* | T-069 | phiên điều phối giữ | — | Chỉ nối đính chính (đã làm); chờ Codex kiểm lại, Minh nghiệm thu |
| nen-w4 | T-071 W4a nền | High (thao tác DB và máy có rủi ro) | Chủ exp-app, máy tải AWS, Prometheus sống ở S0–S3 | Ngay (E1 và chuẩn bị); E2 chờ cổng |
| luat-w4 | T-072 W4b luật | High (thống kê, tiêu chí khai trước) | Grafana chỉ ở S2 (E3) | Ngay |
| rca-w5 | T-073 W5 | High (tích hợp nhiều thành phần) | exp-obs nhẹ ở S0; chủ máy ở S4 (E5) | Ngay |
| danh-gia-w6 | T-074 W6 | High (thiết kế khoa học) | Không máy cho tới S5 | Ngay |
| llm-w8 | T-075 W8 | Medium (phạm vi demo) | Không máy | **Chờ Minh (Q6, nhà cung cấp LLM)** |

Đổi mức model: phiên điều phối ghi ví dụ cụ thể (lỗi lặp, không tiến triển), phần việc bị ảnh hưởng, báo Minh; giữ checkpoint trước khi đổi (R8).

### Thứ tự dùng máy (chi tiết ở `LICH-MAY.md`)

E1 (đồng bộ ngày Ticket/Payment theo giá trị đích, kiểm sức chứa vé, chụp mốc DB) → E2 (khoảng 1, chọn ngưỡng) → E3 (nạp luật, kiểm webhook ngoài khoảng chấm) → E4 (khoảng 2, đo báo động giả) → E5 (nghiệm thu W5) → E6 (W6 đo khôi phục DB, **sau E5**) → E7 (diễn tập W9a).

**Cổng phát E2** (mọi điều kiện, ghi vào `TRANG-THAI.json` khi đạt):
1. E1 xong, sức chứa vé đủ cho E2 + E4 + E5 (C3).
2. Minh chọn phương án tải A/B/C và duyệt lượt dài (R7), duyệt ngưỡng ứng viên báo động giả (R5).
3. T-072 đã chốt biểu thức, nhãn, nhịp đánh giá, khoảng nhìn lùi, quy tắc gom, cách đếm sự cố vắt qua biên; T-071 đã chứng minh xuất được đúng các chuỗi đó (CHẶN 3 của Codex bản 4).
4. Tập lượt E2 và ngân sách cố định trong `results/T-071/khai-truoc-e2.json`, có hash trong LOG trước khi phát.
5. Mục lỗi 10/50/99% (luật 21) của T-071 đã được phiên điều phối soát.

### Sửa so với bản 4 (ngoài các sửa đã có ở `thong-nhat.md` §1)

| # | Bản 4 / thong-nhat | Bản 5 | Vì sao | Loại |
|---|---|---|---|---|
| C1 | E6 "khi exp-app rảnh" | E6 chỉ **sau E5**; từ lúc chụp mốc ở E1 tới hết E5 không khôi phục hay sửa DB (trừ E1) | exp-app "nghỉ" ở E3 (bản 4 §2.4); khôi phục DB lúc đó làm E2 và E4 khác trạng thái DB, mất phép so độ trôi đã thống nhất (Q3) | sửa nhỏ (thứ tự) |
| C2 | I1–I6 | Thêm I7–I15 (`HOP-DONG.md`) | Các rủi ro dẫm chân tìm thấy khi đọc code (danh sách ở LOG phiên 1) | sửa nhỏ (hợp đồng) |
| C3 | E1: đồng bộ ngày, chụp mốc | Thêm kiểm chỉ đọc sức chứa vé (`configured_capacity`, `held`, `purchased` của ticket type tải) so với nhu cầu E2+E4+E5; thiếu thì **lỗi chặn E2**, trình Minh | Chưa ai kiểm; vé hết thì hành trình mua lỗi, giờ "khỏe" sai. Nâng sức chứa là sửa dữ liệu, thuộc Minh | sửa nhỏ (thiếu bước kiểm) |
| C4 | Phương án B/C: mặt trái 14 lượt, M1 chạy kèm | Thêm: runner xếp `stage_m1` + `xuat_bo_sung` (truy vấn Prometheus sống) chạy **trong chu kỳ đo kế tiếp**, trái I3; và `inj3` dò exp-app mỗi chu kỳ | `runner4.py` `m1_worker` chờ t+PHASE+150 rồi stage trong lúc chu kỳ sau chạy | thông tin thêm cho R7, không đổi phương án |
| C5 | llm-w8 "Bắt đầu: Q6 duyệt" | Giữ; thêm: chọn nhà cung cấp LLM là gửi dữ liệu ca ra ngoài (R3) | AGENTS, quyền gửi ra ngoài | làm rõ |
| C6 | Grafana chỉ đổi ở E3 | Thêm khung Grafana ở E5 cho W5 (đổi nguồn JSON hiển thị) | W5 tiêu chí "kiểm dashboard hiện hành, lưu trữ và phát lại khi đổi nguồn JSON" | sửa nhỏ (khung giờ) |
| C7 | "nhánh hoặc checkout riêng" | Repo RCA: mọi phiên dùng chung checkout `D:\RCA-flashticket` (không worktree), vì T-069, gói bàn giao và hồ sơ T-070–T-075 chưa commit. Repo lab: mỗi phiên viết code dùng `git worktree` riêng | Worktree từ nhánh sẽ thiếu file chưa commit; một checkout lab dùng chung sẽ bị đổi nhánh chéo | sửa nhỏ (phân chia thư mục) |
| C8 | I6 "lần lượt từng phiên" | Dòng STATE: mỗi phiên chỉ sửa dòng mình bằng công cụ Edit (đọc lại ngay trước khi sửa); không dùng Write với file chung | Edit báo lỗi khi file đổi sau lần đọc, chặn ghi đè lẫn nhau | sửa nhỏ |
| C9 | README §2: "không còn lịch nào" | Danh sách lịch 20/11 12:4xZ có `m1ft-tiep-nhan`, **đang tắt**, chạy lần cuối 15/11. Không đụng (xóa là của Minh) | Lệch README nhưng không ảnh hưởng an toàn | ghi nhận |
| C10 | Cổng E2 rải ở nhiều nơi | Gom thành 5 điều kiện ở trên | Tránh phát E2 khi thiếu một điều kiện | sửa nhỏ |

### Ba điểm Codex CHẶN ở bản 4 (`thong-nhat.md` §2): xử lý

1. **Lịch tự tiếp nhận:** thiết kế hai nhánh ở mục "Thức và tiếp nhận" dưới. Cấu hình cụ thể **chờ Minh (R6)**. Không bật lịch nào trước khi Minh duyệt. Chặn: chỉ việc bật lịch, không chặn phần khác.
2. **Ai chạy lượt kế tiếp khi laptop mất mạng:** **chờ Minh (R7)**. Đề xuất ở LOG phiên 1. Chặn: E2, E4.
3. **Dữ liệu và mẫu số W4:** giao T-072 và T-071 giải trước E2 (cổng E2 điều kiện 3). Chặn: E2.

### Thức và tiếp nhận

- Chính: (1) mỗi phiên con khi xong lượt, ứng dụng báo về phiên điều phối kèm tên và mã; (2) mỗi job server có lệnh nền theo dõi trên laptop, thoát khi job tới trạng thái cuối; (3) mỗi job Codex nền có mã việc và thread ID trong `TRANG-THAI.json`.
- Mỗi lần thức: đọc `TRANG-THAI.json`, xét việc độc lập đủ điều kiện để phát, rồi mới chờ tiếp.
- Dự phòng (**chờ Minh, R6**): lịch dò định kỳ (đề xuất 15 phút khi có job server đang chạy) chỉ đọc `TRANG-THAI.json`. Nhánh 1, phiên điều phối còn sống: báo đúng mã việc cần xử lý. Nhánh 2, phiên điều phối đã dừng (không hoạt động quá 2 chu kỳ và không còn lệnh nền theo dõi): phiên do lịch mở kiểm chủ cũ và lệnh nền, ghi "nhận quyền điều phối" vào LOG T-070 **một lần** (khóa bằng trường `nguoi_giu` trong `TRANG-THAI.json`), tiếp từ checkpoint theo mục "Khi gián đoạn". Lịch cần ứng dụng Claude đang mở và có mạng; `list_task_runs` chỉ xác nhận lịch đã chạy.

### Khi gián đoạn

Trước khi phát lại bất cứ gì: kiểm tag trên máy tải, container, nhật ký runner/bộ chuỗi, manifest; nhận lại đầu ra đã xong. Không gọi lại nguyên lịch runner; chỉ lịch con cho phần thiếu. Chưa rõ trạng thái thì giữ job, làm việc độc lập. Lỗi một lượt chỉ hỏng lượt đó; sai luật, sai cấu hình, mất telemetry, Prometheus khởi động lại có thể hỏng nhiều lượt. Chạy lại khi tính đúng đòi hỏi.

## Đầu vào

`docs/techstack/ban-giao-dieu-phoi-2026-11-20/` (manifest `SHA256SUMS`, 19 file khớp 20/11); `tasks/T-069-v082-ban-ghim/`, `results/T-069/` (`SHA256SUMS` 318, `SHA256SUMS-2` 348 file khớp 20/11); kế hoạch giai đoạn 2 §8; repo lab `D:/Project/flashticket-rca-lab` commit `407b4f5` (cây sạch); FlashTicket `D:/Project/flash-ticket-platform` revision `36a3725d`.

## Đầu ra

- `tasks/T-070-dieu-phoi-giai-doan-2/`: SPEC (file này), `LOG.md`, `TRANG-THAI.json`, `LICH-MAY.md`, `HOP-DONG.md`.
- SPEC và LOG khởi tạo của T-071–T-075.
- Bản nháp báo nhóm FlashTicket (Q8) ở `results/T-070/nhap-bao-flashticket.md` (chỉ soạn; gửi là của Minh, R3).

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-070 trong `docs/STATE.md`:
- `tasks/T-070-dieu-phoi-giai-doan-2/`, `results/T-070/`.
- Tạo mới `tasks/T-071…T-075/` (SPEC, LOG khởi tạo); sau đó SPEC khóa, LOG thuộc người làm từng task.
- `tasks/T-069-v082-ban-ghim/LOG.md`: chỉ dòng đính chính hash (`thong-nhat.md` §1.1).
- Không chạy máy. Không ghi DECISIONS, WHY, MRP, LESSONS, AGENTS trước khi Minh duyệt (R2).

## Tiêu chí xong

1. Các phiên T-071–T-074 (và T-075 khi Minh duyệt) đã mở, mỗi phiên có SPEC; không có hai chủ cùng máy/dịch vụ trong một khung; mọi lần giao máy ghi ở `LICH-MAY.md`.
2. W4, W5 đạt tiêu chí xong trong SPEC của chúng hoặc dừng có lý do; W8 ở mức Minh chọn; W9a diễn tập 2 lần không lỗi (kế hoạch §8.2).
3. `TRANG-THAI.json` đủ để phiên khác tiếp nhận: mỗi việc có mã slot/tag, phiên chủ, lệnh đã phát, revision, máy, nơi đầu ra, hash, lần kiểm cuối, bước tiếp.
4. Bất đồng và quyết định chờ Minh được gom và trình; không tự quyết mục R1–R8.

## Không làm

Sửa lõi M1/V082, bộ tải, runner chung (R4); mở dữ liệu khóa; thử tải tối đa (Q5 hoãn); phép tách DB khỏi code (chỉ khi W6 cần); bật lại lịch M1 cũ; commit/push (R2); gửi nội dung ra ngoài (R3).

## Chi phí ước lượng

Phiên điều phối: không giờ máy. Bốn phiên làm việc High chạy song song (Minh yêu cầu multi-session; luật cứng 8 đã được Minh nêu rõ ở yêu cầu này). Lượt dài E2, E4 (~7 giờ mỗi khoảng) trình riêng theo luật 8 và 21 (R7).

## Rủi ro và điều chưa chắc

- Trạng thái máy chỉ theo bằng chứng 19/11 20:45Z và 20/11 02:31Z (README §2); **chưa xác minh hiện tại** — T-071 kiểm khi mở khung S0 (chỉ đọc) trước mọi thay đổi.
- Hiệu quả song song phụ thuộc usage của account; hết usage là một tình trạng riêng, báo Minh.
- Nhiều phiên chung một checkout repo RCA: dựa vào kỷ luật ghi file (I10); không có khóa cưỡng chế ngoài cơ chế Edit.

## Prompt bàn giao

Ở `LOG.md`, mục cuối mỗi lượt.

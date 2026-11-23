# Đề xuất gom việc chờ Minh quyết — bản 2 (sau phản biện Codex CX-22, CX-22b)

23/11/2026, điều phối T-070. Bản 1: `de-xuat-quyet-2026-11-23.md` (giữ nguyên). Phản biện: `results/T-070/codex/CX-22-tin-cuoi.md`, `CX-22b-tin-cuoi.md`.

**Bỏ cơ chế "mục không phản đối coi như duyệt"** của bản 1 (trái Luật 0, CX-22 G1). Minh duyệt bằng câu rõ ràng; có thể duyệt nhiều mục một lần bằng số mục.

## 0. Điều phối tự sửa, không cần Minh (đã có quyền)

| # | Việc | Nguồn |
|---|---|---|
| 0.1 | Đồng bộ `TRANG-THAI.json` theo trạng thái thật (S4 đang mở, `/opt/rca-lab` ở E5, dịch vụ T-073 còn chạy) | CX-22 "Lượt 9" |
| 0.2 | Soạn bản nháp báo nhóm FlashTicket (Q8) `results/T-070/nhap-bao-flashticket.md` — đầu ra SPEC T-070 chưa làm; chỉ soạn, gửi là của Minh (R3) | CX-22 |
| 0.3 | Bỏ "phân tích trôi p95" khỏi danh sách chờ Minh (đã làm xong, `results/T-072/troi-p95-e2-e4.md`) | CX-22 |
| 0.4 | Bỏ A2 bản 1 (để nguyên H đã nằm trong §5 bước 6) | CX-22, CX-22b |
| 0.5 | Từ nay: thao tác trên máy (kể cả `git fetch`) giao cho chủ khung; điều phối chỉ nhận SHA. Lỗi nhỏ: Codex sửa, phiên Codex khác kiểm (đúng yêu cầu Minh 22/11) | CX-22, CX-22b |
| 0.6 | Ghi nhận (không đổi kết quả E5): lượt 2 T-073 dùng subagent; điều phối đã `git fetch` trên exp-obs ngày 23/11 01:40Z (chỉ cập nhật ref) | CX-22 |

## 1. Cần Minh duyệt rõ (đề xuất của điều phối)

| # | Đề xuất | Thay đổi so với bản 1 / lý do |
|---|---|---|
| **A1** | Trước khi trả máy: T-073 (chủ S4) chép về laptop, kèm sha256, các file của ca `7577dd5b` mà B3 cần (gói bổ sung, `prometheus.json`, đầu ra V082). Sau đó hoàn tác theo §5: đặt `STOP`, chờ ca đang chạy kết thúc, dừng đúng tiến trình `orchestrator.py`, kiểm I7, checkout H `1bb40ca`, restart Grafana, kiểm còn đúng một integration T-072 + 11 luật + nguồn dashboard cũ, gỡ `t073-webhook`. **Giữ** bộ nhận `t072-bo-nhan` (H còn trỏ vào). Xóa 3 thư mục Grafana rỗng **theo UID hiện tại**, chỉ khi `counts` (dashboard, thư mục con, luật, tài nguyên khác) đều 0 ngay trước khi xóa; thư mục nào có nội dung thì bỏ khỏi lệnh. Rồi điều phối đóng S4 | CX-22 A1, B3: H chưa chạy trên máy; laptop thiếu file thô cho B3 |
| **B1** | Chốt tên hợp đồng G1 của chế độ (b) là `G1 0.5 + che_do_b b-1` (đúng dữ liệu đã phát); đính chính tham chiếu "0.3" ở KE-HOACH §8.2, SPEC T-073, SPEC T-075; giữ bản khóa lịch sử | CX-22 B1 |
| **B3** | T-073 đáp CX-21/21b trên file đã chép ở A1 (không máy), gồm luôn chữ mục WHY cho hai ngưỡng phủ (trình Minh duyệt chữ trước khi ghi). Đính chính bằng file mới, không sửa file đã ghim hash | Gộp B2 vào B3 (CX-22) |
| **B4** | Nhận ngay kết quả chức năng E5: một ô `PAUSE-PAYMENT`, tải ×1, ca hiện trên giao diện 898,8 s sau t̂ (< 25 phút; API 886,8 s), tiêu chí (a)–(d) đạt, "đã hiển thị nhưng thiếu phủ" metric Payment. Nghiệm thu toàn hồ sơ T-073 sau B1, B3 | CX-22 B4 |
| **B5** | Không giao sửa code `live-down` lúc này. SPEC W9a quyết: demo có bấm liên kết đó không; nếu có, trình file ghim cần đổi và tác dụng trên ca demo mới; nếu không, ghi giới hạn và bỏ thao tác bấm | CX-22 B5 |
| **C1** | Nhận ngay số đo R5: 0 sự cố / 383 phút khỏe ×1, cận trên Poisson 95% 3,47/6 giờ. Giới hạn: 7/11 luật chưa kiểm dương; "luật 5xx chưa bị thử" chỉ đúng trên E4 (E5 đã có `t072-loi-payment`); rủi ro ticket là ước lượng mô hình. Chốt hồ sơ W4 sau C2–C3 | CX-22 C1 |
| **C2** | T-071, T-072 đáp CX-19/19b. Sửa **hai** script (`cham_offline.py`, `e4_giai_thich_khac.py`) bằng phiên bản mới, đầu ra riêng, tự ghi hash của chính code chạy; kiểm các nhánh bằng dữ liệu giả; luật `<8` xét cả cửa sổ duy trì; `chon-nguong` trả mã lỗi khi thiếu route. Không ghi đè `e4/giai-thich-khac.json` đã ghim; giữ phép chấm E4 đầu | CX-22 C2, CX-22b (chặn ghi đè) |
| **C3** | Sửa hai lập luận WHY-110 (T-072 soạn chữ, Minh duyệt chữ) | — |
| **C4** | Không chạy khoảng khỏe ≥ 6 giờ riêng. Dùng phút ×1 đủ điều kiện, cùng cấu hình, có Grafana đánh giá của W7, công bố thời lượng thực; theo dõi tỷ lệ request chậm ticket. Không hứa W7 phân xử được nguyên nhân DB | CX-22 C4 sửa lời hứa |
| **C5** | Thử "chạy tải ≥ 5 phút trước phần phát hiện" trong hai lần diễn tập W9a; ghi tác dụng còn chưa kiểm | — |
| **D1** | Nghiệm thu T-069 với ngoại lệ CPU-BOOK-1 (R1); nguyên nhân mẫu đuôi còn mở | CX-22b D1 |
| **D2** | T-066: giữ 2.6; 2.7 tách script phục hồi được khỏi hai script chưa kiểm, chưa xóa; sửa dòng STATE "xóa sau T-067"; người làm đáp CX-13/13b rồi nghiệm thu kỹ thuật W1 | — |
| **D3** | T-068: giữ nội dung `service-graph-4-bak` và kết quả kiểm ca `7ffb2305` (không chỉ giữ hash); người làm đáp CX-14/14b; chỉ chữ sửa WHY-101 cần Minh duyệt mới | CX-22 D3 |
| **E1** | T-074 làm bản 4 (11 điểm CX-15/15b + RQ3d) **kèm phần E6 cụ thể** (giá trị đích hạn bán + sức chứa theo R9, phạm vi DB, khôi phục, kiểm nhất quán) và **một** danh sách quyết định W6 (bỏ câu đã có quyết định), trong đó Q-W6-07 đề xuất M4 + BARO, bỏ số 0,80 làm căn cứ, ghi mặt trái thiếu đối chiếu trace độc lập. Codex hai phiên kiểm. Minh duyệt bản 4 + E6 một lần | Gộp E1–E3 (CX-22) |
| **F1** | W8 mức demo: chạy trên ca W5, dẫn trường bằng chứng, được trả lời "không đủ bằng chứng", giữ nguyên thứ hạng; chất lượng nhiều ca còn mở | — |
| **F2** | Minh chọn: (i) dùng API thật — Minh nêu nhà cung cấp và model, duyệt danh sách trường gửi đi (ứng viên: dịch vụ, thứ hạng, bằng chứng đã tính; **loại** sổ tiêm, đáp án, đường dẫn nhận diện ca), Minh tự cấp khóa; hoặc (ii) trước mắt chỉ chuẩn bị khuôn và kiểm trích dẫn ngoại tuyến bằng ca giả (chưa đạt tiêu chí W8) | CX-22 F2: R3 đang cấm gửi ra ngoài |
| **F3** | Điều phối soạn SPEC W9a trong chat ngay (kịch bản, video, phát lại, hai lần diễn tập, cách bật lại dịch vụ với vùng ghi mới, xử lý `live-down`); Minh duyệt rồi mới tạo file | CX-22 F3 |
| **F4** | Thứ tự máy: nếu W9a sẵn trước E6, cho diễn tập E7 trước E6 khi máy rảnh (SPEC T-070 đang ghi E6 → E7; E6 ngoài đường găng W9a) | CX-22b mới |
| **G1** | Ghi DECISIONS đúng nguyên văn khối dưới (§2), chỉ phần Minh duyệt | CX-22 G1 |
| **G2** | Thực hiện R2(b) đã duyệt 20/11 (commit + push T-069, gói bàn giao `docs/techstack/ban-giao-dieu-phoi-2026-11-20/`, hồ sơ T-070…T-075): điều phối trình danh sách file/hunk thuộc R2(b), tách phần phát sinh sau (DECISIONS/WHY/STATE/KE-HOACH, LOG T-067/T-068) và **không** đụng các thư mục `results/T-032…T-065` chưa track | CX-22 G2 |

## 2. Khối DECISIONS đề xuất (ghi phần Minh duyệt)

> **23/11/2026 — Minh (chat).**
> - Duyệt commit và push gói E5/P/H repo lab: `t073-e5` `81a92736…`, `t073-e5-p` `779f90c9…`, `t073-e5-h` `1bb40ca4…`, theo `results/T-073/trien-khai-e5.md` bản `0befa4d0…`, sau phản biện CX-16…CX-20.
> - [các mục A1, B1, B4, C1, … Minh duyệt, chép nguyên câu đề xuất ở §1].

## 3. Luồng chạy sau khi duyệt

1. 0.1, 0.2 (điều phối, ngay). A1 (T-073, máy) ∥ C2 (T-071, T-072, không máy) ∥ E1 (T-074, không máy) ∥ F3 (điều phối soạn SPEC W9a).
2. B3 sau A1. Mỗi lượt đáp có Codex kiểm (hai phiên khi là phản biện chính thức).
3. G1 ngay khi Minh duyệt; G2 khi Minh duyệt danh sách file.
4. W8 theo F2. E6 khi Minh duyệt bản 4 + E6. E7 theo F4.

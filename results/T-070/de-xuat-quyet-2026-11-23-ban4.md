# Đề xuất gom việc — bản 4 (sau Codex CX-23)

23/11/2026, điều phối T-070. Bản 1–3 giữ nguyên. Phản biện: `results/T-070/codex/CX-22*`, `CX-23-tin-cuoi.md`. Điều phối đồng ý mọi điểm CX-23, không có bất đồng.

**Sửa cách hiểu câu duyệt của Minh** ("duyệt sửa sau khi 2 bên đã thống nhất…"): câu này duyệt **các sửa đổi đề xuất** khi hai bên thống nhất, **không** duyệt chạy máy, nghiệm thu hay đổi lịch (CX-23). Vì vậy bản 4 tách ba nhóm: (1) sửa đã thống nhất, làm ngay; (2) quyết định còn lại, trình Minh một lần; (3) việc đã có quyền từ trước.

## 1. Sửa đã thống nhất — điều phối đã làm

| Việc | Trạng thái |
|---|---|
| `TRANG-THAI.json`: `phien_ban.exp_obs_opt_rca_lab` = E5 `81a9273` (trạng thái cuối đã báo; chủ S4 kiểm thực tế), thêm SHA E5/P/H, bước tiếp | xong |
| Dòng T-070 trong `docs/STATE.md` cập nhật theo E2–E5 | xong |
| Nháp báo FlashTicket bản 2 (`nhap-bao-flashticket.md`; bản 1 giữ `.ban1.md`): tiêu đề "độ trễ trung vị tăng giữa hai đợt đo", tách `EXPLAIN` Booking khỏi thống kê Ticket, câu CPU theo ô (`dinh-chinh-2.md` §3) | xong; gửi hay không là của Minh |
| Ghi vào đầu vào W8/W9a: không dùng chú thích "Hash do chỉ mục T-064 cấp" trên ca `t073-b` (sai, `e5-ket-qua.md` dòng 75); dẫn đúng nguồn thật | ghi trong mục F3 dưới |
| C5: thử khởi tải ≥ 5 phút trong hai lần diễn tập, **giữ** cả cảnh báo đầu lượt | ghi trong F3 |

## 2. Quyết định trình Minh (một lần; Minh trả lời bằng số mục)

| # | Đề xuất của điều phối (Codex đồng ý hướng) | Mặt trái |
|---|---|---|
| **Q1 (A1)** | Cho T-073 (chủ S4): chép về laptop file ca `7577dd5b` mà B3 cần (gói bổ sung, `prometheus.json`, đầu ra V082 gồm chú thích H5, inventory dùng ánh xạ) kèm sha256; rồi hoàn tác §5 (STOP, chờ ca đang chạy xong, dừng đúng tiến trình, I7, checkout H `1bb40ca`, restart Grafana, kiểm một integration T-072 + 11 luật + nguồn dashboard cũ, gỡ `t073-webhook`, **giữ** `t072-bo-nhan`); xóa 3 thư mục Grafana rỗng theo UID chỉ khi `counts` toàn 0 ngay trước khi xóa; điều phối đóng S4 | Diễn tập W9a phải bật lại dịch vụ với vùng ghi mới (~30 phút) |
| **Q2 (B4, C1)** | Nhận ngay: (a) R5 trên E4: 0 sự cố / 383 phút khỏe ×1, cận trên Poisson 95% 3,47/6 giờ; (b) chức năng E5 một ô `PAUSE-PAYMENT` ×1: ca hiện ≤ 898,8 s sau t̂ (< 25 phút), tiêu chí (a)–(d) đạt, thiếu phủ metric Payment. Chốt hồ sơ W4/W5 sau các lượt đáp | — |
| **Q3 (B1)** | Tên hợp đồng G1 chế độ (b): `G1 0.5 + che_do_b b-1`; Codex soạn chữ đính chính cho KE-HOACH §8.2, SPEC T-073, SPEC T-075; Minh duyệt chữ rồi mới áp | Hồ sơ cũ nhắc "0.3" cần đính chính |
| **Q4 (D1)** | Nghiệm thu T-069 với ngoại lệ CPU-BOOK-1 (R1); nguồn mẫu đuôi còn mở (DB, image, tải CPU cùng đổi) | — |
| **Q5 (D2, D3)** | T-066: giữ 2.6, tách script 2.7, chưa xóa; T-068: giữ nội dung bản hoàn tác và hiện vật ca `7ffb2305`. Cho người làm T-066, T-068 đáp phản biện, ghi LOG, file đính chính mới và **dòng STATE** của task mình | — |
| **Q6 (F1)** | W8 mức demo: chạy trên ca W5, dẫn trường bằng chứng, được trả lời "không đủ bằng chứng", gợi ý bước xử lý (yêu cầu của cô), giữ nguyên thứ hạng | Chất lượng giải thích nhiều ca còn mở |
| **Q7 (F2)** | Nhánh (ii) ngay: T-075 soạn khuôn và kiểm trích dẫn ngoại tuyến bằng ca giả (không gửi gì ra ngoài). Để đạt W8, Minh chọn nhánh (i): nhà cung cấp + model + duyệt danh sách trường gửi đi (ứng viên: dịch vụ, thứ hạng, bằng chứng đã tính; loại sổ tiêm, đáp án, đường dẫn nhận diện ca); Minh tự cấp khóa | (ii) chưa đạt tiêu chí W8 |
| **Q8 (E1, E3)** | T-074 soạn bản 4 W6 **và SPEC bổ sung E6** (phạm vi DB, đích hạn bán + sức chứa theo R9, khôi phục, kiểm nhất quán, quyền máy S5) để Minh duyệt một lần sau hai phiên Codex | — |
| **Q9 (F4)** | Nếu W5, W8 sẵn và S4 đã trả trước khi E6 được duyệt, cho diễn tập E7 trước E6 khi máy rảnh; nếu không, giữ thứ tự SPEC (E6 → E7) | Đổi thứ tự so SPEC T-070 |
| **Q10 (G1)** | Ghi DECISIONS khối 23/11 gồm dòng duyệt E5/P/H (nguyên văn ở bản 2 §2) và nguyên câu các mục Q1–Q9 Minh duyệt | — |
| **Q11 (G2)** | Commit + push phần R2(b) (T-069, gói bàn giao, hồ sơ T-070…T-075) theo danh sách file Codex CX-28 lập và điều phối kiểm; căn cứ push: AGENTS luật 11 ("Minh duyệt thì commit và push"). Phần phát sinh sau R2(b) (DECISIONS/WHY/STATE/KE-HOACH, LOG T-067/T-068) trình riêng trong cùng danh sách | — |

## 3. Việc chạy ngay không cần duyệt thêm (trong quyền đã có)

| Việc | Ai | Vùng ghi | Kiểm |
|---|---|---|---|
| **CX-28** liệt kê file/hunk R2(b), tách phần phát sinh | Codex, chỉ đọc | trả lời → điều phối lưu `results/T-070/codex/` | điều phối |
| **CX-26** soạn chữ đính chính G1 (cho Q3) | Codex | file mới `results/T-070/nhap-dinh-chinh-g1.md` | Codex CX-26b |
| **CX-25** đính chính **cơ học** W4: giờ hiệu lực E4 = 06:06:10Z (mốc nhóm truy vấn sau health), phạm vi B2 = 12 container có chuỗi restart | Codex | file mới `results/T-072/dinh-chinh-cx19-co-hoc.md`, `results/T-071/dinh-chinh-cx19-co-hoc.md` | Codex CX-25b |
| **CX-24** phần **cơ học** bộ chấm v2: luật `<8` dùng max trong từng cửa sổ, cờ giao khoảng hệ thống/quan sát, `chon-nguong` thoát khác 0 kèm tên route thiếu; ca giả cho các nhánh; v2 đọc cấu hình ghim đúng nơi, nạp đúng bộ chấm v2, ghi đầu ra + hash riêng | Codex | chỉ file mới trong `results/T-072/v2/` | Codex CX-24b |
| Phần **khó** bộ chấm: xác định đầu khoảng chấm và bằng chứng cháy từ trước (`quy_ve()`, Pending, ca `t0+60`); diễn giải câu −4 s (chỉ trên bốn luật thử); đáp CX-19/19b; chữ sửa WHY-110 | Claude T-072 (T-071 phần B2/K1 của mình) | LOG T-071/T-072; file mới trong `results/T-072/v2/` **sau** CX-24b | Codex hai phiên |
| SPEC W9a soạn trong chat (kịch bản, video, phát lại, hai diễn tập, bật lại dịch vụ với nguồn dashboard mới — commit E5 ghim `t073-e5-001` nên cần commit/nguồn mới; xử lý `live-down`; chú thích hash T-064; khởi tải ≥ 5 phút giữ cảnh báo đầu lượt) | Claude điều phối | chat | Codex |
| W6 bản 4 + SPEC E6 (sau Q8 hay soạn ngay — soạn là trong quyền T-074) | Claude T-074 | `results/T-074/*-4.*` | Codex hai phiên |

**Không dẫm chân:** Codex workspace-write (CX-26 → CX-25 → CX-24) chạy lần lượt, chỉ tạo file mới, kiểm `git status` trước/sau; Claude T-072 không ghi `results/T-072/v2/` tới khi CX-24b xong; chỉ T-073 đụng máy (sau Q1). Kiểm chéo kỹ thuật CX-24b/25b/26b **không** thay phản biện chính thức của phần Codex viết: phần T-072 dùng v2 vẫn qua lượt phản biện chính thức sau.

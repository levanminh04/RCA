# Toàn bộ việc chờ Minh duyệt — 23/11/2026 chiều (điều phối T-070)

Lập lúc ~11:40Z. Mỗi mục: đề xuất của điều phối, lý do, mặt trái. Minh trả lời bằng số mục (ví dụ "duyệt 1–9, 12 theo đề xuất; 10 chọn B"). Mục có dấu **(sau Codex)** chỉ chốt khi lượt Codex kiểm lại đang chạy không còn bất đồng; nếu còn, điều phối trình lại.

## A. Commit repo RCA (thực hiện Q11 đã duyệt)

| # | Việc chờ | Đề xuất | Lý do | Mặt trái |
|---|---|---|---|---|
| 1 | 3 file `results/T-069/thu/*/tai-out/*/raw.json` (199 MB, 60–78 MB/file) | **Không đưa vào git**; chép sang `D:/RCA-archive/T-069/raw-json/` kèm danh sách sha256 (đã có trong `results/T-069/SHA256SUMS-2`) | AGENTS §4, §12: dữ liệu lớn ngoài git, lưu ở `D:/RCA-archive/` kèm sha256; commit còn ~60 MB | Máy mới phải lấy 3 file từ archive để kiểm đủ manifest T-069 |
| 2 | `results/T-073/e5/ca-7577dd5b/…/method-input.json` (29 MB) | **Đưa vào git** | Dưới 50 MB; là đầu vào để tái lập phân tích ca E5 (H5, phủ) | Repo tăng 29 MB |
| 3 | 3 script đã ghim có đường dẫn file khóa (`results/T-069/xac-nhan/xac_nhan_ca.py`, `xac_nhan_ca_3.py`, `results/T-072/e3/b7-cho.sh`) | **Đưa vào git** | Chỉ là đường dẫn, không có khóa; AGENTS.md đã ghi thư mục khóa; bỏ ra thì máy mới không kiểm đủ manifest T-069, E3 | Lộ tên file khóa trên repo riêng tư |
| 4 | 43+ nhật ký thô Codex `results/T-070/codex/CX-*.jsonl` | **Không đưa vào git**, giữ trên laptop | Nhật ký terminal lớn, có lệnh SSH/đường dẫn; brief và `*-tin-cuoi.md` đã đủ làm bằng chứng | Không xem lại được từng lệnh Codex từ git |
| 5 | 2 dòng `KE-HOACH-GIAI-DOAN-2.md` ngày 19/11 (ngày demo chưa chốt, không chặn lịch; nhiều phiên Claude, tách giờ exp-app, W5 song song W3) — CX-28 không tìm thấy dòng duyệt | **Minh xác nhận** đây là ý của Minh 19/11 → đưa vào commit; nếu không, điều phối bỏ riêng hai dòng | Trùng ý Minh đã ghi ở LICH-MAY ("ngày demo không phải điểm chặn", 19/11) và gói bàn giao (nhiều phiên) | — |
| 6 | Thời điểm commit | **Commit ngay** khi các phiên Claude đang rảnh (hiện rảnh); Codex chỉ đọc, chỉ thêm `*-tin-cuoi.md` sau → commit bổ sung sau | Tránh chụp file đang ghi | Có thêm một commit nhỏ sau |

## B. W4 (T-071, T-072)

| # | Việc chờ | Đề xuất |
|---|---|---|
| 7 | Chữ sửa WHY-110 (T-072, `results/T-072/dap-cx19.md` §4): giữ quyết định/công thức/ngưỡng; sửa lý do "khi và chỉ khi" (luật 5xx chỉ là điều kiện đủ), sửa hai phương án đã xét (chọn trên E2 theo R5 không làm E4 mất độc lập — lý do loại thật là R5 không xác định duy nhất θ), thêm điều kiện thất bại (−4 s chỉ trên bốn luật thử), thêm bằng chứng sau khi dùng (E4 0/383; tỷ lệ max S/θ) | **Duyệt (sau Codex CX-33)** |
| 8 | Dùng bộ chấm v2 (`results/T-072/v2/`: phần cơ học Codex + `cham_offline_v2_claude.py`) cho các lần chấm sau (W6/W7); **không** chấm lại E4 | **Duyệt (sau Codex CX-33/33b)** |
| 9 | Chốt hồ sơ W4: R5 đạt (đã nhận Q2) + giới hạn: 7/11 luật chưa kiểm dương, ticket dễ báo động giả, độ tin thấp | **Nghiệm thu T-071, T-072 (sau CX-33/33b)** |

## C. W5 (T-073)

| # | Việc chờ | Đề xuất |
|---|---|---|
| 10 | Chốt hồ sơ W5: chức năng E5 đạt (đã nhận Q2), phủ thiếu do chính lỗi pause, H5 không bắt Payment ở chế độ (b) (câu hỏi cho W6), đính chính e5-1/e5-2 | **Nghiệm thu T-073 (sau Codex CX-31/31b)** |
| 11 | Thư mục Grafana còn sót "T-072 E3 thử (gỡ trước E4)" | **Xóa nếu `counts` toàn 0**, làm ở lần đăng nhập Grafana tới (W9a), giao chủ khung lúc đó, kiểm theo UID như Q1 | 
| 12 | Liên kết `live-down` hỏng và chú thích "Hash do chỉ mục T-064 cấp" sai (chuỗi cố định trong `sau_v082.dung_mot_ca`) | **Sửa trước W9a** bằng một commit lab mới (file ghim T-067 → ghi rõ đổi hash), T-073 soạn, Codex kiểm, Minh duyệt commit; nếu không kịp thì kịch bản demo bỏ thao tác bấm và ghi giới hạn |

## D. W6 / E6 (T-074) — sau Codex CX-32/32b

| # | Việc chờ | Đề xuất (theo T-074 bản 5) |
|---|---|---|
| 13 | A1: K0 hay K2 | **K0** (giữ DB tích lũy, trộn khối, 3 đối chứng BINH-THUONG ×1 làm mốc) — K2 thiếu quyền Redis và đường lui |
| 14 | A2: quyền máy E6 | **exp-app** chủ khung: chỉ sửa đúng dòng hạn bán/sức chứa đã duyệt, chụp mốc PostgreSQL, tạo `/home/ubuntu/t074/`; **exp-obs, máy tải** chỉ đọc; không runner, không tải, không Grafana/Prometheus |
| 15 | A3: giá trị đích | **Hạn bán 2026-12-30T22:16:31.402736Z**; diễn/check-in 31/12 → 01/01/2027; **sức chứa = `purchased` đọc ở bước 1 + 1,5 × nhu cầu cả đợt K0 của phương án B1, làm tròn lên nghìn** |
| 16 | A4: Redis/MongoDB | **Mốc chỉ PostgreSQL**, ghi giới hạn Redis (`NOAUTH`) và MongoDB `user-db` |
| 17 | B1: ô W7 | **Phương án A** (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE) + đối chứng làm mốc: 27 chu kỳ, 14,1 giờ, 35.640 đơn bảo thủ; CPU-EVENT là ứng viên khi có code tham số hóa + SPEC E6b |
| 18 | B2: dung sai ghép | **G = 370 s chính, 120 s báo phụ**; không kéo dài tải |
| 19 | B3: báo động giả ×3 | **Báo "sự cố trên giờ quan sát ×3 đủ điều kiện"**; câu báo động giả mỗi giờ khỏe ×3 để OPEN |
| 20 | B4: nhánh dự phòng khi che G-inst | **Hành vi P7: lỗi chạy, tính trượt** |
| 21 | B5: mốc độ trễ | **Độ trễ từ mốc tiêm theo lịch** + độ lệch bộ tiêm xác nhận; không thêm đầu dò onset |
| 22 | B6: baseline | **M4 (SimpleRCA) + BARO RobustScorer**; bỏ số 0,80 làm căn cứ; ca nhiều chuỗi runtime ghi `LOI_ADAPTER_DA_CHUOI`, tính trượt |
| 23 | B7: việc rẻ dùng lại dữ liệu | **Làm** (17 gói T-069; đếm khóa thứ hai; phân loại phút 10 phút đầu E4) khi có adapter W7 |
| 24 | N5 của T-073 (H5 không kích hoạt cho thành phần tạo ra t̂ ở chế độ (b)) | **Đưa vào câu hỏi mở của W6/W7** (T-074 ghi ở bản kế tiếp), không sửa V082 lúc này |

## E. W8 (T-075) — sau Codex CX-34/34b

| # | Việc chờ | Đề xuất |
|---|---|---|
| 25 | Phạm vi nghiệm thu: tính cả thử ngoại tuyến trên ca thật (E5, 2 ca G1 cũ) | **Có** — không gửi gì ra ngoài; tiêu chí W8 là chạy trên ca W5 |
| 26 | Danh sách trường gửi đi (`results/T-075/khuon-dau-vao.md` §3; loại §4) | **Duyệt danh sách §3** (không nhãn, đường dẫn, trace ID, log thô, giờ tuyệt đối); mặt trái: gửi tên service, thao tác SQL, tên luật |
| 27 | Nhà cung cấp/model | **A: Claude API, `claude-sonnet-5-5`** (rẻ hơn, đủ cho giải thích có lược đồ; T-075 đề xuất opus) với structured outputs, ~chục lần gọi; nếu Minh muốn dữ liệu ở tài khoản nhóm → B (Bedrock). **Minh tự nhập khóa API** |
| 28 | Khi đầu ra LLM trượt bộ kiểm | **Gọi lại 1 lần kèm lỗi; vẫn trượt thì hiện "Không đủ bằng chứng để giải thích tự động"**, không hiện câu chưa kiểm |

## F. Khác

| # | Việc chờ | Đề xuất |
|---|---|---|
| 29 | Gửi bản nháp báo nhóm FlashTicket (`results/T-070/nhap-bao-flashticket.md`, bản 2 đã sửa theo CX-23/23b) | **Minh đọc và tự gửi** nếu thấy có ích (R3); điều phối không gửi |
| 30 | Đáp phản biện T-066 (CX-13/13b) và T-068 (CX-14/14b) — Q5 đã cho phép người làm đáp | **Làm sau khi W6/W8 xong lượt kiểm**, vì usage Claude tuần đã 58% |
| 31 | Ghi LESSONS (bài học vận hành giai đoạn 2) | **Ghi 5 bài:** (i) chạy ≤ 2–3 phiên Claude song song, mỗi phiên ghi LOG từng bước con để cắt hạn mức không mất việc; (ii) không dùng `Start-Job` PowerShell 5.1 cho đầu ra JSON (ghi UTF-16 → chữ loạn); (iii) bộ dò "hết usage" phải dựa vào `turn.completed`, không khớp chữ; (iv) lệnh chờ hẹn giờ trong phiên bị mất khi phiên bị cắt — dùng lịch ngoài hoặc kiểm lại khi thức; (v) điều phối không tự thao tác máy (kể cả `git fetch`), giao chủ khung — Minh duyệt chữ trước khi ghi |
| 32 | Tắt/xóa lịch `t070-danh-thuc-dieu-phoi` (đang tắt) | **Giữ tắt**; bật lại khi Minh treo máy qua đêm |

## Tiếp theo (sau khi Minh duyệt)

1. Điều phối: commit + push repo RCA (mục 1–6); soạn SPEC W9a trình trong chat (đã nợ từ F3).
2. Codex (đang chạy lần lượt): CX-31/31b (T-073) → CX-32/32b (W6 bản 5) → CX-33/33b (W4) → CX-34/34b (T-075). Hết usage → báo Minh đổi tài khoản.
3. Khi CX-32 thống nhất và Minh duyệt mục 13–16: mở S5, T-074 chạy E6 nhánh K0 (sửa hạn bán + sức chứa, chụp mốc PostgreSQL).
4. Khi CX-34 thống nhất và Minh chọn mục 26–28 + nhập khóa: T-075 chạy LLM thật trên ca W5.
5. W9a: sau W5 (đã đạt chức năng) + W8 chạy được; diễn tập 2 lần; có thể trước E6 (Q9).
6. W7 (thu đánh giá): sau E6 + khóa W6 (mục 17–24).

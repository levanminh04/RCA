# Đề xuất gom mọi việc chờ Minh quyết — 23/11/2026 (điều phối T-070)

Mục đích: Minh duyệt một lần, điều phối chạy một luồng liên tục. Mỗi mục: đề xuất, lý do, mặt trái. Mục nào Minh không đồng ý thì ghi số mục; mục còn lại coi như duyệt **đúng nội dung ghi ở đây**.

## A. Máy và E5 (làm ngay)

| # | Đề xuất | Lý do | Mặt trái |
|---|---|---|---|
| A1 | Hoàn tác E5 theo §5 `trien-khai-e5.md` (dừng `orchestrator.py`, checkout H `1bb40ca`, restart Grafana, gỡ `t073-webhook`) **và xóa 3 thư mục Grafana rỗng** (`2026-11-12-g2-v6`, `2026-11-13-l3-p7`, `2026-11-14-l4-temporary`) sau khi kiểm chúng rỗng; đóng S4 | Đưa máy về trạng thái tương đương trước E5; dịch vụ sống sẽ sinh ca rác khi có cảnh báo ở việc máy sau; thư mục rỗng là phần dư do provider tạm P tạo, không ai dùng (giữ chỉ làm bẩn giao diện) | Diễn tập W9a phải triển khai lại (~30 phút, theo gói đã duyệt) |
| A2 | Sau A1, `/opt/rca-lab` ở H; lần đổi checkout tiếp theo chỉ khi có gói được duyệt (W6/W9a) | Không đổi máy ngoài kế hoạch | — |

## B. W5 (T-073)

| # | Đề xuất | Lý do | Mặt trái |
|---|---|---|---|
| B1 | Chốt tên hợp đồng G1 của chế độ (b) là **`G1 0.5 + b-1`** (thay "0.3" trong SPEC T-073), ghi DECISIONS | Ca E5 và dashboard thực tế dùng định dạng này (CX-21 N2); giữ "0.3" thì tiêu chí nghiệm thu không khớp dữ liệu | Hồ sơ cũ nhắc "0.3" cần một dòng đính chính |
| B2 | T-073 soạn mục WHY cho hai ngưỡng phủ (trace lỗ ≤ 30 s; metric lỗ ≤ 4 × bước), ghi đúng thời điểm đặt (trước E5) và căn cứ; Minh duyệt chữ trước khi ghi | Luật cứng 3; CX-21b xác nhận chưa có mục WHY | — |
| B3 | Giao T-073 đáp phản biện CX-21/CX-21b (prompt `CX-21-tin-cuoi.md` dòng 66–136): sửa lỗi nhỏ bằng **file đính chính** (không sửa file đã ghim hash), kiểm phạm vi đầu vào V082 và biên H5 trên gói đã lưu (không máy), ghi giới hạn hai trang L4 và mốc `fault-stop`; bổ sung bàn giao LOG/STATE | Đóng hồ sơ E5; mọi phép kiểm dùng dữ liệu đã lưu | Một lượt Claude + một lượt Codex kiểm lại |
| B4 | Sau B3: **nghiệm thu W5 chức năng** với giới hạn ghi rõ: một ô, tải ×1, "đã hiển thị nhưng thiếu phủ" metric payment, không đánh giá độ chính xác RCA | Hai phiên Codex chấp nhận; không tiêm lại | — |
| B5 | Sửa lỗi liên kết `live-down` của G1 (CX-13b) bằng commit lab mới **trước W9a**, giao T-073 làm cùng chuẩn bị W9a; Codex kiểm; Minh duyệt commit | Demo sẽ bấm vào liên kết hỏng | Thêm một commit lab |

## C. W4 (T-071, T-072)

| # | Đề xuất | Lý do | Mặt trái |
|---|---|---|---|
| C1 | **Nghiệm thu R5/W4**: đạt theo phép so đã khai (0 sự cố / 383 phút khỏe ×1), kèm giới hạn: độ tin thấp (CI 95% tới 3,47/6 giờ), 7/11 luật chưa kiểm dương, luật 5xx chưa bị thử, ticket dễ báo động giả | Hai phiên Codex chấp nhận; tái lập được | — |
| C2 | Giao T-071, T-072 đáp CX-19/CX-19b: đính chính giờ hiệu lực E4 06:06:10Z (F1), câu lệch −4 s (F2), lập luận luật 5xx (N2), phạm vi B2 (F4); sửa `cham_offline.py` ba nhánh khi có cảnh báo (F5) và mã thoát `chon-nguong` khi thiếu route (N1) — code trong `results/T-072/`, giữ bản cũ, không chấm lại E4 | Không đổi kết quả E4; cần trước khi dùng bộ chấm cho ca có sự cố (W6/W7) | Một lượt Claude mỗi task + Codex kiểm |
| C3 | Sửa câu tính độc lập trong WHY-110 theo CX-19 F3 (T-072 soạn chữ, Minh duyệt) | Lập luận hiện tại nói quá | — |
| C4 | **Không** chạy thêm khoảng khỏe ≥ 6 giờ riêng để phân xử trôi p95; gộp vào giờ khỏe ×1 sẵn có của W6/W7, ghi tỷ lệ request chậm của ticket theo thời gian | Tiết kiệm vài giờ máy; dữ liệu W7 cho cùng phép đo | Phân xử trôi muộn hơn |
| C5 | Demo: chạy tải ≥ 5 phút trước phần trình bày phát hiện (T-072 đề xuất); ghi vào SPEC W9a | Giảm báo động giả ở cửa sổ ít request; không đổi ngưỡng | — |

## D. Hồ sơ cũ (T-066, T-068, T-069)

| # | Đề xuất | Lý do |
|---|---|---|
| D1 | T-069: nghiệm thu (CX-05 xong, `dinh-chinh-2.md` đã viết) | Không còn điểm mở ảnh hưởng W3 |
| D2 | T-066: giữ mục 2.6 tới khi quyết CLI `fixture.py`; chưa xóa 2.7 (xét từng script khi cần dung lượng); giao người làm đáp CX-13/13b (ba mức bằng chứng R3a, README, Tempo) rồi nghiệm thu kỹ thuật W1 | Hai phiên Codex đồng ý; xóa không hoàn tác được |
| D3 | T-068: giữ bản hoàn tác `service-graph-4-bak` và dữ liệu thử; giao người làm đáp CX-14/14b (F1 đếm cờ DB, F2 WHY-101 — Minh duyệt chữ, N1 mốc chụp); rồi nghiệm thu | Hai phiên Codex đồng ý |

## E. W6 (T-074) và E6

| # | Đề xuất | Lý do |
|---|---|---|
| E1 | Giao T-074 làm bản 4 theo CX-15/CX-15b (11 điểm, `results/T-070/hop-nhat-cx13-16.md` mục 3) + phạm vi RQ3d; gom **một danh sách quyết định W6 duy nhất** (Q-W6-01…12 cập nhật theo bản 4, mỗi câu có đề xuất); Codex hai phiên kiểm; rồi trình Minh một lần | Nhiều đề xuất ở bản 2/3 đã bị Codex chặn; duyệt bản cũ sẽ phải duyệt lại |
| E2 | N5/Q-W6-07: giữ M4 (SimpleRCA) + BARO theo §8.3, bỏ câu dùng top-1 0,80 của bài báo làm bằng chứng về bản cài M4; không thêm baseline trace | Theo CX-15b N5 và WHY-17 |
| E3 | E6 (đo khôi phục DB) chạy sau khi Minh duyệt bản 4 W6; sửa hạn bán (R9) trước 28/11 trong E6 như đã định | Phụ thuộc thiết kế W6 |

## F. W8 (T-075) và W9a

| # | Đề xuất | Lý do | Cần Minh |
|---|---|---|---|
| F1 | Q6: W8 ở **mức demo** — LLM giải thích dẫn bằng chứng của ca, gợi ý bước xử lý, được trả lời "không đủ bằng chứng"; không đổi thứ hạng RCA; chất lượng giải thích nhiều ca để câu hỏi riêng | Claude và Codex đã đồng tình (SPEC T-075) | Duyệt |
| F2 | Nhà cung cấp LLM: **Anthropic API** (mô hình Claude); gửi ra ngoài chỉ phần tóm tắt ca (dịch vụ, thứ hạng, bằng chứng đã tính), không gửi log thô | Gửi dữ liệu ca ra ngoài là quyền của Minh (R3) | Chọn nhà cung cấp; tự nhập khóa API (agent không nhập khóa) |
| F3 | Sau F1–F2: mở phiên T-075; song song điều phối soạn SPEC W9a (diễn tập 2 lần không lỗi) | Luồng liên tục tới demo | Duyệt SPEC W9a khi trình |

## G. Hồ sơ và commit

| # | Đề xuất |
|---|---|
| G1 | Ghi DECISIONS một khối "23/11/2026" gồm: duyệt gói E5/P/H (SHA), và mọi mục A–F Minh duyệt ở đây |
| G2 | Commit + push repo RCA (hồ sơ T-069…T-075 từ 20/11) sau khi ghi G1; nội dung commit trình trước |

## Luồng chạy sau khi duyệt

1. A1 (T-073, máy) song song C2 (T-071, T-072, không máy) và E1 (T-074, không máy).
2. B3 sau A1 (T-073). Codex kiểm từng lượt đáp (hai phiên khi là phản biện chính).
3. G1 → G2 sau khi các lượt đáp xong.
4. F3 khi có F1–F2. E6 khi Minh duyệt bản 4 W6.
5. Hết usage Codex: báo Minh đổi tài khoản. Hết usage Claude: chạy ít phiên hơn, giữ checkpoint.

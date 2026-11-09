# T-055 — RE3-OB bản cuối: chuẩn bị, mở một lần, chấm và phân tích

- **Người làm:** Claude. **Người phản biện:** Codex, phản biện sau theo quyết định của Minh (gộp sau khi có kết quả).
- **Nguồn quyền:** `results/T-055/grants/minh-re3.txt` (nguyên văn lời Minh 08/11/2026). Minh giao quyết định trong phiên cho Claude, yêu cầu ghi lại mọi quyết định lớn để kiểm. SPEC này được ghi theo quyền giao đó, **chưa được Minh đọc trước khi ghi**.
- **Thuộc gói MRP:** P7, phần dataset giữ ngoài (RE3-OB chỉ mở một lần cho bản cuối; C-15 B/Q-247). Chuẩn bị G4.

## Mục tiêu và câu hỏi nguồn

Đánh giá M1 **đúng bản đã khóa ở P7(a)** (không sửa thiết kế; Q2/Q3 theo đề xuất) cùng baseline và đối chứng trên 30 ca RE3-OB (10 ô). RE3 chỉ có lỗi mã nguồn f1–f5, khác các dataset đã dùng (tài nguyên/mạng/độ trễ). Câu hỏi:

1. RQ3b trên dữ liệu chưa dùng lúc thiết kế: M1 xếp hạng root ra sao so với baseline, theo ô và theo loại lỗi mã nguồn.
2. RQ3d: bỏ E1/E2/E5 hoặc dùng quy tắc đơn giản (C-d1/C-d2) đổi gì.
3. Vì sao kết quả cao hoặc thấp: lần trung gian theo luật 14/15/17/18 như P7(a); hệ quả cho FlashTicket (P9/P10).

Theo WHY-06/Q-246: RE3 chỉ báo cỡ chênh kèm CI bootstrap theo ô, **không có phép kiểm định**, không gộp dataset.

## Đầu vào

- G1: `results/T-021/chia-theo-o/A-phan-tang.csv` (30 dòng RE3-OB), thành viên khớp `results/T-052/ke-hoach-tap-test.json#/cohorts/RE3-OB`.
- Dữ liệu: HF `phamquiluan/RCAEval` revision `afeacb11…`; ba parquet mỗi ca (131,7 MiB tổng) + `inject_time.txt`.
- Code: gói đã ghim của main013-v2 (`results/T-054/runs/chuan-bi-main-013-v2/code-pins.json`) trên EC2; tuyến RE3 đã cài ở H2 (`src/p3/re3.py`, `src/m1/adapter.py`, `results/T-054/scripts/{worker,nguon,cham}.py`).
- Cấu hình M1 và đối chứng: đúng `activated-001/protocol.json#/configurations` của main013-v2. Baseline: cùng config P3-v2/Q85 như main.
- H1 (đơn vị, r, U, alias): bộ giả định tường minh, ghi "chưa kiểm", kiểm bằng preflight không nhãn khóa trước (`results/T-055/scripts/preflight_ec2.py`).

## Phạm vi ghi

- `tasks/T-055-re3-ban-cuoi/{SPEC,LOG}.md`; dòng T-055 trong `docs/STATE.md`.
- `results/T-055/**` (script, biên nhận, giao thức, báo cáo, phân tích).
- Đầu ra thực thi bắt buộc nằm dưới `results/T-054/runs/re3-ban-cuoi-001/` vì code đã ghim chỉ ghi trong `results/T-054` (`bien_nhan.OUT`); thư mục mới, không đụng lượt cũ.
- Vùng riêng `D:/RCA-ext/private/T-055/` (nhãn, kế hoạch tải có tên ca) — ngoài git.
- EC2: `/home/ubuntu/rca-p7/T-055/` (dữ liệu) và `/home/ubuntu/rca-p7/T-054/checkpoint013/work-re3/` (bản sao code root work-v2 + lớp phủ RE3). Telemetry RE3 không về laptop.
- Lớp phủ code: chỉ `results/T-054/scripts/bien_nhan.py` trong code root RE3 trên EC2, thêm quy tắc lỗi RE3 (mục Lỗi). Bản lớp phủ lưu ở `results/T-055/overlay/`. Không sửa file đã ghim trong repo.
- Sổ DECISIONS/WHY: ghi đề xuất dòng trong LOG để Minh duyệt; không tự ghi sổ chính thức.

## Ma trận (khóa trước khi mở)

30 ca × vế: M1, bo-E1, bo-E2, bo-E5, C-a0, C-a1 (seed None); baro, simplerca (M4), tracerca, microrank, circa (seed None); torai_B (seed 0/1/2). 420 slot. Dẫn xuất sau seal, không gọi thêm: C-d1, C-d2 (từ extra của M1), C-c, C-g (như P7). Không chạy: T12 (không có snapshot RE3), C-d3 (OB không có), C-e (chỉ TT), TORAI A (không có nguồn tác giả RE3).

Độ đo: rr, hit@1/3/5, ndcg@5, avg@5; world P, S_lo, S_hi (P là chính). Seed gộp trong ca, đủ seed. Support: NO_EVIDENCE/ERROR/TIMEOUT tính 0; UNSUPPORTED báo riêng.

## Lỗi và thời gian (luật 21)

- Lỗi nguồn/adapter/hạ tầng hoặc preflight lệch: dừng trước phương pháp và trước ghép nhãn.
- ERROR của phương pháp trong pha method trên đầu vào đã xác minh: **tính trượt** (mặc định WHY-06), có biên nhận lỗi, phân tích cơ chế sau. Quy tắc này khóa trước trong lớp phủ; không cần chạy lại slot khác. Lỗi khác chưa phân loại: chỉ chặn slot đó, supervisor chạy tiếp.
- Timeout 600 s/slot như main; poll 0,1 s; max gap < 5 s.
- Lỗi ở 10%: sửa nguồn/adapter, chạy lại toàn bộ (RE3 chưa ghép nhãn). Ở 50% hay 99%: chỉ slot lỗi bị ảnh hưởng.

## Máy

Hai EC2 (2 vCPU, 8 GB, ~24 GB trống), mỗi máy 15 ca, 1 worker. Laptop chỉ điều khiển, nhận kết quả compact và chấm. Ước lượng chưa kiểm: 1–3 giờ.

## Tiêu chí xong

1. 420 slot VERIFIED hoặc kết cục đã khóa; seal trước ghép nhãn; ghi sổ xem test.
2. Bảng RE3 tách khỏi A4; CI bootstrap theo ô; theo ô/loại lỗi.
3. Phân tích nhóm giúp/hại có trung gian và ca đối chiếu; tách quan sát/suy luận/ứng viên/câu hỏi mở; hệ quả FlashTicket.
4. LOG, STATE, quyết định ghi lại để Minh kiểm; prompt phản biện cho Codex.

## Không làm

Không sửa M1 hay cấu hình; không chọn lại thiết kế từ RE3; không mở lại RE3 lần hai; không commit/push; không gửi câu hỏi ra ngoài.

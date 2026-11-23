# Đề xuất gom việc — bản 3: bản 2 + phân việc Codex/Claude

23/11/2026, điều phối T-070. Nội dung mục 0–3 giữ nguyên **bản 2** (`de-xuat-quyet-2026-11-23-ban2.md`). Bản 3 chỉ thêm mục 4 dưới đây.

**Minh (chat, nguyên văn):** "duyệt sửa sau khi 2 bên đã thống nhất, sau đó trình lại cho codex, claude xem có việc nào nhẹ cho codex làm không, tránh dồn nhiều cho claude quá, việc khó để claude, việc vừa sức để codex làm, không dẫm chân nhau".

Cách điều phối hiểu và áp dụng (Codex kiểm ở CX-23): các mục bản 2 §1 được thực hiện khi Codex kiểm lại không còn bất đồng có bằng chứng; điểm còn bất đồng thì trình Minh. Các mục tự bản chất cần Minh chọn hoặc duyệt chữ vẫn chờ Minh: **F2** (nhà cung cấp, model, danh sách trường), chữ mục WHY (B3, C3), chữ đính chính SPEC/KE-HOACH (B1), khối DECISIONS (G1), danh sách file commit (G2).

## 4. Phân việc

Nguyên tắc: việc khó (thiết kế, phân tích cơ chế, thao tác máy nhiều bước, vai trò người làm của task) → Claude. Việc vừa sức (sửa code có đặc tả rõ, kiểm bằng dữ liệu giả, soạn đính chính chữ, liệt kê file) → Codex, mỗi việc Codex có phiên Codex khác kiểm. Mỗi việc một vùng ghi riêng; không hai bên cùng ghi một file.

| Việc | Ai | Vùng ghi duy nhất | Ai kiểm | Phụ thuộc |
|---|---|---|---|---|
| **A1** chép file ca `7577dd5b` (kèm sha256) rồi hoàn tác §5, xóa 3 thư mục rỗng theo UID khi counts = 0 | Claude T-073 (chủ S4) | máy; `results/T-073/e5/hoan-tac/`, `results/T-073/e5/ca-7577dd5b/` | điều phối (lịch máy, SHA) | — |
| **B3** đáp CX-21/21b trên file đã chép (V082 đầu vào, biên H5, hai nhóm metric, L4, `fault-stop`), soạn chữ WHY ngưỡng phủ | Claude T-073 | `results/T-073/dap-cx21/` | Codex CX-27 (kiểm lại) | A1 |
| **C2-code** phiên bản mới `cham_offline` và `e4_giai_thich_khac` (ba nhánh khi có cảnh báo, luật `<8` xét cả cửa sổ, cờ chồng quan sát), `chon-nguong` trả mã lỗi khi thiếu route; tự ghi hash code chạy; kiểm bằng dữ liệu giả; không ghi đè file đã ghim | **Codex CX-24** (workspace-write) | chỉ `results/T-072/v2/` (file mới) | Codex CX-24b | — |
| **C2-chữ** đính chính W4 (F1 giờ hiệu lực 06:06:10Z, F2 câu lệch −4 s, F4 phạm vi B2, N2 lập luận 5xx) | **Codex CX-25** | `results/T-072/dinh-chinh-cx19.md`, `results/T-071/dinh-chinh-cx19.md` (file mới) | Codex CX-25b | — |
| **C2-đáp** bảng phản hồi người làm cho CX-19/19b, dẫn kết quả CX-24/25; soạn chữ sửa WHY-110 (C3) | Claude T-072 (và T-071 cho phần của mình) | LOG T-071/T-072 | Codex (kiểm lại) | CX-24b, CX-25b |
| **B1-chữ** bản nháp đính chính tên G1 `0.5 + che_do_b b-1` cho KE-HOACH §8.2, SPEC T-073, SPEC T-075 (chỉ soạn; áp dụng khi Minh duyệt chữ) | **Codex CX-26** | `results/T-070/nhap-dinh-chinh-g1.md` (file mới) | Codex CX-26b | — |
| **G2-danh sách** liệt kê file/hunk thuộc R2(b) (T-069, gói bàn giao, hồ sơ T-070…T-075), tách phần phát sinh sau và các thư mục chưa track không thuộc R2(b) | **Codex CX-28** (chỉ đọc) | trả lời trong chat → điều phối lưu `results/T-070/codex/` | điều phối kiểm trước khi trình Minh | — |
| **E1** W6 bản 4 + phần E6 + danh sách quyết định W6 duy nhất | Claude T-074 | `results/T-074/*-4.*` | Codex hai phiên | — |
| **F3** SPEC W9a (trình trong chat) | Claude điều phối | chat; sau duyệt mới tạo `tasks/T-07x-…` | Codex | — |
| **D2, D3** đáp CX-13/13b (T-066), CX-14/14b (T-068) | Claude (người làm T-066, T-068) | LOG T-066, T-068; file đính chính mới trong `results/T-066/`, `results/T-068/` | Codex kiểm lại | sau E1, F3 (ưu tiên thấp hơn) |

**Không dẫm chân:**
- Codex chỉ ghi file **mới** trong các vùng nêu trên; không sửa file đã có, không ghi LOG/STATE/SPEC/WHY/DECISIONS, không SSH, không commit, không subagent, `gpt-6.2-astra` high.
- Hai việc Codex workspace-write (CX-24, CX-25, CX-26) chạy **lần lượt** trong một chuỗi để không cùng lúc đổi cây làm việc; mỗi việc kiểm `git status` trước/sau và báo đúng file đã tạo.
- Phiên Claude T-072 chỉ bắt đầu C2-đáp sau CX-24b/CX-25b; trong lúc chờ không ghi `results/T-072/`.
- Máy: chỉ T-073 ở S4 tới khi điều phối đóng S4.
- Hết usage Codex: dừng chuỗi, giữ đầu ra, báo Minh đổi tài khoản.

## Ước lượng thời gian (chưa đo, theo các lượt tương tự hôm qua)

A1 khoảng 20–30 phút; CX-24…26 mỗi việc khoảng 5–15 phút + phiên kiểm; E1 một đến vài lượt Claude; F3 một lượt.

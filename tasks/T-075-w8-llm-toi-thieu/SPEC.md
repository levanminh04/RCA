# T-075 — W8: LLM giải thích tối thiểu cho demo

- **Trạng thái:** đề xuất — **chờ Minh** (Q6 mức demo; nhà cung cấp/mô hình LLM, vì gửi dữ liệu ca ra ngoài là quyền R3). Chưa mở phiên làm việc. Soạn bởi phiên điều phối T-070.
- **Người làm:** Claude (phiên `llm-w8`, mức Medium — phạm vi demo, đầu vào/đầu ra rõ).
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P8, P10 — **Cổng:** chuẩn bị G6.

## Mục tiêu

Kế hoạch §8.2 W8: "LLM tối thiểu: giải thích dẫn bằng chứng, gợi ý bước xử lý, được trả lời 'không đủ bằng chứng'. Mức đánh giá do Minh chọn. Xong khi: chạy được trong demo." MRP P8; bước 5 của cô. Q6 (Claude và Codex đồng tình, Minh chưa duyệt): mức demo, không đổi thứ hạng RCA; chất lượng giải thích trên nhiều ca là câu hỏi riêng.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép kiểm | Phần còn mở |
|---|---|---|
| Giải thích có chỉ dựa trên gói bằng chứng của ca? | Mỗi câu khẳng định dẫn tới trường trong G1/gói bằng chứng; kiểm tự động trích dẫn tồn tại | Chất lượng tổng quát OPEN |
| Có trả lời "không đủ bằng chứng" khi thiếu? | Ca thử thiếu tín hiệu (cắt bớt gói) | — |
| Không đổi thứ hạng RCA? | So danh sách hạng trước/sau | — |

## Đầu vào

Đầu ra G1 đã có (`/srv/rca-lab/rca-results/t065-l11-001/` bản sao trên laptop nếu có; T-061, T-065); sau này G1 0.5 + che_do_b b-1 của T-073 (kiểm tương thích).

## Đầu ra

Code ở worktree lab `D:/Project/rca-lab-wt/T-075` nhánh `t075-llm` (vị trí thư mục đề xuất trong LOG); `results/T-075/` (prompt mẫu, ví dụ đầu ra trên 2–3 ca, kiểm trích dẫn).

## Phạm vi ghi

Ngoài `LOG.md` và dòng T-075 trong `docs/STATE.md`: `results/T-075/`; worktree lab như trên. Không commit/push khi Minh chưa duyệt. Không gửi dữ liệu ra dịch vụ ngoài khi Minh chưa chọn nhà cung cấp.

## Các bước

1. Chờ Minh: Q6, nhà cung cấp/mô hình, khóa API do Minh cấp (agent không nhập khóa).
2. Thiết kế khuôn đầu vào (gói bằng chứng rút gọn từ G1) và khuôn đầu ra (câu + trích dẫn).
3. Cài, chạy trên ca có sẵn, kiểm trích dẫn và trường hợp thiếu bằng chứng.

## Kiểm đúng đắn

Kiểm trích dẫn máy móc; không dùng nhãn/sổ tiêm trong đầu vào LLM (luật cứng 6).

## Tiêu chí xong

Chạy trong demo trên ca W5; ba thuộc tính ở bảng trên đạt trên các ca thử.

## Không làm

Đánh giá chất lượng trên nhiều ca; tinh chỉnh mô hình.

## Chi phí ước lượng

Theo nhà cung cấp Minh chọn; vài chục lần gọi.

## Rủi ro và điều chưa chắc

Gửi dữ liệu ca ra ngoài (tên service, log) — Minh quyết phạm vi.

## Prompt bàn giao

Ở `LOG.md`, mục cuối mỗi lượt.

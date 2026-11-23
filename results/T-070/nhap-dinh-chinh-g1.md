Nháp, chưa áp; Minh duyệt chữ rồi điều phối mới sửa (Luật 0)

# Đính chính tên hợp đồng G1 của chế độ (b)

Minh đã chốt tên `G1 0.5 + che_do_b b-1` tại Q3 trong `docs/DECISIONS.md`. Ba đoạn dưới đây là chữ trình duyệt. Với bản đã khóa, điều phối ghi đính chính riêng, dẫn về đúng dòng gốc.

| Vị trí | Đoạn cũ nguyên văn → đoạn mới đề xuất | Lý do |
|---|---|---|
| `docs/techstack/KE-HOACH-GIAI-DOAN-2.md:140` (§8.2, W5) | `hợp đồng G1 bản 0.3 mang nguồn t̂` → `hợp đồng G1 0.5 + che_do_b b-1 mang nguồn t̂` | Tên mới nêu đúng phiên bản định dạng và khối mang nguồn t̂. |
| `tasks/T-073-w5-rca-truc-tuyen/SPEC.md:32` | `ghi G1 bản 0.3 (mang nguồn t̂)` → `ghi G1 0.5 + che_do_b b-1 (mang nguồn t̂)` | Đầu ra W5 dùng định dạng 0.5 và ca E5 ghi khối b-1. |
| `tasks/T-075-w8-llm-toi-thieu/SPEC.md:22` | `sau này G1 0.3 của T-073 (kiểm tương thích)` → `sau này G1 0.5 + che_do_b b-1 của T-073 (kiểm tương thích)` | W8 cần kiểm tương thích với đúng hợp đồng đầu ra của T-073. |

**Tên file lịch sử.** `tasks/T-073-w5-rca-truc-tuyen/SPEC.md:33` có đoạn `results/T-073/g1-0.3.md` → giữ nguyên `results/T-073/g1-0.3.md` vì đây là đường dẫn tới tài liệu gốc.

**Căn cứ.** `results/T-073/g1-0.3.md:9` ghi định dạng 0.5 và khối `che_do_b` phiên bản b-1. `results/T-073/e5/s49-che-do-b.txt:3` ghi `phien_ban_khoi` bằng `b-1` trong ca E5. Điểm N2 tại `results/T-070/codex/CX-21b-tin-cuoi.md:19` nêu sai lệch với SPEC. Hàng B1 tại `results/T-070/codex/CX-23-tin-cuoi.md:14` xác nhận tên đề xuất khớp cách ghi.

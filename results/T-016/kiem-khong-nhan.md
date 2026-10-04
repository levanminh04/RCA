# Kết quả các phép kiểm không cần nhãn (mục "Kiểm đúng đắn" của SPEC)

T-016, S3, S8, S11. Các phép này không dùng nhãn để quyết định; nhãn chỉ dùng để chấm phép thử giả (mục 6).

| # | Phép kiểm (SPEC) | Kết quả | File |
|---|---|---|---|
| 1 | Số công bố tra **trước** khi chạy | 174 ô tự parse trùng `moc.py` của T-006; tra lúc 10:00, trước lượt chạy chính đầu tiên (10:40) | `moc-cong-bo.json`, `runs/s1-so-moc-t006.txt`, LOG |
| 2a | Chạy lại cùng seed | 90/90 giống hệt | `runs/s3c-lan2.json` |
| 2b | Khác `PYTHONHASHSEED` | 90/90 | `runs/s3d-pythonhashseed.json` |
| 2c | Khác seed | thứ hạng khác 0–24/90 ca; sd Avg@5 ≤ 0,004 | `ngau-nhien.md` mục 4 |
| 3 | Đầu ra không rỗng, không lỗi | 0 ca rỗng, 0 ca lỗi ở mọi khối TORAI (OB, SS: 11 cấu hình × 1–5 seed; TT: 4 × 3 seed; placebo, hoán vị) và RCD (OB 20, SS 10, TT 1 ca) | `cham/*-tong-hop.json` (`kiem.rank_rong`, `so_ca_loi`), `cham/s11-rcd-*.json` |
| 4a | Thứ hạng trùng thứ tự cột | TORAI: không áp dụng được theo nghĩa của `@rca` (TORAI không bọc `@rca` ở Python 3.8; lỗi thì `main.py` dừng). Phép kiểm của `cham.py` với RCD: OB cửa sổ 20: 0 ca; SS cửa sổ 10: 2 ca (`carts_delay_1`, `user_loss_2`) gắn cờ, cùng loại báo động giả như T-006 (đầu ra ngắn tình cờ theo thứ tự cột) | `cham/s11-rcd-*.json` |
| 4b | Nhánh dự phòng của TORAI (`torai.py:330-334`) | Bản gốc cửa sổ 10: 176/184 cụm OB, 171/173 SS, 72/72 TT; thứ hạng cuối trùng thứ hạng "chỉ mức nghiêm trọng" ở 86/90, 88/90, 30/30 ca. Bản sửa: 166/184, 166/173, 67/72. **Ở cấu hình chính thức, CausalRanker hầu như không đóng góp** | `giam-mau-hai-lan.md` mục 5 |
| 5 | Đổi thứ tự cột | Vectơ mức nghiêm trọng, phân cụm không đổi 90/90 (mọi seed, OB, SS, gốc, sửa); thứ hạng đổi 2–14/90 ca, top-1 đổi 0–4/90 — ngang dao động giữa seed | `runs/s8-so-hoan-vi.txt` |
| 6 | Hai cửa sổ đều bình thường (placebo, cửa sổ 10; mốc giả = mốc tiêm − 315 s) | Chấm và soi đều gộp service như `main.py` (`-db` về service, bỏ trùng). OB: AC@1 0,033 (gốc), 0,044 (sửa), Avg@5 0,118; may rủi (xếp đều trên 12–14 service sau gộp, TB theo ca) AC@1 0,074, Avg@5 0,223 → dưới may rủi. SS: AC@1 0,122, Avg@5 0,378–0,380; may rủi trên 11 service sau gộp 0,091 / 0,273 → trên may rủi. Soi SS: service gốc thật đứng hạng TB 4,433 (sửa 4,422), các service bị tiêm khác 4,544 (4,533); top-1 0,122 so với 0,136 → **không có dấu vết riêng của ca**. Mức trên may rủi do các service bị tiêm (và database của chúng, sau khi gộp `-db`) hay được xếp cao: `carts` top-1 27/90; nếu coi 15 ứng viên thô được hoán vị đều rồi mới gộp thì kỳ vọng top-1 ≈ 0,120 (4/5 service gốc có database), gần số quan sát. Ở ca thật, service gốc đứng hạng TB 1,256 (SS), 1,433 (OB) | `cham/s8-tong-hop.json`, `runs/s8-soi-placebo.txt` (bản sửa theo REVIEW R2; bản đầu bỏ qua bước gộp `-db`) |
| 7 | Soi giá trị trung gian | Không thấy điểm > 1e6 ngoài các cột trace_err bị nhân 1e9 có chủ ý của code (18–19 ca OB; chưa kiểm riêng các cột này ảnh hưởng điểm service ra sao). Vectơ mức nghiêm trọng đã chuẩn hóa: 0 ô NaN, 0 ô > 1 trên 6 390 lượt-ca có thu trung gian (`runs/s8-soi-nan.txt`). Dòng giả toàn 0 do ghép theo chỉ số: 2 253 (OB gốc 10) … 0 (bản sửa). Logts lưới đều 15 s; 2 ca OB thiếu dòng nửa lỗi (11, 18 dòng). Không có tên cột trùng giữa metric và log, không cột metric nào tận cùng bằng `_<số>` (210 ca OB, SS, TT dev; `runs/s4-trung-ten-cot.txt`), nên bước bỏ cột trùng (`torai.py:50, 53`) không bỏ gì (E16). Không lỗi `assert` số dòng (E12) ở mọi khối | `runs/s4-soi-dau-vao-*.jsonl`, `cham/*-tong-hop.json`, `runs/s8-soi-nan.txt` |
| 8 | Harness tương đương `main.py`; wrapper không đổi hành vi | 90/90; 90/90 | `runs/s3a-*.json`, `runs/s3b-*.json` |
| 9 | Ví dụ tính tay khớp code chính thức | khớp mọi bước, p-value lệch ≤ 7,9e-15 | `vi-du-tinh-tay.md` |
| 10 | Linux và Windows | TORAI: 90/90 ca giống hệt ở 4 cặp; RCD SS: 90/90 giống hệt (`diem-mo-t006.md` mục 2) | `runs/s11-linux-vs-win-*.json` |

Ghi chú về mục 6:
- Cửa sổ 20 không làm được phép thử giả: cần 600 s bình thường mỗi nửa (1 200 s trước mốc), file chỉ có 720 s trước mốc (SPEC E19). Hệ quả: kết luận "không rò" ở cửa sổ 20 chỉ dựa trên phân tích tĩnh (đường nhãn, hồ sơ mục 8) và trên việc cửa sổ 20 dùng cùng code dựng đầu vào.
- Mốc giả lùi thêm 15 s để bin logts cuối của nửa "lỗi giả" kết thúc trước mốc tiêm thật.
- Avg@5 may rủi = (1 + 2 + 3 + 4 + 5) / (5 × n) = 3/n, với n là số service **sau khi gộp** như phép chấm; tính theo từng ca rồi lấy trung bình.

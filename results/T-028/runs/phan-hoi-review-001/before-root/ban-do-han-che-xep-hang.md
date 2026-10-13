# Bản đồ hạn chế xếp hạng chế độ (a) — T-028

Phân tích dev theo codebook đã duyệt, bản chốt `results/T-028/runs/chot-codebook-002/manifest.json`. Rào cản membership/luật trả về được kiểm trực tiếp; các dấu hiệu còn lại là ứng viên, chưa kiểm nhân quả. Primary chỉ phục vụ trình bày. Kết quả này chưa xác nhận hoặc phủ nhận “lan có đáng kể”; không định nghĩa nhãn lan, không kết luận về giá trị đồ thị.

## 1. Phạm vi và ca sai

Giữ bảng chính RE2-TT dev30 và Nezha-OB main, tất cả phương pháp/trạng thái. TORAI gộp Hit theo ca, giữ từng seed. Non-OK báo riêng; UNSUPPORTED không là chất lượng ranking hay bằng chứng không có tín hiệu. Sai hạng 1 và 5 không cộng thành hai ca.

Nguồn mọi số ở bảng sau: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables` (overall), đối chiếu `results/T-028/runs/buoc3-005/ca-sai.json` và bước 1 `results/T-028/runs/danh-sach-001/step1.json`.

| Dataset | Phương pháp | k | Đúng OK | Sai OK | Non-OK | Tổng | Σ(1−Hit) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nezha-OB | BARO | 1 | 8 | 14 | {} | 22 | 14 |
| Nezha-OB | BARO | 5 | 16 | 6 | {} | 22 | 6 |
| Nezha-OB | CIRCA OLS+RHT+DA | 1 | 0 | 0 | {'UNSUPPORTED': 22} | 22 | 22 |
| Nezha-OB | CIRCA OLS+RHT+DA | 5 | 0 | 0 | {'UNSUPPORTED': 22} | 22 | 22 |
| Nezha-OB | MicroRank full | 1 | 0 | 22 | {} | 22 | 22 |
| Nezha-OB | MicroRank full | 5 | 8 | 14 | {} | 22 | 14 |
| Nezha-OB | SimpleRCA | 1 | 7 | 15 | {} | 22 | 15 |
| Nezha-OB | SimpleRCA | 5 | 18 | 4 | {} | 22 | 3.5 |
| Nezha-OB | TORAI B | 1 | 0 | 0 | {'UNSUPPORTED': 22} | 22 | 22 |
| Nezha-OB | TORAI B | 5 | 0 | 0 | {'UNSUPPORTED': 22} | 22 | 22 |
| Nezha-OB | TraceRCA | 1 | 2 | 20 | {} | 22 | 19.6667 |
| Nezha-OB | TraceRCA | 5 | 11 | 11 | {} | 22 | 10.5 |
| RE2-TT | BARO | 1 | 21 | 9 | {} | 30 | 9 |
| RE2-TT | BARO | 5 | 26 | 4 | {} | 30 | 4 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | 16 | 14 | {} | 30 | 14 |
| RE2-TT | CIRCA OLS+RHT+DA | 5 | 27 | 3 | {} | 30 | 3 |
| RE2-TT | MicroRank full | 1 | 2 | 24 | {'ERROR': 4} | 30 | 28 |
| RE2-TT | MicroRank full | 5 | 13 | 13 | {'ERROR': 4} | 30 | 17 |
| RE2-TT | SimpleRCA | 1 | 25 | 5 | {} | 30 | 5 |
| RE2-TT | SimpleRCA | 5 | 29 | 1 | {} | 30 | 1 |
| RE2-TT | TORAI B | 1 | 26 | 4 | {} | 30 | 4 |
| RE2-TT | TORAI B | 5 | 30 | 0 | {} | 30 | 0 |
| RE2-TT | TraceRCA | 1 | 21 | 5 | {'ERROR': 4} | 30 | 9 |
| RE2-TT | TraceRCA | 5 | 25 | 1 | {'ERROR': 4} | 30 | 5 |

Tổng mức trượt kỳ vọng có non-OK Hit=0, khác số ca sai ranking. Phần tổng cohort và non-OK riêng giữ mẫu số trong JSON nguồn.

Đọc kết quả theo giới hạn đã khai: các ca OK sai RE2 không có M1/M2. Ở Nezha, TraceRCA có một ca root thuộc O nhưng bị loại khỏi R; cùng ca có M6 và được giữ đa nhãn. Vì vậy rào cản tập giải thích trực tiếp ca đó, còn phần lớn ca sai vẫn cần xét ưu tiên điểm/hòa và các cơ chế ứng viên. Nguồn: bảng mechanism_tables overall trong JSON trên, k=1/5; ca cụ thể ở doc-tay.md.

## 2. Nhãn chính, đa nhãn và đối chứng

Nguồn mọi số: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`. Mỗi ô nhãn là số ca / tổng ca OK sai; tổng cohort ở cột riêng. Bảng JSON còn giữ số nhãn/tổng cohort và số False/N/A.

| Dataset | Phương pháp | k | Tổng cohort | Sai OK | M1 | M2 | M3 | M4 | M5 | M6 | M0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nezha-OB | BARO | 1 | 22 | 14 | 0/14 | 0/14 | 0/14 | 0/14 | 7/14 | 0/14 | 7/14 |
| Nezha-OB | BARO | 5 | 22 | 6 | 0/6 | 0/6 | 0/6 | 0/6 | 3/6 | 0/6 | 3/6 |
| Nezha-OB | CIRCA OLS+RHT+DA | 1 | 22 | 0 | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) |
| Nezha-OB | CIRCA OLS+RHT+DA | 5 | 22 | 0 | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) |
| Nezha-OB | MicroRank full | 1 | 22 | 22 | 0/22 | 0/22 | 0/22 | 0/22 | 20/22 | 0/22 | 2/22 |
| Nezha-OB | MicroRank full | 5 | 22 | 14 | 0/14 | 0/14 | 0/14 | 0/14 | 14/14 | 0/14 | 0/14 |
| Nezha-OB | SimpleRCA | 1 | 22 | 15 | 0/15 | 0/15 | 0/15 | 0/15 | 9/15 | 0/15 | 6/15 |
| Nezha-OB | SimpleRCA | 5 | 22 | 4 | 0/4 | 0/4 | 1/4 | 0/4 | 2/4 | 0/4 | 1/4 |
| Nezha-OB | TORAI B | 1 | 22 | 0 | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) |
| Nezha-OB | TORAI B | 5 | 22 | 0 | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) |
| Nezha-OB | TraceRCA | 1 | 22 | 20 | 0/20 | 1/20 | 1/20 | 0/20 | 16/20 | 0/20 | 2/20 |
| Nezha-OB | TraceRCA | 5 | 22 | 11 | 0/11 | 1/11 | 1/11 | 0/11 | 9/11 | 0/11 | 0/11 |
| RE2-TT | BARO | 1 | 30 | 9 | 0/9 | 0/9 | 0/9 | 0/9 | 3/9 | 0/9 | 6/9 |
| RE2-TT | BARO | 5 | 30 | 4 | 0/4 | 0/4 | 0/4 | 0/4 | 2/4 | 0/4 | 2/4 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | 30 | 14 | 0/14 | 0/14 | 0/14 | 8/14 | 2/14 | 0/14 | 4/14 |
| RE2-TT | CIRCA OLS+RHT+DA | 5 | 30 | 3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 3/3 |
| RE2-TT | MicroRank full | 1 | 30 | 24 | 0/24 | 0/24 | 0/24 | 0/24 | 5/24 | 0/24 | 19/24 |
| RE2-TT | MicroRank full | 5 | 30 | 13 | 0/13 | 0/13 | 0/13 | 0/13 | 5/13 | 0/13 | 8/13 |
| RE2-TT | SimpleRCA | 1 | 30 | 5 | 0/5 | 0/5 | 0/5 | 0/5 | 5/5 | 0/5 | 0/5 |
| RE2-TT | SimpleRCA | 5 | 30 | 1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |
| RE2-TT | TORAI B | 1 | 30 | 4 | 0/4 | 0/4 | 0/4 | 0/4 | 1/4 | 0/4 | 3/4 |
| RE2-TT | TORAI B | 5 | 30 | 0 | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) | N/A (0 ca) |
| RE2-TT | TraceRCA | 1 | 30 | 5 | 0/5 | 0/5 | 0/5 | 0/5 | 4/5 | 0/5 | 1/5 |
| RE2-TT | TraceRCA | 5 | 30 | 1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |

Đây là bảng primary theo thứ tự M1→M2→M3→M4→M5→M6→M0; không là nguyên nhân trội. Bảng đa nhãn, đối chứng đúng/sai, số True/False/N/A và phân tầng theo ô/loại lỗi/vị trí/root được xuất đầy đủ tại `bang-theo-o-va-doi-chung.md` và JSON nguồn.

Các quan hệ cấu trúc cần giữ cạnh đối chứng: M1/M2 kéo theo sai; M3 loại Hit=1; M5 True không thể có ở ca đúng top-1; M6 SimpleRCA kéo theo sai top-1; M6 TraceRCA kéo theo M2. M4 thuộc cohort lỗi chưa chứng minh lỗi đó gây mỗi thất bại. Nhóm đúng hoặc sai rỗng cho đối chứng N/A. Các chênh lệch là liên hệ quan sát, không xác nhận nguyên nhân độc lập.

Ví dụ khác biệt primary/đa nhãn: CIRCA RE2 top1 có M4 ở 8/14 ca OK sai và M5 ở 10/14, nhưng primary M5 chỉ 2/14 vì thứ tự cố định. MicroRank RE2 top1 có M0 ở 19/24 ca OK sai; đọc tay mẫu M0 vẫn thấy span A đạt luật native của root, nên thiếu tín hiệu dương không giải thích được các mẫu đó theo M6. Nguồn: `results/T-028/runs/buoc3-005/summary-tables.json` → mechanism_tables overall; `results/T-028/runs/buoc3-005/manual-re2.json` → cases/microrank_full; bảng từng ô nằm ở bang-theo-o-va-doi-chung.md.

## 3. Cơ hội nhận M5 và mức nền P0

Graph G_N là graph phân tích từ cha-con cùng trace trước mốc; không gọi nó là graph native MicroRank hay graph nhân quả CIRCA. BARO/TORAI không nhận graph này, N-end chỉ là bối cảnh. P0 giữ vị trí root, cấu trúc hòa/khối, chiều dài trả về L và tập quan sát O; hoán vị danh tính O trừ root. Chỉ so số cờ cơ sở M5 True với ΣP0 trên cùng tập đủ điều kiện. Root ngoài R/graph thiếu/ranking không hợp lệ cho N/A. Không dùng primary=M5, không OR P0; TORAI báo từng seed.

Nguồn mọi số: `results/T-028/runs/buoc3-005/summary-tables.json` → `P0_tables` (overall); bảng theo ô ở cùng file.

| Dataset | Phương pháp | k | Seed | Đủ điều kiện | Tổng bản ghi | M5 True | ΣP0 | Chênh |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nezha-OB | BARO | 1 | single | 14 | 22 | 7 | 5.71032 | 1.28968 |
| Nezha-OB | BARO | 5 | single | 6 | 22 | 3 | 3.21032 | -0.210317 |
| Nezha-OB | CIRCA OLS+RHT+DA | 1 | single | 0 | 22 | 0 | N/A | N/A |
| Nezha-OB | CIRCA OLS+RHT+DA | 5 | single | 0 | 22 | 0 | N/A | N/A |
| Nezha-OB | MicroRank full | 1 | single | 22 | 22 | 20 | 14.9444 | 5.05556 |
| Nezha-OB | MicroRank full | 5 | single | 14 | 22 | 14 | 12.1389 | 1.86111 |
| Nezha-OB | SimpleRCA | 1 | single | 15 | 22 | 9 | 4.55556 | 4.44444 |
| Nezha-OB | SimpleRCA | 5 | single | 4 | 22 | 2 | 1.66667 | 0.333333 |
| Nezha-OB | TORAI B | 1 | single | 0 | 22 | 0 | N/A | N/A |
| Nezha-OB | TORAI B | 5 | single | 0 | 22 | 0 | N/A | N/A |
| Nezha-OB | TraceRCA | 1 | single | 19 | 22 | 16 | 8.83333 | 7.16667 |
| Nezha-OB | TraceRCA | 5 | single | 10 | 22 | 10 | 7.5 | 2.5 |
| RE2-TT | BARO | 1 | single | 9 | 30 | 3 | 2.25353 | 0.746475 |
| RE2-TT | BARO | 5 | single | 4 | 30 | 2 | 1.7633 | 0.236695 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | single | 14 | 30 | 10 | 3.15378 | 6.84622 |
| RE2-TT | CIRCA OLS+RHT+DA | 5 | single | 3 | 30 | 0 | 0 | 0 |
| RE2-TT | MicroRank full | 1 | single | 24 | 30 | 5 | 11.1294 | -6.12935 |
| RE2-TT | MicroRank full | 5 | single | 13 | 30 | 5 | 6.42769 | -1.42769 |
| RE2-TT | SimpleRCA | 1 | single | 5 | 30 | 5 | 0.857531 | 4.14247 |
| RE2-TT | SimpleRCA | 5 | single | 1 | 30 | 1 | 0.208955 | 0.791045 |
| RE2-TT | TORAI B | 1 | 0 | 4 | 30 | 1 | 0.341927 | 0.658073 |
| RE2-TT | TORAI B | 1 | 1 | 4 | 30 | 1 | 0.341927 | 0.658073 |
| RE2-TT | TORAI B | 1 | 2 | 4 | 30 | 1 | 0.341927 | 0.658073 |
| RE2-TT | TORAI B | 5 | 0 | 0 | 30 | 0 | N/A | N/A |
| RE2-TT | TORAI B | 5 | 1 | 0 | 30 | 0 | N/A | N/A |
| RE2-TT | TORAI B | 5 | 2 | 0 | 30 | 0 | N/A | N/A |
| RE2-TT | TraceRCA | 1 | single | 5 | 30 | 4 | 1.73741 | 2.26259 |
| RE2-TT | TraceRCA | 5 | single | 1 | 30 | 1 | 0.421053 | 0.578947 |

Chênh chỉ mô tả sai lệch với kỳ vọng của null. Không có p-value, ngưỡng đáng kể hoặc số liệu “nhãn lan”. Null không giữ thiên hướng nhận điểm của entity, số kênh/operation/cấu trúc phương pháp; không loại được lan, caller tự bất thường, tác động chung hoặc sai lệch clock/nền/graph/nhãn.

Chiều chênh không đồng nhất: ở top1 RE2, MicroRank có 5 cờ M5 trên 24 bản ghi đủ điều kiện so với ΣP0=11,1294; CIRCA có 10/14 so với 3,15378. Ở top1 Nezha, MicroRank có 20/22 so với 14,9444; TraceRCA có 16/19 so với 8,83333 (ca root ngoài R bị loại). Nguồn: `results/T-028/runs/buoc3-005/summary-tables.json` → P0_tables overall. Đây là số trên tập đủ điều kiện đã nêu, không phải nhãn primary; không gộp seed TORAI.

## 4. Tập trung và biến thiên đầu ra

D là Dice overlap kỳ vọng top-k theo phân phối hạng chính xác, D0 là kỳ vọng hoán vị đều độc lập trên đúng O mỗi ca với L giữ nguyên. Cặp TORAI lấy trung bình tổ hợp seed hợp lệ, mỗi cặp ca đóng góp một lần. Cân đều cặp ô khác nhau; cùng ô giữ riêng.

Nguồn mọi số: `results/T-028/runs/buoc3-005/concentration.json` → `equal_cell_weight_summaries`, `cell_pairs`, `case_pairs`, `within_case_seed_pairs`.

| Dataset | Phương pháp | k | Quan hệ ô | Ô/cặp ô đủ | Tổng | D | D0 | D−D0 | 1−D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RE2-TT | BARO | 1 | khác | 45 | 45 | 0.0641975 | 0.0147059 | 0.0494916 | 0.935802 |
| RE2-TT | BARO | 1 | cùng | 10 | 10 | 0.6 | 0.0147059 | 0.585294 | 0.4 |
| RE2-TT | BARO | 5 | khác | 45 | 45 | 0.148642 | 0.0735294 | 0.0751126 | 0.851358 |
| RE2-TT | BARO | 5 | cùng | 10 | 10 | 0.32 | 0.0735294 | 0.246471 | 0.68 |
| RE2-TT | SimpleRCA | 1 | khác | 45 | 45 | 0.0740741 | 0.0146917 | 0.0593824 | 0.925926 |
| RE2-TT | SimpleRCA | 1 | cùng | 10 | 10 | 0.8 | 0.0146917 | 0.785308 | 0.2 |
| RE2-TT | SimpleRCA | 5 | khác | 45 | 45 | 0.232593 | 0.0734584 | 0.159134 | 0.767407 |
| RE2-TT | SimpleRCA | 5 | cùng | 10 | 10 | 0.533333 | 0.0734584 | 0.459875 | 0.466667 |
| RE2-TT | MicroRank full | 1 | khác | 45 | 45 | 0.691358 | 0.0374211 | 0.653937 | 0.308642 |
| RE2-TT | MicroRank full | 1 | cùng | 10 | 10 | 0.8 | 0.0383333 | 0.761667 | 0.2 |
| RE2-TT | MicroRank full | 5 | khác | 45 | 45 | 0.689383 | 0.187106 | 0.502277 | 0.310617 |
| RE2-TT | MicroRank full | 5 | cùng | 10 | 10 | 0.74 | 0.191667 | 0.548333 | 0.26 |
| RE2-TT | TraceRCA | 1 | khác | 45 | 45 | 0.103704 | 0.0374211 | 0.0662826 | 0.896296 |
| RE2-TT | TraceRCA | 1 | cùng | 10 | 10 | 0.766667 | 0.0383333 | 0.728333 | 0.233333 |
| RE2-TT | TraceRCA | 5 | khác | 45 | 45 | 0.475432 | 0.187106 | 0.288326 | 0.524568 |
| RE2-TT | TraceRCA | 5 | cùng | 10 | 10 | 0.77 | 0.191667 | 0.578333 | 0.23 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | khác | 45 | 45 | 0.11358 | 0.0147059 | 0.0988744 | 0.88642 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | cùng | 10 | 10 | 0.366667 | 0.0147059 | 0.351961 | 0.633333 |
| RE2-TT | CIRCA OLS+RHT+DA | 5 | khác | 45 | 45 | 0.279506 | 0.0735294 | 0.205977 | 0.720494 |
| RE2-TT | CIRCA OLS+RHT+DA | 5 | cùng | 10 | 10 | 0.46 | 0.0735294 | 0.386471 | 0.54 |
| RE2-TT | TORAI B | 1 | khác | 45 | 45 | 0.0839506 | 0.0147059 | 0.0692447 | 0.916049 |
| RE2-TT | TORAI B | 1 | cùng | 10 | 10 | 0.766667 | 0.0147059 | 0.751961 | 0.233333 |
| RE2-TT | TORAI B | 5 | khác | 45 | 45 | 0.399012 | 0.0735294 | 0.325483 | 0.600988 |
| RE2-TT | TORAI B | 5 | cùng | 10 | 10 | 0.56 | 0.0735294 | 0.486471 | 0.44 |
| Nezha-OB | BARO | 1 | khác | 78 | 78 | 0.0833333 | 0.1 | -0.0166667 | 0.916667 |
| Nezha-OB | BARO | 1 | cùng | 9 | 9 | 0.222222 | 0.1 | 0.122222 | 0.777778 |
| Nezha-OB | BARO | 5 | khác | 78 | 78 | 0.497436 | 0.5 | -0.0025641 | 0.502564 |
| Nezha-OB | BARO | 5 | cùng | 9 | 9 | 0.555556 | 0.5 | 0.0555556 | 0.444444 |
| Nezha-OB | SimpleRCA | 1 | khác | 78 | 78 | 0.101763 | 0.1 | 0.00176282 | 0.898237 |
| Nezha-OB | SimpleRCA | 1 | cùng | 9 | 9 | 0.388889 | 0.1 | 0.288889 | 0.611111 |
| Nezha-OB | SimpleRCA | 5 | khác | 78 | 78 | 0.522703 | 0.5 | 0.022703 | 0.477297 |
| Nezha-OB | SimpleRCA | 5 | cùng | 9 | 9 | 0.559259 | 0.5 | 0.0592593 | 0.440741 |
| Nezha-OB | MicroRank full | 1 | khác | 78 | 78 | 0.413462 | 0.1 | 0.313462 | 0.586538 |
| Nezha-OB | MicroRank full | 1 | cùng | 9 | 9 | 0.777778 | 0.1 | 0.677778 | 0.222222 |
| Nezha-OB | MicroRank full | 5 | khác | 78 | 78 | 0.94359 | 0.5 | 0.44359 | 0.0564103 |
| Nezha-OB | MicroRank full | 5 | cùng | 9 | 9 | 1 | 0.5 | 0.5 | 0 |
| Nezha-OB | TraceRCA | 1 | khác | 78 | 78 | 0.290064 | 0.1 | 0.190064 | 0.709936 |
| Nezha-OB | TraceRCA | 1 | cùng | 9 | 9 | 0.277778 | 0.1 | 0.177778 | 0.722222 |
| Nezha-OB | TraceRCA | 5 | khác | 78 | 78 | 0.718269 | 0.5 | 0.218269 | 0.281731 |
| Nezha-OB | TraceRCA | 5 | cùng | 9 | 9 | 0.822222 | 0.5 | 0.322222 | 0.177778 |
| Nezha-OB | CIRCA OLS+RHT+DA | 1 | khác | 0 | 78 | N/A | N/A | N/A | N/A |
| Nezha-OB | CIRCA OLS+RHT+DA | 1 | cùng | 0 | 9 | N/A | N/A | N/A | N/A |
| Nezha-OB | CIRCA OLS+RHT+DA | 5 | khác | 0 | 78 | N/A | N/A | N/A | N/A |
| Nezha-OB | CIRCA OLS+RHT+DA | 5 | cùng | 0 | 9 | N/A | N/A | N/A | N/A |
| Nezha-OB | TORAI B | 1 | khác | 0 | 78 | N/A | N/A | N/A | N/A |
| Nezha-OB | TORAI B | 1 | cùng | 0 | 9 | N/A | N/A | N/A | N/A |
| Nezha-OB | TORAI B | 5 | khác | 0 | 78 | N/A | N/A | N/A | N/A |
| Nezha-OB | TORAI B | 5 | cùng | 0 | 9 | N/A | N/A | N/A | N/A |

Bảng từng cặp ô và biến thiên seed ở `bang-theo-o-va-doi-chung.md`. Xác suất p_i,k(e) theo từng entity và L/|O| mỗi bản ghi ở `phan-phoi-top-k.md`, nguồn `ca-sai.json` → `/main_rows/*/evidence/seed_evidence/*/ranking/p_by_k`, `n`, `L` (phân số chính xác ở `p_by_k_exact`). Phương pháp một seed: biến thiên seed N/A. Non-OK và thiếu cặp không điền 0. 1−D gồm bất định phá hòa độc lập; D lặp lại không chứng minh thuật toán bỏ qua dữ liệu ca.

## 5. Tín hiệu root, proxy và schema

Bảng BARO root mọi ca (đúng/sai) ở `BARO-du-lieu-root.md` và `results/T-028/runs/buoc3-005/BARO-root-data.json`; từng metric/native service và nguồn nằm trong `results/T-028/runs/buoc3-005/ca-sai.json` → `evidence` và `features-no-label`. Đây là quy ước SimpleRCA (strict metric events, trace start P95, log keyword A), không phải luật BARO thực nhận hoặc chuẩn chung. Score BARO có dấu và coverage giữ cạnh dữ liệu; M6/local_nonpositive BARO=N/A.

Raw metric khác đầu vào sau preprocessing BARO. Không events không chứng minh không có tín hiệu; log lỗi A có thể là nền. Proxy end-split chỉ là bối cảnh BARO, khác bảng root trace start; P95 span không là end-to-end latency. Không thêm tỷ số khi nền bằng 0. Luật trace native ≥ cộng làm tròn có thể đánh dấu span không đổi khi σN bằng hoặc làm tròn về 0; native flag dương không tự chứng minh phân phối thay đổi (codebook §3.2).

Nguồn số độ nhạy: `results/T-028/runs/buoc3-005/summary-tables.json` → `proxy_tables`, giữ τ=2/3/4, mẫu số đủ/N/A và mã ca đổi cờ. Các bảng đầy đủ ở `bang-theo-o-va-doi-chung.md`. Proxy không đổi nhãn/primary; membership/status/hòa có độ nhạy N/A, không thêm tolerance.

Schema dùng audit có sẵn: `results/T-028/runs/buoc3-005/schema-tables.json`, nguồn `results/T-024/cham-a.json` → `raw_column_audit`. Đã xuất từng cột/ô, bảng chéo root, O/R/input_shape sau preprocessing và tên cột vắng. Bảng đọc được ở `schema-va-coverage.md`. Không classifier/L*/hoán vị nhãn; chưa tách tác động schema khỏi root, loại lỗi hoặc preprocessing. Nezha không có audit schema tương đương trong đầu vào được phép nên phần này N/A; không quét test.

## 6. Từng nhóm và các giải thích khác

### M1 — Root ngoài tập quan sát O

Rào cản trực tiếp: pipeline không quan sát root trong tập dùng cho lượt xếp hạng. Đã đối chiếu membership từ bản ghi. Chưa tách vì sao: coverage kênh, cửa sổ, mapping hay preprocessing. Không chứng minh root không có lỗi. Can thiệp tăng coverage hoặc giữ preprocessing cần chạy lại phương pháp, ngoài SPEC.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

Không có ca OK sai được gán nhóm này trong bảng chính.

### M2 — Root thuộc O nhưng ngoài tập trả về R

Rào cản trực tiếp của luật trả về. Đã kiểm O/R. TraceRCA lọc ji không hữu hạn; nếu M6 True thì có chuỗi không span A dương theo luật native ⇒ ji NaN ⇒ ngoài R. Chiều ngược chưa được suy: chỉ có N, thiếu baseline hoặc điều kiện khác cũng có thể làm root ngoài R. Trung gian ji không được lưu đầy đủ nên không chạy lại để điền. Các khả năng khác gồm lọc điểm, thiếu quan sát hoặc mapping.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

| Dataset | Phương pháp | k | Đa nhãn / OK sai | Đa nhãn / cohort |
| --- | --- | --- | --- | --- |
| Nezha-OB | TraceRCA | 1 | 1/20 | 1/22 |
| Nezha-OB | TraceRCA | 5 | 1/11 | 1/22 |

### M3 — Hòa cắt biên top-k

Phân rã trực tiếp bất định hòa từ phân phối chính xác từng seed. Đã kiểm full key, nhóm hòa và khối TORAI; khác thắng/thua giữa seed không bị gọi là hòa. Hòa không giải thích tại sao các điểm giống nhau. Có thể do luật đếm rời rạc, điểm giống nhau, candidate/coverage hoặc thứ tự nội khối. Không đổi tolerance hoặc phá hòa theo nhãn.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

| Dataset | Phương pháp | k | Đa nhãn / OK sai | Đa nhãn / cohort |
| --- | --- | --- | --- | --- |
| Nezha-OB | SimpleRCA | 5 | 1/4 | 1/22 |
| Nezha-OB | TraceRCA | 1 | 1/20 | 1/22 |
| Nezha-OB | TraceRCA | 5 | 1/11 | 1/22 |

### M4 — CIRCA thuộc cohort lỗi làm tròn đã xác nhận

Membership dùng danh sách loại dev19 đã khóa. Đã kiểm diagnostics.nodes sau prune, RHT và full key DA trong các ca đọc tay. Đây là lỗi số học xác nhận cấp ca; chưa chứng minh nó gây từng thất bại của root/DA. Tín hiệu raw, quan hệ gọi, preprocessing và mô hình hồi quy vẫn có thể giải thích một thứ hạng. Không chạy bản sửa/ablation trong task.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

| Dataset | Phương pháp | k | Đa nhãn / OK sai | Đa nhãn / cohort |
| --- | --- | --- | --- | --- |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | 8/14 | 8/30 |

### M5 — Ancestor quan sát được chắc chắn trước root

Ứng viên: ancestor trong graph N và ưu tiên thứ hạng cùng xuất hiện. Đã kiểm cha-con trong N, graph quality, full key/khối, proxy P95 và P0 có điều kiện. Chưa xác định thứ tự khởi phát, lan, caller tự bất thường, tải/tài nguyên chung hoặc sự cố đồng thời. P0 không giữ thiên hướng nhận điểm riêng của entity, số kênh/operation hay cấu trúc chấm điểm. Coverage, clock/nền/nhãn, lỗi graph/mapping, thành phần cohort và dao động hữu hạn còn là giải thích khả thi. Can thiệp hoặc đối chứng giữ những yếu tố đó cần phạm vi khác; không được chạy ở đây.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

| Dataset | Phương pháp | k | Đa nhãn / OK sai | Đa nhãn / cohort |
| --- | --- | --- | --- | --- |
| Nezha-OB | BARO | 1 | 7/14 | 7/22 |
| Nezha-OB | BARO | 5 | 3/6 | 3/22 |
| Nezha-OB | MicroRank full | 1 | 20/22 | 20/22 |
| Nezha-OB | MicroRank full | 5 | 14/14 | 14/22 |
| Nezha-OB | SimpleRCA | 1 | 9/15 | 9/22 |
| Nezha-OB | SimpleRCA | 5 | 2/4 | 2/22 |
| Nezha-OB | TraceRCA | 1 | 16/20 | 16/22 |
| Nezha-OB | TraceRCA | 5 | 10/11 | 10/22 |
| RE2-TT | BARO | 1 | 3/9 | 3/30 |
| RE2-TT | BARO | 5 | 2/4 | 2/30 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | 10/14 | 10/30 |
| RE2-TT | MicroRank full | 1 | 5/24 | 5/30 |
| RE2-TT | MicroRank full | 5 | 5/13 | 5/30 |
| RE2-TT | SimpleRCA | 1 | 5/5 | 5/30 |
| RE2-TT | SimpleRCA | 5 | 1/1 | 1/30 |
| RE2-TT | TORAI B | 1 | 1/4 | 1/30 |
| RE2-TT | TraceRCA | 1 | 4/5 | 4/30 |
| RE2-TT | TraceRCA | 5 | 1/1 | 1/30 |

### M6 — Không có bằng chứng cục bộ dương theo luật native

Ứng viên phụ thuộc phương pháp. SimpleRCA dùng score lưu sẵn bằng 0, MicroRank/TraceRCA dùng baseline hữu hạn và không span A đạt luật đã khai, CIRCA xét tập không rỗng trong diagnostics.nodes sau prune với mọi RHT<3. BARO/TORAI N/A. Đã kiểm arithmetic/cửa sổ/availability và độ nhạy proxy; không coi missing là bình thường. Giảm tín hiệu, kênh khác, cửa sổ/clock không khớp, nền chưa sạch, nhãn hoặc coverage vẫn có thể giải thích. Đổi tín hiệu/threshold hoặc chạy can thiệp ngoài phạm vi.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

| Dataset | Phương pháp | k | Đa nhãn / OK sai | Đa nhãn / cohort |
| --- | --- | --- | --- | --- |
| Nezha-OB | MicroRank full | 1 | 1/22 | 1/22 |
| Nezha-OB | MicroRank full | 5 | 1/14 | 1/22 |
| Nezha-OB | SimpleRCA | 1 | 2/15 | 2/22 |
| Nezha-OB | SimpleRCA | 5 | 2/4 | 2/22 |
| Nezha-OB | TraceRCA | 1 | 1/20 | 1/22 |
| Nezha-OB | TraceRCA | 5 | 1/11 | 1/22 |

### M0 — Chưa phân loại

Không có M1–M6 True ở seed sai đủ điều kiện theo quy tắc đã chốt. Giữ cả False và N/A; không tạo cơ chế sau khi nhìn kết quả. Đã đọc tay mẫu cố định, lưu score/thứ hạng/availability. Cấu trúc chấm điểm, tín hiệu nhiều nguồn, giảm tín hiệu, coverage và nền/nhãn có thể còn giải thích; dữ liệu quan sát chưa phân xử nguyên nhân.

Nguồn mọi số nhóm: `results/T-028/runs/buoc3-005/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `results/T-028/runs/buoc3-005/manual-reading.json` và `doc-tay.md`.

| Dataset | Phương pháp | k | Đa nhãn / OK sai | Đa nhãn / cohort |
| --- | --- | --- | --- | --- |
| Nezha-OB | BARO | 1 | 7/14 | 7/22 |
| Nezha-OB | BARO | 5 | 3/6 | 3/22 |
| Nezha-OB | MicroRank full | 1 | 2/22 | 2/22 |
| Nezha-OB | SimpleRCA | 1 | 6/15 | 6/22 |
| Nezha-OB | SimpleRCA | 5 | 1/4 | 1/22 |
| Nezha-OB | TraceRCA | 1 | 2/20 | 2/22 |
| RE2-TT | BARO | 1 | 6/9 | 6/30 |
| RE2-TT | BARO | 5 | 2/4 | 2/30 |
| RE2-TT | CIRCA OLS+RHT+DA | 1 | 4/14 | 4/30 |
| RE2-TT | CIRCA OLS+RHT+DA | 5 | 3/3 | 3/30 |
| RE2-TT | MicroRank full | 1 | 19/24 | 19/30 |
| RE2-TT | MicroRank full | 5 | 8/13 | 8/30 |
| RE2-TT | TORAI B | 1 | 3/4 | 3/30 |
| RE2-TT | TraceRCA | 1 | 1/5 | 1/30 |

## 7. Đối chiếu lời tác giả

| Phương pháp | Giới hạn tác giả/hồ sơ | Nguồn |
| --- | --- | --- |
| BARO | Giả định metric ảnh hưởng latency/error; lỗi tương quan có thể đưa nhiều affected service lên hạng; khái quát deployment/fault còn hạn chế. | results/T-013/ho-so-baro.md §6; docs/knowledge/K1-phuong-phap-rca.md |
| SimpleRCA | Type I/II; threshold-count kém khi lỗi tinh tế/mạng và root không ồn nhất; triệu chứng đơn giản không là chứng minh nhân quả. | results/T-017/ho-so-simplerca.md §6 |
| MicroRank | Lỗi không lệch latency, thiếu trace/instrumentation, overhead và tính reactive; detector không phủ mọi hệ. | results/T-015/ho-so-microrank.md §6 |
| TraceRCA RCAEval | Hồ sơ không có giới hạn riêng tác giả; điều kiện baseline/ji/zero-std là suy từ code, không quy cho bài gốc. | results/T-015/tracerca-rcaeval.md §6 |
| CIRCA | Nền chưa phủ parent values gây bias; meta/common cause ẩn, DA cần thêm dữ liệu thực. | results/T-014/ho-so-circa-kien-truc.md §6 |
| TORAI | Root indicator cần đổi rõ; root yếu có thể đưa affected service lên đầu; lệch mốc và tool/system/fault hạn chế kết luận. | results/T-016/ho-so-torai.md §6 |

Lời tác giả là căn cứ đối chiếu khái niệm. Không chuyển thành kết luận cơ chế đã xác nhận trên cohort T-028. Các lỗi triển khai đã sửa và các giả thuyết đọc từ code được tách khỏi lời tác giả.

## 8. Bảng phụ, kiểm và giới hạn

CIRCA dev19 dùng lại evidence dev30, giữ danh sách loại lỗi làm tròn; số/bằng chứng ở `results/T-028/runs/buoc3-005/ca-sai.json` → `circa_dev19_conditional`, không thay mẫu chính. Nezha A/B/trace_guard chỉ giữ status/Hit có sẵn ở `nezha_saved_sensitivity_flags`; ca ngoài B giữ not_in_cohort, không có đặc trưng hoặc cơ chế mới.

Kiểm độc lập: `results/T-028/runs/buoc3-005/independent-ranking.json`, `results/T-028/runs/buoc3-005/independent-statistics.json`, `results/T-028/runs/buoc3-005/provenance-checks.json`; tự kiểm/phạm vi cuối ở `results/T-028/runs/buoc3-005/final-verification.json`. Mẫu theo mã mờ tăng dần đã khai tại codebook §8; không chọn theo root/Hit hoặc giá trị đặc trưng. Đọc tay: `results/T-028/runs/buoc3-005/manual-reading.json`, `doc-tay.md`; mọi seed liên quan được giữ.

RE2 có ít root và graph N lặp lại; Nezha cadence metric thưa, cửa sổ trace N ngắn, clock/mốc/nền sạch còn OPEN theo WHY-37 và nguồn T-026. Giữ các khác biệt U, loại lỗi, độ dài N; so sánh hai dataset chỉ mô tả, không gộp độ chính xác. Test/giữ ngoài chưa mở nên tính đại diện chưa kiểm.

Bằng chứng kiểm được tới membership, hòa, score/diagnostics lưu sẵn, luật thống kê native, quan hệ caller trong N, schema và mức nền có điều kiện. Chưa phân xử nhân quả, thứ tự khởi phát hoặc các giải thích cạnh tranh đã nêu. Việc chạy lại phương pháp với đầu vào khác/can thiệp nằm ngoài SPEC; không điền trung gian bằng rerun.

Nơi xử lý câu “lan có đáng kể” vẫn OPEN vì Minh chưa chọn. T-028 không tự giao T-029, không biến câu hỏi đó thành cổng mới. Bằng chứng ở đây là đầu vào cho quyết định tiếp theo của Minh.

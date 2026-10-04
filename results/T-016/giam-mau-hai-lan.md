# Lỗi giảm mẫu hai lần và ghép theo chỉ số trong TORAI (RCAEval `259ea41`)

T-016, yêu cầu 2. Nguồn số: `runs/s4-soi-dau-vao-*.jsonl` (soi đầu vào), `cham/s7-tong-hop.json`, `cham/s10-tong-hop.json` (điểm và giá trị trung gian, mọi seed), `cham/bang-so-cong-bo.md` (bảng so với bài), `runs/s12-tinh-tay-*.json` (ví dụ tính tay), `runs/s5-diff.txt` (bản sửa).

## 1. Kết luận ngắn

- **Có lỗi, gồm hai chỗ liền nhau** ở hàm `_rcd_multimodal` (bước CausalRanker):
  - (A) metric bị giảm mẫu 1/15 **hai lần** (`torai.py:81` rồi `:29`);
  - (B) metric và log được ghép bằng `pd.concat(axis=1)` **theo chỉ số dòng**, trong khi metric giữ chỉ số gốc (0, 15, 30, …) còn log có chỉ số 0, 1, 2, … (`torai.py:47-48`).
- Hệ quả với lệnh chính thức (`--length 10`): RCD trong cụm **không nhận cột metric nào** (90/90 ca OB, 90/90 SS, 30/30 TT) và mỗi nửa thêm 1 dòng giả toàn 0. Với `--length 20`: metric vào được nhưng chỉ ở 2–3 dòng lệch thời gian, không trùng dòng nào của log.
- Đây nhiều khả năng là **lỗi khi chuyển code** (mục 3), không phải chủ ý. Không có lời tác giả để khẳng định.
- **Sửa hai chỗ gần như không đổi điểm** (lệch Avg@5 từ −0,007 đến +0,003, ngang dao động giữa các seed). Lý do: ở cả bản gốc lẫn bản sửa, đa số cụm rơi vào nhánh dự phòng về thứ tự mức nghiêm trọng (bản gốc cửa sổ 10: 176/184 cụm OB, 171/173 SS, 72/72 TT). Thứ hạng cuối của TORAI gần như là thứ hạng của SeverityScorer + GMM.
- **Đề xuất cho P3:** dùng bản sửa (`src/torai/`, bản cài RCAEval đã sửa hai lỗi, chưa tương đương TORAI của bài) làm TORAI chính, kèm báo tỉ lệ nhánh dự phòng; giữ bản gốc làm mốc tái lập (mục 7; lý do ở `docs/WHY.md` WHY-19).

## 2. Bằng chứng trên code

`main.py` cắt metric `L·30` dòng mỗi phía mốc tiêm (`main.py:314-315`), 1 dòng/giây.

| Bước | Cửa sổ 10 (600 dòng) | Cửa sổ 20 (1 200 dòng) |
|---|---|---|
| `torai.py:81` `iloc[::15]` | chỉ số 0, 15, …, 585 → 20 normal + 20 anomal | 40 + 40 |
| `torai.py:295` lấy cột của cụm từ metric **đã giảm** | 40 dòng | 80 dòng |
| `torai.py:29` `iloc[::15]` lần nữa | chỉ số gốc 0, 225, 450 → **2 normal + 1 anomal** | 0, 225, …, 1 125 → 3 + 3 |
| `preprocess` bỏ cột hằng riêng từng nửa (`time_series.py:5`) | nửa anomal 1 dòng: mọi cột hằng → **0 cột metric** | còn cột có biến thiên trên 3 điểm |
| `concat(axis=1)` với logts (chỉ số 0–19 / 20–39 hoặc 0–39 / 40–79) | hợp chỉ số: normal `{0, 225, 1…19}` = 21 dòng, anomal `{450, 20…39}` = 21 dòng; dòng 225, 450 không có log → điền 0 | normal 42–43 dòng: 40 dòng log + 2–3 dòng chỉ có metric; ô thiếu điền 0; không dòng nào có cả metric lẫn log, trừ chỉ số 0 |

`mmnsigma` cùng tác giả giảm mẫu một lần (`baro.py:86`); `mmrcd` ghép log/trace vào metric **theo thời gian** bằng `merge_asof` (`mmrcd.py:427-444`). Chú thích `torai.py:80` viết "the metric is sampled every second, resample for 15s" — nói một lần giảm. Docstring `_rcd_multimodal` ghi "Ported from cfm/e2e/rcd.py multimodal branch" (`torai.py:23-24`).

## 3. Bằng chứng trên ca, cả hai cửa sổ

**Soi đầu vào, không chạy RCD** (`scripts/soi_dau_vao.py`, toàn bộ metric, không theo cụm):

| Dataset | Cửa sổ | Dòng sau giảm 2 lần (normal + anomal) | Cột metric sống sót sau giảm 2 lần | Sau giảm 1 lần |
|---|---|---|---|---|
| torai-OB (90 ca) | 10 | 2 + 1 (90/90) | **0 (90/90)** | 20 + 20; ≥ 44 cột |
| torai-OB | 20 | 3 + 3 (89/90; 1 ca 3 + 2) | 42–45 | 40 + 40; ≥ 44 cột |
| torai-SS (90 ca) | 10 | 2 + 1 | **0 (90/90)** | ≥ 50 cột |
| torai-SS | 20 | 3 + 3 | 47–50 | ≥ 51 cột |
| TT dev (30 ca) | 10 | 2 + 1 | **0 (30/30)** | ≥ 261 cột |
| TT dev | 20 | 3 + 3 | 257–267 | ≥ 269 cột |

**Thu giá trị trung gian khi chạy bản gốc** (wrapper chỉ quan sát, seed 0, `cham/s7-tong-hop.json`, `cham/s10-tong-hop.json`):

| Cấu hình | Cụm ≥ 2 service | Cột metric vào RCD | Dòng vào RCD (normal + anomal) | Dòng toàn 0 |
|---|---|---|---|---|
| OB gốc, 10 | 184 | 0 ở mọi cụm | 21 + 21 (182 cụm) | 2 253 |
| SS gốc, 10 | 173 | 0 ở mọi cụm | 21 + 21 | 3 061 |
| TT gốc, 10 | 72 | 0 ở mọi cụm | 21 + 21 | 1 278 |
| OB gốc, 20 | 197 | 2–40 (TB 17,3) | 42 + 43 (191 cụm) | 4 558 |
| OB sửa, 10 | 184 | 4–42 (TB 19,4) | 20 + 20 (182 cụm) | 0 |
| OB sửa, 20 | 197 | 4–42 (TB 18,1) | 40 + 40 (191 cụm) | 0 |

Ví dụ tay ca `checkoutservice_cpu/1` (`vi-du-tinh-tay.md` mục 4): hai dòng giả của cột `cartservice_13` tạo riêng một bin rời rạc hóa (tâm 0).

## 4. Lỗi hay chủ ý

**Nhận định:** lỗi khi chuyển code (port) từ một nhánh khác sang `torai.py`. Lý do:
1. Chú thích ở `:80` mô tả **một** lần giảm để metric khớp chu kỳ 15 s của log; tài liệu RCAEval ghi metric 1 s, logts/tracets 15 s (`docs/TORAI.md`, mục Data Format).
2. `_rcd_multimodal` nhận metric **đã giảm** (`:295`) nhưng tự giảm lại (`:29`), đúng hành vi nếu hàm được viết cho metric thô 1 s (docstring "Ported from …").
3. Với lệnh của chính tác giả (`--length 10`), lần giảm thứ hai xóa toàn bộ metric khỏi bước nhân quả. Bài §3.4 và Hình 3 mô tả đồ thị nhân quả có nút CPU, ErrLog, TraceLat — trái với hành vi này.
4. Hàm cùng tác giả `mmnsigma` giảm một lần; `mmrcd` ghép theo thời gian. Ghép theo chỉ số ở `torai.py:47-48` sinh dòng giả, trái với cách ghép ở `mmrcd`.

**Về câu "bài nói metric được lấy lại mẫu 15 giây"** (prompt T-016, ghi chú REVIEW T-005 R1): đã tìm trong văn bản HTML bài TORAI (`2604.13522v1`): **bài không nêu chu kỳ 15 s ở đâu**; §3.1 chỉ nói đếm mẫu log theo thời gian ("bins the occurrence"). Chu kỳ 15 s chỉ có ở `docs/TORAI.md` và chú thích code. Đính chính ở `dinh-chinh-task-cu.md` mục D2.

**Nguyên nhân khả thi khác (Q-33), và vì sao chưa loại hẳn:**
- (a) Tác giả cố ý giảm vai trò metric trong RCD (ví dụ để RCD tập trung vào log). Không có câu nào trong bài, tài liệu hay chú thích ủng hộ; Hình 3 của bài ngược lại. Không loại hẳn được vì không có lời tác giả.
- (b) Số trong bài được tạo bằng code khác `torai.py` hiện tại. Nhánh `fse26` (bài TORAI) có `torai.py` giống hệt `main` (LOG phiên 1). Bản gốc cửa sổ 10 tái lập `docs/TORAI.md` (mốc A) tới ±0,03 mỗi ô (T-006 mục 7; ở đây trung bình 5 seed lệch ≤ 0,027 mỗi ô, mục 5). Nên số công bố nhiều khả năng được tạo bằng chính code có lỗi.
- (c) Dữ liệu của tác giả lúc chạy có chu kỳ metric 15 s (khi đó một lần giảm là đủ, hai lần vẫn sai). Dữ liệu Figshare có metric 1 s (1 441 dòng / 24 phút).

## 5. Bản sửa và kết quả

**Bản sửa** (`src/torai/torai_sua.py`; `runs/s5-diff.txt` chỉ khác ở các dòng ghi "T-016 sửa"): (A) bỏ lần giảm thứ hai; (B) trong mỗi nửa, đặt lại chỉ số rồi ghép theo vị trí, cắt về độ dài chung (nửa normal giữ các dòng sát mốc, nửa anomal giữ các dòng đầu). Biến thể chỉ (A) để tách tác động.

**Điểm** (trung bình 5 seed với OB, SS; 3 seed với TT dev; mức service; `cham/bang-so-cong-bo.md`):

| Dataset, nguồn, cửa sổ | Bản gốc Avg@5 (sd) | Bản sửa Avg@5 (sd) | Sửa − gốc | Mốc bài (Avg@5) | Gốc − bài | SeverityScorer không cụm (seed 0) |
|---|---|---|---|---|---|---|
| OB, M+L+T, 10 | 0,913 (0,000) | 0,909 (0,003) | −0,004 | 0,93 (Bảng 2) | −0,017 | 0,922 |
| OB, M+L+T, 20 | 0,926 (0,002) | 0,928 (0,004) | +0,002 | 0,93 | −0,004 | 0,933 |
| OB, M+L, 10 | 0,908 (0,001) | 0,905 (0,004) | −0,003 | 0,91 (Bảng 2) | −0,002 | 0,909 |
| SS, M+L, 10 | 0,952 (0,001) | 0,955 (0,003) | +0,003 | 0,94 (Bảng 3) | +0,012 | 0,951 |
| SS, M+L, 20 | 0,941 (0,001) | 0,940 (0,003) | −0,001 | 0,94 | +0,001 | 0,938 |
| TT dev 30 ca, M+L+T, 10 | 0,880 (0,000) | 0,880 (0,000) | 0,000 | không so (60/90 ca TT là test) | — | 0,873 |
| TT dev 30 ca, M+L+T, 20 | 0,820 (0,000) | 0,813 (0,000) | −0,007 | không so | — | 0,820 |

- Biến thể chỉ (A), OB cửa sổ 10, seed 0: 0,911 (gốc seed 0: 0,913; sửa seed 0: 0,911).
- `docs/TORAI.md` (mốc A, OB, Avg@5 theo lỗi 0,96/0,93/1,0/0,93/0,8/0,84): bản gốc cửa sổ 10 trung bình 5 seed 0,960/0,933/1,000/0,920/0,800/0,867 → mọi ô lệch ≤ 0,027 (LOSS +0,027). Khớp như T-006.
- Mọi cấu hình đều "khớp" theo tiêu chí SPEC (AVERAGE lệch ≤ 0,05), cả bản sửa. Tức số công bố **không phân biệt được** bản gốc và bản sửa.

**Vì sao sửa không đổi điểm — nhánh dự phòng** (seed 0, `cham/s7-tong-hop.json`, `cham/s10-tong-hop.json`):

| Cấu hình | Cụm rơi dự phòng / cụm ≥ 2 service | Ca có thứ hạng cuối = thứ hạng "chỉ mức nghiêm trọng" |
|---|---|---|
| OB gốc 10 | 176 / 184 | 86 / 90 |
| OB sửa 10 | 166 / 184 | 80 / 90 |
| OB gốc 20 | 173 / 197 | 79 / 90 |
| OB sửa 20 | 165 / 197 | 74 / 90 |
| SS gốc 10 | 171 / 173 | 88 / 90 |
| SS sửa 10 | 166 / 173 | 85 / 90 |
| TT gốc 10 | 72 / 72 | 30 / 30 |
| TT sửa 10 | 67 / 72 | 28 / 30 |

"Thứ hạng chỉ mức nghiêm trọng" = xếp cụm theo điểm cụm, trong cụm theo điểm service (đúng nhánh dự phòng). Nhánh dự phòng xảy ra khi danh sách service RCD trả không dài bằng số service của cụm: RCD thường chỉ tìm được 1–4 nút liên quan F-node, ít hơn số service trong cụm; với SS, cột `*-db_*` lọt vào cụm (va chạm tiền tố, hồ sơ C8) cũng làm danh sách không khớp. Ở ca nào RCD có ảnh hưởng (cụm nhỏ, đủ service), nó đổi thứ tự trong cụm, nhưng số ca này ít (2–16 ca/90 ở OB, SS, tính bằng 90 trừ cột cuối của bảng) và điểm tăng giảm trái chiều.

**Hệ quả cho cách hiểu số của bài** (chưa kiểm hết, chỉ trên dữ liệu ở đây): trên OB cửa sổ 10, SeverityScorer một mình (không gom cụm, không RCD) đạt Avg@5 0,922, cao hơn TORAI đầy đủ (0,913). Bảng 9 của bài cũng cho SeverityScorer gần TORAI (OB M+L+T: 0,92 so với 0,93). Phần đóng góp của CausalRanker mà bài nêu nhỏ, và trên code này phần lớn do nhánh dự phòng thay RCD.

## 6. Xung đột giữa "tái lập số công bố" và "chạy đúng phương pháp"

- **Tái lập** cần đúng code tác giả, kể cả lỗi: bản gốc cửa sổ 10 khớp `docs/TORAI.md` và Bảng 2, 3. Đây là bằng chứng môi trường, dữ liệu, cách chấm của nhóm đúng.
- **Chạy đúng hơn ở bước nhân quả** (theo bài §3.4: RCD phân tích chuỗi metric, log của các service trong cụm) cần bản sửa. Bản gốc ở cửa sổ 10 là "TORAI không có metric trong bước nhân quả". Bản sửa chỉ là **bản cài RCAEval đã sửa hai lỗi**, chưa phải TORAI của bài: các khác biệt C4–C7 (gán cụm cứng, bỏ trace trong RCD, trọng số nguồn, nhánh dự phòng) vẫn còn, và cách ghép (B) là cách hiểu chưa kiểm (sửa theo REVIEW R3).
- Ở dữ liệu này, hai mục tiêu cho cùng số (lệch ≤ 0,007), nên xung đột **không đổi kết quả P3 về điểm**. Nhưng nó đổi **cách diễn giải ở P4**: nếu dùng bản gốc, mọi hạn chế quan sát được ở bước nhân quả có thể chỉ là hệ quả của lỗi; nếu dùng bản sửa, hạn chế đó thuộc về bản cài RCAEval đã sửa hai lỗi. Quy hạn chế cho TORAI theo bài vẫn OPEN cho tới khi loại được các khác biệt C4–C7.
- Xung đột thứ hai, lớn hơn: nhánh dự phòng (C7) có trong cả hai bản. Nó không phải lỗi rõ ràng (có thể là lựa chọn an toàn của tác giả) nên không sửa. Nhưng nó làm TORAI thực chất là "SeverityScorer + GMM" ở đa số ca. P3, P4 cần báo tỉ lệ này cạnh điểm.

## 7. Đề xuất bản dùng cho P3 (chưa kiểm ngoài các số trên; WHY-19, đã ghi 04/10)

1. TORAI chính ở P3 = bản sửa `src/torai/torai_sua.py` (A + B), tức bản cài RCAEval đã sửa hai lỗi. Lý do: bản này đưa được metric vào bước nhân quả như bài §3.4 mô tả, mà không đổi bước nào khác. Nó chưa tương đương TORAI của bài (C4–C7 còn nguyên), nên kết luận P4 dựa trên nó chỉ nói về bản cài này.
2. Chạy kèm bản gốc trên **một** dataset (torai-OB) làm mốc tái lập, không dùng để kết luận về phương pháp.
3. Mỗi lượt báo thêm: tỉ lệ cụm rơi nhánh dự phòng, số ca thứ hạng cuối trùng thứ hạng chỉ mức nghiêm trọng, và điểm SeverityScorer không cụm (lấy được từ giá trị trung gian, không cần chạy thêm).
4. Đặt seed theo ca (`np.random.seed(seed)` trước mỗi lời gọi) và chạy ít nhất 3 seed (`ngau-nhien.md`).
5. Độ dài cửa sổ: theo quyết định ở G1 (Q-54). Ghi chú cho G1: với cửa sổ 20, bản gốc đã có metric (lệch thời gian) nên khoảng cách gốc–sửa còn nhỏ hơn.

Giả định của đề xuất: cách ghép theo vị trí (B) đúng ý "ghép cột cùng thời điểm". Sai nếu tác giả muốn ghép theo thời gian thật (`merge_asof` như `mmrcd`): khi đó lưới metric (theo mốc tiêm) và lưới log (theo đầu file) lệch nhau tối đa 14 s mỗi dòng (lệch pha đo được 0–14 s, `runs/s4-soi-dau-vao-*.jsonl`). Chưa kiểm cách ghép theo thời gian, vì phải chọn quy tắc làm tròn mà bài không nêu.

Lý do đã ghi ở `docs/WHY.md` WHY-19 (Minh duyệt 04/10).

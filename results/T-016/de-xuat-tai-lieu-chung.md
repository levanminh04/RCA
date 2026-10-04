# Đề xuất cho tài liệu chung (nháp nguyên văn, chờ Minh duyệt)

> **Đã áp (Minh duyệt 04/10/2026: "duyệt đề xuất và sửa đổi nhưng chưa commit").** Số thật lúc ghi (các số tạm đã bị T-017, T-018 dùng): W1 → `docs/WHY.md` **WHY-19**; W2 → **WHY-20**; L1 → `docs/LESSONS.md` **SL36**; K1 → `docs/knowledge/K1-phuong-phap-rca.md` C.5, C.8; D1 → `docs/DECISIONS.md` **Q-57** (gộp ủy quyền SPEC và hai lần duyệt của Minh cho T-016). L2, R1 đã rút. Nội dung dưới giữ nguyên làm hồ sơ.

T-016 không ghi các file dưới đây. Mỗi mục: file đích, đoạn cũ → đoạn mới, lý do, kết luận phụ thuộc. Số mục (WHY-xx, SLxx, Q-xx) là số tạm; người ghi dịch lên nếu phiên khác đã dùng số đó (rà lại 04/10 sau phản biện: WHY cuối là WHY-17, LESSONS cuối SL34, DECISIONS cuối Q-55 — đã do T-017 dùng — nên nháp T-016 dùng WHY-18, WHY-19, SL35, Q-56).

## W1 — `docs/WHY.md`: thêm mục bản TORAI dùng cho P3

- **File đích:** `docs/WHY.md`, thêm vào cuối file.
- **Đoạn cũ:** (không có).
- **Đoạn mới:**

```markdown
## WHY-18. Bản TORAI dùng cho P3: bản sửa hai chỗ trong `src/torai/` — Đề xuất (G1) (T-016)

- **Chọn:** TORAI chính ở P3 là `src/torai/torai_sua.py`: code RCAEval `259ea41` chép nguyên văn, chỉ sửa (A) bỏ lần giảm mẫu metric thứ hai trong `_rcd_multimodal` (`torai.py:29`) và (B) ghép metric với logts theo vị trí trong từng nửa thay cho `concat` theo chỉ số (`torai.py:47-48`). Bản gốc chạy kèm trên torai-OB làm mốc tái lập. Đặt seed theo ca, ít nhất 3 seed. Mỗi lượt báo tỉ lệ cụm rơi nhánh dự phòng và điểm SeverityScorer không cụm.
- **Vì sao:** ở lệnh chính thức (`--length 10`), bản gốc đưa 0 cột metric vào bước nhân quả ở mọi ca OB, SS, TT dev đã thử, trái với bài §3.4 (CausalRanker phân tích chuỗi metric và log). Bản sửa đưa metric vào bước nhân quả như bài mô tả mà không đổi bước nào khác. Nó là bản cài RCAEval đã sửa hai lỗi, chưa tương đương TORAI của bài: gán cụm cứng, bỏ trace trong RCD, trọng số nguồn khác và nhánh dự phòng vẫn còn (`ho-so-torai.md` C4–C7). Lỗi nhiều khả năng do chuyển code: chú thích `torai.py:80` mô tả một lần giảm; `mmnsigma` giảm một lần; `mmrcd` ghép theo thời gian (`results/T-016/giam-mau-hai-lan.md` mục 4).
- **Phương án đã xét:**
  - Bản gốc nguyên trạng: tái lập số công bố, nhưng là "TORAI không có metric trong bước nhân quả"; hạn chế thấy ở P4 có thể chỉ là hệ quả của lỗi.
  - Bản sửa ghép theo thời gian (`merge_asof` như `mmrcd`): cần tự chọn quy tắc làm tròn giữa lưới metric (theo mốc tiêm) và lưới log (theo đầu file, lệch 0–14 s); bài không nêu. Chưa kiểm.
  - Sửa thêm (đưa trace vào RCD, GMM gán mềm, bỏ nhánh dự phòng): là thay đổi phương pháp, không phải sửa lỗi; không làm.
- **Bằng chứng:** `results/T-016/giam-mau-hai-lan.md` mục 3, 5; trung bình 5 seed, Avg@5 bản gốc / bản sửa: OB cửa sổ 10 0,913 / 0,909; OB 20 0,926 / 0,928; SS 10 0,952 / 0,955; SS 20 0,941 / 0,940; TT dev 10 0,880 / 0,880. Hai bản cho cùng điểm trong dao động giữa seed, vì phần lớn cụm rơi nhánh dự phòng ở cả hai (OB cửa sổ 10: 176/184 và 166/184 cụm).
- **Giới hạn:** chọn bản sửa không làm điểm tốt hơn; chỉ sửa hai lỗi đầu vào của bước nhân quả. Kết luận P3, P4 dựa trên bản này nói về bản cài RCAEval đã sửa; quy hạn chế cho TORAI theo bài vẫn OPEN ở các khác biệt C4–C7. Cửa sổ P3 chưa chốt (Q-54). Cách ghép (B) theo vị trí là một cách hiểu ý tác giả (chưa kiểm cách khác).
- **Kết luận phụ thuộc:** mọi số TORAI ở P3; mọi nhận định ở P4 về bước CausalRanker của TORAI.
```

- **Lý do:** luật cứng 3 (lựa chọn quan trọng phải có WHY trước khi dùng trong kết quả).
- **Kết luận phụ thuộc:** như trong đoạn.

## W2 — `docs/WHY.md`: seed và số lần chạy cho phương pháp có ngẫu nhiên

- **File đích:** `docs/WHY.md`, sau W1.
- **Đoạn mới:**

```markdown
## WHY-19. Đặt seed theo ca và số lần chạy cho TORAI, RCD — Đề xuất (G1) (T-016)

- **Chọn:** gọi `np.random.seed(s)` ngay trước mỗi lời gọi phương pháp cho từng ca; TORAI ít nhất 3 seed; RCD số seed tối đa vừa ngân sách Q-40 của dataset đó, tối thiểu 1, và ghi rõ số seed (RCD torai-OB cửa sổ 20 tốn 1,56 giờ/seed, TT khoảng 74 phút/seed, nên 5 seed vượt Q-40); báo trung bình và khoảng; phân tích từng ca dùng mọi seed.
- **Vì sao:** RCAEval không đặt seed (`rcd.py:458`; `torai()` không có tham số seed), nên một lượt `main.py` không lặp lại được. Với seed đặt theo ca, TORAI tất định: cùng seed hai lần, khác `PYTHONHASHSEED`, Linux và Windows đều cho thứ hạng giống hệt 90/90 ca (`results/T-016/ngau-nhien.md` mục 3). Giữa các seed, TORAI đổi thứ hạng ở tới 24/90 ca, top-1 tới 9/90 ca, dù sd Avg@5 ≤ 0,004 (mục 4); RCD dao động lớn hơn nhiều (T-006: 2–6/90 ca trùng thứ hạng giữa các lần).
- **Phương án đã xét:** không đặt seed như RCAEval (không tái lập được); seed 420 cố định như RCD gốc (tái lập được nhưng che dao động); trung bình 5 lần như bài (§4.2) mà không ghi seed (không tái lập được).
- **Kết luận phụ thuộc:** số TORAI, RCD ở P3; phân tích từng ca ở P4.
```

## L1 — `docs/LESSONS.md`: khớp số công bố không chứng minh phương pháp chạy đúng

- **File đích:** `docs/LESSONS.md`, bảng "Sai lầm không được lặp lại", thêm dòng sau SL34 (SL34 do T-017 ghi).
- **Đoạn mới:**

```markdown
| SL35 | Kết luận "TORAI khớp" chỉ dựa vào điểm cuối khớp số công bố (T-006). Ở đúng cấu hình đó, bước nhân quả không nhận cột metric nào do lỗi giảm mẫu hai lần, và 176/184 cụm rơi nhánh dự phòng về thứ tự mức nghiêm trọng; số vẫn khớp dù bản cài đang kiểm có lỗi; chưa xác minh code hay lượt chạy nào tạo số công bố (T-016) | Trước khi gọi một phương pháp là "kiểm đúng đắn": soi đầu vào thật của từng thành phần (số cột, số dòng), đếm số lần rơi nhánh dự phòng bên trong, và so điểm với một bản bỏ thành phần đó (ví dụ chỉ SeverityScorer) |
```

- **Lý do:** cùng loại với SL24 nhưng ở mức thành phần bên trong phương pháp; T-006 có phép kiểm "nhánh dự phòng" của wrapper `@rca` nhưng không có của nhánh dự phòng riêng của TORAI.
- **Kết luận phụ thuộc:** cách viết SPEC kiểm đúng đắn của các task P1/P3 sau.

## L2 — rút lại (sửa theo tự soát N3, REVIEW T-016)

Không đề xuất dòng LESSONS thứ hai (nháp cũ "viện dẫn bài phải ghi mục"): nội dung đã nằm trong QT17 và SL17 (số và khẳng định phải có nguồn). Đính chính câu sai cụ thể nằm ở `dinh-chinh-task-cu.md` mục D2.

## K1 — `docs/knowledge/K1-phuong-phap-rca.md` mục C.8 (TORAI) và C.5 (RCD)

- **File đích:** `docs/knowledge/K1-phuong-phap-rca.md:224` (C.8, gạch "Graph/ranker") và `:198` (C.5, gạch "Graph/ranker").
- **Đoạn cũ (C.8):** "Trong cluster, Ψ-PC học causal DAG trên time-series nodes; CausalRanker xếp bằng conditional-independence score."
- **Đoạn mới (C.8):** "Trong cluster, bản cài RCAEval chạy lõi RCD (Ψ-PC **cục bộ**: chỉ học cạnh nối F-node, không học DAG đầy đủ) trên chuỗi metric và mẫu log, xếp theo p-value của phép kiểm với F-node; nếu RCD không xếp đủ service của cụm thì lùi về thứ tự mức nghiêm trọng (`torai.py:330-334`). Ở lệnh chính thức, bước này không nhận metric (lỗi giảm mẫu hai lần) và đa số cụm rơi nhánh lùi (T-016, `results/T-016/giam-mau-hai-lan.md`)."
- **Đoạn cũ (C.5):** "alpha empirical (`0.01` local start; code thử trong khoảng `0.001–0.1`)."
- **Đoạn mới (C.5):** "α bắt đầu 0,01 ở pha 1 và 0,001 ở pha 2, tăng 0,1 mỗi vòng tới < 1 cho tới khi đủ hàng xóm F (`rcd.py:23-25, 189, 302`); khoảng 0,001–0,1 là khoảng tác giả đã thử cho α khởi đầu (chú thích `rcd.py:296-301`)."
- **Lý do:** K1 tự ghi "chưa kiểm lại"; MRP §11 yêu cầu P1 kiểm lại khẳng định quan trọng trên code gốc. Hai câu trên sai hoặc thiếu so với code.
- **Kết luận phụ thuộc:** cách trình bày TORAI, RCD trong báo cáo cho cô (phần "đồ thị dùng ở đâu").

## D1 — `docs/DECISIONS.md`: ghi ủy quyền tự duyệt SPEC

- **File đích:** `docs/DECISIONS.md`, thêm dòng cuối bảng.
- **Đoạn mới:** `| Q-56 | 04/10 | Minh ủy quyền người làm T-016 tự viết SPEC rồi triển khai ngay, không dừng chờ duyệt; chỉ áp dụng cho task này (prompt Đợt 1 ngày 04/10/2026). Mọi luật khác của AGENTS giữ nguyên. | AGENTS mục 5 bước 2; tasks/T-016-ho-so-torai/LOG.md |`
- **Lý do:** AGENTS mục 4: quyết định của Minh trong chat phải vào DECISIONS. Nếu prompt Đợt 1 áp dụng chung cho nhiều task, Minh có thể muốn ghi một dòng chung thay vì dòng riêng.

## R1 — rút lại (sửa theo tự soát N3, REVIEW T-016)

Không cần sửa `data/README.md`: file đó mô tả thư mục `data/`, còn 30 ca TT nằm ở `D:\RCA-ext\work\T-016\data\`; nguồn, cách kiểm và lệnh dựng lại đã ghi ở `results/T-016/moi-truong.md` mục 4 (cùng cách T-006 ghi dữ liệu torai).

## Không đề xuất

- MRP, AGENTS, review-prompt: không cần sửa.
- STATE: chỉ dòng T-016 (đã ghi theo phạm vi).

# Phản biện T-005

- **Người phản biện:** Codex — **Ngày:** 03/10/2026 — **Commit/diff đã đọc:** commit gốc `38d3c1b`; `git status --short`, `git diff 38d3c1b`. Các file T-005 chưa được Git theo dõi, nên đã đọc trực tiếp toàn bộ thay vì coi diff rỗng là không có thay đổi.
- **Đã đọc:** `D:/RCA-flashticket/AGENTS.md`, `docs/STATE.md`, `docs/MRP.md`, `docs/WHY.md`, `docs/DECISIONS.md`, `docs/LESSONS.md`; SPEC và toàn bộ LOG T-005; mẫu REVIEW; toàn bộ 53 file trong `results/T-005/`, gồm log cài Python nén; T-001 mục 8–9; hai nguồn DT18 và hướng dẫn cô. Đã đối chiếu code tại `D:/RCA-ext/src/RCAEval`, `baro`, `GDN` theo revision trong manifest T-001; bài BARO và TORAI, cả HTML và PDF.

## Kết luận chung

Không thấy lỗi CHẶN làm sai số đo thời gian/RAM hoặc làm lệch nhiệm vụ nghiên cứu của T-005. Có hai điểm KHÔNG CHẶN: diễn giải tốc độ TORAI thiếu khác biệt quan trọng trong công việc được đo; tiêu chí không ghi ngoài phạm vi có ngoại lệ đã được LOG thừa nhận. Số đo chỉ chứng minh code được gọi đã chạy hết không lỗi; không chứng minh phương pháp đúng, và không thay việc kiểm đúng đắn mà Minh đã duyệt tách sang T-006/T-007.

## Các điểm

### R1. Diễn giải tốc độ TORAI thiếu việc giảm mẫu hai lần — KHÔNG CHẶN

- **Ở đâu:** [do-kha-thi.md](D:/RCA-flashticket/results/T-005/do-kha-thi.md:42), mục 2a, dòng TORAI. Bước chịu ảnh hưởng: bước 7, diễn giải kết quả bước 6 và lập kế hoạch P3.
- **Sai gì:** Câu “TORAI lấy metric mỗi 15 điểm một lần … nên nhanh hơn RCD” mô tả thiếu đầu vào thực tế của lõi RCD. Code giảm mẫu hai lần. Với biến thể `win`, phần metric bị loại khỏi đầu vào lõi sau tiền xử lý. Vì vậy chênh lệch thời gian chưa chứng minh tốc độ của lõi trên metric chỉ giảm 15 lần, hoặc riêng tác dụng của bước giảm mẫu.
- **Bằng chứng:** `D:/RCA-ext/src/RCAEval/RCAEval/e2e/torai.py:81` giảm mẫu 15 lần; dòng 295 lấy metric đã giảm cho cụm; dòng 312 gọi `_rcd_multimodal`; helper dòng 29 lại giảm 15 lần. Tính trực tiếp vị trí dòng từ hai phép cắt: `range(600)[::15][::15]` còn 0, 225, 450, tức hai điểm trước và một điểm sau mốc. Helper dòng 33–37 gọi `preprocess` riêng hai phía rồi lấy giao cột. `RCAEval/io/time_series.py:4–5,105` loại cột hằng; phía sau chỉ một dòng nên toàn bộ cột metric bị loại. Lõi vẫn nhận log. TORAI còn khác RCD ở gom cụm và nhánh dùng điểm nghiêm trọng khi lõi không trả đủ service (dòng 330–334). Hai log TORAI ghi 7,103 s và 15,081 s; các số này đúng.
- **Hậu quả:** Dùng lời giải thích hiện tại để dự trù thời gian cho bản TORAI đã sửa có thể đánh giá thiếu khối lượng xử lý. Đã xét câu giới hạn “chạy được = chạy hết không lỗi” và quyết định tách kiểm đúng đắn; chúng giữ giá trị của số đo nguyên trạng, nhưng không chứng minh nguyên nhân chênh lệch tốc độ.
- **Đề xuất sửa:** Thay câu quy nguyên nhân bằng mô tả thời gian của bản RCAEval nguyên trạng, ghi rõ nhánh lõi giảm mẫu metric hai lần và hệ quả trên `win`. Ghi chưa tách được nguyên nhân chênh lệch. Giữ nguyên số đo; xử lý thuật toán theo phạm vi kiểm đúng đắn đã duyệt.

### R2. Tiêu chí không ghi ngoài phạm vi còn ngoại lệ cache — KHÔNG CHẶN

- **Ở đâu:** [SPEC.md](D:/RCA-flashticket/tasks/T-005-do-kha-thi/SPEC.md), “Tiêu chí xong”, dòng cuối; [LOG.md](D:/RCA-flashticket/tasks/T-005-do-kha-thi/LOG.md:66), “Kết thúc phiên 1”, mục 2. Bước chịu ảnh hưởng: xác nhận hoàn tất SPEC.
- **Sai gì:** Không thể xác nhận tiêu chí tuyệt đối “Không có file nào ngoài Phạm vi ghi bị tạo hay sửa” từ hồ sơ hiện tại. LOG tự ghi có cache nằm ngoài các đường dẫn được liệt kê trong SPEC.
- **Bằng chứng:** LOG ghi “Tác dụng phụ ngoài phạm vi, do công cụ tự ghi: cache của pip … cache font của matplotlib trong thư mục người dùng”. SPEC cho ghi `results/T-005/`, `D:/RCA-ext/`, LOG, dòng STATE và cài Python 3.8.10 cho người dùng. Việc cài đã được duyệt; hồ sơ đã đọc chưa ghi Minh chấp nhận riêng ngoại lệ cache. Các sửa tài liệu và tạo T-006/T-007 về sau có duyệt bổ sung trong LOG, nên không gộp chúng vào điểm này.
- **Hậu quả:** Đây là lệch phạm vi ghi đã xảy ra theo LOG, không phải lỗi số đo hay bằng chứng mở dữ liệu khóa. Nó chỉ ngăn xác nhận rằng mọi tiêu chí xong đều được thỏa nguyên văn.
- **Đề xuất sửa:** Ghi rõ ngoại lệ này khi xác nhận hoàn tất, để Minh quyết chấp nhận các cache đã tạo. Giữ nguyên hiện trạng trong lúc phản hồi; không tự xóa cache.

## Điều đã kiểm và thấy đúng

- **Đầu ra và phép đo:** Đủ dòng cho danh sách đã chốt hoặc lý do không đo. 26 dòng JSONL khớp nguyên từng bản `TONG_KET` trong 26 log: 23 lượt xong, ba lượt dừng sau một giờ. Số thời gian/RAM trong bảng khớp sau làm tròn. GDN có đủ 30 epoch, 2876 cửa sổ học và 719 kiểm định. Ba script qua phân tích cú pháp bằng `ast.parse`, không tạo file.
- **Tính lại rẻ:** Ngoại suy BOCPD từ thời gian hàm đã lưu là 138,445 phút, phù hợp “≈140 phút”. `90 × (238 + 174 + 30) / 3600 = 11,05` giờ, phù hợp “≈11 giờ”. Hai phép ngoại suy được ghi “chưa kiểm”; không coi chúng là kết quả chạy 90 ca.
- **Đối chiếu bài:** Số CIRCA 7564,88 s, BOCPD 173,37 s, N-Sigma 0,53 s và chú thích CIRCA chỉ có 15/100 ca khớp PDF [BARO, Bảng 3, 5, 6](https://arxiv.org/pdf/2405.09330). Các số thời gian TORAI dùng trong LOG khớp [TORAI, Bảng 8](https://arxiv.org/pdf/2604.13522v1). Hồ sơ đã phân biệt dữ liệu BARO với RE2-TT; không dùng chênh lệch này để kết luận chất lượng phương pháp.
- **Code và môi trường:** HEAD ba repo khớp manifest; working tree ba repo sạch. Hồ sơ có lệnh cài, freeze, nguồn dữ liệu, kiểm hash và hai file vá. Các lượt cài hỏng cùng lượt sửa đều còn log. Đã kiểm sâu TORAI và GDN; kiểm thêm BARO/BOCPD, CIRCA-PC, RCD, MicroRank và TraceRCA. Không dựng lại môi trường hoặc chạy lại phương pháp.
- **Đường nhãn:** Script gọi RCA với `sli=None`, không truyền tên ca, service gốc hay loại lỗi. Tên service trong trace là thành phần quan sát, không phải nhãn nguyên nhân. Mốc trace được đổi sang micro giây. Mốc tiêm dùng cho chế độ biết trước, cửa sổ BOCPD đo thêm và đoạn học GDN đều được SPEC/LOG duyệt; không có đánh giá tự phát hiện từ cửa sổ này. `attack` của GDN đặt toàn 0, không vào loss, đồ thị học hay chọn checkpoint. Checkpoint chọn bằng validation loss (mất mát trên tập kiểm định).
- **Giới hạn tính đúng:** GDN vẫn chuẩn hóa điểm lỗi bằng toàn chuỗi đang chấm trong code gốc; MicroRank và CIRCA cũng có khác biệt thuật toán cần xử lý khi kiểm đúng đắn. T-005 không chấm thứ hạng hoặc tuyên bố tái lập độ chính xác. Chưa dùng số đo để xác nhận baseline đúng.
- **G1 và WHY:** Danh sách gọn là quyết định của Minh; ba ví dụ thuật toán của cô không bị coi là ba phương pháp bắt buộc. Họ học có đồ thị hiện có GDN ở phần phát hiện, chưa có đại diện RCA trong danh sách gọn. T-005 không chọn dataset, không chốt dev/test, không đưa ra kết luận RQ1/RQ3 hoặc lợi ích đồ thị. WHY-02/P6 giữ cơ chế cụ thể ở trạng thái ứng viên sau P4; WHY-10 chưa quyết GNN. Câu GDN “đạt tiêu chí 3” đã được bỏ.
- **Phạm vi kiểm:** Log giải nén T-005 ghi đúng năm file của một ca TORAI; script không truy cập `data/locked/`. Chỉ đối chiếu hồ sơ lịch sử, không mở zip hoặc dữ liệu khóa để kiểm lại. Máy không dành riêng và nhiễu khi đo đã được công khai; không chứng nhận đây là thời gian chuẩn hoặc ngân sách P3 đã đạt.
- **File của phiên phản biện:** Chỉ tạo `D:/RCA-flashticket/tasks/T-005-do-kha-thi/REVIEW.md`. Không đổi quyết định, LOG, STATE, code hoặc kết quả; không commit. R1 là đề xuất chỉnh diễn giải, R2 là ngoại lệ cần Minh quyết.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|

| R1 | Đúng; phạm vi khác một chút | Kiểm lại: `torai.py:81` giảm 15 lần, `_rcd_multimodal` (dòng 29) giảm thêm 15 lần; `range(600)[::15][::15]` = [0, 225, 450], tức 1 điểm sau mốc; `drop_constant` trên 1 dòng bỏ mọi cột (`io/time_series.py:5`). Vậy ở `win` lõi RCD trong TORAI không nhận metric. Hẹp hơn reviewer ngầm nêu: ở `full` còn 3 điểm sau mốc ([900, 1125, 1350]), nên metric không bị loại toàn bộ. Rộng hơn: đây cũng là vấn đề tính đúng của TORAI bản RCAEval với `--length 10`, cần chuyển cho T-006/T-007 biết, không chỉ là câu diễn giải tốc độ. Đề xuất sửa của reviewer hợp lý; không đổi số đo | Duyệt (04/10) |
| R2 | Đúng | LOG phiên 1 mục 2 tự ghi cache pip và cache font matplotlib nằm ngoài Phạm vi ghi, chưa có câu Minh chấp nhận. Thêm cùng loại mà reviewer không nêu: đăng ký Python 3.8 với `py` launcher (đi kèm việc cài đã duyệt, nên chấp nhận được). Không đề xuất xóa cache | Duyệt (04/10) |
| N1 | KHÔNG CHẶN | BOCPD: bảng 2b ghi "như `reproduce_bocpd`" nhưng chỉ giống cách cắt 300+300. `reproduce_bocpd` chọn cột `latency-50` và `_error` (`baro/reproducibility.py:140-144`); script đưa metric thô vào `bocpd()`, hàm tự chọn mọi cột chứa `latency` (cả -50 và -90) và `_error`: 76 cột, 60 không hằng (`runs/14-dem-bien.log`). Mục 4 nói chậm hơn bài 8 lần "chưa rõ lý do" mà bỏ sót nguyên nhân khả thi này (Q-33). Sửa: ghi rõ khác tập cột; thêm nguyên nhân khả thi, "chưa kiểm" | Duyệt (04/10) |
| N2 | KHÔNG CHẶN | Cửa sổ trace ±300 s theo `startTime` cho MicroRank/TraceRCA không đến từ RCAEval: `main.py` không có nhánh đọc trace. `do-kha-thi.md` mục 1 và docstring `chuan_bi_dau_vao.py` ghi như một phần của cấu hình RCAEval. Số đo không đổi; nguồn lựa chọn ghi sai, thiếu lý do. Sửa: ghi là lựa chọn của người làm, tương tự cửa sổ metric | Duyệt (04/10) |
| N3 | KHÔNG CHẶN | N-Sigma phát hiện 59 s so với 0,53 s của bài: bỏ sót nguyên nhân khả thi. `nsigma` (repo BARO) là vòng lặp tính lại mean/std trên toàn quá khứ mỗi bước, O(n²) mỗi cột; script chạy trên mọi cột thô (375). Sửa: thêm vào mục 4 như nguyên nhân khả thi, "chưa kiểm" | Duyệt (04/10) |
| N4 | KHÔNG CHẶN | Dao động RCD (69 và 99 s) chỉ quy cho "không đặt seed". Lượt lan2 có import 14,0 s so với 4,4 s ở lan1 (`ket-qua-do.jsonl`), tức máy bận hơn lúc lan2. Sửa: thêm nguyên nhân tải máy | Duyệt (04/10) |
| N5 | KHÔNG CHẶN | Ước lượng 90 ca (mục 4) dùng thời gian `full`, trong khi `main.py` chạy theo cửa sổ. Đã ghi "chưa kiểm" nhưng không nói đây là cận trên với ca lớn nhất. Sửa: thêm một câu | Duyệt (04/10) |

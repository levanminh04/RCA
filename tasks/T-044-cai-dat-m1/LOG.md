# Nhật ký T-044

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Phiên 1 — 29/10/2026 — Claude — cloud (container Linux Ubuntu 24.04, repo `/home/user/RCA`, branch `claude/sweet-hawking-dy078d`) — vai trò: người làm

- Minh duyệt SPEC ngày 29/10/2026 (Q-212).

**Mở phiên:** đã đọc AGENTS, STATE, SPEC T-044. Đây là mục LOG đầu tiên. Chưa có `results/T-044/`, `src/m1/`, `src/m1_danh_gia/`.

**Công đoạn và mục tiêu nguồn:**
- Giai đoạn 1 theo lời Minh trong chat phiên này: tự rà SPEC độc lập trước khi viết code. Có điểm CHẶN hoặc đề xuất làm khác SPEC thì dừng, commit LOG, trình Minh trong chat.
- Mục tiêu nguồn: DT18-NV2; bước 2, 4 của cô; MRP P6 tầng 1–4 và đoạn P7 "Trước G3, phương pháp và các đối chứng đã khai báo phải được cài và kiểm đầu vào, trung gian, hành vi trên dev"; Q-209 mục 9.
- Môi trường theo lời Minh: dùng `$HOME/m1env/bin/python` thay `py -3` và thay đường dẫn `D:/RCA-ext`; không có `data/`, không tải dữ liệu; không cần Codex trong phiên này.

**Diễn biến** (theo thứ tự đã làm; không ghi giờ vì không đo):
- Kiểm hash T-043: `$HOME/m1env/bin/python -B results/T-043/scripts/tao_manifest.py --kiem` → `{"so_file_manifest": 69, "so_file_that": 69, "thieu": [], "thua": [], "lech": [], "dong_bang_phien7_khop": "10/10", "luot_thieu": ["runs/khe-open-001"], "PASS": false}`, mã thoát 1. Xem R1.
  - Lần theo: `runs/khe-open-001` là lượt hỏng, để lại một thư mục rỗng (LOG T-043 dòng 5658). Git chỉ lưu `results/T-043/runs/khe-open-001.stdout.txt` (`git ls-files results/T-043/runs`). Manifest không ghi file nào trong thư mục đó.
  - Chạy cùng lệnh trên bản sao `results/T-043` ở scratchpad (`/tmp/claude-0/-home-user-RCA/d9b3137b-19ef-51a4-bac8-e0bccb1b549f/scratchpad/manifest-check`), có thêm đúng thư mục rỗng đó: PASS, 69/69 file, đóng băng 10/10, không thiếu lượt. Không ghi gì vào `results/T-043/`.
- Đếm fixture: `fixture-dac-ta.json` có 82 mục; `fixture/fixture-bo-sung.json` có 8 mục (B1–B8). `fixture/ket-qua-kiem.json#/so_phep_kiem` = 109; 12 phép thuộc D13 (59, 61–67), còn 97 phép trong phạm vi T-044.
- Môi trường `m1env` (venv trên `/usr/bin/python3.12`, Python 3.12.3): numpy 1.26.4, pandas 2.2.3, scipy 1.14.1, networkx 2.5, pytest 8.3.4, drain3 0.9.11 (kèm cachetools 4.2.1, jsonpickle 1.5.1) khớp SPEC. **pyarrow chưa cài**; `pip index versions pyarrow` có 18.1.0. Gói gián tiếp lệch `py312-pin` (`results/T-006/runs/freeze-py312-pin.txt`), dạng cloud/pin: python-dateutil 3.0.0/2.8.2, pytz 2026.6/2023.3, tzdata 2026.6/2023.3, packaging 26.3/23.1, pluggy 1.7.0/1.5.0, iniconfig 2.3.1/2.0.0, six 1.17.0/1.16.0, decorator 5.3.1/5.1.1. networkx 2.5: `all_simple_paths(G, R, R)` trả rỗng, giống 2.8.8 mà fixture 18 dẫn. drain3 0.9.11: `TemplateMiner.match` đòi khớp hoàn toàn (docstring "Match shall be perfect (sim_th=1.0)"); có `Drain.tree_search(root_node, tokens, sim_th, include_params)`.
- Đọc nguồn: SPEC T-043 (Phụ lục B, C, D và tiêu chí xong); `dac-ta-phuong-phap-v1.md`; `hop-dong.json`; `ma-tran-thu.json`; `dinh-nghia-pha2.json`; `fixture-dac-ta.json`; `fixture/fixture-bo-sung.json`; `fixture/ket-qua-kiem.json` (danh sách 109 phép); `dinh-chinh-phien8.md`, `dinh-chinh-phien9.md`, `dinh-chinh-phien10.md`; `bao-cao.md`; MRP §2, P6, P7; WHY-06, WHY-15, WHY-55–65; DECISIONS Q-199–Q-212; LESSONS; DT18; thư cô (`advisor-2026-09-23.md`, `advisor-thu-dang-ky-de-tai.md`); SPEC T-045; code chỉ đọc `src/p3/` (ban_ghi, cua_so, danh_gia, nezha, selector, nhan, runner, worker, adapters/nezha), `src/simplerca/core.py`, `src/do_thi/builder.py`; `results/T-028/codebook.md` §4–5 (M5); `results/T-034/goi-g2.md` UV-6.
- Phép đếm chỉ đọc, không nhãn, trên `results/T-043/ks16/dem-khong-nhan.json#/cases/*/call_rows` (cạnh gọi có n_N + n_A > 0), tìm thành phần liên thông mạnh bằng Tarjan trong bộ nhớ:
  - RE2-TT: 24/30 ca có SCC 3 nút {ts-seat-service, ts-travel-service, ts-travel2-service}, với cạnh seat→travel, travel→seat, seat→travel2, travel2→seat; travel và travel2 không kề nhau. 6/30 ca không có cạnh nào giữa ba nút.
  - Nezha-OB: 0/22 ca có vòng.
  - Hậu tố cột metric RE2-TT (`#/cases/*/metric_rows`) đều thuộc 8 hậu tố ở `hop-dong.json#/kenh/RE2-TT`; 21 tên kênh Nezha-OB đều có trong `#/kenh/Nezha-OB`.

## Tự rà SPEC

Mỗi điểm ghi: mức; chỗ; vấn đề; bằng chứng; hậu quả; đề xuất tối thiểu. "Chặn" nói rõ chặn phần nào.

### A. Điểm CHẶN

**R1 — Lệnh kiểm hash T-043 không thể PASS trên một bản clone git. CHẶN tiêu chí 1 (theo câu chữ) và yêu cầu "phải PASS" của Minh.**
- Ở đâu: SPEC T-044 dòng 44, 86, 118.
- Vấn đề: thư mục rỗng của lượt hỏng `results/T-043/runs/khe-open-001` không có trong clone, vì git không lưu thư mục rỗng. `tao_manifest.py --kiem` kiểm cả việc mỗi lượt còn tồn tại, nên báo `luot_thieu`.
- Bằng chứng: kết quả lệnh ở mục Diễn biến; LOG T-043 dòng 5658 ("để lại thư mục rỗng và `runs/khe-open-001.stdout.txt` rỗng"); bản sao có thêm thư mục rỗng cho PASS. 69/69 file khớp hash; 10/10 hash đóng băng khớp.
- Hậu quả: nội dung nguồn T-043 đã được xác nhận bằng hash. Chỉ điều kiện "PASS" là không đạt được trên mọi bản clone, kể cả khi T-045 chạy trên một clone mới.
- Đề xuất tối thiểu: Minh chấp nhận bằng chứng thay thế cho tiêu chí 1: chạy `--kiem` trên bản sao `results/T-043` ngoài repo, có thêm thư mục rỗng đó; ghi cả hai kết quả vào LOG; sửa SPEC T-044 dòng 118 cho đúng. Phương án khác: tạo thư mục rỗng tại chỗ trước khi kiểm. Git không ghi nhận thư mục này, nhưng đó vẫn là ghi vào `results/T-043/`, vùng SPEC cấm ghi, nên cần Minh duyệt.

**R2 — E1-CP: tiêu chí 2 đòi phần CP của fixture 2, 3 phải qua, còn mục "Không làm" bỏ E1-CP. CHẶN tiêu chí 2.**
- Ở đâu: SPEC T-044 dòng 119 (chỉ trừ D13), dòng 131 (bỏ E1-CP), dòng 96 (khối 6 "E1-U (2–5)"); `fixture-dac-ta.json` dòng 57–58 (đáp án `"CP": 60` và `"CP": 0`); `fixture/ket-qua-kiem.json`, phép "2" và "3" kiểm "U, CP".
- Hậu quả: theo câu chữ, task không thể "xong" dù mọi phần khác đúng; hoặc người làm phải tự bỏ hai phép kiểm.
- Đề xuất tối thiểu, khuyến nghị (a):
  - (a) cài một hàm thuần tính khoảng E1-CP theo SPEC T-043 dòng 613 (đường găng CRISP, happensBefore với 1 ms), kiểm bằng fixture 2, 3; không nối vào cấu hình hay runner nào. Chi phí nhỏ, đúng Q-209 mục 9, dùng lại được ở chặng 2;
  - (b) tiêu chí 2 trừ thêm phần CP của fixture 2, 3.

**R3 — Điều kiện UV-6 của E3 chưa thành phép tính xác định, và không có đáp án. CHẶN luật C bước 1 cho E3 trong khối K (T-045).**
- Ở đâu: SPEC T-043 dòng 870 (luật C bước 1 "vi phạm UV-6 (với E3)") và dòng 781; `ma-tran-thu.json` dòng 49; đặc tả v1 dòng 244; nguồn `results/T-034/goi-g2.md` dòng 753 ("Bác bỏ nếu số ca đang đúng bị hỏng nhiều hơn số ca return được sửa").
- Vấn đề: chưa nói "đang đúng" là gì (root chắc chắn ở hạng 1, Hit@1 kỳ vọng, hay RR = 1); khi root hòa ở đầu thì tính sao; "được sửa" là lên hạng bất kỳ (UV-6 viết "root lên hạng") hay thành đúng; đếm trên những ca nào; áp trong từng thế giới thế nào. LOG T-043 dòng 4580, 4814 dùng "ca đúng" theo Hit@1, nhưng không nói cách xử lý hòa.
- Hậu quả: E3 có 4 ô nên là thành phần ít ca. Luật C dừng ở bước đầu tiên khớp. Vi phạm UV-6 thì E3 HẠI và cấu hình chứa E3 bị loại ở lượt một của luật khối. Không vi phạm thì tới bước 4, KHÔNG ĐỦ CA, và E3 được giữ bật (D2a). Hai cách đọc hợp lý có thể cho hai quyết định ngược nhau.
- Đề xuất tối thiểu: Minh chọn một định nghĩa; người làm ghi vào `results/T-044/dinh-chinh-cai-dat.md`, kèm đáp án fixture (ca hòa, ca hỏng, ca được sửa). Khuyến nghị:
  - "ca đang đúng": hit@1 = 1 ở cấu hình bỏ E3, tức root một mình ở hạng 1;
  - "bị hỏng": ca đang đúng mà hit@1 < 1 ở cấu hình có E3;
  - "được sửa": ca có loại lỗi return hoặc exception, hit@1 < 1 khi bỏ E3 và = 1 khi có E3;
  - đếm trên 52 ca; áp riêng trong từng thế giới.
  - Phương án khác: (b) cộng phần chênh của hit@1 kỳ vọng; (c) theo RR, mọi lần lên hạng là "sửa".

**R4 — Luật nhóm vòng (SCC) của E5 có nhiều cách đọc, và dev có vòng thật. CHẶN kết quả E5 ở RE2-TT (8/16 cấu hình khối K có E5).**
- Ở đâu: SPEC T-043 dòng 669–671; đặc tả v1 dòng 306–308; fixture 8.
- Vấn đề: câu "Trong một SCC, chỉ được giải thích bởi thành viên có bất thường không lan, hoặc bởi bên được gọi ngoài SCC" chưa nói hai điều:
  - (i) thành viên giải thích có phải kề cạnh theo hướng của lớp kênh không;
  - (ii) kênh lan xuôi của một thành viên SCC có được bên gọi ngoài SCC giải thích không. Đọc chữ "chỉ" theo nghĩa đen thì không.
- Bằng chứng: SCC 3 nút ở 24/30 ca RE2-TT (mục Diễn biến); travel và travel2 không kề nhau. Fixture 8 chỉ có vòng 2 nút và kênh lan ngược, nên không phân xử được (i), (ii). Luật chỉ áp khi ít nhất hai nút của vòng có cờ F_raw (D19). Số ca như vậy chưa biết, vì M1 chưa chạy.
- Đề xuất tối thiểu: Minh chọn; người làm ghi vào `dinh-chinh-cai-dat.md`, kèm fixture vòng 3 nút. Khuyến nghị: đọc câu này là một hạn chế đặt lên luật chung, giữ kề cạnh. Với e thuộc SCC S:
  - kênh lan ngược của e được bên được gọi b giải thích theo luật chung nếu b ∉ S; nếu b ∈ S thì chỉ khi b có kênh F_raw lớp không lan;
  - kênh lan xuôi của e được bên gọi a giải thích theo luật chung nếu a ∉ S; nếu a ∈ S thì chỉ khi a có kênh F_raw lớp không lan.

**R5 — Đường xử lý log của E3 (Drain) thiếu bốn quy định; mỗi quy định đổi tập kênh. CHẶN các kênh khi E3 bật (8/16 cấu hình khối K).**
- Ở đâu: SPEC T-043 dòng 636–637; đặc tả v1 dòng 150, 227–228; Đ15.
- Vấn đề và bằng chứng:
  1. Chuỗi đưa vào Drain ở Nezha-OB chưa định. Cột `Log` là JSON ngoài; khóa `log` là một chuỗi JSON (`hop-dong.json` dòng 69). Adapter P3 truyền nguyên chuỗi `Log` (`src/p3/adapters/nezha.py` dòng 94). Converter Nezha chỉ lấy chuỗi `log` (`results/T-042/runs/continuation-001/bao-cao-bo-sung.md` dòng 26). Cũng có thể dùng thông điệp đã giải mã. Ba cách cho mẫu khác nhau.
  2. Cách khớp dòng A với mẫu học từ N chưa định. `TemplateMiner.match` của drain3 0.9.11 đòi khớp hoàn toàn. Khớp theo ngưỡng giống 0,4 mà không học là cách khác. Cách thứ nhất đưa nhiều dòng A vào ô "mẫu mới" hơn.
  3. Biểu thức che token chưa định: "chuỗi trong ngoặc" gồm loại ngoặc nào; hex ≥ 8 có cần chữ số không; IP có kèm cổng không; che theo thứ tự nào.
  4. Kết quả Drain phụ thuộc thứ tự dòng khi học. Phép xáo hàng (A4) cần một thứ tự chuẩn.
- Hậu quả: E3 ít ca; luật C và UV-6 quyết E3 trên đúng các kênh này. Không có quy định, người cài phải tự chọn bốn điểm mà không có căn cứ đã duyệt.
- Đề xuất tối thiểu: Minh chọn; người làm ghi vào `dinh-chinh-cai-dat.md`, kèm fixture nhỏ cho che token và khớp mẫu. Khuyến nghị:
  - (1) Nezha-OB dùng chuỗi `log` của JSON ngoài; giải mã không được thì dùng nguyên chuỗi. RE2-TT dùng cột `message`;
  - (2) khớp theo ngưỡng giống 0,4 của chính Drain (`Drain.tree_search`), không cập nhật mẫu, để giữ nghĩa "học trên N rồi áp cho A"; không khớp thì vào "mẫu mới". Phương án khác: `match` khớp hoàn toàn;
  - (3) che theo thứ tự UUID → IPv4 (cổng tùy chọn) → chuỗi hex dài ≥ 8 có ít nhất một chữ số → số → nội dung trong (), [], {}; tắt phần che sẵn của drain3;
  - (4) học theo thứ tự (mốc ns, thực thể, nội dung).

**R6 — Hợp đồng chưa có đường đưa quy tắc riêng của dataset vào phương pháp. CHẶN runner và adapter (đầu ra 1, mục runner; tiêu chí 7; bước 1 của T-045).**
- Ở đâu: `hop-dong.json` dòng 6, 13 (API 7 tham số; khóa của `params`); dòng 54–66 (ánh xạ kênh metric → lớp theo dataset); dòng 68–70 (severity cho Nezha-OB, từ khóa cho RE2-TT); SPEC T-043 dòng 711 và đặc tả v1 dòng 379 ("Nezha-OB chỉ dùng trace" cho E9); Đ19 (các khóa đã thêm).
- Vấn đề: phương pháp phải biết bảng lớp kênh, quy tắc dòng lỗi và các nguồn dùng cho khởi phát của dataset đang chạy. `params` không có khóa nào cho các quy tắc này, cũng không có tên dataset. Suy từ dữ liệu (ví dụ có cột severity hay không) là đoán, và dễ sai trên FlashTicket.
- Đề xuất tối thiểu: ghi một đính chính hợp đồng giống cách Đ19 làm (không sửa `hop-dong.json`), Minh duyệt. Nội dung: `params.ho_so_nguon` = {`kenh_metric`: bảng hậu tố hoặc tên kênh → lớp; `quy_tac_log`: {kiểu "severity", danh sách lỗi, danh sách không lỗi} hoặc {kiểu "từ khóa", danh sách từ khóa}; `nguon_khoi_phat`: danh sách nguồn}. Runner điền từ `hop-dong.json#/kenh/<dataset>`, `#/severity/<dataset>` và đặc tả v1 §7.11. Thiếu khóa thì bản ghi ERROR; không đặt mặc định.

**R7 — Nhiều phần dùng ở T-045 không có đáp án, mà SPEC chỉ cho người làm tự lập đáp án cho đối chứng. CHẶN căn cứ "code đúng" của các phần (i)–(iii).**
- Ở đâu: SPEC T-044 dòng 89 (N1 chỉ nêu C-a1, C-d2, C-c, C-d1) và dòng 119.
- Phần chưa có fixture đáp án:
  - (i) đếm cờ M5 từ thứ hạng, G_N và root (điều kiện riêng của E5). Fixture 52, 53 nhận số ca M5 làm đầu vào. Thêm một chỗ mơ hồ nhỏ: G_N theo `results/T-028/codebook.md` §4 đòi cả span cha lẫn span con trong N; `dinh-nghia-pha2.json#/do_thi_quan_sat` chia theo end của span cha. Hai cách chỉ khác ở span con kết thúc sau t khi span cha kết thúc trước t;
  - (ii) xử lý "phụ thuộc quan sát" trong luật C và luật chọn khối (SPEC T-043 dòng 896–898);
  - (iii) bước 8 luật chọn khối: khi nào kết cục đảo trạng thái "mâu thuẫn với lựa chọn" (SPEC T-043 dòng 807);
  - (iv) dựng vùng E7 theo hai cách. Fixture 70 nhận R_r làm đầu vào; fixture 31, 42 chỉ có vùng rỗng;
  - (v) khởi phát E9 và phép tắt E9 trên cạnh có E2 bất thường. B2–B5 nhận khởi phát làm đầu vào;
  - (vi) T4c (xem R9).
- Hậu quả: (i)–(iii) là đầu vào trực tiếp của quyết định khối K ở T-045. Thiếu đáp án thì test có thể qua dù code sai (câu A2 của SPEC). (iv)–(vi) dùng ở task (2) và ở T4.
- Đề xuất tối thiểu: mở rộng N1 của Q-212 cho (i)–(vi). Người làm lập ca giả có đáp án tính tay ở `results/T-044/fixture/dap-an-thanh-phan.json`, đánh dấu "đáp án của người làm T-044, chưa qua phản biện"; Codex kiểm khi phản biện. Sửa SPEC T-044 dòng 89 tương ứng. Với (i), dùng G_N theo codebook (cả hai span trong N), vì Phụ lục C dẫn đúng `codebook.md:95`.

### B. Điểm KHÔNG CHẶN cần Minh biết hoặc chọn

**R8 — Adapter dữ liệu dev và nguồn của mốc t. KHÔNG CHẶN T-044; ảnh hưởng T-045.**
- SPEC không ghi ai viết phần đọc dữ liệu dev rồi đổi sang API M1. Phần này gồm: đọc RE2-TT qua `src/p3/selector.py`, `cua_so.py`; đọc Nezha-OB qua `src/p3/nezha.py`; dựng `params.coverage` theo luật F (a) (Đ9) từ mốc đầu và cuối của từng file; lấy `thoi_gian_nguon`, `nguon_metric`, `phan_hoach_NA_da_kiem` từ `provenance`; khai `don_vi_thoi_gian`; dựng `canh_tinh` từ T-038, T-039; lấy `severity_raw` theo đường đọc ở `hop-dong.json` dòng 69. T-045 chỉ được sửa `src/m1` theo đính chính đã duyệt, nên phần này phải nằm trong T-044.
- Mốc t của RE2-TT chỉ có trong file nhãn `results/T-022/nhan-dev.json`. KS-16 pha 1 đọc nó qua `p3.nhan.nap_moc` (`ks16/ks16_pha1_v11.py` dòng 735). Tiêu chí 4 cấm module trong `src/m1` đọc đường dẫn nhãn.
- Cách xử lý trong phạm vi:
  - viết adapter trong `src/m1`; chỉ kiểm được trên khung dữ liệu tổng hợp theo schema của `src/p3`, vì cloud không có dữ liệu thật;
  - runner nhận bảng mốc {mã mờ: t} làm đầu vào, không tự đọc file nhãn. T-045 tạo bảng mốc bằng `p3.nhan.nap_moc` trong `results/T-045/`, đúng tiền lệ KS-16;
  - T-045 bước 1 là nơi kiểm adapter trên dữ liệu thật.

**R9 — Bốn định nghĩa còn mơ hồ ở các phần dùng sau khối K. KHÔNG CHẶN: T4 chỉ báo cáo; E7, E9 thuộc task (2); C-d1 chỉ báo cáo.** Đề xuất ghi vào `dinh-chinh-cai-dat.md` theo cách đọc dưới đây, kèm đáp án tự lập (R7), để Minh duyệt.
- **T4c** (SPEC T-043 dòng 409; `ma-tran-thu.json` dòng 34 ghi T4 có 9 cấu hình, gồm cả T4c): chưa nói m đặt ở đâu trong khóa, gộp theo thực thể thế nào, r_u lấy trên tập nào, và T4c có phải cấu hình thứ 10 không. Cách đọc đề xuất:
  - với mỗi đơn vị phân vị có cờ: m = log(1 + |trung vị A − trung vị N| / max(|trung vị N|, r_u)), với r_u là hiệu dương nhỏ nhất giữa hai giá trị khác nhau trong N ∪ A của đơn vị; đơn vị đếm có m = 0;
  - khóa thực thể thêm phần tử thứ tư: max m trên các kênh có cờ của khóa đó;
  - T4c là phép xếp lại trên lượt R0 gốc, không chấm lại, nên T4 vẫn là 9 cấu hình.
- **E7** (SPEC T-043 dòng 690): chưa rõ "bên gọi … mọi kênh bị coi là kế thừa" và "bên được gọi lan xuôi từ r*". Cách đọc đề xuất: trên đồ thị con F_raw, R_r = {r} ∪ {a có đường a → … → r và mọi kênh F_raw của a có F_I = 0 ở cấu hình đang chạy} ∪ {b có đường r → … → b và có ít nhất một kênh F_raw lớp lan xuôi}. Khi E5 tắt, phần bên gọi rỗng; báo cáo ghi rõ điều này.
- **E9** (đặc tả v1 dòng 375; Đ11; SPEC T-043 dòng 711). Cách đọc đề xuất:
  - ô 10 giây đặt từ t; mẫu vào ô theo end của span, hoặc theo mốc của nguồn metric; ô không có mẫu thì bỏ qua; khởi phát chỉ tính theo hướng có cờ;
  - "tắt trên cạnh có E2 bất thường": cạnh dùng để giải thích có đơn vị E2 với F_raw,lên = 1 thì không phủ quyết. Khi E2 tắt không có đơn vị cạnh, nên điều kiện này không xảy ra.
- **C-d1** (SPEC T-043 dòng 719): "ưu tiên nút không có bên được gọi bất thường". Cách đọc đề xuất:
  - nhóm 1: thực thể có K_raw,₁ > 0 mà không có bên được gọi nào có K_raw,₁ > 0 (cạnh N ∪ A, cộng cạnh tĩnh khi T12 bật), xếp theo K_raw;
  - nhóm 2: các thực thể có cờ còn lại, xếp theo K_raw; nhóm 3: tầng 3;
  - C-d1, C-d3 tính lại trên kết quả chấm của từng cấu hình, không phải cấu hình riêng.

**R10 — Tiêu chí 7 "đếm cấu hình khớp `ngan_sach`" chỉ kiểm được một phần. KHÔNG CHẶN.**
- `ma-tran-thu.json` dòng 50 có mục "khoảng 9 × 52". K-b, T6–T12, KB, T13 phụ thuộc cấu hình thắng của K hoặc chuỗi cuối, nên chưa có trước T-045.
- Cách xử lý: runner sinh danh sách theo tham số (cấu hình thắng, chuỗi cuối). Kiểm số đúng ở phần đã xác định, dùng một cấu hình thắng giả: T1 1 cấu hình × 3 hash seed, cộng 30 mốc giả; T4 9; T4b 1; K 16; K-b 2; T6, T9, T11, T12 mỗi bước 1; KB 4; T13 bằng số thành phần đang bật cộng 7 (sau Đ16). Báo cáo ghi rõ phần "khoảng" không có số chính xác để so.

**R11 — Lỗ rò nhãn ở mức giá trị. KHÔNG CHẶN; thêm phép chặn trong phạm vi.**
- Bộ kiểm trường cấm chỉ xét tên khóa (`hop-dong.json` dòng 18). Runner cầm mã mờ và `case_dir`. `case_dir` chứa tên root và loại lỗi, ví dụ `data/rcaeval/re2tt_ts-route-service_socket_3` trong `results/T-022/allowlist-dev.json`.
- Cách xử lý: trước khi gọi phương pháp, runner kiểm rằng không chuỗi mã mờ hay `case_dir` nào nằm trong `params`, `aliases`, `inventory`. Có test và một đột biến tương ứng.

**R12 — Giao diện bộ đánh giá phải đủ cho T-045. KHÔNG CHẶN; làm trong phạm vi.**
- Phép độ bền của T-045 (bước 7) chạy lại luật C và luật chọn khối trên mẫu ô có lặp, với δ_d theo n_d gốc. Đ5 (Q-209 mục 2) cần n_N, n_A, T của từng đơn vị đếm. SPEC T-044 không nêu hai nhu cầu này. T-045 chỉ được sửa `src/m1_danh_gia` theo đính chính.
- Cách xử lý: bộ đánh giá nhận trọng số ca và δ_d cố định làm tham số. Bản ghi lưu chi tiết từng đơn vị (nhãn, p, e, n, T) theo thế giới. Test: gán trọng số 2 cho một ô phải cho cùng kết quả như nhân bản các ca của ô đó.

**R13 — Một số đáp án đặc tả nằm trong văn bản; fixture 1 chỉ kiểm từ mức kênh. KHÔNG CHẶN; đề xuất thêm test trong phạm vi, không đổi đáp án.**
- Q-209 mục 9 nói "mọi đáp án đặc tả". Các ví dụ có đáp án nhưng chưa thành fixture:
  - Đ10 (`dinh-chinh-phien9.md` dòng 73–76): hai ví dụ E6b đổi hạng root qua cạnh không chạm root;
  - đặc tả v1 dòng 349: π(R) ≈ 0,833;
  - SPEC T-043 dòng 392: 100 → 200 sự kiện cho e_up = 0,5, p ≈ 4,0 × 10⁻⁹;
  - Đ17 (`dinh-chinh-phien10.md` dòng 81): cần tự chọn dataset của từng ca và |E_X|, nên phần đầu vào này đánh dấu là người làm bổ sung.
- Fixture 1 (S1–S7) kiểm từ kênh trở đi; phép tính span → kênh của cả chuỗi chưa được kiểm (`fixture-dac-ta.json#/nguyen_tac/5`). Đề xuất dựng trace tổng hợp theo `#/trace_mau_S` cho S1, S2, S2b, S5 (mô tả đã đủ số), chạy cả chuỗi từ span, rồi so với đúng đáp án của fixture 1. S3, S6, S7 cần tự chọn thêm số (số dòng log, thao tác mới), nên chỉ làm nếu Minh đồng ý.
- Nơi ghi: `results/T-044/fixture/dap-an-van-ban.json` (kèm dòng nguồn) và `results/T-044/tests/`.

**R14 — Môi trường. KHÔNG CHẶN.**
- pyarrow chưa cài; SPEC T-044 dòng 52 đòi ghim một phiên bản. Bước 1 cài pyarrow 18.1.0, bản T-043 đã dùng (`results/T-043/manifest.json#/runtime/parquet`) và có trên PyPI qua proxy. T-044 không đọc parquet.
- Các gói gián tiếp lệch `py312-pin` (mục Diễn biến); M1 không dùng trực tiếp chúng. Giữ `requirements-m1.txt` đúng danh sách SPEC; ghi thêm `results/T-044/freeze-m1.txt` (pip freeze đủ) để T-045 dựng lại bằng `pip install -c`.

### C. Tự diễn giải sẽ áp dụng trong phạm vi (ghi trước khi viết test)

- **Sai số so đáp án** (SPEC T-044 dòng 89: "theo fixture"):
  - đáp án dạng phân số hoặc số hữu tỉ: sai số ≤ 1e−12;
  - số thập phân đã làm tròn trong fixture (0,588; 9,65 × 10⁻¹³; 5,27 × 10⁻¹⁰⁰; 0,0005934196726…): lệch không quá nửa đơn vị của chữ số cuối đã ghi;
  - thứ hạng, trạng thái, tập: khớp tuyệt đối; `p_toi_da`: so ≤.
- **Biên của luật C** (δ; δ_d = 1/n_d; fixture 38 ghi "không lớn hơn hẳn 1/30"): tính RR, MRR, ΔMRR bằng phân số chính xác từ `danh_gia.phan_bo_hang`, để so đúng tại biên. Ví dụ: một ca RE2-TT đi từ RR 0 lên 1 cho ΔMRR_d đúng bằng 1/30.
- **Tất định:** Σs tính bằng `math.fsum`; mọi tập, đồ thị và thứ tự nút sắp theo tên; dòng log vào Drain theo thứ tự chuẩn (R5); hash pha 1 tính trên JSON đã chuẩn hóa (khóa sắp, không có trường thời gian hay run_id).
- **Bản ghi:** dựng cùng schema với `ban_ghi.tao` để `danh_gia` đọc được, nhưng không gọi `ban_ghi.tao` hay `ban_ghi.kiem` (SPEC T-044 dòng 46 chỉ cho lấy `CAM`). Không dùng tên khóa cấm trong bản ghi, ví dụ không đặt khóa `nhan`, `root`, `cell`.
- **Khi E3 bật**, kênh mẫu Drain thay kênh log lỗi cơ bản. Căn cứ: `hop-dong.json` dòng 51 (`log_loi_co_ban`, "khi": "E3 tắt") và đặc tả v1 dòng 139. Câu "E3 bật bổ sung" ở SPEC T-043 dòng 648 hiểu là bổ sung so với nhánh tắt, không cộng thêm kênh cơ bản.
- **`params.coverage`:** `khoang` = [mốc bản ghi đầu, mốc bản ghi cuối] của từng file; M1 cộng r_ns (khớp B1, B8). Danh sách rỗng nghĩa là không có file, tức XÁC NHẬN THIẾU THU. Thiếu khóa thì UNSUPPORTED (Đ19 điểm 4).
- **Phân bổ fixture vào khối:** B1, B8 vào khối 2 (quan sát); B2–B5 vào khối 8 (E9); B6, B7 vào khối 10 (C-d2, C-d3). SPEC T-044 dòng 94 ghi "B1–B8 phần liên quan" ở khối 4; bảng ánh xạ sẽ nằm trong báo cáo.

### D. Đề xuất ngoài phạm vi T-044 (cho T-045; Minh quyết; không làm trong task này)

- **D1.** Ở T-045 bước 1, đối chiếu số trung gian của M1 với số không nhãn của KS-16 từng ca (`results/T-043/ks16/dem-khong-nhan.json#/cases/*`): span sau bỏ lặp, span mồ côi, span gốc, span bọc, số đơn vị đủ hỗ trợ, F, H, T. Phép này rẻ, không cần nhãn, và kiểm thẳng adapter trên dữ liệu thật.
- **D2.** Ở T-045 pha 2, trước khối K: dùng `src/m1_danh_gia` tính lại MRR và số ca có cờ M5 của sáu baseline từ bản ghi P3, rồi so với `results/T-043/ks16/dem-sau-ghep-nhan.json#/hinh_dang_xep_hang_baseline` và `results/T-034/bang-baseline.json`. Đây là phép tái lập số đã có cho bộ đánh giá (AGENTS mục 5, bước 4).

## Kết luận giai đoạn 1

- Có 7 điểm CHẶN (R1–R7) và các đề xuất làm khác SPEC: sửa tiêu chí 1, mục "Không làm", bước 3; đính chính hợp đồng (R6); các định nghĩa ở R3–R5 và R9.
- Theo lời Minh: **DỪNG**. Chưa viết code, chưa tạo `results/T-044/`, chưa cài pyarrow. Trình Minh toàn bộ các điểm trong chat, gom một lượt.
- Khi Minh duyệt, phần làm được ngay mà không phụ thuộc R3–R7: bước 1 (môi trường), bước 2 (chép đáp án U, H), khung test, các khối 1–4, 6, 9 ở phần không dùng Drain hay SCC.

**Quyết định của Minh trong phiên:** chưa có (chờ trả lời các điểm trên).

**Kết thúc lượt (AGENTS mục 7):**
1. Đã làm gì: kiểm hash T-043, môi trường, đếm fixture; đọc nguồn; tự rà SPEC; ghi LOG này; cập nhật dòng T-044 trong STATE.
2. File đã thay đổi: `tasks/T-044-cai-dat-m1/LOG.md` (mới); `docs/STATE.md` (dòng T-044). Ngoài repo: bản sao `results/T-043` trong scratchpad để kiểm hash.
3. Kiểm đã chạy và kết quả: như mục Diễn biến.
4. Điều chưa chắc hoặc cần Minh quyết:
   - Cần quyết: R1–R7. Cần biết hoặc chọn: R8–R14. D1, D2 là đề xuất cho T-045.
   - Task chưa đạt tiêu chí nào. Các câu A1–A5 chưa được trả lời, vì chưa có code.
   - Các khuyến nghị ở R3–R5, R9 là cách đọc của người làm, **chưa kiểm**, và người làm cũng là người viết đặc tả T-043, nên có thể mang cùng cách hiểu sai. Codex chưa xem các điểm này.
5. Bước tiếp theo chính xác: chờ Minh trả lời. Sau khi Minh duyệt: ghi các sửa SPEC đã duyệt (nếu Minh cho phép sửa SPEC); ghi `results/T-044/dinh-chinh-cai-dat.md` với các quyết định; làm bước 1 của SPEC: `$HOME/m1env/bin/python -m pip install pyarrow==18.1.0`, tạo `results/T-044/requirements-m1.txt` và `results/T-044/freeze-m1.txt`, rồi chạy `$HOME/m1env/bin/python -c` in phiên bản từng gói.
6. Lệnh cuối cùng đã chạy trước khi ghi LOG: kiểm chữ ký `drain3.drain.Drain.tree_search` bằng `inspect` (chỉ đọc).

Lệnh phép đếm vòng (chỉ đọc, không nhãn): đọc `results/T-043/ks16/dem-khong-nhan.json`; với mỗi ca, dựng đồ thị có hướng từ `call_rows` có n_N + n_A > 0 (bỏ cạnh tự lặp); tìm SCC bằng Tarjan; đếm ca có SCC từ 2 nút. Chạy bằng `$HOME/m1env/bin/python -c`, kết quả ghi ở mục Diễn biến.

---

## Prompt bàn giao của lượt này cho agent đối phương

Prompt cho Codex soát các đề xuất sửa SPEC của lượt này. Minh quyết có gửi hay không.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-044, tasks/T-044-cai-dat-m1/SPEC.md; các đề xuất sửa SPEC và đính chính do người làm trình sau khi tự rà SPEC, ghi ở tasks/T-044-cai-dat-m1/LOG.md, phiên 1, mục "Tự rà SPEC" và "Kết luận giai đoạn 1".
- Công đoạn: soát SPEC (các đề xuất sửa SPEC T-044 và đính chính đề xuất, trước khi viết code).
- Gói/cổng: P6 (M1); chuẩn bị G3.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện.
- Tài liệu gốc: tasks/T-044-cai-dat-m1/SPEC.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md Phụ lục B, C, D; results/T-043/dac-ta-phuong-phap-v1.md, hop-dong.json, ma-tran-thu.json, dinh-nghia-pha2.json, fixture-dac-ta.json, fixture/fixture-bo-sung.json, fixture/ket-qua-kiem.json, dinh-chinh-phien8.md, dinh-chinh-phien9.md, dinh-chinh-phien10.md, bao-cao.md, ks16/dem-khong-nhan.json; tasks/T-045-chay-khoi-k-dev/SPEC.md; src/p3/. Branch claude/sweet-hawking-dy078d trên remote github.com/levanminh04/RCA; điểm gốc của branch là commit 6b2f6ac6 (trùng master); xem git diff 6b2f6ac6..origin/claude/sweet-hawking-dy078d.
- Phản biện và phản hồi trước: lượt rà SPEC T-044 của Codex trong chat ngày 29/10/2026, đã nhập vào SPEC theo Q-212; ngoài ra không có.
- Code và kết quả liên quan: chưa có code. Lệnh kiểm hash T-043: py -3 -B results/T-043/scripts/tao_manifest.py --kiem.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

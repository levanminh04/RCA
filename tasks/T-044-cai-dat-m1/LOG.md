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

---

### Lượt 2 (phiên 1) — đề xuất chi tiết theo yêu cầu của Minh

**Lời Minh:** "đã cập nhật quyền cho github, các đề xuất bên trên tôi muốn nghe đề xuất chi tiết của bạn, tôi không muốn đi theo hướng chọn dễ bỏ khó, chỉ bỏ khi chúng ít mang lại giá trị".

**Đã làm thêm:**
- Push branch thành công (`895a76bc` lên `origin/claude/sweet-hawking-dy078d`).
- Đọc code gốc của Nezha (github.com/IntelligentDDS/nezha, commit `d8140101fdb4`): `log_parsing.py`, `log_template/drain3_hipster.ini`, `log_template/drain3_ts.ini`. Bản clone không blob nằm ngoài repo, ở `/home/user/intelligentdds/nezha`. Lệnh `git ls-tree -l` đã lỡ kéo khoảng 295 MB blob trước khi tôi dừng nó; không đụng repo RCA.
- Đọc mã TrainTicket (github.com/FudanSELab/train-ticket, commit `313886e99bef`): `RouteServiceImpl.java`, `SeatServiceImpl.java`. Bản clone không blob ở `/home/user/fudanselab/train-ticket`, ngoài repo.
- Thử drain3 0.9.11 trong bộ nhớ, trên 2 ví dụ đồ chơi, ngưỡng 0,4, độ sâu 4:
  - N gồm 20 dòng "TraceID: <HEX> SpanID: <HEX> conversion request successful". Dòng A "… conversion request failed": `match` (khớp hoàn toàn) trả không khớp; `tree_search` (ngưỡng 0,4) gán vào mẫu "successful".
  - N có "order <NUM> placed by alice" một lần. Dòng A "… placed by bob": `match` trả không khớp; `tree_search` gán đúng mẫu "alice".

**Nguyên tắc chọn ở lượt này:**
- prior work là mặc định (QT2);
- khi nguồn không phân xử được mà phép đo không nhãn rẻ, thì đo trên dev trước khi chốt;
- đổi thiết kế đã đóng băng thì ghi rõ là đổi thiết kế;
- chỉ bỏ phần ít giá trị, và nói vì sao ít giá trị.

**R1 — kiểm hash T-043 trên bản clone.**
- Đề xuất: viết `results/T-044/scripts/kiem_hash_t043.py`:
  - chép `results/T-043` vào thư mục tạm;
  - tạo lại thư mục của lượt có trong `manifest.json#/luot_chay` mà không có trên đĩa, chỉ khi manifest không ghi file nào dưới đường dẫn đó (tức thư mục vốn rỗng);
  - chạy nguyên `tao_manifest.py --kiem` trên bản sao; in danh sách thư mục đã dựng; mọi lệch khác vẫn FAIL.
- Dùng lại được ở mọi phiên cloud và ở T-045 nếu T-045 chạy trên clone mới.
- Không sửa T-043: thêm `.gitkeep` sẽ làm manifest báo "thừa" và buộc mở lại T-043, trái Q-209 mục 7.
- Sửa SPEC dòng 118: "PASS ở đầu phiên, chạy trực tiếp, hoặc qua `results/T-044/scripts/kiem_hash_t043.py` khi bản clone thiếu thư mục rỗng của lượt hỏng (git không lưu thư mục rỗng)."

**R2 — E1-CP.**
- Đề xuất: cài E1-CP đủ như một chế độ của E1 (`params.bat_tat.E1 = "CP"`; hợp đồng đã có giá trị này), theo CRISP §5.1–5.2 (`the-doc/crisp.md`):
  - con kết thúc cuối (LFC) nằm trên đường găng; lùi dần theo happensBefore với 1 ms, khi không có sự kiện của con khác trong vùng chồng lấn;
  - con cắt về [s₀, s₁) của cha;
  - u = d − |hợp các con trên đường găng|.
- Kiểm: fixture 2, 3, và một ca span tự lập (cha có ba con, hai con song song).
- Không đưa E1-CP vào ma trận dev; giữ quyết định K-b không chạy E1-CP (Q2).
- Vì sao làm đủ, không chỉ viết một hàm rời: Đ21 ghi khác biệt E1-CP so với E1-U trên 444 cha chồng lấn ở Nezha-OB "chưa được kiểm"; có chế độ CP thì T-045 đo được khác biệt này gần như không tốn (D4); chặng 2 (FlashTicket có gọi song song) dùng lại được.
- Sửa SPEC dòng 131: "E1-CP không thuộc ma trận dev (khai trước KHÔNG ĐỦ CA, chặng 2); chế độ E1 = CP vẫn được cài và kiểm bằng fixture 2, 3." Sửa dòng 96: "E1-U, E1-CP (2–5)".

**R3 — UV-6.**
- Căn cứ chọn định nghĩa:
  - codebook T-028 (WHY-38) coi ca "đúng tại k" là ca có Hit@k = 1 theo phân phối chính xác; ca có 0 < Hit@k < 1 mang nhãn riêng M3 (hòa cắt biên);
  - LOG T-043 dòng 4580 và 4814 dùng "ca đúng" theo Hit@1.
- Định nghĩa đề xuất, cho cặp (c bỏ E3, c):
  - ca đang đúng: Hit@1(c bỏ E3) = 1;
  - ca bị hỏng: ca đang đúng mà Hit@1(c) < 1, kể cả khi root rơi vào hòa ở đầu;
  - ca lỗi mã được sửa: loại lỗi return hoặc exception (nhãn dev, chỉ đọc ở pha 2), Hit@1(c bỏ E3) < 1 và Hit@1(c) = 1;
  - vi phạm khi số ca bị hỏng lớn hơn số ca được sửa; đếm trên 52 ca; tính riêng trong P, S_lo, S_hi;
  - ca không OK có Hit@1 = 0 (WHY-28), nên không thể là ca đang đúng.
- Báo kèm, không dùng để quyết định: bản tính theo phần chênh của Hit@1 kỳ vọng; số ca lỗi mã có root lên hạng.
- Chỉ áp cho cặp một thành phần; xem R7 (vii) về cặp (R0, c).
- Đáp án tự lập: một ca hỏng do hòa ở đầu; một ca return được sửa; một ca exception lên hạng 3 → 2 (không tính là sửa); một phép đếm vi phạm và một phép đếm không vi phạm.

**R4 — nhóm vòng (SCC) của E5.**
- Ba cách đọc:
  - (A) giữ kề cạnh: e ∈ S chỉ được bên được gọi trực tiếp b giải thích; nếu b ∈ S thì b phải có kênh không lan;
  - (B) như (A), nhưng bên gọi ngoài S không giải thích được kênh lan xuôi (đọc chữ "chỉ" theo nghĩa đen);
  - (C′) co vòng: coi S như một nút.
    - Kênh lan ngược của e ∈ S là kế thừa khi có thành viên m ≠ e có kênh F_raw không lan (E1, E2, tài nguyên tăng), hoặc có b ∉ S được một thành viên nào đó của S gọi và b có kênh F_raw thuộc lớp giải thích được của luật chung.
    - Kênh lan xuôi của e ∈ S là kế thừa khi có thành viên m ≠ e có kênh không lan, hoặc có a ∉ S gọi một thành viên của S và a có kênh F_raw bất kỳ.
- Khuyến nghị (C′):
  - luật chung đã "bắc cầu theo F_raw". Với chuỗi travel → seat → config mà config chậm, không có vòng thì travel được giải thích qua seat;
  - có vòng seat ↔ travel (RE2-TT có vòng ở 24/30 ca) thì (A) chặn mất chuỗi đó, vì seat chỉ có kênh lan ngược. travel thành nghi phạm giả chỉ vì có vòng;
  - (C′) giữ chuỗi tới nguyên nhân ngoài vòng, mà vẫn không cho hai triệu chứng trong vòng giải thích lẫn nhau. Câu SCC dùng chữ "thành viên", không kèm điều kiện kề cạnh; trong SCC mọi thành viên tới được nhau.
- Mặt trái: một cờ không lan yếu ở một thành viên xa vẫn xóa được bằng chứng mạnh của root nằm trong vòng. Đây là cùng loại điều kiện thất bại với fixture 57, nhưng tầm rộng hơn; ghi vào điều kiện thất bại của E5.
- Fixture 8 đúng ở cả ba cách đọc. Đáp án tự lập để phân biệt các cách: vòng 3 nút như RE2-TT với (a) nguyên nhân ngoài vòng gọi qua seat; (b) cờ CPU ở travel2; (c) kênh lan xuôi của seat, có bên gọi ngoài vòng; (d) vòng 2 nút chỉ có kênh lan ngược.

**R5 — đường xử lý log của E3 (Drain).**
1. Chuỗi đưa vào Drain:
   - Nezha `log_parsing.py`, hàm `pod_to_service` (dòng 94–127): adservice và cartservice dùng chuỗi `log` của JSON ngoài; tám dịch vụ còn lại giải mã `log` thêm một lần rồi lấy `message`. Điều này khớp với KS-16: adservice và cartservice không có severity xác định (Đ15).
   - Đề xuất cho Nezha-OB, viết thành một quy tắc chung không gọi tên dịch vụ: lấy `log`; nếu `log` giải mã được thành JSON có khóa `message` kiểu chuỗi thì dùng `message`, không thì dùng `log`; JSON ngoài không giải mã được thì dùng nguyên chuỗi. Adapter làm việc này, không phải lõi. `severity_raw` giữ đường đọc cũ.
   - RE2-TT dùng cột `message` nguyên văn. Cấu hình TrainTicket của Nezha thuộc một triển khai khác, nên chưa có căn cứ áp cho RCAEval.
2. Khớp dòng A:
   - Hai cách hỏng theo hai kiểu, như ví dụ đồ chơi ở trên.
   - Khớp theo ngưỡng 0,4 hỏng im lặng: dòng lỗi mới bị gộp vào mẫu thường. Khi đó E3 ra KHÔNG TÁC DỤNG hoặc KHÔNG ĐỦ CA, rồi được giữ bật theo D2a mà không làm gì.
   - Khớp hoàn toàn hỏng lộ ra được: tín hiệu giả hiện qua vế mốc giả và UV-6, và giảm được bằng che token.
   - Nezha học trên toàn bộ dữ liệu với ngưỡng cao (OB 0,9; TT 0,8), nên dòng thông điệp mới thường thành cụm mới, gần với khớp hoàn toàn.
   - Đề xuất: cài cả hai cách khớp, chọn bằng `params.tham_so_E3.khop`; mặc định khớp hoàn toàn (`TemplateMiner.match`, `full_search_strategy="fallback"`); T-045 đo cả hai bằng phép không nhãn (D3) trước khối K, trình ở điểm dừng D17 để Minh chốt.
3. Che token (**đổi thiết kế**: bỏ "chuỗi trong ngoặc" khỏi SPEC T-043 B2 E3):
   - TrainTicket ghi log dạng `"[getRouteById][Find route error][Route not found][RouteId: {}]"` (`RouteServiceImpl.java` dòng 84). Che chuỗi trong ngoặc biến dòng này thành `[<*>][<*>][<*>][<*>]`, một token. Mọi thông điệp có cùng số nhóm ngoặc gộp làm một mẫu, gộp cả dòng lỗi với dòng thường.
   - Chưa kiểm RE2-TT có dùng đúng bản TrainTicket này không (T-002 không ghi phiên bản). Nezha không che ngoặc ở cả hai cấu hình.
   - Đề xuất: che theo thứ tự, với ranh giới không dính chữ hoặc số như Nezha: UUID → `<UUID>`; IPv4, cổng tùy chọn → `<IP>`; `0x…` và chuỗi hex dài ≥ 8 có ít nhất một chữ số và một chữ a–f → `<HEX>`; số nguyên hoặc thập phân có dấu → `<NUM>`. Tắt phần che sẵn của drain3.
   - Không lấy các mẫu che riêng của Nezha cho OB (ITEM, PRODUCTID…), vì chúng gắn với từng câu log của Online Boutique, trái WHY-08.
4. Thứ tự học: sắp dòng N theo (mốc ns, thực thể, nội dung) rồi mới đưa vào Drain.
5. Ngưỡng 0,4:
   - Lệch prior work (Nezha dùng 0,9 và 0,8) và chưa có WHY.
   - Căn cứ có trong repo: `results/T-016/dung-logts-tracets.md` dòng 60 — với log OB chưa che, ngưỡng 0,4 cho 95 mẫu so với 73 của tác giả TORAI, còn ngưỡng cao hơn tách tới 1.398 mẫu.
   - Đề xuất: giữ 0,4 và ghi WHY; D3 báo thêm số đo ở ngưỡng của Nezha để thấy độ nhạy; chỉ đổi khi Minh quyết.

**R6 — hồ sơ nguồn (đính chính hợp đồng, như cách Đ19 làm).**
- `params.ho_so_nguon` gồm ba khóa:
  - `kenh_metric`: {kiểu "hậu tố" hoặc "tên kênh", bảng → lớp};
  - `quy_tac_log`: {kiểu "từ khóa", danh sách, không phân biệt hoa thường} hoặc {kiểu "severity", danh sách lỗi, danh sách không lỗi};
  - `nguon_khoi_phat`: danh sách nguồn dùng cho khởi phát E9.
- Giá trị:
  - RE2-TT: 8 hậu tố (`hop-dong.json` dòng 55); từ khóa ERROR, FAIL, EXCEPTION, tìm chuỗi con (`src/simplerca/core.py:87`); khởi phát từ trace và metric;
  - Nezha-OB: 21 tên kênh (dòng 61); severity theo dòng 69; khởi phát chỉ từ trace (đặc tả v1 dòng 379).
- Runner điền từ `hop-dong.json`. Thiếu khóa hoặc gặp lớp lạ thì bản ghi ERROR; không suy từ dữ liệu. Bảng lớp → hướng → lớp lan (`lop_huong`) như nhau cho mọi dataset, nên nằm trong lõi.
- Thêm `params.tham_so_E3` = {khop, sim_th = 0,4, do_sau = 4} cho R5.

**R7 — đáp án tự lập cho các phần thiếu.**
- Mở rộng N1 (Q-212) sang: (i) đếm cờ M5, dùng G_N theo codebook §4 (cả hai span trong N); (ii) phụ thuộc quan sát; (iii) bước 8 luật khối; (iv) E7; (v) E9; (vi) T4c; (vii) cặp (R0, c).
- Định nghĩa đề xuất cho (iii): thành phần đang bật mà phép đảo cho HẠI, hoặc KHÔNG TÁC DỤNG trong khi nó không phải thành phần cuối còn đáp ứng tầng 2, thì là xung đột; thành phần đang tắt mà phép đảo cho GIÚP thì là xung đột; còn TRÁI CHIỀU thì báo để Minh quyết.
- Định nghĩa đề xuất cho (vii): với cặp (R0, c) ở bước 4 luật khối, chỉ áp các vế không gắn với thành phần nào (mốc giả; M + M′ ≥ 3 và P + P′ = 0; TRÁI CHIỀU; HẠI gộp). UV-6 và điều kiện M5 chỉ áp cho cặp một thành phần, vì:
  - Phụ lục C định nghĩa chúng cho một thành phần ("So cặp (c bỏ E5, c)");
  - mọi c có E3 hoặc E5 đều đã qua cặp một thành phần, nên không mất phép chặn nào.
  - Nhãn kết cục của (R0, c) dùng hợp các E_X của thành phần trong c.
- Ghi vào `results/T-044/fixture/dap-an-thanh-phan.json`, đánh dấu như N1.
- Sửa SPEC dòng 89 tương ứng; tiêu chí 2 (dòng 119) thêm "và các ca trong `dap-an-doi-chung.json`, `dap-an-thanh-phan.json`".

**R9 — bốn định nghĩa.**
- **T4c:** K′ = (max s, max m, số kênh, Σs), tức m đứng ngay sau max s.
  - Lý do: nhánh z (phép so của T4b) để độ lớn đứng đầu trong tầng; T4c là bản không phụ thuộc đơn vị của đúng ý đó. Đặt m ở cuối chỉ phá hòa tuyệt đối, nên gần như không đổi gì; giá trị thấp, không làm.
  - max m lấy trên các kênh có cờ của chính khóa đó; r_u là hiệu dương nhỏ nhất giữa hai giá trị khác nhau trong N ∪ A; nếu mọi giá trị bằng nhau thì m = 0.
  - Xếp lại trên lượt R0 mặc định (ε = 0,05; α = 0,01), không chấm lại; T4 vẫn là 9 cấu hình.
- **E7, cách 1**, trên đồ thị con F_raw: R_r = {r} ∪ Lên ∪ Xuống.
  - Lên = {a có đường a → … → r, và mọi kênh F_raw của a có giải thích theo luật E5}. "Có giải thích" gồm trạng thái "đề xuất" khi E5 tắt và "áp dụng" khi E5 bật; kênh bị E9 phủ quyết không tính.
  - Xuống = {b có đường r → … → b, và có ít nhất một kênh F_raw lớp lan xuôi có giải thích}.
  - Dùng cả trạng thái "đề xuất" để vùng không rỗng chỉ vì E5 tắt.
- **E9:**
  - ô 10 giây đặt từ t; mẫu vào ô theo end của span, hoặc theo mốc thật của nguồn metric; ô không có mẫu thì bỏ qua; khởi phát tính theo hướng có cờ;
  - đơn vị đã có cờ thì luôn có khởi phát, vì r_d(A) > r_d(N) buộc ít nhất một ô vượt r_d(N);
  - "tắt trên cạnh có E2 bất thường" chỉ áp khi E2 bật. Không tính E2 riêng để chặn E9 khi E2 tắt, vì làm vậy sẽ bỏ mất lần phủ quyết đúng khi bên được gọi chỉ có nhiễu.
- **C-d1:**
  - nhóm 1: thực thể có cờ mà không bên được gọi nào có cờ; nhóm 2: các thực thể có cờ còn lại; nhóm 3: tầng 3. Trong nhóm xếp theo K_raw;
  - tính lại trên kết quả chấm của từng cấu hình, không phải cấu hình riêng.

**R13 — test bổ sung.**
- Chạy đầu-cuối từ span cho cả bảy ca S1–S7. Bộ sinh trace dùng `#/trace_mau_S`: 20 request ở N và 20 ở A, con nối tiếp nhau, khoảng ngoài span 1 ms.
- Đầu vào người làm bổ sung, đánh dấu rõ:
  - S3: R trả lỗi nhanh (R.handle 31 → 5 ms), không gọi X; mỗi request một dòng lỗi ở F, A, R trong A; thêm dòng INFO ở cả N và A. Không có dòng INFO ở N thì H của log bắt đầu ở A, làm T_N^chắc = 0 và kênh log ra NO_BASELINE; ca này cho thấy giá trị của phép đầu-cuối;
  - S6: 20 span R.newop là span gốc riêng, chỉ có ở A;
  - S7: R không có span; span X.handle thành span mồ côi.
- Đáp án vẫn là của fixture 1. Lệch thì ghi đính chính.
- Đáp án trong văn bản: Đ10 (hai ví dụ), đặc tả v1 dòng 349, SPEC T-043 dòng 392, Đ17 (người làm bổ sung dataset của từng ca và |E_X|).

**R8 — adapter.**
- Thêm bộ dữ liệu tổng hợp nhỏ, do test sinh ra trong thư mục tạm, đi đúng đường đọc `src/p3/selector.py` (RE2-TT, parquet) và `src/p3/nezha.py` (allowlist, sha256, 11 nguồn metric, 165 kênh, 5 + 5 điểm).
- Mục đích: kiểm adapter → M1 → bản ghi trên chính bộ đọc của P3, trước T-045. Cần pyarrow (bước 1).

**Đề xuất cho T-045** (cần sửa SPEC T-045; Minh quyết riêng):
- D1: đối chiếu số trung gian của M1 với KS-16 từng ca. Rẻ, không nhãn, kiểm adapter trên dữ liệu thật.
- D2: tái lập MRR và số ca M5 của sáu baseline bằng `src/m1_danh_gia`. G_N lấy từ `call_rows` của KS-16; đích so là `results/T-034/bang-baseline.json` và `ks16/dem-sau-ghep-nhan.json#/hinh_dang_xep_hang_baseline`.
- D3 (mới): đo E3 không nhãn trước khối K:
  - số mẫu theo thực thể; tỷ lệ dòng A vào "mẫu mới" và số thực thể có cờ mẫu mới, ở cả hai cách khớp;
  - ở Nezha-OB: số dòng A severity lỗi bị gán vào mẫu không phải lỗi;
  - ở mốc giả RE2-TT: số thực thể có cờ mẫu mới;
  - in năm mẫu đầu của hai ca mỗi dataset;
  - tùy chọn: số đo ở ngưỡng của Nezha.
  - Trình ở điểm dừng D17. Chi phí vài phút máy.
- D4 (mới): mô tả khác biệt u_CP − u_U trên 444 cha chồng lấn ở Nezha-OB. Chỉ mô tả.

**Cần Minh duyệt:** SPEC T-044 dòng 89, 96, 118, 119, 131; các đính chính sẽ ghi vào `results/T-044/dinh-chinh-cai-dat.md` (UV-6, SCC, E3 kèm đổi thiết kế che token, hồ sơ nguồn, cặp (R0, c), T4c, E7, E9, C-d1); WHY cho các lựa chọn E3 và SCC (soạn sau khi Minh chốt); SPEC T-045 cho D1–D4.

**Tác dụng phụ ngoài repo trong phiên:** bản sao `results/T-043` trong scratchpad (`…/scratchpad/manifest-check`); hai bản clone chỉ đọc `/home/user/intelligentdds/nezha` (khoảng 295 MB) và `/home/user/fudanselab/train-ticket`. Đề xuất xóa ba thư mục này khi Minh đồng ý; nội dung cần dẫn đã ghi bằng commit và số dòng ở trên.

**Kết thúc lượt 2 (AGENTS mục 7):**
1. Đã làm gì: push; đọc code gốc Nezha và TrainTicket; thử drain3; soạn đề xuất chi tiết.
2. File đã thay đổi: LOG này (ghi thêm). Ngoài repo: như mục trên.
3. Kiểm: như mục "Đã làm thêm".
4. Cần Minh quyết: như mục "Cần Minh duyệt". Các khuyến nghị đều **chưa kiểm** trên dữ liệu thật. Riêng giả định RE2-TT ghi log theo kiểu ngoặc của TrainTicket bản `313886e` chưa xác nhận; D3 sẽ cho thấy.
5. Bước tiếp theo chính xác: chờ Minh trả lời. Sau khi duyệt: sửa SPEC đã duyệt; ghi `dinh-chinh-cai-dat.md`; làm bước 1 (`$HOME/m1env/bin/python -m pip install pyarrow==18.1.0`), rồi đi tiếp các bước của SPEC.
6. Lệnh cuối: đọc dòng log của `SeatServiceImpl.java` bằng `git show` (chỉ đọc).

#### Prompt bàn giao của lượt 2 cho agent đối phương

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-044, tasks/T-044-cai-dat-m1/SPEC.md; các đề xuất sửa SPEC và đính chính do người làm trình sau khi tự rà SPEC, ghi ở tasks/T-044-cai-dat-m1/LOG.md, phiên 1: mục "Tự rà SPEC", "Kết luận giai đoạn 1" và "Lượt 2 (phiên 1) — đề xuất chi tiết theo yêu cầu của Minh".
- Công đoạn: soát SPEC (các đề xuất sửa SPEC T-044, đính chính và đề xuất cho T-045, trước khi viết code).
- Gói/cổng: P6 (M1); chuẩn bị G3.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện.
- Tài liệu gốc: tasks/T-044-cai-dat-m1/SPEC.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md Phụ lục B, C, D; results/T-043/dac-ta-phuong-phap-v1.md, hop-dong.json, ma-tran-thu.json, dinh-nghia-pha2.json, fixture-dac-ta.json, fixture/fixture-bo-sung.json, fixture/ket-qua-kiem.json, dinh-chinh-phien8.md, dinh-chinh-phien9.md, dinh-chinh-phien10.md, bao-cao.md, the-doc/crisp.md, ks16/dem-khong-nhan.json; results/T-028/codebook.md; results/T-016/dung-logts-tracets.md; tasks/T-045-chay-khoi-k-dev/SPEC.md; src/p3/; mã nguồn ngoài: github.com/IntelligentDDS/nezha commit d8140101fdb4 (log_parsing.py, log_template/*.ini), github.com/FudanSELab/train-ticket commit 313886e99bef. Branch claude/sweet-hawking-dy078d trên remote github.com/levanminh04/RCA; điểm gốc của branch là commit 6b2f6ac6 (trùng master); xem git diff 6b2f6ac6..origin/claude/sweet-hawking-dy078d.
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

---

### Lượt 2, phần bổ sung (phiên 1) — soát lại trước khi trình Minh

**Đã làm:**
- Commit, push `3b5b86cf`.
- Soát lại mọi trích dẫn của mục lượt 2 trên file gốc. Các số dòng và con trỏ đều khớp.
- Tính lại nhóm vòng từ `results/T-043/ks16/dem-khong-nhan.json#/cases/*/call_rows` (file không nhãn, `#/labels_read` = false), bằng networkx 2.5 trong bộ nhớ:
  - RE2-TT: nhóm vòng {ts-seat-service, ts-travel-service, ts-travel2-service} ở 24/30 ca; cạnh trong vòng là seat ↔ travel và seat ↔ travel2;
  - Nezha-OB: 0/22 ca;
  - số này tính trên đồ thị gọi đầy đủ. E5 xét vòng trên đồ thị con F_raw (D19), nên số ca E5 gặp vòng chưa biết.
- Đọc docstring `TemplateMiner.match` và tham số mặc định của drain3 0.9.11 đã cài.
- Đọc mã TrainTicket v1.0.0 có sẵn trong repo (T-038).

**Sửa và bổ sung so với mục lượt 2** (mục lượt 2 giữ nguyên làm lịch sử):

1. **R1.** Sửa cả ba chỗ nói "PASS": SPEC T-044 dòng 44, 86, 118. Lượt 2 chỉ nêu dòng 118.
2. **R2.**
   - Sửa thêm dòng 64 (đầu ra 1, danh sách thành phần): thêm E1-CP. Hợp đồng đã có giá trị này (`hop-dong.json` dòng 13: `"E1": "U|CP|tat"`).
   - Ca tự lập, tính tay: cha [0; 100); ba con [10; 40), [20; 60), [65; 90).
     - Đường găng: [65; 90) kết thúc cuối; lùi về [20; 60); con [10; 40) kết thúc trong khoảng của [20; 60) nên bị bỏ qua.
     - u_CP = 100 − (40 + 25) = 35; u_U = 100 − |[10; 60) ∪ [65; 90)| = 100 − 75 = 25.
3. **R3.**
   - Đếm gộp 52 ca là cách đọc theo câu chữ: `ma-tran-thu.json#/dieu_kien_rieng/E3` không chia theo dataset.
   - Ô kích hoạt E3 chỉ có ở Nezha-OB (`dinh-nghia-pha2.json#/o_kich_hoat/E3/dieu_kien_ca`: "RE2-TT không có loại lỗi mã"). Vậy "được sửa" chỉ xảy ra ở Nezha-OB; "bị hỏng" xảy ra ở cả hai dataset.
   - Phương án đếm riêng theo dataset chặt hơn: một ca hỏng ở RE2-TT luôn là vi phạm. Báo kèm số theo dataset; Minh chọn.
4. **R4.**
   - Lý do đổi khuyến nghị từ cách (A) ở giai đoạn 1 sang (C′): ví dụ chuỗi travel → seat → config có vòng seat ↔ travel, ở mục lượt 2.
   - Thêm D5 (tùy chọn, cho T-045): ở pha 1, đếm số kênh có trạng thái kế thừa khác nhau giữa (A) và (C′). Không nhãn; chỉ để biết mức ảnh hưởng của cách đọc; không dùng để chọn.
5. **R5.**
   - (2) Câu "E3 ra KHÔNG TÁC DỤNG hoặc KHÔNG ĐỦ CA, rồi được giữ bật theo D2a" ở lượt 2 chưa chính xác.
     - D2a chỉ giữ bật khi KHÔNG ĐỦ CA.
     - E3 có 4 ô, nên luật C dừng ở KHÔNG ĐỦ CA, trước GIÚP; các vế HẠI đứng trước KHÔNG ĐỦ CA.
     - Hệ quả: trên dev, lợi ích của E3 không thể ra GIÚP; chỉ phần hại là bắt được. Cách khớp làm lỗi lộ ra mới giữ được tác dụng của luật C đối với E3.
   - (2) Mặt trái của từng cách khớp:
     - khớp hoàn toàn: N của Nezha-OB chỉ dài 42–97 giây (đặc tả v1 dòng 241). Token biến chỉ gặp một giá trị ở N thì vẫn là chữ cố định trong mẫu; dòng A cùng mẫu mà khác giá trị sẽ vào "mẫu mới";
     - khớp theo ngưỡng: khi E3 bật, kênh log lỗi cơ bản bị thay (`hop-dong.json` dòng 51). Dòng lỗi bị gộp vào mẫu lớp thường thì mất hẳn bằng chứng log lỗi.
   - (2) Thêm phương án (c): khớp theo ngưỡng 0,4, nhưng chỉ trong các mẫu cùng lớp với dòng.
     - Dòng lỗi (severity ở Nezha-OB, từ khóa ở RE2-TT) chỉ khớp mẫu lớp lỗi; dòng thường chỉ khớp mẫu lớp thường; dòng UNKNOWN khớp mọi mẫu. Không khớp thì vào "mẫu mới".
     - (c) chặn được cả hai kiểu hỏng trên. Đây là cơ chế mới, chưa có prior work; nếu chọn thì phải có WHY.
   - (2) Đề xuất thay bản lượt 2: cài cả (a) khớp hoàn toàn, (b) khớp theo ngưỡng, (c).
     - Mặc định (a), vì đó là hàm suy luận của chính drain3: "Match shall be perfect (sim_th=1.0)" (`drain3/template_miner.py` dòng 149–152, bản 0.9.11; `full_search_strategy="fallback"` theo docstring dòng 156–166).
     - D3 đo cả ba; Minh chốt ở điểm dừng D17.
   - (3) Bằng chứng trong repo, thay cho bản clone ngoài:
     - TrainTicket v1.0.0 lưu ở `results/T-038/sources/train-ticket-v1.0.0/`; T-038 dùng bản này làm snapshot tham khảo có điều kiện (`results/T-038/de-xuat-nguon-va-tach.md` dòng 9). Chưa xác nhận RE2-TT chạy đúng bản này;
     - `ts-route-service/src/main/java/route/service/RouteServiceImpl.java` dòng 84 (error) và `ts-seat-service/src/main/java/seat/service/SeatServiceImpl.java` dòng 114 (info) đều có bốn nhóm ngoặc vuông. Che nội dung trong ngoặc biến cả hai dòng thành cùng một token;
     - phương án (b) hiểu "ngoặc" là ngoặc kép: không có căn cứ trong T-043. Nguy cơ chưa kiểm: gộp các thông điệp dạng JSON chỉ khác giá trị chuỗi.
   - (6) Mới: các tham số còn lại của drain3 giữ mặc định của 0.9.11 (`drain3/drain.py` dòng 54–61): max_children 100, max_clusters không giới hạn, extra_delimiters rỗng, parametrize_numeric_tokens True. Ghi vào `params.tham_so_E3`. Không lấy extra_delimiters ["_"] trong cấu hình OB của Nezha (WHY-08).
   - D3 bổ sung: ở cả hai dataset, với từng cách khớp, đếm số dòng A là dòng lỗi mà bị gán vào mẫu lớp thường.
6. **R7.**
   - (iii) Định nghĩa thay bản lượt 2. Với cấu hình thắng w và thành phần x, đảo x trong cùng bối cảnh; xét cặp (w không có x, w có x):
     - x đang bật: GIÚP hoặc KHÔNG ĐỦ CA (D2a) là nhất quán; HẠI hoặc KHÔNG TÁC DỤNG là xung đột;
     - x đang tắt: HẠI hoặc KHÔNG TÁC DỤNG là nhất quán; GIÚP là xung đột; KHÔNG ĐỦ CA là xung đột với D2a;
     - TRÁI CHIỀU: chưa phân xử, trình Minh. "Phụ thuộc quan sát" xử lý như KHÔNG ĐỦ CA (D2f);
     - bỏ ngoại lệ "thành phần cuối còn đáp ứng tầng 2" của bản lượt 2: luật chọn khối không dùng tầng 2 để chọn; bước 8 chỉ yêu cầu trình Minh.
   - (vii) Lý do thay bản lượt 2: ở cặp (R0, c), số ca hỏng hay số cờ M5 có thể đổi do thành phần khác trong c. Áp UV-6 hay điều kiện M5 cho cặp này là gán cho E3 hay E5 phần thay đổi không phải của chúng. Câu "không mất phép chặn nào" ở lượt 2 quá mạnh; cách đọc này bỏ hẳn phép UV-6 trên (R0, c).
7. **R9.**
   - T4c, đơn vị đếm: m tính theo tần suất. λ = n/T; m = log(1 + |λ_A − λ_N| / max(λ_N, r_u)), với r_u = 1/T_N (một sự kiện trong thời gian quan sát N).
     - Lý do: đơn vị đếm cũng bão hòa. n_N = 0 cho e_up = 1 (đặc tả v1 dòng 119); ô "mẫu mới" luôn có n_N = 0, vì Drain học trên N.
     - Bản giai đoạn 1 (m = 0 cho đơn vị đếm) bỏ đúng chỗ bão hòa hay gặp nhất của log. Đây là tự diễn giải, cần Minh duyệt.
   - T4c, vị trí m: lượt 2 thay giai đoạn 1 (từ cuối khóa lên ngay sau max s). Lượt R0 mặc định ghi thêm thứ tự T4c trong cùng bản ghi pha 1; bộ đánh giá chấm cả hai thứ tự.
   - E9, lý do thay bản lượt 2: thành phần đang tắt thì thông tin của nó không được vào đường tính thứ hạng; có vậy phép bật/tắt mới đo đúng một thành phần. E9 đổi trạng thái kế thừa, tức đổi thứ hạng, nên không tính E2 ngầm khi E2 tắt. E7 dùng trạng thái "đề xuất" của E5 khi E5 tắt thì được, vì E7 chỉ mô tả, không đổi thứ hạng.
8. **Tác dụng phụ ngoài repo:** bản clone TrainTicket ngoài repo không còn cần cho bằng chứng. Vẫn đề xuất xóa cả ba thư mục như mục lượt 2, khi Minh đồng ý.

**Kết thúc phần bổ sung (AGENTS mục 7):**
1. Đã làm: soát trích dẫn; tính lại nhóm vòng; đọc drain3 và TrainTicket v1.0.0 trong repo; ghi phần này.
2. File đã thay đổi: LOG này (ghi thêm). Không sửa SPEC, không có code.
3. Kiểm: networkx trên `call_rows` cho RE2-TT 24/30, Nezha-OB 0/22; so prompt lượt 2 với `docs/review-prompt.md`: chỉ khác phần điền.
4. Cần Minh quyết: danh sách "Cần Minh duyệt" ở lượt 2, sửa theo các mục 1–7 ở trên. Mọi khuyến nghị vẫn chưa kiểm trên dữ liệu thật.
5. Bước tiếp theo: như lượt 2.
6. Lệnh cuối: đọc khóa `params.bat_tat` trong `results/T-043/hop-dong.json` bằng grep (chỉ đọc).

#### Prompt bàn giao sau phần bổ sung cho agent đối phương (thay prompt lượt 2)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-044, tasks/T-044-cai-dat-m1/SPEC.md; các đề xuất sửa SPEC và đính chính do người làm trình sau khi tự rà SPEC, ghi ở tasks/T-044-cai-dat-m1/LOG.md, phiên 1: mục "Tự rà SPEC", "Kết luận giai đoạn 1", "Lượt 2 (phiên 1) — đề xuất chi tiết theo yêu cầu của Minh" và "Lượt 2, phần bổ sung (phiên 1) — soát lại trước khi trình Minh".
- Công đoạn: soát SPEC (các đề xuất sửa SPEC T-044, đính chính và đề xuất cho T-045, trước khi viết code).
- Gói/cổng: P6 (M1); chuẩn bị G3.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện.
- Tài liệu gốc: tasks/T-044-cai-dat-m1/SPEC.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md Phụ lục B, C, D; results/T-043/dac-ta-phuong-phap-v1.md, hop-dong.json, ma-tran-thu.json, dinh-nghia-pha2.json, fixture-dac-ta.json, fixture/fixture-bo-sung.json, fixture/ket-qua-kiem.json, dinh-chinh-phien8.md, dinh-chinh-phien9.md, dinh-chinh-phien10.md, bao-cao.md, the-doc/crisp.md, ks16/dem-khong-nhan.json; results/T-028/codebook.md; results/T-016/dung-logts-tracets.md; results/T-038/de-xuat-nguon-va-tach.md và results/T-038/sources/train-ticket-v1.0.0/ (ts-route-service RouteServiceImpl.java, ts-seat-service SeatServiceImpl.java); tasks/T-045-chay-khoi-k-dev/SPEC.md; src/p3/; drain3 0.9.11 (drain3/template_miner.py, drain3/drain.py); mã nguồn ngoài: github.com/IntelligentDDS/nezha commit d8140101fdb4 (log_parsing.py, log_template/*.ini), github.com/FudanSELab/train-ticket commit 313886e99bef. Branch claude/sweet-hawking-dy078d trên remote github.com/levanminh04/RCA; điểm gốc của branch là commit 6b2f6ac6 (trùng master); xem git diff 6b2f6ac6..origin/claude/sweet-hawking-dy078d.
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

---

### Giai đoạn 2 (phiên 1) — Minh duyệt các đề xuất; bắt đầu triển khai

**Quyết định của Minh trong phiên** (lời Minh trong chat ngày 29/10/2026): "duyệt toàn bộ các đề xuất bên trên của bạn, nếu không còn vướng mắc gì thì hãy tiếp tục t-044 giúp tôi". Phạm vi duyệt là 11 mục "Cần anh duyệt" trong chat, theo các khuyến nghị của người làm, đã ghi ở mục lượt 2 và phần bổ sung:
1. R1: script `results/T-044/scripts/kiem_hash_t043.py`; sửa SPEC T-044 dòng 44, 86, 118.
2. R2: cài đủ chế độ E1-CP, không vào ma trận dev; sửa SPEC T-044 dòng 64, 96, 131.
3. R3: định nghĩa UV-6 theo Hit@1 = 1; đếm **gộp** 52 ca; báo kèm số theo dataset, bản Hit@1 kỳ vọng và số ca lên hạng.
4. R4: nhóm vòng E5 theo cách đọc (C′).
5. R5: chuỗi vào Drain theo quy tắc chung; cài ba cách khớp (a), (b), (c), mặc định (a); **đổi thiết kế**: bỏ che "chuỗi trong ngoặc"; bộ che UUID → IP → HEX → NUM; thứ tự học; giữ ngưỡng 0,4; tham số drain3 còn lại theo mặc định 0.9.11.
6. R6: `params.ho_so_nguon`, `params.tham_so_E3`.
7. R7: mở rộng N1; định nghĩa bước 8 luật chọn khối và cặp (R0, c); sửa SPEC T-044 dòng 89, 119.
8. R8–R14 như đã trình; R13 có đầu vào người làm bổ sung cho S3, S6, S7.
9. Ghi các đính chính vào `results/T-044/dinh-chinh-cai-dat.md`. WHY cho E3 và nhóm vòng: người làm soạn, trình riêng (WHY ngoài phạm vi ghi).
10. Sửa SPEC T-045 cho D1–D5. D5 là mục "tùy chọn" trong đề xuất; lời duyệt "toàn bộ các đề xuất" được hiểu là duyệt cả D5. Vì D5 cần cách đọc (A) của nhóm vòng, `src/m1` cài thêm cách đọc này như một tùy chọn chẩn đoán, không vào ma trận.
11. Xóa ba thư mục ngoài repo đã liệt kê.

Dòng ghi DECISIONS cho các duyệt này: người làm đề xuất ở cuối phiên (AGENTS mục 4); chưa ghi.

**Kế hoạch giai đoạn 2:** áp mục 1, 2, 7, 10 vào SPEC; ghi `dinh-chinh-cai-dat.md` (mục 3–9); xóa thư mục ngoài repo (mục 11); rồi làm bước 0–9 của SPEC T-044. Mỗi bước con ghi một dòng ở đây và commit.
- Mục 11 (xóa thư mục ngoài repo): đã xóa bản sao `manifest-check` trong scratchpad (9,1 MB), `/home/user/intelligentdds/nezha` (295 MB), `/home/user/fudanselab/train-ticket` (396 KB) và hai thư mục cha rỗng. Repo RCA không đổi.
- Áp mục 1, 2, 7 vào SPEC T-044 (dòng 44, 64, 86, 89, 96, 118, 119, 131) và mục 10 vào SPEC T-045 (nguồn hash cho D2; đầu ra 9; D1, D4 trong bước 2; bước 2b cho D3, D5; D17 chốt cách khớp E3; D2 đầu bước 6; một dòng bảng mặc định; tiêu chí 6). Không sửa dòng nào khác.
- Mục 1 (R1): viết `results/T-044/scripts/kiem_hash_t043.py`. Chạy trực tiếp `tao_manifest.py --kiem`: FAIL chỉ vì `luot_thieu: ["runs/khe-open-001"]` (`results/T-044/runs/kiem-hash-t043-001/truc-tiep.txt`). Chạy qua script: dựng lại đúng `runs/khe-open-001`, PASS 69/69 file, 10/10 hash đóng băng (`…/stdout.txt`). Thử phản chứng trên bản sao trong scratchpad có một file bị sửa: script vẫn FAIL, báo `lech`. `results/T-043` không đổi (git status sạch).
- Mục 3–9: ghi `results/T-044/dinh-chinh-cai-dat.md` Phần I (CĐ1–CĐ16), trạng thái "đã duyệt 29/10/2026". Phần II (lệch khi cài) để trống.
- Bước 0 (mở giai đoạn 2): kiểm hash T-043 PASS qua script (mục trên). Đếm: `fixture-dac-ta.json#/fixtures` có 82 mục (id 1–82); `fixture/fixture-bo-sung.json#/fixtures` có 8 mục; `fixture/ket-qua-kiem.json#/so_phep_kiem` = 109. Nguồn đọc: AGENTS, STATE, SPEC T-044, SPEC T-045, SPEC T-043 Phụ lục B–D, đặc tả v1, ba file đính chính (đọc lại theo từng khối khi cài).
- Bước 1 (môi trường): cài pyarrow 18.1.0 từ PyPI (wheel 40 MB) vào `$HOME/m1env`; ghi `results/T-044/requirements-m1.txt` (7 gói) và `results/T-044/freeze-m1.txt` (17 dòng). Kiểm `importlib.metadata.version`: 7/7 khớp. Python 3.12.3 (T-043 dùng 3.12.10 trên Windows).
- Sửa `dinh-chinh-cai-dat.md` CĐ4 trước khi dùng: bản vừa ghi có câu "mỗi thực thể có một Drain riêng", trái Đ15 điểm 5 ("Drain học chung cho mọi thực thể"). Đây là câu người làm tự thêm khi chép, không thuộc đề xuất đã duyệt. Sửa thành một Drain chung cho mọi thực thể, đơn vị là cặp (thực thể, mẫu); ba cách khớp chỉ xét mẫu đã biết của chính thực thể (Đ15 điểm 5).
- Bước 2: ghi `results/T-044/fixture/dap-an-u-h.json`: U1–U6 từ `dinh-chinh-phien10.md` dòng 42–47, H1–H6 từ dòng 144–149. Cột `van_ban` do script tách nguyên văn từng ô; cột `may_doc` người làm chép tay từ đúng ô đó, không thêm hướng ở U3, U6 vì ô không ghi. Chờ người phản biện đối chiếu từng dòng.
- Bước 3 (khung test): viết `results/T-044/tests/` (conftest, 11 file theo khối, `test_tinh.py`, `test_runner.py`, bộ sinh trace `sinh_trace_S.py`) và ba file đáp án tự lập: `results/T-044/fixture/dap-an-thanh-phan.json` (45 mục), `dap-an-doi-chung.json` (11 mục), `dap-an-van-ban.json` (5 mục), cùng dấu "đáp án của người làm T-044, chưa qua phản biện". 208 test được thu; chạy lần đầu: 206 đỏ, 2 xanh (hai kiểm tĩnh trên package rỗng) — `results/T-044/runs/test-do-001/`. Test đọc đáp án từ JSON; không đọc `kiem_fixture.py`.
- Diễn giải phát sinh khi viết test (sẽ ghi vào `dinh-chinh-cai-dat.md` Phần II): cổng qua khi p < α (chặt), như KS-16 pha 2 (`ks16_pha2_v11.py:160`) và E3b ở `dinh-nghia-pha2.json`; đặc tả không ghi ≤ hay <; không fixture nào rơi đúng biên.
- Khối 1 (hợp đồng, trường cấm, CĐ12): `src/m1/hop_dong.py`, `src/m1/kieu.py`; 9/9 test qua (fixture 74 bốn phép, tên cấm, GT1–GT4).
- Khối 2 và 4 (quan sát, đơn vị đếm, ba thế giới; E4, cổng, cache, nhánh z): `src/m1/quan_sat.py`, `src/m1/e4.py`, `src/m1/xep_hang.py` (cần cho fixture 29), `src/m1_danh_gia/rr.py`, `the_gioi.py`. 33/36 test qua; H4–H6 chờ hàm chạy chuỗi (khối 9). Fixture 29 thêm phép kiểm nguyên nhân (chỉ điểm đổi; cặp U1 của A, U2 của B), viết lại từ câu văn của đáp án.
- Khối 3 và 6 (tiền xử lý span, E1-U, E1-CP, E2-C, E2-VC): `src/m1/span.py`, `src/m1/e2.py`. 18/18 test qua (`test_k03_span.py` 5, `test_k06_e1_e2.py` 13; gồm CP1, E2C1, E2VC1 và fixture 2, 3 ở chế độ CP). Commit d1b08650. Dòng LOG này ghi bù sau commit.
- Khối 5, 7, 8 (kênh, severity, E3 Drain chung, E3b, E5 với nhóm vòng C′ và A, E6b, E7, E9): `src/m1/kenh.py`, `e3.py`, `e5.py`, `e7.py`, `e9.py`, `src/m1_danh_gia/e7.py`. 64/64 test qua (`test_k05_kenh.py` 9, `test_k07_e3.py` 20, `test_k08_e5_e6_e7_e9.py` 35). Ba test verdict của khối 9 (31, 42, 82) qua. Commit eabd98de. Dòng LOG này ghi bù sau commit.
- Khối 9 (chuỗi, API 7 tham số): `src/m1/chuoi.py`. `test_k09_chuoi.py` 17/17 qua: S1–S7 × C0–C5 ở mức kênh và đầu-cuối từ span (trace do `sinh_trace_S.py` sinh). Soi trung gian từng ô (thực thể có cờ, tầng, mục kế thừa): khớp lý do mong đợi, ví dụ S3-C4 log lỗi của F, A được giải thích bởi R; S2b-C3 phủ đỉnh chọn R; S7 chỉ A.callR có cờ vì span bọc không có con. H4, H6 qua ngay. H5 đỏ vì test của người làm giả định status 'OK'; đáp án H5 chỉ ghi "kết quả bằng cạnh quan sát; so_canh_tinh = 0", còn ca nhỏ `_ca_nho` không có phép chấm OK nên cả hai bản ghi là NO_EVIDENCE (đúng quy ước `ban_ghi.tao`: OK cần danh sách khác rỗng). Sửa test: so status và kết quả hai bản ghi với nhau, và thêm một ca có bằng chứng dùng cạnh (S2, cấu hình E1-U, E2-VC, E5 bật) để phép so có nghĩa; 16/16 test `test_k02_quan_sat.py` qua. `test_tinh.py` 3/3 qua. Tổng khối 1–9: 147 test qua.
- Khối 10 (đối chứng): `src/m1/doi_chung.py` (C-d1 theo CĐ10, C-d2 theo Đ11, C-d3 theo thẻ đọc PetShop với `networkx.all_simple_paths` của networkx 2.5, C-g, C-c với điểm RRF chính xác bằng phân số), `src/m1_danh_gia/moc_gia.py` (vế mốc giả C-e: mẫu số, CHUA_KIEM_DUOC, KHONG_PHAN_XU_DUOC ở trần, HAI khi tăng > 0,10, so bằng phân số). Kiểm trước: networkx 2.5 trả bộ sinh rỗng khi nguồn trùng đích (`all_simple_paths`, nhánh `if source in targets`), như 2.8.8 của PetShop, nên fixture 18 giữ nghĩa. Chuỗi gắn C-d1, C-d2, C-d3 vào `extra.doi_chung` trên kết quả chấm của cấu hình ở thế giới P (CĐ10); khởi phát (Đ11) giờ luôn tính cho đơn vị phân vị có cờ vì C-d2 cần, E5 chỉ dùng khi E9 bật. Bản ghi thêm `loai_thay_doi` cho đơn vị đếm (tên `nhan` là trường cấm). Thêm 4 đáp án tự lập vào `dap-an-doi-chung.json` (CD1-S3 theo phản ví dụ ở SPEC T-043 B5 "Ở S3, C-d1 chọn X"; CD3-S1; CD3-S7; CD3-KG không span gốc, theo Đ12 và B7), cùng dấu chưa qua phản biện. `test_k10_doi_chung.py` 27/27 qua; khối 9 và khối 2 chạy lại vẫn xanh. Cảnh báo duy nhất: DeprecationWarning của `networkx/release.py` khi import trên Python 3.12, không ảnh hưởng tính toán.
- Khối 11 (bộ đánh giá): `src/m1_danh_gia/luat_c.py` (bảy bước theo thứ tự, phân số chính xác, ngưỡng tăng/giảm ô 1e-12 theo `dinh-nghia-pha2.json#/rr_theo_o`, trọng số và δ_d cố định theo CĐ13, cặp (R0, c) không áp UV-6 và M5 theo CĐ6.4; báo kèm kiểm dấu hai phía và kết cục ở δ = 0,005, 0,02), `chon_khoi.py` (lượt một, lượt hai, cờ trái chiều, tập gần tốt nhất, bước 8), `boi_canh.py`, `m5.py` (đứng trước hẳn theo codebook T-028 §4; G_N theo end), `uv6.py`, `dau_vet.py`. `test_k11_danh_gia.py` 33/33 qua ngay lượt đầu; soi trung gian 34, 38, 40, 54, 60 (ΔMRR từng dataset, P, M, P′, M′, |E_X|, δ_d) và 47, 50 (tập cố định, hai lượt loại, mức chênh −1/312) khớp lời giải của fixture.
- Tự soát phát hiện thiếu: SPEC bước 3 yêu cầu đáp án tự lập cho T4c nhưng `dap-an-thanh-phan.json` chưa có mục T4c, và chuỗi chưa ghi thứ tự T4c (CĐ7: "thứ tự thứ hai, ghi trong cùng bản ghi pha 1"). Đã thêm 7 đáp án tính tay T4C-1…T4C-6 và T4C-S1 (S1 cấu hình C0 qua chuỗi: T4c cho R, A, F; E6a cho A, F trước R), cùng dấu chưa qua phản biện; viết test trước, thấy đỏ, rồi gắn T4c vào chuỗi (`extra.T4c`, chỉ khi E6a, thế giới P). Bản ghi thêm `extra.kenh_co` (kênh có cờ của P kèm F_I, cho dấu vết E5 phía bộ đánh giá) và `extra.G_N` (cạnh cha–con khác chủ khi cả hai span thuộc N, cho cờ M5); cả hai không chứa nhãn. Toàn bộ test: 214 qua, 5 đỏ (đều là runner, chưa viết).
- Bước 5 (runner, pha 2, adapter): `src/m1/runner.py` (`ap_dinh_chinh` áp Đ16 lên bản sao trong bộ nhớ, ghi Đ3, Đ7 là đính chính chỉ chữ không áp; `sinh_cau_hinh` cho T1 1, T4 9, T4b 1, K 16, K-b 2, T6, T9, T11, T12 mỗi bước 1, T10 0, KB 4, T13 = bỏ từng thành phần đang bật + 7 đối chứng; mỗi cấu hình có `ma_noi_dung` để chạy một lần cấu hình trùng giữa các bước; tham số E4 lấy từ `hop-dong.json` vì `ma-tran-thu.json` thiếu q_hi, q_lo; `tham_so_E3` mặc định cách khớp (a), `tham_so_E5` cách đọc C′; `pha1` chặn chuỗi cấm ở mức giá trị (CĐ12), ghi `ban-ghi.jsonl` JSON chuẩn hóa không NaN, `pha1.json` có sha256, `thoi-gian.json` không băm), `src/m1_danh_gia/pha2.py` (kiểm hash, ghép nhãn, RR, Hit@1, hạng kỳ vọng, cờ M5 từ `extra.G_N`, ba thế giới, WORLD_DEPENDENT; `ket_cuc_cap` áp luật C trong ba thế giới, tự đếm M5 cho cặp E5 và UV-6 cho cặp E3; `dem_moc_gia`), `src/m1/adapter.py` (RE2-TT qua `selector.chon_ca`; Nezha-OB qua `nezha.chon_ca`, `doc_cua_so`; F theo từng file trên toàn file; r theo `hop-dong.json`; chuỗi vào Drain và severity thô của Nezha-OB theo CĐ4.1; hồ sơ nguồn theo CĐ5). Đối chiếu số đếm không nhãn KS-16 (`ks16/dem-khong-nhan.json#/cases/*/metric_rows`): hậu tố metric RE2-TT đúng 8 mục của `hop-dong.json` dòng 55, kênh Nezha-OB đúng 21 mục dòng 61, nên hồ sơ nguồn không làm bản ghi nào ERROR vì lớp lạ.
- Sửa chuỗi trong bước 5: (1) cột metric không khai nguồn trước đây lặng lẽ dùng `metrics.time`, trái Đ19 điểm 3; nay không chấm và ghi `diagnostics.cot_metric_chua_khai_nguon`. (2) Giá trị metric không hữu hạn bị bỏ ngay khi gom mẫu (đặc tả v1 dòng 110), vì khởi phát E9 và T4c dùng danh sách chưa lọc. (3) Bản ghi thêm `extra.don_vi_phan_vi` (chi tiết đơn vị phân vị, CĐ13). Phát hiện khi viết adapter: bản đầu đưa đường dẫn tệp metric của Nezha-OB vào `params.nguon_metric`, trái luật cứng 6; đã đổi sang mã trung tính `metric:<dịch vụ>`, `metric:front_service` (tệp front và tệp pod frontend phải khác mã, nếu không mốc của nguồn này đè nguồn kia). Runner chặn thêm mọi đường dẫn tệp, tên thư mục ca và tên file phút của Nezha-OB.
- Test thêm: `test_runner.py` 8/8 (đính chính, số cấu hình, ngân sách 1.144 ≤ 1.300, hai pha hash ổn định, chặn rò, tham số E4 khớp hợp đồng, T13, pha 2 với M5 và luật C ba thế giới); `test_adapter.py` 3/3 (bộ dữ liệu tổng hợp RE2-TT parquet và Nezha-OB CSV đúng schema của `src/p3`, sinh trong thư mục tạm; hash sai bị từ chối); `test_k09_chuoi.py` thêm MET1 (đáp án tự lập). Toàn bộ: 226/226 qua.
- Bước 6 (tất định): thêm cơ chế xáo hàng vào `tests/conftest.py` (`M1_XAO=<seed>` xáo mọi danh sách đầu vào mà thứ tự không mang nghĩa, ở mọi tầng gọi; metric của chuỗi chỉ xáo khi mọi nguồn dùng `metrics.time`) và script `results/T-044/scripts/tat_dinh.py` (104 bản ghi: trace S1–S7 và ca metric với 13 cấu hình gồm E1-CP, E3, E6b, E9, T12, nhánh z, cách đọc A; băm JSON chuẩn hóa; cache cổng mới mỗi lượt). Lượt xáo đầu tiên đỏ 6 test (dựng lại và lưu ở `runs/tat-dinh-000-truoc-sua/`): `e2.gan_canh` trả danh sách theo thứ tự đầu vào; `e5.phan_loai` duyệt kênh giải thích theo thứ tự đầu vào nên thứ tự mục `inherited_by` đổi (F_I không đổi, hash pha 1 đổi). Sửa: sắp cạnh theo (bên gọi, bên được gọi), sắp kênh theo mã. Lượt chạy script đầu tiên dừng vì ca metric thiếu lớp `latency-90` trong hồ sơ của bộ sinh S (chỉ có cpu); đổi sang hồ sơ RE2-TT của `hop-dong.json`; đầu ra lỗi của lượt đó bị ghi đè, chỉ còn ghi lại ở đây. Kết quả `runs/tat-dinh-001/tong-hop.json`: 104 bản ghi giống hệt qua 4 thứ tự × PYTHONHASHSEED 0, 1, 2 (0 sha256 lệch); 226 phép kiểm qua và giống hệt ở cả 12 biến thể. Tổng thời gian khoảng 90 giây.
- Bước 7 (đột biến): script `results/T-044/scripts/dot_bien.py` chép `src/`, `results/T-043` (trừ runs), tests và fixture của T-044 vào thư mục tạm; mỗi đột biến thay đúng một chuỗi (kiểm xuất hiện đúng một lần), chạy toàn bộ test; không sửa repo. Lượt `runs/dot-bien-001`: 20 đột biến, đối chứng không đột biến xanh, 18 bị bắt, **2 sống sót**: D02 (bỏ cắt con về cha trong `span.chuan_bi`) vì fixture 4, 5 chỉ gọi `cat_con`, `doc_quyen_U` trực tiếp, không đi qua đường chuỗi dùng thật; D10 (mặc định cách đọc nhóm vòng của `e5.phan_loai` thành A) vì test nhóm vòng luôn truyền cách đọc. Vá bằng test, không thêm đáp án mới: fixture 2–5 đi qua `chuan_bi` (U, CP, đếm con vượt biên); SCC1–SCC4 gọi không truyền cách đọc phải cho đáp án C′; chuỗi thiếu `tham_so_E5` phải gọi E5 với 'co_vong' (thêm D21 cho chỗ này). Lượt `runs/dot-bien-002`: 21 đột biến, đối chứng xanh 235/235, **21/21 bị bắt** (D19 bỏ thứ tự chuẩn của E5 chỉ lộ khi xáo hàng nên chạy với M1_XAO=1). Gồm sáu ví dụ của SPEC: đảo lớp lan (D01), bỏ cắt con E1 (D02), đổi khóa hòa (D03), bỏ duyệt list ở bộ kiểm trường cấm (D04), đổi δ luật C (D05), rò nhãn vào pha 1 (D06 mã mờ vào params, D07 import bộ đánh giá, D08 trỏ file nhãn). Mỗi lượt khoảng 85 giây.
- Bước 8 (đính chính): ghi `results/T-044/dinh-chinh-cai-dat.md` Phần II. Không fixture hay đáp án nào của T-043 lệch với code (97/97 qua, không sửa đáp án), nên không có đáp án đặc tả cần đính chính. Phần II gồm: A. 20 cách hiểu ở chỗ đặc tả không nói (PII-01…PII-20, ví dụ cổng p < α chặt, E9 tắt trên cạnh E2, khởi phát của kênh E2-VC, vùng E7 rỗng khi ứng viên không có cờ, M5 "đứng trước hẳn" trên khối, giá trị metric không hữu hạn, đích C-d3, mẫu số C-e khi bản ghi lỗi, danh sách T13 và C-e, nền của các bước sau K-b, cờ trái chiều trong luật khối, cột metric không khai nguồn, quy ước adapter), **chờ Minh quyết**; B. quy ước biểu diễn; C. các sửa đã làm trong phiên; D. giới hạn và phần chưa kiểm. Soạn `results/T-044/de-xuat-why.md`: ba đề xuất WHY (đường xử lý log của E3; nhóm vòng C′; ngưỡng Drain 0,4), chưa ghi `docs/WHY.md` vì ngoài phạm vi ghi. Kiểm lại trích dẫn: KS-16 pha 2 dòng 160 dùng `<`; `dinh-nghia-pha2.json` dòng 44 ghi "p < 0,01"; `results/T-016/dung-logts-tracets.md` dòng 60 và bảng dòng 44–53; `RouteServiceImpl.java` dòng 84.

### Kết thúc phiên — giai đoạn 2, phiên 1 (29/10/2026; Claude; cloud, branch `claude/sweet-hawking-dy078d`; người làm)

**1. Đã làm gì.** Bước 0–9 của SPEC, không dừng giữa chừng (không gặp trường hợp dừng bắt buộc: không có đáp án lệch code, không cần ghi ngoài phạm vi, không cần gói ngoài danh sách ghim, không dùng subagent):
- bước 0–2: kiểm hash T-043 (PASS qua script), môi trường, chép U1–U6, H1–H6;
- bước 3: khung test và đáp án tự lập, thấy đỏ 206/208;
- bước 4: cài 11 khối `src/m1`, `src/m1_danh_gia`; bổ sung T4c (thiếu ở bước 3);
- bước 5: runner hai pha, pha 2, adapter RE2-TT và Nezha-OB;
- bước 6: tất định PASS (sau khi chuẩn hóa thứ tự đầu ra của E2, E5);
- bước 7: đột biến 21/21 (sau khi vá hai lỗ hổng test);
- bước 8: Phần II của `dinh-chinh-cai-dat.md`; bản nháp WHY;
- bước 9: `bao-cao.md`, `bang-phep-kiem.json`, lượt xác nhận cuối, `manifest.json`.

**2. File đã thay đổi trong giai đoạn 2** (commit từ c6a29315 tới commit chứa mục này):
- mới: `src/m1/` (17 tệp), `src/m1_danh_gia/` (12 tệp), `results/T-044/` (đáp án, tests, scripts, runs, báo cáo, bảng phép kiểm, đính chính, đề xuất WHY, requirements, freeze, manifest);
- sửa theo các mục Minh duyệt đầu giai đoạn 2: `tasks/T-044-cai-dat-m1/SPEC.md`, `tasks/T-045-chay-khoi-k-dev/SPEC.md`;
- `tasks/T-044-cai-dat-m1/LOG.md` (nối thêm); dòng T-044 trong `docs/STATE.md`.
- Không sửa `src/p3`, `results/T-043`, `requirements.txt` gốc, DECISIONS, WHY, MRP, KE-HOACH, task cũ.

**3. Kiểm đã chạy và kết quả** (số lấy từ file):
- 235/235 phép kiểm qua (`results/T-044/bang-phep-kiem.json#/tong`); 97/97 phép T-043 trong phạm vi (`#/T043/qua_trong_pham_vi`), 12 phép D13 loại theo ngoại lệ đã duyệt.
- Tất định: `results/T-044/runs/tat-dinh-002/tong-hop.json#/ket_luan` PASS (104 bản ghi, 4 thứ tự × 3 hash seed; 235 phép giống hệt ở 12 biến thể).
- Đột biến: `results/T-044/runs/dot-bien-002/tong-hop.json#/so_bi_bat` = 21/21; đối chứng xanh.
- Hash T-043: `results/T-044/runs/kiem-hash-t043-002/stdout.txt` PASS 69/69, 10/10. Manifest T-044: `tao_manifest.py --kiem` PASS 218/218.

**4. Điều chưa chắc hoặc cần Minh quyết.**
- **Task đã đạt** (trong phạm vi fixture): code làm đúng đặc tả trên mọi ca giả có đáp án; test có sức bắt lỗi với 21 đột biến; nhãn không lọt (kiểm tĩnh, fixture 74, CĐ12); tất định trên ca giả.
- **Câu hỏi nguồn trả lời tới đâu:** A1–A4 trả lời trong phạm vi fixture. A5: không chỗ sai; 20 chỗ đặc tả không nói, người làm đã chọn cách hiểu. Task không trả lời câu hỏi hiệu quả nào (RQ3b–d) và không kiểm hành vi trên dữ liệu thật; MRP P7 "kiểm đầu vào, trung gian, hành vi trên dev" mới đạt phần code và ca giả, phần dev thuộc T-045.
- **Cần Minh quyết:**
  1. 20 cách hiểu ở `results/T-044/dinh-chinh-cai-dat.md` Phần II mục A (PII-01…PII-20). Theo tiêu chí 8, task ở trạng thái "chờ Minh" tới khi quyết. Đề xuất: giữ cách đã cài.
  2. Ghi dòng DECISIONS cho các duyệt đầu giai đoạn 2 (đề xuất nguyên văn ở dưới).
  3. Ba đề xuất WHY ở `results/T-044/de-xuat-why.md` (E3, nhóm vòng C′, ngưỡng Drain); ghi vào `docs/WHY.md` cần duyệt riêng.
  4. Chuyển prompt phản biện dưới đây cho Codex và chọn phạm vi ghi của lượt phản biện.
  5. Dòng "Git remote … đã push tới `bc686d80`" trong `docs/STATE.md` đã cũ (branch này đã push tới commit chứa mục này); dòng đó ngoài quyền ghi của T-044. Đề xuất sửa khi Minh duyệt merge.
- **Bất đồng còn lại:** chưa có lượt phản biện kết quả nào.
- **Thiếu bằng chứng:** biên p = α không có fixture; khoảng tin cậy bootstrap chưa nằm trong `luat_c`; adapter chưa chạy trên dữ liệu dev; C-g, C-c chưa nối bản ghi P3 thật; cạnh tĩnh chưa đọc T-038, T-039; thời gian, RAM trên ca thật. Đáp án tự lập (73 mục) chưa qua phản biện; nếu đáp án nào sai thì code đang khớp cùng cách hiểu sai.
- **Quyết định bị ảnh hưởng:** T-045 bắt đầu khi T-044 được nghiệm thu (STATE dòng T-045). Cách khớp E3 chốt ở D17 của T-045.

**Đề xuất dòng DECISIONS (chưa ghi; chờ Minh duyệt):**
> | Q-213 | 29/10/2026 | “duyệt toàn bộ các đề xuất bên trên của bạn, nếu không còn vướng mắc gì thì hãy tiếp tục t-044 giúp tôi” | Duyệt 11 mục đề xuất của T-044 phiên 1 (R1–R14, D1–D5): script kiểm hash T-043 trên bản clone và sửa SPEC T-044 dòng 44, 86, 118; E1-CP là chế độ của E1, chỉ kiểm bằng fixture, không vào ma trận dev; UV-6 đếm gộp theo Hit@1 = 1; nhóm vòng E5 theo cách đọc C′, cách đọc A chỉ chẩn đoán (D5 của T-045); đường xử lý log của E3 (chuỗi vào Drain theo quy tắc chung, một Drain chung, ba cách khớp mặc định (a), bỏ che chuỗi trong ngoặc — đổi thiết kế, che UUID → IP → HEX → NUM, giữ ngưỡng 0,4); `params.ho_so_nguon`, `params.tham_so_E3`, `params.tham_so_E5`; mở rộng đáp án tự lập N1; ghi đính chính Phần I vào `results/T-044/dinh-chinh-cai-dat.md`; sửa SPEC T-045 theo D1–D5; xóa ba thư mục ngoài repo. Nguồn: chat 29/10/2026. |

**Bước tiếp theo chính xác.**
- Minh: quyết bốn mục trên; chuyển prompt dưới đây cho Codex.
- Khi có `tasks/T-044-cai-dat-m1/REVIEW.md`: mở phiên mới của người làm, đọc AGENTS, STATE, SPEC, mục này của LOG; tự soát đầu ra gốc trước khi mở kết luận phản biện (AGENTS mục 5 bước 7); chạy lại `cd results/T-044/tests && python -B -m pytest -q -p no:cacheprovider` và `python -B results/T-044/scripts/tao_manifest.py --kiem` để chắc đầu ra không đổi.
- Sửa code sau phản biện thì chạy lại `scripts/tat_dinh.py`, lưới pytest của bước 6, `scripts/dot_bien.py` (lượt mới), rồi `tao_manifest.py --tao`.

**Lệnh cuối đã chạy:** `$HOME/m1env/bin/python -B results/T-044/scripts/tao_manifest.py --kiem` (PASS 218/218), rồi push branch.

**Prompt phản biện cho Codex** (Prompt chung + khối "Soát kết quả" + khối G3 của `docs/review-prompt.md`, chép nguyên văn, chỉ điền thông tin trung tính):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-044 — cài chuỗi M1 và kiểm đặc tả; tasks/T-044-cai-dat-m1/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6 (M1); chuẩn bị G3.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (theo SPEC).
- Tài liệu gốc: tasks/T-044-cai-dat-m1/SPEC.md; tasks/T-044-cai-dat-m1/LOG.md; tasks/T-045-chay-khoi-k-dev/SPEC.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md (Phụ lục B–D); results/T-043/dac-ta-phuong-phap-v1.md, hop-dong.json, ma-tran-thu.json, dinh-nghia-pha2.json, bang-chuyen-giao.json, fixture-dac-ta.json, fixture/fixture-bo-sung.json, dinh-chinh-phien8.md, dinh-chinh-phien9.md, dinh-chinh-phien10.md; results/T-044/dinh-chinh-cai-dat.md; git diff 6b2f6ac6..1487416c trên branch claude/sweet-hawking-dy078d (LOG và STATE ở commit kế tiếp trên cùng branch).
- Phản biện và phản hồi trước: không có bản phản biện dạng file cho T-044. Lượt rà SPEC của Codex diễn ra trong chat ngày 29/10/2026 (SPEC T-044 dòng 3).
- Code và kết quả liên quan: branch claude/sweet-hawking-dy078d, commit 1487416c; src/m1/, src/m1_danh_gia/; results/T-044/ (bao-cao.md, bang-phep-kiem.json, dinh-chinh-cai-dat.md, de-xuat-why.md, fixture/, tests/, scripts/, runs/); manifest results/T-044/manifest.json, kiểm bằng `py -3 -B results/T-044/scripts/tao_manifest.py --kiem`; môi trường results/T-044/requirements-m1.txt và results/T-044/freeze-m1.txt (Python 3.12); chạy test: `cd results/T-044/tests` rồi `py -3 -B -m pytest -q -p no:cacheprovider`; các lệnh khác ở results/T-044/bao-cao.md mục 11.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền khi chuyển prompt: chỉ trả lời trong chat, hoặc ghi tasks/T-044-cai-dat-m1/REVIEW.md (chưa có) theo tasks/_MAU/REVIEW.md>.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

# Phản biện T-016

- **Người phản biện:** Codex — **Ngày:** 04/10/2026.
- **Commit/diff đã đọc:** task chưa commit, không có commit gốc để so. Đã đọc file hiện tại, `git status --short`, diff `docs/STATE.md`, diff bản sửa TORAI với code gốc. Các thay đổi của task khác đã có trước phiên phản biện.
- **Đã đọc:** AGENTS; SPEC và toàn LOG T-016; mẫu REVIEW và review-prompt; toàn bộ tài liệu, CSV, JSON, lock và 25 script trong `results/T-016/`; các đầu ra trong `cham/`, `runs/`, gồm các gói nén; hai file `src/torai/`; STATE, MRP, WHY, DECISIONS, LESSONS; hai nguồn DT18/cô; phần TORAI/RCD liên quan trong T-001, T-005, T-006 và cách dựng EC2 T-007.
- **Nguồn ngoài repo:** code RCAEval đúng revision của SPEC; RCD gốc trong `D:/RCA-ext/work/T-016/src/rcd`; các thư mục lượt chạy, dữ liệu TT dev và kết quả EC2 đã giải nén; môi trường công cụ. Đã kết nối EC2 để đọc `~/rca/T-016/`, log dựng/chạy, revision và đối chiếu hai gói kết quả với bản trong repo. Đã đọc [bài TORAI v1](https://arxiv.org/html/2604.13522v1), [bài RCD](https://proceedings.neurips.cc/paper_files/paper/2022/file/c9fcd02e6445c7dfbad6986abee53d0d-Paper-Conference.pdf) và [phụ lục RCD](https://proceedings.neurips.cc/paper_files/paper/2022/file/c9fcd02e6445c7dfbad6986abee53d0d-Supplemental-Conference.pdf).
- **Cách kiểm:** chỉ đọc và tính lại từ đầu ra đã lưu. Không chạy thực nghiệm mới, không mở `data/locked/`, không đọc repo lưu trữ. Hai kiểm tra bổ trợ bằng subagent chỉ đọc; bằng chứng của các điểm dưới đã được đối chiếu lại.

## Kết luận chung

Không thấy lỗi CHẶN làm mất tính dùng được của các lượt chạy đã lưu. Có sáu điểm KHÔNG CHẶN: hai lỗi tính/đối chiếu ở S8–S9, ba lỗi diễn giải kỹ thuật và một đường ghi ngoài phạm vi EC2. Cần sửa các điểm này trước khi dùng hồ sơ và nháp tài liệu chung làm căn cứ khoa học; không cần chạy lại TORAI/RCD để sửa chúng.

## Các điểm

### R1. Tỷ lệ khớp `logts` bỏ qua cột dư — KHÔNG CHẶN

- **Ở đâu:** S9; `results/T-016/scripts/dung_logts.py:111–140,165`; `results/T-016/dung-logts-tracets.md:43–55`; `tasks/T-016-ho-so-torai/SPEC.md:95`.
- **Sai gì:** SPEC yêu cầu tính trên toàn bảng, kể cả cột không ghép được. Script lại đặt mẫu số bằng `mau.size`. Cột dư bên dựng, kể cả service chỉ có bên dựng, không bị tính là sai. Đây là lỗi số đo đã xảy ra, không phải việc OPEN của P4.
- **Bằng chứng:** đọc `so_hungarian`: dòng 117 chỉ đếm ô bảng mẫu; dòng 124–126 bỏ qua service không có cột mẫu. Tính lại bằng Python chỉ đọc `runs/s9/so-sanh-lan2.json`: giữ nguyên phép ghép và số ô trùng, mẫu số bằng 96 dòng × tổng `max(cot_mau, cot_dung)` trong từng service. B ngưỡng 0,4: **4 684/9 984 = 46,915%**, thay vì 66,8%. B ngưỡng 0,7: **4 996/134 688 = 3,709%**, thay vì 71,3%.
- **Hậu quả và giới hạn:** tỷ lệ hiện tại làm bản tách quá nhiều mẫu trông khớp hơn. Kết luận không đạt 95% vẫn đúng. Có thể định nghĩa một chỉ số chỉ đo độ phủ bảng mẫu; các cột dư cũng đã được báo riêng. Nhưng đó không phải chỉ số toàn bảng mà SPEC và docstring đã khai báo. Ghi “cận trên” do ghép tối ưu không thay thế việc tính cột không ghép được.
- **Đề xuất sửa:** sửa mẫu số và bảng S9 theo SPEC, tính lại từ kết quả đã lưu. Nếu giữ chỉ số cũ thì phải gọi đúng là độ phủ bảng mẫu và ghi rõ sai khác với SPEC; không dùng nó làm tỷ lệ khớp toàn bảng.

### R2. Phép soi placebo và mốc may rủi khác đơn vị chấm — KHÔNG CHẶN

- **Ở đâu:** S8; `results/T-016/scripts/soi_placebo.py:11–28`; `results/T-016/kiem-khong-nhan.md:15,24`; `runs/s8-soi-placebo.txt`.
- **Sai gì:** điểm chính gộp `-db` về service và bỏ trùng theo `main.py`/T-006. Phép soi chỉ tách tiền tố trước `_`. Vì vậy nó bỏ qua các lần một database được chấm đúng cho service gốc. Mốc may rủi `1/15` cũng không áp dụng cho điểm SS sau gộp.
- **Bằng chứng:** đọc trực tiếp bốn gói `runs/khoi/s8-*-placebo.tar.gz` trong bộ nhớ, ánh xạ và bỏ trùng đúng cách chấm. SS gốc: hạng TB gốc thật/gốc khác **4,433/4,544**, thay vì 4,71/4,76. SS sửa: **4,422/4,533**, thay vì 4,87/4,88. Top-1 tương ứng **0,122/0,136** ở cả hai bản, thay vì số thô 0,100/0,114. Nếu xếp đều service sau gộp, mốc SS gốc là **1/11**, Avg@5 **3/11**. Nếu hoán vị đều 15 ứng viên thô rồi gộp, bốn trong năm service gốc có database: kỳ vọng top-1 trung bình là **(4×2+1)/(5×15) = 0,120**, gần số quan sát 0,122. OB cũng có số ứng viên thay đổi giữa ca: mốc trung bình là **0,07446/0,22338**, thay vì 0,071/0,214.
- **Hậu quả và giới hạn:** độ vượt may rủi và các số dùng để giải thích SS bị sai đơn vị. Sau sửa, gốc thật vẫn không đứng cao hơn rõ so với các gốc khác; chưa có bằng chứng mới cho rò nhãn. Không quy lỗi này thành kết quả phương pháp bị rò.
- **Đề xuất sửa:** dùng cùng ánh xạ service cho phép soi và điểm chính. Ghi rõ mô hình may rủi; cập nhật số và diễn giải từ thứ hạng đã lưu. Không cần lượt chạy mới.

### R3. Sửa hai lỗi chưa đủ để quy hạn chế cho TORAI theo bài — KHÔNG CHẶN

- **Ở đâu:** S13–S14; `results/T-016/giam-mau-hai-lan.md:110–116`; nháp W1 trong `de-xuat-tai-lieu-chung.md:15–21`.
- **Sai gì:** câu “nếu dùng bản sửa, hạn chế đó mới thuộc về phương pháp” và “chỉ làm phương pháp đúng mô tả” đi xa hơn bằng chứng. A+B đưa metric trở lại và bỏ dòng giả. Chúng chưa làm bản cài tương đương TORAI trong bài.
- **Bằng chứng:** chính `ho-so-torai.md:150–153` ghi C4–C7: gán cụm cứng, bỏ trace khỏi RCD, vectơ/trọng số nguồn khác bài, nhánh dự phòng. Các phần này còn nguyên ở bản sửa. [Bài TORAI §3.3–3.4 và Hình 3](https://arxiv.org/html/2604.13522v1#S3.SS3) mô tả gán mềm và phân tích chuỗi đa nguồn. `giam-mau-hai-lan.md:122` còn ghi ghép theo vị trí là giả định, chưa xác nhận ý tác giả.
- **Hậu quả và giới hạn:** P4 có thể quy một hạn chế của bản cài cho TORAI trong bài mà chưa loại sai khác cài đặt. Đã xét câu W1 “ở bước này”, phần ghi B chưa kiểm và đoạn thừa nhận C7: chúng giới hạn việc sửa đầu vào, nhưng không cứu được hai câu quy kết rộng trên. Finding không phản đối đề xuất dùng A+B và không yêu cầu cài thêm thành phần trong T-016.
- **Đề xuất sửa:** gọi A+B là “bản cài RCAEval đã sửa hai lỗi”. Kết luận P4 giới hạn vào bản cài đó; việc quy cho TORAI theo bài vẫn OPEN ở các khác biệt còn lại.

### R4. Nháp LESSONS biến suy đoán về code công bố thành sự thật — KHÔNG CHẶN

- **Ở đâu:** S14; `results/T-016/de-xuat-tai-lieu-chung.md:48`, nháp L1/SL34.
- **Sai gì:** khẳng định số khớp “vì số công bố được tạo bằng chính code có lỗi”. Task không có bằng chứng về lượt chạy/code thực sự tạo bảng công bố.
- **Bằng chứng:** `giam-mau-hai-lan.md` §4(b) chỉ viết “nhiều khả năng” và vẫn giữ khả năng tác giả dùng code khác. §5 viết số công bố **không phân biệt được** bản gốc với bản sửa: cả hai đạt ngưỡng khớp. Chính nhánh dự phòng cũng giải thích vì sao hai bản gần nhau mà không cần giả định cùng nguồn code.
- **Hậu quả và giới hạn:** nếu nhập nguyên văn vào LESSONS, một CANDIDATE trở thành FACT và làm sai căn cứ của báo cáo sau. Đây là lỗi của nháp; chưa có bằng chứng câu đó đã được ghi vào tài liệu chung.
- **Đề xuất sửa:** thay bằng “số vẫn khớp dù bản cài đang kiểm có lỗi; chưa xác minh code/lượt chạy tạo số công bố”. Giữ bài học khớp điểm không chứng minh chạy đúng từng thành phần.

### R5. C10 mô tả thiếu trường hợp khác biệt trong cách xếp p-value — KHÔNG CHẶN

- **Ở đâu:** S2/S13; `results/T-016/ho-so-torai.md:156`, dòng C10.
- **Sai gì:** mô tả khác biệt giữa so danh sách theo thứ tự từ điển và so `max(P)` bằng trường hợp hòa p-value đầu. Hai cách có thể khác ngay khi p-value đầu không bằng nhau.
- **Bằng chứng:** [phụ lục RCD, Thuật toán 3](https://proceedings.neurips.cc/paper_files/paper/2022/file/c9fcd02e6445c7dfbad6986abee53d0d-Supplemental-Conference.pdf), đối chiếu `_order_neighbors` của RCD gốc và RCAEval `rcd.py:211–222`. Tính trực tiếp từ `runs/s12-tinh-tay-goc.json`, đường JSON `/tinh_tay/cac_cum/1/pc/9`, α=0,91: `cartservice_13` có p đầu **0,517733**, max **0,583480**; `shippingservice_16` có p đầu **0,569831**, max **0,569831**. So danh sách chọn nút thứ hai là lớn nhất; so max chọn nút thứ nhất.
- **Hậu quả và giới hạn:** hồ sơ thu hẹp sai phạm vi khác biệt bài/code. Đây là phản ví dụ cho mô tả, chưa chứng minh thứ hạng task sai: các nút này có thể đã được nhận ở vòng α trước. Kiểm các nhóm hàng xóm mới trong hai ví dụ tính tay chưa thấy khác biệt tại lúc xếp.
- **Đề xuất sửa:** ghi “khác khi thứ tự theo danh sách p-value khác thứ tự theo max của danh sách; tác động tới đầu ra chưa đo”. Không sửa thuật toán hoặc yêu cầu thí nghiệm mới.

### R6. Dựng Python EC2 đã ghi ngoài phạm vi SPEC — KHÔNG CHẶN

- **Ở đâu:** S11/E0; `results/T-016/scripts/e0_dung_ec2.sh:8,15`; `moi-truong.md` §3; phạm vi EC2 trong SPEC.
- **Sai gì:** chỉ đặt `UV_PYTHON_INSTALL_DIR` không giữ mọi đầu ra của `uv python install` trong `~/rca/T-016/`. Bước dựng còn tạo liên kết thực thi trong thư mục người dùng chung.
- **Bằng chứng:** SSH chỉ đọc `ls -ld --full-time ~/.local/bin ~/.local/bin/python3.8` xác nhận liên kết `/home/ubuntu/.local/bin/python3.8` trỏ tới Python trong T-016, tạo lúc **01:53:37 UTC ngày 04/10**, đúng bước E0. `~/rca/T-016/runs/e0.log` cùng thời điểm cảnh báo `/home/ubuntu/.local/bin` chưa có trong PATH. Đường này nằm ngoài phạm vi `~/rca/T-016/`.
- **Hậu quả và giới hạn:** câu “mọi thứ ghi trong T-016” không đúng; máy dùng chung có thêm một đường tìm Python ngoài task. Chưa thấy ảnh hưởng tới điểm: các lượt chạy gọi trực tiếp Python của môi trường T-016. Không kết luận có thêm file ngoài phạm vi khi chưa có bằng chứng.
- **Đề xuất sửa:** ghi nhận đường đã tạo và trình Minh cách xử lý liên kết đó. Khi sửa script dựng, đặt cả thư mục liên kết thực thi trong T-016, hoặc dùng tùy chọn không tạo liên kết. Reviewer không xóa hay sửa gì trên EC2.

## Điều đã kiểm và thấy đúng

- **Tiêu chí xong:** đủ các đầu ra và dòng STATE yêu cầu. Tiêu chí 3, 5–8, 10–12 có đầu ra phù hợp; các phép so S3 và S12 có bằng chứng đã lưu. Các phần hồ sơ/diễn giải của tiêu chí 1–2 và số đối chiếu của tiêu chí 4, 9 cần sửa theo R1–R5. Không biến việc chưa tái lập đủ 90 ca TT hoặc chưa đo biến thể C4–C11 thành lỗi: SPEC đã giới hạn và nêu hệ quả.
- **Số chính:** tính lại **7 611 thứ hạng** từ gói kết quả, theo ánh xạ service của cách chấm chính; AC@1, AC@3, Avg@5 khớp các tổng hợp đã kiểm, sai lệch không quá 1e-12. `ca-da-chay.csv` có 7 612 dòng, gồm một dòng script tính tay; khớp các lượt lưu, không thiếu/thừa khóa ca–khối–seed. Hai gói EC2 trong repo khớp hash bản trên EC2. Không chép hash vào phần lập luận.
- **Code và tính tay:** bản sửa chỉ đổi A/B và thêm cờ điều khiển. Ví dụ tính tay khớp 78 lần PC ở bản gốc và 101 lần ở bản sửa; sai số p-value lớn nhất như báo cáo. Code lõi tính lại được viết độc lập; dùng GMM của sklearn đúng ngoại lệ SPEC. Khớp code không tự chứng minh khớp toàn phương pháp trong bài (R3).
- **Đường nhãn:** không thấy service gốc, loại lỗi, tên ca hoặc đường dẫn ca được truyền vào lõi xếp hạng. Harness dùng chúng để định danh kết quả; `sli=None`. Mốc tiêm được dùng trong chế độ biết trước thời điểm, đã ghi rõ. `tracets_lat` dùng dữ liệu cả đoạn lỗi được nhận diện là vấn đề khi chuyển sang tự phát hiện; chưa tuyên bố detector hợp lệ từ các lượt này.
- **Dev/test:** 30 ca TT được đối chiếu với ca dev bằng mốc và giá trị metric; các gói chạy chỉ chứa các ca được phép. Không thấy mở dữ liệu test trong đường thực thi đã soát. Không dùng kết quả 30 ca để nhận đã tái lập Bảng 4. Bộ dữ liệu và giao thức P3 vẫn chờ tổng hợp G1; TT topology và nhãn chưa đủ để quy riêng tác động vị trí hoặc chấm vùng ảnh hưởng RQ3c.
- **Đồ thị và đối chứng:** TORAI/RCD học quan hệ quanh F-node, không dùng đồ thị gọi để phát hiện. RCD không phải phép bỏ riêng gom cụm của TORAI: tín hiệu, giảm mẫu, đơn vị xếp và nhánh dự phòng cùng khác. Hồ sơ nêu đúng rằng chênh lệch không quy riêng cho một thành phần. Chưa có nhánh không đồ thị của RQ3 trong task này, nên không suy kết luận về giá trị cấu trúc từ các điểm đã chạy.
- **DT18/cô và quyết định:** T-016 phục vụ hiểu sâu phương pháp. Danh sách gọn do Minh quyết Q-37/Q-38, có thống kê/luật, nhân quả, trace/PageRank, đa nguồn; GDN ở nhóm phát hiện. Không coi ba ví dụ của cô là ba baseline bắt buộc. Các cơ chế P6 là ứng viên sau P4; không thấy T-016 chốt cơ chế đó trước thực nghiệm. W1/W2 và cấu hình dựng cho dataset khác đang là đề xuất, chưa phải quyết định P3.
- **WHY/LESSONS:** đã đọc cả lập luận, không chỉ kiểm có đề mục. SPEC và hồ sơ có lý do cho A/B, seed, phép ghép S9 và phạm vi dữ liệu; nháp chưa được nhập WHY. Không đánh đồng đề xuất bản P3 với quyết định đã có hiệu lực. R3/R4 là chỗ diễn giải vượt bằng chứng; các số chạy chính, tách cấu hình/ca và các giới hạn đã được giữ rõ.
- **Phạm vi phiên này:** chỉ tạo `tasks/T-016-ho-so-torai/REVIEW.md`; không ghi LOG, STATE hay file khác, không commit. Việc ghi ngoài phạm vi phát hiện ở R6 thuộc lượt E0 của người làm, không phải thao tác sửa của reviewer.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | **Đúng** | Tính lại từ `runs/s9/so-sanh-lan2.json`, mẫu số = 96 × Σ max(cột mẫu, cột dựng) theo service: B ngưỡng 0,4 = 4 684/9 984 = 46,915 %; B 0,7 = 4 996/134 688 = 3,709 %; mọi cấu hình đều ≤ 50,2 %. Script đặt mẫu số = `mau.size`, trái SPEC S9. Kết luận "không đạt 95 %" và hai nguyên nhân (mốc thời gian, cấu hình Drain) không đổi; bảng S9 và câu "tỉ lệ cận trên" phải sửa. Sửa tối thiểu: thêm cột "ô trùng / toàn bảng" vào script và bảng; giữ số cũ dưới tên "độ phủ bảng mẫu". Không cần chạy lại phương pháp. | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| R2 | **Đúng** | Tính lại với ánh xạ `split("_")[0].replace("-db","")` + bỏ trùng (như `cham.py`), từ thứ hạng đã lưu: SS gốc hạng TB gốc thật/khác 4,433/4,544, top-1 0,122/0,136; SS sửa 4,422/4,533; may rủi SS 1/11 = 0,0909, Avg@5 0,2727; OB 0,07446/0,22338. Trùng số reviewer. Kết luận "không thấy rò" giữ nguyên (gốc thật không đứng cao hơn gốc khác); số trong `kiem-khong-nhan.md` mục 6, `runs/s8-soi-placebo.txt`, báo cáo C và LOG phải sửa; `soi_placebo.py` phải dùng cùng ánh xạ. | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| R3 | **Đúng** | Bản sửa chỉ đổi A, B; C4–C7 (gán cứng, bỏ trace trong RCD, trọng số nguồn, nhánh dự phòng) còn nguyên, và (B) là cách hiểu chưa kiểm. Hai câu "hạn chế đó mới thuộc về phương pháp" (`giam-mau-hai-lan.md` mục 6) và "chạy đúng mô tả của bài" (W1, mục 7) vượt bằng chứng. Sửa theo đề xuất reviewer: gọi là "bản cài RCAEval đã sửa hai lỗi"; quy kết cho TORAI theo bài để OPEN ở các khác biệt còn lại. Không đổi đề xuất dùng A+B. | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| R4 | **Đúng** | `giam-mau-hai-lan.md` §4(b) chỉ nói "nhiều khả năng"; §5 cho thấy số công bố không phân biệt được hai bản, và nhánh dự phòng tự giải thích việc hai bản gần nhau. Nháp SL34 viết thành sự thật là sai mức chắc chắn. Sửa câu theo đề xuất reviewer. | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| R5 | **Đúng** | Kiểm trên `runs/s12-tinh-tay-goc.json`, cụm `{cartservice, shippingservice}`, lần PC thứ 9, α = 0,91: `cartservice_13` [0,5177; 0,5835; …], `shippingservice_16` [0,5698; …]; so danh sách → `shippingservice_16` lớn hơn, so max → `cartservice_13` lớn hơn. Mô tả C10 ("khác khi hai nút cùng p-value đầu") hẹp hơn thực tế. Sửa câu; tác động tới đầu ra vẫn "chưa đo". | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| R6 | **Đúng, phạm vi rộng hơn** | SSH chỉ đọc: E0 (`uv python install`) tạo mới **ba** đường ngoài `~/rca/T-016/`: thư mục `~/.local`, `~/.local/bin` (đều tạo 01:53:37 UTC, trước đó không tồn tại) và liên kết `~/.local/bin/python3.8` → Python trong T-016. Không thấy file nào khác ngoài `~/rca/` có thời điểm trong khoảng E0. Không ảnh hưởng điểm (mọi lượt gọi Python của env T-016 bằng đường tuyệt đối). Đây là vi phạm phạm vi ghi (Luật 0 mục 8). Đề xuất hoàn tác, chờ Minh duyệt: `rm ~/.local/bin/python3.8 && rmdir ~/.local/bin ~/.local` (chỉ chạy được khi hai thư mục rỗng; lúc kiểm chỉ chứa đúng liên kết này). Sửa script dựng: thêm `UV_PYTHON_BIN_DIR=$B/python/bin` hoặc `--no-bin`; sửa `moi-truong.md` mục 3 câu "mọi thứ ghi trong T-016". | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| N1 (tự tìm) | KHÔNG CHẶN | `quy-mo-tt.md` mục 4: lý do "pha 2 chỉ nhận ≤ 5 biến" sai — giá trị trung gian cho thấy mức cuối pha 1 còn tới 29 cột (8 383/9 636 cụm > 5). Lý do thật không lỗi `assert`: số dòng (40–80) > số biến. Sửa câu. | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| N2 (tự tìm) | KHÔNG CHẶN | Nháp WHY-18 "RCD ít nhất 5 seed" mâu thuẫn Q-40 (RCD OB cửa sổ 20: 1,56 giờ/seed; TT khoảng 74 phút/seed). Sửa thành "số seed tối đa vừa ngân sách Q-40, tối thiểu 1, ghi rõ". | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| N3 (tự tìm) | KHÔNG CHẶN | Nháp SL35 trùng QT17/SL17; nháp mục `data/README.md` không cần (dữ liệu nằm ngoài `data/`, lệnh dựng lại đã ở `moi-truong.md` mục 4). Đề xuất bỏ hai nháp này. | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |
| N4 (tự tìm) | KHÔNG CHẶN | `kiem-khong-nhan.md` mục 7: câu "chúng có 0 sau khi chuẩn hóa nếu cả đoạn lỗi cũng 0" (cột trace_err nhân 1e9) chưa được kiểm. Bỏ câu hoặc ghi "chưa kiểm". | Duyệt sửa (Minh, 04/10: "duyệt sửa đổi"); đã sửa, xem LOG phiên 2 |

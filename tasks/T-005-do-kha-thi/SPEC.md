# T-005 — Đo khả thi môi trường và thời gian chạy

- **Trạng thái:** đã duyệt (03/10/2026)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1 (chuẩn bị P3) — **Cổng:** G1

## Mục tiêu

Kiểm các phương pháp và bộ phát hiện đã chốt ở Q-37 và Q-38 trên laptop này (Windows 11, chỉ CPU, RAM 16 GB):
- có cài được không, có chạy được không;
- mỗi phương pháp chạy một ca mất bao lâu và tốn bao nhiêu RAM.

Kết quả dùng để:
- lập kế hoạch chạy tay một ca ở P1 và chạy trên nhiều ca ở P3;
- trả lời tiêu chí 3 của WHY-10 cho GDN ("chạy được trên CPU của laptop 16 GB").

Task này không trả lời câu hỏi khoa học nào và không chấm điểm phương pháp.

## Đầu vào

- `results/T-001/danh-sach-phuong-phap.md` mục 8 (danh sách đã chốt) và mục 9 (revision của code).
- Code chính thức ở đúng revision ở mục 9 của file trên: RCAEval `259ea41`, BARO `e35f4ec`, GDN `9853899`.
- **Dữ liệu để đo:**
  - Một ca có sẵn trong `data/rcaeval/`: ca có tổng kích thước `metrics.parquet` + `traces.parquet` lớn nhất, để thử tải nặng nhất.
  - Chọn theo kích thước file, không theo tên ca hay nhãn.
  - Không đụng `data/locked/`.
  - **Đây không phải là chọn dataset** (MRP §4, Q-31). Minh đồng ý dùng ca có sẵn chỉ để đo thời gian ngày 03/10/2026.
- **GDN:** học trên đoạn trước lúc tiêm của tối đa 5 ca có sẵn cùng hệ với ca đo, chọn theo kích thước file.
- **TORAI** cần chuỗi thời gian log/trace đã xử lý:
  - Tải `torai-data.zip` (91 MB) từ Figshare, article 31925976, và kiểm hash theo Figshare.
  - File zip chứa cả các ca đang khóa, nên **chỉ giải nén đúng ca dùng để đo**. Được đọc danh sách tên mục trong zip để tìm đúng ca, nhưng không giải nén và không đọc nội dung ca khác.
- Mốc tiêm (`inject_time.txt`) chỉ dùng để cắt cửa sổ cho phương pháp chạy ở chế độ "biết trước thời điểm" và để lấy đoạn bình thường cho GDN. Kết quả không được chấm, nên mốc này không vào bất kỳ đánh giá nào.

## Đầu ra

- `results/T-005/do-kha-thi.md`: mỗi phương pháp và bộ phát hiện một dòng, gồm:
  - môi trường;
  - cài được không;
  - chạy được không;
  - thời gian chạy (giây);
  - RAM đỉnh (MB);
  - lỗi gặp và cách xử lý;
  - kết luận cho P1/P3.

  Cuối file: đề xuất cho P3 nếu có phương pháp quá chậm, và lý do không đo cho từng mục không đo.
- `results/T-005/moi-truong.md`: hướng dẫn dựng lại ba môi trường trên máy khác, gồm phiên bản Python, lệnh cài, file vá, nguồn và hash của dữ liệu đã tải.
- `results/T-005/scripts/`: script đo và các bộ đọc dữ liệu tối thiểu dùng riêng cho việc đo.
- `results/T-005/runs/`: log của mọi lượt cài và chạy, kể cả lượt hỏng (luật cứng 10).

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-005/`
- `D:\RCA-ext\` (ngoài repo): bản clone code các phương pháp, ba môi trường Python, dữ liệu TORAI đã tải. Không chép code ngoài vào repo.
- Cài **Python 3.8.10 cho tài khoản người dùng**, bằng bộ cài chính thức của python.org. Minh duyệt cùng SPEC ngày 03/10/2026.

## Các bước

1. **Cài Python 3.8.10** cho tài khoản người dùng.
   — Kiểm bằng: `py -3.8 --version`.
2. **Clone code** vào `D:\RCA-ext\src\` ở đúng revision.
   — Kiểm bằng: `git -C <thư mục> rev-parse HEAD` khớp mục 9 của file kết quả T-001.
3. **Tạo ba môi trường** trong `D:\RCA-ext\envs\`:
   - `py312`: RCAEval chế độ mặc định, cộng psutil và pyarrow. Dùng cho BARO, N-Sigma, CIRCA-PC, MicroRank, TraceRCA, BOCPD, N-Sigma phát hiện.
   - `py38-rcd`: theo `requirements_torai.lock`, cộng chép 5 file vá trong `RCAEval/lib/` vào site-packages, thay cho `script/link.sh` (bản này viết cho Linux). Dùng cho RCD và TORAI.
   - `py38-gdn`: torch 1.5.1+cpu, torch-scatter, torch-sparse bản cho torch 1.5.0+cpu, torch-geometric 1.5.0, theo `install.sh` của GDN. Dùng cho GDN.

   — Kiểm bằng: `pip check` và một lệnh import thử cho mỗi môi trường.

   Nếu `py38-gdn` không cài được: thử chạy GDN trên torch/PyG đời mới trong `py312`, ghi rõ đó là lệch so với code gốc.
4. **Chọn ca đo và ca học cho GDN** theo kích thước file.
   — Kiểm bằng: ghi tên ca và kích thước vào LOG và `do-kha-thi.md`.
5. **Tải và kiểm `torai-data.zip`; giải nén đúng ca đo.**
   — Kiểm bằng: hash khớp Figshare; chỉ có một thư mục ca được giải nén.
6. **Đo từng mục:** BARO, N-Sigma, CIRCA-PC, MicroRank, TraceRCA bản RCAEval, RCD, TORAI, BOCPD, N-Sigma phát hiện, GDN (học và suy luận tách riêng).
   - Mỗi lượt chạy trong một tiến trình con, có giới hạn **1 giờ**.
   - Ghi thời gian bằng `time.perf_counter`, RAM đỉnh bằng psutil.
   - Đầu ra xếp hạng được lưu nhưng không đọc, không chấm.
   - Vượt 1 giờ thì dừng và ghi "> 1 giờ".

   — Kiểm bằng: mỗi mục có log trong `results/T-005/runs/`.
7. **Ghi `do-kha-thi.md` và `moi-truong.md`.**
   — Kiểm bằng: mọi mục ở bước 6 có một dòng kết quả.

## Tiêu chí xong

- Mọi phương pháp và bộ phát hiện trong Q-37 và Q-38 có một dòng trong `do-kha-thi.md`: kết quả đo, hoặc lý do không đo.
- Mọi lượt cài và chạy, kể cả lượt hỏng, có log trong `results/T-005/runs/`.
- `moi-truong.md` đủ để một agent khác dựng lại ba môi trường trên máy khác.
- Không có file nào ngoài Phạm vi ghi bị tạo hay sửa; không mở `data/locked/`; chỉ một ca của zip TORAI được giải nén.

## Không làm

- Không chấm điểm, không đọc thứ hạng mà phương pháp trả ra.
- Không viết adapter chính thức; việc đó thuộc P3, đặt ở `src/`.
- Không cài lại SimpleRCA và không dựng đồ thị kiến trúc cho CIRCA. Cả hai cần code mới, và phần tính toán của chúng nhẹ hơn CIRCA-PC. Ghi lý do không đo trong `do-kha-thi.md`.
- Không chọn dataset, không chạy trên dữ liệu khác ngoài các ca nêu ở Đầu vào.
- Không sửa code thuật toán của các phương pháp, trừ sửa tối thiểu để chạy được (ví dụ API thư viện đã đổi). Mọi chỗ sửa ghi vào LOG và `moi-truong.md`.

## Chi phí ước lượng

- **Tải:** khoảng 0,7–1 GB.
  - Python 3.8.10: 28 MB.
  - Gói cho `py312`, có torch bản CPU: khoảng 300–500 MB.
  - `py38-rcd`: khoảng 150 MB.
  - `py38-gdn`: khoảng 130 MB.
  - `torai-data.zip`: 91 MB.
- **Đĩa:** khoảng 2–3 GB.
- **Thời gian:** mỗi lượt chạy tối đa 1 giờ, nên không chạm ngưỡng phải báo trước của luật cứng 8. Tổng khoảng 2–4 giờ.

Toàn bộ là ước lượng, **chưa kiểm**.

## Rủi ro và điều chưa chắc

- Python 3.8 đã hết hỗ trợ từ 10/2024; bộ cài vẫn còn trên python.org (kiểm ngày 02/10/2026).
- File vá của RCAEval viết cho Linux; chép tay trên Windows có thể thiếu bước. **Chưa kiểm.**
- PyG 1.5 trên Windows có thể không cài được. Cách xử lý ở bước 3.
- CIRCA-PC trên khoảng 360 biến mỗi ca có thể vượt 1 giờ. Kết quả "> 1 giờ" vẫn là kết quả hợp lệ.
- Cấu trúc thư mục trong `torai-data.zip` **chưa kiểm**. Nếu không giải nén riêng một ca được mà không lộ các ca khác thì dừng, đề xuất lại.
- Thời gian đo trên một ca chỉ là chỉ báo. Ca khác hoặc dataset khác có thể nặng hơn.

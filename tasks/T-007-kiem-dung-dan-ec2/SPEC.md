# T-007 — Kiểm đúng đắn trên EC2: MicroRank, TraceRCA, BOCPD

- **Trạng thái:** đã duyệt (03/10/2026)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1 (chuẩn bị P3) — **Cổng:** G1
- **Số phiên:** 2. Phiên 1 dựng máy và giao việc; phiên 2 thu kết quả. Lý do: phải chờ EC2 chạy qua đêm. Đây là ngoại lệ với AGENTS mục 5 ("làm xong trong một phiên"); Minh chấp nhận khi duyệt SPEC này ngày 03/10/2026.
- **Chạy song song với:** T-006 (laptop). Bước E2, E3 chờ file `results/T-006/x1-chot-moi-truong.md`.

## Mục tiêu

Kiểm MicroRank, TraceRCA, BOCPD chạy đúng, trên Linux như tác giả, trước khi dùng số của chúng (LESSONS SL24, Q-41). Đồng thời dựng sẵn EC2 cho T-008 và P3.

Task không trả lời câu hỏi nghiên cứu nào và không chọn dataset. Dữ liệu ở đây chỉ dùng để tái lập số đã công bố.

## Đầu vào

- **EC2** `ubuntu@3.104.124.160` (Q-42): Ubuntu 24.04.4, 2 vCPU, RAM 7,6 GiB, không có swap, đĩa 29 GB. SSH bằng `C:\Windows\System32\OpenSSH\ssh.exe -i D:\RCA-ext\keys\keys.pem -o UserKnownHostsFile=D:\RCA-ext\keys\known_hosts`. Minh bật, tắt máy.
- **Code:** clone lên EC2 ở đúng revision mục 9 của `results/T-001/danh-sach-phuong-phap.md` (RCAEval `259ea41`, BARO `e35f4ec`).
- **Bộ thư viện:** theo `results/T-006/x1-chot-moi-truong.md` (T-006 ghi).
- **Bộ đọc trace:** `results/T-005/scripts/chay_mot_luot.py` (nhánh `microrank`, `tracerca`) và cách cắt cửa sổ trace trong `results/T-005/scripts/chuan_bi_dau_vao.py`. RCAEval không có code đọc trace.
- **Dữ liệu** (chỉ tải lên EC2, không có dữ liệu khóa):
  - RE2-OB từ Hugging Face `phamquiluan/RCAEval`, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`: `traces.parquet` và `inject_time.txt` của 90 ca `re2ob_*`, khoảng 840 MB. Kiểm SHA-256 theo HF (file LFS) hoặc git blob oid (file nhỏ).
  - `fse-ob`: Zenodo 11046533, 144 MB, MD5 theo Zenodo.
- **Nguồn mốc:**
  - Bài TORAI, arXiv 2604.13522v1, Bảng 2, dòng Trace: MicroRank AVERAGE A5 = 0,33; TraceRCA AVERAGE A5 = 0,62 (từng ô theo bảng).
  - README của BARO: tái lập BOCPD trên Online Boutique, P/R/F1 = 0,76/1,00/0,87.
  - Bài BARO, arXiv 2405.09330, Bảng 2: BARO trên Online Boutique, P/R/F1 = 0,69/1/0,82 (khác README; báo cả hai).

## Đầu ra

- `results/T-007/kiem-dung-dan.md`: mỗi mục (MicroRank, TraceRCA, BOCPD) một kết luận: **khớp**, **lệch** (kèm nguyên nhân hoặc "chưa tìm ra" kèm lý do), **không có mốc**. Mỗi ô: mốc, nguồn, kết quả của mình, độ lệch.
- `results/T-007/moi-truong-ec2.md`: cách dựng môi trường trên EC2, danh sách gói (pip freeze), lệnh tải dữ liệu và hash.
- `results/T-007/scripts/`: script chạy và chấm.
- `results/T-007/runs/`: mọi lượt chạy, kể cả lượt hỏng; mỗi khối nén riêng.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- Trên EC2: thư mục `~/rca/`, cộng các gói hệ thống cài ở bước E0.
- `results/T-007/`
- `D:\RCA-ext\keys\known_hosts` (SSH tự ghi).
- Dòng T-007 trong `docs/STATE.md`: đọc lại file ngay trước khi sửa, vì T-006 chạy song song.

## Các bước

| Bước | Việc | Phụ thuộc | Kiểm bằng |
|---|---|---|---|
| E0 | Cài gói hệ thống theo README RCAEval (`build-essential`, `libxml2`, `libxml2-dev`, `zlib1g-dev`, `python3-tk`, `graphviz`) và `python3.12-venv`; cài uv; clone RCAEval, BARO; dựng **cả** `py312` (bản mới nhất) và `py312-pin` (cùng cách như T-006: `uv --exclude-newer 2024-12-22`, phương án dự phòng như SPEC T-006) | không | `git rev-parse HEAD`; `pip check`; import thử |
| E1 | Tải RE2-OB (trace và mốc tiêm của 90 ca) và `fse-ob` | không | hash khớp nguồn; log trong `runs/` |
| E2 | Chờ file X1 của T-006. Nếu X1 ghi "dừng" thì dừng E2, E3 và báo Minh. Không thì: MicroRank, TraceRCA trên 90 ca RE2-OB, cửa sổ 300 s trước + 300 s sau mốc tiêm (`--length 10`, như lệnh TORAI trong `docs/TORAI.md`), bằng bộ đọc trace của T-005 | E0, E1, X1 | mỗi ca có file kết quả; nhật ký tiến độ |
| E3 | Chạy nền nối tiếp E2: `python main.py --dataset OnlineBoutique --anomaly-detection` của BARO | E0, E1, X1 | đầu ra P/R/F1; nhật ký tiến độ |
| E4 (phiên 2) | Chép kết quả về `results/T-007/`; chấm; so mốc; viết `kiem-dung-dan.md`; báo Minh **Stop** EC2 (không Terminate) | E2, E3 | Tiêu chí xong |

**Cách chạy:**
- E2, E3 chạy bằng `nohup` hoặc `tmux` để chạy tiếp khi laptop tắt.
- Kết quả ghi theo từng ca; mỗi khối nén riêng ngay khi xong. Dừng giữa chừng thì các khối đã xong vẫn còn trên đĩa EC2.
- Giới hạn mỗi khối 3 giờ (Q-40). Vượt thì dừng, ghi "vượt ngân sách".
- Không chạy việc nặng khác trên EC2 trong lúc E2, E3 chạy (SL30). Thời gian vẫn ghi lại, nhưng số đo chính thức thuộc T-008.
- Sau mỗi bước: thêm một dòng vào LOG.

## Kiểm đúng đắn

**Tiêu chí khớp** (chốt trước khi chạy, giống T-006):
- Phương pháp tất định (MicroRank, TraceRCA, BOCPD): mỗi ô lệch ≤ 0,02.
- Loại B (MicroRank, TraceRCA: bộ đọc trace và cửa sổ của tác giả không công bố): ghi độ lệch, nêu các nguyên nhân khả thi (Q-33); không kết luận "sai" chỉ vì lệch.
- Không chỉnh tham số để cho khớp.

**Phép kiểm không cần nhãn:**
- Thứ hạng không rỗng.
- Chạy lại một số ca cùng đầu vào ra cùng thứ hạng.
- Giá trị trung gian hợp lý (QT5).

**Kiểm chính script chấm:** chấm bằng `RCAEval.benchmark.evaluation.Evaluator`, ánh xạ thao tác về service theo cách của `main.py` (`x.split("_")[0]`). Nhãn (service gốc, loại lỗi lấy từ tên thư mục ca) chỉ dùng để chấm, không đưa vào phương pháp.

**Không kiểm được trong task, và hệ quả (SL26):**
- Bộ đọc trace của tác giả không công bố, nên lệch ở MicroRank, TraceRCA có thể do bộ đọc. Hệ quả: chỉ kết luận được "khớp" hoặc "lệch, nguyên nhân khả thi là ...".
- Cách chạy BOCPD của tác giả cắt cửa sổ quanh mốc tiêm, tức mốc tiêm đi vào đầu vào của bộ phát hiện. Dùng được để tái lập, không dùng cho chế độ tự phát hiện ở P3 (luật cứng 6). Ghi rõ trong `kiem-dung-dan.md`.
- Không tái lập trên Train Ticket (RE2-TT có ca khóa).

## Tiêu chí xong

- MicroRank, TraceRCA, BOCPD mỗi mục có kết luận kèm bằng chứng.
- Mọi khối có log trong `results/T-007/runs/`.
- `moi-truong-ec2.md` đủ để dựng lại EC2 từ đầu.
- Không chép dữ liệu khóa hay zip TORAI lên EC2; không ghi ngoài Phạm vi ghi.
- Mục kết thúc phiên trong LOG cho cả hai phiên; prompt phản biện cho Codex ở cuối LOG.
- Đã báo Minh Stop EC2.

## Không làm

- Không chép zip TORAI hay bất kỳ dữ liệu khóa nào lên EC2.
- Không Terminate máy.
- Không sửa code phương pháp.
- Không đo thời gian chính thức (thuộc T-008).
- Không chọn dataset.

## Chi phí ước lượng

Toàn bộ là ước lượng, **chưa kiểm**.

- E0: 45–90 phút. E1: khoảng 15 phút. E2: 2–4 giờ. E3: 2–4 giờ (README BARO ghi "around two hours"; EC2 chậm hơn). E4: khoảng 30 phút.
- EC2 khoảng 6–10 giờ, giá $0,1197/giờ, tức khoảng $1–1,2.
- Tải khoảng 1 GB, chỉ trên EC2.
- Có các khối dài hơn 1 giờ (luật cứng 8). Minh duyệt SPEC này ngày 03/10/2026 là duyệt các khối đó.
- So với Q-40: ghi khối nào vượt 3 giờ.

## Rủi ro và điều chưa chắc

- EC2 m7i-flex có mức nền 40% mỗi vCPU; chạy nặng nhiều giờ có thể bị hãm tốc. Không ảnh hưởng tính đúng, chỉ làm lâu hơn.
- Không có swap: lượt nào cần hơn khoảng 7 GB RAM sẽ bị hệ điều hành dừng. MicroRank toàn ca RE2-TT ở T-005 cần 2,3 GB RSS; ca RE2-OB nhỏ hơn.
- Địa chỉ IP đổi mỗi lần Minh Stop/Start máy; phiên 2 hỏi Minh địa chỉ mới nếu kết nối không được.
- Nếu X1 của T-006 chậm, E2, E3 bắt đầu muộn tương ứng.

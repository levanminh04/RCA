# T-006 — Kiểm đúng đắn các phương pháp trên laptop

- **Trạng thái:** đã duyệt (03/10/2026)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1 (chuẩn bị P3) — **Cổng:** G1
- **Chạy song song với:** T-007 (EC2). T-007 đọc file `results/T-006/x1-chot-moi-truong.md` do task này ghi.

## Mục tiêu

Biết code đang chạy cho kết quả đúng hay không, trước khi dùng số của nó (LESSONS SL24, Q-41). Cách làm: chạy lại các phương pháp trên dữ liệu có số công bố, so từng ô. Đồng thời chốt bộ thư viện cho Python 3.12 (bước X1) và chuyển kết quả đó cho T-007.

Phạm vi: BARO, N-Sigma, CIRCA-PC, RCD, TORAI, N-Sigma phát hiện, GDN. MicroRank, TraceRCA, BOCPD thuộc T-007.

Task không trả lời câu hỏi nghiên cứu nào và không chọn dataset. Dữ liệu ở đây chỉ dùng để tái lập số đã công bố.

## Đầu vào

**Code:** `D:\RCA-ext\src\` ở đúng revision mục 9 của `results/T-001/danh-sach-phuong-phap.md` (RCAEval `259ea41`, BARO `e35f4ec`, GDN `9853899`). Kiểm bằng `git rev-parse HEAD` trước khi chạy.

**Môi trường có sẵn** (dựng ở T-005, xem `results/T-005/moi-truong.md`): `py38-rcd` (lock của TORAI), `py38-gdn`, `py312` (bản thư viện mới nhất ngày 03/10/2026).

**Môi trường mới:**
- `py312-pin`: RCAEval `[default]`, chỉ lấy bản phát hành trước ngày 22/12/2024 (ngày nộp bài RCAEval), cài bằng `uv --exclude-newer 2024-12-22`. uv cài trong `D:\RCA-ext\envs\tools`, không cài vào Python hệ thống.
  - Nếu gói nào không có bản dựng sẵn trước ngày đó: chỉ ghim các thư viện chính (pandas < 3, numpy < 2, causal-learn ≤ 0.1.3.9, scikit-learn, scipy, torch theo bản phát hành trước ngày đó), ghi lại trong `moi-truong.md`.
- `py38-rcdlock`: theo `docs/SETUP.md` của RCAEval: `pip install -e .[rcd]` (lock `requirements_rcd.lock`), chép 5 file vá của `script/link.sh` vào site-packages (Windows không dùng symlink).

**Dữ liệu** (tải vào `D:\RCA-ext\data\`; kiểm hash trước khi dùng):
- `torai-OB`, `torai-SS`: giải nén từ `D:\RCA-ext\dl\torai-data.zip` (đã kiểm MD5 ở T-005). Chỉ hai thư mục này; không giải nén và không đọc nội dung gì trong `torai-TT`.
- RE1-OB, RE1-SS: Zenodo 14590730 (29,5 + 75,4 MB, MD5 theo Zenodo).
- `fse-ob`, `fse-ss`: Zenodo 11046533 (144 + 121 MB, MD5 theo Zenodo).
- Dữ liệu mẫu BARO `simple_data.csv` (0,6 MB, GitHub release 0.0.4 của BARO). Ghi SHA-256.
- Dữ liệu mẫu MSL có sẵn trong repo GDN (`data/msl`).

**Nguồn mốc:**
- README của BARO; `docs/TORAI.md`, `docs/SETUP.md` của RCAEval.
- Bài BARO, arXiv 2405.09330 (FSE'24): Bảng 2, 3.
- Bài TORAI, arXiv 2604.13522v1 (FSE'26): Bảng 2, 3.

**Ba loại mốc:**
- **A**: có lệnh tái lập của tác giả và đầu ra mong đợi ghi sẵn.
- **B**: chỉ có số trong bài; phải dựng lại cách chạy theo mô tả.
- **C**: không có mốc.

## Đầu ra

- `results/T-006/kiem-dung-dan.md`: mỗi mục một kết luận: **khớp**, **lệch** (kèm nguyên nhân, hoặc "chưa tìm ra" kèm lý do), hoặc **không có mốc** (kèm lý do). Mỗi ô ghi: mốc, nguồn, kết quả của mình, độ lệch.
- `results/T-006/x1-chot-moi-truong.md`: kết quả X1 và bộ thư viện đã chốt (hoặc "dừng").
- `results/T-006/moi-truong.md`: cách dựng `py312-pin`, `py38-rcdlock`; danh sách gói đầy đủ (pip freeze).
- `results/T-006/scripts/`: script chạy và chấm.
- `results/T-006/runs/`: mọi lượt chạy, kể cả lượt hỏng (luật cứng 10). Mỗi khối nén riêng: log, file kết quả từng ca, đầu ra của `main.py`.
- Đề xuất mục WHY cho bộ thư viện đã chốt. Chỉ đề xuất trong LOG; Minh duyệt mới ghi `docs/WHY.md`.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-006/`
- `D:\RCA-ext\` (môi trường, dữ liệu, thư mục làm việc). Không sửa `D:\RCA-ext\src\` (code của tác giả) và không sửa các môi trường của T-005 ngoài việc thêm môi trường mới.
- Dòng T-006 trong `docs/STATE.md`: đọc lại file ngay trước khi sửa, vì T-007 chạy song song.

## Các bước

### Bước 0 — chuẩn bị (trước khi chạy luồng)

1. Kiểm revision của ba repo. — Kiểm bằng: `git rev-parse HEAD`.
2. **Kiểm tĩnh `sli`:** `main.py` truyền `sli` suy từ tên service gốc (nhãn). Grep các hàm `baro`, `nsigma`, `circa`, `rcd`, `torai` của RCAEval để chắc chúng không đọc `sli`. Nếu hàm nào đọc: ghi lại, báo Minh trước khi dùng kết quả của hàm đó. — Kiểm bằng: kết quả grep ghi vào LOG.
3. Tải dữ liệu, kiểm hash. — Kiểm bằng: hash khớp nguồn; log trong `runs/`.
4. **Kiểm quan hệ RE1 với `fse-*`:** so danh sách ca và nội dung vài ca. Kết quả quyết định số trong bài BARO có so được với kết quả chạy trên RE1 không. Nếu không so được: chạy thẳng trên `fse-*` bằng script dựng lại cách chạy của `main.py`, ghi là loại B. — Kiểm bằng: bảng so ghi vào LOG.

### Bốn luồng chạy song song (mỗi luồng tuần tự)

| Luồng | Khối (theo thứ tự) | Mốc |
|---|---|---|
| **L1** (`py38-rcd`) | TORAI ×3 trên `torai-OB`, rồi ×3 trên `torai-SS`. Lệnh `main.py --method torai --length 10` | A: `docs/TORAI.md` (OB); B: Bảng 2, 3 bài TORAI |
| **L2** (`py38-rcd`) | RCD ×3 trên `torai-OB`, rồi ×3 trên `torai-SS` (`--length 10`) | B: Bảng 2, 3 bài TORAI (dòng Metric) |
| **L3** (`py38-rcdlock`) | Dựng môi trường, rồi RCD ×1 trên RE1-OB: `main.py --method rcd --dataset online-boutique`, độ dài mặc định | A: `docs/SETUP.md` (tác giả chạy 1 lần) |
| **L4** (`py312`, `py312-pin`) | ① Dựng `py312-pin`. ② **X1**: chạy bằng **cả hai** bộ thư viện: ví dụ mẫu BARO (A: phát hiện ở bước 243, top 5 cụ thể); `reproduce_baro` trên `fse-ob` (A: Avg@5 0,91/0,96/0,95/0,62/0,86); CIRCA trên `torai-OB` (B). ③ **Chốt bộ thư viện** theo luật dưới; ghi `results/T-006/x1-chot-moi-truong.md`. ④ Bằng bộ đã chốt: BARO và CIRCA trên `torai-OB/SS` (B: Bảng 2, 3 bài TORAI; bỏ dòng BARO của Bảng 2 vì trùng từng số với Bảng 4, nghi chép nhầm); `baro`, `nsigma`, `circa` của RCAEval khi biết mốc tiêm, trên RE1 hoặc `fse` theo kết quả bước 0.4 (B: Bảng 3 bài BARO, các dòng [t_inject]). ⑤ N-Sigma phát hiện trên `fse-ob/ss` (B: Bảng 2 bài BARO; cách chấm chép từ `reproduce_bocpd`). ⑥ GDN chạy `run.sh` với dữ liệu MSL mẫu, 2 lần cùng seed (C: loss giảm, hai lần ra cùng kết quả, điểm hữu hạn) | như cột trái |

**Luật chốt bộ thư viện ở X1** (viết trước khi chạy):
- Bộ ghim khớp mốc → dùng bộ ghim (SL29).
- Chỉ bộ hiện tại khớp → dùng bộ hiện tại, ghi lý do.
- Không bộ nào khớp → **dừng** các khối Python 3.12 còn lại, báo Minh, ghi "dừng" vào file X1 để T-007 cũng dừng.

### Cách chạy (áp dụng mọi khối)

- Dùng đúng lệnh của tác giả (`main.py` RCAEval, `main.py` BARO). Chỉ chỗ không có lệnh mới dùng script của mình; ghi là loại B.
- **Mỗi khối "phương pháp × dataset × lần" có thư mục làm việc riêng** trong `D:\RCA-ext\work\T-006\`, vì `main.py` chấm mọi file trong thư mục `output`.
- `main.py` ghi file kết quả ngay sau mỗi ca. Khối nào xong thì nén vào `results/T-006/runs/`. Dừng giữa chừng thì các khối đã xong vẫn còn; chỉ khối dở phải chạy lại.
- Mỗi tiến trình đặt `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` để 4 luồng không tranh CPU. Rủi ro rất nhỏ: chữ số thập phân cuối có thể khác khi chạy đa luồng.
- Mỗi ca ghi thời điểm bắt đầu và kết thúc vào nhật ký tiến độ (SL25).
- Giới hạn mỗi khối 3 giờ (Q-40). Vượt thì dừng, ghi "vượt ngân sách".
- Theo dõi RAM trống. Dưới 3 GB thì báo Minh tắt ứng dụng khác.
- Thời gian trong task này **không dùng làm số đo**, vì máy chạy song song. Đo sạch thuộc T-008.
- Sau mỗi khối: thêm một dòng vào LOG.

## Kiểm đúng đắn

**Tiêu chí khớp** (chốt trước khi chạy):
- Phương pháp tất định: mỗi ô lệch ≤ 0,02.
- RCD, TORAI: trung bình 3 lần; ô AVERAGE lệch ≤ 0,05; báo từng ô và độ lệch giữa các lần.
- Loại B: ghi độ lệch, nêu các nguyên nhân khả thi (Q-33); không kết luận "sai" chỉ vì lệch.
- Không chỉnh tham số để cho khớp.

**Phép kiểm không cần nhãn, cho mọi khối:**
- Thứ hạng không rỗng.
- Không rơi vào nhánh dự phòng "trả thứ tự cột" (bắt thông báo lỗi ở stderr của wrapper `@rca`).
- Phương pháp tất định: chạy lại cùng đầu vào ra cùng thứ hạng.
- Giá trị trung gian hợp lý (ví dụ mật độ đồ thị của CIRCA; QT5).

**Kiểm chính script chấm của mình:** tính lại Avg@5 từ file từng ca bằng `RCAEval.benchmark.evaluation.Evaluator`; phải ra đúng số `main.py` in ra. AC@1, AC@3 tính cùng cách (`main.py` không in hai chỉ số này).

**Không kiểm được trong task, và hệ quả (SL26):**
- Không tái lập trên Train Ticket: RE2-TT có ca khóa; bài BARO cho CIRCA trên Train Ticket chỉ có 15/100 ca. Hệ quả: tính đúng trên dữ liệu cỡ Train Ticket chưa được kiểm trực tiếp.
- Dòng BARO ở Bảng 2 bài TORAI nghi chép nhầm. Hệ quả: BARO trên `torai-OB` không có mốc từ bài TORAI; dùng mốc của bài BARO thay.
- GDN không có số mốc. Hệ quả: chỉ biết GDN chạy ổn định, không biết nó cho kết quả đúng như bài.
- Cách chạy BOCPD của tác giả đưa mốc tiêm vào đầu vào (cắt cửa sổ quanh mốc). Dùng được để tái lập, không dùng cho chế độ tự phát hiện ở P3 (luật cứng 6). Ghi rõ trong `kiem-dung-dan.md`.

## Tiêu chí xong

- Đủ 7 mục (BARO, N-Sigma, CIRCA-PC, RCD, TORAI, N-Sigma phát hiện, GDN), mỗi mục có kết luận kèm bằng chứng.
- X1 đã chốt; `x1-chot-moi-truong.md` đã có.
- Mọi khối có log trong `results/T-006/runs/`.
- Không đọc `torai-TT`, không đụng `data/locked/`, không ghi ngoài Phạm vi ghi.
- Mục kết thúc phiên trong LOG theo AGENTS mục 7; prompt phản biện cho Codex ở cuối LOG.

## Không làm

- Không đo thời gian chính thức (thuộc T-008).
- Không sửa code phương pháp.
- Không chạy trên RE2-TT.
- Không chọn dataset.
- Không chỉnh tham số theo kết quả.

## Chi phí ước lượng

Toàn bộ là ước lượng, **chưa kiểm** (chưa chạy trên máy này với các dữ liệu này).

- Tải khoảng 0,4 GB.
- Laptop chạy 4 luồng khoảng 3,5–4,5 giờ: L1 1,5–3,5 giờ; L2 1,5–3 giờ; L3 1,5–3 giờ; L4 3–4,5 giờ (X1 xong khoảng 1 giờ sau khi bắt đầu).
- Có các khối dài hơn 1 giờ (luật cứng 8). Minh duyệt SPEC này ngày 03/10/2026 là duyệt các khối đó.
- So với Q-40 (3 giờ cho mỗi phương pháp trên một dataset): ghi khối nào vượt.
- RAM: dự kiến dưới 3 GB cho cả 4 luồng.

## Rủi ro và điều chưa chắc

- `uv --exclude-newer` có thể không cài được trên Windows vì thiếu bản dựng sẵn. Đã có phương án dự phòng ở mục Đầu vào.
- RE1 có thể không phải dữ liệu của bài BARO. Bước 0.4 kiểm điều này.
- Có thể lệch do Windows khác Linux. Nếu một mục lệch, đề xuất với Minh chạy lại mục đó trên EC2 trong T-007.
- Laptop phải không ngủ trong lúc chạy (Minh đặt Sleep = Never khi cắm điện; agent không đổi cài đặt hệ thống).

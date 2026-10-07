# T-025 — Chế độ (b): N-Sigma, BOCPD và RCA tại báo động đầu trên 30 ca dev RE2-TT

- **Trạng thái:** đã duyệt 06/10/2026 (lời Minh: "bạn tạo spec cho 2 task luôn cho tôi"; phân công: "claude sẽ làm 25"; về chi phí: "tôi cho phép chạy lâu mà"). Người làm rà lại SPEC trước khi triển khai (bước 0).
- **Người làm:** Claude.
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ2, RQ1 và DT18-NV3 qua P3, chế độ (b): phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố (Q-74 Q11). Trả lời:
1. N-Sigma (tập cột chính và đối chứng mọi cột) và BOCPD phát hiện ra sao trên 30 ca dev (§7.4).
2. BARO, CIRCA kiến trúc (OLS đã khóa), TORAI (nguồn B) xếp root ra sao khi chạy tại báo động đầu t̂ của N-Sigma tập chính và của BOCPD; thành công chung (§7.5).

Không kết luận về đồ thị (P4).

## Đầu vào

- Giao thức `results/T-022/giao-thuc-v2.md` (mục 4, 7, 8, 9, 10, 13); cấu hình `results/T-022/cau-hinh/p3-re2tt-v2.json` (`che_do_b`).
- `results/T-022/allowlist-dev.json`, `nhan-dev.json` (chỉ evaluator đọc; runner chế độ (b) không đọc mốc), `mappings/universe-re2tt-dev.json`.
- Mã `src/p3/` (hash `8d4cc8196c87ee56…`, `results/T-031/moi-truong.json`); `src/p3/adapters/phat_hien.py` (BOCPD, N-Sigma, `luot_rca`), `src/p3/danh_gia.py` (`cham_phat_hien`, `thanh_cong_chung`).
- Khóa: `results/T-031/khoa-cau-hinh.md` (CIRCA OLS+RHT+DA; TORAI B). Pilot và chiếu: `results/T-031/do-chi-phi.md` mục 2, 4–7; script `results/T-031/scripts/{chay.py, chay_ec2.py, chay_torai_ec2.sh, bocpd_tien_to.py}`.
- Quyết định: Q-72, Q-79 (BOCPD trên EC2, không trần 20 giờ; Minh theo dõi qua SSH và dừng khi thấy quá lâu; giữ đầu vào không chọn theo mốc, tiến độ từng ca, giữ lượt hỏng), Q-80, Q-82.
- EC2: host và key theo LOG T-031 14:05–14:47 (`D:/RCA-ext/keys/`, không chép key vào repo). Dữ liệu 30 ca dev có sẵn ở `~/rca/T-031/` (89 parquet; chỉ đọc). Env `main` của T-031 thiếu BARO và ba gói mà BARO import (`matplotlib`, `requests`, `tqdm`). T-025 dựng env riêng `~/rca/T-025/envs/main`: Python 3.12.3 do uv cài vào `~/rca/T-025/python`; numpy 1.26.4, pandas 2.2.3, pyarrow 18.1.0, scipy 1.14.1, psutil 6.1.1 như T-031, thêm matplotlib 3.10.0, requests 2.30.0, tqdm 4.65.0 như laptop. Chép mã BARO e35f4ec lên `~/rca/T-025/src/baro`, so SHA-256 từng tệp với laptop. Mọi cache đặt trong `~/rca/T-025/`; ghi `pip freeze` (sửa C1, Minh duyệt 06/10/2026). Trên cả hai máy, env T-025 thêm scikit-learn 1.6.0, networkx 2.8.8, statsmodels 0.14.4, joblib 1.2.0, threadpoolctl 3.1.0, drain3 0.9.11 và gói nào còn thiếu khi thử import, theo phiên bản laptop; chép CIRCA 0215e18, RCAEval 259ea41, `src/circa_kien_truc`, `src/torai`, BARO, so SHA-256; TORAI chạy bằng Python 3.8 với lock T-016, dựng trong `~/rca/T-025` (như T-031); chép 89 parquet sang máy hai, kiểm SHA-256 với allowlist. Laptop chỉ làm việc nhẹ: chốt danh sách bản ghi, evaluator, tính tay, báo cáo; test T-030 chạy trên laptop chỉ khi không có tiến trình T-024 nào (sửa đổi môi trường, Minh duyệt 06/10/2026: "duyệt văn bản trên, miễn là vẫn giữ nguyên cách làm, đây chỉ đơn giản là đổi môi trường thôi"). IP có thể đổi sau khi Stop/Start: không vào được thì hỏi Minh.

## Đầu ra

Trong `results/T-025/`:
- `runs/<run-id>/`: mọi lượt (BOCPD từ EC2 chép về, N-Sigma, RCA tại t̂), bản ghi §13, stdout/stderr, tiến độ từng ca, thời gian, RSS; giữ lượt hỏng. Không chép telemetry (bảng CSV TORAI: ghi manifest rồi xóa, như T-031).
- `bao-dong.json`: báo động thô từng ca, từng bộ phát hiện; điểm đổi BOCPD kèm `maxes` gốc (§7.2); trạng thái (`OK`, `ERROR` do posterior không hữu hạn, `TIMEOUT`); t̂ của lượt RCA (§7.5). Không chứa nhãn.
- `ban-ghi-dua-vao-cham.json`: danh sách mọi bản ghi đưa vào evaluator (đường dẫn, SHA-256, hash `src/p3`). Ghi trước lượt evaluator đầu tiên.
- `phat-hien.json`, `phat-hien.md`: §7.4 theo cửa sổ 60 s và theo ca; báo động sai mỗi giờ (mẫu số riêng từng bộ); độ trễ N-Sigma, độ lệch vị trí điểm đổi hồi cứu BOCPD; số thông báo sau thời gian trơ.
- `cham-b.json`, `cham-b.md`: RCA tại t̂, 3 ranker × 2 bộ phát hiện; thành công chung (§7.5); thứ hạng tại báo động sai báo riêng; độ đo §8 trên ca có lượt RCA; CIRCA kèm riêng nhóm không vượt ngưỡng 1e10 theo luật §6.5 áp trên bản ghi tại t̂; TORAI trung bình 3 seed.
- `chi-phi.md`: thời gian thật từng ca BOCPD trên EC2, N-Sigma, RCA; so với chiếu laptop của T-031 (H1/H2).
- `scripts/`.

## Phạm vi ghi

- `results/T-025/` (tạm ở `results/T-025/work/`).
- EC2: chỉ `~/rca/T-025/`. Đọc, không sửa `~/rca/T-031/` (env, dữ liệu). Không đụng `~/rca/T-014`, `~/rca/T-015`, `~/rca-t003`.
- EC2 thứ hai (`3.107.246.249`, key `keys.pem`): chỉ ghi `~/rca/T-025/`. Không đụng mọi thư mục khác đang có trong `~/rca/` của máy đó. (sửa đổi môi trường, Minh duyệt 06/10/2026: "duyệt văn bản trên, miễn là vẫn giữ nguyên cách làm, đây chỉ đơn giản là đổi môi trường thôi").
- `src/p3/`: chỉ sửa lỗi runner hoặc adapter thấy khi chạy; mỗi lần sửa ghi LOG, chạy lại test T-030 (đầu ra ở `results/T-025/test-chay-lai/`), giữ lượt hỏng. Sửa làm đổi hash `src/p3` khi T-024 đang dùng lại bản ghi T-031: dừng, báo Minh trước.
- Test T-030 ghi/xóa cache trong `results/T-030/work/`; được ghi trong thư mục đó.
- `tasks/T-025-che-do-b/LOG.md`; dòng T-025 trong `docs/STATE.md`.

Không sửa SPEC này, `results/T-022/`, `results/T-030/` (trừ `work/`), `results/T-031/`, `results/T-024/`, `docs/`, code phương pháp, môi trường chung, `data/`. Python không ghi bytecode.

## Các bước

Giới hạn mỗi lượt, khai trước theo §8.3 (N3):
- **BOCPD: 6 giờ (21.600 s) mỗi ca** (một lượt = một ca đủ 1.441 điểm). Lý do: chiếu laptop ca lớn nhất ≈ 0,8–0,9 giờ (`results/T-031/do-chi-phi.md` mục 5, chưa kiểm); 6 giờ chừa ≈ 6–7 lần cho dao động máy và tốc độ EC2 chưa đo. Không đổi sau khi thấy thời gian.
- **Mọi lượt khác: 3.600 s.**
Vượt thì ghi `TIMEOUT`, giữ lượt, chạy ca tiếp. Minh dừng giữa chừng thì ca chưa chạy là `TIMEOUT` (§8.3). Mọi trạng thái khác `OK` ở mẫu số, tính trượt.

0. **Rà SPEC và mở phiên.** Rà SPEC này độc lập (xem prompt trong LOG). Có điểm chặn thì dừng, báo Minh. Không thì: kiểm hash `src/p3`, hash dữ liệu trên laptop và trên EC2 so với allowlist, môi trường hai máy. — kiểm: mục "Rà SPEC" và dòng mở phiên trong LOG.
1. **Khởi chạy BOCPD 30 ca trên EC2** trong tmux (chạy tiếp khi laptop tắt), tuần tự theo thứ tự mã mờ, qua runner chế độ (b) không đọc mốc. Kiểm posterior hữu hạn (§7.2). Tiến độ từng ca ghi ra file đọc được qua SSH (`~/rca/T-025/trang-thai.txt`). Ghi LOG checkpoint: lệnh xem tiến độ, đường dẫn, cách dừng. Phiên có thể kết thúc khi BOCPD đang chạy.
2. **N-Sigma trên EC2 thứ hai, song song với bước 1:** 30 ca × tập chính và đối chứng mọi cột (§7.3). Không chạy lượt nào của T-025 trên laptop. (sửa đổi môi trường, Minh duyệt 06/10/2026: "duyệt văn bản trên, miễn là vẫn giữ nguyên cách làm, đây chỉ đơn giản là đổi môi trường thôi").
3. **Lượt RCA tại t̂** (§7.5) cho BARO, CIRCA OLS (RHT+DA, kèm RHT-only), TORAI B (seed 0, 1, 2), với t̂ = báo động đầu của N-Sigma tập chính và của BOCPD. Ca không có báo động: không có lượt RCA, tính trượt. Cửa sổ chạm biên file: cắt, ghi độ dài thực; lỗi do N ngắn là `ERROR`. N-Sigma đối chứng chỉ chấm phát hiện, không chạy RCA (Q-74 Q12 dùng nó làm đối chứng phát hiện). RCA tại t̂ của N-Sigma chạy trên EC2 thứ hai ngay khi N-Sigma xong; RCA tại t̂ của BOCPD chạy trên máy nào rảnh trước, sau khi bước 1 xong (chép bản ghi BOCPD nếu cần). Mỗi lượt ghi rõ chạy trên máy nào. (sửa đổi môi trường, Minh duyệt 06/10/2026: "duyệt văn bản trên, miễn là vẫn giữ nguyên cách làm, đây chỉ đơn giản là đổi môi trường thôi").
4. **Chốt danh sách bản ghi**: ghi `bao-dong.json`, `ban-ghi-dua-vao-cham.json`, thêm một dòng LOG có giờ máy. Sau dòng này không chạy lại, không thêm, không bỏ bản ghi nào vì kết quả chấm.
5. **Evaluator:** phát hiện (§7.4) và RCA (§7.5, §8). Nhãn chỉ nối sau khi đầu ra đã ghi ra file. Ca bộ phát hiện không `OK`: phát hiện theo ca và thành công chung tính trên 30 ca, ca không `OK` là trượt. Chấm theo cửa sổ, báo động sai mỗi giờ, độ trễ và số thông báo chỉ tính trên ca `OK`, ghi rõ "có điều kiện trên n ca OK", kèm số ca theo trạng thái (sửa U1, Minh duyệt 06/10/2026).
6. **Viết `phat-hien.md`, `cham-b.md`, `chi-phi.md`.** Ghi rõ: BOCPD và nhánh dùng nó là hồi cứu (§4, §7.2), không gắn với thời điểm t̂+300; tên "độ lệch vị trí điểm đổi hồi cứu" cho BOCPD; chi phí là của EC2; CIRCA báo trên mọi ca có lượt RCA, kèm riêng nhóm không vượt ngưỡng.

## Kiểm đúng đắn

- Test T-030 đạt 57/57 trên cùng hash `src/p3`: dùng lại `results/T-024/test-chay-lai/tom-tat.json` (06/10 21:59); T-025 chỉ kiểm hash `src/p3` trước bước 5; chạy lại nếu hash đổi (Minh duyệt 07/10/2026: "duyệt a, b").
- §11.8 trên đầu ra thật: đổi mốc ở phía evaluator thì báo động giống hệt (cả hai bộ phát hiện); `job.json` bộ phát hiện không có mốc.
- BOCPD: chạy cùng một ca ngắn (tiền tố T = 150 của ca nhỏ nhất) trên laptop và EC2 cho R và điểm đổi giống hệt hoặc chỉ lệch ở mức dấu phẩy động; ghi kết quả. Kiểm posterior hữu hạn ở mọi ca; ghi tần suất `ERROR`.
- N-Sigma tập chính: so báo động 3 ca pilot với `results/T-031/runs/pilot-nsigma-001` (cùng hash mã thì phải giống hệt).
- Trước khi chốt danh sách (bước 4): chạy khô evaluator với nhãn giả (mốc và root gán ngẫu nhiên, không đọc file nhãn thật) để bắt lỗi chương trình; sửa script nếu cần trước khi thấy số thật (Minh duyệt 07/10/2026: "duyệt a, b").
- Tính lại độc lập (mã riêng, không dùng `src/p3/danh_gia.py`) chấm phát hiện và thành công chung ở cả 30 ca, mọi bộ phát hiện và ranker; phải khớp từng ca (Minh duyệt 07/10/2026: "duyệt a, b").
- Thứ hạng tại t̂: ở ca có t̂ = t (nếu có), so với bản ghi chế độ (a) cùng phương pháp (EC2 so với laptop); giống hệt, hoặc lệch chỉ ở mức dấu phẩy động; báo đúng điều thấy được (sửa đổi môi trường, Minh duyệt 06/10/2026: "duyệt văn bản trên, miễn là vẫn giữ nguyên cách làm, đây chỉ đơn giản là đổi môi trường thôi").
- Kết quả quá đẹp thì soi từng ca và chạy phép thử giả trong evaluator trước khi báo.
- Không kiểm được trong task: tính đại diện cho test; ảnh hưởng của mốc cố định ở giây 720 (§7.1).

## Tiêu chí xong

- `bao-dong.json`, `ban-ghi-dua-vao-cham.json`, `phat-hien.json`, `cham-b.json` có thật, parse được; `phat-hien.md`, `cham-b.md`, `chi-phi.md` có thật, mỗi số có nguồn.
- 30 ca × (BOCPD, N-Sigma chính, N-Sigma đối chứng) có trạng thái; ca chưa chạy do Minh dừng ghi `TIMEOUT` kèm lời Minh.
- LOG có dòng chốt danh sách bản ghi trước lượt evaluator đầu tiên.
- Tiến trình trên EC2 đã kết thúc hoặc đã dừng; LOG ghi trạng thái EC2 (máy còn bật hay không, do Minh quyết).
- Không mở `data/locked/`; không đổi cấu hình sau khi thấy số.
- LOG đủ để agent khác làm tiếp; dòng STATE đã cập nhật; prompt phản biện viết sẵn cuối LOG.

## Không làm

Không chia đoạn chuỗi, không đổi hazard, likelihood, tập cột hay tiền xử lý BOCPD để rút thời gian. Không chạy MicroRank, SimpleRCA, TraceRCA ở chế độ (b) (§7.5). Không mở lượt RCA ở thông báo sau thời gian trơ (chỉ đếm). Không gộp episode khi chấm phát hiện. Không chọn ngưỡng, seed, cột sau khi thấy số. Không mở test, RE3-OB; không chạy Nezha, Eadro. Không sửa WHY, DECISIONS, giao thức. Không bật/tắt EC2 nếu Minh chưa bảo. Không commit hay push khi Minh chưa duyệt.

## Chi phí ước lượng

**Chưa kiểm.**
- BOCPD 30 ca: laptop chiếu ≈ 8–35 giờ (`results/T-031/do-chi-phi.md` mục 5); EC2 chưa đo, sẽ biết sau ca đầu. Q-79 cho phép chạy lâu trên EC2; duyệt SPEC này là đồng ý trước lượt BOCPD dài hơn 1 giờ (luật cứng 8).
- N-Sigma laptop: ≈ 4 phút (tập chính), ≈ 51 phút (mọi cột).
- RCA tại t̂: tối đa 2 × 30 lượt BARO, CIRCA và 2 × 30 × 3 lượt TORAI B; TORAI trên laptop 25–88 s/lượt → tới ≈ 2–4,5 giờ tổng nếu mọi ca có báo động. Duyệt SPEC này là đồng ý trước đợt này trên laptop.
- Công agent ≈ 4–6 giờ, chia 2–3 phiên (phiên khởi chạy, phiên sau khi BOCPD xong).
- RAM BOCPD ≈ 200 MB/ca; EC2 7,6 GB. Đĩa < 1 GB.

## Rủi ro và điều chưa chắc

- Posterior BOCPD không hữu hạn ở một số ca → `ERROR`; tần suất chưa kiểm.
- Tốc độ EC2 (2 vCPU = 1 lõi vật lý) chưa đo; dao động ≈ 3 lần từng thấy trên laptop. Ca chạm 6 giờ thì `TIMEOUT`.
- Mốc RE2-TT luôn ở giây 720: số phát hiện chỉ nói cho cấu hình này (§7.1).
- Ngưỡng 1e10 cho CIRCA tại t̂: nguyên nhân lỗi làm tròn chỉ xác nhận ở 11 ca dev chế độ (a) (WHY-36); tại t̂ nhóm vượt ngưỡng chỉ có nghĩa là vượt ngưỡng.
- Cửa sổ quanh t̂ có thể chạm biên file (t̂ gần đầu hoặc cuối bản ghi).
- T-024 chạy song song trên laptop: không chạy hai lượt nặng cùng lúc.

# Nhật ký T-034 — Gói trình G2

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Phiên 1 — 13/10/2026 — Claude — laptop Windows 11 (LeVanMinh) và hai EC2 hiện có — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, toàn bộ SPEC T-034. Task chưa có LOG, chưa có dòng STATE và chưa có `results/T-034/`: đây là trạng thái mở task đã dự kiến ở bước 0 của SPEC. Không có đầu ra phiên trước cần kiểm.

**Nguồn duyệt (nguyên lời Minh, chép từ SPEC):**
- Duyệt SPEC bản 3 và giao triển khai, 13/10/2026: “DUYỆT. TẠO SPEC GIÚP TÔI, TRONG QUÁ TRÌNH TẠO KIỂM LẠI 1 LẦN NỮA, KHÔNG DÙNG SUBAGENT, SAU ĐÓ TẠO PROMPT YÊU CẦU CLAUDE TRIỂN KHAI TASK 34, SAU ĐÓ LIỆT KÊ CHO TÔI CÁC LƯU Ý VỀ TASK NÀY ĐỂ TRÁNH VIỆC CLAUDE LÀM XONG RỒI TÔI MỚI PHÁT HIỆN CÓ ĐIỀU GÌ ĐÓ VƯỢT TRÁI MONG MUỐN CỦA TÔI CŨNG NHƯ ẢNH HƯỞNG KẾT QUẢ BẢO VỆ ĐỒ ÁN”.
- Duyệt bổ sung, 13/10/2026: “DUYỆT SỬA SPEC R1–R5, bước tự kiểm trước triển khai”.
- Duyệt mở rộng, 13/10/2026: “vậy 2 phép kiểm này làm trong t34 luôn ? nếu vậy thì duyệt sửa spec, điều phối sử dụng tài nguyên phù hợp”.
- Prompt giao việc của Minh trong chat 13/10/2026: thực hiện T-034 theo SPEC đã duyệt; Claude làm, Codex phản biện kết quả; không dùng subagent; tự xử lý các bước và lựa chọn kỹ thuật trong quyền đã duyệt, không xin duyệt lại.
- Minh duyệt SPEC ngày 13/10/2026 (ba lời trên). Các lời duyệt này hiện chỉ nằm trong SPEC, chưa có dòng trong `docs/DECISIONS.md`; SPEC không cho T-034 sửa DECISIONS nên chỉ ghi nhận ở đây và trình ở cuối phiên.

**Công đoạn và mục tiêu nguồn:** làm. Cổng G2 của MRP §7 (sau P3, P4): bảng baseline trên dev và bản đồ hạn chế; ba câu của PLAN-P3-G2 §8; sáu câu MRP §7; năm đầu ra P4 (MRP P4, “Cách dùng G2”). Nguồn đề tài: DT18-NV2, NV3; hướng dẫn của cô §1 (“chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có → tiếp cận phương pháp đồ thị”). Phạm vi được duyệt: tổng hợp K1–K7, hai phép E1 (quy tắc pattern TraceRCA) và E2 (BOCPD miền log trên hai ca underflow), điều phối laptop và hai EC2 hiện có. Không chọn thành phần P5/P6, không mở test, không sửa baseline.

**Diễn biến** (một dòng mỗi bước con, ghi ngay khi xong; giờ theo đồng hồ laptop, +07):

- 12:05 — Đọc nguồn khung: AGENTS; STATE; SPEC T-034; MRP toàn bộ; PLAN-P3-G2 toàn bộ; DT18; hướng dẫn của cô 23/09; LESSONS; WHY-01, WHY-02, WHY-22–50 và mọi phần nối tới “Đính chính phạm vi kết luận phụ thuộc WHY-47”; DECISIONS các dòng Q-04, Q-30, Q-35, Q-38, Q-40, Q-41, Q-43, Q-44, Q-58–Q-63, Q-65, Q-70, Q-82–Q-89, Q-93, Q-127, Q-137–Q-145. Không sửa file nào.
- 12:15 — Đọc nguồn diễn giải theo đúng thứ tự bắt buộc của SPEC: `results/T-032/runs/bo-sung-toan-dien-20261012-001/doi-chieu-dien-giai-review-001.md` → `bo-sung-bao-cao-review-001.md` → `BAO-CAO-TONG-HOP.md` → `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/report-final-004.md`. Sau đó mới đọc `results/T-032/nguyen-nhan-xep-hang.md`, hai bản đồ T-028/T-029 (phần bảng chính), `closure-ledger.json` (26 dòng cho 23 câu hỏi nguồn) cùng `closure-ledger-review-001.json` (đính chính; `/source_ledger` dẫn về ledger gốc).
- 12:20 — Đọc nguồn hai phép: `results/T-032/scripts/tracerca_original_ranking_v1.py`; mã tác giả `author-tracerca/source/run_localization_association_rule_mining_20210516.py`; `author-tracerca/design.md`; `results/T-032/thiet-ke-phep-doi-011.md`; ledger `/h6_pair_audit`, `/pattern_candidate`. BOCPD: `D:/RCA-ext/src/baro/baro/_bocpd.py` (BARO `e35f4ec`), `results/T-033/scripts/bocpd_core.py`, `src/p3/adapters/phat_hien.py` (`diem_doi_tu_R`), `zero-lineage-summary-001.json`. Bốn NPZ nguồn của E2 có sẵn trên laptop dưới `results/T-033/runs/checkpoint-handoff-001/artifacts/runs/` (`bocpd-rest-001/<ca>--full.npz`, `bocpd-factorial-rest-001/<ca>--PF.npz`); mỗi NPZ chứa X, times, columns, R, m, CP_flags, predictive_density, normalizer.
- 12:24 — Kiểm chỉ đọc hai EC2 qua SSH (cấu hình kết nối tham khảo từ `root_remote.py` và `t33/controller.py`, giữ `StrictHostKeyChecking=yes`, không xuất nội dung khóa). EC2 T-032 `3.26.62.217`: 2 CPU, load 0,0, MemAvailable 7.387.197.440 byte, đĩa trống 20.148.215.808 byte, không có tiến trình nghiên cứu. EC2 T-033 `3.107.246.249`: kết nối được, không có tiến trình nghiên cứu (dòng tài nguyên bị cắt khỏi đầu ra, sẽ đo lại trước khi dùng). Cả hai chưa có `/home/ubuntu/rca/T-034/`. Không start/stop máy.

**Tự kiểm SPEC trước triển khai (bước 0 của SPEC).** Đối chiếu mục tiêu, thiết kế, phép phân xử, phạm vi và tiêu chí xong với DT18, hướng dẫn của cô, MRP §2–§7, PLAN §8, WHY-01, quyết định hiện hành và bằng chứng mới nhất. Kết luận: **không thấy lỗi hoặc mâu thuẫn chặn** mục tiêu, phép phân xử hay kết luận; tiếp tục phần đã duyệt. Sáu điểm ghi nhận, không điểm nào đòi sửa SPEC:

1. *Điều kiện bắt đầu.* T-032 đóng 13/10 (Q-145), T-033 đóng 11/10 (Q-140): đạt. Dòng STATE của hai task còn câu “bổ sung Q-144 … chờ Minh xem báo cáo”. Gói bổ sung Q-144 không có bản ghi nghiệm thu riêng và chưa qua phản biện chính thức; gói đính chính bảy file thì Minh đã duyệt (“DUYỆT SỬA NHƯ ĐỀ XUẤT:”). SPEC T-034, duyệt sau đó, nêu đích danh gói bổ sung và bản đính chính là nguồn bắt buộc. Xử lý: dùng số của gói bổ sung theo SPEC, luôn kèm giới hạn và ghi đúng là “báo cáo người làm, có audit hỗ trợ”; nêu điểm này ở §8 của gói để Minh biết.
2. *Năm đầu ra P4 (MRP §7, “Cách dùng G2”).* Mẫu dòng K3 trong SPEC không liệt kê riêng cột “loại nguồn hạn chế” (dữ liệu / giao thức / bản cài / cách tính; AGENTS 3.17, MRP P4 mục 2–3). SPEC nêu các trường tối thiểu và không cấm thêm. Xử lý trong phạm vi: thêm cột loại nguồn vào K3 và một bảng ở K1 nối năm đầu ra P4 với các mục của gói.
3. *E1, “các cấu hình ngưỡng 1 và 3 đã có”.* Pipeline cũ (bản cài theo lời văn) lưu ba nhánh: `to_p` (cờ lời gọi ở 1 lần độ lệch chuẩn, thời lượng span phía gọi), `to_p3` (3 lần), `to_c` (1 lần, thời lượng span phía được gọi). Ở mã tác giả, “ngưỡng 1 và 3” là ngưỡng chọn đặc trưng, một tham số khác. Cách hiểu khai trước khi chạy: bản giữ nguyên tái lập cả ba nhánh đã lưu; can thiệp báo cho `to_p` (nhánh chính, nơi định nghĩa quan hệ cũ) và `to_p3`; `to_c` báo phụ vì cùng trung gian, không dùng để đếm kết luận chính. Số mã tác giả (ngưỡng chọn đặc trưng 1 và 3, đơn vị ms) đặt riêng.
4. *E2, FF/PF.* FF là chuỗi full 1.441 điểm (36 cột ở cả hai ca); PF là nhánh tiền tố 720 điểm với mặt nạ cột của tiền tố (30 cột) và thang full. Đúng với `zero-lineage-summary-001.json#/cases/*/source_FF`, `/source_PF`.
5. *K7, câu về Sock Shop và LEMMA-RCA.* Nguồn cần (gói G1 `results/T-021/goi-g1.md`, thẻ T-019, T-011, WHY-21) không nằm trong danh sách “Đầu vào” của SPEC. Đọc chỉ đọc là đủ để trả lời câu SPEC yêu cầu; dẫn nguồn đầy đủ.
6. *Số của K4 trong SPEC* (16 / 21 / 15 trên 52 ca) khớp `results/T-032/nguyen-nhan-xep-hang.md` mục 5.4 (0+16, 21+0, 9+6); sẽ kiểm lại từ JSON nguồn trước khi dùng.

- 12:26 — V1 lượt 001 (`results/T-034/scripts/v1_kiem_nguon.py` → `results/T-034/runs/v1-001-truoc-noi-why/v1.json`): hai cây bổ sung 6.224/6.224 file khớp `manifest-final.json` (882.842.856 byte, 4,7 giây); gói đính chính 3/3 file; kết quả cũ theo `old-files-before.json`: 18.016/18.016 file của T-006…T-033 (trừ T-032) và `src/`, 531/531 file T-032 được dùng; 0 lệch, 0 thiếu. Tài liệu chỉ nối: phần đầu của WHY, DECISIONS, LOG T-032, LOG T-033 khớp mọi chứng nhận. Phần nối sau chứng nhận mới nhất: DECISIONS 443 byte (dòng Q-145, lời Minh “ĐÓNG T-032”); LOG T-032 1.985 byte (mục “Đóng task”); WHY và LOG T-033 không có phần nối thêm. **Lượt này ghi trạng thái FAIL** vì một dòng: `source_pins` của gói đính chính ghim `tasks/T-034-g2-goi-trinh/SPEC.md` ở bản nháp 09/10 (17.068 byte), còn bản đang dùng là SPEC đã duyệt 13/10 (53.557 byte). Đây không phải hỏng nguồn: SPEC quy định tài liệu khung và SPEC ghim theo phiên bản đang dùng. Giữ lượt 001; sửa script để báo riêng tài liệu khung có trong `source_pins`, chạy lại thành lượt 002.
- 12:30 — V1 lượt 002 → `results/T-034/runs/v1-002-truoc-noi-why/v1.json`: **PASS**. Nhóm bất biến: 6.224 + 3 + 27 + 18.016 + 531 file khớp, 0 lệch, 0 thiếu. Bốn tài liệu chỉ nối: phần đầu khớp mọi chứng nhận. Tài liệu khung có trong `source_pins` báo riêng ở `/frame_docs_in_review_pins`: MRP, LESSONS, DT18, lời cô trùng bản ghim; SPEC T-034 khác bản nháp cũ như đã giải thích. Phiên bản khung đang dùng ghim ở `/frame` (WHY trước nối: 150.070 byte, `2b2893e4…`; STATE trước sửa: 11.205 byte, `d67a0bda…`; SPEC T-034: 53.557 byte, `e849b88f…`; AGENTS trùng chứng nhận 13/10). STATE khác chứng nhận 13/10 vì dòng T-032 đã chuyển “Xong” khi đóng task; không phải file chỉ nối nên chỉ ghim. Nguồn ngoài: B16 (`flash-ticket-platform` HEAD `98d5ad55…`), `_bocpd.py` và `utility.py` của BARO `e35f4ec1…`.
- 12:31 — Nối WHY-51 vào cuối `docs/WHY.md`: nguyên văn khối ```markdown của Phụ lục SPEC (5.744 byte, `dfca21a8…`), gồm cả mục “Bổ sung WHY-51 — Hai phép phân xử trong T-034”. Trước khi nối đã kiểm: V1 đạt, WHY trùng bản ghim, chưa có mã WHY-51 trong file. Sau nối: 155.815 byte, `eb860b7d…`; 150.070 byte đầu giữ nguyên; phần nối trùng từng byte với phụ lục. Biên nhận: `results/T-034/runs/why-51-noi-001/receipt.json`. Không sửa mục WHY nào khác.
- 12:32 — Thêm riêng dòng T-034 vào bảng của `docs/STATE.md` (sau dòng T-033). Kiểm: bỏ dòng mới thì file trùng từng byte với bản trước (11.205 byte, `d67a0bda…`). Không sửa dòng task khác.
- Ghi chú về giờ: ba dòng 12:30–12:32 ở trên ghi sớm hơn đồng hồ một hai phút; từ đây giờ lấy từ lệnh `date`.
- 12:35 — Viết `results/T-034/thiet-ke-hai-phep-kiem.md` **trước khi chạy nhánh đổi** (bản đầu: `749090a5…`). Nội dung: nguồn, 13 cặp/11 ca của E1 và bốn chuỗi của E2, yếu tố giữ/đổi, kiểm tương đương và dung sai, bảng diễn giải, dự đoán của người làm, máy và dự toán. Trước khi viết đã đọc lại Mục III-B, III-C của bài TraceRCA (PDF cùng mã băm `771c24d0…` với bản T-032 đã đọc; chữ trích bằng `pdftotext`, để ngoài repo). Điều xác minh được: bài viết điểm dịch vụ là giá trị lớn nhất qua **mọi** tập nghi ngờ chứa nó; mã tác giả chỉ chấm tập một dịch vụ. Vậy bản cài theo lời văn khớp bài ở điểm này; không có căn cứ gọi quy tắc “chấm qua mọi tập” là lỗi cài bài.
- 12:38 — Chọn máy. E1: EC2 T-032 (bảng span đã phát lại và môi trường ở đó). E2: EC2 T-033 thay cho laptop, vì bốn NPZ nguồn có sẵn tại chỗ với cùng mã băm, đó là máy đã tạo bản gốc, và laptop chỉ còn 2.460.979.200 byte RAM trống (đo 12:34). EC2 T-033 đo lại: 2 CPU, load 0,0, MemAvailable 7.481.065.472 byte, đĩa trống 1.319.153.664 byte; Python 3.12.3, NumPy 1.26.4, SciPy 1.14.1, mpmath 1.3.0; `_bocpd.py` tại `/home/ubuntu/rca/T-025/src/baro` có mã băm `4a57fde3…` (trùng laptop và bản T-033 đã ghim).
- 12:40 — E1: tạo `/home/ubuntu/rca/T-034/e1/` trên EC2 T-032; chuyển `e1_pattern_rule.py` (`01852d2d…`), ledger đính chính (`03606df0…`) và bản thiết kế; mã băm hai đầu khớp. Bảy file nguồn T-032 trên EC2 trùng bản ghim (script, ba module, `cases.json`, `summary.json`, bảng nối).
- 12:41 — **E1 lượt 001 chạy xong** (EC2, `runs/e1-001`, exit 0, khoảng 30 giây máy, RSS đỉnh 1.211.668 KB, đầu ra 6.030.494 byte). Fixture đạt (12 phép, gồm giá trị tính tay của ví dụ Hình 2 cho cả hai nhánh). **Bản giữ nguyên trùng `cases.json` cũ ở 11/11 ca, 0 khác biệt** trên mọi trường. Mọi phép kiểm của bản instrument đạt ở mọi nhánh có điểm (điểm và pattern tốt nhất của nhánh A trùng hàm gốc; bản tính lại độc lập trùng tập phổ biến, tập `top` và điểm hai nhánh). `interpretable = true`. Đưa về `results/T-034/runs/e1-001/` (`out/`, `launch/`), 22/22 file khớp mã băm hai đầu; gói `remote.tar.gz` `a6ca6885…`.
- 12:45 — E2, fixture trên laptop lượt 001: F1 và F3 đạt; **F2 không đạt điều kiện hợp lệ** (bản gốc không có trạng thái nào về 0; khối lượng nhỏ nhất của tham chiếu e^−126). Lỗi thiết kế fixture, không phải lỗi phép tính. Giữ lượt lỗi ở `results/T-034/runs/e2-fixtures-laptop-001-fail/`. Thử thêm ba cấu hình dữ liệu (không lưu file): nhảy theo cấp số nhân làm mã gốc báo `LinAlgError`; d = 3–8 với đoạn ngắn không tạo underflow. Cấu hình đạt: 200 điểm mức 0, 15 điểm mức 40, 15 điểm mức −40, d = 2.
- 12:48 — E2, fixture laptop lượt 002 (`runs/e2-fixtures-laptop-002/`): F1, F2, F3 đạt. F1: `exp(logpdf)` trùng `pdf` gốc từng bit; lệch posterior lớn nhất 7,1e-14; lệch tham chiếu mpmath 7,8e-14. F2: bản gốc có 2.335 trạng thái bằng 0, bản miền log lệch tham chiếu 5,4e-10, MAP và CP trùng. F3 (đối chứng dương): bản gốc cho CP [4], tham chiếu và bản miền log cho [4, 7]. Nối **Mục nối 1** vào bản thiết kế (đổi dữ liệu F2; bản thiết kế sau nối `61bacbc5…`), trước khi chạy bốn chuỗi thật.
- 12:49 — E2: tạo `/home/ubuntu/rca/T-034/e2/` trên EC2 T-033; chuyển `e2_bocpd_log.py` (`6dbe17c7…`), `zero-lineage-summary-001.json` (`1f407781…`) và bản thiết kế; mã băm hai đầu khớp. Fixture trên EC2 (`runs/e2-fixtures-ec2-001`): F1, F2, F3 đạt, 13,1 giây.
- 12:49 (05:49:37Z) — **Khởi chạy E2 lượt 001** trên EC2 T-033, hai tiến trình nền bằng `nohup` (PID 58899, 58902), mỗi tiến trình một ca: PF trước, FF sau; mỗi chuỗi sham rồi miền log; `OPENBLAS_NUM_THREADS=1`. Lệnh và mã băm nguồn ở `/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/` (`run-<ca>.sh`, `pins.txt`). Tiến độ: `…/e2-001-launch/<ca>--<nhánh>.out` và `runs/e2-001/<ca>--<nhánh>--progress.jsonl`. Xem bằng: `ssh … ubuntu@3.107.246.249 'tail -n 2 /home/ubuntu/rca/T-034/e2/runs/e2-001-launch/*.out; cat /home/ubuntu/rca/T-034/e2/runs/e2-001-launch/*.done.txt'`. Tiến trình không phụ thuộc phiên SSH hay laptop; laptop chỉ cần để thu kết quả. Pilot đo được: sham PF tới bước 500/720 sau 37 giây, RSS 119 MB.
- 12:55 — K2: viết `results/T-034/scripts/k2_bang_baseline.py`. Bảng lấy nguyên số của `results/T-024/cham-a.json`, `results/T-025/phat-hien.json`, `cham-b.json`, `results/T-026/cham-a.json`, `results/T-029/a-so-b.json`, `fast-summary-001.json` (T-033). **V2 đạt, 0 lệch** (dung sai 1e-12): số tổng xếp hạng tính lại từ bản ghi từng lượt cùng file nhãn bằng một bộ chấm viết riêng (RE2-TT dev30 và dev19, Nezha-OB main; 6 phương pháp; TORAI 3 seed); P/R/F1, báo động sai mỗi giờ và độ trễ tính lại từ `results/T-025/bao-dong.json` theo quy tắc cửa sổ 60 giây; thành công chung chế độ (b) và bảng G tính lại từ bảng theo ca; nhánh mã tác giả TraceRCA tính lại từ 208 hàng Full008 và khớp ledger. Hai lượt thử đầu của script dừng vì lỗi của script (N-Sigma không lưu `chi_so`; mục `tren_ca_t_hat_dung` rỗng khi không có báo động đầu đúng); đã sửa, không ảnh hưởng số.
- 13:05 (06:04:46Z) — **E2 lượt 001 xong** (EC2 T-033; mỗi chuỗi PF khoảng 150 giây, FF khoảng 750 giây; RSS đỉnh 247 MB; đầu ra 1,08 MB). Đưa về `results/T-034/runs/e2-001/` (`out/`, `launch/`, `fixtures-ec2/`), 36/36 file khớp mã băm hai đầu; gói `f06e32a9…`. Kết quả thô, **chưa dùng để kết luận**:
  - sham của bốn chuỗi trùng `m`, `CP_flags`, `maxes` với bản lưu; R không trùng từng bit; lệch tương đối lớn nhất 4,3e-11 (3ae-PF), 7,0e-11 (3ae-FF), 8,9e-11 (ba83-FF), **2,1e-9 (ba83-PF, vượt dung sai 1e-9 đã khai → chuỗi này không đạt sham ở lượt 001)**;
  - bản miền log: `m` và CP trùng bản gốc ở 3ae-PF, ba83-PF, ba83-FF; **khác ở 3ae-FF**: `m` khác tại 12 chỉ số 752–763; CP bản gốc có 755, bản miền log có 752, 760, 764; các CP khác trùng. Trái dự đoán tôi ghi trong thiết kế.
- 13:03 — Nối **Mục nối 2** vào thiết kế (trước khi thấy kết quả miền log của hai chuỗi FF): giả thuyết về nguyên nhân lệch sham, phép kiểm tất định, phép đo theo lịch sử dòng dõi. Script v2 sinh bằng `scripts/make_e2_v2.py`.
- 13:08 (06:09:34Z) — Phép kiểm tất định `e2-determinism-001` trên EC2 T-033: không đặt biến luồng (OpenBLAS 2 luồng, như lượt gốc T-033) thì density 720/720 hàng và R trùng bản lưu **từng bit** ở cả hai chuỗi PF; đặt 1 luồng thì density lệch từ bước 1 và R trùng 55%, lặp lại cho cùng kết quả. Nguyên nhân lệch sham của lượt 001: tôi đặt `OPENBLAS_NUM_THREADS=1`, khác cấu hình nguồn.
- 13:12 — Script v3 (`scripts/make_e2_v3.py` → `e2_bocpd_log_v3.py`, `2206b495…`): thêm tham chiếu độc lập bằng số thực mở rộng 80 bit (đệ quy tuyến tính như mã gốc, không logsumexp), khối lượng ở trạng thái bị underflow ảnh hưởng, đoạn phân kỳ, lớp “hệ quả sau underflow”. Fixture v3 trên EC2: lượt 002-v3 và 003-v3 **không đạt F4** (tham chiếu mở rộng lấy `exp` ở float64, pdf của F2 tự về 0; lượt 003 chạy lại nhầm bản chưa sửa vì lệnh vá script hỏng); lượt 004-v3 đạt F1–F4. Giữ cả ba.
- 13:13 — Nối **Mục nối 3** vào thiết kế (bản sau nối `96fbf6de…`), chuyển lên EC2.
- 13:13 (06:13:44Z) — **Khởi chạy E2 lượt 002** trên EC2 T-033 (PID 60980, 60983), script v3, không đặt biến luồng. Mỗi chuỗi: sham → miền log → tham chiếu mở rộng. Dự toán khoảng 35 phút chờ, khoảng 66 phút máy. Xem tiến độ: `ssh … ubuntu@3.107.246.249 'cat /home/ubuntu/rca/T-034/e2/runs/e2-002-launch/*.done.txt; tail -n 1 /home/ubuntu/rca/T-034/e2/runs/e2-002-launch/*.out'`. Tiến trình không phụ thuộc phiên SSH hay laptop.
- 13:19 (06:18:46Z) — E2 lượt 002, **hai chuỗi PF xong** (mỗi chuỗi khoảng 300 giây, RSS đỉnh 154 MB). Sham trùng bản lưu **từng bit** ở cả hai (R, `m`, CP, `maxes`). Tham chiếu số thực mở rộng trùng bản miền log (`m`, CP trùng; lệch log lớn nhất 1,16e-11 và 1,09e-11, ngưỡng 1e-8). `m` và CP của bản miền log trùng bản gốc ở cả hai chuỗi.
- 13:27 (06:27:20Z) — **Dừng hai chuỗi FF của lượt 002** khi còn ở bước sham. Lý do: hai tiến trình, mỗi tiến trình 2 luồng OpenBLAS, trên máy 2 CPU (load 4,0); sham FF mới tới bước 500 sau 459 giây (lượt 001: khoảng 45 giây); dự phóng cả lượt trên 3 giờ, vượt ngưỡng 1 giờ của AGENTS 3.8. Lỗi điều phối của tôi (dự toán suy từ chuỗi d = 1). Ghi `INTERRUPTED-FF.txt` trong `…/e2-002-launch/`. Phần FF dở dang giữ nguyên, không dùng; chưa có kết quả nhánh đổi nào của FF ở lượt này.
- 13:27 (06:27:36Z) — **Khởi chạy E2 lượt 003** trên EC2 T-033 (PID 61734): hai chuỗi FF chạy lần lượt trong một tiến trình nền, script v3, không đặt biến luồng. Lệnh và mã băm nguồn: `/home/ubuntu/rca/T-034/e2/runs/e2-003-launch/` (`run.sh`, `pins.txt`). Số đo đầu lượt: sham tới bước 1.000 sau 152 giây, RSS 144 MB; dự phóng khoảng 20 phút mỗi chuỗi. Xem tiến độ: `ssh … ubuntu@3.107.246.249 'cat /home/ubuntu/rca/T-034/e2/runs/e2-003-launch/done.txt; tail -n 1 /home/ubuntu/rca/T-034/e2/runs/e2-003-launch/*.out'`. Tiến trình không phụ thuộc phiên SSH hay laptop.
- 13:31 — Đưa về laptop, kiểm mã băm hai đầu: `e2-002` (12 file `out/` + 17 file `launch/`), `e2-determinism-001` (14 file), ba lượt fixture v3 trên EC2 (`e2-fixtures-ec2-002-v3-fail`, `003-v3-fail`, `004-v3`; mỗi lượt 2 file). Tất cả khớp. Danh sách mã băm phía EC2 và gói tar nằm cạnh từng thư mục `results/T-034/runs/<lượt>/`.
- 13:32 — Nối **Mục nối 4** vào thiết kế (dừng FF của lượt 002, chạy lại tuần tự; không đổi nội dung khoa học). Bản sau nối: `3f3bc939…`.
- 13:33 — Đã viết, **chưa chạy**: `scripts/g2_lib.py` (sổ số liệu: file + con trỏ JSON → giá trị), `g2_ban_do.py`, `g2_ban_do_rows.py` (26 hàng bản đồ), `g2_extra_facts.py`, `hai_phep_kiem_build.py` (gom E1/E2, tính V6/V7).
- 13:36 — K2, lượt chính thức `results/T-034/runs/k2-001/`: **V2 đạt, 0 lệch**; nội dung trùng lượt thử (chỉ khác thời điểm tạo). Chép thành `results/T-034/bang-baseline.json` (`e5c6b015…`).
- 13:43 (06:42:46Z) — E2 lượt 003, chuỗi full của `dev-3ae0a6c15a` xong (909 giây, RSS đỉnh 277 MB). Bản giữ nguyên trùng bản lưu **từng bit**. Tham chiếu số thực mở rộng trùng bản miền log (MAP, CP trùng; lệch log lớn nhất 1,3e-10, ngưỡng 1e-8) và **khác bản gốc** ở 12 chỉ số 752–763. CP: bản gốc có 755; bản miền log có 752, 760, 764; mọi CP khác trùng. Vậy khác biệt thấy ở lượt 001 được xác nhận dưới cấu hình của nguồn và bằng một phép tham chiếu độc lập.
- 13:44–13:57 — Trong lúc chờ: viết `scripts/g2_blocks.py` (bảng sinh tự động), `g2_doc_facts.py`, `g2_render.py`, `v4_kiem_so.py`, `e2_gom_luot_dung.py`, `manifest_cuoi.py`; hai bản mẫu `scripts/mau/goi-g2.md`, `scripts/mau/hai-phep-kiem.md`. Đọc lại: `docs/review-prompt.md`; MRP §2–§7; bản đối chiếu đính chính 13/10; `closure-ledger.json` (26 câu hỏi) và `closure-ledger-review-001.json`; T-032 mục 5–8; gói G1 (`results/T-021/goi-g1.md`), thẻ T-019, T-011; chuẩn B16; T-006, T-007, T-017 (trạng thái tái lập); `results/T-032/thiet-ke-phep-doi-009.md` (định nghĩa hai nhánh bộ chia) và `thiet-ke-bang-mo-ta-004.md` mục 5b (định nghĩa lời gọi chậm).
- 13:58 (06:58:05Z) — **E2 lượt 003 xong** cả hai chuỗi FF (chuỗi thứ hai 918 giây; cả lượt 31 phút, dưới một giờ). Chuỗi full của `dev-ba831dbeb8`: bản giữ nguyên trùng từng bit; MAP và CP của bản miền log trùng bản gốc. Đưa về `results/T-034/runs/e2-003/` (`out/` 8 file, `launch/` 9 file, khớp mã băm hai đầu).
- 13:58 — Gom lượt dùng để kết luận: `scripts/e2_gom_luot_dung.py` → `results/T-034/runs/e2-used-001/` (22 file chép nguyên, có manifest): PF từ `e2-002`, FF từ `e2-003`, ví dụ nhỏ từ `e2-fixtures-ec2-004-v3`, phép kiểm tất định từ `e2-determinism-001`.
- 13:58 — `scripts/hai_phep_kiem_build.py` → `results/T-034/hai-phep-kiem.json`. **V6 đạt** (ví dụ nhỏ; bản giữ nguyên 11/11 ca, 0 khác biệt; 28/28 kết quả nhánh có điểm qua kiểm độc lập; đủ 13 cặp × 3 nhánh; điểm nhánh chỉ tập một dịch vụ không bao giờ cao hơn nhánh mọi tập; quan hệ nhánh mọi tập trùng quan hệ cũ trong ledger). **V7 đạt** (F1–F4; đủ bốn chuỗi; bản giữ nguyên trùng từng bit 4/4; tham chiếu mở rộng 4/4; hữu hạn và chuẩn hóa ở mọi cột; trạng thái sạch trước khi underflow có khối lượng lệch nhiều nhất 2,2e-11; không có chỗ MAP khác nào không giải thích được; đối chiếu phép cũ của T-033 lệch nhiều nhất 1,2e-12).
- 13:58 — Nối **Mục nối 5** vào thiết kế: đính chính câu “d = 1” của Mục nối 4 (và của dòng LOG 13:27): chuỗi PF có T = 720, d = 30; chuỗi FF có T = 1441, d = 36. Vì sao chỉ chuỗi FF chậm mười lần khi hai tiến trình chạy cùng lúc: chưa kiểm, không ảnh hưởng kết quả. Bản thiết kế sau nối: `520068d0…`.
- 13:59 — K3: `scripts/g2_ban_do.py` → `results/T-034/runs/g2-build-001/ban-do-g2.json` (26 dòng G2-H01…G2-H26; chép thành `results/T-034/ban-do-g2.json`). Lần chạy thử đầu (`runs/g2-try/`) lộ 13 con trỏ JSON sai trong script; đã sửa. **V3 đạt**: 68/68 mã gốc và 26/26 dòng của sổ đối chiếu có chỗ; ba mã ở danh sách “không đưa vào” kèm lý do. Tổng theo ô của mỗi (dataset, phương pháp) khớp số của T-028.
- 13:59–14:01 — Dựng `goi-g2.md` và `hai-phep-kiem.md` (`scripts/g2_render.py`), chạy V4 (`scripts/v4_kiem_so.py`). Lần đầu **V4 hỏng: 112 chữ số không qua sổ** (chủ yếu “hạng 1”, số mục, tham số viết bằng chữ số, mã trạng thái HTTP); không có số kết quả nào viết tay. Sửa văn bản và danh sách lớp được phép, còn 2, rồi **0**. Các lần dựng ghi đè trong cùng thư mục `g2-build-001`; không giữ bản trung gian của văn bản.
- 14:02–14:05 — V5: đọc lại toàn văn hai file đã dựng, đối chiếu nguồn. Sửa mười chỗ (danh sách ở `results/T-034/runs/g2-build-001/v5-kiem-lap-luan.md` mục 2), trong đó có bốn chỗ tôi viết sai hoặc mạnh hơn nguồn: ba biến thể CIRCA bị trộn; số ca “root không được gọi” đếm sai trong bản dẫn xuất đầu; nghĩa của hai nhánh bộ chia MicroRank tự đoán từ tên khóa; câu “lan không giải thích phần lớn ca sai của MicroRank” mạnh hơn T-032 mục 5.2. Dựng lại; **V4 đạt**: 2.427 số, 35 file nguồn, 0 lệch, 0 chữ số không nguồn.
- 14:09 — **V1 lượt 003** (`results/T-034/runs/v1-003-cuoi/`): **đạt**. Nguồn bất biến không đổi (6.224 + 3 + 27 + 18.016 + 531 file). WHY: phần nối sau chứng nhận mới nhất đúng 5.745 byte, trùng biên nhận WHY-51. So tài liệu khung giữa lượt 002 và 003: chỉ `docs/WHY.md` và `docs/STATE.md` khác, đúng hai thay đổi được phép.
- 14:09 — Kiểm hai EC2 (chỉ đọc): không file nào ngoài `/home/ubuntu/rca/T-034/` có thời điểm sửa sau 05:20Z hôm nay; không còn tiến trình của T-034. Dung lượng đã ghi: EC2 T-032 6,3 MB; EC2 T-033 2,0 MB. Đĩa trống EC2 T-033: 1.320.534.016 byte.
- 14:10 — Manifest: `results/T-034/runs/manifest-cuoi-001/manifest.json` (225 file, 12.665.917 byte dưới `results/T-034/`, chưa gồm chính thư mục manifest). `git status` của các file đã theo dõi giống hệt đầu phiên; HEAD vẫn `6c93e6d`. Không commit, không push.

**Quyết định của Minh trong phiên:** không có quyết định mới. Lời duyệt dùng cho phiên này là ba lời đã ghi nguyên văn trong SPEC (và chép ở đầu mục này). Chưa có dòng nào trong `docs/DECISIONS.md` cho các lời duyệt đó; đề xuất dòng ghi nằm ở báo cáo cuối lượt trong chat, chờ Minh.

**Kết thúc phiên:**

1. **Đã làm gì.** Bước 0–6 của SPEC:
   - Tự kiểm SPEC (không có lỗi chặn; sáu ghi chú); V1; nối WHY-51; thêm dòng T-034 vào STATE.
   - E1 và E2: thiết kế viết trước nhánh đổi (bản đầu và năm mục nối), chạy trên hai EC2 có sẵn, đưa về laptop có kiểm mã băm hai đầu. Giữ mọi lượt lỗi.
   - K2 (`bang-baseline.json`), K3 (`ban-do-g2.json`), K1 và K4–K7, mục 8 (`goi-g2.md`); báo cáo hai phép (`hai-phep-kiem.md`, `.json`).
   - Kiểm V1–V7.
2. **File đã thay đổi.**
   - Tạo: mọi file dưới `results/T-034/` (danh sách và mã băm ở `results/T-034/runs/manifest-cuoi-001/manifest.json`); `tasks/T-034-g2-goi-trinh/LOG.md`.
   - Sửa: `docs/WHY.md` (chỉ nối WHY-51 nguyên văn từ Phụ lục SPEC; biên nhận `results/T-034/runs/why-51-noi-001/receipt.json`); `docs/STATE.md` (chỉ dòng T-034).
   - Trên EC2: chỉ dưới `/home/ubuntu/rca/T-034/` ở cả hai máy.
   - Không sửa: SPEC, MRP, PLAN, DECISIONS, LESSONS, kết quả task khác, `src/`, `data/`. Không mở `data/locked/`. Không commit, không push.
3. **Kiểm tra đã chạy và kết quả.**
   - V1: đạt ở đầu phiên (lượt 002, sau khi sửa cách báo của lượt 001) và ở cuối phiên (lượt 003).
   - V2: đạt, 0 lệch (`runs/k2-001/`, trường `/v2` của `bang-baseline.json`).
   - V3: đạt, 68/68 mã gốc, 26/26 dòng sổ đối chiếu (`ban-do-g2.json#/v3`).
   - V4: đạt, 2.427 số, 0 lệch, 0 chữ số không nguồn (`runs/g2-build-001/v4.json`). Giới hạn: số viết bằng chữ và chữ số trong đoạn mã không được quét.
   - V5: đã đọc và sửa mười chỗ (`runs/g2-build-001/v5-kiem-lap-luan.md`). Đây là tự kiểm của người viết.
   - V6: đạt (`hai-phep-kiem.json#/E1/v6`). V7: đạt (`hai-phep-kiem.json#/E2/v7`).
4. **Điều chưa chắc hoặc cần Minh quyết.**
   - *Đầu ra task đạt gì:* đủ các file của mục “Đầu ra” trong SPEC; K1–K7 có trong `goi-g2.md`; K7 có 15 câu; mỗi dòng bản đồ có mức, nguồn con, giải thích khác, lời tác giả, bảng theo ô (Phụ lục A, B) hoặc lý do không tách.
   - *Câu hỏi nguồn trả lời tới đâu.* RQ1 (trên dev): có bảng theo ô cho hai dataset và hai chế độ. RQ2: phần lớn nhóm sai của các phương pháp xếp hạng đã lần tới bước gây ra ở mức can thiệp; **chưa** phân xử: vì sao hai bộ phát hiện báo trước mốc; vì sao dịch vụ không liên hệ đổi tại mốc; phần ca sai còn lại của MicroRank; câu “lan có đáng kể” (bằng chứng nghiêng về không chiếm đa số, chưa thành tỷ lệ). Gói không trả lời RQ3; chỉ trình mười ứng viên có dự đoán bác bỏ được.
   - *E1:* trả lời được câu đã giao trong 13 cặp: ở cờ một lần độ lệch chuẩn, quy tắc chấm qua tập nhiều dịch vụ không phải bước đưa dịch vụ gọi lên trên root (1/7 và 0/3 cặp đổi chiều); ở cờ ba lần thì có (4/5 cặp Nezha-OB). **Chưa** xác định bước nào gây chênh giữa bản theo lời văn và mã tác giả ở cờ một lần; hai ứng viên từ trung gian (cờ ở lời gọi đi ra của frontend; bước chọn tập ở RE2-TT) chưa được can thiệp.
   - *E2:* trả lời được câu đã giao trên bốn chuỗi: underflow có đổi MAP và điểm đổi ở một chuỗi (12 bước, trong 45 giây đầu sau mốc), không đổi báo động đầu hay điểm đổi trước mốc ở chuỗi nào. **Chưa biết** ở 28 ca dev còn lại. Phép cũ của T-033 (giữ hệ số chuẩn hóa) không được đọc rộng thành “underflow không đổi MAP trên cả chuỗi”.
   - *Phần còn kiểm được trên dev, chưa được giao* (mục 6.1 của gói): đổi riêng bước chọn tập của TraceRCA; đối chiếu cờ theo lời gọi; chạy miền log trên các ca còn lại (mỗi chuỗi full khoảng 15 phút máy, cả lượt hơn một giờ, cần duyệt riêng); hoàn thiện nháp nhãn lan.
   - *Cần Minh quyết:* mười điểm ở mục 8 của `goi-g2.md`. Trong đó: duyệt cổng G2; nhánh TraceRCA mã tác giả; nhãn lan; cách trình bốn ca ERROR; TORAI nguồn B; dòng độ nhạy MicroRank; các phép sau E1/E2; dòng DECISIONS cho lời duyệt T-034; nội dung đề nghị cho P9a.
   - *Điều tôi chưa chắc:* (i) thang mức bằng chứng là quy ước; ranh giới CT/ĐC ở vài dòng có thể bị tranh luận, nên mỗi dòng ghi mức của từng nguồn con. (ii) Diễn giải của các dòng bản đồ dựa trên báo cáo của T-028, T-029, T-032, T-033 và gói đính chính; tôi đối chiếu số và trạng thái, không đọc lại mã của mọi phép đổi cũ. (iii) Danh sách lớp chữ số được phép của V4 do tôi đặt sau khi thấy lượt V4 đầu; không có số kết quả nào nằm trong các lớp đó, nhưng người phản biện nên xem `v4.json#/allow_classes`. (iv) Nháp nhãn lan ở mục 4.3 dùng số đo có sẵn của T-032; tôi không đo thêm độ nhạy.
   - *Phản biện:* chưa có lượt phản biện kết quả nào. Đề xuất chuyển prompt dưới đây cho Codex; Minh quyết gửi hay dừng. Task **chưa đóng**.
5. **Bước tiếp theo chính xác.** Minh chuyển prompt ở cuối mục này cho Codex (phiên mới trong `D:\RCA-flashticket`). Người phản biện bắt đầu từ `results/T-034/goi-g2.md`, `results/T-034/hai-phep-kiem.md`, rồi `results/T-034/runs/g2-build-001/v4.json` và `render/registry.json`. Chạy lại phép kiểm rẻ (chỉ đọc), từ gốc repo, bằng môi trường `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8`:
   - `results/T-034/scripts/v4_kiem_so.py results/T-034/runs/g2-build-001` (ghi đè `v4.json` trong thư mục lượt);
   - `results/T-034/scripts/k2_bang_baseline.py <thư mục lượt mới>` (V2; script tự tạo thư mục, không ghi đè lượt cũ);
   - `results/T-034/scripts/hai_phep_kiem_build.py results/T-034/runs/e1-001 results/T-034/runs/e2-used-001 results/T-034/runs/e2-001 <file ra mới>` (V6, V7).
   Nếu Minh duyệt gói: đề xuất commit ở báo cáo cuối lượt; sau đó đề xuất dòng DECISIONS và cập nhật PLAN/STATE.
6. **Lệnh cuối cùng đã chạy.** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-001` (laptop). Lệnh nghiên cứu cuối trên máy xa: `runs/e2-003-launch/run.sh` trên EC2 T-033 (đã xong 06:58:05Z). Sau đó chỉ còn nối LOG này và sửa dòng T-034 trong STATE thành “chờ phản biện”.

---

## Prompt bàn giao của lượt này cho agent đối phương (Codex, soát kết quả)

Chép nguyên văn “Prompt chung”, khối “Soát kết quả” và khối “G2” của `docs/review-prompt.md`; chỉ điền thông tin trung tính. Minh quyết copy và gửi; tôi không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, `tasks/T-034-g2-goi-trinh/SPEC.md` (SPEC đã được Minh duyệt và khóa ngày 13/10/2026).
- Công đoạn: soát kết quả.
- Gói/cổng: P3, P4; cổng G2.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện kết quả (theo SPEC).
- Tài liệu gốc: `AGENTS.md`; `docs/STATE.md`; `tasks/T-034-g2-goi-trinh/SPEC.md` và `LOG.md`; `docs/MRP.md`; `docs/PLAN-P3-G2.md`; `docs/WHY.md` (gồm WHY-51; phần nối trong task có biên nhận tại `results/T-034/runs/why-51-noi-001/receipt.json`); `docs/DECISIONS.md`; `docs/LESSONS.md`; `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md`; `docs/reference/sources/advisor-2026-09-23.md`; chuẩn quan sát `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`. Commit gốc: `6c93e6d`; mọi file của T-034 chưa commit. `docs/WHY.md` và `docs/STATE.md` đã có thay đổi chưa commit từ trước phiên T-034; phiên bản trước và sau phần của T-034 được ghim ở `results/T-034/runs/v1-002-truoc-noi-why/v1.json` và `results/T-034/runs/v1-003-cuoi/v1.json` (trường `/frame`).
- Phản biện và phản hồi trước: không có bản phản biện kết quả nào của T-034; thư mục task hiện chỉ có `SPEC.md` và `LOG.md`.
- Code và kết quả liên quan: `results/T-034/`: `goi-g2.md`, `hai-phep-kiem.md`, `hai-phep-kiem.json`, `ban-do-g2.json`, `bang-baseline.json`, `thiet-ke-hai-phep-kiem.md`, `scripts/` (gồm `scripts/mau/`), `runs/`. Manifest: `results/T-034/runs/manifest-cuoi-001/manifest.json`. Sổ số liệu: `results/T-034/runs/g2-build-001/render/registry.json`. Kết quả các phép kiểm: `results/T-034/runs/g2-build-001/v4.json`, `results/T-034/runs/g2-build-001/v5-kiem-lap-luan.md`, `results/T-034/runs/v1-003-cuoi/v1.json`, và các trường `/v2`, `/v3`, `/E1/v6`, `/E2/v7` trong ba file JSON ở gốc `results/T-034/`. Nguồn mà gói dùng: `results/T-024`, `T-025`, `T-026`, `T-028`, `T-029`, `T-032`, `T-033`; manifest của gói bổ sung: `results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json` và `manifest-review-001.json`. Môi trường laptop: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8` (Python 3.12, NumPy 1.26.4, SciPy 1.14.1, mpmath 1.3.0); lệnh chạy lại các phép kiểm ghi ở mục “Bước tiếp theo chính xác” của LOG. Lượt E1 chạy trên EC2 của T-032, lượt E2 trên EC2 của T-033, file đặt dưới `/home/ubuntu/rca/T-034/`; lệnh khởi chạy, mã băm nguồn và mã băm hai đầu nằm trong thư mục `launch/` của từng lượt dưới `results/T-034/runs/` và các file `remote-sha256*.txt` cạnh từng lượt.
- Phạm vi ghi được Minh cho phép trong lượt này: Minh chưa nêu quyền ghi cho lượt này; mặc định chỉ đọc và trả lời trong chat. Nếu Minh cho phép ghi thì chỉ ghi đúng một file `tasks/T-034-g2-goi-trinh/REVIEW.md` (hiện chưa tồn tại) theo `tasks/_MAU/REVIEW.md`; không ghi LOG, STATE; không chạy thực nghiệm mới.

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

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

- 14:12 — Sau mục kết thúc phiên ở trên: sửa riêng dòng T-034 trong `docs/STATE.md` thành “Chờ phản biện”; bỏ dòng đó thì file trùng từng byte với bản trước (kiểm bằng script tạm ngoài repo). Đây là lệnh ghi cuối cùng của phiên.

---

## Phiên 2 — 13/10/2026 — Claude — laptop — vai trò: người làm (đáp phản biện và sửa)

**Mở phiên:** cùng cuộc trò chuyện với phiên 1. Đầu ra phiên 1 còn nguyên: 225 file khớp `runs/manifest-cuoi-001/manifest.json` trước khi sửa.

**Công đoạn:** đáp hai lượt phản biện kết quả của Codex (Minh dán vào chat), rồi sửa theo lời duyệt của Minh. Hai lượt đáp đầu chỉ đọc và trả lời trong chat, đúng phạm vi của prompt; không ghi file ở hai lượt đó.

**Tự soát:** kết luận phản biện đến cùng lúc với prompt, nên tôi không tự soát “mù” được. Các điểm tự tìm thêm khi kiểm trên file: N1 (câu phủ định về E1 còn ở nhiều chỗ hơn reviewer nêu), N2 (cặp đảo chiều là ca đã nhìn trước), N3 (D7, HP-5, HP-9 thiếu diễn giải), N4 (câu về TORAI mạnh hơn nguồn).

**Đánh giá phản biện** (bằng chứng riêng ở hai lượt đáp trong chat):

| Điểm | Kết luận của người làm |
|---|---|
| Lượt 1, finding 1 (CHẶN): E1 loại một cơ chế mà can thiệp đã xác nhận có tác động | Đúng. `hai-phep-kiem.json#/E1/pairs/24` |
| Lượt 1, finding 2: D5 có mã, mất nội dung | Đúng. `trace-root-census-001/summary.json#/cases/14` |
| Lượt 1, finding 3: G2-H15 dẫn một lỗi đã sửa | Đúng. `src/torai/torai_sua.py`, cờ `sua_giam_mau` mặc định bật |
| Lượt 1, finding 4: PF mô tả sai | Đúng. Metadata PF: mặt nạ tiền tố, thang toàn bản ghi |
| Lượt 2, N1: ca `dev-6c9afc9822` vẫn là phép hợp lệ | Đúng; tôi rút chữ “không kiểm được”. `…#/E1/pairs/27` |
| Lượt 2, N2: giữ mức CT, chỉ ghi giới hạn khái quát | Đúng |
| Lượt 2, M6 gắn sai điều kiện | Đúng. `results/T-028/ca-sai.json#/main_rows/213, 214, 239, 261`: cả bốn là trễ mạng |
| Lượt 2, N4: nguồn B dùng quan hệ cha–con khi dựng trace | Đúng. `src/p3/torai_b.py`, hàm `ten_cot` |

Không còn bất đồng nội dung với người phản biện.

**Quyết định của Minh trong phiên** (nguyên lời): “duyệt sửa”, trả lời đề xuất sửa ở lượt đáp thứ hai (sáu mục của lượt đáp đầu đã chỉnh theo N1, N2, cộng năm mục bổ sung). Chưa ghi DECISIONS.

**Diễn biến:**
- Chép bản đang phát hành vào `results/T-034/runs/phat-hanh-001/` (`goi-g2.md` `05180184…`, `hai-phep-kiem.md` `693ac6dd…`, `ban-do-g2.json` `e451498a…`).
- Sửa `scripts/mau/hai-phep-kiem.md`, `scripts/mau/goi-g2.md`, `scripts/g2_ban_do_rows.py`, `scripts/g2_ban_do.py`, `scripts/g2_extra_facts.py`, `scripts/g2_blocks.py`. Các script được sửa tại chỗ; bản trước chỉ còn mã băm trong manifest 001.
- Nối **Mục nối 6** vào `thiet-ke-hai-phep-kiem.md`: đính chính cách tổng hợp ở E1.7 (báo theo ba loại cặp) và giới hạn “ca đã nhìn”. Bản sau nối: `b5a3d789…`.
- Dựng lại vào lượt mới `results/T-034/runs/g2-build-002/`; lượt `g2-build-001` giữ nguyên. **V3 đạt** (M6 chuyển sang G2-H06). **V4 đạt**: 2.434 số, 36 file nguồn, 0 lệch, 0 chữ số không nguồn.
- Viết `runs/g2-build-002/v5-bo-sung-sau-phan-bien.md` (ghi rõ bản V5 đầu đã bỏ sót lỗi E1).
- Manifest `results/T-034/runs/manifest-cuoi-002/manifest.json` (239 file). So với manifest 001: đúng mười file đổi (ba file phát hành, bản thiết kế, sáu file trong `scripts/`), không file nào mất, 14 file mới. `bang-baseline.json` và `hai-phep-kiem.json` không đổi.
- Không kết nối EC2, không chạy thực nghiệm, không sửa STATE, không commit.

**Điều đã đổi trong kết luận** (số cũ giữ nguyên):
- E1, cờ một lần độ lệch chuẩn: không còn viết “không phải bước…”. Viết: quy tắc chấm qua tập nhiều dịch vụ có đóng góp nhưng không đủ. Trong 7 cặp Nezha-OB: 1 cặp đảo chiều (ca đã nhìn trước; mức CT, không suy rộng); 5 cặp điểm dịch vụ gọi giảm mà chưa đảo chiều; 1 cặp giữ nguyên điểm và quan hệ vì root không có tập được chấm.
- PF của E2 không phải tiền xử lý chỉ dùng quá khứ.
- G2-H15: bỏ câu “lỗi giảm mẫu hai lần”; kết luận chỉ về bước RCD. Bỏ câu “TORAI B không dựa vào quan hệ gọi” ở mọi chỗ.
- G2-H19 có nội dung D5 và tách D7 khỏi D3; M6 chuyển về dòng trễ mạng; G2-H21 có diễn giải HP-5, HP-9.

**Kết thúc phiên:**

1. **Đã làm gì:** đáp hai lượt phản biện; sửa theo lời duyệt; dựng lại, kiểm lại.
2. **File đã thay đổi:** mười file dưới `results/T-034/` nêu trên, cộng các file mới của `runs/phat-hanh-001/`, `runs/g2-build-002/`, `runs/manifest-cuoi-002/`; LOG này. Không sửa file nào khác.
3. **Kiểm đã chạy:** V3 đạt; V4 đạt trên lượt 002; so hai manifest; quét lại các câu phủ định về E1 và câu về TORAI trong hai văn bản: không còn.
4. **Điều chưa chắc hoặc cần Minh quyết:**
   - Bản sửa chưa được người phản biện kiểm. Finding CHẶN coi như đã xử lý theo đánh giá của người làm, chưa phải theo người phản biện.
   - Tự kiểm V5 của tôi ở phiên 1 đã không bắt được lỗi E1; tôi chưa soát hết nội dung mọi mã HP và M khác xem có mã nào “đủ mã, thiếu nội dung” như D5, D7, M6.
   - Còn mở, không đổi: bước gây chênh giữa hai pipeline TraceRCA ở cờ một lần; “lan có đáng kể”; onset và nền sạch; underflow ở các ca dev còn lại; lợi ích đồ thị.
   - Mười điểm ở mục 8 của `goi-g2.md` vẫn chờ Minh. Hai dòng DECISIONS (lời duyệt T-034; lời Minh cho Codex dùng subagent) chưa ghi.
   - Dòng T-034 trong STATE vẫn là “Chờ phản biện”; tôi không sửa vì lời duyệt không nêu STATE.
5. **Bước tiếp theo chính xác:** Minh chuyển prompt dưới đây cho Codex để kiểm bản sửa, hoặc quyết dừng. Người kiểm đọc `results/T-034/runs/g2-build-002/v5-bo-sung-sau-phan-bien.md` sau khi tự soát, và so `runs/phat-hanh-001/` với ba file phát hành hiện tại.
6. **Lệnh cuối cùng đã chạy:** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-002`.

## Prompt bàn giao của lượt này cho agent đối phương (Codex, kiểm lại phản hồi và sửa)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, `tasks/T-034-g2-goi-trinh/SPEC.md`, đã duyệt và khóa ngày 13/10/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3, P4; cổng G2.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện kết quả, theo SPEC.
- Tài liệu gốc: `AGENTS.md`; `docs/STATE.md`; `tasks/T-034-g2-goi-trinh/SPEC.md` và `LOG.md`; `docs/MRP.md`; `docs/PLAN-P3-G2.md`; `docs/WHY.md`; `docs/DECISIONS.md`; `docs/LESSONS.md`; `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md`; `docs/reference/sources/advisor-2026-09-23.md`; `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`. Commit gốc: `6c93e6d`; các file T-034 chưa commit. Phiên bản khung trước/sau phần T-034: `results/T-034/runs/v1-002-truoc-noi-why/v1.json` và `results/T-034/runs/v1-003-cuoi/v1.json`, trường `/frame`.
- Phản biện và phản hồi trước: hai lượt Codex (phản biện kết quả; kiểm lại phản hồi) và hai lượt Claude đáp, đều ngày 13/10/2026 và đều trong chat; chưa có REVIEW.md. Minh dán nguyên văn các lượt đó cùng prompt này. Lời duyệt sửa của Minh và danh sách sửa: mục “Phiên 2” của `tasks/T-034-g2-goi-trinh/LOG.md`.
- Code và kết quả liên quan: bản trước sửa: `results/T-034/runs/phat-hanh-001/` và lượt `results/T-034/runs/g2-build-001/`, manifest `results/T-034/runs/manifest-cuoi-001/manifest.json`. Bản sau sửa: `results/T-034/goi-g2.md`, `hai-phep-kiem.md`, `ban-do-g2.json`, `thiet-ke-hai-phep-kiem.md` (Mục nối 6), `scripts/` (gồm `scripts/mau/`); lượt dựng `results/T-034/runs/g2-build-002/` (`render/registry.json`, `v4.json`, `v5-bo-sung-sau-phan-bien.md`); manifest `results/T-034/runs/manifest-cuoi-002/manifest.json`. `bang-baseline.json` và `hai-phep-kiem.json` thuộc bản trước sửa. Môi trường laptop: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8`. Chỉ tính đối chiếu từ đầu ra đã lưu; không chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: Minh chưa nêu quyền ghi cho lượt này; mặc định chỉ đọc và trả lời trong chat. Nếu Minh cho phép ghi thì chỉ ghi đúng một bản phản biện lượt mới trong `tasks/T-034-g2-goi-trinh/` theo `tasks/_MAU/REVIEW.md`; không ghi LOG, STATE.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

---

## Phiên 3 — 13/10/2026 — Claude — laptop — vai trò: người làm (đáp lượt soát độc lập và sửa)

**Mở phiên:** cùng cuộc trò chuyện. Trước khi sửa, 239 file khớp `runs/manifest-cuoi-002/manifest.json` (theo lượt kiểm của người phản biện).

**Công đoạn:** Codex soát kết quả độc lập trên bản đã sửa (Minh dán vào chat); tôi đáp trong chat (chỉ đọc), rồi sửa theo lời duyệt.

**Đánh giá phản biện:**

| Điểm | Kết luận của người làm | Bằng chứng riêng |
|---|---|---|
| R1 (CHẶN): câu “BARO và CIRCA có cơ chế khác đã xác lập” dùng để nghiêng về “lan không chiếm đa số” | Đúng | `results/T-032/runs/baro-b2-001/summary.json#/summary/by_dataset/*/native_wrong_at_1`: đổi thang chỉ sửa 3/9 và 2/14 ca sai |
| R2 (CHẶN): UV-7 thành ràng buộc; UV-8 “phải kèm UV-7” | Đúng | `circa-laptop-k2-001/collect-001/summary.json#/summary/k2_cases_with_huge_node/hit1`: có DA 3, có cạnh không DA 0, bỏ cạnh 9; `rht.py` bước DA cộng có điều kiện |
| R3 (KHÔNG CHẶN): kết luận B-1 quá rộng | Đúng | `baro-b1-001/summary.json#/summary/all`: root có thêm cột ở 38/52 ca, hạng không đổi ở 52/52 |

Tự tìm thêm: chữ “nghiêng về không chiếm đa số” còn ở mục 0, câu 8 mục 7, dòng tóm tắt K4 của LOG phiên 1 và trong câu trả lời tôi viết cho Minh ở chat; đều mạnh hơn bằng chứng. Không có bất đồng với người phản biện.

**Quyết định của Minh trong phiên** (nguyên lời): “duyệt sửa”, trả lời bốn mục đề xuất của lượt đáp. Chưa ghi DECISIONS.

**Diễn biến:**
- Chép bản đang phát hành vào `results/T-034/runs/phat-hanh-002/`.
- Sửa `scripts/mau/goi-g2.md` (mục 0, 4.2, UV-7, UV-8, câu 8 mục 7, dòng đầu về sổ số liệu), `scripts/g2_ban_do_rows.py` (G2-H09), `scripts/g2_ban_do.py` (năm số mới).
- Dựng lại vào `results/T-034/runs/g2-build-003/`. **V3 đạt. V4 đạt**: 2.439 số, 36 file nguồn, 0 lệch, 0 chữ số không nguồn.
- Viết `runs/g2-build-003/v5-bo-sung-sau-phan-bien-2.md`.
- Manifest `results/T-034/runs/manifest-cuoi-003/manifest.json` (253 file). So với manifest 002: đúng năm file đổi (`goi-g2.md`, `ban-do-g2.json`, ba file trong `scripts/`), không file nào mất, 14 file mới. `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json`, bản thiết kế không đổi.
- Không kết nối EC2, không chạy thực nghiệm, không sửa STATE, không commit.

**Điều đã đổi trong kết luận** (số cũ giữ nguyên):
- K4: không còn nghiêng về bên nào. Chưa có căn cứ nói lan gây phần lớn ca sai, cũng chưa có căn cứ nói nó là thiểu số. Dòng tóm tắt K4 ở mục kết thúc phiên 1 của LOG này (“bằng chứng nghiêng về không chiếm đa số”) không còn hiệu lực.
- UV-7: chỉ “kiểm và xử lý giá trị không hợp lệ” là yêu cầu kỹ thuật; cách gộp điểm là ứng viên cần so. UV-8 không còn buộc dùng UV-7.
- G2-H09: lọc cột hằng có bỏ cột của root nhưng không phải bước làm root mất hạng; thang IQR không giải thích hết ca sai của BARO.

**Kết thúc phiên:**

1. **Đã làm gì:** đáp ba điểm; sửa theo lời duyệt; dựng lại, kiểm lại.
2. **File đã thay đổi:** năm file nêu trên; các file mới của `runs/phat-hanh-002/`, `runs/g2-build-003/`, `runs/manifest-cuoi-003/`; LOG này.
3. **Kiểm đã chạy:** V3, V4 đạt trên lượt 003; so hai manifest; quét các cụm “nghiêng về”, “phải kèm UV-7”, “không chép nguyên”, “làm mất kênh của root”: không còn.
4. **Điều chưa chắc hoặc cần Minh quyết:**
   - Bản sửa lần hai chưa được người phản biện kiểm.
   - Thấy khi soát lại, **chưa sửa** vì ngoài phạm vi đã duyệt: dòng G2-H12 viết “DA chép điểm đó cho các nút cha” (mã cộng có điều kiện) và “chuỗi bằng chứng đủ từ đầu vào tới hạng” (dựa trên phép bỏ cạnh, không cô lập bước DA). Đề xuất sửa lời văn, chờ Minh.
   - Ba lượt phản biện liên tiếp đều bắt được câu mạnh hơn bằng chứng do tôi viết; tôi không đề xuất dừng phản biện ở lượt này.
   - Còn mở, không đổi: mức đóng góp của lan; cách gộp điểm; bước gây chênh giữa hai pipeline TraceRCA; onset và nền sạch; underflow ngoài hai ca; lợi ích đồ thị. Mười điểm ở mục 8 của gói và hai dòng DECISIONS vẫn chờ Minh. Dòng STATE vẫn “Chờ phản biện”.
5. **Bước tiếp theo chính xác:** Minh chuyển prompt dưới đây cho một phiên Codex mới để soát độc lập bản hiện tại, hoặc quyết dừng.
6. **Lệnh cuối cùng đã chạy:** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-003`.

## Prompt bàn giao của lượt này cho agent đối phương (Codex, soát kết quả)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, `tasks/T-034-g2-goi-trinh/SPEC.md`, đã duyệt và khóa ngày 13/10/2026.
- Công đoạn: soát kết quả.
- Gói/cổng: <gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>.
- Người làm và người phản biện chính thức: <tên theo SPEC; ngoài task thì ghi vai trò dự kiến>.
- Tài liệu gốc: <danh sách đường dẫn và git diff từ commit gốc nếu có>.
- Phản biện và phản hồi trước: có các lượt phản biện và phản hồi ngày 13/10/2026, đều trong chat, chưa có REVIEW.md; phần người làm ghi lại nằm ở mục “Phiên 2” và “Phiên 3” của `tasks/T-034-g2-goi-trinh/LOG.md`, `results/T-034/runs/g2-build-002/v5-bo-sung-sau-phan-bien.md` và `results/T-034/runs/g2-build-003/v5-bo-sung-sau-phan-bien-2.md`. Các lượt đó không được dán kèm prompt này.
- Code và kết quả liên quan: bản hiện tại: `results/T-034/goi-g2.md`, `hai-phep-kiem.md`, `hai-phep-kiem.json`, `ban-do-g2.json`, `bang-baseline.json`, `thiet-ke-hai-phep-kiem.md`, `scripts/` (gồm `scripts/mau/`) và `runs/`. Manifest: `results/T-034/runs/manifest-cuoi-003/manifest.json`. Sổ số liệu và kết quả kiểm số: `results/T-034/runs/g2-build-003/render/registry.json` và `v4.json`. Các bản phát hành trước: `results/T-034/runs/phat-hanh-001/`, `phat-hanh-002/`, manifest 001 và 002. Nguồn của gói: `results/T-024`, `T-025`, `T-026`, `T-028`, `T-029`, `T-032`, `T-033`; manifest bổ sung tại `results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json` và `manifest-review-001.json`. Môi trường laptop: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8`. Chỉ tính đối chiếu từ đầu ra đã lưu; không chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: Minh chưa nêu quyền ghi cho lượt này; mặc định chỉ đọc và trả lời trong chat. Nếu Minh cho phép ghi thì chỉ ghi đúng một file `tasks/T-034-g2-goi-trinh/REVIEW.md` theo `tasks/_MAU/REVIEW.md`; không ghi LOG, STATE.

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

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

## Phiên 4 — 13/10/2026 — Claude — laptop — vai trò: người làm (tự soát, đáp ba lượt Codex, sửa)

**Mở phiên:** phiên mới, không có lịch sử chat của phiên 1–3. Trước khi sửa, 253 file khớp `runs/manifest-cuoi-003/manifest.json` (0 lệch, 0 thiếu); 2.438 con trỏ của sổ số liệu lượt 003 và 36 mã băm nguồn khớp.

**Công đoạn:** bốn lượt chỉ đọc, trả lời trong chat, rồi một lượt sửa theo lời duyệt.

1. Tự soát độc lập (lượt Codex ngày 13/10 chưa tới tay tôi ở lượt này): tám điểm N1–N8.
2. Codex kiểm N1–N8; tôi đáp, thêm mục B (CIRCA trước và sau DA) và N9 (loại span).
3. Codex phản đối một phần mục B; tôi kiểm và rút ba câu.
4. Trình gói sửa S1–S9, rồi trình đoạn cũ → đoạn mới.

**Điểm tự tìm và kết quả sau phản biện:**

| Điểm | Nội dung | Kết quả |
|---|---|---|
| N1 (CHẶN câu K4) | Mục 4.1 loại hẳn "chờ" ở CIRCA | Thống nhất: bỏ câu loại; giữ bằng chứng trước/sau DA. Đã sửa (S1, S2) |
| N2 (CHẶN câu 8) | Lan "được xác lập là cơ chế gây sai" cho trễ mạng, trái G2-H06 | Thống nhất. Đã sửa (S3) |
| N3 | Bốn ứng viên gọi chung là "đồ thị"; điều kiện MRP P6 chưa nêu | Đúng một phần: quan hệ cha–con trong trace vẫn là cấu trúc (MRP P7); không thêm điểm quyết định ở mục 8. Đã sửa (S4, S5) |
| N4 | Tỷ lệ "không nằm phía trên root" chỉ nói về quan hệ gọi | Thống nhất. Đã sửa (S4) |
| N5 | K5 chưa đủ tiêu chí xong | Đúng một phần: UV-9 là kiểm bản cài; UV-10 là yêu cầu DT18. Đã sửa (S5) |
| N6 | Quy cơ chế cho SimpleRCA nói chung | Thu hẹp về bản M4 theo quy ước T-017. Đã sửa (S7) |
| N7 | Mức dòng thấp hơn mức nguồn con ở G2-H06, H17, H22 | Minh chọn phương án (a): nâng mức theo WHY-51, ghi phạm vi trong "Vì sao". Đã sửa (S8) |
| N8 | G2-H25, H26 thiếu số theo ô; K7 thiếu câu về chọn phương pháp | Đã sửa (S9) |
| N9 | UV-10 ghi "chưa kiểm" loại span trong khi thẻ dataset đã ghi | Thống nhất; dẫn `results/T-002/the-rcaeval.md` và `results/T-008/the-dataset.md`. Đã sửa (S5, S6) |

**Sai của người làm trong lượt đáp (chỉ nằm trong chat, không vào file):** tôi đọc nhãn `other` của bảng CIRCA thành "không gọi root" và viết "không phải do chờ có căn cứ ở 5/8 ca". Codex chỉ ra: ở 8/8 ca, `…/circa-laptop-k2-001/cases/RE2-TT/<ca>/obs/ban-ghi-0.json#/extra/call_edges` có đường `ts-admin-travel-service → ts-travel-service → root`; cờ M5 của T-028 tính cả tổ tiên gián tiếp. Tôi kiểm lại, đúng, và rút ba câu. Cũng sửa một dẫn nguồn của Codex: câu về Nezha-OB nằm ở dòng 29 của thẻ, không phải dòng 31.

**Quyết định của Minh trong phiên** (nguyên lời): “duyệt sửa” (cho gói S1–S9, kèm bước trình đoạn cũ → đoạn mới); rồi “duyệt theo đề xuất” (cho lời văn đã trình và S8 phương án (a)). Chưa ghi DECISIONS.

**Diễn biến lượt sửa:**
- Chép bản đang phát hành vào `results/T-034/runs/phat-hanh-003/`.
- Sửa `scripts/mau/goi-g2.md`, `scripts/g2_ban_do_rows.py`, `scripts/g2_ban_do.py` (ba số mới về tác dụng của DA; bảng theo ô cho G2-H25, G2-H26), `scripts/g2_blocks.py` (khối Phụ lục C; câu ở danh sách 1 mục 1), `scripts/g2_render.py` (đăng ký khối mới). Sửa tại chỗ; bản trước còn mã băm trong manifest 003.
- Dựng lại vào `results/T-034/runs/g2-build-004/`. **V3 đạt** (68/68). **V4 đạt**: 2.612 số, 38 file nguồn, 0 lệch, 0 chữ số không nguồn.
- Viết `runs/g2-build-004/v5-bo-sung-sau-phan-bien-3.md`.
- Manifest `results/T-034/runs/manifest-cuoi-004/manifest.json` (267 file). So với manifest 003: đúng bảy file đổi (`goi-g2.md`, `ban-do-g2.json`, năm file trong `scripts/`), không file nào mất, 14 file mới. `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json`, bản thiết kế không đổi.
- Không kết nối EC2, không chạy thực nghiệm, không sửa STATE, không commit.

**Lệch so với bảng S1–S9 đã trình** (đã báo Minh trước khi duyệt lời văn): S1, S2 không ghi các số tôi đếm tay ("8/10", "8/8", "7/8") vì nguồn không có con trỏ tổng; dùng số có nguồn: hạng 1 trước DA / sau DA / bỏ cạnh trong nhóm ca có nút cực lớn, và tác dụng của DA trên 30 ca.

**Điều đã đổi trong kết luận** (số baseline giữ nguyên):
- CIRCA: root đã mất hạng 1 trước bước DA ở mọi ca có nút cực lớn; DA truyền điểm và đổi hạng. Không còn câu loại "chờ"; đóng góp của chờ ghi là chưa phân xử.
- K4: với trễ mạng chỉ xác lập nơi có dấu hiệu. Với TraceRCA bản thư viện, nêu số ca đổi khi bỏ phần chờ, tách khỏi số ca hạng 1.
- K5: ứng viên chia ba loại; UV-10 dẫn kết quả khảo sát loại span; UV-1, UV-2 nêu điều kiện của MRP P6.
- G2-H06, H17, H22 đổi mức dòng (CT, ĐC, CT); G2-H12 thêm trạng thái "chưa phân xử".
- K7 có 16 câu.

**Kết thúc phiên:**

1. **Đã làm gì:** tự soát; đáp ba lượt Codex; sửa theo lời duyệt; dựng lại, kiểm lại.
2. **File đã thay đổi:** bảy file nêu trên; các file mới của `runs/phat-hanh-003/`, `runs/g2-build-004/`, `runs/manifest-cuoi-004/`; LOG này. Không sửa file nào khác.
3. **Kiểm đã chạy:** V3, V4 đạt trên lượt 004; so manifest 003 và 004; `hai-phep-kiem.md` trùng mã băm bản trước; đọc lại toàn bộ phần khác biệt giữa `runs/phat-hanh-003/goi-g2.md` và bản mới.
4. **Điều chưa chắc hoặc cần Minh quyết:**
   - *Task đạt gì:* các câu CHẶN đã thống nhất với Codex đều đã sửa. Bản sửa lần ba **chưa được người phản biện kiểm**.
   - *Câu hỏi nguồn trả lời tới đâu:* RQ1 và phần mô tả của RQ2 có bảng và bản đồ; cơ chế ở nhiều dòng vẫn "chưa phân xử". Không đóng RQ2 hay G2.
   - *Tiêu chí xong của SPEC:* G2-H23, G2-H24 vẫn "không tách theo ô"; tôi chưa kiểm lại xem nguồn có bảng theo ô dùng được không. UV-7(ii) và UV-10 không có dự đoán bác bỏ trên dev, đã ghi lý do; Minh quyết có chấp nhận ngoại lệ này không.
   - *Chưa kiểm:* Phụ lục A, B chưa đọc lại toàn bộ; dòng B16 ở mục 6.2 dựa trên tìm từ khóa, chưa đọc toàn văn; mã E1/E2 và bài TraceRCA không đọc lại ở phiên này.
   - *Còn mở, không đổi:* lan có đáng kể và đóng góp của chờ ở CIRCA; bước gây chênh giữa hai pipeline TraceRCA; onset và nền sạch; underflow ngoài hai ca; lựa chọn P6; lợi ích đồ thị.
   - Bốn lượt liên tiếp đều có câu mạnh hơn bằng chứng do tôi viết, kể cả trong lượt đáp. Tôi không đề xuất dừng phản biện trước khi bản 004 được kiểm.
   - Mười điểm ở mục 8 của gói và các dòng DECISIONS của T-034 vẫn chờ Minh. Dòng T-034 trong STATE vẫn “Chờ phản biện”; tôi không sửa vì lời duyệt không nêu STATE.
5. **Bước tiếp theo chính xác:** Minh chuyển prompt dưới đây cho Codex để kiểm bản sửa, hoặc quyết dừng. Người kiểm so `results/T-034/runs/phat-hanh-003/` với ba file phát hành hiện tại, đọc `results/T-034/runs/g2-build-004/v5-bo-sung-sau-phan-bien-3.md` sau khi tự soát.
6. **Lệnh cuối cùng đã chạy:** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-004`.

## Prompt bàn giao của lượt này cho agent đối phương (Codex, kiểm lại phản hồi và sửa)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, D:/RCA-flashticket/tasks/T-034-g2-goi-trinh/SPEC.md, đã duyệt và khóa ngày 13/10/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3, P4; cổng G2.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện kết quả, theo SPEC.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; tasks/T-034-g2-goi-trinh/SPEC.md và LOG.md; docs/MRP.md; docs/PLAN-P3-G2.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md. Commit gốc: 6c93e6d; các file T-034 chưa commit.
- Phản biện và phản hồi trước: Phiên 2, Phiên 3 và Phiên 4 của tasks/T-034-g2-goi-trinh/LOG.md; results/T-034/runs/g2-build-002/v5-bo-sung-sau-phan-bien.md; results/T-034/runs/g2-build-003/v5-bo-sung-sau-phan-bien-2.md; results/T-034/runs/g2-build-004/v5-bo-sung-sau-phan-bien-3.md; các lượt trong chat ngày 13/10/2026 do Minh cung cấp. Chưa có REVIEW.md.
- Code và kết quả liên quan: bản hiện tại tại results/T-034/goi-g2.md, hai-phep-kiem.md, hai-phep-kiem.json, ban-do-g2.json, bang-baseline.json, thiet-ke-hai-phep-kiem.md, scripts/ và runs/. Manifest hiện tại: results/T-034/runs/manifest-cuoi-004/manifest.json. Sổ số liệu và kiểm số: results/T-034/runs/g2-build-004/render/registry.json và v4.json. Bản trước: runs/phat-hanh-001/, runs/phat-hanh-002/, runs/phat-hanh-003/ và manifest-cuoi-001/002/003. Nguồn: results/T-002, T-008, T-024, T-025, T-026, T-028, T-029, T-032, T-033; src/circa_kien_truc/; results/T-032/runs/circa-laptop-k2-001/. Manifest bổ sung tại results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json, manifest-review-001.json và old-files-before.json. Môi trường: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8. Chỉ đối chiếu/tính lại từ đầu ra đã lưu bằng thao tác không ghi file; không chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản REVIEW được phép ghi>.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

## Phiên 5 — 14/10/2026 — Claude — laptop — vai trò: người làm (đáp lượt Codex kiểm bản 004, sửa)

**Mở phiên:** cùng cuộc trò chuyện với Phiên 4. Trước khi sửa, bản đang phát hành là bản của `runs/manifest-cuoi-004/` (Codex báo toàn bộ tệp khớp manifest ở lượt kiểm).

**Công đoạn:** Codex kiểm bản 004 (Minh dán vào chat, kèm một bản đề xuất của Codex gửi Minh về các phần chưa đạt và câu còn mở); tôi đáp trong chat (chỉ đọc), rồi sửa theo lời duyệt.

**Đánh giá phản biện:**

| Điểm | Kết luận của người làm | Bằng chứng riêng |
|---|---|---|
| Các điểm CHẶN cũ về CIRCA và lan đã sửa đúng (Codex xác nhận) | Ghi nhận | — |
| 1 (CHẶN nghiệm thu đủ SPEC): mở đầu mục 5 nói mọi ứng viên đủ căn cứ, trong khi phần cách gộp điểm chưa có dự đoán | Đúng. Lỗi do tôi: lượt 004 sửa UV-7 mà không sửa câu mở đầu | `runs/phat-hanh-004/goi-g2.md`, mở đầu mục 5 và UV-7 |
| 2 (CHẶN nghiệm thu đủ SPEC): đầu vào bậc thang tách được theo ô | Đúng | Tính lại từ `engine-final-summary-001.json#/slots` ghép `nhan-proxy-va-schema.json#/P1/cases`: tổng 437 → 360 và 361; ô route/mem 27 → 31 ở cả hai nhánh |
| 3 (KHÔNG CHẶN): câu 16 thiếu lý do | Đúng, phạm vi rộng hơn (N10) | MRP mục P1; `results/T-001/danh-sach-phuong-phap.md` dòng 235–244 |
| N10 (tự tìm, KHÔNG CHẶN bảng số): câu 16 bỏ sót tầng hai chưa chạy (Q-62) và việc họ "học có đồ thị" chưa có đại diện xếp hạng | Đã sửa | Q-62; `docs/PLAN-P3-G2.md` dòng 63 |

Không có bất đồng với người phản biện.

**Quyết định của Minh trong phiên** (nguyên lời): “duyệt đề xuất và prompt giao việc cho codex”, trả lời năm mục B1–B5 của lượt đáp. Chưa ghi DECISIONS. Ba việc ở mục C của lượt đáp (ghi DECISIONS, sửa dòng STATE, trình hai phép còn lại) tôi coi là **chưa được giao**: lời duyệt không nêu, và tôi đã ghi là chờ Minh bảo.

**Diễn biến:**
- Chép bản đang phát hành vào `results/T-034/runs/phat-hanh-004/`.
- Sửa `scripts/mau/goi-g2.md` (mở đầu mục 5, UV-7, câu 16, tên Phụ lục C, dòng đầu về sổ số liệu), `scripts/g2_ban_do_rows.py` (G2-H23, G2-H24), `scripts/g2_ban_do.py` (tổng theo ô của hai nhánh nén ghi vào file dẫn xuất của lượt, có tự kiểm tổng; ba số mới), `scripts/g2_blocks.py` (bảng G2-H23 ở Phụ lục C).
- Lượt `runs/g2-build-005/`: **V4 hỏng**, 1 chữ số không qua sổ (tôi viết "ngày 13 và 14/10/2026" ở dòng mở đầu). Giữ làm lượt lỗi.
- Sửa cách viết ngày, dựng lại vào `runs/g2-build-006/`. **V3 đạt** (68/68). **V4 đạt**: 2.675 số, 38 file nguồn, 0 lệch, 0 chữ số không nguồn.
- Viết `runs/g2-build-006/v5-bo-sung-sau-phan-bien-4.md`.
- Manifest `results/T-034/runs/manifest-cuoi-005/manifest.json`; so với manifest 004 ghi ở mục kiểm bên dưới.
- Không kết nối EC2, không chạy thực nghiệm, không sửa STATE, không commit.

**Điều đã đổi trong kết luận** (số baseline giữ nguyên):
- Mục 5 không còn nói mọi ứng viên đủ căn cứ để thử: phần (ii) của UV-7 là câu hỏi thiết kế; UV-10 là yêu cầu DT18 chưa kiểm được trên dev, không phải miễn kiểm.
- G2-H23 có bảng theo ô; ô route/mem tăng trong khi tổng giảm, ghi là quan sát.
- G2-H24 ghi rõ lý do không tách theo ô là giới hạn dữ liệu.
- Câu 16 nêu tiêu chí chọn, tầng hai chưa chạy và họ chưa có đại diện.

**Kết thúc phiên:**

1. **Đã làm gì:** đáp lượt Codex; sửa B1–B5 theo lời duyệt; dựng lại, kiểm lại.
2. **File đã thay đổi:** `results/T-034/goi-g2.md`, `ban-do-g2.json`; bốn file trong `scripts/` nêu trên; các file mới của `runs/phat-hanh-004/`, `runs/g2-build-005/`, `runs/g2-build-006/`, `runs/manifest-cuoi-005/`; LOG này.
3. **Kiểm đã chạy:** V3, V4 đạt trên lượt 006; so manifest 004 và 005; `hai-phep-kiem.md` trùng mã băm bản trước; đọc lại phần khác biệt giữa `runs/phat-hanh-004/goi-g2.md` và bản mới.
4. **Điều chưa chắc hoặc cần Minh quyết:**
   - *Task đạt gì:* các điểm Codex nêu ở lượt kiểm bản 004 đã sửa. Bản 006 **chưa được người phản biện kiểm**.
   - *Tiêu chí xong của SPEC:* còn hai chỗ không đạt theo chữ, đã ghi lý do trong gói: phần (ii) của UV-7 và UV-10 không có dự đoán bác bỏ trên dev; G2-H24 không tách theo ô. Minh quyết có chấp nhận khi xét G2 không.
   - *Ai đã kiểm phần nào:* Phụ lục A, B và dòng B16 ở mục 6.2 do Codex đối chiếu; tôi chưa tự đọc từng dòng.
   - *Còn mở, không đổi:* lan có đáng kể; đóng góp của chờ ở CIRCA; bước gây chênh hai bản TraceRCA; underflow ngoài hai ca; thời điểm sự cố bắt đầu; lựa chọn P6; lợi ích đồ thị. Không đóng RQ2 hay G2.
   - *Chờ Minh:* mười điểm mục 8 của gói; các dòng DECISIONS cho lời duyệt T-034 (gồm ba lời duyệt ở Phiên 4–5); dòng T-034 trong STATE; có giao hai phép còn lại (chênh hai bản TraceRCA; miền log trên các ca còn lại, hơn một giờ máy) không.
5. **Bước tiếp theo chính xác:** Minh chuyển prompt dưới đây cho Codex để kiểm bản 006, hoặc quyết dừng. Người kiểm so `results/T-034/runs/phat-hanh-004/` với ba file phát hành hiện tại, đọc `results/T-034/runs/g2-build-006/v5-bo-sung-sau-phan-bien-4.md` sau khi tự soát.
6. **Lệnh cuối cùng đã chạy:** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-005`.

## Prompt bàn giao của lượt này cho agent đối phương (Codex, kiểm lại phản hồi và sửa)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, tasks/T-034-g2-goi-trinh/SPEC.md, đã duyệt và khóa ngày 13/10/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3, P4; G2.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện.
- Tài liệu gốc: tasks/T-034-g2-goi-trinh/SPEC.md; docs/STATE.md; docs/MRP.md; docs/PLAN-P3-G2.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md. Bản phát hành trước ở results/T-034/runs/phat-hanh-004/.
- Phản biện và phản hồi trước: các lượt trong chat ngày 13/10 và 14/10/2026; phần người làm ghi nhận tại tasks/T-034-g2-goi-trinh/LOG.md, Phiên 1–5; results/T-034/runs/g2-build-004/v5-bo-sung-sau-phan-bien-3.md và results/T-034/runs/g2-build-006/v5-bo-sung-sau-phan-bien-4.md. Chưa có bản REVIEW của T-034 trong repo.
- Code và kết quả liên quan: results/T-034/goi-g2.md; ban-do-g2.json; bang-baseline.json; hai-phep-kiem.md; hai-phep-kiem.json; thiet-ke-hai-phep-kiem.md; scripts/; runs/g2-build-006/; runs/manifest-cuoi-005/manifest.json. Nguồn tại results/T-001, T-002, T-008, T-021, T-024, T-025, T-026, T-028, T-029, T-032, T-033. Manifest nguồn tại results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json, manifest-review-001.json và old-files-before.json. Môi trường đọc và tính đối chiếu: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản REVIEW được phép ghi>.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

## Phiên 6 — 14/10/2026 — Claude — laptop — vai trò: người làm (trả lời Minh về tiêu chí xong, sửa)

**Mở phiên:** cùng cuộc trò chuyện với Phiên 4–5. Trước khi sửa, bản đang phát hành là bản của `runs/manifest-cuoi-005/`.

**Công đoạn:** Minh hỏi vì sao còn chỗ chưa đạt tiêu chí xong của SPEC theo chữ mà không sửa, và yêu cầu soạn prompt giao Codex mọi phần cần kiểm lại. Tôi trả lời trong chat (chỉ đọc), trình ba mục B6–B8, rồi sửa theo lời duyệt. Bản 006 chưa được Codex kiểm khi lượt này bắt đầu.

**Trả lời đã đưa cho Minh:** không có lý do đặc biệt. G2-H19 thiếu số theo ô là do tôi bỏ sót (các báo cáo trước chỉ kể G2-H23, G2-H24). G2-H24 tôi ghi theo hướng "giới hạn chung" mà Codex nêu. Hai phần không có dự đoán bác bỏ (cách gộp điểm; thành phần DT18) không viết dự đoán trung thực được, nên cách sửa là đưa ra khỏi danh sách ứng viên, không phải bịa dự đoán. Tôi không đề xuất sửa SPEC đã khóa.

**Quyết định của Minh trong phiên** (nguyên lời): “duyệt sửa”, trả lời ba mục B6–B8. Chưa ghi DECISIONS.

**Diễn biến:**
- Chép bản đang phát hành vào `results/T-034/runs/phat-hanh-005/`.
- Sửa `scripts/mau/goi-g2.md` (mở đầu mục 5; UV-10 thành mục con “Thành phần DT18 yêu cầu”; dòng mục 6.2; tên Phụ lục C; dòng đầu về sổ số liệu), `scripts/g2_ban_do.py` (hai bảng dẫn xuất theo ô, có tự kiểm tổng), `scripts/g2_blocks.py` (bảng G2-H19, G2-H24 ở Phụ lục C).
- Hai lần chạy `g2_ban_do.py` vào `runs/g2-build-007/` dừng lỗi trước khi ghi bản đồ: (1) tôi giả định 30 file `dev-<ca>--context.json` của T-033 có trên laptop, thực tế chỉ có 1 file khớp mã băm; (2) một tên biến chưa khai trong hàm chính. Không lượt nào ghi đầu ra dùng được; thư mục được dùng lại cho lần chạy đạt.
- Đổi nguồn của bảng G2-H24: tính lại từ `engine-final-summary-001.json#/slots` (trường `native_alarm_times`) và mốc tiêm ở `results/T-022/nhan-dev.json`. Trước khi dùng, tôi kiểm phép tính lại: khớp cả năm tổng của `fast-summary-001.json#/bocpd_post_any_byD` (12, 23, 27, 29, 30) và khớp ca duy nhất có file gốc.
- Dựng vào `runs/g2-build-007/`. **V3 đạt** (68/68). **V4 đạt**: 2.827 số, 38 file nguồn, 0 lệch, 0 chữ số không nguồn.
- Viết `runs/g2-build-007/v5-bo-sung-sau-phan-bien-5.md`.
- Manifest `results/T-034/runs/manifest-cuoi-006/manifest.json` (304 file). So với manifest 005: đúng năm file đổi (`goi-g2.md`, `ban-do-g2.json`, ba file trong `scripts/`), không file nào mất, 14 file mới.
- Không kết nối EC2, không chạy thực nghiệm, không sửa STATE, không commit.

**Làm khác đề xuất đã duyệt — đã dừng phần liên quan:**
- B8 ghi chuyển phần (ii) của UV-7 (cách gộp điểm) thành một dòng ở **mục 6.3**. Khi sửa tôi thấy mục 6.3 là “thuộc đánh giá sau khi khóa thiết kế”, còn cách gộp điểm là câu hỏi thiết kế trên dev, trước khi khóa. Đặt vào 6.3 là xếp sai loại; đặt vào 6.1 là làm khác đề xuất. Theo Luật 0 tôi **không làm phần này**; UV-7 vẫn ghi phần (ii) là “câu hỏi thiết kế, chưa là ứng viên”. Chờ Minh quyết chỗ đặt.
- B7: nguồn của bảng khác với cách tôi mô tả lúc đề xuất ở chỗ dùng file nào; vẫn là “tính lại từ thời điểm báo động đã lưu” và thỏa điều kiện khớp tổng đã nêu trong đề xuất. Tôi báo để Minh và người phản biện biết.

**Kết thúc phiên:**

1. **Đã làm gì:** trả lời câu hỏi của Minh; sửa B6, B7 và phần UV-10 của B8; dựng lại, kiểm lại.
2. **File đã thay đổi:** `results/T-034/goi-g2.md`, `ban-do-g2.json`; ba file trong `scripts/` nêu trên; các file mới của `runs/phat-hanh-005/`, `runs/g2-build-007/`, `runs/manifest-cuoi-006/`; LOG này.
3. **Kiểm đã chạy:** V3, V4 đạt trên lượt 007; bước dựng tự kiểm tổng theo ô của ba bảng dẫn xuất; so manifest 005 và 006; `hai-phep-kiem.md` trùng mã băm bản trước.
4. **Điều chưa chắc hoặc cần Minh quyết:**
   - *Task đạt gì:* mọi dòng G2-Hn nay có số theo ô hoặc bảng theo ô. Bản 006 và 007 **chưa được người phản biện kiểm**.
   - *Tiêu chí xong của SPEC còn một chỗ:* phần (ii) của UV-7 vẫn nằm trong mục ứng viên, không có dự đoán. Cần Minh quyết chỗ đặt (mục 6.1 hay 6.3).
   - *Giới hạn của bảng G2-H24:* 29/30 file gốc theo ca của T-033 không có trên laptop; bảng khớp ở mức tổng và một ca, chưa đối chiếu từng ca với file gốc.
   - *Ai đã kiểm phần nào:* Phụ lục A, B và dòng B16 ở mục 6.2 do Codex đối chiếu ở lượt kiểm bản 004; tôi chưa tự đọc từng dòng.
   - *Còn mở, không đổi:* lan có đáng kể; đóng góp của chờ ở CIRCA; bước gây chênh hai bản TraceRCA; underflow ngoài hai ca; thời điểm sự cố bắt đầu; lựa chọn P6; lợi ích đồ thị. Không đóng RQ2 hay G2.
   - *Chờ Minh:* mười điểm mục 8 của gói; các dòng DECISIONS cho lời duyệt T-034 (Phiên 1–6); dòng T-034 trong STATE; có giao hai phép còn lại không. Nhánh `master` đã có commit mới hơn `6c93e6d` (hiện `1e685ad7`), không phải do tôi.
5. **Bước tiếp theo chính xác:** Minh quyết chỗ đặt phần (ii) của UV-7; chuyển prompt dưới đây cho Codex để kiểm bản 007, hoặc quyết dừng. Người kiểm so `results/T-034/runs/phat-hanh-005/` với ba file phát hành hiện tại, đọc `results/T-034/runs/g2-build-007/v5-bo-sung-sau-phan-bien-5.md` sau khi tự soát.
6. **Lệnh cuối cùng đã chạy:** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-006`.

## Prompt bàn giao của lượt này cho agent đối phương (Codex, kiểm lại phản hồi và sửa)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, tasks/T-034-g2-goi-trinh/SPEC.md, đã duyệt và khóa ngày 13/10/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3, P4; G2.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện.
- Tài liệu gốc: tasks/T-034-g2-goi-trinh/SPEC.md; docs/STATE.md; docs/MRP.md; docs/PLAN-P3-G2.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md. HEAD hiện tại của master: 1e685ad7; các file T-034 chưa commit. Bản phát hành trước ở results/T-034/runs/phat-hanh-005/.
- Phản biện và phản hồi trước: các lượt trong chat ngày 13/10 và 14/10/2026; phần người làm ghi nhận tại tasks/T-034-g2-goi-trinh/LOG.md, Phiên 1–6; results/T-034/runs/g2-build-004/v5-bo-sung-sau-phan-bien-3.md, results/T-034/runs/g2-build-006/v5-bo-sung-sau-phan-bien-4.md và results/T-034/runs/g2-build-007/v5-bo-sung-sau-phan-bien-5.md. Chưa có bản REVIEW của T-034 trong repo.
- Code và kết quả liên quan: results/T-034/goi-g2.md; ban-do-g2.json; bang-baseline.json; hai-phep-kiem.md; hai-phep-kiem.json; thiet-ke-hai-phep-kiem.md; scripts/; runs/g2-build-007/ (lượt dùng để phát hành; runs/g2-build-005/ là lượt lỗi được giữ); runs/manifest-cuoi-006/manifest.json. Các phần thuộc phạm vi kiểm của lượt này: (a) phần khác biệt giữa runs/phat-hanh-005/ và bản hiện tại: G2-H19, G2-H24, mở đầu mục 5, mục con “Thành phần DT18 yêu cầu”, Phụ lục C, và hai file dẫn xuất runs/g2-build-007/t032-dan-xuat.json (trường /by_cell), runs/g2-build-007/t033-dan-xuat.json (trường /by_cell và /bocpd_post_any_by_cell); (b) phần khác biệt giữa runs/phat-hanh-004/ và runs/phat-hanh-005/: mở đầu mục 5, UV-7, G2-H23, G2-H24, câu 16 mục 7; (c) các phần người làm ghi trong LOG là chưa tự đọc từng dòng: Phụ lục A, Phụ lục B, dòng đối chiếu B16 ở mục 6.2, mã E1/E2 và bài/mã TraceRCA; (d) tiêu chí xong của SPEC đối với từng dòng G2-Hn (số theo ô) và từng ứng viên K5; (e) phần (ii) của UV-7, người làm ghi trong LOG Phiên 6 là chưa xử lý. Nguồn tại results/T-001, T-002, T-008, T-021, T-022, T-024, T-025, T-026, T-028, T-029, T-032, T-033. Manifest nguồn tại results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json, manifest-review-001.json và old-files-before.json. Môi trường đọc và tính đối chiếu: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản REVIEW được phép ghi>.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

## Phiên 7 — 14/10/2026 — Claude — laptop — vai trò: người làm (đáp lượt Codex kiểm bản 007, sửa lượt cuối)

**Mở phiên:** cùng cuộc trò chuyện với Phiên 4–6. Codex báo 304 tệp khớp `runs/manifest-cuoi-006/manifest.json` và 2.827 số không lệch trước lượt sửa này.

**Công đoạn:** Codex kiểm bản 007 (Minh dán vào chat); tôi đáp trong chat (chỉ đọc), rồi sửa theo lời duyệt.

**Đánh giá phản biện:**

| Điểm của Codex | Kết luận của người làm | Bằng chứng riêng |
|---|---|---|
| Không thấy lỗi đáng kể mới; đề xuất dừng phản biện bản này | Đồng ý dừng | — |
| Bảng G2-H24 đã được Codex đối chiếu từng ca từ đầu ra BOCPD gốc của 30 ca | Chưa tự kiểm lại phép đối chiếu; chỉ xác nhận nguồn Codex dẫn có trên máy | `results/T-033/runs/session9-report-002/source-catalog.json` tồn tại; `results/T-033/runs/checkpoint-handoff-001/` có 31 file `dev-*--full.npz` |
| G2-H19, G2-H23, Phụ lục A và B, E1, E2 đạt theo phép kiểm của Codex | Ghi nhận; tôi không lặp lại | — |
| Câu hỏi cách gộp điểm nên đặt ở mục 6.1, không phải 6.3 | Đúng; trùng đề xuất lại của tôi ở Phiên 6 | Mục 6.3 của gói là “thuộc đánh giá sau khi khóa thiết kế” |

**Đính chính điều tôi ghi ở Phiên 6:** tôi viết 29/30 file gốc theo ca của T-033 “không có ở máy này”. Chính xác hơn: 29 file `dev-<ca>--context.json` mà `fast-summary-001.json` ghi mã băm không có trên laptop; đầu ra BOCPD gốc dạng NPZ của cả 30 ca thì có, ở thư mục bàn giao Codex dẫn. Tôi đã không tìm ở đó. Giới hạn “chỉ khớp mức tổng và một ca” là giới hạn phép kiểm của tôi, không phải của dữ liệu.

**Quyết định của Minh trong phiên** (nguyên lời): “duyệt toàn bộ đề xuất”, trả lời sáu mục đề xuất của lượt đáp. Tôi hiểu phạm vi như sau, theo đúng chữ của từng mục đã trình:
1. Lượt sửa cuối (chuyển câu hỏi cách gộp điểm sang mục 6.1; cập nhật ghi chú về G2-H24): **được làm**, đã làm ở phiên này.
2. Dừng phản biện T-034: Minh đồng ý dừng.
3. Trình nguyên văn dòng DECISIONS và dòng STATE để Minh duyệt rồi mới ghi: **chỉ được trình**, chưa được ghi.
4. Xét G2 theo mười điểm mục 8 của gói: đây là việc Minh làm; lời duyệt này **không** phải là duyệt G2.
5. Hai phép còn lại để sau G2, mỗi phép một đề xuất riêng: chưa giao.
6. Commit sau khi Minh nghiệm thu: chưa commit.

Chưa ghi DECISIONS.

**Diễn biến:**
- Chép bản đang phát hành vào `results/T-034/runs/phat-hanh-006/`.
- Sửa `scripts/mau/goi-g2.md`: mở đầu mục 5; UV-7 (bỏ phần cách gộp điểm, đổi tên); thêm một dòng ở mục 6.1 và sửa câu đếm dòng; câu 12 mục 7; dòng đầu về sổ số liệu. Không sửa script nào.
- Dựng vào `runs/g2-build-008/`. **V3 đạt** (68/68). **V4 đạt**: 2.827 số, 38 file nguồn, 0 lệch, 0 chữ số không nguồn. Không số nào đổi so với lượt 007.
- Viết `runs/g2-build-008/v5-bo-sung-sau-phan-bien-6.md` (kèm đính chính giới hạn G2-H24).
- Manifest `results/T-034/runs/manifest-cuoi-007/manifest.json`; so với manifest 006 ghi ở mục kiểm.
- Không kết nối EC2, không chạy thực nghiệm, không sửa STATE, không commit.

**Kết thúc phiên:**

1. **Đã làm gì:** đáp lượt Codex; sửa lượt cuối theo lời duyệt; dựng lại, kiểm lại.
2. **File đã thay đổi:** `results/T-034/goi-g2.md`, `ban-do-g2.json` (chỉ khác thời điểm dựng và đường dẫn file dẫn xuất của lượt), `scripts/mau/goi-g2.md`; các file mới của `runs/phat-hanh-006/`, `runs/g2-build-008/`, `runs/manifest-cuoi-007/`; LOG này.
3. **Kiểm đã chạy:** V3, V4 đạt trên lượt 008; so manifest 006 và 007; `hai-phep-kiem.md` trùng mã băm bản trước; đọc lại phần khác biệt giữa `runs/phat-hanh-006/goi-g2.md` và bản mới.
4. **Điều chưa chắc hoặc cần Minh quyết:**
   - *Task đạt gì:* theo tự đánh giá của người làm, tiêu chí xong của SPEC nay đạt theo chữ. Lượt sửa 008 chỉ đổi chỗ và lời văn; **chưa được người phản biện kiểm**, và tôi đã đề xuất không cần thêm vòng. Minh quyết.
   - *Câu hỏi nguồn trả lời tới đâu:* có bảng baseline trên dev và bản đồ hạn chế 26 dòng; cơ chế ở nhiều dòng vẫn “chưa phân xử”. Không đóng RQ2.
   - *Còn mở:* lan có đáng kể; đóng góp của chờ ở CIRCA; bước gây chênh hai bản TraceRCA; underflow ngoài hai ca; thời điểm sự cố bắt đầu; lựa chọn P6; lợi ích đồ thị.
   - *Chờ Minh:* duyệt nguyên văn dòng DECISIONS và dòng STATE (tôi trình trong chat); mười điểm mục 8 của gói, gồm duyệt G2; nghiệm thu T-034; commit.
5. **Bước tiếp theo chính xác:** Minh duyệt hoặc sửa các dòng DECISIONS và STATE tôi trình trong chat; rồi quyết mười điểm ở mục 8 của `results/T-034/goi-g2.md`. Nếu Minh muốn một vòng kiểm nữa, dùng prompt dưới đây.
6. **Lệnh cuối cùng đã chạy:** `python -B -X utf8 results/T-034/scripts/manifest_cuoi.py results/T-034/runs/manifest-cuoi-007`.

## Prompt bàn giao của lượt này cho agent đối phương (Codex, kiểm lại phản hồi và sửa) — soạn theo nghĩa vụ; người làm đề xuất dừng

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-034, tasks/T-034-g2-goi-trinh/SPEC.md, đã duyệt và khóa ngày 13/10/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3, P4; G2.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện.
- Tài liệu gốc: tasks/T-034-g2-goi-trinh/SPEC.md; docs/STATE.md; docs/MRP.md; docs/PLAN-P3-G2.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md. HEAD hiện tại của master: ff5e20a2; các file T-034 chưa commit. Bản phát hành trước ở results/T-034/runs/phat-hanh-006/.
- Phản biện và phản hồi trước: các lượt trong chat ngày 13/10 và 14/10/2026; phần người làm ghi nhận tại tasks/T-034-g2-goi-trinh/LOG.md, Phiên 1–7; các bản V5 bổ sung trong results/T-034/runs/g2-build-004/, g2-build-006/, g2-build-007/ và g2-build-008/. Chưa có bản REVIEW của T-034 trong repo.
- Code và kết quả liên quan: results/T-034/goi-g2.md; ban-do-g2.json; bang-baseline.json; hai-phep-kiem.md; hai-phep-kiem.json; thiet-ke-hai-phep-kiem.md; scripts/; runs/g2-build-008/ (lượt dùng để phát hành); runs/manifest-cuoi-007/manifest.json. Phần khác biệt giữa runs/phat-hanh-006/ và bản hiện tại: mở đầu mục 5, UV-7, mục 6.1, câu 12 mục 7, dòng mở đầu về sổ số liệu. Nguồn tại results/T-001, T-002, T-008, T-021, T-022, T-024, T-025, T-026, T-028, T-029, T-032, T-033. Manifest nguồn tại results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json, manifest-review-001.json và old-files-before.json. Môi trường đọc và tính đối chiếu: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -X utf8.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản REVIEW được phép ghi>.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

## Phiên 7 (nối) — 14/10/2026 — Claude — ghi sổ, cập nhật STATE, commit

**Quyết định của Minh** (nguyên lời): “duyệt sau đó commit và push”, trả lời ba dòng DECISIONS và dòng STATE tôi trình trong chat.

- Nối Q-146, Q-147, Q-148 vào cuối `docs/DECISIONS.md`, đúng nguyên văn đã trình.
- Thay ô trạng thái của dòng T-034 trong `docs/STATE.md`. **Lệch một cụm so với bản đã trình:** bản trình kết thúc bằng “Chưa commit”; vì Minh ra lệnh commit trong cùng lời duyệt, tôi ghi “Kết quả và LOG của task đã commit 14/10; thay đổi trong `docs/` chưa commit” để dòng trạng thái không sai sau khi commit.
- Commit và push: chỉ `results/T-034/` và `tasks/T-034-g2-goi-trinh/`, theo cách năm commit theo task gần nhất trên `master` đã làm. **Không commit `docs/`, `AGENTS.md`, `tasks/_MAU/`:** các file này đang mang thay đổi chưa commit của nhiều task khác; gộp vào commit của T-034 sẽ đưa lên remote những phần không thuộc lời duyệt này. Hệ quả: WHY-51, Q-146–Q-148 và dòng STATE của T-034 đã ghi trên máy nhưng **chưa** lên remote; cần Minh quyết commit `docs/` riêng.
- Không sửa file kết quả nào sau `runs/manifest-cuoi-007/`.

**Còn chờ Minh:** mười điểm ở mục 8 của `results/T-034/goi-g2.md` (gồm duyệt G2); nghiệm thu T-034; commit các file trong `docs/`.

## Phiên 7 (nối 2) — 14/10/2026 — Claude — ghi quyết định duyệt cổng G2

**Quyết định của Minh** (nguyên lời): “duyệt cổng, tạo prompt cho 1 phiên claude mới soạn spec cho p5 , codex sẽ là người làm, claude phản biện, tuân thủ work flow, prompt chuyên nghiệp”; rồi “duyệt đề xuất trước khi sang phiên mới”, trả lời đề xuất ghi Q-149 và dòng “Cổng hiện tại” của STATE.

- Nối Q-149 vào cuối `docs/DECISIONS.md`, đúng nguyên văn đã trình.
- Thêm vào đầu dòng “Cổng hiện tại” của `docs/STATE.md`: “G2 đã duyệt ngày 14/10/2026 (Q-149); kế tiếp là P5.”
- Prompt cho phiên Claude mới soạn đề xuất SPEC của P5 đã đưa Minh trong chat; không ghi thành file.
- Commit `25e71dc4` (đã push) chứa `results/T-034/` và thư mục task tới hết mục “Phiên 7 (nối)”. Mục này và các thay đổi trong `docs/` chưa commit.

**Chưa có lời của Minh, tôi không tự suy:** T-034 đã nghiệm thu hay chưa (dòng task trong STATE vẫn “Chờ Minh nghiệm thu”); chín điểm còn lại ở mục 8 của `results/T-034/goi-g2.md`; có commit các file trong `docs/` không.

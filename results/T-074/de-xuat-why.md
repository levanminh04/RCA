# T-074 — Các mục WHY đề xuất cho W6/W7 (chưa ghi `docs/WHY.md`)

- **Trạng thái:** đề xuất của Claude (phiên `danh-gia-w6`), 20/11/2026. Chưa phản biện, chưa Minh duyệt. Theo I6, chỉ phiên điều phối ghi `docs/WHY.md` sau khi Minh duyệt. Số WHY chính thức do phiên điều phối cấp (mục cuối hiện có: WHY-102).
- Mỗi mục: chọn gì; vì sao; phương án đã xét; bằng chứng; kết luận phụ thuộc; trạng thái. Chi tiết ở `thiet-ke-w6.md` (dẫn mục §).
- Mục nào phụ thuộc kết quả W4/W5 thì chỉ ghi được sau khi có kết quả đó, nhưng phải ghi **trước** lượt thu W7 đầu tiên.

---

## W6-A. Kiểm soát trạng thái DB trong đợt W7 (§5.3)

- **Chọn (ứng viên):** quy tắc khai trước dựa trên W4: trôi E2→E4 vượt mức T-072 đặt → K2 (khôi phục về mốc đầu mỗi khối, trộn trong khối) nếu E6 chứng minh khôi phục nhất quán; ngược lại K0 + ô mốc (K3).
- **Vì sao:** DB tích lũy làm truy vấn nền chậm dần trong một lượt (p50 ×~1,7 sau ~8,5 giờ, `results/T-069/phan-tich/troi-trong-luot.txt`); một đợt A+B+CPU-EVENT thêm tới 74.520 đơn (`du-toan.json`). Thứ tự chạy thành biến lẫn nếu không kiểm soát. Nguyên nhân mẫu đuôi ở T-069 chưa phân xử (`dinh-chinh-1.md` §2), nên không chọn khôi phục với lý do "DB là nguyên nhân".
- **Phương án đã xét:** K0 (giữ tích lũy), K1 (khôi phục một lần), K2, K3; thu nhỏ DB về ~4k đơn (bỏ: xóa dữ liệu nghiệp vụ, dễ bị hiểu là sửa cho giống điều kiện cũ).
- **Bằng chứng:** `thong-nhat.md` §1.2; `lich-su/04` §3–§5; `results/T-071/e1/suc-chua.json`.
- **Bốn điều kiện hợp lệ:** khai trước; áp như nhau mọi ô và mọi phương pháp; không chọn theo điểm (bảo đảm vì RCA chạy sau khi đóng đợt); báo cáo công khai hiện tượng trôi.
- **Kết luận phụ thuộc:** mọi so sánh theo ô của W7; phần "điều kiện khác nhau giữa đầu và cuối đợt".
- **Trạng thái:** CHỜ-MINH (Q-W6-01), CHỜ-W4, CHỜ E6.

## W6-B. Phạm vi ô đánh giá và hai nhóm báo cáo (§4)

- **Chọn:** chỉ ô cột "đánh giá" của T-059 vào nhóm "vị trí mới"; ô dev (T-063/T-064) chỉ vào nhóm "đã phát triển". Phạm vi A / A+B / A+B+C do Minh chọn.
- **Vì sao:** chia theo ô (DECISIONS T-059 11/11; WHY-04): chọn cấu hình rồi báo trên cùng dữ liệu thì số đẹp hơn thực tế. V082 được thiết kế sau khi xem tập chọn dev (`cau-hinh-de-xuat.json#/gioi_han`).
- **Phương án đã xét:** dùng lại ô dev làm đánh giá (trái WHY-04, chỉ được khi Minh duyệt ngoại lệ, KE-HOACH-GIAI-DOAN-TOI D.9); chỉ hạng A (ít ô); thêm B (đổi topology so với W4); thêm C (đổi image hoặc hỗn hợp tải).
- **Bằng chứng:** `thiet-ke-w6.md` §4.2 (đọc code `RcaFaults.java`, `inj3.py`, `proxies.json`, `purchase-journey.js`).
- **Kết luận phụ thuộc:** câu RQ5 "chuyển sang vị trí mới"; mọi khẳng định về họ lỗi cạnh/mạng/cache.
- **Trạng thái:** CHỜ-MINH (Q-W6-02).

## W6-C. Cường độ ô đánh giá chọn bằng đầu dò độc lập (§4.5)

- **Chọn:** cường độ và điều kiện xác nhận của ô đánh giá chốt bằng chế độ `d2` của runner (tiêm 150 s, đầu dò trước/trong/sau, không chạy RCA). Ô không xác nhận được ở pilot thì không vào đợt chính.
- **Vì sao:** cần can thiệp thật xảy ra (T-059 ba lớp nhãn) mà không nhìn điểm phương pháp. Chọn theo đầu dò không đưa nhãn vào phương pháp.
- **Phương án đã xét:** dùng cường độ của ô dev cùng họ (có thể không xác nhận được ở vị trí mới); chọn bằng thử RCA (bị loại: dùng dữ liệu đánh giá để thiết kế).
- **Bằng chứng:** `runner4.py::chay_d2`; T-063 `o-dev-bo-sung.md` (POOL-EVENT chọn 5 connection theo đầu dò).
- **Kết luận phụ thuộc:** tính hợp lệ của mọi ca "đã xác nhận".
- **Trạng thái:** ĐX.

## W6-D. Mức tải, số lần lặp, thứ tự (§5.1–§5.2)

- **Chọn:** mỗi ô đánh giá × {×1, ×3 cả chu kỳ} × 3 lần lặp; đối chứng BINH-THUONG ×1, BINH-THUONG-X3, FLASH-HEALTHY mỗi loại 3; trộn ngẫu nhiên theo khối cân bằng, seed khai trước.
- **Vì sao:** "hai mức tải của một ô đánh giá" (DECISIONS T-059); ba lần lặp đi cùng ô (WHY-04). ×3 cả chu kỳ thay flash vì flash của runner tăng bậc đúng tại t (`runner4.py::start_load`), làm tải và lỗi trùng mốc.
- **Phương án đã xét:** 1 lần lặp (rẻ, không đo được dao động trong ô); flash bậc tại t (trùng mốc); flash bậc tách khỏi t (cần đổi runner, chưa có cấu hình đã chạy).
- **Bằng chứng:** 31,40 phút/chu kỳ (`du-toan.json#/nguon`).
- **Kết luận phụ thuộc:** câu RQ5 "chịu điều kiện tải khác"; câu phụ RQ5 (tải đột biến vs sự cố) để OPEN.
- **Trạng thái:** ĐX.

## W6-E. Nhóm thông tin che của D14 và nhánh dự phòng (§3.3)

- **Chọn:** hai nhóm: G-live (kênh `live-down` của gói bổ sung → H5b) và G-inst (nhiều chuỗi runtime → H8a). H8s1 là phép tính, không che. Nhánh dự phòng G-live: chạy không có gói bổ sung (khóa P7 gốc). G-inst: Minh chọn giữa hành vi P7 (lỗi, tính trượt) và "giữ chuỗi mới nhất".
- **Vì sao:** D14 che thông tin phong phú, kể cả dẫn xuất (B1.9). V082 chỉ bật ba thành phần (`cau-hinh-de-xuat.json`).
- **Phương án đã xét:** che theo thành phần (đã làm ở T-069 bước 7.4, là phép bỏ thành phần); che cả nhóm trace/metric/log chung (không phải thông tin phong phú theo B1.9).
- **Bằng chứng:** `ho-so-chon.md` §15, §17; `dinh-chinh-1.md` §4.
- **Kết luận phụ thuộc:** câu "thông tin nào mang thay đổi V082 so với P7".
- **Điều kiện thất bại:** kiểm kê động (chạy V082 có/không từng nhóm trên ca dev) thấy đầu ra còn khác P7 ở chỗ không giải thích được → còn dẫn xuất chưa che, thêm nhóm, trình lại.
- **Trạng thái:** ĐX; CHỜ-MINH cho G-inst (Q-W6-04). Kiểm tĩnh đã làm: trong V082 chỉ `H5-liveness` đòi đầu vào bổ sung (`src/m1_ft/chay_ca.py:96`, `thanh_phan/h4_h5.py:93`); kiểm động chưa làm.

## W6-F. Thu trước, RCA sau; gói đầu vào không phụ thuộc đầu ra M1 (§8)

- **Chọn:** trong đợt chỉ chụp và niêm gói đầu vào (a) và (b); đóng đợt và băm danh sách; rồi mới chạy mọi phương pháp; chấm sau khi băm đầu ra. Thêm `safe_export.py case-input` (chỉ đòi manifest).
- **Vì sao:** §8.3 nguyên văn. `safe_export.py case` hiện đòi `summary.json` (đọc code). Chạy RCA sau khi đóng đợt làm điều kiện "không chọn theo kết quả" đúng về cấu trúc, và lỗi phương pháp không bao giờ buộc thu lại.
- **Vì sao vẫn phải chụp trong đợt:** `stage_m1.py` đọc tiền tố có giới hạn của file ghi vòng Collector; dời tới sau đợt thì capture có thể đã quay vòng (thời hạn giữ CHƯA-KIỂM).
- **Phương án đã xét:** giữ runner4 (M1 chạy trong đợt, gói phụ thuộc đầu ra); đọc qua API Tempo/Loki/Prometheus sau đợt (P9b, chưa có; Tempo giữ 14 ngày).
- **Kết luận phụ thuộc:** tính độc lập của mọi số W7.
- **Trạng thái:** ĐX.

## W6-G. Quy tắc gói hợp lệ và thay thế (§8.4)

- **Chọn:** năm điều kiện (sổ đủ, can thiệp xác nhận, tải khỏe ở N, telemetry đủ, niêm khớp). Ca không hợp lệ giữ và báo riêng. Thay thế chỉ vì hạ tầng, tối đa 1 lần/slot, lịch con cuối đợt.
- **Vì sao:** luật 10 (giữ mọi lượt), luật 21 (lỗi một slot chỉ chặn slot đó), T-059 (ba lớp nhãn).
- **Phương án đã xét:** không thay thế (mất cân bằng ô khi hạ tầng lỗi); thay không giới hạn (rủi ro chọn ca).
- **Trạng thái:** ĐX; mức "số mẫu tối thiểu" đặt ở pilot, tiêu chí khỏe CHỜ-W4.

## W6-H. Mốc của độ trễ phát hiện (R-07) (§6)

- **Chọn:** mặc định "độ trễ theo mốc tiêm" (t̂ − t). Đầu dò dòng thời gian k6 theo route chỉ khi Minh chọn kết luận theo thời điểm bắt đầu tác động.
- **Vì sao:** §8.3 nguyên văn; MRP P7 "Độ đo" (gọi đúng tên mốc). Mốc onset phải lấy từ tín hiệu bộ chẩn đoán không dùng (R-07; SL18).
- **Phương án đã xét:** onset từ Prometheus (bị loại: cùng nguồn với RCA và luật).
- **Kết luận phụ thuộc:** RQ3a phần độ trễ; nhãn vùng mức endpoint (§9.3).
- **Trạng thái:** CHỜ-MINH (Q-W6-05); chi phí phụ thuộc k6 có ghi từng request (CHƯA-KIỂM).

## W6-I. Ghép sự cố với cửa sổ và độ đo phát hiện (§9.1)

- **Chọn:** cửa sổ dương = đoạn lỗi của ca đã xác nhận; ghép khi t̂ ∈ `[t, t+600+G)`, G = 120 s; trùng tính một lần; đoạn hồi phục không chấm; báo động giả trên đoạn nền và ca đối chứng khỏe.
- **Vì sao:** P/R/F1 theo cửa sổ (MRP P7). G cho phép luật có `for` và nhịp đánh giá; giá trị cụ thể phải ≥ độ trễ tối đa hợp lệ của luật (`for` + `eval_interval` + khoảng nhìn lùi) → CHỜ-W4.
- **Phương án đã xét:** G = 0 (phạt luật có `for`); tính đoạn hồi phục là âm (phạt sự cố kéo dài thật).
- **Trạng thái:** ĐX, CHỜ-W4 (quy tắc gom, G).

## W6-J. Chấm xếp hạng ở chế độ (b) (§9.2)

- **Chọn:** ca không có sự cố ghép giữ trong mẫu số (trượt); báo thêm nhóm có cảnh báo. Nhiều sự cố ghép: chấm sự cố t̂ sớm nhất.
- **Vì sao:** §8.3 nguyên văn ("giữ ca không có cảnh báo trong mẫu số"). Chọn sớm nhất là quy tắc không nhìn đầu ra.
- **Phương án đã xét:** chấm sự cố có điểm tốt nhất (bị loại: chọn theo kết quả); trung bình các sự cố (làm mờ ca).
- **Trạng thái:** ĐX.

## W6-K. Baseline và adapter FlashTicket (§7)

- **Chọn:** SimpleRCA (M4, quy ước T-017) bắt buộc; BARO RobustScorer (RCAEval 259ea41) đưa vào. Adapter dùng thực thể inventory T-037 như M1; BARO `dk_select_useful=False`; quy ước SimpleRCA giữ nguyên WHY-17. Phép kiểm không nhãn trên dev (17 gói T-069, gói T-063) trước khi khóa.
- **Vì sao:** QT7 (baseline mạnh; số công bố SimpleRCA top-1 0,80 trên RE2-TT, ST9); §8.3; QT2 (prior work là mặc định).
- **Phương án đã xét:** thêm MicroRank/TraceRCA/Nezha (chi phí adapter chưa ước lượng); chỉ SimpleRCA.
- **Kết luận phụ thuộc:** câu "so với baseline" trên FlashTicket.
- **Trạng thái:** ĐX; Q-W6-07 cho baseline thêm.

## W6-L. Dùng lại 17 gói T-069 cho nhóm "đã phát triển" ở chế độ (a) (§4.4)

- **Chọn:** chạy baseline, bản che, đối chứng quan hệ trên gói T-069 đã có; báo là nhóm "đã phát triển, thu trước khóa W6".
- **Vì sao:** luật 20 (dùng lại kết quả còn hợp lệ). Gói có hash (`results/T-069/SHA256SUMS*`).
- **Giới hạn:** thu trước khóa; DB khác trạng thái W7; người làm đã xem kết quả (ô tụt CPU-BOOK-1). Không bao giờ vào nhóm "vị trí mới".
- **Trạng thái:** ĐX.

## W6-M. Đối chứng quan hệ chỉ tính toán (§3.4)

- **Chọn:** chạy `DC-bo-quan-he` trên V082 và C-d1/C-d2/C-d3 trên mọi gói W7.
- **Vì sao:** QT8 và RQ3d cần cả hai đối chứng trước khi nói lợi đến từ việc dùng quan hệ. Không tốn giờ máy thu.
- **Giới hạn:** không có đối chứng đồ thị ngẫu nhiên (M-25).
- **Trạng thái:** ĐX.

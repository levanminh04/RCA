# T-033 — Checkpoint hiện trạng để Claude kiểm độc lập

Chốt ngày 2026-10-10T12:12:46.246158+07:00. Task đang thực hiện, chưa nghiệm thu. Codex là người làm; Claude là người phản biện. Minh yêu cầu chốt đầy đủ hiện trạng để kiểm; chưa duyệt sửa guard hoặc chặng tính tiếp trong lượt này.

## Điểm vào và cách tìm bằng chứng

1. Đọc `AGENTS.md`, `tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md`, mục phiên 3 của `LOG.md`, dòng T-033 trong `docs/STATE.md`.
2. Đối chiếu mục tiêu RQ2/P4 trong `docs/MRP.md`, DT18 §2 NV2/NV3, advisor-2026-09-23.md §1 và các nguồn lý do/quyết định trực tiếp. File chỉ mục không thay đọc các nguồn đó.
3. `snapshot.json`: trạng thái EC2 cuối, `/statuses`, `/manifests_verified`, `/factorial_reuse`, `/run_durations_from_status`, `/resources`. `artifact-inventory.json`: SHA và byte từng file gốc trong gói. `receive-status.json`: hash toàn archive khi truyền, trạng thái nhận. `local-verification.json`: kiểm lại file trên laptop và phạm vi ghi.
4. `artifact-locator.json`: tìm record/NPZ theo ca và nhánh; các đường dẫn trong locator tính từ `artifacts/`. `artifacts/` là bản nhận nguyên file EC2, không sửa số hoặc đường dẫn bên trong. Một số record mang đường dẫn EC2, dùng locator để tìm bản cùng SHA trong checkpoint.
5. `source-native/` chứa code native/adapter đúng hash input nguồn; `native-source-manifest.json` khóa SHA. Dùng để đọc, không thay môi trường triển khai. `artifacts/scripts/` là script từng chạy trên EC2; `results/T-033/scripts/` có thêm script chuẩn bị chưa chạy. Các snapshot script lịch sử trong `artifacts/runs/prepare-001/` vẫn giữ.
6. Prompt trung tính theo mẫu ở `prompt-claude.md`, cũng được chép trong LOG phiên 3. Phạm vi hiện tại: chỉ đọc và trả lời trong chat; chưa cấp quyền ghi REVIEW. Thư mục task được liệt kê trước chốt và chưa có REVIEW.

## Trạng thái các chặng — FACT từ file

| Chặng | Bằng chứng hiện có | Phần chưa làm |
|---|---|---|
| Chuẩn bị | Source/allowlist/env/index và nhóm ban đầu: `artifacts/runs/preflight-002/`, `artifacts/inputs/`; `results/T-033/bao-phu-nhom.json` | Độ phủ đọc tay thực tế và nhóm bổ sung sau factorial |
| N-Sigma lõi | Hai bộ cột, 60 record; `artifacts/runs/nsigma-first-001/`, `nsigma-rest-001/`; mean/std/count/flags và nguồn đã tự kiểm | Diễn giải ca/điểm có đối chứng |
| BOCPD lõi | Full và PP của 30 ca, FF kiểm prefix; `bocpd-first-001`, `full-metadata-recheck-001`, `bocpd-first-002`, `bocpd-rest-001`; tự kiểm chung `core-audit-002/verification.json` gồm 120 record N-Sigma/BOCPD | Phân tích đường likelihood/posterior/MAP tới báo sau proxy |
| FP/PF | Pilot và rest đều PASS; 30 ca × 2 hybrid, có 29 ca mới và tái dùng pilot. Rest kết thúc 10:27:24 ngày 10/10 +07, exit 0; `artifacts/runs/bocpd-factorial-rest-001/status.json`, manifest và `*--factorial.json` | Diễn giải các contrasts, khóa nhóm/đối chứng mới và chuỗi tính tay |
| N-Sigma nền cố định | Pilot/rest đủ 60 đơn vị; thống kê được đối chiếu độc lập từ Series gốc; `artifacts/runs/nsigma-frozen-*/` | Diễn giải nguyên nhân chênh ngưỡng theo ca/điểm |
| Độ trễ/kênh/đọc tay | Có trung gian lõi và script chuẩn bị; chưa có run delay/channel | Phần độ trễ, mật độ/chuỗi cờ, trace/log/workload, đọc tay/đối chứng theo SPEC |
| Tổng hợp | Checkpoint kỹ thuật hiện trạng | Báo cáo năm đầu ra P4, căn cứ P6, kiểm tiếp và nghiệm thu |

Các trạng thái PASS trên là kết quả tự kiểm phát lại, driver và manifest. Câu hỏi cơ chế, nguồn vật lý, quyết định P6 và G2 vẫn OPEN. `output-presence.json` liệt kê từng đầu ra SPEC đã/chưa tồn tại ở cấp gốc; không tạo báo cáo nghiên cứu để giả hoàn tất task.

## Lượt lỗi và con trỏ tái dùng

- `bocpd-first-001` STOPPED vì metadata cột wrapper; nguyên trung gian giữ lại. `full-metadata-recheck-001` kiểm hash và dựng metadata đúng từ nguyên R/maxes; `bocpd-first-002` dùng full đã xác minh, không viết lại lượt lỗi. Đọc record và LOG để phân biệt schema với số/CP.
- `core-audit-001` STOPPED do giải nén ma trận predictive trong vòng lặp; giữ stdout/stderr/progress. `core-audit-002` đưa đọc array ra ngoài loop, giữ assert, PASS. Không chạy lại detector trong phép tự kiểm này.
- Hai branch của ca pilot trong factorial rest có `reused_record`; NPZ nằm trong `bocpd-factorial-first-001`, không phải rest. `artifact-locator.json#/factorial` nối đúng record/NPZ này.
- `bao-phu-nhom.json` hiện chỉ khóa nhóm ban đầu; trạng thái NOT_YET_REPLAYED_OR_READ trong bảng là lịch sử khóa, chưa được cập nhật thành bằng chứng cơ chế.

## Guard và ngân sách — OPEN

SPEC dòng 195 dự trù 4–12 giờ máy và ghi "Đây không là timeout". Guard Codex cài lấy thời gian lịch từ `nsigma-first-001/status.json#/started_utc`, gồm khoảng nghỉ, thành hạn 11:46:29 ngày 10/10 +07. Mốc này không phải thời hạn Minh đặt và không chứng minh đã dùng hết giờ xử lý. Các câu trong LOG phiên 1/2 gọi đây là giới hạn đã duyệt được đính chính bởi phiên 3; lịch sử không bị sửa.

Đề xuất chuyển sang tổng thời gian các lượt xử lý, tính cả lượt hỏng/kiểm, giữ trần 12 giờ và 4 GiB: CANDIDATE, chưa Minh duyệt. Code và input budget chưa đổi. `/sum_available_run_wall_s` trong snapshot chỉ là tổng wall của các run có status; có phần chạy song song, chưa bao quát mọi audit/preflight/khoảng EC2 chờ và không là hóa đơn AWS. Chưa dùng nó để cấp giờ còn lại hoặc khởi run.

Đóng gói tạo thêm archive EC2 và bản nhận laptop; nhận trực tiếp không giữ archive thứ hai trên laptop. `local-verification.json#/storage` ghi dung lượng thực tế cả hai nơi sau chốt. Giữ archive/lượt cũ; nếu phần tiếp theo làm vượt 4 GiB thì checkpoint và trình Minh, không tự xóa hoặc nới giới hạn. Guard thời gian hiện chưa sửa.

## EC2 và cách kiểm lại chỉ đọc

Không còn worker T-033 hoặc tmux session T-033; lô cuối đã PASS trước mốc guard. EC2 vẫn bật, chưa tự tắt. Bản gói đầy đủ đã có trên laptop để Claude kiểm code/metadata/trung gian; nguồn dữ liệu dev và môi trường tính vẫn ở EC2. Task còn cần EC2 nếu tiếp các chặng chưa làm. Minh có thể tắt laptop sau khi nhận xong; chưa có công việc nghiên cứu mới chạy nền.

```powershell
ssh -i D:/RCA-ext/keys/keys.pem -o UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes ubuntu@3.107.246.249 'cat ~/rca/T-033/runs/bocpd-factorial-rest-001.exit; tail -n 20 ~/rca/T-033/trang-thai.txt'
```

Nguồn được phép: allowlist trong `artifacts/inputs/source.json`; raw dev tại `/home/ubuntu/rca/T-025/repo/data/rcaeval/`. Code native tại `/home/ubuntu/rca/T-025/src/baro`, adapter tại `/home/ubuntu/rca/T-025/repo/src/p3/`; Python `/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8`, NumPy 1.26.4, pandas 2.2.3. Đọc version/provenance trong `artifacts/runs/preflight-002/environment.json` và từng status. Laptop chỉ xử lý tài liệu/metadata/nhận file; tính toán nghiên cứu trên EC2. Không thực nghiệm mới, không nguồn khóa/test/giữ ngoài, không vùng kết quả T-032, không sửa nguồn cũ.

## Sau lượt kiểm hiện trạng

Minh chuyển prompt thủ công cho Claude; Claude trả lời trong chat nếu chưa có quyền REVIEW riêng. Codex giữ vai trò người làm, nhận các nhận xét để kiểm và trình phương án. Chỉ tiếp nghiên cứu/sửa guard theo quyền Minh quyết; không tự coi yêu cầu chốt checkpoint là duyệt đề xuất trước đó. Chưa nghiệm thu T-033 hoặc đóng RQ2/G2.

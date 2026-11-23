Việc phụ CX-01 (chỉ đọc, không sửa file, không SSH, không commit). Repo RCA D:\RCA-flashticket; repo lab D:/Project/flashticket-rca-lab tại commit 407b4f5 (đọc bằng `git -C D:/Project/flashticket-rca-lab show 407b4f5:<đường>`).
Kiểm từng khẳng định dưới đây trên code thật. Mỗi khẳng định trả lời ĐÚNG / SAI / ĐÚNG MỘT PHẦN, kèm file:dòng và trích đoạn ngắn. Không suy luận ngoài code.
K1. campaigns/runner/runner4.py gọi stage_m1.py, run_m1.py, safe_export.py, xuat_bo_sung.py, sau_v082.py bằng đường dẫn trong cây git REPO tại thời điểm gọi (không nạp trước), nên đổi `git checkout` của /opt/rca-lab giữa lượt làm đổi code chạy.
K2. runner4.py m1_worker chạy stage_m1 (gọi collect_metrics trên Prometheus 127.0.0.1:9090) và xuat_bo_sung (truy vấn localhost:9090) trong lúc chu kỳ tải kế tiếp đang chạy.
K3. File STOP: runner4.py dùng /srv/rca-lab/runs/STOP chung cho mọi lượt; load/controller/tai_linux.py dùng <RCA_LAB_LOAD_STATE>/STOP chung; cả hai không phân theo lượt.
K4. tai_linux.py chặn hai lượt tải chồng (flock + kiểm container rca-tai-) nhưng không kiểm trạng thái tiêm lỗi.
K5. observability/compose.yaml gắn ./grafana/provisioning vào Grafana và ${RCA_LAB_DATA}/rca-results vào thư mục public của Grafana; campaigns/runner/sau_v082.py ghi chỉ mục vào /srv/rca-lab/rca-results/t065-l11-001/.
K6. tai_linux.py: --seconds tối đa 3600; tăng bậc chỉ khi tokens minRefreshRemaining > step + 60; load/scenarios/purchase-journey.js giới hạn seconds ≤ 3600.
K7. campaigns/runner/stage_m1.py ghi 'mode':'a' cố định và đọc capture từ RCA_CAPTURE (mặc định /srv/rca-lab/collector-gateway/capture).
Rồi: nêu thêm bất kỳ đường code nào khiến hai phiên cùng chạy (một phiên đo tải nền bằng tai_linux.py, một phiên phát triển dịch vụ RCA đọc capture/Prometheus trên exp-obs) có thể làm hỏng dữ liệu của nhau, nếu thấy; không thấy thì nói không thấy.
Trả lời tiếng Việt, ngắn, dạng bảng.

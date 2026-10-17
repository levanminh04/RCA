# Chẩn đoán một ca MicroRank trên laptop nguồn — CHỜ MINH DUYỆT

## Chỗ bị chặn và bằng chứng

Cohort EC2 đã tự dừng tại RE2-TT `dev-3defe3d34b`, không retry, không bỏ ca và không tăng ngưỡng. Nguồn đã kiểm hash hai đầu ở `runs/microrank-cohort-failure-001/transport-check.json`. Các con trỏ dưới đây thuộc `failed-case/roundoff-comparison.json` trong cùng thư mục:

- `/numeric_summary/max_ulp_distance`: 41, vượt 16 ULP; `/max_relative`: 4,731118408006869e-15, vượt 16×2^-52 (~3,553e-15).
- `/numeric_summary/beyond_threshold_count`: 126 trường điểm trên 179 cặp đã ghép; 107 operation và 19 service, đếm từ `/score_checks/*/{kind,check/pass}`. Không phải 126 operation.
- `/native_observed_exact/pass`, `/service_order_exact`, `/service_tie_partition_exact`, `/hit_metrics/pass`: đều true; `/outside_whitelist_differences`: rỗng. Bộ ghi không làm đổi đầu ra trong ca này. Chưa xác định thành phần môi trường hoặc bước số học gây khác nguồn.
- `/t028_flags/status`: NOT_PERFORMED. Wrapper đã dừng trước bridge T-028; không nhận cờ M của ca lỗi đã khớp, không dùng trung gian ca lỗi làm bằng chứng.

`cohort/52-cases.json#/overall`: 10 ca đạt (gồm hai pilot đã tái kiểm), một ca blocked, 41 ca chưa chạy. RE2: 2 exact, 5 numeric_only, 2 operation_order, 1 blocked, 20 not_run. Nezha: 1 exact, 21 not_run. Hai ca ERROR trong nhóm exact không có cặp điểm; ULP/tương đối là null, không ghi bằng 0. Bảng đủ 52 hàng ở `runs/microrank-cohort-failure-001/52-cases.md`.

Hậu quả: lõi MicroRank chưa đạt; A′ tiếp tục bị chặn. Ngưỡng đã khóa giữ nguyên. BARO, coverage, SimpleRCA và các phần độc lập vẫn có thể tiếp tục.

## Phương án đề nghị

Chỉ chẩn đoán đúng ca đã dừng trên laptop tạo kết quả gốc, dùng môi trường `D:/RCA-ext/envs/T-014-main/Scripts/python.exe` theo `results/T-031/moi-truong.json#/lenh_chay` và `/moi_truong/T-014-main`. Đây là ngoại lệ cần Minh duyệt đối với điều khoản tính toán EC2-only của SPEC.

Phạm vi cụ thể sau duyệt:

1. Tạo `results/T-032/scripts/diagnose_microrank_laptop_v1.py` và `start_microrank_laptop_diagnostic_001.ps1`. Chỉ wrapper điều phối/quan sát, không sửa code phương pháp, adapter, SPEC, comparator, bộ ghi cũ, môi trường hoặc dữ liệu. Soát code/pin trước chạy.
2. Đọc đúng dữ liệu dev trong allowlist của ca này, kiểm hash nguồn/đầu vào/F/cấu hình/code trước và sau. Khóa Python 3.12.10, các package theo nguồn, hashseed=0 và các biến thread theo nguồn; lưu môi trường thực đo. Không cài package hoặc tự đổi cấu hình nếu không khớp. Nhãn chỉ dùng sau phương pháp để đánh giá; không đưa tên ca hay thông tin nhãn vào payload MicroRank.
3. Một lượt native không bộ ghi, so tuyệt đối các trường tính toán/điểm/thứ tự/hòa/counts với frozen, chỉ loại `run_id` và `cost` như phép so exact gốc. Nếu lệch thì dừng, giữ lỗi và trình; không chạy lượt có bộ ghi.
4. Chỉ nếu native khớp frozen: một lượt cùng đầu vào có bộ ghi đã khóa, kiểm trung gian, rồi so tuyệt đối observed–native và observed–frozen. Không tolerance cho laptop, không sửa ranking và không làm tròn để khớp. Tối đa hai lượt phương pháp, không retry.
5. Chỉ ghi output mới ở `results/T-032/runs/microrank-laptop-diagnostic-001/`, có command, PID, progress, stdout/stderr, môi trường, cost, source/artifact manifest và verdict. Giữ mọi phần hỏng. Đây chỉ là chẩn đoán một ca; chưa cấp quyền chạy cohort laptop, chạy tiếp cohort EC2 hay A′.
6. Ghi LOG và riêng dòng T-032 của STATE theo quyền hiện có. Không sửa WHY-42. Sau kết quả, trình đoạn WHY bổ sung cho Minh duyệt trước dùng kết quả MicroRank trong báo cáo.

Không suy “cùng laptop sẽ exact”. Nếu laptop exact, bằng chứng chỉ giúp khoanh vùng bất đồng giữa các lượt/môi trường, chưa xác định nguyên nhân drift và không khôi phục partition lịch sử. Nếu vẫn lệch, giữ OPEN và trình phương án tiếp, không tăng ngưỡng.

## Chi phí, điều kiện vận hành và phương án thay thế

- Đề nghị trần gộp **10 phút máy, 150 MiB mới**, nằm trong tổng 8 GiB đã duyệt; quá trần dừng/trình, không xóa lượt cũ. Dự kiến 1–3 phút là **chưa đo trên laptop**, không cam kết: ca EC2 vừa đo khoảng 39,856 giây cho native/capture/kiểm; không coi đây là dự toán chính xác cho máy khác.
- EC2 đã đo peak tree RSS cohort 2.143.158.272 byte. Trước chạy laptop đo RAM còn trống; dùng dự trù bảo thủ 2×peak đã đo cộng 256 MiB khoảng trống. Đây là điều kiện vận hành đề xuất, chưa là chứng minh upper bound. Thiếu RAM thì không chạy, trình Minh; guard thực đo dừng nếu tài nguyên/giờ/dung lượng không đủ. Laptop phải mở suốt lượt chẩn đoán; không chạy dài/qua đêm trên laptop trong quyền này.
- Phương án thay thế ít công hơn: giữ MicroRank/A′ OPEN và tiếp phần độc lập trên EC2; chưa đáp ứng lõi MicroRank/A′, không coi task đã xong.
- Chạy lại cùng ca/cùng EC2 chưa có căn cứ sẽ sửa khác biệt; tăng tolerance trái lời duyệt, không đề nghị. Mô phỏng môi trường Windows khác máy hoặc chạy đủ 52 trên laptop chưa có dự toán/phạm vi duyệt; chỉ trình nếu chẩn đoán này cho bằng chứng cần thiết.

## Một dòng quyết định xin phép nối cùng lời duyệt

Đọc lại `docs/DECISIONS.md` ngay trước nối; nếu Q-97 đã được dùng thì dừng trình, không ghi đè. Giữ mọi dòng cũ:

| Q-97 | 10/10/2026 | Minh duyệt đúng results/T-032/de-xuat-microrank-laptop-001.md: ngoại lệ EC2-only chỉ cho chẩn đoán ca RE2 dev-3defe3d34b trên laptop nguồn, tối đa một native và một observed khi native khớp frozen, so tuyệt đối; tối đa 10 phút/150 MiB trong tổng 8 GiB, kiểm nguồn/môi trường/tài nguyên trước, lỗi dừng/không retry/không tăng ngưỡng; chỉ ghi wrapper và run mới T-032, chưa chạy cohort/A′, chưa sửa WHY-42; kết quả cần trình WHY bổ sung trước dùng trong báo cáo. | lời duyệt Minh; results/T-032/de-xuat-microrank-laptop-001.md |

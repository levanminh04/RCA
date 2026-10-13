# T-033 — Tự soát script trước lượt mới, phiên 4

Đây là đầu vào tự soát của người làm, không phải phản biện chính thức của Claude. Không có fixture hay tính nghiên cứu EC2 trong phiên này. Các nhận xét trợ lý dưới đây cần Codex tự đọc và kiểm trước sửa/chạy. Hash script hiện tại và phép AST của người làm nằm trong `script-reading-evidence.json`.

## Chứng cứ người làm đã kiểm trực tiếp

`results/T-033/scripts/channel_context.py` dùng key literal `status` ở dòng 229 và 246 trong cùng dict. Dòng 229 khai `OBSERVED_ARTIFACT`; dòng 246 khai dict mô tả statusCode, ghi đè trạng thái kênh. Đọc đoạn code và AST độc lập cùng xác nhận. Chưa chạy script, chưa có số nghiên cứu mới bị dùng từ lỗi này.

Hậu quả: đầu ra mất trạng thái kênh trace, không đáp ứng schema diễn giải kênh quan sát. Sửa cài đặt tối thiểu ở phiên tiếp: giữ `status` cho trạng thái kênh; đổi key statusCode ở dòng 246 thành `status_code`; kiểm readback và fixture hiện có trên EC2. Giữ bản cũ và hash hai đầu. Không đổi counts, định nghĩa hoặc SPEC. Phần kênh phụ thuộc dừng trước pilot đến khi sửa/kiểm đạt.

## Báo cáo trợ lý đọc hai script độ trễ — chưa phải kiểm EC2 của người làm

Trợ lý `bocpd_contract` đọc toàn hai script, SPEC và bốn file native; báo hash/dung lượng native khớp manifest. BOCPD giữ `m[i]=argmax R[:,i+1]`, CP `|Δm|>1`, sentinel/index/time, non-OK riêng và chuỗi True liên tiếp; dựng mass/normalizer/posterior, constant hazard và theta/predictive pointer phù hợp contract khi đọc code. N-Sigma giữ strict `>`, bắt đầu 100, cờ và mẫu số native, thống kê hữu hạn và chuỗi cờ. Chưa chạy assert trên dữ liệu EC2; người làm chưa hoàn tất đọc độc lập toàn hai script trong phiên này.

Các thiếu sót cài đặt trợ lý chỉ ra, cần người làm xác nhận trước sửa:

1. `nsigma_delay.py` dòng 9–10 chưa neo hash `source.json`; dòng 34 đọc record chưa kiểm qua manifest; dòng 35 chỉ kiểm NPZ theo hash chính record. Cần neo source/status/manifest/record/NPZ của lượt PASS và ghi nguồn vào manifest mới; chưa phải bằng chứng số cũ sai.
2. N-Sigma dòng 72–75 ghi kết quả sau toàn lô, chưa lifecycle/PID/progress/stdout/stderr/STOP/storage guard/manifest và khóa môi trường EC2. Cần ghi theo đơn vị hợp lệ, có checkpoint.
3. N-Sigma tên lượt cố định và xử lý toàn bộ; BOCPD có `--run` nhưng dòng 369 xử lý toàn bộ. Cần điều phối ca đầu rồi phần còn lại, tái dùng pilot đã neo hash; không chạy trùng hay chạy lại PASS. Giữ phép tính.
4. Guard BOCPD dòng 121–123, 147–149 vẫn lấy lịch từ lượt đầu. **Minh đã duyệt sửa guard trong phiên này**, không còn chờ duyệt nguyên tắc; chưa thực hiện sửa/ledger. Báo cáo trợ lý viện checkpoint cũ là OPEN chỉ phản ánh quyền ở phiên 3.
5. N-Sigma có chỉ số báo đầu nhưng cần người làm kiểm bổ sung timestamp/độ lệch có dấu của báo đầu, số điểm/thời gian theo dõi hậu proxy, phạm vi trung gian proxy→báo đầu/cuối và cột bật cờ theo SPEC. Giữ mẫu số native và cờ False của NaN; không tự đổi tiêu chí. Chẩn đoán hữu hạn của x/mean/std là đề xuất chưa kiểm của trợ lý, không là định nghĩa đã quyết.

## Báo cáo trợ lý đọc script kênh — chưa phải kiểm EC2 của người làm

Trợ lý `nsigma_contract` đọc script, SPEC, loader `cua_so.py`, T-002 card/code parent và checkpoint metadata. Báo hash các pin local loader/card/parent và source/preflight/core-first khớp inventory. Chuyển trace clock dùng US=1000000; có kiểm `startTime//1000==startTimeMillis`; logs giữ giây nguyên. Root-or-empty-parent theo T-002. Distinct observed traceID/root traceID là proxy, không gọi request thật; duration unit và nghĩa status raw vẫn OPEN. Workload giữ mọi `*_workload` raw/NaN/Inf; missing log N/A không thành zero; coverage OPEN; giữ off-grid, hash UTF-8 message và vị trí parquet.

Fixture code có kiểm tính tay nhưng **chưa chạy fixture EC2**, chưa kiểm schema/readback từng file, RAM/dung lượng/runtime. Tạo run với `exist_ok=False`; default rest bỏ entry0 sau `--first`, nhưng tên run mới không tự tìm đơn vị PASS trước đó: người làm phải kiểm unit/process và chọn `--cases` trước rest. Guard kênh dòng 81–91 vẫn calendar, chưa sửa.

**Trần 4 GiB chỉ tính đầu ra EC2** theo lời Minh mới; mô tả combined storage trong checkpoint lịch sử không áp dụng cho ngân sách hiện tại. Laptop hash/metadata là kiểm điều khiển, không tính nghiên cứu.

## OPEN và thứ tự tiếp

Trước khởi run: tự đọc lại ba script và native; ledger giờ xử lý gồm lượt hỏng/kiểm, giữ guard cũ, sửa đúng guard, hash hai đầu; chỉ xóa archive đúng lời duyệt sau tự kiểm bản laptop. Đọc MRP/DT18/advisor/LESSONS/WHY-41 trực tiếp trước chọn/diễn giải. Mỗi script pilot nền độc lập SSH → kiểm nguồn/CP/cờ/trung gian/fixture/schema và đo time/RAM/bytes → rest không trùng. Sau phân rã cập nhật khóa nhóm và đối chứng theo SPEC. Không suy cơ chế từ counts; giữ input trùng/collapse hợp lệ/không kênh/lỗi cùng mẫu số riêng. Khóa nhóm, đọc tay và tổng hợp chưa làm.

# Vận hành checkpoint005 — chưa phát main

Đọc reports/tu-soat-005/bao-cao.md và LOG phiên6. Kiểm chỉ đọc:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/trien-khai-005/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-005.json
```

Hiện chỉ được chuẩn bị/kiểm DEV như đã cấp; không đổi cờ G3/test hoặc phát plan giả. Không chạy lại helper create-only cũ. Giữ G2/pilot hợp lệ.

Sau G3/grant đúng phạm vi: (1) tạo bản LOCKED của protocol/policy theo đúng code/config/env/placement được Minh duyệt; ghi nguồn quyền cụ thể, không lấy fixture làm quyền. (2) materialize/attest metadata runtime/independent/binding từ G1 và nguồn gốc đúng94ca, C-e verified/insufficient; A đúng3CSVcohort và grant riêng. Không dùng nhãn/path vào phương pháp. (3) API materialize_main.build(protocol_ref,bundle_ref,grant,destination) biên dịch child plan/authority từng host+aggregate bất biến; kiểm full lock trước phát. Không có auto-dispatch.

Gói freeze007 chứa code/metadata công khai; không chứa nhãn/private source/test telemetry. Chuyển TT theo transfer-plan005 sau grant; hash đích đủ90tệp/máy và code đủ trước chạy. Future main roots khác nhau theo ec2_1/ec2_2 trong dispatch-contract005-final, không dùng cùng prefix của DEV. Bundle/private refs dùng path tương đối code root để có thể chạy trên Linux; nguồn quyền/executable dùng đúng bản từng host. Giữ nguyên metadata fingerprint nguồn khi đổi data_root, không sửa source_row hoặc nhãn để cho khớp.

Mỗi máy dùng main executable đã ghim với p7.py run/resume --plan <path> --sha256 <pin> --authority <path> --authority-sha256 <pin>. p7.py khởi supervisor độc lập SSH; dùng status đọc, drain ngừng phát và để active seal, resume cùng plan/root để nhận token/PID. Không auto retry. Không tự đổi chủ lô khi mất SSH; kiểm controller/PID/attempt rồi mới quyết. Trước phát chừa RAM/đĩa theo plan; laptop cắm điện/không sleep phải được xác minh, không giả định. Không tự bật/tắt EC2 hoặc Scheduled Task.

Nhận mỗi lô vào vùng mới dưới results/T-054, giữ archive/manifest/receipt/envelope gốc. Kiểm hash+bytes tất cả tệp nhận, không sửa đường dẫn trong nội dung. Trong **cùng một process Python**: gọi bien_nhan.receive_paths({remote_ec2_1_code_root:local_received1, remote_ec2_2_code_root:local_received2}); load plan/snapshot bằng read_pin; nguon.authorize(aggregate_plan,authority,'report') kiểm toàn child plan; đối chiếu parts với execution_plan_refs đã khóa; cham.merge_partitions(aggregate_plan,parts) kiểm đủ/không trùng rồi atomic snapshot. Sau đó gọi p7.main(['report', '--plan',..., '--sha256',..., '--authority',..., '--authority-sha256',..., '--snapshot',..., '--snapshot-sha256',...]) ngay trong process đó để giữ mapping. CLI riêng lẻ không tự nạp mapping remote. Chỉ report sau binding và snapshot đủ; quyền nhãn độc lập vẫn bắt buộc. Không chuyển raw test về vì bản gốc còn laptop.

Thời gian0055–9h là kịch bản có giả định, không phải trần. Theo dõi RAM/free disk/temp/phase/heartbeat/error; định kỳ nhận để phát hiện thiếu kết quả, không xóa remote khi chưa Minh duyệt. Lỗi nguồn/permission/schema/adapter/prep/monitor/phân loại mới thì DRAIN phần phụ thuộc, giữ attempt và báo. Không tiến triển/lặp vô tận/hàng chục giờ chưa xong thì báo; PENDING không TIMEOUT. M1 seal trước C-d3; prep trước TORAI; lô độc lập ba máy song song. Không thêm baseline/pilot mặc định.

RE3 H1/H2 và grant cuối tách riêng; chưa có adapter thực được kiểm trên nguồn RE3. Chưa commit/push. Prompt Claude trung tính ở LOG, không tự gửi.

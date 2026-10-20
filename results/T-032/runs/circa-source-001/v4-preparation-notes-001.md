# CIRCA v4: chuẩn bị, chưa chạy

Đã tạo bản mới từ v3 theo Q-103; giữ capture v2 và mọi byte/helper/source pin cũ. Q-114/Q-121 rút quyền bỏ journal nên toàn bộ kiểm vẫn được giữ. Native/adapter/shared/env/data/criteria không đổi.

Đã sửa đúng lỗi bộ kiểm: header DA G+1 và chronology/index/snapshot exit exact; empty/pre-loop exception phân biệt completed=false. Gắn final score index lại group đã ghi. Không sort/deduplicate journal. Final terminal/source checks ghi trước manifest; tất cả log nằm trong hash, check tự loại chính tên check; failure-after-check giữ bản cũ và khai superseded, không cấp dùng check PASS cũ.

Posthoc audit ràng buộc inventory transport hiện tại, kiểm trước/sau đủ run + monitor, giữ original manifest FAIL và không cấp eligibility cho capture cũ. Không gọi native trong audit. CLI audit-fixture mới nối audit → fresh đủ23 trong cùng process/guard600s50MiB. Một pilot dev03 cặp OLS DA/RHT chỉ sau ROOT kiểm full/source/manifest đạt, guard600s150MiB. Chưa tạo controller riêng và không launch.

Receipt v4-static-check-001.json cùng full diff chứa hash/file set. Kiểm laptop chỉ compile/AST và scalar JSON metadata: đủ77 currentclosed byte hash, journal0029 PASS;7mutations bị từ chối; empty/exception schema mock PASS. Đây không là native fixture hay runtime audit PASS. Source DAScorer sorted_nodes statement là dòng254–256, exception được giới hạn vào chính statement với scores=None/journal rỗng và outcome exception; không nhận incomplete call khác.

Các bước ROOT còn phải làm: fullread90KB và diff; đo resource/tổng12GiB/local2GiB; chuyển script và bản inventory hiện tại dưới sources T032, hash2đầu/pin actual source/import. Nếu fixture khác hỏng, giữ run/receipt, không cắt kiểm; samepoint3fail thì dừng/trình. ROOT ghi LOG lỗi/bằng chứng/cách sửa và quản lý EC2.

Lệnh chuẩn bị (chỉ dùng sau ROOT soát, chưa chạy):

```text
replay_circa_v4.py audit-fixture /home/ubuntu/rca/T-032/runs/circa-da-journal-audit-fixture-001 --old-run /home/ubuntu/rca/T-032/runs/circa-nodeview-fixture-001 --transport-inventory /home/ubuntu/rca/T-032/sources/circa-nodeview-transport-002-file-inventory.json --transport-inventory-sha256 0964ddf03d4b0c0f41869136670bdc9d50d982f0ed713810811639dc090f9cf3 --source-closure /home/ubuntu/rca/T-032/sources/circa-source-001/source-closure.json --source-closure-sha256 6d9f39dc6da49f15176caa7e59aa18b43f2664a4124dd048aa976d68cfce409f

replay_circa_v4.py one RE2-TT dev-03d4910932 /home/ubuntu/rca/T-032/runs/circa-re2-first-001 --source-closure /home/ubuntu/rca/T-032/sources/circa-source-001/source-closure.json --source-closure-sha256 6d9f39dc6da49f15176caa7e59aa18b43f2664a4124dd048aa976d68cfce409f
```

Path inventory trên là đích mới được đề xuất cho ROOT chuyển đúng bản file-inventory.json của transport002; ROOT phải kiểm tồn tại/hash, không tự overwrite bản khác. Dùng stage supervisor đã được soát:600s/50MiB rồi600s/150MiB; local reserve2GiB/global12GiB theo Q109. Không song song heavy EC2, không native laptop.

Không sửa LOG/docs/STATE/SPEC/WHY42/code chung hay bản cũ. Chưa có kết luận CIRCA, cohort hoặc A′.

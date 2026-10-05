# Bàn giao bằng chứng dataset T-020 cho root

Luồng chỉ cung cấp FACT/OPEN; không chọn dataset, không khuyến nghị gói và không ra thẻ quyết định. Tệp cuối do root hợp nhất.

- `01-bang-tieu-chi-hop-nhat.md/csv`: 40 phần dữ liệu, cùng chín định nghĩa nguyên MRP, chi phí riêng. RE1-TT/OB và BARO-FSE-OB bổ sung coverage census; không mở số đo RE1-TT.
- `03-task-cham-duoc-va-che-do-b.md`, `task-matrix.csv`, `root-mapping.csv`, `leakage-data.csv`: task/unit/time/root/mapping và các đường rò. Runner audit tám hàng được trích methods worker, chưa tự chứng nhận mode b mới.
- `independence-axes.csv`: 40 hàng, tác giả/injector/collector riêng, reuse và OPEN đủ ba trục. `license-revision.csv`, `schema-provenance.csv`, `heldout-schema-provenance.md`, `schema-witnesses.json` giữ bằng chứng nguồn/schema và lý do còn mở.
- `checks.csv`: 1.053 phép đối chiếu aggregate/census/sum/ratio/invariant trên nguồn gốc; nguồn và cách tính từng hàng. `seeded-checks.csv`: 40 số quan trọng, năm mỗi task dataset. `root-selected-checks.csv`: 40 số mẫu của root, 31 MATCH và 9 OPEN; không giả copy scalar là tái tính raw.
- `T004-no-scientific-pool.json`: T004 chưa triển khai, chưa có pool số khoa học; không tạo năm số giả. `review-rechecks.json` và supporting/census giữ chứng cứ REVIEW T002/T003/T019 trong phạm vi được phép.
- `public-source-claims-checked.csv` kiểm anchor nội dung nguồn công bố; `public-source-verification.json` ghi hẹp DeepTraLog official author PDF và LEMMA arXiv v4. FACT công bố không thay phép kiểm file.
- `spacing-fixes.csv`: 239 ứng viên chỉ thêm khoảng trắng trong root g1/05/06/10; root tự áp và đọc. Không sửa quyết định, chữ/số hoặc file root.

Các bước tái lập trong thư mục repo: chạy build_evidence.py, build_provenance.py, check_root_sample.py, schema_and_spacing.py, final_audit.py theo thứ tự. Chúng chỉ ghi dưới dataset_evidence; extractor public PDF dùng Python bundled có pypdf nếu cần tái tạo nezha-paper-text.json. Không chạy script task cũ.

Giới hạn còn OPEN: C7 giữ ngoài; license applicability/revision của một số release; parent/schema/normal/clock/mapping; independence C9; blind temporal detection và vùng ảnh hưởng thật. TX1 không hoàn toàn ngoài thiết kế. Bank Q49 là lựa chọn bảo toàn do agent được ủy quyền, không phải Minh chọn thí nghiệm. Bank chỉ public labels/ZIP directory, chưa có mechanism bảo đảm V7 exact newline/no inflation trên remote ZIP. First-line theo điều kiện V7 đã có quyền; không đặt thêm gate quyền giả.

Sự cố phạm vi phải giữ trong gói cuối: `scope-incident.md/json` ghi việc đọc nhầm saved schema sample chứa dòng đo DeepTraLog. Không mở data/ hay TX0 và không dùng dòng đó tính số/chọn vai trò, nhưng toàn lượt đã nhìn raw saved payload. Không tuyên bố rộng “không đọc raw”. Source đã loại khỏi proof và helper chặn replay. RE3OB chat sớm nhầm5roots đã sửa4roots/5faults; census thẻ cũ không có lỗi này.

`freeze-recheck.csv` đối chiếu hash inputs với freeze; `final-validation.json` giữ số lượng/audit/thời điểm và `output-manifest.json` hash từng artifact, cả failed runs/scope incident. G1 chưa duyệt; không quyết định mới được ghi.

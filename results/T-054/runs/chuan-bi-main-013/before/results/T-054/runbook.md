# Vận hành hiện hành — checkpoint011, chưa phát main

Đọc `runs/hoan-thien-local-g3-011/bao-cao.md`, `checkpoint.json`, `re3-h1-status.md` và `ho-so-g3.md`. EC2 tạm dừng theo Minh; không SSH/sync/kiểm trong phiên này. Không dùng plan/helper006 với pin011. H2/gRPC và OB source-native đã cài, nhưng H1, cloud và G3 còn mở.

Kiểm checkpoint chỉ đọc, từ repo D:/RCA-flashticket:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/hoan-thien-local-g3-011/verify_manifest.py
```

Plan ứng viên trong `011/prepared/` theo đường dẫn đầy đủ `runs/hoan-thien-local-g3-011/`; packet trong `packets/`. Không chạy lại prepare_local.py/package_candidates.py/check_local.py vào cùng thư mục: đầu ra create-only đã có. Không có queue main hoặc auto-resume nền. Tái dùng pin và kết quả kiểm hợp lệ; chỉ kiểm phần thay đổi hoặc trạng thái động trước chạy.

Đĩa: đọc storage-copy-accounting.json; khoảng10,1GiB là kịch bản có dự phòng, không cận trên. D đủ cho kịch bản tại lần đo. Đề xuất C rút lại, chưa tạo thư mục. Giữ mọi attempt/hỏng và raw kết quả; báo cáo không clone cả cohort. Mỗi lần nhận giữ archive truyền và một bản nhận có hash/receipt.

RAM: snapshot cuối thiếu cho slot lớn. Không giảm reservation để ép chạy và không tự tắt ứng dụng của Minh. Trước main đo lại; driver giữ reserve và chỉ phát khi đủ RAM, tối đa2worker. AC sleep đã đổi45phút thànhkhôngngủ; DC45phút giữ nguyên. Lệnh hoàn tác ở `011/restore-ac-sleep.ps1`; không tự khôi phục khi đang chạy cần thức.

Sau AWS hoạt động, chỉ tiếp tục kiểm/staging cloud khi Minh cho phép: kiểm identity, code, nguồn, môi trường, RAM/đĩa cho candidate011; dùng lại dữ liệu đã đúng, chuyển phần thiếu. Không suy haiIP lịch sử vẫn đúng. Lưu biên nhận current cloud gắn candidate protocol và packet hash. Không dùng receipt008 như current verification.

Sau Minh xét H1/policy và cấp G3/main/A nguồn riêng: lưu đúng lời quyết định, pin exact candidate protocol/sourcebundle và source quyết định. Grant cần g3/test_grant/main_dispatch/torai_A_source_grant=true; cloud_readiness_refs cho haihost; pre_G3_decisions_ref chỉ rõ policy được duyệt và H1 đã có nguồn hoặc được Minh chấp nhận OPEN cho main TT/Nezha. Không tự tạo true hoặc thay missing bằng lời tóm tắt.

Helper ứng viên011/activate_after_g3.py nhận --grant <filequyềnthật> --sha256 <hashđúng>; chỉ tạo metadata LOCKED/attestation/plan, khôngSSH hoặcphátqueue. Nhánh có quyền thật chưa được chạy; khi có quyền phải kiểm output và full locked validator, dừng nếu lỗi, giữ lượt hỏng và trình sửa ngoài quyền. Không gọi thành công kích hoạt chỉ từ kiểm đường chặn. Phần metadata khóa cuối và nguồn quyền phải được đưa/kiểm đúng từnghost trước lệnh run riêng theo CLI p7.py --help; không phát lệnh từ plan candidate.

Vận hành đã khai: per-method600s, C-d360s; một luồng số học, poll0,1s, gap<5s. Không trầncộngdồn, không tựretry. DRAIN dừng phát mới, giữ active đóng/ghi; resume cùng plan/root saukiểm PID/token, không suy SSHngắt là workerchết. Lỗi/chưa rõ nguồn/clock/monitor/RAMđĩa/khôngtiếntriển thìdừng/báo; lượtchưachạy khôngTIMEOUT. KhôngtạoScheduledTask/restartsaureboot.

Nhận/merge theo các receipt/phân vùng đã kiểm005: hash archive và từngtệp, giữ path/lineage và ánhxạ receive_paths, chỉmerge khiđủ union; nhãn evaluator ghép sau. M1sealtrướcC-d3; không phân bổ trùng. RE3 grant/profile/ma trận và bảng cuối riêng, không mở từ quyềnmainTT/Nezha. Khôngcommit/push hoặcxóaresult khi chưaMinhduyệt. PromptClaude trongLOG/011/prompt-claude.md đểMinhchuyểnthủcông.

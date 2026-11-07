# Vận hành hiện hành — chuẩn bị006, main đang bị chặn

**Chưa phát main: 4 ca OB vi phạm điều kiện 5N/5A của bộ đọc. Giữ nguồn, không bỏ ca hoặc tự sửa src.**

Đọc reports/chuan-bi-main-006/bao-cao.md, runs/chuan-bi-main-006/bo-tri-du-kien.json và LOG phiên7. Ba checkpoint01nguồn/danh sách,02transfer,03preflight đã có. Nguồn và TT transfer được Minh cấp riêng cho chuẩn bị; không còn chờ grantchuẩn bị/Acohort cũ. Chưa G3/main, chưa RE3 hoặc commit.

Chỉ đọc để tiếp nhận:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-006/verify_checkpoint.py --manifest results/T-054/manifest-chuan-bi-main-006.json
```

commands-prepared.json có lệnh plan/status theo đúng3host và pin hiện có. Run candidate bị WAIT_G3 trên cả ba máy. Không chạy lại prepare_sources/prepare_plans/stage/transfer/finish: đầu ra create-only đã có, không dùng lại tênrun. Các script hỗ trợ đã được chạy, không có auto-resume/main nền.

Protocol.json/root và freeze007 giữ bản khoa học ứng viên005 đúng byte để plan đã pin tiếp tục kiểm được. Tình trạng vận hành/nguồn mới xem006, không lấy open_choices cũ trong protocol ứng viên làm lời từ chối grantchuẩn bị mới. Source-manifest005 trong bundle là ảnh chụp khoa học, metadataTT/plan006 kèm theo có manifest riêng. Code103pin/9script worker không đổi sau đọc metadata test.

Sau Minh xétG3 và cho main riêng, ghi nguồn quyền đúng lờiMinh trong vùng006; main-grant phải pin approved_candidate_protocol_sha256 và approved_source_bundle_sha256, cấp g3/test_grant/main_dispatch/torai_A_source_grant. Chạy activate_prepared.py --grant <đườngdẫnquyền> --sha256 <pinguồnquyền>. Helper không phát main; xuất activated-001/activation-receipt.json, sourcebundle/bindingv3/policyLOCKED và plan/authority cuối. Không dùng receiptPREPARATION làm bindingv3, không đổi rootprotocol ứng viên đang được pin.

Đưa đúng metadata khóa cuối+nguồnquyền vào code_root mỗihost, giữ mọi filecandidate cũ; privateTT refs cần path tương đối code root, OB/A/labels ởlaptop. Kiểm pin/môi trường/ownership/data/đĩa và no-main-queue trước lệnh run. Runtime/independentTT đầyđủ60member nhưng rawmỗiEC2 chỉ30caseđượcgiao; không cấp labelOB/Amap cho cloud. Không tự đổi chủ lô hoặc chạy dự phòng trùng. Chỉ phát main khi Minh yêu cầu.

Trước main giữ laptop thức: hiện ACsleep45phút; chưa đổi profile điện. Worker2 chỉ khi RAMđủ. Status chỉđọc; DRAIN ngừngphát mới và để activeđóng; resume phải cùng plan/root, kiểm PID/token để không chạyđôi. SSHngắt không tự coi workerđãchết; cloudsupervisor độc lậpSSH. Không tự restart sau reboot hoặc ScheduledTask.

Nhận/hash/snapshot/merge giữ nguyên cơ chế đãkiểm ở checkpoint005: remote prefixes riêng theo ec2_1/ec2_2; giữ nguyên receipt/path, receive_paths ánhxạ bảnnhận trong cùngprocess; compare parts với planrefs; merge_partitions đủuniontrướcnhãn. Gói code/source metadata và dữ liệu ởđích giữ đến khi Minh duyệt dọn. Bản gốc laptop và mọi attempt/hỏng giữ nguyên. Đĩa/output chưa có worstcase; thiếuRAMđĩa/lỗinguồn/clock/phânloạichưarõ thìDRAIN vàbáo, unrun khôngTIMEOUT. Lỗi/khôngtiếntriển/lặpvôtận/hàngchụcgiờchưaxong thìbáo; khôngtrầncộngdồn.

RE3 schema/adapter/quyền cuối riêng chưa triểnkhai trong006; không mở telemetry bằng grantchuẩn bị94. PromptClaude trungtính ở LOG, Minh tự chọnchuyển. Không commit/push.

LưuýnguồnA trướcG3: đọc A-input-limitation.json; một logts thiếu toànN. Giữ source/t/3seed nguyênbản và quy tắc lỗi đãkhai; chưa có kếtcục method, không tự bỏ/bù/dịch nguồn hoặc phát pilot test. Không coi PASS kiểm hash/schema là phươngpháp A chắc chắn chạy thànhcông.

**Trạngtháicuối006: chưa phátmain.** checkpoint-03-final.json/OB-source-blocker.json ghi4caOB vi phạm guard5N5A thật; khônglấy PASS hash/env trước làm readiness cuối. Dùng source-bundle-final-prepared.json, có open_before_run; activationhelper từchối nguồn chưa xửlý trướcLOCKED. Không chạy main hoặc tựđổi guard/loại4ca. Cần trình phânxử/sửatối thiểu theo đúngquyền trướcG3.


## Hiện hành checkpoint008 — cloud tạm dừng theo Minh

Nguồn hiện hành: runs/cai-ob-source-native-008/bao-cao.md, checkpoint.json vàprepared-validation.json. Candidate008đúng35/25/codepinmới;006làlịchsử. KhôngSSH/sync/stagingkiểmcloudđếnkhiMinhchoresume. Khôngphátmainlocalthaythế. Đọcbáo cáoAWSvàRE3 trướcnhậntiếp;G3/mainvẫnchặn.

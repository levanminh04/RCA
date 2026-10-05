# T-020 — Tổng hợp gói quyết định G1

- Trạng thái: tự duyệt theo ủy quyền riêng trong prompt Minh ngày 04/10/2026; chưa duyệt G1.
- Người làm: Codex. Người phản biện: Claude.
- Gói: P1, P2. Cổng: G1.

## Mục tiêu

EXECUTE trong phạm vi tạo gói đề xuất. Đáp nhận xét cô về hiểu sâu kỹ thuật và mở rộng dataset công khai; chuẩn bị danh sách phương pháp, dataset/vai trò, dev/test và ba lựa chọn nhãn/cửa sổ/độ đo Minh chuyển G1. Không chọn thay Minh. RQ1 và khả năng đánh giá RQ3a–d là đích; chưa thực nghiệm P3/P4, chưa thiết kế P5–P8.

## Đầu vào

Đọc toàn bộ AGENTS, STATE, LESSONS, review-prompt, MRP, WHY, DECISIONS, mẫu SPEC/LOG, K1–K4, DT18 và nguồn advisor-2026-09-23. Hồ sơ/kết quả/review task T-001–T-019 (T-004 chưa triển khai). Manifest đóng băng `results/T-020/trung-gian/input-freeze.json` ghi HEAD, hash, byte, mtime. T-013 hiện STATE đã đóng sau sửa R1 và N1–N3; dùng bản hiện hành, kiểm hash lại trước bàn giao. Đọc src chỉ để kiểm cơ chế/adapter. Không xem archive RCA.

## Đầu ra và phạm vi ghi

Chỉ `tasks/T-020-tong-hop-g1/SPEC.md`, LOG append-only; `results/T-020/**`; thư mục tạm D:/RCA-ext/work/T-020/ và data/T-020/ nếu thật cần; đúng dòng T-020 STATE. Không dùng thư mục tạm nếu stdlib đủ. Không sửa mục Task đang mở.

Đầu ra V1–V10 đúng danh sách prompt: g1-goi-quyet-dinh.md; 01-bang-tieu-chi-hop-nhat.md/csv; 02-so-ca-da-nhin.md/csv; 03-task-cham-duoc-va-che-do-b.md; 04-phuong-phap-x-dataset.md/csv; yeu-cau-dau-vao-hop-nhat.csv; 05-nhan-va-cua-so.md; 06-phuong-an-dataset-va-chia.md và chia-theo-o/*.csv; 07-danh-sach-phuong-phap-va-doc-nhanh.md; 08-so-chuyen-g1.csv; 09-kiem-cheo-so-lieu.md/csv; 10-ke-hoach-p3-de-xuat.md; ca-da-chay.csv; dinh-chinh-task-cu.md; de-xuat-tai-lieu-chung.md; manifest.json; scripts/runs/trung-gian.

## Tiên nghiệm — khóa trước khi điền bảng

1. Tiêu chí C1–C9 dùng nguyên định nghĩa MRP §4, không tính điểm tổng và không thay bằng chi phí. Mỗi dataset/release/phần khác tín hiệu là một hàng. Danh sách ứng viên là hợp MRP/P2 và thẻ results, không chọn theo thứ tự hay có sẵn. C1–C4 là điều kiện tác vụ tương ứng; thiếu trace chỉ được vai trò kiến trúc/metric có chủ đích. C5–C8 là khả năng phân xử, chưa biết không bằng đạt. C9 báo riêng ba trục tác giả/injector/collector với bằng chứng; không nhận đủ ba trục khi chỉ khác miền.
2. Dev: được TX1/TX2 nhưng phải đúng nhãn/tác vụ. Test: không có TX2, toàn ô cùng phía, bản sao TX2 kéo theo mức cao nhất. Giữ ngoài: chỉ TX0; C7 OPEN tới G3 là giới hạn được MRP cho phép, không loại bằng lý do này. Chỉ tái lập: dữ liệu đã TX2 hoặc tác vụ khác, không thay dataset độc lập. Nếu không có ứng viên chứng minh đủ C1 và nhãn/schema/TX0, đề xuất chưa có bộ giữ ngoài đủ điều kiện, nêu sớm. Bank được đánh giá như mọi ứng viên, Q49 là quyết định agent theo ủy quyền bảo toàn, không phải Minh chọn thí nghiệm.
3. So phương án bằng phạm vi RQ và mức bằng chứng, không kết quả phương pháp hay mức thắng đồ thị. Ưu tiên bảo đảm điều kiện tác vụ và chống lộ trước độ đa dạng; chi phí riêng. Khi hai phương án không trội mọi chiều, giữ cả hai, trình Minh trade-off. OPEN giữ owner/đầu vào/điểm giải, không điền bằng phỏng đoán. Mỗi khuyến nghị có phản biện mạnh nhất và điều kiện đổi ý.
4. Lấy mẫu số: mỗi task đầu vào có số liệu, dựng danh sách lá số trong JSON/CSV kết quả gốc (không payload số đo mới); loại hash/timestamp không mang nghĩa đếm/độ đo khỏi mẫu. Sắp theo SHA256 của `20261004|task|path|key`, chọn ít nhất 5 đại lượng khác nghĩa/task, nếu ít hơn kiểm toàn bộ và giải thích. Seed kiểm chéo 20261004. Mọi số quyết định-trọng yếu và đại lượng cùng nghĩa lặp ở >=2 tài liệu phải kiểm, ưu tiên census/coverage/normal/time/root/cell. Với CSV tính lại group/count/sum; JSON đối chiếu tổng thành phần hoặc CSV/run gốc, không chỉ chép scalar. Giữ số công bố và đếm artifact riêng khi lệch. Mọi khẳng định quan trọng subagent là đầu vào cần root kiểm.
5. Hai phương pháp kiểm sâu bài/code: chọn một hồ sơ Codex và một Claude bằng SHA256 `20261004|task|method` trong hai pool; khóa chọn trước đọc giá trị. Không chọn theo số điểm. Kiểm công thức, mặc định file:dòng, khác biệt bài/code từ revision gốc T001 §9.
6. Split: seed 20261004; SHA256 `seed|dataset|root|fault` là thứ tự ô. Chỉ census nhãn/metadata. Giữ RE2-TT 10 ô dev v1 nếu census xác nhận không cắt ô; ô TX2 ép dev ở mọi phương án. Các ô còn lại phân khoảng 1/3 dev, 2/3 test, làm tròn dev lên, không tối ưu điểm. Không phân tầng theo topology suy từ số đo. Bộ giữ ngoài nguyên bộ, không split. Bộ ít ô báo số đơn vị bootstrap, không tự đặt ngưỡng đủ CI phổ quát. Dataset chỉ có trace anomaly hoặc chưa census sự cố không giả thành ô root×fault.
7. Cửa sổ: phân biệt thời lượng s/points/tần số và phần fit/hậu sự cố/trigger. Hai phương án quy tắc chung theo thời gian thật, chọn từ prior work và độ dài normal công bố, không theo điểm. Chưa đủ căn cứ cho một số thì nêu số là cấu hình ứng viên, P3 kiểm độ nhạy và chốt theo quy tắc chỉ dựa normal/khả thi, trước ranking score. Retrieval chỉ phần chẩn đoán, không thay xếp hạng; metric→service và candidate ceiling phải định nghĩa.
8. Dùng nhãn: tách fit normal/regime, tune dev, score test; không root/path/mốc tiêm trong chế độ b. Không dùng nhãn test tune/checkpoint. GDN là detector, không tự gọi attribution là RCA. Không trộn giám sát và không giám sát mà không ghi điều kiện.

## Các bước theo phụ thuộc và lệnh kiểm

0. Đã đóng băng trước SPEC. Kiểm `git status`, `git diff HEAD --stat`, `git diff HEAD -- docs/`; manifest hash. Không chạy script triển khai trước khi SPEC được ghi.
1. Tự phản biện SPEC trước triển khai; ghi kết quả vào LOG. Ba subagent độc lập model gpt-6.1-sol/ultra, chỉ ghi thư mục luồng riêng: dataset (V2/V4), ledger (V3/census V7), methods (V5/V6 bằng chứng/V8). Root V1/V9. Subagent không chọn/khuyến nghị/thẻ quyết định. Kiểm `py -3 -X utf8 <script>` của từng luồng, không chạy script cũ chưa kiểm ghi.
2. Giai đoạn A: V1 nguồn G1/cần Minh và V9 proposal/correction; V2 đủ ô có nguồn; V3 normalize/dedup; V4 nhãn/đường lộ; V8 hồ sơ. Kiểm census sums/keys, TX2/no locked theo public metadata, source-line coverage, bài/code 2 phương pháp. Checkpoint LOG và một dòng STATE giai đoạn A/3.
3. Giai đoạn B: V5 sau V2/V4; V6 sau cơ chế/label leak; V7 sau V2–V6. Root tự kiểm số quan trọng từ nguồn gốc. Ít nhất 3 cấu trúc gói; script split assert không trùng ô/TX2-test/census-total. Kiểm `py -3 -X utf8 results/T-020/scripts/...`; giữ stdout/assert trong runs. Checkpoint B/3.
4. Giai đoạn C: V9 đối chiếu với tài liệu chung hiện hành, V10 thẻ đủ trường và sáu câu gate. Tự đọc gói từ đầu; kiểm nguồn mọi số, không chọn theo winner. Script audit links/CSV không trống/method rows/coverage G1/output manifest. Hash input lại; file đổi phân loại bản mới và recheck phần phụ thuộc, không ghi đè file chung. Checkpoint C/3.
5. Bàn giao: LOG báo cáo A–I, bảng việc còn lại (không có làm được mà chưa làm); mẫu reviewer nguyên văn Prompt chung + G1, chỉ điền trung tính và liệt kê file cụ thể, không dùng diff làm phạm vi. Dòng T020 chờ phản biện 04/10/2026 khi đủ, chưa đóng G1. Không commit/push.

## Edge cases và cách xử lý

| Mục | Kiểm | Xử lý |
|---|---|---|
| E1 số lặp/nguồn lệch | đối chiếu key và tổng phần thành phần | giữ hai định nghĩa/số; đính chính có nguồn |
| E2 trùng bản/cùng byte | hash artifact/metadata inject/crosswalk có bằng chứng | union sự cố; chưa đủ bằng chứng giữ quan hệ OPEN, không suy tên |
| E3 đơn vị ca | đọc schema census/label | tách incident/capture/file-minute/trace; không cộng khác đơn vị |
| E4 một lặp/ô hai phía/ít ô | group root×fault và side | tất cả repeats cùng phía; nêu CI yếu |
| E5 tiếp xúc bản sao/paper per-case | ledger nguồn và identity links | truyền TX2 qua bản sao đã chứng minh |
| E6 mức root khác service | mapping nguồn schema | alias tường minh; suy luận CANDIDATE, ceiling OPEN |
| E7 root ngoài trace/cạnh | candidate audit kết quả gốc | miss giữ denominator; không chèn root bằng nhãn |
| E8 inject/onset/end/leak | timestamp metadata, result leakage, runner source | tên độ trễ đúng mốc; mode b chưa hợp lệ nếu leak chưa xử lý |
| E9 normal/warmup/recovery | normal range từng nguồn | không coi min tính toán là đủ calibration |
| E10 thiếu modality/field | matrix signal/schema | adapter có/không suy không nhãn; no run mới |
| E11 điều kiện khác | known/auto/supervised columns | bảng riêng/điều kiện rõ |
| E12 NC/ND/phát hành | nguồn license ghim và lời tác giả | không tự giải nguồn; quyền phái sinh OPEN |
| E13 nguồn mutable | manifest revision/hash | chưa ghim nêu giới hạn tái lập |
| E14 input đổi | hash đầu/cuối | re-read bản mới, record change; chỉ root dòng STATE |
| E15 proposal đã áp | exact/semantic diff WHY/K1/LESSONS/Q | đúng nguyên văn/biến thể/chưa áp |
| E16 Q37/Q38, source attribution | DECISIONS nguyên lời | Q38 thay phần tương ứng Q37; không gộp agent chọn với Minh chọn |
| E17 bootstrap ít ô | đếm ô test và singleton | chỉ nêu phạm vi, không hứa CI mạnh |
| E18 cửa sổ khác đơn vị | timestamps/rates/reference params | so thời lượng thật, giữ điểm/stride riêng |
| E19 JSON 50–100 MB | size trước đọc | stream hoặc bounded query; không in payload |
| E20 Windows UTF8/STATE newline | -X utf8 và byte newline | replace exact một dòng, read-before/write-after |
| E21 context dài | checkpoint từng giai đoạn | LOG đủ đường dẫn/lệnh tiếp nhận; không quên phạm vi |
| E22 script cũ ghi sai chỗ | đọc toàn script/call imports | không chạy nguyên; copy/rewrite output ở T020 hoặc ghi lý do không bảo đảm |

## Kiểm đúng đắn và tiêu chí xong

Mỗi V1–V10 có đầu ra/kiểm ghi LOG. V2 không ô trống và mọi ô quyết định trọng yếu có raw-result check. V3 tái lập, tổng nguồn có reconciliation, 60 locked IDs public không TX2. V1 mọi match G1/chốt ở có row. V7 >=3 gói split tái lập assertions. V8 checklist từng variant/detector và 2 kiểm bài/code, tính lại độc lập nhẹ chỉ TX2 hoặc fixture. Crosscheck >=5 số/task và mọi số gói; số thiếu nguồn không thành FACT. Sáu câu gate và tất cả thẻ đủ trường. Hash output, audit phạm vi writes, prompt reviewer, A–I cuối LOG. P1/P2/G1 đối chiếu riêng. Không declare xong khi phép kiểm được phép còn thiếu.

## Không làm; phép kiểm bỏ và hệ quả

Không chạy RCA/detector mới, không raw TX0/TX1, locked, EC2, tải số đo/zip, sâu nghiên cứu, gửi tin ngoài, git mutation, ghi docs chung. Bỏ P3 runs làm matrix adapter/chi phí dataset mới chưa xác nhận; bỏ raw giữ ngoài làm normal/parent/lan OPEN tới G3; không suy đủ C7/C9. Schema thật giữ ngoài chỉ first line từng signal, tối đa một file/signal, byte-wise dừng LF không buffer đọc trước; nếu file không local/không bảo đảm, ghi Minh quyết, không lấy payload. Không cài gói nếu stdlib đủ.

## Chi phí ước lượng

Task chỉ đọc và tổng hợp, không benchmark thời gian chính thức. Ba subagent gpt-6.1-sol ultra; phép tính metadata nhẹ từng bước dưới 5 phút, không lượt >1h, không EC2; không tải đo, nguồn công khai tổng <=100 MB nếu cần. Chi phí thực nghiệm P3 quy về tổng dataset×seeds và Q40 ba giờ/method/dataset, chỉ đề xuất. Không nêu rủi ro thời hạn/FlashTicket.

## Rủi ro và điều chưa chắc

Chưa kiểm mọi đầu vào task cũ; manifest là snapshot, không chứng minh nội dung đúng. C9 có thể không ứng viên đủ ba trục. Không có nhãn vùng public cho RQ3c; mode b có leakage chọn mẫu; nhiều bộ đã TX1 không đủ nghĩa giữ ngoài. Quan hệ bản sao chưa chứng minh không được merge tùy tiện. Material conflict trong nguồn chung phải nêu cụ thể, giữ OPEN; không tự sửa nguồn.

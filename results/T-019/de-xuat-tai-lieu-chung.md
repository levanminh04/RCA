# Nháp nguyên văn cho tài liệu chung — chưa ghi nguồn chung

Minh quyết có ghi hay không; T-019 không thay AGENTS/MRP/WHY/DECISIONS/LESSONS/data README hoặc task cũ. Không tạo thêm cổng/quy trình.

## docs/DECISIONS.md — ghi ủy quyền, mã để Minh/phiên được duyệt điền

> Ngày04/10/2026, Minh ủy quyền Codex tự viết và tự duyệt SPEC rồi triển khai task T-019 theo prompt Đợt1. Phạm vi: thẻ Sock Shop RE2-SS/RE3-SS và RE1-SS ngắn, census toàn release, kiểm file/sổ ca và nháp tài liệu trong phạm vi task; tải tối đa1GB, không RCA/detector, không chọn/chia dataset, không commit/push. Người phản biện là Claude. Nguồn nguyên văn khối task và ủy quyền: tasks/T-019-the-sock-shop/LOG.md.

## data/README.md — sửa câu khái quát sai và thêm mục dựng T-019

Cũ: “Mỗi ca có `metrics.parquet`, `traces.parquet`, `logs.parquet` (riêng một ca RE2-TT không có log). Vài ca mẫu có thêm `inject_time.txt`.”

Mới nguyên văn:

> Modalities tùy biến thể và ca. RE1-SS có metric và injection, không có log/trace. RE2-SS và RE3-SS có metric/log/injection, không có trace tại revision ghim. RE2-TT có một ca thiếu log. Danh sách file cụ thể phải lấy từ inventory của đúng revision; không suy mọi ca có đủ ba nguồn tín hiệu.

Mục bổ sung nguyên văn:

> **T-019 — Sock Shop và đối chiếu lineage (04/10/2026).** `data/T-019/` giữ245ca RE1/2/3-SS,618file có tổng149.245.189byte. Nguồn Hugging Face RCAEval và revision nằm trong `results/T-019/download-plan.json`; SHA256 LFS hoặc git-blobSHA1 của từng file được kiểm sau tải trong `acquisition/manifest.json` và `inspection/hash-recheck.json`. Bảy file mẫu được tái dùng sau hash; byte mạng SS146.929.723. `D:/RCA-ext/work/T-019/lineage/re2ob/` có180file chỉmetric/injection RE2-OB,14.215.893byte, để so nội dung với nguồn fse/torai; không có trace/log OB tải cho task này. Manifest đầy đủ ở `results/T-019/lineage/download-manifest.json` và `outside-files.csv`. Dữ liệu ngoài git, không phải lựa chọn test/dev ở G1.
>
> Dựng lại SS từ repo root: `py -3 -X utf8 -B results/T-019/acquire.py plan`, rồi ghi kế hoạch vào LOG theo phạm vi được duyệt, `py -3 -X utf8 -B results/T-019/acquire.py acquire --run acquisition-replay-001`. Tên run phải mới; giữ bản cũ, không ghi đè. Script tái dùng từng cache file chỉ sau size/hash. `tai-lap.md` mô tả reader/môi trường và lineage. Không đọc data/locked hoặc repo RCA lưu trữ.

## Hồ sơ G1/P2 — bổ sung kết quả, không quyết chọn/chia

> Sock Shop RCAEval đã có thẻ riêng tại `results/T-019/the-sock-shop.md`. RE2-SS90ca/5root/30ô; RE3-SS30ca/3root/9ô; toàn release SS không có trace. Có graph kiến trúc công bố để đối chiếu tĩnh, chưa pin deployment RCAEval nên bậc root runtime còn OPEN. RE3 có8file chỉ báo log,7nội dung unique; nhãn front-end_f2_2 ngoài cửa sổ chính ca và không khớp own log. Không dùng chúng như8nhãn code-line/onset độc lập. File metric toàn120ca RE2/3-SS căn tiêm±720s, là đường lộ mốc dù bỏ tên ca và file nhãn.
>
> G1 phải xét sổ `so-ca-da-nhin.csv`: toàn90RE2-SS đã qua RCA T006 ở torai-SS;100RE1-SS non-disk đã qua fse-ss;25disk RE1-SS chưa có evidence RCA trực tiếp trong archives đã kiểm, T006 chỉ census và T019 đã đọc số đo. Toàn90RE2-OB đã qua T007; fse/torai đổi tên không tạo dữ liệu test chưa nhìn. Cách chọn dataset, kịch bản graph tĩnh, chia theo ô và ngân sách nhãn vẫn do Minh quyết tại G1.

## Task cũ

Đề xuất điều hướng T-003 và bổ sung phạm vi nguồn T-002 nằm nguyên văn trong `dinh-chinh-task-cu.md`. Không sửa snapshot nguồn hoặc nhãn gốc.

## WHY/LESSONS/AGENTS/MRP

Không có lựa chọn dataset, phương pháp, giao thức hay luật mới cần tự ghi trong các file này. Nếu G1 chọn kịch bản đồ thị kiến trúc cho SS, lý do/đối lập/bằng chứng/kết luận phụ thuộc phải được ghi WHY sau Minh duyệt; T-019 chỉ cung cấp thẻ, không viết trước kết luận chọn.

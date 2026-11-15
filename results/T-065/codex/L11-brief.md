# Brief L11 cho Codex — T-065: cập nhật G-c theo chỉ mục xuất bản 3 của T-064 (15/11/2026 04:55Z)

Bạn là Codex (`gpt-6.1-sol`), **người làm** T-065 trong repo `D:\RCA-flashticket`; Claude là người phản biện. Phiên điều phối giao việc theo lời Minh 15/11/2026 "triển khai phần còn lại giúp tôi" (chuyển qua phiên điều phối; quyết định sửa R9 T-064 ở `docs/DECISIONS.md` mục 15/11 "Sửa R9, R10 … và S1 …").

## Đọc trước
`AGENTS.md`; SPEC và mục cuối LOG T-065; `results/T-065/CHECKPOINT.md`; `results/T-065/kiem/006-gc-cuoi/BAO-CAO.md` (L8b), `kiem/008-s1/BAO-CAO.md` (L10), `kiem/009-s1-anh-minh/GHI-CHU.md`; `results/T-064/ban-xuat/chi-muc-ban.json` (**bản 3**, `phien_ban_chi_muc: 3`, SHA-256 file `e83e1696d04aa684bebbc4da8c3c88d4b415762f34ddb2ffd915637ba95cfecd`) và `chi-muc-ban-2.json` (bản 2, nguồn của L8b); `results/T-064/ho-so-chon.md` §17; `docs/WHY.md` WHY-99.

## Dữ kiện (kiểm lại, không tin brief)
Bản 3 khác bản 2 đúng hai slot `ebd5ef38` của `V082-V066+H8a` và `V071-V041+H8a`: đầu ra chạy lại ở `results/T-064/kiem/nhan-r9/r9/dev3/d0/<bản>/ebd5ef38/` (kênh liveness theo lần dò mới nhất; H5b không còn nhận chết im; theo T-064 hạng và cờ không đổi). `cau_hinh_sha256`, `ma_nguon_sha256` của hai bản không đổi.

## Việc
1. Kiểm SHA chỉ mục bản 3 và mọi `dau_ra`; so với bản 2 bằng máy (chỉ hai slot khác). Lệch khác thì dừng phần phụ thuộc.
2. Đưa chỉ mục bản 3 vào dữ liệu xuất và dashboard theo đường **ít thay đổi nhất** mà vẫn giữ lịch sử: dữ liệu xuất bản mới trong thư mục mới (không ghi đè dữ liệu L8b); dashboard hiện hành phải ghi đúng "chỉ mục bản 3" và đọc dữ liệu mới. Nếu cần sửa file dashboard L8b hiện có hoặc Mục lục, làm như S1: GET hash live trước = pin, ghi hash trước/sau, lưu byte cũ, cách hoàn tác, không ghi đè file đích khác. Nêu phương án đã chọn và phương án khác trong báo cáo.
3. Kiểm: hai slot ebd5ef38 hiển thị đúng `method-output-1.json` mới (hạng, cờ, hash), 82 slot còn lại không đổi so với L8b; API của hai trang hiện hành; chú thích chết im H5b của ebd5ef38 phản ánh đầu ra mới nếu dashboard có hiển thị. Ảnh trình duyệt: nếu lượt CLI không chụp được, ghi phần còn thiếu để Minh chụp.
4. Ghi `results/T-065/kiem/010-chi-muc-3/`, cập nhật `XONG.md`, `CHECKPOINT.md`, manifest (giữ bản trước), nối mục L11 vào LOG T-065, kèm prompt cho Claude kiểm lại (nguyên văn mẫu `docs/review-prompt.md`, khối "Kiểm lại phản hồi và sửa", thông tin trung tính).

## Phạm vi ghi
`results/T-065/`; nối LOG T-065; trên exp-obs: thư mục dữ liệu mới trong `/opt/flash-ticket-obs/rca-ket-qua/`, file dashboard trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/` theo bước 2, tải lại provisioning hoặc khởi động lại Grafana nếu cần. Không sửa `results/T-064/`, SPEC, STATE, docs, REVIEW (trừ khi người phản biện mời). Thấy cần làm khác: dừng, ghi checkpoint, trình lại.

## Dừng
Có `D:/RCA-overnight/STOP` hoặc `~/rca-dieu-phoi/STOP`: dừng ở ranh giới.

## Báo xong
Bốn mục: đã làm gì; file đổi; kiểm đã chạy và kết quả; điều chưa chắc.

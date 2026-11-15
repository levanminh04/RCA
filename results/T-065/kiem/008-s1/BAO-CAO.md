# T-065 L10 — Sửa S1: triển khai/API đạt, còn ảnh

2026-11-15T03:45:09.877Z

Sửa đúng gói S1 L9 đã được Minh duyệt. Nguồn phát hành mới [mục lục](../../grafana-l10/t065-l5-muc-luc.json) chỉ đổi `panels[0].options.content`; mọi trường khác và UID giữ nguyên. Nguồn L5 vẫn giữ.

Mục lục hiện ba bản p7/V082/V071, 28 ca mỗi bản; V082 là đề xuất cuối Minh chọn, V071 là thay thế. Hai liên kết hiện hành trỏ tới UID L8b. Hai dashboard L4 được chuyển vào `RCA FlashTicket/9 · Lưu trữ/L4 · Bộ bản tạm · 14-11/`, giữ nguyên byte và UID; không ghi đè file đích.

Các phép kiểm và nguồn bằng chứng:

- Trước ghi, ba file live khớp pin L9; hai file đích vắng. Biên nhận [may-truoc-001.json](may-truoc-001.json) và byte gốc ở `ban-truoc/`.
- Sau ghi, hash mục lục khớp đúng giá trị dự kiến L9; hai L4 giữ hash/byte. [Hash trước/sau](hash-truoc-sau.json) ghi từng đường dẫn. Mười file còn lại trong inventory provisioning/compose giữ hash, gồm hai L8b, provider, datasource và các dashboard lưu trữ khác.
- [API sau](may-sau-001.json) trả HTTP 200 cho năm UID; nội dung panel mục lục đúng nguồn L10. Search/folders xác nhận nhánh L4 thuộc “9 · Lưu trữ”, còn Hiện hành chỉ có hai L8b. Hai liên kết từ mục lục có đúng đích UID L8b và đích API tồn tại. [Đối chiếu](doi-chieu.json) chứa từng phép kiểm.
- Grafana tự nạp; thời điểm khởi động và restart_count giữ nguyên. Không gọi restart/reload. Không chạy lại dữ liệu/phương pháp hoặc bộ kiểm L8b/L8c.

**Ảnh chưa làm.** Native Chrome có cửa sổ, nhưng browser access host không khả dụng trong lượt này; không tác động UI native. [Biên nhận trình duyệt](trinh-duyet-002.json). Đã gọi `/render/d-solo/t065-l5-muc-luc` với panel 1, API trả HTTP 500 “Rendering failed.”; giữ [response](render-001.json). Chưa có ảnh Mục lục và chưa bấm hai link từ Mục lục trong L10. Minh cần mở app, vào `/d/t065-l5-muc-luc`, chụp ảnh và có thể bấm hai link hiện hành; kiểm đúng hai UID L8b. Không suy lỗi renderer là lỗi dashboard hoặc tự xác nhận nghiệm thu từ API.

S2/S3/S4 chưa được duyệt và chưa sửa. Các báo cáo L5/L8c và hai JSON L8b giữ nguyên hash. L10 chỉ xử lý đường vào/lưu trữ cho yêu cầu giao diện của DT18 và phần G-c; không thêm bằng chứng hiệu quả M1 hoặc khép RQ5/P10. Nghiệm thu T-064/T-065 vẫn do Minh quyết. Cần ảnh và lượt kiểm lại của Claude để xét S1.

[Cách hoàn tác](HOAN-TAC.md) có lệnh và guard pin; lệnh chưa thực thi. Bản manifest trước giữ nguyên ở `../../codex/manifest-L10-truoc.json`. Prompt trung tính cho Claude ở `../../prompt-ban-giao.md` và mục L10 của LOG.

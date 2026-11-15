# T-065 L11/L11b — chỉ mục bản 3 đã xuất và triển khai, API đạt

2026-11-15T05:24:33.664Z. Codex là người làm; Claude là người phản biện. Theo brief L11 và đính chính L11b của Minh. Không thêm quyết định nghiên cứu.

## Kết quả

Đã xuất dữ liệu chỉ mục bản 3 vào thư mục mới /opt/flash-ticket-obs/rca-ket-qua/t065-l11-001/. Giữ nguyên dữ liệu L8b và toàn bộ hồ sơ dừng L11. Hai UID hiện hành vẫn là t065-l8b-rca và t065-l8b-phat-lai, nay đọc dữ liệu mới và ghi “chỉ mục bản 3”. Mục lục giữ UID, ghi đúng đường nguồn T-064 là chỉ mục bản 3 và nêu ảnh Chrome L8c thuộc bản 2.

Mâu thuẫn ban đầu đã được điều phối T-064 đính chính ở cuối hồ sơ chọn §17 và LOG 05:00Z. L11b xác nhận đây là lỗi mô tả, phạm vi đã duyệt vẫn dùng đúng dữ liệu bản 3. Báo cáo dừng nguyên byte giữ tại [BAO-CAO-L11.md](l11b/ban-truoc/BAO-CAO-L11.md); không sửa T-064 hay quyết định trong docs.

## Hai slot cập nhật và phạm vi không đổi

| Slot ebd5ef38 | Bảng cờ | Thứ tự thực thể/tie_group, verdict | Khóa payment-service và H5b |
|---|---|---|---|
| V082-V066+H8a | 65 → 64; bỏ payment-service_live-down | Giữ nguyên | Khóa ghi đè [3,0,0,0,0] được thay bằng khóa nguồn mới; chet_im.thanh_phan và don_vi_co_co rỗng |
| V071-V041+H8a | 65 → 64; bỏ payment-service_live-down | Giữ nguyên | Cùng thay đổi trên |

Đường dẫn, hash đầu ra, từng phần tử khóa và chú thích có trong ../../may-l11/kiem/hai-slot.json#/0 và /1 (tính từ thư mục báo cáo này). Khóa cũng được đối chiếu qua API Infinity tại ../../may-l11/kiem/kiem-khoa-api.json#/rows và key-api/. Bảng hạng hiện hành có năm cột, không hiển thị khóa; lượt này không tự thêm cột.

Dữ liệu đầy đủ, vue, phát lại và từng service projection của hai slot đều cập nhật từ method-output-1.json bản 3. Bảng hạng giữ đầy đủ key ở dữ liệu; bảng cờ, đơn vị, bằng chứng, lớp và kế thừa lấy từ nguồn mới. 64 cờ còn lại giữ toàn bộ trường. Hash cấu hình và mã nguồn cấp bản không đổi.

82 slot còn lại giữ nguyên byte ở file ca, vue, phát lại và các file service. Cả cây du-lieu đã so từng file: ngoài các projection của hai slot, chỉ du-lieu/chi-muc-ban.json đổi trường phiên bản thành 3. Nguồn: ../../may-l11/kiem/doi-chieu-byte.json#/unchanged_slots và /changed_files. Không chạy lại M1, chấm điểm hoặc xuất raw.

## Phép kiểm và bằng chứng

- Chỉ mục bản 3 đúng SHA Minh cấp; 83 dau_ra khớp. Đối chiếu bản 2/3 chỉ hai slot khác, metadata cấp bản giữ. L11 đã kiểm 83 đầu ra của cả hai bản; L11b kiểm lại 83 đầu ra bản 3 trước xuất và trước chốt. Nguồn: tiep-nhan.json, l11b/tiep-nhan.json và l11b/nguon-da-ghim.json.
- Bộ xuất và schema 0.5 đạt 84/84 slot, gồm P7/ebd5ef38 lỗi chạy vẫn rỗng đúng nguồn. Có 1.410 dòng hạng, 1.650 cờ, 26.266 đơn vị, 600 dòng cạnh, 19.971 thao tác; 48.717 phần tử liên kết giải mã một lần, đúng query/kho/cửa sổ. Chín P7 T-062 hồi quy đạt. Nguồn: ../../may-l11/kiem/kiem-xuat.json#/totals, /cases, /urls_decoded_once, /T062_P7_regression; kiem-schema.json#/passed. Giữ số nguyên ns bằng Python.
- API 18/18 trang: ba bản × ba ca (86dea661, ebd5ef38, 00eaea92) × hai UID. Đối chiếu metadata/hash/window, thứ tự hạng, cờ, cạnh, thao tác, bằng chứng và biến chọn. Các request/response lưu api-slots/ và api-luot/. Nguồn: ../../may-l11/kiem/kiem-api.json#/rows. Hai audit bổ sung trên cùng URL Infinity đối chiếu chính xác từng phần tử key, giữ response ở key-api/.
- T1: GET cả ba UID khớp định nghĩa provisioning; Mục lục trỏ đúng hai UID đang đọc dữ liệu mới và ghi chỉ mục bản 3. Nguồn: ../../may-l11/kiem/may-sau.json#/targets và l11b/doi-chieu-dashboard.json.
- T2: đã đối chiếu cả cờ, key, hash đầu ra và chữ H5b/chết im. Hai dashboard không có panel chú thích H5b theo ca. Mô tả H5b cấp cấu hình và tên bản L4 lưu trữ không là khẳng định ca chết im, nên giữ nguyên. Nguồn chú thích H5b của hai đầu ra mới rỗng; bảng cờ không còn live-down. Bằng chứng: l11b/doi-chieu-h5b.json. Lượt rà chữ đầu quá rộng bắt tên bản lưu trữ; đã giữ h5-scan-luot-001.json và kiểm lại đúng ngữ cảnh, không sửa dữ liệu theo phép kiểm sai.
- Nhận gói 19.144.723 byte, SHA hai đầu khớp; 2.404 file trong manifest máy khớp sau giải vào may-l11/. Nguồn: l11b/dong-goi-001.json và kiem-nhan-goi.json. Không nhận raw. Ảnh S1 của Minh ở kiem/009-s1-anh-minh/ đã được ghim từ manifest L11; L11b kiểm/giữ cả thư mục.

## Cách xuất bản và hoàn tác

Chọn thư mục dữ liệu mới, sao byte phần hợp lệ rồi dựng lại hai slot. Thay đúng hai file dashboard hiện hành và Mục lục; giữ UID để đường vào/liên kết không phải đổi. So với tạo UID mới, cách này giảm file và điều hướng phải kiểm, vẫn giữ nguồn/byte cũ tại L8b, grafana-l8b, grafana-l10 và rollback. Ghi đè dữ liệu L8b bị loại vì làm mất mốc đối chiếu.

Trước mỗi bước ghi đã kiểm hash live bằng pin và GET ba UID; byte trước lưu tại ban-truoc/ và trên máy trong t065-l11-001/rollback/. Thay file nguyên tử, chỉ đúng đích đã duyệt. Hash trước/sau tại [hash-du-kien.json](l11b/hash-du-kien.json) và ../../may-l11/kiem/deploy.json. Diff hai dashboard chỉ đổi URL, chữ chỉ mục và tag; Mục lục chỉ đổi panels[0].options.content. Không đổi file provisioning khác, compose, provider, datasource hoặc kho quan sát. Grafana tự nạp, thời gian khởi động/restart_count giữ.

[Cách hoàn tác](l11b/HOAN-TAC.md) có guard pin sau, khôi phục đúng byte ba file và giữ dữ liệu mới làm lịch sử. Chưa chạy hoàn tác.

## Phần còn thiếu và bàn giao

Chưa có ảnh hoặc bấm UI thật của bản 3 trong L11b. Browser access host không khả dụng; công cụ từ chối điều khiển cửa sổ Chrome: “Computer Use was not approved to use Google Chrome”. Biên nhận l11b/trinh-duyet-001.json; không dùng API làm bằng chứng bấm thật. [ANH-CAN-CHUP.md](l11b/ANH-CAN-CHUP.md) có URL bốn trang mẫu của hai slot và phần Mục lục cần Minh chụp. Ảnh L8c và 009 giữ là lịch sử bản 2.

Dữ liệu/API bản 3 đã đạt phạm vi L11/L11b; bằng chứng UI mới còn thiếu. T-065 chưa nghiệm thu. S2–S4 chưa được duyệt, giữ nguyên; các OPEN về Loki và quan sát lịch sử giữ theo hồ sơ trước. Không thêm bằng chứng hiệu quả M1, không khép RQ5/P10 hay suy việc hiển thị đúng là nghiệm thu T-064.

Bước tiếp: Claude đọc nguồn/đầu ra trước rồi kiểm lại theo prompt-ban-giao.md; Minh chụp phần UI còn thiếu và quyết nghiệm thu. Không có job kiểm, thao tác UI hay tunnel mới đang chờ. Không sửa STATE/SPEC/docs/REVIEW/T-064; không commit/push. Đề xuất nội dung commit sau khi Minh duyệt: “T-065: xuất và hiển thị chỉ mục bản 3, giữ lịch sử L8b”.


Đính chính L12 — U2 (15/11/2026): câu “Theo brief L11 và đính chính L11b của Minh” ở đầu báo cáo được đính chính thành “Theo brief L11 và đính chính L11b của phiên điều phối (Minh chuyển), trong phạm vi Minh đã duyệt”. Người soạn brief L11b là phiên điều phối; không ghi thành lời quyết trực tiếp mới của Minh. Giữ câu cũ làm lịch sử. Nguồn: results/T-065/codex/L11b-brief.md; tasks/T-065-giao-dien-grafana/REVIEW-5.md, U2.

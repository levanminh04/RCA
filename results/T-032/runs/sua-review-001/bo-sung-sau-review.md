# T-032 — Bổ sung sau REVIEW

Codex thực hiện bản sửa theo lời Minh duyệt; bắt đầu 11/10, tiếp ngày 12/10/2026. Vai trò lịch sử Claude làm / Codex phản biện trong SPEC được giữ. Minh yêu cầu một phiên Codex mới kiểm bản sửa; ngoại lệ này được ghi trong sổ quyết định và LOG. Đây là báo cáo sửa và tự kiểm, không phải lượt phản biện mới hay nghiệm thu.

## Những kết luận được sửa

| Điểm | Bản sửa | Hệ quả với RQ2 và đồ án |
|---|---|---|
| R1 | Root không hạng 1 chỉ là kết quả xếp hạng. Cờ/phiếu thấp không xác nhận dữ liệu thiếu đáp ứng do lỗi. Return vẫn OPEN. Bảng placebo Nezha có đo trace nhưng metric/log BARO/SimpleRCA được nối từ mốc thật. | Không viết trong báo cáo cuối rằng return không có tín hiệu hoặc mọi ca trễ mạng chỉ có tín hiệu ở cạnh. FlashTicket cần quan sát phù hợp, chưa được khẳng định collector chữa được dữ liệu công khai. |
| R2 | Đổi duration sang uncovered gần giữ hạng chưa bác bỏ chờ. OR cờ theo trace có thể giữ trace trong nhóm dù caller mất cờ. Thu thêm bảng theo trace, không chạy lại PageRank. | Phân biệt cách chia yêu cầu bất thường với cách chấm dịch vụ. Chưa loại ứng viên xử lý chờ chỉ từ phép M-D cũ. |
| R3 | Giữ dev-14701a3bbb chưa rõ dưới cả hai luật. dev-607751ac0a luật code không gắn theo cây con nhưng root vẫn có trong 2/6 trace xét. Ba dạng là quan sát, chưa bao phủ mọi nguyên nhân. | Biết dịch vụ được tiêm lỗi khác với biết vì sao thuật toán xếp sai. Chưa chọn cách sửa các ca này chỉ từ nhãn nhóm. |
| R4 | Giữ số CIRCA; mô tả độ nhạy với cửa sổ. Hai phép đổi chưa tách riêng số điểm học, phân phối nền, giai đoạn lỗi và tập nút. | Đổi đoạn dữ liệu có giá trị chẩn đoán; chưa xác nhận tỉ lệ nguyên nhân hay một cách sửa chung. Cửa sổ đánh giá chính không đổi. |
| R5 | 8 ca không có cạnh đi vào root chỉ chặn cách dựa riêng vào cạnh đi vào. | Chưa kết luận đồ thị nói chung không giúp; quan hệ đi ra/cha–con/máy–dịch vụ chưa được phép ấy đánh giá. |

Bốn báo cáo đã được sửa thống nhất: nguyen-nhan-xep-hang.md, ket-qua-phien-13.md, doc-tay.md, kiem-tiep.md. Tiêu chí 3 trong báo cáo chính ghi **đạt một phần**; các cơ chế chưa được phân xử không bị biến thành đã xác nhận. File theo phiên cũ và mọi lượt chạy được giữ. Đọc kết luận hiện tại từ bốn báo cáo và bản này, không đọc khóa no_signal cũ thành không có tín hiệu.

## Các điểm tự soát

- N1: 52 đơn vị MicroRank native gồm 46 OK sai, 2 OK đúng, 4 ERROR. 48 đơn vị đọc tay gồm 46 OK sai, 1 ERROR, 1 đối chứng đúng; ngoài phần đọc có 3 ERROR và 1 OK đúng. Nguồn: bao-phu-nhom.json → /units, lọc method=microrank_full; kiểm tái lập trong kiem-so/. Không thay số baseline.
- N2: self-check E cũ kiểm KQ13 mục 1–6; không kiểm phần đọc tay mục 7 hoặc doc-tay mục 8. Đã đối chiếu riêng phần này bằng số/phiếu lưu, phạm vi và con trỏ nguồn trong kiem-so/. Không gọi tìm chuỗi số trong văn bản là kiểm đúng nghĩa của mọi câu.
- N3: mốc KT-1 so nhóm trace khác loại; hai mốc khai trước không đạt vẫn được giữ. Phần so cùng loại là phân tích sau khi xem kết quả; không biến thành phép kiểm tách nguyên nhân.
- N4: chưa có nguyên văn đề xuất tương ứng lời duyệt “1 2 3” và dòng Q-142 cũ mà phản hồi chỉ đọc nhắc. Không tái dựng từ trí nhớ. Sổ hiện tại ghi đúng lời duyệt sửa mới của Minh; quyền sửa hiện tại không phụ thuộc vào lời duyệt cũ chưa truy được.
- N5: khi kiểm số phát hiện câu “S-1 không đổi” dùng hạng tốt nhất, trong khi cách đọc chung dùng hạng bi quan. Nguồn simplerca-s1-001/summary.json → /cases/15: native [3,3], changed [3,5]; contrast_scale_v1.py dùng rank_min để gán nhãn tác dụng. Minh duyệt riêng câu thay ngày 12/10. doc-tay mục 8.2 điểm 1 nay ghi giữ hạng tốt nhất 3, hòa [3,5], hạng bi quan 5. Không sửa JSON hay số đã chấm.

## Phạm vi kiểm và bảo toàn lịch sử

Manifest phiên 13 khớp 28/28 file trước sửa; bản trước cùng hash ở truoc-sua.json và ban-truoc/. Manifest phiên 13 được giữ nguyên và chỉ áp dụng cho bản trước của các báo cáo đã sửa. Manifest mới pin bản sửa và nguồn liên quan. REVIEW.md chỉ được điền bảng phản hồi; phần nhận xét và prompt của reviewer giữ nguyên. LOG nối thêm; STATE chỉ dòng T-032. Không sửa SPEC, src, dữ liệu, môi trường, điểm hoặc cửa sổ đóng băng; không mở test, không commit/push.

Lượt mới về M-D lưu thiết kế, script, bảng theo trace, kiểm đối chiếu và mọi lượt lỗi trong md-partition/. Kết quả đầy đủ, chi phí thực và giới hạn được ghi ở phần Kết quả bổ sung M-D dưới đây; file còn nguyên sau usage limit, đã được Codex chính kiểm lại. Prompt phiên mới ở prompt-codex-kiem-lai.txt được dựng nguyên văn từ Prompt chung + Kiểm lại phản hồi và sửa + G2 trong docs/review-prompt.md; chỉ các trường thông tin lượt được điền. Mặc định phiên mới chỉ đọc và trả lời trong chat, vì chưa có quyền ghi REVIEW-2.md.

## Kết quả bổ sung M-D đã kiểm từ file thật

Nguồn: md-partition/attempt-003/summary.json → /status_counts, /cases; case và bảng trace của từng ca trong cùng lượt. Thiết kế ở md-partition/DESIGN.md. Đối chiếu độc lập từ bảng trace đã lưu: kiem-md-doc-lap.json. Hash đầu vào và cả ba lượt đã được kiểm; mọi nguồn đóng băng giữ nguyên.

- 52 ca có trong mẫu số: 48 PASS và 4 N/A do native ERROR. Ở 48 ca, bảy kiểm tra khớp cờ native từng span, thống kê nền, tổng cờ/nhóm của native và M-D, đếm phủ native, OR theo trace và miền giá trị uncovered đều đạt; 8 phép thử khoảng thời gian đạt. Không chạy lại phương pháp hay PageRank.
- Trong 20 ca có dịch vụ gọi trực tiếp đứng trên root ở native, cả 20 có trace mất toàn bộ cờ của một caller nhưng vẫn thuộc nhóm A vì root hoặc dịch vụ khác còn cờ. Có 19 ca còn caller trên root dưới M-D. Đây là bằng chứng về thông tin tại bước OR và đếm phủ, không phải tỷ lệ nguyên nhân sai hoặc chứng minh tất cả hạng giữ nguyên do bước này.
- Ví dụ dev-5467884de4: frontend mất toàn bộ cờ ở 7 trace nhưng các trace vẫn A; trong 7 trace đó root không mang cờ M-D, còn dịch vụ khác mang cờ. Root hạng 5 ở cả native/M-D. Tổng A đều 484, nhưng thực tế có 1 A→N và 1 N→A; vì vậy tổng nhóm bằng nhau không có nghĩa các trace trong nhóm giống nhau. Con trỏ: md-partition/attempt-003/summary.json → /cases, opaque_id=dev-5467884de4, /postanalysis/caller_witnesses/frontend và /transitions; bảng từng trace ở attempt-003/traces/Nezha-OB-dev-5467884de4.json.
- “Nhóm” ở đây là **nhóm các yêu cầu/trace bất thường A** hoặc bình thường N. Một trace có thể chứa span của root, caller và nhiều dịch vụ khác. Thuật toán lấy mọi thao tác trong trace A để dựng đồ thị và đếm phủ; không phải gộp root và caller thành một dịch vụ hay một nguyên nhân. Do đó caller còn được tính có mặt trong A ngay cả khi riêng nó không còn cờ.
- Đối chứng native đúng: dev-57546fd87b và dev-f81f88234e (RE2-TT, delay, root ts-auth-service); không có caller trực tiếp trong tập quan sát. Không có ca native đúng cùng dataset/fault cho cohort 20 ca trên. Thiếu đối chứng phù hợp nên không gán đặc tính OR chung thành nguyên nhân riêng của mọi ca sai.

Giới hạn: M-D đổi cả đại lượng và mức nền; cờ mất chưa xác nhận cờ ban đầu do chờ vật lý. Khi nhóm trace đổi, bảng này chưa tách vai trò PageRank/trọng số/spectrum trong điểm cuối. Muốn phân xử phần còn lại phải đọc trung gian trọng số và điểm đã lưu cho chính ca, kèm đối chứng phù hợp; nếu thiếu thì trình đúng phần thu thêm, chưa tự chạy vượt quyền. RQ2 và quyết định chọn thiết kế P5–P6 vẫn mở ở phần phụ thuộc này.

Chi phí tính thực: 287,300 giây (4 phút 47 giây) cho cả ba lượt; lượt đầy đủ cuối 157,055 giây. Hai lượt lỗi do chưa tìm đúng liên kết capture của một ca đã đóng theo cách hồi cứu; giữ nguyên failure, script từng phiên bản, kết quả đã có và manifest. Lượt cuối dùng liên kết có hash từ audit/check.json. Không có lệch số tính toán trong các ca PASS của lượt lỗi. Ghi chú trước bị ngắt đã gọi nhầm ca lỗi là ERROR; nguồn failure và bản đầy đủ cho thấy thiếu đường capture, không phải sai dữ liệu/cách tính.

## Tự kiểm bản sửa

Bộ kiểm phần đọc tay: kiem-so/result-after-004.json, 412/412 đối chiếu đã ánh xạ đạt; gồm hạng native của 68 đơn vị đọc nốt, các tổng đếm và các điểm nguồn được liệt kê. Không bao phủ mọi số/nhận định trong doc-tay mục8: số theo cạnh của mục8.3 điểm10 và một số cực trị hồi quy cần dùng chuỗi nguồn riêng, không được chứng nhận chỉ bởi bộ này. Script E cũ vẫn chỉ kiểm mục1–6 của KQ13.

Kiểm cũ chạy lại trong gói này: self-check-phien12.json (A46/46, D15/15), self-check-phien13.json (E61/61). B/C là rà chuỗi số với phiếu/đoạn dẫn, có các mục không tìm thấy do số mới, số dòng hoặc mã ca; không nhận là đã kiểm đầy đủ từng câu. Bản kiểm cuối sau khi thêm bảng M-D được giữ thành lượt mới, không ghi đè các lần trước.


## Hoàn thiện sau usage limit — 12/10/2026

Codex chính đã kiểm file thật, không dựng lại tiến độ từ lời trợ lý. M-D attempt-003 có đủ52ca và manifest; hai lượt hỏng, các scriptv1/v2/v3, source hash và bảng trace đều có thật. Cả ba manifest và mọi hash nguồn hiện khớp. Không cần chạy lại phần trích đã hoàn tất. Nhật ký hoàn thành riêng ở md-execution-finish.md; EXECUTION.md của trợ lý giữ đúng bản đã pin trong manifest.

Bản kiểm số cuối: kiem-so/result-after-008.json,412/412 đối chiếu đã ánh xạ đạt. Kiểm thêm17đối chiếu trong kiem-so/kiem-so-bo-sung.json cũng đạt: hai cạnh lời gọi chậm và các cực trị của sáu ca CIRCA, với hash/con trỏ cụ thể. Vì vậy hai nhóm số ấy không còn thiếu kiểm; bộ412 vẫn không chứng nhận mọi token hay lập luận cơ chế.

Self-check E cuối ở self-check-phien13-005.json:61/61đạt. Các lượt002và004 được giữ: script tìm chuỗi báo1điểm vì dấu cách trong danh sách số và trước số in đậm; Codex đã đối chiếu bản trước, khôi phục đúng định dạng câu gốc không thuộc sửa nội dung rồi kiểm lại. Số nguồn không đổi. A46/46vàD15/15đạt ở self-check-phien12-003.json; B/C còn mục rà chuỗi không tìm thấy, không gọi chúng là phép kiểm số đầy đủ.

Prompt được kiểm nguyên văn ngoài8trường thông tin; công đoạn Kiểm lại phản hồi và sửa cùng khốiG2 giữ nguyên. Phiên mới mặc định chỉ đọc/trả lời chat; chưa tự cấp quyền tạo REVIEW-2.md. Chưa mở phiên mới, chưa gửi prompt, chưa commit/push.

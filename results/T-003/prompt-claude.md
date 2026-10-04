Bạn là người phản biện độc lập cho task T-003 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-003-the-dataset-ngoai-rcaeval/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-003-the-dataset-ngoai-rcaeval/SPEC.md, tasks/T-003-the-dataset-ngoai-rcaeval/LOG.md, các file đầu ra: results/T-003/, results/T-008/, results/T-009/, results/T-010/, results/T-011/, results/T-012/, SPEC.md và LOG.md của các nhánh T-008–T-012, data/README.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md và docs/LESSONS.md,
và kết quả `git diff HEAD` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.

# Prompt phản biện

Dùng khi một task chuyển sang "chờ phản biện". Người phản biện là agent **khác** người làm của task (AGENTS mục 1).

## Cách chạy

**Codex phản biện** (chế độ chỉ đọc; chương trình Codex tự lưu câu trả lời cuối vào `REVIEW.md`):

```
codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-xxx-<tên>\REVIEW.md "<dán prompt>"
```

Hoặc mở Codex tương tác trong `D:\RCA-flashticket` rồi dán prompt.

**Claude phản biện:** mở một phiên Claude Code mới trong `D:\RCA-flashticket` rồi dán prompt. Claude được ghi đúng một file là `REVIEW.md` của task.

Sau khi có `REVIEW.md`: mở phiên của người làm, dán câu "Đọc AGENTS.md. Task T-xxx đã có REVIEW.md, hãy ghi ý kiến cho từng điểm vào bảng cuối REVIEW.md và vào LOG, chưa sửa gì khác."

## Prompt chung

Người làm chép prompt này vào cuối `LOG.md` của task, điền chỗ `<...>`, rồi thêm đoạn trọng tâm của cổng nếu có.

```text
Bạn là người phản biện độc lập cho task <T-xxx> của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/<T-xxx-tên>/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/<T-xxx-tên>/SPEC.md, tasks/<T-xxx-tên>/LOG.md, các file đầu ra: <danh sách>,
và kết quả `git diff <commit gốc>` nếu có.
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
```

## Trọng tâm thêm theo cổng

**G0 — MRP:**
```text
Đọc thêm docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
1. Chuỗi gói việc P1–P10 có đi đúng chuỗi cô yêu cầu không
   (hiểu sâu phương pháp → nhiều dataset → hạn chế → 5 bước đồ thị → tích hợp sản phẩm)?
2. Có bước nào cô yêu cầu mà MRP bỏ sót hoặc hiểu sai không?
3. Cách hiểu "graph-based anomaly detection" ở MRP §2.3 có hợp lý không? Có cách hiểu nào tốt hơn không?
4. Câu hỏi nghiên cứu nào không trả lời được bằng dữ liệu dự kiến?
5. Có lựa chọn nào lặp lại một sai lầm trong LESSONS không? Có lựa chọn nào thiếu câu trả lời "tại sao" không?
```

**G1 — phương pháp, dataset, cách chia:**
```text
Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```

**G3 — khóa thiết kế trước khi mở test:**
```text
Mỗi thành phần của phương pháp có trỏ về một hạn chế cụ thể ở P4 không;
có lựa chọn nào được chọn theo mức chênh giữa nhánh đồ thị và không đồ thị không;
nhánh không đồ thị và baseline có đủ mạnh không; giá trị trung gian có gì vô lý không;
bảng diễn giải kết quả đã khóa trước chưa; có rò nhãn không.
```

**G4 — kết quả:**
```text
Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

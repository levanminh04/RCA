# Nháp cho tài liệu chung — chưa ghi nguồn chung

Không sửa AGENTS/MRP/WHY/DECISIONS/LESSONS/K1 hay task cũ. Các mục dưới là đề xuất cho Minh, không phải quyết định. T-013 không chốt cửa sổ/dataset/protocol.

## 1. DECISIONS — ghi quyền thực hiện task

- File đích: `docs/DECISIONS.md`.
- Cũ: chưa có dòng ủy quyền T-013.
- Mới đề xuất, mã do người cập nhật chọn sau khi đọc lại file: “04/10/2026 — Minh ủy quyền Codex tự viết và tự duyệt SPEC T-013 theo prompt Đợt 1 rồi triển khai ngay; người phản biện Claude. Phạm vi ghi chỉ task T-013, results T-013, work T-013 ngoài repo và một dòng STATE; không thay quyết định cửa sổ P3/dataset/protocol G1.”
- Lý do: quyền đang ở prompt/LOG cần bền trong nguồn chung; kết luận phụ thuộc: phạm vi thực hiện T-013, không phải quyết định khoa học mới.

## 2. WHY — cách kiểm cơ chế T-013 (đề xuất, chưa quyết G1)

- File đích: `docs/WHY.md`.
- Cũ: chưa có mục về lựa chọn ví dụ/cách ghi hòa và ba implementation BARO.
- Mới đề xuất:

“Chọn ví dụ T-013 theo rule khóa trong SPEC: TT có metrics.parquet lớn nhất trong 30 ca dev, OB khớp hash mẫu README nếu có; không chọn bằng rank/root. Vì sao: kiểm quy mô TT và nối mốc A mà không chọn kết quả đẹp. Phương án khác: ca nhỏ nhất tiết kiệm thời gian nhưng không kiểm quy mô; chọn ca sai/đúng sau rank chỉ hợp phân tích P4. Điểm tính lại độc lập rồi mới nối nhãn. Code authors được giữ nguyên cả signed max, quantile dict và tie theo cột; đó là đối tượng mô tả/tái lập, không phê duyệt chúng cho protocol P3. Kết luận phụ thuộc: các ví dụ trong T-013, không hiệu quả toàn tập. Source: SPEC T-013, chon-ca.json và kiem-tra.json.”

- Lý do: lựa chọn quan trọng chưa có WHY; kết quả tại chỗ ghi chờ WHY. Không tự chốt cửa sổ hay mapping G1.

## 3. K1 — phân biệt bài với code và đơn vị độ đo

- File đích: `docs/knowledge/K1-phuong-phap-rca.md`, sau công thức §C.4 và dòng độ đo.
- Cũ: công thức bài RobustScorer và mô tả detector trên samples.
- Mới đề xuất:

“Công thức trên là của bài. Ở revision BR e35f4ec và RE259ea41, DataFrame scorer dùng max z có dấu; BR dict dùng quantile theo chỉ số và abs(max−median), không tương đương hai phía. N-Sigma RCA cũng max có dấu/ddof=0; detector N-Sigma abs/ddof=1 và lịch sử mở rộng. Artifact detector BARO đếm theo ca: có alarm là TP, alarm đầu trước injection thêm FP; một ca có thể vừa TP vừa FP. Không dùng số này như P/R/F1 theo window của MRP. T-013 so độc lập từng điểm/posterior và ghi khác biệt bài/code; xem ho-so-baro, ho-so-bocpd, ho-so-nsigma-phat-hien.”

- Lý do/kết luận phụ thuộc: hiểu cơ chế và điều kiện chuyển dataset, không tự đổi benchmark cũ.

## 4. Task cũ — sửa diễn giải tối thiểu

- File đích: năm vị trí D1–D5 trong `dinh-chinh-task-cu.md`; văn bản cũ→mới nguyên văn ở từng mục đó.
- Lý do: bổ sung chứng minh IQR thô, sentinel, điều kiện Recall = 1, tổng chi phí. Số tái lập cũ chưa có bằng chứng cần đổi. Kết luận phụ thuộc: hiểu đúng mốc/tính đúng/chế độ (b)/khả thi.
- Không đề xuất sửa source tác giả hoặc áp dụng bản sửa index vào benchmark trước G1; ảnh hưởng bản sửa detector đầy đủ còn ngoài task.

## 5. G1 — các lựa chọn vẫn OPEN

- File đích: hồ sơ tổng hợp G1 khi Minh chốt; chưa sửa MRP/WHY để cam kết trước.
- Cũ: Q-54 giữ cửa sổ P3 OPEN.
- Mới đề xuất khi có quyết định: ghi rõ row count/cadence, protocol(a)/(b), (b) hồi cứu hay (b) online, rule hòa, mapping metric→service và cách xử lý datapoints ngoài range. Căn cứ có ở `cua-so-va-che-do-b.md`, ví dụ từng ca và chi phí tổng. T-013 không đề xuất con số cửa sổ cụ thể.
- Lý do/kết luận phụ thuộc: khả năng chấm RQ3a và so RCA trên cùng điều kiện; không thêm cổng hay cơ chế kiểm soát mới.

## 6. WHY — phân bổ tác động biên DELAY khi sửa R1 (nháp, chờ Minh)

- File đích: `docs/WHY.md`; chưa ghi nguồn chung.
- Chọn gì: trình bày cả hai thứ tự thêm nền/thêm hậu và lấy trung bình hai thứ tự nếu cần một phân bổ cộng được, không ưu tiên thứ tự. Đây là quy ước số học của phân tích R1, không chọn cửa sổ hoặc nguyên nhân vật lý.
- Vì sao: có tương tác. Nền rồi hậu cho −0,224/−0,032; hậu rồi nền cho 0/−0,256. Chỉ dùng một thứ tự sẽ gán phần tương tác tùy thứ tự. Trung bình cho nền −0,240, hậu −0,016 và tổng −0,256.
- Phương án đã xét: giữ riêng hai thứ tự (đã công bố để người đọc kiểm); chỉ dùng nền trước; chỉ dùng hậu trước; chia tác động std/mean/candidate thành các thành phần riêng (chưa kiểm, không đủ phép can thiệp độc lập ở run này). Không gọi phần nền là tác động thuần std.
- Bằng chứng: `results/T-013/trung-gian/cua-so-delay-ca.csv`, `cua-so-delay-variants.csv`, `cua-so-delay-summary.json`; 25 ca × 4 phối hợp, 50 endpoint khớp rank cũ; công thức và ba ca cụ thể ở `cua-so-va-che-do-b.md` §1. Bốn ca có candidate thêm, đã tính cùng pipeline vào tác động biên.
- Kết luận phụ thuộc: chỉ hai số phân bổ trung bình. Bốn Avg@5, rank/score từng ca, chênh 0,256 và tương tác không phụ thuộc việc Minh duyệt quy ước này. Gai nền/hậu là tải, lỗi hay quan sát vẫn chưa kiểm; số liệu không phân xử nhân quả.

## 7. DECISIONS — quyền sửa sau phản biện (nháp)

- File đích: `docs/DECISIONS.md`; chưa ghi nguồn chung.
- Mới đề xuất: “04/10/2026 — Minh yêu cầu ‘sửa lại các lỗi trên, test cẩn thận’: duyệt sửa R1 và N1–N3 của T-013 theo đề xuất đã ghi trong LOG phiên 2. Chưa duyệt đóng task, chọn cửa sổ, commit hoặc push.”
- Lý do: lưu quyền thực hiện qua phiên; bằng chứng lời Minh đã ghi trong LOG phiên 3 và bảng phản hồi REVIEW. Không là quyết định khoa học mới.

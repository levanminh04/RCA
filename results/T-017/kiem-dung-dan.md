# Kiểm đúng đắn — T017

Các phép kiểm xác nhận từng điều kiện cụ thể, không đồng nhất “không lỗi” với “chạy đúng”. Số bàn giao ban đầu lấy run-dev-004 (`runs/final-summary.json`); 001–003 giữ nguyên lịch sử. Sau sửa N1/N2, lượt mới run-dev-005 khớp toàn bộ 30 diagnosis của run004; kiểm mới tại `runs/fix-n1n2-001/verification.json`. Quy ước M4 **(quy ước triển khai T017, xem docs/WHY.md WHY-17; chưa chốt P3)**.

## Kiểm đạt tại bàn giao run004

| Phép kiểm | Kết quả và bằng chứng |
|---|---|
| Known-answer tổng hợp |16 unittest đạt; metric2+trace1+log1=4, strict threshold, missing/empty, tie, absent entity, std0, alias collision/cycle, boundary/units, negative duration |
| Script độc lập |12 nhóm self-test đạt;2226 mục so ví dụ đạt, mọi count/score/rank bằng tuyệt đối (`example-comparison-v2.json`) |
| Lặp lại |Hai ca đầu allowlist, JSON bằng tuyệt đối (run004 summary/repeat) |
| Đảo thứ tự cột |Hai ca đầu, output/tie groups bằng tuyệt đối; tổng hợp cũng đạt |
| Không fallback/không rỗng/tổng điểm |30/30 đạt;0 ranking trùng thứ tự entity từ cột metric; không dùng fallback (`final-summary.json`) |
| Hòa |Giữ tie group, fractional Hit và bounds; lexical chỉ display (test_ties_and_unobserved) |
| Missing log |cpu_1 unavailable, giữ ca; synthetic phân biệt None và bảng rỗng |
| Input guard |30ca/89file resolve đúng nguồn;2ca ngoài guard và file resolve ra ngoài bị chặn trước đọc (`supplement-001/guard-check.json`). File escape tổng hợp dùng mock resolve, không tạo symlink thật; các file thật không trỏ ngoài |
| Alias |Giữ tên DB, alias trace/log tường minh về metric hoạt động; collision metric/cycle/cột trùng lỗi; ca thứ hai baseline sau guard changes bằng run004 |
| Log sensitivity thực |Ngưỡng0/1/10 có1entity nhận phiếu, độc lập count từng entity đạt; không chọn cấu hình (`supplement-001`) |
| Provenance |30mốc metadata hash khớp manifest T002,70Git blob khớp, PDF bảng2/3 xem ảnh; số công bố tra trước dev |

Metric name parser tách underscore cuối theo schema RCAEval; chưa hỗ trợ suffix metric có underscore tùy ý. Trace và log timestamp range guards kiểm đúng đơn vị. Duration vật lý chưa xác nhận nhưng ratio cùng nguồn không cần đổi. Kiểm guard và alias sau run004 không làm đổi computation với aliases=None; baseline ca thứ hai xác nhận điều đó.

## Sửa N1/N2 đã được Minh duyệt ngày 04/10/2026

N1 là lỗi khóa danh tính: guard bàn giao chỉ kiểm count và đường dẫn, chưa ngăn tập 30 ca bị thay tên. Runner nay đọc `allowlist.json` đã khóa, không ghi đè; kiểm exact-set, thư mục và file resolve trước tạo run hoặc hash/đọc telemetry. Đường dẫn resolve phải giữ chính danh tính ca, kể cả khi đích khác vẫn ở cùng data root. Bộ lọc artifact dùng cùng loader; alias chỉ bỏ prefix từ tên được phép, predicate áp trước trả dòng. Test dùng tên/đường dẫn/row tổng hợp, không mở ca ngoài quyền.

N2 là lỗi hợp đồng ứng viên: adapter nay giữ định danh log trong `[t−half,t+half)`, chuẩn hóa cùng alias, truyền `observed_services`; chỉ log `[t,t+half)` được truyền message để đếm lỗi. ERROR chỉ normal không có phiếu. Thiếu modality và bảng rỗng vẫn khác nhau. `prepare` trả `PreparedInputs` gồm 5 bảng, `metric_services`, `observed_services`; runner truy cập trường bằng tên. Metadata normalized giữ observed_services để bản tính độc lập không mất service normal-only; không lưu message normal.

| Kiểm sau sửa | Kết quả và nguồn |
|---|---|
| Tổng hợp |25/25 unittest đạt; gồm thay tên giữ count30, đổi thứ tự hợp lệ, resolve sang danh tính khác, từ chối trước mkdir/hash/read, predicate prefixed/unprefixed, normal-only ERROR/alias/boundary/log-only/None-vs-empty (`runs/fix-n1n2-001/unit-tests.txt`) |
| Dev và nguồn |30 diagnosis khớp run004 từng JSON; mọi source hash khớp; 2041 tổng score service được kiểm lại; hai ca repeat/permutation đạt; 14 output phụ khớp (`runs/fix-n1n2-001/verification.json`) |
| Guard thực |30 ca/89 file đúng phạm vi; phản ví dụ exact-ID/resolve đạt (`runs/supplement-002/guard-check.json`) |
| Ví dụ độc lập |13 nhóm self-test; 2458 so count/available/float/thành phần/rank/tie/log đạt; max absolute float error 1.16415e-10, dùng relative/absolute tolerance1e−10 (`runs/fix-n1n2-001/independent-example.json`, `verification.json`) |
| Log sensitivity |Ca thứ hai với ngưỡng0/1/10 khớp count độc lập; baseline bằng run005 (`runs/supplement-002/summary.json`) |
| Artifact |Hai parquet có case identity vẫn trả0devrows; không telemetry hoặc giá trị ngoài allowlist (`runs/fix-n1n2-001/fse-filter-001/fse-artifact-result-filter-check.json`) |

Hit1 vẫn25/30; Hit3/5 vẫn29/30; MRR=0.8911111111. Hai normal-control vẫn không đạt abstention; không đổi threshold. Run005 elapsed 46.25s; bộ lọc 1.76s. Chỉ là tiến độ khi máy dùng chung, không phải benchmark cost chính thức. Mọi lượt cũ, allowlist và REVIEW giữ nguyên. Inventory/handoff cũ là snapshot bàn giao; danh sách thay đổi và kiểm bảo toàn sau sửa nằm trong `runs/fix-n1n2-001/`.

## Normal/normal: kết quả không đạt abstention trên dữ liệu thực

Synthetic hai cửa sổ constant bình thường trả abstain đúng. Hai ca thực dùng normal[t−450,t−300) và normal[t−300,t−150), hoàn toàn trước mốc inject đã biết, vẫn trả heuristic_alerts:

| Ca | Score lớn nhất | Entity điểm dương | Abstention |
|---|---:|---:|---|
| re2tt_ts-auth-service_cpu_1 | 196 | 48 | Không đạt |
| re2tt_ts-auth-service_cpu_2 | 278 | 42 | Không đạt |

Nguồn `runs/run-dev-004/*-normal-control.json` và `final-summary.json`. Đây là phép kiểm đã làm và không đạt; không ghi “chưa kiểm”, không điều chỉnh threshold để làm đẹp. Điểm dương không được gọi là tìm ra nguyên nhân có ý nghĩa trong hai cửa sổ này. Các nguyên nhân khả thi khác: baseline/window khác phân bố, std thấp, drift, tương quan thời gian, nhiều phép vượt ngưỡng, hoặc nominal normal có bất thường chưa có nhãn. Không phân tích định lượng toàn dataset (P4) trong task này.

## Tái lập và số công bố

Bảng2 nguyên số ở `so-cong-bo.csv` tra trước chạy. RE2-TT công bố Top1=0,80 trên90ca. Bản M4 này trên30dev có Hit1=0.833333, Hit3/5=0.966667, MRR=0.891111; mỗi ca/bounds có `diem-dev.csv`. Không gọi đây là tái lập trọn hoặc bằng chứng vượt tác giả.60ca đang khóa, source artifact được kiểm không cung cấp output30dev, code/config/window/tie sinh bảng2 chưa xác định. So paper vs dev trực tiếp trộn denominator/protocol/implementation.

Zenodo17105974: hai zip code có inventory/license/hash, không telemetry mới. FSE artifact mới dùng lại từ T012: code21file giống orig; hai parquet kết quả áp predicate allowlist trước đọc/trả giá trị,0devrows. Đã làm kiểm được phép; không ghi “chờ quyền” để bỏ lọc kết quả (`doi-chieu-code.md` §8).

Table3 có mâu thuẫn Eadro-SN I+II hiển thị0,94 nhưng cộtI&II0,96; giữ cả hai theo PDF, chưa tự sửa hoặc tính Type trên dữ liệu mới. Chi tiết `type-i-ii.md`.

## Lượt hỏng, sửa lỗi và thời gian

run001 ca thứ hai thiếu metadata nguồn dự kiến; run002 thiếu local metadata. Lấy30file mốc đúng nguồn/hash đã ghi T002 (tổng300byte), giữ failed JSON/progress. So trung gian phát regex pod làm gộp DB thànhts; bỏ suy đoán tên, thêm regression test, chạy lại30 ở004 lý do(c). Không đổi ngưỡng theo kết quả. Cột registry được dựng lại từ từng run/check, giữ registry thô lịch sử.

Mọi lượt có progress và elapsed ngay từ đầu. Laptop đang chạy nhiều phiên nên không số thời gian chính thức, không so5,99s của tác giả. Môi trường ghi phiên bản phụ đầy đủ; lệnh dựng tại `moi-truong.md`. Không EC2, không lượt>1giờ, không tải dataset mới.

## Chưa kiểm thật sự và hệ quả

| Việc | Lý do | Giả định và khi sai | Cách kiểm/đầu vào cần |
|---|---|---|---|
| Tái lập90RE2-TT |60khóa và chưa có đúngcode/config |Không giả định30 đại diện90; sai nếu chọn dev thiên lệch |ChốtG1, quyềnG3 và chương trình/outputs tác giả |
| So từng ca tác giả |Predicate ở nguồn đã có trả0devrow |Nguồn khác có thể có outputs chưa thấy |Tác giả cung cấp đúng30dev, lọc trước đọc |
| Type exact executable |Bài thiếu rule aggregation/threshold/“stronger” |Không mặc địnhví dụ2× là cấu hình dùng mọi dataset |Code/count/config gốc; không tự tính dataset mới |
| Cost chính thức/quy mô khác |8phiên cùng máy; P3 không thuộc task |Elapsed này không đại diện chạy đơn hoặc hệ lớn hơn |Máy rảnh, protocol G1/P3; không EC2 tại T017 |
| Đơn vị duration, service-latency semantic |Schema chỉ biết cùng nguồn; không đủ physical documentation |Nếu normal/incident khác đơn vị hoặc operation mix thay thì ratio sai nghĩa |Metadata rawcollector; đếm ratio không giải quyết latency semantics |
| Tổng quát hóa failure mechanisms |P4/giao thức dataset chưa chốt |Điểm dương không đồng nghĩa causalroot hoặc calibration |Thực nghiệmP4 sau G1, không tự thiết kế đồ thị |

Không có việc rẻ trong giới hạn đã nêu bị để “chờ quyền”. Bảng tiêu chí `tieu-chi-xong.csv` phân biệt đã hoàn thành công việc với hạn chế kết luận.

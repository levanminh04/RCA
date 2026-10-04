# Phản biện T-019

- **Người phản biện:** Codex — **Ngày:** 04/10/2026 — **Commit/diff đã đọc:** mốc mở phiên trong LOG; đã đọc toàn kết quả `git diff 93f13d4c4a966428177e2acc287d96bc89303e92`. Diff chỉ có các dòng STATE của nhiều task; đầu ra T-019 chưa được Git theo dõi nên được kiểm trực tiếp theo inventory.
- **Phân vai — USER_CONFIRMED:** SPEC ghi Codex làm, Claude phản biện. Minh xác nhận trong phiên này: “Cho phép phiên Codex này phản biện T-019”. Ngoại lệ chỉ áp dụng phiên phản biện này. Không sửa SPEC, LOG, STATE hay quyết định chung.
- **Đã đọc:** AGENTS.md; SPEC và toàn LOG T-019; mẫu REVIEW và thẻ dataset; docs/{STATE,MRP,WHY,DECISIONS,LESSONS,review-prompt}.md; hai nguồn DT18/advisor được giao. Đã đọc thẻ, báo cáo, tiêu chí xong, tự phản biện SPEC, tài liệu tái lập, đính chính, nháp chung; code khảo sát/kiểm và các bảng census, schema, biên, nhãn, probe, exclusions, lineage, exposure, manifest của T-019. Đối chiếu nguồn và các phần liên quan của T-001/T-002/T-003/T-006/T-007. Kiểm toàn bộ đường dẫn và hash bàn giao; không gọi việc kiểm hash là đã đọc ngữ nghĩa mọi file.
- **Nguồn chính thức đã đối chiếu:** [RCAEval v2 §3](https://arxiv.org/html/2412.17015v2); snapshots HF/Sock Shop ghim trong source manifests; runner RCAEval tại revision trong `results/T-019/runner-source/manifest.json`. Hai phương pháp kiểm lấy mẫu: [BARO v1 §3.4](https://arxiv.org/html/2405.09330v1) và [TORAI v1 §3.1–3.4](https://arxiv.org/html/2604.13522v1), cùng code chính thức local đúng revision đã ghi trong T-001.

## Kết luận chung

Không thấy lỗi chặn hoặc lỗi khoa học đáng kể trong thẻ Sock Shop, census, khảo sát metric và sổ ca đã nhìn. Có một điểm KHÔNG CHẶN: kết quả kiểm bàn giao lưu sẵn không còn xác nhận LOG hiện tại. T-019 cung cấp bằng chứng cho tổng hợp G1; chưa phải quyết định chọn dataset hoặc bằng chứng phương pháp đồ thị có hiệu quả.

## Các điểm

### R1. Kết quả kiểm bàn giao không khớp LOG hiện tại — KHÔNG CHẶN

- **Ở đâu:** `results/T-019/artifact-manifest.json:10–14`; `results/T-019/handoff-checks.json:4–5,15`; `results/T-019/tieu-chi-xong.md:12`; prompt cuối `tasks/T-019-the-sock-shop/LOG.md:174–209`.
- **Sai gì:** bước 9/tiêu chí xong 8 viện dẫn bản kiểm bàn giao đạt. Nhưng hai khẳng định “hash đầu ra còn khớp” và “prompt khớp nguyên văn với danh sách đầy đủ” không đúng với bộ file đang phản biện. Hệ quả: không dùng bản PASS này để xác nhận LOG hiện tại chính là bản đã kiểm lúc bàn giao. Không ảnh hưởng trực tiếp các số khoa học đã tính lại.
- **Bằng chứng:** kiểm chỉ đọc toàn manifest: 925 đường dẫn đều tồn tại, đúng phạm vi và không thiếu file; trong 923 mục có hash, chỉ LOG không khớp. Manifest ghi LOG 158.173 byte, file hiện tại 28.111 byte. Đối chiếu prompt cuối với `handoff.prompt_for(handoff.inventory())` trả `false`; bản lưu sẵn ghi `true` cho cả hai phép kiểm và `all_pass`. Chỉ import các định nghĩa, không gọi `build()`, `verify()` hay hàm ghi. Hash của các đầu ra khoa học và dữ liệu được kiểm đều khớp.
- **Phản bác đã xét:** LOG hiện dẫn phạm vi đầy đủ qua `output-files.csv`; inventory đó thực sự đủ. Có thể LOG đã được rút gọn sau lượt kiểm thành công. Chưa có lịch sử để quy thời điểm hoặc người tạo sai khác. Vì vậy đây là sự không khớp hiện tại của chứng cứ bàn giao, không phải kết luận người làm đã kiểm sai lúc đầu, không phải mất dữ liệu và không phải lý do chạy lại RCA.
- **Đề xuất sửa:** khi người làm được Minh cho phép, xác định bản LOG dùng để bàn giao và cập nhật manifest/kết quả kiểm tương ứng bản đó; giữ bản kiểm cũ theo luật giữ lượt chạy. Không tiếp tục viện dẫn PASS cũ cho LOG hiện tại. Không cần sửa số liệu khoa học.

## Điều đã kiểm và thấy đúng

Hai nhánh hỗ trợ chỉ đọc kiểm số liệu và nguồn/lineage. Người phản biện kiểm lại bằng chứng và quyết định nội dung bản này. Không nhánh nào ghi file, chạy RCA/detector hoặc mở dữ liệu khóa.

| Tiêu chí xong của SPEC | Kết quả phản biện |
|---|---|
| 1. Mẫu thẻ và số có nguồn | RE2/RE3 riêng, mỗi thẻ 10 mục và 9 tiêu chí; RE1 ngắn. Các số kiểm được khớp artifacts. |
| 2. Census toàn release | 245 ca/618 file; RE1 125 ca/25 ô, RE2 90 ca/30 ô, RE3 30 ca/9 ô. Có danh sách từng modality; không suy từ hai mẫu. |
| 3. Revision/hash/byte và tám nhãn | 618 file SS đúng size/hash. 180 file OB lineage trong phạm vi; tổng mạng 161.824.212 byte, dưới trần 1 GB. Tám nhãn được đọc, chỉ bảy nội dung riêng; một nhãn ngoài cửa sổ own log. |
| 4. Schema, biên, normal và graph | Schema/biên được kiểm đủ 245 ca. Cả 120 ca RE2/RE3 có metric ±720 giây quanh tiêm. Vắng trace toàn release; parent/linkage/runtime degree N/A đúng, không gán 0% hoặc bậc 0. |
| 5. Probe có control và lý do loại | Tính độc lập trên toàn 120 raw metric khớp 28.098 bộ band/count và 22.572 bộ entity/nhóm/q. Táiaggregate khớp toàn 2.076 hàng theo ca và 702 hàng theo ô. Thiếu số đo không bị gán tỷ lệ 0. |
| 6. Sổ ca đã nhìn | Đọc lại 405 cặp CSV/Parquet: 400 full-content, 5 chỉ khớp phần có thời gian. Sáu archive đúng hash/count/case set và có rank không rỗng. Sổ cuối 1.245 hàng là quan hệ/exposure, không phải số incident riêng. |
| 7. Đính chính và nháp chung | Hai file tồn tại. Đính chính T-003 phân biệt đúng referral thiếu hồ sơ với lỗi số; giới hạn nhãn RE3 được nêu, không sửa nguồn gốc hoặc task cũ. |
| 8. Bàn giao và phạm vi | LOG đủ sáu ý/A–H; inventory đúng vùng được phép. Diff hiện không cho phép quy mọi thay đổi STATE cho T-019; chứng cứ splice và phạm vi code hỗ trợ việc chỉ sửa dòng T-019. Chứng nhận LOG hiện tại có giới hạn R1. Không có chứng cứ ghi nguồn chung khác. |

Các kiểm tra và giới hạn quan trọng:

- Đã đọc code và import trước khi chạy `.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py --read-only`. Toàn bộ 27 kiểm tra đạt, gồm tính lại 465 bộ band/count từ hai raw ca và táiaggregate. Kiểm độc lập bằng NumPy trên toàn 120 ca bổ sung xác nhận toàn bộ phép khảo sát; các phép tính chạy từ stdin, không lưu file.
- Reference/control/post của RE2/RE3 lần lượt 480/240/721 hàng, không chồng nhau. Median/phân vị và OR theo entity được tính trước khi gắn root/fault. Injection chỉ dùng để chia cửa sổ khảo sát mô tả đã được SPEC cho phép; không có phương pháp tự phát hiện nhận mốc tiêm trong T-019. Nhãn root chỉ dùng để tổng hợp “ngoài root”. Thẻ nêu đúng giới hạn nhiều kênh, drift, tải chung, band 0 và mẫu số thiếu; không biến tăng tỷ lệ thành nhãn lan hay nhân quả.
- Thẻ giữ riêng nguồn công bố và release/file thật. Đối chiếu bài benchmark hỗ trợ phần công cụ/giao thức; metadata ghim và file thật mới là bằng chứng vắng trace SS. Không biến nhãn chỉ báo log thành code-line, onset, trace label hoặc vùng ảnh hưởng. Số 720 giây trước tiêm được phân biệt với mô tả 10 phút của bài.
- Đã xem hình kiến trúc chính thức và bảng cạnh/bậc: năm nét từ front-end không có mũi tên; chuỗi orders→shipping→queue→queue-master có mũi tên. Bậc nêu trong thẻ là trên hình tĩnh đã loại external User/icon DB, không phải bậc runtime hoặc graph đầy đủ của deployment RCAEval. Mapping sang release vẫn CANDIDATE. Không có graph tham gia điểm, tập ứng viên hoặc xếp hạng trong task này.
- Đường nhãn trong runner được lần tới đầu ra: `runner-source/main.py:283` lấy root từ path; `:341–363` có nhánh chọn SLI theo root; `:415` truyền SLI vào phương pháp; `:427–429` lưu ranks. Thẻ báo đúng đường rò và không tuyên bố đã có adapter loại rò. Bản chính thức hoặc bản mới không tự chứng minh kết quả hợp lệ.
- Hai phương pháp kiểm lấy mẫu: BARO tại `D:/RCA-ext/src/RCAEval/RCAEval/e2e/baro.py:19–60`, preprocessing `RCAEval/io/time_series.py`, cùng code BARO gốc `D:/RCA-ext/src/baro/baro/{root_cause_analysis,reproducibility}.py`; TORAI tại `D:/RCA-ext/src/RCAEval/RCAEval/e2e/torai.py:69–342`, gồm giảm mẫu, ghép theo chỉ số và đường dự phòng `:330–334`. Revision đối chiếu qua manifest/T-001. Sai khác bài/code đã nêu trong hồ sơ P1 không được dùng để suy rằng archived ranks đúng. Rank không rỗng và metric identity chỉ đủ chứng minh exposure mà T-019 đang khẳng định.
- Danh sách P1 đã được Minh chốt tại Q-37/Q-38 và T-001 §8 có đại diện thống kê, nhân quả, trace/PageRank, đa nguồn và học có đồ thị qua GDN. T-019 không thay danh sách hoặc viết hồ sơ phương pháp mới. Hai phép kiểm lấy mẫu trên không chứng nhận toàn bộ hồ sơ P1 đã xong.
- RQ1 theo vị trí runtime và RQ3 theo trace/vùng/onset vẫn có giới hạn thật, được thẻ giữ OPEN. MRR/Hit@k/NDCG theo một service root chỉ chấm được theo giao thức G1; injection không đủ chấm phát hiện quan sát hoặc vùng ảnh hưởng. Chưa có lựa chọn dataset/dev/test để phê duyệt trong T-019. Toàn 90 RE2-SS đã qua RCA; 100 RE1-SS non-disk có exposure gián tiếp. 25 disk thiếu chứng cứ RCA trực tiếp không đồng nghĩa chưa nhìn: T-019 đã đọc metric và sổ có ghi.
- Không thấy thẻ nâng CANDIDATE thành DECIDED hoặc cam kết cơ chế đồ thị trước P4. WHY-03/04 và MRP §4 được dùng như căn cứ/đề xuất hiện có; không tạo lựa chọn mới cần WHY. Không coi các unknown của gói sau là lỗi của T-019. Đối chứng “không đồ thị” ở WHY-07/P7 đã giới hạn đúng: giữ self-time hoặc đặc trưng theo nút cha thì chỉ phân xử bước đồ thị bị bỏ; T-019 chưa triển khai hoặc suy kết luận từ phép so đó.

**Phạm vi phiên phản biện:** chỉ tạo `tasks/T-019-the-sock-shop/REVIEW.md`. Không sửa LOG/STATE/SPEC, dữ liệu hoặc kết quả; không commit/push. Minh quyết xử lý R1 và các lựa chọn G1; bản phản biện không tự đóng task.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 — KHÔNG CHẶN | Đúng | Kiểm lại trước khi thêm phản hồi: đủ 925 đường dẫn; 923 mục có hash, chỉ LOG lệch. Manifest ghi 158.173 byte, LOG khi mở phiên là 28.111 byte. Prompt cuối không bằng `handoff.prompt_for(handoff.inventory())`, dù bản kiểm lưu sẵn ghi hai phép kiểm này đạt. Phạm vi lỗi là chứng cứ bàn giao hiện tại; chưa xác lập ai đổi LOG hoặc lúc nào, không chứng minh lượt kiểm ban đầu sai. Nội dung Prompt chung + G1 vẫn nguyên văn ngoài phần danh sách file; danh sách đầy đủ còn trong output-files.csv. Kiểm khoa học `verify_final.py --read-only` đạt 27/27; không cần chạy lại RCA hay sửa số liệu vì R1. Đề xuất giữ LOG hiện tại, bảo toàn hai bản manifest/kiểm cũ rồi cập nhật chứng cứ bàn giao cho bản LOG được Minh chấp thuận; chi tiết theo file trong LOG. Phiên này chưa sửa các bản bàn giao. | |

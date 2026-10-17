# T-039 — Tự rà trước triển khai, 15–16/10/2026

**Kết quả:** hash/pin và tập graph đầu vào đạt. Chưa đủ căn cứ cam kết toàn SPEC xong trong một phiên. Chưa tải nguồn mới, lập mapping, dựng hoặc đối chiếu. Đây là tiền kiểm của người làm, không là REVIEW chính thức hoặc nghiệm thu.

Quyền hiện hành là nguyên lời Minh giao trong LOG Phiên 2. Trạng thái ĐỀ XUẤT ở SPEC/STATE trước phiên là mốc cũ, không phải mâu thuẫn quyền còn cần hỏi lại. Đã đọc Prompt chung + Soát SPEC + G3 trước tự rà; không mở kết luận phản biện/phản hồi cũ. Nhận xét dưới đây được lập từ nguồn yêu cầu, manifest, code và metadata công khai.

## Nhận xét độc lập

1. **FACT — phần thiết kế phù hợp câu hỏi nguồn.** DT18-NV2/NV3, cô bước 1 và MRP P5 đòi mô hình có nguồn và ánh xạ tín hiệu. SPEC giữ inventory khác observed nodes, hai mức, owner/scope và phép đối chiếu hai chiều. Phép tính nhận đồ thị là chuẩn hóa khóa, giao/phần riêng và phép chiếu; chưa là chấm bất thường hoặc RCA. Không cần sửa mục tiêu này. P6/P7 mới phân xử lợi ích RQ3; RQ5 còn cần dữ liệu/thực nghiệm FlashTicket. Tiền kiểm không trả lời các câu đó.

2. **FACT — pin nội dung hợp lệ.** `runs/tien-kiem-001/input-verification.json#/all_ok=true`: toàn 187 artifact T-036, mã hiện hành so snapshot/code-hashes, 11 nguồn/manifest T-008 theo manifest cuối T-003 và bảy Git blob nguồn có đối chiếu đều khớp. Không đổi pin hoặc sửa hash. Hash manifest và từng nguồn nằm trong JSON này.

3. **FACT — miền được giao đã xác định.** `runs/tien-kiem-001/graph-inventory.json`: 132 graph hiện hành, 22 opaque dev ID, hai mức và full/N/A, tổng 3.856.723 byte. Path khớp `thong-ke-do-thi.json#/canonical_graph_files`. Full có interval null và nghĩa hợp miền dev-adapter. N/A giữ interval gốc. Theo đặc tả T-035 §2, OB không có ảnh chụp 60/300; SPEC yêu cầu ảnh chụp có sẵn nên không cần tạo cửa sổ hoặc sửa SPEC. Không lấy graph trong runs/ làm đầu vào hiện hành.

4. **CHẶN phát biểu loại object cũ, KHÔNG phải lỗi hash.** `results/T-036/nguon.json`, các source ID Nezha-README/Nezha-tree, ghi `revision_kind` là git tree object. API Git commits xác nhận revision đó là commit, trỏ tới một tree khác. Toàn 1.297 thành viên path/mode/type/blob/size của tree canonical khớp tree đã lưu. README blob cũng khớp. Bằng chứng và URL ở `runs/tien-kiem-001/kiem-loai-object.json`. Không được dùng nhãn loại object cũ để suy luận lineage. Nội dung snapshot vẫn nguyên; không phải lý do đổi ứng dụng, chuyển pin hoặc xác nhận dataset deployment. Chưa sửa registry chung hoặc chọn cách xử lý thay Minh. Sửa tối thiểu cần trình là ghi rõ loại object và quan hệ commit→tree trong registry; tác động pin ba nhánh được nêu trong đề xuất tách. Phần nguồn đã có vẫn được kiểm hash độc lập.

5. **OPEN — revision ứng dụng sinh dataset.** Metadata repository Augmented-OB cho một root commit, cây đầy đủ 274 entry/219 blob và không có gitlink. Đây là snapshot ứng dụng ứng viên. Ngày công bố commit không chứng minh code ấy đã chạy khi thu dataset. Revision Nezha analysis, ứng dụng, Zenodo/dataset, image và deployment vẫn là các đối tượng riêng. Không dùng branch mới nhất/upstream khác thay nguồn. Nếu được tải, kết quả so phải có `revision_link_verified=false` và `conditional_reference=true` cho tới khi có chứng cứ nối deployment.

6. **OPEN — coverage nội dung, lineage nguồn phụ và Node.** Cây metadata chỉ xác định tập phải xét, chưa chứng minh đã đọc đủ hoặc phần loại trừ không ảnh hưởng. `data_integrate.py:239–265,483–488` đọc CSV và biến PodName/OperationName thành event; không xác nhận nó sinh danh sách Source–Target mức ngày hoặc nghĩa định danh Node. Đọc code analysis không đồng nghĩa đọc code thu. Nhận định này chỉ cho các đoạn đã đọc, không phải phủ định mọi code của repo. `cot-node-nezha.md` T-035 đã ghim cũng giữ nghĩa host OPEN; không dùng tính ổn định tên hoặc mở thêm giá trị Node. Cần code/export schema hoặc manifest tác giả để nối nguồn phụ/host/image với dataset. Không dùng metadata ngày chọn P6.

7. **CHẶN cam kết hoàn tất một phiên.** Dự toán cũ 3–5 giờ không có phân rã đủ nguồn/ngoại lệ và mọi lượt. Chưa đọc 215 file nguồn đề xuất; còn build/template/schema/generated, JAR instrumentation, nhánh failpoint và phụ thuộc ngoài snapshot. Chưa có pilot RAM/đầu ra T-039. Không có căn cứ thu hẹp khảo sát theo trace để bù phần thiếu. Cần Minh quyết cách tách trước phần triển khai phụ thuộc; đề xuất cụ thể ở `de-xuat-tach.md`.

## Dự toán toàn phạm vi, chưa đo

| Phần | Giờ công CANDIDATE | Lý do và bất định |
|---|---:|---|
| Truy lineage ứng dụng/Nezha/nguồn phụ | 1–2 | Đọc code/tài liệu đã có và phần bổ sung; nguồn deployment có thể chưa công bố |
| Coverage toàn cây và nguồn gián tiếp | 1,5–2,5 | 215 blob đề nghị lấy; không chỉ whitelist mã chính; phân xử binary/build/generated và nguồn ngoài |
| Bản ghi và mapping có owner/provenance | 1,5–2,5 | Đọc source/handler/client/config rồi mới đối chiếu; không chọn alias theo tỷ lệ khớp |
| Oracle riêng, dựng/đối chiếu | 0,5–1 | Oracle trước code riêng; 132 graph giữ mức/miền/interval và hai views |
| Phân tích mismatch và match tương ứng | 1,5–2,5 | Phải phân xử revision/alias/nhánh/telemetry/chuyển đổi, không chỉ gắn cờ |
| Tự kiểm, manifest, LOG và bàn giao | 1–1,5 | Kiểm tập/members/N/A/projection/determinism, toàn diff và giới hạn kết luận |
| **Tổng** | **7,5–12** | Chưa gồm chờ Minh/tác giả và phản biện; không phải số đo hoặc giới hạn giảm kiểm |

Giờ máy CANDIDATE 15–45 phút tổng cho tối đa ba lần thu nguồn và ba lượt đối chiếu/kiểm; mỗi lượt dự kiến dưới 15 phút, chưa đo. Q-40 áp ngân sách phương pháp; task này không chạy phương pháp RCA. Không dùng dự toán để tự cấp quyền lượt >1 giờ. Chỉ có thời gian chạy tiền kiểm cục bộ được lưu ở environment.json; không dùng nó ngoại suy toàn task.

Nguồn mới đề nghị: 37.102.637 byte nội dung và 422.197 byte metadata theo các response đã quan sát; tổng payload 37.524.834 byte. HTTP/TLS, retry và thay đổi metadata làm byte mạng thật còn OPEN. Danh sách, nhóm, URL, revision, phần loại trừ và đường dẫn ghi ở `de-xuat-tai.json`; chưa có file nguồn mới được lưu.

Không dùng archive để lấy ứng dụng: giữ raw file, không tạo .git, không giải nén JAR ra đĩa. Nguồn thành công một lượt là 37.102.637 byte, cộng metadata. Tổng dự toán giữ ba lượt thu đầy đủ, ba lượt so (396 JSON, giả định 512 KiB/JSON) và 50 MiB cho fixture/trung gian/checkpoint/log là 372.621.350 byte. Đây là ngân sách CANDIDATE có điều kiện, không phải dung lượng đã đo hoặc trần cho mọi số lượt lỗi. Lượt bổ sung vẫn phải giữ và cập nhật tổng; không xóa để vừa dự toán. Chưa chạy đủ để biết cỡ JSON thật.

Peak RAM CANDIDATE 512 MiB nếu xử lý từng file/graph và chỉ đọc từng entry JAR trong bộ nhớ; chưa có pilot. Chưa biết kích thước entry giải nén hoặc phụ thuộc nguồn ngoài. Quan sát máy trong `runs/tien-kiem-001/capacity-observation.json` là dung lượng rỗi tại thời điểm đọc, không phải peak task hoặc phép đo độc quyền. Không dừng tiến trình khác hoặc đo hiệu năng khi T-037/T-038/công việc nặng khác có thể cùng chạy.

## Giới hạn kết quả và bước tiếp

Đạt phần khôi phục quyền, hash/pin, inventory graph đầu vào và lập đề xuất nguồn. Chưa đạt các tiêu chí đầu ra khảo sát/graph/mapping/phân tích của SPEC. Chưa đóng P5b, RQ3/RQ5 hoặc G3.

Minh quyết phạm vi tách, tải cụ thể và cách xử lý mô tả loại object trong registry chung. Trong lúc chờ, phần độc lập từ nguồn cũ đã làm: kiểm toàn input, xác định graph hiện hành, đọc API/đoạn code analysis liên quan, ghi lineage còn thiếu và dự toán. Không còn phần lập bản ghi quan hệ ứng dụng nào có thể hoàn tất trung thực chỉ bằng nguồn hiện có.

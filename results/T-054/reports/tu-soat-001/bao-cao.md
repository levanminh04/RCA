# T-054 — Tự soát từ nguồn và triển khai công cụ

Ngày 05/11/2026. Codex là người làm; Claude giữ vai trò phản biện chính thức. Đây là tự soát của phiên mới, không phải một REVIEW thay Claude. Nguồn quyền mới được giữ nguyên tại `runs/trien-khai-001/quyen-minh.txt`.

## 1. Nhận xét từ nguồn

**Giới hạn thứ tự đọc.** Lệnh đầu đọc 48 dòng SPEC, rộng hơn phần hành chính, đã lộ mục tiêu và bảng câu hỏi. Vì vậy không nhận lượt này là soát mù hoàn toàn. Năm nhận xét riêng đã ghi trong chat trước khi đọc toàn SPEC và phần kết luận phản biện cũ. LOG giữ cả diễn biến và đính chính này.

1. **Yêu cầu nguồn.** DT18-NV2/NV3 và MRP RQ3/P7 cần phương pháp thực sự dùng quan hệ, đánh giá trên dữ liệu chưa dùng chọn thiết kế, đối chứng tương ứng và phân tích theo điều kiện. Q-245 hoãn (b). P7(a) trả lời phần xếp hạng và can thiệp tính toán; chưa trả lời phát hiện hệ thống, độ đúng vùng ảnh hưởng, LLM hoặc hiệu quả FlashTicket. MRP RQ3d/D23 không cho suy lợi ích topology thật hay thắng một phương pháp không quan hệ được chọn độc lập.
2. **Bằng chứng hiện có.** P4 chỉ ra những bước cụ thể gán thông tin chờ vào owner, ghép coverage/weight và bất cân xứng đơn vị. Cũng có ca đúng cùng cơ chế và tác động ngược khi đổi cách tính. T13 giữ kết quả khác dấu giữa TT và OB, các ca E2 đổi khóa, E1 phụ thuộc nền và C-d2 thắng. Đây là bằng chứng tính toán, chưa phân biệt vị trí tiêm, tải, mạng và mất quan sát ở mức vật lý. Nguồn: T-041 §5/§8; T-040 `ban-giao-p6.md`; T-052 `phan-tich-bo-sung-002.json#/mechanisms`, `bao-cao-t13-002.md` và hồ sơ 004.
3. **Tái dùng.** Đã kiểm 576 đầu ra ổn định T-052, 297 mục T-050, 2654 đầu ra T-053 và 93 pin code. Các pin LOG/STATE T-052 là lịch sử, không khôi phục trạng thái cũ. Tái dùng đòi đúng member, window, config, seed, variant và môi trường; hạng khớp chưa chứng minh vùng/coverage hoặc provenance khớp.
4. **Phần có thể làm sai đánh giá.** `p7_a4_v3.evaluate_sealed` gọi `label_reader` mà chưa đối chiếu nhãn G1 độc lập. `_check_record` kiểm trường ngoài nhưng chưa nối normalized input với payload. `_check_failure` cho biên nhận tự gán pha method khi worker phase chưa rõ. `p7_entry_v2` mới bao một lát cắt; `_ket_thuc` của P3 dùng variant `native` cho SimpleRCA timeout. Những điểm này chặn khóa/chấm bản ứng viên, không phải lý do dừng cài wrapper.
5. **Việc tối thiểu.** Trước khóa: hoàn thiện ba liên kết, đủ tuyến/variant, chứng cứ pha, dev parity và chính sách/nguồn/ngân sách. Sau grant: chạy đúng byte bản khóa, bảo toàn kết quả đầu, seal trước ghép nhãn; không sửa thiết kế theo điểm rồi gọi độc lập. RE3 có grant riêng cho bản cuối.

## 2. Đối chiếu SPEC và các ý kiến cũ

Không tìm thấy lỗi nghiêm trọng mới chặn **cài công cụ**. Chưa có bằng chứng để gỡ A/B1/B2/C ở mức G3. SPEC đã giữ đúng các giới hạn và quyền riêng. Không sửa SPEC hoặc thiết kế khoa học.

| Ý kiến | Kiểm riêng và kết luận | Trạng thái hiện tại |
|---|---|---|
| F1 — OB/file chung/cloud | Schema locator và bộ đọc cho thấy metric theo ngày; preflight T-053 ghi bản sao lịch sử. Không có bằng chứng phiên này về hiện trạng máy hoặc đã đọc giá trị test. | Đúng về rủi ro và khai tiếp xúc; SPEC cho OB local. Không gọi là vi phạm cũ. |
| F2, N1 — mở nhãn sớm | A4 cũ có gate hai bộ nhưng các bảng ngoài có thể lộ cùng thông tin. Một seed BLOCKED vẫn cho xem bảng khác sẽ làm mất kết quả chính sạch nếu sửa sau đó. | Đúng; SPEC bước 11 đã chặn mọi bảng khi A4 BLOCKED/PENDING. Fixture mới kiểm gate chung trước reader nhãn. |
| F3, N2 — parity | Đếm lại seal và command đã pin: TT thật có cả EC2 và laptop; TT C-e và OB cũng hỗn hợp. T-050 cần cho C-c/C-g. | Đúng sau đính chính; không nhận toàn TT đến từ EC2. Pilot chưa chạy nên chưa có parity thật. |
| F4 — cạn ngân sách | P3 §8.3 và phương án đề nghị P7 khác cách xử lý lượt chưa chạy. Đây là lựa chọn mẫu số/diễn giải, không phải lỗi câu chữ. | OPEN trước khóa; chưa tự chọn phương án. |
| F5 — vị trí N | C-a0 có `G_N` và `don_vi_phan_vi`; code vị trí dùng node N/alias và p75/p90. Đối chiếu cũ chỉ trong miền pilot đã lưu. | Có thể tái dùng có điều kiện, không thêm 94 K-R0 mặc định. Thiếu trường phải báo riêng. |
| F6, N3 — timeout/sleep | Wall deadline không tự phân biệt máy tạm dừng và lỗi phương pháp. Khoảng hở monitor cũng không tự xác nhận sleep. | Nguy cơ chưa kiểm trên máy thật. Fixture buộc có method-start và gap nhỏ hơn ngưỡng; ngưỡng khoa học chưa chốt. |
| F7 — reboot | Worker độc lập controller không đồng nghĩa tự khởi lại sau reboot. | Giữ resume thủ công, không tạo Scheduled Task. Đã diễn tập kill controller/adopt worker bằng dữ liệu giả. |
| F8 — byte/EOL | Cây có thay đổi ngoài HEAD và biểu diễn EOL khác nhau. Một checkout khác không chứng minh cùng byte. | Gói công cụ giữ đúng byte và blob từ byte đó; chưa phải khóa G3 hoặc một môi trường độc lập đã kiểm. |
| F9 — TORAI A | Q-74 yêu cầu A/B; vắng A trong bảng tổng hợp không hủy quyết định. Đường nguồn A nằm ngoài locked không cấp quyền đọc. | OPEN; không đọc nguồn A và không loại A. |
| F10 — root ngoài U | Đếm metadata G1: cả hai cohort test hiện hành không có root ngoài U. | Dừng đối chiếu nguồn khi gặp root ngoài U; không tự mở U hoặc gán 0. Không suy sang RE3. |
| F11 — prompt | Mẫu trung tính không thay đánh giá bằng chứng; các bản chat cũ là nguồn, không là REVIEW mới. | Không thấy tác động cụ thể mới. Đã khai giới hạn thứ tự đọc của chính phiên này. |
| N4 — identity EC2 | IP/HostKeyAlias lịch sử không chứng minh máy hiện tại. | Chưa SSH; giữ bước kiểm identity/host key khi có quyền. |
| N5/lịch ba máy | Cache Linux không thay kiểm trên laptop. Cloud chỉ hữu ích nếu phủ nhánh cần thiết hoặc phân xử lệch môi trường với tổng chi phí thấp hơn. | Pilot-plan là ứng viên; chưa gán lô để giữ máy bận. ETA/bundle và hạn sáng chưa có số đo đủ. |

## 3. Đã triển khai và kiểm

Chín script trong `scripts/` tạo CLI, liên kết nguồn/nhãn độc lập, biên nhận tại API, pha bền, queue một partition, worker tách phiên, baseline/M1/TORAI hai tầng, C-d3 riêng và bộ chấm. Code cũ/src không bị sửa. Công cụ không tự nâng quyền hoặc chốt các chính sách còn OPEN.

- `fixtures-004/summary.json`: 83 kiểm đạt. Có tuyến đọc/cắt và lõi M1 thật trên parquet/CSV tự sinh cho bảy cấu hình, hai schema; SimpleRCA M4 trên hai schema. Đây không phải pilot dataset thật.
- `fixtures-005/summary.json`: 54 kiểm đạt, thêm kill controller/adopt worker và không nhân đôi attempt/method. `fixtures-009/summary.json`: 60 kiểm đạt, thêm worker C-d3 với DAG/chu trình/thiếu đích, main seal giữ nguyên. Không cộng các lượt trùng thành số kiểm độc lập.
- `fixtures-008/summary.json`: đi qua verify snapshot → nhãn độc lập → A4 → bảng. Có 28 slot tổng hợp, 89 dòng độ đo, bốn dòng vùng và hai dòng vị trí N. Baseline ngoài SimpleRCA ở phép kiểm này là bản ghi tổng hợp, không nhận đã chạy baseline thật. Variant CIRCA chính/phụ và seed TORAI được tách, không bình quân hai variant hoặc coi ba seed là ba ca.
- Chạy thêm semantic verifier trên 16 output reader/lõi của fixtures-004; kiểm method/variant/seed/config/khối hạng đạt. AST của chín script hợp lệ.
- Ma trận dựng từ kế hoạch G1 đã pin: 1342 slot main; 1274 core call sau bỏ slot OB không hỗ trợ; 60 worker C-d3 TT; tối đa 60 C-e. Đây là số đếm công việc, không phải runtime/ETA hoặc số phương pháp đã chạy.
- `runs/freeze-cong-cu-003/`: gói cuối của checkpoint gồm 107 file code/metadata giữ đúng byte, không telemetry/nhãn riêng. Gói là checkpoint công cụ; `runnable_for_test=false`, không phải G3. Các bản trước được giữ; bản cuối bổ sung chuyển kiểu số NumPy theo hợp đồng ghi của P3, đã kiểm riêng.
- `runs/trien-khai-001/cli-checks-002.json`: status/drain/resume/verify qua CLI đạt; sau resume vẫn đúng một attempt. Bản CLI đầu hỏng do stdout Windows cp1252; đã cấu hình UTF-8 trong CLI, giữ biên nhận lỗi 001.

Giữ mọi lượt hỏng. `fixtures-002`: thiếu đường thư viện drain3. `fixtures-003`: epoch giả quá nhỏ so hợp đồng SimpleRCA; bộ sinh đã đổi sang epoch giây hợp lệ, không nới kiểm phương pháp. `fixtures-006/007`: lỗi chuyển biểu diễn khối hạng và cạnh trong wrapper báo cáo; đã sửa trong T-054, kiểm lại ở fixtures-008. Không sửa code/source lịch sử để làm phép kiểm qua.

## 4. Phần còn thiếu và quyết định phụ thuộc

**Task chưa hoàn thành pha 1, chưa khóa G3 và chưa có kết quả P7.** Công cụ đã có các đường và phản ví dụ kiểm được bằng dữ liệu giả. Còn cần ghim plan thực, map nguồn độc lập, môi trường từng pha, chạy pilot dev đủ nhánh và đối chiếu nguồn native, đo throughput/cold/cache/chi phí toàn tuyến. Những phần này không được đổi thành PASS từ việc fixture qua.

Các kết cục ERROR/TIMEOUT thật vẫn BLOCKED khi chưa có phân loại và chính sách đã duyệt; chưa xuất trượt khoa học. Chưa có kiểm byte-cache TORAI trên laptop, ba seed TORAI trên driver mới, parity thật, current EC2 identity, SSH/sync hoặc số đo đủ để chốt worker/budget/hạn sáng. Không dùng gói code thay môi trường và không dùng các số runtime cũ làm ETA.

Minh cần chốt đúng phần phụ thuộc: ngoại lệ cạn ngân sách; giữ/bỏ TORAI A và quyền nguồn nếu giữ; người cấp map/nhãn và quyền materialize; công thức độ nhạy; ngân sách/quyền pilot và máy; timeout/maxgap sau số đo; cuối cùng G3 và grant test riêng. Hai lựa chọn đầu đã được hỏi trong chat, chưa có câu trả lời tại lúc soạn hồ sơ. Không ghi OPEN thành DECIDED.

Về nghiên cứu: dev cho phép mô tả tác dụng tính toán có điều kiện; hiệu quả độc lập RQ3b/d vẫn đợi đánh giá. RQ3a, nhãn vùng độc lập, LLM/FlashTicket và các giải thích vật lý còn mở. Không đề nghị nghiệm thu task hoặc đóng câu hỏi nghiên cứu.

# Ngoại lệ phát lại MicroRank — MINH DUYỆT 10/10/2026 / CHƯA CHẠY COHORT

Minh đã duyệt phương án EC2 theo đúng đề xuất này ngày 10/10/2026, gồm quyền ghi một quyết định mới. Ngoại lệ chỉ áp cho MicroRank của T-032, không áp CIRCA hay phương pháp khác. SPEC giữ nguyên file; đây là ngoại lệ được Minh duyệt, không đổi thuật toán. Quyền A′ vẫn chỉ có hiệu lực khi lõi đạt đủ điều kiện SPEC.

Bổ sung theo lời duyệt: bảng 52 ca ghi mức lệch lớn nhất từng ca (khoảng cách ULP biểu diễn và tương đối), để thấy khoảng cách tới ngưỡng. Ca vượt ngưỡng dừng và trình Minh, không tăng ngưỡng. Đoạn WHY của ngoại lệ phải được Minh duyệt trước khi dùng kết quả MicroRank trong báo cáo.

## Bằng chứng và giới hạn

Lượt native không gắn bộ ghi trên EC2 khớp tuyệt đối với lượt có bộ ghi của cùng ca RE2 dev-12a1a88069. So với bản đóng băng có 157 trường số và bốn trường thứ tự khác. Sai số tuyệt đối lớn nhất khoảng 2,56e-13; hai operation cùng service đổi chỗ ở vị trí 90–91. Nguồn: `runs/tiep-tuc-003/microrank-numeric-audit.json`, các con trỏ `/native_observed_exact`, `/float_exact_count`, `/other_difference_count`, `/max_absolute`; danh sách khác biệt ở `runs/tiep-tuc-003/microrank-native-diagnostic-check.json#/native_vs_frozen/differences`. Hash hai đầu đã kiểm. Số ULP trong audit hiện là |delta|/ulp(expected), chưa phải khoảng cách biểu diễn binary64 chính xác.

Điều này loại được bộ ghi là nguồn gây khác đầu ra trong lượt này. Chưa xác định thành phần môi trường gây sai lệch; chưa chứng minh các ca khác tương đương. Bản đóng băng không có toàn mask/partition lịch sử: counts bằng nhau không chứng minh membership lịch sử bằng nhau. Ngoại lệ dưới đây chỉ xác nhận hợp đồng đầu ra chấm tương đương và trung gian mới tự nhất quán; không biến nguyên nhân drift hoặc cơ chế vật lý thành FACT.

## Tiêu chí ứng viên khai trước đủ 52 ca

1. Giữ nguyên code/revision, cấu hình, input hash, cửa sổ F, detector/SLO, hashseed và dữ liệu gốc. Không đổi tham số hay ép điểm gần nhau thành hòa. Không tolerance ngoài whitelist score operation và score service.
2. Ghép điểm theo operation ID và mapping operation→service thật, không ghép theo vị trí ranking. ID/mapping, tập operation/service, tập quan sát/trả về, mọi counts và metadata phải exact. Các trường record ngoài whitelist vẫn exact như trước.
3. Với hai điểm float64 hữu hạn cùng dấu, khác zero: chấp nhận khi **đồng thời** khoảng cách biểu diễn binary64 ≤16 ULP và `abs(a-b)/max(abs(a),abs(b)) ≤16×2^-52` (khoảng 3,553e-15). ULP được đếm bằng biểu diễn bit có thứ tự, không chia delta cho ulp(expected). Zero, dấu zero, dấu số và trạng thái không hữu hạn giữ exact. Không có absolute floor làm rộng ngưỡng cho điểm sát zero.
4. Lý do chọn 16: cho phép một số hữu hạn bước làm tròn binary64, chặn thay đổi thang điểm tương đối và điểm gần zero bằng hai ràng buộc. Đây là **ngưỡng kiểm kỹ thuật ứng viên**, chưa là chứng minh sai số lý thuyết của PageRank/DStar2. Nó được đề xuất sau khi đã thấy pilot; không gọi là phép kiểm độc lập của nguyên nhân drift. Nếu Minh duyệt, khóa ngưỡng trước 52 ca; không tăng ngưỡng để ca mới qua kiểm.
5. Thứ tự service, mọi quan hệ trước/sau service và **partition nhóm hòa service theo exact key gốc** phải khớp tuyệt đối. Chấm lại bằng code cũ toàn Hit@1..10 và cờ T-028 ở k=1/5: M1–M6, primary/M0, wrong_OK, P0, N/A/reason; tất cả phải exact. Nhãn chỉ nối ở bước đánh giá sau tính phương pháp. Không đưa feature/nhãn vào MicroRank.
6. Đổi chỗ operation chỉ chấp nhận các inversion trong cùng service, hai điểm gần nhau theo chính ngưỡng trên **ở cả bản nguồn lẫn bản phát lại**. Không chấp nhận đảo giữa service, thêm/bớt operation hoặc sửa ranking để khớp. Kiểm lại max-service bằng đúng `ban_ghi.xep_thuc_the` cho từng output; đổi thứ tự không được đổi giá trị tổng hợp của cùng output. Điểm service giữa hai output chỉ được lệch theo whitelist float đã nêu; hạng/hòa/chấm vẫn exact. Lưu cả operation đạt max và thay đổi representative nếu có.
7. Mọi lượt native–observed dùng để kiểm bộ ghi phải exact, kể cả điểm và thứ tự. Tolerance chỉ ở so EC2–frozen, không che tác dụng của bộ ghi.

Nguồn công thức cần tiếp tục giữ: `src/microrank/__init__.py` (mapping, flags/groups), `src/microrank/official.py` (PageRank/spectrum), `src/p3/adapters/microrank.py`, `src/p3/ban_ghi.py` (max/hòa), `src/p3/danh_gia.py`, `results/T-028/codebook.md` và script codebook đã khóa. Manifest tương ứng phải được kiểm trước mọi lần dùng.

## Lượt chạy và bảng phải trả về sau duyệt

- 30 ca RE2 + 22 ca Nezha, giữ mọi ERROR/NO_EVIDENCE và mọi lượt hỏng. Không chỉ chạy ca đã qua pilot; không chọn theo tăng hạng root.
- Mỗi dataset có bảng tất cả 52 ca với một loại chính: `exact`, `numeric_only`, `operation_order`, `service_order_changed`, `blocked`/`not_run`. Operation order ghi thêm số lệch numeric. Status/hòa/Hit/cờ M thay đổi là blocked có reason riêng. Báo đầy đủ mẫu số và phần chưa chạy khi fail-stop; không giả có kết quả các ca còn lại.
- Có số riêng cho khớp hẳn, chỉ lệch số, đổi operation, đổi hạng service, vượt ngưỡng và thiếu kiểm. Đổi hạng service, hòa, chấm hoặc bất kỳ invariant quan trọng nào: dừng MicroRank/A′ ngay, không chạy tiếp dựa trên ca sai. Phần độc lập của T-032 vẫn tiếp.
- Triển khai comparator/fixture trong lượt mới ở `results/T-032/scripts/` và `runs/`; giữ comparator exact và lượt cũ. Trước cohort, benchmark pilot mới cho native/capture/comparator, RAM/dung lượng và dự toán đủ phần còn lại. Mọi chạy dài có supervisor fail-stop, status/progress/PID/stdout/stderr.
- A′ chỉ được xét sau toàn điều kiện lõi/khóa mẫu của SPEC và ngoại lệ được Minh duyệt đạt; duyệt comparator không tự coi lõi đã đủ.

## Hai phương án và chi phí

| Phương án | Chi phí có bằng chứng | Phần chưa đo và hệ quả |
|---|---|---|
| EC2, comparator hẹp ở trên | Ca RE2 pilot nguồn laptop wall 6,594 s; native EC2 cùng ca 5,257 s. Nezha nguồn main22 tổng 128,148 s, mỗi ca 3,894–7,669 s, RSS đỉnh 346,9 MiB | Chưa có full52/capture benchmark; không nhân pilot thành dự toán chính thức hoặc nhận speedup. Đề xuất checkpoint benchmark tối đa 10 phút, ≤150 MiB mới; sau đó dự toán trong ngân sách hiện hữu, vượt thì dừng/trình. Nền chạy độc lập laptop. Cần trả đầy đủ bảng 52 như trên. |
| Phát lại laptop ở môi trường nguồn, giữ exact | Nguồn Nezha22 đo như trên; RE2 pilot nguồn 6,594 s. Không tốn giờ EC2 cho bước này | Không bảo đảm exact chỉ vì cùng laptop; phải khóa Python 3.12.10/packages/threads và hash. Chưa đo capture toàn52, RAM còn trống hoặc ảnh hưởng ứng dụng khác. Cần Minh duyệt ngoại lệ điều khoản EC2-only của SPEC và phạm vi ghi laptop; laptop phải mở suốt lượt. Có thể giảm bất đồng khác nền tảng, nhưng chưa biết có giải quyết drift không. |

Nguồn chi phí: record frozen RE2 trong `results/T-031/runs/microrank-30-001/.../ban-ghi-0.json#/cost`, diagnostic check `/cost`, và `results/T-026/chi-phi.md` đã kiểm manifest. Các số trên là lượt cũ, không dự toán tính tiền hoặc cam kết thời gian full52. Chi phí EC2 theo tiền chưa có loại máy/đơn giá được xác minh; không tự đặt số tiền.

**Trạng thái:** Minh đã duyệt ngoại lệ MicroRank và benchmark trước cohort, cùng quyền nối một dòng quyết định mới. Chưa áp dụng comparator hoặc chạy cohort tại lúc cập nhật trạng thái này; WHY đang trình, chưa nối vào WHY chính thức. Giữ SPEC/Q-93; không thay ngoại lệ cho phương pháp khác. Phương án laptop vẫn là phương án thay thế, chưa có quyền thực hiện.

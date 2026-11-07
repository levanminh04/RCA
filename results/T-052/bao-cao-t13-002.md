# T13 dev và phần bổ sung sau phản biện T-052

Bảng hạng trên 52 ca thật giữ tại `ket-qua-dev.json#/worlds`, bảng độ đo bổ sung ở `do-do-bo-sung.json`. Đây là bản đính chính và mở rộng phân tích của báo cáo 001. Các bảng mới lấy từ seal 492 bản ghi và lưu ở `phan-tich-bo-sung-002.json`.

| Phép so MRR tại P | TT | OB |
|---|---:|---:|
| M1 | 0,927778 | 0,872727 |
| C-a0 | 0,983333 | 0,661883 |
| C-d2 | 0,916667 | 0,899242 |
| Baseline tham chiếu | TORAI B 0,916667 | SimpleRCA M4 0,537542 |
| C-d3 mô tả | 0 trên 30 ca, 4 OK, 6 NO_EVIDENCE, 20 UNSUPPORTED_CYCLIC | 22/22 NO_TARGET lịch sử, không có lượt C-d3 OB mới |

Thứ tự ghép nhãn được đính chính. Bảng baseline độc lập và bảng vùng dùng nhãn dev trên bản ghi đã seal ở task nguồn lúc 18:33 và 18:35. Seal chuẩn hóa riêng T-052 hoàn tất lúc 18:55, sau đó `score_all` mới đọc nhãn để chấm bản chuẩn hóa. Nguồn thời gian là `bang-doc-lap-summary.json`, `vung-ce-summary.json` và `prepared-seal.json` trong `runs/trien-khai-001`.

## Phân tích theo nhóm và phản ví dụ

Các số nhóm ở `phan-tich-bo-sung-002.json#/mechanisms/<dataset>/<vế>/groups`. Bảng ca chứa mọi ca khác RR, kênh root và đối thủ, tầng/khóa và mọi ca cùng root/fault có tác dụng ngược hoặc bằng 0. Đó là đối chiếu hậu kiểm. Cùng root/fault chưa giữ cố định topology, tải hay mức quan sát.

- **TT hại.** C-a0 hơn M1 chủ yếu ở `loss` (3 ca giảm, tổng ΔRR −1,667) và một ca `mem` (−0,5), có một ca `socket` tăng (+0,5). Bỏ riêng E2 chỉ đổi ở `loss` (2 ca, −1,167). Trong `dev-a915aa2424`, exclusive của travel giữ 3881,562205. E2-C đưa bằng chứng cạnh vào train, khóa 4834,194981, và order tăng 86,209133 → 4708,986842. Cả hai vượt travel cùng tầng nên RR 1 → 1/3. `dev-a5cabe5fa7` giữ RR 1 vì root còn vượt train. Frame T-053 `phan-tich-cap-003.json#/frames/K-E1+E5|dev-a915aa2424/new` và vế `K-E1+E2+E5` ghi đủ thứ tự. E5 ở `dev-20acb4402d` vẫn là chuỗi riêng trong báo cáo 001. Không có ca đúng trùng toàn bộ chữ ký cho chuỗi đó.
- **OB giúp.** `network_delay` chiếm 3,938576 của tổng ΔRR 4,638576 ở M1−C-a0, với 6 ca tăng. Bỏ E2 mất tổng 3,304171 trên 5 ca tăng cùng nhóm. Trong `dev-607751ac0a`, chỉ kênh `frontend→checkoutservice` còn bằng chứng tự sinh ở root, điểm 165,081376. M1 đưa checkout lên đầu, còn bỏ E2 đưa vào nhóm hòa cuối. Ca cùng root/fault `dev-2bfc97b01e` giữ hạng 1 cả hai vế, còn khóa 9,105469 khi bỏ E2. Trong sáu ca OB đổi RR khi bỏ E2, 5/6 chỉ có kênh E2 trong danh sách đã lưu và 6/6 chỉ có E2 khi lọc `F_I=1`. Quy tắc C có thể trùng vị trí tiêm ở nhóm này. Để phân biệt hướng gán vật lý với kiểu tiêm hoặc thiếu tín hiệu, cần quan sát hai đầu cạnh và căn cứ điểm tiêm độc lập, chưa có trong phép so.
- **E1 phụ thuộc nền.** Ở `dev-bcbd4f46ae` (TT `socket`), phần kênh operation `RouteRepository.findById` giữ khóa route 890,161905. Khi bỏ E1, khóa root còn 465,855814, thấp hơn auth 510,497914 cùng tầng. Ca `dev-03d4910932` cùng root/fault giữ khóa max 1372,881545 và hạng 1 ở hai vế. Khi E2/E5 đều tắt, C-a1−C-a0 bằng 0 trên TT và −0,030716 trên OB. Đây là kết quả theo hai nền, chưa đủ phân xử mọi tương tác.
- **C-d2 thắng ở OB.** Với `dev-63c30faf34`, M1 đặt adservice trên recommendationservice ở cùng tầng do khóa 1289,898734 so với 620,283120. C-d2 ưu tiên khởi phát phân vị sớm hơn, đưa recommendationservice lên đầu. Cặp cùng root/fault `dev-5467884de4` giữ hạng 1 cả hai cách. C-d2 dùng chính bằng chứng của chuỗi, gồm E2 trong các ca này. So sánh nói về quy tắc ưu tiên, không chứng minh onset vật lý. Xem `#/mechanisms/Nezha-OB/C-d2/cases` và `src/m1/doi_chung.py`.
- **Vùng đổi.** T, ánh xạ vùng theo thực thể đầu hoặc hợp vùng thay đổi ở 23 ca TT và 0 ca OB khi bật T12. Ví dụ `dev-03d4910932` giữ T={route}. Hợp cách 2 tăng từ 16 lên 25, thêm cả admin-route. Snapshot bổ sung cạnh admin-route→route, đồng thời `F_I` của latency-90 auth đổi 1→0. Đường duyệt vùng sử dụng đồ thị sau hợp cạnh và lớp bất thường. Dữ kiện chưa cô lập toàn bộ chín nút tăng do cạnh trực tiếp hay do cờ đổi. Nguồn `#/T12_region_changes/dev-03d4910932` và `results/T-051/t12-001/33.json#/worlds/P`. T12 giữ RR root trên 52 ca. Độ đúng vùng ảnh hưởng thật vẫn cần nhãn độc lập.

Theo vị trí N p75, toàn bộ chênh âm TT khi giữ E2 nằm ở nhóm hub (tổng ΔRR −1,167). OB được lợi ở nhóm giữa, hub và lá khi giữ E2, với tổng ΔRR lần lượt +0,996, +0,859 và +1,493. M1−C-d2 ở OB âm ở nhóm giữa (−1,300) và dương ở hub (+0,717). Nguồn là `/groups/position_N_p75` của từng vế. P90 nằm ở `ket-qua-dev.json#/worlds/P/<dataset>/groups/N_position_p90`. Các nhóm chồng với loại lỗi, nên bảng không tách được riêng tác động của vị trí.

Hạn chế quan sát (vắng trace, đầu quan hệ) cần tách khỏi tác động phép tính (khóa max, ưu tiên onset, duyệt cạnh). Để phân xử phần vật lý cần dữ liệu có vị trí tiêm, quan sát hai đầu/clock, nhãn vùng độc lập và điều kiện tải tương ứng. Đề xuất thu thuộc phần FlashTicket P9/P10. Chưa có dự toán thu hay quyền chạy thêm. Thiếu đó giới hạn kết luận vật lý và độ đúng vùng, trong khi bảng mô tả và các chuỗi tính toán trên vẫn dùng được.

## C-e trên cửa sổ giả

Mỗi vế có 30 cửa sổ TT. Cả năm cặp với M1 có 30 hợp lệ và 0 bị loại theo trạng thái phương pháp. Nguồn `phan-tich-bo-sung-002.json#/C_e` có xác suất đứng đầu từng thực thể, hòa, V0, N1, O/U, tập trả về, RR root tương lai và hai mốc chance.

| Vế | N1 trung bình | V0 CAUSE_FOUND | Số thực thể từng đứng đầu | Tổng xác suất của hai thực thể đầu qua 30 cửa sổ |
|---|---:|---:|---:|---:|
| M1 | 14,70 | 30/30 | 16 | 10 |
| Bỏ E1 | 14,27 | 30/30 | 22 | 5 |
| Bỏ E2 | 14,63 | 30/30 | 16 | 10 |
| Bỏ E5 | 16,63 | 30/30 | 16 | 10 |
| C-a0 | 16,90 | 30/30 | 18 | 10 |
| C-a1 | 16,57 | 30/30 | 16 | 10 |

Trên nền còn E2/E5, giữ E1 đi cùng mức tập trung hạng đầu cao hơn. Giữ E5 giảm N1 khoảng 1,93 so với bỏ E5. Đây là cửa sổ trước tiêm, chưa xác nhận nền khỏe. Các chênh này chưa hiệu chuẩn V0 hoặc đo báo động sai.

T13 đủ căn cứ mô tả kết quả dev và giới hạn của đối chứng. Kết quả vẫn trái chiều giữa TT và OB. Chưa xác nhận hiệu quả độc lập hoặc tác dụng của topology thật. Điểm vào P7 v2 và A4 đã có kiểm giả, còn F3 cần quyền chạy lát cắt dev. Đọc điều kiện khóa tại [hồ sơ G3 bản 002](ho-so-g3-002.md).

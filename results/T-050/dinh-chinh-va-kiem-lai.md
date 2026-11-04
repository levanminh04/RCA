# T-050 — Đính chính sau phản biện

Bản này đính chính cách đọc [báo cáo T-050](bao-cao.md) sau khi đối chiếu lượt đầu và lượt chạy lại. Kết quả theo luật vẫn là **HẠI** cho E6b đã thử. Hành động theo SPEC là đề xuất **giữ E6a+S1 và tắt E6b** trên nền dev hiện hành. Nghiệm thu T-050 và lựa chọn nền T-051 do Minh quyết.

## Phạm vi của kết luận T9

T9 so E6a+S1 với đúng E6b trong T-043 B2 trên nền z hiện hành và dev chế độ (a). E6b dùng PageRank cá nhân hóa để chuyển khối lượng trên đồ thị con dịch vụ bất thường theo chiều **bên gọi → bên được gọi**. Trọng số đích và phân bố khởi tạo lấy từ K_I.max. Trong mã MicroRCA ở revision đã đối chiếu, cạnh gọi được đảo trước PageRank. MicroRCA dùng cả nút host, trọng số cạnh theo cờ bất thường hoặc tương quan và cách cá nhân hóa theo tương quan tài nguyên. Căn cứ MicroRCA trong T-043 là ý tưởng dùng PageRank cá nhân hóa để xếp hạng trên đồ thị con bất thường. [T-043 B2](../../tasks/T-043-thiet-ke-rca-m1/SPEC.md#b2-đặc-tả-thành-phần) · [Mã nguồn MicroRCA tại revision đã kiểm](https://github.com/elastisys/MicroRCA/blob/de334b2815742a248225cf6e242840a9d5fedc9a/MicroRCA.py)

Kết cục HẠI chỉ áp dụng cho cặp đã thử. Hiệu quả của MicroRCA và của biến thể E6b đảo cạnh còn mở. Phép phân xử hướng cạnh sẽ cần giữ nguyên đầu vào, điểm, nút, trọng số và khóa, rồi chỉ đổi chiều cạnh trên cùng dev. Nếu Minh chọn thử, đây là ứng viên thăm dò đặt ra sau khi đã xem kết quả dev và cần SPEC riêng. Lợi ích trên dữ liệu độc lập vẫn cần đánh giá riêng. [MRP §2.3 và P6](../../docs/MRP.md) · [WHY-74](../../docs/WHY.md#why-74-hành-động-t9-khi-e6b-không-tác-dụng--đã-quyết-trước-pha-1-q-240)

## Căn cứ của bước 3

Thay câu giải thích bước 3 ở phần kết quả T9 bằng câu sau.

> Ở cả ba thế giới, bước 3 trả HẠI vì ΔMRR gộp = −1/30, thấp hơn ngưỡng −δ = −0,01.

ΔMRR theo dataset là −13/225 ở RE2-TT và 0 ở Nezha-OB. Ngưỡng riêng theo dataset được dùng ở bước 2 và trong điều kiện bước 5. [Luật C](../../src/m1_danh_gia/luat_c.py) · [Kết quả lượt đầu](cham-001/luat.json) và [lượt chạy lại](cham-002/luat.json), cùng con trỏ `/theo_the_gioi/*/{buoc,dMRR,delta_d,ket_cuc}`.

## Cơ chế quan sát được

Trong ba cửa sổ `loss` 05, 13 và 21, dịch vụ gốc có điểm tự sinh dương. Bước chuyển trên cạnh hiện hành làm khối lượng ròng đi ra khỏi root. Khi dùng π làm phần đầu khóa, các nút khác vượt root và làm RR giảm. Giữ khối lượng khởi tạo v thay cho π, với K_I và K_raw giữ nguyên, đưa RR của cả ba ca về bằng E6a+S1. Ví dụ ở cửa sổ 13, khối lượng chuyển ra ngoài root khoảng 0,04007 mỗi bước tại π, còn chuyển vào khoảng 0,01070. [Vết phân rã RR](cham-002/co-che.json), `/*/comparisons/P`. Đọc `/P/mass` và `/P/E6b` trong bản ghi được trường `replay` trỏ tới.

Phép đếm trên 52 ca thật ở P xác nhận π của root giảm ở 13/14 ca có cạnh đi tới nút khối lượng dương. Ca còn lại có v của root bằng 0. Ở 18 ca root chỉ có cạnh vào từ nút dương, π của root đều tăng. Đây là mô tả về điểm, còn thay đổi hạng phụ thuộc vị trí tương đối của các ứng viên. Cửa sổ 03 và 55 đều giữ RR = 1/2 dù π của root giảm. Phát biểu cơ chế làm giảm RR ở trên áp dụng cho ba ca `loss` đã lần vết. [Bản ghi theo cửa sổ](pha1-002/sidecars.json), dùng các trường `index`, `input` và `replay`. [RR theo ca](cham-002/co-che.json), `/*/comparisons/P/rr`.

Ở các cửa sổ `disk` 23, 49 và 51, v của cùng root tập trung cao và E6b giữ hạng nhất dù có chuyển ròng ra ngoài. Trong C-g với phiếu SimpleRCA, RR ba ca từ 1 lần lượt xuống 1/3, 1/3 và 1/4. Trên đủ 52 ca, C-g giảm RR ở 16 ca, tăng ở 7 và giữ nguyên ở 29. C-g cho thấy giảm RR cũng xảy ra khi đặt bước lan truyền sau SimpleRCA. Hai nhánh khác nhau về nguồn điểm, tập nút và khóa, nên chênh lệch giữa chúng chưa cô lập tác động của phân bố khởi tạo hay chiều cạnh. [Phiếu và nhóm hạng gốc](doi-chung-003.json), `/rows/*/simple_groups`. [Chấm C-g](cham-002/cham.json), `/cau_hinh/C-g/ca/*/theo_the_gioi/P/RR`.

T-043 đã dự báo dạng thất bại này trong §7.8 mục 8. Nút nhận trên cạnh có thể tích lũy khối lượng và vượt nút gửi dù điểm đầu nhỏ hơn. Ví dụ đặc tả A(0,8) → R(0,6) cho π(R) = 5/6. T-050 quan sát dạng phân bổ này ở ba ca `loss`, với cạnh theo hướng gọi đã đặc tả. Độ sâu của các nút nhận chưa được kiểm. [Điều kiện thất bại trong đặc tả T-043](../T-043/dac-ta-phuong-phap-v1.md#78-e6b--pagerank-cá-nhân-hóa-trên-đồ-thị-con-bất-thường)

## Bằng chứng từ lượt chạy lại

Phiên 4 đã khóa và chấm một lượt mới. Đủ 82 cửa sổ phát lại khớp lượt đầu, gồm luật T9, vùng T10 và đối chứng C-c/C-g. Kết quả này cho thấy phép phát lại tái lập được trên đầu vào đã ghim. Kiểm trực tiếp từ log, trace và metric gốc dùng cả hai vế ở ba ca đổi kết cục, được chọn sau chấm. Trên máy tạo dấu vết nguồn của từng ca, 18 giá trị RR qua ba thế giới và các khóa, nhóm hòa đều khớp. Ở phép đối chiếu chéo máy của cửa sổ 05, sai khác khóa S1 tối đa 5,55 × 10⁻¹⁷ và nhóm hòa vẫn khớp. [Manifest Phiên 4](manifest-chay-lai-002.json) · [Đối chiếu hai lượt](kiem-chay-lai-002.json) · [Kiểm từ dữ liệu gốc](kiem-native-quyet-dinh-002.json)

T10 mô tả độ chứa root và độ rộng vùng nghi ngờ trên dev. Độ chính xác của vùng ảnh hưởng còn thiếu nhãn để đánh giá. G3 và test vẫn khóa.

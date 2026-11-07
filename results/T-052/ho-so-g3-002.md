# Hồ sơ G3(a) sau phản biện T-052

Ứng viên để Claude kiểm bản sửa. Dùng cùng [hồ sơ 001](ho-so-g3.md), [phân tích T13 bổ sung](bao-cao-t13-002.md) và [giao thức 002](giao-thuc-p7-a-002.json). Giao thức 002 là bản hiện hành để soát. Nội dung khóa vẫn cần Minh quyết.

| Câu cổng | Căn cứ và giới hạn |
|---|---|
| Mục tiêu | DT18-NV2/NV3 và hướng dẫn cô về quan hệ, so baseline và phân tích trường hợp tốt/xấu. RQ3b/d trên dev; RQ3c mô tả vùng nghi ngờ. RQ3a/(b), độ đúng vùng và áp dụng FlashTicket ở phạm vi đã ghi trong MRP/Q-245. |
| Dữ liệu phân xử | Can thiệp tính toán và đánh đổi theo bộ/ô/ca có quan sát. Tín hiệu thiếu, nhãn vật lý, topology thật và dữ liệu độc lập còn giới hạn. C-e chưa xác nhận nền lành. |
| Baseline | Sáu tuyến đã có số dev, M4 OB giữ giới hạn T-042. T13 có C-a0/a1 và C-d2 cạnh tranh. Pilot tuyến P7 v2 qua ca dev thật vẫn cần thực hiện. |
| Trung gian | 15 đối chiếu native và phân tích hai chiều từ bản ghi đã seal. Bản 002 nối đầu vào/kênh, khóa, hạng và phản ví dụ. Vẫn còn thiếu phép quan sát để quy cơ chế vật lý. |
| Điều kiện và ca | Có bảng fault/vị trí N/ô/ca, paired C-e và vùng đổi. S_lo/S_hi là độ nhạy. Giữ kết quả trái chiều TT/OB. |
| Lý do thiết kế | Bảng dưới tách căn cứ nguồn, yêu cầu đề tài, nhu cầu kỹ thuật và luật chọn dev. |

Nút dùng để chấm là thực thể dịch vụ hoặc thành phần sau chuẩn hóa alias. Trace giữ span theo request và operation để lấy quan hệ cha–con, owner, thời lượng và mốc N/A. Cạnh gọi nối bên gọi với bên được gọi. Log lỗi và metric tài nguyên gắn vào owner theo nguồn. E1 lấy phần khoảng thời gian của span cha ngoài hợp các khoảng con quan sát được. E2-C dùng khoảng còn lại giữa span bọc phía gọi và span phía nhận đủ điều kiện để tạo kênh trên cạnh, rồi gán bằng chứng cho bên được gọi theo luật C. E5 dùng chiều cạnh và thành phần liên thông mạnh để phân lớp kênh. E6a xếp tầng và khóa. E7 duyệt cạnh từ tập đứng đầu để mô tả vùng nghi ngờ. Hợp đồng nguồn nằm ở T-043 §D, §E và bảng B6. Graph gộp không thay cho index span/request.

| Thành phần | Loại căn cứ | Lý do và phương án đã xét | Bằng chứng và thất bại |
|---|---|---|---|
| Ánh xạ, alias, quan sát | DT18 + kỹ thuật + hạn chế dữ liệu | Đưa log/trace/metric về thực thể, giữ ngữ nghĩa nguồn, tách U và O. T-041 §3–4, G2-H16/H19, T-043 D12 và hợp đồng adapter. | Thiếu instrumentation, host binding, hoặc ngữ nghĩa hai đầu không khôi phục bằng alias. N/A và coverage chỉ có nghĩa theo cửa sổ đã khai. |
| E1-U | Ứng viên từ P4 + DT18, giữ theo luật dev | G2-H03/H06 và T-041 §5.2/§6.1 thấy thời gian chờ có thể được tính vào owner. T-043 Q1/E1 thử full và exclusive. WHY-72/76 là căn cứ chọn nền sau thử. | Bỏ E1 trên nền cuối làm TT giảm, OB bằng. C-a1−C-a0 khi E2/E5 tắt là 0 trên TT và −0,030716 trên OB. Lợi ích TT trên nền cuối tập trung ở bốn ca `loss` và một ca `socket`. Thiếu con, clock, bất đồng bộ và span bọc giới hạn cách đọc. |
| E2-C | Ứng viên từ P4 + dùng quan hệ theo DT18, giữ theo luật dev | G2-H06/T-041 cho thấy vị trí tín hiệu phía gọi có thể khác vị trí root. T-043 Q3/E2 và WHY-72/73 so C với VC. | E2 giúp một số `network_delay` OB và hại `loss` TT. Chưa xác định đầu lỗi vật lý, chưa phân xử VC×E5. |
| E5 | Ứng viên từ P4 + phép phân lớp dùng cạnh, giữ theo luật dev | G2-H17/T-041 §6.1 nêu cờ lan và thiếu chuẩn độc lập. T-043 Q8/E5 phân lớp bằng cạnh/SCC. WHY-62 chỉ giải thích vì sao tương quan còn là ứng viên. WHY-72/76 ghi lựa chọn sau dev. | Bỏ E5 giúp TT và hại OB. Chưa đo nhãn lan đáng kể, chưa khẳng định tự sinh là nguyên nhân. T-041 O09 còn phụ thuộc nhãn. |
| E4, z+S1/G3-D1 | Kỹ thuật + ứng viên từ hạn chế điểm/thang P4 | G2-H08/H09/H12 cho thấy khác đơn vị và cực trị. T-043 Q5/E4, WHY-67/69/71 so cổng/thang và phá hòa trên dev. | `c=1` phụ thuộc đơn vị, drift và điểm max có thể đổi hạng. Các kết quả đối chứng không cô lập một cơ chế P4 chung. |
| E6a | DT18 + lựa chọn dev | Cần xếp hạng từ tầng và khóa. So E6b trên chiều đã khai theo WHY-74/75. | Chiều PageRank đảo còn mở. Hạng theo khóa không phải xác suất nguyên nhân. |
| E7 | DT18 | Tạo hai vùng từ tập đầu và quan hệ, báo hợp vùng và tỷ lệ O. T-043 B6/E7 và kiểm vùng T13. | Chưa có căn cứ P4 riêng chứng minh vùng đúng. Cần nhãn vùng độc lập ở P10. |
| E3(a)/E3b tắt | Ứng viên từ P4 đã thử, quyết định dev | G2-H07/H14 và T-041 §5.6–5.7 gợi ý kênh/mẫu log. WHY-66/72/73 và T6 ghi lý do tắt, giữ log lỗi cơ bản. | Nối log–span và hỗ trợ mới vẫn mở. Không quy thất bại cho thiếu log nói chung. |
| E9/T12 tắt | Lựa chọn dev, đối chứng về tín hiệu tĩnh | WHY-76, T-051 và T13 kiểm đối chiếu hai snapshot. T12-on giữ là phép mô tả D8. | Hạng root giữ, vùng đổi trên TT. Revision benchmark của snapshot chưa xác minh. Kết quả không suy cho mọi đồ thị tĩnh. |
| V0, E8, (b), G/H | Truy vết và nghĩa vụ đề tài về sau | WHY-68/77, Q-245, MRP P8–P10. V0 bão hòa C-e dev, chỉ dùng truy vết. | Cần nền lành độc lập để hiệu chuẩn. G4 khai phần thiếu P/R/F1 công khai. |

Mức tiếp xúc theo G1. TT test 60/60 TX1. OB test 34/34 TX1 và 34/34 từng dò triệu chứng. Ca Nezha liền kề có thể dùng chung nguồn theo phút. Bộ đọc phải giữ đúng cửa sổ và báo mọi lần xem test theo Q-211(7). RE3-OB 30 TX0 là chưa thấy nguồn tiếp xúc, cùng hệ OB với Nezha và cùng bộ công cụ với RE2-TT. Tách khỏi dùng trong thiết kế và giữ nguyên bộ cho bản cuối theo Q-247. Nguồn là `results/T-021/goi-g1.md` và `giao-thuc-p7-a-002.json#/exposure`.

B6 hiện có dấu vân tay từng vế, snapshot ghim hash, mã bộ đọc/worker, cấu hình và bảng diễn giải, code A4, quy tắc vị trí N và đường C-e thiếu lịch sử. Các mục còn chặn là biên nhận F3 qua tuyến v2 trên dev, chốt công thức độ nhạy loại lỗi/hoán vị ca, điều phối đầy đủ P7, môi trường và revision khóa, ma trận và ngân sách, private map, quyền G3 và quyền dữ liệu. Xem `giao-thuc-p7-a-002.json#/open_before_execution`. Hai quyền G3 và dữ liệu vẫn do Minh cấp riêng.

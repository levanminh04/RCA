# T-051 — E9, cạnh tĩnh và kiểm bối cảnh

**Trạng thái:** Minh đã chốt nền và duyệt có điều kiện bảng hành động, ngân sách và triển khai dev chế độ (a) ngày 04/11/2026. Xem Q-241.
**Người làm:** Codex. **Người phản biện:** Claude.
**Gói:** P6, chuẩn bị P7. G3 và dữ liệu test vẫn khóa.

## Mục tiêu và nền đầu

Xác định trên dev chế độ (a) khi nào khởi phát giúp E9 giữ lại bằng chứng tự sinh mà E5 định gán kế thừa, việc thêm cạnh tĩnh làm đổi thứ hạng và vùng nghi ngờ qua bước nào, và kết cục của từng thành phần khối K có đổi trong bối cảnh cuối hay không.

Nền Minh chốt bật E1-U, E2-C và E5, dùng z+S1, E6a, ε = 0,05, α = 0,01, chế độ cổng G3/D1 trong mã và cạnh quan sát. E3(a), E3b, E6b, E9 và T12 tắt ở điểm xuất phát. Giữ cờ E2 trái chiều theo dataset. Chiều đảo PageRank còn OPEN. Căn cứ là kết cục T9 cho E6b theo chiều bên gọi → bên được gọi trên dev chế độ (a). [WHY-71–74](../../docs/WHY.md#why-71-d24-hiện-hành-zs1--đã-quyết-để-chọn-thiết-kế-trên-dev-q-237) · [Kế hoạch hiện hành](../../docs/KE-HOACH-SAU-T047.md#cập-nhật-hiện-hành-03112026--sau-nghiệm-thu-t-048t-053) · [Đính chính T-050](../../results/T-050/dinh-chinh-va-kiem-lai.md)

Nút là dịch vụ hoặc thực thể sau ánh xạ. Trace tạo bằng chứng trên nút và cạnh cha–con. Log và metric tạo kênh trên thực thể. E1/E2 dùng quan hệ từ span để tính đặc trưng hoặc gán bằng chứng. E5 dùng cạnh và lớp kênh để xét kế thừa. E9 dùng khởi phát để phủ quyết. E6a+S1 xếp theo tầng và khóa, còn E7 dùng đường đi hoặc liên thông để dựng vùng nghi ngờ. Task phục vụ chọn thiết kế dev cho RQ3b, mô tả vùng cho RQ3c và chuẩn bị đối chứng cho RQ3d. RQ3a cần dữ liệu đánh giá phát hiện. RQ3c cần nhãn vùng. RQ3b và RQ3d cần đánh giá riêng với baseline và đối chứng trên dữ liệu độc lập. [MRP §3 và P6–P7](../../docs/MRP.md) · [DT18](../../docs/reference/sources/DT18-de-tai-va-nhiem-vu.md) · [Hướng dẫn của cô](../../docs/reference/sources/advisor-2026-09-23.md)

## Ma trận và bằng chứng

| Bước | Phép so | Bằng chứng phân xử |
|---|---|---|
| **T11** | E9 bật trừ tắt, giữ E5 bật và cạnh quan sát. | Theo cửa sổ, thế giới và mã kênh, tách trường hợp không có đề xuất kế thừa, bị chặn bởi cạnh E2, thiếu khởi phát, đủ khởi phát có hoặc không phủ quyết. Lần theo khởi phát → phủ quyết → `F_I` → tầng, khóa → RR. Đối chiếu ca tăng, ca giảm và ca có phủ quyết nhưng giữ hạng với ca có điều kiện tương ứng. |
| **T12** | Hợp cạnh quan sát và cạnh tĩnh trừ cạnh quan sát, giữ E9 theo kết cục T11 đã đủ căn cứ dùng. | Báo cạnh trùng, cạnh thêm, endpoint ngoài U, revision, nhóm vòng và đường giải thích của E5. Tách thay đổi RR khỏi thay đổi của hai cách E7, C-d1 và C-d3 ở P. Dùng C-d2 để kiểm đầu vào kênh và khởi phát vẫn bất biến. |
| **KB** | Trên nền sau T12, đảo riêng E1, E2, E3(a), E5. Mỗi cặp tính bật trừ tắt. | So theo luật khối K với kết cục T-053 tương ứng là **GIÚP, TRÁI CHIỀU theo dataset, HẠI, GIÚP**. Báo cả cờ phụ thuộc quan sát mới nếu có. Khi tắt E5, giữ cờ E9 như nền cuối và ghi E9 mất chỗ tác động theo thiết kế. Kết cục đổi thì ghi “phụ thuộc bối cảnh” và trình Minh. |

T11 chỉ ghi “không áp dụng” nếu nền hợp lệ thực sự tắt E5. Tổ hợp E9 × cạnh tĩnh ngoài nhánh do T11 chọn là phép tương tác riêng. Nếu KB đưa tới đề xuất đổi E5, trình phạm vi phải kiểm lại, gồm câu hỏi tương tác VC × E5 còn mở. [T-043 B4 và Phụ lục C](../T-043-thiet-ke-rca-m1/SPEC.md) · [T-053, `/cap`](../../results/T-053/runs/k-cham-001/khoi-k.json)

C-d3 áp dụng cho RE2-TT theo đính chính T-043 Đ12. [Đính chính phiên 9](../../results/T-043/dinh-chinh-phien9.md)

## Chấm và áp luật

- Giữ **52 ca thật, 30 cửa sổ giả RE2-TT**, ba thế giới `P`, `S_lo`, `S_hi`, cửa sổ, U và giao thức dev chế độ (a). Chấm RR theo kỳ vọng của nhóm hòa, giữ ca lỗi trong mẫu số theo hợp đồng. Báo MRR, Hit@1/3/5, NDCG@5, Retrieval@5 và Rerank@1.
- T11/T12 gọi `luat_C`, KB dùng `khoi_K` cho từng cặp. Giữ δ = 0,01 và δ_d lần lượt 1/30, 1/22. KB áp UV-6 cho E3(a) và M5 cho cặp E5, dùng đồ thị cha–con thuộc N để tính M5. Giữ `E_X` từ KS-16 ở pha chấm. E9 có 10 ô, T12 có 13 ô theo định nghĩa sàng trước. Báo riêng số ca thực sự đi vào cơ chế. [KS-16, `/o_kich_hoat`](../../results/T-043/ks16/dem-sau-ghep-nhan.json)
- C-e tính lại N1 tại P cho từng cặp bằng `ve_n1`, dùng cùng vế cho ba thế giới. Mức HẠI là tăng trung bình **lớn hơn 1** thực thể tầng 1 mỗi cửa sổ hợp lệ. Báo V0, mẫu số, số cửa sổ bị loại và kết cục. Nếu mẫu số bằng 0 do mọi cặp cửa sổ bị loại vì `INSUFFICIENT_EVIDENCE`, ghi `CHUA_KIEM_DUOC` và tính các vế còn lại. Thiếu trường bắt buộc, `ERROR` hoặc `UNSUPPORTED` thì dừng phần phụ thuộc. N1 là dung sai thực dụng, hiệu chuẩn `verdict` còn mở. Báo kèm kiểm dấu theo ô, khoảng tin cậy bootstrap theo ô và độ nhạy δ = 0,005/0,02, h = 0,5/2. Quyết định dùng các ngưỡng chính. [WHY-70](../../docs/WHY.md#why-70-vế-mốc-giả-t-047-dùng-số-thực-thể-tầng-1-và-mức-hại-thực-dụng--đã-quyết-về-cách-thử-q-231-chưa-hiệu-chuẩn) · [Helper N1](../../results/T-047/scripts/luat_c_t047.py)

| Kết cục T11/T12 | Hành động đề xuất duyệt trước |
|---|---|
| GIÚP | Dùng nhánh bật cho bước kế tiếp. |
| HẠI | Dùng nhánh tắt. |
| KHÔNG TÁC DỤNG | Đề xuất bỏ, dùng nhánh tắt cho bước kế tiếp nếu ngoại lệ DT18/MRP ở Phụ lục C không áp dụng. |
| KHÔNG ĐỦ CA hoặc phụ thuộc quan sát | Mặc định giữ bật theo D2a/D2f và ghi chưa phân xử. Nếu P cho HẠI, trình Minh trước bước phụ thuộc. |
| TRÁI CHIỀU hoặc thiếu dữ kiện bắt buộc | Trình Minh, chờ chốt nền để chạy bước phụ thuộc. |

Báo riêng kết cục tại từng thế giới, kết cục kết hợp và hành động. KB báo thay đổi bối cảnh để Minh quyết. T-052 dùng nền cuối sau khi các quyết định có căn cứ đã được ghi nhận. [Phụ lục C](../T-043-thiet-ke-rca-m1/SPEC.md#phụ-lục-c--luật-kết-cục-và-bảng-ứng-viên)

## Nguồn, triển khai và tự kiểm

1. **Ghim nguồn.** Dùng ma trận và seal T6 của T-049 để truy nền `K-thang-C`, đối chiếu T-050 và nguồn khối K T-053. Ghim hash mã và môi trường, bộ cửa sổ, alias, cấu hình, thế giới, nguồn tĩnh và hợp đồng số học. Nhãn dev và `E_X` để riêng cho pha chấm. [Seal T6](../../results/T-049/runs/t6-001-seal.json) · [Manifest T-050](../../results/T-050/manifest-chay-lai-002.json) · [Seal T-053](../../results/T-053/runs/k-dong-pha1-001/seal.json)
2. **Kiểm đường phát lại trước E5.** Dấu vết cũ lưu kênh sau lọc U. Ở từng cấu hình, cửa sổ và thế giới, đối chiếu tập mã kênh có cờ đã lưu với tập mã `F_I` đầy đủ và đơn vị có cờ, gồm kênh E2 được gán. Giữ `s_q`, lớp, khởi phát, `m` theo đơn vị, mask cạnh E2 theo thế giới và `G_N`. Chạy E5/E9 trên đủ kênh có thể tác động, sau đó lọc U và tính lại khóa S1 theo `F_I` mới. Thiếu dữ kiện thì khoanh đúng cửa sổ và dùng đường tính gốc đã được duyệt trong ngân sách. [Capture cũ](../../results/T-048/scripts/chay.py#L201) · [Thứ tự chạy gốc](../../src/m1/chuoi.py#L544)
3. **Kiểm riêng T11.** Kiểm ngưỡng nghiêm `> 2 × 10 giây + 1 ms`, dùng mốc ns và nguồn khởi phát hợp lệ. Nezha-OB chỉ dùng trace cho E9. Một cạnh khớp mask E2 theo một trong hai chiều trên bất kỳ đường giải thích nào sẽ chặn phủ quyết của cả kênh. Đếm trạng thái theo mã kênh, lưu riêng các đường giải thích. Khi giữ nguyên đầu vào, bật E9 chỉ có thể đổi `F_I` từ 0 sang 1. RR vẫn có thể tăng, giảm hoặc giữ nguyên. [E9](../../src/m1/e9.py) · [E5](../../src/m1/e5.py#L174)
4. **Kiểm riêng T12.** Chiếu toàn bộ cặp hướng `(source,target)` từ hai mô hình tĩnh đã ghim, áp alias và gộp trùng theo đường chạy gốc. Giữ loại quan hệ và nguồn gốc để diễn giải. Danh sách cạnh theo ca ở KS-16 phụ thuộc nhãn root và chỉ phục vụ pha chấm. Giữ E1, E2, U và đơn vị chấm bất biến. Nút chỉ có trong mô hình tĩnh là `UNOBSERVED`. Theo Đ19, thiếu khai báo cho `UNSUPPORTED`, sai kiểu cho `ERROR`, danh sách rỗng hợp lệ. Kiểm `NO_TARGET`, `UNSUPPORTED_CYCLIC` và thời gian liệt kê đường của C-d3 trước lượt chính. Revision nguồn tĩnh chưa nối được chắc chắn với bản benchmark, nên kết luận T12 có điều kiện theo nguồn. [T-038](../../results/T-038/do-thi/thuc-the.json) · [T-039](../../results/T-039/do-thi/thuc-the.json) · [Chiếu cạnh KS-16](../../results/T-043/ks16/ks16_pha2_v11.py#L207) · [Đ19](../../results/T-043/dinh-chinh-phien10.md#đ19-hợp-đồng-thời-gian-và-đầu-vào-cạnh-tĩnh-f1)
5. **Kiểm tái sử dụng KB theo từng cấu hình.** Đối chiếu nền và bốn biến thể `K-E2+E5`, `K-E1+E5`, `K-E1+E2+E3+E5`, `K-E1+E2`. Chứng minh tương đương dữ liệu, cấu hình, mã và số học giữa bản vá z qua helper T-053 và z đã tích hợp ở T-049. Nếu E9 và T12 vẫn tắt, dùng bản ghi gốc khi đủ căn cứ. Nếu một trong hai bật, dùng trung gian riêng của từng cấu hình và tính lại từ E5. Đọc mỗi tệp nguồn một lần theo cửa sổ cho các cấu hình cần dùng. [Bản vá T-053](../../results/T-053/scripts/pha1.py#L89) · [Seal khối K](../../results/T-053/runs/k-dong-pha1-001/seal.json)
6. **Pilot, seal, chấm và lần vết.** Chọn pilot trước ghép nhãn theo dataset, khối lượng, cấu trúc và khả năng kích hoạt quan sát được, gồm ca có và không có cơ chế. Dùng fixture sẵn có. So đường chạy gốc với phát lại trên cùng máy về đầu vào, `F_I`, `m`, khóa, nhóm hòa, vùng, trạng thái và dấu vết. Nếu sai khác chéo máy ảnh hưởng đối chiếu, khoanh vùng và trình chi phí kiểm trên máy nguồn. Giữ biên nhận từng cửa sổ và mọi lượt hỏng. Seal pha 1 trước khi ghép nhãn. Khi giải thích kết quả, tách hạn chế dữ liệu, giao thức, adapter và giả định phương pháp. [Bộ chấm pha 2](../../src/m1_danh_gia/pha2.py)

## Đầu ra, quyền ghi và tiêu chí xong

SPEC tại `tasks/T-051-t11-t12-va-kb/SPEC.md`. Phạm vi triển khai đề xuất gồm `results/T-051/` cho công cụ gọi lại, hồ sơ nguồn, pilot, bản ghi và seal, kết quả chấm, bảng cơ chế, báo cáo và manifest. Nối `tasks/T-051-t11-t12-va-kb/LOG.md` và cập nhật đúng dòng T-051 trong `docs/STATE.md` theo quyền được duyệt. Bất kỳ thay đổi `src` nào cần đề xuất cụ thể về file, ảnh hưởng và phép hồi quy.

Tiêu chí xong là có căn cứ phát lại hoặc đầu ra từ đường chạy gốc cho phần cần thay, từng cặp đúng cấu hình và đủ miền ca, T11/T12 có chuỗi bằng chứng cho cơ chế hoặc chỉ rõ dữ kiện còn thiếu, KB đối chiếu đúng bối cảnh cũ và mới. Báo nền đề xuất cho T-052 cùng mọi cờ chưa phân xử. T-052 dựng lại vùng trên nền cuối và chuẩn bị đối chứng cho RQ3d. Chiều đảo PageRank, tương tác bổ sung, hiệu chuẩn `verdict`, chế độ (b), RE3-OB, G3/test và triển khai FlashTicket có phạm vi quyết định riêng.

## Ngân sách đề xuất

**25–55 phút triển khai sau duyệt**, chưa đo trên T-051. Đường chính dùng một tiến trình trên laptop, trần đề xuất **60 phút thực**, tính cả pilot, lượt chính và hồ sơ triển khai. Khoảng này giả định đủ trung gian và C-d3 chạy trong dự toán. Cập nhật sau kiểm nguồn và pilot, tách thời gian máy theo cửa sổ, thời gian thực và thời gian chờ quyết định. Đo riêng đọc/hash, giải nén, hậu xử lý, C-d3 và RAM đỉnh. Kiểm ngân sách tuần tự theo dataset của Q-40. Nếu phải tính lại trên diện rộng, cần EC2 hoặc dự báo vượt trần, trình số cửa sổ, thời gian và chi phí trước khi chạy phần đó. [Q-40 và Q-43](../../docs/DECISIONS.md)

## Bàn giao phản biện

Minh chuyển prompt soát SPEC đã trình trong chat cho Claude cùng file này. Mẫu là Prompt chung, khối Soát SPEC và khối G3 trong [hướng dẫn phản biện](../../docs/review-prompt.md). Phạm vi lượt soát đề xuất là chỉ trả lời trong chat.

# WHY đề xuất từ T-043

- **Trạng thái:** đề xuất. Minh duyệt từng mục rồi mới chép vào `docs/WHY.md`; Minh cấp mã chính thức. Mã WHY-M1-xx chỉ dùng trong file này.
- **Phạm vi:** các lựa chọn T-043 phải chốt (SPEC bước 2, 6), cộng các lựa chọn D1–D24 cần mục lý do mà WHY hiện chưa có. Lựa chọn về độ đo chính và E-04 đã ở WHY-06.
- **Quy ước:** mỗi mục ghi chọn gì, vì sao, phương án đã xét, bằng chứng, giới hạn, kết luận phụ thuộc. "Chưa kiểm" là giả thuyết, không là căn cứ đã xác nhận.

## WHY-M1-01. Chia N/A theo thời điểm kết thúc của span

- **Chọn:** span thuộc A khi end ≥ t (SPEC B1.1). Quan hệ cha–con dựng trên toàn miền; tính đặc trưng rồi mới chia (B1.2).
- **Vì sao:**
  - Cùng quy ước với MicroRank và TraceRCA ở P3, nên so với baseline không trộn hai cách chia.
  - Một span kết thúc sau t có thời lượng chịu ảnh hưởng của sự cố, nên xếp vào A.
  - Tính đặc trưng trước khi chia giữ đúng thời gian độc quyền của span cha qua mốc (fixture 44).
- **Phương án đã xét:** chia theo start (`cua_so.py` đếm `spans_N` theo start). Lệch quy ước baseline; span bắt đầu trước t nhưng chậm vì sự cố bị xếp vào N.
- **Bằng chứng:** T-032 bảng C tách trước và sau theo end của span phía gọi. Đối chiếu KS-16 khớp đúng 26/26 ca RE2-TT (LOG phiên 7).
- **Giới hạn:** span rất dài trải qua mốc mang một phần thời gian trước sự cố.
- **Kết luận phụ thuộc:** mọi đơn vị trace của M1.

## WHY-M1-02. Điểm E4 cố định; nhánh z chỉ báo cáo (D24)

- **Chọn:** điểm của chuỗi là e_d của E4 (tỷ lệ vượt ngưỡng nền sau cổng kiểm định). T4b chỉ báo cáo nhánh z. Khối K không đảo E4/z.
- **Vì sao:**
  - E4 cho điểm trong [0; 1] ở mọi loại đơn vị và không phụ thuộc đơn vị đo, nên ghép được kênh đếm với kênh phân vị (fixture 76b).
  - Nhánh z nhạy với IQR nhỏ (G2-H09; fixture 76c) và phụ thuộc đơn vị khi c = 1 (fixture 76a).
  - Chọn giữa hai cách chấm sau khi nhìn số dev sẽ thêm một bậc tự do vào luật chọn.
- **Phương án đã xét:**
  - T4b quyết định cách chấm (Codex B27-4): bị thay bằng D24.
  - Nhánh z làm điểm chính: chưa có căn cứ trên dev.
- **Bằng chứng:** fixture 75, 76, 81, 82 kiểm 109/109 (`fixture/ket-qua-kiem.json`). G2-H09 không phân xử E4 với nhánh z mới (LOG phiên 6, B28-3).
- **Giới hạn (đánh đổi theo D24):**
  - bão hòa: mọi mẫu A vượt ngưỡng thì không phân biệt độ lớn;
  - trôi nền cho điểm cao khi không có lỗi (fixture 81);
  - biên ε·|q| phụ thuộc mức tuyệt đối;
  - cổng giả định mẫu độc lập (B1.3; mô phỏng AR(1) cho tỷ lệ qua cổng 7,3–38,6% khi hệ số 0,5–0,98).
  Chỉ có T4, T4b làm phép độ nhạy. Cách chấm của M1 không còn phương án thay thế ở mức quyết định.
- **Kết luận phụ thuộc:** mọi kết cục khối K và luật C; tỷ lệ `CAUSE_FOUND` ở mốc giả.

## WHY-M1-03. Luật trạng thái quan sát trên dev (hoàn thiện D12)

- **Chọn:** đặc tả v1 mục 2.2, với luật F phương án (a) theo Q-207 (`dinh-chinh-phien9.md` Đ9; thay luật v1.1 đề xuất ở `dinh-chinh-phien8.md` Đ1).
  - Mỗi file nguồn phủ [bản ghi đầu, bản ghi cuối + r); r là độ phân giải mốc. F là bao các file. Khe K là phần của F không thuộc file nào (khe dương giữa hai file).
  - H là bao bản ghi của nguồn trên cả cửa sổ đang xét.
  - Phần ngoài F là XÁC NHẬN THIẾU THU khi có căn cứ phía xuất; phần trong K là OPEN; phần trong F ∩ H ngoài K là A0; phần trong F ngoài H là OPEN.
  - T^chắc = |(F ∩ H) \ K ∩ phía|; T^max = |F ∩ phía|.
  - Ô biên tách theo giây thực.
  - Metric không tham gia T.
  - Thông tin khoảng ghi đi vào phương pháp qua `params.coverage` do runner cấp (Đ2).
- **Vì sao:**
  - "Ngoài khoảng ghi của file" là bằng chứng thiếu thu mà B1.3b đã liệt kê, khi có căn cứ phía xuất.
  - Khe giữa hai file không xác định được là thiếu thu hay đã thu: nó có thể là lúc không có sự kiện, đệm khi xuất, mất bản ghi ở biên file hoặc phần không được xuất. Vì vậy khe là OPEN; ba thế giới quét phần này thay vì chọn một bên là sự thật.
  - Với Nezha-OB, căn cứ phía thu/xuất là điều kiện xuất dữ liệu: mỗi lần tiêm chỉ có ba file phút (`results/T-008/the-dataset.md` §8). Metric theo ngày cho thấy hệ vẫn chạy ngoài F: 740/740 điểm PodWorkload dương ở 22/22 ca (`runs/bien-F-001/ket-qua.json#/tong_hop`). Không suy thiếu thu từ việc không thấy bản ghi.
  - A0 nói về "khoảng có bản ghi" của nguồn, không cắt tại t.
  - Tính H riêng từng phía làm giây cuối mỗi phía thành OPEN giả khi mốc là giây nguyên (lượt thử nhanh `ks16/runs/thu-nhanh-001`).
- **Phương án đã xét:**
  - H theo từng phía: báo kèm ở `T_bien_the_H_theo_phia`.
  - Coi cả F là A0: bỏ mất trạng thái OPEN ở đầu, cuối cửa sổ khi nguồn thưa.
  - Gộp khe giữa hai file vào F làm A0 (bản v1): coi thời gian không thuộc file nào là đã quan sát.
  - Loại khe khỏi F làm thiếu thu (bản v1.1): coi khe là chắc chắn chưa thu. Cả hai cách đều chọn một bên mà dữ liệu không phân xử được.
- **Bằng chứng:**
  - KS-16 pha 1: trace và log Nezha-OB chỉ phủ 41–97 giây ở N và 84–140 giây ở A ở cả 22 ca, ở cả hai bản luật; 488/660 ô N là thiếu thu. RE2-TT không có ô OPEN.
  - Hai bản v1 và v1.1 chênh T ở 12/22 ca Nezha-OB, tối đa 1,21 s (1,01%). Số ô kích hoạt không đổi. 4/1.420 đơn vị đếm đại diện đổi quyết định cổng (`runs/so-v1-v11-004/ket-qua.json`; `dinh-chinh-phien8.md` Đ5). Đây là độ nhạy, không là sai số so với sự thật.
  - Theo (a), đơn vị đếm đại diện phụ thuộc quan sát: RE2-TT 5 (có sẵn, 0 phát sinh thêm), Nezha-OB 4 (đều do khe, đúng bốn đơn vị lật giữa v1 và v1.1) (`runs/khe-open-002/ket-qua.json#/tong_hop`).
- **Giới hạn:**
  - A0 chưa kiểm được trên dữ liệu công khai (D12). Kết luận vẫn ghi "dưới A0".
  - Mép ngoài của F lấy theo bản ghi đầu và cuối. Đây là giả định chưa kiểm, không có cận sai số. Nó sai khi việc xuất bắt đầu trước bản ghi đầu (hoặc kết thúc sau bản ghi cuối) mà không có sự kiện; khi đó T bị đánh giá thấp. Dev có khoảng không bản ghi dài tới 1,212 s giữa hai file, nên mật độ ở mép không loại được một khoảng cỡ đó.
  - Ba thế giới chỉ quét phần bất định đã đưa vào T (khe và phần F ngoài H), không bao bất định ở mép ngoài.
- **Kết luận phụ thuộc:**
  - T của mọi đơn vị đếm; OBS_DEPENDENT; dự đoán "E3b trên Nezha-OB OBS_DEPENDENT" của SPEC mất căn cứ.
  - Chế độ (b) trên Nezha-OB không được dùng `params.coverage` dựng từ file phút, vì file phút mang thông tin phút tiêm (Đ2).

## WHY-M1-04. Span bọc dạng chặt

- **Chọn:** w có đúng một con, con ở thực thể khác, cha của w cùng thực thể.
- **Vì sao:** khi đó g(w) đúng là phần ngoài span bên được gọi. Dạng lỏng (cho thêm con cùng thực thể) làm g(w) trừ cả thời gian của các con ấy.
- **Phương án đã xét:** dạng lỏng.
- **Bằng chứng:** hai dạng trùng nhau ở mọi ca dev: RE2-TT 1.643.384, Nezha-OB 338.829 (`ks16/dem-khong-nhan.json#/tong_hop/*/wrap_strict`, `wrap_loose`). Vì vậy trên dev lựa chọn này không đổi kết quả.
- **Kết luận phụ thuộc:** E1 (bỏ span bọc khỏi mẫu); E2.

## WHY-M1-05. Danh mục kênh và hướng chấm

- **Chọn (`hop-dong.json#/kenh`):**
  - giữ mọi cột metric có trong file;
  - tài nguyên chấm hai hướng ở mọi cấu hình;
  - tỷ lệ thành công chỉ chấm khi E3 bật;
  - metric front của Nezha-OB gắn vào `frontend`.
- **Vì sao:**
  - Theo WHY-27, không bỏ cột cho baseline; dùng cùng nguyên tắc cho M1.
  - B1.4 liệt kê "tài nguyên giảm" như một lớp riêng, không gắn với E3.
  - D2d chỉ cho E3 thêm hướng xuống cho tỷ lệ thành công.
- **Phương án đã xét:**
  - Chỉ giữ P90: là một lựa chọn riêng, lệch WHY-27.
  - Chỉ chấm tài nguyên giảm khi E3 bật: SPEC không gắn hướng này với E3.
- **Bằng chứng:** chưa có bằng chứng dev cho bất kỳ phương án nào. Đây là quy ước đặt trước thực nghiệm.
- **Giới hạn:** nhiều phân vị tương quan làm tăng "số kênh" trong khóa K.
- **Kết luận phụ thuộc:** R0 và mọi cấu hình. Đổi sau khi xem số dev là thay đổi thiết kế, phải trình Minh.

## WHY-M1-06. Hợp đồng severity theo nguồn

- **Chọn:** ánh xạ theo từng nguồn; UNKNOWN không tính là lỗi hay không lỗi; kênh severity gọi đúng là "mật độ dòng lỗi có severity xác định"; NO_BASELINE, NO_A khi không có dòng xác định.
- **Vì sao:**
  - So khớp nguyên chữ `ERROR` cho 0 dòng lỗi, vì giá trị trên dev là chữ thường (T-042 `continuation-001`, `#/values`).
  - Tiền lệ T-042 chỉ hỗ trợ ý "cách đọc trường ảnh hưởng kết quả" (`results/T-042/runs/continuation-001/bao-cao-bo-sung.md:18`). Nó không là bằng chứng cách đọc nào cho RCA tốt hơn (LOG phiên 6, B26-3).
- **Phương án đã xét:** đổi UNKNOWN thành INFO (che thiếu thông tin); đặt ngưỡng độ phủ (chưa có căn cứ).
- **Bằng chứng:** KS-16: adservice và cartservice có log nhưng không có severity xác định ở cả N và A (`ks16/dem-khong-nhan.json#/cases/*/log`).
- **Giới hạn:** độ phủ severity khác nhau giữa N và A vẫn OPEN (N9). Chưa có căn cứ chọn cách hiệu chỉnh. Mục này không quy định cách phân loại mẫu Drain khi có UNKNOWN; phần đó ở `dinh-chinh-phien10.md` Đ15.
- **Kết luận phụ thuộc:** kênh log lỗi cơ bản (E3 tắt) ở Nezha-OB; phân loại mẫu Drain khi E3 bật (Đ15).

## WHY-M1-07. Chưa dùng nối log–span trong bản P7 (lựa chọn ưu tiên phạm vi)

- **Chọn:** E3 đếm theo thực thể và thời gian. Nối log–span là ứng viên chặng 2, khóa trước chặng 3 (`bang-chuyen-giao.json`, dòng `log_span`).
- **Vì sao:** ưu tiên phạm vi. Dùng nối cần thiết kế thêm: kênh (a) và trạng thái khi thiếu liên kết; hợp đồng E5 theo request cho (b); phạm vi phép thử. Phạm vi phép thử chưa thiết kế, nên chưa nói được phải nhân rộng khối K hay không. Chưa ước lượng phần việc. Đây không phải kết luận rằng nối quá tốn hay không thử được trên dev.
- **Phương án đã xét:**
  - Một lõi có nhánh khi thiếu liên kết (dùng nối ở Nezha-OB, nhánh không nối ở RE2-TT). Khả thi, không trái WHY-08: WHY-08 đòi một lõi và định dạng chung, không đòi mọi dataset có cùng loại thông tin; E3 hiện đã có nhánh theo dataset (severity ở Nezha-OB, từ khóa ở RE2-TT).
  - Ứng viên khi dùng: (a) tỷ lệ lần thực hiện thao tác có log lỗi; (b) E5 theo request trong cùng trace (SPEC E3).
- **Lý do cũ đã rút** (`dinh-chinh-phien10.md` Đ18): "dùng nối ở một dataset làm phép tính khác nhau giữa hai dataset"; "chưa có câu hỏi trên dev mà nối phân xử được".
- **Bằng chứng:** RE2-TT không có cột ID, không thông điệp nào chứa chuỗi hex 32 ký tự (KS-16 pha 1). Nezha-OB: 1.537.834/1.539.335 dòng khớp đúng một span (99,90%), 1.501 dòng không khớp, 0 dòng lệch thời gian (`ks16/dem-khong-nhan.json#/cases/*/log_span_join/tong`).
- **Câu hỏi OPEN:** nối log–span có cải thiện RCA không. Nezha-OB dev phân xử được câu này.
- **Dự toán (chưa kiểm; `dinh-chinh-phien10.md` Đ22):** code nối và số đo KS-16 dùng lại được (pha 1 trên 22 ca Nezha-OB, gồm nối: tổng 92,2 s, RSS tối đa 1,41 GB). (a) khoảng nửa đến một phiên thiết kế cộng phản biện, phần cài trong task cài đặt (1); (b) ít nhất một phiên thiết kế riêng. Phép thử đề xuất: một cặp bật/tắt (a) tại cấu hình thắng, chỉ Nezha-OB. Cache M1 chưa có sẵn.
- **Giới hạn:** hoãn có thể đẩy một phép phân xử khả thi trên dev ra sau, làm tăng phần phải thiết kế và đánh giá ở chặng sau. Chưa có bằng chứng buộc phải cài nối ngay, cũng chưa có bằng chứng bỏ nối không mất lợi ích.
- **Kết luận phụ thuộc:** E3, E5; bảng chuyển giao (dòng `log_span`).

## WHY-M1-08. E5 có tương quan giữ ở trạng thái ứng viên (bước 1 của SPEC)

- **Chọn:** chưa đưa vào `ma-tran-thu.json`.
- **Vì sao:** chưa có hợp đồng khả thi trên dev (thẻ MicroHECL).
- **Hợp đồng nếu sau này đề xuất phải ghi:**
  - **chuỗi được so:** metric của cạnh hiện tại và cạnh kề, cùng loại tín hiệu;
  - **cách căn thời gian:** cùng lưới theo phút hoặc 10 giây, mốc theo end;
  - **số mẫu (cấu hình được dẫn):** MicroHECL dùng 60 điểm; đây là cấu hình của bài, không là số mẫu tối thiểu chung. Dev có 5 + 5 điểm metric ở Nezha-OB; trace Nezha-OB chỉ có 4–9 ô 10 giây ở N và 8–14 ô ở A;
  - **chuỗi hằng:** tương quan không xác định, nên không tỉa và ghi UNSUPPORTED;
  - **thiếu dữ liệu:** không nội suy;
  - **điều kiện thất bại:** hai chuỗi trôi cùng chiều (RE2-TT metric 1 giây, tự tương quan) có tương quan cao mà không có quan hệ nhân quả; bão hòa; trễ pha.
- **Kết luận phụ thuộc:** fixture 57 (điều kiện thất bại của E5) vẫn chưa có cách sửa đã kiểm.

## WHY-M1-09. Định nghĩa ô kích hoạt và kiểu quan sát O1–O4

- **Chọn:** `dinh-nghia-pha2.json`, băm trước pha 2 của KS-16.
- **Vì sao:**
  - Ô kích hoạt E_X là nhóm ca mục tiêu khai trước của thành phần. Định nghĩa dựa trên dữ liệu và nhãn của chính ca, không dựa trên đầu ra M1 (chưa cài).
  - E_X không là điều kiện cần để hạng root đổi: thành phần có thể đổi hạng root ở ca ngoài E_X qua điểm của thực thể khác (`dinh-chinh-phien9.md` Đ10). E_X cũng không là bằng chứng cơ chế, lợi ích hay khả năng chuyển sang FlashTicket.
  - Luật C giữ nguyên (Q-207): P > M trong E_X là yêu cầu ưu tiên lợi ích trong nhóm mục tiêu, là chính sách chọn trên dev. Nếu chưa dừng ở bước 1–4, ca có ΔMRR gộp > δ nhưng P ≤ M tới bước 7 (Minh quyết). P ≤ M không có nghĩa lợi ích chỉ nằm ngoài nhóm (`dinh-chinh-phien10.md` Đ17). Luôn báo P′, M′. Câu hỏi cơ chế xét bằng trung gian từng ca; chuyển giao xét ở P10.
  - E1, E2 dùng đúng định nghĩa của số xem trước trong SPEC (8/11, 2/6), nên số T0 khớp số xem trước.
  - SPEC không định nghĩa O1–O4 (LOG phiên 7, R7-2). Người làm đặt theo điều kiện thất bại S7, G2-H19 và luật "quan sát được" B1.9.
- **Phương án đã xét:**
  - E3 theo dữ liệu (log lỗi root tăng) thay cho theo loại lỗi mã: lẫn tác dụng với điều kiện.
  - E5 theo cờ M5 của một baseline duy nhất: hẹp và phụ thuộc baseline được chọn.
- **Bằng chứng:** `ks16/dem-sau-ghep-nhan.json#/o_kich_hoat`. E3 có 4 ô nên là thành phần ít ca. Các thành phần khác ≥ 6 ô.
- **Giới hạn:** ô kích hoạt của E5 dùng M5 trên bản ghi baseline. M5 là đồng xuất hiện, không đo đủ mệnh đề "lan" (`results/T-028/codebook.md:95`). Các giới hạn khác của nhóm mục tiêu ghi ở `dinh-chinh-phien9.md` Đ10.
- **Kết luận phụ thuộc:** "thành phần ít ca" trong luật chọn khối (E3 bị ép bật nếu không HẠI, D2a); P, M của luật C (Q-207): nhãn kết cục ở bước 8 của khối K; quyết định ở T6, T9, T11, T12 và K-b.

## WHY-M1-10. C-h (PRISM) giữ ở trạng thái ứng viên, chưa vào bản P7

- **Chọn:** chưa đưa C-h vào T13. C-h là ứng viên (`dinh-chinh-phien10.md` Đ16).
- **Vì sao:** định nghĩa hiện có chưa xác định được từ đầu vào tới thứ hạng. Còn thiếu: có dùng cổng và cờ E4 hay không; chấm tuyệt đối hay theo hướng; tỷ lệ thành công khi R0 tắt E3; gộp theo thời gian (phụ lục PRISM chưa cho đủ quy tắc); thang khi IQR = 0; kênh thiếu; thực thể không có thuộc tính bên ngoài. Chọn cách xử lý sau khi thấy kết quả sẽ làm phép so khó diễn giải.
- **Phương án đã xét:**
  - Giữ C-h với định nghĩa hiện có: không chọn, vì người cài phải tự thiết kế tiếp.
  - Hoàn thiện công thức ngay: chưa đủ nguồn (gộp thời gian). Bài PRISM đưa một họ điểm lệch với thang dương; IQR chỉ là một lựa chọn.
- **Hệ quả:** chưa có phép so với quy tắc phân biệt thuộc tính nội bộ và bên ngoài, không dùng quan hệ. Các đối chứng đã duyệt khác giữ nguyên.
- **Điều kiện thêm lại:** công thức khóa trọn vẹn trước khi chạy, ghi phần kế thừa PRISM và phần tự thích nghi, Minh duyệt. Khi đó phép so với M1 vẫn trộn cách chấm và cách dùng quan hệ, nên không dùng riêng để quy lợi ích cho E5.
- **Kết luận phụ thuộc:** T13 (RQ3d chỉ còn các đối chứng C-a0, C-a1, C-d1, C-d2, C-d3).

## WHY-M1-11. Thực thể có dữ liệu nhưng không có kênh OK thì không trả về

- **Chọn:** ghi `NO_VALID_CHANNEL`, không trả về, RR = 0 nếu là root; báo riêng số ca.
- **Vì sao:** đây là cách đọc đúng câu "thực thể có ít nhất một kênh OK được xếp theo ba tầng" của B1.6. Xếp thực thể không có phép chấm nào là xếp ngẫu nhiên, trái WHY-26 ("điền phần thiếu cho phương pháp điểm nhờ may").
- **Phương án đã xét:** đưa vào tầng 3. Không chọn vì tầng 3 là "có phép chấm, không có cờ".
- **Kết luận phụ thuộc:** MRR khi root chỉ có kênh LOW_SUPPORT.

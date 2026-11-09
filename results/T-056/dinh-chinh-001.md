# T-056 — Đính chính 001 (sau phản biện Codex, 08/11/2026)

File này sửa diễn giải trong `results/T-056/bao-cao.md`. Báo cáo gốc giữ nguyên, để `manifest-001.json` và `manifest-002.json` vẫn trỏ đúng byte. Không đổi số xếp hạng, không chạy phương pháp, không đổi thiết kế. Mọi điểm là **mô tả sau khi xem** test (C-15 B).

Nguồn quyền: Minh cho phép ghi gói bốn file Codex đề xuất nếu Claude không còn mâu thuẫn với Codex (chat 08/11/2026). Nguồn số: **K** = `results/T-056/ket-qua.json`, **K2** = `results/T-056/ket-qua-002.json`, **B** = `results/T-054/reports/main-013-v2/tables.json`, **P** = `results/T-054/protocol.json`.

Cột "Ai kiểm": C = Claude, X = Codex. Phần nào chỉ một bên kiểm thì ghi đúng như vậy.

## 1. Câu thay thế

| # | Chỗ trong báo cáo | Câu cũ (rút gọn) | Câu thay thế | Ai kiểm |
|---|---|---|---|---|
| D1 | Dòng 139, 141, 160 | 12 ca TT chỉ M1 đúng: "M1 thắng nhờ E1/E2"; "lỗi mạng cần quan hệ" (mức II) | Trong 12 ca TT mà M1 đặt root hạng 1 còn R1 không đạt, C-a0 (tắt E1/E2/E5) cũng đặt root hạng 1 ở 12/12 ca. Vì vậy, nhóm này **không chứng minh lợi thế đòi hỏi bật E1/E2/E5**. Phần tín hiệu và cách tính chung nào tạo lợi thế trước R1 chưa được cô lập. Không mở rộng thành "lỗi mạng không cần quan hệ" hay "E1/E2/E5 không đóng góp trong chuỗi M1". Quan sát giữ lại: 12 ca đều thuộc loss/delay. | C, X |
| D1a | Như trên | — | Phần chung M1/C-a0 **không gồm E3/E3b**: cả hai cấu hình đều tắt E3 và E3b. Phần chung gồm kênh metric, log lỗi cơ bản (khác E3b) và khóa z của E4. Trace operation có ở cả hai nhưng **khác dạng**: M1 (E1 = U) dùng self-time, C-a0 (E1 tắt) dùng thời lượng toàn phần. | C: cấu hình P; X: 12/12 bản ghi |
| D1b | Như trên | — | Ba ca auth/loss (`60f9be319f`, `d62934a19f`, `d819fba4a5`) có 0 cạnh nối ts-auth-service trong `extra/canh` của bản ghi M1. | X; C kiểm lại cả hai bản ghi M1 mỗi ca |
| D2 | Dòng 133 | Nezha-OB "không đơn giản"; M1 0,875 "nhờ E1/E2" | "OB đơn giản hay không" vẫn **OPEN**, vì chưa tính R1 trên OB. M4 thấp hơn không phân xử điều này. Về M1: so với bỏ riêng E1, M1 thắng/hòa/thua 8/25/1; so với bỏ riêng E2 là 7/25/2; so với C-a0 là 11/20/3 (MRR 0,875 so với 0,711). E1/E2 có tác dụng có điều kiện trên OB. Chưa phân rã chênh M1–C-a0 thành các đóng góp độc lập. | C, X |
| D3 | Dòng 126, 128, 159; STATE | "M4 = R1"; "Hạng 1 R1 trùng M4 60/60, 30/30"; "phiếu trace và log không đổi hạng 1 ở ca nào" | R1 tái lập **khối đầu và RR của root** của M4 ở 60/60 ca TT và 30/30 ca RE3. Thứ tự hoặc hòa phía dưới khác ở 16 ca TT và 7 ca RE3. Không gọi hai phương pháp đồng nhất. Phần metric đã giải thích được khối đầu và RR root của M4 trên hai tập này. Khóa `R1_top1_trung_M4_top1` trong K2 chỉ so root đúng/sai ở hạng 1; giữ tên khóa vì file đã ghim. | RR 90/90: C, X; khối đầu, 16/7: X |
| D4 | Dòng 14, 66; STATE | BARO: "một kênh I/O không bất thường vẫn đứng đầu"; "do IQR = 0" | BARO xếp `redis_diskio` đầu ở 30/30 ca. Ở cả 30 ca, median và IQR nền bằng 0, nên điểm bằng max(A) theo **đơn vị gốc** (thang chuẩn hóa bằng 1). Ở 14/30 ca, max(N) > max(A). I/O có bất thường thực hay không: **chưa phân xử**. | C (T-056), X |
| D5 | Dòng 14, 67–68 | TORAI B "dựa trên chuỗi lỗi và độ trễ của trace" nên chọn bên gọi | Cơ chế theo code (`src/torai/torai_sua.py`, đoạn hợp nhất): điểm từng nguồn metric, log, trace_lat, trace_err được chuẩn hóa. Nguồn thiếu được **điền 0 điểm ở modality tương ứng** (không có nghĩa service đã được xác nhận bình thường). Lấy trung bình bốn cột rồi xếp cụm; cụm đầu một service được trả thẳng. Trên RE3 (ba seed): khối đầu là cụm một service ở 90/90 lượt; điểm tính lại khớp khối đầu đã lưu 30/30 (seed 0); root dẫn đầu phần metric ở 27/30; ở 23/26 ca xếp sai, root dẫn metric nhưng thua sau hợp nhất. Thiếu trace của root chưa phải điều kiện đủ để sai (cặp `2b123fa80d`/`83ddf66107`). Nguyên nhân vật lý của triệu chứng phía gọi chưa cô lập. Câu "bên gọi trực tiếp 15/30, root 4/30" (K `#/2_4_baro_torai_RE3/torai_top_vs_root`) vẫn đúng như số đếm. | Code: C, X; các số 90/30/27/23: X |

## 2. Điểm Claude tìm thêm khi rà phần còn lại (Codex chưa kiểm)

| # | Chỗ | Vấn đề | Sửa | Mức |
|---|---|---|---|---|
| D6 | K `#/2_5_vi_tri_N`, các khóa `Nezha-OB|*`/`torai_B` | Ghi MRR 0,0 cho TORAI B trên OB. Thực tế TORAI B có trạng thái `UNSUPPORTED` ở 34/34 ca OB (B `#/rows`, `statuses`), không phải xếp sai. Văn bản báo cáo không dùng số này. | Đọc các ô đó là **không hỗ trợ**, không là MRR 0. Không sửa K vì đã ghim. | KHÔNG CHẶN |
| D7 | Dòng 132 | "Một thống kê đơn lẻ trên metric của chính root là đủ, không cần đồ thị" | Thu về đúng đại lượng: root có số mẫu lệch bền lớn nhất ở 48/60 ca TT và 28/30 ca RE3 (K2 `#/tom_tat/<bộ>/root_events_hon_moi_service_khac`). Ở các ca còn lại, R1 không đủ. Câu này không phải bằng chứng về tác dụng của quan hệ. | KHÔNG CHẶN |
| D8 | Dòng 153 | Phân loại độ khó theo dữ liệu "phản ánh độ khó đúng hơn"; RE3 mức II nhiều "vì baseline trace yếu, không vì ca khó" | Hai cách phân loại đo hai thứ khác nhau; chưa có tiêu chí để gọi cách nào "đúng hơn". Quan sát giữ được: TraceRCA và MicroRank có MRR 0,061 và 0,080 trên RE3 (`results/T-054/reports/re3-ban-cuoi-001/re3-tables.json#/per_case`, lọc P). | KHÔNG CHẶN |
| D10 | Dòng 11, 21 | "Root có span lỗi tăng: 0/30" | Ở 12/30 ca root vắng khỏi trace, nên `root_err_A`/`root_err_N` là rỗng (K `#/2_1_status_span_RE3/theo_ca`), không phải 0. Viết đúng: root không có span lỗi tăng ở **0/18 ca có trace của root**; 12 ca **không quan sát được**. Tương tự cho "lỗi riêng". | KHÔNG CHẶN |
| D9 | Dòng 87 | "M1 mạnh … vì xếp tầng theo kênh của chính root không cần cạnh" | Đây là **ứng viên chưa kiểm**, cùng loại với D1. Trên RE3, M1 và C-a0 cùng MRR 0,925, nên chưa có bằng chứng nhóm vị trí N phụ thuộc vào thành phần quan hệ. Số mỗi nhóm nhỏ (12/18 ca). | KHÔNG CHẶN |

## 3. Không đổi

- Mọi số xếp hạng, K, K2 và các bảng T-054/T-055.
- Kết luận 2.2, 2.3 và vùng 2.5 trong báo cáo; kết luận 2.1 giữ, với cách đếm sửa ở D10. Claude kiểm lại các số 2.1, 2.2, 2.3 (319/2634, 73/273, z khớp 2634/2634 và 273/273), 2.4 và 2.5 khớp K.

## 4. Còn mở

- Phần chung nào của M1/C-a0 tạo lợi thế trước R1 ở 12 ca TT.
- Phân rã chênh M1–C-a0 trên OB thành đóng góp E1/E2/E5 và tương tác.
- OB có "đơn giản" theo nghĩa R1 không (chưa có R1 trên OB thô).
- Bất thường thực của `redis_diskio`; nguyên nhân vật lý của triệu chứng phía gọi ở RE3.
- Hai phân tích ứng viên Codex nêu (RRF/coverage; E5 mất F_I) chưa được duyệt làm.

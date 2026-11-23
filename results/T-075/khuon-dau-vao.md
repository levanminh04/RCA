# T-075 — Khuôn đầu vào W8 (`T075-vao-1`): gói bằng chứng rút gọn

Ngày 23/11/2026. Bản 1. Code: `goi_bang_chung.py`. Phạm vi: Q6, Q7 (DECISIONS 23/11). Chưa gửi gì ra ngoài.

## 1. Nguyên tắc

- Lớp giải thích chỉ **đọc** đầu ra G1 đã có. Không gọi lại lõi, không ghi vào file G1. Vì vậy thứ hạng RCA không đổi theo cấu tạo; K9 kiểm điều này bằng hash file nguồn và bảng hạng trước/sau.
- Gói có hai phần. `gui_di` là phần duy nhất được phép đưa vào LLM. `kiem_toan` giữ ở máy: hash nguồn, con trỏ hash V082, danh sách trường đã loại.
- Mỗi mục trong `gui_di` có `nguon`: con trỏ JSON vào file nguồn. Người đọc lần lại được từ câu giải thích về G1.
- Thời gian là giây tương đối so với mốc t của ca. Ở chế độ (b), mốc này là t̂, giờ bắt đầu của cảnh báo đầu tiên. Gói không chứa giờ tuyệt đối.
- Luật cứng 6: không có sổ tiêm, đáp án, tên ô, đường dẫn hay mã nhận diện ca. `quet_goi` quét khóa cấm và mẫu chữ cấm trước khi trả gói (K8). Phép quét này là heuristic, không thay việc duyệt danh sách trường ở §3.

## 2. Hai nguồn

| Nguồn | Khi dùng | Có gì |
|---|---|---|
| `g1`: file ca G1 0.5 (`du-lieu/<bản>/<ca>.json`), kèm khối `che_do_b` b-1 nếu có | Mặc định khi demo (trang ca W5 đọc đúng file này) | Bảng hạng đầy đủ, bằng chứng theo kênh, kế thừa, vùng, thao tác có cờ. Với `che_do_b`: thêm cảnh báo, độ phủ, số mẫu vào lõi |
| `su_co`: file sự cố của bộ điều phối T-073 | Ca E5 `7577dd5b` ở lượt này. File G1 của ca chưa có trên laptop; Q1 giao T-073 chép về | Kết luận V082, nhóm hạng 1, cảnh báo, độ phủ, số span/log theo thực thể. **Không có** bằng chứng theo kênh |

Với ca `t073-b`, hash đầu ra V082 lấy theo con trỏ `#/du_lieu_loi/v082/output_sha256`. Trong file G1 là `#/che_do_b/du_lieu_loi/v082/output_sha256`. Hash này chỉ nằm trong `kiem_toan`. Gói **không** dùng `ban.ghi_chu_hash` ("Hash do chỉ mục T-064 cấp."): câu này sai với ca `t073-b` (Q6), và vô ích với LLM ở mọi ca.

## 3. Danh sách trường đề xuất gửi đi (chờ Minh duyệt, Q7)

| Khối `gui_di` | Trường | Nguồn | Vì sao cần |
|---|---|---|---|
| `che_do`, `cua_so` | chế độ a/b; nửa nền [−300, 0), nửa sự cố [0, 300); mô tả mốc | hằng số, `su_co` | Để LLM nói đúng "trước/sau mốc" |
| `ket_qua_rca` | bản phương pháp, `ket_luan`, `trang_thai_chay`, `nhom_hang_1`, `xep_hang[]` (`thuc_the`, `hang`, `lop`, `so_kenh_co`) | `#/su_co/ket_luan`, `#/ranking_rows` | Nói lại kết luận và thứ hạng, không đổi |
| `bang_chung[]` (tối đa 20, sắp theo s) | `thuc_the`, `kenh`, `don_vi`, `huong`, `lop`, `diem_s`, `F_I`, `khoi_phat_tuong_doi_s` | `#/bang_chung` | Căn cứ chính của câu giải thích |
| `ke_thua[]` (tối đa 20) | `thuc_the`, `kenh`, `huong`, `duong`, `giai_thich_boi`, `quy_tac`, `trang_thai` | `#/ke_thua` | Giải thích vì sao thực thể có điểm cao vẫn xếp sau |
| `vung` | `T`, `hop_cach_1` | `#/region` | Phạm vi lan |
| `thao_tac_co_co[]` | chủ, tên thao tác, loại, `n_N`, `n_A`, kênh cờ | `#/thao_tac[co_m1]` | Nêu thao tác cụ thể (tên span, câu SQL rút gọn) |
| `canh_xep_hang` | trạng thái, số cạnh | `#/trang_thai_canh` | Nói rõ có hay không có cạnh |
| `canh_bao[]` (chế độ b) | mã luật, tín hiệu, tóm tắt, giây bắt đầu/kết thúc so với t̂ | `che_do_b.canh_bao` | Nói điều gì kích hoạt RCA |
| `do_phu` (chế độ b) | `du_cua_so`, `thieu_bat_buoc`, quy tắc, lỗ lớn nhất của chuỗi thiếu | `che_do_b.du_lieu_loi.phu` | Bắt buộc nêu khi thiếu phủ (K5) |
| `so_mau_vao_loi`, `so_mau_theo_thuc_the` | số span/log/hàng metric theo N, A, theo thực thể | `che_do_b.du_lieu_loi`, bước `kiem_dau_vao` | Quan sát im lặng hoặc tăng giảm lưu lượng |
| `thieu_trong_goi`, `gioi_han` | chuỗi mô tả phần không có | dựng sẵn; `#/gioi_han` | Để LLM biết phần nào vắng |

Dữ liệu gửi đi gồm tên service nội bộ, tên thao tác (có câu SQL như `UPDATE ticket_schema.tbl_tickets`), tên luật cảnh báo và số liệu. Không có log thô, trace ID hay địa chỉ máy. Mặt trái: tên bảng, schema và route nội bộ của FlashTicket vẫn lộ ra nhà cung cấp. Nếu Minh muốn giảm, có thể bỏ `thao_tac_co_co` (mất mức chi tiết thao tác) hoặc đổi tên service sang bí danh rồi đổi lại ở máy (thêm một bước ánh xạ, có thể sai).

## 4. Trường loại khỏi `gui_di`

| Trường | Lý do |
|---|---|
| `ca`, `ma_ca_m1`, `su_co.ma`, `ma` (sự cố) | Mã nhận diện ca, không cần cho giải thích |
| `nguon_ca`, `nguon_cua_so`, `ban.nguon_output`, mọi `path`/`file`/`directory`/`chon_file` | Đường dẫn và tên lượt, có thể mang thông tin chiến dịch hoặc ô (luật cứng 6) |
| `ban.ghi_chu_hash` | Sai với ca `t073-b` (Q6) |
| `ban.sha256_output`, `ban.cau_hinh_*`, `sha256_than`, `spool_seq`, `nhan_webhook_utc` | Hash và số hiệu nội bộ; giữ ở `kiem_toan` |
| `cua_so_ms`, `tu_utc`, `den_loai_tru`, mọi giờ tuyệt đối | Thay bằng giây tương đối |
| `lien_ket[*]`, `metric_links`, `canh_bao[*].nhan.http_url` | URL nội bộ Grafana và địa chỉ đầu dò |
| `thao_tac[*].vi_du`, `canh_thao_tac`, `don_vi_m1` | Trace ID/span ID; khối lớn (hàng trăm mục) không cần cho mức demo |
| `entity_ranking[*].key` | Khóa số nội bộ của lõi; LLM dễ diễn giải sai từng thành phần |
| bước `p7` trong file sự cố | Đầu ra P7, không phải V082; dễ lẫn hai bản |
| `phat_lai` | Có thể mang khối đối chiếu đáp án |

## 5. Khi nào gói "không đủ bằng chứng"

`kiem_w8.phai_khong_du` là quy tắc tất định trên gói, không nhờ LLM. Gói được coi là không đủ khi có một trong ba điều kiện:

- `ket_luan` khác `CAUSE_FOUND`;
- `trang_thai_chay` khác `OK`;
- không mục `bang_chung` nào thuộc nhóm hạng 1.

Khi đó đầu ra phải trả `KHONG_DU_BANG_CHUNG` (K4). Gói E5 lấy từ file sự cố rơi vào điều kiện cuối, vì nguồn này không có bằng chứng theo kênh.

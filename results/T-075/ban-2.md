# T-075 — Bản 2: sửa theo CX-30, CX-30b (23/11/2026)

Bản 1 giữ nguyên, hash ở `SHA256SUMS`. Bản 2 nằm trong các file mới; hash ở `SHA256SUMS-2`. Lượt này vẫn ngoại tuyến: không gọi LLM, không gửi dữ liệu ra ngoài.

| Bản 2 | Thay bản 1 | Nội dung |
|---|---|---|
| `goi_bang_chung_2.py` | `goi_bang_chung.py` | Khuôn gói `T075-vao-2` |
| `kiem_w8_2.py` | `kiem_w8.py` | Bộ kiểm `T075-kiem-2`, khuôn đầu ra `T075-ra-2` |
| `viet_mau_2.py` | `ca-thu/*/dau-ra-*.json` | 8 đầu ra viết tay, ghi ra `ca-thu-2/` |
| `chay_thu_2.py` | `chay_thu.py` | 20 đầu ra sinh có chủ đích, đối chứng chéo, K8, K9 |
| `ket-qua-thu-2.json` | `ket-qua-thu.json` | Kết quả máy của bản 2 |

Chạy lại:

```
py -3 -I -B -X utf8 viet_mau_2.py
py -3 -I -B -X utf8 chay_thu_2.py
```

## 1. Gói `T075-vao-2`

So với `khuon-dau-vao.md`, gói bản 2 khác ở năm điểm:

- **Trạng thái chạy chỉ lấy từ V082 (R2, N1 tự soát).** Nhánh file sự cố không có trạng thái V082. Vì vậy `trang_thai_chay = null`, và `nguon_trang_thai` ghi rõ là không có. Theo quy tắc ở §3, gói khi đó bị coi là không đủ.
- **Ghi rõ phạm vi P7 cơ sở (R2).**
  - Khối `so_mau_vao_loi` đổi tên thành `so_mau_dau_vao_p7_co_so`, có thêm trường `pham_vi`. Hàng metric tách thành hai phần: trong cửa sổ (`N`, `A`) và ngoài cửa sổ.
  - `do_phu.pham_vi` ghi: phép phủ tính trên đầu vào P7 cơ sở, không gồm kênh liveness bổ sung.
  - `so_mau_theo_thuc_the.pham_vi` ghi tương tự.
  - Giới hạn D3 lấy từ `che_do_b.gioi_han` (nửa nền có thể chứa phần đầu sự cố) được thêm vào `gioi_han`.
- **Bỏ `canh_bao[].tom_tat` (R5).** Đây là chữ tự do của chú thích luật, mà K8 không bảo đảm được. Gói chỉ giữ mã luật, tín hiệu và thời gian tương đối.
- **Bằng chứng: sắp F_I = 1 trước, rồi theo s, trước khi cắt 20 mục (R4).** Nhờ vậy kênh tạo hạng không bị cắt. Ghi chú trong `ket_qua_rca` giải thích nghĩa của F_I.
- **`thao_tac_co_co[].kenh_co` chỉ giữ tên, hướng, F_I, điểm s.** Bỏ `khoi_phat` vì đó là giờ tuyệt đối (tự soát lượt này).

Danh sách trường đề xuất gửi đi (`khuon-dau-vao.md` §3) cập nhật theo các điểm trên. Quyết định danh sách và quyền gửi vẫn thuộc Minh (Q7).

## 2. Khuôn đầu ra `T075-ra-2` và bộ kiểm `T075-kiem-2`

- **Khuôn:** mục `thieu_bang_chung` có thêm khóa tùy chọn `vang`, là danh sách con trỏ mà mục đó khai là vắng. Các phần khác giữ như `T075-ra-1`.
- **Kết quả kiểm:** bộ kiểm trả `{hop_khuon, loi}`.
  - `hop_khuon = false` nghĩa là sai khuôn. Thông báo phù hợp khi đó là "Không tạo được giải thích hợp lệ" (R3).
  - "Không đủ bằng chứng" chỉ dùng khi có căn cứ về bằng chứng của ca.

| Mã | Đổi gì | Điểm |
|---|---|---|
| K0 (mới) | Kiểm đúng tập khóa và kiểu ở mọi cấp. Câu phải có ít nhất 3 từ. Đầu vào lạ thì trả sai khuôn, không sập | R3c, N2 tự soát |
| K2 | So kiểu JSON chặt: `false` khác `0` | CX-30b N2 |
| K4 | Ràng buộc theo **trạng thái đầu ra** ở mọi gói. `KHONG_DU_BANG_CHUNG`: không `suy_luan`, không `giam_thieu`, có mục thiếu. `GIAI_THICH`: gói phải đủ, có ≥ 1 gợi ý, và có ≥ 1 khẳng định trích `/bang_chung/<i>` là kênh F_I = 1 của nhóm hạng 1 | R3a, R3b, R4 |
| K4b | Chỉ kiểm con trỏ trong `vang`: mỗi con trỏ phải ra giá trị rỗng/null. Trích bảng có dữ liệu để làm bối cảnh vẫn được | CX-30b N3 |
| K5 | Phải có một **mục thiếu** trích `/do_phu/du_cua_so` hoặc `/do_phu/thieu_bat_buoc…`. Chỉ trích ở câu khác không đủ | CX-30b N1 |

### Quy tắc "đủ bằng chứng" bản 2 — **ứng viên, chưa có mục WHY**

Gói được coi là đủ khi cả ba điều sau đều đúng:

- `ket_luan = CAUSE_FOUND`;
- `trang_thai_chay = OK`;
- **mọi** thực thể nhóm hạng 1 có ≥ 1 mục bằng chứng F_I = 1 trong gói.

Căn cứ: lõi xếp tầng hạng đầu theo kênh F_I = 1 (`src/m1/xep_hang.py`).

Quy tắc này sai trong hai trường hợp:

- **Nhánh H5 của V082:** thực thể "chết im" được đẩy lên đầu mà không qua kênh F_I (`src/m1_ft/thanh_phan/h4_h5.py`). Ca như vậy sẽ bị coi là không đủ. Đây là hướng thận trọng, và chưa có ca thử nào.
- **Gói thiếu thông tin H5:** gói hiện không có trường H5, nên lớp giải thích không nói được lý do này.

Muốn dùng làm luật chính thức, cần Minh duyệt một mục WHY.

## 3. Kết quả thử bản 2

Số liệu từ `ket-qua-thu-2.json`:

- `#/tong`: **28** đầu ra (**8** viết tay, **20** sinh), cả **28** khớp mong đợi khai trong `chay_thu_2.py`.
- K8, K9 đạt.
- `#/doi_chung_cheo`: **49** cặp chéo, **0** cặp lọt. Giờ `#/tong/dat` có tính cả cặp chéo lọt (R6).

| Ca | Nguồn | `phai_khong_du` |
|---|---|---|
| `e5-su-co` | file sự cố E5 | có (không có trạng thái V082, không có bằng chứng) |
| `e5-g1` | G1 đầy đủ E5 `results/T-073/e5/ca-7577dd5b/…/7577dd5b.json`, hash khớp `ca-7577dd5b.SHA256SUMS` | không |
| `cu-1`, `cu-2` | như bản 1 | không / có |
| `gia-1`…`gia-3` | như bản 1 (dựng từ `cu-1`) | có / có / không |
| `gia-4` (mới) | `e5-g1`, bỏ hai mục F_I = 1 của booking-service | có |

Các phản ví dụ của Codex đều được tái hiện thành đầu ra sinh, và bộ kiểm bắt đúng mã:

| Phản ví dụ | Bắt được |
|---|---|
| R3a | K4 |
| R3b | K4 |
| R3c (`null`) | sai khuôn |
| R4 (`gia-4`) | K4 |
| N1 | K5 |
| N2 | K2 |

Câu đúng của N3 (trích bảng có dữ liệu làm bối cảnh) **đạt**.

**Ca E5 (`e5-su-co`).** Mẫu đúng giờ dẫn riêng số span và log của Payment cùng quy ước khóa vắng, và viết "sáu nguồn metric cơ sở thiếu phủ" kèm phạm vi P7 cơ sở. Tên hai luật được dẫn bằng cả đối tượng cảnh báo.

**Ca E5 (`e5-g1`).** Mẫu `GIAI_THICH` dẫn hai kênh SQL F_I = 1 của booking-service, kế thừa lan ngược ở api-gateway, và nêu thiếu phủ ở mục thiếu.

Hai mẫu E5 do người làm viết khi đã biết ô của lượt E5. Chúng chỉ để thử bộ kiểm, không phải bằng chứng chất lượng.

## 4. Đề xuất sửa (thay các mục tương ứng ở `de-xuat-minh.md`; file cũ giữ nguyên)

- **§1 Trường gửi đi:** như `khuon-dau-vao.md` §3, cộng các thay đổi ở §1 của file này. Không gửi `canh_bao.tom_tat`.
- **§3 Khi trượt:**
  - Gọi lại một lần, kèm danh sách lỗi.
  - Nếu vẫn trượt **K0** (sai khuôn): hiện "Không tạo được giải thích hợp lệ".
  - Nếu trượt K2–K7: cũng hiện thông báo trên, kèm mã lỗi.
  - Chỉ hiện "Không đủ bằng chứng" khi `phai_khong_du` = đúng, hoặc khi đầu ra hợp lệ tự trả trạng thái đó.
  - Rút câu "demo không bao giờ hiện câu bịa". Bộ kiểm so chữ, không bảo đảm được điều đó.
- **§4 File G1 ca E5:** đã có trên laptop từ 05:31:40Z (LOG T-073), và đã dùng trong bản 2. Giữ ca `e5-su-co` để minh họa trường hợp thiếu bằng chứng.
- **Phạm vi dữ liệu Q7 (CX-30 mục 2):** Q7 ghi "kiểm trích dẫn ngoại tuyến bằng ca giả". Lượt 1 và lượt 2 dùng thêm nguồn thật trên laptop: E5 (file sự cố, G1) và hai ca G1 dev cũ. Không dữ liệu nào ra ngoài.
  - **Đề xuất:** Minh xác nhận được tính các nguồn thật này vào phần thử ngoại tuyến. SPEC đã nêu "ca có sẵn" và "ca W5".
  - **Mặt trái:** nếu Minh chỉ chấp nhận ca giả, kết quả trên nguồn thật chỉ là tham khảo, và nghiệm thu Q7 dựa trên `gia-1`…`gia-4`. Các ca này vẫn dựng từ ca thật.

# T-075 — Kết quả thử bộ kiểm ngoại tuyến (lượt 1, 23/11/2026)

Lệnh: `py -3 -I -X utf8 chay_thu.py` (chạy trong `results/T-075/`). Số liệu lấy từ `ket-qua-thu.json`; con trỏ ghi ở từng dòng.

**Không gọi LLM.** Mọi "đầu ra LLM" ở đây đều do người làm viết tay, hoặc là đầu ra đúng bị làm hỏng có chủ đích bằng hàm `dot_bien` trong `chay_thu.py`. Kết quả này chỉ cho biết bộ kiểm có bắt được các lỗi đã định hay không. Nó **không** đo chất lượng giải thích của LLM.

## 1. Ca thử

| Ca | Nguồn | `phai_khong_du` | Ghi chú |
|---|---|---|---|
| `e5` | `results/T-073/e5/su-co/bbc0a6d44f.json` (ca thật E5, chế độ b) | có | Gói từ file sự cố: không có bằng chứng theo kênh |
| `cu-1` | `results/T-065/may-l11/du-lieu/V082-V066+H8a/1e5a3dc5.json` (G1 0.5, chế độ a, dev) | không | Có 2 mục bằng chứng, 1 mục kế thừa |
| `cu-2` | `…/729604d2.json` (G1 0.5, chế độ a, dev) | có | `NO_INTRINSIC_ANOMALY`, 0 bằng chứng |
| `gia-1` | `cu-1`, cắt `bang_chung`, `ke_thua`, `thao_tac_co_co` | có | Mô phỏng thiếu tín hiệu |
| `gia-2` | `cu-1`, đổi `ket_luan` thành `INSUFFICIENT_EVIDENCE` | có | |
| `gia-3` | `cu-1`, thêm `do_phu.du_cua_so = false` | không | Thử K5 |

Hai ca cũ được chọn vì chúng nhỏ và phủ hai nhánh (có nguyên nhân, kèm kế thừa / không có bất thường). Lý do này không dính tới đáp án; người làm không đọc nhãn của các ca này. Ca giả chỉ sửa ở tầng gói, không sửa file nguồn.

`#/ca/*/K8_goi_sach`: cả 6 gói đều sạch khóa và chữ cấm.

## 2. Đầu ra và mã bộ kiểm bắt

`#/tong`: 18/18 đầu ra cho kết quả khớp mong đợi khai trước trong `chay_thu.py` (`MONG_DOI` và `dot_bien`).

| Ca | Đầu ra | Mong đợi | Bắt được |
|---|---|---|---|
| e5 | dung | đạt | đạt |
| e5 | sai-doi-hang (nói payment-service mới là hạng 1) | K4, K6 | K4, K5, K6 |
| cu-1 | dung | đạt | đạt |
| cu-1 | sinh-sai-con-tro | K2 | K2, K3, K3b |
| cu-1 | sinh-sai-gia-tri | K2 | K2 |
| cu-1 | sinh-sai-thuc-the | K3 | K3 |
| cu-1 | sinh-sai-so | K3b | K3b |
| cu-1 | sinh-sai-hang | K6 | K6 |
| cu-1 | sinh-sai-cam ("sổ tiêm") | K7 | K7 |
| cu-1 | sinh-sai-khong-trich | K1 | K1, K3 |
| cu-2 | dung | đạt | đạt |
| cu-2 | sai-bia-nguyen-nhan | K4 | K4 |
| gia-1 | dung | đạt | đạt |
| gia-1 | sinh-sai-giai-thich-bia (đầu ra đúng của cu-1) | K2, K4 | K2, K3, K3b, K4 |
| gia-2 | dung | đạt | đạt |
| gia-2 | sinh-sai-giai-thich-bia | K2, K4 | K2, K4 |
| gia-3 | sinh-dung | đạt | đạt |
| gia-3 | sinh-sai-bo-do-phu | K5 | K2, K5 |

Ở cột "Bắt được", các mã thêm ngoài mong đợi đều là hệ quả của cùng một lỗi. Ví dụ: khi con trỏ không tồn tại, giá trị trích bị rỗng, nên K3/K3b cũng báo.

## 3. Ba thuộc tính của SPEC

| Thuộc tính (SPEC) | Phép kiểm | Kết quả trên ca thử |
|---|---|---|
| Giải thích chỉ dựa trên gói | K1–K3b, K7 | Các đầu ra đúng đều đạt. Mọi đầu ra sai có chủ đích đều bị bắt (§2) |
| Trả "không đủ bằng chứng" khi thiếu | K4, K4b; ca `gia-1`, `gia-2`, `cu-2`, `e5` | Đạt. Giải thích bịa trên gói đã cắt bị bắt (K4). Câu nói "không có bằng chứng" trên gói có bằng chứng bị bắt (K4b, §4) |
| Không đổi thứ hạng RCA | K6 (đầu ra), K9 (nguồn) | `#/K9`: với 3 nguồn, hash trước = sau, bảng hạng trước = sau, bảng hạng trong gói = nguồn. Đầu ra đổi hạng bị K6 bắt |

## 4. Tự kiểm: kết quả lượt đầu quá đẹp

Lượt chạy đầu đạt 18/18, nên người làm thêm đối chứng chéo: lấy đầu ra đúng của ca X kiểm trên gói ca Y, với X ≠ Y. Đầu ra như vậy phải trượt.

- **Lượt đầu:** 2/30 cặp lọt (`gia-1->cu-1`, `gia-1->gia-2`). Đầu ra viết "gói không có bằng chứng", trích nguyên khối `/bang_chung`, nhưng gói thực ra có bằng chứng. Bộ kiểm khi đó không bắt được, vì `KHONG_DU_BANG_CHUNG` được phép trên gói đủ.
- **Sửa:** thêm K4b. Mục "thiếu" trích nguyên khối `/bang_chung` hay `/ke_thua` làm căn cứ vắng mặt thì khối đó phải rỗng.
- **Sau sửa:** `#/doi_chung_cheo/dat_ngoai_y_muon` = []. Không còn cặp nào lọt; 18/18 vẫn khớp.

## 5. Điều chưa biết

- **Chưa thử với LLM thật.** Chưa biết model có giữ đúng khuôn, trích dẫn và quy tắc K4 hay không, cũng chưa biết tỷ lệ trượt.
- **Đầu ra mẫu ca E5 do người làm viết.** Người làm biết ô của lượt E5 (đọc `e5-ket-qua.md`, `bang-o-e5.md`), nên câu chữ mẫu có thể vô tình thiên theo đáp án. Câu chỉ nêu quan sát có trong gói và qua K1–K7. Mẫu này không dùng làm bằng chứng về chất lượng.
- **Bộ kiểm so chữ, không hiểu nghĩa** (`khuon-dau-ra.md` §3). Một câu sai suy luận nhưng đúng chữ vẫn qua.
- **Ca E5 chưa có giải thích đầy đủ.** Ca này chạy trên gói từ file sự cố. Cần file G1 của ca (`de-xuat-minh.md` §4).
- **Hai ca G1 cũ là chế độ (a).** Khối `che_do_b` trong file G1 chưa được thử qua nhánh `g1`. Đường đọc `che_do_b` dùng chung hàm `_phan_b` với nhánh `su_co`, nhưng nhánh `g1` + `che_do_b` chưa chạy trên file thật. Khối `che_do_b` mà `g1_b.py` ghi có thể khác file sự cố ở tên khóa; cần kiểm khi có file G1 của E5.

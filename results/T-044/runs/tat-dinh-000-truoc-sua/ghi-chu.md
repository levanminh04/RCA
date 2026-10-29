# Lượt xáo hàng đầu tiên (hỏng), dựng lại để lưu

- Lệnh: `M1_XAO=1 python -B -m pytest -q -p no:cacheprovider` trên bản sao tạm của repo với `src/m1/e2.py`, `src/m1/e5.py` ở commit 4a052745 (trước khi sửa), mọi file khác như lượt `tat-dinh-001`.
- Kết quả: 6 trượt (`pytest-x1.txt`, `pytest-x1.json`).
  - `test_phu_dinh[9, 11, 12, 13]`, `test_E2C_gan_ben_duoc_goi`: `e2.gan_canh` trả `gan` theo thứ tự đầu vào; xáo đầu vào thì thứ tự danh sách đổi, nội dung từng cạnh không đổi.
  - `test_hai_pha_hash_on_dinh`: `e5.phan_loai` duyệt kênh của bên giải thích theo thứ tự đầu vào, nên thứ tự các mục `inherited_by` cùng một kênh đổi; F_I không đổi; hash pha 1 đổi.
- Sửa: `gan_canh` sắp cạnh theo (bên gọi, bên được gọi); `phan_loai` sắp kênh theo mã trước khi duyệt. Sau sửa: `runs/tat-dinh-001` PASS.

# Bổ sung tối thiểu ngoài 9 file H2 — chưa áp dụng

Khi nối toàn tuyến, adapter CIRCA đã khóa trả hai bản ghi `ols+rht_da` và `ols+rht`. Nhưng bộ nhận và bộ tạo TIMEOUT chỉ khai hai bản ghi cho RE2-TT. Giữ nguyên sẽ làm output CIRCA RE3 bị từ chối, hoặc tạo timeout thiếu vế phụ. Không được bỏ bản ghi phụ để lách hợp đồng.

Đề xuất bổ sung đúng hai file, ba điều kiện:

1. `results/T-054/scripts/dieu_phoi.py`: ở phép kiểm `expected_variants`, thay điều kiện `arm == 'circa' and dataset == 'RE2-TT'` bằng `arm == 'circa' and dataset in ('RE2-TT', 'RE3-OB')`. Ở phép kiểm `circa_current` áp dụng cùng điều kiện để RE3 cũng kiểm mốc thật. Không thay điều kiện Nezha.
2. `results/T-054/scripts/bien_nhan.py`: ở `finalize_timeout`, điều kiện tạo hai variant CIRCA thay tương tự để RE3 đủ hai bản ghi TIMEOUT. Không nới phân loại lỗi, deadline hoặc quyền dữ liệu.

Ảnh hưởng: chỉ nhận/kiểm hai bản ghi CIRCA RE3 và bảo toàn hai vế khi timeout đủ điều kiện. TT giữ nguyên, Nezha giữ nguyên, các baseline khác giữ nguyên. SPEC/WHY/DECISIONS ghi bổ sung quyền và lý do này trước sửa; các file ấy đã nằm trong gói tài liệu H2.

Kiểm bằng fixture: CIRCA RE3 đủ hai vế được nhận; thiếu/thừa/sai variant hoặc current bị bác; TIMEOUT đủ điều kiện sinh đúng hai vế; TT/Nezha giữ hành vi tham chiếu. Chưa chạy CIRCA trên dữ liệu đo RE3 hoặc thay chính sách lỗi phương pháp. Chưa sửa hai file này.

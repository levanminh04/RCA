# Kiểm tuyến laptop lô 5 (WHY-96) — 14/11/2026 11:52–11:56Z

5 cặp (bản, ca) đã có đầu ra `exp-obs` chạy lại trên laptop (x86, `py312-pin`, cùng cây mã `b0f79a4d…`, gói bổ sung trùng hash `exp-obs`).
Hai lần chạy trên laptop trùng SHA ở 5/5, nhưng `method-output-1.json` **lệch byte** so với `exp-obs` ở 5/5:

| Cặp | Khác biệt |
|---|---|
| P7 × 659a9dfb1ab0 (so đầu ra phiên B) | chữ số cuối của số thực (vd. 3.67671485539628 / 3.6767148553962805) ở khóa xếp hạng, T4c |
| V013 × e9c9679b | như trên, thêm `p_len` cổng đếm (8.475779264267387e-109 / …397e-109); `ma_nguon_sha256` khác vì bản `exp-obs` chạy ở cây mã cũ |
| V061 × 46aab4be, V018 × 60166807, V002 × 98ea5ba4 | lệch byte (cùng loại, chưa liệt kê từng trường) |

Thứ tự thực thể và nhóm hòa trùng ở hai cặp đã soi. Nguyên nhân khả dĩ: thư viện số học (libm/numpy) khác giữa x86 và ARM ở bit cuối. Theo điều kiện khai trước trong WHY-96, **bỏ tuyến laptop**; mọi cặp lô 5 chạy trên `exp-obs`. Đầu ra ở đây chỉ là lịch sử, không dùng chấm.

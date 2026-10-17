# Bộ dựng từ bản ghi có nguồn và bộ đối chiếu

Hợp đồng ở `results/T-036/hop-dong.md`; registry ban đầu ở `results/T-036/nguon.json`. Hai API thuần không đọc file, không tải nguồn và không nhận nhãn:

```python
from do_thi_tinh import build, compare, project
entity, operation = build(document, registry)
result = compare(entity, trace_entity, mappings, context, registry)
partial_projection = project(operation)
```

Đặt `src` trong Python path tại runner. Python 3.12, chỉ standard library cho mã tĩnh. Kiểm tích hợp T-035 dùng môi trường hiện có `D:/RCA-ext/envs/py312-pin/Scripts/python.exe` vì bộ dựng trace dùng pandas/numpy. Luôn `-X utf8 -B` để không tạo bytecode ngoài phạm vi. Không cần cài gói hoặc thay môi trường.

`build` trả inventory và graph thực thể; graph thao tác giữ component_context và bảng phần không có operation. Resource binding và signal address là lớp có nguồn riêng, chưa là cạnh runtime của T-035. `compare` yêu cầu graph trace T-035 v2.1 đã kiểm manifest ở runner, mapping có nguồn kể cả identity, cùng context miền/revision. Kết quả tách so đầu mút và kiểu; có tập, thành viên gốc, loại trừ và mẫu số. Không sửa graph trace.

Chạy checker bằng tên run mới, không chạy lại tên cũ:

```powershell
& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-036/check.py <run-moi>
```

Checker giữ cả exception/đầu ra lỗi trong run mới, kiểm oracle literal đã có trước code và tính xác định. Đọc `kiem-dung-dan.md` cùng JSON trong run. Không chạy lại `fixtures/define.py` trên fixture đã tồn tại. Fixture là dữ liệu giả kiểm hợp đồng, chưa là graph FlashTicket hay đối chiếu đủ TT/OB. Các task sau phải dẫn từng quan hệ nguồn, xác minh mapping và giữ giới hạn revision. Đọc `ban-giao.md` trước dùng P6/P9.

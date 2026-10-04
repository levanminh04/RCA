# Lượt fixture 001 không hợp lệ cho kết luận PC

Lượt 001 giữ nguyên cùng seed và inputs đã chốt, nhưng bộ ghi CI `RecordCI` có lỗi deepcopy. CausalGraph được deepcopy trong bước định hướng; `__getattr__` của recorder truy cập `base` chưa được phục hồi, gây RecursionError. Đây là lỗi instrumentation của T-014, không phải lỗi thuật toán PC. Bằng chứng ở các JSON traceback và console001.

Đã sửa bằng truy cập attribute không đệ quy và `__deepcopy__` explicit. Lượt002 giữ seed, sample count, dữ liệu và mọi cấu hình. Không chọn một bộ dữ liệu khác để đạt PASS. Các JSON/NPZ/progress/console lượt001 được giữ. Exception duplicate-singular ở bước Fisher-Z trước deepcopy phải được kiểm lại trong lượt002 trước khi dùng làm bằng chứng.

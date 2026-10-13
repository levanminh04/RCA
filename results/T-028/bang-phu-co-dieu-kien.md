# Bảng có điều kiện và đánh dấu độ nhạy có sẵn

Nguồn mọi số: `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `circa_dev19_conditional`, `nezha_saved_sensitivity_flags`; nguồn gốc và hash ở bước 1. CIRCA tái dùng evidence dev30; Nezha không có đặc trưng/gán mới cho view phụ.

## CIRCA dev19

| k | Cohort | Đúng OK | Sai OK | Primary |
| --- | --- | --- | --- | --- |
| 1 | 19 | 13 | 6 | {'M0': 4, 'M5': 2} |
| 5 | 19 | 16 | 3 | {'M0': 3} |

Danh sách ca lỗi làm tròn bị loại giữ nguyên trong `circa_dev19_conditional.excluded_confirmed_rounding11`; không thay mẫu chính.

## Nezha view phụ

| View | Phương pháp | Dấu ca | Ngoài cohort | Đổi status | Đổi Hit1 | Đổi Hit5 |
| --- | --- | --- | --- | --- | --- | --- |
| sensitivity_A | BARO | 22 | 0 | 0 | 1 | 0 |
| sensitivity_A | CIRCA OLS+RHT+DA | 22 | 0 | 0 | 0 | 0 |
| sensitivity_A | MicroRank full | 22 | 0 | 0 | 0 | 0 |
| sensitivity_A | SimpleRCA | 22 | 0 | 0 | 0 | 1 |
| sensitivity_A | TORAI B | 22 | 0 | 0 | 0 | 0 |
| sensitivity_A | TraceRCA | 22 | 0 | 0 | 1 | 0 |
| sensitivity_B | BARO | 22 | 1 | 0 | 0 | 0 |
| sensitivity_B | CIRCA OLS+RHT+DA | 22 | 1 | 0 | 0 | 0 |
| sensitivity_B | MicroRank full | 22 | 1 | 0 | 0 | 0 |
| sensitivity_B | SimpleRCA | 22 | 1 | 0 | 0 | 0 |
| sensitivity_B | TORAI B | 22 | 1 | 0 | 0 | 0 |
| sensitivity_B | TraceRCA | 22 | 1 | 0 | 0 | 0 |
| trace_guard | BARO | 22 | 0 | 0 | 0 | 0 |
| trace_guard | CIRCA OLS+RHT+DA | 22 | 0 | 0 | 0 | 0 |
| trace_guard | MicroRank full | 22 | 0 | 1 | 0 | 1 |
| trace_guard | SimpleRCA | 22 | 0 | 0 | 0 | 0 |
| trace_guard | TORAI B | 22 | 0 | 0 | 0 | 0 |
| trace_guard | TraceRCA | 22 | 0 | 0 | 2 | 3 |

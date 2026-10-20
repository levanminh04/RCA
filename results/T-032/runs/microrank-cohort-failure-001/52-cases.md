# MicroRank — bảng 52 ca tại checkpoint FAIL_STOP

Nguồn đã kiểm hash hai đầu: `transport-check.json`; bảng máy đọc `cohort/52-cases.json#/rows`.
Không tăng ngưỡng, không bỏ ca lỗi. `not_run` chưa có kết quả; dấu “—” là không có phép so số, không phải lệch bằng 0. Ca ERROR khớp trạng thái nhưng không có cặp điểm để tính ULP/tương đối.

| Dataset | Mẫu số | Exact | Chỉ lệch số | Đổi operation | Đổi service | Blocked | Chưa chạy |
|---|---:|---:|---:|---:|---:|---:|---:|
| RE2-TT | 30 | 2 | 5 | 2 | 0 | 1 | 20 |
| Nezha-OB | 22 | 1 | 0 | 0 | 0 | 0 | 21 |

| Dataset | Ca | Trạng thái nguồn | Loại kiểm | ULP lớn nhất | Tương đối lớn nhất |
|---|---|---|---|---:|---:|
| RE2-TT | dev-03d4910932 | ERROR | exact | — | — |
| RE2-TT | dev-12a1a88069 | OK | operation_order | 9 | 1.4669745929577803e-15 |
| RE2-TT | dev-14372e1209 | OK | numeric_only | 8 | 1.1858866486411286e-15 |
| RE2-TT | dev-16597725c1 | OK | operation_order | 2 | 2.8717545525138048e-16 |
| RE2-TT | dev-16870e660c | ERROR | exact | — | — |
| RE2-TT | dev-1e6d61b5ec | OK | numeric_only | 4 | 5.8921860370368715e-16 |
| RE2-TT | dev-20acb4402d | OK | numeric_only | 1 | 1.171868011256556e-16 |
| RE2-TT | dev-260d332c8d | OK | numeric_only | 16 | 2.0187204240419735e-15 |
| RE2-TT | dev-3ae0a6c15a | OK | numeric_only | 10 | 1.2416943301026496e-15 |
| RE2-TT | dev-3defe3d34b | OK | blocked | 41 | 4.7311184080068693e-15 |
| RE2-TT | dev-4e68956051 | ERROR | not_run | — | — |
| RE2-TT | dev-4f8a844308 | OK | not_run | — | — |
| RE2-TT | dev-57546fd87b | OK | not_run | — | — |
| RE2-TT | dev-59f696a169 | OK | not_run | — | — |
| RE2-TT | dev-746fd74313 | OK | not_run | — | — |
| RE2-TT | dev-7f1b6b071d | OK | not_run | — | — |
| RE2-TT | dev-8017c6dc70 | OK | not_run | — | — |
| RE2-TT | dev-98bc73c499 | OK | not_run | — | — |
| RE2-TT | dev-a505ab3f65 | OK | not_run | — | — |
| RE2-TT | dev-a5cabe5fa7 | ERROR | not_run | — | — |
| RE2-TT | dev-a915aa2424 | OK | not_run | — | — |
| RE2-TT | dev-b8bd0abf60 | OK | not_run | — | — |
| RE2-TT | dev-ba831dbeb8 | OK | not_run | — | — |
| RE2-TT | dev-bcbd4f46ae | OK | not_run | — | — |
| RE2-TT | dev-db293894ab | OK | not_run | — | — |
| RE2-TT | dev-de89e2f9e9 | OK | not_run | — | — |
| RE2-TT | dev-f36d0647d5 | OK | not_run | — | — |
| RE2-TT | dev-f81f88234e | OK | not_run | — | — |
| RE2-TT | dev-f9a8e05ed7 | OK | not_run | — | — |
| RE2-TT | dev-fbc45b0c67 | OK | not_run | — | — |
| Nezha-OB | dev-14701a3bbb | OK | exact | 0 | 0 |
| Nezha-OB | dev-1ac905bc95 | OK | not_run | — | — |
| Nezha-OB | dev-27252dca60 | OK | not_run | — | — |
| Nezha-OB | dev-2bfc97b01e | OK | not_run | — | — |
| Nezha-OB | dev-396c8dbf7d | OK | not_run | — | — |
| Nezha-OB | dev-3b92690644 | OK | not_run | — | — |
| Nezha-OB | dev-3e27669440 | OK | not_run | — | — |
| Nezha-OB | dev-515c5f2190 | OK | not_run | — | — |
| Nezha-OB | dev-5467884de4 | OK | not_run | — | — |
| Nezha-OB | dev-55f99f3e0a | OK | not_run | — | — |
| Nezha-OB | dev-5ada15752d | OK | not_run | — | — |
| Nezha-OB | dev-607751ac0a | OK | not_run | — | — |
| Nezha-OB | dev-63c30faf34 | OK | not_run | — | — |
| Nezha-OB | dev-6c9afc9822 | OK | not_run | — | — |
| Nezha-OB | dev-70629373f9 | OK | not_run | — | — |
| Nezha-OB | dev-7b7c973198 | OK | not_run | — | — |
| Nezha-OB | dev-7d3c2fe6d1 | OK | not_run | — | — |
| Nezha-OB | dev-8ecd9880ed | OK | not_run | — | — |
| Nezha-OB | dev-95e164235f | OK | not_run | — | — |
| Nezha-OB | dev-9b9397a4dc | OK | not_run | — | — |
| Nezha-OB | dev-9fd793feb7 | OK | not_run | — | — |
| Nezha-OB | dev-b0f8b2e3ac | OK | not_run | — | — |

Ngưỡng đã duyệt: đồng thời ≤16 ULP và ≤16×2^-52 tương đối; không absolute floor.
Ca dev-3defe3d34b vượt ngưỡng số. Native–observed, thứ tự/hòa service và Hit@1..10 đã khớp; T-028 bridge chưa chạy cho ca lỗi. Không dùng trung gian ca lỗi làm bằng chứng và không chạy A′.
Phần này là tiến độ kiểm phát lại; chưa xác định nguyên nhân drift, partition lịch sử hoặc cơ chế RCA.

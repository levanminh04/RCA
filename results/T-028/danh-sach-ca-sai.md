# Danh sách ca sai — bước 1 T-028

Chỉ trích số đã chấm; nguồn tổng hợp: `results/T-028/runs/danh-sach-001/step1.json`. Không tính đặc trưng hoặc gán cơ chế.

Ca sai OK@k: status OK và Hit@k kỳ vọng <1. Non-OK báo riêng. Mức trượt kỳ vọng gồm non-OK có Hit=0, không phải số ca sai. TORAI gộp seed theo ca. Số thập phân trong bảng làm tròn sáu chữ số; JSON giữ số nguồn.

## Bảng chính

| Dataset | Phương pháp | Tổng ca | OK sai@1 | OK sai@5 | Non-OK | Mức trượt@1 | @5 | Nguồn |
|---|---|---:|---:|---:|---|---:|---:|---|
| RE2-TT | baro | 30 | 9 | 4 | 0 | 9 | 4 | `results/T-024/cham-a.json` `/methods/baro/summaries/dev30/main` |
| RE2-TT | simplerca | 30 | 5 | 1 | 0 | 5 | 1 | `results/T-024/cham-a.json` `/methods/simplerca/summaries/dev30/main` |
| RE2-TT | microrank_full | 30 | 24 | 13 | 4 ERROR | 28 | 17 | `results/T-024/cham-a.json` `/methods/microrank_full/summaries/dev30/main` |
| RE2-TT | tracerca | 30 | 5 | 1 | 4 ERROR | 9 | 5 | `results/T-024/cham-a.json` `/methods/tracerca/summaries/dev30/main` |
| RE2-TT | circa_ols_da | 30 | 14 | 3 | 0 | 14 | 3 | `results/T-024/cham-a.json` `/methods/circa_ols_da/summaries/dev30/main` |
| RE2-TT | torai_B | 30 | 4 | 0 | 0 | 4 | 0 | `results/T-024/cham-a.json` `/methods/torai_B/summaries/dev30/main` |
| Nezha-OB | baro | 22 | 14 | 6 | 0 | 14 | 6 | `results/T-026/cham-a.json` `/tables/main/methods/baro/summary/main` |
| Nezha-OB | simplerca | 22 | 15 | 4 | 0 | 15 | 3.500000 | `results/T-026/cham-a.json` `/tables/main/methods/simplerca/summary/main` |
| Nezha-OB | microrank_full | 22 | 22 | 14 | 0 | 22 | 14 | `results/T-026/cham-a.json` `/tables/main/methods/microrank_full/summary/main` |
| Nezha-OB | tracerca | 22 | 20 | 11 | 0 | 19.666667 | 10.500000 | `results/T-026/cham-a.json` `/tables/main/methods/tracerca/summary/main` |
| Nezha-OB | circa_ols_da | 22 | 0 | 0 | 22 UNSUPPORTED | 22 | 22 | `results/T-026/cham-a.json` `/tables/main/methods/circa_ols_da/summary/main` |
| Nezha-OB | torai_B | 22 | 0 | 0 | 22 UNSUPPORTED | 22 | 22 | `results/T-026/cham-a.json` `/tables/main/methods/torai_B/summary/main` |

CIRCA/TORAI Nezha UNSUPPORTED: chỉ giữ trạng thái và quy tắc mẫu số nguồn, không là kết quả chất lượng xếp hạng hoặc bằng chứng thiếu tín hiệu root.

## Mã ca sai OK và non-OK

### RE2-TT — baro

Nguồn: `results/T-024/cham-a.json` `/methods/baro/summaries/dev30/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-14372e1209`, `dev-16597725c1`, `dev-57546fd87b`, `dev-59f696a169`, `dev-746fd74313`, `dev-a5cabe5fa7`, `dev-a915aa2424`, `dev-f36d0647d5`, `dev-f81f88234e`.
- Sai OK@5: `dev-57546fd87b`, `dev-a5cabe5fa7`, `dev-a915aa2424`, `dev-f81f88234e`.

### RE2-TT — simplerca

Nguồn: `results/T-024/cham-a.json` `/methods/simplerca/summaries/dev30/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-20acb4402d`, `dev-7f1b6b071d`, `dev-a505ab3f65`, `dev-a915aa2424`, `dev-fbc45b0c67`.
- Sai OK@5: `dev-20acb4402d`.

### RE2-TT — microrank_full

Nguồn: `results/T-024/cham-a.json` `/methods/microrank_full/summaries/dev30/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-12a1a88069`, `dev-14372e1209`, `dev-16597725c1`, `dev-1e6d61b5ec`, `dev-20acb4402d`, `dev-260d332c8d`, `dev-3ae0a6c15a`, `dev-3defe3d34b`, `dev-4f8a844308`, `dev-59f696a169`, `dev-746fd74313`, `dev-7f1b6b071d`, `dev-8017c6dc70`, `dev-98bc73c499`, `dev-a505ab3f65`, `dev-a915aa2424`, `dev-b8bd0abf60`, `dev-ba831dbeb8`, `dev-bcbd4f46ae`, `dev-db293894ab`, `dev-de89e2f9e9`, `dev-f36d0647d5`, `dev-f9a8e05ed7`, `dev-fbc45b0c67`.
- Sai OK@5: `dev-12a1a88069`, `dev-16597725c1`, `dev-1e6d61b5ec`, `dev-20acb4402d`, `dev-260d332c8d`, `dev-3defe3d34b`, `dev-59f696a169`, `dev-746fd74313`, `dev-7f1b6b071d`, `dev-8017c6dc70`, `dev-a915aa2424`, `dev-db293894ab`, `dev-f36d0647d5`.
- ERROR: `dev-03d4910932`, `dev-16870e660c`, `dev-4e68956051`, `dev-a5cabe5fa7`.

### RE2-TT — tracerca

Nguồn: `results/T-024/cham-a.json` `/methods/tracerca/summaries/dev30/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-12a1a88069`, `dev-20acb4402d`, `dev-260d332c8d`, `dev-db293894ab`, `dev-f36d0647d5`.
- Sai OK@5: `dev-260d332c8d`.
- ERROR: `dev-03d4910932`, `dev-16870e660c`, `dev-4e68956051`, `dev-a5cabe5fa7`.

### RE2-TT — circa_ols_da

Nguồn: `results/T-024/cham-a.json` `/methods/circa_ols_da/summaries/dev30/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-03d4910932`, `dev-16597725c1`, `dev-3ae0a6c15a`, `dev-4e68956051`, `dev-4f8a844308`, `dev-57546fd87b`, `dev-746fd74313`, `dev-98bc73c499`, `dev-a505ab3f65`, `dev-a915aa2424`, `dev-b8bd0abf60`, `dev-ba831dbeb8`, `dev-f36d0647d5`, `dev-f81f88234e`.
- Sai OK@5: `dev-16597725c1`, `dev-57546fd87b`, `dev-f81f88234e`.

### RE2-TT — torai_B

Nguồn: `results/T-024/cham-a.json` `/methods/torai_B/summaries/dev30/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-16597725c1`, `dev-59f696a169`, `dev-a5cabe5fa7`, `dev-f36d0647d5`.
- Sai OK@5: không có.

### Nezha-OB — baro

Nguồn: `results/T-026/cham-a.json` `/tables/main/methods/baro/summary/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-1ac905bc95`, `dev-27252dca60`, `dev-2bfc97b01e`, `dev-3b92690644`, `dev-5467884de4`, `dev-55f99f3e0a`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-7b7c973198`, `dev-8ecd9880ed`, `dev-9b9397a4dc`, `dev-9fd793feb7`.
- Sai OK@5: `dev-1ac905bc95`, `dev-27252dca60`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-8ecd9880ed`.

### Nezha-OB — simplerca

Nguồn: `results/T-026/cham-a.json` `/tables/main/methods/simplerca/summary/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-1ac905bc95`, `dev-396c8dbf7d`, `dev-3b92690644`, `dev-515c5f2190`, `dev-5467884de4`, `dev-55f99f3e0a`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-7b7c973198`, `dev-8ecd9880ed`, `dev-9b9397a4dc`, `dev-9fd793feb7`, `dev-b0f8b2e3ac`.
- Sai OK@5: `dev-1ac905bc95`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`.

### Nezha-OB — microrank_full

Nguồn: `results/T-026/cham-a.json` `/tables/main/methods/microrank_full/summary/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-14701a3bbb`, `dev-1ac905bc95`, `dev-27252dca60`, `dev-2bfc97b01e`, `dev-396c8dbf7d`, `dev-3b92690644`, `dev-3e27669440`, `dev-515c5f2190`, `dev-5467884de4`, `dev-55f99f3e0a`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-70629373f9`, `dev-7b7c973198`, `dev-7d3c2fe6d1`, `dev-8ecd9880ed`, `dev-95e164235f`, `dev-9b9397a4dc`, `dev-9fd793feb7`, `dev-b0f8b2e3ac`.
- Sai OK@5: `dev-14701a3bbb`, `dev-2bfc97b01e`, `dev-396c8dbf7d`, `dev-3b92690644`, `dev-55f99f3e0a`, `dev-607751ac0a`, `dev-6c9afc9822`, `dev-70629373f9`, `dev-7b7c973198`, `dev-7d3c2fe6d1`, `dev-8ecd9880ed`, `dev-95e164235f`, `dev-9fd793feb7`, `dev-b0f8b2e3ac`.

### Nezha-OB — tracerca

Nguồn: `results/T-026/cham-a.json` `/tables/main/methods/tracerca/summary/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: `dev-14701a3bbb`, `dev-1ac905bc95`, `dev-27252dca60`, `dev-2bfc97b01e`, `dev-396c8dbf7d`, `dev-3b92690644`, `dev-3e27669440`, `dev-515c5f2190`, `dev-5467884de4`, `dev-55f99f3e0a`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-70629373f9`, `dev-7b7c973198`, `dev-7d3c2fe6d1`, `dev-8ecd9880ed`, `dev-95e164235f`, `dev-b0f8b2e3ac`.
- Sai OK@5: `dev-27252dca60`, `dev-2bfc97b01e`, `dev-3b92690644`, `dev-5467884de4`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-70629373f9`, `dev-7b7c973198`, `dev-8ecd9880ed`, `dev-95e164235f`.

### Nezha-OB — circa_ols_da

Nguồn: `results/T-026/cham-a.json` `/tables/main/methods/circa_ols_da/summary/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: không có.
- Sai OK@5: không có.
- UNSUPPORTED: `dev-14701a3bbb`, `dev-1ac905bc95`, `dev-27252dca60`, `dev-2bfc97b01e`, `dev-396c8dbf7d`, `dev-3b92690644`, `dev-3e27669440`, `dev-515c5f2190`, `dev-5467884de4`, `dev-55f99f3e0a`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-70629373f9`, `dev-7b7c973198`, `dev-7d3c2fe6d1`, `dev-8ecd9880ed`, `dev-95e164235f`, `dev-9b9397a4dc`, `dev-9fd793feb7`, `dev-b0f8b2e3ac`.

### Nezha-OB — torai_B

Nguồn: `results/T-026/cham-a.json` `/tables/main/methods/torai_B/summary/main`; từng bản ghi/seed và exception ở `main_rows` của `results/T-028/runs/danh-sach-001/step1.json`.

- Sai OK@1: không có.
- Sai OK@5: không có.
- UNSUPPORTED: `dev-14701a3bbb`, `dev-1ac905bc95`, `dev-27252dca60`, `dev-2bfc97b01e`, `dev-396c8dbf7d`, `dev-3b92690644`, `dev-3e27669440`, `dev-515c5f2190`, `dev-5467884de4`, `dev-55f99f3e0a`, `dev-5ada15752d`, `dev-607751ac0a`, `dev-63c30faf34`, `dev-6c9afc9822`, `dev-70629373f9`, `dev-7b7c973198`, `dev-7d3c2fe6d1`, `dev-8ecd9880ed`, `dev-95e164235f`, `dev-9b9397a4dc`, `dev-9fd793feb7`, `dev-b0f8b2e3ac`.

## CIRCA dev19 — dòng có điều kiện

Nguồn: `results/T-024/cham-a.json` `/methods/circa_ols_da/summaries/dev19/main` và `circa_dev19_conditional` trong `results/T-028/runs/danh-sach-001/step1.json`. Không thay dev30.

- k=1: 6/19 ca sai OK; mức trượt 6; mã: `dev-16597725c1`, `dev-57546fd87b`, `dev-746fd74313`, `dev-a915aa2424`, `dev-f36d0647d5`, `dev-f81f88234e`.
- k=5: 3/19 ca sai OK; mức trượt 3; mã: `dev-16597725c1`, `dev-57546fd87b`, `dev-f81f88234e`.
- Nhóm ca lỗi làm tròn đã xác nhận được giữ nguyên ở `excluded_confirmed_rounding11` của JSON; không suy nó giải thích mọi thất bại CIRCA.

## Nezha: dấu đổi từ số đã lưu

Nguồn: `nezha_saved_sensitivity_flags` trong `results/T-028/runs/danh-sach-001/step1.json`; mỗi dấu trỏ tới `results/T-026/cham-a.json` và bản ghi nguồn. Không có đặc trưng hoặc cơ chế cho các view này.

| View | Phương pháp | Ca included | Không thuộc cohort | Đổi status | Đổi Hit@1 | Đổi Hit@5 |
|---|---|---:|---:|---:|---:|---:|
| sensitivity_A | baro | 22 | 0 | 0 | 1 | 0 |
| sensitivity_A | simplerca | 22 | 0 | 0 | 0 | 1 |
| sensitivity_A | microrank_full | 22 | 0 | 0 | 0 | 0 |
| sensitivity_A | tracerca | 22 | 0 | 0 | 1 | 0 |
| sensitivity_A | circa_ols_da | 22 | 0 | 0 | 0 | 0 |
| sensitivity_A | torai_B | 22 | 0 | 0 | 0 | 0 |
| sensitivity_B | baro | 21 | 1 | 0 | 0 | 0 |
| sensitivity_B | simplerca | 21 | 1 | 0 | 0 | 0 |
| sensitivity_B | microrank_full | 21 | 1 | 0 | 0 | 0 |
| sensitivity_B | tracerca | 21 | 1 | 0 | 0 | 0 |
| sensitivity_B | circa_ols_da | 21 | 1 | 0 | 0 | 0 |
| sensitivity_B | torai_B | 21 | 1 | 0 | 0 | 0 |
| trace_guard | baro | 22 | 0 | 0 | 0 | 0 |
| trace_guard | simplerca | 22 | 0 | 0 | 0 | 0 |
| trace_guard | microrank_full | 22 | 0 | 1 | 0 | 1 |
| trace_guard | tracerca | 22 | 0 | 0 | 2 | 3 |
| trace_guard | circa_ols_da | 22 | 0 | 0 | 0 | 0 |
| trace_guard | torai_B | 22 | 0 | 0 | 0 | 0 |

## Kiểm bước 1

`runs/danh-sach-001/validation.json`: đối chiếu đúng tập ca/status/seed/hash nguồn và đẳng thức Σ(1−Hit)=n·(1−Hit bảng). `runs/danh-sach-001/progress.jsonl`: thời gian từng pha. Các trường evidence/mechanisms trong `results/T-028/runs/danh-sach-001/step1.json` còn null, trạng thái pending_codebook.

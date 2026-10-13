# Proxy P95 của root và caller — T-028

Nguồn mọi số: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → records. Mỗi bản ghi trỏ seed/case và mỗi dòng trỏ aggregate theo native service. Báo mọi ca/seed đã lưu: root và mọi proper ancestor, gồm caller chưa chắc chắn trước root và ca đúng. Không tính lại tín hiệu hoặc gộp P95 qua native service.

SimpleRCA dùng start; các phương pháp khác dùng end theo codebook §3.3. P95 là duration span (μs), không phải end-to-end latency. τ2/3/4 giữ nguyên; không chia nền bằng 0. BARO/TORAI dùng trace làm bối cảnh, không phải tín hiệu native. Non-OK giữ status; số raw có được cũng không là chất lượng phương pháp. Caller N/A khi quan hệ không khả dụng; không đổi thành không có caller.

## RE2-TT / BARO / dev-03d4910932 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/0`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/0/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / BARO / dev-12a1a88069 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/1`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/1/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / BARO / dev-14372e1209 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/2`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/2/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / BARO / dev-16597725c1 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/3`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/3/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / BARO / dev-16870e660c / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/4`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/4/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / BARO / dev-1e6d61b5ec / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/5`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/5/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / BARO / dev-20acb4402d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/6`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/6/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / BARO / dev-260d332c8d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/7`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/7/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / BARO / dev-3ae0a6c15a / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/8`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/8/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / BARO / dev-3defe3d34b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/9`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/9/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / BARO / dev-4e68956051 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/10`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/10/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / BARO / dev-4f8a844308 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/11`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/11/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / BARO / dev-57546fd87b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/12`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/12/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / BARO / dev-59f696a169 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/13`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/13/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / BARO / dev-746fd74313 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/14`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/14/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / BARO / dev-7f1b6b071d / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/15`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/15/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / BARO / dev-8017c6dc70 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/16`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/16/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / BARO / dev-98bc73c499 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/17`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/17/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / BARO / dev-a505ab3f65 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/18`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/18/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / BARO / dev-a5cabe5fa7 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/19`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/19/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | True | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / BARO / dev-a915aa2424 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/20`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/20/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | True | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | True | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | True | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | True | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / BARO / dev-b8bd0abf60 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/21`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/21/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / BARO / dev-ba831dbeb8 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/22`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/22/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / BARO / dev-bcbd4f46ae / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/23`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/23/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / BARO / dev-db293894ab / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/24`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/24/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / BARO / dev-de89e2f9e9 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/25`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/25/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / BARO / dev-f36d0647d5 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/26`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/26/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | True | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / BARO / dev-f81f88234e / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/27`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/27/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / BARO / dev-f9a8e05ed7 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/28`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/28/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / BARO / dev-fbc45b0c67 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/29`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/29/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-03d4910932 / seed single

Root `ts-route-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/30`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/30/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14518 | 13393 | 18395.8 | 77260.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10258 | 9490 | 47189.8 | 116752 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9416 | 8348 | 47256 | 114853 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / SimpleRCA / dev-12a1a88069 / seed single

Root `ts-order-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/31`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/31/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15427 | 14889 | 57213.7 | 57452.2 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-14372e1209 / seed single

Root `ts-route-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/32`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/32/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13735 | 13780 | 38885 | 69277.4 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9718 | 9678 | 51606.8 | 114524 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8332 | 9776 | 67403.6 | 183552 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / SimpleRCA / dev-16597725c1 / seed single

Root `ts-auth-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/33`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/33/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / SimpleRCA / dev-16870e660c / seed single

Root `ts-route-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/34`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/34/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6287 | 5747 | 45278.8 | 79408.4 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14954 | 13650 | 49716 | 207135 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-1e6d61b5ec / seed single

Root `ts-order-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/35`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/35/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / SimpleRCA / dev-20acb4402d / seed single

Root `ts-order-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/36`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/36/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | True | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-260d332c8d / seed single

Root `ts-order-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/37`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/37/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-3ae0a6c15a / seed single

Root `ts-train-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/38`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/38/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14465 | 13504 | 17236 | 55055.2 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6937 | 6395 | 50377.8 | 72971.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10194 | 9556 | 49864.9 | 93806 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15121 | 15011 | 54060 | 95213 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-3defe3d34b / seed single

Root `ts-auth-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/39`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/39/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / SimpleRCA / dev-4e68956051 / seed single

Root `ts-train-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/40`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/40/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14021 | 10409 | 28391 | 638592 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9886 | 7350 | 46021.8 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14723 | 10814 | 48409.5 | 654735 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-4f8a844308 / seed single

Root `ts-route-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/41`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/41/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5557 | 5218 | 44859.8 | 120891 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12731 | 12221 | 48165 | 251630 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-57546fd87b / seed single

Root `ts-auth-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/42`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/42/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / SimpleRCA / dev-59f696a169 / seed single

Root `ts-auth-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/43`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/43/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / SimpleRCA / dev-746fd74313 / seed single

Root `ts-auth-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/44`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/44/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / SimpleRCA / dev-7f1b6b071d / seed single

Root `ts-travel-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/45`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/45/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | True | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17087 | 16505 | 51765.7 | 52017.8 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-8017c6dc70 / seed single

Root `ts-order-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/46`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/46/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-98bc73c499 / seed single

Root `ts-train-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/47`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/47/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6637 | 6333 | 45822 | 70177.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14830 | 14470 | 48918.8 | 73675.3 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-a505ab3f65 / seed single

Root `ts-train-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/48`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/48/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13452 | 10332 | 17553.7 | 644207 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 269 | 177 | 562942 | 4.17226e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9504 | 7306 | 52921.1 | 654673 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8932 | 6505 | 57113.7 | 660280 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / SimpleRCA / dev-a5cabe5fa7 / seed single

Root `ts-travel-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/49`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/49/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 16973 | 17071 | 51627.8 | 51592 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-a915aa2424 / seed single

Root `ts-travel-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/50`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/50/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | True | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-b8bd0abf60 / seed single

Root `ts-route-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/51`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/51/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13620 | 13059 | 42440.5 | 93271.1 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9612 | 9252 | 54088.4 | 119010 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8850 | 7744 | 57366.8 | 121990 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / SimpleRCA / dev-ba831dbeb8 / seed single

Root `ts-train-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/52`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/52/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14948 | 14565 | 46665.2 | 77121.4 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-bcbd4f46ae / seed single

Root `ts-route-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/53`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/53/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6265 | 6367 | 50832.4 | 77495.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15230 | 14380 | 58284.8 | 111801 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-db293894ab / seed single

Root `ts-travel-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/54`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/54/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-de89e2f9e9 / seed single

Root `ts-travel-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/55`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/55/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-f36d0647d5 / seed single

Root `ts-order-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/56`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/56/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-f81f88234e / seed single

Root `ts-auth-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/57`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/57/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-f9a8e05ed7 / seed single

Root `ts-travel-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/58`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/58/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / SimpleRCA / dev-fbc45b0c67 / seed single

Root `ts-train-service`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/59`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/59/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-03d4910932 / seed single

Root `ts-route-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/60`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/60/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | None | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | None | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | None | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | None | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | None | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | None | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | None | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | None | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / MicroRank full / dev-12a1a88069 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/61`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/61/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-14372e1209 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/62`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/62/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / MicroRank full / dev-16597725c1 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/63`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/63/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / MicroRank full / dev-16870e660c / seed single

Root `ts-route-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/64`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/64/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | None | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | None | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | None | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | None | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | None | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | None | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | None | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | None | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-1e6d61b5ec / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/65`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/65/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / MicroRank full / dev-20acb4402d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/66`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/66/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-260d332c8d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/67`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/67/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-3ae0a6c15a / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/68`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/68/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-3defe3d34b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/69`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/69/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / MicroRank full / dev-4e68956051 / seed single

Root `ts-train-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/70`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/70/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | None | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | None | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | None | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | None | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | None | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | None | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | None | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | None | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-4f8a844308 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/71`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/71/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-57546fd87b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/72`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/72/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / MicroRank full / dev-59f696a169 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/73`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/73/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / MicroRank full / dev-746fd74313 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/74`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/74/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / MicroRank full / dev-7f1b6b071d / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/75`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/75/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-8017c6dc70 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/76`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/76/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-98bc73c499 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/77`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/77/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-a505ab3f65 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/78`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/78/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / MicroRank full / dev-a5cabe5fa7 / seed single

Root `ts-travel-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/79`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/79/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | None | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | None | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | None | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | None | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | None | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-a915aa2424 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/80`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/80/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-b8bd0abf60 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/81`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/81/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / MicroRank full / dev-ba831dbeb8 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/82`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/82/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-bcbd4f46ae / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/83`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/83/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-db293894ab / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/84`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/84/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-de89e2f9e9 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/85`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/85/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-f36d0647d5 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/86`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/86/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-f81f88234e / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/87`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/87/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-f9a8e05ed7 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/88`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/88/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / MicroRank full / dev-fbc45b0c67 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/89`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/89/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-03d4910932 / seed single

Root `ts-route-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/90`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/90/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | None | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | None | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | None | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | None | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | None | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | None | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | None | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | None | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / TraceRCA / dev-12a1a88069 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/91`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/91/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-14372e1209 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/92`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/92/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / TraceRCA / dev-16597725c1 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/93`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/93/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / TraceRCA / dev-16870e660c / seed single

Root `ts-route-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/94`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/94/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | None | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | None | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | None | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | None | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | None | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | None | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | None | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | None | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-1e6d61b5ec / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/95`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/95/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / TraceRCA / dev-20acb4402d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/96`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/96/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-260d332c8d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/97`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/97/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | True | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-3ae0a6c15a / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/98`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/98/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-3defe3d34b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/99`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/99/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / TraceRCA / dev-4e68956051 / seed single

Root `ts-train-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/100`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/100/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | None | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | None | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | None | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | None | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | None | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | None | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | None | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | None | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-4f8a844308 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/101`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/101/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-57546fd87b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/102`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/102/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / TraceRCA / dev-59f696a169 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/103`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/103/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / TraceRCA / dev-746fd74313 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/104`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/104/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / TraceRCA / dev-7f1b6b071d / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/105`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/105/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-8017c6dc70 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/106`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/106/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-98bc73c499 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/107`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/107/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-a505ab3f65 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/108`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/108/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / TraceRCA / dev-a5cabe5fa7 / seed single

Root `ts-travel-service`; status `ERROR`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'non_OK'}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/109`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/109/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | None | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | None | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | None | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | None | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | None | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | None | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-a915aa2424 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/110`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/110/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-b8bd0abf60 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/111`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/111/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / TraceRCA / dev-ba831dbeb8 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/112`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/112/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-bcbd4f46ae / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/113`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/113/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-db293894ab / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/114`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/114/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-de89e2f9e9 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/115`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/115/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-f36d0647d5 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/116`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/116/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-f81f88234e / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/117`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/117/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-f9a8e05ed7 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/118`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/118/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / TraceRCA / dev-fbc45b0c67 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/119`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/119/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-03d4910932 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/120`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/120/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-12a1a88069 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/121`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/121/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-14372e1209 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/122`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/122/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-16597725c1 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/123`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/123/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-16870e660c / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/124`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/124/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-1e6d61b5ec / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/125`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/125/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-20acb4402d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/126`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/126/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-260d332c8d / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/127`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/127/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-3ae0a6c15a / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/128`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/128/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-3defe3d34b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/129`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/129/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-4e68956051 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/130`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/130/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-4f8a844308 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/131`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/131/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-57546fd87b / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/132`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/132/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-59f696a169 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/133`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/133/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-746fd74313 / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/134`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/134/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-7f1b6b071d / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/135`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/135/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-8017c6dc70 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/136`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/136/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-98bc73c499 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/137`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/137/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-a505ab3f65 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/138`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/138/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-a5cabe5fa7 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/139`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/139/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-a915aa2424 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/140`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/140/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-b8bd0abf60 / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/141`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/141/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-ba831dbeb8 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/142`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/142/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | True | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | True | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | True | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-bcbd4f46ae / seed single

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/143`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/143/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-db293894ab / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/144`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/144/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-de89e2f9e9 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/145`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/145/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-f36d0647d5 / seed single

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/146`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/146/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-f81f88234e / seed single

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/147`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/147/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-f9a8e05ed7 / seed single

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/148`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/148/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / CIRCA OLS+RHT+DA / dev-fbc45b0c67 / seed single

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/149`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/149/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-03d4910932 / seed 0

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/150`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/150/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-03d4910932 / seed 1

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/151`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/150/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-03d4910932 / seed 2

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/152`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/150/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 135 | 138028 | 984263 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14516 | 13395 | 18443.8 | 77252.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 611 | 646 | 46524 | 114109 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 123 | 479455 | 741230 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 156 | 458260 | 730037 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6903 | 6355 | 42078.4 | 78199.6 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10256 | 9492 | 47191.8 | 116749 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9414 | 8350 | 47239.2 | 115082 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15403 | 14589 | 48913.2 | 119967 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-12a1a88069 / seed 0

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/153`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/151/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-12a1a88069 / seed 1

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/154`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/151/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-12a1a88069 / seed 2

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/155`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/151/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 169816 | 176922 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 664 | 739 | 47343.5 | 46585.9 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 290 | 153 | 54817.3 | 90987.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 183 | 151 | 554648 | 627376 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 183 | 199 | 567454 | 738113 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6436 | 6398 | 56685.8 | 69409.4 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 231 | 47270.5 | 165456 | True | True | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8001 | 8338 | 60463 | 74600.5 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15425 | 14891 | 57202.6 | 57463 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-14372e1209 / seed 0

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/156`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/152/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-14372e1209 / seed 1

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/157`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/152/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-14372e1209 / seed 2

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/158`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/152/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 141 | 206638 | 1.18976e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13734 | 13781 | 38857.8 | 69277 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 692 | 717 | 55955.9 | 510383 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 187 | 111 | 565258 | 1.18636e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 201 | 262 | 517084 | 1.2857e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6490 | 6636 | 59601.7 | 105602 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9716 | 9680 | 51608.8 | 114520 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8330 | 9778 | 67338.4 | 183781 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15189 | 13897 | 56030 | 197273 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-16597725c1 / seed 0

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/159`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/153/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-16597725c1 / seed 1

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/160`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/153/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-16597725c1 / seed 2

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/161`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/153/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2085 | 1994 | 328295 | 938884 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-16870e660c / seed 0

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/162`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/154/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-16870e660c / seed 1

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/163`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/154/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-16870e660c / seed 2

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/164`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/154/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 135 | 144 | 153973 | 1.10822e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13400 | 12182 | 15403 | 67657.6 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 653 | 636 | 46049.6 | 337961 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 129 | 87 | 473499 | 891601 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 197 | 193 | 462177 | 1.00147e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6285 | 5749 | 45261 | 79397.2 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9518 | 8642 | 46911.9 | 110921 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7935 | 7451 | 49347.7 | 152177 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14949 | 13655 | 49711 | 207342 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-1e6d61b5ec / seed 0

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/165`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/155/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-1e6d61b5ec / seed 1

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/166`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/155/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-1e6d61b5ec / seed 2

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/167`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/155/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 236 | 167 | 27452.5 | 100090 | True | True | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 50 | 64 | 26956.6 | 103027 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-20acb4402d / seed 0

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/168`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/156/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-20acb4402d / seed 1

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/169`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/156/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-20acb4402d / seed 2

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/170`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/156/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 234 | 271 | 18793 | 212267 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 88 | 15512.6 | 214065 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-260d332c8d / seed 0

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/171`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/157/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-260d332c8d / seed 1

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/172`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/157/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-260d332c8d / seed 2

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/173`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/157/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 206 | 219 | 18527.5 | 213391 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 64 | 78 | 14433.9 | 342171 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-3ae0a6c15a / seed 0

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/174`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/158/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-3ae0a6c15a / seed 1

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/175`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/158/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-3ae0a6c15a / seed 2

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/176`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/158/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 138 | 138 | 171799 | 428515 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14463 | 13506 | 17258 | 55052 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 745 | 731 | 44449.4 | 45378.5 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 150 | 151 | 535636 | 665613 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 177 | 155 | 519543 | 658592 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6935 | 6397 | 50378.7 | 72969.8 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 10192 | 9558 | 49865.9 | 93795.2 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9665 | 8166 | 53151.4 | 74504.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15115 | 15017 | 53981.3 | 95291.6 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-3defe3d34b / seed 0

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/177`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/159/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-3defe3d34b / seed 1

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/178`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/159/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-3defe3d34b / seed 2

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/179`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/159/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2105 | 2085 | 161529 | 401617 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-4e68956051 / seed 0

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/180`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/160/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-4e68956051 / seed 1

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/181`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/160/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-4e68956051 / seed 2

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/182`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/160/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15780 | 11574 | 4223 | 405062 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 99 | 154896 | 6.55525e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14019 | 10411 | 26414.6 | 638590 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 853 | 470 | 45774 | 45062.4 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 142 | 77 | 472650 | 4.13143e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 248 | 141 | 457524 | 4.09157e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6680 | 4940 | 44270 | 648833 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9884 | 7352 | 46023.5 | 647611 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9385 | 6926 | 47516 | 652192 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14721 | 10816 | 48396 | 654726 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-4f8a844308 / seed 0

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/183`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/161/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-4f8a844308 / seed 1

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/184`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/161/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-4f8a844308 / seed 2

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/185`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/161/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 137 | 144195 | 1.34203e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 11714 | 11092 | 15038.4 | 71977.8 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 721 | 506 | 42052 | 304391 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 89 | 118 | 479216 | 1.33858e+06 | True | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 222 | 151 | 481652 | 1.29467e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 5555 | 5220 | 44865.7 | 120863 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 8276 | 7854 | 44943.5 | 114401 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7625 | 6877 | 47734.2 | 178234 | True | True | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 12729 | 12223 | 48155.2 | 252559 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-57546fd87b / seed 0

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/186`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/162/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-57546fd87b / seed 1

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/187`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/162/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-57546fd87b / seed 2

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/188`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/162/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2065 | 1995 | 393143 | 799459 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-59f696a169 / seed 0

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/189`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/163/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-59f696a169 / seed 1

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/190`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/163/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-59f696a169 / seed 2

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/191`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/163/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-746fd74313 / seed 0

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/192`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/164/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-746fd74313 / seed 1

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/193`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/164/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-746fd74313 / seed 2

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/194`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/164/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 1792 | 1608 | 140291 | 530416 | True | True | False | available / None |

## RE2-TT / TORAI B / dev-7f1b6b071d / seed 0

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/195`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/165/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-7f1b6b071d / seed 1

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/196`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/165/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-7f1b6b071d / seed 2

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/197`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/165/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 147 | 122 | 158506 | 1.12456e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 747 | 748 | 46455.5 | 219024 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 109 | 209 | 502642 | 508436 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 251 | 167 | 503777 | 1.17541e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7487 | 6895 | 46958.1 | 216418 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 17081 | 16511 | 51698 | 52056.5 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-8017c6dc70 / seed 0

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/198`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/166/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-8017c6dc70 / seed 1

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/199`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/166/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-8017c6dc70 / seed 2

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/200`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/166/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 74 | 60 | 17164.4 | 89815.8 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-98bc73c499 / seed 0

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/201`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/167/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-98bc73c499 / seed 1

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/202`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/167/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-98bc73c499 / seed 2

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/203`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/167/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 150 | 147 | 143192 | 406713 | True | False | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13988 | 13398 | 18349.4 | 42357.8 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 790 | 725 | 42450.3 | 42167.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 68 | 481235 | 643686 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 311 | 257 | 466798 | 574873 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6635 | 6335 | 45822 | 70176.7 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9872 | 9486 | 45295.4 | 70237 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9288 | 8681 | 48652.3 | 72927 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14826 | 14474 | 48905 | 73694.7 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-a505ab3f65 / seed 0

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/204`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/168/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-a505ab3f65 / seed 1

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/205`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/168/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-a505ab3f65 / seed 2

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/206`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/168/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15280 | 11329 | 4819 | 405502 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 87 | 173638 | 6.64978e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13450 | 10334 | 17559.2 | 644197 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 809 | 609 | 46449 | 46172.8 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 99 | 79 | 569007 | 4.19734e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 267 | 179 | 563180 | 4.17096e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6382 | 4904 | 56265.3 | 660397 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9502 | 7308 | 52922.3 | 654672 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8930 | 6507 | 57092.5 | 660275 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14339 | 11124 | 58905.2 | 664516 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-a5cabe5fa7 / seed 0

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/207`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/169/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-a5cabe5fa7 / seed 1

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/208`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/169/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-a5cabe5fa7 / seed 2

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/209`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/169/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 150 | 135 | 157160 | 1.34199e+06 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 884 | 883 | 48044.9 | 222650 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 143 | 207 | 489110 | 505936 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 308 | 256 | 480377 | 1.21221e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 7404 | 7168 | 45119.8 | 219462 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 16971 | 17073 | 51625 | 51600.4 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-a915aa2424 / seed 0

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/210`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/170/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-a915aa2424 / seed 1

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/211`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/170/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-a915aa2424 / seed 2

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/212`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/170/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 158618 | 802895 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 841 | 780 | 44258 | 221495 | True | True | True | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 166 | 210 | 558274 | 531840 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 242 | 289 | 529368 | 1.39056e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6892 | 6981 | 53477.9 | 222420 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15890 | 15317 | 56102.6 | 56882 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-b8bd0abf60 / seed 0

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/213`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/171/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-b8bd0abf60 / seed 1

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/214`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/171/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-b8bd0abf60 / seed 2

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/215`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/171/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 138 | 173427 | 1.17183e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13618 | 13061 | 42434 | 93113 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 710 | 673 | 45892.2 | 117522 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 123 | 193 | 611642 | 962671 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 230 | 89 | 641486 | 931589 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6478 | 6195 | 62999.8 | 137940 | True | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9610 | 9254 | 54064.5 | 119009 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8848 | 7746 | 57268.7 | 122002 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14490 | 14619 | 63482.5 | 146145 | True | False | False | available / None |

## RE2-TT / TORAI B / dev-ba831dbeb8 / seed 0

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/216`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/172/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-ba831dbeb8 / seed 1

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/217`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/172/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-ba831dbeb8 / seed 2

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/218`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/172/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 144 | 146860 | 500574 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13930 | 13892 | 14980.4 | 44831.6 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 827 | 763 | 44285.8 | 44286.2 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 121 | 166 | 459601 | 629680 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 229 | 291 | 447273 | 592697 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6608 | 6603 | 42615.9 | 72260.9 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9855 | 9782 | 43560.5 | 73581.7 | False | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9101 | 9227 | 46107 | 76311.1 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 14946 | 14567 | 46659.8 | 77138 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-bcbd4f46ae / seed 0

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/219`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/173/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-bcbd4f46ae / seed 1

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/220`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/173/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-bcbd4f46ae / seed 2

Root `ts-route-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/221`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/173/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-route-service / ts-route-service | False | N/A | None | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 144 | 132 | 210083 | 787051 | True | True | False | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 13368 | 13404 | 39844.7 | 71554.7 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 784 | 762 | 56858.2 | 109895 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 140 | 124 | 562063 | 672150 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 187 | 240 | 533043 | 646172 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6264 | 6368 | 50819.6 | 77570 | False | False | False | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9498 | 9468 | 52457.1 | 114305 | True | False | False | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 7814 | 8657 | 54286.5 | 92513.2 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15228 | 14382 | 58176 | 112061 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-db293894ab / seed 0

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/222`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/174/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-db293894ab / seed 1

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/223`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/174/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-db293894ab / seed 2

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 6. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/224`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/174/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 8757 | 9245 | 56447 | 120461 | True | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 141 | 170851 | 527715 | True | True | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 668 | 648 | 48306.9 | 115476 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 186 | 131 | 495176 | 495097 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 133 | 293 | 500541 | 1.11879e+06 | True | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | False | 6666 | 6561 | 50044.2 | 113228 | True | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | False | 15253 | 14273 | 50084 | 50450.2 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-de89e2f9e9 / seed 0

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/225`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/175/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-de89e2f9e9 / seed 1

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/226`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/175/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-de89e2f9e9 / seed 2

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/227`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/175/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 138 | 144 | 154944 | 377058 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 570 | 582 | 44564.6 | 70317.2 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f36d0647d5 / seed 0

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/228`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/176/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f36d0647d5 / seed 1

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/229`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/176/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f36d0647d5 / seed 2

Root `ts-order-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/230`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/176/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-order-service / ts-order-service | False | N/A | None | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 141 | 144 | 180781 | 188795 | False | False | False | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 686 | 675 | 44707.8 | 44394 | False | False | False | available / None |
| caller | ts-inside-payment-service / ts-inside-payment-service | True | 1 | False | 257 | 187 | 52001.4 | 108544 | True | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 133 | 177 | 582589 | 644641 | False | False | False | available / None |
| caller | ts-preserve-service / ts-preserve-service | True | 1 | False | 241 | 263 | 569858 | 1.00894e+06 | False | False | False | available / None |
| caller | ts-seat-service / ts-seat-service | True | 1 | True | 6536 | 6660 | 57134 | 77701.9 | False | False | False | available / None |
| caller | ts-security-service / ts-security-service | True | 1 | False | 238 | 280 | 50273.9 | 227028 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 9027 | 9148 | 56543.6 | 63407.7 | False | False | False | available / None |
| caller | ts-travel2-service / ts-travel2-service | False | 2 | True | 14561 | 14832 | 58121 | 63107 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f81f88234e / seed 0

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/231`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/177/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f81f88234e / seed 1

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/232`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/177/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f81f88234e / seed 2

Root `ts-auth-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/233`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/177/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-auth-service / ts-auth-service | False | N/A | None | 2120 | 2055 | 416612 | 782776 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f9a8e05ed7 / seed 0

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/234`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/178/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f9a8e05ed7 / seed 1

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/235`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/178/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-f9a8e05ed7 / seed 2

Root `ts-travel-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/236`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/178/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-travel-service / ts-travel-service | False | N/A | None | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | True | 1 | False | 141 | 141 | 167780 | 433168 | True | False | False | available / None |
| caller | ts-food-service / ts-food-service | True | 1 | False | 492 | 480 | 50427.5 | 76370.7 | False | False | False | available / None |

## RE2-TT / TORAI B / dev-fbc45b0c67 / seed 0

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/237`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/179/evidence/seed_evidence/0`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-fbc45b0c67 / seed 1

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/238`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/179/evidence/seed_evidence/1`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## RE2-TT / TORAI B / dev-fbc45b0c67 / seed 2

Root `ts-train-service`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 9. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/239`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/179/evidence/seed_evidence/2`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | ts-train-service / ts-train-service | False | N/A | None | 15855 | 11172 | 4255 | 404959 | True | True | True | available / None |
| caller | ts-admin-travel-service / ts-admin-travel-service | False | 2 | False | 147 | 96 | 163313 | 6.477e+06 | True | True | True | available / None |
| caller | ts-basic-service / ts-basic-service | True | 1 | False | 14098 | 10082 | 17168.9 | 637213 | True | True | True | available / None |
| caller | ts-food-service / ts-food-service | False | 2 | False | 705 | 599 | 43232 | 42353.7 | False | False | False | available / None |
| caller | ts-preserve-other-service / ts-preserve-other-service | False | 2 | False | 162 | 80 | 470126 | 4.08495e+06 | True | True | True | available / None |
| caller | ts-preserve-service / ts-preserve-service | False | 2 | False | 263 | 221 | 459196 | 4.08963e+06 | True | True | True | available / None |
| caller | ts-seat-service / ts-seat-service | False | 2 | False | 6666 | 4759 | 45500.8 | 649550 | True | True | True | available / None |
| caller | ts-ticketinfo-service / ts-ticketinfo-service | False | 2 | False | 9964 | 7124 | 45372.6 | 645848 | True | True | True | available / None |
| caller | ts-travel-service / ts-travel-service | True | 1 | False | 8749 | 6447 | 48258.2 | 652631 | True | True | True | available / None |
| caller | ts-travel2-service / ts-travel2-service | True | 1 | False | 15445 | 10835 | 48688 | 652599 | True | True | True | available / None |

## Nezha-OB / BARO / dev-14701a3bbb / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/240`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/180/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 708 | 704 | 526.65 | 99989.2 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 496 | 420 | 255808 | 410430 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 8029 | 8279 | 172015 | 209640 | False | False | False | available / None |

## Nezha-OB / BARO / dev-1ac905bc95 / seed single

Root `frontend`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/241`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/181/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4734 | 6663 | 183772 | 120286 | False | False | False | available / None |

## Nezha-OB / BARO / dev-27252dca60 / seed single

Root `productcatalogservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 3. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/242`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/182/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | productcatalogservice / productcatalogservice | False | N/A | None | 9705 | 3795 | 3217 | 3309 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 366 | 320 | 177357 | 76649.9 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 6013 | 3847 | 140489 | 103764 | False | False | False | available / None |
| caller | recommendationservice / recommendationservice | True | 1 | True | 760 | 284 | 22115 | 7043.05 | False | False | False | available / None |

## Nezha-OB / BARO / dev-2bfc97b01e / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/243`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/183/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 420 | 608 | 154342 | 169124 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 7662 | 9049 | 115056 | 121809 | False | False | False | available / None |

## Nezha-OB / BARO / dev-396c8dbf7d / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/244`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/184/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 22 | 38 | 661.65 | 999681 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 482 | 786 | 187884 | 1.06692e+06 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 7682 | 9700 | 179342 | 179761 | False | False | False | available / None |

## Nezha-OB / BARO / dev-3b92690644 / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/245`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/185/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 326 | 600 | 222793 | 341393 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 6329 | 10516 | 175415 | 186991 | False | False | False | available / None |

## Nezha-OB / BARO / dev-3e27669440 / seed single

Root `adservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/246`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/186/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | adservice / adservice | False | N/A | None | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | False | 6123 | 9056 | 180827 | 1.0001e+06 | True | True | True | available / None |

## Nezha-OB / BARO / dev-515c5f2190 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/247`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/187/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | False | 7835 | 4857 | 199288 | 4.13323e+06 | True | True | True | available / None |

## Nezha-OB / BARO / dev-5467884de4 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/248`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/188/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1174 | 900 | 40090.6 | 31110.4 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9068 | 6775 | 185988 | 602006 | True | True | False | available / None |

## Nezha-OB / BARO / dev-55f99f3e0a / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/249`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/189/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 334 | 703 | 160187 | 384347 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 3843 | 13049 | 164437 | 182841 | False | False | False | available / None |

## Nezha-OB / BARO / dev-5ada15752d / seed single

Root `frontend`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/250`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/190/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4462 | 7351 | 186409 | 170864 | False | False | False | available / None |

## Nezha-OB / BARO / dev-607751ac0a / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/251`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/191/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 708 | 688 | 246441 | 188425 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 9341 | 8348 | 195918 | 187769 | False | False | False | available / None |

## Nezha-OB / BARO / dev-63c30faf34 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/252`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/192/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7735 | 8473 | 149752 | 563353 | True | True | False | available / None |

## Nezha-OB / BARO / dev-6c9afc9822 / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/253`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/193/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 28 | 27 | 652.35 | 655.8 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 590 | 554 | 194494 | 927689 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 8379 | 8451 | 182994 | 184459 | False | False | False | available / None |

## Nezha-OB / BARO / dev-70629373f9 / seed single

Root `paymentservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/254`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/194/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 13 | 42 | 606.2 | 859.7 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 268 | 894 | 263476 | 292371 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | False | 5563 | 11682 | 185437 | 199601 | False | False | False | available / None |

## Nezha-OB / BARO / dev-7b7c973198 / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/255`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/195/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 20 | 41 | 798.8 | 650 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 416 | 840 | 188773 | 987918 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 6603 | 10690 | 142569 | 194237 | False | False | False | available / None |

## Nezha-OB / BARO / dev-7d3c2fe6d1 / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/256`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/196/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 687 | 893 | 498 | 100029 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 498 | 658 | 217997 | 293235 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 7310 | 9858 | 190392 | 182558 | False | False | False | available / None |

## Nezha-OB / BARO / dev-8ecd9880ed / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/257`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/197/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 703 | 481 | 200788 | 327199 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 8687 | 8367 | 172223 | 189354 | False | False | False | available / None |

## Nezha-OB / BARO / dev-95e164235f / seed single

Root `paymentservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/258`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/198/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 33 | 36 | 302.8 | 476.25 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 678 | 728 | 185713 | 166158 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | False | 8309 | 8745 | 163161 | 116029 | False | False | False | available / None |

## Nezha-OB / BARO / dev-9b9397a4dc / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/259`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/199/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 686 | 632 | 2.99177e+06 | 3.20179e+06 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5145 | 4720 | 3.40418e+06 | 3.82373e+06 | False | False | False | available / None |

## Nezha-OB / BARO / dev-9fd793feb7 / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/260`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/200/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 522 | 1034 | 495.85 | 577830 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 376 | 654 | 349706 | 747030 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5401 | 11445 | 190800 | 375663 | False | False | False | available / None |

## Nezha-OB / BARO / dev-b0f8b2e3ac / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/261`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/201/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 256 | 856 | 173847 | 440784 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5022 | 12347 | 206421 | 218466 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-14701a3bbb / seed single

Root `shippingservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/262`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/202/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 708 | 704 | 526.65 | 99989.2 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 496 | 420 | 255808 | 410430 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 8037 | 8271 | 173504 | 208930 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-1ac905bc95 / seed single

Root `frontend`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/263`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/203/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4736 | 6661 | 183840 | 119703 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-27252dca60 / seed single

Root `productcatalogservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 3. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/264`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/204/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | productcatalogservice / productcatalogservice | False | N/A | None | 9705 | 3795 | 3217 | 3309 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 372 | 314 | 188885 | 72745.2 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 6029 | 3831 | 145080 | 102200 | False | False | False | available / None |
| caller | recommendationservice / recommendationservice | True | 1 | False | 764 | 280 | 22063.3 | 7062.45 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-2bfc97b01e / seed single

Root `checkoutservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/265`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/205/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 420 | 608 | 154342 | 169124 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 7668 | 9043 | 116068 | 121049 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-396c8dbf7d / seed single

Root `emailservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/266`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/206/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 22 | 38 | 661.65 | 999681 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 482 | 786 | 187884 | 1.06692e+06 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 7684 | 9698 | 179264 | 179769 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-3b92690644 / seed single

Root `checkoutservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/267`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/207/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 326 | 600 | 222793 | 341393 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 6333 | 10512 | 176334 | 186572 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-3e27669440 / seed single

Root `adservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/268`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/208/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | adservice / adservice | False | N/A | None | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | False | 6135 | 9044 | 182851 | 1.00009e+06 | True | True | True | available / None |

## Nezha-OB / SimpleRCA / dev-515c5f2190 / seed single

Root `recommendationservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/269`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/209/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | False | 7835 | 4857 | 199288 | 4.13323e+06 | True | True | True | available / None |

## Nezha-OB / SimpleRCA / dev-5467884de4 / seed single

Root `recommendationservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/270`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/210/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1176 | 898 | 40080.8 | 31159.3 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9080 | 6763 | 186123 | 601951 | True | True | False | available / None |

## Nezha-OB / SimpleRCA / dev-55f99f3e0a / seed single

Root `checkoutservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/271`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/211/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 334 | 703 | 160187 | 384347 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 3843 | 13049 | 164437 | 182841 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-5ada15752d / seed single

Root `frontend`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/272`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/212/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4468 | 7345 | 186833 | 169753 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-607751ac0a / seed single

Root `checkoutservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/273`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/213/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 708 | 688 | 246441 | 188425 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9347 | 8342 | 195926 | 187710 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-63c30faf34 / seed single

Root `recommendationservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/274`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/214/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7735 | 8473 | 149752 | 563353 | True | True | False | available / None |

## Nezha-OB / SimpleRCA / dev-6c9afc9822 / seed single

Root `emailservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/275`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/215/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 28 | 27 | 652.35 | 655.8 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 590 | 554 | 194494 | 927689 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 8383 | 8447 | 183445 | 183680 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-70629373f9 / seed single

Root `paymentservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/276`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/216/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 13 | 42 | 606.2 | 859.7 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 268 | 894 | 263476 | 292371 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | False | 5569 | 11676 | 186248 | 199010 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-7b7c973198 / seed single

Root `emailservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/277`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/217/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 20 | 41 | 798.8 | 650 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 416 | 840 | 188773 | 987918 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 6603 | 10690 | 142569 | 194237 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-7d3c2fe6d1 / seed single

Root `shippingservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/278`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/218/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 687 | 893 | 498 | 100029 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 498 | 658 | 217997 | 293235 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 7312 | 9856 | 190375 | 182581 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-8ecd9880ed / seed single

Root `checkoutservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/279`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/219/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 707 | 477 | 212483 | 308619 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 8697 | 8357 | 174391 | 188137 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-95e164235f / seed single

Root `paymentservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/280`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/220/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 33 | 36 | 302.8 | 476.25 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 678 | 728 | 185713 | 166158 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | False | 8309 | 8745 | 163161 | 116029 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-9b9397a4dc / seed single

Root `recommendationservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/281`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/221/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 695 | 623 | 3.03543e+06 | 3.19883e+06 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5173 | 4692 | 3.55501e+06 | 3.75404e+06 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-9fd793feb7 / seed single

Root `shippingservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/282`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/222/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 522 | 1034 | 495.85 | 577830 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 376 | 654 | 349706 | 747030 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5405 | 11441 | 190802 | 375651 | False | False | False | available / None |

## Nezha-OB / SimpleRCA / dev-b0f8b2e3ac / seed single

Root `checkoutservice`; status `OK`; split `start`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/283`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/223/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 256 | 856 | 173847 | 440784 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 5030 | 12339 | 208582 | 217874 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-14701a3bbb / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/284`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/224/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 708 | 704 | 526.65 | 99989.2 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 496 | 420 | 255808 | 410430 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 8029 | 8279 | 172015 | 209640 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-1ac905bc95 / seed single

Root `frontend`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/285`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/225/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4734 | 6663 | 183772 | 120286 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-27252dca60 / seed single

Root `productcatalogservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 3. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/286`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/226/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | productcatalogservice / productcatalogservice | False | N/A | None | 9705 | 3795 | 3217 | 3309 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 366 | 320 | 177357 | 76649.9 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 6013 | 3847 | 140489 | 103764 | False | False | False | available / None |
| caller | recommendationservice / recommendationservice | True | 1 | False | 760 | 284 | 22115 | 7043.05 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-2bfc97b01e / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/287`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/227/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 420 | 608 | 154342 | 169124 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7662 | 9049 | 115056 | 121809 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-396c8dbf7d / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/288`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/228/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 22 | 38 | 661.65 | 999681 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 482 | 786 | 187884 | 1.06692e+06 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | True | 7682 | 9700 | 179342 | 179761 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-3b92690644 / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/289`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/229/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 326 | 600 | 222793 | 341393 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 6329 | 10516 | 175415 | 186991 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-3e27669440 / seed single

Root `adservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/290`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/230/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | adservice / adservice | False | N/A | None | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | True | 6123 | 9056 | 180827 | 1.0001e+06 | True | True | True | available / None |

## Nezha-OB / MicroRank full / dev-515c5f2190 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/291`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/231/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | True | 7835 | 4857 | 199288 | 4.13323e+06 | True | True | True | available / None |

## Nezha-OB / MicroRank full / dev-5467884de4 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/292`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/232/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1174 | 900 | 40090.6 | 31110.4 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9068 | 6775 | 185988 | 602006 | True | True | False | available / None |

## Nezha-OB / MicroRank full / dev-55f99f3e0a / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/293`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/233/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 334 | 703 | 160187 | 384347 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 3843 | 13049 | 164437 | 182841 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-5ada15752d / seed single

Root `frontend`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/294`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/234/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4462 | 7351 | 186409 | 170864 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-607751ac0a / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/295`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/235/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 708 | 688 | 246441 | 188425 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9341 | 8348 | 195918 | 187769 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-63c30faf34 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/296`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/236/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7735 | 8473 | 149752 | 563353 | True | True | False | available / None |

## Nezha-OB / MicroRank full / dev-6c9afc9822 / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/297`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/237/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 28 | 27 | 652.35 | 655.8 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 590 | 554 | 194494 | 927689 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | True | 8379 | 8451 | 182994 | 184459 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-70629373f9 / seed single

Root `paymentservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/298`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/238/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 13 | 42 | 606.2 | 859.7 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 268 | 894 | 263476 | 292371 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | True | 5563 | 11682 | 185437 | 199601 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-7b7c973198 / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/299`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/239/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 20 | 41 | 798.8 | 650 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 416 | 840 | 188773 | 987918 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | True | 6603 | 10690 | 142569 | 194237 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-7d3c2fe6d1 / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/300`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/240/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 687 | 893 | 498 | 100029 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 498 | 658 | 217997 | 293235 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7310 | 9858 | 190392 | 182558 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-8ecd9880ed / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/301`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/241/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 703 | 481 | 200788 | 327199 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 8687 | 8367 | 172223 | 189354 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-95e164235f / seed single

Root `paymentservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/302`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/242/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 33 | 36 | 302.8 | 476.25 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 678 | 728 | 185713 | 166158 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | True | 8309 | 8745 | 163161 | 116029 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-9b9397a4dc / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/303`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/243/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 686 | 632 | 2.99177e+06 | 3.20179e+06 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 5145 | 4720 | 3.40418e+06 | 3.82373e+06 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-9fd793feb7 / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/304`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/244/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 522 | 1034 | 495.85 | 577830 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 376 | 654 | 349706 | 747030 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 5401 | 11445 | 190800 | 375663 | False | False | False | available / None |

## Nezha-OB / MicroRank full / dev-b0f8b2e3ac / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/305`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/245/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 256 | 856 | 173847 | 440784 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 5022 | 12347 | 206421 | 218466 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-14701a3bbb / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/306`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/246/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 708 | 704 | 526.65 | 99989.2 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 496 | 420 | 255808 | 410430 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 8029 | 8279 | 172015 | 209640 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-1ac905bc95 / seed single

Root `frontend`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/307`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/247/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4734 | 6663 | 183772 | 120286 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-27252dca60 / seed single

Root `productcatalogservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 3. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/308`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/248/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | productcatalogservice / productcatalogservice | False | N/A | None | 9705 | 3795 | 3217 | 3309 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 366 | 320 | 177357 | 76649.9 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 6013 | 3847 | 140489 | 103764 | False | False | False | available / None |
| caller | recommendationservice / recommendationservice | True | 1 | False | 760 | 284 | 22115 | 7043.05 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-2bfc97b01e / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/309`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/249/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 420 | 608 | 154342 | 169124 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7662 | 9049 | 115056 | 121809 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-396c8dbf7d / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/310`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/250/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 22 | 38 | 661.65 | 999681 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 482 | 786 | 187884 | 1.06692e+06 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | False | 7682 | 9700 | 179342 | 179761 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-3b92690644 / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/311`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/251/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 326 | 600 | 222793 | 341393 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 6329 | 10516 | 175415 | 186991 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-3e27669440 / seed single

Root `adservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/312`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/252/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | adservice / adservice | False | N/A | None | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | True | 6123 | 9056 | 180827 | 1.0001e+06 | True | True | True | available / None |

## Nezha-OB / TraceRCA / dev-515c5f2190 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/313`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/253/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available / None |
| caller | frontend / frontend | True | 1 | True | 7835 | 4857 | 199288 | 4.13323e+06 | True | True | True | available / None |

## Nezha-OB / TraceRCA / dev-5467884de4 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/314`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/254/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1174 | 900 | 40090.6 | 31110.4 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9068 | 6775 | 185988 | 602006 | True | True | False | available / None |

## Nezha-OB / TraceRCA / dev-55f99f3e0a / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/315`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/255/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 334 | 703 | 160187 | 384347 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 3843 | 13049 | 164437 | 182841 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-5ada15752d / seed single

Root `frontend`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 0. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/316`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/256/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | False | N/A | None | 4462 | 7351 | 186409 | 170864 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-607751ac0a / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/317`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/257/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 708 | 688 | 246441 | 188425 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 9341 | 8348 | 195918 | 187769 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-63c30faf34 / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/318`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/258/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7735 | 8473 | 149752 | 563353 | True | True | False | available / None |

## Nezha-OB / TraceRCA / dev-6c9afc9822 / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/319`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/259/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 28 | 27 | 652.35 | 655.8 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 590 | 554 | 194494 | 927689 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | True | 8379 | 8451 | 182994 | 184459 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-70629373f9 / seed single

Root `paymentservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/320`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/260/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 13 | 42 | 606.2 | 859.7 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 268 | 894 | 263476 | 292371 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | True | 5563 | 11682 | 185437 | 199601 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-7b7c973198 / seed single

Root `emailservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'root_not_returned'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'root_not_returned'}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/321`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/261/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | False | N/A | None | 20 | 41 | 798.8 | 650 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | None | 416 | 840 | 188773 | 987918 | True | True | True | available / None |
| caller | frontend / frontend | False | 2 | None | 6603 | 10690 | 142569 | 194237 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-7d3c2fe6d1 / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/322`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/262/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 687 | 893 | 498 | 100029 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 498 | 658 | 217997 | 293235 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 7310 | 9858 | 190392 | 182558 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-8ecd9880ed / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/323`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/263/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 703 | 481 | 200788 | 327199 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 8687 | 8367 | 172223 | 189354 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-95e164235f / seed single

Root `paymentservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': True}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/324`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/264/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | False | N/A | None | 33 | 36 | 302.8 | 476.25 | False | False | False | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | True | 678 | 728 | 185713 | 166158 | False | False | False | available / None |
| caller | frontend / frontend | False | 2 | True | 8309 | 8745 | 163161 | 116029 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-9b9397a4dc / seed single

Root `recommendationservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/325`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/265/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | False | N/A | None | 686 | 632 | 2.99177e+06 | 3.20179e+06 | False | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5145 | 4720 | 3.40418e+06 | 3.82373e+06 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-9fd793feb7 / seed single

Root `shippingservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': False, 'availability': 'available', 'reason': None}, '5': {'value': False, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 2. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/326`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/266/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | False | N/A | None | 522 | 1034 | 495.85 | 577830 | True | True | True | available / None |
| caller | checkoutservice / checkoutservice | True | 1 | False | 376 | 654 | 349706 | 747030 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | False | 5401 | 11445 | 190800 | 375663 | False | False | False | available / None |

## Nezha-OB / TraceRCA / dev-b0f8b2e3ac / seed single

Root `checkoutservice`; status `OK`; split `end`; sai OK k=1/5: `{'1': True, '5': False}`; cờ cơ sở M5: `{'1': {'value': True, 'availability': 'available', 'reason': None}, '5': {'value': True, 'availability': 'available', 'reason': None}}`. Quan hệ caller: available, lý do None; số ancestor 1. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/327`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/267/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | False | N/A | None | 256 | 856 | 173847 | 440784 | True | False | False | available / None |
| caller | frontend / frontend | True | 1 | True | 5022 | 12347 | 206421 | 218466 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-14701a3bbb / seed single

Root `shippingservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/328`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/268/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | None | N/A | None | 708 | 704 | 526.65 | 99989.2 | True | True | True | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-1ac905bc95 / seed single

Root `frontend`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/329`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/269/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | None | N/A | None | 4734 | 6663 | 183772 | 120286 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-27252dca60 / seed single

Root `productcatalogservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/330`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/270/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | productcatalogservice / productcatalogservice | None | N/A | None | 9705 | 3795 | 3217 | 3309 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-2bfc97b01e / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/331`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/271/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 420 | 608 | 154342 | 169124 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-396c8dbf7d / seed single

Root `emailservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/332`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/272/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | None | N/A | None | 22 | 38 | 661.65 | 999681 | True | True | True | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-3b92690644 / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/333`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/273/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 326 | 600 | 222793 | 341393 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-3e27669440 / seed single

Root `adservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/334`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/274/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | adservice / adservice | None | N/A | None | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-515c5f2190 / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/335`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/275/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-5467884de4 / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/336`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/276/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 1174 | 900 | 40090.6 | 31110.4 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-55f99f3e0a / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/337`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/277/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 334 | 703 | 160187 | 384347 | True | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-5ada15752d / seed single

Root `frontend`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/338`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/278/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | None | N/A | None | 4462 | 7351 | 186409 | 170864 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-607751ac0a / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/339`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/279/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 708 | 688 | 246441 | 188425 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-63c30faf34 / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/340`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/280/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-6c9afc9822 / seed single

Root `emailservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/341`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/281/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | None | N/A | None | 28 | 27 | 652.35 | 655.8 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-70629373f9 / seed single

Root `paymentservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/342`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/282/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | None | N/A | None | 13 | 42 | 606.2 | 859.7 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-7b7c973198 / seed single

Root `emailservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/343`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/283/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | None | N/A | None | 20 | 41 | 798.8 | 650 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-7d3c2fe6d1 / seed single

Root `shippingservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/344`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/284/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | None | N/A | None | 687 | 893 | 498 | 100029 | True | True | True | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-8ecd9880ed / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/345`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/285/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 703 | 481 | 200788 | 327199 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-95e164235f / seed single

Root `paymentservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/346`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/286/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | None | N/A | None | 33 | 36 | 302.8 | 476.25 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-9b9397a4dc / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/347`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/287/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 686 | 632 | 2.99177e+06 | 3.20179e+06 | False | False | False | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-9fd793feb7 / seed single

Root `shippingservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/348`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/288/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | None | N/A | None | 522 | 1034 | 495.85 | 577830 | True | True | True | available / None |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-b0f8b2e3ac / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/349`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/289/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 256 | 856 | 173847 | 440784 | True | False | False | available / None |

## Nezha-OB / TORAI B / dev-14701a3bbb / seed single

Root `shippingservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/350`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/290/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | None | N/A | None | 708 | 704 | 526.65 | 99989.2 | True | True | True | available / None |

## Nezha-OB / TORAI B / dev-1ac905bc95 / seed single

Root `frontend`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/351`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/291/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | None | N/A | None | 4734 | 6663 | 183772 | 120286 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-27252dca60 / seed single

Root `productcatalogservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/352`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/292/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | productcatalogservice / productcatalogservice | None | N/A | None | 9705 | 3795 | 3217 | 3309 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-2bfc97b01e / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/353`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/293/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 420 | 608 | 154342 | 169124 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-396c8dbf7d / seed single

Root `emailservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/354`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/294/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | None | N/A | None | 22 | 38 | 661.65 | 999681 | True | True | True | available / None |

## Nezha-OB / TORAI B / dev-3b92690644 / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/355`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/295/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 326 | 600 | 222793 | 341393 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-3e27669440 / seed single

Root `adservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/356`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/296/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | adservice / adservice | None | N/A | None | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available / None |

## Nezha-OB / TORAI B / dev-515c5f2190 / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/357`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/297/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available / None |

## Nezha-OB / TORAI B / dev-5467884de4 / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/358`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/298/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 1174 | 900 | 40090.6 | 31110.4 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-55f99f3e0a / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/359`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/299/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 334 | 703 | 160187 | 384347 | True | False | False | available / None |

## Nezha-OB / TORAI B / dev-5ada15752d / seed single

Root `frontend`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/360`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/300/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | frontend / frontend | None | N/A | None | 4462 | 7351 | 186409 | 170864 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-607751ac0a / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/361`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/301/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 708 | 688 | 246441 | 188425 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-63c30faf34 / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/362`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/302/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-6c9afc9822 / seed single

Root `emailservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/363`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/303/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | None | N/A | None | 28 | 27 | 652.35 | 655.8 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-70629373f9 / seed single

Root `paymentservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/364`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/304/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | None | N/A | None | 13 | 42 | 606.2 | 859.7 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-7b7c973198 / seed single

Root `emailservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/365`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/305/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | emailservice / emailservice | None | N/A | None | 20 | 41 | 798.8 | 650 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-7d3c2fe6d1 / seed single

Root `shippingservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/366`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/306/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | None | N/A | None | 687 | 893 | 498 | 100029 | True | True | True | available / None |

## Nezha-OB / TORAI B / dev-8ecd9880ed / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/367`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/307/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 703 | 481 | 200788 | 327199 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-95e164235f / seed single

Root `paymentservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/368`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/308/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | paymentservice / paymentservice | None | N/A | None | 33 | 36 | 302.8 | 476.25 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-9b9397a4dc / seed single

Root `recommendationservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/369`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/309/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | recommendationservice / recommendationservice | None | N/A | None | 686 | 632 | 2.99177e+06 | 3.20179e+06 | False | False | False | available / None |

## Nezha-OB / TORAI B / dev-9fd793feb7 / seed single

Root `shippingservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/370`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/310/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | shippingservice / shippingservice | None | N/A | None | 522 | 1034 | 495.85 | 577830 | True | True | True | available / None |

## Nezha-OB / TORAI B / dev-b0f8b2e3ac / seed single

Root `checkoutservice`; status `UNSUPPORTED`; split `end`; sai OK k=1/5: `{'1': False, '5': False}`; cờ cơ sở M5: `{'1': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}, '5': {'value': None, 'availability': 'N/A', 'reason': 'unsupported'}}`. Quan hệ caller: N/A, lý do missing_channel; số ancestor N/A. Nguồn: `results/T-028/runs/phan-hoi-review-001/caller-root-proxy.json` → `/records/371`, `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/311/evidence/seed_evidence/single`.

| Vai trò | Entity / native service | Direct | Khoảng cách | Chắc chắn trước | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng / lý do |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| root | checkoutservice / checkoutservice | None | N/A | None | 256 | 856 | 173847 | 440784 | True | False | False | available / None |

## Giới hạn

Quan hệ caller là graph N quan sát được. Proxy tăng đồng thời, chỉ caller tăng hoặc caller không tăng không phân xử thứ tự khởi phát và lan với nguyên nhân khác. Cờ M5 vẫn chỉ dùng quan hệ/thứ hạng đã khóa; các số này không tạo nhãn mới hoặc chọn lại tiêu chí.

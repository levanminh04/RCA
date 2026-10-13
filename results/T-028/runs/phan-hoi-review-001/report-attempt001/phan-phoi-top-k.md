# Phân phối top-k theo entity và chiều dài trả về

Nguồn mọi số: `results/T-028/runs/phan-hoi-review-001/ca-sai.json` → `/main_rows/*/evidence/seed_evidence/*/ranking`. Xác suất giữ phân phối hòa chính xác từ bản ghi; hiển thị số thập phân, phân số gốc ở p_by_k_exact. Entity ngoài R có p=0; non-OK N/A. L/|O| là chiều dài R trên tập O của chính bản ghi; không thay O bằng U.

## RE2-TT / BARO / dev-03d4910932 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-03d4910932-sNone-h0-cbbe5c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-12a1a88069 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-12a1a88069-sNone-h0-23307e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 1 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 1 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-14372e1209 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-14372e1209-sNone-h0-9b694a/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 1 | 1 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 1 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-16597725c1 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-16597725c1-sNone-h0-b83c52/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 1 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-16870e660c / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-16870e660c-sNone-h0-fab858/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 1 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-1e6d61b5ec / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-1e6d61b5ec-sNone-h0-ed1564/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 1 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 1 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 1 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-20acb4402d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-20acb4402d-sNone-h0-22e6bd/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 1 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-260d332c8d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-260d332c8d-sNone-h0-dbdbd7/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 1 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 1 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-3ae0a6c15a / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-3ae0a6c15a-sNone-h0-f83ef5/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-3defe3d34b / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-3defe3d34b-sNone-h0-dfc9c4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 1 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-4e68956051 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-4e68956051-sNone-h0-70526f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-4f8a844308 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-4f8a844308-sNone-h0-05dc03/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-57546fd87b / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-57546fd87b-sNone-h0-3fb7f2/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 1 |
| ts-preserve-other-mongo | 0 | 1 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-59f696a169 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-59f696a169-sNone-h0-db76fe/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-746fd74313 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-746fd74313-sNone-h0-7cac1b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 1 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-7f1b6b071d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-7f1b6b071d-sNone-h0-b833aa/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-8017c6dc70 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-8017c6dc70-sNone-h0-b7d8f1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 1 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-98bc73c499 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-98bc73c499-sNone-h0-de6480/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 1 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-a505ab3f65 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-a505ab3f65-sNone-h0-2075b5/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-a5cabe5fa7 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-a5cabe5fa7-sNone-h0-5a663b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 1 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 1 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 1 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 1 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-a915aa2424 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-a915aa2424-sNone-h0-714b10/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-b8bd0abf60 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-b8bd0abf60-sNone-h0-b7738b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-ba831dbeb8 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-ba831dbeb8-sNone-h0-3d9c16/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-bcbd4f46ae / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-bcbd4f46ae-sNone-h0-05442c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-db293894ab / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-db293894ab-sNone-h0-56c980/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 1 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 1 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-de89e2f9e9 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-de89e2f9e9-sNone-h0-bb8481/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-f36d0647d5 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-f36d0647d5-sNone-h0-d73bb4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-f81f88234e / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-f81f88234e-sNone-h0-ed16f9/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 1 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 1 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-f9a8e05ed7 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-f9a8e05ed7-sNone-h0-43732b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / BARO / dev-fbc45b0c67 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/baro-30-001/luot/baro-a-dev-fbc45b0c67-sNone-h0-c1d73b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-03d4910932 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-03d4910932-sNone-h0-c07dc5/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-12a1a88069 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-12a1a88069-sNone-h0-3a9e1d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-14372e1209 / seed single

L/|O|=69/69; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-14372e1209-sNone-h0-7cccf1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| istio-init | 0 | 0 |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-16597725c1 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-16597725c1-sNone-h0-bd8f37/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 1 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-16870e660c / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-16870e660c-sNone-h0-f40b88/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-1e6d61b5ec / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-1e6d61b5ec-sNone-h0-f349b0/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 1 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 1 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-20acb4402d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-20acb4402d-sNone-h0-b74713/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 1 | 1 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-260d332c8d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-260d332c8d-sNone-h0-322b15/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-3ae0a6c15a / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-3ae0a6c15a-sNone-h0-d5cd46/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-3defe3d34b / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-3defe3d34b-sNone-h0-a2d104/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-4e68956051 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-4e68956051-sNone-h0-b32dfc/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-4f8a844308 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-4f8a844308-sNone-h0-439d3e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-57546fd87b / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-57546fd87b-sNone-h0-939a3d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 1 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-59f696a169 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-59f696a169-sNone-h0-b44421/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-746fd74313 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-746fd74313-sNone-h0-872556/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 1 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 1 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-7f1b6b071d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-7f1b6b071d-sNone-h0-0bc47f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 1 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-8017c6dc70 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-8017c6dc70-sNone-h0-9b3f75/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-98bc73c499 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-98bc73c499-sNone-h0-cb525c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-a505ab3f65 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-a505ab3f65-sNone-h0-1d202b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-a5cabe5fa7 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-a5cabe5fa7-sNone-h0-f8013a/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 1 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-a915aa2424 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-a915aa2424-sNone-h0-68a198/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 1 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-b8bd0abf60 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-b8bd0abf60-sNone-h0-5adff3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-ba831dbeb8 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-ba831dbeb8-sNone-h0-8ad2e6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-bcbd4f46ae / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-bcbd4f46ae-sNone-h0-5ae26e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-db293894ab / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-db293894ab-sNone-h0-2e0b7b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-de89e2f9e9 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-de89e2f9e9-sNone-h0-da7d66/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-f36d0647d5 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-f36d0647d5-sNone-h0-5aabef/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 1 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 1 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-f81f88234e / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-f81f88234e-sNone-h0-4d6b8e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-f9a8e05ed7 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-f9a8e05ed7-sNone-h0-e66c17/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 1 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / SimpleRCA / dev-fbc45b0c67 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-fbc45b0c67-sNone-h0-87f571/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 1 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-03d4910932 / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-03d4910932-sNone-h0-95c88f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / MicroRank full / dev-12a1a88069 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-12a1a88069-sNone-h0-b85991/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-14372e1209 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-14372e1209-sNone-h0-e8c41f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-16597725c1 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-16597725c1-sNone-h0-55f476/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-16870e660c / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-16870e660c-sNone-h0-c05dc3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / MicroRank full / dev-1e6d61b5ec / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-1e6d61b5ec-sNone-h0-5ffe14/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |

## RE2-TT / MicroRank full / dev-20acb4402d / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-20acb4402d-sNone-h0-2b1829/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |

## RE2-TT / MicroRank full / dev-260d332c8d / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-260d332c8d-sNone-h0-0d7ac8/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |

## RE2-TT / MicroRank full / dev-3ae0a6c15a / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-3ae0a6c15a-sNone-h0-7910fe/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-3defe3d34b / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-3defe3d34b-sNone-h0-d38dd0/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-4e68956051 / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-4e68956051-sNone-h0-19de8a/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / MicroRank full / dev-4f8a844308 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-4f8a844308-sNone-h0-f0dc53/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-57546fd87b / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-57546fd87b-sNone-h0-bdea3f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-59f696a169 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-59f696a169-sNone-h0-0c32ea/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-746fd74313 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-746fd74313-sNone-h0-8b5d24/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-7f1b6b071d / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-7f1b6b071d-sNone-h0-851c6c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-8017c6dc70 / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-8017c6dc70-sNone-h0-023da1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |

## RE2-TT / MicroRank full / dev-98bc73c499 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-98bc73c499-sNone-h0-b7f983/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-a505ab3f65 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-a505ab3f65-sNone-h0-230ffd/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-a5cabe5fa7 / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-a5cabe5fa7-sNone-h0-9df8ca/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / MicroRank full / dev-a915aa2424 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-a915aa2424-sNone-h0-28ebca/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-b8bd0abf60 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-b8bd0abf60-sNone-h0-b296eb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-ba831dbeb8 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-ba831dbeb8-sNone-h0-c6b45c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-bcbd4f46ae / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-bcbd4f46ae-sNone-h0-d20508/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-db293894ab / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-db293894ab-sNone-h0-179db7/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-de89e2f9e9 / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-de89e2f9e9-sNone-h0-69fc25/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-f36d0647d5 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-f36d0647d5-sNone-h0-478733/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-f81f88234e / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-f81f88234e-sNone-h0-cba3d2/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-f9a8e05ed7 / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-f9a8e05ed7-sNone-h0-7020c6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / MicroRank full / dev-fbc45b0c67 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-fbc45b0c67-sNone-h0-6a7e35/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 1 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-03d4910932 / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-03d4910932-sNone-h0-dfd4d6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / TraceRCA / dev-12a1a88069 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-12a1a88069-sNone-h0-9f2be2/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 1 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-14372e1209 / seed single

L/|O|=26/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-14372e1209-sNone-h0-07d352/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-16597725c1 / seed single

L/|O|=24/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-16597725c1-sNone-h0-b227be/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-16870e660c / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-16870e660c-sNone-h0-62dd0e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / TraceRCA / dev-1e6d61b5ec / seed single

L/|O|=20/20; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-1e6d61b5ec-sNone-h0-17b8ef/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-20acb4402d / seed single

L/|O|=15/20; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-20acb4402d-sNone-h0-ec8a01/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 1 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-260d332c8d / seed single

L/|O|=18/20; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-260d332c8d-sNone-h0-6be8b2/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-3ae0a6c15a / seed single

L/|O|=25/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-3ae0a6c15a-sNone-h0-1bd6ca/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 1 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-3defe3d34b / seed single

L/|O|=24/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-3defe3d34b-sNone-h0-08a3cd/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-4e68956051 / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-4e68956051-sNone-h0-44eb21/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / TraceRCA / dev-4f8a844308 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-4f8a844308-sNone-h0-50e607/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-57546fd87b / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-57546fd87b-sNone-h0-5f7c61/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-59f696a169 / seed single

L/|O|=22/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-59f696a169-sNone-h0-bc7bf9/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-746fd74313 / seed single

L/|O|=23/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-746fd74313-sNone-h0-dbb3ec/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-7f1b6b071d / seed single

L/|O|=26/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-7f1b6b071d-sNone-h0-424193/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-8017c6dc70 / seed single

L/|O|=19/20; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-8017c6dc70-sNone-h0-0c48ff/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-98bc73c499 / seed single

L/|O|=25/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-98bc73c499-sNone-h0-a1c01e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 1 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-a505ab3f65 / seed single

L/|O|=23/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-a505ab3f65-sNone-h0-97af88/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0.5 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0.5 |
| ts-train-service | 1 | 1 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-a5cabe5fa7 / seed single

L/|O|=0/27; availability=N/A; reason=non_OK. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-a5cabe5fa7-sNone-h0-70fc22/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | N/A | N/A |
| ts-admin-travel-service | N/A | N/A |
| ts-assurance-service | N/A | N/A |
| ts-auth-service | N/A | N/A |
| ts-basic-service | N/A | N/A |
| ts-config-service | N/A | N/A |
| ts-consign-price-service | N/A | N/A |
| ts-consign-service | N/A | N/A |
| ts-contacts-service | N/A | N/A |
| ts-food-map-service | N/A | N/A |
| ts-food-service | N/A | N/A |
| ts-inside-payment-service | N/A | N/A |
| ts-order-other-service | N/A | N/A |
| ts-order-service | N/A | N/A |
| ts-payment-service | N/A | N/A |
| ts-preserve-other-service | N/A | N/A |
| ts-preserve-service | N/A | N/A |
| ts-price-service | N/A | N/A |
| ts-route-service | N/A | N/A |
| ts-seat-service | N/A | N/A |
| ts-security-service | N/A | N/A |
| ts-station-service | N/A | N/A |
| ts-ticketinfo-service | N/A | N/A |
| ts-train-service | N/A | N/A |
| ts-travel-service | N/A | N/A |
| ts-travel2-service | N/A | N/A |
| ts-user-service | N/A | N/A |

## RE2-TT / TraceRCA / dev-a915aa2424 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-a915aa2424-sNone-h0-9a39dd/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-b8bd0abf60 / seed single

L/|O|=26/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-b8bd0abf60-sNone-h0-e9bb48/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-ba831dbeb8 / seed single

L/|O|=25/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-ba831dbeb8-sNone-h0-5f9608/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 1 | 1 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-bcbd4f46ae / seed single

L/|O|=25/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-bcbd4f46ae-sNone-h0-f9e848/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-db293894ab / seed single

L/|O|=23/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-db293894ab-sNone-h0-cf64a4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 1 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-de89e2f9e9 / seed single

L/|O|=18/20; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-de89e2f9e9-sNone-h0-bc7bf7/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-f36d0647d5 / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-f36d0647d5-sNone-h0-738579/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 1 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 0 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-f81f88234e / seed single

L/|O|=27/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-f81f88234e-sNone-h0-2ab6a4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-basic-service | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-f9a8e05ed7 / seed single

L/|O|=17/20; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-f9a8e05ed7-sNone-h0-f58edd/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-service | 0 | 0 |

## RE2-TT / TraceRCA / dev-fbc45b0c67 / seed single

L/|O|=26/27; availability=available; reason=None. Nguồn bản ghi: `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-fbc45b0c67-sNone-h0-b4dfb5/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-basic-service | 0 | 0.5 |
| ts-config-service | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0.5 |
| ts-train-service | 1 | 1 |
| ts-travel-service | 0 | 1 |
| ts-travel2-service | 0 | 1 |
| ts-user-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-03d4910932 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-03d4910932-sNone-h0-e54417/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-12a1a88069 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-12a1a88069-sNone-h0-ea4bf6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-14372e1209 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-14372e1209-sNone-h0-7794cb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-16597725c1 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-16597725c1-sNone-h0-89c66d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 1 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-16870e660c / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-16870e660c-sNone-h0-e6efeb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 1 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-1e6d61b5ec / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-1e6d61b5ec-sNone-h0-86dfc7/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-20acb4402d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-20acb4402d-sNone-h0-36d5ef/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 1 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-260d332c8d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-260d332c8d-sNone-h0-4db7a2/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 1 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-3ae0a6c15a / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-3ae0a6c15a-sNone-h0-829d79/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-3defe3d34b / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-3defe3d34b-sNone-h0-45f6a5/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 1 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 1 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 1 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-4e68956051 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-4e68956051-sNone-h0-7cd5a1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-4f8a844308 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-4f8a844308-sNone-h0-7aa352/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-57546fd87b / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-57546fd87b-sNone-h0-862055/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 1 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 1 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 1 | 1 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 1 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-59f696a169 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-59f696a169-sNone-h0-fc4c19/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-746fd74313 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-746fd74313-sNone-h0-6c30c3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 1 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-7f1b6b071d / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-7f1b6b071d-sNone-h0-371dd7/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-8017c6dc70 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-8017c6dc70-sNone-h0-78c332/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-98bc73c499 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-98bc73c499-sNone-h0-0e1854/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-a505ab3f65 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-a505ab3f65-sNone-h0-13d377/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-a5cabe5fa7 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-a5cabe5fa7-sNone-h0-c727b3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 1 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-a915aa2424 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-a915aa2424-sNone-h0-811696/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 1 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-b8bd0abf60 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-b8bd0abf60-sNone-h0-0c58be/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-ba831dbeb8 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-ba831dbeb8-sNone-h0-115b30/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-bcbd4f46ae / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-bcbd4f46ae-sNone-h0-c69192/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 1 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-db293894ab / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-db293894ab-sNone-h0-fbacc1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-de89e2f9e9 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-de89e2f9e9-sNone-h0-999d65/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-f36d0647d5 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-f36d0647d5-sNone-h0-c7504e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-f81f88234e / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-f81f88234e-sNone-h0-5efd38/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 1 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 1 | 1 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 1 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-f9a8e05ed7 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-f9a8e05ed7-sNone-h0-f464ea/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / CIRCA OLS+RHT+DA / dev-fbc45b0c67 / seed single

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-fbc45b0c67-sNone-h0-21effb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-03d4910932 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-03d4910932-s0-h0-8cdb6b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-03d4910932 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-03d4910932-s1-h0-7d89f8/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-03d4910932 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-03d4910932-s2-h0-4e1171/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-12a1a88069 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-12a1a88069-s0-h0-389d31/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-12a1a88069 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-12a1a88069-s1-h0-ab05d4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-12a1a88069 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-12a1a88069-s2-h0-04fd89/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-14372e1209 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-14372e1209-s0-h0-adc25f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-14372e1209 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-14372e1209-s1-h0-5b7d1b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-14372e1209 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-14372e1209-s2-h0-ba93b6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-16597725c1 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16597725c1-s0-h0-b566f3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-16597725c1 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16597725c1-s1-h0-990d67/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-16597725c1 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16597725c1-s2-h0-721a29/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-16870e660c / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16870e660c-s0-h0-907fd1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-16870e660c / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16870e660c-s1-h0-48768b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-16870e660c / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16870e660c-s2-h0-d60d5a/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-1e6d61b5ec / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-1e6d61b5ec-s0-h0-e087d4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-1e6d61b5ec / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-1e6d61b5ec-s1-h0-476283/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-1e6d61b5ec / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-1e6d61b5ec-s2-h0-ae694d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-20acb4402d / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-20acb4402d-s0-h0-238a57/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-20acb4402d / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-20acb4402d-s1-h0-5ef419/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-20acb4402d / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-20acb4402d-s2-h0-cc980f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-260d332c8d / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-260d332c8d-s0-h0-429861/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-260d332c8d / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-260d332c8d-s1-h0-f2de3e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-260d332c8d / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-260d332c8d-s2-h0-af0b73/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 1 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-3ae0a6c15a / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-3ae0a6c15a-s0-h0-a3c362/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-3ae0a6c15a / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-3ae0a6c15a-s1-h0-3c61f9/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-3ae0a6c15a / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-3ae0a6c15a-s2-h0-112f57/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 1 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-3defe3d34b / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-3defe3d34b-s0-h0-2d2fcf/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-3defe3d34b / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-3defe3d34b-s1-h0-f80d3b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-3defe3d34b / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-3defe3d34b-s2-h0-b2d633/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-4e68956051 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-4e68956051-s0-h0-29a88a/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-4e68956051 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-4e68956051-s1-h0-1b1d76/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-4e68956051 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-4e68956051-s2-h0-d3e8f8/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-4f8a844308 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-4f8a844308-s0-h0-eca1cb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-4f8a844308 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-4f8a844308-s1-h0-98418e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-4f8a844308 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-4f8a844308-s2-h0-fc2b22/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-57546fd87b / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-57546fd87b-s0-h0-09d70e/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 1 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-57546fd87b / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-57546fd87b-s1-h0-1bc803/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 1 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-57546fd87b / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-57546fd87b-s2-h0-e0b181/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 1 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-59f696a169 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-59f696a169-s0-h0-a6a06d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 1 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-59f696a169 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-59f696a169-s1-h0-fdaf51/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 1 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-59f696a169 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-59f696a169-s2-h0-6c5cc6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 1 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-746fd74313 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-746fd74313-s0-h0-30188b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-746fd74313 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-746fd74313-s1-h0-75c2c9/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-746fd74313 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-746fd74313-s2-h0-8b48ae/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 1 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 1 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 1 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 1 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-7f1b6b071d / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-7f1b6b071d-s0-h0-81c2de/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-7f1b6b071d / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-7f1b6b071d-s1-h0-97c060/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-7f1b6b071d / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-7f1b6b071d-s2-h0-b5dc0d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-8017c6dc70 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-8017c6dc70-s0-h0-fe5366/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-8017c6dc70 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-8017c6dc70-s1-h0-7e7b0f/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-8017c6dc70 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-8017c6dc70-s2-h0-4a3889/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 1 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 1 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 1 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-98bc73c499 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-98bc73c499-s0-h0-5e7707/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-98bc73c499 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-98bc73c499-s1-h0-b800bb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-98bc73c499 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-98bc73c499-s2-h0-3e7667/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a505ab3f65 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a505ab3f65-s0-h0-2739cc/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a505ab3f65 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a505ab3f65-s1-h0-322a86/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a505ab3f65 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a505ab3f65-s2-h0-503c19/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a5cabe5fa7 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a5cabe5fa7-s0-h0-c1efea/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a5cabe5fa7 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a5cabe5fa7-s1-h0-a6f96d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a5cabe5fa7 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a5cabe5fa7-s2-h0-faa19b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 1 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 1 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a915aa2424 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a915aa2424-s0-h0-bf6ace/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a915aa2424 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a915aa2424-s1-h0-c5afb4/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-a915aa2424 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a915aa2424-s2-h0-4f4517/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-b8bd0abf60 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-b8bd0abf60-s0-h0-0e1463/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-b8bd0abf60 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-b8bd0abf60-s1-h0-e221b3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-b8bd0abf60 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-b8bd0abf60-s2-h0-a63bc1/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-ba831dbeb8 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-ba831dbeb8-s0-h0-8a154b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-ba831dbeb8 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-ba831dbeb8-s1-h0-2e06b2/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-ba831dbeb8 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-ba831dbeb8-s2-h0-53457c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-bcbd4f46ae / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-bcbd4f46ae-s0-h0-aeca80/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-bcbd4f46ae / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-bcbd4f46ae-s1-h0-45f245/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-bcbd4f46ae / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-bcbd4f46ae-s2-h0-8b1ab9/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 1 | 1 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-db293894ab / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-db293894ab-s0-h0-c22920/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-db293894ab / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-db293894ab-s1-h0-ac6e7b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-db293894ab / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-db293894ab-s2-h0-f29c55/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-de89e2f9e9 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-de89e2f9e9-s0-h0-d31e2c/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-de89e2f9e9 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-de89e2f9e9-s1-h0-8405a6/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-de89e2f9e9 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-de89e2f9e9-s2-h0-b559e5/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 0 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f36d0647d5 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f36d0647d5-s0-h0-9bcbec/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f36d0647d5 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f36d0647d5-s1-h0-e780e0/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f36d0647d5 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f36d0647d5-s2-h0-1ea50a/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 1 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 1 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f81f88234e / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f81f88234e-s0-h0-6ae71b/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f81f88234e / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f81f88234e-s1-h0-91f454/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f81f88234e / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f81f88234e-s2-h0-c96f53/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 1 | 1 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 1 |
| ts-order-service | 0 | 1 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f9a8e05ed7 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f9a8e05ed7-s0-h0-b1602d/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f9a8e05ed7 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f9a8e05ed7-s1-h0-6762a3/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-f9a8e05ed7 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f9a8e05ed7-s2-h0-9a28eb/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 1 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 0 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 1 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 1 |
| ts-seat-service | 0 | 0 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 0 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 0 | 0 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 1 | 1 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-fbc45b0c67 / seed 0

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-fbc45b0c67-s0-h0-e74e74/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-fbc45b0c67 / seed 1

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-fbc45b0c67-s1-h0-e852cc/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## RE2-TT / TORAI B / dev-fbc45b0c67 / seed 2

L/|O|=68/68; availability=available; reason=None. Nguồn bản ghi: `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-fbc45b0c67-s2-h0-b790bc/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| ts-admin-basic-info-service | 0 | 0 |
| ts-admin-order-service | 0 | 0 |
| ts-admin-route-service | 0 | 0 |
| ts-admin-travel-service | 0 | 0 |
| ts-admin-user-service | 0 | 0 |
| ts-assurance-mongo | 0 | 0 |
| ts-assurance-service | 0 | 0 |
| ts-auth-mongo | 0 | 0 |
| ts-auth-service | 0 | 0 |
| ts-avatar-service | 0 | 0 |
| ts-basic-service | 0 | 1 |
| ts-cancel-service | 0 | 0 |
| ts-config-mongo | 0 | 0 |
| ts-config-service | 0 | 0 |
| ts-consign-mongo | 0 | 0 |
| ts-consign-price-mongo | 0 | 0 |
| ts-consign-price-service | 0 | 0 |
| ts-consign-service | 0 | 0 |
| ts-contacts-mongo | 0 | 0 |
| ts-contacts-service | 0 | 0 |
| ts-execute-service | 0 | 0 |
| ts-food-map-mongo | 0 | 0 |
| ts-food-map-service | 0 | 0 |
| ts-food-mongo | 0 | 0 |
| ts-food-mysql | 0 | 0 |
| ts-food-service | 0 | 0 |
| ts-inside-payment-mongo | 0 | 0 |
| ts-inside-payment-service | 0 | 0 |
| ts-news-service | 0 | 0 |
| ts-notification-mongo | 0 | 0 |
| ts-notification-service | 0 | 0 |
| ts-order-mongo | 0 | 0 |
| ts-order-other-mongo | 0 | 0 |
| ts-order-other-service | 0 | 0 |
| ts-order-service | 0 | 0 |
| ts-payment-mongo | 0 | 0 |
| ts-payment-service | 0 | 0 |
| ts-preserve-mongo | 0 | 0 |
| ts-preserve-other-mongo | 0 | 0 |
| ts-preserve-other-service | 0 | 0 |
| ts-preserve-service | 0 | 0 |
| ts-price-mongo | 0 | 0 |
| ts-price-service | 0 | 0 |
| ts-rebook-service | 0 | 0 |
| ts-route-mongo | 0 | 0 |
| ts-route-plan-service | 0 | 0 |
| ts-route-service | 0 | 0 |
| ts-seat-service | 0 | 1 |
| ts-security-mongo | 0 | 0 |
| ts-security-service | 0 | 0 |
| ts-station-mongo | 0 | 0 |
| ts-station-service | 0 | 0 |
| ts-ticket-office-mongo | 0 | 0 |
| ts-ticket-office-service | 0 | 0 |
| ts-ticketinfo-service | 0 | 1 |
| ts-train-mongo | 0 | 0 |
| ts-train-service | 1 | 1 |
| ts-travel-mongo | 0 | 0 |
| ts-travel-plan-service | 0 | 0 |
| ts-travel-service | 0 | 0 |
| ts-travel2-mongo | 0 | 0 |
| ts-travel2-service | 0 | 1 |
| ts-ui-dashboard | 0 | 0 |
| ts-user-mongo | 0 | 0 |
| ts-user-service | 0 | 0 |
| ts-verification-code-service | 0 | 0 |
| ts-voucher-mysql | 0 | 0 |
| ts-voucher-service | 0 | 0 |

## Nezha-OB / BARO / dev-14701a3bbb / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-14701a3bbb-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 1 | 1 |

## Nezha-OB / BARO / dev-1ac905bc95 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-1ac905bc95-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 1 | 1 |

## Nezha-OB / BARO / dev-27252dca60 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-27252dca60-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / BARO / dev-2bfc97b01e / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/baro-main-dev-2bfc97b01e-h0-lower_median/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 1 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-396c8dbf7d / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 1 | 1 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-3b92690644 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-3b92690644-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 1 | 1 |

## Nezha-OB / BARO / dev-3e27669440 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-3e27669440-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 1 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-515c5f2190 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-515c5f2190-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 1 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / BARO / dev-5467884de4 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-5467884de4-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / BARO / dev-55f99f3e0a / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/baro-main-dev-55f99f3e0a-h0-smallest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-5ada15752d / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-5ada15752d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-607751ac0a / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-607751ac0a-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 1 | 1 |

## Nezha-OB / BARO / dev-63c30faf34 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-63c30faf34-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-6c9afc9822 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-6c9afc9822-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-70629373f9 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-70629373f9-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 1 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / BARO / dev-7b7c973198 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-7b7c973198-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / BARO / dev-7d3c2fe6d1 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 1 | 1 |

## Nezha-OB / BARO / dev-8ecd9880ed / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/baro-main-dev-8ecd9880ed-h0-largest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 1 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-95e164235f / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-95e164235f-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 1 | 1 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-9b9397a4dc / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 1 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / BARO / dev-9fd793feb7 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-9fd793feb7-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / BARO / dev-b0f8b2e3ac / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/baro-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-14701a3bbb / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-14701a3bbb-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0.5 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0.5 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 1 | 1 |

## Nezha-OB / SimpleRCA / dev-1ac905bc95 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-1ac905bc95-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0.5 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 0.5 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-27252dca60 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/simplerca-main-dev-27252dca60-h0-smallest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-2bfc97b01e / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-2bfc97b01e-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-396c8dbf7d / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0.5 |
| cartservice | 0 | 0 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 0.5 |
| emailservice | 0 | 1 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0.5 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0.5 |

## Nezha-OB / SimpleRCA / dev-3b92690644 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-3b92690644-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-3e27669440 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-3e27669440-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 1 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0.5 |
| frontend | 0 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0.5 |

## Nezha-OB / SimpleRCA / dev-515c5f2190 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-515c5f2190-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 1 | 1 |
| cartservice | 0 | 0.166667 |
| checkoutservice | 0 | 0.166667 |
| currencyservice | 0 | 0.166667 |
| emailservice | 0 | 0.166667 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0.166667 |
| productcatalogservice | 0 | 0.166667 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-5467884de4 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-5467884de4-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-55f99f3e0a / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-55f99f3e0a-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0.5 |
| shippingservice | 0 | 0.5 |

## Nezha-OB / SimpleRCA / dev-5ada15752d / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-5ada15752d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 1 | 1 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-607751ac0a / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/simplerca-main-dev-607751ac0a-h0-largest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-63c30faf34 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-63c30faf34-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0.5 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0.5 |
| frontend | 1 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-6c9afc9822 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-6c9afc9822-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 1 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-70629373f9 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-70629373f9-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0.5 |
| currencyservice | 0 | 0.5 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 1 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-7b7c973198 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-7b7c973198-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0.5 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0.5 | 1 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-7d3c2fe6d1 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0.5 |
| frontend | 0 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0.5 |
| shippingservice | 1 | 1 |

## Nezha-OB / SimpleRCA / dev-8ecd9880ed / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-8ecd9880ed-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 1 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / SimpleRCA / dev-95e164235f / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-95e164235f-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 1 |
| frontend | 0 | 0 |
| paymentservice | 1 | 1 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-9b9397a4dc / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 0 |
| emailservice | 0 | 0.5 |
| frontend | 0 | 0 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0.5 |

## Nezha-OB / SimpleRCA / dev-9fd793feb7 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/simplerca-main-dev-9fd793feb7-h0-lower_median/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 0.5 |
| emailservice | 0 | 0 |
| frontend | 0 | 0 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 0.5 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / SimpleRCA / dev-b0f8b2e3ac / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/simplerca-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0.5 | 1 |
| emailservice | 0 | 0 |
| frontend | 0.5 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-14701a3bbb / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-14701a3bbb-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-1ac905bc95 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-1ac905bc95-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-27252dca60 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/microrank-main-dev-27252dca60-h0-smallest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-2bfc97b01e / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-2bfc97b01e-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-396c8dbf7d / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-3b92690644 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-3b92690644-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-3e27669440 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-3e27669440-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-515c5f2190 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-515c5f2190-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-5467884de4 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-5467884de4-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-55f99f3e0a / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-55f99f3e0a-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-5ada15752d / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-5ada15752d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-607751ac0a / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/microrank-main-dev-607751ac0a-h0-largest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-63c30faf34 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-63c30faf34-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-6c9afc9822 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-6c9afc9822-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-70629373f9 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-70629373f9-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-7b7c973198 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-7b7c973198-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-7d3c2fe6d1 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-8ecd9880ed / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-8ecd9880ed-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-95e164235f / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-95e164235f-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-9b9397a4dc / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-9fd793feb7 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/microrank-main-dev-9fd793feb7-h0-lower_median/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 1 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / MicroRank full / dev-b0f8b2e3ac / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/microrank-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 1 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-14701a3bbb / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-14701a3bbb-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-1ac905bc95 / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-1ac905bc95-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 1 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-27252dca60 / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/tracerca-main-dev-27252dca60-h0-smallest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-2bfc97b01e / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-2bfc97b01e-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-396c8dbf7d / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0.333333 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0.333333 | 1 |
| frontend | 0.333333 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-3b92690644 / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-3b92690644-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-3e27669440 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-3e27669440-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 1 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-515c5f2190 / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-515c5f2190-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-5467884de4 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-5467884de4-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-55f99f3e0a / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-55f99f3e0a-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-5ada15752d / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-5ada15752d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0 | 1 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-607751ac0a / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/tracerca-main-dev-607751ac0a-h0-largest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 1 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-63c30faf34 / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-63c30faf34-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-6c9afc9822 / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-6c9afc9822-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 0.5 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0.5 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-70629373f9 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-70629373f9-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 1 |
| checkoutservice | 1 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-7b7c973198 / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-7b7c973198-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-7d3c2fe6d1 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-8ecd9880ed / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-8ecd9880ed-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0.5 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0.5 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 0 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-95e164235f / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-95e164235f-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 1 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / TraceRCA / dev-9b9397a4dc / seed single

L/|O|=9/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 0 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 1 | 1 |
| shippingservice | 0 | 1 |

## Nezha-OB / TraceRCA / dev-9fd793feb7 / seed single

L/|O|=10/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/pilot-001/tracerca-main-dev-9fd793feb7-h0-lower_median/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 0 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 0 |
| recommendationservice | 0 | 1 |
| shippingservice | 1 | 1 |

## Nezha-OB / TraceRCA / dev-b0f8b2e3ac / seed single

L/|O|=8/10; availability=available; reason=None. Nguồn bản ghi: `results/T-026/runs/full-001/tracerca-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |
| adservice | 0 | 0 |
| cartservice | 0 | 0 |
| checkoutservice | 0 | 1 |
| currencyservice | 1 | 1 |
| emailservice | 0 | 0 |
| frontend | 0 | 1 |
| paymentservice | 0 | 0 |
| productcatalogservice | 0 | 1 |
| recommendationservice | 0 | 1 |
| shippingservice | 0 | 0 |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-14701a3bbb / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-14701a3bbb-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-1ac905bc95 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-1ac905bc95-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-27252dca60 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-27252dca60-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-2bfc97b01e / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/pilot-001/circa-main-dev-2bfc97b01e-h0-lower_median/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-396c8dbf7d / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-3b92690644 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-3b92690644-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-3e27669440 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-3e27669440-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-515c5f2190 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-515c5f2190-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-5467884de4 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-5467884de4-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-55f99f3e0a / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/pilot-001/circa-main-dev-55f99f3e0a-h0-smallest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-5ada15752d / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-5ada15752d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-607751ac0a / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-607751ac0a-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-63c30faf34 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-63c30faf34-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-6c9afc9822 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-6c9afc9822-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-70629373f9 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-70629373f9-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-7b7c973198 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-7b7c973198-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-7d3c2fe6d1 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-8ecd9880ed / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/pilot-001/circa-main-dev-8ecd9880ed-h0-largest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-95e164235f / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-95e164235f-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-9b9397a4dc / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-9fd793feb7 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-9fd793feb7-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / CIRCA OLS+RHT+DA / dev-b0f8b2e3ac / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/circa-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-14701a3bbb / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-14701a3bbb-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-1ac905bc95 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-1ac905bc95-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-27252dca60 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-27252dca60-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-2bfc97b01e / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/pilot-001/torai_B-main-dev-2bfc97b01e-h0-lower_median/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-396c8dbf7d / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-3b92690644 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-3b92690644-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-3e27669440 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-3e27669440-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-515c5f2190 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-515c5f2190-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-5467884de4 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-5467884de4-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-55f99f3e0a / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/pilot-001/torai_B-main-dev-55f99f3e0a-h0-smallest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-5ada15752d / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-5ada15752d-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-607751ac0a / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-607751ac0a-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-63c30faf34 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-63c30faf34-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-6c9afc9822 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-6c9afc9822-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-70629373f9 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-70629373f9-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-7b7c973198 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-7b7c973198-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-7d3c2fe6d1 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-8ecd9880ed / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/pilot-001/torai_B-main-dev-8ecd9880ed-h0-largest/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-95e164235f / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-95e164235f-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-9b9397a4dc / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-9fd793feb7 / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-9fd793feb7-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

## Nezha-OB / TORAI B / dev-b0f8b2e3ac / seed single

L/|O|=0/0; availability=N/A; reason=unsupported. Nguồn bản ghi: `results/T-026/runs/full-001/torai_B-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json`.

| Entity (giữ mapping) | p1 | p5 |
| --- | --- | --- |

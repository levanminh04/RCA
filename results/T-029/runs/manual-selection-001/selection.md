# Danh sách đọc tay ghi trước khi đọc

Trong từng bộ, chọn hai mã mờ nhỏ nhất mỗi cơ chế/tổ hợp cờ chính có ca; bao phủ thêm từng cờ độ nhạy đã khóa. Lấy hợp với mọi S, D0 và mọi ca của V7 bằng nhau đúng số ở cấp ca/ô/root/fault/toàn mẫu. Không đặt ngưỡng gần bằng; không chọn theo kết quả mong muốn. Đọc theo mã mờ rồi bộ phát hiện.

Nguồn: theo-ca.json#/rows và runs/step5-001/V7.json#/cases, #/aggregate. selection.json giữ lý do và con trỏ dòng.

| Ca | Bộ | Ô | Lý do |
|---|---|---|---|
| dev-03d4910932 | bocpd | ts-route-service / socket | V7 không phân biệt đúng số: case//B1; mã mờ nhỏ nhất: bocpd/cơ chế/B2; mã mờ nhỏ nhất: bocpd/tổ hợp/B2; mã mờ nhỏ nhất: bocpd/độ nhạy/B2/2; mã mờ nhỏ nhất: bocpd/độ nhạy/B2/5 |
| dev-03d4910932 | nsigma | ts-route-service / socket | mã mờ nhỏ nhất: nsigma/cơ chế/N3; mã mờ nhỏ nhất: nsigma/tổ hợp/N3; mã mờ nhỏ nhất: nsigma/độ nhạy/N3/10; mã mờ nhỏ nhất: nsigma/độ nhạy/N3/20; mã mờ nhỏ nhất: nsigma/độ nhạy/N3/5 |
| dev-03d4910932 | nsigma_doi_chung | ts-route-service / socket | mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N2; mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N2; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N2/10; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N2/5; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N3/20 |
| dev-12a1a88069 | bocpd | ts-order-service / disk | mã mờ nhỏ nhất: bocpd/cơ chế/B2; mã mờ nhỏ nhất: bocpd/cơ chế/B4; mã mờ nhỏ nhất: bocpd/tổ hợp/B2+B4; mã mờ nhỏ nhất: bocpd/độ nhạy/B2/10; mã mờ nhỏ nhất: bocpd/độ nhạy/B2/2; mã mờ nhỏ nhất: bocpd/độ nhạy/B2/5; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w15/k2; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w15/k3; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w15/k5; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w30/k2; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w30/k3; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w30/k5; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w60/k2; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w60/k3; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w60/k5 |
| dev-12a1a88069 | nsigma | ts-order-service / disk | mã mờ nhỏ nhất: nsigma/cơ chế/N1; mã mờ nhỏ nhất: nsigma/cơ chế/N3; mã mờ nhỏ nhất: nsigma/tổ hợp/N1+N3; mã mờ nhỏ nhất: nsigma/độ nhạy/N1/1.5; mã mờ nhỏ nhất: nsigma/độ nhạy/N1/2.0; mã mờ nhỏ nhất: nsigma/độ nhạy/N2/5; mã mờ nhỏ nhất: nsigma/độ nhạy/N3/10; mã mờ nhỏ nhất: nsigma/độ nhạy/N3/20 |
| dev-12a1a88069 | nsigma_doi_chung | ts-order-service / disk | mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N2; mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N2; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N1/1.5; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N2/10; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N2/20; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N2/5 |
| dev-14372e1209 | bocpd | ts-route-service / mem | mã mờ nhỏ nhất: bocpd/tổ hợp/D0; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w30/k2; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w60/k2; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w60/k3; mọi D0 |
| dev-14372e1209 | nsigma | ts-route-service / mem | mã mờ nhỏ nhất: nsigma/cơ chế/N1; mã mờ nhỏ nhất: nsigma/tổ hợp/N1+N3; mã mờ nhỏ nhất: nsigma/độ nhạy/N1/1.5; mã mờ nhỏ nhất: nsigma/độ nhạy/N1/2.0; mã mờ nhỏ nhất: nsigma/độ nhạy/N1/3.0; mã mờ nhỏ nhất: nsigma/độ nhạy/N3/5 |
| dev-14372e1209 | nsigma_doi_chung | ts-route-service / mem | mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N1; mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N1+N2; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N1/1.5; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N1/2.0; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N2/20 |
| dev-16597725c1 | bocpd | ts-auth-service / cpu | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: case//B4/w60/k2; mã mờ nhỏ nhất: bocpd/cơ chế/B4; mã mờ nhỏ nhất: bocpd/tổ hợp/B2+B4; mã mờ nhỏ nhất: bocpd/độ nhạy/B2/10; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w15/k2; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w15/k3; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w30/k3 |
| dev-16597725c1 | nsigma | ts-auth-service / cpu | mã mờ nhỏ nhất: nsigma/tổ hợp/N3; mã mờ nhỏ nhất: nsigma/độ nhạy/N2/5 |
| dev-16597725c1 | nsigma_doi_chung | ts-auth-service / cpu | mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N3/20 |
| dev-16870e660c | bocpd | ts-route-service / mem | V7 không phân biệt đúng số: case//B1; mã mờ nhỏ nhất: bocpd/tổ hợp/D0; mọi D0 |
| dev-1e6d61b5ec | bocpd | ts-order-service / disk | mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w60/k5 |
| dev-20acb4402d | bocpd | ts-order-service / loss | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: cell/ts-order-service|loss/B1 |
| dev-260d332c8d | bocpd | ts-order-service / loss | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: cell/ts-order-service|loss/B1 |
| dev-3ae0a6c15a | bocpd | ts-train-service / cpu | mọi D0 |
| dev-3ae0a6c15a | nsigma | ts-train-service / cpu | mã mờ nhỏ nhất: nsigma/cơ chế/N2; mã mờ nhỏ nhất: nsigma/tổ hợp/N2; mã mờ nhỏ nhất: nsigma/độ nhạy/N2/10 |
| dev-3defe3d34b | bocpd | ts-auth-service / cpu | mọi D0; mọi S |
| dev-3defe3d34b | nsigma_doi_chung | ts-auth-service / cpu | mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N1; mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N4; mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N1+N2+N4; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N1/2.0; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N4 |
| dev-4e68956051 | bocpd | ts-train-service / delay | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: cell/ts-train-service|delay/B1; mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w30/k5 |
| dev-4f8a844308 | bocpd | ts-route-service / mem | mã mờ nhỏ nhất: bocpd/độ nhạy/B4/w15/k5 |
| dev-57546fd87b | bocpd | ts-auth-service / delay | mã mờ nhỏ nhất: bocpd/tổ hợp/B2 |
| dev-59f696a169 | nsigma | ts-auth-service / cpu | mã mờ nhỏ nhất: nsigma/cơ chế/N2; mã mờ nhỏ nhất: nsigma/tổ hợp/N2; mã mờ nhỏ nhất: nsigma/độ nhạy/N2/10 |
| dev-746fd74313 | bocpd | ts-auth-service / delay | V7 không phân biệt đúng số: case//B4/w60/k2; mã mờ nhỏ nhất: bocpd/tổ hợp/B4 |
| dev-746fd74313 | nsigma | ts-auth-service / delay | mã mờ nhỏ nhất: nsigma/độ nhạy/N2/20 |
| dev-746fd74313 | nsigma_doi_chung | ts-auth-service / delay | mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N4; mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N2+N4; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N4 |
| dev-7f1b6b071d | bocpd | ts-travel-service / loss | V7 không phân biệt đúng số: case//B1; mọi D0 |
| dev-8017c6dc70 | bocpd | ts-order-service / disk | V7 không phân biệt đúng số: case//B1 |
| dev-98bc73c499 | bocpd | ts-train-service / cpu | mọi D0; mọi S |
| dev-98bc73c499 | nsigma | ts-train-service / cpu | mã mờ nhỏ nhất: nsigma/độ nhạy/N1/3.0 |
| dev-a505ab3f65 | bocpd | ts-train-service / delay | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: cell/ts-train-service|delay/B1 |
| dev-a5cabe5fa7 | bocpd | ts-travel-service / loss | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: case//B4/w60/k2 |
| dev-a915aa2424 | bocpd | ts-travel-service / loss | mã mờ nhỏ nhất: bocpd/tổ hợp/B4 |
| dev-a915aa2424 | nsigma | ts-travel-service / loss | mã mờ nhỏ nhất: nsigma/độ nhạy/N2/20 |
| dev-ba831dbeb8 | bocpd | ts-train-service / cpu | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: case//B4/w60/k2 |
| dev-bcbd4f46ae | nsigma_doi_chung | ts-route-service / socket | mã mờ nhỏ nhất: nsigma_doi_chung/cơ chế/N3; mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N1+N3; mã mờ nhỏ nhất: nsigma_doi_chung/độ nhạy/N3/10 |
| dev-de89e2f9e9 | bocpd | ts-travel-service / disk | mọi D0 |
| dev-f36d0647d5 | bocpd | ts-order-service / loss | V7 không phân biệt đúng số: cell/ts-order-service|loss/B1; mọi D0; mọi S |
| dev-f36d0647d5 | nsigma | ts-order-service / loss | mã mờ nhỏ nhất: nsigma/tổ hợp/N1+N2 |
| dev-f81f88234e | nsigma_doi_chung | ts-auth-service / delay | mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N2+N4 |
| dev-f9a8e05ed7 | nsigma_doi_chung | ts-travel-service / disk | mã mờ nhỏ nhất: nsigma_doi_chung/tổ hợp/N1+N2 |
| dev-fbc45b0c67 | bocpd | ts-train-service / delay | V7 không phân biệt đúng số: case//B1; V7 không phân biệt đúng số: cell/ts-train-service|delay/B1 |

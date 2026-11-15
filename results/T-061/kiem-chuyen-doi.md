# Kiểm bộ chuyển đổi (T-061)

Lệnh: trong `results/T-061/`, `bash chay-tat-ca.sh && py -3 -B kiem.py`. Kết quả máy ghi ở [`kiem-ket-qua.json`](kiem-ket-qua.json): **110/110 phép kiểm đạt** ở bản 0.2 (`/so_phep_kiem` = 110, `/so_hong` = 0; bản 0.1 trước đó 89/89; 107/107 trước khi thêm file chỉ mục). Mỗi dòng dưới đây ứng với một mục trong `/ket_qua[]` của file đó. File tạm ở `results/T-061/tmp-kiem/` (ghi đè mỗi lần chạy); mọi lệnh chạy với `-B`. Phép sinh bản ghi lỗi gọi môi trường đã ghim của M1 (`D:/RCA-ext/envs/py312-pin` + `T-016-cong-cu`, có numpy), khai ở đầu `kiem.py`.

Đầu vào kiểm hash theo `results/T-058/dem-2026-11-10/artifacts-sha256.json` (khớp): `rca-ban-dau/outputs/c12e47ab/method-output-1.json`, `rca-ban-dau/outputs/f4a8c021/method-output-1.json`, `rca-ban-dau/cases/{c12e47ab,f4a8c021}/request.json`, `src/m1/adapter_flashticket.py`; lớp phát lại thêm `m1-launch-record.json` (danh sách ca), `m1-execution-plan-v2.json`, `ledger-received.jsonl`. Hash nằm trong trường `nguon` của mỗi mẫu và trong `phat_lai.sha256_dap_an`.

## 1. Đối chiếu theo con trỏ JSON (cả hai ca)

So từng giá trị, không chỉ tên trường hay số phần tử. "=" là bằng nhau sau khi đọc JSON.

| Con trỏ M1 | Trường định dạng | Phép so | c12e47ab | f4a8c021 |
|---|---|---|---|---|
| `/verdict` | `su_co.ket_luan` | = | `NO_INTRINSIC_ANOMALY` | `CAUSE_FOUND` |
| `/mode` | `su_co.che_do` | = | `a` | `a` |
| `/status`, `/error` | `su_co.trang_thai`, `loi` | = | `OK`, null | `OK`, null |
| `/method_version` | `nguon.method_version` | = | `M1-T046-1` | `M1-T046-1` |
| `/config_id` | `nguon.config_id` | = | `M1` | `M1` |
| `/window/N`, `/window/A` | `su_co.cua_so_nen/su_co.{tu,den}_ns`; `moc.t_ns` = `/window/A/0` | = | 22:01:00–22:06:00–22:11:00Z | 22:12:28–22:17:28–22:22:28Z |
| (đơn vị) | ns → ms | mọi mốc chia hết 10^6 | đạt | đạt |
| `/classes/*` | `nut[].lop_m1` | = với mọi thực thể; không thêm lớp | 17 × `binh_thuong` | api-gateway, ticket-service `tu_sinh`; config-discovery `ke_thua`; event-service `thieu_du_lieu`; 13 `binh_thuong` |
| `/sets/observed_entities` | ⊆ `nut[].id` | ⊆ | 17 | 17 |
| `/entity_ranking[].tie_group` | `nut.nhom_dong_hang`; `hang` = +1 | = với mọi thực thể có hạng | 17 thực thể, nhóm 0 | 16 thực thể, nhóm 0–3 |
| `/entity_ranking[].key` | `nut.khoa_m1` | = | đạt | đạt |
| (thiếu trong `/entity_ranking`) | `nut.hang` = null | = | không có | `event-service` |
| `/blocks[]` | `xep_hang[]` (thứ tự, thành viên, khóa) | = | 1 khối × 17 | 4 khối: 1, 1, 1, 13 |
| (cỡ khối) | `nut.so_dong_hang` | = số thực thể cùng `tie_group` | 17 | 1, 1, 1, 13 |
| `/extra/canh[i]` | `canh[i].nguon`, `canh[i].dich` | = từng đầu, giữ thứ tự và chiều | 8 | 8 |
| (tập cạnh) | `canh[]` | không có cạnh ngoài M1 | đạt | đạt |
| `/diagnostics/so_canh_tinh` | `canh[].nguon_goc` | 0 → `quan_sat` | 0 | 0 |
| `/evidence_refs` | tập `bang_chung[].don_vi` | = | [] | 8 đơn vị |
| `/extra/kenh_co[]` | `bang_chung[]` (mã, thực thể, kênh, hướng, lớp, s, F_I, khởi phát) | = từng phần tử, giữ thứ tự | 0 | 8 |
| (gắn bằng chứng) | `nut.bang_chung` = mục có cùng `thuc_the` | = | đạt | api-gateway 4, ticket-service 3, config-discovery 1 |
| `/region/T` | `vung.T_m1` | = nguyên văn | 17 thực thể | [api-gateway] |
| `/region/cach_1`, `cach_2`, `hop_cach_1`, `hop_cach_2` | `vung.*` | = khi CAUSE_FOUND; rỗng + `ly_do` khi không (M1 cũng rỗng) | rỗng, `ap_dung` = false | {api-gateway, config-discovery}; {+ ticket-service} |
| `/inherited_by[]` | `giai_thich_ke_thua[]` | = từng phần tử | 0 | đạt (config-discovery qua api-gateway → config-discovery) |
| `/sets/observed`, `/sets/returned`, `/do_phu_cham`, `/diagnostics/NO_VALID_CHANNEL` | `do_phu.*` | = | 17, 17, 1.0, [] | 17, 16, 0.941…, [event-service] |
| `/RANK_CHANGED`, `/OBS_DEPENDENT` | `do_phu.hang_doi_giua_the_gioi`, `don_vi_phu_thuoc_quan_sat` | = | false, [] | false, [] |
| (file) | `nguon.sha256_m1` | = hash tính lại = manifest T-058 | đạt | đạt |

Quy tắc hiển thị kiểm cùng lượt: nút nổi bật ⇔ nhóm 0 và `tu_sinh`; màu chỉ phụ thuộc vai trò; mốc chế độ `a` ghi nguồn bộ điều phối.

## 2. Bốn điều phải giữ (SPEC)

| Điều | Kết quả |
|---|---|
| Ca `c12e47ab`: `NO_INTRINSIC_ANOMALY`, 17 thực thể đồng hạng (một nhóm, `so_dong_hang` = 17), bằng chứng rỗng; không nút nào nổi bật, nghi nguồn hay gốc vùng dù cả 17 "đứng đầu" (`vung.T_m1` có 17, `ap_dung` = false) | Đạt |
| Ca `f4a8c021`: `CAUSE_FOUND`, 16 thực thể có hạng; event-service vai trò `thieu_du_lieu`, `hang` null, màu `#CA95E5`, chữ `?`; dự đoán M1 giữ nguyên (api-gateway hạng 1 nổi bật, ticket-service hạng 2 nghi nguồn, config-discovery hạng 3 bị kéo theo) | Đạt |
| Cả hai ca chế độ `a`: "Mốc tham chiếu do bộ điều phối cấp (chế độ a). RCA và Grafana không tự phát hiện mốc này." | Đạt |
| Liên kết chỉ sinh khi có truy vấn/định danh: ca `f4a8c021` có 4 liên kết metric (truy vấn nguyên văn của adapter) và 4 tìm kiếm TraceQL theo tên span; ca `c12e47ab` không có bằng chứng nên không có liên kết; không trace ID, không dòng log | Đạt |

## 3. Phần tử M1 không đưa vào bản 0.2

Mọi khóa cấp một của `method-output-1.json` và của `/extra` đã được xét. Phần tử không có trong bảng §1 là phần bị bỏ, kèm lý do.

| Phần tử | Lý do bỏ | Mất gì |
|---|---|---|
| `/coverage` (59 mục: độ phủ thời gian từng kênh) | Chi tiết kỹ thuật theo kênh; kết luận độ phủ mức thực thể đã có ở `do_phu_cham`, `NO_VALID_CHANNEL` | Màn chi tiết độ phủ |
| `/worlds` (thứ tự, khối, đơn vị đếm ở P, S_lo, S_hi) | Hiện thứ tự thế giới P; tính ổn định giữa thế giới đã đưa qua `RANK_CHANGED` | Khối của S_lo, S_hi |
| `/ranking_native` | Rỗng ở cả hai ca (M1 không có thứ tự gốc riêng) | Không |
| `/diagnostics` ngoài các trường đã dùng (`span`, `E2_du_phong`, `nguon_metric_unsupported`, `cot_metric_chua_khai_nguon`, `E6b`, `so_cham_hop_le`, `gop_khoa_ghi_ra*`) | Chẩn đoán adapter/chuỗi, dành cho người kiểm phương pháp | Không ảnh hưởng hiển thị kết luận |
| `/extra/T4c` | Thứ tự thứ hai chỉ để báo cáo (T-043 CĐ7); hiện cạnh thứ tự chính dễ làm người xem nhầm hai bảng xếp hạng | Thứ tự T4c |
| `/extra/doi_chung` (C-d1, C-d2, C-d3), `/extra/dau_vao_cd3` | Kết quả của các phương pháp đối chứng, không phải kết luận M1 | So sánh với đối chứng |
| `/extra/don_vi_phan_vi` (169/176 đơn vị) | Chi tiết từng phép chấm phân vị; bằng chứng có cờ đã ở `kenh_co` | Phép chấm không có cờ |
| `/extra/kenh_co_the_gioi` | Kênh có cờ theo từng thế giới; thế giới P đã ở `bang_chung` | Kênh có cờ ở S_lo, S_hi |
| `/extra/thong_ke_log` | Số dòng log theo thực thể; chưa có quy tắc hiển thị | Bối cảnh log |
| `/extra/K_I_P`, `/extra/K_raw_P`, `/extra/blocks_P` | `blocks_P` trùng `/blocks`. `khoa_m1` chỉ giữ **một** trong hai khóa tùy tầng (tầng 1 dùng `K_I`, tầng 2 dùng `K_raw`, `src/m1/xep_hang.py:117–122`), kèm khóa phụ T4c. Ví dụ ca pause, config-discovery: `K_I_P` = [0, 0, 0], khóa xuất ra dùng `K_raw_P` (sửa câu "đã nằm trong khoa_m1" của bản 0.1 theo phản biện) | Khóa không dùng cho tầng của thực thể; mở đầu ra gốc khi cần |
| `/extra/G_N` | Chỉ để bộ đánh giá đếm M5 (chú thích trong `src/m1/chuoi.py`) | Không |
| `/extra/nhom_vong_P`, `/extra/E6b_pi` | Rỗng / null ở cả hai ca | Không |

`/extra/tang_P`, `/extra/canh`, `/extra/kenh_co`, `/extra/che_do` có dùng.

## 4. Phát lại và cách ly nhãn

| Phép kiểm | Kết quả |
|---|---|
| Bỏ khối `phat_lai` khỏi bản phát lại → trùng bản gốc ở mọi trường (cả hai ca) | Đạt |
| `phat_lai.sha256_ket_qua_truoc_ghep` = hash trong `mau/manifest-mau.json` (băm trước khi ghép) | Đạt |
| Khung Grafana bản phát lại = khung gốc + đúng một trường `detail__dap_an` | Đạt |
| Đổi đáp án giả sang `api-gateway`: `id`, `mainstat`, `secondarystat`, `color`, `highlighted`, `detail__hang`, `detail__vung` không đổi | Đạt |
| `chuyen-doi.py` (AST): không import và không có chuỗi trỏ tới `phat-lai`/`dap_an`, ngoài docstring và danh sách cấm đọc | Đạt |
| Hai mẫu không chứa `process_pause`, `operator_only_role`, `ledger`, `intervention`, `docker pause` | Đạt |
| `chuyen-doi.py --vao ledger-received.jsonl` bị từ chối, không ghi file | Đạt |
| Hiển thị thật: DOM của panel gốc và panel phát lại trùng ở cả hai ca ([`hien-thi/dom-mau.json`](hien-thi/dom-mau.json), bản dựng từ dữ liệu trích từ trình duyệt) | Đạt |
| **Đợt (gói C2):** `/ids` của `m1-launch-record.json` = tập mẫu trong manifest mẫu; byte và mã ca khớp | Đạt |
| Mã trùng trong danh sách; danh sách thiếu một ca; thư mục mẫu thiếu một ca; mẫu đổi byte sau khi băm; mã ca trong mẫu khác thư mục nguồn → đều dừng ở bước kiểm đợt | Đạt (5/5) |
| CLI: đợt thiếu ca với đường dẫn nguồn đáp án không tồn tại → dừng "trước khi mở nguồn đáp án" (chứng minh thứ tự: chưa đụng tới nguồn đáp án) | Đạt |
| Không có `__pycache__` mới trong `results/T-061/` và `results/T-058/.../src/m1/` sau toàn bộ lượt kiểm | Đạt |
| **Chỉ mục danh sách sự cố:** đủ mọi mẫu trong manifest mẫu, mỗi dòng trỏ đúng hash mẫu, mới nhất trước; mã/trạng thái/kết luận/nút nghi nguồn hạng 1 khớp từng mẫu; không chứa thông tin phát lại hay đáp án | Đạt (3/3) |

## 5. Tất định và ràng buộc ca

Chạy bộ chuyển đổi trên `method-output-2.json` (lần chạy M1 thứ hai, cùng SHA với lần một theo manifest T-058) cho kết quả trùng mẫu ở mọi trường trừ `nguon.file_m1`. Đầu ra không ghi giờ chuyển đổi.

| Phép kiểm (gói C1, C4) | Kết quả |
|---|---|
| `--ma-ca` khác thư mục chứa file M1 → từ chối | Đạt |
| `request.json` của ca khác → từ chối | Đạt |
| `t` của `request.json` lệch `/window/A/0` → từ chối | Đạt |
| Chế độ khác `a` → từ chối | Đạt |
| `NO_EVIDENCE` dựng trong bộ nhớ theo hình dạng `src/m1/chuoi.py:647–700` (không khối nào, mọi thực thể không có kênh OK): đạt schema; giữ cửa sổ và verdict `INSUFFICIENT_EVIDENCE`; mọi nút thiếu dữ liệu, không hạng; `xep_hang` rỗng | Đạt |
| `ERROR`, `UNSUPPORTED` sinh bằng chính `src/m1/chuoi.py::_ban_ghi_loi` (params của ca c12e47ab; M1 trả `mode = a`, cửa sổ và verdict rỗng): đạt schema; trạng thái và thông báo lỗi giữ nguyên; mốc lấy từ `request.json`; không nút/cạnh/hạng | Đạt (2/2) |
| Khung Grafana dựng được với 0 nút; panel bản ghi sự cố ghi trạng thái, lỗi, verdict "—" | Đạt (2/2) — kiểm ở mức khung và chữ; chưa vẽ trên Grafana |

## 6. Lỗi gặp khi tự kiểm (giữ lại để truy vết)

- Phép kiểm cách ly bản đầu so chuỗi thô và hỏng vì docstring nhắc `phat-lai.py`; bản AST thứ hai hỏng vì `khoi_phat` chứa "phat", rồi vì `dap-an` trong danh sách cấm đọc. Cả ba là dương tính giả của phép kiểm, đã thu hẹp phép kiểm; bộ chuyển đổi không đổi.
- Một lần kiểm Grafana qua API bị "mojibake" do stdin cp1252 của lệnh kiểm, không phải dữ liệu Grafana; xác nhận lại bằng cách đọc trường đã giải mã.
- Phiên 1 ghi ngoài phạm vi: `importlib` sinh `results/T-058/dem-2026-11-10/src/m1/__pycache__/adapter_flashticket.cpython-312.pyc`; `kiem.py` dùng thư mục tạm của Windows. Đã hoàn tác (xóa đúng file `.pyc` và thư mục rỗng, gói C) và sửa: adapter nạp từ byte đã kiểm, `-B`, file tạm trong `tmp-kiem/`.
- Bản 0.2, lần chạy đầu: phép kiểm CLI phát lại hỏng vì thông báo `SystemExit` ra stderr bị mã hóa cp1252 (`-I` bỏ qua `PYTHONIOENCODING`); bộ phát lại đã dừng đúng chỗ. Sửa: bộ phát lại in thông báo qua stdout UTF-8 và trả mã 2.

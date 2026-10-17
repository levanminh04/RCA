# Kiểm đúng đắn — T-040

Lượt hiện hành: `runs/tong-hop-011/` (Phiên 8: không đổi mã; snapshot quyết định thêm Q-174, Q-175; mọi số trùng run 010, `runs/tong-hop-011/so-sanh-010-011.json`). Kết quả kiểm: `runs/tong-hop-011/kiem-tra-002.json` (lượt cuối; `kiem-tra-001.json` là lượt trước). Lượt `runs/tong-hop-010/kiem-tra-003.json` không đạt K5 đúng thiết kế: DECISIONS có thêm Q-174, Q-175 sau snapshot của run 010. Thử điều kiện đạt: `runs/tong-hop-010/thu-r5.json`; thử hai nhánh dừng: `runs/tong-hop-009/thu-r4.json`. Run 010, 009, 008, 007 và 005 giữ làm lịch sử. Mọi lượt, kể cả lượt lỗi, được giữ (mục 5).

## 1. Kiểm đầu vào (`tong_hop.py`, bước 1)

| Phép kiểm | Kết quả | Con trỏ |
|---|---|---|
| Băm từng tệp theo 9 manifest (T-034, T-035, T-036 R1, T-036 V2, artifact V2, T-037, T-038, run sửa R1 của T-038, T-039) | 8 khớp toàn bộ; manifest R1 của T-036 lệch đúng 3 tệp `src/do_thi_tinh/`, khớp thay đổi đã duyệt | `dau-vao.json#/manifest`, `#/manifest_khop_toan_bo` |
| Pin chung của ba nhánh | Cùng đường dẫn, SHA, `created_utc`, hash mã với manifest V2 | `dau-vao.json#/pin_chung` |
| Mã chung hiện hành | Ba tệp khớp hash pin V2 | `dau-vao.json#/ma_chung_hien_hanh` |
| B16 FlashTicket | Khớp registry T-037; repo platform ở commit đã ghim, B16 không sửa | `dau-vao.json#/flashticket` |
| Điều kiện đạt đầu vào (R5) | Từ run 010, `all_checks_pass` gồm B16, ba trường pin của từng nhánh, mã chung từng tệp, đồng bộ graph gốc T-038 với model bản sửa (`dau-vao.json#/kiem_trang_thai`). Tệp ngoài manifest chỉ báo cáo vì không phải đầu vào được đọc. Thử trong bộ nhớ: 14 trường đổi lần lượt đều làm không đạt và báo đúng tên; tệp ngoài manifest giả vẫn đạt. Trước run 010 các kiểm này chỉ được ghi, không chặn; chưa tìm thấy bằng chứng chúng làm sai số đã xuất bản. Từng có lệch phiên bản graph gốc được ghi nhận và tránh dùng: run 005 ghi phép chiếu gốc 121 cạnh so với 122 của bản hiện hành (`runs/tong-hop-005/dau-vao.json#/tep_goc_TT_lech_ban_hien_hanh`) | `runs/tong-hop-010/thu-r5.json` |
| Trạng thái chấp nhận | Q-149/158/164/165/167/171 có mặt; T-038 R1 đã có phản hồi người làm; manifest T-038 là ảnh chụp trước Q-171 (`CHO_KIEM_BAN_SUA`); các dòng DECISIONS nhắc T-038 khớp snapshot đã đọc `runs/tong-hop-009/doc-quyet-dinh.json` (thêm Q-172 so với snapshot run 008) (phép so chỉ phát hiện thêm/sửa/xóa, không suy nghiệm thu); T-035 không có REVIEW | `dau-vao.json#/kiem_trang_thai`, `#/doi_chieu_quyet_dinh_T038` |
| Tệp ngoài manifest | Không có (run đề nghị sửa của reviewer nay nằm trong manifest T-038 nhưng không được dùng làm số; K5 chặn) | `dau-vao.json#/tep_ngoai_manifest` |
| Bản dự kiến lẫn bản hiện hành | Graph gốc `results/T-038/do-thi/` cùng byte với model run sửa R1 | `dau-vao.json#/tep_goc_TT_dong_bo_model_sua` |
| Thay đổi so với Phiên 6 | Không số nào đổi; `tong-hop.json` trùng run 009 sau chuẩn hóa run; `dau-vao.json` thêm 14 khóa kiểm (đều đạt) và đổi đường dẫn snapshot quyết định (thêm Q-173) | `runs/tong-hop-010/so-sanh-009-010.json#/tom_tat` |
| Thay đổi so với Phiên 5 | Không số nào đổi; `tong-hop.json` trùng run 008 ngoài trường run; `dau-vao.json` chỉ đổi đường dẫn snapshot quyết định | `runs/tong-hop-009/so-sanh-008-009.json#/tom_tat` |
| Hành vi dừng (R4) | Đầu vào không đạt (snapshot run 008 gặp Q-172): thoát mã 2, không chạy bước phụ thuộc, bản hiện hành không đổi. Lỗi tính lại chèn giả: thoát mã 2, giữ chẩn đoán trong run, bản hiện hành không đổi | `runs/tong-hop-009/thu-r4.json#/nhanh_dau_vao/expect`, `#/nhanh_tinh_lai/expect` |
| Thay đổi so với Phiên 3 | Chỉ đổi chuỗi trạng thái TT (7 chỗ) và thêm phần lần theo mới; mọi số đã có giữ nguyên; hash 9 manifest như run 007 | `runs/tong-hop-008/so-sanh-007-008.json#/tom_tat` |
| Thay đổi so với Phiên 2 | Chỉ phía tĩnh TT đổi; T, giao, chỉ-có-ở-trace, mức thao tác, FT, OB, số lần theo giữ nguyên | `runs/tong-hop-007/so-sanh-005-007.json#/tom_tat` |

## 2. Tính lại tập và mẫu số (`tong_hop.py`, bước 3)

Với mỗi graph trong 1.069 TT và 132 OB, cả hai phép endpoints và typed:
- Dựng lại S, T từ danh sách thành viên; so với các danh sách đã lưu; tính lại giao, hai phần riêng, tử số, hai mẫu số và tỷ lệ; mẫu số 0 phải cho null.
- Kiểm phân hoạch: chỉ số cạnh của thành viên cộng loại trừ phải phủ đúng mọi cạnh của graph tĩnh và graph trace T-035, không trùng.
- Bản gốc của từng thành viên/loại trừ phải bằng cạnh tại chỉ số đó trong graph đầu vào.
- Khóa phía trace phải bằng ánh xạ đã khai của hai đầu; lý do loại trừ phải khớp trạng thái ánh xạ đúng đầu mút.
- Hash đầu vào và đầu ra khớp bảng tóm tắt nguồn; interval khớp graph đầu vào.

Kết quả: không có lỗi nào (`tong-hop.json#/he_thong/<hệ>/doi_chieu/loi_tinh_lai`). Từng graph: `runs/tong-hop-011/rows-TT.json.gz`, `rows-OB.json.gz`. Các graph giống nhau được nhóm theo vân tay (S, T), kèm danh sách thành viên (`runs/tong-hop-007/tong-hop-raw.json#/comparisons/<hệ>/families/<họ>/views/<view>/shape_members`). Không cộng cửa sổ lặp như bằng chứng độc lập; không lấy trung bình tỷ lệ.

## 3. Kiểm kết quả đã lưu (`kiem_tra.py`)

| Mã | Nội dung | Kết quả lượt cuối |
|---|---|---|
| K1 | Phép thử giả cho hàm tính lại: 7 đột biến trên mỗi mẫu (TT thực thể, OB thao tác) phải bị bắt; bản gốc không lỗi | Đạt |
| K2 | Đường tính thứ hai: kích thước và đại số tập từ danh sách S/T đã lưu (không qua thành viên), so với rows của T-040 | Đạt, 0 lệch ở cả hai hệ |
| K3 | Mọi số chép từ raw sang `tong-hop.json` khớp (429 cặp con trỏ) | Đạt |
| K3b | Số mô tả trích từ `results/T-035/thong-ke-do-thi.json` khớp con trỏ nguồn | Đạt |
| K4 | Sổ số liệu: mỗi số trong ba báo cáo có đoạn chữ, con trỏ trả đúng giá trị, và số hiện trong đoạn chữ | Đạt |
| K4b | Phép thử giả cho K4: đổi một giá trị trong sổ, hoặc xóa đoạn chữ trong báo cáo, phải bị bắt | Đạt |
| K5 | Không số nào lấy từ run đề nghị sửa của reviewer; mọi trường TT phụ thuộc S mang trạng thái có điều kiện (T-038 chưa nghiệm thu); kiểm quyết định theo snapshot khớp hiện hành, và phép thử giả (xóa một dòng, thêm, sửa, xóa hết) đều bị bắt | Đạt |
| K6 | Phạm vi ghi so với mốc Phiên 8 (`runs/tong-hop-010/baseline-phien8/`, chụp sau khi nối Q-175 và sửa đoạn tóm tắt STATE): STATE chỉ đổi dòng T-040; LOG và REVIEW chỉ nối thêm; SPEC không đổi; 183 tệp được bảo vệ không đổi; git status không có mục mới ngoài phạm vi | Đạt |

Số cụ thể của từng phép ở `runs/tong-hop-011/kiem-tra-002.json`.

## 4. Đối chiếu yêu cầu “Kiểm đúng đắn” của SPEC

- Tách endpoints/typed; tách cạnh thực thể, thao tác, phép chiếu và cạnh chỉ ở mức thực thể (đếm theo khóa cạnh đầy đủ, không theo cặp đầu mút): `tong-hop.json#/he_thong/<hệ>/mo_hinh_tinh/so_dem`.
- Mẫu số rỗng: T rỗng được giữ null ở typed và ở ảnh chụp 60 giây rỗng.
- Kiểu unknown: typed bỏ unknown; không lấy kiểu tĩnh lấp trace.
- Không nâng nghĩa: quan hệ thiết kế FT, binding tài nguyên và cạnh SMTP chưa phân kiểu không được gọi là cạnh tính toán đã xác nhận.
- DB logic/instance: giữ qua `resource_bindings`; metric dùng chung không nhân theo thao tác.
- OB: miền dev-adapter ở mọi graph; Node không được coi là host.
- Giới hạn lịch sử đã được Minh chấp nhận ở T-039 (Q-165) giữ nguyên; không mở lại nghiệm thu.

## 5. Mọi lượt chạy

| Run | Kết quả | Ghi chú |
|---|---|---|
| `runs/pilot-001/` | Lỗi | KeyError: tóm tắt T-039 dùng tử số/mẫu số thay cho S/T. Giữ nguyên |
| `runs/pilot-002/` | Đạt | 12 graph mỗi hệ, bỏ băm manifest |
| `runs/pilot-003/` | Đạt | 3 graph mỗi hệ; thử bước lần theo; phát hiện dấu hiệu TT không phân biệt nhóm |
| `runs/tong-hop-001/` | Đạt | Lượt đầy đủ đầu; thiếu kiểm artifact-manifest V2 |
| `runs/tong-hop-002/` | Đạt | Thêm artifact-manifest; entity-only theo khóa đầy đủ |
| `runs/tong-hop-003/` | Đạt; kiểm K3 **lỗi** | `kiem-tra-001.json` bắt lỗi ghi sổ con trỏ (thiếu `/views`) trong `tong_hop.py`; dữ liệu đặt đúng chỗ. Ảnh chụp trước khi ghi nằm ở `baseline/` |
| `runs/tong-hop-004/` | Đạt | Sửa con trỏ; mọi kiểm đạt |
| `runs/tong-hop-005/` | Đạt | Bản cuối Phiên 2 (TT phía tĩnh bị chặn bởi R1) |
| `runs/tong-hop-006/` | Tính đạt; kiểm trạng thái **lỗi** | Điều kiện “không có quyết định nghiệm thu T-038” chưa tính Q-169. Mốc phạm vi Phiên 3 ở `baseline/`. Lượt này vẫn ghi đè `tong-hop.json`, `dau-vao.json` hiện hành dù `all_checks_pass=false` (`runs/tong-hop-006/progress.jsonl` dòng 29–30); run 007 thay sau đó. Đây là lỗi luồng (R4), không phải bằng chứng số sai; phép kiểm trạng thái lúc đó còn lỗi R3 |
| `runs/tong-hop-007/` | Đạt | Bản trình phản biện; nguồn TT là bản sửa R1 của người làm T-038 |
| `runs/tong-hop-008/` | Đạt | Sửa theo REVIEW R1–R3 và N1–N4; mốc phạm vi Phiên 5 ở `baseline/`; snapshot quyết định đã đọc ở `doc-quyet-dinh.json` |
| `runs/thu-r4-dau-vao-001/` | Dừng đúng (thử R4) | Snapshot run 008 không khớp DECISIONS (Q-172); dừng ở cổng đầu vào, thoát mã 2, không ghi bản hiện hành |
| `runs/thu-r4-tinh-lai-001/` | Dừng đúng (thử R4) | Lỗi tính lại chèn giả vào TT; dừng ở cổng tính lại, giữ chẩn đoán, không ghi bản hiện hành |
| `runs/tong-hop-009/` | Đạt | Sửa R4; snapshot quyết định thêm Q-172; mốc phạm vi Phiên 6 ở `baseline/` |
| `runs/tong-hop-010/` | Đạt | Sửa R5; snapshot quyết định thêm Q-173; mốc phạm vi Phiên 7 ở `baseline/`, Phiên 8 ở `baseline-phien8/`; `kiem-tra-003.json` không đạt K5 vì có thêm Q-174, Q-175 (đúng thiết kế) |
| `runs/tong-hop-011/` | Đạt — **hiện hành** | Không đổi mã; snapshot quyết định thêm Q-174, Q-175 |

Stdout từng lượt đầy đủ: `runs/tong-hop-00N.stdout.txt`. Tiến độ từng bước: `progress.jsonl` trong mỗi run.

## 6. Tài nguyên thực đo

- Lượt hiện hành: thời gian và peak working set ở `runs/tong-hop-011/cost.json`; kiểm ở `runs/tong-hop-011/kiem-tra-002.json#/wall_s`, `#/peak_working_set_bytes`.
- Mỗi lượt đầy đủ băm toàn bộ tệp nguồn theo manifest (`cost.json#/bytes_hashed_manifests`, khoảng 1,8 GB từ Phiên 3).
- Dung lượng thư mục `results/T-040/`: `manifest.json#/total_bytes`.
- Không dùng EC2, GPU, tải dữ liệu, test/heldout, telemetry thô hoặc subagent.

## 7. Điều tự kiểm không bao phủ

- Không kiểm lại bộ dựng T-035/T-036 hay việc lập bản ghi của T-038 từ nguồn ứng dụng; dựa vào hash, manifest và trạng thái của task nguồn (T-035 chưa nghiệm thu; SMTP V2 chưa phản biện chính thức; T-038 chưa nghiệm thu).
- Không đọc span thô để phân xử nhóm checkout→currency hoặc năm cặp TT; phép cần thêm được nêu ở `con-mo.json`.
- Tự kiểm của người làm không thay phản biện chính thức của Codex.

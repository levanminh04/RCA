# Định dạng file và chỉ mục mà dashboard G2 đọc (T-062, phiên giao diện G1)

Dashboard đọc file qua Grafana của chính `exp-obs`: thư mục máy `/opt/flash-ticket-obs/rca-ket-qua/` được gắn vào container ở `public/rca` (T-061), nên Infinity gọi `http://localhost:3000/public/rca/...`. **Thả file đúng chỗ, đúng tên là hiện, không cần sửa dashboard hay khởi động lại Grafana.** Người xem chỉ cần tải lại trang (biến danh sách nạp lại khi mở dashboard).

## 1. Trang chính (không đáp án)

| Đường dẫn trên `exp-obs` | Nội dung | Ai sinh |
|---|---|---|
| `rca-ket-qua/<mã>.json` | Kết quả một sự cố, **định dạng 0.2 của T-061** (`results/T-061/dinh-dang-ket-qua-rca.md`), sinh bằng `results/T-061/chuyen-doi.py`. Tên file phải đúng `<mã ca>.json`, mã trùng `su_co.ma`. **Không có khối `phat_lai`.** | phiên điều phối (E2) |
| `rca-ket-qua/chi-muc/danh-sach-su-co.json` | Chỉ mục danh sách sự cố, **đúng định dạng T-061** (`results/T-061/chi-muc.py`, Minh duyệt 11/11/2026). Không đổi gì so với T-061 | phiên điều phối, bằng [`chi-muc-chinh.py`](chi-muc-chinh.py) |

`chi-muc-chinh.py` là bản của `results/T-061/chi-muc.py` nhận thư mục làm tham số (bản T-061 cố định `results/T-061/mau`). Đã kiểm: chạy trên hai mẫu T-061 cho ra file **trùng từng byte** với `results/T-061/mau/chi-muc/danh-sach-su-co.json` (có và không có manifest). Nó dừng nếu gặp file có khối `phat_lai` hoặc tên file khác mã ca.

```bash
py -3 -B results/T-062/giao-dien/chi-muc-chinh.py <thư mục chứa các <mã>.json> [manifest.json]
```

Khung file chỉ mục (giữ nguyên T-061):

```json
{"dinh_dang": "flashticket-rca-danh-sach", "phien_ban": "0.2",
 "su_co": [ {"ma": "f4a8c021", "t_ms": 1794349048000, "t_utc": "2026-11-10T22:17:28.000000000Z",
             "trang_thai": "OK", "ket_luan": "CAUSE_FOUND", "ket_luan_hien_thi": "…",
             "nghi_nguon_hang_1": "api-gateway", "so_thuc_the_quan_sat": 17, "so_thuc_the_co_hang": 16,
             "file": "f4a8c021.json", "sha256_file": "…"} ]}
```

Trường dashboard dùng: `ma`, `t_ms`, `t_utc`, `trang_thai`, `ket_luan_hien_thi`, `nghi_nguon_hang_1`, `so_thuc_the_quan_sat`, `so_thuc_the_co_hang`. Mảng `su_co` xếp mới nhất trước; dashboard giữ thứ tự đó. Khung giờ khi bấm một mã trong danh sách = `t_ms` ± 15 phút (đủ phủ chu kỳ 10/10/10); cửa sổ đúng của M1 lấy từ file sự cố (`cua_so_nen`, `cua_so_su_co`).

## 2. Trang phát lại (có đáp án, tách riêng)

| Đường dẫn trên `exp-obs` | Nội dung | Ai sinh |
|---|---|---|
| `rca-ket-qua/phat-lai/<mã>.phat-lai.json` | Bản phát lại của T-061 (`results/T-061/phat-lai.py`): định dạng 0.2 + khối `phat_lai`. Chỉ sinh **sau khi đã băm đầu ra cả đợt** | phiên điều phối |
| `rca-ket-qua/phat-lai/chi-muc/danh-sach-phat-lai.json` | Chỉ mục phát lại (mới, T-062) | phiên điều phối, bằng [`chi-muc-phat-lai.py`](chi-muc-phat-lai.py) |

```bash
py -3 -B results/T-062/giao-dien/chi-muc-phat-lai.py <thư mục chứa các <mã>.phat-lai.json>
```

Mỗi dòng gồm mọi trường của chỉ mục trang chính, cộng (bản sửa sau phản biện G1, F1′; `tasks/T-062-dem-chang-1-4/REVIEW-G1*.md`):

| Trường | Nghĩa |
|---|---|
| `dap_an_root` | `phat_lai.root_khai_truoc` nếu khóa có (T-062: với lỗi trên tuyến là **cạnh có hướng**, T-059); không có khóa thì `thanh_phan_tiem` (T-061); không có gì thì `—` |
| `dap_an_tap` | `phat_lai.tap_chap_nhan` nếu khóa có (kể cả rỗng); không có khóa thì `[thanh_phan_tiem]` hoặc `[]` |
| `m1_trong_tap` | chữ: vai trò/hạng M1 của **từng** thành phần trong tập (“tên: #h vai trò”; bình thường ghi hạng M1 kèm cỡ nhóm; thiếu dữ liệu ghi không có hạng; không quan sát ghi rõ); `—` khi tập rỗng |
| `hang_tot_nhat_e2` | chép `phat_lai.hang_tot_nhat` (số của e2, mức nút; không tính lại); null nếu không có |
| `hang_tot_nhat_e2_hien_thi` | chữ cho cột dashboard |
| `dap_an_ho_loi`, `dap_an_co_tiem`, `nhan_xet` | như cũ |
| `dap_an_thanh_phan`, `m1_vai_tro_cua_dap_an`, `m1_hang_cua_dap_an` | **cũ, giữ trong giai đoạn chuyển**, nghĩa không đổi: chỉ phần tử đầu của tập (`thanh_phan_tiem`). Dashboard mới không đọc, trừ khi chỉ mục chưa sinh lại (khi đó cột ghi “chỉ mục cũ”) |

Dashboard phát lại đánh dấu ◆ **mọi** thành phần thuộc tập chấp nhận; ◆ chỉ nghĩa “thuộc tập chấp nhận mức nút”, không khẳng định từng đầu là chỗ tiêm hay M1 định vị đúng cạnh. Panel đọc thẳng file `<mã>.phat-lai.json` cũng dùng `tap_chap_nhan`/`root_khai_truoc` với cùng dự phòng T-061. Đây là **hiển thị**, không phải chấm điểm: chấm vẫn bằng script trên file đã băm.

Chỉ mục sinh trước bản sửa này (định dạng cũ) phải **sinh lại** bằng script mới; script không tự sửa file đã sinh.

## 3. Ràng buộc

- Mã ca chỉ gồm chữ thường, số, gạch ngang (mã mờ của bộ điều phối). Mã đi vào URL và biến dashboard.
- Quyền đọc: Grafana chạy bằng user 472 trong container. File phải đọc được bởi mọi user (`chmod a+r`), thư mục `a+rx`.
- Trang chính chỉ đọc `rca-ket-qua/<mã>.json` và `rca-ket-qua/chi-muc/…`; **không** đọc `phat-lai/`. Bộ sinh dashboard chốt điều này (từ khóa `phat_lai.`, `.phat-lai.json`, `danh-sach-phat-lai`, `thanh_phan_tiem` không được có trong JSON trang chính).
- Thư mục `public/rca` của Grafana **không cần đăng nhập**: ai vào được cổng `10.0.0.215:3000` (trong VCN) đều tải được file, kể cả `phat-lai/`. Chỉ đẩy `phat-lai/` sau khi đã băm cả đợt (T-061 §5).
- Thư mục `rca-ket-qua/mau/` là bản sao mẫu T-061 do phiên giao diện chép (có `mau/phat-lai/`); không ghi đè.
- Hiện thư mục chính `rca-ket-qua/` còn hai mẫu T-061 và chỉ mục của chúng (T-061 đặt ngày 11/11). Khi phiên điều phối ghi chỉ mục T-062 vào `rca-ket-qua/chi-muc/danh-sach-su-co.json`, hai mẫu cũ không còn trong danh sách (file vẫn nằm đó, không ảnh hưởng). Muốn xem lại mẫu: chọn "Mẫu T-061" ở ô *Nguồn kết quả*.

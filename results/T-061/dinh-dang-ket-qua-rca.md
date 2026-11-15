# Định dạng kết quả RCA cho giao diện — bản 0.2 (T-061, G1)

> Bản 0.2 (gói C, Minh duyệt 11/11/2026) thay 0.1: thêm bản ghi `NO_EVIDENCE`/`ERROR`/`UNSUPPORTED`, mốc lấy từ `request.json` của bộ điều phối, ràng buộc mã ca, phát lại kiểm đủ đợt, kết quả thử Infinity (§7). Chỉ hỗ trợ chế độ a.

Tài liệu này mô tả một JSON chung cho giao diện phương án A (Grafana, panel Node graph), phương án B (trang riêng) và dịch vụ RCA (G3). Bộ chuyển đổi đọc đầu ra M1 (`method-output-*.json`) và ghi JSON này. Task **không đánh giá M1**; định dạng giữ nguyên dự đoán của M1, kể cả khi dự đoán khác đáp án.

File đi kèm: [`schema.json`](schema.json) (JSON Schema 2020-12), [`chuyen-doi.py`](chuyen-doi.py), [`phat-lai.py`](phat-lai.py), [`khung-grafana.py`](khung-grafana.py), [`mau/`](mau/), [`kiem-chuyen-doi.md`](kiem-chuyen-doi.md), [`kiem-hien-thi.md`](kiem-hien-thi.md). Chạy lại toàn bộ: `bash chay-tat-ca.sh && py -3 kiem.py` trong `results/T-061/`.

## 1. Định dạng phải đáp ứng gì

| Loại | Nội dung | Nguồn |
|---|---|---|
| Yêu cầu đề tài | Sản phẩm có giao diện minh họa kết quả phân tích | DT18 |
| Yêu cầu đề tài | Demo: báo sự cố → đồ thị con bất thường → danh sách nguyên nhân → giải thích | MRP P10, Q-28 |
| Quyết định đã duyệt | Phương án A (Grafana, Node graph) trước; B nếu A không ổn; G2 do Minh làm | M6, chat 11/11; `KE-HOACH-GIAI-DOAN-2.md` §7 |
| Quyết định đã duyệt | G1 gồm: sự cố, nút, cạnh, vai trò (nghi là nguồn, bị kéo theo, bình thường, thiếu dữ liệu), xếp hạng, vùng nghi ngờ, bằng chứng, liên kết sang trace/log/metric | `KE-HOACH-GIAI-DOAN-2.md` §7, dòng G1 |
| Quyết định đã duyệt | Nhãn chỉ ghép sau khi đầu ra cả đợt đã băm, bằng quyền riêng | `PLAN-TRIEN-KHAI.md` §5.2–5.3; SPEC T-061 câu 3 |
| Giới hạn của panel | Khung cạnh bắt buộc `id`, `source`, `target`; khung nút `id`; trường tùy chọn `title`, `subtitle`, `mainstat`, `secondarystat`, `color`, `highlighted`, `nodeRadius`, `arc__*`, `detail__*`, `fixedX/Y`; cạnh: `thickness`, `color`, `strokeDasharray`; `highlighted` của cạnh bỏ từ 10.5 | Tài liệu Grafana Node graph (bản latest, đọc 11/11/2026); kiểm thật trên 13.3.0 ở [`kiem-hien-thi.md`](kiem-hien-thi.md) |
| Tham khảo, không bắt buộc | Kích thước nút theo điểm, vòng `arc__*` theo tỷ lệ request, trace mẫu, đường lan truyền, hai mức xem service/thao tác, bố cục 8 panel | `DE-XUAT-HUONG-GRAFANA-RCA.md` §6.4, §7.2–7.6 (Q-188) |

Bản 0.2 làm đủ các mục "quyết định đã duyệt". Các mục tham khảo chưa làm được hoặc chưa nên làm ghi ở §6.

## 2. Cấu trúc và nguồn từng trường

Ký hiệu cột "Nguồn": **TT** = lấy thẳng từ M1, giữ nguyên giá trị (con trỏ JSON của `method-output-1.json`); **DX** = dẫn xuất theo quy tắc ở §3; **AD** = từ adapter của chính lượt chạy (`results/T-058/dem-2026-11-10/src/m1/adapter_flashticket.py`, kiểm hash); **BCD** = do bộ chuyển đổi hoặc bộ điều phối cấp; **PL** = chỉ có ở bản phát lại.

### 2.1. `su_co` — bản ghi sự cố

| Trường | Ý nghĩa | Nguồn |
|---|---|---|
| `ma` | Mã mờ của ca, do bộ điều phối cấp. Không mang nghĩa nhãn. Phải trùng tên thư mục chứa file M1 và `request.json` | BCD (tham số `--ma-ca`), kiểm ràng buộc |
| `che_do` | Chỉ `a` (biết mốc) ở bản 0.2; chế độ khác bị từ chối | TT `/mode` (nhánh lỗi của M1 điền cứng `a`) |
| `moc.t_ns`, `moc.t_utc` | Mốc chia nền / sự cố | `OK`/`NO_EVIDENCE`: TT `/window/A/0`, kiểm bằng `t` của `rca-ban-dau/cases/<mã>/request.json` (lệch thì dừng). `ERROR`/`UNSUPPORTED`: lấy từ `request.json` vì M1 trả cửa sổ rỗng |
| `moc.nguon`, `moc.mo_ta` | "Mốc tham chiếu do bộ điều phối cấp (chế độ a). RCA và Grafana không tự phát hiện mốc này." — cùng một câu cho **mọi** ca chế độ `a`, nên câu này không lộ ca nào có lỗi | DX D7 |
| `cua_so_nen`, `cua_so_su_co` | `[tu, den)` theo ns, ms, UTC; `null` khi `ERROR`/`UNSUPPORTED` | TT `/window/N`, `/window/A`; ms, UTC là DX D1 |
| `ket_luan` | `CAUSE_FOUND`, `NO_INTRINSIC_ANOMALY`, `INSUFFICIENT_EVIDENCE`; `null` khi `ERROR`/`UNSUPPORTED` | TT `/verdict` |
| `ket_luan_hien_thi` | Câu tiếng Việt cố định theo `ket_luan`; khi lỗi: "M1 không trả kết quả (<trạng thái>)" | DX (bảng tra trong code) |
| `trang_thai`, `loi` | `OK`/`NO_EVIDENCE`/`ERROR`/`UNSUPPORTED`, thông điệp lỗi | TT `/status`, `/error` |

Bản ghi `ERROR`/`UNSUPPORTED` (D10) vẫn là một sự cố trong danh sách: có mã, mốc, trạng thái, thông báo lỗi; không nút, không cạnh, không hạng, không vùng; `do_phu` rỗng. `NO_EVIDENCE` là nhánh riêng: M1 có cửa sổ và verdict nhưng không có khối xếp hạng nào; nút vẫn hiện theo lớp M1 (thường là thiếu dữ liệu), không có hạng.

### 2.2. `nguon` — truy vết

`file_m1`, `sha256_m1`, `bytes_m1` (kiểm khớp `artifacts-sha256.json` trước khi chuyển, lệch thì dừng); `request`, `sha256_request` (bản ghi của bộ điều phối cho đúng ca, cùng manifest); `adapter`, `sha256_adapter` (cùng manifest; adapter được thực thi từ đúng chuỗi byte đã kiểm, không ghi bytecode); `manifest`; `bo_chuyen_doi`, `sha256_bo_chuyen_doi`; `method`, `method_version`, `config_id`, `variant`, `why_ids`, `che_do_m1` lấy TT từ `/method`, `/method_version`, `/config_id`, `/variant`, `/why_ids`, `/extra/che_do`.

### 2.3. `do_phu`

| Trường | Nguồn |
|---|---|
| `so_quan_sat`, `so_tra_hang` | TT `/sets/observed`, `/sets/returned` |
| `do_phu_cham` | TT `/do_phu_cham` |
| `thieu_kenh_hop_le` | TT `/diagnostics/NO_VALID_CHANNEL` |
| `so_canh_quan_sat`, `so_canh_tinh` | TT `/diagnostics/so_canh_quan_sat`, `/diagnostics/so_canh_tinh` |
| `hang_doi_giua_the_gioi` | TT `/RANK_CHANGED` (thứ tự đổi giữa ba thế giới P, S_lo, S_hi) |
| `don_vi_phu_thuoc_quan_sat` | TT `/OBS_DEPENDENT` |
| `thuc_the_khong_co_canh` | DX: thực thể của nút không là đầu cạnh nào |
| `ghi_chu` | Cố định: inventory đầy đủ (32 thực thể) không có trong đầu ra M1; chỉ hiện thực thể M1 quan sát. **Thiếu nguồn** cho các thực thể không quan sát |

### 2.4. `nut[]` — một nút mỗi thực thể

Tập nút = `/sets/observed_entities` ∪ khóa `/classes` ∪ hai đầu mọi cạnh `/extra/canh`.

| Trường | Ý nghĩa | Nguồn |
|---|---|---|
| `id`, `ten` | Tên thực thể theo M1 | TT |
| `lop_m1` | `tu_sinh` (tầng 1), `ke_thua` (tầng 2), `binh_thuong` (tầng 3), `thieu_du_lieu` (không có kênh OK) | TT `/classes/<id>` |
| `vai_tro` | `nghi_nguon`, `bi_keo_theo`, `binh_thuong`, `thieu_du_lieu` | DX D2 (đổi tên 1–1 theo lớp) |
| `tang_m1` | 1, 2, 3; `null` khi thiếu dữ liệu | TT `/extra/tang_P/<id>` |
| `hang`, `nhom_dong_hang` | Hạng gọn = `tie_group` + 1; `null` khi M1 không trả hạng | TT `/entity_ranking[]/tie_group`; DX D3 |
| `so_dong_hang` | Số thực thể cùng nhóm | DX D3 |
| `khoa_m1` | Khóa xếp hạng nguyên văn: (3 − tầng, max s, m của T4c, số kênh, Σs) | TT `/entity_ranking[]/key` |
| `noi_bat` | `true` chỉ khi nhóm 0 **và** lớp `tu_sinh` | DX D4 |
| `goc_vung`, `trong_vung_cach_1`, `trong_vung_cach_2` | Thuộc gốc / vùng cách 1 / vùng cách 2 | DX D5 từ `/region` |
| `co_canh` | Có ít nhất một cạnh | DX |
| `bang_chung` | Danh sách `id` của mục bằng chứng thuộc thực thể | DX D6 |
| `hien_thi.mau`, `nhan_trong`, `nhan_phu` | Màu và chữ trên nút | DX D8 |

### 2.5. `canh[]`

| Trường | Ý nghĩa | Nguồn |
|---|---|---|
| `nguon`, `dich` | Bên gọi → bên được gọi (chủ span cha → chủ span con, `src/m1/span.py::canh_goi`) | TT `/extra/canh[i]/0`, `/1`, giữ thứ tự |
| `id` | `"<nguon>-><dich>"` | DX |
| `chieu` | Hằng `ben_goi->ben_duoc_goi` | DX |
| `nguon_goc` | `quan_sat` khi `/diagnostics/so_canh_tinh` = 0; ngược lại `quan_sat_hoac_tinh` vì M1 gộp hai tập, không tách được từng cạnh | DX |
| `bang_chung` | Mục bằng chứng có đơn vị `canh|<nguon>|<dich>` | DX D6 |
| `hien_thi.mau`, `nhan` | Đỏ nếu có bằng chứng trên cạnh, xám nếu không | DX D8 |

### 2.6. `xep_hang[]`, `vung`, `bang_chung[]`, `giai_thich_ke_thua[]`, `giai_thich`

- `xep_hang[]`: mỗi khối của `/blocks` theo đúng thứ tự: `hang`, `nhom_dong_hang`, `thuc_the` (thứ tự trong khối giữ như M1), `so_thuc_the`, `tang` = 3 − `key[0]`, `khoa_m1` (TT `/blocks[i]/key`).
- `vung`: `T_m1` = TT `/region/T` nguyên văn. `goc`, `hop_cach_1`, `hop_cach_2`, `cach_1`, `cach_2` = TT `/region/...` khi `ap_dung`; rỗng kèm `ly_do` khi không (D5).
- `bang_chung[]`: mỗi kênh có cờ ở thế giới P (`/extra/kenh_co[]`): `id` = `ma`, `don_vi`, `thuc_the`, `kenh` (= `ten`), `huong`, `lop`, `s`, `F_I`, `khoi_phat_ns` — đều TT. `khoi_phat_utc` DX D1. `lien_ket`, `ly_do_khong_lien_ket` DX D9. Tập `don_vi` bằng đúng `/evidence_refs`.
- `giai_thich_ke_thua[]`: TT `/inherited_by[]` (thực thể, mã kênh, đường, kênh giải thích, quy tắc E5, trạng thái). Đây là suy luận của M1 theo quy tắc E5, không phải quan hệ nhân quả đã quan sát.
- `giai_thich`: `null` tới G4 (LLM).

### 2.7. `phat_lai` (chỉ bản phát lại)

`canh_bao`, `nguon_dap_an` + `sha256_dap_an` (kế hoạch v2 và sổ tiêm lỗi, kiểm theo manifest T-058), `sha256_ket_qua_truoc_ghep` (phải có trong `mau/manifest-mau.json`), `thanh_phan_tiem`, `ho_loi`, `moc_xac_nhan_utc`, `nhan_xet`. Xem §5.

## 3. Quy tắc dẫn xuất

- **D1 — đơn vị thời gian.** M1 ghi ns. Grafana dùng ms: `ms = ns // 10^6`. Ở hai mẫu mọi mốc chia hết cho 10^6 (đã kiểm), nên không mất gì. UTC in đủ 9 chữ số phần lẻ.
- **D2 — vai trò.** Đổi tên 1–1 từ lớp M1: `tu_sinh` → nghi là nguồn; `ke_thua` → bị kéo theo; `binh_thuong` → bình thường (có quan sát, không có kênh có cờ); `thieu_du_lieu` → thiếu dữ liệu. Không suy thêm. Hệ quả cần biết: mọi thực thể tầng 1 đều là "nghi là nguồn", không chỉ hạng 1 (ca pause có hai: api-gateway hạng 1, ticket-service hạng 2).
- **D3 — hạng và đồng hạng.** Hạng gọn theo khối: khối thứ i có hạng i+1; mọi thực thể trong khối cùng hạng. Không đổi sang hạng cạnh tranh, không tách hòa. Thực thể không có trong `/entity_ranking` (lớp `thieu_du_lieu`) có `hang = null`.
- **D4 — nổi bật.** `noi_bat` khi thuộc nhóm 0 **và** lớp `tu_sinh`. Lý do: `/region/T` và nhóm đứng đầu luôn tồn tại kể cả khi không thực thể nào bất thường. Ca `c12e47ab` có cả 17 thực thể đồng hạng ở nhóm 0, tầng 3; nếu dùng "đứng đầu" làm nổi bật, người xem sẽ thấy 17 nút nghi nguồn ở một ca M1 kết luận không có bất thường.
- **D5 — vùng nghi ngờ.** Chỉ áp dụng khi `ket_luan = CAUSE_FOUND`. M1 tính `/region` cho nhóm đứng đầu bất kể tầng; ở ca bình thường `/region/T` gồm 17 thực thể nhưng mọi vùng rỗng. Giữ `T_m1` nguyên văn để truy vết; không hiện như gốc vùng. Vùng cách 1 (lên/xuống có giải thích) và cách 2 (thành phần liên thông vô hướng) đều giữ; định dạng không chọn một cách làm "vùng chính" vì M1 (E7) chỉ mô tả, không xếp hạng, và chưa có quyết định chọn cách.
- **D6 — gắn bằng chứng.** Mục bằng chứng thuộc nút theo `thuc_the` của kênh; thuộc cạnh khi `don_vi` có dạng `canh|a|b`. Hai mẫu không có bằng chứng cạnh.
- **D7 — câu mốc.** Theo chế độ, không theo ca. Câu "không có lỗi được tiêm" chỉ xuất hiện ở bản phát lại.
- **D8 — hiển thị.** Màu chỉ phụ thuộc `vai_tro`: nghi nguồn `#E02F44`, bị kéo theo `#FF9830`, bình thường `#8E8E8E`, thiếu dữ liệu `#CA95E5`. Chữ trong nút: `#hạng` cho nghi nguồn/bị kéo theo (thêm `=n` khi n thực thể đồng hạng); `không cờ` cho bình thường (không hiện hạng, vì hạng của khối tầng 3 không phải là mức nghi ngờ); `?` cho thiếu dữ liệu. Chữ phụ: tên vai trò ngắn (vừa khoảng 12 ký tự trong nút, đã thử ở Grafana). Không dùng `nodeRadius` theo điểm. Lý do (sửa theo phản biện): với cấu hình đang dùng (`nhanh_z = true`), `s` của **đơn vị phân vị** là `max(A − trung vị N) / IQR(N)` — số không đơn vị; khi IQR nền gần 0 thì chia cho 1 (`src/m1/e4.py:279`), nên `s` mang đơn vị gốc. `s` của các loại kênh khác có thể tính theo cách khác. Với E1 = U, điểm `op|…` chấm thời gian độc quyền của span. IQR và hệ số chia không được lưu trong đầu ra M1, nên giao diện không phân biệt được hai nhánh. `s` vì vậy không phải thang mức nghiêm trọng chung; chỉ hiện trong chi tiết.
- **D10 — bản ghi lỗi.** `ERROR`/`UNSUPPORTED`: giữ trạng thái và thông báo lỗi của M1; mốc từ `request.json`; mọi phần chẩn đoán rỗng. Panel bản ghi sự cố in trạng thái, lỗi và verdict "—". Hình dạng bản ghi kiểm bằng chính hàm `src/m1/chuoi.py::_ban_ghi_loi`; chưa kiểm xuyên suốt bằng một lượt chạy M1 thật (cần ngoại lệ với "Không chạy lại M1" của SPEC; OPEN).
- **D9 — liên kết bằng chứng.** Chỉ sinh khi có truy vấn hoặc định danh từ nguồn:
  - `metric|<thực thể>_<kênh>` → `loai: metric`, `kho: prometheus`, `truy_van` = truy vấn **nguyên văn** của adapter cho kênh đó (AD `QUERIES`), `bo_loc_chuoi` = nhãn chọn chuỗi của thực thể theo ánh xạ ngược của adapter (`ALIASES`, `INFRA`; `db-size` theo `postgresql_database_name`), `cua_so_ms` = [đầu nền, cuối sự cố].
  - `op|<thực thể>|<tên span>` → `loai: trace_tim_kiem`, `kho: tempo`, TraceQL `{ resource.service.name = "<service>" && name = "<tên span>" }` trong cùng cửa sổ; service theo ánh xạ ngược `ALIASES` (trace dùng `service.name`). Đây là **tìm kiếm**, không phải trace ID. M1 không xuất trace mẫu; bộ chuyển đổi không chọn trace hay dòng log nào.
  - Loại khác (log, cạnh, đếm): `lien_ket = []` kèm `ly_do_khong_lien_ket`.
  - Cả hai loại liên kết là **dẫn xuất, chưa kiểm trên kho của `exp-obs`** (uid nguồn trên `exp-obs`: `prometheus`, `tempo`, `loki` theo `config-public/obs/provisioning/datasources/sources.yaml`).

## 4. Ánh xạ sang Node graph

Do [`khung-grafana.py`](khung-grafana.py) dựng, chỉ đọc JSON định dạng (không đọc M1).

| Khung `nodes` | Lấy từ | | Khung `edges` | Lấy từ |
|---|---|---|---|---|
| `id` | `nut.id` | | `id` | `canh.id` |
| `title` | `nut.ten` | | `source`, `target` | `canh.nguon`, `canh.dich` |
| `subtitle` | `nut.lop_m1` | | `mainstat` | `canh.hien_thi.nhan` |
| `mainstat` | `nut.hien_thi.nhan_trong` | | `color` | `canh.hien_thi.mau` |
| `secondarystat` | `nut.hien_thi.nhan_phu` | | `detail__chieu` | hằng "bên gọi → bên được gọi" |
| `color` | `nut.hien_thi.mau` | | `detail__nguon_goc` | `canh.nguon_goc` |
| `highlighted` | `nut.noi_bat` | | | |
| `detail__vai_tro`, `detail__hang`, `detail__vung`, `detail__bang_chung` | `vai_tro`; hạng + số đồng hạng; gốc/cách 1/cách 2/ngoài vùng/không áp dụng; kênh + hướng + đơn vị | | | |
| `detail__dap_an` | chỉ bản phát lại: "ĐÁP ÁN (phát lại)" ở nút được tiêm | | | |

Khung ghi theo DataFrameJSON (`schema` + `data.values`), `meta.preferredVisualisationType = nodeGraph`, `name`/`refId` = `nodes`/`edges`.

## 5. Phát lại có đáp án

Thứ tự bắt buộc: (1) chạy `chuyen-doi.py` cho cả đợt; (2) `bam-mau.py` băm mọi kết quả vào `mau/manifest-mau.json`; (3) `phat-lai.py` đọc danh sách ca của đợt từ `m1-launch-record.json` (đã ghim trước lượt chạy, chỉ dùng `/ids`, kiểm hash theo manifest lượt chạy) và **kiểm đủ đợt**: không mã trùng; tập mã = tập mẫu trong manifest mẫu; byte từng mẫu khớp; mã ca trong mẫu và thư mục nguồn M1 trùng mã; (4) chỉ khi cả đợt đạt mới mở kế hoạch có vai trò ca và sổ tiêm lỗi (kiểm hash) và **thêm** khối `phat_lai` cho mọi ca. Không đạt thì dừng với thông báo "Dừng trước khi mở nguồn đáp án".

Bảo đảm (kiểm ở [`kiem-chuyen-doi.md`](kiem-chuyen-doi.md) §4): bỏ khối `phat_lai` thì trùng bản gốc ở mọi trường; khung Grafana phát lại chỉ thêm `detail__dap_an`; đổi đáp án sang thành phần khác không đổi màu, hạng, vùng, nổi bật. `chuyen-doi.py` không import hay trỏ tới lớp phát lại và từ chối đọc file có tên chứa `ledger`, `so-tiem-loi`, `execution-plan`, `load-impact`, `light-load`, `dap-an`. Chốt tên file là lớp phòng thủ thêm, không phải bảo đảm đủ; bảo đảm chính là bộ chuyển đổi chỉ mở bốn đường dẫn được truyền vào (đầu ra M1, `request.json`, manifest, adapter).

Ở trực tuyến (G3), quyền đọc đáp án vẫn theo PLAN §5.1: sổ thuộc user `ledger`, tiến trình RCA không đọc được; lớp phát lại chạy riêng, sau khi đợt đã băm.

## 6. Phần chưa có hoặc còn mở

| Điểm | Hiện trạng | Ảnh hưởng | Bước xử lý đề xuất |
|---|---|---|---|
| Cạnh của hạ tầng | 10/17 thực thể (DB, broker, cache, keycloak, mongodb) không có cạnh nào trong `/extra/canh`. Nguyên nhân theo `rca-ban-dau.md` §1: span client DB thuộc JVM gọi, P7 không thêm DB thành nút từ thuộc tính span | Đồ thị hiện 10 nút rời; người xem không thấy service nào dùng DB nào | Không bịa cạnh. Nếu cần cho demo: cạnh tĩnh từ mô hình T-037 với `nguon_goc = tinh` và nét đứt — phải là quyết định riêng của Minh, vì đổi cạnh M1 dùng hay chỉ thêm ở lớp trình bày là hai việc khác nhau |
| Inventory | Đầu ra M1 chỉ có 17 thực thể quan sát; inventory 32 thực thể không có | Không hiện được "có trong kiến trúc nhưng không quan sát" | G3 ghi kèm inventory vào bản ghi sự cố nếu Minh muốn hiện |
| Trace mẫu, dòng log mẫu | M1 không xuất | Panel ④ "trace mẫu" của bố cục tham khảo chưa có nguồn | Chỉ có tìm kiếm TraceQL dẫn xuất (D9). Chọn trace mẫu là việc của G3, cần quy tắc khai trước |
| Đơn vị của `s` | Theo kênh, chưa ghi đơn vị trong định dạng | Không hiện `s` như số có đơn vị | Bổ sung đơn vị kênh khi có nguồn khai đơn vị |
| Vùng cách 1 hay cách 2 | Giữ cả hai | G2 phải chọn cách tô vùng | Minh quyết khi làm G2 |
| `T4c`, đối chứng C-d1/C-d2/C-d3, `don_vi_phan_vi`, `coverage`, `worlds` | Không đưa vào bản 0.2 (lý do từng phần tử ở `kiem-chuyen-doi.md` §3) | Không mất kết luận; mất chi tiết để đào sâu | Thêm khi G2 cần màn chi tiết; `don_vi_phan_vi` là nguồn của lớp thao tác (phần D, chưa duyệt) |
| Chế độ `b` | Bản 0.2 từ chối; `request.json` hiện chỉ có `t`, không có trường chế độ | Chưa hỗ trợ | Cần trường chế độ và nguồn mốc của luật cảnh báo trong bản ghi điều phối |
| Bản ghi lỗi chạy thật | Hình dạng kiểm bằng `_ban_ghi_loi`; `NO_EVIDENCE` dựng trong bộ nhớ theo `chuoi.py`; chưa có lượt M1 thật trả các trạng thái này; chưa vẽ trên Grafana (mới kiểm khung và chữ của panel) | Hợp đồng đã kiểm; hiển thị xuyên suốt OPEN | Kiểm bằng fixture T-044 nếu Minh duyệt ngoại lệ chạy M1, hoặc khi G3 gặp ca thật |
| Xếp hạng E6b | Bộ chuyển đổi từ chối (khóa E6b không mang tầng ở phần tử đầu) | Không ảnh hưởng cấu hình hiện hành (E6a) | Mở rộng nếu đổi cấu hình |

## 7. Đề xuất cấp dữ liệu cho G2

Đã chứng minh bằng hiển thị thật trên Grafana 13.3.0 cục bộ ([`kiem-hien-thi.md`](kiem-hien-thi.md)):
- **Raw frames (TestData):** Node graph hiện đúng màu, nổi bật, chữ, menu chi tiết; kiểm lại trên mẫu 0.2.
- **Infinity 4.1.6 (gói C3, 11/11/2026):** máy chủ Grafana tự tải JSON mẫu (gắn vào `public/t061/`, gọi `http://localhost:3000/public/t061/<ca>.json`); parser `backend` đọc **trực tiếp JSON định dạng 0.2**, không cần bản phẳng: chọn mảng bằng `root_selector` (`nut`, `canh`, `xep_hang`, `su_co`), trường lồng bằng selector có dấu chấm (`hien_thi.mau` → `color`). 13/13 phép kiểm phía máy chủ đạt ([`infinity-ket-qua.json`](infinity-ket-qua.json)); đổi biến `ca` từ `c12e47ab` sang `f4a8c021` trên giao diện làm bản ghi sự cố, màu và nổi bật của nút, bảng hạng cùng đổi đúng; DOM nút khớp bản Raw frames. Cạnh của hai mẫu giống hệt nhau, nên phép đổi ca không quan sát được cạnh đổi; mỗi ca chỉ kiểm được cạnh khớp đúng mẫu của nó.
- **Danh sách sự cố bằng file chỉ mục (Minh duyệt 11/11/2026):** `chi-muc.py` sinh `mau/chi-muc/danh-sach-su-co.json` chỉ từ các mẫu đã băm (kiểm byte theo manifest mẫu; không đọc bản phát lại), mỗi dòng: mã, mốc, trạng thái, kết luận, nút nghi nguồn hạng 1, số thực thể có hạng, file và hash mẫu; mới nhất trước. Panel bảng Infinity đọc file này; cột mã có liên kết `var-ca=${__value.raw}` mở đúng sự cố. Đạt phía máy chủ (2/2 phép kiểm) và trên giao diện: đang ở `f4a8c021`, bấm `c12e47ab` mở đúng sự cố đó, bản ghi, đồ thị và bảng hạng đổi theo. Khi có ca mới, chạy lại `chi-muc.py` là danh sách cập nhật.
- **PostgreSQL:** chưa thử.

**Việc chấm không làm trong Grafana.** Chấm điểm (MRR, Hit@k…) vẫn bằng script đọc đầu ra đã băm và ghép nhãn sau khi niêm phong, như T-054/T-055; Grafana chỉ để xem. Mỗi lượt chạy một ô lỗi là một sự cố, một file JSON, một dòng trong chỉ mục.

Cách cấp file trong phép thử (thư mục tĩnh của chính Grafana) chỉ dùng cho thử cục bộ; trên `exp-obs` cần một nơi đặt JSON mà máy chủ Grafana gọi tới được.

| Đường | Cách làm | Ưu | Nhược / điều kiện | Trạng thái |
|---|---|---|---|---|
| **R — Raw frames nhúng trong dashboard** | `khung-grafana.py` sinh dashboard JSON có sẵn khung | Không cài gì; đã chạy được; dùng ngay hai mẫu | Tĩnh: mỗi sự cố một lần sinh dashboard; không có danh sách sự cố động. Trên `exp-obs` cần thêm một nguồn TestData (core, không phải plugin ngoài) và nhập dashboard — đều là thay đổi trên máy, cần Minh duyệt | Đã kiểm cục bộ |
| **I — Infinity đọc JSON** | JSON định dạng này đặt ở nơi máy chủ Grafana gọi tới được (file tĩnh, sau này dịch vụ G3); truy vấn Infinity với `refId` `nodes`/`edges`/`xep_hang`/`su_co`, biến `ca` trong URL | Đọc thẳng JSON đang có, không cần bản phẳng, không cần DB; đổi ca bằng biến dashboard | Cài plugin trên `exp-obs` là thay đổi trên máy, cần Minh duyệt; bản arm64 của plugin **chưa kiểm**; nơi đặt JSON trên `exp-obs` và cấu hình host cho phép chưa có | **Đã kiểm cục bộ, đạt** (gồm danh sách sự cố bằng file chỉ mục) |
| **P — PostgreSQL** | Bộ nạp ghi bảng `su_co`, `nut`, `canh`, `bang_chung`; SQL đặt tên cột theo trường Node graph; đáp án ở bảng riêng, quyền riêng | Nguồn có sẵn trong Grafana; lọc nhiều sự cố theo thời gian/service bằng SQL; nhiều nơi ghi cùng lúc. Không dùng để chấm: chấm giữ bằng script trên file đã băm (luật cứng 4) | Cần một Postgres **riêng** cho RCA (không dùng DB của FlashTicket trên `exp-app`, vì làm nhiễu hệ đang đo); tốn bộ nhớ trên máy quan sát (ngân sách `PLAN-TRIEN-KHAI.md` §2); cần bộ nạp — **chưa kiểm** | Chưa kiểm |

**Đề xuất (để Minh quyết):**
1. **Chọn Infinity cho G2.** Lý do: đã chạy được cục bộ với chính JSON định dạng 0.2, đổi ca bằng biến dashboard, không cần bộ nạp hay DB. Mặt trái: cần cài plugin trên `exp-obs` (Minh duyệt) và kiểm bản arm64; cần nơi đặt JSON mà Grafana trên `exp-obs` gọi tới được. Phương án khác đã xét: Raw frames (không cài gì nhưng tĩnh, phải sinh lại dashboard mỗi sự cố, nối truy vấn xong lại phải làm lại khi đổi nguồn); PostgreSQL (lọc nhiều sự cố bằng SQL; nhưng thêm một Postgres riêng, bộ nạp, và một bản sao dữ liệu phải giữ khớp file đã băm; chưa thử).
2. **Điều kiện chuyển sang PostgreSQL** (Minh duyệt 11/11/2026): plugin không cài được hoặc không có bản arm64 trên `exp-obs`; hoặc danh sách sự cố bằng file chỉ mục không dùng được; hoặc G3 sinh sự cố liên tục tới mức file không còn quản lý nổi. Không chuyển chỉ vì chấm điểm: chấm giữ bằng script đọc file đã băm.
3. Minh có thể dựng **bố cục** G2 ngay trên dashboard thử `t061-infinity` (cục bộ). Nối truy vấn lên `exp-obs` sau khi Minh duyệt cài plugin và chọn nơi đặt JSON.
4. Định dạng không đổi theo đường cấp dữ liệu; đổi đường chỉ đổi bước dựng khung/truy vấn.

## 8. Cách dùng hai mẫu để bắt đầu G2

- Mẫu: [`mau/c12e47ab.json`](mau/c12e47ab.json) (ca không có bất thường tự sinh), [`mau/f4a8c021.json`](mau/f4a8c021.json) (ca có dự đoán; thực thể bị tạm dừng thiếu dữ liệu). Bản phát lại: `mau/*.phat-lai.json`.
- Khung Node graph dựng sẵn: [`grafana/frames/`](grafana/frames/); dashboard thử Raw frames: [`grafana/provisioning/dashboards/t061.json`](grafana/provisioning/dashboards/t061.json); dashboard thử Infinity có biến `ca`: [`grafana/provisioning/dashboards/t061-infinity.json`](grafana/provisioning/dashboards/t061-infinity.json) (truy vấn sinh bởi [`infinity-thu.py`](infinity-thu.py)).
- Hai ca này phủ được: đồng hạng toàn bộ, nhiều nút nghi nguồn khác hạng, nút bị kéo theo có giải thích E5, nút thiếu dữ liệu không hạng, vùng cách 1 ≠ cách 2, nút không có cạnh. Chưa phủ bằng ca thật: bằng chứng trên cạnh, cạnh tĩnh, `INSUFFICIENT_EVIDENCE`, `NO_EVIDENCE`/`ERROR`/`UNSUPPORTED` (mới kiểm hợp đồng), chế độ `b`, đồng hạng giữa các nút nghi nguồn, cạnh khác nhau giữa hai ca.

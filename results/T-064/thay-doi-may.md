# T-064 — Sổ thay đổi máy (chỉ ghi thêm)

## TD-64-01 — `exp-obs`: thư mục làm việc M1-FT (12/11/2026 21:55Z)

- **Lý do.** Chạy M1-FT trên cùng nền với P7 (WHY-81). Không sửa thư mục ghim `/opt/flash-ticket-rca` (T-058).
- **Lệnh.** `scp` gói `src/m1 src/m1_ft src/p3 results/T-064/kiem/tuong_duong_p7.py results/T-062/ca/_nguon/m1-source-pins.json` (sha256 `34c593241dc445007b3935df8e8a09d567ff2276df324150945048df8e13a699`) → `/tmp/m1ft.tgz`; `sudo mkdir -p /opt/rca-m1ft/{goc,out}`; giải nén vào `goc/`, `chown -R root:root goc`, `chmod -R a+rX goc`; `chown rca out`.
- **Dùng.** `sudo -u rca /opt/flash-ticket-rca/venv/bin/python -B goc/...` — đọc (không ghi) `/opt/flash-ticket-rca/outputs/<id>/method-input.json`; ghi trong `/opt/rca-m1ft/out/`.
- **Kiểm.** Pin 39/39 khớp; `sha256sum src/m1/*.py` trùng với `/opt/flash-ticket-rca/src/m1`.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft /tmp/m1ft.tgz` (không ảnh hưởng dịch vụ nào).

## TD-64-06b — `exp-obs`: mã nguồn lượt chọn `goc-6` (13/11/2026 08:37Z)

- **Lý do.** Chạy biến thể lượt chọn dev bản 2. Đã ghi sổ `chon_dev2_luot1`, mã nguồn `f3211295…`, sau khi sửa H7c (LOG T-064).
- **Lệnh.**
  - `tar` gói `src/m1 src/m1_ft src/p3 results/T-064/bien-the results/T-064/kiem/tuong_duong_p7.py results/T-062/ca/_nguon/m1-source-pins.json`. Hash ở `results/T-064/kiem/goi-tai-len-6b.sha256`.
  - `scp` → `/tmp/m1ft6b.tgz`.
  - `sudo mkdir /opt/rca-m1ft/goc-6`, giải nén, `chown -R root:root`, `chmod -R a+rX`.
- **Kiểm.**
  - Hash gói hai đầu trùng.
  - `sha256sum src/m1/*.py | sha256sum` của `goc-6` trùng `/opt/flash-ticket-rca/src/m1`.
  - `ft.sha_ma_nguon()` trên máy = `f3211295…`, trùng sổ.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/goc-6 /tmp/m1ft6b.tgz`.

## TD-64-07 — `exp-obs`: lô chọn dev bản 2 (13/11/2026 14:09–14:20Z)

- **Lệnh.**
  - `sudo mkdir -p /opt/rca-m1ft/bo-sung-dev2/<mã>`, chép `~/rca-dieu-phoi/ca/<mã>/prometheus-bo-sung.json` cho 13 ca, `chmod -R a+rX`. Hash trùng dòng "M1 xong" của nhật ký đợt thu.
  - `sudo mkdir` `out/chon-dev2-1`, `out/chon-dev2-1b`, `out/khong-hoi-quy-1`, `chown rca`.
  - `~/chay_bien_the_obs_dev2.sh`, `~/canh_hai_luong.sh`, `~/ca-dev2-13.txt`, `~/ca-t062-9.txt`: bản sao từ `results/T-064/kiem/`.
  - Ba luồng `setsid -f nohup`: A xuôi, B ngược (27 bản × 13 ca), T-062 (27 × 9). Script canh dừng luồng trùng.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/bo-sung-dev2 /opt/rca-m1ft/out/chon-dev2-1* /opt/rca-m1ft/out/khong-hoi-quy-1 ~/chay_bien_the_obs_dev2.sh ~/canh_hai_luong.sh ~/ca-*.txt ~/*.log`. Chỉ làm sau khi đã chép đầu ra về repo.

## TD-64-08 — `exp-obs`: mã nguồn và lô lượt chọn 2 `goc-7` (13/11/2026 19:31–19:33Z)

- **Lý do.** Chạy 10 bản `chon_dev2_luot2` (sổ ghi 19:30Z, mã nguồn `6ab3a59d…`), gồm 3 bản đối chứng mã nguồn.
- **Lệnh.**
  - `tar` gói `src/m1 src/m1_ft src/p3`, các `results/T-064/bien-the/*/cau-hinh.json`, `chay_bien_the_obs_luot2.sh`, hai file mã ca, `m1-source-pins.json`. Hash ở `results/T-064/kiem/goi-tai-len-7.sha256`.
  - `scp` → `/tmp/m1ft7.tgz`; `sudo mkdir /opt/rca-m1ft/goc-7`, giải nén, `chown -R root:root`, `chmod -R a+rX`.
  - `sudo mkdir -p /opt/rca-m1ft/out/chon-dev2-2 /opt/rca-m1ft/out/khong-hoi-quy-2`, `chown rca`.
  - `~/chay_bien_the_obs_luot2.sh`: bản sao từ `goc-7`. Hai luồng `setsid -f nohup` (19:32Z): 10 bản × 13 ca dev bản 2 → `out/chon-dev2-2` (log `~/luot2-dev2.log`); 10 bản × 9 ca T-062 → `out/khong-hoi-quy-2` (log `~/luot2-t062.log`).
- **Kiểm.** Hash gói hai đầu trùng. `sha256sum src/m1/*.py | sha256sum` của `goc-7` trùng `/opt/flash-ticket-rca/src/m1` (`fb38cc54…`). `ft.sha_ma_nguon()` trên máy = `6ab3a59d…`, trùng sổ. Trước khi phát: không có `runner3`, `chay_bien_the`, `chay_ca` nào chạy (19:25Z).
- **Lỗi thao tác.** Lệnh kiểm hash đầu chạy bằng user `ubuntu` bị từ chối đọc `/opt/flash-ticket-rca` và dừng giữa chừng sau khi đã tạo `goc-7`; chạy tiếp phần còn lại bằng `sudo -u rca`. Không có thay đổi nào bị lặp.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/goc-7 /opt/rca-m1ft/out/chon-dev2-2 /opt/rca-m1ft/out/khong-hoi-quy-2 /tmp/m1ft7.tgz ~/chay_bien_the_obs_luot2.sh ~/luot2-*.log`. Chỉ làm sau khi đã chép đầu ra về repo.
- **Bổ sung TD-64-08 (13/11 20:08Z).** Luồng T-062 in `XONG` trước 20:07Z (90/90 cặp có `summary.json`). Phát thêm luồng thứ hai cho dev bản 2 theo thứ tự bản ngược lại (`~/luot2-dev2b.log`, cùng script, cùng thư mục ra `out/chon-dev2-2`). Cặp (bản, ca) đã có `summary.json` được bỏ qua; hai luồng đụng cùng một cặp thì luồng đến sau lỗi tạo thư mục và chạy tiếp cặp khác.
  - **Lỗi thao tác.** Lệnh nền hẹn tự phát luồng này đã không phát: phép chặn trùng `ps | grep "[l]uot2-dev2b"` khớp chính dòng lệnh ssh chứa chuỗi đó (cùng loại lỗi tự khớp đã ghi ở LOG phiên 1). Mất khoảng vài phút chạy một luồng; không ảnh hưởng kết quả. Phát tay lúc 20:08Z, chặn trùng bằng kiểm file log.

## TD-64-09 — `exp-obs`: mã nguồn sửa R1 và lô lượt chọn 3 `goc-8` (13/11/2026 22:51–22:53Z)

- **Lý do.** Sửa lỗi phân loại cạnh của H1 (phản biện T-064 lượt 1, R1). Chạy lại 8 bản có H1 và 2 bản đối chứng mã nguồn (sổ `chon_dev2_luot3` ghi 22:51:31Z, mã nguồn `7b4249ff…`).
- **Lệnh.**
  - `tar` gói `src/m1 src/m1_ft src/p3`, các `results/T-064/bien-the/*/cau-hinh.json`, `chay_bien_the_obs_luot3.sh`, hai file mã ca, `m1-source-pins.json`. Hash ở `results/T-064/kiem/goi-tai-len-8.sha256`.
  - `scp` → `/tmp/m1ft8.tgz`; `sudo mkdir /opt/rca-m1ft/goc-8`, giải nén, `chown -R root:root`, `chmod -R a+rX`.
  - `sudo mkdir -p /opt/rca-m1ft/out/chon-dev2-3 /opt/rca-m1ft/out/khong-hoi-quy-3`, `chown rca`.
  - `~/chay_bien_the_obs_luot3.sh`: bản sao từ `goc-8`. Hai luồng `setsid -f nohup` (22:52Z): (1) 10 bản × 13 ca dev bản 2 → `out/chon-dev2-3`, log `~/luot3-dev2.log`; (2) 10 bản × 9 ca T-062 → `out/khong-hoi-quy-3`, log `~/luot3-t062.log`, xong thì chạy tiếp 10 bản × 13 ca dev bản 2 theo thứ tự bản ngược lại, log `~/luot3-dev2b.log` (cặp đã có `summary.json` được bỏ qua).
- **Kiểm.** Hash gói hai đầu trùng (`2aa2520a…`). `sha256sum src/m1/*.py | sha256sum` của `goc-8` trùng `/opt/flash-ticket-rca/src/m1` (`fb38cc54…`). `ft.sha_ma_nguon()` trên máy = `7b4249ff…`, trùng sổ. Trước khi phát: 0 tiến trình python của `runner3` hay `m1_ft`.
- **Lỗi thao tác.** Lần dựng đầu bị chính phép chặn trùng từ chối: `ps | grep "[c]hay_bien_the"` khớp dòng lệnh ssh chứa tên script (cùng loại lỗi tự khớp đã ghi hai lần trước). Lệnh dừng trước mọi thay đổi. Lần hai chặn bằng `ps -eo comm,args | awk '$1 ~ /^python/ && /runner3|m1_ft/'`.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/goc-8 /opt/rca-m1ft/out/chon-dev2-3 /opt/rca-m1ft/out/khong-hoi-quy-3 /tmp/m1ft8.tgz ~/chay_bien_the_obs_luot3.sh ~/luot3-*.log`. Chỉ làm sau khi đã chép đầu ra về repo.

## TD-64-10 — `exp-obs`: mã nguồn đối chứng bỏ quan hệ `goc-9` (14/11/2026 04:19–04:22Z)

- **Lý do.** Đối chứng bỏ quan hệ trên cùng bản (SPEC T-064; R2 REVIEW lượt 1): thành phần mới `DC-bo-quan-he` (`src/m1_ft/thanh_phan/dc_bo_quan_he.py`) tắt E1, E2, E5 của P7. 4 bản V048–V051 = P7, V002, V032, V041 cùng cấu hình bản cha cộng thành phần này. Sổ ghi 04:19:00Z (`vai_tro: doi_chung_bo_quan_he_luot4`, mã nguồn `38b677a2…`).
- **Lệnh.** `tar` gói `src` + 4 `cau-hinh.json` + script + hai file mã ca (`results/T-064/kiem/goi-tai-len-9.sha256`, `eafc5954…`); `scp` → `/tmp/m1ft9.tgz`; `sudo mkdir /opt/rca-m1ft/goc-9`, giải nén, `chown -R root:root`, `chmod -R a+rX`; `sudo mkdir /opt/rca-m1ft/out/dc-dev2-4 dc-t062-4`, `chown rca`; `~/chay_bien_the_obs_luot4.sh`, hai luồng `setsid -f nohup` (04:21Z): 4 × 13 ca dev bản 2 (bo-sung-dev2) và 4 × 9 ca T-062 (bo-sung), log `~/luot4-dev2.log`, `~/luot4-t062.log`.
- **Kiểm.** Hash gói hai đầu trùng; `ft.sha_ma_nguon()` trên máy = `38b677a2…` = sổ; thành phần `DC-bo-quan-he` được nạp. Trước khi phát không có tiến trình `runner3`/`m1_ft`. Máy cục bộ thiếu numpy/scipy nên chưa chạy thử cục bộ.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/goc-9 /opt/rca-m1ft/out/dc-dev2-4 /opt/rca-m1ft/out/dc-t062-4 /tmp/m1ft9.tgz ~/chay_bien_the_obs_luot4.sh ~/luot4-*.log`. Chỉ sau khi chép đầu ra về repo.
- **Hồ sơ lỗi (luật 21).** ~88 cặp, mỗi cặp ~50 s, hai luồng: ~45–60 phút. Lỗi ở 10%/50%/99%: một (bản, ca) lỗi chỉ ghi dòng lỗi, lô chạy tiếp; chạy lại bỏ qua cặp đã có `summary.json` (mất vài phút). Lỗi mã (sai tắt quan hệ) thì sửa `dc_bo_quan_he.py`, lên `goc-10`, chạy lại cả lô (~1 giờ); không ảnh hưởng đầu ra các lượt trước.

## TD-64-11 — `exp-obs`: phiên C, xuất lại gói bổ sung quanh t' và lô dời mốc `goc-10` (14/11/2026 05:17–05:21Z)

- **Lý do.** Kiểm độ nhạy mốc ±30 s (SPEC T-064 bước 6, §7; brief phiên C §2a). Sổ V052–V059 ghi 05:19:19Z (`vai_tro: do_nhay_moc`, `kiem_cai_dat_doi_moc`, `thu_gia_doi_moc`; mã nguồn `05273b2e…`).
- **Lệnh.**
  - `mkdir ~/phien-c`; `sudo mkdir /opt/rca-m1ft/out/pc-bo-sung-dt`, `chown ubuntu:rca`, `chmod 755`. `scp` bộ xuất nguyên bản `results/T-063/dong-goi/xuat_bo_sung.py` (sha256 `7984e6c0…`), `results/T-064/phien-c/doi-moc/xuat_bo_sung_doi_t.sh`, `kiem_bo_sung_doi_t.py`, `ca-dev2-13.txt` vào `~/phien-c/`. Một luồng `setsid -f nohup` (05:17Z): 13 ca dev bản 2 × d ∈ {−30, +30} → `out/pc-bo-sung-dt/d<d>/<id>/prometheus-bo-sung.json`, log `~/phien-c/xuat-bo-sung.log`. Chỉ đọc Prometheus `localhost:9090` (retention đọc 05:17Z: `30d`).
  - `tar` gói `src/m1 src/m1_ft src/p3`, 8 `bien-the/V05[2-9]-*/cau-hinh.json`, `phien-c/doi-moc/chay_doi_moc.sh`, `viec-A.txt`, `viec-B.txt`, `m1-p7-config.json` (`results/T-064/kiem/goi-tai-len-10.sha256`, `f448908a…`); `scp` → `/tmp/m1ft10.tgz`; `sudo mkdir /opt/rca-m1ft/goc-10`, giải nén, `chown -R root:root`, `chmod -R a+rX`; `sudo mkdir /opt/rca-m1ft/out/pc-doi-moc /opt/rca-m1ft/out/pc-doi-moc-dem`, `chown rca`. Hai luồng `setsid -f nohup` (05:20:47Z): `viec-A.txt`, `viec-B.txt`, hạn ngừng phát cặp mới 07:25Z; log `~/phien-c/luot-A.log`, `luot-B.log`.
- **Kiểm.** Hash gói hai đầu trùng. `sha256sum src/m1/*.py | sha256sum` của `goc-10` trùng `/opt/flash-ticket-rca/src/m1` (`fb38cc54…`). `ft.sha_ma_nguon()` trên máy = `05273b2e…` = sổ. `m1-p7-config.json` của gói trùng bản ghim (`eb7dddd7…`). Trước khi phát: 0 tiến trình `chay_ca.py`, 0 `runner3`; lô lượt 4 của điều phối đã in `XONG` ở cả hai log; `results/T-063/thu3/TRANG-THAI.json`: `dang_thu: false`, `du_kien_bat_dau_thu` 08:00Z.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/goc-10 /opt/rca-m1ft/out/pc-doi-moc /opt/rca-m1ft/out/pc-doi-moc-dem /opt/rca-m1ft/out/pc-bo-sung-dt /tmp/m1ft10.tgz ~/phien-c`. Chỉ sau khi chép đầu ra về repo.
- **Hồ sơ lỗi (luật 21).** 176 cặp, ước 1,5–2 giờ hai luồng (chưa đo nhịp dựng lại đầu vào trên ARM). Lỗi một cặp: chỉ ghi dòng lỗi, lô chạy tiếp; chạy lại bỏ qua cặp đã có `summary.json`, đầu vào dựng lại có bộ đệm kiểm hash nên chạy bù rẻ. Lỗi mã (dựng lại sai) phát hiện bằng V058 (phải trùng P7): sửa `doi_moc.py`, lên `goc-11`, chạy lại cả lô. Qua 07:25Z, có `runner3` hoặc file `~/phien-c/DUNG`: dừng phát ở ranh giới cặp; phần thiếu chạy bù sau đợt thu của phiên B.

## TD-64-12 — `exp-obs`: phiên C, mã nguồn H8 `goc-11` và lô H8 chờ phát (14/11/2026 05:41–05:43Z)

- **Lý do.** H8-adapter, H8-log (brief phiên C §2b–2d). Sổ V060–V065 ghi 05:39:46Z (`vai_tro: h8_phien_c`, mã nguồn `b0f79a4d…`). Kiểm cài đặt `thuong01` dùng V058 và V060.
- **Lệnh.** `tar` gói `src/m1 src/m1_ft src/p3`, `bien-the/V06[0-5]-*/cau-hinh.json`, `V058…/cau-hinh.json`, `phien-c/chay_h8.sh`, `cho_roi_chay_h8.sh`, `viec-h8-A.txt`, `viec-h8-B.txt` (`results/T-064/kiem/goi-tai-len-11.sha256`, `8d26aacd…`); `scp` → `/tmp/m1ft11.tgz`; `sudo mkdir /opt/rca-m1ft/goc-11`, giải nén, `chown -R root:root`, `chmod -R a+rX`; `sudo mkdir /opt/rca-m1ft/out/pc-h8`, `chown rca`. `setsid -f nohup bash cho_roi_chay_h8.sh 2026-11-14T07:25Z` (log `~/phien-c/cho-h8.log`): chờ `luot-A.log` và `luot-B.log` in `XONG`, rồi phát hai luồng `chay_h8.sh` (log `h8-A.log`, `h8-B.log`), hạn ngừng phát cặp mới 07:25Z.
- **Kiểm.** Hash gói hai đầu trùng. `src/m1` của `goc-11` trùng bản ghim (`fb38cc54…`). `ft.sha_ma_nguon()` trên máy = `b0f79a4d…` = sổ. Thành phần `H8-adapter`, `H8-log-kq`, `H8-log-chuoi` nạp được.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/goc-11 /opt/rca-m1ft/out/pc-h8 /tmp/m1ft11.tgz`; file trong `~/phien-c`. Chỉ sau khi chép đầu ra về repo.
- **Hồ sơ lỗi (luật 21).** 134 cặp, ước 45–60 phút hai luồng. Lỗi một cặp chỉ ghi dòng lỗi; chạy lại bỏ qua cặp đã có `summary.json`. Riêng `V058 kc thuong01` được **kỳ vọng lỗi** (adapter ghim ném) và không có `summary.json`. Lỗi mã ở một thành phần: chỉ chặn các bản có thành phần đó; sửa, lên `goc-12`, chạy lại các bản đó. Hạn 07:25Z hoặc `runner3`: dừng ở ranh giới cặp, chạy bù sau đợt thu của phiên B.

## TD-64-13 — `exp-obs`: phiên C, chạy 4 bản trên ca RECREATE-PAY (14/11/2026 10:50–10:53Z)

- **Lý do.** Ca thật cho H8-adapter (`results/T-064/phien-c/YEU-CAU-O.md`; phiên B thu, mã mờ `ebd5ef38`). Sổ `chay_them` ghi 10:50:19Z trước khi chạy (mã nguồn `b0f79a4d…`, `goc-11` có sẵn).
- **Lệnh.** `scp` `phien-c/chay_recreate.sh` và `bien-the/V032-H5b/cau-hinh.json` (thành `~/phien-c/cau-hinh-V032-H5b.json`) vào `~/phien-c/`; `chmod a+r` file cấu hình; **`chmod a+rx ~ ~/phien-c`** (để `rca` đọc file cấu hình; sau lệnh `~` là 755 — các lô trước đã cho `rca` đọc `~/rca-dieu-phoi/...` nên nhiều khả năng quyền trước đó đã cho phép đi qua; **chưa kiểm** giá trị trước); `sudo mkdir /opt/rca-m1ft/out/pc-recreate`, `chown rca`; `setsid -f nohup bash chay_recreate.sh` (log `~/phien-c/recreate.log`).
- **Kiểm.** Trước khi phát: 0 `chay_ca.py`, 0 `runner3`; `results/T-063/thu3/TRANG-THAI.json` `dang_thu: false` (đợt xong 10:33Z). Gói bổ sung `bo-sung-dev3/ebd5ef38` sha256 `defa6d73…` khớp `BAN-GIAO-B.md` mục 8. Gói tải về `7ad1f425…` trùng hai đầu.
- **Hoàn tác.** `sudo rm -rf /opt/rca-m1ft/out/pc-recreate /tmp/pc-recreate.tgz ~/phien-c/chay_recreate.sh ~/phien-c/cau-hinh-V032-H5b.json ~/phien-c/recreate.log`. Nếu cần trả quyền home về mặc định Ubuntu: `chmod 750 ~` — **chỉ sau khi** xác nhận không lô nào của `rca` còn đọc dưới `/home/ubuntu` (các lô trước dùng `~/rca-dieu-phoi/ca/...`).

## TD-64-14 — `exp-obs`: lô 5 `goc-12` (14/11/2026 11:45–11:47Z, phiên 5 điều phối)

- Tạo `/opt/rca-m1ft/goc-12` (root, a+rX): `src/m1`, `src/m1_ft` từ laptop (gói `/tmp/goc12.tgz` sha256 `275fe219…`, trùng hai đầu), `src/p3` chép từ `goc-11` (21 file trùng hash bản laptop), `results/T-064/bien-the/*/cau-hinh.json` (81 bản), `results/T-064/kiem/luot5/`, `results/T-063/dong-goi/xuat_bo_sung.py`. `sha_ma_nguon()` = `b0f79a4d…` (= `goc-11`; `diff -r` m1, m1_ft không khác).
- Thư mục mới: `/opt/rca-m1ft/out/l5-bo-sung-dt` (ubuntu), `/opt/rca-m1ft/out/l5`, `out/l5-dem` (rca, do `chay_ca.py` tạo), `~/l5` (log, `bat-dau.txt`).
- Phát 11:47:05Z bằng `setsid nohup`: `l5_xuat_bo_sung.sh` (13 ca dev bản 2 × d ∈ {−60, −15, +15}; 6 ca thu bù 3 × d ∈ {−60, −30, −15, +15, +30}; chỉ đọc Prometheus `localhost:9090`), `l5_chay.sh viec-obs-1.txt` (146 cặp), `l5_chay.sh viec-obs-2.txt` (178 cặp).
- Hoàn tác: `touch ~/l5/DUNG` (dừng ở ranh giới cặp); xóa `goc-12`, `out/l5*`, `~/l5` khi không cần (giữ theo luật 10 tới khi Minh cho).
- 11:55Z dừng hai luồng ở ranh giới cặp (`~/l5/DUNG`, 26 cặp đã xong, giữ) để sắp lại thứ tự; một vòng chờ `pgrep` tự khớp chính nó làm treo kết nối, đã `kill` (không ảnh hưởng đầu ra). 12:00:31Z phát lại `l5_chay.sh viec-obs-A.txt` (355 dòng) và `viec-obs-B.txt` (318 dòng): thêm phần d = 0 trước dự tính chạy laptop (bỏ tuyến laptop, xem `kiem/luot5/laptop-kiem/KET-QUA.md`). Cặp đã có `summary.json` được bỏ qua.

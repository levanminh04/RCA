# Checkpoint phiên C — T-064 (dời mốc ±30 s, H8-adapter, H8-log)

Cập nhật: 14/11/2026 07:30Z. **Phiên C xong phần trong quyền; bàn giao ở `BAN-GIAO-C.md`.** Brief: `tasks/T-062-dem-chang-1-4/PHIEN-C-BRIEF.md`. Nhật ký: `NHAT-KY.md` (cùng thư mục).

## Bước

| Bước | Trạng thái | Đầu ra |
|---|---|---|
| 2a.1 `--doi-t` | xong, kiểm laptop | `src/m1_ft/doi_moc.py`, `src/m1_ft/chay_ca.py` |
| 2a.2 sổ | xong 05:19:19Z | V052–V059 trong `results/T-064/so-bien-the.jsonl` |
| 2a.2 gói bổ sung quanh t' | xong, kiểm 0 lệch | `exp-obs:/opt/rca-m1ft/out/pc-bo-sung-dt/`, `doi-moc/kiem-bo-sung-doi-t.json` |
| 2a.2 lô dời mốc | **xong** 06:34Z, 176/176, nhận về repo | `cham/dau-ra-dev2/V05[2-9]-*`, `bien-the/V05[2-9]-*/ra-doi-moc/` |
| 2a.3 chấm + cơ chế | **xong**; sổ `sau_cham` 06:39:09Z | `cham/doi-moc.json`, `doi-moc/bang-o.md`, `doi-moc/PHAN-TICH.md`, `doi-moc/co-che-tu-dong.md` |
| 2b H8-adapter | cài + test xong; sổ V060/V061 | `thanh_phan/h8_adapter.py`, `tests/test_h8.py`, `h8-adapter/dem-chuoi-trung.json`, `YEU-CAU-O.md` |
| 2c H8-log | cài + test xong; sổ V062–V065 | `thanh_phan/h8_log.py`, `bo_sung.log_phu`, `h8-log/*.json` |
| 2d lô H8 | **xong** 07:21Z, 133/133, nhận, chấm, sổ `sau_cham` 07:24:00Z (`cham/h8.json`) | `exp-obs:/opt/rca-m1ft/out/pc-h8/`, `goc-11` |
| WHY | đề xuất xong, chờ điều phối chép | `de-xuat-WHY.md` |

## Lô

- Dời mốc: `~/phien-c/luot-A.log`, `luot-B.log`; 176 cặp. Lô H8: `~/phien-c/cho-h8.log` → `h8-A.log`, `h8-B.log`; 134 cặp. Cả hai **dừng phát cặp mới lúc 07:25Z** (phiên B thu từ ~07:35Z, dự kiến xong ~10:20Z).
- Đếm: `ls /opt/rca-m1ft/out/pc-doi-moc/*/*/*/summary.json | wc -l` (đủ 176); `ls /opt/rca-m1ft/out/pc-h8/*/*/*/summary.json | wc -l` (đủ 133 — `V058 kc thuong01` được kỳ vọng lỗi, không có summary).
- Dừng khẩn: `touch ~/phien-c/DUNG`.
- **Chạy bù sau đợt thu của phiên B** (khi `results/T-063/thu3/TRANG-THAI.json` có `dang_thu: false` và đợt đã xong, không `runner3`): trên exp-obs `cd ~/phien-c && setsid -f nohup bash chay_doi_moc.sh viec-A.txt > luot-A2.log 2>&1 < /dev/null` (+ `viec-B.txt` → `luot-B2.log`); sau đó `chay_h8.sh viec-h8-A.txt` / `viec-h8-B.txt` → `h8-A2.log`, `h8-B2.log`. Cặp đã có summary tự bỏ qua.

## Bước tiếp

1. (xong) Lô dời mốc xong: `bash results/T-064/phien-c/nhan_phien_c.sh pc-doi-moc ra-doi-moc`; spec chấm `results/T-064/phien-c/cham/spec-doi-moc.json`; `<py ghim> -B results/T-064/phien-c/cham_phien_c.py <spec> results/T-064/phien-c/cham/doi-moc.json`; `co_che_ca_doi.py`. Kiểm: 176 summary, `trung_sha` mọi cặp, V058 `trung_method_input_goc` 22/22 và đầu ra trùng SHA P7.
2. (xong) Lô H8 xong: `nhan_phien_c.sh pc-h8 ra-h8`, chấm như trên với spec-h8; kiểm V060/V061 = bản cha ngoài `extra.m1_ft`; thuong01.
3. (xong) Ghi sổ `sau_cham` (dòng mới, chỉ thêm), `BAN-GIAO-C.md`, hoàn thiện `de-xuat-WHY.md`.

**Bắt buộc khi lô H8 dừng:** đặt `results/T-064/phien-c/TRANG-THAI.json` `lo_exp_obs: "xong"` — phiên B chờ trường này để phát đợt thu.

**Còn lại (chờ dữ liệu/quyết định):** ô RECREATE-PAY (phiên B); các câu ở `BAN-GIAO-C.md` §8. `lo_exp_obs: xong` đã đặt 07:22Z.

**10:57Z:** ca RECREATE-PAY (`ebd5ef38`) đã chạy (TD-64-13): P7/V032 ERROR, V060/V061 payment hạng 1. Chờ Minh nhận Sửa sau 2. `lo_exp_obs: xong`.

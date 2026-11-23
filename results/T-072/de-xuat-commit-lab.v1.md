# T-072 — Đề xuất commit repo lab (luật W4, bộ nhận nhẹ). CHƯA commit

Soạn 21/11/2026 ~03:1xZ, sau khi tính `nguong.json`. Điều phối gom cùng diff compose của T-073, trình Minh (luật cứng 11, I5).

- Worktree `D:/Project/rca-lab-wt/T-072`, nhánh `t072-luat`, HEAD `407b4f5`. Cây chỉ có 6 file mới chưa track; không sửa file nào có sẵn.
- Toàn bộ thay đổi nằm trong `observability/`: diff đầy đủ ở `results/T-072/de-xuat-commit-lab.diff` (991 dòng, `git diff --no-index /dev/null <file>` từng file); sha256 và blob git ở `results/T-072/de-xuat-commit-lab.tsv`. Mọi file là LF (khớp blob khi commit).

| File (repo lab) | Dòng | sha256 (16 ký tự đầu) | Nội dung | Grafana nạp? |
|---|---|---|---|---|
| `observability/grafana/provisioning/alerting/t072-luat.yaml` | 619 | `132eafc0674da5fa` | 11 luật nhóm `t072-w4` (nhịp 10 s), contact point `t072-bo-nhan-nhe` → `http://t072-bo-nhan:9172/t072`; ngưỡng từ `nguong.json` | **có** |
| `observability/grafana/provisioning/alerting/README.md` | 14 | `0faf8b36c13e09aa` | mô tả các file, nguồn sinh, khi nào nạp | không |
| `observability/grafana/provisioning/alerting/t072-thu-e3.yaml.mau` | 231 | `998850096d0b6f91` | 4 luật thử E3 (bản sao p95, ngưỡng 0,005 s) | không (đuôi `.mau`) |
| `observability/grafana/provisioning/alerting/t072-thu-e3-go.yaml.mau` | 11 | `f8b9523b05793684` | `deleteRules` 4 luật thử | không |
| `observability/grafana/provisioning/alerting/t072-hoan-tac-n.yaml.mau` | 38 | `e7c3240e5abcded9` | `deleteRules` 15 uid + `deleteContactPoints` `t072-webhook` | không |
| `observability/t072-bo-nhan/bo_nhan.py` | 42 | `9955589d5df9fab2` | bộ nhận webhook nhẹ (thư viện chuẩn) | — |

Thông điệp commit đề xuất:

```
T-072 W4b: luật cảnh báo Grafana (11 luật, ngưỡng từ E2), bộ nhận webhook nhẹ

observability/grafana/provisioning/alerting/t072-luat.yaml sinh bởi results/T-072/sinh_luat_grafana.py
(repo RCA) từ bieu-thuc.json T072-bieu-thuc-1 và nguong.json (T072-chon-nguong-2 trên E2).
Luật thử E3, gỡ luật thử, hoàn tác: dạng .yaml.mau, Grafana không nạp.
```

## Điểm điều phối cần quyết trước khi commit

1. **Gốc nhánh.** `/opt/rca-lab` exp-obs đang ở `e9a0857` (`t071-nen`, thêm `load/controller/chuoi_tai.py`; `observability/` giống hệt `407b4f5`: 22 file như nhau). Nếu commit trên `407b4f5` rồi checkout ở exp-obs thì mất `chuoi_tai.py` mà E3/E4 cần. Đề xuất: đặt commit này trên `e9a0857` (hoặc trên nhánh gộp của T-071 + T-073); 6 file mới không đụng file nào khác, không xung đột.
2. **Luật thử ở dạng `.mau`** (theo giao việc). Theo `ke-hoach-e3.md` §1.3, commit nạp N của E3 phải có `t072-thu-e3.yaml` (đổi tên). Hai cách: (a) commit này = N (đổi tên luôn): luật thử chỉ cháy khi có tải và phải gỡ bằng G trước E4; (b) giữ `.mau` ở commit này, thêm một commit đổi tên trước E3 (thêm một lần duyệt). Tôi không tự chọn.
3. **Contact point** trỏ `t072-bo-nhan`; dịch vụ này phải có trong compose (diff T-073) ở cùng commit được checkout, nếu không Grafana vẫn nạp luật nhưng gửi tin lỗi (đánh giá luật không ảnh hưởng).

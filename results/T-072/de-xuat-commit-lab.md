# T-072 — Đề xuất commit repo lab N và G (luật W4, luật thử E3, bộ nhận nhẹ). CHƯA commit

Bản 2, 21/11/2026 ~03:2xZ, sửa theo Codex CX-09 (`results/T-070/codex/CX-09-tin-cuoi.md`; bản 1: `de-xuat-commit-lab.v1.md`). Điều phối gom cùng file của T-073 trình Minh (luật cứng 11, I5). Gốc: `e9a0857` (CX-09 Q5: hai worktree gộp lên `e9a0857` không trùng đường dẫn).

- Worktree `D:/Project/rca-lab-wt/T-072` (nhánh `t072-luat`, HEAD `407b4f5`): 6 file mới chưa track, không sửa file có sẵn; đúng trạng thái của **N**. Diff đầy đủ: `de-xuat-commit-lab.diff` (993 dòng); sha256 + blob git: `de-xuat-commit-lab.tsv`. Mọi file LF.

## Commit N (nạp ở E3)

| File (repo lab) | Dòng | sha256 (16 đầu) | Grafana nạp? |
|---|---|---|---|
| `observability/grafana/provisioning/alerting/t072-luat.yaml` | 619 | `132eafc0674da5fa` | **có**: 11 luật `t072-w4` + contact point `t072-bo-nhan-nhe` → `http://t072-bo-nhan:9172/t072` |
| `observability/grafana/provisioning/alerting/t072-thu-e3.yaml` | 231 | `4275ebbc5d9d05a5` | **có**: 4 luật thử `t072-thu-p95-{booking,event,payment,ticket}`, ngưỡng 0,005 s, nhóm `t072-e3-thu` |
| `observability/grafana/provisioning/alerting/t072-thu-e3-go.yaml.mau` | 11 | `f8b9523b05793684` | không (kích hoạt ở G) |
| `observability/grafana/provisioning/alerting/t072-hoan-tac-n.yaml.mau` | 38 | `e7c3240e5abcded9` | không (kích hoạt ở H) |
| `observability/grafana/provisioning/alerting/README.md` | 16 | `6a9b7f95c01c51c0` | không |
| `observability/t072-bo-nhan/bo_nhan.py` | 42 | `9955589d5df9fab2` | — (dịch vụ `t072-bo-nhan` trong `compose.t073-webhook.yaml` của T-073, cùng commit) |

Thông điệp đề xuất (phần T-072):
```
T-072 W4b: luật cảnh báo Grafana (11 luật, ngưỡng từ E2), 4 luật thử E3, bộ nhận webhook nhẹ

t072-luat.yaml sinh bởi results/T-072/sinh_luat_grafana.py (repo RCA) từ bieu-thuc.json T072-bieu-thuc-1
và nguong.json c8f44854 (T072-chon-nguong-2 trên E2). t072-thu-e3.yaml: luật thử, gỡ ở commit G trước E4.
```

## Commit G (gỡ luật thử, con của N; checkout chỉ sau khi lượt `t071-e3-duong-01` và phép đo T-073 đã thoát)

| Thay đổi | File | Kết quả sau khi Grafana khởi động lại |
|---|---|---|
| xóa | `observability/grafana/provisioning/alerting/t072-thu-e3.yaml` | file thử không còn được nạp |
| đổi tên (nội dung giữ nguyên byte, sha256 `f8b9523b05793684`) | `t072-thu-e3-go.yaml.mau` → `t072-thu-e3-go.yaml` | `deleteRules` đúng 4 uid `t072-thu-p95-{booking,event,payment,ticket}` (kiểm: trùng 4 uid của file thử) |
| giữ | `t072-luat.yaml`, `t072-hoan-tac-n.yaml.mau`, README, `bo_nhan.py`, file T-073 | 11 luật thật và bộ nhận chạy tiếp cho E4 |

Thông điệp đề xuất: `T-072 E3: gỡ 4 luật thử (deleteRules) trước giờ hiệu lực E4`.

## Commit H (chỉ khi N nạp lỗi; con của P = `e9a0857`)

Thêm `t072-hoan-tac-n.yaml` (đổi tên từ `.mau`, sha256 `e7c3240e5abcded9`): `deleteRules` 15 uid + `deleteContactPoints` `t072-webhook`. Không chứa file nào khác của N. Thứ tự hoàn tác ở `ke-hoach-e3.md` mục 7 (gỡ bộ nhận khi còn ở N, rồi H, kiểm, rồi về P).

## Còn mở

- Grafana 13.3 xử lý `deleteRules` với uid chưa từng nạp, và thứ tự gỡ luật/contact point trong cùng file: chưa kiểm, phân xử ở S2.
- Digest image bộ nhận chỉ ghim lúc triển khai (CX-09 Q2; `results/T-073/trien-khai-bo-nhan.md` §4).

# Danh sách xóa sau đợt dọn: chờ Minh duyệt

Lập ngày 24/11/2026, sau bước 5, chỉ đọc. **Chưa xóa gì.** Mỗi mục ghi lý do có thể xóa và bằng chứng. Dữ liệu trong `archive/2026-11/` **không** nằm trong danh sách này: phần đó giữ theo luật hiện hành.

| # | Máy | Thứ sẽ xóa | Dung lượng | Vì sao xóa được | Bằng chứng | Lệnh |
|---|---|---|---|---|---|---|
| X1 | tải | 102 container k6 đã thoát (`rca-tai-*`), **giữ 4 ngoại lệ**: `rca-tai-d2-2e071903`, `rca-tai-verify-001..003` | nhỏ (log Docker) | Log Docker của từng container đã có bản trùng byte ở `container.log` cạnh đầu ra | `k6-so-log.out`: trùng 102, khác 0, ngoại lệ 4. `container.log` được tạo bằng `docker logs … > container.log 2>&1` (`tai_linux.py:286`); đã thử hash trên 1 container | `docker rm` từng tên trong danh sách trùng |
| X2 | app | 13 checkout cũ ở `/opt/flash-ticket-build/` (7 theo tên service, `t062-6b21ed5`, `t062-ac33155`, `t063-h3`, `t067-dc-640dbaf9`, `t067-dc-bb84d64f`, `keycloak`) | 2,4 GB | Là worktree git của `/opt/flashticket/src`, dựng lại được theo commit. Không container nào gắn. Image đã build không phụ thuộc thư mục này | `app-kiem-ke-xoa.out` (du, `git worktree list`). Riêng `keycloak` (776d9c9) là nguồn của image Keycloak đang chạy; dựng lại được từ `src` | `git -C /opt/flashticket/src worktree remove --force <dir>` ×13, `git worktree prune`, `rmdir /opt/flash-ticket-build` |
| X3 | app | Container đã dừng `rca-toxiproxy-cu` | nhỏ | Container toxiproxy mới chạy cùng cờ, cùng `proxies.json` | `../sau-buoc-3/app.json` (toxiproxy trùng bước 0) | `docker rm rca-toxiproxy-cu` |
| X4 | app | Volume không tên `6360e5cb…` | 4 KB | Rỗng, không container nào dùng (trước gắn `/data/configdb` của MongoDB) | `../sau-buoc-3/README.md` | `docker volume rm 6360e5cb…` |
| X5 | app | 25 image không container nào dùng: 21 image `ft-local/*` cũ (nhãn `arm64-t062-6b21ed55`, `arm64-t062-ac331553`, `arm64-t063h3-76b34d5e`, các bản `arm64-<sha8>` ngày 11/11), `rabbitmq:4.3.6-alpine`, `hello-world`, `testcontainers/ryuk` | Docker ước thu hồi 4,5 GB (lớp dùng chung) | Không phải image đang chạy, cũng không phải đích hoàn tác (bộ T-067 dùng `arm64-t067-36a3725d`) | `app-kiem-ke-xoa.out` (image đang dùng / mọi image) | `docker rmi <id>` từng image ngoài danh sách đang dùng |
| X6 | app | Build cache Docker | 7,86 GB | Chỉ để build lại nhanh hơn; build lại vẫn được, chỉ chậm hơn | `docker system df` | `docker builder prune -a -f` |
| X7 | obs | 2 folder Grafana rỗng: "T-072 W4 cảnh báo" (`cg51evuk4md4wb`), "T-072 E3 thử (gỡ trước E4)" (`ag51evv3jtxxcf`) | — | 0 luật, 0 dashboard trong cả hai; luật đã ở folder "Cảnh báo FlashTicket" | Đọc qua API ngày 24/11 | `DELETE /api/folders/<uid>` |
| X8 | app | Volume `ft-init-verify-data` (**đề xuất mới, ngoài kế hoạch**) | 95 MB | Volume thử dựng PostgreSQL mới của T-058 (`results/T-058/dem-2026-11-10/verify-fresh-postgres.sh`), tạo 10/11; không container nào dùng. Kết quả phép thử đã ghi ở T-058 | `docker volume inspect`; `git grep` | `docker volume rm ft-init-verify-data` |

**Không xóa:**
- `grafana/k6:1.4.2` trên máy tải: lượt tải sau còn dùng.
- `/opt/rca-tai`: theo Q5.
- Mọi thứ trong `archive/2026-11/`.

**Sau khi xóa sẽ kiểm:**
- `docker ps -a` và `docker volume ls` không còn các mục đã xóa.
- 14 container trên app vẫn chạy.
- `git -C /opt/flashticket/src worktree list` chỉ còn `src` và `build/36a3725d`.
- Grafana còn 5 folder.

## Đã xóa (Minh duyệt "Duyệt xóa cả 8", 24/11/2026 17:20–17:30Z máy)

| # | Kết quả | File |
|---|---|---|
| X1 | So lại log ngay trước khi xóa: 102 container trùng → xóa 102; giữ đúng 4 ngoại lệ | `xoa-x1-tai.*` |
| X2 | 13 worktree đã gỡ (`git worktree remove --force`), `prune`, `rmdir /opt/flash-ticket-build`; `worktree list` chỉ còn `src` và `build/36a3725d` | `xoa-x2-x6-x8-app.*` |
| X3, X4, X8 | Đã xóa `rca-toxiproxy-cu`, volume `6360e5cb…`, volume `ft-init-verify-data` | như trên |
| X5 | Đúng 25 image không container nào dùng; đã xóa. Còn 14 image, cả 14 đang dùng | như trên |
| X6 | Build cache 7,858 GB đã xóa | như trên |
| X7 | Kiểm lại 0 luật, 0 dashboard rồi xóa 2 folder; còn 5 folder, 11 luật, 4 dashboard | `xoa-x7-grafana.*` |

**Sau khi xóa:**
- exp-app: 14/14 container vẫn chạy, 5 volume đều đang dùng; ổ `/` từ 27 GB xuống 15 GB (32%).
- Máy tải: còn 4 container ngoại lệ.

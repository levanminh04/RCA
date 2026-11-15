# Kết nối máy tải

Lượt trước v2: `ket-noi-dau.txt` giữ kết quả ban đầu, 8081 bị từ chối. C1 không thay đổi cổng.

Lượt tiếp nhận v3, 2026-11-11T18:38:42Z từ AWS `3.24.8.49`:

```sh
curl -sS -o /dev/null --max-time 8 -w 'gateway %{http_code}\n' http://129.221.208.47:8081/api/v1/events
curl -sS -o /dev/null --max-time 8 -w 'keycloak %{http_code}\n' http://129.221.208.47:8080/realms/flash-ticket/.well-known/openid-configuration
```

Cả hai trả 200, curl exit 0. Nguồn: `kiem-lai-tai.txt`. Theo brief v3, dùng AWS làm máy tải chính; không cần chờ cổng hoặc dùng exp-obs. C1 không chạm iptables/Security List.

Kiểm cuối phiên từ AWS lúc 2026-11-11T19:06:22Z, cùng hai lệnh trên: Gateway 200, Keycloak 200, curl exit 0. Nguồn `ket-noi-cuoi-v3.txt`. Chrony vẫn đồng bộ, system time chậm 0,000001526 giây, last offset -0,000002498 giây; `NTPSynchronized=yes`. Không có container `rca-tai-` đang chạy ở kiểm cuối; container đã kết thúc được giữ nguyên.

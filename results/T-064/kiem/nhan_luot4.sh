#!/usr/bin/env bash
# Nhận đầu ra lượt 4 (đối chứng bỏ quan hệ) từ exp-obs. Chỉ đọc trên exp-obs; không ghi đè (cp -n).
set -u
cd /d/RCA-flashticket || exit 1
SSH="/c/Program Files/Git/usr/bin/ssh.exe"
O="-i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=20 -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"
H=ubuntu@213.35.116.128
V="V048-DC-P7-boQH V049-DC-V002-boQH V050-DC-V032-boQH V051-DC-V041-boQH"
T=results/T-064/kiem/nhan-luot4; mkdir -p "$T"
"$SSH" $O $H 'cd /opt/rca-m1ft/out && tar -czf - dc-dev2-4 dc-t062-4 | tee /tmp/luot4-out.tgz | sha256sum; sha256sum /tmp/luot4-out.tgz; cat ~/luot4-dev2.log' > "$T/luot4-dev2.log" 2> "$T/ssh.err"
"$SSH" $O $H 'cat ~/luot4-t062.log' > "$T/luot4-t062.log"
"/c/Program Files/Git/usr/bin/scp.exe" $O $H:/tmp/luot4-out.tgz "$T/luot4-out.tgz" || exit 2
sha256sum "$T/luot4-out.tgz" | tee "$T/luot4-out.sha256"; head -2 "$T/luot4-dev2.log"
rm -rf "$T/x"; mkdir "$T/x" && tar -xzf "$T/luot4-out.tgz" -C "$T/x" || exit 3
for B in $V; do
  mkdir -p "results/T-064/cham/dau-ra-dev2/$B" "results/T-064/bien-the/$B/ra-khong-hoi-quy-4"
  cp -rn "$T/x/dc-dev2-4/$B/." "results/T-064/cham/dau-ra-dev2/$B/"
  cp -rn "$T/x/dc-t062-4/$B/." "results/T-064/bien-the/$B/ra-khong-hoi-quy-4/"
done
rm -rf "$T/x"

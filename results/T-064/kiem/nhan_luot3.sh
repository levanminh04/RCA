#!/usr/bin/env bash
# Nhận đầu ra lô lượt chọn 3 từ exp-obs về repo, kiểm đủ và tất định, kiểm ba bản đối chứng mã nguồn, rồi chấm.
# Dùng (Git Bash, từ gốc repo): bash results/T-064/kiem/nhan_luot3.sh
# Chỉ đọc trên exp-obs. Không ghi đè: thư mục đích đã có thì giữ, tar không thay file cũ (-k).
set -u
cd /d/RCA-flashticket || exit 1
SSH="/c/Program Files/Git/usr/bin/ssh.exe"
O="-i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=20 -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"
H=ubuntu@213.35.116.128
V="V038-R1-H1c V039-R1-H1c+H8s1 V040-R1-H1c+H7c+H8s1 V041-R1-H1c+H5b+H8s1 V042-R1-H1c+H5b+H7c+H8s1 V043-R1-H1a V044-R1-H1b V045-R1-GOP-H1cr V046-KC-V028 V047-KC-V002"
T=results/T-064/kiem/nhan-luot3; mkdir -p "$T"
"$SSH" $O $H 'cd /opt/rca-m1ft/out && tar -czf - chon-dev2-3 khong-hoi-quy-3 | tee /tmp/luot3-out.tgz | sha256sum; sha256sum /tmp/luot3-out.tgz; cat ~/luot3-dev2.log' > "$T/luot3-dev2.log" 2> "$T/ssh.err"
"$SSH" $O $H 'cat ~/luot3-t062.log' > "$T/luot3-t062.log"
"/c/Program Files/Git/usr/bin/scp.exe" $O $H:/tmp/luot3-out.tgz "$T/luot3-out.tgz" || exit 2
sha256sum "$T/luot3-out.tgz" | tee "$T/luot3-out.sha256"; head -2 "$T/luot3-dev2.log"
rm -rf "$T/x"; mkdir "$T/x" && tar -xzf "$T/luot3-out.tgz" -C "$T/x" || exit 3
for B in $V; do
  mkdir -p "results/T-064/cham/dau-ra-dev2/$B" "results/T-064/bien-the/$B/ra-khong-hoi-quy-3"
  cp -rn "$T/x/chon-dev2-3/$B/." "results/T-064/cham/dau-ra-dev2/$B/"
  cp -rn "$T/x/khong-hoi-quy-3/$B/." "results/T-064/bien-the/$B/ra-khong-hoi-quy-3/"
done
rm -rf "$T/x"

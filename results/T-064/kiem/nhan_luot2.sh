#!/usr/bin/env bash
# Nhận đầu ra lô lượt chọn 2 từ exp-obs về repo, kiểm đủ và tất định, kiểm ba bản đối chứng mã nguồn, rồi chấm.
# Dùng (Git Bash, từ gốc repo): bash results/T-064/kiem/nhan_luot2.sh
# Chỉ đọc trên exp-obs. Không ghi đè: thư mục đích đã có thì giữ, tar không thay file cũ (-k).
set -u
cd /d/RCA-flashticket || exit 1
SSH="/c/Program Files/Git/usr/bin/ssh.exe"
O="-i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=20 -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"
H=ubuntu@213.35.116.128
V="V028-H1c+H8s1 V029-H1c+H5+H7c+H8s1 V030-GOP-H1cp V031-GOP-H1cr V032-H5b V033-H1c+H5b+H7c+H8s1 V034-H1c+H5b+H8s1 V035-KC-V015 V036-KC-V018 V037-KC-V019"
T=results/T-064/kiem/nhan-luot2; mkdir -p "$T"
"$SSH" $O $H 'cd /opt/rca-m1ft/out && tar -czf - chon-dev2-2 khong-hoi-quy-2 | tee /tmp/luot2-out.tgz | sha256sum; sha256sum /tmp/luot2-out.tgz; cat ~/luot2-dev2.log' > "$T/luot2-dev2.log" 2> "$T/ssh.err"
"$SSH" $O $H 'cat ~/luot2-t062.log' > "$T/luot2-t062.log"
"/c/Program Files/Git/usr/bin/scp.exe" $O $H:/tmp/luot2-out.tgz "$T/luot2-out.tgz" || exit 2
sha256sum "$T/luot2-out.tgz" | tee "$T/luot2-out.sha256"; head -2 "$T/luot2-dev2.log"
rm -rf "$T/x"; mkdir "$T/x" && tar -xzf "$T/luot2-out.tgz" -C "$T/x" || exit 3
for B in $V; do
  mkdir -p "results/T-064/cham/dau-ra-dev2/$B" "results/T-064/bien-the/$B/ra-khong-hoi-quy-2"
  cp -rn "$T/x/chon-dev2-2/$B/." "results/T-064/cham/dau-ra-dev2/$B/"
  cp -rn "$T/x/khong-hoi-quy-2/$B/." "results/T-064/bien-the/$B/ra-khong-hoi-quy-2/"
done
rm -rf "$T/x"

#!/usr/bin/env bash
# Phiên C: nhận đầu ra một lô từ exp-obs về repo, kiểm hash gói hai đầu. Chỉ đọc trên exp-obs; không ghi đè (cp -n).
# Dùng (Git Bash, gốc repo): bash results/T-064/phien-c/nhan_phien_c.sh <thư mục out trên máy: pc-doi-moc|pc-h8> <tên thư mục t062 trong bien-the/<bản>/>
# dev2 → results/T-064/cham/dau-ra-dev2/<bản>/<ca>/; t062 → results/T-064/bien-the/<bản>/<tên>/<ca>/; kc → bien-the/<bản>/ra-kc/<ca>/.
set -u
cd /d/RCA-flashticket || exit 1
SSH="/c/Program Files/Git/usr/bin/ssh.exe"; SCP="/c/Program Files/Git/usr/bin/scp.exe"
O="-i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=20 -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"
H=ubuntu@213.35.116.128; L=$1; TEN=$2
T=results/T-064/phien-c/nhan/$L; mkdir -p "$T"
"$SSH" $O $H "cd /opt/rca-m1ft/out && tar -czf /tmp/pc-$L.tgz $L && sha256sum /tmp/pc-$L.tgz" > "$T/sha-may.txt" || exit 2
"$SCP" $O $H:/tmp/pc-$L.tgz "$T/pc-$L.tgz" || exit 3
(cd "$T" && sha256sum pc-$L.tgz) > "$T/sha-laptop.txt"
[ "$(cut -d' ' -f1 "$T/sha-may.txt")" = "$(cut -d' ' -f1 "$T/sha-laptop.txt")" ] || { echo 'HASH LỆCH'; exit 4; }
rm -rf "$T/x"; mkdir "$T/x" && tar --force-local -xzf "$T/pc-$L.tgz" -C "$T/x" || exit 5
for TAP in dev2 t062 kc; do
  [ -d "$T/x/$L/$TAP" ] || continue
  for BD in "$T/x/$L/$TAP"/*/; do
    B=$(basename "$BD")
    case $TAP in dev2) D="results/T-064/cham/dau-ra-dev2/$B";; t062) D="results/T-064/bien-the/$B/$TEN";; kc) D="results/T-064/bien-the/$B/ra-kc";; esac
    mkdir -p "$D"; cp -rn "$BD." "$D/"
  done
done
find "$T/x/$L" -name summary.json | wc -l
rm -rf "$T/x"
echo NHAN-XONG $(cut -d' ' -f1 "$T/sha-laptop.txt")

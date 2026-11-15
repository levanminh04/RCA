#!/usr/bin/env bash
# Nhận đợt thu chính (thu2) từ exp-obs/exp-app về results/T-063/thu2/ sau `thu2-end`; kiểm hash. Chỉ đọc ở máy nguồn.
# Dùng (Git Bash, gốc repo): bash results/T-063/chay/nhan_thu2.sh
set -euo pipefail
KO="D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key"; KA="D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key"
KH="UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"; O=ubuntu@213.35.116.128; A=ubuntu@129.221.208.47
D=results/T-063/thu2; mkdir -p "$D"
ssh -i "$KO" -o BatchMode=yes -o "$KH" $O 'ps -eo cmd | grep -q "[p]ython3 -B runner3" && { echo "runner3 còn chạy"; exit 2; }; tail -1 ~/rca-dieu-phoi/tiem-loi/so-thu2.jsonl | grep -q thu2-end' < /dev/null
for p in tiem-loi chay ca; do scp -q -r -i "$KO" -o BatchMode=yes -o "$KH" "$O:rca-dieu-phoi/$p" "$D/"; done
mkdir -p "$D/tai-out"
for t in $(ssh -i "$KO" -o BatchMode=yes -o "$KH" $O 'ls ~/rca-dieu-phoi/tai-out | grep "^t2-"' < /dev/null); do
  scp -q -r -i "$KO" -o BatchMode=yes -o "$KH" "$O:rca-dieu-phoi/tai-out/$t" "$D/tai-out/"
  (cd "$D/tai-out/$t" && sha256sum --quiet -c outputs.sha256) || { echo "hash tải lệch: $t"; exit 3; }
done
mkdir -p "$D/audit"
for s in event-service booking-service; do
  ssh -i "$KA" -o BatchMode=yes -o "$KH" $A "sudo cat /opt/flash-ticket-app/rca-faults/$s/audit/executions.jsonl" < /dev/null > "$D/audit/${s%-service}-executions.jsonl"
done
# hash gói ca: so với dòng 'M1 xong' trong nhật ký
PYTHONIOENCODING=utf-8 py -3 - "$D" <<'EOF'
import json, hashlib, sys, pathlib
D = pathlib.Path(sys.argv[1]); bad = 0; n = 0
for l in (D / 'chay/nhat-ky-2.jsonl').read_text(encoding='utf-8').splitlines():
    d = json.loads(l)
    if d.get('msg') != 'M1 xong': continue
    n += 1; f = D / 'ca' / f"{d['id']}.tgz"
    h = hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
    b = hashlib.sha256((D / 'ca' / d['id'] / 'prometheus-bo-sung.json').read_bytes()).hexdigest()
    ok = h == d['tgz_sha256'] and b == d['bo_sung_sha256']; bad += not ok
    print(d['id'], 'OK' if ok else 'LỆCH')
L = (D / 'tiem-loi/so-thu2.jsonl').read_text(encoding='utf-8').splitlines(); prev = '0' * 64; chuoi = True
for l in L:
    chuoi &= json.loads(l)['prev_sha256'] == prev; prev = hashlib.sha256(l.encode()).hexdigest()
print('gói', n, 'lệch', bad, '| sổ', len(L), 'dòng, chuỗi hash', chuoi)
sys.exit(1 if bad or not chuoi else 0)
EOF
(cd "$D" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
echo NHAN-XONG

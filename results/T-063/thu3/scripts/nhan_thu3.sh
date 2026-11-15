#!/usr/bin/env bash
# Nhận đợt thu bù 3 từ exp-obs/exp-app về results/T-063/thu3/thu/ sau `thu3-end`; kiểm hash. Chỉ đọc ở máy nguồn.
# Theo mẫu results/T-063/chay/nhan_thu2.sh; khác: thư mục nguồn ~/rca-dieu-phoi/thu3, sổ so-thu3.jsonl, tag tải lấy từ sổ.
# Dùng (Git Bash, gốc repo): bash results/T-063/thu3/scripts/nhan_thu3.sh
set -euo pipefail
KO="D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key"; KA="D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key"
KH="UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"; O=ubuntu@213.35.116.128; A=ubuntu@129.221.208.47
SRC=${1:-rca-dieu-phoi/thu3}; D=${2:-results/T-063/thu3/thu}; mkdir -p "$D"  # tham số chỉ để nhận chạy thử
ssh -i "$KO" -o BatchMode=yes -o "$KH" $O "ps -eo cmd | grep -q '[p]ython3 -B runner4' && { echo 'runner4 còn chạy'; exit 2; }; tail -1 ~/$SRC/tiem-loi/so-thu3.jsonl | grep -q thu3-end" < /dev/null
for p in tiem-loi chay ca; do scp -q -r -i "$KO" -o BatchMode=yes -o "$KH" "$O:$SRC/$p" "$D/"; done
mkdir -p "$D/tai-out"
for t in $(PYTHONIOENCODING=utf-8 py -3 -c "import json,sys;[print(json.loads(l)['load_tag']) for l in open(sys.argv[1],encoding='utf-8') if '\"cycle-begin\"' in l]" "$D/tiem-loi/so-thu3.jsonl" | tr -d '\r'); do  # py tren Windows in CRLF
  scp -q -r -i "$KO" -o BatchMode=yes -o "$KH" "$O:rca-dieu-phoi/tai-out/$t" "$D/tai-out/"
  (cd "$D/tai-out/$t" && sha256sum --quiet -c outputs.sha256) || { echo "hash tải lệch: $t"; exit 3; }
done
mkdir -p "$D/audit"
for s in event-service booking-service; do
  ssh -i "$KA" -o BatchMode=yes -o "$KH" $A "sudo cat /opt/flash-ticket-app/rca-faults/$s/audit/executions.jsonl" < /dev/null > "$D/audit/${s%-service}-executions.jsonl"
done
PYTHONIOENCODING=utf-8 py -3 - "$D" <<'EOF'
import json, hashlib, sys, pathlib
D = pathlib.Path(sys.argv[1]); bad = 0; n = 0
for l in (D / 'chay/nhat-ky-3.jsonl').read_text(encoding='utf-8').splitlines():
    d = json.loads(l)
    if d.get('msg') != 'M1 xong': continue
    n += 1; f = D / 'ca' / f"{d['id']}.tgz"
    h = hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
    b = hashlib.sha256((D / 'ca' / d['id'] / 'prometheus-bo-sung.json').read_bytes()).hexdigest()
    ok = h == d['tgz_sha256'] and b == d['bo_sung_sha256']; bad += not ok
    print(d['id'], d.get('status'), d.get('deterministic'), 'OK' if ok else 'LỆCH')
L = (D / 'tiem-loi/so-thu3.jsonl').read_text(encoding='utf-8').splitlines(); prev = '0' * 64; chuoi = True
for l in L:
    chuoi &= json.loads(l)['prev_sha256'] == prev; prev = hashlib.sha256(l.encode()).hexdigest()
print('gói', n, 'lệch', bad, '| sổ', len(L), 'dòng, chuỗi hash', chuoi)
sys.exit(1 if bad or not chuoi else 0)
EOF
(cd "$D" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
echo NHAN-XONG

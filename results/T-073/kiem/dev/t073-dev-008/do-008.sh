#!/bin/bash
# T-073: một lần đo dưới tải trong E3 lượt (a) t071-e3-duong-01 (Minh duyệt (a); điều phối T-070 giao).
# Chờ mốc /srv/rca-lab/runs/t071-e3/DA-PHAT → đọc StartedAt → t̂ = floor(StartedAt) + 600
# → tới StartedAt + 900 chạy orchestrator mot (tự chờ tới t̂+750) → stage lại cùng t̂ sau 450 s kể từ lúc stage lần 1.
# Ghi: /srv/rca-lab/runs/t073-dev-008, /srv/rca-lab/m1/t073-dev, /srv/rca-lab/rca-results/t073-dev-001. Không tiêm, không đổi Grafana.
O=/srv/rca-lab/runs/t073-dev-008; L=/opt/rca-lab; C=$L/campaigns/online; M=/srv/rca-lab/m1/t073-dev
MOC=/srv/rca-lab/runs/t071-e3/DA-PHAT
cd $O
ghi() { echo "$(date -u +%FT%T.%NZ) $*" >> tien-do.log; }
ghi "cho moc $MOC; /opt/rca-lab $(git -C $L rev-parse --short HEAD)"
for i in $(seq 1 1080); do [ -e $MOC ] && break; sleep 10; done   # tối đa 3 giờ
[ -e $MOC ] || { ghi "HET GIO cho moc"; echo XONG >> tien-do.log; exit 1; }
cp $MOC moc-da-phat.txt; ghi "thay moc, sha256 $(sha256sum $MOC | cut -c1-64)"
S=$(python3 - "$MOC" <<'PY'
import sys, json, re, datetime as dt
raw = open(sys.argv[1], encoding='utf-8', errors='replace').read()
def ep(s):
    s = s.strip().replace('Z', '+00:00')
    m = re.match(r'^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(\.\d+)?(.*)$', s)
    return dt.datetime.fromisoformat(m[1] + (m[3] or '+00:00')).timestamp() + (float(m[2]) if m[2] else 0)
def tim(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if re.fullmatch(r'(?i)started_?at', k) and isinstance(v, str): return v
            r = tim(v)
            if r: return r
    if isinstance(x, list):
        for v in x:
            r = tim(v)
            if r: return r
try:
    v = tim(json.loads(raw))
except ValueError:
    v = None
if not v:
    m = re.search(r'(?i)started_?at["\'\s:=]+(\d{4}-\d\d-\d\dT[0-9:.]+Z?)', raw)
    v = m[1] if m else None
print(ep(v) if v else 'KHONG')
PY
)
if [ "$S" = KHONG ] || [ -z "$S" ]; then ghi "KHONG doc duoc StartedAt tu moc; dung, khong chay"; echo XONG >> tien-do.log; exit 1; fi
T=$(python3 -c "import math;print(int(math.floor($S))+600)")
echo "{\"started_at_epoch\": $S, \"t_hat\": $T}" > do-song.json; ghi "StartedAt=$S t_hat=$T"
W=$(python3 -c "import time;print(max(0,int($S+900-time.time())))"); ghi "cho $W s toi StartedAt+900"; sleep $W
export RCA_ONLINE_OUT=$O RCA_M1_ROOT=$M
ghi "phat orchestrator mot"
python3 -B $C/orchestrator.py mot --t $T --ra /srv/rca-lab/rca-results/t073-dev-001 > orchestrator.out 2>&1
ghi "orchestrator rc=$?"
ID1=$(python3 -c "import json,glob;print(json.load(open(glob.glob('$O/su-co/*.json')[0])).get('ma_ca_m1',''))")
S1=$(python3 -c "import json,glob;s=json.load(open(glob.glob('$O/su-co/*.json')[0]));print([b for b in s['buoc'] if b['ten'].startswith('stage')][-1]['bat_dau_epoch'])")
W=$(python3 -c "import time;print(max(0,int($S1+450-time.time())))"); ghi "cho $W s de stage lai (stage 1 bat dau $S1)"; sleep $W
ID2=$(python3 -c "import secrets;print(secrets.token_hex(4))")
ghi "stage lai $ID2"
sudo env RCA_M1_ROOT=$M PYTHONDONTWRITEBYTECODE=1 /srv/rca-lab/venv-m1/bin/python -B $C/stage_b.py --id $ID2 --t $T > stage-lai.out 2>&1
ghi "stage lai rc=$?"
sudo python3 - "$M" "$ID1" "$ID2" "$T" "$O/so-stage-lai.json" <<'PY' >> tien-do.log 2>&1
import hashlib, json, sys
M, a, b, t, ra = sys.argv[1:]
D = M + '/cases/'
r = {'t_hat': int(t), 'ma_1': a, 'ma_2': b, 'file': {}}
for f in ('raw-traces.jsonl', 'raw-logs.jsonl', 'prometheus.json', 'inventory.json', 'request.json'):
    x = open(D + a + '/' + f, 'rb').read(); y = open(D + b + '/' + f, 'rb').read()
    r['file'][f] = {'sha_1': hashlib.sha256(x).hexdigest(), 'sha_2': hashlib.sha256(y).hexdigest(),
                    'bytes_1': len(x), 'bytes_2': len(y), 'trung': x == y}
for k in ('1', '2'):
    m = json.load(open(D + r['ma_' + k] + '/manifest.json'))
    r['manifest_' + k] = {'created_utc': m['created_utc'], 'counts': m['counts'],
                          'chon_file': {p: {x: v[x] for x in ('so_file_mo', 'so_file_bo', 'vong_co_the_mat_dau', 'lan_chot')}
                                        for p, v in m['chon_file'].items()}}
open(ra, 'w').write(json.dumps(r, indent=1) + '\n')
print(json.dumps({f: v['trung'] for f, v in r['file'].items()}))
PY
ghi "xong"; echo XONG >> tien-do.log

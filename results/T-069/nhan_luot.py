# -*- coding: utf-8 -*-
"""T-069 — nhận một lượt thu về results/T-069/ (chỉ đọc trên máy; chép nhị phân qua stdout SSH; kiểm sha256 hai đầu).
Dùng: py -3 -I results/T-069/nhan_luot.py <lượt, ví dụ t069-thu>        (biến môi trường T069_SSH = script r.sh)
Ra:
  results/T-069/thu/<lượt>/so.jsonl                      sổ tiêm (đọc bằng user ledger; chỉ phía chấm dùng)
  results/T-069/thu/<lượt>/tiem-loi/so-thu2.jsonl, so-thu3.jsonl   bản chép trùng byte cho script xác nhận T-063
  results/T-069/thu/<lượt>/chay/{nhat-ky-3.jsonl,trang-thai-3.json}, <lượt>.out
  results/T-069/thu/<lượt>/tai-out/<tag>/{state,summary,run,cau-hinh,token-metadata}.json, outputs.sha256 (+raw.json ô FLASH)
  results/T-069/thu/<lượt>/audit/event-executions.jsonl  audit hook Event đầy đủ (exp-app)
  results/T-069/dau-ra/dev3/d0/{P7,V082-V066+H8a}/<mã>/{method-output-1.json,summary.json}
  results/T-069/thu/<lượt>/nhan.sha256                   hash từng file đã nhận = hash trên máy
Không đọc kết quả M1 khi dựng phía phương pháp; đây là phía chấm."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
L = sys.argv[1]; SCR = os.environ['T069_SSH']; BASH = os.environ.get('T069_BASH', 'bash')
R = Path('D:/RCA-flashticket/results/T-069'); G = R / 'thu' / L; DR = R / 'dau-ra/dev3/d0'
V082 = 'V082-V066+H8a'
ghi = []


def ssh(m, cmd):
    r = subprocess.run([BASH, SCR, m, cmd], capture_output=True)
    if r.returncode != 0: raise RuntimeError(f'{m}: {cmd[:80]} rc={r.returncode} {r.stderr[-300:]!r}')
    return r.stdout


def keo(m, src, dst, sudo='sudo -n'):
    """Chép một file (byte) và kiểm sha256 hai đầu."""
    b = ssh(m, f'{sudo} cat {src}')
    s_may = ssh(m, f'{sudo} sha256sum {src}').split()[0].decode()
    s = hashlib.sha256(b).hexdigest()
    if s != s_may: raise RuntimeError(f'lệch hash khi chép {m}:{src}')
    dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(b)
    ghi.append((s, f'{m}:{src}', dst.relative_to(R).as_posix()))
    return b


so = keo('obs', f'/srv/rca-lab/ledger/{L}.jsonl', G / 'so.jsonl', sudo='sudo -n -u ledger')
for f in ('so-thu2.jsonl', 'so-thu3.jsonl'):
    (G / 'tiem-loi').mkdir(parents=True, exist_ok=True); (G / 'tiem-loi' / f).write_bytes(so)
keo('obs', f'/srv/rca-lab/runs/{L}/chay/nhat-ky-3.jsonl', G / 'chay/nhat-ky-3.jsonl', sudo='')
keo('obs', f'/srv/rca-lab/runs/{L}/chay/trang-thai-3.json', G / 'chay/trang-thai-3.json', sudo='')
keo('obs', f'/srv/rca-lab/runs/{L}.out', G / f'{L}.out', sudo='')
keo('app', '/opt/flash-ticket-app/rca-faults/event-service/audit/executions.jsonl', G / 'audit/event-executions.jsonl')
dong = [json.loads(l) for l in so.decode().splitlines()]
chu_ky = {d['opaque_id']: d for d in dong if d['event'] == 'cycle-begin'}
for oid, d in chu_ky.items():
    tag = d['load_tag']; base = f'/srv/rca-lab/load-controller/tai-out/{tag}'
    ten = ['state.json', 'summary.json', 'run.json', 'cau-hinh.json', 'token-metadata.json', 'outputs.sha256']
    if d['cell'] in ('FLASH-HEALTHY', 'HTTP5-EVENT-FLASH'): ten.append('raw.json')
    for f in ten:
        try: keo('obs', f'{base}/{f}', G / 'tai-out' / tag / f, sudo='')
        except RuntimeError as e: print('THIẾU tải', tag, f, str(e)[-120:])
# đầu ra M1 theo nhật ký runner (mã đã cho đầu ra; stage lại thì mã khác mã gốc)
nk = [json.loads(l) for l in (G / 'chay/nhat-ky-3.jsonl').read_text(encoding='utf-8').splitlines()]
ma_ra = {}
for x in nk:
    if x['msg'] in ('M1 xong', 'V082 xong'): ma_ra.setdefault(x.get('goc', x['id']) if x['msg'] == 'M1 xong' else x['id'], x['id'])
for oid in chu_ky:
    ids = sorted({x['id'] for x in nk if x['msg'] in ('M1 xong', 'V082 xong', 'M1 LỖI (chỉ chặn ca này)') and (x.get('goc') == oid or x['id'] == oid)})
    for ma in ids:
        for ban, d in (('P7', f'/srv/rca-lab/m1/outputs/{ma}'), (V082, f'/srv/rca-lab/m1/v082/{ma}')):
            for f in ('method-output-1.json', 'summary.json'):
                try: keo('obs', f'{d}/{f}', DR / ban / ma / f)
                except RuntimeError: print('không có', ban, ma, f)
with open(G / 'nhan.sha256', 'wb') as f:
    f.write(''.join(f'{s}  {dst}  <- {src}\n' for s, src, dst in sorted(ghi, key=lambda x: x[2])).encode())
print(len(ghi), 'file nhận;', 'chu kỳ:', {o: d['cell'] for o, d in chu_ky.items()})

# Tiếp chay_kiem_2.py sau khi finish_load lỗi SSH tạm thời (04:09Z): nhận tải kt2-9e85b4, rồi stage/M1/đóng gói cho t = S+330.
import json, sys, time, secrets, datetime as dt
sys.path.insert(0, 'results/T-063/chay'); sys.stdout.reconfigure(encoding='utf-8')
import runner2 as r
tag = 'kt2-9e85b4'; S = dt.datetime(2026, 11, 13, 3, 57, 58, 744170, tzinfo=dt.timezone.utc).timestamp(); t = int(S + 330)
r.finish_load(tag)
oid = 'kt' + secrets.token_hex(3)
out = {'tag': tag, 'S': S, 't': t, 'oid': oid, 'buoc': []}
def b(ten, fn):
    t0 = time.time()
    try: v = fn(); out['buoc'].append({'buoc': ten, 'ok': True, 'giay': round(time.time() - t0, 1)}); return v
    except Exception as e: out['buoc'].append({'buoc': ten, 'ok': False, 'giay': round(time.time() - t0, 1), 'loi': str(e)[-600:]}); return None
b('stage', lambda: r.ssh('obs', f'sudo /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/stage-m1.py --id {oid} --t {t}', timeout=900))
s = b('run-m1', lambda: json.loads((lambda x: x[x.index('{'):])(r.ssh('obs', f'sudo -u rca /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/run-m1.py --id {oid}', timeout=1800))))
if s: out['m1'] = {k: s.get(k) for k in ('status', 'deterministic_repeat', 'output_sha256', 'run_seconds')}
b('run-m1-lan-2-cung-ma (phai loi: outputs da ton tai)', lambda: r.ssh('obs', f'sudo -u rca /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/run-m1.py --id {oid}', timeout=1800)[-200:])
out['nhan'] = b('nhan_ca', lambda: r.nhan_ca(oid, t))
open(f'results/T-063/kiem-tich-hop/ket-qua-{oid}.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
for x in out['buoc']: print(x['buoc'], 'OK' if x['ok'] else 'LOI', x['giay'], (x.get('loi') or '')[-200:])
print('M1', out.get('m1')); print('oid', oid, 'nhan', out.get('nhan'))

# T-063 REVIEW R2: kiểm tích hợp trên cấu hình cuối — chạy đúng đường M1/đóng gói của runner2 cho cửa sổ pilot L1 sau bảo trì.
import json, sys, time, secrets, datetime as dt
sys.path.insert(0, 'results/T-063/chay'); sys.stdout.reconfigure(encoding='utf-8')
import runner2 as r
t = int(dt.datetime(2026, 11, 13, 3, 9, 57, tzinfo=dt.timezone.utc).timestamp())  # giữa l1maint20261113b (03:07:27–03:12:27Z)
oid = 'kt' + secrets.token_hex(3)
r.CHAY.mkdir(parents=True, exist_ok=True)
out = {'t': t, 'oid': oid, 'buoc': []}
def b(ten, fn):
    t0 = time.time()
    try: v = fn(); out['buoc'].append({'buoc': ten, 'ok': True, 'giay': round(time.time() - t0, 1), 'kq': v}); return v
    except Exception as e: out['buoc'].append({'buoc': ten, 'ok': False, 'giay': round(time.time() - t0, 1), 'loi': str(e)[-400:]}); return None
b('stage', lambda: r.ssh('obs', f'sudo /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/stage-m1.py --id {oid} --t {t}', timeout=900)[-200:])
b('stage-lan-2-cung-ma (phai loi: thu muc da ton tai)', lambda: r.ssh('obs', f'sudo /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/stage-m1.py --id {oid} --t {t}', timeout=900)[-200:])
s = b('run-m1', lambda: json.loads((lambda x: x[x.index('{'):])(r.ssh('obs', f'sudo -u rca /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/run-m1.py --id {oid}', timeout=1800))))
if s: out['m1'] = {k: s.get(k) for k in ('status', 'deterministic_repeat', 'output_sha256', 'run_seconds')}
b('run-m1-lan-2-cung-ma (phai loi: outputs da ton tai)', lambda: r.ssh('obs', f'sudo -u rca /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/run-m1.py --id {oid}', timeout=1800)[-200:])
out['nhan'] = b('nhan_ca (safe-export + bo-sung ban 3 + scp + hash)', lambda: r.nhan_ca(oid, t))
open(f'results/T-063/kiem-tich-hop/ket-qua-{oid}.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
for x in out['buoc']: print(x['buoc'], 'OK' if x['ok'] else 'LOI', x['giay'], (x.get('loi') or '')[:160])
print('M1', out.get('m1')); print('oid', oid)

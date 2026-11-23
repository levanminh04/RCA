# -*- coding: utf-8 -*-
"""T-072 E3 bước 8–9: đối chiếu tin webhook (bộ nhận) với lịch sử trạng thái Grafana (annotation). Chỉ đọc file đã thu."""
import json, sys, datetime, pathlib
D = pathlib.Path(__file__).parent
def ep(s):
    s = s.replace('Z', '+00:00')
    if '.' in s:
        a, b = s.split('.', 1); frac, tz = b[:b.index('+') if '+' in b else len(b)], b[b.index('+'):] if '+' in b else ''
        s = a + '.' + frac[:6] + tz
    return datetime.datetime.fromisoformat(s).timestamp()
TH = ['t072-thu-p95-booking', 't072-thu-p95-event', 't072-thu-p95-payment', 't072-thu-p95-ticket']
tin = []
for l in open(D / 'b8-webhook.jsonl', encoding='utf-8'):
    d = json.loads(l)
    if d['duong_dan'] != '/t072':
        continue
    b = json.loads(d['than'])
    for a in b.get('alerts', []):
        tin.append({'uid': a['labels'].get('t072_uid'), 'status': a['status'], 'startsAt': a['startsAt'], 'endsAt': a.get('endsAt'),
                    'nhan': d['nhan_epoch'], 'fp': a.get('fingerprint'), 'values': a.get('values'), 'nhom_status': b.get('status')})
ls = json.loads((D / 'b9-lich-su.json').read_text(encoding='utf-8'))
ann = ls['annotation']
kq = {}
for u in sorted({t['uid'] for t in tin} | set(TH) | {a['uid'] for a in ann}):
    f = [t for t in tin if t['uid'] == u and t['status'] == 'firing']
    r = [t for t in tin if t['uid'] == u and t['status'] == 'resolved']
    a_al = [a for a in ann if a['uid'] == u and a['new_state'].startswith('Alerting')]
    a_no = [a for a in ann if a['uid'] == u and a['prev_state'].startswith('Alerting') and not a['new_state'].startswith('Alerting')]
    a_pe = [a for a in ann if a['uid'] == u and a['new_state'].startswith('Pending')]
    o = {'so_firing': len(f), 'so_resolved': len(r), 'chuyen_trang_thai': [(a['prev_state'], a['new_state'], a['epoch'] / 1000) for a in ann if a['uid'] == u]}
    if f:
        s0 = ep(f[0]['startsAt']); o['startsAt'] = f[0]['startsAt']; o['tre_gui_firing_s'] = round(f[0]['nhan'] - s0, 3)
        if a_al:
            o['lich_su_alerting'] = a_al[0]['epoch'] / 1000; o['delta_bat_dau_s'] = round(s0 - a_al[0]['epoch'] / 1000, 3)
        if a_pe:
            o['lich_su_pending'] = a_pe[0]['epoch'] / 1000; o['pending_toi_alerting_s'] = round((a_al[0]['epoch'] - a_pe[0]['epoch']) / 1000, 3) if a_al else None
        o['startsAt_moi_tin_firing_giong_nhau'] = len({t['startsAt'] for t in f}) == 1
    if r:
        e0 = ep(r[0]['endsAt']); o['endsAt'] = r[0]['endsAt']; o['tre_gui_resolved_s'] = round(r[0]['nhan'] - e0, 3)
        if a_no:
            o['lich_su_het_alerting'] = a_no[0]['epoch'] / 1000; o['delta_ket_thuc_s'] = round(e0 - a_no[0]['epoch'] / 1000, 3)
    kq[u] = o
dat = {u: (kq.get(u, {}).get('so_firing', 0) >= 1 and kq.get(u, {}).get('so_resolved', 0) >= 1) for u in TH}
lech = {u: (kq.get(u, {}).get('delta_bat_dau_s'), kq.get(u, {}).get('delta_ket_thuc_s')) for u in TH}
doi_chieu = all(v[0] is not None and abs(v[0]) <= 10 and v[1] is not None and abs(v[1]) <= 10 for v in lech.values())
out = {'theo_luat': kq, 'du_firing_resolved_4_luat_thu': dat, 'delta_bat_dau_ket_thuc_s': lech, 'da_doi_chieu_E3': doi_chieu,
       'luat_that_co_chuyen_trang_thai': sorted({a['uid'] for a in ann if a['uid'] and not a['uid'].startswith('t072-thu-')}),
       'so_tin_webhook_t072': len(tin)}
(D / 'b9-doi-chieu.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
sys.stdout.buffer.write(json.dumps({k: out[k] for k in ('du_firing_resolved_4_luat_thu', 'delta_bat_dau_ket_thuc_s', 'da_doi_chieu_E3', 'luat_that_co_chuyen_trang_thai', 'so_tin_webhook_t072')}, ensure_ascii=False).encode() + b'\n')

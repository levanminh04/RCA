# -*- coding: utf-8 -*-
"""T-072 — bộ xuất chuỗi tín hiệu luật (bieu-thuc.json#/xuat_cho_T071/bat_buoc). Chỉ ĐỌC Prometheus.

Trên laptop:  py -3 results/T-072/xuat_tin_hieu.py dung --s <epoch> --e <epoch> > goi.sh
              ssh ... exp-obs 'bash -s' < goi.sh > xuat.json
Lệnh `dung` nhúng danh sách biểu thức (kèm sha256 của bieu-thuc.json) vào một script bash chạy python3 trên exp-obs.
Script đó gọi query_range step 10 s theo khúc ≤ 600 s, nghỉ 0,3 s giữa khúc, ghi lỗi khúc, không nội suy.
"""
import argparse, hashlib, json, pathlib, sys

GOC = pathlib.Path(__file__).with_name('bieu-thuc.json')

REMOTE = r'''
import json, sys, time, urllib.parse, urllib.request
B = 'http://127.0.0.1:9090/api/v1/query_range?'
S, E, STEP, KHUC = __S__, __E__, 10, 600
EX = __EX__
out = {'phien_ban': 'T072-xuat-1', 'bieu_thuc_sha256': '__SHA__', 'cua_so': [S, E], 'step_s': STEP,
       'bat_dau_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'loi_khuc': [], 'chuoi': {}}
for ten, q in EX:
    gop = {}
    s = S
    while s <= E:
        e = min(E, s + KHUC - STEP)
        try:
            r = json.load(urllib.request.urlopen(B + urllib.parse.urlencode({'query': q, 'start': s, 'end': e, 'step': STEP}), timeout=60))
            if r.get('status') != 'success':
                raise RuntimeError(str(r)[:200])
            for x in r['data']['result']:
                k = json.dumps(x['metric'], sort_keys=True)
                gop.setdefault(k, {'metric': x['metric'], 'values': []})['values'] += [[int(round(float(a))), b] for a, b in x['values']]
        except Exception as ex:
            out['loi_khuc'].append({'ten': ten, 'start': s, 'end': e, 'loi': repr(ex)[:200]})
        s = e + STEP
        time.sleep(0.3)
    out['chuoi'][ten] = list(gop.values())
out['ket_thuc_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
sys.stdout.write(json.dumps(out, separators=(',', ':')) + '\n')
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lenh', choices=['dung'])
    ap.add_argument('--s', type=int, required=True)
    ap.add_argument('--e', type=int, required=True)
    a = ap.parse_args()
    raw = GOC.read_bytes()
    d = json.loads(raw.decode('utf-8'))
    ex = [(x['ten'], x['promql']) for x in d['xuat_cho_T071']['bat_buoc']]
    py = (REMOTE.replace('__S__', str(a.s)).replace('__E__', str(a.e))
          .replace('__EX__', json.dumps(ex)).replace('__SHA__', hashlib.sha256(raw).hexdigest()))
    sys.stdout.buffer.write(("#!/bin/bash\n# T-072 xuat_tin_hieu: chỉ đọc Prometheus\npython3 - <<'PYEOF'\n" + py + "PYEOF\n").encode('utf-8'))


main()

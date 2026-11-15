# -*- coding: utf-8 -*-
"""T-063 thu3 — tốc độ byte AMQP broker→Booking theo bậc tải từ do_h4.py. Dùng: py -3 -B phan_tich_do_h4.py <do.jsonl> <epoch bắt đầu tải> <giây đổi bậc> <giây hết tải>"""
import json, sys, statistics as st
f, S, B, E = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
L = [json.loads(l) for l in open(f) if '"conn"' in l]
L = [x for x in L if x.get('conn')]
bac = {'x1': [], 'x3': []}; tonmax = 0
for a, b in zip(L, L[1:]):
    t0, t1 = a['epoch'] - S, b['epoch'] - S
    r = (int(b['conn'][0]) - int(a['conn'][0])) / (b['epoch'] - a['epoch'])
    if 15 <= t0 and t1 <= B: bac['x1'].append(r)
    elif B + 15 <= t0 and t1 <= E: bac['x3'].append(r)
    tonmax = max(tonmax, sum(sum(v[:2]) for k, v in b['queues'].items() if k.endswith('.q')))
out = {k: {'n': len(v), 'tb_B_s': round(st.mean(v), 1), 'min': round(min(v), 1), 'max': round(max(v), 1)} for k, v in bac.items() if v}
out['ton_queue_booking_max'] = tonmax
print(json.dumps(out, ensure_ascii=False))

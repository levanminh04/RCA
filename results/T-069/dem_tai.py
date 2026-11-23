# -*- coding: utf-8 -*-
"""T-069 — đếm trạng thái các bước tải theo chu kỳ (chạy trên exp-obs qua stdin, in JSON ra stdout; chỉ đọc).
Dùng: python3 - <lượt> < dem_tai.py > results/T-069/thu/<lượt>/tai-create-order.json
Đọc sổ tiêm (sudo -u ledger) để lấy tag tải của từng mã ca, rồi container.log của k6 trong tai-out/<tag>/."""
import json, sys, subprocess, collections
L = sys.argv[1]
so = [json.loads(l) for l in subprocess.run(['sudo', '-n', '-u', 'ledger', 'cat', f'/srv/rca-lab/ledger/{L}.jsonl'],
                                            capture_output=True, text=True, check=True).stdout.splitlines()]
out = {}
for d in so:
    if d['event'] != 'cycle-begin': continue
    c = collections.Counter(); buoc = collections.Counter()
    try:
        for l in open(f"/srv/rca-lab/load-controller/tai-out/{d['load_tag']}/container.log"):
            i = l.find('{"type":"request"')
            if i < 0: continue
            try: o = json.loads(l[i:l.rfind('}') + 1].replace('\\"', '"'))
            except Exception: continue
            buoc[f"{o.get('step')}:{o.get('status')}"] += 1
            if o.get('step') == 'create_order': c[str(o.get('status'))] += 1
    except FileNotFoundError:
        c['khong_co_container_log'] = 1
    out[d['opaque_id']] = {'o': d['cell'], 'tag': d['load_tag'], **c, 'buoc': dict(sorted(buoc.items()))}
print(json.dumps(out, ensure_ascii=False, indent=1))

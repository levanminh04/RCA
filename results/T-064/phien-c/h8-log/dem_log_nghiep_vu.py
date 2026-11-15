# -*- coding: utf-8 -*-
"""Phiên C — H8-log bước 1: log nghiệp vụ (`outcome`, `reasonCode`) có trong gói ca không. Chỉ đọc gói ca (raw-logs.jsonl
và request.json để lấy t); không đọc nhãn, sổ tiêm, tên ô. Hai trường được khai trước ở hồ sơ chiến dịch (mục 4, hàng H8),
không chọn theo đáp án.
Dùng: py -3 dem_log_nghiep_vu.py <ra.json> <gói 1> [<gói 2> ...]   (gói = .tgz của T-063 hoặc thư mục <ca>/cases/<id>)
Đếm theo ca × service: số bản ghi; số bản ghi có thân JSON; có `outcome`; có `reasonCode`; vị trí của khóa (thân JSON,
thuộc tính bản ghi); giá trị; số dòng ở N = [t−300, t) và A = [t, t+300); 30 khóa thân JSON hay gặp nhất."""
import json, sys, tarfile, collections
from pathlib import Path

NS = 10 ** 9


def _val(v):
    for k in ('stringValue', 'intValue', 'doubleValue', 'boolValue'):
        if k in v:
            return v[k]
    return None


def doc_goi(p):
    p = Path(p)
    if p.suffix == '.tgz':
        tf = tarfile.open(p)
        m = {x.name.split('/')[-1]: x for x in tf.getmembers() if x.name.startswith('cases/')}
        t = json.load(tf.extractfile(m['request.json']))['t']
        return p.stem, t, (l.decode('utf-8') for l in tf.extractfile(m['raw-logs.jsonl']))
    t = json.loads((p / 'request.json').read_text(encoding='utf-8'))['t']
    return p.name, t, open(p / 'raw-logs.jsonl', encoding='utf-8')


kq = {}
for g in sys.argv[2:]:
    ma, t, dong = doc_goi(g)
    sv = collections.defaultdict(lambda: {'ban_ghi': 0, 'than_json': 0, 'outcome': 0, 'reasonCode': 0,
                                          'outcome_o': collections.Counter(), 'gia_tri': collections.Counter(),
                                          'N': collections.Counter(), 'A': collections.Counter(), 'khoa': collections.Counter()})
    for line in dong:
        if not line.endswith('\n'):
            continue
        d = json.loads(line)
        for rl in d.get('resourceLogs', []):
            res = {a['key']: _val(a['value']) for a in rl.get('resource', {}).get('attributes', [])}
            s = sv[res.get('service.name')]
            for grp in rl.get('scopeLogs', []):
                for r in grp.get('logRecords', []):
                    s['ban_ghi'] += 1
                    at = {a['key']: _val(a['value']) for a in r.get('attributes', [])}
                    b = r.get('body', {}); j = {}
                    if 'stringValue' in b and b['stringValue'].lstrip().startswith('{'):
                        try:
                            j = json.loads(b['stringValue']); j = j if isinstance(j, dict) else {}
                        except ValueError:
                            j = {}
                    if j:
                        s['than_json'] += 1
                        s['khoa'].update(j.keys())
                    o = j.get('outcome', at.get('outcome')); rc = j.get('reasonCode', at.get('reasonCode'))
                    if o is None and rc is None:
                        continue
                    if o is not None:
                        s['outcome'] += 1; s['outcome_o']['than' if 'outcome' in j else 'thuoc_tinh'] += 1
                    if rc is not None:
                        s['reasonCode'] += 1
                    w = int(r.get('timeUnixNano') or r.get('observedTimeUnixNano')) / NS - t
                    gt = f'{o}|{rc}'
                    s['gia_tri'][gt] += 1
                    if -300 <= w < 0: s['N'][gt] += 1
                    elif 0 <= w < 300: s['A'][gt] += 1
    kq[ma] = {k: {**{a: b for a, b in v.items() if not isinstance(b, collections.Counter)},
                  'outcome_o': dict(v['outcome_o']), 'gia_tri': dict(v['gia_tri'].most_common(40)),
                  'N': dict(v['N']), 'A': dict(v['A']), 'khoa': dict(v['khoa'].most_common(30))}
              for k, v in sorted(sv.items(), key=lambda x: str(x[0]))}
    print(ma, {k: (v['ban_ghi'], v['than_json'], v['outcome'], v['reasonCode']) for k, v in kq[ma].items()}, flush=True)
Path(sys.argv[1]).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

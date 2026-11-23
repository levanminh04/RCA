#!/usr/bin/env python3
"""T-071 — gộp raw.json của k6 theo phút UTC (chạy trên exp-obs, thư viện chuẩn). Chỉ đọc raw.json.

Dùng: python3 k6_phut.py RAW_JSON RA_JSON
Đếm mỗi phút [hh:mm:00, +60 s): journey_started (tổng value), journey_finished, journey_failed (số điểm),
dropped_iterations (tổng value), http_reqs có status 429 (tổng value), http_req_failed = 1 (số điểm),
http_reqs (tổng), số điểm bất kỳ (diem). Ghi kèm sha256 của raw.json.
"""
import collections
import hashlib
import json
import sys

raw, ra = sys.argv[1], sys.argv[2]
h = hashlib.sha256()
c = collections.defaultdict(collections.Counter)
with open(raw, 'rb') as f:
    for b in f:
        h.update(b)
        try:
            d = json.loads(b)
        except ValueError:
            c['_loi']['dong_hong'] += 1
            continue
        if d.get('type') != 'Point':
            continue
        m = d['metric']
        dd = d['data']
        p = dd['time'][:16]  # YYYY-MM-DDTHH:MM (UTC, k6 ghi Z)
        v = dd.get('value', 0)
        tg = dd.get('tags') or {}
        x = c[p]
        x['diem'] += 1
        if m == 'journey_started':
            x['journey_started'] += v
        elif m == 'journey_finished':
            x['journey_finished'] += v
        elif m == 'journey_failed':
            x['journey_failed'] += 1
        elif m == 'dropped_iterations':
            x['dropped_iterations'] += v
        elif m == 'http_reqs':
            x['http_reqs'] += v
            if tg.get('status') == '429':
                x['http_429'] += v
        elif m == 'http_req_failed' and v == 1:
            x['http_req_failed'] += 1
out = {'raw': raw, 'raw_sha256': h.hexdigest(), 'phut': {k: dict(v) for k, v in sorted(c.items())}}
json.dump(out, open(ra, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(json.dumps({'raw_sha256': out['raw_sha256'], 'so_phut': len(out['phut'])}))

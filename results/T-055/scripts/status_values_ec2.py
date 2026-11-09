"""Sau R7 BLOCKED (T-055): đếm tập giá trị statusCode gộp toàn host, không theo ca, không nhãn. Chỉ xuất giá trị mã và số span."""
import json, sys
from collections import Counter
from pathlib import Path
import pyarrow.parquet as pq
req = json.loads(sys.stdin.buffer.read())
c = Counter(); svc = Counter()
for case in req['cases'].values():
    t = pq.read_table(Path(req['data_root']) / case['files']['traces.parquet']['path'], columns=['statusCode', 'serviceName']).to_pandas()
    s = t.dropna(subset=['statusCode'])
    c.update(int(x) for x in s['statusCode'])
    svc.update((n, 'gt16' if int(x) > 16 else ('nonzero' if int(x) else 'zero')) for n, x in zip(s['serviceName'], s['statusCode']))
print(json.dumps({'values': sorted(c.items()), 'by_service_class': sorted([list(k) + [v] for k, v in svc.items()])}))

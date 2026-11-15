# -*- coding: utf-8 -*-
"""Phiên C — H8-log: bảng chéo severity (cách P7 phân loại dòng lỗi) × outcome (B16) theo service, trong [t−300, t+300).
Chỉ đọc gói ca. Dùng: py -3 cheo_severity_outcome.py <ra.json> <gói>...  (gói .tgz T-063 hoặc thư mục cases/<id>)"""
import json, sys, collections, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dem_log_nghiep_vu import doc_goi, _val  # noqa: E402
NS = 10 ** 9
kq = {}
for g in sys.argv[2:]:
    ma, t, dong = doc_goi(g)
    c = collections.defaultdict(collections.Counter)
    for line in dong:
        if not line.endswith('\n'): continue
        d = json.loads(line)
        for rl in d.get('resourceLogs', []):
            res = {a['key']: _val(a['value']) for a in rl.get('resource', {}).get('attributes', [])}
            for grp in rl.get('scopeLogs', []):
                for r in grp.get('logRecords', []):
                    w = int(r.get('timeUnixNano') or r.get('observedTimeUnixNano')) / NS - t
                    if not -300 <= w < 300: continue
                    b = r.get('body', {}); j = {}
                    s = b.get('stringValue')
                    if isinstance(s, str) and s.lstrip().startswith('{'):
                        try: j = json.loads(s); j = j if isinstance(j, dict) else {}
                        except ValueError: j = {}
                    sev = j.get('severity') or j.get('level') or r.get('severityText')
                    if not sev and isinstance(s, str):
                        m = re.search(r'\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL)\b', s); sev = m[1] if m else None
                    c[res.get('service.name')][f"{sev}|{j.get('outcome')}|{'N' if w < 0 else 'A'}"] += 1
    kq[ma] = {k: dict(sorted(v.items())) for k, v in sorted(c.items(), key=lambda x: str(x[0]))}
Path(sys.argv[1]).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for ma, v in kq.items():
    print(ma)
    for s, x in v.items(): print('  ', s, x)

"""Exact inventory on second host; host identity prevents confusing two equal paths."""
from pathlib import Path
import csv,hashlib,json,os,sys
base=Path('/home/ubuntu/rca/T-014');target=base/'external-files-ec2-2.csv';records=[]
for p in sorted(base.rglob('*')):
    if not p.is_file() or p==target:continue
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    records.append(dict(host='3.26.62.217',path=str(p),bytes=p.stat().st_size,sha256=h.hexdigest()))
with target.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['host','path','bytes','sha256']);w.writeheader();w.writerows(records)
print(json.dumps(dict(host='3.26.62.217',files=len(records),logical_bytes=sum(r['bytes'] for r in records))))

import hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
plan=json.loads((BASE/'diagram-download-plan.json').read_text(encoding='utf-8'))
assert plan['expected_bytes']<=500000
entry=dict(plan,requested_at_utc=datetime.now(timezone.utc).isoformat(),artifact='snapshots/Architecture.png')
try:
    with urllib.request.urlopen(urllib.request.Request(plan['url'],headers={'User-Agent':'RCA-T019-source-audit/1.0'}),timeout=45) as response:
        b=response.read(plan['expected_bytes']+1)
        entry.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob_oid=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),status=response.status)
        (BASE/entry['artifact']).write_bytes(b)
        assert len(b)==plan['expected_bytes'] and entry['git_blob_oid']==plan['git_blob_oid']
        entry['verified']=True
except Exception as error: entry['error']=repr(error); raise
finally:
    (BASE/'diagram-manifest.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(entry,indent=2))

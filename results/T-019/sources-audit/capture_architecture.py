"""Small files at the Sock Shop revision announced after metadata capture."""
import hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent; OUT=BASE/'snapshots'
SHA='9dff06fae4981921caec6a62393a6ebfce4b3e3f'
files=['internal-docs/design.md','deploy/docker-compose/docker-compose.yml']
manifest=[]
for f in files:
    url=f'https://raw.githubusercontent.com/microservices-demo/microservices-demo/{SHA}/{f}'
    entry=dict(url=url,revision=SHA,source_path=f,artifact='snapshots/sock-shop-'+Path(f).name,requested_at_utc=datetime.now(timezone.utc).isoformat())
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RCA-T019-source-audit/1.0'}),timeout=45) as r:
            b=r.read(100001)
            assert len(b)<=100000
            entry.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status=r.status)
            (BASE/entry['artifact']).write_bytes(b)
    except Exception as e: entry['error']=repr(e); raise
    finally:
        manifest.append(entry)
        (BASE/'architecture-manifest.json').write_text(json.dumps(dict(total_bytes=sum(x.get('bytes',0) for x in manifest),entries=manifest),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,indent=2))

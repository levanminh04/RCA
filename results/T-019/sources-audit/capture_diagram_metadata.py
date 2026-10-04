import hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent; OUT=BASE/'snapshots'; manifest=[]
def get(name,url,revision=None):
    e=dict(url=url,revision=revision,artifact='snapshots/'+name,requested_at_utc=datetime.now(timezone.utc).isoformat())
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RCA-T019-source-audit/1.0'}),timeout=45) as r:
            b=r.read(100001); assert len(b)<=100000
            e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status=r.status)
            (BASE/e['artifact']).write_bytes(b)
        return json.loads(b)
    except Exception as ex: e['error']=repr(ex); raise
    finally:
        manifest.append(e)
        (BASE/'diagram-metadata-manifest.json').write_text(json.dumps(dict(total_bytes=sum(x.get('bytes',0) for x in manifest),entries=manifest),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
repo='microservices-demo/microservices-demo.github.io'
metadata=get('sock-docs-repository.json',f'https://api.github.com/repos/{repo}')
sha=get('sock-docs-commit.json',f"https://api.github.com/repos/{repo}/commits/{metadata['default_branch']}")['sha']
tree=get('sock-docs-tree.json',f'https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1',sha)
entry=next(e for e in tree['tree'] if e['path']=='assets/Architecture.png')
assert not tree['truncated']
plan=dict(revision=sha,source_path=entry['path'],git_blob_oid=entry['sha'],expected_bytes=entry['size'],url=f"https://raw.githubusercontent.com/{repo}/{sha}/{entry['path']}")
(BASE/'diagram-download-plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print(json.dumps(plan,indent=2))

"""Fetch 30 allowed injection-time metadata only; never fetch any telemetry."""
import hashlib,json,urllib.request
from pathlib import Path
root=Path('D:/RCA-flashticket')
allowed=set(json.loads((root/'results/T-017/allowlist.json').read_text()))
manifest=json.loads((root/'results/T-002/local-inspection/run-002/manifest.json').read_text())
def find_rows(x):
    if isinstance(x,dict):
        if 'case' in x and 'source' in x and str(x['source']).endswith('inject_time.txt'):yield x
        for v in x.values():yield from find_rows(v)
    elif isinstance(x,list):
        for v in x:yield from find_rows(v)
rows={r['case']:r for r in find_rows(manifest) if r['case'] in allowed}
assert set(rows)==allowed
out=Path('D:/RCA-ext/work/T-017/injection');out.mkdir(parents=True,exist_ok=True)
records=[]
for case in sorted(allowed):
    row=rows[case];src=row['source']
    if src.startswith('data/'):
        data=(root/src).read_bytes()
    else:
        assert src.endswith('/'+case+'/inject_time.txt') and '/re2tt_' in src
        with urllib.request.urlopen(src,timeout=40) as f:data=f.read(100)
    assert len(data)<50 and hashlib.sha256(data).hexdigest()==row['sha256'],case
    inject=int(data.decode().strip().splitlines()[0])
    path=out/(case+'.txt');path.write_bytes(data)
    records.append({'case':case,'source':src,'path':str(path),'bytes':len(data),'sha256':row['sha256'],'inject_time':inject})
    print(case,'verified',len(data),flush=True)
(root/'results/T-017/sources/injection-manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')

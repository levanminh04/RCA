import json,glob,sys
from pathlib import Path
v1,v2=Path(sys.argv[1]),Path(sys.argv[2]); same=diff=0; bad=[]
K=('status','ranking','entity_ranking','sets','error','extra','ranking_native')
for v in glob.glob(str(v2/'*/attempt-001/verified.json')):
    jid=Path(v).parts[-3]; o=v1/jid/'attempt-001/result.json'
    if not o.exists() or not (v1/jid/'attempt-001/verified.json').exists(): continue
    a=json.load(open(o,encoding='utf-8'));b=json.load(open(Path(v).parent/'result.json',encoding='utf-8'))
    ka=[{k:r.get(k) for k in K} for r in a['records']];kb=[{k:r.get(k) for k in K} for r in b['records']]
    if ka==kb: same+=1
    else: diff+=1; bad.append(jid[:12])
print(json.dumps({'same':same,'diff':diff,'diff_ids':bad[:10]}))

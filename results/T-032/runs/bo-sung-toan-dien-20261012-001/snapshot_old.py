"""Read-only hashing of pre-existing research files; writes only this new run."""
import hashlib, json, pathlib, time, sys
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).parent
EX=('results/T-032/runs/bo-sung-toan-dien-20261012-001/', 'results/T-033/runs/bo-sung-toan-dien-20261012-001/')
start=time.time(); rows=[]; total=0
for group in ('docs','tasks','src','results'):
    for p in (ROOT/group).rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith(EX) or '__pycache__' in p.parts: continue
        h=hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
        s=p.stat().st_size;total+=s
        rows.append({'path':rel,'bytes':s,'sha256':h.hexdigest()})
        if len(rows)%5000==0:
            print(json.dumps({'files':len(rows),'bytes':total,'elapsed_s':round(time.time()-start,1)}),flush=True)
target=OUT/'old-files-before.json'
if target.exists(): raise RuntimeError('snapshot already exists; preserve it')
target.write_text(json.dumps({'created_epoch':time.time(),'elapsed_s':time.time()-start,'bytes':total,'files':rows},ensure_ascii=False),encoding='utf-8')
print(json.dumps({'done':True,'files':len(rows),'bytes':total,'elapsed_s':round(time.time()-start,1)}),flush=True)

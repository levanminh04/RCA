"""Package only explicitly pinned T032 metadata and reader; no dataset/code tests."""
import ast,hashlib,json,tarfile
from pathlib import Path
repo=Path('D:/RCA-flashticket');root=repo/'results/T-032'
plan_path=root/'runs/research-baro-004/plan.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads(plan_path.read_text(encoding='utf-8-sig'))
script=root/'scripts/research_baro_chain_v1.py'
ast.parse(script.read_text(encoding='utf-8-sig'))
assert sha(script)==plan['script_sha256'] and len(plan['cases'])==52
items=[]
for row in plan['repo_inputs']:
 p=repo/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
 if row['path'].startswith('results/T-032/'):
  items.append((p,'repo/'+row['path']))
items.extend([(plan_path,'sources/research-baro-004-plan.json'),(script,'scripts/research_baro_chain_v1.py')])
rows=[{'local':str(p),'relative':rel,'sha256':sha(p),'bytes':p.stat().st_size} for p,rel in items]
out=root/'runs/research-baro-transfer-001';out.mkdir(exist_ok=False)
archive=out/'payload.tar.gz'
with tarfile.open(archive,'x:gz') as tf:
 for p,rel in items:tf.add(p,arcname=rel,recursive=False)
result={'status':'PREPARED','files':rows,'file_count':len(rows),'archive':{'path':str(archive),'sha256':sha(archive),'bytes':archive.stat().st_size},'plan_sha256':sha(plan_path),'script_sha256':sha(script)}
with (out/'inventory.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps({'file_count':len(rows),'archive_bytes':archive.stat().st_size,'plan_sha256':sha(plan_path),'script_sha256':sha(script)}))

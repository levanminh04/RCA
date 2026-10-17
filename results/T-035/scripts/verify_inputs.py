"""Kiểm đầu ra cũ theo manifest đã có, không tự tạo hash để hợp thức nguồn cũ."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-035/runs/buoc0-001'
def read(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
checks=[]
def verify(p,h,m):
    actual=sha(ROOT/p);checks.append({'path':p,'expected':h,'actual':actual,'manifest':m,'pass':actual==h})
for m in ['results/T-002/handoff-manifest.json','results/T-003/runs/final-review-003/artifact-manifest.json','results/T-034/runs/manifest-cuoi-007/manifest.json']:
    d=read(m)
    rows=d.get('artifacts',d.get('files',[]))
    for row in rows:
        p=row['path']
        if (m.startswith('results/T-034/') or p=='results/T-002/local-inspection/run-002/cases.json'
            or p.startswith('results/T-008/sources/') and '/labels/' not in p
            or p in ['results/T-008/runs/evidence-002/summary.json','results/T-008/runs/file-audit-001/summary.json']):
            verify(p,row['sha256'],m)
m='results/T-029/runs/buoc0-001/manifest.json';d=read(m)
verify('results/T-022/allowlist-dev.json',d['nguon']['results/T-022/allowlist-dev.json'],m)
for p,h in d['src_p3']['tep'].items():verify(p,h,m)
m='results/T-029/runs/step5-001/manifest.json';d=read(m)
for p in ['results/T-022/mappings/universe-re2tt-dev.json','results/T-022/nhan-dev.json']:
    verify(p,d['inputs'][p],m)
m='results/T-026/runs/session-005/handoff-manifest.json';d=read(m)
for p in ['results/T-026/allowlist-dev.json','results/T-026/nhan-dev.json']:
    verify(p,d['files'][p]['sha256'],m)
aux=[]
for receipt in (ROOT/'results/T-008/runs/download-001').glob('*.json'):
    d=json.loads(receipt.read_text('utf-8-sig'))
    if not isinstance(d,dict):continue
    p=d.get('path','')
    if p.startswith('online-boutique/rca_data/') and p.endswith(('source_50.csv','destination_50.csv','dependency.csv')):
        verify('data/ngoai-rcaeval/nezha/'+p,d['sha256'],receipt.relative_to(ROOT).as_posix())
        aux.append({'path':'data/ngoai-rcaeval/nezha/'+p,'sha256':d['sha256'],'receipt':receipt.relative_to(ROOT).as_posix(),
                    'source_url':d['url'],'git_blob_sha':d['git_blob_sha']})
result={'checks':checks,'all_pass':all(c['pass'] for c in checks),'auxiliary_sources':aux,
        'governing_hashes':{p:sha(ROOT/p) for p in ['AGENTS.md','tasks/T-035-p5-do-thi-tu-trace/SPEC.md']}}
(OUT/'input-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'mismatches':[c['path'] for c in checks if not c['pass']]}))
assert result['all_pass'],'input_mismatch'

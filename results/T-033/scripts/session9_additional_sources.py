"""Hash verification only for directly read definitions/scoring and platform document."""
import pathlib,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-033/runs/session9-report-001';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((ROOT/'results/T-029/runs/review4-repair-001/verification.json').read_text(encoding='utf-8'))['files']
paths=['results/T-029/scripts/analyze_step5.py','results/T-029/scripts/bocpd_features.py','results/T-029/scripts/nsigma_flags.py','results/T-029/inputs/src-p3-expected.json','results/T-029/features-no-label/bocpd/dev-03d4910932.json','results/T-029/features-no-label/bocpd/dev-12a1a88069.json','results/T-029/features-no-label/bocpd/dev-4f8a844308.json','results/T-029/features-no-label/bocpd/dev-f36d0647d5.json','results/T-029/features-no-label/nsigma/dev-14372e1209--nsigma.json']
checked={}
for r in paths:
 m=v[r];p=ROOT/r;assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'],r;checked[r]=m
code=json.loads((ROOT/'results/T-029/inputs/src-p3-expected.json').read_text())['tep']
for r in ['src/p3/danh_gia.py','src/p3/adapters/phat_hien.py']:
 p=ROOT/r;assert sha(p)==code[r],r;checked[r]={'sha256':sha(p),'bytes':p.stat().st_size,'source':'results/T-029/inputs/src-p3-expected.json#/tep/'+r.replace('~','~0').replace('/','~1')}
p=pathlib.Path('D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md')
checked[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size,'status':'READ_ONLY_CURRENT_DOCUMENT_PIN; no runtime acceptance inferred'}
(OUT/'additional-source-verification.json').write_text(json.dumps({'status':'PASS','files':checked,'manifest':'results/T-029/runs/review4-repair-001/verification.json'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS additional definitions/scoring/B16 pins')

"""Local SHA checks and source preparation only. Never imports research libraries."""
import pathlib,json,ast,hashlib,datetime,difflib
from session6_control import ROOT,OPEN,sha,write
H=ROOT/'results/T-033/runs/checkpoint-handoff-001'; A=H/'artifacts'
inventory=json.loads((H/'artifact-inventory.json').read_text())
verified={}
for rel,m in inventory.items():
 p=A/rel;assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],rel
 verified[rel]=m
assert set(p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file())==set(inventory)
for rel in ('session5-approval-checkpoint-001','session5-checkpoint-001'):
 d=ROOT/'results/T-033/runs'/rel;j=json.loads((d/'manifest.json').read_text())
 entries=j.get('files',j)
 if isinstance(entries,list):entries={x['path']:x for x in entries}
 for n,m in entries.items():assert sha(d/n)==m['sha256'] and (d/n).stat().st_size==m['bytes'],n
native=json.loads((H/'native-source-manifest.json').read_text())
for n,m in native.items():assert sha(H/'source-native'/n)==m['sha256']
write(OPEN/'fresh-laptop-integrity.json',{'status':'PASS','files':len(verified),'bytes':sum(x['bytes'] for x in verified.values()),'inventory_sha256':sha(H/'artifact-inventory.json'),'approval_and_session5_manifests_verified':True,'native_source_verified':native})
stage=ROOT/'results/T-033/scripts/session6-001';stage.mkdir(exist_ok=False)
for n in ('bocpd_delay.py','channel_context.py','bocpd_core.py'):
 old=(OPEN/'scripts'/n).read_text(encoding='utf-8');new=old
 if n in ('bocpd_delay.py','channel_context.py'):
  new=new.replace("self.home / 'runs/session5-budget-001/ledger.json'","self.scoped(os.environ['T033_PROCESSING_LEDGER_PATH'])") if n=='bocpd_delay.py' else new.replace("home / 'runs/session5-budget-001/ledger.json'","(home / os.environ['T033_PROCESSING_LEDGER_PATH']).resolve()")
 if n=='bocpd_delay.py':
  new=new.replace("for item in sorted(self.source['cases'], key=lambda c: c['opaque_id']):","for item in sorted([c for c in self.source['cases'] if c['opaque_id'] in self.args.cases.split(',')], key=lambda c: c['opaque_id']):")
  new=new.replace("parser.add_argument('--run', default='bocpd-delay-001')","parser.add_argument('--run', required=True)\n    parser.add_argument('--cases', required=True)")
 (stage/n).write_text(new,encoding='utf-8')
 (OPEN/(n+'.stage.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='preserved/'+n,tofile='session6-001/'+n)),encoding='utf-8')
 ast.parse(new)
pins={rel:inventory[rel] for rel in inventory if rel=='inputs/source.json' or rel.startswith(('runs/preflight-002/','runs/nsigma-first-001/','runs/nsigma-rest-001/','runs/bocpd-first-002/','runs/bocpd-rest-001/','runs/core-audit-002/'))}
# Files verified at preflight; all original artifacts retain their own exact hashes.
write(stage/'pins.json',{'task':'T-033','files':pins,'source_sha256':inventory['inputs/source.json']['sha256'],'old_native':native,'artifact_inventory_sha256':sha(H/'artifact-inventory.json')})
write(OPEN/'stage-metadata.json',{'status':'PASS','old_scripts_preserved':True,'staged':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in stage.iterdir() if p.is_file()},'changes':'Guard ledger path only plus BOCPD run/case selection; mathematical descriptions unchanged; new N-Sigma lifecycle separate.'})
print('PASS laptop',len(verified),'staged',stage)

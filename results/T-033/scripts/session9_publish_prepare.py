"""Laptop metadata pins and transport preparation only."""
import pathlib,json,ast
from session9_control import ROOT,OPEN,read,write,sha
inp=read(OPEN/'manual-input.json');catalog={}
for name in ['checkpoint-handoff-001','session6-compute-checkpoint-001','session8-extraction-001','session8-evidence-receive-001','session8-stats-receive-001','session9-manual-receive-001']:
 base=ROOT/'results/T-033/runs'/name;inv=read(base/'artifact-inventory.json');entries=inv.get('files',inv)
 if isinstance(entries,list):entries={x.get('path',x.get('relative_path')):x for x in entries}
 for r,m in entries.items():
  p=base/'artifacts'/r;assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],r
  nm={'bytes':m['bytes'],'sha256':m['sha256']}
  if r in inp['pins'] and {k:inp['pins'][r][k] for k in nm}!=nm:
   # Historical live-status snapshots are different artifacts, not scientific
   # inputs. Preserve their inventory namespaces; never pin a stale alias.
   assert not r.startswith('runs/'),r
   catalog[name+'::'+r]={'local_path':str(p.relative_to(ROOT)).replace('\\','/'),**nm,'historical_snapshot_only':True}
   continue
  inp['pins'][r]=nm
  catalog[r]={'local_path':str(p.relative_to(ROOT)).replace('\\','/'),**nm}
inp['catalog']=catalog
ast.parse((ROOT/'results/T-033/scripts/session9_publish.py').read_text(encoding='utf-8'))
write(OPEN/'publish-input.json',inp)
s=(ROOT/'results/T-033/scripts/session9_receive.py').read_text(encoding='utf-8')
s=s.replace('session9-manual-receive-001','session9-final-receive-001').replace('session9-manual-001','session9-final-001').replace('session9-receive-stream-001','session9-final-stream-001')
(ROOT/'results/T-033/scripts/session9_final_receive.py').write_text(s,encoding='utf-8',newline='\n')
print('PASS inventories, pins and publication AST')

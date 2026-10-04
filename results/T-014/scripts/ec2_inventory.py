import os
from pathlib import Path
base=Path('/home/ubuntu/rca/T-014')
os.environ.update(TMPDIR=str(base/'tmp'),XDG_CACHE_HOME=str(base/'cache'),PYTHONDONTWRITEBYTECODE='1')
import json,sys,csv,hashlib,importlib.metadata as md,subprocess
packages=['numpy','pandas','scipy','scikit-learn','causal-learn','networkx','pyarrow','psutil']
environment=dict(python=sys.version,executable=sys.executable,packages={p:md.version(p) for p in packages},source_revision=subprocess.check_output(['git','-C','/home/ubuntu/rca/src/RCAEval','rev-parse','HEAD'],text=True).strip(),limits='read-only shared source/env; all outputs and temporary/cache paths in own task')
(base/'environment.json').write_text(json.dumps(environment,indent=2))
records=[]
for p in sorted(base.rglob('*')):
    if not p.is_file() or p.name=='external-files.csv':continue
    records.append(dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
with (base/'external-files.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(records)
print(json.dumps(dict(environment=environment,files=len(records),logical_bytes=sum(r['bytes'] for r in records))))

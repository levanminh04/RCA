"""Read-only dataset adapter using existing py312's pyarrow; no method run."""
from pathlib import Path
import numpy as np
import pandas as pd
import json, hashlib
root=Path('D:/RCA-flashticket'); work=Path('D:/RCA-ext/work/T-013');work.mkdir(exist_ok=True)
dev=sorted((root/'data/rcaeval').glob('re2tt_*'));assert len(dev)==30
src=sorted([p/'metrics.parquet' for p in dev],key=lambda p:(-p.stat().st_size,str(p)))[0]
d=pd.read_parquet(src)
np.savez_compressed(work/'metrics-selected.npz',values=d.to_numpy(),columns=np.array(d.columns,dtype=str))
meta={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'shape':list(d.shape),'adapter_python':'existing py312; pyarrow','output':str(work/'metrics-selected.npz'),'output_sha256':hashlib.sha256((work/'metrics-selected.npz').read_bytes()).hexdigest()}
(work/'metrics-selected.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(json.dumps(meta))

"""Kiểm lại metadata raw columns; giữ nguyên native numbers và lượt hỏng."""
import hashlib
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
from p3.adapters.phat_hien import cot_bocpd,tien_xu_ly_bocpd
from bocpd_core import result_from_R
H=Path(os.environ['T033_HOME']).resolve()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
S=json.loads((H/'inputs/source.json').read_text())
oid='dev-20acb4402d'
item=next(c for c in S['cases'] if c['opaque_id']==oid)
old=H/'runs/bocpd-first-001'
manifest=json.loads((old/'manifest.json').read_text())
record_path=old/(oid+'--full.json'); record=json.loads(record_path.read_text())
assert sha(record_path)==manifest[record_path.name]['sha256']
assert record['checks']['detector_columns'] is False
assert all(v for k,v in record['checks'].items() if k!='detector_columns')
path=old/(oid+'--full.npz'); assert sha(path)==record['sha256']==manifest[path.name]['sha256']
mp=Path.home()/'rca/T-025/repo'/item['files']['metrics.parquet']['path']
assert sha(mp)==item['files']['metrics.parquet']['sha256']
df=pd.read_parquet(mp); raw_columns=cot_bocpd(df.columns); full=tien_xu_ly_bocpd(df[raw_columns])
with np.load(path,allow_pickle=False) as z:
    assert np.array_equal(z['times'],df['time'].to_numpy())
    assert np.array_equal(z['X'],full.to_numpy(),equal_nan=True)
    assert z['columns'].tolist()==list(full)
    assert record['result']['detector_columns']==list(full)
    result=result_from_R(z['R'],z['maxes'],z['times'],len(raw_columns),full.shape[1],raw_columns)
expected=item['expected']['bocpd']
checks={k:result.get(k)==expected.get(k) for k in ['status','alarms','chi_so','input_shape','detector_columns','diagnostics']}
assert all(checks.values()),checks
out=H/'runs/full-metadata-recheck-001'; out.mkdir(exist_ok=False)
doc={'status':'PASS','opaque_id':oid,'npz':str(path.relative_to(H)),'sha256':sha(path),
     'source_sha256':sha(H/'inputs/source.json'),'result':result,'checks':checks,
     'old_record':str(record_path.relative_to(H)),'old_record_sha256':sha(record_path),
     'same_input_native_validation_from_old_run':{k:v for k,v in record['checks'].items() if k.startswith('same_input_')},
     'change':'Chỉ raw detector_columns metadata; processed columns và X trong NPZ giữ đúng. Không đổi R/m/CP/tham số/tiêu chí khớp.'}
(out/'verification.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2))
print('PASS metadata raw columns repaired in new result; R/m/CP and processed input unchanged')

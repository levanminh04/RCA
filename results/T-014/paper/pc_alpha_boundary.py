"""Phép kiểm alpha: correlation được dựng từ p=.03 trước mọi lời gọi PC.

Không chọn mẫu/cấu hình theo RCA scores hoặc accuracy. Ba variables có p hữu
nghị giữa .01 và .05 để kiểm đúng chiều decision rule p>alpha->remove edge.
"""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from scipy.stats import norm
from causallearn.utils.cit import CIT
from causallearn.search.ConstraintBased.PC import pc

out=Path(__file__).resolve().parent/'pc-alpha-boundary'
out.mkdir(exist_ok=True)
seed,n,target_p=20261004,2000,.03
rng=np.random.default_rng(seed)
raw=rng.normal(size=(n,3));q=np.linalg.qr(raw-raw.mean(axis=0))[0]
target_r=float(np.tanh(norm.ppf(1-target_p/2)/np.sqrt(n-3)))
data=np.column_stack([q[:,0],target_r*q[:,0]+np.sqrt(1-target_r**2)*q[:,1],q[:,2]])
pre={'utc':datetime.now(timezone.utc).isoformat(),'seed':seed,'n':n,'target_p':target_p,
     'target_r':target_r,'derivation':'r=tanh(norm.ppf(1-p/2)/sqrt(n-3)); orthonormal centered x,z; y=r*x+sqrt(1-r*r)*z; third variable orthogonal',
     'purpose':'threshold mechanism, no RCA ranking/labels/accuracy',
     'input_sha256':hashlib.sha256(data.tobytes()).hexdigest(),'estimated_before_run_seconds':10}
(out/'config-before-run.json').write_text(json.dumps(pre,indent=2)+'\n',encoding='utf-8')
np.save(out/'input.npy',data)
actual_p=float(CIT(data,'fisherz')(0,1,()))
records=[]
for alpha in [.01,.05,.1]:
    tic=time.monotonic();g=pc(data,alpha=alpha,indep_test='fisherz',show_progress=False)
    edge_count=int(np.count_nonzero(np.triu(g.G.graph,1)))
    expected=0 if actual_p>alpha else 1
    records.append({'alpha':alpha,'p_01':actual_p,'expected_edge_count':expected,
                    'edge_count':edge_count,'matrix':g.G.graph.tolist(),
                    'threshold_check_pass':edge_count==expected,
                    'elapsed_diagnostic':time.monotonic()-tic})
report={'config_before':pre,'actual_p':actual_p,'records':records,
        'pass':all(x['threshold_check_pass'] for x in records),'time_is_official':False,
        'cannot_replace':'Không đo alpha sensitivity hay accuracy của default RE2-TT, chỉ kiểm ý nghĩa alpha với Fisher-Z đã ghim.'}
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
assert report['pass']

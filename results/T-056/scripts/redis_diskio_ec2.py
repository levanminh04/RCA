import json,sys
import numpy as np, pyarrow.parquet as pq
from pathlib import Path
req=json.loads(sys.stdin.read()); out=[]
for o,c in sorted(req['cases'].items()):
    if c['dataset']!='RE3-OB': continue
    m=pq.read_table(Path(c['data_root'])/c['files']['metrics.parquet'],columns=['time','redis_diskio']).to_pandas()
    t=c['t']; N=m.loc[(m.time>=t-300)&(m.time<t),'redis_diskio'].dropna().to_numpy(); A=m.loc[(m.time>=t)&(m.time<t+300),'redis_diskio'].dropna().to_numpy()
    out.append([o, float(np.median(N)), float(np.percentile(N,75)-np.percentile(N,25)), float(A.max()), float(N.max()), int(len(np.unique(N)))])
print(json.dumps(out))

"""T-033 lõi N-Sigma: pandas Series nguyên bản, dừng nếu flags lệch."""
import argparse
import hashlib
import json
import os
import resource
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
from baro.anomaly_detection import nsigma as native
from p3.adapters.phat_hien import nsigma as adapter, cot_bocpd

H = Path(os.environ['T033_HOME']).resolve()
SOURCE = json.loads((H/'inputs/source.json').read_text())
PREFLIGHT = H/'runs'/os.environ['T033_PREFLIGHT']
INV = json.loads((PREFLIGHT/'inventory.json').read_text())
assert json.loads((PREFLIGHT/'verification.json').read_text())['status']=='PASS'
PATHS = {x['opaque_id']:x['files'] for x in INV['cases']}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
def progress(msg):
    s = datetime.now(timezone.utc).isoformat()+' '+msg
    print(s,flush=True)
    with (H/'trang-thai.txt').open('a') as f: f.write(s+'\n')
def used(): return sum(p.stat().st_size for p in H.rglob('*') if p.is_file())

def statistics(data):
    cols = [c for c in data if c!='time']
    x = data[cols].to_numpy()
    means = np.full(x.shape,np.nan)
    stds = np.full(x.shape,np.nan)
    count = np.zeros(x.shape,dtype=np.uint16)
    flags = np.zeros(x.shape,dtype=bool)
    for j,c in enumerate(cols):
        col = data[c]
        for i in range(100,len(data)):
            history = col.iloc[:i]
            means[i,j] = history.mean()
            stds[i,j] = history.std()
            count[i,j] = history.count()
            flags[i,j] = abs(col.iloc[i]-means[i,j]) > 3*stds[i,j]
    return {'x':x,'mean':means,'std':stds,'count':count,'threshold':3*stds,
            'margin':np.abs(x-means)-3*stds,'Z':flags,'columns':np.array(cols),
            'times':data['time'].to_numpy(),'evaluated':np.arange(len(data))>=100}

def fixtures():
    checks = []
    for name,arr in [('constant',np.full(110,2.)),('step',np.r_[np.zeros(100),np.ones(10)]),
                    ('repeated',np.tile([0.,1.],55)),('leading_missing',np.r_[np.full(101,np.nan),np.arange(9.)]),
                    ('nonfinite',np.r_[np.zeros(100),np.nan,np.inf,-np.inf,np.ones(7)])]:
        raw = pd.DataFrame({'time':np.arange(110),'a':arr})
        data = raw.replace([np.inf,-np.inf],np.nan).ffill()
        stats = statistics(data)
        alarms = data['time'].to_numpy()[stats['Z'].any(axis=1)].tolist()
        expected = sorted(set(native(data,k=3,startsfrom=100)))
        assert alarms == expected
        if name=='step': assert stats['std'][100,0]==0 and stats['Z'][100,0]
        if name=='constant': assert not stats['Z'].any()
        if name=='leading_missing': assert not stats['Z'][100,0] and np.isnan(stats['std'][100,0])
        checks.append({'fixture':name,'flags_native_match':True,'alarms':alarms})
    # Tay độc lập: 100 mẫu gồm 50 số0 và 50 số2: mean1, var mẫu100/99.
    data=pd.DataFrame({'time':np.arange(101),'a':np.r_[np.tile([0.,2.],50),5.]})
    stats=statistics(data)
    assert stats['mean'][100,0]==1 and stats['std'][100,0]==np.sqrt(100/99)
    assert stats['count'][100,0]==100 and stats['Z'][100,0]
    checks.append({'fixture':'manual_mean_ddof1_strict','pass':True})
    return checks

def main(args):
    run=H/'runs'/args.run
    run.mkdir(parents=True,exist_ok=False)
    result={'status':'RUNNING','pid':os.getpid(),'script_sha256':sha(__file__),
            'source_sha256':sha(H/'inputs/source.json'),'cases':{},'command':sys.argv,
            'started_utc':datetime.now(timezone.utc).isoformat()}
    write(run/'status.json',result)
    t0=time.perf_counter()
    try:
        write(run/'fixtures.json',{'status':'PASS','checks':fixtures()})
        cases=SOURCE['cases'][:1] if args.first else SOURCE['cases'][1:]
        for item in cases:
            oid=item['opaque_id']
            if (H/'STOP').exists(): raise RuntimeError('Minh/agent STOP')
            assert used()<SOURCE['budget_bytes']
            assert time.perf_counter()-t0 < SOURCE['budget_compute_s']
            p=Path(PATHS[oid]['metrics.parquet'])
            assert sha(p)==item['files']['metrics.parquet']['sha256']
            raw=pd.read_parquet(p)
            case={}
            for detector,tap in [('nsigma','bocpd'),('nsigma_doi_chung','tat_ca')]:
                progress('NSIGMA START '+oid+'/'+detector)
                start=time.perf_counter()
                cols=cot_bocpd(raw.columns) if tap=='bocpd' else [c for c in raw if c!='time']
                data=raw[['time']+cols].replace([np.inf,-np.inf],np.nan).ffill()
                stats=statistics(data)
                dest=run/(oid+'--'+detector+'.npz')
                projected=sum(a.nbytes for a in stats.values() if isinstance(a,np.ndarray))+65536
                assert used()+projected<SOURCE['budget_bytes'], 'Storage budget before write'
                # Giữ output dù phép so sau đó thất bại.
                np.savez_compressed(dest,**stats)
                fp=H/'inputs'/item['flags'][detector]['path']
                assert sha(fp)==item['flags'][detector]['sha256']
                with np.load(fp,allow_pickle=False) as frozen:
                    checks={'flags':np.array_equal(stats['Z'],frozen['Z']),
                            'columns':np.array_equal(stats['columns'],frozen['columns']),
                            'times':np.array_equal(stats['times'],frozen['times'])}
                alarms=[int(t) for t in stats['times'][stats['Z'].any(axis=1)]]
                core=adapter(raw,tap_cot=tap)
                checks['native_adapter_status']=core['status']==item['expected'][detector]['status']=='OK'
                checks['native_adapter_alarms']=core['alarms']==alarms==item['expected'][detector]['alarms']
                checks['native_adapter_columns']=core['detector_columns']==cols
                record={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
                        'opaque_id':oid,'detector':detector,'output_npz':dest.name,'sha256':sha(dest),
                        'bytes':dest.stat().st_size,'wall_s':time.perf_counter()-start,
                        'rss_peak_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                        'alarm_count':len(alarms),'first_index':int(np.flatnonzero(stats['Z'].any(axis=1))[0]) if alarms else None,
                        'max_d':len(cols),'T':len(data),'source_flags':item['flags'][detector]}
                write(run/(oid+'--'+detector+'.json'),record)
                case[detector]=record
                result['cases'][oid]=case
                write(run/'status.json',result)
                if not all(checks.values()): raise RuntimeError('NSIGMA flags/source mismatch '+oid+'/'+detector)
                progress('NSIGMA PASS '+oid+'/'+detector+' wall_s='+str(round(record['wall_s'],2)))
            byteused=used()
            result['resources']={'new_bytes':byteused,'disk_free_bytes':shutil.disk_usage(H).free,
                                 'ram_available_bytes':psutil.virtual_memory().available}
            write(run/'status.json',result)
            assert byteused<SOURCE['budget_bytes']
        result['status']='PASS'
    except BaseException as exc:
        result['status']='STOPPED'
        result['error']=type(exc).__name__+': '+str(exc)
        traceback.print_exc()
        progress('STOP '+result['error'])
        raise
    finally:
        result['wall_s']=time.perf_counter()-t0
        result['ended_utc']=datetime.now(timezone.utc).isoformat()
        write(run/'status.json',result)
        write(run/'manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in run.iterdir() if p.is_file() and p.name!='manifest.json'})
        progress('NSIGMA '+result['status']+' '+args.run)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',required=True)
    parser.add_argument('--first',action='store_true')
    main(parser.parse_args())

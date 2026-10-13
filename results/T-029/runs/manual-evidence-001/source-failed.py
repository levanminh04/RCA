"""Đọc trung gian tại các ca đã ghi danh sách; không gọi detector/ranker."""
import math
import time
import numpy as np
import pandas as pd
from resume_step7 import ROOT, OUT, read, sha, log, write, now
from p3.selector import nap_allowlist, chon_ca
from bocpd_features import prepare, b4_components

def main():
    log('Lệnh có ghi: T-014-main python -B -W ignore scripts/manual_evidence.py; đọc raw dev qua guard chỉ tại danh sách đã ghi. Tính trung gian tại t̂, không tính lại chuỗi báo động/đặc trưng đã hợp lệ.')
    start=time.perf_counter(); run=OUT/'runs/manual-evidence-001'
    assert not run.exists(); run.mkdir()
    selection=read(OUT/'runs/manual-selection-001/selection.json')
    rows=read(OUT/'theo-ca.json')['rows']; allow=nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
    v7=read(OUT/'runs/step5-001/V7.json')['cases']; interventions=read(OUT/'bocpd-can-thiep.json')['cases']
    evidence=[]; raw_cache={}; checks=[]
    for selected in selection['selected']:
        t0=time.perf_counter(); i=selected['row_index']; r=rows[i]; oid=r['opaque_id']; det=r['detector']; th=r['t_hat_index']
        if oid not in raw_cache:
            files=chon_ca(allow,oid,ROOT,kiem_hash=True,tep=['metrics.parquet'])
            raw_cache[oid]=(files['metrics.parquet'],pd.read_parquet(files['metrics.parquet']))
        rawpath,raw=raw_cache[oid]; f=read(ROOT/r['feature_source']['path'])
        assert sha(ROOT/r['feature_source']['path'])==r['feature_source']['sha256']
        item={'row_index':i,'opaque_id':oid,'detector':det,'cell':r['cell'],'group':r['first_group'],'flags':r['primary_flags'],'D0':r['D0'],
              't_hat':th,'t_hat_plus':r['t_hat_plus_index'],'raw_source':rawpath.relative_to(ROOT).as_posix(),'raw_sha256':sha(rawpath),
              'source':r['feature_source']['path'],'row_pointer':'/rows/'+str(i),'selection_reasons':selected['reasons']}
        if det=='bocpd':
            data,ends,_=prepare(raw); assert data.columns.tolist()==f['columns']
            item['B1']=f['B1_t_hat']; item['leading_nan_end']=ends
            item['intervention']=interventions[oid]
            item['V7']=v7[oid]; item['B4_raw']={}
            for w in (15,30,60):
                comp=b4_components(data,th,w); old=f['B4_t_hat'][str(w)]
                assert (comp is not None)==old['valid']
                if comp is None: item['B4_raw'][str(w)]={'valid':False}; continue
                regular=np.flatnonzero(comp['regular']); j=int(regular[np.argmax(comp['ratio'][regular])]) if len(regular) else None
                maximum=None if j is None else float(comp['ratio'][j])
                assert maximum==old['max_ratio_positive_mad']
                constants=[c for c,z in zip(data.columns,comp['constant_change']) if z]
                assert constants==old['constant_change_columns']
                item['B4_raw'][str(w)]={'valid':True,'max_column':None if j is None else data.columns[j],
                   'before':None if j is None else float(comp['before'][j]),'after':None if j is None else float(comp['after'][j]),
                   'mad':None if j is None else float(comp['mad'][j]),'jump':None if j is None else float(comp['jump'][j]),
                   'normalized':maximum,'constant_change_columns':constants,'constant_count':len(constants),'flags':old['flags']}
            checks.append({'pair':oid+'/'+det,'B4_raw_matches':True})
        else:
            item.update({k:f[k] for k in ('history','r_obs','r_ind','r_nom','N1','N2','N3','N4','N5_types','N6_minutes','trigger_columns')})
            item['trigger_raw']=[]
            filled=raw.replace([np.inf,-np.inf],np.nan).ffill()
            zpath=ROOT/f['nguon']['Z_path']; assert sha(zpath)==f['nguon']['Z_sha256']
            with np.load(zpath,allow_pickle=False) as z:
                Z=z['Z']; columns=z['columns'].tolist()
                trigger=[c for c,hit in zip(columns,Z[th]) if hit]; assert trigger==f['trigger_columns']
                for j,c in enumerate(columns):
                    if c not in trigger:continue
                    series=filled[c]; before=series.iloc[:th]; mean=float(before.mean()); std=float(before.std()); val=float(series.iloc[th])
                    diff=abs(val-mean); threshold=3*std
                    assert diff>threshold and math.isclose(std,f['columns'][j]['std_at_first'],rel_tol=1e-12,abs_tol=1e-12)
                    assert f['columns'][j]['so_bao_Nv']==int(Z[100:720,j].sum())
                    item['trigger_raw'].append({'column':c,'type':f['columns'][j]['type'],'value':val,'past_mean':mean,'past_std':std,
                           'difference':diff,'threshold':threshold,'p_j':f['columns'][j]['p_j'],'Nv_alarm_count':int(Z[100:720,j].sum()),
                           'std_zero':std==0,'sample':{'indices':list(range(th-2,th+3)),'values':[None if pd.isna(x) else float(x) for x in series.iloc[th-2:th+3]]}})
            checks.append({'pair':oid+'/'+det,'trigger_raw_matches':True})
        item['wall_s']=time.perf_counter()-t0; evidence.append(item)
        log('Đã đọc trung gian/raw '+oid+'/'+det+'; nguồn/hash và phép so tại báo động khớp; '+format(item['wall_s'],'.3f')+' s. Chưa suy nguyên nhân nhân quả.')
    d={'status':'PASS','selection_source':{'path':'results/T-029/runs/manual-selection-001/selection.json','sha256':sha(OUT/'runs/manual-selection-001/selection.json')},
       'rows':evidence,'row_count':len(evidence),'raw_case_count':len(raw_cache),'checks':checks,'time':now(),'wall_s':time.perf_counter()-start}
    write(run/'evidence.json',d)
    for x in evidence:
        if x['detector']=='bocpd':
            b=x['B4_raw']['30']; a=x['intervention']; print(json_safe({'oid':x['opaque_id'],'det':x['detector'],'group':x['group'],'th':x['t_hat'],'plus':x['t_hat_plus'],'flags':x['flags'],
                'cp_Nv':a['cp_counts_Nv'],'B2':{k:v['B2'] for k,v in a['sensitivity'].items()},'B4':b,'V7_w30k3':x['V7']['B4']['30']['3']}))
        else: print(json_safe({'oid':x['opaque_id'],'det':x['detector'],'th':x['t_hat'],'flags':x['flags'],'ratios':[x[k] for k in ('r_obs','r_ind','r_nom')],
                      'history':{k:v['ti_le'] for k,v in x['history'].items()},'triggers':x['trigger_raw']}))
def json_safe(x):
    import json
    return json.dumps(x,ensure_ascii=True)
if __name__=='__main__':main()

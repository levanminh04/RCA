"""K8/C2 trung gian cấu trúc không nhãn; gọi sau lượt đồ thị đầy đủ."""
import sys,time,json
from pathlib import Path
from collections import Counter
from run import ROOT,OUT,read,write,np,pd,selector,nezha,nhan
from p3.cua_so import cat_span

out=OUT/'runs'/sys.argv[1];out.mkdir(exist_ok=False)
assert read(OUT/'runs/day-du-001/summary.json')['status']=='PASS','graph_barrier'
jobs=read(OUT/'runs/day-du-001/summary.json')['cases'];results=[];start=time.perf_counter()
for c in jobs:
    ds,oid=c['dataset'],c['opaque_id'];started=time.perf_counter()
    if ds=='RE2-TT':
        allow=selector.nap_allowlist(ROOT/'results/T-022/allowlist-dev.json');files=selector.chon_ca(allow,oid,ROOT,tep=['traces.parquet'])
        frame=pd.read_parquet(files['traces.parquet']);t=nhan.nap_moc(ROOT/'results/T-022/nhan-dev.json')[oid]
        frame=cat_span(frame,t);t_ns=t*nezha.NS
    else:
        allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json');s=nezha.chon_ca(allow,oid,ROOT)
        frame=nezha.doc_cua_so(s)['spans'];t_ns=s['t_ns']
    f=frame.copy(deep=False)
    key=(f.traceID.astype(str)+'|'+f.spanID.astype(str)).to_numpy()
    position=pd.Series(np.arange(len(f)),index=key);position=position[~position.index.duplicated(keep=False)]
    parent=(f.traceID.astype(str)+'|'+f.parentSpanID.astype(str)).map(position).to_numpy(dtype='float64')
    valid=~np.isnan(parent);pi=np.where(valid,parent,0).astype('int64')
    ent=f.serviceName.astype(str).to_numpy()
    cross=valid&(ent[pi]!=ent);child=np.flatnonzero(cross);parents=pi[cross]
    end=(f._end_ns.to_numpy() if '_end_ns' in f else (f.startTime.to_numpy()+f.duration.to_numpy())*1000)
    starts=(f._start_ns.to_numpy() if '_start_ns' in f else f.startTime.to_numpy()*1000)
    calls=pd.DataFrame({'caller':ent[parents],'callee':ent[child],'after':end[parents]>=t_ns})
    edges=[]
    for (a,b),g in calls.groupby(['caller','callee'],sort=True):
        n=int((~g.after).sum());aa=int(g.after.sum())
        edges.append({'caller':a,'callee':b,'before':n,'after':aa,'enough_20_each':n>=20 and aa>=20})
    counts=f.groupby('traceID').size();a=starts>=t_ns
    roots=f.parentSpanID.fillna('').astype(str).isin(['','0','-1','root','0000000000000000']).to_numpy()
    lost=~valid&~roots
    # Kiểm mất cha trong A riêng; F parent và A parent là hai scope khác nhau.
    a_parent=valid&a[pi]
    lost_a=a&~a_parent&~roots
    b=end>=t_ns;b_parent=valid&b[pi];lost_b=b&~b_parent&~roots
    result={'dataset':ds,'opaque_id':oid,'F_rows':len(f),'edge_counts_parent_end_split':edges,
            'span_count_per_trace':{str(int(k)):int(v) for k,v in counts.value_counts().sort_index().items()},
            'A_start_traces':int(f.loc[a,'traceID'].nunique()),
            'A_traces_missing_parent_in_F':int(f.loc[a&lost,'traceID'].nunique()),
            'A_traces_missing_parent_in_A':int(f.loc[lost_a,'traceID'].nunique()),
            'A_end_traces':int(f.loc[b,'traceID'].nunique()),
            'A_end_traces_missing_parent_in_A_end':int(f.loc[lost_b,'traceID'].nunique()),
            'seconds':time.perf_counter()-started}
    write(out/'cases'/ds/f'{oid}.json',result);results.append(result)
    print(ds,oid,len(f),'PASS',flush=True)
write(out/'summary.json',{'status':'PASS','label_free':True,'cases':results,'seconds':time.perf_counter()-start,
                         'protocol':'F theo p3; parent end split cho đếm n_before/n_after, 20 mỗi phía theo call_slow_table_v1.py MIN_CALLS. Không tính tín hiệu hoặc điểm.'})

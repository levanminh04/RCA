"""Selected root numeric leaves: arithmetic from prior results only, no method import."""
from pathlib import Path
import csv,json,hashlib,math,time,sys,statistics
import numpy as np
from scipy import linalg

R=Path('D:/RCA-flashticket');O=R/'results/T-020/trung-gian/method_evidence';t0=time.monotonic()
sys.path.insert(0,str(O/'scripts'))
from microrank_independent_copy import recompute_group,recompute_spectrum
def jr(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def keyget(q,key):
    for k in key.split('/')[1:]:q=q[int(k)] if isinstance(q,list) else q[k.replace('~1','/').replace('~0','~')]
    return q
selected=[x for x in csv.DictReader((R/'results/T-020/trung-gian/root/numeric-leaves.csv').open(encoding='utf-8-sig')) if x['task'] in ['T-013','T-014','T-015','T-017'] and x['selected']=='True']
checks=[];groupcache={};querycache={}
for row in selected:
    p=R/row['path'];q=jr(p);key=row['key'];expected=keyget(q,key);query='';reason='';actual=None
    try:
        if row['task']=='T-013':
            ix=int(key.split('/')[2]) if key.startswith('/checks/') else int(key.split('/')[1]);c=q['checks'][ix] if isinstance(q,dict) else q[ix];tag=c['check']
            if key.endswith('/n_metrics'):
                z=R/'results/T-013/runs/20261004-083543'/f'{tag}-metric.csv';actual=len(list(csv.DictReader(z.open(encoding='utf-8-sig'))));query=f'count rows {z}'
            elif key.endswith('/max_normalized_score_error'):
                z=R/'results/T-013/runs/20261004-083543'/f'{tag}-metric.csv';rr=list(csv.DictReader(z.open(encoding='utf-8-sig')))
                err=[abs((float(x['max_post'])-float(x['median']))/float(x['scale_effective'])-float(x['official_score']))/max(1,abs(float(x['official_score']))) for x in rr]
                actual=max(err);query=f'max |(max_post-median)/scale_effective-official_score|/max(1,|official_score|) over {len(rr)} rows {z}'
                reason='CSV decimal roundtrip; zero compared with 1e-12 tolerance'
            elif key.endswith('/a_cpu/score'):
                n=np.arange(3,dtype=float);post=np.arange(3,12,dtype=float);actual=float((post.max()-np.median(n))/(np.quantile(n,.75)-np.quantile(n,.25)));query='saved synthetic definition kiem_co_che.py:275–278 normal=0,1,2 post=3..11; robust max signed'
            elif key.endswith('/official_mean'):
                actual=float(np.mean(1e16+np.arange(6)*2));query='saved nearconstant fixture kiem_sua_phan_bien.py:93; np.mean(1e16+arange(6)*2), binary64 rounding retained'
        elif row['task']=='T-014':
            if key.endswith('/true_service_rank'):
                ix=int(key.split('/')[2]);case=q['per_case'][ix]['case'];stem=case.split('/')[-2]+'_'+case.split('/')[-1];z=R/'results/T-014/audit/graph-factors'/f'{stem}_reverse_drop.json';v=jr(z)
                ranks=v.get('ranks',v.get('ranks_author_stable_sort',[]));services=list(dict.fromkeys(s.split('_')[0].replace('-db','') for s in ranks));root=case.split('/')[-2].split('_')[0];actual=services.index(root)+1;query=f'canonical service order from {z} saved ranks; root metadata only for scoring'
            elif key=='/points/shippingservice_mem':
                s=jr(R/'results/T-014/audit/mem-target/checkoutservice_mem_2.json');meta=next(x for x in jr('D:/RCA-ext/work/T-014/audit-r/mem-target/inputs.json') if x['stem']=='checkoutservice_mem_2')
                z=Path(meta['input']);rows=list(csv.DictReader(z.open(encoding='utf-8-sig')));cols=list(rows[0]);ts=np.asarray(meta['times'],float);grid=np.arange(s['context']['train_time'][0],s['context']['test_time'][1]+1,dtype=float)
                def series(c):return np.interp(grid,ts,np.asarray([float(x[c]) for x in rows]))
                parents=[a for a,b in s['graph_edges'] if b=='shippingservice_mem'];y=series('shippingservice_mem');x=np.column_stack([series(c) for c in parents]);tx=np.asfortranarray(x[:111]);vx=np.asfortranarray(x[-10:]);ty=y[:111];vy=y[-10:];xm=tx.mean(axis=0);ym=ty.mean();beta=linalg.lstsq(tx-xm,ty-ym,cond=max(tx.shape)*np.finfo(float).eps)[0];intercept=ym-xm@beta
                train=ty-(tx@beta+intercept);test=vy-(vx@beta+intercept);mean=train.mean();var=np.mean((train-mean)**2);scale=math.sqrt(var) if var else 1.;actual=float(np.max(np.abs((test-mean)/scale)));query=f'OLS independent scipy lstsq on saved TX2 derived {z}; parents {parents}, train111/test10, resample np.interp; no CIRCA import'
                reason='Replays OLS/RHT algebra on prior derived TX2 input; graph and upstream preprocessing held fixed'
            elif '/score_info/' in key:
                service=key.split('/')[2];node=q['score_info'][service];confidence=node['info']['Confidence'];actual=statistics.NormalDist().inv_cdf((confidence+1)/2);query=f'NormalDist.inv_cdf((saved score_info/{service}/info/Confidence+1)/2)';reason='Checks Gaussian confidence/score relation; does not independently refit SVR'
            elif key.endswith('/p'):
                rec=q['records'][int(key.split('/')[2])];ci=rec['CI'][int(key.split('/')[4])];a=np.load(R/'results/T-014/paper/pc-fixtures-002/synthetic-inputs.npz')['collider'];rho=np.corrcoef(a[:,ci['a']],a[:,ci['b']])[0,1];z=math.sqrt(len(a)-3)*.5*math.log((1+rho)/(1-rho));actual=2*(1-statistics.NormalDist().cdf(abs(z)));query=f'Fisher z from saved synthetic npz collider N={len(a)}, CI a={ci["a"]},b={ci["b"]},S={ci["S"]}; no PC import'
        elif row['task']=='T-015':
            if key.startswith('/group_intermediates/'):
                snapshot=Path(q['input_path']);
                if not snapshot.exists() and q['input_path'].startswith('/home/ubuntu/rca/T-015/'):
                    snapshot=R/'results/T-015'/q['input_path'].split('/T-015/')[1]
                s=jr(snapshot);g=key.split('/')[2];cache=(str(snapshot),g)
                if cache not in groupcache:groupcache[cache]=recompute_group(s['groups'][g],g=='anomaly',s['options'])
                actual=float(keyget(groupcache[cache],'/'+key.split('/',3)[3]));query=f'independent saved graph incidence→float32 prior→25 synchronous updates, group={g}, {snapshot}; author imports absent'
            elif key.startswith('/spectrum/'):
                op=key.split('/')[2];a=q['groups']['anomaly'];weight=a['official']['weights'][op];count=a['official']['tracecounts'][op];actual=weight*(a['trace_count']-count);query=f'saved anomaly weight({weight})*(group trace_count({a["trace_count"]})-op count({count})) for {op}'
        elif row['task']=='T-017':
            ix=int(key.split('/')[1]);c=q[ix];z=Path(c['score_file'])
            if key.endswith('/positive_services'):
                z=z.with_name(z.stem+'-normal-control.json');v=jr(z);actual=sum(x['metric']+x['trace']+x['log']>0 for x in v['scores'].values());query=f'count positive sum(metric,trace,log) from {z}'
            else:
                v=jr(z);score={s:x['metric']+x['trace']+x['log'] for s,x in v['scores'].items()};root=c['root_for_evaluation'];rs=score[root];lo=1+sum(x>rs for x in score.values());hi=sum(x>=rs for x in score.values());k=int(key.split('/')[2][3:]);kind=key.split('/')[3]
                actual={'hit_optimistic':float(lo<=k),'hit_pessimistic':float(hi<=k),'hit_fractional':sum(i<=k for i in range(lo,hi+1))/(hi-lo+1),'mrr_fractional':sum(1/i for i in range(lo,hi+1))/(hi-lo+1)}[kind];query=f'sum component votes from {z}; root={root} tie positions{lo}..{hi}; {kind},top{k}; root read only after prediction'
        if actual is None:reason='No independent component query implemented for selected key'
    except Exception as exc:reason=f'{type(exc).__name__}: {exc}'
    match=actual is not None and math.isclose(float(actual),float(expected),rel_tol=1e-8,abs_tol=1e-12)
    checks.append({**row,'check_state':'đã đối chiếu phép tính thành phần gốc' if match else 'chưa kiểm' if actual is None else 'cần đối chiếu sai khác','original_value':expected,'recomputed_value':actual,'match':'PASS' if match else 'chua_kiem' if actual is None else 'MISMATCH','query':query,'reason':reason,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with (O/'selected-root-checks.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
(O/'runs/selected-summary.json').write_text(json.dumps({'checks':len(checks),'pass':sum(x['match']=='PASS' for x in checks),'unchecked':sum(x['match']=='chua_kiem' for x in checks),'mismatch':sum(x['match']=='MISMATCH' for x in checks),'elapsed_seconds':time.monotonic()-t0},indent=2),encoding='utf-8')
print((O/'runs/selected-summary.json').read_text())

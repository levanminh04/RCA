"""Existing timers only; projected dataset totals are explicitly unverified."""
from pathlib import Path
import csv,json,re,statistics,datetime
R=Path('D:/RCA-flashticket');O=R/'results/T-020/trung-gian/method_evidence'
rows=[]
def add(method,config,source,observed,case_count,seeds=1,scope='',projectN=90,allow_project=True):
    percase=observed/case_count/seeds if case_count else None
    rows.append(dict(method=method,config=config,source=source,observed_total_seconds=observed,observed_cases=case_count,observed_seeds=seeds,seconds_per_case=percase if percase else 'not_applicable',projection_case_count=projectN if allow_project else 'not_applicable',projection_seed1_seconds=percase*projectN if allow_project and percase else 'not_applicable',projection_seed3_seconds=percase*projectN*3 if allow_project and percase else 'not_applicable',projection_seed3_exceeds_Q40=percase*projectN*3>10800 if allow_project and percase else 'not_applicable',Q40_total_dataset_seconds=10800,state='FACT recorded timing; projection chua_kiem (same dimensions/hardware/load only)',scope=scope,official_runtime=False))
p='results/T-005/runs/ket-qua-do.jsonl'
for i,s in enumerate((R/p).read_text(encoding='utf-8').splitlines(),1):
    q=json.loads(s)
    if q.get('method_s') is not None:
        train=q['muc']=='gdn_hoc'
        inference=q['muc']=='gdn_suy_luan'
        add(q['muc'],q['bien_the']+' '+q['env']+' repeat'+str(q['lan']),p+':'+str(i)+'#method_s',q['method_s'],0 if train else 1,scope=('one model fit/system/seed; dataset total=nseeds*(train_once+sum_inference_cases); never multiply training by90 incidents' if train else 'single reference inference timer only; excludes model training/import/load; full dataset total=nseeds*(train_once+sum_inference_cases), same schema/model/hardware unverified' if inference else 'single reference case; method body timer excludes import/load; dimensions vary by variant; not dataset runtime'),allow_project=not train)
    elif '> 1 gio' in q.get('trang_thai',''):
        add(q['muc'],q['bien_the']+' timeout',p+':'+str(i)+'#tong_s',q['tong_s'],1,scope='failed timeout observation; does not estimate successful runtime',allow_project=False)
p='results/T-013/trung-gian/chi-phi-va-sentinel.json';j=json.loads((R/p).read_text())
# Match the existing single-model benchmark pair; projection retains fixed shape.
gdn_train=next(r for r in rows if r['method']=='gdn_hoc')
gdn_infer=next(r for r in rows if r['method']=='gdn_suy_luan')
gdn_pair=dict(gdn_infer)
gdn_pair.update(method='GDN train+inference',config='T005 one model/system/seed +90 same-shape inference cases',source=gdn_train['source']+' + '+gdn_infer['source'],observed_total_seconds=gdn_train['observed_total_seconds']+gdn_infer['observed_total_seconds'],seconds_per_case='not_applicable',projection_seed1_seconds=gdn_train['observed_total_seconds']+90*gdn_infer['observed_total_seconds'],projection_seed3_seconds=3*(gdn_train['observed_total_seconds']+90*gdn_infer['observed_total_seconds']),scope='UNVERIFIED conditional extrapolation: nseeds*(trainonce/system/seed+N*single_case_inference). Training2876+val719 windows, inference1436windows; same fixed333features/model/hardware/load required. New dataset dimensions/adapters/cost remain chua_kiem. Does not multiply training by incident count.')
gdn_pair['projection_seed3_exceeds_Q40']=gdn_pair['projection_seed3_seconds']>10800
rows.append(gdn_pair)
add('BOCPD','T005 w600 reference',p+'#T005_reference_1440_133_sec',j['T005_reference_1440_133_sec'],1,scope='30equalcases=12.0011h,90=36.0033h eachseed; unverified same T,d assumption')
p='results/T-013/trung-gian/cua-so-delay-summary.json';j=json.loads((R/p).read_text())
add('BARO/N-Sigma arithmetic check','R1 four windows25cases',p+'#elapsed_seconds_shared_machine',j['elapsed_seconds_shared_machine'],25,scope='independent verification all100 configurations; not BARO execution runtime',allow_project=False)
p='results/T-014/runs/followup-cost.json';j=json.loads((R/p).read_text())
add('CIRCA-PC','worker blocks only',p+'#recorded_worker_seconds',j['old_worker_wall_seconds']+sum(r['wall_seconds'] for r in j['statuses']),1,scope='one case repeated graph fits and controls; not per-case baseline runtime',allow_project=False)
add('CIRCA-PC','worker + historical queue',p+'#recorded_worker_plus_queue_seconds',j['old_worker_wall_seconds']+sum(r['wall_seconds'] for r in j['statuses'])+j['historical_queue_without_worker_seconds'],1,scope='recorded block sum13506.46s>10800; reservation900s is not measured; Q40 exception remains OPEN',allow_project=False)
add('CIRCA-PC','queue only',p+'#historical_queue_without_worker_seconds',j['historical_queue_without_worker_seconds'],1,scope='queue included actual-wait accounting; never add900reservation as measured',allow_project=False)
p='results/T-014/audit/cost-summary.json';j=json.loads((R/p).read_text())
add('CIRCA','MEM25 audit mixed configs',p+'#fse_ob.recorded_nonoverlapping_blocks',sum(r['seconds'] for r in j['fse_ob']['recorded_nonoverlapping_blocks']),25,scope='sum disjoint recorded body blocks, not isolated single method; fse-ob exact totalnull',allow_project=False)

# Original per-case timing records, saved local mirror of EC2 execution metadata.
for name,N in [('s11-rcd-ob-len20',90),('s11-tt30-rcd-len10',30),('s11-tt30-torai-goc-len10',30),('s11-tt30-torai-sua-len10',30)]:
    p=Path('D:/RCA-ext/work/T-016/ec2')/name/'seed0/meta.jsonl'
    if p.exists():
        js=[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
        assert len(js)==N and all(j['seed']==0 for j in js)
        add('RCD' if 'rcd' in name else 'TORAI',name,str(p)+'#sum(giay)',sum(j['giay'] for j in js),N,scope='original per-case method timers; complete existing seed0 run; future cost same conditions unverified')
for method in ('goc','sua'):
    p=Path('D:/RCA-ext/work/T-016')/f's10-tt-{method}-len10'
    metas=list(p.glob('seed*/meta.jsonl'))
    js=[json.loads(s) for m in metas for s in m.read_text(encoding='utf-8').splitlines()]
    if js:add('TORAI',f'TT30 laptop {method} length10',str(p)+'/seed*/meta.jsonl#sum(giay)',sum(j['giay'] for j in js),30,seeds=len(metas),scope='shared laptop, multiple seeds already run; not official')
p='results/T-017/runs/run-dev-005/summary.json';js=json.loads((R/p).read_text());
add('SimpleRCA M4','TT30 run005 including checks',p+'#sum(elapsed_seconds_concurrent_laptop)',sum(j['elapsed_seconds_concurrent_laptop'] for j in js),len(js),scope='some cases include repeat/permutation/control checks; shared machine, not isolated primary runtime')
p='results/T-018/runs/b6b7-phan-tich.json';j=json.loads((R/p).read_text())
for name,q in j['luot'].items():
    if q.get('s_hoc'):
        add('GDN',name+' train',p+'#luot.'+name+'.s_hoc',q['s_hoc'],0,scope='training model timer; needs separate inference cost per case; do not multiply learning once per incident',allow_project=False)
with (O/'runtime.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(O/'runs/runtime-detail-summary.json').write_text(json.dumps({'rows':len(rows),'no_method_run':True,'no_telemetry_read':True,'projection_is_not_measurement':True},indent=2),encoding='utf-8')
print(json.dumps({'observed_cost_rows':len(rows),'original_T016_method_timers_present':sum(r['source'].startswith('D:') and 'ec2' in r['source'] for r in rows)}))

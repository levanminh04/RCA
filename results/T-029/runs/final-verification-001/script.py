"""Kiểm cuối T-029 từ file đã lưu; không gọi detector/ranker hoặc tạo số khoa học mới."""
import ast
import hashlib
import json
import re
import subprocess
import time
from collections import Counter
from pathlib import Path
import numpy as np
from repair_reports import ROOT, OUT, LOG, log, sha

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def no_t029_state(s): return ''.join(l for l in s.splitlines(True) if not l.startswith('| T-029 |'))
def nonstate_diff(s): return [x for x in re.split(r'(?=^diff --git )',s,flags=re.M) if x and not x.startswith('diff --git a/docs/STATE.md ')]
def allowed(p): return p.startswith('results/T-029/') or p in ['tasks/T-029-p4-han-che-phat-hien/LOG.md','docs/STATE.md']
def main():
    run=OUT/'runs/final-verification-001';assert not run.exists();run.mkdir()
    start=time.perf_counter();fail=[];counts=Counter();details={}
    log('Lệnh có ghi: T014-main Python -B -X utf8 -W ignore scripts/final_verification.py; chỉ đọc SHA dev, checkpoint và bằng chứng V2-V7 thực, scope before.json; ghi run mới. Không chạy lại output khoa học. V1-V4 hoặc scope lệch => DỪNG toàn task.')
    def ck(k,ok,d=None):
        counts[k]+=1
        if not ok:fail.append({'check':k,'detail':d})
    checkpoint=read(OUT/'runs/checkpoint-after5-001/manifest.json');base=read(OUT/'runs/buoc0-001/manifest.json')
    for p,v in checkpoint['files'].items(): ck('checkpoint_file',(ROOT/p).is_file() and (ROOT/p).stat().st_size==v['bytes'] and sha(ROOT/p)==v['sha256'],p)
    p3=sorted((ROOT/'src/p3').rglob('*.py'));h=hashlib.sha256()
    for p in p3:h.update(p.read_bytes())
    src={'tong':h.hexdigest(),'tep':{p.relative_to(ROOT).as_posix():sha(p) for p in p3}}
    ck('V1_src',src==base['src_p3']==checkpoint['src_p3'])
    for p,v in base['nguon'].items():ck('V1_source',sha(ROOT/p)==v,p)
    from p3.selector import nap_allowlist,chon_ca
    allow=nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
    dev_n=sum(len(chon_ca(allow,oid,ROOT,kiem_hash=True)) for oid in allow);ck('V1_allowlist',len(allow)==30 and dev_n==89)
    if fail:
        (run/'verification.json').write_text(json.dumps({'status':'STOP','failures':fail},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');log('DỪNG toàn task: V1/checkpoint lệch; xem final-verification-001/verification.json.');return
    bd=read(ROOT/'results/T-025/bao-dong.json')['bo_phat_hien'];nm=read(OUT/'runs/nsigma-002/manifest.json');v2n=0
    for oid,c in nm['cases'].items():
        for det,q in c['bo'].items():
            p=ROOT/q['npz'];ck('V2_npz_hash',sha(p)==q['sha256'],oid+'/'+det)
            with np.load(p,allow_pickle=False) as data:
                z=data['Z'];ts=data['times'];idx=np.flatnonzero(z.any(axis=1));ref=bd[det][oid]
                ck('V2_union',[int(ts[i]) for i in idx]==ref['alarms'],oid+'/'+det)
                ck('V2_t_hat',int(ts[idx[0]])==ref['luot_rca']['t_hat'],oid+'/'+det)
                ck('V2_columns',data['columns'].tolist()==ref['detector_columns'],oid+'/'+det)
                ck('V2_grid',z.shape==(1441,len(ref['detector_columns'])) and np.array_equal(ts-ts[0],np.arange(1441)),oid+'/'+det)
            v2n+=1
    ck('V2_pairs',v2n==60)
    artifacts=OUT/'runs/ec2-complete-002/artifacts';chain=artifacts/'runs/chuoi-002'
    dims=read(chain/'v3-dimensions.json');replay=read(chain/'v3-replay.json');v3=read(chain/'v3-check.json')
    ck('V3_count',len(dims)==len({x['opaque_id'] for x in dims})==30)
    for x in dims:ck('V3_dimensions',x['d']==x['expected']==bd['bocpd'][x['opaque_id']]['input_shape']['cot_sau_tien_xu_ly'],x['opaque_id'])
    ck('V3_min_case',min(dims,key=lambda x:(x['d'],x['opaque_id']))['opaque_id']==replay['opaque_id'])
    for k in ['status','chi_so','alarms','input_shape','detector_columns']:ck('V3_replay',replay['result'][k]==bd['bocpd'][replay['opaque_id']][k],k)
    ck('V3_saved',v3['status']=='PASS')
    exp=read(artifacts/'inputs/v4-expected.json');v4=read(chain/'v4-check.json');got={}
    for p in (artifacts/v4['run']/'luot').glob('*/ban-ghi-*.json'):
        d=read(p);got[(d['method'],d['variant'],d['seed'])]=d
    ck('V4_count',len(got)==len(exp['records'])==6)
    for e in exp['records']:
        source=read(ROOT/e['source_path']);g=got[(e['method'],e['variant'],e['seed'])]
        ck('V4_source_sha',sha(ROOT/e['source_path'])==e['source_sha256'],e['source_path'])
        ck('V4_ranking',e['status']==source['status']==g['status'] and e['ranking_native']==source['ranking_native']==g['ranking_native'],e['source_path'])
    q=nm['cases'][exp['opaque_id']]['bo']['nsigma']
    with np.load(ROOT/q['npz'],allow_pickle=False) as d:ck('V4_zero_delay',int(np.flatnonzero(d['Z'][720:].any(axis=1))[0])+720==720)
    ck('V4_saved',v4['status']=='PASS')
    if fail:
        (run/'verification.json').write_text(json.dumps({'status':'STOP','failures':fail},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');log('DỪNG toàn task: V2-V4 lệch; xem final-verification-001/verification.json.');return
    v5=read(OUT/'runs/step5-001/V5.json');ck('V5_saved',v5['status']=='PASS' and v5['rows_checked']==90 and v5['comparisons']==len(v5['details'])==2700 and not v5['differences'] and all(x['equal'] for x in v5['details']))
    ck('V5_script_sha',v5['script_sha256']==sha(OUT/'scripts/verify_flags_independent.py'))
    for rel,n,field in [('runs/nsigma-002/V6-nsigma.json',3,'tests'),('runs/bocpd-features-001/V6-002.json',20,'checks'),('runs/V6-step5-002/check.json',29,'checks')]:
        d=read(OUT/rel);ck('V6_saved',d['status']=='PASS' and len(d[field])==n and all(x.get('pass',x.get('status')=='PASS') for x in d[field]),rel)
    old=OUT/'runs/resume-006-001/analyze-step5-before-timing.py';v6=read(OUT/'runs/V6-step5-002/check.json')
    ck('V6_step5_snapshot',sha(old)==v6['implementation_sha256'])
    def helpers(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text(encoding='utf-8')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
    ck('V6_helpers_unchanged',helpers(old)==helpers(OUT/'scripts/analyze_step5.py'))
    theo=read(OUT/'theo-ca.json');v7=read(OUT/'runs/step5-001/V7.json')
    for row in theo['rows']:
        if row['detector']!='bocpd':continue
        fs=row['feature_source'];f=read(ROOT/fs['path']);ck('V7_feature_sha',sha(ROOT/fs['path'])==fs['sha256'],row['opaque_id']);alarm=set(f['alarms_indices']);th=f['t_hat_index'];oid=row['opaque_id']
        for kind,w,k in [('B1',None,None)]+[('B4',w,k) for w in(15,30,60) for k in(2,3,5)]:
            lo,hi=(3,717) if kind=='B1' else (1+w+30,720-w);source=f['B1_all_Nv'] if w is None else f['B4_all_Nv'][str(w)]
            for i,x in source.items():ck('V7_domain',x['valid']==(lo<=int(i)<=hi),oid+'/'+kind+'/'+str(w)+'/'+i)
            valid=[i for i in range(lo,hi+1) if i not in alarm]
            vals=[source[str(i)]['flag'] if w is None else source[str(i)]['flags'][str(k)] for i in valid]
            at=f['B1_t_hat']['flag'] if w is None else f['B4_t_hat'][str(w)]['flags'][str(k)]
            expect={'control_n':len(vals),'control_true':sum(vals),'control_rate':sum(vals)/len(vals) if vals else None,'at_first_valid':lo<=th<=hi,'at_first':at}
            actual=v7['cases'][oid]['B1'] if w is None else v7['cases'][oid]['B4'][str(w)][str(k)]
            ck('V7_case',all(actual[x]==a for x,a in expect.items()),oid+'/'+kind+'/'+str(w)+'/'+str(k))
    for name,scopes in v7['aggregate'].items():
        for scope,groups in scopes.items():
            for group,g in groups.items():
                ids=[oid for oid,c in v7['cases'].items() if scope=='all' or c[scope]==group]
                parts=[v7['cases'][oid]['B1'] if name=='B1' else v7['cases'][oid]['B4'][name.split('/')[1][1:]][name.split('/')[2][1:]] for oid in ids]
                den=sum(x['control_n'] for x in parts);num=sum(x['control_true'] for x in parts);first=[x['at_first'] for x in parts if x['at_first_valid']];fr=sum(first)/len(first) if first else None;nr=num/den if den else None
                expect={'case_n':len(ids),'at_first_true':sum(first),'at_first_n':len(first),'at_first_rate':fr,'nonalarm_true':num,'nonalarm_n':den,'nonalarm_rate':nr,'rates_exactly_equal':fr is not None and fr==nr}
                ck('V7_aggregate',all(g[x]==a for x,a in expect.items()) and sorted(g['case_ids'])==sorted(ids),name+'/'+scope+'/'+group)
    # Scope so với baseline phiên7 và byte STATE riêng; không đổ lỗi diff có sẵn.
    b7=read(OUT/'runs/resume-step7-001/before.json');b8=read(OUT/'runs/report-repair-001/before.json')
    state=(ROOT/'docs/STATE.md').read_text(encoding='utf-8')
    ck('scope_STATE_session7',no_t029_state(state)==no_t029_state(b7['state']))
    ck('scope_STATE_bytes_session8',no_t029_state((ROOT/'docs/STATE.md').read_bytes().decode('utf-8'))==no_t029_state(bytes.fromhex(b8['state_hex']).decode('utf-8')))
    gitdiff=subprocess.check_output(['git','diff'],cwd=ROOT).decode()
    ck('scope_tracked_diff',nonstate_diff(gitdiff)==nonstate_diff(b7['git_diff']))
    paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0');current={p for p in paths if p and (ROOT/p).is_file() and not p.startswith('data/')}
    changes=[]
    for p,v in b8['files'].items():
        exists=(ROOT/p).is_file();different=not exists or (ROOT/p).stat().st_size!=v['bytes'] or sha(ROOT/p)!=v['sha256']
        if different:changes.append(p);ck('scope_changed_file',allowed(p),p)
    added=sorted(current-set(b8['files']));removed=sorted(set(b8['files'])-current)
    for p in added+removed:ck('scope_added_removed',allowed(p),p)
    ck('scope_LOG_append',LOG.read_bytes().startswith(bytes.fromhex(b8['log_hex'])))
    v8runs=sorted((OUT/'runs').glob('V8-reports-*/verification.json'));latest=v8runs[-1];v8=read(latest)
    ck('V8_final',v8['status']=='PASS' and v8['mismatch_count']==0)
    for name,x in v8['reports'].items():ck('V8_report_hash',sha(OUT/name)==x['sha256'],name)
    for p,h in v8['source_hashes'].items():ck('V8_source_hash',sha(ROOT/p)==h,p)
    result={'status':'PASS' if not fail else 'STOP','counts':dict(counts),'failures':fail,'wall_s':time.perf_counter()-start,'V1_dev_cases':len(allow),'V1_dev_files':dev_n,'src_p3':src,'checkpoint_manifest_sha256':sha(OUT/'runs/checkpoint-after5-001/manifest.json'),'V8_source':latest.relative_to(ROOT).as_posix(),'changed':sorted(changes),'added':added,'removed':removed,'script_sha256':sha(Path(__file__))}
    (run/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(run/'script.py').write_bytes(Path(__file__).read_bytes());(run/'tracked.diff').write_text(gitdiff,encoding='utf-8')
    log('Kiểm cuối '+result['status']+': '+str(len(fail))+' lệch; V1 dev '+str(dev_n)+' tệp, checkpoint '+str(len(checkpoint['files']))+'; V2 '+str(v2n)+' cặp; V3/V4 đọc bản ghi; V5-V7 đã lưu đối chiếu. Scope/diff/hash tại runs/final-verification-001/verification.json. Chưa cập nhật STATE hoặc chép prompt.')
    print(json.dumps({'status':result['status'],'counts':dict(counts),'failures':fail,'wall_s':result['wall_s']},ensure_ascii=False))
    if fail:raise SystemExit(1)
if __name__=='__main__':main()

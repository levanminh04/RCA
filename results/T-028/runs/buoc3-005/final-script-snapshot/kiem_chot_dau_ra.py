"""Final consistency/provenance/scope inspection of T-028 saved artifacts only."""
import argparse
import ast
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
ORDER=['M1','M2','M3','M4','M5','M6']

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);p.add_argument('--output',default='final-verification.json');a=p.parse_args()
    run=ROOT/'results/T-028/runs'/a.run_id;outpath=run/a.output
    if outpath.exists():raise RuntimeError('Preserve previous verification')
    checks=[]
    def check(name,passed,source,**detail):checks.append(dict(name=name,passed=bool(passed),source=source,**detail))
    pre=read('results/T-028/runs/tiep-nhan-001/manifest.json')
    for ref in pre['hash_checks']:
        pp=ROOT/ref['path'];data=pp.read_bytes()
        if ref['path']=='results/T-028/chi-phi.md':
            data=data[:ref['bytes']]
        check('unchanged_preflight_source',sha(data)==ref['sha256'],ref['path'])
    log=(ROOT/'tasks/T-028-p4-han-che-xep-hang/LOG.md').read_bytes()
    check('LOG_previous_prefix_unchanged',sha(log[:pre['old_LOG']['bytes']])==pre['old_LOG']['sha256'],'tasks/T-028-p4-han-che-xep-hang/LOG.md')
    state=(ROOT/'docs/STATE.md').read_bytes();lines=state.splitlines(keepends=True)
    current=[l for l in lines if l.startswith(b'| T-028 |')]
    check('single_T028_STATE_row',len(current)==1,'docs/STATE.md')
    reconstructed=b''.join(pre['old_STATE']['row_T028'].encode('utf-8') if l.startswith(b'| T-028 |') else l for l in lines)
    check('STATE_only_T028_changed',sha(reconstructed)==pre['old_STATE']['sha256'],'docs/STATE.md')
    d=read(str((run/'ca-sai.json').relative_to(ROOT)));step1=read('results/T-028/runs/danh-sach-001/step1.json')
    rows=d['main_rows'];old={(r['dataset'],r['method'],r['opaque_id']):r for r in step1['main_rows']}
    check('main_row_coverage',len(rows)==len(old)==312,str(run/'ca-sai.json'))
    check('main_methods_and_cohorts',Counter((r['dataset'],r['method']) for r in rows)==Counter((r['dataset'],r['method']) for r in step1['main_rows']),str(run/'ca-sai.json'))
    seeds=sum(len(r['evidence']['seed_evidence']) for r in rows)
    check('saved_seed_record_count',seeds==372,str(run/'ca-sai.json'),actual=seeds)
    for r in rows:
        prev=old[(r['dataset'],r['method'],r['opaque_id'])]
        unchanged={k:v for k,v in prev.items() if k not in ('evidence','mechanisms','analysis_state')}
        check('saved_step1_fields',all(r[k]==v for k,v in unchanged.items()),r['source'])
        for k in ('1','5'):
            ass=r['mechanisms'][k]['assignment'];f=r['mechanisms'][k]['explanation_flags_wrong_seeds']
            want=[m for m in ORDER if f[m]['value'] is True]
            if r['wrong_OK_at_'+k]:
                check('wrong_has_fixed_primary_multi',ass['multi']==(want or ['M0']) and ass['primary']==(want[0] if want else 'M0'),r['source'])
            else:check('non_wrong_has_no_assignment',ass['multi']==[] and ass['primary'] is None,r['source'])
        for sid,s in r['evidence']['seed_evidence'].items():
            for k,v in s['by_k'].items():
                if r['method'] in ('baro','torai_B'):check('BARO_TORAI_M6_NA',v['flags']['M6']['value'] is None,s['source'])
                if r['method']=='tracerca' and v['flags']['M6']['value'] is True:check('Trace_M6_implies_M2',v['flags']['M2']['value'] is True,s['source'])
                if v['P0']['availability']=='available':
                    check('P0_same_eligible_base_M5',v['wrong_OK'] and s['status']=='OK' and r['root'] in s['ranking']['R'] and v['flags']['M5']['value'] is not None,s['source'])
                    check('P0_parameter_bounds',0<=v['P0']['a']<=v['P0']['n']-1 and 0<=v['P0']['b']<=v['P0']['n']-1 and 0<=v['P0']['value']<=1,s['source'])
    for r in d['circa_dev19_conditional']['rows']:
        parent=next(x for x in rows if x['dataset']==r['dataset'] and x['method']==r['method'] and x['opaque_id']==r['opaque_id'])
        # graph_role is a presentation annotation added after copying dev30.
        ev={k:v for k,v in parent['evidence'].items() if k!='graph_role'}
        check('CIRCA_dev19_reuses_all_computed_evidence',r['evidence']==ev and r['mechanisms']==parent['mechanisms'],r['source'])
    check('CIRCA_original_cohort_exclusion',len(d['circa_dev19_conditional']['rows'])==19 and d['circa_dev19_conditional']['excluded_confirmed_rounding11']==step1['circa_dev19_conditional']['excluded_confirmed_rounding11'],str(run/'ca-sai.json'))
    check('Nezha_sensitivity_saved_flags_only',d['nezha_saved_sensitivity_flags']==step1['nezha_saved_sensitivity_flags'] and all(f.get('evidence_computed') is False and f.get('mechanisms') is None and 'evidence' not in f for f in d['nezha_saved_sensitivity_flags']),str(run/'ca-sai.json'))
    idx=read(str((run/'features-no-label-index.json').relative_to(ROOT)))
    feature_files=[]
    for ds,ca in idx['cases'].items():
        for oid,ref in ca.items():
            feature_files.append(ROOT/ref['path']);b=(ROOT/ref['path']).read_bytes()
            check('feature_hash_reuse',sha(b)==ref['sha256'],ref['path'])
            feature=json.loads(b);check('label_free_aggregate',feature['aggregate']['label_free'] and 'root' not in feature['aggregate'] and 'fault' not in feature['aggregate'],ref['path'])
    progress=[json.loads(l) for l in (ROOT/'results/T-028/runs/buoc3-002/progress.jsonl').read_text(encoding='utf-8').splitlines()]
    barrier=next(i for i,v in enumerate(progress) if v['stage']=='all_features_serialized_before_labels')
    label=next(i for i,v in enumerate(progress) if v['stage']=='labels_joined_for_analysis_only')
    check('all_52_features_before_label_barrier',sum(v['stage']=='case_features_no_label_written' for v in progress[:barrier])==52 and label>barrier,'results/T-028/runs/buoc3-002/progress.jsonl')
    selected=read(str((run/'manual-selection.json').relative_to(ROOT)))
    manual=read(str((run/'manual-reading.json').relative_to(ROOT)))
    mc=manual['cases']
    identity=lambda rr:sorted((r['dataset'],r['method'],r['opaque_id']) for r in rr)
    check('manual_coverage_matches_selection',identity(mc)==identity(selected),str(run/'manual-reading.json'))
    check('manual_all_criteria_matched',all(r['criterion_match'] is True and r.get('reading_note') and r.get('sources') for r in mc),str(run/'manual-reading.json'))
    for f in ('independent-ranking.json','independent-statistics.json','aggregation-review.json','report-review.json','provenance-checks.json','manual-packaging-check.json','toy-D-checks.json'):
        val=read(str((run/f).relative_to(ROOT)));check('verification_artifact_passed',val['status']=='passed',str(run/f))
    for name in ('ca-sai.json','ca-sai.csv'):
        check('top_level_output_matches_run',(ROOT/'results/T-028'/name).read_bytes()==(run/name).read_bytes(),'results/T-028/'+name)
    csvrows=list(csv.DictReader((run/'ca-sai.csv').open(encoding='utf-8',newline='')))
    check('CSV_312_only_permitted_fields',len(csvrows)==312 and all(set(r)=={'opaque_id','dataset_index','method_index','hit1','hit5','rank_min','rank_max','primary1','primary5','multi1','multi5'} for r in csvrows),str(run/'ca-sai.csv'))
    # Inspect aggregate/analysis JSON keys for prohibited raw payload structures.
    forbidden={'timestamps_ns','spanID','traceID','parentSpanID','message','metric_arrays','spans','logs','edges','adjacency','payload','normal','anomalous'}
    leaks=[]
    def walk(v,loc):
        if isinstance(v,dict):
            for k,w in v.items():
                count_only=k in {'spans','logs','edges'} and (w is None or isinstance(w,int) and not isinstance(w,bool))
                if k in forbidden and not count_only:leaks.append(loc+'/'+k)
                walk(w,loc+'/'+k)
        elif isinstance(v,list):
            for i,w in enumerate(v):walk(w,loc+'/'+str(i))
    for pp in feature_files:
        feature=json.loads(pp.read_text(encoding='utf-8'))
        if feature['dataset']=='Nezha-OB':walk(feature,str(pp.relative_to(ROOT)))
    for r in rows:
        if r['dataset']=='Nezha-OB':walk(r['evidence'],'Nezha/'+r['opaque_id']+'/'+r['method'])
    check('Nezha_no_raw_payload_keys',not leaks,str(run/'ca-sai.json'),leaks=leaks)
    check('no_payload_work_files',not (ROOT/'results/T-028/work').exists() or not any((ROOT/'results/T-028/work').iterdir()),'results/T-028/work/')
    pyfiles=list((ROOT/'results/T-028/scripts').glob('*.py'))
    for pp in pyfiles:ast.parse(pp.read_text(encoding='utf-8'))
    check('all_scripts_AST',True,'results/T-028/scripts/',n=len(pyfiles))
    modified_after=datetime.fromisoformat(pre['started_at_asia_saigon']).timestamp()
    recent_pyc=[str(p.relative_to(ROOT)) for base in (ROOT/'src',ROOT/'results/T-028') for p in base.rglob('*.pyc') if p.stat().st_mtime>=modified_after]
    check('no_bytecode_written',not recent_pyc,'src/; results/T-028/',paths=recent_pyc)
    current_files=[]
    for pp in (ROOT/'results/T-028').rglob('*'):
        if pp.is_file():
            b=pp.read_bytes();current_files.append({'path':str(pp.relative_to(ROOT)).replace('\\','/'),'bytes':len(b),'sha256':sha(b)})
            if pp.suffix=='.json':json.loads(b)
            if pp.suffix=='.jsonl':
                for line in b.decode('utf-8').splitlines():json.loads(line)
    check('all_result_JSON_JSONL_parse',True,'results/T-028/',n=sum(p['path'].endswith(('.json','.jsonl')) for p in current_files))
    report={'status':'passed' if all(c['passed'] for c in checks) else 'failed','checked_at':datetime.now().astimezone().isoformat(),'checks_n':len(checks),'n_failed':sum(not c['passed'] for c in checks),'checks':checks,'result_file_snapshot':current_files,'note':'No ranking method/test execution; CLI diff inspected separately. Existing user changes preserved. Files within result scope; LOG append/STATE row checks above.'}
    outpath.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(report['status'],report['checks_n'],'failures',report['n_failed'])
    if report['status']!='passed':raise SystemExit(1)

if __name__=='__main__':main()

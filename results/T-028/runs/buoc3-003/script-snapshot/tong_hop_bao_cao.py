"""Tables/report material from fixed-codebook T-028 evidence, without raw I/O."""
import argparse
import csv
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
MS=['M1','M2','M3','M4','M5','M6','M0']
FIELDS=['cell','fault','nhom_loi','nhom_vi_tri_p75','root']


def readj(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def writej(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def src(path,pointer=''):return {'path':path,'json_pointer':pointer}


def summary(rows,k):
    wrong=[r for r in rows if r[f'wrong_OK_at_{k}']]
    correct=[r for r in rows if r['status']=='OK' and r[f'hit@{k}']==1]
    counts=Counter(r['status'] for r in rows)
    primary=Counter(r['mechanisms'][str(k)]['assignment']['primary'] for r in wrong)
    multi=Counter(m for r in wrong for m in r['mechanisms'][str(k)]['assignment']['multi'])
    base={}
    for name,rr in [('correct_OK',correct),('wrong_OK',wrong)]:
        base[name]={}
        for m in MS[:-1]:
            ff=[r['mechanisms'][str(k)]['base_flags_all_OK_seeds'][m]['value'] for r in rr]
            base[name][m]={'True':sum(v is True for v in ff),'False':sum(v is False for v in ff),'N/A':sum(v is None for v in ff),'n_eligible':sum(v is not None for v in ff),'n_group':len(rr)}
    return {'n_cohort':len(rows),'status_counts':dict(counts),'n_correct_OK':len(correct),'n_wrong_OK':len(wrong),'n_non_OK':len(rows)-counts['OK'],
            'expected_misses_including_non_OK':math.fsum(1-r[f'hit@{k}'] for r in rows),
            'primary':{m:primary[m] for m in MS},'multi':{m:multi[m] for m in MS},'base_flags':base,
            'correct_wrong_comparison':'available' if wrong and correct else 'N/A_empty_group',
            'structural_relations':'M1/M2 imply wrong; M3 excludes Hit=1; M5 cannot be True at correct top1; Simple M6 implies wrong top1; Trace M6 implies M2; M4 cohort does not establish cause'}


def p0_tables(rows):
    groups=defaultdict(list)
    for r in rows:
        for sid,seed in r['evidence']['seed_evidence'].items():
            for k in (1,5):
                for field,group in [('overall','all')]+[(field,r[field]) for field in FIELDS]:
                    groups[(r['dataset'],r['method'],k,sid,field,group)].append(seed['by_k'][str(k)])
    out=[]
    for (ds,method,k,sid,field,group),rr in sorted(groups.items()):
        eligible=[x for x in rr if x['P0']['availability']=='available']
        assert all(x['flags']['M5']['value'] is not None for x in eligible)
        out.append({'dataset':ds,'method':method,'k':k,'seed':sid,'group_field':field,'group':group,
                    'n_records_total':len(rr),'n_OK_wrong_records':sum(x['wrong_OK'] for x in rr),'n_eligible':len(eligible),
                    'n_NA':len(rr)-len(eligible),'NA_reasons':dict(Counter(x['P0']['reason'] for x in rr if x['P0']['availability']!='available')),
                    'n_base_M5_True_on_eligible':sum(x['flags']['M5']['value'] is True for x in eligible),
                    'sum_P0':math.fsum(x['P0']['value'] for x in eligible) if eligible else None,
                    'difference':sum(x['flags']['M5']['value'] is True for x in eligible)-math.fsum(x['P0']['value'] for x in eligible) if eligible else None,
                    'interpretation':'descriptive conditional null; no p-value, no significance cutoff, no propagation label; TORAI seeds separate'})
    return out


def proxy_tables(rows):
    groups=defaultdict(list)
    for r in rows:
        for k in (1,5):
            group='wrong_OK' if r[f'wrong_OK_at_{k}'] else 'correct_OK' if r['status']=='OK' else 'non_OK'
            split='start' if r['method']=='simplerca' else 'end'
            rr=r['evidence']['root_trace_start_Simple_convention' if split=='start' else 'root_trace_end_context']
            for tau in (2,3,4):
                ff=rr.get('latency_up',{}).get(str(tau),{'value':None,'reason':'unsupported' if r['status']=='UNSUPPORTED' else 'missing_channel'})
                for field,gg in [('overall','all')]+[(field,r[field]) for field in FIELDS]:groups[(r['dataset'],r['method'],k,group,tau,split,field,gg)].append((r['opaque_id'],ff))
    out=[]
    for key,rr in sorted(groups.items()):
        ds,method,k,group,tau,split,field,gg=key
        out.append(dict(dataset=ds,method=method,k=k,ranking_group=group,tau=tau,split=split,group_field=field,group=gg,
                        n_True=sum(f['value'] is True for oid,f in rr),n_False=sum(f['value'] is False for oid,f in rr),n_NA=sum(f['value'] is None for oid,f in rr),
                        n_eligible=sum(f['value'] is not None for oid,f in rr),n_cohort=len(rr),true_cases=[oid for oid,f in rr if f['value'] is True],
                        NA_reasons=dict(Counter(f.get('reason') for oid,f in rr if f['value'] is None))))
    return out


def schema_tables(rows):
    audit=readj('results/T-024/cham-a.json')['raw_column_audit']
    labels={r['opaque_id']:r for r in rows if r['dataset']=='RE2-TT' and r['method']=='baro'}
    allowed={'cpu','mem','diskio','socket','workload','error','latency-50','latency-90'}
    union=audit['union_columns'];out=[];groups=defaultdict(list)
    for oid,raw in audit['by_case'].items():
        present=set(raw['columns']);missing=[c for c in union if c not in present]
        typecounts=Counter(c.rsplit('_',1)[-1] if c.rsplit('_',1)[-1] in allowed else 'time' if c in ('time','time.1') else 'other' for c in missing)
        r=labels[oid]
        out.append({'opaque_id':oid,'cell':r['cell'],'root':r['root'],'fault':r['fault'],'union_n':len(union),'n_present':len(present),'n_absent':len(missing),
                    'missing_columns':missing,'missing_by_type':dict(typecounts),'source':src('results/T-024/cham-a.json','/raw_column_audit/by_case/'+oid)})
        groups[r['cell']].append((oid,present))
    cell=[]
    for cellname,rr in sorted(groups.items()):
        for c in union:
            cell.append({'cell':cellname,'column':c,'native_service':c.rsplit('_',1)[0] if '_' in c else c,'entity':c.split('_')[0],
                         'type':c.rsplit('_',1)[-1] if c.rsplit('_',1)[-1] in allowed else 'time' if c in ('time','time.1') else 'other',
                         'n_present':sum(c in pp for oid,pp in rr),'n_absent':sum(c not in pp for oid,pp in rr),'n_cases':len(rr)})
    cross=[]
    for root in sorted({r['root'] for r in out}):
        ids={r['opaque_id'] for r in out if r['root']==root}
        for c in union:
            rr=[audit['by_case'][oid] for oid in ids]
            cross.append({'root':root,'column':c,'column_entity':c.split('_')[0],'n_present':sum(c in x['columns'] for x in rr),'n_absent':sum(c not in x['columns'] for x in rr),'n_cases':len(rr)})
    coverage=[]
    for r in rows:
        if r['dataset']!='RE2-TT':continue
        for sid,s in r['evidence']['seed_evidence'].items():
            coverage.append({'opaque_id':r['opaque_id'],'method':r['method'],'seed':sid,'cell':r['cell'],'status':r['status'],
                             'O':s['ranking']['O'],'R':s['ranking']['R'],'nO':s['ranking']['n'],'nR':s['ranking']['L'],'input_shape':s['native_input_shape'],
                             'source':s['source']})
    return {'source':src('results/T-024/cham-a.json','/raw_column_audit'),'union_n':len(union),'by_case':out,'by_cell_column':cell,'by_root_column':cross,'native_coverage':coverage,
            'interpretation':'descriptive dev cross-table; raw schema is not common native input; no schema effect separated from root/fault'}


def manual_selection(rows):
    groups=defaultdict(list)
    for r in rows:
        for k in (1,5):
            for m in r['mechanisms'][str(k)]['assignment']['multi']:
                groups[(r['dataset'],r['method'],k,m)].append(r)
    selected=defaultdict(list)
    for key,rr in sorted(groups.items()):
        n=10 if key[-1]=='M0' and len(rr)>10 else len(rr) if key[-1]=='M0' else min(2,len(rr))
        for r in sorted(rr,key=lambda r:r['opaque_id'])[:n]:selected[(r['dataset'],r['method'],r['opaque_id'])].append({'k':key[2],'mechanism':key[3],'group_size':len(rr),'n_required':n})
    return [{'dataset':ds,'method':method,'opaque_id':oid,'requirements':req,'row':next(r for r in rows if (r['dataset'],r['method'],r['opaque_id'])==(ds,method,oid))} for (ds,method,oid),req in sorted(selected.items())]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-id',required=True);a=parser.parse_args()
    run=ROOT/'results/T-028/runs'/a.run_id
    if (run/'summary-tables.json').exists():raise RuntimeError('Summary attempt exists; preserve it before a new attempt')
    doc=readj(str((run/'ca-sai.json').relative_to(ROOT)))
    rows=doc['main_rows'];groups=defaultdict(list)
    provenance_checks=[]
    for r in rows:
        feature=readj(r['evidence']['source']['path'])['aggregate']
        r['evidence']['graph_role']='analysis_context_not_input_to_BARO_TORAI' if r['method'] in ('baro','torai_B') else 'analysis_graph_not_claimed_native_method_graph'
        if r['method']=='baro':
            root=r['root']
            for field in ('trace_start','trace_end','logs_A','simple_native_services'):
                r['evidence']['root_all_native_'+field]={name:v for name,v in feature[field].items() if v['entity']==root}
        for ref in r['source']['records']:
            rec=readj(ref['path'])
            if rec['status']=='UNSUPPORTED':continue
            expected={name:meta.get('sha256') for name,meta in feature['provenance']['sources'].items()}
            if r['dataset']=='Nezha-OB':
                assert rec['input_sha256']==expected,(ref['path'],'input hash mismatch')
                assert rec['window']==feature['window'],(ref['path'],'window mismatch')
            else:
                assert all(rec['input_sha256'].get(name)==v for name,v in expected.items()),(ref['path'],'input hash mismatch')
                assert rec['window']['t']==feature['window']['t']
            provenance_checks.append({'record':ref['path'],'feature':r['evidence']['source']['path'],'status':'passed'})
    writej(run/'provenance-checks.json',{'status':'passed','checks':provenance_checks,'unsupported':'N/A; method did not receive payload'})
    # Attach all BARO native service descriptions without changing any flags.
    (run/'ca-sai-before-native-root-table.json').write_bytes((run/'ca-sai.json').read_bytes())
    writej(run/'ca-sai.json',doc)
    for r in rows:
        for k in (1,5):
            for field,gg in [('overall','all')]+[(field,r[field]) for field in FIELDS]:groups[(r['dataset'],r['method'],k,field,gg)].append(r)
    summaries=[dict(dataset=ds,method=method,k=k,group_field=field,group=gg,**summary(rr,k)) for (ds,method,k,field,gg),rr in sorted(groups.items())]
    writej(run/'summary-tables.json',{'mechanism_tables':summaries,'P0_tables':p0_tables(rows),'proxy_tables':proxy_tables(rows)})
    writej(run/'schema-tables.json',schema_tables(rows))
    writej(run/'manual-selection.json',manual_selection(rows))
    writej(run/'BARO-root-data.json',[{key:r[key] for key in ('dataset','opaque_id','root','fault','cell','status','hit@1','hit@5','rank_min','rank_max','source','evidence')} for r in rows if r['method']=='baro'])
    with (run/'ca-sai.csv').open('w',encoding='utf-8',newline='') as f:
        # Only opaque IDs, numeric measurements and mechanism labels, per SPEC.
        writer=csv.DictWriter(f,fieldnames=['opaque_id','dataset_index','method_index','hit1','hit5','rank_min','rank_max','primary1','primary5','multi1','multi5']);writer.writeheader()
        methods=sorted({r['method'] for r in rows});datasets=['RE2-TT','Nezha-OB']
        for r in rows:writer.writerow(dict(opaque_id=r['opaque_id'],dataset_index=datasets.index(r['dataset']),method_index=methods.index(r['method']),hit1=r['hit@1'],hit5=r['hit@5'],rank_min=r['rank_min'],rank_max=r['rank_max'],primary1=r['mechanisms']['1']['assignment']['primary'],primary5=r['mechanisms']['5']['assignment']['primary'],multi1='|'.join(r['mechanisms']['1']['assignment']['multi']),multi5='|'.join(r['mechanisms']['5']['assignment']['multi'])))
    writej(run/'csv-index-map.json',{'dataset_index':dict(enumerate(datasets)),'method_index':dict(enumerate(methods)),'status_source':'ca-sai.json; CSV contains only opaque ids, numbers and mechanism labels'})
    print('summary tables/schema/BARO root/manual selection/CSV written from saved evidence')


if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()

"""Tables/report material from fixed-codebook T-028 evidence, without raw I/O."""
import argparse
import copy
import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone
import shutil
import time

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


def caller_root_proxy(rows, case_path):
    """Report saved service statistics; never recalculate or merge percentiles."""
    cache, output = {}, []
    escape = lambda s: s.replace('~', '~0').replace('/', '~1')
    for index, r in enumerate(rows):
        path = r['evidence']['source']['path']
        if path not in cache:
            cache[path] = readj(path)['aggregate']
        split = r['evidence']['native_trace_split']
        traces = cache[path]['trace_' + split]
        for sid, s in r['evidence']['seed_evidence'].items():
            before = s['certain_before_root']
            entities = [r['root']] + sorted(set(s['ancestors']['value'] or []))
            observations = []
            for entity in entities:
                role = 'root' if entity == r['root'] else 'caller'
                native = [(name, v) for name, v in traces.items() if v['entity'] == entity]
                if not native:
                    native = [(None, {'nN': None, 'nA': None, 'availability': 'N/A', 'reason': 'missing_channel',
                                      'P95N': {'value': None, 'reason': 'missing_channel'},
                                      'P95A': {'value': None, 'reason': 'missing_channel'},
                                      'latency_up': {str(t): {'value': None, 'reason': 'missing_channel'} for t in (2,3,4)}})]
                for name, v in sorted(native, key=lambda item: item[0] or ''):
                    relation = s['caller_relation'].get(entity, {})
                    observations.append({'role': role, 'entity': entity, 'native_service': name,
                        'nN': v['nN'], 'nA': v['nA'], 'P95N': copy.deepcopy(v['P95N']), 'P95A': copy.deepcopy(v['P95A']),
                        'latency_up': copy.deepcopy(v['latency_up']), 'availability': v['availability'], 'reason': v['reason'],
                        'direct_to_root': relation.get('direct_to_root'), 'shortest_distance': relation.get('shortest_distance'),
                        'certain_before_root': entity in before if role == 'caller' and before is not None else None,
                        'before_reason': 'root_role' if role == 'root' else None if before is not None else 'root_not_returned_or_invalid_ranking',
                        'source': src(path, '/aggregate/trace_' + split + ('/' + escape(name) if name else ''))})
            output.append({'dataset': r['dataset'], 'method': r['method'], 'opaque_id': r['opaque_id'], 'seed': sid,
                'status': s['status'], 'root': r['root'], 'split': split,
                'wrong_OK_by_k': {k: s['by_k'][k]['wrong_OK'] for k in ('1','5')},
                'M5_base_by_k': {k: copy.deepcopy(s['by_k'][k]['flags']['M5']) for k in ('1','5')},
                'caller_availability': s['ancestors']['availability'], 'caller_reason': s['ancestors']['reason'],
                'n_ancestors': len(s['ancestors']['value']) if s['ancestors']['value'] is not None else None,
                'observations': observations,
                'case_source': src(case_path, f'/main_rows/{index}/evidence/seed_evidence/{sid}')})
    return {'scope': 'all saved cases/seeds, root and every proper ancestor; non-OK is context only',
            'thresholds_reused': [2,3,4], 'new_signal_computation': False,
            'interpretation': 'span P95 context; not propagation labels, not BARO/TORAI native evidence', 'records': output}


def structure_description(rows, case_path):
    cache, graphs = {}, {}
    for r in rows:
        key = (r['dataset'], r['opaque_id'])
        path = r['evidence']['source']['path']
        if key not in cache:
            cache[key] = readj(path)['aggregate']
            g = cache[key]['graph_end']
            graphs[key] = {'dataset': r['dataset'], 'opaque_id': r['opaque_id'],
                'nodes': g['nodes'], 'effective_edges': g['effective_edges'],
                'unique_effective_spans_N': g['unique_effective_spans_N'], 'services': g['services'],
                'source': src(path, '/aggregate/graph_end')}
    m0 = [r for r in rows if r['mechanisms']['1']['assignment']['primary'] == 'M0']
    noanc = [r for r in m0 if all(s['ancestors']['value'] == [] for s in r['evidence']['seed_evidence'].values())]
    re2 = [g for (ds, _), g in graphs.items() if ds == 'RE2-TT']
    re2_groups = []
    for edges in sorted({g['effective_edges'] for g in re2}):
        gg = [g for g in re2 if g['effective_edges'] == edges]
        re2_groups.append({'edges': edges, 'n_cases': len(gg),
            'min_spans_N': min(g['unique_effective_spans_N'] for g in gg),
            'max_spans_N': max(g['unique_effective_spans_N'] for g in gg), 'cases': [g['opaque_id'] for g in gg]})
    groups = defaultdict(list)
    nezha = defaultdict(list)
    for i, r in enumerate(rows):
        for sid, s in r['evidence']['seed_evidence'].items():
            pointer = src(case_path, f'/main_rows/{i}/evidence/seed_evidence/{sid}')
            if r['dataset'] == 'RE2-TT' and r['method'] == 'microrank_full':
                p = s['by_k']['1']['P0']
                if p['availability'] == 'available':
                    group = 'auth' if r['root'] == 'ts-auth-service' else str(graphs[(r['dataset'],r['opaque_id'])]['effective_edges']) + '_excluding_auth'
                    groups[group].append({'opaque_id': r['opaque_id'], 'P0': p['value'],
                        'M5': s['by_k']['1']['flags']['M5']['value'], 'source': pointer})
            if r['dataset'] == 'Nezha-OB' and s['status'] == 'OK':
                nezha[r['method']].append({'opaque_id': r['opaque_id'], 'root': r['root'],
                    'ancestors': s['ancestors']['value'], 'before': s['certain_before_root'],
                    'M5': {k: s['by_k'][k]['flags']['M5']['value'] for k in ('1','5')},
                    'wrong': {k: s['by_k'][k]['wrong_OK'] for k in ('1','5')}, 'source': pointer})
    ngraphs = [g for (ds,_),g in graphs.items() if ds == 'Nezha-OB']
    signature = lambda g: json.dumps({k:g[k] for k in ('nodes','effective_edges','services')},sort_keys=True)
    return {'case_source': case_path, 'M0_top1': {'n': len(m0), 'n_no_ancestor': len(noanc),
                'no_ancestor_cases': [dict(dataset=r['dataset'],method=r['method'],opaque_id=r['opaque_id']) for r in noanc]},
            'RE2_graph_groups': re2_groups, 'graph_cases': list(graphs.values()),
            'MicroRank_RE2_top1': {k: {'n':len(v),'M5':sum(x['M5'] is True for x in v),
                'sum_P0':math.fsum(x['P0'] for x in v),'records':v} for k,v in groups.items()},
            'Nezha_degree_summaries': {'n_cases':len(ngraphs),'n_distinct':len({signature(g) for g in ngraphs}),
                'interpretation':'equal saved node/edge counts and service degrees; not proof of identical adjacency'},
            'Nezha_OK_records': dict(nezha), 'interpretation':'description only; no new mechanism or causal attribution'}


def review_from_saved(run, previous):
    """Approved R1-R5 repair from saved statistics and seed flags only."""
    from thuc_hien_buoc3_6 import merge_flags, ORDER
    started = time.perf_counter()
    rp, oldrp = str(run.relative_to(ROOT)).replace('\\','/'), str(previous.relative_to(ROOT)).replace('\\','/')
    manifest = readj(rp + '/manifest.json')
    if manifest['status'] != 'approved_preparing' or (run/'ca-sai.json').exists():
        raise RuntimeError('Preserve existing review attempt')
    at = lambda: datetime.now(timezone(timedelta(hours=7))).isoformat()
    def progress(stage):
        with (run/'progress.jsonl').open('a',encoding='utf-8') as f:
            f.write(json.dumps({'stage':stage,'at':at(),'elapsed_s':time.perf_counter()-started})+'\n')
    manifest.update(status='repairing_saved_metadata',repair_started_at=at())
    writej(run/'manifest.json',manifest)
    try:
        doc = readj(oldrp + '/ca-sai.json')
        changed = []
        for i,r in enumerate(doc['main_rows']):
            for k in ('1','5'):
                for field, eligible in (('base_flags_all_OK_seeds', [s for s in r['evidence']['seed_evidence'].values() if s['status']=='OK']),
                                        ('explanation_flags_wrong_seeds', [s for s in r['evidence']['seed_evidence'].values() if s['by_k'][k]['wrong_OK']])):
                    if not eligible:
                        continue
                    for m in ORDER:
                        old = r['mechanisms'][k][field][m]
                        new = merge_flags([s['by_k'][k]['flags'][m] for s in eligible])
                        assert all(new[key] == old[key] for key in ('value','availability','n_seed_true','n_seed_eligible','n_seed_NA','extent'))
                        if old != new:
                            changed.append({'pointer':f'/main_rows/{i}/mechanisms/{k}/{field}/{m}','old':old,'new':new})
                            r['mechanisms'][k][field][m] = new
        identity = lambda r: (r['dataset'],r['method'],r['opaque_id'])
        lookup = {identity(r):r for r in doc['main_rows']}
        for r in doc['circa_dev19_conditional']['rows']:
            r['mechanisms'] = copy.deepcopy(lookup[identity(r)]['mechanisms'])
        doc['run'] = rp
        doc['review_metadata_repaired_from'] = oldrp + '/ca-sai.json'
        writej(run/'ca-sai.json',doc)
        writej(run/'metadata-changes.json',changed)
        progress('case_NA_reasons_repaired_without_changing_flags')
        reused = ('summary-tables.json','concentration.json','schema-tables.json','BARO-root-data.json',
                  'features-no-label-index.json','csv-index-map.json','ca-sai.csv','manual-nezha.json')
        for name in reused:
            shutil.copyfile(previous/name,run/name)
        for name in ('manual-selection.json','manual-excerpts.json','manual-re2.json','manual-reading.json'):
            obj = readj(oldrp + '/' + name)
            cases = obj if isinstance(obj,list) else obj['cases']
            for c in cases:
                row = lookup[identity(c)]
                if 'row' in c:
                    c['row'] = copy.deepcopy(row)
                elif 'mechanisms' in c:
                    c['mechanisms'] = copy.deepcopy(row['mechanisms'])
                elif 'mechanisms' in c.get('observed_values',{}):
                    c['observed_values']['mechanisms'] = copy.deepcopy(row['mechanisms'])
            if isinstance(obj,dict):
                obj['review_metadata_source'] = rp + '/ca-sai.json'
                obj['original_reading_source'] = oldrp + '/' + name
            writej(run/name,obj)
        writej(run/'caller-root-proxy.json',caller_root_proxy(doc['main_rows'],rp+'/ca-sai.json'))
        writej(run/'structure-description.json',structure_description(doc['main_rows'],rp+'/ca-sai.json'))
        progress('all_saved_root_caller_proxy_and_structure_descriptions_exported')
        manifest.update(status='saved_metadata_and_report_inputs_ready',repair_elapsed_s=time.perf_counter()-started,
            repaired_case_flag_count=len(changed),measurement_source=oldrp,
            reused_files=[{'path':oldrp+'/'+name,'new_path':rp+'/'+name,'sha256':hashlib.sha256((previous/name).read_bytes()).hexdigest()} for name in reused],
            output_sources_note='Old measurements/checks retained; only case-level reasons and report material revised.')
    except BaseException as exc:
        manifest.update(status='failed',error=repr(exc),failed_at=at(),repair_elapsed_s=time.perf_counter()-started)
        raise
    finally:
        writej(run/'manifest.json',manifest)
    print('Review metadata and report inputs ready:',len(changed),'reason fields repaired')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-id',required=True);parser.add_argument('--review-from');a=parser.parse_args()
    run=ROOT/'results/T-028/runs'/a.run_id
    if a.review_from:
        review_from_saved(run,ROOT/'results/T-028/runs'/a.review_from)
        return
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
            saved=readj(r['evidence']['source']['path'])['saved_methods']['baro']['single']['native_saved']
            r['evidence']['BARO_signed_root_metric_keys']=[v for v in saved.get('items',[]) if v['entity']==root]
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

"""T-028 analysis only. No ranking methods are imported or rerun.

All service aggregates are serialized before opening the labels/step1 file.
Nezha payload and normal graphs live only in RAM. Every run is preserved.
"""
import argparse
import copy
import csv
import hashlib
import itertools
import json
import math
import os
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True
KS = (1, 5)
ORDER = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']
METHODS = ['baro', 'simplerca', 'microrank_full', 'tracerca', 'circa_ols_da', 'torai_B']
FIXED_TZ = timezone(timedelta(hours=7))


def now():
    return datetime.now(FIXED_TZ).isoformat(timespec='milliseconds')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def readj(path):
    with (ROOT / path).open(encoding='utf-8') as f:
        return json.load(f)


def writej(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def val(value, reason=None):
    return {'value': value, 'availability': 'available' if value is not None else 'N/A', 'reason': reason}


def source(path, pointer=''):
    return {'path': str(path), 'json_pointer': pointer}


def main_refs():
    re2 = readj('results/T-024/ban-ghi-dua-vao-cham.json')['records']
    nez = readj('results/T-026/ban-ghi-dua-vao-cham.json')['tables']['main']['records']
    variants = {('baro', 'native'): 'baro', ('simplerca', 'native'): 'simplerca',
                ('microrank', 'full'): 'microrank_full', ('tracerca', 'native'): 'tracerca',
                ('circa', 'ols+rht_da'): 'circa_ols_da', ('torai', 'B'): 'torai_B'}
    out = defaultdict(list)
    for ds, refs in [('RE2-TT', re2), ('Nezha-OB', nez)]:
        for ref in refs:
            method = variants.get((ref['method'], ref['variant'])) if ds == 'RE2-TT' else ref['method']
            if ds == 'Nezha-OB':
                method = {'microrank': 'microrank_full', 'circa': 'circa_ols_da', 'torai': 'torai_B'}.get(method, method)
            if method not in METHODS:
                continue
            assert not ref['path'].startswith('data/')
            assert sha(ROOT / ref['path']) == ref['sha256'], ref['path']
            rec = readj(ref['path'])
            assert rec['opaque_id'] == ref['opaque_id']
            out[(ds, ref['opaque_id'], method)].append((ref, rec))
    return out


def graph_relation(graph, root, entities):
    if graph is None:
        return val(None, 'missing_channel'), {}
    reverse = defaultdict(set)
    for e, targets in graph.items():
        for target in targets:
            reverse[target].add(e)
    distance = {root: 0}
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for parent in reverse[current]:
            if parent not in distance:
                distance[parent] = distance[current] + 1
                queue.append(parent)
    ancestors = sorted(set(distance) - {root})
    rows = {}
    for entity in sorted(set(entities) | set(graph)):
        rows[entity] = {'indegree': len(reverse[entity]), 'outdegree': len(graph.get(entity, set())),
                        'direct_to_root': entity != root and root in graph.get(entity, set()),
                        'path_to_root': entity != root and entity in distance,
                        'shortest_distance': distance.get(entity) if entity != root else None}
    return val(ancestors), rows


def stored_local(rec, method):
    """Saved method-native metadata for every entity, before labels are read."""
    if rec['status'] != 'OK':
        return {'availability': 'N/A', 'reason': 'unsupported' if rec['status'] == 'UNSUPPORTED' else 'non_OK'}
    out = {'availability': 'available', 'reason': None, 'items': rec['ranking'],
           'input_shape': rec['input_shape'], 'window': rec['window'], 'input_sha256': rec['input_sha256']}
    if method == 'circa_ols_da':
        out['nodes_after_prune'] = rec.get('diagnostics', {}).get('nodes', {})
        out['graph_diagnostics'] = rec.get('diagnostics', {}).get('graph')
    if method == 'torai_B':
        out['blocks'] = rec.get('blocks')
        out['branches'] = rec.get('extra', {}).get('nhanh_khoi')
        out['diagnostics'] = rec.get('diagnostics', {})
        out['severity'] = val(None, 'intermediate_not_saved_requires_rerun')
    return out


def local_flag(aggregate, rec, method, root):
    if rec['status'] != 'OK':
        return val(None, 'unsupported' if rec['status'] == 'UNSUPPORTED' else 'non_OK')
    if method in ('baro', 'torai_B'):
        return val(None, 'no_native_activation_threshold' if method == 'baro' else 'intermediate_not_saved_requires_rerun')
    if method == 'simplerca':
        keys = {r['entity']: r['key'] for r in rec['entity_ranking']}
        if root not in keys:
            return val(None, 'root_not_returned')
        return val(keys[root][0] == 0)
    if method in ('microrank_full', 'tracerca'):
        table = aggregate['operations_end_tracerca'] if method == 'tracerca' else aggregate['operations_end']
        row = table['services'].get(root)
        return copy.deepcopy(row['local_nonpositive']) if row else val(None, 'empty_A')
    nodes = rec.get('diagnostics', {}).get('nodes')
    if nodes is None:
        return val(None, 'intermediate_not_saved_requires_rerun')
    mapped = [v for n, v in nodes.items() if n.split('_')[0] == root]
    if not mapped:
        return val(None, 'no_metric_after_prune')
    scores = [v.get('rht_score') for v in mapped]
    if any(x is None or not math.isfinite(x) for x in scores):
        return val(None, 'nonfinite')
    return val(all(x < 3 for x in scores))


def merge_flags(seed_flags):
    if any(v['value'] is True for v in seed_flags):
        result = val(True)
    elif any(v['value'] is None for v in seed_flags):
        result = val(None, 'seed_evidence_missing')
    else:
        result = val(False)
    ntrue = sum(v['value'] is True for v in seed_flags)
    nna = sum(v['value'] is None for v in seed_flags)
    result.update(n_seed_true=ntrue, n_seed_eligible=len(seed_flags), n_seed_NA=nna,
                  extent='all' if seed_flags and ntrue == len(seed_flags) else 'partial' if ntrue else 'none')
    return result


def assigned(flags, wrong):
    if not wrong:
        return {'primary': None, 'multi': [], 'applicable': False}
    multi = [m for m in ORDER if flags[m]['value'] is True]
    return {'primary': multi[0] if multi else 'M0', 'multi': multi or ['M0'], 'applicable': True}


def analysis_rows(step1, aggregates, graphs, refs, ranks, feature_paths):
    from ranking_evidence import certain_before, p0_value
    excluded = {x['opaque_id'] if isinstance(x, dict) else x for x in step1['circa_dev19_conditional']['excluded_confirmed_rounding11']}
    rows = []
    for original in step1['main_rows']:
        row = copy.deepcopy(original)
        ds, oid, method, root = row['dataset'], row['opaque_id'], row['method'], row['root']
        agg = aggregates[(ds, oid)]
        split = 'start' if method == 'simplerca' else 'end'
        graph = graphs[(ds, oid)][split]
        if ds == 'Nezha-OB' and method in ('circa_ols_da', 'torai_B'):
            graph = None
        seeds = {}
        for ref, rec in refs[(ds, oid, method)]:
            sid = 'single' if rec['seed'] is None else str(rec['seed'])
            summary = ranks[ref['path']]
            ancestors, relation = graph_relation(graph, root, summary['O'])
            before = certain_before(rec, root)
            local = local_flag(agg, rec, method, root)
            flags = {}
            if rec['status'] != 'OK':
                for m in ORDER:
                    flags[m] = val(None, 'unsupported' if rec['status'] == 'UNSUPPORTED' else 'non_OK')
            else:
                flags['M1'] = val(root not in summary['O'])
                flags['M2'] = val(root in summary['O'] and root not in summary['R'])
                flags['M4'] = val(method == 'circa_ols_da' and oid in excluded)
                flags['M6'] = local
                if graph is None:
                    flags['M5'] = val(None, 'missing_channel')
                elif before is None:
                    flags['M5'] = val(None, 'root_not_returned' if root not in summary['R'] else 'invalid_ranking_invariant')
                else:
                    flags['M5'] = val(bool(set(before) & set(ancestors['value'])))
            metrics = row['seed_metrics'][sid] if 'seed_metrics' in row else row
            by_k = {}
            for k in KS:
                kflags = copy.deepcopy(flags)
                kflags['M3'] = val(0 < metrics[f'hit@{k}'] < 1) if rec['status'] == 'OK' else val(None, 'non_OK')
                wrong = rec['status'] == 'OK' and metrics[f'hit@{k}'] < 1
                if not wrong:
                    p0 = val(None, 'not_OK_wrong_at_k')
                elif summary['availability'] != 'available':
                    p0 = val(None, 'invalid_ranking_invariant')
                elif graph is None:
                    p0 = val(None, 'missing_channel')
                elif root not in summary['R'] or before is None:
                    p0 = val(None, 'root_not_returned')
                else:
                    n = len(summary['O']); a = len(set(ancestors['value']) & (set(summary['O']) - {root})); b = len(before)
                    p0 = val(p0_value(n, a, b)); p0.update(n=n, a=a, b=b)
                by_k[str(k)] = {'flags': kflags, 'P0': p0, 'wrong_OK': wrong, 'assignment': assigned(kflags, wrong)}
            node_rows = {n:v for n,v in rec.get('diagnostics', {}).get('nodes', {}).items() if n.split('_')[0] == root}
            block_rows = []
            for bi, block in enumerate(rec.get('blocks') or []):
                for gi, group in enumerate(block['groups']):
                    if root in group:
                        block_rows.append({'block_index':bi, 'group_index':gi, 'block_key':block['key'],
                                           'group_size':len(group), 'branch':(rec.get('extra', {}).get('nhanh_khoi') or [None]*len(rec['blocks']))[bi]})
            seeds[sid] = {'status':rec['status'], 'source':source(ref['path']), 'ranking':summary,
                          'local_nonpositive':local, 'by_k':by_k, 'caller_relation':relation,
                          'ancestors':ancestors, 'certain_before_root':before, 'CIRCA_root_nodes':node_rows,
                          'TORAI_root_blocks':block_rows, 'native_input_shape':rec['input_shape'],
                          'native_diagnostics':rec.get('diagnostics', {}) if method == 'torai_B' else None}
        by_k = {}
        for k in KS:
            all_ok = [s['by_k'][str(k)]['flags'] for s in seeds.values() if s['status'] == 'OK']
            wrong_ok = [s['by_k'][str(k)]['flags'] for s in seeds.values() if s['by_k'][str(k)]['wrong_OK']]
            base = {m:merge_flags([f[m] for f in all_ok]) if all_ok else val(None, 'non_OK') for m in ORDER}
            explanation = {m:merge_flags([f[m] for f in wrong_ok]) if wrong_ok else val(None, 'no_OK_wrong_seed') for m in ORDER}
            wrong = bool(row[f'wrong_OK_at_{k}'])
            by_k[str(k)] = {'base_flags_all_OK_seeds':base, 'explanation_flags_wrong_seeds':explanation,
                            'assignment':assigned(explanation, wrong), 'n_seed_OK_wrong':len(wrong_ok),
                            'P0_aggregation':'per_seed_only_no_OR'}
        root_metrics = {c:v for c,v in agg['metrics'].items() if v['entity'] == root}
        evidence = {'source':source(feature_paths[(ds,oid)], '/aggregate'), 'native_trace_split':split,
                    'root_metric_Simple_convention':root_metrics,
                    'root_trace_start_Simple_convention':agg['trace_start'].get(root, val(None, 'missing_channel')),
                    'root_trace_end_context':agg['trace_end'].get(root, val(None, 'missing_channel')),
                    'root_logs_A_Simple_convention':agg['logs_A'].get(root, val(None, 'missing_channel')),
                    'root_operations_end_native':{op:v for op,v in agg['operations_end_tracerca' if method=='tracerca' else 'operations_end']['operations'].items() if v['entity'] == root},
                    'seed_evidence':seeds, 'schema_audit':None}
        if row['status'] == 'UNSUPPORTED':
            for field in ('root_metric_Simple_convention', 'root_trace_start_Simple_convention', 'root_trace_end_context', 'root_logs_A_Simple_convention', 'root_operations_end_native'):
                evidence[field] = val(None, 'unsupported')
        row.update(analysis_state='computed_fixed_codebook_002', evidence=evidence, mechanisms=by_k)
        rows.append(row)
    return rows


def output_pairs(rows):
    from ranking_evidence import dice_pair
    by_method = defaultdict(list)
    for row in rows:
        by_method[(row['dataset'], row['method'])].append(row)
    pairs = []
    seed_pairs = []
    for (ds, method), cases in by_method.items():
        for left, right in itertools.combinations(sorted(cases, key=lambda r:r['opaque_id']), 2):
            for k in KS:
                values = []
                invalid = Counter()
                for sl, sr in itertools.product(left['evidence']['seed_evidence'].values(), right['evidence']['seed_evidence'].values()):
                    d = dice_pair(sl['ranking'], sr['ranking'], k)
                    if d['availability'] == 'available': values.append(d)
                    else: invalid[d['reason']] += 1
                metrics = {name:math.fsum(v[name] for v in values)/len(values) for name in ('D','D0','delta','V')} if values else {name:None for name in ('D','D0','delta','V')}
                pairs.append(dict(dataset=ds, method=method, k=k, left=left['opaque_id'], right=right['opaque_id'],
                                  cell_left=left['cell'], cell_right=right['cell'], same_cell=left['cell']==right['cell'],
                                  n_seed_pair_valid=len(values), n_seed_pair_total=len(left['evidence']['seed_evidence'])*len(right['evidence']['seed_evidence']),
                                  availability='available' if values else 'N/A', reasons=dict(invalid), **metrics))
        if method == 'torai_B':
            for row in cases:
                for (si, a), (sj,b) in itertools.combinations(row['evidence']['seed_evidence'].items(),2):
                    for k in KS:
                        seed_pairs.append(dict(dataset=ds, method=method, opaque_id=row['opaque_id'], seed_left=si, seed_right=sj, **dice_pair(a['ranking'],b['ranking'],k)))
    grouped = defaultdict(list)
    for pair in pairs:
        cells = tuple(sorted([pair['cell_left'],pair['cell_right']]))
        grouped[(pair['dataset'],pair['method'],pair['k'],pair['same_cell'],cells)].append(pair)
    cells = []
    for (ds,method,k,same,cellnames), pp in grouped.items():
        valid=[x for x in pp if x['availability']=='available']
        values={name:math.fsum(x[name] for x in valid)/len(valid) if valid else None for name in ('D','D0','delta','V')}
        cells.append(dict(dataset=ds,method=method,k=k,same_cell=same,cells=list(cellnames),n_case_pairs_valid=len(valid),n_case_pairs_total=len(pp),n_seed_pairs_valid=sum(x['n_seed_pair_valid'] for x in pp),n_seed_pairs_total=sum(x['n_seed_pair_total'] for x in pp),**values))
    final = []
    for ds,method in by_method:
        for k in KS:
            for same in (False,True):
                cc=[x for x in cells if x['dataset']==ds and x['method']==method and x['k']==k and x['same_cell']==same]
                valid=[x for x in cc if x['D'] is not None]
                final.append(dict(dataset=ds,method=method,k=k,same_cell=same,n_cell_units_valid=len(valid),n_cell_units_total=len(cc),
                                  **{name:math.fsum(x[name] for x in valid)/len(valid) if valid else None for name in ('D','D0','delta','V')}))
    return {'case_pairs':pairs,'cell_pairs':cells,'equal_cell_weight_summaries':final,'within_case_seed_pairs':seed_pairs}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-id',required=True);parser.add_argument('--reuse-features-from');args=parser.parse_args()
    run=ROOT/'results/T-028/runs'/args.run_id
    if run.exists(): raise RuntimeError('Run exists: preserve it; use a new run-id')
    run.mkdir(parents=True)
    start=time.perf_counter();manifest={'task':'T-028','run_id':args.run_id,'status':'running','started_at':now(),'codebook':{'path':'results/T-028/codebook.md','sha256':sha(ROOT/'results/T-028/codebook.md')},'method_rerun':False,'payload_files':[]}
    def progress(stage,**detail):
        event={'at':now(),'elapsed_s':time.perf_counter()-start,'stage':stage,**detail}
        with (run/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n')
        print(json.dumps(event,ensure_ascii=False),flush=True)
    writej(run/'manifest.json',manifest);progress('start')
    try:
        from native_stats import compute_case, load_case, _span_splits, graph_stats
        from ranking_evidence import ranking_summary
        frozen=readj('results/T-028/runs/chot-codebook-002/manifest.json')
        assert manifest['codebook']['sha256']==frozen['codebook']['sha256']
        manifest['script_snapshot'] = {}
        for script in Path(__file__).parent.glob('*.py'):
            snap = run/'script-snapshot'/script.name
            snap.parent.mkdir(parents=True,exist_ok=True)
            snap.write_bytes(script.read_bytes())
            manifest['script_snapshot'][script.name] = {'path':str(snap.relative_to(ROOT)).replace('\\','/'),'sha256':sha(snap)}
        manifest['source_baseline'] = {p:sha(ROOT/p) for p in ['AGENTS.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-028-p4-han-che-xep-hang/SPEC.md','results/T-028/runs/danh-sach-001/step1.json','results/T-024/ban-ghi-dua-vao-cham.json','results/T-026/ban-ghi-dua-vao-cham.json','results/T-022/allowlist-dev.json','results/T-026/allowlist-dev.json','src/p3/selector.py','src/p3/cua_so.py','src/p3/nezha.py','src/p3/danh_gia.py']}
        writej(run/'manifest.json',manifest)
        refs=main_refs()
        for ds in ('RE2-TT','Nezha-OB'):
            ids={oid for d,oid,m in refs if d==ds}
            assert len(ids)==(30 if ds=='RE2-TT' else 22)
            assert all((ds,oid,method) in refs and refs[(ds,oid,method)] for oid in ids for method in METHODS)
        assert sum(map(len,refs.values()))==372
        progress('saved_records_verified',n=sum(map(len,refs.values())))
        aggregates={};graphs={};rankings={};saved={}
        cases=sorted({(ds,oid) for ds,oid,method in refs})
        reuse_index=None
        if args.reuse_features_from:
            previous=ROOT/'results/T-028/runs'/args.reuse_features_from
            reuse_index=readj(str((previous/'features-no-label-index.json').relative_to(ROOT)))
            previous_manifest=readj(str((previous/'manifest.json').relative_to(ROOT)))
            assert previous_manifest['codebook']['sha256']==manifest['codebook']['sha256']
            manifest['reuse_features_from']=str(previous.relative_to(ROOT)).replace('\\','/')
            manifest['reuse_policy']='existing all-service statistics reused by SHA; rebuild only RAM graph via guarded reader, before opening labels'
            writej(run/'manifest.json',manifest)
        for ds,oid in cases:
            base=refs[(ds,oid,'baro')][0][1]
            t=base['window'].get('t')
            if reuse_index is None:
                aggregate, gg=compute_case(ROOT,ds,oid,t=t)
            else:
                reuse=reuse_index['cases'][ds][oid]
                assert sha(ROOT/reuse['path'])==reuse['sha256']
                previous_feature=readj(reuse['path'])
                aggregate=previous_feature['aggregate']
                payload=load_case(ROOT,ds,oid,t=t)
                assert payload['window']==aggregate['window']
                assert payload['provenance_safe']==aggregate['provenance']
                start_mask,end_mask=_span_splits(payload['spans'],payload['t_seconds'],ds)
                masks={'start':start_mask,'end':end_mask}
                gg={}
                for split in ('start','end'):
                    audit,adj=graph_stats(payload['spans'],masks[split])
                    for field in audit:
                        assert audit[field]==aggregate['graph_'+split][field],(ds,oid,split,field)
                    gg[split]=adj
                del payload,masks,adj
            aggregates[(ds,oid)]=aggregate;graphs[(ds,oid)]=gg
            stored={}
            for method in METHODS:
                stored[method]={}
                for ref,rec in refs[(ds,oid,method)]:
                    if method == 'simplerca' and rec['status']=='OK':
                        actual={r['entity']:r['key'][0] for r in rec['entity_ranking']}
                        expected={e:r['score_reconstructed'] for e,r in aggregate['simple_entity_max'].items()}
                        assert actual==expected, ('SimpleRCA component sum mismatch',ds,oid,[(e,actual.get(e),expected.get(e)) for e in set(actual)|set(expected) if actual.get(e)!=expected.get(e)][:5])
                    if ds=='RE2-TT':
                        assert rec['window']['t']==t
                        for name,meta in aggregate['provenance']['sources'].items():
                            assert rec['input_sha256'].get(name)==meta.get('sha256'), (ds,oid,method,name)
                    key='single' if rec['seed'] is None else str(rec['seed'])
                    rankings[ref['path']]=ranking_summary(rec)
                    stored[method][key]={'record_source':ref,'ranking_summary':rankings[ref['path']],'native_saved':stored_local(rec,method)}
            if reuse_index is None:
                path=run/'features-no-label'/ds/(oid+'.json')
                writej(path,{'dataset':ds,'opaque_id':oid,'aggregate':aggregate,'saved_methods':stored})
                saved[(ds,oid)]=str(path.relative_to(ROOT)).replace('\\','/')
                progress('case_features_no_label_written',dataset=ds,opaque_id=oid,source=saved[(ds,oid)])
            else:
                assert stored==previous_feature['saved_methods']
                saved[(ds,oid)]=reuse['path']
                progress('case_features_reused_RAM_graph_verified',dataset=ds,opaque_id=oid,source=saved[(ds,oid)])
        feature_path=str((run/'features-no-label-index.json').relative_to(ROOT)).replace('\\','/')
        feature_index={'created_before_labels':now(),'cases':{ds:{oid:{'path':saved[(ds,oid)],'sha256':sha(ROOT/saved[(ds,oid)])} for d,oid in cases if d==ds} for ds in ('RE2-TT','Nezha-OB')}}
        writej(ROOT/feature_path,feature_index);progress('all_features_serialized_before_labels',source=feature_path)
        # The first access to labels/scored step1 occurs only after this barrier.
        step1=readj('results/T-028/runs/danh-sach-001/step1.json')
        labels={ds:{x['opaque_id']:x for x in readj(path)['cases']} for ds,path in [('RE2-TT','results/T-022/nhan-dev.json'),('Nezha-OB','results/T-026/nhan-dev.json')]}
        for row in step1['main_rows']:
            label=labels[row['dataset']][row['opaque_id']]
            for field in ('root','fault','cell','nhom_loi','nhom_vi_tri_p75'): assert row[field]==label[field]
        progress('labels_joined_for_analysis_only')
        rows=analysis_rows(step1,aggregates,graphs,refs,rankings,saved)
        out={'task':'T-028','codebook_manifest':'results/T-028/runs/chot-codebook-002/manifest.json','run':str(run.relative_to(ROOT)).replace('\\','/'),'main_rows':rows,
             'circa_dev19_conditional':copy.deepcopy(step1['circa_dev19_conditional']),
             'nezha_saved_sensitivity_flags':copy.deepcopy(step1['nezha_saved_sensitivity_flags'])}
        lookup={(r['dataset'],r['opaque_id'],r['method']):r for r in rows}
        for r in out['circa_dev19_conditional']['rows']:
            mainrow=lookup[(r['dataset'],r['opaque_id'],r['method'])]
            r['evidence']=mainrow['evidence'];r['mechanisms']=mainrow['mechanisms'];r['analysis_state']='reused_dev30_evidence_conditional'
        writej(run/'ca-sai.json',out);progress('step4_assignments_written',n_main_rows=len(rows))
        pairs=output_pairs(rows);writej(run/'concentration.json',pairs);progress('D_D0_written')
        manifest.update(status='analysis_computed_pending_independent_and_manual',finished_analysis_at=now(),elapsed_s=time.perf_counter()-start,
                        feature_index=feature_path,outputs={'ca-sai.json':sha(run/'ca-sai.json'),'concentration.json':sha(run/'concentration.json')})
        writej(run/'manifest.json',manifest)
    except BaseException as exc:
        manifest.update(status='failed',failed_at=now(),elapsed_s=time.perf_counter()-start,error=repr(exc),traceback=traceback.format_exc())
        writej(run/'manifest.json',manifest);progress('failed',error=repr(exc));raise


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()

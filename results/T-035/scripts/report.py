"""Tổng hợp sau barrier ghi đồ thị; ghép nhãn chỉ ở phần báo cáo."""
import json,sys,time,re,csv,hashlib,shutil
from pathlib import Path
from collections import Counter,defaultdict
from run import ROOT,OUT,read,write,selector,pd

def canonical_graphs(cases):
    paths=[]
    for c in cases:
        ds,oid=c['dataset'],c['opaque_id']
        run='day-du-001' if (OUT/'runs/day-du-001/cases'/ds/f'{oid}.json').exists() else 'pilot-002'
        for p in sorted((OUT/'runs'/run/'do-thi'/ds/oid).rglob('*.json')):
            dest=OUT/'do-thi'/ds/oid/p.relative_to(OUT/'runs'/run/'do-thi'/ds/oid)
            dest.parent.mkdir(parents=True,exist_ok=True)
            assert not dest.exists();shutil.copyfile(p,dest)
            assert selector.sha256_file(p)==selector.sha256_file(dest)
            paths.append(dest.relative_to(ROOT).as_posix())
    return paths

def k3(cases):
    original=read(ROOT/'results/T-002/local-inspection/run-002/cases.json')
    allow=selector.nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
    rows=[]
    for c in cases:
        if c['dataset']!='RE2-TT':continue
        name=Path(allow[c['opaque_id']]['case_dir']).name
        ix=next(i for i,x in enumerate(original) if x['case']==name)
        old=original[ix]['trace'];now=c['windows']['full']
        expected=[old['n_spans'],old['parent_resolved_count'],old['parent_reference_count'],len(old['graphs']['full']['nodes']),len(old['graphs']['full']['edges'])]
        actual=[now['stats']['raw_spans'],now['stats']['resolved_parents'],now['stats']['parent_references'],now['entity_nodes'],now['entity_edges']]
        graph=read(OUT/'do-thi/RE2-TT'/c['opaque_id']/'thuc-the/full.json')
        edges=sorted([r['source'],r['target']] for r in graph['edges'])
        nodes=sorted(r['id'] for r in graph['nodes'])
        rows.append({'opaque_id':c['opaque_id'],'source_pointer':f'#/{ix}/trace','expected':expected,'actual':actual,
                     'pass':expected==actual and edges==sorted(old['graphs']['full']['edges']) and nodes==sorted(old['graphs']['full']['nodes'])})
    result={'rows':rows,'pass':all(r['pass'] for r in rows),'totals':[sum(r['actual'][i] for r in rows) for i in range(3)],
            'node_edge_distribution':dict(Counter(f'{r["actual"][3]}/{r["actual"][4]}' for r in rows))}
    write(OUT/'runs/kiem-cuoi-001/K3.json',result);assert result['pass'],'K3_STOP'
    return result

def vocabulary(cases):
    allrows=[];ds_summary={}
    pattern=re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|(?<![A-Za-z0-9])[0-9a-fA-F]{16,}(?![A-Za-z0-9])|/\d+(?:/|$)')
    for ds in ['RE2-TT','Nezha-OB']:
        rows=[c for c in cases if c['dataset']==ds];presence=defaultdict(set);owners=defaultdict(set);data={}
        for c in rows:
            for o in c['vocabulary']['full']['operations']:
                oid=o['id'];presence[oid].add(c['opaque_id']);owners[o['operation']].add(o['entity']);data[oid]=o
            allrows.append({'dataset':ds,'opaque_id':c['opaque_id'],'windows':c['vocabulary']})
        idlike=[oid for oid in data if pattern.search(data[oid]['operation'] or '')]
        only_http=[oid for oid in data if (data[oid]['operation'] or '').upper() in ['GET','POST','PUT','PATCH','DELETE','HEAD','OPTIONS']]
        ds_summary[ds]={'distinct_entity_operations':len(data),'distinct_names':len(owners),
                        'operations_present_all_cases':sum(len(v)==len(rows) for v in presence.values()),
                        'operations_one_case':sorted(k for k,v in presence.items() if len(v)==1),
                        'candidate_id_names':idlike,'only_http_method':only_http,
                        'names_multiple_entities':{str(k):sorted(v) for k,v in owners.items() if len(v)>1},
                        'presence':{k:sorted(v) for k,v in sorted(presence.items())},
                        'max_child_signature_count':max(o['child_signature_count'] for c in rows for o in c['vocabulary']['full']['operations']),
                        'max_internal_depth':max(o['max_internal_depth'] for c in rows for o in c['vocabulary']['full']['operations'])}
    write(OUT/'tu-vung-thao-tac.json',{'datasets':ds_summary,'cases':allrows,'id_rule':pattern.pattern,
                                      'rule_status':'description_only_no_normalization'})
    return ds_summary

def nezha_extra(cases):
    ver=read(OUT/'runs/buoc0-001/input-verification.json');frozen=read(ROOT/'results/T-003/runs/final-review-003/artifact-manifest.json')
    lookup={r['path']:r['sha256'] for r in frozen['files']};refs=[];days={}
    for r in ver['auxiliary_sources']:
        assert r['receipt'] in lookup and selector.sha256_file(ROOT/r['receipt'])==lookup[r['receipt']],'receipt_not_frozen'
        assert selector.sha256_file(ROOT/r['path'])==r['sha256'],'auxiliary_changed'
        p=Path(r['path']);day=p.parent.parent.name;record=dict(r)
        if p.name=='dependency.csv':
            f=pd.read_csv(ROOT/p,usecols=['Source','Target'],dtype=str)
            record['pairs']=sorted(set(tuple(x) for x in f[['Source','Target']].itertuples(index=False,name=None)))
            record['columns_read']=['Source','Target']
        else:
            with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:headers=next(csv.reader(f))
            record['headers']=headers;record['columns_read']='header_only'
            # Cặp tường minh từ hai tên service trong header, không suy kiểu quan hệ.
            names=set(s for c in cases if c['dataset']=='Nezha-OB' for s in c['windows']['full']['coverage'])
            dictionary={a+'_'+b:(a,b) for a in names for b in names}
            record['pairs']=sorted(dictionary[h] for h in headers if h in dictionary)
            record['unmapped_headers']=[h for h in headers if h not in dictionary and h not in ('time','timestamp')]
        refs.append(record);days.setdefault(day,{})[p.name]=record
    comparisons=[]
    for c in cases:
        if c['dataset']!='Nezha-OB':continue
        day=next(iter(c['node']['metric_Node_headers'])).split('/')[-3]
        graph=read(OUT/'do-thi/Nezha-OB'/c['opaque_id']/'thuc-the/full.json')
        observed={(e['source'],e['target']) for e in graph['edges']}
        for name,r in days[day].items():
            reference=set(map(tuple,r['pairs']))
            comparisons.append({'opaque_id':c['opaque_id'],'day':day,'reference':name,'trace_edges':len(observed),
                                'reference_pairs':len(reference),'trace_only':sorted(observed-reference),
                                'reference_only':sorted(reference-observed),'intersection':len(observed&reference)})
    write(OUT/'runs/kiem-cuoi-001/K6.json',{'sources':refs,'comparisons':comparisons,
          'scope':'day-level relationship metadata may aggregate test intervals; only descriptive comparison, never builder/P6 input',
          'generation':'OPEN: inspected README, paper and downloaded analysis code do not define generation of the three CSV artifacts',
          'independence':'NOT_CONFIRMED'})
    nodes=[{'opaque_id':c['opaque_id'],**c['node']} for c in cases if c['dataset']=='Nezha-OB']
    values=sorted(set(n for c in nodes for n in c['node_to_pods']))
    pods=defaultdict(set)
    for c in nodes:
        for pod,ns in c['pod_to_nodes'].items():pods[pod].update(ns)
    write(OUT/'cot-node-nezha.json',{'meaning':'OPEN','deployment_edges_confirmed':False,'distinct_Node':values,
        'pod_to_nodes_all_dev':{p:sorted(v) for p,v in sorted(pods.items())},'cases':nodes,
        'source_review':[{'source':'results/T-008/sources/README.md','finding':'No definition of exported Node column'},
                         {'source':'results/T-008/sources/FSE2023_Nezha.pdf','page':8,'finding':'Kubernetes and Node Exporter described; no exported column-to-host identifier contract'},
                         {'source':'results/T-008/sources/tree.json','finding':'Published Python inventory contains analysis, not collector/export code defining Node'}],
        'missing':'Collector/export code or explicit column definition linking these Node values to host identities.'})

def labels(cases):
    # Chỉ chạy sau canonical graphs và label-free supplement đã ghi.
    supplemental=read(OUT/'runs/bo-sung-001/summary.json');assert supplemental['label_free']
    label_maps={ds:{c['opaque_id']:c for c in read(ROOT/f'results/{task}/nhan-dev.json')['cases']} for ds,task in [('RE2-TT','T-022'),('Nezha-OB','T-026')]}
    counts={(c['dataset'],c['opaque_id']):c for c in supplemental['cases']};rows=[];cell=defaultdict(list)
    for c in cases:
        ds,oid=c['dataset'],c['opaque_id'];l=label_maps[ds][oid];root=l['root'];sc=counts[(ds,oid)]
        incoming=[e for e in sc['edge_counts_parent_end_split'] if e['callee']==root]
        enough=[e for e in incoming if e['enough_20_each']]
        status='no_incoming' if not incoming else 'too_sparse' if not enough else 'has_20_each'
        row={'dataset':ds,'opaque_id':oid,'root':root,'fault':l['fault'],'cell':l['cell'],
             'root_coverage':c['windows']['full']['coverage'].get(root,'outside_inventory'),
             'incoming_status':status,'incoming':incoming,'F_counts':{k:sc[k] for k in ['A_start_traces','A_traces_missing_parent_in_F','A_traces_missing_parent_in_A','A_end_traces','A_end_traces_missing_parent_in_A_end']},
             'entity_full':c['windows']['full']['entity_fingerprint'],'operation_full':c['windows']['full']['operation_fingerprint']}
        rows.append(row);cell[ds+'|'+str(l['cell'])].append(row)
    totals=dict(Counter(r['incoming_status'] for r in rows))
    write(OUT/'do-phu-theo-nhan.json',{'label_join_after_graph_and_supplement':True,'rows':rows,'totals':totals,
          'cells':{k:{'cases':len(v),'incoming_status':dict(Counter(r['incoming_status'] for r in v)),
                      'entity_shapes':len({r['entity_full'] for r in v}),'operation_shapes':len({r['operation_full'] for r in v})} for k,v in sorted(cell.items())},
          'G2_H19_expected':{'no_incoming':8,'too_sparse':7},
          'G2_H19_match':totals.get('no_incoming',0)==8 and totals.get('too_sparse',0)==7,
          'definition':'Same incoming entity pair needs at least 20 parent-end-before and 20 parent-end-after calls on F, per T032 call_slow_table_v1 MIN_CALLS. No graph design uses this label grouping.'})
    return totals

def main():
    full=read(OUT/'runs/day-du-001/summary.json');assert full['status']=='PASS' and len(full['cases'])==52
    cases=full['cases'];paths=canonical_graphs(cases);kt=k3(cases);v=vocabulary(cases);nezha_extra(cases);totals=labels(cases)
    stats={}
    for ds in ['RE2-TT','Nezha-OB']:
        rows=[c for c in cases if c['dataset']==ds]
        stats[ds]={'cases':len(rows),'full_entity_shapes':len({c['windows']['full']['entity_fingerprint'] for c in rows}),
                   'full_operation_shapes':len({c['windows']['full']['operation_fingerprint'] for c in rows}),
                   'N_entity_shapes':len({c['windows']['N']['entity_fingerprint'] for c in rows}),
                   'A_entity_shapes':len({c['windows']['A']['entity_fingerprint'] for c in rows}),
                   'N_A_entity_changed':sum(c['windows']['N']['entity_fingerprint']!=c['windows']['A']['entity_fingerprint'] for c in rows),
                   'N_A_operation_changed':sum(c['windows']['N']['operation_fingerprint']!=c['windows']['A']['operation_fingerprint'] for c in rows),
                   'span_total':sum(c['windows']['full']['stats']['raw_spans'] for c in rows),
                   'cross_parent_events':sum(c['windows']['full']['stats']['cross_entity_parent_events'] for c in rows),
                   'cross_parent_contains':sum(c['windows']['full']['stats']['cross_parent_contains_child'] for c in rows),
                   'same_entity_events':sum(c['windows']['full']['stats']['same_entity_parent_events'] for c in rows),
                   'operation_pairs_per_entity_edge':[], 'snapshot_shapes':{}}
        for size in [60,300] if ds=='RE2-TT' else []:
            window_rows=[w for c in rows for n,w in c['windows'].items() if n.startswith('s'+str(size)+'-')]
            stats[ds]['snapshot_shapes'][str(size)]={'windows':len(window_rows),'distinct':len({w['entity_fingerprint'] for w in window_rows}),
                  'empty_windows':sum(w['entity_nodes']==0 for w in window_rows)}
        for c in rows:
            o=read(OUT/'do-thi'/ds/c['opaque_id']/'thao-tac/full.json');owner=dict(o['belongs_to']);pair=defaultdict(set)
            for e in o['edges']:
                a,b=owner.get(e['source'],e['source']),owner.get(e['target'],e['target'])
                if a!=b and e['type']!='span-parent':pair[(a,b)].add((e['source'],e['target']))
            stats[ds]['operation_pairs_per_entity_edge'].append({'opaque_id':c['opaque_id'],'edge_pair_counts':[{'source':a,'target':b,'operation_pairs':len(s)} for (a,b),s in sorted(pair.items())]})
    write(OUT/'thong-ke-do-thi.json',{'datasets':stats,'cases':cases,'K3':kt,'canonical_graph_files':paths,
                                    'cost':{'full_run_seconds':full['seconds'],'peak_rss_bytes':max(c['peak_rss_bytes'] for c in cases)},
                                    'window_definition':'RE2 full dev trace table, Nezha authorized dev window only; N/A fully contained spans; RE2 snapshots min(start) anchor, end<right; parent must be in same window'})
    print(json.dumps({'K3':kt['pass'],'stats':{d:{k:x for k,x in s.items() if k not in ('operation_pairs_per_entity_edge',)} for d,s in stats.items()},'K8':totals},ensure_ascii=False,indent=1))

if __name__=='__main__':main()

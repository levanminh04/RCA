"""Summarize supported author probe; never replace published/default/P3 results."""
import pathlib,json,hashlib,collections,csv
P=pathlib.Path(__file__).parent/'author-tracerca'
src=P/'full007-stream/summary.json'
x=json.loads(src.read_text(encoding='utf-8'))
rows=x['rows']; assert len(rows)==208
slots={(r['dataset'],r['opaque_id'],r['latency_unit'],r['feature_selection_threshold']) for r in rows}
assert len(slots)==208 and len({s[:2] for s in slots})==52
manifest=json.loads((P/'full007-manifest.json').read_text(encoding='utf-8'))
for rel,m in manifest.items():
 f=P/rel;assert f.stat().st_size==m['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256'],rel
groups=[]
for dataset in ['RE2-TT','Nezha-OB']:
 for unit in ['ms','us']:
  for threshold in [1.,3.]:
   rr=[r for r in rows if (r['dataset'],r['latency_unit'],r['feature_selection_threshold'])==(dataset,unit,threshold)]
   assert len(rr)==(30 if dataset=='RE2-TT' else 22)
   g={'dataset':dataset,'unit':unit,'feature_threshold':threshold,'N':len(rr),'statuses':dict(collections.Counter(r['status'] for r in rr)),'root_absent':sum(r['root_rank_min'] is None for r in rr),'ties_at_root':sum(r['root_rank_min'] is not None and r['root_rank_max']>r['root_rank_min'] for r in rr)}
   for k in [1,2,3]:
    g['hit'+str(k)+'_pessimistic']=sum(r['root_rank_max'] is not None and r['root_rank_max']<=k for r in rr)
    g['hit'+str(k)+'_optimistic']=sum(r['root_rank_min'] is not None and r['root_rank_min']<=k for r in rr)
    g['hit'+str(k)+'_expected']=sum(min(1.,max(0.,(k-r['root_rank_min']+1)/(r['root_rank_max']-r['root_rank_min']+1))) if r['root_rank_min'] is not None else 0. for r in rr)
   g['pairs_without_history_total']=sum(r['feature_missing_history_pairs_ignored'] for r in rr)
   g['cache_fallback_pairs_total']=sum(r['native_cache_fallback_pairs_used'] for r in rr)
   g['max_patterns_seen']=max(r['stream'].get('patterns_seen',0) for r in rr)
   groups.append(g)
out={'status':'PASS','scope':'Supported latency-only adapter, short history; NOT default/published reproduction or P3 replacement. Root absent/no evidence count 0 in diagnostic Hit denominator. Expected tie convention uniform permutation within exact equal scores. No unit/threshold selected from these results.','source':str(src.relative_to(P.parent)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':208,'unique_cases':52,'manifest_files_pass':len(manifest),'elapsed_s':x['elapsed_s'],'groups':groups}
(P/'supported-summary-001.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (P/'supported-comparison-001.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['dataset','unit','feature_threshold','N','root_absent','ties_at_root']+[f'hit{k}_{s}' for k in [1,2,3] for s in ['pessimistic','expected','optimistic']]
 w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(groups)
print(json.dumps({'PASS':True,'rows':len(rows),'groups':groups},ensure_ascii=False))

"""Full1069 replay: R1, comparator-only and comparator+provenance SMTP delta."""
from engine_smtp import *
import traceback,platform

def main(name):
 out=HERE/'checks'/name;out.mkdir(parents=True,exist_ok=False);started=time.perf_counter();rows=[]
 try:
  new=api();old=package('t038_original_R1',ROOT/'results/T-036/runs/kiem-r1-after-002/code')
  base=ROOT/'results/T-038';previous=load(HERE/'before/results/T-038/manifest.json');index={r['path']:r for r in previous['files']}
  def frozen(path):
   p=base/path;assert sha(p)==index[p.relative_to(ROOT).as_posix()]['sha256'];return load(p)
  doc=frozen('ban-ghi.json');reg=frozen('runs/doi-chieu-dev-002/registry.json');mapping=frozen('mapping.json')
  bg={'entity':frozen('do-thi/thuc-the.json'),'operation':frozen('do-thi/thao-tac.json')}
  snap=canon([doc,reg]);assert new.build(doc,reg)==old.build(doc,reg)==(bg['entity'],bg['operation']);assert snap==canon([doc,reg])
  delta=load(ROOT/'results/T-036/runs/doi-chieu-smtp-001/checks-smtp-v2-001/proposed-T038-delta.json')
  # Record ID was an explicit preview identifier in the approved package; retain it for exact provenance.
  nd=copy.deepcopy(doc);nd['relations'].append(delta)
  ne,no=new.build(nd,reg);graphs={'entity':ne,'operation':no};projection=new.project(no)
  save(HERE/'ban-ghi.json',nd);save(HERE/'nguon.json',frozen('nguon.json'));save(HERE/'mapping.json',mapping)
  save(HERE/'registry-compare.json',reg)
  save(HERE/'do-thi/thuc-the.json',ne);save(HERE/'do-thi/thao-tac.json',no);save(HERE/'do-thi/chieu-thuc-the.json',projection)
  save(out/'delta.json',delta)
  for g,prior in [(ne,bg['entity']),(no,bg['operation'])]:
   assert [e for e in g['edges'] if delta['id'] not in e['record_ids']]==prior['edges']
   assert len(g['edges'])==len(prior['edges'])+1
  perm=copy.deepcopy(nd)
  for key in ['entities','operations','relations','resource_bindings','signals']:perm[key].reverse()
  assert new.build(perm,reg)==(ne,no)
  summary=frozen('runs/doi-chieu-dev-002/summary.json');assert summary['graph_count']==1069
  t35=ROOT/'results/T-035/manifest.json';assert sha(t35)==previous['input_manifests']['results/T-035/manifest.json']['sha256']
  m35={r['path']:r for r in load(t35)['files']}
  for i,row in enumerate(summary['rows'],1):
   ip=ROOT/row['input'];assert sha(ip)==row['input_sha256']==m35[row['input']]['sha256'];trace=load(ip);level=row['level']
   mappings=[m for m in mapping if m['level']=='entity' or level=='operation']
   ctx=dict(system='RE2-TT',level=level,domain='dev-file',trace_revision='T035-v2.1-manifest:'+sha(t35),revision_link_verified=False,revision_provenance=[])
   priorpath=ROOT/row['output'];assert sha(priorpath)==row['output_sha256'];prior=read_result(priorpath)
   before=canon([bg[level],graphs[level],trace,mappings,ctx,reg])
   replay=old.compare(bg[level],trace,mappings,ctx,reg)
   assert replay==prior,'R1 replay differs from exact saved result'
   only=new.compare(bg[level],trace,mappings,ctx,reg);assert only==prior,'unplanned comparator effect without SMTP'
   got=new.compare(graphs[level],trace,mappings,ctx,reg);independent(got,graphs[level],trace,mappings)
   repeated=new.compare(graphs[level],trace,mappings,ctx,reg);assert repeated==got
   reordered=new.compare(graphs[level],permute(trace),list(reversed(mappings)),ctx,reg)
   assert semantic(reordered)==semantic(got),'order-sensitive result'
   assert before==canon([bg[level],graphs[level],trace,mappings,ctx,reg])
   for vn,v in got['views'].items():
    beforev=only['views'][vn]
    assert v['T']==beforev['T'] and v['intersection']==beforev['intersection'] and v['trace_only']==beforev['trace_only']
    assert v['members']['trace']==beforev['members']['trace'] and v['exclusions']['trace']==beforev['exclusions']['trace']
    added={canon(x) for x in v['S']}-{canon(x) for x in beforev['S']}
    assert len(added)==(1 if vn=='endpoints' else 0)
    assert {canon(x) for x in beforev['S']}<={canon(x) for x in v['S']}
    if added:
     k=json.loads(next(iter(added)));assert k[3]==['smtp',None]
    else:assert v==beforev
   tail=row['input'].split('results/T-035/do-thi/RE2-TT/',1)[1]+'.gz'
   dest=out/'doi-chieu'/tail;compressed(dest,got)
   # Comparator-only output is retained per graph, not just count assertions.
   compressed(out/'comparator-only'/tail,only)
   rows.append(dict(input=row['input'],input_sha256=sha(ip),level=level,interval_ns=trace['interval_ns'],output=dest.relative_to(ROOT).as_posix(),output_sha256=sha(dest),
                    baseline_output=row['output'],baseline_replayed_exactly=True,comparator_only_exact_equal=True,repeat_exact=True,reorder_semantic_equal=True,input_unchanged=True,
                    views={n:{k:len(v[k]) for k in ['S','T','intersection','static_only','trace_only']} for n,v in got['views'].items()},
                    exclusions={n:{side:dict(Counter(x['reason'] for x in v['exclusions'][side])) for side in ['static','trace']} for n,v in got['views'].items()}))
   if i%25==0 or i==1069:
    print(canon(dict(done=i,total=1069,seconds=time.perf_counter()-started)),flush=True)
    with (out/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(canon(dict(done=i,total=1069,seconds=time.perf_counter()-started))+'\n')
  save(out/'summary.json',dict(all_pass=True,graph_count=len(rows),rows=rows,pin=load(HERE/'pin.json'),delta_separated=True,entity_edges_before=len(bg['entity']['edges']),entity_edges_after=len(ne['edges']),operation_edges_before=len(bg['operation']['edges']),operation_edges_after=len(no['edges']),family_counts=summary['graph_family_counts']))
  save(out/'cost.json',dict(elapsed_seconds=time.perf_counter()-started,peak_process_rss_bytes=peak(),python=sys.version,platform=platform.platform(),isolated_benchmark=False,network_bytes=0,output_bytes=sum(p.stat().st_size for p in out.rglob('*') if p.is_file())))
  save(HERE/'diff.json',dict(all_pass=True,graphs=1069,comparator_only_unchanged=1069,delta_endpoint_static_key_added_each_graph=1,typed_unchanged=True,trace_inputs_mappings_and_intersections_unchanged=True,limits='Source SMTP is untyped, trace channel absent; static-only key is not proof of runtime failure.'))
 except Exception:
  save(out/'failure.json',dict(traceback=traceback.format_exc(),completed=len(rows),elapsed_seconds=time.perf_counter()-started));raise
if __name__=='__main__':main(sys.argv[1])

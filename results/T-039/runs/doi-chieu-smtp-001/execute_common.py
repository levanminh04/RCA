"""Replay all existing OB graphs with an explicit common pin; legacy runner retained."""
from pathlib import Path
import sys,copy,time,traceback,platform
from pin_loader import api as current_api,package
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'results/T-038/runs/doi-chieu-smtp-001'))
from engine_smtp import load,sha,canon,save,compressed,read_result,module,peak,semantic,independent,permute,Counter

def main(name):
 out=HERE/'checks'/name;out.mkdir(parents=True,exist_ok=False);started=time.perf_counter();rows=[]
 try:
  api=current_api();old=package('t039_legacy_R1_replay',ROOT/'results/T-036/runs/kiem-r1-after-002/code')
  legacy=module('t039_original_oracle_checker',ROOT/'results/T-039/execute_pinned.py')
  # Preserve the complete literal OB fixture checker, with outputs redirected.
  legacy.oracle(api,out)
  base=ROOT/'results/T-039';previous=load(HERE/'before/results/T-039/manifest.json');idx={x['path']:x for x in previous['files']}
  def frozen(path):
   p=base/path;assert sha(p)==idx[p.relative_to(ROOT).as_posix()]['sha256'];return load(p)
  doc=frozen('ban-ghi.json');reg=frozen('nguon.json');mappingdoc=frozen('mapping.json');mapping=mappingdoc['rows']
  before=canon([doc,reg]);ent,op=api.build(doc,reg)
  assert (ent,op)==old.build(doc,reg)==(frozen('do-thi/thuc-the.json'),frozen('do-thi/thao-tac.json'))
  assert before==canon([doc,reg])
  perm=copy.deepcopy(doc)
  for k in ['entities','operations','relations','resource_bindings','signals']:perm[k].reverse()
  assert api.build(perm,reg)==(ent,op)
  for path,value in [('ban-ghi.json',doc),('nguon.json',reg),('mapping.json',mappingdoc),('do-thi/thuc-the.json',ent),('do-thi/thao-tac.json',op),('do-thi/chieu-thuc-the.json',api.project(op))]:save(HERE/path,value)
  summary=frozen('doi-chieu/tong-hop.json');assert summary['graph_count']==132
  m35=load(ROOT/'results/T-035/manifest.json');ix35={x['path']:x for x in m35['files']}
  for i,row in enumerate(summary['rows'],1):
   path=ROOT/row['path'];assert sha(path)==ix35[row['path']]['sha256'];trace=load(path);sg=ent if row['level']=='entity' else op
   mappings=[m for m in mapping if row['level']=='operation' or m['level']=='entity']
   ctx=dict(system='Nezha-OB',level=row['level'],domain='dev-adapter',trace_revision='T035-v2.1-canonical',revision_link_verified=False,revision_provenance=[])
   priorpath=ROOT/row['output'];assert sha(priorpath)==idx[row['output']]['sha256'];prior=load(priorpath)
   before=canon([sg,trace,mappings,ctx,reg]);replay=old.compare(sg,trace,mappings,ctx,reg);assert replay==prior
   got=api.compare(sg,trace,mappings,ctx,reg);assert got==prior
   legacy.independent(got,sg,trace,mappings);independent(got,sg,trace,mappings)
   assert api.compare(sg,trace,mappings,ctx,reg)==got
   reordered=api.compare(sg,permute(trace),list(reversed(mappings)),ctx,reg);assert semantic(reordered)==semantic(got)
   assert before==canon([sg,trace,mappings,ctx,reg])
   dest=out/'doi-chieu'/row['opaque_id']/row['level']/(row['window']+'.json');save(dest,got)
   rows.append(dict(row,input_sha256=sha(path),baseline_output=row['output'],output=dest.relative_to(ROOT).as_posix(),output_sha256=sha(dest),baseline_replayed_exactly=True,common_pin_result_exact_equal=True,input_unchanged=True,repeat_exact=True,reorder_semantic_equal=True))
   if i%22==0:
    print(canon(dict(done=i,total=132,seconds=time.perf_counter()-started)),flush=True)
  save(out/'summary.json',dict(all_pass=True,graph_count=132,rows=rows,pin=load(HERE/'pin.json'),record_counts=summary['record_counts'],static_counts=summary['static_counts'],mapping_counts=summary['mapping_counts']))
  save(out/'cost.json',dict(elapsed_seconds=time.perf_counter()-started,peak_process_rss_bytes=peak(),python=sys.version,platform=platform.platform(),isolated_benchmark=False,network_bytes=0,output_bytes=sum(p.stat().st_size for p in out.rglob('*') if p.is_file())))
  save(HERE/'diff.json',dict(all_pass=True,graphs=132,replayed_R1_exact=132,new_comparator_exact_equal=132,builder_full_model_exact_equal=True,sets_members_exclusions_denominators_intervals_unchanged=True,source_deployment_runtime_alias_limits_unchanged=True))
 except Exception:
  save(out/'failure.json',dict(traceback=traceback.format_exc(),completed=len(rows),elapsed_seconds=time.perf_counter()-started));raise
if __name__=='__main__':main(sys.argv[1])

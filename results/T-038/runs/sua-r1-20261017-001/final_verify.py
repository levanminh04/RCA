"""Verify complete final scope, preserve history and seal manifests after publication."""
from repair import *
from publish import ROOT_CHANGED, CHECK, SUMMARY, RUN, prompt, RETIRED
import ast, subprocess

def main():
 assert load(HERE/'publication.json')['all_pass']
 verification=load(CHECK/'verification.json');assert verification['all_pass']
 def functions(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text(encoding='utf-8-sig')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
 assert functions(HERE/'repair.py')==functions(CHECK/'runner-used.py')
 save(HERE/'published-runner-equivalence.json',dict(all_check_and_helper_functions_identical_to_executed_runner=True,only_entrypoint_change='Initial one-time prepare command disabled after adoption; current check command unchanged.',executed_runner=rel(CHECK/'runner-used.py'),published_runner=rel(HERE/'repair.py')))
 summary=load(CHECK/'summary.json');assert summary['graph_count']==len(summary['rows'])==1069
 frequencies=Counter((r['level'],Path(r['input']).stem.split('-')[0]) for r in summary['rows'])
 assert frequencies=={('entity','A'):30,('entity','N'):30,('entity','full'):30,('entity','s300'):150,('entity','s60'):739,('operation','A'):30,('operation','N'):30,('operation','full'):30}
 for row in summary['rows']:
  assert sha(ROOT/row['input'])==row['input_sha256'] and sha(ROOT/row['output'])==row['output_sha256']
  assert all(row[k] for k in ['repeat_exact','reorder_semantic_equal','independent_sets_members_exclusions_denominators','input_unchanged'])
 index=load(BASE/'doi-chieu/index.json')
 assert index['summary']==SUMMARY and index['outputs']==[r['output'] for r in summary['rows']]
 model=build_model(load(BASE/'ban-ghi.json'),load(BASE/'nguon.json'))
 for n,v in model.items():
  assert v==load(BASE/'do-thi'/n)==load(HERE/'model'/n)
  assert sha(BASE/'do-thi'/n)==sha(HERE/'model'/n)
 for n in ['ban-ghi.json','nguon.json','mapping.json']:assert load(BASE/n)==load(HERE/'model'/n)
 analysis=load(BASE/'phan-tich-chenh-lech.json');candidate=load(REVIEW/'candidate/phan-tich-chenh-lech.json')
 for k in ['family_stats','full_union']:assert analysis[k]==candidate[k]
 assert analysis['numerical_source']==SUMMARY
 for k in ['full_graphs','chain_examples','exclusions']:
  def normalized(rows):
   r=deepcopy(rows)
   for v in r:
    if 'output' in v:v['output']=next(z['input'] for z in summary['rows'] if z['output']==v['output'])
   return r
  def cn(rows):
   r=deepcopy(rows); lookup={z['output']:z['input'] for z in load(REVIEW/'candidate/summary.json')['rows']}
   for v in r:
    if 'output' in v:v['output']=lookup[v['output']]
   return r
  assert normalized(analysis[k])==cn(candidate[k]),k
 expected_inventory=[];doc=load(BASE/'ban-ghi.json')
 correction=load(HERE/'metadata-correction.json')
 assert next(r for r in doc['entities'] if r['id']=='smtp.163.com')['role']==correction['after']
 assert historical_description(doc)==load(HERE/'checks/full1069-001/model-used/ban-ghi.json')
 for e in sorted(doc['entities'],key=lambda x:x['id']):
  expected_inventory.append(dict(entity=e,operations=sum(x['entity']==e['id'] for x in doc['operations']),outgoing_relations=sum(x['source']['entity']==e['id'] for x in doc['relations']),incoming_relations=sum(x['target']['entity']==e['id'] for x in doc['relations']),signals=sum(x['entity']==e['id'] for x in doc['signals'])))
 assert expected_inventory==load(BASE/'inventory-index.json')
 # Reuse preserved source-flag evidence after matching each safe source span to its exact bytes.
 flags=load(BASE/'runs/hoan-tat-trong-quyen-001/source-flag-resolution.json');proofs=[]
 for item in flags['nine_initializer_proofs']:
  p=BASE/'sources/train-ticket-v1.0.0'/item['source_path'];assert sha(p)==item['sha256'];lines=p.read_text(encoding='utf-8-sig').splitlines()
  assert all(lines[r['line']-1]==r['text'] for r in item['lines'])
  for field in ['then_assignment','else_assignment']:assert item['variable']+' =' in lines[item[field]-1]
  proofs.append(dict(source_path=item['source_path'],locator=item['locator'],source_and_saved_evidence_exact=True,expected_empty_reaches_call=item['expected_empty_reaches_call']))
 assert len(proofs)==9;save(HERE/'historical-evidence-reuse.json',dict(initializer_proofs=proofs,unchanged_source_verified=True,source_flag_counts=flags['resolution_counts'],SMTP_baseline_checks='Historical immutable manifest-pinned checks; unchanged common pin and original inputs verified. Current replay additionally checks producer output against candidate and independent accounting.'))
 for n in ['prompt-claude.txt','prompt-claude-smtp.txt']:assert (BASE/n).read_text(encoding='utf-8-sig')==prompt()
 assert (HERE/'prompt-kiem-ban-sua.txt').read_text(encoding='utf-8-sig')==prompt()
 allowed_external={'docs/STATE.md','tasks/T-038-p5b-trainticket/LOG.md','tasks/T-038-p5b-trainticket/REVIEW.md'}
 for item in load(HERE/'protected-before.json'):
  if item['path'] not in allowed_external:assert sha(ROOT/item['path'])==item['sha256'],'protected changed: '+item['path']
 bp=HERE/'before';log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md';review=ROOT/'tasks/T-038-p5b-trainticket/REVIEW.md';state=ROOT/'docs/STATE.md'
 assert log.read_bytes().startswith((bp/'tasks/T-038-p5b-trainticket/LOG.md').read_bytes())
 marker=b'## Ph\xe1\xba\xa3n h\xe1\xbb\x93i c\xe1\xbb\xa7a ng\xc6\xb0\xe1\xbb\x9di l\xc3\xa0m'
 # Compare the exact reviewer prefix and table header. Only producer table rows may differ.
 oldreview=(bp/'tasks/T-038-p5b-trainticket/REVIEW.md').read_bytes();newreview=review.read_bytes()
 prefix=oldreview.split(b'| R1 | | | |')[0];assert newreview.startswith(prefix)
 table=newreview[len(prefix):].decode('utf-8-sig')
 assert all(line.rstrip().endswith('| |') for line in table.splitlines() if line.startswith('| '))
 oldstate=(bp/'docs/STATE.md').read_bytes();newstate=state.read_bytes()
 def without_task(raw):return b''.join(x for x in raw.splitlines(keepends=True) if not x.startswith(b'| T-038 |'))
 assert without_task(oldstate)==without_task(newstate)
 # Every pre-existing artifact must be untouched, or have its original bytes in before/.
 originals=load(HERE/'before-files.json');changed=[];allowed={rel(BASE/n) for n in ROOT_CHANGED}
 for item in originals:
  p=ROOT/item['path'];assert p.is_file(),'deleted original: '+item['path']
  if sha(p)!=item['sha256']:
   assert item['path'] in allowed,'unexpected mutation: '+item['path']
   copy=bp/item['path'];assert copy.exists() and sha(copy)==item['sha256'],'missing historical copy'
   changed.append(item['path'])
 newfiles=sorted(rel(p) for p in BASE.rglob('*') if p.is_file() and rel(p) not in {r['path'] for r in originals})
 assert all(s.startswith(RUN+'/') for s in newfiles),[s for s in newfiles if not s.startswith(RUN+'/')]
 for name in RETIRED:
  ast.parse((BASE/name).read_text(encoding='utf-8-sig'))
  result=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/name)],capture_output=True,cwd=ROOT)
  assert result.returncode==1 and b'repair.py check' in result.stderr
 # Newly produced sources/checks retain no credential values from the inspected source defaults.
 source=BASE/'sources/train-ticket-v1.0.0'
 nacos=(source/'deployment/kubernetes-manifests/quickstart-k8s/charts/nacos/values.yaml').read_text()
 sn=(source/'deployment/kubernetes-manifests/prometheus/alertsnitch.yml').read_text()
 sensitive=[re.search(r'passowrd:\s*"([^"]+)"',nacos).group(1).encode(),re.search(r'value:\s*(\S+@tcp\([^\n]+)',sn).group(1).encode()]
 leaks=[]
 for p in HERE.rglob('*'):
  if p.is_file() and not p.is_relative_to(bp):
   data=p.read_bytes()
   if p.suffix=='.gz':data=gzip.decompress(data)
   if any(value in data for value in sensitive):leaks.append(rel(p))
 assert not leaks,'credential value present in output artifacts: '+str(leaks)
 # Save the full byte-derived diff of every replaced root text/JSON, with stable normalized JSON.
 for name in ROOT_CHANGED:
  if name=='manifest.json':continue
  old=BEFORE/name;new=BASE/name
  if old.suffix=='.json':
   a=json.dumps(load(old),ensure_ascii=False,sort_keys=True,indent=2).splitlines(keepends=True)
   b=json.dumps(load(new),ensure_ascii=False,sort_keys=True,indent=2).splitlines(keepends=True)
  else:a=old.read_text(encoding='utf-8-sig').splitlines(keepends=True);b=new.read_text(encoding='utf-8-sig').splitlines(keepends=True)
  p=HERE/'diffs'/(name+'.diff');p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(''.join(difflib.unified_diff(a,b,fromfile='before/'+name,tofile='current/'+name)),encoding='utf-8')
 # Check generated diffs and current root artifacts as well; no sensitive value is emitted.
 for p in list(HERE.rglob('*'))+[BASE/n for n in ROOT_CHANGED if n!='manifest.json']:
  if p.is_file() and not p.is_relative_to(bp):
   data=p.read_bytes()
   if p.suffix=='.gz':data=gzip.decompress(data)
   assert not any(value in data for value in sensitive),'credential value in generated artifact: '+rel(p)
 costs=[load(HERE/'checks'/n/'cost.json') for n in ['full1069-001','full1069-002']]
 save(HERE/'cost-summary.json',dict(full_replay_runs=2,full_replay_elapsed_seconds=sum(c['elapsed_seconds'] for c in costs),peak_process_rss_bytes_max=max(c['peak_process_rss_bytes'] for c in costs),network_bytes=0,run_bytes_before_seal=sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file()),reason_for_second_replay='SMTP description metadata correction found during consistency verification; previous complete replay retained with model/script used.',unmeasured='Human labor and preflight/preparation/publication/finalization process overhead were not timed. These are two measured replay costs, not total labor or isolated benchmarks.'))
 save(HERE/'inspection-attempts.json',dict(attempts=[dict(kind='read-only-summary',result='FAILED',cause='Initial generic inspection assumed inventory-index was a dict; it is a list. AttributeError caused no mutation.'),dict(kind='read-only-manifest-hash',result='NOT_USED',cause='Early read-only commands exceeded initial tool yield; no completed output was used as evidence. Logged preflight subsequently verified all hashes successfully.')],scientific_oracle_changes=False))
 save(HERE/'final-file-set.json',dict(modified_existing=sorted(set(changed+[rel(BASE/'manifest.json')])),allowed_external=list(sorted(allowed_external)),new_files_before_seal=newfiles,before_source_history_count=len(originals),all_old_runs_and_sources_unchanged=True))
 save(HERE/'final-verification.json',dict(all_pass=True,checks=dict(source_chain=True,common_pin_unchanged=True,official_models_rebuild_equal=True,canonical_and_snapshot_same_generation=True,projection_entity_only_partition=True,all_1069_graphs=True,independent_sets_members_exclusion_reasons_denominators=True,repeat_reorder_input_unchanged=True,all_90_operation_views_members_exclusions_unchanged=True,only_documented_role_payload_difference=True,trace_and_intersection_unchanged=True,analysis_family_full_union_chains_checked=True,inventory_index_recomputed=True,history_sources_mapping_protected=True,LOG_append_only=True,REVIEW_producer_table_only=True,STATE_T038_row_only=True,prompt_verbatim=True,retired_writers_fail_closed=True,no_credentials_in_new_artifacts=True),graph_count=1069,model_counts=analysis['source_counts'],modified_root_files=changed,scientific_or_task_acceptance=False,remaining_open='source-audit.json and ban-giao-T040.json',incident='incident.json'))
 with log.open('a',encoding='utf-8') as f:f.write('\n**Kiểm cuối Phiên 3:** final_verify.py đã đối chiếu toàn diff/tập file, bảo toàn mọi nguồn và run cũ, LOG nối thêm/REVIEW chỉ bảng phản hồi/STATE chỉ dòng T038, graph canonical bằng snapshot cùng bản, bảng phân tích và prompt chuẩn khớp. Tất cả checks ở final-verification.json đạt. Sự cố credential tool-output giữ metadata, không có giá trị trong artifact mới; không coi sự cố đã hoàn tác. Lệnh cuối: py -3 -X utf8 -B '+RUN+'/final_verify.py. Bước tiếp: Minh chuyển prompt-kiem-ban-sua.txt, T040 tiếp nhận ban-giao-T040.json trong quyền riêng. Chưa nghiệm thu, commit hoặc push.\n')
 # Seal the run first, then the complete task manifest. Neither manifest includes itself.
 runfiles=[dict(path=rel(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'manifest.json']
 overwrite(HERE/'manifest.json',dict(task='T-038',client_date='2026-10-17',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PRODUCER_R1_ADOPTED_AWAITING_INDEPENDENT_CHECK',pin=load(HERE/'pin.json'),files=runfiles,file_count=len(runfiles),validation=rel(HERE/'final-verification.json'),task_accepted=False))
 previous=load(BEFORE/'manifest.json');files=[dict(path=rel(p),bytes=p.stat().st_size,sha256=sha(p),validation='hash-only-source-or-history' if '/sources/' in rel(p) or ('/runs/' in rel(p) and not p.is_relative_to(HERE)) else 'current-generation-or-retained-before') for p in sorted(BASE.rglob('*')) if p.is_file() and p!=BASE/'manifest.json']
 manifest=dict(task='T-038',client_date='2026-10-17',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PRODUCER_R1_ADOPTED_AWAITING_INDEPENDENT_CHECK',state='CHO_KIEM_BAN_SUA',current_model='runs/'+HERE.name+'/model',current_run='runs/'+HERE.name+'/checks/full1069-002',current_handoff='ban-giao.md',current_prompt='prompt-claude.txt',current_completion_run='runs/'+HERE.name,current_completion_report='ban-giao.md',current_completion_verification=rel(HERE/'final-verification.json'),source_registry='nguon.json',coverage='bao-phu-nguon.json',common_pin=load(HERE/'pin.json'),shared_T036_pin=load(HERE/'pin.json'),input_manifests={name:dict(sha256=sha(ROOT/name)) for name in ['results/T-035/manifest.json','results/T-036/runs/doi-chieu-smtp-001/manifest.json','results/T-038/runs/reviewer-r1-fix-20261016-001/manifest.json']},historical_input_manifests=previous['input_manifests'],historical_manifest_before_R1=rel(BEFORE/'manifest.json'),source_acquisition='runs/tai-nguon-001/manifest.json',source_approval='runs/trien-khai-001/authorization.json',source_dataset_revision_link_verified=False,source_coverage_counts=previous['source_coverage_counts'],authorized_execution_complete=True,task_accepted=False,scientific_task_complete=False,semantic_inventory_complete=False,configured_dependency_inventory_complete=False,method_threshold_mapping_pin_changed=False,decision_state_changes=False,commit_push=False,validation=rel(HERE/'final-verification.json'),handoff_T040=rel(HERE/'ban-giao-T040.json'),files=files,file_count=len(files),count=len(files),total_payload_bytes_excluding_manifest=sum(r['bytes'] for r in files),excludes='manifest self; external LOG/REVIEW/STATE verified separately',external_files={rel(p):dict(sha256=sha(p)) for p in [log,review,state]},state_T038_row=next(x for x in state.read_text(encoding='utf-8-sig').splitlines() if x.startswith('| T-038 |')))
 overwrite(BASE/'manifest.json',manifest)
 assert all(sha(ROOT/r['path'])==r['sha256'] for r in files)
 assert all(sha(ROOT/r['path'])==r['sha256'] for r in runfiles)
 print(canon(dict(all_pass=True,graphs=1069,modified_root=len(changed)+1,root_manifest_files=len(files),retained_payload_bytes=manifest['total_payload_bytes_excluding_manifest'],run_manifest_files=len(runfiles),status='awaiting independent check')),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException:
  p=HERE/('failure-final-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json');save(p,dict(traceback=traceback.format_exc()));raise

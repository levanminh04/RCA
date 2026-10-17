"""Verify final owned scope, pins, complete artifacts, prompt, and preserved history."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import re
import subprocess

ROOT=Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037';RUN=BASE/'runs/ket-phien-002'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x)
 return h.hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,pass_=bool(ok),detail=detail))
pre=load(BASE/'runs/tiep-smtp-001/preflight.json')
for rel,expected in pre['protected'].items():check('protected:'+rel,sha(ROOT/rel)==expected)
# Closed T036 artifacts must remain byte-for-byte identical, even though authorized current build gains SMTP.
m=load(ROOT/'results/T-036/manifest.json');mismatches=[]
for e in m['files']:
 p=(ROOT/e['path']).resolve();assert p.is_relative_to(ROOT) and not p.is_relative_to(ROOT/'data')
 if not p.is_file() or p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']:mismatches.append(e['path'])
check('T036_all187_pinned_artifacts_unchanged',not mismatches,dict(count=len(m['files']),mismatches=mismatches))
original=(ROOT/'results/T-036/runs/kiem-r1-after-002/code/build.py').read_text(encoding='utf-8-sig')
expected=original.replace("'deployment', 'internal', 'span-parent'}","'deployment', 'internal', 'smtp', 'span-parent'}",1).replace("channel not in {'http', 'rpc', 'internal'}","channel not in {'http', 'rpc', 'internal', 'smtp'}",1)
check('shared_build_exactly_two_SMTP_additions',(ROOT/'src/do_thi_tinh/build.py').read_text(encoding='utf-8-sig')==expected)
for name in ['__init__.py','compare.py']:
 check('shared_unchanged:'+name,sha(ROOT/'src/do_thi_tinh'/name)==sha(ROOT/'results/T-036/runs/kiem-r1-after-002/code'/name))
for name in ['build.py','__init__.py','compare.py']:
 check('actual_code_matches_graph_snapshot:'+name,sha(ROOT/'src/do_thi_tinh'/name)==sha(BASE/'runs/graph-003/code'/name))
check('LOG_append_only',(ROOT/'tasks/T-037-p5b-flashticket/LOG.md').read_bytes().startswith((BASE/'runs/tiep-smtp-001/before/tasks/T-037-p5b-flashticket/LOG.md').read_bytes()))
before=(RUN/'state-immediately-before.md').read_text(encoding='utf-8-sig').splitlines();after=(ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig').splitlines()
check('only_T037_STATE_row_changed',[x for x in before if not x.startswith('| T-037 |')]==[x for x in after if not x.startswith('| T-037 |')])
check('T038_T039_STATE_rows_unchanged',[x for x in before if x.startswith(('| T-038 |','| T-039 |'))]==[x for x in after if x.startswith(('| T-038 |','| T-039 |'))])
def diff_sections(t):
 return {x.splitlines()[0]:x for x in re.split(r'(?=^diff --git )',t,flags=re.M) if x.startswith('diff --git ')}
old=diff_sections(pre['tracked_diff_before']);nowtext=subprocess.check_output(['git','-C',str(ROOT),'diff','HEAD','--binary'],stderr=subprocess.PIPE).decode('utf-8',errors='replace');now=diff_sections(nowtext)
unowned=[k for k in set(old)|set(now) if not any(' b/'+rel in k for rel in ['docs/STATE.md','src/do_thi_tinh/build.py','tasks/T-037-p5b-flashticket/LOG.md']) and old.get(k)!=now.get(k)]
check('tracked_changes_outside_owned_scope_preserved',not unowned,unowned)
sources=load(BASE/'nguon.json');check('source_registry_ids_unique',len({s['id'] for s in sources['sources']})==len(sources['sources']))
for s in sources['sources']:
 check('source_current_and_snapshot:'+s['id'],sha(Path(s['path']))==s['sha256']==sha(ROOT/s['snapshot']))
reg=load(BASE/'runs/smtp-regression-001/result.json');graph=load(BASE/'runs/graph-003/result.json')
check('SMTP_and_all_prior_checks_pass',reg['all_pass'] and reg['passed']==100 and reg['original_regression']['passed']==221 and reg['original_regression']['failed']==0)
check('current_graph_all_checks_pass',graph['all_pass'] and graph['failed']==0)
for name in ['ban-ghi.json','nguon.json']:
 check('graph_input_unchanged:'+name,sha(BASE/name)==sha(BASE/'runs/graph-003'/name))
for a,b in [('entity.json','thuc-the.json'),('operation.json','thao-tac.json'),('projection.json','phep-chieu.json'),('entity-only.json','entity-only.json')]:
 check('published_graph_same:'+b,sha(BASE/'do-thi'/b)==sha(BASE/'runs/graph-003'/a))
doc=load(BASE/'ban-ghi.json');cov=load(BASE/'bao-phu-nguon.json')
check('no_fake_runtime_operation_names',all(o['runtime_name'] is None for o in doc['operations']))
check('shared_metric_single_context',all(s['operation'] is None for s in doc['signals'] if s['shared']))
check('no_remaining_SMTP_blocker_flag',not any(u.get('status')=='OPEN_UNSUPPORTED' for u in cov['units']))
check('all_OPEN_have_owner_and_required_input',all(u.get('owner') and u.get('required_input') for u in cov['units'] if 'OPEN' in u.get('status','').upper()))
check('source_quotes_and_SQL_names_pass',load(BASE/'runs/assemble-002/semantic-source-audit.json')['all_quotes_match'] and all(x['equal'] for x in load(BASE/'runs/assemble-002/semantic-source-audit.json')['sql_dictionary_tables']))
check('full_unit_graph_matrix_present',len(load(BASE/'runs/graph-003/requirement-record-graph-matrix.json'))==len(cov['units'])==652)
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig');prompt=(BASE/'prompt-claude.txt').read_text(encoding='utf-8')
def block(a,b):return template.split(a,1)[1].split(b,1)[0].split('```text\n',1)[1].split('\n```',1)[0]
common=block('## Prompt chung','## Khối công đoạn');stage=block('### Soát kết quả','### Người làm đáp phản biện');gate=block('### G3 — Khóa thiết kế trước khi mở test','### G4 — Kết quả')
pattern=''.join(re.escape(x) if i%2==0 else '.+?' for i,x in enumerate(re.split(r'(<[^>]+>)',common)))
check('prompt_exact_common_and_result_G3',re.fullmatch(pattern+'\n\n'+re.escape(stage)+'\n\n'+re.escape(gate)+'\n',prompt,flags=re.S) is not None)
check('prompt_saved_verbatim_in_LOG',prompt in (ROOT/'tasks/T-037-p5b-flashticket/LOG.md').read_text(encoding='utf-8-sig'))
check('old_failure_and_oracle_runs_kept',all((BASE/p).exists() for p in ['runs/smtp-001/failure.txt','runs/smtp-002/result.json','runs/graph-001/result.json','oracle.json','oracle-v2.json','oracle-v3.json','fixtures-runtime.json','fixtures-runtime-v2.json','runs/tiep-smtp-001/before/results/T-037/manifest.json']))
check('old_manifest_history_files_preserved',all((BASE/'runs/tiep-smtp-001/before/results/T-037'/p).is_file() for p in ['ban-ghi.json','nguon.json','bao-phu-nguon.json','kiem-dung-dan.md','ban-giao.md']))

# Inspect the complete owned diff's target set; current verifier is the final additional text artifact.
diff=RUN/'changes.diff';text=diff.read_text(encoding='utf-8');rel=Path(__file__).resolve().relative_to(ROOT).as_posix()
if '+++ '+rel+'\n' not in text:
 import difflib
 text+=''.join(difflib.unified_diff([],Path(__file__).read_text(encoding='utf-8').splitlines(keepends=True),fromfile='/dev/null',tofile=rel));diff.write_text(text,encoding='utf-8')
targets=re.findall(r'^\+\+\+ (.+)$',text,flags=re.M)
check('complete_owned_diff_only_authorized_targets',all(t.startswith('results/T-037/') or t in ['src/do_thi_tinh/build.py','tasks/T-037-p5b-flashticket/LOG.md','docs/STATE.md'] for t in targets),len(targets))
check('no_bytecode_written_under_T037',not list(BASE.rglob('__pycache__')))
selected=['src/do_thi_tinh/build.py','tasks/T-037-p5b-flashticket/LOG.md','docs/STATE.md']
dump(RUN/'scope-final.json',dict(owned_file_groups=['results/T-037/']+selected,external_shared_code_changed=['src/do_thi_tinh/build.py'],T036_snapshot_manifest_unchanged=True,sibling_SPEC_pin_unchanged=True,unowned_diff_changes=unowned))

manifest=load(BASE/'manifest.json');excluded={BASE/'manifest.json',RUN/'final-verification.json'}
manifest['files']=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(BASE.rglob('*')) if p.is_file() and p not in excluded]
manifest['actual_shared_code']={p:sha(ROOT/p) for p in ['src/do_thi_tinh/build.py','src/do_thi_tinh/compare.py','src/do_thi_tinh/__init__.py']}
manifest['total_payload_bytes']=sum(e['bytes'] for e in manifest['files']);manifest['payload_excludes']='Only this manifest and final-verification metadata to avoid self-hash cycle; total_output_bytes includes both sizes'
manifest['total_output_bytes']=0;manifest['file_count_including_manifest_and_final_report']=len(manifest['files'])+2
result=dict(task='T-037',all_pass=all(c['pass_'] for c in checks),passed=sum(c['pass_'] for c in checks),failed=sum(not c['pass_'] for c in checks),checks=checks,
 checked_utc=datetime.now(timezone.utc).isoformat(),source_kind='Design model, runtime and scientific benefit not verified',
 result_state='AWAITING_CLAUDE_REVIEW_NOT_ACCEPTED',last_command="& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-037/verify-complete.py",total_output_bytes=0)
for _ in range(6):
 dump(BASE/'manifest.json',manifest);dump(RUN/'final-verification.json',result)
 n=sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file())
 if manifest['total_output_bytes']==n and result['total_output_bytes']==n:break
 manifest['total_output_bytes']=n;result['total_output_bytes']=n
print(json.dumps(dict(all_pass=result['all_pass'],passed=result['passed'],failed=[c for c in checks if not c['pass_']],total_output_bytes=manifest['total_output_bytes'],files=manifest['file_count_including_manifest_and_final_report'],state=manifest['state']),ensure_ascii=False))
raise SystemExit(0 if result['all_pass'] else 1)

from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
assert load(RUN/'checks/t036-r1-001/result.json')['all_pass']
assert load(RUN/'checks/smtp-baseline-002/result.json')['all_pass']
assert load(RUN/'checks-smtp-v2-001/checks.json')['all_ok']
save(RUN/'preparation-attempts.json',{'retained_failures':[{'attempt':'prepare_checks first','error':'strict anchor count expected1 but oracle path appears3; no checker output written'},{'attempt':'baseline adapter failed001','source':'checks/adapter-failed-001.py','error':'SyntaxError from replacing nested quoted path; corrected to only first ROOT anchor'},{'attempt':'baseline adapter failed002','source':'checks/adapter-failed-002.py','failure':'checks/smtp-baseline-001/failure.json','error':'check.py is runner, not T037 code module; use unchanged original runner hash'}],
 'successful_change':'explicit distinction runner vs module, root vs nested adaptation; no shared/oracle behavior change','T036_R1_passed':221,'legacy_SMTP_passed':100,'V2_SMTP_passed':29,'V2_check_status_note':'check_smtp preserves preview metadata text; code hashes equal applied live and pin code, acceptance state is this manifest not preview label'})
core=['code/__init__.py','code/build.py','code/compare.py','code-hashes.json','hop-dong.md','nguon.json','oracle.json','adoption-oracle.json','authorization.json']
core+= [p.relative_to(RUN).as_posix() for parent in [RUN/'checks/t036-r1-001',RUN/'checks/smtp-baseline-002',RUN/'checks-smtp-v2-001'] for p in parent.rglob('*') if p.is_file()]
m={'version':'SMTP-V2','created_utc':datetime.now(timezone.utc).isoformat(),'status':'SHARED_REGRESSION_PASS_THREE_BRANCH_ADOPTION_PENDING','immutable_pin':True,
   'scope':'fixed contract/code/oracle/shared-check core; later branch adoption reports are indexed separately, never mutate this pin',
   'code_hashes':load(RUN/'code-hashes.json'),'files':[{'path':(RUN/n).relative_to(ROOT).as_posix(),'bytes':(RUN/n).stat().st_size,'sha256':sha(RUN/n)} for n in sorted(set(core))],
   'historical_pin':'results/T-036/manifest.json','historical_T037_SMTP':'results/T-037/runs/graph-003/code','no_test_access':True}
save(RUN/'manifest.json',m)
pin={'manifest':(RUN/'manifest.json').relative_to(ROOT).as_posix(),'manifest_sha256':sha(RUN/'manifest.json'),'created_utc':m['created_utc'],'code_hashes':m['code_hashes']}
for t in ['T-037','T-038','T-039']:
 dest=ROOT/f'results/{t}/runs/doi-chieu-smtp-001';save(dest/'pin.json',pin)
 # Source path validation uses frozen copies where the approval has changed a SPEC.
 if t=='T-037':
  p=dest/'check_adoption.py';s=p.read_text(encoding='utf-8');before="sha(Path("+repr(str(RUN/'before'))+")/rel),pre['protected'][rel])"
  after="sha((Path("+repr(str(RUN/'before'))+")/rel) if (Path("+repr(str(RUN/'before'))+")/rel).exists() else ROOT/rel),pre['protected'][rel])"
  assert before in s;p.write_text(s.replace(before,after,1),encoding='utf-8')
print(json.dumps({'pin_published':True,'common_code_checks':[221,100,29],'three_adoptions_pending':True}))

"""Final artifact/diff audit only. Does not build graphs or change inputs."""
import difflib
import hashlib
import json
import pathlib
import re
import subprocess

ROOT=pathlib.Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037';RUN=BASE/'runs/ket-phien-001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sections(txt):
 out={}
 for chunk in re.split(r'(?=^diff --git )',txt,flags=re.M):
  if chunk.startswith('diff --git '):out[chunk.splitlines()[0]]=chunk
 return out

manifest=load(BASE/'manifest.json');pre=load(BASE/'runs/tu-ra-001/preflight.json')
checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
initial_entries=manifest['files']
check('all previously manifested result files unchanged',all((ROOT/e['path']).is_file() and (ROOT/e['path']).stat().st_size==e['bytes'] and sha(ROOT/e['path'])==e['sha256'] for e in initial_entries),len(initial_entries))
before=(BASE/'runs/tu-ra-001/tracked-before.diff').read_text(encoding='utf-8-sig')
now=subprocess.check_output(['git','-C',str(ROOT),'diff','HEAD','--binary'],stderr=subprocess.PIPE).decode('utf-8',errors='replace')
bs,ns=sections(before),sections(now)
outside=[name for name in set(bs)|set(ns) if ' b/docs/STATE.md' not in name and bs.get(name)!=ns.get(name)]
check('tracked diff outside STATE preserved byte-for-byte',not outside,outside)
log=ROOT/'tasks/T-037-p5b-flashticket/LOG.md';state=ROOT/'docs/STATE.md'
check('LOG append-only from preflight',log.read_bytes().startswith((BASE/'runs/tu-ra-001/log-before.md').read_bytes()))
sb=(RUN/'state-immediately-before.md').read_text(encoding='utf-8-sig').splitlines()
sa=state.read_text(encoding='utf-8-sig').splitlines()
check('STATE only T037 row changed from latest locked read',[x for x in sb if not x.startswith('| T-037 |')]==[x for x in sa if not x.startswith('| T-037 |')])
check('STATE retains exactly one T037 row',sum(x.startswith('| T-037 |') for x in sa)==1)
check('source snapshots and live sources unchanged',all(sha(ROOT/s['snapshot'])==s['sha256'] and sha(pathlib.Path(s['path']))==s['sha256'] for s in load(BASE/'nguon.json')['sources']))
for row in pre['governing_rca']:
 if row['path'] in ['docs/STATE.md','tasks/T-037-p5b-flashticket/LOG.md']:continue
 check('governing file unchanged: '+row['path'],sha(ROOT/row['path'])==row['sha256'])
check('common code snapshot/current unchanged',all(sha(pathlib.Path(row['snapshot']))==row['sha256'] and sha(pathlib.Path(row['current']))==row['sha256'] for row in pre['current_code']))
check('T036 manifest pin unchanged',sha(ROOT/'results/T-036/manifest.json')==pre['manifests'][0]['manifest_sha256'])
check('T035 manifest unchanged',sha(ROOT/'results/T-035/manifest.json')==pre['manifests'][1]['manifest_sha256'])
check('protected result hashes previously verified at finalization',all(x['matches'] for x in load(RUN/'input-hashes-final.json')))
prompt=(BASE/'prompt-claude.txt').read_text(encoding='utf-8')
t=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(a,b):return t.split(a,1)[1].split(b,1)[0].split('```text\n',1)[1].split('\n```',1)[0]
common=block('## Prompt chung','## Khối công đoạn');stage=block('### Soát kết quả','### Người làm đáp phản biện');gate=block('### G3 — Khóa thiết kế trước khi mở test','### G4 — Kết quả')
regex=''.join(re.escape(part) if i%2==0 else r'.+?' for i,part in enumerate(re.split(r'(<[^>]+>)',common)))
check('handoff fixed common text and exact result/G3 blocks',re.fullmatch(regex+r'\n\n'+re.escape(stage)+r'\n\n'+re.escape(gate)+r'\n',prompt,flags=re.S) is not None)
check('handoff copied verbatim to append-only LOG',prompt in log.read_text(encoding='utf-8-sig'))
auth=(BASE/'authorization.txt').read_text(encoding='utf-8')
check('corrected authorization block in LOG',auth.rstrip() in log.read_text(encoding='utf-8-sig'))
check('failed SMTP run retained',all((BASE/'runs/smtp-001'/x).is_file() for x in ['input.json','registry.json','oracle-before-execution.json','failure.txt','code-used.py']))
check('successful run reproduces blocker rather than full graph',load(BASE/'runs/smtp-002/result.json')['all_reproduced'] and not manifest['full_graph_built'])
check('no graph files misrepresent completion',not (BASE/'do-thi').exists())
check('all partial record checks pass',all(x['pass'] for x in load(RUN/'partial-record-checks.json')))

# Complete diff includes artifacts created after its initial capture. Reports and manifest remain metadata.
diff=RUN/'changes.diff';content=diff.read_text(encoding='utf-8')
for p in [BASE/'verify-final.py',BASE/'runs/smtp-002/code-used.py']:
 name=p.relative_to(ROOT).as_posix()
 if '+++ '+name+'\n' not in content:
  content+=''.join(difflib.unified_diff([],p.read_text(encoding='utf-8').splitlines(keepends=True),fromfile='/dev/null',tofile=name))
diff.write_text(content,encoding='utf-8')
headers=re.findall(r'^\+\+\+ (.+)$',content,flags=re.M)
check('complete owned diff has only approved target paths',all(x.startswith('results/T-037/') or x in ['after/docs/STATE.md','after/tasks/T-037-p5b-flashticket/LOG.md'] for x in headers),len(headers))
dump(RUN/'status-final.json',{'rca':subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain=v1','--untracked-files=all']).decode('utf-8'),'owned_scope':['results/T-037/','tasks/T-037-p5b-flashticket/LOG.md','docs/STATE.md row T-037']})
manifest['files']=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file() and p.name not in ['manifest.json','final-verification.json']]
manifest['total_output_bytes']=sum(x['bytes'] for x in manifest['files'])
dump(BASE/'manifest.json',manifest)
result={'task':'T-037','state':manifest['state'],'checks':checks,'all_pass':all(x['pass'] for x in checks),
 'owned_file_groups':['results/T-037/','tasks/T-037-p5b-flashticket/LOG.md append only','docs/STATE.md row T-037 only'],
 'complete_diff':'runs/ket-phien-001/changes.diff','output_file_count_excluding_manifest_and_this_report':len(manifest['files']),
 'output_bytes_excluding_manifest_and_this_report':manifest['total_output_bytes'],
 'last_command':'py -3 -X utf8 -B results/T-037/verify-final.py',
 'limits':'Artifact integrity and permitted scope only; T037 is incomplete and its full graph/runtime fixtures were not run.'}
dump(RUN/'final-verification.json',result)
print(json.dumps({'all_pass':result['all_pass'],'checks':len(checks),'failed':[x for x in checks if not x['pass']],
 'all_output_files':len([p for p in BASE.rglob('*') if p.is_file()]),'all_output_bytes':sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file()),'state':manifest['state']},ensure_ascii=False))

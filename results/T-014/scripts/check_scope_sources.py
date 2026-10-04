"""Check source revisions/hashes and enumerate only owned mutations."""
import hashlib,json,subprocess,importlib.util
from pathlib import Path
repo=Path('D:/RCA-flashticket');out=repo/'results/T-014'
def git(base,*args):return subprocess.check_output(['git','-C',str(base),*args],text=True).strip()
sources={'CIRCA':Path('D:/RCA-ext/work/T-014/CIRCA'),'RCAEval':Path('D:/RCA-ext/src/RCAEval')}
expected=json.loads((out/'paper/source-manifest.json').read_text())
checks={key:dict(path=str(base),HEAD=git(base,'rev-parse','HEAD'),expected=expected[key+'_revision'],tracked_diff=git(base,'diff','--name-only')) for key,base in sources.items()}
for c in checks.values():c['revision_matches']=c['HEAD']==c['expected'];c['tracked_source_unchanged']=not c['tracked_diff']
source_files=[]
for row in expected['files']:
    p=Path(row['duong_dan']);actual=hashlib.sha256(p.read_bytes()).hexdigest()
    source_files.append(dict(path=str(p),sha256=actual,matches_saved=actual==row['sha256']))
causal=Path(importlib.util.find_spec('causallearn').origin).parent
sklearn=Path(importlib.util.find_spec('sklearn').origin).parent
libraries={causal:['search/ConstraintBased/PC.py','utils/PCUtils/SkeletonDiscovery.py','utils/cit.py','graph/GraphClass.py'],sklearn:['linear_model/_base.py','preprocessing/_data.py','utils/extmath.py']}
library_files=[dict(path=str(base/rel),sha256=hashlib.sha256((base/rel).read_bytes()).hexdigest()) for base,rels in libraries.items() for rel in rels]
diff=git(repo,'diff','--name-only');untracked=git(repo,'ls-files','--others','--exclude-standard')
owned=[s for s in untracked.splitlines() if s.startswith(('results/T-014/','tasks/T-014-ho-so-circa/','src/circa_kien_truc/'))]
other=[s for s in untracked.splitlines() if s not in owned]
state=json.loads((out/'runs/state-updates.jsonl').read_text(encoding='utf-8-sig').splitlines()[-1])
report=dict(source_checks=checks,source_file_checks=source_files,pinned_library_file_hashes=library_files,current_repo_HEAD=git(repo,'rev-parse','HEAD'),base_HEAD='93f13d4c4a966428177e2acc287d96bc89303e92',owned_untracked_count=len(owned),other_sessions_untracked_count=len(other),tracked_changed_files=diff.splitlines(),last_state_update_preserves_other_bytes=state['preserved_other_bytes'],pass_=all(c['revision_matches'] and c['tracked_source_unchanged'] for c in checks.values()) and all(c['matches_saved'] for c in source_files),scope_warning='Current git status includes independent sessions. It does not identify their mutations as T014. Full T014 outputs also include outside-work/env/EC2 inventory, not only git diff.')
(out/'runs/scope-and-sources.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(pass_=report['pass_'],owned_untracked_count=len(owned),other_sessions_untracked_count=len(other),tracked_changed_files=report['tracked_changed_files'])))
assert report['pass_']

"""Check preservation/deltas and seal the metadata revision. No test source I/O."""
import ast
import difflib
import json
from pathlib import Path
from activate import ROOT,RUN,pin
from bien_nhan import atomic,digest,read_pin,Blocked


def changes(a,b,path=''):
    if type(a)!=type(b):return [dict(path=path,before=a,after=b)]
    if isinstance(a,dict):
        rows=[]
        for k in sorted(set(a)|set(b)):
            q=path+'/'+str(k).replace('~','~0').replace('/','~1')
            if k not in a:rows.append(dict(path=q,added=b[k]))
            elif k not in b:rows.append(dict(path=q,removed=a[k]))
            else:rows.extend(changes(a[k],b[k],q))
        return rows
    if isinstance(a,list)and len(a)==len(b):return [row for i,(x,y)in enumerate(zip(a,b))for row in changes(x,y,path+'/'+str(i))]
    return []if a==b else [dict(path=path,before=a,after=b)]


def main():
    base=RUN/'pre-review-001';old=read_pin(pin(base/'manifest.json'));preserved=read_pin(pin(base/'preservation.json'))['preserved_paths']
    assert digest(base/'manifest.json')=='3dac84b5346e05ad6a2ad3d1a647313afa0bf4a9f0fa27baa1538dbfd2008b0b'
    n=0
    for rel,meta in {**old['outputs'],**old['reviewed_documents']}.items():
        path=ROOT/(preserved[rel]['path']if rel in preserved else rel)
        assert path.stat().st_size==meta['bytes']and digest(path)==meta['sha256'],rel;n+=1
    atomic(RUN/'preservation-check.json',dict(PASS=True,original_files_checked=n,
           original_manifest=pin(base/'manifest.json'),mapping=pin(base/'preservation.json'),original_reviewed_bytes_kept=True))
    import main as launch
    try:launch.main(pin(RUN/'grant-template.json'))
    except Blocked as exc:assert str(exc)=='WAIT_MINH_FINAL_013_G3_SOURCE_TRANSFER_MAIN_SCORE'
    else:raise AssertionError('false grant entered main')
    for host in ('ec2_1','ec2_2'):assert read_pin(pin(RUN/(host+'-after-review-environment.json')))['PASS']
    revision=read_pin(pin(RUN/'metadata-revision-check.json'));assert revision['PASS']and revision['code_unchanged']==106
    manifest_rels=set(old['outputs'])
    delta={};text_patch=[]
    excluded=('manifest.json','commit-files.json','complete-preparation-diff.patch','final-root-change-list.json','diff-check.json','scope-and-code-self-check.json')
    for rel,copy in preserved.items():
        after=ROOT/rel;before=ROOT/copy['path']
        if not after.is_file()or after.name in excluded:continue
        if digest(after)==copy['sha256']:continue
        if after.suffix=='.json':
            delta[rel]=changes(json.loads(before.read_bytes()),json.loads(after.read_bytes()))
        elif after.suffix in ('.md','.py'):
            text_patch.extend(difflib.unified_diff(before.read_text(encoding='utf-8').splitlines(True),after.read_text(encoding='utf-8').splitlines(True),fromfile='reviewed/'+rel,tofile=rel))
    atomic(RUN/'metadata-after-review.json',dict(changed_json_files=delta,
          note='Complete JSON semantic delta for preserved metadata; new evidence files are listed by the new manifest'))
    (RUN/'metadata-after-review.patch').open('x',encoding='utf-8').writelines(text_patch)
    before_pins=read_pin(pin(RUN/'before-pins.json'));full=[];rootchanges={};issues=[]
    for rel,meta in before_pins.items():
        prior=RUN/'before'/rel;current=ROOT/rel
        oldlines=prior.read_text(encoding='utf-8').splitlines(True);newlines=current.read_text(encoding='utf-8').splitlines(True)
        full.extend(difflib.unified_diff(oldlines,newlines,fromfile='before/'+rel,tofile=rel))
        for tag,i,j,k,l in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
            if tag in ('replace','insert'):
                for index in range(k,l):
                    s=newlines[index].rstrip('\r\n')
                    if s.rstrip(' \t')!=s:issues.append([rel,index+1])
        if rel.endswith(('LOG.md','DECISIONS.md','WHY.md')):assert current.read_bytes().startswith(prior.read_bytes())
        rootchanges[rel]=dict(before=meta,after=pin(current))
    assert not issues,issues
    # These old derived ledgers were preserved under pre-review-001 before replacement.
    (RUN/'complete-preparation-diff.patch').write_text(''.join(full),encoding='utf-8',newline='')
    (RUN/'final-root-change-list.json').write_text(json.dumps(rootchanges,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (RUN/'diff-check.json').write_text(json.dumps(dict(PASS=True,files=len(rootchanges),issues=issues,method='new logical lines only; CRLF/LF bytes retained'))+'\n',encoding='utf-8')
    parsed=0
    for p in RUN.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'));parsed+=1
    atomic(RUN/'after-review-self-check.json',dict(PASS=True,AST_scripts=parsed,core_code_unchanged=106,
         grant_entry_blocked=True,original_files_preserved=n,new_method_runs=0,raw_test_payloads_read=False,
         metadata=pin(RUN/'metadata-revision-check.json'),delta=pin(RUN/'metadata-after-review.json')))
    candidates=list(before_pins);excluded_files=[]
    for p in RUN.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(ROOT).as_posix()
        if p.suffix in ('.py','.json','.md','.patch','.txt','.jsonl')and'.partial'not in p.name:candidates.append(rel)
        else:excluded_files.append(rel)
    candidates += [(RUN/name).relative_to(ROOT).as_posix()for name in ('manifest.json','commit-files.json')]
    atomic(RUN/'commit-files.json',dict(candidates=sorted(set(candidates)),excluded_kept_in_place=sorted(excluded_files),approved=False,
           note='Only a proposal; inspect pre-existing unstaged dependencies/hunks before any commit'))
    outputs={}
    for p in sorted(RUN.rglob('*')):
        if p.is_file()and p!=RUN/'manifest.json':outputs[p.relative_to(ROOT).as_posix()]=dict(bytes=p.stat().st_size,sha256=digest(p))
    code=read_pin(pin(RUN/'code-pins.json'))['code_pins']
    for rel,sha in code.items():
        p=ROOT/rel;assert digest(p)==sha;outputs[rel]=dict(bytes=p.stat().st_size,sha256=sha)
    docs={rel:dict(bytes=(ROOT/rel).stat().st_size,sha256=digest(ROOT/rel))for rel in before_pins if not rel.endswith('.py')}
    external=read_pin(pin(RUN/'local-external-code-pins.json'))['files']
    ext={rel:dict(bytes=m['bytes'],sha256=m['sha256'])for rel,m in external.items()}
    atomic(RUN/'manifest.json',dict(schema='T054-CHECKPOINT013-POST-REVIEW-1',outputs=outputs,reviewed_documents=docs,
          local_external_code=ext,immutable_output_count=len(outputs),previous_reviewed_manifest=pin(base/'manifest.json'),
          preservation=pin(RUN/'preservation-check.json'),raw_test_payloads_in_this_package=False,
          note='Metadata revision after Claude review. Code/slots/config/seed/source/window/env unchanged; prior bytes and all failed attempts retained. No G3/main grants.'))
    print(json.dumps(dict(PASS=True,outputs=len(outputs),documents=len(docs),external=len(ext),preserved=n,core_code_unchanged=len(code))))


if __name__=='__main__':main()

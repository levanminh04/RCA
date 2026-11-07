"""Include nested fixture manifests while retaining the first manifest and ledger."""
import ast
from activate import ROOT,RUN,pin
from bien_nhan import atomic,digest,read_pin


def main():
    previous=read_pin(pin(RUN/'manifest-history-001/manifest.json'))
    before=read_pin(pin(RUN/'before-pins.json'))
    files=[p for p in RUN.rglob('*')if p.is_file()]
    selected=list(before);excluded=[]
    for p in files:
        rel=p.relative_to(ROOT).as_posix()
        if p.suffix in ('.py','.json','.md','.patch','.txt','.jsonl')and '.partial'not in p.name:selected.append(rel)
        else:excluded.append(rel)
    selected += [(RUN/name).relative_to(ROOT).as_posix()for name in ('manifest.json','commit-files.json')]
    atomic(RUN/'commit-files.json',dict(candidates=sorted(set(selected)),excluded_kept_in_place=sorted(excluded),
          scope='delta013 proposal only; inspect unstaged baseline dependencies before any commit',approved=False))
    outputs={}
    for p in sorted(RUN.rglob('*')):
        if p.is_file()and p!=RUN/'manifest.json':outputs[p.relative_to(ROOT).as_posix()]=dict(bytes=p.stat().st_size,sha256=digest(p))
    code=read_pin(pin(RUN/'code-pins.json'))['code_pins']
    for rel,sha in code.items():
        p=ROOT/rel;assert digest(p)==sha;outputs[rel]=dict(bytes=p.stat().st_size,sha256=sha)
    reviewed={rel:dict(bytes=(ROOT/rel).stat().st_size,sha256=digest(ROOT/rel))for rel in before if not rel.endswith('.py')}
    external=read_pin(pin(RUN/'local-external-code-pins.json'))['files']
    for rel,meta in external.items():assert digest(__import__('pathlib').Path(rel))==meta['sha256']
    for p in RUN.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
    manifest=dict(previous,outputs=outputs,reviewed_documents=reviewed,
          local_external_code={rel:dict(bytes=m['bytes'],sha256=m['sha256'])for rel,m in external.items()},
          immutable_output_count=len(outputs),
          sealing_note='Included both nested generated-fixture manifests; first manifest/finalizer/list retained under manifest-history-001. No code/data/method result changed.')
    atomic(RUN/'manifest.json',manifest)
    print(__import__('json').dumps(dict(PASS=True,outputs=len(outputs),documents=len(reviewed),external=len(external))))


if __name__=='__main__':main()

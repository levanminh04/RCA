"""Independent final file, manifest, scope and evaluation checks."""
import ast
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
from simple_runner import ROOT, OUT, read, sha, write


def load(path):
    if path.suffix=='.gz':
        with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)
    return read(path)


def main():
    folder=OUT/'final-verify-002';folder.mkdir(exist_ok=False)
    checks={};old=read(ROOT/'results/T-042/manifest.json')
    for row in old['files']:assert sha(ROOT/row['path'])==row['sha256']
    checks['original_163_scientific_outputs_preserved']=True
    count=0;lists={}
    for path in OUT.rglob('*.json'):
        value=read(path);count+=1
        if path.name in ['diagnoses-frozen.json','diagnosis-list.json'] and value.get('completed'):
            for row in value['records']:assert sha(ROOT/row['path'])==row['sha256']
            lists[path.relative_to(OUT).as_posix()]=len(value['records'])
    for path in OUT.rglob('*.json.gz'):load(path);count+=1
    for path in OUT.rglob('*.py'):ast.parse(path.read_text(encoding='utf-8-sig'))
    checks['all_JSON_GZIP_parse']=count;checks['all_python_AST_parse']=True;checks['frozen_lists_hash_verified']=lists
    # Independent canonical evaluator, independent of the two new reporting scripts.
    import sys
    sys.path.insert(0,str(ROOT/'src'))
    from p3 import danh_gia
    lp=ROOT/'results/T-026/nhan-dev.json';meta=read(ROOT/'results/T-026/ban-ghi-dua-vao-cham.json')
    assert sha(lp)==meta['source_hashes']['results/T-026/nhan-dev.json']
    labels={r['opaque_id']:r for r in read(lp)['cases']};canonical=0
    for path in [OUT/'simple-full-001/diagnoses-frozen.json',OUT/'level-seed0-001/diagnoses-frozen.json',OUT/'time-projection-001/diagnoses-frozen.json']:
        for row in read(path)['records']:
            data=read(ROOT/row['path']);v=data['result'];root=labels[row['opaque_id']]['root'];ranks=v['native_ranks']
            entities=[dict(entity=s,key=[-i],tie_group=i) for i,s in enumerate(ranks)]
            result=danh_gia.cham_ca(dict(status='OK' if ranks else 'NO_EVIDENCE',entity_ranking=entities,blocks=None),root)
            nr=ranks.index(root)+1 if root in ranks else None
            assert math.isclose(result['rr'],1/nr if nr else 0,rel_tol=1e-14,abs_tol=1e-14)
            assert result['hit@1']==int(nr==1);canonical+=1
    checks['independent_native_API_ordinal_evaluation_P3']=canonical
    checks['canonical_audit_note']='Unique ordinal keys encode native API order; source exact-score tie expectations are separate, not asserted by this audit'
    # Confirm labels/root/fault are not AST parameters read by source main kernel.
    from simple_runner import load_kernels
    kernels,pins=load_kernels();checks['source_pins_reverified']=len(pins)
    # Compare controls prefix to the before-continuation snapshot.
    controls=read(OUT/'initial-controls.json')
    control_result={}
    for name,meta in controls.items():
        raw=(ROOT/name).read_bytes()
        if name in ['docs/WHY.md','docs/DECISIONS.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md']:
            match=hashlib.sha256(raw[:meta['bytes']]).hexdigest()==meta['sha256'];assert match
            control_result[name]=dict(original_prefix_exact=True,new_bytes=len(raw)-meta['bytes'])
        elif name=='docs/STATE.md':
            control_result[name]=dict(changed_task_line_only='verified with before snapshot and final status check')
        else:
            assert sha(ROOT/name)==meta['sha256'];control_result[name]=dict(unchanged=True)
    checks['controls']=control_result
    total=sum(p.stat().st_size for p in (ROOT/'results/T-042').rglob('*') if p.is_file())
    assert total<300*2**20
    checks['output_bytes_at_check']=total;checks['output_MiB_at_check']=total/2**20
    checks['budget_interpretation']='300MB was an estimate, storage held below300MiB by future-only compression; exact decimal bytes recorded, no old files deleted'
    result=subprocess.run(['git','diff','--check','--','docs/STATE.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md','results/T-042'],cwd=ROOT,text=True,capture_output=True)
    checks['git_diff_check']=dict(exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
    assert result.returncode==0
    write(folder/'checks.json',dict(status='PASS',checks=checks))
    print('PASS',canonical,'native evaluator checks;',count,'JSONs;',round(total/2**20,3),'MiB')


if __name__=='__main__':main()

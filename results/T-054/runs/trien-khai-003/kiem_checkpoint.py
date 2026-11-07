"""Kiểm toàn bộ checkpoint, giới hạn quyền và bảo toàn lịch sử; không chạy method."""
import argparse
import ast
import hashlib
import json
import tarfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=OUT/'runs/trien-khai-003'

def load(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,pin):
    assert p.is_file(),('missing',str(p))
    expected=pin if isinstance(pin,str) else pin['sha256']
    assert sha(p)==expected,('hash',str(p))
    if isinstance(pin,dict) and 'bytes'in pin:assert p.stat().st_size==pin['bytes'],('bytes',str(p))

def validate():
    before=load(RUN/'before.json')['files']
    allowed={'docs/STATE.md','tasks/T-054-khoa-g3-chay-p7-a/LOG.md','tasks/T-054-khoa-g3-chay-p7-a/SPEC.md'}
    allowed.update('results/T-054/'+name for name in ['authorization.json','environment.json','ho-so-g3.md',
        'matrix.json','pilot-plan.json','protocol.json','reuse.json','runbook.md','source-manifest.json'])
    allowed.update(p.relative_to(ROOT).as_posix() for p in (OUT/'scripts').glob('*.py'))
    changed=[]
    for relative,pin in before.items():
        path=ROOT/relative;assert path.is_file(),('removed',relative)
        if sha(path)!=pin['sha256']:
            assert relative in allowed,('scope',relative);changed.append(relative)
    old=before['tasks/T-054-khoa-g3-chay-p7-a/LOG.md'];raw=(ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').read_bytes()
    assert hashlib.sha256(raw[:old['bytes']]).hexdigest()==old['sha256'],'LOG prefix'
    a=(RUN/'STATE-before.txt').read_bytes();check(RUN/'STATE-before.txt',before['docs/STATE.md'])
    b=(ROOT/'docs/STATE.md').read_bytes();old_lines=a.splitlines(keepends=True);new_lines=b.splitlines(keepends=True)
    assert len(old_lines)==len(new_lines)
    diffs=[(x,y)for x,y in zip(old_lines,new_lines)if x!=y]
    assert len(diffs)==1 and all(x.startswith('- **T-054 —'.encode())for x in diffs[0]),'STATE outside row'
    source=load(OUT/'source-manifest.json')
    assert len(source['own_scripts'])==9 and len(source['legacy_code'])==93
    for section in ('own_scripts','legacy_code'):
        for relative,pin in source[section].items():check(ROOT/relative,pin)
    for p in (OUT/'scripts').glob('*.py'):ast.parse(p.read_bytes(),filename=str(p))
    protocol=load(OUT/'protocol.json');doc=dict(protocol);fingerprint=doc.pop('fingerprint')
    import sys
    sys.path.insert(0,str(OUT/'scripts'))
    from bien_nhan import fingerprint as fp
    assert fp(doc)==fingerprint
    old_protocol=load(RUN/'before-files/protocol.json')
    preserved=['A4','C_e','Cd3','a4_record_contract','configurations','effective_config','ranking','regions','window']
    assert all(protocol[k]==old_protocol[k]for k in preserved),'science protocol changed'
    matrix=load(OUT/'matrix.json');old_matrix=load(RUN/'before-files/matrix.json')
    assert all(matrix[k]==old_matrix[k]for k in ('main','derived','ce'))
    assert len(matrix['auxiliary'])==180 and all(j['a4']is False for j in matrix['auxiliary'])
    authority=load(OUT/'authorization.json')
    assert all(authority[k]is False for k in ('g3','test_grant','ssh_grant','sync_grant','commit_push'))
    assert protocol['status']=='CANDIDATE_NOT_LOCKED' and protocol['real_execution_ready']is False
    from dieu_phoi import status
    from cham import verify_snapshot
    total=0
    for name,expected in [('pilot-local-007',32),('pilot-local-008',8)]:
        directory=RUN/name;plan=load(directory/'plan.json');state=status(directory/'queue')
        assert state['controller']is None and len(state['jobs'])==expected
        assert all(v['state']=='VERIFIED'for v in state['jobs'].values())
        assert plan['mode']=='dev' and all(j['evaluation_mode']=='dev' for j in plan['jobs'])
        assert set(j['slot']['dataset']for j in plan['jobs'])=={'RE2-TT','Nezha-OB'}
        verify_snapshot(load(directory/'sealed-snapshot.json'),plan['jobs'])
        total+=expected
    assert load(RUN/'regression-transport-001/summary.json')['count']==60
    assert load(RUN/'regression-transport-001/summary.json')['PASS']is True
    assert load(RUN/'new-guard-checks.json')['PASS']is True
    assert load(RUN/'new-guard-checks.json')['count']==16
    assert load(RUN/'source-original-checks.json')['PASS']is True
    assert all(r['exact']for r in load(RUN/'control-T050-parity.json')['rows'])
    diagnostic=load(RUN/'diagnostic-thread-001/summary.json')
    assert diagnostic['same_normalized_input_as_one_thread']and diagnostic['exact_scientific_fields_vs_old']
    assert diagnostic['main_config_changed']is False
    numeric=load(RUN/'numeric-parity-analysis.json')
    assert numeric['tolerance_chosen']is False and len(numeric['rows'])==3
    for version,plan_name,arm in [('code-pilot-002','pilot-local-005','M1'),
                                  ('code-pilot-006-r2','pilot-local-006','C-d3'),
                                  ('code-pilot-007','pilot-local-007','circa')]:
        plan=load(RUN/plan_name/'plan.json')
        job=next(j for j in plan['jobs']if j['slot']['arm']==arm and j['slot']['dataset']=='RE2-TT')
        for p in (RUN/version).glob('*.py'):check(p,job['code_pins']['results/T-054/scripts/'+p.name])
    exported=load(RUN/'metadata-export-001/summary.json')
    assert exported['documents_overwritten']is False
    for name,pin in exported['exported_documents'].items():check(Path(pin['path']),pin)
    freeze=OUT/'runs/freeze-cong-cu-005';files=load(freeze/'files.json')['files'];assert len(files)==107
    for relative,pin in files.items():check(ROOT/relative,pin);check(freeze/'code'/relative,pin)
    with tarfile.open(freeze/'code.tar.gz','r:gz')as archive:
        assert set(archive.getnames())==set(files)
        for member in archive.getmembers():
            assert member.isfile()and hashlib.sha256(archive.extractfile(member).read()).hexdigest()==files[member.name]['sha256']
    assert load(freeze/'package.json')['test_allowed']is False
    import psutil
    owned=[]
    for process in psutil.process_iter(['pid','cmdline']):
        try:
            parts=[x.replace('\\','/')for x in process.info['cmdline']or[]]
            is_worker=any(x.endswith('/T-054/scripts/worker.py')for x in parts)
            is_supervisor=any(x.endswith('/T-054/scripts/p7.py')for x in parts)and'_supervise'in parts
            if is_worker or is_supervisor:owned.append(process.info['pid'])
        except(psutil.NoSuchProcess,psutil.AccessDenied):pass
    assert not owned,('owned processes live',owned)
    return {'PASS':True,'scope':'integrity, evidence linkage and permission checks; NOT G3/scientific acceptance',
      'existing_files_checked':len(before),'changed_existing_files':changed,
      'protected_existing_files_preserved':len(before)-len(changed),'LOG_append_only':True,'STATE_only_T054_row':True,
      'science_fields_preserved':preserved,'own_scripts_AST':9,'legacy_code_pins':93,
      'DEV_slots_verified':total,'DEV_cases':4,'transport_checks':60,'new_guard_checks':16,
      'code_versions_exact':3,'freeze_files_exact':len(files),'live_owned_workers':owned,
      'known_numeric_parity_issues_preserved':3,'G3':False,'main_started':False,'test_opened':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--manifest');args=parser.parse_args()
    result=validate()
    if args.manifest:
        manifest=load(ROOT/args.manifest)
        for relative,pin in manifest['outputs'].items():check(ROOT/relative,pin)
        result['manifest_outputs_verified']=len(manifest['outputs'])
    else:
        p=RUN/'validation.json';assert not p.exists()
        p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

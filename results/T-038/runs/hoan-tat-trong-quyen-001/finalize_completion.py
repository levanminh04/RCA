"""Kiểm bổ sung và manifest; không mở lại raw/index cách ly hay chạy thí nghiệm."""
import ast
from collections import Counter
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import re
import time
import traceback

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'results/T-038'
RUN=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')


def diff(before,after,name):
    return ''.join(difflib.unified_diff(before.decode('utf-8-sig').splitlines(keepends=True),after.decode('utf-8-sig').splitlines(keepends=True),fromfile=name+':before',tofile=name+':after'))


def main():
    start=time.monotonic()
    assert not (RUN/'completion-verification.json').exists(), 'Do not overwrite finished run'
    checks={}
    old=load(RUN/'before-manifest.json')
    allowed={f'results/T-038/{s}' for s in ['bao-phu-nguon.json','bao-phu-nguon.md','phan-tich-chenh-lech.json','phan-tich-chenh-lech.md','kiem-dung-dan.md','ban-giao.md','de-nghi-tiep-theo.md','LICH-SU.md','kha-thi.json']}
    changed=[]
    for r in old['files']:
        if sha(ROOT/r['path'])!=r['sha256']:changed.append(r['path'])
    checks['only_expected_existing_artifacts_changed']=set(changed)==allowed
    checks['all_other_5224_previous_artifacts_hash_unchanged']=len(old['files'])-len(changed)==5224 and set(changed)<=allowed
    checks['prior_manifest_preserved']=sha(OUT/'manifest.json')==sha(RUN/'before-manifest.json')
    baseline=load(OUT/'runs/kiem-dau-vao-001/baseline.json')
    protected={p:sha(ROOT/p)==v['sha256'] for p,v in baseline.items() if p not in ['docs/STATE.md','tasks/T-038-p5b-trainticket/LOG.md']}
    checks['governing_files_SPEC_decisions_unchanged']=all(protected.values())
    inputs=load(OUT/'runs/kiem-dau-vao-002/input-verification.json')
    checks['input_manifest_pin_unchanged']=all(sha(ROOT/p)==v['sha256'] for p,v in inputs['input_manifests'].items())
    checks['all187_T036_artifacts_unchanged']=all(sha(ROOT/r['path'])==r['sha256'] for r in inputs['t036_files'])
    for p,expected in load(ROOT/'results/T-036/runs/kiem-r1-after-002/code-hashes.json').items():
        assert sha(ROOT/p)==sha(ROOT/'results/T-036/runs/kiem-r1-after-002/code'/Path(p).name)==expected
    checks['shared_code_still_exact_old_pin']=True
    for name in ['ban-ghi.json','mapping.json','nguon.json']:
        assert sha(OUT/name)==sha(RUN/('before-'+name))
    expected=load(OUT/'runs/doi-chieu-dev-002/input-hashes.json')
    checks['model_mapping_registry_graphs_not_changed']=all(sha(OUT/name)==value for name,value in expected.items())
    summary=load(OUT/'runs/doi-chieu-dev-002/summary.json')
    checks['all1069_comparison_outputs_current']=summary['graph_count']==1069 and not summary['errors'] and all(sha(ROOT/r['output'])==r['output_sha256'] and sha(ROOT/r['input'])==r['input_sha256'] for r in summary['rows'])
    checks['prior_repeat_reorder_set_checks_remain_valid']=load(OUT/'runs/doi-chieu-dev-002/self-checks.json')['ok'] and load(OUT/'runs/ket-phien-002/final-verification.json')['ok']
    current_analysis,old_analysis=load(OUT/'phan-tich-chenh-lech.json'),load(RUN/'before-phan-tich-chenh-lech.json')
    checks['old_numerical_analysis_values_unchanged']=all(current_analysis[k]==v for k,v in old_analysis.items())
    coverage=load(OUT/'bao-phu-nguon.json')
    counts=dict(Counter(r['status'] for r in coverage['files']))
    checks['coverage_statuses_depths_exact']=counts==coverage['statuses']=={'read':2783,'excluded':43,'open':1} and coverage['read_depths']==dict(Counter(r['read_depth'] for r in coverage['files']))
    checks['coverage_entire_tree_partition']=len(coverage['directories'])==1094 and len(coverage['files'])==len({r['path'] for r in coverage['files']})==2827
    checks['all27_old_OPEN_accounted']=len(load(RUN/'coverage/findings.json')['records'])==27 and load(RUN/'coverage/findings.json')['all_checks_ok']
    checks['content_and_runtime_limits_not_promoted']=not coverage['semantic_source_inventory_complete'] and not coverage['content_scope_complete'] and not coverage['remaining_content_open_blocks_declared_current_inventory']
    flags=load(RUN/'source-flag-resolution.json')
    checks['nine_initializers_and151_flags_accounted']=flags['ok'] and len(flags['nine_initializer_proofs'])==9 and len(flags['rows'])==151 and {r['original_index'] for r in flags['rows']}==set(range(151))
    matrix=load(OUT/'hoan-tat-trong-quyen.json')
    checks['authorized_complete_not_task_acceptance']=matrix['authorized_execution_complete'] and not matrix['full_task_accepted'] and not matrix['shared_SMTP_fix_applied'] and not matrix['research_questions_closed']
    preview=load(RUN/'smtp/kiem-preview-001/checks.json')
    checks['SMTP_preview_only26_pass']=preview['all_ok'] and preview['shared_code_unchanged'] and len(preview['checks'])==26
    package=load(RUN/'smtp/package-manifest.json')
    package_rows=package['files']
    for r in package_rows:
        p=ROOT/r['path'] if r['path'].startswith('results/') else RUN/'smtp'/r['path']
        assert sha(p)==r['sha256'],r['path']
    checks['concrete_SMTP_package_integrity']=True
    checks['SMTP_oracle_before_candidate']=sha(RUN/'smtp/oracle-before-code.json')==preview['oracle_sha256']
    plan=load(RUN/'smtp/plan.json')
    checks['proposal_not_applied_and_runner_adoption_explicit']=plan['status']=='CANDIDATE_NOT_APPLIED_AWAITING_MINH_APPROVAL' and bool(plan['runner_adoption']) and bool(plan['proposed_writes']['new_run_exact_runner_files'])
    for directory in ['lineage','lineage-branch-followup']:
        for r in load(RUN/directory/'requests.json'):
            if 'saved' in r:assert sha(RUN/directory/r['saved'])==r['sha256']
    checks['new_metadata_receipts_and_failures_retained']=len(load(RUN/'lineage-resolution.json')['failed_requests_preserved'])==2
    log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md'
    before_log=(RUN/'LOG-before.md').read_bytes()
    checks['LOG_append_only']=log.read_bytes().startswith(before_log)
    before=(RUN/'STATE-immediate-before.md').read_bytes();after=(RUN/'STATE-immediate-after.md').read_bytes()
    pattern=re.compile(rb'(?m)^\| T-038 \|[^\r\n]*')
    checks['STATE_only_T038_row']=len(pattern.findall(before))==len(pattern.findall(after))==1 and pattern.sub(b'T038',before)==pattern.sub(b'T038',after)
    state_now=(ROOT/'docs/STATE.md').read_bytes()
    checks['STATE_own_row_still_current']=pattern.findall(state_now)==pattern.findall(after)
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
    def block(head):return re.search(re.escape(head)+r'\s+```text\n(.*?)\n```',template,re.S)[1]
    body='\nKhông sửa ngoài phạm vi trên,'+block('## Prompt chung').split('\nKhông sửa ngoài phạm vi trên,',1)[1]
    for name,stage in [('prompt-claude.txt','### Soát kết quả'),('prompt-claude-smtp.txt','### Soát SPEC')]:
        prompt=(OUT/name).read_text(encoding='utf-8')
        assert body in prompt and prompt.endswith(block(stage)+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n') and prompt.rstrip() in log.read_text(encoding='utf-8-sig')
    checks['two_neutral_handoffs_verbatim']=True
    parsed=[];AST=[]
    for p in sorted(RUN.rglob('*')):
        if not p.is_file():continue
        if p.suffix=='.json':load(p);parsed.append(p.relative_to(ROOT).as_posix())
        if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p));AST.append(p.relative_to(ROOT).as_posix())
    checks['new_derived_JSON_and_Python_parse']=True
    checks['no_bytecode_generated']=not list(OUT.rglob('__pycache__'))
    result=dict(task='T-038',checks=checks,protected_files=protected,changed_existing_artifacts=changed,new_derived_JSON=parsed,AST=AST,
        source_and_quarantine_decoded=False,active_pin_changed=False,scientific_task_accepted=False,authorized_execution_complete=True,
        additional_elapsed_verification_seconds=time.monotonic()-start,shared_STATE_other_rows_changed_after_release=pattern.sub(b'T038',state_now)!=pattern.sub(b'T038',after),
        ok=all(checks.values()),created_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    if not result['ok']:
        save(RUN/('completion-failed-'+dt.datetime.now().strftime('%H%M%S')+'.json'),result)
        raise AssertionError([k for k,v in checks.items() if not v])
    with log.open('ab') as f:
        f.write(('\n\n**Kiểm cuối lượt bổ sung:** finalize_completion.py đạt kiểm hash/pin chung, đủ1069output/input bất biến, numericalanalysis khôngđổi, coverage status/depth/group vàtoàn27mục,9initializer/151flags, góiSMTP26checks/candidate/oracle/filehash, hai promptnguyênmẫu, JSON/AST và LOGappend-only/STATEchỉT038. Đã sửa summary read_depths từCounter sau tựkiểm hỗtrợ, giữbảntrước; khôngđổi nguồn/model/sốso. Không sửa src/shared/SPEC/WHY/DECISIONS/taskkhác, khôngcommit/push. Lệnhcuốiđãchạy: `py -3 -X utf8 -B results/T-038/runs/hoan-tat-trong-quyen-001/finalize_completion.py`. Bướctiếp: Minhduyệt chínhxác góiSMTP mớiápdụng vàtiếpnhậnpin; phầntrongquyềnT038 đãhoàntất, khôngtựnghiệmthu/G3.\n').encode('utf-8'))
    (RUN/'LOG.diff').write_text(diff(before_log,log.read_bytes(),'tasks/T-038-p5b-trainticket/LOG.md'),encoding='utf-8')
    (RUN/'STATE.diff').write_text(diff(before,after,'docs/STATE.md'),encoding='utf-8')
    for name in sorted(allowed):
        p=ROOT/name;prev=RUN/('before-'+p.name)
        if prev.exists():(RUN/(p.name+'.diff')).write_text(diff(prev.read_bytes(),p.read_bytes(),name),encoding='utf-8')
    result['external_mutations']=[dict(path='tasks/T-038-p5b-trainticket/LOG.md',change='append only',sha256=sha(log)),dict(path='docs/STATE.md',change='T038 row only',written_sha256=hashlib.sha256(after).hexdigest(),current_sha256=sha(ROOT/'docs/STATE.md'))]
    save(RUN/'completion-verification.json',result)
    quarantined={'runs/trien-khai-001/coverage/content-index.json','runs/trien-khai-001/coverage/coverage.json','runs/trien-khai-001/coverage/archive-structures.json'}
    files=[]
    for p in sorted(p for p in OUT.rglob('*') if p.is_file() and p!=OUT/'manifest.json'):
        relative=p.relative_to(OUT).as_posix()
        files.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p),validation='hash-only-source-or-quarantined' if relative.startswith('sources/') or relative in quarantined else 'derived-artifact'))
    old.update(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='authorized T038 execution completed; exact shared SMTP package awaiting Minh approval; full task not accepted',
        current_completion_run=RUN.relative_to(OUT).as_posix(),current_completion_report='hoan-tat-trong-quyen.md',current_SMTP_proposal='goi-sua-SMTP.md',current_completion_verification='runs/hoan-tat-trong-quyen-001/completion-verification.json',
        source_coverage_counts=counts,authorized_execution_complete=True,scientific_task_complete=False,semantic_inventory_complete=False,
        previous_supplement_manifest='runs/hoan-tat-trong-quyen-001/before-manifest.json',file_count=len(files),files=files,total_artifact_bytes_excluding_manifest=sum(r['bytes'] for r in files),
        last_external_LOG_sha256=sha(log),last_external_STATE_sha256=sha(ROOT/'docs/STATE.md'))
    save(OUT/'manifest.json',old)
    print(json.dumps(dict(ok=True,checks=len(checks),file_count=len(files),logical_bytes_excluding_manifest=old['total_artifact_bytes_excluding_manifest'],manifest_bytes=(OUT/'manifest.json').stat().st_size,authorized_execution_complete=True,SMTP_applied=False),ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except Exception as e:
        save(RUN/('finalizer-error-'+dt.datetime.now().strftime('%H%M%S')+'.json'),dict(error=repr(e),traceback=traceback.format_exc()))
        raise

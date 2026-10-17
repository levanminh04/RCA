"""Kiểm/manifest triển khai; nguồn và index cách ly chỉ hash, không parse."""
import ast
import datetime as dt
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import re
import time
from engine import ROOT, OUT, load, save, checksum, canon, pinned_api


def diff(before, after, name):
    return ''.join(difflib.unified_diff(before.decode('utf-8-sig').splitlines(keepends=True),
        after.decode('utf-8-sig').splitlines(keepends=True),fromfile=name+':before',tofile=name+':after'))


def main():
    start=time.monotonic()
    run=OUT/'runs/ket-phien-002'
    run.mkdir(exist_ok=True)
    assert not (run/'final-verification.json').exists(), 'Keep completed final run immutable'
    (run/'finalize_implementation.py').write_bytes(Path(__file__).read_bytes())
    checks={}
    baseline=load(OUT/'runs/kiem-dau-vao-001/baseline.json')
    protected={p:checksum(ROOT/p)==v['sha256'] for p,v in baseline.items()
        if p not in {'docs/STATE.md','tasks/T-038-p5b-trainticket/LOG.md'}}
    checks['protected_files_unchanged']=all(protected.values())
    log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md'
    beforelog=(OUT/'runs/kiem-dau-vao-001/LOG-before.md').read_bytes()
    checks['log_append_only']=log.read_bytes().startswith(beforelog)
    before=(run/'STATE-immediate-before.md').read_bytes()
    after=(run/'STATE-immediate-after.md').read_bytes()
    row=re.compile(rb'(?m)^\| T-038 \|[^\r\n]*')
    checks['state_only_own_row']=len(row.findall(before))==len(row.findall(after))==1 and row.sub(b'T038',before)==row.sub(b'T038',after)
    now=(ROOT/'docs/STATE.md').read_bytes()
    checks['state_own_row_still_current']=row.findall(now)==row.findall(after)
    inputs=load(OUT/'runs/kiem-dau-vao-002/input-verification.json')
    checks['input_manifests_pinned']=all(checksum(ROOT/p)==v['sha256'] for p,v in inputs['input_manifests'].items())
    inputs_checked=[]
    for group in ['t036_files','rcaeval_sources','t002_public_metadata','t035_documents']:
        rows=inputs[group]
        assert all(checksum(ROOT/r['path'])==r['sha256'] and (ROOT/r['path']).stat().st_size==r['bytes'] for r in rows)
        inputs_checked.append(dict(group=group,count=len(rows),ok=True))
    checks['upstream_artifacts_unchanged']=True
    build,compare=pinned_api()
    checks['pinned_api_integrity']=True
    doc,registry=load(OUT/'ban-ghi.json'),load(OUT/'nguon.json')
    eg,og=build.build(doc,registry)
    checks['rebuild_exact_entity_graph']=canon(eg)==canon(load(OUT/'do-thi/thuc-the.json'))
    checks['rebuild_exact_operation_graph']=canon(og)==canon(load(OUT/'do-thi/thao-tac.json'))
    projected=build.project(og)
    projected_keys={canon(build.edge_signature(r)) for r in projected['edges']}
    entity_keys={canon(build.edge_signature(r)) for r in eg['edges']}
    entity_only=load(OUT/'do-thi/chi-thuc-the.json')['edges']
    only_keys={canon(build.edge_signature(r)) for r in entity_only}
    checks['projection_and_entity_only_partition']=canon(projected)==canon(load(OUT/'do-thi/chieu-thao-tac.json')) and not projected_keys&only_keys and projected_keys|only_keys==entity_keys
    saved_assembly=OUT/'runs/lap-ban-ghi-005'
    checks['assembly_snapshots_exact']=all(checksum(OUT/p)==checksum(saved_assembly/p) for p in ['ban-ghi.json','nguon.json','do-thi/thuc-the.json','do-thi/thao-tac.json'])
    assembly=load(saved_assembly/'result.json')
    checks['model_report_counts']=len(doc['entities'])==assembly['entities']==110 and len(doc['operations'])==assembly['operations']==993 and len(doc['relations'])==assembly['relations']==508 and len(doc['signals'])==assembly['signals']==139
    checks['shared_signals_not_assigned_per_operation']=all(s['operation'] is None for s in doc['signals'] if s['shared'])
    checks['runtime_names_not_invented']=all(o['runtime_name'] is None for o in doc['operations'])
    acquired=load(OUT/'runs/tai-nguon-001/manifest.json')
    for i,r in enumerate(acquired['files']):
        assert checksum(ROOT/r['path'])==r['sha256']
        if i%700==0: print(canon(dict(stage='source-hash-only',done=i+1,total=2827)),flush=True)
    checks['every_acquired_blob_hash']=len(acquired['files'])==2827 and acquired['ok']
    coverage=load(OUT/'bao-phu-nguon.json')
    checks['coverage_partition']=len(coverage['directories'])==1094 and len(coverage['files'])==2827 and sum(coverage['statuses'].values())==2827 and coverage['statuses']=={'read':2758,'excluded':42,'open':27}
    summary=load(OUT/'runs/doi-chieu-dev-002/summary.json')
    selfchecks=load(OUT/'runs/doi-chieu-dev-002/self-checks.json')
    checks['all_1069_inputs_compared']=summary['graph_count']==1069 and not summary['errors'] and summary['conditional_reference_count']==1069
    checks['repeat_reorder_unchanged_all']=selfchecks['ok'] and len(selfchecks['rows'])==1069
    checks['oracle_all_pass']=summary['fixture_checks_passed']==summary['fixture_checks_total']==23
    for key,value in load(OUT/'runs/doi-chieu-dev-002/input-hashes.json').items():
        assert checksum(OUT/key)==value
    checks['comparison_final_inputs_unchanged']=True
    summary_rows=[]
    for i,r in enumerate(summary['rows']):
        assert checksum(ROOT/r['input'])==r['input_sha256']
        assert checksum(ROOT/r['output'])==r['output_sha256']
        result=json.loads(gzip.decompress((ROOT/r['output']).read_bytes()))
        assert result['conditional_reference'] and result['interval_ns']==r['interval_ns']
        for view,vals in result['views'].items():
            S,T=set(map(canon,vals['S'])),set(map(canon,vals['T']))
            assert set(map(canon,vals['intersection']))==S&T
            assert set(map(canon,vals['static_only']))==S-T
            assert set(map(canon,vals['trace_only']))==T-S
            assert vals['static_denominator']==len(S) and vals['trace_denominator']==len(T)
            assert vals['static_fraction']==(len(S&T)/len(S) if S else None)
            assert vals['trace_fraction']==(len(S&T)/len(T) if T else None)
        summary_rows.append(dict(input=r['input'],output=r['output'],ok=True))
        if i%300==0:print(canon(dict(stage='final-comparison-output',done=i+1,total=1069)),flush=True)
    checks['final_all_output_hashes_sets_intervals_NA']=True
    checks['supplement_same_outputs']=load(OUT/'runs/doi-chieu-dev-002/cross-run-equivalence.json')['ok']
    checks['SMTP_preserved_uncoerced']=load(OUT/'fixtures/smtp-counterexample.json')['actual_rejection']=='relation_type' and not load(OUT/'fixtures/smtp-counterexample.json')['coercion_applied']
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
    prompt=(OUT/'prompt-claude.txt').read_text(encoding='utf-8')
    def block(heading):return re.search(re.escape(heading)+r'\s+```text\n(.*?)\n```',template,re.S)[1]
    body=block('## Prompt chung').split('\nKhông sửa ngoài phạm vi trên,',1)[1]
    checks['prompt_verbatim_and_in_log']='\nKhông sửa ngoài phạm vi trên,'+body in prompt and prompt.endswith(block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n') and prompt.rstrip() in log.read_text(encoding='utf-8-sig')
    quarantined={'runs/trien-khai-001/coverage/content-index.json','runs/trien-khai-001/coverage/coverage.json','runs/trien-khai-001/coverage/archive-structures.json'}
    parsed=[]
    pyfiles=[]
    for path in sorted(OUT.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(OUT).as_posix()
        if relative.startswith('sources/') or relative in quarantined:continue
        if path.suffix=='.json' and path!=OUT/'manifest.json':
            load(path);parsed.append(relative)
        if path.suffix=='.py':
            ast.parse(path.read_text(encoding='utf-8-sig'),filename=relative);pyfiles.append(relative)
    checks['derived_json_parse_selective']=True
    checks['own_python_AST']=True
    checks['no_bytecode_generated']=not list(OUT.rglob('__pycache__'))
    checks['partial_conclusions_preserved']=not coverage['semantic_source_inventory_complete'] and not summary['complete_source_inventory_claim'] and not summary['benefit_or_instrumentation_claim']
    result=dict(task='T-038',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),checks=checks,
        protected_files=protected,upstream_groups=inputs_checked,source_content_parse=False,
        quarantine_hash_only=sorted(quarantined),parsed_derived_json=parsed,AST_files=pyfiles,
        shared_state_other_rows_changed_after_release=row.sub(b'T038',now)!=row.sub(b'T038',after),
        scientific_task_complete=False,download_authorized=True,source_complete=False,
        spec_or_scientific_decision_changed=False,commit_push=False,check_elapsed_seconds=time.monotonic()-start,ok=all(checks.values()))
    if not result['ok']:
        stamp=dt.datetime.now().strftime('%H%M%S')
        save(run/('failed-'+stamp+'.json'),result)
        raise AssertionError([k for k,v in checks.items() if not v])
    with log.open('ab') as f:
        f.write(('\n\n**Kiểm cuối triển khai:** finalize_implementation.py đạt toàn bộ kiểm pin/hash, rebuild/đếm bản ghi, đủ 1069 output và tập/mẫu số/interval, input bất biến, oracle/lặp/đảo, coverage partition, LOG append-only, STATE chỉ dòng T038 và prompt nguyên văn. Nguồn/mẫu/index cách ly chỉ hash, không parse lại. Giữ phần khoa học chưa đủ và mọi lượt lỗi. Lệnh cuối đã chạy: `py -3 -X utf8 -B results/T-038/finalize_implementation.py`. Bước tiếp: Minh chuyển prompt-claude.txt cho Claude soát kết quả và quyết phần thiếu; không tự chạy ngoài quyền hoặc nghiệm thu.\n').encode('utf-8'))
    (run/'LOG.diff').write_text(diff(beforelog,log.read_bytes(),'tasks/T-038-p5b-trainticket/LOG.md'),encoding='utf-8')
    (run/'STATE.diff').write_text(diff(before,after,'docs/STATE.md'),encoding='utf-8')
    result['external_mutations']=[dict(path='tasks/T-038-p5b-trainticket/LOG.md',mode='append-only',sha256=checksum(log)),dict(path='docs/STATE.md',mode='T038 row only',written_sha256=hashlib.sha256(after).hexdigest(),current_sha256=checksum(ROOT/'docs/STATE.md'))]
    save(run/'final-verification.json',result)
    save(run/'compared-output-verification.json',dict(ok=True,rows=summary_rows))
    # Previous manifest already copied before approved continuation.
    assert checksum(OUT/'manifest.json')==checksum(OUT/'runs/trien-khai-001/manifest-before.json')
    files=[]
    for i,path in enumerate(sorted(p for p in OUT.rglob('*') if p.is_file() and p!=OUT/'manifest.json')):
        relative=path.relative_to(OUT).as_posix()
        files.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=checksum(path),
                          validation='hash-only-source-or-quarantined' if relative.startswith('sources/') or relative in quarantined else 'derived-artifact'))
        if i%1500==0:print(canon(dict(stage='manifest-all-history',done=i+1)),flush=True)
    manifest=dict(task='T-038',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),client_date='2026-10-16',
        status='partial; full dev comparison complete; waiting independent result review and missing-source/SMTP decisions',
        current_model='runs/lap-ban-ghi-005',current_run='runs/doi-chieu-dev-002',current_handoff='ban-giao.md',
        source_registry='nguon.json',coverage='bao-phu-nguon.json',current_prompt='prompt-claude.txt',
        shared_T036_pin=inputs['pin'],input_manifests=inputs['input_manifests'],
        source_acquisition='runs/tai-nguon-001/manifest.json',source_approval='runs/trien-khai-001/authorization.json',
        previous_manifest='runs/trien-khai-001/manifest-before.json',source_dataset_revision_link_verified=False,
        file_count=len(files),total_artifact_bytes_excluding_manifest=sum(r['bytes'] for r in files),files=files,
        disk_condition='Logical retained bytes incl source/all history/intermediates; NTFS allocation/metadata and future runs unknown.',
        validation='All entries hash verified during sweep; protected samples/indexes never decoded by finalizer. Semantic selective checks listed in final-verification.',
        scientific_task_complete=False,semantic_inventory_complete=False,decision_state_changes=False,
        commit_push=False,excludes='manifest self; external LOG/STATE exact mutation records in final-verification')
    save(OUT/'manifest.json',manifest)
    assert load(OUT/'manifest.json')['file_count']==len(files)
    assert all((ROOT/r['path']).stat().st_size==r['bytes'] for r in files)
    print(canon(dict(ok=True,checks=len(checks),file_count=len(files),logical_bytes_excluding_manifest=manifest['total_artifact_bytes_excluding_manifest'],final_manifest_bytes=(OUT/'manifest.json').stat().st_size,graph_count=1069,task_complete=False)))


if __name__=='__main__':main()

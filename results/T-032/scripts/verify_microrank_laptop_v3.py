"""Read-only stdlib verification of closed MicroRank laptop artifacts.

No method, adapter, data or native replay is imported. The only optional write
is one new root verification receipt outside the immutable cohort.
"""
from __future__ import annotations
import argparse
import ctypes
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys

REPO = Path('D:/RCA-flashticket')
BASE = REPO / 'results/T-032'
OUT = BASE / 'runs/microrank-laptop-cohort-001'
ACCOUNTING = BASE / 'runs/microrank-laptop-cohort-001-accounting'
EXACT_FIELDS = ('opaque_id','method','method_version','variant','mode','detector','detector_columns','seed','hashseed',
 'config_id','why_ids','window','input_shape','status','method_status_raw','error','ranking_native','ranking','entity_ranking',
 'blocks','sets','diagnostics','extra','input_sha256')
EXCLUDED_FIELDS = ('run_id','cost')
VALID_TERMINALS = ('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES','PASS_FULL52_LAPTOP_EXACT')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def exact(left, right, pointer=''):
    if type(left) is not type(right):
        return [pointer + ': type']
    if isinstance(left, dict):
        result = [] if set(left) == set(right) else [pointer + ': keys']
        for key in sorted(set(left) & set(right)):
            result.extend(exact(left[key], right[key], pointer + '/' + str(key)))
        return result
    if isinstance(left, list):
        result = [] if len(left) == len(right) else [pointer + ': length']
        for index, (a, b) in enumerate(zip(left, right)):
            result.extend(exact(a, b, pointer + '/' + str(index)))
        return result
    if isinstance(left, float):
        return [] if left.hex() == right.hex() else [pointer + ': float bits']
    return [] if left == right else [pointer + ': value']


def compare_records(left, right):
    fields = set(EXACT_FIELDS) | set(EXCLUDED_FIELDS)
    require(set(left) == fields and set(right) == fields, 'record field schema differs')
    return exact({k: left[k] for k in EXACT_FIELDS}, {k: right[k] for k in EXACT_FIELDS})


def resolved_source(value):
    path = Path(value)
    path = path if path.is_absolute() else REPO / path
    require(path.resolve().is_relative_to(REPO.resolve()), 'source outside canonical repo: ' + str(path))
    require('locked' not in [part.lower() for part in path.parts], 'locked source is forbidden')
    require(not path.is_symlink(), 'redirected source')
    return path


class Checks:
    def __init__(self):
        self.verified = []
        self.manifests = []

    def pin(self, path, expected, size=None):
        path = Path(path)
        require(re.fullmatch(r'[0-9a-f]{64}', expected) is not None, 'invalid pin ' + str(path))
        require(path.is_file() and not path.is_symlink(), 'missing/redirected file ' + str(path))
        measured = path.stat().st_size
        actual = sha(path)
        require(actual == expected and (size is None or measured == size), 'hash/size differs ' + str(path))
        self.verified.append({'path': str(path), 'bytes': measured, 'sha256': actual})

    def manifest(self, directory, file_name, key='files', legacy_default_exclusion=False, appended_subtree=None):
        directory = Path(directory)
        seal = read(directory / file_name)
        rows = seal[key]
        excludes = seal.get('manifest_excludes', [file_name] if legacy_default_exclusion else None)
        require(excludes == [file_name], 'unexpected exclusions ' + str(directory / file_name))
        seen = set()
        for row in rows:
            relative = PurePosixPath(row['path'])
            require(not relative.is_absolute() and '..' not in relative.parts and '\\' not in row['path'] and row['path'] not in seen,
                    'duplicate/escaped artifact path')
            path = directory / relative
            require(path.resolve().is_relative_to(directory.resolve()), 'artifact path escaped')
            self.pin(path, row['sha256'], row['bytes'])
            seen.add(row['path'])
        actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}
        approved_append = set()
        if appended_subtree is not None:
            appended_root = directory / PurePosixPath(appended_subtree)
            require(appended_root.resolve().is_relative_to(directory.resolve()), 'appended subtree escaped')
            approved_append = {p.relative_to(directory).as_posix() for p in appended_root.rglob('*') if p.is_file()} - seen
        require(actual == seen | {file_name} | approved_append, 'manifest full file set differs ' + str(directory))
        self.manifests.append({'path': str(directory / file_name), 'sha256': sha(directory / file_name), 'file_count': len(rows), 'full_file_set': not bool(approved_append), 'approved_appended_fixture_files': sorted(approved_append)})
        return seal


def process_identity_alive(identity):
    if not identity or os.name != 'nt':
        return {'identity': identity, 'alive': None, 'reason': 'no identity or non-Windows host'}
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel.GetProcessTimes.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.FILETIME),ctypes.POINTER(wintypes.FILETIME),ctypes.POINTER(wintypes.FILETIME),ctypes.POINTER(wintypes.FILETIME))
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    handle = kernel.OpenProcess(0x1000, False, identity['pid'])
    if not handle:
        error = ctypes.get_last_error()
        require(error == 87, 'process query failed, identity unknown: ' + str(error))
        return {'identity': identity, 'alive': False, 'reason': 'PID absent'}
    try:
        exit_code = wintypes.DWORD()
        require(kernel.GetExitCodeProcess(handle,ctypes.byref(exit_code)), 'process exit query failed')
        if exit_code.value != 259:
            return {'identity': identity, 'alive': False, 'reason': 'process exited'}
        creation, ending, kernel_time, user_time = (wintypes.FILETIME() for _ in range(4))
        require(kernel.GetProcessTimes(handle,ctypes.byref(creation),ctypes.byref(ending),ctypes.byref(kernel_time),ctypes.byref(user_time)), 'creation time query failed')
        ticks = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
        actual_seconds = ticks / 10000000 - 11644473600
        if 'creation_time_utc' in identity:
            expected = datetime.fromisoformat(identity['creation_time_utc'].replace('Z','+00:00')).timestamp()
        else:
            expected = identity.get('creation_time', identity.get('create_time'))
        require(expected is not None, 'identity lacks process creation time')
        same = abs(actual_seconds - expected) < 0.001
        return {'identity': identity, 'alive': same, 'reason': 'same creation time' if same else 'PID reused by another process'}
    finally:
        kernel.CloseHandle(handle)


def validate_case(row, checks):
    directory = Path(row['artifacts']['path'])
    require(directory.resolve().is_relative_to(OUT.resolve()), 'case outside cohort')
    checks.pin(directory/'closed.json', row['artifacts']['closed_sha256'])
    seal = checks.manifest(directory, 'closed.json')
    require(seal['status'] == 'CLOSED_EXACT_CASE', 'case not closed exact')
    audit = checks.manifest(directory/'audit', 'check.json', 'artifact_manifest')
    checks.pin(directory/'audit/check.json', row['artifacts']['audit_check_sha256'])
    require(audit['status'] == 'PASS' and audit['passed'] is True, 'audit did not pass')
    require((audit['dataset'],audit['opaque_id'],audit['source_status']) == (row['dataset'],row['opaque_id'],row['source_status']), 'audit identity/source status differs')
    for key in ('native_frozen_exact','observed_frozen_exact','native_observed_exact','capture_pass','t028_pass','source_checks_passed'):
        require(audit.get(key) is True and (key == 'source_checks_passed' or row.get(key) is True), 'exact/source/capture/T028 check missing: ' + key)
    for key in ('numeric_differences','service_order_tie_differences','other_differences'):
        require(audit.get(key) == [], 'audit differences present: ' + key)
    source = resolved_source(audit['source']['path'])
    require(audit['source']['sha256'] == row['source_sha256'], 'frozen source pin differs')
    checks.pin(source, row['source_sha256'])
    frozen = read(source)
    records = {}
    historical_retrospective = (row['dataset'],row['opaque_id']) == ('RE2-TT','dev-3defe3d34b') and directory == OUT/'retrospective-dev-3defe3d34b'
    if historical_retrospective:
        retro = read(directory/'audit/retrospective-source-check.json')
        require(retro['methods_executed'] is False and retro['old_files_edited'] is False, 'retrospective unexpectedly mutated/replayed')
        old_seal = resolved_source(retro['old_closed_manifest']['path'])
        checks.pin(old_seal,retro['old_closed_manifest']['sha256'])
        checks.manifest(old_seal.parent,old_seal.name)
        for old_pin in retro['pins']:
            require(old_pin['pass'] is True and old_pin['expected_sha256'] == old_pin['actual_sha256'], 'retrospective source pin failed')
            checks.pin(resolved_source(old_pin['path']),old_pin['expected_sha256'],old_pin['bytes'])
    for mode in ('native','observed'):
        entry = audit[mode]
        record_path = Path(entry['record_path'])
        require(record_path.resolve().is_relative_to(BASE.resolve()), 'record outside approved task')
        checks.pin(record_path, entry['record_sha256'])
        child_directory = record_path.parent
        checks.pin(child_directory/'check.json', entry['check_sha256'])
        if historical_retrospective:
            require(child_directory == BASE/'runs/microrank-laptop-diagnostic-001'/mode, 'historical record path differs')
        child = checks.manifest(child_directory,'check.json','artifact_manifest',historical_retrospective)
        require(child['status'] == 'PASS' and child['source_checks_passed'] is True, 'child source did not pass')
        if not historical_retrospective:
            require(child['passed'] is True and child['worker_streams_closed'] is True, 'child/streams did not pass')
        require(child['mode'] == mode and child['dataset'] == row['dataset'] and child['opaque_id'] == row['opaque_id'] and child['frozen_sha256'] == row['source_sha256'], 'child source/mode differs')
        checks.pin(child_directory/'job.json',entry['job_sha256'])
        require(child['job_sha256'] == entry['job_sha256'], 'child job pin differs')
        require(child['differences'] == [], 'child differences')
        if not historical_retrospective:
            require(child['native_observed_differences'] == [], 'child native-observed differences')
        if mode == 'native':
            require(child['native_observer_absent'] is True, 'native observer invariant')
            if not historical_retrospective:
                require(child['native_frozen_exact'] is True, 'native exact invariant')
        else:
            require(child['capture_check']['pass'] is True, 'observed capture invariant')
            if not historical_retrospective:
                require(child['observed_frozen_exact'] is True and child['native_observed_exact'] is True, 'observed exact invariant')
        records[mode] = read(record_path)
        require(not compare_records(frozen,records[mode]), mode + ' frozen comparison differs')
    require(not compare_records(records['native'],records['observed']), 'native-observed parent comparison differs')
    require(audit['native']['job_sha256'] == audit['observed']['job_sha256'], 'native-observed job differs')
    checks.pin(directory/'audit/exact-comparison.json',audit['comparison_sha256'])
    checks.pin(directory/'audit/t028-check.json',audit['t028_sha256'])
    require(audit['intermediates_eligible'] is (row['source_status'] == 'OK') and row['intermediates_eligible'] is audit['intermediates_eligible'], 'eligibility differs')
    numeric = audit['numeric_summary']
    if row['source_status'] == 'OK':
        require(numeric['status'] == 'COMPUTED_EXACT' and numeric['nonexact_score_count'] == 0 and numeric['max_ulp_distance'] == 0 and numeric['max_relative'] == 0,
                'numeric summary not exact')
        require(row['max_ulp_distance'] == 0 and row['max_relative'] == 0 and row['matched_score_count'] == numeric['matched_score_count'], 'table numeric summary differs')
    else:
        require(audit['non_OK_exact_observation_valid'] is True and audit['non_OK_mechanism_NA_reason'], 'non-OK invariant missing')
        require(row['max_ulp_distance'] is None and row['max_relative'] is None, 'non-OK numeric summary must be N/A')
    streams = read(directory/'stream-receipts.json')
    require(streams['all_child_streams_closed'] is True, 'case streams closure absent')
    for file in streams['files']:
        require(Path(file['path']).resolve().is_relative_to(OUT.resolve()), 'external log outside cohort')
        checks.pin(file['path'],file['sha256'],file['bytes'])
    terminal = read(directory/'case-terminal.json')
    require(terminal['wall_s'] >= 0 and terminal['wall_s'] <= 600 and 0 <= terminal['new_task_bytes_delta'] <= 157286400, 'case cost exceeds unchanged caps')
    return {'dataset':row['dataset'],'opaque_id':row['opaque_id'],'source_status':row['source_status'],
            'frozen_native_observed_exact':True,'capture_T028_pass':True,'status':'PASS','wall_s':terminal['wall_s']}


def validate_recovery(migration, checks):
    require(migration['schema']=='T032-MicroRank-laptop-controller-migration-v3' and migration['authority']=='Q-126'
            and migration['root_verified'] is True, 'migration not approved v3')
    for field in ('same_exact_fields','same_case_set','previous_artifacts_immutable'):
        require(migration[field] is True,'migration invariant missing: '+field)
    previous_path=resolved_source(migration['previous_migration_path'])
    require(previous_path.resolve().is_relative_to(BASE.resolve()),'previous migration outside task')
    checks.pin(previous_path,migration['previous_migration_sha256'])
    previous=read(previous_path)
    require(previous['schema']=='T032-MicroRank-laptop-controller-migration-v2' and previous['authority']=='Q-126'
            and previous['root_verified'] is True, 'historical migration invalid')
    for name, key in [('batch_microrank_laptop_exact_v2.py','controller_sha256'),('start_microrank_laptop_cohort_002.ps1','launcher_sha256'),
                      ('verify_microrank_laptop_v2.py','verifier_sha256')]:
        checks.pin(BASE/'scripts'/name,previous[key])
    checks.pin(BASE/'scripts/batch_microrank_laptop_exact_v3.py',migration['controller_sha256'])
    checks.pin(BASE/'scripts/start_microrank_laptop_cohort_003.ps1',migration['launcher_sha256'])
    checks.pin(Path(__file__),migration['verifier_sha256'])
    checks.pin(BASE/'scripts/replay_microrank_laptop_exact_v2.py',migration['wrapper_sha256'])
    require(migration['wrapper_sha256']==migration['new_wrapper_sha256']==previous['wrapper_sha256']
            and migration['old_source_pin_sha256']==previous['old_source_pin_sha256']
            and migration['plan_sha256']==previous['plan_sha256'],'historical policy/wrapper differs')
    checks.pin(OUT/'source-pin-manifest.json',migration['old_source_pin_sha256'])
    checks.pin(OUT/'plan-52.json',migration['plan_sha256'])
    checks.pin(OUT/'segments/001/launcher-closed.json',migration['initial_segment_closed_sha256'])
    original=read(OUT/'source-pin-manifest.json')
    checks.pin(BASE/'scripts/batch_microrank_laptop_exact_v1.py',migration['historical_controller_sha256'])
    checks.pin(BASE/'scripts/replay_microrank_laptop_exact_v1.py',migration['old_wrapper_sha256'])
    require(original['controller_sha256']==migration['historical_controller_sha256'] and original['wrapper_sha256']==migration['old_wrapper_sha256']
            and original['exact_fields']==list(EXACT_FIELDS) and original['no_tolerance'] is True,'historical exact source policy differs')
    decision=resolved_source(migration['decision_file'])
    require(decision.resolve()==(REPO/'docs/DECISIONS.md').resolve(),'decision source differs')
    checks.pin(decision,migration['decision_sha256'])
    require('| Q-126 |' in decision.read_text(encoding='utf-8-sig'),'Q126 missing')
    fixture_path=resolved_source(migration['fixture_check_path'])
    checks.pin(fixture_path,migration['fixture_check_sha256'])
    require(fixture_path==OUT/'tool-check/runtime-002/check.json','unchanged wrapper fixture differs')
    additional=migration['additional_tool_wall_s']
    require(type(additional) in (int,float) and math.isfinite(additional) and additional>=0
            and abs(migration['tool_validation_wall_s']-previous['tool_validation_wall_s']-additional)<1e-6,
            'old and new tool charges must appear exactly once')
    recovery_path=resolved_source(migration['tool_abort_recovery_path'])
    require(recovery_path.resolve().is_relative_to(BASE.resolve()),'recovery outside task')
    checks.pin(recovery_path,migration['tool_abort_recovery_sha256'])
    recovery=read(recovery_path)
    require(recovery['status']=='ROOT_VERIFIED_TOOL_ABORT_BEFORE_NATIVE_OBSERVED' and recovery['authority']=='Q-108/Q-126'
            and recovery['segment_id']=='002' and recovery['partial_dataset']=='Nezha-OB' and recovery['partial_opaque_id']=='dev-63c30faf34',
            'only root-verified segment002 attach abort is recoverable')
    require(recovery['root_closed_cases_verified']==13 and recovery['root_process_identities_closed'] is True
            and recovery['methods_executed'] is False and recovery['retry_method'] is False,'recovery boundary missing')
    segment=OUT/'segments/002'
    for name,key in [('failure.json','failure_sha256'),('terminal.json','terminal_sha256'),('launcher-terminal.json','launcher_terminal_sha256'),
                     ('launcher-closed.json','launcher_closed_sha256')]:
        checks.pin(segment/name,recovery[key])
    checks.pin(resolved_source(recovery['table_path']),recovery['table_sha256'])
    checks.pin(resolved_source(recovery['cohort_manifest_path']),recovery['cohort_manifest_sha256'])
    failure=read(segment/'failure.json'); terminal=read(segment/'terminal.json'); launcher=read(segment/'launcher-terminal.json')
    require(failure['state']['error_type']=='NoSuchProcess' and 'attach_child' in failure['traceback'] and 'pid=57736' in failure['traceback'],
            'different tool failure cannot resume')
    require(terminal['status']==launcher['status']=='FAIL_STOP' and terminal['active'] is None and terminal['all_children_closed'] is True
            and launcher['exit_code']==1 and launcher['timed_out'] is False and launcher['error'] is None
            and launcher['all_controller_streams_closed'] is True,'failed segment not safely closed')
    accounting_path=ACCOUNTING/'002/accounting-failure-closed.json'
    checks.pin(accounting_path,recovery['accounting_failure_closed_sha256'])
    accounting=checks.manifest(accounting_path.parent,accounting_path.name,'artifact_manifest')
    require(accounting['status']=='FAIL_STOP' and accounting['segment_id']=='002' and accounting['timed_out'] is False
            and accounting['all_supervisor_streams_closed'] is True and recovery['closing_tail_reserve_s']==20
            and recovery['actual_accountant_elapsed_s']==accounting['elapsed_s']
            and abs(recovery['charged_elapsed_s']-accounting['elapsed_s']-20)<1e-6,'failed actual charge differs')
    snapshot=read(recovery['table_path'])
    failed=[r for r in snapshot['rows'] if r['case_status'] not in ('PASS','not_run')]
    require(len(snapshot['rows'])==52 and sum(r['case_status']=='PASS' for r in snapshot['rows'])==13
            and len(failed)==1 and (failed[0]['dataset'],failed[0]['opaque_id'])==(recovery['partial_dataset'],recovery['partial_opaque_id'])
            and failed[0]['source_sha256']==recovery['partial_source_sha256'] and failed[0]['classification']=='other_error'
            and failed[0]['artifacts'] is None,'historical failure table differs')
    partial=OUT/'cases'/recovery['partial_dataset']/recovery['partial_opaque_id']
    require({r['path'] for r in recovery['current_partial_case_files']}=={'prepare/check.json','prepare/prepare.json','prepare/progress.jsonl'},
            'recovery authorizes only source-only preparation')
    for item in recovery['current_partial_case_files']:
        checks.pin(partial/item['path'],item['sha256'],item['bytes'])
    checks.pin(partial/'prepare/check.json',recovery['prepare_check_sha256'])
    checks.pin(partial/'prepare/prepare.json',recovery['prepare_payload_sha256'])
    prepared=checks.manifest(partial/'prepare','check.json','artifact_manifest')
    require(prepared['status']=='PASS' and prepared['passed'] is True and prepared['source_checks_passed'] is True
            and prepared['methods_executed'] is False and prepared['dataset']==recovery['partial_dataset']
            and prepared['opaque_id']==recovery['partial_opaque_id'] and prepared['prepare_sha256']==recovery['prepare_payload_sha256'],
            'reuse preparation is not source-only PASS')
    require(not (segment/'supervisor-failure.json').exists(),'supervisor failure cannot recover')
    return recovery,previous,accounting,snapshot


def verify(migration_path=None, expect_full=False, v2_fixture_sha256=None):
    require(migration_path is not None,'v3 verification needs pinned migration/root recovery')
    checks=Checks(); migration=read(migration_path)
    recovery,previous,failed_accounting,snapshot=validate_recovery(migration,checks)
    index=checks.manifest(OUT,'manifest.json')
    status,table,plan=(read(OUT/name) for name in ('status.json','52-cases.json','plan-52.json'))
    recovery_pending=status['status']=='FAIL_STOP' and status['segment_id']=='002'
    require(index['status'] in VALID_TERMINALS or recovery_pending,'cohort not clean or bound tool abort')
    require(index['all_controller_streams_closed'] is True and status['status']==index['status']==table['status']
            and status['active'] is None,'cohort not closed/idle')
    if recovery_pending:
        checks.pin(OUT/'manifest.json',recovery['cohort_manifest_sha256'])
        checks.pin(OUT/'52-cases.json',recovery['table_sha256'])
        partial=OUT/'cases'/recovery['partial_dataset']/recovery['partial_opaque_id']
        require({p.relative_to(partial).as_posix() for p in partial.rglob('*') if p.is_file()}
                =={r['path'] for r in recovery['current_partial_case_files']},'partial case contains method/extra artifacts')
    require(len(plan['rows'])==len(table['rows'])==52 and len({(r['dataset'],r['opaque_id']) for r in plan['rows']})==52,'locked52 differs')
    require(sum(r['dataset']=='RE2-TT' for r in plan['rows'])==30 and sum(r['dataset']=='Nezha-OB' for r in plan['rows'])==22,'dataset counts differ')
    require(table['plan_sha256']==sha(OUT/'plan-52.json'),'table plan differs')
    for fixture_name in ('runtime-001','runtime-002'):
        fixture=checks.manifest(OUT/'tool-check'/fixture_name,'check.json','artifact_manifest')
        require(fixture['status']=='PASS' and fixture['passed'] is True and fixture['frozen_self_check_count']==52
                and fixture['all_fixture_checks_passed'] is True and fixture['original_comparator_fixtures_pass'] is True,'full fixture invalid')
    if v2_fixture_sha256:
        checks.pin(OUT/'tool-check/runtime-002/check.json',v2_fixture_sha256)
    cases=[]; partial_count=0
    for locked,row,old in zip(plan['rows'],table['rows'],snapshot['rows']):
        require(all(row[key]==value for key,value in locked.items()),'immutable source row changed')
        if old['case_status']=='PASS':
            require(not exact(old,row),'old exact case/table altered')
        if row['case_status']=='PASS': cases.append(validate_case(row,checks))
        elif row['case_status']=='not_run': pass
        else:
            require(recovery_pending and not exact(row,old) and (row['dataset'],row['opaque_id'])==(recovery['partial_dataset'],recovery['partial_opaque_id']),
                    'partial/failed case outside exact recovery')
            partial_count+=1
    require(partial_count==(1 if recovery_pending else 0),'partial recovery count differs')
    require(status['completed_case_count']==len(cases) and table['counts']['exact']+table['counts']['non_OK_exact']==len(cases),'complete count differs')
    require(table['counts']['not_run']==52-len(cases)-partial_count and table['counts']['other_error']==partial_count
            and table['counts']['numeric_difference']==table['counts']['service_order_tie_difference']==0,'case counts/differences invalid')
    if expect_full:
        require(len(cases)==52 and index['status']=='PASS_FULL52_LAPTOP_EXACT' and table['all_52_complete'] is True,'full52 not complete')
    segments=[]; identities=[]; process_reports=[]; phases={}; additional=migration['additional_tool_wall_s']
    # Historical002's prior excludes future v3 tool work. Add that work once after002.
    prior_wall=previous['tool_validation_wall_s']
    require(type(prior_wall) in (int,float) and math.isfinite(prior_wall) and 0<=prior_wall<=18000,'tool wall invalid')
    def closed_identity(identity):
        if identity:
            report=process_identity_alive(identity)
            require(report['alive'] is False,'recorded owned identity still alive/unknown')
            identities.append(report)
    for directory in sorted((OUT/'segments').iterdir()):
        if not directory.is_dir(): continue
        require(re.fullmatch(r'[0-9]{3}',directory.name),'invalid segment name')
        seal=checks.manifest(directory,'launcher-closed.json'); launcher=read(directory/'launcher-terminal.json'); terminal=read(directory/'terminal.json')
        failed=directory.name=='002' and launcher['status']=='FAIL_STOP'
        require(launcher['status']==seal['status']==terminal['status'] and (launcher['status'] in VALID_TERMINALS or failed),'different failed segment')
        checks.pin(directory/'terminal.json',launcher['terminal_sha256'])
        require(launcher['exit_code']==(1 if failed else 0) and launcher['all_controller_streams_closed'] is True
                and terminal['all_children_closed'] is True and terminal['active'] is None,'segment not closed')
        if failed:
            require(abs(failed_accounting['prior_package_wall_s']-prior_wall)<1e-6,'historical002 prior sum differs')
            charged=recovery['charged_elapsed_s'];basis='failed actual accountant elapsed plus20s reserve; bound pre-native abort'
            account_launch=read(ACCOUNTING/'002/launch.json')
        elif directory.name=='001':
            require(migration['historical_unmeasured_tail_reserve_s']==20,'historical tail differs')
            charged=launcher['elapsed_s']+20;basis='historical measured supervisor plus20s tail reserve';account_launch=None
        else:
            accounting_path=ACCOUNTING/directory.name/'accounting-closed.json'
            accounting=checks.manifest(accounting_path.parent,'accounting-closed.json','artifact_manifest')
            require(accounting['status']=='PASS_ACCOUNTING_CLOSED' and accounting['supervisor_exit_code']==0 and accounting['segment_id']==directory.name
                    and accounting['all_supervisor_streams_closed'] is True,'lifetime accounting invalid')
            checks.pin(directory/'launcher-terminal.json',accounting['launcher_terminal_sha256'])
            checks.pin(directory/'launcher-closed.json',accounting['launcher_closed_sha256'])
            require(accounting['elapsed_s']>=launcher['elapsed_s'] and abs(accounting['prior_package_wall_s']-prior_wall)<1e-6
                    and accounting['closing_tail_reserve_s']==20 and abs(accounting['charged_elapsed_s']-accounting['elapsed_s']-20)<1e-6
                    and abs(accounting['cumulative_package_wall_s']-prior_wall-accounting['charged_elapsed_s'])<1e-6,'actual lifetime sum differs')
            charged=accounting['charged_elapsed_s'];basis='actual accountant lifetime plus20s closing reserve'
            account_launch=read(accounting_path.parent/'launch.json')
        if directory.name!='001':
            for key in ('redirector_identity','actual_controller_identity','supervisor_identity'):closed_identity(launcher.get(key))
            for key in ('accountant_identity','supervisor_identity'):closed_identity(account_launch.get(key))
            for identity in terminal['guard']['process_identities']:closed_identity(identity)
            if (directory/'controller-identity.json').exists():closed_identity(read(directory/'controller-identity.json'))
            command=read(directory/'command.json')
            version='v2' if directory.name=='002' else 'v3'
            expected=previous if version=='v2' else migration
            checks.pin(BASE/'scripts'/('batch_microrank_laptop_exact_'+version+'.py'),command['controller_sha256'])
            require(command['controller_sha256']==expected['controller_sha256'] and command['wrapper_sha256']==expected['wrapper_sha256'],'segment tool version differs')
            checks.pin(BASE/'scripts/replay_microrank_laptop_exact_v2.py',command['wrapper_sha256'])
            argv=command['argv']
            require('--migration-file' in argv and '--migration-sha256' in argv,'segment migration binding missing')
            checks.pin(argv[argv.index('--migration-file')+1],argv[argv.index('--migration-sha256')+1])
            expected_migration=previous if version=='v2' else migration
            require(not exact(read(argv[argv.index('--migration-file')+1]),expected_migration),'segment migration policy differs')
            for process_path in sorted((directory/'logs').glob('*-process.json')):
                report=read(process_path);supervision=report['process_supervision']
                require(report['exit_code']==0 and 0<=report['wall_s']<=600,'process failure/cost cap')
                require(supervision['phase']==report['phase'] and supervision['processes'],'phase identity missing')
                require(report['phase'] not in phases,'repeated method/process phase; no retry')
                phases[report['phase']]=str(process_path)
                for identity in supervision['processes']:
                    require(identity['peak_lifetime_working_set_bytes']>=0 and identity['peak_sampled_rss_bytes']>=0,'process peak invalid')
                    closed_identity(identity)
                process_reports.append({'path':str(process_path),'sha256':sha(process_path),'phase':report['phase'],'process_count':len(supervision['processes']),
                    'individual_lifetime_peak_max_bytes':supervision['individual_lifetime_peak_max_bytes'],'peak_sampled_tree_rss_bytes':supervision['peak_sampled_tree_rss_bytes']})
        prior_wall+=charged
        segments.append({'segment_id':directory.name,'status':launcher['status'],'charge_s':charged,'basis':basis,'cumulative_wall_s':prior_wall})
        if directory.name=='002':
            prior_wall+=additional
            segments.append({'segment_id':'v3-tool-validation','charge_s':additional,'basis':'new tool wall exactly once after historical002','cumulative_wall_s':prior_wall})
        require(prior_wall<=18000,'package exceeds five-hour ceiling')
    for row in table['rows']:
        if row['case_status']=='PASS' and row['opaque_id'] not in ('dev-3defe3d34b','dev-14701a3bbb'):
            for phase in ('native','observed','audit'):
                require(phase+'-'+row['opaque_id'] in phases,'closed new case lacks unique process phase: '+phase)
    first_re2=[]
    for path in sorted((OUT/'segments').glob('*/first-re2-peak.json')):
        checkpoint=read(path)
        require(checkpoint['dataset']=='RE2-TT','first RE2 identity differs')
        match=[r for r in table['rows'] if (r['dataset'],r['opaque_id'])==(checkpoint['dataset'],checkpoint['opaque_id'])]
        require(len(match)==1 and match[0]['case_status']=='PASS' and match[0]['artifacts']['closed_sha256']==checkpoint['case_closed_sha256'],'first RE2 not exact closed case')
        measurement=checkpoint['measurement']
        require((measurement['dataset'],measurement['opaque_id'])==(checkpoint['dataset'],checkpoint['opaque_id']),'measurement identity differs')
        for mode in ('native','observed'):
            phase=measurement[mode];cost=measurement[mode+'_worker_cost']
            require(cost['peak_rss_mb']>0 and phase['individual_lifetime_peak_max_bytes']>0 and phase['processes']
                    and all(p['peak_lifetime_working_set_bytes']>=0 for p in phase['processes']),'first RE2 lifetime peak missing')
        first_re2.append({'path':str(path),'sha256':sha(path),'value':checkpoint})
    if any(row['case_status']=='PASS' and row['dataset']=='RE2-TT' and row['opaque_id']!='dev-3defe3d34b' for row in table['rows']):
        require(len(first_re2)==1,'first RE2 checkpoint must be measured once')
    return {'schema':'T032-MicroRank-laptop-root-closed-verification-v3','status':'PASS_CLOSED_ARTIFACTS',
        'at_utc':datetime.now(timezone.utc).isoformat(),'cohort_status':status['status'],'completed_case_count':len(cases),
        'remaining_case_count':52-len(cases),'partial_prepared_case_count':partial_count,'full52_exact':len(cases)==52,
        'cohort_manifest_sha256':sha(OUT/'manifest.json'),'source_pin_manifest_sha256':sha(OUT/'source-pin-manifest.json'),'plan_sha256':sha(OUT/'plan-52.json'),
        'tool_abort_recovery_sha256':migration['tool_abort_recovery_sha256'],'cases':cases,'segments':segments,
        'charged_package_wall_s':prior_wall,'process_identity_checks':identities,'first_re2_peak_checkpoints':first_re2,
        'worker_process_reports':process_reports,'closed_manifest_checks':checks.manifests,'verified_files':checks.verified,
        'limitations':['Exact intermediates do not establish physical waiting or answer RQ2/P4.',
          'Historical001 lacks creation times; historical unobserved descendants are not reconstructed.',
          'Only the pinned segment002 prepare-only tool abort is admitted; failed receipts stay FAIL_STOP.']}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--migration-file')
    parser.add_argument('--expect-full',action='store_true')
    parser.add_argument('--v2-fixture-sha256')
    parser.add_argument('--output')
    args=parser.parse_args()
    result=verify(args.migration_file,args.expect_full,args.v2_fixture_sha256)
    if args.output:
        output=Path(args.output)
        require(output.resolve().is_relative_to(BASE.resolve()) and not output.resolve().is_relative_to(OUT.resolve()),'verification output must be a new artifact outside immutable cohort')
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8',newline='\n') as stream:
            json.dump(result,stream,ensure_ascii=False,indent=2,allow_nan=False)
            stream.write('\n')
    print(json.dumps({k:result[k] for k in ('status','cohort_status','completed_case_count','remaining_case_count','full52_exact','charged_package_wall_s')},ensure_ascii=False))
    return 0


if __name__=='__main__':
    sys.dont_write_bytecode=True
    raise SystemExit(main())

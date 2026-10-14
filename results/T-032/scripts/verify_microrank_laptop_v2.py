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


def verify(migration_path=None, expect_full=False, v2_fixture_sha256=None):
    checks = Checks()
    index = checks.manifest(OUT,'manifest.json',appended_subtree='tool-check/runtime-002' if v2_fixture_sha256 else None)
    require(index['status'] in VALID_TERMINALS and index['all_controller_streams_closed'] is True, 'cohort not closed')
    status, table, plan, source_pins = (read(OUT/name) for name in ('status.json','52-cases.json','plan-52.json','source-pin-manifest.json'))
    require(status['status'] == index['status'] == table['status'] and status['active'] is None, 'cohort status differs/not idle')
    require(len(plan['rows']) == len(table['rows']) == 52 and len({(r['dataset'],r['opaque_id']) for r in plan['rows']}) == 52, 'locked 52-row set differs')
    require(sum(r['dataset']=='RE2-TT' for r in plan['rows']) == 30 and sum(r['dataset']=='Nezha-OB' for r in plan['rows']) == 22, 'dataset counts differ')
    require(table['plan_sha256'] == sha(OUT/'plan-52.json'), 'table plan pin differs')
    fixture = checks.manifest(OUT/'tool-check/runtime-001','check.json','artifact_manifest')
    require(fixture['status'] == 'PASS' and fixture['passed'] is True and fixture['frozen_self_check_count']==52
            and fixture['all_fixture_checks_passed'] is True and fixture['original_comparator_fixtures_pass'] is True, 'historical fixture invalid')
    if v2_fixture_sha256:
        checks.pin(OUT/'tool-check/runtime-002/check.json',v2_fixture_sha256)
        new_fixture = checks.manifest(OUT/'tool-check/runtime-002','check.json','artifact_manifest')
        require(new_fixture['status'] == 'PASS' and new_fixture['passed'] is True and new_fixture['frozen_self_check_count']==52
                and new_fixture['all_fixture_checks_passed'] is True and new_fixture['original_comparator_fixtures_pass'] is True, 'new wrapper fixture invalid')
    cases = []
    for locked, row in zip(plan['rows'],table['rows']):
        require(all(row[key] == value for key,value in locked.items()), 'immutable source row changed')
        require(row['case_status'] in ('PASS','not_run'), 'partial/blocked/failed row')
        if row['case_status'] == 'PASS':
            cases.append(validate_case(row,checks))
    require(status['completed_case_count'] == len(cases), 'completed count differs')
    require(table['counts']['exact'] + table['counts']['non_OK_exact'] == len(cases), 'table exact counts differ')
    require(table['counts']['not_run'] == 52-len(cases), 'table remaining count differs')
    if expect_full:
        require(len(cases)==52 and index['status']=='PASS_FULL52_LAPTOP_EXACT' and table['all_52_complete'] is True,'full52 not complete')
    migration = read(migration_path) if migration_path else None
    if migration:
        require(migration['authority']=='Q-126' and migration['root_verified'] is True,'migration not approved')
        checks.pin(OUT/'source-pin-manifest.json',migration['old_source_pin_sha256'])
        checks.pin(OUT/'plan-52.json',migration['plan_sha256'])
        checks.pin(OUT/'segments/001/launcher-closed.json',migration['initial_segment_closed_sha256'])
        checks.pin(BASE/'scripts/batch_microrank_laptop_exact_v2.py',migration['controller_sha256'])
        checks.pin(BASE/'scripts/replay_microrank_laptop_exact_v2.py',migration['wrapper_sha256'])
    segments=[]
    identities=[]
    process_reports=[]
    prior_wall=0.0 if migration is None else migration['tool_validation_wall_s']
    require(type(prior_wall) in (int,float) and 0 <= prior_wall <= 18000, 'tool-validation wall invalid')
    for directory in sorted((OUT/'segments').iterdir()):
        if not directory.is_dir():
            continue
        launcher_closed=checks.manifest(directory,'launcher-closed.json')
        launcher=read(directory/'launcher-terminal.json')
        terminal=read(directory/'terminal.json')
        require(launcher['status']==launcher_closed['status']==terminal['status'] and launcher['status'] in VALID_TERMINALS,
                'segment terminal differs/failed')
        checks.pin(directory/'terminal.json',launcher['terminal_sha256'])
        require(launcher['exit_code']==0 and launcher['all_controller_streams_closed'] is True and terminal['all_children_closed'] is True
                and terminal['active'] is None,'segment not closed')
        accounting_path=ACCOUNTING/directory.name/'accounting-closed.json'
        basis='historical measured supervisor; tail unmeasured'
        charged=launcher['elapsed_s']
        if accounting_path.is_file():
            accounting=checks.manifest(accounting_path.parent,'accounting-closed.json','artifact_manifest')
            require(accounting['status']=='PASS_ACCOUNTING_CLOSED' and accounting['supervisor_exit_code']==0 and accounting['segment_id']==directory.name
                    and accounting['all_supervisor_streams_closed'] is True,'lifetime accounting invalid')
            checks.pin(directory/'launcher-terminal.json',accounting['launcher_terminal_sha256'])
            checks.pin(directory/'launcher-closed.json',accounting['launcher_closed_sha256'])
            require(accounting['elapsed_s'] >= launcher['elapsed_s'] and abs(accounting['prior_package_wall_s']-prior_wall)<0.000001,'lifetime sum differs')
            require(accounting['closing_tail_reserve_s']==20 and abs(accounting['charged_elapsed_s']-accounting['elapsed_s']-20)<0.000001, 'final closing reserve/charge differs')
            charged=accounting['charged_elapsed_s']
            basis='actual accountant entry through supervisor exit, accounting inventory/cached hashes, plus20s conservative final receipt write reserve'
            for key in ('redirector_identity','actual_controller_identity','supervisor_identity'):
                identity=launcher.get(key)
                if identity:
                    observation=process_identity_alive(identity)
                    require(observation['alive'] is False,'recorded controller/supervisor identity alive/unknown')
                    identities.append(observation)
        elif directory.name=='001' and migration:
            require(migration['historical_unmeasured_tail_reserve_s']==20,'historical tail reserve differs')
            charged += 20
            basis='historical measured supervisor plus 20s conservative unmeasured sealing-tail reserve'
        elif directory.name!='001':
            raise ValueError('v2 segment lacks lifetime accounting')
        prior_wall += charged
        require(prior_wall <= 18000,'whole package five-hour ceiling exceeded')
        if directory.name!='001':
            require(migration is not None,'new segment requires reviewed migration')
            command=read(directory/'command.json')
            checks.pin(BASE/'scripts/batch_microrank_laptop_exact_v2.py',command['controller_sha256'])
            checks.pin(BASE/'scripts/replay_microrank_laptop_exact_v2.py',command['wrapper_sha256'])
            for process_path in sorted((directory/'logs').glob('*-process.json')):
                process_report=read(process_path)
                require(process_report['exit_code']==0 and 0 <= process_report['wall_s'] <= 600, 'process failure/cost exceeds unchanged cap')
                supervision=process_report['process_supervision']
                require(supervision['phase']==process_report['phase'] and supervision['processes'], 'process identity report absent')
                for identity in supervision['processes']:
                    require(identity['peak_lifetime_working_set_bytes'] >= 0 and identity['peak_sampled_rss_bytes'] >= 0, 'process peak invalid')
                    observation=process_identity_alive(identity)
                    require(observation['alive'] is False,'closed worker identity still alive/unknown')
                    identities.append(observation)
                process_reports.append({'path':str(process_path),'sha256':sha(process_path),'phase':process_report['phase'],
                    'process_count':len(supervision['processes']),'individual_lifetime_peak_max_bytes':supervision['individual_lifetime_peak_max_bytes'],
                    'peak_sampled_tree_rss_bytes':supervision['peak_sampled_tree_rss_bytes']})
        segments.append({'segment_id':directory.name,'status':launcher['status'],'charge_s':charged,'basis':basis,'cumulative_wall_s':prior_wall})
    first_re2=[]
    for path in sorted((OUT/'segments').glob('*/first-re2-peak.json')):
        checkpoint=read(path)
        require(checkpoint['dataset']=='RE2-TT', 'first RE2 checkpoint identity differs')
        match=[r for r in table['rows'] if r['dataset']==checkpoint['dataset'] and r['opaque_id']==checkpoint['opaque_id']]
        require(len(match)==1 and match[0]['case_status']=='PASS' and match[0]['artifacts']['closed_sha256']==checkpoint['case_closed_sha256'], 'first RE2 checkpoint not bound to exact closed case')
        measurement=checkpoint['measurement']
        require(measurement['dataset']==checkpoint['dataset'] and measurement['opaque_id']==checkpoint['opaque_id'], 'first RE2 measurement identity differs')
        for mode in ('native','observed'):
            phase=measurement[mode]
            worker_cost=measurement[mode+'_worker_cost']
            require(worker_cost['peak_rss_mb'] > 0 and phase['individual_lifetime_peak_max_bytes'] > 0, 'first RE2 lifetime peak not measured')
            require(phase['processes'] and all(p['peak_lifetime_working_set_bytes'] >= 0 for p in phase['processes']), 'first RE2 phase identities missing')
        first_re2.append({'path':str(path),'sha256':sha(path),'value':checkpoint})
    return {'schema':'T032-MicroRank-laptop-root-closed-verification-v2','status':'PASS_CLOSED_ARTIFACTS',
        'at_utc':datetime.now(timezone.utc).isoformat(),'cohort_status':status['status'],'completed_case_count':len(cases),
        'remaining_case_count':52-len(cases),'full52_exact':len(cases)==52,'cohort_manifest_sha256':sha(OUT/'manifest.json'),
        'source_pin_manifest_sha256':sha(OUT/'source-pin-manifest.json'),'plan_sha256':sha(OUT/'plan-52.json'),
        'cases':cases,'segments':segments,'charged_package_wall_s':prior_wall,'process_identity_checks':identities,
        'first_re2_peak_checkpoints':first_re2,'worker_process_reports':process_reports,'closed_manifest_checks':checks.manifests,'verified_files':checks.verified,
        'limitations':['Exact replay licenses these intermediates only; it does not establish a physical waiting mechanism or answer RQ2/P4.',
                      'Historical segment001 process receipts lack creation time; unobserved historical descendants are not reconstructed.',
                      'Existing original wrapper fixture checks are preserved; new wrapper fixture checks must be verified separately before launch.']}


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

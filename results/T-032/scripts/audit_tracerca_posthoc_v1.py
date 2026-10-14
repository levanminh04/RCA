"""Audit the approved retained TraceRCA ERROR; no ranking function is called.

The closed inventory binds the original failed directory, including its FAIL
check, source/import receipts, invocation, job, record and every capture file.
Only the logical dtype decoder is corrected in replay_tracerca_v3. A new PASS
does not rewrite or replace the original FAIL, and does not claim wait cause.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import traceback

import replay_tracerca_v3 as r

BASE = Path('/home/ubuntu/rca/T-032')
ORIGINAL = BASE / 'runs/tracerca-path-pilots-001/re2-error'
INVENTORY = BASE / 'runs/tracerca-dtype-source-inventory-001.json'
INVENTORY_SHA256 = '873f5a5ff947dfbbf3ae77168c40002cb7c8ddf64c0077ec2dd8b92ae33b159d'
OLD_WRAPPER_SHA256 = '09456386cffe618668c41d0bf1315006de0910a11241bb89b6aedb66892a75b5'
FROZEN_SHA256 = '7d4e3f96986ec5d9c1dc27f8d869b0db2eb53b75fac35c4aa95e9930d26e2b09'
SHARED_PINS = {
    'capture_tracerca.py': 'a883dfddc56abbb68447052b40764613b10b86621b9e8c80d86e143976f7ebe4',
    'replay_microrank.py': '193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562',
    'capture_microrank.py': 'b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b',
}


def require(condition, message):
    if not condition:
        raise r.ReplayError(message)


def verify_original_inventory():
    require(INVENTORY.resolve() == INVENTORY and not INVENTORY.is_symlink(), 'original inventory redirected')
    require(r.sha(INVENTORY) == INVENTORY_SHA256, 'original inventory hash differs')
    inventory = r.read(INVENTORY)
    require(inventory['root'] == str(ORIGINAL), 'original inventory points to another run')
    require(ORIGINAL.resolve() == ORIGINAL and not ORIGINAL.is_symlink(), 'original directory redirected')
    rows = inventory['files']
    seen = set()
    for row in rows:
        raw = row['path']
        relative = PurePosixPath(raw)
        require(isinstance(raw, str) and '\\' not in raw and not relative.is_absolute()
                and all(part not in ('.', '..') for part in relative.parts) and raw not in seen,
                'invalid/duplicate original artifact path')
        path = ORIGINAL / relative
        require(path.resolve().is_relative_to(ORIGINAL) and not path.is_symlink(), 'original artifact redirected')
        require(r.sha(path) == row['sha256'] and path.stat().st_size == row['bytes'], 'original artifact hash/bytes differs: ' + raw)
        seen.add(raw)
    actual = {path.relative_to(ORIGINAL).as_posix() for path in ORIGINAL.rglob('*') if path.is_file()}
    require(actual == seen, 'original full inventory missing/extra files')
    required = {'check.json', 'source.json', 'source-checks.json', 'invocation.json', 'job.json',
                'ban-ghi-0.json', 'ket-qua.json', 'capture/capture.json', 'capture/capture-start.json'}
    require(required <= seen, 'original controls incomplete')
    return inventory


def audit(out):
    before = verify_original_inventory()
    for name, expected in SHARED_PINS.items():
        require(r.sha(BASE / 'scripts' / name) == expected, 'shared dependency pin differs: ' + name)
    require(r.sha(BASE / 'scripts/replay_tracerca_v2.py') == OLD_WRAPPER_SHA256, 'preserved v2 wrapper changed')
    original_check = r.read(ORIGINAL / 'check.json')
    require(original_check['status'] == 'FAIL' and original_check.get('intermediates_eligible') is False,
            'original failure classification changed')
    require(original_check.get('type') == 'TypeError' and "data type 'string' not understood" in original_check.get('error', ''),
            'original failure is not approved dtype decoder failure')
    original_invocation = r.read(ORIGINAL / 'invocation.json')
    require(original_invocation.get('command') == 'one' and original_invocation.get('hashseed') == '0',
            'original invocation scope/hashseed differs')
    require(original_invocation['scripts']['replay_tracerca_v2.py'] == OLD_WRAPPER_SHA256,
            'original invocation wrapper pin differs')
    require(all(original_invocation['scripts'].get(name) == expected for name, expected in SHARED_PINS.items()),
            'original invocation capture/shared pin differs')
    checks = []
    r.progress(out, 'SOURCE_CHECK_START', methods_executed=False)
    entry, frozen, _index26, code_hashes = r.source_for('RE2-TT', 'dev-03d4910932', checks)
    require(entry['sha256'] == FROZEN_SHA256 and frozen['status'] == 'ERROR', 'frozen ERROR identity changed')
    external = r.external_sources(checks)
    original_source = r.read(ORIGINAL / 'source.json')
    require(original_source['dataset'] == 'RE2-TT' and original_source['opaque_id'] == 'dev-03d4910932'
            and original_source['entry'] == entry and original_source['source_status'] == 'ERROR'
            and original_source['source_run_id'] == frozen['run_id'], 'original frozen source binding differs')
    require(original_source.get('selected_allowlist_hashes_equal_frozen_inputs') is True, 'original input hash gate not passed')
    require(original_source['exact_fields'] == list(r.EXACT_FIELDS)
            and original_source['excluded_fields'] == r.EXCLUDED_FIELDS, 'original exact field policy differs')
    require(not r.exact_differences(original_source['external'], external), 'original/current external source closure differs')
    allow_path = Path(original_source['allowlist_path'])
    require(allow_path == r.safe_source('results/T-022/allowlist-dev.json') and r.sha(allow_path) == original_source['allowlist_sha256'],
            'original selected allowlist path/hash differs')
    from p3 import selector
    allow = selector.nap_allowlist(allow_path)
    wanted = {name: meta['sha256'] for name, meta in allow['dev-03d4910932']['files'].items() if meta is not None}
    require(wanted == frozen['input_sha256'], 'selected allowlist differs from frozen input hashes')
    original_job = r.read(ORIGINAL / 'job.json')
    require(original_job['kind'] == 'ranker' and original_job['method'] == 'tracerca'
            and original_job['t'] == frozen['window']['t'] and original_job['model'] is None,
            'original worker job differs from frozen invocation')
    require({name: item['sha256'] for name, item in original_job['files'].items()} == wanted,
            'original job input hashes differ')
    for row in original_source['actual_imports']:
        require(row['path'] in code_hashes and row['sha256'] == code_hashes[row['path']], 'original p3 import not frozen')
        r.verify(row['path'], row['sha256'], 'retained actual import', checks)
    original_audit = r.read(ORIGINAL / 'source-checks.json')['checks']
    require(original_audit and all(row.get('pass') is True for row in original_audit), 'original source audit failed')
    for row in original_audit:
        if row.get('authority') == 'approved TraceRCA-only source path selection':
            require(row['selected_parent'] == str(r.LOWERCASE_PARENT), 'original lowercase selection differs')
    from p3.adapters import tracerca as adapter
    native_module = importlib.import_module('RCAEval.e2e.tracerca')
    functions = {'adapter': adapter.chay, 'native': native_module.tracerca, 'operation_slo': native_module.get_operation_slo}
    start = r.read(ORIGINAL / 'capture/capture-start.json')
    require(start['packages'] == external['versions'], 'captured numerical package versions differ')
    require(start['thread_environment']['PYTHONHASHSEED'] == '0', 'captured hashseed differs')
    require(set(start['sources']) == set(functions), 'captured function source set differs')
    for name, function in functions.items():
        actual_path = Path(function.__code__.co_filename).resolve()
        recorded = start['sources'][name]
        require(recorded['path'] == str(actual_path) and recorded['sha256'] == r.sha(actual_path)
                and recorded['first_line'] == function.__code__.co_firstlineno, 'captured native/adapter function source differs: ' + name)
    summary = r.read(ORIGINAL / 'capture/capture.json')
    require(summary['status'] == 'captured_unverified_replay' and not summary['errors'], 'original capture incomplete')
    require(summary['adapter_status'] == 'ERROR' and summary['adapter_returned_status'] == 'ERROR'
            and summary['adapter_threw'] is False and summary['native_outcome'] == 'exception',
            'original ERROR native/adapter outcomes differ')
    replay = r.read(ORIGINAL / 'ban-ghi-0.json')
    differences = r.compare_records(frozen, replay)
    require(not differences, 'original record is not exactly frozen')
    r.progress(out, 'FROZEN_COMPARE_DONE', match=True, methods_executed=False)
    capture = r.verify_tracerca(ORIGINAL / 'capture', summary)
    for key in ('pass', 'hooks_restored', 'native_mutation_preserved', 'adapter_input_unchanged', 'partition_restored', 'native_slo_exact'):
        require(capture.get(key) is True, 'posthoc capture invariant missing/failed: ' + key)
    require(capture['native_outcome'] == 'exception' and capture['adapter_status'] == 'ERROR'
            and capture['adapter_threw'] is False, 'posthoc original ERROR path changed')
    actual_imports = r.loaded_sources(code_hashes)
    r.external_sources(checks)
    after = verify_original_inventory()
    require(before == after, 'original inventory changed during audit')
    r.dump(out / 'source-checks.json', {'checks': checks, 'original_source_audit_all_pass': True})
    r.progress(out, 'FINISHED', status='PASS', methods_executed=False)
    r.dump(out / 'check.json', {'status': 'PASS', 'method': 'tracerca', 'dataset': 'RE2-TT', 'opaque_id': 'dev-03d4910932',
        'frozen_path': entry['path'], 'frozen_sha256': entry['sha256'], 'frozen_status': 'ERROR', 'replay_status': replay['status'],
        'exact_fields': list(r.EXACT_FIELDS), 'excluded_fields': r.EXCLUDED_FIELDS, 'differences': differences,
        'compare': {'pass': True, 'difference_count': 0, 'exact_fields': list(r.EXACT_FIELDS), 'excluded_fields': r.EXCLUDED_FIELDS},
        'record_exact': True, 'capture_status': summary['status'], 'capture_check': capture, 'intermediates_eligible': True,
        'methods_executed': False, 'original_run': str(ORIGINAL), 'original_check_sha256': r.sha(ORIGINAL / 'check.json'),
        'original_verdict_retained': 'FAIL', 'original_full_inventory_verified': True,
        'original_inventory_path': str(INVENTORY), 'original_inventory_sha256': INVENTORY_SHA256,
        'original_artifact_manifest': before['files'], 'actual_imports_after': actual_imports,
        'table_columns_provenance': r.TABLE_COLUMNS_PROVENANCE,
        'artifact_manifest': r.artifact_manifest(out), 'manifest_excludes': ['check.json'],
        'limits': 'posthoc exact frozen ERROR and saved input/output reconstruction only; no native call; original FAIL unchanged; string backend historically unrecorded; no mechanism/wait claim'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('new_run_dir')
    args = parser.parse_args()
    require(os.name == 'posix' and Path.home() == Path('/home/ubuntu'), 'EC2 only')
    require(os.environ.get('PYTHONHASHSEED') == '0', 'hashseed must be fixed before startup')
    out = r.new_directory(args.new_run_dir)
    r.dump(out / 'invocation.json', {'argv': sys.argv, 'methods_executed': False, 'hashseed': os.environ.get('PYTHONHASHSEED'),
        'script_sha256': r.sha(__file__), 'original_inventory_path': str(INVENTORY), 'original_inventory_sha256': INVENTORY_SHA256,
        'scripts': {name: r.sha(BASE / 'scripts' / name) for name in tuple(SHARED_PINS) + ('replay_tracerca_v3.py',)}})
    try:
        audit(out)
        return 0
    except BaseException as error:
        r.progress(out, 'FAILED', methods_executed=False, error=str(error))
        r.dump(out / ('failure-after-check.json' if (out / 'check.json').exists() else 'check.json'),
            {'status': 'FAIL', 'method': 'tracerca', 'intermediates_eligible': False, 'methods_executed': False,
             'error': str(error), 'traceback': traceback.format_exc(), 'retained': 'all old/new artifacts; no retry'})
        return 1


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())

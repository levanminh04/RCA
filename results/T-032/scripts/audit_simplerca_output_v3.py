"""T-032 verify a retained SimpleRCA capture; never invokes a ranking method.

Pandas StringDtype is restored with pandas.array, not a NumPy dtype. The
original failed check remains untouched. Input hashes below bind this audit
to the first completed observed call before the verifier-only correction.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import traceback
import replay_simplerca as r

BASE = Path('/home/ubuntu/rca/T-032')
FIRST = BASE / 'runs/simplerca-re2-first-001'
FIRST_HASHES = {
    'capture/capture.json': '119183c17dcb2f1a5d60df47d7cc35e1f0e028a179ccbb32fc0ed2a3e51779c2',
    'source.json': '47ec02e915738854b34f8f85c1eca54a3426c6181f928c9a41bc9b6621ee61d0',
    'source-checks.json': '8abf90973b3b6983992dbe4ae2ffa826187664faffb9c054bad8af050eee2dd9',
    'ban-ghi-0.json': 'dd0d9fd82f586b57af4498a959e4835e4ac1eb18d20ac84330a011f50d1c160c',
    'invocation.json': 'bdd4bc31e37fa8354de824ddbf0c3bdb31f9babbcf6332a4b65e1df0ee9f1cd4',
    'check.json': '4437aad08489813eb4562c48627d36b514a807a9494c8b114adaa1cbb5f09522',
}


def table_columns(directory, meta):
    import numpy as np
    import pandas as pd
    path = (directory / meta['path']).resolve()
    if directory.resolve() not in path.parents:
        raise r.ReplayError('capture table reference escaped directory')
    stored = pd.read_parquet(path, use_threads=False)
    if len(stored) != meta['rows']:
        raise r.ReplayError('capture table row count mismatch')
    result = {}
    for column in meta['columns']:
        values = stored[column['storage']]
        dtype = pd.api.types.pandas_dtype(column['dtype'])
        extension = pd.api.types.is_extension_array_dtype(dtype)
        if column['encoding'] == 'tagged_json_scalar':
            decoded = [r.decode(json.loads(value)) for value in values]
            array = pd.array(decoded, dtype=dtype) if extension else np.asarray(decoded, dtype=dtype)
        else:
            array = pd.array(values.tolist(), dtype=dtype) if extension else values.to_numpy(dtype=dtype, copy=True)
        if 'special_state_column' in column:
            state = stored[column['special_state_column']].to_numpy()
            if not np.isin(state, [0, 1, 2, 3]).all():
                raise r.ReplayError('unknown nonfinite state')
            array[state == 1], array[state == 2], array[state == 3] = np.nan, np.inf, -np.inf
        result[r.decode(column['name'])] = array
    return result


def corrected_verifier(directory, summary):
    # Only substitute the restoration helper, never native code or its return.
    import replay_simplerca_v4 as verifier
    return verifier.verify_simplerca(directory, summary)


def fixtures(out):
    import numpy as np
    import pandas as pd
    from capture_simplerca import SimpleRcaCapture
    serializer = SimpleRcaCapture.__new__(SimpleRcaCapture)
    serializer.np, serializer.pd = np, pd
    serializer.directory = out
    serializer._artifacts = []
    serializer._table_cache = {}
    serializer._table_content = {}
    cases = []
    for name, dtype, values in [
        ('string', 'string', ['plain', '', 'tiếng Việt']), ('string_NA', 'string', ['x', pd.NA, None]),
        ('Int64', 'Int64', [1, 0, -2]), ('Int64_NA', 'Int64', [1, pd.NA, None]),
        ('boolean', 'boolean', [True, False, True]), ('boolean_NA', 'boolean', [True, pd.NA, None]),
        ('Float64', 'Float64', [1.0, -0.0, 2.5]), ('Float64_NA', 'Float64', [1.0, pd.NA, None]),
    ]:
        frame = pd.DataFrame({'message': pd.array(values, dtype=dtype)})
        frame.index.name = 'position'
        meta = serializer._table(name + '.parquet', frame)
        original = serializer._table_signature(frame)
        restored = pd.DataFrame(table_columns(out, meta))
        restored.index.name = 'position'
        actual = serializer._table_signature(restored)
        differences = r.exact_differences(original, actual)
        cases.append({'name': name, 'pass': not differences, 'differences': differences})
    r.dump(out / 'check.json', {'status': 'PASS' if all(x['pass'] for x in cases) else 'FAIL',
           'fixtures': cases, 'methods_executed': False, 'artifact_manifest': r.artifact_manifest(out)})
    return 0 if all(x['pass'] for x in cases) else 1


def audit(out):
    for relative, expected in FIRST_HASHES.items():
        if r.sha(FIRST / relative) != expected:
            raise r.ReplayError('retained pilot changed: ' + relative)
    audit_rows = []
    entry, frozen, _index, hashes = r.source_for('RE2-TT', 'dev-03d4910932', audit_rows)
    r.internal_sources(audit_rows)
    source = r.read(FIRST / 'source.json')
    if source['entry'] != entry or not source['selected_allowlist_hashes_equal_frozen_inputs']:
        raise r.ReplayError('retained source reference differs')
    for row in source['actual_imports']:
        if row['path'] not in hashes or row['sha256'] != hashes[row['path']]:
            raise r.ReplayError('retained import not frozen')
        r.verify(row['path'], row['sha256'], 'retained source actual imports', audit_rows)
    if not all(row['pass'] for row in r.read(FIRST / 'source-checks.json')['checks']):
        raise r.ReplayError('retained source check failed')
    differences = r.compare_records(frozen, r.read(FIRST / 'ban-ghi-0.json'))
    if differences:
        raise r.ReplayError('retained native record no longer exact')
    summary = r.read(FIRST / 'capture/capture.json')
    capture = corrected_verifier(FIRST / 'capture', summary)
    if not capture['pass']:
        raise r.ReplayError('capture verifier did not pass')
    r.dump(out / 'check.json', {'status': 'PASS', 'dataset': 'RE2-TT', 'method': 'simplerca',
           'opaque_id': 'dev-03d4910932', 'frozen_path': entry['path'], 'frozen_sha256': entry['sha256'],
           'record_exact': True, 'differences': differences, 'capture_check': capture,
           'original_run': str(FIRST), 'original_control_hashes': FIRST_HASHES,
           'original_artifact_manifest': r.artifact_manifest(FIRST), 'source_checks': audit_rows,
           'intermediates_eligible': True, 'methods_executed': False,
           'limits': 'value/type/order/logical dtype verified; pandas string storage backend identity was not recorded; no mechanism claim'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['fixture', 'audit'])
    parser.add_argument('output')
    args = parser.parse_args()
    if os.name != 'posix' or Path.home() != Path('/home/ubuntu'):
        raise RuntimeError('EC2 only')
    out = r.new_directory(args.output)
    r.dump(out / 'invocation.json', {'mode': args.mode, 'script_sha256': r.sha(__file__),
        'replay_script_sha256': r.sha(Path(r.__file__)), 'capture_script_sha256': r.sha(Path(r.__file__).with_name('capture_simplerca.py'))})
    try:
        code = fixtures(out) if args.mode == 'fixture' else audit(out)
        r.dump(out / 'manifest.json', {'files': r.artifact_manifest(out)})
        print('PASS' if not code else 'FAIL', flush=True)
        sys.exit(code or 0)
    except Exception as error:
        r.dump(out / 'failure.json', {'status': 'FAIL', 'error': str(error), 'traceback': traceback.format_exc(), 'methods_executed': False})
        raise

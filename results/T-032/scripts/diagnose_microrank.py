"""One Minh-approved native-only diagnostic; no permission to resume the cohort."""
import contextlib
import json
import os
from pathlib import Path
import sys
import time
import traceback

import replay_microrank as r

BASE = Path.home() / 'rca/T-032'
OLD = BASE / 'runs/re2-ok-001'
OUT = BASE / 'runs/microrank-native-diagnostic-001'
OID = 'dev-12a1a88069'


def main():
    r.new_directory(OUT)
    audit = []
    try:
        entry, frozen, index26, code_hashes = r.source_for('RE2-TT', OID, audit)
        old_check = r.read(OLD / 'check.json')
        expected = {x['path']: x for x in old_check['artifact_manifest']}
        for rel in ('job.json', 'ban-ghi-0.json', 'ket-qua.json', 'source.json'):
            assert r.sha(OLD / rel) == expected[rel]['sha256'], rel
        job = r.read(OLD / 'job.json')
        from p3 import runner, selector, worker
        from p3.adapters import microrank as adapter
        import microrank
        allow = selector.nap_allowlist(r.safe_source('results/T-022/allowlist-dev.json'))
        selected = selector.chon_ca(allow, OID, r.RE2_RAW_REPO, kiem_hash=True)
        wanted = {name: meta['sha256'] for name, meta in allow[OID]['files'].items() if meta is not None}
        assert wanted == frozen['input_sha256']
        assert job == {'kind': 'ranker', 'method': 'microrank', 't': frozen['window']['t'],
                       'model': None, 'files': {name: {'path': path, 'sha256': wanted[name]}
                                                for name, path in selected.items()}}
        assert sys.gettrace() is None and sys.getprofile() is None
        assert os.environ['PYTHONHASHSEED'] == '0'
        r.dump(OUT / 'job.json', job)
        r.dump(OUT / 'source.json', {'frozen_entry': entry, 'source_checks': audit,
               'actual_imports': r.loaded_sources(code_hashes), 'old_check_sha256': r.sha(OLD/'check.json'),
               'observer_attached': False, 'script_sha256': r.sha(__file__)})
        started = time.perf_counter()
        with (OUT/'worker-stdout.txt').open('x') as out, (OUT/'worker-stderr.txt').open('x') as err:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                worker.main(str(OUT/'job.json'), str(OUT/'ket-qua.json'))
        cost = r.measured_cost(started, 0)
        cost['env'] = 'T-032-native-only-diagnostic'
        cost['measurement_note'] = 'wall without observer; process lifetime RSS; IO not measured'
        base = {'run_id': OUT.name, 'opaque_id': OID, 'mode': 'a', 'seed': None, 'hashseed': 0,
                'detector': None, 'detector_columns': None, 'config_id': 'p3-re2tt-v2'}
        runner._ket_thuc(OUT, OUT/'ket-qua.json', [cost], base, 'microrank', 'a')
        native = r.read(OUT/'ban-ghi-0.json')
        observed = r.read(OLD/'ban-ghi-0.json')
        from_frozen = r.compare_records(frozen, native)
        from_observed = r.compare_records(observed, native)
        check = {'status': 'DIAGNOSTIC_COMPLETE', 'dataset': 'RE2-TT', 'opaque_id': OID,
                 'native_vs_frozen': {'exact_match': not from_frozen, 'differences': from_frozen},
                 'native_vs_observed': {'exact_match': not from_observed, 'differences': from_observed},
                 'actual_imports_after': r.loaded_sources(code_hashes),
                 'intermediates_eligible': False, 'cohort_resume_authorized': False,
                 'limits': 'one native-only run; isolates observer effect on this run, not the platform component causing drift',
                 'artifact_manifest': r.artifact_manifest(OUT)}
        r.dump(OUT/'check.json', check)
        print(json.dumps({'status':check['status'], 'native_vs_frozen_difference_count':len(from_frozen),
                          'native_vs_observed_difference_count':len(from_observed)}), flush=True)
        return 0
    except BaseException as exc:
        r.dump(OUT/'failure.json', {'error':str(exc), 'traceback':traceback.format_exc(), 'source_checks':audit})
        raise


if __name__ == '__main__':
    sys.exit(main())

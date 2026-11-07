"""Verify final worker forwarding of exact-read source pins; generated004 only."""
from pathlib import Path
import sys
import copy
from unittest.mock import patch
import json

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
OUT = RUN/sys.argv[1]
OUT.mkdir(exist_ok=False)
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-054/scripts'),
                'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
from bien_nhan import read_pin, ref, atomic, fingerprint, Blocked
from p3 import re3
from p3.adapters import baro
import worker

checks = []
for arm in ('M1', 'baro'):
    job = read_pin(ref(RUN/('synthetic-004/worker-'+arm+'/job.json')))
    attempt = OUT/arm; attempt.mkdir()
    pin = atomic(attempt/'job.json', job)
    raw = {'status': 'NO_EVIDENCE', 'items': [], 'ranking_native': [], 'observed_entities': ['a', 'b'],
           'method_status_raw': 'GENERATED WIRING STUB', 'input_shape': {}}
    with patch('p3.re3.read_case', wraps=re3.read_case) as reader, patch('p3.adapters.baro.chay', return_value=raw):
        worker.main(pin['path'], str(attempt), 'FINAL-WIRING-FIXTURE')
        assert reader.call_count == 1
        assert reader.call_args.kwargs['expected'] == job['source']['files']
    out = read_pin(ref(attempt/'result.json'))
    inv = read_pin(ref(attempt/'invocation.json'))
    assert inv['re3_profile_ref'] == job['re3_profile_ref']
    assert out['records'][0]['status'] == ('OK' if arm == 'M1' else 'NO_EVIDENCE')
    checks.append({'name': arm+'_worker_forwards_exact_read_pins', 'PASS': True,
                   'mocked': 'BARO method only; M1 core and both reader paths run normally'})

atomic(OUT/'checks.json', checks)
print(json.dumps({'PASS': True, 'checks': len(checks)}))

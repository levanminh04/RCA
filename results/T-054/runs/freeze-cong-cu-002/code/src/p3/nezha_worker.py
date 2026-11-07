"""Worker T-026: guard/hash → đọc cửa sổ trong RAM → gọi đúng phương pháp.

python -B -m p3.nezha_worker <job.json> <result.json>
Không lưu payload metric/span/log; parent dựng bản ghi §13 và chi phí.
"""
import argparse
import json
import os
import sys
import time
from numbers import Integral
from pathlib import Path

sys.dont_write_bytecode = True


def _json_default(value):
    if isinstance(value, Integral):
        return int(value)
    if hasattr(value, 'item'):
        return value.item()
    if hasattr(value, 'tolist'):
        return value.tolist()
    raise TypeError(type(value).__name__)


def main(job_path, result_path):
    from .nezha import nap_allowlist, chon_ca, doc_cua_so
    from .adapters.nezha import chay, METHODS, UNSUPPORTED
    from .selector import LoiRunner
    with open(job_path, encoding='utf-8-sig') as source:
        job = json.load(source)
    required = {'allowlist_path', 'opaque_id', 'repo_root', 'view', 'method', 'trace_guard_s'}
    if not required <= set(job):
        raise LoiRunner('job Nezha thiếu trường: ' + ','.join(sorted(required - set(job))))
    if any(field in job for field in ('root', 'fault', 'cell', 'case', 'label', 'nhan')):
        raise LoiRunner('job worker không nhận nhãn chấm')
    method, guard = job['method'], job['trace_guard_s']
    if method not in METHODS:
        raise LoiRunner('method ngoài phạm vi Q-85')
    if isinstance(guard, bool) or not isinstance(guard, int):
        raise LoiRunner('trace_guard_s phải là int')
    started = time.perf_counter()
    times = {}
    print('PROGRESS START method=' + method, flush=True)
    phase = time.perf_counter()
    allowlist = nap_allowlist(job['allowlist_path'])
    selection = chon_ca(allowlist, job['opaque_id'], job['repo_root'], view=job['view'])
    if guard not in (0, selection['trace_guard_s']):
        raise LoiRunner('trace_guard_s không khớp metadata ngày của ca')
    times['guard_hash'] = time.perf_counter() - phase
    print('PROGRESS GUARD_HASH_OK', flush=True)
    phase = time.perf_counter()
    if method in UNSUPPORTED:
        marker = int(selection['t_ns'])
        window = {'t_ns': marker, 'N_ns': [marker - 300_000_000_000, marker],
                  'A_ns': [marker, marker + 300_000_000_000], 'trace_guard_s': guard}
        provenance = {'source_payload_loaded': False}
        payload = None
    else:
        payload = doc_cua_so(selection, trace_guard_s=guard)
        window, provenance = payload['window'], payload['provenance']
    times['doc_cat'] = time.perf_counter() - phase
    print('PROGRESS READ_CUT_OK', flush=True)
    phase = time.perf_counter()
    results = chay(method, payload, trace_guard_s=guard)
    times['phuong_phap'] = time.perf_counter() - phase
    print('PROGRESS METHOD_DONE status=' + ','.join(result['status'] for result in results), flush=True)
    output = {'kind': 'nezha_ranker', 'method': method, 'view': selection['view'],
              'ket_qua_nhieu': results, 'window': window, 'provenance': provenance,
              'input_sha256': {rel: meta['sha256'] for rel, meta in selection['files'].items()},
              'read_columns': {'metrics': [] if payload is None else [
                  column for column in payload['metric'].columns if column != 'time']},
              'buoc_s': {key: round(value, 6) for key, value in times.items()},
              'tong_trong_tien_trinh_s': round(time.perf_counter() - started, 6),
              'hashseed': os.environ.get('PYTHONHASHSEED')}
    destination = Path(result_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2,
                                     allow_nan=False, default=_json_default) + '\n', encoding='utf-8')
    print('PROGRESS WRITTEN', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job')
    parser.add_argument('result')
    args = parser.parse_args()
    main(args.job, args.result)

"""T-026: metadata độ dài trace N main/cắt N trên 22 dev, chỉ payload RAM.

Không gọi phương pháp/evaluator hoặc đọc nhãn. Chỉ chạy sau khi các lượt
nặng đã xong. Selector/bộ đọc Nezha đã khóa giới hạn cửa sổ trước khi dùng.
Operation có <2 span N và có A chỉ liệt kê cho ca MicroRank guard ERROR.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-026'
sys.path.insert(0, str(ROOT / 'src'))
from p3 import nezha
from p3.adapters.nezha import _trace


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def local(path):
    p = (ROOT / path).resolve()
    parts = p.relative_to(ROOT).parts
    if 'locked' in parts:
        raise ValueError('không đọc data/locked')
    return p


def rel(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def dump(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def hull(frame):
    if len(frame) == 0:
        return {'spans': 0, 'first_end_ns': None, 'last_end_ns': None,
                'first_start_ns': None, 'last_start_ns': None,
                'end_hull_s': None, 'start_hull_s': None}
    st_lo, st_hi = int(frame['_start_ns'].min()), int(frame['_start_ns'].max())
    en_lo, en_hi = int(frame['_end_ns'].min()), int(frame['_end_ns'].max())
    return {'spans': int(len(frame)), 'first_end_ns': en_lo, 'last_end_ns': en_hi,
            'first_start_ns': st_lo, 'last_start_ns': st_hi,
            'end_hull_s': (en_hi - en_lo) / 1e9, 'start_hull_s': (st_hi - st_lo) / 1e9}


def operation_counts(frame):
    op = frame['serviceName'] + '_' + frame['methodName'].fillna(frame['operationName'])
    return Counter(op.tolist())


def collect(plan_path, output_path):
    output_path.relative_to(OUT / 'runs')
    if output_path.exists():
        raise FileExistsError('không ghi đè lượt coverage trước')
    progress_path = output_path.with_name(output_path.stem + '.progress.jsonl')
    failure_path = output_path.with_name(output_path.stem + '.failure.json')
    if progress_path.exists() or failure_path.exists():
        raise FileExistsError('đường dẫn lượt coverage đã dùng; giữ lượt cũ')
    started = time.perf_counter()
    plan = read(plan_path)
    # Chỉ snapshot trạng thái/bằng chứng bản ghi, không dùng root hoặc điểm.
    guard_metas = [m for m in plan['tables']['trace_guard']['records'] if m['method'] == 'microrank']
    if len(guard_metas) != 22 or len({m['opaque_id'] for m in guard_metas}) != 22:
        raise ValueError('kế hoạch không đủ 22 MicroRank guard')
    record_status, record_sources = {}, {}
    for m in guard_metas:
        p = local(m['path'])
        p.relative_to(OUT / 'runs')
        if not p.exists():
            raise ValueError('chưa xong lượt nặng; thiếu bản ghi: ' + m['path'])
        rec = read(p)
        if rec['opaque_id'] != m['opaque_id'] or rec['method'] != 'microrank' or rec['variant'] != 'full':
            raise ValueError('bản ghi MicroRank khác kế hoạch')
        record_status[m['opaque_id']] = rec['status']
        record_sources[m['opaque_id']] = {'path': m['path'], 'sha256': sha(p), 'status': rec['status']}
    allow_path = OUT / 'allowlist-dev.json'
    allow = nezha.nap_allowlist(allow_path)
    if len(allow) != 22 or set(allow) != set(record_status):
        raise ValueError('không đúng cohort 22 dev')
    cases = []
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with progress_path.open('x', encoding='utf-8', newline='\n') as progress_file:
        def progress(event, **extra):
            row = {'at_utc': now(), 'event': event, **extra}
            progress_file.write(json.dumps(row, ensure_ascii=True, allow_nan=False) + '\n')
            progress_file.flush()
            print(json.dumps(row, ensure_ascii=True), flush=True)
        progress('TRACE_N_COVERAGE_START', expected_dev=22, labels_read=False, method_called=False)
        try:
            for index, oid in enumerate(sorted(allow), 1):
                tick = time.perf_counter()
                progress('CASE_START', opaque_id=oid, index=index)
                selection = nezha.chon_ca(allow, oid, ROOT, view='main')
                payload = nezha.doc_cua_so(selection, trace_guard_s=0)
                t, guard = int(payload['t_ns']), selection['trace_guard_s']
                main, main_diag = _trace(payload, 0)
                cut, cut_diag = _trace(payload, guard)
                main_n, cut_n = main.loc[main['_end_ns'] < t], cut.loc[cut['_end_ns'] < t]
                main_a, cut_a = main.loc[main['_end_ns'] >= t], cut.loc[cut['_end_ns'] >= t]
                expected_n = main.loc[main['_end_ns'] < t - guard * 1_000_000_000]
                # _trace resets indices after the guard removes N; compare rows,
                # columns and values rather than the new ordinal index labels.
                exact_n = cut_n.reset_index(drop=True).equals(expected_n.reset_index(drop=True))
                exact_a = main_a.reset_index(drop=True).equals(cut_a.reset_index(drop=True))
                ns_us = bool(((main['_end_ns'] < t) ==
                              ((main['startTime'] + main['duration']) < t // 1000)).all())
                ns_us_cut = bool(((main['_end_ns'] < t - guard * 1_000_000_000) ==
                                  ((main['startTime'] + main['duration']) < t // 1000 - guard * 1_000_000)).all())
                if not exact_n or not exact_a or not ns_us or not ns_us_cut:
                    raise ValueError('coverage: cắt N/A/ns-us khác hợp đồng')
                low = []
                if record_status[oid] == 'ERROR':
                    nc, cc, ac = operation_counts(main_n), operation_counts(cut_n), operation_counts(main_a)
                    low = [{'operation': op, 'main_N_spans': nc[op], 'cut_N_spans': cc[op], 'A_spans': ac[op]}
                           for op in sorted(ac) if cc[op] < 2]
                cases.append({'opaque_id': oid, 't_ns': t, 'guard_s': guard,
                              'main_N_bounds_ns': [t - 300_000_000_000, t],
                              'cut_N_bounds_ns': [t - 300_000_000_000, t - guard * 1_000_000_000],
                              'main_N_nominal_s': 300, 'cut_N_nominal_s': 300 - guard,
                              'main_N_observed': hull(main_n), 'cut_N_observed': hull(cut_n),
                              'A_rows_main': int(len(main_a)), 'A_rows_cut': int(len(cut_a)),
                              'N_rows_removed': int(len(main_n) - len(cut_n)),
                              'microrank_guard_status': record_status[oid],
                              'microrank_guard_record': record_sources[oid],
                              'operations_below_two_in_cut_N_present_A': low,
                              'checks': {'cut_rule_exact': exact_n, 'A_exact_same': exact_a,
                                         'ns_us_membership': ns_us, 'ns_us_cut_membership': ns_us_cut,
                                         'clock_shift_ns': 0},
                              'input_sha256': payload['input_sha256'] if 'input_sha256' in payload
                                              else {p: m['sha256'] for p, m in selection['files'].items()},
                              'elapsed_s': round(time.perf_counter() - tick, 6)})
                progress('CASE_DONE', opaque_id=oid, index=index, elapsed_s=cases[-1]['elapsed_s'],
                         main_N_spans=len(main_n), cut_N_spans=len(cut_n),
                         guard_status=record_status[oid])
                del payload, selection, main, cut, main_n, cut_n, main_a, cut_a, expected_n
            source_files = {p: m['sha256'] for c in allow.values() for p, m in c['files'].items()}
            doc = {'created_at_utc': now(), 'dataset': 'Nezha-OB dev', 'n_cases': 22,
                   'plan': {'path': rel(plan_path), 'sha256': sha(plan_path)},
                   'allowlist': {'path': rel(allow_path), 'sha256': sha(allow_path)},
                   'code_hashes': {rel(p): sha(p) for p in [Path(__file__), ROOT / 'src/p3/nezha.py',
                                                          ROOT / 'src/p3/adapters/nezha.py']},
                   'source_files': source_files, 'source_count': len(source_files),
                   'labels_read': False, 'method_called': False, 'evaluator_called': False,
                   'payload_files': [], 'clock_shift_ns': 0,
                   'N_split': 'MicroRank/TraceRCA end < t; cut N end < t-guard; outer start>=t-300/end<t+300',
                   'observed_hull_limit': 'Min/max span timestamps are not continuous observation or independent samples.',
                   'simple_split_note': 'SimpleRCA splits by start and also applies cut end; this table reports the end-based trace N, not a SimpleRCA training duration.',
                   'cases': cases, 'microrank_guard_status_counts': dict(Counter(record_status.values())),
                   'elapsed_s': round(time.perf_counter() - started, 6)}
            dump(output_path, doc)
            progress('TRACE_N_COVERAGE_DONE', output=rel(output_path), elapsed_s=doc['elapsed_s'])
        except Exception as exc:
            dump(failure_path, {'at_utc': now(), 'error': repr(exc), 'completed_case_ids': [c['opaque_id'] for c in cases],
                                'labels_read': False, 'method_called': False, 'payload_files': [],
                                'elapsed_s': round(time.perf_counter() - started, 6)})
            progress('TRACE_N_COVERAGE_FAILED', error=repr(exc))
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', default='results/T-026/runs/full-001/plan.json')
    parser.add_argument('--output', default='results/T-026/runs/session-005/trace-N-coverage.json')
    args = parser.parse_args()
    collect(local(args.plan), local(args.output))

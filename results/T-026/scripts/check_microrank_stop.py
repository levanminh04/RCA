"""Kiểm không nhãn của điểm dừng MicroRank; không gọi phương pháp."""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import nezha
from p3.adapters.nezha import _trace


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check(oid, out):
    allow = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    selected = nezha.chon_ca(allow, oid, ROOT)
    payload = nezha.doc_cua_so(selected)
    t = payload['t_ns']
    guard = selected['trace_guard_s']
    spans = payload['spans']
    cut, diagnostics = _trace(payload, guard)
    before = spans[spans['_end_ns'] < t]
    after = spans[spans['_end_ns'] >= t]
    cut_before = cut[cut['_end_ns'] < t]
    cut_after = cut[cut['_end_ns'] >= t]

    def counts(df):
        ops = df['serviceName'] + '_' + df['methodName'].fillna(df['operationName'])
        return {str(k): int(v) for k, v in ops.value_counts().items()}

    main_n, cut_n, a = counts(before), counts(cut_before), counts(after)
    low = [{'operation': op, 'main_N_spans': main_n.get(op, 0),
            'cut_N_spans': cut_n.get(op, 0), 'A_spans': a[op]}
           for op in sorted(a) if cut_n.get(op, 0) < 2]

    def coverage(df):
        if df.empty:
            return {'spans': 0, 'end_hull_s': 0, 'start_hull_s': 0}
        return {'spans': len(df),
                'first_end_ns': int(df['_end_ns'].min()),
                'last_end_ns': int(df['_end_ns'].max()),
                'end_hull_s': float((df['_end_ns'].max() - df['_end_ns'].min()) / nezha.NS),
                'start_hull_s': float((df['_start_ns'].max() - df['_start_ns'].min()) / nezha.NS)}

    plan = json.loads((ROOT / 'results/T-026/runs/full-001/plan.json').read_text(encoding='utf-8'))
    refs = {e['source_view']: e for e in plan['unique_records']
            if e['worker_method'] == 'microrank' and e['opaque_id'] == oid}
    records = {view: json.loads((ROOT / e['path']).read_text(encoding='utf-8'))
               for view, e in refs.items() if view in ('main', 'trace_guard')}
    # Ns membership independently agrees with the exact expression of the method.
    ns_us_ok = all(((df['_end_ns'] < t) ==
                   ((df['startTime'] + df['duration']) < t // 1000)).all()
                  for df in (spans, cut))
    retained_exact = cut_before.index.size == (spans['_end_ns'] < t - guard * nezha.NS).sum()
    a_same = cut_after.reset_index(drop=True).equals(after.reset_index(drop=True))
    same_input = records['main']['input_sha256'] == records['trace_guard']['input_sha256']
    same_window = all(records['main']['window'][key] == records['trace_guard']['window'][key]
                      for key in ('t_ns', 'N_ns', 'A_ns'))
    matches_record = all(records['trace_guard']['diagnostics'][key] == diagnostics[key]
                         for key in diagnostics)
    caused_by_cut = (bool(low) and all(r['main_N_spans'] >= 2 and r['cut_N_spans'] == 1 for r in low)
                     and records['main']['status'] == 'OK' and records['trace_guard']['status'] == 'ERROR'
                     and ns_us_ok and retained_exact and a_same and same_input and same_window and matches_record)
    result = {'at_utc': datetime.now(timezone.utc).isoformat(), 'opaque_id': oid,
              'labels_read': False, 'method_called': False, 'payload_files': [],
              'guard_s': guard, 'main_N_bounds_ns': [t - 300 * nezha.NS, t],
              'cut_N_bounds_ns': [t - 300 * nezha.NS, t - guard * nezha.NS],
              'main_N_nominal_s': 300, 'cut_N_nominal_s': 300 - guard,
              'main_N_observed': coverage(before), 'cut_N_observed': coverage(cut_before),
              'operations_below_two_in_cut_N_present_A': low,
              'A_rows_main': len(after), 'A_rows_cut': len(cut_after),
              'checks': {'ns_us_membership': bool(ns_us_ok), 'cut_rule_exact': bool(retained_exact),
                         'A_exact_same': bool(a_same), 'input_hashes_same': same_input,
                         'window_t_N_A_same': same_window, 'diagnostics_match_saved': matches_record},
              'caused_by_cut_not_runner': bool(caused_by_cut),
              'evidence_records': {v: {'path': refs[v]['path'], 'sha256': sha(ROOT / refs[v]['path']),
                                       'status': records[v]['status']} for v in records},
              'code_hashes': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p)
                              for p in (ROOT / 'src/p3/nezha.py', ROOT / 'src/p3/adapters/nezha.py',
                                        ROOT / 'src/microrank/__init__.py', Path(__file__))}}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps(result, ensure_ascii=True))
    if not caused_by_cut:
        raise SystemExit('Evidence condition not satisfied; do not resume')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--opaque-id', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    check(args.opaque_id, ROOT / args.output)

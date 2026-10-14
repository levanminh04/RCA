"""Q-125 root metadata verification of closed TraceRCA segments, stdlib only.

Never invokes RCA, fixtures, adapters, table reconstruction or score formulas.
Rechecks every saved byte, pinned validator invariant, exact source record and
capture/function/import binding. Formula reconstruction remains the pinned v3
runtime proof, authenticated here by manifests. PASS is exact-replay coverage,
not manual mechanism completion or evidence of physical waiting/causality.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

BASE = Path('/home/ubuntu/rca/T-032')
RUN = BASE / 'runs/tracerca-cohort-001'
TOOLS = BASE / 'runs/tracerca-cohort-proposal-001/tool-check/tool-pins.json'
CONTROLLER = BASE / 'scripts/run_tracerca_cohort_v1.py'


def load_controller(expected):
    if hashlib.sha256(TOOLS.read_bytes()).hexdigest() != expected:
        raise RuntimeError('tool receipt hash differs before verifier import')
    pins = json.loads(TOOLS.read_text(encoding='utf-8-sig'))
    if hashlib.sha256(CONTROLLER.read_bytes()).hexdigest() != pins['scripts']['run_tracerca_cohort_v1.py']:
        raise RuntimeError('controller pin differs before stdlib-only import')
    spec = importlib.util.spec_from_file_location('tracerca_root_pinned_stdlib', CONTROLLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.tool_pins(expected)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-segment', required=True, type=int)
    parser.add_argument('--last-closure-sha256', required=True)
    parser.add_argument('--tool-pins-sha256', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    c = load_controller(args.tool_pins_sha256)
    output = Path(args.out)
    c.require(output.parent == BASE / 'runs' and output.resolve() == output
              and not output.exists() and output.name.startswith('tracerca-cohort-root-'), 'new root receipt path required')
    c.require(1 <= args.through_segment <= 49, 'invalid segment limit')
    output.mkdir()
    verdict = {'status': 'VERIFYING', 'at_utc': c.now(), 'argv': sys.argv,
               'verifier_sha256': c.sha(__file__), 'tool_pins_sha256': args.tool_pins_sha256,
               'methods_executed': False, 'fixtures_executed': False,
               'manual_complete': False, 'research_complete': False, 'physical_wait': 'OPEN'}
    try:
        rows = c.load_plan()
        validator = c.pilot_validator()
        reused = c.verify_reuse(rows, validator)
        for row in rows:
            c.source_binding(row)
        segments = sorted((RUN / 'segments').iterdir())
        c.require([p.name for p in segments] == [f'{i:03d}' for i in range(1, args.through_segment + 1)], 'extra/missing/running segment')
        table = None
        segment_proofs = []
        prior_elapsed = 0.0
        baseline = None
        pid_identities = {}
        for i, segment in enumerate(segments, 1):
            manifest_path = segment / 'closed-manifest.json'
            if i == args.through_segment:
                c.require(c.sha(manifest_path) == args.last_closure_sha256, 'last closure pin differs')
            closed = c.read(manifest_path)
            c.require(closed['root'] == str(segment) and closed['streams_closed'] is True
                      and closed['manifest_excludes'] == ['closed-manifest.json'], 'closed stream/root policy differs')
            c.verify_inventory(segment, closed['files'], ('closed-manifest.json',))
            for case in closed['case_files']:
                case_root = Path(case['directory'])
                c.require(case_root.parent == RUN / 'cases' and case_root.resolve() == case_root, 'closed case escaped run')
                c.verify_inventory(case_root, case['files'])
            terminal = c.read(segment / 'supervisor-terminal.json')
            supervisor = c.read(segment / 'supervisor-status.json')
            c.require(terminal['table_sha256'] == c.sha(segment / 'table-52.json')
                      and terminal['supervisor_status_sha256'] == c.sha(segment / 'supervisor-status.json'), 'supervisor terminal binding differs')
            pid = c.read(segment / 'supervisor.pid.json')
            pid_identities[pid['pid']] = pid['start_ticks']
            pid_identities.update({int(p): identity for p, identity in terminal['descendant_identities'].items()})
            if i < args.through_segment:
                c.require(closed['status'] == 'CHECKPOINT' and closed['controller_exit_code'] == 0
                          and closed['budget_including_close_pass'] is True, 'non-checkpoint prior segment; no continuation')
            if closed['status'] in c.SUCCESS:
                controller_terminal = c.read(segment / 'terminal.json')
                c.require(closed['controller_exit_code'] == 0 and closed['budget_including_close_pass'] is True
                          and controller_terminal['status'] == closed['status'] == supervisor['status']
                          and controller_terminal['table_sha256'] == c.sha(segment / 'table-52.json')
                          and controller_terminal['status_sha256'] == c.sha(segment / 'status.json'), 'successful terminal binding differs')
                invocation = c.read(segment / 'invocation.json')
                segment_baseline = invocation['initial_baseline_task_bytes']
                c.require(baseline is None or baseline == segment_baseline, 'baseline changed')
                baseline = segment_baseline
                c.require(invocation['plan_sha256'] == c.PLAN_SHA and invocation['forecast_sha256'] == c.FORECAST_SHA
                          and invocation['prior_inventory_sha256'] == c.PRIOR_SHA
                          and invocation['script_sha256'] == c.sha(CONTROLLER), 'controller source/plan binding differs')
                caps = invocation['caps']
                c.require(caps == {'wall_s': c.MAX_WALL_S, 'new_bytes': c.MAX_NEW_BYTES, 'case_s': c.MAX_CASE_S,
                         'case_bytes': c.MAX_CASE_BYTES, 'combined_bytes': c.MAX_COMBINED_BYTES,
                         'laptop_reserved_bytes': c.LAPTOP_RESERVE_BYTES, 'tree_rss_bytes': c.MAX_RSS_BYTES,
                         'ram_reserve_bytes': c.MIN_AVAILABLE_BYTES}, 'operating caps changed')
            else:
                c.require(closed['status'] == 'FAIL_STOP', 'unexpected closure status')
            candidate = c.read(segment / 'table-52.json')['rows']
            c.require(len(candidate) == 52 and all(all(c.identical(new[key], source[key]) for key in source)
                      for new, source in zip(candidate, rows)), '52 table/source/order binding differs')
            if table is not None:
                for old, new in zip(table, candidate):
                    if old['state'] in ('EXACT', 'REUSED_EXACT'):
                        c.require(c.identical(old, new), 'previous closed case row changed')
            table = candidate
            c.require(abs(closed['prior_segment_wall_s'] - prior_elapsed) <= 1e-6, 'cumulative segment elapsed binding differs')
            prior_elapsed += closed['segment_elapsed_s']
            c.require(supervisor['peak_tree_rss_bytes'] <= c.MAX_RSS_BYTES or closed['status'] == 'FAIL_STOP', 'RSS cap ignored')
            segment_proofs.append({'segment': i, 'status': closed['status'], 'closed_manifest_sha256': c.sha(manifest_path),
                'segment_files': len(closed['files']), 'case_manifest_count': len(closed['case_files']),
                'segment_elapsed_s': closed['segment_elapsed_s']})
        process_table = c.proc_table()
        c.require(not any(pid in process_table and process_table[pid]['start_ticks'] == identity
                         and process_table[pid]['state'] != 'Z' for pid, identity in pid_identities.items()), 'known worker/supervisor still running')
        expected_case_dirs = set()
        exact_new = 0
        checks = []
        pending_seen = False
        for row in table:
            key = (row['dataset'], row['opaque_id'])
            if key in reused:
                c.require(row['state'] == 'REUSED_EXACT' and c.identical(row['result'], reused[key]), 'reused case proof differs')
            elif row['state'] == 'EXACT':
                c.require(not pending_seen, 'new cases selected/skipped outside locked order')
                directory = RUN / 'cases' / (row['dataset'] + '-' + row['opaque_id'])
                expected_case_dirs.add(directory.name)
                proof = c.verify_case(directory, row, validator)
                c.require(c.identical(proof, row['result']) and row['record_exact'] is True
                          and row['intermediates_exact_eligible'] is True, 'closed exact row proof differs')
                invocation = c.read(directory / 'invocation.json')
                c.require(invocation['command'] == 'one' and invocation['argv'] ==
                          [str(c.WRAPPER), 'one', row['dataset'], row['opaque_id'], str(directory)], 'one native CLI invocation differs')
                exact_new += 1
                checks.append({'row_index': row['row_index'], **proof})
            else:
                pending_seen = True
                c.require(row['state'] in ('PENDING', 'FAILED', 'RUNNING') and row['record_exact'] is None
                          and row['intermediates_exact_eligible'] is False and row['result'] is None, 'unverified row promoted to usable')
                if row['state'] in ('FAILED', 'RUNNING'):
                    directory = RUN / 'cases' / (row['dataset'] + '-' + row['opaque_id'])
                    if directory.exists():
                        expected_case_dirs.add(directory.name)
                    c.require(segment_proofs[-1]['status'] == 'FAIL_STOP', 'incomplete case after successful checkpoint')
            c.require(row['physical_wait'] == 'OPEN' and row['mechanism_status'] == 'N/A_NON_OK'
                      if row['source_status'] != 'OK' else row['physical_wait'] == 'OPEN'
                      and row['mechanism_status'].startswith('OPEN'), 'mechanism/physical claim promoted')
        c.require({p.name for p in (RUN / 'cases').iterdir()} == expected_case_dirs, 'extra/unlisted case directories')
        full = segment_proofs[-1]['status'] == 'PASS_FULL_52_EXACT'
        c.require(not full or exact_new == 49 and all(r['state'] in ('EXACT', 'REUSED_EXACT') for r in table), 'full52 declared without all49new')
        if segment_proofs[-1]['status'] in c.SUCCESS:
            c.require(prior_elapsed <= c.MAX_WALL_S and baseline is not None
                      and 0 <= c.logical_size(BASE) - baseline + c.RESERVE_BYTES <= c.MAX_NEW_BYTES
                      and c.logical_size(BASE) + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES,
                      'post-close cumulative operating budget exceeded')
        verdict.update(status='PASS_CLOSED_FULL_52_EXACT' if full else
                       'PASS_CLOSED_CHECKPOINT_METADATA' if segment_proofs[-1]['status'] == 'CHECKPOINT' else 'PASS_CLOSED_FAIL_STOP_METADATA_ONLY',
                       all_52_exact=full, exact_new_case_count=exact_new, reused_case_count=3,
                       segments=segment_proofs, source_plan_sha256=c.PLAN_SHA, all_case_checks=checks,
                       processes_gone=True, cumulative_segment_wall_s=prior_elapsed,
                       remaining_research='manual full group/caller-root/control links and instrumentation semantics remain OPEN',
                       formula_note='pinned v3 captured-table/SLO/count/score reconstruction authenticated; no new scientific computation by root verifier')
    except BaseException as exc:
        verdict.update(status='FAIL_ROOT_VERIFY', error=str(exc), traceback=traceback.format_exc(), all_52_exact=False)
    c.dump_new(output / 'check.json', verdict)
    c.dump_new(output / 'manifest.json', {'status': verdict['status'], 'files': c.inventory(output),
                                         'manifest_excludes': ['manifest.json']})
    print(json.dumps({'status': verdict['status'], 'check': str(output / 'check.json')}, ensure_ascii=False))
    return 0 if verdict['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())

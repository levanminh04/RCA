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
import time

BASE = Path('/home/ubuntu/rca/T-032')
RUN = BASE / 'runs/tracerca-cohort-001'
TOOLS = BASE / 'runs/tracerca-cohort-proposal-001/tool-check-v2/tool-pins.json'
CONTROLLER = BASE / 'scripts/run_tracerca_cohort_v2.py'


def load_controller(expected):
    if hashlib.sha256(TOOLS.read_bytes()).hexdigest() != expected:
        raise RuntimeError('tool receipt hash differs before verifier import')
    pins = json.loads(TOOLS.read_text(encoding='utf-8-sig'))
    if hashlib.sha256(CONTROLLER.read_bytes()).hexdigest() != pins['scripts']['run_tracerca_cohort_v2.py']:
        raise RuntimeError('controller pin differs before stdlib-only import')
    spec = importlib.util.spec_from_file_location('tracerca_root_pinned_stdlib', CONTROLLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.tool_pins(expected)
    return module


def checkpoint(c, before, after, state, terminal, case_limit, prior_completed, routes):
    """Authenticate existing first-new-case/route stops against table transitions."""
    new_indices = []
    for i, (old, new) in enumerate(zip(before, after)):
        c.require(new['row_index'] == old['row_index'] == i, 'table row index differs')
        if old['state'] in ('EXACT', 'REUSED_EXACT'):
            c.require(c.identical(old, new), 'previous closed row changed')
        elif new['state'] == 'EXACT':
            c.require(old['state'] == 'PENDING', 'failed/running case retried')
            new_indices.append(i)
        else:
            c.require(old['state'] == new['state'] == 'PENDING', 'successful segment contains failed/running transition')
    pending_indices = [i for i, old in enumerate(before) if old['state'] == 'PENDING']
    c.require(new_indices and new_indices == pending_indices[:len(new_indices)] and len(new_indices) <= case_limit,
              'segment selected/skipped/reordered new cases')
    required_reason = None
    route_set = set(routes)
    for offset, i in enumerate(new_indices, 1):
        row = after[i]
        route = row['dataset'] + ':' + row['code_route'] + ':' + row['source_status']
        unseen = route not in route_set
        route_set.add(route)
        if required_reason is not None:
            c.require(False, 'continued past mandatory first-new-case/source-route checkpoint')
        if prior_completed + offset == 1:
            required_reason = 'FIRST_NEW_CASE'
        elif unseen:
            required_reason = 'UNSEEN_ROUTE'
        elif offset >= case_limit:
            required_reason = 'ROOT_SEGMENT_CASE_LIMIT'
    completed = prior_completed + len(new_indices)
    c.require(state['new_case_completed_total'] == terminal['new_case_completed_total'] == completed
              and state['new_routes_checked'] == sorted(route_set), 'checkpoint count/source-route coverage differs')
    full = all(row['state'] in ('EXACT', 'REUSED_EXACT') for row in after)
    if full:
        c.require(completed == 49 and state['status'] == terminal['status'] == 'PASS_FULL_52_EXACT'
                  and state['checkpoint_reason'] is None, 'full52 terminal differs')
    else:
        c.require(required_reason is not None and state['status'] == terminal['status'] == 'CHECKPOINT'
                  and state['checkpoint_reason'] == required_reason, 'mandatory checkpoint reason differs')
    return new_indices, completed, route_set


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-segment', required=True, type=int)
    parser.add_argument('--last-closure-sha256', required=True)
    parser.add_argument('--last-accounting-sha256', required=True)
    parser.add_argument('--tool-pins-sha256', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    verification_started = time.monotonic()
    c = load_controller(args.tool_pins_sha256)
    output = Path(args.out)
    c.require(output.parent == BASE / 'runs' and output.resolve() == output
              and not output.exists() and output.name.startswith('tracerca-cohort-root-'), 'new root receipt path required')
    c.require(1 <= args.through_segment <= 49, 'invalid segment limit')
    output.mkdir()
    verdict = {'status': 'VERIFYING', 'at_utc': c.now(), 'argv': sys.argv,
               'verifier_sha256': c.sha(__file__), 'tool_pins_sha256': args.tool_pins_sha256,
               'methods_executed': False, 'fixtures_executed': False, 'manual_complete': False,
               'research_complete': False, 'physical_wait': 'OPEN'}
    try:
        rows = c.load_plan()
        validator = c.pilot_validator()
        reused = c.verify_reuse(rows, validator)
        for row in rows:
            c.source_binding(row)
        segments = sorted((RUN / 'segments').iterdir())
        expected_names = [f'{i:03d}' for i in range(1, args.through_segment + 1)]
        c.require([p.name for p in segments] == expected_names
                  and [p.name for p in sorted((RUN / 'accounting').iterdir())] == expected_names, 'extra/missing/running segment/accounting')
        table = c.table_initial(rows)
        for row in table:
            key = (row['dataset'], row['opaque_id'])
            if key in reused:
                row.update(state='REUSED_EXACT', record_exact=True, intermediates_exact_eligible=True,
                           result=reused[key], mechanism_status=reused[key]['mechanism_status'])
        prior_elapsed = 0.0
        baseline = None
        completed = 0
        routes = set()
        previous_accounting_sha = None
        previous_closure_sha = None
        pid_identities = set()
        checks = []
        segment_proofs = []
        for i, segment in enumerate(segments, 1):
            closed = c.closure(segment, args.last_closure_sha256 if i == args.through_segment else None)
            c.require(closed['manifest_excludes'] == ['closed-manifest.json']
                      and closed['whole_supervisor_accounting_required'] is True, 'v2 whole accounting policy differs')
            account = c.accounting(segment, args.last_accounting_sha256 if i == args.through_segment else None)
            directory = RUN / 'accounting' / segment.name
            account_invocation = c.read(directory / 'invocation.json')
            c.require(account_invocation['tool_pins_sha256'] == args.tool_pins_sha256
                      and account_invocation['script_sha256'] == c.sha(BASE / 'scripts/start_tracerca_cohort_segment_v2.py')
                      and account_invocation['previous_accounting_sha256'] == previous_accounting_sha,
                      'accountant tool/history binding differs')
            c.require(account['prior_charged_elapsed_s'] == prior_elapsed
                      and account['previous_accounting_sha256'] == previous_accounting_sha,
                      'whole-supervisor cumulative ledger differs')
            prior_elapsed += account['charged_elapsed_s']
            current_baseline = account['initial_baseline_task_bytes']
            c.require(baseline is None or baseline == current_baseline, 'initial package baseline changed')
            baseline = current_baseline
            c.require(account['new_bytes_including_final_reserve'] == account['task_bytes_before_final_receipts'] - baseline + c.RESERVE_BYTES
                      and account['byte_reserve'] == c.RESERVE_BYTES
                      and 0 <= account['new_bytes_including_final_reserve'] <= c.MAX_NEW_BYTES
                      and account['task_bytes_before_final_receipts'] + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES
                      and prior_elapsed <= c.MAX_WALL_S, 'accounting operating cap differs')
            resource = c.read(directory / 'resource-summary.json')
            c.require(resource['resource_failure'] == [] and resource['sample_count'] > 0
                      and resource['sampled_peak_tree_rss_bytes'] <= c.MAX_RSS_BYTES
                      and resource['inventory_on_resource_thread'] is False and resource['poll_s'] == 0.1,
                      'independent resource monitor failed')
            sample_count = 0
            sampled_peak = 0
            sampled_identities = set()
            with (directory / 'resource-samples.jsonl').open(encoding='utf-8') as samples_stream:
                for line in samples_stream:
                    sample = json.loads(line)
                    c.require(isinstance(sample['sampled_tree_rss_bytes'], int)
                              and 0 <= sample['sampled_tree_rss_bytes'] <= c.MAX_RSS_BYTES
                              and isinstance(sample['available_ram_bytes'], int)
                              and sample['available_ram_bytes'] >= c.MIN_AVAILABLE_BYTES, 'saved resource sample breached cap')
                    sample_count += 1
                    sampled_peak = max(sampled_peak, sample['sampled_tree_rss_bytes'])
                    sampled_identities.update((pid, ticks) for pid, ticks in sample['identities'])
            c.require(sample_count == resource['sample_count']
                      and sampled_peak == resource['sampled_peak_tree_rss_bytes'], 'resource sample/summary binding differs')
            pid_identities.update(sampled_identities)
            for identity in resource['descendant_identities']:
                pid_identities.add((identity['pid'], identity['start_ticks']))
            accountant_pid = c.read(directory / 'accountant.pid.json')
            pid_identities.add((accountant_pid['pid'], accountant_pid['start_ticks']))
            supervisor_pid = c.read(segment / 'supervisor.pid.json')
            supervisor_process = c.read(directory / 'supervisor-process.json')
            c.require(supervisor_pid['pid'] == supervisor_process['pid']
                      and supervisor_pid['start_ticks'] == supervisor_process['start_ticks'], 'supervisor PID identity differs')
            pid_identities.add((supervisor_pid['pid'], supervisor_pid['start_ticks']))
            terminal = c.read(segment / 'supervisor-terminal.json')
            supervisor = c.read(segment / 'supervisor-status.json')
            controller_state = c.read(segment / 'status.json')
            controller_terminal = c.read(segment / 'terminal.json')
            c.require(terminal['table_sha256'] == c.sha(segment / 'table-52.json')
                      and terminal['supervisor_status_sha256'] == c.sha(segment / 'supervisor-status.json')
                      and supervisor['controller_exit_code'] == terminal['controller_exit_code'] == 0
                      and supervisor['status'] == terminal['status'] == closed['status'] == controller_terminal['status']
                      and controller_terminal['controller_exit_code'] == 0
                      and controller_terminal['table_sha256'] == c.sha(segment / 'table-52.json')
                      and controller_terminal['status_sha256'] == c.sha(segment / 'status.json'), 'successful terminal/status binding differs')
            for identity in terminal['descendant_identities']:
                pid_identities.add((identity['pid'], identity['start_ticks']))
            invocation = c.read(segment / 'invocation.json')
            c.require(invocation['initial_baseline_task_bytes'] == baseline
                      and invocation['plan_sha256'] == c.PLAN_SHA and invocation['forecast_sha256'] == c.FORECAST_SHA
                      and invocation['prior_inventory_sha256'] == c.PRIOR_SHA
                      and invocation['script_sha256'] == c.sha(CONTROLLER)
                      and invocation['tool_pins_sha256'] == args.tool_pins_sha256, 'controller source/budget binding differs')
            c.require(invocation['caps'] == {'wall_s': c.MAX_WALL_S, 'new_bytes': c.MAX_NEW_BYTES, 'case_s': c.MAX_CASE_S,
                'case_bytes': c.MAX_CASE_BYTES, 'combined_bytes': c.MAX_COMBINED_BYTES,
                'closing_allocation_s': c.CLOSING_ALLOCATION_S, 'case_closing_allocation_s': c.CASE_CLOSING_ALLOCATION_S,
                'laptop_reserved_bytes': c.LAPTOP_RESERVE_BYTES, 'tree_rss_bytes': c.MAX_RSS_BYTES,
                'ram_reserve_bytes': c.MIN_AVAILABLE_BYTES}, 'Q125 operating caps changed')
            argv = invocation['argv']
            c.require(argv[0] == str(CONTROLLER), 'controller CLI path differs')
            parse = argparse.ArgumentParser()
            parse.add_argument('--segment', type=int, required=True)
            parse.add_argument('--previous-closure-sha256')
            parse.add_argument('--previous-accounting-sha256')
            parse.add_argument('--snapshot', required=True)
            parse.add_argument('--snapshot-sha256', required=True)
            parse.add_argument('--tool-pins-sha256', required=True)
            parse.add_argument('--case-limit', type=int, required=True)
            options = parse.parse_args(argv[1:])
            c.require(options.segment == i and 1 <= options.case_limit <= 49
                      and options.previous_closure_sha256 == previous_closure_sha
                      and options.previous_accounting_sha256 == previous_accounting_sha
                      and options.tool_pins_sha256 == args.tool_pins_sha256
                      and options.snapshot == invocation['snapshot_path']
                      and options.snapshot_sha256 == invocation['snapshot_sha256']
                      and account_invocation['snapshot_sha256'] == options.snapshot_sha256
                      and account_invocation['snapshot_path'] == options.snapshot, 'segment CLI/snapshot/history differs')
            snapshot_path = Path(options.snapshot)
            c.require(snapshot_path.is_relative_to(BASE / 'runs') and snapshot_path.resolve() == snapshot_path, 'saved snapshot escaped task runs')
            c.require(c.sha(snapshot_path) == options.snapshot_sha256
                      and c.identical(c.read(options.snapshot), invocation['snapshot']), 'saved budget snapshot changed')
            snapshot = invocation['snapshot']
            snapshot_before = snapshot['remote_task_bytes']
            remaining_wall, remaining_bytes = c.package_remaining(account['prior_charged_elapsed_s'], baseline, snapshot_before)
            c.require(snapshot['micro_laptop_segment_running'] is False and snapshot['no_other_ec2_heavy_worker'] is True
                      and 0 <= snapshot['local_task_bytes'] <= c.LAPTOP_RESERVE_BYTES
                      and snapshot['laptop_reserve_bytes'] == c.LAPTOP_RESERVE_BYTES and snapshot['max_combined_bytes'] == c.MAX_COMBINED_BYTES
                      and snapshot['spec_remaining_wall_s'] >= remaining_wall
                      and snapshot['spec_remaining_new_bytes'] >= remaining_bytes, 'saved SPEC/resource budget insufficient')
            accountant_argv = account_invocation['argv']
            launcher_script = BASE / 'scripts/start_tracerca_cohort_segment_v2.py'
            c.require(accountant_argv[0] == str(launcher_script) and accountant_argv.count('--account') == 1
                      and '--supervise' not in accountant_argv, 'accountant CLI role/path differs')
            account_options = parse.parse_args([item for item in accountant_argv[1:] if item != '--account'])
            c.require(vars(account_options) == vars(options), 'accountant/controller CLI bindings differ')
            expected_supervisor_command = [str(c.PYTHON), '-B', '-X', 'utf8', str(launcher_script),
                *[item for item in accountant_argv[1:] if item != '--account'], '--supervise']
            expected_controller_command = [str(c.PYTHON), '-B', '-X', 'utf8', *argv]
            launch = c.read(segment / 'launcher.json')
            c.require(supervisor_process['command'] == account['supervisor_command']
                      == account_invocation['supervisor_command'] == expected_supervisor_command
                      and supervisor['controller_command'] == launch['controller_command']
                      == account_invocation['controller_command'] == expected_controller_command
                      and launch['accountant_pid'] == accountant_pid['pid']
                      and launch['accountant_command'] == [str(c.PYTHON), '-B', '-X', 'utf8', *accountant_argv]
                      and launch['snapshot_sha256'] == options.snapshot_sha256
                      and launch['tool_pins_sha256'] == args.tool_pins_sha256
                      and launch['detached_session'] is True and launch['single_heavy_worker'] is True
                      and launch['thread_environment_preserved'] is True, 'launch/supervisor/controller argv/PID binding differs')
            candidate = c.read(segment / 'table-52.json')['rows']
            c.require(len(candidate) == 52 and all(all(c.identical(new[key], source[key]) for key in source)
                      for new, source in zip(candidate, rows)), '52 source/main/F/a/h0/order scope differs')
            new_indices, completed, routes = checkpoint(c, table, candidate, controller_state, controller_terminal,
                                                        options.case_limit, completed, routes)
            case_seals = {Path(case['directory']).name: case for case in closed['case_files']}
            c.require(len(case_seals) == len(closed['case_files']), 'duplicate case seal')
            expected_case_seals = {row['dataset'] + '-' + row['opaque_id'] for row in candidate if row['state'] == 'EXACT'}
            c.require(set(case_seals) == expected_case_seals, 'segment case seal coverage differs')
            for name, case in case_seals.items():
                case_root = Path(case['directory'])
                c.require(case_root == RUN / 'cases' / name and case_root.resolve() == case_root, 'sealed case escaped run')
                c.verify_inventory(case_root, case['files'])
            for row_index in new_indices:
                row = candidate[row_index]
                case_root = RUN / 'cases' / (row['dataset'] + '-' + row['opaque_id'])
                proof = c.verify_case(case_root, row, validator)
                receipt = c.verify_case_receipt(segment, row)
                c.require(c.identical(proof, row['result']) and row['record_exact'] is True
                          and row['intermediates_exact_eligible'] is True, 'exact closed case proof differs')
                case_invocation = c.read(case_root / 'invocation.json')
                c.require(case_invocation['command'] == 'one' and case_invocation['argv'] ==
                          [str(c.WRAPPER), 'one', row['dataset'], row['opaque_id'], str(case_root)], 'one native invocation differs')
                pid_identities.add((receipt['pid'], receipt['start_ticks']))
                checks.append({'row_index': row_index, 'segment': i, 'case_receipt_sha256': c.sha(segment / 'logs' / f'{row_index:02d}.case-closed.json'), **proof})
            c.require({p.name for p in (segment / 'logs').glob('*.case-closed.json')}
                      == {f'{row_index:02d}.case-closed.json' for row_index in new_indices}, 'extra/missing case closing receipts')
            table = candidate
            previous_accounting_sha = c.sha(directory / 'ledger.json')
            previous_closure_sha = c.sha(segment / 'closed-manifest.json')
            segment_proofs.append({'segment': i, 'status': closed['status'], 'closed_manifest_sha256': previous_closure_sha,
                'accounting_sha256': previous_accounting_sha, 'supervisor_actual_elapsed_s': account['supervisor_actual_elapsed_s'],
                'accountant_observed_elapsed_s': account['accountant_observed_elapsed_s'],
                'closing_allocation_s': account['closing_allocation_s'], 'charged_elapsed_s': account['charged_elapsed_s'],
                'new_case_rows': new_indices, 'new_routes_checked': sorted(routes)})
            if i < args.through_segment:
                c.require(closed['status'] == 'CHECKPOINT', 'continued after full/failed segment')
        process_table = c.proc_table()
        c.require(all(isinstance(pid, int) and pid > 0 and isinstance(identity, int) and identity > 0 for pid, identity in pid_identities), 'invalid process identity')
        c.require(not any(pid in process_table and process_table[pid]['start_ticks'] == identity
                          and process_table[pid]['state'] != 'Z' for pid, identity in pid_identities), 'known process still running')
        expected_case_dirs = {row['dataset'] + '-' + row['opaque_id'] for row in table if row['state'] == 'EXACT'}
        c.require({p.name for p in (RUN / 'cases').iterdir()} == expected_case_dirs, 'extra/unlisted case directories')
        for row in table:
            if (row['dataset'], row['opaque_id']) in reused:
                c.require(row['state'] == 'REUSED_EXACT' and c.identical(row['result'], reused[(row['dataset'], row['opaque_id'])])
                          and row['record_exact'] is True and row['intermediates_exact_eligible'] is True, 'reused case exact proof differs')
            elif row['state'] == 'PENDING':
                c.require(row['record_exact'] is None and row['intermediates_exact_eligible'] is False and row['result'] is None, 'pending promoted usable')
            else:
                c.require(row['state'] == 'EXACT', 'unsuccessful case in usable segment')
            c.require(row['physical_wait'] == 'OPEN' and (row['mechanism_status'] == 'N/A_NON_OK' if row['source_status'] != 'OK'
                      else row['mechanism_status'].startswith('OPEN')), 'mechanism/physical conclusion promoted')
        current_size = c.logical_size(BASE)
        c.require(baseline is not None and 0 <= current_size - baseline + c.RESERVE_BYTES <= c.MAX_NEW_BYTES
                  and current_size + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES
                  and prior_elapsed <= c.MAX_WALL_S, 'post-close package operating budget exceeded')
        full = segment_proofs[-1]['status'] == 'PASS_FULL_52_EXACT'
        c.require(not full or completed == 49 and len(checks) == 49, 'full52 without49new exact/capped cases')
        verdict.update(status='PASS_CLOSED_FULL_52_EXACT' if full else 'PASS_CLOSED_CHECKPOINT_METADATA',
            all_52_exact=full, exact_new_case_count=completed, reused_case_count=3, segments=segment_proofs,
            source_plan_sha256=c.PLAN_SHA, all_case_checks=checks, known_processes_gone=True,
            cumulative_charged_wall_s=prior_elapsed, closing_allocations_are_measured=False,
            remaining_research='manual groups/caller-root/controls/instrumentation semantics remain OPEN',
            formula_note='unchanged pinned v3 table/SLO/count/score proof; root authenticates metadata, no RCA execution')
    except BaseException as exc:
        verdict.update(status='FAIL_ROOT_VERIFY', error=str(exc), traceback=traceback.format_exc(), all_52_exact=False,
                       eligibility='no new success claim; retain partial/failure artifacts and do not retry')
    verdict.update(root_verification_observed_wall_s=time.monotonic() - verification_started,
        root_verification_closing_allocation_s=c.CLOSING_ALLOCATION_S,
        root_verification_time_is_in_supervisor_ledger=False,
        cost_note='root metadata verification is separate measured tool cost; include it and final allocation in cumulative task/package accounting before another launch')
    c.dump_new(output / 'check.json', verdict)
    c.dump_new(output / 'manifest.json', {'status': verdict['status'], 'files': c.inventory(output), 'manifest_excludes': ['manifest.json']})
    print(json.dumps({'status': verdict['status'], 'check': str(output / 'check.json')}, ensure_ascii=False))
    return 0 if verdict['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())

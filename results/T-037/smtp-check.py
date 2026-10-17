"""T-037 SMTP contract checks and unchanged T-036 regression, outputs only in T-037.

Run after the approved shared patch and when no other heavy task is running:
  D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B results/T-037/smtp-check.py smtp-regression-001
The literal oracle was saved before this runner. All SMTP examples are synthetic.
"""
from copy import deepcopy
from datetime import datetime, timezone
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import random
import re
import subprocess
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-037'
ORACLE = BASE / 'fixtures-smtp.json'
ORACLE_SHA256 = '23642f9be9b43297dd9b74bd16bb4959c747ee27e85e9bfd02a8c1a190361330'
PIN = ROOT / 'results/T-036/runs/kiem-r1-after-002'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write('\n')


def text_save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(value)


def load_package(name, directory):
    spec = importlib.util.spec_from_file_location(
        name, directory / '__init__.py', submodule_search_locations=[str(directory)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def signatures(graph):
    return sorted([[row[key] for key in ['source', 'target', 'type', 'channel', 'messaging']]
                   for row in graph['edges']], key=canonical)


def main():
    if len(sys.argv) != 2 or not re.fullmatch('smtp-regression-[a-z0-9][a-z0-9-]*', sys.argv[1]):
        raise ValueError('new_smtp_regression_run_name_required')
    out = BASE / 'runs' / sys.argv[1]
    out.mkdir(exist_ok=False)
    started = time.perf_counter()
    checks = []
    stages = []

    def progress(stage):
        row = dict(stage=stage, elapsed_seconds=time.perf_counter() - started)
        stages.append(row)
        with (out / 'progress.jsonl').open('a', encoding='utf-8') as handle:
            handle.write(canonical(row) + '\n')

    def check(name, actual, expected=True):
        checks.append(dict(name=name, ok=actual == expected, actual=actual, expected=expected))

    def require(name, actual, expected=True):
        check(name, actual, expected)
        if actual != expected:
            raise ValueError('input_or_authorized_patch_verification_failed:' + name)

    def reject(name, function, expected):
        try:
            function()
        except ValueError as error:
            check(name, str(error).split(':')[0], expected)
        else:
            check(name, 'ACCEPTED', expected)

    try:
        save(out / 'environment.json', dict(
            command=[sys.executable, '-X', 'utf8', '-B', str(Path(__file__).resolve()), sys.argv[1]],
            python=sys.version, executable=sys.executable, platform=platform.platform(),
            device=platform.node(), started_utc=datetime.now(timezone.utc).isoformat(),
            client_timezone='Asia/Saigon', hashseed=os.getenv('PYTHONHASHSEED'),
            scope='Synthetic SMTP representation and full prior checker; no raw telemetry/test/heldout.',
            measurement_condition='Caller must ensure no concurrent heavy work; runner does not stop other processes.'))
        progress('verify-original-pin-and-approved-patch')
        require('literal_oracle_sha256', sha(ORACLE), ORACLE_SHA256)
        oracle = read(ORACLE)
        expected = oracle['literal_expectations']
        manifest_path = ROOT / oracle['old_pin']['manifest']
        require('T036_manifest_sha256', sha(manifest_path), oracle['old_pin']['manifest_sha256'])
        manifest = read(manifest_path)
        require('T036_created_utc', manifest['created_utc'], oracle['old_pin']['created_utc'])
        require('T036_current_run', manifest['current_run'], oracle['old_pin']['current_run'])
        counterexample = ROOT / oracle['source_requirement']['path']
        require('source_counterexample_sha256', sha(counterexample), oracle['source_requirement']['sha256'])
        code_hashes = read(PIN / 'code-hashes.json')
        require('snapshot_code_hashes_are_manifest_covered', next(
            row['sha256'] for row in manifest['files']
            if row['path'] == (PIN / 'code-hashes.json').relative_to(ROOT).as_posix()), sha(PIN / 'code-hashes.json'))
        old_build = PIN / 'code/build.py'
        require('old_build_sha256', sha(old_build), oracle['old_pin']['build_sha256'])
        source_checker = ROOT / 'results/T-036/check.py'
        require('original_checker_sha256', sha(source_checker), oracle['old_pin']['checker_sha256'])
        verification = []
        for original, digest in code_hashes.items():
            snapshot = PIN / 'code' / Path(original).name
            require('old_snapshot:' + original, sha(snapshot), digest)
            if original != 'src/do_thi_tinh/build.py':
                require('unchanged_shared_code:' + original, sha(ROOT / original), digest)
            verification.append(dict(path=original, snapshot_sha256=digest, current_sha256=sha(ROOT / original)))
        original_build = old_build.read_text(encoding='utf-8-sig')
        patched_build = original_build
        patch_pairs = [
            ("'deployment', 'internal', 'span-parent'}", "'deployment', 'internal', 'smtp', 'span-parent'}"),
            ("channel not in {'http', 'rpc', 'internal'}", "channel not in {'http', 'rpc', 'internal', 'smtp'}"),
        ]
        for before, after in patch_pairs:
            require('patch_anchor_once:' + before, patched_build.count(before), 1)
            patched_build = patched_build.replace(before, after, 1)
        current_build_path = ROOT / 'src/do_thi_tinh/build.py'
        current_build = current_build_path.read_text(encoding='utf-8-sig')
        require('current_build_exactly_approved_two_changes', current_build, patched_build)
        save(out / 'input-code-verification.json', verification)
        text_save(out / 'approved-build.diff', ''.join(difflib.unified_diff(
            original_build.splitlines(keepends=True), current_build.splitlines(keepends=True),
            fromfile='pinned-T036/build.py', tofile='current-src/do_thi_tinh/build.py')))
        (out / 'oracle.json').write_bytes(ORACLE.read_bytes())
        (out / 'runner.py').write_bytes(Path(__file__).read_bytes())
        (out / 'current-build.py').write_bytes(current_build_path.read_bytes())

        current = load_package('t037_smtp_current', ROOT / 'src/do_thi_tinh')
        old = load_package('t037_smtp_old', PIN / 'code')
        registry = dict(sources=[dict(id='SMTP-ORACLE', kind='synthetic', revision='smtp-oracle-v1',
            sha256=sha(ORACLE), condition='Literal synthetic fixture, not runtime or RCA benefit.')])
        document = oracle['base_document']
        save(out / 'registry.json', registry)
        save(out / 'document.json', document)
        before_input = canonical([document, registry])
        progress('smtp-build-project-and-negative-cases')
        case_outputs = []
        for relation_type in expected['smtp_call_types']:
            variant = deepcopy(document)
            variant['relations'][0]['type'] = relation_type
            snapshot = canonical([variant, registry])
            reject('old_rejects_smtp:' + relation_type,
                   lambda value=variant: old.build(value, registry), expected['old_build_smtp_error'])
            entity, operation = current.build(variant, registry)
            projected = current.project(operation)
            entity_signature = deepcopy(expected['entity_signature'])
            entity_signature[2] = relation_type
            operation_signature = deepcopy(expected['operation_signature'])
            operation_signature[2] = relation_type
            check('entity_smtp_literal:' + relation_type, signatures(entity), [entity_signature])
            check('operation_smtp_literal:' + relation_type, signatures(operation), [operation_signature])
            check('projection_smtp_literal:' + relation_type, signatures(projected), [entity_signature])
            check('smtp_record_retained:' + relation_type, entity['records'], variant['relations'])
            check('runtime_names_not_invented:' + relation_type,
                  [row['runtime_name'] for row in operation['nodes']], [None, None, None])
            check('no_static_event_count:' + relation_type,
                  all('event_count' not in edge for graph in [entity, operation] for edge in graph['edges']))
            check('build_project_inputs_unchanged:' + relation_type, canonical([variant, registry]), snapshot)
            case_outputs.append(dict(case='smtp:' + relation_type, entity=entity, operation=operation, projection=projected))

        op_to_op = deepcopy(document)
        op_to_op['relations'][0]['target']['operation'] = 'nhận tổng hợp'
        entity, operation = current.build(op_to_op, registry)
        check('operation_to_operation_literal', signatures(operation), [expected['operation_to_operation_signature']])
        check('operation_to_operation_projection', signatures(current.project(operation)), [expected['entity_signature']])
        case_outputs.append(dict(case='operation_to_operation', entity=entity, operation=operation))

        entity_only = deepcopy(document)
        entity_only['operations'] = []
        entity_only['relations'][0]['source']['operation'] = None
        entity, operation = current.build(entity_only, registry)
        projected = current.project(operation)
        for key, actual in [('entity_edge_count', len(entity['edges'])), ('operation_edge_count', len(operation['edges'])),
                            ('projection_edge_count', len(projected['edges'])), ('exclusions', operation['operation_exclusions'])]:
            check('entity_only:' + key, actual, expected['entity_only'][key])
        check('entity_only_does_not_invent_operations', operation['nodes'], [])
        check('entity_only_keeps_smtp', signatures(entity), [expected['entity_signature']])
        case_outputs.append(dict(case='entity_only', entity=entity, operation=operation, projection=projected))

        exclusions = deepcopy(document)
        internal = deepcopy(exclusions['relations'][0])
        internal.update(id='internal-call', target=dict(entity='ticket-service', operation='chuẩn bị delivery'), channel='internal')
        span_parent = deepcopy(exclusions['relations'][0])
        span_parent.update(id='span-parent-call', target=dict(entity='smtp', operation='nhận tổng hợp'),
                           type='span-parent', channel='span-parent')
        exclusions['relations'].extend([internal, span_parent])
        entity, operation = current.build(exclusions, registry)
        projected = current.project(operation)
        for key, graph in [('entity_record_ids', entity), ('operation_record_ids', operation), ('projection_record_ids', projected)]:
            actual = sorted({ident for row in graph['edges'] for ident in row['record_ids']})
            check('internal_span_parent:' + key, actual, expected['internal_and_span_parent'][key])
        check('internal_span_parent_kept_in_records', sorted(row['id'] for row in entity['records']),
              ['internal-call', 'smtp-call', 'span-parent-call'])
        check('cross_owner_span_parent_not_entity_dependency', signatures(entity), [expected['entity_signature']])
        case_outputs.append(dict(case='internal_and_span_parent', entity=entity, operation=operation, projection=projected))

        for name, relation_type in [('data_smtp', 'dữ-liệu'), ('message_smtp', 'thông-điệp'),
                                    ('deployment_smtp', 'triển-khai'), ('span_parent_smtp', 'span-parent')]:
            variant = deepcopy(document)
            variant['relations'][0]['type'] = relation_type
            snapshot = canonical(variant)
            reject('negative:' + name, lambda value=variant: current.build(value, registry), expected['negative_cases'][name])
            check('negative_input_unchanged:' + name, canonical(variant), snapshot)
        variant = deepcopy(document)
        variant['relations'][0]['channel'] = 'smtp-not-a-protocol-alias'
        reject('negative:unknown_transport', lambda: current.build(variant, registry), expected['negative_cases']['unknown_transport'])

        progress('comparison-is-structural-not-protocol-confirmation')
        comparison_doc = deepcopy(document)
        second_transport = deepcopy(comparison_doc['relations'][0])
        second_transport.update(id='http-same-endpoints', channel='http')
        comparison_doc['relations'].append(second_transport)
        static, static_operation = current.build(comparison_doc, registry)
        provenance = document['relations'][0]['provenance']
        mappings = [dict(level='entity', original=ident, candidates=[ident], verified=True, provenance=provenance)
                    for ident in ['ticket-service', 'smtp']]
        trace = dict(level='entity', nodes=[dict(id='ticket-service'), dict(id='smtp')], interval_ns=None,
                     edges=[dict(source='ticket-service', target='smtp', type='gọi-đồng-bộ',
                                 evidence_source='trace', destination=None, event_count=1,
                                 witness=[['synthetic-trace', 'synthetic-span']])])
        context = dict(system='synthetic-smtp', level='entity', domain='synthetic', trace_revision='synthetic-only',
                       revision_link_verified=False, revision_provenance=[])
        snapshot = canonical([static, trace, mappings, context, registry])
        result = current.compare(static, trace, mappings, context, registry)
        check('two_static_transports_remain_separate_before_compare', len(static['edges']), 2)
        for view in ['typed', 'endpoints']:
            data = result['views'][view]
            check('comparison:' + view + ':intersection', data['intersection'], expected['comparison'][view + '_intersection'])
            check('comparison:' + view + ':counts', [data[key] for key in ['numerator', 'static_denominator', 'trace_denominator']],
                  expected['comparison']['typed_counts'])
            originals = data['members']['static'][0]['members']
            check('comparison:' + view + ':original_static_channels',
                  sorted(row['original']['channel'] for row in originals), expected['comparison']['static_original_channels'])
        check('trace_schema_does_not_claim_transport', 'channel' in trace['edges'][0], expected['comparison']['trace_has_transport_field'])
        check('compare_all_inputs_unchanged', canonical([static, trace, mappings, context, registry]), snapshot)
        check('revision_unverified_stays_conditional', result['conditional_reference'])
        check('interpretation_stays_structural', result['interpretation'], 'structural_agreement; not runtime ground truth or RCA benefit')
        save(out / 'compare-http-smtp-same-endpoints.json', result)

        unknown_doc = deepcopy(document)
        unknown_doc['relations'][0]['type'] = 'gọi-chưa-phân-kiểu'
        unknown_static, _ = current.build(unknown_doc, registry)
        unknown_trace = deepcopy(trace)
        unknown_trace['edges'][0]['type'] = 'gọi-chưa-phân-kiểu'
        unknown = current.compare(unknown_static, unknown_trace, mappings, context, registry)
        for view in ['typed', 'endpoints']:
            check('unknown:' + view + ':counts',
                  [unknown['views'][view][key] for key in ['numerator', 'static_denominator', 'trace_denominator']],
                  expected['comparison']['unknown_type_' + view + '_counts'])
        check('unknown_typed_excludes_both',
              [unknown['views']['typed']['exclusions'][side][0]['reason'] for side in ['static', 'trace']],
              ['unknown_type', 'unknown_type'])
        save(out / 'compare-unknown-smtp.json', unknown)

        progress('determinism-and-input-immutability')
        expected_build = canonical(current.build(exclusions, registry))
        expected_comparison = canonical(result)
        for seed in expected['deterministic_seeds']:
            shuffled = deepcopy(exclusions)
            rng = random.Random(seed)
            for collection in ['entities', 'operations', 'relations', 'resource_bindings', 'signals']:
                rng.shuffle(shuffled[collection])
            check('build_reorder:' + str(seed), canonical(current.build(shuffled, registry)), expected_build)
            shuffled_mapping = deepcopy(mappings)
            rng.shuffle(shuffled_mapping)
            check('compare_mapping_reorder:' + str(seed),
                  canonical(current.compare(static, trace, shuffled_mapping, context, registry)), expected_comparison)
        check('original_fixture_and_registry_not_mutated', canonical([document, registry]), before_input)
        save(out / 'smtp-cases.json', case_outputs)

        progress('full-original-T036-checker-with-output-redirection-only')
        original = source_checker.read_text(encoding='utf-8-sig')
        adapted = original
        replacements = [
            ('ROOT = Path(__file__).resolve().parents[2]', 'ROOT = Path(' + repr(ROOT.as_posix()) + ')'),
            ("out = ROOT / 'results/T-036/runs' / sys.argv[1]", 'out = Path(' + repr((out / 't036-regression').as_posix()) + ')'),
            ("command=f'{sys.executable} -X utf8 -B results/T-036/check.py {sys.argv[1]}'",
             "command=f'{sys.executable} -X utf8 -B {Path(__file__).as_posix()} {sys.argv[1]}'"),
        ]
        for before, after in replacements:
            require('checker_adapter_anchor_once:' + before, adapted.count(before), 1)
            adapted = adapted.replace(before, after, 1)
        adapted_path = out / 'T036-check-adapted.py'
        text_save(adapted_path, adapted)
        text_save(out / 'T036-check-adaptation.diff', ''.join(difflib.unified_diff(
            original.splitlines(keepends=True), adapted.splitlines(keepends=True),
            fromfile='original-results/T-036/check.py', tofile=adapted_path.relative_to(ROOT).as_posix())))
        save(out / 'T036-check-adaptation.json', dict(
            source=str(source_checker), source_sha256=sha(source_checker), adapted_sha256=sha(adapted_path),
            changes=[dict(before=before, after=after) for before, after in replacements],
            unchanged_test_logic=True, output_root=(out / 't036-regression').as_posix()))
        command = [sys.executable, '-X', 'utf8', '-B', str(adapted_path), sys.argv[1]]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        child_started = time.perf_counter()
        with (out / 'T036-stdout.txt').open('x', encoding='utf-8') as stdout, \
                (out / 'T036-stderr.txt').open('x', encoding='utf-8') as stderr:
            child = subprocess.run(command, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, check=False)
        save(out / 'T036-command.json', dict(command=command, returncode=child.returncode,
             wall_seconds=time.perf_counter() - child_started))
        check('original_checker_exit_zero', child.returncode, 0)
        regression_path = out / 't036-regression/result.json'
        if not regression_path.is_file():
            raise ValueError('original_checker_did_not_produce_result; see retained stderr/failure')
        regression = read(regression_path)
        for key in ['passed', 'failed', 'compatibility_graph_count', 'trace_projection_pair_count']:
            check('original_checker:' + key, regression[key], expected['original_T036_regression'][key])
        check('original_checker_all_pass', regression['all_pass'])
        reference = read(PIN / 'result.json')
        check('all_221_original_check_records_unchanged', regression['checks'], reference['checks'])
        compared_artifacts = []
        for name in ['entity.json', 'operation.json', 'projection.json', 'compare-unknown.json',
                     'compare-two-queues.json', 'compare-trace-builder-messaging.json', 'r1-regression.json',
                     'trace-synthetic-messaging.json', 'compatibility.json', 'trace-projections.json']:
            check('prior_artifact_semantics_unchanged:' + name, read(out / 't036-regression' / name), read(PIN / name))
            compared_artifacts.append(dict(name=name, old_sha256=sha(PIN / name),
                new_sha256=sha(out / 't036-regression' / name)))
        save(out / 'prior-artifact-comparison.json', compared_artifacts)
        require('original_T036_checker_file_not_changed', sha(source_checker), oracle['old_pin']['checker_sha256'])
        require('old_T036_manifest_file_not_changed', sha(manifest_path), oracle['old_pin']['manifest_sha256'])
        require('shared_build_did_not_drift_during_run', current_build_path.read_text(encoding='utf-8-sig'), patched_build)
        progress('finished')
        summary = dict(task='T-037', all_pass=all(row['ok'] for row in checks),
            passed=sum(row['ok'] for row in checks), failed=sum(not row['ok'] for row in checks), checks=checks,
            seconds=time.perf_counter() - started, stages=stages,
            original_regression={key: regression[key] for key in ['passed', 'failed', 'compatibility_graph_count',
                'trace_projection_pair_count', 'seconds', 'peak_working_set_bytes', 'python_tracemalloc_peak_bytes']},
            oracle_sha256=sha(ORACLE), current_build_sha256=sha(current_build_path),
            limitation='Synthetic representation + unchanged prior regression; no runtime/protocol confirmation/RCA benefit.')
        save(out / 'result.json', summary)
        print(canonical(dict(all_pass=summary['all_pass'], passed=summary['passed'], failed=summary['failed'],
            original_regression=summary['original_regression'], output=out.as_posix())))
        return 0 if summary['all_pass'] else 1
    except Exception:
        save(out / 'failure.json', dict(traceback=traceback.format_exc(), checks=checks,
            seconds=time.perf_counter() - started, stages=stages))
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

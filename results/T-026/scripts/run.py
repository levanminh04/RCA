"""T-026: khai danh sách trước điểm, chạy tuần tự, kiểm và chốt trước evaluator.

Không đọc nhãn. Giữ mọi lượt; không ghi đè. Pilot chỉ dùng lại cùng đầu vào/hash.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-026'
sys.path.insert(0, str(ROOT / 'src'))
from p3 import ban_ghi, nezha, runner
from p3.adapters.nezha import METHODS, UNSUPPORTED, VARIANTS, VERSIONS, chay
from p3.selector import LoiRunner

WHY = ['WHY-22', 'WHY-24', 'WHY-26', 'WHY-27', 'WHY-28', 'WHY-31', 'WHY-32', 'WHY-33', 'WHY-37']
CONFIG = 't026-ob-q85-native-v1'
DERIVED = [{'id': 'microrank_top11', 'source_variant': 'full'}]

def now():
    return datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def dump(path, doc):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def rel(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()

def source_hash():
    h = hashlib.sha256()
    files = {}
    for p in sorted((ROOT / 'src/p3').rglob('*.py')):
        data = p.read_bytes()
        h.update(data)
        files[rel(p)] = hashlib.sha256(data).hexdigest()
    return {'tong': h.hexdigest(), 'tep': files}

def progress(out, event, **extra):
    row = {'at_utc': now(), 'event': event, **extra}
    with (out / 'progress.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=True, allow_nan=False) + '\n')
    print(json.dumps(row, ensure_ascii=True), flush=True)

def dependency_hashes():
    names = ['results/T-026/allowlist-dev.json', 'results/T-026/nhan-dev.json',
             'results/T-026/mappings/ob.json', 'results/T-026/config/adapter-config.json',
             'results/T-026/kiem-dau-vao.md', 'results/T-026/runs/factors-001/factors.json',
             'results/T-026/runs/pilot-001/summary.json',
             'results/T-022/giao-thuc-v2.md', 'docs/WHY.md', 'docs/DECISIONS.md',
             'tasks/T-026-nezha-ob-che-do-a/SPEC.md']
    names += [rel(p) for folder in ('src/p3', 'src/microrank', 'src/simplerca')
              for p in sorted((ROOT / folder).rglob('*.py'))]
    return {p: sha(ROOT / p) for p in names}

def method_name(method):
    return 'torai' if method == 'torai_B' else method

def verify_sources():
    doc = read(OUT / 'runs/session-004/source-integrity-final.json')
    for m in doc['files']:
        p = ROOT / m['path']
        if p.stat().st_size != m['bytes'] or sha(p) != m['sha256']:
            raise LoiRunner('source changed: ' + m['path'])
    return {'at_utc': now(), 'files_verified': len(doc['files']), 'files': doc['files'], 'payload_files': []}

def plan(out):
    out.mkdir(parents=True, exist_ok=False)
    allow = nezha.nap_allowlist(OUT / 'allowlist-dev.json')
    if len(allow) != 22:
        raise LoiRunner('expected 22 dev')
    pilot = read(OUT / 'runs/pilot-001/summary.json')
    if source_hash() != pilot['src_p3']:
        raise LoiRunner('code changed since valid pilot')
    old = {}
    for r in pilot['runs']:
        if r['hashseed'] == 0 and r['role'] in ('smallest', 'lower_median', 'largest'):
            key = (r['view'], r['method'], r['opaque_id'])
            if key in old:
                raise LoiRunner('duplicate reuse candidate')
            old[key] = ROOT / r['run_dir'] / 'ban-ghi-0.json'
    ids = sorted(allow)
    disputed = [o for o in ids if allow[o].get('t_ns_sensitivity_A') is not None]
    if len(disputed) != 1:
        raise LoiRunner('Q-84 disputed ID count')
    unique, index = [], {}

    def entry(view, method, oid):
        key = (view, method, oid)
        if key in index:
            return index[key]
        p = old.get(key)
        reuse = p is not None
        if p is None:
            p = out / f'{method}-{view}-{oid}-h0-full' / 'ban-ghi-0.json'
        e = {'opaque_id': oid, 'method': method_name(method), 'worker_method': method,
             'variant': VARIANTS[method], 'seed': None,
             'hashseed': None if method in UNSUPPORTED else 0,
             'path': rel(p), 'source_view': view, 'reused_pilot': reuse,
             'expected_t_ns': allow[oid]['t_ns_sensitivity_A'] if view == 'sensitivity_A' else allow[oid]['t_ns'],
             'trace_guard_s': allow[oid]['trace_guard_s'] if view == 'trace_guard' else 0}
        if reuse:
            e['sha256'] = sha(p)
            rec = read(p)
            validate_record(e, rec, allow)
        index[key] = e
        unique.append(e)
        return e

    tables = {}
    for table in ('main', 'sensitivity_A', 'sensitivity_B', 'trace_guard'):
        co = [o for o in ids if table != 'sensitivity_B' or o not in disputed]
        rows = []
        for method in METHODS:
            for oid in co:
                v = 'main'
                if table == 'sensitivity_A' and oid in disputed:
                    v = 'sensitivity_A'
                elif table == 'trace_guard' and method != 'baro':
                    v = 'trace_guard'
                rows.append(entry(v, method, oid))
        tables[table] = {'case_ids': co, 'records': rows}
    projection = sum(v['total_22_s'] for methods in pilot['projection'].values() for v in methods.values())
    reused_wall = sum(read(ROOT / e['path'])['cost']['wall_s'] for e in unique if e['reused_pilot'])
    doc = {'declared_at_utc': now(), 'labels_read': False, 'evaluator_called': False,
           'src_p3': source_hash(), 'source_hashes': dependency_hashes(), 'tables': tables,
           'unique_records': unique, 'derived': DERIVED, 'timeout_s': 3600,
           'reuse_rule': 'Same hash/input/window/config; cost-selected h0 pilots only; no h1/locator',
           'counts': {'unique': len(unique), 'reuse': sum(e['reused_pilot'] for e in unique),
                      'new_supported': sum(not e['reused_pilot'] and e['worker_method'] not in UNSUPPORTED for e in unique),
                      'new_unsupported': sum(not e['reused_pilot'] and e['worker_method'] in UNSUPPORTED for e in unique)},
           'cost_projection': {'unverified': True, 'main_plus_guard_s': projection,
              'reuse_recorded_wall_s': reused_wall, 'new_supported_estimate_s': projection - reused_wall + 60,
              'additional_checks_evaluator_s_scenario': [120, 600], 'total_minutes_scenario': [25, 35],
              'assumptions': 'same input factors/startup/cache; alternate four calls ~60s',
              'failure_cases': 'new operations/errors/cold IO/runtime variance'}}
    if doc['counts'] != {'unique': 248, 'reuse': 27, 'new_supported': 137, 'new_unsupported': 84}:
        raise LoiRunner('unexpected declared count: ' + str(doc['counts']))
    dump(out / 'source-integrity-before.json', verify_sources())
    dump(out / 'plan.json', doc)
    progress(out, 'PLAN_WRITTEN', counts=doc['counts'], timeout_s=3600)

def validate_record(e, rec, allow):
    for k in ('opaque_id', 'method', 'variant', 'seed', 'hashseed'):
        if rec.get(k) != e[k]:
            raise LoiRunner('record differs ' + k + ': ' + e['path'])
    if rec['mode'] != 'a' or rec['config_id'] != CONFIG:
        raise LoiRunner('wrong mode/config')
    if rec['status'] not in ('OK', 'NO_EVIDENCE', 'ERROR', 'TIMEOUT', 'UNSUPPORTED'):
        raise LoiRunner('unexpected status')
    window = rec['window']
    if window is not None and (window['t_ns'] != e['expected_t_ns'] or window['trace_guard_s'] != e['trace_guard_s']):
        raise LoiRunner('record wrong boundary/guard')
    if rec['status'] == 'UNSUPPORTED':
        if e['worker_method'] not in UNSUPPORTED or not rec.get('error') or rec['diagnostics'].get('method_called') is not False:
            raise LoiRunner('unsupported contract differs')
    elif rec['status'] != 'TIMEOUT':
        wanted = {p: m['sha256'] for p, m in allow[e['opaque_id']]['files'].items()}
        if rec['input_sha256'] != wanted:
            raise LoiRunner('input hash differs')
    ban_ghi.kiem(rec)
    rows = rec['entity_ranking']
    if len({x['entity'] for x in rows}) != len(rows):
        raise LoiRunner('duplicate entities')
    keys = [tuple(x['key']) for x in rows]
    if any(not all(math.isfinite(v) for v in key) for key in keys) or keys != sorted(keys, reverse=True):
        raise LoiRunner('nonfinite/unsorted keys')
    if rec['status'] == 'OK' and not rows:
        raise LoiRunner('OK empty')
    if rec['status'] != 'OK' and rows:
        raise LoiRunner('non-OK ranks')

def one(out, e, allow):
    method = e['worker_method']
    d = (ROOT / e['path']).parent
    d.mkdir(exist_ok=False)
    oid, guard = e['opaque_id'], e['trace_guard_s']
    view = 'sensitivity_A' if e['source_view'] == 'sensitivity_A' else 'main'
    job = {'allowlist_path': str(OUT / 'allowlist-dev.json'), 'opaque_id': oid,
           'repo_root': str(ROOT), 'view': view, 'method': method, 'trace_guard_s': guard}
    dump(d / 'job.json', job)
    progress(out, 'METHOD_START', method=method, source_view=e['source_view'], opaque_id=oid, hashseed=e['hashseed'])
    if method in UNSUPPORTED:
        start = time.perf_counter()
        selection = nezha.chon_ca(allow, oid, ROOT, view=view)
        t = selection['t_ns']
        window = {'t_ns': t, 'N_ns': [t - 300_000_000_000, t], 'A_ns': [t, t + 300_000_000_000], 'trace_guard_s': guard}
        result = chay(method)[0]
        output = {'window': window, 'input_sha256': {p: m['sha256'] for p, m in selection['files'].items()},
                  'provenance': {'source_payload_loaded': False}, 'ket_qua_nhieu': [result],
                  'buoc_s': {'guard_hash': time.perf_counter() - start, 'phuong_phap': 0}}
        dump(d / 'ket-qua.json', output)
        cost = {'wall_s': round(time.perf_counter() - start, 6), 'peak_rss_mb': None, 'read_bytes': None,
                'write_bytes': None, 'exit_code': 0, 'timed_out': False, 'env': 'parent-no-method', 'hashseed': None}
    else:
        cost = runner.chay_tien_trinh('main', ['-m', 'p3.nezha_worker', str(d / 'job.json'), str(d / 'ket-qua.json')], 3600, 0, d)
        if cost['timed_out']:
            result = {'status': 'TIMEOUT', 'error': 'timeout3600s', 'items': [], 'variant': VARIANTS[method]}
            output = {'window': None, 'input_sha256': {}, 'buoc_s': {}}
        elif cost['exit_code'] != 0 or not (d / 'ket-qua.json').exists():
            dump(d / 'cost.json', cost)
            dump(d / 'loi-runner.json', {'runner_error': True, 'cost': cost})
            raise LoiRunner('worker failed; preserve ' + rel(d))
        else:
            output = read(d / 'ket-qua.json')
            result = output['ket_qua_nhieu'][0]
    dump(d / 'cost.json', cost)
    rec = ban_ghi.tao(method_name(method), VERSIONS[method], VARIANTS[method], 'a', result,
                     output['window'], CONFIG, WHY, seed=None, hashseed=e['hashseed'], run_id=d.name, opaque_id=oid)
    rec['cost'] = {**cost, 'buoc_s': output.get('buoc_s', {})}
    rec['input_sha256'] = output['input_sha256']
    rec['extra'].update(source_view=e['source_view'], pilot_only=False, source_provenance_file='ket-qua.json')
    validate_record(e, rec, allow)
    dump(d / 'ban-ghi-0.json', rec)
    progress(out, 'METHOD_DONE', method=method, source_view=e['source_view'], opaque_id=oid,
             status=rec['status'], wall_s=cost['wall_s'], peak_rss_mb=cost['peak_rss_mb'])
    return rec

def run(out):
    doc = read(out / 'plan.json')
    if source_hash() != doc['src_p3'] or dependency_hashes() != doc['source_hashes']:
        raise LoiRunner('dependencies changed after declaration')
    allow = nezha.nap_allowlist(OUT / 'allowlist-dev.json')
    started = time.perf_counter()
    progress(out, 'FULL_START', timeout_s=3600, labels_read=False, declared_unique=248)
    done, halted = [], False
    for e in doc['unique_records']:
        if halted and e['worker_method'] == 'microrank' and not e['reused_pilot']:
            progress(out, 'MICRORANK_NOT_RUN', opaque_id=e['opaque_id'], source_view=e['source_view'])
            continue
        if e['reused_pilot']:
            if sha(ROOT / e['path']) != e['sha256']:
                raise LoiRunner('pilot record changed')
            rec = read(ROOT / e['path'])
            progress(out, 'REUSED_PILOT', path=e['path'])
        else:
            rec = one(out, e, allow)
        validate_record(e, rec, allow)
        done.append({**e, 'sha256': sha(ROOT / e['path']), 'status': rec['status'], 'cost': rec['cost']})
        if e['worker_method'] == 'microrank' and rec['status'] in ('ERROR', 'TIMEOUT'):
            halted = True
            progress(out, 'MICRORANK_BRANCH_STOP', reason='Q-77/WHY-31; report Minh', path=e['path'])
    dump(out / 'summary.json', {'at_utc': now(), 'runs': done, 'microrank_halted': halted,
          'complete': len(done) == len(doc['unique_records']), 'status_counts': dict(Counter(r['status'] for r in done)),
          'elapsed_s': time.perf_counter() - started, 'labels_read': False, 'evaluator_called': False, 'payload_files': []})
    check(out)
    progress(out, 'FULL_DONE', complete=len(done) == 248, microrank_halted=halted)

def check(out, suffix=''):
    doc = read(out / 'plan.json')
    allow = nezha.nap_allowlist(OUT / 'allowlist-dev.json')
    issues, rows = [], []
    for e in doc['unique_records']:
        p = ROOT / e['path']
        if not p.exists():
            issues.append({'path': e['path'], 'kind': 'not_run'})
            continue
        rec = read(p)
        validate_record(e, rec, allow)
        d = rec['diagnostics']
        keys = [tuple(x['key']) for x in rec['entity_ranking']]
        if any(any(abs(v) > 1e6 for v in k) for k in keys):
            issues.append({'path': e['path'], 'kind': 'key_over_1e6'})
        if d.get('all_items_tied'):
            issues.append({'path': e['path'], 'kind': 'all_items_tied'})
        rows.append({'path': e['path'], 'status': rec['status'], 'key_finite_sorted': True,
                     'observed_n': rec['sets']['observed'], 'returned_n': rec['sets']['returned'],
                     'diagnostics': d, 'input_shape': rec['input_shape']})
    diagnostic_name = 'diagnostics' + suffix + '.json'
    source_name = 'source-integrity-continued-001.json' if suffix else 'source-integrity-final.json'
    dump(out / diagnostic_name, {'at_utc': now(), 'runs': rows, 'issues': issues, 'labels_read': False,
          'evaluator_called': False, 'source_integrity': rel(out / source_name), 'payload_files': []})
    dump(out / source_name, verify_sources())

def continue_microrank(out):
    """Minh duyệt đúng10 đã khai, sau chứng minh lỗi do cắt N; giữ lịch sử."""
    proof_path = OUT / 'runs/session-005/microrank-stop-evidence-002.json'
    proof = read(proof_path)
    if not proof['caused_by_cut_not_runner'] or not all(proof['checks'].values()):
        raise LoiRunner('conditional approval not satisfied')
    doc = read(out / 'plan.json')
    history = read(out / 'summary.json')
    if history['complete'] or not history['microrank_halted']:
        raise LoiRunner('expected historical MicroRank stop')
    if source_hash() != doc['src_p3'] or dependency_hashes() != doc['source_hashes']:
        raise LoiRunner('dependencies changed after declaration')
    events = [json.loads(line) for line in (out / 'progress.jsonl').read_text(encoding='utf-8').splitlines()]
    if events[-1]['event'] != 'FULL_DONE':
        raise LoiRunner('prior heavy driver must finish')
    skipped = {e['opaque_id'] for e in events if e['event'] == 'MICRORANK_NOT_RUN'}
    exact = {'dev-607751ac0a', 'dev-63c30faf34', 'dev-6c9afc9822', 'dev-70629373f9',
             'dev-7b7c973198', 'dev-7d3c2fe6d1', 'dev-95e164235f', 'dev-9b9397a4dc',
             'dev-9fd793feb7', 'dev-b0f8b2e3ac'}
    pending = [e for e in doc['unique_records'] if not (ROOT / e['path']).exists()]
    if (skipped != exact or len(pending) != 10 or {e['opaque_id'] for e in pending} != exact
            or any(e['worker_method'] != 'microrank' or e['source_view'] != 'trace_guard'
                   or e['reused_pilot'] or e['hashseed'] != 0 for e in pending)):
        raise LoiRunner('pending differs from exact10 approved')
    for e in pending:
        if (ROOT / e['path']).parent.exists():
            raise LoiRunner('existing pending directory; do not overwrite')
    historical_files = {rel(out / name): sha(out / name) for name in
                        ('summary.json', 'diagnostics.json', 'source-integrity-final.json', 'progress.jsonl')}
    retained = {e['path']: sha(ROOT / e['path']) for e in doc['unique_records'] if e not in pending}
    authorization = {'at_utc': now(), 'source': 'Minh reply recorded verbatim in LOG: Quyết định của Minh trong phiên',
                     'conditional_scope': 'exact10 predeclared MicroRank trace_guard, unchanged configuration; preserve every ERROR',
                     'condition_proof': rel(proof_path), 'condition_proof_sha256': sha(proof_path),
                     'pending': pending, 'historical_files': historical_files, 'retained_records': retained,
                     'labels_read': False, 'evaluator_called': False}
    dump(out / 'continuation-authorization-001.json', authorization)
    snapshot = out / 'runner-source-002.py'
    with snapshot.open('xb') as f:
        f.write(Path(__file__).read_bytes())
    allow = nezha.nap_allowlist(OUT / 'allowlist-dev.json')
    started = time.perf_counter()
    progress(out, 'MICRORANK_CONTINUATION_START', exact_pending=10, condition_proof=rel(proof_path))
    for e in pending:
        one(out, e, allow)
    for path, expected in retained.items():
        if sha(ROOT / path) != expected:
            raise LoiRunner('historical record changed')
    done = []
    for e in doc['unique_records']:
        rec = read(ROOT / e['path'])
        validate_record(e, rec, allow)
        done.append({**e, 'sha256': sha(ROOT / e['path']), 'status': rec['status'], 'cost': rec['cost']})
    dump(out / 'summary-continued-001.json', {'at_utc': now(), 'runs': done, 'complete': len(done) == 248,
         'microrank_halted': False, 'historical_microrank_halted': True, 'continuation_authorized': True,
         'authorization_path': rel(out / 'continuation-authorization-001.json'),
         'historical_files': historical_files, 'status_counts': dict(Counter(r['status'] for r in done)),
         'elapsed_s': history['elapsed_s'] + time.perf_counter() - started,
         'continuation_elapsed_s': time.perf_counter() - started,
         'labels_read': False, 'evaluator_called': False, 'payload_files': []})
    check(out, '-continued-001')
    progress(out, 'MICRORANK_CONTINUATION_DONE', complete=True, exact_pending=10)

def freeze(out, fake_checks):
    if (OUT / 'ban-ghi-dua-vao-cham.json').exists():
        raise LoiRunner('do not overwrite freeze')
    plan_doc = read(out / 'plan.json')
    suffix = '-continued-001' if (out / 'summary-continued-001.json').exists() else ''
    summary = read(out / ('summary' + suffix + '.json'))
    diag = read(out / ('diagnostics' + suffix + '.json'))
    fake = read(fake_checks)
    if not summary['complete'] or summary['microrank_halted'] or diag['issues']:
        raise LoiRunner('incomplete/unresolved diagnostic; no freeze')
    if not fake.get('pass'):
        raise LoiRunner('fake evaluator checks not passed')
    if source_hash() != plan_doc['src_p3'] or dependency_hashes() != plan_doc['source_hashes']:
        raise LoiRunner('dependencies changed')
    allow = nezha.nap_allowlist(OUT / 'allowlist-dev.json')
    tables, unique = {}, []
    for e in plan_doc['unique_records']:
        p = ROOT / e['path']
        rec = read(p)
        validate_record(e, rec, allow)
        unique.append({**e, 'sha256': sha(p)})
    bypath = {e['path']: e for e in unique}
    for name, table in plan_doc['tables'].items():
        tables[name] = {'case_ids': table['case_ids'], 'records': [bypath[e['path']] for e in table['records']]}
    hashes = {**plan_doc['source_hashes'], rel(out / 'plan.json'): sha(out / 'plan.json'),
              rel(out / 'source-integrity-final.json'): sha(out / 'source-integrity-final.json'),
              rel(fake_checks): sha(fake_checks)}
    for name in ('summary' + suffix + '.json', 'diagnostics' + suffix + '.json'):
        hashes[rel(out / name)] = sha(out / name)
    if suffix:
        for name in ('source-integrity-continued-001.json', 'continuation-authorization-001.json', 'runner-source-002.py',
                     'summary.json', 'diagnostics.json'):
            hashes[rel(out / name)] = sha(out / name)
        proof = OUT / 'runs/session-005/microrank-stop-evidence-002.json'
        hashes[rel(proof)] = sha(proof)
    for p in sorted((OUT / 'scripts').glob('*.py')):
        hashes[rel(p)] = sha(p)
    external_manifest = OUT / 'runs/session-005/external-code-manifest.json'
    hashes[rel(external_manifest)] = sha(external_manifest)
    for name in ('trace-N-coverage.json', 'pre-freeze-verification.json', 'pre-freeze-verification-002.json', 'published-reference.json'):
        evidence = OUT / 'runs/session-005' / name
        hashes[rel(evidence)] = sha(evidence)
    external = read(external_manifest)['external_source_hashes']
    for name, expected in external.items():
        if sha(name) != expected:
            raise LoiRunner('external method source changed: ' + name)
    snapshot = out / 'runner-source-001.py'
    hashes[rel(snapshot)] = sha(snapshot)
    run_files = {rel(p): sha(p) for folder in {str((ROOT / e['path']).parent) for e in unique}
                 for p in Path(folder).iterdir() if p.is_file()}
    stamp = now()
    doc = {'frozen_at': stamp, 'src_p3_sha256': source_hash()['tong'], 'source_hashes': hashes,
           'tables': tables, 'unique_records': unique, 'derived': DERIVED,
           'plan_path': rel(out / 'plan.json'), 'plan_sha256': sha(out / 'plan.json'),
           'run_file_hashes': run_files, 'external_source_hashes': external,
           'labels_read': False, 'first_real_evaluator_after': stamp,
           'payload_files': []}
    dump(OUT / 'ban-ghi-dua-vao-cham.json', doc)
    log = ROOT / 'tasks/T-026-nezha-ob-che-do-a/LOG.md'
    with log.open('a', encoding='utf-8', newline='\n') as f:
        f.write(f'\n### Chốt danh sách trước evaluator thật — {stamp} (giờ máy UTC)\n\n')
        f.write('Đã chốt ban-ghi-dua-vao-cham.json: 248 bản ghi nguồn; bốn bảng tham chiếu 132/132/126/132 lượt, top11 dẫn xuất đã khai trước. Kiểm nhãn giả đã đạt; nguồn/code/manifest/diagnostic hợp lệ. Chưa đọc nhãn thật hoặc gọi evaluator thật. Sau dòng này không thêm, bỏ hoặc chạy lại bản ghi vì điểm chấm.\n')
    progress(out, 'FROZEN_BEFORE_EVALUATOR', frozen_at=stamp, unique_records=248)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stage', choices=('plan', 'run', 'continue-microrank', 'freeze'))
    ap.add_argument('--run-id', default='full-001')
    ap.add_argument('--fake-checks')
    args = ap.parse_args()
    if not args.run_id or '/' in args.run_id or '\\' in args.run_id or '..' in args.run_id:
        ap.error('invalid run-id')
    out = OUT / 'runs' / args.run_id
    try:
        if args.stage == 'plan':
            plan(out)
        elif args.stage == 'run':
            run(out)
        elif args.stage == 'continue-microrank':
            continue_microrank(out)
        else:
            if not args.fake_checks:
                ap.error('freeze requires fake checks')
            freeze(out, ROOT / args.fake_checks)
    except Exception as exc:
        if out.exists():
            failure = out / ('failure-' + args.stage + '.json')
            if not failure.exists():
                dump(failure, {'at_utc': now(), 'error': repr(exc), 'stage': args.stage})
        raise

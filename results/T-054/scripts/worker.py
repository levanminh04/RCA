"""Worker một slot, pha bền trước API. Không nhận nhãn khoa học."""
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

from bien_nhan import (ROOT, Blocked, append, atomic, fingerprint, no_labels,
                       normalized_digest, read_pin, ref)
from nguon import source_row


def setup(job):
    sys.path.insert(0, str(ROOT / 'src'))
    for p in job.get('pythonpath', []):
        sys.path.append(p)
    for p, sha in job.get('code_pins', {}).items():
        from bien_nhan import digest
        if digest(ROOT / p) != sha:
            raise Blocked('code khác pin thực chạy')
    if job['kind'] != 'synthetic':
        if job.get('evaluation_mode') not in ('dev', 'test', 'heldout'):
            raise Blocked('thiếu miền quyền dev/test trước I/O')
        if job['slot']['dataset'] == 'RE3-OB':
            from nguon import validate_re3_job
            validate_re3_job(job)
        elif job.get('evaluation_mode') == 'heldout':
            raise Blocked('heldout domain requires RE3 dataset')
        from lap_ho_so import stable_environment
        actual = stable_environment()
        expected_env = job.get('prep_environment_sha256') if job['kind'] == 'torai_prep' else job['slot']['environment_sha256']
        if fingerprint(actual) != expected_env:
            raise Blocked('môi trường thực chạy khác slot đã ghim')
        if not job.get('code_pins'):
            raise Blocked('thiếu pin code trước đọc dữ liệu')
        if job['kind'] not in ('torai_run', 'cd3'):
            from nguon import compare_sources
            r = read_pin(job['runtime_ref'])
            source = read_pin(job['independent_source_ref'])
            bindings = compare_sources(r, source, job['slot']['dataset'], job['g1_revision'])
            if bindings[job['slot']['opaque_id']] != job['slot']['source_sha256']:
                raise Blocked('source không cùng nguồn độc lập')
            if job['source'] != r['cases'][job['slot']['opaque_id']]:
                raise Blocked('job source khác runtime có biên nhận')
            if job.get('inventory') != r['inventory']:
                raise Blocked('U khác bản kê nguồn')
            if job['evaluation_mode'] == 'test':
                # Giữ nguyên guard v3; wrapper mới không thay kiểm cohort G1 hay locator.
                sys.path.append(str(ROOT / 'results/T-052/scripts'))
                import p7_guard_v3
                verified = p7_guard_v3.open_runtime(job['protocol_ref'], job['runtime_ref'],
                              job['runtime_binding_ref'], granted=True)
                if verified.receipt()['cases'][job['slot']['opaque_id']] != bindings[job['slot']['opaque_id']]:
                    raise Blocked('guard v3 và source binding không cùng ca')
            expected_t = job['source'].get('t', job['source'].get('t_ns', 0) // 10**9)
            if job['slot']['view'] == 'ce':
                expected_t -= 300
                if job['source'].get('ce_history') != 'verified':
                    raise Blocked('C-e chưa có chứng cứ lịch sử/A0 trước method')
            if job['t'] != expected_t or job['slot']['window'] != {'t': expected_t, 'half_width_s': 300}:
                raise Blocked('cửa sổ thực dùng khác nguồn và slot')
        if job['kind'] == 'm1' and fingerprint(job['config']) != job['slot']['config_sha256']:
            raise Blocked('config khác pin trước đọc dữ liệu')


def main(job_path, attempt_path, token):
    job = json.loads(Path(job_path).read_bytes())
    no_labels(job)
    setup(job)
    slot = job['slot']
    attempt = Path(attempt_path)
    phase_file = attempt / 'phases.jsonl'

    def phase(name, state='start', **extra):
        append(phase_file, dict(token=token, pid=os.getpid(), phase=name, state=state, **extra))

    def call(args, fn, **bindings):
        if slot['dataset'] == 'RE3-OB':
            bindings['re3_profile_ref'] = job['re3_profile_ref']
            re3_private_input_check(args, job)
        invocation = dict(schema='T054-INVOKE-1', slot_sha256=fingerprint(slot), token=token,
                          config_sha256=slot['config_sha256'], source_sha256=slot['source_sha256'],
                          environment_sha256=slot['environment_sha256'], window=slot['window'],
                          seed=slot['seed'], normalized_input_sha256=normalized_digest(args), **bindings)
        atomic(attempt / 'invocation.json', invocation)
        phase('method', invocation_sha256=fingerprint(invocation))
        result = fn()
        phase('method', 'end', invocation_sha256=fingerprint(invocation))
        return invocation, result

    try:
        phase('source_validation')
        kind = job['kind']
        if job.get('fixture_route'):
            from bien_nhan import OUT
            base = Path(job['data_root']).resolve()
            try:
                base.relative_to(OUT / 'runs'); inside = True
            except ValueError:
                inside = False
            if (kind != 'synthetic' or not inside or base.name != 'synthetic-data'
                    or read_pin(job['fixture_origin']).get('schema') != 'T054-GENERATED-FIXTURE'):
                raise Blocked('fixture route ngoài dữ liệu giả được sinh riêng')
            kind = job['fixture_route']
        if kind == 'synthetic':
            # Chỉ dữ liệu tổng hợp để kiểm vận hành, không đọc dataset.
            phase('source_validation', 'end')
            scenario = job.get('scenario', 'ok')
            if scenario == 'source_error':
                raise Blocked('synthetic source error')
            if scenario == 'before_method_timeout':
                phase('read'); time.sleep(job['sleep_s'])
            def fake():
                if scenario in ('method_timeout', 'slow_ok'):
                    time.sleep(job['sleep_s'])
                if scenario == 'partial':
                    (attempt / 'result.json.partial-fixture').write_text('{', encoding='utf-8')
                    os._exit(3)
                return job['synthetic_records']
            invocation, records = call(job.get('signals', {}), fake)
        elif kind == 'cd3':
            from fractions import Fraction
            from m1 import doi_chung
            from cham import main_records_from_seal
            if slot['dataset'] != 'RE2-TT' or slot['arm'] != 'C-d3':
                raise Blocked('C-d3 worker chỉ TT, OB giữ support riêng')
            if job.get('main_dependency'):
                from nguon import main_dependency_record
                source_record, actual_key = main_dependency_record(job, job['main_seal'])
                if actual_key != job['main_key']:
                    raise Blocked('C-d3 lookup không cùng khóa dependency')
            else:
                if slot['source_sha256'] != fingerprint({'seal': job['main_seal']['sha256'], 'key': job['main_key']}):
                    raise Blocked('C-d3 khác main seal/key đã khai')
                source_record = main_records_from_seal(job['main_seal'], job['main_key'])
            data = dict(source_record['extra']['dau_vao_cd3'])
            if 'canh' not in data:
                data['canh'] = source_record['extra']['canh']
            no_labels(data)
            scores = {e: Fraction(*pair) for e, pair in data['diem'].items()}
            invocation, raw = call(data, lambda: doi_chung.cd3(data['canh'], scores, data['dich']),
                                   main_seal_ref=job['main_seal'], main_key=job['main_key'],
                                   dependency_sha256=fingerprint(job.get('main_dependency')))
            records = [dict(raw, method='C-d3', variant='cd3', mode='a', seed=None, status=raw['trang_thai'])]
        elif kind == 'torai_run':
            # Chạy bằng py38. Prep do process khác đóng trước; không dựng lại seed.
            import pandas as pd
            prep = read_pin(job['prepared'])
            if prep['slot_sha256'] != fingerprint(slot) or prep['token'] != token:
                raise Blocked('prep không cùng seed/slot/token')
            phase('read_prep')
            tables = {k: pd.read_csv(read_pin_path(v)) for k, v in prep['tables'].items()}
            from p3.adapters import torai
            args = [tables[k] for k in ('metric', 'logts', 'tracets_err', 'tracets_lat')]
            run_torai = (lambda: torai.chay(*args, job['t'], slot['seed'], dataset='torai-ob')) if slot['dataset'] == 'RE3-OB' else (
                lambda: torai.chay(*args, job['t'], slot['seed']))
            invocation, raw = call(args + [job['t'], slot['seed']], run_torai, prepared_ref=job['prepared'])
            records = package(job, [raw], prep['window'])
            for record in records:
                record['extra']['chuan_bi'] = prep.get('details')
                record['extra']['information_boundary'] = ('author_full_file_retrospective'
                    if slot['arm'] == 'torai_A' else 't_plus_300')
        else:
            row = job['source']
            if fingerprint(row) != slot['source_sha256']:
                raise Blocked('source row không cùng slot')
            re3_profile = None
            if slot['dataset'] == 'RE3-OB':
                from p3 import re3
                re3_profile = re3.validate_profile(read_pin(job['re3_profile_ref']))
            files = source_row(row, job['data_root'])
            if job.get('evaluation_mode') == 'test':
                import p7_entry_v2
                checked = p7_entry_v2.source_selection(read_pin(job['runtime_ref']), slot['opaque_id'],
                           view=slot['view'], repo=job['data_root'])
                if checked is None:
                    raise Blocked('C-e insufficient cần dòng support riêng trước phát method')
            phase('source_validation', 'end')
            ds, arm = slot['dataset'], slot['arm']
            if kind == 'm1':
                from m1 import adapter, chuoi, cong, e4, hop_dong, runner
                contract = read_pin(job['m1_contract'])
                phase('adapter_read_cut')
                if ds == 'RE2-TT':
                    with patch('m1.adapter.selector.chon_ca', return_value=files):
                        data = adapter.ca_re2tt({slot['opaque_id']: row}, slot['opaque_id'], job['t'],
                                               job['data_root'], contract, job['inventory'])
                elif ds == 'RE3-OB':
                    payload = re3.read_case(files, job['t'], re3_profile, expected=row['files'])
                    data = adapter.ca_re3(payload, re3_profile, slot['opaque_id'],
                                           [slot['opaque_id'], *files.values()])
                elif ds == 'Nezha-OB':
                    selection = ob_selection(job, files)
                    with patch('m1.adapter.nezha.chon_ca', return_value=selection):
                        data = adapter.ca_nezha({}, slot['opaque_id'], job['data_root'], contract,
                                              inventory=job['inventory'], layout='source_native')
                else:
                    raise Blocked('M1 dataset has no declared adapter')
                config = job['config']
                if fingerprint(config) != slot['config_sha256']:
                    raise Blocked('config không cùng slot')
                params = runner._params(config, data)
                params['tach_cd3'] = True
                if arm == 'T12-on':
                    graph = read_pin(job['static_snapshot'])
                    params['canh_tinh'] = {'revision': job['static_snapshot']['sha256'],
                                          'canh': [[e['source'], e['target']] for e in graph['edges']]}
                chuoi._kiem_params(params)
                forbidden = [slot['opaque_id'], *files.values()]
                if ds == 'RE3-OB':
                    forbidden += [str(Path(f).parent) for f in files.values()]
                if hop_dong.vi_pham_gia_tri(params, data['aliases'], data['inventory'], forbidden):
                    raise Blocked('chuỗi riêng lọt vào API')
                args = [data['spans'], data['metrics'], data['logs'], data['inventory'], data['aliases'], job['t'], params]
                no_labels(args)
                phase('adapter_read_cut', 'end')
                chuoi.CACHE = e4.CacheCong()
                invocation, raw = call(args, lambda: chuoi.chay(*args))
                hop_dong.kiem_ban_ghi(raw)
                records = [raw]
            elif kind in ('baseline', 'torai_prep'):
                from p3 import cua_so, worker as old_worker
                phase('read')
                if ds == 'Nezha-OB':
                    from p3 import nezha
                    from p3.adapters.nezha import UNSUPPORTED, chay
                    selected = ob_selection(job, files)
                    payload = None if arm in UNSUPPORTED else nezha.doc_cua_so(
                        selected, trace_guard_s=0, layout='source_native')
                    window = (payload['window'] if payload is not None else {'t_ns': row['t_ns'],
                              'N_ns': [row['t_ns'] - 300 * nezha.NS, row['t_ns']],
                              'A_ns': [row['t_ns'], row['t_ns'] + 300 * nezha.NS], 'trace_guard_s': 0})
                    phase('read', 'end')
                    invocation, raws = call([payload, 0], lambda: chay(arm, payload, trace_guard_s=0))
                    records = package(job, raws, window)
                elif ds in ('RE2-TT', 'RE3-OB'):
                    if ds == 'RE3-OB':
                        win = re3.read_case(files, job['t'], re3_profile, expected=row['files'])
                        window = win['window']
                        phase('read', 'end'); phase('cut')
                    else:
                        metric = old_worker._doc_parquet(files, 'metrics.parquet')
                        traces = old_worker._doc_parquet(files, 'traces.parquet') if arm in ('simplerca', 'microrank', 'tracerca', 'circa', 'torai_B') else None
                        logs = old_worker._doc_parquet(files, 'logs.parquet') if arm in ('simplerca', 'torai_B') else None
                        phase('read', 'end'); phase('cut')
                        win, window = cua_so.cat_ca(metric, traces, logs, job['t'])
                    phase('cut', 'end')
                    if kind == 'torai_prep':
                        from p3.adapters import torai
                        phase('prepare')
                        prep_inputs = [win, job['t']]
                        if arm == 'torai_A':
                            from nguon import author_source
                            import pandas as pd
                            phase('author_source_validation')
                            csvs = author_source(job)
                            phase('author_source_validation', 'end'); phase('read_author')
                            source_tables = [pd.read_csv(csvs[k]) for k in ('logts', 'tracets_err', 'tracets_lat')]
                            prep_inputs.extend(source_tables)
                            phase('read_author', 'end'); phase('prepare')
                            tabs = torai.chuan_bi_A(win['metric'], *source_tables, job['t'])
                        else:
                            if ds == 'RE3-OB':
                                status_meaning = re3.validate_torai_status(win['traces']['statusCode'], re3_profile)
                                tabs = torai.chuan_bi_B(win['metric'], win['traces'], win['logs'], job['t'], chi_ts=False)
                                tabs[4]['trace_error_series_semantics'] = status_meaning
                            else:
                                tabs = torai.chuan_bi_B(win['metric'], win['traces'], win['logs'], job['t'])
                        table_refs = {}
                        for k, tab in zip(('metric', 'logts', 'tracets_err', 'tracets_lat'), tabs[:4]):
                            p = attempt / (k + '.csv')
                            tab.to_csv(p, index=False, float_format='%.17g')
                            table_refs[k] = ref(p)
                        atomic(attempt / 'prepared.json', dict(schema='T054-PREP-1', token=token,
                               slot_sha256=fingerprint(slot), tables=table_refs, window=window,
                               normalized_input_sha256=normalized_digest(prep_inputs), details=tabs[4],
                               author_source_ref=job.get('author_source_ref'),
                               **({'re3_profile_ref': job['re3_profile_ref']} if ds == 'RE3-OB' else {})))
                        phase('prepare', 'end')
                        return
                    from p3.adapters import baro, simplerca, microrank, tracerca, circa
                    functions = {'baro': lambda: [baro.chay(win['metric'], job['t'])],
                        'simplerca': lambda: [simplerca.chay(win['metric'], win['traces'], win['logs'], job['t'])],
                        'microrank': lambda: [microrank.chay(win['traces'], job['t'])],
                        'tracerca': lambda: [tracerca.chay(win['traces'], job['t'])],
                        'circa': lambda: circa.chay(win['metric'], win['traces'], job['t'], 'ols')}
                    if ds == 'RE3-OB':
                        functions.update(baro=lambda: [baro.chay(win['metric'], job['t'], dataset='re3-ob')],
                            tracerca=lambda: [tracerca.chay(win['traces'], job['t'], dataset='re3-ob')],
                            circa=lambda: circa.chay(win['metric'], win['traces'], job['t'], 'ols', dataset='re3-ob'))
                    invocation, raws = call([win, job['t']], functions[arm])
                    if arm == 'circa':
                        window['circa_current'] = raws[0].get('diagnostics', {}).get('circa_current')
                    records = package(job, raws, window)
                else:
                    raise Blocked('baseline dataset has no declared adapter')
            else:
                raise Blocked('worker kind chưa hỗ trợ')
        phase('write')
        output = dict(schema='T054-RESULT-1', token=token, slot_sha256=fingerprint(slot),
                      invocation_sha256=fingerprint(invocation), records=records,
                      record_sha256=fingerprint(records))
        no_labels(output)
        atomic(attempt / 'result.json', output)
        phase('write', 'end')
    except BaseException as exc:
        phase('exception', error_type=type(exc).__name__)
        atomic(attempt / 'failure.json', {'type': type(exc).__name__, 'classification': 'UNCLASSIFIED',
                                         'token': token, 'message': str(exc)})
        raise


def read_pin_path(pin):
    from bien_nhan import digest
    p = Path(pin['path'])
    if digest(p) != pin['sha256'] or p.stat().st_size != pin['bytes']:
        raise Blocked('CSV khác prep')
    return p


def re3_private_input_check(value, job):
    """Check values as well as keys, including object columns of signal tables."""
    paths = [str(Path(job['data_root']) / v['path']) for v in job['source']['files'].values()]
    forbidden = [job['slot']['opaque_id'], *paths]
    forbidden += [str(Path(p).parent) for p in paths]
    forbidden += [Path(p).parent.name for p in paths]

    def walk(x):
        if isinstance(x, str):
            if any(s and s in x for s in forbidden):
                raise Blocked('RE3 private locator/identifier in method input')
        elif isinstance(x, dict):
            for k, v in x.items():
                walk(k); walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
        elif hasattr(x, 'columns'):
            for c in x.columns:
                walk(c)
                for v in x[c]:
                    walk(v)
    walk(value)


def ob_selection(job, files):
    from p3 import nezha
    row = job['source']
    return {'opaque_id': job['slot']['opaque_id'], 'view': 'main', 't_ns': row['t_ns'],
            'trace_guard_s': row['trace_guard_s'],
            'files': {k: dict(row['files'][k], absolute_path=v) for k, v in files.items()},
            'universe': job['inventory'], 'aliases': dict(nezha.POD_ALIASES)}


def package(job, raws, window):
    from p3 import ban_ghi, runner
    from p3.adapters.nezha import VARIANTS, VERSIONS
    arm = job['slot']['arm']
    method = 'torai' if arm in ('torai_A', 'torai_B') else arm
    records = []
    for raw in raws:
        variant = raw.get('variant') or ('A' if arm == 'torai_A' else VARIANTS[arm])
        # M4 được ghim rõ cả đường thành công và timeout; không dùng default native.
        records.append(ban_ghi.tao(method, VERSIONS[arm] if job['slot']['dataset'] == 'Nezha-OB'
                       else job['method_version'], variant, 'a', raw, window, 'T054-P7-a', runner.WHY[method],
                       seed=job['slot']['seed'], hashseed=0))
    return records


if __name__ == '__main__':
    main(*sys.argv[1:])

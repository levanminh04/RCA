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
        if job.get('evaluation_mode') not in ('dev', 'test'):
            raise Blocked('thiếu miền quyền dev/test trước I/O')
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
            if (kind != 'synthetic' or not base.is_relative_to(OUT / 'runs') or base.name != 'synthetic-data'
                    or read_pin(job['fixture_origin']).get('schema') != 'T054-GENERATED-FIXTURE'):
                raise Blocked('fixture route ngoài dữ liệu giả được sinh riêng')
            kind = job['fixture_route']
        if kind == 'synthetic':
            # Aucune lecture de dataset; protocole de panne et transport seulement.
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
            if slot['source_sha256'] != fingerprint({'seal': job['main_seal']['sha256'], 'key': job['main_key']}):
                raise Blocked('C-d3 khác main seal/key đã khai')
            source_record = main_records_from_seal(job['main_seal'], job['main_key'])
            data = source_record['extra']['dau_vao_cd3']
            no_labels(data)
            scores = {e: Fraction(*pair) for e, pair in data['diem'].items()}
            invocation, raw = call(data, lambda: doi_chung.cd3(data['canh'], scores, data['dich']))
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
            invocation, raw = call(args + [job['t'], slot['seed']],
                                   lambda: torai.chay(*args, job['t'], slot['seed']), prepared_ref=job['prepared'])
            records = package(job, [raw], prep['window'])
        else:
            row = job['source']
            if fingerprint(row) != slot['source_sha256']:
                raise Blocked('source row không cùng slot')
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
                else:
                    selection = ob_selection(job, files)
                    with patch('m1.adapter.nezha.chon_ca', return_value=selection):
                        data = adapter.ca_nezha({}, slot['opaque_id'], job['data_root'], contract,
                                              inventory=job['inventory'])
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
                    payload = None if arm in UNSUPPORTED else nezha.doc_cua_so(selected, trace_guard_s=0)
                    window = (payload['window'] if payload is not None else {'t_ns': row['t_ns'],
                              'N_ns': [row['t_ns'] - 300 * nezha.NS, row['t_ns']],
                              'A_ns': [row['t_ns'], row['t_ns'] + 300 * nezha.NS], 'trace_guard_s': 0})
                    phase('read', 'end')
                    invocation, raws = call([payload, 0], lambda: chay(arm, payload, trace_guard_s=0))
                    records = package(job, raws, window)
                else:
                    metric = old_worker._doc_parquet(files, 'metrics.parquet')
                    traces = old_worker._doc_parquet(files, 'traces.parquet') if arm != 'baro' else None
                    logs = old_worker._doc_parquet(files, 'logs.parquet') if arm in ('simplerca', 'torai_B') else None
                    phase('read', 'end'); phase('cut')
                    win, window = cua_so.cat_ca(metric, traces, logs, job['t'])
                    phase('cut', 'end')
                    if kind == 'torai_prep':
                        from p3.adapters import torai
                        phase('prepare')
                        tabs = torai.chuan_bi_B(win['metric'], win['traces'], win['logs'], job['t'])
                        table_refs = {}
                        for k, tab in zip(('metric', 'logts', 'tracets_err', 'tracets_lat'), tabs[:4]):
                            p = attempt / (k + '.csv')
                            tab.to_csv(p, index=False, float_format='%.17g')
                            table_refs[k] = ref(p)
                        atomic(attempt / 'prepared.json', dict(schema='T054-PREP-1', token=token,
                               slot_sha256=fingerprint(slot), tables=table_refs, window=window,
                               normalized_input_sha256=normalized_digest([win, job['t']]), details=tabs[4]))
                        phase('prepare', 'end')
                        return
                    from p3.adapters import baro, simplerca, microrank, tracerca, circa
                    functions = {'baro': lambda: [baro.chay(win['metric'], job['t'])],
                        'simplerca': lambda: [simplerca.chay(win['metric'], win['traces'], win['logs'], job['t'])],
                        'microrank': lambda: [microrank.chay(win['traces'], job['t'])],
                        'tracerca': lambda: [tracerca.chay(win['traces'], job['t'])],
                        'circa': lambda: circa.chay(win['metric'], win['traces'], job['t'], 'ols')}
                    invocation, raws = call([win, job['t']], functions[arm])
                    records = package(job, raws, window)
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
    method = 'torai' if arm == 'torai_B' else arm
    records = []
    for raw in raws:
        variant = raw.get('variant') or VARIANTS[arm]
        # M4 được ghim rõ cả đường thành công và timeout; không dùng default native.
        records.append(ban_ghi.tao(method, VERSIONS[arm] if job['slot']['dataset'] == 'Nezha-OB'
                       else job['method_version'], variant, 'a', raw, window, 'T054-P7-a', runner.WHY[method],
                       seed=job['slot']['seed'], hashseed=0))
    return records


if __name__ == '__main__':
    main(*sys.argv[1:])

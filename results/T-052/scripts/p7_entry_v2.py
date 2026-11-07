"""Ứng viên điểm vào P7 local. Kế hoạch và manifest runtime được ghim độc lập."""
import hashlib
import json
import pathlib
import re
import time
from dataclasses import dataclass
from unittest.mock import patch

from common import ROOT, dump, read, save
from m1 import chuoi, hop_dong, runner
from p3 import ban_ghi, nezha, runner as p3runner, selector
from p3.adapters.nezha import VARIANTS as OB_VARIANTS, VERSIONS as OB_VERSIONS
from p7_entry import InputError, METHODS, load, no_labels, seal, join_labels, cd3_after_seal


@dataclass(frozen=True)
class Runtime:
    protocol: dict
    manifest: dict


def checked_document(path, sha256):
    raw = pathlib.Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise InputError('hash metadata không khớp nguồn khóa')
    return json.loads(raw)


def fingerprint(config):
    return hashlib.sha256(dump(config).encode('utf-8')).hexdigest()


def open_runtime(protocol_path, protocol_sha256, runtime_path, runtime_sha256, *, granted=False):
    if not granted:
        raise PermissionError('Chưa có quyền mở P7')
    protocol = checked_document(protocol_path, protocol_sha256)
    if protocol['status'] != 'LOCKED_G3':
        raise InputError('giao thức chưa khóa G3')
    cohort_ref = protocol['cohorts_source']
    plan = checked_document(ROOT / cohort_ref['path'], cohort_ref['sha256'])
    manifest = checked_document(runtime_path, runtime_sha256)
    no_labels(manifest)
    dataset = manifest['dataset']
    if dataset not in ('RE2-TT', 'Nezha-OB'):
        raise InputError('nguồn ngoài P7(a)')
    members = plan['cohorts'][dataset]['members_locked_sha256']
    expected = {'test-' + sha[:10]: sha for sha in members}
    actual = {oid: row['member_sha256'] for oid, row in manifest['cases'].items()}
    if len(expected) != len(members) or actual != expected or manifest['inventory'] != plan['inventory'][dataset]:
        raise InputError('manifest runtime không khớp toàn bộ cohort/inventory G1')
    return Runtime(protocol, manifest)


def source_selection(manifest, oid, *, view='main', repo=ROOT):
    """Chỉ gọi sau open_runtime. Kiểm toàn bộ locator trước stat/hash payload."""
    ds = manifest['dataset']
    if oid not in manifest['cases']:
        raise InputError('ca ngoài cohort đã khóa')
    case = manifest['cases'][oid]
    if ds not in ('RE2-TT', 'Nezha-OB') or view not in ('main', 'ce') or (view == 'ce' and ds != 'RE2-TT'):
        raise InputError('nguồn hoặc cửa sổ ngoài P7(a)')
    repo = pathlib.Path(repo).resolve()
    prefix = ('data', 'locked', 'rcaeval-re2tt-60') if ds == 'RE2-TT' else nezha.DATA_PREFIX
    base = (repo / pathlib.Path(*prefix)).resolve()
    if not base.is_relative_to(repo):
        raise InputError('gốc nguồn thoát repo')
    selected = {}
    for name, meta in case['files'].items():
        rel = meta['path']
        parts = rel.split('/')
        if ('\\' in rel or ':' in rel or any(p in ('', '.', '..') for p in parts)
                or tuple(parts[:len(prefix)]) != prefix):
            raise InputError('locator ngoài gốc nguồn đã khai')
        if ds == 'Nezha-OB':
            if name != rel:
                raise InputError('khóa locator OB không khớp')
            nezha._relative_path(rel)
        elif name != parts[-1] or name not in ('metrics.parquet', 'traces.parquet', 'logs.parquet'):
            raise InputError('nguồn TT ngoài hợp đồng parquet')
        full = (repo / pathlib.Path(*parts)).resolve()
        if not full.is_relative_to(base) or not re.fullmatch(r'[0-9a-f]{64}', meta['sha256']):
            raise InputError('đường dẫn hoặc hash nguồn không hợp lệ')
        selected[name] = dict(meta, absolute_path=str(full))
    if ds == 'RE2-TT':
        if (not {'metrics.parquet', 'traces.parquet'} <= set(selected)
                or len({pathlib.PurePosixPath(x['path']).parent for x in selected.values()}) != 1):
            raise InputError('tập file TT không thuộc một ca')
        if type(case['t']) is not int:
            raise InputError('mốc TT phải là giây nguyên')
        if view == 'ce' and case.get('ce_history') == 'insufficient':
            return None
        if view == 'ce' and case.get('ce_history') != 'verified':
            raise InputError('thiếu biên nhận hỗ trợ lịch sử C-e')
        result = {name: meta['absolute_path'] for name, meta in selected.items()}
    else:
        # Dùng lại hợp đồng bộ đọc, chỉ thay phép kiểm mã dev ở lớp bao ngoài.
        nezha._validate_case({'opaque_id': 'dev-0000000000', 't_ns': case['t_ns'],
                              'trace_guard_s': case['trace_guard_s'], 'files': case['files']})
        result = {'opaque_id': oid, 'view': 'main', 't_ns': case['t_ns'], 'trace_guard_s': case['trace_guard_s'],
                  'files': selected, 'universe': manifest['inventory'], 'aliases': dict(nezha.POD_ALIASES)}
    for meta in selected.values():
        source = pathlib.Path(meta['absolute_path'])
        if not source.is_file() or source.stat().st_size != meta['bytes'] or selector.sha256_file(source) != meta['sha256']:
            raise InputError('nguồn không khớp bản kê runtime đã ghim')
    return result


def static_params(protocol, dataset):
    ref = protocol['snapshots'][dataset]
    graph = checked_document(ROOT / ref['path'], ref['sha256'])
    return {'revision': ref['path'], 'canh': [[e['source'], e['target']] for e in graph['edges']]}


def m1(runtime, oid, arm, config, *, view='main'):
    protocol, manifest = runtime.protocol, runtime.manifest
    approved = protocol['configurations'].get(arm)
    if not approved or fingerprint(config) != approved['sha256']:
        raise InputError('cấu hình khác dấu vân tay của vế')
    if view == 'ce' and arm != 'M1':
        raise InputError('C-e P7 chỉ khai cho M1')
    selected = source_selection(manifest, oid, view=view)
    if selected is None:
        return {'status': 'INSUFFICIENT_EVIDENCE', 'blocks': [], 'reason': 'C_E_HISTORY_NOT_SUPPORTED'}
    inputs = manifest
    if view == 'ce':
        case = dict(manifest['cases'][oid])
        case['t'] -= 300
        inputs = dict(manifest, cases={oid: case})
    with patch('p7_entry.select', return_value=selected):
        case, t = load(inputs, oid, ROOT, granted=True)
    params = runner._params(config, case)
    params['tach_cd3'] = True
    if arm == 'T12-on':
        params['canh_tinh'] = static_params(protocol, manifest['dataset'])
    chuoi._kiem_params(params)
    args = (case['spans'], case['metrics'], case['logs'], case['inventory'], case['aliases'], t, params)
    no_labels(args)
    if hop_dong.vi_pham_gia_tri(params, case['aliases'], case['inventory'], case['chuoi_cam']):
        raise InputError('định danh riêng lọt vào tham số')
    return chuoi.chay(*args)


def _process(directory, env, job, deadline, *, script=None):
    directory.mkdir()
    job_path, result_path = directory / 'job.json', directory / 'ket-qua.json'
    save(job_path, job)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return None, {'timed_out': True, 'wall_s': 0, 'peak_rss_mb': 0, 'read_bytes': 0,
                      'write_bytes': 0, 'exit_code': None}
    args = [str(script)] if script else ['-m', 'p3.worker']
    cost = p3runner.chay_tien_trinh(env, args + [str(job_path), str(result_path)], remaining, 0, directory)
    save(directory / 'cost.json', cost)
    if cost['timed_out']:
        return None, cost
    if cost['exit_code'] or not result_path.is_file():
        raise InputError('worker lỗi, xem biên nhận riêng; dừng trước chấm')
    return result_path, cost


def run_baseline(dataset, selection, source_meta, oid, method, out_dir, timeout_s, *, t=None, seed=None):
    """Dùng chung tuyến sau selector cho P7 và pilot dev đã được cấp quyền."""
    if dataset not in ('RE2-TT', 'Nezha-OB') or method not in METHODS or not 0 < timeout_s <= 3600:
        raise InputError('lượt baseline ngoài phạm vi khai báo')
    if method == 'torai_B' and dataset == 'RE2-TT' and seed is None:
        raise InputError('thiếu seed TORAI đã khai')
    out = pathlib.Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=False)
    deadline = time.monotonic() + timeout_s
    if dataset == 'Nezha-OB':
        job = {'method': method, 'selection': {k: v for k, v in selection.items() if k != 'opaque_id'}}
        path, cost = _process(out / 'worker', 'main', job, deadline,
                              script=ROOT / 'results/T-052/scripts/p7_ob_worker.py')
        result = read(path) if path else {}
        raw = result['ket_qua_nhieu'][0] if path else {'status': 'TIMEOUT', 'items': []}
        name = 'torai' if method == 'torai_B' else method
        record = ban_ghi.tao(name, OB_VERSIONS[method], OB_VARIANTS[method], 'a', raw,
                             result.get('window'), 'p7-a', p3runner.WHY[name], hashseed=0,
                             run_id=out.name, opaque_id=oid)
        record['cost'] = cost
        record['input_sha256'] = result.get('input_sha256', {})
        save(out / 'ban-ghi-0.json', record)
        return [record]
    files = {name: {'path': path, 'sha256': source_meta[name]['sha256']} for name, path in selection.items()}
    base = {'config_id': 'p7-a', 'opaque_id': oid, 'run_id': out.name, 'seed': seed,
            'hashseed': 0, 'detector': None, 'detector_columns': None}
    if method == 'torai_B':
        work = out / 'bang'
        path, prep_cost = _process(out / 'chuan-bi', 'drain', {'kind': 'torai_prep', 'method': method,
            'files': files, 't': t, 'work_dir': str(work)}, deadline)
        if path is None:
            return p3runner._ket_thuc(out, None, [prep_cost], base, method, 'a')
        prep = read(path)
        result, cost = _process(out / 'torai', 'py38', {'kind': 'torai_run', 'work_dir': str(work),
                                                       't': t, 'seed': seed}, deadline)
        return p3runner._ket_thuc(out, result, [prep_cost, cost], base, method, 'a', prep=prep)
    result, cost = _process(out / 'worker', 'main', {'kind': 'ranker', 'method': method, 'files': files,
                                                    't': t, 'model': 'ols' if method == 'circa' else None}, deadline)
    return p3runner._ket_thuc(out, result, [cost], base, method, 'a', model='ols' if method == 'circa' else None)


def baseline(runtime, oid, method, out_dir, timeout_s, *, seed=None):
    manifest = runtime.manifest
    started = time.monotonic()
    selection = source_selection(manifest, oid)
    case = manifest['cases'][oid]
    return run_baseline(manifest['dataset'], selection, case['files'], oid, method, out_dir,
                        timeout_s - (time.monotonic() - started), t=case.get('t'), seed=seed)

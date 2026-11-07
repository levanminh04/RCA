"""Điểm vào P7 local: quyền → thành viên/hash → đọc/cắt → API phi nhãn → seal.

Chưa materialize metadata test thật. Mỗi tiến trình xử lý một ca; không dùng patch selector giữa các thread.
"""
import copy
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from unittest.mock import patch

from common import ROOT, dump, digest, save, read
from m1 import adapter, chuoi, hop_dong, runner
from p3 import cua_so, nezha, worker

METHODS = ('baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai_B')
LABEL_KEYS = {'root', 'fault', 'cell', 'labels', 'ground_truth', 'fault_type', 'nhan'}


class InputError(ValueError):
    """Lỗi quyền/metadata/dữ liệu; dừng trước bảng khoa học."""


def no_labels(value):
    if isinstance(value, dict):
        if set(value) & LABEL_KEYS:
            raise InputError('metadata phương pháp có trường nhãn')
        for v in value.values(): no_labels(v)
    elif isinstance(value, (list, tuple)):
        for v in value: no_labels(v)


def select(manifest, oid, root, *, granted=False, fixture=False):
    if not granted:
        raise PermissionError('Chưa có quyền mở dữ liệu P7')
    base = pathlib.Path(root).resolve()
    allowed = (ROOT / ('results/T-052/fixtures-p7-001' if fixture else 'data/locked')).resolve()
    if not base.is_relative_to(allowed):
        raise InputError('kho dữ liệu ngoài phạm vi đã giao')
    no_labels(manifest)
    if not re.fullmatch(r'(test|fixture)-[0-9a-f]{10}', str(oid)) or oid not in manifest['cases']:
        raise InputError('ca ngoài danh sách đã khóa')
    case = manifest['cases'][oid]
    if case['member_sha256'] not in manifest['members_locked']:
        raise InputError('thành viên không khớp cohort G1 đã khóa')
    paths = {}
    # Kiểm tất cả đường dẫn trước stat/hash/read; không in locator trong lỗi.
    for name, meta in case['files'].items():
        rel = meta['path']
        if not isinstance(rel, str) or '\\' in rel or re.match(r'^[A-Za-z]:', rel):
            raise InputError('locator không hợp lệ')
        posix = pathlib.PurePosixPath(rel)
        if posix.is_absolute() or any(x in ('.', '..', '') for x in rel.split('/')):
            raise InputError('locator thoát phạm vi')
        full = (base / pathlib.Path(*posix.parts)).resolve()
        if not full.is_relative_to(base): raise InputError('locator thoát phạm vi sau resolve')
        paths[name] = full
    for name, p in paths.items():
        meta = case['files'][name]
        if not p.is_file() or p.stat().st_size != meta['bytes'] or digest(p) != meta['sha256']:
            raise InputError('nguồn không khớp manifest đã materialize')
    if manifest['dataset'] == 'Nezha-OB':
        for name in paths: nezha._relative_path(name)  # Giữ hợp đồng nguồn Q-85, không tự mở ngày/schema khác.
        guard = case['trace_guard_s']
        days = {pathlib.PurePosixPath(n).parts[-3] for n in paths}
        if len(days) != 1 or guard != {'2022-08-22': 41, '2022-08-23': 32}[next(iter(days))]:
            raise InputError('nguồn/trace guard chưa được khóa')
        return {'opaque_id': oid, 'view': 'main', 't_ns': case['t_ns'], 'trace_guard_s': guard,
                'files': {n: dict(case['files'][n], absolute_path=str(p)) for n, p in paths.items()},
                'universe': manifest['inventory'], 'aliases': dict(nezha.POD_ALIASES)}
    if manifest['dataset'] != 'RE2-TT': raise InputError('adapter dataset chưa được khóa')
    if not {'metrics.parquet', 'traces.parquet'} <= set(paths): raise InputError('thiếu nguồn bắt buộc')
    return {k: str(v) for k, v in paths.items()}


def load(manifest, oid, root, *, granted=False, fixture=False, kind='M1'):
    selected = select(manifest, oid, root, granted=granted, fixture=fixture)
    case = manifest['cases'][oid]
    contract = read('results/T-043/hop-dong.json')
    try:
        if manifest['dataset'] == 'RE2-TT':
            t = case['t']
            if kind == 'M1':
                # Chỉ thay bộ chọn; đọc/cắt/chuẩn hóa của adapter hiện hành giữ nguyên.
                with patch('m1.adapter.selector.chon_ca', return_value=selected):
                    data = adapter.ca_re2tt({oid: case}, oid, t, root, contract, manifest['inventory'])
            else:
                raw = {k: worker._doc_parquet(selected, k + '.parquet') for k in ('metrics', 'traces', 'logs')}
                data, _ = cua_so.cat_ca(raw['metrics'], raw['traces'], raw['logs'], t)
        else:
            t = case['t_ns'] // nezha.NS
            if kind == 'M1':
                with patch('m1.adapter.nezha.chon_ca', return_value=selected):
                    data = adapter.ca_nezha({}, oid, root, contract, inventory=manifest['inventory'])
            else:
                data = nezha.doc_cua_so(selected)
    except Exception as exc:
        raise InputError('đọc/cắt nguồn thất bại: ' + type(exc).__name__) from None
    return data, t


def m1(manifest, oid, root, config, *, granted=False, fixture=False):
    case, t = load(manifest, oid, root, granted=granted, fixture=fixture)
    params = runner._params(config, case)
    params['tach_cd3'] = True
    chuoi._kiem_params(params)  # Lỗi runner không trở thành điểm 0.
    forbidden = [oid, *(m['path'] for m in manifest['cases'][oid]['files'].values())]
    if hop_dong.vi_pham_gia_tri(params, case['aliases'], case['inventory'], forbidden):
        raise InputError('định danh riêng lọt vào cấu hình phương pháp')
    args = (case['spans'], case['metrics'], case['logs'], case['inventory'], case['aliases'], t, params)
    no_labels(args)
    return chuoi.chay(*args)


def baseline(manifest, oid, root, method, *, granted=False, fixture=False, seed=0, torai_executor=None, spies=None,
             out_dir=None, timeout_s=180):
    if method not in METHODS: raise InputError('baseline ngoài ma trận đã khóa')
    payload, t = load(manifest, oid, root, granted=granted, fixture=fixture, kind='baseline')
    if spies:
        return spies[method](payload, t)  # Fixture kiểm luồng; không gọi đây là kiểm khoa học baseline.
    if manifest['dataset'] == 'Nezha-OB':
        from p3.adapters.nezha import chay
        return chay(method, payload, trace_guard_s=0)
    from p3.adapters import baro, simplerca, microrank, tracerca, circa, torai
    if method == 'baro': return baro.chay(payload['metric'], t)
    if method == 'simplerca': return simplerca.chay(payload['metric'], payload['traces'], payload['logs'], t)
    if method == 'microrank': return microrank.chay(payload['traces'], t)
    if method == 'tracerca': return tracerca.chay(payload['traces'], t)
    if method == 'circa': return circa.chay(payload['metric'], payload['traces'], t, 'ols')
    begin=time.perf_counter()
    prepared = torai.chuan_bi_B(payload['metric'], payload['traces'], payload['logs'], t)
    if torai_executor is None:
        return torai_local(prepared[:4],t,seed,out_dir,timeout_s-(time.perf_counter()-begin))
    return torai_executor(prepared[:4], t, seed)


def torai_local(tables,t,seed,out_dir,timeout_s):
    """Cùng tuyến CSV %.17g và Python 3.8 với p3.runner; thư mục do SPEC P7 giao."""
    started=time.perf_counter()
    if out_dir is None: raise InputError('cần thư mục kết quả TORAI đã được giao')
    folder=pathlib.Path(out_dir).resolve()
    folder.mkdir(parents=True,exist_ok=False)
    for name,df in zip(('metric','logts','tracets_err','tracets_lat'),tables):
        df.to_csv(folder/(name+'.csv'),index=False,float_format='%.17g')
    save(folder/'job.json',{'t':t,'seed':seed})
    timeout_s-=time.perf_counter()-started
    if timeout_s<=0:return {'status':'TIMEOUT','items':[],'error':'vượt thời gian đã khai'}
    env=dict(os.environ,PYTHONPATH=os.pathsep.join(['D:/RCA-ext/src/RCAEval',str(ROOT/'src')]),PYTHONHASHSEED='0')
    with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
        try:
            proc=subprocess.run(['D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe','-B',
                str(ROOT/'results/T-052/scripts/torai_p7_worker.py'),str(folder)],
                stdout=out,stderr=err,env=env,timeout=timeout_s,cwd=ROOT)
        except subprocess.TimeoutExpired:
            return {'status':'TIMEOUT','items':[],'error':'vượt thời gian đã khai'}
    if proc.returncode!=0 or not (folder/'result.json').exists():
        raise InputError('executor TORAI lỗi; dừng trước bảng khoa học')
    return read(folder/'result.json')


def seal(output, records):
    for record in records: no_labels(record)
    save(output, records)
    return digest(output)


def join_labels(output, expected_sha256, label_reader):
    # label_reader không được gọi trước kiểm seal thành công.
    if digest(output) != expected_sha256: raise InputError('bản ghi thay đổi sau seal')
    records = read(output)
    labels = label_reader()
    return records, labels


def cd3_after_seal(output, expected_sha256, destination, *, dataset, timeout_s=15, record_index=0):
    if dataset != 'RE2-TT': raise InputError('C-d3 mới không được khai cho dataset này')
    if not 0 < timeout_s <= 3600: raise InputError('thiếu giới hạn thời gian C-d3 hợp lệ')
    if digest(output) != expected_sha256: raise InputError('hạng chính chưa khớp seal')
    rec = read(output)[record_index]
    payload = {'canh': rec['extra']['canh'], **rec['extra']['dau_vao_cd3']}
    inp = pathlib.Path(destination).with_suffix('.input.json')
    save(inp, payload)
    try:
        result = subprocess.run([sys.executable, '-B', '-S', str(ROOT/'results/T-052/scripts/cd3_worker.py'), str(inp)],
            capture_output=True, text=True, encoding='utf-8', timeout=timeout_s, cwd=ROOT)
        value = json.loads(result.stdout) if result.returncode == 0 else {
            'trang_thai': 'ERROR', 'blocks': [], 'returncode': result.returncode, 'error_type': 'CD3_WORKER_ERROR'}
    except subprocess.TimeoutExpired:
        value = {'trang_thai': 'TIMEOUT', 'blocks': [], 'timeout_seconds': timeout_s}
    except (json.JSONDecodeError,OSError) as exc:
        value = {'trang_thai':'ERROR','blocks':[],'error_type':type(exc).__name__}
    assert digest(output) == expected_sha256  # Không được đổi bản ghi/hạng chính sau lỗi C-d3.
    value['main_seal_sha256'] = expected_sha256
    value['so_span_goc_A'] = payload['so_span_goc_A']
    save(destination, value)
    return value

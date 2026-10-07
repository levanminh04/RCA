"""Runner P3 (§3, §4, §13): chọn ca, dựng job, chạy worker ở tiến trình con, đo chi phí, ghi bản ghi.

Chỉ runner đọc allowlist và mốc tiêm (chế độ a). Chế độ (b) không đọc mốc: t̂ lấy từ bản ghi bộ phát hiện.
Giới hạn mỗi lượt (`timeout_s`) do SPEC của task chạy khai trước (§8.3, N3); vượt → TIMEOUT.
Lỗi runner (hash sai, worker thoát lỗi không ghi kết quả) không thành bản ghi chấm được.
"""
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

from . import ban_ghi, selector

ROOT = Path(__file__).resolve().parents[2]
ENVS = {
    'main': 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe',
    'py38': 'D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe',
    'drain': 'D:/RCA-ext/envs/T-016-cong-cu/Scripts/python.exe',
}
PYTHONPATH = {
    'main': ['D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro', str(ROOT / 'src'), 'D:/RCA-ext/work/T-014/CIRCA'],
    'py38': ['D:/RCA-ext/src/RCAEval', str(ROOT / 'src')],
    'drain': [str(ROOT / 'src')],
}
TORAI_TT = Path('D:/RCA-ext/work/T-016/data/torai-TT')
WHY = {'baro': ['WHY-22', 'WHY-24', 'WHY-26', 'WHY-27', 'WHY-28'],
       'simplerca': ['WHY-17', 'WHY-22', 'WHY-26', 'WHY-28', 'WHY-33'],
       'microrank': ['WHY-22', 'WHY-26', 'WHY-28', 'WHY-31'],
       'tracerca': ['WHY-22', 'WHY-26', 'WHY-28', 'WHY-32'],
       'circa': ['WHY-22', 'WHY-26', 'WHY-27', 'WHY-28', 'WHY-30'],
       'torai': ['WHY-19', 'WHY-20', 'WHY-22', 'WHY-26', 'WHY-28', 'WHY-29'],
       'bocpd': ['WHY-25', 'WHY-34', 'WHY-35'], 'nsigma': ['WHY-34', 'WHY-35']}


class Timeout(Exception):
    pass


def chay_tien_trinh(env, args, timeout_s, hashseed=None, log_dir=None, poll=0.1):
    """Chạy một tiến trình con, đo wall, RSS đỉnh (cả cây), byte đọc/ghi; giết cả cây khi quá hạn."""
    import psutil
    e = dict(os.environ)
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    e['PYTHONPATH'] = os.pathsep.join(PYTHONPATH[env])
    e['PYTHONIOENCODING'] = 'utf-8'
    if hashseed is not None:
        e['PYTHONHASHSEED'] = str(hashseed)
    log_dir = Path(log_dir) if log_dir else None
    out = open(log_dir / 'stdout.txt', 'w', encoding='utf-8') if log_dir else subprocess.DEVNULL
    err = open(log_dir / 'stderr.txt', 'w', encoding='utf-8') if log_dir else subprocess.DEVNULL
    t0 = time.perf_counter()
    p = psutil.Popen([ENVS[env], '-B', '-W', 'ignore'] + list(args), env=e, cwd=str(ROOT), stdout=out, stderr=err)
    peak, rb, wb, timed_out = 0, 0, 0, False
    try:
        while True:
            try:
                procs = [p] + p.children(recursive=True)
                rss = 0
                for q in procs:
                    try:
                        rss += q.memory_info().rss
                        io = q.io_counters()
                        if q is p:
                            rb, wb = io.read_bytes, io.write_bytes
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                peak = max(peak, rss)
            except psutil.NoSuchProcess:
                pass
            if p.poll() is not None:
                break
            if time.perf_counter() - t0 > timeout_s:
                timed_out = True
                for q in p.children(recursive=True) + [p]:
                    try:
                        q.kill()
                    except psutil.NoSuchProcess:
                        pass
                p.wait()
                break
            time.sleep(poll)
    finally:
        if log_dir:
            out.close(); err.close()
    return {'wall_s': round(time.perf_counter() - t0, 3), 'peak_rss_mb': round(peak / 2**20, 1),
            'read_bytes': rb, 'write_bytes': wb, 'exit_code': p.returncode, 'timed_out': timed_out,
            'env': env, 'hashseed': hashseed}


def _job(run_dir, job):
    run_dir.mkdir(parents=True, exist_ok=True)
    jp, rp = run_dir / 'job.json', run_dir / 'ket-qua.json'
    jp.write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding='utf-8')
    return jp, rp


def _tac_gia_A(case_dir, torai_tt=TORAI_TT):
    """Thư mục torai-TT của ca: <service>_<lỗi>/<lần>. Runner suy từ case_dir; phương pháp không nhận."""
    name = Path(case_dir).name.replace('re2tt_', '')
    svc_fault, rep = name.rsplit('_', 1)
    d = Path(torai_tt) / svc_fault / rep
    return {k: str(d / (k + '.csv')) for k in ('logts', 'tracets_err', 'tracets_lat')}


def chay_luot(allowlist, opaque_id, method, mode, t, out_dir, timeout_s, repo_root=ROOT, seed=None,
              hashseed=0, model=None, detector=None, detector_columns=None, tap_cot='bocpd', config_id='p3-re2tt-v2', torai_tt=TORAI_TT):
    """Một lượt. method: baro|simplerca|microrank|tracerca|circa|torai_A|torai_B|bocpd|nsigma.
    Trả danh sách bản ghi (CIRCA cho hai bản ghi RHT+DA, RHT-only). TIMEOUT → bản ghi trạng thái TIMEOUT."""
    files = selector.chon_ca(allowlist, opaque_id, repo_root, kiem_hash=False)
    meta = {k: {'path': v, 'sha256': allowlist[opaque_id]['files'][k]['sha256']} for k, v in files.items()}
    run_id = f'{method}-{mode}-{opaque_id}-s{seed}-h{hashseed}-{uuid.uuid4().hex[:6]}'
    run_dir = Path(out_dir) / run_id
    base = dict(run_id=run_id, opaque_id=opaque_id, mode=mode, seed=seed, hashseed=hashseed,
                detector=detector, detector_columns=detector_columns, config_id=config_id)
    t_start = time.perf_counter()
    if method in ('bocpd', 'nsigma'):
        jp, rp = _job(run_dir, {'kind': 'detector', 'method': method, 'files': meta, 'tap_cot': tap_cot})
        cost = chay_tien_trinh('main', ['-m', 'p3.worker', str(jp), str(rp)], timeout_s, hashseed, run_dir)
        return _ket_thuc_detector(run_dir, rp, cost, base, method, tap_cot)
    if method in ('torai_A', 'torai_B'):
        work = run_dir / 'bang'
        job = {'kind': 'torai_prep', 'method': method, 'files': meta, 't': t, 'work_dir': str(work)}
        if method == 'torai_A':
            job['tac_gia'] = _tac_gia_A(allowlist[opaque_id]['case_dir'], torai_tt)
        jp, rp = _job(run_dir / 'chuan-bi', job)
        cost1 = chay_tien_trinh('main' if method == 'torai_A' else 'drain', ['-m', 'p3.worker', str(jp), str(rp)],
                                timeout_s, hashseed, run_dir / 'chuan-bi')
        con_lai = timeout_s - cost1['wall_s']
        if con_lai <= 0:
            cost1 = dict(cost1, timed_out=True)
        if cost1['timed_out'] or cost1['exit_code'] != 0 or not rp.exists():
            return _ket_thuc(run_dir, None, [cost1], base, method, mode)
        prep = json.loads(rp.read_text(encoding='utf-8'))
        jp2, rp2 = _job(run_dir / 'torai', {'kind': 'torai_run', 'work_dir': str(work), 't': t, 'seed': seed})
        cost2 = chay_tien_trinh('py38', ['-m', 'p3.worker', str(jp2), str(rp2)], con_lai, hashseed, run_dir / 'torai')
        return _ket_thuc(run_dir, rp2, [cost1, cost2], base, method, mode, prep=prep)
    jp, rp = _job(run_dir, {'kind': 'ranker', 'method': method, 'files': meta, 't': t, 'model': model})
    cost = chay_tien_trinh('main', ['-m', 'p3.worker', str(jp), str(rp)], timeout_s, hashseed, run_dir)
    return _ket_thuc(run_dir, rp, [cost], base, method, mode, model=model)


def _gop_cost(costs):
    return {'wall_s': round(sum(c['wall_s'] for c in costs), 3),
            'peak_rss_mb': max(c['peak_rss_mb'] for c in costs),
            'read_bytes': sum(c['read_bytes'] for c in costs), 'write_bytes': sum(c['write_bytes'] for c in costs),
            'exit_code': costs[-1]['exit_code'], 'tien_trinh': costs}


def _ghi(run_dir, recs):
    for i, r in enumerate(recs):
        (Path(run_dir) / f'ban-ghi-{i}.json').write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding='utf-8')
    return recs


def _ket_thuc(run_dir, rp, costs, base, method, mode, prep=None, model=None):
    cost = _gop_cost(costs)
    ten = 'torai' if method.startswith('torai') else method
    version = {'baro': 'RCAEval 259ea41 e2e/baro.py', 'simplerca': 'src/simplerca (T-017, M4)',
               'microrank': 'src/microrank (MicroRank-RCAEval sửa đầu vào)',
               'tracerca': 'RCAEval 259ea41 e2e/tracerca.py + lọc ji hữu hạn',
               'circa': 'src/circa_kien_truc + RCAEval 259ea41 RHT/DA; CIRCA 0215e18',
               'torai': 'src/torai/torai_sua.py (RCAEval 259ea41 sửa A, B)'}[ten]
    if any(c['timed_out'] for c in costs):
        if ten == 'circa':
            variants = [f'{model}+rht_da', f'{model}+rht']
        else:
            variants = ['full' if ten == 'microrank' else method.split('_')[-1] if ten == 'torai' else 'native']
        recs = []
        for v in variants:
            r = ban_ghi.tao(ten, version, v, mode, {'status': 'TIMEOUT', 'error': 'vượt giới hạn mỗi lượt'}, None,
                            base['config_id'], WHY.get(ten, []),
                            **{k: base[k] for k in ('seed', 'hashseed', 'detector', 'detector_columns',
                                                    'run_id', 'opaque_id')})
            r['cost'] = cost
            recs.append(r)
        return _ghi(run_dir, recs)
    if rp is None or not Path(rp).exists() or cost['exit_code'] != 0:
        loi = {'run_id': base['run_id'], 'opaque_id': base['opaque_id'], 'loi_runner': True,
               'cost': cost, 'goi_y': 'xem stderr.txt trong thư mục lượt'}
        (Path(run_dir) / 'loi-runner.json').write_text(json.dumps(loi, ensure_ascii=False, indent=1), encoding='utf-8')
        raise selector.LoiRunner(f'worker lỗi: {base["run_id"]}')
    res = json.loads(Path(rp).read_text(encoding='utf-8'))
    window = res.get('window') or (prep or {}).get('window')
    ket_qua = res.get('ket_qua_nhieu') or [res['ket_qua']]
    recs = []
    for kq in ket_qua:
        variant = kq.get('variant') or (method.split('_')[-1] if ten == 'torai' else 'full' if ten == 'microrank' else 'native')
        r = ban_ghi.tao(ten, version, variant, mode, kq, window, base['config_id'], WHY.get(ten, []),
                        **{k: base[k] for k in ('seed', 'hashseed', 'detector', 'detector_columns', 'run_id', 'opaque_id')})
        r['cost'] = cost
        r['cost']['buoc_s'] = res.get('buoc_s') if prep is None else {'chuan_bi': prep.get('buoc_s'), 'torai': res.get('buoc_s')}
        r['input_sha256'] = res.get('input_sha256') or (prep or {}).get('input_sha256') or {}
        r['input_shape']['metric_columns'] = (res.get('read_columns') or (prep or {}).get('read_columns') or {}).get('metrics')
        if prep is not None:
            r['extra']['chuan_bi'] = prep.get('chuan_bi')
        recs.append(r)
    return _ghi(run_dir, recs)


def _ket_thuc_detector(run_dir, rp, cost, base, method, tap_cot):
    if cost['timed_out']:
        r = {'run_id': base['run_id'], 'opaque_id': base['opaque_id'], 'method': method, 'tap_cot': tap_cot,
             'status': 'TIMEOUT', 'alarms': [], 'cost': cost}
        return _ghi(run_dir, [r])
    if not Path(rp).exists() or cost['exit_code'] != 0:
        (Path(run_dir) / 'loi-runner.json').write_text(json.dumps({'cost': cost}, indent=1), encoding='utf-8')
        raise selector.LoiRunner(f'worker lỗi: {base["run_id"]}')
    res = json.loads(Path(rp).read_text(encoding='utf-8'))
    kq = res['ket_qua']
    from .adapters.phat_hien import luot_rca
    r = {'run_id': base['run_id'], 'opaque_id': base['opaque_id'], 'method': method, 'mode': 'b',
         'tap_cot': tap_cot, 'why_ids': WHY[method], 'status': kq['status'], 'error': kq.get('error'),
         'alarms': kq.get('alarms', []), 'bat_dau_danh_gia': kq.get('bat_dau_danh_gia'),
         'detector_columns': kq.get('detector_columns'), 'input_shape': kq.get('input_shape'),
         'diagnostics': kq.get('diagnostics', {}), 'luot_rca': luot_rca(kq.get('alarms', [])),
         'times': res['times'], 'input_sha256': res.get('input_sha256'),
         'cost': dict(cost, buoc_s=res.get('buoc_s'))}
    return _ghi(run_dir, [r])

"""Điểm nối T-047; cấu hình/phương pháp không đọc nhãn chấm.

Ghi chỉ results/T-047. Lỗi được lưu trước khi dừng; thư mục lượt không ghi đè.
Pha 2/độ bền gọi một helper; không monkeypatch src.
"""
import copy
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

import numpy as np

from m1 import chuoi, cong, e4, hop_dong, runner, xep_hang
from m1_danh_gia import pha2, rr
import luat_c_t047 as lc

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-047'
MODE = {'cong_phan_vi': 'G3', 'cong_dem': 'D1', 'thang': 'E4+T4c'}


def duong_ra(path):
    p = Path(path).resolve()
    if not p.is_relative_to(OUT.resolve()):
        raise ValueError('đường ghi ngoài T-047')
    return p


def ghi(path, value):
    p = duong_ra(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(pha2.ma_hoa_json(value), ensure_ascii=False, sort_keys=True, indent=1,
                            allow_nan=False) + '\n', encoding='utf-8')


def cau_hinh(mt, nhom):
    if nhom not in ('K', 'T1'):
        raise ValueError('T-047 chỉ chạy K hoặc T1')
    ds = runner.sinh_cau_hinh(runner.ap_dinh_chinh(copy.deepcopy(mt)), {}, dict(runner.R0))[nhom]
    for c in ds:
        c['che_do'] = dict(MODE)
        c['ma_noi_dung_T047'] = hashlib.sha256(runner._json(c).encode()).hexdigest()
    return ds


def kiem_ban_ghi(rec):
    status = rec.get('status')
    if status not in ('OK', 'NO_EVIDENCE'):
        raise ValueError(f'dừng theo trạng thái {status!r}')
    if rec.get('method_version') != chuoi.PHIEN_BAN_CHE_DO or (rec.get('extra') or {}).get('che_do') != MODE:
        raise ValueError('bản ghi không ở chế độ mới')
    hop_dong.kiem_ban_ghi(rec)


def pha1(cases, moc, configs, path):
    """Cùng giao diện runner, kiểm lỗi ngay sau mỗi bản ghi và trước công việc tiếp."""
    path = duong_ra(path)
    path.mkdir(parents=True, exist_ok=False)
    ghi(path / 'tham-so.json', {'configs': configs, 'che_do': MODE,
                              'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
                              'code_revision': 'c298188e', 'code_correction': 'Q-233/C1',
                              'source_sha256': {name: hashlib.sha256(Path(mod.__file__).read_bytes()).hexdigest()
                                  for name,mod in [('src/m1/cong.py',cong),('src/m1/chuoi.py',chuoi),
                                                   ('src/m1/runner.py',runner),('src/m1/e4.py',e4)]},
                              'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED')})
    cam = sorted({c['opaque_id'] for c in cases} | {c['case_dir'] for c in cases if c.get('case_dir')}
                 | {x for c in cases for x in c.get('chuoi_cam', []) if x})
    if not cases or not configs or len({c['opaque_id'] for c in cases}) != len(cases) or len({c['config_id'] for c in configs}) != len(configs):
        raise ValueError('tập ca/cấu hình rỗng hoặc trùng')
    records, start = [], time.monotonic()
    with (path / 'progress.jsonl').open('x', encoding='utf-8') as progress:
        def event(x):
            progress.write(json.dumps(dict(x, elapsed=time.monotonic() - start), ensure_ascii=False) + '\n')
            progress.flush()
        event({'event': 'start', 'cases': len(cases), 'configs': len(configs)})
        for c in sorted(cases, key=lambda x: x['opaque_id']):
            chuoi.CACHE = e4.CacheCong()
            for config in sorted(configs, key=lambda x: x['config_id']):
                p = runner._params(config, c)
                if p.get('che_do') != MODE or hop_dong.vi_pham_gia_tri(p, c.get('aliases') or {}, c.get('inventory') or [], cam):
                    raise ValueError('chế độ sai hoặc chuỗi cấm trong đầu vào')
                event({'event': 'start_record', 'case': c['opaque_id'], 'config': config['config_id']})
                rec = chuoi.chay(c['spans'], c.get('metrics') or [], c.get('logs') or [], c.get('inventory') or [],
                                c.get('aliases') or {}, moc[c['opaque_id']], p)
                rec = dict(rec, opaque_id=c['opaque_id'])
                # Lưu ngay cả ERROR/UNSUPPORTED trước khi validation dừng vòng lặp.
                ghi(path / 'records' / f'{len(records):05d}.json', rec)
                records.append(rec)
                event({'event': 'record', 'case': c['opaque_id'], 'config': config['config_id'], 'status': rec.get('status')})
                kiem_ban_ghi(rec)
        records.sort(key=lambda r: (r['config_id'], r['opaque_id']))
        data = ('\n'.join(runner._json(r) for r in records) + '\n').encode()
        (path / 'ban-ghi.jsonl').write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        meta = {'tep': 'ban-ghi.jsonl', 'sha256': digest, 'so_ban_ghi': len(records), 'so_ca': len(cases),
                'cau_hinh': sorted(c['config_id'] for c in configs), 'phien_ban': chuoi.PHIEN_BAN_CHE_DO, 'che_do': MODE}
        ghi(path / 'pha1.json', meta)
        event({'event': 'done', 'sha256': digest})
    return meta


def ghi_hash_log(paths, log_path=None):
    """Kiểm pha 1 rồi nối LOG trước khi caller được đọc nhãn chấm."""
    expected = ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md'
    log = Path(log_path) if log_path else expected
    if log.resolve() != expected.resolve():
        raise ValueError('chỉ ghi LOG T-047')
    rows = []
    for path in paths:
        p = duong_ra(path)
        meta = json.loads((p / 'pha1.json').read_text(encoding='utf-8'))
        _, recs = pha2.doc(p, meta['sha256'])
        for rec in recs:
            kiem_ban_ghi(rec)
        rows.append((p.relative_to(ROOT).as_posix(), meta['sha256']))
    b = log.read_bytes()
    nl = '\r\n' if b'\r\n' in b else '\n'
    from datetime import datetime
    s = '\n### Hash pha 1 trước đọc nhãn — ' + datetime.now().astimezone().isoformat(timespec='seconds') + '\n\n'
    s += '\n'.join(f'- `{path}`: `{h}`' for path, h in rows) + '\n'
    log.write_bytes(b + s.replace('\n', nl).encode())
    return dict(rows)


def kiem_hash_trong_log(path, log_text):
    path = duong_ra(path)
    meta = json.loads((path / 'pha1.json').read_text(encoding='utf-8'))
    line = f"- `{path.relative_to(ROOT).as_posix()}`: `{meta['sha256']}`"
    if line not in log_text:
        raise ValueError('hash pha 1 chưa được ghi LOG')
    _, recs = pha2.doc(path, meta['sha256'])
    for r in recs:
        kiem_ban_ghi(r)
    return meta, recs


def pha2_khoi(kq, ce, E_X, trong_so=None, h=lc.H):
    return lc.danh_gia_khoi(kq, ce, E_X, trong_so, h)


def mau_do_ben(kq, ce, E_X, trong_so):
    return pha2_khoi(kq, ce, E_X, trong_so, lc.H)


def do_ben(kq, ce, E_X, seed, n=1000):
    ca = next(iter(kq['cau_hinh'].values()))['ca']
    ds = [{'ma': o, 'dataset': x['dataset'], 'o': x['o']} for o, x in sorted(ca.items())]
    rng = np.random.default_rng(seed)
    original = mau_do_ben(kq, ce, E_X, {x['ma']: 1 for x in ds})
    rows = []
    for i in range(n):
        weights = rr.lay_mau_o(ds, rng)
        r = mau_do_ben(kq, ce, E_X, weights)
        # Giữ mọi mẫu, gồm không chọn được và C-e chưa kiểm; không âm thầm bỏ mẫu.
        rows.append({'i': i, 'trong_so': weights, 'chon_khoi': r['chon_khoi'], 'buoc8': r['buoc8']})
    return {'seed': seed, 'n': n, 'mau_goc': original, 'mau': rows}


def do_nhay(kq, ce, E_X):
    return {str(h): pha2_khoi(kq, ce, E_X, h=h) for h in (lc.H, lc.Fraction(1, 2), lc.Fraction(2))}


def phuc_dung_S0(blocks):
    items = []
    for b in blocks:
        k = b['key']
        if len(k) != 5 or len(b['groups']) != 1:
            raise ValueError('không phải khối S1 E6a')
        for e in b['groups'][0]:
            items.append((e, tuple(k[:2] + k[3:])))
    if len({e for e, _ in items}) != len(items):
        raise ValueError('thực thể trùng')
    return xep_hang._nhom(xep_hang.sap_khoa(items))

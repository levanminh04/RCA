"""Phép tất định cấp bản ghi (SPEC T-044 bước 6, tiêu chí 5).

Chạy chuỗi M1 trên bộ ca giả (trace S1–S7 của fixture 1, ca metric MET1) với nhiều cấu hình; mỗi bản ghi được băm
sha256 trên JSON chuẩn hóa. Thứ tự 0 là thứ tự gốc; thứ tự 1–3 xáo mọi danh sách đầu vào ở mọi tầng gọi như
`tests/conftest.py#XAO`, với cache cổng mới cho từng lượt. In bảng {thứ tự: {mã: sha256}} ra stdout dạng JSON.
Chạy dưới PYTHONHASHSEED 0, 1, 2 rồi so: mọi sha256 phải giống hệt. Đầu ra ghi kèm 'hash_seed' (biến môi trường
PYTHONHASHSEED lúc chạy) để bộ tổng hợp kiểm seed thật (C7).

    PYTHONHASHSEED=0 python -B results/T-044/scripts/tat_dinh.py > ban-ghi-h0.json
"""
import functools
import hashlib
import importlib
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'results' / 'T-044' / 'tests'))

import conftest  # noqa: E402
import sinh_trace_S  # noqa: E402
from m1 import chuoi, e4  # noqa: E402

U = ['A', 'B', 'F', 'I', 'R', 'X']
CAU_HINH = {
    'C0': {}, 'C1': {'E1': 'U'}, 'C2': {'E1': 'U', 'E2': 'C'}, 'C3': {'E1': 'U', 'E2': 'VC'},
    'C4': {'E1': 'U', 'E2': 'VC', 'E5': True}, 'C5': {'E1': 'U', 'E2': 'VC', 'E3b': True, 'E5': True},
    'CP': {'E1': 'CP', 'E2': 'VC', 'E5': True},
    'E3': {'E1': 'U', 'E2': 'C', 'E3': True, 'E5': True},
    'E6b': {'E1': 'U', 'E2': 'VC', 'E3': True, 'E3b': True, 'E5': True, 'E6': 'b'},
    'E9': {'E1': 'U', 'E2': 'VC', 'E3b': True, 'E5': True, 'E9': True},
    'T12': {'E1': 'U', 'E2': 'VC', 'E5': True, 'T12': True},
    'z': {'E1': 'U', 'E5': True},
    'ke_canh': {'E1': 'U', 'E2': 'VC', 'E5': True},
}


def _bang(seed):
    """Bọc các hàm theo conftest.XAO; seed 0 không bọc."""
    goc = []
    if not seed:
        return goc
    dem = {'n': 0}
    for mod, ham in conftest.XAO.items():
        m = importlib.import_module(mod)
        for h, vt in ham.items():
            f = getattr(m, h)
            ten = f'{mod}.{h}'

            def g(*args, _f=f, _ten=ten, _vt=vt, **kw):
                dem['n'] += 1
                rng = random.Random(f'{seed}|{_ten}|{dem["n"]}')
                args = list(args)
                for i in _vt:
                    if i < len(args) and isinstance(args[i], list) and not (_ten == 'm1.chuoi.chay' and i == 1):
                        x = list(args[i])
                        rng.shuffle(x)
                        args[i] = x
                for k in list(kw):
                    if k in conftest.TEN_KW and isinstance(kw[k], list):
                        x = list(kw[k])
                        rng.shuffle(x)
                        kw[k] = x
                if _ten == 'm1.chuoi.chay' and len(args) >= 7 and isinstance(args[1], list):
                    tg = (args[6] or {}).get('thoi_gian_nguon') or {}
                    if all(v == 'metrics.time' for v in tg.values()):
                        x = list(args[1])
                        rng.shuffle(x)
                        args[1] = x
                return _f(*args, **kw)
            goc.append((m, h, f))
            setattr(m, h, functools.wraps(f)(g))
    return goc


def _tra(goc):
    for m, h, f in goc:
        setattr(m, h, f)


def _ca():
    out = []
    for s in ('S1', 'S2', 'S2b', 'S3', 'S5', 'S6', 'S7'):
        spans, logs = sinh_trace_S.sinh(s, t=1000, mau=conftest.FIXTURE['trace_mau_S'])
        out.append((s, spans, [], logs, {}))
    spans, logs = sinh_trace_S.sinh('S5', t=1000, mau=conftest.FIXTURE['trace_mau_S'])
    metrics = [{'time': 700 + 10 * i, 'R_cpu': (10 + 0.1 * (i % 7)) if i < 30 else (float('nan') if i == 33 else 50.0),
                'A_latency-90': 5.0 + 0.01 * (i % 3) + (2.0 if i >= 30 else 0.0)} for i in range(60)]
    out.append(('MET', spans, metrics, logs, {'nguon_metric': {'R_cpu': 'm', 'A_latency-90': 'm'},
                                               'thoi_gian_nguon': {'m': 'metrics.time'}}))
    return out


HOP_DONG = json.loads((ROOT / 'results' / 'T-043' / 'hop-dong.json').read_text(encoding='utf-8'))


def _params(ten, ch, them):
    from m1 import adapter
    p = sinh_trace_S.params(ch)
    p['ho_so_nguon'] = adapter.ho_so_nguon(HOP_DONG, 'RE2-TT')  # đủ 8 hậu tố metric của hop-dong.json
    p.update(them)
    p['config_id'] = ten
    if ten == 'z':
        p['nhanh_z'] = True
    if ten == 'ke_canh':
        p['tham_so_E5'] = {'doc_nhom_vong': 'ke_canh'}
    if ch.get('T12'):
        p['canh_tinh'] = {'revision': 'gia', 'canh': [['I', 'R'], ['X', 'R']]}
    return p


def main():
    bang = {}
    for thu_tu in (0, 1, 2, 3):
        goc = _bang(thu_tu)
        try:
            h = {}
            for ma_ca, spans, metrics, logs, them in _ca():
                for ten, ch in CAU_HINH.items():
                    chuoi.CACHE = e4.CacheCong()
                    rec = chuoi.chay(spans, metrics, logs, U, {}, 1000, _params(ten, ch, them))
                    if rec.get('error'):
                        raise SystemExit(f'{ma_ca}/{ten}: {rec["error"]}')
                    s = json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
                    h[f'{ma_ca}|{ten}'] = hashlib.sha256(s.encode('utf-8')).hexdigest()
            bang[str(thu_tu)] = h
        finally:
            _tra(goc)
    bang['hash_seed'] = os.environ.get('PYTHONHASHSEED')
    print(json.dumps(bang, sort_keys=True, indent=1))


if __name__ == '__main__':
    main()

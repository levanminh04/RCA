"""T-025 kiểm đúng đắn: BOCPD trên tiền tố T điểm đầu của một ca, chạy trên laptop và EC2, so R và điểm đổi.

Tiền xử lý §7.2 trên cả bản ghi (`phat_hien.tien_xu_ly_bocpd`, giữ d của ca), lấy T dòng đầu, gọi
`online_changepoint_detection` như §7.2, rồi `phat_hien.diem_doi_tu_R`. Lưu R (.npy), maxes gốc, m, điểm đổi.
Không nhãn; chỉ là phép so hai máy, không dùng để chấm.

python bocpd_r_tien_to.py <oid> <T>            # chạy, ghi runs/bocpd-r-tien-to-<máy>-NNN/
python bocpd_r_tien_to.py so <dir_a> <dir_b>    # so hai lượt, ghi so-sanh.json vào dir_a
"""
import json
import sys
import time
from pathlib import Path

import chung


def chay(oid, T):
    import numpy as np
    import pandas as pd
    from functools import partial
    from baro._bocpd import MultivariateT, constant_hazard, online_changepoint_detection
    from p3.adapters import phat_hien
    al = chung.nap_allowlist()
    f = chung.selector.chon_ca(al, oid, chung.DATA_ROOT, kiem_hash=True, tep=['metrics.parquet'])
    L = chung.Luot('bocpd-r-tien-to-' + ('ec2' if chung.EC2 else 'laptop'), {'opaque_id': oid, 'T': T})
    m = pd.read_parquet(f['metrics.parquet'])
    cot = phat_hien.cot_bocpd(m.columns)
    data = phat_hien.tien_xu_ly_bocpd(m[cot])
    X = data.to_numpy()[:T]
    s = time.perf_counter()
    R, maxes = online_changepoint_detection(X, partial(constant_hazard, 50), MultivariateT(dims=X.shape[1]))
    wall = time.perf_counter() - s
    cps, mm = phat_hien.diem_doi_tu_R(R)
    np.save(L.dir / 'R.npy', R)
    np.save(L.dir / 'maxes.npy', maxes)
    out = {'opaque_id': oid, 'T': T, 'd': int(X.shape[1]), 'giay_goi_bocpd': round(wall, 3),
           'X_sha256': __import__('hashlib').sha256(X.tobytes()).hexdigest(),
           'cps': cps, 'm': None if cps is None else [int(x) for x in mm], 'numpy': np.__version__}
    chung.ghi_json(L.dir / 'ket-qua.json', out)
    L.xong({'d': out['d'], 'giay': out['giay_goi_bocpd'], 'so_diem_doi': None if cps is None else len(cps)})


def so(a, b):
    import numpy as np
    a, b = Path(a), Path(b)
    ka, kb = (json.loads((d / 'ket-qua.json').read_text(encoding='utf-8')) for d in (a, b))
    Ra, Rb = np.load(a / 'R.npy'), np.load(b / 'R.npy')
    ma, mb = np.load(a / 'maxes.npy'), np.load(b / 'maxes.npy')
    lech = np.abs(Ra - Rb)
    rel = lech / np.maximum(np.abs(Ra), np.finfo(float).tiny)
    out = {'a': a.name, 'b': b.name, 'X_giong': ka['X_sha256'] == kb['X_sha256'], 'd': [ka['d'], kb['d']],
           'R_giong_het': bool((Ra == Rb).all()), 'R_lech_tuyet_doi_max': float(lech.max()),
           'R_lech_tuong_doi_max_o_R_lon_hon_1e-12': float(rel[np.abs(Ra) > 1e-12].max()),
           'so_o_khac': int((Ra != Rb).sum()), 'so_o': int(Ra.size),
           'maxes_giong': bool((ma == mb).all()), 'm_giong': ka['m'] == kb['m'], 'cps_giong': ka['cps'] == kb['cps'],
           'so_diem_doi': [len(ka['cps'] or []), len(kb['cps'] or [])], 'giay': [ka['giay_goi_bocpd'], kb['giay_goi_bocpd']]}
    chung.ghi_json(a / 'so-sanh.json', out)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1] == 'so':
        so(sys.argv[2], sys.argv[3])
    else:
        chay(sys.argv[1], int(sys.argv[2]))

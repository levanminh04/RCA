"""T-029: N1–N6 và phần định vị không nhãn theo SPEC khóa; không đọc dữ liệu/nhãn."""
import numpy as np

P0 = 0.0027
HISTORY = ((100, 200), (200, 400), (400, 720))
N1_LEVELS = (1.5, 2.0, 3.0)
N2_LEVELS = (5, 10, 20)


def column_type(name):
    suffix = name.split('_', 1)[1] if '_' in name else ''
    if 'latency' in suffix:
        return 'latency'
    if 'error' in suffix:
        return 'error'
    if 'cpu' in suffix:
        return 'cpu'
    if 'mem' in suffix:
        return 'mem'
    if any(x in suffix for x in ('network', 'net_', 'rx', 'tx', 'receive', 'transmit')):
        return 'mang'
    return 'khac'


def features(Z, columns, std_at_first, universe):
    """Z là cờ BARO từng cột trên lưới 0..1440. Không nhận root, fault, tên ca hoặc đường dẫn."""
    Z = np.asarray(Z, dtype=bool)
    if Z.shape != (1441, len(columns)) or not len(columns):
        raise ValueError('Lưới Z phải là 1441 × d, d > 0')
    al = np.flatnonzero(Z.any(axis=1))
    first = int(al[0]) if len(al) else None
    after = al[al >= 720]
    p = Z[100:720].mean(axis=0)
    hist = {f'{a}:{b}': {'so_bao_cot_giay': int(Z[a:b].sum()),
                         'mau_so_cot_giay': (b-a)*len(columns),
                         'ti_le': float(Z[a:b].mean()),
                         'ti_le_tung_cot': Z[a:b].mean(axis=0).tolist()}
            for a, b in HISTORY}
    head, tail = hist['100:200']['ti_le'], hist['400:720']['ti_le']
    trig = np.flatnonzero(Z[first]) if first is not None else np.array([], dtype=int)
    dense = {str(k): (p > k*P0) for k in N2_LEVELS}
    n2 = {str(k): bool(dense[str(k)][trig].any()) for k in N2_LEVELS}
    sd = np.asarray(std_at_first, dtype=float)
    if sd.shape != (len(columns),):
        raise ValueError('std_at_first không cùng số cột')
    rows = []
    for j, c in enumerate(columns):
        rows.append({'column': c, 'service': c.split('_', 1)[0], 'type': column_type(c),
                     'p_j': float(p[j]), 'so_bao_Nv': int(Z[100:720, j].sum()),
                     'bao_tai_t_hat': bool(j in trig),
                     'std_zero_at_first': bool(sd[j] == 0),
                     'std_at_first': float(sd[j]) if np.isfinite(sd[j]) else None,
                     'N2_dense': {str(k): bool(dense[str(k)][j]) for k in N2_LEVELS}})
    n5 = {}
    for kind in ('latency', 'error', 'cpu', 'mem', 'mang', 'khac'):
        ix = [j for j, c in enumerate(columns) if column_type(c) == kind]
        n5[kind] = {'so_cot': len(ix), 'so_bao_cot_giay': int(Z[100:720, ix].sum()),
                    'mau_so_cot_giay': 620*len(ix),
                    'ti_le': float(Z[100:720, ix].mean()) if ix else None}
    n6 = []
    for a in range(720, 1441, 60):
        b = min(a+60, 1441)
        n6.append({'tu': a, 'den_exclusive': b, 'so_giay': b-a,
                   'so_giay_bao': int(Z[a:b].any(axis=1).sum()),
                   'r_obs': float(Z[a:b].any(axis=1).mean()),
                   'so_bao_cot_giay': int(Z[a:b].sum()),
                   'mau_so_cot_giay': (b-a)*len(columns),
                   'ti_le_cot_giay': float(Z[a:b].mean())})
    service_map = {}
    unmatched = sorted({c.split('_', 1)[0] for c in columns} - set(universe))
    for key in ('baseline', '5', '10', '20'):
        keep = np.ones(len(columns), dtype=bool) if key == 'baseline' else ~dense[key]
        service_map[key] = {}
        for s in universe:
            ix = [j for j, c in enumerate(columns) if c.split('_', 1)[0] == s and keep[j]]
            positions = np.flatnonzero(Z[720:, ix].any(axis=1)) if ix else np.array([], dtype=int)
            service_map[key][s] = {'so_cot': len(ix),
                                   'first_after_index': int(positions[0]+720) if len(positions) else None}
    return {'s0': 100, 'moc': 720, 'd': len(columns), 't_hat_index': first,
            't_hat_plus_index': int(after[0]) if len(after) else None,
            'history': hist, 'columns': rows,
            'N1': {str(k): bool(first is not None and first < 200 and head >= k*tail)
                   for k in N1_LEVELS},
            'N2': n2,
            'N3': {str(k): bool(first is not None and first < 720 and not n2[str(k)])
                   for k in N2_LEVELS},
            'N4': bool(any(sd[j] == 0 for j in trig)),
            'trigger_columns': [columns[j] for j in trig],
            'trigger_types': {kind: sum(column_type(columns[j]) == kind for j in trig)
                              for kind in sorted({column_type(columns[j]) for j in trig})},
            'r_obs': float(Z[100:720].any(axis=1).mean()),
            'r_ind': float(1-np.prod(1-p)),
            'r_nom': float(1-(1-P0)**len(columns)),
            'N5_types': n5, 'N6_minutes': n6,
            'E_services': service_map, 'E_columns_outside_U': unmatched,
            'V7': {'status': 'N/A', 'ly_do': 'N1–N4 chứa điều kiện báo động; N5/N6 là mô tả.'}}

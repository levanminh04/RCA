"""BARO RobustScorer (§6.1). RCAEval 259ea41 e2e/baro.py, tham số mặc định."""
from ..ban_ghi import thuc_the_metric
from ..cua_so import doi_ten_latency, tien_xu_ly_main
from . import LoiRunner, loi

VERSION = 'RCAEval 259ea41 e2e/baro.py'


def chuan_bi(metric_win):
    """Cắt trước (runner), tiền xử lý main.py sau, đổi tên latency như main.py:333–339."""
    return doi_ten_latency(tien_xu_ly_main(metric_win))


def diem_lai(data, t):
    """Tính lại max robust z bằng đúng các lời gọi của baro() (baro.py:22–50)."""
    from RCAEval.io.time_series import preprocess
    from sklearn.preprocessing import RobustScaler
    n = preprocess(data=data[data['time'] < t], dataset='re2-tt', dk_select_useful=False)
    a = preprocess(data=data[data['time'] >= t], dataset='re2-tt', dk_select_useful=False)
    cols = [x for x in n.columns if x in a.columns]
    out = []
    for c in cols:
        sc = RobustScaler().fit(n[c].to_numpy().reshape(-1, 1))
        z = sc.transform(a[c].to_numpy().reshape(-1, 1))[:, 0]
        out.append((c, float(max(z))))
    return out, cols


def chay(metric_win, t):
    from RCAEval.e2e.baro import baro
    data = chuan_bi(metric_win)
    shape = {'metric_cols': int(metric_win.shape[1] - 1), 'metric_cols_after_preprocess': None}
    try:
        out = baro(data, t, dataset='re2-tt', dk_select_useful=False)
    except Exception as exc:  # noqa: BLE001 — lỗi của phương pháp
        r = loi(exc); r['input_shape'] = shape
        return r
    diem, cols = diem_lai(data, t)
    shape['metric_cols_after_preprocess'] = len(cols)
    lai = [c for c, _ in sorted(diem, key=lambda x: x[1], reverse=True)]
    if lai != out['ranks']:
        raise LoiRunner('BARO: thứ tự dựng lại từ khóa không trùng thứ tự chính thức')
    sc = dict(diem)
    items = [(c, thuc_the_metric(c), (sc[c],)) for c in out['ranks']]
    return {'status': 'OK' if items else 'NO_EVIDENCE', 'method_status_raw': None, 'error': None,
            'ranking_native': out['ranks'], 'items': items,
            'observed_entities': sorted({thuc_the_metric(c) for c in cols}),
            'input_shape': shape, 'diagnostics': {'key_check': 'pass', 'rank_equals_column_order': out['ranks'] == cols}}

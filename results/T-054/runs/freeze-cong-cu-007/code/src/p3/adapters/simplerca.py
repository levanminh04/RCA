"""SimpleRCA (M4, quy ước T-017) (§6.2, WHY-17, WHY-33).

Runner đã lọc span theo §5.2 trước khi gọi `prepare`, vì adapter T-017 chỉ lọc theo startTime.
Metric truyền dạng thô (như T-017 run_dev.py:96–99); `prepare` tự cắt cùng cửa sổ.
"""
from ..ban_ghi import thuc_the_metric
from . import loi

VERSION = 'src/simplerca (T-017, M4)'


def chay(metric_win, spans, logs, t):
    from simplerca import Config, diagnose
    from simplerca.adapter import core_input, prepare
    tr = None if spans is None else spans[['serviceName', 'startTime', 'duration']]
    shape = {'metric_cols': int(metric_win.shape[1] - 1), 'spans': None if tr is None else int(len(tr)),
             'log_rows': None if logs is None else int(len(logs))}
    try:
        prepared = prepare(metric_win, tr, logs, t)
        res = diagnose(**core_input(prepared), config=Config())
    except Exception as exc:  # noqa: BLE001
        r = loi(exc); r['input_shape'] = shape
        return r
    obs = sorted({thuc_the_metric(s) for s in prepared.observed_services})
    if res['status'] == 'abstain':
        return {'status': 'NO_EVIDENCE', 'method_status_raw': 'abstain', 'error': None, 'items': [],
                'ranking_native': res['ranks'], 'observed_entities': obs, 'input_shape': shape}
    items = [(s, thuc_the_metric(s), (float(res['scores'][s]['score']),)) for s in res['ranks']]
    return {'status': 'OK', 'method_status_raw': res['status'], 'error': None,
            'ranking_native': res['ranks'], 'items': items, 'observed_entities': obs, 'input_shape': shape,
            'diagnostics': {'key_check': 'pass', 'tie_groups_goc': len(res['tie_groups'])}}

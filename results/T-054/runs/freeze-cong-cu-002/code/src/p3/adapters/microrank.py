"""MicroRank-RCAEval sửa đầu vào (§6.3, WHY-31). Xếp đầy đủ làm chính; kèm top-11 của code."""
from . import loi

VERSION = 'src/microrank (MicroRank-RCAEval sửa đầu vào)'
RONG = ('missing_window', 'no_anomalous_traces', 'no_normal_traces')


def chay(spans, t):
    from microrank import microrank
    shape = {'spans': int(len(spans)), 'operations': None}
    obs = sorted(set(spans['serviceName'].dropna().astype(str)))
    try:
        res = microrank(spans, int(t) * 1_000_000)
    except Exception as exc:  # noqa: BLE001 — ValueError của code: operation mới, std NaN, ID xung đột...
        r = loi(exc); r['input_shape'] = shape; r['observed_entities'] = obs
        return r
    st = res.get('status')
    if st in RONG or not res.get('full_ranks'):
        return {'status': 'NO_EVIDENCE', 'method_status_raw': st, 'error': None, 'items': [],
                'ranking_native': [], 'observed_entities': obs, 'input_shape': shape}
    ops = res['operation_services']
    shape['operations'] = len(ops)
    items = [(op, ops[op], (res['scores'][op],)) for op in res['full_ranks']]
    return {'status': 'OK', 'method_status_raw': st, 'error': None,
            'ranking_native': res['full_ranks'], 'items': items, 'observed_entities': obs, 'input_shape': shape,
            'diagnostics': {'key_check': 'pass', 'counts': res.get('counts')},
            'extra': {'top11_ranks': res['ranks'], 'service_ranks_top11': res['service_ranks_top11']}}

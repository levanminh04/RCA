"""TraceRCA lọc hữu hạn (§6.4, WHY-32). Gọi RCAEval e2e/tracerca.py nguyên trạng; đọc `ji_dict`
lúc hàm trả về bằng sys.setprofile (D11); giữ operation có ji hữu hạn, sắp giảm dần."""
import math
import sys

from . import LoiRunner, loi

VERSION = 'RCAEval 259ea41 e2e/tracerca.py + lọc ji hữu hạn'


def _mod():
    import importlib
    return importlib.import_module('RCAEval.e2e.tracerca')  # RCAEval.e2e.__init__ che tên module bằng hàm


def _goi(mod, spans, t_us):
    bat = {}
    code = mod.tracerca.__code__

    def prof(frame, event, arg):
        if event == 'return' and frame.f_code is code:
            bat['ji'] = dict(frame.f_locals.get('ji_dict') or {})
    old = sys.getprofile()
    sys.setprofile(prof)
    try:
        out = mod.tracerca(spans.copy(deep=True), t_us, dataset='re2-tt')
    finally:
        sys.setprofile(old)
    return out, bat.get('ji')


def chay(spans, t):
    shape = {'spans': int(len(spans)), 'operations': None}
    obs = sorted(set(spans['serviceName'].dropna().astype(str)))
    mod = _mod()
    try:
        out, ji = _goi(mod, spans, int(t) * 1_000_000)
    except Exception as exc:  # noqa: BLE001 — KeyError khi operation mới sau mốc
        r = loi(exc); r['input_shape'] = shape; r['observed_entities'] = obs
        return r
    if ji is None:
        raise LoiRunner('TraceRCA: không bắt được ji_dict')
    d = spans[['serviceName', 'methodName', 'operationName']].copy()
    d['methodName'] = d['methodName'].fillna(d['operationName'])
    d['operation'] = d['serviceName'] + '_' + d['methodName']
    pairs = d[['operation', 'serviceName']].drop_duplicates()
    amb = pairs[pairs['operation'].duplicated(keep=False)]
    if not amb.empty:
        return {'status': 'ERROR', 'error': 'operation ứng nhiều service: ' + ','.join(sorted(set(amb.operation))[:5]),
                'items': [], 'ranking_native': out['ranks'], 'observed_entities': obs, 'input_shape': shape}
    svc = dict(zip(pairs['operation'], pairs['serviceName']))
    shape['operations'] = len(ji)
    co_nan = any(not math.isfinite(float(v)) for v in ji.values())
    huu_han = sorted([(op, float(v)) for op, v in ji.items() if math.isfinite(float(v))],
                     key=lambda x: x[1], reverse=True)
    if not co_nan and [op for op, _ in huu_han] != list(out['ranks']):
        raise LoiRunner('TraceRCA: thứ tự từ ji_dict không trùng thứ tự chính thức khi không có NaN')
    items = [(op, svc[op], (v,)) for op, v in huu_han]
    return {'status': 'OK' if items else 'NO_EVIDENCE', 'method_status_raw': None, 'error': None,
            'ranking_native': [op for op, _ in huu_han], 'items': items, 'observed_entities': obs,
            'input_shape': shape,
            'diagnostics': {'key_check': 'pass' if not co_nan else 'nan_present', 'ji_nan': sum(
                not math.isfinite(float(v)) for v in ji.values())},
            'extra': {'ranks_chinh_thuc': list(out['ranks'])}}

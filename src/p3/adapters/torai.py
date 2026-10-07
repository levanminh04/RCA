"""TORAI bản sửa (§6.6, WHY-19, WHY-20, WHY-29). Hai tầng tiến trình:

1. chuan_bi_A / chuan_bi_B (Python 3.12): dựng bốn bảng metric, logts, tracets_err, tracets_lat.
2. chay (py38-rcdlock, Python 3.8): `np.random.seed(seed)` rồi gọi `torai_sua.torai` nguyên trạng;
   dựng khóa hai cấp từ biến cục bộ bắt bằng sys.setprofile (D10) và kiểm khớp `ranks`.

Không truyền service, fault_type, case cho phương pháp. Mã này phải chạy được trên Python 3.8.
"""
import sys

import numpy as np
import pandas as pd

VERSION = 'src/torai/torai_sua.py (RCAEval 259ea41 sửa A, B)'
N_DONG = 20  # main.py:381–393 với --length 10: 20 dòng mỗi phía


def chuan_bi_metric(metric_win):
    from ..cua_so import doi_ten_latency, tien_xu_ly_main
    return doi_ten_latency(tien_xu_ly_main(metric_win, chi_ts=True))


def cat_20(df, t):
    a = df[df['time'] < t].tail(N_DONG)
    b = df[df['time'] >= t].head(N_DONG)
    return pd.concat([a, b], ignore_index=True)


def chuan_bi_A(metric_win, logts, tracets_err, tracets_lat, t):
    """Nguồn A: file tác giả, cắt 20 dòng mỗi phía theo time < t; ghi lệch lưới so với t."""
    lt, te, tl = cat_20(logts, t), cat_20(tracets_err, t), cat_20(tracets_lat, t)
    times = logts['time'].to_numpy()
    sau = times[times >= t]
    N = lt[lt['time'] < t]
    info = {'lech_luoi_s': None if not len(sau) else int(sau[0] - t),
            'N_phu': [int(N['time'].min()), int(N['time'].max()) + 15] if len(N) else None,
            'A_phu': [int(lt[lt['time'] >= t]['time'].min()), int(lt['time'].max()) + 15] if (lt['time'] >= t).any() else None,
            'nguong_tracets_lat': 'toàn file (tác giả)'}
    return chuan_bi_metric(metric_win), lt, te, tl, info


def chuan_bi_B(metric_win, spans, logs, t):
    from ..torai_b import nguon_b
    lt, te, tl, info = nguon_b(spans, logs, t)
    return chuan_bi_metric(metric_win), lt.reset_index(), te.reset_index(), tl.reset_index(), info


def _khoi(loc, rcd_returns):
    """Dựng khối theo đúng vòng lặp torai_sua.py:296–360."""
    cluster_rank, y_pred = loc['cluster_rank'], np.asarray(loc['y_pred'])
    y_train, service_list = np.asarray(loc['y_train']), list(loc['service_list'])
    blocks, it, fallback, n_multi = [], iter(rcd_returns), 0, 0
    for cluster_idx, score in cluster_rank:
        idx = np.where(y_pred == cluster_idx)[0]
        members = [service_list[i] for i in idx]
        ys = y_train[idx]
        if len(members) == 1:
            blocks.append({'key': [float(score)], 'groups': [[members[0]]], 'nhanh': 'don'})
            continue
        n_multi += 1
        aa = sorted(zip(members, ys), key=lambda x: x[1], reverse=True)
        ret = next(it)
        tmp = [s.split('_')[0] for s in ret['ranks']]
        internal = []
        for s in tmp:
            if s not in internal:
                internal.append(s)
        if len(internal) == len(members):
            blocks.append({'key': [float(score)], 'groups': [[s] for s in internal], 'nhanh': 'rcd'})
        else:
            fallback += 1
            groups = []
            for i, (s, y) in enumerate(aa):
                if i and y == aa[i - 1][1]:
                    groups[-1].append(s)
                else:
                    groups.append([s])
            blocks.append({'key': [float(score)], 'groups': groups, 'nhanh': 'du_phong'})
    return blocks, {'cum': len(cluster_rank), 'cum_nhieu_service': n_multi, 'cum_du_phong': fallback}


def chay(metric, logts, tracets_err, tracets_lat, t, seed, dataset='torai-tt'):
    from torai import torai_sua as mod
    data = {'metric': metric, 'logts': logts, 'tracets_err': tracets_err, 'tracets_lat': tracets_lat}
    loc, rcd = {}, []
    code_t, code_r = mod.torai.__code__, mod._rcd_multimodal.__code__

    def prof(frame, event, arg):
        if event == 'return':
            if frame.f_code is code_t:
                loc.update({k: frame.f_locals.get(k) for k in ('cluster_rank', 'y_pred', 'y_train', 'service_list')})
            elif frame.f_code is code_r:
                rcd.append(arg)
    shape = {'metric_cols': int(metric.shape[1] - 1), 'logts_cols': int(logts.shape[1] - 1),
             'tracets_err_cols': int(tracets_err.shape[1] - 1), 'tracets_lat_cols': int(tracets_lat.shape[1] - 1)}
    np.random.seed(seed)
    old = sys.getprofile()
    sys.setprofile(prof)
    try:
        out = mod.torai(data, t, dataset=dataset, anomalies=None, dk_select_useful=False, sli=None, verbose=False)
    except Exception as exc:  # noqa: BLE001
        return {'status': 'ERROR', 'error': '%s: %s' % (type(exc).__name__, exc), 'items': [], 'ranking_native': [],
                'input_shape': shape}
    finally:
        sys.setprofile(old)
    ranks = list(out['ranks'])
    if not ranks:
        return {'status': 'NO_EVIDENCE', 'items': [], 'ranking_native': [], 'input_shape': shape}
    blocks, diag = _khoi(loc, rcd)
    noi = [s for b in blocks for g in b['groups'] for s in g]
    if ['%s_A' % s for s in noi] != ranks:
        from ..selector import LoiRunner
        raise LoiRunner('TORAI: thứ tự dựng lại từ khối không trùng ranks chính thức')
    diag['key_check'] = 'pass'
    diag['ty_le_du_phong'] = (diag['cum_du_phong'] / diag['cum_nhieu_service']) if diag['cum_nhieu_service'] else None
    obs = sorted(set(loc['service_list']))
    for b in blocks:
        b.pop('nhanh_', None)
    return {'status': 'OK', 'method_status_raw': None, 'error': None, 'ranking_native': ranks,
            'items': [('%s_A' % s, s, b['key']) for b in blocks for g in b['groups'] for s in g],
            'blocks': [{'key': b['key'], 'groups': b['groups']} for b in blocks],
            'observed_entities': obs, 'input_shape': shape, 'diagnostics': diag,
            'extra': {'nhanh_khoi': [b['nhanh'] for b in blocks]}}

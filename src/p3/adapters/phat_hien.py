"""Hai bộ phát hiện chế độ (b) (§7.1–7.3, WHY-34). Nhận cả bản ghi metric một lần; không nhận mốc tiêm,
nhãn, tên hay đường dẫn ca. Gọi là phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố."""
import numpy as np

VERSION_BOCPD = 'BARO e35f4ec _bocpd.online_changepoint_detection, hazard 50, MultivariateT; m[i] = argmax R[:, i+1]'
VERSION_NSIGMA = 'BARO e35f4ec anomaly_detection.nsigma, k=3, startsfrom=100'


def cot_bocpd(columns):
    """Q-67: tên chứa latency-50 hoặc _error, bỏ queue-master và rabbitmq_ (reproducibility.py:140–145)."""
    out = []
    for c in columns:
        if c == 'time' or 'queue-master' in c or 'rabbitmq_' in c:
            continue
        if 'latency-50' in c or '_error' in c:
            out.append(c)
    return out


def tien_xu_ly_bocpd(df):
    """reproducibility.py:147–154 trên cả chuỗi (look-ahead, khai báo)."""
    from baro.utility import drop_constant
    data = drop_constant(df)
    data = data.ffill().fillna(0)
    for c in data.columns:
        data[c] = (data[c] - np.min(data[c])) / (np.max(data[c]) - np.min(data[c]))
    return data.ffill().fillna(0)


def diem_doi_tu_R(R):
    """m[i] = argmax R[:, i+1], i = 0..T-1; điểm đổi = i >= 1 có |m[i] - m[i-1]| > 1. Trả (cps, m) hoặc
    (None, chỉ số cột R hỏng đầu tiên) nếu R[:, 1..T] có phần tử không hữu hạn (V2-S1)."""
    T = R.shape[1] - 1
    sub = R[:, 1:T + 1]
    bad = ~np.isfinite(sub).all(axis=0)
    if bad.any():
        return None, int(np.argmax(bad)) + 1
    m = sub.argmax(axis=0)
    cps = [i for i in range(1, T) if abs(int(m[i]) - int(m[i - 1])) > 1]
    return cps, m


def bocpd(metrics):
    from functools import partial
    from baro._bocpd import MultivariateT, constant_hazard, online_changepoint_detection
    from baro.utility import find_cps
    times = metrics['time'].to_numpy()
    cols = cot_bocpd(metrics.columns)
    data = tien_xu_ly_bocpd(metrics[cols])
    shape = {'T': int(len(times)), 'cot_tho': len(cols), 'cot_sau_tien_xu_ly': int(data.shape[1])}
    try:
        R, maxes = online_changepoint_detection(data.to_numpy(), partial(constant_hazard, 50),
                                                MultivariateT(dims=data.shape[1]))
    except Exception as exc:  # noqa: BLE001
        return {'status': 'ERROR', 'error': f'{type(exc).__name__}: {exc}', 'alarms': [], 'input_shape': shape,
                'detector_columns': cols}
    cps, m = diem_doi_tu_R(R)
    goc = [int(i) for i, _ in find_cps(maxes)]
    if cps is None:
        return {'status': 'ERROR', 'error': f'posterior BOCPD không hữu hạn ở cột R {m}', 'alarms': [],
                'input_shape': shape, 'detector_columns': cols, 'diagnostics': {'cot_R_hong_dau_tien': m,
                                                                                'diem_doi_maxes_goc': goc}}
    return {'status': 'OK', 'alarms': [int(times[i]) for i in cps], 'chi_so': cps, 'input_shape': shape,
            'detector_columns': cols, 'bat_dau_danh_gia': 1,
            'diagnostics': {'diem_doi_maxes_goc': goc, 'co_sentinel_goc': bool(goc and goc[-1] == len(times))}}


def nsigma(metrics, tap_cot='bocpd'):
    """D9: inf → NaN, ffill (chỉ quá khứ); không min–max, không bỏ cột hằng. Báo động gộp, sắp, bỏ trùng."""
    from baro.anomaly_detection import nsigma as ns
    cols = cot_bocpd(metrics.columns) if tap_cot == 'bocpd' else [c for c in metrics.columns if c != 'time']
    data = metrics[['time'] + cols].replace([np.inf, -np.inf], np.nan).ffill()
    shape = {'T': int(len(data)), 'cot': len(cols)}
    try:
        al = ns(data, k=3, startsfrom=100)
    except Exception as exc:  # noqa: BLE001
        return {'status': 'ERROR', 'error': f'{type(exc).__name__}: {exc}', 'alarms': [], 'input_shape': shape,
                'detector_columns': cols}
    return {'status': 'OK', 'alarms': sorted({int(a) for a in al}), 'input_shape': shape,
            'detector_columns': cols, 'bat_dau_danh_gia': 100}


def luot_rca(alarms, tro=300):
    """§7.5 (D7): báo động đầu mở lượt RCA ở t̂; báo động trong `tro` giây sau thông báo không mở thông báo mới."""
    tb = []
    for a in sorted(alarms):
        if not tb or a >= tb[-1] + tro:
            tb.append(int(a))
    return {'t_hat': tb[0] if tb else None, 'thong_bao': tb, 'so_thong_bao': len(tb)}

"""Cắt cửa sổ và tiền xử lý theo §5 (WHY-22).

N = [t-300, t), A = [t, t+300), theo timestamp, nửa mở. Metric theo `time` (giây);
span vào khi startTime >= t-300 và startTime + duration < t+300 (µs, so bằng số nguyên);
log theo `timestamp` (giây). Runner cắt trước; tiền xử lý của tác giả chạy sau, chỉ trên
dữ liệu trong cửa sổ (D1). Thiếu dữ liệu thì ghi độ dài thực, không kéo dài cửa sổ.
"""
import numpy as np
import pandas as pd

NUA = 300
US = 1_000_000


def _so_nguyen(t):
    if isinstance(t, (bool, np.bool_)) or not float(t).is_integer():
        raise ValueError(f'mốc chia phải là giây nguyên: {t!r}')
    return int(t)


def cat_metric(metrics, t, nua=NUA):
    t = _so_nguyen(t)
    tm = pd.to_numeric(metrics['time'], errors='raise')
    return metrics.loc[(tm >= t - nua) & (tm < t + nua)].reset_index(drop=True)


def cat_span(traces, t, nua=NUA):
    """Span phải bắt đầu >= t-nua và kết thúc < t+nua (đã có lúc t+nua). [D2]"""
    t = _so_nguyen(t)
    st = traces['startTime'].astype('int64')
    en = st + traces['duration'].astype('int64')
    keep = (st >= (t - nua) * US) & (en < (t + nua) * US)
    return traces.loc[keep].reset_index(drop=True)


def cat_log(logs, t, nua=NUA):
    t = _so_nguyen(t)
    ts = pd.to_numeric(logs['timestamp'], errors='raise')
    return logs.loc[(ts >= t - nua) & (ts < t + nua)].reset_index(drop=True)


def _giay_thuc(tmin, tmax, lo, hi):
    """Số giây của [lo, hi) có trong phạm vi file [tmin, tmax] (nhịp 1 s, biên nguyên)."""
    if tmin is None:
        return 0
    return int(max(0, min(hi, tmax + 1) - max(lo, tmin)))


def cat_ca(metrics, traces, logs, t, nua=NUA):
    """Cắt ba nguồn quanh t. Trả (dict dữ liệu, dict thông tin cửa sổ)."""
    t = _so_nguyen(t)
    m = cat_metric(metrics, t, nua)
    tr = cat_span(traces, t, nua) if traces is not None else None
    lg = cat_log(logs, t, nua) if logs is not None else None
    tm = pd.to_numeric(metrics['time'])
    tmin, tmax = (int(tm.min()), int(tm.max())) if len(tm) else (None, None)
    mt = pd.to_numeric(m['time'])
    info = {
        't': t, 'N': [t - nua, t], 'A': [t, t + nua],
        'rows_N': int((mt < t).sum()), 'rows_A': int((mt >= t).sum()),
        'seconds_N': _giay_thuc(tmin, tmax, t - nua, t),
        'seconds_A': _giay_thuc(tmin, tmax, t, t + nua),
        'spans_N': None if tr is None else int((tr['startTime'].astype('int64') < t * US).sum()),
        'spans_A': None if tr is None else int((tr['startTime'].astype('int64') >= t * US).sum()),
        'log_rows_N': None if lg is None else int((pd.to_numeric(lg['timestamp']) < t).sum()),
        'log_rows_A': None if lg is None else int((pd.to_numeric(lg['timestamp']) >= t).sum()),
        'circa_current': None,
    }
    return {'metric': m, 'traces': tr, 'logs': lg}, info


def tien_xu_ly_main(data, chi_ts=False):
    """Tiền xử lý metric như RCAEval main.py:290–309, chạy sau khi đã cắt (D1).

    chi_ts=True là nhánh torai-TT/mm-tt của main.py:298–301 (giữ cột ts-* và time).
    """
    data = data.copy()
    if 'time.1' in data:
        data = data.drop(columns=['time.1'])
    data = data.loc[:, ~data.columns.str.endswith('_latency-50')]
    if chi_ts:
        time_col = data['time']
        data = data.loc[:, data.columns.str.startswith('ts-')]
        data['time'] = time_col
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.ffill()
    data = data.fillna(0)
    return data


def doi_ten_latency(data):
    """main.py:333–339: đổi `_latency-90` thành `_latency` trước khi gọi phương pháp."""
    return data.rename(columns={c: c.replace('_latency-90', '_latency')
                                for c in data.columns if c.endswith('_latency-90')})


def dem_d1(metrics, t, nua=NUA):
    """D1 (§5.3): so 'cắt trước, tiền xử lý sau' với thứ tự main.py (tiền xử lý toàn file rồi cắt).

    Không dùng nhãn nào ngoài mốc t. Đếm ô khác nhau (trừ cột time) trong cửa sổ.
    Ghi thêm: cắt theo dòng như main.py (tail/head) có cho đúng các dòng của cắt theo thời gian không.
    """
    t = _so_nguyen(t)
    toan = tien_xu_ly_main(metrics)
    a = cat_metric(toan, t, nua)
    b = tien_xu_ly_main(cat_metric(metrics, t, nua))
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        raise ValueError('D1: hai cách cho bảng khác hình dạng')
    cols = [c for c in a.columns if c != 'time']
    av, bv = a[cols].to_numpy(dtype=float), b[cols].to_numpy(dtype=float)
    khac = ~((av == bv) | (np.isnan(av) & np.isnan(bv)))
    raw = cat_metric(metrics, t, nua)[cols].replace([np.inf, -np.inf], np.nan)
    rong_dau = raw.isna().to_numpy()
    n = toan[toan['time'] < t].tail(nua)
    an = toan[toan['time'] >= t].head(nua)
    theo_dong = pd.concat([n, an], ignore_index=True)
    return {
        'n_cot': len(cols), 'n_dong': int(len(a)), 'n_o': int(khac.size),
        'o_khac': int(khac.sum()), 'cot_co_o_khac': int(khac.any(axis=0).sum()),
        'o_trong_tho_trong_cua_so': int(rong_dau.sum()),
        'cat_theo_dong_trung_cat_theo_thoi_gian': bool(
            len(theo_dong) == len(a) and (theo_dong['time'].to_numpy() == a['time'].to_numpy()).all()),
        'cot_khac': sorted(np.array(cols)[khac.any(axis=0)].tolist()),
    }

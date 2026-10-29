"""Adapter dữ liệu dev → API M1 (dinh-chinh-cai-dat.md CĐ4.1, CĐ5, CĐ11; hop-dong.json; Đ9 v1.1, Đ19).

Chỉ runner gọi; phương pháp không thấy đường dẫn, mã mờ hay case_dir. Không đọc nhãn: nhận allowlist (đường dẫn,
hash), mã mờ và mốc t của lượt (chế độ (a): mốc tiêm runner truyền, Q-66; mốc giả: t − 300).
- RE2-TT: `p3.selector.chon_ca` (kiểm SHA-256), đọc parquet; miền như `p3.cua_so.cat_span`, `cat_metric`, `cat_log`.
- Nezha-OB: `p3.nezha.chon_ca` rồi `p3.nezha.doc_cua_so` (mốc t_ns trong allowlist; miền [t − 300, t + 300)).
- F của từng nguồn: danh sách [min x, max x] của TỪNG file, tính trên toàn file (trace theo end, log theo mốc, metric
  theo cột thời gian), không gộp khe; r theo `hop-dong.json#/quan_sat/do_phan_giai_r` (Đ9 v1.1; Đ19 điểm 4).
- Metric: giá trị không hữu hạn thành None (đặc tả v1 dòng 110). RE2-TT một file metric mỗi ca nên
  `thoi_gian_nguon = "metrics.time"` (Đ19 điểm 3); Nezha-OB truyền mốc ns thật của từng nguồn từ `provenance` và
  `phan_hoach_NA_da_kiem` (đã kiểm ở `nezha.doc_cua_so`); coverage khai theo từng nguồn metric. Mã nguồn là chuỗi trung tính ('metric'; 'metric:<dịch vụ>',
  'metric:front_service'), không là đường dẫn (luật cứng 6).
- `chuoi_cam`: mã mờ, case_dir, tên thư mục ca (mang root và loại lỗi) và mọi đường dẫn tệp của ca; runner từ chối nếu chuỗi nào lọt vào đầu vào (CĐ12).
- Log Nezha-OB: chuỗi vào Drain theo CĐ4.1; `severity_raw` theo đường đọc `hop-dong.json#/severity/Nezha-OB`.
"""
import csv
import json
import math

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from p3 import nezha, selector
from m1 import e3

NS = 10 ** 9
US = 10 ** 6
NUA = 300
COT_SPAN_RE2 = ['traceID', 'spanID', 'parentSpanID', 'serviceName', 'operationName', 'startTime', 'duration']
TU_KHOA_RE2 = ['ERROR', 'FAIL', 'EXCEPTION']  # src/simplerca/core.py:22


def ho_so_nguon(hop_dong, dataset):
    """CĐ5: hồ sơ nguồn điền từ hop-dong.json."""
    k = hop_dong['kenh'][dataset]
    if dataset == 'RE2-TT':
        return {'kenh_metric': {'kieu': 'hau_to', 'bang': dict(k['metric_theo_hau_to'])},
                'quy_tac_log': {'kieu': 'tu_khoa', 'tu_khoa': list(TU_KHOA_RE2)},
                'nguon_khoi_phat': ['trace', 'metric']}
    if dataset == 'Nezha-OB':
        sev = hop_dong['severity']['Nezha-OB']
        return {'kenh_metric': {'kieu': 'ten_kenh', 'bang': dict(k['metric_theo_kenh'])},
                'quy_tac_log': {'kieu': 'severity', 'loi': list(sev['loi']), 'khong_loi': list(sev['khong_loi'])},
                'nguon_khoi_phat': ['trace']}
    raise ValueError(dataset)


def _r_ns(hop_dong, khoa):
    return int(round(hop_dong['quan_sat']['do_phan_giai_r'][khoa] * NS))


def _so(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _dong_metric(df, cot_thoi_gian='time'):
    cols = [c for c in df.columns if c != cot_thoi_gian]
    out = []
    for row in df.itertuples(index=False):
        r = dict(zip(df.columns, row))
        d = {'time': int(r[cot_thoi_gian])}
        for c in cols:
            d[c] = _so(r[c])
        out.append(d)
    return out, cols


def _rong(x):
    return x is None or (isinstance(x, float) and math.isnan(x)) or x == ''


# ---------------------------------------------------------------- RE2-TT

def ca_re2tt(allowlist, opaque_id, t, repo_root, hop_dong, inventory, kiem_hash=True, canh_tinh=None):
    """Một ca RE2-TT cho runner.pha1. t: mốc của lượt (giây nguyên)."""
    files = selector.chon_ca(allowlist, opaque_id, repo_root, kiem_hash=kiem_hash)
    for ten in ('traces.parquet', 'metrics.parquet'):
        if ten not in files:
            raise selector.LoiRunner(f'ca thiếu {ten}')
    t = int(t)
    lo, hi = t - NUA, t + NUA
    tr = pq.read_table(files['traces.parquet'], columns=COT_SPAN_RE2).to_pandas()
    st = tr['startTime'].to_numpy(np.int64)
    en = st + tr['duration'].to_numpy(np.int64)
    F_trace = [[int(en.min()) * 1000, int(en.max()) * 1000]] if len(en) else []
    keep = (st >= lo * US) & (en < hi * US)
    sub = tr.loc[keep]
    spans = [{'traceID': str(a), 'spanID': str(b), 'parentSpanID': '' if _rong(c) else str(c), 'owner': str(d),
              'operation': str(e), 'start_us': int(f), 'duration_us': int(g)}
             for a, b, c, d, e, f, g in sub[COT_SPAN_RE2].itertuples(index=False, name=None)]
    mt = pq.read_table(files['metrics.parquet']).to_pandas()
    tm = pd.to_numeric(mt['time'], errors='raise').to_numpy(np.int64)
    F_metric = [[int(tm.min()) * NS, int(tm.max()) * NS]] if len(tm) else []
    metrics, cols = _dong_metric(mt.loc[(tm >= lo) & (tm < hi)].reset_index(drop=True))
    logs, F_log, cot_log = [], [], None
    if 'logs.parquet' in files:
        lg = pq.read_table(files['logs.parquet']).to_pandas()
        cot_log = list(lg.columns)
        ts = pd.to_numeric(lg['timestamp'], errors='raise').to_numpy(float)
        if len(ts):
            F_log = [[int(round(ts.min() * NS)), int(round(ts.max() * NS))]]
        w = (ts >= lo) & (ts < hi)
        for x, e, m in zip(ts[w], lg['container_name'].to_numpy()[w], lg['message'].astype(str).to_numpy()[w]):
            logs.append({'timestamp': int(x) if float(x).is_integer() else float(x), 'entity': str(e), 'message': m})
    params_ca = {
        'ho_so_nguon': ho_so_nguon(hop_dong, 'RE2-TT'),
        'don_vi_thoi_gian': {'spans.start_us': 'us', 'metrics.time': 's', 'logs.timestamp': 's'},
        'coverage': {'trace': {'khoang': F_trace, 'r_ns': _r_ns(hop_dong, 'RE2-TT span')},
                     'log': {'khoang': F_log, 'r_ns': _r_ns(hop_dong, 'RE2-TT log')},
                     'metric': {'khoang': F_metric, 'r_ns': _r_ns(hop_dong, 'RE2-TT metric')}},
        'nguon_metric': {c: 'metric' for c in cols},
        'thoi_gian_nguon': {'metric': 'metrics.time'},
        'phan_hoach_NA_da_kiem': {}}
    if canh_tinh is not None:
        params_ca['canh_tinh'] = canh_tinh
    case_dir = allowlist[opaque_id].get('case_dir')
    cam = [opaque_id] + ([case_dir, case_dir.rstrip('/').rsplit('/', 1)[-1]] if case_dir else []) + sorted(
        m['path'] for m in allowlist[opaque_id]['files'].values() if m)
    return {'opaque_id': opaque_id, 'case_dir': case_dir, 'chuoi_cam': cam, 'spans': spans,
            'metrics': metrics, 'logs': logs, 'inventory': list(inventory), 'aliases': {}, 'params_ca': params_ca,
            'chan_doan_adapter': {'span_toan_file': int(len(tr)), 'span_trong_mien': len(spans),
                                  'dong_metric_trong_mien': len(metrics), 'cot_metric': len(cols),
                                  'co_file_log': 'logs.parquet' in files, 'cot_log': cot_log,
                                  'dong_log_trong_mien': len(logs)}}


# ---------------------------------------------------------------- Nezha-OB

def severity_raw_nezha(cot_log):
    """hop-dong.json#/severity/Nezha-OB: JSON ngoài, khóa `log` là chuỗi JSON; giải mã lần hai, khóa `severity`.
    Trả giá trị thô (chưa chuẩn hóa) hoặc None."""
    try:
        ngoai = json.loads(cot_log)
        trong = json.loads(ngoai['log'])
    except (TypeError, ValueError, KeyError):
        return None
    return trong.get('severity') if isinstance(trong, dict) else None


def _khoang_file_nezha(sel):
    """F của từng file, đọc toàn file qua `nezha._open_source` (kiểm hash): trace theo end, log theo mốc (từng file
    phút); metric theo cột Time (từng nguồn, khóa là đường dẫn tương đối)."""
    out = {'trace': [], 'log': [], 'metric': {}}
    csv.field_size_limit(10_000_000)
    for rel, meta in sorted(sel['files'].items()):
        kind = nezha._relative_path(rel).parts[-2]
        with nezha._open_source(meta) as f:
            if kind == 'metric':
                x = [nezha.parse_time_ns(r['Time']) for r in csv.DictReader(f)]
            else:
                cot = 'EndTimeUnixNano' if kind == 'trace' else 'TimeUnixNano'
                x = [int(r[cot]) for r in csv.DictReader(f)]
        if not x:
            continue
        if kind == 'metric':
            out['metric'][rel] = [min(x), max(x)]
        else:
            out[kind].append([min(x), max(x)])
    return out


def ca_nezha(allowlist, opaque_id, repo_root, hop_dong, inventory=None, canh_tinh=None):
    """Một ca Nezha-OB cho runner.pha1. Mốc của lượt là t_ns của allowlist (trả kèm để runner dựng bảng mốc)."""
    sel = nezha.chon_ca(allowlist, opaque_id, repo_root)
    win = nezha.doc_cua_so(sel)
    sp = win['spans']
    spans = [{'traceID': str(a), 'spanID': str(b), 'parentSpanID': '' if _rong(c) else str(c), 'owner': str(d),
              'operation': str(e), 'start_us': int(f), 'duration_us': int(g)}
             for a, b, c, d, e, f, g in sp[['traceID', 'spanID', 'parentSpanID', 'serviceName', 'operationName',
                                            'startTime', 'duration']].itertuples(index=False, name=None)]
    metrics, cols = _dong_metric(win['metric'])
    prov = win['provenance']
    ma_nguon = {}
    for c in cols:
        rel = prov['channels'][c]['source']
        ma = 'metric:front_service' if rel.endswith('/front_service.csv') else 'metric:' + c.split('_', 1)[0]
        if ma_nguon.setdefault(rel, ma) != ma:
            raise selector.LoiRunner('Nezha: một nguồn metric cho nhiều dịch vụ')
    if len(set(ma_nguon.values())) != len(ma_nguon):
        raise selector.LoiRunner('Nezha: hai nguồn metric cùng mã')
    nguon_metric = {c: ma_nguon[prov['channels'][c]['source']] for c in cols}
    nguon_ts = {ma_nguon[rel]: list(s['timestamps_ns']) for rel, s in prov['sources'].items()
                if s['kind'] == 'metric'}
    lg = win['logs']
    logs = [{'timestamp': int(x), 'entity': str(e), 'message': e3.chuoi_vao_drain_nezha(m),
             'severity_raw': severity_raw_nezha(m)}
            for x, e, m in lg[['timestamp', 'container_name', 'message']].itertuples(index=False, name=None)]
    kf = _khoang_file_nezha(sel)
    r = _r_ns(hop_dong, 'Nezha-OB')
    params_ca = {
        'ho_so_nguon': ho_so_nguon(hop_dong, 'Nezha-OB'),
        'don_vi_thoi_gian': {'spans.start_us': 'us', 'metrics.time': 'ns', 'logs.timestamp': 'ns'},
        'coverage': dict({'trace': {'khoang': kf['trace'], 'r_ns': r}, 'log': {'khoang': kf['log'], 'r_ns': r}},
                         **{ma_nguon[rel]: {'khoang': [k], 'r_ns': r} for rel, k in kf['metric'].items()
                            if rel in ma_nguon}),
        'nguon_metric': nguon_metric, 'thoi_gian_nguon': nguon_ts,
        'phan_hoach_NA_da_kiem': {ma: True for ma in nguon_ts}}
    if canh_tinh is not None:
        params_ca['canh_tinh'] = canh_tinh
    t_ns = sel['t_ns']
    return {'opaque_id': opaque_id, 'spans': spans, 'metrics': metrics, 'logs': logs,
            'inventory': list(inventory if inventory is not None else nezha.UNIVERSE), 'aliases': {},
            'params_ca': params_ca, 't': t_ns // NS,
            'chuoi_cam': [opaque_id] + sorted(sel['files']) + sorted(k.rsplit('/', 1)[1] for k in sel['files']
                                                                      if '/trace/' in k or '/log/' in k),
            'chan_doan_adapter': {'span_trong_mien': len(spans), 'dong_metric': len(metrics), 'cot_metric': len(cols),
                                  'dong_log': len(logs), 'so_file_trace': len(kf['trace']),
                                  'so_file_log': len(kf['log']), 'cua_so': win['window']}}

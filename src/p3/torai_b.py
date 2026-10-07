"""Dựng đầu vào TORAI nguồn B từ parquet RE2 (§6.6, WHY-29) và theo quy ước tác giả cho K-B1.

Tên cột trace TT (N1): cột = service + '_' + operation chuẩn hóa. Chuẩn hóa operationName: bỏ
'/api/v1/', bỏ '{' '}', '_' → '-', mỗi chuỗi dấu cách hoặc '/' → một '-', bỏ '-' ở hai đầu.
Service = serviceName của span; riêng span có operationName chỉ là phương thức HTTP lấy serviceName
của span con (parentSpanID = spanID của nó); không có con thì giữ service của span.
Giao thức không nói khi span con thuộc nhiều service: lần dựng 1 lấy span con bắt đầu sớm nhất
(phá hòa theo spanID) và đếm số span như vậy.

Không import sklearn; chạy được trong T-016-cong-cu (drain3) và T-014-main.
"""
import re

import numpy as np
import pandas as pd

BIN = 15
HTTP = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')
US = 1_000_000


def chuan_hoa_op(op):
    s = str(op).replace('/api/v1/', '').replace('{', '').replace('}', '').replace('_', '-')
    s = re.sub(r'[ /]+', '-', s)
    return s.strip('-')


def ten_cot(traces, cach_con='som_nhat'):
    """Trả (Series tên cột theo chỉ số traces, số span HTTP có con thuộc nhiều service)."""
    t = traces[['traceID', 'spanID', 'parentSpanID', 'serviceName', 'operationName', 'startTime']].copy()
    is_http = t['operationName'].astype(str).isin(HTTP)
    svc = t['serviceName'].astype(str).copy()
    nhieu = 0
    if is_http.any():
        con = t.loc[t['parentSpanID'].notna(), ['traceID', 'parentSpanID', 'serviceName', 'startTime', 'spanID']]
        con = con.rename(columns={'parentSpanID': 'spanID_cha', 'serviceName': 'svc_con', 'spanID': 'spanID_con',
                                  'startTime': 'start_con'})
        cha = t.loc[is_http, ['traceID', 'spanID']].reset_index().rename(columns={'spanID': 'spanID_cha'})
        m = cha.merge(con, on=['traceID', 'spanID_cha'], how='inner')
        if len(m):
            dem = m.groupby('index')['svc_con'].nunique()
            nhieu = int((dem > 1).sum())
            if cach_con == 'som_nhat':
                m = m.sort_values(['index', 'start_con', 'spanID_con'], kind='mergesort')
            else:
                raise ValueError(cach_con)
            chon = m.drop_duplicates('index').set_index('index')['svc_con']
            svc.loc[chon.index] = chon.astype(str)
    cot = svc + '_' + t['operationName'].map(chuan_hoa_op)
    return cot, nhieu


def _luoi(t0, n_bin):
    return np.arange(t0, t0 + BIN * n_bin, BIN)


def dung_tracets(traces, luoi, span_nguong, cach_con='som_nhat'):
    """luoi: mảng thời điểm đầu bin (bước 15 s). span_nguong: mặt nạ bool chọn span học μ, σ (ddof 1).

    tracets_err = tổng statusCode mỗi (cột, bin); tracets_lat = số span có duration > μ + 3σ.
    Cột có < 2 span học ngưỡng thì bỏ khỏi tracets_lat (đếm vào `cot_bo_lat`).
    """
    cot, nhieu = ten_cot(traces, cach_con)
    t = pd.DataFrame({'cot': cot.to_numpy(), 'giay': (traces['startTime'].astype('int64') // US).to_numpy(),
                      'duration': traces['duration'].astype('float64').to_numpy(),
                      'status': pd.to_numeric(traces['statusCode'], errors='coerce').to_numpy(dtype='float64'),
                      'hoc': np.asarray(span_nguong, dtype=bool)})
    t0, t_end = int(luoi[0]), int(luoi[-1]) + BIN
    t = t[(t['giay'] >= t0) & (t['giay'] < t_end)].copy()
    t['bin'] = t0 + ((t['giay'] - t0) // BIN) * BIN
    cols = sorted(t['cot'].unique())
    err = t.groupby(['bin', 'cot'])['status'].sum(min_count=0).unstack()
    err = err.reindex(index=luoi, columns=cols).fillna(0)
    st = t[t['hoc']].groupby('cot')['duration'].agg(['mean', 'std', 'count'])
    ok = st[st['count'] >= 2]
    nguong = t['cot'].map(ok['mean'] + 3 * ok['std'])
    lat = t[t['cot'].isin(ok.index) & (t['duration'] > nguong)].groupby(['bin', 'cot']).size().unstack()
    lat = lat.reindex(index=luoi, columns=sorted(ok.index)).fillna(0)
    err.index.name = lat.index.name = 'time'
    return err, lat, {'span_http_con_nhieu_service': nhieu, 'cot_bo_lat': sorted(set(cols) - set(ok.index))}


def dung_logts(logs, luoi, sim_th=0.4, depth=4):
    """Drain riêng mỗi service (chế độ B của T-016), id toàn cục theo thứ tự xuất hiện; đếm theo timestamp."""
    from drain3 import TemplateMiner
    from drain3.template_miner_config import TemplateMinerConfig

    def miner():
        c = TemplateMinerConfig()
        c.drain_sim_th = sim_th
        c.drain_depth = depth
        c.profiling_enabled = False
        return TemplateMiner(config=c)
    t0, t_end = int(luoi[0]), int(luoi[-1]) + BIN
    lg = logs[(logs['timestamp'] >= t0) & (logs['timestamp'] < t_end)].sort_values('timestamp', kind='stable')
    tms, map_id, dem, cot = {}, {}, 0, []
    for svc, msg in zip(lg['container_name'], lg['message']):
        tm = tms.setdefault(svc, miner())
        cid = tm.add_log_message(str(msg))['cluster_id']
        if (svc, cid) not in map_id:
            dem += 1
            map_id[(svc, cid)] = dem
        cot.append(f'{svc}_{map_id[(svc, cid)]}')
    lg = lg.assign(cot=cot, bin=t0 + ((lg['timestamp'] - t0) // BIN) * BIN)
    out = lg.groupby(['bin', 'cot']).size().unstack() if len(lg) else pd.DataFrame(index=luoi)
    out = out.reindex(index=luoi).fillna(0)
    out.index.name = 'time'
    return out


def nguon_b(traces_win, logs_win, t):
    """Nguồn B cho P3: lưới 15 s gốc t-300 (40 bin); span đã lọc §5.2; ngưỡng học trên span kết thúc < t."""
    luoi = _luoi(t - 300, 40)
    st = traces_win['startTime'].astype('int64')
    hoc = (st >= (t - 300) * US) & (st + traces_win['duration'].astype('int64') < t * US)
    err, lat, info = dung_tracets(traces_win, luoi, hoc.to_numpy())
    lt = dung_logts(logs_win, luoi) if logs_win is not None else pd.DataFrame(index=pd.Index(luoi, name='time'))
    info['log_rows_cua_so'] = None if logs_win is None else int(len(logs_win))
    return lt, err, lat, info


def theo_quy_uoc_tac_gia(traces, luoi_tac_gia, cach_con='som_nhat'):
    """K-B1: lưới của file tác giả, ngưỡng μ + 3σ trên toàn file (mọi span trong phạm vi lưới)."""
    return dung_tracets(traces, np.asarray(luoi_tac_gia, dtype='int64'), np.ones(len(traces), dtype=bool), cach_con)


def so_theo_ten_cot(mine, mau):
    """So theo đúng tên cột (cột, bin). Cột chỉ có ở một bên: mọi ô tính sai. NaN bản tác giả coi là 0
    (TORAI ffill rồi điền 0; T-016 dung_logts.py:so_theo_ten)."""
    idx = mau.index
    cols = sorted(set(mine.columns) | set(mau.columns))
    m = mine.reindex(index=idx)
    trung = 0
    for c in cols:
        if c in mine.columns and c in mau.columns:
            trung += int(np.isclose(m[c].fillna(0).to_numpy(float), mau[c].fillna(0).to_numpy(float)).sum())
    return {'so_o': len(idx) * len(cols), 'o_trung': trung, 'so_cot_hop': len(cols),
            'cot_chi_ban_dung': sorted(set(mine.columns) - set(mau.columns)),
            'cot_chi_ban_tac_gia': sorted(set(mau.columns) - set(mine.columns)),
            'o_nan_ban_tac_gia': int(mau.isna().to_numpy().sum())}

"""KS-16 pha 1 (T-043, bước 4): đếm mô tả chỉ đọc, KHÔNG nhãn, trên 52 ca dev.

Đầu vào:
- RE2-TT: 30 ca qua `src/p3/selector.py` (allowlist T-022, kiểm SHA-256 từng file dữ liệu);
  mốc t lấy bằng `nhan.nap_moc` (chỉ trả mốc tiêm; chế độ (a), Q-66). Không đọc root, loại lỗi, ô.
- Nezha-OB: 22 ca qua `src/p3/nezha.py` (allowlist T-026, kiểm SHA-256); t_ns nằm trong allowlist.
- Không đọc `data/locked/`, không đọc file nào chứa nhãn ngoài mốc t.

Định nghĩa đo nằm ở hằng DINH_NGHIA bên dưới và được ghi vào file kết quả. Mỗi ca ghi tiến độ,
thời gian và RAM (RSS) vào progress.jsonl. Chạy:
  python -B results/T-043/ks16/ks16_pha1.py --run results/T-043/ks16/runs/pha1-001
"""
import argparse
import csv
import hashlib
import json
import os
import platform
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import pandas as pd
try:
    import pyarrow  # noqa: F401
except ImportError:  # như T-035: numpy/pandas của py312-pin, reader Parquet của môi trường T-014
    sys.path.append('D:/RCA-ext/envs/T-014-main/Lib/site-packages')
    import pyarrow  # noqa: F401
import pyarrow.parquet as pq
import psutil

from p3 import nezha, nhan, selector

NUA = 300
CELL = 10
US = 1_000_000
TOL_US = 1000              # dung sai 1 ms (CRISP) cho chồng lấn và vượt biên cha
M_SPAN, M_METRIC, M_COUNT = 20, 5, 10
GATE_EXACT_MAX = 100
SEV_LOI = {'ERROR', 'FATAL', 'CRITICAL'}
SEV_KHONG_LOI = {'TRACE', 'DEBUG', 'INFO', 'WARN', 'WARNING'}
KW = re.compile('|'.join(re.escape(x) for x in ('ERROR', 'FAIL', 'EXCEPTION')), re.IGNORECASE)  # SimpleRCA core.py:22
HEX32 = re.compile(r'\b[0-9a-f]{32}\b')

DINH_NGHIA = {
    'mien_che_do_a': 'span có start >= t-300 s và end < t+300 s (như cua_so.cat_span); log/metric theo mốc thời gian trong [t-300, t+300)',
    'chia_N_A': 'span thuộc A khi end >= t (SPEC B1.1); log/metric theo mốc thời gian',
    'trung_lap': 'bỏ bản lặp y hệt (mọi cột) và đếm; khóa (traceID, spanID) trùng mà nội dung khác thì đếm là ERROR',
    'cha_con': 'cha resolve khi (traceID, parentSpanID) có trong miền; parent rỗng là span gốc; còn lại là mồ côi',
    'loi_goi': 'cặp cha–con khác chủ (owner) trong miền; trước/sau mốc theo end của span phía gọi p (như T-032 bảng C)',
    'span_boc_chat': 'w có đúng một con và con đó ở thực thể khác; cha của w resolve và cùng thực thể với w',
    'span_boc_long': 'w có đúng một con ở thực thể khác (cho phép thêm con cùng thực thể); cha cùng thực thể',
    'chong_lan': 'con cắt về [s_p, e_p); con i chồng lấn nếu với anh em bắt đầu trước nó, min(e_i, max e trước) - s_i > 1 ms. Tỷ lệ quyết định Q2 = số span cha có ít nhất một cặp con chồng lấn / số span cha có >= 2 con không suy biến',
    'vuot_bien_cha': 'con có s_c < s_p - 1 ms hoặc e_c > e_p + 1 ms (chỉ chẩn đoán)',
    'thoi_gian_doc_quyen_U': 'u = d_p - |hợp các con đã cắt về cha|',
    'don_vi_thao_tac': '(chủ, tên thao tác); E1 tắt: mọi span; E1 bật: bỏ span bọc chặt. Đủ hỗ trợ khi n_N >= 20 và n_A >= 20',
    'don_vi_canh': 'cạnh a->b của span bọc chặt; mẫu g = u(w); đủ hỗ trợ khi n_N >= 20 và n_A >= 20',
    'don_vi_metric': 'mỗi cột metric; đủ hỗ trợ khi số giá trị hữu hạn ở N và A đều >= 5',
    'don_vi_dem': 'log theo thực thể và tần suất theo thao tác; đủ khi tổng n_N + n_A >= 10',
    'che_do_cong': 'đơn vị phân vị đủ hỗ trợ: n_N + n_A <= 100 thì chính xác, > 100 thì xấp xỉ (SPEC B1.3)',
    'dong_loi_log': 'Nezha-OB: severity trong JSON lồng của Log (hợp đồng T-042 continuation-001), strip + upper; {ERROR,FATAL,CRITICAL} là lỗi; {TRACE,DEBUG,INFO,WARN,WARNING} không lỗi; còn lại UNKNOWN. RE2-TT: từ khóa SimpleRCA ERROR|FAIL|EXCEPTION, không phân biệt hoa thường',
    'khoang_ghi_file_F': 'trace: [min end, max end] của mọi span trong file nguồn của ca (Nezha: hợp ba file phút, kiểm khe > 10 s); log: [min, max] mốc thời gian; metric: [min, max] cột thời gian',
    'do_phan_giai_moc': 'mỗi bản ghi tại x phủ [x, x + r): r = 1 s cho log và metric RE2-TT (mốc giây nguyên), 1 µs cho span RE2-TT, 1 ns cho Nezha-OB',
    'bao_ban_ghi_H': 'luật chính: H = [min x, max x + r) của bản ghi nguồn (mọi thực thể gộp) trong cả cửa sổ đang xét [t-300, t+300) (mốc giả: [t-600, t)). Biến thể báo kèm: H tính riêng từng phía N, A (lượt thử nhanh cho thấy biến thể này biến giây cuối mỗi phía thành OPEN giả khi mốc là giây nguyên)',
    'trang_thai_o': 'ô 10 s: hoàn toàn ngoài F -> XAC_NHAN_THIEU_THU; hoàn toàn trong F ∩ H -> QUAN_SAT_A0; hoàn toàn trong F, ngoài H -> OPEN; còn lại -> O_BIEN (ghi số giây từng loại). XAC_NHAN_CO_QUAN_SAT = 0 vì dev không có siêu dữ liệu collector',
    'T_quan_sat': 'T_chac = |F ∩ H ∩ phía| (giây, liên tục); T_max = |F ∩ phía|. P: (chac_N, chac_A); S_lo: (max_N, chac_A); S_hi: (chac_N, max_A). Biến thể H theo phía báo ở T_bien_the_H_theo_phia',
    'moc_gia': "chỉ RE2-TT: t' = t - 300; miền [t-600, t); N' = [t-600, t-300), A' = [t-300, t)",
    'noi_log_span': 'Nezha-OB: dòng log trong miền có TraceID và SpanID; khớp theo (TraceID, SpanID) với span của miền; lệch thời gian khi mốc log ngoài [s - 1 s, e + 1 s]; báo thêm khớp chỉ theo SpanID',
}


def now():
    return datetime.now(timezone.utc).isoformat()


def json_mac_dinh(x):
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        return float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, (np.ndarray, tuple)):
        return list(x)
    raise TypeError(f'không ghi được {type(x)}')


def rss():
    return psutil.Process().memory_info().rss


def sha_file(p):
    return selector.sha256_file(p)


# ---------------------------------------------------------------- span

def chuan_hoa_span(tid, sid, pid, owner, op, s_us, e_us):
    df = pd.DataFrame({'tid': tid, 'sid': sid, 'pid': pid, 'owner': owner, 'op': op,
                       's': np.asarray(s_us, dtype=np.int64), 'e': np.asarray(e_us, dtype=np.int64)})
    df['pid'] = df['pid'].fillna('').astype(str)
    n0 = len(df)
    dup_same = int(df.duplicated(keep='first').sum())
    df = df.drop_duplicates(keep='first').reset_index(drop=True)
    key_dup = df.duplicated(['tid', 'sid'], keep=False)
    n_key_conflict = int(key_dup.sum())
    if n_key_conflict:
        df = df.loc[~key_dup].reset_index(drop=True)
    return df, {'rows_in': n0, 'identical_dropped': dup_same, 'key_conflict_rows_removed': n_key_conflict}


def cau_truc(df, t_us):
    """Cha–con, lời gọi, span bọc, chồng lấn, thời gian độc quyền, độ sâu. df đã bỏ trùng."""
    n = len(df)
    keys = (df['tid'] + ':' + df['sid']).to_numpy()
    pkeys = (df['tid'] + ':' + df['pid']).to_numpy()
    idx = pd.Index(keys)
    par = idx.get_indexer(pkeys)
    empty_parent = (df['pid'].to_numpy() == '') | (df['pid'].to_numpy() == '0')
    par = np.where(empty_parent, -1, par)
    orphan = (~empty_parent) & (par < 0)
    own = df['owner'].astype('category')
    oc = own.cat.codes.to_numpy()
    names = list(own.cat.categories)
    s = df['s'].to_numpy()
    e = df['e'].to_numpy()
    d = e - s
    side_A = e >= t_us
    has_par = par >= 0
    ci = np.nonzero(has_par)[0]
    pi = par[ci]
    cross = oc[ci] != oc[pi]
    n_child = np.bincount(pi, minlength=n)
    n_child_other = np.bincount(pi[cross], minlength=n)
    parent_same = np.zeros(n, bool)
    parent_same[ci] = ~cross
    wrap_strict = (n_child == 1) & (n_child_other == 1) & parent_same
    wrap_loose = (n_child_other == 1) & parent_same
    # con cắt về cha
    cs = np.maximum(s[ci], s[pi])
    ce = np.minimum(e[ci], e[pi])
    beyond = (s[ci] < s[pi] - TOL_US) | (e[ci] > e[pi] + TOL_US)
    valid = ce > cs
    cdf = pd.DataFrame({'p': pi[valid], 'cs': cs[valid], 'ce': ce[valid]}).sort_values(['p', 'cs'], kind='mergesort')
    g = cdf.groupby('p', sort=False)['ce']
    prev = g.cummax().groupby(cdf['p'], sort=False).shift(1)
    prevv = prev.to_numpy(dtype=float)
    csv_ = cdf['cs'].to_numpy(dtype=float)
    cev = cdf['ce'].to_numpy(dtype=float)
    ov = np.where(np.isnan(prevv), -np.inf, np.minimum(cev, prevv) - csv_)
    child_ov = ov > TOL_US
    contrib = np.maximum(0.0, cev - np.where(np.isnan(prevv), csv_, np.maximum(csv_, prevv)))
    union = np.bincount(cdf['p'].to_numpy(), weights=contrib, minlength=n)
    u = d - union
    n_valid_child = np.bincount(cdf['p'].to_numpy(), minlength=n)
    parent_ov = np.bincount(cdf['p'].to_numpy()[child_ov], minlength=n) > 0
    # độ sâu
    depth = np.zeros(n, np.int64)
    sdepth = np.zeros(n, np.int64)
    for _ in range(256):
        nd = np.where(has_par, depth[np.maximum(par, 0)] + 1, 0)
        ns = np.where(has_par, sdepth[np.maximum(par, 0)] + (oc != oc[np.maximum(par, 0)]), 0)
        if np.array_equal(nd, depth) and np.array_equal(ns, sdepth):
            break
        depth, sdepth = nd, ns
    return {
        'par': par, 'oc': oc, 'names': names, 's': s, 'e': e, 'd': d, 'u': u, 'side_A': side_A,
        'ci': ci, 'pi': pi, 'cross': cross, 'wrap_strict': wrap_strict, 'wrap_loose': wrap_loose,
        'orphan': orphan, 'empty_parent': empty_parent, 'beyond': beyond,
        'n_valid_child': n_valid_child, 'parent_ov': parent_ov, 'child_ov_n': int(child_ov.sum()),
        'depth': depth, 'sdepth': sdepth,
    }


def tom_tat_cau_truc(df, c, t_us):
    n = len(df)
    par, oc, side_A = c['par'], c['oc'], c['side_A']
    ci, pi, cross = c['ci'], c['pi'], c['cross']
    multi = c['n_valid_child'] >= 2
    out = {
        'n_spans': n, 'n_N': int((~side_A).sum()), 'n_A': int(side_A.sum()),
        'root_spans': int(c['empty_parent'].sum()), 'parent_resolved': int((par >= 0).sum()),
        'orphans': int(c['orphan'].sum()),
        'orphans_N': int((c['orphan'] & ~side_A).sum()), 'orphans_A': int((c['orphan'] & side_A).sum()),
        'children': int(len(ci)), 'cross_entity_children': int(cross.sum()),
        'wrap_strict': int(c['wrap_strict'].sum()), 'wrap_loose': int(c['wrap_loose'].sum()),
        'parents_with_child': int((c['n_valid_child'] >= 1).sum()),
        'parents_with_ge2_children': int(multi.sum()),
        'parents_with_overlap': int((c['parent_ov'] & multi).sum()),
        'children_overlapping_earlier_sibling': c['child_ov_n'],
        'children_beyond_parent_1ms': int(c['beyond'].sum()),
        'max_depth': int(c['depth'].max()) if n else 0,
        'max_service_depth': int(c['sdepth'].max()) if n else 0,
        'service_depth_hist': {str(k): int(v) for k, v in zip(*np.unique(c['sdepth'], return_counts=True))},
    }
    out['overlap_share_parents_ge2'] = (out['parents_with_overlap'] / out['parents_with_ge2_children']
                                        if out['parents_with_ge2_children'] else None)
    out['overlap_share_parents_with_child'] = (out['parents_with_overlap'] / out['parents_with_child']
                                               if out['parents_with_child'] else None)
    # lời gọi khác chủ (để đối chiếu T-032 sau barrier)
    s, e, d = c['s'], c['e'], c['d']
    p_, c_ = pi[cross], ci[cross]
    before = e[p_] < t_us
    pre = s[c_] - s[p_]
    post = e[p_] - e[c_]
    gap = d[p_] - d[c_]
    calls = {}
    for nm, m in (('before', before), ('after', ~before)):
        k = int(m.sum())
        calls[nm] = {'n': k,
                     'nested_share': float(((pre[m] >= 0) & (post[m] >= 0)).mean()) if k else None,
                     'pre_negative_share': float((pre[m] < 0).mean()) if k else None,
                     'post_negative_share': float((post[m] < 0).mean()) if k else None,
                     'gap_negative_share': float((gap[m] < 0).mean()) if k else None,
                     'median_d_p_us': float(np.median(d[p_][m])) if k else None,
                     'median_d_c_us': float(np.median(d[c_][m])) if k else None,
                     'median_gap_us': float(np.median(gap[m])) if k else None}
    out['all_calls'] = calls
    return out


def don_vi_span(df, c):
    names = c['names']
    oc, side_A, d, u = c['oc'], c['side_A'], c['d'], c['u']
    ws = c['wrap_strict']
    ops = df['op'].to_numpy()
    rows = []
    t = pd.DataFrame({'o': oc, 'op': ops, 'A': side_A, 'd': d, 'u': u, 'w': ws})
    for (o, op), g in t.groupby(['o', 'op'], sort=True):
        gN, gA = g[~g['A']], g[g['A']]
        nwN, nwA = gN[~gN['w']], gA[~gA['w']]
        rows.append([names[o], op, len(gN), len(gA), len(nwN), len(nwA),
                     float(gN['d'].median()) if len(gN) else None, float(gA['d'].median()) if len(gA) else None,
                     float(nwN['u'].median()) if len(nwN) else None, float(nwA['u'].median()) if len(nwA) else None])
    # cạnh qua span bọc chặt; và mọi lời gọi khác chủ theo cạnh
    ci, pi, cross = c['ci'], c['pi'], c['cross']
    wmask = ws[pi] & cross
    w_, ch_ = pi[wmask], ci[wmask]
    e_rows = []
    et = pd.DataFrame({'a': oc[w_], 'b': oc[ch_], 'A': side_A[w_], 'g': u[w_], 'dc': d[ch_]})
    for (a, b), g in et.groupby(['a', 'b'], sort=True):
        gN, gA = g[~g['A']], g[g['A']]
        e_rows.append([names[a], names[b], len(gN), len(gA),
                       float(gN['g'].median()) if len(gN) else None, float(gA['g'].median()) if len(gA) else None,
                       float(gN['dc'].median()) if len(gN) else None, float(gA['dc'].median()) if len(gA) else None])
    p_, c_ = pi[cross], ci[cross]
    ct = pd.DataFrame({'a': oc[p_], 'b': oc[c_], 'A': side_A[p_], 'gap': d[p_] - d[c_], 'dc': d[c_]})
    call_rows = []
    for (a, b), g in ct.groupby(['a', 'b'], sort=True):
        gN, gA = g[~g['A']], g[g['A']]
        call_rows.append([names[a], names[b], len(gN), len(gA),
                          float(gN['dc'].median()) if len(gN) else None, float(gA['dc'].median()) if len(gA) else None,
                          float(gN['gap'].median()) if len(gN) else None, float(gA['gap'].median()) if len(gA) else None])
    return rows, e_rows, call_rows


def tom_tat_don_vi(op_rows, edge_rows):
    def mode(nN, nA):
        return 'exact' if nN + nA <= GATE_EXACT_MAX else 'asymptotic'
    out = {'ops': len(op_rows), 'edges_wrapped': len(edge_rows)}
    for lab, iN, iA in (('op_E1_tat', 2, 3), ('op_E1_bat', 4, 5)):
        ok = [r for r in op_rows if r[iN] >= M_SPAN and r[iA] >= M_SPAN]
        out[lab] = {'du_ho_tro': len(ok), 'thieu': len(op_rows) - len(ok),
                    'exact': sum(mode(r[iN], r[iA]) == 'exact' for r in ok),
                    'asymptotic': sum(mode(r[iN], r[iA]) == 'asymptotic' for r in ok)}
    ok = [r for r in edge_rows if r[2] >= M_SPAN and r[3] >= M_SPAN]
    out['canh_E2'] = {'du_ho_tro': len(ok), 'thieu': len(edge_rows) - len(ok),
                      'exact': sum(mode(r[2], r[3]) == 'exact' for r in ok),
                      'asymptotic': sum(mode(r[2], r[3]) == 'asymptotic' for r in ok)}
    freq_ok = [r for r in op_rows if r[2] + r[3] >= M_COUNT]
    out['tan_suat_E3b'] = {'du_tong_10': len(freq_ok), 'NEW_OP': sum(r[2] == 0 and r[3] > 0 for r in op_rows),
                           'STOPPED': sum(r[2] > 0 and r[3] == 0 for r in op_rows)}
    return out


# ---------------------------------------------------------------- quan sát

def do_dai(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def quan_sat(times_s, F, lo, t, hi, r=0.0):
    """times_s: mốc bản ghi (giây, float) của nguồn trong file; F = (f0, f1) đã đệm r, hoặc None.

    Luật chính: H trên cả cửa sổ [lo, hi). Biến thể: H theo từng phía (chỉ báo T).
    """
    res = {'F_rel_t': None if F is None else [F[0] - t, F[1] - t], 'r': r}
    sides = {'N': (lo, t), 'A': (t, hi)}
    Hside, Hwhole = {}, None
    win = times_s[(times_s >= lo) & (times_s < hi)]
    if len(win):
        Hwhole = (float(win.min()), float(win.max()) + r)
    for k, (a, b) in sides.items():
        x = times_s[(times_s >= a) & (times_s < b)]
        Hside[k] = (float(x.min()), float(x.max()) + r) if len(x) else None
    H = {k: Hwhole for k in sides}
    res['H_rel_t'] = None if Hwhole is None else [Hwhole[0] - t, Hwhole[1] - t]
    res['H_theo_phia_rel_t'] = {k: (None if v is None else [v[0] - t, v[1] - t]) for k, v in Hside.items()}

    def tinh_T(Hd):
        T = {}
        for k, (a, b) in sides.items():
            tmax = 0.0 if F is None else do_dai(F[0], F[1], a, b)
            tch = 0.0 if (F is None or Hd[k] is None) else do_dai(max(F[0], Hd[k][0]), min(F[1], Hd[k][1]), a, b)
            T[k] = {'chac': tch, 'max': tmax}
        return T
    T = tinh_T(H)
    res['T'] = T
    res['T_bien_the_H_theo_phia'] = tinh_T(Hside)
    res['worlds'] = {'P': [T['N']['chac'], T['A']['chac']], 'S_lo': [T['N']['max'], T['A']['chac']],
                     'S_hi': [T['N']['chac'], T['A']['max']]}
    # ô 10 s
    counts = {k: {'XAC_NHAN_CO_QUAN_SAT': 0, 'QUAN_SAT_A0': 0, 'OPEN': 0, 'XAC_NHAN_THIEU_THU': 0, 'O_BIEN': 0}
              for k in sides}
    bien, open_rec = [], 0
    hist = np.histogram(win, bins=np.arange(lo, hi + CELL, CELL))[0] if len(win) else np.zeros((hi - lo) // CELL, int)
    states = []
    for i, c0 in enumerate(range(lo, hi, CELL)):
        c1 = c0 + CELL
        k = 'N' if c0 < t else 'A'
        inF = 0.0 if F is None else do_dai(F[0], F[1], c0, c1)
        h = H[k]
        inFH = 0.0 if (F is None or h is None) else do_dai(max(F[0], h[0]), min(F[1], h[1]), c0, c1)
        if inF == 0:
            st = 'XAC_NHAN_THIEU_THU'
        elif inFH == CELL:
            st = 'QUAN_SAT_A0'
        elif inF == CELL and inFH == 0:
            st = 'OPEN'
            if hist[i] > 0:
                open_rec += 1
        else:
            st = 'O_BIEN'
            bien.append({'o': c0 - t, 'giay_A0': inFH, 'giay_open': inF - inFH, 'giay_thieu': CELL - inF,
                         'ban_ghi': int(hist[i])})
        counts[k][st] += 1
        states.append(st)
    res['o'] = counts
    res['o_bien'] = bien
    res['o_open_co_ban_ghi_cung_nguon'] = open_rec
    res['trang_thai_o'] = states
    return res


def F_tu_khoi(ranges, khe_s=10):
    """ranges: [(min, max)] theo file; hợp nếu liên tục (khe <= khe_s); trả F và danh sách khe."""
    if not ranges:
        return None, []
    r = sorted(ranges)
    khe = []
    a, b = r[0]
    for x, y in r[1:]:
        if x - b > khe_s:
            khe.append([b, x])
        b = max(b, y)
    return (a, b), khe


# ---------------------------------------------------------------- RE2-TT

def ca_re2(allow, moc, oid):
    t0 = time.time()
    files = selector.chon_ca(allow, oid, ROOT)
    t = int(moc[oid])
    lo, hi = t - NUA, t + NUA
    out = {'dataset': 'RE2-TT', 'opaque_id': oid, 't': t,
           'files': {k: {'sha256': allow[oid]['files'][k]['sha256']} for k in files}}
    cols = ['traceID', 'spanID', 'parentSpanID', 'serviceName', 'operationName', 'startTime', 'duration']
    tr = pq.read_table(files['traces.parquet'], columns=cols).to_pandas()
    full_rows = len(tr)
    st = tr['startTime'].to_numpy(np.int64)
    en = st + tr['duration'].to_numpy(np.int64)
    # đối chiếu T-035 K3 trên toàn bảng: tham chiếu cha resolve
    kk = pd.Index(tr['traceID'] + ':' + tr['spanID']).unique()
    pp = tr['parentSpanID'].fillna('')
    nonempty = (pp != '').to_numpy()
    resolved_full = int((kk.get_indexer((tr['traceID'] + ':' + pp)[nonempty]) >= 0).sum())
    out['full_table'] = {'rows': full_rows, 'parent_nonempty': int(nonempty.sum()), 'parent_resolved_any': resolved_full}
    F_tr = (float(en.min()) / US, float(en.max()) / US + 1e-6)
    keep = (st >= lo * US) & (en < hi * US)
    df, dd = chuan_hoa_span(tr['traceID'][keep], tr['spanID'][keep], tr['parentSpanID'][keep],
                            tr['serviceName'][keep], tr['operationName'][keep], st[keep], en[keep])
    out['dedupe'] = dd
    c = cau_truc(df, t * US)
    out['trace'] = tom_tat_cau_truc(df, c, t * US)
    op_rows, edge_rows, call_rows = don_vi_span(df, c)
    out['units'] = tom_tat_don_vi(op_rows, edge_rows)
    out['op_rows'] = op_rows
    out['edge_rows'] = edge_rows
    out['call_rows'] = call_rows
    ent = {}
    for nm, k in zip(c['names'], range(len(c['names']))):
        m = c['oc'] == k
        ent[nm] = {'spans_N': int((m & ~c['side_A']).sum()), 'spans_A': int((m & c['side_A']).sum())}
    # mốc giả: miền [t-600, t)
    keep2 = (st >= (t - 2 * NUA) * US) & (en < t * US)
    df2, dd2 = chuan_hoa_span(tr['traceID'][keep2], tr['spanID'][keep2], tr['parentSpanID'][keep2],
                              tr['serviceName'][keep2], tr['operationName'][keep2], st[keep2], en[keep2])
    c2 = cau_truc(df2, (t - NUA) * US)
    op2, edge2, _ = don_vi_span(df2, c2)
    out['moc_gia'] = {'dedupe': dd2, 'n_spans': len(df2), 'n_N': int((~c2['side_A']).sum()),
                      'n_A': int(c2['side_A'].sum()), 'units': tom_tat_don_vi(op2, edge2)}
    end_s = en.astype(float) / US
    del tr, st, en, df, c, df2, c2
    # metric
    mt = pq.read_table(files['metrics.parquet']).to_pandas()
    tm = pd.to_numeric(mt['time']).to_numpy(np.int64)
    F_m = (float(tm.min()), float(tm.max()) + 1.0)
    win = (tm >= lo) & (tm < hi)
    mN, mA = win & (tm < t), win & (tm >= t)
    metr = []
    for col in mt.columns:
        if col == 'time':
            continue
        v = pd.to_numeric(mt[col], errors='coerce').to_numpy(float)
        metr.append([col, int(np.isfinite(v[mN]).sum()), int(np.isfinite(v[mA]).sum())])
    w2 = (tm >= t - 2 * NUA) & (tm < t)
    out['moc_gia']['metric_rows_N'] = int((w2 & (tm < t - NUA)).sum())
    out['moc_gia']['metric_rows_A'] = int((w2 & (tm >= t - NUA)).sum())
    out['metric'] = {'cot': len(metr), 'rows_N': int(mN.sum()), 'rows_A': int(mA.sum()),
                     'du_ho_tro': sum(r[1] >= M_METRIC and r[2] >= M_METRIC for r in metr),
                     'exact': sum(r[1] >= M_METRIC and r[2] >= M_METRIC and r[1] + r[2] <= GATE_EXACT_MAX for r in metr),
                     'asymptotic': sum(r[1] >= M_METRIC and r[2] >= M_METRIC and r[1] + r[2] > GATE_EXACT_MAX for r in metr)}
    out['metric_rows'] = metr
    metric_s = tm.astype(float)
    del mt
    # log
    if 'logs.parquet' in files:
        lg = pq.read_table(files['logs.parquet']).to_pandas()
        out['log_columns'] = list(lg.columns)
        ts = pd.to_numeric(lg['timestamp']).to_numpy(np.int64)
        F_l = (float(ts.min()), float(ts.max()) + 1.0)
        win = (ts >= lo) & (ts < hi)
        sub = lg.loc[win]
        sA = ts[win] >= t
        isloi = sub['message'].astype(str).map(lambda x: bool(KW.search(x))).to_numpy()
        hexid = sub['message'].astype(str).map(lambda x: bool(HEX32.search(x))).to_numpy()
        lrows = []
        for nm, g in pd.DataFrame({'c': sub['container_name'].to_numpy(), 'A': sA, 'l': isloi}).groupby('c'):
            lrows.append([nm, int((~g['A']).sum()), int(g['A'].sum()), int((g['l'] & ~g['A']).sum()), int((g['l'] & g['A']).sum())])
            ent.setdefault(nm, {})['log_N'] = int((~g['A']).sum())
            ent[nm]['log_A'] = int(g['A'].sum())
        out['log'] = {'rows_N': int((~sA).sum()), 'rows_A': int(sA.sum()), 'error_rows_N': int((isloi & ~sA).sum()),
                      'error_rows_A': int((isloi & sA).sum()), 'id_columns': False,
                      'messages_with_hex32': int(hexid.sum()),
                      'don_vi_dem_log_loi_du_10': sum(r[3] + r[4] >= M_COUNT for r in lrows),
                      'don_vi_dem_log_tong_du_10': sum(r[1] + r[2] >= M_COUNT for r in lrows)}
        out['log_rows'] = lrows
        w2 = (ts >= t - 2 * NUA) & (ts < t)
        out['moc_gia']['log_rows_N'] = int((w2 & (ts < t - NUA)).sum())
        out['moc_gia']['log_rows_A'] = int((w2 & (ts >= t - NUA)).sum())
        log_s = ts.astype(float)
        del lg
    else:
        F_l, log_s = None, np.array([], float)
        out['log'] = {'khong_co_file': True}
    out['entities'] = ent
    out['quan_sat'] = {'trace': quan_sat(end_s, F_tr, lo, t, hi, 1e-6), 'log': quan_sat(log_s, F_l, lo, t, hi, 1.0),
                       'metric': quan_sat(metric_s, F_m, lo, t, hi, 1.0)}
    out['quan_sat_moc_gia'] = {'trace': quan_sat(end_s, F_tr, t - 2 * NUA, t - NUA, t, 1e-6),
                               'log': quan_sat(log_s, F_l, t - 2 * NUA, t - NUA, t, 1.0),
                               'metric': quan_sat(metric_s, F_m, t - 2 * NUA, t - NUA, t, 1.0)}
    # ô OPEN có bản ghi của nguồn khác
    out['o_open_co_ban_ghi_nguon_khac'] = mo_khac(out['quan_sat'], {'trace': end_s, 'log': log_s, 'metric': metric_s}, lo, hi)
    out['cost'] = {'giay': round(time.time() - t0, 2), 'rss_bytes': rss()}
    return out


def mo_khac(qs, times, lo, hi):
    res = {}
    for src, q in qs.items():
        n = 0
        for i, st in enumerate(q['trang_thai_o']):
            if st != 'OPEN':
                continue
            c0, c1 = lo + i * CELL, lo + (i + 1) * CELL
            if any(((x >= c0) & (x < c1)).any() for k, x in times.items() if k != src):
                n += 1
        res[src] = n
    return res


# ---------------------------------------------------------------- Nezha-OB

def doc_csv_cot(path, cols, lo=None, hi=None, tcol=None):
    csv.field_size_limit(10_000_000)
    rows = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        for row in r:
            if tcol is not None:
                x = int(row[tcol])
                if lo is not None and not (lo <= x < hi):
                    continue
            rows.append([row[c] for c in cols])
    return rows


def severity(log_field):
    try:
        outer = json.loads(log_field)
        inner = json.loads(outer['log'])
        v = inner.get('severity') if isinstance(inner, dict) else None
    except Exception:
        return 'UNKNOWN'
    if not isinstance(v, str):
        return 'UNKNOWN'
    v = v.strip().upper()
    if v in SEV_LOI:
        return 'LOI'
    if v in SEV_KHONG_LOI:
        return 'KHONG_LOI'
    return 'UNKNOWN'


def ca_nezha(allow, oid):
    t0 = time.time()
    sel = nezha.chon_ca(allow, oid, ROOT)
    t_ns = sel['t_ns']
    t = t_ns // nezha.NS
    lo, hi = t - NUA, t + NUA
    win = nezha.doc_cua_so(sel)
    out = {'dataset': 'Nezha-OB', 'opaque_id': oid, 't': int(t), 'files': {k: {'sha256': v['sha256']} for k, v in sel['files'].items()},
           'adapter_window': win['window'],
           'adapter_span_rows': int(len(win['spans'])),
           'adapter_span_duplicate_rows': win['provenance']['span_duplicate_rows']}
    sp = win['spans']
    df, dd = chuan_hoa_span(sp['traceID'], sp['spanID'], sp['parentSpanID'], sp['serviceName'], sp['operationName'],
                            sp['startTime'].to_numpy(np.int64), (sp['startTime'] + sp['duration']).to_numpy(np.int64))
    out['dedupe'] = dd
    out['parent_id_values_empty'] = int((sp['parentSpanID'].fillna('') == '').sum())
    c = cau_truc(df, t * US)
    out['trace'] = tom_tat_cau_truc(df, c, t * US)
    op_rows, edge_rows, call_rows = don_vi_span(df, c)
    out['units'] = tom_tat_don_vi(op_rows, edge_rows)
    out['op_rows'] = op_rows
    out['edge_rows'] = edge_rows
    out['call_rows'] = call_rows
    ent = {}
    for k, nm in enumerate(c['names']):
        m = c['oc'] == k
        ent[nm] = {'spans_N': int((m & ~c['side_A']).sum()), 'spans_A': int((m & c['side_A']).sum())}
    span_key = pd.Series(np.arange(len(df)), index=pd.Index(df['tid'] + ':' + df['sid']))
    sid_count = df['sid'].value_counts()
    s_arr, e_arr = df['s'].to_numpy(), df['e'].to_numpy()
    # F của trace/log: hợp các file phút, đọc toàn file (không chỉ miền)
    ranges = {'trace': [], 'log': []}
    rec_times = {'trace': [], 'log': []}
    join = {'per_file': [], 'tong': {}}
    lrows = {}
    tot = {'lines': 0, 'with_ids': 0, 'match_one': 0, 'no_match': 0, 'match_time_off': 0,
           'match_by_spanid_only_multi': 0, 'N': {}, 'A': {}}
    for side in ('N', 'A'):
        tot[side] = {'lines': 0, 'with_ids': 0, 'match_one': 0, 'no_match': 0, 'match_time_off': 0}
    for rel, meta in sorted(sel['files'].items()):
        kind = Path(rel).parent.name
        if kind == 'trace':
            rr = doc_csv_cot(meta['absolute_path'], ['EndTimeUnixNano'])
            x = np.array([int(r[0]) for r in rr], dtype=np.int64) / 1e9
            ranges['trace'].append((float(x.min()), float(x.max())))
            rec_times['trace'].append(x)
        elif kind == 'log':
            rr = doc_csv_cot(meta['absolute_path'], ['TimeUnixNano', 'PodName', 'TraceID', 'SpanID', 'Log'])
            x = np.array([int(r[0]) for r in rr], dtype=np.int64)
            ranges['log'].append((float(x.min()) / 1e9, float(x.max()) / 1e9))
            rec_times['log'].append(x / 1e9)
            pf = {'file': rel, 'lines': 0, 'with_ids': 0, 'match_one': 0, 'no_match': 0, 'match_time_off': 0}
            for (ts, pod, tid, sid, logf) in rr:
                ts = int(ts)
                if not (lo * nezha.NS <= ts < hi * nezha.NS):
                    continue
                side = 'N' if ts < t_ns else 'A'
                ent_name = nezha.POD_ALIASES.get(pod, pod)
                sev = severity(logf)
                lr = lrows.setdefault(ent_name, {'N': [0, 0, 0, 0], 'A': [0, 0, 0, 0]})  # dòng, xác định, lỗi, UNKNOWN
                lr[side][0] += 1
                lr[side][1] += sev != 'UNKNOWN'
                lr[side][2] += sev == 'LOI'
                lr[side][3] += sev == 'UNKNOWN'
                pf['lines'] += 1
                tot[side]['lines'] += 1
                if tid and sid:
                    pf['with_ids'] += 1
                    tot[side]['with_ids'] += 1
                    j = span_key.get(tid + ':' + sid)
                    if j is None:
                        pf['no_match'] += 1
                        tot[side]['no_match'] += 1
                        if sid_count.get(sid, 0) > 1:
                            tot['match_by_spanid_only_multi'] += 1
                    else:
                        tus = ts / 1000
                        if s_arr[j] - US <= tus <= e_arr[j] + US:
                            pf['match_one'] += 1
                            tot[side]['match_one'] += 1
                        else:
                            pf['match_time_off'] += 1
                            tot[side]['match_time_off'] += 1
            join['per_file'].append(pf)
    for k in ('lines', 'with_ids', 'match_one', 'no_match', 'match_time_off'):
        tot[k] = tot['N'][k] + tot['A'][k]
    join['tong'] = tot
    out['log_span_join'] = join
    out['log_rows'] = [[k, v['N'][0], v['A'][0], v['N'][2], v['A'][2], v['N'][1], v['A'][1], v['N'][3], v['A'][3]]
                       for k, v in sorted(lrows.items())]
    for k, v in lrows.items():
        ent.setdefault(k, {})['log_N'] = v['N'][0]
        ent[k]['log_A'] = v['A'][0]
    out['log'] = {'rows_N': sum(v['N'][0] for v in lrows.values()), 'rows_A': sum(v['A'][0] for v in lrows.values()),
                  'error_rows_N': sum(v['N'][2] for v in lrows.values()), 'error_rows_A': sum(v['A'][2] for v in lrows.values()),
                  'unknown_rows_N': sum(v['N'][3] for v in lrows.values()), 'unknown_rows_A': sum(v['A'][3] for v in lrows.values()),
                  'id_columns': True,
                  'don_vi_dem_log_loi_du_10': sum(v['N'][2] + v['A'][2] >= M_COUNT for v in lrows.values()),
                  'thuc_the_N_co_log_khong_xac_dinh': sorted(k for k, v in lrows.items() if v['N'][0] > 0 and v['N'][1] == 0),
                  'thuc_the_A_co_log_khong_xac_dinh': sorted(k for k, v in lrows.items() if v['A'][0] > 0 and v['A'][1] == 0)}
    F_tr, khe_tr = F_tu_khoi(ranges['trace'])
    F_l, khe_l = F_tu_khoi(ranges['log'])
    out['file_ranges'] = {'trace': [[a - t, b - t] for a, b in ranges['trace']], 'log': [[a - t, b - t] for a, b in ranges['log']],
                          'khe_trace': khe_tr, 'khe_log': khe_l}
    tr_s = np.concatenate(rec_times['trace']) if rec_times['trace'] else np.array([], float)
    lg_s = np.concatenate(rec_times['log']) if rec_times['log'] else np.array([], float)
    # metric: mốc thời gian theo marker front_service (5 N + 5 A); F theo từng file metric (toàn file)
    metr = []
    for name, arr in win['metric_arrays'].items():
        metr.append([name, int(np.isfinite(arr['normal']).sum()), int(np.isfinite(arr['anomalous']).sum())])
    out['metric'] = {'cot': len(metr), 'rows_N': 5, 'rows_A': 5,
                     'du_ho_tro': sum(r[1] >= M_METRIC and r[2] >= M_METRIC for r in metr),
                     'exact': sum(r[1] >= M_METRIC and r[2] >= M_METRIC for r in metr), 'asymptotic': 0}
    out['metric_rows'] = metr
    mranges = []
    for rel, meta in sorted(sel['files'].items()):
        if Path(rel).parent.name != 'metric':
            continue
        rr = doc_csv_cot(meta['absolute_path'], ['Time'])
        x = np.array([nezha.parse_time_ns(r[0]) for r in rr], dtype=np.int64) / 1e9
        mranges.append((float(x.min()), float(x.max())))
    F_m = (max(a for a, _ in mranges), min(b for _, b in mranges)) if mranges else None
    marker = np.asarray(win['metric']['time'].to_numpy(np.int64), float) / 1e9
    out['entities'] = ent
    out['quan_sat'] = {'trace': quan_sat(tr_s, F_tr, lo, t, hi), 'log': quan_sat(lg_s, F_l, lo, t, hi),
                       'metric': quan_sat(marker, F_m, lo, t, hi)}
    out['o_open_co_ban_ghi_nguon_khac'] = mo_khac(out['quan_sat'], {'trace': tr_s, 'log': lg_s, 'metric': marker}, lo, hi)
    out['cost'] = {'giay': round(time.time() - t0, 2), 'rss_bytes': rss()}
    return out


# ---------------------------------------------------------------- tổng hợp

def tong_hop(cases):
    agg = {}
    for ds in ('RE2-TT', 'Nezha-OB'):
        cs = [c for c in cases if c.get('dataset') == ds and 'trace' in c]
        if not cs:
            continue
        a = {'so_ca': len(cs)}
        sumk = lambda k: sum(c['trace'][k] for c in cs)  # noqa: E731
        for k in ('n_spans', 'n_N', 'n_A', 'orphans', 'children', 'cross_entity_children', 'wrap_strict', 'wrap_loose',
                  'parents_with_child', 'parents_with_ge2_children', 'parents_with_overlap',
                  'children_overlapping_earlier_sibling', 'children_beyond_parent_1ms'):
            a[k] = sumk(k)
        a['overlap_share_parents_ge2'] = a['parents_with_overlap'] / a['parents_with_ge2_children'] if a['parents_with_ge2_children'] else None
        a['overlap_share_parents_with_child'] = a['parents_with_overlap'] / a['parents_with_child'] if a['parents_with_child'] else None
        a['max_service_depth'] = max(c['trace']['max_service_depth'] for c in cs)
        for k in ('op_E1_tat', 'op_E1_bat', 'canh_E2'):
            a[k] = {kk: sum(c['units'][k][kk] for c in cs) for kk in ('du_ho_tro', 'thieu', 'exact', 'asymptotic')}
        a['tan_suat_E3b'] = {kk: sum(c['units']['tan_suat_E3b'][kk] for c in cs) for kk in ('du_tong_10', 'NEW_OP', 'STOPPED')}
        a['metric'] = {kk: sum(c['metric'][kk] for c in cs) for kk in ('cot', 'du_ho_tro', 'exact', 'asymptotic')}
        qs = {}
        for src in ('trace', 'log', 'metric'):
            st = {}
            for side in ('N', 'A'):
                st[side] = {k: sum(c['quan_sat'][src]['o'][side][k] for c in cs)
                            for k in ('XAC_NHAN_CO_QUAN_SAT', 'QUAN_SAT_A0', 'OPEN', 'XAC_NHAN_THIEU_THU', 'O_BIEN')}
            T = {side: {'chac_min': min(c['quan_sat'][src]['T'][side]['chac'] for c in cs),
                        'chac_max': max(c['quan_sat'][src]['T'][side]['chac'] for c in cs),
                        'max_min': min(c['quan_sat'][src]['T'][side]['max'] for c in cs)} for side in ('N', 'A')}
            qs[src] = {'o': st, 'T': T,
                       'o_open_co_ban_ghi_cung_nguon': sum(c['quan_sat'][src]['o_open_co_ban_ghi_cung_nguon'] for c in cs),
                       'o_open_co_ban_ghi_nguon_khac': sum(c['o_open_co_ban_ghi_nguon_khac'][src] for c in cs),
                       'so_o_bien': sum(len(c['quan_sat'][src]['o_bien']) for c in cs),
                       'ca_co_o_OPEN': sum(any(s == 'OPEN' for s in c['quan_sat'][src]['trang_thai_o']) for c in cs)}
        a['quan_sat'] = qs
        agg[ds] = a
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--only', default=None, help='giới hạn mã mờ, phân tách dấu phẩy (thử nhanh)')
    args = ap.parse_args()
    run = ROOT / args.run
    run.mkdir(parents=True, exist_ok=False)
    prog = open(run / 'progress.jsonl', 'a', encoding='utf-8')

    def log(**kw):
        kw['at'] = now()
        kw['rss_bytes'] = rss()
        prog.write(json.dumps(kw, ensure_ascii=False) + '\n')
        prog.flush()
        print(json.dumps(kw, ensure_ascii=False), flush=True)

    t_start = time.time()
    allow_re = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    moc = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')
    allow_nz = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    only = set(args.only.split(',')) if args.only else None
    work = [('RE2-TT', o) for o in sorted(allow_re)] + [('Nezha-OB', o) for o in sorted(allow_nz)]
    if only:
        work = [w for w in work if w[1] in only]
    log(event='start', n_cases=len(work), python=sys.version, numpy=np.__version__, pandas=pd.__version__,
        pyarrow=pyarrow.__version__, platform=platform.platform())
    cases, loi = [], []
    for i, (ds, oid) in enumerate(work):
        try:
            r = ca_re2(allow_re, moc, oid) if ds == 'RE2-TT' else ca_nezha(allow_nz, oid)
            cases.append(r)
            log(event='case_done', i=i + 1, dataset=ds, opaque_id=oid, giay=r['cost']['giay'])
        except Exception as exc:  # giữ ca lỗi trong kết quả, không dừng cả lượt
            loi.append({'dataset': ds, 'opaque_id': oid, 'loi': f'{type(exc).__name__}: {exc}'})
            log(event='case_error', i=i + 1, dataset=ds, opaque_id=oid, loi=f'{type(exc).__name__}: {exc}')
    out = {
        'schema': 'T043-KS16-pha1-v1', 'task': 'T-043', 'buoc': '4 pha 1 (không nhãn)', 'run': args.run,
        'created_utc': now(), 'labels_read': False,
        'ghi_chu_nhan': 'RE2-TT chỉ đọc mốc t qua nhan.nap_moc (chế độ (a), Q-66); không đọc root, loại lỗi, ô.',
        'inputs': {'results/T-022/allowlist-dev.json': sha_file(ROOT / 'results/T-022/allowlist-dev.json'),
                   'results/T-026/allowlist-dev.json': sha_file(ROOT / 'results/T-026/allowlist-dev.json'),
                   'script': sha_file(Path(__file__))},
        'dinh_nghia': DINH_NGHIA,
        'tham_so': {'NUA': NUA, 'CELL': CELL, 'TOL_US': TOL_US, 'M_SPAN': M_SPAN, 'M_METRIC': M_METRIC,
                    'M_COUNT': M_COUNT, 'GATE_EXACT_MAX': GATE_EXACT_MAX},
        'so_ca_xong': len(cases), 'ca_loi': loi,
        'tong_hop': tong_hop(cases),
        'cases': cases,
        'cost': {'tong_giay': round(time.time() - t_start, 1), 'rss_cuoi_bytes': rss()},
    }
    with open(run / 'dem-khong-nhan.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=None, allow_nan=False, default=json_mac_dinh)
    h = sha_file(run / 'dem-khong-nhan.json')
    log(event='end', so_ca=len(cases), ca_loi=len(loi), tong_giay=out['cost']['tong_giay'], sha256=h)


if __name__ == '__main__':
    main()

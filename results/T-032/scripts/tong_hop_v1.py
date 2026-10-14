#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T-032, phiên 12 — dựng bảng tự động theo ca cho phần tổng hợp.

Chỉ ghép các file kết quả đã có (đã kiểm khớp bản đóng băng ở phiên 9–11).
Không gọi phương pháp RCA nào, không đọc dữ liệu thô, không tính điểm mới.
Nhãn (root, loại lỗi) lấy từ chính các file kết quả đã nối nhãn; ở đây chỉ dùng để
tổ chức bảng phân tích.

Dùng:  python3 -B -X utf8 tong_hop_v1.py <thư mục chứa results/...> <thư mục ra>

Đầu ra (trong <thư mục ra>):
  doi-chieu-dung-sai.json     bảng theo đơn vị (372) + cặp đối chứng (301) + bảng nhóm (52)
  chuoi-bang-chung.json       chuỗi đầu vào → xử lý → trung gian → điểm/hạng theo đơn vị
  phan-xu-caller-root.json    mọi đơn vị có cờ M5 nguồn, từng dịch vụ phía trên đứng trước root
  can-thiep-tinh-toan.json    A′ theo ca + sổ các phép đổi khác
  kha-nang-do-trace.json      mức đo được "dịch vụ gọi chờ root" theo ba mức chặt
  coverage-trace.json         độ phủ trace theo ca
  ke-hoach-doc-tay.json       đơn vị đọc tay theo nhóm, chọn bằng quy tắc
  phieu-doc/<mã>.txt          phiếu đọc cho từng đơn vị đọc tay
  tu-kiem.json                các phép tự kiểm của script này
"""
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

IN = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(os.path.join(OUT, 'phieu-doc'), exist_ok=True)

T32 = 'results/T-032/'
RUNS = T32 + 'runs/'
T28 = 'results/T-028/runs/phan-hoi-review-001/'
USED = {}


def L(rel):
    p = os.path.join(IN, rel)
    with open(p, 'rb') as f:
        b = f.read()
    USED[rel] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    return json.loads(b.decode('utf-8'))


def W(name, obj):
    p = os.path.join(OUT, name)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')


def names(lst):
    out = []
    for x in lst or []:
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            out.append(x.get('entity') or x.get('service') or x.get('name'))
    return out


def ptr(rel, pointer):
    return {'path': rel, 'json_pointer': pointer}


CHECKS = []


def check(name, ok, detail=None):
    CHECKS.append({'name': name, 'pass': bool(ok), 'detail': detail})


# ---------------------------------------------------------------- nạp nguồn
cat = L(T32 + 'bao-phu-nhom.json')
t028 = L(T28 + 'ca-sai.json')
proxy = L(T28 + 'caller-root-proxy.json')
cp_units = L(RUNS + 'chain-position-002/units.json')
cp_sum = L(RUNS + 'chain-position-002/summary.json')
link_cases = L(RUNS + 'slow-call-flag-link-001/cases.json')
link_sum = L(RUNS + 'slow-call-flag-link-001/summary.json')
mr_ap = L(RUNS + 'microrank-core-aprime-c1-002/summary.json')
mr_md = L(RUNS + 'microrank-md-001/collect-001/summary.json')
mr_pt = L(RUNS + 'microrank-partition-001/collect-001/summary.json')
mr_vf = L(RUNS + 'microrank-laptop-verify-001/result.json')
tr_td = L(RUNS + 'tracerca-core-td-001/summary.json')
tr_sc = L(RUNS + 'tracerca-score-contrast-001/summary.json')
tr_or = L(RUNS + 'tracerca-original-ranking-001/cases.json')
sr_dc = L(RUNS + 'simplerca-decomposition-002/summary.json')
sr_s1 = L(RUNS + 'simplerca-s1-001/summary.json')
ba_b1 = L(RUNS + 'baro-b1-001/summary.json')
ba_b2 = L(RUNS + 'baro-b2-001/summary.json')
inh = L(RUNS + 'inherit-verify-001/result.json')
ci_k2 = L(RUNS + 'circa-laptop-k2-001/collect-001/summary.json')
ci_ed = L(RUNS + 'circa-laptop-k2-edges-001/collect-001/summary.json')
ci_k1 = L(RUNS + 'circa-k1-002/k1.json')
to_sv = L(RUNS + 'torai-severity-table-003/summary.json')
to_lc = L(RUNS + 'torai-log-contrast-001/summary.json')
to_s1 = L(RUNS + 'torai-log-contrast-seeds-001/summary.json')
to_s2 = L(RUNS + 'torai-log-contrast-seeds-002/summary.json')
to_bd = L(RUNS + 'torai-block-decomposition-001/summary.json')
sem = L(RUNS + 'trace-semantics-002/semantics.json')
cslow = L(RUNS + 'call-slow-001/summary.json')
cint = L(RUNS + 'call-interval-001/summary.json')
rsl = L(RUNS + 'root-signal-location-001/summary.json')
plc = L(RUNS + 'root-signal-placebo-003/summary.json')
census = L(RUNS + 'trace-root-census-001/summary.json')
derived = L(RUNS + 'derived-tables-001/derived.json')
mchain = L(RUNS + 'metric-chain-001/rows.json')
kndt_old = L(T32 + 'kha-nang-do-trace.json')

UP_CLASSES = set(cp_sum['groups']['phia_tren'])
BI_CLASSES = set(cp_sum['groups']['hai_chieu'])
DOWN_CLASSES = set(cp_sum['groups']['phia_duoi'])
NOREL_CLASSES = set(cp_sum['groups']['khong_lien_he'])
NOSPAN_CLASSES = set(cp_sum['groups']['khong_co_span'])


def pos_group(cls):
    if cls in UP_CLASSES:
        return 'phia_tren'
    if cls in BI_CLASSES:
        return 'hai_chieu'
    if cls in DOWN_CLASSES:
        return 'phia_duoi'
    if cls in NOREL_CLASSES:
        return 'khong_lien_he'
    if cls in NOSPAN_CLASSES:
        return 'khong_co_span'
    return 'khac:' + str(cls)


def coarse(kind):
    """Gộp tên cột thành loại thô; chỉ dùng cho chữ ký đường đi."""
    if kind is None:
        return '-'
    k = str(kind).lower()
    if 'latency' in k:
        return 'do-tre'
    if 'network' in k:
        return 'mang'
    if 'mem' in k:
        return 'mem'
    if 'cpu' in k:
        return 'cpu'
    return str(kind)


def idx(rows, keyf):
    d = {}
    for i, r in enumerate(rows):
        d[keyf(r)] = (i, r)
    return d


DO = lambda r: (r['dataset'], r['opaque_id'])
O = lambda r: r['opaque_id']

I_t028 = idx(t028['main_rows'], lambda r: (r['dataset'], r['method'], r['opaque_id']))
I_proxy = idx(proxy['records'], lambda r: (r['dataset'], r['method'], r['opaque_id'], str(r['seed'])))
I_cp = idx(cp_units, lambda r: (r['dataset'], r['method'], r['opaque_id'], None if r['seed'] is None else str(r['seed'])))
I_link = idx(link_cases, lambda r: (r['dataset'], r['method'], r['opaque_id']))
I_mr_ap = idx(mr_ap['cases'], DO)
I_mr_md = idx(mr_md['cases'], DO)
I_mr_pt = idx(mr_pt['cases'], DO)
I_mr_vf = idx(mr_vf['rows'], DO)
I_tr_td = idx(tr_td['cases'], DO)
I_tr_sc = idx(tr_sc['cases'], DO)
I_tr_or = idx(tr_or['cases'], DO)
I_sr_dc = idx(sr_dc['cases'], DO)
I_sr_s1 = idx(sr_s1['cases'], DO)
I_ba_b1 = idx(ba_b1['cases'], DO)
I_ba_b2 = idx(ba_b2['cases'], DO)
I_inh = idx(inh['rows'], lambda r: (r['method'], r['opaque_id']))
I_ci_k2 = idx(ci_k2['cases'], O)
I_ci_ed = idx(ci_ed['cases'], O)
I_ci_k1 = idx(ci_k1['cases'], O)
I_to_sv = idx(to_sv['units'], lambda r: (r['opaque_id'], r['seed']))
I_to_lc = idx(to_lc['cases'], O)
I_to_bd = idx(to_bd['units'], lambda r: (r['opaque_id'], r['seed']))
I_sem = idx(sem['cases'], DO)
I_cslow = idx(cslow['cases'], DO)
I_cint = idx(cint['cases'], DO)
I_rsl = idx(rsl['cases'], DO)
I_plc = idx(plc['cases'], DO)
I_census = idx(census['cases'], DO)
I_kndt = idx(kndt_old['cases'], DO)

seed_rows = {}
for src, rel in ((to_s1, 'torai-log-contrast-seeds-001'), (to_s2, 'torai-log-contrast-seeds-002')):
    for i, r in enumerate(src['rows']):
        seed_rows[(r['opaque_id'], r['branch'])] = (rel, i, r)

ba_pairs = defaultdict(list)
for i, p in enumerate(derived['baro']['pairs']):
    ba_pairs[(p['dataset'], p['opaque_id'])].append((i, p))
ba_case = idx(derived['baro']['cases'], DO)
sr_pairs = defaultdict(list)
for i, p in enumerate(derived['simplerca']['pairs']):
    sr_pairs[(p['dataset'], p['opaque_id'])].append((i, p))
mc_rows = defaultdict(dict)
for i, r in enumerate(mchain):
    mc_rows[(r['dataset'], r['method'], r['opaque_id'])][r['entity']] = (i, r)

# ---------------------------------------------------------------- mức đo được theo ca (ba mức chặt)
OLD_OK = 'đo được (có điều kiện)'
STRICT_NOTE = {
    'đo được': ('Điều kiện: mã đã triển khai lúc thu dữ liệu gọi theo cùng cách với commit công khai duy nhất '
                '(IntelligentDDS/Augmented-OnlineBoutique 94a01ba4); span phía gọi do interceptor phía gọi của '
                'OpenTelemetry tạo quanh lời gọi gRPC chặn. Đo được thời lượng dịch vụ gọi chờ lời gọi tới root '
                'và phần nằm trong span của root. Không tách được phần ngoài span của root (đường truyền, hàng đợi, '
                'xử lý trước khi span của root bắt đầu).'),
    'đo được một phần': ('Có cạnh gọi tới root đủ lời gọi, khoảng thời gian hợp lệ, và mọi chỗ gọi là lời gọi chặn ở cả '
                         'bảy tag ứng viên. Thiếu đúng một bằng chứng: công cụ và phiên bản đã tạo span (RCAEval không '
                         'công bố), nên chưa kiểm được span phía gọi bao đúng lời gọi chặn. Vì vậy chỉ gọi là quan sát '
                         '"span phía gọi dài ra", chưa gọi là đã đo thời gian chờ.'),
    'không đo được': 'Root không được dịch vụ nào gọi trong trace, hoặc cạnh gọi tới root có dưới 20 lời gọi ở một phía mốc.',
}


def strict_level(dataset, old_level):
    if old_level == OLD_OK:
        return 'đo được' if dataset == 'Nezha-OB' else 'đo được một phần'
    return 'không đo được'


def root_positions_top(dataset, oid):
    e = I_rsl.get((dataset, oid))
    if not e or e[1].get('status') != 'OK':
        return None
    rp = e[1].get('root_positions') or {}
    out = []
    for k, v in rp.items():
        if isinstance(v, dict) and v.get('rank_max') == 1 and v.get('rank_min') == 1:
            out.append(k)
    return out


CASE = {}
for (ds, oid), (i, c) in I_sem.items():
    cs_i, cs = I_cslow[(ds, oid)]
    edges_to_root = cs.get('edges_to_root') or {}
    CASE[(ds, oid)] = {
        'dataset': ds, 'opaque_id': oid, 'root': c['root'], 'fault': c['fault'], 'cell': c['cell'],
        'muc_do_duoc': strict_level(ds, c['level']),
        'muc_phien_10': c['level'], 'ly_do': c['reason'],
        'so_canh_toi_root': c.get('incoming_edges'),
        'ty_le_loi_goi_cham_toi_root_lon_nhat_sau_moc': cs.get('to_root_max_slow_share_after'),
        'vi_tri_trace_root_dung_dau': root_positions_top(ds, oid),
        'nguon': {'muc': ptr(RUNS + 'trace-semantics-002/semantics.json', '/cases/%d' % i),
                  'loi_goi_cham': ptr(RUNS + 'call-slow-001/summary.json', '/cases/%d' % cs_i)},
        '_edges_to_root': edges_to_root,
    }

# ---------------------------------------------------------------- chi tiết theo phương pháp


def eff_rank(rmin, rmax):
    return [rmin, rmax]


def baro_detail(ds, oid):
    d = {}
    i1, b1 = I_ba_b1[(ds, oid)]
    i2, b2 = I_ba_b2[(ds, oid)]
    ic, bc = ba_case[(ds, oid)]
    nat = b2['native']
    chg = b2['changed']
    above_nat = names(nat.get('above_root'))
    above_chg = names(chg.get('above_root'))
    pairs = []
    mc = mc_rows.get((ds, 'baro', oid), {})
    for ip, p in ba_pairs.get((ds, oid), []):
        e = p['entity']
        m = mc.get(e, (None, {}))[1]
        pairs.append({
            'entity': e, 'relation_phien9': p['relation'],
            'cot_thang': p['entity_best']['column'], 'loai_cot': p['entity_best']['kind'], 'z': p['entity_best']['z'],
            'IQR_tren_median': p['entity_best']['IQR_over_abs_median'],
            'lech_tren_median': p['entity_best']['numerator_over_abs_median'],
            'vi_tri_chuoi_goi': m.get('position'), 'nhom_xu_huong': m.get('win_group'),
            'luu_luong_doi': m.get('traffic_changed'),
            'con_tren_root_duoi_B2': e in above_chg,
            'nguon': ptr(RUNS + 'derived-tables-001/derived.json', '/baro/pairs/%d' % ip)})
    d['root'] = {'cot_thang': bc['root']['column'], 'loai_cot': bc['root']['kind'], 'z': bc['root']['z'],
                 'IQR_tren_median': bc['root']['IQR_over_abs_median'],
                 'lech_tren_median': bc['root']['numerator_over_abs_median'],
                 'hang': eff_rank(nat.get('root_rank_min'), nat.get('root_rank_max')),
                 'so_nhom_hoa': nat.get('n_tie_groups'), 'so_thuc_the': nat.get('n_entities')}
    d['tren_root'] = pairs
    d['B1_khong_loc_cot_hang'] = {'tac_dung_len_root': b1['b1_effect_on_root'],
                                  'cot_root_duoc_giu_them': len(b1.get('root_columns_added_by_b1') or []),
                                  'cot_tot_nhat_cua_root_la_cot_them': b1.get('root_best_column_added_by_b1'),
                                  'nguon': ptr(RUNS + 'baro-b1-001/summary.json', '/cases/%d' % i1)}
    d['B2_thang_do_lech_chuan'] = {'tac_dung_len_root': b2['effect_on_root'],
                                    'hang_root': eff_rank(chg.get('root_rank_min'), chg.get('root_rank_max')),
                                    'cap_mat': b2['pairs_no_longer_above'], 'cap_moi': b2['pairs_newly_above'],
                                    'nguon': ptr(RUNS + 'baro-b2-001/summary.json', '/cases/%d' % i2)}
    d['_above'] = above_nat
    d['_still'] = {'B2': set(above_chg)}
    top = None
    if pairs:
        top = max(pairs, key=lambda x: x['z'])
    b2first = chg.get('root_rank_max') == 1
    sig = 'B2:%s|dau:%s|cot:%s' % ('len-hang-1' if b2first else 'khong-len-hang-1',
                                    (top or {}).get('vi_tri_chuoi_goi') or 'khong-ro',
                                    coarse((top or {}).get('loai_cot')))
    d['thuc_the_z_cao_nhat_tren_root'] = top['entity'] if top else None
    return d, sig


def simplerca_detail(ds, oid):
    d = {}
    i0, c = I_sr_dc[(ds, oid)]
    i1, s1 = I_sr_s1[(ds, oid)]
    rp = c.get('root_parts') or {}
    chg = s1.get('changed') or {}
    above_chg = names(chg.get('above_root'))
    mc = mc_rows.get((ds, 'simplerca', oid), {})
    dp = {p['entity']: (ip, p) for ip, p in sr_pairs.get((ds, oid), [])}
    pairs = []
    for a in c.get('above_root') or []:
        e = a['entity']
        m = mc.get(e, (None, {}))[1]
        ip, p = dp.get(e, (None, {}))
        diff = a.get('difference_vs_root') or {}
        pairs.append({'entity': e, 'phieu_metric': a.get('metric'), 'phieu_trace': a.get('trace'), 'phieu_log': a.get('log'),
                      'diem': a.get('score'), 'chenh_metric': diff.get('metric'), 'chenh_trace': diff.get('trace'),
                      'chenh_log': diff.get('log'), 'chenh_diem': diff.get('score'),
                      'rieng_metric_du_quyet_dinh': (diff.get('metric') is not None and diff.get('score') is not None
                                                     and diff.get('metric') > 0 and (diff.get('metric') >= diff.get('score'))),
                      'loai_cot_nhieu_phieu_nhat': p.get('entity_top_column_kind'),
                      'phieu_cot_nhieu_nhat': p.get('entity_top_column_votes'),
                      'mot_cot_vuot_tong_diem_root': p.get('entity_top_single_column_exceeds_root_total_score'),
                      'vi_tri_chuoi_goi': m.get('position'), 'nhom_xu_huong': m.get('win_group'),
                      'luu_luong_doi': m.get('traffic_changed'),
                      'con_tren_root_duoi_S1': e in above_chg,
                      'nguon': ptr(RUNS + 'simplerca-decomposition-002/summary.json', '/cases/%d/above_root' % i0)})
    d['root'] = {'phieu_metric': rp.get('metric'), 'phieu_trace': rp.get('trace'), 'phieu_log': rp.get('log'),
                 'diem': rp.get('score'), 'cot_metric_co_phieu': rp.get('metric_columns_with_votes'),
                 'cot_metric_dung_duoc': rp.get('metric_columns_usable'),
                 'hang': eff_rank(rp.get('rank_min'), rp.get('rank_max'))}
    d['tren_root'] = pairs
    d['so_cap_rieng_metric_quyet_dinh'] = c.get('above_decided_by_metric_alone')
    d['S1_dem_theo_cot'] = {'tac_dung_len_root': s1.get('effect_on_root'),
                            'hang_root': eff_rank(chg.get('root_rank_min'), chg.get('root_rank_max')),
                            'so_nhom_hoa': chg.get('n_tie_groups'),
                            'cap_mat': s1.get('pairs_no_longer_above'), 'cap_moi': s1.get('pairs_newly_above'),
                            'nguon': ptr(RUNS + 'simplerca-s1-001/summary.json', '/cases/%d' % i1)}
    d['_above'] = [p['entity'] for p in pairs]
    d['_still'] = {'S1': set(above_chg)}
    top = max(pairs, key=lambda x: x['diem']) if pairs else None
    sig = 'metric-root:%s|dau:%s|cot:%s' % ('khong-phieu' if not rp.get('metric') else 'co-phieu',
                                             (top or {}).get('vi_tri_chuoi_goi') or 'khong-ro',
                                             coarse((top or {}).get('loai_cot_nhieu_phieu_nhat')))
    return d, sig


def microrank_detail(ds, oid):
    d = {}
    ia, a = I_mr_ap[(ds, oid)]
    im, m = I_mr_md[(ds, oid)]
    ip, p = I_mr_pt[(ds, oid)]
    lk = I_link.get((ds, 'microrank', oid))
    if a.get('status') != 'OK':
        return {'trang_thai_phat_lai': a.get('status')}, 'khong-OK'
    br = a['branches']
    wn, wu, c1 = br['w_native'], br['w_unit'], br['c1']
    cnt = a['counts']
    A = cnt.get('A') or 0
    above = names(wn.get('above_root'))
    ent = {}
    if lk:
        for e in lk[1].get('entities') or []:
            ent[e['entity']] = e
    pairs = []
    mo15 = (p.get('branches') or {}).get('mo15') or {}
    mo1 = (p.get('branches') or {}).get('mo1p50') or {}
    ab15 = set(names(mo15.get('above')))
    ab1 = set(names(mo1.get('above')))
    wu_p = a.get('w_unit_pairs_above_root_native') or {}
    c1_p = a.get('c1_pairs_above_root_native') or {}
    md_p = m.get('pairs_above_root_native') or {}
    for x in wn.get('above_root') or []:
        e = x['entity']
        le = ent.get(e, {})
        tr = le.get('trace') or {}
        pairs.append({'entity': e, 'relation_phien9': x.get('relation'), 'vi_tri_chuoi_goi': pos_group(le.get('class')) if le else None,
                      'thao_tac_cao_nhat': x.get('operation'), 'diem': x.get('score'), 'hang': x.get('rank_min'),
                      'trace_bat_thuong_tu_mang_co': x.get('max_operation_own_A'),
                      'trace_bat_thuong_chi_ngu_canh': x.get('max_operation_context_only_A'),
                      'ty_le_trace_bat_thuong_gan_voi_root': tr.get('share_linked'),
                      'con_tren_root': {'A_phay': (wu_p.get(e) or {}).get('still_above'),
                                        'C1': (c1_p.get(e) or {}).get('still_above'),
                                        'MD': (md_p.get(e) or {}).get('still_above'),
                                        'chia_mo15': (e in ab15) if mo15.get('status') == 'OK' else None,
                                        'chia_mo1p50': (e in ab1) if mo1.get('status') == 'OK' else None}})
    d['dem'] = {'trace_bat_thuong': A, 'trace_binh_thuong': cnt.get('N'), 'ty_le_trace_bat_thuong': cnt.get('share_A'),
                'trace_bat_thuong_khong_co_dich_vu_root': cnt.get('A_traces_without_root_service'),
                'trace_bat_thuong_root_tu_mang_co': cnt.get('A_traces_root_service_own_abnormal'),
                'span_mang_co': cnt.get('abnormal_spans')}
    r = wn.get('root') or {}
    d['root'] = {'thao_tac_cao_nhat': r.get('operation'), 'diem': r.get('score'), 'hang': eff_rank(r.get('rank_min'), r.get('rank_max'))}
    d['tren_root'] = pairs
    d['A_phay_trong_so_don_vi'] = {'tac_dung_len_root': a.get('w_unit_effect_on_root'),
                                    'hang_root': eff_rank((wu.get('root') or {}).get('rank_min'), (wu.get('root') or {}).get('rank_max')),
                                    'nguon': ptr(RUNS + 'microrank-core-aprime-c1-002/summary.json', '/cases/%d/branches/w_unit' % ia)}
    d['C1_dem_rieng'] = {'tac_dung_len_root': a.get('c1_effect_on_root'),
                         'hang_root': eff_rank((c1.get('root') or {}).get('rank_min'), (c1.get('root') or {}).get('rank_max')),
                         'nguon': ptr(RUNS + 'microrank-core-aprime-c1-002/summary.json', '/cases/%d/branches/c1' % ia)}
    mdv = (m.get('views') or {}).get('md') or {}
    d['MD_co_theo_phan_chua_phu'] = {'tac_dung_len_root': m.get('md_effect_on_root'),
                                      'hang_root': eff_rank(mdv.get('root_rank_min'), mdv.get('root_rank_max')),
                                      'nguon': ptr(RUNS + 'microrank-md-001/collect-001/summary.json', '/cases/%d' % im)}

    def part(b):
        if not b:
            return {'trang_thai': 'không có nhánh'}
        call = b.get('call') or {}
        return {'trang_thai': b.get('status'), 'loi': b.get('error'),
                'hang_root': eff_rank(b.get('root_rank_min'), b.get('root_rank_max')),
                'so_tren_root': len(b.get('above') or []) if b.get('status') == 'OK' else None,
                'dau_bang': names(b.get('top')),
                'ty_le_trace_bat_thuong_co_root': b.get('new_abnormal_share_with_root'),
                'so_trace_bat_thuong_moi': call.get('new_abnormal') if isinstance(call, dict) else None}
    d['chia_theo_bai_goc'] = {'dat_moc_90': p.get('gate_pass'), 'mo15': part(mo15), 'mo1p50': part(mo1),
                              'nguon': ptr(RUNS + 'microrank-partition-001/collect-001/summary.json', '/cases/%d' % ip)}
    d['_above'] = above
    d['_still'] = {'A_phay': {e for e in above if (wu_p.get(e) or {}).get('still_above')},
                   'C1': {e for e in above if (c1_p.get(e) or {}).get('still_above')},
                   'MD': {e for e in above if (md_p.get(e) or {}).get('still_above')},
                   'chia_mo15': ab15 if mo15.get('status') == 'OK' else None}
    n_up = sum(1 for x in pairs if x['vi_tri_chuoi_goi'] in ('phia_tren', 'hai_chieu'))
    if not p.get('gate_pass'):
        chia = 'N/A-moc-90'
    elif mo15.get('status') != 'OK':
        chia = 'khong-OK'
    elif mo15.get('root_rank_max') == 1:
        chia = 'len-hang-1'
    elif (mo15.get('root_rank_min') or 99) < (r.get('rank_min') or 0):
        chia = 'tang-chua-hang-1'
    else:
        chia = 'khong-tang'
    c1s = 'len-hang-1' if (c1.get('root') or {}).get('rank_max') == 1 else 'khong-len-hang-1'
    sig = 'chia:%s|C1:%s|phia-tren:%s' % (chia, c1s, 'co' if n_up else 'khong')
    return d, sig


def tracerca_detail(ds, oid):
    d = {}
    it, t = I_tr_td[(ds, oid)]
    isc, sc = I_tr_sc[(ds, oid)]
    io, orr = I_tr_or[(ds, oid)]
    lk = I_link.get((ds, 'tracerca', oid))
    if t.get('status') != 'OK':
        return {'trang_thai_phat_lai': t.get('status'), 'ly_do': t.get('reason')}, 'khong-OK'
    nat = t['native']
    td = t['t_d']
    H = t['counts']['H_native']
    measurable = bool(lk and lk[1].get('root_edge_measurable'))
    ent = {}
    if lk:
        for e in lk[1].get('entities') or []:
            ent[e['entity']] = e
    views = sc.get('views') or {}
    ab_tr1 = set(names((views.get('tr1') or {}).get('above')))
    ab_ts = set(names((views.get('ts') or {}).get('above')))
    td_p = t.get('pairs_above_root_native') or {}
    r = nat.get('root') or {}
    pairs = []
    for x in nat.get('above_root') or []:
        e = x['entity']
        le = ent.get(e, {})
        sp = le.get('span') or {}
        pg = pos_group(le.get('class')) if le else None
        wait = None
        if pg in ('phia_tren', 'hai_chieu'):
            wait = (sp.get('share_r50') is not None and sp.get('share_r50') >= 0.5) if measurable else 'khong-xet-duoc'
        pairs.append({'entity': e, 'relation_phien9': x.get('relation'), 'vi_tri_chuoi_goi': pg, 'lop': le.get('class'),
                      'thao_tac_cao_nhat': x.get('operation'), 'a': x.get('a'), 'n': x.get('n'), 'diem': x.get('score'),
                      'ty_le_a_tren_n': (x.get('a') / x.get('n')) if x.get('n') else None,
                      'ty_le_span_mang_co_la_span_cho_root': sp.get('share_r50'),
                      'chu_yeu_la_cho_root': wait,
                      'con_tren_root': {'TD': (td_p.get(e) or {}).get('still_above'),
                                        'ty_le_a_tren_n': e in ab_tr1, 'so_tuyet_doi_a': e in ab_ts}})
    d['H'] = H
    d['canh_toi_root_xet_duoc'] = measurable
    d['root_duoc_xep'] = nat.get('root_ranked')
    d['root'] = {'thao_tac_cao_nhat': r.get('operation'), 'a': r.get('a'), 'n': r.get('n'), 'diem': r.get('score'),
                 'ty_le_a_tren_n': (r.get('a') / r.get('n')) if r.get('n') else None,
                 'hang': eff_rank(r.get('rank_min'), r.get('rank_max'))}
    d['tren_root'] = pairs
    d['TD_co_theo_phan_chua_phu'] = {'tac_dung_len_root': t.get('td_effect_on_root'),
                                      'hang_root': eff_rank((td.get('root') or {}).get('rank_min'), (td.get('root') or {}).get('rank_max')),
                                      'nguon': ptr(RUNS + 'tracerca-core-td-001/summary.json', '/cases/%d' % it)}

    def vw(k):
        v = views.get(k) or {}
        return eff_rank(v.get('root_rank_min'), v.get('root_rank_max')) if v.get('root_ranked') else None
    d['doi_cong_thuc_diem'] = {'ty_le_a_tren_n': vw('tr1'), 'ty_le_tu_20_span': vw('tr1m'), 'so_tuyet_doi_a': vw('ts'),
                               'nguon': ptr(RUNS + 'tracerca-score-contrast-001/summary.json', '/cases/%d' % isc)}
    ob = (orr.get('branches') or {}).get('to_p') or {}
    d['buoc_xep_hang_bai_goc_to_p'] = {'trang_thai': ob.get('status'), 'dac_trung_huu_ich': ob.get('feature_useful'),
                                        'root_diem_duong': ob.get('root_score_positive'),
                                        'hang_root': eff_rank(ob.get('root_rank_min'), ob.get('root_rank_max')),
                                        'dau_bang': names(ob.get('top')),
                                        'nguon': ptr(RUNS + 'tracerca-original-ranking-001/cases.json', '/cases/%d/branches/to_p' % io)}
    d['_above'] = [p['entity'] for p in pairs]
    d['_still'] = {'TD': {e for e in d['_above'] if (td_p.get(e) or {}).get('still_above')},
                   'ty_le': ab_tr1, 'tuyet_doi': ab_ts}
    if not nat.get('root_ranked'):
        return d, 'root-khong-duoc-xep'
    n_wait = sum(1 for p in pairs if p['chu_yeu_la_cho_root'] is True)
    n_up = sum(1 for p in pairs if p['vi_tri_chuoi_goi'] in ('phia_tren', 'hai_chieu'))
    if n_wait:
        w = 'co' if n_wait == len(pairs) else 'mot-phan'
    elif n_up and not measurable:
        w = 'khong-xet-duoc'
    else:
        w = 'khong'
    tr1 = (views.get('tr1') or {})
    sig = 'cho-root:%s|ty-le:%s' % (w, 'len-hang-1' if tr1.get('root_rank_max') == 1 else 'khong-len-hang-1')
    return d, sig


def circa_detail(oid):
    d = {}
    i2, c = I_ci_k2[oid]
    ie, e = I_ci_ed[oid]
    i1, k1 = I_ci_k1[oid]
    v = c['views']
    obs = c.get('obs') or {}
    huge_svc = set(obs.get('services_with_da_huge') or [])
    above_da = names(v['native_da'].get('above_root'))
    above_rht = names(v['native_rht'].get('above_root'))
    above_k2 = set(names(v['k2_rht'].get('above_root')))
    ev = e.get('views') or {}
    callers = set(c.get('callers_of_root') or [])
    pairs = []
    for x in above_da:
        pairs.append({'entity': x, 'goi_truc_tiep_root': x in callers, 'mang_khoa_cuc_lon_sau_DA': x in huge_svc,
                      'dung_tren_root_o_bang_khong_DA': x in above_rht, 'con_tren_root_khi_bo_canh_bang_RHT': x in above_k2})
    hn = obs.get('huge_nodes') or []
    d['nut_cuc_lon'] = [{'nut': h.get('node'), 'so_cha': h.get('n_parents'), 'y_train_so_gia_tri': h.get('train_y_n_unique'),
                         'y_train_do_lech_chuan': h.get('train_y_std'), 'scale_phan_du': h.get('residual_scale'),
                         'rht': h.get('rht_score'), 'rht_khong_canh': h.get('rht_without_edges')} for h in hn]
    d['co_nut_cuc_lon'] = c.get('has_huge_node')
    d['root_mang_khoa_cuc_lon_sau_DA'] = obs.get('root_has_da_huge_node')
    d['nguon_khoa_cuc_lon_cua_root'] = obs.get('root_da_huge_source')
    d['hang_root'] = {'RHT': eff_rank(v['native_rht'].get('root_rank_min'), v['native_rht'].get('root_rank_max')),
                      'DA': eff_rank(v['native_da'].get('root_rank_min'), v['native_da'].get('root_rank_max')),
                      'K2_khong_canh_RHT': eff_rank(v['k2_rht'].get('root_rank_min'), v['k2_rht'].get('root_rank_max')),
                      'k2x_chi_canh_cung_dich_vu': eff_rank((ev.get('k2x') or {}).get('root_rank_min'), (ev.get('k2x') or {}).get('root_rank_max')),
                      'k2s_chi_canh_khac_dich_vu': eff_rank((ev.get('k2s') or {}).get('root_rank_min'), (ev.get('k2s') or {}).get('root_rank_max'))}
    d['cot_tot_nhat_cua_root'] = v['native_da'].get('root_best_item')
    d['tac_dung_DA_len_root'] = c.get('da_effect_on_root')
    d['tac_dung_bo_canh_len_root_RHT'] = (c.get('k2') or {}).get('removing_edges_effect_on_root')
    d['tren_root_bang_DA'] = pairs
    d['nguon'] = {'K2': ptr(RUNS + 'circa-laptop-k2-001/collect-001/summary.json', '/cases/%d' % i2),
                  'loai_canh': ptr(RUNS + 'circa-laptop-k2-edges-001/collect-001/summary.json', '/cases/%d' % ie),
                  'K1': ptr(RUNS + 'circa-k1-002/k1.json', '/cases/%d' % i1)}
    d['_above'] = above_da
    d['_still'] = {'K2_RHT': above_k2 & set(above_da)}
    n_huge_above = sum(1 for p in pairs if p['mang_khoa_cuc_lon_sau_DA'])
    sig = 'cuc-lon:%s|tren-root-cuc-lon:%s|DA:%s' % ('co' if c.get('has_huge_node') else 'khong',
                                                      'co' if n_huge_above else 'khong', c.get('da_effect_on_root'))
    return d, sig


def torai_detail(oid, seed):
    d = {}
    iu, u = I_to_sv[(oid, seed)]
    ib, b = I_to_bd[(oid, seed)]
    il, lc = I_to_lc[oid]
    pairs = []
    for a in u.get('above_root') or []:
        pairs.append({'entity': a['entity'], 'severity': a.get('severity'), 'chenh_severity': a.get('severity_minus_root'),
                      'cung_cum_voi_root': a.get('same_cluster_as_root'), 'chenh_theo_nguon': a.get('difference_by_source'),
                      'nguon_chenh_lon_nhat': a.get('largest_source_difference')})
    d['root'] = {'vecto_4_nguon': u.get('root_vector'), 'severity': u.get('root_severity'),
                 'hang_severity': u.get('root_severity_rank'), 'kich_thuoc_cum': u.get('root_cluster_size'),
                 'nhanh_xep_trong_cum': u.get('root_cluster_branch'), 'hang': eff_rank(u.get('root_rank_min'), u.get('root_rank_max'))}
    d['mat_hang_o_dau'] = u.get('where_lost')
    d['tren_root'] = pairs
    br = lc.get('branches') or {}

    def bb(k):
        x = br.get(k) or {}
        return {'hang_root_seed0': eff_rank(x.get('root_rank_min'), x.get('root_rank_max')), 'tren_root_seed0': names(x.get('above_root'))}
    d['bo_cot_log_nen_khong_doi_tl2'] = bb('tl2')
    d['bo_nguon_log_tl1'] = bb('tl1')
    for k in ('tl1', 'tl2'):
        sr = seed_rows.get((oid, k))
        key = 'bo_nguon_log_tl1' if k == 'tl1' else 'bo_cot_log_nen_khong_doi_tl2'
        if sr:
            d[key]['kiem_seed_1_2'] = {'hang_giong_nhau_ba_seed': sr[2].get('root_rank_same_across_seeds'), 'theo_seed': sr[2].get('seeds'),
                                       'nguon': ptr(RUNS + sr[0] + '/summary.json', '/rows/%d' % sr[1])}
        else:
            d[key]['kiem_seed_1_2'] = 'không chạy riêng: ở seed 0 root nằm trong cụm một dịch vụ và không khối nào do nhánh RCD xếp (KQ10 mục 8)'
    d['nguon'] = {'severity': ptr(RUNS + 'torai-severity-table-003/summary.json', '/units/%d' % iu),
                  'khoi': ptr(RUNS + 'torai-block-decomposition-001/summary.json', '/units/%d' % ib),
                  'doi_log': ptr(RUNS + 'torai-log-contrast-001/summary.json', '/cases/%d' % il)}
    d['_above'] = [p['entity'] for p in pairs]
    d['_still'] = {'tl1_seed0': set(names((br.get('tl1') or {}).get('above_root')))}
    logmax = all(p['nguon_chenh_lon_nhat'] == 'log' for p in pairs) if pairs else None
    tl1 = (br.get('tl1') or {}).get('root_rank_max') == 1
    sr1 = seed_rows.get((oid, 'tl1'))
    if sr1 and str(seed) in (sr1[2].get('seeds') or {}):
        rr = sr1[2]['seeds'][str(seed)].get('root_rank') or [None, None]
        tl1 = rr[1] == 1
        d['bo_nguon_log_tl1']['hang_root_dung_seed_nay'] = rr
    sig = 'severity-root:%s|log-chenh-lon-nhat:%s|bo-log:%s' % (
        'cao-nhat' if (u.get('root_severity_rank') or [9])[0] == 1 else 'khong-cao-nhat',
        {True: 'moi-cap', False: 'khong-moi-cap', None: '-'}[logmax], 'len-hang-1' if tl1 else 'khong-len-hang-1')
    return d, sig


# ---------------------------------------------------------------- phát lại khớp


def replay_exact(u):
    ds, m, oid, seed = u['dataset'], u['method'], u['opaque_id'], u['seed']
    if m in ('baro', 'simplerca'):
        e = I_inh.get((m, oid))
        if e:
            ok = oid not in (inh['summary'][m].get('not_exact') or []) and e[1].get('status') == 'OK'
            return {'trang_thai': 'phát lại trùng bản đóng băng từng bit' if ok else 'LỆCH',
                    'nguon': ptr(RUNS + 'inherit-verify-001/result.json', '/rows/%d' % e[0])}
    if m == 'microrank_full':
        e = I_mr_vf.get((ds, oid))
        if e:
            return {'trang_thai': 'phát lại trùng bản đóng băng từng bit' if e[1].get('result') == 'exact' else 'LỆCH: %s' % e[1].get('result'),
                    'nguon': ptr(RUNS + 'microrank-laptop-verify-001/result.json', '/rows/%d' % e[0])}
    if m == 'tracerca':
        e = I_tr_td.get((ds, oid))
        if e:
            return {'trang_thai': 'ji dựng lại trùng native từng bit' if e[1].get('sham_ji_bit_exact') else e[1].get('status'),
                    'ghi_chu': 'lượt phát lại 52/52 khớp: EC2 runs/tracerca-cohort-simple-001/segments/003/terminal.json (KQ9 mục 3)',
                    'nguon': ptr(RUNS + 'tracerca-core-td-001/summary.json', '/cases/%d' % e[0])}
    if m == 'circa_ols_da' and ds == 'RE2-TT':
        e = I_ci_k2.get(oid)
        if e:
            return {'trang_thai': 'sham và nhánh quan sát trùng bản đóng băng từng bit' if (e[1].get('sham_exact') and e[1].get('obs_exact')) else 'LỆCH',
                    'nguon': ptr(RUNS + 'circa-laptop-k2-001/collect-001/summary.json', '/cases/%d' % e[0])}
    if m == 'torai_B' and ds == 'RE2-TT':
        e = I_to_sv.get((oid, seed))
        if e:
            ck = e[1].get('checks') or {}
            return {'trang_thai': 'bảng severity dựng lại trùng bản ghi' if all(bool(x) for x in ck.values()) else 'LỆCH',
                    'ghi_chu': 'lượt phát lại 90/90 khớp từng bit: EC2 runs/torai-core-obs-001/progress.jsonl (KQ10 mục 5)',
                    'nguon': ptr(RUNS + 'torai-severity-table-003/summary.json', '/units/%d/checks' % e[0])}
    return {'trang_thai': 'không áp dụng: bản ghi không OK ở nguồn, phương pháp không chạy'}


# ---------------------------------------------------------------- bảng theo đơn vị
def t028_info(u):
    ds, m, oid = u['dataset'], u['method'], u['opaque_id']
    i, r = I_t028[(ds, m, oid)]
    out = {'nguon': ptr(T28 + 'ca-sai.json', '/main_rows/%d' % i), 'trang_thai': r['status']}
    seed = u['seed']
    sm = r.get('seed_metrics') or {}
    if seed is not None and str(seed) in sm:
        s = sm[str(seed)]
        out['hang'] = [s.get('rank_min'), s.get('rank_max')]
    else:
        out['hang'] = [r.get('rank_min'), r.get('rank_max')]
    out['sai_o_k1_theo_ca'] = r.get('wrong_OK_at_1')
    out['sai_o_k5_theo_ca'] = r.get('wrong_OK_at_5')
    mech = r.get('mechanisms') or {}
    out['co'] = {k: (mech.get(k, {}).get('assignment') or {}).get('multi') for k in ('1', '5')}
    out['co_chinh'] = {k: (mech.get(k, {}).get('assignment') or {}).get('primary') for k in ('1', '5')}
    return out


def chain_info(u):
    e = I_cp.get((u['dataset'], u['method'], u['opaque_id'], None if u['seed'] is None else str(u['seed'])))
    if not e:
        return None
    i, c = e
    if c.get('status') != 'OK' or not c.get('root_ranked', False):
        return {'trang_thai': c.get('status'), 'root_duoc_xep': c.get('root_ranked'),
                'nguon': ptr(RUNS + 'chain-position-002/units.json', '/%d' % i)}
    by = Counter(pos_group(a['class']) for a in c.get('above') or [])
    top = (c.get('top1_when_root_not_first') or [{}])[0]
    return {'so_ung_vien': c.get('n_candidates'), 'so_tren_root': c.get('n_above'), 'tren_root_theo_vi_tri': dict(by),
            'thuc_the_dung_dau': c.get('top_entity'), 'vi_tri_thuc_the_dung_dau': pos_group(top.get('class')) if top.get('class') else None,
            'hang_root': c.get('root_rank'),
            'so_ung_vien_phia_tren_root': sum(v for k, v in (c.get('candidates_by_class') or {}).items() if k in UP_CLASSES),
            'nguon': ptr(RUNS + 'chain-position-002/units.json', '/%d' % i)}


def error_text(u):
    p = os.path.join(IN, u['source']['path'])
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            r = json.load(f)
        return r.get('error')
    return None


UNITS = []
BYID = {}
INTERNAL = {}
for u in cat['units']:
    ds, m, oid, seed = u['dataset'], u['method'], u['opaque_id'], u['seed']
    row = {'unit_id': u['unit_id'], 'dataset': ds, 'method': m, 'opaque_id': oid, 'seed': seed, 'trang_thai_nguon': u['status'],
           'cell': u['cell'], 'vai_tro': u['roles'], 'nhom': u['groups'],
           'ban_ghi_dong_bang': {'path': u['source']['path'], 'sha256': u['source_sha256']},
           't028': t028_info(u), 'phat_lai': replay_exact(u), 'vi_tri_chuoi_goi': chain_info(u)}
    ci = CASE[(ds, oid)]
    row['root'] = ci['root']
    row['fault'] = ci['fault']
    row['trace_cua_ca'] = {k: v for k, v in ci.items() if not k.startswith('_') and k not in ('dataset', 'opaque_id', 'root', 'fault', 'cell')}
    det, sig = None, None
    if u['status'] != 'OK':
        det = {'ly_do_khong_OK': error_text(u)}
        sig = 'trang-thai:' + u['status']
    elif m == 'baro':
        det, sig = baro_detail(ds, oid)
    elif m == 'simplerca':
        det, sig = simplerca_detail(ds, oid)
    elif m == 'microrank_full':
        det, sig = microrank_detail(ds, oid)
    elif m == 'tracerca':
        det, sig = tracerca_detail(ds, oid)
    elif m == 'circa_ols_da':
        det, sig = circa_detail(oid)
    elif m == 'torai_B':
        det, sig = torai_detail(oid, seed)
    INTERNAL[u['unit_id']] = {k: v for k, v in det.items() if k.startswith('_')}
    row['chi_tiet'] = {k: v for k, v in det.items() if not k.startswith('_')}
    hang = row['t028']['hang']
    row['dung_hang_1'] = (u['status'] == 'OK' and hang[1] == 1)
    row['trong_5_hang_dau'] = (u['status'] == 'OK' and hang[1] is not None and hang[1] <= 5)
    row['duong_di'] = sig if not row['dung_hang_1'] else 'dung-hang-1|' + sig
    UNITS.append(row)
    BYID[u['unit_id']] = row

check('số đơn vị = 372', len(UNITS) == 372, len(UNITS))

bad = [r['unit_id'] for r in UNITS if 'LỆCH' in str(r['phat_lai'].get('trang_thai'))]
check('không đơn vị nào có phát lại lệch bản đóng băng', not bad, bad[:5])
h1 = Counter()
for r in UNITS:
    if r['dung_hang_1'] and (r['seed'] in (None, 0)):
        h1[(r['dataset'], r['method'])] += 1
exp_h1 = {('RE2-TT', 'baro'): 21, ('Nezha-OB', 'baro'): 8, ('RE2-TT', 'simplerca'): 25, ('Nezha-OB', 'simplerca'): 7, ('RE2-TT', 'microrank_full'): 2,
          ('RE2-TT', 'tracerca'): 21, ('Nezha-OB', 'tracerca'): 2, ('RE2-TT', 'circa_ols_da'): 16, ('RE2-TT', 'torai_B'): 26}
check('số ca root hạng 1 theo phương pháp trùng KQ9 (BARO 21+8, SimpleRCA 25+7, MicroRank 2+0, TraceRCA 21+2, CIRCA 16, TORAI B 26)',
      all(h1.get(k, 0) == v for k, v in exp_h1.items()) and h1.get(('Nezha-OB', 'microrank_full'), 0) == 0, {'%s|%s' % k: v for k, v in h1.items()})

# tự kiểm: hạng root ở bảng vị trí trùng T-028
bad = [r['unit_id'] for r in UNITS if r['vi_tri_chuoi_goi'] and r['vi_tri_chuoi_goi'].get('hang_root') is not None
       and list(r['vi_tri_chuoi_goi']['hang_root']) != list(r['t028']['hang'])]
check('hạng root ở bảng vị trí trùng T-028 ở mọi đơn vị OK có root được xếp', not bad, bad[:5])

bad = [r['unit_id'] for r in UNITS if r['vi_tri_chuoi_goi'] is None]
check('mọi đơn vị đều nối được với bảng vị trí trên chuỗi gọi', not bad, bad[:5])

# tự kiểm: số cặp theo phương pháp trùng KQ9/KQ11
pair_counts = Counter()
for r in UNITS:
    if r['trang_thai_nguon'] == 'OK' and r['method'] != 'torai_B':
        pair_counts[(r['dataset'], r['method'])] += len(r['chi_tiet'].get('tren_root') or r['chi_tiet'].get('tren_root_bang_DA') or [])
    if r['method'] == 'torai_B' and r['seed'] == 0:
        pair_counts[(r['dataset'], r['method'])] += len(r['chi_tiet'].get('tren_root') or [])
exp = {('RE2-TT', 'microrank_full'): 132, ('Nezha-OB', 'microrank_full'): 120, ('RE2-TT', 'tracerca'): 15, ('Nezha-OB', 'tracerca'): 75,
       ('RE2-TT', 'simplerca'): 20, ('Nezha-OB', 'simplerca'): 44, ('RE2-TT', 'baro'): 103, ('Nezha-OB', 'baro'): 59,
       ('RE2-TT', 'circa_ols_da'): 110, ('RE2-TT', 'torai_B'): 7}
check('số cặp (thực thể đứng trên root, root) trùng KQ9/KQ11', all(pair_counts.get(k) == v for k, v in exp.items()),
      {'%s|%s' % k: [pair_counts.get(k), v] for k, v in exp.items()})

# tự kiểm: số cặp "chủ yếu là chờ root" của TraceRCA trùng KQ11 mục 2.1 (4/4 và 9/15)
w = Counter()
for r in UNITS:
    if r['method'] == 'tracerca' and r['trang_thai_nguon'] == 'OK':
        for p in r['chi_tiet'].get('tren_root') or []:
            if p['vi_tri_chuoi_goi'] in ('phia_tren', 'hai_chieu') and p['chu_yeu_la_cho_root'] in (True, False):
                w[(r['dataset'], 'xet')] += 1
                w[(r['dataset'], 'dat')] += 1 if p['chu_yeu_la_cho_root'] else 0
check('TraceRCA: cặp phía trên xét được và đạt 50% trùng KQ11 (4/4; 9/15)',
      (w[('RE2-TT', 'dat')], w[('RE2-TT', 'xet')], w[('Nezha-OB', 'dat')], w[('Nezha-OB', 'xet')]) == (4, 4, 9, 15), dict(('%s|%s' % k, v) for k, v in w.items()))
w = Counter()
for r in UNITS:
    if r['method'] == 'microrank_full' and r['trang_thai_nguon'] == 'OK':
        lk = I_link.get((r['dataset'], 'microrank', r['opaque_id']))
        meas = bool(lk and lk[1].get('root_edge_measurable'))
        for p in r['chi_tiet'].get('tren_root') or []:
            if p['vi_tri_chuoi_goi'] in ('phia_tren', 'hai_chieu') and meas:
                w[(r['dataset'], 'xet')] += 1
                w[(r['dataset'], 'dat')] += 1 if (p['ty_le_trace_bat_thuong_gan_voi_root'] or 0) >= 0.5 else 0
check('MicroRank: cặp phía trên xét được và đạt 50% trùng KQ11 (0/10; 4/16)',
      (w[('RE2-TT', 'dat')], w[('RE2-TT', 'xet')], w[('Nezha-OB', 'dat')], w[('Nezha-OB', 'xet')]) == (0, 10, 4, 16), dict(('%s|%s' % k, v) for k, v in w.items()))

lv = Counter((c['dataset'], c['muc_do_duoc']) for c in CASE.values())
check('mức đo được: Nezha-OB 16 đo được; RE2-TT 21 một phần; 15 không đo được',
      lv[('Nezha-OB', 'đo được')] == 16 and lv[('RE2-TT', 'đo được một phần')] == 21 and
      lv[('Nezha-OB', 'không đo được')] + lv[('RE2-TT', 'không đo được')] == 15, {'%s|%s' % k: v for k, v in lv.items()})

# ---------------------------------------------------------------- cặp đối chứng và bảng nhóm
PAIRS = []
for i, p in enumerate(cat['counterpart_pairs']):
    wu = BYID[p['wrong_unit_id']]
    ctrls = []
    for c in p['control_classes']:
        cu = BYID.get(c['selected_correct_unit_id'])
        ctrls.append({'unit_id': c['selected_correct_unit_id'], 'cung_o': c['same_cell'], 'cung_kenh': c['same_channels'],
                      'cung_seed': c['same_seed_key'], 'duong_di': cu['duong_di'] if cu else None,
                      'hang_root': cu['t028']['hang'] if cu else None})
    ctrls.sort(key=lambda c: (not c['cung_o'], not c['cung_kenh'], c['unit_id']))
    PAIRS.append({'chi_so': i, 'don_vi_sai': p['wrong_unit_id'], 'k': p['k'], 'nhom': p['group_ids'],
                  'buoc_dang_xet': p['target_step'], 'duong_di_don_vi_sai': wu['duong_di'], 'hang_root_don_vi_sai': wu['t028']['hang'],
                  'so_lop_doi_chung': len(ctrls), 'doi_chung': ctrls,
                  'doi_chung_doc_truoc': ctrls[0]['unit_id'] if ctrls else None,
                  'ly_do_thieu_doi_chung': p['missing_control_reason'], 'pham_vi_thieu': p.get('scope_of_absence'),
                  'nguon': ptr(T32 + 'bao-phu-nhom.json', '/counterpart_pairs/%d' % i)})
check('số yêu cầu đối chứng = 301', len(PAIRS) == 301, len(PAIRS))
check('số yêu cầu không có đối chứng đúng = 110', sum(1 for p in PAIRS if not p['doi_chung']) == 110,
      sum(1 for p in PAIRS if not p['doi_chung']))
PAIR_BY = {(p['don_vi_sai'], p['k']): p for p in PAIRS}

GROUPS = []
READ = {}
for g in cat['groups']:
    wus = sorted(g['selected_wrong_unit_ids'])
    sigs = defaultdict(list)
    for uid in wus:
        sigs[BYID[uid]['duong_di']].append(uid)
    reads = []
    for s, lst in sorted(sigs.items()):
        uid = lst[0]
        pr = PAIR_BY.get((uid, g['k']))
        ctrl = pr['doi_chung_doc_truoc'] if pr else None
        cinfo = None
        if pr and pr['doi_chung']:
            c0 = pr['doi_chung'][0]
            cinfo = {'unit_id': c0['unit_id'], 'cung_o': c0['cung_o'], 'cung_kenh': c0['cung_kenh']}
        reads.append({'duong_di': s, 'so_don_vi_cung_duong_di': len(lst), 'don_vi_cung_duong_di': lst, 'don_vi_sai_doc': uid,
                      'doi_chung_doc': cinfo, 'ly_do_thieu_doi_chung': pr['ly_do_thieu_doi_chung'] if pr else None})
        READ.setdefault(uid, set()).add(g['group_id'])
        if ctrl:
            READ.setdefault(ctrl, set()).add(g['group_id'])
    GROUPS.append({'group_id': g['group_id'], 'dataset': g['dataset'], 'method': g['method'], 'k': g['k'], 'co_hoac_trang_thai': g['flag_or_status'],
                   'so_don_vi_sai': len(wus), 'so_ca_nguon': g['n_source_cases'], 'so_duong_di_khac_nhau': len(sigs),
                   'phan_bo_duong_di': {s: len(l) for s, l in sorted(sigs.items())}, 'doc_tay': reads,
                   'nguon': ptr(T32 + 'bao-phu-nhom.json', '/groups/%d' % cat['groups'].index(g))})
check('số nhóm = 52', len(GROUPS) == 52, len(GROUPS))

# bảng đếm theo phương pháp × dataset
SUMM = defaultdict(lambda: defaultdict(int))
for r in UNITS:
    k = '%s|%s' % (r['dataset'], r['method'])
    SUMM[k]['don_vi'] += 1
    SUMM[k]['OK'] += r['trang_thai_nguon'] == 'OK'
    SUMM[k]['khong_OK'] += r['trang_thai_nguon'] != 'OK'
    SUMM[k]['dung_hang_1'] += r['dung_hang_1']
    SUMM[k]['sai_hang_1_OK'] += (r['trang_thai_nguon'] == 'OK' and not r['dung_hang_1'])
    SUMM[k]['trong_5_hang_dau'] += r['trong_5_hang_dau']
SIGT = defaultdict(Counter)
for r in UNITS:
    SIGT['%s|%s' % (r['dataset'], r['method'])][r['duong_di']] += 1

W('doi-chieu-dung-sai.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'mo_ta': 'Bảng tự động theo đơn vị (ca × phương pháp × seed), phủ toàn bộ 372 đơn vị của danh mục đã khóa; cặp đối chứng theo điều kiện; bảng nhóm. Chỉ ghép file kết quả đã có.',
    'cach_doc': {'dung_hang_1': 'hạng lớn nhất của root (tính bi quan khi hòa) bằng 1',
                 'duong_di': 'chữ ký đường xử lý do script đặt từ các trường của bảng; dùng để chọn đơn vị đọc tay, không phải nguyên nhân',
                 'doi_chung': 'sắp theo cùng ô, rồi cùng kênh, rồi mã ca nhỏ nhất; không ghép theo kết quả',
                 'so_ca': 'mọi con số "bao nhiêu ca" trong báo cáo lấy từ bảng này hoặc từ file kết quả được trỏ'},
    'dem_theo_phuong_phap': {k: dict(v) for k, v in sorted(SUMM.items())},
    'duong_di_theo_phuong_phap': {k: dict(v) for k, v in sorted(SIGT.items())},
    'don_vi': UNITS, 'cap_doi_chung': PAIRS, 'nhom': GROUPS, 'nguon_da_dung': USED})

# ---------------------------------------------------------------- chuỗi bằng chứng
STEPS = {
    'baro': ['bảng metric theo cửa sổ F → lọc cột hằng, lấy giao cột hai đoạn',
             'median và IQR của đoạn nền → z = |x − median| / IQR, lấy lớn nhất theo cột',
             'điểm thực thể = z lớn nhất trong các cột của nó → xếp hạng'],
    'simplerca': ['metric, trace, log theo cửa sổ F',
                  'mỗi mẫu metric vượt mean + 3·std của nền là một phiếu; trace và log mỗi kênh 0 hoặc 1 phiếu',
                  'điểm = phiếu metric + phiếu trace + phiếu log → xếp hạng'],
    'microrank_full': ['bảng span theo cửa sổ F; mức nền theo thao tác',
                       'span vượt mean + 3·std mang cờ; trace có bất kỳ span mang cờ vào nhóm bất thường',
                       'PageRank trên hai nhóm trace → trọng số; đếm phủ theo thao tác',
                       'spectrum dstar2 → điểm thao tác → lấy lớn nhất theo dịch vụ → xếp hạng'],
    'tracerca': ['bảng span theo cửa sổ F; mean, std theo thao tác ở đoạn nền',
                 'span vượt mean + 3·std mang cờ: a (số span mang cờ của thao tác), n (số span sau mốc), H (tổng số span mang cờ)',
                 'điểm thao tác = 2a/(n + H), bỏ giá trị không hữu hạn → lấy lớn nhất theo dịch vụ → xếp hạng'],
    'circa_ols_da': ['bảng metric nhịp 1 giây; đồ thị metric dựng từ quan hệ gọi',
                     'hồi quy OLS từng nút theo nút cha trên 111 điểm trước mốc; chuẩn hóa phần dư 10 điểm cuối theo độ lệch chuẩn phần dư train (RHT)',
                     'DA: cộng điểm hậu duệ vào tổ tiên → khóa xếp hạng theo dịch vụ'],
    'torai_B': ['bốn bảng: metric, log (do ta dựng, nguồn B), độ trễ trace, lỗi trace',
                'mỗi nguồn: |z| lớn nhất sau mốc theo mean, std trước mốc, chia tổng nguồn → vectơ bốn số theo dịch vụ; severity là trung bình',
                'phân cụm Gaussian mixture; cụm xếp theo severity trung bình; trong cụm: RCD, không đủ thì theo severity'],
}
CH = []
for r in UNITS:
    m = r['method']
    c = {'unit_id': r['unit_id'], 'dataset': r['dataset'], 'method': m, 'opaque_id': r['opaque_id'], 'seed': r['seed'],
         'trang_thai_nguon': r['trang_thai_nguon'], 'cell': r['cell'], 'nhom': r['nhom'],
         'dau_vao': {'ban_ghi_dong_bang': r['ban_ghi_dong_bang'], 'phat_lai': r['phat_lai']},
         'cac_buoc_cua_phuong_phap': STEPS[m],
         'trung_gian_va_diem': r['chi_tiet'],
         'hang_root': r['t028']['hang'], 'co_T028': r['t028']['co'], 'nguon_hang_va_co': r['t028']['nguon'],
         'vi_tri_chuoi_goi': r['vi_tri_chuoi_goi'], 'duong_di': r['duong_di'],
         'trang_thai_dien_giai': 'xem doc-tay.md và nguyen-nhan-xep-hang.md; bảng này chỉ nối giá trị, không tự là kết luận cơ chế'}
    CH.append(c)
W('chuoi-bang-chung.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'mo_ta': 'Theo ca/phương pháp/cấu hình/seed: đầu vào → xử lý → trung gian → điểm/nhóm hòa/hạng, có đường dẫn và con trỏ nguồn. Thay bản initial-report-005 (lưu ở runs/tong-hop-phien-12-001/ban-truoc/).',
    'trang_thai': 'TỔNG HỢP PHIÊN 12; không tự đóng RQ2/G2',
    'so_don_vi': len(CH), 'don_vi': CH, 'nguon_da_dung': USED})

# ---------------------------------------------------------------- bảng caller/root (mọi đơn vị có cờ M5 nguồn)
M5 = []
M5_COUNT = defaultdict(lambda: defaultdict(int))
for u in cat['units']:
    ds, m, oid, seed = u['dataset'], u['method'], u['opaque_id'], u['seed']
    pe = I_proxy.get((ds, m, oid, 'single' if seed is None else str(seed)))
    row = BYID[u['unit_id']]
    key = '%s|%s' % (ds, m)
    M5_COUNT[key]['don_vi_trong_cohort'] += 1
    if u['status'] != 'OK':
        M5_COUNT[key]['khong_OK'] += 1
        continue
    if not row['dung_hang_1']:
        M5_COUNT[key]['sai_hang_1_OK'] += 1
    if not pe:
        M5_COUNT[key]['thieu_ban_ghi_proxy'] += 1
        continue
    pi, pr_ = pe
    b = pr_['M5_base_by_k']
    m5k = [k for k in ('1', '5') if (b.get(k) or {}).get('value') is True]
    na = [k for k in ('1', '5') if (b.get(k) or {}).get('availability') != 'available']
    if na and not m5k:
        M5_COUNT[key]['M5_khong_xac_dinh'] += 1
    if not m5k:
        continue
    M5_COUNT[key]['co_M5_o_k1_hoac_k5'] += 1
    det = row['chi_tiet']
    internal = INTERNAL[u['unit_id']]
    above = set(internal.get('_above') or [])
    still = internal.get('_still') or {}
    ci = CASE[(ds, oid)]
    e2r = ci['_edges_to_root']
    pairs_det = {p['entity']: p for p in (det.get('tren_root') or det.get('tren_root_bang_DA') or [])}
    callers = []
    for ob in pr_['observations']:
        if ob.get('role') == 'root':
            continue
        if not ob.get('certain_before_root'):
            continue
        e = ob['entity']
        edge = e2r.get('%s→%s' % (e, ci['root']))
        pd_ = pairs_det.get(e, {})
        tinh = {'dung_tren_root_trong_phat_lai': e in above,
                'con_tren_root_duoi_phep_doi': {k: ((e in v) if v is not None else None) for k, v in still.items()}}
        if m == 'tracerca':
            w_ = pd_.get('chu_yeu_la_cho_root')
            tinh['buoc_tao_uu_the'] = ('gắn cờ theo thời lượng cả span: xác nhận ở mức tính toán (từ 50% span mang cờ là span bao lời gọi chậm tới root)' if w_ is True
                                       else 'không xét được: cạnh tới root dưới 20 lời gọi ở một phía' if w_ == 'khong-xet-duoc'
                                       else 'chưa phân xử: dưới 50% span mang cờ là span chờ root' if w_ is False
                                       else 'không áp dụng: thực thể không nằm phía trên root trên đồ thị của ca')
            tinh['a'] = pd_.get('a'); tinh['n'] = pd_.get('n'); tinh['ty_le_span_cho_root'] = pd_.get('ty_le_span_mang_co_la_span_cho_root')
        elif m == 'microrank_full':
            s_ = pd_.get('ty_le_trace_bat_thuong_gan_voi_root')
            tinh['buoc_tao_uu_the'] = ('đếm phủ trên nhóm trace bất thường do bước chia của bản thư viện; phần lớn trace bất thường chứa thao tác này không gắn với root'
                                       if (s_ is not None and s_ < 0.5) else
                                       'từ 50% trace bất thường chứa thao tác này gắn với root' if s_ is not None else 'không xét được ở mức trace')
            tinh['ty_le_trace_gan_voi_root'] = s_
            tinh['trace_tu_mang_co'] = pd_.get('trace_bat_thuong_tu_mang_co'); tinh['trace_chi_ngu_canh'] = pd_.get('trace_bat_thuong_chi_ngu_canh')
        elif m == 'simplerca':
            tinh['buoc_tao_uu_the'] = ('phép cộng phiếu không cùng thang: riêng phiếu metric đã quyết định' if pd_.get('rieng_metric_du_quyet_dinh')
                                       else 'phiếu metric cùng với trace/log' if pd_ else 'thực thể không đứng trên root ở hạng nhỏ nhất')
            tinh['chenh_metric'] = pd_.get('chenh_metric'); tinh['loai_cot'] = pd_.get('loai_cot_nhieu_phieu_nhat'); tinh['nhom_xu_huong'] = pd_.get('nhom_xu_huong')
        elif m == 'baro':
            tinh['buoc_tao_uu_the'] = 'z theo median/IQR của cột riêng thực thể; BARO không nhận quan hệ gọi trong đầu vào'
            tinh['cot_thang'] = pd_.get('cot_thang'); tinh['loai_cot'] = pd_.get('loai_cot'); tinh['nhom_xu_huong'] = pd_.get('nhom_xu_huong')
        elif m == 'circa_ols_da':
            tinh['buoc_tao_uu_the'] = ('bước DA chuyển giá trị cực lớn từ hậu duệ lên: xác nhận ở mức tính toán' if pd_.get('mang_khoa_cuc_lon_sau_DA')
                                       else 'chưa phân xử: thực thể không mang khóa cực lớn' if pd_ else 'thực thể không đứng trên root ở bảng DA')
            tinh['mang_khoa_cuc_lon'] = pd_.get('mang_khoa_cuc_lon_sau_DA'); tinh['tren_root_o_bang_khong_DA'] = pd_.get('dung_tren_root_o_bang_khong_DA')
        elif m == 'torai_B':
            tinh['buoc_tao_uu_the'] = 'severity (trung bình bốn nguồn); nguồn chênh lớn nhất: %s' % pd_.get('nguon_chenh_lon_nhat')
            tinh['chenh_theo_nguon'] = pd_.get('chenh_theo_nguon')
        tin_hieu = {'P95_span_sau_moc_vuot_3_lan_nen_T028': ((ob.get('latency_up') or {}).get('3') or {}).get('value'),
                    'P95N': (ob.get('P95N') or {}).get('value'), 'P95A': (ob.get('P95A') or {}).get('value'),
                    'goi_truc_tiep_root': ob.get('direct_to_root'), 'khoang_cach_ngan_nhat': ob.get('shortest_distance')}
        cho = {'muc_do_duoc_cua_ca': ci['muc_do_duoc'],
               'canh_truc_tiep_toi_root_du_loi_goi': bool(edge),
               'ty_le_loi_goi_cham_sau_moc': (edge or {}).get('slow_share_after'),
               'ty_le_loi_goi_cham_o_nen': (edge or {}).get('slow_share_before'),
               'so_loi_goi_cham_sau_moc': (edge or {}).get('n_slow_after'),
               'phan_vuot_nam_trong_span_root': (edge or {}).get('slow_inside_callee_span'),
               'phan_vuot_nam_ngoai_span_root': (edge or {}).get('slow_outside_callee_span')}
        chua = []
        if ci['muc_do_duoc'] != 'đo được':
            chua.append('chưa xác lập "chờ" ở mức ngữ nghĩa ghi span: ' + ('thiếu công cụ ghi span' if ci['muc_do_duoc'] == 'đo được một phần' else 'không có cạnh đủ lời gọi tới root'))
        if not edge:
            chua.append('không có cạnh gọi trực tiếp đủ 20 lời gọi mỗi phía từ thực thể này tới root; nếu là phía trên gián tiếp thì chờ theo dây chuyền chưa đo riêng')
        chua.append('phần ngoài span của root (đường truyền, hàng đợi, xử lý quanh lời gọi) không tách được: mỗi lời gọi chỉ có hai span')
        callers.append({'thuc_the_phia_tren': e, 'bang_chung_tinh_toan': tinh, 'bang_chung_tin_hieu': tin_hieu,
                        'kha_nang_do_cho': cho, 'chua_biet': chua,
                        'nguon_T028': ob.get('source')})
    M5.append({'unit_id': u['unit_id'], 'dataset': ds, 'method': m, 'opaque_id': oid, 'seed': seed, 'cell': u['cell'], 'root': ci['root'],
               'co_M5_o_k': m5k, 'hang_root': row['t028']['hang'], 'duong_di': row['duong_di'],
               'so_thuc_the_phia_tren_chac_chan_truoc_root': len(callers), 'thuc_the': callers,
               'nguon_M5': ptr(T28 + 'caller-root-proxy.json', '/records/%d' % pi)})
check('số đơn vị có cờ M5 nguồn ở k=1 hoặc k=5 = 82 (80 ca × phương pháp, TORAI ba seed)', len(M5) == 82, len(M5))

# bảng đếm theo dataset/phương pháp/ô
by_cell = defaultdict(lambda: defaultdict(int))
for x in M5:
    by_cell['%s|%s|%s' % (x['dataset'], x['method'], x['cell'])]['don_vi_M5'] += 1
m5_evi = defaultdict(Counter)
for x in M5:
    for c in x['thuc_the']:
        m5_evi['%s|%s' % (x['dataset'], x['method'])][c['bang_chung_tinh_toan'].get('buoc_tao_uu_the', '-')] += 1
W('phan-xu-caller-root.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'mo_ta': 'Mọi đơn vị có cờ M5 ở nguồn T-028 (k=1 hoặc k=5); từng thực thể phía trên chắc chắn đứng trước root; ba nhóm bằng chứng độc lập và phần chưa biết. Không phải nhãn lan.',
    'hop_dong_dem': {'don_vi': 'ca × phương pháp × seed', 'cac_cot_bang_chung': 'chồng lấn, không cộng thành tỷ lệ nguyên nhân',
                     'N': 'ghi ngay bên số: cohort, số OK, số sai hạng 1 OK, số có M5'},
    'dem_theo_dataset_phuong_phap': {k: dict(v) for k, v in sorted(M5_COUNT.items())},
    'dem_theo_o': {k: dict(v) for k, v in sorted(by_cell.items())},
    'bang_chung_tinh_toan_theo_thuc_the': {k: dict(v) for k, v in sorted(m5_evi.items())},
    'don_vi_M5': M5, 'nguon_da_dung': USED})

# ---------------------------------------------------------------- can thiệp tính toán
AP = []
for i, c in enumerate(mr_ap['cases']):
    if c.get('status') != 'OK':
        AP.append({'dataset': c['dataset'], 'opaque_id': c['opaque_id'], 'trang_thai': c.get('status'), 'trang_thai_nguon': c.get('source_status'),
                   'ghi_chu': 'không đủ điều kiện A′: nguồn không OK, không có hai nhóm trace',
                   'nguon': ptr(RUNS + 'microrank-core-aprime-c1-002/summary.json', '/cases/%d' % i)})
        continue
    br = c['branches']
    AP.append({'dataset': c['dataset'], 'opaque_id': c['opaque_id'], 'cell': c['cell'], 'trang_thai': 'OK',
               'J0': {'W_native_trung_ban_dong_bang_tung_bit': c.get('sham_w_native_bit_exact'),
                      'so_trace_hai_nhom_khop': c.get('partition_counts_match'), 'dem_phu_khop': c.get('coverage_counts_match'),
                      'hang_root_trung_T028': c.get('self_check_native_rank_equals_t028'), 'dem': c.get('counts')},
               'W_native': {'root': br['w_native'].get('root'), 'so_tren_root': len(br['w_native'].get('above_root') or [])},
               'W_unit': {'root': br['w_unit'].get('root'), 'so_tren_root': len(br['w_unit'].get('above_root') or [])},
               'tac_dung_len_root': c.get('w_unit_effect_on_root'),
               'cap_tren_root': c.get('w_unit_pairs_above_root_native'),
               'nguon': ptr(RUNS + 'microrank-core-aprime-c1-002/summary.json', '/cases/%d' % i)})
REG = [
    {'ma': "A′", 'phuong_phap': 'MicroRank', 'buoc_doi': 'trọng số PageRank ở đầu vào spectrum đặt bằng 1', 'thiet_ke': 'SPEC mục A′; WHY-40',
     'ket_qua': RUNS + 'microrank-core-aprime-c1-002/summary.json', 'con_tro_tom_tat': '/summary/w_unit', 'dien_giai': 'ket-qua-phien-9.md mục 2'},
    {'ma': 'M-C1', 'phuong_phap': 'MicroRank', 'buoc_doi': 'đếm riêng (trace mà thao tác tự mang cờ) thay đếm phủ', 'thiet_ke': 'thiet-ke-phep-doi-001.md; WHY-44',
     'ket_qua': RUNS + 'microrank-core-aprime-c1-002/summary.json', 'con_tro_tom_tat': '/summary/c1', 'dien_giai': 'ket-qua-phien-9.md mục 2'},
    {'ma': 'M-D', 'phuong_phap': 'MicroRank', 'buoc_doi': 'cờ theo phần span chưa được span con phủ', 'thiet_ke': 'thiet-ke-phep-doi-001.md, -003.md; WHY-44',
     'ket_qua': RUNS + 'microrank-md-001/collect-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-10.md mục 2'},
    {'ma': 'chia trace mo15, mo1p50', 'phuong_phap': 'MicroRank', 'buoc_doi': 'bộ chia trace theo công thức của bài gốc, span đầu do ta quy ước', 'thiet_ke': 'thiet-ke-phep-doi-009.md; WHY-46, WHY-47',
     'ket_qua': RUNS + 'microrank-partition-001/collect-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-11.md mục 4'},
    {'ma': 'T-D', 'phuong_phap': 'TraceRCA', 'buoc_doi': 'cờ theo phần span chưa được span con phủ', 'thiet_ke': 'thiet-ke-phep-doi-001.md; WHY-44',
     'ket_qua': RUNS + 'tracerca-core-td-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-9.md mục 3'},
    {'ma': 'đổi công thức điểm (a/n, a)', 'phuong_phap': 'TraceRCA', 'buoc_doi': 'điểm thao tác 2a/(n+H) thay bằng a/n hoặc a', 'thiet_ke': 'thiet-ke-phep-doi-011.md mục 2; WHY-47',
     'ket_qua': RUNS + 'tracerca-score-contrast-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-11.md mục 8'},
    {'ma': 'bước xếp hạng của bài TraceRCA gốc (to_p, to_c, to_p3)', 'phuong_phap': 'TraceRCA (cài theo lời văn của bài; không phải mã tác giả)', 'buoc_doi': 'cả bước xếp hạng', 'thiet_ke': 'thiet-ke-phep-doi-011.md mục 3; WHY-47',
     'ket_qua': RUNS + 'tracerca-original-ranking-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-11.md mục 9'},
    {'ma': 'B-1', 'phuong_phap': 'BARO', 'buoc_doi': 'không lọc cột hằng', 'thiet_ke': 'thiet-ke-phep-doi-001.md; WHY-44',
     'ket_qua': RUNS + 'baro-b1-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-9.md mục 5'},
    {'ma': 'B-2', 'phuong_phap': 'BARO', 'buoc_doi': 'thang độ lệch chuẩn thay thang IQR', 'thiet_ke': 'thiet-ke-phep-doi-002.md; WHY-44',
     'ket_qua': RUNS + 'baro-b2-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-9.md mục 5'},
    {'ma': 'S-1', 'phuong_phap': 'SimpleRCA', 'buoc_doi': 'đếm theo cột thay đếm theo mẫu', 'thiet_ke': 'thiet-ke-phep-doi-002.md; WHY-44',
     'ket_qua': RUNS + 'simplerca-s1-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-9.md mục 4'},
    {'ma': 'K-1', 'phuong_phap': 'CIRCA', 'buoc_doi': 'so bản ghi có DA và không DA (không can thiệp)', 'thiet_ke': 'thiet-ke-phep-doi-001.md; WHY-44',
     'ket_qua': RUNS + 'circa-k1-002/k1.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-9.md mục 6'},
    {'ma': 'K-2', 'phuong_phap': 'CIRCA', 'buoc_doi': 'bỏ mọi cạnh của đồ thị metric', 'thiet_ke': 'thiet-ke-phep-doi-001.md mục 8, -003.md; WHY-44, WHY-45',
     'ket_qua': RUNS + 'circa-laptop-k2-001/collect-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-10.md mục 1'},
    {'ma': 'K-2 theo loại cạnh (k2x, k2s)', 'phuong_phap': 'CIRCA', 'buoc_doi': 'bỏ cạnh giữa hai dịch vụ, hoặc bỏ cạnh cùng dịch vụ', 'thiet_ke': 'thiet-ke-phep-doi-005.md; WHY-45',
     'ket_qua': RUNS + 'circa-laptop-k2-edges-001/collect-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-10.md mục 7'},
    {'ma': 'tl1, tl2', 'phuong_phap': 'TORAI B', 'buoc_doi': 'bỏ nguồn log, hoặc bỏ cột log nền không đổi', 'thiet_ke': 'thiet-ke-phep-doi-006.md; WHY-45',
     'ket_qua': RUNS + 'torai-log-contrast-001/summary.json', 'con_tro_tom_tat': '/summary', 'dien_giai': 'ket-qua-phien-10.md mục 8'},
]
EFFECT = []
for r in UNITS:
    if r['trang_thai_nguon'] != 'OK':
        continue
    d = r['chi_tiet']
    e = {'unit_id': r['unit_id'], 'hang_goc': r['t028']['hang']}
    for k in ('B1_khong_loc_cot_hang', 'B2_thang_do_lech_chuan', 'S1_dem_theo_cot', 'A_phay_trong_so_don_vi', 'C1_dem_rieng',
              'MD_co_theo_phan_chua_phu', 'TD_co_theo_phan_chua_phu'):
        if k in d:
            e[k] = {'tac_dung_len_root': d[k].get('tac_dung_len_root'), 'hang_root': d[k].get('hang_root')}
    if 'chia_theo_bai_goc' in d:
        e['chia_theo_bai_goc'] = {b: {'trang_thai': d['chia_theo_bai_goc'][b].get('trang_thai'), 'hang_root': d['chia_theo_bai_goc'][b].get('hang_root')} for b in ('mo15', 'mo1p50')}
        e['chia_theo_bai_goc']['dat_moc_90'] = d['chia_theo_bai_goc'].get('dat_moc_90')
    if 'doi_cong_thuc_diem' in d:
        e['doi_cong_thuc_diem'] = {k: v for k, v in d['doi_cong_thuc_diem'].items() if k != 'nguon'}
        e['buoc_xep_hang_bai_goc_to_p'] = {k: v for k, v in d['buoc_xep_hang_bai_goc_to_p'].items() if k != 'nguon'}
    if 'hang_root' in d and r['method'] == 'circa_ols_da':
        e['CIRCA'] = d['hang_root']
    if r['method'] == 'torai_B':
        e['tl1'] = d['bo_nguon_log_tl1']
        e['tl2'] = d['bo_cot_log_nen_khong_doi_tl2']
    EFFECT.append(e)
W('can-thiep-tinh-toan.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'A_phay': {'trang_thai': 'đã chọn trong thiết kế (Q-92), đã duyệt chạy (Q-93), đã chạy ở phiên 9',
               'kiem': {'W_native_trung_ban_dong_bang_tung_bit': sum(1 for a in AP if a.get('J0', {}).get('W_native_trung_ban_dong_bang_tung_bit')),
                        'so_ca_du_dieu_kien': sum(1 for a in AP if a['trang_thai'] == 'OK'),
                        'so_ca_khong_du_dieu_kien': sum(1 for a in AP if a['trang_thai'] != 'OK'),
                        'truong_hop_tu_dung_spectrum': mr_ap.get('spectrum_fixtures'),
                        'j0_manifest_sha256': mr_ap.get('j0_manifest_sha256')},
               'tom_tat': mr_ap['summary'].get('w_unit'),
               'gioi_han': 'A′ chỉ so toàn gói trọng số trên J0; không tách cạnh gọi, độ trung tâm hay prior; không phân xử dịch vụ gọi chờ root; không phải đối chứng "không đồ thị" của phương pháp mới.',
               'theo_ca': AP},
    'so_cac_phep_doi': REG,
    'tac_dung_theo_don_vi': EFFECT,
    'ghi_chu': 'Số của nhánh phép đổi đo tác động của một bước tính trên dev, không phải thành tích của một phương pháp. Mọi lượt, kể cả lượt hỏng, giữ trong runs/.',
    'nguon_da_dung': USED})

# ---------------------------------------------------------------- khả năng đo trace và độ phủ
KN = []
CV = []
for c in kndt_old['cases']:
    ds, oid = c['dataset'], c['opaque_id']
    ci = CASE[(ds, oid)]
    si, s = I_sem[(ds, oid)]
    edges = []
    for e in s.get('edges') or []:
        edges.append({k: e.get(k) for k in ('edge', 'n_before', 'n_after', 'C1_enough_calls', 'nested_share_before', 'gap_negative_share_before',
                                             'C2_interval_valid', 'C3_source_synchronous', 'source_pair_found', 'what_grew',
                                             'median_d_p_before_us', 'median_d_p_after_us')})
    n = dict(c)
    n['capability_tam_phien_8'] = n.pop('capability')
    n['classification_reason_tam_phien_8'] = n.pop('classification_reason')
    new = {'dataset': ds, 'opaque_id': oid, 'root': ci['root'], 'fault': ci['fault'],
           'muc_do_duoc': ci['muc_do_duoc'], 'giai_thich_muc': STRICT_NOTE[ci['muc_do_duoc']],
           'tieu_chi': {'C1_co_canh_toi_root_tu_20_loi_goi_moi_phia': any(e.get('C1_enough_calls') for e in edges),
                        'C2_gap_am_khong_qua_1pt_o_nen': any(e.get('C1_enough_calls') and e.get('C2_interval_valid') for e in edges),
                        'C3_moi_cho_goi_la_loi_goi_chan_o_moi_phien_ban_ung_vien': any(e.get('C1_enough_calls') and e.get('C3_source_synchronous') for e in edges),
                        'C4_gan_duoc_cong_cu_va_phien_ban_ghi_span': ds == 'Nezha-OB'},
           'ly_do_phien_10': s.get('reason'), 'canh_toi_root': edges,
           'ty_le_loi_goi_cham_toi_root_lon_nhat_sau_moc': ci['ty_le_loi_goi_cham_toi_root_lon_nhat_sau_moc'],
           'dau_vao_thieu': ([] if ci['muc_do_duoc'] == 'đo được' else
                             ['công cụ và phiên bản ghi span của bản triển khai RE2-TT (tác giả không công bố)'] if ci['muc_do_duoc'] == 'đo được một phần'
                             else ['lời gọi tới root trong trace (root không được gọi, hoặc dưới 20 lời gọi ở một phía)']),
           'khong_do_duoc_o_moi_ca': 'phần ngoài span của root gồm những gì (đường truyền, hàng đợi, xử lý quanh lời gọi): mỗi lời gọi chỉ có hai span',
           'nguon': ptr(RUNS + 'trace-semantics-002/semantics.json', '/cases/%d' % si),
           'kiem_ke_truong_tho_va_payload_phien_8': n}
    KN.append(new)
    ce = I_census.get((ds, oid))
    it_ = I_cint.get((ds, oid))
    pl = I_plc.get((ds, oid))
    cen = ce[1] if ce else {}
    st = (pl[1].get('structure') if pl else None) or {}
    CV.append({'dataset': ds, 'opaque_id': oid,
               'luoc_do_tho': c.get('raw_schema'), 'so_dong_co_gia_tri_theo_truong': c.get('raw_field_nonempty_row_counts'),
               'dem_trong_cua_so_F': c.get('F_counts'), 'noi_cha_con_trong_F': c.get('F_parent_resolution_rows'),
               'thong_ke_khoang_trong_F': c.get('F_interval_statistics'),
               'don_vi_va_toan_ven': c.get('raw_integrity_and_units'),
               'span_dau_va_span_mat_cha': {'so_span': cen.get('spans'), 'so_trace': cen.get('traces'), 'span_dau_khai_bao': cen.get('declared_root_spans'),
                                            'span_mat_cha': cen.get('orphan_spans'), 'trace_sau_moc': cen.get('after_traces'),
                                            'trace_mot_span_dau': cen.get('one_root_after_traces'), 'nen': cen.get('baseline'),
                                            'dat_moc_90': cen.get('gate'),
                                            'nguon': ptr(RUNS + 'trace-root-census-001/summary.json', '/cases/%d' % ce[0]) if ce else None},
               'gioi_han_cua_so': {'span_som_nhat_tru_moc_giay': st.get('earliest_start_minus_t_s'), 'span_muon_nhat_tru_moc_giay': st.get('latest_end_minus_t_s'),
                                   'nguon': ptr(RUNS + 'root-signal-placebo-003/summary.json', '/cases/%d/structure' % pl[0]) if pl else None},
               'khoang_loi_goi': {'trang_thai': (it_[1].get('status') if it_ else None),
                                  'nguon': ptr(RUNS + 'call-interval-001/summary.json', '/cases/%d' % it_[0]) if it_ else None},
               'canh_toi_root': new['canh_toi_root'],
               'ten_dai_luong': 'chồng lấn, lồng nhau, gap = span phía gọi − span phía được gọi; không đặt tên là thời gian chờ ở RE2-TT'})
lvc = defaultdict(Counter)
for k in KN:
    lvc[k['dataset']][k['muc_do_duoc']] += 1
W('kha-nang-do-trace.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'cau_hoi': 'Đo được việc dịch vụ gọi chờ root hay không, theo từng ca dev',
    'dinh_nghia_ba_muc': {'đo được': 'có quan hệ cùng yêu cầu và bằng chứng ngữ nghĩa, khoảng thời gian của chờ đồng bộ đã kiểm (C1–C4 đều đạt)',
                          'đo được một phần': 'có quan hệ và khoảng quan sát hợp lệ (C1–C3 đạt) nhưng thiếu bằng chứng để gọi khoảng ấy là chờ (C4 không đạt)',
                          'không đo được': 'thiếu quan hệ hoặc số lời gọi (C1 không đạt)'},
    'tieu_chi': {'C1': 'có cạnh gọi tới root với từ 20 lời gọi mỗi phía mốc', 'C2': 'ở nền, span phía được gọi dài hơn span phía gọi ở không quá 1% lời gọi',
                 'C3': 'mọi chỗ gọi của cặp dịch vụ trong mã nguồn là lời gọi chặn ở mọi phiên bản ứng viên',
                 'C4': 'gắn được công cụ và phiên bản ghi span với dataset (Nezha-OB: commit công khai duy nhất sinh đủ 55/55 tên span; RE2-TT: bảy tag ứng viên, công cụ ghi span không công bố)'},
    'theo_dataset': {ds: {'so_ca': sum(v.values()), 'theo_muc': dict(v)} for ds, v in lvc.items()},
    'gan_phien_ban': {'nguon': ptr(RUNS + 'source-fingerprint-001/fingerprint.json', ''), 'dien_giai': 'ket-qua-phien-10.md mục 6.1'},
    'gioi_han_suy_rong': 'Mức theo ca chỉ cho câu hỏi chờ root; không đánh giá chất lượng trace cho bài toán khác. 52 ca dev; chưa ca test nào.',
    'ca': KN, 'nguon_da_dung': USED})
W('coverage-trace.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'mo_ta': 'Lược đồ, kênh quan sát, nối cha–con, chồng lấn, span thiếu và giới hạn cửa sổ theo ca. Không đặt tên chỉ số nào là thời gian chờ khi chưa có căn cứ.',
    'tom_tat_theo_dataset': {'span_dau': census.get('summary'), 'khoang_loi_goi': cint.get('summary')},
    'ca': CV, 'nguon_da_dung': USED})

# ---------------------------------------------------------------- kế hoạch đọc tay và phiếu đọc


def short(uid):
    return uid.replace('|seed=single', '').replace('|', '__').replace('=', '')


def fmt(v, nd=3):
    if isinstance(v, float):
        if abs(v) >= 1e6 or (abs(v) < 1e-3 and v != 0):
            return '%.3g' % v
        return ('%.' + str(nd) + 'f') % v
    return str(v)


def sheet(uid):
    r = BYID[uid]
    d = r['chi_tiet']
    m = r['method']
    Ls = []
    Ls.append('ĐƠN VỊ %s' % uid)
    Ls.append('  ô %s | trạng thái nguồn %s | hạng root %s | cờ T-028 k1=%s k5=%s | nhóm sai: %s' % (
        r['cell'], r['trang_thai_nguon'], r['t028']['hang'], r['t028']['co']['1'], r['t028']['co']['5'], ', '.join(r['nhom']) or '(không)'))
    Ls.append('  đường đi: %s' % r['duong_di'])
    tc = r['trace_cua_ca']
    Ls.append('  trace của ca: mức đo được "%s"; tỷ lệ lời gọi chậm tới root lớn nhất sau mốc %s; vị trí trace root đứng đầu %s' % (
        tc['muc_do_duoc'], fmt(tc['ty_le_loi_goi_cham_toi_root_lon_nhat_sau_moc']), tc['vi_tri_trace_root_dung_dau']))
    vc = r['vi_tri_chuoi_goi'] or {}
    if vc.get('so_tren_root') is not None:
        Ls.append('  vị trí chuỗi gọi: %s thực thể trên root %s; đứng đầu %s (%s); ứng viên phía trên root %s/%s' % (
            vc.get('so_tren_root'), vc.get('tren_root_theo_vi_tri'), vc.get('thuc_the_dung_dau'), vc.get('vi_tri_thuc_the_dung_dau'),
            vc.get('so_ung_vien_phia_tren_root'), vc.get('so_ung_vien')))
    if r['trang_thai_nguon'] != 'OK':
        Ls.append('  lý do không OK: %s' % d.get('ly_do_khong_OK'))
        return Ls
    if m == 'baro':
        ro = d['root']
        Ls.append('  root: cột %s (%s) z=%s; IQR/median=%s; lệch/median=%s; %s thực thể, %s nhóm hòa' % (
            ro['cot_thang'], ro['loai_cot'], fmt(ro['z']), fmt(ro['IQR_tren_median']), fmt(ro['lech_tren_median']), ro['so_thuc_the'], ro['so_nhom_hoa']))
        for p in sorted(d['tren_root'], key=lambda x: -x['z'])[:6]:
            Ls.append('    trên root: %s | cột %s (%s) z=%s | IQR/median=%s lệch/median=%s | vị trí %s | xu hướng %s | lưu lượng đổi %s | còn trên root dưới B-2: %s' % (
                p['entity'], p['cot_thang'], p['loai_cot'], fmt(p['z']), fmt(p['IQR_tren_median']), fmt(p['lech_tren_median']),
                p['vi_tri_chuoi_goi'], p['nhom_xu_huong'], p['luu_luong_doi'], p['con_tren_root_duoi_B2']))
        if len(d['tren_root']) > 6:
            Ls.append('    … còn %d thực thể trên root' % (len(d['tren_root']) - 6))
        b1, b2 = d['B1_khong_loc_cot_hang'], d['B2_thang_do_lech_chuan']
        Ls.append('  B-1: %s (root thêm %s cột; cột tốt nhất là cột thêm: %s) | B-2: %s, hạng root %s, cặp mất %s, cặp mới %s' % (
            b1['tac_dung_len_root'], b1['cot_root_duoc_giu_them'], b1['cot_tot_nhat_cua_root_la_cot_them'],
            b2['tac_dung_len_root'], b2['hang_root'], b2['cap_mat'], b2['cap_moi']))
    elif m == 'simplerca':
        ro = d['root']
        Ls.append('  root: phiếu metric %s (cột có phiếu %s/%s) + trace %s + log %s = %s' % (
            ro['phieu_metric'], ro['cot_metric_co_phieu'], ro['cot_metric_dung_duoc'], ro['phieu_trace'], ro['phieu_log'], ro['diem']))
        for p in sorted(d['tren_root'], key=lambda x: -(x['diem'] or 0))[:6]:
            Ls.append('    trên root: %s | metric %s trace %s log %s = %s | chênh metric %s | cột nhiều phiếu nhất: %s (%s phiếu; một cột vượt tổng điểm root: %s) | vị trí %s | xu hướng %s | còn trên root dưới S-1: %s' % (
                p['entity'], p['phieu_metric'], p['phieu_trace'], p['phieu_log'], p['diem'], p['chenh_metric'], p['loai_cot_nhieu_phieu_nhat'],
                p['phieu_cot_nhieu_nhat'], p['mot_cot_vuot_tong_diem_root'], p['vi_tri_chuoi_goi'], p['nhom_xu_huong'], p['con_tren_root_duoi_S1']))
        if len(d['tren_root']) > 6:
            Ls.append('    … còn %d thực thể trên root' % (len(d['tren_root']) - 6))
        s1 = d['S1_dem_theo_cot']
        Ls.append('  riêng metric quyết định ở %s/%s cặp | S-1: %s, hạng root %s, %s nhóm hòa, cặp mất %s, cặp mới %s' % (
            d['so_cap_rieng_metric_quyet_dinh'], len(d['tren_root']), s1['tac_dung_len_root'], s1['hang_root'], s1['so_nhom_hoa'], s1['cap_mat'], s1['cap_moi']))
    elif m == 'microrank_full':
        c = d['dem']
        Ls.append('  chia trace: %s bất thường / %s bình thường (tỷ lệ %s); trace bất thường không có dịch vụ root %s; root tự mang cờ ở %s trace bất thường' % (
            c['trace_bat_thuong'], c['trace_binh_thuong'], fmt(c['ty_le_trace_bat_thuong']), c['trace_bat_thuong_khong_co_dich_vu_root'], c['trace_bat_thuong_root_tu_mang_co']))
        Ls.append('  root: thao tác %s điểm %s hạng %s' % (d['root']['thao_tac_cao_nhat'], fmt(d['root']['diem']), d['root']['hang']))
        for p in sorted(d['tren_root'], key=lambda x: x['hang'] or 99)[:5]:
            Ls.append('    trên root: %s (hạng %s) | %s | vị trí %s | tự mang cờ %s, chỉ ngữ cảnh %s | tỷ lệ trace gắn với root %s | còn trên root: %s' % (
                p['entity'], p['hang'], p['thao_tac_cao_nhat'], p['vi_tri_chuoi_goi'], p['trace_bat_thuong_tu_mang_co'], p['trace_bat_thuong_chi_ngu_canh'],
                fmt(p['ty_le_trace_bat_thuong_gan_voi_root']), p['con_tren_root']))
        if len(d['tren_root']) > 5:
            Ls.append('    … còn %d thực thể trên root' % (len(d['tren_root']) - 5))
        pt = d['chia_theo_bai_goc']
        Ls.append("  A′: %s → hạng %s | M-C1: %s → hạng %s | M-D: %s → hạng %s" % (
            d['A_phay_trong_so_don_vi']['tac_dung_len_root'], d['A_phay_trong_so_don_vi']['hang_root'], d['C1_dem_rieng']['tac_dung_len_root'],
            d['C1_dem_rieng']['hang_root'], d['MD_co_theo_phan_chua_phu']['tac_dung_len_root'], d['MD_co_theo_phan_chua_phu']['hang_root']))
        Ls.append('  chia theo bài gốc (đạt mốc 90%%: %s): mo15 %s hạng %s, trên root %s, đầu bảng %s, tỷ lệ trace bất thường có root %s | mo1p50 %s hạng %s' % (
            pt['dat_moc_90'], pt['mo15'].get('trang_thai'), pt['mo15'].get('hang_root'), pt['mo15'].get('so_tren_root'), pt['mo15'].get('dau_bang'),
            fmt(pt['mo15'].get('ty_le_trace_bat_thuong_co_root')), pt['mo1p50'].get('trang_thai'), pt['mo1p50'].get('hang_root')))
    elif m == 'tracerca':
        if 'root' not in d:
            Ls.append('  phát lại: %s' % d)
            return Ls
        ro = d['root']
        Ls.append('  H=%s; cạnh tới root xét được: %s; root được xếp: %s' % (d['H'], d['canh_toi_root_xet_duoc'], d['root_duoc_xep']))
        Ls.append('  root: %s a=%s n=%s (a/n=%s) điểm %s hạng %s' % (ro['thao_tac_cao_nhat'], ro['a'], ro['n'], fmt(ro['ty_le_a_tren_n']), fmt(ro['diem'], 4), ro['hang']))
        for p in sorted(d['tren_root'], key=lambda x: -(x['diem'] or 0))[:6]:
            Ls.append('    trên root: %s | %s | a=%s n=%s (a/n=%s) điểm %s | vị trí %s (%s) | tỷ lệ span mang cờ là span chờ root %s → chủ yếu chờ root: %s | còn trên root: %s' % (
                p['entity'], p['thao_tac_cao_nhat'], p['a'], p['n'], fmt(p['ty_le_a_tren_n']), fmt(p['diem'], 4), p['vi_tri_chuoi_goi'], p['lop'],
                fmt(p['ty_le_span_mang_co_la_span_cho_root']), p['chu_yeu_la_cho_root'], p['con_tren_root']))
        if len(d['tren_root']) > 6:
            Ls.append('    … còn %d thực thể trên root' % (len(d['tren_root']) - 6))
        ob = d['buoc_xep_hang_bai_goc_to_p']
        Ls.append('  T-D: %s → hạng %s | xếp theo a/n: hạng %s; a/n từ 20 span: %s; theo a: %s | bước của bài gốc (to_p): %s, đặc trưng hữu ích %s, root điểm dương %s, hạng %s, đầu bảng %s' % (
            d['TD_co_theo_phan_chua_phu']['tac_dung_len_root'], d['TD_co_theo_phan_chua_phu']['hang_root'], d['doi_cong_thuc_diem']['ty_le_a_tren_n'],
            d['doi_cong_thuc_diem']['ty_le_tu_20_span'], d['doi_cong_thuc_diem']['so_tuyet_doi_a'], ob['trang_thai'], ob['dac_trung_huu_ich'],
            ob['root_diem_duong'], ob['hang_root'], ob['dau_bang']))
    elif m == 'circa_ols_da':
        Ls.append('  có nút cực lớn: %s %s' % (d['co_nut_cuc_lon'], [(h['nut'], 'cha=%s' % h['so_cha'], 'std_y_train=%s' % fmt(h['y_train_do_lech_chuan']), 'rht=%s' % fmt(h['rht']), 'rht_không_cạnh=%s' % fmt(h['rht_khong_canh'])) for h in d['nut_cuc_lon']]))
        Ls.append('  root: cột %s | hạng RHT %s, DA %s (DA: %s), không cạnh %s, k2x %s, k2s %s | root mang khóa cực lớn sau DA: %s %s' % (
            d['cot_tot_nhat_cua_root'], d['hang_root']['RHT'], d['hang_root']['DA'], d['tac_dung_DA_len_root'], d['hang_root']['K2_khong_canh_RHT'],
            d['hang_root']['k2x_chi_canh_cung_dich_vu'], d['hang_root']['k2s_chi_canh_khac_dich_vu'], d['root_mang_khoa_cuc_lon_sau_DA'], d['nguon_khoa_cuc_lon_cua_root']))
        for p in d['tren_root_bang_DA'][:7]:
            Ls.append('    trên root (bảng DA): %s | gọi trực tiếp root %s | mang khóa cực lớn %s | cũng trên root ở bảng không DA %s | còn trên root khi bỏ cạnh %s' % (
                p['entity'], p['goi_truc_tiep_root'], p['mang_khoa_cuc_lon_sau_DA'], p['dung_tren_root_o_bang_khong_DA'], p['con_tren_root_khi_bo_canh_bang_RHT']))
        if len(d['tren_root_bang_DA']) > 7:
            Ls.append('    … còn %d thực thể trên root' % (len(d['tren_root_bang_DA']) - 7))
    elif m == 'torai_B':
        ro = d['root']
        Ls.append('  root: vectơ %s severity %s hạng severity %s; cụm %s dịch vụ, nhánh %s; hạng %s' % (
            {k: fmt(v) for k, v in (ro['vecto_4_nguon'] or {}).items()}, fmt(ro['severity']), ro['hang_severity'], ro['kich_thuoc_cum'], ro['nhanh_xep_trong_cum'], ro['hang']))
        for p in d['tren_root']:
            Ls.append('    trên root: %s severity %s (chênh %s) | cùng cụm %s | chênh theo nguồn %s | lớn nhất: %s' % (
                p['entity'], fmt(p['severity']), fmt(p['chenh_severity']), p['cung_cum_voi_root'], {k: fmt(v) for k, v in (p['chenh_theo_nguon'] or {}).items()}, p['nguon_chenh_lon_nhat']))
        Ls.append('  mất hạng ở: %s' % d['mat_hang_o_dau'])
        Ls.append('  tl2 (bỏ cột log nền không đổi): %s | tl1 (bỏ nguồn log): %s' % (d['bo_cot_log_nen_khong_doi_tl2'], d['bo_nguon_log_tl1']))
    return Ls


PLAN = []
ALL_READ = sorted(READ)
for uid in ALL_READ:
    lines = sheet(uid)
    with open(os.path.join(OUT, 'phieu-doc', short(uid) + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    PLAN.append({'unit_id': uid, 'phieu': 'phieu-doc/' + short(uid) + '.txt', 'phu_nhom': sorted(READ[uid]),
                 'vai_tro_doc': 'sai' if not BYID[uid]['dung_hang_1'] or BYID[uid]['trang_thai_nguon'] != 'OK' else 'đối chứng đúng'})
W('ke-hoach-doc-tay.json', {
    'task': 'T-032', 'schema': 'tong-hop-phien-12-v1',
    'quy_tac': ['mỗi nhóm trong 52 nhóm: với mỗi đường đi khác nhau trong các đơn vị sai của nhóm, đọc đơn vị có mã nhỏ nhất',
                'đối chứng: của chính đơn vị sai đó ở đúng k của nhóm; ưu tiên cùng ô, rồi cùng kênh, rồi mã nhỏ nhất',
                'không ghép theo chênh điểm, vị trí dịch vụ gọi hay kết quả phép đổi',
                'đường đi là chữ ký do script đặt từ bảng; đơn vị cùng đường đi không được đếm là đã đọc tay'],
    'so_don_vi_doc_tay_khong_trung': len(ALL_READ),
    'so_don_vi_sai_doc': sum(1 for p in PLAN if p['vai_tro_doc'] == 'sai'),
    'so_doi_chung_doc': sum(1 for p in PLAN if p['vai_tro_doc'] != 'sai'),
    'nhom': GROUPS, 'don_vi_doc': PLAN})

with open(os.path.join(OUT, 'phieu-doc-tat-ca.txt'), 'w', encoding='utf-8', newline='\n') as f:
    for g in GROUPS:
        f.write('=' * 100 + '\nNHÓM %s — %s đơn vị sai, %s đường đi: %s\n' % (g['group_id'], g['so_don_vi_sai'], g['so_duong_di_khac_nhau'], g['phan_bo_duong_di']))
        for rd in g['doc_tay']:
            f.write('- đọc sai: %s [đường đi %s; cùng đường đi %d đơn vị] | đối chứng: %s%s\n' % (
                rd['don_vi_sai_doc'], rd['duong_di'], rd['so_don_vi_cung_duong_di'],
                (rd['doi_chung_doc'] or {}).get('unit_id'), '' if rd['doi_chung_doc'] else ' (thiếu: %s)' % rd['ly_do_thieu_doi_chung']))

W('tu-kiem.json', {'checks': CHECKS, 'all_pass': all(c['pass'] for c in CHECKS)})
for c in CHECKS:
    print(('PASS ' if c['pass'] else 'FAIL ') + c['name'], '' if c['pass'] else c['detail'])
print('groups', len(GROUPS), 'reading units', len(ALL_READ), 'wrong', sum(1 for p in PLAN if p['vai_tro_doc'] == 'sai'))
print('sig table', json.dumps({k: dict(v) for k, v in sorted(SIGT.items())}, ensure_ascii=False))

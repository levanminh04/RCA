"""T-045 D1 (không nhãn): đối chiếu số trung gian của bản ghi M1 với KS-16 (`results/T-043/ks16/dem-khong-nhan.json`)
từng ca: span sau bỏ lặp, bản lặp bỏ, span mồ côi, span gốc, span bọc, con vượt biên cha, số đơn vị (thao tác,
metric, log) và đủ hỗ trợ, chế độ cổng, số dòng log, F, H, T và số ô theo trạng thái (trace, log; metric RE2-TT).

Định nghĩa khác đã biết (không tính là lệch):
- Metric lớp "tỷ lệ thành công" chỉ chấm khi E3 bật (hop-dong.json#/kenh/lop_huong); KS-16 đếm mọi cột. So số cột M1
  với số cột KS-16 trừ cột tỷ lệ thành công.
- Nezha-OB: M1 tính quan sát theo từng nguồn metric (Đ19); KS-16 tính một "metric" (marker). Chỉ báo, không so.
- Trường quan sát (F, H, T, ô): `dem-khong-nhan.json` là bản KS-16 v1 (khe giữa file phút Nezha-OB không tách); M1
  cài luật F phương án (a) của Q-207 (khe giữa file là OPEN), tức bản v1.1 `ks16/runs/pha1-002/dem-khong-nhan.json`
  (báo cáo T-043 dòng 28–29, 87). So cả hai; kết luận theo v1.1 (LOG phiên 1, Đ-12).
- Nezha-OB: adapter đưa span về µs nguyên (`start_us`, `duration_us`), còn F tính từ mốc ns của file; H của trace
  có thể lệch tới khoảng 2 µs. Ghi riêng `khop_trong_2us`.
Chạy: $PY -B results/T-045/scripts/d1_doi_chieu_ks16.py <lượt R0 seed 0> [<lượt K-E1> <lượt K-E2>] --ra <json>
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1 import kenh as kenh_mod  # noqa: E402

TOL_S = 1e-6
TOL_US_CAT = 2e-6 + 1e-9  # cắt mốc span về µs


def doc_ban_ghi(d, chi_cau_hinh=None):
    """Đọc theo dòng (tệp khối K khoảng 0,9 GB); chi_cau_hinh: chỉ giữ các config_id này."""
    d = Path(d)
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    out = []
    with open(d / meta['tep'], encoding='utf-8') as f:
        for x in f:
            if x.strip():
                r = json.loads(x)
                if chi_cau_hinh is None or r['config_id'] in chi_cau_hinh:
                    out.append(r)
    return out


def ho_so(hop_dong, ds):
    from m1 import adapter
    return adapter.ho_so_nguon(hop_dong, ds)


def dem_pv(rec, tien_to):
    pv = [u for u in (rec.get('extra') or {}).get('don_vi_phan_vi') or [] if u['ma'].startswith(tien_to)]
    ok = [u for u in pv if u['trang_thai'] == 'OK']
    return {'tong': len(pv), 'OK': len(ok),
            'chinh_xac': sum(1 for u in ok if u.get('cach_cong_len') == 'chinh_xac'),
            'xap_xi': sum(1 for u in ok if u.get('cach_cong_len') == 'xap_xi')}


def so(lech, ten, m1, ks):
    lech[ten] = {'M1': m1, 'KS16': ks, 'khop': m1 == ks}


def so_s(lech, ten, m1_ns, ks_s):
    m1_s = None if m1_ns is None else m1_ns / 1e9
    d = None if (m1_s is None or ks_s is None) else abs(m1_s - ks_s)
    lech[ten] = {'M1_s': m1_s, 'KS16_s': ks_s, 'lech_s': d, 'khop': d is not None and d <= TOL_S,
                 'khop_trong_2us': d is not None and d <= TOL_US_CAT}


def doi_chieu(rec, ks, hop_dong, t_s, ks11=None):
    ds = ks['dataset']
    out = {}
    sp = (rec.get('diagnostics') or {}).get('span') or {}
    tr = ks['trace']
    so(out, 'span_sau_bo_lap', sp.get('so_span'), tr['n_spans'])
    so(out, 'ban_lap_bo', sp.get('bo_lap'), ks['dedupe']['identical_dropped'])
    so(out, 'span_mo_coi', sp.get('mo_coi'), tr['orphans'])
    so(out, 'span_goc', sp.get('goc'), tr['root_spans'])
    so(out, 'span_boc', sp.get('span_boc'), tr['wrap_strict'])
    so(out, 'con_vuot_bien_cha', sp.get('con_vuot_bien_cha'), tr['children_beyond_parent_1ms'])
    op = dem_pv(rec, 'op|')
    u = ks['units']
    so(out, 'thao_tac_E1_tat_tong', op['tong'], u['ops'])
    so(out, 'thao_tac_E1_tat_du_ho_tro', op['OK'], u['op_E1_tat']['du_ho_tro'])
    so(out, 'thao_tac_E1_tat_chinh_xac', op['chinh_xac'], u['op_E1_tat']['exact'])
    so(out, 'thao_tac_E1_tat_xap_xi', op['xap_xi'], u['op_E1_tat']['asymptotic'])
    # metric: bỏ cột lớp "tỷ lệ thành công" (chỉ chấm khi E3 bật)
    hs = ho_so(hop_dong, ds)
    rows = [r for r in ks['metric_rows']
            if kenh_mod.huong_cham('metric', False, kenh_mod.lop_metric(r[0], hs) or 'tài nguyên')
            and kenh_mod.lop_metric(r[0], hs) is not None]
    khong_lop = [r[0] for r in ks['metric_rows'] if kenh_mod.lop_metric(r[0], hs) is None]
    du = [r for r in rows if r[1] >= 5 and r[2] >= 5]
    mt = dem_pv(rec, 'metric|')
    so(out, 'metric_cot_cham_R0', mt['tong'], len(rows))
    so(out, 'metric_du_ho_tro', mt['OK'], len(du))
    so(out, 'metric_chinh_xac', mt['chinh_xac'], sum(1 for r in du if r[1] + r[2] <= 100))
    so(out, 'metric_xap_xi', mt['xap_xi'], sum(1 for r in du if r[1] + r[2] > 100))
    out['metric_cot_khong_co_lop'] = khong_lop
    # log theo thực thể
    tk = ((rec.get('extra') or {}).get('thong_ke_log') or {}).get('theo_thuc_the') or {}
    m1_log = {k: sum(v[p][f] for v in tk.values()) for k, (p, f) in
              {'dong_N': ('N', 'dong'), 'dong_A': ('A', 'dong'), 'loi_N': ('N', 'loi'), 'loi_A': ('A', 'loi'),
               'unknown_N': ('N', 'unknown'), 'unknown_A': ('A', 'unknown')}.items()}
    lg = ks.get('log') or {}
    so(out, 'log_dong_N', m1_log['dong_N'], lg.get('rows_N'))
    so(out, 'log_dong_A', m1_log['dong_A'], lg.get('rows_A'))
    so(out, 'log_loi_N', m1_log['loi_N'], lg.get('error_rows_N'))
    so(out, 'log_loi_A', m1_log['loi_A'], lg.get('error_rows_A'))
    if ds == 'Nezha-OB':
        so(out, 'log_unknown_N', m1_log['unknown_N'], lg.get('unknown_rows_N'))
        so(out, 'log_unknown_A', m1_log['unknown_A'], lg.get('unknown_rows_A'))
    dv_log = [x for x in ((rec.get('worlds') or {}).get('P') or {}).get('don_vi_dem') or [] if x['ma'].startswith('log|')]
    so(out, 'don_vi_log_loi_du_10_P', sum(1 for x in dv_log if x['trang_thai'] == 'OK'), lg.get('don_vi_dem_log_loi_du_10'))
    # quan sát: F, H, T, ô
    cov = rec.get('coverage') or {}
    nguon = ['trace', 'log'] + (['metric'] if ds == 'RE2-TT' else [])
    for n in nguon:
        q = cov.get(n) or {}
        k = ((ks11 or ks).get('quan_sat') or {}).get(n) or {}
        if q.get('trang_thai') != 'OK':
            out[f'{n}_trang_thai'] = {'M1': q.get('trang_thai'), 'khop': False}
            continue
        for p in ('N', 'A'):
            so_s(out, f'{n}_T_chac_{p}', q['T_chac'][p], k['T'][p]['chac'])
            so_s(out, f'{n}_T_max_{p}', q['T_max'][p], k['T'][p]['max'])
            o_m1 = {kk: v for kk, v in q['o'][p].items() if v}
            o_ks = {kk: v for kk, v in k['o'][p].items() if v}
            so(out, f'{n}_o_{p}', o_m1, o_ks)
        t_ns = int(round(t_s * 1e9))
        for ten, kk in (('F', 'F_rel_t'), ('H', 'H_rel_t')):
            m = q.get(ten)
            m_rel = None if m is None else [(m[0] - t_ns) / 1e9, (m[1] - t_ns) / 1e9]
            kv = k.get(kk)
            if kv and isinstance(kv[0], list):  # v1.1: F là danh sách khoảng theo file; so bao [đầu, cuối]
                kv = [kv[0][0], kv[-1][1]]
            out[f'{n}_{ten}_rel_t'] = {'M1': m_rel, 'KS16': kv, 'r_KS16': k.get('r'),
                                      'khop_trong_r': (m_rel is not None and kv is not None and
                                                       abs(m_rel[0] - kv[0]) <= TOL_S and
                                                       abs(m_rel[1] - kv[1]) <= max(TOL_S, (k.get('r') or 0) + TOL_S))}
    if ds == 'Nezha-OB':
        kq = (ks.get('quan_sat') or {}).get('metric') or {}
        out['metric_Nezha_chi_bao'] = {
            'KS16_T_chac': {p: kq.get('T', {}).get(p, {}).get('chac') for p in ('N', 'A')},
            'M1_T_chac_theo_nguon': {n: {p: q['T_chac'][p] / 1e9 for p in ('N', 'A')}
                                     for n, q in sorted(cov.items()) if n.startswith('metric:') and q.get('trang_thai') == 'OK'}}
    return out


def doi_chieu_K(rec_E1, rec_E2, ks):
    out = {}
    u = ks['units']
    if rec_E1 is not None:
        op = dem_pv(rec_E1, 'op|')
        # E1 bật bỏ span bọc khỏi mẫu: thao tác chỉ gồm span bọc không còn đơn vị (op_rows cột 4, 5 là n_N, n_A khi E1 bật)
        so(out, 'thao_tac_E1_bat_tong', op['tong'], sum(1 for r in ks['op_rows'] if r[4] + r[5] > 0))
        so(out, 'thao_tac_E1_bat_du_ho_tro', op['OK'], u['op_E1_bat']['du_ho_tro'])
        so(out, 'thao_tac_E1_bat_chinh_xac', op['chinh_xac'], u['op_E1_bat']['exact'])
        so(out, 'thao_tac_E1_bat_xap_xi', op['xap_xi'], u['op_E1_bat']['asymptotic'])
    if rec_E2 is not None:
        cn = dem_pv(rec_E2, 'canh|')
        so(out, 'canh_E2_tong', cn['tong'], u['edges_wrapped'])
        so(out, 'canh_E2_du_ho_tro', cn['OK'], u['canh_E2']['du_ho_tro'])
        so(out, 'canh_E2_chinh_xac', cn['chinh_xac'], u['canh_E2']['exact'])
        so(out, 'canh_E2_xap_xi', cn['xap_xi'], u['canh_E2']['asymptotic'])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('luot_R0')
    ap.add_argument('--luot-K', default=None, help='lượt chứa K-E1 và K-E2 (tùy chọn)')
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ks16 = json.loads((ROOT / 'results/T-043/ks16/dem-khong-nhan.json').read_text(encoding='utf-8'))
    ks_cua = {c['opaque_id']: c for c in ks16['cases']}
    ks11 = {c['opaque_id']: c for c in json.loads((ROOT / 'results/T-043/ks16/runs/pha1-002/dem-khong-nhan.json')
                                                 .read_text(encoding='utf-8'))['cases']}
    hop_dong = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
    recK = {}
    if a.luot_K:
        for r in doc_ban_ghi(a.luot_K, {'K-E1', 'K-E2'}):
            recK[(r['config_id'], r['opaque_id'])] = r
    kq = {'nguon_KS16': 'results/T-043/ks16/dem-khong-nhan.json', 'luot_R0': a.luot_R0, 'luot_K': a.luot_K, 'ca': {}}
    for r in doc_ban_ghi(a.luot_R0):
        ks = ks_cua[r['opaque_id']]
        x = {'status': r['status']}
        if r['status'] in ('OK', 'NO_EVIDENCE'):
            x.update(doi_chieu(r, ks, hop_dong, ks['t']))
            v11 = doi_chieu(r, ks, hop_dong, ks['t'], ks11=ks11[r['opaque_id']])
            for k, v in v11.items():
                if k.startswith(('trace_', 'log_T', 'log_o', 'log_F', 'log_H', 'metric_T', 'metric_o', 'metric_F', 'metric_H')):
                    x[k + '__v11'] = v
        if a.luot_K:
            x.update(doi_chieu_K(recK.get(('K-E1', r['opaque_id'])), recK.get(('K-E2', r['opaque_id'])), ks))
        # luật F phương án (a), Q-207: khe giữa file là OPEN → T^chắc như v1.1 (khe loại ở P), T^max như v1 (khe tính ở
        # S_lo, S_hi), trạng thái ô như v1.1
        if r['status'] in ('OK', 'NO_EVIDENCE'):
            la = {}
            for n in ('trace', 'log'):
                for p_ in ('N', 'A'):
                    la[f'{n}_T_chac_{p_}_nhu_v11'] = x.get(f'{n}_T_chac_{p_}__v11', {}).get('khop_trong_2us')
                    la[f'{n}_T_max_{p_}_nhu_v1'] = x.get(f'{n}_T_max_{p_}', {}).get('khop_trong_2us')
                    la[f'{n}_o_{p_}_nhu_v11'] = x.get(f'{n}_o_{p_}__v11', {}).get('khop')
            x['luat_F_a_Q207'] = {'dat': all(v is True for v in la.values()), 'chi_tiet': la}
        x['lech'] = sorted(k for k, v in x.items() if isinstance(v, dict) and v.get('khop') is False
                           and k != 'luat_F_a_Q207')
        x['lech_v11_ngoai_2us'] = sorted(k for k, v in x.items() if k.endswith('__v11') and isinstance(v, dict)
                                         and v.get('khop') is False and not v.get('khop_trong_2us'))
        kq['ca'][r['opaque_id']] = dict(x, dataset=ks['dataset'])
    tong = {}
    for oid, x in kq['ca'].items():
        for k in x['lech']:
            tong.setdefault(k, []).append(oid)
    kq['tong_hop'] = {'so_ca': len(kq['ca']), 'so_ca_co_lech': sum(1 for x in kq['ca'].values() if x['lech']),
                      'lech_theo_dai_luong': {k: len(v) for k, v in sorted(tong.items())},
                      'so_ca_dat_luat_F_a_Q207': sum(1 for x in kq['ca'].values() if (x.get('luat_F_a_Q207') or {}).get('dat')),
                      'so_ca_lech_v11_ngoai_2us': sum(1 for x in kq['ca'].values() if x.get('lech_v11_ngoai_2us')),
                      'lech_v11_ngoai_2us': sorted({k for x in kq['ca'].values() for k in x.get('lech_v11_ngoai_2us', [])}),
                      'ca_theo_dai_luong': {k: v for k, v in sorted(tong.items())}}
    Path(a.ra).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(kq['tong_hop'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

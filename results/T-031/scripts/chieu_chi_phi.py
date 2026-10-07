"""T-031 bước 7: tổng hợp số đo và chiếu chi phí 30 ca theo cách khai trước (LOG T-031 10:42). Không dùng nhãn.

- Đo thật 30 ca: MicroRank (bước 2), CIRCA SVR (bước 3), TORAI (bước 4; phần đã chạy).
- Pilot 3 ca (BARO, SimpleRCA, TraceRCA, N-Sigma chính và đối chứng): wall mỗi lượt nội suy tuyến tính từng đoạn
  theo yếu tố đầu qua 3 ca pilot, cộng trên 30 ca; kèm 30 × min và 30 × max. "Chưa kiểm".
- BOCPD tiền tố: p, chiếu 1.441 điểm theo T² và T^p; chiếu 30 ca theo d² và d^q; thứ yếu × (1441/300)^(p−2).
  Số mũ trong lượt từ tiến độ (log thời gian tích lũy theo log số bước, nửa sau lượt). "Chưa kiểm".

python chieu_chi_phi.py <cau-hinh.json>   (đường dẫn các tóm tắt, xem ví dụ trong LOG)
"""
import json
import math
import sys

import numpy as np

import chung

T_DU = 1441


def nap(p):
    return json.loads(open(p, encoding='utf-8').read())


def walls(tom, key='opaque_id'):
    out = {}
    for r in nap(tom)['luot']:
        w = (r.get('cost') or {}).get('wall_s')
        if w is not None:
            out.setdefault(r[key], []).append(w)
    return out


def noi_suy(pilot_w, yeu_to, cot):
    xs = sorted((yeu_to[o][cot], float(np.mean(w))) for o, w in pilot_w.items())
    x, y = np.array([a for a, _ in xs], float), np.array([b for _, b in xs], float)
    tong = float(sum(np.interp(r[cot], x, y) for r in yeu_to.values()))
    return {'diem_pilot': [[a, b] for a, b in xs], 'yeu_to': cot, 'tong_30_ca_s': round(tong, 1),
            'can_30_min_s': round(30 * float(y.min()), 1), 'can_30_max_s': round(30 * float(y.max()), 1)}


def so_mu_trong_luot(mau, T):
    """Số mũ e của thời gian tích lũy theo số bước (log–log), chỉ mẫu có bước ≥ T/2."""
    pts = [(b, s) for s, b in mau if b >= T / 2 and s > 0]
    if len(pts) < 3:
        return None
    lx, ly = np.log([b for b, _ in pts]), np.log([s for _, s in pts])
    return float(np.polyfit(lx, ly, 1)[0])


def bocpd(tom_nho, tom_lon, yeu_to):
    def doc(tom):
        d = nap(tom)
        out = {}
        for r in d['luot']:
            kq = r.get('ket_qua') or {}
            out[r['T']] = {'trang_thai': r['trang_thai'], 'giay_goi': kq.get('giay_goi_bocpd'), 'd': kq.get('d'),
                           'wall_s': r['cost']['wall_s'], 'peak_rss_mb': r['cost']['peak_rss_mb'],
                           'ms_moi_lan_pdf': (1000 * kq['giay_goi_bocpd'] / kq['so_lan_pdf']) if kq.get('giay_goi_bocpd') else None,
                           'so_mu_trong_luot': so_mu_trong_luot(kq.get('mau_tien_do') or [], r['T']) if kq else None,
                           'tien_do_cuoi': r.get('tien_do_cuoi')}
        return d['opaque_id'], out
    on, n = doc(tom_nho)
    ol, l = doc(tom_lon)
    dn, dl = n[300]['d'], l[300]['d']
    ok = all(v['trang_thai'] == 'OK' for v in list(n.values()) + list(l.values()))
    res = {'ca_nho': {'opaque_id': on, 'd': dn, 'luot': n}, 'ca_lon': {'opaque_id': ol, 'd': dl, 'luot': l},
           'tat_ca_OK': ok}
    if not ok:
        res['ghi_chu'] = 'có lượt không OK: chỉ có cận dưới; không chiếu'
        return res
    pn = math.log2(n[600]['giay_goi'] / n[300]['giay_goi'])
    pl = math.log2(l[300]['giay_goi'] / l[150]['giay_goi'])
    res['p'] = {'ca_nho': pn, 'ca_lon': pl}
    res['chieu_1441_mot_ca_s'] = {
        'ca_nho': {'T2': n[600]['giay_goi'] * (T_DU / 600) ** 2, 'Tp': n[600]['giay_goi'] * (T_DU / 600) ** pn},
        'ca_lon': {'T2': l[300]['giay_goi'] * (T_DU / 300) ** 2, 'Tp': l[300]['giay_goi'] * (T_DU / 300) ** pl}}
    cn, cl = n[300]['giay_goi'] / 300 ** 2, l[300]['giay_goi'] / 300 ** 2
    q = math.log(cl / cn) / math.log(dl / dn)
    ds = [r['bocpd_d'] for r in yeu_to.values()]
    t2 = sum(cn * T_DU ** 2 * (d / dn) ** 2 for d in ds)
    tq = sum(cn * T_DU ** 2 * (d / dn) ** q for d in ds)
    res['c'] = {'ca_nho': cn, 'ca_lon': cl}
    res['q'] = q
    res['chieu_30_ca_s'] = {'d2_T2': t2, 'dq_T2': tq}
    res['chieu_30_ca_gio'] = {k: v / 3600 for k, v in res['chieu_30_ca_s'].items()}
    res['thu_yeu_nhan_1441_300_mu_p_tru_2'] = {
        f'{k}_p_{ten}': v * (T_DU / 300) ** (p - 2) / 3600
        for k, v in res['chieu_30_ca_s'].items() for ten, p in (('nho', pn), ('lon', pl))}
    res['phan_bo_d_30_ca'] = {'min': min(ds), 'max': max(ds), 'tong': sum(ds)}
    return res


def main(cfg_path):
    cfg = nap(cfg_path)
    yeu_to = {r['opaque_id']: r for r in nap(cfg['yeu_to'])['ca']}
    out = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'nguon': cfg}
    do = {}
    mr = nap(cfg['microrank'])
    do['microrank'] = {'tong_30_ca_s': mr['chi_phi']['tong_wall_s'], 'max_rss_mb': mr['chi_phi']['max_peak_rss_mb'],
                       'max_luot_s': max(r['wall_s'] for r in mr['ca'] if r.get('wall_s'))}
    for k in ('circa_h0_lan1', 'circa_h0_lan2', 'circa_h1', 'circa_h2'):
        d = nap(cfg[k])
        w = [x for v in walls(cfg[k]).values() for x in v]
        do[k] = {'tong_30_ca_s': d['tong_wall_s'], 'max_rss_mb': d['max_peak_rss_mb'], 'max_luot_s': max(w), 'so_luot': len(w)}
    for k in ('torai_B', 'torai_A'):
        if cfg.get(k):
            d = nap(cfg[k])
            w = [x for v in walls(cfg[k]).values() for x in v]
            do[k] = {'xong': d.get('xong'), 'so_luot': len(w), 'tong_s': round(sum(w), 1),
                     'max_luot_s': max(w) if w else None,
                     'max_rss_mb': max(((r.get('cost') or {}).get('peak_rss_mb') or 0) for r in d['luot'])}
    out['do_that'] = do
    pl = {}
    for m, cot in (('baro', 'baro_cot_hai_nua'), ('simplerca', 'cua_so_span'), ('tracerca', 'cua_so_span'),
                   ('nsigma', 'nsigma_cot'), ('nsigma_doi_chung', 'nsigma_doi_chung_cot')):
        w = walls(cfg['pilot_' + m])
        d = nap(cfg['pilot_' + m])
        pl[m] = noi_suy(w, yeu_to, cot)
        pl[m]['max_rss_mb'] = d['max_peak_rss_mb']
        pl[m]['max_luot_s'] = max(x for v in w.values() for x in v)
    out['pilot_chieu'] = pl
    if cfg.get('bocpd_nho') and cfg.get('bocpd_lon'):
        out['bocpd'] = bocpd(cfg['bocpd_nho'], cfg['bocpd_lon'], yeu_to)
    chung.ghi_json(chung.OUT / 'chieu-chi-phi.json', out)
    print(json.dumps({k: out[k] for k in ('do_that', 'pilot_chieu')}, ensure_ascii=False, indent=1))
    if 'bocpd' in out:
        print(json.dumps(out['bocpd'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])

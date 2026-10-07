"""T-031 bước 3: K-SVR1–4 (giao-thuc-v2 §6.5, WHY-30, D5) từ hai lượt SVR 30 ca, hash seed 0. Không dùng nhãn.

K-SVR1: cấu hình đúng bài (ANMRegressor(SVR(kernel="sigmoid")), tham số khác mặc định sklearn 1.6.0, lớp RCAEval).
K-SVR2: 30/30 ca không ném lỗi, mọi z hữu hạn, không nút có cha hiệu lực rơi value_error_fallback; TIMEOUT tính
không đạt (SPEC). K-SVR3: lượt 2 cho bản ghi giống hệt lượt 1 (trừ run_id, opaque_id, cost, input_sha256).
K-SVR4: tổng wall lượt 1 ≤ 3 giờ. Luật khóa: SVR nếu đạt cả bốn, không thì OLS.

python k_svr.py <tom-tat lượt 1> <tom-tat lượt 2>
"""
import inspect
import json
import sys

import chung

NGUONG_KSVR4_S = 3 * 3600


def nap(p):
    return json.loads(open(p, encoding='utf-8').read())


def ksvr1():
    from sklearn.svm import SVR
    from p3.adapters import circa
    mac_dinh, dung = SVR().get_params(), circa._svr().get_params()
    khac = {k: [mac_dinh[k], dung[k]] for k in mac_dinh if mac_dinh[k] != dung[k]}
    src = inspect.getsource(circa.cham_svr)
    lop = 'RHTScorer(regressor=ANMRegressor(regressor=tao_hoi_quy()))' in src and \
        'from RCAEval.graph_heads.rht import RHTScorer, DAScorer, ANMRegressor' in src
    return {'tham_so_khac_mac_dinh': khac, 'goi_qua_lop_RCAEval': lop,
            'nguon_bai': 'CIRCA 0215e18 circa/experiment/comparison/models.py:583–586: '
                         'ANMRegressor(regressor=SVR(kernel="sigmoid"))',
            'dat': khac == {'kernel': ['rbf', 'sigmoid']} and lop}


def main(p1, p2):
    a, b = nap(p1), nap(p2)
    assert a['cau_hinh']['model'] == b['cau_hinh']['model'] == 'svr'
    l1 = {r['opaque_id']: r for r in a['luot'] if r['hashseed'] == 0}
    l2 = {r['opaque_id']: r for r in b['luot'] if r['hashseed'] == 0}
    k1 = ksvr1()
    ca, ca3 = [], []
    for oid in sorted(l1):
        r = l1[oid]
        st = {v: x['status'] for v, x in (r.get('bien_the') or {}).items()}
        c = r.get('circa') or {}
        loi = r.get('loi_runner')
        ok = (not loi and len(st) == 2 and all(s in ('OK', 'NO_EVIDENCE') for s in st.values())
              and c.get('z_khong_huu_han') == 0 and c.get('vef_nut_co_cha') == 0)
        ca.append({'opaque_id': oid, 'trang_thai': st, 'loi_runner': loi, 'routes': c.get('routes'),
                   'value_error_fallback': c.get('vef_nut'), 'z_khong_huu_han': c.get('z_khong_huu_han'),
                   'so_nut': c.get('so_nut'), 'so_canh': c.get('so_canh'), 'cha_lon_nhat': c.get('cha_lon_nhat'),
                   'current_bang_t_cong_299': c.get('current_bang_t_cong_299'),
                   'wall_s': (r.get('cost') or {}).get('wall_s'), 'peak_rss_mb': (r.get('cost') or {}).get('peak_rss_mb'),
                   'dat_ksvr2': ok})
        r2 = l2.get(oid) or {}
        h1 = {v: x['ban_ghi_hash'] for v, x in (r.get('bien_the') or {}).items()}
        h2 = {v: x['ban_ghi_hash'] for v, x in (r2.get('bien_the') or {}).items()}
        ca3.append({'opaque_id': oid, 'giong_het': bool(h1) and h1 == h2, 'lan1': h1, 'lan2': h2})
    tw = round(sum(x['wall_s'] or 0 for x in ca), 1)
    k2 = {'so_ca': len(ca), 'so_ca_dat': sum(x['dat_ksvr2'] for x in ca), 'dat': len(ca) == 30 and all(x['dat_ksvr2'] for x in ca),
          'tong_route': {}}
    for x in ca:
        for k, v in (x['routes'] or {}).items():
            k2['tong_route'][k] = k2['tong_route'].get(k, 0) + v
    k3 = {'so_ca_giong_het': sum(x['giong_het'] for x in ca3), 'dat': len(ca3) == 30 and all(x['giong_het'] for x in ca3)}
    k4 = {'tong_wall_lan1_s': tw, 'nguong_s': NGUONG_KSVR4_S, 'dat': tw <= NGUONG_KSVR4_S,
          'tong_wall_lan2_s': b.get('tong_wall_s')}
    dat = k1['dat'] and k2['dat'] and k3['dat'] and k4['dat']
    doc = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'nguon': {'lan1': p1, 'lan2': p2},
           'src_p3_sha256': [a['src_p3_sha256'], b['src_p3_sha256']],
           'K_SVR1': k1, 'K_SVR2': k2, 'K_SVR3': k3, 'K_SVR4': k4,
           'dat_ca_bon': dat, 'mo_hinh_khoa': 'svr' if dat else 'ols',
           'ten_trong_bang': 'CIRCA kiến trúc, SVR(sigmoid)+RHT+DA, cấu hình P3' if dat
           else 'CIRCA kiến trúc, OLS+RHT+DA, cấu hình P3',
           'ca': ca, 'K_SVR3_ca': ca3}
    chung.ghi_json(chung.OUT / 'k-svr.json', doc)
    print(json.dumps({k: doc[k] for k in ('K_SVR1', 'K_SVR3', 'K_SVR4', 'dat_ca_bon', 'mo_hinh_khoa')},
                     ensure_ascii=False))
    print('K_SVR2', {k: v for k, v in k2.items()})


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

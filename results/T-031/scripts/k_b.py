"""T-031 bước 4: K-B (giao-thuc-v2 §6.6, WHY-29, D4) và lệch lưới nguồn A, không dùng nhãn, không chấm.

K-B1: dẫn từ T-030 (`results/T-030/k-b1.json`). K-B2: tổng `logts` B mỗi service = số dòng log của service trong
cửa sổ, cả 30 ca (tính trong lượt B trước khi xóa bảng). Ghi thêm, không tính đạt: tổng log toàn file mỗi service
của parquet so với `logts.csv` tác giả. K-B3: TORAI sửa chạy trên B ở 30 ca × 3 seed không lỗi (TIMEOUT là không
đạt, SPEC); ghi tỉ lệ cụm rơi nhánh dự phòng. Lệch lưới A từng ca từ bước chuẩn bị nguồn A. Luật khóa: B làm dòng
chính khi đạt cả K-B1, K-B2, K-B3; không thì A.

python k_b.py <tom-tat torai_B> <tom-tat torai_A | -> [lech-luoi-a.json]
Khi lượt B chưa đủ 90 lượt hoặc chưa có lượt A ('-'): ghi kết quả từng phần, không khóa nguồn.
"""
import json
import sys

import pandas as pd

import chung
from p3.runner import _tac_gia_A


def nap(p):
    return json.loads(open(p, encoding='utf-8').read())


def log_toan_file(al, oid):
    """Ghi thêm cho K-B2: tổng log mỗi service toàn file, parquet so với logts tác giả."""
    f = chung.selector.chon_ca(al, oid, chung.ROOT, kiem_hash=False)
    pq = {}
    if 'logs.parquet' in f:
        pq = pd.read_parquet(f['logs.parquet'], columns=['container_name']).groupby('container_name').size().to_dict()
    lt = pd.read_csv(_tac_gia_A(al[oid]['case_dir'])['logts']).set_index('time')
    tg = {}
    for c in lt.columns:
        s = c.rsplit('_', 1)[0]
        tg[s] = tg.get(s, 0) + float(lt[c].sum())
    sv = sorted(set(pq) | set(tg))
    return {'tong_parquet': int(sum(pq.values())), 'tong_tac_gia': float(sum(tg.values())),
            'so_service_parquet': len(pq), 'so_service_tac_gia': len(tg),
            'so_service_lech': sum(1 for s in sv if float(pq.get(s, 0)) != tg.get(s, 0.0))}


def main(pB, pA, p_lech=None):
    al, _ = chung.nap()
    B = nap(pB)
    A = nap(pA) if pA != '-' else {'luot': [], 'src_p3_sha256': B['src_p3_sha256']}
    kb1_src = nap(chung.ROOT / 'results/T-030/k-b1.json')
    kb1 = {'nguon': 'results/T-030/k-b1.json', 'tong': kb1_src['tong'], 'dat': kb1_src['dat'],
           'ket_luan': kb1_src['ket_luan']['K_B1'], 'ghi_chu': kb1_src['ket_luan']['ghi_chu']}
    lb = B['luot']
    ids = sorted({r['opaque_id'] for r in lb})
    kb2_ca, kb3_luot = [], []
    for oid in ids:
        rs = [r for r in lb if r['opaque_id'] == oid]
        k2 = [r.get('k_b2') for r in rs]
        r0 = next((r for r in rs if r.get('seed') == 0), rs[0])
        man = {r['seed']: (r.get('bang_manifest') or {}).get('logts.csv', {}).get('sha256') for r in rs}
        kb2_ca.append({'opaque_id': oid, 'dat': all(x and x['dat'] for x in k2), 'seed0': r0.get('k_b2'),
                       'logts_giong_nhau_3_seed': len(set(man.values())) == 1 and None not in man.values(),
                       'them_toan_file': log_toan_file(al, oid)})
        for r in rs:
            st = {v: x['status'] for v, x in (r.get('bien_the') or {}).items()}
            ok = not r.get('loi_runner') and bool(st) and all(s in ('OK', 'NO_EVIDENCE') for s in st.values())
            kb3_luot.append({'opaque_id': oid, 'seed': r['seed'], 'trang_thai': st, 'loi_runner': r.get('loi_runner'),
                             'torai': r.get('torai'), 'chuan_bi': r.get('chuan_bi'), 'input_shape': r.get('input_shape'),
                             'wall_s': (r.get('cost') or {}).get('wall_s'), 'dat': ok})
    kb2 = {'so_ca': len(kb2_ca), 'so_ca_dat': sum(x['dat'] for x in kb2_ca),
           'dat': len(kb2_ca) == 30 and all(x['dat'] for x in kb2_ca)}
    tl = [x['torai']['ty_le_du_phong'] for x in kb3_luot if x.get('torai') and x['torai'].get('ty_le_du_phong') is not None]
    cum = sum((x.get('torai') or {}).get('cum_nhieu_service') or 0 for x in kb3_luot)
    dp = sum((x.get('torai') or {}).get('cum_du_phong') or 0 for x in kb3_luot)
    kb3 = {'so_luot': len(kb3_luot), 'so_luot_dat': sum(x['dat'] for x in kb3_luot),
           'dat': len(kb3_luot) == 90 and all(x['dat'] for x in kb3_luot),
           'cum_nhieu_service': cum, 'cum_du_phong': dp, 'ty_le_du_phong_gop': dp / cum if cum else None,
           'ty_le_du_phong_tung_luot': {'min': min(tl) if tl else None, 'max': max(tl) if tl else None}}
    lech = []
    for oid in sorted({r['opaque_id'] for r in A['luot']}):
        rs = [r for r in A['luot'] if r['opaque_id'] == oid]
        cb = [r.get('chuan_bi') for r in rs]
        st = {r['seed']: {v: x['status'] for v, x in (r.get('bien_the') or {}).items()} for r in rs}
        lech.append({'opaque_id': oid, 'chuan_bi': cb[0], 'giong_nhau_3_seed': all(c == cb[0] for c in cb),
                     'trang_thai_A': st, 'loi_runner': [r.get('loi_runner') for r in rs if r.get('loi_runner')]})
    du = bool(B.get('xong')) and len(kb3_luot) == 90 and pA != '-'
    dat = bool(kb1['dat']) and kb2['dat'] and kb3['dat']
    doc = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'nguon': {'B': pB, 'A': pA},
           'src_p3_sha256': sorted({B['src_p3_sha256'], A['src_p3_sha256']}),
           'K_B1': kb1, 'K_B2': kb2, 'K_B3': kb3, 'du_luot': du,
           'dat_ca_ba': dat if du else None, 'nguon_chinh_khoa': ('B' if dat else 'A') if du else None,
           'trang_thai': 'đủ lượt' if du else 'TỪNG PHẦN: lượt B chưa đủ 90 hoặc chưa có lượt A; chưa khóa nguồn',
           'lech_luoi_A': {'phan_bo_lech_s': sorted({x['chuan_bi']['lech_luoi_s'] for x in lech if x['chuan_bi']}),
                           'ca': lech},
           'lech_luoi_A_khong_chay_torai': nap(p_lech) if p_lech else None,
           'chi_phi': {'B_tong_wall_s': B.get('tong_wall_s'), 'A_tong_wall_s': A.get('tong_wall_s'),
                       'B_max_rss_mb': B.get('max_peak_rss_mb'), 'A_max_rss_mb': A.get('max_peak_rss_mb')},
           'K_B2_ca': kb2_ca, 'K_B3_luot': kb3_luot}
    chung.ghi_json(chung.OUT / 'k-b.json', doc)
    print(json.dumps({k: doc[k] for k in ('K_B2', 'K_B3', 'dat_ca_ba', 'nguon_chinh_khoa')}, ensure_ascii=False))
    print('K_B1', kb1['dat'], 'lech A', doc['lech_luoi_A']['phan_bo_lech_s'])


if __name__ == '__main__':
    main(*sys.argv[1:4])

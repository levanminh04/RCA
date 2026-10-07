"""T-031 (Q-81, WHY-36): tổng hợp lượt CIRCA V∞. Không dùng nhãn, không chấm.

Từ `runs/circa-vinf-001` (model=ols_vinf, 30 ca × hash seed 0, 1, 2):
1. Trạng thái 4 biến thể từng lượt; lỗi runner.
2. Bản OLS gốc trong lượt V∞ có giống hệt lượt `circa-ols-h{hs}-001` cùng hash seed (so bản ghi trừ
   run_id, opaque_id, cost, input_sha256) không: bằng chứng V∞ không đổi bản gốc.
3. Số nút luật +inf / luật 0 từng ca; tên nút +inf (tên metric, không phải nhãn).
4. Cỡ nhóm hòa đầu của thứ hạng thực thể V∞ (DA, RHT-only) và bản gốc, để thấy V∞ biến các ca bị ghim
   thành nhóm hòa ra sao. Chỉ so thứ hạng với nhau.

python k_vinf.py
"""
import json
from pathlib import Path

import chung

RUN = chung.OUT / 'runs' / 'circa-vinf-001'
BO = ('run_id', 'opaque_id', 'cost', 'input_sha256')


def gon(r):
    return json.dumps({k: v for k, v in r.items() if k not in BO}, sort_keys=True, ensure_ascii=False)


def doc_luot(run, oid, hs):
    ds = sorted((chung.OUT / 'runs' / run / 'luot').glob(f'circa-a-{oid}-sNone-h{hs}-*'))
    if len(ds) != 1:
        return None
    recs = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(ds[0].glob('ban-ghi-*.json'))]
    return {r['variant']: r for r in recs}


def nhom_dau(rec):
    er = rec.get('entity_ranking') or []
    return sum(1 for r in er if r['tie_group'] == 0) if er else None


def main():
    tom = json.loads((RUN / 'tom-tat.json').read_text(encoding='utf-8'))
    assert tom.get('xong'), 'lượt chưa xong'
    rows = []
    for l in tom['luot']:
        oid, hs = l['opaque_id'], l['hashseed']
        v = doc_luot('circa-vinf-001', oid, hs)
        o = doc_luot(f'circa-ols-h{hs}-001', oid, hs)
        row = {'opaque_id': oid, 'hashseed': hs, 'loi_runner': l.get('loi_runner'),
               'trang_thai': {k: r['status'] for k, r in (v or {}).items()}}
        if v and o:
            row['ols_giong_luot_ols'] = all(gon(v[k]) == gon(o[k]) for k in ('ols+rht_da', 'ols+rht'))
        vn = (v or {}).get('ols_vinf+rht_da', {}).get('diagnostics', {}).get('vinf_nodes') or {}
        row['nut_inf'] = vn.get('inf') or []
        g = ((v or {}).get('ols+rht', {}).get('diagnostics') or {}).get('nodes') or {}
        row['diem_goc_nut_inf'] = {n: float(g[n]['rht_score']) for n in row['nut_inf'] if n in g}
        row['so_zero'] = len(vn.get('zero') or [])
        row['nhom_hoa_dau'] = {k: nhom_dau(r) for k, r in (v or {}).items()}
        row['khoa_dau_inf'] = {k: (r.get('entity_ranking') or [{}])[0].get('key', [None])[0] == 'inf'
                               for k, r in (v or {}).items() if k.startswith('ols_vinf')}
        rows.append(row)
    h0 = [r for r in rows if r['hashseed'] == 0]
    doc = {
        'mo_ta': __doc__.strip(), 'run': RUN.name, 'src_p3_sha256': tom['src_p3_sha256'],
        'so_luot': len(rows), 'so_loi_runner': sum(1 for r in rows if r['loi_runner']),
        'moi_bien_the_OK': sum(1 for r in rows if r['trang_thai'] and all(s == 'OK' for s in r['trang_thai'].values())),
        'ols_giong_luot_ols': sum(1 for r in rows if r.get('ols_giong_luot_ols')),
        'hs0_so_ca_co_nut_inf': sum(1 for r in h0 if r['nut_inf']),
        'hs0_so_ca_co_nut_zero': sum(1 for r in h0 if r['so_zero']),
        'hs0_ten_nut_inf': sorted({n for r in h0 for n in r['nut_inf']}),
        'hs0_nut_inf_diem_goc_tren_1e10': sum(1 for r in h0 for x in r['diem_goc_nut_inf'].values() if x > 1e10),
        'hs0_nut_inf_diem_goc_duoi_1e10': sum(1 for r in h0 for x in r['diem_goc_nut_inf'].values() if x <= 1e10),
        'hs0_ca_co_nut_inf_diem_goc_tren_1e10': sum(1 for r in h0 if any(x > 1e10 for x in r['diem_goc_nut_inf'].values())),
        'hs0_so_ca_dau_DA_la_inf': sum(1 for r in h0 if r['khoa_dau_inf'].get('ols_vinf+rht_da')),
        'hs0_nhom_hoa_dau_vinf_DA_min_trung_vi_max': None,
        'tong_wall_s': tom.get('tong_wall_s'), 'max_peak_rss_mb': tom.get('max_peak_rss_mb'),
        'luot': rows,
    }
    import statistics
    g = [r['nhom_hoa_dau'].get('ols_vinf+rht_da') for r in h0]
    doc['hs0_nhom_hoa_dau_vinf_DA_min_trung_vi_max'] = [min(g), statistics.median(g), max(g)]
    chung.ghi_json(chung.OUT / 'k-vinf.json', doc)
    print({k: v for k, v in doc.items() if k not in ('luot', 'mo_ta')})


if __name__ == '__main__':
    main()

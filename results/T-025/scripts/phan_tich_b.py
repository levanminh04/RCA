"""T-025 bước 6: số liệu phụ cho báo cáo, đọc đầu ra evaluator đã ghi (`cham/`) và bản ghi đã chốt. Vai evaluator:
đọc nhãn sau khi danh sách đã chốt. Không đổi bản ghi, không đổi cấu hình.

- Theo ca: vị trí t̂ (giây từ đầu file), t̂ − t_tiêm, cửa sổ A = [t̂, t̂+300) có chứa mốc không, hạng root mỗi ranker.
- Tách thứ hạng tại báo động sai theo việc A có chứa mốc (báo riêng, không cộng vào thành công chung, §7.5).
- TORAI: tỉ lệ cụm rơi nhánh dự phòng, seed cho thứ tự giống nhau không. BARO: thứ hạng trùng thứ tự cột.
- Chi phí: wall, RSS từng lượt (EC2), BOCPD theo số cột d.

python phan_tich_b.py <ban-ghi-dua-vao-cham.json> <thư mục cham>
"""
import json
import statistics
import sys
from pathlib import Path

import chung
from p3 import nhan

KEYS = ('baro:native', 'circa:ols+rht_da', 'circa:ols+rht', 'torai_B')


def main(ds_path, cham_dir):
    ds = json.loads(Path(ds_path).read_text(encoding='utf-8'))
    lab = nhan.nap_nhan(chung.ROOT / 'results/T-022/nhan-dev.json')
    cham_dir = Path(cham_dir)
    cb = json.loads((cham_dir / 'cham-b.json').read_text(encoding='utf-8'))['theo_bo_phat_hien']
    ph = json.loads((cham_dir / 'phat-hien.json').read_text(encoding='utf-8'))['bo_phat_hien']
    det, rca = {}, {}
    for it in ds['ban_ghi']:
        r = json.loads((chung.ROOT / it['duong_dan']).read_text(encoding='utf-8'))
        if it['loai'] == 'bo_phat_hien':
            det.setdefault(it['nhom'], {})[r['opaque_id']] = r
        else:
            rca.setdefault(it['nhom'], []).append(r)
    ids = sorted(lab)
    out = {'mo_ta': __doc__.strip(), 'theo_ca': {}, 'bao_dong_sai_theo_A': {}, 'torai': {}, 'baro': {}, 'chi_phi': {}}
    for oid in ids:
        L = lab[oid]
        row = {'root': L['root'], 'fault': L['fault'], 'cell': L['cell'],
               'chi_so_moc': det['bocpd'][oid]['times'].index(L['inject_time'])}
        for nhom in ('bocpd', 'nsigma', 'nsigma_doi_chung'):
            r = det[nhom][oid]
            t0 = r['times'][0]
            th = r['luot_rca']['t_hat']
            row[nhom] = {'t_hat_giay_tu_dau_file': th - t0, 't_hat_tru_t_tiem': th - L['inject_time'],
                         'A_chua_moc': th + 300 > L['inject_time'], 'so_bao_dong': len(r['alarms']),
                         'do_tre_s': ph[nhom]['ca'][oid]['do_tre_s'], 'so_thong_bao': r['luot_rca']['so_thong_bao']}
            if nhom in cb:
                row[nhom]['hang_root'] = {k: {'min': cb[nhom][k]['ca'][oid]['hang_min'],
                                              'max': cb[nhom][k]['ca'][oid]['hang_max'],
                                              'hit@1': cb[nhom][k]['ca'][oid]['hit@1'],
                                              'rr': cb[nhom][k]['ca'][oid]['rr']} for k in KEYS}
        out['theo_ca'][oid] = row
    out['chi_so_moc_cac_gia_tri'] = sorted({r['chi_so_moc'] for r in out['theo_ca'].values()})
    for nhom in ('bocpd', 'nsigma'):
        g = {}
        for k in KEYS:
            for chua in (True, False):
                os_ = [o for o in ids if not cb[nhom][k]['ca'][o]['t_hat_dung']
                       and out['theo_ca'][o][nhom]['A_chua_moc'] == chua]
                g.setdefault(k, {})['A_chua_moc' if chua else 'A_khong_chua_moc'] = {
                    'n': len(os_), 'hit@1': (sum(cb[nhom][k]['ca'][o]['hit@1'] for o in os_) / len(os_)) if os_ else None,
                    'hit@5': (sum(cb[nhom][k]['ca'][o]['hit@5'] for o in os_) / len(os_)) if os_ else None,
                    'mrr': (sum(cb[nhom][k]['ca'][o]['rr'] for o in os_) / len(os_)) if os_ else None}
        out['bao_dong_sai_theo_A'][nhom] = g
        tr = [r for r in rca[nhom] if r['method'] == 'torai']
        dp = [r['diagnostics'].get('ty_le_du_phong') for r in tr]
        per = {}
        for r in tr:
            per.setdefault(r['opaque_id'], []).append(r['ranking_native'])
        out['torai'][nhom] = {'so_luot': len(tr), 'ty_le_du_phong': {'tb': statistics.mean(dp), 'min': min(dp), 'max': max(dp),
                                                                      'so_luot_bang_1': sum(x == 1 for x in dp)},
                              'so_ca_3_seed_cung_thu_tu': sum(all(x == v[0] for x in v) for v in per.values()),
                              'so_ca': len(per)}
        br = [r for r in rca[nhom] if r['method'] == 'baro']
        out['baro'][nhom] = {'so_luot': len(br), 'rank_equals_column_order': sum(bool(r['diagnostics'].get('rank_equals_column_order')) for r in br),
                             'key_check_pass': sum(r['diagnostics'].get('key_check') == 'pass' for r in br)}
        cp = {}
        for r in rca[nhom]:
            if r['method'] == 'circa' and r['variant'].endswith('rht'):
                continue  # hai biến thể CIRCA cùng một lượt, cùng chi phí
            cp.setdefault(r['method'], []).append(r['cost']['wall_s'])
        out['chi_phi'][f'rca_{nhom}'] = {m: {'n': len(v), 'tong_s': round(sum(v), 1), 'tb_s': round(statistics.mean(v), 1),
                                             'min_s': round(min(v), 1), 'max_s': round(max(v), 1)} for m, v in cp.items()}
    for nhom in ('bocpd', 'nsigma', 'nsigma_doi_chung'):
        w = [det[nhom][o]['cost']['wall_s'] for o in ids]
        rss = [det[nhom][o]['cost']['peak_rss_mb'] for o in ids]
        x = {'tong_s': round(sum(w), 1), 'tb_s': round(statistics.mean(w), 1), 'min_s': round(min(w), 1),
             'max_s': round(max(w), 1), 'rss_max_mb': max(rss)}
        if nhom == 'bocpd':
            d = [det[nhom][o]['input_shape']['cot_sau_tien_xu_ly'] for o in ids]
            x['theo_ca'] = {o: {'d': dd, 'wall_s': ww} for o, dd, ww in zip(ids, d, w)}
            n = len(d)
            md, mw = sum(d) / n, sum(w) / n
            sxy = sum((a - md) * (b - mw) for a, b in zip(d, w))
            sxx = sum((a - md) ** 2 for a in d)
            b1 = sxy / sxx
            x['hoi_quy_wall_theo_d'] = {'he_so_s_moi_cot': b1, 'chan_s': mw - b1 * md,
                                        'tuong_quan': sxy / (sxx * sum((b - mw) ** 2 for b in w)) ** 0.5}
            x['wall_chia_d'] = {'tb': statistics.mean(ww / dd for dd, ww in zip(d, w)),
                                'min': min(ww / dd for dd, ww in zip(d, w)), 'max': max(ww / dd for dd, ww in zip(d, w))}
            x['wall_chia_d2'] = {'min': min(ww / dd ** 2 for dd, ww in zip(d, w)),
                                 'max': max(ww / dd ** 2 for dd, ww in zip(d, w))}
            x['d'] = {'min': min(d), 'max': max(d), 'tong': sum(d), 'tong_d2': sum(v * v for v in d)}
        out['chi_phi'][nhom] = x
    chung.ghi_json(cham_dir / 'phan-tich-b.json', out)
    print(json.dumps({k: v for k, v in out.items() if k in ('bao_dong_sai_theo_A', 'torai', 'baro')}, ensure_ascii=False)[:3000])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

"""T-031 bước 1: bảng yếu tố 30 ca và ca pilot từng phương pháp (giao-thuc-v2 §12), không dùng nhãn.

Luật khai trước (LOG T-031 10:20): sắp theo bộ yếu tố (thứ tự từ điển); nhỏ nhất, trung vị dưới (vị trí 15/30),
lớn nhất; hòa thì mã mờ nhỏ hơn. CIRCA lấy yếu tố từ tóm tắt lượt K-SVR đầu (đồ thị dựng từ N, hash seed 0);
TORAI từ tóm tắt lượt nguồn A và B seed 0 (số cột đưa vào `torai`). Thiếu nguồn nào thì bỏ phương pháp đó.

python chon_ca_pilot.py <yeu-to.json> [circa=<tom-tat.json>] [torai_A=<tom-tat.json>] [torai_B=<tom-tat.json>]
"""
import json
import sys

import chung

YEU_TO = {
    'bocpd': ('bocpd_d',),
    'nsigma': ('nsigma_cot',),
    'nsigma_doi_chung': ('nsigma_doi_chung_cot',),
    'baro': ('baro_cot_hai_nua',),
    'simplerca': ('cua_so_span', 'cua_so_dong_log', 'cua_so_cot_metric'),
    'microrank': ('cua_so_span', 'cua_so_operation'),
    'tracerca': ('cua_so_span', 'cua_so_operation'),
}


def main(yeu_to, **nguon):
    ca = {r['opaque_id']: r for r in json.loads(open(yeu_to, encoding='utf-8').read())['ca']}
    gt = {pp: {oid: tuple(r[k] if r[k] is not None else -1 for k in ks) for oid, r in ca.items()}
          for pp, ks in YEU_TO.items()}
    ten = dict(YEU_TO)
    if 'circa' in nguon:
        luot = json.loads(open(nguon['circa'], encoding='utf-8').read())['luot']
        gt['circa'] = {r['opaque_id']: (r['circa']['so_nut'], r['circa']['so_canh'], r['circa']['cha_lon_nhat'])
                       for r in luot if r.get('hashseed') == 0 and r.get('circa', {}).get('so_nut') is not None}
        ten['circa'] = ('so_nut', 'so_canh', 'cha_lon_nhat')
    for src in ('torai_A', 'torai_B'):
        if src in nguon:
            luot = json.loads(open(nguon[src], encoding='utf-8').read())['luot']
            gt[src] = {r['opaque_id']: (sum(v for k, v in r['input_shape'].items() if k.endswith('_cols')),)
                       for r in luot if r.get('seed') == 0 and r.get('input_shape')}
            ten[src] = ('metric_cols + logts_cols + tracets_err_cols + tracets_lat_cols',)
    chon = {pp: chung.chon_pilot(v) for pp, v in gt.items() if len(v) == 30}
    thieu = {pp: len(v) for pp, v in gt.items() if len(v) != 30}
    doc = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'nguon': {'yeu_to': yeu_to, **nguon},
           'yeu_to': {pp: list(ks) for pp, ks in ten.items()},
           'chon': {pp: {vt: {'opaque_id': oid, 'gia_tri': list(gt[pp][oid])} for vt, oid in c.items()}
                    for pp, c in chon.items()},
           'phuong_phap_thieu_ca': thieu,
           'bang_30_ca': {oid: {pp: list(gt[pp][oid]) for pp in gt if oid in gt[pp]} for oid in sorted(ca)}}
    chung.ghi_json(chung.OUT / 'ca-pilot.json', doc)
    for pp, c in doc['chon'].items():
        print(pp, {vt: (x['opaque_id'], x['gia_tri']) for vt, x in c.items()})
    if thieu:
        print('thiếu ca:', thieu)


if __name__ == '__main__':
    main(sys.argv[1], **dict(a.split('=', 1) for a in sys.argv[2:]))

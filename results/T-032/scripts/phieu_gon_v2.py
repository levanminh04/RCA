#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T-032, phiên 13 — phiếu đọc gọn cho MỌI đơn vị sai chưa đọc tay ở phiên 12 (Minh duyệt đọc hết, Q-141).

Bản v2 = v1 (hàm head, body giữ nguyên) + phần in mới: mọi đơn vị sai hoặc không OK có reading_status khác "đã đọc tay" trong
bao-phu-nhom.json, xếp theo phương pháp, dataset, đường đi; kèm mã đơn vị cùng đường đi đã đọc ở phiên 12.
Dùng: python3 -B -X utf8 phieu_gon_v2.py <thư mục có doi-chieu-dung-sai.json và ke-hoach-doc-tay.json> <bao-phu-nhom.json> <thư mục ra mới>

Bản v1:

Chỉ trình bày lại doi-chieu-dung-sai.json và ke-hoach-doc-tay.json (đầu ra của tong_hop_v1.py).
Không tính gì mới. Mỗi đơn vị in đầy đủ một lần; lần sau chỉ nhắc mã.

Dùng: python3 -B -X utf8 phieu_gon_v1.py <thư mục out của tong_hop_v1.py>
"""
import json
import os
import sys

OUT = sys.argv[1]
D = json.load(open(os.path.join(OUT, 'doi-chieu-dung-sai.json'), encoding='utf-8'))
P = json.load(open(os.path.join(OUT, 'ke-hoach-doc-tay.json'), encoding='utf-8'))
U = {u['unit_id']: u for u in D['don_vi']}
B = json.load(open(sys.argv[2], encoding='utf-8'))
DEST = sys.argv[3]
os.makedirs(DEST, exist_ok=False)


def f(v, nd=2):
    if v is None:
        return '-'
    if isinstance(v, bool):
        return 'C' if v else 'K'
    if isinstance(v, float):
        if abs(v) >= 1e5 or (abs(v) < 1e-2 and v != 0):
            return '%.2g' % v
        return ('%.' + str(nd) + 'f') % v
    return str(v)


def sv(s):
    return (s or '-').replace('-service', '').replace('ts-', '')


POS = {'phia_tren': 'TREN', 'hai_chieu': '2CHIEU', 'phia_duoi': 'DUOI', 'khong_lien_he': 'KLH', 'khong_co_span': 'KSPAN', None: '-'}


def head(u):
    t = u['t028']
    tc = u['trace_cua_ca']
    vc = u['vi_tri_chuoi_goi'] or {}
    s = '%s%s | %s | hang %s | co k1=%s k5=%s | %s' % (
        u['opaque_id'], '' if u['seed'] is None else ' seed%s' % u['seed'], sv(u['cell']), t['hang'], t['co']['1'], t['co']['5'], u['duong_di'])
    s += '\n     trace-ca: muc=%s; cham-toi-root=%s; root-dau-o=%s' % (tc['muc_do_duoc'], f(tc['ty_le_loi_goi_cham_toi_root_lon_nhat_sau_moc']), tc['vi_tri_trace_root_dung_dau'])
    if vc.get('so_tren_root') is not None:
        s += ' | tren-root %s %s; dau=%s(%s); uv-phia-tren %s/%s' % (
            vc['so_tren_root'], {POS.get(k, k): v for k, v in (vc.get('tren_root_theo_vi_tri') or {}).items()}, sv(vc.get('thuc_the_dung_dau')),
            POS.get(vc.get('vi_tri_thuc_the_dung_dau'), vc.get('vi_tri_thuc_the_dung_dau')), vc.get('so_ung_vien_phia_tren_root'), vc.get('so_ung_vien'))
    return s


def body(u):
    d = u['chi_tiet']
    m = u['method']
    L = []
    if u['trang_thai_nguon'] != 'OK':
        return ['     KHONG-OK: %s' % d.get('ly_do_khong_OK')]
    if m == 'baro':
        r = d['root']
        L.append('     root: %s(%s) z=%s iqr/med=%s lech/med=%s; %s tt, %s nhom-hoa' % (r['cot_thang'].split('_', 1)[-1], r['loai_cot'], f(r['z'], 1), f(r['IQR_tren_median']), f(r['lech_tren_median']), r['so_thuc_the'], r['so_nhom_hoa']))
        ab = sorted(d['tren_root'], key=lambda x: -x['z'])
        for p in ab[:5]:
            L.append('     ^ %s: %s(%s) z=%s iqr/med=%s lech/med=%s %s xu-huong=%s luu-luong-doi=%s B2con=%s' % (
                sv(p['entity']), p['cot_thang'].split('_', 1)[-1], p['loai_cot'], f(p['z'], 1), f(p['IQR_tren_median']), f(p['lech_tren_median']),
                POS.get(p['vi_tri_chuoi_goi'], p['vi_tri_chuoi_goi']), p['nhom_xu_huong'], f(p['luu_luong_doi']), f(p['con_tren_root_duoi_B2'])))
        if len(ab) > 5:
            from collections import Counter
            c = Counter((POS.get(p['vi_tri_chuoi_goi'], p['vi_tri_chuoi_goi']), p['loai_cot']) for p in ab[5:])
            L.append('     ^ +%d khac: %s; B2con %d/%d' % (len(ab) - 5, dict(('%s/%s' % k, v) for k, v in c.items()), sum(1 for p in ab if p['con_tren_root_duoi_B2']), len(ab)))
        b1, b2 = d['B1_khong_loc_cot_hang'], d['B2_thang_do_lech_chuan']
        L.append('     B1: %s (root +%s cot; cot tot nhat la cot them: %s) | B2: %s hang %s mat %s moi %s' % (
            b1['tac_dung_len_root'], b1['cot_root_duoc_giu_them'], f(b1['cot_tot_nhat_cua_root_la_cot_them']), b2['tac_dung_len_root'], b2['hang_root'], b2['cap_mat'], b2['cap_moi']))
    elif m == 'simplerca':
        r = d['root']
        L.append('     root: metric %s (%s/%s cot co phieu) + trace %s + log %s = %s' % (r['phieu_metric'], r['cot_metric_co_phieu'], r['cot_metric_dung_duoc'], r['phieu_trace'], r['phieu_log'], r['diem']))
        ab = sorted(d['tren_root'], key=lambda x: -(x['diem'] or 0))
        for p in ab[:5]:
            L.append('     ^ %s: m%s t%s l%s=%s chenh-m=%s; cot-max %s %sp (1cot>root: %s) %s xu-huong=%s S1con=%s' % (
                sv(p['entity']), p['phieu_metric'], p['phieu_trace'], p['phieu_log'], p['diem'], p['chenh_metric'], p['loai_cot_nhieu_phieu_nhat'],
                p['phieu_cot_nhieu_nhat'], f(p['mot_cot_vuot_tong_diem_root']), POS.get(p['vi_tri_chuoi_goi'], p['vi_tri_chuoi_goi']), p['nhom_xu_huong'], f(p['con_tren_root_duoi_S1'])))
        if len(ab) > 5:
            L.append('     ^ +%d khac' % (len(ab) - 5))
        s1 = d['S1_dem_theo_cot']
        L.append('     rieng-metric-quyet-dinh %s/%s | S1: %s hang %s, %s nhom-hoa, mat %s moi %s' % (d['so_cap_rieng_metric_quyet_dinh'], len(ab), s1['tac_dung_len_root'], s1['hang_root'], s1['so_nhom_hoa'], s1['cap_mat'], s1['cap_moi']))
    elif m == 'microrank_full':
        c = d['dem']
        r = d['root']
        L.append('     chia: A=%s N=%s (%s); A-khong-co-root=%s; A-root-tu-co=%s | root: %s diem=%s' % (
            c['trace_bat_thuong'], c['trace_binh_thuong'], f(c['ty_le_trace_bat_thuong']), c['trace_bat_thuong_khong_co_dich_vu_root'], c['trace_bat_thuong_root_tu_mang_co'],
            (r['thao_tac_cao_nhat'] or '').split('_', 1)[-1][:40], f(r['diem'])))
        ab = sorted(d['tren_root'], key=lambda x: x['hang'] or 99)
        for p in ab[:4]:
            k = p['con_tren_root']
            L.append('     ^ %s h%s %s tu-co=%s ngu-canh=%s gan-root=%s | con: A\'%s C1%s MD%s mo15%s' % (
                sv(p['entity']), p['hang'], POS.get(p['vi_tri_chuoi_goi'], p['vi_tri_chuoi_goi']), p['trace_bat_thuong_tu_mang_co'], p['trace_bat_thuong_chi_ngu_canh'],
                f(p['ty_le_trace_bat_thuong_gan_voi_root']), f(k['A_phay']), f(k['C1']), f(k['MD']), f(k['chia_mo15'])))
        if len(ab) > 4:
            n15 = sum(1 for p in ab if p['con_tren_root']['chia_mo15'])
            nc1 = sum(1 for p in ab if p['con_tren_root']['C1'])
            nl = sum(1 for p in ab if (p['ty_le_trace_bat_thuong_gan_voi_root'] or 0) >= 0.5)
            L.append('     ^ +%d khac | tong %d: con sau C1 %d, con sau mo15 %d, gan-root>=0.5: %d' % (len(ab) - 4, len(ab), nc1, n15, nl))
        pt = d['chia_theo_bai_goc']
        L.append("     A': %s->%s | C1: %s->%s | MD: %s->%s | mo15(moc90 %s): %s hang %s, tren %s, dau %s, A-co-root %s | mo1p50: %s hang %s" % (
            d['A_phay_trong_so_don_vi']['tac_dung_len_root'], d['A_phay_trong_so_don_vi']['hang_root'], d['C1_dem_rieng']['tac_dung_len_root'], d['C1_dem_rieng']['hang_root'],
            d['MD_co_theo_phan_chua_phu']['tac_dung_len_root'], d['MD_co_theo_phan_chua_phu']['hang_root'], f(pt['dat_moc_90']), pt['mo15'].get('trang_thai'), pt['mo15'].get('hang_root'),
            pt['mo15'].get('so_tren_root'), [sv(x) for x in pt['mo15'].get('dau_bang') or []], f(pt['mo15'].get('ty_le_trace_bat_thuong_co_root')), pt['mo1p50'].get('trang_thai'), pt['mo1p50'].get('hang_root')))
    elif m == 'tracerca':
        if 'root' not in d:
            return ['     phat-lai: %s' % d]
        r = d['root']
        L.append('     H=%s canh-toi-root-xet-duoc=%s root-duoc-xep=%s | root: %s a=%s n=%s a/n=%s diem=%s' % (
            d['H'], f(d['canh_toi_root_xet_duoc']), f(d['root_duoc_xep']), (r['thao_tac_cao_nhat'] or '').split('_', 1)[-1][:40], r['a'], r['n'], f(r['ty_le_a_tren_n']), f(r['diem'], 4)))
        ab = sorted(d['tren_root'], key=lambda x: -(x['diem'] or 0))
        for p in ab[:5]:
            k = p['con_tren_root']
            L.append('     ^ %s a=%s n=%s a/n=%s diem=%s %s(%s) span-cho-root=%s cho=%s | con: TD%s a/n%s a%s' % (
                sv(p['entity']), p['a'], p['n'], f(p['ty_le_a_tren_n']), f(p['diem'], 4), POS.get(p['vi_tri_chuoi_goi'], p['vi_tri_chuoi_goi']), p['lop'],
                f(p['ty_le_span_mang_co_la_span_cho_root']), f(p['chu_yeu_la_cho_root']) if isinstance(p['chu_yeu_la_cho_root'], bool) else p['chu_yeu_la_cho_root'],
                f(k['TD']), f(k['ty_le_a_tren_n']), f(k['so_tuyet_doi_a'])))
        if len(ab) > 5:
            L.append('     ^ +%d khac' % (len(ab) - 5))
        ob = d['buoc_xep_hang_bai_goc_to_p']
        dc = d['doi_cong_thuc_diem']
        L.append('     TD: %s->%s | a/n: %s; a/n>=20span: %s; a: %s | bai-goc to_p: %s huu-ich=%s root-duong=%s hang %s dau %s' % (
            d['TD_co_theo_phan_chua_phu']['tac_dung_len_root'], d['TD_co_theo_phan_chua_phu']['hang_root'], dc['ty_le_a_tren_n'], dc['ty_le_tu_20_span'], dc['so_tuyet_doi_a'],
            ob['trang_thai'], f(ob['dac_trung_huu_ich']), f(ob['root_diem_duong']), ob['hang_root'], [sv(x) for x in ob['dau_bang'] or []]))
    elif m == 'circa_ols_da':
        h = d['hang_root']
        L.append('     cuc-lon=%s %s' % (f(d['co_nut_cuc_lon']), [(x['nut'], 'cha%s' % x['so_cha'], 'std-y=%s' % f(x['y_train_do_lech_chuan']), 'rht=%s' % f(x['rht']), 'k2=%s' % f(x['rht_khong_canh'])) for x in d['nut_cuc_lon']]))
        L.append('     root: %s | RHT %s DA %s (%s) | K2 %s k2x %s k2s %s | root-cuc-lon-sau-DA=%s %s' % (
            d['cot_tot_nhat_cua_root'], h['RHT'], h['DA'], d['tac_dung_DA_len_root'], h['K2_khong_canh_RHT'], h['k2x_chi_canh_cung_dich_vu'], h['k2s_chi_canh_khac_dich_vu'],
            f(d['root_mang_khoa_cuc_lon_sau_DA']), d['nguon_khoa_cuc_lon_cua_root']))
        ab = d['tren_root_bang_DA']
        for p in ab[:6]:
            L.append('     ^ %s goi-tt-root=%s cuc-lon=%s tren-o-RHT=%s con-khi-bo-canh=%s' % (sv(p['entity']), f(p['goi_truc_tiep_root']), f(p['mang_khoa_cuc_lon_sau_DA']), f(p['dung_tren_root_o_bang_khong_DA']), f(p['con_tren_root_khi_bo_canh_bang_RHT'])))
        if len(ab) > 6:
            L.append('     ^ +%d khac: cuc-lon %d/%d; tren-o-RHT %d/%d' % (len(ab) - 6, sum(1 for p in ab if p['mang_khoa_cuc_lon_sau_DA']), len(ab), sum(1 for p in ab if p['dung_tren_root_o_bang_khong_DA']), len(ab)))
    elif m == 'torai_B':
        r = d['root']
        L.append('     root: vec=%s sev=%s hang-sev %s; cum %s (%s); hang %s' % ({k: f(v, 3) for k, v in (r['vecto_4_nguon'] or {}).items()}, f(r['severity'], 3), r['hang_severity'], r['kich_thuoc_cum'], r['nhanh_xep_trong_cum'], r['hang']))
        for p in d['tren_root']:
            L.append('     ^ %s sev=%s (+%s) cung-cum=%s chenh=%s max=%s' % (sv(p['entity']), f(p['severity'], 3), f(p['chenh_severity'], 3), f(p['cung_cum_voi_root']), {k: f(v, 3) for k, v in (p['chenh_theo_nguon'] or {}).items()}, p['nguon_chenh_lon_nhat']))
        t1, t2 = d['bo_nguon_log_tl1'], d['bo_cot_log_nen_khong_doi_tl2']
        L.append('     mat-o: %s | tl2 seed0 %s | tl1 seed0 %s; seed nay %s; ba seed giong: %s' % (
            (d['mat_hang_o_dau'] or '')[:70], t2['hang_root_seed0'], t1['hang_root_seed0'], t1.get('hang_root_dung_seed_nay'),
            (t1.get('kiem_seed_1_2') or {}).get('hang_giong_nhau_ba_seed') if isinstance(t1.get('kiem_seed_1_2'), dict) else 'khong chay rieng'))
    return L


READ = {u['unit_id'] for u in B['units'] if u['reading_status'].startswith('đã đọc tay')}
read_by_path = {}
for g in P['nhom']:
    for rd in g['doc_tay']:
        read_by_path.setdefault((g['dataset'], g['method'], rd['duong_di']), set()).add(rd['don_vi_sai_doc'])
todo = [u for u in D['don_vi'] if (not u['dung_hang_1'] or u['trang_thai_nguon'] != 'OK') and u['unit_id'] not in READ]
index = []
for m in sorted({u['method'] for u in todo}):
    out = []
    rows = sorted((u for u in todo if u['method'] == m), key=lambda u: (u['dataset'], u['trang_thai_nguon'] != 'OK', u['duong_di'] or '', u['opaque_id'], str(u['seed'])))
    last = None
    for u in rows:
        key = (u['dataset'], u['trang_thai_nguon'], u['duong_di'])
        if key != last:
            ref = sorted(read_by_path.get((u['dataset'], m, u['duong_di']), ()))
            out.append('## %s | %s | duong di: %s | da doc o phien 12: %s' % (u['dataset'], u['trang_thai_nguon'], u['duong_di'], [r.split('|')[2] + ('' if r.endswith('single') else ' ' + r.split('|')[3]) for r in ref]))
            last = key
        out.append('  S  ' + head(u))
        out.extend(body(u))
        index.append({'unit_id': u['unit_id'], 'method': m, 'dataset': u['dataset'], 'status': u['trang_thai_nguon'], 'duong_di': u['duong_di']})
    with open(os.path.join(DEST, m + '.txt'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(out) + '\n')
    print(m, len(rows), sum(1 for u in rows if u['trang_thai_nguon'] == 'OK'), sum(len(x) for x in out))
json.dump({'n': len(index), 'units': index}, open(os.path.join(DEST, 'danh-sach.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('tong', len(index), 'OK', sum(1 for i in index if i['status'] == 'OK'))

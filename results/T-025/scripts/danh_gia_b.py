"""T-025 bước 5: evaluator chế độ (b). Nơi duy nhất của T-025 đọc nhãn; chỉ chạy sau khi danh sách bản ghi đã chốt.

Đọc đúng các bản ghi trong `ban-ghi-dua-vao-cham.json` (kiểm SHA-256 từng tệp), rồi mới nạp nhãn.
- Phát hiện (§7.4, SPEC bước 5 sửa U1): theo ca trên 30 ca (ca bộ phát hiện không OK = không phát hiện, trượt);
  theo cửa sổ 60 s, báo động sai mỗi giờ, độ trễ, số thông báo: chỉ trên ca OK ("có điều kiện trên n ca OK").
- RCA tại t̂ (§7.5, §8): thành công chung trên 30 ca (t̂ ≥ t_tiêm và root trong top-k, quy tắc hòa §8.4; ca không có
  lượt RCA hoặc báo động đầu sai = trượt); độ đo §8 trên ca có lượt RCA, tách t̂ đúng/sai; TORAI trung bình 3 seed
  theo ca trước khi gộp; CIRCA kèm nhóm ca không có nút RHT > 1e10 trong bản ghi tại t̂ (luật §6.5, WHY-36).
- Bootstrap theo cặp ô (§8.8) cho thành công chung.

python danh_gia_b.py <ban-ghi-dua-vao-cham.json> <thư mục ra> [doi_moc=0] [nhan_tep=<tệp nhãn giả>]
doi_moc: cộng vào mốc tiêm trong evaluator (phép thử §11.8 / phép thử giả); không đổi bản ghi đầu vào.
nhan_tep: chỉ cho chạy khô với nhãn giả (SPEC, Kiểm đúng đắn); mặc định nhãn thật results/T-022/nhan-dev.json.
"""
import json
import statistics
import sys
from pathlib import Path

import chung
from p3 import danh_gia, nhan

NHAN = chung.ROOT / 'results/T-022/nhan-dev.json'
UNIVERSE = chung.ROOT / 'results/T-022/mappings/universe-re2tt-dev.json'
KS = (1, 3, 5)
NGUONG_CIRCA = 1e10


def doc_danh_sach(p):
    doc = json.loads(Path(p).read_text(encoding='utf-8'))
    out = {'bo_phat_hien': {}, 'rca': {}}
    for it in doc['ban_ghi']:
        f = chung.ROOT / it['duong_dan']
        if chung.sha256_file(f) != it['sha256']:
            raise SystemExit(f'SHA-256 sai: {it["duong_dan"]}')
        r = json.loads(f.read_text(encoding='utf-8'))
        if it['loai'] == 'bo_phat_hien':
            out['bo_phat_hien'].setdefault(it['nhom'], {})[r['opaque_id']] = r
        else:
            out['rca'].setdefault(it['nhom'], []).append(r)
    return doc, out


def tom_so(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    return {'n': len(xs), 'trung_vi': statistics.median(xs), 'tb': sum(xs) / len(xs), 'min': min(xs), 'max': max(xs)}


def phat_hien(recs, lab, ids):
    """recs: {oid: bản ghi bộ phát hiện}; lab: nhãn (đã cộng doi_moc nếu có)."""
    ca, tong = {}, {'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0, 'bo': 0, 'cat_ngang_moc': 0}
    sai = giay = 0
    tb_sai = tb_dung = 0
    for oid in ids:
        r = recs.get(oid)
        st = r['status'] if r else 'TIMEOUT'
        ti = lab[oid]['inject_time']
        row = {'status': st, 'phat_hien_ca': False}
        if st == 'OK':
            c = danh_gia.cham_phat_hien(r['times'], r['alarms'], ti, r['bat_dau_danh_gia'])
            row.update(c)
            for k in tong:
                tong[k] += c['cua_so'][k]
            sai += c['bao_dong_sai']
            giay += c['giay_binh_thuong_danh_gia']
            tb = r['luot_rca']['thong_bao']
            row['t_hat'] = r['luot_rca']['t_hat']
            row['t_hat_dung'] = row['t_hat'] is not None and row['t_hat'] >= ti
            row['thong_bao'] = {'tong': len(tb), 'truoc_tiem': sum(a < ti for a in tb), 'sau_tiem': sum(a >= ti for a in tb)}
            tb_sai += row['thong_bao']['truoc_tiem']
            tb_dung += row['thong_bao']['sau_tiem']
        ca[oid] = row
    ok = [o for o in ids if ca[o]['status'] == 'OK']
    p = tong['tp'] / (tong['tp'] + tong['fp']) if tong['tp'] + tong['fp'] else None
    rc = tong['tp'] / (tong['tp'] + tong['fn']) if tong['tp'] + tong['fn'] else None
    agg = {
        'so_ca': len(ids), 'trang_thai': {s: sum(ca[o]['status'] == s for o in ids) for s in danh_gia.TRANG_THAI},
        'theo_ca_tren_30': {'phat_hien': sum(ca[o]['phat_hien_ca'] for o in ids),
                            'ty_le': sum(ca[o]['phat_hien_ca'] for o in ids) / len(ids),
                            'bao_dong_dau_dung': sum(bool(ca[o].get('t_hat_dung')) for o in ids),
                            'khong_bao_dong': sum(ca[o]['status'] == 'OK' and ca[o].get('t_hat') is None for o in ids)},
        'co_dieu_kien_tren_ca_OK': {
            'n_ca_OK': len(ok), 'cua_so': tong,
            'precision': p, 'recall': rc, 'f1': (2 * p * rc / (p + rc)) if p and rc else (0.0 if p is not None and rc is not None else None),
            'fpr': tong['fp'] / (tong['fp'] + tong['tn']) if tong['fp'] + tong['tn'] else None,
            'bao_dong_sai': sai, 'giay_binh_thuong_danh_gia': giay,
            'bao_dong_sai_moi_gio': sai / giay * 3600 if giay else None,
            'do_tre_s': tom_so([ca[o].get('do_tre_s') for o in ok]),
            'thong_bao_truoc_tiem': tb_sai, 'thong_bao_sau_tiem': tb_dung,
            'thong_bao_sai_moi_gio': tb_sai / giay * 3600 if giay else None,
            'thong_bao_moi_ca': tom_so([ca[o]['thong_bao']['tong'] for o in ok]),
            'so_bao_dong_moi_ca': tom_so([len(recs[o]['alarms']) for o in ok]),
        }}
    return agg, ca


def theo_nhom_phat_hien(ca, lab, truong):
    out = {}
    for oid, row in ca.items():
        g = out.setdefault(lab[oid][truong], {'n': 0, 'phat_hien': 0, 'bao_dong_dau_dung': 0, 'OK': 0})
        g['n'] += 1
        g['phat_hien'] += row['phat_hien_ca']
        g['bao_dong_dau_dung'] += bool(row.get('t_hat_dung'))
        g['OK'] += row['status'] == 'OK'
    return dict(sorted(out.items()))


def vuot_nguong_circa(rec):
    nodes = (rec.get('diagnostics') or {}).get('nodes') or {}
    return any(float(v.get('rht_score', 0)) > NGUONG_CIRCA for v in nodes.values())


DO_DO_SO = tuple(f'hit@{k}' for k in range(1, 11)) + ('rr', 'ndcg@5', 'avg@5')


def trung_binh(ds):
    """Trung bình độ đo theo seed của một ca (TORAI 3 seed), trước khi gộp (§8.8).
    Cận lạc quan/bi quan: seed không có root (opt/pes None, mọi độ đo 0 theo `do_ca`) tính 0 (sửa G3, phiên 2).
    rank_min/rank_max không lấy trung bình; danh sách theo seed nằm ở hang_min/hang_max của ca."""
    n = len(ds)
    out = {k: sum(d[k] for d in ds) / n for k in DO_DO_SO}
    for side in ('opt', 'pes'):
        out[side] = {k: sum((d[side] or {}).get(k, 0.0) for d in ds) / n for k in DO_DO_SO}
    out['rank_min'] = out['rank_max'] = None
    out['status'] = ds[0]['status'] if all(d['status'] == ds[0]['status'] for d in ds) else 'NHIEU:' + ','.join(
        d['status'] for d in ds)
    out['root_trong_tra_ve'] = sum(d['root_trong_tra_ve'] for d in ds) / n
    return out


def dem_trang_thai(per_case):
    """Đếm trạng thái của thành công chung, gồm KHONG_CO_LUOT và BAO_DONG_DAU_SAI (G4, phiên 2)."""
    out = {}
    for v in per_case.values():
        out[v['status']] = out.get(v['status'], 0) + 1
    return dict(sorted(out.items()))


def rca(recs_list, det, lab, ids, U):
    """recs_list: mọi bản ghi RCA của một bộ phát hiện. Trả bảng theo biến thể ranker."""
    by = {}
    for r in recs_list:
        key = 'torai_B' if r['method'] == 'torai' else f'{r["method"]}:{r["variant"]}'
        by.setdefault(key, {}).setdefault(r['opaque_id'], []).append(r)
    out = {}
    for key, per in sorted(by.items()):
        ca, joint, cond_all, cond_dung, cond_sai = {}, {}, {}, {}, {}
        for oid in ids:
            rs = sorted(per.get(oid, []), key=lambda x: (x.get('seed') is None, x.get('seed')))
            d = det.get(oid)
            th = d['luot_rca']['t_hat'] if d and d['status'] == 'OK' else None
            ti = lab[oid]['inject_time']
            root = lab[oid]['root']
            if not rs:
                ca[oid] = {'co_luot_rca': False, 't_hat': th}
                joint[oid] = danh_gia.do_ca({}, False)
                joint[oid]['status'] = 'KHONG_CO_LUOT'
                continue
            if th is None or any(r['window']['t'] != th for r in rs if r.get('window')):
                raise SystemExit(f'{key} {oid}: t của lượt RCA không trùng t̂ của bộ phát hiện')
            per_seed = [danh_gia.cham_ca(r, root) for r in rs]
            m = trung_binh(per_seed) if len(per_seed) > 1 else per_seed[0]
            dung = th >= ti
            row = {'co_luot_rca': True, 't_hat': th, 't_hat_dung': dung, 'status': [r['status'] for r in rs],
                   'seeds': [r.get('seed') for r in rs], 'hang_min': [p['rank_min'] for p in per_seed],
                   'hang_max': [p['rank_max'] for p in per_seed],
                   'hit@1': m['hit@1'], 'hit@3': m['hit@3'], 'hit@5': m['hit@5'], 'rr': m['rr'],
                   'window': {k: (rs[0].get('window') or {}).get(k) for k in ('seconds_N', 'seconds_A', 'rows_N', 'rows_A')},
                   'ngau_nhien_O': [danh_gia.muc_ngau_nhien(r, root, U) for r in rs][0],
                   'bon_tap': danh_gia.bon_tap(rs[0], U) if rs[0]['status'] == 'OK' else None,
                   'chan_doan': [{k: (r.get('diagnostics') or {}).get(k) for k in
                                  ('key_check', 'rank_equals_column_order', 'ty_le_du_phong', 'cum_du_phong')
                                  if k in (r.get('diagnostics') or {})} for r in rs]}
            if key.startswith('circa'):
                row['vuot_1e10'] = vuot_nguong_circa(rs[0])
            ca[oid] = row
            cond_all[oid] = m
            (cond_dung if dung else cond_sai)[oid] = m
            if dung:
                joint[oid] = m
            else:
                joint[oid] = danh_gia.do_ca({}, False)
                joint[oid]['status'] = 'BAO_DONG_DAU_SAI'
        res = {'thanh_cong_chung_tren_30': {f'hit@{k}': sum(joint[o][f'hit@{k}'] for o in ids) / len(ids) for k in KS},
               'thanh_cong_chung_bang_chinh': danh_gia.tong_hop(joint),
               'trang_thai_thanh_cong_chung': dem_trang_thai(joint),
               'so_ca_co_luot_rca': len(cond_all), 'so_ca_t_hat_dung': len(cond_dung), 'so_ca_t_hat_sai': len(cond_sai),
               'tren_ca_co_luot_rca': danh_gia.tong_hop(cond_all) if cond_all else None,
               'tren_ca_t_hat_dung': danh_gia.tong_hop(cond_dung) if cond_dung else None,
               'tai_bao_dong_sai_bao_rieng': danh_gia.tong_hop(cond_sai) if cond_sai else None,
               'theo_loai_loi_thanh_cong_chung': danh_gia.theo_nhom(joint, lab, 'fault'),
               'theo_root_thanh_cong_chung': danh_gia.theo_nhom(joint, lab, 'root'),
               'theo_nhom_vi_tri_thanh_cong_chung': danh_gia.theo_nhom(joint, lab, 'nhom_vi_tri_p75'),
               'theo_o_thanh_cong_chung': danh_gia.theo_nhom(joint, lab, 'cell'),
               'rcaeval_tren_ca_co_luot_rca': rcaeval(per, lab),
               'ngau_nhien_O_tb_hit@1_tren_ca_co_luot': (sum(ca[o]['ngau_nhien_O']['O_hit@1'] for o in cond_all)
                                                         / len(cond_all)) if cond_all else None}
        if key.startswith('circa'):
            ok19 = [o for o in ids if not ca[o].get('vuot_1e10')]
            res['nhom_khong_vuot_1e10'] = {
                'so_ca': len(ok19), 'so_ca_vuot': len(ids) - len(ok19),
                'ca_vuot': sorted(o for o in ids if ca[o].get('vuot_1e10')),
                'thanh_cong_chung': danh_gia.tong_hop({o: joint[o] for o in ok19}) if ok19 else None,
                'tren_ca_co_luot_rca': danh_gia.tong_hop({o: cond_all[o] for o in ok19 if o in cond_all})
                if any(o in cond_all for o in ok19) else None}
            if key.endswith('rht_da'):
                rr = [r for rs in per.values() for r in rs if r['status'] == 'OK']
                routes = {}
                for r in rr:
                    for k2, v in ((r.get('diagnostics') or {}).get('regression_routes') or {}).items():
                        routes[k2] = routes.get(k2, 0) + v
                res['regression_routes_tong'] = routes
        out[key] = {'tong_hop': res, 'ca': ca, '_joint': joint}
    return out


def rcaeval(per, lab):
    """§8.6 (G4, phiên 2): bảng RCAEval riêng trên bản ghi tại t̂ của mọi ca có lượt RCA (có điều kiện, không phải
    thành công chung). Nhiều seed: từng seed riêng."""
    seeds = sorted({r.get('seed') for rs in per.values() for r in rs}, key=lambda x: (x is None, x))
    out = {}
    for sd in seeds:
        recs = {o: r for o, rs in per.items() for r in rs if r.get('seed') == sd}
        out[f'seed={sd}'] = danh_gia.bang_rcaeval(recs, lab)
    return out


def kiem_moc_tren_luoi(data, lab):
    """G4: mốc tiêm (sau doi_moc) phải là một điểm của lưới `times` trong bản ghi bộ phát hiện (bắt sai đơn vị)."""
    for nhom, recs in data['bo_phat_hien'].items():
        for oid, r in recs.items():
            if r.get('times') and lab[oid]['inject_time'] not in set(r['times']):
                raise SystemExit(f'{nhom} {oid}: mốc tiêm không nằm trên lưới times của bản ghi')


def main(ds_path, out_dir, doi_moc='0', nhan_tep=None):
    doc, data = doc_danh_sach(ds_path)  # đọc và kiểm hash bản ghi TRƯỚC khi nạp nhãn
    lab = nhan.nap_nhan(Path(nhan_tep) if nhan_tep else NHAN)
    dm = int(doi_moc)
    for o in lab:
        lab[o]['inject_time'] += dm
    kiem_moc_tren_luoi(data, lab)
    U = json.loads(UNIVERSE.read_text(encoding='utf-8'))['U']
    ids = sorted(lab)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ph = {'mo_ta': 'Phát hiện chế độ (b), §7.4; SPEC T-025 bước 5 (U1).', 'danh_sach': str(ds_path),
          'nhan': str(nhan_tep or NHAN.relative_to(chung.ROOT).as_posix()),
          'src_p3_sha256': doc.get('src_p3_sha256'), 'doi_moc': dm, 'bo_phat_hien': {}}
    for nhom, recs in sorted(data['bo_phat_hien'].items()):
        agg, ca = phat_hien(recs, lab, ids)
        ph['bo_phat_hien'][nhom] = {'tong_hop': agg, 'theo_loai_loi': theo_nhom_phat_hien(ca, lab, 'fault'),
                                    'theo_root': theo_nhom_phat_hien(ca, lab, 'root'),
                                    'theo_o': theo_nhom_phat_hien(ca, lab, 'cell'),
                                    'audit_cot': danh_gia.audit_cot({o: r.get('detector_columns') or []
                                                                     for o, r in recs.items()}), 'ca': ca}
    chung.ghi_json(out / 'phat-hien.json', ph)
    cb = {'mo_ta': 'RCA tại t̂ chế độ (b), §7.5, §8; SPEC T-025.', 'danh_sach': str(ds_path), 'doi_moc': dm,
          'nhan': ph['nhan'],
          'src_p3_sha256': doc.get('src_p3_sha256'), 'theo_bo_phat_hien': {}}
    boot_in, o_cua = {}, {o: lab[o]['cell'] for o in ids}
    for nhom, recs in sorted(data['rca'].items()):
        det = data['bo_phat_hien'][nhom]
        res = rca(recs, det, lab, ids, U)
        for key, v in res.items():
            boot_in[f'{key}[{nhom}]'] = v.pop('_joint')
        cb['theo_bo_phat_hien'][nhom] = res
    cb['bootstrap_thanh_cong_chung'] = danh_gia.bootstrap(boot_in, o_cua) if boot_in else None
    chung.ghi_json(out / 'cham-b.json', cb)
    print(json.dumps({'phat_hien': {k: v['tong_hop']['theo_ca_tren_30'] for k, v in ph['bo_phat_hien'].items()}},
                     ensure_ascii=False))


if __name__ == '__main__':
    kw = dict(a.split('=', 1) for a in sys.argv[3:])
    main(sys.argv[1], sys.argv[2], **kw)

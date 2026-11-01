"""T-045 bước 6 (pha 2 khối K; đọc nhãn sau khi hash pha 1 đã ghi ở LOG): chấm, luật C cho mọi cặp ở P, S_lo, S_hi,
luật chọn khối bước 1–8 và 10, C-d1, C-d3 (chỉ báo cáo), dấu vết E5, mốc giả theo verdict. Dùng nguyên
`m1_danh_gia` (pha2.cham, ket_cuc_cap, dem_moc_gia, mrr_cau_hinh; chon_khoi.chon, kiem_cau_hinh_thang; dau_vet).

- Chấm trên từng phần cấu hình (`tach_cau_hinh.py`) để không nạp tệp 0,9 GB; mỗi phần kiểm hash qua `pha2.doc`, và
  tệp tách phải ghi `tach_tu` đúng hash pha 1 của lượt gốc.
- Nhãn: `results/T-022/nhan-dev.json`, `results/T-026/nhan-dev.json` (kiểm hash), lấy root, ô (cell), loại lỗi (fault).
- E_X: `results/T-043/ks16/dem-sau-ghep-nhan.json#/o_kich_hoat/<thành phần>/<dataset>/o` (định nghĩa băm ở T-043). Cặp
  (R0, c) nhiều thành phần dùng hợp E_X của thành phần đang bật (CĐ6.4).
- δ_d cố định 1/30, 1/22 (Phụ lục C). Vế mốc giả từ lượt mốc giả RE2-TT (`pha2.dem_moc_gia`).
- Từ chối chạy luật C nếu `tai-lap-baseline.json#/dat` không đúng (SPEC bước 6: D2 lệch thì dừng phần phụ thuộc).
Mặc định của bảng SPEC áp tự động; tình huống dừng (bước 7 không còn cấu hình; bước 8 cấu hình thắng không có E1,
E2, E5) chỉ ghi `trinh_Minh`, không tự chọn thay.
Chạy: $PY -B results/T-045/scripts/pha2_khoi_k.py --ra results/T-045/khoi-k.json [--nhan-gia] (nhãn giả chỉ để thử code)
"""
import argparse
import collections
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1_danh_gia import chon_khoi, dau_vet, luat_c, pha2, rr  # noqa: E402

RUNS = ROOT / 'results/T-045/runs'
TP = ['E1', 'E2', 'E3', 'E5']
IT_CA = ['E3']  # ma-tran-thu.json#/buoc/<K>/thanh_phan_it_ca
DO_THI = ['E1', 'E2', 'E5']  # Phụ lục C "Ràng buộc với MRP"
DD = {'RE2-TT': Fraction(1, 30), 'Nezha-OB': Fraction(1, 22)}
LUOT_THAT = ['b2b-k16-re2-001', 'b5-k16-nezha-001']
LUOT_MG = 'b2b-k16-re2-mocgia-001'
NHAN = {'results/T-022/nhan-dev.json': ('RE2-TT', '34846de381e8863b882a49661b02a8a0f8efee6f13103985166199a0d127d269'),
        'results/T-026/nhan-dev.json': ('Nezha-OB', '5127993d0b2016d961ba3382ec8bd353602872a11fcbc4e51c3ae1ecc73c46f4')}
WORLDS = ('P', 'S_lo', 'S_hi')


def f(x):
    return None if x is None else float(x)


def nap_nhan(gia):
    if gia:  # thử code: không đọc tệp nhãn; mã ca từ allowlist, root giả không có trong U, ô giả theo vị trí
        out = {}
        for rel, ds in (('results/T-022/allowlist-dev.json', 'RE2-TT'), ('results/T-026/allowlist-dev.json', 'Nezha-OB')):
            ma = sorted(c['opaque_id'] for c in json.loads((ROOT / rel).read_text(encoding='utf-8'))['cases'])
            for i, o in enumerate(ma):
                out[o] = {'root': 'khong-co', 'dataset': ds, 'o': f'{ds}|{i % 7}', 'loai_loi': 'x'}
        return out
    out = {}
    for rel, (ds, h) in NHAN.items():
        p = ROOT / rel
        if hashlib.sha256(p.read_bytes()).hexdigest() != h:
            raise SystemExit(f'HASH LỆCH: {rel}')
        for c in json.loads(p.read_text(encoding='utf-8'))['cases']:
            out[c['opaque_id']] = {'root': c['root'], 'dataset': ds, 'o': c['cell'], 'loai_loi': c['fault']}
    return out


def nap_E_X(gia):
    """E_X theo thành phần (tệp suy từ nhãn, chỉ đọc ở pha 2); chế độ nhãn giả không đọc tệp."""
    if gia:
        return {x: {f'RE2-TT|{i}' for i in range(7)} for x in TP}
    okh = json.loads((ROOT / 'results/T-043/ks16/dem-sau-ghep-nhan.json').read_text(encoding='utf-8'))['o_kich_hoat']
    return {x: set(okh[x]['RE2-TT']['o']) | set(okh[x]['Nezha-OB']['o']) for x in TP}


def phan_cua(L):
    d = RUNS / L / 'theo-cau-hinh'
    tach = json.loads((d / 'tach.json').read_text(encoding='utf-8'))
    goc = json.loads((RUNS / L / 'pha1.json').read_text(encoding='utf-8'))['sha256']
    if tach['sha256_goc'] != goc or not tach.get('noi_lai_dung_goc'):
        raise SystemExit(f'tệp tách của {L} không khớp lượt gốc')
    return {cid: d / cid for cid in tach['phan']}


def cham_luot(L, nhan):
    out = {}
    for cid, d in sorted(phan_cua(L).items()):
        meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
        out[cid] = pha2.cham(d, meta['sha256'], nhan)['cau_hinh'][cid]
    return out


def doc_ban_ghi(L, cid):
    d = phan_cua(L)[cid]
    return {r['opaque_id']: r for r in (json.loads(x) for x in (d / 'ban-ghi.jsonl').read_text(encoding='utf-8')
                                       .splitlines() if x)}


def ten_k(name):
    return 'K-' + name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    ap.add_argument('--nhan-gia', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    if not a.nhan_gia:
        d2 = json.loads((ROOT / 'results/T-045/tai-lap-baseline.json').read_text(encoding='utf-8'))
        if not d2.get('dat'):
            raise SystemExit('D2 chưa đạt (tai-lap-baseline.json#/dat): dừng luật C theo SPEC bước 6')
    nhan = nap_nhan(a.nhan_gia)
    # chấm
    kq = {'cau_hinh': {}}
    for L in LUOT_THAT:
        for cid, x in cham_luot(L, nhan).items():
            kq['cau_hinh'].setdefault(cid, {'ca': {}})['ca'].update(x['ca'])
    kq_mg = {'cau_hinh': {cid: {'ca': x['ca']} for cid, x in cham_luot(LUOT_MG, nhan).items()}}
    cfg = sorted(kq['cau_hinh'])
    ten_cfg = [c[2:] for c in cfg]
    luu = Path(a.ra).with_suffix('')  # kết quả chấm, cho phép độ bền dùng lại (do_ben.py)
    luu.mkdir(exist_ok=True)
    for ten_tep, x in (('kq.json', kq), ('kq_mg.json', kq_mg)):
        (luu / ten_tep).write_text(json.dumps(pha2.ma_hoa_json(x), ensure_ascii=False) + '\n', encoding='utf-8')
    if len(cfg) != 16 or any(len(kq['cau_hinh'][c]['ca']) != 52 for c in cfg):
        raise SystemExit('khối K không đủ 16 cấu hình × 52 ca')
    # E_X
    E_X = nap_E_X(a.nhan_gia)
    # cặp
    cap, cap_day_du, cap_ds = {}, {}, []
    for name in ten_cfg:
        s = chon_khoi.tap(name)
        ds_cap = []
        if name != 'R0' and len(s) > 1:
            ds_cap.append(('R0', name, luat_c.NHIEU_THANH_PHAN, set().union(*(E_X[x] for x in s))))
        for x in sorted(s):
            ds_cap.append((chon_khoi.ten(s - {x}, TP), name, x, E_X[x]))
        for at, bt, tp, ex in ds_cap:
            k = f'{at}|{bt}'
            if k in cap:
                continue
            mg = pha2.dem_moc_gia(kq_mg, ten_k(at), ten_k(bt))
            v = pha2.ket_cuc_cap(kq, ten_k(at), ten_k(bt), sorted(ex), tp, 'khoi_K', moc_gia=mg[:2],
                                 delta_d_co_dinh=DD)
            cap[k] = v['ket_hop']
            cap_day_du[k] = dict(v, moc_gia_dem={'tat': mg[0], 'bat': mg[1], 'bi_loai': mg[2]['bi_loai']},
                                 thanh_phan=tp, so_o_E_X=len(ex))
            cap_ds.append(k)
    # MRR theo thế giới
    MRR = {w: pha2.mrr_cau_hinh(kq, None, w) for w in WORLDS}
    MRR_ten = {w: {c[2:]: MRR[w][c]['gop'] for c in cfg} for w in WORLDS}
    chon = {'P': chon_khoi.chon(TP, IT_CA, DO_THI, MRR_ten['P'], cap)}
    for w in ('S_lo', 'S_hi'):  # bước 10
        chon[w] = chon_khoi.chon(TP, IT_CA, DO_THI, MRR_ten[w], cap, the_gioi=w)
    thang = chon['P']['chon']
    buoc8 = chon_khoi.kiem_cau_hinh_thang(thang, TP, cap, IT_CA) if thang else None
    # mặc định của bảng SPEC T-045 (dòng 99–109)
    mac_dinh = []
    if thang is None:
        mac_dinh.append({'tinh_huong': 'buoc7_khong_con_cau_hinh', 'hanh_dong': 'DỪNG, trình Minh'})
    else:
        if 'khong_co_thanh_phan_do_thi' in chon['P']['ly_do_trinh_Minh']:
            mac_dinh.append({'tinh_huong': 'buoc8_khong_E1_E2_E5', 'hanh_dong': 'DỪNG, trình Minh'})
        if 'trai_chieu_dataset' in chon['P']['ly_do_trinh_Minh']:
            mac_dinh.append({'tinh_huong': 'buoc6_trai_chieu_dataset', 'hanh_dong': 'giữ cấu hình thắng; gắn cờ; báo MRR từng dataset'})
        if buoc8['xung_dot']:
            mac_dinh.append({'tinh_huong': 'buoc8_ket_cuc_dao_mau_thuan', 'thanh_phan': buoc8['xung_dot'],
                             'hanh_dong': 'giữ cấu hình thắng; ghi xung đột kèm cặp'})
        if buoc8['phu_thuoc_quan_sat']:
            mac_dinh.append({'tinh_huong': 'buoc8_phu_thuoc_quan_sat_khong_it_ca', 'thanh_phan': buoc8['phu_thuoc_quan_sat'],
                             'hanh_dong': 'giữ cấu hình thắng; ghi "phụ thuộc quan sát"'})
        for w in ('S_lo', 'S_hi'):
            if chon[w]['chon'] != thang:
                mac_dinh.append({'tinh_huong': f'buoc10_{w}_khac_P', 'chon_o_the_gioi': chon[w]['chon'],
                                 'hanh_dong': 'giữ lựa chọn tại P; ghi "phụ thuộc quan sát"'})
    trai_chieu_o = sorted(k for k, v in cap.items() if v['ket_cuc_P'] == 'TRAI_CHIEU_O')
    if trai_chieu_o:
        mac_dinh.append({'tinh_huong': 'luatC_buoc7_trai_chieu_o', 'cap': trai_chieu_o,
                         'hanh_dong': 'không là căn cứ loại; ghi cờ'})
    # theo cấu hình: MRR, RR theo ô, M5, Hit@1, mốc giả, C-d1, C-d3
    o_cua = {o: c['o'] for o, c in kq['cau_hinh'][cfg[0]]['ca'].items()}
    ds_cua = {o: c['dataset'] for o, c in kq['cau_hinh'][cfg[0]]['ca'].items()}
    theo_cfg = {}
    for cid in cfg:
        ca = kq['cau_hinh'][cid]['ca']
        rP = {o: c['theo_the_gioi']['P']['RR'] for o, c in ca.items()}
        mg = kq_mg['cau_hinh'][cid]['ca']
        vd = collections.Counter(c['verdict'] for c in mg.values())
        n_mg = sum(v for k, v in vd.items() if k not in ('INSUFFICIENT_EVIDENCE', None))
        theo_cfg[cid] = {
            'MRR': {w: {k: f(v) for k, v in MRR[w][cid].items()} for w in WORLDS},
            'MRR_phan_so': {w: MRR[w][cid] for w in WORLDS},
            'RR_o_P': {o: f(v) for o, v in rr.rr_o(rP, o_cua).items()},
            'ca_M5_P': sum(1 for c in ca.values() if c['theo_the_gioi']['P']['M5']),
            'hit1_P': f(sum((c['theo_the_gioi']['P']['hit1'] for c in ca.values()), Fraction(0))),
            'WORLD_DEPENDENT': kq['cau_hinh'][cid].get('WORLD_DEPENDENT') or sorted(o for o, c in ca.items() if c['WORLD_DEPENDENT']),
            'moc_gia': {'verdict': dict(vd), 'mau_so': n_mg,
                        'ti_le_CAUSE_FOUND': (vd.get('CAUSE_FOUND', 0) / n_mg) if n_mg else None},
            'RR_ca_P': {o: f(v) for o, v in rP.items()}}
    # C-d1, C-d3 (chỉ báo cáo) và dấu vết E5: đọc bản ghi
    for cid in cfg:
        cd = {'C-d1': {}, 'C-d3': {}}
        tt = collections.Counter()
        for L in LUOT_THAT:
            for o, r in doc_ban_ghi(L, cid).items():
                root = nhan[o]['root']
                for m in ('C-d1', 'C-d3'):
                    x = r['extra']['doi_chung'][m]
                    cd[m][o] = rr.rr_ca(x.get('blocks') or [], root, x.get('trang_thai') == 'OK')
                    tt[(m, x.get('trang_thai'))] += 1
        theo_cfg[cid]['doi_chung'] = {
            m: {'MRR_gop': f(sum(v.values(), Fraction(0)) / len(v)),
                **{d: f(sum((v[o] for o in v if ds_cua[o] == d), Fraction(0)) / sum(1 for o in v if ds_cua[o] == d))
                   for d in ('RE2-TT', 'Nezha-OB')}} for m, v in cd.items()}
        theo_cfg[cid]['doi_chung_trang_thai'] = {f'{m}|{s}': n for (m, s), n in tt.items()}
    dau = {}
    for name in ten_cfg:
        s = chon_khoi.tap(name)
        if 'E5' not in s:
            continue
        bo = chon_khoi.ten(s - {'E5'}, TP)
        tong = collections.Counter()
        for L in LUOT_THAT:
            rb, rt = doc_ban_ghi(L, ten_k(name)), doc_ban_ghi(L, ten_k(bo))
            for o in rb:
                x = dau_vet.root_E5_tu_ban_ghi(rt[o], rb[o], nhan[o]['root'])
                tong['ca'] += 1
                tong['root_mat_kenh'] += int(x['mat_kenh_F_raw'][0] > 0)
                tong['root_het_tu_sinh'] += int(x['mat_kenh_F_raw'][1] > 0 and not x['con_tu_sinh'])
                if x['hang_bo_E5'] is not None and x['hang_bat_E5'] is not None:
                    tong['hang_tang'] += int(x['hang_bat_E5'] > x['hang_bo_E5'])
                    tong['hang_giam'] += int(x['hang_bat_E5'] < x['hang_bo_E5'])
        mgr = doc_ban_ghi(LUOT_MG, ten_k(name))
        k, n = 0, 0
        for r in mgr.values():
            a_, b_ = dau_vet.ty_le_ke_thua_lop_lan(r)
            k, n = k + a_, n + b_
        tong['moc_gia_kenh_lan_ke_thua'] = k
        tong['moc_gia_kenh_lan'] = n
        dau[f'{bo}|{name}'] = dict(tong)
    out = {'nhan_gia': a.nhan_gia, 'thanh_phan': TP, 'it_ca': IT_CA, 'do_thi': DO_THI, 'delta_d': DD,
           'E_X_so_o': {x: len(E_X[x]) for x in TP}, 'cau_hinh': theo_cfg,
           'cap': {k: cap_day_du[k] for k in cap_ds}, 'chon_khoi': chon, 'buoc8': buoc8, 'mac_dinh_ap': mac_dinh,
           'dau_vet_E5': dau, 'luot': {'that': LUOT_THAT, 'moc_gia': LUOT_MG}, 'giay': round(time.time() - t0, 1)}
    Path(a.ra).write_text(json.dumps(pha2.ma_hoa_json(out), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'thang': thang, 'gan_tot_nhat': chon['P']['gan_tot_nhat'], 'trinh_Minh': chon['P']['trinh_Minh'],
                      'ly_do': chon['P']['ly_do_trinh_Minh'], 'S_lo': chon['S_lo']['chon'], 'S_hi': chon['S_hi']['chon'],
                      'buoc8': buoc8, 'mac_dinh': [m['tinh_huong'] for m in mac_dinh], 'giay': out['giay']},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

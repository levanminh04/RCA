"""Runner M1 (SPEC T-044 bước 5; SPEC T-043 B4; ma-tran-thu.json; hop-dong.json; dinh-chinh-cai-dat.md CĐ11, CĐ12).

- `ap_dinh_chinh`: áp các đính chính có hiệu lực làm đổi việc sinh cấu hình lên bản sao trong bộ nhớ của
  `ma-tran-thu.json` (file đóng băng giữ nguyên). Đính chính chỉ đổi chữ ghi riêng, không áp.
- `sinh_cau_hinh`: danh sách cấu hình theo bước, từ R0 (chuỗi gốc, D22) và trạng thái chuỗi do bộ đánh giá chốt.
  T13 gồm chuỗi cuối bỏ từng thành phần đang bật và 7 đối chứng (C-a0, C-a1 chạy M1; C-d1, C-d2, C-d3 đọc từ bản
  ghi chuỗi cuối; C-c, C-g tính từ bản ghi P3). C-e là vế mốc giả, không là cấu hình riêng: chạy lại cấu hình của
  cặp ở mốc t − 300 trên RE2-TT (SPEC T-043 B2 C-e; dinh-chinh-phien10.md dòng 73 tách "vế mốc giả C-e").
- `pha1`: chạy phương pháp trên mọi (cấu hình, ca); chặn rò nhãn ở mức giá trị (CĐ12); ghi bản ghi JSON chuẩn hóa
  và hash. Không đọc nhãn. Pha 2 nằm ở m1_danh_gia.pha2.
"""
import copy
import hashlib
import json
import time
from pathlib import Path

from m1 import chuoi, e4, hop_dong

R0 = {'E1': 'tat', 'E2': 'tat', 'E3': False, 'E3b': False, 'E5': False, 'E6': 'a', 'E9': False, 'T12': False}
# hop-dong.json#/vao/params/tham_so_E4 (q_hi, q_lo không có ở ma-tran-thu.json#/co_dinh_moi_buoc/tham_so_E4)
TS_HOP_DONG = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
               'n_exact_max': 100, 'count_min': 10}
KHOI_K = ('E1', 'E2', 'E3', 'E5')
BAT_K = {'E1': 'U', 'E2': 'C', 'E3': True, 'E5': True}
T4_EPS = (0.0, 0.05, 0.2)
# CĐ4, CĐ5: cách khớp mặc định (a); T-045 chốt ở D17 theo D3. Nhóm vòng cách đọc C′ (CĐ3).
TS_E3 = {'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4}
TS_E5 = {'doc_nhom_vong': 'co_vong'}
T4_ALPHA = (0.001, 0.01, 0.05)
DOI_CHUNG_T13 = ('C-a0', 'C-a1', 'C-d1', 'C-d2', 'C-d3', 'C-c', 'C-g')
CHAY_M1 = {'C-a0': True, 'C-a1': True, 'C-d1': False, 'C-d2': False, 'C-d3': False, 'C-c': False, 'C-g': False}
NGUON_DOI_CHUNG = {'C-d1': 'extra.doi_chung của bản ghi chuỗi cuối (CĐ10)',
                   'C-d2': 'extra.doi_chung của bản ghi chuỗi cuối (CĐ10)',
                   'C-d3': 'extra.doi_chung của bản ghi chuỗi cuối (CĐ10)',
                   'C-c': 'doi_chung.cc trên bản ghi P3 của BARO, SimpleRCA M4, TraceRCA lọc hữu hạn',
                   'C-g': 'doi_chung.cg trên phiếu SimpleRCA (T-024, T-026) và cạnh N ∪ A của chuỗi'}

DINH_CHINH = [
    {'ma': 'Đ16', 'nguon': 'results/T-043/dinh-chinh-phien10.md dòng 70',
     'con_tro': '#/buoc/<ma = T13>/so_sanh, #/buoc/<ma = T13>/so_cau_hinh',
     'thay_doi': 'bỏ "C-h" khỏi so_sanh; so_cau_hinh "+ 8 đối chứng" thành "+ 7 đối chứng"'}]
DINH_CHINH_CHI_CHU = [
    {'ma': 'Đ3', 'nguon': 'results/T-043/dinh-chinh-phien8.md dòng 55–65; bị Đ9 (dinh-chinh-phien9.md) thay tiếp',
     'con_tro': '#/co_dinh_moi_buoc/the_gioi', 'ly_do_khong_ap': 'chỉ đổi câu mô tả; chuỗi luôn tính đủ ba thế giới'},
    {'ma': 'Đ7', 'nguon': 'results/T-043/dinh-chinh-phien8.md dòng 124–129', 'con_tro': '#/ngan_sach/thoi_gian',
     'ly_do_khong_ap': 'chỉ đổi câu trỏ mục báo cáo'}]


class LoiRoNhan(ValueError):
    """Mã mờ hay case_dir lọt vào đầu vào của phương pháp (CĐ12)."""


def ap_dinh_chinh(mt):
    mt = copy.deepcopy(mt)
    t13 = next(b for b in mt['buoc'] if b['ma'] == 'T13')
    t13['so_sanh'] = [x for x in t13['so_sanh'] if x != 'C-h']
    t13['so_cau_hinh'] = 'số thành phần đang bật + 7 đối chứng'
    mt['dinh_chinh_da_ap'] = copy.deepcopy(DINH_CHINH)
    mt['dinh_chinh_chi_chu'] = copy.deepcopy(DINH_CHINH_CHI_CHU)
    return mt


def _ts(mt, **doi):
    ts = dict(TS_HOP_DONG)
    ts.update(mt['co_dinh_moi_buoc'].get('tham_so_E4', {}))
    ts.update(doi)
    return ts


def _ma_noi_dung(bat_tat, ts, nhanh_z, ts3, ts5, doi_chung=None):
    d = {'bat_tat': bat_tat, 'tham_so_E4': ts, 'nhanh_z': nhanh_z, 'tham_so_E3': ts3, 'tham_so_E5': ts5}
    if doi_chung is not None:  # C-a0, C-a1 không dựng vùng E7 (S14): khác cấu hình cùng bat_tat
        d['doi_chung'] = doi_chung
    s = json.dumps(d, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def _cau_hinh(buoc, ten, bat_tat, ts, nhanh_z=False, ts3=None, ts5=None, **them):
    bt = dict(R0)
    bt.update(bat_tat)
    ts3, ts5 = dict(ts3 or TS_E3), dict(ts5 or TS_E5)
    out = {'config_id': f'{buoc}-{ten}', 'buoc': buoc, 'bat_tat': bt, 'tham_so_E4': ts, 'nhanh_z': nhanh_z,
           'tham_so_E3': ts3, 'tham_so_E5': ts5, 'ma_noi_dung': _ma_noi_dung(bt, ts, nhanh_z, ts3, ts5, them.get('doi_chung'))}
    out.update(them)
    return out


def _ten_k(bt):
    on = [x for x in KHOI_K if (bt.get(x) not in ('tat', False, None))]
    return '+'.join(on) if on else 'R0'


def _bat(x, v):
    return v not in ('tat', False, None) and not (x == 'E6' and v == 'a')


def sinh_cau_hinh(mt, thang, chuoi_cuoi, nen=None):
    """Cấu hình theo bước của `ma-tran-thu.json` sau khi áp đính chính.
    thang: cấu hình thắng của khối K sau K-b ({E1, E2, E3, E5}); chuoi_cuoi: chuỗi cuối đủ khóa của bat_tat.
    nen: {bước: bat_tat nền} để ghi đè chuỗi tới bước trước của T6, T9, T11, T12; mặc định suy từ thang và chuoi_cuoi
    (T6: thang; T9: thêm E3b của chuỗi cuối; T11: thêm E6; T12: thêm E9)."""
    if 'dinh_chinh_da_ap' not in mt:
        raise ValueError('ma trận chưa áp đính chính')
    ts = _ts(mt)
    out = {}
    out['T1'] = [_cau_hinh('T1', 'R0', {}, ts)]
    out['T4'] = [_cau_hinh('T4', f'e{e}-a{a}', {}, _ts(mt, epsilon=e, alpha=a)) for e in T4_EPS for a in T4_ALPHA]
    out['T4b'] = [_cau_hinh('T4b', 'z', {}, ts, nhanh_z=True)]
    k = []
    for m in range(16):
        bt = {x: (BAT_K[x] if (m >> i) & 1 else R0[x]) for i, x in enumerate(KHOI_K)}
        k.append(_cau_hinh('K', _ten_k(bt), bt, ts))
    out['K'] = sorted(k, key=lambda c: (len(c['config_id']), c['config_id']))
    full = {x: BAT_K[x] for x in KHOI_K}
    kb = []
    thang_bt = {x: thang.get(x, R0[x]) for x in KHOI_K}
    for goc, ten_goc in ((thang_bt, 'thang'), (full, 'day_du')):
        if goc.get('E2') == 'C':
            bt = dict(goc, E2='VC')
            if all(bt != c['bat_tat_k'] for c in kb):
                kb.append(dict(_cau_hinh('K-b', f'{ten_goc}-E2VC', bt, ts), bat_tat_k=bt))
    for c in kb:
        c.pop('bat_tat_k')
    out['K-b'] = kb
    nen = dict(nen or {})
    n6 = nen.get('T6', thang_bt)
    n9 = nen.get('T9', dict(n6, E3b=chuoi_cuoi.get('E3b', False)))
    n11 = nen.get('T11', dict(n9, E6=chuoi_cuoi.get('E6', 'a')))
    n12 = nen.get('T12', dict(n11, E9=chuoi_cuoi.get('E9', False)))
    out['T6'] = [_cau_hinh('T6', 'E3b', dict(n6, E3b=True), ts)]
    out['T9'] = [_cau_hinh('T9', 'E6b', dict(n9, E6='b'), ts, ghi_chu='C-g, C-c chỉ báo cáo')]
    out['T10'] = []
    out['T11'] = [_cau_hinh('T11', 'E9', dict(n11, E9=True), ts)]
    out['T12'] = [_cau_hinh('T12', 'T12', dict(n12, T12=True), ts, can_canh_tinh=True)]
    cuoi = dict(R0)
    cuoi.update(chuoi_cuoi)
    kbo = []
    for x in KHOI_K:
        bt = dict(cuoi)
        bt[x] = R0[x] if _bat(x, cuoi[x]) else BAT_K[x]
        kbo.append(_cau_hinh('KB', f'dao-{x}', bt, ts, can_canh_tinh=bool(bt.get('T12'))))
    out['KB'] = kbo
    t13 = next(b for b in mt['buoc'] if b['ma'] == 'T13')
    dc_t13 = [x for x in t13['so_sanh'] if x != 'C-e']
    if tuple(dc_t13) != DOI_CHUNG_T13:
        raise ValueError(f'danh sách đối chứng T13 khác dự kiến: {dc_t13}')
    l13 = []
    for x in ('E1', 'E2', 'E3', 'E3b', 'E5', 'E6', 'E9', 'T12'):
        if _bat(x, cuoi[x]):
            bt = dict(cuoi)
            bt[x] = R0[x]
            l13.append(_cau_hinh('T13', f'bo-{x if x != "E6" else "E6b"}', bt, ts, can_canh_tinh=bool(bt.get('T12'))))
    for x in dc_t13:
        if x == 'C-a0':
            bt = chuoi.doi_chung_cau_hinh('C-a0', cuoi)
        elif x == 'C-a1':
            bt = chuoi.doi_chung_cau_hinh('C-a1', cuoi)
        else:
            l13.append({'config_id': f'T13-{x}', 'buoc': 'T13', 'doi_chung': x, 'chay_M1': False,
                        'nguon': NGUON_DOI_CHUNG[x]})
            continue
        bt = {k: v for k, v in bt.items() if k != 'E7'}
        l13.append(_cau_hinh('T13', x, bt, ts, doi_chung=x, chay_M1=True))
    out['T13'] = l13
    return out


# ---------------------------------------------------------------- pha 1

def _json(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def _params(cau_hinh, ca):
    p = copy.deepcopy(cau_hinh['params']) if 'params' in cau_hinh else {
        'config_id': cau_hinh['config_id'], 'bat_tat': dict(cau_hinh['bat_tat']),
        'tham_so_E4': dict(cau_hinh['tham_so_E4']), 'nhanh_z': cau_hinh.get('nhanh_z', False),
        'tham_so_E3': dict(cau_hinh.get('tham_so_E3') or TS_E3), 'tham_so_E5': dict(cau_hinh.get('tham_so_E5') or TS_E5),
        'the_gioi': ['P', 'S_lo', 'S_hi']}
    p['config_id'] = cau_hinh['config_id']
    if cau_hinh.get('chay_M1') and cau_hinh.get('doi_chung'):  # C-a0, C-a1: chuỗi không dựng vùng E7 (S14)
        p['doi_chung'] = cau_hinh['doi_chung']
    rieng = ca.get('params_ca') or {}
    if 'doi_chung' in rieng:  # chỉ cấu hình đối chứng C-a0, C-a1 được tắt vùng E7 (S14)
        raise ValueError('params_ca không được mang doi_chung')
    trung = sorted(set(rieng) & set(p))
    if trung:
        raise ValueError(f'params của ca trùng khóa với params của cấu hình: {trung}')
    p.update(copy.deepcopy(rieng))
    return p


def pha1(ca, moc, cau_hinh, thu_muc):
    """ca: [{'opaque_id', 'spans', 'metrics', 'logs', 'inventory', 'aliases', 'params_ca'?, 'case_dir'?, 'chuoi_cam'?}];
    moc: {mã mờ: t} (giây); cau_hinh: [{'config_id', 'params'} hoặc {'config_id', 'bat_tat', 'tham_so_E4', ...}].
    Ghi `ban-ghi.jsonl` (JSON chuẩn hóa, sắp theo cấu hình rồi ca), `pha1.json` (hash) và `thoi-gian.json` (không băm).
    Không đọc nhãn: chỉ nhận mã mờ và mốc t."""
    thu_muc = Path(thu_muc)
    thu_muc.mkdir(parents=True, exist_ok=True)
    cam = sorted({c['opaque_id'] for c in ca} | {c['case_dir'] for c in ca if c.get('case_dir')}
                 | {x for c in ca for x in (c.get('chuoi_cam') or []) if x})
    ds_ch = sorted(cau_hinh, key=lambda c: c['config_id'])
    ds_ca = sorted(ca, key=lambda x: x['opaque_id'])
    for ten, ds_x, k in (('config_id', ds_ch, 'config_id'), ('opaque_id', ds_ca, 'opaque_id')):
        if len({x[k] for x in ds_x}) != len(ds_x):
            raise ValueError(f'{ten} trùng')
    dong_theo, tg = {}, {}
    # ca ở vòng ngoài, cache cổng mới cho mỗi ca: dùng lại giữa các cấu hình của cùng ca, không giữ mẫu của ca đã
    # xong (C8, S38); dòng ghi ra vẫn sắp theo cấu hình rồi ca, nên hash không đổi
    for c in ds_ca:
        chuoi.CACHE = e4.CacheCong()
        for ch in ds_ch:
            p = _params(ch, c)
            vp = hop_dong.vi_pham_gia_tri(p, c.get('aliases') or {}, c.get('inventory') or [], cam)
            if vp:
                raise LoiRoNhan(f'chuỗi cấm trong đầu vào của phương pháp: {sorted(set(x[0] for x in vp))}')
            t0 = time.perf_counter()
            rec = chuoi.chay(c['spans'], c.get('metrics') or [], c.get('logs') or [], c.get('inventory') or [],
                             c.get('aliases') or {}, moc[c['opaque_id']], p)
            tg[f"{ch['config_id']}|{c['opaque_id']}"] = time.perf_counter() - t0
            hop_dong.kiem_ban_ghi(rec)
            dong_theo[(ch['config_id'], c['opaque_id'])] = _json(dict(rec, opaque_id=c['opaque_id']))
    dong = [dong_theo[k] for k in sorted(dong_theo)]
    du_lieu = ('\n'.join(dong) + '\n').encode('utf-8')
    (thu_muc / 'ban-ghi.jsonl').write_bytes(du_lieu)
    h = hashlib.sha256(du_lieu).hexdigest()
    meta = {'tep': 'ban-ghi.jsonl', 'sha256': h, 'so_ban_ghi': len(dong), 'phien_ban': chuoi.PHIEN_BAN,
            'cau_hinh': sorted(c['config_id'] for c in cau_hinh), 'so_ca': len(ca)}
    (thu_muc / 'pha1.json').write_text(_json(meta) + '\n', encoding='utf-8')
    (thu_muc / 'thoi-gian.json').write_text(json.dumps(tg, sort_keys=True, indent=1) + '\n', encoding='utf-8')
    return {'sha256': h, 'so_ban_ghi': len(dong), 'tep': str(thu_muc / 'ban-ghi.jsonl')}

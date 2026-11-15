# -*- coding: utf-8 -*-
"""Bộ chấm T-064 theo `results/T-064/tieu-chi-chon.md` mục 2–3 (quy ước P7(a), `src/p3/danh_gia.py` §8.4).

Chỉ chạy sau khi đầu ra phương pháp đã ghi ra file; là nơi duy nhất ở T-064 đọc nhãn. Không import từ phương pháp.

- Khối/nhóm hòa: `danh_gia.khoi_tu_ban_ghi` (không viết lại; cùng phép kiểm hợp lệ).
- Một đáp án: `danh_gia.phan_bo_hang` (phân bố chính xác dưới hoán vị đều trong nhóm hòa).
- Tập chấp nhận nhiều thành phần: hạng của **thành phần tốt nhất** trong tập = min hạng. Dưới hoán vị đều trong
  nhóm hòa đầu tiên chứa ≥ 1 thành phần chấp nhận (g phần tử, m thành phần chấp nhận), P(min = pos + q) =
  C(g−q, m−1) / C(g, m). Với m = 1 công thức trùng `phan_bo_hang` (kiểm trong `kiem_cham.py`).
- Trạng thái khác `OK`, đáp án vắng: trượt (hạng vô cùng) — tiêu chí mục 2 "Trạng thái đặc biệt".
"""
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

_R = Path(__file__).resolve().parents[2]
if str(_R) not in sys.path:
    sys.path.insert(0, str(_R))
from src.p3 import danh_gia  # noqa: E402

CAT_HANG = 6  # tiêu chí mục 3: tổng hạng kỳ vọng, mỗi ca cắt ở 6


def phan_bo_hang_tap(blocks, tap):
    """Phân bố chính xác của min hạng các thành phần trong `tap`. Không có thành phần nào: {}."""
    tap = set(tap)
    if len(tap) == 1:
        return danh_gia.phan_bo_hang(blocks, next(iter(tap)))
    pos, i = 0, 0
    while i < len(blocks):
        j = i
        while j + 1 < len(blocks) and blocks[j + 1]['key'] == blocks[i]['key']:
            j += 1
        sg = blocks[i:j + 1]
        thanh_vien = [e for b in sg for g in b['groups'] for e in g]
        m = len(tap.intersection(thanh_vien))
        if m:
            if len(sg) != 1 or len(sg[0]['groups']) != 1:
                # Khối cùng khóa nhiều nhóm (TORAI) không xuất hiện ở M1; không đoán, báo lỗi để xử lý riêng.
                raise danh_gia.LoiBanGhi('tập chấp nhận rơi vào siêu khối nhiều nhóm: chưa hỗ trợ')
            g = len(thanh_vien)
            mau = comb(g, m)
            return {pos + q: Fraction(comb(g - q, m - 1), mau) for q in range(1, g - m + 2)}
        pos += len(thanh_vien)
        i = j + 1
    return {}


def cham_ca_loi(rec, tap):
    """Một ca có tiêm lỗi → {'p1','p3','hang_ky_vong','hang_cat','nhom_hang_1','status','trong_tra_ve'}."""
    ok = rec.get('status') == 'OK'
    dist = phan_bo_hang_tap(danh_gia.khoi_tu_ban_ghi(rec), tap) if ok else {}
    if not dist:
        return {'status': rec.get('status'), 'trong_tra_ve': False, 'p1': 0.0, 'p3': 0.0,
                'hang_ky_vong': None, 'hang_cat': float(CAT_HANG), 'nhom_hang_1': nhom_hang_1(rec) if ok else []}
    p1 = sum(p for r, p in dist.items() if r <= 1)
    p3 = sum(p for r, p in dist.items() if r <= 3)
    ev = sum(p * r for r, p in dist.items())
    ev_cat = sum(p * min(r, CAT_HANG) for r, p in dist.items())
    return {'status': 'OK', 'trong_tra_ve': True, 'p1': float(p1), 'p3': float(p3), 'hang_ky_vong': float(ev),
            'hang_cat': float(ev_cat), 'nhom_hang_1': nhom_hang_1(rec),
            'phan_bo': {str(r): str(p) for r, p in sorted(dist.items())}}


def nhom_hang_1(rec):
    blocks = danh_gia.khoi_tu_ban_ghi(rec)
    return [e for g in blocks[0]['groups'] for e in g] if blocks else []


def cham_ca_khong_loi(rec):
    """K đếm thô: mọi kết luận khác NO_INTRINSIC_ANOMALY (kể cả lỗi chạy) tính 1."""
    v = rec.get('verdict') if rec.get('status') == 'OK' else f"STATUS:{rec.get('status')}"
    return {'verdict': v, 'k': int(v != 'NO_INTRINSIC_ANOMALY')}


def tong_hop(ca_loi):
    """ca_loi: {ma: cham_ca_loi}. Trả AC@1, AC@3, tổng hạng kỳ vọng cắt 6."""
    v = list(ca_loi.values())
    return {'n': len(v), 'AC@1': sum(x['p1'] for x in v), 'AC@3': sum(x['p3'] for x in v),
            'tong_hang_cat': sum(x['hang_cat'] for x in v)}


def so_sanh(x, y, eps=1e-9):
    """Tiêu chí mục 3: trả 'tot_len' | 'xau_di' | 'bang' của bản x so với y theo thứ tự AC@1, AC@3, tổng hạng (nhỏ hơn tốt)."""
    for k, dau in (('AC@1', 1), ('AC@3', 1), ('tong_hang_cat', -1)):
        d = (x[k] - y[k]) * dau
        if abs(d) >= eps:
            return 'tot_len' if d > 0 else 'xau_di'
    return 'bang'


def khong_xau_di(x, y, eps=1e-9):
    return x['AC@1'] >= y['AC@1'] - eps and x['AC@3'] >= y['AC@3'] - eps


def tut_qua_2_bac(ca_x, ca_y):
    """Danh sách ca có hạng kỳ vọng của x tụt quá 2 bậc so với y (tiêu chí mục 3, điều kiện chung).

    Dùng hạng kỳ vọng không cắt; ca trượt (không có trong trả về / lỗi chạy) = vô cùng. Trượt ở cả hai bản: không tính tụt.
    """
    inf = float('inf')
    hx = {m: (v['hang_ky_vong'] if v['hang_ky_vong'] is not None else inf) for m, v in ca_x.items()}
    hy = {m: (v['hang_ky_vong'] if v['hang_ky_vong'] is not None else inf) for m, v in ca_y.items()}
    return [m for m in ca_x if hx[m] != hy[m] and (hx[m] - hy[m] > 2 + 1e-9)]


def chieu_canh_ve_nut(rec):
    """Tiêu chí mục 2 "Bản có đầu ra cạnh": một cạnh ở hạng k cho hai đầu nút hạng k nếu chúng chưa có hạng tốt hơn.
    Hạng nút ban đầu = vị trí đầu nhóm hòa trong `entity_ranking` (1-based). Trả bản ghi mới chỉ thay `entity_ranking`
    (nhóm theo hạng sau chiếu; khóa = −hạng) để chấm như bản không cạnh. Không có `canh_xep_hang`: trả nguyên bản ghi."""
    canh = ((rec.get('extra') or {}).get('m1_ft') or {}).get('canh_xep_hang')
    if rec.get('status') != 'OK' or not canh:
        return rec
    hang, vt = {}, 0
    blocks = danh_gia.khoi_tu_ban_ghi(rec)
    for b in blocks:
        tv = [e for g in b['groups'] for e in g]
        for e in tv:
            hang[e] = vt + 1
        vt += len(tv)
    for c in canh:
        if not c.get('co'):
            continue
        for e in (c['nguon'], c['dich']):
            if c['hang'] < hang.get(e, float('inf')):
                hang[e] = c['hang']
    thu_tu = sorted(hang, key=lambda e: (hang[e], e))
    nhom, er = {}, []
    for e in thu_tu:
        g = nhom.setdefault(hang[e], len(nhom))
        er.append({'entity': e, 'key': [-float(hang[e])], 'tie_group': g})
    out = dict(rec); out['entity_ranking'] = er; out.pop('blocks', None)
    return out


def cham_canh(rec, canh_dung):
    """Bảng cạnh: hạng kỳ vọng (dưới hoán vị đều trong nhóm hòa) của đúng cạnh có hướng và loại.
    canh_dung = (nguon, dich, loai). Bản không có đầu ra cạnh: 'UNSUPPORTED'."""
    canh = ((rec.get('extra') or {}).get('m1_ft') or {}).get('canh_xep_hang')
    if canh is None:
        return {'trang_thai': 'UNSUPPORTED'}
    a, b, loai = canh_dung
    idx = [i for i, c in enumerate(canh) if (c['nguon'], c['dich'], c['loai']) == (a, b, loai)]
    if not idx:
        return {'trang_thai': 'VANG', 'top3': 0.0, 'hang_ky_vong': None}
    c = canh[idx[0]]
    cung = [x for x in canh if x['tie_group'] == c['tie_group']]
    lo = min(x['hang'] for x in cung); g = len(cung)
    hk = lo + (g - 1) / 2
    top3 = sum(1 for q in range(1, g + 1) if lo + q - 1 <= 3) / g
    return {'trang_thai': 'OK', 'hang_ky_vong': hk, 'top3': top3, 'co': c['co'], 'diem': c['diem']}

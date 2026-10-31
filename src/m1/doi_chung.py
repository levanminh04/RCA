"""Đối chứng (SPEC T-043 B2 bảng đối chứng; đặc tả v1 §8; Đ11, Đ12; dinh-chinh-cai-dat.md CĐ10). Chỉ báo cáo.

- C-d1 (CĐ10): nhóm 1 = thực thể có cờ mà không bên được gọi nào có cờ; nhóm 2 = thực thể có cờ còn lại;
  nhóm 3 = có kênh OK, không cờ. Trong nhóm xếp theo K_raw; hòa theo khóa chính xác.
- C-d2 (Đ11): khởi phát của thực thể = khởi phát sớm nhất trong các đơn vị phân vị bất thường; sớm hơn đứng trước;
  cùng khởi phát thì K_raw lớn hơn đứng trước; không khởi phát xếp sau mọi thực thể có khởi phát, hòa theo K_raw.
- C-d3 (thẻ đọc PetShop 2e96f93): đảo đồ thị gọi; ứng viên = nút bất thường không có cha nhân quả bất thường;
  điểm = tổng lớn nhất trên đường đơn tới đích qua toàn nút bất thường (gồm ứng viên và đích); chạy riêng từng đích,
  gộp max. Chu trình: UNSUPPORTED_CYCLIC; không đích: NO_TARGET; không ứng viên có điểm: NO_EVIDENCE.
  Đích chế độ (a): chủ span gốc (parent rỗng) trong A có bất thường lớp lan ngược. Điểm nút = K_raw,₁.
- C-g: SimpleRCA cộng bước E6b; danh sách trả về đúng tập SimpleRCA trả.
- C-c: RRF k = 60 trên ba baseline không dùng quan hệ; hạng trung bình trong nhóm hòa; danh sách ERROR đóng góp 0.
Khối theo quy ước src/p3/danh_gia: mỗi nhóm hòa một khối, khóa giảm ngặt.
"""
import math
from fractions import Fraction

import networkx as nx

from m1 import xep_hang


def _khoi(items):
    """items: [(thực thể, khóa)] → khối; khóa bằng nhau là hòa; trong nhóm sắp theo tên chỉ để hiển thị."""
    items = xep_hang.sap_khoa(items)
    return xep_hang._nhom(items)


def _q(x):
    """Số dùng để so khóa: số nguyên giữ nguyên, Fraction giữ nguyên, số thực đổi sang giá trị đúng (S20)."""
    if isinstance(x, (int, Fraction)) and not isinstance(x, bool):
        return x
    return Fraction(float(x))


def _theo_e(kenh):
    co = {}
    for k in kenh:
        if k.co:
            co.setdefault(k.thuc_the, []).append(k)
    return co


# ---------------------------------------------------------------- C-d1

def cd1(kenh, canh, quan_sat):
    co = _theo_e(kenh)
    V = set(co)
    K = {e: xep_hang.khoa_q(co.get(e, [])) for e in V | set(quan_sat)}
    goi_co = {a for a, b in canh if a != b and a in V and b in V}
    items = []
    for e in sorted(K):
        if e in V:
            nhom = 2 if e in goi_co else 1
        else:
            nhom = 3
        items.append((e, (3 - nhom,) + tuple(K[e])))
    blocks = _khoi(items)
    return {'trang_thai': 'OK' if blocks else 'NO_EVIDENCE', 'blocks': blocks}


# ---------------------------------------------------------------- C-d2

def cd2(thuc_the):
    """thuc_the: [(tên, khởi phát hoặc None, K_raw)] với K_raw là bộ (max s, số kênh, Σs) hoặc phần đầu của nó."""
    items = []
    for ten, kp, K in thuc_the:
        K = tuple(Fraction(_q(x)) for x in K)  # khóa ghi ra là số thực ở mọi phần, như trước (_thuc)
        items.append((ten, (Fraction(1), -Fraction(_q(kp))) + K if kp is not None else (Fraction(0), Fraction(0)) + K))
    blocks = _khoi(items)
    return {'trang_thai': 'OK' if blocks else 'NO_EVIDENCE', 'blocks': blocks}


def cd2_tu_kenh(kenh, quan_sat):
    co = _theo_e(kenh)
    out = []
    for e in sorted(set(co) | set(quan_sat)):
        ds = co.get(e, [])
        kp = [k.khoi_phat for k in ds if k.loai == 'phan_vi' and k.khoi_phat is not None]
        out.append((e, min(kp) if kp else None, xep_hang.khoa_q(ds)))
    kq = cd2(out)
    kq['so_thuc_the_co_khoi_phat'] = sum(1 for _, kp, _ in out if kp is not None)
    kq['so_thuc_the_co_co'] = len(co)
    return kq


# ---------------------------------------------------------------- C-d3

def dich_cd3(spans_A, bat_thuong_lan_nguoc):
    """Đích chế độ (a): chủ span gốc (parent rỗng) trong A và có bất thường lớp lan ngược. Span mồ côi không là gốc."""
    goc = {s['chu'] for s in spans_A if s.get('parent') in (None, '')}
    return sorted(goc & set(bat_thuong_lan_nguoc))


def cd3(canh_goi, diem, dich):
    """canh_goi: [(bên gọi, bên được gọi)]; diem: {thực thể bất thường: K_raw,₁}; dich: [đích]."""
    if not dich:
        return {'trang_thai': 'NO_TARGET', 'diem_ung_vien': {}, 'blocks': []}
    bt = set(diem)
    G = nx.DiGraph()
    G.add_nodes_from(sorted(bt | set(dich) | {x for c in canh_goi for x in c}))
    G.add_edges_from(sorted({(b, a) for a, b in canh_goi if a != b}))  # chiều nhân quả: bên được gọi → bên gọi
    H = G.subgraph(sorted(bt))
    if not nx.is_directed_acyclic_graph(H):
        return {'trang_thai': 'UNSUPPORTED_CYCLIC', 'diem_ung_vien': {}, 'blocks': []}
    ung = sorted(v for v in bt if not any(p in bt for p in G.predecessors(v)))
    diem_ung = {}
    for d in sorted(dich):
        for c in ung:
            best = None
            for path in nx.all_simple_paths(G, c, d):
                if all(x in bt for x in path):
                    s = sum((_q(diem[x]) for x in path), Fraction(0))  # cộng chính xác (S20)
                    best = s if best is None or s > best else best
            if best is not None:
                diem_ung[c] = max(diem_ung.get(c, best), best)
    if not diem_ung:
        return {'trang_thai': 'NO_EVIDENCE', 'diem_ung_vien': {}, 'blocks': [], 'ung_vien': ung}
    blocks = _khoi([(e, (s,)) for e, s in diem_ung.items()])
    return {'trang_thai': 'OK', 'diem_ung_vien': {e: float(s) for e, s in diem_ung.items()}, 'blocks': blocks,
            'ung_vien': ung}


# ---------------------------------------------------------------- C-g

def cg(phieu, thu_tu_SimpleRCA, canh):
    """phieu: {thực thể: số phiếu SimpleRCA}; thu_tu_SimpleRCA: [nhóm hòa] theo bản ghi P3; canh: N ∪ A của chuỗi."""
    if not thu_tu_SimpleRCA:
        return {'trang_thai': 'NO_EVIDENCE', 'blocks': []}
    tap = [e for g in thu_tu_SimpleRCA for e in g]
    max_p = max((phieu.get(e, 0) for e in tap), default=0)
    if max_p <= 0:
        n = len(thu_tu_SimpleRCA)
        return {'trang_thai': 'OK', 'ghi_chu': 'tong_s_g_bang_0',
                'blocks': [{'key': [float(n - i)], 'groups': [sorted(g)]} for i, g in enumerate(thu_tu_SimpleRCA)]}
    s_g = {e: phieu.get(e, 0) / max_p for e in tap}
    duong = sorted(e for e in tap if s_g[e] > 0)
    pi = xep_hang.pagerank(duong, s_g, set(canh or ()))
    items = [(e, (xep_hang._lam_tron_12(pi[e]), s_g[e])) for e in duong]
    blocks = _khoi(items)
    khong = sorted(e for e in tap if s_g[e] <= 0)
    if khong:
        blocks.append({'key': [0.0, 0.0], 'groups': [khong]})
    return {'trang_thai': 'OK', 'blocks': blocks, 'pi': pi, 's_g': s_g}


# ---------------------------------------------------------------- C-c

def _hang_trung_binh(ds):
    out, pos = {}, 0
    for g in ds:
        n = len(g)
        r = Fraction(2 * pos + n + 1, 2)  # (pos + 1 + pos + n) / 2
        for e in g:
            out[e] = r
        pos += n
    return out


def cc(danh_sach, k=60):
    """danh_sach: {baseline: [nhóm hòa] hoặc None (ERROR)}. Điểm RRF chính xác (Fraction); khối theo điểm."""
    diem = {}
    for ten in sorted(danh_sach):
        ds = danh_sach[ten]
        if not ds:
            continue
        for e, r in _hang_trung_binh(ds).items():
            diem[e] = diem.get(e, Fraction(0)) + 1 / (k + r)
    if not diem:
        return {'trang_thai': 'NO_EVIDENCE', 'diem': {}, 'blocks': []}
    theo = {}
    for e, v in diem.items():
        theo.setdefault(v, []).append(e)
    blocks = [{'key': [float(v)], 'groups': [sorted(theo[v])]} for v in sorted(theo, reverse=True)]
    return {'trang_thai': 'OK', 'diem': {e: float(v) for e, v in diem.items()},
            'diem_chinh_xac': {e: str(v) for e, v in diem.items()}, 'blocks': blocks}

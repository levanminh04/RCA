"""WORLD_DEPENDENT (bộ đánh giá tính sau ghép nhãn; SPEC T-043 B1.3b): ca có thứ hạng root khác nhau giữa ba thế giới.
Kèm nguyên nhân: có cổng đổi kết quả hay chỉ điểm đổi, kênh đổi giữa các thế giới, phần khóa phân định quan hệ và cặp
đơn vị làm đổi quan hệ với root."""
from m1_danh_gia import rr


def world_dependent(blocks_theo_the_gioi, root):
    pb = {w: rr.phan_bo(b, root) for w, b in blocks_theo_the_gioi.items()}
    vals = {w: tuple(sorted(d.items())) for w, d in pb.items()}
    return {'WORLD_DEPENDENT': len(set(vals.values())) > 1,
            'hang_ky_vong': {w: rr.hang_ky_vong(b, root) for w, b in blocks_theo_the_gioi.items()}}


def _g(k, ten):
    """Đọc trường của kênh: đối tượng Kenh hoặc dict của bản ghi (extra.kenh_co_the_gioi). Mã kênh đọc từ khóa 'ma'
    của bản ghi (gồm đơn vị, S12); không dựng lại từ tên."""
    if isinstance(k, dict):
        if ten == 'co':
            return True  # bản ghi chỉ lưu kênh có cờ
        if ten == 'F_raw':
            return 1
        return k.get(ten) if ten == 'F_I' else k[ten]
    return getattr(k, ten, None)


# Tên các phần của khóa khối theo độ dài khóa: E6a (3 − tầng, K) và E6b (π, K_I, K_raw); xep_hang.xep.
TEN_KHOA = {4: ('tang', 'max_s', 'so_kenh', 'tong_s'),
            7: ('pi', 'K_I.max_s', 'K_I.so_kenh', 'K_I.tong_s', 'K_raw.max_s', 'K_raw.so_kenh', 'K_raw.tong_s')}


def _vi_tri(blocks):
    out = {}
    for bi, b in enumerate(blocks):
        for gi, g in enumerate(b['groups']):
            for e in g:
                out[e] = (bi, gi, tuple(float(x) for x in (b['key'] if isinstance(b['key'], (list, tuple))
                                                           else [b['key']])))
    return out


def _truoc_han(a, r):
    """a chắc chắn đứng trước r: khối khóa lớn hơn, hoặc cùng khối và nhóm đứng trước (như codebook T-028 §4)."""
    if a[0] == r[0]:
        return a[1] < r[1]
    return a[2] > r[2]


def _quan_he(v, e, root):
    """Quan hệ của e với root trong một thế giới: 'truoc' (chắc chắn đứng trước), 'sau', 'hoa' (không bên nào chắc
    chắn đứng trước), 'vang' (e không được xếp)."""
    if e not in v:
        return 'vang'
    if _truoc_han(v[e], v[root]):
        return 'truoc'
    if _truoc_han(v[root], v[e]):
        return 'sau'
    return 'hoa'


def _phan_khoa(v, e, root):
    """Phần đầu tiên của khóa xếp hạng mà e và root khác nhau trong một thế giới: {'chi_so', 'ten'}; None khi một bên
    vắng hoặc hai khóa bằng nhau."""
    if e not in v or root not in v:
        return None
    ke, kr = v[e][2], v[root][2]
    for i, (a, b) in enumerate(zip(ke, kr)):
        if a != b:
            ten = TEN_KHOA.get(len(ke), ())
            return {'chi_so': i, 'ten': ten[i] if i < len(ten) else f'k{i}'}
    return None


def _trang_thai(ks, e):
    """{mã kênh: trạng thái} của các kênh có cờ của e; trạng thái = điểm s và F_I (None khi đầu vào không có F_I)."""
    return {_g(k, 'ma'): {'s': float(_g(k, 's')), 'F_I': _g(k, 'F_I')}
            for k in ks if _g(k, 'thuc_the') == e and _g(k, 'co')}


def nguyen_nhan(kenh_theo_the_gioi, root, blocks_theo_the_gioi):
    """Giải thích WORLD_DEPENDENT (SPEC T-043 B1.3b, dòng 464; dinh-chinh-cai-dat.md S13). kenh_theo_the_gioi:
    {thế giới: [kênh]}.
    - 'loai': 'cong_doi' khi cờ của một kênh đổi giữa các thế giới, ngược lại 'chi_diem_doi'.
    - 'theo_the_gioi'[w], cho mỗi thế giới w khác P mà quan hệ với root đổi:
      'doi' = [{'thuc_the', 'P': quan hệ ở P, w: quan hệ ở w}] cho mọi thực thể (xếp ở P hoặc ở w) mà quan hệ với root
      đổi; quan hệ là 'truoc', 'hoa', 'sau', 'vang' (`_quan_he`), nên gồm cả đảo thứ tự, vào/ra nhóm hòa, xuất
      hiện/vắng. 'vuot' = thực thể thành 'truoc' ở w mà ở P không 'truoc'; 'bi_vuot' = ngược lại.
      'kenh_doi' = {thực thể: [{'ma', 'P': trạng thái ở P, w: trạng thái ở w}]} cho root và các thực thể trong 'doi':
      kênh xuất hiện, mất cờ, đổi điểm hoặc đổi F_I giữa P và w (trạng thái None khi kênh không có cờ ở thế giới đó).
      'phan_khoa' = [{'thuc_the', 'P', w}]: phần của khóa xếp hạng phân định quan hệ e–root ở mỗi thế giới
      (`_phan_khoa`).
      'cap' = [((root, [mã]), (e, [mã]))] cho các thực thể trong 'doi'. [mã] của một thực thể là các kênh đổi của nó;
      khi nó không có kênh đổi, là kênh có điểm lớn nhất ở w (ở P nếu vắng ở w), tức kênh không đổi đứng trong cặp.
      'khong_co_kenh_doi' = True khi root và mọi thực thể trong 'doi' đều không có kênh đổi: quan hệ đổi do thực thể
      khác (ví dụ khối lượng PageRank ở E6b), không do kênh của cặp.
      Root vắng ở một trong hai thế giới thì ghi 'root_vang'. Không có thay đổi thì không có mục.
    - 'cap': cặp đầu tiên (thế giới theo tên, rồi thực thể theo tên), hoặc None.
    Quy tắc "đứng trước hẳn" của cờ M5 (m5.py) giữ riêng."""
    co = {w: {_g(k, 'ma'): _g(k, 'F_raw') for k in ks if _g(k, 'co')} for w, ks in kenh_theo_the_gioi.items()}
    ma_all = set().union(*[set(v) for v in co.values()]) if co else set()
    cong_doi = any(len({co[w].get(m, 0) for w in co}) > 1 for m in ma_all)

    def kenh_doi(w, e):
        a = _trang_thai(kenh_theo_the_gioi.get('P', []), e)
        b = _trang_thai(kenh_theo_the_gioi.get(w, []), e)
        return [{'ma': m, 'P': a.get(m), w: b.get(m)} for m in sorted(set(a) | set(b)) if a.get(m) != b.get(m)]

    def manh(w, e):
        for ww in (w, 'P'):
            ks = [k for k in kenh_theo_the_gioi.get(ww, []) if _g(k, 'thuc_the') == e and _g(k, 'co')]
            if ks:
                return [_g(max(ks, key=lambda k: (float(_g(k, 's')), _g(k, 'ma'))), 'ma')]
        return []

    def don_vi(w, e, kd):
        return [x['ma'] for x in kd] if kd else manh(w, e)

    vP = _vi_tri(blocks_theo_the_gioi['P'])
    theo, cap = {}, None
    for w in sorted(blocks_theo_the_gioi):
        if w == 'P':
            continue
        vw = _vi_tri(blocks_theo_the_gioi[w])
        if (root in vP) != (root in vw):
            theo[w] = {'root_vang': 'P' if root not in vP else w, 'doi': [], 'vuot': [], 'bi_vuot': [], 'cap': [],
                       'kenh_doi': {root: kenh_doi(w, root)}, 'phan_khoa': [], 'khong_co_kenh_doi': False}
            continue
        if root not in vP:
            continue
        doi = []
        for e in sorted((set(vP) | set(vw)) - {root}):
            qp, qw = _quan_he(vP, e, root), _quan_he(vw, e, root)
            if qp != qw:
                doi.append({'thuc_the': e, 'P': qp, w: qw})
        if not doi:
            continue
        vuot = [d['thuc_the'] for d in doi if d[w] == 'truoc']
        bi_vuot = [d['thuc_the'] for d in doi if d['P'] == 'truoc']
        kd = {x: kenh_doi(w, x) for x in [root] + [d['thuc_the'] for d in doi]}
        c = [((root, don_vi(w, root, kd[root])), (d['thuc_the'], don_vi(w, d['thuc_the'], kd[d['thuc_the']])))
             for d in doi]
        pk = [{'thuc_the': d['thuc_the'], 'P': _phan_khoa(vP, d['thuc_the'], root),
               w: _phan_khoa(vw, d['thuc_the'], root)} for d in doi]
        theo[w] = {'doi': doi, 'vuot': vuot, 'bi_vuot': bi_vuot, 'cap': c, 'kenh_doi': kd, 'phan_khoa': pk,
                   'khong_co_kenh_doi': not any(kd.values())}
        if cap is None and c:
            cap = c[0]
    return {'loai': 'cong_doi' if cong_doi else 'chi_diem_doi', 'cap': cap, 'theo_the_gioi': theo}

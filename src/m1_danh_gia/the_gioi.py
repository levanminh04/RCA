"""WORLD_DEPENDENT (bộ đánh giá tính sau ghép nhãn; SPEC T-043 B1.3b): ca có thứ hạng root khác nhau giữa ba thế giới.
Kèm nguyên nhân: có cổng đổi kết quả hay chỉ điểm đổi, và cặp đơn vị làm đảo thứ tự."""
from m1_danh_gia import rr


def world_dependent(blocks_theo_the_gioi, root):
    pb = {w: rr.phan_bo(b, root) for w, b in blocks_theo_the_gioi.items()}
    vals = {w: tuple(sorted(d.items())) for w, d in pb.items()}
    return {'WORLD_DEPENDENT': len(set(vals.values())) > 1,
            'hang_ky_vong': {w: rr.hang_ky_vong(b, root) for w, b in blocks_theo_the_gioi.items()}}


def _g(k, ten):
    """Đọc trường của kênh: đối tượng Kenh hoặc dict của bản ghi (extra.kenh_co_the_gioi)."""
    if isinstance(k, dict):
        if ten == 'ma':
            return f"{k['thuc_the']}|{k['ten']}|{k['huong']}"
        if ten == 'co':
            return True  # bản ghi chỉ lưu kênh có cờ
        if ten == 'F_raw':
            return 1
        return k[ten]
    return getattr(k, ten)


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


def nguyen_nhan(kenh_theo_the_gioi, root, blocks_theo_the_gioi):
    """Giải thích WORLD_DEPENDENT (SPEC T-043 B1.3b, dòng 464). kenh_theo_the_gioi: {thế giới: [kênh]}.
    - 'loai': 'cong_doi' khi cờ của một kênh đổi giữa các thế giới, ngược lại 'chi_diem_doi'.
    - 'theo_the_gioi'[w]: 'vuot' = thực thể chắc chắn đứng trước root ở w mà không chắc chắn đứng trước ở P;
      'bi_vuot' = ngược lại; 'cap' = [((root, kênh mạnh nhất của root ở w), (e, kênh mạnh nhất của e ở w))].
      Root vắng ở một trong hai thế giới thì ghi 'root_vang'. Không có thay đổi thì không có mục.
    - 'cap': cặp đầu tiên (thế giới theo tên, rồi thực thể theo tên), hoặc None."""
    co = {w: {_g(k, 'ma'): _g(k, 'F_raw') for k in ks if _g(k, 'co')} for w, ks in kenh_theo_the_gioi.items()}
    ma_all = set().union(*[set(v) for v in co.values()]) if co else set()
    cong_doi = any(len({co[w].get(m, 0) for w in co}) > 1 for m in ma_all)

    def manh(w, e):
        ks = [k for k in kenh_theo_the_gioi.get(w, []) if _g(k, 'thuc_the') == e and _g(k, 'co')]
        if not ks:
            return None
        return _g(max(ks, key=lambda k: (float(_g(k, 's')), _g(k, 'ten'))), 'ten')

    vP = _vi_tri(blocks_theo_the_gioi['P'])
    theo, cap = {}, None
    for w in sorted(blocks_theo_the_gioi):
        if w == 'P':
            continue
        vw = _vi_tri(blocks_theo_the_gioi[w])
        if (root in vP) != (root in vw):
            theo[w] = {'root_vang': 'P' if root not in vP else w, 'vuot': [], 'bi_vuot': [], 'cap': []}
            continue
        if root not in vP:
            continue
        chung = sorted((set(vP) & set(vw)) - {root})
        vuot = [e for e in chung if _truoc_han(vw[e], vw[root]) and not _truoc_han(vP[e], vP[root])]
        bi_vuot = [e for e in chung if _truoc_han(vP[e], vP[root]) and not _truoc_han(vw[e], vw[root])]
        if not (vuot or bi_vuot):
            continue
        c = [((root, manh(w, root)), (e, manh(w, e))) for e in sorted(vuot + bi_vuot)]
        theo[w] = {'vuot': vuot, 'bi_vuot': bi_vuot, 'cap': c}
        if cap is None and c:
            cap = c[0]
    return {'loai': 'cong_doi' if cong_doi else 'chi_diem_doi', 'cap': cap, 'theo_the_gioi': theo}

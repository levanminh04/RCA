"""WORLD_DEPENDENT (bộ đánh giá tính sau ghép nhãn; SPEC T-043 B1.3b): ca có thứ hạng root khác nhau giữa ba thế giới.
Kèm nguyên nhân: có cổng đổi kết quả hay chỉ điểm đổi, và cặp đơn vị làm đảo thứ tự."""
from m1_danh_gia import rr


def world_dependent(blocks_theo_the_gioi, root):
    pb = {w: rr.phan_bo(b, root) for w, b in blocks_theo_the_gioi.items()}
    vals = {w: tuple(sorted(d.items())) for w, d in pb.items()}
    return {'WORLD_DEPENDENT': len(set(vals.values())) > 1,
            'hang_ky_vong': {w: rr.hang_ky_vong(b, root) for w, b in blocks_theo_the_gioi.items()}}


def nguyen_nhan(kenh_theo_the_gioi, root, blocks_theo_the_gioi):
    """kenh_theo_the_gioi: {thế giới: [Kenh]}. 'cong_doi' khi cờ F_raw của một kênh đổi giữa các thế giới, ngược lại
    'chi_diem_doi'. Cặp: kênh mạnh nhất của root và kênh mạnh nhất của thực thể vượt root ở thế giới khác P."""
    co = {w: {k.ma: k.F_raw for k in ks} for w, ks in kenh_theo_the_gioi.items()}
    ma_all = set().union(*[set(v) for v in co.values()])
    cong_doi = any(len({co[w].get(m, 0) for w in co}) > 1 for m in ma_all)
    cap = None
    for w, b in blocks_theo_the_gioi.items():
        if w == 'P':
            continue
        thu_tu = [e for blk in b for g in blk['groups'] for e in g]
        if root in thu_tu and thu_tu.index(root) > 0:
            vuot = thu_tu[0]
            def manh(e):
                ks = [k for k in kenh_theo_the_gioi[w] if k.thuc_the == e and k.co]
                return max(ks, key=lambda k: (k.s, k.ten)).ten if ks else None
            cap = ((root, manh(root)), (vuot, manh(vuot)))
            break
    return {'loai': 'cong_doi' if cong_doi else 'chi_diem_doi', 'cap': cap}

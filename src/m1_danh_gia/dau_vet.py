"""Dấu vết E5 phía bộ đánh giá (SPEC T-043 B4 khối K; fixture 80). Chạy sau ghép nhãn, từ cặp (c bỏ E5, c).

- root mất kênh nào: (số kênh F_raw = 1 của root bị E5 coi là kế thừa, số kênh F_raw = 1 của root);
- còn tự sinh: root còn kênh F_I = 1;
- hạng kỳ vọng của root trước và sau E5.
Ở mốc giả: số kênh F_raw lớp lan bị coi là kế thừa trên tổng số kênh F_raw lớp lan (từ bản ghi, không cần nhãn).
"""
from m1_danh_gia import rr


def _so(x):
    if x is None:
        return None
    return int(x) if x.denominator == 1 else float(x)


def root_E5(kenh, F_I, blocks_bo, blocks_bat, root):
    """kenh: [Kenh] của c; F_I: {mã kênh: 0/1} của c (E5 bật); blocks của c bỏ E5 và của c."""
    co = [k for k in kenh if k.co and k.thuc_the == root]
    mat = sum(1 for k in co if F_I.get(k.ma, 1) == 0)
    return {'mat_kenh_F_raw': [mat, len(co)], 'con_tu_sinh': any(F_I.get(k.ma, 1) == 1 for k in co),
            'hang_bo_E5': _so(rr.hang_ky_vong(blocks_bo, root)), 'hang_bat_E5': _so(rr.hang_ky_vong(blocks_bat, root))}


def root_E5_tu_ban_ghi(rec_bo, rec_bat, root):
    """Như root_E5, đọc kênh có cờ của thế giới P từ bản ghi M1 (extra.kenh_co)."""
    co = [k for k in rec_bat['extra']['kenh_co'] if k['thuc_the'] == root]
    mat = sum(1 for k in co if k['F_I'] == 0)
    return {'mat_kenh_F_raw': [mat, len(co)], 'con_tu_sinh': any(k['F_I'] == 1 for k in co),
            'kenh_mat': sorted(k['ma'] for k in co if k['F_I'] == 0),  # mã kênh gồm đơn vị (S12)
            'hang_bo_E5': _so(rr.hang_ky_vong(rec_bo['extra']['blocks_P'] or [], root)),
            'hang_bat_E5': _so(rr.hang_ky_vong(rec_bat['extra']['blocks_P'] or [], root))}


def ty_le_ke_thua_lop_lan(rec):
    """(số kênh F_raw lớp lan có F_I = 0, số kênh F_raw lớp lan) ở thế giới P của một bản ghi."""
    lan = [k for k in rec['extra']['kenh_co'] if k['lop'] in ('lan_nguoc', 'lan_xuoi')]
    return sum(1 for k in lan if k['F_I'] == 0), len(lan)

"""Vế mốc giả C-e của luật C (SPEC T-043 B2 C-e, Phụ lục C "Vế mốc giả"; D17; D2f). Chạy sau ghép nhãn.

- Cặp (tắt, bật) theo cửa sổ giả; "bị báo" = verdict CAUSE_FOUND.
- Mẫu số: cặp mà cả hai nhánh khác INSUFFICIENT_EVIDENCE; số cặp bị loại báo riêng.
- Mẫu số 0: CHUA_KIEM_DUOC, không áp (không coi là tỷ lệ 0).
- 1 − tỷ lệ nhánh tắt ≤ 0,10: KHONG_PHAN_XU_DUOC (không có nghĩa là đã đạt).
- Tăng > 0,10: HAI. Còn lại: KHONG_KICH_HOAT. So sánh bằng phân số chính xác.
"""
from fractions import Fraction

NGUONG = Fraction(1, 10)


def ve_tu_dem(tat, bat):
    """tat, bat: (số CAUSE_FOUND, mẫu số n) của hai nhánh trên cùng mẫu số."""
    c_t, n = tat
    c_b, n_b = bat
    if n != n_b:
        raise ValueError('hai nhánh khác mẫu số')
    if n == 0:
        return {'ve': 'CHUA_KIEM_DUOC', 'n': 0, 'ty_le_tat': None, 'ty_le_bat': None, 'tang': None}
    r_t, r_b = Fraction(c_t, n), Fraction(c_b, n)
    tang = r_b - r_t
    if 1 - r_t <= NGUONG:
        ve = 'KHONG_PHAN_XU_DUOC'
    elif tang > NGUONG:
        ve = 'HAI'
    else:
        ve = 'KHONG_KICH_HOAT'
    return {'ve': ve, 'n': n, 'ty_le_tat': float(r_t), 'ty_le_bat': float(r_b), 'tang': float(tang)}


def ve_moc_gia(cap):
    """cap: [(verdict nhánh tắt, verdict nhánh bật)] theo cửa sổ giả."""
    giu = [(a, b) for a, b in cap if a != 'INSUFFICIENT_EVIDENCE' and b != 'INSUFFICIENT_EVIDENCE']
    n = len(giu)
    kq = ve_tu_dem((sum(a == 'CAUSE_FOUND' for a, _ in giu), n), (sum(b == 'CAUSE_FOUND' for _, b in giu), n))
    kq.update({'mau_so': n, 'bi_loai': len(cap) - n, 'HAI': kq['ve'] == 'HAI'})
    return kq

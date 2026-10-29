"""E9 — phủ quyết theo thứ tự thời gian (SPEC T-043 B2 E9; đặc tả v1 §7.11 sửa bởi Đ11; dinh-chinh-cai-dat.md CĐ9).

- Khởi phát chỉ xác định cho đơn vị phân vị: đầu ô o_s giây đầu tiên trong A (lưới ô đặt từ t) mà tỷ lệ mẫu vượt
  ngưỡng hướng d trong ô lớn hơn r_d(N); ô không có mẫu bỏ qua. Đơn vị đếm không có khởi phát.
- Phủ quyết khi và chỉ khi e có khởi phát, mọi b ∈ B(e) có khởi phát, và khởi phát của e sớm hơn khởi phát của từng
  b quá 2 ô cộng τ. Thiếu khởi phát: không phủ quyết, lý do 'khong_du_khoi_phat'.
"""
import math


def khoi_phat(moc_A, gia_tri_A, nguong, r_N, t, huong, o_s=10):
    o = {}
    for m, x in zip(moc_A, gia_tri_A):
        if m < t:
            continue
        k = math.floor((m - t) / o_s)
        v = o.setdefault(k, [0, 0])
        v[0] += 1
        v[1] += int(x > nguong if huong == 'len' else x < nguong)
    for k in sorted(o):
        n, vuot = o[k]
        if vuot / n > r_N:
            return t + k * o_s
    return None


def phu_quyet(kp_e, kp_B, o_s=10, tau=0.001):
    if kp_e is None or not kp_B or any(b is None for b in kp_B):
        return False, 'khong_du_khoi_phat'
    if all(b - kp_e > 2 * o_s + tau for b in kp_B):
        return True, 'da_xet_phu_quyet'
    return False, 'da_xet_khong_phu_quyet'

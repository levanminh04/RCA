"""Ứng viên T-053: giữ đường native, tính lại khi trung gian tràn."""
import math
from fractions import Fraction

from m1 import e4

NATIVE = e4.diem_z


def _float_or_inf(value):
    try:
        return float(value)
    except OverflowError:
        return math.inf if value > 0 else -math.inf


def diem_z(normal, anomalous, *, record=None):
    with e4.np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            return NATIVE(normal, anomalous)
        except FloatingPointError as exc:
            cause = str(exc)

    # Không áp dụng ứng viên cho đầu vào ngoài miền mẫu hữu hạn của SPEC.
    values = sorted(map(float, normal))
    active = list(map(float, anomalous))
    if not all(map(math.isfinite, values + active)):
        return NATIVE(normal, anomalous)

    def quartile(numerator):
        index, remainder = divmod((len(values) - 1) * numerator, 4)
        left = Fraction(values[index])
        if remainder == 0:
            return left
        return left + (Fraction(values[index + 1]) - left) * remainder / 4

    median = quartile(2)
    iqr = quartile(3) - quartile(1)
    scale = iqr if iqr >= Fraction(10 * e4.EPS_MACH) else Fraction(1)
    up = (Fraction(max(active)) - median) / scale
    down = (median - Fraction(min(active))) / scale
    z_up, z_down = map(_float_or_inf, (up, down))
    finite = math.isfinite(z_up) and math.isfinite(z_down)
    if record is not None:
        record(dict(native_error=cause, exact=[str(x) for x in (median, iqr, scale, up, down)],
                    z_final_representable=finite))
    if not finite:
        return NATIVE(normal, anomalous)
    return dict(med_N=float(median), IQR=_float_or_inf(iqr), c=_float_or_inf(scale),
                z_len=z_up, z_xuong=z_down, huu_han=True)

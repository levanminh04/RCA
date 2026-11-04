"""Oracle độc lập và tái lập fixture native T-048, không đọc dữ liệu dev."""
import hashlib
import json
import math
import sys
import warnings
from decimal import Decimal, localcontext
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "results/T-044/tests")]

from m1 import chuoi, e4, xep_hang
from m1.kieu import Kenh
from test_k12_luot4 import _ca_metric
from z_on_dinh import diem_z


def oracle(normal, anomalous):
    with localcontext() as ctx:
        ctx.prec = 2500
        values = sorted(Decimal.from_float(float(x)) for x in normal)
        active = [Decimal.from_float(float(x)) for x in anomalous]

        def q(p):
            index = (len(values) - 1) * Decimal(p)
            left, right = math.floor(index), math.ceil(index)
            if left == right:
                return values[left]
            return (right - index) * values[left] + (index - left) * values[right]

        median = q("0.5")
        iqr = q("0.75") - q("0.25")
        scale = iqr if iqr >= 10 * Decimal.from_float(sys.float_info.epsilon) else Decimal(1)
        return tuple(map(float, (median, iqr, scale, (max(active) - median) / scale,
                                 (median - min(active)) / scale)))


def run():
    prefix = "results/T-048/"
    fixture_path = prefix + "runs/kiem-cuc-tri-z-001/command.json"
    manifest = json.loads((ROOT / (prefix + "manifest.json")).read_bytes())
    fixture_bytes = (ROOT / fixture_path).read_bytes()
    expected = manifest["closed_outputs"][fixture_path]
    if isinstance(expected, dict):
        expected = expected["sha256"]
    assert hashlib.sha256(fixture_bytes).hexdigest() == expected
    fixture = json.loads(fixture_bytes)
    samples = fixture["fixtures"] + [
        dict(id="subtraction_recovers_after_division", N=[-1.5e308] * 11 + [-5e307] * 10,
             A=[1.5e308] * 20),
        dict(id="interpolant_recovers", N=[-1e308, 1e308], A=[1e308]),
        dict(id="floor_below", N=[0, 2**-53], A=[-1, 2]),
        dict(id="floor_equal", N=[0, 20 * sys.float_info.epsilon], A=[-1, 2]),
        dict(id="floor_above", N=[0, 2**-47], A=[-1, 2]),
        dict(id="ordinary", N=[0, 1, 2, 7], A=[-5, 30]),
        dict(id="ordinary_tie", N=[2.0] * 11, A=[1.0, 3.0]),
        dict(id="single_direction_native_invalid", N=[1e308] * 11,
             A=[-1e308] + [1.5e308] * 20),
    ]
    checks = {}
    keys = ("med_N", "IQR", "c", "z_len", "z_xuong")
    for item in samples:
        normal, active = item["N"], item["A"]
        oracle_values = oracle(normal, active)
        diagnostics = []
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always")
            native = e4.diem_z(normal, active)
            candidate = diem_z(normal, active, record=diagnostics.append)
        if not diagnostics:
            assert candidate == native
        if all(map(math.isfinite, oracle_values[-2:])):
            assert candidate["huu_han"]
            for key, value in zip(keys, oracle_values, strict=True):
                assert math.isclose(candidate[key], value, rel_tol=2e-15, abs_tol=0)
        else:
            assert candidate["huu_han"] == native["huu_han"]
            assert all(repr(candidate[k]) == repr(native[k]) for k in keys)
        checks[item["id"]] = dict(native=native, candidate=candidate, oracle=dict(zip(keys, oracle_values)),
                                   diagnostic=diagnostics, warnings=[str(w.message) for w in seen])

    # Phép cộng khóa độc lập với lỗi float trong median/IQR/trừ/chia.
    channels = [Kenh("S", f"k{i}", "len", "khong_lan", 1e308) for i in range(2)]
    key = xep_hang.khoa_q(channels)
    with localcontext() as ctx:
        ctx.prec = 2500
        assert Decimal(key[-1].numerator) / key[-1].denominator == 2 * Decimal.from_float(1e308)
    try:
        xep_hang.xep(channels)
    except OverflowError as exc:
        checks["key"] = dict(sum=str(key[-1]), native=type(exc).__name__, message=str(exc))
    else:
        raise AssertionError("Thiếu lỗi native chuyển khóa")

    chain = {}
    for item in fixture["fixtures"]:
        rows, params = _ca_metric(item["N"], item["A"], che_do=fixture["mode"])
        if item.get("two"):
            for row in rows:
                row["S_mem"] = row["S_cpu"]
            params["nguon_metric"]["S_mem"] = "S"
            params["ho_so_nguon"]["kenh_metric"]["bang"]["mem"] = "tài nguyên"
        for mode, scorer in (("E4", e4.diem_z), ("z", e4.diem_z), ("candidate", diem_z)):
            trace = {}
            native_rank = xep_hang.xep

            def rank(channels, **kwargs):
                trace["channels"] = [dict(name=k.ma, F_raw=k.F_raw, hop_le=k.hop_le, score=k.s)
                                     for k in channels]
                return native_rank(channels, **kwargs)

            with warnings.catch_warnings(), patch.object(e4, "diem_z", scorer), patch.object(xep_hang, "xep", rank):
                warnings.simplefilter("ignore", RuntimeWarning)
                result = chuoi.chay([], rows, [], ["S"], {}, 1000, dict(params, nhanh_z=mode != "E4"))
            chain.setdefault(item["id"], {})[mode] = dict(trace=trace, record=result)
    key_case = chain["finite_channels_sum_overflow"]
    assert key_case["E4"]["record"]["status"] == "OK"
    for mode in ("z", "candidate"):
        assert key_case[mode]["record"]["status"] == "ERROR"
        assert "too large" in key_case[mode]["record"]["error"]
        assert sum(c["F_raw"] for c in key_case[mode]["trace"]["channels"]) == 2
    return dict(checks=checks, chain=chain)


def clean(value):
    if isinstance(value, float) and not math.isfinite(value):
        return repr(value)
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


if __name__ == "__main__":
    from m1_danh_gia.pha2 import ma_hoa_json

    print(json.dumps(ma_hoa_json(clean(run())), ensure_ascii=False, sort_keys=True, allow_nan=False, default=str))

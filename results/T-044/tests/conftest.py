"""T-044: khung test. Đáp án đọc từ JSON (SPEC T-044 bước 3, tiêu chí 3); code gọi từ src/m1, src/m1_danh_gia.

- Đặt biến môi trường M1_KET_QUA=<đường dẫn .json> để ghi kết quả từng phép kiểm (mã phép, qua/trượt).
- Mã phép (`ma`) theo `results/T-043/fixture/ket-qua-kiem.json#/ket_qua/*/id` cho 82 fixture; B1–B8, U1–U6,
  H1–H6 theo tên mục; đáp án tự lập theo `id` trong file đáp án của T-044.
"""
import json
import os
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))

T043 = ROOT / 'results' / 'T-043'
T044 = ROOT / 'results' / 'T-044'


def _doc(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


FIXTURE = _doc(T043 / 'fixture-dac-ta.json')
BO_SUNG = _doc(T043 / 'fixture' / 'fixture-bo-sung.json')
DAP_AN_UH = _doc(T044 / 'fixture' / 'dap-an-u-h.json')


def _doc_neu_co(ten):
    p = T044 / 'fixture' / ten
    return _doc(p) if p.exists() else {'muc': []}


DAP_AN_DOI_CHUNG = _doc_neu_co('dap-an-doi-chung.json')
DAP_AN_THANH_PHAN = _doc_neu_co('dap-an-thanh-phan.json')
DAP_AN_VAN_BAN = _doc_neu_co('dap-an-van-ban.json')


def fx(i):
    """Fixture theo id (1–82) của fixture-dac-ta.json."""
    for f in FIXTURE['fixtures']:
        if f['id'] == i:
            return f
    raise KeyError(i)


def bx(ma):
    """Fixture bổ sung B1–B8."""
    for f in BO_SUNG['fixtures']:
        if f['id'] == ma:
            return f
    raise KeyError(ma)


def uh(ma):
    for f in DAP_AN_UH['U'] + DAP_AN_UH['H']:
        if f['id'] == ma:
            return f
    raise KeyError(ma)


def tu_lap(tep, ma):
    """Mục đáp án tự lập (dấu 'đáp án của người làm T-044, chưa qua phản biện')."""
    for m in tep['muc']:
        if m['id'] == ma:
            return m
    raise KeyError(ma)


def mau(chuoi):
    """Đọc cách viết mẫu của fixture: '20x0', '13x0+7x1', '4x[0,1,2,3,4]', '{0..19}x1e-16',
    '1e-14 + {0..19}x1e-16', '2000..2299'. Chỉ là cách đọc đầu vào; không thêm giá trị."""
    s = chuoi.replace(' ', '')
    m = re.fullmatch(r'([0-9.eE+-]+)\+\{(\d+)\.\.(\d+)\}x([0-9.eE+-]+)', s)
    if m:
        c, a, b, k = float(m[1]), int(m[2]), int(m[3]), float(m[4])
        return [c + i * k for i in range(a, b + 1)]
    m = re.fullmatch(r'\{(\d+)\.\.(\d+)\}x([0-9.eE+-]+)', s)
    if m:
        a, b, k = int(m[1]), int(m[2]), float(m[3])
        return [i * k for i in range(a, b + 1)]
    m = re.fullmatch(r'(-?\d+)\.\.(-?\d+)', s)
    if m:
        return [float(i) for i in range(int(m[1]), int(m[2]) + 1)]
    out = []
    for phan in s.split('+'):
        m = re.fullmatch(r'(\d+)x\[([^\]]*)\]', phan)
        if m:
            out += [float(v) for v in m[2].split(',')] * int(m[1])
            continue
        m = re.fullmatch(r'(\d+)x([0-9.eE-]+)', phan)
        if not m:
            raise ValueError(chuoi)
        out += [float(m[2])] * int(m[1])
    return out


def phan_so(x):
    """Số thực của fixture (RR đã làm tròn như 0.3333333333333333) đổi về phân số gần nhất.
    Chỉ dùng để đọc đầu vào RR của fixture luật C; RR do code tính luôn là phân số chính xác."""
    return Fraction(x).limit_denominator(10 ** 6)


def gan_bang(a, b, tol=1e-12):
    return abs(float(a) - float(b)) <= tol


def gan_lam_tron(gia_tri, dap_an):
    """Đáp án thập phân đã làm tròn: lệch không quá nửa đơn vị của chữ số cuối đã ghi (CĐ16)."""
    s = repr(dap_an) if isinstance(dap_an, float) else str(dap_an)
    if 'e' in s or 'E' in s:
        mant, exp = s.lower().split('e')
        so_le = len(mant.split('.')[1]) if '.' in mant else 0
        buoc = 10 ** (int(exp) - so_le)
    else:
        so_le = len(s.split('.')[1]) if '.' in s else 0
        buoc = 10 ** (-so_le)
    return abs(float(gia_tri) - float(dap_an)) <= buoc / 2 + 1e-15


# ---- ghi kết quả từng phép kiểm ----
_KQ = []


def pytest_runtest_logreport(report):
    if report.when != 'call' and not (report.when == 'setup' and report.outcome != 'passed'):
        return
    ma = None
    for k, v in getattr(report, 'user_properties', []):
        if k == 'ma':
            ma = v
    _KQ.append({'test': report.nodeid, 'ma': ma, 'ket_qua': report.outcome})


def pytest_sessionfinish(session, exitstatus):
    p = os.environ.get('M1_KET_QUA')
    if p:
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        Path(p).write_text(json.dumps(_KQ, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


@pytest.fixture
def ma(record_property):
    """Gắn mã phép kiểm vào kết quả: gọi ma('25-cong-oracle')."""
    def _gan(x):
        record_property('ma', x)
    return _gan


# ---- phép tất định (SPEC T-044 bước 6) ----
# M1_XAO=<số nguyên dương>: mọi đầu vào dạng danh sách mà thứ tự không mang nghĩa được xáo (bản sao, không sửa dữ
# liệu test) trước khi vào hàm, ở mọi tầng gọi. Metric của chuoi.chay chỉ xáo khi mọi nguồn dùng "metrics.time",
# vì mốc riêng của nguồn ghép với hàng theo thứ tự (Đ19 điểm 3). Không xáo danh sách có thứ tự mang nghĩa
# (thứ tự SimpleRCA của C-g, danh sách của C-c, thứ tự thành phần của luật chọn khối).
XAO = {
    'm1.chuoi': {'chay': (0, 2, 3)},
    'm1.span': {'chuan_bi': (0,)},
    'm1.e2': {'gan_canh': (0,)},
    'm1.e3': {'hoc_va_dem': (0, 1)},
    'm1.e4': {'cham_phan_vi': (0, 1)},
    'm1.e5': {'phan_loai': (0, 1)},
    'm1.e7': {'vung': (1, 2, 3)},
    'm1.kenh': {'don_vi_log': (0, 1)},
    'm1.xep_hang': {'xep': (0,)},
    'm1.doi_chung': {'cd1': (0, 1), 'cd3': (0,), 'cd2_tu_kenh': (0,), 'cg': (2,)},
    'm1_danh_gia.luat_c': {'ap_dung': (0,)},
    'm1_danh_gia.uv6': {'dem': (0,)},
    'm1_danh_gia.m5': {'G_N_tu_span': (0,)},
    'm1_danh_gia.moc_gia': {'ve_moc_gia': (0,)},
}
TEN_KW = {'canh': True, 'kenh': True}


@pytest.fixture(autouse=True)
def xao_hang(monkeypatch):
    seed = os.environ.get('M1_XAO')
    if not seed or seed == '0':
        yield
        return
    import functools
    import importlib
    import random
    dem = {'n': 0}

    def boc(ten, f, vi_tri):
        @functools.wraps(f)
        def g(*args, **kw):
            dem['n'] += 1
            rng = random.Random(f'{seed}|{ten}|{dem["n"]}')
            args = list(args)
            for i in vi_tri:
                if i < len(args) and isinstance(args[i], list):
                    if ten == 'm1.chuoi.chay' and i == 1:
                        continue
                    x = list(args[i])
                    rng.shuffle(x)
                    args[i] = x
            for k in list(kw):
                if k in TEN_KW and isinstance(kw[k], list):
                    x = list(kw[k])
                    rng.shuffle(x)
                    kw[k] = x
            if ten == 'm1.chuoi.chay' and len(args) >= 7 and isinstance(args[1], list):
                tg = (args[6] or {}).get('thoi_gian_nguon') or {}
                if all(v == 'metrics.time' for v in tg.values()):
                    x = list(args[1])
                    rng.shuffle(x)
                    args[1] = x
            return f(*args, **kw)
        return g

    for mod, ham in XAO.items():
        m = importlib.import_module(mod)
        for h, vi_tri in ham.items():
            monkeypatch.setattr(m, h, boc(f'{mod}.{h}', getattr(m, h), vi_tri))
    yield

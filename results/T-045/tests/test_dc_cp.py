"""ĐC3 (results/T-045/dinh-chinh-cai-dat.md): chuỗi chỉ tính đường găng E1-CP khi E1 = CP. Không đổi kết quả: với
mọi cấu hình của bộ ca tất định T-044 (`tat_dinh.py`, gồm E1 tắt, U, CP), bản ghi giống hệt bản ghi khi buộc tính u_CP."""
import json

import pytest


def test_DC3_chuan_bi_khong_tinh_CP_giu_truong_khac():
    import conftest as c44  # results/T-045/tests/conftest.py (chép FIXTURE của T-044)
    import sinh_trace_S
    from m1 import span
    spans, _ = sinh_trace_S.sinh('S2b', t=1000, mau=c44.FIXTURE['trace_mau_S'])
    a = span.chuan_bi(spans, t=1000 * 10 ** 6, tau=1000)
    b = span.chuan_bi(spans, t=1000 * 10 ** 6, tau=1000, tinh_CP=False)
    assert a['chan_doan'] == b['chan_doan'] and set(a['spans']) == set(b['spans'])
    for k in a['spans']:
        x, y = dict(a['spans'][k]), dict(b['spans'][k])
        assert y.pop('u_CP') is None
        x.pop('u_CP')
        assert x == y


@pytest.mark.parametrize('ten', ['C0', 'C1', 'C2', 'CP', 'E3', 'E6b', 'E9', 'z'])
def test_DC3_ban_ghi_nhu_khi_buoc_tinh_CP(ten, monkeypatch):
    import tat_dinh  # results/T-044/scripts/tat_dinh.py
    from m1 import chuoi, e4, span
    ch = tat_dinh.CAU_HINH[ten]

    def chay_het():
        out = []
        for ma_ca, spans, metrics, logs, them in tat_dinh._ca():
            chuoi.CACHE = e4.CacheCong()
            rec = chuoi.chay(spans, metrics, logs, tat_dinh.U, {}, 1000, tat_dinh._params(ten, ch, them))
            assert not rec.get('error')
            out.append(json.dumps(rec, sort_keys=True, ensure_ascii=False, allow_nan=False))
        return out

    moi = chay_het()
    goc = span.chuan_bi
    monkeypatch.setattr(span, 'chuan_bi', lambda *a, **k: goc(*a, **dict(k, tinh_CP=True)))
    assert chay_het() == moi


@pytest.mark.parametrize('E1, phai_goi', [('tat', False), ('U', False), ('CP', True)])
def test_DC3_chi_tinh_duong_gang_khi_E1_CP(E1, phai_goi, monkeypatch):
    import tat_dinh
    from m1 import chuoi, e4, span
    dem = {'n': 0}
    goc = span.doc_quyen_CP

    def dem_goi(*a, **k):
        dem['n'] += 1
        return goc(*a, **k)
    monkeypatch.setattr(span, 'doc_quyen_CP', dem_goi)
    ma_ca, spans, metrics, logs, them = tat_dinh._ca()[0]
    chuoi.CACHE = e4.CacheCong()
    rec = chuoi.chay(spans, metrics, logs, tat_dinh.U, {}, 1000, tat_dinh._params('x', {'E1': E1}, them))
    assert not rec.get('error') and (dem['n'] > 0) == phai_goi

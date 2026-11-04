"""Kiểm C1 đã áp vào chính API src, không thay hàm bằng ứng viên."""
import random
from m1 import cong


def test_c1_api_src_bat_bien_chuoi_gan_hang():
    a={299-i:.235+(.00000000000000004 if i%3==0 else 0) for i in range(300)}
    expected=cong.tu_tuong_quan(a);keys=list(a);rng=random.Random(20261102)
    for _ in range(25):
        rng.shuffle(keys)
        assert cong.tu_tuong_quan({j:a[j] for j in keys})==expected


def test_c1_api_src_tong_dung_va_khong_phu_thuoc_hang():
    rows=[(j*cong.NS,x) for j in range(30) for x in (1e16,1.,-1e16)]
    rng=random.Random(7);expected=None
    for _ in range(20):
        rng.shuffle(rows)
        result=cong.o_1s([x for x,v in rows],[v for x,v in rows],300*cong.NS,'N')
        assert set(result.values())=={1./3}
        if expected is None:expected=result
        assert result==expected


def test_c1_api_src_giu_dieu_kien_bien():
    assert cong.tu_tuong_quan({i:float(i) for i in range(9)})==(None,'it_o')
    assert cong.tu_tuong_quan({i:1. for i in range(300)})==(None,'phuong_sai_0')

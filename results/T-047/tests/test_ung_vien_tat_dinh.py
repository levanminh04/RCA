"""Chỉ test ứng viên riêng, không thay hàm src đang dùng bởi M1."""
import random
import numpy as np
from m1 import cong
import ung_vien_cong_tat_dinh as candidate


def test_hang_gan_hang_bat_bien_khi_dao_thu_tu_them_dict():
    values=[.235+(.00000000000000004 if i%3==0 else 0) for i in range(300)]
    original={299-i:v for i,v in enumerate(values)}
    reference=candidate.tu_tuong_quan(original)
    rng=random.Random(20261102)
    keys=list(original)
    for _ in range(25):
        rng.shuffle(keys)
        shuffled={j:original[j] for j in keys}
        assert candidate.tu_tuong_quan(shuffled)==reference
    assert cong.tu_tuong_quan(original)==reference


def test_nhieu_mau_moi_o_khong_phu_thuoc_thu_tu_cong():
    t=300*cong.NS
    rows=[]
    for j in range(30):
        for x in (1e16,1.,-1e16):rows.append(((j+1)*cong.NS,x))
    rng=random.Random(0)
    baseline=candidate.o_1s([x for x,v in rows],[v for x,v in rows],t,'N')
    assert set(baseline.values())=={1./3}  # tổng toán học là 1, không chấp nhận mất số hạng nhỏ.
    for _ in range(20):
        rng.shuffle(rows)
        assert candidate.o_1s([x for x,v in rows],[v for x,v in rows],t,'N')==baseline


def test_ton_trong_dieu_kien_it_o_va_phuong_sai_khong():
    assert candidate.tu_tuong_quan({i:float(i) for i in range(9)})==(None,'it_o')
    assert candidate.tu_tuong_quan({i:1. for i in range(300)})==(None,'phuong_sai_0')

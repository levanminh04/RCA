"""Đ5 phục dựng D1 từ sự kiện có burst biết trước; kiểm với chuỗi thật trên ca giả."""
import copy
import pytest
import adapter_t047 as ad
import d5_t047
from m1 import chuoi, runner


def test_phi_burst_va_doi_chieu_record(matrix, synthetic_input):
    case, moc = synthetic_input
    cfg = ad.cau_hinh(matrix, 'T1')[0]
    case['logs'] = [dict(timestamp=(900 if i < 20 else 1100)*10**9,
                         entity='A', message='ERROR burst', severity_raw=None) for i in range(60)]
    case['params_ca']['coverage']['log'] = {'khoang': [[700*10**9, 1300*10**9]], 'r_ns': 10**9}
    rec = chuoi.chay(case['spans'], [], case['logs'], case['inventory'], {}, 1000, runner._params(cfg, case))
    assert rec['status'] == 'OK'
    result = d5_t047.tinh(case, 1000, rec, cfg)
    assert result['so_don_vi_dem_OK_P'] == 1
    u = result['units'][0]
    # 20 sự kiện trong một ô trên 10 ô: s²/mean = 20.
    assert u['phi'] == 20 and u['n_N'] == 20 and len(u['perturbations']) == 9
    assert result['huong_cham'] == ['len'] and u['original']['F_raw_xuong'] == 0
    assert not next(x for x in u['perturbations'] if x['fN'] == x['fA'] == 1)['changed']
    bad = copy.deepcopy(rec)
    bad['worlds']['P']['don_vi_dem'][0]['p_len'] = -1
    with pytest.raises(ValueError, match='lệch bản ghi'):
        d5_t047.tinh(case, 1000, bad, cfg)
    badcase = copy.deepcopy(case)
    badcase['logs'] = badcase['logs'][1:]
    with pytest.raises(ValueError, match='số sự kiện N lệch'):
        d5_t047.tinh(badcase, 1000, rec, cfg)

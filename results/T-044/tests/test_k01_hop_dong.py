"""Khối 1: hợp đồng, bộ kiểm trường cấm (fixture 74); chặn rò nhãn ở mức giá trị (CĐ12)."""
import json

import pytest

from conftest import fx, tu_lap, DAP_AN_THANH_PHAN


def _dung_tuple(x):
    """Fixture 74 viết tuple trong JSON bằng chuỗi 'TUPLE:<json>'; dựng lại tuple thật."""
    if isinstance(x, str) and x.startswith('TUPLE:'):
        return tuple(_dung_tuple(v) for v in json.loads(x[len('TUPLE:'):]))
    if isinstance(x, dict):
        return {k: _dung_tuple(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_dung_tuple(v) for v in x]
    return x


@pytest.mark.parametrize('i', range(4), ids=[f'74-{i + 1}' for i in range(4)])
def test_74_truong_cam(i, ma):
    from m1 import hop_dong
    ca = fx(74)['ca'][i]
    ma(f'74-{i + 1}')
    rec = _dung_tuple(ca['ban_ghi'])
    if i == 2:
        assert isinstance(rec['evidence_refs'], tuple)
    tu_choi = bool(hop_dong.vi_pham_truong_cam(rec))
    assert tu_choi == (ca['dap_an'] == 'TU_CHOI')


def test_ten_cam_dung_hop_dong(ma):
    """Danh sách tên cấm = hop-dong.json#/cam/ten_cam = CAM của ban_ghi cộng FORBIDDEN_LABEL_KEYS của nezha."""
    from m1 import hop_dong
    from p3 import ban_ghi, nezha
    from conftest import T043, _doc
    ma('hop_dong-ten_cam')
    hd = _doc(T043 / 'hop-dong.json')
    assert set(hd['cam']['ten_cam']) == set(ban_ghi.CAM) | set(nezha.FORBIDDEN_LABEL_KEYS)
    assert hop_dong.TEN_CAM == frozenset(hd['cam']['ten_cam'])


@pytest.mark.parametrize('muc', ['GT1', 'GT2', 'GT3', 'GT4'])
def test_ro_gia_tri(muc, ma):
    """CĐ12: mã mờ hay case_dir không được xuất hiện như giá trị trong params, aliases, inventory."""
    from m1 import hop_dong
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    d = m['dau_vao']
    vp = hop_dong.vi_pham_gia_tri(d['params'], d['aliases'], d['inventory'], d['chuoi_cam'])
    assert bool(vp) == m['dap_an']['tu_choi']

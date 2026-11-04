"""Guard phải so cùng tên đã resolve và vẫn chặn đường thoát T047."""
from pathlib import Path
import pytest
import adapter_t047 as ad


@pytest.mark.parametrize('prefix_path,prefix_base', [(True, False), (False, True), (True, True), (False, False)])
def test_guard_cung_ten_win32_sau_resolve(monkeypatch, prefix_path, prefix_base):
    base = str(ad.OUT)
    target = base + '\\runs\\guard-test\\cases\\x'
    def resolve(p):
        s = str(p)
        return Path(('\\\\?\\' if (prefix_base if s == base else prefix_path) else '') + s)
    monkeypatch.setattr(Path, 'resolve', resolve)
    assert ad.duong_ra(target) == Path(target)


@pytest.mark.parametrize('resolved', [r'D:\RCA-flashticket\results\T-047-evil\x',
                                      r'D:\RCA-flashticket\src\x', r'E:\outside\x',
                                      r'\\?\E:\outside\x', r'\\?\UNC\host\share\x'])
def test_guard_van_chan_duong_resolve_ra_ngoai(monkeypatch, resolved):
    base = str(ad.OUT)
    # Tên đầu vào nằm trong T047 nhưng đích resolve ra ngoài (ví dụ junction).
    target = base + '\\runs\\junction\\x'
    monkeypatch.setattr(Path, 'resolve', lambda p: Path(base if str(p) == base else resolved))
    with pytest.raises(ValueError, match='ngoài T-047'):
        ad.duong_ra(target)


def test_guard_thuc_chan_dotdot():
    with pytest.raises(ValueError, match='ngoài T-047'):
        ad.duong_ra(ad.OUT / '..' / '..' / 'src' / 'x')


def test_dang_duong_khong_doi_device_path_la():
    p = Path(r'\\?\GLOBALROOT\Device\HarddiskVolume1\x')
    assert ad._dang_duong_win32(p) == p

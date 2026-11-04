"""Dùng lại ca đúng seed/cấu hình không gọi worker, ca khác seed phải từ chối."""
import json
import time
from types import SimpleNamespace
import pytest
import adapter_t047 as ad
import chay_t047_v3 as d


def setup(monkeypatch,sandbox_adapter,matrix,synthetic_input,name):
    from pathlib import Path
    driver_file=ad.OUT/'scripts/chay_t047_v3.py'
    driver_file.parent.mkdir(parents=True,exist_ok=True)
    driver_file.write_bytes(Path(d.__file__).read_bytes())
    monkeypatch.setattr(d,'__file__',str(driver_file))
    monkeypatch.setattr(d,'ROOT',ad.ROOT)
    monkeypatch.setenv('PYTHONHASHSEED','2')
    case,moc=synthetic_input;cfg=ad.cau_hinh(matrix,'T1')
    src=ad.OUT/'runs/original'
    ad.pha1([case],moc,cfg,src/'cases'/case['opaque_id']/'phase1')
    ad.ghi(src/'cases'/case['opaque_id']/'summary.json',dict(seed='2',fake=False,shuffle=None))
    ad.ghi(ad.OUT/'runs/ngan-sach.json',dict(start_epoch=time.time(),prior_seconds=0,cap_seconds=25200))
    monkeypatch.setattr(d.old,'danh_sach_ca',lambda *a:([('SYNTHETIC',case['opaque_id'])],{},{}))
    monkeypatch.setattr(d,'configs',lambda g:cfg)
    monkeypatch.setattr(d.subprocess,'Popen',lambda *a,**k:pytest.fail('ca dùng lại không được chạy worker'))
    a=SimpleNamespace(run=ad.OUT/('runs/'+name),dataset='all',stage='full',group='T1',workers=3,
                      fake=False,shuffle=None,reuse=src)
    return a,src,case


def test_dung_lai_ca_hop_le_khong_chay_lai(monkeypatch,sandbox_adapter,matrix,synthetic_input):
    a,src,case=setup(monkeypatch,sandbox_adapter,matrix,synthetic_input,'good')
    original=(src/'cases'/case['opaque_id']/'phase1/ban-ghi.jsonl').read_bytes()
    d.control(a)
    assert (a.run/'ban-ghi.jsonl').read_bytes()==original
    r=json.loads((a.run/'result.json').read_text())
    assert r['done']==r['planned']==r['reused']==1 and not r['failed']


def test_tu_choi_khac_seed(monkeypatch,sandbox_adapter,matrix,synthetic_input):
    a,src,case=setup(monkeypatch,sandbox_adapter,matrix,synthetic_input,'bad')
    monkeypatch.setenv('PYTHONHASHSEED','0')
    with pytest.raises(ValueError,match='khác cấu hình/seed'):
        d.control(a)
    assert not (a.run/'cases').exists()

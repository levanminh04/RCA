"""Ghép tuần tự phải khớp pha 1 chung, gồm đủ ma trận và từng byte."""
import copy
from pathlib import Path
import chay_t047_v2 as driver
import adapter_t047 as ad


def test_ghep_tuan_tu_khop_pha1_chung(sandbox_adapter, matrix, synthetic_input):
    case, moc = synthetic_input
    case2 = copy.deepcopy(case)
    case2['opaque_id'] = 'another-synthetic-case'
    all_moc = dict(moc, **{case2['opaque_id']:1000})
    cfg = ad.cau_hinh(matrix, 'K')[:3]
    out = ad.OUT/'runs/stream'
    for c in (case, case2):
        ad.pha1([c], all_moc, cfg, out/'cases'/c['opaque_id']/'phase1')
    merged = driver.merge(out, [('fake',case['opaque_id']), ('fake',case2['opaque_id'])], cfg)
    common = ad.pha1([case2,case], all_moc, cfg, ad.OUT/'runs/common')
    assert merged['sha256'] == common['sha256'] and merged['so_ban_ghi'] == 6
    assert (out/'ban-ghi.jsonl').read_bytes() == (ad.OUT/'runs/common/ban-ghi.jsonl').read_bytes()

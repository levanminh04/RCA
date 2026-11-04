"""Gate trước nhãn, tính toàn vẹn phần tách và mẫu bootstrap không bị bỏ."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import adapter_t047 as ad
import pha2_t047 as driver
from m1 import chuoi, runner


def synthetic_phase1(adapter, name='input'):
    path = adapter.OUT / 'runs' / name
    path.mkdir(parents=True)
    recs = [dict(config_id=cid, opaque_id=oid, status='OK',
                 method_version=chuoi.PHIEN_BAN_CHE_DO, extra=dict(che_do=ad.MODE))
            for cid in ('K-E1', 'K-R0') for oid in ('opaque-a', 'opaque-b')]
    data = ('\n'.join(runner._json(x) for x in recs) + '\n').encode()
    (path / 'ban-ghi.jsonl').write_bytes(data)
    meta = dict(tep='ban-ghi.jsonl', sha256=hashlib.sha256(data).hexdigest(),
                so_ban_ghi=4, so_ca=2, cau_hinh=['K-E1', 'K-R0'])
    (path / 'pha1.json').write_text(json.dumps(meta), encoding='utf-8')
    return path, meta


def test_gate_rejects_before_any_label_or_d2_access(sandbox_adapter, monkeypatch):
    adapter = sandbox_adapter
    path, meta = synthetic_phase1(adapter)
    log = adapter.ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md'
    log.parent.mkdir(parents=True)
    log.write_text('Không có hash\n', encoding='utf-8')
    touched = []
    monkeypatch.setattr(driver.old, 'nap_nhan', lambda *_: touched.append('labels'))
    monkeypatch.setattr(driver.old, 'nap_E_X', lambda *_: touched.append('E_X'))
    monkeypatch.setattr(driver.subprocess, 'run', lambda *_a, **_k: touched.append('D2'))
    args = SimpleNamespace(that=path, ce=path, run=adapter.OUT / 'runs/audit', bootstrap=False)
    with pytest.raises(ValueError, match='chưa ghi LOG'):
        driver.run(args)
    assert not touched and not Path(args.run).exists()
    line = f"- `{path.relative_to(adapter.ROOT).as_posix()}`: `{meta['sha256']}`"
    assert driver.verify_logged({'that': path}, line)['that'] == meta
    # Có dòng LOG vẫn không cho dùng byte đã bị đổi.
    with (path / 'ban-ghi.jsonl').open('ab') as f:
        f.write(b'\n')
    with pytest.raises(ValueError, match='hash/ma trận'):
        driver.verify_logged({'that': path}, line)
    assert not touched


def test_reused_split_must_reconstruct_parent_bytes(sandbox_adapter):
    path, meta = synthetic_phase1(sandbox_adapter)
    result = driver.parts(path, meta)
    assert sorted(result) == meta['cau_hinh']
    assert driver.parts(path, meta) == result
    p, m = result['K-E1']
    # Kẻ sửa đồng thời cả byte và hash phần tách: vẫn phải bị hash gốc chặn.
    rows = [json.loads(x) for x in (p / 'ban-ghi.jsonl').read_text(encoding='utf-8').splitlines()]
    rows[0]['extra']['unapproved'] = True
    data = ('\n'.join(runner._json(x) for x in rows) + '\n').encode()
    (p / 'ban-ghi.jsonl').write_bytes(data)
    m['sha256'] = hashlib.sha256(data).hexdigest()
    (p / 'pha1.json').write_text(json.dumps(m), encoding='utf-8')
    with pytest.raises(ValueError, match='hash gốc'):
        driver.parts(path, meta)


def test_no_graph_and_empty_selection_stop_but_flags_do_not():
    def selected(winner):
        return {'chon_khoi': {'P': {'chon': winner, 'trinh_Minh': True}}}
    assert driver.stop_reason(selected(None)) == 'buoc7_khong_con_cau_hinh'
    assert driver.stop_reason(selected('R0')) == driver.stop_reason(selected('E3')) == 'buoc8_khong_E1_E2_E5'
    assert driver.stop_reason(selected('E1+E3')) is None


def test_bootstrap_preserves_every_unchecked_sample(block_data):
    kq, ce, ex = block_data
    from conftest import ce_rec
    for recs in ce.values():
        for oid in recs:
            recs[oid] = ce_rec(0, True)
    events, samples = [], []
    result = driver.bootstrap(kq, ce, ex, lambda **x: events.append(x), samples.append, n=3)
    assert result['seed'] == 20261102 and result['n'] == 3
    assert len(samples) == sum(result['loai'].values()) == 3
    assert result['tan_suat_co']['Ce_chua_kiem'] == 3
    assert [e['i'] for e in events if e['event'] == 'bootstrap_sample'] == [1, 2, 3]
    assert all(s['chon_khoi']['P']['cap_Ce_chua_kiem'] for s in samples)
    assert all(sum(c.values()) == 3 for c in result['tan_suat_the_gioi'].values())

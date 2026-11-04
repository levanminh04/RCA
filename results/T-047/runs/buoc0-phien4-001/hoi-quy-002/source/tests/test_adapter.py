"""Đường ghi, metadata, lỗi, hash/LOG và chiếu S1→S0 trên dữ liệu giả."""
import copy
import hashlib
import json
from fractions import Fraction as F

import pytest

import adapter_t047 as ad
from m1 import chuoi, hop_dong, runner, xep_hang
from m1.kieu import Kenh
from m1_danh_gia import pha2


@pytest.mark.parametrize('group,count', [('K', 16), ('T1', 1)])
def test_sinh_cau_hinh_day_du_che_do(matrix, group, count):
    original = copy.deepcopy(matrix)
    configs = ad.cau_hinh(matrix, group)
    assert len(configs) == count and len({c['config_id'] for c in configs}) == count
    assert matrix == original
    for c in configs:
        assert c['che_do'] == ad.MODE and runner._params(c, {})['che_do'] == ad.MODE
        raw = {k: v for k, v in c.items() if k != 'ma_noi_dung_T047'}
        assert c['ma_noi_dung_T047'] == hashlib.sha256(runner._json(raw).encode()).hexdigest()
        assert c['tham_so_E3']['khop'] == 'hoan_toan' and c['tham_so_E5']['doc_nhom_vong'] == 'co_vong'
    if group == 'K':
        assert {c['config_id'] for c in configs} == {'K-' + ('+'.join(x) if x else 'R0') for x in
            __import__('itertools').chain.from_iterable(__import__('itertools').combinations(('E1', 'E2', 'E3', 'E5'), n)
                                                       for n in range(5))}


def test_khong_sinh_nhom_ngoai_spec(matrix):
    with pytest.raises(ValueError):
        ad.cau_hinh(matrix, 'T13')


@pytest.mark.parametrize('status', ['OK', 'NO_EVIDENCE'])
def test_che_do_tung_ban_ghi(status):
    rec = {'status': status, 'method_version': chuoi.PHIEN_BAN_CHE_DO, 'extra': {'che_do': dict(ad.MODE)}}
    ad.kiem_ban_ghi(rec)
    for bad in [dict(rec, method_version=chuoi.PHIEN_BAN), dict(rec, extra={}),
                dict(rec, extra={'che_do': dict(ad.MODE, cong_dem='D0')})]:
        with pytest.raises(ValueError, match='chế độ mới'):
            ad.kiem_ban_ghi(bad)
    rec['extra']['nhan'] = {'root': 'A'}
    with pytest.raises(hop_dong.LoiTruongCam):
        ad.kiem_ban_ghi(rec)


@pytest.mark.parametrize('status', ['ERROR', 'UNSUPPORTED', 'ALIEN', None])
def test_trang_thai_truoc_che_do(status):
    # Không có extra/method_version: phải báo trạng thái, không lẫn lỗi cấu hình.
    with pytest.raises(ValueError, match='trạng thái'):
        ad.kiem_ban_ghi({'status': status})


def test_duong_ghi_chan_T045_va_thoat_thu_muc():
    assert ad.duong_ra(ad.OUT / 'runs/test/a.json').is_relative_to(ad.OUT)
    for p in [ad.ROOT / 'results/T-045/a.json', ad.OUT / '../T-045/a.json', ad.ROOT / 'src/a.py', ad.ROOT.parent]:
        with pytest.raises(ValueError):
            ad.duong_ra(p)


def test_pha1_chuoi_gia_hash_metadata_va_LOG(sandbox_adapter, matrix, synthetic_input):
    a = sandbox_adapter
    case, moc = synthetic_input
    configs = a.cau_hinh(matrix, 'T1')
    first, second = a.OUT / 'runs/one', a.OUT / 'runs/two'
    meta = a.pha1([case], moc, configs, first)
    meta2 = a.pha1([case], moc, configs, second)
    assert meta == meta2 and meta['phien_ban'] == chuoi.PHIEN_BAN_CHE_DO
    saved = json.loads((first / 'tham-so.json').read_text(encoding='utf-8'))
    assert saved['configs'] == configs and saved['che_do'] == a.MODE
    assert saved['code_revision'] == 'c298188e' and saved['git_head']
    _, records = pha2.doc(first, meta['sha256'])
    assert len(records) == 1 and records[0]['status'] == 'OK'
    a.kiem_ban_ghi(records[0])
    assert json.loads((first / 'records/00000.json').read_text(encoding='utf-8')) == records[0]
    events = [json.loads(x) for x in (first / 'progress.jsonl').read_text(encoding='utf-8').splitlines()]
    assert [x['event'] for x in events] == ['start', 'start_record', 'record', 'done']
    assert all(x['elapsed'] >= 0 for x in events)
    with pytest.raises(ValueError, match='chưa được ghi LOG'):
        a.kiem_hash_trong_log(first, '')
    log = a.ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md'
    log.parent.mkdir(parents=True); log.write_bytes(b'old log\r\n')
    hashes = a.ghi_hash_log([first])
    assert hashes == {first.relative_to(a.ROOT).as_posix(): meta['sha256']}
    assert log.read_bytes().startswith(b'old log\r\n')
    assert a.kiem_hash_trong_log(first, log.read_text(encoding='utf-8')) == (meta, records)
    with pytest.raises(ValueError):
        a.ghi_hash_log([first], a.OUT / 'wrong-log.md')
    with pytest.raises(FileExistsError):
        a.pha1([case], moc, configs, first)
    (first / 'ban-ghi.jsonl').write_bytes((first / 'ban-ghi.jsonl').read_bytes() + b'\n')
    with pytest.raises(pha2.LoiHash):
        a.kiem_hash_trong_log(first, log.read_text(encoding='utf-8'))


def test_NO_EVIDENCE_thuc_su_van_kiem_che_do(sandbox_adapter, matrix, synthetic_input):
    a = sandbox_adapter; case, moc = synthetic_input
    case['spans'] = []
    path = a.OUT / 'runs/no-evidence'
    meta = a.pha1([case], moc, a.cau_hinh(matrix, 'T1'), path)
    _, records = pha2.doc(path, meta['sha256'])
    assert records[0]['status'] == 'NO_EVIDENCE'
    a.kiem_ban_ghi(records[0])


@pytest.mark.parametrize('status', ['ERROR', 'UNSUPPORTED'])
def test_loi_duoc_giu_va_dung_phat_viec(sandbox_adapter, matrix, synthetic_input, status):
    a = sandbox_adapter; case, moc = synthetic_input
    cfg = a.cau_hinh(matrix, 'T1')[0]
    bad = copy.deepcopy(cfg); bad['config_id'] = 'A-bad'
    if status == 'ERROR':
        bad['params'] = {}  # chuỗi thật trả ERROR, chưa tới chấm
    else:
        bad['bat_tat']['T12'] = True  # chuỗi thật trả UNSUPPORTED vì thiếu cạnh tĩnh
    good = copy.deepcopy(cfg); good['config_id'] = 'Z-next'
    path = a.OUT / ('runs/' + status)
    with pytest.raises(ValueError, match=status):
        a.pha1([case], moc, [good, bad], path)
    records = list((path / 'records').glob('*.json'))
    assert len(records) == 1
    error = json.loads(records[0].read_text(encoding='utf-8'))
    assert error['status'] == status and error['config_id'] == 'A-bad'
    saved = json.loads((path / 'tham-so.json').read_text(encoding='utf-8'))
    assert saved['configs'] == [good, bad] and saved['che_do'] == a.MODE
    assert not (path / 'pha1.json').exists() and not (path / 'ban-ghi.jsonl').exists()
    events = [json.loads(x) for x in (path / 'progress.jsonl').read_text(encoding='utf-8').splitlines()]
    assert sum(x['event'] == 'start_record' for x in events) == 1


def test_pha1_chan_ro_nhan_va_che_do_sai_truoc_chuoi(sandbox_adapter, matrix, synthetic_input):
    a = sandbox_adapter; case, moc = synthetic_input
    config = a.cau_hinh(matrix, 'T1')[0]
    bad = copy.deepcopy(config); bad['che_do']['thang'] = 'E4'
    with pytest.raises(ValueError, match='chế độ sai'):
        a.pha1([case], moc, [bad], a.OUT / 'runs/bad-mode')
    case['aliases']['A'] = 'prefix-' + case['opaque_id']
    with pytest.raises(ValueError, match='chuỗi cấm'):
        a.pha1([case], moc, [config], a.OUT / 'runs/leak')
    assert not list(a.OUT.rglob('records/*.json'))


def test_hash_chua_day_du_khong_duoc_noi_LOG(sandbox_adapter, matrix, synthetic_input):
    a = sandbox_adapter; case, moc = synthetic_input
    path = a.OUT / 'runs/incomplete'
    meta = a.pha1([case], moc, a.cau_hinh(matrix, 'T1'), path)
    meta['so_ban_ghi'] += 1
    (path / 'pha1.json').write_text(json.dumps(meta), encoding='utf-8')
    log = a.ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md'
    log.parent.mkdir(parents=True); log.write_bytes(b'old\n')
    with pytest.raises(pha2.LoiDuLieuPha2):
        a.ghi_hash_log([path])
    assert log.read_bytes() == b'old\n'


def test_phuc_dung_S0_phai_sap_va_gop_lai():
    blocks = [{'key': [2, 1., 9., 1, 1.], 'groups': [['A']]},
              {'key': [2, 1., 8., 2, 2.], 'groups': [['B']]},
              {'key': [2, 1., 7., 1, 1.], 'groups': [['C']]}]
    expected = [{'key': [2, 1., 2, 2.], 'groups': [['B']]},
                {'key': [2, 1., 1, 1.], 'groups': [['A', 'C']]}]
    assert ad.phuc_dung_S0(blocks) == expected


@pytest.mark.parametrize('swap', [False, True])
def test_phuc_dung_bang_xep_hang_S0_truc_tiep(swap):
    kenh = [Kenh('A', 'a1', 'len', 'lan_nguoc', 1.0, F_raw=1),
            Kenh('B', 'b1', 'len', 'lan_nguoc', 1.0, F_raw=1),
            Kenh('B', 'b2', 'len', 'lan_nguoc', 1.0, F_raw=1),
            Kenh('C', 'c1', 'len', 'lan_nguoc', .5, F_raw=1)]
    fi = {k.ma: (0 if swap and k.thuc_the == 'B' else 1) for k in kenh}
    kwargs = dict(F_I=fi, thuc_the_co_kenh_OK=['A', 'B', 'C', 'D'])
    s0 = xep_hang.xep(kenh, **kwargs)['blocks']
    s1 = xep_hang.xep(kenh, khoa_T4c={'A': (9., 9.), 'B': (1., 1.), 'C': (20., 20.)}, **kwargs)['blocks']
    assert s0 != s1 and ad.phuc_dung_S0(s1) == s0


@pytest.mark.parametrize('blocks', [[{'key': [2, 1, 1, 1], 'groups': [['A']]}],
    [{'key': [2, 1, 0, 1, 1], 'groups': [['A'], ['B']]}],
    [{'key': [2, 1, 0, 1, 1], 'groups': [['A', 'A']]}]])
def test_phuc_dung_tu_choi_dau_vao_sai(blocks):
    with pytest.raises(ValueError):
        ad.phuc_dung_S0(blocks)

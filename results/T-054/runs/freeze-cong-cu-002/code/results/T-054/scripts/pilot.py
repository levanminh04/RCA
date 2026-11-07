"""Pilot chỉ sau grant ghim plan; so field chính xác với bản nguồn."""
import copy
import gzip
import json
from pathlib import Path
from bien_nhan import ROOT, Blocked, digest, fingerprint, read_pin


def comparable(record, control=False):
    record = copy.deepcopy(record)
    for k in ('opaque_id', 'config_id', 'variant'):
        record.pop(k, None)
    if control:
        record['region'] = None
    if 'extra' in record:
        record['extra'].pop('dau_vao_cd3', None)
        record['extra'].get('doi_chung', {}).pop('C-d3', None)
    return record


def reference(pin, config_id=None):
    p = Path(pin['path'])
    if not p.is_absolute(): p = ROOT / p
    if p.suffix != '.gz':
        return read_pin(pin)
    if digest(p) != pin['sha256']:
        raise Blocked('native reference khác pin')
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        rows = [json.loads(line) for line in f]
    found = [r for r in rows if r.get('config_id') == config_id]
    if len(found) != 1:
        raise Blocked('native reference thiếu/trùng config')
    return found[0]


def compare(reference_pin, observed, *, source_machine, target_machine, tolerance=None,
            config_id=None, control=False):
    expected = reference(reference_pin, config_id)
    a, b = comparable(expected, control), comparable(observed, control)
    if a == b:
        return {'PASS': True, 'comparison': 'exact', 'source_machine': source_machine,
                'target_machine': target_machine, 'reference': reference_pin}
    # Dung sai chưa được Minh khóa: không tự chọn để cho qua.
    if source_machine != target_machine and tolerance is None:
        raise Blocked('parity khác máy lệch, dung sai chưa khóa')
    raise Blocked('status/intermediate/ranking/region parity lệch; cần phân xử từng field')


def plan_candidate():
    return {'status': 'CANDIDATE_WAIT_PILOT_GRANT', 'measured_runtime': None,
            'local': ['TT nhẹ/nặng + C-e', 'OB E2/C-d2 giúp và đối chiếu', 'T12 vùng đổi/không đổi',
                      'TORAI 3 seed + prep cache byte parity', 'đo throughput 1 rồi 2/3 worker'],
            'ec2_1': ['TT có native cùng máy và nhánh driver còn thiếu, sau identity/env/sync grant'],
            'ec2_2': 'Chỉ phát khi có nhánh driver cần thiết và giảm đường găng; chưa tự dựng thêm lô.',
            'reference_sources': ['T-024', 'T-026', 'T-050', 'T-053', 'T-051'],
            'source_machine_per_window': 'required_before_run', 'budget': None,
            'cross_machine_tolerance': None, 'ssh_performed': False, 'dev_pilot_run': False,
            'note': 'Không dùng thiếu quyền pilot để dừng việc cài/fixture độc lập.'}

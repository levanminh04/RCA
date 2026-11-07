"""Kiểm ánh xạ riêng trước khi cấp và sử dụng biên nhận runtime P7."""
from dataclasses import dataclass
import json
import re

from common import ROOT, dump, save
import p7_entry_v2 as v2
from p7_entry import InputError, no_labels


def read_pin(ref):
    if not isinstance(ref, dict) or not isinstance(ref.get('path'), str) or not sha(ref.get('sha256')):
        raise InputError('thiếu đường dẫn hoặc SHA-256 đã ghim')
    return v2.checked_document(ROOT / ref['path'], ref['sha256'])


def sha(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _case_binding(dataset, row):
    """Chỉ các trường bộ đọc sử dụng, kiểu và đơn vị theo nguồn."""
    required = {'member_sha256', 'files'}
    if dataset == 'RE2-TT':
        required |= {'t', 'ce_history'}
        if type(row.get('t')) is not int or row.get('ce_history') not in ('verified', 'insufficient'):
            raise InputError('mốc TT hoặc hỗ trợ C-e chưa xác minh')
    elif dataset == 'Nezha-OB':
        required |= {'t_ns', 'trace_guard_s'}
        if type(row.get('t_ns')) is not int or type(row.get('trace_guard_s')) is not int:
            raise InputError('mốc OB hoặc trace guard chưa xác minh')
    else:
        raise InputError('dataset ngoài P7(a)')
    if set(row) != required or not sha(row.get('member_sha256')):
        raise InputError('trường ca khác hợp đồng runtime')
    files = row['files']
    if not isinstance(files, dict) or not files:
        raise InputError('tập file rỗng hoặc không hợp lệ')
    for meta in files.values():
        if (not isinstance(meta, dict) or set(meta) != {'path', 'sha256', 'bytes'}
                or not isinstance(meta['path'], str) or not meta['path'] or not sha(meta['sha256'])
                or type(meta['bytes']) is not int or meta['bytes'] <= 0):
            raise InputError('file chưa có locator, byte và SHA-256 hợp lệ')
    return v2.fingerprint(row)


def _snapshot(protocol_ref, runtime_ref, granted):
    if not granted:
        raise PermissionError('Chưa có quyền mở P7')
    return v2.open_runtime(ROOT / protocol_ref['path'], protocol_ref['sha256'],
                           ROOT / runtime_ref['path'], runtime_ref['sha256'], granted=True)


def attest_runtime(protocol_ref, runtime_ref, private_ref, output, *, granted=False):
    """Lớp quản lý dữ liệu nhận bản đồ từ nguồn duyệt riêng, trước khi phát biên nhận.

    Private map dùng khóa hash thành viên đầy đủ. Ref do bên quản lý cung cấp
    từ nguồn độc lập với bản kê runtime. Không lấy ref từ chính bản kê.
    """
    snap = _snapshot(protocol_ref, runtime_ref, granted)
    if private_ref['sha256'] in (runtime_ref['sha256'], protocol_ref['sha256']):
        raise InputError('bản đồ riêng phải được ghim độc lập')
    private = read_pin(private_ref)
    no_labels(private)
    dataset = snap.manifest['dataset']
    if private.get('schema') != 'P7-CASE-SOURCE-001' or private.get('dataset') != dataset:
        raise InputError('sai hợp đồng nguồn bản đồ riêng')
    runtime_cases = snap.manifest['cases']
    source_cases = private['cases_by_member']
    if set(source_cases) != {row['member_sha256'] for row in runtime_cases.values()}:
        raise InputError('bản đồ riêng thiếu hoặc thừa thành viên G1')
    case_hashes = {}
    for oid, row in runtime_cases.items():
        case_hash = _case_binding(dataset, row)
        if _case_binding(dataset, source_cases[row['member_sha256']]) != case_hash:
            raise InputError('file, mốc hoặc hỗ trợ C-e không khớp nguồn riêng')
        case_hashes[oid] = case_hash
    receipt = {'schema': 'P7-RUNTIME-BINDING-001', 'dataset': dataset,
               'protocol_sha256': protocol_ref['sha256'], 'runtime_sha256': runtime_ref['sha256'],
               'private_source_sha256': private_ref['sha256'], 'cases': case_hashes}
    save(output, receipt)
    return receipt


@dataclass(frozen=True)
class VerifiedRuntime:
    """Bản chụp bất biến. Mỗi tuyến thực thi lấy một bản giải mã riêng."""
    protocol_json: str
    manifest_json: str
    receipt_json: str
    receipt_sha256: str

    def snapshot(self):
        return v2.Runtime(json.loads(self.protocol_json), json.loads(self.manifest_json))

    def receipt(self):
        return json.loads(self.receipt_json)


def open_runtime(protocol_ref, runtime_ref, receipt_ref, *, granted=False):
    snap = _snapshot(protocol_ref, runtime_ref, granted)
    receipt = read_pin(receipt_ref)
    dataset = snap.manifest['dataset']
    cases = {oid: _case_binding(dataset, row) for oid, row in snap.manifest['cases'].items()}
    if (receipt.get('schema') != 'P7-RUNTIME-BINDING-001' or receipt.get('dataset') != dataset
            or receipt.get('protocol_sha256') != protocol_ref['sha256']
            or receipt.get('runtime_sha256') != runtime_ref['sha256']
            or not sha(receipt.get('private_source_sha256')) or receipt.get('cases') != cases):
        raise InputError('biên nhận không khớp bản kê đã xác minh')
    return VerifiedRuntime(dump(snap.protocol), dump(snap.manifest), dump(receipt), receipt_ref['sha256'])

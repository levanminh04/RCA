"""Cổng trước seal và điểm vào chấm A4. Công thức vẫn dùng a4_v2."""
from pathlib import Path

from common import ROOT, digest, save
import a4_v2
import p7_entry_v2 as v2
from p3 import danh_gia
from p7_entry import InputError, no_labels
from p7_guard_v3 import VerifiedRuntime, read_pin

DATASETS = ('RE2-TT', 'Nezha-OB')
BASELINES = {'RE2-TT': ('torai_B', 'torai', 'B'), 'Nezha-OB': ('simplerca', 'simplerca', 'M4')}
NORMAL_STATUSES = {'OK', 'NO_EVIDENCE', 'UNSUPPORTED'}


def _slot(runtime, oid, arm, seed):
    if not isinstance(runtime, VerifiedRuntime):
        raise InputError('cần runtime đã có biên nhận đối chiếu nguồn riêng')
    snap, binding = runtime.snapshot(), runtime.receipt()
    dataset = snap.manifest['dataset']
    if oid not in binding['cases']:
        raise InputError('ca ngoài cohort đã đối chiếu')
    contract = snap.protocol['a4_record_contract']
    seeds = contract['torai_B_seeds']
    if len(seeds) != 3 or any(type(s) is not int for s in seeds) or len(set(seeds)) != 3:
        raise InputError('phải khóa đúng ba seed nguyên TORAI B')
    worker, baseline_method, baseline_variant = BASELINES[dataset]
    if arm == 'M1' and seed is None:
        config = snap.protocol['configurations']['M1']
        if v2.fingerprint(config['config']) != config['sha256']:
            raise InputError('cấu hình M1 lệch dấu vân tay')
        method, variant, config_sha = 'M1', config['config']['config_id'], config['sha256']
    elif arm == worker and (seed in seeds and type(seed) is int if dataset == 'RE2-TT' else seed is None):
        method, variant = baseline_method, baseline_variant
        config_sha = v2.fingerprint(contract['baselines'][dataset])
    else:
        raise InputError('vế hoặc seed ngoài ma trận A4')
    return {'dataset': dataset, 'opaque_id': oid, 'arm': arm, 'method': method, 'variant': variant,
            'seed': seed, 'config_sha256': config_sha, 'case_sha256': binding['cases'][oid],
            'runtime_receipt_sha256': runtime.receipt_sha256}


def _check_record(record, slot):
    if any(k not in record or record[k] != slot[k] for k in ('method', 'variant')) or record.get('mode') != 'a':
        raise InputError('bản ghi sai phương pháp, biến thể hoặc chế độ')
    if record.get('seed') != slot['seed'] or type(record.get('seed')) is not type(slot['seed']):
        raise InputError('bản ghi sai seed')
    if slot['arm'] != 'M1' and record.get('opaque_id') != slot['opaque_id']:
        raise InputError('bản ghi baseline sai mã ca')
    if slot['arm'] == 'M1' and record.get('config_id') != slot['variant']:
        raise InputError('bản ghi M1 sai cấu hình')
    if record.get('status') not in NORMAL_STATUSES | {'ERROR', 'TIMEOUT'}:
        raise InputError('trạng thái ngoài hợp đồng A4')
    if record['status'] == 'OK':
        views = [record]
        if slot['arm'] == 'M1':
            worlds = record.get('worlds', {})
            if not all(isinstance(worlds.get(w), dict) and 'blocks' in worlds[w] for w in a4_v2.WORLDS):
                raise InputError('bản ghi M1 thiếu world')
            views = [worlds[w] for w in a4_v2.WORLDS]
        for view in views:
            if not danh_gia.khoi_tu_ban_ghi(view):
                raise InputError('bản ghi OK thiếu thứ hạng')


def _phase(slot, record):
    if record['status'] == 'TIMEOUT':
        cost = record.get('cost') or {}
        steps = cost.get('tien_trinh') or [cost]
        last = steps[-1]
        if last.get('timed_out') and last.get('exit_code') is None and last.get('wall_s') == 0:
            return 'before_worker_start'
        if slot['arm'] == 'torai_B' and slot['dataset'] == 'RE2-TT':
            return 'torai_preparation' if len(steps) == 1 else 'torai_worker_phase_unknown'
        return 'worker_phase_unknown'
    if record['status'] == 'ERROR':
        return 'm1_core_unclassified' if slot['arm'] == 'M1' else 'baseline_unclassified'
    return 'completed'


def run_slot(runtime, oid, arm, output_dir, *, seed=None, timeout_s=None):
    """Chạy đúng một vế đã khai. Ghi attempt riêng kể cả khi bị chặn."""
    slot = _slot(runtime, oid, arm, seed)
    snap = runtime.snapshot()
    out = ROOT / output_dir
    out.mkdir(parents=True, exist_ok=False)
    attempt = {'schema': 'P7-A4-ATTEMPT-001', 'slot': slot}
    try:
        if arm == 'M1':
            config = snap.protocol['configurations']['M1']['config']
            record = v2.m1(snap, oid, 'M1', config)
        else:
            declared = snap.protocol['a4_record_contract']['baselines'][slot['dataset']]
            if (declared.get('worker') != arm or declared.get('method') != slot['method']
                    or declared.get('variant') != slot['variant'] or type(timeout_s) is not int
                    or not 0 < timeout_s <= 3600 or timeout_s != declared.get('timeout_s')):
                raise InputError('lượt baseline lệch biến thể hoặc thời hạn đã khóa')
            records = v2.baseline(snap, oid, arm, out / 'runner', timeout_s, seed=seed)
            if len(records) != 1:
                raise InputError('vế A4 phải trả đúng một bản ghi')
            record, = records
        _check_record(record, slot)
        no_labels(record)
    except Exception as exc:
        phase = 'source_or_runner' if isinstance(exc, InputError) else 'unclassified_exception'
        save(out / 'attempt.json', dict(attempt, phase=phase, blocked=True, error_type=type(exc).__name__))
        raise
    attempt.update(phase=_phase(slot, record), record=record, record_sha256=v2.fingerprint(record))
    save(out / 'attempt.json', attempt)
    return attempt


def _expected(runtimes):
    if set(runtimes) != set(DATASETS):
        raise InputError('A4 cần đúng hai bộ đã khai')
    protocols = set()
    slots = {}
    for dataset in DATASETS:
        runtime = runtimes[dataset]
        if not isinstance(runtime, VerifiedRuntime) or runtime.receipt()['dataset'] != dataset:
            raise InputError('sai bộ của biên nhận runtime')
        protocols.add(runtime.receipt()['protocol_sha256'])
        contract = runtime.snapshot().protocol['a4_record_contract']
        if len(runtime.receipt()['cases']) != contract['counts'][dataset]:
            raise InputError('số ca khác giao thức A4 đã khóa')
        baseline = BASELINES[dataset][0]
        seeds = contract['torai_B_seeds'] if dataset == 'RE2-TT' else (None,)
        for oid in runtime.receipt()['cases']:
            for arm, seed in [('M1', None), *((baseline, s) for s in seeds)]:
                slot = _slot(runtime, oid, arm, seed)
                slots[_key(slot)] = slot
    if len(protocols) != 1:
        raise InputError('hai bộ dùng khác giao thức khóa')
    return slots


def _key(slot):
    return slot['dataset'], slot['opaque_id'], slot['arm'], slot['seed']


def _check_failure(attempt, review, contract):
    record = attempt['record']
    status = record['status']
    if status in NORMAL_STATUSES:
        return
    key = v2.fingerprint(attempt)
    item = review.get(key)
    if not item or item.get('input_and_config_validated') is not True or not item.get('reason'):
        raise InputError('lỗi chưa được xác nhận nguồn, dừng trước seal A4')
    proof = read_pin(item.get('evidence'))
    no_labels(proof)
    if (proof.get('attempt_sha256') != key or proof.get('phase') != item.get('phase')
            or proof.get('classification') != item.get('classification')):
        raise InputError('bằng chứng phân loại không khớp lượt')
    if status == 'ERROR' and item.get('classification') == 'method_error' and item.get('phase') == 'method':
        return
    if status == 'TIMEOUT' and item.get('classification') == 'declared_timeout':
        allowed = contract.get('timeout_policy', {}).get('score_phases', [])
        if item.get('phase') in allowed and attempt['phase'] not in ('torai_preparation', 'before_worker_start'):
            return
    raise InputError('lỗi dữ liệu, điều phối hoặc hết giờ ngoài quy tắc A4 đã khóa')


def _validate(attempts, runtimes, review):
    wanted = _expected(runtimes)
    selected = {}
    for attempt in attempts:
        slot = attempt.get('slot', {})
        key = _key(slot)
        if (attempt.get('schema') != 'P7-A4-ATTEMPT-001' or attempt.get('blocked')
                or key in selected or key not in wanted or v2.fingerprint(slot) != v2.fingerprint(wanted[key])):
            raise InputError('lượt thiếu, trùng hoặc sai vế, ca, cấu hình hay nguồn A4')
        record = attempt['record']
        _check_record(record, wanted[key])
        if attempt.get('record_sha256') != v2.fingerprint(record) or attempt.get('phase') != _phase(slot, record):
            raise InputError('bản ghi hoặc biên nhận bước chạy không khớp')
        no_labels(attempt)
        contract = runtimes[slot['dataset']].snapshot().protocol['a4_record_contract']
        _check_failure(attempt, review, contract)
        selected[key] = record
    if set(selected) != set(wanted):
        raise InputError('chưa đủ tất cả ca và seed của A4')
    return selected


def _review(ref):
    if ref is None:
        return {}
    doc = read_pin(ref)
    no_labels(doc)
    if doc.get('schema') != 'P7-FAILURE-REVIEW-001':
        raise InputError('sai hợp đồng biên nhận phân loại lỗi')
    return doc['assessments']


def seal_for_a4(output, attempt_refs, runtimes, *, failure_review_ref=None):
    """Chỉ seal từ biên nhận đã ghim, sau kiểm đủ vế và phân loại lỗi."""
    attempts = [read_pin(ref) for ref in attempt_refs]
    _validate(attempts, runtimes, _review(failure_review_ref))
    bundle = {'schema': 'P7-A4-SEAL-001', 'attempts': attempts,
              'failure_review_sha256': failure_review_ref['sha256'] if failure_review_ref else None}
    no_labels(bundle)
    save(output, bundle)
    return digest(output)


def evaluate_sealed(seal_ref, runtimes, label_reader, *, failure_review_ref=None):
    """Kiểm lại seal và mọi điều kiện trước lần đầu gọi bên đọc nhãn."""
    bundle = read_pin(seal_ref)
    review_sha = failure_review_ref['sha256'] if failure_review_ref else None
    if bundle.get('schema') != 'P7-A4-SEAL-001' or bundle.get('failure_review_sha256') != review_sha:
        raise InputError('seal không khớp biên nhận phân loại lỗi')
    records = _validate(bundle['attempts'], runtimes, _review(failure_review_ref))
    labels = label_reader()
    tables = []
    tt_seeds = runtimes['RE2-TT'].snapshot().protocol['a4_record_contract']['torai_B_seeds']
    for dataset in DATASETS:
        oids = runtimes[dataset].receipt()['cases']
        baseline = BASELINES[dataset][0]
        seeds = tt_seeds if dataset == 'RE2-TT' else (None,)
        left = {oid: records[dataset, oid, 'M1', None] for oid in oids}
        right = {oid: [records[dataset, oid, baseline, seed] for seed in seeds] for oid in oids}
        tables.append((left, right, labels[dataset]))
    return a4_v2.evaluate(*tables, torai_seeds=tt_seeds, expected_counts=tuple(len(t[0]) for t in tables))

"""Read verified closed metadata only; never import or execute an RCA method."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'runs' / 'microrank-cohort-failure-001'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

receipt = read(BASE / 'transport-check.json')
assert receipt['status'] == 'PASS' and len(receipt['files']) == 15
for row in receipt['files']:
    path = Path(row['local'])
    assert path.resolve().is_relative_to(BASE.resolve())
    data = path.read_bytes()
    assert len(data) == row['bytes']
    assert hashlib.sha256(data).hexdigest() == row['sha256']

table = read(BASE / 'cohort' / '52-cases.json')
report = read(BASE / 'failed-case' / 'roundoff-comparison.json')
check = read(BASE / 'failed-case' / 'check.json')
rows = table['rows']
assert len(rows) == 52
assert len({(r['dataset'], r['opaque_id']) for r in rows}) == 52
for dataset, expected in [('RE2-TT', 30), ('Nezha-OB', 22)]:
    selected = [r for r in rows if r['dataset'] == dataset]
    assert len(selected) == expected
    actual = collections.Counter(r['classification'] for r in selected)
    declared = table['by_dataset'][dataset]['classification_counts']
    assert dict(actual) == {k: v for k, v in declared.items() if v}
assert table['status'] == 'FAIL_STOP'
assert check['status'] == 'FAIL_STOP' and report['classification'] == 'blocked'
assert report['numeric_summary'] == check['numeric_summary']
bad = collections.Counter(r['kind'] for r in report['score_checks'] if not r['check']['pass'])
summary = {
    'control_metadata_validation': 'PASS',
    'method_cohort_status': 'FAIL_STOP',
    'verified_transport_files': 15,
    'table': {'path': 'cohort/52-cases.json', 'pointer': '/rows',
              'overall': table['overall'], 'by_dataset': table['by_dataset']},
    'failed_case': {
        'dataset': check['dataset'], 'opaque_id': check['opaque_id'],
        'source_capture_hash_checks': all(r['pass'] is True for r in check['source_checks']),
        'native_observed_exact': report['native_observed_exact'],
        'service_order_exact': report['service_order_exact'],
        'service_tie_partition_exact': report['service_tie_partition_exact'],
        'hit_metrics_exact': report['hit_metrics']['pass'],
        'outside_whitelist_differences': report['outside_whitelist_differences'],
        't028_flags': report['t028_flags'],
        'threshold': report['threshold'],
        'numeric_summary': report['numeric_summary'],
        'beyond_threshold_by_kind': dict(bad),
        'guard': check['guard'],
        'source': 'failed-case/roundoff-comparison.json',
    },
    'all_case_contracts_passed': False,
    'A_prime_ready': False,
    'no_retry_no_skip_no_tolerance_increase': True,
    'limits': 'Partial cohort; not_run means no result. T028 flags not checked for failed case. No numerical drift or physical cause identified.',
}
(BASE / 'comparison-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
lines = [
    '# MicroRank — bảng 52 ca tại checkpoint FAIL_STOP', '',
    'Nguồn đã kiểm hash hai đầu: `transport-check.json`; bảng máy đọc `cohort/52-cases.json#/rows`.',
    'Không tăng ngưỡng, không bỏ ca lỗi. `not_run` chưa có kết quả; dấu “—” là không có phép so số, không phải lệch bằng 0. Ca ERROR khớp trạng thái nhưng không có cặp điểm để tính ULP/tương đối.', '',
    '| Dataset | Mẫu số | Exact | Chỉ lệch số | Đổi operation | Đổi service | Blocked | Chưa chạy |',
    '|---|---:|---:|---:|---:|---:|---:|---:|',
]
for dataset, entry in table['by_dataset'].items():
    c = entry['classification_counts']
    lines.append(f"| {dataset} | {entry['denominator']} | {c['exact']} | {c['numeric_only']} | {c['operation_order']} | {c['service_order_changed']} | {c['blocked']} | {c['not_run']} |")
lines += ['', '| Dataset | Ca | Trạng thái nguồn | Loại kiểm | ULP lớn nhất | Tương đối lớn nhất |', '|---|---|---|---|---:|---:|']
for r in rows:
    ulp = '—' if r['max_ulp_distance'] is None else str(r['max_ulp_distance'])
    rel = '—' if r['max_relative'] is None else format(r['max_relative'], '.17g')
    lines.append(f"| {r['dataset']} | {r['opaque_id']} | {r['source_status']} | {r['classification']} | {ulp} | {rel} |")
lines += ['', 'Ngưỡng đã duyệt: đồng thời ≤16 ULP và ≤16×2^-52 tương đối; không absolute floor.',
          'Ca dev-3defe3d34b vượt ngưỡng số. Native–observed, thứ tự/hòa service và Hit@1..10 đã khớp; T-028 bridge chưa chạy cho ca lỗi. Không dùng trung gian ca lỗi làm bằng chứng và không chạy A′.',
          'Phần này là tiến độ kiểm phát lại; chưa xác định nguyên nhân drift, partition lịch sử hoặc cơ chế RCA.']
(BASE / '52-cases.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS_METADATA', 'cases': 52, 'overall': table['overall'], 'failed_beyond_threshold_by_kind': dict(bad)}, ensure_ascii=False))

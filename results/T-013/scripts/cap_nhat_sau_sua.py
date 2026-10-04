"""Integrate the approved correction evidence without rerunning methods.

One-shot scoped update. All historical runs and the reviewer body are retained.
"""
import csv
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-013'
TASK = ROOT / 'tasks/T-013-ho-so-baro'
FIX = OUT / 'runs/sua-N1-20261004-195501'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


focused = load(FIX / 'ket-qua.json')
window = load(OUT / 'trung-gian/cua-so-delay-summary.json')
R1 = Path(window['run_dir'])
assert focused['status'] == 'pass' and window['status'] == 'complete'
assert len(focused['checks']) == 19 and focused['real_metric_points_checked'] == 1316
assert window['all_endpoint_metric_ranks_exact'] and window['all_endpoint_service_ranks_exact']
assert window['all_repeat_permutation_checks_pass']
assert abs(window['baseline_effect_shapley_average'] + window['post_effect_shapley_average'] + .256) < 1e-10
assert not (FIX / 'tich-hop.json').exists(), 'One-shot integration already done'

# Source/output hashes are checked before incorporating the R1 evidence.
for group in ['sources', 'output_files']:
    for record in load(R1 / 'manifest.json')[group]:
        path = Path(record['path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], str(path)

summary = load(FIX / 'truoc-kiem-tra.json')
original_checks = list(summary['checks'])
summary['checks'] += focused['checks'] + [
    {'check': 'R1-50-endpoint-ranks', 'status': 'pass', 'metric_exact': True, 'service_exact': True, 'source': str(R1 / 'checks.json')},
    {'check': 'R1-100-repeat-and-permutation', 'status': 'pass', 'scope': 'scores invariant; ties follow column order', 'source': str(R1 / 'checks.json')},
    {'check': 'R1-four-Avg5-and-contribution-sum', 'status': 'pass', 'Avg5': window['Avg5_four_variants'], 'delta': -.256, 'baseline_effect': -.240, 'post_effect': -.016},
    {'check': 'R1-candidate-changes', 'status': 'pass', 'cases': window['candidate_change_cases'], 'source': str(OUT / 'trung-gian/cua-so-delay-metric.csv')},
]
summary['approved_corrections'] = {
    'authorization': '04/10/2026 — Minh: sửa lại các lỗi trên, test cẩn thận',
    'findings': ['R1', 'N1', 'N2', 'N3'],
    'runs': [str(R1), str(FIX)],
    'historical_checks_preserved': len(original_checks),
    'new_checks': 23,
    'scope': 'R1 reuses 25 old DELAY cases for algebra; N1 rechecks two original examples; no full dataset benchmark',
    'pending': 'WHY arithmetic attribution convention and Minh task closure',
}
assert summary['checks'][:len(original_checks)] == original_checks
dump(OUT / 'kiem-tra.json', summary)

ledger = read_csv(FIX / 'truoc-ca-da-chay.csv')
original_ledger_count = len(ledger)
ledger += read_csv(FIX / 'ca-da-chay.csv')
variants = read_csv(OUT / 'trung-gian/cua-so-delay-variants.csv')
assert len(variants) == 100 and len({r['case'] for r in variants}) == 25
for r in variants:
    case, trial = r['case'].rsplit('_', 1)
    ledger.append({
        'ca': 'fse-ob/' + case + '/' + trial,
        'file_nguon': r['source'],
        'phuong_phap': 'N-Sigma independent window algebra',
        'muc_dich': 'R1 ' + r['variant'] + '; independent + repeat + column permutation; run ' + R1.name,
        'ly_do': 'c' if r['variant'] in {'N300-A300', 'N360-A361'} else 'b',
    })
with (OUT / 'ca-da-chay.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['ca', 'file_nguon', 'phuong_phap', 'muc_dich', 'ly_do'])
    writer.writeheader()
    writer.writerows(ledger)

marker = '## Phản hồi của người làm (người làm điền sau)'
review_path = TASK / 'REVIEW.md'
before_review = review_path.read_bytes()
body = before_review.split(marker.encode('utf-8'))[0]
assert hashlib.sha256(body).hexdigest() == '27ff525c10c00da3a4a7492b31084fc4712045d31257c1bafa88b053dedf0283'
decision = 'Minh duyệt sửa 04/10/2026: “sửa lại các lỗi trên, test cẩn thận”. Chưa duyệt đóng task.'
table = f'''{marker}

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng — lỗi CHẶN đã sửa theo Minh | Trước sửa hồ sơ không giải thích đúng ô DELAY. Đã bổ sung đủ 25 ca × 4 phối hợp nền/hậu; 50 endpoint khớp từng metric và service rank T-006, 100 phối hợp kiểm lặp/đảo cột giữ điểm. Avg@5 là 0,936/0,712/0,936/0,680; trung bình hai thứ tự phân bổ nền −0,240, hậu −0,016, bao gồm bốn ca đổi candidate. §1 có trung gian từng metric, ba ca cụ thể và giới hạn nhân quả; tiêu chí 4 đã cập nhật. Không chốt L. Nguồn: results/T-013/trung-gian/cua-so-delay-summary.json và run sua-R1-20261004-195903. | {decision} |
| N1 | Đúng (tự tìm S1) — đã sửa helper | Thiếu variance bù sai số/near-constant bound đã sửa trong scripts/kiem_co_che.py. Phản ví dụ điểm cũ 5,057563 nay 18, khớp StandardScaler ghim, scale hiệu dụng 1. Tám synthetic và tám cấu hình hai ca gốc khớp 1.316 điểm chính thức (normalized error 0); so điểm lịch sử sai số ≤2,35e-16, mọi rank giữ nguyên. Kiểm lặp/đảo cột đạt; output cũ giữ nguyên. Nguồn: runs/sua-N1-20261004-195501/ket-qua.json. | {decision} |
| N2 | Đúng (tự tìm S2) — đã sửa mô tả | Hồ sơ N-Sigma phát hiện đã ghi n là số mẫu không NaN, công thức cần giá trị hữu hạn, inf không tự loại. Phản ví dụ pandas count 3/finite 2, mean Infinity/std NaN được giữ trong checks; không ảnh hưởng ví dụ hữu hạn cũ. | {decision} |
| N3 | Đúng (tự tìm S3) — đã sửa điều kiện | Hồ sơ BOCPD đã thêm tổng mass dương và hữu hạn để suy q_t(0)=0,02. Kiểm core mass 0/posterior NaN và mass dương/posterior (0,02;0,98) xác nhận điều kiện; không suy wrapper min–max lỗi trên cùng input. Không sửa code tác giả. | {decision} |
'''
review_path.write_bytes(body + table.encode('utf-8'))
assert review_path.read_bytes().split(marker.encode('utf-8'))[0] == body

# Preserve the focused test code as used, and record source/output provenance.
shutil.copyfile(OUT / 'scripts/kiem_sua_phan_bien.py', FIX / 'script.py')
sources = [OUT / 'scripts/kiem_co_che.py', OUT / 'scripts/kiem_sua_phan_bien.py',
           Path(summary['selection']['selected'][0]['source']),
           Path(summary['selection']['selected'][1]['source']),
           Path('D:/RCA-ext/work/T-013/metrics-selected.npz'),
           Path('D:/RCA-ext/work/T-013/metrics-selected.json')]
manifest = load(FIX / 'manifest.json')
manifest['tested_sources'] = [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]
manifest['test_outputs'] = [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                            for p in sorted(FIX.iterdir()) if p.is_file() and (p.name in {'ket-qua.json', 'checks.json', 'ca-da-chay.csv', 'tien-do.jsonl', 'script.py'} or p.name.startswith(('TT-', 'OB-')))]
manifest['focused_test_status'] = 'pass'
dump(FIX / 'manifest.json', manifest)

report = {'status': 'integrated', 'historical_checks': len(original_checks), 'new_checks': 23,
          'total_checks': len(summary['checks']), 'historical_ledger_rows': original_ledger_count,
          'ledger_rows': len(ledger), 'R1_final_run': str(R1), 'focused_run': str(FIX),
          'reviewer_body_preserved': True, 'closure_approved': False}
dump(FIX / 'tich-hop.json', report)
with (TASK / 'LOG.md').open('a', encoding='utf-8', newline='') as f:
    f.write('''
### Kết quả sửa và kiểm tập trung

- **R1:** đã phân rã đúng 25 ca DELAY, bốn phối hợp 300/360 nền × 300/361 hậu. 50 endpoint khớp từng metric/service rank T-006; 100 phối hợp lặp và đảo cột giữ điểm. Bốn Avg@5: 0,936; 0,712; 0,936; 0,680. Tác động trung bình hai thứ tự: nền −0,240, hậu −0,016, có tương tác và bốn ca thêm candidate. §1 có đủ bảng 25 ca, trung gian metric, ba ca diễn giải và các nguyên nhân vật lý chưa phân xử; §2–4 giữ nguyên. Không chọn L hoặc kết luận đồ thị.
- Run R1 cuối: `results/T-013/runs/sua-R1-20261004-195903/`. Bốn run R1 được giữ (195551,195631,195734,195903); tất cả số học đạt. Run đầu hash progress ghi trước complete: đã giữ manifest trước sửa hash và đính chính metadata, không đổi số. Các run sau lần lượt cải thiện thứ tự ghi hash, chẩn đoán candidate bị bỏ và snapshot script/bốn Avg@5. Thời gian run cuối 12,133 giây trên máy dùng chung, không benchmark.
- **N1:** sửa helper bằng variance hai lượt có bù sai số và bound gần hằng của sklearn ghim; không gọi helper variance tác giả trong nhánh độc lập. Tám synthetic có phản ví dụ gốc 5,057563→18/scale1, hằng, trên bound, scale nhỏ, offset lớn, missing. Tám cấu hình hai ca gốc × L10/L20 × BR/RE kiểm đủ 1.316 điểm: sai số normalized official 0, lịch sử lớn nhất 2,346069e-16; mọi metric rank cũ giữ nguyên, repeat/permutation score đạt.
- **N2:** sửa n thành số mẫu không NaN, điều kiện hữu hạn và inf không bị pandas loại. **N3:** thêm tổng mass dương hữu hạn; core synthetic mass0/posteriorNaN so massdương/q0=0,02. Cả hai kiểm xác nhận giới hạn, không coi đầu ra NaN hợp lệ hoặc suy wrapper lỗi.
- 19 phép kiểm tập trung đạt tại `results/T-013/runs/sua-N1-20261004-195501/ket-qua.json`; runtime 24,017 giây trên máy dùng chung. Agent khác đã so độc lập code sklearn ghim, đọc 19 checks và 1.316 điểm CSV: không finding mới, không sửa file/không chạy thêm fullmethod. Code tác giả giữ nguyên. Không chạy BOCPD full TT hoặc benchmark toàn tập.
- Main kiem-tra giữ nguyên 131 checks lịch sử và run_dir, thêm 23 checks/aggregate của bản sửa (tổng 154). Ledger giữ 66 dòng cũ, thêm 18 dòng N1–N3 và 100 cấu hình số học R1 (tổng 184); mỗi dòng R1 ghi independent + repeat + permutation, không gọi phương pháp tác giả. Chỉ 25 ca DELAY đã chạy T-006, không chọn bằng kết quả đẹp.
- Bảng cuối REVIEW đã ghi tình trạng sửa và lời Minh duyệt; thân reviewer giữ nguyên byte. Nháp WHY giải thích lựa chọn hạch toán hai thứ tự đã thêm vào de-xuat-tai-lieu-chung, ghi chờ WHY tại chỗ; không ghi nguồn chung, không tự đóng task.
''')
print(json.dumps(report, ensure_ascii=False))

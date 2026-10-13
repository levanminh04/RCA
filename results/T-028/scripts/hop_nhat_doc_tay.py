"""Package completed human readings; do not calculate or assign mechanisms."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / 'results/T-028/runs/buoc3-005'


def load(name):
    return json.loads((RUN / name).read_text(encoding='utf-8'))


def write(path, value):
    if path.exists():
        raise RuntimeError('Preserve existing output: ' + str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main():
    re2, nez, selected, analysis = (load(n) for n in ('manual-re2.json', 'manual-nezha.json', 'manual-selection.json', 'ca-sai.json'))
    assert re2['status'] == 'all_fixed_criteria_matched'
    assert nez['mismatches_n'] == 0 and not nez['criterion_changed']
    cases = list(re2['cases'])
    for note in nez['notes']:
        assert all(v['manual_judgement'] == 'khớp tiêu chí đã duyệt' for v in note['requirement_verdicts'])
        cases.append({
            'dataset': note['dataset'], 'method': note['method'], 'opaque_id': note['opaque_id'],
            'requirements': note['requirements'], 'criterion_match': True,
            'reading_note': note['manual_criterion_observation'] + ' ' + note['manual_judgement'],
            'observed_values': note['actual_intermediates'],
            'sources': [dict(role=k, **v) for k, v in note['sources'].items()],
            'RAM_window_recheck': note['RAM_window_recheck'],
            'alternative_explanations': note['alternative_explanations'],
            'conclusion_level': 'Khớp tiêu chí quan sát; chưa phân xử nhân quả.'})
    identity = lambda r: (r['dataset'], r['method'], r['opaque_id'])
    cases.sort(key=identity)
    assert sorted(map(identity, cases)) == sorted(map(identity, selected))
    assert all(c['criterion_match'] and c['reading_note'] and c['sources'] for c in cases)
    payload = {
        'task': 'T-028', 'run_id': 'buoc3-005', 'status': 'completed',
        'packaged_at': datetime.now().astimezone().isoformat(),
        'selection_source': 'results/T-028/runs/buoc3-005/manual-selection.json',
        'reading_sources': ['results/T-028/runs/buoc3-005/manual-re2.json', 'results/T-028/runs/buoc3-005/manual-nezha.json'],
        'case_method_n': len(cases), 'requirements_n': sum(len(c['requirements']) for c in cases),
        'criterion_mismatches_n': 0, 'all_related_seeds_read': True,
        'criterion_changed': False, 'method_rerun': False,
        'note': 'Hợp nhất ghi nhận đã đọc, không tự tính verdict hoặc sửa gán. Root và quan hệ là nhãn phân tích. Các giải thích nhân quả vẫn chưa kiểm.',
        'cases': cases}
    write(RUN / 'manual-reading.json', payload)
    rows = {identity(r): (i, r) for i, r in enumerate(analysis['main_rows'])}
    lines = ['# Đọc tay các ca theo codebook', '',
             'Mẫu được chọn trước đọc theo codebook §8, gộp mục trùng và giữ mọi yêu cầu theo k/cơ chế. '
             'Ghi nhận gốc: `results/T-028/runs/buoc3-005/manual-re2.json` và `manual-nezha.json`. '
             'Bản hợp nhất: `results/T-028/runs/buoc3-005/manual-reading.json`.', '',
             f'Đã đọc {len(cases)} mục phương pháp × ca, tương ứng {payload["requirements_n"]} yêu cầu nhóm; '
             'không thấy gán tự động lệch tiêu chí đã duyệt. Nguồn số: `manual-reading.json` → '
             '`case_method_n`, `requirements_n`, `criterion_mismatches_n`. '
             'Khớp tiêu chí quan sát chưa xác nhận giải thích nhân quả. Không sửa codebook.', '',
             'Mỗi mục dưới là ví dụ cho các nhóm được ghi ở dòng Yêu cầu. Giá trị đầy đủ, availability/N/A '
             'và seed nằm trong `observed_values` của bản hợp nhất; đọc tay không điền trung gian bằng chạy lại phương pháp.', '']
    for j, c in enumerate(cases):
        i, r = rows[identity(c)]
        req = '; '.join(f'k={v["k"]}, {v["mechanism"]}' for v in c['requirements'])
        pointer = f'results/T-028/runs/buoc3-005/manual-reading.json → /cases/{j}'
        lines += [f'## {c["dataset"]} · {c["method"]} · {c["opaque_id"]}', '',
                  f'Root phân tích: `{r["root"]}`. Yêu cầu: {req}.', '', c['reading_note'], '',
                  f'Nguồn ghi nhận và toàn bộ số: `{pointer}`; evidence đã lưu: '
                  f'`results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/{i}`.', '']
        for sid, seed in r['evidence']['seed_evidence'].items():
            rank = seed['ranking']
            loc = rank.get('entity_locations', {}).get(r['root'])
            local = seed['local_nonpositive']
            values = {'status': seed['status'], 'root_location': loc,
                      'root_key': rank.get('entity_keys', {}).get(r['root']),
                      'root_location_availability': 'available' if loc is not None else 'N/A; root outside R or non-OK',
                      'local_nonpositive': local,
                      'P0': {k: seed['by_k'][k]['P0'] for k in ('1', '5')}}
            lines += [f'Seed `{sid}` (nguồn `/main_rows/{i}/evidence/seed_evidence/{sid}`): '
                      '`' + json.dumps(values, ensure_ascii=False, separators=(',', ':')) + '`', '']
        lines += ['Nguồn đối chiếu: ' + '; '.join('`' + s['path'] + ' → ' + s.get('json_pointer', '') + '`' for s in c['sources']), '']
    lines += ['## Giải thích khác còn lại', '',
              'Các nhóm chỉ là dấu hiệu theo tiêu chí đã khai. Cửa sổ/đồng hồ, nền chưa sạch, '
              'coverage và mapping, cấu trúc chấm điểm, loại tín hiệu, thông tin parent hoặc common cause, '
              'nhãn gốc và độ đại diện còn có thể giải thích sai hạng. Trạng thái cụ thể theo từng nhóm '
              'ở `ban-do-han-che-xep-hang.md` §6 và từng ghi nhận gốc. Phép can thiệp sẽ phân xử '
              'cần thay đầu vào/chạy phương pháp, nằm ngoài SPEC. Nơi xử lý câu “lan có đáng kể” giữ OPEN.', '']
    target = ROOT / 'results/T-028/doc-tay.md'
    if target.exists():
        raise RuntimeError('Preserve existing manual report')
    target.write_text('\n'.join(lines), encoding='utf-8')
    for name in ('ca-sai.json', 'ca-sai.csv'):
        top = ROOT / 'results/T-028' / name
        if top.exists():
            raise RuntimeError('Preserve existing top output')
        top.write_bytes((RUN / name).read_bytes())
    with (RUN / 'handoff-progress.jsonl').open('a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps({'stage': 'manual_packaged_and_step6_outputs_ready', 'at': payload['packaged_at']}, ensure_ascii=False) + '\n')
    print('Packaged', len(cases), payload['requirements_n'])


if __name__ == '__main__':
    main()

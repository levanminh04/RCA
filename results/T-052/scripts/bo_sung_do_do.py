"""Tổng hợp cột Q-62 còn thiếu từ điểm đã chấm; không chạy phương pháp."""
import time

from common import ROOT, RUN, digest, pin, read, save, timing
from m1_danh_gia import pha2


def main():
    start = time.perf_counter()
    path = 'results/T-052/ket-qua-dev.json'
    data = pha2.giai_ma_json(read(path))
    tables = {}
    for world, datasets in data['worlds'].items():
        tables[world] = {}
        for dataset, table in datasets.items():
            methods = {}
            for name, rows in table['per_case'].items():
                n = len(rows)
                summary = dict(table['summary'][name]['metrics'])
                # Cùng định nghĩa p3.danh_gia.tong_hop; Rerank là tỉ số gộp.
                for k in (5, 10):
                    den = sum(r[f'hit@{k}'] for r in rows.values())
                    summary[f'retrieval@{k}'] = den / n
                    summary[f'rerank@1(K={k})'] = (
                        sum(r['hit@1'] for r in rows.values()) / den if den else None)
                methods[name] = {'n': n, 'metrics': summary,
                                 'status': table['summary'][name]['status']}
            tables[world][dataset] = methods
    manifest = read('results/T-052/manifest.json')
    native, sources = {}, {}
    for dataset, path0 in [('RE2-TT', 'results/T-024/cham-a.json'),
                           ('Nezha-OB', 'results/T-026/cham-a.json')]:
        pin(path0, next(r for r in manifest['upstream_inputs_verified'] if r['path'] == path0))
        source = read(path0)
        methods = source['methods'] if dataset == 'RE2-TT' else source['tables']['main']['methods']
        native[dataset] = {}
        for name, item in methods.items():
            summary = item['summaries']['dev30'] if dataset == 'RE2-TT' else item['summary']
            native[dataset][name] = summary['rcaeval']
        sources[dataset] = {'path': path0, 'sha256': digest(ROOT / path0),
                           'pointer': '/methods/<method>/summaries/dev30/rcaeval' if dataset == 'RE2-TT'
                           else '/tables/main/methods/<method>/summary/rcaeval'}
    save(ROOT / 'results/T-052/do-do-bo-sung.json', {
        'status': 'DESCRIPTIVE_DEV_SUPPLEMENT',
        'source_scored': {'path': path, 'sha256': digest(ROOT / path)},
        'expected_ties': tables, 'baseline_native_order': native, 'native_sources': sources,
        'definitions': {
            'expected_ties': 'Cùng p3.danh_gia: Retrieval@K = mean Hit@K; Rerank@1(K) = sum Hit@1 / sum Hit@K, mẫu số 0 là null. Seed trung bình trong ca như bảng chính.',
            'native_order': 'Giữ bảng RCAEval nguyên gốc của baseline, tách thứ tự native khỏi kỳ vọng hòa. Không đưa số 0 giả từ ranking_native rỗng cho M1.',
            'M1_AC': 'Một root mỗi ca: kỳ vọng AC@k bằng Hit@k; Avg@5 là trung bình Hit@1..5. M1 giữ khối hòa, không chọn một thứ tự tùy ý để tạo bảng native.',
            'UNSUPPORTED': 'Giữ mẫu số/trạng thái giao thức; không diễn giải số 0 là so sánh hiệu quả thuật toán.'}})
    save(RUN / 'do-do-bo-sung-summary.json', timing('metric_supplement', start, PASS=True))


if __name__ == '__main__':
    main()

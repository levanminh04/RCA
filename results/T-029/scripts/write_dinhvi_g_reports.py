"""T-029 bước 8, bảng E/G từ JSON đã kiểm; không gọi detector hoặc ranker.

Tạo báo cáo mới, bảng tổng hợp nguồn và kiểm độc lập. Mọi số Markdown
được Report.num nối tới một scalar JSON để V8 kiểm lại.
"""
from collections import Counter
from pathlib import Path
import json
import math
import statistics
import time

from report_support import Report, esc
from resume_step7 import ROOT, OUT, now, read, sha, log, write

RUN = OUT / 'runs/report-dinhvi-g-001'
AGG = 'results/T-029/runs/report-dinhvi-g-001/source-aggregates.json'
LOC = 'results/T-029/dinh-vi.json'
G = 'results/T-029/a-so-b.json'
NS = 'results/T-029/n-sigma-cot.json'
VARIANTS = ('baseline', '5', '10', '20')
DETECTORS = ('nsigma', 'nsigma_doi_chung')
METRICS = ('hit@1', 'hit@5')
POINTS = ('a', 't_hat_plus', 't_hat')
CHANGES = ('a_to_tplus', 'tplus_to_first')
METHOD_NAMES = {'baro': 'BARO native', 'circa_ols_rht': 'CIRCA OLS RHT',
                'circa_ols_da': 'CIRCA OLS RHT+DA', 'torai_B': 'TORAI B'}
DET_NAMES = {'bocpd': 'BOCPD', 'nsigma': 'N-Sigma chính',
             'nsigma_doi_chung': 'N-Sigma đối chứng'}
VAR_NAMES = {'baseline': 'Giữ cột', '5': 'Bỏ N2 mức 5·p0',
             '10': 'Bỏ N2 mức 10·p0', '20': 'Bỏ N2 mức 20·p0'}


def md(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def ptr(*parts):
    return '/' + '/'.join(esc(x) for x in parts)


def source(path, pointer):
    return f'Nguồn: `{path}#{pointer}`. Mỗi ô số có con trỏ riêng trong bảng nguồn V8.\n\n'


def signs(values, case_ids):
    return {key + '_count': sum(f(value) for value in values)
            for key, f in (('positive', lambda x: x > 0),
                           ('negative', lambda x: x < 0), ('zero', lambda x: x == 0))} | {
        key + '_case_ids': [oid for oid, value in zip(case_ids, values) if f(value)]
        for key, f in (('positive', lambda x: x > 0),
                       ('negative', lambda x: x < 0), ('zero', lambda x: x == 0))}


def loc_summary(rows):
    return {'n': len(rows), 'mean_expected_rank': statistics.mean(r['expected_rank'] for r in rows),
            'mean_top1_probability': statistics.mean(r['root_top1_probability'] for r in rows),
            'uniform_expected_rank': statistics.mean(r['uniform_identity_expected_rank'] for r in rows),
            'uniform_top1_probability': statistics.mean(r['uniform_identity_top1_probability'] for r in rows),
            'root_no_alarm_count': sum(r['root_first_after_index'] is None for r in rows),
            'root_no_columns_count': sum(r['root_columns_remaining'] == 0 for r in rows),
            'service_counts': sorted({r['service_count'] for r in rows})}


def assemble(location, nsigma, comparisons):
    """Only aggregate frozen results. Independent checks are in verify_aggregates."""
    cases = location['cases']
    ids = sorted(cases)
    cells = sorted({r['cell'] for r in cases.values()})
    result = {'units': {'case_count': len(ids), 'cell_count': len(cells),
                        'detector_count_G': len(comparisons['by_detector']),
                        'method_count_G': len(comparisons['by_detector']['bocpd']),
                        'point_count_G': len(POINTS), 'seed_count': len(
                            comparisons['by_detector']['bocpd']['torai_B']['by_seed_on_30_cases'])},
              'location': {}, 'heuristic': {}, 'G_signs': {}, 'TORAI': {},
              'circa_paired_complete': {}}
    outside = []
    for oid in ids:
        for det in DETECTORS:
            for entity in nsigma['cases'][oid][det]['E_columns_outside_U']:
                outside.append({'opaque_id': oid, 'detector': det, 'entity': entity})
    result['outside_universe'] = {'entity_case_count': len(outside), 'rows': outside}
    for det in DETECTORS:
        variants = {}
        for variant in VARIANTS:
            all_rows = [cases[o]['nsigma'][det][variant] for o in ids]
            cell_rows = {c: [cases[o]['nsigma'][det][variant] for o in ids if cases[o]['cell'] == c]
                         for c in cells}
            changes = [cases[o]['nsigma'][det][variant]['expected_rank'] -
                       cases[o]['nsigma'][det]['baseline']['expected_rank'] for o in ids]
            probability_changes = [cases[o]['nsigma'][det][variant]['root_top1_probability'] -
                                   cases[o]['nsigma'][det]['baseline']['root_top1_probability'] for o in ids]
            variants[variant] = {'all': loc_summary(all_rows),
                                 'by_cell': {c: loc_summary(rs) for c, rs in cell_rows.items()},
                                 'rank_change_vs_baseline': signs(changes, ids),
                                 'top1_change_vs_baseline': signs(probability_changes, ids)}
        result['location'][det] = variants
    for oid in ids:
        result['heuristic'][oid] = {}
        for w, h in cases[oid]['bocpd']['heuristic'].items():
            regular = [r for r in h['columns'] if r['normalized_jump'] is not None]
            maximum = max((r['normalized_jump'] for r in regular), default=None)
            result['heuristic'][oid][w] = {
                'valid': h['valid'], 'regular_column_count': len(regular),
                'maximum_normalized_jump': maximum,
                'maximum_columns': [r['column'] for r in regular if r['normalized_jump'] == maximum],
                'constant_change_count': sum(r['constant_change'] for r in h['columns']),
                'constant_change_columns': [r['column'] for r in h['columns'] if r['constant_change']],
                'source_pointer': ptr('cases', oid, 'bocpd', 'heuristic', w)}
    for det, methods in comparisons['by_detector'].items():
        result['G_signs'][det] = {}
        result['circa_paired_complete'][det] = {}
        for method, table in methods.items():
            rows = table['per_case']
            result['G_signs'][det][method] = {}
            for change in CHANGES:
                result['G_signs'][det][method][change] = {
                    metric: signs([r['signed_deltas'][change][metric] for r in rows],
                                  [r['opaque_id'] for r in rows]) for metric in METRICS}
            if method.startswith('circa'):
                existing = table['circa_threshold']['paired_by_cell']
                result['circa_paired_complete'][det][method] = {
                    cell: existing.get(cell, {'n': 0, 'case_ids': [],
                                             'points': {p: {m: None for m in METRICS} for p in POINTS},
                                             'signed_deltas': {d: {m: None for m in METRICS} for d in CHANGES}})
                    for cell in cells}
            if method == 'torai_B':
                seeds = sorted(table['by_seed_on_30_cases'], key=int)
                disagree = [r['opaque_id'] for r in rows if any(
                    len({r['points'][p]['per_seed'][s][metric] for s in seeds}) != 1
                    for p in POINTS for metric in METRICS)]
                result['TORAI'][det] = {'seed_ids': [int(s) for s in seeds],
                                        'seed_disagree_case_count': len(disagree),
                                        'seed_disagree_case_ids': disagree, 'case_count': len(rows)}
    return result


def verify_aggregates(aggregate, location, nsigma, comparisons):
    """Recompute service order from label-free service timestamps, not location ranks.

    Also recompute every G mean/delta from stored per-seed scalar results and
    direct per-case rows; never run a ranker. Checks do not use assemble helpers.
    """
    checks = []
    failures = []

    def check(name, actual, expected, number=False):
        good = math.isclose(actual, expected, rel_tol=0, abs_tol=1e-12) if number else actual == expected
        checks.append({'name': name, 'pass': good})
        if not good:
            failures.append({'name': name, 'actual': actual, 'expected': expected})

    cases = location['cases']
    ids = sorted(cases)
    for oid in ids:
        for det in DETECTORS:
            f = nsigma['cases'][oid][det]
            for variant in VARIANTS:
                services = f['E_services'][variant]
                times = {s: math.inf if r['first_after_index'] is None else r['first_after_index']
                         for s, r in services.items()}
                root = cases[oid]['root']
                earlier = [s for s, t in times.items() if t < times[root]]
                same = [s for s, t in times.items() if t == times[root]]
                expected_rank = sum(range(len(earlier) + 1, len(earlier) + len(same) + 1)) / len(same)
                output = cases[oid]['nsigma'][det][variant]
                prefix = oid + '/' + det + '/' + variant
                check(prefix + '/expected_rank', output['expected_rank'], expected_rank, True)
                check(prefix + '/top1', output['root_top1_probability'],
                      1 / len(same) if not earlier else 0, True)
                check(prefix + '/root_time', output['root_first_after_index'], services[root]['first_after_index'])
                check(prefix + '/root_columns', output['root_columns_remaining'], services[root]['so_cot'])
                check(prefix + '/service_n', output['service_count'], len(services))
                check(prefix + '/uniform_rank', output['uniform_identity_expected_rank'], (len(services) + 1) / 2, True)
                check(prefix + '/uniform_top1', output['uniform_identity_top1_probability'], 1 / len(services), True)
            for w, h in cases[oid]['bocpd']['heuristic'].items():
                for j, c in enumerate(h['columns']):
                    ratio = abs(c['median_after'] - c['median_before']) / (1.4826 * c['mad']) if c['mad'] else None
                    check(oid + '/heuristic/w' + w + '/' + str(j) + '/ratio', c['normalized_jump'], ratio,
                          ratio is not None)
                    check(oid + '/heuristic/w' + w + '/' + str(j) + '/constant', c['constant_change'],
                          c['mad'] == 0 and c['median_after'] != c['median_before'])
        # Heuristic has no detector attribution and no newly invented service rank.
    for det in DETECTORS:
        for variant in VARIANTS:
            summary = aggregate['location'][det][variant]
            for kind, output_key, value_key in [('rank', 'rank_change_vs_baseline', 'expected_rank'),
                                               ('top1', 'top1_change_vs_baseline', 'root_top1_probability')]:
                output = summary[output_key]
                differences = {oid: cases[oid]['nsigma'][det][variant][value_key] -
                                cases[oid]['nsigma'][det]['baseline'][value_key] for oid in ids}
                for sign, compare in [('positive', lambda x: x > 0), ('negative', lambda x: x < 0),
                                      ('zero', lambda x: x == 0)]:
                    selected = [oid for oid in ids if compare(differences[oid])]
                    check('location-sign/' + det + '/' + variant + '/' + kind + '/' + sign + '/count',
                          output[sign + '_count'], len(selected))
                    check('location-sign/' + det + '/' + variant + '/' + kind + '/' + sign + '/ids',
                          output[sign + '_case_ids'], selected)
            for group, output in [('all', summary['all'])] + list(summary['by_cell'].items()):
                chosen = [r for r in cases.values() if group == 'all' or r['cell'] == group]
                values = [r['nsigma'][det][variant] for r in chosen]
                prefix = 'aggregate/' + det + '/' + variant + '/' + group
                check(prefix + '/n', output['n'], len(values))
                check(prefix + '/mean_rank', output['mean_expected_rank'],
                      sum(r['expected_rank'] for r in values) / len(values), True)
                check(prefix + '/mean_top1', output['mean_top1_probability'],
                      sum(r['root_top1_probability'] for r in values) / len(values), True)
                check(prefix + '/no_alarm', output['root_no_alarm_count'],
                      len([r for r in values if r['root_first_after_index'] is None]))
                check(prefix + '/no_columns', output['root_no_columns_count'],
                      len([r for r in values if not r['root_columns_remaining']]))
                check(prefix + '/uniform_rank', output['uniform_expected_rank'],
                      sum(r['uniform_identity_expected_rank'] for r in values) / len(values), True)
                check(prefix + '/uniform_top1', output['uniform_top1_probability'],
                      sum(r['uniform_identity_top1_probability'] for r in values) / len(values), True)
                check(prefix + '/servicecounts', output['service_counts'], sorted({r['service_count'] for r in values}))
    for oid in ids:
        for w, original in cases[oid]['bocpd']['heuristic'].items():
            output = aggregate['heuristic'][oid][w]
            regular = [c for c in original['columns'] if c['mad'] > 0]
            maximum = max((c['normalized_jump'] for c in regular), default=None)
            prefix = 'heuristic-aggregate/' + oid + '/' + w
            check(prefix + '/max', output['maximum_normalized_jump'], maximum, maximum is not None)
            check(prefix + '/maxcols', output['maximum_columns'],
                  [c['column'] for c in regular if c['normalized_jump'] == maximum])
            check(prefix + '/nregular', output['regular_column_count'], len(regular))
            changed = [c['column'] for c in original['columns'] if c['mad'] == 0 and c['jump'] != 0]
            check(prefix + '/nconstant', output['constant_change_count'], len(changed))
            check(prefix + '/constantcols', output['constant_change_columns'], changed)
    for det, methods in comparisons['by_detector'].items():
        for method, table in methods.items():
            rows = table['per_case']
            for row in rows:
                prefix = 'G/' + det + '/' + method + '/' + row['opaque_id']
                for point in POINTS:
                    scores = row['points'][point]
                    for metric in METRICS:
                        mean = statistics.mean(s[metric] for s in scores['per_seed'].values())
                        check(prefix + '/' + point + '/' + metric + '/seedmean', scores[metric], mean, True)
                for metric in METRICS:
                    check(prefix + '/window/' + metric, row['signed_deltas']['a_to_tplus'][metric],
                          row['points']['t_hat_plus'][metric] - row['points']['a'][metric], True)
                    check(prefix + '/event/' + metric, row['signed_deltas']['tplus_to_first'][metric],
                          row['points']['t_hat'][metric] - row['points']['t_hat_plus'][metric], True)
            groups = [('all30', table['all30'], rows)]
            groups += [('cell/' + c, output, [r for r in rows if r['cell'] == c]) for c, output in table['by_cell'].items()]
            groups += [('event/' + c, output, [r for r in rows if r['group'] == c]) for c, output in table['by_event_group'].items()]
            if method.startswith('circa'):
                limit = table['circa_threshold']
                high = {}
                for point in POINTS:
                    high[point] = [r['opaque_id'] for r in rows if any(
                        s['circa_nodes_gt_1e10'] for s in r['points'][point]['per_seed'].values())]
                    check('G/' + det + '/' + method + '/' + point + '/highids', limit['high_case_ids_by_point'][point], high[point])
                chosen = [r for r in rows if all(r['opaque_id'] not in high[p] for p in POINTS)]
                groups.append(('pairedclean', limit['paired_no_node_exceeds_at_any_point'], chosen))
                groups += [('pairedcell/' + c, output, [r for r in chosen if r['cell'] == c]) for c, output
                           in aggregate['circa_paired_complete'][det][method].items()]
            for group, output, chosen in groups:
                prefix = 'G/' + det + '/' + method + '/' + group
                check(prefix + '/n', output['n'], len(chosen))
                for point in POINTS:
                    for metric in METRICS:
                        expected = statistics.mean(r['points'][point][metric] for r in chosen) if chosen else None
                        check(prefix + '/' + point + '/' + metric, output['points'][point][metric], expected, bool(chosen))
                for change in CHANGES:
                    for metric in METRICS:
                        expected = statistics.mean(r['signed_deltas'][change][metric] for r in chosen) if chosen else None
                        check(prefix + '/' + change + '/' + metric, output['signed_deltas'][change][metric], expected, bool(chosen))
            for change in CHANGES:
                for metric in METRICS:
                    s = aggregate['G_signs'][det][method][change][metric]
                    values = [r['signed_deltas'][change][metric] for r in rows]
                    check('signcount/' + det + '/' + method + '/' + change + '/' + metric,
                          s['positive_count'] + s['negative_count'] + s['zero_count'], len(rows))
                    check('positiveids/' + det + '/' + method + '/' + change + '/' + metric,
                          s['positive_case_ids'], [r['opaque_id'] for r in rows if r['signed_deltas'][change][metric] > 0])
                    check('negativeids/' + det + '/' + method + '/' + change + '/' + metric,
                          s['negative_case_ids'], [r['opaque_id'] for r in rows if r['signed_deltas'][change][metric] < 0])
                    for sign, compare in [('positive', lambda x: x > 0), ('negative', lambda x: x < 0),
                                          ('zero', lambda x: x == 0)]:
                        selected = [r['opaque_id'] for r in rows if compare(r['signed_deltas'][change][metric])]
                        check('G-sign/' + det + '/' + method + '/' + change + '/' + metric + '/' + sign + '/n',
                              s[sign + '_count'], len(selected))
                        check('G-sign/' + det + '/' + method + '/' + change + '/' + metric + '/' + sign + '/ids',
                              s[sign + '_case_ids'], selected)
    check('units/cases', aggregate['units']['case_count'], len(ids))
    check('units/cells', aggregate['units']['cell_count'], len({r['cell'] for r in cases.values()}))
    check('units/Gdetectors', aggregate['units']['detector_count_G'], len(comparisons['by_detector']))
    check('units/Gmethods', aggregate['units']['method_count_G'], len(comparisons['by_detector']['bocpd']))
    check('units/Gpoints', aggregate['units']['point_count_G'], len(comparisons['by_detector']['bocpd']['baro']['per_case'][0]['points']))
    for det in comparisons['by_detector']:
        rows = comparisons['by_detector'][det]['torai_B']['per_case']
        seeds = sorted(comparisons['by_detector'][det]['torai_B']['by_seed_on_30_cases'], key=int)
        disagree = [r['opaque_id'] for r in rows if any(
            len({r['points'][p]['per_seed'][s][m] for s in seeds}) != 1 for p in POINTS for m in METRICS)]
        output = aggregate['TORAI'][det]
        check('TORAI/' + det + '/seedids', output['seed_ids'], [int(s) for s in seeds])
        check('TORAI/' + det + '/cases', output['case_count'], len(rows))
        check('TORAI/' + det + '/disagree_n', output['seed_disagree_case_count'], len(disagree))
        check('TORAI/' + det + '/disagree_ids', output['seed_disagree_case_ids'], disagree)
        check('units/seed_count/' + det, aggregate['units']['seed_count'], len(seeds))
    outside = [{'opaque_id': o, 'detector': d, 'entity': e} for o in ids for d in DETECTORS
               for e in nsigma['cases'][o][d]['E_columns_outside_U']]
    check('outside_U/count', aggregate['outside_universe']['entity_case_count'], len(outside))
    check('outside_U/rows', aggregate['outside_universe']['rows'], outside)
    return {'status': 'PASS' if not failures else 'STOP', 'check_count': len(checks),
            'mismatch_count': len(failures), 'mismatches': failures, 'checks': checks,
            'method': 'Service timestamps recompute ranks/ties; heuristic median/MAD recompute ratios; stored seeds and cases independently recompute G means, deltas, groups and high-score cohorts.'}


def write_location(aggregate, location):
    report = Report('dinh-vi.md', RUN)
    n = report.num
    body = '# Định vị theo báo động đầu sau mốc\n\n'
    body += ('C3: N-Sigma có cờ từng cột nên có thể gắn báo động với dịch vụ đã ánh xạ. '
             'Root được chấm theo thứ tự báo động đầu sau mốc của dịch vụ; đây là phân tích nhờ nhãn mốc. '
             'Thứ tự này không xác nhận thời điểm bắt đầu sự cố, quan hệ nhân quả hoặc “lan”. '
             'BOCPD chỉ xuất điểm đổi đa biến. Heuristic (quy tắc phân tích) bước median dưới đây không là đầu ra định vị của BOCPD.\n\n')
    body += ('Mẫu có ' + n(AGG, '/units/case_count') + ' ca thuộc ' + n(AGG, '/units/cell_count') + ' ô. '
             'Các bảng theo ô và từng ca được trình bày trước khi gộp. Dịch vụ không báo trong Av đồng hạng cuối; '
             'dịch vụ hết cột sau độ nhạy vẫn ở cùng tập ứng viên. Bỏ N2 chỉ loại cột báo dày trong Nv, '
             'không bảo đảm loại cột có báo động kéo dài qua mốc.\n\n')
    body += source(AGG, '/units')
    body += '## Quy tắc và mức nền\n\n'
    body += ('Hạng là kỳ vọng khi hòa; xác suất đứng đầu cũng lấy kỳ vọng trong khối hòa đầu. '
             'Mức nền hoán vị đều danh tính dịch vụ trên các vị trí, giữ nguyên các khối hòa. '
             'Phân tích giữ cùng universe của giao thức; vì vậy số dịch vụ và mức nền không đổi khi loại cột. '
             'Có ' + n(AGG, '/outside_universe/entity_case_count') + ' cặp thực thể–ca ngoài universe: '
             '`istio-init` ở `dev-14372e1209` của N-Sigma đối chứng. Không gán thực thể này thành dịch vụ trong bảng E; '
             'cờ của nó vẫn được giữ trong bộ phát hiện gốc.\n\n')
    body += source(NS, '/cases/dev-14372e1209/nsigma_doi_chung/E_columns_outside_U')
    body += '| Bộ / độ nhạy | Tập dịch vụ | E[hạng] mức nền | P(đứng đầu) mức nền |\n|---|---|---|---|\n'
    for det in DETECTORS:
        for variant in VARIANTS:
            base = ptr('location', det, variant, 'all')
            body += ('| ' + DET_NAMES[det] + ' / ' + VAR_NAMES[variant] + ' | ' +
                     n(AGG, base + '/service_counts/0') + ' | ' + n(AGG, base + '/uniform_expected_rank') +
                     ' | ' + n(AGG, base + '/uniform_top1_probability') + ' |\n')
    body += '\n' + source(AGG, '/location')
    for det in DETECTORS:
        body += '## ' + DET_NAMES[det] + ': theo ô\n\n'
        body += '| Ô | Độ nhạy | Ca | E[hạng root] | P(root đứng đầu) | Root không báo | Root hết cột |\n|---|---|---|---|---|---|---|\n'
        for cell in sorted(aggregate['location'][det]['baseline']['by_cell']):
            for variant in VARIANTS:
                base = ptr('location', det, variant, 'by_cell', cell)
                body += ('| ' + md(cell) + ' | ' + VAR_NAMES[variant] + ' | ' +
                         ' | '.join(n(AGG, base + '/' + field) for field in
                                    ('n', 'mean_expected_rank', 'mean_top1_probability',
                                     'root_no_alarm_count', 'root_no_columns_count')) + ' |\n')
        body += '\n' + source(AGG, ptr('location', det))
        body += '## ' + DET_NAMES[det] + ': từng ca và mọi độ nhạy\n\n'
        body += ('Trong cột hạng/P, P là xác suất root đứng đầu; N/A ở thời điểm nghĩa là root không có báo động trong Av. '
                 'Mọi khối hòa và số cột còn lại từng dịch vụ nằm trong JSON nguồn.\n\n')
        body += ('| Ca | Ô | Báo root đầu sau mốc, giữ cột | Hạng/P giữ cột | Hạng/P bỏ N2 mức 5·p0 | '
                 'Hạng/P bỏ N2 mức 10·p0 | Hạng/P bỏ N2 mức 20·p0 |\n|---|---|---|---|---|---|---|\n')
        for oid, case in sorted(location['cases'].items()):
            base = ptr('cases', oid, 'nsigma', det)
            parts = [n(LOC, base + '/baseline/root_first_after_index')]
            for variant in VARIANTS:
                parts.append(n(LOC, base + '/' + variant + '/expected_rank') + ' / ' +
                             n(LOC, base + '/' + variant + '/root_top1_probability'))
            body += '| ' + oid + ' | ' + md(case['cell']) + ' | ' + ' | '.join(parts) + ' |\n'
        body += '\n' + source(LOC, '/cases')
    body += '## Tổng hợp và độ nhạy: đại lượng nào đổi chiều\n\n'
    body += '| Bộ / độ nhạy | Ca | E[hạng root] | P(root đứng đầu) | Root không báo | Root hết cột |\n|---|---|---|---|---|---|\n'
    for det in DETECTORS:
        for variant in VARIANTS:
            base = ptr('location', det, variant, 'all')
            body += ('| ' + DET_NAMES[det] + ' / ' + VAR_NAMES[variant] + ' | ' +
                     ' | '.join(n(AGG, base + '/' + field) for field in
                                ('n', 'mean_expected_rank', 'mean_top1_probability',
                                 'root_no_alarm_count', 'root_no_columns_count')) + ' |\n')
    body += '\n' + source(AGG, '/location')
    body += ('N-Sigma chính: loại cột N2 làm hạng root trung bình kém hơn ở mọi mức đã khai, '
             'trong khi xác suất đứng đầu trung bình tăng. Vì vậy không gọi độ nhạy này là cải thiện định vị chung. '
             'Ô auth/cpu và các ca mất báo động root giải thích phần giảm hạng; các ô khác có hướng thay đổi khác nhau như bảng theo ô.\n\n'
             'N-Sigma đối chứng: hạng trung bình tốt hơn mức nền ở mọi mức; xác suất đứng đầu đổi chiều so với mức nền. '
             'Bản giữ cột hơi trên nền; bỏ N2 chính cho P(root đứng đầu)=' +
             n(AGG, '/location/nsigma_doi_chung/10/all/mean_top1_probability') + ', dưới mức nền ' +
             n(AGG, '/location/nsigma_doi_chung/10/all/uniform_top1_probability') + '. '
             'Các mức bỏ N2 khác có hướng khác. Hạng tốt hơn mức nền không đồng nghĩa root thường đứng đầu.\n\n')
    body += '| Bộ / độ nhạy | Hạng tốt hơn giữ cột | Hạng kém hơn giữ cột | Hạng giữ nguyên | P đứng đầu tăng | P giảm | P giữ nguyên |\n|---|---|---|---|---|---|---|\n'
    for det in DETECTORS:
        for variant in VARIANTS[1:]:
            base = ptr('location', det, variant)
            fields = [('rank_change_vs_baseline', 'negative_count'), ('rank_change_vs_baseline', 'positive_count'),
                      ('rank_change_vs_baseline', 'zero_count'), ('top1_change_vs_baseline', 'positive_count'),
                      ('top1_change_vs_baseline', 'negative_count'), ('top1_change_vs_baseline', 'zero_count')]
            body += '| ' + DET_NAMES[det] + ' / ' + VAR_NAMES[variant] + ' | ' + ' | '.join(
                n(AGG, base + '/' + a + '/' + b) for a, b in fields) + ' |\n'
    body += '\n' + source(AGG, '/location')
    body += ('Danh sách mọi ca đổi hướng nằm ở `rank_change_vs_baseline` và `top1_change_vs_baseline` của nguồn tổng hợp; '
             'bảng từng ca ở trên giữ đủ giá trị ở mọi mức. Không chọn mức N2 theo kết quả.\n\n')
    body += '## BOCPD: bảng phụ bước nhảy tại t̂⁺\n\n'
    body += ('Bảng này chọn t̂⁺ nhờ nhãn mốc rồi xếp cột theo bước median chuẩn hóa với MAD quá khứ, trước min–max. '
             'Các cửa sổ quanh t̂⁺ được dùng cho phân tích hồi cứu. Đây không là cờ B4/V7 trong Nv và không là output định vị BOCPD. '
             'Không thêm ngưỡng hoặc gộp các cột này thành thứ hạng dịch vụ. '
             'MAD bằng không được tách riêng: cột đổi khỏi nền hằng không có bước chuẩn hóa hữu hạn để xếp cùng nhóm MAD dương.\n\n')
    body += '| Ca | Ô | w | Cột cùng bước chuẩn hóa lớn nhất | Bước chuẩn hóa | Cột MAD dương | Cột nền hằng đổi |\n|---|---|---|---|---|---|---|\n'
    for oid, case in sorted(location['cases'].items()):
        for w, h in sorted(aggregate['heuristic'][oid].items(), key=lambda x: int(x[0])):
            base = ptr('heuristic', oid, w)
            body += ('| ' + oid + ' | ' + md(case['cell']) + ' | w' + w + ' | ' +
                     md(', '.join(h['maximum_columns']) or 'N/A') + ' | ' +
                     ' | '.join(n(AGG, base + '/' + field) for field in
                                ('maximum_normalized_jump', 'regular_column_count', 'constant_change_count')) + ' |\n')
    body += '\n' + source(LOC, '/cases/{mã-ca}/bocpd/heuristic/{w}/columns')
    body += source(AGG, '/heuristic')
    body += ('Trung gian từng cột gồm median trước/sau, MAD, bước tuyệt đối và trạng thái nền hằng nằm tại JSON gốc; '
             'tên cột cùng cực đại và danh sách cột nền hằng đổi nằm tại JSON tổng hợp. '
             'Thay w có thể đổi cột lớn nhất; bảng giữ mọi w đã khai, không dùng một cấu hình để xác nhận root.\n\n')
    body += '## Mức bằng chứng, giải thích khác và lời tác giả\n\n'
    body += ('E là liên hệ: thứ tự báo động/cột được đối chiếu số học với feature đã lưu trước nối nhãn. '
             'Đọc tay của task bổ sung trung gian nhưng không xác nhận sự kiện mới tại mốc hoặc hướng ảnh hưởng giữa dịch vụ. '
             'Giải thích khác còn mở gồm cờ đã tồn tại trước mốc, khác số/loại cột theo dịch vụ, hòa nhiều dịch vụ, '
             'tải đổi, missing/ffill, cột root ít nhạy và nền không dừng. '
             'Phạm vi chỉ là RE2-TT dev với cửa sổ/nền khóa; không suy hiệu quả online hoặc khái quát sang dataset khác.\n\n')
    body += ('[BARO §3.2–3.3](https://arxiv.org/html/2405.09330v1#S3.SS2) tách bộ phát hiện đa biến khỏi RobustScorer định vị. '
             'Code N-Sigma trả các báo động metric; code BOCPD trả chỉ số điểm đổi, xem '
             '`results/T-013/ho-so-nsigma-phat-hien.md` §3 và `ho-so-bocpd.md` §1/§3. '
             'Đặc điểm không xuất native service attribution phù hợp thiết kế đã khảo sát. '
             'Chưa thấy trong nguồn đã khảo sát tác giả đề xuất thứ tự báo động đầu sau mốc của dịch vụ như bảng E, '
             'hoặc coi heuristic median/MAD này là đầu ra BOCPD.\n\n')
    body += ('Nguồn đọc tay: `results/T-029/doc-tay.md` và `runs/manual-notes-001/notes.json#/rows`. '
             'Nguồn kiểm số học độc lập: `runs/report-dinhvi-g-001/checks.json`; '
             'script `scripts/write_dinhvi_g_reports.py` tính tổng hợp rồi kiểm lại bằng thời điểm từng dịch vụ và trung gian median/MAD.\n')
    report.save(body)


def g_values(report, path, base):
    n = report.num
    output = []
    for metric in METRICS:
        output += [n(path, base + ptr('points', p, metric)) for p in POINTS]
        output += [n(path, base + ptr('signed_deltas', d, metric)) for d in CHANGES]
    return ' | '.join(output)


G_HEADER = ('| {label} | n | Hit@1(a) | Hit@1(t̂⁺) | Hit@1(t̂) | Δ cửa sổ Hit@1 | Δ sự kiện Hit@1 | '
            'Hit@5(a) | Hit@5(t̂⁺) | Hit@5(t̂) | Δ cửa sổ Hit@5 | Δ sự kiện Hit@5 |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|---|\n')


def write_comparison(aggregate, comparisons):
    report = Report('a-so-b.md', RUN)
    n = report.num
    body = '# RCA ở mốc, báo động đầu và báo động đầu sau mốc\n\n'
    body += ('C4: đây là so sánh ghép cặp trên ' + n(AGG, '/units/case_count') + ' ca dev, '
             + n(AGG, '/units/detector_count_G') + ' bộ phát hiện và ' + n(AGG, '/units/method_count_G') +
             ' phương pháp. Các điểm chạy là (a) tại mốc nhãn, (b) tại t̂ và I3 tại t̂⁺. '
             'I3 là RCA tại báo động đầu sau mốc, chọn nhờ nhãn mốc; không phải cận trên chất lượng RCA '
             'hoặc bằng chứng đã chọn đúng sự kiện thật ngoài quy ước proxy.\n\n')
    body += source(G, '/by_detector')
    body += ('Quy ước dấu: Δ cửa sổ = Hit(t̂⁺) − Hit(a); Δ sự kiện = Hit(t̂) − Hit(t̂⁺). '
             'Dương nghĩa chất lượng tăng tại điểm phía sau phép trừ; âm nghĩa giảm. '
             'Hai chênh cộng thành Hit(t̂) − Hit(a). Đây là phân rã mô tả thay điểm chạy; '
             'thay điểm còn thay nền, hậu kỳ, tập cột và dữ liệu dựng graph của ranker, nên không phân xử '
             'hai cơ chế nhân quả độc lập. Non-OK giữ trong mẫu số và chấm trượt. '
             'Hòa tính kỳ vọng theo giao thức gốc; TORAI dùng hòa khối/cụm theo giao thức.\n\n')
    body += ('Bảng theo ô và từng ca giữ nguyên số đóng băng T-024/T-025; I3 lấy bản ghi đã chép và kiểm hash. '
             'Mỗi dòng JSON có nguồn bản ghi ở `points/{điểm}/per_seed/{seed}/source_record`, '
             'nguồn số gốc ở `frozen_score_sources` và nguồn nhóm ở `group_source`. '
             'N-Sigma đối chứng không có RCA trong T-025 nên không thêm vào bảng này.\n\n')
    for det, methods in comparisons['by_detector'].items():
        body += '## ' + DET_NAMES[det] + ': theo ô\n\n'
        for method, table in methods.items():
            body += '### ' + METHOD_NAMES[method] + '\n\n' + G_HEADER.format(label='Ô')
            for cell, row in sorted(table['by_cell'].items()):
                base = ptr('by_detector', det, method, 'by_cell', cell)
                body += '| ' + md(cell) + ' | ' + n(G, base + '/n') + ' | ' + g_values(report, G, base) + ' |\n'
            body += '\n' + source(G, ptr('by_detector', det, method, 'by_cell'))
        body += '## ' + DET_NAMES[det] + ': ghép cặp từng ca\n\n'
        for method, table in methods.items():
            body += '### ' + METHOD_NAMES[method] + '\n\n'
            body += ('| Ca / ô / nhóm | Hit@1(a) | Hit@1(t̂⁺) | Hit@1(t̂) | Δ cửa sổ Hit@1 | Δ sự kiện Hit@1 | '
                     'Hit@5(a) | Hit@5(t̂⁺) | Hit@5(t̂) | Δ cửa sổ Hit@5 | Δ sự kiện Hit@5 |\n'
                     '|---|---|---|---|---|---|---|---|---|---|---|\n')
            for index, row in enumerate(table['per_case']):
                base = ptr('by_detector', det, method, 'per_case', index)
                label = row['opaque_id'] + ' / ' + md(row['cell']) + ' / ' + row['group']
                body += '| ' + label + ' | ' + g_values(report, G, base) + ' |\n'
            body += '\n' + source(G, ptr('by_detector', det, method, 'per_case'))
    body += '## Toàn mẫu và các nhóm chọn sự kiện\n\n'
    body += G_HEADER.format(label='Bộ / phương pháp / nhóm')
    for det, methods in comparisons['by_detector'].items():
        for method, table in methods.items():
            base = ptr('by_detector', det, method)
            body += '| ' + DET_NAMES[det] + ' / ' + METHOD_NAMES[method] + ' / mọi ca | ' + n(G, base + '/all30/n') + ' | ' + g_values(report, G, base + '/all30') + ' |\n'
            for group, row in sorted(table['by_event_group'].items()):
                b = base + ptr('by_event_group', group)
                body += '| ' + DET_NAMES[det] + ' / ' + METHOD_NAMES[method] + ' / ' + group + ' | ' + n(G, b + '/n') + ' | ' + g_values(report, G, b) + ' |\n'
    body += '\n' + source(G, '/by_detector/{bộ}/{phương-pháp}/all30 và /by_event_group')
    body += ('N-Sigma chính: BARO có Δ cửa sổ trung bình bằng ' +
             n(G, '/by_detector/nsigma/baro/all30/signed_deltas/a_to_tplus/hit@1') + ' cho Hit@1. '
             'Trung bình này không phải mọi ca bất biến: bảng dấu dưới đây có cả ca tăng và giảm. '
             'Chất lượng tại t̂ của các phương pháp giảm mạnh hơn tại t̂⁺ trong toàn mẫu, '
             'nhưng nhóm E-gần của TORAI có hướng ngược. '\
             'BOCPD: nhóm E-xa và E-gần cho hướng khác nhau, do cửa sổ E-gần có thể chứa mốc và dữ liệu sau mốc. '
             'Báo động trước mốc vẫn bị tính trượt thành công chung của P3; Hit RCA ở đây chỉ là chất lượng xếp hạng riêng.\n\n')
    body += '## Mọi ca có chênh lệch dương và số ca theo dấu\n\n'
    body += '| Bộ / phương pháp | Chênh / độ đo | Dương | Âm | Bằng không | Ca dương |\n|---|---|---|---|---|---|\n'
    for det, methods in comparisons['by_detector'].items():
        for method in methods:
            for change in CHANGES:
                for metric in METRICS:
                    base = ptr('G_signs', det, method, change, metric)
                    row = aggregate['G_signs'][det][method][change][metric]
                    name = 'cửa sổ' if change == 'a_to_tplus' else 'sự kiện'
                    body += ('| ' + DET_NAMES[det] + ' / ' + METHOD_NAMES[method] + ' | ' + name + ' / ' + metric +
                             ' | ' + ' | '.join(n(AGG, base + '/' + field) for field in
                                                ('positive_count', 'negative_count', 'zero_count')) +
                             ' | ' + ', '.join(row['positive_case_ids']) + ' |\n')
    body += '\n' + source(AGG, '/G_signs')
    body += ('Đây là khai mọi ngoại lệ theo dấu, không chọn ví dụ tốt cho giả thuyết. '
             'Các danh sách ca âm/bằng không cũng được giữ tại JSON tổng hợp; giá trị riêng có trong bảng từng ca.\n\n')
    body += '## TORAI: giữ seed và trung bình theo ca\n\n'
    body += ('TORAI có ' + n(AGG, '/units/seed_count') + ' seed. Mỗi điểm chạy lấy trung bình seed trong ca trước khi gộp giữa ca. '
             'Các seed không tạo thêm mẫu độc lập. Bảng từng ca phía trên là trung bình seed; '
             'bảng sau giữ số của từng seed trên cùng cohort.\n\n')
    body += G_HEADER.format(label='Bộ / seed')
    for det in comparisons['by_detector']:
        for index, seed in enumerate(aggregate['TORAI'][det]['seed_ids']):
            base = ptr('by_detector', det, 'torai_B', 'by_seed_on_30_cases', str(seed))
            body += '| ' + DET_NAMES[det] + ' / seed ' + n(AGG, ptr('TORAI', det, 'seed_ids', index)) + ' | ' + n(G, base + '/n') + ' | ' + g_values(report, G, base) + ' |\n'
    body += '\n' + source(G, '/by_detector/{bộ}/torai_B/by_seed_on_30_cases')
    for det in comparisons['by_detector']:
        body += (DET_NAMES[det] + ': có ' + n(AGG, ptr('TORAI', det, 'seed_disagree_case_count')) +
                 ' / ' + n(AGG, ptr('TORAI', det, 'case_count')) + ' ca khác Hit@1 hoặc Hit@5 giữa seed tại một điểm chạy. '
                 'Do đó các Hit seed riêng trong từng ca trùng giá trị trung bình đã trình bày; '
                 'JSON vẫn giữ đủ `points/{điểm}/per_seed` và `signed_deltas_by_seed`.\n\n')
    body += source(AGG, '/TORAI')
    body += '## CIRCA: điểm RHT lớn và bảng ghép cặp không vượt\n\n'
    body += ('Theo Q-82, báo mọi ca và tách ca có nút RHT vượt ' +
             n(G, '/by_detector/bocpd/circa_ols_rht/circa_threshold/threshold') +
             '. Tập vượt thay đổi theo điểm chạy. Mẫu ghép cặp dưới đây chỉ giữ ca không vượt ở mọi điểm; '
             'không loại Non-OK khỏi mẫu số. Đây là độ nhạy đã khóa, không là bộ số thay thế P3.\n\n')
    body += '| Bộ / cấu hình | Điểm chạy | Số ca vượt / tổng | Mã ca vượt |\n|---|---|---|---|\n'
    for det, methods in comparisons['by_detector'].items():
        for method in ('circa_ols_rht', 'circa_ols_da'):
            limits = methods[method]['circa_threshold']
            for point in POINTS:
                base = ptr('by_detector', det, method, 'circa_threshold')
                body += ('| ' + DET_NAMES[det] + ' / ' + METHOD_NAMES[method] + ' | ' + point + ' | ' +
                         n(G, base + '/high_count_by_point/' + point) + ' / ' +
                         n(G, ptr('by_detector', det, method, 'all30', 'n')) + ' | ' +
                         ', '.join(limits['high_case_ids_by_point'][point]) + ' |\n')
    body += '\n' + source(G, '/by_detector/{bộ}/{circa}/circa_threshold/high_case_ids_by_point')
    body += '### Mẫu ghép cặp, toàn mẫu còn lại\n\n' + G_HEADER.format(label='Bộ / cấu hình')
    for det in comparisons['by_detector']:
        for method in ('circa_ols_rht', 'circa_ols_da'):
            base = ptr('by_detector', det, method, 'circa_threshold', 'paired_no_node_exceeds_at_any_point')
            body += '| ' + DET_NAMES[det] + ' / ' + METHOD_NAMES[method] + ' | ' + n(G, base + '/n') + ' | ' + g_values(report, G, base) + ' |\n'
    body += '\n' + source(G, '/by_detector/{bộ}/{circa}/circa_threshold/paired_no_node_exceeds_at_any_point')
    body += '### Mẫu ghép cặp, giữ đủ các ô\n\n'
    body += ('Ô không còn ca giữ n bằng ' + n(AGG, '/circa_paired_complete/bocpd/circa_ols_rht/ts-train-service|cpu/n') +
             ' và độ đo N/A, không quy thành chất lượng bằng không.\n\n')
    for det in comparisons['by_detector']:
        for method in ('circa_ols_rht', 'circa_ols_da'):
            body += '#### ' + DET_NAMES[det] + ' / ' + METHOD_NAMES[method] + '\n\n' + G_HEADER.format(label='Ô')
            for cell in sorted(aggregate['circa_paired_complete'][det][method]):
                base = ptr('circa_paired_complete', det, method, cell)
                body += '| ' + md(cell) + ' | ' + n(AGG, base + '/n') + ' | ' + g_values(report, AGG, base) + ' |\n'
            body += '\n' + source(AGG, ptr('circa_paired_complete', det, method))
    body += ('Đổi chiều cần giữ trong kết luận: BOCPD/CIRCA RHT+DA có Δ sự kiện Hit@5=' +
             n(G, '/by_detector/bocpd/circa_ols_da/all30/signed_deltas/tplus_to_first/hit@5') +
             ' trên mọi ca, nhưng bằng ' +
             n(G, '/by_detector/bocpd/circa_ols_da/circa_threshold/paired_no_node_exceeds_at_any_point/signed_deltas/tplus_to_first/hit@5') +
             ' trên mẫu ghép cặp không vượt. Hit@1 cũng chuyển từ ' +
             n(G, '/by_detector/bocpd/circa_ols_da/all30/signed_deltas/tplus_to_first/hit@1') + ' sang ' +
             n(G, '/by_detector/bocpd/circa_ols_da/circa_threshold/paired_no_node_exceeds_at_any_point/signed_deltas/tplus_to_first/hit@1') +
             '. Hai mẫu khác nhau; không gán sự đổi chiều riêng cho ngưỡng hoặc coi một bảng là đúng và bảng kia sai. '
             'Tập ô/case còn lại được khai đầy đủ để thấy giới hạn kết luận.\n\n')
    body += '## Bằng chứng, giải thích khác và tác giả\n\n'
    body += ('I3 là can thiệp đổi điểm chạy, kết quả có dấu được kiểm trên cùng ca và phương pháp. '
             'Nó cho biết hệ quả số học của điểm chạy trong giao thức, không xác nhận nguyên nhân vật lý. '
             'Giải thích khác gồm dữ liệu lỗi vào nền, thay extrema hậu kỳ, thay cột hằng/ứng viên, '
             'thay trace dựng graph, số học RHT lớn, cạnh tranh giữa dịch vụ và thời điểm t̂⁺ vẫn lệch sự kiện thật. '
             'Không có đối chứng để tách riêng tất cả giải thích này trong task.\n\n')
    body += ('[BARO §4.8.1](https://arxiv.org/html/2405.09330v1#S4.SS8.SSS1) đã khảo sát độ nhạy RCA với điểm phát hiện '
             'và nêu nền mean/std nhận dữ liệu bất thường khi báo trễ. Nguồn đó dùng hệ/giao thức khác, '
             'không là mốc số công bố cho RE2-TT ở đây. '
             'Chưa thấy trong nguồn đã khảo sát tác giả nêu phân rã ghép cặp chọn sai sự kiện/cửa sổ như bảng G này, '
             'hoặc bảo đảm t̂⁺ là điểm chạy tối ưu. Phân tích cửa sổ đã có tại '
             '`results/T-013/cua-so-va-che-do-b.md` §1 cũng giữ các tương tác, không quy mọi thay đổi cho riêng scale nền.\n\n')
    body += ('Kiểm độc lập số gốc và bản ghi: `results/T-029/runs/compare-rca-001/verification.json`. '
             'Kiểm bảng tổng hợp/dấu/mẫu ghép cặp của báo cáo: `runs/report-dinhvi-g-001/checks.json`. '
             'Các lần chạy cũ và kết quả P3 giữ nguyên. D (thời lượng lỗi), clock tuyệt đối và sự kiện thật ngoài proxy vẫn OPEN; '
             'task không suy D từ telemetry để chấm lại, không kết luận về “lan” và không tự tổng hợp G2.\n')
    report.save(body)


def main():
    started = time.perf_counter()
    log('Lệnh có ghi: T-014-main python -B -W ignore results/T-029/scripts/write_dinhvi_g_reports.py; tạo E/G Markdown, nguồn tổng hợp và kiểm độc lập từ JSON lưu. Không rerun detector/ranker. Bước7 COMPLETE đã được root xác nhận; Claude vẫn người phản biện.')
    assert not RUN.exists(), 'Không ghi đè lượt báo cáo E/G'
    assert not (OUT / 'dinh-vi.md').exists() and not (OUT / 'a-so-b.md').exists(), 'Không ghi đè báo cáo'
    RUN.mkdir()
    write(RUN / 'invocation.json', {'time': now(), 'command': 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/write_dinhvi_g_reports.py',
                                  'script_sha256': sha(Path(__file__)), 'role': 'Hỗ trợ Codex người làm; Claude phản biện', 'status': 'RUNNING'})
    try:
        checkpoint = read(OUT / 'runs/checkpoint-after5-001/manifest.json')['files']
        source_paths = (LOC, G, NS)
        mismatches = [p for p in source_paths if sha(ROOT / p) != checkpoint[p]['sha256'] or
                      (ROOT / p).stat().st_size != checkpoint[p]['bytes']]
        if mismatches:
            log('DỪNG TOÀN TASK: nguồn E/G lệch hash checkpoint/V1: ' + repr(mismatches))
            raise RuntimeError('V1 source mismatch')
        location, nsigma, comparisons = [read(ROOT / p) for p in (LOC, NS, G)]
        assert comparisons['status'] == 'PASS'
        assert read(OUT / 'runs/compare-rca-001/verification.json')['status'] == 'PASS'
        assert (OUT / 'runs/manual-notes-001/notes.json').is_file()
        sources = {p: sha(ROOT / p) for p in source_paths}
        aggregate = assemble(location, nsigma, comparisons)
        aggregate['source_hashes'] = sources
        aggregate['interpretation'] = 'Frozen scalar aggregation only; no added thresholds, detector runs, ranker runs, native BOCPD service ranking or causal/propagation claims.'
        verification = verify_aggregates(aggregate, location, nsigma, comparisons)
        write(RUN / 'checks.json', verification)
        if verification['status'] != 'PASS':
            raise RuntimeError('E/G aggregate independent verification failed')
        write(RUN / 'source-aggregates.json', aggregate)
        write_location(aggregate, location)
        write_comparison(aggregate, comparisons)
        write(RUN / 'manifest.json', {'status': 'PASS', 'time': now(), 'seconds': time.perf_counter() - started,
                                    'source_hashes': sources, 'checks': verification['check_count'],
                                    'mismatches': verification['mismatch_count'],
                                    'script_sha256': sha(Path(__file__)),
                                    'outputs': {p.relative_to(ROOT).as_posix(): sha(p) for p in
                                                [OUT / 'dinh-vi.md', OUT / 'a-so-b.md'] + sorted(RUN.glob('*.bindings.json')) +
                                                [RUN / 'source-aggregates.json', RUN / 'checks.json']}})
        log('E/G báo cáo đã ghi, kiểm độc lập PASS, mọi số có bindings nguồn. Đã giữ theo ô/từng ca/mức nền/độ nhạy, dấu dương và CIRCA paired clean đổi chiều; không sửa JSON cũ hoặc chạy lại phương pháp. Root còn V8 và tự kiểm cuối task.')
        print(json.dumps({'status': 'PASS', 'checks': verification['check_count'], 'mismatches': verification['mismatch_count'], 'seconds': time.perf_counter() - started}))
    except Exception as error:
        write(RUN / 'manifest-stop.json', {'status': 'STOP', 'time': now(), 'seconds': time.perf_counter() - started,
                                         'error': type(error).__name__ + ': ' + str(error), 'script_sha256': sha(Path(__file__))})
        log('DỪNG bước báo cáo E/G và bước phụ thuộc: ' + type(error).__name__ + ': ' + str(error) + '; giữ mọi lượt, báo root, không đổi định nghĩa/nguồn.')
        raise


if __name__ == '__main__':
    main()

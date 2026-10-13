"""T-026: báo cáo từ JSON đã chấm; không chạy phương pháp hoặc đổi lựa chọn."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
import statistics

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-026'
PRIMARY = ('baro', 'simplerca', 'microrank_full', 'tracerca', 'circa_ols_da', 'torai_B')
SUPPORTED = PRIMARY[:4]
NAMES = {'baro': 'BARO', 'simplerca': 'SimpleRCA M4', 'microrank_full': 'MicroRank full',
         'tracerca': 'TraceRCA finite', 'circa_ols_da': 'CIRCA', 'torai_B': 'TORAI B', 'microrank_top11': 'MicroRank top-11'}
TITLES = {'main': 'Chính — 22 ca theo inject_time', 'sensitivity_A': 'Độ nhạy A — 22 ca, một ca dùng inject_timestamp',
          'sensitivity_B': 'Độ nhạy B — 21 ca đồng thuận', 'trace_guard': 'Bổ sung — cắt trace N theo độ lệch ngày'}

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def fmt(x):
    return 'N/A' if x is None else f'{x:.4f}'

def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(str(x).replace('|', ' / ').replace('\n', '<br>') for x in row) + ' |' for row in rows])

def sign(x):
    return 0 if abs(x) < 1e-12 else 1 if x > 0 else -1

def pair_ci(boot, a, b, metric):
    name = a + ' - ' + b
    if name in boot['hieu']:
        ci = boot['hieu'][name][metric]
        lo, hi = ci['lo'], ci['hi']
    else:
        ci = boot['hieu'][b + ' - ' + a][metric]
        lo, hi = (-ci['hi'] if ci['hi'] is not None else None), (-ci['lo'] if ci['lo'] is not None else None)
    return fmt(lo) + '–' + fmt(hi)

def main():
    d = read(OUT / 'cham-a.json')
    manifest = read(OUT / 'ban-ghi-dua-vao-cham.json')
    continued_summary = OUT / 'runs/full-001/summary-continued-001.json'
    continued_diag = OUT / 'runs/full-001/diagnostics-continued-001.json'
    if continued_summary.exists() != continued_diag.exists():
        raise ValueError('summary/diagnostics của lượt tiếp tục chưa đồng bộ')
    full_path = continued_summary if continued_summary.exists() else OUT / 'runs/full-001/summary.json'
    diag_path = continued_diag if continued_diag.exists() else OUT / 'runs/full-001/diagnostics.json'
    full, diag = read(full_path), read(diag_path)
    if not full.get('complete'):
        raise ValueError('không viết báo cáo khi cohort chưa hoàn tất')
    full_rel, diag_rel = full_path.relative_to(OUT).as_posix(), diag_path.relative_to(OUT).as_posix()
    coverage_path = OUT / 'runs/session-005/trace-N-coverage.json'
    coverage = read(coverage_path)
    trace_coverage = {c['opaque_id']: c for c in coverage['cases']}
    if coverage['n_cases'] != 22 or set(trace_coverage) != set(d['tables']['trace_guard']['case_ids']):
        raise ValueError('coverage không đủ/khác 22 ca đã chấm')
    guard_micro = d['tables']['trace_guard']['methods']['microrank_full']['per_case']
    error_ids = sorted(o for o, pc in guard_micro.items() if pc['status'] == 'ERROR')
    if any(trace_coverage[o]['microrank_guard_status'] != guard_micro[o]['status'] for o in trace_coverage):
        raise ValueError('trạng thái coverage khác các bản ghi đã chấm')
    pilot = read(OUT / 'runs/pilot-001/summary.json')
    comparison = read(ROOT / 'results/T-024/cham-a.json')
    sections = ['# T-026 — Xếp hạng tầng 1 chế độ (a) trên Nezha-OB dev',
        'Ngày 07/10/2026. Codex làm, Claude phản biện. Chỉ 22 ca dev, không mở test. '
        'Mục tiêu RQ1/DT18-NV3: xếp service gốc khi biết cửa sổ. Không kết luận về giá trị đồ thị.',
        '## Nguồn và lựa chọn đã khóa',
        'Mọi số chấm trong báo cáo lấy từ `results/T-026/cham-a.json`, trường `tables`; '
        'mỗi ca có `source_path` và hash bản ghi. Manifest `ban-ghi-dua-vao-cham.json` được chốt lúc '
        + manifest['frozen_at'] + ' (UTC), trước evaluator thật. Danh sách đã khai trong `runs/full-001/plan.json`. '
        'Không đổi cấu hình hoặc chọn lại bản ghi theo điểm.',
        'Q-84 giữ ba bảng mốc; Q-85/WHY-37 khóa alias tường minh, U=10, 16 kênh pod + 5 front, loại Node*, '
        'giữ lặp. BARO dùng 5N+5A ordinal; SimpleRCA dùng arrays native, không điền. '
        'Bảng cắt N chỉ nhận end < t−41 s ngày 22/08 và end < t−32 s ngày 23/08, giữ A native; '
        'không dịch clock hoặc tích chéo với các mốc Q-84. BARO trong bảng này tham chiếu chính vì không dùng trace.',
        'CIRCA và TORAI B là UNSUPPORTED theo Q-85, không gọi phương pháp. Số 0 của hai dòng này '
        'là quy tắc mẫu số khi không hỗ trợ dữ liệu, không phải đo chất lượng chẩn đoán. '
        'Seed/hashseed null; các phương pháp chạy có hashseed 0. Kiểm MicroRank hashseed 1 và đổi locator '
        'đã có trong pilot cùng hash, không chạy lại.',
        '## Giới hạn đã khai trước',
        'Nezha-OB đo metric khoảng 60 s, chỉ 5 điểm mỗi phía; RE2-TT đo 1 s. Cùng cửa sổ ±300 s '
        'không có nghĩa cùng cadence, số điểm hoặc độ phủ trace/log. Khác biệt với T-024 không được quy '
        'riêng cho đổi hệ thống. Nền sạch, recovery, thời điểm tiêm thật, đồng bộ tuyệt đối và lệch trace theo ngày '
        'còn OPEN. Hàng lặp không là quan sát độc lập; hull/giây có dòng không là quan sát liên tục.',
        '## Quy tắc chấm',
        'Các độ đo bảng chính dùng kỳ vọng khi thứ tự trong nhóm khóa bằng nhau được hoán vị đều. '
        'Root vắng và mọi trạng thái khác OK tính 0, giữ trong mẫu số. Retrieval@K=Hit@K; '
        'Rerank@1(K)=tổng Hit@1/tổng Hit@K, mẫu số 0 là N/A. Cận hòa chỉ cho độ đo đơn điệu, '
        'không cho Rerank. Bảng RCAEval dùng thứ tự gốc và báo riêng, không dùng để kết luận khi có hòa.',
        'Bootstrap lấy lại các ô root × fault thực tế, mỗi ô mang toàn bộ ca; B=10.000, seed=20261005, '
        'khoảng phân vị 95%, mẫu ghép cặp cho mọi phương pháp. Rerank tính lại trên mỗi mẫu, đếm N/A. '
        'Không chép 10 ô × 3 ca của RE2. Khoảng chỉ nói về các ô dev này, không đại diện cho test.']
    coverage_rows = []
    for oid in sorted(trace_coverage):
        c = trace_coverage[oid]
        coverage_rows.append([oid, c['guard_s'], c['main_N_nominal_s'],
                              fmt(c['main_N_observed']['end_hull_s']), c['cut_N_nominal_s'],
                              fmt(c['cut_N_observed']['end_hull_s']), fmt(c['cut_N_observed']['start_hull_s']),
                              c['main_N_observed']['spans'], c['cut_N_observed']['spans'], guard_micro[oid]['status']])
    sections += ['## Độ dài nền trace thực và điểm dừng MicroRank',
        'Nguồn `runs/session-005/trace-N-coverage.json`, từng mã ca trong `cases`; '
        'đây là metadata đầu vào, không là kết quả xếp hạng. Bảng ghi N chia theo thời điểm kết thúc '
        'của MicroRank/TraceRCA. SimpleRCA chia theo bắt đầu và cũng cắt theo end; '
        'không gọi các số này là độ dài train của SimpleRCA.',
        'Khoảng N cho phép là 300 s ở chính và 259/268 s sau cắt 41/32 s. Khoảng đó là biên cửa sổ; '
        'end hull/start hull chỉ là max−min timestamp của span thực sự có. '
        'Hull và số span lặp không chứng minh độ phủ liên tục, nền sạch hoặc số mẫu độc lập.',
        table(['Mã ca', 'Cắt s', 'N chính biên s', 'N chính end hull s', 'N cắt biên s',
               'N cắt end hull s', 'N cắt start hull s', 'Span N chính', 'Span N cắt', 'MicroRank cắt N'], coverage_rows),
        f'MicroRank cắt N có {len(error_ids)}/22 ca ERROR; mã ca: ' + (', '.join(error_ids) if error_ids else 'không có') +
        '. Nguồn trạng thái `cham-a.json → tables.trace_guard.methods.microrank_full.per_case` và bản ghi nguồn mỗi ca. '
        'Mọi ERROR được giữ trong mẫu số; không bỏ ca hoặc sửa phương pháp để cứu kết quả.',
        'Nhánh MicroRank dừng ở ERROR đầu tiên theo Q-77/WHY-31. Minh duyệt có điều kiện tiếp tục '
        '10 lượt chưa chạy sau khi chứng minh cắt N đúng, A giữ nguyên và membership ns/µs khớp. '
        'Bằng chứng `runs/session-005/microrank-stop-evidence-002.json` và quyết định nguyên văn trong LOG; '
        'lượt ERROR ban đầu và các kết quả sau điểm dừng đều được giữ. '
        'Không đổi ngưỡng, cửa sổ, seed hoặc dữ liệu vì kết quả.',
        'Bảng độ nhạy cắt N có điều kiện vì phần trace N quan sát có thể quá ngắn, dù biên cho phép vẫn 259/268 s. '
        'ERROR do thiếu mẫu nền là hạn chế của phép cắt với hợp đồng MicroRank, không là phép đo riêng '
        'chất lượng xếp hạng trên ca đó. Đổi dấu trong bảng này phải đọc cùng độ phủ và trạng thái, '
        'không quy riêng cho khả năng chẩn đoán hoặc chứng minh đồng hồ đã đồng bộ.']
    if error_ids:
        error_rows = []
        for oid in error_ids:
            low = trace_coverage[oid]['operations_below_two_in_cut_N_present_A']
            saved = read(ROOT / guard_micro[oid]['source_path'])
            error_rows.append([oid, saved.get('error'), len(low),
                               str(min((v['main_N_spans'] for v in low), default=0)) + '–' +
                               str(max((v['main_N_spans'] for v in low), default=0)),
                               str(min((v['cut_N_spans'] for v in low), default=0)) + '–' +
                               str(max((v['cut_N_spans'] for v in low), default=0)),
                               trace_coverage[oid]['checks']['A_exact_same']])
        sections += ['Chi tiết ERROR và số operation có A nhưng <2 span N sau cắt; '
                     'đường dẫn/từng operation có trong coverage JSON, thông điệp lỗi giữ từ bản ghi:',
                     table(['Mã ca', 'Lỗi gốc', 'Operation N cắt <2', 'Span N chính / op min–max',
                            'Span N cắt / op min–max', 'A giữ nguyên'], error_rows)]
    for name, t in d['tables'].items():
        sections += ['## ' + TITLES[name],
            f"Nguồn: `cham-a.json → tables.{name}`. {t['n_cases']} ca, {t['n_cells']} ô; cỡ ô: " +
            ', '.join(f'{size} ca × {count} ô' for size, count in sorted(Counter(t['cell_sizes'].values()).items())) + '.',
            table(['Phương pháp', 'Hit@1', 'Hit@3', 'Hit@5', 'Avg@5', 'MRR', 'NDCG@5', 'Retrieval@10', 'Rerank K5', 'Rerank K10'],
                [[NAMES[m]] + [fmt(t['methods'][m]['summary']['main'][k]) for k in
                  ('hit@1', 'hit@3', 'hit@5', 'avg@5', 'mrr', 'ndcg@5', 'retrieval@10', 'rerank@1(K=5)', 'rerank@1(K=10)')]
                 for m in PRIMARY]),
            table(['Phương pháp', 'OK', 'NO_EVIDENCE', 'ERROR', 'UNSUPPORTED', 'TIMEOUT'],
                [[NAMES[m]] + [t['methods'][m]['summary']['main']['trang_thai'][s] for s in
                 ('OK', 'NO_EVIDENCE', 'ERROR', 'UNSUPPORTED', 'TIMEOUT')] for m in PRIMARY]),
            'MicroRank top-11 dẫn xuất từ cùng lượt: ' + ', '.join(k + '=' + fmt(t['methods']['microrank_top11']['summary']['main'][k])
                for k in ('hit@1', 'hit@3', 'hit@5', 'mrr', 'avg@5')) + '. Không chạy thêm.']
        boot = t['bootstrap']['phuong_phap']
        sections += ['Cận bi quan–lạc quan do hòa (không là CI), nguồn `tables.' + name + '.methods.*.summary.main.can_bi_quan/can_lac_quan`:',
            table(['Phương pháp', 'Hit@1', 'Hit@3', 'Hit@5', 'MRR', 'NDCG@5', 'Avg@5', 'Retrieval@10'],
                [[NAMES[m]] + [fmt(t['methods'][m]['summary']['main']['can_bi_quan'][k]) + '–' +
                 fmt(t['methods'][m]['summary']['main']['can_lac_quan'][k]) for k in
                 ('hit@1', 'hit@3', 'hit@5', 'mrr', 'ndcg@5', 'avg@5', 'retrieval@10')] for m in PRIMARY])]
        sections += ['Khoảng bootstrap 95% (Hit@1; MRR; Rerank K5), nguồn `tables.' + name + '.bootstrap.phuong_phap`:',
            table(['Phương pháp', 'Hit@1 CI', 'MRR CI', 'Rerank K5 CI', 'Rerank K5 N/A / 10000'],
                [[NAMES[m], *[fmt(boot[m][k]['lo']) + '–' + fmt(boot[m][k]['hi']) for k in ('hit@1', 'rr', 'rerank@1(K=5)')],
                  boot[m]['rerank@1(K=5)']['n_na']] for m in PRIMARY])]
        sections += ['CI bootstrap ghép cặp 95% cho hiệu a−b; nguồn `tables.' + name + '.bootstrap.hieu`:',
            table(['Cặp', 'Hit@1 CI', 'Avg@5 CI', 'MRR CI'],
                [[NAMES[a] + ' − ' + NAMES[b]] + [pair_ci(t['bootstrap'], a, b, k)
                 for k in ('hit@1', 'avg@5', 'rr')] for a, b in combinations(SUPPORTED, 2)])]
    sections += ['## Độ nhạy và giới hạn kết luận',
        'Bảng sau xét dấu chênh trung bình cho từng cặp trong bốn phương pháp có hỗ trợ. '
        '“Ổn định Q-84” chỉ có nghĩa dấu giữ ở chính/A/B; bảng cắt N báo riêng. '
        'Hòa hoặc đảo chiều được nêu điều kiện, không đổi thiết kế. Nguồn `tables.*.methods.*.summary.main`.']
    rows, stability = [], []
    for a, b in combinations(SUPPORTED, 2):
        for metric in ('hit@1', 'avg@5', 'mrr'):
            vals = {t: d['tables'][t]['methods'][a]['summary']['main'][metric] - d['tables'][t]['methods'][b]['summary']['main'][metric] for t in TITLES}
            stable = len({sign(vals[t]) for t in ('main', 'sensitivity_A', 'sensitivity_B')}) == 1
            guard_same = sign(vals['trace_guard']) == sign(vals['main'])
            rows.append([NAMES[a] + ' − ' + NAMES[b], metric] + [fmt(vals[t]) for t in TITLES] +
                        ['Ổn định' if stable else 'Có điều kiện', 'Giữ dấu' if guard_same else 'Đổi/hòa'])
            stability.append({'a': a, 'b': b, 'metric': metric, 'differences': vals, 'stable_Q84': stable, 'same_sign_trace_guard': guard_same})
    sections += [table(['Cặp', 'Độ đo', 'Chính', 'A', 'B', 'Cắt N', 'Q-84', 'Cắt N so chính'], rows),
        'Cận 1/22 chỉ cho thay đổi trung bình Hit@k của một phương pháp khi một ca đổi đầu ra. '
        'Không dùng cận này cho hiệu hai phương pháp, Rerank hay khoảng bootstrap. '
        'Điểm trung bình và dấu không tự chứng minh khác biệt thống kê; CI từng cặp nằm trong `tables.*.bootstrap.hieu`.']
    sections += ['## Bốn tập và mức ngẫu nhiên',
        'Nguồn `tables.main.methods.*.per_case.*.four_sets/random` và `summary.random`. Inventory và tập chấm đều U=10. '
        'Tập O là sau tiền xử lý; root ngoài O có mức ngẫu nhiên O bằng 0. Thực thể ngoài U giữ chỗ và đếm riêng.',
        table(['Phương pháp', '|O| TB', 'Root trong O', 'Root trả về', 'Random O Hit1', 'Random O Hit5', 'Random U Hit1', 'Random U Hit5'],
            [[NAMES[m]] + [fmt(d['tables']['main']['methods'][m]['summary']['random'][k]) for k in
             ('O_size_mean', 'root_coverage_O', 'root_coverage_returned', 'O_hit@1', 'O_hit@5', 'U_hit@1', 'U_hit@5')] for m in PRIMARY])]
    rows = []
    for m in PRIMARY:
        pc = d['tables']['main']['methods'][m]['per_case']
        rows.append([NAMES[m], len(d['universe']), fmt(sum(x['four_sets']['quan_sat'] for x in pc.values())/len(pc)),
                     len(d['universe']), fmt(sum(x['four_sets']['tra_ve'] for x in pc.values())/len(pc)),
                     sorted({e for x in pc.values() for e in x['four_sets']['quan_sat_ngoai_U']}),
                     sorted({e for x in pc.values() for e in x['four_sets']['tra_ve_ngoai_U']})])
    sections += [table(['Phương pháp', 'Inventory', 'O TB', 'Chấm', 'Trả về TB', 'O ngoài U', 'Trả về ngoài U'], rows)]
    for field, title in [('fault', 'Theo loại lỗi'), ('nhom_loi', 'Theo nhóm lỗi'), ('cell', 'Theo ô'), ('nhom_vi_tri_p75', 'Theo nhóm vị trí root')]:
        groups = d['tables']['main']['methods']['baro']['summary']['grouped'][field]
        sections += ['## ' + title + ' — bảng chính',
            'Nguồn `tables.main.methods.*.summary.grouped.' + field + '`. Mỗi ô chỉ 1–2 ca, không suy mẫu hình từ một ô.',
            table([title, 'n'] + [NAMES[m] + ' Hit1 / MRR' for m in SUPPORTED],
                [[g, groups[g]['n']] + [fmt(d['tables']['main']['methods'][m]['summary']['grouped'][field][g]['hit@1']) + ' / ' +
                    fmt(d['tables']['main']['methods'][m]['summary']['grouped'][field][g]['mrr']) for m in SUPPORTED] for g in groups])]
    sections += ['## Từng ca — bảng chính',
        'Nguồn `tables.main.methods.*.per_case`. Hạng a–b là nhóm hòa; ∞ là root vắng/non-OK. '
        'Theo ca của A/B/cắt N đầy đủ trong JSON, giữ cùng nguồn/hash và mẫu số.']
    rows = []
    for oid in d['tables']['main']['case_ids']:
        label = d['tables']['main']['methods']['baro']['per_case'][oid]['label']
        row = [oid, label['root'], label['fault']]
        for m in SUPPORTED:
            pc = d['tables']['main']['methods'][m]['per_case'][oid]
            rank = '∞' if pc['rank_min'] is None else str(pc['rank_min']) + ('–' + str(pc['rank_max']) if pc['rank_max'] != pc['rank_min'] else '')
            row.append(rank + ' / ' + fmt(pc['hit@1']) + ' / ' + fmt(pc['rr']))
        rows.append(row)
    sections += [table(['Mã ca', 'Root', 'Loại lỗi'] + [NAMES[m] + ' hạng / H1 / RR' for m in SUPPORTED], rows)]
    for name, t in d['tables'].items():
        sections += ['## RCAEval riêng — ' + TITLES[name],
            'Nguồn `tables.' + name + '.methods.*.summary.rcaeval`; thứ tự gốc, không hòa kỳ vọng. Ca non-OK vẫn ở mẫu số.',
            table(['Phương pháp', 'AC1', 'AC3', 'AC5', 'Avg5', 'Retrieval5', 'Retrieval10', 'Rerank K5', 'Rerank K10'],
                [[NAMES[m]] + [fmt(t['methods'][m]['summary']['rcaeval'][k]) for k in
                 ('AC@1', 'AC@3', 'AC@5', 'Avg@5', 'retrieval_service(5)', 'retrieval_service(10)', 'rerank_service(1,5)', 'rerank_service(1,10)')] for m in PRIMARY])]
    sections += ['## So với T-024 — tách dataset',
        'Nguồn OB: `cham-a.json → tables.main.methods.*.summary.main`; nguồn RE2-TT: '
        '`results/T-024/cham-a.json → methods.*.summaries.dev30.main`. Các dòng cùng phương pháp, không gộp dataset. '
        'RE2-TT có inventory khác và 30 ca; OB có 22 ca, thêm lỗi mã nguồn. Cadence, cửa sổ hiệu lực, '
        'loại lỗi và coverage khác nhau nên không quy chênh riêng cho đổi hệ thống.',
        table(['Phương pháp', 'OB Hit1', 'RE2 Hit1', 'OB MRR', 'RE2 MRR', 'OB Avg5', 'RE2 Avg5'],
            [[NAMES[m]] + [fmt((d['tables']['main']['methods'][m]['summary']['main'] if dataset == 'OB' else
                comparison['methods'][m]['summaries']['dev30']['main'])[k]) for k in ('hit@1', 'mrr', 'avg@5') for dataset in ('OB', 'RE2')] for m in SUPPORTED]),
        'CIRCA/TORAI không có phép đo chất lượng trên OB để so với T-024. T-024 còn có bảng 19 ca cho CIRCA, '
        'không lấy 19 ca đó làm cohort OB. Bài Nezha có MicroRank tại Table 3 trên 56 ca OB: AS@1=41,07%, '
        'AS@3=48,21%, AS@5=62,5%. Nguồn `runs/session-005/published-reference.json`, PDF lưu tại '
        '`results/T-008/sources/FSE2023_Nezha.pdf`, trang 8–9, §5.1–5.3.1. Cohort 56 ca khác 22 dev và bài '
        'không xác nhận cùng cửa sổ/cài RCAEval đã sửa/quy tắc hòa này; không so trực tiếp hoặc gọi tái lập. '
        'Table 3 không có BARO, SimpleRCA hoặc TraceRCA; không có số công bố tương ứng để so trong bảng đó.',
        '## Kiểm đúng đắn và điều còn OPEN',
        f"Kiểm độc lập {d['validation']['n_independent_case_checks']} method × ca × bảng (kể cả top-11) khớp "
        'từng độ đo/cận/trạng thái; phép tính độc lập dùng khóa trực tiếp, không dùng `src/p3/danh_gia.py` làm phép kiểm. '
        f"{d['validation']['n_rcaeval_case_checks']} đối chiếu RCAEval theo hạng gốc cũng khớp. "
        'Nguồn `runs/evaluator-001/checks.json`; kiểm nhãn giả trên cả bốn bảng ở `runs/evaluator-fake-full-001/checks.json` trước chốt.',
        'Selector/fixture 21/21 và hồi quy T-030 57/57 đã hợp lệ trên hash cuối phiên 4; không chạy lại khi hash không đổi. '
        'Mọi record/hash/source toàn vẹn; phương pháp trace giữ split operation. Mọi đầu ra TraceRCA OK/NO_EVIDENCE '
        'có ji kiểm độc lập; ERROR/TIMEOUT giữ trạng thái/thông điệp, không giả kiểm ji. '
        'Chi tiết đầy đủ `' + diag_rel + '`, không thấy khóa không hữu hạn hoặc sai thứ tự. '
        'Pilot không được dùng làm bằng chứng mọi ca sẽ OK.',
        'OPEN: nền sạch/recovery, thời điểm tiêm thật, clock tuyệt đối, nguyên nhân lệch trace theo ngày, '
        'tính đại diện cho test và quyền dùng bằng văn bản chưa được tác giả phản hồi. Gỡ Nezha nếu tác giả phản đối theo Q-59. '
        'Không kết luận giá trị đồ thị. Giới hạn cần đưa vào tài liệu chính thức: cadence/coverage/lặp, '
        'các điều kiện độ nhạy, UNSUPPORTED và giới hạn mẫu ô nhỏ.']
    (OUT / 'cham-a.md').write_text('\n\n'.join(sections) + '\n', encoding='utf-8', newline='\n')
    with (OUT / 'runs/evaluator-001/stability.json').open('x', encoding='utf-8') as f:
        json.dump({'sources': ['results/T-026/cham-a.json'], 'pairwise_point_differences': stability}, f, ensure_ascii=False, indent=2, allow_nan=False)
    cost_rows = []
    unique = {m['path']: read(ROOT / m['path']) for m in manifest['unique_records']}
    for view in ('main', 'sensitivity_A', 'trace_guard'):
        for method in ('baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai'):
            metas = [m for m in manifest['unique_records'] if m['source_view'] == view and m['method'] == method]
            if not metas:
                continue
            rr = [unique[m['path']] for m in metas]
            wall = [r['cost']['wall_s'] for r in rr]
            rss = [r['cost'].get('peak_rss_mb') for r in rr if r['cost'].get('peak_rss_mb') is not None]
            cost_rows.append([view, method, len(rr), sum(m['reused_pilot'] for m in metas),
                f'{sum(wall):.3f}', f'{min(wall):.3f}–{max(wall):.3f}', f'{statistics.median(wall):.3f}', fmt(max(rss) if rss else None), dict(Counter(r['status'] for r in rr))])
    new = [r for r in full['runs'] if not r['reused_pilot']]
    new_wall = sum(r['cost']['wall_s'] for r in new)
    reused_wall = sum(r['cost']['wall_s'] for r in full['runs'] if r['reused_pilot'])
    measured = sum(r['cost']['wall_s'] for r in unique.values())
    cost = ['# T-026 — Chi phí chạy đầy đủ và chấm',
        'Ngày 07/10/2026. Nguồn lượt: `' + full_rel + '`, từng `cost.json`/record; '
        'danh sách duy nhất trong `ban-ghi-dua-vao-cham.json`. Không cộng lại các tham chiếu A/B/BARO guard vào thời gian máy.',
        f"{len(unique)} bản ghi nguồn: {sum(r['reused_pilot'] for r in full['runs'])} dùng lại pilot, {len(new)} mới. "
        f"Tổng wall các nguồn duy nhất {measured:.3f} s; phần chạy mới {new_wall:.3f} s ({new_wall/60:.2f} phút), "
        f"phần dùng lại {reused_wall:.3f} s. Elapsed ghi trong `{full_rel}` là {full['elapsed_s']:.3f} s. "
        'Elapsed lấy nguyên trường nguồn và có thể gồm điều phối/chờ xử lý điểm dừng; '
        'wall từng bản ghi không cộng thời gian đọc/viết báo cáo hoặc chờ hội thoại.',
        table(['View nguồn', 'Phương pháp', 'Lượt', 'Dùng lại', 'Wall tổng s', 'Min–max s', 'Median s', 'RSS max MiB', 'Trạng thái'], cost_rows),
        'RSS lấy mẫu cây tiến trình mỗi 0,1 s, tính theo MiB; có thể bỏ qua đỉnh ngắn hơn nhịp lấy mẫu. '
        'UNSUPPORTED mới tạo ở parent, không đo RSS riêng; pilot dùng lại có RSS cây tiến trình kiểm nguồn, '
        'không phải RSS phương pháp. N/A không có nghĩa 0 RAM. '
        'Thời gian UNSUPPORTED chỉ kiểm selector/hash và ghi metadata, không chạy method.',
        'Pilot không nhãn: tổng 231,404 s, RSS đỉnh 526,5 MiB, 30 bản ghi (24 OK/6 UNSUPPORTED), '
        'nguồn `runs/pilot-001/summary.json`. Phép chiếu cũ main22+guard22 là 1545,454 s (25,8 phút), chưa gồm '
        'đổi mốc, kiểm/evaluator. Trước full đã khai thêm các phần đó và dùng lại pilot, scenario tổng 25–35 phút '
        'là chưa kiểm, không khoảng tin cậy. `new_supported_estimate_s` trong plan trừ thêm wall sáu unsupported pilot; '
        'đây là sai số nhỏ của phép chiếu, không thay danh sách hoặc thiết kế. Tổng thực tế ở bảng này dùng nguồn duy nhất.',
        'Độ nhạy B tái dùng hoàn toàn 21 ca; A tái dùng 21 ca và có 6 record riêng cho ca đổi mốc; '
        'bảng cắt N có 66 trace-method records và 44 UNSUPPORTED riêng, BARO dùng lại 22 main. '
        'Không tự tạo tích chéo. MicroRank hashseed 1/locator và fixture/hồi quy hợp lệ đã giữ, không chạy lại. '
        'Nhánh cắt N giữ điểm dừng ERROR theo Q-77 và gói tiếp tục có điều kiện của Minh; '
        'lỗi trong `summary-continued-001.json` vẫn là lượt thực, không thời gian hoàn tất thành công.',
        'Kiểm nhãn giả, evaluator, xác minh cuối có wall/RSS riêng trong `runs/session-005/timing.json`; '
        'không đưa công agent/chờ hội thoại vào runtime phương pháp. TIMEOUT 3600 s đã khai trước. '
        'Không sửa nguồn/code phương pháp, không payload dẫn xuất/bytecode mới. Clock/nền sạch/cadence vẫn là giới hạn khoa học.']
    timing_path = OUT / 'runs/session-005/timing.json'
    if timing_path.exists():
        timing = read(timing_path)
        timing_fields = [('full_driver_s', 'Điều phối lượt đầy đủ trước điểm dừng'),
                         ('continuation_s', 'Điều phối phần MicroRank tiếp tục'),
                         ('fake_evaluator_s', 'Evaluator dùng nhãn giả trên cohort đủ'),
                         ('pre_freeze_verify_s', 'Xác minh trước chốt'),
                         ('coverage_s', 'Đo metadata nền trace'),
                         ('real_evaluator_s', 'Evaluator thật và kiểm độc lập')]
        missing = [key for key, _ in timing_fields if key not in timing]
        if missing:
            raise ValueError('timing thiếu số đã hứa báo: ' + ','.join(missing))
        active_s = sum(timing[key] for key, _ in timing_fields)
        cost += ['## Chi phí kiểm, evaluator và tổng thời gian máy hoạt động',
                 'Nguồn `runs/session-005/timing.json`; coverage đối chiếu trường `elapsed_s` '
                 'trong `runs/session-005/trace-N-coverage.json`. Các phần dưới là thời gian riêng '
                 'của điều phối và kiểm/chấm, không cộng lại wall từng record.',
                 table(['Phần', 'Giây'], [[label, f'{timing[key]:.3f}'] for key, label in timing_fields]),
                 f'Tổng các phần máy hoạt động đã đo là {active_s:.3f} s ({active_s/60:.2f} phút), '
                 'không cộng thời gian Minh/agent trao đổi hoặc chờ quyết định và không cộng pilot lịch sử. '
                 'Đây là tổng các phần được liệt kê, không là thời gian tính riêng của phương pháp; '
                 'wall nguồn duy nhất ở bảng trên gồm pilot được dùng lại và lượt ERROR, nên không cộng hai tổng này.']
    auxiliary_rows = []
    for action in ('coverage', 'evaluate', 'report', 'final-verify'):
        p = OUT / f'runs/aux-{action}-001/cost.json'
        if p.exists():
            aux = read(p)
            auxiliary_rows.append([action, f"{aux['wall_s']:.3f}", fmt(aux.get('peak_rss_mb')),
                                   p.relative_to(OUT).as_posix()])
    if auxiliary_rows:
        cost += ['Chi phí/RSS của các tiến trình phụ đã hoàn tất trước lúc viết báo cáo:',
                 table(['Thao tác', 'Wall s', 'RSS đỉnh MiB', 'Nguồn'], auxiliary_rows),
                 'Những dòng này mô tả lại các phần kiểm/chấm trong tổng trên, không cộng thêm lần nữa. '
                 'Chi phí của chính lượt viết báo cáo và xác minh sau bàn giao được wrapper ghi khi chúng '
                 'kết thúc; khi chưa có file không suy thành 0 RAM hoặc 0 giây.']
    (OUT / 'chi-phi.md').write_text('\n\n'.join(cost) + '\n', encoding='utf-8', newline='\n')
    print('Wrote cham-a.md, chi-phi.md and stability.json')

if __name__ == '__main__':
    main()

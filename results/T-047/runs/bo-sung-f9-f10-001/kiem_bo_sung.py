"""Bổ sung số F9/F10 từ kết quả đã lưu; không chạy M1 hoặc đổi luật.

Python -B; chỉ ghi ket-qua.json cạnh script. Giữ attempts nếu lỗi/chạy lại.
Anchor manifest trước sửa được giữ trong before/ để tái lập sau bàn giao.
"""
import sys
sys.dont_write_bytecode = True
import collections
import hashlib
import json
import math
import os
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'ket-qua.json'
BEFORE = 'results/T-047/runs/bo-sung-f9-f10-001/before/manifest.json'
Q_PATH = 'results/T-047/khoi-k/kq.json'
K_PATH = 'results/T-047/khoi-k.json'
SAMPLE_PATH = 'results/T-047/runs/b6-c1-do-ben-001/samples.jsonl'
LOSS5 = ('dev-20acb4402d', 'dev-f36d0647d5', 'dev-7f1b6b071d',
         'dev-a5cabe5fa7', 'dev-a915aa2424')
LOSS_CELLS = ('ts-order-service|loss', 'ts-travel-service|loss')
DATASETS = ('gop', 'RE2-TT', 'Nezha-OB')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(d):
    return Fraction(*d['phan_so']) if set(d) == {'phan_so'} else d


def encode(x):
    if isinstance(x, Fraction):
        return {'phan_so': [x.numerator, x.denominator]}
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-12, abs_tol=1e-12)


def main(out):
    inputs, checks = out['inputs'], out['checks']
    raw = (ROOT / BEFORE).read_bytes()
    manifest = json.loads(raw)['outputs']
    inputs[BEFORE] = {'sha256': sha(raw), 'bytes': len(raw), 'role': 'frozen manifest anchor'}

    def load(rel, parse=True):
        assert not rel.startswith('data/') and (ROOT / rel).resolve().is_relative_to(ROOT)
        raw = (ROOT / rel).read_bytes()
        assert sha(raw) == manifest[rel]['sha256'], ('SHA_INPUT', rel)
        inputs[rel] = {'sha256': sha(raw), 'bytes': len(raw), 'manifest': BEFORE}
        return json.loads(raw, object_hook=decode) if parse else raw

    handoff_path = 'results/T-047/runs/dap-phan-bien-001/ket-qua.json'
    handoff = load(handoff_path)
    protected = handoff['handoff']['protected_sha256']
    assert len(protected) == 75 and 'src/p3/danh_gia.py' in protected
    for rel, expected in protected.items():
        raw = (ROOT / rel).read_bytes()
        assert sha(raw) == expected, ('SHA_PROTECTED', rel)
        inputs[rel] = {'sha256': sha(raw), 'bytes': len(raw),
                       'source': handoff_path + '#/handoff/protected_sha256'}
    checks['protected_75_including_p3_metric_API_SHA'] = True
    q, k = load(Q_PATH), load(K_PATH)
    log = (ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md').read_text(encoding='utf8')
    assert all(digest in log for digest in k['hash_pha1'].values())
    out['phase1_gate'] = {'hashes_already_logged': k['hash_pha1'],
        'scope': 'Chỉ đọc đầu ra đã chấm/hash; không nạp nhãn hoặc payload pha 1.'}

    metrics, cross_rows = {}, []
    for cid, cfg in q['cau_hinh'].items():
        metrics[cid] = {}
        assert len(cfg['ca']) == 52
        for oid, case in cfg['ca'].items():
            p = case['theo_the_gioi']['P']
            assert close(p['do']['rr'], p['RR']), (cid, oid, 'RR')
            assert close(p['do']['hit@1'], p['hit1']), (cid, oid, 'Hit1')
            assert p['RR'] == k['cau_hinh'][cid]['RR_ca_P'][oid]
            cross_rows.append({'config': cid, 'opaque_id': oid, 'RR_match': True, 'Hit1_match': True})
        for scope in DATASETS:
            selected = [c for c in cfg['ca'].values() if scope == 'gop' or c['dataset'] == scope]
            vals = [c['theo_the_gioi']['P'] for c in selected]
            n = len(vals)
            assert n == {'gop': 52, 'RE2-TT': 30, 'Nezha-OB': 22}[scope]
            mrr = sum((v['RR'] for v in vals), Fraction(0)) / n
            assert mrr == cfg['MRR_the_gioi']['P'][scope]
            assert mrr == k['cau_hinh'][cid]['MRR_phan_so']['P'][scope]
            assert close(mrr, k['cau_hinh'][cid]['MRR']['P'][scope])
            hit1_sum = sum((v['hit1'] for v in vals), Fraction(0))
            hit3_sum = math.fsum(v['do']['hit@3'] for v in vals)
            hit5_sum = math.fsum(v['do']['hit@5'] for v in vals)
            metrics[cid][scope] = {'n': n, 'MRR': mrr, 'MRR_decimal': float(mrr),
                'Hit1': hit1_sum / n, 'Hit3': hit3_sum / n, 'Hit5': hit5_sum / n,
                'NDCG5': math.fsum(v['do']['ndcg@5'] for v in vals) / n,
                'Retrieval5': hit5_sum / n,
                'Rerank1_K5': None if hit5_sum == 0 else float(hit1_sum) / hit5_sum,
                'sum_Hit1': hit1_sum, 'sum_Hit5': hit5_sum,
                'source': Q_PATH + f'#/cau_hinh/{cid}/ca/<ca>/theo_the_gioi/P',
                'definition': 'MRR/Hit/NDCG trung bình theo ca; Rerank là tổng Hit1 chia tổng Hit5.'}
    assert len(metrics) == 16 and len(cross_rows) == 832
    expected = {
        ('K-E1+E2', 'gop'): (.7994, .6538, .9231, 1.0000, .8501),
        ('K-E1+E2', 'RE2-TT'): (.8222, .7000, .9333, 1.0000, .8672),
        ('K-E1+E2', 'Nezha-OB'): (.7682, .5909, .9091, 1.0000, .8268),
        ('K-E2+E5', 'gop'): (.7863, .6731, .8846, .9038, .8089),
        ('K-E2+E5', 'RE2-TT'): (.7229, .6000, .8333, .8333, .7385),
        ('K-E2+E5', 'Nezha-OB'): (.8727, .7727, .9545, 1.0000, .9050),
    }
    for key, values in expected.items():
        row = metrics[key[0]][key[1]]
        actual = tuple(float(row[f]) for f in ('MRR', 'Hit1', 'Hit3', 'Hit5', 'NDCG5'))
        assert tuple(round(v, 4) for v in actual) == values, (key, actual, values)
    a, b = metrics['K-E1+E2']['gop'], metrics['K-E2+E5']['gop']
    assert a['sum_Hit5'] == 52 and b['sum_Hit5'] == 47
    assert a['sum_Hit1'] == 34 and b['sum_Hit1'] == 35
    assert b['Rerank1_K5'] > a['Rerank1_K5'] and b['Retrieval5'] < a['Retrieval5']
    out['metrics'] = metrics
    out['metric_crosschecks'] = {'rows': cross_rows, 'six_Claude_rows_match_at_4_decimals': True,
        'Rerank_comparison': {'E1+E2': {'numerator': 34, 'denominator': 52},
                              'E2+E5': {'numerator': 35, 'denominator': 47}},
        'limits': ['Rerank conditional trên phần root được đưa vào top5; hai mẫu số khác nhau.',
                   'Tổng Hit5 là khối lượng/kỳ vọng số ca được truy hồi khi có hòa, không luôn là số nguyên.',
                   'MRR và Hit1 giữ Fraction; Hit3/5/NDCG lấy số thực do bộ chấm đã lưu.']}
    checks['metrics_16_configs_3_scopes_832_crosschecks'] = True
    checks['six_Claude_rows_and_conditional_Rerank_denominators'] = True

    questions = {}
    question_pairs = {'Q1': 'E2|E1+E2', 'Q3': 'E1|E1+E2',
                      'Q6': 'E1+E2|E1+E2+E3', 'Q8': 'E1+E2|E1+E2+E5'}
    for question, pair in question_pairs.items():
        a, b = ('K-' + c for c in pair.split('|'))
        v = k['cap'][pair]['theo_the_gioi']['P']
        delta = {scope: metrics[b][scope]['MRR'] - metrics[a][scope]['MRR'] for scope in DATASETS}
        assert delta == v['dMRR'], (question, pair)
        counts = {side: sum(c['theo_the_gioi']['P']['M5'] for c in q['cau_hinh'][cfg]['ca'].values())
                  for side, cfg in (('off', a), ('on', b))}
        questions[question] = {'pair': pair, 'delta_MRR': delta,
            'outcome': v['ket_cuc'], 'step': v['buoc'], 'UV6': v['UV6'],
            'M5_counts': counts, 'E5_condition': v['dieu_kien_E5'],
            'P': v['P'], 'M': v['M'], 'P_prime': v['P_phay'], 'M_prime': v['M_phay'],
            'special_harm_reasons': v['ly_do_hai_rieng'], 'N1': v['moc_gia'],
            'source': K_PATH + '#/cap/' + pair + '/theo_the_gioi/P',
            'limits': ['Kết cục luật tại một bối cảnh trên dev; không là tác dụng độc lập hoặc xác nhận cơ chế.']}
        if question == 'Q8':
            assert counts['on'] <= counts['off'] and v['dieu_kien_E5'] == 'KHONG_HAI'
    out['questions'] = questions
    checks['Q1_Q3_Q6_Q8_deltas_match_main_and_Q8_M5'] = True

    a, b = q['cau_hinh']['K-E1+E2']['ca'], q['cau_hinh']['K-E1+E2+E5']['ca']
    changes = {group: [] for group in ('up', 'down', 'same')}
    all_rows = {}
    for oid in sorted(a):
        before, after = a[oid]['theo_the_gioi']['P']['RR'], b[oid]['theo_the_gioi']['P']['RR']
        group = 'up' if after > before else 'down' if after < before else 'same'
        row = {'opaque_id': oid, 'o': a[oid]['o'], 'dataset': a[oid]['dataset'],
               'RR_before': before, 'RR_after': after, 'delta_RR': after - before, 'group': group}
        changes[group].append(row); all_rows[oid] = row
    assert {key: len(rows) for key, rows in changes.items()} == {'up': 9, 'down': 6, 'same': 37}
    assert all(all_rows[oid]['group'] == 'down' for oid in LOSS5)
    six = [row for row in all_rows.values() if row['o'] in LOSS_CELLS]
    assert len(six) == 6 and set(LOSS5) < {row['opaque_id'] for row in six}
    out['e5_changes'] = {'pair': 'E1+E2|E1+E2+E5', 'n': len(all_rows),
        'counts': {key: len(rows) for key, rows in changes.items()}, 'groups': changes,
        'five_loss_cases': [all_rows[oid] for oid in LOSS5],
        'six_cases_in_two_loss_cells': six, 'loss_cells': LOSS_CELLS,
        'source': Q_PATH + '#/cau_hinh/K-<config>/ca/<ca>/theo_the_gioi/P/RR',
        'limits': ['Năm ca loss tụt là tập con của sáu ca trong hai ô; không thay mẫu số ô bằng số ca.',
                   'Sáu ca tụt của phép so còn gồm ca ngoài nhóm loss; danh sách đủ được giữ ở groups/down.']}
    checks['E5_52_cases_9_up_6_down_37_same_and_loss_sets'] = True

    samples = [json.loads(line) for line in load(SAMPLE_PATH, False).splitlines() if line]
    frequency = collections.Counter({name: 0 for name in ('E1', 'E2', 'E3', 'E5')})
    flagged, flag_components = 0, collections.Counter()
    for sample in samples:
        winner = sample['chon_khoi']['P']['chon']
        if winner and winner != 'R0':
            frequency.update(winner.split('+'))
        flags = (sample['buoc8']['P'] or {}).get('trinh_Minh', [])
        flagged += bool(flags); flag_components.update(flags)
    assert len(samples) == 1000
    assert dict(frequency) == {'E1': 527, 'E2': 954, 'E3': 0, 'E5': 439}
    assert flagged == 521 and dict(flag_components) == {'E5': 426, 'E2': 102, 'E1': 25}
    out['component_frequency'] = {'n': len(samples), 'enabled_in_selected_configuration': dict(frequency),
        'buoc8_flagged_samples': flagged, 'buoc8_component_flags_overlapping': dict(flag_components),
        'source': SAMPLE_PATH, 'pointer_enabled': 'JSONL #/chon_khoi/P/chon',
        'pointer_flags': 'JSONL #/buoc8/P/trinh_Minh',
        'limits': ['Tần suất thành phần bật khác số mẫu có cờ và khác số cờ theo thành phần.',
                   'Không là xác suất thành phần đúng, có ích hoặc được duyệt dùng.']}
    checks['component_frequencies_and_distinct_521_flags'] = True
    out['limitations'] = ['Chỉ hậu xử lý đầu ra dev đã tái sử dụng, không chạy phương pháp hoặc nạp nhãn mới.',
        'Không đổi lựa chọn, mức HẠI, ma trận hoặc luật; không dùng độ đo báo kèm để chọn lại.',
        'Các bảng mô tả không phân xử chiều mạng, nhóm vòng, hiệu chuẩn hoặc hiệu quả độc lập.']
    out['all_checks_true'] = all(checks.values())


if __name__ == '__main__':
    started = time.perf_counter()
    attempt = {'inputs': {}, 'checks': {}, 'status': 'RUNNING',
        'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'command': [sys.executable, '-B', str(Path(__file__).resolve())],
        'dont_write_bytecode': sys.dont_write_bytecode,
        'PYTHONDONTWRITEBYTECODE': os.environ.get('PYTHONDONTWRITEBYTECODE'),
        'prior_budget_upper_seconds_not_reset': 27644.31266450882}
    prior = json.loads(OUT.read_text(encoding='utf8')) if OUT.exists() else {}
    history = prior.get('attempts', [])
    try:
        main(attempt)
        attempt['status'] = 'COMPLETE'
    except BaseException:
        attempt.update(status='ERROR', all_checks_true=False, error=traceback.format_exc())
        print(attempt['error'], file=sys.stderr)
    attempt['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    attempt['elapsed_seconds'] = time.perf_counter() - started
    history.append(attempt)
    # Giữ metadata bàn giao do root bổ sung nếu script được tái lập về sau.
    payload = dict(prior)
    payload.update(attempt)
    payload.update(schema='T047-F9-F10-supplement-v1', attempts=history,
                   script_sha256=sha(Path(__file__).read_bytes()))
    payload['timing'] = {key: attempt[key] for key in ('started_at_utc', 'finished_at_utc',
        'elapsed_seconds', 'command', 'prior_budget_upper_seconds_not_reset')}
    OUT.write_text(json.dumps(encode(payload), ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'output': str(OUT), 'status': attempt['status'],
        'all_checks_true': attempt['all_checks_true'], 'elapsed_seconds': attempt['elapsed_seconds']}, ensure_ascii=False))
    if attempt['status'] != 'COMPLETE':
        raise SystemExit(1)

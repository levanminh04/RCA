"""Tự kiểm đầu ra T-024 sau chấm; không chạy phương pháp, chỉ đọc JSON và nguồn đã chốt."""
import hashlib
import itertools
import json
import math
from collections import Counter
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-024'


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'),
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def exact(rec, root):
    if rec['status'] != 'OK':
        return {}
    blocks = rec.get('blocks')
    if blocks is None:
        rows = rec['entity_ranking']
        found = next((x for x in rows if x['entity'] == root), None)
        if found is None:
            return {}
        ranks = [i+1 for i, x in enumerate(rows) if x['tie_group'] == found['tie_group']]
        return {r: Fraction(1, len(ranks)) for r in ranks}
    pos, idx = 0, 0
    while idx < len(blocks):
        end = idx + 1
        while end < len(blocks) and blocks[end]['key'] == blocks[idx]['key']:
            end += 1
        group = blocks[idx:end]
        target = next((i for i, b in enumerate(group) if any(root in g for g in b['groups'])), None)
        sizes = [sum(map(len, b['groups'])) for b in group]
        if target is not None:
            inner, offset = None, 0
            for g in group[target]['groups']:
                if root in g:
                    inner = list(range(offset+1, offset+len(g)+1))
                    break
                offset += len(g)
            counts = Counter()
            for perm in itertools.permutations(range(len(group))):
                before = sum(sizes[j] for j in perm[:perm.index(target)])
                for p in inner:
                    counts[pos+before+p] += 1
            total = math.factorial(len(group)) * len(inner)
            return {r: Fraction(c, total) for r, c in counts.items()}
        pos += sum(sizes)
        idx = end
    return {}


def main():
    dest = OUT / 'work/kiem-cuoi.json'
    if dest.exists():
        raise RuntimeError('Không ghi đè lượt kiểm đã có')
    doc = load(OUT / 'cham-a.json')
    manifest = load(OUT / 'ban-ghi-dua-vao-cham.json')
    assert len(manifest['records']) == 420
    assert len(doc['methods']) == 11 and sum(m['primary'] for m in doc['methods'].values()) == 6
    hashes, status, n_dist = {}, Counter(), 0
    cache = {}
    for meta in manifest['records']:
        p = (ROOT / meta['path']).resolve()
        p.relative_to(ROOT)
        assert 'locked' not in p.parts
        assert sha(p) == meta['sha256']
        rec = load(p)
        cache[meta['path']] = rec
        status[rec['status']] += 1
    for mid, m in doc['methods'].items():
        assert len(m['per_case']) == 30
        for oid, pc in m['per_case'].items():
            if mid == 'microrank_top11':
                continue  # Đã kiểm dẫn xuất đối chiếu extra gốc trong evaluator.
            by_seed = {('single' if r['seed'] is None else str(r['seed'])): r
                       for r in (cache[p] for p in pc['source_paths'])}
            assert set(by_seed) == set(pc['seed_metrics'])
            for s, rec in by_seed.items():
                dist = exact(rec, pc['label']['root'])
                expected = {str(r): str(p) for r, p in dist.items()}
                assert expected == pc['rank_distribution_by_seed'][s], (mid, oid, s)
                got = pc['seed_metrics'][s]
                for k in range(1, 11):
                    hit = float(sum(v for r, v in dist.items() if r <= k))
                    assert math.isclose(hit, got[f'hit@{k}'], abs_tol=1e-12)
                rr = float(sum(v/r for r, v in dist.items()))
                assert math.isclose(rr, got['rr'], abs_tol=1e-12)
                n_dist += 1
        for co, summary in m['summaries'].items():
            ss = summary['main']
            assert ss['n'] == (30 if co == 'dev30' else 19)
            assert sum(ss['trang_thai'].values()) == ss['n']
            assert ss['hit@1'] <= ss['hit@3'] <= ss['hit@5'] <= ss['retrieval@10']
            assert ss['retrieval@5'] == ss['hit@5']
            for key in ('hit@1', 'hit@3', 'hit@5', 'avg@5', 'mrr', 'ndcg@5', 'retrieval@5', 'retrieval@10'):
                assert 0 <= ss['can_bi_quan'][key] <= ss[key] + 1e-12
                assert ss[key] <= ss['can_lac_quan'][key] + 1e-12 <= 1 + 1e-12
            for K in (5, 10):
                value = ss[f'rerank@1(K={K})']
                if ss[f'retrieval@{K}']:
                    assert math.isclose(value, ss['hit@1']/ss[f'retrieval@{K}'], abs_tol=1e-12)
                else:
                    assert value is None
    protected = load(OUT / 'work/protected-before.json')
    changes = [p for p, h in protected.items() if not (ROOT/p).exists() or sha(ROOT/p) != h]
    approval = load(OUT / 'work/minh-duyet-kiem-tay.json')
    approved_changes = approval['protected_file_changes']
    assert len(approved_changes) == 1
    approved = approved_changes[0]
    assert approved['path'] == 'tasks/T-024-cham-che-do-a/SPEC.md'
    assert protected[approved['path']] == approved['before_sha256']
    approved_bytes = (ROOT/approved['path']).read_bytes()
    assert sha(ROOT/approved['path']) == approved['after_sha256']
    assert approved_bytes.count(approved['new'].encode('utf-8')) == 1
    restored = approved_bytes.replace(approved['new'].encode('utf-8'), approved['old'].encode('utf-8'))
    assert hashlib.sha256(restored).hexdigest() == approved['before_sha256']
    unexpected_changes = [p for p in changes if p != approved['path']]
    assert not unexpected_changes, unexpected_changes
    assert sha(OUT/'ban-ghi-dua-vao-cham.json') == approval['manifest_sha256']
    validation = doc['validation']
    assert len({x['opaque_id'] for x in validation['rank_checks']}) >= 3
    assert all(x['pass'] for x in validation['rank_checks'])
    assert all(validation['bootstrap_same_seed_exact'].values())
    assert validation['random_check']['pass']
    # Fixture có hòa khối chỉ là phép kiểm, không phải một ca của cohort.
    fixture = validation['torai_block_fixture']
    assert fixture['kind'] == 'synthetic_validation_only'
    assert fixture['excluded_from_cohort'] is True and fixture['pass'] is True
    assert fixture['root'] == 'A'
    assert fixture['record'] == {'status': 'OK', 'blocks': [
        {'key': [0.5], 'groups': [['A'], ['B']]},
        {'key': [0.5], 'groups': [['C'], ['D']]}]}
    dist = exact(fixture['record'], fixture['root'])
    assert dist == {1: Fraction(1, 2), 3: Fraction(1, 2)}
    assert fixture['rank_distribution'] == {'1': '1/2', '3': '1/2'}
    manual = {f'hit@{k}': float(sum(p for r, p in dist.items() if r <= k)) for k in range(1, 11)}
    manual['rr'] = float(sum(p/r for r, p in dist.items()))
    manual['ndcg@5'] = sum(float(p)/math.log2(1+r) for r, p in dist.items() if r <= 5)
    manual['avg@5'] = sum(manual[f'hit@{k}'] for k in range(1, 6))/5
    for k, v in manual.items():
        assert math.isclose(v, fixture['manual'][k], abs_tol=1e-12)
        assert math.isclose(v, fixture['evaluator'][k], abs_tol=1e-12)
    assert math.isclose(manual['hit@1'], 1/2, abs_tol=1e-12)
    assert math.isclose(manual['rr'], 2/3, abs_tol=1e-12)
    assert math.isclose(manual['avg@5'], 4/5, abs_tol=1e-12)
    torai = [r for r in cache.values() if r['method'] == 'torai']
    n_ties = sum(any(a['key'] == b['key'] for a, b in itertools.combinations(r['blocks'], 2)) for r in torai)
    assert len(torai) == validation['torai_cohort_ties']['source_records'] == 180
    assert n_ties == validation['torai_cohort_ties']['records_with_equal_blocks'] == 0
    assert all(x['opaque_id'] in doc['cohorts']['dev30']['case_ids'] for x in validation['rank_checks'])
    assert any(x['method'] == 'torai_B' for x in validation['rank_checks'])
    for p in (OUT/'cham-a.json', OUT/'cham-a.md', OUT/'ban-ghi-dua-vao-cham.json'):
        assert p.is_file() and p.stat().st_size
        hashes[p.relative_to(ROOT).as_posix()] = sha(p)
    result = {'at': datetime.now(timezone(timedelta(hours=7))).isoformat(),
              'source_records_checked': len(manifest['records']), 'source_status': dict(status),
              'independent_rank_distributions_checked': n_dist, 'source_hashes_pass': True,
              'protected_files_checked': len(protected), 'protected_files_changed': changes,
              'approved_protected_file_changes': approved_changes,
              'unexpected_protected_file_changes': unexpected_changes,
              'manual_distinct_cases': len({x['opaque_id'] for x in validation['rank_checks']}),
              'torai_block_fixture_independent_pass': True,
              'torai_cohort_records_with_equal_blocks': n_ties,
              'main_metrics_bounds_ratio_denominator_pass': True, 'artifact_sha256': hashes,
              'files_in_T024': len([p for p in OUT.rglob('*') if p.is_file()])}
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

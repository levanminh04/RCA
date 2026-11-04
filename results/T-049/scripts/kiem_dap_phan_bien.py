"""Đối chiếu R1–R3 từ đầu ra đã khóa; không chạy lại phương pháp."""
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-049'
DEST = OUT / 'runs/dap-phan-bien-001/doi-chieu.json'
sys.path[:0] = [str(ROOT / p) for p in ('src', 'results/T-049/scripts')]
from cham import nap_nhan


def read(name):
    return json.loads((ROOT / name).read_bytes())


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def verify(name, expected):
    path = ROOT / name
    assert path.stat().st_size == expected['bytes'] and digest(path) == expected['sha256'], name


def rr(data, cfg, oid):
    return Fraction(*data['cau_hinh'][cfg]['ca'][oid]['theo_the_gioi']['P']['RR']['phan_so'])


def fr(value):
    return {'phan_so': [value.numerator, value.denominator]}


def main():
    original = read('results/T-049/runs/dap-phan-bien-001/ban-truoc/manifest.json')
    for name in ('results/T-049/runs/kb-001-cham/co-che.jsonl',
                 'results/T-049/runs/kb-001-cham/kq.json',
                 'results/T-049/runs/kb-001-cham/doc-co-che.json',
                 'results/T-049/runs/kb-001-cham/ket-cuc.json'):
        verify(name, original['outputs'][name])
    upstream_name = 'results/T-053/manifest.json'
    verify(upstream_name, original['upstream_manifests'][upstream_name])
    old = read(upstream_name)
    source = 'results/T-053/runs/k-cham-001/kq.json'
    verify(source, old['outputs'][source])
    previous = read(source)
    current = read('results/T-049/runs/kb-001-cham/kq.json')
    labels = nap_nhan(False)  # hàm kiểm hash tệp nhãn dev, chỉ dùng ở đánh giá
    cfg_c, cfg_vc = 'K-thang-C', 'K-thang-VC'
    re2 = sorted(k for k, row in labels.items() if row['dataset'] == 'RE2-TT')
    lost = [k for k in re2 if rr(previous, 'K-E1+E2+E5', k) < rr(previous, 'K-E1+E5', k)]
    gained = [k for k in re2 if rr(current, cfg_vc, k) > rr(current, cfg_c, k)]
    assert lost == gained == ['dev-a915aa2424', 'dev-f36d0647d5']
    r1 = {'cases': {}, 'MRR_RE2_E1_E5': fr(sum(rr(previous, 'K-E1+E5', k) for k in re2) / len(re2)),
          'MRR_RE2_VC': fr(sum(rr(current, cfg_vc, k) for k in re2) / len(re2)),
          'restored_RE2_MRR': fr(sum(rr(current, cfg_vc, k) - rr(current, cfg_c, k) for k in re2) / len(re2))}
    assert r1['MRR_RE2_E1_E5'] == r1['MRR_RE2_VC'] == fr(Fraction(29, 30))
    assert r1['restored_RE2_MRR'] == fr(Fraction(7, 180))
    for k in gained:
        r1['cases'][k] = {'E1_E5': fr(rr(previous, 'K-E1+E5', k)),
                         'E1_E2C_E5': fr(rr(previous, 'K-E1+E2+E5', k)),
                         'C': fr(rr(current, cfg_c, k)), 'VC': fr(rr(current, cfg_vc, k)),
                         'previous_pointer': f'/cau_hinh/K-E1+E5/ca/{k}/theo_the_gioi/P/RR',
                         'current_pointer': f'/cau_hinh/{cfg_vc}/ca/{k}/theo_the_gioi/P/RR'}
    identified = []
    fake = {}
    with (OUT / 'runs/kb-001-cham/co-che.jsonl').open(encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            row = json.loads(line)
            if row['config'] not in (cfg_c, cfg_vc):
                continue
            if row['kind'] == 'that' and row['config'] == cfg_vc:
                p = row['worlds']['P']
                if p['VC']['status'] == 'dinh_danh':
                    oid = row['id']
                    assigned = p['VC']['phu_nho_nhat']['dinh_danh']
                    identified.append({'id': oid, 'line': line_number, 'root': labels[oid]['root'],
                                       'identified': assigned, 'root_identified': labels[oid]['root'] in assigned,
                                       'RR_C': fr(rr(current, cfg_c, oid)), 'RR_VC': fr(rr(current, cfg_vc, oid)),
                                       'C_at_ceiling': rr(current, cfg_c, oid) == 1})
            elif row['kind'] == 'ce':
                fake[row['config'], row['id']] = {'line': line_number, 'worlds': {
                    w: {k: p[k] for k in ('N1', 'V0', 'keys', 'blocks', 'tier', 'channels', 'inherited')}
                    for w, p in row['worlds'].items()},
                    'VC_status': row['worlds']['P']['VC']['status']}
    assert len(identified) == 26
    root_identified = sum(v['root_identified'] for v in identified)
    ceiling = sum(v['C_at_ceiling'] for v in identified)
    assert (root_identified, ceiling) == (19, 21)
    missing = [v for v in identified if not v['root_identified']]
    assert len(missing) == 7
    r2 = {'identified': 26, 'root_identified': root_identified, 'root_not_identified': len(missing),
          'C_at_ceiling': ceiling, 'C_below_ceiling': 26 - ceiling,
          'cases': identified, 'root_not_identified_cases': missing, 'VC_E5_paths': {}}
    profiles = read('results/T-049/runs/kb-001-cham/doc-co-che.json')['pairs'][cfg_vc]['profiles']
    for oid in ('dev-63c30faf34', 'dev-607751ac0a'):
        p = profiles[oid]
        off, on = p['world_P_off'], p['world_P_on']
        path = {'frontend_tier_C': off['tier']['frontend'], 'frontend_tier_VC': on['tier']['frontend'],
                'frontend_inherited_C': [v for v in off['inherited'] if v['thuc_the'] == 'frontend'],
                'frontend_intrinsic_VC': [v for v in on['channels'] if v['entity'] == 'frontend' and v['F_I'] == 1],
                'M5_C': current['cau_hinh'][cfg_c]['ca'][oid]['theo_the_gioi']['P']['M5'],
                'M5_VC': current['cau_hinh'][cfg_vc]['ca'][oid]['theo_the_gioi']['P']['M5'],
                'profile_pointer': f'/pairs/{cfg_vc}/profiles/{oid}'}
        assert (path['M5_C'], path['M5_VC']) == (False, True)
        if oid == 'dev-63c30faf34':
            channels = [v for v in path['frontend_intrinsic_VC'] if v['class'] == 'lan_nguoc']
            explained = {v['ma'] for v in path['frontend_inherited_C']}
            assert len(channels) == 3 and {v['id'] for v in channels} == explained
            assert (path['frontend_tier_C'], path['frontend_tier_VC']) == (2, 1)
        else:
            vc_edges = [v for v in path['frontend_intrinsic_VC'] if 'E2VC:' in v['id']]
            assert len(vc_edges) == 1 and vc_edges[0]['class'] == 'khong_lan'
            assert (path['frontend_tier_C'], path['frontend_tier_VC']) == (1, 1)
        r2['VC_E5_paths'][oid] = path
    fake_ids = sorted(oid for cfg, oid in fake if cfg == cfg_c)
    assert len(fake_ids) == 30
    statuses = Counter()
    for oid in fake_ids:
        c, vc = fake[cfg_c, oid], fake[cfg_vc, oid]
        assert c['worlds'] == vc['worlds'], ('C-e changes', oid)
        statuses[vc['VC_status']] += 1
    assert statuses == {'rong': 25, 'khong_dinh_danh': 5}
    total_n1 = sum(fake[cfg_c, oid]['worlds']['P']['N1'] for oid in fake_ids)
    assert Fraction(total_n1, len(fake_ids)) == Fraction(147, 10)
    kc = read('results/T-049/runs/kb-001-cham/ket-cuc.json')[cfg_vc]
    assert kc['theo_the_gioi']['P']['moc_gia']['ve'] == 'KHONG_KICH_HOAT'
    r3 = {'fake_windows': 30, 'VC_status_P': dict(statuses), 'compared_worlds': ['P', 'S_lo', 'S_hi'],
          'checked_fields': ['N1', 'V0', 'keys', 'blocks', 'tier', 'channels', 'inherited'],
          'all_fields_equal': True, 'N1_mean_C_and_VC': fr(Fraction(total_n1, len(fake_ids))),
          'law_status_unchanged': 'KHONG_KICH_HOAT',
          'interpretation': 'C-e không phân xử được tác hại khi VC có đỉnh định danh trên tập mốc giả này; không phải bằng chứng an toàn.'}
    result = {'PASS': True, 'scope': 'Main K-b pair, P for identified/ceiling; C-e equivalence all worlds',
              'source_hashes_verified': True, 'R1': r1, 'R2': r2, 'R3': r3,
              'actions_unchanged': {'K-b': 'GIU_C', 'T6': 'DE_XUAT_BO'},
              'N1_DT18_exception': 'E3b không phải thành phần quan hệ cuối cùng, nền giữ E1-U/E2-C/E5. Không thay helper hoặc luật.'}
    with DEST.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'PASS': True, 'R1_restored': r1['restored_RE2_MRR'],
                      'R2_identified': 26, 'root_identified': 19, 'C_at_ceiling': 21,
                      'R3_equal_fake_windows': 30}, ensure_ascii=False))


if __name__ == '__main__':
    main()

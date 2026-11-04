"""Tái lập số đáp phản biện T-047 từ đầu ra đã lưu; không chạy M1.

Chạy Python -B. Chỉ ghi ket-qua.json cạnh script, giữ lịch sử attempts.
Đầu vào được kiểm SHA trước giải mã; không đọc raw dev hay data/locked.
"""
import sys
sys.dont_write_bytecode = True
import collections
import copy
import hashlib
import json
import os
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'ket-qua.json'
CELLS = ('G0D0_S0', 'G0D0_S1', 'G3D1_S0', 'G3D1_S1')
LOSS = ('dev-20acb4402d', 'dev-f36d0647d5', 'dev-7f1b6b071d',
        'dev-a5cabe5fa7', 'dev-a915aa2424')
LOSS_O = ('ts-order-service|loss', 'ts-travel-service|loss')
M5_CFG = ('E1', 'E1+E5', 'E2', 'E2+E5', 'E1+E2', 'E1+E2+E5')
NATIVE = 'results/T-047/runs/b5-c1-co-che-001/native'
EXPECTED_CELLS = {
    'E1+E2|E1+E2+E5': ['HAI', 'HAI', 'TRAI_CHIEU_DATASET', 'TRAI_CHIEU_DATASET'],
    'E2+E5|E1+E2+E5': ['HAI', 'HAI', 'KHONG_TAC_DUNG', 'KHONG_TAC_DUNG'],
    'E3+E5|E1+E3+E5': ['GIUP', 'GIUP', 'HAI', 'HAI'],
    'R0|E3+E5': ['HAI', 'HAI', 'TRAI_CHIEU_DATASET', 'TRAI_CHIEU_DATASET'],
    'E3|E1+E3': ['GIUP', 'KHONG_TAC_DUNG', 'GIUP', 'KHONG_TAC_DUNG'],
    'R0|E1+E2+E5': ['GIUP', 'TRAI_CHIEU_DATASET', 'GIUP', 'TRAI_CHIEU_DATASET'],
    'R0|E2+E5': ['GIUP', 'TRAI_CHIEU_DATASET', 'GIUP', 'TRAI_CHIEU_DATASET'],
    'E1|E1+E5': ['HAI', 'TRAI_CHIEU_DATASET', 'TRAI_CHIEU_DATASET', 'TRAI_CHIEU_DATASET'],
    'E2|E2+E5': ['GIUP', 'KHONG_TAC_DUNG', 'GIUP', 'TRAI_CHIEU_DATASET'],
    'R0|E1+E2+E3+E5': ['TRAI_CHIEU_DATASET'] * 4,
    'R0|E1+E3+E5': ['TRAI_CHIEU_DATASET'] * 4,
    'R0|E2+E3': ['TRAI_CHIEU_DATASET'] * 4,
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def hook(d):
    return Fraction(*d['phan_so']) if set(d) == {'phan_so'} else d


def encode(x):
    if isinstance(x, Fraction):
        return {'phan_so': [x.numerator, x.denominator]}
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def main(result):
    manifests, inputs, manifest_paths = {}, result['inputs'], {}
    for task in ('T-047', 'T-045', 'T-043'):
        rel = ('results/T-047/runs/dap-phan-bien-001/before/manifest.json'
               if task == 'T-047' else f'results/{task}/manifest.json')
        raw = (ROOT / rel).read_bytes()
        manifest = json.loads(raw)
        if task == 'T-047':
            files = manifest['outputs']
        elif task == 'T-045':
            files = manifest['files']
        else:
            files = {x['path']: x for x in manifest['outputs']}
        manifests[task] = files
        manifest_paths[task] = rel
        inputs[rel] = {'sha256': sha(raw), 'bytes': len(raw), 'role': 'manifest anchor'}

    def checked(rel, task='T-047', parse=True):
        rel = str(rel).replace('\\', '/')
        if 'data/locked' in rel or not (ROOT / rel).resolve().is_relative_to(ROOT):
            raise ValueError('đầu vào ngoài repo hoặc dữ liệu khóa')
        raw = (ROOT / rel).read_bytes()
        expected = manifests[task][rel]['sha256']
        got = sha(raw)
        assert got == expected, ('SHA_INPUT', rel, expected, got)
        inputs[rel] = {'sha256': got, 'bytes': len(raw),
                       'manifest': manifest_paths[task]}
        if not parse:
            return raw
        parsed = json.loads(raw, object_hook=hook)
        if '/native/T045/' in rel or '/native/T047/' in rel:
            source = parsed['source']
            anchor = 'T-045' if '/native/T045/' in rel else 'T-047'
            assert manifests[anchor][source['file']]['sha256'] == source['sha256']
            result.setdefault('native_source_references', {})[source['file']] = {
                'sha256_recorded_by_snapshot': source['sha256'],
                'manifest': manifest_paths[anchor],
                'scope': 'Đối chiếu provenance của snapshot đã hash với manifest gốc; không đọc lại payload tại bước này.'}
        return parsed

    # Các API ra quyết định không đổi kể từ T-045; kiểm trước import.
    api = sorted(p for p in manifests['T-045'] if p.startswith('src/m1_danh_gia/'))
    assert len(api) == 12
    for rel in api:
        checked(rel, 'T-045', False)
    for rel in ('results/T-047/scripts/luat_c_t047.py',
                'results/T-047/scripts/adapter_t047.py'):
        checked(rel, parse=False)
    sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts')]
    import luat_c_t047 as lc
    import adapter_t047 as ad
    from m1_danh_gia import chon_khoi, luat_c, m5, pha2, rr

    k = checked('results/T-047/khoi-k.json')
    q = checked('results/T-047/khoi-k/kq.json')
    ce = checked('results/T-047/khoi-k/ce.json')
    old = checked('results/T-045/khoi-k.json', 'T-045')
    table = checked('results/T-047/so-sanh-t045.json')
    ex_source = checked('results/T-043/ks16/dem-sau-ghep-nhan.json', 'T-043')
    ex = {tp: set().union(*(set(ex_source['o_kich_hoat'][tp][d]['o'])
                           for d in ('RE2-TT', 'Nezha-OB')))
          for tp in lc.TP}
    log = (ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md').read_text(encoding='utf8')
    assert all(digest in log for digest in k['hash_pha1'].values())
    result['phase1_gate'] = {'hashes': k['hash_pha1'], 'logged': True,
        'note': 'Đọc đầu ra pha 2/snapshot đã hash; không đọc lại payload pha 1 hoặc file nhãn.'}
    checks = result['checks']
    checks['source_API_12_SHA'] = True

    # F2: k là bội số của hai Ô, không cộng bội số năm ca.
    sample_rel = 'results/T-047/runs/b6-c1-do-ben-001/samples.jsonl'
    samples = [json.loads(x, object_hook=hook) for x in checked(sample_rel, parse=False).splitlines() if x]
    cases = q['cau_hinh']['K-E1+E2']['ca']
    o_cases = {o: sorted(oid for oid, c in cases.items() if c['o'] == o) for o in LOSS_O}
    assert set(LOSS) <= set(sum(o_cases.values(), []))
    assert len(sum(o_cases.values(), [])) == 6
    groups = {str(i): collections.Counter() for i in range(4)}
    groups['>=4'] = collections.Counter()
    flag_count, components, sizes, flagged_types = 0, collections.Counter(), collections.Counter(), collections.Counter()
    sample_rows = []
    for s in samples:
        w = s['trong_so']
        for oids in o_cases.values():
            assert len({w[x] for x in oids}) == 1
        kval = sum(w[oids[0]] for oids in o_cases.values())
        winner = s['chon_khoi']['P']['chon']
        category = 'dung' if s['loai'] != 'chon' else ('co_E5' if 'E5' in winner.split('+') else 'khong_E5')
        groups[str(kval) if kval < 4 else '>=4'][category] += 1
        flags = (s['buoc8']['P'] or {}).get('trinh_Minh', [])
        if flags:
            flag_count += 1
            components.update(flags)
            sizes[len(flags)] += 1
            flagged_types[s['loai']] += 1
        sample_rows.append({'i': s['i'], 'line': s['i'] + 1, 'k': kval,
                            'winner': winner, 'category': category, 'buoc8_trinh_Minh': flags})
    group_rows = {g: {c: count[c] for c in ('co_E5', 'khong_E5', 'dung')} for g, count in groups.items()}
    expected_groups = ((101, 0, 0), (215, 43, 0), (107, 199, 0), (15, 200, 0), (1, 118, 1))
    assert [tuple(x.values()) for x in group_rows.values()] == list(expected_groups)
    assert len(samples) == 1000 and flag_count == 521
    assert dict(components) == {'E5': 426, 'E2': 102, 'E1': 25}
    assert sizes[1] == 489 and sum(v for n, v in sizes.items() if n > 1) == 32
    assert flagged_types['chon'] == 520 and sum(flagged_types.values()) == 521
    result['bootstrap'] = {'source': sample_rel, 'pointer': 'JSONL #/trong_so, #/chon_khoi/P, #/buoc8/P/trinh_Minh',
        'k_definition': 'Tổng bội số của hai ô; mỗi ô lấy bội số chung một lần.',
        'loss_cells': o_cases, 'groups': group_rows, 'n': len(samples), 'buoc8_nonempty': flag_count,
        'components_overlapping': dict(components), 'single_component_samples': sizes[1],
        'multiple_component_samples': sum(v for n, v in sizes.items() if n > 1),
        'flagged_types': dict(flagged_types), 'samples': sample_rows}
    old_boot = checked('results/T-045/do-ben.json', 'T-045')
    new_boot = checked('results/T-047/runs/b6-c1-do-ben-001/do-ben.json')
    new_freq = collections.Counter(s['chon_khoi']['P']['chon'] for s in samples)
    assert old_boot['seed'] == 20261101 and new_boot['seed'] == 20261102
    assert old_boot['tan_suat_thang']['E1+E2'] == 767 and new_freq['E1+E2'] == 518
    assert old_boot['tan_suat_thang']['E2+E5'] == 190 and new_freq['E2+E5'] == 403
    result['bootstrap']['old_vs_new_frequency'] = {
        'old_seed': old_boot['seed'], 'new_seed': new_boot['seed'],
        'old': old_boot['tan_suat_thang'], 'new': dict(new_freq),
        'source_old': 'results/T-045/do-ben.json#/tan_suat_thang',
        'source_new': 'results/T-047/runs/b6-c1-do-ben-001/samples.jsonl #/chon_khoi/P/chon',
        'limitation': 'So tần suất tổng; khác seed, gói cổng, thang và vế C-e, không ghép mẫu hoặc quy riêng một yếu tố.'}
    checks['bootstrap_expected_groups_and_flags'] = True

    # M5 đầy đủ tại bốn ô cho sáu cấu hình, không suy từ MRR.
    values, labels, snapshot_count, rr_matches = {}, {}, 0, 0
    for cfg in M5_CFG:
        values[cfg] = {cell: {} for cell in CELLS}
        for oid, score in table['cau_hinh']['K-' + cfg]['ca'].items():
            a = checked(f'{NATIVE}/T045/that/K-{cfg}/{oid}.json')
            b = checked(f'{NATIVE}/T047/that/K-{cfg}/{oid}.json')
            snapshot_count += 2
            assert a['label'] == b['label'] and a['G_N'] == b['G_N']
            labels[oid] = a['label']; root = a['label']['root']
            blocks = (a['blocks'], a['T4c']['blocks'], ad.phuc_dung_S0(b['blocks']), b['blocks'])
            assert ad.phuc_dung_S0(a['T4c']['blocks']) == a['blocks']
            for cell, bl in zip(CELLS, blocks):
                ok = score['status'][cell] == 'OK'
                assert rr.rr_ca(bl, root, ok) == score['RR'][cell]
                rr_matches += 1
                values[cfg][cell][oid] = ok and m5.co_M5(bl, root, a['G_N'])
    assert snapshot_count == 624 and rr_matches == 1248
    m5_rows = {}
    ds = [{'ma': o, 'dataset': lab['dataset'], 'o': lab['o']} for o, lab in labels.items()]
    for a, b in (('E1+E2', 'E1+E2+E5'), ('E1', 'E1+E5'), ('E2', 'E2+E5')):
        row = {}
        for cell in CELLS:
            counts = (sum(values[a][cell].values()), sum(values[b][cell].values()))
            rt = {o: x['RR'][cell] for o, x in table['cau_hinh']['K-' + a]['ca'].items()}
            rb = {o: x['RR'][cell] for o, x in table['cau_hinh']['K-' + b]['ca'].items()}
            verdict = luat_c.ap_dung(ds, rt, rb, ex['E5'], thanh_phan='E5', M5=counts)
            assert counts[1] < counts[0]
            row[cell] = {'counts_off_on': counts, 'full_without_Ce': verdict}
        m5_rows[a + '|' + b] = row
    result['M5_four_cells'] = {'snapshots': snapshot_count, 'RR_matches': rr_matches, 'pairs': m5_rows,
        'source': NATIVE, 'pointers': ['#/G_N', '#/blocks', '#/T4c/blocks', '#/label/root'],
        'definition': 'M5 theo ca, từ đồ thị G_N; không là cờ cho mọi ca tụt hạng.'}
    checks['M5_624_snapshots_1248_RR_and_decreases_all_12_cells'] = True

    # 12 kết cục đổi: giữ mọi vế có thể áp dụng, chỉ bỏ vế C-e.
    changed = sorted(key for key in k['cap'] if old['cap'][key]['theo_the_gioi']['P']['ket_cuc'] != k['cap'][key]['theo_the_gioi']['P']['ket_cuc'])
    assert set(changed) == set(EXPECTED_CELLS)
    four = {}
    for key in changed:
        a, b, tp, comps = lc.cac_cap()[key]
        ex_pair = set().union(*(ex[x] for x in comps))
        rows = {}
        for cell in CELLS:
            rt = {o: x['RR'][cell] for o, x in table['cau_hinh']['K-' + a]['ca'].items()}
            rb = {o: x['RR'][cell] for o, x in table['cau_hinh']['K-' + b]['ca'].items()}
            aggregate = luat_c.tong_hop(ds, rt, rb, ex_pair)
            rank_only = luat_c.ket_cuc_tu_tong_hop(aggregate, delta_d=lc.DD)
            if tp == 'E5':
                full = m5_rows[key][cell]['full_without_Ce']
            else:
                assert tp != 'E3', 'nhóm này cần thêm UV-6 đầy đủ ở hai ô giữa'
                full = rank_only
            rows[cell] = {'rank_only': rank_only, 'full_without_Ce': full,
                          'aggregate': aggregate}
        verdicts = [rows[c]['full_without_Ce']['ket_cuc'] for c in CELLS]
        assert verdicts == EXPECTED_CELLS[key], (key, verdicts)
        assert verdicts[0] == old['cap'][key]['theo_the_gioi']['P']['ket_cuc']
        assert verdicts[-1] == k['cap'][key]['khong_moc_gia']['P']
        four[key] = {'cells': rows, 'verdicts': verdicts,
                     'T045': old['cap'][key]['theo_the_gioi']['P']['ket_cuc'],
                     'T047_without_Ce': k['cap'][key]['khong_moc_gia']['P'],
                     'T047_with_Ce': k['cap'][key]['theo_the_gioi']['P']['ket_cuc']}
    result['twelve_pairs'] = {'cell_order': CELLS, 'pairs': four, 'n': len(four),
        'source': 'results/T-047/so-sanh-t045.json#/cau_hinh/<cfg>/ca/<oid>/RR/<cell>',
        'limits': ['G3/D1 vẫn đi chung.', 'Không chọn lại cổng/thang/ma trận.',
                   'M5 đã tính cả bốn ô cho ba cặp E5; các cặp còn lại không áp M5/UV-6.']}
    checks['twelve_pairs_full_four_cells_and_endpoints'] = True

    # Tái tính tất cả 43 cặp có/không N1 và bộ chọn.
    with_n1 = lc.danh_gia_khoi(q, ce, ex)
    no_n1, changed_n1 = {}, []
    for key, (a, b, tp, comps) in lc.cac_cap().items():
        assert with_n1['cap'][key] == k['cap'][key]
        v = pha2.ket_cuc_cap(q, 'K-' + a, 'K-' + b, sorted(set().union(*(ex[x] for x in comps))),
                            tp, 'khoi_K', moc_gia=None, delta_d_co_dinh=lc.DD)
        assert {w: v['theo_the_gioi'][w]['ket_cuc'] for w in lc.WORLDS} == k['cap'][key]['khong_moc_gia']
        no_n1[key] = v['ket_hop']
        if v['theo_the_gioi']['P']['ket_cuc'] != k['cap'][key]['theo_the_gioi']['P']['ket_cuc']:
            changed_n1.append({'pair': key, 'without': v['theo_the_gioi']['P'],
                               'with': k['cap'][key]['theo_the_gioi']['P']})
    expected_n1 = {'R0|E1+E3', 'R0|E2+E3', 'R0|E1+E2+E3', 'R0|E1+E3+E5', 'R0|E1+E2+E3+E5'}
    assert {x['pair'] for x in changed_n1} == expected_n1
    mrr = {c[2:]: v['gop'] for c, v in pha2.mrr_cau_hinh(q).items()}
    no_choice = chon_khoi.chon(lc.TP, lc.IT_CA, lc.DO_THI, mrr, no_n1)
    assert no_choice['chon'] == with_n1['chon_khoi']['P']['chon'] == 'E1+E2'
    f6 = {}
    for key in ('E3+E5|E1+E3+E5', 'E2+E3+E5|E1+E2+E3+E5'):
        a, b, tp, comps = lc.cac_cap()[key]
        v = pha2.ket_cuc_cap(q, 'K-' + a, 'K-' + b, sorted(set().union(*(ex[x] for x in comps))),
                            tp, 'khoi_K', delta_d_co_dinh=lc.DD)['theo_the_gioi']['P']
        assert v['ket_cuc'] == 'HAI' and v['buoc'] == 3
        f6[key] = {'without_N1': v, 'with_N1': k['cap'][key]['theo_the_gioi']['P'],
                   'interpretation': 'N1 là nhánh dừng sớm; bỏ N1 vẫn HẠI, không là nguyên nhân độc quyền.'}
    result['N1'] = {'pair_count': len(no_n1), 'changed_count': len(changed_n1), 'changed': changed_n1,
                    'winner_with': with_n1['chon_khoi']['P']['chon'], 'winner_without': no_choice['chon'],
                    'without_choice': no_choice, 'F6': f6,
                    'source': 'results/T-047/khoi-k.json#/cap; khoi-k/kq.json; khoi-k/ce.json'}
    checks['N1_5_of_43_and_same_winner_F6'] = True

    # Phảnfact số học: chỉ thay RR, không phải biến thể phương pháp.
    counter = {}
    for oid in LOSS:
        modified = copy.deepcopy(q)
        a = modified['cau_hinh']['K-E2+E5']['ca'][oid]['theo_the_gioi']
        b = modified['cau_hinh']['K-E1+E2']['ca'][oid]['theo_the_gioi']
        before = {w: a[w]['RR'] for w in lc.WORLDS}
        for w in lc.WORLDS:
            a[w]['RR'] = b[w]['RR']
        run = lc.danh_gia_khoi(modified, ce, ex)
        winners = {w: run['chon_khoi'][w]['chon'] for w in lc.WORLDS}
        expected = 'E1+E2' if oid == 'dev-a915aa2424' else 'E2+E5'
        assert set(winners.values()) == {expected}
        counter[oid] = {'RR_before': before, 'RR_assigned': {w: b[w]['RR'] for w in lc.WORLDS},
                        'winners': winners}
    result['RR_counterfactual'] = {'cases': counter, 'winner_changes': 4, 'n': 5,
        'source': 'results/T-047/khoi-k/kq.json#/cau_hinh/K-<cfg>/ca/<oid>/theo_the_gioi/<world>/RR',
        'limits': ['Chỉ đổi RR của E2+E5 thành RR E1+E2 theo từng thế giới.',
                   'Hit1, M5, C-e, E_X và luật giữ nguyên; dữ liệu giả định không bảo đảm RR/Hit1 nhất quán.',
                   'Không phải kết quả của phương pháp sửa hoặc bằng chứng tác động nhân quả.']}
    checks['RR_only_counterfactual_4_of_5'] = True

    # Năm ca loss: trùng kênh/thực thể giải thích với cửa sổ giả, và đường E2/nhóm vòng.
    overlaps, totals = {}, collections.Counter()
    for oid in LOSS:
        true = checked(f'{NATIVE}/T047/that/K-E1+E2+E5/{oid}.json')
        fake = checked(f'{NATIVE}/T047/ce/K-E1+E2+E5/{oid}.json')
        root = true['label']['root']
        explain = [x for x in true['inherited_by'] if x['thuc_the'] == root and x['trang_thai'] == 'ap_dung']
        channels = {x['giai_thich_ma'] for x in explain}
        entities = {x['giai_thich'][0] for x in explain}
        fake_channels = set(fake['channels'])
        fake_entities = {x['value']['thuc_the'] for x in fake['channels'].values()}
        channel_match, entity_match = sorted(channels & fake_channels), sorted(entities & fake_entities)
        totals.update({'channel_denominator': len(channels), 'channel_numerator': len(channel_match),
                       'entity_denominator': len(entities), 'entity_numerator': len(entity_match)})
        e2 = []
        for row in explain:
            ch = true['channels'][row['giai_thich_ma']]['value']
            if ch['don_vi'].startswith('canh|') or ch['don_vi'].startswith('edge|'):
                e2.append({'inherited_by': row, 'explaining_channel': ch})
        # Lưu cả kênh thay vì đoán E2 từ tên, để kiểm riêng schema thực tế.
        e2_channels = [x['value'] for x in true['channels'].values()
                       if x['value']['don_vi'].startswith('canh|') or x['value']['don_vi'].startswith('edge|')]
        overlaps[oid] = {'root': root, 'root_applied_explanations': explain,
            'channel_denominator': len(channels), 'channel_matches': channel_match,
            'entity_denominator': len(entities), 'entity_matches': entity_match,
            'root_outgoing_edges': [x for x in true['canh'] if x[0] == root],
            'root_GN_outgoing_edges': [x for x in true['G_N'] if x[0] == root],
            'root_cycle_groups': [x for x in true['nhom_vong'] if root in x],
            'E2_channels_on_edges_from_root': [ch for ch in e2_channels
                if ch['don_vi'].split('|')[1] == root],
            'root_applied_cycle_explanations': [x for x in explain if x['quy_tac'] == 'nhom_vong'],
            'E2_explanations_detected_by_unit': e2, 'E2_channels_by_unit': e2_channels,
            'source_true': f'{NATIVE}/T047/that/K-E1+E2+E5/{oid}.json',
            'source_fake': f'{NATIVE}/T047/ce/K-E1+E2+E5/{oid}.json'}
        rr4 = {cfg: q['cau_hinh']['K-' + cfg]['ca'][oid]['theo_the_gioi']['P']['RR']
               for cfg in ('R0', 'E5', 'E2+E5', 'E1+E2+E5')}
        overlaps[oid]['RR_four_configurations_P'] = rr4
        overlaps[oid]['E5_alone_below_R0'] = rr4['E5'] < rr4['R0']
        overlaps[oid]['drop_only_after_E2_added'] = rr4['E5'] >= rr4['R0'] and rr4['E2+E5'] < rr4['R0']
    assert dict(totals) == {'channel_denominator': 44, 'channel_numerator': 1,
                            'entity_denominator': 23, 'entity_numerator': 6}
    assert sum(x['E5_alone_below_R0'] for x in overlaps.values()) == 4
    assert [o for o, x in overlaps.items() if x['drop_only_after_E2_added']] == ['dev-f36d0647d5']
    result['loss_explanations'] = {'totals': dict(totals), 'cases': overlaps,
        'units': ['ca–kênh', 'ca–thực thể'],
        'limits': ['Lấy tập duy nhất trong từng ca rồi cộng; không là số phần tử duy nhất toàn bộ dataset.',
                   'Trùng thực thể không đòi trùng kênh. Hai tỷ lệ không phân xử nhiễu/nhân quả.',
                   'Cạnh là bên gọi→bên được gọi; đường E5 không tự là chiều nguyên nhân vật lý.',
                   'Nhóm vòng và E2 có thể cùng tham gia, không coi là các nguyên nhân loại trừ nhau.']}
    checks['overlaps_1_of_44_channels_6_of_23_entities'] = True

    # Thế giới: đối chiếu điểm từng bản ghi; kiểm phân bố hạng root từ snapshot.
    world_changes, rank_changes, full_group_changes, records = [], [], [], 0
    rank_source_counts = collections.Counter()
    def groups(blocks):
        return tuple(tuple(tuple(sorted(group)) for group in block['groups']) for block in blocks)
    for cid, cfg in q['cau_hinh'].items():
        fallback = None
        for oid, row in cfg['ca'].items():
            records += 1
            p = row['theo_the_gioi']['P']
            for w in ('S_lo', 'S_hi'):
                diff = [name for name in ('RR', 'hit1', 'M5', 'hang') if row['theo_the_gioi'][w][name] != p[name]]
                if diff:
                    world_changes.append({'config': cid, 'case': oid, 'world': w, 'fields': diff})
            native_path = f'{NATIVE}/T047/that/{cid}/{oid}.json'
            if native_path in manifests['T-047']:
                native = checked(native_path)
                root = native['label']['root']
                rank_source_counts['native_snapshot'] += 1
            else:
                if fallback is None:
                    split = k['luot']['that'].replace('\\', '/') + '/theo-cau-hinh/' + cid
                    meta = checked(split + '/pha1.json')
                    payload_rel = split + '/' + meta['tep']
                    raw = checked(payload_rel, parse=False)
                    assert sha(raw) == meta['sha256']
                    fallback = {r['opaque_id']: r for r in (json.loads(line) for line in raw.splitlines() if line)}
                    assert len(fallback) == 52 and set(fallback) == set(cfg['ca'])
                    del raw
                native = fallback[oid]
                assert native['config_id'] == cid
                root = labels[oid]['root']
                rank_source_counts['existing_phase1_split'] += 1
            base = rr.phan_bo(native['blocks'], root)
            for w in ('S_lo', 'S_hi'):
                current = rr.phan_bo(native['worlds'][w]['blocks'], root)
                if current != base:
                    rank_changes.append({'config': cid, 'case': oid, 'world': w})
                if groups(native['worlds'][w]['blocks']) != groups(native['blocks']):
                    full_group_changes.append({'config': cid, 'case': oid, 'world': w})
    assert records == 832 and not world_changes and not rank_changes
    non_e3 = {key: value['theo_the_gioi']['P']['moc_gia']['tang'] for key, value in k['cap'].items() if 'E3' not in key}
    assert max(non_e3.values()) == Fraction(13, 30)
    h_rows = {}
    for name, hval in (('0.5', Fraction(1, 2)), ('1', Fraction(1)), ('2', Fraction(2))):
        run = lc.danh_gia_khoi(q, ce, ex, h=hval)
        h_rows[name] = {'h': hval, 'winners': {w: run['chon_khoi'][w]['chon'] for w in lc.WORLDS},
                        'buoc8': run['buoc8'], 'N1_hai_pairs': sorted(key for key, value in run['cap'].items()
                            if value['theo_the_gioi']['P']['moc_gia']['ve'] == 'HAI')}
        assert set(h_rows[name]['winners'].values()) == {'E1+E2'}
        assert hval > max(non_e3.values())
    result['worlds_and_h'] = {'records': records, 'score_changes': world_changes,
        'rank_sources': dict(rank_source_counts),
        'root_rank_distribution_changes': rank_changes, 'all_candidate_groups_checked': records,
        'all_candidate_groups_changes': full_group_changes,
        'non_E3_N1_deltas': non_e3,
        'max_non_E3_N1_delta': max(non_e3.values()), 'h': h_rows,
        'limits': ['Không có chênh hạng/điểm trong dữ liệu này không chứng minh ổn định ngoài dev.',
                   'Mức tăng N1 lớn nhất ngoài E3 là 13/30 < h nhỏ nhất 1/2; phép h này không tạo áp lực lên nhánh còn tranh chọn.',
                   'Không suy các khóa hoặc kênh trung gian bằng nhau từ hạng/điểm bằng nhau.']}
    checks['worlds_832_root_rank_RR_Hit1_M5_equal_and_h_logic'] = True
    result['limitations'] = ['Hậu xử lý trên dev đã tái sử dụng; không chạy phương pháp, không xác nhận hiệu quả RCA.',
        'Không thay luật chọn, tham số, ma trận, E_X hoặc mức HẠI.',
        'Kiểm số không đóng các câu hỏi về chiều nguyên nhân vật lý, nền, hiệu chuẩn hoặc G3/D1 riêng.']
    result['all_checks_true'] = all(checks.values())


if __name__ == '__main__':
    start = time.perf_counter()
    attempt = {'started_at_utc': datetime.now(timezone.utc).isoformat(),
               'command': [sys.executable, '-B', str(Path(__file__).resolve())],
               'dont_write_bytecode': sys.dont_write_bytecode,
               'PYTHONDONTWRITEBYTECODE': os.environ.get('PYTHONDONTWRITEBYTECODE'),
               'prior_budget_seconds_not_reset': 26436.123382091522,
               'inputs': {}, 'checks': {}, 'status': 'RUNNING'}
    history = []
    if OUT.exists():
        prior = json.loads(OUT.read_text(encoding='utf8'))
        history = prior.get('attempts', [])
    try:
        main(attempt)
        attempt['status'] = 'COMPLETE'
    except BaseException:
        attempt['status'] = 'ERROR'
        attempt['all_checks_true'] = False
        attempt['error'] = traceback.format_exc()
        print(attempt['error'], file=sys.stderr)
    attempt['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    attempt['elapsed_seconds'] = time.perf_counter() - start
    history.append(attempt)
    payload = {'schema': 'T047-dap-phan-bien-reproduction-v1', 'latest': attempt,
               'attempts': history, 'script_sha256': sha(Path(__file__).read_bytes())}
    # Các con trỏ ổn định cho tài liệu; attempts giữ nguyên lịch sử từng lượt.
    aliases = {'checks': 'checks', 'bootstrap': 'bootstrap', 'bon_o': 'twelve_pairs',
               'm5_bon_o': 'M5_four_cells', 'rr_gia_dinh': 'RR_counterfactual',
               'doi_chieu_moc_gia': 'loss_explanations', 'n1': 'N1',
               'world_h': 'worlds_and_h', 'inputs': 'inputs', 'limitations': 'limitations',
               'native_source_references': 'native_source_references'}
    for public, internal in aliases.items():
        if internal in attempt:
            payload[public] = attempt[internal]
    if 'loss_explanations' in attempt:
        payload['e2_duong_root'] = attempt['loss_explanations']['cases']
    if 'N1' in attempt:
        payload['f6'] = attempt['N1']['F6']
    payload['timing'] = {key: attempt[key] for key in ('started_at_utc', 'finished_at_utc',
        'elapsed_seconds', 'command', 'prior_budget_seconds_not_reset')}
    payload['all_checks_true'] = attempt['all_checks_true']
    OUT.write_text(json.dumps(encode(payload), ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'output': str(OUT), 'status': attempt['status'],
                      'all_checks_true': attempt['all_checks_true'],
                      'elapsed_seconds': attempt['elapsed_seconds']}, ensure_ascii=False))
    if attempt['status'] != 'COMPLETE':
        raise SystemExit(1)

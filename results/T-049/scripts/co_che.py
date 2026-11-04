"""Đối chiếu dấu vết gán cạnh, cờ tần suất, E5 và khóa với bản ghi native."""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from chuan_bi import OUT, ROOT, read, sha
from dong_pha1 import native_and_trace
from m1 import e5, xep_hang
from m1.kieu import Kenh
from m1_danh_gia import pha2, rr
from cham import nap_nhan, save


def rank_frame(record, trace, world):
    i = pha2.WORLDS.index(world)
    frame = pha2.giai_ma_json(trace['xep'][i])
    channels = [Kenh(**{k: v for k, v in row.items() if k != 'ma'}) for row in frame['kenh']]
    magnitude = frame['m']
    rebuilt = xep_hang.xep(channels, F_I=frame['F_I'], thuc_the_co_kenh_OK=frame['co_OK'],
                           khoa_T4c=magnitude)
    assert rebuilt['blocks'] == record['worlds'][world]['blocks'], ('khóa/hòa', world)
    assert rebuilt['tang'] == frame['ket_qua']['tang'], ('tầng', world)
    assert len({channel.ma for channel in channels}) == len(channels)
    # E5 nhận cả kênh ngoài U, còn frame xếp hạng chỉ giữ U.
    # So được FI native khi mọi nguồn có thể tạo kênh đều thuộc U.
    units = trace['world_state'][world]['units']
    owners = {row['don_vi']['thuc_the'] for row in units}
    for row in trace['gan_canh']:
        owners.update(assigned for _, _, assigned, _ in row['gan'])
        owners.update(row['dinh_danh'])
    ref = None
    if owners <= set(trace['U']):
        ref = e5.phan_loai(channels, record['extra']['canh'], bat=True)
        assert ref['F_I'] == frame['F_I'], ('E5/FI', world)
    return channels, frame, rebuilt, ref


def vc_assignment(trace, world, config):
    units = trace['world_state'][world]['units']
    scored = [(row['don_vi'], row['cham']) for row in units if row['don_vi']['nhom'] == 'canh'
              and row['cham'].get('F_raw_len')]
    if not scored:
        assert not trace['gan_canh']
        return {'status': 'rong', 'dinh': [], 'canh': []}
    i = pha2.WORLDS.index(world)
    actual = trace['gan_canh'][i]
    weighted = {(u['ben_goi'], u['ben_duoc_goi']): k['e_len'] for u, k in scored}
    nodes = sorted({n for edge in weighted for n in edge})
    graph = {frozenset(edge) for edge in weighted if edge[0] != edge[1]}
    if actual['du_phong']:
        assert len(nodes) > 25 and not actual['dinh_danh']
        status, minimum = 'du_phong', None
    elif not config.endswith('VC'):
        assert not actual['dinh_danh']
        status, minimum = 'gan_ben_duoc_goi', None
    else:
        for k in range(len(nodes) + 1):
            covers = [set(group) for group in itertools.combinations(nodes, k)
                      if all(edge.intersection(group) for edge in graph)]
            if covers:
                break
        identified = sorted(set.intersection(*covers))
        assert identified == actual['dinh_danh']
        for entity in identified:
            score = max(s for edge, s in weighted.items() if entity in edge)
            _, _, got = next(row for row in actual['kenh'] if row[:2] == [entity, f'E2VC:{entity}'])
            assert score == float(pha2.giai_ma_json(got))
        status = 'dinh_danh' if identified else 'khong_dinh_danh'
        minimum = {'co': k, 'so_phu': len(covers), 'dinh_danh': identified}
    return {'status': status, 'dinh': nodes, 'canh': [[*ab, value] for ab, value in sorted(weighted.items())],
            'phu_nho_nhat': minimum, 'native': actual}


def describe(entry, root, stage):
    record, sidecar = native_and_trace(entry)
    trace = sidecar['trace']
    out = {}
    for w in pha2.WORLDS:
        channels, frame, rank, ref = rank_frame(record, trace, w)
        relevant = {root, *[e for e, tier in rank['tang'].items() if tier == 1]}
        relevant_channels = [k for k in channels if k.co and
                             (k.thuc_the in relevant or k.nhom in ('canh', 'tan_suat'))]
        keys = {e: b['key'] for b in rank['blocks'] for g in b['groups'] for e in g if e in relevant}
        max_groups = {}
        for entity, tier in rank['tang'].items():
            active = [k for k in channels if k.co and k.thuc_the == entity and
                      (tier != 1 or frame['F_I'].get(k.ma, 1) == 1)]
            maximum = max((k.s_chinh_xac for k in active), default=None)
            best = [k for k in active if k.s_chinh_xac == maximum]
            kinds = sorted({k.loai for k in best})
            max_groups[entity] = dict(tier=tier, kinds=kinds, ids=[k.ma for k in best])
        world = {'keys': keys, 'blocks': rank['blocks'], 'N1': trace['world_state'][w]['N1'],
                 'V0': trace['world_state'][w]['V0'], 'tier': rank['tang'],
                 'max_groups': max_groups,
                 'rr': rr.rr_ca(rank['blocks'], root, record['status'] == 'OK'),
                 'E5_replay': ref is not None,
                 'inherited': (ref['inherited_by'] if ref else record['inherited_by'] if w == 'P' else None),
                 'channels': [{'entity': k.thuc_the, 'id': k.ma, 'unit': k.don_vi, 'class': k.lop,
                               'F_raw': k.F_raw, 'F_I': frame['F_I'].get(k.ma, 1), 's': k.s,
                               'm': trace['don_vi_the_gioi'][pha2.WORLDS.index(w)]['m'].get(k.don_vi, 0)}
                              for k in relevant_channels]}
        world['PV'] = {unit: value for unit, value in trace['phan_vi'].items()
                       if unit in {k.don_vi for k in relevant_channels}}
        if stage == 'K-b':
            world['VC'] = vc_assignment(trace, w, entry['config'])
        else:
            world['tan_suat'] = [row for row in trace['world_state'][w]['units']
                                 if row['don_vi']['nhom'] == 'tan_suat']
        out[w] = world
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seal', type=Path)
    parser.add_argument('scoring', type=Path)
    args = parser.parse_args()
    path = args.seal.resolve()
    expected = read(args.scoring / 'so-lan-nhin.json')
    assert sha(path) == expected['seal_sha256']
    seal = read(path)
    labels = nap_nhan(False)
    target = args.scoring / 'co-che.jsonl'
    stage = seal['stage']
    counts = Counter()
    with target.open('x', encoding='utf-8') as stream:
        for kind, entries in seal['entries'].items():
            for entry in entries:
                oid = entry['job']['opaque_id']
                evidence = describe(entry, labels[oid]['root'] if kind == 'that' else '', stage)
                for w, result in evidence.items():
                    counts[f'{entry["config"]}|{kind}|{w}|replay'] += 1
                    if stage == 'K-b':
                        counts[f'{entry["config"]}|{kind}|{w}|{result["VC"]["status"]}'] += 1
                print(json.dumps(pha2.ma_hoa_json({'kind': kind, 'id': oid, 'config': entry['config'],
                                                  'worlds': evidence}), ensure_ascii=False), file=stream)
    save(args.scoring / 'co-che-dem.json', counts)


if __name__ == '__main__':
    main()

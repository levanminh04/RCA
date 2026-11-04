"""Phát lại toàn bộ bước đổi C→VC hoặc bỏ E3b, so đủ kênh/E5/khóa/hòa với native."""
import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

from chuan_bi import OUT, ROOT, read, sha
from kiem_tai_su_dung import records
from m1 import e2, e5, xep_hang
from m1.kieu import Kenh
from m1_danh_gia import pha2
from cham import nap_nhan, save


def frames(seal):
    by_window = defaultdict(list)
    for kind, entries in seal['entries'].items():
        for entry in entries:
            by_window[kind, entry['index']].append(entry)
    for key, entries in sorted(by_window.items()):
        paths = {}
        selection = defaultdict(set)
        for entry in entries:
            for kind in ('native', 'trace'):
                spec = entry[kind]
                paths[spec['path']] = spec
                selection[spec['path']].add(entry['source_config'])
        loaded = {path: records(path, paths[path], ids) for path, ids in selection.items()}
        group = {}
        for entry in entries:
            cid = entry['config']
            record, sidecar = [loaded[entry[k]['path']][entry['source_config']] for k in ('native', 'trace')]
            group[cid] = record, sidecar['trace']
        yield key, group


def channels(trace, world):
    frame = pha2.giai_ma_json(trace['xep'][pha2.WORLDS.index(world)])
    return [Kenh(**{k: v for k, v in row.items() if k != 'ma'}) for row in frame['kenh']], frame


def assign_vc(before, trace, world):
    units = pha2.giai_ma_json(trace['world_state'][world]['units'])
    edges = {(u['don_vi']['ben_goi'], u['don_vi']['ben_duoc_goi']): u['cham']
             for u in units if u['don_vi']['nhom'] == 'canh' and u['cham'].get('F_raw_len')}
    weighted = {edge: score['e_len_q'] if score.get('e_len_q') is not None else score['e_len']
                for edge, score in edges.items()}
    assignment = e2.gan_canh([(a, b, s) for (a, b), s in weighted.items()], che_do='VC')
    previous = {channel.don_vi: channel for channel in before if channel.nhom == 'canh' and channel.co}
    result = [channel for channel in before if channel.nhom != 'canh' or not channel.co]
    for entity, name, score in assignment['kenh']:
        if name.startswith('E2VC:'):
            covered = [edge for edge in weighted if entity in edge]
            best = max(covered, key=lambda edge: (weighted[edge], edge))
        else:
            best, = [edge for edge in weighted if name == f'E2:{edge[0]}->{edge[1]}']
        unit = f'canh|{best[0]}|{best[1]}'
        source = previous[unit]
        result.append(Kenh(entity, name, 'len', 'khong_lan', float(score),
                           loai='phan_vi', nhom='canh', khoi_phat=source.khoi_phat, don_vi=unit,
                           s_q=score if isinstance(score, Fraction) else None))
    return result


def replay(channels, trace, record, world):
    graph = record['extra']['canh']
    effect = e5.phan_loai(channels, graph, bat=True)
    i = pha2.WORLDS.index(world)
    mdv = pha2.giai_ma_json(trace['don_vi_the_gioi'][i]['m'])
    magnitude = {}
    for channel in channels:
        if channel.co:
            m = mdv.get(channel.don_vi, 0)
            raw, intrinsic = magnitude.get(channel.thuc_the, (0, 0))
            magnitude[channel.thuc_the] = (max(raw, m), max(intrinsic, m)
                                          if effect['F_I'].get(channel.ma, 1) else intrinsic)
    rank = xep_hang.xep(channels, F_I=effect['F_I'], khoa_T4c=magnitude,
                        thuc_the_co_kenh_OK={k.thuc_the for k in channels if k.trang_thai == 'OK'})
    return effect, rank


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scoring', type=Path)
    args = parser.parse_args()
    folder = args.scoring.resolve()
    assert folder.parent == OUT / 'runs'
    receipt = read(folder / 'so-lan-nhin.json')
    path = ROOT / receipt['seal']
    assert sha(path) == receipt['seal_sha256']
    seal = read(path)
    if seal['stage'] == 'K-b':
        pairs = [('K-thang-C', 'K-thang-VC'), ('K-day-du-C', 'K-day-du-VC')]
    else:
        pairs = [tuple(seal['configs'])]
    labels = nap_nhan(False)
    counts, rows = Counter(), []
    for (kind, index), group in frames(seal):
        for off, on in pairs:
            off_record, off_trace = group[off]
            on_record, on_trace = group[on]
            oid = on_record['opaque_id']
            for world in pha2.WORLDS:
                off_channels, off_frame = channels(off_trace, world)
                on_channels, on_frame = channels(on_trace, world)
                if seal['stage'] == 'K-b':
                    candidate = assign_vc(off_channels, off_trace, world)
                    target, frame, trace = on_record, on_frame, on_trace
                    source_graph = off_record['extra']['canh']
                    assert source_graph == on_record['extra']['canh']
                else:
                    candidate = [k for k in on_channels if k.nhom != 'tan_suat']
                    target, frame, trace = off_record, off_frame, off_trace
                    assert off_record['extra']['canh'] == on_record['extra']['canh']
                expected_channels = off_channels if seal['stage'] == 'T6' else on_channels
                assert {k.ma: asdict(k) for k in candidate} == {k.ma: asdict(k) for k in expected_channels}
                units = trace['world_state'][world]['units']
                owners = {u['don_vi']['thuc_the'] for u in units
                          if u['don_vi']['nhom'] != 'canh' and
                          (u['cham'].get('F_raw_len') or u['cham'].get('F_raw_xuong'))}
                edge_frames = trace['gan_canh']
                if edge_frames:
                    owners.update(row[0] for row in edge_frames[pha2.WORLDS.index(world)]['kenh'])
                assert owners <= set(trace['U']), 'Cần phục hồi kênh ngoài U để replay E5'
                effect, rank = replay(candidate, trace, target, world)
                assert effect['F_I'] == frame['F_I'], (kind, index, world, on, 'FI')
                assert rank['blocks'] == target['worlds'][world]['blocks'], (kind, index, world, on, 'blocks')
                assert rank['tang'] == frame['ket_qua']['tang'], (kind, index, world, on, 'tier')
                counts[f'{on}|{kind}|{world}'] += 1
                rows.append(dict(kind=kind, index=index, id=oid, pair=[off, on], world=world,
                                 channels=len(candidate), FI=len(effect['F_I']),
                                 root=labels[oid]['root'] if kind == 'that' else None))
    save(folder / 'replay-cap.json', {'PASS': True, 'counts': counts, 'rows': rows})
    print('PASS replay cặp', sum(counts.values()), flush=True)


if __name__ == '__main__':
    main()

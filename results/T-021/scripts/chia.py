"""T-021 bước 5: chia dev/test/giữ ngoài theo ô (root × loại lỗi), hai phiên bản, hai gói.

Chỉ dùng census nhãn (runs/census-002) và nhóm vị trí đã tính (runs/vi-tri-001). Không đọc dữ liệu đo.
Chạy: py -3 -X utf8 results/T-021/scripts/chia.py --run chia-001
Seed 20261004 (dùng lại seed T-020; seed không mang thông tin về kết quả).
Thứ tự ô: SHA-256 của "seed|dataset|root|fault", như results/T-020/scripts/chia_theo_o.py.

Phiên bản "ty-le" (như T-020): ô có ca TX2 ép vào dev; trong các ô còn lại, ceil(1/3) ô đầu theo thứ tự hash vào dev, còn lại test.
Phiên bản "phan-tang": làm như trên nhưng riêng trong từng loại lỗi: mỗi loại lỗi có ceil(1/3) số ô của nó ở dev
(tính cả ô TX2 đã ép), phần còn lại test.
RE2-TT ở cả hai phiên bản: 10 ô dev của v1 (30 ca TX2) ở dev, 20 ô kia (60 ca TX1) ở test.
Bộ giữ ngoài: nguyên bộ, mọi ca phải là TX0 (MRP §4:117).
"""
import argparse, collections, csv, hashlib, json, math, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R = lambda *p: os.path.join(ROOT, *p)
SEED = '20261004'
CENSUS = 'results/T-021/runs/census-002/census-cases.csv'
VITRI = 'results/T-021/runs/vi-tri-001/vi-tri-theo-o.csv'

PACKAGES = {
    'A': {'RE2-TT': 'split', 'Eadro-TT': 'split', 'Nezha-OB': 'split', 'RE3-OB': 'holdout'},
    'B': {'RE2-TT': 'split', 'Eadro-TT': 'split', 'Nezha-OB': 'split', 'Eadro-SN': 'split', 'Nezha-TT': 'split',
          'RE3-TT': 'split', 'RE3-OB': 'holdout', 'OpenRCA-Bank': 'holdout'},
}
FAULT_GROUP = {
    'cpu': 'tài nguyên', 'mem': 'tài nguyên', 'disk': 'tài nguyên', 'cpu_load': 'tài nguyên',
    'cpu_contention': 'tài nguyên', 'cpu_consumed': 'tài nguyên',
    'delay': 'mạng', 'loss': 'mạng', 'network_delay': 'mạng', 'network_loss': 'mạng',
    'socket': 'tài nguyên',  # stress-ng, results/T-002/the-rcaeval.md:17
    'return': 'mã nguồn', 'exception': 'mã nguồn',
    'f1': 'mã nguồn', 'f2': 'mã nguồn', 'f3': 'mã nguồn', 'f4': 'mã nguồn', 'f5': 'mã nguồn',
}


def h(ds, cell):
    return hashlib.sha256(f'{SEED}|{ds}|{cell[0]}|{cell[1]}'.encode()).hexdigest()


def fault_group(ds, fault):
    if ds == 'OpenRCA-Bank':
        f = fault.lower()
        return 'mạng' if 'network' in f else 'tài nguyên'
    return FAULT_GROUP[fault]


def load_positions():
    pos = collections.defaultdict(dict)
    with open(R(VITRI), encoding='utf-8') as f:
        for x in csv.DictReader(f):
            ds = x['dataset']
            if ds == 'RE2-TT' and x['do_thi'] != 'pre_injection':
                continue
            if ds in ('RE2-OB', 'RE3-TT') :
                continue
            key = (x['root'], x['fault'])
            pos[ds].setdefault(key, set()).add(x['nhom_p75'])
    out = {ds: {k: (v.pop() if len(v) == 1 else 'phụ thuộc đồng hồ') for k, v in d.items()} for ds, d in pos.items()}
    # RE2-TT: ô test không có đồ thị đã lưu; suy theo root từ các ô dev cùng root (chưa kiểm)
    by_root = collections.defaultdict(set)
    for (root, _), g in out['RE2-TT'].items():
        by_root[root].add(g)
    out['RE2-TT-root'] = {r: (g.pop() if len(g) == 1 else 'không ổn định') for r, g in by_root.items()}
    return out


def split(ds, cells, version):
    tx2 = {k for k, cs in cells.items() if any(c['tx'] == 'TX2' for c in cs)}
    if ds == 'RE2-TT':
        assert len(tx2) == 10 and sum(len(cells[k]) for k in tx2) == 30
        return {k: 'dev' if k in tx2 else 'test' for k in cells}
    dev = set(tx2)
    if version == 'ty-le':
        rest = sorted((k for k in cells if k not in tx2), key=lambda k: h(ds, k))
        dev |= set(rest[:math.ceil(len(rest) / 3)])
    else:
        by_fault = collections.defaultdict(list)
        for k in cells:
            by_fault[k[1]].append(k)
        for f, ks in by_fault.items():
            target = math.ceil(len(ks) / 3)
            forced = [k for k in ks if k in tx2]
            rest = sorted((k for k in ks if k not in tx2), key=lambda k: h(ds, k))
            dev |= set(rest[:max(0, target - len(forced))])
    return {k: 'dev' if k in dev else 'test' for k in cells}


def adjacency(ds, roles):
    """Ca liền kề trong cùng phiên/ngày mà nằm khác phía (dev/test). Chỉ Eadro, Nezha có nhiều lần tiêm mỗi file."""
    fam = ds.split('-')[0]
    if fam == 'Eadro':
        lab = json.load(open(R('results/T-009/runs/run-001/labels.json'), encoding='utf-8'))
        ev = [(x['source'], x['start'], x['start'] + x['duration'], (x['service'], x['fault']))
              for x in lab if 'Eadro-' + x['dataset'] == ds]
    elif fam == 'Nezha':
        lab = json.load(open(R('results/T-008/runs/run-001/labels.json'), encoding='utf-8'))
        ev = [(x['date'], int(x['inject_timestamp_raw']), int(x['inject_timestamp_raw']), (x['service'], x['fault']))
              for x in lab if 'Nezha-' + x['dataset'] == ds]
    else:
        return None
    by = collections.defaultdict(list)
    for e in ev:
        by[e[0]].append(e)
    pairs, gaps = 0, []
    for _, es in by.items():
        es.sort(key=lambda e: e[1])
        for a, b in zip(es, es[1:]):
            if roles[a[3]] != roles[b[3]]:
                pairs += 1
                gaps.append(round(b[1] - a[2]))
    gaps.sort()
    return dict(nhom_file=len(by), cap_lien_ke_khac_phia=pairs,
                khoang_cach_giay_min=gaps[0] if gaps else None,
                khoang_cach_giay_trung_vi=gaps[len(gaps) // 2] if gaps else None)


HAU_TO = ' (suy theo root, chưa kiểm)'


def nhom(x):
    # so phủ theo nhóm vị trí; trạng thái "suy theo root" báo ở trường riêng (REVIEW-2 R1)
    return x['nhom_vi_tri_p75'].replace(HAU_TO, '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    out_dir = R('results/T-021/runs', a.run)
    os.makedirs(out_dir, exist_ok=False)
    os.makedirs(R('results/T-021/chia-theo-o'), exist_ok=True)
    with open(R(CENSUS), encoding='utf-8') as f:
        census = list(csv.DictReader(f))
    pos = load_positions()
    report = {}
    for pkg, sel in PACKAGES.items():
        for version in ('ty-le', 'phan-tang'):
            out, summ, cover, adj = [], [], {}, {}
            for ds, strat in sel.items():
                rows = [c for c in census if c['dataset'] == ds]
                assert rows, ds
                cells = collections.defaultdict(list)
                for c in rows:
                    cells[(c['root'], c['fault'])].append(c)
                if strat == 'holdout':
                    roles = {k: 'giu-ngoai' for k in cells}
                    assert all(c['tx'] == 'TX0' for c in rows), f'{ds}: giữ ngoài phải toàn TX0'
                else:
                    roles = split(ds, cells, version)
                for k, cs in cells.items():
                    if roles[k] != 'dev':
                        assert all(c['tx'] != 'TX2' for c in cs), (ds, k)
                    if ds == 'RE2-TT':
                        p = pos['RE2-TT'].get(k) or (pos['RE2-TT-root'].get(k[0], 'OPEN') + ' (suy theo root, chưa kiểm)')
                    elif ds in pos:
                        p = pos[ds].get(k, 'OPEN')
                    else:
                        p = 'OPEN'
                    for c in cs:
                        out.append(dict(goi=pkg, phien_ban=version, dataset=ds, case=c['case'], root=c['root'],
                                        fault=c['fault'], nhom_loi=fault_group(ds, c['fault']), rep=c['rep'],
                                        tx=c['tx'], probe_trieu_chung='có' if c['probe_trieu_chung'] else '',
                                        vai_tro=roles[k], nhom_vi_tri_p75=p, seed=SEED))
                # tổng khớp census
                got = [x for x in out if x['dataset'] == ds]
                assert len(got) == len(rows) and len({(x['root'], x['fault']) for x in got}) == len(cells)
                for role in sorted(set(roles.values())):
                    ks = [k for k in cells if roles[k] == role]
                    cs = [c for k in ks for c in cells[k]]
                    summ.append(dict(dataset=ds, vai_tro=role, o=len(ks), ca=len(cs),
                                     o_mot_lan_lap=sum(1 for k in ks if len(cells[k]) == 1),
                                     tx=dict(collections.Counter(c['tx'] for c in cs)),
                                     loai_loi=sorted({k[1] for k in ks})))
                adj[ds] = adjacency(ds, roles) if strat == 'split' else None
            # mỗi ô đúng một phía
            sides = collections.defaultdict(set)
            for x in out:
                sides[(x['dataset'], x['root'], x['fault'])].add(x['vai_tro'])
            assert all(len(v) == 1 for v in sides.values())
            # phủ theo phía (K6): nhóm lỗi, loại lỗi, nhóm vị trí
            for role in ('dev', 'test', 'giu-ngoai'):
                xs = [x for x in out if x['vai_tro'] == role]
                cover[role] = dict(nhom_loi=dict(collections.Counter(x['nhom_loi'] for x in xs)),
                                   nhom_vi_tri_theo_ca=dict(collections.Counter(nhom(x) for x in xs)),
                                   ca_vi_tri_suy_theo_root_chua_kiem=sum(1 for x in xs if HAU_TO in x['nhom_vi_tri_p75']))
            # loại lỗi chỉ có ở một phía, theo từng bộ được chia
            vang = []
            for ds, strat in sel.items():
                if strat != 'split':
                    continue
                f_dev = {x['fault'] for x in out if x['dataset'] == ds and x['vai_tro'] == 'dev'}
                f_test = {x['fault'] for x in out if x['dataset'] == ds and x['vai_tro'] == 'test'}
                for f in sorted(f_dev ^ f_test):
                    vang.append(dict(dataset=ds, fault=f, chi_o=('dev' if f in f_dev else 'test')))
                g_dev = {nhom(x) for x in out if x['dataset'] == ds and x['vai_tro'] == 'dev'}
                g_test = {nhom(x) for x in out if x['dataset'] == ds and x['vai_tro'] == 'test'}
                for g in sorted(g_dev ^ g_test):
                    vang.append(dict(dataset=ds, nhom_vi_tri=g, chi_o=('dev' if g in g_dev else 'test')))
            name = f'{pkg}-{version}'
            with open(R('results/T-021/chia-theo-o', name + '.csv'), 'w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=list(out[0]))
                w.writeheader()
                w.writerows(out)
            report[name] = dict(tom_tat=summ, phu_theo_phia=cover, vang_mot_phia=vang, ca_lien_ke_khac_phia=adj,
                                assert_dat=['mỗi ô đúng một phía', 'không ca TX2 ở test hay giữ ngoài',
                                            'mọi ca giữ ngoài là TX0', 'tổng ca và ô khớp census-002',
                                            'RE2-TT: 10 ô / 30 ca TX2 ở dev'])
    with open(os.path.join(out_dir, 'bao-cao-chia.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    for n, r_ in report.items():
        print('==', n)
        for s in r_['tom_tat']:
            print(' ', s)
        print('  vắng một phía:', r_['vang_mot_phia'])
        print('  liền kề khác phía:', r_['ca_lien_ke_khac_phia'])


if __name__ == '__main__':
    main()

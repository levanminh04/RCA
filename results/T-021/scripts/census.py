"""T-021 bước 2: đếm lại ca, root, ô và mức tiếp xúc (TX) từ file kết quả gốc.

Chỉ đọc results/ của các task cũ. Không đọc data/locked/, không đọc dữ liệu đo.
Chạy: py -3 -X utf8 results/T-021/scripts/census.py --run census-001
Nguồn TX chia ba nhóm (SPEC T-021, Đầu vào):
  v1  : docs/MRP.md:120, docs/knowledge/K2-du-lieu.md §1-2
  the : các task thẻ T-002, T-003, T-008-T-012, T-019 (đọc thống kê dữ liệu đo -> TX1)
  chay: sổ chạy phương pháp T-005-T-007, T-013-T-018 (đã thấy kết quả phương pháp -> TX2)
"""
import argparse, collections, csv, json, os, re, tarfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R = lambda *p: os.path.join(ROOT, *p)


def rows(path):
    with open(R(path), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def jload(path):
    with open(R(path), encoding='utf-8') as f:
        return json.load(f)


CASE_RE = re.compile(r'^(re[123])(tt|ob|ss)_(.+)_([a-z]+\d?)_(\d+)$')
SUITE_NAME = {'tt': 'TT', 'ob': 'OB', 'ss': 'SS'}


def rcaeval_cases():
    """Mọi ca RCAEval từ cây file Hugging Face (T-002, metadata công khai)."""
    src = 'results/T-002/public-metadata/run-002/hf-tree.json'
    tree = jload(src)
    files = collections.defaultdict(set)
    for it in tree:
        p = it['path']
        parts = p.split('/')
        if CASE_RE.match(parts[0]) and len(parts) == 2:
            files[parts[0]].add(parts[1])
        elif CASE_RE.match(parts[0]) and it['type'] == 'directory':
            files.setdefault(parts[0], set())
    out = []
    for case, fs in sorted(files.items()):
        m = CASE_RE.match(case)
        fam, sys_, root, fault, rep = m.groups()
        out.append(dict(dataset=f'{fam.upper()}-{SUITE_NAME[sys_]}', case=case, root=root, fault=fault,
                        rep=int(rep), trace='traces.parquet' in fs, log='logs.parquet' in fs,
                        metric='metrics.parquet' in fs, census_source=src))
    return out


def nezha_eadro():
    out = []
    for task, src, fam in [('T-008', 'results/T-008/runs/run-001/labels.json', 'Nezha'),
                           ('T-009', 'results/T-009/runs/run-001/labels.json', 'Eadro')]:
        lab = jload(src)
        rep = collections.Counter()
        for i, x in enumerate(lab):
            key = (x['dataset'], x['service'], x['fault'])
            rep[key] += 1
            ident = x.get('inject_time_raw') or x.get('start')
            out.append(dict(dataset=f"{fam}-{x['dataset']}", case=f"{x['dataset']}|{x['service']}|{x['fault']}|{ident}",
                            root=x["service"], fault=x["fault"], rep=rep[key], trace=None, log=None, metric=None,
                            census_source=f'{src}#{i}'))
    return out


def fse_bank():
    out = []
    src = 'results/T-012/runs/fse-file-inspect-003/census.json'
    c = jload(src)
    for x in c['root_sets']:
        out.append(dict(dataset='FSE-2026-TT', case=x['case'], root='+'.join(x['roots']), fault=str(x['fault_type']),
                        rep=1, trace=None, log=None, metric=None, census_source=src))
    src = 'results/T-012/runs/bank-label-reproduce-002/record.csv'
    rep = collections.Counter()
    for i, x in enumerate(rows(src)):
        key = (x.get('component') or x.get('root'), x.get('reason'))
        rep[key] += 1
        out.append(dict(dataset='OpenRCA-Bank', case=f'bank#{i}', root=key[0], fault=key[1], rep=rep[key],
                        trace=None, log=None, metric=None, census_source=f'{src}#{i}'))
    return out


def ran_cases():
    """Ca đã chạy phương pháp (TX2), đọc từ sổ chạy gốc. Trả {dataset: {case: nguồn}}."""
    tx2 = collections.defaultdict(dict)
    pat = re.compile(r're2(tt|ob)_[a-z0-9-]+?_[a-z]+_\d')
    for t in ['T-013', 'T-014', 'T-015', 'T-016', 'T-017', 'T-018']:
        src = f'results/{t}/ca-da-chay.csv'
        for i, x in enumerate(rows(src)):
            s = ' '.join(list(x.values())[:2])
            m = pat.search(s)
            if m:
                case = m.group(0)
                tx2['RE2-' + m.group(1).upper()].setdefault(case, f'{src}#row{i + 2}')
                continue
            m = re.search(r'torai-(OB|SS|TT)[\\/]([a-z0-9-]+?)_([a-z]+)[\\/](\d)', s)
            if m:
                sys_, root, fault, rep = m.groups()
                case = f're2{sys_.lower()}_{root}_{fault}_{rep}'
                tx2['RE2-' + sys_].setdefault(case, f'{src}#row{i + 2}')
    # T-019 sổ tiếp xúc SS/OB: ca công khai có kết quả RCA (T-006, T-007), danh tính đã xác lập
    src = 'results/T-019/so-ca-da-nhin.csv'
    for i, x in enumerate(rows(src)):
        if x['exposure'] == 'RCA_result' and x['public_case'] and x['identity'] != 'not-established':
            ds = {'RE1SS': 'RE1-SS', 'RE2SS': 'RE2-SS', 'RE2OB': 'RE2-OB'}[x['public_family']]
            tx2[ds].setdefault(x['public_case'], f'{src}#row{i + 2}')
    # T-006: main.py baro --dataset re1-ob chạy trên bản Zenodo của RE1-OB (125 ca)
    src = 'results/T-006/runs/kiem-chay-fse-baro-main-re1-ob.tar.gz'
    with tarfile.open(R(src)) as tf:
        for n in tf.getnames():
            m = re.search(r'output/results/([a-z0-9-]+?)_([a-z]+)_(\d)\.json$', n)
            if m:
                tx2['RE1-OB'].setdefault(f're1ob_{m.group(1)}_{m.group(2)}_{m.group(3)}', f'{src}!{n}')
    return tx2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    out_dir = R('results/T-021/runs', a.run)
    os.makedirs(out_dir, exist_ok=False)

    cases = rcaeval_cases() + nezha_eadro() + fse_bank()
    tx2 = ran_cases()
    t019 = {x['public_case']: i for i, x in enumerate(rows('results/T-019/so-ca-da-nhin.csv'))
            if x['exposure'] == 'telemetry_inspection_only'}
    t002_local = {x['case'] for x in jload('results/T-002/local-inspection/run-002/cases.json')}
    probe = {'Nezha': 'results/T-008/runs/trace-symptoms-002/result.json',
             'Eadro': 'results/T-009/runs/inspect-004/symptom-metrics.json'}
    for p in probe.values():
        assert os.path.exists(R(p)), p

    for c in cases:
        ds, case = c['dataset'], c['case']
        c['probe_trieu_chung'] = ''
        if case in tx2.get(ds, {}):
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX2', 'chay', tx2[ds][case]
        elif ds == 'RE2-TT':
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX1', 'v1', 'docs/MRP.md:120; docs/knowledge/K2-du-lieu.md:15-17'
        elif case in t019:
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX1', 'the', f'results/T-019/so-ca-da-nhin.csv#row{t019[case] + 2}'
        elif case in t002_local:
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX1', 'the', 'results/T-002/local-inspection/run-002/cases.json'
        elif ds.startswith(('Nezha', 'Eadro')):
            fam = ds.split('-')[0]
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX1', 'the', c['census_source']
            c['probe_trieu_chung'] = probe[fam]
        elif ds == 'FSE-2026-TT':
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX1', 'the', 'results/T-012/runs/fse-file-inspect-003/descriptive-bands.json'
        else:
            c['tx'], c['tx_nhom'], c['tx_nguon'] = 'TX0', '', 'không thấy nguồn tiếp xúc trong ba nhóm'

    # Mọi ca TX2 trong sổ chạy phải khớp một ca trong census
    known = {(c['dataset'], c['case']) for c in cases}
    missing = [(d, k) for d, m in tx2.items() for k in m if (d, k) not in known]
    assert not missing, missing[:5]

    fields = ['dataset', 'case', 'root', 'fault', 'rep', 'trace', 'log', 'metric', 'tx', 'tx_nhom', 'tx_nguon',
              'probe_trieu_chung', 'census_source']
    with open(os.path.join(out_dir, 'census-cases.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(cases)

    summ = {}
    for ds in sorted({c['dataset'] for c in cases}):
        cs = [c for c in cases if c['dataset'] == ds]
        cells = collections.Counter((c['root'], c['fault']) for c in cs)
        summ[ds] = dict(cases=len(cs), roots=len({c['root'] for c in cs}), cells=len(cells),
                        faults=dict(collections.Counter(c['fault'] for c in cs)),
                        rep_min=min(cells.values()), rep_max=max(cells.values()),
                        single_rep_cells=sum(1 for v in cells.values() if v == 1),
                        trace=sum(1 for c in cs if c['trace']), log=sum(1 for c in cs if c['log']),
                        metric=sum(1 for c in cs if c['metric']),
                        tx=dict(collections.Counter(c['tx'] for c in cs)),
                        probe=sum(1 for c in cs if c['probe_trieu_chung']))
    # Đối chiếu với sổ T-020 (chỉ đối chiếu, lệch thì ghi)
    t020 = collections.defaultdict(list)
    for x in rows('results/T-020/trung-gian/exposure_ledger/public-census.csv'):
        t020[x['dataset']].append(x)
    alias = {'Nezha-OB': 'Nezha-OB', 'Nezha-TT': 'Nezha-TT', 'Eadro-SN': 'Eadro-SN', 'Eadro-TT': 'Eadro-TT',
             'FSE-2026-TT': 'FSE-2026-propagation-TT', 'OpenRCA-Bank': 'OpenRCA-Bank'}
    cmp_rows = []
    for ds, s in summ.items():
        t = t020.get(alias.get(ds, ds), [])
        ttx = dict(collections.Counter(x['factual_seen'] for x in t))
        tcells = len({(x['root'], x['fault']) for x in t})
        cmp_rows.append(dict(dataset=ds, cases=s['cases'], t020_cases=len(t), cells=s['cells'], t020_cells=tcells,
                             tx=json.dumps(s['tx'], sort_keys=True), t020_tx=json.dumps(ttx, sort_keys=True),
                             lech='' if (s['cases'] == len(t) and s['cells'] == tcells and s['tx'] == ttx) else 'LỆCH'))
    with open(os.path.join(out_dir, 'doi-chieu-T020.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(cmp_rows[0]))
        w.writeheader()
        w.writerows(cmp_rows)
    with open(os.path.join(out_dir, 'census-summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summ, f, ensure_ascii=False, indent=1)
    for r_ in cmp_rows:
        print(r_)


if __name__ == '__main__':
    main()

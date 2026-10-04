"""T-019: inspect dataset identity and past run membership; never run RCA/detector.

Usage (existing pinned environment, single parquet reader):
  D:/RCA-ext/envs/py312/Scripts/python.exe results/T-019/lineage/check_lineage.py local
  ... check_lineage.py download  # only after parent has logged plan
  ... check_lineage.py compare --ss-root data/T-019
"""
import argparse
import collections
import csv
import hashlib
import json
import os
from pathlib import Path
import tarfile
import time
import urllib.request

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
LOCAL = Path('D:/RCA-ext/data')
OB = Path('D:/RCA-ext/work/T-019/lineage/re2ob')
REV = 'afeacb11bcc94dadfd1c8f483ee4377b2b8b614e'
SOURCES = ['fse-ss', 'torai-SS', 'RE1-SS', 'fse-ob', 'torai-OB']


def digest(p):
    sha = hashlib.sha256()
    git = hashlib.sha1(b'blob %d\0' % p.stat().st_size)
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            sha.update(b)
            git.update(b)
    return {'bytes': p.stat().st_size, 'sha256': sha.hexdigest(), 'git_oid': git.hexdigest()}


def put_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def put_csv(name, rows):
    if not rows:
        raise ValueError('empty output ' + name)
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def info_progress(s):
    with (OUT / 'progress.log').open('a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%dT%H:%M:%S') + ' ' + s + '\n')
    print(s, flush=True)


def runs():
    """Read archive members and meta only, no extraction or source writes."""
    selected = [
        ('T-006', 'fse-ss', REPO / 'results/T-006/runs/l4-baro-fse-ss-lan1.tar.gz'),
        ('T-006', 'fse-ob', REPO / 'results/T-006/runs/l4-baro-fse-ob-lan1.tar.gz'),
        ('T-006', 'torai-SS', REPO / 'results/T-006/runs/torai-torai-ss-lan1.tar.gz'),
        ('T-006', 'torai-OB', REPO / 'results/T-006/runs/torai-torai-ob-lan1.tar.gz'),
        ('T-007', 'RE2-OB', REPO / 'results/T-007/runs/py312-pin/microrank.tar.gz'),
        ('T-007', 'RE2-OB', REPO / 'results/T-007/runs/py312-pin/tracerca.tar.gz'),
    ]
    member_rows, manifest = [], []
    for task, source, p in selected:
        with tarfile.open(p) as t:
            members = [m for m in t.getmembers() if m.isfile() and '/results/' in m.name and m.name.endswith('.json')]
            # Validate every archived result parses and holds nonempty rank output.
            valid, empty = 0, 0
            for m in members:
                payload = json.load(t.extractfile(m))
                ranks = payload.get('0', payload.get('ranks'))
                if ranks:
                    valid += 1
                else:
                    empty += 1
                member_rows.append({'task': task, 'source': source, 'case': Path(m.name).stem,
                                    'archive': str(p), 'member': m.name, 'result_nonempty': bool(ranks)})
            meta = []
            for m in t.getmembers():
                if m.isfile() and m.name.endswith('/meta.json'):
                    meta.append(json.load(t.extractfile(m)))
            manifest.append({'task': task, 'source': source, 'archive': str(p), **digest(p),
                             'result_count': len(members), 'valid_nonempty': valid, 'empty': empty, 'meta': meta})
            info_progress('run inventory %s %s: %d results' % (task, source, len(members)))
    put_csv('run-members.csv', member_rows)
    put_json('run-manifest.json', manifest)
    # No direct RE1-SS run? Inspect every meta command of T006 archives as evidence,
    # while avoiding expensive decompression of data: archive size stays moderate.
    cmds = []
    for p in sorted((REPO / 'results/T-006/runs').glob('*.tar.gz')):
        with tarfile.open(p) as t:
            for m in t.getmembers():
                if m.isfile() and m.name.endswith('/meta.json'):
                    meta = json.load(t.extractfile(m))
                    cmds.append({'archive': str(p), 'member': m.name, 'cmd': meta.get('cmd'),
                                 'data_links': meta.get('lien_ket'), 'state': meta.get('trang_thai')})
    put_json('all-T006-run-commands.json', cmds)


def local():
    inventory, overlap = [], []
    for source in SOURCES:
        cases = sorted((LOCAL / source).glob('*/*/inject_time.txt'))
        for i, injection in enumerate(cases, 1):
            p = injection.parent
            label = p.parent.name + '_' + p.name
            inject = injection.read_text().strip()
            files = {x.name: digest(x) for x in sorted(p.iterdir()) if x.is_file() and
                     x.name in ['data.csv', 'simple_data.csv', 'simple_metrics.csv', 'logts.csv', 'tracets_err.csv', 'tracets_lat.csv', 'inject_time.txt']}
            inventory.append({'source': source, 'case': label, 'path': str(p), 'inject_time': inject,
                              'files': files, 'missing_metrics': not any(n in files for n in ['data.csv', 'simple_metrics.csv'])})
            if i % 25 == 0 or i == len(cases):
                info_progress('local %s %d/%d' % (source, i, len(cases)))
    a = {(r['source'], r['case']): r for r in inventory}
    for row in inventory:
        if row['source'] != 'fse-ss':
            continue
        r = a.get(('RE1-SS', row['case']))
        overlap.append({'source_a': 'fse-ss', 'case_a': row['case'], 'source_b': 'RE1-SS', 'case_b': row['case'],
                        'inject_equal': row['inject_time'] == r['inject_time'],
                        'raw_data_hash_equal': row['files']['data.csv']['sha256'] == r['files']['data.csv']['sha256'],
                        'simple_data_hash_equal': row['files']['simple_data.csv']['sha256'] == r['files']['simple_data.csv']['sha256']})
    put_json('local-file-manifest.json', inventory)
    put_csv('local-fse-RE1-SS-overlap.csv', overlap)
    runs()


def download():
    plan = json.loads((OUT / 'download-plan.json').read_text())
    rows, total = [], 0
    info_progress('download RE2-OB start expected=%d' % plan['expected_bytes'])
    for i, e in enumerate(plan['files'], 1):
        p = OB / e['path']
        p.parent.mkdir(parents=True, exist_ok=True)
        url = 'https://huggingface.co/datasets/phamquiluan/RCAEval/resolve/' + REV + '/' + e['path']
        t0 = time.monotonic()
        if p.exists():
            got = digest(p)
            method = 'reused'
        else:
            method = 'downloaded'
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'T019-lineage'}), timeout=120) as r, p.open('wb') as f:
                for b in iter(lambda: r.read(1024 * 1024), b''):
                    f.write(b)
                    total += len(b)
                    if total > 100_000_000:
                        raise ValueError('100MB lineage cap exceeded')
            got = digest(p)
        ok = got['bytes'] == e['size'] and (got['sha256'] == e['lfs']['oid'] if e.get('lfs') else got['git_oid'] == e['oid'])
        rows.append({'path': str(p), 'hf_path': e['path'], 'url': url, 'revision': REV,
                     'method': method, 'expected': e, 'actual': got, 'ok': ok, 'seconds': round(time.monotonic()-t0, 3)})
        put_json('download-manifest.json', {'network_bytes': total, 'files': rows})
        if not ok:
            raise ValueError('hash mismatch: ' + str(p))
        if i % 20 == 0 or i == len(plan['files']):
            info_progress('download RE2-OB %d/%d network=%d' % (i, len(plan['files']), total))


def compare_frames(pa, pb):
    import numpy as np
    import pandas as pd
    a = pd.read_csv(pa) if pa.suffix == '.csv' else pd.read_parquet(pa)
    b = pd.read_csv(pb) if pb.suffix == '.csv' else pd.read_parquet(pb)
    result = {'rows_a': len(a), 'rows_b': len(b), 'cols_a': len(a.columns), 'cols_b': len(b.columns),
              'column_set_equal': set(a.columns) == set(b.columns), 'time_vector_equal': False,
              'common_columns': len(set(a.columns) & set(b.columns)), 'value_columns_compared': 0,
              'value_columns_different': 0, 'nan_masks_different': 0, 'max_abs_diff': 0.0,
              'full_content_equal': False, 'common_content_equal': False, 'finite_time_content_equal': False}
    if 'time' not in a or 'time' not in b:
        result['error'] = 'time missing'
        return result
    for frame, key in [(a, 'a'), (b, 'b')]:
        finite = frame['time'].dropna()
        result['time_min_'+key] = float(finite.min())
        result['time_max_'+key] = float(finite.max())
    result['time_vector_equal'] = len(a) == len(b) and np.allclose(a['time'], b['time'], rtol=0, atol=0, equal_nan=True)
    for frame,key in [(a,'a'), (b,'b')]:
        result['rows_without_time_'+key] = int(frame['time'].isna().sum())
        result['non_time_nonnull_cells_in_missing_time_rows_'+key] = int(frame.loc[frame['time'].isna()].drop(columns=['time']).notna().to_numpy().sum())
    a = a.loc[a['time'].notna()].reset_index(drop=True)
    b = b.loc[b['time'].notna()].reset_index(drop=True)
    result['finite_time_vector_equal'] = len(a)==len(b) and np.allclose(a['time'],b['time'],rtol=0,atol=0,equal_nan=True)
    if not result['finite_time_vector_equal']:
        return result
    for c in sorted(set(a.columns) & set(b.columns) - {'time'}):
        va, vb = a[c].to_numpy(), b[c].to_numpy()
        result['value_columns_compared'] += 1
        if np.issubdtype(va.dtype, np.number) and np.issubdtype(vb.dtype, np.number):
            nan_a, nan_b = np.isnan(va), np.isnan(vb)
            if not np.array_equal(nan_a, nan_b):
                result['nan_masks_different'] += 1
            eq = np.allclose(va, vb, rtol=1e-12, atol=1e-12, equal_nan=True)
            delta = np.abs(va.astype(float)-vb.astype(float))
            finite = delta[np.isfinite(delta)]
            if finite.size:
                result['max_abs_diff'] = max(result['max_abs_diff'], float(finite.max()))
        else:
            eq = np.array_equal(va, vb)
        if not eq:
            result['value_columns_different'] += 1
    result['common_content_equal'] = result['value_columns_compared'] > 0 and result['value_columns_different'] == 0 and result['nan_masks_different'] == 0
    result['finite_time_content_equal'] = result['column_set_equal'] and result['common_content_equal']
    result['full_content_equal'] = result['time_vector_equal'] and result['finite_time_content_equal']
    return result


def compare(ss_root):
    import numpy as np
    import pandas as pd
    inventory = json.loads((OUT / 'local-file-manifest.json').read_text())
    # Source case IDs are different releases; first use exact injection bytes
    # (not merely names) to narrow candidates, then compare all metric values.
    public = []
    for family, root in [('re1ss', Path(ss_root)), ('re2ss', Path(ss_root)), ('re2ob', OB)]:
        for p in root.rglob('inject_time.txt'):
            if not p.parent.name.startswith(family + '_'):
                continue
            t = pd.read_parquet(p.parent/'metrics.parquet', columns=['time'])['time'].to_numpy(dtype='float64')
            public.append({'family': family, 'case': p.parent.name, 'path': p.parent,
                           'inject_time': p.read_text().strip(), 'inject_sha': digest(p)['sha256'],
                           'time_hash': hashlib.sha256(t.tobytes()).hexdigest(), 'time_rows': len(t),
                           'time_min': float(np.nanmin(t)), 'time_max': float(np.nanmax(t))})
    public_index = collections.defaultdict(list)
    for p in public:
        public_index[(p['family'], p['inject_time'])].append(p)
    time_index = collections.defaultdict(list)
    for p in public:
        time_index[(p['family'], p['time_hash'])].append(p)
    put_json('public-time-inventory.json', [{**p, 'path': str(p['path'])} for p in public])
    members = list(csv.DictReader((OUT / 'run-members.csv').open(encoding='utf-8')))
    run_index = {(r['source'], r['case']): r for r in members if r['task']=='T-006'}
    missing_run_evidence = []
    rows, details = [], []
    for i, local in enumerate(inventory, 1):
        source = local['source']
        families = ['re2ob'] if source.endswith('ob') or source.endswith('OB') else ['re1ss', 're2ss']
        pa = Path(local['path']) / ('simple_metrics.csv' if source.startswith('torai') else 'simple_data.csv')
        t = pd.read_csv(pa, usecols=['time'])['time'].to_numpy(dtype='float64')
        time_hash = hashlib.sha256(t.tobytes()).hexdigest()
        run = run_index.get((source, local['case']))
        if source=='RE1-SS':
            run = run_index.get(('fse-ss', local['case']))
            task_ran = 'T-006 via byte-identical fse-ss' if run else 'T-006 metadata census; T-019 metric inspection; no direct RCA run found'
        else:
            task_ran = 'T-006' if run else 'no selected run evidence'
            if not run:
                missing_run_evidence.append((source,local['case']))
        run_ref = run['archive']+'!'+run['member'] if run else 'T-006/runs/05d-so-re1-fse-ss.log; all-T006-run-commands.json'
        for family in families:
            injection_candidates = public_index.get((family, local['inject_time']), [])
            time_candidates = time_index.get((family, time_hash), [])
            candidates = {p['case']:p for p in injection_candidates+time_candidates}.values()
            windows = [p for p in public if p['family']==family and p['time_min'] <= float(np.nanmax(t)) and float(np.nanmin(t)) <= p['time_max']]
            if not candidates:
                rows.append({'case': local['case'], 'source': source, 'public_family': family.upper(),
                             'public_case': '', 'task_ran': task_ran,
                             'evidence': 'no-identical-injection/time-vector candidate; %d overlapping public metric windows' % len(windows),
                             'identity': 'not-established', 'inject_time': local['inject_time'],
                             'comparison_ref': 'public-time-inventory.json', 'metric_input': str(pa), 'run_ref': run_ref})
            for p in candidates:
                pb = p['path'] / 'metrics.parquet'
                detail = {'source': source, 'local_case': local['case'], 'public_family': family,
                          'public_case': p['case'], 'local_metric': str(pa), 'public_metric': str(pb),
                          'inject_value_equal': local['inject_time']==p['inject_time'], 'inject_byte_sha_equal': local['files']['inject_time.txt']['sha256'] == p['inject_sha'],
                          **compare_frames(pa, pb)}
                details.append(detail)
                identity = 'metric-content-equal-to-tolerance' if detail['full_content_equal'] else 'metric-content-equal-after-omitting-missing-time-rows' if detail['finite_time_content_equal'] else 'partial-metric-content-equal-to-tolerance' if detail['common_content_equal'] else 'same-injection-or-time-only'
                rows.append({'case': local['case'], 'source': source, 'public_family': family.upper(),
                             'public_case': p['case'], 'task_ran': task_ran,
                             'evidence': identity, 'identity': identity, 'inject_time': local['inject_time'],
                             'comparison_ref': 'public-metric-comparisons.json#%d' % (len(details)-1), 'metric_input': str(pa), 'run_ref': run_ref})
        if i % 25 == 0 or i == len(inventory):
            info_progress('public compare %d/%d details=%d' % (i, len(inventory), len(details)))
    # Public RE2-OB directly used by T007, evidenced by parsed archive members.
    names = {r['case'] for r in members if r['task'] == 'T-007' and r['source'] == 'RE2-OB'}
    for p in public:
        if p['family'] == 're2ob':
            short = p['case'].removeprefix('re2ob_')
            rows.append({'case': p['case'], 'source': 'HF RE2-OB', 'public_family': 'RE2OB', 'public_case': p['case'],
                         'task_ran': 'T-007' if short in names else '', 'evidence': 'archived MicroRank/TraceRCA result member' if short in names else 'no output member',
                         'identity': 'direct-run', 'inject_time': p['inject_time'], 'comparison_ref': 'run-members.csv', 'metric_input': str(p['path']/'metrics.parquet'), 'run_ref': 'run-members.csv'})
    put_json('public-metric-comparisons.json', details)
    put_csv('so-ca-da-nhin.csv', rows)
    put_json('summary.json', {'local_source_counts': dict(collections.Counter(r['source'] for r in inventory)),
                             'public_counts': dict(collections.Counter(p['family'] for p in public)),
                             'evidence_counts': dict(collections.Counter((r['source']+' -> '+r['public_family']+' '+r['identity']) for r in rows)),
                             'injection_collisions': {family+':'+inj:[p['case'] for p in ps] for (family, inj),ps in public_index.items() if len(ps)>1},
                             'total_ledger_rows': len(rows), 'comparison_count': len(details),
                             'T007_result_cases': len(names), 'missing_run_evidence': missing_run_evidence,
                             'numeric_equality_tolerance': {'rtol':1e-12,'atol':1e-12},
                             'no_candidate_coverage': 'all public family injection values and complete time vectors; window intersection additionally counted'})


def verify():
    import numpy as np
    import pandas as pd
    import pyarrow as pa
    local = json.loads((OUT/'local-file-manifest.json').read_text())
    files = []
    for i,row in enumerate(local,1):
        for name, expected in row['files'].items():
            p = Path(row['path'])/name
            actual = digest(p)
            files.append({'path':str(p),'baseline':expected,'final':actual,'unchanged':actual==expected})
        if i%100==0 or i==len(local):
            info_progress('verify local source unchanged %d/%d' % (i,len(local)))
    for row in json.loads((OUT/'run-manifest.json').read_text()):
        p=Path(row['archive'])
        actual=digest(p)
        expected={k:row[k] for k in ['bytes','sha256','git_oid']}
        files.append({'path':str(p),'baseline':expected,'final':actual,'unchanged':actual==expected})
    downloads=json.loads((OUT/'download-manifest.json').read_text())
    outside=[]
    for row in downloads['files']:
        actual=digest(Path(row['path']))
        outside.append({'path':row['path'],'bytes':actual['bytes'],'sha256':actual['sha256'],
                        'git_oid':actual['git_oid'],'unchanged_after_download':actual==row['actual']})
    put_json('source-file-integrity.json', {'files':files,'all_unchanged':all(x['unchanged'] for x in files),
                                         'outside_downloads_still_match':all(x['unchanged_after_download'] for x in outside)})
    put_csv('outside-files.csv',outside)
    ledger=list(csv.DictReader((OUT/'so-ca-da-nhin.csv').open(encoding='utf-8')))
    summary=json.loads((OUT/'summary.json').read_text())
    checks={'local_case_count':len(local)==505,'public_family_counts':summary['public_counts']=={'re1ss':125,'re2ss':90,'re2ob':90},
            'ledger_rows':len(ledger)==910,'ledger_unique_keys':len(ledger)==len({(x['source'],x['case'],x['public_family'],x['public_case']) for x in ledger}),
            'all_selected_direct_runs_have_evidence':not summary['missing_run_evidence'],
            'T007_all90cases':summary['T007_result_cases']==90,
            'all_download_files_hash_match':len(downloads['files'])==180 and all(x['ok'] for x in downloads['files']),
            'exact_download_size':downloads['network_bytes']==14_215_893,
            'all_inspected_sources_unchanged':all(x['unchanged'] for x in files),
            'outside_downloads_unchanged':all(x['unchanged_after_download'] for x in outside)}
    put_json('verification.json',{'checks':checks,'all_pass':all(checks.values()),
                                  'runtime':{'python':__import__('sys').version,'executable':__import__('sys').executable,
                                             'pandas':pd.__version__,'numpy':np.__version__,'pyarrow':pa.__version__}})
    assert all(checks.values()), checks


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['local','download','compare','verify'])
    ap.add_argument('--ss-root', default='data/T-019')
    args = ap.parse_args()
    if args.mode == 'local':
        local()
    elif args.mode == 'download':
        download()
    elif args.mode=='compare':
        compare(args.ss_root)
    else:
        verify()

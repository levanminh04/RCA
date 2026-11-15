"""T-042: verify only explicitly referenced sources; never run a method."""
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-042'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def verify():
    checks = []

    def check(path, expected, manifest, role):
        p = Path(path)
        if not p.is_absolute():
            p = ROOT / p
        actual = sha(p) if p.is_file() else None
        row = dict(path=str(p), expected_sha256=expected, actual_sha256=actual,
                   manifest=str(manifest), role=role, match=actual == expected)
        checks.append(row)
        if not row['match']:
            raise RuntimeError('SOURCE_MISMATCH ' + str(p))

    fm = 'results/T-026/ban-ghi-dua-vao-cham.json'
    hm = 'results/T-026/runs/session-005/handoff-manifest.json'
    handoff = read(ROOT / hm)
    for p in [fm, 'results/T-026/cham-a.json']:
        check(p, handoff['files'][p]['sha256'], hm, 'frozen_evaluation')
    frozen = read(ROOT / fm)
    for p, expected in frozen['source_hashes'].items():
        if p.startswith(('src/p3/', 'src/microrank/', 'src/simplerca/')) or p in [
            'results/T-026/allowlist-dev.json', 'results/T-026/nhan-dev.json',
            'results/T-026/mappings/ob.json', 'results/T-026/config/adapter-config.json',
            'results/T-026/kiem-dau-vao.md',
            'results/T-026/runs/session-005/external-code-manifest.json',
            'results/T-026/runs/session-005/published-reference.json']:
            check(p, expected, fm, 'code_or_input_contract')
    extm = 'results/T-026/runs/session-005/external-code-manifest.json'
    ext = read(ROOT / extm)
    for p, expected in ext['external_source_hashes'].items():
        check(p, expected, extm, 'external_code')
    records = {x['path']: x for table in frozen['tables'].values()
               if isinstance(table, dict) for x in table.get('records', [])}
    for p, row in records.items():
        check(p, row['sha256'], fm, 'frozen_dev_record')
    am = 'results/T-026/allowlist-dev.json'
    allow = read(ROOT / am)
    assert len(allow['cases']) == 22
    sources = {p: x for c in allow['cases'] for p, x in c['files'].items()}
    for p, row in sources.items():
        check(p, row['sha256'], am, 'allowlisted_dev_source_hash_only')
    nm = 'results/T-008/runs/run-001/manifest.json'
    nezha = read(ROOT / nm)
    for row in nezha['sources']:
        check('results/T-008/' + row['path'], row['sha256'], nm, 'Nezha_primary_source')
    gm = 'results/T-034/runs/manifest-cuoi-007/manifest.json'
    g = read(ROOT / gm)
    for row in g['files']:
        if row['path'] in ['results/T-034/ban-do-g2.json', 'results/T-034/bang-baseline.json',
                           'results/T-034/goi-g2.md', 'results/T-034/hai-phep-kiem.json']:
            check(row['path'], row['sha256'], gm, 'G2')
    bm = 'results/T-034/ban-do-g2.json'
    for p, expected in read(ROOT / bm)['sources'].items():
        if p.startswith(('results/T-032/runs/microrank', 'results/T-032/runs/simplerca',
                         'results/T-032/runs/root-signal', 'results/T-032/runs/trace-root',
                         'results/T-032/runs/bo-sung-toan-dien', 'results/T-032/kha-nang',
                         'results/T-034/')):
            check(p, expected, bm, 'reused_intermediate')
    sm = 'results/T-017/sources/download-manifest.json'
    snapshots = read(ROOT / sm)
    bases = [ROOT / 'results/T-017/sources', Path('D:/RCA-ext/work/T-017/sources-audit')]
    for row in snapshots:
        if row['file'].startswith(('tree-', 'github/')) or row['file'] == 'fang2026rethinking-fse.pdf':
            candidates = [p / row['file'] for p in bases if (p / row['file']).is_file()]
            if not candidates:
                raise FileNotFoundError(row['file'])
            check(candidates[0], row['sha256'], sm, 'SimpleRCA_primary_source')
    invm = 'results/T-017/inventory-files.csv'
    wanted = ['doi-chieu-code.md', 'so-cong-bo.csv', 'type-i-ii.md', 'fse26-pages.txt',
              'pdf-manifest.json', 'fse-new-artifact-code-comparison.json']
    with (ROOT / invm).open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            if Path(row['absolute_path']).name in wanted:
                check(row['absolute_path'], row['sha256'], invm, 'SimpleRCA_document')
    pm = 'src/microrank/PROVENANCE.json'
    provenance = read(ROOT / pm)
    check('src/microrank/official.py', provenance['sha256'], pm, 'extracted_official_functions')
    result = dict(schema='T042-sources-v1', created_utc=datetime.now(timezone.utc).isoformat(),
                  checks=checks, all_match=True,
                  scope=dict(dev_cases=22, unique_dev_files=len(sources),
                             unique_dev_bytes=sum(x['bytes'] for x in sources.values()),
                             frozen_records=len(records), test_opened=False, downloads=0),
                  revisions=dict(Nezha=nezha['revision'], MicroRank=provenance['revision'],
                                 RCAEval=ext['rcaeval_revision'], BARO=ext['baro_revision']),
                  licenses=dict(Nezha='MIT code; data use Q-59', MicroRank='MIT extracted code',
                                RCAEval='MIT', BARO='MIT', SimpleRCA_upstream='OPEN: no LICENSE/COPYING in three pinned trees'),
                  unavailable=[dict(path=x['source'], exists=Path(x['source']).is_file(),
                                    effect='whole upstream preprocessing not reverified; extracted functions remain hash-valid')
                               for x in provenance['functions']],
                  environment=dict(python=sys.version, executable=sys.executable,
                                   packages={x: importlib.metadata.version(x) for x in ['numpy', 'pandas', 'psutil']}),
                  source_manifest_hashes={p: sha(ROOT / p) for p in [hm, fm, extm, nm, gm, bm, sm, invm, pm]})
    write(OUT / 'nguon.json', result)
    plan = dict(schema='T042-plan-v1', frozen_before_method=True, dev_ids=sorted(c['opaque_id'] for c in allow['cases']),
                branches={s: dict(metric_rule=rule, metric_aggregation=agg) for s, rule, agg in [
                    ('S0', 'sigma', 'events'), ('S1', 'sigma', 'channels'), ('S2', 'p95', 'events'), ('S3', 'p95', 'channels')]},
                fixed=dict(sigma=3, ddof=0, quantile=0.95, quantile_method='linear', trace_factor=3,
                           log_threshold=0, keywords=['ERROR', 'FAIL', 'EXCEPTION'], trace_guard_s=0,
                           view='main', window_s=300, duplicates='retain', filling='none', scoring='P3 exact ties'),
                predictions=dict(threshold='P95 can change the per-channel count while all other inputs stay fixed',
                                 aggregation='channels replaces each positive count by one, changing relative metric/modal weight',
                                 alternative='neither change need repair errors; true positives can be lost',
                                 interaction='S3 identifies combined sensitivity, not the author program'),
                reuse=dict(frozen_baseline=fm, previous_channels='results/T-032/runs/simplerca-s1-001/summary.json',
                           policy='reuse full valid intermediates if available; replay S0 only for missing thresholds/counts',
                           microrank='read saved interventions only; do not rerun'),
                budget=dict(max_case_branches=88, estimated_machine_minutes=[20,60], max_single_run_s=3600,
                            expected_rss_mb=2000, expected_output_mb=300, downloads=0),
                dependencies=['verified sources', 'WHY-54 written', 'fixtures', 'independent window audit',
                              'unlabeled pilot cost', 'serialize diagnoses and list', 'join dev labels', 'P3 and independent evaluator'])
    write(OUT / 'ke-hoach-chay.json', plan)
    print(json.dumps(dict(status='PASS', checks=len(checks), dev_sources=len(sources), records=len(records))))


if __name__ == '__main__':
    verify()

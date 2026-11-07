"""Package only the approved DEV routes, pinned references and current code."""
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
OUT = ROOT / 'results/T-054'
sys.path[:0] = [str(OUT / 'scripts'), str(ROOT / 'src')]
from bien_nhan import digest, fingerprint, read_pin, ref, atomic
from nguon import original_dev_sources, compare_sources
from pilot import reference


def main():
    manifest = json.loads((OUT / 'manifest-chuan-bi-main-006.json').read_bytes())['outputs']
    def pinned(relative):
        return read_pin(dict(manifest[relative], path=relative))
    prior = pinned('results/T-054/runs/trien-khai-003/pilot-local-007/plan.json')
    ceplan = pinned('results/T-054/runs/trien-khai-004/pilot-2-worker-001/plan.json')
    original = pinned('results/T-054/runs/trien-khai-005/dev-metadata.json')
    candidates = pinned('results/T-054/runs/trien-khai-003/before-files/pilot-plan.json')['candidates']
    p52 = json.loads((ROOT / 'results/T-052/manifest-dinh-chinh-g3-004.json').read_bytes())['outputs']
    baselines = read_pin(dict(p52['results/T-052/ket-qua-dev-doc-lap-001.json'],
                             path='results/T-052/ket-qua-dev-doc-lap-001.json'))['baseline_native_checks']
    configs = json.loads((ROOT / 'results/T-052/giao-thuc-p7-a-003.json').read_bytes())['configurations']
    refs = {}
    jobs = []
    native = next(c for c in candidates if c['opaque_id'] == 'dev-a915aa2424' and c['window'] == 'that')
    config_ids = {'C-a0': 'K-R0', 'C-a1': 'K-E1', 'bo-E1': 'K-E2+E5',
                  'bo-E2': 'K-E1+E5', 'bo-E5': 'K-E1+E2'}
    for arm in ('C-a0', 'C-a1', 'bo-E1', 'bo-E2', 'bo-E5', 'T12-on'):
        job = copy.deepcopy(next(j for j in prior['jobs'] if j['slot']['dataset'] == 'RE2-TT' and j['slot']['arm'] == arm))
        job.update(source=original['job']['source'], t=original['job']['t'])
        for key in ('opaque_id', 'member_sha256', 'source_sha256', 'window'):
            job['slot'][key] = original['job']['slot'][key]
        source = original['source']
        if arm == 'T12-on':
            m51 = json.loads((ROOT / 'results/T-051/manifest.json').read_bytes())['outputs']
            path = 'results/T-051/t12-001/05.json'
            expected = read_pin(dict(m51[path], path=path))
            fields = dict(world_blocks={w: expected['worlds'][w]['rank'][1]['blocks'] for w in ('P', 'S_lo', 'S_hi')},
                          P_tiers=expected['worlds']['P']['rank'][1]['tang'], P_region=expected['worlds']['P']['region'][1],
                          edges=sorted(set(map(tuple, expected['edges'])) | set(map(tuple, expected['static']['added']))))
            refs[arm] = dict(kind='T12', fields=fields, origin=dict(m51[path], path=path))
        else:
            refs[arm] = dict(kind='M1', record=reference(native['native_record'], config_ids[arm]),
                             origin=native['native_record'], control=arm in ('C-a0', 'C-a1'))
        jobs.append(dict(job=job, independent=source, reference_key=arm))
    for arm, seed in [('baro', None), ('simplerca', None), ('tracerca', None),
                      ('torai_B', 0), ('torai_B', 1), ('torai_B', 2)]:
        job = copy.deepcopy(next(j for j in prior['jobs'] if j['slot']['dataset'] == 'RE2-TT'
                                 and j['slot']['arm'] == arm and j['slot']['seed'] == seed))
        job.update(source=original['job']['source'], t=original['job']['t'])
        for key in ('opaque_id', 'member_sha256', 'source_sha256', 'window'):
            job['slot'][key] = original['job']['slot'][key]
        matching = [p for p in baselines if p['opaque_id'] == 'dev-a915aa2424' and p['method'] == arm
                    and read_pin(p).get('seed') == seed]
        assert len(matching) == 1
        key = arm + '-' + str(seed)
        refs[key] = dict(kind='baseline', record=read_pin(matching[0]), origin=matching[0])
        jobs.append(dict(job=job, independent=original['source'], reference_key=key))
    ce = copy.deepcopy(next(j for j in ceplan['jobs'] if j['slot']['dataset'] == 'RE2-TT'))
    ce_source = original_dev_sources(read_pin(ce['independent_source_ref']))
    ce_native = next(c for c in candidates if c['opaque_id'] == ce['slot']['opaque_id'] and c['window'] == 'ce')
    refs['C-e'] = dict(kind='M1', record=reference(ce_native['native_record'], 'K-E1+E2+E5'), origin=ce_native['native_record'])
    jobs.append(dict(job=ce, independent=ce_source, reference_key='C-e'))
    error = copy.deepcopy(next(j for j in prior['jobs'] if j['slot']['dataset'] == 'RE2-TT' and j['slot']['arm'] == 'tracerca'))
    error_source = original_dev_sources(read_pin(error['independent_source_ref']))
    proposal = pinned('results/T-054/runs/trien-khai-002/pilot-proposal.json')['baseline_jobs']
    errref = next(p['source_ref'] for p in proposal if all(p[k] == error['slot'][k]
                      for k in ('dataset', 'opaque_id', 'arm', 'seed')))
    refs['tracerca-error'] = dict(kind='baseline', record=read_pin(errref), origin=errref)
    jobs.append(dict(job=error, independent=error_source, reference_key='tracerca-error'))
    pins = {}
    sources = {}
    code = json.loads((OUT / 'runs/hoan-thien-local-g3-011/current-code-pins.json').read_bytes())['code_pins']
    for rel, old_sha in code.items():
        if rel.startswith(('src/', 'results/T-052/scripts/', 'results/T-054/scripts/')):
            if rel not in {f'results/T-054/scripts/{n}.py' for n in ('p7', 'nguon', 'dieu_phoi', 'cham', 'fixtures')}:
                assert digest(ROOT / rel) == old_sha, rel
            sources[rel] = ROOT / rel
    for row in jobs:
        job = row['job']
        runtime = dict(dataset='RE2-TT', inventory=job['inventory'], g1_revision=job['g1_revision'],
                       cases={job['slot']['opaque_id']: job['source']})
        independent = copy.deepcopy(row['independent'])
        independent['cases_by_member'] = {job['slot']['member_sha256']: independent['cases_by_member'][job['slot']['member_sha256']]}
        compare_sources(runtime, independent, 'RE2-TT', job['g1_revision'])
        row['independent'] = independent
        for meta in job['source']['files'].values():
            assert meta['path'].startswith('data/rcaeval/')
            path = ROOT / meta['path']
            assert path.stat().st_size == meta['bytes'] and digest(path) == meta['sha256']
            sources[meta['path']] = path
    for rel in ('results/T-043/hop-dong.json', 'results/T-038/do-thi/thuc-the.json', 'results/T-039/do-thi/thuc-the.json',
                'results/T-043/fixture-dac-ta.json', 'results/T-043/fixture/fixture-bo-sung.json',
                'results/T-044/fixture/dap-an-u-h.json', 'results/T-044/tests/test_adapter.py',
                'results/T-044/tests/conftest.py', 'results/T-044/tests/sinh_trace_S.py'):
        sources[rel] = ROOT / rel
    upstream = Path('D:/RCA-ext/src/RCAEval')
    revision = subprocess.check_output(['git', '-C', str(upstream), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == '259ea4167160256a74ad30004aa3d96a998c846e'
    subprocess.run(['git', '-C', str(upstream), 'diff', '--quiet', 'HEAD'], check=True)
    tracked = subprocess.check_output(['git', '-C', str(upstream), 'ls-files', 'RCAEval'], text=True).splitlines()
    for rel in tracked:
        if rel.endswith('.py'):
            sources['upstream/RCAEval/' + rel] = upstream / rel
    sources['results/T-054/runs/chuan-bi-main-013/remote_dev.py'] = RUN / 'remote_dev.py'
    metadata = dict(jobs=jobs, references=refs, error_audit=pinned('results/T-054/runs/trien-khai-003/operation-error-audit.json'),
                    upstream_revision=revision, preparation_permission=json.loads((RUN / 'preparation-permission.json').read_bytes()))
    blobs = {'dev-metadata.json': json.dumps(metadata, ensure_ascii=False).encode('utf-8')}
    pins = {rel: dict(bytes=path.stat().st_size, sha256=digest(path)) for rel, path in sources.items()}
    archive = RUN / 'dev-package.tar.gz'
    with tarfile.open(archive, 'x:gz') as tar:
        for rel, path in sorted(sources.items()):
            tar.add(path, arcname=rel, recursive=False)
        blobs['files.json'] = json.dumps(pins, sort_keys=True).encode('utf-8')
        for rel, data in blobs.items():
            item = tarfile.TarInfo(rel); item.size = len(data)
            tar.addfile(item, io.BytesIO(data))
    atomic(RUN / 'dev-package.json', dict(archive=ref(archive), files=pins, jobs=len(jobs),
           raw_scope='two approved TT DEV cases only', test_transferred=False, upstream_revision=revision))
    print(json.dumps(dict(jobs=len(jobs), files=len(pins), archive_bytes=archive.stat().st_size)))


if __name__ == '__main__':
    main()

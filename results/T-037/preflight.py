"""Read-only input audit; all outputs stay inside results/T-037/runs/."""
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import re
import subprocess
import sys
import time

ROOT = pathlib.Path('D:/RCA-flashticket')
PLATFORM = pathlib.Path('D:/Project/flash-ticket-platform')
RUN = ROOT / 'results/T-037/runs/tu-ra-001'

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args]).decode('utf-8', errors='replace')

def audit_manifest(path):
    m = json.loads(path.read_text(encoding='utf-8-sig'))
    checked = []
    errors = []
    entries = m.get('files', m.get('artifacts', []))
    if isinstance(entries, dict):
        raise ValueError('Unexpected manifest mapping; do not guess schema')
    for e in entries:
        p = (ROOT / e['path']).resolve()
        if not p.is_relative_to(ROOT) or p.is_relative_to(ROOT / 'data'):
            raise ValueError('Forbidden manifest entry: ' + str(p))
        actual = {'path': e['path'], 'exists': p.is_file()}
        if p.is_file():
            actual.update(bytes=p.stat().st_size, sha256=sha(p))
        actual['ok'] = actual.get('sha256') == e['sha256'] and actual.get('bytes') == e['bytes']
        checked.append(actual)
        if not actual['ok']:
            errors.append(actual)
    return {'manifest': str(path), 'manifest_sha256': sha(path), 'checked_count': len(checked),
            'total_bytes': sum(e.get('bytes', 0) for e in checked), 'errors': errors, 'files': checked}

def main():
    RUN.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    for name, p in [('log-before.md', ROOT/'tasks/T-037-p5b-flashticket/LOG.md'), ('state-before.md', ROOT/'docs/STATE.md')]:
        (RUN/name).write_bytes(p.read_bytes())
    (RUN/'tracked-before.diff').write_text(git(ROOT, 'diff', 'HEAD', '--binary'), encoding='utf-8')
    (RUN/'status-before.txt').write_text(git(ROOT, 'status', '--porcelain=v1', '--untracked-files=all'), encoding='utf-8')
    result = {'task': 'T-037', 'client_date': '2026-10-15',
              'recorded_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'device': platform.node(), 'platform': platform.platform(),
              'python': sys.version, 'executable': sys.executable,
              'command': 'py -3 -X utf8 -B results/T-037/preflight.py',
              'intent': 'EXECUTE_CONDITIONAL_SELF_AUDIT', 'official_reviewer': 'Claude',
              'benchmark': False, 'reason_not_benchmark': 'Concurrent read-only source collection; no performance claim',
              'rca_head': git(ROOT, 'rev-parse', 'HEAD').strip(),
              'platform_head': git(PLATFORM, 'rev-parse', 'HEAD').strip(),
              'platform_status': git(PLATFORM, 'status', '--porcelain=v1', '--untracked-files=all'),
              'manifests': [audit_manifest(ROOT/'results/T-036/manifest.json'), audit_manifest(ROOT/'results/T-035/manifest.json')]}
    m = json.loads((ROOT/'results/T-036/manifest.json').read_text(encoding='utf-8-sig'))
    result['pin'] = {k: m.get(k) for k in ('created_utc', 'current_run', 'schema_version')}
    result['pin']['matches_spec'] = m['created_utc'] == '2026-10-15T13:45:08.305188+00:00' and m['current_run'] == 'runs/kiem-r1-after-002'
    hashes = json.loads((ROOT/'results/T-036/runs/kiem-r1-after-002/code-hashes.json').read_text(encoding='utf-8-sig'))
    result['code_hashes_raw'] = hashes
    result['current_code'] = []
    for p in sorted((ROOT/'results/T-036/runs/kiem-r1-after-002/code').glob('*.py')):
        current = ROOT/('results/T-036/check.py' if p.name == 'check.py' else 'src/do_thi_tinh/'+p.name)
        result['current_code'].append({'snapshot': str(p), 'current': str(current), 'sha256': sha(p), 'current_sha256': sha(current), 'matches': sha(p)==sha(current)})
    selected = ['AGENTS.md', '.agents/skills/govern-capstone-work/SKILL.md',
                '.agents/skills/govern-capstone-work/references/project-authority-and-gates.md',
                'docs/evidence/project-direction/2026-09-18-de-tai-va-nhiem-vu.md', 'docs/project/roles.md',
                'docs/architecture/B11-C-target-architecture.md', 'docs/architecture/B12-data-ownership-and-schema.md',
                'docs/architecture/B13-api-and-event-contracts.md', 'docs/architecture/B14-main-flow-sequences.md',
                'docs/architecture/B16-observability-baseline.md']
    result['platform_sources'] = []
    for rel in selected:
        p = PLATFORM/rel
        txt = p.read_text(encoding='utf-8-sig')
        result['platform_sources'].append({'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size,
            'lines': len(txt.splitlines()), 'headings': [{'line': i, 'text': line} for i, line in enumerate(txt.splitlines(),1) if line.startswith('#')],
            'dirty': git(PLATFORM, 'status', '--porcelain=v1', '--', rel).strip(),
            'last_commit': git(PLATFORM, 'log', '-1', '--format=%H', '--', rel).strip()})
    result['governing_rca'] = []
    for rel in ['AGENTS.md','docs/STATE.md','docs/MRP.md','docs/WHY.md','docs/DECISIONS.md','docs/LESSONS.md',
                'docs/review-prompt.md','docs/reference/sources/DT18-de-tai-va-nhiem-vu.md',
                'docs/reference/sources/advisor-2026-09-23.md','tasks/T-037-p5b-flashticket/SPEC.md',
                'tasks/T-037-p5b-flashticket/LOG.md','tasks/T-036-p5b-hop-dong-chung/LOG.md']:
        p = ROOT/rel
        result['governing_rca'].append({'path': rel, 'bytes':p.stat().st_size, 'sha256':sha(p)})
    result['elapsed_seconds_non_benchmark'] = time.perf_counter()-started
    result['all_checks_pass'] = result['pin']['matches_spec'] and all(not x['errors'] for x in result['manifests']) and all(x['matches'] for x in result['current_code'])
    (RUN/'preflight.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'all_checks_pass':result['all_checks_pass'], 'device':result['device'],
          'pin':result['pin'], 'manifests':[{k:v for k,v in x.items() if k!='files'} for x in result['manifests']],
          'sources':[{k:v for k,v in x.items() if k not in ('headings','sha256','last_commit')} for x in result['platform_sources']]}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except BaseException:
        import traceback
        RUN.mkdir(parents=True, exist_ok=True)
        (RUN/'failure.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise

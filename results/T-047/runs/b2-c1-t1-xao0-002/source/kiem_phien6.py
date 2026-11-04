"""Kiểm phạm vi và manifest tại mốc bàn giao Q-233, không chấm phương pháp."""
import argparse
import ast
import hashlib
import json
import subprocess
import time
import xml.etree.ElementTree as ET

import psutil
import adapter_t047 as ad
import tep_pha1


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def text(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--status', required=True)
    ap.add_argument('--scoring-read', action='store_true')
    a = ap.parse_args()
    root, out = ad.ROOT, ad.OUT
    audit = ad.duong_ra(a.run)
    audit.mkdir(parents=True, exist_ok=False)
    before = out / 'runs/c1-ap-dung-001/before'
    receipt = json.loads((out / 'runs/c1-ap-dung-001/commit.json').read_text(encoding='utf-8'))
    applied = json.loads((out / 'runs/c1-ap-dung-001/ap-dung.json').read_text(encoding='utf-8'))
    git = lambda *args: subprocess.check_output(['git', *args], cwd=root)
    commit = git('rev-parse', 'HEAD').decode().strip()
    checks = {
        'WHY_unchanged': (root / 'docs/WHY.md').read_bytes() == (before / 'docs/WHY.md').read_bytes(),
        'SPEC_unchanged': (root / 'tasks/T-047-khoi-k-luot-2/SPEC.md').read_bytes() ==
                          (before / 'tasks/T-047-khoi-k-luot-2/SPEC.md').read_bytes(),
        'LOG_append_only': (root / 'tasks/T-047-khoi-k-luot-2/LOG.md').read_bytes().startswith(
                          (before / 'tasks/T-047-khoi-k-luot-2/LOG.md').read_bytes()),
        'DECISIONS_only_Q233_added': text(root / 'docs/DECISIONS.md') == text(before / 'docs/DECISIONS.md') +
                                   '\n' + text(out / 'runs/c1-ap-dung-001/Q-233-row.txt'),
        'source_C1_exact_hash': sha(root / 'src/m1/cong.py') == applied['source_after_sha256'],
        'source_unchanged_since_C1_commit': not git('diff', commit, '--', 'src'),
        'one_authorized_commit': commit == '6d9744ab0147dd526a0979ddcc7cc035f091d35d',
        'commit_only_source_and_Q233': set(git('show', '--format=', '--name-only', commit).decode().split()) ==
                                      {'src/m1/cong.py', 'docs/DECISIONS.md'},
    }
    old_state = (before / 'docs/STATE.md').read_bytes().splitlines()
    new_state = (root / 'docs/STATE.md').read_bytes().splitlines()
    delta = [(b, c) for b, c in zip(old_state, new_state) if b != c]
    checks['STATE_only_T047'] = len(old_state) == len(new_state) and len(delta) == 1 and all(
        b.startswith(b'- **T-047 ') and c.startswith(b'- **T-047 ') for b, c in delta)
    for p in (out / 'scripts').glob('*.py'):
        ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
    checks['scripts_syntax'] = True
    phases = {}
    log_text = text(root / 'tasks/T-047-khoi-k-luot-2/LOG.md')
    for p in sorted((out / 'runs').glob('b*-c1-*')):
        if (p / 'pha1.json').is_file() and (p.name.startswith('b2-c1-t1-') or p.name.startswith('b3-k-c1-')):
            m = tep_pha1.kiem(p)
            phases[p.relative_to(root).as_posix()] = m
    checks['completed_phase_hashes_in_LOG'] = all(
        f"- `{name}`: `{m['sha256']}`" in log_text for name, m in phases.items())
    tests = {}
    for name, n in [('c1-T-044-001', 374), ('c1-T-045-001', 16), ('c1-T-046-001', 46),
                    ('c1-hoi-quy-001', 155), ('c1-giai-thich-test-001', 5),
                    ('c1-guard-hoi-quy-002', 171)]:
        suites = list(ET.parse(out / 'runs' / name / 'junit.xml').getroot().iter('testsuite'))
        tests[name] = dict(tests=sum(int(x.get('tests', 0)) for x in suites),
                           failures=sum(int(x.get('failures', 0)) + int(x.get('errors', 0)) for x in suites),
                           skipped=sum(int(x.get('skipped', 0)) for x in suites))
        checks['tests_' + name] = tests[name] == dict(tests=n, failures=0, skipped=0)
    processes = []
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmd = proc.info['cmdline'] or []
            if '--worker' in cmd and any('chay_t047_v3.py' in s for s in cmd):
                processes.append(dict(pid=proc.pid, cmd=cmd))
        except psutil.Error:
            pass
    checks['no_method_workers'] = not processes
    diff = subprocess.run(['git', 'diff', '--check'], cwd=root, capture_output=True)
    (audit / 'git-diff-check.txt').write_bytes(diff.stdout + diff.stderr)
    checks['git_diff_check'] = diff.returncode == 0
    b = json.loads((out / 'runs/ngan-sach.json').read_text(encoding='utf-8'))
    used = b.get('used_seconds_when_waiting') if b.get('waiting_for_Minh_since_epoch') else None
    used = b['prior_seconds'] + time.time() - b['start_epoch'] if used is None else used
    checks['within_total_8_hours'] = b['cap_seconds'] == 28800 and used <= b['cap_seconds']
    if a.status == 'COMPLETE_PENDING_REVIEW':
        checks['T1_complete_PASS'] = json.loads((out / 't1.json').read_text(encoding='utf-8'))['PASS'] is True
        checks['T1_count_238'] = sum(m['so_ban_ghi'] for p, m in phases.items() if '/b2-' in p) == 238
        checks['K_count_1312'] = sum(m['so_ban_ghi'] for p, m in phases.items() if '/b3-' in p) == 1312
        checks['post_outputs_exist'] = all((out / p).is_file() for p in [
            'tai-lap-baseline.json', 'khoi-k.json', 'do-ben.json', 'so-sanh-t045.json', 'co-che-khoi-k.json'])
    else:
        checks['stop_named'] = a.status.startswith('STOP_')
    result = dict(integrity_PASS=all(checks.values()), status=a.status, checks=checks, tests=tests,
                  phase1=phases, budget_used_seconds=used, source_receipt=receipt,
                  workers=processes, scoring_labels_read=a.scoring_read,
                  note='Kiểm toàn vẹn/phạm vi không xác nhận cơ chế, hiệu chuẩn hay hiệu quả RCA.')
    ad.ghi(audit / 'kiem-ban-giao.json', result)
    files = {}
    for p in sorted(out.rglob('*')):
        if p.is_file() and p != out / 'manifest.json':
            files[p.relative_to(root).as_posix()] = dict(bytes=p.stat().st_size, sha256=sha(p))
    ad.ghi(out / 'manifest.json', dict(schema='T047-Q233-manifest-v1', status=a.status,
        git_HEAD=commit, source_base='c298188e', source_correction='Q-233/C1',
        source_sha256={'src/m1/cong.py': sha(root / 'src/m1/cong.py')},
        scoring_labels_read=a.scoring_read, phase1=phases, outputs=files,
        source_manifests={f'T-{s}': sha(root / f'results/T-{s}/manifest.json') for s in ('043', '044', '045', '046')},
        integrity_check=(audit / 'kiem-ban-giao.json').relative_to(root).as_posix(),
        note='Giữ mọi lượt kể cả lỗi/trước C1. Trạng thái chờ phản biện không tự nghiệm thu hoặc mở test.'))
    print(json.dumps(dict(integrity_PASS=result['integrity_PASS'], files=len(files), status=a.status,
                          used_minutes=used / 60, failed=[k for k, v in checks.items() if not v])))
    if not result['integrity_PASS']:
        raise SystemExit('Bàn giao còn lỗi toàn vẹn/phạm vi; xem kiem-ban-giao.json')


if __name__ == '__main__':
    main()

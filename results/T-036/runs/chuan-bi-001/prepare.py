"""Ghim đầu vào hiện hành; không tải, không đọc telemetry thô."""
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', '-C', str(cwd), *args]).decode('utf-8')


def main():
    selected = {}
    checks = []
    manifests = ['results/T-035/manifest.json', 'results/T-002/handoff-manifest.json',
                 'results/T-003/runs/final-review-003/artifact-manifest.json']
    public = ['results/T-002/public-metadata/run-002/sources/github-README.md',
              'results/T-002/public-metadata/run-002/sources/github-main-commit.json',
              'results/T-002/public-metadata/run-002/sources/hf-README.md',
              'results/T-008/sources/README.md', 'results/T-008/sources/repository.json',
              'results/T-008/sources/tree.json']
    for name in manifests:
        data = json.loads((ROOT / name).read_text(encoding='utf-8-sig'))
        entries = data.get('files', data.get('artifacts', []))
        for row in entries:
            p = row['path']
            use = name == manifests[0] or p in public
            if not use:
                continue
            # Manifest T-035 ne contient que sorties/code/documentation permis.
            if '/locked/' in p or '..' in Path(p).parts:
                raise ValueError('forbidden_manifest_path')
            actual = sha(ROOT / p)
            checks.append({'path': p, 'manifest': name, 'expected': row['sha256'],
                           'actual': actual, 'ok': actual == row['sha256']})
            selected[p] = (name, actual)
    save(OUT / 'input-verification.json', {'checks': checks})
    if not all(x['ok'] for x in checks):
        raise ValueError('input_hash_mismatch')
    sources = []
    system_root = Path('D:/Project/flash-ticket-platform')
    commit = git('rev-parse', 'HEAD', cwd=system_root).strip()
    for code, filename in [('B11', 'B11-C-target-architecture.md'),
                           ('B12', 'B12-data-ownership-and-schema.md'),
                           ('B13', 'B13-api-and-event-contracts.md'),
                           ('B14', 'B14-main-flow-sequences.md'),
                           ('B16', 'B16-observability-baseline.md')]:
        path = system_root / 'docs/architecture' / filename
        rel = path.relative_to(system_root).as_posix()
        head = subprocess.check_output(['git', '-C', str(system_root), 'show', f'HEAD:{rel}'])
        sources.append({'id': code, 'system': 'FlashTicket', 'kind': 'design',
                        'path': path.as_posix(), 'revision': commit,
                        'sha256': sha(path), 'dirty': head != path.read_bytes(),
                        'locator': 'toàn văn; các đoạn dùng được dẫn riêng trong provenance',
                        'dataset_link': 'not_applicable',
                        'condition': 'thiết kế bản mới; chưa là runtime', 'open': [
                            {'input': 'build/deployment/export runtime', 'owner': 'nhóm hệ thống/P9b',
                             'affects': 'xác nhận hệ đã chạy và placement thực'}]})
    for ident, path, system, kind in [
            ('RCAEval-README', public[0], 'RE2-TT', 'public-document'),
            ('RCAEval-revision', public[1], 'RE2-TT', 'repository-metadata'),
            ('RCAEval-dataset', public[2], 'RE2-TT', 'dataset-metadata'),
            ('Nezha-README', public[3], 'Nezha-OB', 'public-document'),
            ('Nezha-repository', public[4], 'Nezha-OB', 'repository-metadata'),
            ('Nezha-tree', public[5], 'Nezha-OB', 'repository-metadata')]:
        if path not in selected:
            raise ValueError(f'source_not_verified:{path}')
        manifest, digest = selected[path]
        sources.append({'id': ident, 'system': system, 'kind': kind, 'path': path,
                        'revision': 'snapshot đã lưu theo manifest; không là revision ứng dụng',
                        'sha256': digest, 'manifest': manifest, 'locator': 'toàn văn/JSON',
                        'dataset_link': 'OPEN', 'condition': 'nguồn khởi đầu truy phiên bản',
                        'open': [{'input': 'revision ứng dụng + image/deployment sinh dataset',
                                  'owner': 'T-038' if system == 'RE2-TT' else 'T-039',
                                  'affects': 'quy chênh lệch cho instrumentation'}]})
    for ident, path in [('T035-contract', 'results/T-035/dac-ta-do-thi.md'),
                         ('T035-code', 'src/do_thi/builder.py'),
                         ('T035-signals', 'results/T-035/thong-tin-theo-quan-he.md')]:
        sources.append({'id': ident, 'system': 'common', 'kind': 'internal-contract',
                        'path': path, 'revision': 'v2.1', 'sha256': selected[path][1],
                        'manifest': manifests[0], 'locator': 'toàn văn',
                        'dataset_link': 'not_applicable',
                        'condition': 'đầu vào ghim; chưa suy nghiệm thu T-035', 'open': []})
    save(ROOT / 'results/T-036/nguon.json', {'version': 1, 'sources': sources,
         'branches': {'FlashTicket': {'next': 'T-037', 'application_code': 'chưa có bản mới theo Minh'},
                      'RE2-TT': {'next': 'T-038', 'candidate_repository': 'https://github.com/FudanSELab/train-ticket',
                                'revision_dataset_application': 'OPEN; chưa tải'},
                      'Nezha-OB': {'next': 'T-039', 'candidate_repository': 'https://github.com/IntelligentDDS/Augmented-OnlineBoutique',
                                  'revision_dataset_application': 'OPEN; chưa tải'}}})
    save(OUT / 'preflight.json', {'started_utc': datetime.now(timezone.utc).isoformat(),
         'command': 'py -3 -X utf8 -B results/T-036/runs/chuan-bi-001/prepare.py',
         'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
         'base_commit': git('rev-parse', 'HEAD').strip(), 'git_status_before': git('status', '--porcelain'),
         'tracked_diff_before_sha256': hashlib.sha256(git('diff', '--binary').encode()).hexdigest(),
         'spec_sha256': sha(ROOT / 'tasks/T-036-p5b-hop-dong-chung/SPEC.md'),
         'manifest_hashes': {p: sha(ROOT / p) for p in manifests},
         'protected_hashes': {p: sha(ROOT / p) for p in [
             'AGENTS.md', 'docs/DECISIONS.md', 'docs/WHY.md', 'docs/MRP.md',
             'docs/LESSONS.md', 'docs/review-prompt.md', 'tasks/T-036-p5b-hop-dong-chung/SPEC.md']},
         'scope': ['results/T-036/', 'src/do_thi_tinh/__init__.py', 'src/do_thi_tinh/build.py',
                   'src/do_thi_tinh/compare.py', 'src/do_thi_tinh/README.md',
                   'tasks/T-036-p5b-hop-dong-chung/LOG.md', 'docs/STATE.md:T-036'],
         'subagents': False, 'network_download': False})
    (OUT / 'tracked-before.diff').write_text(git('diff', '--binary'), encoding='utf-8')
    print(json.dumps({'verified': len(checks), 'sources': len(sources), 'ok': True}))


if __name__ == '__main__':
    main()

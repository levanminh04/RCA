"""Freeze handoff file set and verify verbatim review prompt. No raw input."""
import ast
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-023'
LOG = ROOT / 'tasks/T-023-kiem-eadro/LOG.md'
BASE = '3b1e0dd2c736821d7a9e242a33fe1e600425f715'
OUTPUTS = 'results/T-023/de-xuat-chia-phien.csv, results/T-023/de-xuat-chia-phien.md, results/T-023/allowlist-phien.json, results/T-023/ke-hoach-kiem.md, results/T-023/kiem-eadro.md, results/T-023/bang-dieu-kien.csv, results/T-023/de-xuat-why.md, results/T-023/scripts/, results/T-023/runs/'


def digest(p):
    b = p.read_bytes()
    return {'path': str(p.relative_to(ROOT)).replace('\\', '/'), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


if __name__ == '__main__':
    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8')
    common = re.search(r'```text\n(.*?)\n```', template.split('## Prompt chung', 1)[1], re.S).group(1)
    expected = common.replace('<T-xxx>', 'T-023').replace('<T-xxx-tên>', 'T-023-kiem-eadro').replace('<danh sách>', OUTPUTS).replace('<commit gốc>', BASE)
    logtext = LOG.read_text(encoding='utf-8')
    actual = re.findall(r'```text\n(.*?)\n```', logtext, re.S)[-1]
    assert actual == expected, 'review prompt differs from the complete template'
    assert logtext.rstrip().endswith('```'), 'review prompt must end LOG'
    state_lines = (ROOT / 'docs/STATE.md').read_text(encoding='utf-8').splitlines()
    row = next(x for x in state_lines if x.startswith('| T-023 |'))
    assert 'Chờ phản biện (Claude)' in row
    files = [p for p in OUT.rglob('*') if p.is_file()]
    for p in files:
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8-sig'))
        elif p.suffix == '.csv':
            list(csv.DictReader(p.open(encoding='utf-8-sig')))
        elif p.suffix == '.py':
            ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
        if p.suffix in ('.py', '.md'):
            assert all(line == line.rstrip() for line in p.read_text(encoding='utf-8-sig').splitlines()), 'trailing whitespace '+str(p)
    run = OUT / 'runs/handoff-001'
    run.mkdir(exist_ok=False)
    checks = {'PASS': True, 'review_prompt_exact_template': True, 'no_G2_block_in_template': '**G2' not in template,
              'review_prompt_last_in_LOG': True, 'state_T023_awaiting_Claude': True,
              'all_JSON_CSV_script_syntax_valid': True, 'final_verifier': 'runs/check-005/verification.json',
              'raw_opened_in_handoff_check': False}
    (run / 'verification.json').write_text(json.dumps(checks, indent=2)+'\n', encoding='utf-8')
    manifest = {'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'task': 'T-023',
                'scientific_run': 'stream-002', 'retained_superseded_run': 'stream-001',
                'artifact_files': [digest(p) for p in sorted(OUT.rglob('*')) if p.is_file()],
                'LOG': digest(LOG), 'STATE_T023_row': row,
                'scope': ['results/T-023/', 'tasks/T-023-kiem-eadro/LOG.md', 'docs/STATE.md row T-023'],
                'external_files_written': [], 'DECISIONS_and_WHY': 'proposal only, no write',
                'note': 'manifest excludes its own bytes; original raw-run manifest retained separately'}
    (run / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS handoff: exact review prompt, parsed files, awaiting Claude; ' + str(len(manifest['artifact_files'])) + ' hashed artifact files plus manifest')

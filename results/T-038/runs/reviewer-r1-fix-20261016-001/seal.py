"""Final read-back and reviewer-only manifest sealing, retaining the first seal."""
from copy import deepcopy
from datetime import datetime, timezone
import ast
import json
from pathlib import Path
import time

import prepare_repair as repair

HERE, ROOT, BASE = repair.HERE, repair.ROOT, repair.BASE


def main():
    started = time.perf_counter()
    summary = repair.load(HERE / 'candidate/summary.json')
    graphs = {level: repair.load(HERE / 'candidate/do-thi' / name) for level, name in [('entity', 'thuc-the.json'), ('operation', 'thao-tac.json')]}
    mappings = repair.load(BASE / 'mapping.json')
    for i, row in enumerate(summary['rows'], 1):
        assert repair.sha(ROOT / row['input']) == row['input_sha256']
        assert repair.sha(ROOT / row['output']) == row['output_sha256']
        result = repair.read_compressed(ROOT / row['output'])
        trace = repair.load(ROOT / row['input'])
        repair.check_result(result, graphs[row['level']], trace, mappings)
        for name, view in result['views'].items():
            for key, expected in row['views'][name].items():
                assert (len(view[key]) if isinstance(view[key], list) else view[key]) == expected
        if i % 300 == 0:
            print(repair.canonical({'read_back_verified': i, 'total': summary['graph_count']}), flush=True)
    protected = repair.load(HERE / 'protected-before.json')
    changed = [dict(path=name, expected_sha256=digest, actual_sha256=repair.sha(ROOT / name))
        for name, digest in protected.items() if repair.sha(ROOT / name) != digest]
    assert {r['path'] for r in changed} <= {'docs/STATE.md', 'docs/DECISIONS.md'}
    expected_row = repair.load(HERE / 'before/manifest.json')['state_T038_row']
    assert next(x for x in (ROOT / 'docs/STATE.md').read_text(encoding='utf-8-sig').splitlines() if x.startswith('| T-038 |')) == expected_row
    for path in HERE.rglob('*.py'):
        ast.parse(path.read_text(encoding='utf-8-sig'))
    for path in HERE.rglob('*.json'):
        repair.load(path)
    repair.save('checks/seal-verification.json', dict(all_pass=True,
        candidate_outputs_read_back_and_independently_checked=summary['graph_count'],
        protected_unchanged=len(protected) - len(changed), external_shared_metadata_changes=changed,
        T038_STATE_row_unchanged=True, root_producer_outputs_modified=False,
        first_seal_and_finalizer_version_retained=True,
        accounting_correction='First finalizer stdout printed the total checked count under protected_unchanged; final verification already distinguished external changes. Corrected stdout label calculation without changing model/graph/result.',
        elapsed_seconds=time.perf_counter() - started, network_bytes=0,
        reviewer_report_sha256=repair.sha(ROOT / 'tasks/T-038-p5b-trainticket/REVIEW.md')))
    prior = repair.load(HERE / 'manifest-first-finalization.json')
    files = [dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=repair.sha(p))
        for p in sorted(HERE.rglob('*')) if p.is_file() and p != HERE / 'manifest.json']
    manifest = {k: v for k, v in prior.items() if k not in {'files', 'file_count', 'total_payload_bytes_excluding_manifest', 'created_utc'}}
    manifest.update(created_utc=datetime.now(timezone.utc).isoformat(), files=files,
        file_count=len(files), total_payload_bytes_excluding_manifest=sum(x['bytes'] for x in files),
        previous_manifest='manifest-first-finalization.json',
        reviewer_report=dict(path='tasks/T-038-p5b-trainticket/REVIEW.md', sha256=repair.sha(ROOT / 'tasks/T-038-p5b-trainticket/REVIEW.md')),
        final_validation='checks/seal-verification.json')
    # Explicit reviewer-run manifest replacement; the exact old manifest is retained above.
    (HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for row in manifest['files']:
        assert repair.sha(ROOT / row['path']) == row['sha256']
    print(repair.canonical(dict(status='VALIDATED_REPAIR_PROPOSAL_NOT_ADOPTED', graphs=summary['graph_count'],
        files=len(files), bytes=manifest['total_payload_bytes_excluding_manifest'],
        protected_unchanged=len(protected) - len(changed), external_shared_metadata_changes=len(changed))), flush=True)


if __name__ == '__main__':
    main()

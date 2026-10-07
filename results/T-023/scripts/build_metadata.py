"""T-023 bước 0–1: chỉ metadata đã lưu; không mở ZIP hoặc telemetry."""
import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import pathlib
import platform
import re
import sys
import time
import traceback

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-023'
SEED = 20261004
SESSION = re.compile(r'TT\.\d{4}-\d{2}-\d{2}T\d{6}D\d{4}-\d{2}-\d{2}T\d{6}')
SOURCE_FILES = [
    'results/T-009/runs/run-001/labels.json',
    'results/T-009/runs/run-001/normal_intervals.json',
    'results/T-009/runs/run-001/inventory.json',
    'results/T-009/runs/inspect-004/nested-inventory.json',
    'results/T-009/runs/inspect-004/logical-member-sizes.json',
    'results/T-009/runs/download-001/archive-directory.json',
    'results/T-009/runs/download-001/manifest.json',
    'results/T-021/chia-theo-o/A-phan-tang.csv',
    'AGENTS.md', 'docs/PLAN-P3-G2.md', 'docs/DECISIONS.md',
    'tasks/T-023-kiem-eadro/SPEC.md',
]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def session_of_label(source):
    return pathlib.PurePosixPath(source).name.replace('.fault-', '.').removesuffix('.json')


def main(run):
    start = time.monotonic()
    labels = [x for x in load(SOURCE_FILES[0]) if x['dataset'] == 'TT']
    normals = [x for x in load(SOURCE_FILES[1]) if x['dataset'] == 'TT']
    inventory = [x for x in load(SOURCE_FILES[3]) if x['dataset'] == 'TT']
    groups = collections.defaultdict(list)
    for x in labels:
        groups[session_of_label(x['source'])].append(x)
    assert len(labels) == 81 and len(groups) == 9
    roots = collections.defaultdict(set)
    cells = collections.Counter((x['service'], x['fault']) for x in labels)
    for sid, rows in groups.items():
        assert len(rows) == 9 and len({x['service'] for x in rows}) == 3
        for x in rows:
            roots[x['service']].add(sid)
    assert len(roots) == 27 and all(len(v) == 1 for v in roots.values())
    assert len(cells) == 81 and set(cells.values()) == {1}
    assert dict(collections.Counter(x['fault'] for x in labels)) == {
        'cpu_load': 27, 'network_delay': 27, 'network_loss': 27}
    assert len({(x['source'], x['index_in_file']) for x in labels}) == 81
    scores = {s: hashlib.sha256(f'{SEED}|Eadro-TT|{s}'.encode()).hexdigest() for s in groups}
    ordered = sorted(groups, key=lambda s: (scores[s], s))
    dev, test = ordered[:3], ordered[3:]
    normal_order = sorted(normals, key=lambda x: session_of_label(x['source']))
    assert len(normal_order) == 2
    roles = {s: 'dev' for s in dev} | {s: 'test' for s in test}
    roles.update({session_of_label(x['source']): role for x, role in
                  zip(normal_order, ('reference', 'control'))})
    # Match only neutral session token + relative leaf path. Hash/byte equality
    # resolves metadata duplicates, never array order or last-wins.
    representations = collections.defaultdict(list)
    for x in inventory:
        if not (x['member'].endswith(('/spans.json', '/logs.json')) or
                ('/metrics/' in x['member'] and x['member'].endswith('.csv'))):
            continue
        match = SESSION.search(x['member'])
        assert match, x['member']
        key = (match.group(), x['member'][match.end() + 1:])
        representations[key].append(x)
    session_members = collections.defaultdict(list)
    duplicates = []
    member_rows = []
    for (sid, relative), copies in sorted(representations.items()):
        assert len({(x['bytes'], x['sha256']) for x in copies}) == 1, (sid, relative)
        outer = [x for x in copies if x['origin'] == 'outer']
        assert len(outer) <= 1
        chosen = outer[0] if outer else copies[0]
        assert outer or len(copies) == 1, (sid, relative)
        item = {k: chosen[k] for k in ('origin', 'member', 'bytes', 'sha256')}
        session_members[sid].append(item)
        if len(copies) > 1:
            duplicates.append({'session': sid, 'relative_member': relative,
                               'canonical': item, 'representations': copies})
        for x in copies:
            member_rows.append({'session': sid, 'proposed_role': roles.get(sid, 'OPEN'),
                                'origin': x['origin'], 'member': x['member'],
                                'bytes': x['bytes'], 'sha256': x['sha256'],
                                'canonical': x is chosen, 'approval': 'NOT_APPROVED'})
    assert len(session_members) == 12 and len(duplicates) == 261
    assert all(len(xs) == 29 for xs in session_members.values())
    unlabeled = sorted(set(session_members) - set(roles))
    assert unlabeled == ['TT.2022-04-20T134450D2022-04-20T155957']
    # Cross-check the extracted event metadata against each saved label source.
    for sid, rows in groups.items():
        source = rows[0]['source']
        label = load('results/T-009/' + source)
        for row in rows:
            native = label['faults'][row['index_in_file']]
            assert (native['name'], native['fault'], native['start'], native['duration']) == (
                row['entity_raw'], row['fault'], row['start'], row['duration'])
        assert label['start'] == rows[0]['session_start']
        assert label['end'] == rows[0]['session_end']
    for x in normal_order:
        source = load('results/T-009/' + x['source'])
        assert source['faults'] == [] and source['start'] == x['start'] and source['end'] == x['end']
    archive = ROOT / 'data/ngoai-rcaeval/eadro/train-ticket/TT Dataset.zip'
    archive_manifest = next(x for x in load(SOURCE_FILES[6])['items'] if x['path'].startswith('train-ticket/'))
    assert archive.is_file() and archive.stat().st_size == archive_manifest['actual_bytes']
    directory = next(x for x in load(SOURCE_FILES[5])['items'] if x['path'].startswith('train-ticket/'))
    outer_names = {x['name'] for x in directory['members']}
    proposed = []
    session_rows = []
    events = []
    for sid in sorted(session_members):
        rows = sorted(groups.get(sid, []), key=lambda x: x['start'])
        normal = next((x for x in normal_order if session_of_label(x['source']) == sid), None)
        role = roles.get(sid, 'OPEN')
        members = session_members[sid]
        for member in members:
            assert (member['member'] if member['origin'] == 'outer' else member['origin']) in outer_names
        label_sources = sorted({x['source'] for x in rows}) if rows else [normal['source']] if normal else []
        session_rows.append({
            'session': sid, 'kind': 'fault' if rows else 'faults=[]' if normal else 'unlabelled',
            'proposed_role': role, 'approval': 'NOT_APPROVED', 'event_count': len(rows),
            'roots': ';'.join(sorted({x['service'] for x in rows})),
            'fault_types': ';'.join(sorted({x['fault'] for x in rows})),
            'label_sources': ';'.join(label_sources),
            'canonical_origins': ';'.join(sorted({x['origin'] for x in members})),
            'member_count': len(members), 'logical_bytes': sum(x['bytes'] for x in members),
            'member_map': f'runs/{run.name}/member-map.csv', 'seed': SEED if rows else '',
        })
        if role in ('dev', 'reference', 'control'):
            proposed.append({'session': sid, 'role': role, 'label_sources': label_sources,
                             'scope': 'whole_session_all_three_channels', 'members': members})
        previous_end = None
        for x in rows:
            lower = max(x['session_start'], x['start'] - 300,
                        previous_end if previous_end is not None else x['session_start'])
            events.append({'session': sid, 'proposed_role': role, 'event_index': x['index_in_file'],
                           'source': x['source'], 'root_for_audit_only': x['service'],
                           'fault_for_audit_only': x['fault'], 'injection_start_s': x['start'],
                           'injection_end_s': x['end_derived'], 'session_start_s': x['session_start'],
                           'session_end_s': x['session_end'], 'previous_injection_end_s': previous_end,
                           'q64_pre_start_s': lower, 'q64_pre_available_s': x['start'] - lower,
                           'q64_post_end_s': x['start'] + 300})
            assert x['start'] + 300 <= x['session_end']
            previous_end = x['end_derived']
    # Only metadata from the previous cell split: report the migration; no rights.
    with (ROOT / SOURCE_FILES[7]).open(encoding='utf-8-sig', newline='') as f:
        old_rows = list(csv.DictReader(f))
    old_tt = [x for x in old_rows if x.get('dataset') == 'Eadro-TT']
    old_header = list(old_rows[0])
    summary = {'task': 'T-023', 'step': 'metadata_only', 'new_telemetry_rows_read': 0,
               'archive_payloads_opened': 0, 'events': 81, 'roots': 27, 'fault_sessions': 9,
               'dev_sessions_proposed': dev, 'test_sessions_proposed': test,
               'dev_events_proposed': 27, 'test_events_proposed': 54,
               'dev_roots_proposed': 9, 'test_roots_proposed': 18, 'root_overlap': 0,
               'normal_sessions_proposed': [x['session'] for x in proposed if x['role'] != 'dev'],
               'unlabelled_sessions_excluded': unlabeled,
               'metadata_duplicate_telemetry_members': len(duplicates),
               'canonical_members_proposed': sum(len(x['members']) for x in proposed),
               'logical_telemetry_bytes_proposed': sum(m['bytes'] for x in proposed for m in x['members']),
               'q64_pre_available_s_all_events': sorted(set(round(x['q64_pre_available_s'], 6) for x in events)),
               'old_cell_split_rows_tt': len(old_tt), 'old_cell_split_header': old_header,
               'all_metadata_checks_passed': True, 'elapsed_seconds': time.monotonic() - start,
               'status': 'WAITING_FOR_SESSION_APPROVAL'}
    metadata_sources = [{
        'path': p, 'bytes': (ROOT / p).stat().st_size,
        'sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()} for p in SOURCE_FILES]
    metadata_sources.extend({'path': 'results/T-009/' + p, 'bytes': (ROOT / 'results/T-009' / p).stat().st_size,
                             'sha256': hashlib.sha256((ROOT / 'results/T-009' / p).read_bytes()).hexdigest()}
                            for p in sorted({x['source'] for x in labels + normals}))
    allowlist = {'schema_version': 1, 'task': 'T-023', 'status': 'proposed',
                 'approved_by': None, 'approved_at': None, 'approval_quote': None,
                 'approved_sessions': [], 'proposed_sessions': proposed,
                 'test_sessions': test, 'unlabelled_sessions': unlabeled,
                 'denied_origins': ['TT Dataset/TT-all.txz', 'TT Dataset/no fault/TT-no-fault.txz'],
                 'seed': SEED, 'split_key': '20261004|Eadro-TT|<session>', 'dev_fraction': '3/9',
                 'archive': {'path': str(archive.relative_to(ROOT)).replace('\\', '/'),
                             'source_manifest': SOURCE_FILES[6], 'expected_bytes': archive_manifest['actual_bytes'],
                             'expected_sha256': archive_manifest['sha256'], 'hash_rechecked_in_T023': False},
                 'metadata_run': str(run.relative_to(OUT)).replace('\\', '/'),
                 'provenance': metadata_sources,
                 'note': 'Không có quyền đọc mới; loader phải từ chối khi status != approved. Nhãn chỉ dùng audit/chấm.'}
    write_csv(OUT / 'de-xuat-chia-phien.csv', session_rows)
    write_csv(run / 'events.csv', events)
    write_csv(run / 'member-map.csv', member_rows)
    write_json(run / 'duplicates-metadata.json', duplicates)
    write_json(run / 'split-order.json', {'seed': SEED, 'key': '20261004|Eadro-TT|<session>',
                                        'rank': [{'session': s, 'sha256': scores[s]} for s in ordered]})
    write_json(OUT / 'allowlist-phien.json', allowlist)
    write_json(run / 'summary.json', summary)
    write_json(run / 'manifest.json', {
        'started_at': dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).isoformat(),
        'command': ' '.join(sys.argv), 'python': sys.version, 'device': platform.node(),
        'input_metadata': metadata_sources, 'archive_stat_only': True,
        'archive_hash_rechecked': False, 'telemetry_opened': [],
        'script_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'logical_bytes_definition': 'Tổng byte cuối canonical; không phải RAM/đĩa ghi hoặc byte nén stream.',
    })
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'metadata-\d{3}', args.run_id):
        raise ValueError('run-id không hợp lệ')
    run = OUT / 'runs' / args.run_id
    run.mkdir(parents=True, exist_ok=False)
    try:
        main(run)
    except Exception as error:
        write_json(run / 'failure.json', {'error': repr(error), 'traceback': traceback.format_exc(),
                                         'telemetry_opened': []})
        raise

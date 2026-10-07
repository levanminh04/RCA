"""Kiểm độc lập bản đề xuất, nhãn nguồn và provenance; không đọc archive."""
import argparse
import collections
import csv
import datetime
import hashlib
import json
import pathlib
import re
import shutil
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-023'


def j(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main(run_id):
    run = OUT / 'runs' / run_id
    run.mkdir(exist_ok=False)
    started = time.monotonic()
    checks = {}
    try:
        a = j(OUT / 'allowlist-phien.json')
        assert a['status'] == 'proposed' and a['approved_sessions'] == []
        assert a['approved_by'] is None and a['approval_quote'] is None
        checks['approval_not_inferred_from_spec'] = True
        source = ROOT / 'results/T-009'
        files = sorted((source / 'sources/labels/TT').glob('*.json'))
        direct = {}
        empty = []
        for path in files:
            s = path.stem.replace('.fault-', '.')
            x = j(path)
            if x['faults']:
                direct[s] = x
            else:
                empty.append(s)
        assert len(direct) == 9 and len(empty) == 2
        assert sum(len(x['faults']) for x in direct.values()) == 81
        root_sessions = collections.defaultdict(set)
        for s, x in direct.items():
            for fault in x['faults']:
                root_sessions[fault['name']].add(s)
        assert len(root_sessions) == 27 and all(len(v) == 1 for v in root_sessions.values())
        # Independent neutral ordering from original source filenames.
        rank = sorted(direct, key=lambda s: hashlib.sha256(('20261004|Eadro-TT|' + s).encode()).digest())
        proposed_dev = sorted(x['session'] for x in a['proposed_sessions'] if x['role'] == 'dev')
        assert proposed_dev == sorted(rank[:3])
        assert sorted(a['test_sessions']) == sorted(rank[3:])
        assert sorted(x['session'] for x in a['proposed_sessions'] if x['role'] != 'dev') == sorted(empty)
        checks['split_matches_direct_labels_and_seed'] = True
        raw_inventory = [x for x in j(source / 'runs/inspect-004/nested-inventory.json') if x['dataset'] == 'TT']
        index = {(x['origin'], x['member']): x for x in raw_inventory}
        assert len(index) == len(raw_inventory)
        canonical_keys = set()
        for session in a['proposed_sessions']:
            assert session['session'] not in a['test_sessions'] + a['unlabelled_sessions']
            members = session['members']
            assert len(members) == 29
            assert sum(m['member'].endswith('/spans.json') for m in members) == 1
            assert sum(m['member'].endswith('/logs.json') for m in members) == 1
            assert sum(m['member'].endswith('.csv') for m in members) == 27
            for m in members:
                key = (m['origin'], m['member'])
                assert key not in canonical_keys
                canonical_keys.add(key)
                old = index[key]
                assert (m['bytes'], m['sha256']) == (old['bytes'], old['sha256'])
                assert session['session'] + '/' in m['member']
                assert m['origin'] == 'outer' if session['role'] == 'dev' else m['origin'].endswith(session['session'] + '.tar.xz')
                assert m['origin'] not in a['denied_origins']
                p = pathlib.PurePosixPath(m['member'])
                assert not p.is_absolute() and '..' not in p.parts
        assert len(canonical_keys) == 145
        checks['exact_members_and_scope_match_source_metadata'] = True
        # Metadata duplicate comparison includes labels, not just raw telemetry.
        identities = collections.defaultdict(list)
        for x in raw_inventory:
            member = x['member'].removeprefix('TT Dataset/') if x['origin'] == 'outer' else x['member']
            identities[member].append(x)
        duplicate_groups = [xs for xs in identities.values() if len(xs) > 1]
        assert len(duplicate_groups) == 270
        assert all(len({(x['bytes'], x['sha256']) for x in xs}) == 1 for xs in duplicate_groups)
        duplicate_nested_bytes = sum(x['bytes'] for xs in duplicate_groups for x in xs if x['origin'] != 'outer')
        assert duplicate_nested_bytes == j(source / 'runs/inspect-004/logical-member-sizes.json')['groups']['TT']['verified_duplicate_nested_member_bytes']
        for path in files:
            matching = [x for x in raw_inventory if x['origin'] == 'outer' and pathlib.PurePosixPath(x['member']).name == path.name]
            assert len(matching) == 1
            assert matching[0]['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        checks['all_11_saved_labels_match_outer_hash_metadata'] = True
        checks['all_270_duplicate_groups_exact_in_metadata'] = True
        old = [x for x in rows(ROOT / 'results/T-021/chia-theo-o/A-phan-tang.csv') if x['dataset'] == 'Eadro-TT']
        old_roles = collections.defaultdict(set)
        case_sessions = {
            'TT|{}|{}|{}'.format(f['name'].removeprefix('dockercomposemanifests_').removesuffix('_1'),
                               f['fault'], f['start']): s
            for s, label in direct.items() for f in label['faults']}
        for x in old:
            assert x['case'] in case_sessions, x['case']
            old_roles[case_sessions[x['case']]].add(x['vai_tro'])
        assert len(old_roles) == 9 and all(v == {'dev', 'test'} for v in old_roles.values())
        checks['old_cell_split_mixes_all_9_sessions'] = True
        for p in a['provenance']:
            assert hashlib.sha256((ROOT / p['path']).read_bytes()).hexdigest() == p['sha256'], p['path']
        checks['source_hashes_unchanged_since_metadata_run'] = True
        event_rows = rows(OUT / 'runs/metadata-001/events.csv')
        assert len(event_rows) == 81
        pre = []
        for e in event_rows:
            native = direct[e['session']]['faults'][int(e['event_index'])]
            assert float(e['injection_start_s']) == native['start']
            assert float(e['injection_end_s']) == native['start'] + native['duration']
            assert float(e['q64_post_end_s']) == native['start'] + 300
            previous_end = float(e['previous_injection_end_s']) if e['previous_injection_end_s'] else direct[e['session']]['start']
            assert float(e['q64_pre_start_s']) == max(native['start'] - 300, direct[e['session']]['start'], previous_end)
            pre.append(float(e['q64_pre_available_s']))
        assert max(pre) < 300
        checks['all_81_q64_pre_windows_shorter_than_300s'] = True
        table = rows(OUT / 'de-xuat-chia-phien.csv')
        assert len(table) == 12 and all(x['approval'] == 'NOT_APPROVED' for x in table)
        checks['proposal_table_complete_and_not_approved'] = True
        result = {'task': 'T-023', 'checks': checks, 'all_passed': True,
                  'metadata_only': True, 'new_telemetry_rows_read': 0, 'archive_payloads_opened': 0,
                  'old_mixed_sessions': sorted(old_roles), 'duplicate_final_member_groups': 270,
                  'duplicate_nested_bytes': duplicate_nested_bytes,
                  'q64_pre_available_s_min': min(pre), 'q64_pre_available_s_max': max(pre),
                  'input_label_files': [str(p.relative_to(ROOT)).replace('\\', '/') for p in files],
                  'elapsed_seconds': time.monotonic() - started,
                  'disk_free_bytes_observed': shutil.disk_usage(ROOT).free,
                  'peak_ram': None, 'peak_ram_note': 'Không đo lượt metadata ngắn; không suy RAM streaming.'}
    except Exception as exc:
        result = {'all_passed': False, 'checks_completed': checks, 'error': repr(exc)}
        (run / 'failure.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        raise
    (run / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    run_id = parser.parse_args().run_id
    if not re.fullmatch(r'check-\d{3}', run_id):
        raise ValueError('run-id không hợp lệ')
    main(run_id)

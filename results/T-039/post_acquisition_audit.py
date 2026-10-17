"""Đếm khối lượng nguồn để xét khả thi; không là semantic inventory/mapping."""
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import re
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
OUT = BASE / 'runs' / sys.argv[1]
OUT.mkdir(parents=True, exist_ok=False)
start = time.perf_counter()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


try:
    a = json.loads((BASE / 'runs/thu-nguon-001/acquisition.json').read_text(encoding='utf-8'))
    inputs = a['files'] + a['metadata']
    integrity = []
    for row in inputs:
        p = ROOT / row['path']
        b = p.read_bytes()
        integrity.append({'path': row['path'], 'ok': len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256']})
    assert all(r['ok'] for r in integrity)
    save('integrity.json', {'all_ok': True, 'count': len(integrity), 'rows': integrity})
    groups = defaultdict(lambda: {'files': 0, 'utf8_lines': 0, 'utf8_bytes': 0, 'binary_files': 0})
    paths = []
    jars = []
    ob = BASE / 'sources/augmented-ob-94a01ba4'
    for row in a['files']:
        p = ROOT / row['path']
        rel = p.relative_to(ob) if p.is_relative_to(ob) else p.relative_to(BASE / 'sources/nezha-d8140101')
        group = rel.parts[1] if len(rel.parts) > 2 and rel.parts[0] == 'src' else ('OB-other' if p.is_relative_to(ob) else 'Nezha-supplement')
        groups[group]['files'] += 1
        try:
            text = p.read_text(encoding='utf-8')
            lines = len(text.splitlines())
            groups[group]['utf8_lines'] += lines
            groups[group]['utf8_bytes'] += row['bytes']
            kind = 'utf8_decoded_for_size_only'
        except UnicodeDecodeError:
            groups[group]['binary_files'] += 1
            lines = None
            kind = 'binary_identity_only'
        paths.append({'path': row['path'], 'bytes': row['bytes'], 'lines': lines,
                      'integrity_verified': True, 'profile_status': kind,
                      'semantic_review': 'not_claimed_by_this_script'})
        if p.suffix == '.jar':
            with zipfile.ZipFile(p) as z:
                jars.append({'path': row['path'], 'entry_count': len(z.infolist()),
                             'expanded_total_bytes': sum(e.file_size for e in z.infolist()),
                             'largest_entry_bytes': max(e.file_size for e in z.infolist()),
                             'manifest': z.read('META-INF/MANIFEST.MF').decode('utf-8', errors='replace'),
                             'expanded_disk_bytes': 0, 'executed': False})
    save('source-profile.json', {'status': 'cost_profile_not_semantic_coverage',
         'groups': dict(groups), 'rows': paths,
         'total_utf8_lines': sum(g['utf8_lines'] for g in groups.values()),
         'total_utf8_bytes': sum(g['utf8_bytes'] for g in groups.values()),
         'binary_files': sum(g['binary_files'] for g in groups.values())})
    save('jar-metadata.json', jars)
    resources = []
    for p in sorted((ob / 'kubernetes-manifests').glob('*.yaml')):
        for document in re.split(r'(?m)^---\s*$', p.read_text(encoding='utf-8')):
            kind = re.search(r'(?m)^kind:\s*(\S+)', document)
            name = re.search(r'(?m)^metadata:\s*\n\s+name:\s*(\S+)', document)
            if kind and name:
                resources.append({'path': p.relative_to(ROOT).as_posix(),
                                  'kind': kind[1], 'name': name[1]})
    protos = []
    for p in sorted(ob.rglob('*.proto')):
        text = p.read_text(encoding='utf-8')
        protos.append({'path': p.relative_to(ROOT).as_posix(),
                       'services': re.findall(r'(?m)^service\s+(\w+)', text),
                       'rpc_names': re.findall(r'\brpc\s+(\w+)\s*\(', text),
                       'note': 'lexical declaration count, not registered runtime inventory'})
    save('declarations.json', {'resource_declarations': resources,
         'declaration_count': len(resources),
         'distinct_kind_name_count': len({(r['kind'], r['name']) for r in resources}),
         'protos': protos, 'claim': 'source structure only; no union deployment or runtime assertions'})
    save('finish.json', {'all_ok': True, 'seconds_not_isolated_pilot': time.perf_counter() - start,
                         'new_network_bytes': 0, 'rca_or_build_run': False})
    print(json.dumps({'all_ok': True, 'source_inputs': len(integrity),
          'utf8_lines': sum(g['utf8_lines'] for g in groups.values()),
          'utf8_bytes': sum(g['utf8_bytes'] for g in groups.values()),
          'binary_files': sum(g['binary_files'] for g in groups.values()),
          'resource_declarations': len(resources),
          'distinct_kind_name': len({(r['kind'], r['name']) for r in resources})}))
except BaseException as error:
    save('failure.json', {'type': type(error).__name__, 'message': str(error)})
    raise

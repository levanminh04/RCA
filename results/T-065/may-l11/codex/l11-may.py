"""T-065 L11b: copy pinned exports, rebuild two slots, update three pinned dashboards.

P is injected by the local packager. No raw export, M1 run, scoring, or credential file.
"""
import base64
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time
import urllib.request

R = pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l11-001')
OLD = R.with_name('t065-l8b-001')
B = pathlib.Path('/opt/flash-ticket-obs/pinned')
C = 'flash-ticket-obs-grafana'


def stop():
    for home in ('/home/ubuntu', '/root'):
        assert not (pathlib.Path(home) / 'rca-dieu-phoi/STOP').exists(), 'STOP remote'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(p):
    return json.loads(pathlib.Path(p).read_bytes())


def digest(data):
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def pin(p):
    return digest(pathlib.Path(p).read_bytes())


def write(p, value):
    p = pathlib.Path(p)
    assert p.is_relative_to(R)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf8')


def emit(value):
    print(json.dumps(value, ensure_ascii=False), flush=True)


def inspect():
    return json.loads(subprocess.check_output(['docker', 'inspect', C]))[0]


def api(endpoint):
    env = dict(x.split('=', 1) for x in inspect()['Config']['Env'] if '=' in x)
    auth = base64.b64encode((env.get('GF_SECURITY_ADMIN_USER', 'admin') + ':' + env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
    request = urllib.request.Request('http://10.0.0.215:3000' + endpoint, headers={'Authorization': 'Basic ' + auth})
    with urllib.request.urlopen(request, timeout=35) as result:
        return {'http': result.status, 'data': json.load(result)}


def inventory():
    stop()
    ins = inspect()
    return {'utc': now(), 'files': {str(p): pin(p) for p in [B / 'compose.json', *sorted((B / 'provisioning').rglob('*'))] if p.is_file()},
            'machine': {'started_at': ins['State']['StartedAt'], 'restart_count': ins['RestartCount'], 'status': ins['State']['Status']}}


def check_old():
    for rel, expected in P['old_files'].items():
        assert pin(OLD / rel) == expected, ('old pin', rel)


def targets_current(which):
    result = {}
    for name, target in P['targets'].items():
        path = pathlib.Path(target['path'])
        assert path.is_relative_to(B / 'provisioning/dashboards') and not path.is_symlink()
        assert pin(path) == target[which], ('target pin', name, which)
        result[name] = {'path': str(path), **pin(path), 'api': api('/api/dashboards/uid/' + target['uid'])}
        assert result[name]['api']['http'] == 200
        for field in ('uid', 'title', 'panels', 'templating', 'time'):
            assert result[name]['api']['data']['dashboard'][field] == read(path)[field], ('GET/file', name, field)
    return result


def rebuild(ed, case):
    name, ca = ed['ban'], case['ca']
    directory = R / 'du-lieu' / name
    d = read(directory / (ca + '.json'))
    old = copy.deepcopy(d)
    m = read(R / 'nguon' / name / ca / 'method-output-1.json')
    assert pin(R / 'nguon' / name / ca / 'method-output-1.json')['sha256'] == case['sha256']
    for key in ('cau_hinh_sha256', 'ma_nguon_sha256'):
        assert m['extra']['m1_ft'][key] == ed[key]
    flags, units = m['extra']['kenh_co'], m['extra']['don_vi_phan_vi']
    assert len(flags) == 64 and not any(f['don_vi'] == 'metric|payment-service_live-down' for f in flags)
    assert m['extra']['m1_ft']['chu_thich']['H5-liveness']['chet_im']['thanh_phan'] == {}
    unit_map = {u['ma']: u for u in units}
    meta = d['ban']
    meta.update(nguon_output=case['dau_ra'], sha256_output=case['sha256'])
    rank = [{**r, 'hang': r['tie_group'] + 1, 'lop': m['classes'].get(r['entity']),
             'so_kenh_co': sum(f['thuc_the'] == r['entity'] for f in flags)} for r in m['entity_ranking']]
    assert [(r['entity'], r['tie_group']) for r in old['entity_ranking']] == [(r['entity'], r['tie_group']) for r in m['entity_ranking']]
    for op in d['thao_tac']:
        key = 'op|' + op['chu'] + '|' + op['ten']
        unit = unit_map.get(key)
        selected = [f for f in flags if f['don_vi'] == key]
        state = unit['trang_thai'] if unit else 'KHONG_CHAM_SPAN_BOC'
        op.update(trang_thai_m1=state, co_len=unit.get('F_raw_len', 0) if unit else 0,
                  co_xuong=unit.get('F_raw_xuong', 0) if unit else 0, co_m1=bool(selected), so_kenh_co=len(selected),
                  kenh_co=selected, don_vi_m1=unit, mau='#E02F44' if selected else '#8E8E8E' if state == 'OK' else '#CA95E5', ban_kinh=32)
    links = {row['id']: row['lien_ket'] for row in old['bang_chung']}
    assert all(f['ma'] in links for f in flags), 'new evidence needs another export path'
    d['bang_chung'] = [{'id': f['ma'], 'don_vi': f['don_vi'], 'thuc_the': f['thuc_the'], 'kenh': f['ten'], 'huong': f['huong'],
                       'lop': f['lop'], 's': f['s'], 'F_I': f['F_I'], 'khoi_phat_ns': f.get('khoi_phat'), 'lien_ket': links[f['ma']]} for f in flags]
    d.update(entity_ranking=m['entity_ranking'], ranking_rows=rank, co_m1=flags, don_vi_m1=units,
             region=m['region'], classes=m['classes'], ke_thua=m['inherited_by'], nguon_cua_so=case['dau_ra'])
    d['su_co']['ket_luan'] = m['verdict']
    assert d['su_co']['ket_luan'] == old['su_co']['ket_luan']
    edge_ranks = m['extra']['m1_ft'].get('canh_xep_hang')
    d['canh_xep_hang'] = edge_ranks or []
    d['trang_thai_canh'] = 'không có đầu ra cạnh' if edge_ranks is None else f'{len(edge_ranks)} dòng cạnh từ extra.m1_ft.canh_xep_hang; không xếp lại'
    write(directory / (ca + '.json'), d)
    vue_path = directory / 'vue' / (ca + '.json')
    write(vue_path, {k: d.get(k) for k in read(vue_path)})
    for svc in d['services']:
        service_path = directory / 'thao-tac-vue' / ca / (svc + '.json')
        service = read(service_path)
        ops = [op for op in d['thao_tac'] if op['chu'] == svc]
        own = {op['id'] for op in ops}
        edges = [e for e in d['canh_thao_tac'] if e['source'] in own or e['target'] in own]
        ids = own | {x for e in edges for x in (e['source'], e['target'])}
        fields = ('id', 'ten', 'co_m1', 'chu', 'trang_thai_m1', 'mau', 'loai')
        nodes = [{**{k: op[k] for k in fields}, 'ngoai_service': op['chu'] != svc,
                  'don_vi_m1': {k: (op.get('don_vi_m1') or {}).get(k) for k in ('e_len', 'e_xuong')}} for op in d['thao_tac'] if op['id'] in ids]
        service.update(ban=meta, thao_tac=ops, nut=nodes, canh=edges)
        write(service_path, service)
    replay_path = directory / 'phat-lai' / (ca + '.json')
    replay = read(replay_path)
    replay.update(ban=meta, ranking_rows=rank, canh_xep_hang=d['canh_xep_hang'])
    write(replay_path, replay)
    return {'ban': name, 'ca': ca, 'flags_before': len(old['co_m1']), 'flags_after': len(flags),
            'payment_key_before': next(r['key'] for r in old['entity_ranking'] if r['entity'] == 'payment-service'),
            'payment_key_after': next(r['key'] for r in rank if r['entity'] == 'payment-service'),
            'H5_after': m['extra']['m1_ft']['chu_thich']['H5-liveness'], 'source': case['dau_ra'], 'source_sha256': case['sha256']}


def checker():
    spec = importlib.util.spec_from_file_location('l11_inherited_checker', R / 'codex/l8b-kiem.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.R = module.X.ROOT = R
    return module


def compare_bytes():
    changed = []
    for old in sorted((OLD / 'du-lieu').rglob('*')):
        if not old.is_file():
            continue
        rel = old.relative_to(OLD)
        if pin(old) != pin(R / rel):
            allowed = str(rel) == 'du-lieu/chi-muc-ban.json' or any(name in rel.parts and ('ebd5ef38' in rel.parts or old.name == 'ebd5ef38.json') for name in P['changed_variants'])
            assert allowed, ('unrelated data changed', str(rel))
            changed.append(str(rel))
    unchanged = []
    for ed in read(R / 'nguon/chi-muc-ban.json')['ban']:
        for case in ed['cac_ca']:
            if ed['ban'] in P['changed_variants'] and case['ca'] == 'ebd5ef38':
                continue
            rels = [pathlib.Path('du-lieu') / ed['ban'] / sub / (case['ca'] + '.json') for sub in ('', 'vue', 'phat-lai')]
            rels += [p.relative_to(OLD) for p in (OLD / 'du-lieu' / ed['ban'] / 'thao-tac-vue' / case['ca']).glob('*.json')]
            assert all(pin(OLD / rel) == pin(R / rel) for rel in rels)
            unchanged.append({'ban': ed['ban'], 'ca': case['ca'], 'files': len(rels), 'byte_identical': True})
    assert len(unchanged) == 82
    write(R / 'kiem/doi-chieu-byte.json', {'utc': now(), 'unchanged_slots': unchanged, 'changed_files': changed, 'old_files_checked': len(P['old_files'])})


def stage():
    stop()
    assert not R.exists() and not R.is_symlink(), 'new root exists'
    check_old()
    before = inventory()
    assert before['files'] == P['pinned_files'], 'provisioning changed since reception'
    before['targets'] = targets_current('before')
    R.mkdir()
    write(R / 'codex/payload.json', P)
    write(R / 'kiem/may-truoc.json', before)
    for folder in ('du-lieu', 'nguon'):
        shutil.copytree(OLD / folder, R / folder)
    for rel, encoded in P['files_b64'].items():
        target = R / rel
        assert target.is_relative_to(R)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(base64.b64decode(encoded))
    idx = read(R / 'nguon/chi-muc-ban.json')
    assert idx['phien_ban_chi_muc'] == 3
    assert pin(R / 'nguon/chi-muc-ban.json')['sha256'] == P['index3_sha256']
    changed = []
    for ed in idx['ban']:
        for case in ed['cac_ca']:
            if case['dau_ra']:
                assert pin(R / 'nguon' / ed['ban'] / case['ca'] / 'method-output-1.json')['sha256'] == case['sha256']
            if ed['ban'] in P['changed_variants'] and case['ca'] == 'ebd5ef38':
                changed.append(rebuild(ed, case))
    projected = read(R / 'du-lieu/chi-muc-ban.json')
    projected['phien_ban_chi_muc'] = 3
    write(R / 'du-lieu/chi-muc-ban.json', projected)
    write(R / 'kiem/hai-slot.json', changed)
    compare_bytes()
    k = checker()
    k.verify_export()
    k.verify_schema()
    check_old()
    assert inventory()['files'] == before['files'], 'stage modified provisioning'
    emit({'stage': 'passed', 'slots': 84, 'unchanged_slots': 82, 'changed': changed})


def replace_guarded(path, data, expected):
    stop()
    assert pin(path) == expected
    temp = R / 'kiem' / ('replace-' + str(time.time_ns()))
    temp.write_bytes(data)
    os.chmod(temp, path.stat().st_mode)
    assert pin(path) == expected
    os.replace(temp, path)


def deploy():
    stop()
    assert not (R / 'kiem/deploy.json').exists(), 'preserve previous deploy'
    read(R / 'kiem/kiem-xuat.json')
    before = inventory()
    assert before['files'] == P['pinned_files'], 'provisioning pin changed'
    before['targets'] = targets_current('before')
    write(R / 'kiem/truoc-ghi.json', before)
    changes = []
    for name, target in P['targets'].items():
        path = pathlib.Path(target['path'])
        data = (R / 'grafana' / name).read_bytes()
        assert digest(data) == target['after']
        backup = R / 'rollback' / name
        assert not backup.exists()
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(path.read_bytes())
        assert pin(backup) == target['before']
        replace_guarded(path, data, target['before'])
        record = {'file': str(path), 'before': target['before'], 'after': pin(path), 'backup': str(backup)}
        changes.append(record)
        emit({'event': 'replaced', **record})
        write(R / 'kiem/deploy-tien-do.json', changes)
    write(R / 'kiem/deploy.json', {'utc': now(), 'files': changes, 'restart': False})


def verify():
    stop()
    k = checker()
    k.ready()
    k.verify_api()
    # The dashboard's table has five visible columns; audit keys through the
    # same live Infinity URL using an extra read-only query, without changing UI.
    keys = []
    for name in P['changed_variants']:
        d = read(R / 'du-lieu' / name / 'ebd5ef38.json')
        dash = read(R / 'grafana/t065-l8b-rca.json')
        target = copy.deepcopy(next(p for p in dash['panels'] if p['id'] == 4)['targets'][0])
        count = max(len(row['key']) for row in d['ranking_rows'])
        fields = ','.join('"k%d":key[%d]' % (i, i) for i in range(count))
        target.update(refId='key_audit', root_selector='$$.([ranking_rows.{"entity":entity,' + fields + '}])',
                      columns=[{'selector': 'entity', 'text': 'entity', 'type': 'string'}] +
                      [{'selector': 'k%d' % i, 'text': 'k%d' % i, 'type': 'number'} for i in range(count)])
        answer = k.query([target], k.variables(d), d['cua_so_ms'])
        write(R / 'kiem/key-api' / (name + '.json'), answer)
        rows = k.frame_rows(answer['response'])['key_audit']
        lengths = {row['entity']: len(row['key']) for row in d['ranking_rows']}
        actual = [(row['entity'], [row.get('k%d' % i) for i in range(lengths[row['entity']])]) for row in rows]
        assert actual == [(row['entity'], row['key']) for row in d['ranking_rows']], ('API key', name)
        keys.append({'ban': name, 'rows': len(rows), 'passed': True})
    write(R / 'kiem/kiem-khoa-api.json', {'utc': now(), 'rows': keys, 'visible_table_has_key_column': False, 'evidence': 'read-only Infinity query on the dashboard source URL'})
    after = inventory()
    after['targets'] = targets_current('after')
    changed_paths = {target['path'] for target in P['targets'].values()}
    assert set(after['files']) == set(P['pinned_files'])
    for path, expected in P['pinned_files'].items():
        if path not in changed_paths:
            assert after['files'][path] == expected, ('other provisioning changed', path)
    assert after['machine'] == read(R / 'kiem/may-truoc.json')['machine']
    check_old()
    compare_bytes()
    write(R / 'kiem/may-sau.json', after)
    emit({'verify': 'passed', 'API_pages': 18, 'key_audits': len(keys), 'only_three_dashboard_files_changed': True, 'old_data_preserved': True, 'restart': False})


def rollback():
    stop()
    targets_current('after')
    for name, target in P['targets'].items():
        data = (R / 'rollback' / name).read_bytes()
        assert digest(data) == target['before']
        replace_guarded(pathlib.Path(target['path']), data, target['after'])
        emit({'event': 'restored', 'file': target['path'], **target['before']})


if 'P' not in globals():
    P = read(R / 'codex/payload.json')
stop()
action = sys.argv[1]
if action == 'stage':
    stage()
elif action == 'deploy':
    deploy()
elif action == 'verify':
    verify()
elif action == 'rollback':
    rollback()
else:
    raise ValueError(action)

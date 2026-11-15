"""Kiểm độc lập bộ xuất và kết quả Infinity; không chạy/chấm M1."""
import base64
import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

spec = importlib.util.spec_from_file_location('l8b_export', pathlib.Path(__file__).with_name('l8b-xuat.py'))
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)
R = X.ROOT
read, write, sha, now, stop = X.read, X.write, X.sha, X.now, X.stop


def assert_equal(actual, expected, message):
    assert actual == expected, message


def forbidden_keys(x):
    banned = {'phat_lai', 'root_khai_truoc', 'tap_chap_nhan', 'o_loi', 'thanh_phan_tiem', 'dap_an'}
    if isinstance(x, dict):
        return [k for k in x if k in banned] + [k for v in x.values() for k in forbidden_keys(v)]
    if isinstance(x, list):
        return [k for v in x for k in forbidden_keys(v)]
    return []


def verify_export():
    stop()
    idx = read(R / 'nguon/chi-muc-ban.json')
    rows, nlinks = [], 0
    for b in idx['ban']:
        for c in b['cac_ca']:
            stop()
            root = R / 'du-lieu' / b['ban']
            d = read(root / (c['ca'] + '.json'))
            assert d['phien_ban_dinh_dang'] == '0.5'
            assert isinstance(d['ranking_rows'], list) and isinstance(d['co_m1'], list)
            assert isinstance(d['services'], list) and len(d['services']) > 0
            assert_equal([x['ma'] for x in d['service_options']], d['services'], 'service scalar projection')
            assert all(isinstance(x['ma'], str) and isinstance(x['ten'], str) for x in d['service_options'])
            for key in ('ban', 'trang_thai', 'cau_hinh_sha256', 'ma_nguon_sha256'):
                assert_equal(d['ban'][key], b[key], ('metadata', b['ban'], c['ca'], key))
            assert_equal(d['ban']['cau_hinh_file_sha256'], b.get('cau_hinh_file_sha256'), 'config byte hash')
            assert d['ban']['nguon_output'] == c['dau_ra'] and d['ban']['sha256_output'] == c['sha256']
            assert not forbidden_keys(d), (b['ban'], c['ca'], 'answer key')
            assert d['cua_so_ms'][1] - d['cua_so_ms'][0] == 600000
            m = None
            if c['dau_ra']:
                p = R / 'nguon' / b['ban'] / c['ca'] / 'method-output-1.json'
                assert sha(p) == c['sha256']
                m = read(p)
                assert_equal(d['entity_ranking'], m['entity_ranking'], 'ranking source order/ties/key')
                assert_equal(d['co_m1'], m['extra']['kenh_co'], 'all flags')
                assert_equal(d['don_vi_m1'], m['extra']['don_vi_phan_vi'], 'all units with ns')
                assert_equal(d['canh_xep_hang'], m['extra'].get('m1_ft', {}).get('canh_xep_hang', []), 'edges order/rank')
                assert_equal(d['region'], m['region'], 'region')
                assert d['trang_thai_chay'] == m['status']
                assert_equal([d['cua_so_ms'][0] * 1000000, d['cua_so_ms'][1] * 1000000], [m['window']['N'][0], m['window']['A'][1]], 'ns boundaries')
                projected = [{k: r[k] for k in ('entity', 'key', 'tie_group')} for r in d['ranking_rows']]
                assert_equal(projected, m['entity_ranking'], 'display order')
                assert all(r['hang'] == r['tie_group'] + 1 for r in d['ranking_rows'])
                units = {u['ma']: u for u in m['extra']['don_vi_phan_vi']}
                op_flags = 0
                for o in d['thao_tac']:
                    key = 'op|' + o['chu'] + '|' + o['ten']
                    unit = units.get(key)
                    expected = [f for f in m['extra']['kenh_co'] if f['don_vi'] == key]
                    assert_equal(o['kenh_co'], expected, 'operation flags')
                    assert_equal(o['don_vi_m1'], unit, 'operation unit')
                    assert o['co_m1'] == bool(expected)
                    if unit:
                        assert_equal([o['mau_N'], o['mau_A']], [unit['n_N'], unit['n_A']], (b['ban'], c['ca'], o['ten'], 'samples'))
                    assert o['ban_kinh'] == 32
                    op_flags += len(expected)
                assert op_flags == sum(f['don_vi'].startswith('op|') for f in m['extra']['kenh_co']), 'lost operation flags'
                if b['ban'] in ('p7', 'V082-V066+H8a'):
                    assert d['trang_thai_canh'] == 'không có đầu ra cạnh'
            else:
                assert d['trang_thai_chay'] == 'LOI_CHAY' and d['loi_chay'] == c['loi_chay']
                assert d['ranking_rows'] == d['entity_ranking'] == d['co_m1'] == d['canh_xep_hang'] == d['thao_tac'] == []
                assert d['services'] == [X.EMPTY]
            links = [lk for o in d['thao_tac'] for lk in o.get('lien_ket', [])] + [lk for f in d['bang_chung'] for lk in f['lien_ket']] + d['metric_links']
            for lk in links:
                pane = json.loads(urllib.parse.parse_qs(urllib.parse.urlparse(lk['url']).query)['panes'][0])['a']
                q = pane['queries'][0]
                assert pane['datasource'] == lk['kho'] == q['datasource']['uid']
                assert (q.get('query') or q.get('expr')) == lk['truy_van']
                assert [int(pane['range']['from']), int(pane['range']['to'])] == [d['cua_so_ms'][0], d['cua_so_ms'][1] - 1]
                nlinks += 1
            vue = read(root / 'vue' / (c['ca'] + '.json'))
            for k, value in vue.items():
                assert_equal(value, d[k], 'vue projection ' + k)
            for svc in d['services']:
                s = read(root / 'thao-tac-vue' / c['ca'] / (svc + '.json'))
                assert_equal(s['thao_tac'], [o for o in d['thao_tac'] if o['chu'] == svc], 'service operations')
                own = {o['id'] for o in s['thao_tac']}
                assert_equal(s['canh'], [e for e in d['canh_thao_tac'] if e['source'] in own or e['target'] in own], 'service observed edges')
                assert len({o['id'] for o in s['nut']}) == len(s['nut'])
                node_ids = {o['id'] for o in s['nut']}
                assert all(e['source'] in node_ids and e['target'] in node_ids for e in s['canh'])
            replay = read(root / 'phat-lai' / (c['ca'] + '.json'))
            assert_equal(replay['ranking_rows'], d['ranking_rows'], 'replay ranks')
            if c['nguon'] != 't062':
                assert 'phat_lai' not in replay
            else:
                assert_equal(replay['phat_lai'], X.checked_old('p7/phat-lai/' + c['ca'] + '.json')['phat_lai'], 'replay original answers only')
            if c['nguon'] == 't062' and b['ban'] == 'p7':
                old = X.checked_old('p7/' + c['ca'] + '.json')
                assert_equal(d['thao_tac'], old['thao_tac'], 'T062 P7 operations regression')
                assert_equal(d['canh_thao_tac'], old['canh_thao_tac'], 'T062 P7 graph regression')
            rows.append({'ban': b['ban'], 'ca': c['ca'], 'status': d['trang_thai_chay'], 'ranking': len(d['ranking_rows']),
                         'flags': len(d['co_m1']), 'units': len(d['don_vi_m1']), 'edges': len(d['canh_xep_hang']),
                         'operations': len(d['thao_tac']), 'links': len(links), 'passed': True})
    result = {'utc': now(), 'status': 'dat', 'cases': len(rows), 'urls_decoded_once': nlinks, 'rows': rows,
              'totals': {k: sum(x[k] for x in rows) for k in ('ranking', 'flags', 'units', 'edges', 'operations')},
              'schema_version': '0.5', 'source_numbers_and_ns_preserved': True, 'T062_P7_regression': 9,
              'answer_keys_in_main': [], 'no_rescoring': True}
    write(R / 'kiem/kiem-xuat.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, ensure_ascii=False), flush=True)


def api(endpoint, body=None):
    # Không mở env file, không ghi/in credential. Chỉ lấy credential của container đã được Minh cấp.
    import subprocess
    ins = json.loads(subprocess.check_output(['docker', 'inspect', X.C]))[0]
    env = dict(s.split('=', 1) for s in ins['Config']['Env'] if '=' in s)
    auth = base64.b64encode((env.get('GF_SECURITY_ADMIN_USER', 'admin') + ':' + env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
    req = urllib.request.Request('http://10.0.0.215:3000' + endpoint,
                                 data=None if body is None else json.dumps(body, ensure_ascii=False).encode(),
                                 headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=55) as r:
            result = {'http': r.status, 'data': json.load(r)}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            raw = json.loads(raw)
        except ValueError:
            pass
        result = {'http': e.code, 'data': raw}
    def trim(x):
        if isinstance(x, dict):
            if isinstance(x.get('custom'), dict):
                x['custom'].pop('data', None)  # Infinity lặp lại tài liệu nguồn lớn ở metadata.
            for v in x.values():
                trim(v)
        elif isinstance(x, list):
            for v in x:
                trim(v)
    trim(result)
    return result


def frame_rows(response):
    assert response['http'] == 200, ('HTTP', response['http'])
    assert isinstance(response['data'], dict), 'response is not JSON object'
    out = {}
    for ref, r in response['data']['results'].items():
        assert not r.get('error'), (ref, r.get('error'))
        rows = []
        for f in r.get('frames', []):
            fields, values = f['schema']['fields'], f['data']['values']
            for i in range(len(values[0]) if values else 0):
                rows.append({field['name']: values[k][i] for k, field in enumerate(fields)})
        out[ref] = rows
    return out


def variables(d):
    svc = next((r['entity'] for r in d['ranking_rows'] if any(o['chu'] == r['entity'] for o in d['thao_tac'])), d['services'][0])
    ops = [o for o in d['thao_tac'] if o['chu'] == svc]
    op = next((o['id'] for o in ops if o['co_m1']), ops[0]['id'] if ops else X.EMPTY)
    return {'ban': d['ban']['ban'], 'ca': d['ca'], 'dv': svc, 'dv_svc': 'discovery-server' if svc == 'config-discovery' else svc,
            'op': op, 't_tu': d['tu_utc'], 't_den': X.iso(d['cua_so_ms'][1] - 1)}


def query(targets, values, w):
    rendered = []
    for target in targets:
        raw = json.dumps(target, ensure_ascii=False)
        for k, v in values.items():
            for suffix in ('', ':value', ':raw'):
                raw = raw.replace('${' + k + suffix + '}', str(v))
        t = json.loads(raw)
        assert '${' not in json.dumps(t), 'unexpanded target variable'
        t.update(intervalMs=15000, maxDataPoints=1000)
        rendered.append(t)
    request = {'from': str(w[0]), 'to': str(w[1] - 1), 'queries': rendered}
    return {'utc': now(), 'request': request, 'response': api('/api/ds/query', request)}


def panel_targets(panels):
    return [dict(t, refId=str(p['id']) + '_' + t['refId']) for p in panels for t in p.get('targets', []) if not t.get('hide')]


def verify_api():
    stop()
    idx = read(R / 'nguon/chi-muc-ban.json')
    dashboards, dashboard_api = {}, {}
    for uid in (X.UID, X.REPLAY):
        result = api('/api/dashboards/uid/' + uid)
        dashboard_api[uid] = result
        assert result['http'] == 200
        dashboards[uid] = result['data']['dashboard']
        source = read(R / 'grafana' / (uid + '.json'))
        for field in ('uid', 'title', 'templating', 'panels', 'time'):
            assert_equal(dashboards[uid][field], source[field], 'loaded dashboard ' + field)
    write(R / 'kiem/dashboard-api.json', dashboard_api)
    report = []
    for b in idx['ban']:
        for ca in ('86dea661', 'ebd5ef38', '00eaea92'):
            stop()
            d = read(R / 'du-lieu' / b['ban'] / (ca + '.json'))
            v, w = variables(d), d['cua_so_ms']
            for uid, dash in dashboards.items():
                slot_file = R / 'kiem/api-slots' / b['ban'] / ca / (uid + '.json')
                # Checkpoint theo slot. Chỉ dùng lại khi nguồn và dashboard/request không đổi.
                fingerprint = hashlib.sha256((sha(R / 'du-lieu' / b['ban'] / (ca + '.json')) + sha(R / 'grafana' / (uid + '.json'))).encode()).hexdigest()
                if slot_file.exists():
                    slot = read(slot_file)
                    assert slot['fingerprint'] == fingerprint
                    report.append(slot['summary'])
                    continue
                panel_ids = (3, 4, 5, 6, 7) if uid == X.REPLAY else (3, 4, 5, 6, 8, 9, 10, 21, 22, 23, 24, 25, 26, 28, 29)
                targets = panel_targets([p for p in dash['panels'] if p['id'] in panel_ids])
                answers, rows = [], {}
                for j in range(0, len(targets), 3):
                    answer = query(targets[j:j + 3], v, w)
                    answers.append(answer)
                    # Giữ response lỗi trước khi assert; không xóa lượt hỏng.
                    write(R / 'kiem/api-luot' / b['ban'] / ca / uid / (f'{j:02d}-{time.time_ns()}.json'), answer)
                    rows.update(frame_rows(answer['response']))
                def subset(ref, names):
                    return [[r.get(k) for k in names] for r in rows[ref]]
                assert_equal(subset('4_rank', ('entity', 'hang', 'tie_group', 'lop', 'so_kenh_co')),
                             [[r.get(k) for k in ('entity', 'hang', 'tie_group', 'lop', 'so_kenh_co')] for r in d['ranking_rows']], ('API ranks', b['ban'], ca))
                edge_fields = ('nguon', 'dich', 'loai', 'hang', 'tie_group', 'co', 'trang_thai', 'nguon_xac_minh')
                assert_equal(subset('6_edge_rank', edge_fields), [[e.get(k) for k in edge_fields] for e in d['canh_xep_hang']], 'API edge ranks')
                assert_equal(subset('5_edge_state', ('ket_qua',)), [[d['trang_thai_canh']]], 'API absent-edge explanation')
                meta = {x['a_truong']: x.get('b_gia_tri') for x in rows['3_meta']}
                for label, expected in [('Bản', b['ban']), ('Trạng thái bản', b['trang_thai']), ('Trạng thái chạy', d['trang_thai_chay']),
                                        ('Hash cấu hình (JSON chuẩn hóa)', b['cau_hinh_sha256'] or 'null — chỉ mục nguồn chưa cấp'),
                                        ('Hash byte file cấu hình', b.get('cau_hinh_file_sha256') or 'null — chỉ mục nguồn chưa cấp'),
                                        ('Hash mã nguồn', b['ma_nguon_sha256'] or 'null — chỉ mục nguồn chưa cấp'),
                                        ('Hash đầu ra', d['ban']['sha256_output'] or 'không có đầu ra'),
                                        ('Bắt đầu (bao gồm)', d['tu_utc']), ('Kết thúc (loại trừ)', d['den_loai_tru']),
                                        ('Lỗi chạy (nguồn)', d['loi_chay'] or 'không có')]:
                    assert_equal(meta[label], expected, ('API meta', label, b['ban'], ca))
                if uid == X.UID:
                    fields = ('ma', 'thuc_the', 'don_vi', 'ten', 'huong', 'lop', 'F_I')
                    assert_equal(subset('9_flags', fields), [[f.get(k) for k in fields] for f in d['co_m1']], 'API flags')
                    ops = [o for o in d['thao_tac'] if o['chu'] == v['dv']]
                    assert_equal(subset('22_ops', ('id', 'loai', 'trang_thai', 'co', 'len', 'xuong', 'mau_N', 'mau_A')),
                                 [[o['id'], o['loai'], o['trang_thai_m1'], 'có cờ M1' if o['co_m1'] else 'không có cờ M1', o['co_len'], o['co_xuong'], o['mau_N'], o['mau_A']] for o in ops], 'API operation flags/counts')
                    chosen = next((o for o in ops if o['id'] == v['op']), None)
                    link_fields = ('url', 'truy_van', 'pham_vi', 'ghi_chu')
                    assert_equal(subset('25_oplinks', link_fields), [[l.get(k) for k in link_fields] for l in (chosen['lien_ket'] if chosen else [])], 'API operation evidence links')
                variable_targets = [dict(var['query']['infinityQuery'], refId=var['name'] + '_v') for var in dash['templating']['list'] if var['type'] == 'query']
                var_rows, var_answers = {}, []
                for j in range(0, len(variable_targets), 3):
                    answer = query(variable_targets[j:j + 3], v, w)
                    var_answers.append(answer)
                    write(R / 'kiem/api-luot' / b['ban'] / ca / uid / (f'vars-{j:02d}-{time.time_ns()}.json'), answer)
                    var_rows.update(frame_rows(answer['response']))
                assert_equal([x['__value'] for x in var_rows['ban_v']], [b['ban'] for b in idx['ban']], 'version variable')
                assert_equal([x['__value'] for x in var_rows['ca_v']], [c['ca'] for c in b['cac_ca']], 'case variable')
                assert_equal([x['__value'] for x in var_rows['dv_v']], d['services'], 'service fallback variable')
                assert_equal(var_rows['t_tu_v'][0]['v'], d['tu_utc'], 'ISO from variable')
                assert_equal(var_rows['t_den_v'][0]['v'], X.iso(w[1] - 1), 'ISO to variable')
                summary = {'ban': b['ban'], 'ca': ca, 'uid': uid, 'service': v['dv'], 'op': v['op'], 'window_ms': w,
                           'rank_rows': len(d['ranking_rows']), 'flag_rows': len(d['co_m1']), 'edges': len(d['canh_xep_hang']),
                           'targets': len(targets), 'variables': len(variable_targets), 'passed': True}
                slot = {'utc': now(), 'fingerprint': fingerprint, 'summary': summary, 'panels': answers, 'variables': var_answers}
                write(slot_file, slot)
                report.append(summary)
                print(json.dumps({'api_slot': [b['ban'], ca, uid], 'passed': True}), flush=True)
    write(R / 'kiem/kiem-api.json', {'utc': now(), 'status': 'dat', 'pages': len(report), 'rows': report,
                                    'minimum_three_cases_per_variant': True, 'cases': ['86dea661', 'ebd5ef38', '00eaea92'],
                                    'evidence': 'api-slots và api-luot; query/data API, không phải thao tác UI thật'})


def verify_schema():
    from jsonschema import Draft202012Validator
    schema = read(R / 'dinh-dang/0.5/ca.schema.json')
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    rows = []
    for b in read(R / 'nguon/chi-muc-ban.json')['ban']:
        for c in b['cac_ca']:
            p = R / 'du-lieu' / b['ban'] / (c['ca'] + '.json')
            validator.validate(read(p))
            rows.append({'file': str(p.relative_to(R)), 'passed': True})
    write(R / 'kiem/kiem-schema.json', {'utc': now(), 'schema_sha256': sha(R / 'dinh-dang/0.5/ca.schema.json'),
                                      'schema': 'dinh-dang/0.5/ca.schema.json', 'passed': len(rows), 'rows': rows})
    print(json.dumps({'schema_validated': len(rows)}))


def ready():
    for attempt in range(3):
        records = {}
        ok = True
        for uid in (X.UID, X.REPLAY):
            answer = api('/api/dashboards/uid/' + uid)
            records[uid] = answer
            if answer['http'] != 200:
                ok = False
                continue
            current = answer['data']['dashboard']
            source = read(R / 'grafana' / (uid + '.json'))
            ok = ok and current['templating'] == source['templating'] and current['panels'] == source['panels']
        write(R / 'kiem/nap-dashboard' / (str(time.time_ns()) + '.json'), records)
        if ok:
            print(json.dumps({'dashboard_ready': True, 'attempt': attempt + 1}))
            return
        if attempt < 2:
            time.sleep(10)
    raise AssertionError('new dashboard definition not loaded after three reads')


def response_state(response):
    payload = response.get('data') if isinstance(response.get('data'), dict) else {}
    errors = [r['error'] for r in payload.get('results', {}).values() if r.get('error')]
    n = sum(max((len(v) for v in f.get('data', {}).get('values', [])), default=0)
            for r in payload.get('results', {}).values() for f in r.get('frames', []))
    return ('loi' if response['http'] != 200 or errors else 'co_du_lieu' if n else 'rong'), n, errors


def verify_links():
    stop()
    idx = read(R / 'nguon/chi-muc-ban.json')
    rows, new_requests = [], 0
    for b in idx['ban']:
        for ca in ('86dea661', '659a9dfb1ab0', 'ebd5ef38', '00eaea92'):
            d = read(R / 'du-lieu' / b['ban'] / (ca + '.json'))
            if d['trang_thai_chay'] == 'LOI_CHAY':
                rows.append({'ban': b['ban'], 'ca': ca, 'state': 'loi_chay_khong_dung_lien_ket', 'queries': 0})
                continue
            links = [lk for o in d['thao_tac'] for lk in o.get('lien_ket', [])] + d['metric_links']
            for kho in ('tempo', 'loki', 'prometheus'):
                stop()
                link = next(lk for lk in links if lk['kho'] == kho)
                pane = json.loads(urllib.parse.parse_qs(urllib.parse.urlparse(link['url']).query)['panes'][0])['a']
                request = {'from': pane['range']['from'], 'to': pane['range']['to'],
                           'queries': [dict(pane['queries'][0], intervalMs=15000, maxDataPoints=1000)]}
                key = hashlib.sha256(json.dumps(request, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
                cache = R / 'kiem/link-requests' / (key + '.json')
                reused = cache.exists()
                if reused:
                    answer = read(cache)
                    assert_equal(answer['request'], request, 'reuse only identical request/window')
                else:
                    answer = {'utc': now(), 'request': request, 'response': api('/api/ds/query', request)}
                    write(cache, answer)
                    new_requests += 1
                state, n, errors = response_state(answer['response'])
                rows.append({'ban': b['ban'], 'ca': ca, 'kho': kho, 'link': link, 'request_key': key,
                             'response_file': str(cache.relative_to(R)), 'reused_identical_request': reused,
                             'utc': answer['utc'], 'http': answer['response']['http'], 'state': state, 'rows': n, 'errors': errors,
                             'bam_that': False})
                write(R / 'kiem/kiem-links.json', {'utc': now(), 'status': 'dang_kiem', 'new_requests': new_requests, 'rows': rows})
                assert state != 'loi', (b['ban'], ca, kho, errors)
    write(R / 'kiem/kiem-links.json', {'utc': now(), 'status': 'dat', 'new_requests': new_requests,
                                     'samples': sum('kho' in x for x in rows), 'rows': rows,
                                     'note': 'Bản dùng lại có request/query/window giống hệt; không gọi là truy vấn mới hoặc bấm thật. Rỗng chỉ là không khớp truy vấn ở kho tại giờ ghi, không xác định nguyên nhân.'})
    print(json.dumps({'link_samples': sum('kho' in x for x in rows), 'new_requests': new_requests,
                      'states': {s: sum(x.get('state') == s for x in rows) for s in ('co_du_lieu', 'rong')}}), flush=True)


def live_snapshot():
    """Chỉ thêm snapshot cho service/ca mẫu; phần khác tiếp tục ghi chưa truy vấn."""
    stop()
    dash = read(R / 'grafana' / (X.UID + '.json'))
    panels = [p for p in dash['panels'] if p['id'] in (31, 32, 33, 34, 35)]
    report = []
    for ca in ('86dea661', '659a9dfb1ab0', 'ebd5ef38', '00eaea92'):
        d = read(R / 'du-lieu/V082-V066+H8a' / (ca + '.json'))
        v = variables(d)
        dst = R / 'du-lieu/trang-thai' / ca / (v['dv'] + '.json')
        slot = R / 'kiem/live-slots' / ca / (v['dv'] + '.json')
        if slot.exists():
            saved = read(slot)
            assert saved['window_ms'] == d['cua_so_ms'] and saved['variables'] == v
            report.append(saved['summary'])
            continue
        targets = panel_targets(panels)
        answers, entries = [], []
        for j in range(0, len(targets), 2):
            stop()
            answer = query(targets[j:j + 2], v, d['cua_so_ms'])
            write(R / 'kiem/live-luot' / ca / (str(time.time_ns()) + '.json'), answer)
            answers.append(answer)
            for ref, result in answer['response'].get('data', {}).get('results', {}).items():
                one = {'http': answer['response']['http'], 'data': {'results': {ref: result}}}
                state, n, errors = response_state(one)
                p = next(p for p in panels if str(p['id']) == ref.split('_', 1)[0])
                target = next(q for q in answer['request']['queries'] if q['refId'] == ref)
                entries.append({'panel': p['id'], 'kho': target['datasource']['uid'], 'trang_thai': state, 'so_dong': n,
                                'utc': answer['utc'], 'tu_utc': d['tu_utc'], 'den_loai_tru': d['den_loai_tru'],
                                'loi': '; '.join(errors), 'dien_giai': {'co_du_lieu': 'Có dữ liệu khớp truy vấn trong cửa sổ; số dòng có thể bị giới hạn.',
                                'rong': 'API thành công, không có dữ liệu khớp truy vấn tại kho ở giờ ghi; chưa xác định nguyên nhân.',
                                'loi': 'Lỗi API, không diễn giải dữ liệu.'}[state], 'request': target})
                assert state != 'loi', (ca, p['id'], errors)
        entries.sort(key=lambda x: x['panel'])
        assert [e['panel'] for e in entries] == [31, 32, 33, 34, 35]
        previous = read(dst)
        write(R / 'kiem/live-truoc' / ca / (v['dv'] + '.json'), previous)
        write(dst, {'queries': entries, 'window': [d['cua_so_ms'][0], d['cua_so_ms'][1] - 1]})
        panel = next(p for p in dash['panels'] if p['id'] == 28)
        shown = query(panel_targets([panel]), v, d['cua_so_ms'])
        write(R / 'kiem/live-panel28' / (ca + '.json'), shown)
        f = frame_rows(shown['response'])['28_query_state']
        fields = ('panel', 'kho', 'trang_thai', 'so_dong', 'utc', 'tu_utc', 'den_loai_tru', 'loi')
        assert_equal([[x.get(k) for k in fields] for x in f], [[x.get(k) for k in fields] for x in entries], 'snapshot table API')
        summary = {'ca': ca, 'service': v['dv'], 'queries': len(entries), 'states': {s: sum(e['trang_thai'] == s for e in entries) for s in ('co_du_lieu', 'rong', 'loi')}, 'snapshot_table_api_match': True}
        write(slot, {'utc': now(), 'window_ms': d['cua_so_ms'], 'variables': v, 'responses': answers, 'entries': entries, 'panel28': shown, 'summary': summary})
        report.append(summary)
        print(json.dumps({'live_snapshot': summary}, ensure_ascii=False), flush=True)
    write(R / 'kiem/kiem-live.json', {'utc': now(), 'status': 'dat', 'rows': report,
                                    'other_services': 'Giữ snapshot cũ có giờ nguồn hoặc chua_truy_van, không suy hiện trạng từ raw.'})


if __name__ == '__main__':
    if sys.argv[1] == 'export':
        verify_export()
    elif sys.argv[1] == 'api':
        verify_api()
    elif sys.argv[1] == 'schema':
        verify_schema()
    elif sys.argv[1] == 'ready':
        ready()
    elif sys.argv[1] == 'links':
        verify_links()
    elif sys.argv[1] == 'live':
        live_snapshot()
    else:
        raise SystemExit('unknown action')

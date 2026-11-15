"""L8: xuất bản chỉ mục 2; không chạy/chấm/sửa M1. Chạy trên exp-obs.

Chỉ ghi dưới ROOT mới và hai file provisioning mới. JSON dùng số nguyên Python
để giữ nguyên ns; hạng, cờ và cạnh được sao nguyên từ method-output.
"""
import base64
import copy
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001')
OLD = ROOT.parent / 't065-l4-001'
PROVISION = pathlib.Path('/opt/flash-ticket-obs/pinned/provisioning/dashboards')
UID = 't065-l8b-rca'
REPLAY = 't065-l8b-phat-lai'
URL = 'http://localhost:3000/public/rca/t065-l8b-001/du-lieu'
C = 'flash-ticket-obs-grafana'
EMPTY = '__khong_co__'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(p):
    h = hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))


def write(p, obj):
    p = pathlib.Path(p)
    assert p.is_relative_to(ROOT), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')


def stop():
    assert not pathlib.Path('/home/ubuntu/rca-dieu-phoi/STOP').exists(), 'STOP remote'


def iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def inventory():
    ins = json.loads(subprocess.check_output(['docker', 'inspect', C]))[0]
    files = {}
    pinned = pathlib.Path('/opt/flash-ticket-obs/pinned')
    for p in [pinned / 'compose.json', *sorted((pinned / 'provisioning').rglob('*')),
              *sorted(OLD.rglob('*')), *sorted((ROOT.parent / 't065-l3-001').rglob('*'))]:
        if p.is_file():
            files[str(p)] = {'sha256': sha(p), 'bytes': p.stat().st_size}
    return {'utc': now(), 'files': files, 'machine': {
        'started_at': ins['State']['StartedAt'], 'restart_count': ins['RestartCount'],
        'memory_limit': ins['HostConfig']['Memory'], 'status': ins['State']['Status'],
        'stop': pathlib.Path('/home/ubuntu/rca-dieu-phoi/STOP').exists(),
        'stats': subprocess.check_output(['docker', 'stats', '--no-stream', '--format', '{{json .}}', C], text=True).strip()}}


def checked_old(rel):
    m = read(ROOT / 'nguon/manifest-T065-truoc.json')['files']
    p = OLD / rel
    expected = m['du-lieu-l4/' + rel]
    assert sha(p) == expected['sha256'] and p.stat().st_size == expected['bytes'], str(p)
    return read(p)


def evidence(kho, query, window, scope, note):
    q = {'refId': 'A', 'datasource': {'type': kho, 'uid': kho}}
    if kho == 'tempo':
        q.update(queryType='traceql', query=query, limit=50, tableType='traces')
    elif kho == 'loki':
        q.update(expr=query, queryType='range', maxLines=200)
    else:
        q.update(expr=query, range=True)
    pane = {'a': {'datasource': kho, 'queries': [q], 'range': {'from': str(window[0]), 'to': str(window[1] - 1)}}}
    encoded = urllib.parse.quote(json.dumps(pane, ensure_ascii=False, separators=(',', ':')), safe='')
    return {'kho': kho, 'loai': {'tempo': 'trace_tim_kiem', 'loki': 'log', 'prometheus': 'metric'}[kho],
            'cach_lay': 'dan_xuat', 'truy_van': query, 'cua_so_ms': window, 'pham_vi': scope,
            'ghi_chu': note, 'url': '/explore?schemaVersion=1&orgId=1&panes=' + encoded}


def attrs(values):
    return {x['key']: next(iter(x.get('value', {}).values()), None) for x in values}


def normalized_id(value, length, root=False):
    # Cùng hợp đồng adapter_flashticket.hex_id; OTLP của gói dùng hex, không base64.
    if root and (value is None or value == '' or value == '0' * length):
        return ''
    assert isinstance(value, str) and re.fullmatch('[a-fA-F0-9]{' + str(length) + '}', value), value
    assert value != '0' * length, value
    return value.lower()


def op_id(owner, operation):
    raw = json.dumps([owner, operation], ensure_ascii=False, separators=(',', ':')).encode()
    return 'o' + hashlib.sha256(raw).hexdigest()[:20]


def dev3_template(ca, w):
    """Dựng lớp trình bày từ OTLP theo miền/alias/parent của P7; không tính điểm."""
    stop()
    src = pathlib.Path('/opt/flash-ticket-rca/cases') / ca
    manifest = read(src / 'manifest.json')
    assert [x * 1000 for x in manifest['method_window_seconds']] == w, ca
    proof = {'ca': ca, 'manifest_file': str(src / 'manifest.json'), 'manifest_sha256': sha(src / 'manifest.json'),
             'window_ms': w, 'files': {}, 'source': 'manifest của gói ca hiện có trên exp-obs; không tải raw'}
    for name in ('inventory.json', 'raw-traces.jsonl', 'raw-logs.jsonl', 'prometheus.json'):
        p = src / name
        expected = manifest['files'][name]
        actual = sha(p)
        assert actual == expected['sha256'] and p.stat().st_size == expected['bytes'], str(p)
        proof['files'][name] = {'file': str(p), 'sha256': actual, 'bytes': p.stat().st_size}
    write(ROOT / 'nguon-dev3' / ca / 'manifest.json', manifest)
    aliases = {'discovery-server': 'config-discovery'}
    spans, rawmeta = {}, {}
    raw_links = 0
    lo, hi, t = w[0] * 1000000, w[1] * 1000000, (w[0] + 300000) * 1000000
    duplicates = 0
    with (src / 'raw-traces.jsonl').open() as f:
        for line in f:
            if not line.strip():
                continue
            for rs in json.loads(line).get('resourceSpans', []):
                svc = attrs(rs.get('resource', {}).get('attributes', []))['service.name']
                owner = aliases.get(svc, svc)
                for scope in rs.get('scopeSpans', []):
                    for raw in scope.get('spans', []):
                        st, en = int(raw['startTimeUnixNano']), int(raw['endTimeUnixNano'])
                        assert en >= st
                        if st < lo or en >= hi:
                            continue
                        a = attrs(raw.get('attributes', []))
                        tid, sid = normalized_id(raw['traceId'], 32), normalized_id(raw['spanId'], 16)
                        parent = normalized_id(raw.get('parentSpanId'), 16, root=True)
                        row = {'traceID': tid, 'spanID': sid, 'parentSpanID': parent, 'owner': owner,
                               'operation': raw['name'], 'start_us': st // 1000, 'duration_us': en // 1000 - st // 1000}
                        # Ap dụng lần cắt của chuoi.py trên số us đã chuẩn hóa.
                        if row['start_us'] * 1000 < lo or (row['start_us'] + row['duration_us']) * 1000 >= hi:
                            continue
                        key = (tid, sid)
                        if key in spans:
                            assert spans[key] == row, ('duplicate conflict', ca, key)
                            duplicates += 1
                            continue
                        spans[key] = row
                        kind = ('message' if a.get('messaging.system') or raw.get('kind') in (4, 5)
                                else 'SQL/cache' if a.get('db.system') or a.get('db.system.name')
                                else 'HTTP' if any(k.startswith('http.') for k in a)
                                else 'job' if re.search('scheduling|quartz', scope.get('scope', {}).get('name', '')) else 'khac')
                        rawmeta[key] = {'service': svc, 'kind': kind, 'attrs': a}
                        raw_links += len(raw.get('links', []))
    children = {k: [] for k in spans}
    for k, s in spans.items():
        parent = (s['traceID'], s['parentSpanID'])
        if parent in spans:
            children[parent].append(k)
    groups, edges = {}, {}
    orphan = roots = wrappers = 0
    for key, s in sorted(spans.items(), key=lambda x: (x[1]['start_us'], *x[0])):
        parent = (s['traceID'], s['parentSpanID'])
        is_orphan = bool(s['parentSpanID']) and parent not in spans
        is_root = not s['parentSpanID']
        wrapper = len(children[key]) == 1 and spans[children[key][0]]['owner'] != s['owner'] and parent in spans and spans[parent]['owner'] == s['owner']
        orphan += is_orphan
        roots += is_root
        wrappers += wrapper
        oid = op_id(s['owner'], s['operation'])
        phase = 'A' if (s['start_us'] + s['duration_us']) * 1000 >= t else 'N'
        if oid not in groups:
            groups[oid] = {'id': oid, 'chu': s['owner'], 'ten': s['operation'], 'types': set(), 'routes': set(),
                           'n_N': 0, 'n_A': 0, 'mau_N': 0, 'mau_A': 0, 'span_boc': 0, 'mo_coi': 0,
                           'goc': 0, 'dich_quan_sat': set(), 'vi_du': [], 'service': rawmeta[key]['service']}
        g = groups[oid]
        g['n_' + phase] += 1
        g['mau_' + phase] += not wrapper  # P7 E1-U bỏ mẫu span bọc.
        g['span_boc'] += wrapper
        g['mo_coi'] += is_orphan
        g['goc'] += is_root
        g['types'].add(rawmeta[key]['kind'])
        a = rawmeta[key]['attrs']
        method = a.get('http.request.method', a.get('http.method'))
        if a.get('http.route') and method:
            g['routes'].add((rawmeta[key]['service'], method, a['http.route']))
        if a.get('server.address'):
            g['dich_quan_sat'].add(a['server.address'])
        if len(g['vi_du']) < 3:
            g['vi_du'].append({'trace_id': s['traceID'], 'span_id': s['spanID'], 'parent_span_id': s['parentSpanID'], 'phia': phase})
        if parent in spans:
            p = spans[parent]
            pid = op_id(p['owner'], p['operation'])
            eid = pid + '->' + oid
            e = edges.setdefault(eid, {'id': eid, 'source': pid, 'target': oid, 'loai': 'span_cha_con', 'so_quan_he': 0, 'so_N': 0, 'so_A': 0, 'vi_du': []})
            e['so_quan_he'] += 1
            e['so_' + phase] += 1
            if len(e['vi_du']) < 3:
                e['vi_du'].append({'trace_id': s['traceID'], 'cha_span_id': p['spanID'], 'con_span_id': s['spanID']})
    logs = set()
    with (src / 'raw-logs.jsonl').open() as f:
        for line in f:
            if not line.strip():
                continue
            for rs in json.loads(line).get('resourceLogs', []):
                svc = attrs(rs.get('resource', {}).get('attributes', []))['service.name']
                if any(lo <= int(r.get('timeUnixNano') or r.get('observedTimeUnixNano') or 0) < hi
                       for scope in rs.get('scopeLogs', []) for r in scope.get('logRecords', [])):
                    logs.add(svc)
    for g in groups.values():
        svc = g.pop('service')
        g['loai'] = ', '.join(sorted(g.pop('types')))
        g['dich_quan_sat'] = sorted(g['dich_quan_sat'])
        g['lien_ket'] = [evidence('tempo', '{ resource.service.name = ' + json.dumps(svc) + ' && name = ' + json.dumps(g['ten']) + ' }', w,
                                  'tim_span_thao_tac', 'Owner/tên thao tác quan sát từ raw trace đã kiểm hash; không phải trace M1 chọn.')]
        if svc in logs:
            g['lien_ket'].append(evidence('loki', '{service_name=' + json.dumps(svc) + '}', w, 'ngu_canh_service', 'Service có log trong cửa sổ raw đã băm; không khẳng định log do thao tác phát.'))
        routes = g.pop('routes')
        for service, method, route in sorted(routes):
            query = 'sum by (http_request_method,http_route) (rate(http_server_request_duration_seconds_count{service_name=' + json.dumps(service) + ',http_request_method=' + json.dumps(method) + ',http_route=' + json.dumps(route) + '}[1m]))'
            g['lien_ket'].append(evidence('prometheus', query, w, 'route_http_quan_sat', 'Route/method quan sát từ raw span đã băm.'))
        g['ly_do_khong_prometheus'] = None if routes else 'Không có cặp http.route/method trong raw span; không dựng metric từ tên thao tác.'
    metrics = []
    metric_sources = [src / 'prometheus.json', pathlib.Path('/opt/rca-m1ft/bo-sung-dev3') / ca / 'prometheus-bo-sung.json']
    for p in metric_sources:
        if not p.exists():
            continue
        doc = read(p)
        write(ROOT / 'nguon-dev3' / ca / p.name, doc)
        proof['files'][p.name] = {'file': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
        # Hợp đồng gói metric: danh sách bundle {query,result}; không đoán biểu thức.
        bundles = doc if isinstance(doc, list) else doc.get('queries', doc.get('bundles', []))
        if isinstance(bundles, dict):
            bundles = list(bundles.values())
        for q in bundles:
            if isinstance(q, dict) and q.get('query') and q.get('result'):
                metrics.append(evidence('prometheus', q['query'], w, 'truy_van_metric_da_luu', 'Truy vấn nguyên văn gói metric có dữ liệu đã lưu; có thể gồm nhiều service.'))
    result = {'thao_tac': list(groups.values()), 'canh_thao_tac': list(edges.values()), 'metric_links': metrics,
              'quan_he': {'da_ho_tro': ['span_cha_con'], 'span_link': {'trang_thai': 'chua_ho_tro', 'so_link_raw': raw_links}},
              'tien_xu_ly': {'so_span': len(spans), 'bo_lap': 0, 'mo_coi': orphan, 'goc': roots, 'span_boc': wrappers, 'he_span': 1000},
              'gioi_han': 'Trace/log/metric có nguồn đã băm trên exp-obs. Log là ngữ cảnh service. Span link chưa hỗ trợ. Các panel sống phụ thuộc retention; nguồn raw có không bảo đảm kho hiện tại còn dữ liệu.'}
    proof.update(spans=len(spans), duplicate_raw=duplicates, operations=len(groups), operation_edges=len(edges), metric_links=len(metrics), log_services=sorted(logs))
    write(ROOT / 'cache-dev3' / (ca + '.json'), result)
    proof['cache_sha256'] = sha(ROOT / 'cache-dev3' / (ca + '.json'))
    write(ROOT / 'kiem/dev3' / (ca + '.json'), proof)
    print(json.dumps({'utc': now(), 'dev3_done': ca, 'spans': len(spans), 'ops': len(groups)}, ensure_ascii=False), flush=True)
    return result


def export():
    stop()
    index_file = ROOT / 'nguon/chi-muc-ban.json'
    assert sha(index_file) == '7e4278d6fbf1ae124da865780642304e459869d3d239787615fefed66fb12b0b'
    idx = read(index_file)
    assert idx['phien_ban_chi_muc'] == 2 and len(idx['ban']) == 3
    outputs, windows = {}, {}
    for b in idx['ban']:
        assert len(b['cac_ca']) == 28
        for c in b['cac_ca']:
            p = ROOT / 'nguon' / b['ban'] / c['ca'] / 'method-output-1.json'
            if c['dau_ra'] is not None:
                assert sha(p) == c['sha256'], str(p)
                m = read(p)
                outputs[(b['ban'], c['ca'])] = m
                assert m['window']['don_vi'] == 'ns'
                assert m['window']['N'][1] == m['window']['A'][0]
                w = [m['window']['N'][0] // 1000000, m['window']['A'][1] // 1000000]
                assert w[1] - w[0] == 600000
                assert c['ca'] not in windows or windows[c['ca']] == w
                windows[c['ca']] = w
                if b['ban'] != 'p7':
                    for k in ('cau_hinh_sha256', 'ma_nguon_sha256'):
                        assert m['extra']['m1_ft'][k] == b[k]
            else:
                assert c['loi_chay'] and read(ROOT / 'nguon' / b['ban'] / c['ca'] / 'loi-chay.json')['status'] == 'ERROR'
    assert len(outputs) == 83 and len(windows) == 28
    templates = {}
    for c in idx['ban'][0]['cac_ca']:
        stop()
        if c['nguon'] != 'dev3':
            templates[c['ca']] = checked_old('p7/' + c['ca'] + '.json')
        else:
            cache = ROOT / 'cache-dev3' / (c['ca'] + '.json')
            if cache.exists():
                proof = read(ROOT / 'kiem/dev3' / (c['ca'] + '.json'))
                assert sha(cache) == proof['cache_sha256'], str(cache)
                assert proof['window_ms'] == windows[c['ca']]
                for p in proof['files'].values():
                    assert sha(p['file']) == p['sha256'], p['file']
                templates[c['ca']] = read(cache)
            else:
                templates[c['ca']] = dev3_template(c['ca'], windows[c['ca']])
    comparisons, all_links, variants = [], [], []
    for b in idx['ban']:
        cases = []
        for c in b['cac_ca']:
            stop()
            ca = c['ca']
            w = windows[ca]
            m = outputs.get((b['ban'], ca))
            d = copy.deepcopy(templates[ca]) if m else {'thao_tac': [], 'canh_thao_tac': [], 'metric_links': []}
            meta = {k: b[k] for k in ('ban', 'mo_ta', 'trang_thai', 'cau_hinh_sha256', 'ma_nguon_sha256')}
            meta['cau_hinh_file_sha256'] = b.get('cau_hinh_file_sha256')
            meta.update(nguon_output=c['dau_ra'], sha256_output=c['sha256'], loi_chay=c.get('loi_chay'),
                        ghi_chu_hash='Hai hash cấp bản P7 chưa được chỉ mục cấp (null); không suy ra.' if b['ban'] == 'p7' else 'Hash do chỉ mục T-064 cấp.')
            run_state = m['status'] if m else 'LOI_CHAY'
            flags = m['extra'].get('kenh_co', []) if m else []
            units = m['extra'].get('don_vi_phan_vi', []) if m else []
            umap = {u['ma']: u for u in units}
            rank = [{**r, 'hang': r['tie_group'] + 1, 'lop': m.get('classes', {}).get(r['entity']),
                     'so_kenh_co': sum(f['thuc_the'] == r['entity'] for f in flags)} for r in m['entity_ranking']] if m else []
            er = m['extra'].get('m1_ft', {}).get('canh_xep_hang') if m else None
            edge_state = ('không có đầu ra phương pháp — lỗi chạy' if m is None else
                          'không có đầu ra cạnh' if er is None else f'{len(er)} dòng cạnh từ extra.m1_ft.canh_xep_hang; không xếp lại')
            for op in d['thao_tac']:
                unit = umap.get('op|' + op['chu'] + '|' + op['ten'])
                of = [f for f in flags if f['don_vi'] == 'op|' + op['chu'] + '|' + op['ten']]
                state = unit['trang_thai'] if unit else 'KHONG_CHAM_SPAN_BOC'
                op.update(trang_thai_m1=state, co_len=unit.get('F_raw_len', 0) if unit else 0,
                          co_xuong=unit.get('F_raw_xuong', 0) if unit else 0, co_m1=bool(of), so_kenh_co=len(of),
                          kenh_co=of, don_vi_m1=unit, mau='#E02F44' if of else '#8E8E8E' if state == 'OK' else '#CA95E5', ban_kinh=32)
            if m and c['nguon'] == 'dev3':
                diag = d['tien_xu_ly']
                for k in ('so_span', 'bo_lap', 'mo_coi', 'goc', 'span_boc'):
                    assert diag[k] == m['diagnostics']['span'][k], (b['ban'], ca, k, diag[k], m['diagnostics']['span'][k])
            old_e = {x['id']: x.get('lien_ket', []) for x in d.get('bang_chung', [])}
            def flag_links(f):
                if f['ma'] in old_e:
                    return copy.deepcopy(old_e[f['ma']])
                found = [op for op in d['thao_tac'] if op['chu'] == f['thuc_the'] and
                         (not f['don_vi'].startswith('op|') or f['don_vi'] == 'op|' + op['chu'] + '|' + op['ten'])]
                result, seen = [], set()
                for op in found:
                    for lk in op.get('lien_ket', []):
                        if lk['url'] not in seen:
                            seen.add(lk['url'])
                            result.append(copy.deepcopy(lk))
                return result
            d['bang_chung'] = [{'id': f['ma'], 'don_vi': f['don_vi'], 'thuc_the': f['thuc_the'], 'kenh': f['ten'],
                               'huong': f['huong'], 'lop': f['lop'], 's': f['s'], 'F_I': f['F_I'], 'khoi_phat_ns': f.get('khoi_phat'),
                               'lien_ket': flag_links(f)} for f in flags]
            if not m:
                d['gioi_han'] = 'P7 lỗi chạy, không có đầu ra phương pháp và không dựng hạng/cờ. Cửa sổ ca chỉ dùng điều hướng, lấy từ đầu ra V082 cùng ca đã kiểm hash; không phải đầu ra của P7.'
            d.update(phien_ban_dinh_dang='0.5', ban=meta, ca=ca, nguon_ca=c['nguon'], cua_so_ms=w, tu_utc=iso(w[0]), den_loai_tru=iso(w[1]),
                     trang_thai_chay=run_state, loi_chay=c.get('loi_chay'), nguon_cua_so=(c['dau_ra'] or next(x['dau_ra'] for x in idx['ban'][1]['cac_ca'] if x['ca'] == ca)),
                     su_co={'ma': ca, 'ket_luan': m['verdict'] if m else None, 'trang_thai': run_state,
                            'cua_so_nen': {'tu_ms': w[0], 'den_ms': w[0] + 300000}, 'cua_so_su_co': {'tu_ms': w[0] + 300000, 'den_ms': w[1]}},
                     entity_ranking=m['entity_ranking'] if m else [], ranking_rows=rank, canh_xep_hang=er if er is not None else [], trang_thai_canh=edge_state,
                     co_m1=flags, don_vi_m1=units, region=m.get('region') if m else None, classes=m.get('classes') if m else {}, ke_thua=m.get('inherited_by') if m else [])
            for k in ('xep_hang', 'do_phu', 'vung', 'canh', 'giai_thich_ke_thua', 'nut', 'nguon'):
                d.pop(k, None)
            if m:
                meta.update(method_version=m['method_version'], config_id=m['config_id'], variant=m['variant'])
            services = list(dict.fromkeys([r['entity'] for r in rank] + [o['chu'] for o in d['thao_tac']])) or [EMPTY]
            d['services'] = services
            d['service_options'] = [{'ma': svc, 'ten': '(Không có đầu ra — lỗi chạy)' if svc == EMPTY else svc} for svc in services]
            write(ROOT / 'du-lieu' / b['ban'] / (ca + '.json'), d)
            vue_keys = ('ban', 'ca', 'cua_so_ms', 'tu_utc', 'den_loai_tru', 'su_co', 'ranking_rows', 'canh_xep_hang', 'trang_thai_canh',
                        'region', 'co_m1', 'bang_chung', 'metric_links', 'gioi_han', 'trang_thai_chay', 'loi_chay', 'nguon_cua_so', 'services', 'service_options')
            write(ROOT / 'du-lieu' / b['ban'] / 'vue' / (ca + '.json'), {k: d.get(k) for k in vue_keys})
            for svc in services:
                ops = [o for o in d['thao_tac'] if o['chu'] == svc]
                own = {o['id'] for o in ops}
                edges = [e for e in d['canh_thao_tac'] if e['source'] in own or e['target'] in own]
                ids = own | {x for e in edges for x in (e['source'], e['target'])}
                fields = ('id', 'ten', 'co_m1', 'chu', 'trang_thai_m1', 'mau', 'loai')
                nodes = [{**{k: o[k] for k in fields}, 'ngoai_service': o['chu'] != svc,
                          'don_vi_m1': {k: (o.get('don_vi_m1') or {}).get(k) for k in ('e_len', 'e_xuong')}} for o in d['thao_tac'] if o['id'] in ids]
                write(ROOT / 'du-lieu' / b['ban'] / 'thao-tac-vue' / ca / (svc + '.json'),
                      {'ban': meta, 'ca': ca, 'service': svc, 'cua_so_ms': w, 'thao_tac': ops, 'nut': nodes, 'canh': edges,
                       'thong_bao': (f'{len(ops)} thao tác từ trace; {sum(bool(o["co_m1"]) for o in ops)} có cờ M1 bản {b["ban"]}.' if ops else
                                     'Không có đầu ra phương pháp vì lỗi chạy; không dựng thao tác/hạng.' if not m else
                                     'Không có thao tác cho service trong trace sau cắt cửa sổ; chưa phân xử không phát sinh hay không được thu.')})
            replay = {'ban': meta, 'ca': ca, 'cua_so_ms': w, 'ranking_rows': rank, 'canh_xep_hang': er or [], 'gioi_han': 'Chưa cấp nguồn đáp án dev cho lớp giao diện; không dựng đáp án.'}
            if c['nguon'] == 't062':
                original = checked_old('p7/phat-lai/' + ca + '.json')
                replay.update(phat_lai=original['phat_lai'], gioi_han='Chỉ ghép đáp án gốc; không chấm hay mang kết quả chấm P7 sang bản khác.')
            write(ROOT / 'du-lieu' / b['ban'] / 'phat-lai' / (ca + '.json'), replay)
            case_links = [lk for op in d['thao_tac'] for lk in op.get('lien_ket', [])] + [lk for f in d['bang_chung'] for lk in f['lien_ket']] + d['metric_links']
            for lk in case_links:
                pane = json.loads(urllib.parse.parse_qs(urllib.parse.urlparse(lk['url']).query)['panes'][0])['a']
                assert pane['datasource'] == lk['kho']
                assert [int(pane['range']['from']), int(pane['range']['to'])] == [w[0], w[1] - 1]
                all_links.append({'ban': b['ban'], 'ca': ca, **lk})
            assert not any(k in d for k in ('phat_lai', 'tap_chap_nhan', 'root_khai_truoc', 'dap_an'))
            assert d['entity_ranking'] == (m['entity_ranking'] if m else [])
            assert d['co_m1'] == (m['extra'].get('kenh_co', []) if m else [])
            comparisons.append({'ban': b['ban'], 'ca': ca, 'source': c['dau_ra'], 'sha256': c['sha256'], 'window_ms': w,
                                'trang_thai_chay': run_state, 'ranking': len(rank), 'flags': len(flags), 'units': len(units),
                                'edges': len(er or []), 'operations': len(d['thao_tac']), 'links': len(case_links), 'exact': True})
            cases.append({'ma': ca, 'ban': b['ban'], 'nguon': c['nguon'], 'tu': w[0], 'den': w[1] - 1,
                          'ket_luan': m['verdict'] if m else None, 'trang_thai_chay': run_state, 'file': ca + '.json'})
        write(ROOT / 'du-lieu' / b['ban'] / 'chi-muc.json', {'su_co': cases})
        variants.append({**{k: v for k, v in b.items() if k != 'cac_ca'}, 'cac_ca': [c['ma'] for c in cases]})
    write(ROOT / 'du-lieu/chi-muc-ban.json', {'phien_ban_chi_muc': 2, 'ban': variants})
    write(ROOT / 'kiem/doi-chieu-xuat.json', comparisons)
    write(ROOT / 'kiem/lien-ket.json', all_links)
    # Giữ snapshot cũ đã kiểm, không phát lại các truy vấn sống theo ba bản.
    for ca, template in templates.items():
        services = set(o['chu'] for o in template['thao_tac'])
        for b in idx['ban']:
            d = read(ROOT / 'du-lieu' / b['ban'] / 'vue' / (ca + '.json'))
            services.update(d['services'])
        for svc in services:
            old = OLD / 'trang-thai' / ca / (svc + '.json')
            if old.exists() and ca not in [c['ca'] for c in idx['ban'][0]['cac_ca'] if c['nguon'] == 'dev3']:
                shot = checked_old('trang-thai/' + ca + '/' + svc + '.json')
            else:
                shot = {'queries': [{'panel': p, 'kho': kho, 'trang_thai': 'chua_truy_van', 'so_dong': None, 'utc': None,
                                     'tu_utc': iso(windows[ca][0]), 'den_loai_tru': iso(windows[ca][1]),
                                     'loi': 'Chưa lưu snapshot API cho tổ hợp này; nguồn raw không chứng minh kho sống còn dữ liệu.'}
                                    for p, kho in ((31, 'prometheus'), (32, 'prometheus'), (33, 'prometheus'), (34, 'tempo'), (35, 'loki'))]}
            write(ROOT / 'du-lieu/trang-thai' / ca / (svc + '.json'), shot)
    print(json.dumps({'utc': now(), 'export': len(comparisons), 'source_outputs': len(outputs), 'links': len(all_links)}, ensure_ascii=False), flush=True)


def dashboards():
    stop()
    for replay in (False, True):
        d = read(ROOT / 'nguon' / ('dashboard-phat-lai.json' if replay else 'dashboard-chinh.json'))
        raw = json.dumps(d, ensure_ascii=False).replace('http://localhost:3000/public/rca/t065-l4-001', URL).replace('t065-l4-rca', UID).replace('t065-l4-phat-lai', REPLAY)
        d = json.loads(raw)
        d.update(id=None, uid=REPLAY if replay else UID, version=1, title='T-065 L8b — ' + ('phát lại CÓ ĐÁP ÁN' if replay else 'M1-FT đề xuất cuối V082'), tags=['RCA', 'T-065', 'L8b', 'chi-muc-2'])
        d['time'] = {'from': '2026-11-14T07:39:15.000Z', 'to': '2026-11-14T07:49:14.999Z'}
        caseurl = URL + '/${ban}/vue/${ca}.json'
        for v in d['templating']['list']:
            if v['name'] == 'ban':
                v['current'] = {'text': 'V082-V066+H8a', 'value': 'V082-V066+H8a'}
            elif v['name'] == 'ca':
                v['current'] = {'text': '86dea661', 'value': '86dea661'}
            elif v['name'] == 'dv':
                v['query']['infinityQuery']['root_selector'] = '$$.([service_options.{"__text":ten,"__value":ma}])'
                v['current'] = {'text': 'event-service', 'value': 'event-service'}
            elif v['name'] == 'op':
                v['query']['infinityQuery']['root_selector'] = '$$.( $count(thao_tac)>0 ? [thao_tac.{"__text":ten,"__value":id}] : [{"__text":"(Không có thao tác)","__value":"__khong_co__"}] )'
        for p in d['panels']:
            if p['id'] == 1:
                p['options']['content'] = p['options']['content'].replace('Trạng thái truy vấn là snapshot', 'Trang này dùng chỉ mục bản 2; V082 là bản đề xuất cuối, V071 là bản thay thế có đầu ra cạnh. Ca lỗi chạy chỉ hiển thị lỗi và nguồn lỗi, không có hạng. Trạng thái truy vấn là snapshot')
            if p['id'] == 2:
                p['targets'][0]['root_selector'] = '$$.([su_co.{"ma":ma,"nguon":nguon,"trang_thai_chay":trang_thai_chay,"ket_luan":ket_luan,"tu":$fromMillis(tu),"den":$fromMillis(den)}])'
                p['targets'][0]['columns'].insert(2, {'selector': 'trang_thai_chay', 'text': 'trang_thai_chay', 'type': 'string'})
            if p['id'] == 3:
                fields = [('Bản', 'ban.ban'), ('Trạng thái bản', 'ban.trang_thai'), ('Trạng thái chạy', 'trang_thai_chay'),
                          ('Hash cấu hình (JSON chuẩn hóa)', 'ban.cau_hinh_sha256 ? ban.cau_hinh_sha256 : "null — chỉ mục nguồn chưa cấp"'),
                          ('Hash byte file cấu hình', 'ban.cau_hinh_file_sha256 ? ban.cau_hinh_file_sha256 : "null — chỉ mục nguồn chưa cấp"'),
                          ('Hash mã nguồn', 'ban.ma_nguon_sha256 ? ban.ma_nguon_sha256 : "null — chỉ mục nguồn chưa cấp"'),
                          ('Hash đầu ra', 'ban.sha256_output ? ban.sha256_output : "không có đầu ra"'),
                          ('Bắt đầu (bao gồm)', 'tu_utc'), ('Kết thúc (loại trừ)', 'den_loai_tru'),
                          ('Nguồn đầu ra', 'ban.nguon_output ? ban.nguon_output : "không có đầu ra phương pháp"'),
                          ('Lỗi chạy (nguồn)', 'loi_chay ? loi_chay : "không có"'), ('Nguồn cửa sổ ca', 'nguon_cua_so'),
                          ('Kết luận phương pháp', 'su_co.ket_luan ? su_co.ket_luan : "không có — lỗi chạy"'),
                          ('Ghi chú hash', 'ban.ghi_chu_hash'), ('Giới hạn', 'gioi_han')]
                p['targets'][0]['root_selector'] = '$$.([' + ','.join('{"a_truong":' + json.dumps(k, ensure_ascii=False) + ',"b_gia_tri":' + v + '}' for k, v in fields) + '])'
                added = 6
                p['gridPos']['h'] += added
                for q in d['panels']:
                    if q['id'] != 3 and q['gridPos']['y'] > p['gridPos']['y']:
                        q['gridPos']['y'] += added
            if p['id'] == 28:
                p['fieldConfig']['overrides'][0]['properties'][0]['value'][0]['options']['chua_truy_van'] = {'text': 'Chưa có snapshot API'}
        # Đặt default time từ đúng ca được chọn, không dùng giờ suy đoán.
        first = read(ROOT / 'du-lieu/V082-V066+H8a/vue/86dea661.json')
        d['time'] = {'from': first['tu_utc'], 'to': iso(first['cua_so_ms'][1] - 1)}
        write(ROOT / 'grafana' / (d['uid'] + '.json'), d)
    print(json.dumps({'dashboards': [UID, REPLAY]}))


def service_options():
    """Sửa riêng projection của biến service; không dựng lại raw/M1 hoặc số liệu."""
    stop()
    changed = []
    for b in read(ROOT / 'nguon/chi-muc-ban.json')['ban']:
        for c in b['cac_ca']:
            for sub in ('', 'vue'):
                p = ROOT / 'du-lieu' / b['ban'] / sub / (c['ca'] + '.json')
                d = read(p)
                d['service_options'] = [{'ma': svc, 'ten': '(Không có đầu ra — lỗi chạy)' if svc == EMPTY else svc} for svc in d['services']]
                before = sha(p)
                write(p, d)
                changed.append({'file': str(p.relative_to(ROOT)), 'before': before, 'after': sha(p)})
    write(ROOT / 'kiem/fix01-service-options.json', {'utc': now(), 'reason': 'Infinity JSONata $ trong map chuỗi trả mảng một phần tử; dùng object có trường ma/ten thay vì $', 'files': changed,
                                                   'raw_rerun': False, 'method_rerun': False})
    print(json.dumps({'service_projection_updated': len(changed), 'raw_rerun': False}))


def refresh_dashboard():
    """Chỉ cập nhật hai file L8b do chính lượt này tạo; giữ byte trước sửa."""
    stop()
    deployed = read(ROOT / 'kiem/deploy.json')
    records = []
    for entry in deployed['new_dashboards']:
        p = pathlib.Path(entry['file'])
        assert p.name in (UID + '.json', REPLAY + '.json') and p.is_relative_to(PROVISION)
        assert sha(p) == entry['sha256'], 'file mới đã đổi ngoài lượt: ' + str(p)
        backup = ROOT / 'rollback/fix01' / p.name
        assert not backup.exists()
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(p.read_bytes())
        p.write_bytes((ROOT / 'grafana' / p.name).read_bytes())
        records.append({'file': str(p), 'before': entry['sha256'], 'after': sha(p), 'backup': str(backup)})
    write(ROOT / 'kiem/deploy-fix01.json', {'utc': now(), 'files': records, 'restart': False})
    print(json.dumps({'new_dashboard_refresh': len(records), 'restart': False}))


def deploy():
    stop()
    before = read(ROOT / 'kiem/may-truoc.json')
    new = []
    for uid in (UID, REPLAY):
        p = PROVISION / 'RCA FlashTicket/1 · Kết quả hiện hành' / (uid + '.json')
        assert not p.exists(), str(p)
        source = ROOT / 'grafana' / (uid + '.json')
        p.write_bytes(source.read_bytes())
        new.append({'file': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size})
    after = inventory()
    unchanged = all(after['files'].get(p) == v for p, v in before['files'].items())
    assert unchanged
    write(ROOT / 'kiem/deploy.json', {'utc': now(), 'new_dashboards': new, 'old_files_unchanged': len(before['files']),
                                      'restart_by_agent': False, 'machine': after['machine']})
    print(json.dumps({'new_dashboards': new, 'old_unchanged': len(before['files']), 'restart': False}))


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'inventory':
        stop()
        result = inventory()
        write(ROOT / 'kiem/may-truoc.json', result)
        print(json.dumps({'utc': result['utc'], 'prior_files': len(result['files']), 'machine': result['machine']}))
    elif action == 'export':
        export()
    elif action == 'dashboards':
        dashboards()
    elif action == 'deploy':
        deploy()
    elif action == 'service-options':
        service_options()
    elif action == 'refresh-dashboard':
        refresh_dashboard()
    else:
        raise SystemExit('unknown action')

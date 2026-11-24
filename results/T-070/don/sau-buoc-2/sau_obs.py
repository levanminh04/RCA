# Kiểm sau dời trên obs (bước 2). Chỉ đọc, trừ một thông báo thử từ Grafana tới bộ nhận (ghi 1 dòng webhook.jsonl).
import hashlib, json, os, subprocess, sys, glob, urllib.request, urllib.parse, base64, time
OUT = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
N = '/srv/flashticket-rca'; R = N + '/rca'; A = N + '/archive/2026-11'
H = 'b0f79a4dffd552f6e6026172b9058cd54ee9272475d927e35f19e22b04411b8d'


def sha_file(p):
    d = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            d.update(b)
    return d.hexdigest()


def sha_tree(root):
    res = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            if os.path.isfile(p) and not os.path.islink(p):
                res[os.path.relpath(p, root)] = sha_file(p)
    return res


def sh(cmd, user=None):
    if user:
        cmd = ['sudo', '-n', '-u', user] + cmd
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def cu(k, fn):
    try:
        OUT[k] = fn()
    except Exception as e:
        OUT[k] = {'LOI': repr(e)[:300]}


cu('snapshot_sha256', lambda: sha_tree(f'{R}/method/{H}'))
cu('ghim_sha256', lambda: {os.path.basename(p): sha_file(p) for p in [
    R + '/m1-source-pins.json', R + '/m1-p7-config.json', R + '/flashticket-inventory-source.json',
    f'{R}/method/{H}/results/T-064/bien-the/V082-V066+H8a/cau-hinh.json']})
cu('hoi_quy_chuan_sha256', lambda: {p.split('rca/')[-1]: sha_file(p) for p in sorted(glob.glob(R + '/v082-hoi-quy/*/method-output-*.json'))})
cu('dev_sha256', lambda: sha_tree(R + '/results/dev'))
so = sorted(glob.glob(N + '/ledger/*'))
cu('cach_ly', lambda: {
    'archive_runs_t069-chinh.out_ton_tai(root)': os.path.isfile(A + '/runs/t069-chinh.out'),
    'rca_doc_archive_runs_t069(rc)': sh(['test', '-r', A + '/runs/t069-chinh.out'], 'rca')[0],
    'rca_qua_archive_runs(rc -x)': sh(['test', '-x', A + '/runs'], 'rca')[0],
    'rca_qua_runs_moi(rc -x)': sh(['test', '-x', N + '/runs'], 'rca')[0],
    'rca_qua_ledger(rc -x)': sh(['test', '-x', N + '/ledger'], 'rca')[0],
    'so_tiem': {os.path.basename(p): sh(['test', '-r', p], 'rca')[0] for p in so},
    'rca_doc_pins(rc)': sh(['test', '-r', R + '/m1-source-pins.json'], 'rca')[0],
    'rca_qua_cases(rc -x)': sh(['test', '-x', R + '/cases'], 'rca')[0],
})
env = {}
for line in open('/etc/flashticket-rca/grafana.env'):
    k, _, v = line.strip().partition('=')
    env[k] = v.strip().strip('"').strip("'")
cred = env.get('GF_SECURITY_ADMIN_USER', 'admin') + ':' + str(env.get('GF_SECURITY_ADMIN_PASSWORD'))
auth = 'Basic ' + base64.b64encode(cred.encode()).decode()
B = 'http://10.0.0.215:3000'


def get(path, data=None, method=None):
    rq = urllib.request.Request(B + path, data=data, method=method,
                                headers={'Authorization': auth, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(rq, timeout=30) as r:
        return r.status, json.load(r)


def grafana():
    rules = get('/api/v1/provisioning/alert-rules')[1]
    folders = get('/api/folders')[1]
    dash = get('/api/search?type=dash-db')[1]
    cps = get('/api/v1/provisioning/contact-points')[1]
    ds = {}
    for uid in ['prometheus', 'loki', 'tempo', 'infinity-rca']:
        try:
            ds[uid] = get(f'/api/datasources/uid/{uid}/health')[1].get('status')
        except Exception as e:
            ds[uid] = repr(e)[:120]
    return {'luat': sorted([{'uid': r['uid'], 'title': r['title'], 'folderUID': r['folderUID'], 'nhom': r['ruleGroup'],
                             'nhan_t072_uid': (r.get('labels') or {}).get('t072_uid'),
                             'receiver': (r.get('notification_settings') or {}).get('receiver')} for r in rules],
                           key=lambda x: x['uid']),
            'folder': [{'uid': f['uid'], 'title': f['title']} for f in folders],
            'dashboard': [{'uid': d['uid'], 'title': d['title'], 'folderUid': d.get('folderUid')} for d in dash],
            'contact_point': [{'uid': c.get('uid'), 'name': c.get('name'), 'type': c.get('type'),
                               'url': (c.get('settings') or {}).get('url')} for c in cps],
            'datasource_health': ds}


cu('grafana', grafana)


def public():
    res = {}
    for f in ['du-lieu/chi-muc-ban.json']:
        with urllib.request.urlopen(B + '/public/rca/dev/' + f, timeout=20) as r:
            b = r.read()
            res[f] = {'http': r.status, 'sha256': hashlib.sha256(b).hexdigest()}
    return res


cu('public_dev', public)


def bo_nhan():
    f = N + '/alerts/bo-nhan/webhook.jsonl'
    truoc = sum(1 for _ in open(f)) if os.path.exists(f) else 0
    body = json.dumps({'receivers': [{'name': 't072-bo-nhan-nhe', 'grafana_managed_receiver_configs': [
        {'uid': 't072-webhook', 'name': 't072-bo-nhan-nhe', 'type': 'webhook',
         'settings': {'url': 'http://t072-bo-nhan:9172/t072', 'httpMethod': 'POST'}, 'secureSettings': {}}]}]}).encode()
    st, res = get('/api/alertmanager/grafana/config/api/v1/receivers/test', data=body, method='POST')
    time.sleep(5)
    sau = sum(1 for _ in open(f)) if os.path.exists(f) else 0
    return {'http': st,
            'ket_qua_grafana': [[c.get('status') for c in r.get('grafana_managed_receiver_configs', [])] for r in res.get('receivers', [])],
            'dong_truoc': truoc, 'dong_sau': sau}


cu('bo_nhan', bo_nhan)
T0, T1 = 1795402800, 1795406400


def q(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def mau():
    res = {}
    res['prom_count_over_time_up_1h'] = q('http://127.0.0.1:9090/api/v1/query?' + urllib.parse.urlencode(
        {'query': 'sum(count_over_time(up[1h]))', 'time': T1}))['data']['result']
    res['prom_so_chuoi_span_metrics'] = q('http://127.0.0.1:9090/api/v1/query?' + urllib.parse.urlencode(
        {'query': 'count({__name__=~"traces_span_metrics.*|traces_spanmetrics.*"})', 'time': T1}))['data']['result']
    res['loki_so_dong_1h'] = q('http://127.0.0.1:3100/loki/api/v1/query?' + urllib.parse.urlencode(
        {'query': 'sum(count_over_time({service_name=~".+"}[1h]))', 'time': T1 * 10**9}))['data']['result']
    res['tempo_so_trace_1h'] = len(q('http://127.0.0.1:3200/api/search?' + urllib.parse.urlencode(
        {'start': T0, 'end': T1, 'limit': 100000})).get('traces', []))
    return res


cu('mau_kho', mau)
cu('git_lab', lambda: sh(['git', '-C', '/opt/flashticket-rca', 'rev-parse', 'HEAD'])[1].strip())
cu('con_duong_cu', lambda: [p for p in ['/opt/rca-lab', '/srv/rca-lab', '/etc/rca-lab', '/home/ubuntu/t063'] if os.path.exists(p)])
json.dump(OUT, sys.stdout, ensure_ascii=False, indent=1)

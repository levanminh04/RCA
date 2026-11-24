# Bước 0 kế hoạch dọn (T-070): chụp hiện trạng CHỈ ĐỌC. Chạy: sudo -n python3 - <may> < buoc0.py
# Không in giá trị biến môi trường (chỉ tên + sha256 rút gọn 16 hex). Không đọc nội dung log.
import hashlib, json, os, subprocess, sys, glob, urllib.request, urllib.parse, base64, time, tempfile, shutil

MAY = sys.argv[1]
OUT = {'may': MAY, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
BAN_NHAY = ('pass', 'secret', 'token', 'key', 'pwd', 'credential')


def sh(cmd, user=None, timeout=300):
    if user:
        cmd = ['sudo', '-n', '-u', user] + cmd
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr.strip()[-500:]


def h(v):
    return hashlib.sha256(str(v).encode()).hexdigest()[:16]


def sha_file(p):
    d = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            d.update(b)
    return d.hexdigest()


def sha_tree(root):
    res = {}
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            if os.path.isfile(p) and not os.path.islink(p):
                res[os.path.relpath(p, root)] = sha_file(p)
    return res


def nhay(s):
    return any(k in str(s).lower() for k in BAN_NHAY)


def containers(chi_ten=None):
    rc, ids, _ = sh(['docker', 'ps', '-aq'])
    res = []
    for cid in ids.split():
        rc, js, err = sh(['docker', 'inspect', cid])
        c = json.loads(js)[0]
        name = c['Name'].lstrip('/')
        if chi_ten and name not in chi_ten:
            continue
        cfg, hc = c['Config'], c['HostConfig']
        env = {}
        for e in cfg.get('Env') or []:
            k, _, v = e.partition('=')
            env[k] = 'sha256:' + h(v)
        cmd = cfg.get('Cmd') or []
        ent = cfg.get('Entrypoint') or []
        lb = cfg.get('Labels') or {}
        log_path = c.get('LogPath') or ''
        res.append({
            'ten': name, 'image': cfg.get('Image'), 'image_id': c.get('Image'),
            'trang_thai': c['State'].get('Status'), 'ma_thoat': c['State'].get('ExitCode'),
            'project': lb.get('com.docker.compose.project'), 'service': lb.get('com.docker.compose.service'),
            'working_dir': lb.get('com.docker.compose.project.working_dir'),
            'config_files': lb.get('com.docker.compose.project.config_files'),
            'environment_file': lb.get('com.docker.compose.project.environment_file'),
            'nhan_khac': {k: v for k, v in lb.items() if not k.startswith('com.docker.compose') and not k.startswith('org.opencontainers')},
            'mounts': [{'loai': m.get('Type'), 'nguon': m.get('Source'), 'dich': m.get('Destination'), 'rw': m.get('RW'),
                        'ten_volume': m.get('Name')} for m in c.get('Mounts', [])],
            'memory': hc.get('Memory'), 'network_mode': hc.get('NetworkMode'), 'log_config': hc.get('LogConfig'),
            'restart': hc.get('RestartPolicy'), 'ports': hc.get('PortBindings'), 'user': cfg.get('User'),
            'cmd': cmd if not any(nhay(a) for a in cmd) else {'sha256': h(json.dumps(cmd)), 'so_doi_so': len(cmd)},
            'entrypoint': ent if not any(nhay(a) for a in ent) else {'sha256': h(json.dumps(ent))},
            'env': env,
            'log_path': log_path, 'log_bytes': os.path.getsize(log_path) if log_path and os.path.exists(log_path) else None,
        })
    return res


def stat(paths):
    res = {}
    for p in paths:
        rc, o, e = sh(['stat', '-c', '%U:%G %a %F', p])
        res[p] = o.strip() if rc == 0 else 'KHONG-CO'
    return res


def grep_cu(roots, bo):
    mau = ['/opt/rca-lab', '/srv/rca-lab', '/etc/rca-lab', '/opt/flash-ticket-', '/home/ubuntu/t06', '/home/ubuntu/t07']
    cmd = ['find'] + roots + ['('] + sum([['-path', b, '-o'] for b in bo], [])[:-1] + [')', '-prune', '-o',
           '-type', 'f', '-size', '-1024k', '-print0']
    r = subprocess.run(cmd, capture_output=True, timeout=600)
    files = [f for f in r.stdout.decode(errors='replace').split('\0') if f]
    hit = {}
    for f in files:
        try:
            with open(f, 'rb') as fh:
                b = fh.read()
        except Exception:
            continue
        if b'\0' in b[:4096]:
            continue
        m = [x for x in mau if x.encode() in b]
        if m:
            hit[f] = m
    return {'so_file_quet': len(files), 'file_co_duong_cu': hit}


def cu(name, fn):
    try:
        OUT[name] = fn()
    except Exception as ex:
        OUT[name] = {'LOI': repr(ex)[:400]}


cu('compose_ls', lambda: sh(['docker', 'compose', 'ls', '-a', '--format', 'json'])[1])
cu('volume_ls', lambda: sh(['docker', 'volume', 'ls', '--format', '{{.Name}}'])[1].split())
cu('findmnt', lambda: {p: sh(['findmnt', '-n', '-o', 'SOURCE', '-T', p])[1].strip() for p in ('/opt', '/srv', '/etc', '/home')})

if MAY == 'obs':
    SNAP = '/srv/rca-lab/m1-snapshots/b0f79a4dffd552f6e6026172b9058cd54ee9272475d927e35f19e22b04411b8d'
    M1 = '/srv/rca-lab/m1'
    cu('containers', containers)
    cu('snapshot_sha256', lambda: sha_tree(SNAP))
    cu('ghim_sha256', lambda: {p: sha_file(p) for p in [M1 + '/m1-source-pins.json', M1 + '/m1-p7-config.json',
                                                           M1 + '/flashticket-inventory-source.json',
                                                           SNAP + '/results/T-064/bien-the/V082-V066+H8a/cau-hinh.json']})
    cu('hoi_quy_chuan_sha256', lambda: {p: sha_file(p) for p in sorted(glob.glob(M1 + '/v082-hoi-quy/*/method-output-*.json'))})
    cu('venv_python', lambda: sh(['/srv/rca-lab/venv-m1/bin/python', '--version'])[1].strip())
    cu('venv_pip_freeze', lambda: sh(['/srv/rca-lab/venv-m1/bin/python', '-m', 'pip', 'freeze', '--all'])[1].splitlines())
    cu('dev_sha256', lambda: sha_tree('/srv/rca-lab/rca-results/t065-l11-001'))
    cu('stat', lambda: stat(['/srv/rca-lab', '/srv/rca-lab/m1', '/srv/rca-lab/m1/cases', '/srv/rca-lab/m1/outputs',
                             '/srv/rca-lab/m1/t073-dev', '/srv/rca-lab/m1-snapshots', '/srv/rca-lab/venv-m1',
                             '/srv/rca-lab/rca-results', '/srv/rca-lab/rca-results/t065-l11-001', '/srv/rca-lab/ledger',
                             '/srv/rca-lab/runs', '/srv/rca-lab/runs/t072-e3-01', '/srv/rca-lab/runs/t072-e3-01-cfg',
                             '/srv/rca-lab/load-controller', '/srv/rca-lab/collector-gateway', '/srv/rca-lab/trace-goi',
                             '/etc/rca-lab', '/etc/rca-lab/controller', '/opt/rca-lab', '/var/lib/flash-ticket-ledger']))
    so_tiem = sorted(glob.glob('/srv/rca-lab/ledger/*'))
    cu('cach_ly', lambda: {
        'runs/t069-chinh.out_ton_tai(root)': os.path.isfile('/srv/rca-lab/runs/t069-chinh.out'),
        'rca_doc_runs/t069-chinh.out(rc)': sh(['test', '-r', '/srv/rca-lab/runs/t069-chinh.out'], user='rca')[0],
        'rca_qua_runs(rc test -x)': sh(['test', '-x', '/srv/rca-lab/runs'], user='rca')[0],
        'so_tiem_file': [os.path.basename(p) for p in so_tiem],
        'rca_doc_so_tiem(rc)': {os.path.basename(p): sh(['test', '-r', p], user='rca')[0] for p in so_tiem},
        'rca_qua_ledger(rc test -x)': sh(['test', '-x', '/srv/rca-lab/ledger'], user='rca')[0],
    })
    cu('stop', lambda: {p: os.path.exists(p) for p in ['/srv/rca-lab/runs/STOP', '/srv/rca-lab/load-controller/STOP']})

    def pypi():
        d = tempfile.mkdtemp(prefix='don-pypi-')
        os.chmod(d, 0o777)
        rc, o, e = sh(['/srv/rca-lab/venv-m1/bin/python', '-m', 'pip', 'download', '--no-deps', '--no-cache-dir',
                       '-q', '-d', d, 'six==1.16.0'], user='ubuntu', timeout=120)
        n = os.listdir(d)
        shutil.rmtree(d)
        return {'rc': rc, 'file_tai': n, 'loi': e}
    cu('pypi', pypi)

    def grafana():
        env = {}
        for line in open('/etc/rca-lab/grafana.env'):
            k, _, v = line.strip().partition('=')
            env[k] = v.strip().strip('"').strip("'")
        u = env.get('GF_SECURITY_ADMIN_USER', 'admin')
        p = env.get('GF_SECURITY_ADMIN_PASSWORD')
        auth = 'Basic ' + base64.b64encode(f'{u}:{p}'.encode()).decode()
        base = 'http://10.0.0.215:3000'

        def get(path):
            rq = urllib.request.Request(base + path, headers={'Authorization': auth})
            with urllib.request.urlopen(rq, timeout=20) as r:
                return json.load(r)
        rules = get('/api/v1/provisioning/alert-rules')
        folders = get('/api/folders')
        dash = get('/api/search?type=dash-db')
        cps = get('/api/v1/provisioning/contact-points')
        return {
            'luat': sorted([{'uid': r['uid'], 'title': r['title'], 'folderUID': r['folderUID'], 'nhom': r['ruleGroup'],
                             'nhan_t072_uid': (r.get('labels') or {}).get('t072_uid'),
                             'receiver': ((r.get('notification_settings') or {}).get('receiver'))} for r in rules],
                           key=lambda x: x['uid']),
            'folder': [{'uid': f['uid'], 'title': f['title']} for f in folders],
            'dashboard': [{'uid': d['uid'], 'title': d['title'], 'folderUid': d.get('folderUid')} for d in dash],
            'contact_point': [{'uid': c.get('uid'), 'name': c.get('name'), 'type': c.get('type')} for c in cps],
        }
    cu('grafana', grafana)

    T0, T1 = 1795402800, 1795406400  # 2026-11-23T03:00Z .. 04:00Z (khoảng cố định trước ngày dời)

    def q(url):
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)

    def mau_kho():
        res = {}
        pq = urllib.parse.urlencode({'query': 'sum(count_over_time(up[1h]))', 'time': T1})
        res['prom_count_over_time_up_1h'] = q('http://127.0.0.1:9090/api/v1/query?' + pq)['data']['result']
        pq = urllib.parse.urlencode({'query': 'count({__name__=~"traces_span_metrics.*|traces_spanmetrics.*"})', 'time': T1})
        res['prom_so_chuoi_span_metrics'] = q('http://127.0.0.1:9090/api/v1/query?' + pq)['data']['result']
        lb = q('http://127.0.0.1:3100/loki/api/v1/labels?' + urllib.parse.urlencode({'start': T0 * 10**9, 'end': T1 * 10**9}))['data']
        nhan = 'service_name' if 'service_name' in lb else lb[0]
        lq = urllib.parse.urlencode({'query': f'sum(count_over_time({{{nhan}=~".+"}}[1h]))', 'time': T1 * 10**9})
        res['loki_nhan'] = nhan
        res['loki_so_dong_1h'] = q('http://127.0.0.1:3100/loki/api/v1/query?' + lq)['data']['result']
        tq = urllib.parse.urlencode({'start': T0, 'end': T1, 'limit': 100000})
        res['tempo_so_trace_1h'] = len(q('http://127.0.0.1:3200/api/search?' + tq).get('traces', []))
        res['khoang'] = ['2026-11-23T03:00:00Z', '2026-11-23T04:00:00Z']
        return res
    cu('mau_kho', mau_kho)
    cu('grep_duong_cu', lambda: grep_cu(['/opt', '/etc', '/home', '/root', '/var/spool/cron'],
                                        ['/opt/rca-lab', '/home/ubuntu/.cache', '/opt/unified-monitoring-agent', '/etc/ssl']))

elif MAY == 'app':
    cu('containers', containers)
    cu('compose_dir', lambda: open('/home/ubuntu/t063/inj/compose-dir').read().strip())
    cu('stat', lambda: stat(['/opt/flash-ticket-app', '/opt/flash-ticket-app/env', '/opt/flash-ticket-app/env-t062',
                             '/opt/flash-ticket-app/rca-faults', '/opt/flash-ticket-app/secrets', '/opt/flash-ticket-app/otel',
                             '/opt/flash-ticket-app/l1-vnpay', '/opt/flash-ticket-app/rca-toxiproxy', '/opt/flash-ticket-infra',
                             '/opt/flash-ticket-build', '/opt/flash-ticket-build/t067-compose', '/opt/flash-ticket-src',
                             '/opt/docs/architecture/data/mongodb/schema.cjs', '/home/ubuntu/t063/inj', '/srv/rca-lab',
                             '/srv/rca-lab/collector-agent', '/etc/rca-lab', '/opt/rca-lab'] +
                            sorted(glob.glob('/opt/flash-ticket-app/rca-faults/*/*'))))
    cu('env_file_sha256', lambda: {p: sha_file(p) for p in sorted(glob.glob('/opt/flash-ticket-app/env-t062/*.env') +
                                                                  glob.glob('/opt/flash-ticket-app/env/*'))})

    def db():
        sql = ("select lifecycle_state, count(*) from booking_schema.tbl_orders group by 1 order by 1;")
        rc, o, e = sh(['docker', 'exec', '-i', 'flash-ticket-infra-postgres-1', 'psql', '-U', 'postgres', '-X', '-At',
                       '-d', 'booking_db', '-c', 'begin read only; ' + sql + ' rollback;'])
        return {'rc': rc, 'ket_qua': o.splitlines(), 'loi': e}
    cu('db_don', db)
    cu('tien_trinh_tran', lambda: sh(['pgrep', '-af', 'mock-runner|tunnel-supervisor|ssh -R'])[1].splitlines())
    cu('grep_duong_cu', lambda: grep_cu(['/opt', '/etc', '/home', '/root', '/var/spool/cron'],
                                        ['/opt/rca-lab', '/opt/flash-ticket-src', '/opt/flash-ticket-build',
                                         '/home/ubuntu/.m2', '/opt/flash-ticket-infra/services', '/opt/flash-ticket-app/collector',
                                         '/opt/unified-monitoring-agent', '/etc/ssl', '/home/ubuntu/.cache']))

elif MAY == 'tai':
    rc, o, e = sh(['docker', 'ps', '-a', '--filter', 'name=rca-tai-', '--filter', 'status=exited', '--format', '{{.Names}}'])
    ten = o.split()
    OUT['so_container_rca_tai_da_thoat'] = len(ten)

    def k6():
        ds, ngoai_le = [], []
        for t in ten:
            c = json.loads(sh(['docker', 'inspect', t])[1])[0]
            out = [m['Source'] for m in c.get('Mounts', []) if m.get('Destination') == '/out']
            lp = c.get('LogPath') or ''
            r = {'ten': t, 'ma_thoat': c['State'].get('ExitCode'), 'nguon_out': out[0] if out else None,
                 'co_container_log': bool(out) and os.path.isfile(os.path.join(out[0], 'container.log')),
                 'log_docker_bytes': os.path.getsize(lp) if lp and os.path.exists(lp) else None}
            ds.append(r)
            if not r['co_container_log']:
                ngoai_le.append(t)
        return {'tat_ca': ds, 'ngoai_le': ngoai_le}
    cu('k6_container', k6)
    cu('stat', lambda: stat(['/srv/rca-lab', '/srv/rca-lab/load-runs', '/etc/rca-lab', '/etc/rca-lab/load-secret',
                             '/opt/rca-lab', '/opt/rca-tai']))
    cu('cong_19091', lambda: sh(['ss', '-tln'])[1].count(':19091'))
    cu('grep_duong_cu', lambda: grep_cu(['/opt', '/etc', '/home', '/root', '/var/spool/cron'],
                                        ['/opt/rca-lab', '/opt/rca-tai/out', '/home/ubuntu/x86-check', '/home/ubuntu/uvenv',
                                         '/etc/ssl', '/home/ubuntu/.cache']))

json.dump(OUT, sys.stdout, ensure_ascii=False, indent=1, default=str)

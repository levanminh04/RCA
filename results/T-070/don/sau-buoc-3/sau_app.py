# Kiểm sau dời trên app (bước 3). Chỉ đọc. Không in giá trị env (chỉ sha256 rút gọn, như buoc0.py).
import hashlib, json, os, subprocess, sys, time, glob
OUT = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}


def sh(cmd, timeout=120):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr.strip()[-300:]


def h(v):
    return hashlib.sha256(str(v).encode()).hexdigest()[:16]


def sha_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


BAN_NHAY = ('pass', 'secret', 'token', 'key', 'pwd', 'credential')


def containers():
    res = []
    for cid in sh(['docker', 'ps', '-aq'])[1].split():
        c = json.loads(sh(['docker', 'inspect', cid])[1])[0]
        cfg, hc = c['Config'], c['HostConfig']
        env = {}
        for e in cfg.get('Env') or []:
            k, _, v = e.partition('=')
            env[k] = 'sha256:' + h(v)
        cmd = cfg.get('Cmd') or []
        lb = cfg.get('Labels') or {}
        res.append({'ten': c['Name'].lstrip('/'), 'image': cfg.get('Image'), 'image_id': c.get('Image'),
                    'trang_thai': c['State'].get('Status'), 'project': lb.get('com.docker.compose.project'),
                    'config_files': lb.get('com.docker.compose.project.config_files'),
                    'environment_file': lb.get('com.docker.compose.project.environment_file'),
                    'nhan_khac': {k: v for k, v in lb.items() if not k.startswith('com.docker.compose') and not k.startswith('org.opencontainers')},
                    'mounts': [{'loai': m.get('Type'), 'nguon': m.get('Source'), 'dich': m.get('Destination'), 'rw': m.get('RW'), 'ten_volume': m.get('Name')} for m in c.get('Mounts', [])],
                    'memory': hc.get('Memory'), 'network_mode': hc.get('NetworkMode'), 'log_config': hc.get('LogConfig'),
                    'restart': hc.get('RestartPolicy'), 'ports': hc.get('PortBindings'), 'user': cfg.get('User'),
                    'cmd': cmd if not any(any(k in str(a).lower() for k in BAN_NHAY) for a in cmd) else {'sha256': h(json.dumps(cmd)), 'so_doi_so': len(cmd)},
                    'env': env})
    return res


OUT['containers'] = containers()
OUT['volume_ls'] = sh(['docker', 'volume', 'ls', '--format', '{{.Name}}'])[1].split()
OUT['volume_dung_boi'] = {v: sh(['docker', 'ps', '-a', '--filter', 'volume=' + v, '--format', '{{.Names}}'])[1].split() for v in OUT['volume_ls']}
OUT['env_file_sha256'] = {p: sha_file(p) for p in sorted(glob.glob('/opt/flashticket/env/*'))}
rc, o, e = sh(['docker', 'exec', '-i', 'flash-ticket-infra-postgres-1', 'psql', '-U', 'postgres', '-X', '-At', '-d', 'booking_db',
               '-c', 'begin read only; select lifecycle_state, count(*) from booking_schema.tbl_orders group by 1 order by 1; rollback;'])
OUT['db_don'] = {'rc': rc, 'ket_qua': o.splitlines(), 'loi': e}
OUT['compose_dir'] = open('/srv/flashticket-rca/faults/inject-state/compose-dir').read().strip()
OUT['schema_cjs'] = sh(['stat', '-c', '%F %s', '/opt/flashticket/docs/architecture/data/mongodb/schema.cjs'])[1].strip()
OUT['con_duong_cu'] = [p for p in ['/opt/rca-lab', '/srv/rca-lab', '/etc/rca-lab', '/opt/flash-ticket-src', '/opt/flash-ticket-infra', '/home/ubuntu/t063'] if os.path.exists(p)]
OUT['git_lab'] = sh(['git', '-C', '/opt/flashticket-rca', 'rev-parse', 'HEAD'])[1].strip()
json.dump(OUT, sys.stdout, ensure_ascii=False, indent=1)

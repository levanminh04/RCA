# -*- coding: utf-8 -*-
"""T-063 thu3 — hồ sơ đóng băng bản 3 (bản sao dong-bang/dong_bang.py + file của thu bù 3; chỉ đọc).
Khác bản gốc: thêm ~/inj3.py và ~/t063/thu3/* trên exp-app, ~/rca-dieu-phoi/thu3-cong-cu/* trên exp-obs, nhãn image Event, file thu3 ở laptop.
Gốc: Dùng: py -3 -B results/T-063/dong-bang/dong_bang.py [ten-file.json]
→ results/T-063/dong-bang/<ten-file> (mặc định dong-bang.json = bản 1; bản 2: dong-bang-2.json, giữ bản 1) (+ in tóm tắt). Không đọc nội dung file env/bí mật: chỉ băm.
"""
import datetime as dt, hashlib, json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
SSH = 'C:/Program Files/Git/usr/bin/ssh.exe'
KH = 'UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts'
MAY = {'app': ['-i', 'D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key', '-o', 'BatchMode=yes', '-o', KH, 'ubuntu@129.221.208.47'],
       'obs': ['-i', 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', '-o', 'BatchMode=yes', '-o', KH, 'ubuntu@213.35.116.128']}


def ssh(m, cmd):
    return subprocess.run([SSH] + MAY[m] + [cmd], capture_output=True, text=True, encoding='utf-8', timeout=120).stdout


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


out = {'utc': dt.datetime.now(dt.timezone.utc).isoformat()}
out['exp_app_container'] = [l.split('\t') for l in ssh('app', "docker ps --format '{{.Names}}\t{{.Image}}\t{{.ID}}' | sort").splitlines()]
out['exp_app_image_id'] = dict(l.split(' ', 1) for l in ssh('app', "for c in $(docker ps --format '{{.Names}}'); do echo \"$c $(docker inspect $c --format '{{.Image}}')\"; done").splitlines() if ' ' in l)
out['exp_app_file_sha256'] = dict(reversed(l.split('  ', 1)) for l in ssh('app', 'sudo sha256sum /opt/flash-ticket-app/collector/config.json /opt/flash-ticket-app/compose-t062/*.yml /opt/flash-ticket-app/compose-exp/keycloak.yml '
                                                                           '/opt/flash-ticket-app/rca-toxiproxy/proxies.json /opt/flash-ticket-app/env-t062/*.env /opt/flash-ticket-infra/deploy/docker-compose.*.yml '
                                                                           '/opt/flash-ticket-infra/deploy/mongodb/compose.yaml /home/ubuntu/inj2.py /home/ubuntu/inj3.py /home/ubuntu/t063/thu3/*.sh /home/ubuntu/t063/thu3/*.patch /home/ubuntu/t063/thu3/*.py /opt/flash-ticket-app/l1-vnpay/*.py 2>/dev/null').splitlines() if '  ' in l)
out['exp_obs_file_sha256'] = dict(reversed(l.split('  ', 1)) for l in ssh('obs', 'sha256sum /opt/flash-ticket-obs/pinned/*.json ~/rca-dieu-phoi/*.py ~/rca-dieu-phoi/*.json ~/rca-dieu-phoi/k6/* ~/rca-dieu-phoi/thu3-cong-cu/* 2>/dev/null; sudo sha256sum /opt/flash-ticket-rca/stage-m1.py /opt/flash-ticket-rca/run-m1.py /opt/flash-ticket-rca/m1-p7-config.json /home/ubuntu/t058/safe-export.py').splitlines() if '  ' in l)
out['exp_obs_container'] = [l.split('\t') for l in ssh('obs', "docker ps --format '{{.Names}}\t{{.Image}}' | sort").splitlines()]
out['prometheus_flags'] = ssh('obs', "curl -s localhost:9090/api/v1/status/flags | python3 -c \"import json,sys;d=json.load(sys.stdin)['data'];print(json.dumps({k:d[k] for k in d if 'retention' in k}))\"").strip()
loc = ['results/T-063/chay/runner2.py', 'results/T-063/chay/runner3.py', 'results/T-062/tai-2/tai_linux.py', 'results/T-063/tiem-loi/inj2.py', 'results/T-063/dong-goi/xuat_bo_sung.py',
       'results/T-062/tai-2/chay-tai.ps1', 'results/T-062/tai-2/k6/hanh-trinh.js', 'results/T-062/tai-2/k6/cau-hinh.json',
       'results/T-063/chay/lich-2.json', 'results/T-062/ca/_nguon/m1-source-pins.json', 'results/T-062/ca/_nguon/m1-p7-config.json',
       'results/T-064/tieu-chi-chon.md', 'results/T-063/thu3/scripts/runner4.py', 'results/T-063/thu3/scripts/tao_runner4.py',
       'results/T-063/thu3/scripts/inj3.py', 'results/T-063/thu3/lich-3.json', 'results/T-063/thu3/scripts/xac_nhan_ca_3.py',
       'results/T-063/thu3/dieu-kien-xac-nhan-3.md', 'results/T-063/thu3/scripts/h3-pool-event.patch',
       'results/T-063/thu3/scripts/build-t063-event.sh', 'results/T-063/thu3/scripts/deploy-t063-event.sh']
out['laptop_file_sha256'] = {p: (sha(R / p) if (R / p).exists() else None) for p in loc}
out['event_image_labels'] = ssh('app', "docker inspect flash-ticket-event-service-event-service-1 --format '{{json .Config.Labels}}'").strip()
out['flashticket_repo'] = subprocess.run(['git', '-C', 'D:/Project/flash-ticket-platform', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
RA = R / 'results/T-063/dong-bang' / sys.argv[1]
assert not RA.exists(), 'không ghi đè hồ sơ đóng băng đã có'
RA.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('container exp-app', len(out['exp_app_container']), '| file exp-app', len(out['exp_app_file_sha256']), '| file exp-obs', len(out['exp_obs_file_sha256']))
print('thiếu ở laptop:', [p for p, h in out['laptop_file_sha256'].items() if h is None])
print(out['prometheus_flags'])

#!/usr/bin/env python3
"""T-062: KP-19 — filelog của Collector exp-app ghim đường dẫn theo ID container cũ; trỏ lại ID container đang chạy.
Chỉ đổi khóa `include` của filelog/<svc>; lưu bản cũ config.json.truoc-t062-<giờ>. Không in bí mật (file không chứa bí mật ở các khóa này)."""
import json, subprocess, shutil, datetime as dt, hashlib
P = '/opt/flash-ticket-app/collector/config.json'
c = json.load(open(P))
ts = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
before = hashlib.sha256(open(P, 'rb').read()).hexdigest()
shutil.copy2(P, P + '.truoc-t062-' + ts)
changed = {}
for k, v in c['receivers'].items():
    if not k.startswith('filelog/'): continue
    svc = k.split('/', 1)[1]
    name = f'flash-ticket-{svc}-{svc}-1'
    cid = subprocess.check_output(['docker', 'inspect', name, '--format', '{{.Id}}'], text=True).strip()
    new = [f'/var/lib/docker/containers/{cid}/{cid}-json.log']
    if v['include'] != new:
        changed[svc] = {'cu': v['include'][0].split('/')[-2][:12], 'moi': cid[:12]}
        v['include'] = new
json.dump(c, open(P, 'w'), indent=1)
after = hashlib.sha256(open(P, 'rb').read()).hexdigest()
print(json.dumps({'sha256_truoc': before, 'sha256_sau': after, 'ban_cu': P + '.truoc-t062-' + ts, 'doi': changed}, indent=1))

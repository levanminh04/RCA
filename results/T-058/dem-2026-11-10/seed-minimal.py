#!/usr/bin/env python3
"""Create a synthetic event from the repository's documented SQL fixture."""
import datetime
import json
from pathlib import Path
import subprocess
import uuid

root=Path('/home/ubuntu/t058')
if (root/'seed-fixture.json').exists():
    raise SystemExit('Seed already exists; use seed-fixture.json')
source=Path('/opt/flash-ticket-src/docs/java-workflow/reports/2026-11-02-booking-flow-seed119.sql')
sql=source.read_text()
original={'category_id':'d79b7e19-273d-43f5-929b-66563533d413','venue_id':'cb593c60-690b-49c4-a224-497560854372',
          'event_id':'83c2d8fb-9ca6-4277-8beb-4122d72dceb8','ticket_type_id':'27ecd568-a44d-4db1-aaeb-3d168e56483f',
          'second_ticket_type_id':'1e46cbb3-4c74-40e0-b490-6c1a3cb7b364'}
ids={k:str(uuid.uuid4()) for k in original}
for key,value in original.items():
    sql=sql.replace(value,ids[key])
now=datetime.datetime.now(datetime.timezone.utc)
for old,delta in [('2026-11-23T16:39:33Z',7),('2026-11-24T16:39:33Z',8),('2026-11-01T16:39:33Z',-1),('2026-11-16T16:39:33Z',3)]:
    sql=sql.replace(old,(now+datetime.timedelta(days=delta)).strftime('%Y-%m-%dT%H:%M:%SZ'))
sql=sql.replace('[TEST119] Booking end-to-end 2026-11-02 16:39 UTC','Evening concert')
sql=sql.replace('TEST119','Concert').replace('Test venue 119','Concert hall')
sql=sql.replace('Synthetic data for manual booking and VNPay sandbox testing','Synthetic event for API verification')
(root/'seed-minimal.sql').write_text(sql)
p=subprocess.run(['docker','exec','-i','flash-ticket-infra-postgres-1','psql','-X','-v','ON_ERROR_STOP=1','-U','postgres','-d','postgres'],input=sql,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if p.returncode:
    print(p.stderr)
    raise SystemExit(p.returncode)
env=dict(line.split('=',1) for line in Path('/opt/flash-ticket-infra/.env').read_text().splitlines() if line and not line.startswith('#'))
js='db.getSiblingDB("admin").auth("user_admin",'+json.dumps(env['USER_DB_ADMIN_PASSWORD'])+');\n'
js+=Path('/opt/flash-ticket-src/deploy/mongodb/30-seed-authoritative.js').read_text()
p=subprocess.run(['docker','exec','-i','flash-ticket-infra-user-db-1','mongosh','--quiet','--file','/dev/stdin'],input=js,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if p.returncode:
    raise SystemExit('MongoDB seed failed; diagnostic withheld')
ids.update(utc=now.isoformat(),sql_source=str(source),method='SQL event and snapshots; repository MongoDB authoritative seed',
           note='Only synthetic initialization; event publication API and message propagation are not validated by this seed')
(root/'seed-fixture.json').write_text(json.dumps(ids,indent=2)+'\n')
print(json.dumps(ids,indent=2))

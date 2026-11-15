#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

p=Path('/opt/flash-ticket-app/env/booking-service.env')
values=dict(x.split('=',1) for x in p.read_text().splitlines() if x and not x.startswith('#'))
if sys.argv[1]=='on': values['OTEL_JAVAAGENT_DEBUG']='true'
else: values.pop('OTEL_JAVAAGENT_DEBUG',None)
p.write_text(''.join(k+'='+v+'\n' for k,v in sorted(values.items())))
p.chmod(0o600)
import os
subprocess.run(['docker','compose','-f','/opt/flash-ticket-app/compose-exp/booking-service.yml','-p','flash-ticket-booking-service','up','-d'],env=dict(os.environ,IMAGE='ft-local/booking-service:arm64-e4304048'),check=True)
print('Booking agent debug',sys.argv[1])

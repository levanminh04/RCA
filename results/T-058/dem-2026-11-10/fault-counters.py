"""Operator snapshot; never part of the method input pack."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
import urllib.request

role,phase=sys.argv[1:3]
if role not in ['app','obs'] or phase not in ['before','after']: raise SystemExit('Bad snapshot arguments')
with urllib.request.urlopen('http://127.0.0.1:8888/metrics',timeout=10) as response:
    metrics=response.read().decode()
chosen=[line for line in metrics.splitlines() if not line.startswith('#') and any(word in line for word in
        ['receiver_accepted','receiver_refused','exporter_sent','exporter_send_failed','exporter_enqueue_failed','exporter_queue_size'])]
result={'role':role,'phase':phase,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'chrony_tracking':subprocess.check_output(['chronyc','tracking'],text=True),
        'collector_counters':chosen}
path=Path('/home/ubuntu/t058')/('fault-counters-'+phase+'-'+role+'.json')
if path.exists(): raise SystemExit('Refuse to overwrite a counter snapshot')
path.write_text(json.dumps(result,indent=2)+'\n')
print('Saved',path)

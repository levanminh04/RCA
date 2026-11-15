"""Freeze the overnight execution choices before either method window is run."""
import datetime
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
target=root/'m1-execution-plan.json'
if target.exists(): raise SystemExit('Refuse to overwrite the frozen execution plan')
names=['src/m1/adapter_flashticket.py','stage-m1.py','run-m1.py','m1-p7-config.json',
       'm1-source-pins.json','flashticket-inventory-source.json','pause-probe.py','light-load.py']
plan={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'scope':'C4 feasibility only; one reversible probe plus one normal window under STEER #3; not SPEC 3+1',
      'mode':'a','method':'unchanged P7; seven arguments only; locked configuration from T054 main013-v2',
      'planned_cases':[{'opaque_id':'8d31bc06','operator_only_role':'normal',
                        't':int(datetime.datetime(2026,11,10,21,35,tzinfo=datetime.timezone.utc).timestamp())},
                       {'opaque_id':'a7c92f1e','operator_only_role':'one reversible process pause',
                        't_rule':'floor confirmed intervention epoch_ns / 1e9, from operator ledger; only t crosses into request.json',
                        'planned_not_before_utc':'2026-11-10T21:50:00Z','component':'booking-service','duration_seconds':300}],
      'method_window_rule':'[t-300s,t+300s); spans must start >= lower and end < upper',
      'raw_pack_window_rule':'[t-600s,t+600s); stage only after upper bound plus export flush',
      'load':'fixed arrival 1 request/s, equal alternating catalog/detail/availability, 21:15-22:15Z',
      'resource_windows':'20:45-21:15 idle; 21:15-21:45 load; no intervention during these windows',
      'repeat':'two runs per identical frozen input with fresh in-memory cache; compare canonical output SHA256',
      'checks':['39 source pins','manifest hashes','forbidden fields recursively','opaque IDs and ledger paths excluded',
                'rca user cannot read operator ledger','inspect nonempty intermediate spans/nodes/edges and fallback counts'],
      'interpretation':'Record ERROR/UNSUPPORTED/NO_TARGET without inventing data; diagnose adapter or orchestration errors separately. No efficacy or RQ5 claim.',
      'files_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}}
target.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Frozen',plan['frozen_utc'],len(names),'file hashes')

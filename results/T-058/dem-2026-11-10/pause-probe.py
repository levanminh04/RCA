#!/usr/bin/env python3
"""Operator-only reversible probe. Never imported by the RCA adapter or runner."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

NAME='flash-ticket-booking-service-booking-service-1'
OPAQUE='a7c92f1e'
FOLDER=Path('/var/lib/flash-ticket-ledger')
FOLDER.mkdir(exist_ok=True,mode=0o700)
LEDGER=FOLDER/'ledger.jsonl'
os.umask(0o077)

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def append(event):
    lines=LEDGER.read_text().splitlines() if LEDGER.exists() else []
    previous='0'*64
    for line in lines:
        old=json.loads(line); expected=old.pop('sha256')
        if old['previous_sha256']!=previous or hashlib.sha256(canonical(old).encode()).hexdigest()!=expected:
            raise RuntimeError('Invalid existing ledger chain')
        previous=expected
    event=dict(event,sequence=len(lines)+1,previous_sha256=previous)
    event['sha256']=hashlib.sha256(canonical(event).encode()).hexdigest()
    with LEDGER.open('a') as stream:
        stream.write(canonical(event)+'\n'); stream.flush(); os.fsync(stream.fileno())
    os.chmod(LEDGER,0o600)
    print(canonical(event),flush=True)

def inspect():
    data=json.loads(subprocess.check_output(['docker','inspect',NAME]))[0]
    return {k:data['State'][k] for k in ['Running','Paused','OOMKilled','Status']}

def stamp():
    now=time.time_ns()
    return {'epoch_ns':now,'utc':datetime.datetime.fromtimestamp(now/1e9,datetime.timezone.utc).isoformat()}

if LEDGER.exists() and LEDGER.stat().st_size:
    raise SystemExit('Refuse to repeat the one authorized probe with an existing ledger')
initial=inspect()
if not initial['Running'] or initial['Paused']: raise SystemExit('Target must be running and not paused')
chrony=subprocess.check_output(['chronyc','tracking'],text=True)
# A second independent unpause protects recovery if this Python process is killed.
subprocess.run(['systemd-run','--unit=t058-unpause-failsafe','--on-active=330s',
                '/usr/bin/docker','unpause',NAME],check=True)
started=stamp(); paused=False
try:
    result=subprocess.run(['docker','pause',NAME],capture_output=True,text=True)
    state=inspect(); paused=state['Paused']
    confirmed=stamp()
    append({'opaque_id':OPAQUE,'event':'intervention_start','component':'booking-service',
            'fault_family':'process_pause','mechanism':'docker pause','position':NAME,
            'command':['docker','pause',NAME],'command_exit':result.returncode,
            'requested':started,'confirmed':confirmed,'independent_probe':state,
            'clock':chrony,'planned_duration_seconds':300,
            'load_schedule':'21:15Z-22:15Z fixed-arrival 1 request/s; 3 read endpoints',
            'manifest_reference':'manifest-digest.json','agent_version':'2.33.1',
            'sampling':'parentbased_always_on; no tail sampling'})
    if result.returncode or not paused: raise RuntimeError('Pause not confirmed')
    marker=Path('/home/ubuntu/t058/pause-start.json')
    marker.write_text(canonical({'opaque_id':OPAQUE,'t':confirmed['epoch_ns']//10**9})+'\n')
    marker.chmod(0o644)
    time.sleep(300)
finally:
    requested=stamp()
    recovery=subprocess.run(['docker','unpause',NAME],capture_output=True,text=True)
    state=inspect()
    append({'opaque_id':OPAQUE,'event':'intervention_end','component':'booking-service',
            'fault_family':'process_pause','command':['docker','unpause',NAME],
            'command_exit':recovery.returncode,'requested':requested,'confirmed':stamp(),
            'independent_probe':state})
    if state['Paused'] or not state['Running']: raise RuntimeError('Recovery not confirmed')
    subprocess.run(['systemctl','stop','t058-unpause-failsafe.timer'],check=True)
    Path('/home/ubuntu/t058/pause-probe.done').touch()

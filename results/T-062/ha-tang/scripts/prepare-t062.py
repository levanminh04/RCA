#!/usr/bin/env python3
"""T-062 A2: dựng /opt/flash-ticket-app/{env-t062,compose-t062} từ bản đang chạy. Không in giá trị env."""
import pathlib, re, shutil, sys, json, hashlib, os
SHA = sys.argv[1]
A = pathlib.Path('/opt/flash-ticket-app')
SVCS = ['discovery-server','api-gateway','user-service','event-service','ticket-service','booking-service','payment-service']
FAULT = {'booking-service','event-service'}
envd, cd = A/'env-t062', A/'compose-t062'
envd.mkdir(mode=0o700, exist_ok=True); cd.mkdir(exist_ok=True)
report = {}
IDENT = ('service.name','service.version','service.instance.id','host.id','deployment.environment')
for s in SVCS:
    lines = (A/'env'/f'{s}.env').read_text().splitlines()
    out, changed = [], []
    for l in lines:
        k = l.split('=',1)[0] if '=' in l else None
        if k == 'JAVA_TOOL_OPTIONS':
            v = re.sub(r'-javaagent:\S+\s*', '', l.split('=',1)[1]).strip()
            out.append(f'{k}={v}'); changed.append('JAVA_TOOL_OPTIONS: bỏ -javaagent (image tự gắn)'); continue
        if k == 'OTEL_RESOURCE_ATTRIBUTES':
            kept = [p for p in l.split('=',1)[1].split(',') if p and p.split('=')[0] not in IDENT]
            if kept: out.append(f'{k}={",".join(kept)}')
            changed.append(f'OTEL_RESOURCE_ATTRIBUTES: bỏ khóa định danh (còn {len(kept)})'); continue
        if k in ('SERVICE_VERSION','OTEL_AGENT_ENABLED','SPRING_PROFILES_ACTIVE','FT_FAULTS_ENABLED','FT_FAULT_CONTROL_FILE','FT_FAULT_AUDIT_FILE'):
            continue
        out.append(l)
    out += [f'SERVICE_VERSION={SHA}', 'OTEL_AGENT_ENABLED=true']
    changed += ['SERVICE_VERSION=<commit T-062>', 'OTEL_AGENT_ENABLED=true']
    if s in FAULT:
        out += ['SPRING_PROFILES_ACTIVE=rca-test','FT_FAULTS_ENABLED=true',
                'FT_FAULT_CONTROL_FILE=/run/fault-control/control.json','FT_FAULT_AUDIT_FILE=/run/fault-audit/executions.jsonl']
        changed += ['SPRING_PROFILES_ACTIVE=rca-test','FT_FAULTS_ENABLED=true','FT_FAULT_*_FILE']
    p = envd/f'{s}.env'; p.write_text('\n'.join(out)+'\n'); os.chmod(p, 0o600)
    report[s] = {'thay_doi': changed, 'sha256_env_cu': hashlib.sha256((A/'env'/f'{s}.env').read_bytes()).hexdigest(),
                 'sha256_env_moi': hashlib.sha256(p.read_bytes()).hexdigest()}
# compose: bỏ mount /otel của host (image đã có agent 2.33.1), giữ mọi hardening khác
common = (A/'compose-exp'/'_common.yml').read_text()
common = common.replace('    volumes:\n      - /opt/flash-ticket-app/otel:/otel:ro\n', '')
assert '/otel' not in common
(cd/'_common.yml').write_text(common)
for s in SVCS:
    y = (A/'compose-exp'/f'{s}.yml').read_text().replace('../env/', '../env-t062/')
    if s in FAULT:
        y = y.rstrip('\n') + f'\n    volumes:\n      - /opt/flash-ticket-app/rca-faults/{s}/control:/run/fault-control:ro\n      - /opt/flash-ticket-app/rca-faults/{s}/audit:/run/fault-audit:rw\n'
    (cd/f'{s}.yml').write_text(y)
print(json.dumps(report, ensure_ascii=False, indent=1))

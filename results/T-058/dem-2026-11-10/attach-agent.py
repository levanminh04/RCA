#!/usr/bin/env python3
import datetime
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time

os.umask(0o077)
app=Path('/opt/flash-ticket-app')
root=Path('/home/ubuntu/t058')
images={x['service']:x for x in json.loads((root/'build-manifest.json').read_text())}
shutil.copytree(app/'compose',app/'compose-exp',dirs_exist_ok=True)
common=app/'compose-exp/_common.yml'
text=common.read_text()
if '/otel:ro' not in text:
    text+='    volumes:\n      - /opt/flash-ticket-app/otel:/otel:ro\n'
common.write_text(text)
keycloak=app/'compose-exp/keycloak.yml'
text=keycloak.read_text()
if '/otel:ro' not in text:
    text=text.replace('    volumes:\n','    volumes:\n      - /opt/flash-ticket-app/otel:/otel:ro\n',1)
keycloak.write_text(text)
inventory=json.loads((root/'env-inventory.json').read_text())
for svc,item in images.items():
    path=app/'env'/(svc+'.env')
    values=dict(x.split('=',1) for x in path.read_text().splitlines() if x and not x.startswith('#'))
    values.update({
      'JAVA_TOOL_OPTIONS':'-javaagent:/otel/opentelemetry-javaagent.jar -XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC -Dotel.instrumentation.common.logging.trace-id-key=traceId -Dotel.instrumentation.common.logging.span-id-key=spanId',
      'OTEL_SERVICE_NAME':svc,
      'OTEL_RESOURCE_ATTRIBUTES':'deployment.environment=exp,host.id=exp-app,service.instance.id='+svc+'-1,service.version='+item['commit'],
      'OTEL_EXPORTER_OTLP_ENDPOINT':'http://127.0.0.1:4318',
      'OTEL_EXPORTER_OTLP_PROTOCOL':'http/protobuf',
      'OTEL_TRACES_SAMPLER':'parentbased_always_on', 'OTEL_LOGS_EXPORTER':'none',
      'OTEL_METRIC_EXPORT_INTERVAL':'10000',
      'OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY':'traceId',
      'OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY':'spanId',
    })
    if svc!='keycloak':
        values.update(LOGGING_STRUCTURED_FORMAT_CONSOLE='logstash',INSTANCE_ID=svc+'-1',HOST_ID='exp-app',SERVICE_VERSION=item['commit'],ENVIRONMENT='exp')
    else:
        values['OTEL_EXPORTER_OTLP_ENDPOINT']='http://10.0.0.158:4318'
    path.write_text(''.join(k+'='+v+'\n' for k,v in sorted(values.items())))
    path.chmod(0o600)
    inventory[svc]=sorted(values)
(root/'env-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
ports={'discovery-server':8761,'keycloak':8080,'user-service':8085,'event-service':8086,
       'ticket-service':8084,'booking-service':8082,'payment-service':8083,'api-gateway':8081}
records=[]
for svc,port in ports.items():
    print(datetime.datetime.now(datetime.timezone.utc).isoformat(),svc,'ATTACH_AGENT',flush=True)
    env=dict(os.environ,IMAGE=images[svc]['image'])
    p=subprocess.run(['docker','compose','-f',str(app/'compose-exp'/(svc+'.yml')),'-p','flash-ticket-'+svc,'up','-d'],env=env)
    record={'service':svc,'compose_exit':p.returncode}
    deadline=time.monotonic()+150
    host='10.0.0.158' if svc in ['keycloak','api-gateway'] else '127.0.0.1'
    while p.returncode==0 and time.monotonic()<deadline:
        try:
            with socket.create_connection((host,port),timeout=2):
                record['listening']=True
            break
        except OSError:
            time.sleep(3)
    record['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    records.append(record)
    (root/'agent-startup.json').write_text(json.dumps(records,indent=2)+'\n')
    print(record,flush=True)
subprocess.run(['python3',str(root/'setup-collector.py')],check=True)
subprocess.run(['docker','compose','-f',str(app/'collector/compose.json'),'-p','flash-ticket-collector','up','-d','--force-recreate'],check=True)
(root/'agent-attached.done').touch()
print(datetime.datetime.now(datetime.timezone.utc).isoformat(),'AGENT_ATTACHED',flush=True)

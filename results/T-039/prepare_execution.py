"""Ghi phần nguồn chung OB, snapshot quyền và registry trước dựng; không lấy nguồn mới."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
OB = BASE / 'sources/augmented-ob-94a01ba4'
RUN = BASE / 'runs/trien-khai-001'
RUN.mkdir(parents=True, exist_ok=False)
(BASE / 'parts').mkdir(exist_ok=True)


def save(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


for name in ['manifest.json', 'nguon.json', 'ban-giao.md', 'kiem-dung-dan.md']:
    shutil.copyfile(BASE / name, RUN / ('before-' + name))
shutil.copyfile(ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md', RUN / 'LOG-open.md')
shutil.copyfile(BASE / 'fixtures/oracle.json', RUN / 'oracle-before-transform.json')
save(RUN / 'authorization.json', {'date_user': '2026-10-16', 'agent': 'Codex', 'role': 'implementer',
     'user_verbatim': 'làm trong 1 phiên, triển khai luôn giúp tôi nếu không còn vướng mắc nào',
     'scope': ['results/T-039/', 'append T039 LOG', 'T039 row of STATE only'],
     'common_pin': sha(ROOT / 'results/T-036/manifest.json'),
     'oracle_sha256_before_transform': sha(BASE / 'fixtures/oracle.json'),
     'new_download_authorized': False, 'existing_download_authorization': 'authorization-20261016.json',
     'meaning': 'Proceed full SPEC this session; preserve conditions/OPEN; no SPEC/shared code change'})
save(RUN / 'protected-before.json', [{'path': p, 'sha256': sha(ROOT / p)} for p in [
     'AGENTS.md', 'tasks/T-039-p5b-online-boutique/SPEC.md',
     'results/T-036/manifest.json', 'results/T-035/manifest.json',
     'src/do_thi_tinh/__init__.py', 'src/do_thi_tinh/build.py', 'src/do_thi_tinh/compare.py']])
doc = {'scope': {'system': 'Nezha-OB', 'revision': '94a01ba4c7c79e0c0b2c9da073ba081fcedc4bf1'},
       'entities': [], 'operations': [], 'relations': [], 'resource_bindings': [], 'signals': []}


def prov(path, loc, cond):
    return [{'source_id': 'OB:' + path, 'locator': loc, 'condition': cond}]


def entity(ident, typ, granularity, role, path, loc, cond):
    doc['entities'].append({'id': ident, 'name': ident, 'type': typ, 'granularity': granularity,
        'role': role, 'provenance': prov(path, loc, cond)})


def relation(ident, source, target, typ, channel, path, loc, cond):
    doc['relations'].append({'id': 'common:' + ident, 'source': {'entity': source, 'operation': None},
       'target': {'entity': target, 'operation': None}, 'type': typ, 'channel': channel,
       'messaging': None, 'context': cond, 'provenance': prov(path, loc, cond)})


entity('mysql', 'database', 'instance', 'data-instance', 'kubernetes-manifests/mysql.yaml', 'L1–45',
       'K8s mysql endpoint deployment candidate; runtime image/build/digest unverified')
for db, owner in [('addatabase', 'adservice'), ('Productdb', 'productcatalogservice')]:
    name = 'mysql/' + db
    entity(name, 'database', 'logical', 'datastore', 'hack/init_mysql.sql',
           'L1–15' if db == 'addatabase' else 'L91–129', 'SQL source candidate; actual initialization unverified')
    doc['resource_bindings'].append({'id': 'common:hosted:' + db, 'entity': name, 'resource': 'mysql',
         'relation': 'hosted_on', 'provenance': prov('hack/init_mysql.sql', 'L1–129',
            'candidate endpoint from adservice/productcatalog config; not a runtime placement claim') +
            prov('kubernetes-manifests/' + owner + '.yaml', 'env MYSQL_ADDR and database configuration',
                 'one mysql Service namespace hipster; no physical host inference')})
entity('redis-cart', 'cache', 'logical', 'datastore', 'kubernetes-manifests/redis.yaml', 'L15–67',
       'Redis variant; active only if selected manifest and REDIS_ADDR configured')
for ident, yaml, role in [('mysqld-exporter', 'mysql_exporter.yaml', 'mysql-metrics-exporter'),
                           ('redis-exporter', 'redis_exporter.yaml', 'redis-metrics-exporter')]:
    path = 'kubernetes-manifests/' + yaml
    entity(ident, 'service', 'component', role, path, 'container/exporter and service port declaration',
           'only start_with_istio_exporter variant; exporter implementation/image not inspected')
entity('otel-collector', 'external', 'component', 'observability', 'kubernetes-manifests/checkoutservice.yaml',
       'env COLLECTOR_ADDR', 'external configured collector; implementation/export schema absent from snapshot')
entity('istio-injection', 'unknown', 'component', 'deployment-template', 'kubernetes-manifests/start_demo_with_istio.sh',
       'L3–27', 'istioctl kube-inject is an external template dependency; not a concrete sidecar instance')
entity('web-client', 'external', 'logical', 'browser', 'src/frontend/templates/header.html', 'L19–34',
       'browser consumes HTML/assets; no browser telemetry supplied')
entity('frontend', 'service', 'logical', 'application', 'kubernetes-manifests/frontend.yaml', 'Deployment and Service frontend',
       'source revision candidate; runtime not verified')
for ident in ['stackpath.bootstrapcdn.com', 'fonts.googleapis.com', 'fonts.gstatic.com']:
    entity(ident, 'external', 'logical', 'browser-asset-origin', 'src/frontend/templates/header.html', 'L26–31',
           'external resource reference in browser HTML; not frontend server egress')
    relation('asset:' + ident, 'web-client', ident, 'gọi-đồng-bộ', 'http',
             'src/frontend/templates/header.html', 'L26–31', 'browser may fetch stylesheet/font when rendered; runtime unverified')
relation('browser:frontend', 'web-client', 'frontend', 'gọi-đồng-bộ', 'http',
         'kubernetes-manifests/frontend.yaml', 'L78–104', 'frontend exposed via Service; browser interaction candidate')
for service in ['frontend', 'cartservice', 'checkoutservice', 'productcatalogservice', 'currencyservice',
                'adservice', 'emailservice', 'paymentservice', 'recommendationservice', 'shippingservice']:
    p = 'kubernetes-manifests/' + service + '.yaml'
    entity(service, 'service', 'logical', 'application', p, 'Deployment/Service and SERVICE_NAME environment',
           'snapshot deployment candidate, not proof of dataset deployment')
    doc['signals'].append({'id': 'common:trace:' + service, 'kind': 'trace', 'entity': service,
       'operation': None, 'address': ['candidate-config', 'hipster', service, 'OTLP', 'COLLECTOR_ADDR'],
       'shared': False, 'provenance': prov(p, 'env SERVICE_NAME/COLLECTOR_ADDR',
         'address/config only; source schema and export to dataset unverified')})
doc['signals'].append({'id': 'common:metric:mysql', 'kind': 'metric', 'entity': 'mysql',
    'operation': None, 'address': ['candidate-exporter', 'hipster', 'mysql', '9104'], 'shared': True,
    'provenance': prov('kubernetes-manifests/mysql_exporter.yaml', 'L9–16,49–55',
        'exporter variant only; metric series not opened, schema/host not verified')})
doc['signals'].append({'id': 'common:metric:redis', 'kind': 'metric', 'entity': 'redis-cart',
    'operation': None, 'address': ['candidate-exporter', 'hipster', 'redis-cart', '9121'], 'shared': True,
    'provenance': prov('kubernetes-manifests/redis_exporter.yaml', 'L53–56,69–76',
        'exporter variant only; shared resource, no operation metric duplication')})
save(BASE / 'parts/common.json', doc)
print('Execution snapshot and independent oracle saved; common source fragment prepared.')

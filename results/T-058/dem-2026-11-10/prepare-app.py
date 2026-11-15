#!/usr/bin/env python3
"""Provision fresh experiment configuration on exp-app; never print secrets."""
import base64
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

os.umask(0o077)
repo = Path('/opt/flash-ticket-src')
app = Path('/opt/flash-ticket-app')
infra = Path('/opt/flash-ticket-infra')
revisions = json.loads(Path('/home/ubuntu/t058/revisions.json').read_text())['service']

def rand():
    return subprocess.check_output(['openssl', 'rand', '-hex', '24'], text=True).strip()

def template(text):
    return dict(re.findall(r'^([A-Z][A-Z0-9_]*)=(.*)$', text, re.M))

def private_file(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
    path.chmod(0o600)

def envfile(path, values):
    private_file(path, ''.join(f'{k}={v}\n' for k, v in sorted(values.items())))

if (app / 'env/.prepared').exists():
    raise SystemExit('Refuse to regenerate an existing secret set')

root = template((repo / '.env.example').read_text())
root.update({
    'POSTGRES_USER': 'postgres', 'POSTGRES_DB': 'keycloak_db',
    'POSTGRES_MEMORY_LIMIT': '1536m', 'PG_SHARED_BUFFERS': '256MB',
    'PG_MAX_CONNECTIONS': '120', 'RABBITMQ_MEMORY_LIMIT': '1g',
    'RABBITMQ_ADMIN_USERNAME': 'flash_ticket_admin',
    'RABBITMQ_USERNAME': 'flash_ticket_app',
    'RABBITMQ_IDENTITY_USERNAME': 'flash_ticket_identity',
    'RABBITMQ_HOST': '127.0.0.1', 'RABBITMQ_PORT': '5672',
    'RABBITMQ_MANAGEMENT_PORT': '15672', 'RABBITMQ_VHOST': '/',
    'REDIS_HOST': '127.0.0.1', 'REDIS_PORT': '6379',
    'SERVER_ADDRESS': '127.0.0.1', 'USER_DB_PORT': '27017',
    'KC_DB_URL': 'jdbc:postgresql://postgres:5432/keycloak_db',
    'KC_HOSTNAME': 'http://10.0.0.158:8080',
    'KC_BOOTSTRAP_ADMIN_USERNAME': 'admin',
    'KC_DB_POOL_MIN_SIZE': '2', 'KC_DB_POOL_INITIAL_SIZE': '2',
    'KC_DB_POOL_MAX_SIZE': '10', 'KC_HTTP_MAX_QUEUED_REQUESTS': '100',
    'EUREKA_SERVER_URL': 'http://127.0.0.1:8761/eureka/',
    'BOOKING_SERVICE_URL': 'http://127.0.0.1:8082',
    'INTERNAL_SERVICE_CLIENT_SECRET': rand(),
})
for name in list(root):
    if any(x in name for x in ['PASSWORD', 'CLIENT_SECRET']):
        root[name] = rand()
for name in ['POSTGRES_PASSWORD', 'REDIS_PASSWORD', 'KC_BOOTSTRAP_ADMIN_PASSWORD',
             'RABBITMQ_PASSWORD', 'RABBITMQ_ADMIN_PASSWORD', 'RABBITMQ_IDENTITY_PASSWORD',
             'USER_DB_ADMIN_PASSWORD', 'USER_DB_VIEWER_PASSWORD']:
    root.setdefault(name, rand())
for svc in ['EVENT', 'BOOKING', 'PAYMENT', 'TICKET']:
    for kind in ['ADMIN', 'VIEWER']:
        root.setdefault(f'{svc}_DB_{kind}_PASSWORD', rand())
envfile(repo / '.env', root)
envfile(infra / '.env', root)

# A separate deployment copy preserves the tracked source and relative mounts.
shutil.copytree(repo / 'deploy', infra / 'deploy', dirs_exist_ok=True)
# The official postgres entrypoint sources non-executable .sh files and passes
# its own positional arguments. This script expects initialize as argument 1.
# Making the deployment copy executable gives it a clean argv on fresh init.
(infra / 'deploy/postgres/00-business-databases.sh').chmod(0o755)
shutil.copytree(repo / 'docs/architecture/data', infra / 'docs/architecture/data', dirs_exist_ok=True)
for source in [repo / 'services/99-table-prefix.sql'] + list((repo / 'services').glob('*/database/90-erd-reader.sql')):
    dest = infra / source.relative_to(repo)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
for svc in ['event', 'booking', 'payment', 'ticket']:
    dest = infra / f'services/{svc}-service/database/90-erd-reader.sql'
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f'''\\set ON_ERROR_STOP on
\\connect {svc}_db
BEGIN;
GRANT CONNECT ON DATABASE {svc}_db TO {svc}_erd;
GRANT USAGE ON SCHEMA {svc}_schema TO {svc}_erd;
GRANT SELECT ON ALL TABLES IN SCHEMA {svc}_schema TO {svc}_erd;
ALTER DEFAULT PRIVILEGES FOR ROLE {svc}_owner IN SCHEMA {svc}_schema GRANT SELECT ON TABLES TO {svc}_erd;
COMMIT;
''')
        dest.chmod(0o644)
for filename in ['docker-compose.redis.yml', 'docker-compose.rabbitmq.yml']:
    p = infra / 'deploy' / filename
    p.write_text(p.read_text().replace('0.0.0.0:', '127.0.0.1:'))
# Use the requested MongoDB 7 line with the repository's fresh-init scripts.
p = infra / 'deploy/mongodb/compose.yaml'
text = p.read_text()
text = re.sub(r'(?m)^    image: mongo:.*$', '    image: mongo:7.0', text)
p.write_text(text)

realm = json.loads((repo / 'deploy/keycloak/import/flash-ticket-realm.json').read_text())
credentials = []
client_secrets = {}
for client in realm.get('clients', []):
    if not client.get('publicClient', False):
        secret = root['INTERNAL_SERVICE_CLIENT_SECRET'] if client['clientId'] == 'internal-service' else rand()
        client['secret'] = secret
        client_secrets[client['clientId']] = secret
for user in realm.get('users', []):
    if user.get('serviceAccountClientId'):
        continue
    password = rand()
    user['credentials'] = [{'type': 'password', 'value': password, 'temporary': False}]
    user['requiredActions'] = []
    credentials.append({'id': user.get('id'), 'username': user['username'], 'password': password,
                        'realmRoles': user.get('realmRoles', [])})
# No real SMTP service or third-party credential is used in this experiment.
realm['smtpServer'] = {}
import_dir = infra / 'keycloak/keycloak/import'
private_file(import_dir / 'flash-ticket-realm.json', json.dumps(realm, indent=2) + '\n')
# Keycloak runs with its image user, so the non-secret directory is traversable;
# the realm file contains generated secrets and is group-readable only by it.
import_dir.chmod(0o750)
os.chown(import_dir, 1000, 1000)
rp = import_dir / 'flash-ticket-realm.json'
os.chown(rp, 1000, 1000)
rp.chmod(0o640)
themes = repo / 'deploy/keycloak/themes'
if themes.exists():
    shutil.copytree(themes, infra / 'keycloak/keycloak/themes', dirs_exist_ok=True)
private_file(app / 'env/test-users.json', json.dumps(credentials, indent=2) + '\n')
private_file(app / 'env/client-secrets.json', json.dumps(client_secrets, indent=2) + '\n')

issuer = root['KC_HOSTNAME'] + '/realms/flash-ticket'
common = {
    'EUREKA_CLIENT_ENABLED': 'true', 'EUREKA_SERVER_URL': root['EUREKA_SERVER_URL'],
    'EUREKA_INSTANCE_PREFER_IP_ADDRESS': 'true', 'EUREKA_INSTANCE_IP_ADDRESS': '127.0.0.1',
    'SERVER_ADDRESS': '127.0.0.1', 'KEYCLOAK_ISSUER_URI': issuer,
    'KEYCLOAK_JWK_SET_URI': issuer + '/protocol/openid-connect/certs',
    'KEYCLOAK_TOKEN_URI': issuer + '/protocol/openid-connect/token',
    'KEYCLOAK_AUDIENCE': 'flash-ticket-api',
    'KEYCLOAK_IDENTITY_REALM_ID': realm['id'],
    'INTERNAL_SERVICE_CLIENT_SECRET': root['INTERNAL_SERVICE_CLIENT_SECRET'],
    'RABBITMQ_HOST': '127.0.0.1', 'RABBITMQ_PORT': '5672', 'RABBITMQ_VHOST': '/',
    'RABBITMQ_USERNAME': root['RABBITMQ_USERNAME'], 'RABBITMQ_PASSWORD': root['RABBITMQ_PASSWORD'],
    'RABBITMQ_BUSINESS_EXCHANGE': 'business.ex', 'REDIS_HOST': '127.0.0.1',
    'REDIS_PORT': '6379', 'REDIS_PASSWORD': root['REDIS_PASSWORD'],
    'JAVA_TOOL_OPTIONS': '-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC',
}
inventory = {}
for svc, spec in revisions.items():
    if svc == 'keycloak':
        continue
    raw = subprocess.check_output(['git','-C', str(repo), 'show', spec['commit']+':'+spec['path']+'/.env.example'], text=True)
    values = template(raw)
    values.update(common)
    prefix = svc.removesuffix('-service').replace('-', '_').upper()
    if svc == 'api-gateway':
        values.update(SERVER_ADDRESS='10.0.0.158', EUREKA_INSTANCE_IP_ADDRESS='10.0.0.158')
    if svc.endswith('-service'):
        values.update({f'{prefix}_ENVIRONMENT': 'exp', f'{prefix}_HOST_ID': 'exp-app',
                       f'{prefix}_INSTANCE_ID': svc+'-1', f'{prefix}_SERVICE_VERSION': spec['commit']})
        for key, val in common.items():
            if key.startswith('KEYCLOAK_') or key.startswith('RABBITMQ_') or key == 'INTERNAL_SERVICE_CLIENT_SECRET':
                values[prefix+'_'+key] = val
        if prefix != 'USER':
            values[prefix+'_DB_PASSWORD'] = root[prefix+'_DB_ADMIN_PASSWORD']
            values[prefix+'_DB_URL'] = f'jdbc:postgresql://127.0.0.1:5432/{prefix.lower()}_db?currentSchema={prefix.lower()}_schema'
            values[prefix+'_DB_USERNAME'] = prefix.lower()+'_admin'
    if svc == 'user-service':
        uri = 'mongodb://user_admin:'+root['USER_DB_ADMIN_PASSWORD']+'@127.0.0.1:27017/user_db?authSource=admin'
        values.update(MONGO_URI=uri, USER_MONGO_URI=uri,
                      USER_KEYCLOAK_ADMIN_BASE_URL=root['KC_HOSTNAME'],
                      USER_KEYCLOAK_ADMIN_REALM='flash-ticket', USER_KEYCLOAK_ADMIN_CLIENT_ID='user-management',
                      USER_KEYCLOAK_ADMIN_CLIENT_SECRET=client_secrets.get('user-management', rand()))
    if svc == 'event-service':
        values.update(EVENT_BOOKING_BASE_URL='http://127.0.0.1:8082', EVENT_PAYMENT_BASE_URL='http://127.0.0.1:8083', EVENT_SERVER_ADDRESS='127.0.0.1')
    if svc == 'payment-service':
        values.update(PAYMENT_SERVICE_CLIENT_SECRET=root['INTERNAL_SERVICE_CLIENT_SECRET'],
                      PAYMENT_SERVICE_TOKEN_URI=common['KEYCLOAK_TOKEN_URI'],
                      BOOKING_SERVICE_URL='http://127.0.0.1:8082', PAYMENT_DOCKER_BOOKING_URL='http://127.0.0.1:8082',
                      VNPAY_TMN_CODE='EXPERIMENT', VNPAY_HASH_SECRET=rand(),
                      VNPAY_API_URL='http://127.0.0.1:9/vnpay-unavailable',
                      VNPAY_PAYMENT_URL='http://127.0.0.1:9/vnpay-unavailable',
                      VNPAY_RETURN_URL='http://127.0.0.1:9/vnpay-return',
                      VNPAY_IPN_URL='http://127.0.0.1:9/vnpay-ipn',
                      PAYMENT_VNPAY_ENABLED='false', PAYMENT_VNPAY_CALLBACKS_ENABLED='false')
        values.pop('NGROK_AUTHTOKEN', None)
        values.pop('NGROK_DOMAIN', None)
    if svc == 'ticket-service':
        values.update(TICKET_QR_KEY_RING_LOCATION='file:/run/ticket-qr/key-ring.json', TICKET_QR_ACTIVE_KEY_VERSION='v1',
                      MAIL_HOST='127.0.0.1', MAIL_PORT='2525', MAIL_USERNAME='experiment', MAIL_PASSWORD=rand(),
                      MAIL_SMTP_AUTH='false', MAIL_SMTP_STARTTLS_ENABLE='false', MAIL_SMTP_STARTTLS_REQUIRED='false',
                      TICKET_MAIL_HEALTH_ENABLED='false', TICKET_MAIL_FROM='experiment@example.invalid',
                      TICKET_BUYER_BASE_URL='http://127.0.0.1:5173')
    for key in list(values):
        if ('IMAGES_API_' in key or 'IMAGE_API_' in key or key.endswith('CLOUD_NAME')):
            values[key] = ''
    envfile(app / 'env' / (svc+'.env'), values)
    inventory[svc] = sorted(values)
    shutil.copy2(repo / 'deploy/app' / (svc+'.yml'), app / 'compose' / (svc+'.yml'))
shutil.copy2(repo / 'deploy/app/_common.yml', app / 'compose/_common.yml')
# Remove the ngrok service entirely in the experiment copy (no dummy token).
p = app / 'compose/payment-service.yml'
p.write_text(p.read_text().split('\n  ngrok:', 1)[0]+'\n')
shutil.copy2(repo / 'deploy/app/keycloak.yml', app / 'compose/keycloak.yml')
p = app / 'compose/keycloak.yml'
p.write_text(p.read_text().replace('0.0.0.0:8080:', '10.0.0.158:8080:'))
kc = {
    'KC_DB': 'postgres', 'KC_DB_URL': root['KC_DB_URL'], 'KC_DB_USERNAME': root['POSTGRES_USER'],
    'KC_DB_PASSWORD': root['POSTGRES_PASSWORD'], 'KC_HOSTNAME': root['KC_HOSTNAME'],
    'KC_HTTP_ENABLED': 'true', 'KC_BOOTSTRAP_ADMIN_USERNAME': root['KC_BOOTSTRAP_ADMIN_USERNAME'],
    'KC_BOOTSTRAP_ADMIN_PASSWORD': root['KC_BOOTSTRAP_ADMIN_PASSWORD'],
    'KC_DB_POOL_MIN_SIZE': '2', 'KC_DB_POOL_INITIAL_SIZE': '2', 'KC_DB_POOL_MAX_SIZE': '10',
    'KC_HTTP_MAX_QUEUED_REQUESTS': '100', 'FT_IDENTITY_OUTBOX_ENABLED': 'true',
    'FT_IDENTITY_OUTBOX_INTERVAL_MS': '1000', 'FT_IDENTITY_RABBITMQ_HOST': 'rabbitmq',
    'FT_IDENTITY_RABBITMQ_PORT': '5672', 'FT_IDENTITY_RABBITMQ_VHOST': '/',
    'FT_IDENTITY_RABBITMQ_USERNAME': root['RABBITMQ_IDENTITY_USERNAME'],
    'FT_IDENTITY_RABBITMQ_PASSWORD': root['RABBITMQ_IDENTITY_PASSWORD'],
    'INTERNAL_SERVICE_CLIENT_SECRET': root['INTERNAL_SERVICE_CLIENT_SECRET'],
}
envfile(app / 'env/keycloak.env', kc)
key = subprocess.check_output(['openssl','rand','-base64','32'], text=True).strip()
private_file(app / 'secrets/ticket-qr/key-ring.json', json.dumps({'keys': {'v1': key}})+'\n')
os.chown(app / 'secrets/ticket-qr', 10001, 10001)
(app / 'secrets/ticket-qr').chmod(0o750)
os.chown(app / 'secrets/ticket-qr/key-ring.json', 10001, 10001)
(app / 'secrets/ticket-qr/key-ring.json').chmod(0o440)
inventory['keycloak'] = sorted(kc)
Path('/home/ubuntu/t058/env-inventory.json').write_text(json.dumps(inventory, indent=2)+'\n')
(app / 'env/.prepared').touch()
print('Prepared fresh secret set, service env, private realm import, QR ring, and deployment copies; no secret values printed.')

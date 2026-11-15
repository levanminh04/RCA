#!/usr/bin/env python3
"""Resume the failed fresh init only in its explicitly verified empty state."""
from pathlib import Path
import subprocess

infra=Path('/opt/flash-ticket-infra')
for svc in ['event','payment']:
    path=infra/f'services/{svc}-service/database/90-erd-reader.sql'
    assert path.resolve().is_relative_to(infra.resolve())
    if path.is_dir():
        path.rmdir()  # only Docker-created, empty mount-source directory
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'''\\set ON_ERROR_STOP on
\\connect {svc}_db
BEGIN;
GRANT CONNECT ON DATABASE {svc}_db TO {svc}_erd;
GRANT USAGE ON SCHEMA {svc}_schema TO {svc}_erd;
GRANT SELECT ON ALL TABLES IN SCHEMA {svc}_schema TO {svc}_erd;
ALTER DEFAULT PRIVILEGES FOR ROLE {svc}_owner IN SCHEMA {svc}_schema GRANT SELECT ON TABLES TO {svc}_erd;
COMMIT;
''')
    path.chmod(0o644)
original=(infra/'deploy/postgres/00-business-databases.sh').read_text()
original=original.replace("IF EXISTS (SELECT FROM pg_database WHERE datname IN ('event_db','booking_db','payment_db','ticket_db'))\n     OR EXISTS (SELECT FROM pg_roles WHERE rolname ~ '^(event|booking|payment|ticket)_(owner|admin|erd)$') THEN",
                          "IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'event_db') OR EXISTS (SELECT FROM pg_database WHERE datname IN ('booking_db','payment_db','ticket_db')) OR EXISTS (SELECT FROM pg_roles WHERE rolname ~ '^(booking|payment|ticket)_(owner|admin|erd)$') THEN")
needle='  psql -X -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" \\\n'
addition='''  if [ "$service" = event ]; then
    psql -X -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d event_db -f /opt/flash-ticket/readers/event.sql -f /opt/flash-ticket/99-table-prefix.sql
    continue
  fi
'''
assert needle in original
original=original.replace(needle,addition+needle,1)
path=Path('/home/ubuntu/t058/resume-business.sh')
path.write_text(original)
path.chmod(0o644)
print('Created missing inspection grants and guarded resume script; no database dropped.')

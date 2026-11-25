python3 - <<'PY'
import json
for l in open('/srv/flashticket-rca/alerts/bo-nhan/webhook.jsonl'):
    d=json.loads(l); b=json.loads(d['than'])
    print(d['nhan_webhook_utc'][:19], b.get('status'), [(a['labels'].get('t072_uid'), a['status'], a['startsAt'][:19]) for a in b.get('alerts',[])])
PY

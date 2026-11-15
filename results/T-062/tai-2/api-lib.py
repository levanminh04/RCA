# Appended after the pinned auth.py source; runs only in remote Python memory.
import datetime as dt
import time
import uuid

evidence = []
tokens = {}
def api(method, path, role=None, body=None, key=None):
    headers = {'Content-Type':'application/json'}
    if role:
        if role not in tokens:
            tokens[role] = role_token(role)
        headers['Authorization'] = 'Bearer ' + tokens[role]
    if key:
        headers['Idempotency-Key'] = key
    req = urllib.request.Request('http://10.0.0.158:8081'+path,
        data=None if body is None else json.dumps(body).encode(), headers=headers, method=method)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        response = urllib.request.urlopen(req, timeout=35)
    except urllib.error.HTTPError as error:
        response = error
    raw = response.read()
    try:
        value = json.loads(raw) if raw else {}
    except ValueError:
        value = {'nonJson':True}
    record = {'utc':started, 'method':method, 'path':path, 'status':response.code,
              'requestId':response.headers.get('X-Request-Id'),
              'correlationId':response.headers.get('X-Correlation-Id'),
              'returnedTraceId':response.headers.get('X-Trace-Id'),
              'role':role, 'bytes':len(raw)}
    if response.code >= 400:
        record['error'] = {k:value[k] for k in ['code','message','error','status','reasonCode','traceId'] if isinstance(value,dict) and k in value}
    evidence.append(record)
    return value.get('data',value) if isinstance(value,dict) else value

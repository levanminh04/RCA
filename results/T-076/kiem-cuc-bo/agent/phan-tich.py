"""T-076 bước 4: đọc payload thô (traces.jsonl, metrics.jsonl của Collector thử không processor), tìm sentinel giả,
liệt kê khóa thuộc tính theo loại span. In JSON tóm tắt.
    py -3 phan-tich.py <thư mục lượt>"""
import collections, json, pathlib, sys

D = pathlib.Path(sys.argv[1])
SENT = ['SENTINELTOKENQ', 'SENTINELHASHQ', 'SENTINELCODEQ', 'sentinel.email', 'sentinel.body', '0900111222',
        'SENTINELJWT', 'SENTINELCOOKIE', 'SENTINELBODY', 'SENTINELSECRET', 'SENTINELPATHBAD', 'token-thu-']
KIND = {1: 'INTERNAL', 2: 'SERVER', 3: 'CLIENT', 4: 'PRODUCER', 5: 'CONSUMER'}


def val(v):
    for k in ('stringValue', 'intValue', 'doubleValue', 'boolValue'):
        if k in v:
            return v[k]
    if 'arrayValue' in v:
        return [val(x) for x in v['arrayValue'].get('values', [])]
    return v


def attrs(lst):
    return {a['key']: val(a['value']) for a in lst or []}


tim = collections.defaultdict(list)       # sentinel -> nơi thấy
khoa = collections.defaultdict(collections.Counter)  # loại span -> khóa
tai_nguyen = {}
so_span = collections.Counter()
for f in ('traces.jsonl', 'metrics.jsonl'):
    p = D / f
    if not p.exists():
        continue
    raw = p.read_text(encoding='utf-8')
    for s in SENT:
        if s in raw:
            tim[s].append(f)
    if f != 'traces.jsonl':
        continue
    for line in raw.splitlines():
        if not line.strip():
            continue
        for rs in json.loads(line).get('resourceSpans', []):
            ra = attrs(rs.get('resource', {}).get('attributes'))
            tai_nguyen = {k: ra.get(k) for k in ('service.name', 'service.version', 'deployment.environment', 'host.id')}
            for ss in rs.get('scopeSpans', []):
                for sp in ss.get('spans', []):
                    loai = KIND.get(sp.get('kind'), str(sp.get('kind')))
                    so_span[loai] += 1
                    a = attrs(sp.get('attributes'))
                    khoa[loai].update(a.keys())
                    for ev in sp.get('events', []):
                        khoa[loai + ':event:' + ev.get('name', '')].update(attrs(ev.get('attributes')).keys())
                    blob = json.dumps(sp)
                    for s in SENT:
                        if s in blob:
                            for k, v in list(a.items()) + [('event:' + e.get('name', '') + '.' + kk, vv)
                                                           for e in sp.get('events', []) for kk, vv in attrs(e.get('attributes')).items()]:
                                if s in json.dumps(v):
                                    tim[s].append(f'{loai} {sp.get("name")} :: {k}')
print(json.dumps({'tai_nguyen': tai_nguyen, 'so_span': so_span,
                  'sentinel_thay': {k: sorted(set(v)) for k, v in tim.items()},
                  'sentinel_khong_thay': [s for s in SENT if s not in tim],
                  'khoa_theo_loai': {k: sorted(v) for k, v in sorted(khoa.items())}}, ensure_ascii=False, indent=1))

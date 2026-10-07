"""Timestamp-first lexical JSON framing. Never decode rejected record content.

Opaque byte framing is necessary to reach timestamps. It is not semantic parsing.
Only the record admitted by Gate may be passed to json.loads or a consumer.
"""
import collections
import datetime as dt
import json
import math
import re

TOKEN = re.compile(rb'\s*("(?:[^"\\]|\\.)*"|[{}\[\]:,]|[^\s{}\[\]:,"]+)', re.S)
NUMBER = re.compile(rb'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\Z')
LOG_DATE = re.compile(rb'^"(?:\[)?(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d(?:\.\d+)?)')
LOG_ALT = re.compile(rb'^"\[(\d{4}-[A-Za-z]{3}-\d\d \d\d:\d\d:\d\d(?:\.\d+)?)')


def value_end(data, start):
    """Return exclusive end of an opaque JSON value, None if chunk incomplete."""
    m = TOKEN.match(data, start)
    if not m:
        return None
    first = m.group(1)
    if first not in (b'{', b'['):
        return m.end()
    stack = [first]
    pos = m.end()
    while stack:
        m = TOKEN.match(data, pos)
        if not m:
            return None
        t = m.group(1)
        if t in (b'{', b'['):
            stack.append(t)
        elif t in (b'}', b']'):
            if (stack.pop(), t) not in ((b'{', b'}'), (b'[', b']')):
                raise ValueError('JSON bracket mismatch')
        pos = m.end()
    return pos


def fields(raw):
    """Object fields as raw key/value bytes; no decoded values or nested search."""
    raw = raw.strip()
    if raw[:1] != b'{':
        raise ValueError('object required')
    pos = 1
    first = True
    while True:
        m = TOKEN.match(raw, pos)
        if not m:
            raise ValueError('incomplete object')
        key = m.group(1)
        if key == b'}':
            if raw[m.end():].strip():
                raise ValueError('trailing object bytes')
            return
        if not first:
            if key != b',':
                raise ValueError('object comma required')
            m = TOKEN.match(raw, m.end())
            if not m:
                raise ValueError('incomplete object key')
            key = m.group(1)
        if not key.startswith(b'"'):
            raise ValueError('object key is not string')
        colon = TOKEN.match(raw, m.end())
        if not colon or colon.group(1) != b':':
            raise ValueError('missing colon')
        end = value_end(raw, colon.end())
        if end is None:
            raise ValueError('incomplete value')
        yield key, raw[colon.end():end].strip()
        pos = end
        first = False


def field(raw, name):
    # Field names are grammar/clock keys, not record payload. Normalize escapes so
    # startTime + \u0073tartTime is duplicate, not a timestamp gate bypass.
    matches = [v for k, v in fields(raw) if json.loads(k) == name]
    if len(matches) != 1:
        raise ValueError('missing or repeated field: ' + name)
    return matches[0]


def array_raw(raw):
    raw = raw.strip()
    if raw[:1] != b'[':
        raise ValueError('array required')
    pos = 1
    first = True
    while True:
        m = TOKEN.match(raw, pos)
        if not m:
            raise ValueError('incomplete array')
        if m.group(1) == b']':
            if raw[m.end():].strip():
                raise ValueError('trailing array bytes')
            return
        if not first:
            if m.group(1) != b',':
                raise ValueError('array comma required')
            pos = m.end()
            m = TOKEN.match(raw, pos)
            if not m or m.group(1) in (b',', b']'):
                raise ValueError('array value required after comma')
        end = value_end(raw, pos)
        if end is None:
            raise ValueError('incomplete array value')
        yield raw[pos:end].strip()
        pos = end
        first = False


def stream_array(reader):
    buf = b''
    opened = False
    need_comma = False
    after_comma = False
    while True:
        chunk = reader.read(65536)
        if chunk:
            buf += chunk
        if not opened:
            buf = buf.lstrip()
            if not buf:
                if chunk:
                    continue
                raise ValueError('empty JSON')
            if buf[:1] != b'[':
                raise ValueError('top level array required')
            buf = buf[1:]
            opened = True
        while True:
            buf = buf.lstrip()
            if need_comma and buf[:1] == b',':
                buf = buf[1:]
                need_comma = False
                after_comma = True
                continue
            if buf[:1] == b']':
                if after_comma:
                    raise ValueError('trailing array comma')
                # Consume trailing stream for hash; reject non-whitespace suffix.
                if buf[1:].strip() or reader.read().strip():
                    raise ValueError('trailing JSON')
                return
            if need_comma and buf:
                raise ValueError('stream array comma required')
            if buf[:1] == b',':
                raise ValueError('unexpected array comma')
            end = value_end(buf, 0)
            if end is None:
                break
            yield buf[:end]
            buf = buf[end:]
            need_comma = True
            after_comma = False
        if not chunk:
            raise ValueError('truncated JSON array')


class Gate:
    def __init__(self, policy, session):
        self.policy, self.session = policy, session
        self.counts = collections.Counter()
        self.classifications = collections.Counter()
        self.denied_intervals = collections.Counter()

    def accept(self, start, end=None):
        self.counts['total'] += 1
        if start is None or not math.isfinite(start) or (end is not None and (not math.isfinite(end) or end < start)):
            self.counts['unknown_clock'] += 1
            return False
        end = start if end is None else end
        denied = []
        classes = []
        for h, offset in self.policy['hypotheses_seconds'].items():
            found = False
            for x in self.policy['intervals']:
                if start + offset <= x['end_s'] and end + offset >= x['start_s']:
                    found = True
                    classes.append((h, x['session']))
                    if x['role'] in ('test', 'unlabelled'):
                        denied.append((h, x['session']))
            if not found:
                classes.append((h, 'outside_known_intervals'))
        if denied:
            self.counts['denied_B1'] += 1
            self.denied_intervals.update(denied)
            return False
        self.counts['admitted'] += 1
        self.classifications.update(classes)
        return True

    def result(self):
        return {'counts': dict(self.counts),
                'denied_by_interval_hypothesis': [{'hypothesis': h, 'interval': s, 'count': n}
                    for (h, s), n in sorted(self.denied_intervals.items())],
                'admitted_classifications': [{'hypothesis': h, 'interval': s, 'count': n}
                    for (h, s), n in sorted(self.classifications.items())]}


def span_clock(raw):
    try:
        start, duration = field(raw, 'startTime'), field(raw, 'duration')
        if not NUMBER.fullmatch(start) or not NUMBER.fullmatch(duration):
            return None, None
        start, duration = float(start) / 1e6, float(duration) / 1e6
        if duration < 0:
            return None, None
        return start, start + duration
    except (ValueError, OverflowError):
        return None, None


def admitted_spans(envelope, gate, decoder=json.loads):
    # Framing process map stays opaque. A process is resolved only for an admitted span.
    spans = field(envelope, 'spans')
    process_raw = None
    cache = {}
    for raw in array_raw(spans):
        start, end = span_clock(raw)
        if not gate.accept(start, end):
            continue
        span = decoder(raw)
        pid = span.get('processID')
        if pid not in cache:
            if process_raw is None:
                process_raw = field(envelope, 'processes')
            # Reject escaped process keys rather than silently last-wins aliases.
            process_fields = list(fields(process_raw))
            if any(b'\\' in k for k, v in process_fields):
                raise ValueError('escaped process key unsupported')
            candidates = [v for k, v in process_fields if k == json.dumps(pid).encode()]
            if len(candidates) != 1:
                cache[pid] = None
            else:
                cache[pid] = decoder(candidates[0]).get('serviceName')
        yield span, cache[pid], start, end


def log_clock(raw):
    # Only a fixed timestamp prefix is inspected. Remaining message is opaque.
    m = LOG_DATE.match(raw[:80]) or LOG_ALT.match(raw[:80])
    if not m:
        return None
    try:
        text = m.group(1).decode('ascii')
        fmt = '%Y-%b-%d %H:%M:%S' if re.search('[A-Za-z]', text) else '%Y-%m-%d %H:%M:%S'
        if '.' in text:
            fmt += '.%f'
        return dt.datetime.strptime(text, fmt).replace(tzinfo=dt.timezone.utc).timestamp()
    except ValueError:
        return None


def admitted_logs(rawmap, gate, decoder=json.loads):
    for service_key, values in fields(rawmap):
        service = None
        for raw in array_raw(values):
            timestamp = log_clock(raw)
            if not gate.accept(timestamp):
                continue
            if service is None:
                service = decoder(service_key)
            yield service, decoder(raw), timestamp


class Selector:
    def __init__(self, allow):
        if allow['status'] != 'approved':
            raise PermissionError('not approved')
        self.allow = allow
        self.members = {(m['origin'], m['member']): (s, m)
                        for s in allow['approved_sessions'] for m in s['members']}
        if len(self.members) != 145:
            raise PermissionError('unexpected member count')

    def require(self, origin, member):
        try:
            s, m = self.members[(origin, member)]
        except KeyError:
            raise PermissionError('member not approved') from None
        if origin in self.allow['denied_origins'] or s['session'] in self.allow['test_sessions'] + self.allow['unlabelled_sessions']:
            raise PermissionError('forbidden session/container')
        return s, m

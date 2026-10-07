"""One pass through 145 approved members, timestamp B1 before semantic records.

Only stdlib. No baseline, labels into model, offset correction, or raw output.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import sys
import tarfile
import time
import traceback
import zipfile
from b1_reader import Gate, Selector, admitted_logs, admitted_spans, stream_array

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-023'


def load(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))


def save(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def csvsave(p, rows):
    if not rows:
        p.write_text('', encoding='utf-8')
        return
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def digest_file(p):
    h = hashlib.sha256()
    n = 0
    with p.open('rb') as f:
        while b := f.read(1024 * 1024):
            h.update(b)
            n += len(b)
    return n, h.hexdigest()


class HashReader:
    def __init__(self, f):
        self.f, self.n, self.h = f, 0, hashlib.sha256()
    def read(self, n=-1):
        b = self.f.read(n)
        self.n += len(b)
        self.h.update(b)
        return b
    def readable(self):
        return True


def stats(values):
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return {'n': 0, 'invalid': len(values), 'min': None, 'q25': None, 'median': None,
                'q75': None, 'max': None, 'mean': None, 'sd': None}
    mean = math.fsum(vals) / len(vals)
    return {'n': len(vals), 'invalid': len(values) - len(vals), 'min': vals[0],
            'q25': vals[int((len(vals)-1)*.25)], 'median': vals[int((len(vals)-1)*.5)],
            'q75': vals[int((len(vals)-1)*.75)], 'max': vals[-1], 'mean': mean,
            'sd': math.sqrt(math.fsum((x-mean)**2 for x in vals) / len(vals))}


def identity_stats(rows, window=None):
    groups = collections.defaultdict(dict)
    multiplicity = collections.Counter()
    invalid_id_rows = 0
    for r in rows:
        if not all(isinstance(x, str) and re.fullmatch('[0-9a-fA-F]+', x) for x in r['key']):
            invalid_id_rows += 1
            continue
        groups[r['key']][r['signature']] = r
        multiplicity[(r['key'], r['signature'])] += 1
    chosen = {k: next(iter(v.values())) for k, v in groups.items() if len(v) == 1}
    count = collections.Counter(raw_rows=len(rows), unique_keys=len(groups),
                                invalid_id_rows=invalid_id_rows,
                                conflict_keys=sum(len(v) > 1 for v in groups.values()),
                                variants=sum(len(v) for v in groups.values()),
                                exact_extra_rows=sum(n-1 for n in multiplicity.values()))
    edges = collections.Counter()
    for key, r in chosen.items():
        if window and not (window[0] <= r['start'] < window[1]):
            continue
        count['usable_nonconflict_keys'] += 1
        if not r['refs']:
            count['root_no_CHILD_OF'] += 1
        if len(r['refs']) > 1:
            count['multiple_parent'] += 1
        for parent in r['refs']:
            count['parent_references'] += 1
            if parent not in groups:
                count['parent_missing_in_safe_set'] += 1
            elif len(groups[parent]) > 1:
                count['parent_conflicting'] += 1
            else:
                count['parent_unique_identity'] += 1
                if multiplicity[(parent, next(iter(groups[parent])))] > 1:
                    count['parent_repeated_exact'] += 1
                pr = chosen[parent]
                if window and not window[0] <= pr['start'] < window[1]:
                    count['parent_outside_window'] += 1
                if r['service'] and pr['service']:
                    edges[(pr['service'], r['service'])] += 1
    count['service_edges'] = [{'parent': a, 'child': b, 'count': n} for (a, b), n in sorted(edges.items())]
    return dict(count)


def windows(session, allow, events):
    bound = next(x for x in allow['B1']['intervals'] if x['session'] == session)
    result = [('session', bound['start_s'], bound['end_s'])]
    for e in events:
        if e['session'] == session and e['proposed_role'] == 'dev':
            idx = e['event_index']
            result += [('event-'+idx+'-pre', float(e['q64_pre_start_s']), float(e['injection_start_s'])),
                       ('event-'+idx+'-post', float(e['injection_start_s']), float(e['q64_post_end_s']))]
    return result


def trace_inspect(f, session, allow, events, run):
    gate = Gate(allow['B1'], session)
    rows = []
    tags = collections.Counter()
    for envelope in stream_array(f):
        for span, service, start, end in admitted_spans(envelope, gate):
            key = (span.get('traceID'), span.get('spanID'))
            refs = [(r.get('traceID'), r.get('spanID')) for r in span.get('references', []) if r.get('refType') == 'CHILD_OF']
            tagkeys = {t.get('key') for t in span.get('tags', [])}
            for tag in ('span.kind', 'http.status_code', 'error', 'hostname', 'peer.service', 'instance'):
                tags[tag] += int(tag in tagkeys)
            signature = hashlib.sha256(json.dumps([service, span], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            rows.append(dict(key=key, signature=signature, start=start, end=end, service=service,
                             operation=span.get('operationName'), refs=refs))
    summary = {'gate': gate.result(), 'identity': identity_stats(rows), 'tag_presence_admitted_rows': dict(tags),
               'native_start_stats_s': stats([r['start'] for r in rows]),
               'native_duration_stats_s': stats([r['end']-r['start'] for r in rows])}
    services = collections.Counter(r['service'] for r in rows)
    ops = collections.Counter((r['service'], r['operation']) for r in rows)
    summary['services_admitted_rows'] = dict(services)
    summary['operations_admitted_rows'] = [{'service': s, 'operation': o, 'count': n} for (s, o), n in sorted(ops.items(), key=str)]
    coverage = []
    for name, start, end in windows(session, allow, events):
        sub = [r for r in rows if start <= r['start'] < end]
        ids = identity_stats(rows, (start, end))
        coverage.append({'session': session, 'window': name, 'start_s': start, 'end_s': end,
                         'span_rows': len(sub), 'services': len({r['service'] for r in sub if r['service']}),
                         'distinct_seconds': len({int(r['start']) for r in sub}),
                         'nonconflict_keys': ids.get('usable_nonconflict_keys', 0),
                         'parent_missing_safe': ids.get('parent_missing_in_safe_set', 0),
                         'parent_conflicting': ids.get('parent_conflicting', 0),
                         'parent_outside_window': ids.get('parent_outside_window', 0)})
    summary['windows'] = coverage
    csvsave(run / (session + '-safe-spans.csv'), [dict(trace_id=r['key'][0], span_id=r['key'][1],
        signature=r['signature'], native_start_s=r['start'], native_end_s=r['end'], service=r['service'],
        operation=r['operation'], safe_parent_refs=json.dumps(r['refs'])) for r in rows])
    return summary, rows


LINK = re.compile(r'Span reported: ([0-9a-f]+):([0-9a-f]+):([0-9a-f]+):', re.I)


def log_inspect(f, session, allow, events):
    gate = Gate(allow['B1'], session)
    times = collections.defaultdict(list)
    levels = collections.Counter()
    links = []
    for service, message, timestamp in admitted_logs(f.read(), gate):
        times[service].append(timestamp)
        level = re.search(r'\b(TRACE|DEBUG|INFO|WARN|ERROR|FATAL)\b', message)
        levels[(service, level.group(1) if level else 'unknown')] += 1
        m = LINK.search(message)
        if m:
            links.append({'service': service, 'native_log_s': timestamp, 'trace_id': m[1], 'span_id': m[2], 'parent_id': m[3]})
    result = {'gate': gate.result(), 'services': {s: {'count': len(t), 'min_s': min(t), 'max_s': max(t),
                          'descending_adjacent': sum(b < a for a, b in zip(t, t[1:]))} for s, t in times.items()},
              'levels': [{'service': s, 'level': l, 'count': n} for (s, l), n in sorted(levels.items())],
              'windows': [{'session': session, 'window': name,
                           'lines': sum(sum(start <= t < end for t in ts) for ts in times.values()),
                           'services': sum(any(start <= t < end for t in ts) for ts in times.values())}
                          for name, start, end in windows(session, allow, events)],
              'span_reported_admitted': len(links)}
    return result, links


def metric_inspect(f, member, session, allow, events):
    text = f.read().decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text))
    channels = reader.fieldnames[1:]
    series = {c: [] for c in channels}
    timestamps = []
    for r in reader:
        timestamps.append(float(r['timestamp']))
        for c in channels:
            try:
                series[c].append(float(r[c]))
            except (ValueError, TypeError):
                series[c].append(float('nan'))
    service = Path(member).stem
    ws = windows(session, allow, events)
    # Fixed equal quarters of full normal session; no adaptive clean selection.
    a, b = timestamps[0], timestamps[-1] + 1
    if next(x['role'] for x in allow['approved_sessions'] if x['session'] == session) != 'dev':
        ws += [('quarter-'+str(k+1), a+(b-a)*k/4, a+(b-a)*(k+1)/4) for k in range(4)]
    rows = []
    for name, start, end in ws:
        ix = [i for i, t in enumerate(timestamps) if start <= t < end]
        ts = [timestamps[i] for i in ix]
        delta = collections.Counter(round(y-x, 6) for x, y in zip(ts, ts[1:]))
        for c in channels:
            st = stats([series[c][i] for i in ix])
            rows.append({'session': session, 'service': service, 'channel': c, 'window': name,
                         'start_s': start, 'end_s': end, 'first_sample_s': min(ts) if ts else None,
                         'last_sample_s': max(ts) if ts else None, 'duplicate_timestamps': len(ts)-len(set(ts)),
                         'cadence_non1': sum(v for d, v in delta.items() if d != 1),
                         'constant': st['n'] > 0 and st['min'] == st['max'], **st})
    return rows


def peak_working_set():
    try:
        import ctypes
        class PMC(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong),
                        ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                        ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
        pm = PMC()
        pm.cb = ctypes.sizeof(pm)
        handle = ctypes.windll.kernel32.GetCurrentProcess
        handle.restype = ctypes.c_void_p
        query = ctypes.windll.psapi.GetProcessMemoryInfo
        query.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
        query.restype = ctypes.c_int
        if not query(handle(), ctypes.byref(pm), pm.cb):
            return None
        return pm.PeakWorkingSetSize
    except Exception:
        return None


def main(run, fixture):
    started = time.monotonic()
    allow = load('results/T-023/allowlist-phien.json')
    assert load('results/T-023/runs/' + fixture + '/verification.json')['PASS']
    selector = Selector(allow)
    save(run / 'allowlist-snapshot.json', allow)
    save(run / 'progress.json', {'stage': 'hash_before_stream', 'elapsed_s': 0})
    n, h = digest_file(ROOT / allow['archive']['path'])
    assert n == allow['archive']['expected_bytes'] and h == allow['archive']['expected_sha256']
    save(run / 'archive-verification.json', {'PASS': True, 'bytes': n, 'sha256': h,
         'source': allow['archive']['source_manifest'], 'verified_before_any_member_open': True,
         'elapsed_s': time.monotonic()-started, 'testzip_called': False})
    events = list(csv.DictReader((OUT / 'runs/metadata-001/events.csv').open(encoding='utf-8-sig')))
    member_log, metric_rows, results = [], [], {}
    span_rows, link_rows = {}, {}
    def consume(origin, member, f):
        sess, expected = selector.require(origin, member)
        session = sess['session']
        results.setdefault(session, {'role': sess['role']})
        t0 = time.monotonic()
        reader = HashReader(f)
        if member.endswith('/spans.json'):
            tr, spans = trace_inspect(reader, session, allow, events, run)
            results[session]['trace'], span_rows[session] = tr, spans
        elif member.endswith('/logs.json'):
            logs, links = log_inspect(reader, session, allow, events)
            results[session]['log'], link_rows[session] = logs, links
        else:
            metric_rows.extend(metric_inspect(reader, member, session, allow, events))
        assert reader.read() == b''
        assert reader.n == expected['bytes'] and reader.h.hexdigest() == expected['sha256'], 'member hash mismatch'
        member_log.append({'session': session, 'origin': origin, 'member': member, 'bytes': reader.n,
                           'sha256': reader.h.hexdigest(), 'hash_PASS': True, 'elapsed_s': time.monotonic()-t0})
        csvsave(run / 'opened-members.csv', member_log)
        save(run / 'progress.json', {'stage': 'stream', 'members_done': len(member_log),
             'last_member': member, 'elapsed_s': time.monotonic()-started, 'peak_working_set_bytes': peak_working_set()})
        if member.endswith('/spans.json') or member.endswith('/logs.json'):
            print(session + ' ' + Path(member).name + ' complete', flush=True)
    with zipfile.ZipFile(ROOT / allow['archive']['path']) as archive:
        # ZIP central directory only; never testzip or open a denied archive/member.
        for origin, member in selector.members:
            if origin == 'outer':
                selector.require(origin, member)
                with archive.open(member) as f:
                    consume(origin, member, f)
        origins = sorted({o for o, m in selector.members if o != 'outer'})
        for origin in origins:
            assert origin not in allow['denied_origins']
            wanted = {m for o, m in selector.members if o == origin}
            observed = set()
            with archive.open(origin) as compressed:
                with tarfile.open(fileobj=compressed, mode='r|xz') as tar:
                    for entry in tar:
                        if not entry.isfile():
                            continue
                        selector.require(origin, entry.name)  # deny before extractfile
                        assert entry.name not in observed, 'repeated TAR member'
                        observed.add(entry.name)
                        with tar.extractfile(entry) as f:
                            consume(origin, entry.name, f)
            assert observed == wanted
    assert len(member_log) == 145 and len({(x['origin'], x['member']) for x in member_log}) == 145
    assert sum(x['bytes'] for x in member_log) == sum(m['bytes'] for s in allow['approved_sessions'] for m in s['members'])
    for session, summary in results.items():
        spans = span_rows[session]
        index = collections.defaultdict(list)
        for r in spans:
            index[r['key']].append(r)
        diffs = []
        counters = collections.Counter()
        safe_links = []
        for link in link_rows[session]:
            key = (link['trace_id'], link['span_id'])
            matches = index[key]
            unique = {r['signature']: r for r in matches}
            if not matches:
                counters['no_match_in_safe_set'] += 1
            elif len(unique) > 1:
                counters['conflicting_match'] += 1
            else:
                counters['unique_identity_match'] += 1
                r = next(iter(unique.values()))
                counters['service_agrees'] += int(r['service'] == link['service'])
                diffs.append(link['native_log_s'] - r['start'])
                safe_links.append({**link, 'span_native_start_s': r['start'],
                                   'native_log_minus_span_s': diffs[-1], 'same_service': r['service'] == link['service']})
        summary['native_identity_log_join'] = {'counts': dict(counters), 'time_difference_s': stats(diffs),
            'note': 'safe subset only, no offset applied; unmatched does not prove export orphan'}
        csvsave(run / (session + '-safe-log-links.csv'), safe_links)
    csvsave(run / 'metric-stats.csv', metric_rows)
    csvsave(run / 'trace-window-coverage.csv', [w for r in results.values() for w in r['trace']['windows']])
    csvsave(run / 'log-window-coverage.csv', [w for r in results.values() for w in r['log']['windows']])
    save(run / 'sessions.json', results)
    save(run / 'cost.json', {'elapsed_s': time.monotonic()-started, 'logical_member_bytes': sum(x['bytes'] for x in member_log),
                           'peak_working_set_bytes': peak_working_set(), 'members': len(member_log),
                           'no_download_install_EC2': True, 'baseline_run': False})
    save(run / 'progress.json', {'stage': 'complete', 'members_done': 145, 'elapsed_s': time.monotonic()-started})
    save(run / 'manifest.json', {'inputs': [{'path': p, 'bytes': digest_file(ROOT/p)[0], 'sha256': digest_file(ROOT/p)[1]}
          for p in ['results/T-023/allowlist-phien.json', 'results/T-023/ke-hoach-kiem.md',
                    'results/T-023/runs/metadata-001/events.csv',
                    'results/T-009/runs/inspect-004/raw-sessions.json',
                    'results/T-023/scripts/b1_reader.py', 'results/T-023/scripts/inspect_approved.py',
                    'results/T-023/scripts/check_b1.py']], 'fixture_run': fixture,
          'outputs': [{'path': str(p.relative_to(ROOT)).replace('\\', '/'), 'bytes': digest_file(p)[0], 'sha256': digest_file(p)[1]}
                      for p in sorted(run.iterdir()) if p.is_file()]})
    print('complete: 145 approved members, no forbidden member', flush=True)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser()
    p.add_argument('--run-id', required=True)
    p.add_argument('--fixture-run', required=True)
    args = p.parse_args()
    run = OUT / 'runs' / args.run_id
    run.mkdir(exist_ok=False)
    try:
        main(run, args.fixture_run)
    except Exception:
        (run / 'failure.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise

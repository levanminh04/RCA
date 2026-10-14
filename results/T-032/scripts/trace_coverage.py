"""T-032 observed trace intervals and coverage, EC2 only.

No RCA call, threshold, label, wait-time estimate or self-time estimate. Raw
payload stays in RAM. All source reads are restricted to frozen dev allowlists.
Each invocation creates a new run. Use fixture, one DATASET OPAQUE_ID, or cohort.
"""
import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import csv
from datetime import datetime, timezone
import hashlib
import heapq
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import time
import traceback

sys.dont_write_bytecode = True
BASE = Path('/home/ubuntu/rca/T-032')
REPO = BASE / 'repo'
PACKAGE_SHA = '03919f7895fedfd2aac8affd11d256acc5a4696341fed5812ef73c8ce417dec4'
CODE_ADDENDUM_SHA = 'f241b48cb0fd336aac5e6bf409cc811d945d99d6dee3ffcc1c4136ad8724974e'
SOURCE_TASKS = {'T-022', 'T-024', 'T-026', 'T-028', 'T-029', 'T-031'}
ROOT_MARKERS = {'root', '0', '0000000000000000'}
NS = 1_000_000_000
US = 1_000_000
OID = re.compile(r'^dev-[0-9a-f]{10}$')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key: ' + key)
        out[key] = value
    return out


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_object)


def write(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def progress(out, stage, **values):
    event = dict(utc=datetime.now(timezone.utc).isoformat(), stage=stage, **values)
    with (out / 'progress.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + '\n')
    print(json.dumps(event, ensure_ascii=False, allow_nan=False), flush=True)


def relative(name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('invalid relative source path')
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ('', '.', '..') for x in name.split('/')):
        raise ValueError('absolute/traversal source path')
    forbidden = {'locked', 'test', 'heldout', 'archive', 'T-033'}
    if any(x.lower() in {y.lower() for y in forbidden} for x in p.parts):
        raise ValueError('forbidden source path')
    return p


class Sources:
    def __init__(self):
        path = BASE / 'inputs/package-manifest.json'
        actual = sha(path)
        if actual != PACKAGE_SHA:
            raise ValueError('authorized package manifest hash mismatch')
        self.package = {r['path']: r['sha256'] for r in read(path)['files']}
        self.inputs = [dict(path=str(path), sha256=actual, expected=PACKAGE_SHA,
                            provenance='authorized T-032 source transfer')]
        self.checked = {}
        addendum = BASE / 'inputs/method-code-addendum-001.json'
        if sha(addendum) != CODE_ADDENDUM_SHA:
            raise ValueError('authorized source code addendum hash mismatch')
        extra = read(addendum)
        self.inputs.append(dict(path=str(addendum), sha256=CODE_ADDENDUM_SHA,
                                expected=CODE_ADDENDUM_SHA, provenance='authorized additional code transfer'))
        for row in extra['files']:
            if row['path'] in self.package and self.package[row['path']] != row['sha256']:
                raise ValueError('source code hash authorities disagree')
            self.package[row['path']] = row['sha256']

    def verify(self, name, expected=None, provenance='package-manifest.json#/files'):
        p = relative(name)
        if p.parts[0] == 'results':
            if len(p.parts) < 3 or p.parts[1] not in SOURCE_TASKS:
                raise ValueError('outside source-task scope')
        elif p.parts[0] != 'src':
            raise ValueError('outside source-code/result scope')
        path = (REPO / p).resolve()
        if not path.is_relative_to(REPO.resolve()):
            raise ValueError('source escapes task repo')
        wanted = expected or self.package.get(name)
        if wanted is None:
            raise ValueError('no frozen hash for ' + name)
        if name in self.package and self.package[name] != wanted:
            raise ValueError('source hash authorities disagree: ' + name)
        if name not in self.checked:
            actual = sha(path)
            self.checked[name] = actual
            self.inputs.append(dict(path=name, sha256=actual, expected=wanted,
                                    bytes=path.stat().st_size, provenance=provenance))
        if self.checked[name] != wanted:
            raise ValueError('frozen source hash mismatch: ' + name)
        return path

    def json(self, name, expected=None, provenance='package-manifest.json#/files'):
        return read(self.verify(name, expected, provenance))


def integer(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('not an integer')
    try:
        val = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('invalid integer') from exc
    if not val.is_finite() or val != int(val):
        raise ValueError('nonfinite/nonintegral integer')
    return int(val)


def text_id(value):
    if value is None or isinstance(value, float) and math.isnan(value):
        return None
    return str(value)


@dataclass(slots=True)
class Span:
    parent: object
    service: str
    operation: str
    start: object
    end: object
    duration: object
    signature: bytes
    source: str
    ordinal: int
    valid: bool
    rows: int = 1
    conflict: bool = False
    signatures: object = None
    scope_rows: object = None


class Inventory:
    def __init__(self, scopes):
        self.scopes = scopes
        self.nodes = {}
        self.rows = Counter()
        self.raw_checks = Counter()
        self.source_rows = Counter()
        self.nonempty_fields = Counter()
        self.examples = defaultdict(list)
        self.duplicate_rows = 0
        self.conflicting_rows = 0
        self.residual_min = None
        self.residual_max = None

    def example(self, code, source, ordinal):
        # Row locators, not raw payload, IDs or timestamp vectors.
        if len(self.examples[code]) < 5:
            self.examples[code].append(dict(source=source, data_row_ordinal_1based=ordinal))

    def memberships(self, start, end, valid):
        names = ['raw_source']
        if not valid:
            return names
        for name, (lo, t, hi, guard, kind) in self.scopes.items():
            outer = start >= lo and end < hi
            if not outer:
                continue
            if (kind == 'F' or kind == 'N_start' and start < t and (not guard or end < t - guard)
                    or kind == 'A_start' and start >= t
                    or kind == 'N_end' and end < t - guard
                    or kind == 'A_end' and end >= t
                    or kind == 'kept_end' and (end < t - guard or end >= t)
                    or kind == 'kept_start' and (start >= t or start < t and end < t - guard)):
                names.append(name)
        return names

    def add(self, row, dataset, aliases, source, ordinal):
        self.source_rows[source] += 1
        self.rows['raw_source'] += 1
        for field, value in row.items():
            if value is not None and str(value).strip() and not (
                    isinstance(value, float) and math.isnan(value)):
                self.nonempty_fields[field] += 1
        if dataset == 'RE2-TT':
            tid, sid, parent = (text_id(row[k]) for k in ('traceID', 'spanID', 'parentSpanID'))
            service, operation = text_id(row['serviceName']), text_id(row['operationName'])
            try:
                start, duration = integer(row['startTime']), integer(row['duration'])
                end = start + duration
            except ValueError:
                start = duration = end = None
            if start is not None and row.get('startTimeMillis') is not None:
                try:
                    mismatch = start // 1000 != integer(row['startTimeMillis'])
                except ValueError:
                    mismatch = True
                self.raw_checks['startTimeMillis_mismatch_rows'] += int(mismatch)
                if mismatch:
                    self.example('startTimeMillis_mismatch', source, ordinal)
        else:
            tid, sid, parent = (text_id(row[k]) for k in ('TraceID', 'SpanID', 'ParentID'))
            pod = text_id(row['PodName'])
            service = aliases.get(pod)
            operation = text_id(row['OperationName'])
            if service is None:
                self.raw_checks['unknown_pod_alias_rows'] += 1
                self.example('unknown_pod_alias', source, ordinal)
            try:
                start, end, duration = (integer(row[k]) for k in
                                       ('StartTimeUnixNano', 'EndTimeUnixNano', 'Duration'))
            except ValueError:
                start = duration = end = None
            if start is not None:
                residual = end - start - duration * 1000
                self.residual_min = residual if self.residual_min is None else min(self.residual_min, residual)
                self.residual_max = residual if self.residual_max is None else max(self.residual_max, residual)
                mismatch = not 0 <= residual < 1000
                self.raw_checks['End_minus_Start_vs_Duration_precision_mismatch_rows'] += int(mismatch)
                if mismatch:
                    self.example('duration_precision_mismatch', source, ordinal)
                for name, (_lo, t, hi, _guard, kind) in self.scopes.items():
                    if kind != 'F':
                        continue
                    us_end_ns = (start // 1000 + duration) * 1000
                    mismatch = (us_end_ns < t) != (end < t) or (us_end_ns < hi) != (end < hi)
                    self.raw_checks[name + '/ns_us_end_membership_mismatch_rows'] += int(mismatch)
        valid = start is not None and end >= start and duration >= 0
        if not valid:
            self.raw_checks['invalid_timing_rows'] += 1
            self.example('invalid_timing', source, ordinal)
        else:
            self.raw_checks['zero_interval_rows'] += int(end == start)
            for name, (lo, t, hi, guard, kind) in self.scopes.items():
                if kind != 'F':
                    continue
                checks = {'starts_exact_lo': start == lo, 'starts_exact_t': start == t,
                          'ends_exact_t': end == t, 'ends_exact_hi': end == hi,
                          'crosses_lo': start < lo < end, 'crosses_t': start < t < end,
                          'crosses_hi': start < hi < end, 'ends_before_lo': end <= lo,
                          'starts_at_or_after_hi': start >= hi,
                          'excluded_by_outer': not (start >= lo and end < hi)}
                for check, condition in checks.items():
                    self.raw_checks[name + '/' + check] += int(condition)
        names = self.memberships(start, end, valid)
        self.rows.update(x for x in names if x != 'raw_source')
        if not tid or not sid:
            self.raw_checks['missing_trace_or_span_id_rows'] += 1
            self.example('missing_id', source, ordinal)
            return
        if not service:
            self.raw_checks['missing_service_rows'] += 1
            self.example('missing_service', source, ordinal)
        signature = hashlib.sha256(json.dumps(row, sort_keys=True, default=str,
                                              separators=(',', ':'), allow_nan=True).encode()).digest()
        key = (tid, sid)
        existing = self.nodes.get(key)
        if existing is None:
            self.nodes[key] = Span(parent, service, operation, start, end, duration,
                                   signature, source, ordinal, valid)
            return
        if existing.scope_rows is not None:
            existing.scope_rows.update(names)
        known = {existing.signature} if existing.signatures is None else existing.signatures
        if signature in known:
            self.duplicate_rows += 1
        else:
            self.conflicting_rows += 1
            self.example('conflicting_key', source, ordinal)
            if not existing.conflict:
                existing.conflict = True
                existing.signatures = {existing.signature}
                initial = self.memberships(existing.start, existing.end, existing.valid)
                existing.scope_rows = Counter({name: existing.rows for name in initial})
                existing.scope_rows.update(names)
            existing.signatures.add(signature)
        existing.rows += 1

    def selected(self, name):
        return {key: span for key, span in self.nodes.items() if (
            name in span.scope_rows if span.scope_rows is not None else
            name in self.memberships(span.start, span.end, span.valid))}


def union(intervals):
    ordered = sorted((a, b) for a, b in intervals if b > a)
    if not ordered:
        return 0
    total, lo, hi = 0, *ordered[0]
    for a, b in ordered[1:]:
        if a > hi:
            total += hi - lo
            lo, hi = a, b
        else:
            hi = max(hi, b)
    return total + hi - lo


def intersecting_pairs(intervals):
    active, count = [], 0
    for lo, hi in sorted((a, b) for a, b in intervals if b > a):
        while active and active[0] <= lo:
            heapq.heappop(active)
        count += len(active)
        heapq.heappush(active, hi)
    return count


def cycle_nodes(parents):
    done, cycles = set(), set()
    for origin in parents:
        if origin in done:
            continue
        seen, chain, current = {}, [], origin
        while current in parents and current not in done and current not in seen:
            seen[current] = len(chain)
            chain.append(current)
            current = parents[current]
        if current in seen:
            cycles.update(chain[seen[current]:])
        done.update(chain)
    return cycles


def stat_add(stats, field, value):
    item = stats.setdefault(field, dict(n=0, sum=0, min=None, max=None))
    item['n'] += 1
    item['sum'] += value
    item['min'] = value if item['min'] is None else min(item['min'], value)
    item['max'] = value if item['max'] is None else max(item['max'], value)


def analyze(inv, name):
    selected = inv.selected(name)
    usable = {k: s for k, s in selected.items() if not s.conflict}
    sid_counts = Counter(k[1] for k in inv.nodes)
    counts = Counter(input_rows=inv.rows[name], selected_unique_keys=len(selected),
                     conflicting_keys_excluded=sum(s.conflict for s in selected.values()),
                     unique_usable_keys=len(usable), parent_field_nonempty_keys=0,
                     unique_trace_ids_selected=len({k[0] for k in selected}),
                     unique_trace_ids_usable=len({k[0] for k in usable}))
    selected_sids = Counter(k[1] for k in selected)
    counts['span_ids_reused_across_selected_traces'] = sum(n > 1 for n in selected_sids.values())
    counts['keys_with_span_id_reused_across_selected_traces'] = sum(n for n in selected_sids.values() if n > 1)
    edges, candidates = {}, {}
    resolution_rows = Counter()
    trace_issues, trace_parent_absence = set(), Counter()
    service_observations = {}
    for key, child in usable.items():
        service_row = service_observations.setdefault(child.service or '<missing>', dict(unique_keys=0, rows=0))
        service_row['unique_keys'] += 1
        service_row['rows'] += child.rows
        if child.parent in (None, ''):
            status = 'parent_field_absent'
            trace_parent_absence[key[0]] += 1
        else:
            counts['parent_field_nonempty_keys'] += 1
            pk = (key[0], child.parent)
            raw_parent = inv.nodes.get(pk)
            if pk == key:
                status = 'self_parent'
                candidates[key] = pk
            elif raw_parent is None:
                status = 'possible_root_marker_without_matching_parent' if child.parent in ROOT_MARKERS else 'parent_absent_authorized_source_set'
                if sid_counts[child.parent]:
                    counts['unresolved_parent_id_present_only_other_trace_keys'] += 1
            elif raw_parent.conflict:
                status = 'ambiguous_parent_conflicting_raw_key'
            elif pk not in usable:
                status = 'parent_in_raw_excluded_by_selected_scope'
            else:
                status = 'resolved_within_trace'
                edges[key] = pk
                candidates[key] = pk
                counts['resolved_cross_source_file_keys'] += int(child.source != raw_parent.source)
        counts[status + '_keys'] += 1
        if status not in ('parent_field_absent', 'possible_root_marker_without_matching_parent', 'resolved_within_trace'):
            trace_issues.add(key[0])
        resolution_rows[status] += child.rows
    cycles = cycle_nodes(candidates)
    counts['cycle_nodes_keys'] = len(cycles)
    counts['traces_with_any_cycle_nodes'] = len({k[0] for k in cycles})
    counts['traces_with_any_unresolved_ambiguous_self_or_scope_excluded_parent'] = len(trace_issues)
    absent_parent_histogram = Counter(trace_parent_absence[tid] for tid in {k[0] for k in usable})
    children = defaultdict(list)
    relations = {}
    for ck, pk in edges.items():
        child, parent = usable[ck], usable[pk]
        if ck in cycles or pk in cycles:
            counts['cycle_connected_edges_excluded_from_geometry'] += 1
            continue
        if not child.valid or not parent.valid or not child.service or not parent.service:
            counts['invalid_timing_or_service_edges_excluded_from_geometry'] += 1
            continue
        a, b = max(child.start, parent.start), min(child.end, parent.end)
        clipped = (a, max(a, b))
        counts['child_starts_before_parent_keys'] += int(child.start < parent.start)
        counts['child_ends_after_parent_keys'] += int(child.end > parent.end)
        counts['resolved_zero_overlap_keys'] += int(b <= a)
        counts['geometry_edge_keys'] += 1
        children[pk].append((ck, clipped))
        relation = (parent.service, parent.operation, child.service, child.operation)
        result = relations.setdefault(relation, dict(edge_keys=0, edge_rows_retained_by_methods=0,
                                                     parent_instances=0, clipped_overlap_interval_sum=0,
                                                     union_within_each_parent_interval_sum=0,
                                                     child_outside_parent_interval_sum=0))
        result['edge_keys'] += 1
        result['edge_rows_retained_by_methods'] += child.rows
        result['clipped_overlap_interval_sum'] += max(0, b - a)
        result['child_outside_parent_interval_sum'] += child.end - child.start - max(0, b - a)
    stats, service_stats = {}, {}
    for pk, parent in usable.items():
        if not parent.valid or not parent.service or pk in cycles:
            counts['parent_geometry_keys_excluded'] += 1
            continue
        direct = children.get(pk, [])
        intervals = [interval for _ck, interval in direct]
        covered = union(intervals)
        span_interval = parent.end - parent.start
        interval_sum = sum(max(0, b - a) for a, b in intervals)
        if not 0 <= covered <= span_interval or interval_sum < covered:
            raise ValueError('observed interval invariant failed')
        values = {'parent_interval': span_interval, 'direct_child_union_in_parent': covered,
                  'parent_interval_uncovered_by_observed_direct_children': span_interval - covered,
                  'direct_child_clipped_interval_sum': interval_sum,
                  'overlap_excess_from_summing_direct_children': interval_sum - covered,
                  'positive_overlap_direct_child_pairs': intersecting_pairs(intervals)}
        counts['parent_geometry_keys'] += 1
        counts['parents_with_observed_resolved_direct_children'] += int(bool(direct))
        for field, value in values.items():
            stat_add(stats, field, value)
            service = service_stats.setdefault(parent.service, {})
            stat_add(service, field, value)
        grouped = defaultdict(list)
        for ck, clipped in direct:
            child = usable[ck]
            grouped[(parent.service, parent.operation, child.service, child.operation)].append(clipped)
        for relation, segments in grouped.items():
            relations[relation]['parent_instances'] += 1
            relations[relation]['union_within_each_parent_interval_sum'] += union(segments)
    return dict(counts=dict(counts), parent_resolution_rows=dict(resolution_rows), interval_statistics=stats,
                observed_services=service_observations,
                traces_by_number_of_parent_field_absent_spans={str(k): v for k, v in sorted(absent_parent_histogram.items())},
                service_interval_statistics=service_stats,
                operation_relations=[dict(parent_service=k[0], parent_operation=k[1], child_service=k[2],
                                           child_operation=k[3], **v) for k, v in sorted(relations.items(),
                                                                                     key=lambda item: str(item[0]))],
                denominator_notes='Rows preserve source duplicates. Geometry uses unique nonconflicting IDs. '
                                  'Parent interval summaries include leaves; pair unions are nonadditive across child groups. '
                                  'Parent-field absence histogram does not establish complete/rooted requests.')


def definitions(dataset):
    return dict(interval='[start,end), observed timestamps only; zero-duration intervals have length zero',
                parent_join='Exact (traceID,parentSpanID) -> (traceID,spanID); never join by spanID alone',
                union='Union of clipped intervals of observed resolved direct children only; no descendant double counting',
                uncovered='parent observed interval length minus direct-child union; neither self-time nor wait time',
                overlap_excess='sum of clipped direct-child lengths minus their union; not pairwise summed overlap',
                rows_vs_keys='Method-facing duplicate rows are retained; structural geometry uses unique IDs and excludes conflicts/cycles',
                root_marker_policy='Null/empty parent is absence. Other prior-audit marker tokens are reported as possible markers '
                                   'only when no exact parent key exists; none establishes a real request root',
                source_unit='RE2 native startTime/duration units; frozen adapter assumes us; physical duration unit requires instrumentation provenance'
                            if dataset == 'RE2-TT' else 'ns endpoints; source Duration in us checked by 0 <= End-Start-Duration*1000 < 1000',
                causal_limit='Positive overlap, parent-child, containment, root markers and SpanKind alone do not prove synchronous waiting',
                coverage_limit='Within-authorized-source-set presence; no known denominator for total generated/sampled spans or requests',
                clock_limit='Intervals compare recorded timestamps; cross-host clock synchronization/error not established',
                window='Frozen F: start>=t-300 and end<t+300. Main start/end split and existing Nezha guard only; no new threshold')


def scopes_for(dataset, case, t):
    factor = US if dataset == 'RE2-TT' else NS
    views = [('main', t, 0)]
    if dataset == 'Nezha-OB':
        views.append(('trace_guard', t, case['trace_guard_s'] * NS))
        alternate = case.get('t_ns_sensitivity_A')
        views.append(('sensitivity_A', t if alternate is None else alternate, 0))
    result = {}
    for view, marker, guard in views:
        kinds = ['F', 'N_start', 'A_start', 'N_end', 'A_end']
        if guard:
            kinds.extend(['kept_end', 'kept_start'])
        for kind in kinds:
            result[view + '/' + kind] = (marker - 300 * factor, marker,
                                        marker + 300 * factor, guard, kind)
    return result


def raw_sources(reader, dataset, case):
    sources = []
    for name, meta in case['files'].items():
        if meta is None:
            continue
        rel = meta['path']
        p = relative(rel)
        if dataset == 'RE2-TT':
            if name != 'traces.parquet':
                continue
            if p.parts[:2] != ('data', 'rcaeval') or len(p.parts) != 4 or p.name != name:
                raise ValueError('trace outside RE2 dev locator contract')
            root = Path('/home/ubuntu/rca/T-031/repo')
            allowed_base = root / 'data/rcaeval'
        else:
            if '/trace/' not in rel:
                continue
            prefix = ('data', 'ngoai-rcaeval', 'nezha', 'online-boutique', 'rca_data')
            if (p.parts[:5] != prefix or len(p.parts) != 8 or
                    p.parts[5] not in ('2022-08-22', '2022-08-23') or p.parts[6] != 'trace' or
                    not re.fullmatch(r'\d{2}_\d{2}_trace\.csv', p.name)):
                raise ValueError('trace outside Nezha OB dev locator contract')
            root, allowed_base = REPO, REPO.joinpath(*prefix)
        path = root.joinpath(*p.parts).resolve()
        if not path.is_relative_to(allowed_base.resolve()):
            raise ValueError('raw locator escapes authorized dataset base')
        if path.stat().st_size != meta['bytes'] or sha(path) != meta['sha256']:
            raise ValueError('raw allowlist hash/size mismatch: ' + rel)
        reader.inputs.append(dict(path=rel, absolute_path=str(path), bytes=meta['bytes'],
                                  sha256=meta['sha256'], provenance='frozen dev allowlist#/cases/files'))
        sources.append((rel, path, meta))
    if not sources:
        raise ValueError('case has no allowlisted trace source')
    return sorted(sources, key=lambda row: row[0])


def schema_rows(path, dataset):
    if dataset == 'RE2-TT':
        import pyarrow.parquet as pq
        pf = pq.ParquetFile(path)
        schema = [{'name': f.name, 'type': str(f.type), 'nullable': f.nullable} for f in pf.schema_arrow]
        needed = {'traceID', 'spanID', 'parentSpanID', 'serviceName', 'operationName', 'startTime', 'duration'}
        if not needed <= {f['name'] for f in schema}:
            raise ValueError('RE2 trace schema missing required fields')
        def rows():
            for batch in pf.iter_batches(batch_size=65536):
                yield from batch.to_pylist()
        return schema, rows()
    stream = path.open(encoding='utf-8-sig', newline='')
    csv_reader = csv.DictReader(stream)
    names = csv_reader.fieldnames
    needed = {'TraceID', 'SpanID', 'ParentID', 'PodName', 'OperationName',
              'StartTimeUnixNano', 'EndTimeUnixNano', 'Duration'}
    if names is None or len(names) != len(set(names)) or not needed <= set(names):
        stream.close()
        raise ValueError('Nezha trace schema invalid')
    def rows():
        try:
            yield from csv_reader
        finally:
            stream.close()
    return [{'name': name, 'type': 'CSV source string'} for name in names], rows()


def preparation(reader):
    comparison = reader.json('results/T-029/runs/compare-rca-preparation-001/manifest.json')
    index24_name = 'results/T-024/ban-ghi-dua-vao-cham.json'
    index24 = reader.json(index24_name, comparison['source_hashes'][index24_name],
                          'T029 preparation manifest#/source_hashes')
    index26 = reader.json('results/T-026/ban-ghi-dua-vao-cham.json')
    for name in ('src/p3/cua_so.py', 'src/p3/worker.py', 'src/p3/selector.py',
                 'src/p3/nezha.py', 'src/p3/adapters/nezha.py', 'src/p3/adapters/simplerca.py',
                 'src/p3/adapters/microrank.py', 'src/p3/adapters/tracerca.py',
                 'src/p3/adapters/circa.py', 'src/p3/torai_b.py'):
        reader.verify(name, index26['source_hashes'][name], 'T026 frozen index#/source_hashes')
    for name in ('src/microrank/__init__.py', 'src/simplerca/adapter.py',
                 'src/circa_kien_truc/builder.py'):
        reader.verify(name, index26['source_hashes'].get(name), 'frozen code manifest')
    alias_source = reader.verify('src/p3/nezha.py')
    aliases = None
    for node in ast.parse(alias_source.read_text(encoding='utf-8-sig')).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'POD_ALIASES'
                                              for t in node.targets):
            aliases = ast.literal_eval(node.value)
    if not isinstance(aliases, dict):
        raise ValueError('no frozen explicit Nezha alias map')
    allow22 = reader.json('results/T-022/allowlist-dev.json')
    allow26 = reader.json('results/T-026/allowlist-dev.json',
                          index26['source_hashes']['results/T-026/allowlist-dev.json'],
                          'T026 frozen index#/source_hashes')
    allows = {'RE2-TT': allow22, 'Nezha-OB': allow26}
    for ds, allow in allows.items():
        cases = allow['cases']
        if allow['so_ca'] != len(cases) or len({x['opaque_id'] for x in cases}) != len(cases):
            raise ValueError('allowlist case count/identity mismatch')
        if any(not OID.fullmatch(x['opaque_id']) for x in cases):
            raise ValueError('non-dev opaque identity in allowlist')
    references = {'RE2-TT': index24['records'], 'Nezha-OB': index26['tables']['main']['records']}
    return allows, references, aliases


def case_marker(reader, dataset, case, references):
    refs = [r for r in references if r['opaque_id'] == case['opaque_id'] and
            r['method'] == 'baro' and r['variant'] == 'native' and r['seed'] is None]
    if len(refs) != 1:
        raise ValueError('ambiguous frozen reference for F')
    ref = refs[0]
    record = reader.json(ref['path'], ref['sha256'], 'frozen record index#/records')
    if record['opaque_id'] != case['opaque_id'] or record['mode'] != 'a':
        raise ValueError('frozen reference identity/mode mismatch')
    window = record['window']
    if dataset == 'RE2-TT':
        t = integer(window['t'])
        if window['N'] != [t - 300, t] or window['A'] != [t, t + 300]:
            raise ValueError('frozen F differs from approved contract')
        marker = t * US
    else:
        marker = integer(case['t_ns'])
        if (window['t_ns'] != marker or window['N_ns'] != [marker - 300 * NS, marker] or
                window['A_ns'] != [marker, marker + 300 * NS]):
            raise ValueError('Nezha metadata/frozen F disagreement')
    if dataset == 'RE2-TT':
        trace_refs = [r for r in references if r['opaque_id'] == case['opaque_id'] and
                      r['method'] == 'microrank' and r['variant'] == 'full' and r['seed'] is None]
        if len(trace_refs) != 1:
            raise ValueError('ambiguous frozen reference for trace F counts')
        trace_ref = trace_refs[0]
        trace_record = reader.json(trace_ref['path'], trace_ref['sha256'], 'T024 frozen record index#/records')
        trace_window = trace_record['window']
        if any(trace_window[k] != window[k] for k in ('t', 'N', 'A')):
            raise ValueError('frozen BARO/trace F disagreement')
        counts = {'main/N_start': trace_window['spans_N'], 'main/A_start': trace_window['spans_A']}
        count_source = dict(path=trace_ref['path'], json_pointer='/window', sha256=trace_ref['sha256'])
    else:
        counts = {'main/N_start': window['trace_rows_N_start'], 'main/A_start': window['trace_rows_A_start'],
                  'main/N_end': window['trace_rows_N_end'], 'main/A_end': window['trace_rows_A_end']}
        count_source = dict(path=ref['path'], json_pointer='/window', sha256=ref['sha256'])
    return marker, dict(path=ref['path'], json_pointer='/window', sha256=ref['sha256']), counts, count_source


def payload_contract(dataset, schemas):
    raw_fields = sorted({f['name'] for schema in schemas.values() for f in schema})
    common = dict(raw_fields=raw_fields, no_RCA_method_called=True,
                  method_views='Audit split descriptors only; source kernels are not altered or replayed here',
                  code_provenance='manifest.json#/inputs contains frozen worker/adapter code hashes')
    if dataset == 'RE2-TT':
        common['runner'] = 'Keeps full raw trace columns, applies F using startTime + duration'
        common['methods'] = {
            'baro': 'No trace input',
            'simplerca': 'Adapter passes serviceName,startTime,duration; core gets per-service duration arrays; IDs/parents/operation/status lost',
            'microrank': 'Raw F frame reaches adapter; core uses traceID,spanID,parentSpanID,serviceName,methodName,operationName,startTime,duration',
            'tracerca': 'Raw F frame reaches adapter; kernel field usage is not verified by this coverage invocation; consult frozen external code evidence separately',
            'circa': 'N-end trace supplies architecture parent links; RCA score uses metric graph rather than per-request intervals',
            'torai_B': 'Raw F spans become 15-second operation count/error tables; HTTP alias can use parent links; per-request IDs/intervals lost'}
    else:
        common['runner'] = 'Explicit PodName->service alias; OperationName duplicated as methodName; ns endpoints retained in internal payload; startTime=floor(ns/1000), Duration us; duplicate rows retained'
        common['methods'] = {
            'baro': 'No trace input',
            'simplerca': 'Core gets per-service Duration arrays from N/A start split; no request/parent/operation IDs; existing guard affects only N',
            'microrank': 'Standardized span frame reaches adapter after existing end-based N guard; IDs/parents retained; no SpanKind/attributes exist in raw schema',
            'tracerca': 'Same outer/end guard frame; kernel field usage is not verified by this coverage invocation; raw schema has no span type or await events',
            'circa': 'UNSUPPORTED; no method call', 'torai_B': 'UNSUPPORTED; no method call'}
    return common


def audit_case(reader, dataset, case, references, aliases, out):
    started = time.perf_counter()
    marker, marker_source, frozen_counts, count_source = case_marker(reader, dataset, case, references)
    inv = Inventory(scopes_for(dataset, case, marker))
    schemas = {}
    sources = raw_sources(reader, dataset, case)
    progress(out, 'RAW_HASH_PASS', dataset=dataset, opaque_id=case['opaque_id'], source_files=len(sources))
    for relative_path, path, meta in sources:
        schema, rows = schema_rows(path, dataset)
        schemas[relative_path] = schema
        for ordinal, row in enumerate(rows, 1):
            inv.add(row, dataset, aliases, relative_path, ordinal)
        if path.stat().st_size != meta['bytes'] or sha(path) != meta['sha256']:
            raise ValueError('raw source changed during audit')
        progress(out, 'SOURCE_READ', dataset=dataset, opaque_id=case['opaque_id'],
                 source=relative_path, source_rows=inv.source_rows[relative_path])
    profiles = {}
    count_checks = {scope: dict(expected=expected, actual=inv.rows[scope], passed=expected == inv.rows[scope])
                    for scope, expected in frozen_counts.items()}
    if any(not x['passed'] for x in count_checks.values()):
        write(out / ('count-mismatch-' + case['opaque_id'] + '.json'),
              dict(dataset=dataset, opaque_id=case['opaque_id'], checks=count_checks, source=count_source))
        raise ValueError('frozen method-facing F row-count mismatch')
    for scope in ['raw_source'] + list(inv.scopes):
        profiles[scope] = analyze(inv, scope)
        progress(out, 'SCOPE_DONE', dataset=dataset, opaque_id=case['opaque_id'], scope=scope)
    result = dict(status='STRUCTURE_AND_INTERVAL_AUDIT_ONLY', dataset=dataset, opaque_id=case['opaque_id'],
                  definitions=definitions(dataset), schemas=schemas, source_row_counts=dict(inv.source_rows),
                  raw_field_nonempty_row_counts=dict(inv.nonempty_fields), raw_checks=dict(inv.raw_checks),
                  duplicate_identical_raw_rows=inv.duplicate_rows, conflicting_raw_rows=inv.conflicting_rows,
                  conflict_unique_keys=sum(x.conflict for x in inv.nodes.values()),
                  duplicate_note='Signature hashes include all raw fields; identical duplicates collapsed for geometry only',
                  precision_residual_ns=dict(min=inv.residual_min, max=inv.residual_max),
                  issue_row_references=dict(inv.examples), frozen_F_source=marker_source,
                  frozen_method_facing_count_checks=count_checks, frozen_count_source=count_source,
                  scopes={name: dict(lo=v[0], t=v[1], hi=v[2], guard=v[3], split=v[4])
                          for name, v in inv.scopes.items()}, profiles=profiles,
                  payload_field_contract=payload_contract(dataset, schemas),
                  wait_capability=dict(status='OPEN_PENDING_INSTRUMENTATION_AND_CASE_INTERPRETATION',
                                       measured='Observed same-trace relations and intervals, subject to ambiguity/window/clock limits',
                                       not_established=['synchronous await/wait intervals', 'caller computation time',
                                                        'complete trace/request sampling coverage', 'cross-host clock error bound'],
                                       needed=['dataset instrumentation revision and exporter field lineage',
                                               'operation-level synchronous/async semantics or explicit await/blocking intervals',
                                               'clock synchronization/error and sampling policy/loss evidence']),
                  elapsed_s=time.perf_counter() - started)
    filename = dataset + '-' + case['opaque_id'] + '.json'
    write(out / filename, result)
    progress(out, 'CASE_PASS', dataset=dataset, opaque_id=case['opaque_id'], output=filename,
             elapsed_s=result['elapsed_s'])
    return dict(dataset=dataset, opaque_id=case['opaque_id'], path=filename,
                sha256=sha(out / filename), bytes=(out / filename).stat().st_size)


def fixture(out):
    checks = []
    def check(name, actual, expected):
        checks.append(dict(name=name, actual=actual, expected=expected, passed=actual == expected))
        if actual != expected:
            raise ValueError('fixture failed: ' + name)
    def make(rows, specs=None):
        inv = Inventory(specs or {'main/F': (0, 50, 100, 0, 'F')})
        for n, (tid, sid, parent, start, end) in enumerate(rows, 1):
            inv.add(dict(TraceID=tid, SpanID=sid, ParentID=parent, PodName='fixture-pod',
                         OperationName='fixture-op', StartTimeUnixNano=start,
                         EndTimeUnixNano=end, Duration=0), 'Nezha-OB', {'fixture-pod':'fixture-service'},
                    'synthetic_fixture', n)
        return inv
    nested = make([('t','p',None,0,100), ('t','c','p',10,90), ('t','g','c',20,80)])
    a = analyze(nested, 'raw_source')
    check('nested_direct_union_sum_no_descendant_double_count', a['interval_statistics']['direct_child_union_in_parent']['sum'], 140)
    check('nested_uncovered_interval_sum', a['interval_statistics']['parent_interval_uncovered_by_observed_direct_children']['sum'], 100)
    parallel = make([('t','p',None,0,100), ('t','c1','p',10,70), ('t','c2','p',40,90)])
    a = analyze(parallel, 'raw_source')
    check('parallel_union', a['interval_statistics']['direct_child_union_in_parent']['sum'], 80)
    check('parallel_overlap_excess', a['interval_statistics']['overlap_excess_from_summing_direct_children']['sum'], 30)
    check('parallel_overlap_pair_count', a['interval_statistics']['positive_overlap_direct_child_pairs']['sum'], 1)
    asynchronous = make([('t','p',None,0,100), ('t','c','p',70,140)])
    a = analyze(asynchronous, 'raw_source')
    check('async_extends_parent', a['counts']['child_ends_after_parent_keys'], 1)
    check('async_clipped_union', a['interval_statistics']['direct_child_union_in_parent']['sum'], 30)
    check('async_not_wait_semantics', definitions('Nezha-OB')['uncovered'], 'parent observed interval length minus direct-child union; neither self-time nor wait time')
    missing = make([('t','c','absent',10,30), ('other','absent',None,0,40)])
    a = analyze(missing, 'raw_source')
    check('missing_parent_within_trace', a['counts']['parent_absent_authorized_source_set_keys'], 1)
    check('cross_trace_parent_never_joined', a['counts']['unresolved_parent_id_present_only_other_trace_keys'], 1)
    boundary = make([('t','before',None,-10,10), ('t','at_lo',None,0,10),
                     ('t','at_hi',None,90,100), ('t','inside',None,10,99)])
    check('boundary_F_membership', analyze(boundary, 'main/F')['counts']['input_rows'], 2)
    check('raw_parent_present_but_window_excluded', analyze(make([('t','p',None,-1,99), ('t','c','p',10,20)]), 'main/F')['counts']['parent_in_raw_excluded_by_selected_scope_keys'], 1)
    identical = make([('t','p',None,0,99), ('t','c','p',10,20), ('t','c','p',10,20)])
    a = analyze(identical, 'raw_source')
    check('identical_duplicate_rows_reported', identical.duplicate_rows, 1)
    check('identical_duplicate_geometry_not_doubled', a['interval_statistics']['direct_child_union_in_parent']['sum'], 10)
    check('method_duplicate_rows_preserved', a['parent_resolution_rows']['resolved_within_trace'], 2)
    conflict = make([('t','p',None,0,99), ('t','p',None,1,99), ('t','c','p',10,20)])
    check('conflicting_parent_not_resolved', analyze(conflict, 'raw_source')['counts']['ambiguous_parent_conflicting_raw_key_keys'], 1)
    cyc = make([('t','a','b',0,90), ('t','b','a',0,90), ('t','s','s',0,90)])
    check('cycles_excluded', analyze(cyc, 'raw_source')['counts']['cycle_nodes_keys'], 3)
    invalid = make([('t','bad',None,20,10), ('t','zero',None,10,10)])
    check('invalid_interval', invalid.raw_checks['invalid_timing_rows'], 1)
    check('zero_interval', invalid.raw_checks['zero_interval_rows'], 1)
    guarded = make([('t','n',None,20,44), ('t','gap',None,30,46), ('t','cross',None,40,60)],
                   {'guard/N_start':(0,50,100,5,'N_start'), 'guard/N_end':(0,50,100,5,'N_end'),
                    'guard/A_start':(0,50,100,5,'A_start'), 'guard/A_end':(0,50,100,5,'A_end')})
    check('existing_guard_end_strict', analyze(guarded, 'guard/N_end')['counts']['input_rows'], 1)
    check('existing_guard_crossing_N_start_excluded', analyze(guarded, 'guard/N_start')['counts']['input_rows'], 1)
    check('existing_guard_A_end_unchanged', analyze(guarded, 'guard/A_end')['counts']['input_rows'], 1)
    combined = make([('t','n',None,20,44), ('t','gap',None,30,46), ('t','cross',None,40,60)],
                    {'guard/kept_end':(0,50,100,5,'kept_end'),
                     'guard/kept_start':(0,50,100,5,'kept_start')})
    check('existing_guard_combined_end_input', analyze(combined, 'guard/kept_end')['counts']['input_rows'], 2)
    check('existing_guard_combined_simple_input', analyze(combined, 'guard/kept_start')['counts']['input_rows'], 1)
    for n, segments in enumerate([[], [(0,0)], [(1,4),(2,3)], [(1,4),(4,6)],
                                  [(1,3),(5,8)], [(0,8),(2,4),(3,7)]]):
        oracle = len({x for lo, hi in segments for x in range(lo, hi)})
        check('union_grid_oracle_' + str(n), union(segments), oracle)
        pair_oracle = sum(min(b,d) > max(a,c) for i,(a,b) in enumerate(segments)
                          for c,d in segments[i+1:] if b>a and d>c)
        check('overlap_pair_oracle_' + str(n), intersecting_pairs(segments), pair_oracle)
    write(out / 'fixture-checks.json', dict(status='PASS', checks=checks,
                                          semantics='Synthetic geometry only; async fixture does not infer real waiting'))
    return [dict(path='fixture-checks.json', sha256=sha(out/'fixture-checks.json'),
                 bytes=(out/'fixture-checks.json').stat().st_size)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('fixture', 'one', 'cohort'))
    parser.add_argument('--dataset', choices=('RE2-TT','Nezha-OB'))
    parser.add_argument('--opaque-id')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if os.name != 'posix' or Path.home() != Path('/home/ubuntu'):
        raise RuntimeError('EC2-only script; no laptop research execution')
    if not Path(__file__).resolve().is_relative_to((BASE/'scripts').resolve()):
        raise RuntimeError('script must reside in authorized T-032/scripts')
    out = Path(args.out).resolve()
    if out.parent != (BASE / 'runs').resolve() or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', out.name):
        raise ValueError('output must be a new direct child of T-032/runs')
    if args.mode == 'one' and (args.dataset is None or not OID.fullmatch(args.opaque_id or '')):
        raise ValueError('one requires a dataset and dev opaque identity')
    if args.mode == 'fixture' and (args.dataset is not None or args.opaque_id is not None):
        raise ValueError('fixture must not select source data')
    if args.mode == 'cohort' and args.opaque_id is not None:
        raise ValueError('cohort cannot select a single opaque identity')
    out.mkdir(parents=True, exist_ok=False)
    started, reader, outputs = time.perf_counter(), None, []
    try:
        progress(out, 'START', command=sys.argv, script_sha256=sha(Path(__file__)))
        if args.mode == 'fixture':
            outputs = fixture(out)
        else:
            reader = Sources()
            allows, refs, aliases = preparation(reader)
            cohorts = [args.dataset] if args.dataset else ['RE2-TT','Nezha-OB']
            for ds in cohorts:
                cases = allows[ds]['cases']
                if args.mode == 'one':
                    cases = [x for x in cases if x['opaque_id'] == args.opaque_id]
                    if len(cases) != 1:
                        raise ValueError('case not in frozen dev allowlist')
                for case in sorted(cases, key=lambda x: x['opaque_id']):
                    progress(out, 'CASE_START', dataset=ds, opaque_id=case['opaque_id'])
                    outputs.append(audit_case(reader, ds, case, refs[ds], aliases, out))
        manifest = dict(status='PASS_OBSERVATION_AUDIT_ONLY', command=sys.argv,
                        script_sha256=sha(Path(__file__)), elapsed_s=time.perf_counter()-started,
                        inputs=[] if reader is None else reader.inputs, outputs=outputs,
                        limits='No wait/self-time classification or RCA conclusions; raw payload not persisted')
        write(out / 'manifest.json', manifest)
        progress(out, 'PASS', cases=len(outputs) if args.mode != 'fixture' else 0,
                 elapsed_s=manifest['elapsed_s'])
    except BaseException as exc:
        write(out / 'failure.json', dict(status='FAIL', error=str(exc), traceback=traceback.format_exc(),
                                         elapsed_s=time.perf_counter()-started, outputs_completed=outputs,
                                         inputs=[] if reader is None else reader.inputs,
                                         script_sha256=sha(Path(__file__))))
        progress(out, 'FAIL', error=str(exc))
        raise


if __name__ == '__main__':
    main()

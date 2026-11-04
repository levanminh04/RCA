"""Giải thích delta T1 trước/sau C1 bằng đầu vào và hai API cổng độc lập.

Không đọc nhãn, E_X hoặc kết quả chấm. Không chạy whole M1, không monkeypatch.
Chạy riêng cho lượt thật (52 ca) và C-e (30 ca): --old <lượt cũ> --new
<lượt C1 đã hoàn tất> --run <thư mục audit mới trong T-047>.
Chỉ EXPLAINED khi mẫu thô tái lập đầy đủ đơn vị native ở cả hai API và
mọi delta đã được phân xử. Downstream chưa phân xử giữ OPEN, kể cả p-only.
"""
import argparse
import ast
import collections
import hashlib
import json
import math
import subprocess
import sys
import time
import types
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts')]
import adapter_t047 as ad
import tep_pha1
from m1 import adapter, chuoi, cong, e4, runner, span
from p3 import nezha, selector

OLD_REV = 'c298188e'
C1_REV = '6d9744ab'
NS = 10 ** 9


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def git_source(rev, name):
    return subprocess.check_output(['git', 'show', f'{rev}:{name}'], cwd=ROOT)


def _text(data):
    return data.decode('utf-8-sig').replace('\r\n', '\n')


def frozen_source():
    """Hai namespace riêng; chỉ hai function đã duyệt được khác trong src."""
    name = 'src/m1/cong.py'
    old_bytes, fixed_bytes = git_source(OLD_REV, name), git_source(C1_REV, name)
    current = (ROOT / name).read_bytes()
    if _text(current) != _text(fixed_bytes):
        raise ValueError('src/m1/cong.py hiện tại khác commit C1 đã duyệt')
    def tree_parts(data):
        tree = ast.parse(_text(data))
        functions = {x.name: ast.dump(x, include_attributes=False) for x in tree.body
                     if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))}
        other = [ast.dump(x, include_attributes=False) for x in tree.body
                 if not isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))]
        return functions, other
    a, ao = tree_parts(old_bytes)
    b, bo = tree_parts(current)
    changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    if changed != ['o_1s', 'tu_tuong_quan'] or ao != bo:
        raise ValueError('C1 không còn đúng phạm vi hai function đã duyệt')
    sources = {}
    for module in (adapter, chuoi, e4, runner, span, cong, selector, nezha):
        path = Path(module.__file__).resolve()
        rel = path.relative_to(ROOT).as_posix()
        expected = fixed_bytes if module is cong else git_source(OLD_REV, rel)
        data = path.read_bytes()
        if _text(data) != _text(expected):
            raise ValueError('source phụ thuộc đổi ngoài C1: ' + rel)
        sources[rel] = dict(sha256=digest(data), git_sha256=digest(expected))
    old = types.ModuleType('T047_cong_frozen_c298188e')
    old.__file__ = f'{OLD_REV}:{name}'
    exec(compile(_text(old_bytes), old.__file__, 'exec'), old.__dict__)
    return old, dict(old_revision=OLD_REV, new_revision=C1_REV, changed_functions=changed,
                     old_source_sha256=digest(old_bytes), sources=sources)


def delta_fields(before, after, pointer=''):
    """Toàn bộ delta, giữ cả trường có/mất; không cắt ví dụ hoặc độ sâu."""
    if isinstance(before, dict) and isinstance(after, dict):
        out = []
        for key in sorted(set(before) | set(after)):
            p = pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')
            if key not in before or key not in after:
                out.append(dict(pointer=p, before=before.get(key), after=after.get(key),
                                before_present=key in before, after_present=key in after))
            else:
                out.extend(delta_fields(before[key], after[key], p))
        return out
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [row for i, (a, b) in enumerate(zip(before, after))
                for row in delta_fields(a, b, pointer + '/' + str(i))]
    return [] if before == after else [dict(pointer=pointer or '/', before=before, after=after,
                                           before_present=True, after_present=True)]


def audit_intermediates(api, N, mN, A, mA, t_ns, bounds):
    o = api.o_1s(mN, N, t_ns, 'N')
    # C1 orders keys explicitly; frozen code reduces in insertion order.
    order = sorted(o, reverse=True) if api is cong else list(o)
    values = np.array([o[j] for j in order], float)
    mean = float(values.mean()) if len(values) else None
    variance = float(((values - mean) ** 2).mean()) if len(values) else None
    rho, reason = api.tu_tuong_quan(o)
    kb = api.chuan_bi_khoi(N, mN, A, mA, t_ns, *bounds)
    products = {} if rho is None else {
        str(k): dict(pairs=[j for j in order if j + k in o],
                     values=[(o[j] - mean) * (o[j + k] - mean) for j in order if j + k in o])
        for k in range(1, api.K_MAX + 1)}
    return dict(o_1s=[dict(j=j, value=o[j]) for j in o], reduction_order=order,
                mean=mean, variance=variance,
                rho={str(k): value for k, value in rho.items()} if rho is not None else None, rho_reason=reason,
                lag_products=products, b=kb.get('b'), roi_G0=kb.get('roi_G0'),
                blocks_N={str(k): v for k, v in (kb.get('khoi_N') or {}).items()},
                blocks_A={str(k): v for k, v in (kb.get('khoi_A') or {}).items()})


def explain_unit(raw, old_unit, new_unit, ts, old_api):
    """Tái tính cùng mẫu N/A và đúng API; p-only chưa thay thế phép kiểm này."""
    N, mN, A, mA = (raw[k] for k in ('N', 'mN', 'A', 'mA'))
    if len(N) != len(mN) or len(A) != len(mA):
        raise ValueError('mốc và giá trị không cùng chiều dài')
    directions = tuple(d for d in ('len', 'xuong') if old_unit.get('p_' + d) is not None
                       or new_unit.get('p_' + d) is not None)
    if not directions or old_unit['ma'] != new_unit['ma']:
        raise ValueError('đơn vị đổi không đủ hướng hoặc đổi mã')
    ma = old_unit['ma']
    min_samples = int(ts['m_metric'] if ma.startswith('metric|') else ts['m_span'])
    actual, facts, mismatches = {}, {}, {}
    for version, api, native in (('before', old_api, old_unit), ('after', cong, new_unit)):
        def gate(d):
            return api.p_theo_G3(N, mN, A, mA, raw['t_ns'], *raw['bounds'], d, ts, ma)
        computed = e4.cham_phan_vi(N, A, min_samples, ts, huong_cham=directions, ham_p=gate)
        slim = chuoi._gon_pv(ma, computed)
        actual[version] = slim
        mismatches[version] = delta_fields(native, slim)
        facts[version] = audit_intermediates(api, N, mN, A, mA, raw['t_ns'], raw['bounds'])
    out = dict(ma=ma, directions=directions, native_before=old_unit, native_after=new_unit,
               recomputed=actual, native_mismatches=mismatches,
               input=dict(N=N, mN=mN, A=A, mA=mA, t_ns=raw['t_ns'], bounds=raw['bounds'],
                          provenance=raw['provenance']), intermediates=facts,
               p={d: dict(before=old_unit.get('p_' + d), after=new_unit.get('p_' + d),
                           recomputed_before=actual['before'].get('p_' + d),
                           recomputed_after=actual['after'].get('p_' + d)) for d in directions},
               F_raw={d: dict(before=old_unit.get('F_raw_' + d), after=new_unit.get('F_raw_' + d))
                      for d in ('len', 'xuong')})
    out['status'] = 'OPEN' if any(mismatches.values()) else 'EXPLAINED_BY_C1_ON_IDENTICAL_RAW'
    out['explanation'] = ('Mẫu/mốc không đổi; source chỉ đổi o_1s/tu_tuong_quan. '
                          'Audit giữ phép cộng ô, thứ tự giảm, mean/variance, từng tích theo lag, rho, b và p. '
                          'Chỉ công nhận giải thích khi tái lập toàn bộ trường đơn vị native ở cả hai phiên bản.')
    return out


def _file_provenance(path, role):
    path = Path(path)
    return dict(file=path.relative_to(ROOT).as_posix(), sha256=selector.sha256_file(path), role=role)


class RawInputs:
    """Nạp chỉ đầu vào cần để giải thích, không gọi chuoi.chay hoặc nhan."""
    def __init__(self):
        contract_rel = 'results/T-043/hop-dong.json'
        manifest = json.loads((ROOT / 'results/T-043/manifest.json').read_text(encoding='utf-8'))
        contract_hash = next(x['sha256'] for x in manifest['outputs'] if x['path'] == contract_rel)
        pins_path = ROOT / 'results/T-022/mappings/universe-re2tt-dev.json'
        pins = json.loads(pins_path.read_text(encoding='utf-8'))['nguon']
        handoff_path = ROOT / 'results/T-026/runs/session-005/handoff-manifest.json'
        handoff = json.loads(handoff_path.read_text(encoding='utf-8'))['files']
        controls = {contract_rel: contract_hash,
                    'results/T-022/allowlist-dev.json': pins['results/T-022/allowlist-dev.json'],
                    'results/T-026/allowlist-dev.json': handoff['results/T-026/allowlist-dev.json']['sha256']}
        for rel, expected in controls.items():
            if selector.sha256_file(ROOT / rel) != expected:
                raise ValueError('hash nguồn điều khiển raw lệch: ' + rel)
        self.controls = dict(verified=controls,
                             allowlist_re_pin=_file_provenance(pins_path, 'allowlist pin'),
                             allowlist_nezha_manifest=_file_provenance(handoff_path, 'allowlist manifest'))
        self.re = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
        self.nz = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
        self.contract = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
        self.cache = {}

    def dataset(self, oid):
        if oid in self.re and oid not in self.nz:
            return 'RE2-TT'
        if oid in self.nz and oid not in self.re:
            return 'Nezha-OB'
        raise ValueError('opaque_id không thuộc đúng một allowlist dev')

    def one(self, oid, rec, ma):
        ds = self.dataset(oid)
        t_ns = rec['window']['A'][0]
        lo, hi = rec['window']['N'][0], rec['window']['A'][1]
        if t_ns % NS or t_ns - lo != 300 * NS or hi - t_ns != 300 * NS:
            raise ValueError('miền native không khớp 300 giây mỗi phía')
        if ds == 'RE2-TT' and ma.startswith('metric|'):
            cot = ma.split('|', 1)[1]
            files = selector.chon_ca(self.re, oid, ROOT, tep=['metrics.parquet'])
            path = files['metrics.parquet']
            frame = pq.read_table(path, columns=['time', cot]).to_pandas()
            rows = [(int(t) * NS, float(v)) for t, v in frame[['time', cot]].itertuples(index=False, name=None)
                    if adapter._so(v) is not None and lo <= int(t) * NS < hi]
            source = 'metric'
            provenance = [_file_provenance(path, 'metric column ' + cot)]
            N, mN = [v for t, v in rows if t < t_ns], [t for t, v in rows if t < t_ns]
            A, mA = [v for t, v in rows if t >= t_ns], [t for t, v in rows if t >= t_ns]
        else:
            key = (oid, t_ns)
            if key not in self.cache:
                if ds == 'RE2-TT':
                    files = selector.chon_ca(self.re, oid, ROOT, tep=['traces.parquet'])
                    path = files['traces.parquet']
                    frame = pq.read_table(path, columns=adapter.COT_SPAN_RE2).to_pandas()
                    raw_spans = []
                    for a, b, c, d, e, f, g in frame[adapter.COT_SPAN_RE2].itertuples(index=False, name=None):
                        if int(f) * 1000 >= lo and (int(f) + int(g)) * 1000 < hi:
                            raw_spans.append(dict(traceID=str(a), spanID=str(b),
                                parentSpanID='' if adapter._rong(c) else str(c), owner=str(d), operation=str(e),
                                start_us=int(f), duration_us=int(g)))
                    case = dict(spans=raw_spans, metrics=[], params_ca=dict(don_vi_thoi_gian={'spans.start_us': 'us'}))
                    provenance = [_file_provenance(path, 'trace rows filtered by native window')]
                else:
                    case = adapter.ca_nezha(self.nz, oid, ROOT, self.contract)
                    provenance = [dict(file=x['path'], sha256=x['sha256'], role='Nezha adapter source')
                                  for x in self.nz[oid]['files'].values()]
                self.cache.clear()  # chỉ giữ một ca, không tích dữ liệu raw qua 52 ca
                self.cache[key] = (case, provenance)
            case, provenance = self.cache[key]
            if ma.startswith('metric|'):
                cot = ma.split('|', 1)[1]
                params = case['params_ca']
                source = params['nguon_metric'][cot]
                times = params['thoi_gian_nguon'][source]
                rows = [(int(t), row[cot]) for t, row in zip(times, case['metrics'])
                        if row.get(cot) is not None and math.isfinite(row[cot]) and lo <= int(t) < hi]
                N, mN = [v for t, v in rows if t < t_ns], [t for t, v in rows if t < t_ns]
                A, mA = [v for t, v in rows if t >= t_ns], [t for t, v in rows if t >= t_ns]
            elif ma.startswith('op|'):
                _, owner, operation = ma.split('|', 2)
                prep = span.chuan_bi(case['spans'], t=t_ns / 1000, tau=1000, tinh_CP=False)
                if prep['loi']:
                    raise ValueError('raw span không hợp lệ')
                unit = span.mau_thao_tac(prep, 'tat')[(owner, operation)]
                N, A = unit['N'], unit['A']
                mN, mA = ([int(t * 1000) for t in unit['moc_' + side]] for side in ('N', 'A'))
                source = 'trace'
            else:
                raise ValueError('OPEN: đơn vị ngoài metric/op của T1-R0: ' + ma)
        if source not in rec['coverage']:
            raise ValueError('thiếu coverage của nguồn')
        bounds = cong.bien_phia(rec['coverage'][source], t_ns)
        return dict(N=N, mN=mN, A=A, mA=mA, t_ns=t_ns, bounds=bounds,
                    provenance=provenance, source=source)


def read_run(path):
    path = ad.duong_ra(path)
    meta = tep_pha1.kiem(path)  # pha1.json chỉ có sau khi lượt đã ghép hoàn tất
    if meta['so_ca'] not in (30, 52) or meta['so_ban_ghi'] != meta['so_ca'] or meta['cau_hinh'] != ['T1-R0']:
        raise ValueError('chỉ nhận toàn bộ lượt T1-R0 52 ca thật hoặc 30 C-e đã hoàn tất')
    rows = {}
    with (path / meta['tep']).open('rb') as f:
        for line, data in enumerate(f, 1):
            if data.strip():
                rec = json.loads(data)
                rows[rec['opaque_id']] = (rec, dict(file=(path / meta['tep']).relative_to(ROOT).as_posix(),
                                                   line=line, sha256=meta['sha256']))
    return path, meta, rows


def parameters(path, oid, c1):
    p = path / 'cases' / oid / 'phase1/tham-so.json'
    meta = json.loads(p.read_text(encoding='utf-8'))
    configs = meta['configs']
    if len(configs) != 1 or configs[0]['config_id'] != 'T1-R0':
        raise ValueError('metadata không phải T1-R0')
    if meta.get('code_revision') != OLD_REV:
        raise ValueError('metadata không khai revision nền c298188e')
    if c1:
        expected = digest((ROOT / 'src/m1/cong.py').read_bytes())
        if meta.get('code_correction') != 'Q-233/C1' or meta.get('source_sha256', {}).get('src/m1/cong.py') != expected:
            raise ValueError('lượt mới không có provenance source C1 đúng')
    elif meta.get('code_correction'):
        raise ValueError('lượt cũ có code correction; không phải trước C1')
    return configs[0]['tham_so_E4'], dict(file=p.relative_to(ROOT).as_posix(), sha256=digest(p.read_bytes()),
                                          claimed_revision=meta['code_revision'], git_head=meta.get('git_head'),
                                          correction=meta.get('code_correction'))


def compare_case(oid, before, after, ts, old_api, raw_loader, event):
    full = delta_fields(before, after)
    old_units = {u['ma']: (i, u) for i, u in enumerate(before['extra']['don_vi_phan_vi'])}
    new_units = {u['ma']: (i, u) for i, u in enumerate(after['extra']['don_vi_phan_vi'])}
    changed = [ma for ma in sorted(set(old_units) | set(new_units))
               if old_units.get(ma, (None, None))[1] != new_units.get(ma, (None, None))[1]]
    units, opens, explained_prefixes = {}, [], []
    if before['window'] != after['window'] or before['coverage'] != after['coverage']:
        opens.append('native window/coverage thay đổi; không thể gán cho C1')
    for ma in changed:
        if ma not in old_units or ma not in new_units:
            units[ma] = dict(status='OPEN', reason='tập đơn vị có/mất; C1 không thay tập đơn vị')
            opens.append(ma + ': tập đơn vị đổi')
            continue
        try:
            raw = raw_loader.one(oid, before, ma)
            result = explain_unit(raw, old_units[ma][1], new_units[ma][1], ts, old_api)
            units[ma] = result
            if result['status'] == 'OPEN':
                opens.append(ma + ': API không tái lập toàn bộ native')
            elif old_units[ma][0] != new_units[ma][0]:
                opens.append(ma + ': thứ tự đơn vị đổi')
            else:
                explained_prefixes.append('/extra/don_vi_phan_vi/' + str(old_units[ma][0]) + '/')
        except Exception as error:
            units[ma] = dict(status='OPEN', reason=f'{type(error).__name__}: {error}')
            opens.append(ma + ': thiếu hoặc lệch đầu vào/tái tính')
        event(event='unit_done', opaque_id=oid, unit=ma, status=units[ma]['status'])
    unexplained = [d for d in full if not any(d['pointer'].startswith(p) for p in explained_prefixes)]
    # Đổi tầng/blocks/F_I... phải được giải thích tiếp; p được tái lập chưa miễn phần này.
    if unexplained:
        opens.append('delta ngoài đơn vị cổng chưa được phân xử; xem unexplained_fields')
    downstream = {field: dict(before=before.get(field), after=after.get(field)) for field in
                  ('blocks', 'entity_ranking', 'worlds', 'verdict', 'classes', 'inherited_by')
                  if before.get(field) != after.get(field)}
    downstream.update({f'extra.{field}': dict(before=before['extra'].get(field), after=after['extra'].get(field))
                       for field in ('tang_P', 'K_I_P', 'K_raw_P', 'kenh_co', 'kenh_co_the_gioi', 'T4c')
                       if before['extra'].get(field) != after['extra'].get(field)})
    return dict(opaque_id=oid, changed_fields=full, changed_units=units, downstream=downstream,
                unexplained_fields=unexplained, OPEN=opens,
                status='OPEN' if opens else 'EXPLAINED_BY_C1' if full else 'IDENTICAL')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--old', required=True)
    parser.add_argument('--new', required=True)
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    out = ad.duong_ra(args.run)
    out.mkdir(parents=True, exist_ok=False)
    old_api, sources = frozen_source()
    old_path, old_meta, before = read_run(args.old)
    new_path, new_meta, after = read_run(args.new)
    if old_meta['so_ca'] != new_meta['so_ca'] or set(before) != set(after):
        raise ValueError('hai lượt không cùng tập ca')
    raw_loader = RawInputs()
    start, summary = time.monotonic(), {}
    with (out / 'progress.jsonl').open('x', encoding='utf-8') as progress:
        def event(**row):
            row.update(seconds=time.monotonic() - start)
            budget_path = ad.OUT / 'runs/ngan-sach.json'
            if budget_path.exists():
                b = json.loads(budget_path.read_text(encoding='utf-8'))
                row['budget_seconds'] = b['prior_seconds'] + time.time() - b['start_epoch']
            progress.write(json.dumps(row, ensure_ascii=False) + '\n')
            progress.flush()
            if budget_path.exists() and row['budget_seconds'] >= b['cap_seconds']:
                raise TimeoutError('dừng ở trần tổng gói chạy')
        ad.ghi(out / 'command.json', dict(argv=sys.argv, source=sources,
                 old=dict(path=str(old_path.relative_to(ROOT)), meta=old_meta),
                 new=dict(path=str(new_path.relative_to(ROOT)), meta=new_meta),
                 raw_controls=raw_loader.controls,
                 script_sha256=digest(Path(__file__).read_bytes())))
        event(event='start', cases=len(before))
        for oid in sorted(before):
            a, b = before[oid][0], after[oid][0]
            ts_old, src_old = parameters(old_path, oid, False)
            ts_new, src_new = parameters(new_path, oid, True)
            if ts_old != ts_new:
                raise ValueError('tham số E4 đổi ngoài C1')
            result = compare_case(oid, a, b, ts_old, old_api, raw_loader, event)
            result['source'] = dict(before=before[oid][1], after=after[oid][1],
                                   params_before=src_old, params_after=src_new)
            file = out / 'cases' / (oid + '.json')
            ad.ghi(file, result)
            summary[oid] = dict(status=result['status'], changed_units=len(result['changed_units']),
                                changed_fields=len(result['changed_fields']), OPEN=result['OPEN'],
                                file=file.relative_to(ROOT).as_posix())
            event(event='case_done', opaque_id=oid, **{k: summary[oid][k] for k in ('status', 'changed_units')})
        states = collections.Counter(x['status'] for x in summary.values())
        result = dict(schema='T047-C1-full-delta-audit-v1', cases=summary, counts=dict(states),
                      PASS=states['OPEN'] == 0, sources=sources,
                      old_hash=old_meta['sha256'], new_hash=new_meta['sha256'],
                      scope='T1 native trước/sau C1; đủ lượt thật hoặc C-e; không nhãn/chấm RCA.',
                      limits=['Audit riêng này không thay T1 bất biến seed/xáo hoặc đối chiếu T-046.',
                              'Downstream đổi nhưng chưa phân xử giữ OPEN; không tự quy p-only là hợp lệ.',
                              'Thiếu raw hoặc API không tái lập native thì không công nhận giải thích C1.'])
        ad.ghi(out / 'summary.json', result)
        event(event='done', **result['counts'])
    print(json.dumps(dict(PASS=result['PASS'], counts=result['counts'], file=str(out / 'summary.json'))))
    if not result['PASS']:
        raise SystemExit('OPEN: xem mọi delta chưa phân xử trong audit')


if __name__ == '__main__':
    main()

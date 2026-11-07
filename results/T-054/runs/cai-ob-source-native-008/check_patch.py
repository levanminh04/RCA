"""Approved OB patch: generated inputs only; retains every run and failure."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import copy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-054/scripts'),
                str(ROOT / 'results/T-044/tests'), str(ROOT / 'results/T-043/scripts'),
                'D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro',
                'D:/RCA-ext/work/T-014/CIRCA', 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
from bien_nhan import canonical, fingerprint
from test_adapter import _nezha, _re2, _tg, U_S
from p3 import nezha
from p3.adapters import nezha as baselines
from m1 import adapter, chuoi, runner, e4
from pandas.testing import assert_frame_equal
import numpy as np
import pandas as pd


def old_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, RUN / 'before' / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    dest = RUN / sys.argv[1]
    dest.mkdir(exist_ok=False)
    checks = []
    def save():
        (dest / 'result.json').write_text(json.dumps({'checks': checks, 'telemetry_used': False},
                                                    ensure_ascii=False, indent=2), encoding='utf8')
    def check(name, fn):
        try:
            fn()
            checks.append({'name': name, 'PASS': True})
        except BaseException:
            checks.append({'name': name, 'PASS': False, 'traceback': traceback.format_exc()})
            save()
            raise
        save()
    def same(a, b):
        assert canonical(a) == canonical(b)
    old_reader = old_module('p3._nezha_008_before', 'src/p3/nezha.py')
    old_core = old_module('m1._chuoi_008_before', 'src/m1/chuoi.py')
    contract = json.loads((ROOT / 'results/T-043/hop-dong.json').read_bytes())
    cfgs = json.loads((ROOT / 'results/T-054/protocol.json').read_bytes())['configurations']

    def run(data, cfg, core=chuoi):
        core.CACHE = e4.CacheCong()
        params = runner._params(cfg, data)
        params['tach_cd3'] = True
        return core.chay(data['spans'], data['metrics'], data['logs'], data['inventory'],
                         data['aliases'], data['t'], params)

    modes = () if '--tt-only' in sys.argv else ('rectangular', '2N5A', '3N5A', '6N5A', '5N6A', 'empty-source')
    for mode in modes:
        generated = dest / mode
        al, t = _nezha(generated)
        allow = nezha.nap_allowlist(al)
        oid = next(iter(allow))
        row = allow[oid]
        if mode != 'rectangular':
            rel = sorted(k for k in row['files'] if '/metric/' in k)[0]
            f = generated / rel
            with f.open(encoding='utf8', newline='') as stream:
                reader = csv.DictReader(stream)
                fields, rows = reader.fieldnames, list(reader)
            inside = [r for r in rows if t-300*nezha.NS <= nezha.parse_time_ns(r['Time']) < t+300*nezha.NS]
            normal = [r for r in inside if nezha.parse_time_ns(r['Time']) < t]
            incident = [r for r in inside if nezha.parse_time_ns(r['Time']) >= t]
            if mode in ('2N5A', '3N5A'):
                normal = normal[-int(mode[0]):]
            elif mode == '6N5A':
                extra = copy.deepcopy(normal[0]); extra['Time'] = _tg(t-270*nezha.NS) + ' +0000 UTC m=+1.5'
                normal.append(extra)
            elif mode == '5N6A':
                extra = copy.deepcopy(incident[0]); extra['Time'] = _tg(t+30*nezha.NS) + ' +0000 UTC m=+1.5'
                incident.append(extra)
            else:
                normal, incident = [], []
            outside = [r for r in rows if r not in inside]
            with f.open('w', encoding='utf8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(outside+normal+incident)
            row['files'][rel].update(sha256=hashlib.sha256(f.read_bytes()).hexdigest(), bytes=f.stat().st_size)
        selected = nezha.chon_ca(allow, oid, generated)
        payload = nezha.doc_cua_so(selected, layout='source_native')
        data = adapter.ca_nezha(allow, oid, generated, contract, layout='source_native')
        if mode == 'rectangular':
            previous = old_reader.doc_cua_so(selected)
            check('rectangular_reader_frame', lambda: assert_frame_equal(previous['metric'], payload['metric']))
            check('rectangular_provenance_window', lambda: same(previous['provenance'], payload['provenance']))
            check('rectangular_window', lambda: same(previous['window'], payload['window']))
            check('rectangular_normalized_input', lambda: same(data, adapter.ca_nezha(allow, oid, generated, contract)))
            forced = dict(payload, metric_layout='source_native', metric_sources={})
            for rel0, source in payload['provenance']['sources'].items():
                if source['kind'] != 'metric':
                    continue
                columns = [c for c, info in payload['provenance']['channels'].items() if info['source']==rel0]
                forced['metric_sources'][rel0] = pd.DataFrame({'time':source['timestamps_ns'],
                    **{c:payload['metric'][c].to_numpy() for c in columns}})
            def same_baro_keys():
                a, b = baselines.chay('baro',payload)[0], baselines.chay('baro',forced)[0]
                for field in ('status','items','ranking_native','observed_entities'):
                    same(a[field],b[field])
            check('rectangular_BARO_forced_sourcewise_keys_ties',same_baro_keys)
            for arm in ('M1','bo-E1','bo-E2','bo-E5','C-a0','C-a1'):
                cfg = cfgs[arm]['config']
                check('rectangular_core_full_record_' + arm, lambda cfg=cfg: same(run(data, cfg), run(data, cfg, old_core)))
        else:
            def legacy_rejected():
                try: nezha.doc_cua_so(selected)
                except Exception as exc:
                    assert '5N+5A' in str(exc)
                    return
                raise AssertionError('legacy accepted ragged input')
            check(mode+'_legacy_unchanged_rejects', legacy_rejected)
            def retained():
                frame = payload['metric_sources'][rel]
                assert len(frame) == len(normal)+len(incident)
                assert sorted(frame['time']) == sorted(nezha.parse_time_ns(r['Time']) for r in normal+incident)
                assert len(data['params_ca']['thoi_gian_nguon'][data['params_ca']['nguon_metric'][next(c for c in frame if c!='time')]]) == len(frame)
            check(mode+'_real_samples_times_only', retained)
            result = run(data, cfgs['M1']['config'])
            check(mode+'_core_no_contract_error', lambda: assert_ok(result))
            if mode == '2N5A':
                for kind in ('duplicate','outside','cross-source','wrong-time','missing-source'):
                    bad = copy.deepcopy(data)
                    ix = bad['params_ca']['chi_so_hang_metric']; src = next(k for k,v in ix.items() if v)
                    if kind=='duplicate': ix[src][1] = ix[src][0]
                    elif kind=='outside': ix[src][0] = len(bad['metrics'])
                    elif kind=='cross-source': ix[src][0] = next(v[0] for k,v in ix.items() if k!=src and v)
                    elif kind=='wrong-time': bad['params_ca']['thoi_gian_nguon'][src][0] += 1
                    else: ix.pop(src)
                    check('invalid_mapping_'+kind, lambda bad=bad: assert_error(run(bad,cfgs['M1']['config'])))
        # Core BARO on all source input paths; empty source may be NO_EVIDENCE, not invented data.
        if mode == 'empty-source':
            def empty_baro_preserves_error():
                result = baselines.chay('baro',payload)[0]
                assert result['status']=='ERROR' and 'IndexError' in result['error']
                assert not result['items']
            check('empty_source_BARO_preserves_native_error_no_fake_samples',empty_baro_preserves_error)
        else:
            check(mode+'_BARO_valid_native_keys', lambda: assert_baseline(baselines.chay('baro',payload)[0]))
        check(mode+'_SimpleRCA_native_arrays', lambda: assert_baseline(baselines.chay('simplerca',payload)[0]))
    generated = dest / 'TT-default'
    al, _, _ = _re2(generated, t=1700000000)
    from p3 import selector
    allow = selector.nap_allowlist(al); oid = next(iter(allow))
    data = adapter.ca_re2tt(allow,oid,1700000000,generated,contract,U_S)
    data['t'] = 1700000000  # RE2 adapter returns signals; the runner supplies this declared mode-(a) landmark.
    check('TT_default_full_core_unchanged',lambda: same(run(data,cfgs['M1']['config']),run(data,cfgs['M1']['config'],old_core)))
    print(json.dumps({'PASS':True,'checks':len(checks),'result':str(dest/'result.json')}),flush=True)


def assert_ok(record):
    assert record.get('status',record.get('trang_thai')) not in ('ERROR','TIMEOUT'), str(record)[:600]
def assert_error(record):
    assert record.get('status',record.get('trang_thai')) == 'ERROR', str(record)[:600]
def assert_baseline(record):
    assert record['status'] in ('OK','NO_EVIDENCE'), str(record)[:600]
    assert record['diagnostics']['ranking_nonfinite_keys']==0

if __name__=='__main__':
    main()

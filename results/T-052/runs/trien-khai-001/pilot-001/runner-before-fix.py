"""Native C-a tại các miền dev; không nạp nhãn, đóng dấu trước C-d3."""
import copy
import gzip
import hashlib
import json
import pathlib
import subprocess
import sys
import time
import traceback
from fractions import Fraction

from common import ROOT, RUN, digest, dump, event, metadata, native_index, native_rows, pin, read, save, timing
from chay import capture
from chay_pha1 import tat_ha_toc
from m1 import adapter, chuoi, doi_chung, e4, runner
from p3 import nezha, selector

# Chọn bằng miền và quy mô/nhánh đã ghim; không đọc root/fault/RR.
INDICES = (0, 43, 55, 60, 81)
CONFIGS = {'M1': 'K-E1+E2+E5', 'C-a0': 'K-R0', 'C-a1': 'K-E1'}


def comparable(record):
    rec = copy.deepcopy(record)
    for key in ('opaque_id', 'variant', 'config_id'):
        rec.pop(key, None)
    rec['region'] = None  # E7 tắt có chủ ý ở C-a, không ảnh hưởng hạng.
    rec['extra'].pop('dau_vao_cd3', None)
    rec['extra']['doi_chung'].pop('C-d3', None)
    return rec


def main():
    start = time.perf_counter()
    target = RUN / 'pilot-001'
    target.mkdir()
    tat_ha_toc()
    entries, base, lineage = metadata()
    manifest, index = native_index()
    save(target / 'plan.json', {'indices': INDICES, 'configs': CONFIGS,
         'lineage': lineage, 'runner_sha256': digest(__file__),
         'cd3_timeout_seconds': 15, 'label_access': False, 'budget_seconds': 3600})
    contract = read('results/T-043/hop-dong.json')
    allow_tt = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    allow_ob = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    universe = read('results/T-022/mappings/universe-re2tt-dev.json')['U']
    comparisons = []
    for n in INDICES:
        begin = time.perf_counter()
        job = entries[n]['job']
        event('pilot_start', index=n, dataset=job['dataset'], window=job['window'])
        if job['dataset'] == 'RE2-TT':
            case = adapter.ca_re2tt(allow_tt, job['opaque_id'], job['t'], ROOT, contract, universe)
            t = job['t']
        else:
            case = adapter.ca_nezha(allow_ob, job['opaque_id'], ROOT, contract)
            t = case['t']
        # Cùng chuẩn hóa với công cụ nguồn để so SHA, không đọc nhãn.
        from chay import dump as historical_dump
        normal = {k: case.get(k) for k in ('spans', 'metrics', 'logs', 'inventory', 'aliases', 'params_ca')}
        input_hash = hashlib.sha256(historical_dump(dict(normal, t=t)).encode()).hexdigest()
        item, command = index[(job['opaque_id'], job['window'])]
        wanted = native_rows(item, manifest, set(CONFIGS.values()))
        side_item = {'path': item['trace'], 'sha256': item['trace_sha256']}
        side = native_rows(side_item, manifest, set(CONFIGS.values()))
        for cid in CONFIGS.values():
            assert side[cid]['trace']['normalized_input_sha256'] == input_hash
        chuoi.CACHE = e4.CacheCong()
        for name, cid in CONFIGS.items():
            config = copy.deepcopy(base)
            config.update(config_id=name, nhanh_z=True)
            config['bat_tat'] = copy.deepcopy(command['configs'][cid]['bat_tat'])
            if name != 'M1':
                assert config['bat_tat'] == {k: v for k, v in chuoi.doi_chung_cau_hinh(name, base['bat_tat']).items() if k != 'E7'}
                config.update(chay_M1=True, doi_chung=name)
            params = runner._params(config, case)
            params['tach_cd3'] = True
            config = {'config_id': name, 'params': params}
            tick = time.perf_counter()
            rec, trace, clocks, effective = capture(case, t, config, compact=True, input_sha256=input_hash)
            assert not trace['capture_errors'], trace['capture_errors']
            assert rec['status'] in ('OK', 'NO_EVIDENCE'), rec.get('error')
            old_samples = {u: x['mau_sha256'] for u, x in side[cid]['trace']['phan_vi'].items()}
            assert {u: x['mau_sha256'] for u, x in trace['phan_vi'].items()} == old_samples
            # Seal trước tính/khởi chạy bất kỳ C-d3 mới hoặc evaluator nào.
            body = {'record': rec, 'trace': trace, 'effective': effective, 'timing': clocks}
            path = target / f'{n:02d}-{name}.json.gz'
            path.write_bytes(gzip.compress(dump(body).encode('utf-8'), mtime=0))
            save(target / f'{n:02d}-{name}-seal.json', {'native_sha256': digest(path),
                 'input_sha256': input_hash, 'main_sealed_before_cd3': True, 'labels_read': False})
            left, right = comparable(rec), comparable(wanted[cid])
            mismatches = [k for k in sorted(set(left) | set(right)) if dump(left.get(k)) != dump(right.get(k))]
            row = timing('native', tick, index=n, config=name, status=rec['status'],
                         mismatch_fields=mismatches, input_sha256=input_hash,
                         samples_hashes={u: x['mau_sha256'] for u, x in trace['phan_vi'].items()},
                         E7_intentionally_disabled=name != 'M1', source=item['path'])
            save(target / f'{n:02d}-{name}-comparison.json', row)
            comparisons.append(row)
            event('pilot_result', index=n, config=name, seconds=row['elapsed_seconds'], mismatches=mismatches)
            if mismatches:
                save(target / f'{n:02d}-{name}-mismatch.json', {'actual': left, 'expected': right})
                raise ValueError(('native parity', n, name, mismatches))
            if name == 'M1' and job['dataset'] == 'RE2-TT':
                payload = {'canh': rec['extra']['canh'], **rec['extra']['dau_vao_cd3']}
                payload_path = target / f'{n:02d}-cd3-input.json'
                save(payload_path, payload)
                try:
                    result = subprocess.run([sys.executable, '-B', '-S', __file__, 'cd3', str(payload_path)],
                        cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=15)
                    assert result.returncode == 0, result.stderr
                    result = json.loads(result.stdout)
                except subprocess.TimeoutExpired:
                    result = {'trang_thai': 'TIMEOUT', 'blocks': [], 'timeout_seconds': 15}
                save(target / f'{n:02d}-cd3.json', dict(result, main_native_sha256=digest(path)))
        event('pilot_window_done', index=n, elapsed_seconds=time.perf_counter() - begin)
    save(target / 'summary.json', timing('pilot', start, PASS=True, comparisons=comparisons,
        labels_read=False, native_comparisons=len(comparisons), code_lineage=lineage))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'cd3':
        data = read(pathlib.Path(sys.argv[2]))
        result = doi_chung.cd3(data['canh'], {k: Fraction(*v) for k, v in data['diem'].items()}, data['dich'])
        print(dump(dict(result, so_span_goc_A=data['so_span_goc_A'])))
    else:
        try:
            main()
        except BaseException as exc:
            save(RUN / 'pilot-001' / 'failure.json', {'error': repr(exc), 'traceback': traceback.format_exc()})
            raise

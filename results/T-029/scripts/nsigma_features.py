"""T-029 bước1/3: BARO riêng cột; bước4 được mở riêng sau phụ thuộc V3. Không đọc nhãn root/fault."""
import argparse
import contextlib
import hashlib
import json
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'results/T-029'
LOG = ROOT/'tasks/T-029-p4-han-che-phat-hien/LOG.md'


def stamp():
    return datetime.now(ZoneInfo('Asia/Saigon')).isoformat(timespec='seconds')


def log(msg):
    with LOG.open('a', encoding='utf-8') as f:
        f.write(f'\n- {stamp()} — Hỗ trợ Codex N-Sigma: {msg}\n')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def choose_run():
    n = 1
    while (OUT/f'runs/nsigma-{n:03}').exists():
        n += 1
    return OUT/f'runs/nsigma-{n:03}'


def extract(resume_from=None, run_path=None):
    from baro.anomaly_detection import nsigma
    from p3.adapters.phat_hien import cot_bocpd, luot_rca
    from p3.selector import nap_allowlist, chon_ca
    from test_nsigma import run_tests
    run = Path(run_path).resolve() if run_path else choose_run()
    assert run.parent == (OUT/'runs').resolve() and run.name.startswith('nsigma-')
    if run.exists():
        assert resume_from and {p.name for p in run.iterdir()} == {
            f'{n}-source-before-resume.py' for n in ('nsigma_features', 'nsigma_flags', 'test_nsigma')}, 'Lượt mới chỉ được có ba snapshot nguồn cũ'
    log(f'Lệnh có ghi: nsigma_features.py extract, Python T014-main -B; lượt {run.relative_to(ROOT)} giữ mọi lượt. Resume={resume_from}; dùng lại cặp đã SHA/V2 kiểm, chỉ tính cặp thiếu; chưa ghi features-no-label khi 2a chưa PASS.')
    run.mkdir(parents=True, exist_ok=bool(resume_from))
    start = time.perf_counter()
    sources = ['tasks/T-029-p4-han-che-phat-hien/SPEC.md', 'results/T-022/allowlist-dev.json',
               'results/T-022/mappings/universe-re2tt-dev.json', 'results/T-025/bao-dong.json',
               'results/T-025/cham/soi-nsigma-t-hat.json', 'results/T-025/cham/phan-tich-b.json',
               'results/T-031/moi-truong.json', 'src/p3/adapters/phat_hien.py', 'src/p3/selector.py']
    sources += [f'results/T-029/scripts/{n}.py' for n in ('nsigma_features', 'nsigma_flags', 'test_nsigma')]
    manifest = {'status': 'RUNNING', 'bat_dau': stamp(), 'lenh': 'T014-main python.exe -B -W ignore '+' '.join(sys.argv),
                'nguon': {p: sha(ROOT/p) for p in sources},
                'baro_nsigma': {'path': str(Path(sys.modules['baro.anomaly_detection'].__file__)),
                                'sha256': sha(sys.modules['baro.anomaly_detection'].__file__)},
                'V2': {'status': 'RUNNING', 'so_cap': 0, 'so_cap_tinh_moi': 0, 'so_cap_dung_lai': 0}, 'cases': {}}
    dump(run/'manifest.json', manifest)
    try:
        with (run/'stdout.txt').open('w', encoding='utf-8') as stdout, (run/'stderr.txt').open('w', encoding='utf-8') as stderr, contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            al = nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
            bd = json.loads((ROOT/'results/T-025/bao-dong.json').read_text(encoding='utf-8'))['bo_phat_hien']
            if resume_from:
                previous = Path(resume_from).resolve()
                assert previous.parent == (OUT/'runs').resolve() and previous != run
                old = json.loads((previous/'manifest.json').read_text(encoding='utf-8'))
                assert all(sha(previous/p) == h for p, h in old['output_sha256'].items()), 'SHA output cũ lệch: DỪNG'
                for p, h in old['nguon'].items():
                    actual = run/'nsigma_features-source-before-resume.py' if p == 'results/T-029/scripts/nsigma_features.py' else ROOT/p
                    assert sha(actual) == h, f'SHA nguồn dùng lại lệch {p}: DỪNG'
                reused = []
                for oid, case in sorted(old['cases'].items()):
                    assert case['moc_index'] == 720 and case['T'] == 1441
                    assert case['metric_sha256'] == al[oid]['files']['metrics.parquet']['sha256']
                    for detector, r in sorted(case['bo'].items()):
                        assert r['status'] == 'PASS' and sha(ROOT/r['npz']) == r['sha256']
                        assert json.loads((previous/f'{oid}--{detector}.json').read_text(encoding='utf-8')) == r
                        with np.load(ROOT/r['npz'], allow_pickle=False) as arr:
                            Z, times, cols = arr['Z'], arr['times'], arr['columns'].tolist()
                            assert Z.dtype == np.bool_ and Z.shape == (1441, len(cols))
                            assert np.array_equal(times-times[0], np.arange(1441))
                            alarms = [int(times[i]) for i in np.flatnonzero(Z.any(axis=1))]
                            assert alarms == bd[detector][oid]['alarms'] and luot_rca(alarms)['t_hat'] == bd[detector][oid]['luot_rca']['t_hat'], 'V2 dùng lại lệch: DỪNG'
                            assert cols == bd[detector][oid]['detector_columns']
                        reused.append({'opaque_id': oid, 'detector': detector, 'npz': r['npz'], 'sha256': r['sha256']})
                    # Bản sao JSON trong bộ nhớ; không ghi bất kỳ byte nào vào lượt cũ.
                    manifest['cases'][oid] = case
                assert len(reused) == 13, 'Resume phải đúng13 cặp đã được kiểm'
                missing = [[oid, detector] for oid in sorted(al) for detector in ('nsigma', 'nsigma_doi_chung')
                           if detector not in manifest['cases'].get(oid, {}).get('bo', {})]
                assert len(missing) == 47
                manifest['resume'] = {'from': previous.relative_to(ROOT).as_posix(),
                                      'manifest_sha256': sha(previous/'manifest.json'),
                                      'source_snapshots': {p.name: sha(p) for p in run.glob('*-source-before-resume.py')},
                                      'reused_pairs': reused, 'missing_pairs_at_start': missing}
                manifest['V2']['so_cap'] = len(reused)
                manifest['V2']['so_cap_dung_lai'] = len(reused)
                tests = json.loads((previous/'V6-nsigma.json').read_text(encoding='utf-8'))
                assert tests['status'] == 'PASS'
                manifest['V6_reused_from'] = {'path': (previous/'V6-nsigma.json').relative_to(ROOT).as_posix(),
                                             'sha256': sha(previous/'V6-nsigma.json')}
                dump(run/'manifest.json', manifest)
                log('Resume kiểm lại31SHA output cũ, nguồn khóa và13V2 trực tiếp từ NPZ PASS; chỉ47cặp thiếu, tham chiếu13NPZ cũ; không tính lại13cặp. V6 dùng lại PASS nguồn test/flags giữ nguyên.')
            else:
                tests = run_tests()
            dump(run/'V6-nsigma.json', tests)
            log(f'V6 N-Sigma tổng hợp PASS {len(tests["tests"])} phép thử: ma trận đáp án N1–N4, đuôi dày BARO, cột chuẩn độc lập. N3 không dùng kiểm này để suy độc lập trên dev.')
            # Đọc chỉ chi_so_moc từ nguồn đã chốt T025; không chuyển root/fault sang đặc trưng.
            moc = {oid: row['chi_so_moc'] for oid, row in json.loads((ROOT/'results/T-025/cham/phan-tich-b.json').read_text(encoding='utf-8'))['theo_ca'].items()}
            assert len(al) == 30 and all(moc[oid] == 720 for oid in al), 'Mốc không 720 ở mọi ca: DỪNG'
            for oid in sorted(al):
                existing = manifest['cases'].get(oid, {}).get('bo', {})
                if all(detector in existing for detector in ('nsigma', 'nsigma_doi_chung')):
                    continue
                cstart = time.perf_counter()
                log(f'Bắt đầu ca {oid}: SHA guard metrics, đọc D9, gọi BARO riêng từng cột cho hai tập. Ghi Z/std/timing riêng và kiểm V2 ngay từng cặp.')
                files = chon_ca(al, oid, ROOT, kiem_hash=True, tep=['metrics.parquet'])
                raw = pd.read_parquet(files['metrics.parquet'])
                times = raw['time'].to_numpy()
                assert len(times) == 1441 and np.array_equal(times-times[0], np.arange(1441)), 'Lưới không 0..1440: DỪNG'
                case = manifest['cases'].get(oid, {'metric_sha256': sha(files['metrics.parquet']), 'moc_index': 720, 'T': 1441, 'bo': {}})
                for detector in ('nsigma', 'nsigma_doi_chung'):
                    if detector in case['bo']:
                        log(f'{oid}/{detector}: dùng lại NPZ cũ đã kiểm SHA/V2, không gọi lại BARO và không ghi đè.')
                        continue
                    pstart = time.perf_counter()
                    columns = cot_bocpd(raw.columns) if detector == 'nsigma' else [c for c in raw.columns if c != 'time']
                    assert columns == bd[detector][oid]['detector_columns'], 'Tập cột lệch nguồn T025: DỪNG'
                    data = raw[['time']+columns].replace([np.inf, -np.inf], np.nan).ffill()
                    Z = np.zeros((1441, len(columns)), dtype=bool)
                    indexes = {int(t): i for i, t in enumerate(times)}
                    for j, c in enumerate(columns):
                        alarm = nsigma(data[['time', c]], k=3, startsfrom=100)
                        for t in alarm:
                            Z[indexes[int(t)], j] = True
                    merged = [int(times[i]) for i in np.flatnonzero(Z.any(axis=1))]
                    t_hat = luot_rca(merged)['t_hat']
                    first = indexes[t_hat] if t_hat is not None else None
                    sd = data[columns].iloc[:first].std().to_numpy() if first is not None else np.full(len(columns), np.nan)
                    path = run/f'{oid}--{detector}.npz'
                    np.savez_compressed(path, Z=Z, columns=np.asarray(columns), times=times, std_at_first=sd)
                    equal = merged == bd[detector][oid]['alarms'] and t_hat == bd[detector][oid]['luot_rca']['t_hat']
                    r = {'status': 'PASS' if equal else 'FAIL', 'd': len(columns), 'so_bao': len(merged),
                         't_hat': t_hat, 't_hat_index': first, 'alarms_equal': merged == bd[detector][oid]['alarms'],
                         't_hat_equal': t_hat == bd[detector][oid]['luot_rca']['t_hat'],
                         'npz': path.relative_to(ROOT).as_posix(), 'sha256': sha(path),
                         'wall_s': time.perf_counter()-pstart}
                    case['bo'][detector] = r
                    dump(run/f'{oid}--{detector}.json', r)
                    manifest['cases'][oid] = case
                    manifest['V2']['so_cap'] += 1
                    manifest['V2']['so_cap_tinh_moi'] += 1
                    dump(run/'manifest.json', manifest)
                    log(f'V2 {oid}/{detector}: {r["status"]}; {len(columns)} cột, {len(merged)} giây báo, t_hat_index={first}; wall={r["wall_s"]:.3f}s; Z và SHA đã lưu.')
                    if not equal:
                        raise RuntimeError(f'V2 lệch {oid}/{detector}: DỪNG ngay, không xử lý')
                case['wall_s'] = time.perf_counter()-cstart
                print(json.dumps({'opaque_id': oid, 'status': 'PASS', 'wall_s': case['wall_s']}), flush=True)
                dump(run/'manifest.json', manifest)
                log(f'Xong ca {oid}, V2 cả hai cặp PASS, wall={case["wall_s"]:.3f}s. Không nối nhãn.')
        assert manifest['V2']['so_cap'] == 60 and len(manifest['cases']) == 30
        if resume_from:
            assert manifest['V2']['so_cap_tinh_moi'] == 47 and manifest['V2']['so_cap_dung_lai'] == 13
        manifest['V2']['status'] = 'PASS'
        manifest['status'] = 'PASS'
    except BaseException as exc:
        manifest['status'] = 'STOPPED'
        manifest['error'] = f'{type(exc).__name__}: {exc}'
        with (run/'stderr.txt').open('a', encoding='utf-8') as f:
            traceback.print_exc(file=f)
        log(f'DỪNG lượt {run.name}: {manifest["error"]}. Giữ mọi output, không sửa định nghĩa/ngưỡng hoặc tự chạy lại.')
        raise
    finally:
        manifest['ket_thuc'] = stamp()
        manifest['wall_s'] = time.perf_counter()-start
        manifest['output_sha256'] = {p.name: sha(p) for p in run.iterdir() if p.is_file() and p.name != 'manifest.json'}
        dump(run/'manifest.json', manifest)
        log(f'Kết thúc lệnh extract {run.name}: {manifest["status"]}, V2={manifest["V2"]}, wall={manifest["wall_s"]:.3f}s; giữ stdout/stderr/manifest. Chưa lưu bước4.')
    print(json.dumps({'run': run.relative_to(ROOT).as_posix(), 'status': manifest['status'], 'V2': manifest['V2']}))


def save_features(run_path):
    from nsigma_flags import features
    run = Path(run_path).resolve()
    assert run.parent == (OUT/'runs').resolve() and run.name.startswith('nsigma-')
    manifest = json.loads((run/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['status'] == 'PASS' and manifest['V2']['status'] == 'PASS' and manifest['V2']['so_cap'] == 60
    assert json.loads((run/'V6-nsigma.json').read_text(encoding='utf-8'))['status'] == 'PASS'
    output = OUT/'features-no-label/nsigma'
    assert not output.exists(), 'Không đè output features cũ'
    universe = json.loads((ROOT/'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    log('Lệnh có ghi: nsigma_features.py features sau root xác nhận 2a PASS; V6-N và V2 60/60 PASS. Tạo features-no-label/nsigma kèm hash, chưa nối root/fault/cell.')
    output.mkdir(parents=True, exist_ok=False)
    index = {'status': 'RUNNING', 'bat_dau': stamp(), 'run': run.relative_to(ROOT).as_posix(),
             'nguon_manifest_sha256': sha(run/'manifest.json'),
             'feature_script_sha256': sha(Path(__file__)),
             'flag_script_sha256': sha(Path(__file__).with_name('nsigma_flags.py')),
             'N5_mapping': {'latency': "suffix chứa 'latency'", 'error': "suffix chứa 'error'",
                            'cpu': "suffix chứa 'cpu'", 'mem': "suffix chứa 'mem'",
                            'mang': ['network', 'net_', 'rx', 'tx', 'receive', 'transmit'],
                            'khac': 'mọi suffix còn lại, gồm socket/diskio/workload',
                            'canh_bao': 'Chưa xác nhận nghĩa telemetry socket; mạng=0 không chứng minh không có kênh mạng. Giữ nguyên suffix/tên để đọc lại.'},
             'cases': {}}
    try:
        for oid, case in manifest['cases'].items():
            rows = {}
            for detector, r in case['bo'].items():
                p = ROOT/r['npz']
                assert sha(p) == r['sha256'], 'Hash Z lệch: DỪNG'
                with np.load(p, allow_pickle=False) as arr:
                    f = features(arr['Z'], arr['columns'].tolist(), arr['std_at_first'], universe)
                for column in f['columns']:
                    column['raw_suffix'] = column['column'].split('_', 1)[1] if '_' in column['column'] else ''
                f['N5_mapping'] = index['N5_mapping']
                f['opaque_id'] = oid
                f['bo_phat_hien'] = detector
                f['nguon'] = {'Z_path': r['npz'], 'Z_sha256': r['sha256'],
                              'bao_dong': f'results/T-025/bao-dong.json#/bo_phat_hien/{detector}/{oid}'}
                path = output/f'{oid}--{detector}.json'
                dump(path, f)
                rows[detector] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}
            index['cases'][oid] = rows
            dump(output/'manifest.json', index)
            log(f'Bước4 N1–N6/E không root {oid}: lưu hai bộ kèm hash; không đọc/ghép root, loại lỗi, ô.')
        index['status'] = 'PASS'
    except BaseException as exc:
        index['status'] = 'STOPPED'
        index['error'] = f'{type(exc).__name__}: {exc}'
        log(f'DỪNG lưu features: {index["error"]}; giữ mọi output.')
        raise
    finally:
        index['ket_thuc'] = stamp()
        dump(output/'manifest.json', index)
        log(f'Bước4 phần N-Sigma kết thúc {index["status"]}, {len(index["cases"])} ca; manifest/hash lưu trước nối nhãn.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=('extract', 'features'))
    parser.add_argument('--run')
    parser.add_argument('--resume-from')
    args = parser.parse_args()
    if args.step == 'extract':
        extract(args.resume_from, args.run)
    else:
        if not args.run:
            parser.error('features cần --run')
        save_features(args.run)

"""T-029 step6 P1: source duration inquiry and raw root metric minute summaries.

This is a label-using analysis, kept outside features-no-label. No duration is
inferred from telemetry. No rescoring without a published D<721 seconds.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

import bocpd_features as bf

RUN = bf.OUT / 'runs/proxy-001'
SOURCES = [
    {'path': 'results/T-002/public-metadata/run-002/sources/paper-v2.html', 'line': 427,
     'url': 'https://arxiv.org/html/2412.17015v2#S3.SS3', 'section': '3.3',
     'finding': 'Nêu 10 phút nền trước tiêm, rồi thu telemetry bất thường; đoạn này không nêu thời lượng lỗi sau tiêm.'},
    {'path': 'results/T-002/public-metadata/run-002/sources/github-README.md', 'line': 162,
     'url': 'https://github.com/phamquiluan/RCAEval/blob/259ea4167160256a74ad30004aa3d96a998c846e/README.md',
     'finding': 'Cấu trúc file nêu inject_time timestamp, không có end_time hoặc D trong phần mô tả này.'},
    {'path': 'results/T-002/public-metadata/run-002/sources/hf-README.md', 'line': 97,
     'url': 'https://huggingface.co/datasets/phamquiluan/RCAEval/blob/afeacb11bcc94dadfd1c8f483ee4377b2b8b614e/README.md',
     'finding': 'Mô tả inject_time chia normal trước và faulty sau mốc; đây là mô tả proxy, không bằng chứng độc lập về thời điểm kết thúc.'},
    {'path': 'docs/knowledge/K2-du-lieu.md', 'line': 14,
     'finding': 'Đã ghi inject time không phải independent anomaly-onset truth (nhãn thời điểm bất thường độc lập).'},
]


def source_record():
    result = []
    for source in SOURCES:
        item = dict(source)
        path = bf.ROOT / source['path']
        item['sha256'] = bf.digest(path)
        result.append(item)
    return {'examined_sources': result, 'looked_up_at': bf.now(), 'script_sha256': bf.digest(__file__),
            'published_fault_duration_D_seconds': None,
            'duration_status': 'OPEN: chưa thấy thời lượng lỗi sau tiêm trong các nguồn đã khảo sát',
            'original_repository_revision': '259ea4167160256a74ad30004aa3d96a998c846e',
            'original_repository_tree_check': 'git ls-tree -r --name-only HEAD: không thấy tên script inject/chaos/fault/collect/stress; script/ chỉ link/tag',
            'online_primary_search': {
                'queries': ['site:github.com/phamquiluan RCAEval fault injection duration',
                            'site:github.com/phamquiluan RCAEval chaosblade inject script'],
                'used_url': 'https://github.com/phamquiluan/RCAEval',
                'finding': 'Không thấy thông tin D hay script tiêm lỗi trong kết quả primary khảo sát; không kết luận mọi nguồn đều thiếu.'},
            'rescore': {'performed': False, 'reason': 'SPEC F P1 chỉ cho chấm lại khi nguồn nêu D<721 s; chưa có bằng chứng đó'},
            'causal_limit': 'Median metrics không xác minh được thời điểm kết thúc lỗi hoặc onset thật.'}


def compute():
    bf.audit('Lệnh có ghi: T-014-main python -B -W ignore results/T-029/scripts/proxy_analysis.py --compute; P1 bước6 riêng có nhãn, không ghi features-no-label.')
    allow_path = bf.ROOT / 'results/T-022/allowlist-dev.json'
    labels_path = bf.ROOT / 'results/T-022/nhan-dev.json'
    universe_path = bf.ROOT / 'results/T-022/mappings/universe-re2tt-dev.json'
    allow = json.loads(allow_path.read_text(encoding='utf-8'))['cases']
    labels = {item['opaque_id']: item for item in json.loads(labels_path.read_text(encoding='utf-8'))['cases']}
    universe = json.loads(universe_path.read_text(encoding='utf-8'))['U']
    bf.audit('Đọc nhãn dev root/inject_time và universe riêng cho P1; không chọn cột theo fault. Guard metrics từng ca trước đọc raw.')
    rows = {}
    started = time.perf_counter()
    for item in sorted(allow, key=lambda x: x['opaque_id']):
        t0 = time.perf_counter()
        oid = item['opaque_id']
        meta = item['files']['metrics.parquet']
        path = bf.ROOT / meta['path']
        if bf.digest(path) != meta['sha256']:
            bf.audit(f'DỪNG V1 SHA metrics lệch trước P1 {oid}.')
            raise RuntimeError(f'SHA metrics lệch {oid}')
        metrics = pd.read_parquet(path)
        lab = labels[oid]
        if len(metrics) != 1441 or not np.all(np.diff(metrics['time'].to_numpy()) == 1) or int(lab['inject_time'] - metrics['time'].iloc[0]) != 720:
            bf.audit(f'DỪNG P1 lưới/mốc khác SPEC ở {oid}.')
            raise RuntimeError('Lưới thời gian hoặc mốc lệch')
        root = lab['root']
        if root not in universe:
            raise RuntimeError(f'Root ngoài universe ở {oid}')
        columns = [c for c in metrics if c != 'time' and c.split('_', 1)[0] == root]
        if not columns:
            raise RuntimeError(f'Không có cột root trong {oid}')
        raw = metrics[columns]
        if np.isinf(raw.to_numpy(dtype=float)).any():
            raise RuntimeError(f'P1 raw inf chưa có quy ước tại {oid}')
        cohorts = {}
        for detector, s0 in (('bocpd', 1), ('nsigma_and_nsigma_control', 100)):
            baseline = raw.iloc[s0:720]
            low, high = baseline.quantile(.01), baseline.quantile(.99)
            windows = []
            for minute, left in enumerate(range(720, 1441, 60), 1):
                right = min(left + 60, 1441)
                medians = raw.iloc[left:right].median()
                unknown = low.isna() | high.isna() | medians.isna()
                if unknown.any():
                    failure = {'opaque_id': oid, 'detector': detector, 's0': s0, 'minute': minute,
                               'index_range': [left, right], 'columns_undefined': list(unknown[unknown].index),
                               'missing_baseline_count': baseline.count().astype(int).to_dict(),
                               'missing_minute_count': raw.iloc[left:right].count().astype(int).to_dict(),
                               'reason': 'SPEC chưa quy định mẫu số khi median/quantile không xác định; không tự coi False hoặc đổi denominator'}
                    bf.write_json(RUN / 'undefined-diagnostic.json', failure)
                    bf.audit(f'DỪNG P1 tại {oid}, {detector}, phút{minute}: median/quantile không xác định; giữ diagnostic, chờ chỉ dẫn.')
                    raise RuntimeError('P1 missing median/quantile chưa quy định')
                outside = (medians < low) | (medians > high)
                windows.append({'minute': minute, 'index_range_half_open': [left, right], 'seconds': right - left,
                                'partial_minute': right - left < 60, 'outside_columns': list(outside[outside].index),
                                'outside_count': int(outside.sum()), 'total_root_columns': len(columns),
                                'ratio': float(outside.mean()), 'median_by_column': {c: float(medians[c]) for c in columns},
                                'observed_count_by_column': {c: int(raw.iloc[left:right][c].count()) for c in columns}})
            cohorts[detector] = {'Nv_half_open': [s0, 720], 'q01': {c: float(low[c]) for c in columns},
                                'q99': {c: float(high[c]) for c in columns}, 'minutes_after_injection': windows}
        rows[oid] = {'opaque_id': oid, 'root': root, 'fault': lab['fault'], 'cell': lab['cell'],
                     'root_columns': columns, 'total_root_columns': len(columns), 'by_Nv': cohorts,
                     'source': {'metrics_path': meta['path'], 'metrics_sha256': meta['sha256'],
                                'labels': f'results/T-022/nhan-dev.json#/cases/{oid}'},
                     'seconds': round(time.perf_counter() - t0, 3)}
        bf.write_json(RUN / f'{oid}.json', rows[oid])
        bf.audit(f'P1 guard PASS {oid}; mọi cột root không chọn fault; 2 Nv ×13 phút (phút cuối1giây); {rows[oid]["seconds"]} s.')
    outputs = {p.relative_to(bf.ROOT).as_posix(): bf.digest(p) for p in sorted(RUN.glob('*.json'))}
    bf.write_json(RUN / 'manifest.json', {'status': 'PASS', 'cases': len(rows), 'seconds': round(time.perf_counter() - started, 3),
                                        'allowlist_sha256': bf.digest(allow_path), 'labels_sha256': bf.digest(labels_path),
                                        'universe_sha256': bf.digest(universe_path), 'script_sha256': bf.digest(__file__),
                                        'outputs': outputs, 'preprocessing': 'Raw metrics; pandas quantile/median bỏ NaN khi còn quan sát; inf hoặc statistic không xác định thì dừng',
                                        'quantile_interpolation': 'pandas linear default',
                                        'denominator': 'Mọi cột của root theo mapping tiền tố trước underscore; không chọn theo fault',
                                        'rescore_performed': False, 'duration_D': None})
    print(json.dumps({'status': 'PASS', 'cases': len(rows)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources-only', action='store_true')
    parser.add_argument('--compute', action='store_true')
    args = parser.parse_args()
    try:
        if args.sources_only:
            bf.audit('Lệnh có ghi: T-014-main python -B -W ignore proxy_analysis.py --sources-only; đọc/băm nguồn công khai đã lưu, ghi source evidence JSON, không telemetry.')
            path = RUN / 'sources.json'
            version = 2
            while path.exists():
                path = RUN / f'sources-{version:03d}.json'
                version += 1
            bf.write_json(path, source_record())
            print(json.dumps({'duration_D': None, 'rescore_performed': False}))
        elif args.compute:
            compute()
        else:
            raise ValueError('Chọn --sources-only hoặc --compute')
    except Exception as error:
        bf.audit(f'DỪNG proxy_analysis.py: {type(error).__name__}: {error}; giữ output, báo root; không tự xử lý.')
        raise

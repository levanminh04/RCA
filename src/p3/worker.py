"""Tiến trình con của runner: một lượt = một ca × một thành phần × một seed.

python -B -m p3.worker <job.json> <ket-qua.json>

Phần runner của tiến trình (đọc job, kiểm hash, đọc tệp, cắt cửa sổ) biết đường dẫn; hàm adapter chỉ nhận
dữ liệu đã cắt và mốc chia. Ghi kết quả từng phần kèm thời gian từng bước. Mã chạy được trên Python 3.8
cho loại job 'torai_run'.
"""
import json
import os
import sys
import time


def _doc_parquet(files, ten, cot=None):
    import pandas as pd
    if ten not in files:
        return None
    return pd.read_parquet(files[ten], columns=cot)


def _kiem_hash(job):
    from .selector import LoiRunner, sha256_file
    out = {}
    for name, meta in (job.get('files') or {}).items():
        h = sha256_file(meta['path'])
        if h != meta['sha256']:
            raise LoiRunner('SHA-256 sai: %s' % name)
        out[name] = h
    return out


def main(job_path, out_path):
    with open(job_path, encoding='utf-8') as f:
        job = json.load(f)
    buoc, t0 = {}, time.perf_counter()

    def moc(name, start):
        buoc[name] = round(time.perf_counter() - start, 6)
        return time.perf_counter()
    kind = job['kind']
    res = {'kind': kind}
    s = time.perf_counter()
    if kind == 'torai_run':
        import pandas as pd
        d = job['work_dir']
        tabs = {k: pd.read_csv(os.path.join(d, k + '.csv')) for k in ('metric', 'logts', 'tracets_err', 'tracets_lat')}
        s = moc('doc', s)
        from .adapters import torai
        res['ket_qua'] = torai.chay(tabs['metric'], tabs['logts'], tabs['tracets_err'], tabs['tracets_lat'],
                                    job['t'], job['seed'])
        moc('phuong_phap', s)
    else:
        res['input_sha256'] = _kiem_hash(job)
        files = {k: v['path'] for k, v in job['files'].items()}
        s = moc('kiem_hash', s)
        from . import cua_so
        metrics = _doc_parquet(files, 'metrics.parquet')
        need_tr = kind in ('ranker', 'torai_prep') and job['method'] in ('simplerca', 'microrank', 'tracerca', 'circa', 'torai_B')
        traces = _doc_parquet(files, 'traces.parquet') if need_tr else None
        need_lg = (kind == 'ranker' and job['method'] == 'simplerca') or (kind == 'torai_prep' and job['method'] == 'torai_B')
        logs = _doc_parquet(files, 'logs.parquet') if need_lg else None
        res['read_columns'] = {'metrics': [c for c in metrics.columns if c != 'time']}
        s = moc('doc', s)
        if kind == 'detector':
            from .adapters import phat_hien
            if job['method'] == 'bocpd':
                res['ket_qua'] = phat_hien.bocpd(metrics)
            else:
                res['ket_qua'] = phat_hien.nsigma(metrics, job.get('tap_cot', 'bocpd'))
            res['times'] = [int(x) for x in metrics['time']]
            moc('phuong_phap', s)
        else:
            t = job['t']
            win, info = cua_so.cat_ca(metrics, traces, logs, t)
            res['window'] = info
            s = moc('cat', s)
            m = job['method']
            if kind == 'torai_prep':
                from .adapters import torai
                if m == 'torai_A':
                    import pandas as pd
                    a = job['tac_gia']
                    lt, te, tl = (pd.read_csv(a[k]) for k in ('logts', 'tracets_err', 'tracets_lat'))
                    from .selector import sha256_file
                    res['input_sha256'].update({'tac_gia/' + k: sha256_file(a[k]) for k in a})
                    mt, lt, te, tl, extra = torai.chuan_bi_A(win['metric'], lt, te, tl, t)
                else:
                    mt, lt, te, tl, extra = torai.chuan_bi_B(win['metric'], win['traces'], win['logs'], t)
                d = job['work_dir']
                os.makedirs(d, exist_ok=True)
                for k, df in (('metric', mt), ('logts', lt), ('tracets_err', te), ('tracets_lat', tl)):
                    df.to_csv(os.path.join(d, k + '.csv'), index=False, float_format='%.17g')
                res['chuan_bi'] = extra
                moc('chuan_bi', s)
            else:
                from .adapters import baro, simplerca, microrank, tracerca, circa
                if m == 'baro':
                    res['ket_qua'] = baro.chay(win['metric'], t)
                elif m == 'simplerca':
                    res['ket_qua'] = simplerca.chay(win['metric'], win['traces'], win['logs'], t)
                elif m == 'microrank':
                    res['ket_qua'] = microrank.chay(win['traces'], t)
                elif m == 'tracerca':
                    res['ket_qua'] = tracerca.chay(win['traces'], t)
                elif m == 'circa':
                    res['ket_qua_nhieu'] = circa.chay(win['metric'], win['traces'], t, job['model'])
                    res['window']['circa_current'] = res['ket_qua_nhieu'][0].get('diagnostics', {}).get('circa_current')
                else:
                    raise ValueError('phương pháp lạ: %s' % m)
                moc('phuong_phap', s)
    res['buoc_s'] = buoc
    res['tong_trong_tien_trinh_s'] = round(time.perf_counter() - t0, 6)
    res['hashseed'] = os.environ.get('PYTHONHASHSEED')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, default=_json_default)


def _json_default(o):
    import numpy as np
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, tuple):
        return list(o)
    raise TypeError(type(o))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

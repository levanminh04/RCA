"""T-025 kiểm đúng đắn không dùng nhãn (SPEC mục "Kiểm đúng đắn").

1. N-Sigma tập chính: báo động 3 ca pilot so với results/T-031/runs/pilot-nsigma-001 (cùng hash src/p3 → giống hệt).
2. §11.8: job.json của mọi lượt bộ phát hiện không có mốc (khóa 't') hay trường nhãn; chỉ có kind, method, files, tap_cot.
3. Lượt RCA: số lượt theo trạng thái, key_check, lỗi runner; t của cửa sổ = t̂ của bộ phát hiện.
4. BOCPD: tần suất ERROR (posterior không hữu hạn), sentinel của maxes gốc.

python kiem_b.py nsigma=<lượt> [bocpd=<lượt>] [rca_nsigma=<lượt>] [rca_bocpd=<lượt>]
"""
import json
import sys
from pathlib import Path

import chung

T031 = chung.ROOT / 'results/T-031/runs/pilot-nsigma-001'
CAM = ('t', 'inject_time', 'root', 'fault', 'cell', 'nhan', 'label', 'case')


def ban_ghi(d):
    return {json.loads(p.read_text(encoding='utf-8'))['opaque_id']: json.loads(p.read_text(encoding='utf-8'))
            for p in sorted(Path(d).glob('luot/*/ban-ghi-0.json'))}


def kiem_job(d):
    sai = []
    for p in sorted(Path(d).glob('luot/*/job.json')):
        j = json.loads(p.read_text(encoding='utf-8'))
        if set(j) != {'kind', 'method', 'files', 'tap_cot'} or any(k in j for k in CAM):
            sai.append(p.parent.name)
    return {'so_job': len(list(Path(d).glob('luot/*/job.json'))), 'job_sai': sai}


def main(nsigma=None, bocpd=None, rca_nsigma=None, rca_bocpd=None, nsigma_doi_chung=None):
    L = chung.Luot('kiem-b', {'nsigma': nsigma, 'bocpd': bocpd, 'rca_nsigma': rca_nsigma, 'rca_bocpd': rca_bocpd})
    out = {}
    det = {}
    for ten, d in (('nsigma', nsigma), ('nsigma_doi_chung', nsigma_doi_chung), ('bocpd', bocpd)):
        if d:
            det[ten] = ban_ghi(chung.OUT / d)
            out[f'job_{ten}'] = kiem_job(chung.OUT / d)
            out[f'trang_thai_{ten}'] = {s: sum(r['status'] == s for r in det[ten].values())
                                        for s in ('OK', 'ERROR', 'TIMEOUT')}
    if nsigma:
        pilot = ban_ghi(T031)
        p_hash = json.loads((T031 / 'cau-hinh.json').read_text(encoding='utf-8'))['src_p3']['tong']
        out['nsigma_vs_pilot_T031'] = {
            'cung_hash_src_p3': p_hash == chung.hash_p3()['tong'],
            'ca': {o: {'bao_dong_giong_het': pilot[o]['alarms'] == det['nsigma'][o]['alarms'],
                       'luot_rca_giong_het': pilot[o]['luot_rca'] == det['nsigma'][o]['luot_rca'],
                       'cot_giong_het': pilot[o]['detector_columns'] == det['nsigma'][o]['detector_columns']}
                   for o in sorted(pilot)}}
    if bocpd:
        b = det['bocpd']
        out['bocpd'] = {
            'error': {o: r.get('error') for o, r in b.items() if r['status'] == 'ERROR'},
            'sentinel_goc_moi_ca_OK': sum(bool((r.get('diagnostics') or {}).get('co_sentinel_goc'))
                                          for r in b.values() if r['status'] == 'OK'),
            'so_ca_OK': sum(r['status'] == 'OK' for r in b.values()),
            'd_sau_tien_xu_ly': {o: (r.get('input_shape') or {}).get('cot_sau_tien_xu_ly') for o, r in sorted(b.items())}}
    for ten, d, dn in (('rca_nsigma', rca_nsigma, 'nsigma'), ('rca_bocpd', rca_bocpd, 'bocpd')):
        if not d:
            continue
        recs = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((chung.OUT / d).glob('luot/*/ban-ghi-*.json'))]
        tom = json.loads((chung.OUT / d / 'tom-tat.json').read_text(encoding='utf-8'))
        lech_t = [r['run_id'] for r in recs if r.get('window') and dn in det
                  and r['window']['t'] != det[dn][r['opaque_id']]['luot_rca']['t_hat']]
        tt = {}
        for r in recs:
            k = f'{r["method"]}:{r["variant"]}'
            tt.setdefault(k, {}).setdefault(r['status'], 0)
            tt[k][r['status']] += 1
        out[ten] = {'so_ban_ghi': len(recs), 'trang_thai': tt,
                    'key_check': {k: sum((r.get('diagnostics') or {}).get('key_check') == k for r in recs)
                                  for k in ('pass', 'fail', None)},
                    'so_loi_runner': tom.get('so_loi_runner'), 'lech_t_hat': lech_t,
                    'detector_ghi_dung': all(r.get('detector') == dn for r in recs)}
    chung.ghi_json(L.dir / 'kiem-b.json', out)
    print(json.dumps(out, ensure_ascii=False)[:3000])
    L.xong({k: (v if not isinstance(v, dict) or len(json.dumps(v)) < 300 else '...') for k, v in out.items()})


if __name__ == '__main__':
    main(**dict(a.split('=', 1) for a in sys.argv[1:]))

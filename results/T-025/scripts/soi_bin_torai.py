"""T-025 phiên 3 (R1, Minh duyệt 07/10): bin N của TORAI B nằm trước đầu dữ liệu. Chỉ đọc parquet dev, không đọc nhãn.

`src/p3/torai_b.py:113` dựng 40 bin 15 s từ t̂−300; `:73, :78, :106` điền 0 vào bin không có sự kiện, kể cả bin trước
đầu file. Với t̂ của mỗi bộ phát hiện, đếm trong 20 bin N: số bin kết thúc trước span đầu tiên (hoàn toàn trước dữ
liệu trace), số bin chứa span đầu (phủ một phần), số bin hoàn toàn trước dòng log đầu tiên.

python soi_bin_torai.py → results/T-025/cham/soi-bin-torai.json
"""
import json

import pyarrow.parquet as pq

import chung

ALLOW = json.loads(chung.ALLOWLIST.read_text(encoding='utf-8'))
BD = json.loads((chung.OUT / 'bao-dong.json').read_text(encoding='utf-8'))['bo_phat_hien']
BIN = 15


def min_cot(p, cot):
    return int(pq.read_table(chung.DATA_ROOT / p, columns=[cot]).column(0).to_pandas().min())


def main():
    out = {'mo_ta': __doc__.strip(), 'theo_bo': {}}
    dau = {}
    for c in ALLOW['cases']:
        f = c['files']
        dau[c['opaque_id']] = {'metric': min_cot(f['metrics.parquet']['path'], 'time'),
                               'trace': min_cot(f['traces.parquet']['path'], 'startTime') // 10 ** 6,
                               'log': min_cot(f['logs.parquet']['path'], 'timestamp') if f.get('logs.parquet') else None}
    for nhom in ('bocpd', 'nsigma'):
        rows = {}
        for oid, d0 in dau.items():
            th = BD[nhom][oid]['luot_rca']['t_hat']
            bins = [th - 300 + BIN * k for k in range(20)]
            r = {'t_hat_giay_tu_dau_file': th - d0['metric'],
                 'bin_N_truoc_trace': sum(b + BIN <= d0['trace'] for b in bins),
                 'bin_N_phu_mot_phan': sum(b < d0['trace'] < b + BIN for b in bins),
                 'bin_N_truoc_log': None if d0['log'] is None else sum(b + BIN <= d0['log'] for b in bins)}
            r['bu_0'] = r['bin_N_truoc_trace'] > 0 or r['bin_N_phu_mot_phan'] > 0
            rows[oid] = r
        v = list(rows.values())
        full = [r['bin_N_truoc_trace'] for r in v if r['bin_N_truoc_trace'] > 0]
        out['theo_bo'][nhom] = {
            'tong_hop': {'ca_co_bin_hoan_toan_truoc_trace': len(full),
                         'ca_chi_phu_mot_phan': sum(r['bin_N_truoc_trace'] == 0 and r['bin_N_phu_mot_phan'] > 0 for r in v),
                         'ca_bu_0': sum(r['bu_0'] for r in v),
                         'so_bin_truoc_trace_min_max': [min(full), max(full)] if full else None,
                         'ca_bu_0_co_t_hat_sau_giay_420': sum(r['bu_0'] and r['t_hat_giay_tu_dau_file'] > 420 for r in v)},
            'theo_ca': rows}
    chung.ghi_json(chung.OUT / 'cham/soi-bin-torai.json', out)
    print(json.dumps({k: v['tong_hop'] for k, v in out['theo_bo'].items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()

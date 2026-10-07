"""T-025 phiên 3 (N1, Minh duyệt 07/10): vì sao N-Sigma báo ngay sau giây 100. Chỉ đọc parquet dev, không đọc nhãn.

Tại đúng chỉ số t̂ của bản ghi bộ phát hiện đã chốt, tính lại luật §7.3 (|x − mean| > 3·std trên iloc[:i], dữ liệu đã
qua D9) cho từng cột; đếm số cột báo, số cột báo có std quá khứ = 0, số cột báo có < 20 điểm quá khứ không NaN.
Không chạy lại bộ phát hiện, không đổi bản ghi.

python soi_nsigma_t_hat.py → results/T-025/cham/soi-nsigma-t-hat.json
"""
import json
import statistics

import numpy as np
import pandas as pd

import chung
from p3.adapters.phat_hien import cot_bocpd

ALLOW = json.loads(chung.ALLOWLIST.read_text(encoding='utf-8'))
BD = json.loads((chung.OUT / 'bao-dong.json').read_text(encoding='utf-8'))['bo_phat_hien']


def main():
    out = {'mo_ta': __doc__.strip(), 'theo_bo': {}}
    for nhom, tap in (('nsigma', 'chinh'), ('nsigma_doi_chung', 'doi_chung')):
        rows = {}
        for c in ALLOW['cases']:
            oid = c['opaque_id']
            m = pd.read_parquet(chung.DATA_ROOT / c['files']['metrics.parquet']['path'])
            i = int(np.where(m['time'].to_numpy() == BD[nhom][oid]['luot_rca']['t_hat'])[0][0])
            cols = cot_bocpd(m.columns) if tap == 'chinh' else [x for x in m.columns if x != 'time']
            d = m[cols].replace([np.inf, -np.inf], np.nan).ffill()
            past = d.iloc[:i]
            sd = past.std()
            trig = (d.iloc[i] - past.mean()).abs() > 3 * sd
            tc = list(trig[trig].index)
            rows[oid] = {'chi_so_t_hat': i, 'so_cot': len(cols), 'so_cot_bao': len(tc),
                         'so_cot_bao_std0': int(sum(sd[k] == 0 for k in tc)),
                         'so_cot_bao_duoi_20_diem': int(sum(int(past[k].notna().sum()) < 20 for k in tc))}
        v = list(rows.values())
        k = [r['so_cot_bao'] for r in v]
        out['theo_bo'][nhom] = {
            'tong_hop': {'so_ca': len(v), 'chi_so_t_hat': sorted(r['chi_so_t_hat'] for r in v),
                         'so_cot_bao': {'trung_vi': statistics.median(k), 'min': min(k), 'max': max(k)},
                         'ca_co_cot_bao_std0': sum(r['so_cot_bao_std0'] > 0 for r in v),
                         'ca_moi_cot_bao_deu_std0': sum(r['so_cot_bao_std0'] == r['so_cot_bao'] for r in v),
                         'ca_co_cot_bao_duoi_20_diem': sum(r['so_cot_bao_duoi_20_diem'] > 0 for r in v)},
            'theo_ca': rows}
    chung.ghi_json(chung.OUT / 'cham/soi-nsigma-t-hat.json', out)
    print(json.dumps({k: {a: b for a, b in v['tong_hop'].items() if a != 'chi_so_t_hat'}
                      for k, v in out['theo_bo'].items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()

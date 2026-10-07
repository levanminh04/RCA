"""T-031 bước 1: yếu tố chi phí sau tiền xử lý ở 30 ca dev (giao-thuc-v2 §12), không dùng nhãn.

Chỉ đọc allowlist và mốc tiêm (cắt cửa sổ chế độ a). Dùng đúng các hàm của src/p3 (cửa sổ §5.2, tiền xử lý
của adapter). CIRCA và TORAI lấy yếu tố từ bản ghi bước 3, 4 (xem chon_ca_pilot.py). Báo theo mã mờ.

python yeu_to.py
"""
import sys

import pandas as pd

import chung
from p3 import cua_so
from p3.adapters import baro, phat_hien

COT_SPAN = ['serviceName', 'methodName', 'operationName', 'startTime', 'duration']


def main():
    al, moc = chung.nap()
    L = chung.Luot('yeu-to')
    rows = []
    for i, oid in enumerate(sorted(al)):
        f = chung.selector.chon_ca(al, oid, chung.ROOT)
        m = pd.read_parquet(f['metrics.parquet'])
        tr = pd.read_parquet(f['traces.parquet'], columns=COT_SPAN)
        lg = pd.read_parquet(f['logs.parquet'], columns=['timestamp']) if 'logs.parquet' in f else None
        t = moc[oid]
        win, info = cua_so.cat_ca(m, tr, lg, t)
        # BOCPD, N-Sigma: cả bản ghi (chế độ b), không dùng mốc
        cot = phat_hien.cot_bocpd(m.columns)
        d = phat_hien.tien_xu_ly_bocpd(m[cot]).shape[1]
        # BARO: cột còn ở cả hai nửa sau tiền xử lý (như diem_lai)
        _, cot_baro = baro.diem_lai(baro.chuan_bi(win['metric']), t)
        sp = win['traces']
        op = sp['serviceName'] + '_' + sp['methodName'].fillna(sp['operationName'])
        r = {'opaque_id': oid, 'T_ban_ghi': int(len(m)), 'cot_metric_file': int(m.shape[1] - 1),
             'bocpd_cot_tho': len(cot), 'bocpd_d': int(d),
             'nsigma_cot': len(cot), 'nsigma_doi_chung_cot': int(m.shape[1] - 1),
             'baro_cot_hai_nua': len(cot_baro),
             'cua_so_cot_metric': int(win['metric'].shape[1] - 1), 'cua_so_dong_metric': int(len(win['metric'])),
             'cua_so_span': int(len(sp)), 'cua_so_operation': int(op.nunique()),
             'cua_so_dong_log': None if win['logs'] is None else int(len(win['logs'])),
             'co_logs_parquet': 'logs.parquet' in f,
             'window': {k: info[k] for k in ('rows_N', 'rows_A', 'seconds_N', 'seconds_A', 'spans_N', 'spans_A',
                                             'log_rows_N', 'log_rows_A')}}
        rows.append(r)
        L.ghi(f'[{i + 1}/30] {oid} d={d} baro={len(cot_baro)} span={r["cua_so_span"]} op={r["cua_so_operation"]} '
              f'log={r["cua_so_dong_log"]} RAM={chung.ram_trong_gb()}GB')
        del m, tr, lg, win, sp
    doc = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'run': L.dir.name, 'ca': rows}
    chung.ghi_json(L.dir / 'yeu-to.json', doc)
    L.xong({'so_ca': len(rows)})


if __name__ == '__main__':
    main()

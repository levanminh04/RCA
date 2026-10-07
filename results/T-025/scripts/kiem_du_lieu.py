"""T-025 bước 0: SHA-256 mọi tệp của 30 ca dev so với allowlist, trên máy đang chạy (laptop hoặc EC2).

Thêm (không nhãn): bảng metric của mỗi ca có cột `time` tăng ngặt, bước 1 s, 1.441 dòng (BOCPD coi thứ tự
dòng là thời gian). Không đọc nhãn.

python kiem_du_lieu.py
"""
import chung


def main():
    import numpy as np
    import pandas as pd
    al = chung.nap_allowlist()
    L = chung.Luot('kiem-du-lieu-' + ('ec2' if chung.EC2 else 'laptop'))
    rows, sai = {}, 0
    for oid in sorted(al):
        f = chung.selector.chon_ca(al, oid, chung.DATA_ROOT, kiem_hash=False)
        r = {}
        for name, p in f.items():
            ok = chung.sha256_file(p) == al[oid]['files'][name]['sha256']
            r[name] = ok
            sai += not ok
        tm = pd.read_parquet(f['metrics.parquet'], columns=['time'])['time'].to_numpy()
        d = np.diff(tm)
        r['metric_time'] = {'n': int(len(tm)), 'tang_ngat': bool((d > 0).all()), 'buoc': sorted({int(x) for x in d})}
        rows[oid] = r
        L.ghi(f'{oid} {r}')
    chung.ghi_json(L.dir / 'kiem-du-lieu.json', {'mo_ta': __doc__.strip(), 'so_ca': len(rows), 'so_tep_sai': sai,
                                                  'ca': rows})
    L.xong({'so_ca': len(rows), 'so_tep_sai': sai})


if __name__ == '__main__':
    main()

"""T-045: soi trung gian của bản ghi pha 1 theo từng ca (QT5; SPEC T-045 bước 1–2), không đọc nhãn.

Theo từng bản ghi: status, verdict (tùy chọn ẩn, Đ-6), khối, trạng thái đơn vị, cổng, điểm, ngưỡng, nhóm kênh có cờ,
OBS_DEPENDENT, RANK_CHANGED, số gộp khóa ghi ra, E2 dự phòng, cột metric chưa khai nguồn, nguồn metric UNSUPPORTED,
trạng thái quan sát theo nguồn, dòng log trong ô OPEN/thiếu thu của N (kiểm điều kiện tương đương của E3, LOG phiên 1).
Chạy: $PY -B results/T-045/scripts/soi_ban_ghi.py <thư mục lượt> [--an-verdict] [--ra <file json>]
"""
import argparse
import collections
import json
import math
import sys
from pathlib import Path

NGUONG_LON = 1e15  # QT5 "ngưỡng cực lớn": chỉ cờ để soi tay; metric bộ nhớ theo byte có thể tới 1e10


def nhom_cua_ma(ma):
    return ma.split('|', 1)[0]


def soi(rec, an_verdict):
    out = {'config_id': rec['config_id'], 'ca': rec['opaque_id'], 'status': rec['status'], 'error': rec.get('error')}
    if not an_verdict:
        out['verdict'] = rec.get('verdict')
    if rec['status'] not in ('OK', 'NO_EVIDENCE'):
        return out
    blocks = rec.get('blocks') or []
    sets = rec.get('sets') or {}
    out['so_khoi'] = len(blocks)
    out['co_khoi_dau'] = sum(len(g) for g in blocks[0]['groups']) if blocks else 0
    out['tra_ve'] = sets.get('returned')
    out['quan_sat'] = sets.get('observed')
    out['toan_hoa'] = len(blocks) == 1 and out['tra_ve'] and out['tra_ve'] > 1
    tang = (rec.get('extra') or {}).get('tang_P') or {}
    out['tang'] = dict(collections.Counter(str(v) for v in tang.values()))
    # đơn vị phân vị
    pv = (rec.get('extra') or {}).get('don_vi_phan_vi') or []
    tt = collections.Counter((nhom_cua_ma(u['ma']), u['trang_thai']) for u in pv)
    out['phan_vi_trang_thai'] = {f'{a}|{b}': n for (a, b), n in sorted(tt.items())}
    cong = collections.Counter()
    e_max, nguong = 0.0, []
    for u in pv:
        if u['trang_thai'] != 'OK':
            continue
        n = nhom_cua_ma(u['ma'])
        for d in ('len', 'xuong'):
            p = u.get(f'p_{d}')
            if p is None:
                continue
            cong[(n, d, 'tinh')] += 1
            cong[(n, d, u.get(f'cach_cong_{d}') or '?')] += 1
            if p < 0.01:
                cong[(n, d, 'p<alpha')] += 1
            if p == 0.01:
                cong[(n, d, 'p==alpha')] += 1
            if u.get(f'F_raw_{d}'):
                cong[(n, d, 'F_raw')] += 1
                e_max = max(e_max, u.get(f'e_{d}') or 0.0)
        for k in ('h', 'l'):
            v = u.get(k)
            if v is not None and (not math.isfinite(v) or abs(v) > NGUONG_LON):
                nguong.append((u['ma'], k, v))
    out['cong_phan_vi'] = {'|'.join(k): v for k, v in sorted(cong.items())}
    out['e_max_phan_vi'] = e_max
    out['nguong_cuc_lon'] = nguong[:10]
    out['so_nguong_cuc_lon'] = len(nguong)
    # đơn vị đếm, theo thế giới
    dem = {}
    for w, x in (rec.get('worlds') or {}).items():
        c = collections.Counter()
        for u in x.get('don_vi_dem') or []:
            n = nhom_cua_ma(u['ma'])
            c[(n, u['trang_thai'])] += 1
            for d in ('len', 'xuong'):
                p = u.get(f'p_{d}')
                if p is not None:
                    c[(n, d, 'tinh')] += 1
                    if p < 0.01:
                        c[(n, d, 'p<alpha')] += 1
                    if p == 0.01:
                        c[(n, d, 'p==alpha')] += 1
                if u.get(f'F_raw_{d}'):
                    c[(n, d, 'F_raw')] += 1
        dem[w] = {'|'.join(map(str, k)): v for k, v in sorted(c.items())}
    out['dem'] = dem
    # kênh có cờ, nhóm kênh (QT5: một nhóm kênh chiếm gần hết)
    kc = (rec.get('extra') or {}).get('kenh_co') or []
    nh = collections.Counter(nhom_cua_ma(k['don_vi'] or k['ma'].split('|', 1)[1]) if k.get('don_vi') else '?' for k in kc)
    out['kenh_co'] = len(kc)
    out['kenh_co_theo_nhom'] = dict(nh)
    out['nhom_chiem'] = (max(nh.values()) / len(kc)) if kc else None
    out['diem_max_kenh'] = max((k['s'] for k in kc), default=0.0)
    out['diem_lon_hon_1'] = sum(1 for k in kc if k['s'] > 1)
    out['diem_lon_hon_1e6'] = sum(1 for k in kc if k['s'] > 1e6)
    out['OBS_DEPENDENT'] = len(rec.get('OBS_DEPENDENT') or [])
    out['RANK_CHANGED'] = rec.get('RANK_CHANGED')
    dg = rec.get('diagnostics') or {}
    out['gop_khoa_ghi_ra'] = dg.get('gop_khoa_ghi_ra')
    out['gop_khoa_ghi_ra_T4c'] = dg.get('gop_khoa_ghi_ra_T4c')
    out['E2_du_phong'] = dg.get('E2_du_phong')
    out['cot_metric_chua_khai_nguon'] = len(dg.get('cot_metric_chua_khai_nguon') or [])
    out['nguon_metric_unsupported'] = dg.get('nguon_metric_unsupported')
    out['NO_VALID_CHANNEL'] = len(dg.get('NO_VALID_CHANNEL') or [])
    out['so_cham_hop_le'] = dg.get('so_cham_hop_le')
    out['span'] = dg.get('span')
    out['do_phu_cham'] = rec.get('do_phu_cham')
    cov = rec.get('coverage') or {}
    out['coverage'] = {n: (q.get('trang_thai') if q.get('trang_thai') != 'OK' else
                           {'T_chac': q.get('T_chac'), 'T_max': q.get('T_max'), 'o': q.get('o')})
                       for n, q in sorted(cov.items())}
    out['coverage_unsupported'] = sorted(n for n, q in cov.items() if q.get('trang_thai') != 'OK')
    tk = ((rec.get('extra') or {}).get('thong_ke_log') or {}).get('theo_thuc_the') or {}
    out['log_dong'] = {'N': sum(v['N']['dong'] for v in tk.values()), 'A': sum(v['A']['dong'] for v in tk.values()),
                       'loi_N': sum(v['N']['loi'] for v in tk.values()), 'loi_A': sum(v['A']['loi'] for v in tk.values()),
                       'unknown_N': sum(v['N']['unknown'] for v in tk.values()),
                       'unknown_A': sum(v['A']['unknown'] for v in tk.values())}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('luot')
    ap.add_argument('--an-verdict', action='store_true')
    ap.add_argument('--ra', default=None)
    a = ap.parse_args()
    d = Path(a.luot)
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    recs = [json.loads(x) for x in (d / meta['tep']).read_text(encoding='utf-8').splitlines() if x]
    kq = [soi(r, a.an_verdict) for r in recs]
    s = json.dumps(kq, ensure_ascii=False, indent=1)
    if a.ra:
        Path(a.ra).write_text(s + '\n', encoding='utf-8')
    else:
        sys.stdout.write(s + '\n')


if __name__ == '__main__':
    main()

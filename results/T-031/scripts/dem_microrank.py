"""T-031 bước 2 (D6, giao-thuc-v2 §6.3, Q-77): MicroRank ở 30 ca dev, cửa sổ §5.2, PYTHONHASHSEED=0.

Chỉ đọc trạng thái và chi phí; không chạy evaluator, không in thứ hạng. Mỗi lượt qua runner P3 (tiến trình con,
giới hạn 3.600 s). Lỗi runner ghi riêng, không phải trạng thái phương pháp. Báo theo mã mờ và nguyên nhân.

python dem_microrank.py
"""
import re

import chung
from p3 import runner

NGUYEN_NHAN = [  # (mẫu trong thông điệp ValueError của src/microrank, nhãn nguyên nhân)
    (r'No normal baseline for', 'operation mới sau mốc (không có nền)'),
    (r'Normal std undefined', 'std nền không xác định (< 2 span)'),
    (r'Conflicting observations', 'ID trùng khác nội dung'),
    (r'Ambiguous service_method', 'khóa service_method mơ hồ'),
    (r'Non-finite suspiciousness|Invalid weighted spectrum', 'điểm không hữu hạn'),
    (r'Invalid span time|Null |Missing', 'đầu vào span không hợp lệ'),
]


def nguyen_nhan(rec):
    if rec['status'] == 'TIMEOUT':
        return 'vượt 3.600 s'
    if rec['status'] != 'ERROR':
        return None
    for pat, ten in NGUYEN_NHAN:
        if re.search(pat, rec.get('error') or ''):
            return ten
    return 'khác'


def so_op(rec):
    """Số operation nêu trong thông điệp 'No normal baseline for: a,b,...' (không ghi tên vào bảng tóm tắt)."""
    m = re.search(r'No normal baseline for: (.*)$', rec.get('error') or '')
    return len(m.group(1).split(',')) if m else None


def main():
    al, moc = chung.nap()
    L = chung.Luot('microrank-30', {'phuong_phap': 'microrank', 'hashseed': 0, 'che_do': 'a'})
    rows = []
    for i, oid in enumerate(sorted(al)):
        ram = chung.ram_trong_gb()
        try:
            rec = runner.chay_luot(al, oid, 'microrank', 'a', moc[oid], L.dir / 'luot', chung.TIMEOUT_S, hashseed=0)[0]
        except Exception as exc:  # noqa: BLE001 — lỗi runner: ghi, không gán trạng thái phương pháp
            rows.append({'opaque_id': oid, 'loi_runner': f'{type(exc).__name__}: {exc}', 'ram_truoc_gb': ram})
            L.ghi(f'[{i + 1}/30] {oid} LỖI RUNNER {type(exc).__name__}: {exc}')
            continue
        r = {'opaque_id': oid, 'run_id': rec['run_id'], 'status': rec['status'],
             'method_status_raw': rec['method_status_raw'], 'nguyen_nhan': nguyen_nhan(rec),
             'so_operation_khong_nen': so_op(rec), 'input_shape': rec['input_shape'],
             'counts': (rec.get('diagnostics') or {}).get('counts'),
             'wall_s': rec['cost']['wall_s'], 'peak_rss_mb': rec['cost']['peak_rss_mb'],
             'buoc_s': rec['cost'].get('buoc_s'), 'ram_truoc_gb': ram}
        rows.append(r)
        L.ghi(f'[{i + 1}/30] {oid} {r["status"]} {r["nguyen_nhan"] or ""} wall={r["wall_s"]}s '
              f'rss={r["peak_rss_mb"]}MB RAM={ram}GB')
    tong = {}
    for r in rows:
        k = r.get('status', 'LOI_RUNNER')
        tong[k] = tong.get(k, 0) + 1
    theo_nn = {}
    for r in rows:
        if r.get('nguyen_nhan'):
            theo_nn.setdefault(r['nguyen_nhan'], []).append(r['opaque_id'])
    loi = sum(r.get('status') in ('ERROR', 'TIMEOUT') for r in rows)
    doc = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'run': L.dir.name,
           'src_p3_sha256': L.ch['src_p3']['tong'], 'timeout_moi_luot_s': chung.TIMEOUT_S,
           'tong_theo_trang_thai': tong, 'ca_theo_nguyen_nhan': theo_nn,
           'so_ca_error_timeout': loi, 'so_ca_loi_runner': tong.get('LOI_RUNNER', 0),
           'dung_nhanh_microrank_D6': loi >= 1,
           'chi_phi': {'tong_wall_s': round(sum(r.get('wall_s') or 0 for r in rows), 1),
                       'max_peak_rss_mb': max((r.get('peak_rss_mb') or 0) for r in rows)},
           'ca': rows}
    chung.ghi_json(L.dir / 'dem-loi-microrank.json', doc)
    L.xong({k: doc[k] for k in ('tong_theo_trang_thai', 'so_ca_error_timeout', 'dung_nhanh_microrank_D6', 'chi_phi')})


if __name__ == '__main__':
    main()

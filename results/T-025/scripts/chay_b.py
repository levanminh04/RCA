"""T-025 bước 1–2: chạy một bộ phát hiện chế độ (b) qua runner P3 trên 30 ca dev, tuần tự theo mã mờ.

Vai runner chế độ (b): chỉ đọc allowlist, không đọc nhãn hay mốc tiêm (SPEC bước 1). Bộ phát hiện nhận cả bản ghi
1.441 điểm (§7.1). Mỗi lượt = một ca, tiến trình con; giới hạn khai trước trong SPEC: BOCPD 21.600 s, N-Sigma 3.600 s.
Vượt → TIMEOUT, giữ lượt, chạy ca tiếp. Tiến độ từng ca: tien-do.txt của lượt và (nếu có) tệp trạng thái chung.

python chay_b.py <ten> <bocpd|nsigma> [tap_cot=bocpd|tat_ca] [ca=all|oid,oid] [trang_thai=<tệp>]
"""
import hashlib
import json
import sys
from pathlib import Path

import chung


def h(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def cho_t024(L, poll=30):
    """SPEC: không chạy cạnh T-024 trên laptop. Đợi khi có tiến trình mà dòng lệnh chứa 'T-024'. Trả số giây đợi."""
    import time
    import psutil
    t0, bao = time.perf_counter(), False
    while True:
        dang = []
        for p in psutil.process_iter(['pid', 'cmdline']):
            try:
                if any('T-024' in (a or '') for a in (p.info['cmdline'] or [])):
                    dang.append(p.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        if not dang:
            return round(time.perf_counter() - t0, 1)
        if not bao:
            L.ghi(f'đợi T-024 (pid {dang})')
            bao = True
        time.sleep(poll)


def main(ten, method, tap_cot='bocpd', ca='all', trang_thai=None):
    runner = chung.cau_hinh_runner()
    al = chung.nap_allowlist()
    ids = sorted(al) if ca == 'all' else ca.split(',')
    to = chung.timeout_cho(method)
    L = chung.Luot(ten, {'phuong_phap': method, 'tap_cot': tap_cot, 'ca': ids, 'timeout_moi_luot_s': to,
                         'mode': 'b'}, trang_thai=trang_thai)
    base = L.dir / 'luot'
    rows = []
    for n, oid in enumerate(ids, 1):
        doi = 0.0 if chung.EC2 else cho_t024(L)
        ram = chung.ram_trong_gb()
        L.ghi(f'[{n}/{len(ids)}] {oid} bắt đầu; RAM trống {ram} GB')
        row = {'opaque_id': oid, 'ram_truoc_gb': ram, 'doi_t024_s': doi}
        try:
            recs = runner.chay_luot(al, oid, method, 'b', None, base, to, repo_root=chung.DATA_ROOT, tap_cot=tap_cot)
            r = recs[0]
            row.update({'run_id': r['run_id'], 'status': r['status'], 'error': r.get('error'),
                        'so_bao_dong': len(r.get('alarms') or []), 'bao_dong_hash': h(r.get('alarms')),
                        'luot_rca': r.get('luot_rca'), 'input_shape': r.get('input_shape'),
                        'diagnostics': r.get('diagnostics'),
                        'cost': {k: r['cost'].get(k) for k in ('wall_s', 'peak_rss_mb', 'exit_code', 'timed_out')},
                        'buoc_s': r['cost'].get('buoc_s')})
        except Exception as exc:  # noqa: BLE001 — lỗi runner, không phải trạng thái phương pháp
            row['loi_runner'] = f'{type(exc).__name__}: {exc}'
        rows.append(row)
        L.ghi(f'[{n}/{len(ids)}] {oid} {row.get("status") or "LOI_RUNNER " + row.get("loi_runner", "")} '
              f'wall={(row.get("cost") or {}).get("wall_s")}s rss={(row.get("cost") or {}).get("peak_rss_mb")}MB '
              f'shape={row.get("input_shape")}')
        chung.ghi_json(L.dir / 'tom-tat.json', {'mo_ta': __doc__.strip(), 'run': L.dir.name,
                                                'src_p3_sha256': L.ch['src_p3']['tong'], 'xong': False, 'luot': rows})
    tw = round(sum((r.get('cost') or {}).get('wall_s') or 0 for r in rows), 1)
    chung.ghi_json(L.dir / 'tom-tat.json', {'mo_ta': __doc__.strip(), 'run': L.dir.name,
                                            'src_p3_sha256': L.ch['src_p3']['tong'], 'xong': True, 'tong_wall_s': tw,
                                            'so_loi_runner': sum('loi_runner' in r for r in rows), 'luot': rows})
    L.xong({'tong_wall_s': tw, 'so_luot': len(rows), 'trang_thai': {s: sum(r.get('status') == s for r in rows)
                                                                   for s in ('OK', 'ERROR', 'TIMEOUT')}})


if __name__ == '__main__':
    kw = dict(a.split('=', 1) for a in sys.argv[3:])
    main(sys.argv[1], sys.argv[2], **kw)

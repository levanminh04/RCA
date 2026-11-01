"""T-045 D3 (không nhãn, pha 1, chỉ mô tả; SPEC T-045 bước 2b): so ba cách khớp của E3 (`params.tham_so_E3.khop`):
(a) hoan_toan, (b) nguong, (c) nguong_cung_lop, trên bản ghi cấu hình R0 + E3 (`K-E3`). Chỉ đọc
`extra.thong_ke_log` (cặp thực thể–mẫu, ô mẫu mới) và các đơn vị log của thế giới P; không đọc `verdict` (Đ-6).

Đại lượng theo ca và gộp theo dataset:
- số mẫu theo thực thể (cặp thực thể–mẫu học từ N);
- tỷ lệ dòng A vào "mẫu mới" (Σ mau_moi / Σ dòng A);
- số thực thể có cờ "mẫu mới" (đơn vị `log|<e>|mau_moi` có F_raw lên ở thế giới P) — ở mốc giả RE2-TT là đại lượng SPEC;
- số dòng A là dòng lỗi bị gán vào mẫu lớp thường (Σ loi_xac_dinh_A của cặp lớp 'thuong');
- năm mẫu đầu (theo n_N + n_A giảm dần) của hai ca đầu theo mã mờ mỗi dataset (Đ-11).
Chạy: $PY -B results/T-045/scripts/d3_e3_khong_nhan.py --luot <khop>=<thư mục lượt> ... --ra <json>
"""
import argparse
import collections
import json
from pathlib import Path


def doc(d):
    """Đọc theo dòng; chỉ giữ bản ghi cấu hình K-E3 (lượt khối K có 16 cấu hình, khoảng 0,9 GB)."""
    d = Path(d)
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    out = []
    with open(d / meta['tep'], encoding='utf-8') as f:
        for x in f:
            if x.strip():
                r = json.loads(x)
                if r['config_id'].split('|')[0] == 'K-E3':
                    out.append(r)
    return out


def theo_ca(rec):
    if rec['status'] not in ('OK', 'NO_EVIDENCE'):
        return {'status': rec['status'], 'error': rec.get('error')}
    tk = (rec.get('extra') or {}).get('thong_ke_log') or {}
    cap = tk.get('cap_drain') or []
    mm = tk.get('mau_moi') or {}
    tt = tk.get('theo_thuc_the') or {}
    dong_A = sum(v['A']['dong'] for v in tt.values())
    loi_A = sum(v['A']['loi'] for v in tt.values())
    mau_theo_e = collections.Counter(c['thuc_the'] for c in cap)
    lop = collections.Counter(c['lop'] for c in cap)
    loi_vao_thuong = sum(c['loi_xac_dinh_A'] for c in cap if c['lop'] == 'thuong')
    loi_vao_loi = sum(c['loi_xac_dinh_A'] for c in cap if c['lop'] == 'loi')
    dv = ((rec.get('worlds') or {}).get('P') or {}).get('don_vi_dem') or []
    co_mau_moi = sorted({u['ma'].split('|')[1] for u in dv if u['ma'].endswith('|mau_moi') and u.get('F_raw_len')})
    top = sorted(cap, key=lambda c: (-(c['n_N'] + c['n_A']), c['thuc_the'], str(c['mau'])))[:5]
    return {'status': rec['status'], 'so_cap_mau': len(cap), 'so_thuc_the_co_mau': len(mau_theo_e),
            'mau_theo_thuc_the': dict(sorted(mau_theo_e.items())), 'lop_cap': dict(lop),
            'dong_A': dong_A, 'dong_A_mau_moi': sum(mm.values()),
            'ti_le_A_mau_moi': (sum(mm.values()) / dong_A) if dong_A else None,
            'dong_loi_A': loi_A, 'dong_loi_A_vao_mau_thuong': loi_vao_thuong, 'dong_loi_A_vao_mau_loi': loi_vao_loi,
            'dong_loi_A_vao_mau_moi_hoac_khong_xac_dinh': loi_A - loi_vao_thuong - loi_vao_loi,
            'thuc_the_co_co_mau_moi_P': co_mau_moi,
            'nam_mau_dau': [{'thuc_the': c['thuc_the'], 'khuon': c['khuon'], 'lop': c['lop'], 'n_N': c['n_N'],
                             'n_A': c['n_A']} for c in top]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', action='append', required=True, help='<nhãn>=<thư mục lượt>')
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    out = {'luot': {}, 'tong_hop': {}}
    for x in a.luot:
        nhan, d = x.split('=', 1)
        recs = doc(d)  # D3 chỉ trên R0 + E3
        ca = {r['opaque_id']: theo_ca(r) for r in recs}
        ok = [c for c in ca.values() if c['status'] in ('OK', 'NO_EVIDENCE')]
        out['luot'][nhan] = {'thu_muc': d, 'config_id': sorted({r['config_id'] for r in recs}), 'ca': ca}
        tA = sum(c['dong_A'] for c in ok)
        out['tong_hop'][nhan] = {
            'so_ca': len(ca), 'so_ca_loi': len(ca) - len(ok),
            'so_cap_mau': sum(c['so_cap_mau'] for c in ok),
            'so_mau_tren_thuc_the_trung_vi': (sorted(v for c in ok for v in c['mau_theo_thuc_the'].values())
                                              or [None])[len([v for c in ok for v in c['mau_theo_thuc_the'].values()]) // 2],
            'dong_A': tA, 'dong_A_mau_moi': sum(c['dong_A_mau_moi'] for c in ok),
            'ti_le_A_mau_moi': (sum(c['dong_A_mau_moi'] for c in ok) / tA) if tA else None,
            'dong_loi_A': sum(c['dong_loi_A'] for c in ok),
            'dong_loi_A_vao_mau_thuong': sum(c['dong_loi_A_vao_mau_thuong'] for c in ok),
            'so_ca_co_dong_loi_A_vao_mau_thuong': sum(1 for c in ok if c['dong_loi_A_vao_mau_thuong']),
            'so_thuc_the_co_co_mau_moi_P': sum(len(c['thuc_the_co_co_mau_moi_P']) for c in ok),
            'so_ca_co_co_mau_moi_P': sum(1 for c in ok if c['thuc_the_co_co_mau_moi_P'])}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(out['tong_hop'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

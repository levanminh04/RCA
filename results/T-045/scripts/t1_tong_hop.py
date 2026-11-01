"""T-045 T1 (không nhãn; SPEC T-045 bước 2, đầu ra 2): tổng hợp từ các lượt R0.
- Bất biến hash seed: sha256 của `ban-ghi.jsonl` giống nhau giữa các lượt seed; lệch thì liệt kê ca và trường lệch.
- Bất biến thứ tự hàng: lượt xáo so với lượt seed 0 (cùng seed), như trên.
- QT5 theo ca (`soi_ban_ghi.soi`): điểm > 1, > 1e6, toàn hòa, ngưỡng cực lớn, nhóm kênh chiếm gần hết.
- Phân bố điểm (kênh có cờ ở P), trạng thái đơn vị, verdict của lượt chính (R0, T1 — được nhìn trước D17).
- Mốc giả (RE2-TT): tỷ lệ qua cổng theo loại đơn vị và nguồn; tỷ lệ CAUSE_FOUND tuyệt đối trên cửa sổ khác
  INSUFFICIENT_EVIDENCE (D17).
- Đ5 (Q-209): số đơn vị đếm có quyết định cổng đổi khi T lệch ±1% (`e4.doi_quyet_dinh_khi_T_lech`), thế giới P.
Chạy: $PY -B results/T-045/scripts/t1_tong_hop.py --seed 0=<lượt> --seed 1=<lượt> --seed 2=<lượt> --xao <lượt>
      [--moc-gia <lượt>] --ra <json>
"""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1 import e4, runner  # noqa: E402
import soi_ban_ghi  # noqa: E402


def doc(d):
    d = Path(d)
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    du = (d / meta['tep']).read_bytes()
    if hashlib.sha256(du).hexdigest() != meta['sha256']:
        raise SystemExit(f'hash lệch ở {d}')
    return meta, {(r['config_id'], r['opaque_id']): r for r in (json.loads(x) for x in du.decode('utf-8').splitlines() if x)}


def truong_lech(a, b, duong=''):
    if type(a) is not type(b):
        return [duong or '/']
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f'{duong}/{k}')
            else:
                out += truong_lech(a[k], b[k], f'{duong}/{k}')
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [f'{duong}[len]']
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += truong_lech(x, y, f'{duong}[{i}]')
        return out
    return [] if a == b else [duong]


def so_luot(goc, khac):
    mg, rg = goc
    mk, rk = khac
    out = {'sha256_goc': mg['sha256'], 'sha256_khac': mk['sha256'], 'giong_het': mg['sha256'] == mk['sha256']}
    if not out['giong_het']:
        lech = {}
        for k in sorted(set(rg) | set(rk)):
            if k not in rg or k not in rk:
                lech['|'.join(k)] = ['thiếu bản ghi']
                continue
            t = truong_lech(rg[k], rk[k])
            if t:
                lech['|'.join(k)] = t[:20]
        out['ca_lech'] = lech
    return out


def d5_dem(rec, ts):
    n, doi = 0, []
    for u in ((rec.get('worlds') or {}).get('P') or {}).get('don_vi_dem') or []:
        if u['trang_thai'] != 'OK' or u.get('T_N') is None:
            continue
        n += 1
        if e4.doi_quyet_dinh_khi_T_lech(u['n_N'], u['n_A'], u['T_N'], u['T_A'], ts):
            doi.append(u['ma'])
    return n, doi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', action='append', default=[])
    ap.add_argument('--xao', default=None)
    ap.add_argument('--moc-gia', default=None)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    seeds = dict(x.split('=', 1) for x in a.seed)
    luot = {s: doc(d) for s, d in seeds.items()}
    goc = luot['0']
    out = {'luot': {'seed': seeds, 'xao': a.xao, 'moc_gia': a.moc_gia}, 'bat_bien': {}}
    for s in sorted(luot):
        if s != '0':
            out['bat_bien'][f'seed0_vs_seed{s}'] = so_luot(goc, luot[s])
    if a.xao:
        out['bat_bien']['seed0_vs_xao'] = so_luot(goc, doc(a.xao))
    ts = dict(runner.TS_HOP_DONG)
    # theo ca, lượt chính (seed 0)
    ca = {}
    for (cid, oid), r in sorted(goc[1].items()):
        s = soi_ban_ghi.soi(r, an_verdict=False)
        n_d5, doi = d5_dem(r, ts) if r['status'] == 'OK' else (0, [])
        s['D5_T_lech_1pt'] = {'so_don_vi_dem_OK_P': n_d5, 'so_doi_quyet_dinh': len(doi), 'don_vi': doi}
        ca[oid] = s
    out['theo_ca'] = ca
    ok = [c for c in ca.values() if c['status'] == 'OK']
    out['tong_hop'] = {
        'so_ca': len(ca), 'status': dict(collections.Counter(c['status'] for c in ca.values())),
        'verdict': dict(collections.Counter(c.get('verdict') for c in ca.values())),
        'QT5': {'ca_diem_lon_hon_1': sum(1 for c in ok if c['diem_lon_hon_1']),
                'ca_diem_lon_hon_1e6': sum(1 for c in ok if c['diem_lon_hon_1e6']),
                'ca_toan_hoa': sum(1 for c in ok if c['toan_hoa']),
                'ca_nguong_cuc_lon': sum(1 for c in ok if c['so_nguong_cuc_lon']),
                'ca_nhom_kenh_tren_90pt': sum(1 for c in ok if (c['nhom_chiem'] or 0) > 0.9),
                'ca_gop_khoa_ghi_ra': sum(1 for c in ok if any((c['gop_khoa_ghi_ra'] or {}).values())),
                'ca_gop_khoa_T4c': sum(1 for c in ok if c['gop_khoa_ghi_ra_T4c']),
                'ca_cot_metric_chua_khai_nguon': sum(1 for c in ok if c['cot_metric_chua_khai_nguon']),
                'ca_nguon_metric_unsupported': sum(1 for c in ok if c['nguon_metric_unsupported']),
                'ca_coverage_unsupported': sum(1 for c in ok if c['coverage_unsupported']),
                'ca_OBS_DEPENDENT': sum(1 for c in ok if c['OBS_DEPENDENT']),
                'ca_RANK_CHANGED': sum(1 for c in ok if c['RANK_CHANGED'])},
        'kenh_co_P': {'tong': sum(c['kenh_co'] for c in ok),
                      'theo_nhom': dict(sum((collections.Counter(c['kenh_co_theo_nhom']) for c in ok), collections.Counter()))},
        'D5_T_lech_1pt': {'so_don_vi_dem_OK_P': sum(c['D5_T_lech_1pt']['so_don_vi_dem_OK_P'] for c in ca.values()),
                          'so_doi_quyet_dinh': sum(c['D5_T_lech_1pt']['so_doi_quyet_dinh'] for c in ca.values())}}
    if a.moc_gia:
        mg = doc(a.moc_gia)[1]
        cong = collections.Counter()
        vd = collections.Counter()
        for (cid, oid), r in sorted(mg.items()):
            vd[r.get('verdict')] += 1
            s = soi_ban_ghi.soi(r, an_verdict=False)
            for k, v in (s.get('cong_phan_vi') or {}).items():
                cong['phan_vi|' + k] += v
            for k, v in ((s.get('dem') or {}).get('P') or {}).items():
                cong['dem|' + k] += v
        n = sum(v for k, v in vd.items() if k not in ('INSUFFICIENT_EVIDENCE', None))
        out['moc_gia'] = {'so_cua_so': len(mg), 'verdict': dict(vd), 'mau_so': n,
                          'ti_le_CAUSE_FOUND': (vd.get('CAUSE_FOUND', 0) / n) if n else None,
                          'cong': dict(sorted(cong.items()))}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'bat_bien': {k: v['giong_het'] for k, v in out['bat_bien'].items()},
                      'tong_hop': out['tong_hop'], 'moc_gia': {k: v for k, v in (out.get('moc_gia') or {}).items()
                                                               if k != 'cong'}}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

"""T-045: tách RR theo dataset và loại lỗi cho R0, T4c, cấu hình thắng khối K, nhánh z (T4b) và sáu baseline (QT15:
tách theo ô trước khi nêu mẫu hình; MRP P7 báo theo dataset, loại lỗi). Chỉ mô tả. Đọc nhãn.
Chạy: $PY -B results/T-045/scripts/theo_loai_loi.py --thang E1+E2 --ra results/T-045/theo-loai-loi.json
"""
import argparse
import collections
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1_danh_gia import pha2, rr  # noqa: E402
from p3 import danh_gia  # noqa: E402
import d2_baseline as d2  # noqa: E402
import pha2_khoi_k as pk  # noqa: E402

RUNS = ROOT / 'results/T-045/runs'


def rr_luot(L, cid, nhan, khoa='blocks'):
    out = {}
    d = pk.phan_cua(L)[cid] if (RUNS / L / 'theo-cau-hinh').exists() else RUNS / L
    for x in (d / 'ban-ghi.jsonl').read_text(encoding='utf-8').splitlines():
        if x:
            r = json.loads(x)
            if r['config_id'] != cid:
                continue
            o = r['opaque_id']
            b = r['blocks'] if khoa == 'blocks' else (r['extra'].get('T4c') or {}).get('blocks')
            out[o] = rr.rr_ca(b or [], nhan[o]['root'], r['status'] == 'OK')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--thang', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    nhan = pk.nap_nhan(False)
    pp = {}
    for L in ('b2b-k16-re2-001', 'b5-k16-nezha-001'):
        for k, cid in (('R0', 'K-R0'), (f'thang {a.thang}', 'K-' + a.thang)):
            pp.setdefault(k, {}).update(rr_luot(L, cid, nhan))
    for L in ('b2-t1-re2-seed0-001', 'b2-t1-nezha-seed0-001'):
        pp.setdefault('T4c', {}).update(rr_luot(L, 'T1-R0', nhan, khoa='T4c'))
    for L in ('b4-t4b-re2-001', 'b4-t4b-nezha-001'):
        pp.setdefault('z (T4b)', {}).update(rr_luot(L, 'T4b-z', nhan))
    # baseline: theo cách của D2 (trung bình seed)
    dn = d2.doc('results/T-043/dinh-nghia-pha2.json')
    chon24 = {tuple(x) for x in dn['ban_ghi_baseline']['RE2-TT']['chon']}
    idx = [(('RE2-TT', r['method'], r['variant']), r) for r in d2.doc('results/T-024/ban-ghi-dua-vao-cham.json')['records']
           if (r['method'], r['variant']) in chon24]
    idx += [(('Nezha-OB', r['method'], r['variant']), r) for r in d2.doc('results/T-026/ban-ghi-dua-vao-cham.json')['unique_records']
            if r['source_view'] == 'main']
    bl = collections.defaultdict(lambda: collections.defaultdict(list))
    for (ds, m, v), r in idx:
        rec = json.loads((ROOT / r['path']).read_text(encoding='utf-8'))
        ok = rec.get('status') == 'OK'
        bl[f'{m}/{v}'][r['opaque_id']].append(rr.rr_ca(danh_gia.khoi_tu_ban_ghi(rec) if ok else [], nhan[r['opaque_id']]['root'], ok))
    for k, v in bl.items():
        pp['baseline ' + k] = {o: sum(x, Fraction(0)) / len(x) for o, x in v.items()}
    out = {}
    for ten, rrs in pp.items():
        g = collections.defaultdict(list)
        for o, x in rrs.items():
            g[(nhan[o]['dataset'], nhan[o]['loai_loi'])].append(x)
            g[(nhan[o]['dataset'], 'tat_ca')].append(x)
        out[ten] = {f'{d}|{l}': {'n': len(x), 'MRR': float(sum(x, Fraction(0)) / len(x))} for (d, l), x in sorted(g.items())}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    khoa = sorted({k for v in out.values() for k in v})
    print('nhóm'.ljust(26) + ''.join(t[:12].rjust(13) for t in out))
    for k in khoa:
        print(k[:26].ljust(26) + ''.join((f"{out[t][k]['MRR']:.3f}" if k in out[t] else '-').rjust(13) for t in out))


if __name__ == '__main__':
    main()

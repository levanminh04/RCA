"""T-045: lần theo cơ chế hai kết cục quan trọng của khối K (luật cứng 15; chỉ mô tả, không đổi lựa chọn). Đọc nhãn.

(1) E3 trong cặp (R0, E3) và (E1+E2, E1+E2+E3): ở ca root tụt RR, các thực thể đứng trước hẳn root ở cấu hình bật E3
    có kênh mạnh nhất (điểm lớn nhất, phá hòa theo mã) thuộc nhóm đơn vị nào: `log|…|mau_moi` (ô mẫu mới), `log|…|mau:…`
    (mẫu Drain lỗi hoặc thường), `op|` (thời lượng, gồm hướng xuống do E3 thêm), `metric|` …; so với ca root không đổi.
(2) E5 trong cặp (E1+E2, E1+E2+E5): ở ca root tụt hạng, kênh của root bị E5 coi là kế thừa (`inherited_by` trạng
    thái `ap_dung`) được giải thích bởi kênh nào (thực thể, nhóm đơn vị, lớp) và qua quy tắc nào.
Chạy: $PY -B results/T-045/scripts/co_che_khoi_k.py --ra results/T-045/co-che-khoi-k.json
"""
import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1_danh_gia import rr  # noqa: E402
import pha2_khoi_k as pk  # noqa: E402


def nhom_dv(ma):
    p = ma.split('|')
    if p[0] == 'log':
        return 'log|mau_moi' if p[-1] == 'mau_moi' else ('log|mau' if p[-1].startswith('mau:') else 'log|log_loi')
    if p[0] == 'metric':
        return 'metric|' + p[1].split('_', 1)[1] if '_' in p[1] else 'metric'
    return p[0]


def vi_tri(blocks):
    out = {}
    for bi, b in enumerate(blocks or []):
        for gi, g in enumerate(b['groups']):
            for e in g:
                out[e] = (bi, gi)
    return out


def truoc(a, r):
    return a[0] < r[0] or (a[0] == r[0] and a[1] < r[1])


def kenh_manh(rec, e):
    ks = [k for k in rec['extra']['kenh_co'] if k['thuc_the'] == e]
    if not ks:
        return None
    k = max(ks, key=lambda k: (k['s'], k['ma']))
    return {'nhom': nhom_dv(k['don_vi']) + ('|xuong' if k['huong'] == 'xuong' else ''), 'lop': k['lop'], 's': k['s']}


def so_E3(nhan, tat, bat):
    out = {'ca_tut': 0, 'ca_khong_doi_hoac_tang': 0, 'nhom_kenh_vuot_root': collections.Counter(),
           'so_thuc_the_vuot_root_tang_them': [], 'theo_dataset': collections.Counter(), 'vi_du': []}
    for L in pk.LUOT_THAT:
        rt, rb = pk.doc_ban_ghi(L, 'K-' + tat), pk.doc_ban_ghi(L, 'K-' + bat)
        for o in sorted(rb):
            root = nhan[o]['root']
            a, b = rr.rr_ca(rt[o]['blocks'] or [], root), rr.rr_ca(rb[o]['blocks'] or [], root)
            if b >= a:
                out['ca_khong_doi_hoac_tang'] += 1
                continue
            out['ca_tut'] += 1
            out['theo_dataset'][nhan[o]['dataset']] += 1
            vt_t, vt_b = vi_tri(rt[o]['blocks']), vi_tri(rb[o]['blocks'])
            vuot_t = {e for e in vt_t if root in vt_t and truoc(vt_t[e], vt_t[root])}
            vuot_b = {e for e in vt_b if root in vt_b and truoc(vt_b[e], vt_b[root])}
            moi = sorted(vuot_b - vuot_t)
            out['so_thuc_the_vuot_root_tang_them'].append(len(moi))
            for e in moi:
                k = kenh_manh(rb[o], e)
                out['nhom_kenh_vuot_root'][k['nhom'] if k else 'khong_kenh'] += 1
            if len(out['vi_du']) < 4:
                out['vi_du'].append({'ca': o, 'dataset': nhan[o]['dataset'], 'RR_tat': float(a), 'RR_bat': float(b),
                                     'root_kenh_manh_tat': kenh_manh(rt[o], root), 'root_kenh_manh_bat': kenh_manh(rb[o], root),
                                     'vuot_moi': [{'thuc_the': e, **(kenh_manh(rb[o], e) or {})} for e in moi[:5]]})
    n = out['so_thuc_the_vuot_root_tang_them']
    out['so_thuc_the_vuot_root_tang_them'] = {'trung_vi': sorted(n)[len(n) // 2] if n else None, 'tong': sum(n)}
    out['nhom_kenh_vuot_root'] = dict(out['nhom_kenh_vuot_root'].most_common())
    out['theo_dataset'] = dict(out['theo_dataset'])
    return out


def so_E5(nhan, tat, bat):
    out = {'ca_tut': 0, 'ca_tang': 0, 'giai_thich_kenh_root': collections.Counter(), 'quy_tac': collections.Counter(),
           'lop_kenh_root_mat': collections.Counter(), 'vi_du': []}
    for L in pk.LUOT_THAT:
        rt, rb = pk.doc_ban_ghi(L, 'K-' + tat), pk.doc_ban_ghi(L, 'K-' + bat)
        for o in sorted(rb):
            root = nhan[o]['root']
            a, b = rr.rr_ca(rt[o]['blocks'] or [], root), rr.rr_ca(rb[o]['blocks'] or [], root)
            if b > a:
                out['ca_tang'] += 1
            if b >= a:
                continue
            out['ca_tut'] += 1
            ib = [i for i in rb[o]['inherited_by'] if i['thuc_the'] == root and i['trang_thai'] == 'ap_dung']
            kc = {k['ma']: k for k in rb[o]['extra']['kenh_co']}
            for i in ib:
                g = kc.get(i['giai_thich_ma'])
                out['giai_thich_kenh_root'][(nhom_dv(g['don_vi']) + '|' + g['lop']) if g else 'ngoai_U'] += 1
                out['quy_tac'][i['quy_tac']] += 1
                k = kc.get(i['ma'])
                if k:
                    out['lop_kenh_root_mat'][nhom_dv(k['don_vi']) + '|' + k['lop']] += 1
            if len(out['vi_du']) < 4:
                out['vi_du'].append({'ca': o, 'dataset': nhan[o]['dataset'], 'RR_tat': float(a), 'RR_bat': float(b),
                                     'giai_thich': [{'kenh_root': i['ma'], 'boi': i['giai_thich_ma'], 'quy_tac': i['quy_tac']}
                                                    for i in ib[:4]]})
    for k in ('giai_thich_kenh_root', 'quy_tac', 'lop_kenh_root_mat'):
        out[k] = dict(out[k].most_common())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    nhan = pk.nap_nhan(False)
    out = {'E3_R0': so_E3(nhan, 'R0', 'E3'), 'E3_E1+E2': so_E3(nhan, 'E1+E2', 'E1+E2+E3'),
           'E5_E1+E2': so_E5(nhan, 'E1+E2', 'E1+E2+E5'), 'E5_R0': so_E5(nhan, 'R0', 'E5')}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for k, v in out.items():
        print(k, json.dumps({x: y for x, y in v.items() if x != 'vi_du'}, ensure_ascii=False))


if __name__ == '__main__':
    main()

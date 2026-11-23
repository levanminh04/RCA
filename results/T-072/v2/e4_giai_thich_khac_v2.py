# -*- coding: utf-8 -*-
"""T-072 v2 — độ phủ và khoảng cách tới ngưỡng của từng chuỗi luật."""
import collections
import importlib.util
import json
import pathlib
import sys

CODE = pathlib.Path(__file__).resolve()
spec = importlib.util.spec_from_file_location('cham_offline_v2', CODE.with_name('cham_offline_v2.py'))
cham = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(cham)


def giai_thich(bt, du, ng, ph):
    luoi = sorted(du.luoi)
    lop_buoc = {t: ph.lop(t // 60 * 60) for t in luoi}
    out = {'so_buoc_theo_lop': dict(collections.Counter(lop_buoc.values())), 'luat': {}}
    for L in bt['luat']:
        data = du.chuoi.get('tin-hieu/' + L['uid'], {})
        th = cham.nguong_cua(L, ng)
        op, fs = L['dieu_kien']['phep'], L['for_s']
        o = {'nguong': th, 'phep': op, 'so_instance': len(data), 'theo_lop': {}}
        for lop in ('khoe-x1', 'flash', 'bien'):
            bs = [t for t in luoi if lop_buoc[t] == lop]
            r = {'buoc': len(bs)}
            for k, d in sorted(data.items()):
                vals = [d[t] for t in bs if t in d]
                S = []
                for t in bs:
                    mau = [d.get(u) for u in range(t - fs, t + 1, cham.STEP)]
                    if None not in mau:
                        S.append(cham.gia_tri_duy_tri(op, mau))
                rr = {'diem': len(vals), 'ty_le_co_diem': round(len(vals) / len(bs), 4) if bs else None}
                if vals:
                    rr.update({'max_tho': max(vals), 'min_tho': min(vals),
                               'so_buoc_tho_vuot': sum(cham.dung(op, v, th) for v in vals)})
                if S:
                    rr.update({'max_duy_tri_for': max(S) if op == '>' else None,
                               'min_duy_tri_for': min(S) if op == '<' else None})
                r[k or '(mot-chuoi)'] = rr
            o['theo_lop'][lop] = r
        out['luat'][L['uid']] = o
    for r in bt['tham_so_co_dinh']['routes']:
        for ten in (f'phu/tong-{r}', f'phu/5xx-{r}', f'phu/ty-le-loi-chua-chan-5xx-{r}'):
            d = du.chuoi.get(ten, {}).get(r, {})
            for lop in ('khoe-x1', 'flash'):
                vals = [d[t] for t in luoi if lop_buoc[t] == lop and t in d]
                out.setdefault('phu', {})[f'{ten}|{lop}'] = {
                    'diem': len(vals), 'min': min(vals) if vals else None, 'max': max(vals) if vals else None}
    return out


def main():
    g = cham.GOC
    du = cham.Du()
    for f in sorted((g / 'e4/xuat').glob('*.t072.json')):
        du.them(cham.nap(f))
    ph = cham.Phut(cham.nap(g / 'e4/phut.json'))
    out = giai_thich(cham.nap(g / 'bieu-thuc.json'), du, cham.nap(g / 'nguong.json')['nguong'], ph)
    out['dau_vao_sha256'] = {str(p): cham.sha(p) for p in (CODE, cham.CODE)}
    cham.RA.mkdir(exist_ok=True)
    dich = cham.RA / 'giai-thich-khac.json'
    dich.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(dich)


if __name__ == '__main__':
    main()

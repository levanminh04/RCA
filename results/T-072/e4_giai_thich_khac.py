# -*- coding: utf-8 -*-
"""T-072 E4: xét giải thích khác cho "0 sự cố": độ phủ dữ liệu từng chuỗi luật theo lớp phút, khoảng cách tới ngưỡng
(giá trị duy trì for_s, giá trị thô), NoData. Chỉ đọc chuỗi đã chuyển và phân loại phút. Ghi e4/giai-thich-khac.json."""
import json, glob, pathlib, collections
G = pathlib.Path(__file__).parent
src = (G / 'cham_offline.py').read_text(encoding='utf-8'); ns = {'__name__': 'lib', '__file__': str(G / 'cham_offline.py')}
exec(compile(src.rstrip()[:-len('main()')], 'cham_offline.py', 'exec'), ns)
du = ns['Du']()
for f in sorted(glob.glob(str(G / 'e4/xuat/*.t072.json'))): du.them(json.loads(open(f, encoding='utf-8').read()))
ph = ns['Phut'](json.loads((G / 'e4/phut.json').read_text(encoding='utf-8')))
bt = json.loads((G / 'bieu-thuc.json').read_text(encoding='utf-8')); ng = json.loads((G / 'nguong.json').read_text(encoding='utf-8'))['nguong']
luoi = sorted(du.luoi); lop_buoc = {t: ph.lop(t // 60 * 60) for t in luoi}
so_buoc_lop = collections.Counter(lop_buoc.values())
out = {'so_buoc_theo_lop': dict(so_buoc_lop), 'luat': {}}
for L in bt['luat']:
    ten = 'tin-hieu/' + L['uid']; data = du.chuoi.get(ten, {})
    th = ns['nguong_cua'](L, ng); op = L['dieu_kien']['phep']; fs = L['for_s']
    o = {'nguong': th, 'phep': op, 'so_instance': len(data), 'theo_lop': {}}
    for lop in ('khoe-x1', 'flash', 'bien'):
        bs = [t for t in luoi if lop_buoc[t] == lop]
        r = {'buoc': len(bs)}
        for k, d in sorted(data.items()):
            vals = [d[t] for t in bs if t in d]
            S = [min(d.get(u) for u in range(t - fs, t + 1, 10)) for t in bs if all(d.get(u) is not None for u in range(t - fs, t + 1, 10))]
            rr = {'diem': len(vals), 'ty_le_co_diem': round(len(vals) / len(bs), 4) if bs else None}
            if vals:
                rr.update({'max_tho': max(vals), 'min_tho': min(vals), 'so_buoc_tho_vuot': sum(1 for v in vals if ns['dung'](op, v, th))})
            if S:
                rr.update({'max_duy_tri_for': max(S) if op == '>' else None, 'min_duy_tri_for': min(S) if op == '<' else None})
            r[k or '(mot-chuoi)'] = rr
        o['theo_lop'][lop] = r
    out['luat'][L['uid']] = o
for r in bt['tham_so_co_dinh']['routes']:
    for ten in (f'phu/tong-{r}', f'phu/5xx-{r}', f'phu/ty-le-loi-chua-chan-5xx-{r}'):
        d = du.chuoi.get(ten, {}).get(r, {})
        for lop in ('khoe-x1', 'flash'):
            vals = [d[t] for t in luoi if lop_buoc[t] == lop and t in d]
            out.setdefault('phu', {})[f'{ten}|{lop}'] = {'diem': len(vals), 'min': min(vals) if vals else None, 'max': max(vals) if vals else None}
(G / 'e4/giai-thich-khac.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('ok')

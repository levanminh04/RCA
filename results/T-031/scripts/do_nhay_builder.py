"""T-031 bước 3: độ nhạy builder CIRCA với hash seed (giao-thuc-v2 §6.5, §11.11) bằng mô hình đã khóa.

So lượt hash seed 1 và 2 với lượt hash seed 0 của cùng mô hình, từng ca: đổi cạnh đồ thị metric (tập cạnh vào
bước chấm = cha của từng nút), đổi cạnh gọi, đổi thứ hạng DA và RHT-only (thứ tự nút gốc và thứ hạng thực thể kèm
nhóm hòa). Chỉ so thứ hạng với nhau, không dùng nhãn, không in thứ hạng. Không chọn seed theo kết quả.

python do_nhay_builder.py <tom-tat h0> <tom-tat h1> <tom-tat h2>
"""
import hashlib
import json
import sys
from pathlib import Path

import chung


def nap(p):
    return json.loads(open(p, encoding='utf-8').read())


def thuc_the(run_dir, variant):
    """Hash thứ hạng thực thể (entity, tie_group) của biến thể từ bản ghi §13 trong thư mục lượt."""
    for p in sorted(Path(run_dir).glob('ban-ghi-*.json')):
        r = json.loads(p.read_text(encoding='utf-8'))
        if r.get('variant') == variant:
            x = [[e['entity'], e['tie_group']] for e in r['entity_ranking']]
            return hashlib.sha256(json.dumps(x).encode()).hexdigest()[:16]
    return None


def main(p0, p1, p2):
    runs = {}
    for hs, p in ((0, p0), (1, p1), (2, p2)):
        d = nap(p)
        runs[hs] = (d, {r['opaque_id']: r for r in d['luot'] if r['hashseed'] == hs}, Path(p).parent / 'luot')
    model = runs[0][0]['cau_hinh']['model']
    assert all(runs[h][0]['cau_hinh']['model'] == model for h in runs)
    ca, tong = [], {}
    for oid in sorted(runs[0][1]):
        row = {'opaque_id': oid}
        g = {h: runs[h][1].get(oid) or {} for h in runs}
        for hs in (1, 2):
            c0, c = (g[0].get('circa') or {}), (g[hs].get('circa') or {})
            b0, b = (g[0].get('bien_the') or {}), (g[hs].get('bien_the') or {})
            da, rht = f'{model}+rht_da', f'{model}+rht'
            x = {'doi_canh': c0.get('canh_hash') != c.get('canh_hash'),
                 'doi_canh_goi': c0.get('call_edges_hash') != c.get('call_edges_hash'),
                 'so_canh': [c0.get('so_canh'), c.get('so_canh')],
                 'doi_thu_tu_DA': (b0.get(da) or {}).get('thu_tu_hash') != (b.get(da) or {}).get('thu_tu_hash'),
                 'doi_thu_tu_RHT': (b0.get(rht) or {}).get('thu_tu_hash') != (b.get(rht) or {}).get('thu_tu_hash'),
                 'doi_thuc_the_DA': thuc_the(runs[0][2] / g[0]['run_id'], da) != thuc_the(runs[hs][2] / g[hs]['run_id'], da),
                 'trang_thai': {v: y['status'] for v, y in b.items()}}
            row[f'h{hs}'] = x
            for k in ('doi_canh', 'doi_canh_goi', 'doi_thu_tu_DA', 'doi_thu_tu_RHT', 'doi_thuc_the_DA'):
                tong.setdefault(f'h{hs}', {}).setdefault(k, 0)
                tong[f'h{hs}'][k] += int(x[k])
        ca.append(row)
    doc = {'mo_ta': __doc__.strip(), 'tao_luc_utc': chung.bay_gio(), 'mo_hinh': model,
           'nguon': {'h0': p0, 'h1': p1, 'h2': p2},
           'src_p3_sha256': sorted({runs[h][0]['src_p3_sha256'] for h in runs}),
           'so_ca': len(ca), 'tong_so_ca_doi': tong,
           'tong_wall_s': {f'h{h}': runs[h][0].get('tong_wall_s') for h in runs}, 'ca': ca}
    chung.ghi_json(chung.OUT / 'do-nhay-builder.json', doc)
    print(json.dumps({'mo_hinh': model, 'tong_so_ca_doi': tong}, ensure_ascii=False))


if __name__ == '__main__':
    main(*sys.argv[1:4])

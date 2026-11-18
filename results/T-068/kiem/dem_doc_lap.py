"""T-068 — kiểm độc lập file service-graph so với file ca (viết riêng, không import service_graph.py).

Dùng: py -3 -B dem_doc_lap.py <thư mục du-lieu> <thư mục service-graph> [<bản>/<ca> ...]
Không có cặp nào thì kiểm mọi cặp trong chi-muc-ban.json. In JSON tóm tắt; mã thoát 1 nếu có lệch.
"""
import json
import sys
from urllib.parse import parse_qs, urlparse
from pathlib import Path

MAU = {'tu_sinh': '#E02F44', 'ke_thua': '#FF9830', 'binh_thuong': '#8E8E8E'}
HE = {'postgresql': 'postgresql-shared-instance', 'redis': 'cache', 'mongodb': 'mongodb-instance'}
MAY = {'postgres': 'postgresql-shared-instance', 'user-db': 'mongodb-instance', 'redis': 'cache', 'rabbitmq': 'broker'}


def dich(chuoi, loai):
    if chuoi.endswith(')') and ' (' in chuoi:
        he = chuoi.rsplit(' (', 1)[1][:-1].lower()
        return HE.get(he)
    if 'SQL/cache' in loai:
        return MAY.get(chuoi)
    return None


def ky_vong(ca):
    if ca.get('trang_thai_chay') != 'OK' or not ca.get('ranking_rows'):
        return {'khong_co': True}
    chu = {}
    for t in ca['thao_tac']:
        chu[t['id']] = t['chu']
    cap = {}
    for e in ca['canh_thao_tac']:
        a, b = chu[e['source']], chu[e['target']]
        if a != b:
            n, s = cap.get((a, b), (0, 0))
            cap[(a, b)] = (n + e['so_N'], s + e['so_A'])
    ht = set()
    for t in ca['thao_tac']:
        for x in t['dich_quan_sat']:
            d = dich(x, t['loai'])
            if d and d != t['chu'] and d in (ca.get('classes') or {}) and (t['chu'], d) not in cap:
                ht.add((t['chu'], d))
    hang = {r['entity']: (r['hang'], r['lop']) for r in ca['ranking_rows']}
    nut = set(hang) | {t['chu'] for t in ca['thao_tac']} | {x for k in list(cap) + list(ht) for x in k}
    return {'khong_co': False, 'cap': cap, 'ht': ht, 'hang': hang, 'nut': nut}


def kiem(ca, g):
    k, loi = ky_vong(ca), []
    if k['khong_co']:
        if g.get('trang_thai') != 'khong_co_dau_ra' or not any(n['title'] == 'không có đầu ra' for n in g['nut']):
            loi.append('ca lỗi chạy không hiện "không có đầu ra"')
        if any(e['detail__loai'] != 'chu_thich' for e in g['canh']) or any(n['id'][:2] != '__' for n in g['nut']):
            loi.append('ca lỗi chạy có nút/cạnh dữ liệu')
        if any('viewPanel=panel-3' not in n.get('detail__url', '') for n in g['nut']):
            loi.append('nút chú thích không mở bảng trạng thái')
        loi += kiem_link(ca, g, True)
        return loi
    if {n['id'] for n in g['nut']} != k['nut']:
        loi.append('tập nút lệch')
    for n in g['nut']:
        h = k['hang'].get(n['id'])
        if h and (n['mainstat'] != f'#{h[0]}' or n['color'] != MAU[h[1]] or n['detail__lop'] != h[1]):
            loi.append(f'màu/hạng lệch {n["id"]}')
    cap = {(e['source'], e['target']): (e['detail__so_N'], e['detail__so_A']) for e in g['canh'] if e['detail__loai'] == 'span_cha_con'}
    ht = {(e['source'], e['target']) for e in g['canh'] if e['detail__loai'] == 'dich_quan_sat'}
    if cap != k['cap']:
        loi.append('cạnh liên dịch vụ hoặc số N/A lệch')
    if ht != k['ht']:
        loi.append('cạnh hạ tầng lệch')
    if any(e['mainstat'] != 'có quan sát' or e['detail__so_N'] is not None for e in g['canh'] if e['detail__loai'] == 'dich_quan_sat'):
        loi.append('cạnh hạ tầng có số')
    if any(d not in (ca.get('classes') or {}) for _, d in ht):
        loi.append('cạnh hạ tầng tới đích ngoài classes')
    loi += kiem_link(ca, g, False)
    return loi


def kiem_link(ca, g, chu_thich):
    """R1: cạnh không có link; nút dịch vụ mở đúng bản/ca/cửa sổ và var-dv = chính nút."""
    loi = []
    if any('detail__url' in e for e in g['canh']):
        loi.append('cạnh có link')
    dv = {x for x in ca.get('services') or [] if not x.startswith('__')}
    w = ca['cua_so_ms']
    for n in g['nut']:
        q = parse_qs(urlparse(n.get('detail__url', '')).query, keep_blank_values=True)
        if not q:
            if n['id'] in dv:
                loi.append(f'nút dịch vụ thiếu link {n["id"]}')
            continue
        muon = {'var-ban': [g['ban']], 'var-ca': [g['ca']], 'from': [str(w[0])], 'to': [str(w[1] - 1)]}
        if any(q.get(k) != v for k, v in muon.items()):
            loi.append(f'link sai bản/ca/cửa sổ {n["id"]}')
        if not chu_thich and q.get('var-dv') != [n['id']]:
            loi.append(f'link sai dịch vụ {n["id"]}')
    return loi


def main():
    du_lieu, sg = Path(sys.argv[1]), Path(sys.argv[2])
    cap = [tuple(x.split('/')) for x in sys.argv[3:]]
    if not cap:
        idx = json.loads((du_lieu / 'chi-muc-ban.json').read_text(encoding='utf-8'))
        cap = [(v['ban'], c) for v in idx['ban'] for c in v['cac_ca']]
    ket, tong = {}, {'cap': 0, 'ok': 0, 'khong_co_dau_ra': 0, 'canh_lien_dv': 0, 'canh_ha_tang': 0}
    for ban, c in cap:
        ca = json.loads((du_lieu / ban / f'{c}.json').read_text(encoding='utf-8'))
        g = json.loads((sg / ban / f'{c}.json').read_text(encoding='utf-8'))
        loi = kiem(ca, g)
        tong['cap'] += 1
        tong['ok'] += not loi
        tong['khong_co_dau_ra'] += g.get('trang_thai') == 'khong_co_dau_ra'
        tong['canh_lien_dv'] += sum(e['detail__loai'] == 'span_cha_con' for e in g['canh'])
        tong['canh_ha_tang'] += sum(e['detail__loai'] == 'dich_quan_sat' for e in g['canh'])
        if loi:
            ket[f'{ban}/{c}'] = loi
    print(json.dumps({'tong': tong, 'loi': ket}, ensure_ascii=False, indent=1))
    sys.exit(1 if ket else 0)


if __name__ == '__main__':
    main()

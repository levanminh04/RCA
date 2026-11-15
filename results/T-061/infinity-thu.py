"""T-061 (gói C3): thử nguồn Infinity trên Grafana 13.3.0 cục bộ với hai mẫu 0.2.

Điều kiện: container t061-grafana có plugin yesoreyeram-infinity-datasource, nguồn uid infinity-t061, thư mục mau/
gắn vào /usr/share/grafana/public/t061 (máy chủ Grafana tự gọi http://localhost:3000/public/t061/<ca>.json).
Script: (1) gửi truy vấn Infinity (parser backend, chạy phía máy chủ) qua /api/ds/query cho từng ca, đối chiếu từng
khung với JSON mẫu; (2) đổi ca A → B và kiểm bản ghi sự cố, nút, cạnh, hạng cùng đổi; (3) sinh dashboard thử có biến
`ca` (grafana/provisioning/dashboards/t061-infinity.json). Ghi kết quả ở infinity-ket-qua.json.
Cách dùng: py -3 -B infinity-thu.py
"""
import json
import sys
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
GOC = Path(__file__).resolve().parent
API = 'http://127.0.0.1:3061'
DS = {'type': 'yesoreyeram-infinity-datasource', 'uid': 'infinity-t061'}
URL = 'http://localhost:3000/public/t061/{ca}.json'

COT_NUT = [('id', 'id', 'string'), ('ten', 'title', 'string'), ('lop_m1', 'subtitle', 'string'),
           ('hien_thi.nhan_trong', 'mainstat', 'string'), ('hien_thi.nhan_phu', 'secondarystat', 'string'),
           ('hien_thi.mau', 'color', 'string'), ('noi_bat', 'highlighted', 'boolean'),
           ('vai_tro', 'detail__vai_tro', 'string'), ('hang', 'detail__hang', 'number')]
COT_CANH = [('id', 'id', 'string'), ('nguon', 'source', 'string'), ('dich', 'target', 'string'),
            ('hien_thi.nhan', 'mainstat', 'string'), ('hien_thi.mau', 'color', 'string'),
            ('nguon_goc', 'detail__nguon_goc', 'string')]
COT_HANG = [('hang', 'hang', 'number'), ('so_thuc_the', 'so_thuc_the', 'number'), ('tang', 'tang', 'number'),
            ('thuc_the', 'thuc_the', 'string')]
COT_SU_CO = [('ma', 'ma', 'string'), ('trang_thai', 'trang_thai', 'string'), ('ket_luan', 'ket_luan', 'string'),
             ('moc.t_utc', 'moc', 'string'), ('moc.mo_ta', 'mo_ta_moc', 'string')]
URL_DS = 'http://localhost:3000/public/t061/chi-muc/danh-sach-su-co.json'
COT_DS = [('ma', 'ma', 'string'), ('t_utc', 'moc', 'string'), ('trang_thai', 'trang_thai', 'string'),
          ('ket_luan', 'ket_luan', 'string'), ('nghi_nguon_hang_1', 'nghi_nguon_hang_1', 'string'),
          ('so_thuc_the_co_hang', 'so_thuc_the_co_hang', 'number')]
LINK_MO_CA = '/d/t061-infinity/t-061-thu-infinity?var-ca=${__value.raw}'


def target(ref, url, root, cot):
    return {'refId': ref, 'datasource': DS, 'type': 'json', 'source': 'url', 'parser': 'backend', 'format': 'table',
            'url': url, 'url_options': {'method': 'GET', 'data': ''}, 'root_selector': root,
            'columns': [{'selector': s, 'text': t, 'type': k} for s, t, k in cot]}


def cac_target(url):
    return [target('nodes', url, 'nut', COT_NUT), target('edges', url, 'canh', COT_CANH),
            target('xep_hang', url, 'xep_hang', COT_HANG), target('su_co', url, 'su_co', COT_SU_CO)]


def hoi(targets):
    body = json.dumps({'queries': targets, 'from': 'now-1h', 'to': 'now'}).encode()
    req = urllib.request.Request(API + '/api/ds/query', body, {'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def cot(frame, ten):
    names = [f['name'] for f in frame['schema']['fields']]
    return frame['data']['values'][names.index(ten)] if ten in names else None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    kq, chi_tiet = [], {}

    def ghi(ten, dat, ct=None):
        kq.append({'phep_kiem': ten, 'dat': bool(dat), 'chi_tiet': ct})

    du_lieu = {}
    for ca in ('c12e47ab', 'f4a8c021'):
        mau = json.load(open(GOC / 'mau' / f'{ca}.json', encoding='utf-8'))
        r = hoi(cac_target(URL.format(ca=ca)))
        loi = {k: v.get('error') for k, v in r['results'].items() if v.get('error')}
        ghi(f'{ca}: bốn truy vấn Infinity không lỗi', not loi, loi or None)
        fr = {k: v['frames'][0] for k, v in r['results'].items() if v.get('frames')}
        du_lieu[ca] = fr
        if 'nodes' not in fr or 'edges' not in fr:
            continue
        n, e = fr['nodes'], fr['edges']
        chi_tiet[ca] = {k: [f['name'] + ':' + f['type'] for f in v['schema']['fields']] for k, v in fr.items()}
        ghi(f'{ca}: khung nodes đúng id, title, color, highlighted, mainstat theo thứ tự mẫu',
            cot(n, 'id') == [x['id'] for x in mau['nut']] and cot(n, 'title') == [x['ten'] for x in mau['nut']]
            and cot(n, 'color') == [x['hien_thi']['mau'] for x in mau['nut']]
            and cot(n, 'highlighted') == [x['noi_bat'] for x in mau['nut']]
            and cot(n, 'mainstat') == [x['hien_thi']['nhan_trong'] for x in mau['nut']])
        ghi(f'{ca}: hạng trong khung nodes giữ null cho thực thể không có hạng',
            cot(n, 'detail__hang') == [x['hang'] for x in mau['nut']], cot(n, 'detail__hang'))
        ghi(f'{ca}: khung edges đúng id, source, target, color',
            cot(e, 'source') == [x['nguon'] for x in mau['canh']] and cot(e, 'target') == [x['dich'] for x in mau['canh']]
            and cot(e, 'id') == [x['id'] for x in mau['canh']] and cot(e, 'color') == [x['hien_thi']['mau'] for x in mau['canh']])
        ghi(f'{ca}: khung hạng đúng số khối và cỡ khối',
            cot(fr.get('xep_hang', {'schema': {'fields': []}, 'data': {'values': []}}), 'so_thuc_the')
            == [x['so_thuc_the'] for x in mau['xep_hang']])
        ghi(f'{ca}: bản ghi sự cố đúng mã, trạng thái, kết luận, mốc',
            cot(fr['su_co'], 'ma') == [mau['su_co']['ma']] and cot(fr['su_co'], 'ket_luan') == [mau['su_co']['ket_luan']]
            and cot(fr['su_co'], 'trang_thai') == [mau['su_co']['trang_thai']]
            and cot(fr['su_co'], 'moc') == [mau['su_co']['moc']['t_utc']])
    # danh sách sự cố từ file chỉ mục
    ds = json.load(open(GOC / 'mau' / 'chi-muc' / 'danh-sach-su-co.json', encoding='utf-8'))['su_co']
    r = hoi([target('ds', URL_DS, 'su_co', COT_DS)])
    loi = r['results']['ds'].get('error')
    ghi('danh sách sự cố: truy vấn Infinity trên file chỉ mục không lỗi', not loi, loi)
    if not loi:
        f = r['results']['ds']['frames'][0]
        ghi('danh sách sự cố: đúng số dòng, thứ tự mới nhất trước, mã/trạng thái/kết luận/nút nghi nguồn khớp chỉ mục',
            cot(f, 'ma') == [x['ma'] for x in ds] and cot(f, 'ket_luan') == [x['ket_luan'] for x in ds]
            and cot(f, 'trang_thai') == [x['trang_thai'] for x in ds]
            and cot(f, 'nghi_nguon_hang_1') == [x['nghi_nguon_hang_1'] for x in ds],
            {'ma': cot(f, 'ma'), 'nghi_nguon_hang_1': cot(f, 'nghi_nguon_hang_1')})
    a, b = du_lieu.get('c12e47ab', {}), du_lieu.get('f4a8c021', {})
    if a and b:
        ghi('đổi ca A → B: bản ghi sự cố, nút (màu/nổi bật), cạnh, hạng đều đổi theo ca',
            cot(a['su_co'], 'ma') != cot(b['su_co'], 'ma') and cot(a['nodes'], 'color') != cot(b['nodes'], 'color')
            and cot(a['nodes'], 'highlighted') != cot(b['nodes'], 'highlighted')
            and cot(a['xep_hang'], 'so_thuc_the') != cot(b['xep_hang'], 'so_thuc_the'),
            {'A': cot(a['su_co'], 'ket_luan'), 'B': cot(b['su_co'], 'ket_luan')})

    # dashboard thử có biến ca
    url_bien = URL.replace('{ca}', '${ca}')
    tg = cac_target(url_bien)
    dash = {'uid': 't061-infinity', 'title': 'T-061 thử Infinity', 'schemaVersion': 41, 'editable': True,
            'time': {'from': 'now-1h', 'to': 'now'},
            'templating': {'list': [{'name': 'ca', 'type': 'custom', 'query': 'c12e47ab,f4a8c021',
                                     'current': {'text': 'c12e47ab', 'value': 'c12e47ab'},
                                     'options': [{'text': x, 'value': x, 'selected': x == 'c12e47ab'}
                                                 for x in ('c12e47ab', 'f4a8c021')]}]},
            'panels': [
                {'id': 4, 'type': 'table', 'title': 'Danh sách sự cố (click mã để mở)', 'datasource': DS,
                 'targets': [target('ds', URL_DS, 'su_co', COT_DS)], 'gridPos': {'h': 5, 'w': 24, 'x': 0, 'y': 0},
                 'fieldConfig': {'defaults': {}, 'overrides': [
                     {'matcher': {'id': 'byName', 'options': 'ma'},
                      'properties': [{'id': 'links', 'value': [{'title': 'Mở sự cố', 'url': LINK_MO_CA}]}]}]}},
                {'id': 1, 'type': 'table', 'title': 'Sự cố ${ca}', 'datasource': DS, 'targets': [tg[3]],
                 'gridPos': {'h': 4, 'w': 24, 'x': 0, 'y': 5}},
                {'id': 2, 'type': 'nodeGraph', 'title': 'Đồ thị ${ca}', 'datasource': DS, 'targets': tg[:2],
                 'gridPos': {'h': 16, 'w': 16, 'x': 0, 'y': 9}},
                {'id': 3, 'type': 'table', 'title': 'Xếp hạng ${ca}', 'datasource': DS, 'targets': [tg[2]],
                 'gridPos': {'h': 16, 'w': 8, 'x': 16, 'y': 9}}]}
    (GOC / 'grafana/provisioning/dashboards/t061-infinity.json').write_text(
        json.dumps(dash, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (GOC / 'infinity-ket-qua.json').write_text(json.dumps(
        {'plugin': 'yesoreyeram-infinity-datasource', 'grafana': '13.3.0', 'url_mau': URL, 'parser': 'backend',
         'so_phep_kiem': len(kq), 'so_hong': sum(not x['dat'] for x in kq), 'ket_qua': kq, 'truong_khung': chi_tiet},
        ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for x in kq:
        print(('ĐẠT ' if x['dat'] else 'HỎNG') + ' ' + x['phep_kiem'] + ('' if x['dat'] else f"  {x['chi_tiet']}"))
    return 0 if all(x['dat'] for x in kq) else 1


if __name__ == '__main__':
    sys.exit(main())

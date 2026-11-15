"""T-061: dựng hai khung `nodes`, `edges` cho panel Node graph từ ĐỊNH DẠNG (mau/*.json), không đọc M1.

Mục đích: kiểm định dạng đủ cho Node graph. Khung ghi theo DataFrameJSON để nạp vào TestData (kịch bản Raw frames).
Sinh luôn provisioning (nguồn TestData, một dashboard) cho Grafana cục bộ.

Cách dùng: py -3 khung-grafana.py  (chạy trong results/T-061)
"""
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent
MAU = GOC / 'mau'
RA = GOC / 'grafana'


def truong(ten, kieu, gia_tri, ten_hien=None):
    f = {'name': ten, 'type': kieu}
    if ten_hien:
        f['config'] = {'displayName': ten_hien}
    return f, gia_tri


def khung(ten, cac_truong):
    return {'schema': {'name': ten, 'refId': ten, 'meta': {'preferredVisualisationType': 'nodeGraph'},
                       'fields': [f for f, _ in cac_truong]},
            'data': {'values': [v for _, v in cac_truong]}}


def dung(kq):
    nut = kq['nut']
    bc = {b['id']: b for b in kq['bang_chung']}

    def mo_ta_bc(ids):
        return '; '.join(f"{bc[i]['kenh']} {bc[i]['huong']} ({bc[i]['don_vi']})" for i in ids) or '—'

    def vung(n):
        if not kq['vung']['ap_dung']:
            return 'không áp dụng'
        nhan = []
        if n['goc_vung']:
            nhan.append('gốc')
        if n['trong_vung_cach_1']:
            nhan.append('cách 1')
        if n['trong_vung_cach_2']:
            nhan.append('cách 2')
        return ', '.join(nhan) or 'ngoài vùng'

    def hang(n):
        if n['hang'] is None:
            return 'không có hạng'
        return f"{n['hang']}" + (f" (đồng hạng {n['so_dong_hang']})" if n['so_dong_hang'] > 1 else '')

    ds = [
        truong('id', 'string', [n['id'] for n in nut]),
        truong('title', 'string', [n['ten'] for n in nut]),
        truong('subtitle', 'string', [n['lop_m1'] or '' for n in nut]),
        truong('mainstat', 'string', [n['hien_thi']['nhan_trong'] for n in nut]),
        truong('secondarystat', 'string', [n['hien_thi']['nhan_phu'] for n in nut]),
        truong('color', 'string', [n['hien_thi']['mau'] for n in nut]),
        truong('highlighted', 'boolean', [n['noi_bat'] for n in nut]),
        truong('detail__vai_tro', 'string', [n['vai_tro'] for n in nut], 'Vai trò (M1)'),
        truong('detail__hang', 'string', [hang(n) for n in nut], 'Hạng'),
        truong('detail__vung', 'string', [vung(n) for n in nut], 'Vùng nghi ngờ'),
        truong('detail__bang_chung', 'string', [mo_ta_bc(n['bang_chung']) for n in nut], 'Bằng chứng'),
    ]
    pl = kq.get('phat_lai')
    if pl:
        ds.append(truong('detail__dap_an', 'string',
                         ['ĐÁP ÁN (phát lại): thành phần được tiêm' if n['id'] == pl['thanh_phan_tiem'] else ''
                          for n in nut], 'Đáp án (phát lại)'))
    canh = kq['canh']
    dc = [
        truong('id', 'string', [c['id'] for c in canh]),
        truong('source', 'string', [c['nguon'] for c in canh]),
        truong('target', 'string', [c['dich'] for c in canh]),
        truong('mainstat', 'string', [c['hien_thi']['nhan'] for c in canh]),
        truong('color', 'string', [c['hien_thi']['mau'] for c in canh]),
        truong('detail__chieu', 'string', ['bên gọi → bên được gọi'] * len(canh), 'Chiều'),
        truong('detail__nguon_goc', 'string', [c['nguon_goc'] for c in canh], 'Nguồn cạnh'),
    ]
    return [khung('nodes', ds), khung('edges', dc)]


def panel_graph(pid, tieu_de, frames, x, y):
    return {'id': pid, 'type': 'nodeGraph', 'title': tieu_de, 'gridPos': {'h': 14, 'w': 12, 'x': x, 'y': y},
            'datasource': {'type': 'grafana-testdata-datasource', 'uid': 'testdata-t061'},
            'targets': [{'refId': 'A', 'scenarioId': 'raw_frame',
                         'datasource': {'type': 'grafana-testdata-datasource', 'uid': 'testdata-t061'},
                         'rawFrameContent': json.dumps(frames, ensure_ascii=False)}]}


def panel_chu(pid, kq, x, y):
    sc = kq['su_co']
    dong = [f"**Sự cố {sc['ma']}** · chế độ {sc['che_do']} · trạng thái M1 `{sc['trang_thai']}`",
            f"Mốc {sc['moc']['t_utc']} — {sc['moc']['mo_ta']}",
            f"Kết luận M1: `{sc['ket_luan'] or '—'}` — {sc['ket_luan_hien_thi']}"]
    if sc.get('loi'):
        dong.append(f"Lỗi: {sc['loi']}")
    dong += [
            f"Quan sát {kq['do_phu']['so_quan_sat']}, trả hạng {kq['do_phu']['so_tra_hang']}; "
            f"thiếu kênh hợp lệ: {', '.join(kq['do_phu']['thieu_kenh_hop_le']) or 'không'}",
            f"Nguồn: {kq['nguon']['method_version']} / {kq['nguon']['config_id']} / sha256 {kq['nguon']['sha256_m1'][:12]}…"]
    if kq.get('phat_lai'):
        dong.append(f"**Phát lại:** {kq['phat_lai']['nhan_xet']}")
    return {'id': pid, 'type': 'text', 'title': f"Sự cố {sc['ma']}", 'gridPos': {'h': 5, 'w': 12, 'x': x, 'y': y},
            'options': {'mode': 'markdown', 'content': '\n\n'.join(dong)}}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    (RA / 'frames').mkdir(parents=True, exist_ok=True)
    ca = [('c12e47ab.json', 'Ca c12e47ab'), ('f4a8c021.json', 'Ca f4a8c021'),
          ('f4a8c021.phat-lai.json', 'Ca f4a8c021 — bản phát lại'), ('c12e47ab.phat-lai.json', 'Ca c12e47ab — bản phát lại')]
    panels, pid = [], 1
    for i, (ten, td) in enumerate(ca):
        kq = json.load(open(MAU / ten, encoding='utf-8'))
        frames = dung(kq)
        (RA / 'frames' / ten).write_text(json.dumps(frames, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        x, y = (i % 2) * 12, (i // 2) * 19
        panels.append(panel_chu(pid, kq, x, y)); pid += 1
        panels.append(panel_graph(pid, td, frames, x, y + 5)); pid += 1
    dash = {'uid': 't061-mau', 'title': 'T-061 mẫu kết quả RCA', 'schemaVersion': 41, 'editable': True,
            'time': {'from': 'now-1h', 'to': 'now'}, 'panels': panels}
    p = RA / 'provisioning'
    (p / 'dashboards').mkdir(parents=True, exist_ok=True)
    (p / 'datasources').mkdir(parents=True, exist_ok=True)
    (p / 'dashboards' / 't061.json').write_text(json.dumps(dash, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (p / 'dashboards' / 'provider.yaml').write_text(
        'apiVersion: 1\nproviders:\n  - name: t061\n    type: file\n    options:\n      path: /etc/grafana/provisioning/dashboards\n',
        encoding='utf-8')
    (p / 'datasources' / 'testdata.yaml').write_text(
        'apiVersion: 1\ndatasources:\n  - name: TestData\n    type: grafana-testdata-datasource\n    uid: testdata-t061\n    access: proxy\n',
        encoding='utf-8')
    print('đã ghi', len(panels), 'panel')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""T-072 — đọc thẳng đầu ra của T-071 sang định dạng `cham_offline.py` đọc. Không sửa file nào của T-071.

  xuat  <thư mục xuat_chuoi.py của một lượt> [<thư mục> ...] --ra-thu-muc <dir>
        → mỗi lượt một file `<tên thư mục>.t072.json` dạng T072-xuat-1 {cua_so, step_s, loi_khuc, chuoi}
  phut  <đầu ra phan_loai_phut.py> --ra <file>
        → {khoang: [[phút, phút + 60, lớp]], ...}; lớp = nhãn T-071 đổi '_' → '-' (khoe_x1 → khoe-x1)
  doi-chieu-phut <đầu ra phan_loai_phut.py> <file phut đã chuyển>   (đếm phút theo lớp trước/sau; thoát 1 nếu lệch)

Giữ nguyên mốc thời gian (chỉ đổi số thực nguyên → số nguyên; mốc không nguyên → dừng), nhãn chuỗi, giá trị (chuỗi
nguyên văn của Prometheus) và khúc lỗi. Chỉ chuyển chuỗi `tin-hieu/*` và `phu/*` (query_range); mẫu thô `tho/*` không
dùng cho chấm, để nguyên ở T-071.

Khúc của xuat_chuoi.py: query_range [a_k, b_k − step]; khúc lỗi ghi [a_k, b_k] (ISO) → loi_khuc {ten, start a_k,
end b_k − step}. Cửa sổ lưới: [bat_dau, mốc lưới cuối ≤ ket_thuc − step].
"""
import argparse, collections, datetime as dt, gzip, hashlib, json, pathlib, sys

STEP = 10


def ep(s):
    return int(dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp())


def nguyen(ts):
    f = float(ts)
    if f != int(f):
        raise SystemExit(f'mốc không nguyên giây: {ts}')
    return int(f)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def xuat(thu_muc, ra_dir):
    d = pathlib.Path(thu_muc)
    tom = json.loads((d / 'tom-tat.json').read_text(encoding='utf-8'))
    t0, t1 = ep(tom['bat_dau']), ep(tom['ket_thuc'])
    if t0 % STEP:
        raise SystemExit('bat_dau không canh 10 s')
    cuoi = t0 + ((t1 - STEP - t0) // STEP) * STEP
    doc = {'phien_ban': 'T072-xuat-1', 'nguon': {'thu_muc': str(d), 'tom_tat_sha256': sha(d / 'tom-tat.json'),
                                                'bieu_thuc_sha256': tom.get('bieu_thuc_sha256'), 'file': {}},
           'cua_so': [t0, cuoi], 'step_s': STEP, 'loi_khuc': [], 'chuoi': {}}
    so = {}
    for ten, c in tom['chuoi'].items():
        if not (ten.startswith('tin-hieu/') or ten.startswith('phu/')):
            continue
        if c.get('loai') != 'range':
            raise SystemExit(f'{ten}: không phải query_range')
        f = d / c['file']
        doc['nguon']['file'][ten] = sha(f)
        with gzip.open(f, 'rt', encoding='utf-8') as g:
            x = json.load(g)
        if x['ten'] != ten or int(x.get('step_s') or STEP) != STEP:
            raise SystemExit(f'{ten}: tên hoặc step lệch')
        doc['chuoi'][ten] = [{'metric': s['metric'], 'values': [[nguyen(t), v] for t, v in s['values']]} for s in x['result']]
        so[ten] = sum(len(s['values']) for s in x['result'])
        for lk in c.get('khuc_loi', []):
            a, b = ep(lk['khuc'][0]), ep(lk['khuc'][1])
            doc['loi_khuc'].append({'ten': ten, 'start': a, 'end': b - STEP, 'loi': lk.get('loi')})
        if so[ten] != c.get('so_diem', so[ten]):
            raise SystemExit(f'{ten}: số điểm {so[ten]} khác tom-tat {c.get("so_diem")}')
    ra = pathlib.Path(ra_dir) / (d.name + '.t072.json')
    ra.write_text(json.dumps(doc, separators=(',', ':')) + '\n', encoding='utf-8')
    return {'ra': str(ra), 'cua_so': doc['cua_so'], 'so_chuoi': len(so), 'so_diem': sum(so.values()), 'loi_khuc': len(doc['loi_khuc'])}


def lop(n):
    return n.replace('_', '-')


def phut(src, ra):
    k = json.loads(pathlib.Path(src).read_text(encoding='utf-8'))
    kh = []
    for r in k['phut']:
        m = ep(r['phut'])
        if m % 60:
            raise SystemExit(f'phút không tròn: {r["phut"]}')
        kh.append([m, m + 60, lop(r['nhan'])])
    out = {'phien_ban': 'T072-phut-1', 'nguon': {'file': str(src), 'sha256': sha(src),
                                                'khai_truoc_sha256': k.get('tom_tat', {}).get('khai_truoc_sha256')},
           'anh_xa_nhan': 'nhãn T-071 đổi "_" thành "-"; khoe_x1 → khoe-x1 (lớp mẫu số của cham_offline.py)',
           'khoang': kh}
    pathlib.Path(ra).write_text(json.dumps(out, ensure_ascii=False) + '\n', encoding='utf-8')
    return doi_chieu(src, ra)


def doi_chieu(src, ra):
    k = json.loads(pathlib.Path(src).read_text(encoding='utf-8'))
    o = json.loads(pathlib.Path(ra).read_text(encoding='utf-8'))
    truoc = collections.Counter(lop(r['nhan']) for r in k['phut'])
    sau = collections.Counter(x[2] for x in o['khoang'])
    phut_trung = len(o['khoang']) - len({x[0] for x in o['khoang']})
    kq = {'truoc': dict(truoc), 'sau': dict(sau), 'khoe_x1_tom_tat_T071': k.get('tom_tat', {}).get('khoe_x1_phut'),
          'phut_trung': phut_trung, 'khop': truoc == sau and phut_trung == 0 and
          (k.get('tom_tat', {}).get('khoe_x1_phut') in (None, sau.get('khoe-x1', 0)))}
    return kq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lenh', choices=['xuat', 'phut', 'doi-chieu-phut'])
    ap.add_argument('vao', nargs='+')
    ap.add_argument('--ra')
    ap.add_argument('--ra-thu-muc')
    a = ap.parse_args()
    if a.lenh == 'xuat':
        kq = [xuat(x, a.ra_thu_muc) for x in a.vao]
        ok = True
    elif a.lenh == 'phut':
        kq = phut(a.vao[0], a.ra)
        ok = kq['khop']
    else:
        kq = doi_chieu(a.vao[0], a.vao[1])
        ok = kq['khop']
    sys.stdout.buffer.write((json.dumps(kq, ensure_ascii=False) + '\n').encode('utf-8'))
    sys.exit(0 if ok else 1)


main()

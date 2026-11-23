#!/usr/bin/env python3
"""T-071 — xuất chuỗi luật W4 từ Prometheus exp-obs theo khúc (SPEC T-071 bước 4; HOP-DONG I3, I11).

Chạy trên exp-obs (Python 3 thư viện chuẩn), truy vấn http://127.0.0.1:9090. Chỉ đọc Prometheus.
Đầu vào: results/T-072/bieu-thuc.json (mục xuat_cho_T071): bat_buoc (query_range, step_s) và
khuyen_nghi_tho (mẫu thô, instant query `selector[Ks]`, giữ timestamp gốc).

Cách xuất (theo bieu-thuc.json#/xuat_cho_T071/cach_xuat):
- khoảng [bat_dau, ket_thuc] do người gọi đưa (mỗi lượt: load-start − 600 s tới hết lượt + 300 s);
- chia khúc liền nhau ≤ 600 s; query_range khúc k: start = a_k, end = a_k + 600 − step (không trùng điểm giữa khúc);
  thô: instant `selector[600s]` tại time = a_k + 600 (lấy mẫu trong (a_k, a_k + 600]);
- nghỉ NGHI giây giữa mọi truy vấn; lỗi thì thử lại tối đa 3 lần (nghỉ 2 s, 5 s), vẫn lỗi thì ghi lỗi khúc, không nội suy;
- đầu ra: mỗi chuỗi một file JSON gzip (danh sách {metric, values}), `khuc.jsonl` (một dòng/khúc/chuỗi: số điểm,
  số chuỗi nhãn, lỗi, thời gian), `mau-moi-phut.json` (số điểm theo phút UTC cho từng chuỗi và từng bộ nhãn),
  `tom-tat.json`, `SHA256SUMS`.
Dùng: python3 xuat_chuoi.py BIEU_THUC.json BAT_DAU_ISO KET_THUC_ISO THU_MUC_RA [--nghi 0.3] [--chi ten1,ten2]
"""
import argparse
import collections
import datetime as dt
import gzip
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PROM = 'http://127.0.0.1:9090'
KHUC_S = 600


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def parse(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()


def goi(duong, tham_so):
    """Một truy vấn GET; trả (data, None) hoặc (None, lỗi) sau 3 lần thử."""
    url = PROM + duong + '?' + urllib.parse.urlencode(tham_so)
    loi = None
    for i, cho in enumerate((0, 2, 5)):
        if cho:
            time.sleep(cho)
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
            if d.get('status') == 'success':
                return d['data'], None, i + 1
            loi = f"status={d.get('status')} {d.get('errorType')}: {str(d.get('error'))[:300]}"
        except urllib.error.HTTPError as e:
            loi = f'HTTP {e.code}: {e.read()[:300].decode(errors="replace")}'
        except Exception as e:  # mạng, timeout, JSON hỏng
            loi = f'{type(e).__name__}: {str(e)[:300]}'
    return None, loi, 3


def khoa(metric):
    return json.dumps(metric, sort_keys=True, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('bieu_thuc')
    ap.add_argument('bat_dau')
    ap.add_argument('ket_thuc')
    ap.add_argument('ra')
    ap.add_argument('--nghi', type=float, default=0.3)
    ap.add_argument('--chi', default='')
    a = ap.parse_args()

    raw = pathlib.Path(a.bieu_thuc).read_bytes()
    bt = json.loads(raw)['xuat_cho_T071']
    viec = [dict(x, loai='range') for x in bt['bat_buoc']]
    viec += [dict(x, loai='tho') for x in bt.get('khuyen_nghi_tho', [])]
    if a.chi:
        chon = set(a.chi.split(','))
        viec = [v for v in viec if v['ten'] in chon]

    t0 = parse(a.bat_dau)
    t1 = parse(a.ket_thuc)
    t0 = t0 - (t0 % 10)  # canh bước 10 s
    khuc = []
    a_k = t0
    while a_k < t1:
        khuc.append((a_k, min(a_k + KHUC_S, t1)))
        a_k += KHUC_S

    ra = pathlib.Path(a.ra)
    ra.mkdir(parents=True, exist_ok=False)  # không ghi đè lượt xuất cũ (luật giữ mọi lượt)
    (ra / 'chuoi').mkdir()
    nhat_ky = open(ra / 'khuc.jsonl', 'w', encoding='utf-8')
    mau_phut = {}
    tom = {'bieu_thuc': a.bieu_thuc, 'bieu_thuc_sha256': hashlib.sha256(raw).hexdigest(),
           'phien_ban_bieu_thuc': json.loads(raw).get('phien_ban'), 'bat_dau': iso(t0), 'ket_thuc': iso(t1),
           'so_khuc': len(khuc), 'khuc_s': KHUC_S, 'nghi_s': a.nghi, 'prometheus': PROM,
           'bat_dau_xuat_utc': iso(time.time()), 'chuoi': {}}

    for v in viec:
        gop = collections.OrderedDict()  # khóa nhãn -> {metric, values{ts: val}}
        loi_khuc = []
        for (ka, kb) in khuc:
            bd = time.time()
            if v['loai'] == 'range':
                step = int(v.get('step_s', 10))
                end = kb - step if kb - ka >= step else ka
                data, loi, lan = goi('/api/v1/query_range', {'query': v['promql'], 'start': ka, 'end': end, 'step': step})
            else:
                data, loi, lan = goi('/api/v1/query', {'query': f"{v['selector']}[{int(kb - ka)}s]", 'time': kb})
            so_diem = 0
            so_nhan = 0
            if data is not None:
                for s in data.get('result', []):
                    k = khoa(s['metric'])
                    o = gop.setdefault(k, {'metric': s['metric'], 'values': {}})
                    for ts, val in s.get('values', []):
                        o['values'][float(ts)] = val
                    so_diem += len(s.get('values', []))
                    so_nhan += 1
            else:
                loi_khuc.append({'khuc': [iso(ka), iso(kb)], 'loi': loi})
            nhat_ky.write(json.dumps({'ten': v['ten'], 'khuc': [iso(ka), iso(kb)], 'so_diem': so_diem,
                                      'so_bo_nhan': so_nhan, 'lan_thu': lan, 'loi': loi,
                                      'giay': round(time.time() - bd, 3)}, ensure_ascii=False) + '\n')
            nhat_ky.flush()
            time.sleep(a.nghi)
        ds = []
        phut = {}
        for k, o in gop.items():
            vals = sorted(o['values'].items())
            ds.append({'metric': o['metric'], 'values': [[ts, val] for ts, val in vals]})
            c = collections.Counter(iso(ts)[:16] for ts, _ in vals)
            phut[k] = dict(sorted(c.items()))
        ten_file = v['ten'].replace('/', '__') + '.json.gz'
        with gzip.open(ra / 'chuoi' / ten_file, 'wt', encoding='utf-8') as f:
            json.dump({'ten': v['ten'], 'loai': v['loai'], 'promql': v.get('promql') or v.get('selector'),
                       'step_s': v.get('step_s'), 'result': ds}, f, ensure_ascii=False)
        mau_phut[v['ten']] = phut
        tong = sum(len(x['values']) for x in ds)
        tom['chuoi'][v['ten']] = {'file': 'chuoi/' + ten_file, 'loai': v['loai'], 'so_bo_nhan': len(ds),
                                  'so_diem': tong, 'khuc_loi': loi_khuc}
        print(json.dumps({'ten': v['ten'], 'bo_nhan': len(ds), 'diem': tong, 'khuc_loi': len(loi_khuc)},
                         ensure_ascii=False), flush=True)
    nhat_ky.close()
    tom['xong_xuat_utc'] = iso(time.time())
    (ra / 'mau-moi-phut.json').write_text(json.dumps(mau_phut, ensure_ascii=False, indent=0), encoding='utf-8')
    (ra / 'tom-tat.json').write_text(json.dumps(tom, ensure_ascii=False, indent=1), encoding='utf-8')
    dong = []
    for p in sorted(ra.rglob('*')):
        if p.is_file() and p.name != 'SHA256SUMS':
            dong.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ra).as_posix()}')
    (ra / 'SHA256SUMS').write_text('\n'.join(dong) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())

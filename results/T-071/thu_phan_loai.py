"""T-071 — thử phan_loai_phut.py trên dữ liệu tổng hợp (không mạng). Ca: selector restarts rỗng; container mất giữa
khoảng; một đích liveness mất liên tục; restart thật → B2/suy_giam; L1 tách theo đích.
Dùng: python3 thu_phan_loai.py PHAN_LOAI_PHUT.py THU_MUC_THU (thư mục chưa tồn tại). Thoát 1 nếu có ca sai."""
import datetime as dt
import gzip
import hashlib
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
P, W = sys.argv[1], pathlib.Path(sys.argv[2])
W.mkdir()
T0 = dt.datetime(2026, 11, 20, 10, 0, tzinfo=dt.timezone.utc).timestamp()
S, F = T0 + 5.5, T0 + 606.0  # lượt ×1 600 s: 10:00:05.5 → 10:10:06
SAI = []


def ca(ten, dk, ct=''):
    if not dk:
        SAI.append(ten)
    print(('ĐẠT ' if dk else 'SAI ') + ten + ' | ' + ct)


def xuat(goc, chuoi):
    d = goc / 't-a'
    (d / 'chuoi').mkdir(parents=True)
    tom = {'chuoi': {}}
    for ten, result in chuoi.items():
        f = 'chuoi/' + ten.replace('/', '__') + '.json.gz'
        with gzip.open(d / f, 'wt', encoding='utf-8') as g:
            json.dump({'ten': ten, 'result': result}, g)
        tom['chuoi'][ten] = {'file': f, 'khuc_loi': []}
    (d / 'tom-tat.json').write_text(json.dumps(tom), encoding='utf-8')


def buoc(a, b, f):
    return [[t, str(f(t))] for t in range(int(a), int(b), 10) if f(t) is not None]


def dung(ten, restarts, live):
    e = W / ten
    (e / 'luot/t-a').mkdir(parents=True)
    iso = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    (e / 'luot/t-a/state.json').write_text(json.dumps({'StartedAt': iso(S), 'FinishedAt': iso(F), 'ExitCode': 0,
                                                       'OOMKilled': False}))
    k6 = {dt.datetime.fromtimestamp(T0 + 60 * i, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M'):
          {'diem': 300, 'journey_started': 72} for i in range(11)}
    (e / 'luot/t-a/k6-phut.json').write_text(json.dumps({'raw_sha256': 'x', 'phut': k6}))
    lo, hi = T0 - 600, F + 300
    xuat(e / 'xuat-doc-lap', {
        'doc-lap/up': [{'metric': {'job': j}, 'values': buoc(lo, hi, lambda t: 1)}
                       for j in ('prometheus', 'central-collector', 'otelcol-contrib')],
        'doc-lap/restarts': restarts(lo, hi)})
    xuat(e / 'xuat', live(lo, hi))
    kh = e / 'kh.json'
    kh.write_text(json.dumps({'luot': [{'thu_tu': 1, 'tag': 't-a', 'muc': 'x1', 'seconds': 600, 'buoc_tai': 0,
                                        'multiplier': 1}]}))
    h = hashlib.sha256(kh.read_bytes()).hexdigest()
    r = subprocess.run([sys.executable, P, str(kh), h, str(e), str(e / 'pl.json')], capture_output=True, text=True,
                       encoding='utf-8')
    if r.returncode:
        print(r.stderr[-800:])
    return {x['phut'][11:16]: x for x in json.load(open(e / 'pl.json', encoding='utf-8'))['phut']}


def live_ok(lo, hi):
    return {'tin-hieu/live-3-trang-thai': [
        {'metric': {'http_url': 'u1'}, 'values': buoc(lo, hi, lambda t: 0)},
        {'metric': {'http_url': 'u2'}, 'values': buoc(lo, hi, lambda t: 1 if T0 + 360 <= t < T0 + 420 else 0)},
        {'metric': {'http_url': 'u3'}, 'values': buoc(lo, hi, lambda t: 0 if t < T0 + 120 else None)}],
        'tho/httpcheck-status-co-ma': [{'metric': {'http_url': 'u3'}, 'values': buoc(lo, T0 + 120, lambda t: 200)}]}


# A: selector restarts rỗng
p = dung('A', lambda lo, hi: [], live_ok)
ca('A selector rỗng → mọi phút có cờ thieu_b2, nhãn không đổi',
   all(x['co']['thieu_b2'] and 'rỗng' in x['co']['thieu_b2'][0] for x in p.values()) and p['10:05']['nhan'] == 'khoe_x1',
   json.dumps(p['10:05']['co'], ensure_ascii=False))


# B: c2 mất từ 10:04; c1 restart tăng ở 10:07:30
def rs_b(lo, hi):
    return [{'metric': {'container_name': 'flash-ticket-c1', 'container_id': '1'},
             'values': buoc(lo, hi, lambda t: 1 if t >= T0 + 450 else 0)},
            {'metric': {'container_name': 'flash-ticket-c2', 'container_id': '2'},
             'values': buoc(lo, T0 + 240, lambda t: 0)},
            {'metric': {'container_name': 'rca-toxiproxy', 'container_id': '3'}, 'values': buoc(lo, hi, lambda t: 0)}]


p = dung('B', rs_b, live_ok)
ca('B phút 10:03 đủ B2 → thieu_b2 rỗng', p['10:03']['co']['thieu_b2'] == [], str(p['10:03']['co']))
ca('B container c2 mất từ 10:04 → 10:05, 10:06 cờ thieu_b2=[c2], nhãn khoe_x1',
   p['10:05']['co']['thieu_b2'] == ['flash-ticket-c2'] and p['10:06']['co']['thieu_b2'] == ['flash-ticket-c2']
   and p['10:05']['nhan'] == 'khoe_x1', f"{p['10:05']['co']} {p['10:05']['nhan']}")
ca('B c1 restart 10:07 → vi phạm B2, suy_giam', p['10:07']['vi_pham'] == ['B2'] and p['10:07']['nhan'] == 'suy_giam',
   f"{p['10:07']['vi_pham']} {p['10:07']['nhan']}")
ca('B container không phải flash-ticket-* không xét', all('rca-toxiproxy' not in x['co']['thieu_b2'] for x in p.values()))
# L1
l1 = p['10:06']['ghi_kem']['L1_theo_dich']
ca('L1 tách theo đích: u1 tốt 6, u2 lỗi 6 ở 10:06, u3 mất liên tục 6 bước không có',
   l1.get('u1') == {'0': 6, 'khong_co_buoc': 0} and l1.get('u2') == {'1': 6, 'khong_co_buoc': 0}
   and l1.get('u3') == {'khong_co_buoc': 6}, json.dumps(l1))
ca('L1 không đổi nhãn (10:06 có u2 dò lỗi, u3 mất dò vẫn khoe_x1)', p['10:06']['nhan'] == 'khoe_x1', p['10:06']['nhan'])
ca('L1 phút 10:01 u3 còn dò', p['10:01']['ghi_kem']['L1_theo_dich'].get('u3') == {'0': 6, 'khong_co_buoc': 0},
   json.dumps(p['10:01']['ghi_kem']['L1_theo_dich']))
ca('biên: 10:00 (StartedAt), 10:01 (2 phút đầu), 10:10 (FinishedAt) là bien',
   [p[k]['nhan'] for k in ('10:00', '10:01', '10:10')] == ['bien', 'bien', 'bien'])
print('TONG', 'ĐẠT' if not SAI else 'SAI: ' + ', '.join(SAI))
sys.exit(1 if SAI else 0)

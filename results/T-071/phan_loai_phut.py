#!/usr/bin/env python3
"""T-071 — phân loại từng phút UTC của một khoảng tải nền theo bản khai trước đã khóa (offline, chỉ đọc file đã xuất).

Dùng: python3 phan_loai_phut.py KHAI_TRUOC.json SHA256_KHOA THU_MUC_E2 RA.json
THU_MUC_E2 có:
  luot/<tag>/{state.json, run.json, k6-phut.json}        (k6-phut.json do k6_phut.py sinh từ raw.json)
  xuat/<tag>/        đầu ra xuat_chuoi.py với results/T-072/bieu-thuc.json (chuỗi luật: chỉ ghi kèm)
  xuat-doc-lap/<tag>/ đầu ra xuat_chuoi.py với results/T-071/chuoi-phan-loai.json (chuỗi độc lập: dùng phân loại)

Quy tắc lấy nguyên từ bản khóa (phan_loai_phut, tieu_chi_khoe_moi_phut, nguyen_tac_doc_lap). Thứ tự nhãn:
mat_quan_sat > bien > quota > flash > suy_giam > khoe_x1. Chuỗi luật và L1 không đổi nhãn; chỉ ghi kèm.
Chi tiết cài đặt không có trong bản khóa (ghi rõ ở đầu ra `cai_dat`):
  - "thiếu mẫu up": trong phút không có mẫu nào của job, hoặc có khoảng giữa hai mẫu liên tiếp > 2,5 × trung vị
    nhịp của job giao phút; job không có chuỗi nào trong cửa sổ → mọi phút mat_quan_sat.
  - tăng của bộ đếm trong phút = giá trị mẫu cuối ≤ m+60 trừ giá trị mẫu cuối ≤ m (chuỗi mới xuất hiện trong phút:
    trừ 0); giảm = reset (Collector) / khởi động lại.
  - B2 xét container có `container_name` bắt đầu bằng `flash-ticket-`; danh sách áp dụng = mọi tên như vậy có chuỗi ở
    bất kỳ đâu trong khoảng xuất; tên áp dụng không có mẫu trong phút (gồm container đã mất) → cờ thieu_b2; selector
    rỗng → mọi phút cờ thieu_b2. OOM không có chuỗi Prometheus riêng nên B2 chỉ đo restart (OOM của container k6 ở
    state.json kiểm riêng mỗi lượt). B2 thiếu chỉ gắn cờ, không đổi nhãn.
  - L1 ghi kèm theo từng đích http_url (đếm bước trạng thái 0/1/2 và bước không có giá trị), không gộp.
  - cảnh báo trong phút (`canh_bao`) để trống: T-072 điền bằng chấm offline trên chuỗi đã xuất.
"""
import collections
import datetime as dt
import gzip
import hashlib
import json
import pathlib
import re
import statistics
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
KHAI, H, E2, RA = sys.argv[1:5]
raw = pathlib.Path(KHAI).read_bytes()
if hashlib.sha256(raw).hexdigest() != H:
    raise SystemExit('bản khai trước không khớp sha256 khóa')
K = json.loads(raw)
E2 = pathlib.Path(E2)
JOB_UP = ['prometheus', 'central-collector', 'otelcol-contrib']
K5_X1, K5_X3, QUOTA = 65, 195, 0.2
NHAN_THU_TU = ['mat_quan_sat', 'bien', 'quota', 'flash', 'suy_giam', 'khoe_x1']


def ts_docker(s):
    m = re.fullmatch(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(\.\d+)?Z', s)
    return dt.datetime.fromisoformat(m.group(1) + '+00:00').timestamp() + (float('0' + m.group(2)) if m.group(2) else 0)


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


# ---- lượt ----
luot = []
for l in K['luot']:
    d = E2 / 'luot' / l['tag']
    st = json.load(open(d / 'state.json'))
    k6 = json.load(open(d / 'k6-phut.json'))
    luot.append(dict(l, S=ts_docker(st['StartedAt']), F=ts_docker(st['FinishedAt']), exit=st['ExitCode'],
                     oom=st['OOMKilled'], k6=k6['phut'], raw_sha256=k6['raw_sha256']))


# ---- chuỗi đã xuất (gộp các lượt, bỏ trùng theo nhãn + timestamp) ----
def doc_xuat(goc):
    chuoi = collections.defaultdict(dict)  # ten -> {khoa_nhan: {ts: val}}
    loi_khuc = []
    for d in sorted((E2 / goc).iterdir()):
        tom = json.load(open(d / 'tom-tat.json', encoding='utf-8'))
        for ten, m in tom['chuoi'].items():
            for x in m['khuc_loi']:
                loi_khuc.append({'ten': ten, 'khuc': x['khuc'], 'loi': x['loi'], 'xuat': d.name})
            r = json.load(gzip.open(d / m['file'], 'rt', encoding='utf-8'))
            for s in r['result']:
                k = json.dumps(s['metric'], sort_keys=True)
                chuoi[ten].setdefault(k, {}).update({float(t): float(v) for t, v in s['values']})
    return chuoi, loi_khuc


luat, loi_luat = doc_xuat('xuat')
dl, loi_dl = doc_xuat('xuat-doc-lap')


def mau(ten, kn):
    return sorted(dl.get(ten, {}).get(kn, {}).items())


def tang(vals, a, b):
    """tăng của bộ đếm trong (a, b]; None nếu không có mẫu ≤ b."""
    sau = [v for t, v in vals if t <= b]
    if not sau:
        return None
    truoc = [v for t, v in vals if t <= a]
    return sau[-1] - (truoc[-1] if truoc else 0.0)


# ---- phạm vi phút ----
m0 = int(min(l['S'] for l in luot) // 60) * 60
m1 = int(max(l['F'] for l in luot) // 60) * 60
phut = list(range(m0, m1 + 60, 60))
lt_cua = lambda m: [l for l in luot if m < l['F'] and m + 60 > l['S']]
cai_dat_note = []

# up: nhịp trung vị từng job
up = {}
for kn, vals in dl.get('doc-lap/up', {}).items():
    job = json.loads(kn).get('job')
    up.setdefault(job, []).extend(sorted(vals.items()))
nhip = {j: statistics.median([b[0] - a[0] for a, b in zip(v, v[1:])]) for j, v in up.items() if len(v) > 2}
cai_dat_note.append({'up_jobs_co_chuoi': sorted(up), 'nhip_trung_vi_s': nhip})

# B2: danh sách container áp dụng = mọi container_name `flash-ticket-*` có chuỗi restarts ở bất kỳ đâu trong khoảng
# xuất (gộp các container_id của cùng tên). Phút nào một tên áp dụng không có mẫu → cờ thieu_b2 (kể cả khi container
# mất hẳn trước phút đó). Selector rỗng → mọi phút cờ thieu_b2. Chỉ gắn cờ, không đổi nhãn (bản khóa B2).
b2 = collections.defaultdict(list)  # container_name -> [danh sách mẫu đã sắp của từng chuỗi]
for kn, vals in dl.get('doc-lap/restarts', {}).items():
    ten = json.loads(kn).get('container_name', '')
    if ten.startswith('flash-ticket-'):
        b2[ten].append(sorted(vals.items()))
B2_AP_DUNG = sorted(b2)
cai_dat_note.append({'b2_container_ap_dung': B2_AP_DUNG,
                     'b2_selector_rong': not dl.get('doc-lap/restarts')})

# L1 (chỉ ghi kèm): đếm theo từng đích http_url; tập đích = mọi http_url thấy trong live-3-trang-thai hoặc mẫu thô
# httpcheck_status có mã. Bước không có giá trị của một đích trong phút → 'khong_co_buoc' (bieu-thuc coi như trạng thái 2).
L1_DICH = sorted({json.loads(kn).get('http_url') for ten in ('tin-hieu/live-3-trang-thai', 'tho/httpcheck-status-co-ma')
                  for kn in luat.get(ten, {})} - {None})
BUOC_PHUT = 6  # bước 10 s mỗi phút (bieu-thuc step_s = 10)
cai_dat_note.append({'l1_dich': L1_DICH})

ket = []
for m in phut:
    a, b = m, m + 60
    ly = collections.defaultdict(list)
    gia_tri = {}
    co = {}
    ls = lt_cua(m)
    l = ls[0] if len(ls) == 1 else None
    # --- mat_quan_sat ---
    for j in JOB_UP:
        v = up.get(j, [])
        trong = [x for x in v if a <= x[0] < b]
        if not v:
            ly['mat_quan_sat'].append(f'up {j}: không có chuỗi')
            continue
        if not trong:
            ly['mat_quan_sat'].append(f'up {j}: không có mẫu trong phút')
        if any(x[1] == 0 for x in trong):
            ly['mat_quan_sat'].append(f'up {j} = 0')
        nh = nhip.get(j)
        if nh and any(t2 - t1 > 2.5 * nh and t1 < b and t2 > a for (t1, _), (t2, _) in zip(v, v[1:])):
            ly['mat_quan_sat'].append(f'up {j}: khoảng hở > 2,5 × nhịp')
    for kn, vals in dl.get('doc-lap/prom-start', {}).items():
        v = sorted(vals.items())
        if any(v2 != v1 and a <= t2 < b for (t1, v1), (t2, v2) in zip(v, v[1:])):
            ly['mat_quan_sat'].append('Prometheus khởi động lại')
    for kn, vals in dl.get('doc-lap/otel-uptime', {}).items():
        v = sorted(vals.items())
        if any(v2 < v1 and a <= t2 < b for (t1, v1), (t2, v2) in zip(v, v[1:])):
            ly['mat_quan_sat'].append('Collector uptime reset ' + json.loads(kn).get('job', ''))
    for kn, vals in dl.get('doc-lap/otel-loi', {}).items():
        d_ = tang(sorted(vals.items()), a, b)
        if d_ and d_ > 0:
            ly['mat_quan_sat'].append('Collector lỗi ' + json.loads(kn).get('__name__', '') + f' +{d_:g}')
    for x in loi_dl + loi_luat:
        # khúc lỗi: tên khúc ISO [a, b]
        ka, kb = [dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp() for s in x['khuc']]
        if ka < b and kb > a:
            ly['mat_quan_sat'].append('khúc xuất lỗi: ' + x['ten'])
    k6 = (l['k6'].get(iso(m)[:16]) if l else None) or {}
    if l and not k6.get('diem'):
        ly['mat_quan_sat'].append('k6 không có điểm trong phút')
    # --- bien ---
    if not ls:
        ly['bien'].append('ngoài lượt (giữa hai lượt)')
    elif len(ls) > 1:
        ly['bien'].append('giao hai lượt')
    else:
        S, F = l['S'], l['F']
        if a <= S < b: ly['bien'].append('chứa StartedAt')
        if a <= F < b: ly['bien'].append('chứa FinishedAt')
        if l.get('buoc_tai') and a <= S + l['buoc_tai'] < b: ly['bien'].append('chứa bậc 600 s')
        if a < S + 120 and b > S: ly['bien'].append('2 phút đầu')
        if a < F and b > S + l['seconds'] + 1e-9 and S + l['seconds'] < F: ly['bien'].append('gracefulStop')
    # --- mức tải ---
    muc = None
    if l:
        muc = 'x3' if (l.get('buoc_tai') and a >= l['S'] + l['buoc_tai']) else 'x1'
    # --- K, B2 ---
    vi = []
    if l:
        if k6.get('journey_failed'): vi.append('K1')
        if k6.get('dropped_iterations'): vi.append('K2')
        if k6.get('http_429'): vi.append('K3')
        if k6.get('http_req_failed'): vi.append('K4')
        if k6.get('journey_started', 0) < (K5_X3 if muc == 'x3' else K5_X1): vi.append('K5')
    gia_tri['k6'] = {x: k6.get(x, 0) for x in ('journey_started', 'journey_finished', 'journey_failed',
                                               'dropped_iterations', 'http_429', 'http_req_failed', 'http_reqs', 'diem')}
    rs = []
    thieu_b2 = []
    if not B2_AP_DUNG:
        thieu_b2.append('(selector container_restarts_total rỗng: không có container flash-ticket-* nào)')
    for ten in B2_AP_DUNG:
        if not any(a <= t < b for v in b2[ten] for t, _ in v):
            thieu_b2.append(ten)  # không quan sát được trong phút (gồm container đã mất trước phút)
        if any((tang(v, a, b) or 0) > 0 for v in b2[ten]):
            rs.append(ten)
    if rs:
        vi.append('B2')
    gia_tri['b2_restart'] = rs
    co['thieu_b2'] = thieu_b2
    th = {json.loads(kn).get('__name__'): sorted(vals.items()) for kn, vals in dl.get('doc-lap/throttle-booking', {}).items()}
    dt_ = tang(th.get('container_cpu_throttling_data_throttled_periods_total', []), a, b)
    dp_ = tang(th.get('container_cpu_throttling_data_periods_total', []), a, b)
    ratio = (dt_ / dp_) if (dt_ is not None and dp_) else None
    gia_tri['throttle_ratio_booking'] = ratio
    # --- nhãn ---
    if ly['mat_quan_sat']:
        nhan = 'mat_quan_sat'
    elif ly['bien']:
        nhan = 'bien'
    elif ratio is not None and ratio > QUOTA and not vi:
        nhan = 'quota'
        ly['quota'].append(f'throttle {ratio:.3f} > 0,2')
    elif muc == 'x3':
        nhan = 'flash'
    elif vi:
        nhan = 'suy_giam'
        ly['suy_giam'] = vi
    else:
        nhan = 'khoe_x1'
    # --- ghi kèm: L1 và số điểm chuỗi luật ---
    l1 = {u: collections.Counter() for u in L1_DICH}
    for kn, vals in luat.get('tin-hieu/live-3-trang-thai', {}).items():
        u = json.loads(kn).get('http_url')
        for t, v in vals.items():
            if a <= t < b:
                l1.setdefault(u, collections.Counter())[str(int(v))] += 1
    l1 = {u: dict(c, khong_co_buoc=max(0, BUOC_PHUT - sum(c.values()))) for u, c in l1.items()}
    diem_luat = {ten: sum(1 for kn, vals in s.items() for t in vals if a <= t < b)
                 for ten, s in luat.items() if ten.startswith('tin-hieu/')}
    ket.append({'phut': iso(m), 'luot': l['tag'] if l else None, 'muc': muc, 'nhan': nhan,
                'ly_do': {k: v for k, v in ly.items() if v}, 'vi_pham': vi, 'gia_tri': gia_tri, 'co': co,
                'ghi_kem': {'L1_theo_dich': l1, 'diem_chuoi_luat': diem_luat},
                'canh_bao': None})

# cờ lan_cua_so: phút không phải biên mà cửa sổ 300 s của một bước trong phút giao phút lớp khác (m−5 … m−1)
by = {r['phut']: r for r in ket}
for i, r in enumerate(ket):
    if r['nhan'] == 'bien':
        r['co']['lan_cua_so'] = None
        continue
    truoc = [ket[j]['nhan'] if j >= 0 else 'ngoai_e2' for j in range(i - 5, i)]
    r['co']['lan_cua_so'] = any(n != r['nhan'] for n in truoc)

# ---- tổng hợp ----
dem = collections.Counter(r['nhan'] for r in ket)
dem_luot = collections.defaultdict(collections.Counter)
for r in ket:
    dem_luot[r['luot'] or '(giữa lượt)'][r['nhan']] += 1
khoe = [r for r in ket if r['nhan'] == 'khoe_x1']
chuyen = [{'tu': p['tag'], 'sang': q['tag'], 'giay': round(q['S'] - p['F'], 3)} for p, q in zip(luot, luot[1:])]
tom = {
    'khai_truoc': KHAI, 'khai_truoc_sha256': H,
    'cua_so': [iso(m0), iso(m1 + 60)], 'so_phut': len(ket), 'dem_theo_nhan': dict(dem),
    'khoe_x1_phut': len(khoe), 'khoe_x1_khong_co_lan_cua_so': sum(1 for r in khoe if not r['co']['lan_cua_so']),
    'du_sau_gio_khoe_x1': len(khoe) >= 360,
    'dem_theo_luot': {k: dict(v) for k, v in dem_luot.items()},
    'luot': [{k: l[k] for k in ('thu_tu', 'tag', 'muc', 'seconds')} | {'StartedAt': iso(l['S']), 'FinishedAt': iso(l['F']),
             'giay_chay': round(l['F'] - l['S'], 3), 'exit': l['exit'], 'oom': l['oom'], 'raw_sha256': l['raw_sha256']}
             for l in luot],
    'chuyen_luot_giay': chuyen,
    'khuc_xuat_loi': loi_luat + loi_dl,
    'cai_dat': cai_dat_note,
    'thieu_b2_phut': sum(1 for r in ket if r['co'].get('thieu_b2')),
    'vi_pham_theo_ma': dict(collections.Counter(v for r in ket for v in r['vi_pham'])),
    'ghi_chu': 'canh_bao để trống: T-072 điền (chấm offline). Không chọn ngưỡng ở đây.'}
json.dump({'tom_tat': tom, 'phut': ket}, open(RA, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(json.dumps(tom, ensure_ascii=False, indent=1))

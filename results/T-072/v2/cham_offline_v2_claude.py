# -*- coding: utf-8 -*-
"""T-072 — bộ chấm offline. Bản v2_claude = v2 của Codex (CX-24) + phần quy_ve / Pending / ca đầu khoảng của
Claude T-072 (đáp CX-19 F5). File v2 của Codex giữ nguyên.

T-072 — bộ chấm offline luật cảnh báo W4 và quy tắc chọn ngưỡng.

Đọc: bieu-thuc.json (T072-bieu-thuc-1), quy-tac-gom.json, quy-tac-chon-nguong.json (phiên bản đọc từ chính file),
chuỗi xuất dạng xuat_tin_hieu.py (T072-xuat-1). Không đọc sổ tiêm/nhãn ca (luật cứng 6).

Lệnh:
  cham        --xuat f1.json [f2.json ...] --nguong nguong.json [--phut phut.json] [--chen ten|khoa|t0|dai|gia] [--ra out.json]
  chon-nguong --xuat ...E2... --phut phut-E2.json --ra nguong.json
  tu-kiem     (phép thử giả trên chuỗi tổng hợp; thoát 1 nếu có ca sai)

phut.json: {"khoang": [[start_epoch, end_epoch, "lop"], ...]} (nửa mở; lop như T-071, khỏe ×1 = "khoe-x1").
--chen: thay giá trị chuỗi `ten` (khóa = giá trị http_route/http_url, '' nếu một chuỗi) trong [t0, t0+dai) bằng `gia`
        ('none' = xóa điểm); dùng cho phép thử giả trên dữ liệu thật.
"""
import argparse, hashlib, json, math, pathlib, sys

CODE = pathlib.Path(__file__).resolve()
GOC = CODE.parent.parent
RA = CODE.parent / 'ra'
STEP = 10
GHEP_S = 300
KHOE = 'khoe-x1'


def nap(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def khoa(metric):
    return metric.get('http_route') or metric.get('http_url') or ''


# ---------- dữ liệu ----------
class Du:
    """chuoi[ten][khoa] = {t: float}; luoi = tập bước có xuất; hong[ten] = tập bước thuộc khúc lỗi."""

    def __init__(self):
        self.chuoi, self.luoi, self.hong = {}, set(), {}

    def them(self, doc):
        s, e, st = doc['cua_so'][0], doc['cua_so'][1], doc.get('step_s', STEP)
        self.luoi |= set(range(s, e + 1, st))
        for lk in doc.get('loi_khuc', []):
            self.hong.setdefault(lk['ten'], set()).update(range(lk['start'], lk['end'] + 1, st))
        for ten, ds in doc['chuoi'].items():
            c = self.chuoi.setdefault(ten, {})
            for x in ds:
                d = c.setdefault(khoa(x['metric']), {})
                for t, v in x['values']:
                    d[int(t)] = float(v)


def chen(du, spec):
    ten, k, t0, dai, gia = spec.split('|')
    t0, dai = int(t0), int(dai)
    d = du.chuoi.setdefault(ten, {}).setdefault(k, {})
    for t in range(t0 - t0 % STEP, t0 + dai, STEP):
        if t < t0:
            continue
        if gia == 'none':
            d.pop(t, None)
        else:
            d[t] = float(gia)


# ---------- đánh giá luật ----------
def nguong_cua(luat, ng):
    n = luat['dieu_kien']['nguong']
    if isinstance(n, (int, float)):
        return float(n)
    if n not in ng:
        raise SystemExit(f'thiếu ngưỡng {n}')
    return float(ng[n])


def dung(op, v, th):
    return v > th if op == '>' else v < th


def gia_tri_duy_tri(phep, mau):
    """Giá trị bất lợi nhất cho điều kiện trong một cửa sổ đủ mẫu."""
    return max(mau) if phep == '<' else min(mau)


def danh_gia(bt, du, ng):
    """Trả danh sách khoảng cháy {uid, loai, nhan, t_hat, t_het, cat_cuoi}."""
    luoi = sorted(du.luoi)
    ra = []
    for L in bt['luat']:
        ten = 'tin-hieu/' + L['uid']
        th, op, fs = nguong_cua(L, ng), L['dieu_kien']['phep'], L['for_s']
        trong_dung = L['no_data_state'] == 'Alerting'
        data = du.chuoi.get(ten, {})
        khoas = sorted(data) if data else ['']
        hong = du.hong.get(ten, set())
        for k in khoas:
            d = data.get(k, {})
            tp, firing, t_hat = None, False, None
            prev = None
            for t in luoi:
                if prev is not None and t - prev != STEP:  # lỗ lưới giữa hai file xuất → đặt lại
                    if firing:
                        ra.append(_kc(L, k, t_hat, prev + STEP, True, tp))
                    tp, firing = None, False
                prev = t
                if t in hong:
                    if firing:
                        ra.append(_kc(L, k, t_hat, t, True, tp))
                    tp, firing = None, False
                    continue
                v = d.get(t)
                ok = trong_dung if v is None else dung(op, v, th)
                # Pending (Claude T-072, v2_claude): giữ nguyên. tp = bước đúng đầu tiên của dãy đúng liên tiếp; Alerting khi
                # t - tp >= for_s. Khớp Grafana (Normal->Pending ở lần đánh giá đúng đầu tiên) trên 4 luật thử E3 (lệch -4 s, pha).
                # Dãy đúng ngay từ bước đầu lưới: lịch sử trước lưới không thấy -> quy_ve gắn cờ 'pending-tu-dau-luoi'.
                if ok:
                    if tp is None:
                        tp = t
                    if not firing and t - tp >= fs:
                        firing, t_hat = True, t
                else:
                    if firing:
                        ra.append(_kc(L, k, t_hat, t, False, tp))
                    tp, firing = None, False
            if firing:
                ra.append(_kc(L, k, t_hat, None, True, tp))
    return ra


def _kc(L, k, t_hat, t_het, cat, tp):
    return {'uid': L['uid'], 'loai': L['loai'], 'khoa': k, 't_hat': t_hat, 't_het': t_het, 'cat': cat, 'tp': tp}


# ---------- gom và quy về phút ----------
def gom(kcs):
    out = []
    for loai in ('he-thong', 'quan-sat'):
        ds = sorted((x for x in kcs if x['loai'] == loai), key=lambda x: x['t_hat'])
        cur = None
        for x in ds:
            het = math.inf if x['t_het'] is None else x['t_het']
            if cur and x['t_hat'] <= cur['_het'] + GHEP_S:
                cur['canh_bao'].append(x)
                cur['_het'] = max(cur['_het'], het)
            else:
                cur = {'loai': loai, 't_hat': x['t_hat'], '_het': het, 'canh_bao': [x]}
                out.append(cur)
    for s in out:
        s['t_het'] = None if s['_het'] == math.inf else s.pop('_het')
        s.pop('_het', None)
    return sorted(out, key=lambda s: (s['t_hat'], s['loai']))


class Phut:
    def __init__(self, doc):
        self.k = [tuple(x) for x in (doc or {}).get('khoang', [])]

    def lop(self, t):
        for a, b, l in self.k:
            if a <= t < b:
                return l
        return 'chua-phan-loai'

    def so_phut(self, lop, luoi):
        ph = {t // 60 * 60 for t in luoi}
        return sum(1 for m in ph if self.lop(m) == lop)


def quy_ve(sus, phut, t_dau, bat_dau=None):
    """Quy sự cố về phút theo quy-tac-gom.json#/quy_ve_phut (Claude T-072, v2_claude; sửa CX-19 F5).

    - Lớp = lớp của phút chứa t̂ sự cố (t̂ = lúc vào Alerting), như cũ.
    - bat_dau = đầu khoảng chấm (giờ hiệu lực hoặc mốc khai trước), epoch giây. Sự cố có t̂ < bat_dau: còn cháy tại
      bat_dau (t_het None hoặc t_het > bat_dau; khoảng nửa mở) -> 'dang-chay-luc-bat-dau'; đã hết -> 'truoc-khoang'.
      Cả hai không vào tử số. bat_dau = None -> không xét. (Bản cũ so tp với bước đầu lưới xuất: sai nghĩa quy tắc, bỏ.)
    - Cờ 'pending-truoc-khoang': có cảnh báo vào Pending trước bat_dau nhưng Alerting từ bat_dau trở đi (vẫn đếm theo t̂).
    - Cờ 'pending-tu-dau-luoi': dãy đúng bắt đầu ngay bước đầu lưới t_dau; offline không thấy lịch sử trước lưới nên
      t̂ offline có thể muộn hơn Grafana; phải đối chiếu lịch sử trạng thái Grafana.
    """
    for s in sus:
        m = s['t_hat'] // 60 * 60
        s['lop'] = phut.lop(m)
        s['co'] = []
        if bat_dau is not None and s['t_hat'] < bat_dau:
            s['lop'] = 'dang-chay-luc-bat-dau' if (s['t_het'] is None or s['t_het'] > bat_dau) else 'truoc-khoang'
        elif bat_dau is not None and any(c.get('tp') is not None and c['tp'] < bat_dau for c in s['canh_bao']):
            s['co'].append('pending-truoc-khoang')
        if any(c.get('tp') == t_dau for c in s['canh_bao']):
            s['co'].append('pending-tu-dau-luoi')
        lops = {phut.lop(x) for x in range(m - GHEP_S, m + 1, 60)}
        if lops - {phut.lop(m)}:  # so với lớp của phút (không với lớp đầu khoảng), v2_claude
            s['co'].append('cua-so-lan')
        if any(c['cat'] and c['t_het'] is not None for c in s['canh_bao']):
            s['co'].append('lo-du-lieu-xuat')
        if s['t_het'] is None:
            s['co'].append('chua-het')
    return sus


def poisson_ci(n, a=0.05):
    def cdf(k, lam):
        return sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k + 1))

    def tim(f, lo, hi):
        for _ in range(100):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lo = 0.0 if n == 0 else tim(lambda l: 1 - cdf(n - 1, l) < a / 2, 0, 10 * n + 10)
    hi = tim(lambda l: cdf(n, l) > a / 2, 0, 10 * n + 20)
    return lo, hi


def cham(bt, du, ng, phut, bat_dau=None):
    kcs = danh_gia(bt, du, ng)
    luoi = sorted(du.luoi)
    sus = quy_ve(gom(kcs), phut, luoi[0] if luoi else 0, bat_dau)
    quan_sat = [q for q in sus if q['loai'] == 'quan-sat']
    dem = {}
    for s in sus:
        if s['loai'] == 'he-thong' and any(
                (q['t_het'] is None or s['t_hat'] < q['t_het']) and
                (s['t_het'] is None or q['t_hat'] < s['t_het']) for q in quan_sat):
            s['co'].append('chong-quan-sat')
        dem.setdefault(s['loai'], {}).setdefault(s['lop'], 0)
        dem[s['loai']][s['lop']] += 1
    pk = phut.so_phut(KHOE, [t for t in luoi if bat_dau is None or t // 60 * 60 >= bat_dau])  # chỉ phút trọn từ bat_dau
    n = dem.get('he-thong', {}).get(KHOE, 0)
    ty = None
    if pk:
        lo, hi = poisson_ci(n)
        ty = {'su_co': n, 'phut_khoe_x1': pk, 'moi_6_gio': n / (pk / 360), 'ci95_moi_6_gio': [lo / (pk / 360), hi / (pk / 360)],
              'du_6_gio': pk >= 360}
    return {'khoang_chay': kcs, 'su_co': sus, 'dem': dem, 'ty_le_khoe_x1': ty,
            'so_buoc': len(luoi), 'so_phut': len({t // 60 for t in luoi})}


# ---------- chọn ngưỡng ----------
def chon_nguong(bt, qt, du, phut):
    luat = {L['uid']: L for L in bt['luat']}
    ct = qt['cong_thuc']
    ng, chi_tiet = {}, {}
    luoi = sorted(du.luoi)
    for r in bt['tham_so_co_dinh']['routes']:
        for loai, ten, fsuid, k, san, cong in (
                ('p95', f'tin-hieu/t072-p95-{r}', f't072-p95-{r}', ct['p95']['k_p95'], ct['p95']['san_p95_s'], True),
                ('loi', f'phu/ty-le-loi-chua-chan-5xx-{r}', f't072-loi-{r}', ct['ty_le_loi']['k_loi'], ct['ty_le_loi']['san_loi'], False)):
            d = du.chuoi.get(ten, {}).get(r, {})
            w = luat[fsuid]['for_s']
            phep = luat[fsuid]['dieu_kien']['phep']
            S_all, S_sach = [], []
            for t in luoi:
                if phut.lop(t // 60 * 60) != KHOE:
                    continue
                vs = [d.get(u) for u in range(t - w, t + 1, STEP)]
                if any(v is None for v in vs):
                    continue
                s = gia_tri_duy_tri(phep, vs)
                S_all.append(s)
                m = t // 60 * 60
                if not ({phut.lop(x) for x in range(m - GHEP_S, m + 1, 60)} - {KHOE}):
                    S_sach.append(s)
            tenp = f'theta_{loai}_{r}'
            if len(S_all) < qt['thong_ke'].get('so_buoc_toi_thieu', 120):
                chi_tiet[tenp] = {'loi': 'không đủ dữ liệu E2', 'so_buoc': len(S_all)}
                continue
            M = max(S_all)
            th = max(k * M, M + san) if cong else max(k * M, san)
            th = math.ceil(th * 1000 - 1e-9) / 1000
            ng[tenp] = th
            chi_tiet[tenp] = {'M': M, 'M_bo_cua_so_lan': max(S_sach) if S_sach else None, 'so_buoc': len(S_all),
                              'so_buoc_sach': len(S_sach)}
    return ng, chi_tiet


# ---------- phép thử giả ----------
def tu_kiem(bt):
    sai = []
    ng = {f'theta_{a}_{r}': (0.2 if a == 'p95' else 0.05) for a in ('p95', 'loi') for r in bt['tham_so_co_dinh']['routes']}
    T0 = 1_800_000_000  # chia hết cho 60

    def du_nen(dai=7200, tai=True):
        d = Du()
        doc = {'cua_so': [T0, T0 + dai], 'step_s': STEP, 'loi_khuc': [], 'chuoi': {}}
        ts = list(range(T0, T0 + dai + 1, STEP))
        for r in bt['tham_so_co_dinh']['routes']:
            if tai:
                doc['chuoi'][f'tin-hieu/t072-p95-{r}'] = [{'metric': {'http_route': r}, 'values': [[t, '0.05'] for t in ts]}]
                doc['chuoi'][f'phu/ty-le-loi-chua-chan-5xx-{r}'] = [{'metric': {'http_route': r}, 'values': [[t, '0'] for t in ts]}]
        doc['chuoi']['tin-hieu/t072-live'] = [{'metric': {'http_url': u}, 'values': [[t, '0'] for t in ts]} for _, u in
                                              [(0, 'u1'), (0, 'u2')]]
        doc['chuoi']['tin-hieu/t072-mat-do'] = [{'metric': {}, 'values': [[t, '8'] for t in ts]}]
        doc['chuoi']['tin-hieu/t072-mat-gw'] = [{'metric': {}, 'values': [[t, '9'] for t in ts]}]
        d.them(doc)
        return d

    def ca(ten, chens, ky_vong, phut=None, bo=None, bat_dau=None, co=None, so_khoang=None):
        d = du_nen()
        for c in chens:
            chen(d, c)
        if bo:
            bo(d)
        kq = cham(bt, d, ng, Phut(phut), None if bat_dau is None else T0 + bat_dau)
        got = [(s['loai'], s['lop'], s['t_hat'] - T0) for s in kq['su_co']]
        if got != ky_vong:
            sai.append({'ca': ten, 'ky_vong': ky_vong, 'duoc': got})
        if co is not None and [sorted(s['co']) for s in kq['su_co']] != co:
            sai.append({'ca': ten + '/co', 'ky_vong': co, 'duoc': [sorted(s['co']) for s in kq['su_co']]})
        if so_khoang is not None and len(kq['khoang_chay']) != so_khoang:
            sai.append({'ca': ten + '/so-khoang', 'ky_vong': so_khoang, 'duoc': len(kq['khoang_chay'])})
        return kq

    P = 'tin-hieu/t072-p95-booking'
    ca('nen-khong-su-co', [], [])
    ca('buoc-nhay-120s', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)])
    ca('bang-nguong-khong-chay', [f'{P}|booking|{T0+1000}|120|0.2'], [])  # điều kiện là '>' nghiêm
    ca('buoc-nhay-50s-ngan-hon-for', [f'{P}|booking|{T0+1000}|50|0.5'], [])
    ca('dung-60s-dung-nguong-for', [f'{P}|booking|{T0+1000}|70|0.5'], [('he-thong', 'chua-phan-loai', 1060)])
    ca('hai-buoc-cach-200s-gop', [f'{P}|booking|{T0+1000}|120|0.5', f'{P}|booking|{T0+1320}|120|0.5'],
       [('he-thong', 'chua-phan-loai', 1060)])
    ca('hai-buoc-cach-400s-tach', [f'{P}|booking|{T0+1000}|120|0.5', f'{P}|booking|{T0+1520}|120|0.5'],
       [('he-thong', 'chua-phan-loai', 1060), ('he-thong', 'chua-phan-loai', 1580)])
    ca('hai-route-chong-gop', [f'{P}|booking|{T0+1000}|120|0.5', f'tin-hieu/t072-p95-event|event|{T0+1030}|200|0.9'],
       [('he-thong', 'chua-phan-loai', 1060)])
    ca('loi-5xx', [f'phu/ty-le-loi-chua-chan-5xx-payment|payment|{T0+2000}|0|0'], [])  # phu/* không là chuỗi luật
    for r in bt['tham_so_co_dinh']['routes']:  # mỗi luật lỗi và mỗi luật p95 đều phải bắt được
        ca(f'luat-loi-{r}', [f'tin-hieu/t072-loi-{r}|{r}|{T0+2000}|90|0.4'], [('he-thong', 'chua-phan-loai', 2060)])
        ca(f'luat-loi-{r}-duoi-nguong', [f'tin-hieu/t072-loi-{r}|{r}|{T0+2000}|90|0.04'], [])
        ca(f'luat-p95-{r}', [f'tin-hieu/t072-p95-{r}|{r}|{T0+2500}|90|0.3'], [('he-thong', 'chua-phan-loai', 2560)])
    # Ca đầu khoảng (Claude T-072, v2_claude; thay ca cũ "Pending ở t0 -> đang cháy", sai nghĩa quy tắc, CX-19 F5).
    ca('dung-tu-dau-luoi-khong-bat-dau', [f'{P}|booking|{T0}|120|0.5'], [('he-thong', 'chua-phan-loai', 60)],
       co=[['pending-tu-dau-luoi']], so_khoang=1)
    ca('pending-truoc-alerting-sau-bat-dau', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)],
       bat_dau=1030, co=[['pending-truoc-khoang']], so_khoang=1)
    ca('alerting-dung-bat-dau-van-dem', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)],
       bat_dau=1060, co=[['pending-truoc-khoang']], so_khoang=1)
    ca('pending-dung-bat-dau-khong-co', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)],
       bat_dau=1000, co=[[]], so_khoang=1)
    ca('dang-chay-luc-bat-dau', [f'{P}|booking|{T0+1000}|300|0.5'], [('he-thong', 'dang-chay-luc-bat-dau', 1060)],
       bat_dau=1100, co=[[]], so_khoang=1)
    ca('het-truoc-bat-dau', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'truoc-khoang', 1060)], bat_dau=1200, co=[[]])
    ca('het-dung-bat-dau-nua-mo', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'truoc-khoang', 1060)],
       bat_dau=1120, co=[[]])
    kq_ms = ca('mau-so-sau-bat-dau', [], [], phut={'khoang': [[T0, T0 + 7300, KHOE]]}, bat_dau=1200)
    if kq_ms['ty_le_khoe_x1']['phut_khoe_x1'] != 101:
        sai.append({'ca': 'mau-so-sau-bat-dau', 'duoc': kq_ms['ty_le_khoe_x1']['phut_khoe_x1']})
    ca('mat-do-dung-mot-khoang', ['tin-hieu/t072-mat-do||%d|120|none' % (T0 + 4000)], [('quan-sat', 'chua-phan-loai', 4060)],
       so_khoang=1)
    ca('guard-khong-diem-khong-chay', [f'{P}|booking|{T0+1000}|600|none'], [])
    ca('live-30s', ['tin-hieu/t072-live|u1|%d|30|1' % (T0 + 3000)], [('he-thong', 'chua-phan-loai', 3020)])
    ca('live-15s-khong', ['tin-hieu/t072-live|u1|%d|15|1' % (T0 + 3000)], [])
    ca('mat-do-thieu-diem-la-quan-sat', ['tin-hieu/t072-mat-do||%d|120|none' % (T0 + 4000)], [('quan-sat', 'chua-phan-loai', 4060)])
    ca('mat-gw-tuoi-lon', ['tin-hieu/t072-mat-gw||%d|120|90' % (T0 + 4000)], [('quan-sat', 'chua-phan-loai', 4060)])
    ph = {'khoang': [[T0, T0 + 1200, KHOE], [T0 + 1200, T0 + 1500, 'bien'], [T0 + 1500, T0 + 7300, KHOE]]}
    kq = ca('vat-qua-bien-dem-mot-lan', [f'{P}|booking|{T0+1100}|300|0.5'], [('he-thong', KHOE, 1160)], ph)
    if kq['ty_le_khoe_x1']['phut_khoe_x1'] != 116:
        sai.append({'ca': 'mau-so-phut', 'duoc': kq['ty_le_khoe_x1']})
    ca('bat-dau-trong-bien', [f'{P}|booking|{T0+1250}|120|0.5'], [('he-thong', 'bien', 1310)], ph)
    kq = ca('cua-so-lan-co-co', [f'{P}|booking|{T0+1560}|120|0.5'], [('he-thong', KHOE, 1620)], ph)
    if 'cua-so-lan' not in kq['su_co'][0]['co']:
        sai.append({'ca': 'co-cua-so-lan', 'duoc': kq['su_co'][0]['co']})

    def hong(d):
        d.hong.setdefault(P, set()).update(range(T0 + 1080, T0 + 1100, STEP))
    ca('khuc-xuat-loi-dat-lai', [f'{P}|booking|{T0+1000}|130|0.5'], [('he-thong', 'chua-phan-loai', 1060)], bo=hong)
    # chọn ngưỡng: M = 0.05 → θ_p95 = max(0.075, 0.1) = 0.1; θ_loi = 0.05
    d = du_nen()
    chen(d, f'{P}|booking|{T0+500}|30|0.3')  # gai 30 s < for: không vào M
    n, ct = chon_nguong(bt, nap(GOC / 'quy-tac-chon-nguong.json'), d, Phut({'khoang': [[T0, T0 + 7300, KHOE]]}))
    if n.get('theta_p95_booking') != 0.1 or n.get('theta_loi_booking') != 0.05:
        sai.append({'ca': 'chon-nguong', 'duoc': n})
    d = du_nen(dai=600)
    n, ct = chon_nguong(bt, nap(GOC / 'quy-tac-chon-nguong.json'), d, Phut({'khoang': [[T0, T0 + 700, KHOE]]}))
    if n or 'không đủ' not in json.dumps(ct, ensure_ascii=False):
        sai.append({'ca': 'chon-nguong-thieu-du-lieu', 'duoc': [n, ct]})
    lo, hi = poisson_ci(0)
    if not (abs(hi - 3.689) < 0.01 and lo == 0):
        sai.append({'ca': 'poisson', 'duoc': [lo, hi]})
    return sai


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lenh', choices=['cham', 'chon-nguong', 'tu-kiem'])
    ap.add_argument('--xuat', nargs='*', default=[])
    ap.add_argument('--nguong')
    ap.add_argument('--phut')
    ap.add_argument('--chen', action='append', default=[])
    ap.add_argument('--bat-dau', help='đầu khoảng chấm: epoch giây hoặc YYYY-mm-ddTHH:MM:SSZ (v2_claude)')
    ap.add_argument('--ra', help='Tên file JSON xuất trong v2/ra/')
    a = ap.parse_args()
    dich = pathlib.Path(a.ra or f'{a.lenh}.json')
    if dich.parent == pathlib.Path('.'):
        dich = RA / dich
    dich = dich.resolve()
    if dich.parent != RA or dich.suffix.lower() != '.json':
        ap.error('--ra phải là file .json trong v2/ra/')
    bt = nap(GOC / 'bieu-thuc.json')
    if a.lenh == 'tu-kiem':
        sai = tu_kiem(bt)
        out = {'phep_thu_gia': 'tu-kiem', 'sai': sai, 'dat': not sai}
    else:
        du = Du()
        for f in a.xuat:
            du.them(nap(f))
        for c in a.chen:
            chen(du, c)
        phut = Phut(nap(a.phut) if a.phut else None)
        bat_dau = None
        if a.bat_dau:
            import datetime as _dt
            bat_dau = (int(a.bat_dau) if a.bat_dau.isdigit()
                       else int(_dt.datetime.fromisoformat(a.bat_dau.replace('Z', '+00:00')).timestamp()))
        if a.lenh == 'cham' and not a.nguong:
            a.nguong = str(GOC / 'nguong.json')
        dauvao = {f: sha(f) for f in a.xuat + ([a.phut] if a.phut else []) + ([a.nguong] if a.nguong else [])}
        dauvao.update({str(GOC / x): sha(GOC / x) for x in
                       ('bieu-thuc.json', 'quy-tac-gom.json', 'quy-tac-chon-nguong.json')})
        if a.lenh == 'chon-nguong':
            qt_doc = nap(GOC / 'quy-tac-chon-nguong.json')
            ng, ct = chon_nguong(bt, qt_doc, du, phut)
            thieu = [f"{route} ({loai}, {ct[ten]['so_buoc']} bước)"
                     for route in bt['tham_so_co_dinh']['routes'] for loai in ('p95', 'loi')
                     if (ten := f'theta_{loai}_{route}') not in ng]
            if thieu:
                print('Không đủ dữ liệu E2 cho route: ' + ', '.join(thieu), file=sys.stderr)
                return 1
            out = {'phien_ban': 'T072-nguong', 'quy_tac': qt_doc['phien_ban'], 'nguong': ng, 'chi_tiet': ct, 'dau_vao_sha256': dauvao}
            out['trong_mau'] = cham(bt, du, ng, phut)['dem']
        else:
            ng = nap(a.nguong)['nguong']
            out = cham(bt, du, ng, phut, bat_dau)
            out.update({'nguong': ng, 'chen': a.chen, 'bat_dau_khoang': bat_dau, 'dau_vao_sha256': dauvao})
    out.setdefault('dau_vao_sha256', {})[str(CODE)] = sha(CODE)
    txt = json.dumps(out, ensure_ascii=False, indent=1)
    RA.mkdir(exist_ok=True)
    dich.write_text(txt + '\n', encoding='utf-8')
    sys.stdout.buffer.write((json.dumps({k: out[k] for k in out if k in ('dat', 'sai', 'dem', 'ty_le_khoe_x1', 'nguong', 'so_buoc', 'so_phut')},
                                        ensure_ascii=False) + '\n').encode('utf-8'))
    return int(a.lenh == 'tu-kiem' and bool(sai))


if __name__ == '__main__':
    sys.exit(main())

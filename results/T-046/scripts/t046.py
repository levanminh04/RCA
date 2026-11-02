"""T-046: nạp ca, dựng cửa sổ (thật, A/A theo A1, C-e), chạy chuỗi M1 có móc ghi mẫu và mốc thời gian, rồi tính p của
từng phép theo G0, G1, G3 và quy tắc `verdict` V0, V1, V3 (SPEC T-046 mục Ứng viên, Phạm vi phép kiểm, A1–A5).

Không sửa src. Móc chỉ đọc giá trị đi qua các hàm của chuỗi (`span.mau_thao_tac`, `span.mau_canh`,
`e4.cham_phan_vi`, `kenh.don_vi_log`, `kenh.don_vi_mau_drain`) và thay cache cổng `chuoi.CACHE` (đối tượng có cùng
giao diện; ở chế độ ghi, p tính bằng chính `e4.p_cong`). Bản ghi của chuỗi phải giống hệt bản ghi không móc (kiểm
ở bước 1 với bản ghi T-045). Không đọc nhãn: chỉ mã mờ và mốc t chế độ (a).

Cửa sổ:
- 'that': t (mốc tiêm).
- 'aa' (A1): đầu vào cắt về [t − 300, t) (span theo start, end; metric, log theo mốc; coverage cắt cùng đoạn);
  chạy tại t″: RE2-TT t − 150; Nezha-OB ⌊(s₀ + t)/2⌋ giây, s₀ là end sớm nhất của span thuộc N.
- 'ce': chỉ RE2-TT, t − 300 (adapter nạp miền [t − 600, t)).
"""
import copy
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for p in (ROOT / 'src', Path(__file__).resolve().parent):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from m1 import adapter, chuoi, e3 as e3_mod, e4, hop_dong, kenh as kenh_mod, quan_sat, runner, span  # noqa: E402
from p3 import nezha, nhan, selector  # noqa: E402
import cong  # noqa: E402

NS = 10 ** 9
NUA = 300
CONG = ('G0', 'G1', 'G3')
VERDICT = ('V0', 'V3', 'V1')


# ---------------------------------------------------------------- môi trường, cấu hình

def moi_truong():
    return {
        'hop_dong': json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8')),
        'U_re': json.loads((ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U'],
        'moc_re': nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json'),  # chỉ mốc tiêm (Q-66)
        're': selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json'),
        'nz': nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json'),
    }


def danh_sach_ca(mt):
    return [('RE2-TT', o) for o in sorted(mt['re'])] + [('Nezha-OB', o) for o in sorted(mt['nz'])]


def cau_hinh(ten):
    """'R0' (T1-R0 như T-045) hoặc 'K-du' (A5: E1-U, E2-C, E3, E5 bật; cấu hình K-E1+E2+E3+E5 của khối K)."""
    mt = runner.ap_dinh_chinh(json.loads((ROOT / 'results/T-043/ma-tran-thu.json').read_text(encoding='utf-8')))
    sinh = runner.sinh_cau_hinh(mt, {}, dict(runner.R0))
    if ten == 'R0':
        return sinh['T1'][0]
    if ten == 'K-du':
        c = [c for c in sinh['K'] if c['config_id'] == 'K-E1+E2+E3+E5']
        assert len(c) == 1
        return c[0]
    raise ValueError(ten)


# ---------------------------------------------------------------- nạp ca, cửa sổ

def nap(ds, oid, kieu, mt):
    """Trả (ca, t_chay, meta). t_chay là giây nguyên."""
    if ds == 'RE2-TT':
        t = mt['moc_re'][oid]
        t_nap = t - NUA if kieu == 'ce' else t
        ca = adapter.ca_re2tt(mt['re'], oid, t_nap, ROOT, mt['hop_dong'], mt['U_re'])
    else:
        if kieu == 'ce':
            raise ValueError('Nezha-OB không có C-e (D6)')
        ca = adapter.ca_nezha(mt['nz'], oid, ROOT, mt['hop_dong'])
        t = ca['t']
    meta = {'dataset': ds, 'opaque_id': oid, 'kieu': kieu, 't': t}
    if kieu == 'that':
        return ca, t, meta
    if kieu == 'ce':
        meta['t_chay'] = t - NUA
        return ca, t - NUA, meta
    ca = cat_aa(ca, t * NS)
    if ds == 'RE2-TT':
        t2 = t - 150
    else:
        s0 = min((s['start_us'] + s['duration_us']) * 1000 for s in ca['spans']) if ca['spans'] else None
        if s0 is None:
            raise ValueError('Nezha-OB A/A: không có span thuộc N')
        meta['s0_ns'] = int(s0)
        t2 = ((int(s0) + t * NS) // 2) // NS
    meta['t_chay'] = t2
    return ca, t2, meta


def cat_aa(ca, t_ns):
    """A1: cắt đầu vào và coverage về [t − 300, t)."""
    ca = copy.deepcopy(ca)
    pc = ca['params_ca']
    dv = pc['don_vi_thoi_gian']
    lo, hi = t_ns - NUA * NS, t_ns
    he_s = chuoi._he_so_ns(dv['spans.start_us'])
    he_m = chuoi._he_so_ns(dv['metrics.time'])
    he_l = chuoi._he_so_ns(dv['logs.timestamp'])
    ca['spans'] = [s for s in ca['spans']
                   if s['start_us'] * he_s >= lo and (s['start_us'] + s['duration_us']) * he_s < hi]
    tg = pc.get('thoi_gian_nguon') or {}
    rieng = {k: v for k, v in tg.items() if isinstance(v, list)}
    giu = []
    for i, r in enumerate(ca['metrics']):
        moc = [int(r['time'] * he_m)] + [int(v[i]) for v in rieng.values()]
        if all(lo <= m < hi for m in moc):
            giu.append(i)
    ca['metrics'] = [ca['metrics'][i] for i in giu]
    for k, v in rieng.items():
        tg[k] = [v[i] for i in giu]
    ca['logs'] = [g for g in ca['logs'] if lo <= g['timestamp'] * he_l < hi]
    for ten, c in (pc.get('coverage') or {}).items():
        r = c['r_ns']
        moi = []
        for a, b in c['khoang']:
            a2, b2 = max(a, lo), min(b + r, hi) - r
            if b2 >= a2 and min(b + r, hi) > max(a, lo):
                moi.append([a2, b2])
        c['khoang'] = moi
    return ca


# ---------------------------------------------------------------- móc

class CacheMoc:
    """Cùng giao diện `e4.CacheCong.p`. Chế độ 'ghi': tính bằng e4.p_cong và ghi lại; 'phat': trả p đã cho theo
    (mã đơn vị, hướng), kiểm mẫu trùng mẫu đã ghi."""

    def __init__(self, che_do='ghi', bang=None):
        self.che_do = che_do
        self.bang = bang or {}
        self.ghi = {}
        self.trung = 0
        self.moi = 0

    def p(self, khoa_don_vi, A, N, huong, ts):
        k = (khoa_don_vi, huong)
        sig = _chu_ky(N, A)
        if self.che_do == 'phat':
            p, cach, sig0 = self.bang[k]
            if sig0 != sig:
                raise RuntimeError(f'mẫu khác lúc ghi: {k}')
            self.moi += 1
            return p, cach
        self.moi += 1
        kq = e4.p_cong(A, N, huong, int(ts.get('n_exact_max', 100)))
        self.ghi[k] = (kq[0], kq[1], sig)
        return kq


def _chu_ky(N, A):
    h = hashlib.sha256()
    h.update(json.dumps([sorted(float(x) for x in N), sorted(float(x) for x in A)]).encode())
    return h.hexdigest()


class Moc:
    """Gắn móc trong `with`; trả lại hàm gốc khi ra."""

    def __init__(self, cache, dem_cong=None):
        """dem_cong (bản 3): None giữ cờ đếm của chuỗi (D0); hoặc {'c': 'D1'|'DE', 'nguong': {(nhóm, hướng): α_ô},
        'alpha': α, 't_ns': t} để thay cờ và điểm của đơn vị đếm theo D1/DE trước khi dựng kênh."""
        self.cache = cache
        self.dem_cong = dem_cong
        self.cap = {'op': {}, 'canh': {}, 'pv': {}, 'dem': {}, 'su_kien_N': {}, 'h0': None}

    def __enter__(self):
        self._goc = (span.mau_thao_tac, span.mau_canh, e4.cham_phan_vi, kenh_mod.don_vi_log,
                     kenh_mod.don_vi_mau_drain, chuoi.CACHE, e3_mod.hoc_va_dem, chuoi._kenh_tu_ket_qua)
        g_tt, g_canh, g_pv, g_log, g_drain, _, g_hoc, g_kenh = self._goc
        cap = self.cap
        dc = self.dem_cong

        def kenh_tu_ket_qua(u, kq, huong_cham, lop_cua, khoi_phat=None):
            ma = u.get('ma')
            if (dc is not None and u.get('loai') == 'dem' and kq.get('trang_thai') == 'OK'
                    and kq.get('nhan') not in ('NEW_OP', 'STOPPED') and ma in cap['su_kien_N']):
                phi, _ = cong.he_so_phan_tan(cap['su_kien_N'][ma], cap['h0'], dc['t_ns'])
                lam = Fraction(kq['n_N']) * Fraction(kq['T_A']) / Fraction(kq['T_N'])
                kq = dict(kq)
                for d in ('len', 'xuong'):
                    p = cong.p_D1(kq['n_N'], kq['n_A'], kq['T_N'], kq['T_A'], phi, d)
                    a = dc['nguong'].get((u['nhom'], d), dc['alpha']) if dc['c'] == 'DE' else dc['alpha']
                    cheng = (kq['n_A'] - lam) if d == 'len' else (lam - kq['n_A'])
                    qua = d in huong_cham and p < a and cheng > 0
                    e_q = (max(Fraction(0), (kq['n_A'] - lam) / max(kq['n_A'], 1)) if d == 'len'
                           else max(Fraction(0), (lam - kq['n_A']) / max(lam, 1)))
                    kq[f'F_raw_{d}'] = int(qua)
                    kq[f'e_{d}_q'] = e_q if qua else Fraction(0)
                    kq[f'e_{d}'] = float(kq[f'e_{d}_q'])
            return g_kenh(u, kq, huong_cham, lop_cua, khoi_phat)

        def _h0(dong_N, dong_A):
            m = [d['moc'] for d in list(dong_N) + list(dong_A)]
            if m:
                cap['h0'] = min(m) if cap['h0'] is None else min(cap['h0'], min(m))

        def hoc_va_dem(dong_N, dong_A, tham_so_E3, quy_tac):
            # B2: mốc sự kiện N của từng cặp (thực thể, mẫu); lặp lại đúng vòng học N của e3.hoc_va_dem trên một Drain
            # mới cùng tham số và cùng thứ tự (tất định), rồi kiểm số dòng trùng
            out = g_hoc(dong_N, dong_A, tham_so_E3, quy_tac)
            dr = e3_mod.Drain(depth=int(tham_so_E3['do_sau']), sim_th=float(tham_so_E3['sim_th']), max_children=100,
                              max_clusters=None, extra_delimiters=(), parametrize_numeric_tokens=True)
            ev = {}
            for d in sorted(dong_N, key=lambda x: (x['moc'], x['thuc_the'], x['noi_dung'])):
                cl, _ = dr.add_log_message(e3_mod.che_token(d['noi_dung']))
                ev.setdefault((d['thuc_the'], cl.cluster_id), []).append(d['moc'])
            for (e, cid), c in out['cap'].items():
                if len(ev.get((e, cid), [])) != c['n_N']:
                    raise RuntimeError(f'mốc sự kiện N lệch số dòng: {(e, cid)}')
                cap['su_kien_N'][f'log|{e}|mau:{cid}'] = ev.get((e, cid), [])
            _h0(dong_N, dong_A)
            return out

        def mau_thao_tac(prep, E1):
            out = g_tt(prep, E1)
            cap['op'] = out
            return out

        def mau_canh(prep):
            out = g_canh(prep)
            cap['canh'] = out
            return out

        def cham_phan_vi(N, A, m, ts, huong_cham=('len',), cache=None, khoa_don_vi=None):
            kq = g_pv(N, A, m, ts, huong_cham=huong_cham, cache=cache, khoa_don_vi=khoa_don_vi)
            cap['pv'][khoa_don_vi] = {'N': list(N), 'A': list(A), 'huong_cham': list(huong_cham), 'kq': kq}
            return kq

        def don_vi_log(*a, **k):
            out = g_log(*a, **k)
            dong_N, dong_A, quy_tac, E3_bat = a[:4]
            if not E3_bat:
                ev = {}
                for d in dong_N:
                    if e3_mod._lop_dong(d, quy_tac) == e3_mod.LOI:
                        ev.setdefault(d['thuc_the'], []).append(d['moc'])
                for u in out:
                    m = ev.get(u['thuc_the'], [])
                    if len(m) != u['n_N']:
                        raise RuntimeError(f"mốc sự kiện N lệch: {u['thuc_the']}")
                    cap['su_kien_N'][f"log|{u['thuc_the']}|{u['ten']}"] = m
                _h0(dong_N, dong_A)
            for u in out:
                cap['dem'][f"log|{u['thuc_the']}|{u['ten']}"] = {k2: u[k2] for k2 in ('thuc_the', 'nhom', 'huong_cham')}
            return out

        def don_vi_mau_drain(*a, **k):
            out = g_drain(*a, **k)
            for u in out:
                cap['dem'][f"log|{u['thuc_the']}|{u['ten']}"] = {k2: u[k2] for k2 in ('thuc_the', 'nhom', 'huong_cham')}
            return out

        span.mau_thao_tac, span.mau_canh = mau_thao_tac, mau_canh
        e4.cham_phan_vi = cham_phan_vi
        kenh_mod.don_vi_log, kenh_mod.don_vi_mau_drain = don_vi_log, don_vi_mau_drain
        chuoi.CACHE = self.cache
        e3_mod.hoc_va_dem = hoc_va_dem
        chuoi._kenh_tu_ket_qua = kenh_tu_ket_qua
        return self

    def __exit__(self, *a):
        (span.mau_thao_tac, span.mau_canh, e4.cham_phan_vi, kenh_mod.don_vi_log, kenh_mod.don_vi_mau_drain,
         chuoi.CACHE, e3_mod.hoc_va_dem, chuoi._kenh_tu_ket_qua) = self._goc
        return False


def chay_chuoi(ca, t, ch, cache, dem_cong=None):
    """Chạy một cấu hình như runner.pha1 (kiểm rò nhãn ở mức giá trị, kiểm bản ghi), có móc. Trả (rec, cap)."""
    p = runner._params(ch, ca)
    cam = sorted({ca['opaque_id']} | ({ca['case_dir']} if ca.get('case_dir') else set())
                 | {x for x in (ca.get('chuoi_cam') or []) if x})
    vp = hop_dong.vi_pham_gia_tri(p, ca.get('aliases') or {}, ca.get('inventory') or [], cam)
    if vp:
        raise runner.LoiRoNhan(f'chuỗi cấm trong đầu vào: {sorted(set(x[0] for x in vp))}')
    with Moc(cache, dem_cong) as m:
        rec = chuoi.chay(ca['spans'], ca.get('metrics') or [], ca.get('logs') or [], ca.get('inventory') or [],
                         ca.get('aliases') or {}, t, p)
    hop_dong.kiem_ban_ghi(rec)
    return rec, m.cap, p


def json_ban_ghi(rec, oid):
    return runner._json(dict(rec, opaque_id=oid))


# ---------------------------------------------------------------- bảng phép kiểm

def _moc_metric(ca, p, t_ns):
    """Mốc thời gian (ns) của mẫu N, A theo từng cột metric, đúng cách chuoi._chay dựng (thứ tự hàng)."""
    metrics = ca.get('metrics') or []
    dv = p['don_vi_thoi_gian']
    he_m = chuoi._he_so_ns(dv['metrics.time'])
    lo, hi = t_ns - NUA * NS, t_ns + NUA * NS
    tg = quan_sat.thoi_gian_nguon_metric(dict(p, nguon_metric=(p.get('nguon_metric') or {})),
                                         [int(r['time'] * he_m) for r in metrics])
    out = {}
    if not metrics:
        return out
    cols = sorted({k for r in metrics for k in r if k != 'time'})
    for cot in cols:
        ng = (p.get('nguon_metric') or {}).get(cot)
        if ng is None:
            continue
        tt = tg[ng]
        moc = tt['moc'] if tt['trang_thai'] == 'OK' else [int(r['time'] * he_m) for r in metrics]
        N, A, mN, mA = [], [], [], []
        for r, mc in zip(metrics, moc):
            v = r.get(cot)
            if v is None or not math.isfinite(v) or not (lo <= mc < hi):
                continue
            if mc < t_ns:
                N.append(v)
                mN.append(int(mc))
            else:
                A.append(v)
                mA.append(int(mc))
        out[f'metric|{cot}'] = (N, mN, A, mA, cot)
    return out


def bien_don_vi(rec, p, ma, t_ns):
    """Biên phía cho chia khối (SPEC A3 điểm 3, sửa 17:52 và 20:44): N từ max(t − 300, H₀ làm tròn xuống ô 10 giây, F₀),
    A tới min(t + 300, H₁ làm tròn lên ô 10 giây, F₁); H, F là bao bản ghi và khoảng ghi của nguồn của đơn vị trong bản
    ghi chuỗi (`coverage.<nguồn>`). Nguồn: trace cho thao tác, cạnh; nguồn metric của cột cho metric. Không có H, F
    thì giữ 300 giây."""
    lo, hi = t_ns - NUA * NS, t_ns + NUA * NS
    if ma.startswith('metric|'):
        nguon = (p.get('nguon_metric') or {}).get(ma.split('|', 1)[1])
    else:
        nguon = 'trace'
    q = (rec.get('coverage') or {}).get(nguon) or {}
    H, F = q.get('H'), q.get('F')
    goc = lo
    o = 10 * NS  # ô 10 giây của B1.3b, gốc ở đầu miền; làm tròn H ra ngoài (N4: mép bản ghi lệch vài ms không được bớt khối)
    if H:
        lo2 = goc + ((int(H[0]) - goc) // o) * o
        hi2 = goc + -((goc - int(H[1])) // o) * o
        lo, hi = max(lo, lo2), min(hi, hi2)
    if F:
        lo, hi = max(lo, int(F[0])), min(hi, int(F[1]))
    return lo, hi


def bang_phep(ca, t, p, rec, cap, tinh_cong=CONG, bo_dem_gio=None):
    """Bảng phép kiểm của một cửa sổ: đơn vị phân vị (p theo từng cổng) và đơn vị đếm (p nhị thức của chuỗi)."""
    import time as _t
    t_ns = int(round(t * NS))
    he_s = chuoi._he_so_ns(p['don_vi_thoi_gian']['spans.start_us'])
    aliases = ca.get('aliases') or {}
    U = set(chuoi._alias(aliases, x) for x in (ca.get('inventory') or []))
    ts = p['tham_so_E4']
    alpha = ts['alpha']
    moc = {}
    for (chu, op), m in cap['op'].items():
        moc[f'op|{chu}|{op}'] = (m['N'], [int(x * he_s) for x in m['moc_N']], m['A'], [int(x * he_s) for x in m['moc_A']],
                                 chu)
    for (a, b), m in cap['canh'].items():
        moc[f'canh|{a}|{b}'] = (m['N'], [int(x * he_s) for x in m['moc_N']], m['A'], [int(x * he_s) for x in m['moc_A']],
                                b)
    mm = _moc_metric(ca, p, t_ns)
    nhom_op = 'op_full' if p['bat_tat']['E1'] == 'tat' else 'op_excl'
    pv = []
    gio = {g: 0.0 for g in tinh_cong}
    for ma in sorted(cap['pv']):
        c = cap['pv'][ma]
        kq = c['kq']
        if ma.startswith('metric|'):
            N, mN, A, mA, cot = mm[ma]
            e = chuoi._ten_metric(cot, aliases)[0]
            nhom, nguon = 'metric', 'metric'
        else:
            N, mN, A, mA, e = moc[ma]
            nhom = nhom_op if ma.startswith('op|') else 'canh'
            nguon = 'trace'
        # mẫu móc được phải trùng mẫu chuỗi đưa vào E4 (thứ tự và giá trị)
        if [float(x) for x in N] != [float(x) for x in c['N']] or [float(x) for x in A] != [float(x) for x in c['A']]:
            raise RuntimeError(f'mẫu và mốc lệch: {ma}')
        dong = {'ma': ma, 'e': e, 'trong_U': e in U, 'nhom': nhom, 'nguon': nguon, 'huong_cham': c['huong_cham'],
                'trang_thai': kq['trang_thai'], 'hop_le': bool(kq['hop_le']), 'n_N': kq['n_N'], 'n_A': kq['n_A'],
                'huong': {}}
        if kq['trang_thai'] == 'OK':
            kb = None
            if 'G1' in tinh_cong or 'G3' in tinh_cong:
                bN, bA = bien_don_vi(rec, p, ma, t_ns)
                kb = cong.chuan_bi_khoi([float(x) for x in N], mN, [float(x) for x in A], mA, t_ns, bN, bA)
                dong['khoi'] = {k: kb.get(k) for k in ('roi_G0', 'b', 'cham_tran', 'so_o_N', 'so_khoi_N', 'so_khoi_A',
                                                         'rho_b', 'rho1')}
                dong['khoi']['phia_giay'] = [round((t_ns - bN) / NS, 3), round((bA - t_ns) / NS, 3)]
            for d in c['huong_cham']:
                h = {'p_G0': kq[f'p_{d}'], 'cach_G0': kq[f'cach_cong_{d}'], 'e_tho': kq[f'e_{d}_tho'],
                     'chenh_duong': kq[f'e_{d}_tho'] > 0, 'rA': kq[f'r_{d}_A'], 'rN': kq[f'r_{d}_N'],
                     'F_raw_G0': kq[f'F_raw_{d}']}
                assert h['F_raw_G0'] == int(h['p_G0'] < alpha and h['chenh_duong'])
                for g in tinh_cong:
                    if g == 'G0':
                        continue
                    if g == 'G4':
                        if nhom == 'metric':
                            t0 = _t.perf_counter()
                            r = cong.p_G4_metric([float(x) for x in N], mN, [float(x) for x in A], mA, t_ns, d, ts)
                            gio[g] += _t.perf_counter() - t0
                            h['p_G4'], h['cach_G4'], h['G4_phi'] = r['p'], r['cach'], r.get('phi')
                        else:
                            h['p_G4'], h['cach_G4'] = None, 'G3'  # đơn vị sự kiện: lấy p G3 khi ghép (B1)
                        continue
                    t0 = _t.perf_counter()
                    r = cong.p_theo_cong(g, [float(x) for x in N], mN, [float(x) for x in A], mA, t_ns, d, ts, ma, kb=kb)
                    gio[g] += _t.perf_counter() - t0
                    h[f'p_{g}'] = r['p']
                    h[f'cach_{g}'] = r['cach']
                    if g == 'G3' and r.get('chi_tiet'):
                        h['G3'] = {k: r['chi_tiet'][k] for k in ('cach', 'so_cach', 'dem_vuot')}
                dong['huong'][d] = h
        pv.append(dong)
    dem = []
    by_ma = {x['ma']: x for x in rec['worlds']['P']['don_vi_dem']}
    for ma in sorted(by_ma):
        x = by_ma[ma]
        u = cap['dem'].get(ma)
        if u is None:
            raise RuntimeError(f'không thấy đơn vị đếm trong móc: {ma}')
        e = u['thuc_the']
        dd = {'ma': ma, 'e': e, 'trong_U': e in U, 'nhom': u['nhom'], 'nguon': 'log',
              'huong_cham': list(u['huong_cham']), 'trang_thai': x['trang_thai'],
              'hop_le': x['trang_thai'] == 'OK', 'nhan': x['loai_thay_doi'],
              'p_len': x['p_len'], 'p_xuong': x['p_xuong'],
              'F_raw_len': x['F_raw_len'], 'F_raw_xuong': x['F_raw_xuong'], 'n_N': x['n_N'], 'n_A': x['n_A'],
              'T_N': x['T_N'], 'T_A': x['T_A']}
        if dd['hop_le'] and dd['nhan'] not in ('NEW_OP', 'STOPPED') and ma in cap['su_kien_N']:
            phi, so_o = cong.he_so_phan_tan(cap['su_kien_N'][ma], cap['h0'], t_ns)
            dd['D1_phi'], dd['D1_so_o'] = phi, so_o
            lam = Fraction(x['n_N']) * Fraction(x['T_A']) / Fraction(x['T_N'])
            dd['chenh_len_duong'] = (x['n_A'] - lam) > 0
            dd['chenh_xuong_duong'] = (lam - x['n_A']) > 0
            for d in ('len', 'xuong'):
                dd[f'p_D1_{d}'] = cong.p_D1(x['n_N'], x['n_A'], x['T_N'], x['T_A'], phi, d)
        dem.append(dd)
    FI = sorted({(k['don_vi'], k['huong'], k['F_I']) for k in rec['extra']['kenh_co_the_gioi']['P']})
    return {'pv': pv, 'dem': dem, 'F_I_G0': [list(x) for x in FI], 'U': sorted(U),
            'so_cham_hop_le': rec['diagnostics']['so_cham_hop_le'], 'verdict_chuoi': rec['verdict'],
            'alpha': alpha, 'gio_cong': gio}


# ---------------------------------------------------------------- verdict theo tổ hợp (R0: F_I = F_raw)

def co_theo_cong(bang, g, c='D0', nguong=None):
    """[(mã, hướng, F_raw)] của mọi phép hợp lệ, thực thể thuộc U, theo cổng phân vị g và cổng đếm c (bản 3, B1–B2).
    g: G0 | G1 | G3 | G4 | GE (GE: p của G4, ngưỡng theo ô). c: D0 (cờ của chuỗi) | D1 | DE (DE: p của D1, ngưỡng theo
    ô). nguong: {(nhóm, hướng): α_ô} của dataset của bảng, cho GE/DE; ô không có thì dùng α. NEW_OP, STOPPED tách
    riêng (cờ trực tiếp, giữ nguyên)."""
    alpha = bang['alpha']
    nguong = nguong or {}
    phep, truc_tiep = [], []
    for u in bang['pv']:
        if not (u['hop_le'] and u['trong_U']):
            continue
        for d, h in u['huong'].items():
            p = h['p_G4'] if g == 'GE' else h[f'p_{g}']
            a = nguong.get((u['nhom'], d), alpha) if g == 'GE' else alpha
            phep.append({'ma': u['ma'], 'd': d, 'p': p, 'F': int(p < a and h['chenh_duong']), 'loai': 'pv',
                         'nhom': u['nhom']})
    for u in bang['dem']:
        if not (u['hop_le'] and u['trong_U']):
            continue
        if u['nhan'] in ('NEW_OP', 'STOPPED'):
            d = 'len' if u['nhan'] == 'NEW_OP' else 'xuong'
            truc_tiep.append({'ma': u['ma'], 'd': d, 'F': int(u[f'F_raw_{d}']), 'nhan': u['nhan'], 'nhom': u['nhom']})
            continue
        for d in u['huong_cham']:
            if c == 'D0':
                phep.append({'ma': u['ma'], 'd': d, 'p': u[f'p_{d}'], 'F': int(u[f'F_raw_{d}']), 'loai': 'dem',
                             'nhom': u['nhom']})
                continue
            p = u[f'p_D1_{d}']
            a = nguong.get((u['nhom'], d), alpha) if c == 'DE' else alpha
            phep.append({'ma': u['ma'], 'd': d, 'p': p, 'F': int(p < a and u[f'chenh_{d}_duong']), 'loai': 'dem',
                         'nhom': u['nhom']})
    return phep, truc_tiep


def holm_bac(phep, alpha):
    """Tập (mã, hướng) bị bác ở thủ tục Holm bước xuống; ngưỡng chặt (p < α/(m − i)), như cổng qua khi p < α."""
    m = len(phep)
    bac = set()
    for i, x in enumerate(sorted(phep, key=lambda z: (z['p'], z['ma'], z['d']))):
        if x['p'] < alpha / (m - i):
            bac.add((x['ma'], x['d']))
        else:
            break
    return bac


def verdict_R0(bang, g, v, F_I=None, c='D0', nguong=None):
    """Verdict ở R0 (F_I = F_raw) cho tổ hợp (g, c, v). F_I: {(mã, hướng): 0/1} khi có E5 (không dùng ở R0)."""
    phep, tt = co_theo_cong(bang, g, c, nguong)
    fi = (lambda x: x['F']) if F_I is None else (lambda x: F_I.get((x['ma'], x['d']), 0) * x['F'])
    co = [x for x in phep if fi(x)]
    co_tt = [x for x in tt if fi(x)]
    if v == 'V0':
        cf = bool(co or co_tt)
    elif v == 'V3':
        cf = len({x['ma'] for x in co + co_tt}) >= 2
    elif v == 'V1':
        bac = holm_bac(phep, bang['alpha'])
        cf = any((x['ma'], x['d']) in bac for x in co) or bool(co_tt)
    elif v.startswith('V4:'):  # bản 4, C2 (sửa 15:01): tỷ lệ đơn vị có cờ trên đơn vị có phép hợp lệ >= q
        n = so_don_vi_hop_le(bang)
        cf = n > 0 and len({x['ma'] for x in co + co_tt}) / n >= float(v[3:])
    else:
        raise ValueError(v)
    if cf:
        return 'CAUSE_FOUND'
    return 'NO_INTRINSIC_ANOMALY' if bang['so_cham_hop_le'] > 0 else 'INSUFFICIENT_EVIDENCE'


def chi_nho_truc_tiep(bang, g, v, c='D0', nguong=None):
    """CAUSE_FOUND chỉ nhờ NEW_OP/STOPPED: bỏ các cờ đó thì không còn CAUSE_FOUND."""
    if verdict_R0(bang, g, v, c=c, nguong=nguong) != 'CAUSE_FOUND':
        return False
    b2 = dict(bang, dem=[u for u in bang['dem'] if u['nhan'] not in ('NEW_OP', 'STOPPED')])
    return verdict_R0(b2, g, v, c=c, nguong=nguong) != 'CAUSE_FOUND'


# ---------------------------------------------------------------- tiện ích tổng hợp

def wilson(k, n, z=1.959964):
    if not n:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - r) / d, 6), round((c + r) / d, 6)]


def nap_luot(luot):
    """{mã: nội dung tệp ca} của một lượt b3."""
    out = {}
    for f in sorted((Path(luot) / 'ca').glob('*.json')):
        out[f.stem] = json.loads(f.read_bytes().decode('utf-8'))
    return out


# ---------------------------------------------------------------- chạy chuỗi với cổng g (phát lại p)

def chay_voi_cong(ca, t, ch, g):
    """Chạy lần ghi (G0, móc) để có mẫu và mốc, tính bảng phép kiểm; nếu g khác G0, chạy lại chuỗi với cache phát lại
    p theo g cho mọi phép phân vị (kiểm mẫu trùng lần ghi). Trả (rec_g, bang, p, rec_G0)."""
    c0 = CacheMoc()
    rec0, cap, p = chay_chuoi(ca, t, ch, c0)
    bang = bang_phep(ca, t, p, rec0, cap)
    if g == 'G0':
        return rec0, bang, p, rec0
    tb = {}
    for u in bang['pv']:
        for d, h in u['huong'].items():
            k = (u['ma'], d)
            tb[k] = (h[f'p_{g}'], h[f'cach_{g}'], c0.ghi[k][2])
    for k, v in c0.ghi.items():  # phép của đơn vị không OK không gọi cache; mọi phép đã gọi phải có trong bảng
        if k not in tb:
            raise RuntimeError(f'thiếu p phát lại: {k}')
    rec_g, cap_g, _ = chay_chuoi(ca, t, ch, CacheMoc('phat', tb))
    return rec_g, bang, p, rec0


def F_I_tu_ban_ghi(rec):
    """{(mã đơn vị, hướng): 1} cho kênh có cờ và F_I = 1 ở thế giới P."""
    out = {}
    for k in rec['extra']['kenh_co_the_gioi']['P']:
        if k['F_I'] == 1 and k.get('don_vi'):
            out[(k['don_vi'], k['huong'])] = 1
    return out


# ---------------------------------------------------------------- GE, DE (bản 3, B1, B2)

LUOI_GE = (0.01, 0.005, 0.002, 0.001, 5e-4, 2e-4, 1e-4, 1e-5, 1e-6)


def chon_nguong(ps, alpha=0.01, luoi=LUOI_GE):
    """Giá trị lớn nhất trong lưới sao cho tỷ lệ p < ngưỡng <= alpha; None khi không có hoặc không có phép."""
    if not ps:
        return None
    n = len(ps)
    for a in sorted(luoi, reverse=True):
        if sum(1 for p in ps if p < a) / n <= alpha:
            return a
    return None



# ---------------------------------------------------------------- ghép lượt bản 3 (B5)

def nap_ghep(luot_cu, luot_moi):
    """Ghép bảng của lượt cũ (G0, G1, G3) với lượt bản 3 (G0, G4 cho metric; D1 cho đơn vị đếm). Kiểm: cùng ca, cùng
    cửa sổ, cùng sha256 bản ghi chuỗi, cùng tập phép; p G0 trùng; đơn vị đếm trùng p chuỗi. Đơn vị sự kiện: p_G4 = p_G3.
    Trả (ca, thong_ke_kiem)."""
    cu = nap_luot(luot_cu)
    moi = nap_luot(luot_moi)
    if set(cu) != set(moi):
        raise RuntimeError('hai lượt khác tập ca')
    kiem = {'cua_so': 0, 'phep_pv': 0, 'phep_dem': 0, 'G4_lay_G3': 0}
    for oid, x in cu.items():
        y = moi[oid]
        if set(x['cua_so']) != set(y['cua_so']):
            raise RuntimeError(f'khác cửa sổ: {oid}')
        for k, w in x['cua_so'].items():
            w2 = y['cua_so'][k]
            if w['sha256_ban_ghi'] != w2['sha256_ban_ghi']:
                raise RuntimeError(f'bản ghi chuỗi khác giữa hai lượt: {oid} {k}')
            kiem['cua_so'] += 1
            b, b2 = w['bang'], w2['bang']
            pv2 = {u['ma']: u for u in b2['pv']}
            for u in b['pv']:
                u2 = pv2[u['ma']]
                if set(u['huong']) != set(u2['huong']):
                    raise RuntimeError(f'khác tập hướng: {u["ma"]}')
                for d, h in u['huong'].items():
                    h2 = u2['huong'][d]
                    if h['p_G0'] != h2['p_G0']:
                        raise RuntimeError(f'p G0 khác: {oid} {k} {u["ma"]} {d}')
                    if u['nhom'] == 'metric':
                        h['p_G4'], h['cach_G4'], h['G4_phi'] = h2['p_G4'], h2['cach_G4'], h2.get('G4_phi')
                    else:
                        h['p_G4'], h['cach_G4'] = h['p_G3'], 'G3:' + h['cach_G3']
                        kiem['G4_lay_G3'] += 1
                    kiem['phep_pv'] += 1
            dem2 = {u['ma']: u for u in b2['dem']}
            if set(dem2) != {u['ma'] for u in b['dem']}:
                raise RuntimeError(f'khác tập đơn vị đếm: {oid} {k}')
            b['dem'] = []
            for ma in sorted(dem2):
                u2 = dem2[ma]
                b['dem'].append(u2)
                kiem['phep_dem'] += 1
    return cu, kiem



# ---------------------------------------------------------------- chạy với bộ cổng khóa (bản 3, sau khóa)

def dien_G4(bang):
    """Đơn vị sự kiện: p_G4 = p_G3 (B1)."""
    for u in bang['pv']:
        if u['nhom'] != 'metric':
            for h in u['huong'].values():
                if 'p_G3' in h:
                    h['p_G4'], h['cach_G4'] = h['p_G3'], 'G3:' + h['cach_G3']
    return bang


def chay_voi_bo(ca, t, ch, g, c, nguong, alpha=0.01):
    """Lần ghi (G0, D0) có móc để có mẫu, mốc, bảng phép; nếu bộ khác (G0, D0) thì chạy lại chuỗi: p phân vị phát lại
    theo g (GE: p_G4 nhân α/α_ô, để p' < α tương đương p < α_ô), cờ đếm thay theo c. nguong: {(nhóm, hướng): α_ô} của
    dataset (GE và DE dùng chung bảng; khóa nhóm không trùng). Trả (rec_bo, bang, p, rec_G0)."""
    can = {'G0'}
    if g == 'G1':
        can.add('G1')
    if g in ('G3', 'G4', 'GE'):
        can.add('G3')
    if g in ('G4', 'GE'):
        can.add('G4')
    c0 = CacheMoc()
    rec0, cap, p = chay_chuoi(ca, t, ch, c0)
    bang = dien_G4(bang_phep(ca, t, p, rec0, cap, tinh_cong=tuple(x for x in ('G0', 'G1', 'G3', 'G4') if x in can)))
    if g == 'G0' and c == 'D0':
        return rec0, bang, p, rec0
    tb = {}
    for u in bang['pv']:
        for d, h in u['huong'].items():
            k = (u['ma'], d)
            if g == 'GE':
                a = nguong.get((u['nhom'], d), alpha)
                pp = min(1.0, h['p_G4'] * alpha / a)
            else:
                pp = h[f'p_{g}']
            tb[k] = (pp, 'phat_' + g, c0.ghi[k][2])
    for k in c0.ghi:
        if k not in tb:
            raise RuntimeError(f'thiếu p phát lại: {k}')
    dc = None if c == 'D0' else {'c': c, 'nguong': nguong, 'alpha': alpha, 't_ns': int(round(t * NS))}
    rec_g, _, _ = chay_chuoi(ca, t, ch, CacheMoc('phat', tb), dc)
    return rec_g, bang, p, rec0



def so_don_vi_co(bang, g, c='D0', nguong=None):
    """Số đơn vị khác nhau có cờ (F_I = F_raw ở R0), gồm NEW_OP, STOPPED; dùng cho V4."""
    phep, tt = co_theo_cong(bang, g, c, nguong)
    return len({x['ma'] for x in phep if x['F']} | {x['ma'] for x in tt if x['F']})



def so_don_vi_hop_le(bang):
    """Số đơn vị khác nhau (thực thể thuộc U) có ít nhất một phép chấm hợp lệ (phân vị hoặc đếm, kể cả NEW_OP, STOPPED)."""
    return len({u['ma'] for u in bang['pv'] if u['hop_le'] and u['trong_U']}
               | {u['ma'] for u in bang['dem'] if u['hop_le'] and u['trong_U']})

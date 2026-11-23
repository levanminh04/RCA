# -*- coding: utf-8 -*-
"""T-069 bước 6 — chấm ca mới bằng bộ chấm T-064 (không sửa) và lập bảng theo ô theo results/T-069/tieu-chi.json.
Dùng: D:/RCA-flashticket/.venv/Scripts/python.exe -B results/T-069/bang_theo_o.py <lượt chính> [<lượt chính 2> ...] [--lap <lượt lặp>]
Đầu vào (đã nhận bằng nhan_luot.py, đã xác nhận bằng xac-nhan/*.py):
  results/T-069/thu/<lượt>/so.jsonl, chay/nhat-ky-3.jsonl; results/T-069/xac-nhan/<lượt>-thu2.json, <lượt>-thu3.json;
  results/T-069/dau-ra/dev3/d0/<bản>/<mã>/ (method-output-1.json + summary.json, hoặc loi-chay.json).
Ra: results/T-069/tap-moi.json, cham/spec-moi.json, cham/cham-moi-A.json (+ .txt), bang-theo-o.json, bang-theo-o.md.
Quy tắc (khai trước, tieu-chi.json): hạng = hang_cat; tụt = mới > cũ + 1; ghép được = đạt điều kiện xác nhận của nhóm ca cũ
và có đầu ra; D1–D5 trên tập ghép được, số cũ tính lại trên đúng tập đó; D1–D5 theo lần thu chính, lần lặp chỉ xếp nhóm (c)."""
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); T = R / 'results/T-064'; Q = R / 'results/T-069'
a = sys.argv[1:]
LAP = a[a.index('--lap') + 1] if '--lap' in a else None
CHINH = [x for i, x in enumerate(a) if x != '--lap' and (i == 0 or a[i - 1] != '--lap')]
TC = json.loads((Q / 'tieu-chi.json').read_text(encoding='utf-8'))
spec_ = importlib.util.spec_from_file_location('cham_dev3_t064', T / 'cham/cham_dev3.py')
C = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(C)
cham = C.cham
BAN = {'V082': 'V082-V066+H8a', 'P7': 'P7'}
DR = Q / 'dau-ra/dev3/d0'


def doc_luot(L):
    G = Q / 'thu' / L
    so = [json.loads(l) for l in (G / 'so.jsonl').read_text(encoding='utf-8').splitlines()]
    nk = [json.loads(l) for l in (G / 'chay/nhat-ky-3.jsonl').read_text(encoding='utf-8').splitlines()]
    xn = {}
    for g in ('thu2', 'thu3'):
        f = Q / 'xac-nhan' / f'{L}-{g}.json'
        xn[g] = json.loads(f.read_text(encoding='utf-8'))['ca'] if f.exists() else {}
    ca = []
    for d in so:
        if d['event'] != 'cycle-begin': continue
        oid = d['opaque_id']; ev = [x['event'] for x in so if x.get('opaque_id') == oid]
        # mã có đầu ra: ưu tiên mã gốc nếu có thư mục đầu ra V082 hoặc P7, rồi mã stage lại theo nhật ký
        ung = [oid] + [x['id'] for x in nk if x['msg'] in ('M1 xong', 'V082 xong') and x.get('goc', '') == oid and x['id'] != oid]
        ma = next((m for m in ung if any((DR / b / m).exists() for b in BAN.values())), oid)
        ca.append({'luot': L, 'oid': oid, 'ma': ma, 'o': d['cell'], 'su_kien': ev, 'xac_nhan': {g: xn[g].get(oid) for g in xn},
                   'nhat_ky_m1': [{k: x.get(k) for k in ('t', 'msg', 'id', 'lan', 'status', 'deterministic', 'verdict', 'trung_sha', 'err')}
                                  for x in nk if x['msg'].startswith(('M1', 'V082', 'sau V082')) and (x.get('id', '').startswith(oid) or x.get('goc') == oid)]})
    return ca


def cham_mot(ban, ma, c):
    rec, sh, nguon = C.tim(ban, ma, 0)
    if c['loai'] == 'loi':
        r = cham.cham_ca_loi(cham.chieu_canh_ve_nut(rec), c['tap_chap_nhan'])
        return {'status': rec.get('status'), 'verdict': rec.get('verdict'), 'hang_cat': r['hang_cat'], 'hang_ky_vong': r['hang_ky_vong'],
                'p1': r['p1'], 'p3': r['p3'], 'nhom_hang_1': cham.nhom_hang_1(rec) if rec.get('status') == 'OK' else [],
                'sha256': sh, 'nguon': nguon, '_r': r}
    r = cham.cham_ca_khong_loi(rec)
    return {'status': rec.get('status'), 'verdict': rec.get('verdict'), 'k': r['k'],
            'nhom_hang_1': cham.nhom_hang_1(rec) if rec.get('status') == 'OK' else [], 'sha256': sh, 'nguon': nguon}


def summary(ban, ma):
    f = DR / ban / ma / 'summary.json'
    return json.loads(f.read_text(encoding='utf-8')) if f.exists() else None


# --- ca mới của lượt chính, ghép với cặp khai trước
moi = [x for L in CHINH for x in doc_luot(L)]
C.UU[:] = ['../T-069/dau-ra']
dem = {}
hang = []
for cp in TC['cap_ca']:
    o = cp['o']; cung = [x for x in moi if x['o'] == o]
    k = dem.get(o, 0); dem[o] = k + 1
    x = cung[k] if k < len(cung) else None
    nhom = 'thu2' if cp['cu']['nhom_thu'].startswith('thu2') else 'thu3'
    row = {'o': o, 'loai': cp['loai'], 'ma_cu': cp['cu']['ma'], 'nhom_thu_cu': nhom,
           'cu': {b: {kk: cp['cu'][b].get(kk) for kk in ('status', 'hang_cat', 'p1', 'p3', 'k', 'verdict', 'sha256')} for b in BAN}}
    if x is None:
        row.update(ghep_duoc=False, ly_do=['chưa thu']); hang.append(row); continue
    xn = x['xac_nhan'][nhom] or {}
    row.update(luot=x['luot'], oid=x['oid'], ma_moi=x['ma'], su_kien=x['su_kien'], nhat_ky_m1=x['nhat_ky_m1'],
               xac_nhan={'script': f'xac_nhan_ca{"" if nhom == "thu2" else "_3"}.py', 'xac_nhan': xn.get('xac_nhan'),
                         'khong_du_du_lieu': xn.get('khong_du_du_lieu'), 'ly_do': xn.get('ly_do'), 'dieu_kien': xn.get('dieu_kien')})
    row['moi'] = {k: cham_mot(b, x['ma'], cp) for k, b in BAN.items()}
    sv, sp = summary(BAN['V082'], x['ma']), summary('P7', x['ma'])
    row['trung_sha_V082'] = sv.get('trung_sha') if sv else None
    row['lap_trung_P7'] = sp.get('deterministic_repeat') if sp else None
    ly = []
    tco = Q / 'thu' / x['luot'] / 'tai-create-order.json'  # phụ lục tieu-chi-bo-sung.json: chu kỳ phải có create_order 201
    if tco.exists():
        n201 = json.loads(tco.read_text(encoding='utf-8')).get(x['oid'], {}).get('201', 0)
        row['create_order_201'] = n201
        if not n201: ly.append('tải mua vé không hoạt động (create_order 201 = 0)')
    if xn.get('xac_nhan') is not True: ly.append('không xác nhận can thiệp' + (' (thiếu dữ liệu)' if xn.get('khong_du_du_lieu') else ''))
    if row['moi']['V082']['status'] == 'MISSING': ly.append('thiếu đầu ra V082')
    if row['moi']['P7']['status'] == 'MISSING': ly.append('thiếu đầu ra/lỗi chạy P7 chưa ghi')
    if sv and sv.get('trung_sha') is not True: ly.append('V082 hai lần chạy không trùng SHA')
    if sp and sp.get('deterministic_repeat') is not True: ly.append('P7 hai lần chạy không trùng SHA')
    row['ghep_duoc'] = not ly; row['ly_do'] = ly
    if cp['loai'] == 'loi':
        for b in BAN:
            row[f'delta_{b}'] = row['moi'][b]['hang_cat'] - row['cu'][b]['hang_cat']
        row['tut_V082'] = row['delta_V082'] > 1
        row['doi_hang'] = row['delta_V082'] != 0 or row['delta_P7'] != 0
        row['nhom'] = ('a' if row['delta_V082'] > 0 and row['delta_P7'] > 0 else 'b' if row['delta_V082'] > 0 else None)
    else:
        row['dk_V082'] = row['moi']['V082']['k'] - row['cu']['V082']['k']
        row['dk_P7'] = row['moi']['P7']['k'] - row['cu']['P7']['k']
    hang.append(row)

# --- lần lặp (nếu có): ghép theo ô và thứ tự
if LAP:
    lap = doc_luot(LAP); C.UU[:] = ['../T-069/dau-ra']; dl = {}
    for x in lap:
        cand = [r for r in hang if r['o'] == x['o'] and 'lap' not in r and r.get('ma_moi')]
        if not cand: continue
        r = cand[0]; cp = next(c for c in TC['cap_ca'] if c['cu']['ma'] == r['ma_cu'])
        nhom = r['nhom_thu_cu']; xn = x['xac_nhan'][nhom] or {}
        r['lap'] = {'luot': LAP, 'oid': x['oid'], 'ma': x['ma'], 'xac_nhan': xn.get('xac_nhan'), 'ly_do_xn': xn.get('ly_do'),
                    'moi': {k: {kk: v for kk, v in cham_mot(b, x['ma'], cp).items() if kk != '_r'} for k, b in BAN.items()}}
        if cp['loai'] == 'loi':
            hv = r['lap']['moi']['V082']['hang_cat']; hc = r['cu']['V082']['hang_cat']
            if r['lap']['xac_nhan'] is True and hc - 1 <= hv <= hc + 1 and r.get('delta_V082', 0) > 0:
                r['nhom'] = (r['nhom'] or '') + '+c' if r.get('nhom') else 'c'

# --- tổng trên tập ghép được
def tong(rows, phia, b):
    loi = {r['ma_cu']: (r['cu'][b] if phia == 'cu' else r['moi'][b]) for r in rows if r['loai'] == 'loi'}
    t = {'n': len(loi), 'AC@1': sum(v['p1'] for v in loi.values()), 'AC@3': sum(v['p3'] for v in loi.values()),
         'tong_hang_cat': sum(v['hang_cat'] for v in loi.values())}
    kl = [r for r in rows if r['loai'] != 'loi']
    t['K'] = sum((r['cu'][b] if phia == 'cu' else r['moi'][b])['k'] for r in kl); t['so_ca_khong_loi'] = len(kl)
    return t


gd = [r for r in hang if r['ghep_duoc']]
TONG = {f'{b}_{p}': tong(gd, p, b) for b in BAN for p in ('cu', 'moi')}
v_c, v_m, p_m = TONG['V082_cu'], TONG['V082_moi'], TONG['P7_moi']
loi_v082 = [r['ma_moi'] for r in gd if r['moi']['V082']['status'] not in ('OK',)]
D = {
    'D1': v_m['AC@3'] < v_c['AC@3'] - 1e-9,
    'D2': v_c['AC@1'] - v_m['AC@1'] >= 2 - 1e-9,
    'D3': v_m['AC@1'] < p_m['AC@1'] - 1e-9 or v_m['AC@3'] < p_m['AC@3'] - 1e-9 or v_m['tong_hang_cat'] > p_m['tong_hang_cat'] + 1e-9,
    'D4_ung_vien': loi_v082,
    'D5': v_m['K'] - v_c['K'] >= 2,
}
D['D4'] = bool(loi_v082)  # phân loại hạ tầng/không hạ tầng ghi tay trong bảng .md sau khi đọc nhật ký
# ứng viên lặp theo quy tắc khai trước
loi_doi = [r for r in gd if r['loai'] == 'loi' and r['doi_hang']]
thu_tu = {c['o'] + c['cu']['ma']: i for i, c in enumerate(TC['cap_ca'])}
k1 = sorted([r for r in loi_doi if r['tut_V082']], key=lambda r: -r['delta_V082'])
k2 = sorted([r for r in loi_doi if not r['tut_V082'] and r['delta_V082'] != 0], key=lambda r: -abs(r['delta_V082']))
k3 = sorted([r for r in loi_doi if r['delta_V082'] == 0 and r['delta_P7'] != 0], key=lambda r: -abs(r['delta_P7']))
k4 = [r for r in gd if r['loai'] != 'loi' and r['dk_V082'] > 0] if D['D5'] else []
lap_ds = [(r['o'], r['ma_cu']) for r in (k1 + k2 + k3 + k4)][:4]

ket = {'luot_chinh': CHINH, 'luot_lap': LAP, 'tieu_chi_sha256': hashlib.sha256((Q / 'tieu-chi.json').read_bytes()).hexdigest(),
       'so_o': len(hang), 'ghep_duoc': len(gd), 'tong_tren_tap_ghep_duoc': TONG, 'dieu_kien_dung': D,
       'o_can_lap_theo_quy_tac': lap_ds, 'o_can_lap_vuot_4': max(0, len(k1 + k2 + k3 + k4) - 4),
       'hang': [{k: (v if k not in ('moi',) else {b: {kk: vv for kk, vv in x.items() if kk != '_r'} for b, x in v.items()})
                 for k, v in r.items()} for r in hang]}
(Q / 'bang-theo-o.json').write_bytes((json.dumps(ket, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))

# --- chấm bằng cham_dev3.py nguyên bản trên tập ca mới (đối chiếu tổng; bộ chấm không sửa)
tap = {'muc_dich': 'T-069: ca mới trên bản ghim (chấm bằng cham_dev3.py T-064, không sửa)',
       'ca': [{'ma': r['ma_moi'], 'o': r['o']} for r in hang if r.get('ma_moi')]}
(Q / 'tap-moi.json').write_bytes((json.dumps(tap, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
sp = {'tap': {'moi': 'results/T-069/tap-moi.json'}, 'ban': ['P7', 'V082-V066+H8a'], 'cap': [['P7', 'V082-V066+H8a']],
      'goc_uu_tien': ['../T-069/dau-ra']}
(Q / 'cham').mkdir(exist_ok=True)
(Q / 'cham/spec-moi.json').write_bytes((json.dumps(sp, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
rc = subprocess.run([sys.executable, '-B', str(T / 'cham/cham_dev3.py'), str(Q / 'cham/spec-moi.json'), str(Q / 'cham/cham-moi-A.json')],
                   capture_output=True, text=True, encoding='utf-8', cwd=str(R))
(Q / 'cham/cham-moi-A.txt').write_bytes(rc.stdout.encode('utf-8'))
if rc.returncode != 0: print('cham_dev3 lỗi:', rc.stderr[-500:])

# --- bảng .md
def f(x): return '–' if x is None else (f'{x:g}' if isinstance(x, (int, float)) else str(x))
md = ['# T-069 — bảng theo ô (sinh bằng `bang_theo_o.py`; nguồn số: `bang-theo-o.json`)', '',
      f'Lượt chính: {", ".join(CHINH)}' + (f'; lượt lặp: {LAP}' if LAP else '') + f'. Tiêu chí: `tieu-chi.json` (sha256 `{ket["tieu_chi_sha256"][:12]}…`).', '',
      '| Ô | Mã cũ → mới | Ghép được | V082 cũ → mới | P7 cũ → mới | Tụt V082 | Nhóm | V082 verdict mới | trung_sha V082 / lặp P7 | Lần lặp V082/P7 |',
      '|---|---|---|---|---|---|---|---|---|---|']
for r in hang:
    if r['loai'] == 'loi':
        vc, vm = r['cu']['V082']['hang_cat'], r.get('moi', {}).get('V082', {}).get('hang_cat')
        pc, pm = r['cu']['P7']['hang_cat'], r.get('moi', {}).get('P7', {}).get('hang_cat')
        tut = f(r.get('tut_V082'))
    else:
        vc, vm = f"k={r['cu']['V082']['k']}", f"k={r.get('moi', {}).get('V082', {}).get('k')}"
        pc, pm = f"k={r['cu']['P7']['k']}", f"k={r.get('moi', {}).get('P7', {}).get('k')}"
        tut = '–'
    lp = r.get('lap')
    lps = '–' if not lp else (f"{f(lp['moi']['V082'].get('hang_cat', lp['moi']['V082'].get('k')))}/{f(lp['moi']['P7'].get('hang_cat', lp['moi']['P7'].get('k')))}"
                              + ('' if lp['xac_nhan'] else ' (không xác nhận)'))
    md.append(f"| {r['o']} | {r['ma_cu']} → {r.get('ma_moi', '–')} | {'có' if r['ghep_duoc'] else 'không: ' + '; '.join(r['ly_do'])} | "
              f"{f(vc)} → {f(vm)} | {f(pc)} → {f(pm)} | {tut} | {f(r.get('nhom'))} | {f(r.get('moi', {}).get('V082', {}).get('verdict'))} | "
              f"{f(r.get('trung_sha_V082'))} / {f(r.get('lap_trung_P7'))} | {lps} |")
md += ['', f'**Tổng trên {len(gd)} ô ghép được** (AC@1, AC@3 trên {v_c["n"]} ô lỗi; K trên {v_c["so_ca_khong_loi"]} ô không lỗi):', '',
       '| Bản | AC@1 | AC@3 | Tổng hạng cắt | K |', '|---|---|---|---|---|']
for k, v in TONG.items():
    md.append(f"| {k} | {f(v['AC@1'])} | {f(v['AC@3'])} | {f(v['tong_hang_cat'])} | {f(v['K'])} |")
md += ['', '**Điều kiện dừng:** ' + ', '.join(f'{k} = {f(v)}' for k, v in D.items()), '',
       f'**Ô cần lặp theo quy tắc khai trước:** {lap_ds or "không có"}' + (f' (vượt 4: {ket["o_can_lap_vuot_4"]})' if ket['o_can_lap_vuot_4'] else ''), '',
       f'Đối chiếu `cham_dev3.py` nguyên bản: `cham/cham-moi-A.txt` — {rc.stdout.strip()}']
(Q / 'bang-theo-o.md').write_bytes(('\n'.join(md) + '\n').encode('utf-8'))
print('\n'.join(md))

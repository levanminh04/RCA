# -*- coding: utf-8 -*-
"""Chạy M1-FT một bản trên một ca (trên exp-obs, user rca, venv P7 — WHY-81). Hai lần, kiểm trùng SHA.

  python -B chay_ca.py --id <mã mờ> --cau-hinh <file.json> --ban <mã biến thể> --ra <thư mục> [--goc /opt/flash-ticket-rca]
Đọc: <goc>/outputs/<id>/method-input.json (đầu vào P7 đã ghim) và, khi cấu hình cần, <goc>/cases/<id>/raw-traces.jsonl
+ request.json (chỉ lấy t). Ghi: <ra>/<id>/method-output-{1,2}.json, summary.json. Không đọc sổ tiêm lỗi/nhãn.

Kiểm độ nhạy mốc (phiên C, 14/11): `--doi-t d` (giây, mặc định 0). d ≠ 0: dựng lại đầu vào từ gói ca với t' = t + d bằng
đường của runner ghim (`m1_ft.doi_moc`), mọi nơi dùng t đều dùng t' (inputs[5], cửa sổ cắt span/log/metric của M1,
`span_phu`, H5b). Gói metric bổ sung phải xuất quanh t' (`t` của gói = t'); ngoại lệ `--bo-sung-t-goc`: cho dùng gói quanh
t gốc chỉ khi không kênh nào của gói mà cấu hình dùng có dữ liệu (chứng minh không ảnh hưởng, ghi vào summary).
d = 0 và không `--dung-lai-dau-vao`: đường cũ, đầu ra và summary như trước.
"""
import argparse, hashlib, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
_SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SRC))
from m1 import hop_dong  # noqa: E402
from m1.adapter_flashticket import jsonl  # noqa: E402
from m1_ft import chay as ft, bo_sung as bs  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--id', required=True); ap.add_argument('--cau-hinh', required=True); ap.add_argument('--ban', required=True)
ap.add_argument('--ra', required=True); ap.add_argument('--goc', default='/opt/flash-ticket-rca')
ap.add_argument('--bo-sung', default='/opt/rca-m1ft/bo-sung/{id}/prometheus-bo-sung.json', help='gói metric bổ sung của ca')
ap.add_argument('--doi-t', type=int, default=0, help='dời mốc t (giây) để kiểm độ nhạy mốc; 0 = như cũ')
ap.add_argument('--dung-lai-dau-vao', action='store_true', help='dựng lại đầu vào từ gói ca (tự bật khi --doi-t ≠ 0)')
ap.add_argument('--cau-hinh-p7', default=None, help='cấu hình khóa P7; mặc định <goc>/m1-p7-config.json')
ap.add_argument('--bo-sung-t-goc', action='store_true', help='cho dùng gói bổ sung quanh t gốc khi kênh dùng tới rỗng')
ap.add_argument('--dem-dau-vao', default=None, help='thư mục bộ đệm đầu vào dựng lại <dir>/<id>/d<d>/ (kiểm hash khi đọc)')
a = ap.parse_args()
if not a.id.isalnum(): raise SystemExit('mã ca phải là mã mờ')
goc = Path(a.goc)
cau_hinh = json.loads(Path(a.cau_hinh).read_text(encoding='utf-8'))
dung_lai = a.dung_lai_dau_vao or a.doi_t != 0
moc = None  # thông tin truy vết của phép dời mốc (chỉ khi dựng lại)
t0 = time.monotonic()
# H8-adapter (phiên C): biến đổi gói metric ghim TRƯỚC adapter. Nếu biến đổi không đổi gói (không có nhóm cần nối) thì
# đầu vào trùng đầu vào không bật → dùng đường thường (method-input đã lưu hoặc bộ đệm). Nếu đổi: bắt buộc dựng lại, không
# dùng bộ đệm (đầu vào khác bản không bật).
tf = [tp for tp in ft.tao_thanh_phan(cau_hinh) if hasattr(tp, 'bien_doi_goi_ghim')]
h8a = None
if tf:
    _b = json.loads((goc / 'cases' / a.id / 'prometheus.json').read_text(encoding='utf-8'))
    _inv = json.loads((goc / 'cases' / a.id / 'inventory.json').read_text(encoding='utf-8'))
    _m = _b
    for tp in tf:
        _m = tp.bien_doi_goi_ghim(_m, _inv)
    h8a = {'doi_goi': ft.canonical(_m) != ft.canonical(_b), 'chan_doan': [tp.cd['goi_ghim'] for tp in tf]}
    if h8a['doi_goi']:
        dung_lai, a.dem_dau_vao = True, None
    del _b, _m
if not dung_lai:
    inputs = json.loads((goc / 'outputs' / a.id / 'method-input.json').read_text(encoding='utf-8'))
    t_goc = inputs[5]
else:
    from m1_ft import doi_moc
    t_goc = json.loads((goc / 'cases' / a.id / 'request.json').read_text(encoding='utf-8'))['t']
    p7_path = Path(a.cau_hinh_p7) if a.cau_hinh_p7 else goc / 'm1-p7-config.json'
    p7_bytes = p7_path.read_bytes()
    dem = Path(a.dem_dau_vao) / a.id / f'd{a.doi_t}' if a.dem_dau_vao else None
    if dem is not None and (dem / 'moc.json').exists():
        # bộ đệm: dùng lại đầu vào đã dựng cho (ca, d) — chỉ khi hash file khớp hash ghi lúc dựng và cùng cấu hình P7
        moc = json.loads((dem / 'moc.json').read_text(encoding='utf-8'))
        raw = (dem / 'method-input.json').read_bytes()
        if hashlib.sha256(raw).hexdigest() != moc['input_sha256'] or \
                moc['cau_hinh_p7_sha256'] != hashlib.sha256(p7_bytes).hexdigest() or moc['t_goc'] != t_goc:
            raise SystemExit('bộ đệm đầu vào lệch hash/cấu hình')
        inputs, ser = json.loads(raw), None
        moc['tu_bo_dem'] = True
    else:
        bd = None
        if h8a and h8a['doi_goi']:
            def bd(bundles, inv):
                for tp in tf:
                    bundles = tp.bien_doi_goi_ghim(bundles, inv)
                return bundles
        inputs, moc, ser = doi_moc.dung_dau_vao(goc / 'cases' / a.id, a.id, t_goc + a.doi_t, json.loads(p7_bytes), bd)
        moc.update({'doi_t': a.doi_t, 't_goc': t_goc, 'cau_hinh_p7_sha256': hashlib.sha256(p7_bytes).hexdigest()})
        if dem is not None:  # ghi nguyên tử: file tạm rồi đổi tên; moc.json ghi sau cùng
            dem.mkdir(parents=True, exist_ok=True)
            tam = dem / f'method-input.json.tam{a.ban.replace("/", "_")}'
            tam.write_bytes((ser + '\n').encode('utf-8')); tam.replace(dem / 'method-input.json')  # byte: không đổi \n
            tm = dem / f'moc.json.tam{a.ban.replace("/", "_")}'
            tm.write_bytes((json.dumps(moc, ensure_ascii=False) + '\n').encode('utf-8')); tm.replace(dem / 'moc.json')
        moc = dict(moc, tu_bo_dem=False)
    luu = goc / 'outputs' / a.id / 'method-input.json'
    if a.doi_t == 0 and luu.exists() and not (h8a and h8a['doi_goi']):
        # phép kiểm đường dựng lại: phải trùng byte method-input.json đã lưu của P7
        moc['trung_method_input_goc'] = hashlib.sha256(luu.read_bytes()).hexdigest() == moc['input_sha256']
    del ser
if hop_dong.vi_pham_truong_cam(inputs): raise SystemExit('trường cấm trong đầu vào')
t_m1 = inputs[5]
if t_m1 != t_goc + a.doi_t: raise SystemExit('t của đầu vào khác t gốc + doi_t')
can = ft.can_bo_sung(cau_hinh); them = {}
if 'span_phu' in can:
    t_req = json.loads((goc / 'cases' / a.id / 'request.json').read_text(encoding='utf-8'))['t']
    if t_req + a.doi_t != t_m1: raise SystemExit('t của request (+ doi_t) khác t trong method-input')
    them['span_phu'] = bs.span_phu(jsonl([goc / 'cases' / a.id / 'raw-traces.jsonl']), t_m1)
    if hop_dong.vi_pham_truong_cam([them]): raise SystemExit('trường cấm trong bo_sung')
if 'bundles' in can:
    them['bundles'] = json.loads((goc / 'cases' / a.id / 'prometheus.json').read_text(encoding='utf-8'))
    if hop_dong.vi_pham_truong_cam([them['bundles']]): raise SystemExit('trường cấm trong bundles')
if 'log_phu' in can:
    them['log_phu'] = bs.log_phu(jsonl([goc / 'cases' / a.id / 'raw-logs.jsonl']), t_m1)
    if hop_dong.vi_pham_truong_cam([them['log_phu']]): raise SystemExit('trường cấm trong log_phu')
if 'bundles_bo_sung' in can:
    goi = json.loads(Path(a.bo_sung.format(id=a.id)).read_text(encoding='utf-8'))
    if goi.get('t') == t_m1:
        pass
    elif a.doi_t != 0 and a.bo_sung_t_goc and goi.get('t') == t_goc:
        dung = {k for tp in ft.tao_thanh_phan(cau_hinh) if hasattr(tp, 'kenh_moi') for k in tp.kenh_moi()}
        co = sorted(b['channel'] for b in goi['bundles'] if b['channel'] in dung and b['result'])
        if co: raise SystemExit(f'gói bổ sung quanh t gốc có dữ liệu ở kênh cấu hình dùng: {co}')
        moc['bo_sung_t_goc_kenh_dung_rong'] = sorted(dung)
    else:
        raise SystemExit('t của gói bổ sung khác t của ca')
    if moc is not None:
        moc['bo_sung'] = {'t': goi.get('t'), 'cua_so': goi.get('cua_so'), 'phien_ban': goi.get('phien_ban'),
                          'sha256': hashlib.sha256(Path(a.bo_sung.format(id=a.id)).read_bytes()).hexdigest()}
    them['bundles_bo_sung'] = goi['bundles']
t_bs = time.monotonic() - t0
out = Path(a.ra) / a.id; out.mkdir(parents=True, exist_ok=False)
sh, giay = [], []
for n in (1, 2):
    t1 = time.monotonic(); rec = ft.chay(inputs, cau_hinh, ban=a.ban, bo_sung=them); giay.append(round(time.monotonic() - t1, 2))
    if h8a is not None:
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {}).setdefault('H8-adapter', {})['goi_ghim'] = h8a
    if a.doi_t != 0:  # truy vết trong đầu ra; d = 0 không thêm khóa (giữ đầu ra như cũ)
        rec.setdefault('extra', {}).setdefault('m1_ft', {})['doi_t'] = {'giay': a.doi_t, 't_goc': t_goc, 't_dung': t_m1}
    enc = ft.canonical(rec) + '\n'; (out / f'method-output-{n}.json').write_text(enc, encoding='utf-8')
    sh.append(hashlib.sha256(enc.encode()).hexdigest())
tom = {'id': a.id, 'ban': a.ban, 'status': rec.get('status'), 'verdict': rec.get('verdict'),
       'nhom_hang_1': [r['entity'] for r in rec.get('entity_ranking', []) if r['tie_group'] == 0],
       'output_sha256': sh, 'trung_sha': sh[0] == sh[1], 'giay_chay': giay, 'giay_bo_sung': round(t_bs, 2),
       'cau_hinh_sha256': ft.sha_cau_hinh(cau_hinh), 'ma_nguon_sha256': ft.sha_ma_nguon(),
       'chu_thich': (rec.get('extra') or {}).get('m1_ft', {}).get('chu_thich')}
if h8a is not None:
    tom['h8_adapter'] = h8a
if moc is not None:
    tom['doi_t'] = a.doi_t
    tom['moc'] = moc
(out / 'summary.json').write_text(json.dumps(tom, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(json.dumps({k: tom[k] for k in ('id', 'ban', 'verdict', 'nhom_hang_1', 'trung_sha', 'giay_chay')}, ensure_ascii=False))

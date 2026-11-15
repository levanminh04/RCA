"""T-061: chuyển đầu ra M1 (method-output-*.json) sang định dạng kết quả RCA bản 0 cho giao diện.

Chỉ đọc: (1) file đầu ra M1, (2) manifest hash để kiểm file, (3) adapter FlashTicket của chính lượt chạy
(lấy truy vấn metric và ánh xạ tên service), (4) request.json của bộ điều phối cho đúng ca (mốc t). Cả bốn kiểm hash
theo cùng manifest; adapter được thực thi từ đúng chuỗi byte đã kiểm, không ghi bytecode. Không đọc sổ tiêm lỗi,
kế hoạch có vai trò ca, log tải hay bất kỳ nhãn nào. Đáp án chỉ ghép ở lớp phát lại, sau khi đầu ra đã băm.

Bản 0.2 hỗ trợ chế độ a và bốn trạng thái của M1: OK, NO_EVIDENCE (có cửa sổ và verdict), ERROR và UNSUPPORTED
(M1 trả cửa sổ và verdict rỗng; mốc lấy từ request.json của bộ điều phối).

Quy ước: mọi trường lấy thẳng từ M1 giữ nguyên giá trị; trường dẫn xuất theo quy tắc ghi trong
`dinh-dang-ket-qua-rca.md` §3. Đầu ra tất định (không ghi giờ chuyển đổi), để băm lại được.

Cách dùng:
  py -3 -B chuyen-doi.py --vao <outputs/<mã>/method-output-1.json> --request <cases/<mã>/request.json>
     --manifest <artifacts-sha256.json> --goc-manifest <thư mục gốc của manifest> --adapter <adapter_flashticket.py>
     --ma-ca <mã mờ> --ra <đầu ra.json>
Mã ca phải trùng tên thư mục chứa file M1 và thư mục chứa request.json.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import types
from pathlib import Path

sys.dont_write_bytecode = True

DINH_DANG = 'flashticket-rca-ket-qua'
PHIEN_BAN_DINH_DANG = '0.2'
TRANG_THAI_LOI = ('ERROR', 'UNSUPPORTED')
CAM_DOC = ('ledger', 'so-tiem-loi', 'execution-plan', 'load-impact', 'light-load', 'dap-an')

VAI_TRO = {  # lớp M1 → vai trò hiển thị (trực tiếp theo lớp, không suy thêm)
    'tu_sinh': 'nghi_nguon',
    'ke_thua': 'bi_keo_theo',
    'binh_thuong': 'binh_thuong',
    'thieu_du_lieu': 'thieu_du_lieu',
}
NHAN_VAI_TRO = {  # ngắn để vừa trong nút Node graph (khoảng 12 ký tự)
    'nghi_nguon': 'nghi nguồn',
    'bi_keo_theo': 'bị kéo theo',
    'binh_thuong': 'bình thường',
    'thieu_du_lieu': 'thiếu dữ liệu',
}
MAU = {  # màu chỉ phụ thuộc vai trò dự đoán của M1
    'nghi_nguon': '#E02F44',
    'bi_keo_theo': '#FF9830',
    'binh_thuong': '#8E8E8E',
    'thieu_du_lieu': '#CA95E5',
}
MAU_CANH_THUONG = '#999999'
MAU_CANH_BANG_CHUNG = '#E02F44'
NHAN_KET_LUAN = {
    'CAUSE_FOUND': 'M1 thấy thành phần có bất thường tự sinh',
    'NO_INTRINSIC_ANOMALY': 'M1 không thấy bất thường tự sinh ở thành phần nào',
    'INSUFFICIENT_EVIDENCE': 'M1 không có phép chấm hợp lệ nào',
}
MO_TA_MOC = {
    'a': 'Mốc tham chiếu do bộ điều phối cấp (chế độ a). RCA và Grafana không tự phát hiện mốc này.',
    'b': 'Mốc do luật cảnh báo phát hiện (chế độ b).',
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def doc_da_kiem(path, manifest_path, goc):
    """Đọc byte một lần, kiểm sha256 và kích thước theo manifest trên chính chuỗi byte đó.
    Trả (đường dẫn tương đối theo manifest, sha256, số byte, byte); lệch hoặc thiếu thì dừng."""
    m = json.load(open(manifest_path, encoding='utf-8'))
    rel = Path(os.path.relpath(path, goc)).as_posix()
    muc = m['files'].get(rel)
    if muc is None:
        raise SystemExit(f'Không có {rel} trong manifest {manifest_path}')
    b = Path(path).read_bytes()
    h = hashlib.sha256(b).hexdigest()
    if h != muc['sha256'] or len(b) != muc['bytes']:
        raise SystemExit(f'Hash lệch: {rel}')
    return rel, h, len(b), b


def nap_adapter(b, ten):
    """Thực thi adapter từ đúng chuỗi byte đã kiểm hash; không ghi .pyc, không đọc lại file."""
    mod = types.ModuleType('adapter_flashticket_t058')
    mod.__file__ = ten
    exec(compile(b, ten, 'exec'), mod.__dict__)
    return mod


def ns_utc(ns):
    return dt.datetime.fromtimestamp(ns // 10**9, tz=dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S') + \
        f'.{ns % 10**9:09d}Z'


def khoang(lo, hi):
    # ms là số nguyên khi ns chia hết cho 10^6; không thì giữ phần lẻ ở ns, ms làm tròn xuống (ghi rõ trong tài liệu)
    return {'tu_ns': lo, 'den_ns': hi, 'tu_ms': lo // 10**6, 'den_ms': hi // 10**6,
            'tu_utc': ns_utc(lo), 'den_utc': ns_utc(hi)}


class AnhXa:
    """Ánh xạ tên thực thể M1 → nhãn trong kho, lấy từ adapter của chính lượt chạy (không tự đặt)."""

    def __init__(self, ad):
        self.queries = {q['channel']: q['query'] for q in ad.QUERIES}
        self.metric_nguoc = {}
        for nhan, tt in list(ad.ALIASES.items()) + list(ad.INFRA.items()):
            self.metric_nguoc.setdefault(tt, nhan)
        self.trace_nguoc = {tt: nhan for nhan, tt in ad.ALIASES.items()}

    def tach_metric(self, phan):
        """'api-gateway_latency-90' → ('api-gateway', 'latency-90'); tiền tố là tên thực thể đổi '_' thành '-'."""
        for kenh in sorted(self.queries, key=len, reverse=True):
            if phan.endswith('_' + kenh):
                return phan[:-len(kenh) - 1], kenh
        return None, None


def lien_ket(don_vi, thuc_the, cua_so_ms, ax):
    """Liên kết chỉ sinh khi có truy vấn/định danh từ nguồn tương ứng. Trả (danh sách, lý do khi rỗng)."""
    loai = don_vi.split('|', 1)[0]
    if loai == 'metric':
        tien_to, kenh = ax.tach_metric(don_vi.split('|', 1)[1])
        if kenh is None or tien_to != thuc_the.replace('_', '-'):
            return [], 'không tách được kênh/thực thể từ mã đơn vị'
        if kenh == 'db-size':
            bo_loc = {'postgresql_database_name': thuc_the}
        else:
            bo_loc = {'service_name': ax.metric_nguoc.get(thuc_the, thuc_the)}
        return [{'loai': 'metric', 'kho': 'prometheus', 'truy_van': ax.queries[kenh], 'bo_loc_chuoi': bo_loc,
                 'cua_so_ms': cua_so_ms, 'cach_lay': 'dan_xuat',
                 'ghi_chu': 'Truy vấn nguyên văn của adapter lượt chạy; bộ lọc chuỗi theo ánh xạ tên của adapter. '
                            'Chọn chuỗi của thực thể từ kết quả, không phải truy vấn riêng cho thực thể.'}], None
    if loai == 'op':
        _, chu, ten = don_vi.split('|', 2)
        svc = ax.trace_nguoc.get(chu, chu)
        tq = '{ resource.service.name = %s && name = %s }' % (json.dumps(svc), json.dumps(ten))
        return [{'loai': 'trace_tim_kiem', 'kho': 'tempo', 'truy_van': tq, 'cua_so_ms': cua_so_ms,
                 'cach_lay': 'dan_xuat',
                 'ghi_chu': 'Tìm span cùng service và tên thao tác trong cửa sổ. Không phải trace ID do M1 chọn; '
                            'M1 không xuất trace mẫu.'}], None
    return [], f'loại đơn vị "{loai}" chưa có truy vấn hoặc định danh từ nguồn'


def moc_tu_request(t_req):
    t_ns = int(t_req) * 10**9
    return {'t_ns': t_ns, 't_utc': ns_utc(t_ns), 'nguon': 'bo_dieu_phoi',
            'mo_ta': MO_TA_MOC['a'] + ' Lấy từ request.json của bộ điều phối cho đúng ca.'}


def ban_ghi_loi(m1, ma_ca, nguon, t_req):
    """ERROR/UNSUPPORTED: M1 trả cửa sổ và verdict rỗng (src/m1/chuoi.py::_ban_ghi_loi). Giữ sự cố trong danh sách
    với trạng thái, thông báo lỗi và mốc của bộ điều phối; không nút, không cạnh, không hạng."""
    return {
        'dinh_dang': DINH_DANG, 'phien_ban_dinh_dang': PHIEN_BAN_DINH_DANG,
        'su_co': {'ma': ma_ca, 'che_do': 'a', 'moc': moc_tu_request(t_req),
                  'cua_so_nen': None, 'cua_so_su_co': None, 'ket_luan': None,
                  'ket_luan_hien_thi': f'M1 không trả kết quả ({m1["status"]})',
                  'trang_thai': m1['status'], 'loi': m1.get('error')},
        'nguon': dict(nguon, method=m1.get('method'), method_version=m1.get('method_version'),
                      config_id=m1.get('config_id'), variant=m1.get('variant'), why_ids=m1.get('why_ids') or [],
                      che_do_m1=None),
        'do_phu': {'so_quan_sat': m1['sets']['observed'], 'so_tra_hang': m1['sets']['returned'],
                   'do_phu_cham': None, 'thieu_kenh_hop_le': [], 'so_canh_quan_sat': None, 'so_canh_tinh': None,
                   'thuc_the_khong_co_canh': [], 'hang_doi_giua_the_gioi': None, 'don_vi_phu_thuoc_quan_sat': [],
                   'ghi_chu': 'M1 không trả kết quả; không có độ phủ.'},
        'nut': [], 'canh': [], 'xep_hang': [],
        'vung': {'ap_dung': False, 'ly_do': 'M1 không trả kết quả.', 'goc': [], 'hop_cach_1': [], 'hop_cach_2': [],
                 'cach_1': {}, 'cach_2': {}, 'T_m1': None},
        'bang_chung': [], 'giai_thich_ke_thua': [], 'giai_thich': None,
    }


def chuyen(m1, ma_ca, nguon, ax, t_req):
    if m1.get('mode') != 'a':
        raise SystemExit('Định dạng 0.2 chỉ hỗ trợ chế độ a')
    if m1['status'] in TRANG_THAI_LOI:
        return ban_ghi_loi(m1, ma_ca, nguon, t_req)
    if m1['status'] not in ('OK', 'NO_EVIDENCE'):
        raise SystemExit(f'Trạng thái M1 lạ: {m1["status"]}')
    if (m1.get('extra') or {}).get('E6b_pi') is not None:
        raise SystemExit('Đầu ra xếp hạng E6b: khóa không mang tầng ở phần tử đầu; định dạng 0.2 chưa hỗ trợ')
    w = m1['window']
    if int(t_req) * 10**9 != w['A'][0]:
        raise SystemExit('Mốc trong request.json không khớp /window/A/0 của M1')
    if w.get('don_vi') != 'ns':
        raise SystemExit('Cửa sổ M1 không ở đơn vị ns')
    cs_nen = khoang(*w['N'])
    cs_sc = khoang(*w['A'])
    cs_ms = [cs_nen['tu_ms'], cs_sc['den_ms']]
    verdict = m1['verdict']
    classes = m1['classes']
    xep = {r['entity']: r for r in m1['entity_ranking']}
    blocks = m1['blocks']
    tang_P = m1['extra']['tang_P']
    canh = [tuple(c) for c in m1['extra']['canh']]
    kenh_co = m1['extra']['kenh_co']
    region = m1.get('region') or {}
    ap_dung_vung = verdict == 'CAUSE_FOUND' and bool(region)
    hop1 = set(region.get('hop_cach_1') or []) if ap_dung_vung else set()
    hop2 = set(region.get('hop_cach_2') or []) if ap_dung_vung else set()
    goc = list(region.get('T') or []) if ap_dung_vung else []

    # ---- bằng chứng: mỗi kênh có cờ ở thế giới P là một mục
    bang_chung = []
    bc_theo_tt, bc_theo_canh = {}, {}
    for k in kenh_co:
        lk, ly_do = lien_ket(k['don_vi'], k['thuc_the'], cs_ms, ax)
        muc = {'id': k['ma'], 'don_vi': k['don_vi'], 'thuc_the': k['thuc_the'], 'kenh': k['ten'],
               'huong': k['huong'], 'lop': k['lop'], 's': k['s'], 'F_I': k['F_I'],
               'khoi_phat_ns': k['khoi_phat'], 'khoi_phat_utc': ns_utc(k['khoi_phat']) if k['khoi_phat'] else None,
               'lien_ket': lk, 'ly_do_khong_lien_ket': ly_do}
        bang_chung.append(muc)
        bc_theo_tt.setdefault(k['thuc_the'], []).append(k['ma'])
        if k['don_vi'].startswith('canh|'):
            _, a, b = k['don_vi'].split('|', 2)
            bc_theo_canh.setdefault((a, b), []).append(k['ma'])

    # ---- khối xếp hạng
    so_trong_khoi = {}
    xep_hang = []
    for i, b in enumerate(blocks):
        tt = [e for g in b['groups'] for e in g]
        so_trong_khoi[i] = len(tt)
        tang = 3 - b['key'][0]
        xep_hang.append({'hang': i + 1, 'nhom_dong_hang': i, 'thuc_the': tt, 'so_thuc_the': len(tt), 'tang': tang,
                         'khoa_m1': b['key']})

    # ---- nút: thực thể quan sát ∪ đầu cạnh
    ten_nut = sorted(set(m1['sets']['observed_entities']) | {x for c in canh for x in c} | set(classes))
    co_canh = {x for c in canh for x in c}
    nut = []
    for e in ten_nut:
        lop = classes.get(e)
        vai_tro = VAI_TRO.get(lop, 'khong_ro')
        r = xep.get(e)
        hang = r['tie_group'] + 1 if r else None
        n_dong = so_trong_khoi[r['tie_group']] if r else None
        tang = tang_P.get(e)
        noi_bat = bool(r) and r['tie_group'] == 0 and lop == 'tu_sinh'
        if vai_tro in ('nghi_nguon', 'bi_keo_theo'):
            nhan_trong = f'#{hang}' + (f' ={n_dong}' if n_dong and n_dong > 1 else '')
        elif vai_tro == 'binh_thuong':
            nhan_trong = 'không cờ'
        else:
            nhan_trong = '?'
        nhan_phu = NHAN_VAI_TRO.get(vai_tro, 'không rõ')
        nut.append({
            'id': e, 'ten': e, 'lop_m1': lop, 'vai_tro': vai_tro, 'tang_m1': tang,
            'hang': hang, 'nhom_dong_hang': r['tie_group'] if r else None, 'so_dong_hang': n_dong,
            'khoa_m1': r['key'] if r else None,
            'noi_bat': noi_bat, 'goc_vung': e in goc, 'trong_vung_cach_1': e in hop1, 'trong_vung_cach_2': e in hop2,
            'co_canh': e in co_canh, 'bang_chung': sorted(bc_theo_tt.get(e, [])),
            'hien_thi': {'mau': MAU.get(vai_tro, '#8E8E8E'), 'nhan_trong': nhan_trong, 'nhan_phu': nhan_phu},
        })

    ds_canh = []
    nguon_canh = 'quan_sat' if m1['diagnostics'].get('so_canh_tinh', 0) == 0 else 'quan_sat_hoac_tinh'
    for a, b in canh:
        bc = sorted(bc_theo_canh.get((a, b), []))
        ds_canh.append({'id': f'{a}->{b}', 'nguon': a, 'dich': b, 'chieu': 'ben_goi->ben_duoc_goi',
                        'nguon_goc': nguon_canh, 'bang_chung': bc,
                        'hien_thi': {'mau': MAU_CANH_BANG_CHUNG if bc else MAU_CANH_THUONG,
                                     'nhan': 'có kênh bất thường' if bc else 'cạnh gọi quan sát'}})

    ke_thua = [{'thuc_the': x['thuc_the'], 'kenh_ma': x['ma'], 'duong': x['duong'], 'giai_thich_boi': x['giai_thich_ma'],
                'quy_tac': x['quy_tac'], 'trang_thai': x['trang_thai']} for x in m1.get('inherited_by', [])]

    che_do = m1['mode']
    ket_luan_hien_thi = NHAN_KET_LUAN.get(verdict, verdict)
    return {
        'dinh_dang': DINH_DANG, 'phien_ban_dinh_dang': PHIEN_BAN_DINH_DANG,
        'su_co': {
            'ma': ma_ca, 'che_do': che_do,
            'moc': {'t_ns': w['A'][0], 't_utc': ns_utc(w['A'][0]), 'nguon': 'bo_dieu_phoi',
                    'mo_ta': MO_TA_MOC['a']},
            'cua_so_nen': cs_nen, 'cua_so_su_co': cs_sc,
            'ket_luan': verdict, 'ket_luan_hien_thi': ket_luan_hien_thi,
            'trang_thai': m1['status'], 'loi': m1['error'],
        },
        'nguon': dict(nguon, method=m1['method'], method_version=m1['method_version'], config_id=m1['config_id'],
                      variant=m1['variant'], why_ids=m1['why_ids'], che_do_m1=m1['extra'].get('che_do')),
        'do_phu': {'so_quan_sat': m1['sets']['observed'], 'so_tra_hang': m1['sets']['returned'],
                   'do_phu_cham': m1['do_phu_cham'], 'thieu_kenh_hop_le': m1['diagnostics']['NO_VALID_CHANNEL'],
                   'so_canh_quan_sat': m1['diagnostics']['so_canh_quan_sat'],
                   'so_canh_tinh': m1['diagnostics']['so_canh_tinh'],
                   'thuc_the_khong_co_canh': sorted(set(ten_nut) - co_canh),
                   'hang_doi_giua_the_gioi': m1['RANK_CHANGED'], 'don_vi_phu_thuoc_quan_sat': m1['OBS_DEPENDENT'],
                   'ghi_chu': 'Inventory đầy đủ không có trong đầu ra M1; chỉ hiện thực thể M1 quan sát.'},
        'nut': nut, 'canh': ds_canh, 'xep_hang': xep_hang,
        'vung': {'ap_dung': ap_dung_vung,
                 'ly_do': None if ap_dung_vung else 'Không có thành phần tầng 1; nhóm đứng đầu không phải gốc vùng.',
                 'goc': goc, 'hop_cach_1': sorted(hop1), 'hop_cach_2': sorted(hop2),
                 'cach_1': region.get('cach_1') if ap_dung_vung else {},
                 'cach_2': region.get('cach_2') if ap_dung_vung else {},
                 'T_m1': region.get('T')},
        'bang_chung': bang_chung, 'giai_thich_ke_thua': ke_thua,
        'giai_thich': None,
    }


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--vao', required=True)
    ap.add_argument('--request', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--goc-manifest', required=True)
    ap.add_argument('--adapter', required=True)
    ap.add_argument('--ma-ca', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args(argv)
    for p in (a.vao, a.request, a.manifest, a.adapter):
        if any(x in Path(p).name.lower() for x in CAM_DOC):
            raise SystemExit(f'Bộ chuyển đổi không được đọc file có thể chứa nhãn: {p}')
    if Path(a.vao).resolve().parent.name != a.ma_ca or Path(a.request).resolve().parent.name != a.ma_ca:
        raise SystemExit('Mã ca không trùng thư mục chứa file M1 hoặc request.json')
    rel, h, n, b_m1 = doc_da_kiem(a.vao, a.manifest, a.goc_manifest)
    rel_rq, h_rq, _, b_rq = doc_da_kiem(a.request, a.manifest, a.goc_manifest)
    rel_ad, h_ad, _, b_ad = doc_da_kiem(a.adapter, a.manifest, a.goc_manifest)
    m1 = json.loads(b_m1.decode('utf-8'))
    t_req = json.loads(b_rq.decode('utf-8'))['t']
    ax = AnhXa(nap_adapter(b_ad, rel_ad))
    nguon = {'file_m1': rel, 'sha256_m1': h, 'bytes_m1': n, 'request': rel_rq, 'sha256_request': h_rq,
             'adapter': rel_ad, 'sha256_adapter': h_ad,
             'manifest': Path(os.path.relpath(a.manifest, Path(__file__).resolve().parents[2])).as_posix(),
             'bo_chuyen_doi': 'results/T-061/chuyen-doi.py',
             'sha256_bo_chuyen_doi': sha256_file(__file__)}
    out = chuyen(m1, a.ma_ca, nguon, ax, t_req)
    Path(a.ra).parent.mkdir(parents=True, exist_ok=True)
    with open(a.ra, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, allow_nan=False)
        f.write('\n')
    print(f'{a.ra}: {len(out["nut"])} nút, {len(out["canh"])} cạnh, {len(out["bang_chung"])} bằng chứng, '
          f'trạng thái {out["su_co"]["trang_thai"]}, kết luận {out["su_co"]["ket_luan"]}')


if __name__ == '__main__':
    sys.exit(main())

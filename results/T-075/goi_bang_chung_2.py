"""T-075 (W8) — bản 2 (sửa theo CX-30, CX-30b; bản 1 giữ nguyên ở goi_bang_chung.py) — dựng gói bằng chứng rút gọn cho LLM từ đầu ra G1 của một ca. Không gọi mạng, không gọi LLM.

Hai nguồn được hỗ trợ:
  - `g1`   : file ca G1 bản 0.5 (`du-lieu/<bản>/<ca>.json`, do `sau_v082.py` ghi); nếu có khối `che_do_b` (b-1)
             thì lấy thêm cảnh báo, độ phủ, số mẫu vào lõi từ khối đó.
  - `su_co`: file sự cố của bộ điều phối T-073 (`su-co/<mã>.json`). Dùng khi file G1 của ca chưa có trên laptop
             (trường hợp ca E5 `7577dd5b` ở lượt này). Gói này KHÔNG có bảng bằng chứng theo kênh.

Gói có hai phần:
  - `gui_di`   : phần duy nhất được phép đưa vào LLM (khi Minh duyệt danh sách trường, Q7). Mọi trích dẫn của đầu ra
                 trỏ vào phần này. Không chứa sổ tiêm, đáp án, tên ô, đường dẫn hay mã nhận diện ca (luật cứng 6).
  - `kiem_toan`: chỉ giữ ở máy: hash nguồn, con trỏ nguồn, danh sách trường đã loại. Không gửi đi.

Mỗi mục trong `gui_di` mang `nguon` = con trỏ JSON vào file nguồn để người đọc lần lại được.
Thời gian trong `gui_di` là giây tương đối so với mốc t của ca (t̂ ở chế độ b), không dùng giờ tuyệt đối.
"""
import hashlib
import json
import re
import sys

KHUON_VAO = 'T075-vao-2'
SO_BANG_CHUNG_TOI_DA = 20
SO_KE_THUA_TOI_DA = 20

# Khóa không bao giờ được xuất hiện trong `gui_di` (kiểm ở `quet_goi`). Danh sách khóa nhận diện/nhãn đã biết.
KHOA_CAM = {
    'nguon_ca', 'nguon_cua_so', 'nguon_output', 'ghi_chu_hash', 'phat_lai', 'dap_an', 'so_tiem', 'ledger',
    'ca', 'ma_ca_m1', 'su_co_b', 'opaque_id', 'path', 'file', 'directory', 'url', 'http_url', 'ra',
}
# Mẫu chữ không được xuất hiện ở bất kỳ giá trị nào của `gui_di` hay trong đầu ra LLM. Đây là phép quét chữ
# (heuristic): bắt đường dẫn, tên sổ tiêm, công cụ tiêm, tên lượt/chiến dịch và dạng tên ô viết hoa có gạch.
# Không thay được việc người duyệt đọc danh sách trường.
MAU_CAM = [
    r'ledger', r'so[-_ ]?tiem', r'sổ tiêm', r'\binj3\b', r'\btiem\b', r'tiêm', r'dap[-_ ]?an', r'đáp án',
    r'/srv/', r'/opt/', r'results/', r'D:/', r'\.jsonl\b', r'\bdev[0-9]\b', r'\bt0[0-9]{2}-(?:e[0-9]|dev|l[0-9])',
    r'\b[A-Z]{2,}-[A-Z]{2,}(?:-[0-9A-Z]+)?\b',
]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for khuc in iter(lambda: f.read(1 << 20), b''):
            h.update(khuc)
    return h.hexdigest()


def doc_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def _rel_s(ns, t_ns):
    return None if ns is None else round((ns - t_ns) / 1e9, 3)


def xep_hang_tu_g1(g1):
    """Danh sách hạng của G1 theo đúng thứ tự file: [(thuc_the, hang)]. Dùng để kiểm giữ nguyên thứ hạng."""
    return [(r['entity'], r['hang']) for r in g1['ranking_rows']]


def _goi_g1(g1, nguon_ten):
    sc = g1['su_co']
    t_ns = sc['cua_so_su_co']['tu_ms'] * 1_000_000
    b = g1.get('che_do_b')
    che_do = 'b' if b else 'a'
    rr = g1['ranking_rows']
    nhom1 = [r['entity'] for r in rr if r['hang'] == 1]
    gui = {
        'khuon': KHUON_VAO,
        'che_do': che_do,
        'cua_so': {
            'nen_s': [-300, 0], 'su_co_s': [0, 300],
            'moc': 't̂ = giờ bắt đầu của cảnh báo đầu tiên' if che_do == 'b'
                   else 'mốc ca do bộ điều phối cấp (chế độ a, ca thử)',
        },
        'ket_qua_rca': {
            'ban_phuong_phap': g1['ban']['ban'],
            'ket_luan': sc['ket_luan'], 'nguon_ket_luan': '#/su_co/ket_luan',
            'trang_thai_chay': g1['trang_thai_chay'], 'nguon_trang_thai': '#/trang_thai_chay',
            'nhom_hang_1': nhom1,
            'xep_hang': [{'thuc_the': r['entity'], 'hang': r['hang'], 'lop': r['lop'],
                          'so_kenh_co': r['so_kenh_co'], 'nguon': f'#/ranking_rows/{i}'}
                         for i, r in enumerate(rr)],
            'ghi_chu': 'Thứ hạng do lõi RCA tính; lớp giải thích không được đổi. lop: tu_sinh = có kênh bất thường '
                       'riêng; ke_thua = bất thường được giải thích bởi thực thể khác; binh_thuong = không có kênh cờ. '
                       'Kênh có F_I = 1 là kênh đưa thực thể vào tầng hạng đầu; F_I = 0 là kênh có cờ nhưng không '
                       'tạo hạng.',
        },
    }
    bc_all = sorted(enumerate(g1['bang_chung']), key=lambda x: (-(x[1].get('F_I') or 0), -(x[1].get('s') or 0), x[0]))
    gui['bang_chung'] = [{
        'thuc_the': b_['thuc_the'], 'kenh': b_['kenh'], 'don_vi': b_['don_vi'], 'huong': b_['huong'],
        'lop': b_['lop'], 'diem_s': b_['s'], 'F_I': b_['F_I'],
        'khoi_phat_tuong_doi_s': _rel_s(b_.get('khoi_phat_ns'), t_ns), 'nguon': f'#/bang_chung/{i}',
    } for i, b_ in bc_all[:SO_BANG_CHUNG_TOI_DA]]
    gui['bang_chung_bo_bot'] = max(0, len(bc_all) - SO_BANG_CHUNG_TOI_DA)
    gui['ke_thua'] = [{
        'thuc_the': k['thuc_the'], 'kenh': k['kenh'], 'huong': k['huong'], 'duong': k['duong'],
        'giai_thich_boi': k['giai_thich'], 'quy_tac': k['quy_tac'], 'trang_thai': k['trang_thai'],
        'nguon': f'#/ke_thua/{i}',
    } for i, k in enumerate(g1['ke_thua'][:SO_KE_THUA_TOI_DA])]
    gui['ke_thua_bo_bot'] = max(0, len(g1['ke_thua']) - SO_KE_THUA_TOI_DA)
    reg = g1.get('region') or {}
    gui['vung'] = {'T': reg.get('T', []), 'hop_cach_1': reg.get('hop_cach_1', []), 'nguon': '#/region'}
    gui['thao_tac_co_co'] = [{
        'chu': t['chu'], 'ten': t['ten'], 'loai': t['loai'], 'n_N': t['n_N'], 'n_A': t['n_A'],
        'kenh_co': [{'ten': k.get('ten'), 'huong': k.get('huong'), 'F_I': k.get('F_I'), 'diem_s': k.get('s')}
                    for k in t['kenh_co']],  # bỏ `khoi_phat` (giờ tuyệt đối)
        'nguon': f'#/thao_tac/{i}',
    } for i, t in enumerate(g1['thao_tac']) if t.get('co_m1')][:SO_BANG_CHUNG_TOI_DA]
    gui['canh_xep_hang'] = {'trang_thai': g1.get('trang_thai_canh'), 'so_canh': len(g1.get('canh_xep_hang') or []),
                            'nguon': '#/trang_thai_canh'}
    gui['gioi_han'] = [g1['gioi_han']] if g1.get('gioi_han') else []
    if b and b.get('gioi_han'):
        gui['gioi_han'].append(b['gioi_han'])  # D3: nửa nền có thể chứa phần đầu sự cố (R2)
    kt = {'nguon_kieu': 'g1', 'nguon_ten': nguon_ten,
          'loai_khoi_gui_di': ['ca', 'nguon_ca', 'nguon_cua_so', 'cua_so_ms', 'tu_utc', 'den_loai_tru',
                               'ban.nguon_output', 'ban.sha256_output', 'ban.ghi_chu_hash', 'ban.mo_ta',
                               'ban.cau_hinh_*', 'lien_ket[*]', 'metric_links', 'thao_tac[*].vi_du',
                               'canh_thao_tac', 'don_vi_m1', 'phat_lai', 'entity_ranking.key'],
          'xep_hang_nguon': xep_hang_tu_g1(g1)}
    if b:
        gui.update(_phan_b(b, t_ns // 1_000_000_000, pre='#/che_do_b'))
        v = (b.get('du_lieu_loi') or {}).get('v082') or {}
        kt['v082_output_sha256'] = {'gia_tri': v.get('output_sha256'),
                                    'con_tro': '#/che_do_b/du_lieu_loi/v082/output_sha256'}
    else:
        gui['do_phu'] = None
        gui['thieu_trong_goi'] = ['Chế độ a: không có khối độ phủ cửa sổ và cảnh báo.']
    return gui, kt


def _phan_b(b, t_s, pre):
    """Cảnh báo, độ phủ, số mẫu vào lõi từ một khối có cấu trúc như file sự cố T-073 (hoặc che_do_b)."""
    out = {}
    def _het(c):
        e = ((c.get('i1') or {}).get('t_het') or {}).get('epoch_s')
        return None if e is None else e - t_s

    out['canh_bao'] = [{
        'ma_luat': c['ma_luat'], 'tin_hieu': (c.get('nhan') or {}).get('t072_tin_hieu'),
        'bat_dau_tuong_doi_s': c['t_hat'] - t_s, 'ket_thuc_tuong_doi_s': _het(c),
        'nguon': f'{pre}/canh_bao/{i}',
    } for i, c in enumerate(b.get('canh_bao', []))]
    dl = b.get('du_lieu_loi') or {}
    phu = dl.get('phu') or {}
    out['do_phu'] = {
        'du_cua_so': phu.get('du_cua_so'), 'thieu_bat_buoc': phu.get('thieu_bat_buoc', []),
        'quy_tac': phu.get('quy_tac'),
        'lo_lon_nhat_s': {k: v.get('lo_lon_nhat_s') for k, v in (phu.get('nguon') or {}).items()
                          if k in set(phu.get('thieu_bat_buoc', []))},
        'pham_vi': 'tính trên đầu vào P7 cơ sở (V082 đọc lại), trước gói bổ sung liveness; kênh bổ sung không '
                   'nằm trong phép phủ này',
        'nguon': f'{pre}/du_lieu_loi/phu',
    }
    hm = dl.get('hang_metric') or {}
    out['so_mau_dau_vao_p7_co_so'] = {
        'pham_vi': 'đầu vào P7 cơ sở (V082 đọc lại), chưa gồm gói bổ sung; N = [t−300, t), A = [t, t+300)',
        'span': dl.get('span'), 'log': dl.get('log'),
        'hang_metric_trong_cua_so': {'N': hm.get('N'), 'A': hm.get('A')},
        'hang_metric_ngoai_cua_so': hm.get('ngoai'),
                             'nguon': f'{pre}/du_lieu_loi'}
    return out


def _goi_su_co(sc, nguon_ten):
    """Gói rút gọn từ file sự cố T-073 khi chưa có file G1 của ca trên laptop."""
    t_s = sc['t_hat']
    kq = sc['ket_qua']
    gui = {
        'khuon': KHUON_VAO, 'che_do': 'b',
        'cua_so': {'nen_s': [-300, 0], 'su_co_s': [0, 300], 'moc': 't̂ = giờ bắt đầu của cảnh báo đầu tiên'},
        'ket_qua_rca': {
            'ban_phuong_phap': next((b['tom_tat'].get('ban') for b in sc['buoc'] if b['ten'] == 'v082'), None),
            'ket_luan': kq['verdict'], 'nguon_ket_luan': '#/ket_qua/verdict',
            'trang_thai_chay': None,
            'nguon_trang_thai': 'không có: file sự cố chỉ có trạng thái bước P7 (`#/du_lieu_loi/p7_status`), '
                                'không có trạng thái V082',
            'nhom_hang_1': kq['nhom_hang_1'],
            'xep_hang': [{'thuc_the': e, 'hang': 1, 'lop': None, 'so_kenh_co': None, 'nguon': '#/ket_qua/nhom_hang_1'}
                         for e in kq['nhom_hang_1']],
            'ghi_chu': 'Chỉ có nhóm hạng 1 của V082 trong file sự cố; bảng hạng đầy đủ nằm ở file G1 của ca, '
                       'chưa có trong gói này.',
        },
        'bang_chung': [], 'bang_chung_bo_bot': 0, 'ke_thua': [], 'ke_thua_bo_bot': 0,
        'vung': None, 'thao_tac_co_co': [], 'canh_xep_hang': None,
        'thieu_trong_goi': ['Bảng bằng chứng theo kênh, kế thừa, vùng và bảng hạng đầy đủ của V082 không có trong '
                            'nguồn này (file sự cố của bộ điều phối; các khối đó nằm ở file G1 của ca).'],
        'gioi_han': [],
    }
    gui.update(_phan_b(sc, t_s, pre='#'))
    kdv = next((b['tom_tat'] for b in sc['buoc'] if b['ten'] == 'kiem_dau_vao'), None)
    if kdv:
        gui['so_mau_theo_thuc_the'] = {'span': kdv.get('span_theo_thuc_the'), 'log': kdv.get('log_theo_thuc_the'),
                                       'pham_vi': 'đầu vào P7 cơ sở (bước kiem_dau_vao), chưa gồm gói bổ sung',
                                       'ghi_chu': 'N = nửa nền [t−300, t), A = nửa sự cố [t, t+300); '
                                                  'thiếu khóa nghĩa là 0 mẫu.',
                                       'nguon': f"#/buoc/{[b['ten'] for b in sc['buoc']].index('kiem_dau_vao')}"
                                                '/tom_tat'}
    v = sc['du_lieu_loi'].get('v082') or {}
    kt = {'nguon_kieu': 'su_co', 'nguon_ten': nguon_ten,
          'v082_output_sha256': {'gia_tri': v.get('output_sha256'), 'con_tro': '#/du_lieu_loi/v082/output_sha256'},
          'loai_khoi_gui_di': ['ma', 'ma_ca_m1', 'buoc[*].tom_tat.directory/files/chon_file', 'chon_file',
                               'canh_bao[*].nhan.http_url', 'canh_bao[*].sha256_than', 'spool_seq',
                               'nhan_webhook_utc', 'mọi giờ tuyệt đối', 'buoc[p7] (bản P7, không phải V082)'],
          'xep_hang_nguon': [(e, 1) for e in kq['nhom_hang_1']]}
    return gui, kt


def dung_goi(duong_dan, kieu, nguon_ten=None):
    """Trả (goi, sha256 nguồn). goi = {'gui_di': ..., 'kiem_toan': ...}."""
    d = doc_json(duong_dan)
    if kieu == 'g1':
        gui, kt = _goi_g1(d, nguon_ten)
    elif kieu == 'su_co':
        gui, kt = _goi_su_co(d, nguon_ten)
    else:
        raise ValueError(kieu)
    kt['nguon_sha256'] = sha256_file(duong_dan)
    goi = {'gui_di': gui, 'kiem_toan': kt}
    loi = quet_goi(gui)
    if loi:
        raise ValueError(f'gói chứa trường/chữ cấm: {loi}')
    return goi


def quet_goi(x, p=''):
    """Quét `gui_di`: khóa cấm và mẫu chữ cấm. Trả danh sách vi phạm (rỗng = đạt)."""
    loi = []
    if isinstance(x, dict):
        for k, v in x.items():
            if k in KHOA_CAM:
                loi.append(f'khóa cấm {p}/{k}')
            loi += quet_goi(v, f'{p}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            loi += quet_goi(v, f'{p}/{i}')
    elif isinstance(x, str):
        for m in MAU_CAM:
            if re.search(m, x):
                loi.append(f'mẫu cấm {m!r} ở {p}: {x[:60]!r}')
    return loi


if __name__ == '__main__':
    goi = dung_goi(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    json.dump(goi, sys.stdout, ensure_ascii=False, indent=1)

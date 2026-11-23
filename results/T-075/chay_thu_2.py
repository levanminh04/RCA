"""T-075 bản 2 — chạy thử bộ kiểm `kiem_w8_2` trên gói `goi_bang_chung_2`. Không gọi LLM, không mạng.
Bản 1 (`chay_thu.py`, `ket-qua-thu.json`) giữ nguyên. Kết quả bản 2 ghi riêng: `ca-thu-2/`, `ket-qua-thu-2.json`.

Nguồn đầu ra: `viet_tay` (ca-thu-2/<ca>/dau-ra-*.json, ghi bởi viet_mau_2.py) hoặc `sinh` (đột biến có chủ đích
trong file này, ghi ra dau-ra-sinh-*.json). Mong đợi khai trong MONG_DOI / dot_bien: 'dat', 'sai_khuon', hoặc tập
mã phép kiểm phải bắt.
`#/tong/dat` = mọi đầu ra khớp mong đợi VÀ K8 đạt VÀ K9 đạt VÀ đối chứng chéo không lọt cặp nào (CX-30 R6).
Chạy: py -3 -I -B -X utf8 viet_mau_2.py && py -3 -I -B -X utf8 chay_thu_2.py
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from goi_bang_chung_2 import dung_goi, quet_goi, sha256_file, doc_json, xep_hang_tu_g1  # noqa: E402
from kiem_w8_2 import kiem, phai_khong_du  # noqa: E402

GOC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(GOC, '..', '..'))
NGUON = {
    'e5-su-co': ('results/T-073/e5/su-co/bbc0a6d44f.json', 'su_co'),
    'e5-g1': ('results/T-073/e5/ca-7577dd5b/srv/rca-lab/rca-results/t073-e5-001/du-lieu/V082-V066+H8a/7577dd5b.json',
              'g1'),
    'cu-1': ('results/T-065/may-l11/du-lieu/V082-V066+H8a/1e5a3dc5.json', 'g1'),
    'cu-2': ('results/T-065/may-l11/du-lieu/V082-V066+H8a/729604d2.json', 'g1'),
}
CA_THU = os.path.join(GOC, 'ca-thu-2')
MONG_DOI = {  # đầu ra viết tay
    ('e5-su-co', 'dung'): 'dat', ('e5-su-co', 'sai-doi-hang'): {'K4', 'K6'},
    ('e5-g1', 'dung'): 'dat', ('cu-1', 'dung'): 'dat',
    ('cu-2', 'dung'): 'dat', ('cu-2', 'sai-bia-nguyen-nhan'): {'K4'},
    ('gia-1', 'dung'): 'dat', ('gia-2', 'dung'): 'dat',
}


def ghi(p, x):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(x, f, ensure_ascii=False, indent=1)
        f.write('\n')


def xep_hang_nguon(duong, kieu):
    d = doc_json(duong)
    return xep_hang_tu_g1(d) if kieu == 'g1' else [(e, 1) for e in d['ket_qua']['nhom_hang_1']]


def ca_gia(goi):
    out = {}
    g = copy.deepcopy(goi['cu-1'])
    g['gui_di'].update(bang_chung=[], ke_thua=[], thao_tac_co_co=[])
    g['kiem_toan']['ca_gia'] = 'cu-1 cắt bang_chung, ke_thua, thao_tac_co_co'
    out['gia-1'] = g
    g = copy.deepcopy(goi['cu-1'])
    g['gui_di']['ket_qua_rca']['ket_luan'] = 'INSUFFICIENT_EVIDENCE'
    g['kiem_toan']['ca_gia'] = 'cu-1 đổi ket_luan thành INSUFFICIENT_EVIDENCE'
    out['gia-2'] = g
    g = copy.deepcopy(goi['cu-1'])
    g['gui_di']['do_phu'] = {'du_cua_so': False, 'thieu_bat_buoc': ['metric:cpu:payment-service'],
                             'quy_tac': 'giả lập', 'lo_lon_nhat_s': {'metric:cpu:payment-service': 120.0},
                             'pham_vi': 'giả lập', 'nguon': 'giả lập'}
    g['gui_di']['thieu_trong_goi'] = []
    g['kiem_toan']['ca_gia'] = 'cu-1 thêm do_phu.du_cua_so = false'
    out['gia-3'] = g
    g = copy.deepcopy(goi['e5-g1'])  # phản ví dụ CX-30 R4
    g['gui_di']['bang_chung'] = [b for b in g['gui_di']['bang_chung']
                                 if not (b['thuc_the'] == 'booking-service' and b['F_I'] == 1)]
    g['kiem_toan']['ca_gia'] = 'e5-g1 bỏ hai mục F_I = 1 của booking-service (chỉ còn workload F_I = 0)'
    out['gia-4'] = g
    return out


def dot_bien(m):
    """Đầu ra sai sinh từ đầu ra viết tay đúng. Mỗi mục: (ca, tên) -> (đầu ra, mong đợi)."""
    cu1, e5g = m['cu-1'], m['e5-g1']
    o = {}

    def D(x):
        return copy.deepcopy(x)
    x = D(cu1); x['khang_dinh'][1]['trich_dan'][0]['con_tro'] = '/bang_chung/5'
    o[('cu-1', 'sai-con-tro')] = (x, {'K2'})
    x = D(cu1); x['khang_dinh'][1]['trich_dan'][1]['gia_tri'] = 3.1
    o[('cu-1', 'sai-gia-tri')] = (x, {'K2'})
    x = D(cu1); x['khang_dinh'].append({'id': 'k5', 'loai': 'quan_sat', 'cau': 'booking-service cũng có cpu tăng.',
                                        'trich_dan': [{'con_tro': '/bang_chung/0'}]})
    o[('cu-1', 'sai-thuc-the')] = (x, {'K3'})
    x = D(cu1); x['khang_dinh'][1]['cau'] = x['khang_dinh'][1]['cau'].replace('2,76', '7,5')
    o[('cu-1', 'sai-so')] = (x, {'K3b'})
    x = D(cu1); x['xep_hang_nhac_lai'] = [['ticket-service'], ['payment-service']]
    o[('cu-1', 'sai-hang')] = (x, {'K6'})
    x = D(cu1); x['thieu_bang_chung'][0]['cau'] += ' Cần đối chiếu sổ tiêm.'
    o[('cu-1', 'sai-cam')] = (x, {'K7'})
    # CX-30 R3a: KHONG_DU nhưng giữ suy_luan, giam_thieu, không nêu thiếu (gói đủ)
    x = D(cu1); x['trang_thai'] = 'KHONG_DU_BANG_CHUNG'; x['thieu_bang_chung'] = []
    o[('cu-1', 'sai-r3a-tu-choi-van-suy-luan')] = (x, {'K4'})
    # CX-30 R3b: GIAI_THICH rỗng, chỉ một mục thiếu dẫn /bang_chung_bo_bot
    x = D(cu1); x['khang_dinh'] = []; x['goi_y_xu_ly'] = []
    x['thieu_bang_chung'] = [{'cau': 'Thiếu một số mục.', 'trich_dan': [{'con_tro': '/bang_chung_bo_bot'}]}]
    o[('cu-1', 'sai-r3b-giai-thich-rong')] = (x, {'K4'})
    # CX-30 R3c: null trong khang_dinh → sai khuôn, không sập
    x = D(cu1); x['khang_dinh'].append(None)
    o[('cu-1', 'sai-r3c-null')] = (x, 'sai_khuon')
    x = D(cu1); x['them'] = 1
    o[('cu-1', 'sai-khoa-la')] = (x, 'sai_khuon')
    x = D(cu1); x['khang_dinh'][0]['cau'] = 'a'
    o[('cu-1', 'sai-cau-rong')] = (x, 'sai_khuon')
    x = D(cu1); x['khang_dinh'][0]['trich_dan'] = []
    o[('cu-1', 'sai-khong-trich')] = (x, 'sai_khuon')
    # CX-30b N3: câu đúng dẫn bảng có dữ liệu làm bối cảnh → phải đạt
    x = D(cu1); x['thieu_bang_chung'] = [{'cau': 'Gói có bằng chứng cho payment-service, nhưng thiếu thông tin độ phủ.',
                                          'trich_dan': [{'con_tro': '/bang_chung'}, {'con_tro': '/thieu_trong_goi/0'}]}]
    o[('cu-1', 'dung-n3-boi-canh')] = (x, 'dat')
    # K4b: khai vắng một bảng có dữ liệu
    x = D(cu1); x['thieu_bang_chung'][0]['vang'] = ['/bang_chung']
    o[('cu-1', 'sai-k4b-khai-vang')] = (x, {'K4b'})
    # gia-3 (thiếu phủ): đúng = cu-1 + mục thiếu nêu phủ; CX-30b N1: giấu thiếu phủ, gắn /do_phu/quy_tac vào câu hạng
    x = D(cu1); x['thieu_bang_chung'] = [{'cau': 'Metric cpu của payment-service thiếu phủ cửa sổ (lỗ khoảng 120 s); '
                                                 'cần đối chiếu thêm trước khi hành động.',
                                          'trich_dan': [{'con_tro': '/do_phu/thieu_bat_buoc'},
                                                        {'con_tro': '/do_phu/lo_lon_nhat_s'}]}]
    o[('gia-3', 'dung')] = (x, 'dat')
    x = D(cu1); x['thieu_bang_chung'] = [{'cau': 'Không có thông tin bổ sung về độ phủ.',
                                          'trich_dan': [{'con_tro': '/ket_qua_rca/ket_luan'}]}]
    x['khang_dinh'][0]['trich_dan'].append({'con_tro': '/do_phu/quy_tac'})
    o[('gia-3', 'sai-n1-giau-thieu-phu')] = (x, {'K5'})
    # CX-30b N2: false → 0 trên mẫu E5
    x = D(m['e5-su-co']); x['thieu_bang_chung'][2]['trich_dan'][0]['gia_tri'] = 0
    o[('e5-su-co', 'sai-n2-bool-so')] = (x, {'K2'})
    # gia-1, gia-2: giải thích của cu-1 trên gói đã cắt / lõi báo thiếu
    o[('gia-1', 'sai-giai-thich-bia')] = (D(cu1), {'K2', 'K4'})
    o[('gia-2', 'sai-giai-thich-bia')] = (D(cu1), {'K4'})
    # gia-4 (CX-30 R4): giải thích E5 trên gói chỉ còn workload F_I = 0 của booking-service
    x = D(e5g); x['khang_dinh'][1]['trich_dan'] = [{'con_tro': '/bang_chung/3'}]
    x['khang_dinh'][1]['cau'] = 'booking-service có kênh workload giảm.'
    o[('gia-4', 'sai-r4-kenh-khong-tao-hang')] = (x, {'K4'})
    return o


def khop(md, kq):
    if md == 'sai_khuon':
        return not kq['hop_khuon']
    if md == 'dat':
        return kq['hop_khuon'] and not kq['loi']
    return kq['hop_khuon'] and md <= {e.split(':', 1)[0] for e in kq['loi']}


def main():
    ket_qua = {'phien_ban': 'T075-kiem-2', 'ca': {}, 'tong': {}}
    goi, truoc = {}, {}
    for ca, (rel, kieu) in NGUON.items():
        p = os.path.join(REPO, rel)
        truoc[ca] = (sha256_file(p), xep_hang_nguon(p, kieu))
        goi[ca] = dung_goi(p, kieu, ca)
    goi.update(ca_gia(goi))

    viet = {}
    for ca in goi:
        d = os.path.join(CA_THU, ca)
        os.makedirs(d, exist_ok=True)
        ghi(os.path.join(d, 'goi.json'), goi[ca])
        for f in sorted(os.listdir(d)):
            if f.startswith('dau-ra-') and f.endswith('.json') and not f.startswith('dau-ra-sinh-'):
                viet[(ca, f[7:-5])] = doc_json(os.path.join(d, f))
    sinh = dot_bien({ca: viet[(ca, 'dung')] for ca in ('cu-1', 'e5-g1', 'e5-su-co')})

    dem = {'khop': 0, 'khong_khop': 0, 'viet_tay': 0, 'sinh': 0}
    for ca in goi:
        rec = {'phai_khong_du': phai_khong_du(goi[ca]['gui_di']), 'K8_goi_sach': quet_goi(goi[ca]['gui_di']) == [],
               'dau_ra': {}}
        ds = [(t, x, MONG_DOI.get((ca, t)), 'viet_tay') for (c, t), x in viet.items() if c == ca]
        for (c, t), (x, md) in sinh.items():
            if c == ca:
                ghi(os.path.join(CA_THU, ca, f'dau-ra-sinh-{t}.json'), x)
                ds.append(('sinh-' + t, x, md, 'sinh'))
        for ten, x, md, nguon in ds:
            kq = kiem(goi[ca]['gui_di'], x)
            ok = md is not None and khop(md, kq)
            dem['khop' if ok else 'khong_khop'] += 1
            dem[nguon] += 1
            rec['dau_ra'][ten] = {'nguon': nguon, 'mong_doi': md if isinstance(md, str) or md is None else sorted(md),
                                  'hop_khuon': kq['hop_khuon'], 'loi': kq['loi'], 'khop_mong_doi': ok}
        ket_qua['ca'][ca] = rec

    cheo = {}
    dung_ca = {ca: x for (ca, t), x in viet.items() if t == 'dung'}
    dung_ca['gia-3'] = sinh[('gia-3', 'dung')][0]
    for xa, ra in dung_ca.items():
        for y, g in goi.items():
            if xa != y:
                kq = kiem(g['gui_di'], ra)
                cheo[f'{xa}->{y}'] = sorted({e.split(':', 1)[0] for e in kq['loi']}) if kq['hop_khuon'] else ['K0']
    lot = [k for k, v in cheo.items() if not v]
    ket_qua['doi_chung_cheo'] = {'so_cap': len(cheo), 'ma_bat': cheo, 'dat_ngoai_y_muon': lot}

    k9 = {}
    for ca, (rel, kieu) in NGUON.items():
        p = os.path.join(REPO, rel)
        xh_goi = [[r['thuc_the'], r['hang']] for r in goi[ca]['gui_di']['ket_qua_rca']['xep_hang']]
        k9[ca] = {'sha_truoc_bang_sau': truoc[ca][0] == sha256_file(p),
                  'xep_hang_nguon_truoc_bang_sau': [list(t) for t in truoc[ca][1]]
                  == [list(t) for t in xep_hang_nguon(p, kieu)],
                  'xep_hang_goi_bang_nguon': xh_goi == [list(t) for t in truoc[ca][1]],
                  'sha256': truoc[ca][0]}
    ket_qua['K9'] = k9
    k9_dat = all(v for r in k9.values() for k, v in r.items() if k != 'sha256')
    k8_dat = all(r['K8_goi_sach'] for r in ket_qua['ca'].values())
    ket_qua['tong'] = {'dau_ra': dem['khop'] + dem['khong_khop'], 'viet_tay': dem['viet_tay'], 'sinh': dem['sinh'],
                       'khop_mong_doi': dem['khop'], 'khong_khop': dem['khong_khop'], 'K8_dat': k8_dat,
                       'K9_dat': k9_dat, 'cheo_lot': len(lot),
                       'dat': dem['khong_khop'] == 0 and k8_dat and k9_dat and not lot}
    ghi(os.path.join(GOC, 'ket-qua-thu-2.json'), ket_qua)
    print(json.dumps(ket_qua['tong'], ensure_ascii=False))
    for ca, r in ket_qua['ca'].items():
        for ten, v in r['dau_ra'].items():
            if not v['khop_mong_doi']:
                print('KHÔNG KHỚP', ca, ten, v['mong_doi'], v['hop_khuon'], v['loi'])
    print('chéo lọt:', lot)
    return 0 if ket_qua['tong']['dat'] else 1


if __name__ == '__main__':
    sys.exit(main())

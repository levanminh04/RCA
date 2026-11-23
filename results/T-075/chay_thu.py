"""T-075 (W8) — chạy thử bộ kiểm ngoại tuyến trên ca thật (E5, 2 ca G1 cũ) và ca giả. Không gọi LLM, không mạng.

"LLM" ở lượt này là đầu ra viết tay (`ca-thu/<ca>/dau-ra-*.json`) hoặc đầu ra đúng bị làm hỏng có chủ đích
(`dot_bien`), ghi lại ra `ca-thu/<ca>/` để soát. Mỗi đầu ra có kết quả mong đợi khai trong `MONG_DOI`
(đạt, hoặc tập mã phép kiểm phải bắt). Ngoài K1–K7 của kiem_w8.py, chạy thêm:
  K8 gói sạch: `quet_goi` không thấy khóa/chữ cấm trong `gui_di`.
  K9 thứ hạng RCA trước/sau: sha256 file nguồn trước = sau khi dựng gói và chạy lớp giải thích; bảng hạng đọc lại từ
     nguồn sau khi chạy = trước; bảng hạng trong gói = bảng hạng nguồn. Đầu ra giải thích chỉ ghi vào thư mục ca-thu.
Cách chạy (từ thư mục này):  py -3 -I -X utf8 chay_thu.py
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from goi_bang_chung import dung_goi, quet_goi, sha256_file, doc_json, xep_hang_tu_g1  # noqa: E402
from kiem_w8 import kiem, phai_khong_du  # noqa: E402

GOC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(GOC, '..', '..'))
NGUON = {
    'e5': ('results/T-073/e5/su-co/bbc0a6d44f.json', 'su_co'),
    'cu-1': ('results/T-065/may-l11/du-lieu/V082-V066+H8a/1e5a3dc5.json', 'g1'),
    'cu-2': ('results/T-065/may-l11/du-lieu/V082-V066+H8a/729604d2.json', 'g1'),
}
CA_THU = os.path.join(GOC, 'ca-thu')


def ghi(p, x):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(x, f, ensure_ascii=False, indent=1)
        f.write('\n')


def xep_hang_nguon(duong, kieu):
    d = doc_json(duong)
    return xep_hang_tu_g1(d) if kieu == 'g1' else [(e, 1) for e in d['ket_qua']['nhom_hang_1']]


def ca_gia(goi_cu1):
    """Ca giả dựng từ gói cu-1 (chỉ sửa ở tầng gói, không sửa file nguồn)."""
    g1 = copy.deepcopy(goi_cu1)
    g1['gui_di']['bang_chung'] = []
    g1['gui_di']['ke_thua'] = []
    g1['gui_di']['thao_tac_co_co'] = []
    g1['kiem_toan']['ca_gia'] = 'cu-1 cắt bang_chung, ke_thua, thao_tac_co_co (mô phỏng thiếu tín hiệu)'
    g2 = copy.deepcopy(goi_cu1)
    g2['gui_di']['ket_qua_rca']['ket_luan'] = 'INSUFFICIENT_EVIDENCE'
    g2['kiem_toan']['ca_gia'] = 'cu-1 đổi ket_luan thành INSUFFICIENT_EVIDENCE'
    g3 = copy.deepcopy(goi_cu1)
    g3['gui_di']['do_phu'] = {'du_cua_so': False, 'thieu_bat_buoc': ['metric:cpu:payment-service'],
                              'quy_tac': 'giả lập', 'lo_lon_nhat_s': {'metric:cpu:payment-service': 120.0},
                              'nguon': 'giả lập'}
    g3['gui_di']['thieu_trong_goi'] = []
    g3['kiem_toan']['ca_gia'] = 'cu-1 thêm do_phu.du_cua_so = false (cpu payment-service thiếu)'
    return {'gia-1': g1, 'gia-2': g2, 'gia-3': g3}


def dot_bien(dung):
    """Các đầu ra sai sinh từ đầu ra đúng của cu-1, mỗi cái nhắm một phép kiểm."""
    out = {}
    x = copy.deepcopy(dung); x['khang_dinh'][1]['trich_dan'][0]['con_tro'] = '/bang_chung/5'
    out['sai-con-tro'] = (x, {'K2'})
    x = copy.deepcopy(dung); x['khang_dinh'][1]['trich_dan'][1]['gia_tri'] = 3.1
    out['sai-gia-tri'] = (x, {'K2'})
    x = copy.deepcopy(dung)
    x['khang_dinh'].append({'id': 'k5', 'loai': 'quan_sat', 'cau': 'booking-service cũng có cpu tăng.',
                            'trich_dan': [{'con_tro': '/bang_chung/1'}]})
    out['sai-thuc-the'] = (x, {'K3'})
    x = copy.deepcopy(dung); x['khang_dinh'][1]['cau'] = x['khang_dinh'][1]['cau'].replace('2,76', '7,5')
    out['sai-so'] = (x, {'K3b'})
    x = copy.deepcopy(dung); x['xep_hang_nhac_lai'] = [['ticket-service'], ['payment-service']]
    x['khang_dinh'][2]['cau'] = x['khang_dinh'][2]['cau'].replace('hạng 2', 'hạng 1')
    out['sai-hang'] = (x, {'K6'})
    x = copy.deepcopy(dung); x['thieu_bang_chung'][0]['cau'] += ' Cần đối chiếu sổ tiêm.'
    out['sai-cam'] = (x, {'K7'})
    x = copy.deepcopy(dung); x['khang_dinh'][0]['trich_dan'] = []
    out['sai-khong-trich'] = (x, {'K1'})
    return out


def main():
    ket_qua = {'ca': {}, 'tong': {}}
    goi = {}
    truoc = {}
    for ca, (rel, kieu) in NGUON.items():
        p = os.path.join(REPO, rel)
        truoc[ca] = (sha256_file(p), xep_hang_nguon(p, kieu))
        goi[ca] = dung_goi(p, kieu, ca)
    goi.update(ca_gia(goi['cu-1']))

    dung_cu1 = doc_json(os.path.join(CA_THU, 'cu-1', 'dau-ra-dung.json'))
    sinh = {'cu-1': dot_bien(dung_cu1)}
    gia3_dung = copy.deepcopy(dung_cu1)
    gia3_dung['thieu_bang_chung'] = [{
        'cau': 'Metric cpu của payment-service thiếu phủ trong cửa sổ (lỗ khoảng 120 s); mức tăng cpu cần đối chiếu '
               'thêm trước khi hành động.',
        'trich_dan': [{'con_tro': '/do_phu/thieu_bat_buoc'}, {'con_tro': '/do_phu/lo_lon_nhat_s'}]}]
    sinh['gia-3'] = {'dung': (gia3_dung, set()), 'sai-bo-do-phu': (copy.deepcopy(dung_cu1), {'K5'})}
    sinh['gia-1'] = {'sai-giai-thich-bia': (copy.deepcopy(dung_cu1), {'K2', 'K4'})}
    sinh['gia-2'] = {'sai-giai-thich-bia': (copy.deepcopy(dung_cu1), {'K2', 'K4'})}

    MONG_DOI = {  # đầu ra viết tay có sẵn trong ca-thu/<ca>/
        ('e5', 'dung'): set(), ('e5', 'sai-doi-hang'): {'K4', 'K6'},
        ('cu-1', 'dung'): set(),
        ('cu-2', 'dung'): set(), ('cu-2', 'sai-bia-nguyen-nhan'): {'K4'},
        ('gia-1', 'dung'): set(), ('gia-2', 'dung'): set(),
    }

    so_dat = so_truot = 0
    for ca, g in goi.items():
        d = os.path.join(CA_THU, ca)
        os.makedirs(d, exist_ok=True)
        ghi(os.path.join(d, 'goi.json'), g)
        rec = {'phai_khong_du': phai_khong_du(g['gui_di']), 'K8_goi_sach': quet_goi(g['gui_di']) == [],
               'dau_ra': {}}
        dau_ra = {}
        for f in sorted(os.listdir(d)):
            if f.startswith('dau-ra-') and f.endswith('.json') and not f.startswith('dau-ra-sinh-'):
                ten = f[len('dau-ra-'):-5]
                dau_ra[ten] = (doc_json(os.path.join(d, f)), MONG_DOI.get((ca, ten)))
        for ten, (x, md) in sinh.get(ca, {}).items():
            ghi(os.path.join(d, f'dau-ra-sinh-{ten}.json'), x)
            dau_ra['sinh-' + ten] = (x, md)
        for ten, (x, md) in dau_ra.items():
            loi = kiem(g['gui_di'], x)
            ma = {e.split(':', 1)[0] for e in loi}
            if md is None:
                dung_mong_doi = None
            elif not md:
                dung_mong_doi = not loi
            else:
                dung_mong_doi = md <= ma
            rec['dau_ra'][ten] = {'mong_doi': sorted(md) if md is not None else 'chưa khai', 'ma_bat': sorted(ma),
                                  'loi': loi, 'khop_mong_doi': dung_mong_doi}
            if dung_mong_doi:
                so_dat += 1
            else:
                so_truot += 1
        ket_qua['ca'][ca] = rec

    # Đối chứng chéo: đầu ra đúng của ca X kiểm trên gói ca Y (X ≠ Y) phải trượt; nếu đạt thì bộ kiểm quá lỏng.
    dung_ca = {ca: doc_json(os.path.join(CA_THU, ca, 'dau-ra-dung.json'))
               for ca in goi if os.path.exists(os.path.join(CA_THU, ca, 'dau-ra-dung.json'))}
    dung_ca['gia-3'] = gia3_dung
    cheo = {}
    for x, ra in dung_ca.items():
        for y, g in goi.items():
            if x == y:
                continue
            loi = kiem(g['gui_di'], ra)
            cheo[f'{x}->{y}'] = sorted({e.split(':', 1)[0] for e in loi})
    lot = [k for k, v in cheo.items() if not v]
    ket_qua['doi_chung_cheo'] = {'ma_bat': cheo, 'dat_ngoai_y_muon': lot}
    print('đối chứng chéo:', len(cheo), 'cặp; đạt ngoài ý muốn:', lot)

    # K9 — giữ nguyên thứ hạng RCA trước/sau
    k9 = {}
    for ca, (rel, kieu) in NGUON.items():
        p = os.path.join(REPO, rel)
        sha_sau, xh_sau = sha256_file(p), xep_hang_nguon(p, kieu)
        xh_goi = [(r['thuc_the'], r['hang']) for r in goi[ca]['gui_di']['ket_qua_rca']['xep_hang']]
        k9[ca] = {'sha_truoc_bang_sau': truoc[ca][0] == sha_sau,
                  'xep_hang_nguon_truoc_bang_sau': [list(t) for t in truoc[ca][1]] == [list(t) for t in xh_sau],
                  'xep_hang_goi_bang_nguon': [list(t) for t in xh_goi] == [list(t) for t in truoc[ca][1]],
                  'sha256': sha_sau}
    ket_qua['K9'] = k9
    k9_dat = all(all(v for k, v in r.items() if k != 'sha256') for r in k9.values())
    k8_dat = all(r['K8_goi_sach'] for r in ket_qua['ca'].values())
    ket_qua['tong'] = {'dau_ra_khop_mong_doi': so_dat, 'dau_ra_khong_khop': so_truot, 'K8_dat': k8_dat,
                       'K9_dat': k9_dat, 'dat': so_truot == 0 and k8_dat and k9_dat}
    ghi(os.path.join(GOC, 'ket-qua-thu.json'), ket_qua)
    print(json.dumps(ket_qua['tong'], ensure_ascii=False))
    for ca, r in ket_qua['ca'].items():
        for ten, v in r['dau_ra'].items():
            print(f"{ca:6} {ten:28} mong_doi={v['mong_doi']} bat={v['ma_bat']} khop={v['khop_mong_doi']}")
    return 0 if ket_qua['tong']['dat'] else 1


if __name__ == '__main__':
    sys.exit(main())

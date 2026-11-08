"""So tương đương dev (laptop, trên kết quả nhận từ EC2) theo tiêu chí đã khai trước khi chạy:
chỉ được khác (a) extra.dau_vao_cd3.dich, extra.dau_vao_cd3.so_span_goc_A; (b) diagnostics.span.goc, diagnostics.span.mo_coi.
Mọi trường khác của bản ghi (khối ba world, kênh, vùng, G_N, canh, tầng, điểm...) phải trùng hệt.
Thêm: phép dựng đích từ trung gian (đường dùng cho test) trùng đích lượt chạy đủ; C-d3 từ trung gian trùng C-d3 lượt đủ;
ca dev-607751ac0a: bản ghi 'cu' trên EC2 trùng bản ghi laptop đã lưu (dev-ob-001, cùng config).
Chạy: py -3 -B results/T-054/runs/sua-cd3-ob-001/so_sanh.py
"""
import copy
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
GOC = RUN.parents[3]
NHAN = RUN / 'nhan'
CHO_PHEP = [('extra', 'dau_vao_cd3', 'dich'), ('extra', 'dau_vao_cd3', 'so_span_goc_A'),
            ('diagnostics', 'span', 'goc'), ('diagnostics', 'span', 'mo_coi')]


def bo(rec):
    r = copy.deepcopy(rec)
    for path in CHO_PHEP:
        x = r
        for k in path[:-1]:
            x = x.get(k, {})
        x.pop(path[-1], None)
    return r


def diff(a, b, p=''):
    if type(a) is not type(b):
        return [p]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            out += diff(a.get(k), b.get(k), p + '/' + str(k)) if k in a and k in b else [p + '/' + str(k)]
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [p]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, p + f'[{i}]')
        return out
    return [] if a == b else [p]


tong = {'schema': 'T054-SUA-CD3-DEV-SO-SANH-1', 'tieu_chi_cho_phep_khac': ['/'.join(p) for p in CHO_PHEP], 'cases': {}}
for f in sorted(NHAN.glob('*/ra/dev-*.json')):
    d = json.loads(f.read_text(encoding='utf-8'))
    cu, moi = d['ban_ghi_cu'], d['ban_ghi_moi']
    khac = diff(bo(cu), bo(moi))
    tong['cases'][d['opaque_id']] = {
        'may': f.parts[-3], 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
        'khac_ngoai_cho_phep': khac[:20], 'n_khac_ngoai_cho_phep': len(khac),
        'span_cu': {k: cu['diagnostics']['span'][k] for k in ('goc', 'mo_coi')},
        'span_moi': {k: moi['diagnostics']['span'][k] for k in ('goc', 'mo_coi')},
        'n_span_doi_root': d['n_span_doi_root_moi'],
        'dich_cu': d['dich_cu'], 'dich_moi': d['dich_moi'],
        'so_span_goc_A_cu': d['so_span_goc_A_cu'], 'so_span_goc_A_moi': d['so_span_goc_A_moi'],
        'dan_xuat_trung_lan_chay': d['dan_xuat_trung_lan_chay'], 'cd3_dan_xuat_trung': d['cd3_dan_xuat_trung'],
        'cd3_cu': d['cd3_cu']['trang_thai'], 'cd3_moi': d['cd3_moi']['trang_thai'], 'giay': d['giay'],
    }
    if d['opaque_id'] == 'dev-607751ac0a':
        ref = json.loads((GOC / 'results/T-054/runs/cai-ob-source-native-008/dev-ob-001/result.json')
                         .read_text(encoding='utf-8'))['records'][0]
        kh = diff(cu, ref)
        tong['doi_chieu_laptop_ec2_dev_607751ac0a'] = {'n_khac': len(kh), 'khac': kh[:20]}
c = tong['cases']
tong['tom_tat'] = {
    'n_ca': len(c),
    'tuong_duong_ngoai_cho_phep': sum(v['n_khac_ngoai_cho_phep'] == 0 for v in c.values()),
    'dan_xuat_trung': sum(v['dan_xuat_trung_lan_chay'] and v['cd3_dan_xuat_trung'] for v in c.values()),
    'cd3_cu': {s: sum(v['cd3_cu'] == s for v in c.values()) for s in sorted({v['cd3_cu'] for v in c.values()})},
    'cd3_moi': {s: sum(v['cd3_moi'] == s for v in c.values()) for s in sorted({v['cd3_moi'] for v in c.values()})},
    'ca_root_marker': sum(v['n_span_doi_root'] > 0 for v in c.values()),
}
(RUN / 'dev-so-sanh.json').write_text(json.dumps(tong, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
print(json.dumps({k: tong[k] for k in ('tom_tat',)} | {'laptop_ec2': tong.get('doi_chieu_laptop_ec2_dev_607751ac0a')},
                 ensure_ascii=False))

"""Kiểm phục vụ đính chính 002 (T-054, phản biện Codex lượt 2). Chỉ đọc result.json đã xác minh; không chạy phương pháp.

1. So toàn bộ danh sách khối worlds/P/blocks của M1 với từng vế (không chỉ khối đầu/RR root như doi_top_khi_bo).
2. Với các ca TT mà bỏ E1 làm RR đổi: kênh op của root bị E5 giải thích bởi kênh E2, kênh khác hay cả hai.
3. Kênh F_I của root ở C-a0 cho ca OB network_delay.
Chạy từ gốc repo: py -3 -B results/T-054/reports/p7a-013-v2/kiem-toan-ven/so_khoi.py
"""
import json
import os
from collections import Counter

R = 'results/T-054/reports/p7a-013-v2/'
d = json.load(open(R + 'phan-tich-nhom.json', encoding='utf-8'))
tg = d['trung_gian_theo_ca']


def rec(path):
    return json.load(open(path, encoding='utf-8'))['records'][0]


def bl(r):
    return [[sorted(g) for g in b['groups']] for b in r['worlds']['P']['blocks']]


def flat(b):
    return [e for blk in b for g in blk for e in g]


out = {'schema': 'T054-SO-KHOI-1', 'nguon': R + 'phan-tich-nhom.json#/trung_gian_theo_ca', 'so_khoi': {}, 'vi_du': {}}
cnt = Counter()
for key, arms in sorted(tg.items()):
    ds, o = key.split('|')
    m = bl(rec(arms['M1']['result']))
    for a in ('bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'T12-on'):
        x = bl(rec(arms[a]['result']))
        cnt[(ds, a, 'n')] += 1
        cnt[(ds, a, 'ca_doi_ca_danh_sach')] += x != m
        cnt[(ds, a, 'ca_doi_khoi_dau')] += x[:1] != m[:1]
        cnt[(ds, a, 'ca_doi_thu_tu_5_dau')] += flat(x)[:5] != flat(m)[:5]
        if x != m and f'{ds}|{a}' not in out['vi_du']:
            i = next(i for i in range(max(len(x), len(m))) if i >= len(x) or i >= len(m) or x[i] != m[i])
            out['vi_du'][f'{ds}|{a}'] = {'ca': o, 'khoi_lech_dau_tien': i, 'so_khoi_M1': len(m), 'so_khoi_ve': len(x)}
for (ds, a, k), v in sorted(cnt.items()):
    out['so_khoi'].setdefault(f'{ds}|M1 vs {a}', {})[k] = v

# 2. E1×E5 trên TT
e1 = {}
for c in d['so_cap']['RE2-TT|M1-bo-E1|RR']['cases']:
    o = c['opaque_id']
    t = tg['RE2-TT|' + o]['bo-E1']
    r = rec(t['result'])
    root = d['cases']['RE2-TT'][o]['root']
    by = {}
    for x in r.get('inherited_by', []):
        if x['thuc_the'] == root and x['trang_thai'] == 'ap_dung' and x['don_vi'].startswith('op|'):
            by.setdefault(x['ma'], set()).add('E2' if str(x['giai_thich'][1]).startswith('E2:') else 'khac')
    top = [ch for ch in t['root_channels'] if ch['fam'] == 'op_full'][:1]
    e1[o] = {'M1_rr': c['M1'], 'boE1_rr': c['bo-E1'],
             'kenh_op_root_bi_giai_thich_theo_nguon': dict(Counter('+'.join(sorted(v)) for v in by.values())),
             'op_full_manh_nhat_root': ({'s': top[0]['s'], 'F_I': top[0]['F_I']} if top else None)}
out['E1xE5_TT_ca_boE1_doi_RR'] = e1

# 3. OB network_delay ở C-a0
nd = {}
for o, v in sorted(d['cases']['Nezha-OB'].items()):
    if v['fault'] != 'network_delay':
        continue
    t = tg['Nezha-OB|' + o]['C-a0']
    nd[o] = {'root': v['root'], 'kenh_F_I_root_C-a0': [{'fam': x['fam'], 's': x['s'], 'ten': x['ten']}
                                                          for x in t['root_channels'] if x['F_I'] == 1]}
out['OB_network_delay_C-a0'] = nd

dst = R + 'kiem-toan-ven/so-khoi.json'
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
print(json.dumps(out['so_khoi'], ensure_ascii=False, indent=0))
print({o: v['kenh_op_root_bi_giai_thich_theo_nguon'] for o, v in e1.items()})

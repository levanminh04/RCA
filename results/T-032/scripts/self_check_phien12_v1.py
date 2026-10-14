#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T-032, phiên 12 — tự soát số của báo cáo chính, doc-tay.md và kiem-tiep.md.

Hai phần:
 A. Tính lại từ các bảng của phiên 12 những con số mới của báo cáo chính và so với giá trị ghi trong báo cáo
    (giá trị kỳ vọng chép tay từ báo cáo vào danh sách CLAIMS dưới đây).
 B. Soát chép số: với mỗi dòng của ba file .md có dẫn "KQ9/KQ10/KQ11 mục X", mọi con số trong dòng phải có mặt
    trong các mục được dẫn của file kết quả tương ứng. Số không tìm thấy được liệt kê để người làm xem tay.

Dùng: python3 -B -X utf8 self_check_phien12_v1.py <thư mục results/T-032> <file kết quả json>
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = sys.argv[1]
OUTP = sys.argv[2]


def L(rel):
    return json.load(open(os.path.join(ROOT, rel), encoding='utf-8'))


def T(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


D = L('doi-chieu-dung-sai.json')
M5 = L('phan-xu-caller-root.json')
KN = L('kha-nang-do-trace.json')
PLAN = L('runs/tong-hop-phien-12-001/ke-hoach-doc-tay.json')
CL = L('runs/tong-hop-phien-12-001/tracerca-cap-theo-lop.json')
CT = L('can-thiep-tinh-toan.json')
BP = L('bao-phu-nhom.json')
U = D['don_vi']
BY = {u['unit_id']: u for u in U}
res = []


def claim(name, got, exp):
    res.append({'claim': name, 'got': got, 'expected': exp, 'ok': got == exp})


# ---- A1. bảng mục 2
dem = D['dem_theo_phuong_phap']
exp2 = {'RE2-TT|baro': (21, 30), 'Nezha-OB|baro': (8, 22), 'RE2-TT|simplerca': (25, 30), 'Nezha-OB|simplerca': (7, 22),
        'RE2-TT|microrank_full': (2, 26), 'Nezha-OB|microrank_full': (0, 22), 'RE2-TT|tracerca': (21, 26), 'Nezha-OB|tracerca': (2, 22),
        'RE2-TT|circa_ols_da': (16, 30)}
for k, (h, n) in exp2.items():
    claim('mục 2: %s hạng 1 / chạy được' % k, [dem[k]['dung_hang_1'], dem[k]['OK']], [h, n])
t = [u for u in U if u['method'] == 'torai_B' and u['dataset'] == 'RE2-TT']
claim('mục 2: TORAI B 26/30 ở cả ba seed', [sum(1 for u in t if u['seed'] == s and u['dung_hang_1']) for s in (0, 1, 2)], [26, 26, 26])
claim('mục 2: Nezha-OB không chạy được 22 + 22', [dem['Nezha-OB|circa_ols_da']['khong_OK'], dem['Nezha-OB|torai_B']['khong_OK']], [22, 22])
claim('mục 1: 372 đơn vị, 192 sai hoặc không chạy được, 52 nhóm',
      [len(U), BP['counts']['n_wrong_or_non_OK_units'], len(D['nhom'])], [372, 192, 52])
tk = L('runs/tong-hop-phien-12-001/tu-kiem.json')
claim('mục 1: 13/13 tự kiểm', [sum(1 for c in tk['checks'] if c['pass']), len(tk['checks'])], [13, 13])

# ---- A2. bảng mục 5.3
c = M5['dem_theo_dataset_phuong_phap']
e = M5['bang_chung_tinh_toan_theo_thuc_the']
top_up = Counter()
n_ent = Counter()
for x in M5['don_vi_M5']:
    k = '%s|%s' % (x['dataset'], x['method'])
    vc = BY[x['unit_id']]['vi_tri_chuoi_goi'] or {}
    top_up[k] += vc.get('vi_tri_thuc_the_dung_dau') in ('phia_tren', 'hai_chieu')
    n_ent[k] += len(x['thuc_the'])
exp53 = {  # cohort, sai hạng 1 OK, M5, top phía trên, số thực thể
    'RE2-TT|tracerca': (30, 5, 4, 3, 5), 'Nezha-OB|tracerca': (22, 20, 16, 12, 20), 'RE2-TT|microrank_full': (30, 24, 5, 0, 10),
    'Nezha-OB|microrank_full': (22, 22, 20, 0, 20), 'RE2-TT|simplerca': (30, 5, 5, 4, 7), 'Nezha-OB|simplerca': (22, 15, 9, 6, 9),
    'RE2-TT|baro': (30, 9, 3, 1, 11), 'Nezha-OB|baro': (22, 14, 7, 2, 7), 'RE2-TT|circa_ols_da': (30, 14, 10, 9, 26),
    'RE2-TT|torai_B': (90, 12, 3, 3, 6)}
for k, v in exp53.items():
    claim('mục 5.3: %s' % k, [c[k]['don_vi_trong_cohort'], c[k].get('sai_hang_1_OK', 0), c[k].get('co_M5_o_k1_hoac_k5', 0), top_up[k], n_ent[k]], list(v))


def ev(k, sub):
    return sum(v for kk, v in e.get(k, {}).items() if sub in kk)


claim('mục 5.3: TraceRCA RE2-TT 4 xác nhận, 1 không xét được', [ev('RE2-TT|tracerca', 'xác nhận'), ev('RE2-TT|tracerca', 'không xét được')], [4, 1])
claim('mục 5.3: TraceRCA Nezha-OB 9 / 6 / 5', [ev('Nezha-OB|tracerca', 'xác nhận'), ev('Nezha-OB|tracerca', 'chưa phân xử'), ev('Nezha-OB|tracerca', 'không xét được')], [9, 6, 5])
claim('mục 5.3: MicroRank 10; 16 và 4', [ev('RE2-TT|microrank_full', 'không gắn với root'), ev('Nezha-OB|microrank_full', 'không gắn với root'), ev('Nezha-OB|microrank_full', 'từ 50%')], [10, 16, 4])
claim('mục 5.3: SimpleRCA 6 và 6 do riêng metric', [ev('RE2-TT|simplerca', 'riêng phiếu metric'), ev('Nezha-OB|simplerca', 'riêng phiếu metric')], [6, 6])
claim('mục 5.3: CIRCA 24 cực lớn, 2 không', [ev('RE2-TT|circa_ols_da', 'xác nhận'), ev('RE2-TT|circa_ols_da', 'chưa phân xử')], [24, 2])
claim('mục 5.3: TORAI 6 thực thể, log lớn nhất', [ev('RE2-TT|torai_B', 'log')], [6])
claim('mục 5.3: 82 đơn vị M5; 1 không xác định ở TraceRCA Nezha-OB', [len(M5['don_vi_M5']), c['Nezha-OB|tracerca'].get('M5_khong_xac_dinh')], [82, 1])
claim('mục 5.3: 80 ca × phương pháp', [len({(x['dataset'], x['method'], x['opaque_id']) for x in M5['don_vi_M5']})], [80])

# ---- A3. mức đo được (mục 5.4)
td = KN['theo_dataset']
claim('mục 5.4: mức theo dataset', [td['RE2-TT']['theo_muc'].get('đo được', 0), td['Nezha-OB']['theo_muc'].get('đo được', 0),
                                    td['RE2-TT']['theo_muc'].get('đo được một phần', 0), td['Nezha-OB']['theo_muc'].get('đo được một phần', 0),
                                    td['RE2-TT']['theo_muc'].get('không đo được', 0), td['Nezha-OB']['theo_muc'].get('không đo được', 0)], [0, 16, 21, 0, 9, 6])
rs = Counter()
for k in KN['ca']:
    if k['muc_do_duoc'] == 'không đo được':
        rs[(k['dataset'], 'không được' in (k['ly_do_phien_10'] or ''))] += 1
claim('mục 5.4: không đo được: root không được gọi 6 + 2; cạnh dưới 20 lời gọi 3 + 4',
      [rs[('RE2-TT', True)], rs[('Nezha-OB', True)], rs[('RE2-TT', False)], rs[('Nezha-OB', False)]], [6, 2, 3, 4])

# ---- A4. đọc tay
claim('đọc tay: 100 đơn vị, 76 sai, 24 đối chứng', [PLAN['so_don_vi_doc_tay_khong_trung'], PLAN['so_don_vi_sai_doc'], PLAN['so_doi_chung_doc']], [100, 76, 24])
reads = [r for g in PLAN['nhom'] for r in g['doc_tay']]
claim('đọc tay: 114 lượt = 36 cùng ô + 67 khác ô + 11 không đối chứng',
      [len(reads), sum(1 for r in reads if r['doi_chung_doc'] and r['doi_chung_doc']['cung_o']),
       sum(1 for r in reads if r['doi_chung_doc'] and not r['doi_chung_doc']['cung_o']), sum(1 for r in reads if not r['doi_chung_doc'])], [114, 36, 67, 11])
claim('đọc tay: 52/52 nhóm có đơn vị sai được đọc', [sum(1 for g in PLAN['nhom'] if g['doc_tay'])], [52])
claim('đối chứng: 301 yêu cầu, 110 không có', [len(D['cap_doi_chung']), sum(1 for p in D['cap_doi_chung'] if not p['doi_chung'])], [301, 110])
sai_doc = {r['don_vi_sai_doc'] for r in reads}
da_doc = {p['unit_id'] for p in PLAN['don_vi_doc']}
sai_all = {u['unit_id'] for u in U if 'wrong_or_non_OK' in u['vai_tro']}
non_ok = lambda st: sum(1 for u in U if u['trang_thai_nguon'] == st and u['unit_id'] not in da_doc)
claim('KT-14: 192 đơn vị sai; 76 đã đọc (74 chọn theo đường đi + 2 đọc làm đối chứng k=5); 116 chưa đọc; trong đó 42 UNSUPPORTED, 6 ERROR',
      [len(sai_all), len(sai_all & da_doc), len(sai_doc), len(sai_all - da_doc), non_ok('UNSUPPORTED'), non_ok('ERROR')], [192, 76, 74, 116, 42, 6])

# ---- A5. CIRCA (mục 3.5; doc-tay 5.1, 5.3)
ci = [u for u in U if u['method'] == 'circa_ols_da' and u['trang_thai_nguon'] == 'OK']
m4 = [u for u in ci if 'M4' in (u['t028']['co']['1'] or [])]
claim('H14: 8 ca M4; cả 8 có 3 thực thể trên root đều cực lớn; bỏ cạnh root hạng 1 ở 8/8',
      [len(m4), sum(1 for u in m4 if len(u['chi_tiet']['tren_root_bang_DA']) == 3 and all(p['mang_khoa_cuc_lon_sau_DA'] for p in u['chi_tiet']['tren_root_bang_DA'])),
       sum(1 for u in m4 if u['chi_tiet']['hang_root']['K2_khong_canh_RHT'][1] == 1)], [8, 8, 8])
rh = sorted((u['chi_tiet']['hang_root']['RHT'][0] for u in ci if u['chi_tiet']['root_mang_khoa_cuc_lon_sau_DA']), reverse=True)
claim('H14: 3 ca đúng nhờ root nhận giá trị cực lớn; hạng trước DA 8, 7, 2',
      [rh, all(u['dung_hang_1'] for u in ci if u['chi_tiet']['root_mang_khoa_cuc_lon_sau_DA'])], [[8, 7, 2], True])
claim('H13: 11 ca có nút cực lớn', [sum(1 for u in ci if u['chi_tiet']['co_nut_cuc_lon'])], [11])
da_down = sorted([(u['opaque_id'], u['root'], u['chi_tiet']['hang_root']['RHT'][0], u['chi_tiet']['hang_root']['DA'][0], u['chi_tiet']['hang_root']['K2_khong_canh_RHT'][0])
                  for u in ci if u['chi_tiet']['tac_dung_DA_len_root'] == 'giảm hạng' and not u['chi_tiet']['co_nut_cuc_lon']])
claim('KT-15: 3 ca DA giảm hạng không dính cực lớn, đều root ts-auth-service; hạng 2→15, 40→46, 10→22; không cạnh 1, 34, 22',
      [[x[1] for x in da_down], sorted((x[2], x[3], x[4]) for x in da_down)], [['ts-auth-service'] * 3, [(2, 15, 1), (10, 22, 22), (40, 46, 34)]])
a915 = BY['RE2-TT|circa_ols_da|dev-a915aa2424|seed=single']['chi_tiet']['hang_root']
claim('mục 3.5: dev-a915aa2424 hạng 3 → 29 khi bỏ cạnh', [a915['DA'][0], a915['K2_khong_canh_RHT'][0]], [3, 29])

# ---- A6. KT-4
cp = CL['theo_dataset']['Nezha-OB']['chung_phia_tren']
claim('KT-4: 40 cặp; 36 có a lớn hơn root; 24 tỷ lệ thấp hơn; còn 15 dưới tỷ lệ; còn 36 dưới số tuyệt đối; còn 36 dưới T-D; trung vị 3,4%',
      [cp['cap'], cp['a_lon_hon_root'], cp['ty_le_thap_hon_root'], cp['con_duoi_ty_le'], cp['con_duoi_tuyet_doi'], cp['con_duoi_TD'], round(cp['trung_vi_ty_le'] * 100, 1)],
      [40, 36, 24, 15, 36, 36, 3.4])

# ---- A7. A′
k = CT['A_phay']['kiem']
claim('mục 10: A′ 48 ca đủ điều kiện, 4 không', [k['so_ca_du_dieu_kien'], k['so_ca_khong_du_dieu_kien'], k['W_native_trung_ban_dong_bang_tung_bit']], [48, 4, 48])

# ---- A8. root không được ai gọi: 8 ca
claim('mục 0, D2: 8 ca root không được dịch vụ nào gọi; 15 ca không đo được', [rs[('RE2-TT', True)] + rs[('Nezha-OB', True)], sum(rs.values())], [8, 15])

# ---- B. soát chép số theo mục được dẫn
KQ = {'KQ9': T('ket-qua-phien-9.md'), 'KQ10': T('ket-qua-phien-10.md'), 'KQ11': T('ket-qua-phien-11.md')}


def sections(text):
    out = {}
    cur = None
    for line in text.split('\n'):
        m = re.match(r'^(#{2,3})\s+(\d+(?:\.\d+)?)[.\s]', line)
        if m:
            cur = m.group(2)
            out.setdefault(cur, [])
        if cur:
            out[cur].append(line)
            if '.' in cur:
                out.setdefault(cur.split('.')[0], []).append(line)
    return {k: '\n'.join(v) for k, v in out.items()}


SEC = {k: sections(v) for k, v in KQ.items()}
NUM = re.compile(r'\d+(?:[.,]\d+)*')


def nums(s):
    s = re.sub(r'`[^`]*`', ' ', s)
    return set(x.replace('.', '').replace(',', '.') if re.fullmatch(r'\d{1,3}(?:\.\d{3})+', x) else x.replace(',', '.') for x in NUM.findall(s))


CITE = re.compile(r'(KQ9|KQ10|KQ11|ket-qua-phien-9\.md`?|ket-qua-phien-10\.md`?|ket-qua-phien-11\.md`?)\s*(?:\(viết tắt KQ\d+\))?\s*mục\s+((?:\d+(?:\.\d+)?)(?:\s*(?:,|và)\s*\d+(?:\.\d+)?)*)')
ALIAS = {'ket-qua-phien-9.md': 'KQ9', 'ket-qua-phien-10.md': 'KQ10', 'ket-qua-phien-11.md': 'KQ11'}
unmatched = []
n_lines = 0
n_tokens = 0
for fn in ('nguyen-nhan-xep-hang.md', 'kiem-tiep.md', 'doc-tay.md'):
    for ln, line in enumerate(T(fn).split('\n'), 1):
        cites = CITE.findall(line)
        if not cites:
            continue
        pool = set()
        for src, secs in cites:
            src = ALIAS.get(src.rstrip('`'), src)
            for s in re.findall(r'\d+(?:\.\d+)?', secs):
                pool |= nums(SEC[src].get(s, ''))
        body = CITE.sub(' ', line)
        body = re.sub(r'\b(?:H|D|KT-|K-|Q-|WHY-|T-)\d+\b', ' ', body)
        body = re.sub(r'mục\s+\d+(?:\.\d+)?(?:\s*(?:,|và|–)\s*\d+(?:\.\d+)?)*', ' ', body)
        toks = nums(body)
        n_lines += 1
        for tkn in sorted(toks):
            n_tokens += 1
            if tkn not in pool:
                unmatched.append({'file': fn, 'line': ln, 'token': tkn, 'cited': ['%s mục %s' % (ALIAS.get(a.rstrip('`'), a), b) for a, b in cites]})

out = {'A_claims': res, 'A_all_ok': all(r['ok'] for r in res), 'A_n': len(res),
       'B_lines_with_citation': n_lines, 'B_tokens_checked': n_tokens, 'B_unmatched': unmatched}
with open(OUTP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for r in res:
    if not r['ok']:
        print('LỆCH', r)
print('A: %d claims, mismatch %d' % (len(res), sum(1 for r in res if not r['ok'])))
print('B: %d dòng có dẫn nguồn, %d số, %d số không thấy trong mục được dẫn' % (n_lines, n_tokens, len(unmatched)))
for u in unmatched:
    print('  ?', u['file'], u['line'], u['token'], u['cited'])

# ---- C. soát số của doc-tay.md với phiếu gọn (thêm sau lượt 002)
# Mỗi con số trong mục 1–6 của doc-tay.md phải có trong phiếu gọn của đúng phương pháp, chấp nhận ba cách viết lại:
# nguyên giá trị; phần trăm (giá trị × 100, làm tròn 0–2 chữ số); làm tròn tới 0–4 chữ số.
SHEET = {'1': 'tracerca', '2': 'microrank_full', '3': 'baro', '4': 'simplerca', '5': 'circa_ols_da', '6': 'torai_B'}
FNUM = re.compile(r'(?<![\w.])-?\d+(?:\.\d+)?(?:e[+-]?\d+)?')


def sheet_vals(name):
    txt = open(os.path.join(ROOT, 'runs/tong-hop-phien-12-001/phieu-gon', name + '.txt'), encoding='utf-8').read()
    vals = set()
    for x in FNUM.findall(txt):
        try:
            vals.add(float(x))
        except ValueError:
            pass
    return vals


def variants(vals):
    out = set()
    for v in vals:
        for d in range(0, 5):
            out.add(round(v, d))
            out.add(round(abs(v), d))
        for d in range(0, 3):
            out.add(round(v * 100, d))
            out.add(round(abs(v) * 100, d))
    return out


POOL = {k: variants(sheet_vals(v)) for k, v in SHEET.items()}
ALLP = set().union(*POOL.values())
doc = T('doc-tay.md')
cur = None
c_checked = 0
c_other = []
c_miss = []
for ln, line in enumerate(doc.split('\n'), 1):
    m = re.match(r'^## (\d+)\.', line)
    if m:
        cur = m.group(1)
    if cur not in SHEET or line.startswith('#'):
        continue
    body = re.sub(r'`[^`]*`', ' ', line)
    body = re.sub(r'\b(?:KT-|K-|Q-|WHY-|T-|S-|B-|M-C|k = |k=)\d+\b', ' ', body)
    body = re.sub(r'mục\s+\d+(?:\.\d+)?(?:\s*(?:,|và|–)\s*\d+(?:\.\d+)?)*', ' ', body)
    body = re.sub(r'(?:đường|điểm|đường đi)\s+\d+(?:\s*(?:,|và)\s*\d+)*', ' ', body)
    body = re.sub(r'^\s*\d+\.\s', ' ', body)
    for x in NUM.findall(body):
        if re.fullmatch(r'\d{1,3}(?:\.\d{3})+', x):
            v = float(x.replace('.', ''))
        else:
            try:
                v = float(x.replace(',', '.'))
            except ValueError:
                continue
        c_checked += 1
        if v in POOL[cur]:
            continue
        (c_other if v in ALLP else c_miss).append({'line': ln, 'section': cur, 'token': x})
out['C_doc_tay_tokens_checked'] = c_checked
out['C_found_only_in_other_method_sheet'] = c_other
out['C_not_found_in_any_sheet'] = c_miss
with open(OUTP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('C: %d số của doc-tay.md mục 1–6; %d chỉ thấy ở phiếu phương pháp khác; %d không thấy ở phiếu nào' % (c_checked, len(c_other), len(c_miss)))
for u in c_miss:
    print('  ?', u['line'], u['section'], u['token'])
print('  (khác phiếu):', [(u['line'], u['token']) for u in c_other])
